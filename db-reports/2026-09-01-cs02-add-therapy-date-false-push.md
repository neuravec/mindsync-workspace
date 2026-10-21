# CS-02: "Add your next session date" false push - production evidence

Date: 2026-09-01
Author: database-administrator (read-only prod audit via Heroku one-off dyno)
Scope: MSV3.10 CS-02 - user report that the ADD_THERAPY_DATE push ("you haven't set an upcoming therapy session yet") fired for a user who says she had already set her next session date.

## Access method

All queries ran read-only against prod Postgres via `heroku run -a mindsync python < script.py` (REPL-safe scripts, one statement per line, `SET TRANSACTION READ ONLY`, `SET statement_timeout`). Three one-off dynos were used (`run.9434`, `run.5255`, `run.7668`); each was stopped after its output was captured. No writes were made anywhere.

## Schema check (prod, not models.py)

`user_preferences`, `notification_moments`, `notification_logs` and `users` were inspected via `information_schema.columns` before trusting field names. Two things worth flagging:

- **`user_preferences` has no `updated_at` / `created_at` column at all.** There is no audit trail of when `therapy_schedule`, `custom_therapy_sessions`, or `next_session_date` were last written. This directly limits Question 2 below (see verdict) and is not new - this is the second CS-family case where "did the user's edit land before or after the system reacted" cannot be answered from prod data alone. Recommend `backend-api` add an `updated_at` column (or a lightweight schedule-write audit log) if this class of report recurs.
- `notification_moments.scoring_signals` is a Postgres `json` column (not `jsonb`); `->>'date_status'` extraction works as expected, confirmed live.
- No other drift found: `notification_logs.moment_id` exists per migration mm4n5o6p7q8r, `notification_moments` columns match `models.py` exactly.

## Question 1: identifying the reported user and her data

A name search for "[fragment nicku]" (any casing, any substring) against `user_profile.full_name` returned **zero rows** - no user in prod has "[fragment nicku]" anywhere in `full_name`. Broadening the search (`%[fragment nicku]%`, `%wera%`, `ver%`) surfaced exactly one plausible match: a profile with `full_name = "[fragment nicku]"` (the only "[fragment nicku]" match in the entire 1,810-row `user_profile` table; fill rate for `full_name` is 1,260/1,810 filled, 1,250 non-empty). This user has 14 ADD_THERAPY_DATE moments in the last 30 days and a `time_zone` of `UTC-4`, and her push timestamps land at ~22:0x UTC daily, i.e. 18:00 local - exactly `DAY_PRECISION_SEND_HOUR`. This is treated as the reported user for the rest of this report (identifier masked below; only a truncated user-id suffix is used, matching the codebase's own `token_suffix` debugging convention - no raw Firebase UID or full name is reproduced here).

**Her current (2026-09-01) scheduling fields, raw, unmasked (these are scheduling data, not medical content):**

| Field | Value |
|---|---|
| `time_zone` | `UTC-4` |
| `therapy_frequency` | `weekly` |
| `custom_interval_days` | `NULL` |
| `next_session_date` | `NULL` |
| `therapy_schedule` | `NULL` |
| `custom_therapy_sessions` | `NULL` |
| `notification_enabled` | `true` |

**All three fields that feed `compute_next_session_date()` are simultaneously NULL right now.** There is no trace anywhere in her preferences row of a Wednesday-15:00 (or any) session, past or future.

**Her ADD_THERAPY_DATE moment history (most recent 15, which is also all of the last 30 days' worth):**

Fifteen moments, one per calendar day, **2026-08-01 through 2026-08-15 with no gaps**, then **nothing since**. Every row: `status = EXPIRED`, `scoring_signals->>'date_status' = NULL` (i.e. the JSON key is simply absent - this predates the `date_status` field), `sent_at` populated 3-5 minutes after `created_at`, `push_delivered` alternating True/False (mostly True), and **no linked `notification_logs` row via `moment_id`** for any of them (that reconciliation column has no backfill for pre-CS-20 rows, consistent with rows this old).

The actual push copy delivered (pulled directly from `push_title`/`push_body`, safe to reproduce - this is plain push copy per the model's own docstring, not therapy content) for the three most recent sends:

> **Add your next session date** - "You haven't set an upcoming therapy session yet - add one so MindSync can help you prepare."

This is the `_FALLBACK` ("never set") copy branch, not `_FALLBACK_PASSED` ("set one, it passed"). Consistent with `date_status = NULL`: this generator predates the 2026-08-16 post-release-review fix that added the two-branch copy logic and the `CooldownGiveUpThrottle` (7-day cooldown, give-up after 3 consecutive unengaged sends).

**Checking whether she's still getting this push type at all:** querying all her `notification_moments` after 2026-08-15 (any type) shows she is very much alive in the notification system - `MONTHLY_SUMMARY_READY` (2, latest 2026-09-01), `WEEKLY_SUMMARY_READY` (3, latest 2026-08-31), `THERAPY_RELATIONSHIP_CHECKIN` (3, latest 2026-08-30), `REFLECTION_INVITATION` (3, latest 2026-08-30) - but **zero ADD_THERAPY_DATE moments since 2026-08-15**. That specific generator has gone silent for her while every other moment type keeps firing normally, which is the expected fingerprint of the give-up throttle tripping (three-plus consecutive unengaged ADD_THERAPY_DATE sends -> permanent-until-reset quiet period for that moment type only), not a general notification outage.

Her account: `created_at = 2026-03-31`, `last_login = NULL`, `activated_at = NULL` - both tracking columns are unset despite an account old enough to be generating weekly/monthly summaries and therapy-relationship-checkin content, so treat those two columns as an unreliable engagement signal for her specifically (likely a broader tracking gap, not something specific to this bug).

## Question 2: timing correlation (save vs. push)

**Cannot be fully determined from prod data** - `user_preferences` carries no `updated_at`, so there is no way to timestamp when (or whether) a save attempt landed, only what the row holds right now versus what `notification_moments.created_at`/`sent_at` recorded historically.

What the data does support:

- Her last ADD_THERAPY_DATE push fired 2026-08-15 22:02 UTC (18:02 local) and was delivered at 22:05 UTC - a 3-minute gap, not a stale/delayed delivery.
- As of right now, all three schedule-bearing columns are NULL. If she genuinely saved a Wednesday-15:00 session (recently, around when this ticket was filed), that save is **not currently reflected in the database at all** - either it was never persisted, or it was persisted and has since been cleared by a later action (e.g. a frequency switch without re-sending `custom_sessions`, a path `crud.update_therapy_schedule` explicitly guards against for one specific case but which may have other triggers not covered).
- If instead her report describes the Aug 1-15 period (plausible: support tickets on this kind of issue often surface days to weeks after the fact, and her push history stops cold exactly when the documented 2026-08-16 fix would have started throttling her), then the mechanism is very likely the already-diagnosed pre-fix bug: the OLD generator had no `date_status` distinction at all and no cooldown, so a user who genuinely once had a session that later passed (or any transient/expired schedule state) would get the "you never set one" copy daily, indefinitely, until the fix shipped.

Both readings are consistent with the data; distinguishing them needs either (a) the exact date/time of her support call, or (b) an audit column on `user_preferences` going forward.

## Question 3: global cross-check, last 30 days

ADD_THERAPY_DATE moments in the last 30 days, grouped by `scoring_signals->>'date_status'`, cross-checked against each recipient's **current** preferences state:

| date_status | moments | distinct users | w/ any `next_session_date` | w/ FUTURE `next_session_date` | w/ non-empty `therapy_schedule` | w/ non-empty `custom_therapy_sessions` | future date but BOTH schedule fields empty |
|---|---|---|---|---|---|---|---|
| NULL (pre-fix generator) | 24,694 | 1,786 | 14 | 0 | 73 | 121 | 0 |
| `never_set` | 17 | 11 | 0 | 0 | 0 | 0 | 0 |
| `passed` | 4 | 2 | 0 | 2 | 2 | 4 | 0 |

Two things stand out:

1. **The pre-fix ("NULL") bucket still dominates volume in the 30-day window** (24,694 of 24,715 total, 99.9%) because the lookback window (now - 30 days = 2026-08-02) still spans most of the pre-fix flood period. This matches the post-release-review's own characterization almost exactly: status breakdown for the same 30-day window is `EXPIRED 24,661 / OPENED 37 / ACTED 15 / SENT 2`, an engagement rate of (37+15)/24,715 = **0.21%**, identical to the review's previously reported figure for the Aug 10-16 window.
2. **Only 21 moments across 13 distinct users carry the new `date_status` tag** in the entire 16 days since the fix (2026-08-16 through 2026-09-01) - roughly 1.3 moments/day system-wide, down from ~1,780/day pre-fix. This is the expected, intended effect of the 7-day cooldown + 3-strikes give-up (most of the affected population had already accumulated 3+ unengaged sends by the time the fix shipped, so it gave up on almost everyone almost immediately) - flagged here only as a side observation for product/growth awareness, not part of this bug.
3. **`future_but_empty_both` is 0 in every bucket.** The specific systemic hypothesis "user has a stored FUTURE `next_session_date` but `therapy_schedule`/`custom_therapy_sessions` are both empty, so eligibility silently ignores it" affects **zero** users among last-30-day ADD_THERAPY_DATE recipients, measured against current state. This is a proxy (current state, not state-at-generation-time - the same audit-trail gap as Question 2 applies), but it does mean this exact failure mode is not currently a visible systemic driver at scale, even though it remains a structurally real gap in the code (see Question 4/verdict).

## Question 4: data-format integrity

Samples pulled directly from prod (8 rows each, user ids truncated to last 6 characters):

**`therapy_schedule`** (weekly/biweekly recurring entries) - all 8 samples use `day_of_week` as an integer 0-6 (Monday-first) and `time_of_day` as 24-hour `"HH:MM"`, e.g. `[{"day_of_week": 2, "time_of_day": "15:00", "therapist_name": null}]` (day 2 = Wednesday, 15:00 - notably this is the exact "Wednesday 15:00" pattern the reported user described, on a different account). No locale weekday names, no 12-hour format, no empty-string-vs-NULL ambiguity observed in the sample.

**`custom_therapy_sessions`** (one-off calendar-picked sessions) - `date` as ISO `"YYYY-MM-DD"`, `time_of_day` as 24-hour `"HH:MM"`, `therapist_name` nullable and correctly UTF-8/unicode-escaped when present (one sample carries a Polish name with `ł` correctly round-tripping). No corruption observed.

**`next_session_date`** - all 8 samples are `timestamp with time zone`, always rendered with an explicit `+00:00` offset (Postgres storing everything internally as UTC per column type `DateTime(timezone=True)`). No naive-datetime rows found in this sample.

Within the 8-row samples pulled, no encoding, locale, or naive/aware mismatch was found. This does not rule out a client-side (Flutter) encoding bug for a single incident, since prod would only show the corrupted value if a bad value actually got written and this samples only from users with non-empty data today - but it does mean the stored format itself, where it is populated, is clean and internally consistent with what the parser expects.

## Question 5: delivery-lag distribution

ADD_THERAPY_DATE moments in the last 30 days with `sent_at` populated (n = 24,715):

| metric | value |
|---|---|
| average lag | 1.8 min |
| median lag | 1.1 min |
| p95 lag | 5.6 min |
| max lag | 14.0 min |
| moments delivered >1h after creation | 0 |
| moments delivered >6h after creation | 0 |

Delivery is consistently fast and tight to the 5-minute `deliver_due_moments` cadence, with **zero** cases of a multi-hour gap in the last 30 days. The reported user's own moments individually confirm this (3-5 minute `sent_at - created_at` gap on each of her 15 rows). **Stale-state delivery (hypothesis c) is ruled out**, both globally and for this specific user - there is no evidence of a queue-backlog delay class of bug here.

## Verdict

**(d) other, more precisely a two-part answer, not a clean single letter:**

1. **The specific symptom described (daily "you haven't set a session" push despite the user having session data) matches the signature of an already-diagnosed and already-fixed bug**, not a new regression. The reported user's own ADD_THERAPY_DATE history is fifteen consecutive daily pushes (2026-08-01 to 2026-08-15) carrying the pre-fix, no-distinction copy ("you haven't set an upcoming therapy session yet"), with `date_status = NULL` throughout - the exact fingerprint of the generator version that predates the 2026-08-16 post-release-review fix (which added the `date_status: "passed"` copy branch and the cooldown/give-up throttle). Her ADD_THERAPY_DATE pushes stop cold immediately after that date while every other moment type keeps firing for her normally through 2026-09-01, which is the expected behavior of the give-up throttle tripping, not a global outage. If her report describes something from that window, it is very likely this already-fixed issue reaching the ticket queue late.
2. **Separately, and unresolved**: her preferences right now (2026-09-01) show `next_session_date`, `therapy_schedule`, and `custom_therapy_sessions` all simultaneously NULL - no trace of a Wednesday-15:00 (or any) session anywhere. If her complaint is recent rather than historical, this points at **(a) a save that never persisted** (or was persisted and later silently cleared) rather than (b) a parser/timezone misread - the stored-data-format samples in Question 4 show no encoding red flags, and (c) stale delivery is conclusively ruled out by Question 5. But `user_preferences` has no `updated_at` column, so this cannot be proven from prod data alone; it can only be narrowed by getting the exact date/time of her support call and comparing it against the fact that no ADD_THERAPY_DATE moment has fired for her since 2026-08-15.

## Handoffs to `backend-api`

- **Confirm exact date of [użytkowniczka V]'s report.** If it is on/before 2026-08-16, this is very likely the already-fixed pre-release bug and no new code change is needed for her case specifically - just customer communication. If it is after 2026-08-16 and she insists she saved a schedule recently, investigate the Flutter `PUT /therapy-schedule` call path for this account (silent failure, retry-without-persist, or a race with another settings write) since prod shows zero trace of her save in any of the three schedule columns.
- **Consider adding an `updated_at` column to `user_preferences`** (or a lightweight write-audit log for the schedule fields specifically). This is the second class of "did the save actually land, and when" question DBA could not answer from prod data alone in the last two months; a timestamp would make future disputes like this resolvable in one query instead of a code archaeology exercise.
- **No action needed on delivery latency or data-format encoding** - both are clean per Questions 4 and 5.
- Not part of this ticket, but worth a look separately: the give-up throttle appears to have silenced ADD_THERAPY_DATE for the large majority of the previously-spammed population almost immediately after shipping (21 moments/13 users system-wide in 16 days, versus ~1,786 users/day before). Whether that is the intended steady state or an over-correction is a product question, not a bug, flagged here only for awareness.

## Notes on method

Per the access recipe: all queries were run via `heroku run -a mindsync python < script.py` (REPL-safe, one statement per line), each one-off dyno was stopped immediately after its output was captured (`run.9434`, `run.5255`, `run.7668`), and every query was a bounded, read-only `SELECT` (`SET TRANSACTION READ ONLY`, `LIMIT` on every row-returning query, aggregates for the cross-checks). No raw Firebase UID, full name, or free-text/therapy content is reproduced in this report; the reported user is identified only by a masked user-id suffix held internally for engineering follow-up, not printed here.
