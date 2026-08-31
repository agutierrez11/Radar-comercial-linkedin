# Agent runtime brief — Design a Brand Template System like Stripe Design

## Core principle

the system is judged on whether the worst output a PM can produce is still on-brand. Optimise for the floor, not the ceiling.

## Context the agent must establish before generating

> Before producing the deck, the agent must know each item below.
> - If the user's prior messages already supply an item, use it; do NOT re-ask.
> - If an item can be reasonably inferred from the user's stated topic, infer it and state the assumption inline on slide 2.
> - Ask only what is missing AND cannot be inferred — one targeted question at a time, not a script.

1. **The brand inputs** — palette (primary + secondary + functional + chart palette), typography (display + body + 2-3 weights), grid (column count + gutter + baseline), spacing scale (4 / 8 / 16 / 24 / 40 / 64 or brand-specified). Missing inputs are flagged.
2. **Token export format** — Figma variables, JSON design tokens, PPTX theme file, Keynote theme. The system ships in the formats the user's toolchain consumes.
3. **The volume signal** — how many decks per quarter does the org produce? Drives the number of organisms and templates (more volume → more templates → less freelance composition).
4. **The user population** — PMs only / PMs + designers / PMs + execs + sales. Different populations need different constraint levels (sales decks need a more rigid template; PMs need a wider organism library).
5. **The governance owner** — who owns the system after launch? The deck cannot ship without a named maintainer.
6. **Existing artefacts to audit** — if there's an existing brand PPT template, the agent audits which of its layouts can become organisms in the new system.

## Mandatory checks (during generation)

- The system defines all four layers (atoms, molecules, organisms, templates). A "template system" that only ships layouts is rejected.
- Every colour / type / spacing value in the deck is a named token. Hard-coded hex values inside the deck are flagged.
- Every atom and molecule has a documented rule and a do/don't pair.
- The self-presentation deck is built only from documented components — no one-off slides, no off-system imagery.
- A named maintainer and contribution process appears on slide 14. Ungoverned systems decay; the agent does not ship without governance.
- Maximum two type families and three weights total across the system.
- Chart palette is part of the brand atom set; Excel-default chart colours are forbidden.
- The default neutrals are true off-white `#F8F8F6` and true white `#FFFFFF`. Cream / ivory / parchment / warm-beige (`#F5EFE3`, `#F7F3EB`, `#FAF7F2`) is forbidden as a corporate-template default — it reads as editorial / lifestyle, not enterprise.
- Every methodology claim has a citation to Frost, Atlassian, Carbon, or comparable published design-system documentation.

## Template selection

- **Stripe-style Restraint** (default, bundled): deep ink + true off-white + single accent, 12-column grid with 24px gutter, sans-serif display + sans-serif body. The shape of Stripe Design's published work.
- **Atlassian-style Documentation-Heavy** (alternate): more text-density per slide, generous do/don't pairs, for systems where the documentation visibility itself is part of the deliverable.
- **Carbon-style Industrial** (alternate): IBM Carbon-influenced; cooler greys, more functional palette, for B2B / industrial / fintech brands.

## Use the bundled deck as a starting point

The included reference deck is the ~18-slide self-presentation deck for a worked example brand template system — atomic hierarchy explained, colour tokens, type tokens, spacing tokens, molecule library, organism library, template library, do/don't pairs, chart palette, photography treatment, motion tokens, governance, token export, the self-presentation test, roadmap, credits. The agent should copy this deck and replace tokens slot-by-slot, preserving the slot grammar — every slot demonstrates a specific layer of the system, and removing one slot breaks the hierarchy proof.

## Recommended N-slide structure (the system's own self-presentation deck)

| # | Page | Purpose |
|---:|---|---|
| 1 | Cover — brand wordmark + system version | The system has a version number |
| 2 | Why this exists — the "47-layouts-failed" story | Set the problem |
| 3 | The grammar — atoms / molecules / organisms / templates explained | Methodology |
| 4 | Colour tokens — primary + secondary + functional palettes | Atom layer |
| 5 | Type tokens — type scale and pairings | Atom layer |
| 6 | Spacing + grid tokens — 4pt / 8pt scale + 12-column grid | Atom layer |
| 7 | Molecule library — title blocks, KPI cards, citations, callouts | Molecule layer |
| 8 | Organism library — full slide compositions (8-12 organisms) | Organism layer |
| 9 | Template library — cover, section divider, hero metric, compare, data, quote, end | Template layer |
| 10 | Do/Don't pairs — 6 worked examples | Live guidelines |
| 11 | Chart palette + data-viz rules | Charts are atoms too |
| 12 | Photography treatment + crop rules | Photographic atoms |
| 13 | Motion + transition tokens | Motion is part of the system |
| 14 | Governance — how new components are added, who owns the system | The system has a maintainer |
| 15 | Token export — how to consume in PPTX / Keynote / Figma | Pipeline |
| 16 | The self-presentation test — this deck was built only from the system | Proof |
| 17 | Roadmap — v1.1 components, v2 expansion areas | The system is versioned |
| 18 | Credits + maintainer + change log | Pentagram-tradition team credit |
