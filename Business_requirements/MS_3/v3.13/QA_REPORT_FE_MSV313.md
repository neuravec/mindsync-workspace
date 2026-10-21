# QA Report – Frontend – MSV3.13 – 2026-09-03

Worktree: `C:/Users/mikol/Notebooks/MindSync/Heroku/wt-msv313-fe/mindsync_app`, branch `msv3.13`, HEAD `733444a` (commits `3fa50c7` CS-02, `733444a` CS-01), base `dev` `73e5314`.
Comparison baseline: untouched `dev` checkout at `C:/Users/mikol/Notebooks/MindSync/Heroku/mindsync-frontend/mindsync_app` (read-only, not modified).
No app code was edited. No tests were added – no coverage gap tied to this batch was found (see section 3). Nothing was pushed.

## Verdict: GO

`flutter analyze` is byte-for-byte identical between the branch and untouched `dev`. Every failing test in the full `test/` tree (31 of 2,196 run) reproduces identically on the untouched `dev` checkout, so all 31 are pre-existing baseline failures, not regressions. Zero references to the removed `custom_interval_days`/`customIntervalDays` field remain in `lib/`. The batch's own coverage matrix (CS-02's custom-frequency UI/payload/parsing and CS-01's debrief-match fix across all three frequency modes and both 72h branches) is fully present and green. One typography violation (em dash) was found in two newly-added test-file comments; it is cosmetic only, not a functional or test-correctness issue, and does not change the verdict.

---

## 1. flutter analyze

Ran on both the worktree and the untouched `dev` checkout.

| | Worktree (msv3.13) | dev (73e5314) |
|---|---|---|
| Errors | 1 | 1 |
| Warnings | 9 | 9 |
| Infos | 128 | 128 |
| Total | 138 | 138 |

Sorted, normalized (timing line stripped) diff between the two full outputs: **identical, zero differences**. No new analyzer issue was introduced by this branch. The single error (`test/screens/main_tab/widgets/session_setup_screen_test.dart:111:70`, `body_might_complete_normally`) is pre-existing on `dev` and is the same known compile error referenced in the task baseline.

## 2. Test suite – per-directory pass/fail, whole `test/` tree

Run with `flutter test <dir> --concurrency=2`, one process at a time, foreground. `test/screens/fab_flows/record_session_appbar_close_test.dart` was excluded per instructions (known hang); the other six files in that directory were run explicitly by path. No orphaned `flutter_tester`/`dart` processes were found before starting.

| Directory | Pass | Fail | Notes |
|---|---:|---:|---|
| test/api | 138 | 0 | |
| test/bloc | 102 | 0 | |
| test/core | 86 | 0 | |
| test/navigation | 65 | 0 | |
| test/providers | 6 | 0 | |
| test/services | 101 | 0 | |
| test/utils | 122 | 0 | |
| test/widgets | 158 | 0 | |
| test/screens/{account,auth,character_tab,debrief_capture,errors} | 142 | 0 | |
| test/screens/{health_check,main_page,moments,my_therapy} | 91 | 0 | |
| test/screens/main_tab | 248 | 1 | pre-existing (below) |
| test/screens/settings | 50 | 0 | |
| test/screens/reflect_tab | 73 | 0 | |
| test/screens/{sign_up,splash,welcome} | 59 | 0 | |
| test/screens/{stats_tab,subscription} | 68 | 0 | |
| test/screens/therapy_capture | 57 | 0 | |
| test/screens/therapy_onboarding | 89 | 1 | pre-existing (below) |
| test/screens/therapy_tab | 192 | 6 | pre-existing (below) |
| test/screens/wow | 7 | 3 | pre-existing (below) |
| test/screens/workspace | 193 | 0 | |
| test/screens/fab_flows (6 of 7 files; hang file excluded) | 43 | 0 | |
| test/ui/settings | 13 | 5 | pre-existing (below) |
| test/ui/main_tab | 15 | 0 | |
| test/ui/reflect_tab | 29 | 15 | pre-existing (below) |
| test/l10n_completeness_test.dart + test/widget_test.dart | 18 | 0 | |
| **Total run** | **2165** | **31** | **all 31 pre-existing** |

`test/screens/fab_flows/record_session_appbar_close_test.dart` was not run (excluded per instructions, known hanging file, not a compile/logic failure).

### Failing tests – all classified PRE-EXISTING, proven by direct re-run on untouched dev

Each was re-run on the untouched `dev` checkout and reproduces identically (same failure, same assertion, same line):

1. `test/screens/main_tab/widgets/session_setup_screen_test.dart:111:70` – compile error, `body_might_complete_normally` on `when(() => settingsCubit.addCustomSession(any())).thenAnswer((_) {});`. Confirmed: identical source line on `dev`; same compile failure when run standalone on `dev`.
2. `test/screens/therapy_onboarding/onboarding_lead_source_view_wave4_test.dart` – 1 failure, "tapping other chip calls setLeadSource(\"other\")" (`No matching calls` on the mock). Confirmed: same single failure when the file is run standalone on `dev`.
3. `test/screens/therapy_tab/therapy_card_detail_screen_error_test.dart` – 6 failures (500-response leak guard, no-response guard, generic-exception guard, 404 "source removed" message, retry-button re-fetch, retry-button tap-target size). Confirmed: same 6 failures, same file, when run standalone on `dev`.
4. `test/screens/wow/wow_screen_adaptive_cta_test.dart` – 3 failures ("not_right_now shows the 3-action core menu", "never_been shows the 3-action core menu (no \"session\")", "null therapy status defaults to the 3-action core menu"). Confirmed: same 3 failures when run standalone on `dev`.
5. `test/ui/settings/widgets/save_feedback_indicator_test.dart` – 5 failures (all animation-timing/opacity assertions, `StateError: Bad state: Too many elements` / opacity-value mismatches). Confirmed: same 5 failures when run standalone on `dev`.
6. `test/ui/reflect_tab/reflect_thinking_indicator_test.dart` – 15 failures (bubble border-radius, breathing-dot opacity widgets, alignment, etc.). Spot-confirmed: same failure signature reproduces on `dev` standalone; count (15) matches the documented pre-existing baseline exactly.

None of these six files were touched by this branch's diff (`git diff 73e5314..HEAD --stat`), and none relate to therapy-schedule/frequency or debrief-matching logic. **Zero NEW failures.**

## 3. Coverage check for the batch

All six required coverage points are present and green, with exact file/test names:

**(a) Custom segment renders only the calendar, no interval row**
`test/ui/settings/widgets/therapy_frequency_selector_test.dart`:
- "no interval row and no calendar are shown for weekly (MSV3.13 CS-02)"
- "custom frequency shows the calendar and nothing else (MSV3.13 CS-02)" > "selecting Custom reveals the calendar view"
- "custom frequency shows the calendar and nothing else (MSV3.13 CS-02)" > "no \"Every\"/days interval row is rendered for Custom - the user hand-picks dates on the calendar instead"
- "custom frequency shows the calendar and nothing else (MSV3.13 CS-02)" > "deselecting Custom (switching to Weekly) hides the calendar"

**(b) PUT payload has no `custom_interval_days`**
`test/api/users_manager_therapy_schedule_test.dart` > "syncTherapySchedule PUT payload contract" > "the PUT body never contains a custom_interval_days key"

**(c) GET JSON with and without the legacy key parses**
`test/api/models/settings/therapy_schedule_response_test.dart` – "a response still carrying the legacy custom_interval_days key" (the deliberate backward-compat literal, line 85) plus the model's normal-response parse cases in the same file (all part of the 138/138 green `test/api` run).

**(d) Main-tab offline fallback for custom = manual dates**
`test/ui/main_tab/main_tab_next_session_test.dart` > "NextSession computation" > "custom frequency (MSV3.13 CS-02: calendar dates only)":
- "returns null when there are no custom sessions at all"
- "returns null when every custom session is in the past"
- "returns the nearest future custom session, ignoring farther and past ones"
- "an empty recurring schedule does not prevent a custom-session result - custom frequency never reads [schedule]"

**(e) `debriefMatchesSession` 49h/3d/6d/30d = match, before-session = no match, day boundary**
`test/screens/main_tab/cubit/next_session_action_test.dart` > "debriefMatchesSession":
- "same calendar day as the session is a match"
- "created 47h after the session on a different day matches"
- "created 49h after the session still matches (no upper bound)"
- "created 3 days after the session still matches"
- "created 6 days after the session still matches (Darek's repro)"
- "created 30 days after the session still matches"
- "created before the session does not match"
- "session at 23:50, debrief created 20 minutes later (past midnight, different calendar day) still matches"
- "session at 23:50, debrief created 6 days later (crossing several midnights) still matches"
- "session on Dec 31 23:00, debrief created Jan 1 00:30 (year boundary) still matches"

**(f) Darek's repro through `computeNextSessionAction` in all three frequency modes and both 72h branches**
`test/screens/main_tab/cubit/next_session_action_late_debrief_cs01_test.dart` (new file, 9 distinct scenarios × parametrization = 20 executed test instances):
- "MSV3.13 CS-01: late After Therapy unsticks the card (Darek repro, custom one-off session, no future date)" – After Therapy submitted 1h / 30h / 144h (6d) / 720h (30d) late → `noNextSessionKnown`, no future session on the calendar.
- "MSV3.13 CS-01: late debrief (6 days, Darek's own number) with a future session known" – future session >72h away → `betweenSessions`; future session <72h away → `prepCta`.
- "MSV3.13 CS-01 regression guard: recurring frequencies (weekly, biweekly) are not left stuck by a late debrief" – weekly and biweekly, each with a 3-day-late debrief, both unstick correctly.

Together with `test/screens/main_tab/cubit/main_tab_cubit_next_session_test.dart` (custom-frequency `_computeNextSession`/`_computeLastSession` gap tests, calendar-dates-only) and `test/screens/settings/cubit/settings_cubit_therapy_schedule_test.dart` (signature/call-site coverage for the removed `customIntervalDays` parameter), the batch's two changes (CS-02 removal, CS-01 fix) are both covered end to end: unit-level predicate, cubit-level state-machine, widget-level UI, and wire-level API contract. **No coverage gap tied to this batch was found; no new tests were written.**

## 4. Grep gate

`customIntervalDays|custom_interval_days|CustomInterval|customInterval`:

- `lib/`: **0 hits.** Clean.
- `test/`: 13 hits, all expected:
  - Historical/explanatory comments referencing the MSV3.13 CS-02 removal (`main_tab_cubit_next_session_test.dart:16`, `settings_cubit_therapy_schedule_test.dart:23,26,27,242,255`, `main_tab_next_session_test.dart:23`, `therapy_frequency_selector_test.dart:15`, `users_manager_therapy_schedule_test.dart:101`).
  - One deliberate legacy-key JSON literal exercising backward compatibility: `test/api/models/settings/therapy_schedule_response_test.dart:75,80,85` ("a response still carrying the legacy custom_interval_days key").

No production code or non-backward-compat test logic still references the removed field.

## 5. Em dash gate

Scanned all lines added by `git diff 73e5314..HEAD` (this branch vs. base `dev`) for U+2014. Found **2 occurrences**, both in one test file's comments/group descriptions (not production code, not user-facing copy):

- `mindsync_app/test/screens/main_tab/cubit/main_tab_cubit_next_session_test.dart:37` – `// Gap 3 — Custom frequency: reads only the hand-picked calendar sessions`
- `mindsync_app/test/screens/main_tab/cubit/main_tab_cubit_next_session_test.dart:55` – `group('_computeNextSession — custom frequency (calendar dates only)', () {`

These are internal test-code comments/group labels, not shipped UI text or documentation prose, and do not affect test correctness or behavior. Flagging per the project's em-dash ban for completeness; not fixed here since it is cosmetic and outside this task's DONE_WHEN (report either way). If desired, these two characters can be swapped for a plain hyphen or restructured sentence in a follow-up touch of this test file.

## 6. Files touched by this QA pass

- Read only. No application code, test code, or configuration was modified.
- Report written to: `C:/Users/mikol/Notebooks/MindSync/Heroku/Business_requirements/MS_3/v3.13/QA_REPORT_FE_MSV313.md` (this file).

## Summary

GO. `flutter analyze` shows zero delta versus `dev`. All 2,196 executed tests are accounted for: 2,165 pass, 31 fail, and every one of the 31 failures independently reproduces on the untouched `dev` checkout, so none are attributable to this branch. The CS-02 (custom-interval removal) and CS-01 (debrief-match ceiling removal) changes each have direct, passing test coverage spanning unit/cubit/widget/wire layers, including Darek's exact multi-day-late repro across all three frequency modes and both sides of the 72h between-sessions/prepare boundary. The only defect found is two em dashes in test-file comments (cosmetic, non-blocking).
