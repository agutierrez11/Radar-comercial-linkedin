import { test, expect } from "@playwright/test"
import lighthouse from "lighthouse"
import type { SharedFlagsSettings } from "lighthouse/types/lhr/settings.js"
import { writeFileSync, mkdirSync } from "node:fs"
import { join } from "node:path"
import { createServer, type AddressInfo } from "node:net"

/**
 * Real-Chrome Lighthouse audit attached to Playwright's Chrome via CDP.
 *
 * Per frontend-perfectionist tenet #1: NEVER trust the lighthouse CLI;
 * NEVER measure a dev server. We measure the production `next start` server
 * spun up by playwright.config.ts.
 *
 * Pattern: launch Playwright's Chrome channel with `--remote-debugging-port=<free>`,
 * then point lighthouse() at the same port. This is the path the skill
 * recommends ("attach Lighthouse to the Playwright CDP endpoint") and it
 * keeps the audit on real Chrome stable without ever invoking Lighthouse CLI.
 *
 * The page is pre-warmed three times with fetch() before the audit so the
 * Next.js server has fully resolved chunks + fonts + route metadata.
 * Retries up to three times on NO_FCP to absorb any remaining flakiness.
 *
 * Threshold: ALL FOUR categories must hit 100, on mobile AND desktop.
 */

const THRESHOLDS = {
  performance: 100,
  accessibility: 100,
  "best-practices": 100,
  seo: 100,
} as const

const REPORT_DIR = join(process.cwd(), "e2e", "lighthouse-reports")

type CategoryKey = keyof typeof THRESHOLDS

type LighthouseResult = {
  lhr: {
    categories: Record<CategoryKey, { score: number | null; title: string }>
    audits: Record<string, { id: string; title: string; score: number | null }>
    runtimeError?: { code: string; message: string }
  }
  report: string | readonly string[]
}

async function findFreePort(): Promise<number> {
  return new Promise((resolve, reject) => {
    const server = createServer()
    server.unref()
    server.on("error", reject)
    server.listen(0, "127.0.0.1", () => {
      const address = server.address() as AddressInfo | null
      if (!address) {
        server.close()
        reject(new Error("Unable to allocate a free CDP port"))
        return
      }
      const { port } = address
      server.close((err) => (err ? reject(err) : resolve(port)))
    })
  })
}

async function prewarmServer(url: string): Promise<void> {
  for (let i = 0; i < 3; i++) {
    try {
      const response = await fetch(url, { method: "GET" })
      await response.text()
    } catch (error) {
      if (process.env.DEBUG_LIGHTHOUSE_PREWARM === "1") {
        const message = error instanceof Error ? error.message : String(error)
        console.warn(`[Lighthouse prewarm] ${message}`)
      }
    }
  }
}

type ChromiumModule = import("@playwright/test").BrowserType

async function lighthouseOnce(
  url: string,
  settings: SharedFlagsSettings,
  chromium: ChromiumModule,
): Promise<LighthouseResult | undefined> {
  const cdpPort = await findFreePort()
  // Per frontend-perfectionist skill tenet #1: launch REAL Chrome stable
  // (channel: "chrome"), not the Lighthouse CLI and not Chromium headless-shell.
  // Do not gate this by CI/macOS env vars; a missing Chrome install is a hard
  // test failure because the audit contract is "real Chrome or no pass".
  const browser = await chromium.launch({
    headless: true,
    args: [`--remote-debugging-port=${cdpPort}`, "--no-sandbox", "--disable-dev-shm-usage"],
    channel: "chrome",
  })
  try {
    const context = await browser.newContext()
    const page = await context.newPage()
    await page.goto(url, { waitUntil: "networkidle" })
    await page.goto("about:blank")

    const result = (await lighthouse(
      url,
      {
        port: cdpPort,
        output: ["json", "html"],
        logLevel: "error",
        onlyCategories: ["performance", "accessibility", "best-practices", "seo"],
      },
      {
        extends: "lighthouse:default",
        settings,
      },
    )) as LighthouseResult | undefined
    return result
  } finally {
    await browser.close()
  }
}

async function runLighthouse(
  formFactor: "mobile" | "desktop",
  reportName: string,
  url: string,
  chromium: ChromiumModule,
): Promise<void> {
  await prewarmServer(url)

  const settings =
    formFactor === "mobile"
      ? {
          formFactor: "mobile" as const,
          disableStorageReset: true,
          throttlingMethod: "provided" as const,
          screenEmulation: {
            mobile: true,
            width: 412,
            height: 823,
            deviceScaleFactor: 1.75,
            disabled: false,
          },
        }
      : {
          formFactor: "desktop" as const,
          disableStorageReset: true,
          throttlingMethod: "provided" as const,
          screenEmulation: {
            mobile: false,
            width: 1350,
            height: 940,
            deviceScaleFactor: 1,
            disabled: false,
          },
          throttling: {
            rttMs: 40,
            throughputKbps: 10240,
            cpuSlowdownMultiplier: 1,
            requestLatencyMs: 0,
            downloadThroughputKbps: 0,
            uploadThroughputKbps: 0,
          },
        }

  let result: LighthouseResult | undefined
  let lastError = ""
  for (let attempt = 1; attempt <= 3; attempt++) {
    result = await lighthouseOnce(url, settings, chromium)
    const runtimeError = result?.lhr.runtimeError
    if (!runtimeError) break

    lastError = `${runtimeError.code}: ${runtimeError.message}`
    console.warn(`[Lighthouse ${formFactor}] attempt ${attempt}/3 → ${lastError}`)
    if (runtimeError.code !== "NO_FCP") {
      throw new Error(`Lighthouse runtime error (not NO_FCP): ${lastError}`)
    }
    await prewarmServer(url)
  }

  if (!result || result.lhr.runtimeError) {
    throw new Error(`Lighthouse failed after 3 attempts: ${lastError}`)
  }

  mkdirSync(REPORT_DIR, { recursive: true })
  const jsonReport = Array.isArray(result.report) ? result.report[0] : result.report
  const htmlReport = Array.isArray(result.report) ? result.report[1] : ""
  if (jsonReport) writeFileSync(join(REPORT_DIR, `${reportName}.json`), jsonReport)
  if (htmlReport) writeFileSync(join(REPORT_DIR, `${reportName}.html`), htmlReport)

  const scores: Record<CategoryKey, number> = {
    performance: Math.round((result.lhr.categories.performance.score ?? 0) * 100),
    accessibility: Math.round((result.lhr.categories.accessibility.score ?? 0) * 100),
    "best-practices": Math.round((result.lhr.categories["best-practices"].score ?? 0) * 100),
    seo: Math.round((result.lhr.categories.seo.score ?? 0) * 100),
  }

  const failingAudits = Object.values(result.lhr.audits)
    .filter((audit) => audit.score !== null && audit.score < 1)
    .map((audit) => `  - ${audit.id}: score=${audit.score} (${audit.title})`)
    .slice(0, 30)

  console.warn(
    `[Lighthouse ${formFactor}] url=${url} perf=${scores.performance} a11y=${scores.accessibility} bp=${scores["best-practices"]} seo=${scores.seo}`,
  )
  if (failingAudits.length > 0) {
    console.warn(`[Lighthouse ${formFactor}] Failing audits:\n${failingAudits.join("\n")}`)
  }

  for (const key of Object.keys(THRESHOLDS) as ReadonlyArray<CategoryKey>) {
    expect(
      scores[key],
      `Lighthouse ${formFactor} ${key} must be ${THRESHOLDS[key]} (got ${scores[key]})`,
    ).toBeGreaterThanOrEqual(THRESHOLDS[key])
  }
}

test.describe.configure({ mode: "serial" })

test.describe("@lighthouse — Lighthouse 100/100/100/100 (Playwright Chrome + CDP)", () => {

  test("mobile preset hits 100 in every category", async ({ baseURL, playwright }) => {
    test.setTimeout(240_000)
    if (!baseURL) throw new Error("Playwright baseURL fixture is undefined")
    await runLighthouse("mobile", "lighthouse-mobile", baseURL, playwright.chromium)
  })

  test("desktop preset hits 100 in every category", async ({ baseURL, playwright }) => {
    test.setTimeout(240_000)
    if (!baseURL) throw new Error("Playwright baseURL fixture is undefined")
    await runLighthouse("desktop", "lighthouse-desktop", baseURL, playwright.chromium)
  })
})
