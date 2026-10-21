---
name: project-main-mc-v3-fe2-2026-10-18
description: Main MC v3 FE-2 (22b468a pushed feat/main-v3) - session/relationship/observations/affirmation sheets, McSheetHarness state-driving recipe, --no-pub, Write tool \u escapes, 120 col format, context_description already says "Based on"
metadata:
  type: project
---

FE-2 of Main MC v3 committed as 22b468a on `feat/main-v3` (worktree mindsync-frontend-wt-main-v3) and pushed. Builds on [[project-main-mc-v3-fe1-2026-10-18]].

- `McMainScreen._mcSheetBody(id)` opens the MC v3 sheet for session, relationship, observations, affirmation; other tiles still use `sheetBody` (MainTabScreen's interim legacy bodies) until FE-3..FE-5 add their case there. `McMainScreen` takes `sessionActions` (McSessionActions) and `openCheckIn` for tests.
- Shared rules live in mc_tile_models: `mcSessionInfo` (McSessionKind) and `mcRelationshipKind`, used by tile AND sheet. Shared widgets: `widgets/mc_buttons.dart` (McPrimaryButton 52/r26, McDisabledButton, McDoneRow, McUsageChip, McSheetLoading, McSheetError(tile) logging `retry`).
- Test harness: `test/screens/main_tab/mc/sheets/mc_sheet_support.dart` `McSheetHarness.install(sample)` re-stubs `whenListen(h.mainTab, controller.stream, ...)` so a test can push new MainTabStates mid-test; `pumpSheet(tester, sample, tileId)`.

**Why:** later Main tasks reuse these seams and the gotchas below cost time.
**How to apply:**
- Run `flutter test --no-pub` / `flutter analyze --no-pub`: without it every run does pub get and rewrites linux/macos/windows plugin registrants (restore with `git checkout --` before staging).
- The Write tool turns backslash-u escapes in file content (the long dash 2014, even the narrow no-break space 202f) into the literal characters. In Dart use `String.fromCharCode(0x202f)`; scan new files for non-ASCII bytes with grep -P before committing.
- FE-1 mc/ files are formatted with `dart format --line-length 120`; format only new files (and your own hunks).
- Pure (non-widget) tests calling `DateFormat` need `await initializeDateFormatting('en')` in setUpAll.
- Backend `context_description` usually already starts with "Based on ..." (LLM prompt), so the legacy "Based on: " prefix doubled it; `mcObservationBasis` skips the prefix when the text starts with the localized label.
- Board `done_session` state in MCStates ("Friday at 5:00 PM with Anna, every week.") is a demo flip; the real sheet shows the upcoming state after setup (SPEC 3.1 wins).
