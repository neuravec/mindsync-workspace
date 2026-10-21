# QA regression: subscription + onboarding redesign

Date: 2026-10-02/03 (runs crossed midnight local time). Branch `feat/subscription-onboarding-redesign` in both repos, all changes uncommitted. Backend HEAD 7d467c8 (= `main`), frontend HEAD a985620 (= `dev`).

## Verdict

**GO for commit.** No NEW failure remains. Every failure still present also fails on a clean checkout of `main` (backend) or `dev` (frontend). Four test-only fixes were needed; all four were tests made wrong by an intended change in this batch (listed below). Nothing was committed or pushed, no app code was touched.

Two follow-ups for the lead (not blocking the commit):

1. The new copy for `onboarding_modalityTitle` ("What kind of therapy is it?") also changes the title of the My Therapy "edit therapy approach" sheet, which reuses the key (`lib/screens/my_therapy/widgets/therapy_modality_edit_sheet.dart:130`). It reads fine there, but it is a second surface the spec did not mention.
2. `test_purchase_path_trial_ended_does_not_require_consent` pins that the purchase path emits `trial_ended` (outcome converted) without the consent check. Only the hourly job is consent-gated (G21 option A). Confirm this matches the lead decision.

## Test-only fixes made (each one is an intended behavior change)

| File | Why it was wrong | Change |
|---|---|---|
| `MindSync/app/tests/test_prep_card_overhaul.py::TestAutoGenerateEndpoint::test_auto_generate_free_tier_raises_403` | Security fix H-1 moved the auto-generate gate from `can_use_ai` to `is_user_premium`. The test still patched `can_use_ai`, so with a MagicMock db the endpoint passed the gate, created a card and made a real OpenAI call with the dummy key (about 50 s of retries), then failed on response validation. | Patch `is_user_premium=False`, assert 403 and that `crud.create_session_prep_card` is never called. |
| `mindsync_app/test/screens/my_therapy/my_therapy_screen_test.dart` (modality edit saves) | Expected the old title "Choose your therapy approach"; copy-en.md changes `onboarding_modalityTitle` to "What kind of therapy is it?" (existing key, new text). | Expect the new title (2 lines). |
| `mindsync_app/test/screens/wow/wow_cubit_test.dart` ("trial days come from the subscription end date") | New test. Trial days are counted in local calendar days (FE-FIX-1 M9), but the test used `DateTime.now() + 70 h`, so the result was 2 or 3 depending on the hour it ran (it failed at 00:10). | End date = local noon 3 calendar days ahead. |
| `mindsync_app/test/screens/wow/wow_screen_test.dart` + `wow_test_helpers.dart` ("first step in therapy: trial chip...") | Same issue with `now + 80 h`, expecting "4 days left"; only passes between 16:00 and midnight. | New helper `trialEndInCalendarDays(int)` in `wow_test_helpers.dart`; default and this test use 4 calendar days at local noon. |

After the fixes `test/screens/wow` passes 75/75 and `test/screens/my_therapy` 13/13, verified after midnight when the old versions failed.

## Backend (pytest)

The single full run (`python -m pytest app/tests/ -q`) got through 100% of tests with 10 `F` marks but hit the 10-minute tool limit before printing its summary. So the same file list was rerun in two halves to get the summary; the counts match.

| Run | Passed | Failed |
|---|---|---|
| Half 1 (103 files) | 2954 | 5 |
| Half 2 (102 files) | 3133 | 5 |
| **Total before the test fix** | **6087** | **10** |
| **Total after the test fix** | **6088** | **9 (all BASELINE)** |

All 9 remaining failures also fail on a clean `main` worktree (7 test files rerun there: 9 failed, 407 passed). The batch's own test files (`test_subscription_onboarding_redesign.py`, `test_starter_pack_premium_source.py`, `test_trial_lifecycle_events.py`, `test_behavioral_posthog.py`, `test_prep_cards.py`, `test_debriefs.py`, `test_between_sessions.py`, `test_subscription_cross_account_guard.py`, `test_timeline.py`) pass together: 422/422.

The known flaky `test_consent::test_is_consent_active_after_regrant_returns_true` passed in this run. The baseline is 9 here, not the ~20 the implementer listed. The split run may order tests differently, but the full run's dot stream also showed exactly 10 `F` marks.

### BASELINE failures (backend)

- `test_first_impression.py::TestFirstImpressionEndpoint::test_language_mapping` (`'de' == 'German'`)
- `test_notification_improvements.py::TestBetweenSessionsPlaceholder::test_between_sessions_key_in_defaults`
- `test_notification_improvements.py::TestBetweenSessionsPlaceholder::test_between_sessions_default_is_true`
- `test_notification_improvements.py::TestBetweenSessionsPlaceholder::test_between_sessions_placeholder_comment_in_source`
- `test_notification_improvements.py::TestNotificationTimezoneIndexMigration::test_migration_creates_index`
- `test_onboarding_v2.py::TestResetTherapyOnboarding::test_preserves_therapy_data`
- `test_symptom_suggestions.py::TestSymptomSuggestionResponseSchema::test_from_attributes_config`
- `test_therapy_frequency.py::TestIsOnWeekYearBoundary::test_year_boundary_dec_to_jan_known_limitation`
- `test_walkthrough.py::TestCompleteWalkthroughStepEndpoint::test_all_five_tabs_awards_points`

### Boot check

Env shims from `app/tests/conftest.py`, plus a Windows-only `rq` stub (no `fork` on Windows) and a mocked Firebase credential, then `import app.main`:

- Branch: `import app.main` OK, 343 routes, `/api/v1/users/usage` registered. Every table (79) compiles to DDL with the `postgresql` dialect.
- Clean `main`: OK, 342 routes, 79 tables.
- `app/models/models.py` only adds the `STARTER_PACK = "starter_pack"` constant and `PAID_GRANTED_VIA_VALUES` on an existing `String(20)` column. No new table or column, no Alembic migration in this batch, so deploy does not depend on a migration.
- Caveat: Python 3.14 locally, Heroku runs 3.12.2.

## Frontend (flutter test, one directory at a time, `--exclude-tags marketing`)

| Directory | Passed | Failed | Class |
|---|---|---|---|
| top-level (`l10n_completeness_test.dart`, `widget_test.dart`) | 18 | 0 | |
| api | 138 | 0 | |
| bloc | 128 | 0 | |
| core | 86 | 0 | |
| navigation | 70 | 0 | |
| providers | 8 | 0 | |
| services | 120 | 0 | |
| support | 11 | 0 | |
| utils | 122 | 0 | |
| ui | 78 | 18 | BASELINE (identical list on `dev`) |
| widgets | 158 | 0 | |
| screens/account | 7 | 0 | |
| screens/audio_chat | 24 | 0 | |
| screens/auth | 31 | 0 | |
| screens/character_tab | 51 | 0 | |
| screens/debrief_capture | 61 | 0 | |
| screens/errors | 4 | 0 | |
| screens/fab_flows | 43 | 2 | BASELINE + HANG (`record_session_appbar_close_test.dart`) |
| screens/health_check | 30 | 0 | |
| screens/main_page | 34 | 0 | |
| screens/main_tab | 268 | 0 | |
| screens/moments | 22 | 0 | |
| screens/my_therapy | 13 | 0 | was 12/1 before the test fix |
| screens/reflect_entry | 78 | 0 | |
| screens/reflect_tab | 149 | 0 | |
| screens/settings | 50 | 0 | |
| screens/sign_up | 50 | 0 | |
| screens/splash | 17 | 0 | |
| screens/stats_tab | 40 | 0 | |
| screens/subscription | 132 | 0 | |
| screens/therapy_capture | 57 | 0 | |
| screens/therapy_onboarding | 160 | 0 | |
| screens/therapy_tab | 192 | 6 | BASELINE (identical list on `dev`) |
| screens/usage | 95 | 0 | |
| screens/welcome | 8 | 0 | |
| screens/workspace | 193 | 0 | |
| screens/wow | 75 | 0 | was 73/2 before the test fixes |
| **Total** | **2821** | **26** | all BASELINE |

`test/marketing_shots` was skipped as instructed. The baseline is 26 failures (known baseline about 30).

### Settled: `record_session_appbar_close_test.dart`

Run alone on the branch and on a clean `dev` worktree (`flutter pub get` there), both give exactly the same result:
- "AppBar-X on a Yieks-class error (mic permission) calls discardRecording()" fails after 1 s with `Found 0 widgets with type "VoiceErrorCard"`.
- "AppBar-X on a non-Yieks error (network upload failure) does NOT call discardRecording()" never completes and was killed at the 570 s cap.

Verdict: **BASELINE + HANG**, not caused by this batch.

### BASELINE failures (frontend)

- `test/ui/reflect_tab/reflect_chat_bubble_test.dart`: 3 (border radius, deepOcean left border, user variant background)
- `test/ui/reflect_tab/reflect_chat_input_test.dart`: 5 (accent bar height 0 / 3, borderRadius 12, send SVG, disabled while waiting)
- `test/ui/reflect_tab/reflect_starter_chips_test.dart`: 1 (48 px tap target)
- `test/ui/reflect_tab/reflect_thinking_indicator_test.dart`: 4
- `test/ui/settings/widgets/save_feedback_indicator_test.dart`: 5
- `test/screens/therapy_tab/therapy_card_detail_screen_error_test.dart`: 6 ("Router operation requested with a context that does not include a Router")
- `test/screens/fab_flows/record_session_appbar_close_test.dart`: 2 (see above)

### NEW failures

None after the four test-only fixes. Before the fixes there were 4 NEW failures (backend prep auto-generate 403, my_therapy modality title, two wow trial-day tests); the causes and fixes are in the table at the top.

### flutter analyze

- 153 issues: **0 errors**, 10 warnings, 143 infos.
- Changed files (`git diff --name-only dev` plus untracked, 208 files): no warnings in batch app or test code. The one warning in a changed file is `test/marketing_shots/therapy_timeline_shot_test.dart:19` (unused import), an untracked marketing-shots file outside this batch's scope. There are 33 infos in changed files, all lint-level: `prefer_const_*`, deprecated `hasFlag` in tests, and deprecated `DropdownButtonFormField.value` at `lib/screens/therapy_onboarding/views/onboarding_schedule_view.dart:263`.

## Re-verification matrix (item 3)

All named tests exist and passed in the runs above.

| Behavior | Covering tests (passing) |
|---|---|
| (a) usage 404/500: no chips, no gates, no trial UI | `test/screens/usage/usage_model_and_cubit_test.dart` "404 (backend without the route...) -> unavailable, every chip hidden, nothing gated" and "500 usage_unavailable -> ..."; `usage_chip_and_gate_test.dart` "renders nothing for premium, errors..." and "hidden (usage 404): the flow opens, untouched"; `usage_external_entry_gate_test.dart` "usage unavailable (5xx): behaves as today"; `trial_visibility_test.dart` "hidden for usage 404" (TrialBar), "never with usage unavailable (404 before the backend deploy)", "usage 404: nothing at all". Backend: `TestUsageEndpoint::test_error_returns_500_not_a_plan`. |
| (b) gate at zero opens paywall, never blocks reading | `usage_chip_and_gate_test.dart` "at 0: logs, opens the paywall for the feature, returns false after close", "After therapy at 0 opens the paywall, not the flow"; `usage_external_entry_gate_test.dart` "reading routes are never gated", "a reading route navigates synchronously, unchanged", "at 0: every creation flow becomes its premium_gate paywall". |
| (c) starter transaction handled by one cubit; non-VERIFIED → no success | `test/screens/subscription/cubit/subscription_cubit_analytics_test.dart` "G2: a starter-pack transaction is ignored completely", "only VERIFIED passes"; `test/screens/main_page/daily_page/cubit/starter_package_cubit_test.dart` "a subscription product on the shared stream is ignored", "G4: a 200 with status FAILED: no retry, no success, transaction left open"; `test/providers/subscription/subscription_repository_test.dart` "markAsOneTimePurchased throws ReceiptNotVerifiedException on FAILED". Backend: `test_starter_pack_premium_source.py::TestStarterPurchaseSetsSource::test_failed_verification_writes_nothing`. |
| (d) 5-step vs 7-step branching, resume, answer change, consent once | `therapy_onboarding_cubit_branching_test.dart` "in therapy with consent: 7 steps...", "status $status: 5 steps...", "a yes answer without Art.9 consent does not count", "changing the answer back to in therapy brings the steps back", "changing the answer to not in therapy removes them again", "saved step 6 (not in therapy) resumes on the companion, 5 steps", "resumed on step 4, answering the journey again resets branching"; `therapy_onboarding_fe_fix1_test.dart` "in therapy: 7 steps, back to next session...", "after a saved schedule, switching the answer sends an empty one"; consent once: `onboarding_redesign_views_test.dart` "both boxes required; consent accepted exactly once" and `onboarding_gdpr_sequencing_test.dart` "acceptConsent calls UsersManager.flushPendingProfile once". |
| (e) existing-account log-in routing | `test/services/post_login_destination_resolver_test.dart` "onboarding completed -> main page", "onboarding not completed -> therapy onboarding (the bug fix)", "backend 5xx -> main page as before, never read as needs onboarding", "network error -> main page as before"; `test/screens/auth/auth_cubit_email_login_destination_test.dart` (passes in screens/auth). |
| (f) no cold OS push prompt for new-flow accounts; unchanged for existing | `test/services/fcm_cold_prompt_policy_test.dart` "existing users: initialize() still asks the OS cold, exactly as before", "during the post-onboarding flow: no cold prompt...", "new-flow account with permission granted: token still registered, no dialog", "Not now persists per account...". |
| (g) backend rules | Free cannot auto-generate prep cards: `test_subscription_onboarding_redesign.py::TestSecurityFixH1AutoGenerate::test_free_user_with_no_manual_card_is_refused_every_time`, `::test_expired_trial_is_refused`, `TestEndpointGates::test_prep_auto_generate_403_detail_unchanged`, plus the fixed `test_prep_card_overhaul.py::...::test_auto_generate_free_tier_raises_403`. Non-allowlisted SKU: `TestSecurityFixH2OneTimePurchase::test_non_one_time_sku_is_400_before_receipt_and_events`, `::test_google_subscription_sku_also_refused`, `test_starter_pack_premium_source.py::...::test_other_one_time_sku_is_refused`. Per-type limits: `TestPerTypeCounters` (8 tests). Usage equals gate counters: `TestUsageEndpoint::test_used_equals_gate_counters`, `TestSecurityFixesM1M2::test_usage_used_matches_gate_after_delete`, `TestPlanPersonProperties::test_helper_matches_usage_endpoint`. `trial_ended` without consent: `test_trial_lifecycle_events.py::test_hourly_job_no_trial_ended_capture_without_consent`, `::test_hourly_job_no_capture_when_context_exists_without_consent` (see follow-up 2 for the purchase path). |
| (h) privacy: no typed text in events | `therapy_onboarding_analytics_fe_fix2_test.dart` `expectPrivacy()` (typed name, custom focus area, goal text and orca name never in any property, used in 3 journeys); `test/screens/wow/wow_cubit_test.dart` "privacy: no event carries the name, focus area names or bio text"; `subscription_body_test.dart` "G17: promo expanded once per paywall...; the code is never sent"; `usage_model_and_cubit_test.dart` "usage_load_failed ... carries no message". Backend: no dedicated "no free text" test. The batch's backend events carry only plan, source, outcome and platform fields, and `TestPinnedPaymentEventProperties` pins their exact property sets. |

No behavior in the list is without a passing test.

## l10n (item 4)

- `test/l10n_completeness_test.dart`: passes (in the top-level run, 18/18).
- Added lines in `git diff dev -- lib/l10n/app_*.arb` (all 7 files, 2488 added lines): **0** U+2014, **0** U+2013.
- For information: the regenerated `lib/l10n/generated/app_localizations.dart` has 2 added doc-comment lines with U+2014. They come from two older strings (the "recordings under 10 minutes" and "use other apps while saving" texts), not from keys added by this batch.

## What could not be run as asked

- The backend full suite could not print its summary within the 10-minute tool cap. The run reached 100% (10 `F`), and the summary came from the same file list split into two halves.
- `record_session_appbar_close_test.dart` hangs (over 9 minutes, killed at the cap) on both the branch and `dev`.
- Temporary worktrees (`main` for the backend, `dev` for the frontend) were created in the session scratchpad and removed afterwards. `git worktree list` shows only the main checkouts.
