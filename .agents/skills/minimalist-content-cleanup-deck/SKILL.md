---
name: minimalist-content-cleanup-deck
display_name: Clean a Content Heap like a Top Design-System Maintainer
description: |
  Clean an internal deck the way a top design-system maintainer actually cleans one — atomic structure, CRAP discipline, no decoration. A variable-length, 1920×1080 cleanup pass that takes a 40-80-slide content heap (RFCs, architecture reviews, ops decks pasted from docs and Slack) and returns an 18-35-slide readable deck, cutting 30-55% of slides through delete / merge / rewrite decisions. Three irreducible disciplines — every kept slide is named at one atomic level (atom / molecule / organism), every kept slide passes the four-question CRAP audit (Contrast / Repetition / Alignment / Proximity), and body text is held to 60-80 chars per line on a multiple-of-base-unit spacing grid. Use for quarterly architecture reviews, RFC decks, ops decks, and any internal deck where a VP said "I couldn't get past slide 9."
metadata:
  short-description: Same content, half the slides, twice the dwell time — atomic cuts, CRAP discipline, no decoration.
lang: en-US
category: design-craft
tags:
  - content-cleanup
  - design-system
  - notion
  - atomic-design
  - crap-principles
  - minimalism
  - design-system
  - internal-deck
previews:
  - previews/01-cover.png
  - previews/02-thesis.png
  - previews/03-persona.png
  - previews/04-methodology.png
  - previews/05-atom-inventory.png
  - previews/06-cut-list.png
  - previews/07-merge-list.png
  - previews/08-rewrite-list.png
  - previews/09-atomic-diagram.png
  - previews/10-card-08-architecture.png
  - previews/11-card-11-migration.png
  - previews/12-card-15-cost.png
  - previews/13-card-19-risks.png
  - previews/14-card-23-rollout.png
  - previews/15-card-27-metrics.png
  - previews/16-before-after-sample.png
  - previews/17-new-toc.png
  - previews/18-style-rules.png
  - previews/19-handoff-onepager.png
  - previews/20-sources.png
thumbnails:
  - thumbnails/01-cover.png
  - thumbnails/02-thesis.png
  - thumbnails/03-persona.png
  - thumbnails/04-methodology.png
  - thumbnails/05-atom-inventory.png
  - thumbnails/06-cut-list.png
  - thumbnails/07-merge-list.png
  - thumbnails/08-rewrite-list.png
  - thumbnails/09-atomic-diagram.png
  - thumbnails/10-card-08-architecture.png
  - thumbnails/11-card-11-migration.png
  - thumbnails/12-card-15-cost.png
  - thumbnails/13-card-19-risks.png
  - thumbnails/14-card-23-rollout.png
  - thumbnails/15-card-27-metrics.png
  - thumbnails/16-before-after-sample.png
  - thumbnails/17-new-toc.png
  - thumbnails/18-style-rules.png
  - thumbnails/19-handoff-onepager.png
  - thumbnails/20-sources.png
---

# Clean a Content Heap like a Top Design-System Maintainer

> Same content, half the slides, twice the dwell time — atomic cuts, CRAP discipline, no decoration.

![minimalist-content-cleanup-deck methodology illustration](https://cdn1.genspark.ai/user-upload-image/slide_agent/v2-catalog-hero/150-notion-atlassian-content-deck.png)

## Why this skill works

- **The VP gets past slide 9.** A delete-and-merge pass cuts 30-55% of input slides before any rewrite — the deck shortens before it tightens.
- **Next quarter's deck inherits the rules.** The final slide is a printable atomic + CRAP one-pager the team uses as a style guide, so the cleanup compounds across reviews.
- **You bring the deck.** Hand the agent the input deck (or its outline); it returns a cut list, a merge list, a rewrite list, and a CRAP-Atomic Slide Card per kept slide.

## Methodology cheat-sheet

**Atomic × CRAP × Top Design-System Restraint** — five frameworks compressed into one cleanup discipline: hierarchy (Atomic Design), audit (CRAP), typography (Atlassian-style 60-80 char measure), restraint (cool minimalism), procedure (delete-merge-rewrite, in that order).

1. **Atomic Design hierarchy**[^5] — Brad Frost's five-level model: atoms (text, icon, button) → molecules (search input, callout) → organisms (header, slide) → templates → pages. Every kept slide is named at one level; slides that don't fit are merged or cut.
2. **CRAP principles**[^4] — Robin Williams' *Non-Designer's Design Book* canon: Contrast, Repetition, Alignment, Proximity. Every slide passes the four-question audit; failing slides are rewritten or merged.
3. **Atlassian Design System line-length + spacing**[^1][^2][^3] — body text 60-80 chars per line (10-12 words), spacing on a 4px multiple-of-base-unit grid, paragraph spacing managed in Figma libraries. Atlassian's public design-system docs are the source.
4. **Productivity-doc warm minimalism — cooled** — single display weight, single body weight, generous surface space. This skill *cools* the warm-beige docs aesthetic to neutral white (`#FFFFFF` + ink `#111111` + slate `#3F4A57`) — the warm-beige published surfaces lean warm; this deck deliberately doesn't.
5. **The "delete or merge" rule** — slides that are pasted screenshots without commentary are either merged into the next slide as a callout, or cut. Multi-sentence job descriptions are two slides.
6. **One slide, one job** — the slide's job sentence fits on one line; if it needs two sentences, it's two slides.

## Before / After

### Slide 11 of 47 (in a typical RFC deck)

**Typical PPT template**

> **Architecture**
>
> *(Slack screenshot of a 14-message thread, unreadable at deck zoom)*
>
> - Discussed in #eng-arch on Tuesday
> - We want to migrate
> - Pending review
> - See doc

**This skill's rewrite**

> *(cut. Merged into slide 8 as a single callout.)*
>
> **Slide 8 (merged):**
> *Migration timeline approved 2026-04-12; details in [doc link].
> See appendix slide A3 for the original #eng-arch thread.*
>
> Slide count: 47 → 28. The architecture decision is now on one page,
> not two.

### The style-guide handoff slide

**Typical PPT template**

> **Thanks!**
>
> *(no equivalent — the typical deck has no handoff)*

**This skill's rewrite**

> **Atomic + CRAP — Style Rules for Q3**
>
> *Body text*: 60-80 chars per line (Inter Regular, 16pt).[^1]
> *Headings*: Semibold, two weights total.
> *Atomic chips*: atom / molecule / organism — coloured slate `#3F4A57`.
> *CRAP audit*: every slide passes Contrast / Repetition / Alignment /
> Proximity before review.[^4]
> *Cut-ratio target*: ≥30% of input slides cut or merged.

### The cut-list slide

**Typical PPT template**

> *(no equivalent — the typical deck has no cut pass)*

**This skill's rewrite**

> **Cut list — 19 slides recommended for deletion**
>
> | Input # | Title | Reason |
> |---|---|---|
> | 03 | "Agenda" | Re-stated by slide 02. Cut. |
> | 07 | "Background context" | No new info beyond slide 06. Cut. |
> | 11 | "Slack thread screenshot" | No commentary — merge as callout on 08. |
> | 17-19 | "Sub-team updates (3 identical templates)" | Merge to one summary slide. |
> | 22 | "Risks (pasted from Confluence)" | Rewrite as 3 lines on slide 21. |
> | … | *(13 more entries)* | |
>
> *Output: 47 → 28 slides (40% cut). Below 30% triggers a re-review.*

## What this skill produces

A variable-length, 1920×1080 cleanup-pass deck. Output length mirrors the input's outline minus 30-55% of slides — typical input 40-80 slides, typical output 18-35 slides. The visual mode is cool minimalism: pure white background, ink body, a single cool-slate accent (deliberately *cool*, to keep the deck out of the warm-beige docs aesthetic lineage), two type weights only (body Regular + heading Semibold), one sans-serif (Inter / IBM Plex Sans), top-design-system-style 4px-base spacing, 60-80 char measure. No icons except atomic-level chips. No drop shadows, no gradients, no decorative dividers, no full-bleed photos.

## Sources

[^1]: Atlassian Design System. *Typography — applying typography (60-80 char line length).* https://atlassian.design/foundations/typography/applying-typography

[^2]: Atlassian Design System. *Spacing — multiple-of-base-unit grid.* https://atlassian.design/foundations/spacing

[^3]: Atlassian Design System. *Typography (beta) — paragraph spacing in Figma libraries.* https://atlassian.design/foundations/typography-beta

[^4]: Williams R. *The Non-Designer's Design Book.* 4th ed., Peachpit Press, 2014. ISBN 978-0133966152. https://www.peachpit.com/store/non-designers-design-book-9780133966152 — the canonical source of the C.R.A.P. (Contrast, Repetition, Alignment, Proximity) framework.

[^5]: Frost B. *Atomic Design* (book home + chapter 2 methodology). https://atomicdesign.bradfrost.com/ ; https://atomicdesign.bradfrost.com/chapter-2/
