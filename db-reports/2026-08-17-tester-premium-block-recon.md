# Tester "already has premium" block — recon (2026-08-17)

**Urgency:** production, live purchase blocked. **Scope of this pass:** read-only recon (SELECT only) + a proposed narrow fix. **No DML executed.**

## Question

Tester `[e-mail testera A]` on Android gets "can't buy — you already have premium" when attempting a real purchase. Find the real account state and the exact row/column causing the block, then propose (not run) a fix.

## Account found

Only **one** account exists under this email — no second/old account, no cross-account situation:

| id (Firebase UID) | email | created_at | last_login | activated_at |
|---|---|---|---|---|
| `<UID-3>` | [e-mail testera A] | 2026-08-17 16:31:37 | NULL | NULL |

Registered today, ~1-2 hours before this recon. `activated_at` NULL = hasn't fired a qualifying therapy-loop event yet (unrelated to billing).

## Direct answer: which row/column makes the backend think he has premium

`user_subscription`, single row:

| id | user_id | subscription_type | start_date | end_date | is_active |
|---|---|---|---|---|---|
| 31285 | <UID-3> | PREMIUM | 2026-08-17 | **2026-08-21** | **True** |

`end_date - start_date = 4 days`. This is not a receipt-backed purchase and not a promo code — it is the **automatic signup free trial**, created by `_create_initial_subscription(db, user_id, 4, mark_had_trial=False)` in `MindSync/app/api/v1/endpoints/users.py:111-164`, called from `POST /users/subscription` (`MindSync/app/api/v1/endpoints/users.py:402-426`), which the client calls once after registration/device-type submission. It unconditionally grants 4 days of `subscription_type=PREMIUM, is_active=True` to any brand-new user, iOS or Android, with **no receipt, no promo code, and no store transaction of any kind**. This is confirmed as the intended, standard trial mechanism (per operator), not a data bug — the bug is what happens next.

Corroborating query (`subscription_receipts` for this user_id): **0 rows**. He has never even reached the purchase-verification endpoints (`POST /subscription_data` / `POST /one_time_purchase`) — the block is happening *before* any receipt hits our backend. `user_promo_code`: 0 rows. `user_profile.has_used_promo_code = False`. This rules out both a promo code and a receipt-based cause for this specific case.

## Question 2 (operator): is there ANY schema-level distinction between trial / promo / paid?

**No.** `user_subscription` (live prod columns, `information_schema`):

```
id integer, user_id varchar, subscription_type USER-DEFINED (enum: BASIC|PREMIUM), start_date date, end_date date, is_active boolean
```

That's it — no `source`, `plan_type`, `product_id`, `is_trial`, or FK to a receipt/promo row. `subscription_type` only encodes the *tier* (basic vs premium), never the *origin*.

The one column that looks like it should carry this signal — `user_subscription_trial.had_trial` — **does not apply to this grant**. For this user that row exists (`id=17887`) but `had_trial=False`, `trial_started_at=NULL`. Reading the code confirms why: `had_trial` is reserved for an *Apple/Google in-app-purchase* trial offer (set from `is_trial`/`paymentState==2` in `_verify_apple_receipt`/`_verify_google_receipt`, `MindSync/app/services/subscription_service.py`), a completely different concept from this internal 4-day signup grace period. The signup grant is created with `mark_had_trial=False` and never touches this table's boolean. So there is genuinely **no queryable way to tell "premium from the free signup trial" apart from "premium from a real purchase"** other than the indirect join I used below (does a VERIFIED receipt exist for this user_id).

The canonical premium gate in code, `is_user_premium()` (`MindSync/app/api/v1/endpoints/_therapy_helpers.py:28-51`), is exactly `is_active == True AND (end_date IS NULL OR end_date > NOW())` — it cannot see "why" `is_active` is true. Whatever downstream check produces the "you already have premium, can't buy" message (client-side paywall gate reading subscription status, most likely — I did not find a purchase-time rejection in `POST /subscription_data`/`POST /one_time_purchase`, and Flutter's paywall UI is `flutter-mobile`'s code, not mine to trace further) is reading this same undifferentiated flag.

## Question 3 (operator): scale — how many users are in this state right now

Bounded aggregates over `user_subscription` × `subscription_receipts`, prod-wide:

| Metric | Count |
|---|---|
| Active premium **with no VERIFIED receipt at all** ("trial-like", same shape as the tester) | **8** |
| ...of which registered in the last 30 days | **6** |
| Active premium **backed by a VERIFIED receipt** (genuinely paid, still in period) | 5 |
| Active premium, total | 13 |
| Users registered in the last 30 days (all, any tier) | 65 |
| Users, total | 1,817 |

Read: right now, **8 of the 13 people the system currently calls "premium" (62%) have paid nothing and hold no receipt** — they are inside the 4-day signup grace window (or, in principle, someone manually flipped `is_active` with no receipt, but the shape matches the trial exactly). Every one of those 8 people would hit the identical "already have premium, can't buy" wall if they tried to purchase right now, for as long as they're inside their trial window. This is small in absolute terms today (8 people) but it is structural, not a one-off: it reproduces for every new signup, every time, for the first 4 days after registration — a monetization-blocking bug on the newest, highest-intent cohort, not a one-user data anomaly.

## Question 4 (operator, downgraded to secondary): cross-account replay (HIGH-001)

Checked and **ruled out** for this case — there is nothing to replay:
- Only one account exists under this email (see above).
- `subscription_receipts` has 0 rows for this user_id → 0 `platform_transaction_id` values → cross-account match query against all other users returns 0 rows.
- Full-value match on `purchase_token` and on `order_id` against every other user in the table: 0 rows.

HIGH-001's guard (`find_cross_account_receipt`, deployed 2026-08-16, memory: `db-reports/2026-08-16-hi001-receipt-reuse-check.md`) is not implicated — it only ever runs after a receipt is submitted and platform-verified, and this user has never submitted one.

## Proposed fix — NOT executed, needs operator sign-off

Scope: exactly one row, keyed by `user_id` (not email). Single column changed.

```sql
-- BEFORE — confirm current state
SELECT id, user_id, subscription_type, start_date, end_date, is_active
FROM user_subscription
WHERE user_id = '<UID-3>';
-- expected: id=31285 | subscription_type=PREMIUM | start_date=2026-08-17 | end_date=2026-08-21 | is_active=True

BEGIN;

UPDATE user_subscription
SET is_active = false
WHERE user_id = '<UID-3>';
-- expect: UPDATE 1

-- AFTER — verify before committing
SELECT id, user_id, subscription_type, start_date, end_date, is_active
FROM user_subscription
WHERE user_id = '<UID-3>';
-- expected: is_active=False, every other column unchanged

COMMIT;   -- only if AFTER matches; otherwise ROLLBACK
```

**What this does and does not do:**
- Flips `is_active` true→false on `user_subscription.id=31285` only. `subscription_type` stays `PREMIUM`, `start_date`/`end_date` stay `2026-08-17`/`2026-08-21` — the row is preserved as an audit trail of "this person had a signup trial," it is not deleted.
- Satisfies `is_user_premium()`'s AND-check immediately (`is_active == True` becomes false, so the whole condition is false regardless of `end_date`), so any code path reading that function — and, if the client reads `is_active` directly, that path too — will now report "not premium."
- **This is not a manual invention** — it is byte-for-byte what MindSync's own hourly `deactivate_expired_subscriptions` job (`MindSync/app/services/subscription_service.py:51+`) will do to this exact row automatically on **2026-08-21**, once `end_date` passes. This SQL just does it 4 days early, for this one user, on request.
- Does not touch `subscription_receipts` (he has none), `user_promo_code` (he has none), or any other user's row.
- No unique constraint or other row anywhere is affected — `ids_sql`/`WHERE` is scoped to this single `user_id` throughout.

After this runs, the tester should be able to open the purchase flow and complete a real purchase; `POST /subscription_data` / `POST /one_time_purchase` will create a fresh `subscription_receipts` row and, on verified success, call `_activate_user_subscription` to re-set `is_active=True` with the real store-backed expiry — this time indistinguishable at the DB level from every other trial-derived row, which is exactly the systemic gap below.

## Handoff — systemic bug, not just this tester (`backend-api` + `flutter-mobile`)

1. **Root cause to fix, not just patch:** `user_subscription` has no source/origin signal. `backend-api` should add a way to tell "signup trial" apart from "real subscription" — cheapest: a nullable `source` (or `granted_via`) column (`'signup_trial' | 'purchase' | 'promo'`), populated by `_create_initial_subscription` and by the purchase/promo activation paths. `user_subscription_trial.had_trial` is not that column — it's IAP-trial-specific and already means something else; overloading it would break B12's `trial_started`/`trial_ended` PostHog instrumentation.
2. **The actual UI/logic block ("already have premium, can't buy") needs to be traced and fixed at the source**, not just patched per-user in the DB: find where the "already has premium" purchase-block decision is made (most likely `flutter-mobile`'s paywall reading `GET /users/subscription`'s raw `is_active`, but confirm — I did not find a purchase-time rejection in the backend verification endpoints) and make it allow "upgrade/convert from trial" rather than treating a still-active signup trial as "already subscribed, nothing to sell." This is what's actively blocking revenue from every new user during their first 4 days.
3. **Scale to track:** re-run the OP2/OP3/OP4 aggregate queries above periodically — 8 trial-only-premium / 13 active-premium today is the baseline to compare against after a fix ships.

## Queries run (all SELECT, via `heroku run -a mindsync python`, run.2816, stopped after capture)

`information_schema` recon on `users`, `user_subscription`, `subscription_receipts`, `user_subscription_trial`, `promo_code`, `user_promo_code`, plus a search for any promo/trial/voucher/redeem/grant-named table (found only the three listed above — no other candidate table exists) and every column named `%email%` in the schema (`users.email`, `clinicians.email`, `clinician_invites.patient_email` — confirms `email` lives only on `users` for regular accounts, not `user_profile`). Then per-user_id lookups across `user_profile`, `user_subscription`, `user_subscription_trial`, `subscription_receipts` (token truncated to 12 chars, never logged in full), `user_promo_code`⋈`promo_code`, and three cross-account match queries (`platform_transaction_id`, full `purchase_token`, full `order_id` — none displayed, only user_id/status/receipt_id on match). No token, receipt content, or other PII beyond the operator-supplied email and the resulting Firebase UID appears in this report.
