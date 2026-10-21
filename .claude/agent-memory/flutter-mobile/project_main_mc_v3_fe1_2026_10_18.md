---
name: project-main-mc-v3-fe1-2026-10-18
description: Main MC v3 FE-1 (c3b222b, pushed feat/main-v3, worktree mindsync-frontend-wt-main-v3) - tile shell under lib/screens/main_tab/mc, scrim-vs-back sheet route, post-frame/ensureVisualUpdate trap, NNBSP in jm(), test harness McHarness
metadata:
  type: project
---

FE-1 of Main MC v3 (team main) committed as c3b222b on `feat/main-v3` and pushed (upstream set to origin/feat/main-v3; the worktree branch was created tracking origin/dev, so a bare `git push` was a risk). FE-2..FE-5 replace the interim sheets.

- Layout: `lib/screens/main_tab/mc/` (mc_main_screen, tiles/mc_tile_models pure rules for all 8 tiles, widgets/mc_sheet|mc_tile|mc_header|mc_status_row|mc_icons|mc_type|mc_dot, lists/McListsCubit read-only, mc_seen_store, mc_analytics). `MainTabScreen` keeps only refresh-on-visit + `FirstWeekCubit.load()` and passes `mainLegacySheetBody` (today's widgets) to McMainScreen.
- `McSheetRoute extends ModalBottomSheetRoute`: the barrier and system back both call `maybePop`, so scrim is detected with a `Listener` around `super.buildModalBarrier()` (pointer-up within 1 s of the pop). Sheet code closes via `McSheet.close(context, method)`.
- Test harness: `test/screens/main_tab/mc/mc_test_support.dart` (`McHarness.install(McSample.home()|states())`, MCHome/MCStates sample data). Parity shots: `test/main_parity_shots/` (tag marketing, `MAIN_PARITY_SHOTS_DIR`), boundary in `MaterialApp.builder`, `ParityShell` stand-in nav+FAB inside `home` so sheets cover it.

**Why:** later Main tasks build on these seams; the gotchas cost time.
**How to apply:**
- `addPostFrameCallback` alone schedules no frame: `pumpAndSettle` then never runs it (and on device it can wait). Chain `..ensureVisualUpdate()`.
- intl `DateFormat.jm()/j()` put U+202F before AM/PM; boards show a plain space. Normalize in test assertions, not in the app.
- Ahem in widget tests makes tiles taller than 132; visibility tests must compute expectations from real rects.
- mocktail `thenThrow` throws synchronously, so `future.catchError` never sees it; wrap optional calls in an async try helper.
- Dart files in this worktree are CRLF, ARB files LF; keep each file's ending when scripting edits.
- `dart run build_runner` (~3 min cold) also rewrites unrelated `.freezed.dart` with real diffs: restore everything not yours before staging.

Related: [[project-workspace-wa1-v3-fe1-2026-10-18]], [[project-cards-v3-fe3-2026-10-18]].
