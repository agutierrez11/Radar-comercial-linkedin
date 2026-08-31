import { expect, test } from "@playwright/test"
import { SITE_CONFIG } from "../lib/site-config"

const LAUNCH_GATING_PATTERN = new RegExp(
  [
    ["coming", "soon"],
    ["coming", "june"],
    ["codex", "edition", "is", "coming"],
    ["currently", "available", "for", "opencode"],
  ]
    .map((parts) => parts.join("\\s+"))
    .join("|"),
  "i",
)

test.describe("home page — content", () => {
  test("renders the wordmark, hero copy, and footer", async ({ page }) => {
    await page.goto("/")

    await expect(
      page.getByRole("heading", { level: 1, name: SITE_CONFIG.wordmark }),
    ).toBeVisible()

    await expect(page.getByText(SITE_CONFIG.eyebrow, { exact: true })).toBeVisible()

    await expect(page.getByText(SITE_CONFIG.heroLineA, { exact: false }).first()).toBeVisible()
    await expect(
      page.getByText(SITE_CONFIG.heroLineB.slot, { exact: false }).first(),
    ).toBeVisible()
    await expect(
      page.getByText(SITE_CONFIG.heroLineB.keyword, { exact: false }).first(),
    ).toBeVisible()

    await expect(page.getByText("lazycodex.ai", { exact: false }).first()).toBeVisible()
  })

  test("does not show launch gating copy", async ({ page }) => {
    await page.goto("/")
    const visibleText = await page.locator("body").innerText()

    expect(visibleText).not.toMatch(LAUNCH_GATING_PATTERN)
  })

  test("has a single h1 and no broken landmarks", async ({ page }) => {
    await page.goto("/")
    const h1s = await page.locator("h1").count()
    expect(h1s).toBe(1)
    await expect(page.locator("main")).toHaveCount(1)
    await expect(page.locator("footer")).toHaveCount(1)
  })

  test("skip-link is hidden until focused", async ({ page }) => {
    await page.goto("/")
    const skip = page.getByRole("link", { name: "Skip to main content" })
    await expect(skip).toHaveClass(/sr-only/)
    await skip.focus()
    await expect(skip).toBeFocused()
  })
})
