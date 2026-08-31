Multi-model routing sends each part of a run to the model that fits it best, instead of running everything on one model. LazyCodex installs OmO's routing defaults into Codex so a serious repository is not bottlenecked by a single context window or price point.

### Current baseline

The `4.12.1` bundled `model-catalog.json` centers the default profile on `gpt-5.5`:

| Profile | Model | Reasoning |
| --- | --- | --- |
| Default | `gpt-5.5` | `high` |
| Plan mode | `gpt-5.5` | `xhigh` |
| Worker | `gpt-5.5` | `high` |
| Verifier | `gpt-5.5` | `high` |

The actual model name you see may differ as Codex and OpenAI update their model lineup. This doc focuses on *how* LazyCodex uses model profiles, not on comparing specific models.

### What gets routed

- **Planning and exploration** go to a strong reasoning model that can hold a large context and weigh trade-offs.
- **Implementation turns** go to a fast, capable coding model for the bulk of the edit loop.
- **Verification** goes to a model used as an oracle, chosen for judgment rather than throughput.
- **Specialist skills** can target their own model when a skill benefits from a specific profile.

### Why role profiles exist

Role-based profiles separate work by nature:

- General tasks follow the default model setting.
- Plan mode may demand stronger reasoning.
- Worker and verifier are kept separate so the same result is checked from a different angle.

This pairs with [Agent Roles](./discipline-agents.md). Even when multiple roles move in parallel, each role's model profile is tracked in the Codex configuration.

### How it fits the harness

Routing is part of the harness setup that `npx lazycodex-ai install` wires into Codex. It detects the available subscriptions and provider auth, then maps roles to models so you do not hand-configure each one.

### Provider auth

Auth targets Codex itself, not LazyCodex. Once Codex is logged in, the installer's subscription detection and provider routing take over. If you let an LLM agent run the install, it walks the same detection and selection for you.

### User notes

- The model name you see after install may differ from what the docs list. The installed `model-catalog.json` and the models your Codex build supports take precedence.
- Model settings balance quality and speed. Lowering them arbitrarily can degrade planning, review, and QA quality together.
- When in doubt, check install state and Codex config first.

### Customizing it

Routing and provider settings live in the configuration. See [Configuration](./configuration.md) for the fields that control which model handles which role, and how to override the defaults per project.
