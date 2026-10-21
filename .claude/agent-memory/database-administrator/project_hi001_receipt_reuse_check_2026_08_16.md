---
name: hi001-receipt-reuse-check-2026-08-16
description: subscription_receipts cross-user order_id reuse check for HIGH-001 (receipt replay) — Google clean, Apple unmeasurable
metadata:
  type: project
---

For backend-api's HIGH-001 fix (receipt replay across Firebase accounts, no cross-user binding check on `POST /subscription_data`/`POST /one_time_purchase`), checked prod `subscription_receipts` (120 rows total: apple FAILED 42/VERIFIED 11, google FAILED 20/VERIFIED 47) for existing `(platform, order_id)` reuse across different `user_id`s.

**Result: zero collisions found**, both `status='VERIFIED'`-only and all-statuses. But this is only a real signal for Google — **100% of Apple rows (53/53) have NULL/empty `order_id`**; it's effectively an Android-only field in this table. Schema has no Apple stable identifier at all: no `original_transaction_id` column, only an undecoded `base64_receipt` (raw base64 blob, not JSON, not parsed).

**Why:** determines whether a DB-level unique constraint on `(platform, order_id)` is safe to add alongside the service-layer check. Full report: `db-reports/2026-08-16-hi001-receipt-reuse-check.md`.

**How to apply:** if backend-api asks again whether Apple receipt data has a stable dedup key in prod — it doesn't, as of 2026-08-16. They'd need to add a new column populated from App Store Server API / verifyReceipt response going forward; existing `base64_receipt` blobs aren't queryable without a decode step (which I did not do — decoding+displaying receipt content risks exposing PII-adjacent data, out of scope for a read-only check anyway). A unique constraint on `order_id` alone would give real coverage for Google only and silently zero coverage for Apple.

Related: [[reference_database_administrator_agent]] for the access recipe; [[feedback_heroku_run_local_stdout_buffering]] for a new gotcha hit while running this check.
