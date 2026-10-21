---
name: project-main-mc-v3-fe3-2026-10-18
description: Main MC v3 FE-3 (7e2adc9 pushed feat/main-v3) - Agenda/To-do sheets ticked on Main, McListsCubit account-scoped + optimistic revert, Workspace reload via isAccountScopedInstanceLive, close method "action", test gotchas (stub reads optimistic state, map contains, isSemantics)
metadata:
  type: project
---

FE-3 of Main MC v3 committed as 7e2adc9 + b15903c (tick_failed event) on `feat/main-v3` (worktree mindsync-frontend-wt-main-v3) and pushed. Builds on [[project-main-mc-v3-fe2-2026-10-18]].

- `McListsCubit` is now `registerAccountScoped` (McMainScreen takes the GetIt one; `test/core/account_scope_reset_test.dart` lists it). `setAgendaDone` / `setTodoDone` return false only on failure; per-item revert to the original index; in-flight ids ignored.
- Workspace sync: `AgendaCubit`/`TodoCubit` have `loadActive({silent})`, NOT `load()`. Refresh only when `isAccountScopedInstanceLive<T>()` so Main never builds a Workspace cubit.
- `McCloseMethod.action` / `mainCloseAction` added for "Edit in Workspace" (closes sheet then `selectTab(workspace, scrollTo:)`); `mcEditInWorkspace` + `mcWorkspaceTabIndex` live in widgets/mc_check_row.dart.
- `workspace_item_action` from Main: logged once on server success (not on tap), props exactly section_name/action/surface; a failed tick logs `main_sheet_action` tick_failed (Main-only, avoids the workspace branch's `check_failed` constant).

**Why:** FE-4/FE-5 and integration reuse these seams; the gotchas cost a test round.
**How to apply:**
- A mocktail `thenAnswer` closure that reads `cubit.state` runs AFTER the optimistic emit; answer from captured sample items instead.
- `expect(listOfMaps, contains({...}))` fails (identity); use `contains(equals({...}))`.
- Flutter 3.41: `containsSemantics` is deprecated, use `isSemantics` (same params, partial match).
- This SDK prints analyzer lines as `error - ...`, not `error •`; filter with `^ *error`.
- `dart format --output=none` still says "Changed" but writes nothing; FE-1 test files are not 120-formatted, so never format them whole.
- Existing error strings (`therapy_couldNotSaveChanges`, `common_errorTryLater`) lack diacritics in de/fr/nb; add a clean `mc_` key instead.
