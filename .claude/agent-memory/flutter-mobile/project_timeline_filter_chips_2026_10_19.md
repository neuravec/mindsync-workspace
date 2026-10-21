---
name: timeline-filter-chips-2026-10-19
description: SUPERSEDED by A3 v2 (cae29d8). Timeline filter chips made one compact horizontal row, abb644b pushed to origin/dev; ensureVisible-walks-PageView trap, loading state has no filter, horizontal-row test recipe
metadata:
  type: project
---

Fix abb644b on origin/dev (2026-10-19, fast-forward from d59d6b4, branch fix/timeline-filter-chips, worktree mindsync-frontend-wt-timeline-chips). Operator screenshot: the 10 Timeline chips wrapped over 4-5 rows (256 dp area at 360 wide). Now `_FilterChips` (private, therapy_tab_screen.dart, only user) is a SingleChildScrollView row: 32 dp pills in 48 dp targets, bar 56 dp (`ValueKey('timelineFilterBar')`, scroll `timelineFilterScroll`), first entry 200 dp higher.

**Why:** operator asked for the top chips to stop taking half the screen; visual-only change, filtering/order/l10n/events untouched.

**How to apply:**
- Never use `Scrollable.ensureVisible` / `tester`-style reveal for a chip row inside a main tab: it walks ALL ancestor scrollables, including the tab PageView, and would shift the page. Use the row's own controller + `RenderAbstractViewport.maybeOf(chip).getOffsetToReveal(...)` (needs `import 'package:flutter/rendering.dart' show RenderAbstractViewport;`, material does not export it).
- `TherapyTabCubit.loadTimeline` emits Loading (no filter) before the filtered state, so the chips highlight All during every filter load (pre-existing). The row gets `revealActive: false` then so it does not scroll back to All.
- Tests on a horizontal chip row: `ensureVisible` + `pumpAndSettle` before tapping off-screen chips; a post-frame `animateTo` needs several pumps (one long pump only ticks t=0); Loading shows a spinner, so no pumpAndSettle there.
- Same wrapped-chip pattern still lives in KE map (`ke_map_chips`) and Star of skills (`star_chip_*`), not top-of-screen, left unchanged. Orca memory filter row is already a horizontal scroll (40 dp pills).
- Both `timeline_filter_selected` (screen) and `timeline_filter_changed` (cubit) still fire per tap; the overlap is still open, see [[project-cards-v3-fe3-2026-10-18]].
