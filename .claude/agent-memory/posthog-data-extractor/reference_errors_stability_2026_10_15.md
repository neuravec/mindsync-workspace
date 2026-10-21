---
name: reference_errors_stability_2026_10_15
description: Error/stability baselines 2026-10-15 (30d/14d), error-event catalog incl. new 10-03 events, single-user loop traps, profile-404 = first-launch path
metadata:
  type: reference
---

Full extract: `analytics-reports/raw/2026-10-15-errors-stability.md`.

- Error-like events flowing (10-15): `api_error`, `client_error` (only prop `error_type`), `$exception` (use `$exception_types`, `$os_name`; no `$os`), plus `*_failed` family. New since 2026-10-03 (no earlier baseline): `auth_validation_failed` (reason = form validation, not a bug), `login_failed` (`reason`), `usage_load_failed`, `paywall_load_failed`. Defined in code but 0 events/30d: `subscription_restore_failed`, `onboarding_step_save_failed`, `onboarding_load_failed`, `backend_provisioning_failed`, `first_conversation_send_failed`, `error_occurred`.
- Reason keys differ per event: `error_type`, `failure_reason`, `reason`, `error_class`; coalesce via JSONExtractString. `password_reset_failed`, `onboarding_symptom_sync_failed` carry no reason.
- Single-user loops dominate counts: `subscription_verification_failed` (90% one person, `expired` loop on 10-03), `recording_processing_failed` (100%), `paywall_load_failed` (98%), `$exception` (81%). Always report persons.
- `api_error` 404 on `get_user_profile_and_subscription` (and `therapy-context`) is `is_expected=false` but is the first-launch "profile not created yet" path: 35/35 people were brand-new, within 30 min of first event. Exclude it when computing "real error" share.
- Baselines 14d: 165 app-active people; real-error share 21% excluding first-launch 404s (38% incl.); `$exception` 6%; client sessions with an error event 25% (124/492). `client_error` FirebaseAuthException is Android-only, mostly on `mainPage` (11 people/30d).
- Shared scratchpad is used by parallel agents: another agent overwrote my `ev.txt`. Use a unique subfolder per run.
