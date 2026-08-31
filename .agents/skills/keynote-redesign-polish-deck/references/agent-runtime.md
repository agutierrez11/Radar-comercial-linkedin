# Agent runtime brief — Redesign a Deck like Apple Keynote design lead

## Core principle

the worst-case slide determines the perception of the deck — optimise for the floor, not the ceiling. Every slide must defend its existence as one idea expressed visually.

## Context the agent must establish before generating

> Before producing the deck, the agent must know each item below.
> - If the user's prior messages already supply an item, use it; do NOT re-ask.
> - If an item can be reasonably inferred from the user's stated topic, infer it and state the assumption inline on slide 2.
> - Ask only what is missing AND cannot be inferred — one targeted question at a time, not a script.

1. **The existing deck** — slide count, format (PPTX / PDF / Google Slides / Keynote), and a one-line summary of what it's trying to do.
2. **The high-stakes moment** — what is this deck for? (Launch event / external keynote / board meeting / sales pitch.) The bar for negative space scales with the audience.
3. **Background mode** — black or white? Pick one and hold it across the deck. Mixed black-and-white decks are flagged.
4. **The accent color** — Apple-blue `#0071E3` by default, otherwise a single brand color. Multi-color accent palettes are reduced to one.
5. **The runtime budget** — how many minutes does the presenter have? Drives the slide count and the depth of the cut.
6. **The "must keep" slides** — any slide the user cannot lose (a regulatory disclosure, a single chart). These are flagged as slot-locked.

## Mandatory checks (during generation)

- Every redesigned slide is one idea, one verb, one image or one chart, ≤15 words.
- Every multi-bullet input slide is split into separate slides with builds rather than compressed.
- 50% of every slide canvas is empty space (the agent measures pixel coverage of the rendered slide).
- One type family at two weights across the whole deck. Three-weight decks are flagged.
- Background is pure black `#000000` or pure white `#FFFFFF` for every slide. Cream / ivory / parchment / warm-beige (`#F5EFE3`, `#F7F3EB`, `#FAF7F2`) is forbidden — Apple's keynote canon is pure black or pure white only.
- Stock business photography ("handshake", "diverse team at laptop") is replaced with product photography on the background colour, or removed entirely.
- The Slide Diet Tracker at the back records the word count delta and design move for every input slide. Slides cut entirely are listed with reason ("merged into slide 4", "moved to website").
- Every claim in the redesigned deck that came from the original retains its source citation.

## Template selection

- **Black Keynote** (default, bundled): pure black `#000000` background, SF Pro Display white type, single accent. The shape of the 2007 iPhone keynote.
- **White Keynote** (alternate): pure white `#FFFFFF` background, SF Pro Display black type, single accent. The shape of later product-page launches.
- **Build-heavy** (alternate, for technical product talks): black or white background but every slide is a sequenced build of 2-5 elements — for deep-dive product walkthroughs.

## Use the bundled deck as a starting point

The included reference deck demonstrates the redesign on a representative "before" deck — a 30-slide engineer-written product pitch with bullet-list density — alongside the rebuilt "after" version at the same slide count. The agent should copy the after-deck's slot grammar (cover word + image, why-now sentence, 200pt single number, body slides at one idea each, single ask, contact card, Slide Diet Tracker) and apply it to the user's input.

## Recommended N-slide structure

The redesigned deck is typically the same length as the input or shorter. For a representative 30-slide business deck redesigned into ~24 slides:

| # | Page | Purpose |
|---:|---|---|
| 1 | Cover — one word + one image | Product name, no tagline |
| 2 | Why now — one sentence full-bleed | Replaces "Agenda" |
| 3 | The one number — single stat at 200pt | Replaces 3-bullet market overview |
| 4–N-3 | Body slides — one idea each | One verb, one image or one chart, one sentence ≤15 words |
| N-2 | The ask — one sentence | What the audience should do |
| N-1 | Thank-you — name + email only | No "next steps" bullets |
| N | Slide Diet Tracker — word-count delta table | The surgery, auditable |

The agent reports: input slide count, output slide count, total word reduction %, slides flagged for further surgery.
