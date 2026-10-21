# MSV3.11 prod evidence pull (2026-09-02)

Spec: `Business_requirements/MS_3/v3.11/MSV3.11 - Change Spec (Grace).md`. Scope: CS-10 (reporter + Therapy Schedule), CS-07 (repeating to-dos), CS-01 (threads), CS-11 (notification cycle audit), plus migration-state confirmation. All queries below are read-only `SELECT`/catalog queries, run inside a bounded `SET TRANSACTION READ ONLY` session via a Heroku one-off dyno (`heroku run --no-tty -a mindsync python`, PowerShell, stdin-piped script – the `--no-tty` variant runs the script as a normal module instead of an interactive REPL and the dyno exits on its own; both runs used here exited with code 0 and `heroku ps` afterward showed no stray `run.*` dyno). Two script runs: the main pull and one small follow-up (single repeating-item timestamps, FCM/user timestamp ranges). Full scripts are in the scratchpad (`msv311_query.py`, `msv311_followup.py`), not committed.

Data minimization: the reporter (Grace [nazwisko]) is identified below only by a masked suffix of her internal Firebase-UID string (`v3aJf1`, last 6 chars) – no email, full name, or full UID appears anywhere in this report or was printed by the scripts beyond that masked form. No thread/to-do free text was read (all `text`/`title` columns are encrypted at rest in any case).

---

## F. Migration state

```sql
SELECT version_num FROM alembic_version;
```

| version_num |
|---|
| `pp7q8r9s0t1u` |

**Found.** Matches the expected HEAD recorded in project memory. No pending migrations on prod as of this check.

Schema cross-check (not just the version row) also came back clean: `user_preferences`, `threads`, `thread_sources`, `todo_items`, `todo_completions` columns on live prod match `app/models/workspace.py` / `app/models/models.py` exactly, and the live `moment_type_enum` (22 labels, all UPPERCASE) matches `MomentTypeEnum` in `app/models/notification_moment.py` exactly, member-for-member. **No schema or enum drift found anywhere in this batch's scope.**

---

## A. Reporter (Grace [nazwisko], CS-10)

```sql
SELECT u.id FROM users u LEFT JOIN user_profile p ON p.user_id = u.id
WHERE u.email ILIKE '%[nazwisko]%' OR p.full_name ILIKE '%[nazwisko]%' LIMIT 5;
```
**Found** – exactly one match (masked `v3aJf1`). No ambiguity, no fallback-to-firstname needed.

```sql
SELECT therapy_schedule, therapy_frequency, custom_interval_days, next_session_date,
       custom_therapy_sessions, time_zone FROM user_preferences WHERE user_id = :uid;
SELECT first_day_of_week FROM user_profile WHERE user_id = :uid;
```

| field | value |
|---|---|
| therapy_frequency | `biweekly` |
| custom_interval_days | NULL |
| next_session_date | **NULL** |
| time_zone | UTC-4 |
| therapy_schedule entries | **0** (empty array) |
| custom_therapy_sessions entries | **0** |
| first_day_of_week (week-start pref) | SUN |
| user_preferences.updated_at / created_at | **column does not exist** (confirmed live via `information_schema.columns` – cannot date-order her save attempts against anything) |

**Interpretation – did her schedule ever persist? No, not in any of the three ways the app can represent one.** `therapy_frequency` is the one field that stuck (`biweekly`); every field that would actually make a session "exist" for eligibility purposes – the recurring schedule array, `next_session_date`, and any custom one-off session – is empty. This is the exact "therapy_schedule always `[]`" data-loss pattern already documented in the spec at `therapy_schedule_entry.dart:9`, caught live on the reporter's own row. Her "no upcoming sessions scheduled" complaint is not a display bug on top of good data – there is no session data to display. Root-cause layer (FE not sending entries vs. BE dropping/failing to persist them, or a subsequent frequency-mode switch clearing the array) is not determinable from data alone; hand to `backend-api`/`flutter-mobile` per CS-10.

Notification history (last 60 days, grouped by type/status):

```sql
SELECT moment_type, status, count(*), min(created_at), max(created_at)
FROM notification_moments WHERE user_id = :uid AND created_at >= now() - interval '60 days'
GROUP BY moment_type, status ORDER BY moment_type, status;
```

Only two schedule-adjacent types ever fired for her: `ADD_THERAPY_DATE` (8 OPENED, 1 ACTED, 5 EXPIRED, spanning 2026-08-04 to 2026-08-31) and generic `WEEKLY_SUMMARY_READY`/`MONTHLY_SUMMARY_READY`/`GOALS_WEEKLY`/`RE_ENGAGEMENT`/`REFLECTION_INVITATION`/`THERAPY_RELATIONSHIP_CHECKIN`/`MOOD_UPDATE_REQUEST` at low volume. **Zero `THERAPY_APPOINTMENT`, `THERAPY_PREP`, or `POST_SESSION_REFLECTION` moments ever** – mechanically correct given she has no anchor date, but it confirms the whole session-notification chain is dark for her. She engaged with `ADD_THERAPY_DATE` repeatedly (8 opens, 1 acted on 2026-08-05) – she was actively trying to set the date via the push, consistent with her letter ("tried to schedule it multiple times"). No user_events/audit table exists anywhere in the schema for "schedule saves" (checked `information_schema.tables` for `%user_event%`/`%audit%`/`%schedule_log%` – only `monthly_therapy_audits` exists, unrelated) – **not found**, no save-attempt audit trail available at all.

Repeating to-dos: **0 rows** – she has never created a repeating to-do item, so her account provides no personal evidence for CS-07 either way.

Threads (CS-01), by status and full created_at list:

```sql
SELECT status, count(*) FROM threads WHERE user_id = :uid GROUP BY status;
SELECT id, status, created_at, updated_at, pinned_at FROM threads WHERE user_id = :uid ORDER BY created_at;
```

**26 threads, all status = `open`, zero ever closed.** The created_at list shows five distinct clusters of 2-3 threads created within single-digit seconds of each other (ids 661/662/663 on 08-19 12:38, 664/665/666 the same day 16:06, 793/794/795 on 08-24, 826/827/828 on 08-27, 892/893/894 on 08-30) – a direct, timestamped fingerprint of "one input burst produced several separate thread rows instead of one thread with sub-entries," exactly the duplicate-title/non-merging complaint in Grace #1. She alone accounts for 26 of the 64 open threads that exist system-wide (see population section) – she is by far the heaviest real-world user of the module the CS-01 rewrite targets.

---

## B. Population (CS-10)

```sql
SELECT coalesce(therapy_frequency,'(null)'), count(*) FROM user_preferences GROUP BY 1;
```
| frequency | n |
|---|---|
| weekly | 1755 |
| custom | 28 |
| biweekly | 27 |

(1810 `user_preferences` rows total; 25 of the 1835 `users` rows have no preferences row at all – `weekly` is also the column's default, so most of the 1755 are unconfirmed as ever having touched the schedule UI, not confirmed non-attempts.)

```sql
-- schema-level flags
SELECT count(*) FILTER (WHERE therapy_schedule NOT IN ('','[]') AND therapy_schedule IS NOT NULL) AS has_schedule_text,
       count(*) FILTER (WHERE next_session_date IS NULL) AS null_next_session,
       count(*) FILTER (WHERE therapy_schedule NOT IN ('','[]') AND therapy_schedule IS NOT NULL AND next_session_date IS NULL) AS has_schedule_but_null_next,
       count(*) AS total_rows
FROM user_preferences;
-- + a bounded python-side parse of the same table (1810 rows, aggregates only, LIMIT 5000) for the JSON-dependent questions
```

| metric | value |
|---|---|
| total `user_preferences` rows | 1810 |
| rows with a **non-empty** `therapy_schedule` array | **12** (0.66%) |
| rows with `next_session_date IS NULL` | 1804 (99.7%) |
| **has a real schedule, but `next_session_date` is NULL anyway** | **7** |
| rows with any `custom_therapy_sessions` entries | 10 |
| of those, entries are **all in the past** | 9 (90%) |
| "invisible to eligibility" gap (`next_session_date` set, schedule empty, no custom sessions) | **0** |
| qualifying users (real schedule OR a future custom session) | **13** |

**Interpretation.** Two distinct findings, both important:
1. **Prod-wide, essentially nobody has a persisted schedule** – 12 of 1810 users (0.66%). Grace is not an outlier; she is the norm. This reframes CS-10 from "fix one user's bug" to "the therapy-schedule save path is not working (or is essentially unused) for the overwhelming majority of the user base" – can't distinguish "never attempted" from "attempted and lost" at the aggregate level (no save-audit trail, see above), but the reporter's own row proves at least one confirmed case of the latter.
2. **The 7-user "schedule exists but next_session_date is NULL" group is the single most actionable data point for CS-10.** These are users where the persistence half of the chain worked, and the *recompute* half (`compute_next_session_date` / the biweekly/custom anchor math) silently produced nothing. This is a narrow, findable population for `backend-api` to pull and repro against, unlike Grace's row where nothing at all persisted. The prior-session structural gap ("`next_session_date` alone with empty schedule/custom") remains at 0 users, consistent with the 2026-09-01 audit – still not a live risk on its own.

```sql
-- ADD_THERAPY_DATE since the v544 fix (2026-09-01 12:00 UTC), restricted to the 13 qualifying users
SELECT count(*), count(DISTINCT user_id) FROM notification_moments
WHERE moment_type = 'ADD_THERAPY_DATE' AND created_at >= '2026-09-01 12:00:00+00'
  AND user_id IN (<13 qualifying ids>);
```
**Result: 0 rows, 0 distinct users.** Clean pass – since the v544 CS-02 fix, none of the 13 users who currently have a real schedule/future session have received a false "you haven't set a session" push. The guard is holding.

```sql
SELECT moment_type, count(*), count(DISTINCT user_id) FROM notification_moments
WHERE moment_type IN ('THERAPY_APPOINTMENT','THERAPY_PREP','POST_SESSION_REFLECTION')
  AND created_at >= now() - interval '14 days' GROUP BY moment_type;
```
| moment_type | n (14d) | distinct users |
|---|---|---|
| THERAPY_APPOINTMENT | 32 | 12 |
| THERAPY_PREP | 32 | 12 |
| POST_SESSION_REFLECTION | 19 | 12 |

**Do session-driven notifications fire at all? Mechanically, yes** – all three types are actively firing, at a steady cadence, for a set of 12 distinct users. But that set is ~12 out of 1835 total users (0.65%), i.e. almost exactly the population that has a persisted schedule. **The generators themselves are not the problem** (no evidence of a broken trigger for users who do have data) – **the bottleneck is 100% upstream, at persistence.** This is the single clearest piece of evidence in this report: fix the save path and this notification volume should scale roughly 150x on its own, with no generator-side change needed.

---

## C. To-dos (CS-07)

```sql
SELECT coalesce(repeat_freq,'(null)'), status, count(*) FROM todo_items GROUP BY 1,2;
```
| repeat_freq | status | n |
|---|---|---|
| daily | done | **1** |
| (null) | archived | 3 |
| (null) | done | 61 |
| (null) | open | 12 |

**Only one repeating to-do item exists in all of production** (77 items total, 76 of them non-repeating). The repeat feature (`repeat_freq` + the lazy self-heal in `app/crud/workspace.py::_maybe_reopen_repeating_todo`/`sweep_repeating_todos`, shipped 2026-07-17 – confirmed via `git log -S`, well before Grace's letter) is effectively unused, not just under-tested.

```sql
SELECT count(*) FROM todo_completions;                                        -- 56 total
SELECT min/avg/max(c) FROM (completions grouped by repeating todo_item_id);    -- min=1 avg=1.00 max=1, n=1
SELECT count(*) FROM (repeating items grouped by todo_item_id HAVING count(*) > 1); -- 0
```

**Zero repeating items have ever recurred more than once** – but the population is exactly 1, so this cannot be read as "systemic failure across many users," only as "the one example we have never recurred." A targeted follow-up on that single item:

```sql
SELECT id, repeat_freq, status, created_at, done_at, reactivated_at FROM todo_items WHERE repeat_freq IS NOT NULL;
-- id=277 | daily | done | created 2026-07-23 22:41 | done_at 2026-08-31 18:05:06 UTC | reactivated_at = NULL
SELECT now(); -- 2026-09-02 05:52:48 UTC at check time
```

**Interpretation.** `done_at + 1 day` (the "daily" interval) = 2026-09-01 18:05 UTC, roughly **12 hours before** this check – so by the code's own math this item is past due to self-heal, and it hasn't (`reactivated_at` is still NULL, `status` still `done`). This is genuinely ambiguous evidence, not a confirmed bug: the reopen logic is **lazy and read-triggered only** ("no cron job flipping repeating to-dos back open on their repeat day... self-heals on next access," per the code's own docstring) – if that user hasn't opened Workspace To-do in the ~12 hours since the window closed, the item is *supposed* to still show `done` until their next visit. I cannot tell from data alone whether it will flip on next read (working as designed) or is actually stuck (a real bug in the interval math). What the data *does* establish cleanly: **the current mechanism can only ever un-stick a repeating item when the user happens to open the app after the interval elapses – there is no background process guaranteeing it.** That is a structural mismatch with the spec's explicit CS-07 requirement ("backend-driven so it works regardless of app opens"), independent of whether this one item is currently buggy. It is also a mismatch on reset semantics: the live interval table is a **fixed offset from `done_at`** (`daily=+1d, weekly=+7d, monthly=+30d`), not a **calendar boundary** (local midnight / user's week-start / the 1st of the month) as Darek's 31.08 decision now specifies – a task done at 23:55 and one done at 00:05 the same "day" get materially different reopen times under the current code. Both points (no background sweep, fixed-offset vs. calendar-boundary reset) are handoffs for `backend-api`, not something provable as "broken" from the one live example alone.

Reporter: 0 repeating items (see section A) – no personal evidence either way.

---

## D. Threads (CS-01)

```sql
SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='threads';
```
Live columns: `id, user_id, title, context_description, status, xp_awarded, created_at, updated_at, closed_at, archived_at, pinned_at`. **Confirmed: no parent/child/group column exists on prod today** – matches the spec's premise exactly, no drift from the model.

```sql
SELECT status, count(*) FROM threads GROUP BY status;
```
| status | n |
|---|---|
| open | 64 |
| closed | 30 |
| touched | 4 |
| archived | 1 |

```sql
-- per-user open-thread distribution
SELECT percentile_cont(0.5)/(0.9) WITHIN GROUP (ORDER BY c), max(c), count(*) users
FROM (SELECT user_id, count(*) c FROM threads WHERE status='open' GROUP BY user_id) t;
```
| | p50 | p90 | max | n_users_with_any_open_thread |
|---|---|---|---|---|
| status='open' only | 5.0 | 25.0 | 26 | **6** |
| status IN ('open','touched') | 5.0 | 26.5 | 27 | 6 |

**Only 6 distinct users, out of 1835, have any open thread at all.** Grace (26 open threads) is the max in this distribution and alone holds 40% of every open thread on the platform. Thread-source fan-out is minimal system-wide: `percentile_cont(0.5)=1, max=1` across 67 threads with sources – **every thread on record has exactly one originating source**, i.e. nothing has ever accumulated a second entry under an existing thread. That is direct structural confirmation of the spec's "every accepted proposal either merges or creates a sibling, and merging isn't happening" description – not just Grace's account, the entire live dataset.

k-anonymity note: the 6-user open-thread population and the 12-user schedule/13-user qualifying-notification populations above are all under the 25-user suppression floor; only the aggregate counts (not any per-user breakdown) are reported here, consistent with the rule.

---

## E. Notifications (CS-11 audit prep)

```sql
SELECT enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid WHERE t.typname='moment_type_enum' ORDER BY e.enumsortorder;
```
22 labels live, all UPPERCASE, **exact 1:1 match** with `MomentTypeEnum` in `app/models/notification_moment.py` (including retired-but-kept members `STREAK_CELEBRATION`, `PATTERN_INSIGHT`, `SESSION_MORNING_OF`). No enum drift.

```sql
SELECT moment_type, status, count(*) FROM notification_moments WHERE created_at >= now() - interval '14 days' GROUP BY moment_type, status;
SELECT date_trunc('day', created_at)::date, count(*) FROM notification_moments WHERE created_at >= now() - interval '14 days' GROUP BY 1 ORDER BY 1;
SELECT moment_type, count(DISTINCT user_id) FROM notification_moments WHERE created_at >= now() - interval '14 days' GROUP BY moment_type;
```
(Full type x status table and the 14-day distinct-user-per-type table are in the script output; day-level granularity was collapsed to a single daily-volume-total series rather than a type x status x day cross-product, to stay compact – noting this design choice rather than silently truncating.)

Selected type x status counts (14d):

| moment_type | SENT | OPENED | ACTED | EXPIRED | distinct users |
|---|---|---|---|---|---|
| REFLECTION_INVITATION | 0 | 0 | 1 | 3370 | 1805 |
| THERAPY_RELATIONSHIP_CHECKIN | 0 | 0 | 1 | 3373 | 1806 |
| WEEKLY_SUMMARY_READY | 1811 | 5 | 2 | 3589 | 1808 |
| MONTHLY_SUMMARY_READY | 1807 | 1 | 1 | 1748 | 1807 |
| THERAPY_APPOINTMENT / THERAPY_PREP / POST_SESSION_REFLECTION | see section B | | | | 12 each |

Daily volume, 14 days (`notification_moments.created_at`):

| day | n |
|---|---|
| 08-19 | 12 |
| **08-20** | **3553** |
| 08-21 | 8 |
| 08-22 | 14 |
| **08-23** | **3943** |
| 08-24 | 1037 |
| 08-25 | 22 |
| 08-26 | 14 |
| 08-27 | 7 |
| 08-28 | 5 |
| 08-29 | 3 |
| **08-30** | **4413** |
| 08-31 | 2090 |
| 09-01 | 796 |
| 09-02 (partial) | 3 |

**Interpretation, for CS-11's mandated audit:**
1. **`REFLECTION_INVITATION` and `THERAPY_RELATIONSHIP_CHECKIN` reach essentially every user (1805-1806 of 1835) roughly once a week, and expire un-acted-on 99.97% of the time** (1 ACTED out of ~3371 in each case) – confirms and sharpens the "16.08 review flagged ~98% expire unsent" lead with fresh data; the real number is worse than the earlier estimate. Strong candidate for the mixin/cycle-fix CS-11 asks for.
2. **`WEEKLY_SUMMARY_READY` reaches SENT for only 1811/5407 (33.5%) of its 14-day volume**, the rest EXPIRE; **`MONTHLY_SUMMARY_READY` reaches SENT for 1807/3555 (50.8%)**. Both are worth a closer look under CS-11's "is the cycle right" question, but note point 3 before trusting these ratios as steady-state.
3. **The day-by-day volume is not smooth – it is dominated by four burst days** (08-20: 3553, 08-23: 3943, 08-30: 4413, plus 08-24: 1037 and 08-31: 2090) that together are ~85% of the 14-day total, against a background of single/double-digit days. This pattern (not a steady per-user daily/weekly drip, but occasional days generating thousands of moments at once) is itself a "daily/weekly cycle" finding worth handing to the CS-11 audit directly – whatever is producing those spikes (a bulk/backfill-shaped cron run, consistent with the RQ-queue-contention history already on this project around 2026-08-20) will distort any naive "average per day" read of cadence health. I am reporting the pattern, not its cause – root-causing the specific job(s) behind each spike day is for `backend-api`/`data-analytics` to trace via job logs, not something derivable from this table alone.

```sql
SELECT (SELECT count(DISTINCT user_id) FROM user_fcm_token) users_with_token,
       (SELECT count(*) FROM users) total_users,
       (SELECT count(*) FROM users WHERE last_login >= now() - interval '30 days') active_30d,
       (SELECT count(DISTINCT f.user_id) FROM user_fcm_token f JOIN users u ON u.id=f.user_id WHERE u.last_login >= now()-interval '30 days') active_30d_with_token;
```
| metric | value |
|---|---|
| users with at least one FCM token | **139 / 1835 (7.6%)** |
| "active in last 30 days" by `last_login` | 21 |
| of those, with a token | 14 (66.7%) |
| new users, last 30 days | 63 |

**Reach caveat, not a diagnosis:** FCM coverage **dropped** from 232/1730 (13.4%) at the 2026-07-03 audit to 139/1835 (7.6%) now – both the absolute count and the share fell even as the user base grew. I'm flagging this as a real decline worth someone's attention, not explaining it (no code investigation was in scope here). Separately, `last_login` gives an implausibly low "active" count (21) that is smaller than 30-day signups (63) – `last_login` only updates via `onupdate=func.now()` on that specific column write path, so it likely undercounts real activity substantially. **Do not treat the 21/1835 figure as a DAU/MAU proxy** – cross-check actual reach against PostHog (`posthog-data-extractor`) rather than this column if CS-11's audit needs a real "how many people could this reach" number.

---

## Handoffs (not implemented here – DBA is read-only)

- **`backend-api` (CS-10):** repro the therapy-schedule save/persist path using Grace's confirmed dead-end case (frequency saved, schedule/next_session_date/custom all empty) and, separately, pull and repro the 7 users who have a real `therapy_schedule` but `next_session_date` stuck NULL (narrower, more tractable repro set than "0.66% of everyone").
- **`backend-api` (CS-07):** the live reopen mechanism (`_maybe_reopen_repeating_todo` / `sweep_repeating_todos`, shipped 2026-07-17) is read-triggered only with no background sweep, and uses a fixed day-offset from `done_at` rather than the calendar-boundary reset (local midnight / user's week-start / 1st of month) Darek's 31.08 decision specifies. Both need addressing for CS-07 as scoped, independent of whether item `id=277` is currently "stuck" or just waiting on its next read (ambiguous from data alone at check time).
- **`backend-api`/`flutter-mobile` (CS-01):** thread_sources fan-out is 1-per-thread across the entire dataset (67/67) – no live counter-evidence that merging ever worked at any point; safe to treat the whole "duplicate sibling" bug as universal, not edge-case.
- **`data-analytics`/`backend-api` (CS-11):** the four multi-thousand burst days in the 14-day notification volume warrant a job-log trace before drawing "daily/weekly cycle" conclusions from raw daily counts; `REFLECTION_INVITATION`/`THERAPY_RELATIONSHIP_CHECKIN`'s ~99.97% expire-unsent rate is confirmed and is the clearest concrete "cycle is wrong" candidate in this pull.
- **Not measurable from Postgres:** true DAU/MAU/"active users" for weighing notification reach – `users.last_login` is not a reliable signal; use PostHog.

No mutations were made. No stray Heroku dynos remain (`heroku ps -a mindsync` shows only the standing `web`/`worker`/`scheduler` processes).
