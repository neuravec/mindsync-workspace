---
name: project-timeline-a3-v2-2026-10-19
description: Timeline A3 v2 (wrapped filter pills, 800 labels in deep ocean, pastel pink Monthly tile) pushed cae29d8 to origin/dev; negative Wrap runSpacing for 44 px targets, Center(widthFactor 1) in Wrap, Monthly tone split open
metadata:
  type: project
---

Timeline A3 v2 shipped 2026-10-19 as cae29d8 (fast-forward on origin/dev from 40e3469, branch feat/timeline-a3-v2, worktree mindsync-frontend-wt-timeline-a3). Darek approved the board with "IMPLEMENTUJ" after two tweaks: row labels in the default colour for every type, Monthly tile pastel pink #F3D6EA / #6E2A55. Supersedes the scrolling chip row of [[timeline-filter-chips-2026-10-19]].

**Why:** operator wanted all filters visible at once in at most 1/5 of the screen (measured on 390 x 844).

**How to apply:**
- Measured block: 126 px (3 rows) in EN/NB/SV, 164 px (4 rows) in DE/ES/FR/PL at 390 x 844. At 360 x 800 most locales are 164 px = 20.5%, slightly over a fifth: if Darek complains on a small Android, that is why.
- 44 px touch targets with no visual change: each Wrap child is the pill plus 3 px sides and 6 px top/bottom, block padding shrinks by the same, `Wrap(runSpacing: -6)`. RenderWrap has no assert on negative spacing; in the overlap the LATER child (row below) wins the hit test. Exclusive area per interior row is 38, not 44 (geometry: 32 + 6 pitch).
- `Container(alignment: ...)` inside a Wrap stretches to the Wrap's full width (Align takes bounded max width). Use `Center(widthFactor: 1, heightFactor: 1)` to centre in minHeight without stretching.
- Monthly colour is Timeline-only: `MsCardTone.timelineOf(kind)` / `MsCardTone.timelineMonthly`; `MsCardTone.of(monthly)` (card header) stays dark per board AMonthly. Open question for the lead: should the Monthly card header follow the pink. `labelOnWhite` was removed (Timeline was its only user).
- Event test recipe: real `TherapyTabCubit(timelineManager: mock, ...)` registered in sl, `unawaited(cubit.loadTimeline())` before pump, then tap a pill: asserts timeline_viewed, timeline_filter_selected and timeline_filter_changed together.
- Parity render: `a3v2_timeline_monthly` in test/card_parity_shots/fe3_cards_parity_shot_test.dart (marketing tag, `CARDS_PARITY_SHOTS_DIR=... --tags marketing --run-skipped --plain-name ATimeline`).
