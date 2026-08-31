One command installs the OmO agent harness for Codex without a global package install.

### Prerequisites

- [Node.js](https://nodejs.org) — any maintained LTS; `npx` ships with it. Bun is **not** required: the installer runs on plain Node.
- [OpenAI Codex](https://github.com/openai/codex): the **Codex App** (recommended) or the **Codex CLI**.

LazyCodex runs *inside* Codex. Codex must be installed and logged in before you start. If you are setting up for the first time, the Codex App is the easier path — you can open a project and run `$command` directly from the GUI.

> Do NOT use `npm install -g` or `bun add -g`. Always invoke via `npx`.

### Install

The command is one line. No global install, no setup files.

```bash
npx lazycodex-ai install
```

This is exactly equivalent to `npx --yes --package oh-my-openagent omo install --platform=codex`.

To skip the TUI and run a fully autonomous, prompt-free setup:

```bash
npx lazycodex-ai install --no-tui --codex-autonomous
```

The installer connects commands, skills, hooks, model routing, and verification defaults into your Codex configuration. It is strongly recommended to let an LLM agent run the install — the agent handles subscription detection, model selection, and provider auth automatically.

After install, the next Codex launch asks you to approve the `omo` hooks in the startup review. Hooks do not run before approval.

If the install feels like too many steps, you do not have to run the command yourself. Open Codex and give it the [lazycodex.ai](https://lazycodex.ai) link, then ask it to install LazyCodex. The agent reads the docs and walks the setup.

> **Stuck?** Join the [LazyCodex Discord](https://discord.gg/6ztZB9jvWq) and ask **Jobdori** for help.

### Install from the Codex marketplace (experimental)

The npx installer above stays the primary path. As an additive, experimental alternative you can install from inside Codex itself: type `/plugins`, open the **Add Marketplace** tab ("Add a marketplace from a Git repo or local root."), and enter `https://github.com/code-yeongyu/lazycodex`, then install `omo` from the `sisyphuslabs` marketplace. Or from the CLI:

```bash
codex plugin marketplace add https://github.com/code-yeongyu/lazycodex
codex plugin add omo@sisyphuslabs
```

On the next launch, approve the omo hooks in Codex's startup review — hooks never run before approval. The first approved session prints `LazyCodex bootstrap running in background — restart the session when it completes` while a background worker finishes the setup (config blocks, agent roles, bin links, a pinned `sg` binary for the `ast_grep` MCP); restart when it is done. The marketplace path never touches Codex permission settings — autonomous mode remains the explicit `npx lazycodex-ai install --no-tui --codex-autonomous` choice.

Upgrade with `codex plugin marketplace upgrade sisyphuslabs`. The next startup review shows the hooks as **Modified** — expected after every upgrade, because the plugin files changed and the previous trust hashes no longer match — re-approve them and the following session re-runs bootstrap on the new version. If anything looks pending or degraded, `npx lazycodex-ai doctor` explains what and why.

### Authentication

Auth targets **Codex itself**, not LazyCodex. The Codex CLI logs in during its own setup; the Codex App logs in through the app UI. There is no separate LazyCodex login command.

Once Codex is logged in, `npx lazycodex-ai install` handles subscription detection, model selection, and provider routing. If you let an LLM agent run the install, it walks the same process for you.

To check what is configured:

```bash
npx lazycodex-ai doctor
```

`doctor` explains what is set up, what is missing, and why it matters. See [Configuration](./configuration.md) for provider and routing details.

### Windows

Native Windows works with both install paths.

- **Node:** `npx lazycodex-ai install` needs Node.js on `PATH` (LTS recommended). On marketplace installs the bootstrap step provisions a pinned Node LTS runtime into `%USERPROFILE%\.codex\runtime\node\` automatically when `node` is missing — installing Node yourself first also works and skips the download.
- **Git Bash:** required for shell hooks. The installer and the marketplace bootstrap both try `winget install --id Git.Git -e --source winget` when Git Bash is missing. If Git lives somewhere custom, set `OMO_CODEX_GIT_BASH_PATH` to a path like `C:\Program Files\Git\bin\bash.exe`.
- **`where bash` shows `C:\Windows\System32\bash.exe`:** that is the WSL launcher, not Git Bash — LazyCodex intentionally ignores `System32` and `WindowsApps` `bash.exe` shims when resolving Git Bash. Install Git for Windows or point `OMO_CODEX_GIT_BASH_PATH` at a real Git Bash so the resolver finds it.
- **Troubleshooting:** the Windows marketplace bootstrap writes a transcript to `%USERPROFILE%\.codex\plugins\data\omo-sisyphuslabs\bootstrap\ps-bootstrap.log`; degraded lines look like `degraded component=node reason=... hint=npx lazycodex-ai doctor`. Run `npx lazycodex-ai doctor` for the full health report.

### Let an agent do it

It is strongly recommended to let an LLM agent run the install and walk the setup for you. The agent handles subscription detection, model selection, and provider auth automatically.
