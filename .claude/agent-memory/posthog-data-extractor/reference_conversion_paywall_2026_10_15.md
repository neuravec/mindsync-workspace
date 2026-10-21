---
name: reference-conversion-paywall-2026-10-15
description: Paywall/purchase/trial event taxonomy as of 2026-10-15 (which side emits, double-emission of purchase_completed, Windows-backend test pollution, trial_ended only on conversion) plus 60d conversion baselines
metadata:
  type: reference
---

Verified 2026-10-15 (extract `analytics-reports/raw/2026-10-15-conversion-paywall.md`).

- `subscription_purchase_completed` is emitted by BOTH client (`posthog-flutter`, carries `trigger_feature`/`subscription_type`) and backend (`posthog-python`, `platform`/`product_sku`). Count buyers per person; client event = the purchase act. Backend includes 24h sandbox renewals (Apple `premium_m_01`).
- **Backend events with `$os=Windows`** (SKU `com.mindsync.premium`, ~186 purchase_completed / 3 persons, 08-19..10-14) = a local/test backend writing to prod PostHog. Exclude from purchase counts. Heroku backend shows `$os=Linux`.
- `trial_started` backend-only since 2026-10-03 09:22, 4-day `signup` trial. `trial_ended` fired only 2x, both `outcome=converted`: expiries without purchase are NOT emitted. Trial->paid must be computed as "purchase after trial_started".
- `subscription_product_selected.selection_source=default` = automatic yearly preselection; use `user` for intentional choice.
- Baselines 60d (08-16..10-15, testers excluded via heuristics in [[reference-post-onboarding-offer-and-test-accounts-2026-10-03]]): real buyers 6 (all monthly or starter, 0 yearly); paywall reach 5.8% pre-10-03 vs 14.9% post; trials 54 (33 Android / 21 iOS), conversions n<5, all Android; restore used only by testers; zero real-user `purchase_failed` after 10-03.
- iOS App Store build after 10-03 mostly 2.0.100 with ~0 paywall reach: check iOS version before reading iOS conversion.
