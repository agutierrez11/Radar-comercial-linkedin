`$init-deep` generates hierarchical `AGENTS.md` context so agents start from local guidance before touching a large repository. Run it once per project, and again whenever the architecture shifts enough that the existing context no longer reflects reality.

### What it produces

- A root `AGENTS.md` that orients agents to the project: stack, layout, conventions, and where to look first.
- Nested `AGENTS.md` files in the directories that matter most, so an agent descending into a package gets scoped guidance instead of guessing.
- References to project rules, skills, and instruction files the harness should respect.

### When to run it

- Onboarding a repository that is too large or too old to explain from memory.
- After a major refactor, migration, or layout change.
- When agents keep picking the wrong files or ignoring local conventions.

### How to use it

```text
$init-deep
```

The command walks the tree, reads the files that define how the project actually works, and writes the context. Review the generated `AGENTS.md` files, trim anything stale, and commit them. Agents in later turns read that context before they edit, so the first session pays for every session after it.

### After init

With context in place, move to [`$ulw-plan`](./ulw-plan.md) when the work needs a plan, or [`$ulw-loop`](./ulw-loop.md) for a single verified task.
