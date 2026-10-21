---
name: project-main-mc-v3-fe4-2026-10-18
description: Main MC v3 FE-4 (ee8d9f1 pushed feat/main-v3) - Habits sheet on last7, write answers carry one preference week (merge), DST bug in date walks, McSheetFrame.bodyBleedStart for real 48 px hit areas, test traps
metadata:
  type: project
---

FE-4 of Main MC v3 committed as ee8d9f1 on `feat/main-v3` (worktree mindsync-frontend-wt-main-v3) and pushed. Builds on [[project-main-mc-v3-fe3-2026-10-18]].

- `HabitsCubit` loads `window=last7`, falls back to `week` once on a 422 (`_fetchWeekly`, remembered for the cubit's life). `toggleDay` works outside Edit; days before `habitLocalStartDate` (unless ticked) and before `window.start` are inert.
- Backend `PUT /habits/{id}/checks/{date}`, PATCH and reorder answer with the preference WEEK of the written date (today for PATCH/reorder), never the rolling window: `mergeHabitIntoWindow` keeps the other week's days. Replacing the habit wholesale silently drops ticks.
- `habitWindowDates`/`habitMonthGridRows` walked local midnights + 24 h: wrong dates around DST (25 Oct 2026 listed twice, last day dropped; October/March month grids too). Now UTC midnights; verified the old walk fails on this machine (Europe/Warsaw).
- Sheet kit: `mc/sheets/habits/` (sheet, week grid, month, editor) + `widgets/mc_dashed.dart`. Editor shows in place of the list via the cubit's `editorRequest`; closing the sheet clears it and leaves Edit.

**Why:** later Main tasks (FE-5 focus, FE-6 first week) and integration reuse these seams; the traps cost test rounds.
**How to apply:**
- Hit tests stop at every ancestor's size: an OverflowBox/negative-margin "48 px" area is fake (getSize says 48, taps miss). Use `showMcSheet(bodyBleedStart:)` so the body owns the padding, and prove it with a tap at the edge plus a mutation run.
- `McHarness` stubs `habits.logMainSheetViewed` (returns bool); any new non-void cubit method the sheets call on a MockCubit needs a stub there.
- `OverflowBox` inside a Row in a scroll view asserts (infinite height); use `Text(softWrap: false, overflow: visible)`.
- Python `Path.write_text` on Windows writes CRLF; write bytes or pass `newline='\n'` for LF files.
- `test/core/account_scope_reset_regression_test.dart` pins the count of `registerAccountScoped` calls: bump it with every new account-scoped cubit.
