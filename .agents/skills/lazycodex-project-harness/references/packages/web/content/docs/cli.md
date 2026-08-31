The `lazycodex-ai` CLI is the entry point for installing and diagnosing the harness. It is meant to be run through `npx` — never install it globally.

### Forwarding to OmO

The bin reads its arguments and forwards them to `oh-my-openagent`. The `install` subcommand is special-cased to lock the Codex platform target; everything else passes through as-is.

**install** expands to:

```bash
npx lazycodex-ai install
# → npx --yes --package oh-my-openagent omo install --platform=codex
```

Arguments after `install` are appended verbatim:

```bash
npx lazycodex-ai install --no-tui --codex-autonomous
# → npx --yes --package oh-my-openagent omo install --platform=codex --no-tui --codex-autonomous
```

**Other subcommands** forward without the platform lock:

```bash
npx lazycodex-ai <args...>
# → npx --yes --package oh-my-openagent omo <args...>
```

### install

```bash
npx lazycodex-ai install
```

Installs the OmO agent harness into Codex: commands, skills, hooks, model routing, and verification defaults in one pass.

To skip the TUI and let the installer run autonomously:

```bash
npx lazycodex-ai install --no-tui --codex-autonomous
```

### `--dry-run`

Place `--dry-run` as the **first** argument to print the resolved `npx` command without executing it:

```bash
npx lazycodex-ai --dry-run install --no-tui --codex-autonomous
```

Output:

```text
npx --yes --package oh-my-openagent omo install --platform=codex --no-tui --codex-autonomous
```

`--dry-run` is stripped before forwarding, so the remaining arguments are interpreted exactly as they would be in a real run. Use it to verify the exact `omo` call before executing.

### doctor

```bash
npx lazycodex-ai doctor
```

Prints a health report: what is configured, what is missing, and why. Checks plugin cache, hooks, MCP servers, agent roles, and Codex config state. Run this first when a hook is pending, a skill is not loading, or routing looks wrong.

### Prerequisites

- [Node.js](https://nodejs.org) — any maintained LTS; `npx` ships with it. Bun is **not** required for the installer.
- The [OpenAI Codex CLI](https://github.com/openai/codex) or the Codex app, logged in.

> Do not use `npm install -g` or `bun add -g`. Always invoke via `npx`.

### Marketplace alternative

As an additive, experimental path you can install from inside Codex: type `/plugins`, open the **Add Marketplace** tab, and enter `https://github.com/code-yeongyu/lazycodex`, then install `omo` from the `sisyphuslabs` marketplace. Or from the CLI:

```bash
codex plugin marketplace add https://github.com/code-yeongyu/lazycodex
codex plugin add omo@sisyphuslabs
```

Upgrade with `codex plugin marketplace upgrade sisyphuslabs`. After an upgrade the hooks show as **Modified** — expected, because plugin files changed and the previous trust hashes no longer match. Re-approve and the next session runs the new version's bootstrap.

The npx installer above stays the primary path. See [Installation](./installation.md) for the full walkthrough.

### Exit behavior

The bin executes the resolved command with inherited stdio and exits with that command's status code. If `npx` itself fails to spawn, it prints the error and exits non-zero.

### In-session commands

Once installed, LazyCodex registers OmO commands inside Codex. These are `$command` invocations in the Codex input — not shell commands. Syntax and usage flows are collected in the [Commands](./ulw-plan.md) section.
