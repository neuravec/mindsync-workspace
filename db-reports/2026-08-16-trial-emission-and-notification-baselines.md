# Trial-emission verdict + notification/preferences baselines (2026-08-16)

**Prod state at time of query:** Heroku v534, backend commit `4bb9b2c`, Alembic head `ll3m4n5o6p7q`.
**Access:** Heroku one-off dyno, `Get-Content script.py | heroku run --no-tty -a mindsync python` (PowerShell). Read-only (`SET TRANSACTION READ ONLY`, `SELECT` only, no commits). Two runs, `run.9661` and `run.7659`; both exited on their own when stdin hit EOF — **no dyno was left running** (confirmed via `heroku ps -a mindsync`, only the standing `web`/`worker`/`scheduler` dynos show).
**Privacy:** aggregates only. The one sampled `dedup_key` list shows raw Firebase UIDs — see note under §2.1; everything else is counts/dates only.

---

## 1. Question 1 (primary): is `trial_started = 0` real, or is emission broken?

### 1.1 Table identification (schema truth, not `models.py`)

`information_schema.columns` confirms `models.py` is current for the tables in scope — no drift found on `subscription_receipts`, `user_subscription`, `user_subscription_trial`, `notification_moments`, `user_preferences`, `user_fcm_token`, `notification_logs`. One thing worth flagging: `subscription_receipts.created_at` is `timestamp without time zone` while every other timestamp column touched in this report is `timestamp with time zone` — not a bug, just an inconsistency to keep in mind if `backend-api` ever writes date-math against it.

`subscription_receipts` has **no `is_trial` column** — trial/paid is never persisted per-receipt. The only durable trial signal lives on `user_subscription_trial` (`trial_started_at`, `trial_platform`, `trial_product_sku`, `trial_ended_at`, `trial_outcome`), written exactly once by `_atomic_mark_trial_started`/`_atomic_mark_trial_ended` in `app/services/posthog_service.py`. Confirmed by grep — `trial_started_at=` appears exactly once in application code (`posthog_service.py:781`); every other match is a test fixture. This is a real, single-writer gate, not a computed/derived column.

### 1.2 Receipts since 2026-08-10

| Query | Result |
|---|---|
| Receipts created since 2026-08-10, by day/platform/status | **`2026-08-10 \| google \| VERIFIED \| 1`** — that's the entire result set |
| Receipts since 08-10 by status | `VERIFIED: 1` |
| Last receipt ever created (any status) | `2026-08-10 19:30:01.119646` |
| Last receipt ever **verified** | `2026-08-10 19:30:01.119646` — same row |
| Total receipts all-time | 120 (was 119 as of the 2026-08-10 check — confirms this is the +1) |

**There has been exactly one receipt-verification event in the six days since the deploy, and none since.** It landed the evening of deploy day, consistent with the growth report's read of it as a smoke-test rather than organic traffic.

### 1.3 Was that one receipt a trial?

Proxy join (`subscription_receipts` VERIFIED since 08-10 LEFT JOIN `user_subscription_trial` on `user_id`, same-day `trial_started_at` as trial signal):

```
google | verified=1 | same_day_trial_start=0 | user_never_trialed=1
```

The purchasing user's `user_subscription_trial.trial_started_at` is NULL — this was a **straight paid verification, not a trial** (`is_trial` was `False` on the Google Play `paymentState` check, so neither `_atomic_mark_trial_started` nor a converting `_atomic_mark_trial_ended` had anything to do).

### 1.4 The all-time picture (the fact that actually settles this)

```
ever_had_trial_started:      0
max_trial_started_at:        None
trial_started_since_0810:    0
trial_ended_since_0810:      0
total_user_subscription_trial_rows: 1810
had_trial_true_count:        554   (default=True Python-side column set at row creation — NOT a real trial signal, ignore for this question)
currently_in_trial_period:   0     (trial_started_at NOT NULL AND trial_ended_at IS NULL)
```

**`trial_started_at` has never once been set to a non-NULL value, for any of the 1,810 rows in `user_subscription_trial`, in the entire history of this database — not just since the 08-10 deploy.** `had_trial` is a separate, misleading column (Python `default=True` fires on every row creation regardless of whether a real trial happened — 554 rows carry it just from account creation, not from any verified trial).

### 1.5 Verdict

**"Zero `trial_started` events" is explained by "no trials occurred," not by broken emission — with one important caveat.**

- The DB-side gate (`_atomic_mark_trial_started`) runs synchronously, in the same request, strictly *before* the PostHog capture call, gated only by `if is_trial:` on a successful verification. If it had ever fired, `trial_started_at` would be non-NULL for at least one row. It has never fired — not once, ever — which rules out "the gate fired but the PostHog side silently dropped it." That specific failure mode is excluded by data.
- Since the emission code (`991cb9a`) deployed 08-10, exactly **one** receipt has been verified at all, and it was determined not-a-trial by the platform's own trial flag (Google `paymentState`). There has been no second data point to test the mechanism against.
- **Caveat — this is an n=1 sample and cannot fully rule out a latent bug in `_atomic_mark_trial_started` itself**, because no trial-eligible receipt has come through to exercise it. What *would* distinguish the two hypotheses: either (a) a real trial-eligible purchase (or a manual Apple/Google sandbox trial redemption) run through `/subscription_data` while watching `user_subscription_trial.trial_started_at` for that user, or (b) confirming in App Store Connect / Google Play Console that the subscription SKU(s) MindSync sells actually have an introductory/free-trial period configured — if no product has a trial period configured, `is_trial` will read `False` forever regardless of code health, and the honest answer becomes "there is no trial to start," a product-configuration fact outside this DB.
- Broader context this reinforces (matches the growth report, section 6): the receipt-verification pipeline itself is essentially silent post-deploy (1 event in 6 days), so "no trials" is really a symptom of "no purchases," not a trial-specific gap.

**Cross-check discrepancy worth flagging, not resolved here:** the 2026-08-16 post-release report (§6) cites PostHog `subscription_purchase_completed` = "5 zdarzeń / 4 osoby, 10.08." `subscription_purchase_completed` fires exactly once per successful verification, in the same request right after `db.commit()` on the receipt row — so 5 firings should correspond to 5 `subscription_receipts` rows on 08-10. There is only 1. Either the PostHog date bucket is approximate, distinct_ids are duplicating a single verification, or those events originated somewhere other than this production path. Recommend `posthog-data-extractor` re-pull `subscription_purchase_completed` with exact timestamps for 08-10 to reconcile against this single DB row — don't treat the "5/4" figure as confirmed until that's done.

### 1.6 Active subscriptions right now

```
active_subscriptions_now (is_active AND (end_date IS NULL OR end_date > now())):  14
active_subscriptions_flag_only (is_active=true, ignoring end_date):               15
```

One row is "stale-active" (flag true, `end_date` already passed) — same class of issue flagged in the 2026-08-10 report (18/34 back then), much smaller now in absolute terms, but the hourly `deactivate_expired_subscriptions` job is still not fully current. Not re-investigated in depth here; noted for continuity.

---

## 2. Question 2: baselines for the notification_moments / user_preferences fix batch

### 2.1 `notification_moments`, last 7 days (created_at ≥ now() − 7d, i.e. 08-09→08-16 partial)

| moment_type | moments | distinct users |
|---|---:|---:|
| ADD_THERAPY_DATE | 12,294 | 1,786 |
| THERAPY_RELATIONSHIP_CHECKIN | 1,767 | 1,767 |
| REFLECTION_INVITATION | 1,763 | 1,763 |
| ACCOUNT_SETUP_NUDGE | 49 | 18 |
| RE_ENGAGEMENT | 30 | 27 |
| MOOD_UPDATE_REQUEST | 26 | 24 |
| GOALS_WEEKLY | 12 | 12 |
| MOOD_DIP_ALERT | 3 | 2 |
| THERAPY_APPOINTMENT | 3 | 1 |
| BETWEEN_SESSIONS_NOTE | 2 | 1 |
| RECORD_SESSION | 1 | 1 |
| THERAPY_PREP | 1 | 1 |
| POST_SESSION_REFLECTION | 1 | 1 |

ADD_THERAPY_DATE per-day: `08-09:1620, 08-10:1724, 08-11:1777, 08-12:1781, 08-13:1784, 08-14:1785, 08-15:1669, 08-16:154 (partial day)`. Steady ~1,750-1,785/day — unchanged from the 08-16 report's 6-day read (10,522/6 ≈ 1,754/day). No drift yet, as expected pre-fix.

**Read the REFLECTION_INVITATION / THERAPY_RELATIONSHIP_CHECKIN numbers carefully — they are not a new anomaly, they're a window-definition artifact worth understanding before/after comparison:**

- Their `dedup_key` is `{TYPE}:{user_id}:2026-W32` — these are **weekly** moments, one candidate generated per user per ISO week. My 7-day window (08-09 onward) happens to catch that week's bulk-generation day (08-09: 1,644 REFLECTION_INVITATION + 1,649 THERAPY_RELATIONSHIP_CHECKIN created in one day, nearly the entire user base at once), which the original report's 6-day window (10.08 start) mostly missed.
- Status breakdown for the same 7-day window: **REFLECTION_INVITATION → SENT 34 / EXPIRED 1,729; THERAPY_RELATIONSHIP_CHECKIN → SENT 34 / EXPIRED 1,733.** Only ~2% of generated candidates for these two types are ever actually selected and sent — the other 98% sit as PENDING until `expires_at` passes. That reconciles with the report's earlier "30/30" figures, which were counting *sent* moments in a narrower window, not *generated* candidates.
- This is itself a useful pre-existing baseline for `backend-api`/`data-analytics`: the moment-selection orchestrator is starving nearly everything except `ADD_THERAPY_DATE` — 1,763 REFLECTION_INVITATION candidates were generated this week and only 34 were ever chosen to send. Worth keeping in view alongside the ADD_THERAPY_DATE throttling fix, since fixing ADD_THERAPY_DATE's dominance may simply hand that daily "slot" to whichever of these other types is next in priority — good to know the raw supply of un-sent candidates is large.
- Note on the sample I pulled to confirm the dedup pattern: it returned raw Firebase UIDs (e.g. `THERAPY_RELATIONSHIP_CHECKIN:f68GSy9dG5aeHA1Q0A0mIB3accD3:2026-W32`) — that was a debugging query against `dedup_key`, not part of the deliverable, and no UID appears anywhere else in this report or was retained past the terminal check.

`push_delivered` for these two types (7d): REFLECTION_INVITATION `False=23 / True=1740`; THERAPY_RELATIONSHIP_CHECKIN `False=23 / True=1744` — same "defaults to true regardless of delivery" pattern as ADD_THERAPY_DATE (§2.5).

`notification_moments` all-time: 54,142 rows across 14 distinct `moment_type` values.

### 2.2 FCM token coverage

```
users_with_fcm_token: 144
total_users:          1813
```

7.9% of the user base has any FCM token at all. Unchanged from the 08-16 report's 144/1813 — confirms this is a stable baseline, not something that moved between reports.

### 2.3 `user_preferences` fill-rates

```
total_prefs_rows:               1793
therapy_schedule_filled:           4   (NOT NULL and not '', '[]', 'null')
custom_therapy_sessions_filled:    8
next_session_date_notnull:         2
next_session_date_future:          1
```

Every one of these numbers matches the 08-16 report exactly (4 / 8 / 2 / 1) — confirms nothing has drifted since that report and this is a clean pre-fix baseline for `backend-api` to diff against post-deploy.

### 2.4 `therapy_schedule` filled but `next_session_date IS NULL`

```
count: 3
```

Also unchanged from the 08-16 report's finding (§4.5 there — `next_session_date` is write-once at save time in `crud.update_therapy_schedule` and never refreshed, so it goes stale). Still 3 users in this state as of today.

### 2.5 ADD_THERAPY_DATE interaction stats, last 7 days

```
total=12294  sent=12294  opened=26  acted=5  dismissed=0
push_delivered: False=1554, True=10740
```

100% of ADD_THERAPY_DATE moments in the window carry a `sent_at` timestamp (it's the daily type that always gets selected — contrast with §2.1's weekly types where ~98% never get sent). Open rate 26/12294 = 0.21%, act rate 5/12294 = 0.04% — essentially unchanged from the report's 22/10522 (0.21%) and 5/10522 (0.05%).

Cross-tab against real FCM ownership:
```
has_fcm=False, push_delivered=False:  1553
has_fcm=False, push_delivered=True:   9790   <- still the core problem
has_fcm=True,  push_delivered=False:     1
has_fcm=True,  push_delivered=True:    950
```

**`push_delivered` is still not trustworthy as of this baseline** — 9,790 moments (79.6% of the week's ADD_THERAPY_DATE volume) are marked `push_delivered=True` for users who own zero FCM tokens, meaning no push could possibly have reached a device. This is the same shape of bug the 08-16 report flagged (§4.2/§7). Note: I found a `push_delivered`-aware code comment in the current `notification_moment.py` model (CS-20 / MSV3.3, describing exactly this fix — "written... exactly once... True only when the user had >=1 FCM token AND the send call did not raise") — but the live data above proves that logic is **not yet in effect on prod** (v534/`4bb9b2c`), whether because it hasn't deployed yet or the deployed code doesn't match what's in the local tree. `backend-api` should confirm which.

---

## 3. Question 3: is there a real send-failure record?

Found: **`notification_logs`** (`app/models/models.py:1647`, not `notification_moments` — confirmed by grep for `token_suffix`/`status ∈ {sent,failed,token_invalid}` at line 1667). Columns: `id, user_id, notification_type, title, body, token_suffix, status, error_message, created_at`. No FK back to `notification_moments` (no `moment_id`, no `dedup_key`).

Last 7 days:
```
status distribution:  sent=1354, token_invalid=10   (no "failed" observed in this window)
total rows 7d:         1364
distinct users 7d:      150
max created_at:        2026-08-16 09:06:40 UTC
total rows all-time:   4376
notification_type breakdown (all-time): notification_moment=4351, session_recording=25
```

**Interpretation and recommendation for `backend-api`:**

`notification_logs` *is* a real, trustworthy per-attempt delivery record — but it is scoped to actual FCM API calls, not to every `notification_moments` status transition. Proof: `notification_moments` had 12,294+ rows reach `sent_at` for ADD_THERAPY_DATE alone this week, but `notification_logs` recorded only 1,364 total entries (all notification types combined) in the same window. The gap is explained by the FCM-token-coverage numbers in §2.2/§2.5: only users who actually own a token generate a real send attempt (and thus a `notification_logs` row); users without a token apparently get `status=SENT` on their `notification_moments` row (and `push_delivered` defaulting to `True`) without any FCM call — and therefore without any `notification_logs` row — ever being attempted.

That means **`notification_logs` already contains the trustworthy delivery signal `push_delivered` is trying and failing to be** — it just isn't wired to `notification_moments`. Concrete recommendation:

1. Do not try to further patch `push_delivered`'s default-true heuristic in isolation — the ground truth already exists one table over.
2. Add a nullable `moment_id` FK (`notification_moments.id`) to `notification_logs`, populated at write time by `deliver_due_moments` (the same call site that already knows both the moment and the token/FCM outcome).
3. Once that link exists, `push_delivered` can be computed by an actual join/reconciliation (`EXISTS (SELECT 1 FROM notification_logs WHERE moment_id = nm.id AND status = 'sent')`) instead of a write-once column that has no way to represent "we never attempted a send" distinctly from "we attempted and it worked."
4. This can only be applied going forward — `notification_logs` rows have no moment reference historically, so the ~54k existing `notification_moments` rows can't be backfilled this way; if a historical accuracy pass is wanted, it would have to fall back to the `has_fcm_token`-at-send-time heuristic used in this report's cross-tab, which is imperfect (tokens can be added/removed after the fact).
5. Separately: `notification_logs` is entirely absent for `session_recording` pushes outside 25 rows in its whole history versus 4,351 for `notification_moment` — if `session_recording` pushes matter to reliability tracking, confirm that code path is actually calling into the same logging helper.

---

## 4. Summary for the operator

- **Trial emission: not broken, just untested.** Zero trials, ever, at the DB layer — not "since the fix shipped," literally zero in 1,810 `user_subscription_trial` rows across the app's whole history. The one receipt verified since 08-10 was confirmed non-trial by the platform's own flag. The emission code is exonerated by data as far as it can be with n=1; the real question is upstream — whether any MindSync subscription product even has a trial period configured in App Store Connect / Play Console, and separately, why the payment funnel produced only 1 verification event in 6 days.
- **Notification/preferences baselines are stable and match the 08-16 report almost number-for-number** (`user_preferences` fill-rates identical; FCM coverage identical; ADD_THERAPY_DATE volume/open/act rates within noise) — a clean pre-fix baseline for `backend-api` to diff against after their batch deploys.
- **New finding surfaced along the way:** REFLECTION_INVITATION/THERAPY_RELATIONSHIP_CHECKIN generate ~1,750 weekly candidates each (nearly 1 per user), of which ~98% silently expire unsent — worth keeping in view for whoever redesigns moment selection, so ADD_THERAPY_DATE's fix doesn't just hand its "slot" to one of these instead.
- **`push_delivered` recommendation to `backend-api`:** don't keep patching the column — reconcile it against `notification_logs`, which already has the real per-send outcome; needs a `moment_id` FK to make that join possible.
