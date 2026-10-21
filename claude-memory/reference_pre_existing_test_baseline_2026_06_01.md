---
name: reference-pre-existing-test-baseline-2026-06-01
description: "As of 2026-06-01 the test suite has ~85 PRE-EXISTING failing tests (NOT regressions). Which they are + why, so future sessions don't misattribute them."
metadata: 
  node_type: memory
  type: reference
  originSessionId: 94b6bc39-12b3-4989-a285-b47b82295a02
---

As of 2026-06-01, before any new feature work, the full test suites already have a large pre-existing red baseline. Establishing this so a future session that runs `pytest`/`flutter test` does NOT blame its own changes.

**Backend (full `pytest app/tests/`): ~54 pre-existing failures (separate from any new work).** Categories:
- **Legacy-disabled notification tests (~30):** `test_notification_improvements`, `test_notification_premium_gate`, `test_post_session_nudge`, `test_prep_card_overhaul::TestNotifyPrepMorningOf`, `test_prep_reminder`, `test_symptom_tracking_reminder`, `test_health_check*`. These exercise legacy `notify_*` functions gated by `settings.notification_legacy_jobs_enabled` (default **False**, `config.py:234`), which early-return after the moments hard cutover (2026-05-15). Mocks asserted "called once" → "called 0 times". The live path is the orchestrator, not these. See [[project-notification-moments-shipped-2026-05-15]].
- **Time-bombed test (1):** `test_moments_endpoints_get_by_id::test_own_moment_returns_200` — moment factory hardcodes `2026-05-15` + expires_at=+24h; endpoint compares to real `now` → 404 (expired). Fix = make the fixture date relative to now.
- **Untouched-module drift (~23):** `test_voice_fixes` (RAG injection), `test_walkthrough`, `test_first_impression`, `test_symptom_suggestions`, `test_therapy_frequency`, `test_custom_therapy_sessions`, `test_onboarding_v2::test_preserves_therapy_data`, `test_dedup_key_generators::TestMoodDip...` — schema/enum-drift or stale assertions in modules unrelated to notifications/summaries.

**Frontend (full `flutter test`): ~31 pre-existing failures.** Categories:
- **Stale design-token widget tests (21):** `test/ui/reflect_tab/*` (reflect_chat_bubble/input/starter_chips/thinking_indicator — assertions like "4px deepOcean left border", "16px radius"), `test/ui/settings/widgets/save_feedback_indicator_test.dart` (5), `test/ui/settings/widgets/therapy_frequency_selector_test.dart` (2). Widgets pumped in isolation; not affected by global/DI changes.
- **ConsentManager GetIt registration gap (10):** `test/screens/sign_up/onboarding_gdpr_sequencing_test.dart` (6) + `test/screens/settings/privacy_data_section_test.dart` (4). `TherapyOnboardingCubit` has a pre-existing eager field `final ConsentManager _consentManager = sl();` (cubit line ~32, added in the May consent work); these tests' `setUp` never registers a `ConsentManager` mock → `Bad state: GetIt ... ConsentManager is not registered` at construction. Fix = register a `MockConsentManager` in those tests' setUp (and stub `getArt9HealthStatus`/`grant`/`withdraw` if the path hits them). privacy_data_section's "no CircularProgressIndicator" may be a separate stale loading assertion.

**Verification method:** these were confirmed pre-existing by (a) the legacy flag default, (b) stack traces pointing at unmodified widgets / pre-existing fields, and (c) the full suite importing cleanly (no import breakage). A clean baseline could not be diffed because the repo is NOT under git. See [[project-nine-issue-fix-2026-06-01]].
