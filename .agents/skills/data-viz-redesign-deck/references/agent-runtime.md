# Agent runtime brief — Redo Data Viz like Nathan Yau

## Core principle

most "ugly chart" complaints are about palette and gridlines. The real problem is encoding choice — the wrong chart type forces the eye to compare on perceptual axes it's bad at. Solve encoding first; everything else is downstream.

## Context the agent must establish before generating

> Before producing the deck, the agent must know each item below.
> - If the user's prior messages already supply an item, use it; do NOT re-ask.
> - If an item can be reasonably inferred from the user's stated topic, infer it and state the assumption inline on slide 2.
> - Ask only what is missing AND cannot be inferred — one targeted question at a time, not a script.

1. **The deck and its 5 worst charts** — by impact, not by ugliness. The agent prioritises the chart the CMO can't read, not the one with the rainbow palette.
2. **Per chart: the question it answers** — in plain English ("Which 2 categories drove >50% of Q4 revenue?"). If the user can't name a question, the chart is on the slide-11 "delete" list.
3. **Current encoding per chart** — donut / 3D bar / stacked column / dual-axis / pie / etc. The agent places each on the Cleveland-McGill ladder on slide 2.
4. **Audience reading time per chart** — a 5-second glance (executive review) needs a different encoding than a 60-second study (analyst working session).
5. **Cross-deck rules currently in place (if any)** — same-scale small multiples, color semantics (actuals vs plan vs forecast), unit suffix. The agent enforces IBCS on slide 9.
6. *(optional)* **The BI tool** — Tableau / Power BI / Looker / Plotly — affects what palette + encoding swaps are actually buildable.

## Mandatory checks (during generation)

- Every kept chart has a Chart Redesign Card naming the *question it answers* in plain English. Charts without a question are listed on slide 11 for deletion.
- No 3D charts, no donuts where a bar works, no rainbow palettes, no dual y-axis without an explicit cited reason. The agent does not let "but the brand guide says rainbow" through without a Cleveland-McGill counter-argument.
- Small multiples share scale and color semantics (IBCS conformance). The Q3 chart and the Q4 chart use the same y-range; the actuals-color on chart 4 is the same actuals-color on chart 9.
- Sequential / diverging / categorical palettes are picked once on slide 10 and reused across the entire deck. Per-chart palette choices are flagged.
- Pie charts allowed only if ≤2 slices and the comparison is "majority vs not." Three-or-more-slice pies are converted to ranked horizontal bars.
- Tables are first-class — if the answer is a number, the answer is a number, not a chart. A "Total customers: 1.2M" donut is replaced by a number in the slide title.
- Every methodology principle (Cleveland-McGill, Tufte, Knaflic, IBCS) carries a footnote citation. The Chart Redesign Card cites the perceptual-rank ladder by reference, not by hand-wave.

## Template selection

- **Monthly Business Review** (default, bundled): CMO / CFO monthly deck shape, ~15 charts, KPI-led, 5-second glance audience.
- **Board / Investor** (alternate): tighter visual restraint, ~8 charts, single-page summary, no clutter.
- **BI Style Guide** (alternate): no specific deck — outputs the rules + a chart-library catalogue for analytics-platform owners.
- **Consulting Working Session** (alternate): ~25 charts, more depth per card, 60-second-study audience, footnote-density permitted.
- **Conference Talk Data Deck** (alternate): ~10 charts, one-chart-per-slide, speaker-led pacing, story-first ordering rather than KPI-grid ordering.

## Use the bundled deck as a starting point

The included `deck/data-viz-redesign-deck.slides/` is a complete reference cleanup built around a fictional retail-company monthly CMO review whose input deck had 22 charts. The agent should copy this deck and replace content while preserving the 12-slot playlist — the Encoding Ladder (slide 02), the 5 Chart Redesign Card slots (slides 04-08), and the Style-Guide One-Pager (slide 12) are slot-locked.

## Recommended 12-slide structure

| # | Page | Purpose | Required? |
|---:|---|---|:---:|
| 1 | Cover | "Redesigning the charts in [deck name]" + before/after thumbnail | yes |
| 2 | Encoding Ladder | Cleveland-McGill ranking applied to this deck's charts | **yes** |
| 3 | Top 5 worst charts | Thumbnails ranked by impact, not by ugliness | **yes** |
| 4 | Chart Redesign Card 1 | Full before/after with the 5-field card | **yes** |
| 5 | Chart Redesign Card 2 | Same shape | **yes** |
| 6 | Chart Redesign Card 3 | Same shape | **yes** |
| 7 | Chart Redesign Card 4 | Same shape | yes |
| 8 | Chart Redesign Card 5 | Same shape | yes |
| 9 | Cross-deck rules | Same scale, same color semantics, same unit suffix (IBCS) | **yes** |
| 10 | Palette + type cleanup | One sequential + one categorical + one diverging palette | yes |
| 11 | The 3 charts to delete | Charts that should not exist; data lives in table or in text | **yes** |
| 12 | Style-guide one-pager | Reusable rules for next quarter's deck | **yes** |
