# Agent runtime brief — Art-direct an Annual Report like a Magazine art director

## Core principle

an annual report is a *system*, not a series of pages. The art director's job is to define rules that hold across 80-200 spreads — and the system is judged by the spread you didn't art-direct (the financial appendix), not the one you did (the cover).

## Context the agent must establish before generating

> Before producing the deck, the agent must know each item below.
> - If the user's prior messages already supply an item, use it; do NOT re-ask.
> - If an item can be reasonably inferred from the user's stated topic, infer it and state the assumption inline on slide 2.
> - Ask only what is missing AND cannot be inferred — one targeted question at a time, not a script.

1. **Filing target** — 10-K / S-1 / impact report / sustainability report / hybrid. Calibrates legal-typesetting requirements (risk-factor sections for S-1).
2. **Stance** — substance (Berkshire-class, monospaced-feel anti-design) or polish (Patagonia-class, editorial-confessional). The agent will not let a deck mix both.
3. **One reference report the CEO loves** — and one reference the CFO loves. The agent calls out where they conflict on slide 2.
4. **Photographer or photo discipline** — named photographer (Tim Davis, Catherine Opie, Joel Meyerowitz scale) OR one disciplined photo style (e.g., "documentary, available light, environmental portraits only"). Never a stock mix.
5. **Type system in two weights** — display + body; the agent flags any third weight.
6. **Cover concept in one sentence** — a single image, a single-word or single-line title.
7. *(optional)* **Production specs** — trim, paper, ink, finishing; or digital-export spec if web-only.
8. *(optional)* **Schedule** — editorial / photo / typesetting / press milestones.

## Mandatory checks (during generation)

- Slide 2 declares stance (substance / polish); slides 3-14 are consistent with that stance. Mixed-stance decks are rewritten — a Berkshire-substance deck cannot also commission a Tim Davis photo essay; a Patagonia-polish deck cannot also typeset its letter in Courier.
- Two type weights maximum across the system. A third weight triggers a slide-5 callout asking the user to drop one. Display weight and body weight are named (e.g. "Tiempos Headline Medium" + "Söhne Regular"), not generic.
- Photography is named: one photographer OR one disciplined photo style. Stock-photo mixes are flagged. The slide-7 image direction is the AD's defensible decision, not a placeholder.
- Financial pages (slide 9) share the master grid (slide 6) with editorial pages. Standalone "spreadsheet" pages are rewritten.
- Risk-factor / disclosure typesetting (slide 10) is treated as a *design* problem (S-1 specific). Small print is typeset on the master grid, not dumped as boilerplate at the back.
- Every methodology claim or case-study reference (Berkshire, Patagonia, Pinterest 2019, Pentagram, Apple 10-K) carries a footnote citation. Unverifiable attributions are corrected — see the audit changelog in the spec.
- Colophon (slide 14) names every collaborator — AD, designers, photographer, printer, paper, copy editor. Like the Pentagram tradition, the team is never erased.

## Template selection

- **Editorial Polish** (default, bundled): Patagonia-class editorial-confessional shape, full-bleed photography, named photographer, drop-cap letter spread.
- **Substance Anti-Design** (alternate): Berkshire-class monospaced-feel shape, no photography, structural-only design, restraint as the brand.
- **Tech IPO S-1** (alternate): Pinterest-2019-class narrative-led prospectus shape, risk-factor section as typeset feature, illustration over photography.
- **Sustainability / Impact** (alternate): hybrid shape, infographic-grade data pages alongside editorial chapters, third-party-audit colophon entries (B Corp, ISSB, GRI).
- **Apple-Class Restraint** (alternate): 10-K shape with minimal photography, single accent, structural rigor as the brand voice — for companies whose brand is "we do not over-design."

## Use the bundled deck as a starting point

The included `deck/annual-report-art-direction-deck.slides/` is a complete reference brief for a fictional Series-D fintech S-1 with a "Patagonia confessional" stance. The agent should copy this deck and replace content while preserving the 14-slot playlist — the Stance slide (slide 02), the Opening-Spread Concept (slide 04), the Type System (slide 05), and the Colophon (slide 14) are slot-locked.

## Recommended 14-slide structure

| # | Page | Purpose | Required? |
|---:|---|---|:---:|
| 1 | Cover | Project name + filing target (10-K / S-1 / impact report) | yes |
| 2 | Stance | One sentence: substance or polish, with named reference | **yes** |
| 3 | Audience + reading occasion | Who reads what page, in what setting | yes |
| 4 | Opening-Spread Concept | Mocked cover → opener → letter spread | **yes** |
| 5 | Type system | Display + body + caption, two weights max, named | **yes** |
| 6 | Grid + chapter furniture | Folio, running head, callout, drop-cap, pull-quote | **yes** |
| 7 | Image direction | Named photographer / illustrator OR named photo discipline | **yes** |
| 8 | Color system | 1 primary + 1 accent + neutrals, named hex | yes |
| 9 | Data-page system | Charts, tables, footnote grid for financial section | **yes** |
| 10 | Risk-factor / disclosure typesetting | How the small print sits on the page (S-1 specific) | yes |
| 11 | Cover concept | Final cover render, single image, one-line title | yes |
| 12 | Production specs | Trim, paper, ink, finishing — or digital export spec | yes |
| 13 | Schedule | Editorial → photo → typesetting → press milestones | yes |
| 14 | Colophon | Named credits — AD, designers, photographer, printer, paper | **yes** |
