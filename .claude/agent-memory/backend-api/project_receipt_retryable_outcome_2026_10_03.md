---
name: project-receipt-retryable-outcome-2026-10-03
description: Receipt endpoints return fail_reason + retryable so Flutter can finish dead StoreKit transactions; retryable=false ONLY for terminal transaction states (security H-1)
metadata:
  type: project
---

2026-10-03, commits `c7a5a01` -> `f4d5cef` -> `2732275` on MindSync main, NOT pushed. POST /users/subscription_data and /users/one_time_purchase gained additive `fail_reason` (null on VERIFIED) and `retryable` (false on VERIFIED). Mapping in dependency-free `app/services/receipt_verification_outcome.py`.

Final rule: retryable=false ONLY for expired, already_bound_to_other_account, google_state_1, apple_status_21006/21008/21010. Everything else (incl. 21002, 21003, 21004, missing_receipt, no_latest_info, product_not_in_receipt, no_* field-missing reasons, unsupported_product, unknown) is retryable.

**Why:** the client finishes the transaction on retryable=false, and on Android that also acknowledges it (cancels Google's 3-day auto-refund). My first mapping marked "missing data" reasons definitive; security review H-1 showed they occur on genuine just-paid transactions (stale local iOS receipt on first purchase, client/API defects, our config for 21004, Apple documents 21002 as possibly transient) and would charge users with no premium. Also (L-3): Apple subscription `expired` reads the NEWEST latest_receipt_info entry, so it means "this Apple ID has no active subscription", not a per-transaction verdict.

**How to apply:** default any new or ambiguous verifier fail reason to retryable; only add to the definitive set when the reason describes the transaction's own terminal state. Flutter reads these responses as raw `Map<String, dynamic>` (users_manager.dart / subscription_repository.dart), so adding keys is non-breaking.
