---
name: stale-storekit-transactions-2026-10-03
description: Dead (expired) StoreKit transactions blocked monthly repurchase; fixed by finishing on backend retryable=false; key non-obvious facts about the purchase flow
metadata:
  type: project
---

Commits 6499692 + 354cb23 (security H-1/L-2 gate) on mindsync-frontend dev (local, NOT pushed as of 2026-10-03). Backend adds `fail_reason` + `retryable` to /subscription_data and /one_time_purchase (classifier in MindSync `app/services/receipt_verification_outcome.py`).

Non-obvious facts:
- Receipt responses are raw `Map<String, dynamic>`, no Freezed response model; parsing lives in `ensureReceiptVerified` (subscription_repository.dart).
- `PurchasesRemoteDatasource.purchaseNonConsumableProduct` calls `restorePurchases()` BEFORE every iOS buy, so each tap floods the stream with `restored` transactions. Left as-is; candidate to remove.
- "User-initiated" = FIRST `purchased` transaction for the tapped product after the tap, timestamp ignored (security L-2, clock skew); active product cleared right after handling it.
- Finish gate `shouldFinishDeadTransaction` (purchase_failure_reason.dart, security H-1): needs explicit `retryable == false`; Android and iOS user-initiated only for {expired, google_state_1} (Android ack kills Google's 3-day auto-refund); iOS background any definitive reason. `isGooglePlayStore` is a reassignable test seam (not @visibleForTesting: that annotation warns on lib callers).
- Do not run `dart format` on these cubits: the repo is not formatter-clean, it reflows whole files.
- Restore of only dead transactions now gives no inline feedback (silent): UX follow-up.
- Backend also fires its own `subscription_verification_failed`; client fires one too (pre-existing double emission).

**Why:** StoreKit 1 refuses a new purchase while an unfinished transaction for that product exists.
**How to apply:** any purchase-stream change must keep background redeliveries silent and never finish without a definitive backend answer.
