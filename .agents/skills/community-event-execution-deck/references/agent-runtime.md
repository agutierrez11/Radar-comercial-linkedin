# Agent runtime brief — Run a Community Event like a PTA chair

## Core principle

a community-event deck is judged by whether volunteers show up and whether the board approves it Thursday. Aesthetic decks lose to ugly checklists. Default to checklist-density and named-person specificity over visual flourish.

## Context the agent must establish before generating

> Before producing the deck, the agent must know each item below.
> - If the user's prior messages already supply an item, use it; do NOT re-ask.
> - If an item can be reasonably inferred from the user's stated topic, infer it and state the assumption inline on slide 2.
> - Ask only what is missing AND cannot be inferred — one targeted question at a time, not a script.

1. **Event name + date** — drives the cover and the 6-week timeline on slide 4.
2. **IAP2 participation level** — Inform / Consult / Involve / Collaborate / Empower. The agent puts this on slide 2 as a chip and matches the success metric on slide 3 accordingly (e.g., Inform → attendance count; Empower → decision adopted).
3. **Goal in one sentence + named beneficiary group** — "Raise $8K for the 4th-grade science enrichment program" beats "support the school".
4. **Volunteer roster** — names, shifts, phone numbers, arrival times. If the user has TBDs, the agent flags how many.
5. **Permits, insurance, cleanup plan** — named permits + filing dates + COI line. The agent will not let these slip to appendix.
6. *(optional)* **Budget detail** — income, expense, weekly cash-flow.
7. *(optional)* **Board context** — quorum, who needs to second the motion, prior precedent.

## Mandatory checks (during generation)

- Slide 2 names the IAP2 level; the success metric on slide 3 matches that level. Inform → attendance count; Consult → number of stakeholder comments received; Involve → number of co-designed elements; Collaborate → number of partner-organisations engaged; Empower → number of community-adopted decisions.
- Volunteer Roster Grid lists named individuals per shift with phone contacts. "TBD" rows are highlighted red and counted in a header line ("3 shifts unfilled — see week-3 recruitment plan on slide 4").
- Permits, COI / liability insurance, and cleanup plan are body slides (7, 11), never appendix. The treasurer reads these first; missing them costs the board vote.
- Communication plan covers save-the-date 4 weeks out, reminder 1 week, day-of details day-before — National PTA cadence. Each communication names a specific channel (school email, classroom flyer, group chat, parish bulletin, neighbourhood Nextdoor) — not just "communications".
- Day-of run-of-show is in 15-minute increments with named owner per slot. Generic "volunteers handle setup" rows are rewritten with names.
- Final slide is a formal Robert's Rules-style motion the board can vote on, drafted in the exact words the chair will read aloud.
- Every external framework reference (PTA, IAP2, NACo, ICMA, Robert's Rules) carries a footnote citation.
- All deck pages print legibly black-and-white on US Letter (no white-on-pale-yellow text, no full-bleed dark backgrounds with white text under 14pt, no thin hairline borders that disappear on a budget photocopier).

## Template selection

- **PTA Fall Festival** (default, bundled): elementary-school PTA shape, fundraising-focused, parent-volunteer roster.
- **Municipal Town Hall** (alternate): higher IAP2 level (Consult / Involve), city-council motion shape, accessibility / language-access focus.
- **Library / Parks Department** (alternate): program-series shape, multi-week run, single coordinator + volunteer rotation.
- **Faith-Community Event** (alternate): parish / congregation shape, lay-leader volunteer roster, pastor / rabbi / imam approval slide instead of board motion.
- **Neighbourhood Non-Profit Fundraiser** (alternate): 501(c)(3) compliance lines, named-donor recognition slide, post-event tax-receipt cadence.

## Use the bundled deck as a starting point

The included `deck/community-event-execution-deck.slides/` is a complete reference deck for a PTA Fall Festival, designed to satisfy a school-board approval vote on Thursday and a 30-volunteer crew on Saturday. The agent should copy this deck and replace content while preserving the 12-slot playlist — the IAP2 chip (slide 02), the Volunteer Roster Grid (slide 05), and the Robert's Rules motion (slide 12) are slot-locked.

## Recommended 12-slide structure

| # | Page | Purpose | Required? |
|---:|---|---|:---:|
| 1 | Cover | Event name + date + IAP2 level chip | yes |
| 2 | What kind of event | IAP2 Spectrum placement + success metric | **yes** |
| 3 | Goal in one sentence | + named beneficiary group | **yes** |
| 4 | Timeline | T-6 wk → T+1 wk Gantt | yes |
| 5 | Volunteer Roster Grid | Role × shift × name × contact × arrival time | **yes** |
| 6 | Site plan | Layout, traffic flow, ADA access | yes |
| 7 | Permits / insurance / liability | Named permits + filing dates + COI line | **yes** |
| 8 | Communication plan | Save-the-date / reminder / day-of, channel each | yes |
| 9 | Budget | Income, expense, cash-flow week-by-week | yes |
| 10 | Day-of run-of-show | 15-min increments, named owner each slot | **yes** |
| 11 | Cleanup + debrief plan | Trash, lost-and-found, debrief survey | **yes** |
| 12 | Motion for the board | Drafted as Robert's Rules motion | **yes** |
