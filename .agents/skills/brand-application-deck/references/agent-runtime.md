# Agent runtime brief — Apply a Brand like Pentagram

## Core principle

the skill *applies* a brand system; it does not *invent* one. The user must supply the brand. If the brand inputs are incomplete, the agent asks for them rather than guessing.

## Context the agent must establish before generating

> Before producing the deck, the agent must know each item below.
> - If the user's prior messages already supply an item, use it; do NOT re-ask.
> - If an item can be reasonably inferred from the user's stated topic, infer it and state the assumption inline on slide 2.
> - Ask only what is missing AND cannot be inferred — one targeted question at a time, not a script.

1. **The brand system inputs** — palette (primary + secondary + functional), typography (display + body + weights), logo (lockups + clear-space rules), grid (column count + gutter), photography treatment (colour-grade + crop ratios), chart palette, transition language. Missing inputs are flagged; the agent does not invent.
2. **The existing deck** — slide count, format, and the one-line external purpose.
3. **The audience** — Fortune 500 RFP / investor partner / industry conference / employee all-hands. Different audiences expect different brand-application registers.
4. **Brand-supplied photography** — does the user have a brand image library? If not, the agent uses placeholder studio photography rebuilt to the brand's colour-grade.
5. **Chart palette spec** — does the brand publish a data-viz spec? If yes, every chart inherits it; if no, default to single-colour bar charts using the brand primary.
6. **Mandatory legal / compliance elements** — disclaimers, regulatory marks, partner co-brand lockups. The agent applies these in brand-correct positions rather than as PowerPoint corner-stickers.

## Mandatory checks (during generation)

- All seven brand systems (logo, typography, palette, grid, photography, charts, transitions) are inherited on every slide. The Brand-Decision Map records the inherited decision per slide per system.
- Maximum three type weights total across the entire deck (Vignelli / Pentagram restraint).
- The typography pairing is constant across the deck — no slide uses a font outside the brand's specified display + body pairing.
- Every chart inherits the brand palette; Excel-default chart colours (Office blue/orange) are rewritten.
- Existing images are rebuilt to the brand's colour-grade (e.g., 10% primary overlay if the brand publishes one). Stock-photo aesthetic ("handshake", "diverse team at laptop") is replaced or removed.
- The logo is placed at brand-spec size and clear-space; oversized cover logos are reduced.
- The Brand-Decision Map appendix is present and complete — one row per slide × seven systems.
- Every external claim retains its source citation from the original deck.
- The palette defaults to high-contrast cool (navy `#0F2540` + electric blue `#0066FF` + white `#FFFFFF`) only when the user supplies no brand palette. Cream / ivory / parchment / warm-beige (`#F5EFE3`, `#F7F3EB`, `#FAF7F2`) is never used as a default — it is only applied if the user's brand system explicitly specifies a warm-bone palette.

## Template selection

- **Pentagram Curatorial** (default, bundled): generous white space, single hero image per slide, restrained type, footer brand mark. The shape of Pentagram's case-study slide work.
- **Wolff Olins Brand-Strategy** (alternate): strategy diagrams alongside brand imagery, for decks that need to carry strategic content under a brand surface.
- **Bibliothèque Editorial** (alternate): higher type-density, magazine-grid layouts, for editorial-feeling brand decks (publishing, content, media).

## Use the bundled deck as a starting point

The included reference deck is a complete 16-slide brand-applied enterprise pitch demonstrating the seven-system audit on a worked example brand. The agent should copy this deck and replace content while preserving the slot grammar — cover with brand mark, brand-locked agenda, palette-signature why-now, body slides with brand grid applied, brand data-viz slide, brand photography close, credits with brand-correct contact card, Brand-Decision Map appendix. The slot grammar is locked; the brand inputs are not.

## Recommended N-slide structure

A typical 16-slide brand-applied enterprise pitch (the bundled reference deck):

| # | Page | Purpose |
|---:|---|---|
| 1 | Cover — brand wordmark + one brand image | The brand on stage |
| 2 | Brand-locked agenda — type system shown | First-pass typography proof |
| 3 | Why-now statement — single brand colour block | Palette signature |
| 4–13 | Body slides — brand grid applied to existing content | Systemic application across 10 slides |
| 14 | Data slide — chart palette inherited from brand | Brand data-viz proof |
| 15 | Closing — brand photography treatment | Photographic signature |
| 16 | Credits — type pairing locked, brand contact card | Brand-correct close |
| Appendix | Brand-Decision Map — 7-system audit per slide | The proof of systemic application |
