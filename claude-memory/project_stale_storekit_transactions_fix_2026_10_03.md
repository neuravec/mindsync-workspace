---
name: project-stale-storekit-transactions-fix-2026-10-03
description: Monthly purchase blocked on iOS by never-finished expired StoreKit transactions; fix with fail_reason+retryable and a client finish gate; round 2 PUSHED BE main 513d690 + FE dev dc45f26
metadata:
  node_type: memory
  type: project
  originSessionId: d253df82-302d-4280-885b-a03d87e54631
  modified: 2026-10-03T09:44:28.591Z
---

Symptom (2026-10-03, operator's TestFlight account): "Continue with monthly" gave "Something went wrong", annual worked. PostHog showed `subscription_purchase_failed store_error` ~1s after tap (Apple sheet never opened) plus dozens of `subscription_verification_failed expired` for old `premium_m_01` transactions.

Root cause: client never called completePurchase() on a non-VERIFIED backend answer, so expired transactions were redelivered forever and StoreKit 1 refuses to buy a product with an unfinished transaction. Manually editing user_subscription in the DB does nothing on Apple's side. The same scenario hits real users who let a sub lapse and try to resubscribe.

Fix: backend `/subscription_data` and `/one_time_purchase` return `fail_reason` + `retryable` (app/services/receipt_verification_outcome.py). retryable=false ONLY for terminal states: expired, already_bound_to_other_account, google_state_1, apple_status_21006/21008/21010. Client gate `shouldFinishDeadTransaction` (lib/managers/purchase_failure_reason.dart): Android finishes only expired/google_state_1 (acknowledging cancels Google's 3-day auto-refund); iOS user-initiated only expired/google_state_1; iOS background any retryable=false.

**Why:** security-guardian H-1 blocked the first version: finishing on reasons like 21002/missing_receipt could close a just-paid purchase without premium.

**How to apply:** any new fail_reason must be classified there (default = retryable). Open follow-ups: device-QA on operator's account after TestFlight build; M-1 specific message for already_bound_to_other_account; L-1 rate limit on receipt endpoints; drop pre-buy restorePurchases() in purchases_data_provider.dart; "nothing to restore" UX; subscription_verification_failed emitted on both BE and FE; posthog-data-extractor to confirm subscription_purchase_pending and subscription_stale_transaction_finished flow.

Round 2 (same day, after device test): the first diagnosis was incomplete. Real root causes:
- iOS monthly: `purchases_data_provider.dart` called restorePurchases() before every buy; restored transactions sit unfinished on the queue and StoreKit 1 answers `storekit_duplicate_product_object`. Pre-buy restore removed (FE dc45f26). Finishing stale transactions alone could never fix it.
- Android "no premium after purchase": `is_user_premium` compared DATE end_date with NOW(), so access ended at 00:00 UTC of the expiry day; Google Play 5-minute test subs were never premium, real users lost the last day. Now the expiry day counts as paid, except signup_trial (keeps trial_ends_at contract). Profile `subscription_is_active` now equals is_user_premium (BE 513d690, no migration).
- Reflect cached isPremium from startup (route snapshot + singleton cubit): added ReflectChatCubit.refreshUsage(), called from MainPageCubit.refreshSubscriptionInfo.
- Restore with nothing to restore was silent: `onNothingRestored` callback + event `subscription_restore_empty`.
- Drawer "?" = empty full_name; now person icon + Account label. Why the operator's profile name is empty was NOT checked in prod.

**Why:** PostHog error code (`error_message` on subscription_purchase_failed) was the evidence that exposed the real cause; read it first next time.
Full BE suite was NOT run for 513d690 (background run killed for low memory); 1448 tests in the 33 files touching the gate/profile passed.
