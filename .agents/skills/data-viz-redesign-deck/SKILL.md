---
name: data-viz-redesign-deck
display_name: Redo Data Viz like a Top Data-Visualization Designer
description: |
  Redo the data viz in a deck the way a top data-visualization designer actually redoes it — pick the encoding first, declutter second, color last. A 12-slide, 1920×1080 chart-redesign deck for analysts, consultants, and BI leads whose monthly review decks ship 6-15 charts each. Three irreducible disciplines — every chart names the question it answers (charts without a question are deleted), every chart is placed on the Cleveland-McGill perceptual ladder before any palette decision, and small multiples share scale and color semantics (IBCS conformance). No 3D charts, no donuts where a bar works, no rainbow palettes, no dual y-axis without explicit cited reason. Use for monthly business reviews, board / CFO decks, BI portal templates, and any deck where readers say "I couldn't read the chart."
metadata:
  short-description: The chart is the wrong type, not the wrong color — encoding first, color last.
lang: en-US
category: design-craft
tags:
  - data-visualization
  - chart-redesign
  - data-viz-design
  - cleveland-mcgill
  - ibcs
  - tufte
  - storytelling-with-data
  - bi-analytics
previews:
  - previews/01-01-cover.png
  - previews/02-02-encoding-ladder.png
  - previews/03-03-top-5-worst.png
  - previews/04-04-card-1-donut.png
  - previews/05-05-card-2-stacked-bar.png
  - previews/06-06-card-3-dual-axis.png
  - previews/07-07-card-4-rainbow-line.png
  - previews/08-08-card-5-3d-column.png
  - previews/09-09-cross-deck-rules.png
  - previews/10-10-palette-type.png
  - previews/11-11-charts-to-delete.png
  - previews/12-12-style-guide.png
thumbnails:
  - thumbnails/01-01-cover.png
  - thumbnails/02-02-encoding-ladder.png
  - thumbnails/03-03-top-5-worst.png
  - thumbnails/04-04-card-1-donut.png
  - thumbnails/05-05-card-2-stacked-bar.png
  - thumbnails/06-06-card-3-dual-axis.png
  - thumbnails/07-07-card-4-rainbow-line.png
  - thumbnails/08-08-card-5-3d-column.png
  - thumbnails/09-09-cross-deck-rules.png
  - thumbnails/10-10-palette-type.png
  - thumbnails/11-11-charts-to-delete.png
  - thumbnails/12-12-style-guide.png
---

# Redo Data Viz like a Top Data-Visualization Designer

> The chart is the wrong type, not the wrong color — encoding first, color last.

![data-viz-redesign-deck methodology illustration](https://cdn1.genspark.ai/user-upload-image/slide_agent/v2-catalog-hero/149-flowingdata-data-viz-rework.png)

## Why this skill works

- **The CMO finally reads chart 14.** Every chart is placed on the Cleveland-McGill perceptual ladder before any palette decision — 3D donuts get re-encoded to ranked bars, not just re-coloured.
- **Next quarter's deck inherits the rules.** The final slide is a printable style-guide one-pager (same scale, same color semantics, same unit suffix) so the cleanup compounds month over month.
- **You bring the deck.** Hand the agent the input deck (or a list of the chart questions); it returns a redesigned chart-by-chart cleanup with one Chart Redesign Card per fix.

## Methodology cheat-sheet

**Encoding × Declutter × IBCS** — the data-visualization-design / Storytelling-with-Data discipline applied to a real deck: encoding first, declutter second, color last, then enforced across the deck with IBCS.

1. **Cleveland-McGill perceptual ranking**[^1][^2][^3] — position on a common scale > position on non-aligned scales > length > angle > area > volume > color saturation. Pick the highest-ranked encoding the data supports. Cleveland & McGill's 1984 JASA study and the 1985 *Science* extension are the canon.
2. **Tufte's data-ink ratio**[^4] — maximise data-ink, erase non-data-ink: gridlines, chart borders, legends-as-noise. *The Visual Display of Quantitative Information* is the source.
3. **Yau's "make it readable" loop**[^5][^6] — show the rough chart, ask "what's the one thing?", strip everything that doesn't carry that thing. Nathan Yau's *Visualize This* (2nd ed., Wiley 2024) and his published data-visualization writing archive.
4. **Knaflic's declutter sequence**[^7][^8] — remove chart border, remove gridlines, remove data markers, lighten axis labels, soften axis lines, leverage color sparingly. *Storytelling with Data* and the 5-step decluttering post.
5. **IBCS notation**[^9][^10] — International Business Communication Standards: same scale across small multiples, same unit suffix, same color semantics for actual / plan / forecast. Rolf Hichert's IBCS Association argues it's shaping ISO 24896.
6. **One chart, one question** — multi-axis charts are split into two charts. Knaflic-canonical rule.

## Before / After

### A chart on slide 6

**Typical PPT template**

> *(3D donut chart, 7 product categories, rainbow palette, no labels,
> legend on the right, gradient slice borders)*
>
> **Q4 Revenue by Category**

**This skill's rewrite**

> *(Chart Redesign Card 2)*
>
> *Question*: Which 2 categories drove >50% of Q4 revenue?
> *Current encoding*: 3D donut (area, perceptual rank 5/6).[^1]
> *Recommended encoding*: ranked horizontal bar (position on common
> scale, rank 1/6).
> *Declutter*: remove border, axis label only on top bar, top-2 bars
> in analytic blue `#0066CC`, rest in muted gray `#9CA3AF`.[^7]
> *IBCS*: actuals, no plan comparison, unit suffix "$M" on title.[^9]

### The "delete this chart" slide

**Typical PPT template**

> *(no equivalent — the typical deck has no delete pass)*

**This skill's rewrite**

> **The 3 charts to delete**
>
> 1. Slide 9 — "Total customers: 1.2M". *Answer is a number. Put it
>    in the title, drop the chart.*
> 2. Slide 14 — "NPS by region (5 dual-axis pie charts)". *No
>    question; delete or replace with a sortable table.*
> 3. Slide 19 — "Marketing channels (3D stacked column)". *Three
>    competing encodings on one chart. Split into 2 small multiples.*

### The cross-deck rules slide

**Typical PPT template**

> **Chart Standards**
> - Use brand colors
> - Make it look nice
> - Be consistent
> - Add data labels
> - Make it professional

**This skill's rewrite**

> **Cross-deck rules (IBCS-conformant)**[^9]
>
> *Same scale*: every small-multiple set shares y-axis range.
> *Same color semantics*: actuals = ink `#1A1A1A`; plan = muted gray
> `#9CA3AF`; forecast = striped fill of plan color.
> *Same unit suffix*: $M or % declared in chart title, never on bars.
> *Same time axis*: months left-to-right, no quarter-month mixing.
> *Pie rule*: ≤2 slices and "majority vs not" — else use a bar.

## What this skill produces

A 12-slide, 1920×1080 chart-redesign deck for monthly reviews, board decks, and BI templates. The deck is *the cleanup*, not the review itself — it's what you hand to a CMO or a BI team to argue that the input deck's 22 charts should become 14 charts (and 3 should be deleted entirely because the answer is a number, not a picture). The visual mode is analytic-ink: chart canvas paper-white, ink data, one analytic-blue highlight series, muted-gray context, monochrome-blue sequential palette, blue–gray–orange diverging palette. Tabular numerals only. One sans-serif (Inter / IBM Plex Sans).

## Sources

[^1]: Cleveland WS, McGill R. *Graphical Perception: Theory, Experimentation, and Application to the Development of Graphical Methods.* JASA, vol. 79, 1984. http://euclid.psych.yorku.ca/www/psy6135/papers/ClevelandMcGill1984.pdf

[^2]: Cleveland WS, McGill R. *Graphical Perception (1984)* — Taylor & Francis Online JASA mirror. https://www.tandfonline.com/doi/abs/10.1080/01621459.1984.10478080

[^3]: Cleveland WS, McGill R. *Graphical Perception and Graphical Methods for Analyzing Scientific Data.* Science, 1985. https://web.cs.dal.ca/~sbrooks/csci4166-6406/seminars/readings/Cleveland_GraphicalPerception_Science85.pdf

[^4]: Tufte E. *The Visual Display of Quantitative Information* (data-ink ratio). Graphics Press. https://www.edwardtufte.com/book/the-visual-display-of-quantitative-information/

[^5]: Yau N. *Visualize This: The FlowingData Guide to Design, Visualization, and Statistics* (2nd ed., Wiley 2024). https://www.wiley.com/en-us/Visualize+This%3A+The+FlowingData+Guide+to+Design%2C+Visualization%2C+and+Statistics%2C+2nd+Edition-p-9781394214860

[^6]: FlowingData — Nathan Yau's archive. https://flowingdata.com/

[^7]: Knaflic CN. *Storytelling with Data: A Data Visualization Guide for Business Professionals.* Wiley, 2015. https://s3.amazonaws.com/files.commons.gc.cuny.edu/wp-content/blogs.dir/20521/files/2022/09/Knaflic-storytelling-data.pdf

[^8]: Knaflic CN. *Declutter your data visualizations (5 steps).* Storytelling with Data blog, 2016-03-01. https://www.storytellingwithdata.com/blog/2016/3/1/declutter-your-data-visualizations

[^9]: IBCS — International Business Communication Standards. https://www.ibcs.com/

[^10]: *International Business Communication Standards (Hichert / IBCS Association).* Wikipedia. https://en.wikipedia.org/wiki/International_Business_Communication_Standards
