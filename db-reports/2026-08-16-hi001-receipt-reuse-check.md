# HIGH-001 receipt cross-user reuse check — prod `subscription_receipts`

**Date:** 2026-08-16
**Requested by:** backend-api (fixing HIGH-001 — receipt replay across Firebase accounts, no cross-user binding check on `POST /subscription_data` / `POST /one_time_purchase`)
**Access:** Heroku one-off dyno (`heroku run -a mindsync python < script.py`), read-only `SELECT` only, `SET statement_timeout = 15000` set first, no `commit()`. Two dynos ended up running (`run.7137`, `run.9114`) due to a retry after an initial output-buffering stall on the local end — both stopped after the query results were captured; only `run.7137`'s output was used (full session, ending in `DONE_SENTINEL`).

## 1. Schema — no drift from `app/models/models.py`

```sql
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'subscription_receipts'
ORDER BY ordinal_position;
```

| column | type | nullable |
|---|---|---|
| id | integer | NO |
| user_id | varchar | NO |
| platform | varchar | NO |
| product_sku | varchar | NO |
| base64_receipt | text | YES |
| purchase_token | text | YES |
| order_id | varchar | YES |
| purchase_time | bigint | YES |
| status | varchar | YES |
| created_at | timestamp | YES |

Matches `SubscriptionReceipt` in `MindSync/app/models/models.py:533-554` exactly. No orphaned/extra columns, no enum drift (all plain `String`/`Text`/`BigInteger`).

## 2. Apple stable identifier — not present anywhere in the schema

There is **no `original_transaction_id` column, and no dedicated Apple-transaction-identifier column of any kind.** The only Apple-side data is `base64_receipt` (`Text`, nullable) — this is the **raw base64 receipt blob the client sent**, not a parsed/decoded verification response, not JSON, not queryable. If `original_transaction_id` exists anywhere in prod today, it is only inside that opaque blob, unparsed.

**Practical consequence:** there is currently no column you can put a uniqueness constraint on for Apple. `order_id` doesn't help either — see §4. Any DB-level Apple dedup requires `backend-api` to add a new column (e.g. `apple_original_transaction_id`) populated going forward by decoding the App Store Server API / `verifyReceipt` response at verification time. Existing rows cannot be backfilled from `base64_receipt` without a decode step — flagging this as a follow-up for `backend-api` to scope separately; I did not attempt to decode any receipt blob (out of scope for a read-only DBA check, and decoding+displaying receipt contents would risk exposing PII-adjacent data).

## 3. Universe size — total rows by platform × status

```sql
SELECT platform, status, count(*) FROM subscription_receipts GROUP BY 1,2 ORDER BY 1,2;
```

| platform | status | count |
|---|---|---|
| apple | FAILED | 42 |
| apple | VERIFIED | 11 |
| google | FAILED | 20 |
| google | VERIFIED | 47 |

**Total: 120 rows** (42+11+20+47 = 120, matches today's earlier baseline report). No `PENDING` (the model default) or other status values present — every row in prod is terminal (`FAILED` or `VERIFIED`).

## 4. `order_id` fill-rate by platform — this is the load-bearing finding

```sql
SELECT platform,
       count(*) FILTER (WHERE order_id IS NULL OR order_id = '') AS null_or_empty,
       count(*) AS total
FROM subscription_receipts GROUP BY 1 ORDER BY 1;
```

| platform | null/empty order_id | total rows |
|---|---|---|
| apple | **53** | **53** |
| google | 26 | 67 |

**100% of Apple rows (53/53) have a NULL or empty `order_id`.** `order_id` is effectively an Android-only field in this table today — it is never populated for Apple receipts. For Google, 41/67 (67−26) rows have a usable `order_id`.

This directly bounds what a DB-level unique constraint on `(platform, order_id)` could ever catch: **it would be silent for Apple by construction**, no matter how clean the Google side is.

## 5. Cross-user reuse check — `status = 'VERIFIED'` only

```sql
SELECT platform, order_id, count(*) AS rows_cnt, count(DISTINCT user_id) AS distinct_users
FROM subscription_receipts
WHERE status = 'VERIFIED' AND order_id IS NOT NULL AND order_id <> ''
GROUP BY platform, order_id
HAVING count(DISTINCT user_id) > 1;
```

**Result: 0 rows returned.** Summary aggregate (`dup_pairs`, `rows_involved`, `user_instances`) = **0, 0, 0**.

Zero `(platform, order_id)` pairs among VERIFIED, comparable (non-null/non-empty) rows are shared across more than one `user_id`. This check only had 41 Google rows to look at (0 comparable Apple rows, per §4); of VERIFIED Google rows specifically it's a subset of those 41 with non-null order_id and status=VERIFIED — none collided.

## 6. Cross-user reuse check — all statuses (not just VERIFIED)

```sql
SELECT platform, order_id, count(*) AS rows_cnt, count(DISTINCT user_id) AS distinct_users
FROM subscription_receipts
WHERE order_id IS NOT NULL AND order_id <> ''
GROUP BY platform, order_id
HAVING count(DISTINCT user_id) > 1;
```

**Result: also 0 rows returned.** Aggregate = **0, 0, 0** — identical to the VERIFIED-only check. Widening to all statuses found no additional collisions, so this isn't a "verified rows happen to be clean but failed ones aren't" situation — there is no `order_id` reuse across users anywhere in the table, verified or not.

## Bottom line for the HIGH-001 decision

- **Google:** `order_id` reuse across different `user_id`s is **zero today, both in VERIFIED-only and all-status views** (0 of 41 comparable rows implicated). Clean enough that a DB-level unique constraint on `(platform, order_id)` — scoped to non-null/non-empty `order_id` (e.g. a partial unique index `WHERE order_id IS NOT NULL AND order_id <> ''`) — would not break on existing Google data. At only 120 rows total this is not a strong statistical guarantee (small n), but there is no observed violation to reason around.
- **Apple:** the check is **not informative** — `order_id` is 100% unpopulated for Apple (53/53 rows), and there is no other stable identifier (no `original_transaction_id` column; only an undecoded `base64_receipt` blob). A unique constraint on `order_id` provides **zero protection for Apple replay** as the table stands. Prod data being "clean" on the Apple side is not verified — it's simply unmeasurable with what's stored today.

**Recommendation to weigh, not a decision I'm making:** the service-layer check you're adding is necessary regardless (it's the only thing that currently covers Apple at all). For the DB-level unique constraint: safe to add for `(platform, order_id)` scoped to Google-only or to non-null/non-empty values (won't conflict with existing rows), but it will silently not protect Apple until a real stable Apple identifier column exists and is populated. That's a schema/logic change — naming **`backend-api`** as owner for both (a) adding an `apple_original_transaction_id`-style column populated from the App Store Server API / receipt-verification response going forward, and (b) deciding whether the partial unique index ships now (Google-only real coverage) or is deferred until the Apple identifier exists too, to avoid a constraint that looks like full coverage but isn't.

## Privacy note

No raw `user_id`, `order_id`, or receipt content was displayed at any point — every query above is a bounded aggregate (`COUNT`/`GROUP BY`/`HAVING`), and all collision checks returned zero rows so there was nothing to further redact.
