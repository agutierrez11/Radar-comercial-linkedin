import { defineConfig, devices } from "@playwright/test"
import { createServer, type AddressInfo } from "node:net"

/**
 * Dynamic free-port allocation — never collides with `localhost:3000`.
 * Override with `PORT=…` to pin a port (CI logs / debugging).
 *
 * The chosen port is also exported on `process.env.LAZYCODEX_BASE_URL` so the
 * Lighthouse spec (which spawns its own browser via the playwright fixture)
 * can construct the right base URL without hardcoding anything.
 */
async function findFreePort(): Promise<number> {
  return new Promise((resolve, reject) => {
    const server = createServer()
    server.unref()
    server.on("error", reject)
    server.listen(0, "127.0.0.1", () => {
      const address = server.address() as AddressInfo | null
      if (!address) {
        server.close()
        reject(new Error("Unable to allocate a free TCP port"))
        return
      }
      const { port } = address
      server.close((err) => (err ? reject(err) : resolve(port)))
    })
  })
}

const PORT = process.env.PORT ? Number(process.env.PORT) : await findFreePort()
process.env.PORT = String(PORT)
process.env.LAZYCODEX_BASE_URL = `http://127.0.0.1:${PORT}`
const BASE_URL = `http://127.0.0.1:${PORT}`

export default defineConfig({
  testDir: "./e2e",
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: 1,
  reporter: process.env.CI ? [["github"], ["list"]] : "list",
  timeout: 180_000,
  use: {
    baseURL: BASE_URL,
    trace: "on-first-retry",
    headless: true,
  },

  projects: [
    {
      name: "chromium",
      use: {
        ...devices["Desktop Chrome"],
        headless: true,
      },
    },
  ],

  webServer: {
    command: "pnpm run build && pnpm run start",
    env: { PORT: String(PORT) },
    url: BASE_URL,
    reuseExistingServer: !process.env.CI,
    timeout: 240_000,
    stdout: "pipe",
    stderr: "pipe",
  },
})
