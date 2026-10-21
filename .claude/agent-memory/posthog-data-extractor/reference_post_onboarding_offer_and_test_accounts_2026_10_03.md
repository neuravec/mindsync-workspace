---
name: reference-post-onboarding-offer-and-test-accounts-2026-10-03
description: How the 2026-10-02 post-onboarding offer is measured (no offer_shown event; paywall_shown trigger_feature=post_onboarding), which builds carry it (2.0.97+), and how to tell internal testers / Play automation accounts apart from real users on fresh TestFlight/internal builds
metadata:
  type: reference
---

Verified 2026-10-03 (extract: `analytics-reports/raw/2026-10-03-post-onboarding-offer-check.md`).

**Offer measurement (subscription redesign, FE commit 02f8d0b):**
- There is NO `post_onboarding_offer_shown` event. "Offer on screen" = `paywall_shown` with `properties.trigger_feature = 'post_onboarding'` (deferred until `revealPaywall()`).
- Skip = `post_onboarding_offer_not_shown`, prop `reason` in {not_just_onboarded, status_unavailable, already_premium, no_active_trial, already_seen, products_unavailable}. Client logic: `already_premium` = active sub AND `premium_source` in {null, purchase, starter_pack}; a fresh `signup_trial` account should NOT hit it.
- `post_onboarding_offer_option_selected` / `post_onboarding_offer_result` had never fired as of 2026-10-03 (absent from event_definitions).
- `paywall_load_failed.error_type` = Dart runtimeType (`_Exception`), no store error code. It also carries a `user_id` property (Firebase UID): never select it.
- Backend `trial_started` first fired 2026-10-03 09:22 UTC (deploy f5ea34d).

**Build mapping:** new onboarding flow = `$app_version` 2.0.97+ (iOS build 164+, Android 168+, first event 2026-10-03 07:39 UTC). 2.0.96 predates the commit. Method that worked: `git log` of `mindsync-frontend` dev, the "Pre-release updates" commits are Codemagic version bumps; first bump after the feature commit = first build carrying it.

**Who is on fresh internal builds (classification heuristics, no IDs stored):**
- Internal testers: 30+ distinct `$app_version` lifetime, repeated `onboarding_completed` (5-6x), several `subscription_purchase_completed`. On Android this is the only tester signal (no `$is_testflight`).
- One mega-merged automation person: 411 distinct_ids, 67 versions, OnePlus8Pro + emulator events, never onboards; emits all `paywall_load_failed` (no Play billing on the device farm). Likely shared "App access" login of Play pre-launch robots. Exclude from any user count.
- New OnePlus8Pro persons appear on every new Android build within hours (pre-launch bots); some walk 10+ onboarding steps without completing. Already covered by [[default-exclusion-filters]].
- iOS events with `$is_testflight = false` on a not-yet-public version = probably a developer Xcode build.

**How to apply:** for any "does feature X show to users" question right after a release, first list persons per new `$app_version` and classify them with the heuristics above; on 2026-10-03 the answer was 0 real users on the new builds, so the verdict was "insufficient data", not "bug".
