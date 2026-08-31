# Agent runtime brief — Clean a Content Heap like Atlassian Design

## Core principle

cleaning a deck is *deleting*, not generating. The agent's leverage move is the cut list, not the rewrite list. Default to cutting and merging before rewording; default to merging before deleting only when the cut content has a future referent (then it goes to appendix).

## Context the agent must establish before generating

> Before producing the deck, the agent must know each item below.
> - If the user's prior messages already supply an item, use it; do NOT re-ask.
> - If an item can be reasonably inferred from the user's stated topic, infer it and state the assumption inline on slide 2.
> - Ask only what is missing AND cannot be inferred — one targeted question at a time, not a script.

1. **The input deck** — slide titles + a one-line summary per slide. The agent runs the Atom Inventory on slide 1 against this.
2. **The minimum-must-survive slides** — slides the user knows cannot be cut (the architecture decision, the budget ask). These are excluded from the cut list.
3. **The deck's audience and reading occasion** — VP review (5-second-glance), team working session (30-second-study), board pre-read (read-alone offline). Calibrates line length and slide density.
4. **Pasted-content sources** — Slack screenshots, Confluence pages, notebook outputs. These are first candidates for cut-or-merge.
5. **Cut-ratio target** — default 40%; the user can override down to 30% (minimum, below which the agent flags that cleanup hasn't happened) or up to 60%.
6. *(optional)* **Style rules already in place** — line length, type weights, palette. The agent preserves any existing system rather than imposing a new one.

## Mandatory checks (during generation)

- Each kept slide has a CRAP-Atomic Slide Card naming atomic level (atom / molecule / organism) and one-sentence job. The atomic level is a chip in the slide corner, not an essay.
- Cut ratio ≥ 30% of input slides removed or merged. Below 30%, the agent flags on slide 2 that cleanup hasn't actually happened and asks the user to commit to specific cuts.
- Body text 60-80 characters per line. Over-length lines are wrapped or shortened (Atlassian rule). The agent measures, doesn't guess.
- Two type weights maximum across the deck. A third weight triggers an explicit override question.
- Pasted screenshots without commentary are merged into the next slide as a callout, or cut. Slack threads, Confluence excerpts, and notebook outputs are never standalone slides.
- One slide, one job — the slide's job sentence fits on one line. If it needs two sentences, it's two slides.
- Every methodology principle (Atomic Design, CRAP, Atlassian typography, Notion design analysis) carries a footnote citation.
- No icons except atomic-level chips (atom / molecule / organism). No decoration that isn't load-bearing — no drop shadows, no gradients, no decorative dividers, no full-bleed photos behind text.
- The accent is *cool* slate `#3F4A57`, not warm beige. Notion's published surfaces lean warm; this deck deliberately cools that.

## Template selection

- **Architecture / RFC Review** (default, bundled): engineering-review shape, code blocks and architecture diagrams as first-class atoms, decision-record callouts.
- **Ops Review** (alternate): metrics-grid emphasis, runbook callouts, incident-postmortem shape.
- **Product RFC** (alternate): user-flow diagram + decision-matrix shape, more text-heavy.
- **Design Review** (alternate): mocked-screen-grid shape, before/after comparison slides as first-class organisms, design-token callouts.
- **All-Hands Pre-Read** (alternate): one-page-per-team shape, executive-glance audience, heavy cut-and-merge before any rewrite.

## Use the bundled deck as a starting point

The included `deck/minimalist-content-cleanup-deck.slides/` is a complete reference cleanup pass built around a fictional 47-slide quarterly architecture review cut to 28 slides. The agent should copy this deck and replace content while preserving the playlist — the Atom Inventory (slide 01), the Cut List (slide 02), the Merge List (slide 03), the Atomic-Level Diagram (slide 05), and the Style-Guide Handoff (last slide) are slot-locked.

## Recommended N-slide structure

This skill operates as a *cleanup pass*, not a fixed-length deck. The output is the input deck minus 30-60% of slides. Output structure mirrors the input's outline; the table below defines the *process slides* the cleanup itself produces.

| # | Page | Purpose | Required? |
|---:|---|---|:---:|
| 1 | Atom Inventory | Audit of input deck — every repeated atom listed, duplicates flagged | **yes** |
| 2 | Cut list | Slides recommended for deletion (with one-line reason each) | **yes** |
| 3 | Merge list | Slide pairs/triples recommended to combine | **yes** |
| 4 | Rewrite list | Slides that pass cut/merge but fail CRAP audit | **yes** |
| 5 | Atomic-level diagram | Kept slides classified atom / molecule / organism | **yes** |
| 6+ | Per-kept-slide CRAP-Atomic Slide Card | One card per remaining slide | **yes** |
| N-2 | New TOC | Cleaned outline showing before/after slide count | yes |
| N-1 | Style rules going forward | Line length, spacing, type weights, palette | **yes** |
| N | Style-guide handoff | Atomic + CRAP rules as a printable one-pager for the team | **yes** |

*(Typical input: 40-80 slides; typical output: 18-35 slides; cut ratio target: 40-55%.)*
