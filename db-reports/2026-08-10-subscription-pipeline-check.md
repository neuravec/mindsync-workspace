# Subscription / purchase pipeline check - 2026-08-10

## Question

Has there been ANY completed purchase / verified receipt since 2026-07-22, or did the purchase/verification pipeline break?

Trigger: PostHog (last 14d, project 141170) funnel `subscription_screen_opened` 25/11 users -> `subscription_product_selected` 5/4 -> `subscription_purchase_started` 2/2 -> `subscription_purchase_failed` 1/1 -> `subscription_purchase_completed` **0**. PostHog cannot tell "no transactions" from "backend stopped emitting/verifying" - the DB is ground truth.

## Method

Access: `heroku run -a mindsync python < script.py` (Azure Postgres has no public DNS from local/dev; this is the only path). REPL-safe script, read-only `SELECT` + `db.rollback()` after every block (no writes, no `commit()`). Dyno `run.5048`, stopped after capture via `heroku ps:stop run.5048 -a mindsync`. Columns verified against live `information_schema.columns` first (not just `models.py`) - no drift found on these six tables.

## Exact queries run

```sql
-- schema check
SELECT table_name, column_name, data_type, is_nullable FROM information_schema.columns
WHERE table_name IN ('subscription_receipts','user_subscription','user_subscription_trial',
                      'promo_code','user_promo_code','token_usage_log')
ORDER BY table_name, ordinal_position;

-- subscription_receipts
SELECT count(*) AS total, max(created_at), min(created_at) FROM subscription_receipts;
SELECT date_trunc('week', created_at)::date AS wk, platform, status, count(*)
FROM subscription_receipts WHERE created_at >= '2026-07-01' GROUP BY 1,2,3 ORDER BY 1,2,3;
SELECT count(*) FILTER (WHERE created_at >= '2026-07-22') AS since_0722,
       count(*) FILTER (WHERE created_at >= '2026-07-27') AS since_0727
FROM subscription_receipts;
SELECT status, count(*) FROM subscription_receipts GROUP BY 1 ORDER BY 2 DESC;

-- user_subscription
SELECT count(*) AS total, count(*) FILTER (WHERE is_active) AS active_flag_true,
       count(*) FILTER (WHERE is_active AND end_date > now()) AS active_and_not_expired,
       count(*) FILTER (WHERE end_date >= '2026-07-22') AS end_date_since_0722,
       count(*) FILTER (WHERE start_date >= '2026-07-22') AS start_date_since_0722,
       count(DISTINCT user_id) AS distinct_ever
FROM user_subscription;
SELECT subscription_type, is_active, count(*) FROM user_subscription GROUP BY 1,2 ORDER BY 1,2;
SELECT count(*) FROM user_subscription WHERE end_date >= now() - interval '30 days' AND end_date <= now();

-- user_subscription_trial
SELECT count(*) AS total, count(*) FILTER (WHERE had_trial) AS had_trial_true FROM user_subscription_trial;

-- promo codes
SELECT count(*) AS total, max(used_at) FROM user_promo_code;
SELECT date_trunc('week', used_at)::date AS wk, count(*) FROM user_promo_code
WHERE used_at >= '2026-07-01' GROUP BY 1 ORDER BY 1;

-- token usage (AI cost proxy)
SELECT count(*) FILTER (WHERE created_at >= now() - interval '14 days') AS last_14d,
       count(*) FILTER (WHERE created_at >= now() - interval '28 days' AND created_at < now() - interval '14 days') AS prior_14d,
       sum(cost_usd) FILTER (WHERE created_at >= now() - interval '14 days') AS cost_last_14d,
       sum(cost_usd) FILTER (WHERE created_at >= now() - interval '28 days' AND created_at < now() - interval '14 days') AS cost_prior_14d
FROM token_usage_log;
```

## Results

**subscription_receipts** (all-time and windowed)

| metric | value |
|---|---|
| total rows (all-time) | 119 |
| first created_at | 2025-03-17 14:31:50 |
| **last created_at** | **2026-07-10 23:26:05** |
| rows since 2026-07-22 | **0** |
| rows since 2026-07-27 | **0** |
| status all-time | FAILED=62, VERIFIED=57 (0 stuck PENDING) |

Weekly breakdown since 2026-07-01 - only one non-empty week:

| week (Mon) | platform | status | count |
|---|---|---|---|
| 2026-07-06 | google | VERIFIED | 2 |

Every other week from 07-13 through 08-10 (today) has **zero** rows.

**user_subscription**

| metric | value |
|---|---|
| total rows | 1,796 (= distinct users ever, 1:1) |
| is_active=True | 34 (all PREMIUM) |
| is_active=True AND end_date > now() | 16 |
| end_date >= 2026-07-22 | 54 |
| start_date >= 2026-07-22 | 41 |
| subscription_type x is_active | BASIC/False=649, PREMIUM/False=1113, PREMIUM/True=34 |
| end_date in last 30d (expired/expiring) | 55 |

**user_subscription_trial**: 1,796 rows (1:1 with users), 554 with `had_trial=True`.

**user_promo_code**: 22 redemptions all-time, last `used_at` 2026-07-16 22:46:30. Since 2026-07-01: exactly 1 redemption (week of 07-13). None since.

**token_usage_log** (AI cost, engagement proxy): last 14d = 55,567 rows / $49.56 vs prior 14d = 69,059 rows / $59.66 - roughly a 20% decline, consistent with the broader traffic dip PostHog shows (25 users saw the subscription screen in 14d), not a payment-specific collapse.

## Code cross-check (why the DB numbers can be trusted as "endpoint not called", not "endpoint failed silently")

Read `app/api/v1/endpoints/users.py` (`POST /subscription_data`, ~line 408-509): the handler does, in this exact order, on every invocation:

1. `db.add(new_receipt); db.commit()` with `status="PENDING"` (row exists, guaranteed, before anything else happens)
2. fires `subscription_receipt_received`
3. verifies synchronously, sets `status` to `VERIFIED` or `FAILED`, `db.commit()`
4. fires `subscription_purchase_completed` or `subscription_verification_failed`

So a `subscription_receipts` row is written and committed *before* `subscription_receipt_received` is even captured - there is no code path that fires that PostHog event without first persisting a DB row. Grepping the whole backend, `subscription_purchase_started` and `subscription_purchase_failed` do **not** appear anywhere server-side - they only exist client-side (Flutter, around the native Apple/Google purchase dialog), fired before our backend is ever called.

The `user_subscription.start_date >= 2026-07-22` (41 rows) finding looked at first like contradicting "zero receipts" - it doesn't: `_create_initial_subscription` (`users.py` ~line 89) creates a `user_subscription` row **at registration** for every new user (trial PREMIUM or BASIC with `is_active=False`), independent of any purchase. `_activate_user_subscription` (the only function that touches `end_date`/real activation) is called from exactly one place: the receipt-verification success path above. So the 41 rows are new-user signups getting their default trial/basic row, not evidence of purchase activity.

## Interpretation / verdict

**This reads as a genuine top-of-funnel purchase-conversion problem, not a broken backend verification or persistence pipeline.**

- The last purchase attempt that ever reached our backend and was processed was **2026-07-10** (part of 2 Google receipts in the week of 07-06, both `VERIFIED`). Nothing has hit `POST /subscription_data` since - not a failure, not a retry, not a stuck `PENDING` row, nothing. Zero rows of any status since 07-10.
- The receipt-write code path is proven reliable when it runs: its own history contains both `FAILED` (62) and `VERIFIED` (57) outcomes normally, and there are zero orphaned `PENDING` rows anywhere. If the endpoint were being called and erroring, we would expect to see new `FAILED` rows, not silence. We see silence -> the endpoint is not being invoked.
- This matches the client-side funnel: 2 users tapped "subscribe" in the last 14 days, 1 hit `subscription_purchase_failed` (a platform-level Apple/Google outcome that fires *before* our backend), and 0 ever produced a `subscription_receipts` row. The purchase attempts are dying between the native store dialog and our API - i.e. before backend code is reachable at all - or there simply were none that reached a real purchase attempt.
- Given only 25 users opened the subscription screen and 2 started a purchase in 14 days, the more likely explanation is simply **very low volume**, not instrumentation failure: 2 attempts is too small a sample to expect a completion, and the DB shows no sign the backend would have mishandled one had it arrived.

**One unresolved discrepancy, flagged rather than resolved here:** the growth-analyst brief that triggered this check stated PostHog's last-ever `subscription_receipt_received` and `subscription_purchase_completed` events were seen on **2026-07-22**. Given the code guarantees a `subscription_receipts` row is committed in the same request, in the same code path, immediately before that exact event fires, a real 07-22 firing should have produced a DB row - and there is none after 07-10 (a 12-day gap). This cannot be resolved from Postgres alone. Two explanations are possible: (a) the "last seen" PostHog date in the brief was approximate/stale rather than a precise last-occurrence timestamp, or (b) there is a genuine persistence anomaly. (a) is far more likely given the code path leaves no room for step 2 to fire without step 1 having committed - but this needs an exact-timestamp re-check against PostHog to close out with certainty. By contrast, `promo_code_applied`'s PostHog last-seen date (07-21) is a close 5-day match to the DB's last `user_promo_code.used_at` (07-16), which is within normal noise - only the receipts event shows the large gap.

**Secondary finding (not core to this question, flagging for backend-api):** 18 of the 34 `user_subscription` rows with `is_active=True` have `end_date <= now()` (i.e., expired but still flagged active). CLAUDE.md documents an hourly job to "deactivate expired subscriptions" (`app/tasks/subscriptions.py`, backend-api-owned) - worth a quick check that this job is actually running/scheduled, since 18 stale-active rows suggest it may be lagging or not running. Not investigated further here since it's outside this question's scope.

## Handoffs

- **growth-analyst**: verdict is "near-zero real purchase attempts in the last month" (2 receipts since 07-01, both 07-06/07-10, both Google/VERIFIED; nothing since), not a backend outage. This is a conversion/volume problem worth a funnel deep-dive (why do 25 subscription-screen views produce only 2 purchase attempts, and why does even 1-of-2 fail before reaching our backend) - growth-analyst + posthog-data-extractor territory, cross-referencing exact event timestamps against the DB numbers above.
- **backend-api**: no evidence of a broken verification/persistence pipeline - do not spend time on `/subscription_data` itself. Do please sanity-check the hourly "deactivate expired subscriptions" job given the 18 stale-active `user_subscription` rows noted above.
- **flutter-mobile / instrumentation**: worth checking whether the client reliably calls `POST /subscription_data` after every successful native purchase (StoreKit/Play Billing), since 1 of 2 `subscription_purchase_started` events resulted in a client-side `subscription_purchase_failed` and neither produced a backend receipt row - if a successful platform purchase can occur without the app ever calling our verify endpoint, that would be a silent revenue-loss bug, but there is no DB evidence either way this period (sample size too small: 0 completions, 0 receipts).

No PII, no per-user identifiers were queried or included - all results are aggregate counts. Dyno `run.5048` stopped after capture.
