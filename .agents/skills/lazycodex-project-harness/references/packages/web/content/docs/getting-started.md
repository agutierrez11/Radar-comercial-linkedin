LazyCodex is most useful as a harness for complex codebases: project memory, planning, execution, verified completion, skills, hooks, model routing, and diagnostics. This page walks through install verification and the four commands you will reach for most often.

### Prerequisites

- `npx` available from a Node.js/npm install. Bun is not required.
- Codex App or [OpenAI Codex CLI](https://github.com/openai/codex).

LazyCodex connects OmO commands, skills, and hooks into Codex configuration. If Codex is working normally, the install flow is the same for App and CLI.

### Install

The simplest approach: open a new task in Codex, give it the LazyCodex GitHub link, and ask it to install.

```text
https://github.com/code-yeongyu/lazycodex

Install LazyCodex from this repository.
```

If you prefer running the command directly:

```bash
npx lazycodex-ai install
```

After install, reopen Codex and check that OmO commands and skills appear in the `$` menu. The next launch asks you to approve the `omo` hooks in the startup review — hooks do not run before approval.

If the status shows `pending` or `degraded`, run the diagnostic first:

```bash
npx lazycodex-ai doctor
```

### Authentication

LazyCodex has no separate login. The installer (or the agent running it) handles subscription detection, model selection, and provider auth. Codex App or Codex CLI must already be logged in, but that is a prerequisite rather than a LazyCodex-specific step.

See [Configuration](./configuration.md) for provider and routing details.

### The four commands

| Command | Use it when |
| --- | --- |
| `$init-deep` | The repository is too large or too old to explain from memory. |
| `$ulw-plan` | The work needs decisions before any code is written. |
| `$start-work` | A plan exists and should be executed to completion. |
| `$ulw-loop` | You want the agent to keep going until the result is verified. |

### Your first run

Start by giving the agent project context with hierarchical `AGENTS.md` memory:

```text
$init-deep
```

Then pick the command that matches your task.

**If you need to plan first** — this reads the repository and writes a decision-complete plan without touching product code. Approve the plan before it executes.

```text
$ulw-plan "add a done-toggle helper to the small task app"
```

**If a plan already exists** — execute it. All checkboxes must complete before it stops.

```text
$start-work
```

**If you want end-to-end verified completion** — the loop keeps going until evidence proves the result.

```text
$ulw-loop "fix the payment flow failure and verify end to end"
```

### How to choose

Start with `$init-deep` once per repository so agents have hierarchical `AGENTS.md` context to work from.

For anything ambiguous, run `$ulw-plan` first. It interviews you, explores the codebase in parallel, and writes a decision-complete plan to `plans/<slug>.md` without touching product code.

Hand that plan to `$start-work` to execute it: durable Boulder state, parallel subagents, strict TDD, and five evidence gates. It prints `ORCHESTRATION COMPLETE` when every checkbox is done.

`$ulw-loop` is the tightest loop — use it for a single task that must run until an oracle verifies completion. It does not plan; it executes and verifies.

### A typical session

```text
$init-deep
$ulw-plan "add rate limiting to the api gateway"
$start-work plans/add-rate-limiting.md
```

If the job is small and well-understood, skip the plan and loop directly:

```text
ulw fix the flaky checkout test
```

See [Feature coverage](./skills.md) for the skills that add specialist judgment around these commands.
