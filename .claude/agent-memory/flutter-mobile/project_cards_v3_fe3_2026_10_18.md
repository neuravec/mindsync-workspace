---
name: project-cards-v3-fe3-2026-10-18
description: Cards v3 FE3 (Weekly/Monthly period_card extras, Realization, Timeline) pushed 2938293 on origin/feat/cards-v3; open timeline_filter_changed overlap; plugin-registrant and caret-scroll test gotchas
metadata:
  type: project
---

Cards v3 FE3 done 2026-10-18, commit 2938293 on origin/feat/cards-v3 (worktree mindsync-frontend-wt-cards-v3, after FE1 2610d6c and FE2 39a8d7f). Weekly/Monthly read `GET /analytics/period_card` through PeriodCardManager -> PeriodCardCubit, created only for COMPLETED, non premium-locked cards (mixin `PeriodCardHost` in `period_card_extras.dart`); any failure = card without chart/stats.

**Why:** team cards plan (SPEC in the session scratchpad teams/cards/), boards AWeekly/AMonthly/ARealization/ATimeline, decisions D3 (Edit only where an update endpoint exists: Weekly LEGACY only), D10 (no Monthly bookmarks), D12, D14, D19.

**How to apply:**
- Open: Timeline sends both `timeline_filter_changed` (old, cubit) and `timeline_filter_selected` (new, SPEC 5) for the same tap; operator/lead must pick one. Do not silently remove either.
- Deploy order: backend period_card before the app, otherwise charts/stats stay hidden (no crash).
- `flutter test`/`flutter analyze` (pub get) rewrites linux/macos/windows generated plugin registrants (line-ending noise): `git checkout --` them before staging.
- In widget tests a focused TextField scrolls its caret back into view after ensureVisible, so a header Save tap misses (offset off-screen): unfocus first.
- Subagent harness refuses writing REPORT.md files; report content goes into the final output.

Related: [[project-cards-redesign-2026-10-13]]
