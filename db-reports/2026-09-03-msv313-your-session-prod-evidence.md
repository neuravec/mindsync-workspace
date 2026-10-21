# MSV3.13 CS-01 / CS-02 prod evidence

**Date:** 2026-09-03 (access restored same day after an earlier Heroku CLI credential outage; see revision history below)
**Backend at time of query:** Heroku v548, commit `072a25b`, `alembic_version.version_num = m313a1b2c3d4` (confirmed directly from the `alembic_version` table, not just trusted from the deploy log)
**Access:** Heroku one-off dyno (`heroku run --no-tty -a mindsync python < script.py`), read-only SELECTs and ORM reads only, `SET TRANSACTION READ ONLY` set first, dyno self-exited on stdin EOF (confirmed via `heroku ps -a mindsync` immediately after -- no leftover one-off, nothing to stop).

## 0. Schema confirmation

```sql
SELECT column_name, data_type FROM information_schema.columns
WHERE table_name='user_preferences'
  AND column_name IN ('custom_interval_days','therapy_schedule','custom_therapy_sessions','next_session_date','time_zone','therapy_frequency')
ORDER BY column_name;
```

| column | data_type |
|---|---|
| custom_therapy_sessions | text |
| next_session_date | timestamp with time zone |
| therapy_frequency | character varying |
| therapy_schedule | text |
| time_zone | character varying |

`custom_interval_days` is **gone** -- confirmed absent from `information_schema.columns` (0 rows for that name). Matches the coordinator's claim; migration `m313a1b2c3d4` has run.

## 1-2. Accounts (given, not re-derived this pass)

Both were supplied by the coordinator from an earlier partial read; this pass fetched full untruncated rows for both.

| user_id | frequency | time_zone (raw) |
|---|---|---|
| `<UID-1>` (Darek) | custom | `UTC+2` |
| `<UID-2>` (second tester) | custom | `UTC-5` |

## 3. Darek's row -- full raw data, tz resolution, and pure-function recompute

**Raw `user_preferences` row:**

- `therapy_frequency` = `custom`
- `time_zone` = `UTC+2`
- `next_session_date` (persisted) = `2026-09-04 18:00:00+00:00`
- `therapy_schedule` = `[{"day_of_week": 0, "time_of_day": "10:00", "therapist_name": null}]` (a recurring Monday 10:00 slot also exists, but is irrelevant here -- see below)
- `custom_therapy_sessions` (**full, untruncated** -- resolves the coordinator's "one truncated entry" note; there is no truncated/malformed entry, it was just a partial earlier read):
  ```json
  [
    {"date": "2026-08-13", "time_of_day": "17:00", "therapist_name": "[terapeutka]"},
    {"date": "2026-08-19", "time_of_day": "10:00", "therapist_name": "[terapeutka]"},
    {"date": "2026-08-26", "time_of_day": "18:00", "therapist_name": "[terapeutka]"},
    {"date": "2026-09-04", "time_of_day": "18:00", "therapist_name": "[terapeutka]"}
  ]
  ```

**How `time_zone='UTC+2'` actually resolves (grepped `app/api/v1/endpoints/therapy_tracking.py:302` and `app/crud/crud.py:~1554`):** both the `/therapy-tracking/session-state` endpoint and `crud.get_therapy_schedule_with_frequency` resolve the timezone with a bare

```python
try:
    user_tz = pytz.timezone(prefs.time_zone or "UTC")
except Exception:
    user_tz = pytz.UTC
```

`pytz.timezone()` only accepts IANA zone names (or plain `"UTC"`) -- it does **not** accept offset strings like `"UTC+2"` or `"UTC-5"` and raises `UnknownTimeZoneError` for them. Reproduced live: `"UTC+2" in pytz.all_timezones` is `False`, so both read paths silently fall through to the `except` and use **plain UTC**, discarding the +2 offset entirely. The codebase already has a correct utility for this exact case -- `app.utils.time_utils.parse_timezone()`, which resolves `"UTC+2"` to `pytz.FixedOffset(120)` and `"UTC-5"` to `pytz.FixedOffset(-300)` -- but neither therapy-schedule read path calls it.

| | app's actual resolution (bare `pytz.timezone`) | what `parse_timezone()` would give |
|---|---|---|
| `now_local` for Darek right now | `2026-09-03 07:58:08+00:00` (UTC) | `2026-09-03 09:58:08+02:00` |

**Does this shift the persisted `next_session_date`?** Yes, and it already has. Darek picked "2026-09-04, 18:00" for his next session. If the app correctly resolved his `UTC+2` timezone, 18:00 local (CEST) is `16:00:00+00:00` in UTC. Instead, the persisted value is `2026-09-04 18:00:00+00:00` -- exactly the naive `18:00` re-interpreted as UTC, a **2-hour skew** baked in at write time by the same tz bug (this write happens inside `crud.get_therapy_schedule_with_frequency`'s self-heal `db.commit()`, which is why the persisted value matches the buggy recompute exactly rather than drifting). This is a real, confirmed, quantifiable bug -- **but it is a stable, self-consistent 2-hour offset, not a source of the "stuck" symptom**: every read recomputes the same wrong-but-stable instant, so it doesn't by itself explain why the card stopped advancing. Flagging separately below for backend-api.

**Pure-function recompute** (using the app's actual, buggy `now_local` in UTC, matching what the deployed code produces):

- `schedule` entries are **ignored** for `frequency="custom"` post-CS-02 (confirmed by reading the deployed `compute_next_session_date`/`compute_last_session_datetime`: the `"custom"` branch returns purely from `custom_sessions`, with no fallback to `entries` at all any more).
- `compute_next_session_date(...)` = `2026-09-04 18:00:00+00:00` (matches the persisted anchor exactly -- expected, since the anchor was itself written by this same computation).
- `compute_last_session_datetime(..., max_hours_ago=744.0)` [31-day custom-frequency lookback] = `2026-08-26 18:00:00+00:00` -- the Aug 26 [terapeutka] session, correctly identified as the most recent past occurrence.
- `compute_last_session_datetime(..., max_hours_ago=30.0)` [the endpoint's narrow "did a session just happen" window] = `None` -- Aug 26 is roughly a week before "now", well outside 30 hours.

## 4. SessionDebrief / SessionPrepCard / BetweenSessionNote, 2026-08-20 onward (Darek)

**SessionDebrief** (id, session_date, created_at, updated_at, processing_status, input_type):

| id | session_date | created_at | processing_status |
|---|---|---|---|
| 3004 | 2026-08-20 18:31:58 | 2026-08-20 18:31:59 | COMPLETED |
| 3005 | 2026-08-20 18:32:21 | 2026-08-20 18:32:21 | COMPLETED |
| 3104 | 2026-09-02 18:23:21 | 2026-09-02 18:23:21 | COMPLETED |

**SessionPrepCard** (created_at >= 2026-08-20): one row, id 3037, `created_at=2026-08-21 09:14:54`, `session_date=None`, COMPLETED, not deleted.

**BetweenSessionNote** (created_at >= 2026-08-20): one row, id 4490, `created_at=2026-09-02 18:09:40`, COMPLETED, not deleted.

**Latest non-deleted SessionPrepCard overall (no date filter, for the `prep_done` boundary check):** most recent is still id 3037, `created_at=2026-08-21 09:14:54` -- there is **no prep card newer than Aug 21** anywhere in Darek's history (19 rows total go back to March; the full list was inspected and none postdate Aug 21).

**What this proves about the Aug 26 session's debrief:** there is a debrief-free gap between `2026-08-20 18:32` and `2026-09-02 18:23` -- i.e. **zero `session_debriefs` rows exist anywhere near 2026-08-26**. The two Aug 20 rows (23 seconds apart, likely a double-tap) line up with the *Aug 19, 10:00* custom session (submitted ~1.3 days late), not Aug 26. The single Sep 2 row (id 3104) is the only candidate for the Aug 26, 18:00 [terapeutka] session -- submitted **~7 days late** (`2026-09-02 18:23:21` minus `2026-08-26 18:00:00` = 7 days 0h23m), which matches the coordinator's own description of Darek's report ("about 6 days" late) almost exactly. **Conclusion: After Therapy for the Aug 26 session was in fact persisted to the backend -- just very late, and under one specific row (id 3104).** This is not a lost write; it is a matching-window problem, confirmed directly below.

## 5. What `/therapy-tracking/session-state` would return right now (pure functions only, not the live endpoint)

Reasoning strictly from the fetched rows plus the deployed `_debrief_matches_session`/`get_session_cycle_state` logic (read from `app/api/v1/endpoints/therapy_tracking.py`, current commit `072a25b`):

- `recent_occ` (30h window) = `None` -> the endpoint's first branch (`recent_occ_utc is not None and not recent_debrief_done` -> `debrief_cta`) does **not** fire. Too much time has passed since Aug 26 for "recently ended, no debrief yet" to trigger from a fresh computation today.
- `last_occ` (31-day window) = `2026-08-26 18:00:00+00:00`. Checking `debrief_done` against it: debrief id 3104 (`2026-09-02 18:23:21+00:00`) is `>= session_utc` (Aug 26 18:00) -- under the **currently deployed** (CS-01-fixed, no-ceiling) matching rule this **matches**, so `debrief_done = True` for this cycle.
- `prep_done`: boundary = `last_occ_utc` = Aug 26 18:00. The latest prep card overall is id 3037, `created_at = 2026-08-21 09:14`, which is **before** the boundary -> `prep_done = False`.
- State chain: `recent_occ_utc is None` (skip debrief_cta) -> `not prep_done` is `True` -> **state = `"prep_cta"`**.

So the pure backend computation, run fresh today, would **not** reproduce "stuck on session ended" -- it would say "time to prep for your Sept 4 session." This is consistent with the debrief for Aug 26 having actually landed (id 3104) and the ceiling that used to block that match having been removed in this exact deploy (commit `48ffdbc`, "remove 48h ceiling from debrief-match (MSV3.13 CS-01)").

**Critical caveat, read directly from the CS-01 commit message itself:** *"This endpoint has no callers in the Flutter app today (the Main card uses its own client-side implementation, fixed separately on the FE branch) -- this is a consistency fix, not the user-visible one."* In other words, `/therapy-tracking/session-state` is not what renders Darek's "Your Session" card at all -- the card is driven by the Flutter client's own local reimplementation of this same matching logic (`debriefMatchesSession` in `main_tab_cubit.dart`). The backend fix computed above is real and correct, but it cannot by itself un-stick Darek's card unless the equivalent 48h-ceiling removal has also shipped to a build he is running. This was not verified in this pass (it is a Flutter-side file, out of this agent's scope) -- see handoff below.

## 6. CS-02 population sizing

Skipped per the coordinator's message -- already captured pre-migration: 2 users had a `custom_interval_days` value (both `frequency=custom`, both with a future manual date already on file), 29 users have `frequency='custom'` overall. Not re-queried (the column no longer exists to re-check against).

## 7. Stale `next_session_date` signal (more than 7 days in the past, schedule or custom sessions still on file)

```sql
SELECT count(*) FROM user_preferences
WHERE next_session_date IS NOT NULL
  AND next_session_date < now() - interval '7 days'
  AND (therapy_schedule IS NOT NULL OR custom_therapy_sessions IS NOT NULL);
```

**Count: 5 users.**

| user_id | next_session_date |
|---|---|
| GaASKCUCocbIwuNk6rnI63dDTqY2 | 2026-07-26 08:40:00+00:00 |
| 5qaBI5YbxqOCco2o95sa0CaLnoj1 | 2026-08-18 19:00:00+00:00 |
| Zqxm5U7PedekTnKE311seuJmSiB2 | 2026-08-24 10:00:00+00:00 |
| B9MrjTOGytUmaoPnIuNrFx5zPoU2 | 2026-08-24 10:00:00+00:00 |
| g93ZoQZIXCb69SgvgcTRxBBpUMT2 | 2026-08-26 16:45:00+00:00 |

n=5 is below the 25-user k-anonymity floor for any aggregate/segment claim, but these are bare user_id + timestamp pairs requested explicitly by the coordinator for direct bug triage, not a demographic segment -- reported as asked. Note Darek's own row is **not** in this list: his persisted `next_session_date` (`2026-09-04`) is in the future, so he doesn't trip this particular staleness check even though his card was stuck -- confirming this signal and the CS-01 debrief-matching bug are two independent things, not the same root cause.

## Second account (`<UID-2>`, "[testerka K]") -- brief

- `frequency=custom`, `time_zone=UTC-5` (same tz-fallback-to-UTC bug applies: `parse_timezone` would give `FixedOffset(-300)`, the app gives plain UTC).
- `custom_therapy_sessions`: 2026-05-20 11:00, 2026-07-01 12:45, 2026-08-26 01:45 "[testerka K]".
- `next_session_date` persisted = `None`.
- Recompute: `next_occ = None` (no future date on file), `last_occ` (31-day window) = `2026-08-26 01:45:00+00:00`, `recent_occ` (30h) = `None`.
- No anomaly beyond "no future session scheduled," which is the correct, expected state for someone whose last calendar date has passed with nothing new added. Consistent with the coordinator's guess that this is a different, unrelated tester account -- no further action indicated.

## What this means for FE vs BE

**Observation (directly from the data above):**
- The Aug 26 After Therapy debrief for Darek's session **was persisted** to `session_debriefs` (id 3104), just ~7 days late.
- The backend's own matching rule that used to reject a debrief that late (a 48-hour ceiling) has already been removed in this exact deploy (v548 / commit `48ffdbc`).
- Recomputing the state machine fresh, right now, from the pure functions yields `"prep_cta"`, not the stuck `"debrief_cta"`/"session has ended" Darek reported.
- `UserPreferences.time_zone` values in the offset-string form (`"UTC+2"`, `"UTC-5"`) are silently downgraded to plain UTC by both therapy-schedule read paths, a distinct, confirmed 2-hour skew in Darek's persisted `next_session_date` that is stable (doesn't drift further) but is real and separately worth fixing.

**Inference (not directly observed, flagged as such):**
- The commit message for the backend fix states plainly that `/therapy-tracking/session-state` "has no callers in the Flutter app today" and that the Main card uses its own client-side match logic, "fixed separately on the FE branch." This agent did not read the Flutter code, so it cannot confirm whether that client-side fix has shipped to a build Darek is running. **If it has not**, Darek's card will keep showing "Session has ended" indefinitely even though the backend and the (unused) endpoint now agree the debrief matches -- because the client never asks the backend for this state at all; it computes it locally from the same debrief rows using its own (possibly still-ceilinged) logic.
- This is the single open question that decides whether CS-01 is actually fixed for Darek: **is the Flutter-side `debriefMatchesSession` 48h-ceiling removal in a build he has, or still pending?**

## Handoff

- **To backend-api / flutter-mobile / integration-devops (via the lead):** confirm whether the client-side `debriefMatchesSession` fix (mirroring commit `48ffdbc`) has shipped and to which TestFlight build; if not, that is the actual blocker for Darek, not anything server-side. Ask Darek to reopen the app once that build is confirmed live and report whether the card advances.
- **To backend-api:** the `pytz.timezone()`-without-offset-support bug in `app/api/v1/endpoints/therapy_tracking.py:302` and `app/crud/crud.py`'s `get_therapy_schedule_with_frequency` should call `app.utils.time_utils.parse_timezone()` instead, which already handles `"UTC±H[:MM]"` strings correctly. Confirmed impact: any user whose `time_zone` is stored as an offset string (not an IANA name) gets a silent, stable 2-5+ hour skew in their computed/persisted therapy-schedule times. Prevalence across the user base was not sized in this pass (would need one more bounded `LIKE 'UTC%'` count query) -- available as a fast follow-up if wanted.
- **To the lead:** the stale-`next_session_date` signal (5 users, listed above) is unrelated to Darek's specific bug (his own `next_session_date` is not stale) -- worth a separate look if it's on the radar, but not part of CS-01's root cause.

## Revision history

- 2026-09-03 (first pass): blocked before any query ran -- Heroku CLI credentials were dead (`heroku auth:whoami` -> `Invalid credentials provided`). See prior report content (superseded) and agent memory `reference_heroku_dyno_access_recipe.md` for the diagnosis.
- 2026-09-03 (this pass): access restored, confirmed via `heroku auth:whoami`; full evidence collected as above.
