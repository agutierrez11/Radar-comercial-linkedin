# packages/web Agent Notes

This package is a Next.js 16 app. Before making Next.js-specific code or config changes, read the installed version-matched docs under `node_modules/next/dist/docs/`, starting with `node_modules/next/dist/docs/index.md`.

The project also enables Next DevTools MCP through `.mcp.json` using the pinned `next-devtools-mcp@0.3.10` package. When the dev server is running, Next.js 16 exposes its MCP endpoint at `/_next/mcp`; use the MCP server for live route, metadata, logs, and error diagnostics when available.

Lighthouse tests must always use real Chrome through Playwright's `channel: "chrome"` plus the Lighthouse Node API/CDP path. Do not use the Lighthouse CLI, do not skip audits based on CI/local environment, and do not fall back to bundled Chromium.

Keep the LazyCodex visual surface unchanged unless the user explicitly asks for design changes. Treat `DESIGN.md` as the source of truth for colors, typography, spacing, image behavior, and landing/docs information architecture.
