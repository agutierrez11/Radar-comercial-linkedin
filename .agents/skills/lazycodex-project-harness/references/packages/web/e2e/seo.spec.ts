import { expect, test } from "@playwright/test"

const LAUNCH_GATING_PATTERN = new RegExp(
  [
    ["coming", "soon"],
    ["coming", "june"],
    ["currently", "available", "for", "opencode"],
  ]
    .map((parts) => parts.join("\\s+"))
    .join("|"),
  "i",
)

function readPngDimensions(buffer: Buffer): { width: number; height: number } {
  const pngSignature = "89504e470d0a1a0a"
  expect(buffer.subarray(0, 8).toString("hex")).toBe(pngSignature)

  return {
    width: buffer.readUInt32BE(16),
    height: buffer.readUInt32BE(20),
  }
}

test.describe("site SEO + metadata", () => {
  test("has a unique <title>, description, canonical, lang, viewport", async ({ page }) => {
    await page.goto("/")

    await expect(page).toHaveTitle(/LazyCodex.*Codex/i)

    const description = await page.locator('meta[name="description"]').getAttribute("content")
    expect(description).toBeTruthy()
    expect(description?.length).toBeGreaterThan(50)
    expect(description?.length).toBeLessThanOrEqual(170)
    expect(description).toMatch(/Codex/i)
    expect(description).toMatch(/agent harness/i)
    expect(description).toMatch(/complex codebases/i)
    expect(description).not.toMatch(LAUNCH_GATING_PATTERN)

    const canonical = await page.locator('link[rel="canonical"]').getAttribute("href")
    // Next.js metadataBase + canonical: "/" can resolve to either with or
    // without trailing slash depending on the App Router version. Accept
    // both; the SEO contract is "the canonical URL points to the apex".
    expect(canonical).toMatch(/^https:\/\/lazycodex\.ai\/?$/)

    const lang = await page.locator("html").getAttribute("lang")
    expect(lang).toBe("en")

    const viewport = await page.locator('meta[name="viewport"]').getAttribute("content")
    expect(viewport).toMatch(/width=device-width/)
  })

  test("has OpenGraph and Twitter card tags", async ({ page }) => {
    await page.goto("/")

    await expect(page.locator('meta[property="og:title"]')).toHaveAttribute(
      "content",
      /LazyCodex/,
    )
    await expect(page.locator('meta[property="og:description"]')).toHaveAttribute(
      "content",
      /Codex/,
    )
    await expect(page.locator('meta[property="og:type"]')).toHaveAttribute("content", "website")
    await expect(page.locator('meta[property="og:url"]')).toHaveAttribute(
      "content",
      "https://lazycodex.ai",
    )
    await expect(page.locator('meta[property="og:image"]')).toHaveCount(1)

    await expect(page.locator('meta[name="twitter:card"]')).toHaveAttribute(
      "content",
      "summary_large_image",
    )
    await expect(page.locator('meta[name="twitter:image"]')).toHaveCount(1)
  })

  test("has JSON-LD SoftwareApplication structured data", async ({ page }) => {
    await page.goto("/")
    const jsonLd = await page.locator('script[type="application/ld+json"]').textContent()
    expect(jsonLd).toBeTruthy()
    const parsed = JSON.parse(jsonLd ?? "{}")
    expect(parsed["@type"]).toBe("SoftwareApplication")
    expect(parsed.name).toBe("LazyCodex")
    expect(parsed.url).toBe("https://lazycodex.ai")
  })

  test("/robots.txt and /sitemap.xml are reachable", async ({ request }) => {
    const robots = await request.get("/robots.txt")
    expect(robots.status()).toBe(200)
    const robotsText = await robots.text()
    expect(robotsText).toMatch(/Allow:\s*\//i)
    expect(robotsText).toMatch(/Sitemap:\s*https:\/\/lazycodex\.ai\/sitemap\.xml/i)

    const sitemap = await request.get("/sitemap.xml")
    expect(sitemap.status()).toBe(200)
    const sitemapText = await sitemap.text()
    expect(sitemapText).toMatch(/<loc>https:\/\/lazycodex\.ai\/<\/loc>/i)
    expect(sitemapText).toMatch(/<loc>https:\/\/lazycodex\.ai\/docs<\/loc>/i)
  })

  test("/docs route is reachable", async ({ request }) => {
    const docs = await request.get("/docs")
    expect(docs.status()).toBe(200)
  })

  test("/manifest.webmanifest is reachable and valid", async ({ request }) => {
    const manifest = await request.get("/manifest.webmanifest")
    expect(manifest.status()).toBe(200)
    const parsed = await manifest.json()
    expect(parsed.name).toBe("LazyCodex")
    expect(parsed.start_url).toBe("/")
  })

  test("opengraph image and twitter image render as PNGs", async ({ request }) => {
    // given
    const expectedSize = { width: 1200, height: 630 }

    // when
    const og = await request.get("/opengraph-image")

    // then
    expect(og.status()).toBe(200)
    expect(og.headers()["content-type"]).toMatch(/image\/png/)
    expect(readPngDimensions(await og.body())).toEqual(expectedSize)

    // when
    const tw = await request.get("/twitter-image")

    // then
    expect(tw.status()).toBe(200)
    expect(tw.headers()["content-type"]).toMatch(/image\/png/)
    expect(readPngDimensions(await tw.body())).toEqual(expectedSize)
  })

  test("serves the unified LazyCodex favicon assets", async ({ page, request }) => {
    await page.goto("/")

    const iconHref = await page.locator('link[rel="icon"]').getAttribute("href")
    expect(iconHref).toContain("/icon.svg")
    expect(iconHref).not.toContain("/icon.png")

    const svgIcon = await request.get("/icon.svg")
    expect(svgIcon.status()).toBe(200)
    expect(svgIcon.headers()["content-type"]).toMatch(/image\/svg\+xml/)
    expect(await svgIcon.text()).toContain("LazyCodex mark")

    const appleIconHref = await page.locator('link[rel="apple-touch-icon"]').getAttribute("href")
    expect(appleIconHref).toContain("/apple-icon.png")

    const appleIcon = await request.get("/apple-icon.png")
    expect(appleIcon.status()).toBe(200)
    expect(appleIcon.headers()["content-type"]).toMatch(/image\/png/)
    expect(readPngDimensions(await appleIcon.body())).toEqual({ width: 180, height: 180 })
  })
})
