---
name: reference-release-2-0-117-2026-10-21
description: Store release 2.0.117 (redesign) identification, first real-user timestamps per OS, $app_build key, exception-signature method, release-day baselines 2026-10-21
metadata:
  type: reference
---

Verified 2026-10-21 (extract `analytics-reports/raw/2026-10-21-release-adoption-stability.md`).

- Store redesign build = `$app_version` 2.0.117: Android build 188 (first real store user 2026-10-20 02:12 UTC), iOS build 184 (`$is_testflight=false`, first real user 2026-10-21 07:49 UTC). 2.0.113-2.0.116 (10-19) were test builds only. Previous store: 2.0.110 (Android 181, iOS 177).
- Build number key is `$app_build` (there is no `$build`). iOS and Android build numbers are independent.
- How to identify a store build: iOS = first version with `$is_testflight=false` on all events; Android = version on which every new install (first event per person) lands from date X.
- `$exception_values` comes back `<redacted>`; describe signatures with `$exception_types` + `$exception_functions` + `$screen_name` + `$exception_fingerprint`.
- All `$exception` on 2.0.113-2.0.117 came from the OnePlus8Pro automation person (Play pre-launch). Real users on 2.0.117: 0 exceptions (n=7 on 10-21). Recurring bot-only signature: ProviderNotFoundException in `ErrorView.build` on subscription screen since 2026-09-02.
- New Main polls `/health-check/latest` (404, expected) ~52x per person per 7d vs ~5x on 2.0.110.
- `follow_up_failed` first fired ever 2026-10-21 (status_class not_found, iOS, 1 new user).
- Baselines: clean app DAU 22-25 early Oct -> 7-11 on 10-19..10-21 (decline predates release). ~40% of backend `user_registered` persons never emit a flutter event (stable weekly since 09-27, not a release regression).
- Native crashes are invisible in PostHog (`posthog-flutter` captures Dart only); point to Play Console vitals / App Store Connect.

**How to apply:** re-run adoption on 10-23+ with the same clean filters; anchor "after" to the per-OS first-real-user timestamps above.
