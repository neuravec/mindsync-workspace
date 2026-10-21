---
name: post-onboarding-offer-diagnosis-2026-10-03
description: Why post_onboarding_offer_not_shown said already_premium (not a fresh-account bug); Reset onboarding re-triggers the offer decision; debug builds pollute PostHog; paywall_load_failed error_type is useless
metadata:
  type: project
---

Read-only diagnosis (2026-10-03) of the WOW offer skip reasons (`WowCubit._offerSkipReason`).

Facts verified, non-obvious:
- A fresh account can NOT hit `already_premium`: sign-up (SignUpCubit, both email and OAuth) calls POST /users/subscription BEFORE onboarding, which writes `granted_via='signup_trial'`; the profile returns `subscription_is_active=true, premium_source='signup_trial', subscription_end_date='YYYY-MM-DDT00:00:00'` (proved offline through the response_model). `premiumSource == null` -> already_premium is deliberate (legacy paid rows) and changing it cannot make the offer appear: `signupTrialDaysLeft` requires `signup_trial`, so null would fall to `no_active_trial` anyway.
- Settings -> "Reset onboarding" is in RELEASE builds, has no analytics event, and after re-completing onboarding `completedInThisSession=true` -> the offer decision runs again for an old (possibly paid) account. Re-runs are indistinguishable from fresh ones except via `hours_since_signup` (Firebase creationTime) on `first_capture_prompt_shown`.
- Debug builds send every event to PostHog with `debug_mode=true`; filter it before counting.
- `paywall_load_failed.error_type` is always `_Exception` (runtimeType of `Exception(...)`); WOW fires it at preload with `trigger_feature=post_onboarding` even when the later skip reason is something else.
- WOW has no product-load retry; a failure or >4 s load = `products_unavailable`, and the offer is lost for good for that account.
- iOS StoreKit 1 observer starts on the first purchaseStream listen (plugin onListen), so WOW's product preload makes StoreKit redeliver unfinished transactions and verify them in background; backend rejects cross-account binding (`already_bound_to_other_account`).

**Why:** analyst suspected `premiumSource == null` treated as premium; that was refuted, cause is QA accounts re-running onboarding.
**How to apply:** for any "offer/paywall not shown" report, first split PostHog by debug_mode, $os, build, and check account age; in the rebuilt flow (paywall after Reflect voice session) re-read the profile right before deciding and retry products once.
