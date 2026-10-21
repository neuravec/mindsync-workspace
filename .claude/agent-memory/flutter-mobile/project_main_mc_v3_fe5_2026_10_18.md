---
name: project-main-mc-v3-fe5-2026-10-18
description: Main MC v3 FE-5 (5510394 pushed feat/main-v3) - Focus Areas sheet + Mood trend rename; whenListen state needs a stream listener, Listener/SizedBox handles only hit the icon, Container alignment goes full width, harness changes for FE-6
metadata:
  type: project
---

FE-5 of Main MC v3 committed as 5510394 + fafe1c5 (rate_failed, add_failed, delete_cancelled events) on `feat/main-v3` (worktree mindsync-frontend-wt-main-v3) and pushed. Builds on [[project-main-mc-v3-fe4-2026-10-18]].

- Sheet kit `mc/sheets/focus/` (sheet, row with 1..10 scale, edit, rules, McFocusSheetCubit per opening). `McMainScreen.openSheet` creates the cubit for focus, passes `McFocusSheet.trailing(ui)` (7 days + pencil) and closes it after. Writes go to SymptomTrackingCubit; `showSymptomDeleteConfirm` (stats sheet) is the shared two-tier confirm.
- "during setup" = one rating in total within 24 h of `userInfo.createdAt`; the tile uses the same rule (MCStates "3 tracked"). `SymptomCardModel.scoresCount` added.
- Harness: McSample has `accountCreatedAt` + `moodTrend`; `McSample.states()` areas are Sleep/Anxiety/Energy with setup ratings (account created 12 Oct 08:30); McHarness registers a MockMoodTrendCubit (`h.moodTrend`) and stubs every symptom write; McSheetHarness has `failures` and `focusConfirm`; `mcFocusHomeSample()` = board MCHome-mood data.
- Rename: values of 11 keys changed per language; `mc_focus_rename_test` scans every arb value for the old names.

**Why:** FE-6 (first week, step 5 opens Focus Areas) and integration reuse these seams; the traps below cost test rounds.
**How to apply:**
- bloc_test `whenListen` updates `cubit.state` only through a listener on `stream`; in a pure cubit test stub `when(() => mock.state)` inside the answer.
- `ReorderableDragStartListener`/`Listener` + `SizedBox(Center(icon))` only hits on the icon: wrap in `ColoredBox(Color(0x00000000))` (fixed in the FE-4 habits handle too, edge-drag tests prove it).
- `Container(alignment: ...)` inside Center/Align takes the full width; use `Center(widthFactor: 1)` inside instead.
- Sheet bodies scroll inside the sheet: `ensureVisible` before tapping rows lower down.
- Python heredocs in the Bash tool can fail to parse on long scripts; write the script with Write and run `python -I file`.
