---
name: reference-acquisition-cube-2026-10-15
description: Canonical "new user" definition + one-query acquisition cube (week x os x country x locale x install_source x lead x funnel/retention flags) and 60d acquisition baselines as of 2026-10-15
metadata:
  type: reference
---

Canonical new user = person_id whose FIRST `posthog-flutter` event since 2026-04-22 falls in the window; exclude person-level bots (`$device_model` OnePlus8Pro/Pixel 6 Pro) and testers (`$is_testflight`/`$is_emulator`). Not `user_registered` (backend; 26% of registrations have no app events under the same person_id = identity not merged). Not `app_install_attributed` (fires on upgrades/reinstalls).

**Pattern that beats the 10 s server limit and the 12-query budget:** ONE per-person subquery (argMinIf for os/cc/locale/install_source, argMaxIf for survey `source_value`, countIf flags, `groupUniqArrayIf(toDate(timestamp), lib flutter)` + `arrayExists(x -> x >= fd+1 AND x <= fd+7, ds)` for retention), grouped by all dims, `--format csv --out` to scratchpad, then slice locally in Python. ~260 rows for 60d, ran well under 10 s. Query verbatim in `analytics-reports/raw/2026-10-15-acquisition.md`.

Facts verified 2026-10-15: `$locale` and `$geoip_country_code` on 100% of flutter events; `$device_language` does not exist. `onboarding_lead_source_selected.source_value` enum: app_store, friend, therapist, other, social_media, blog.

Baselines (2026-08-16..10-15): 296 clean new (avg ~35/wk), 94 started onboarding, 71 completed (24%); R7 18%, R14 10%. Spike 09-21..10-05 (47/78/60 per wk) mostly Android fr/ar/fa from West Africa/Middle East, completion 5-11%. iOS 46% completion / R14 33% vs Android 22% / 8%. 81% of new have `install_source='google-play'` (uninformative). `install_source='blog'` still 0; web PostHog 8-22 visitors/wk.

**How to apply:** reuse the cube for any acquisition/cohort-quality question; compare new numbers to these baselines. See [[reference-blog-attribution-2026-10-07]], [[default-exclusion-filters]].
