# KE team-account backfill sizing (2026-10-19)

**Question.** Two internal team accounts, "A (operator)" and "B (Darek)": what is their KE (Character tab) state on prod right now, and how much source data would a full-history KE read have to process for them?

**Method.** One read-only one-off dyno run (run.5656, `heroku run --no-tty`, Heroku v576 = code 73081cc). Every query ran in its own `READ ONLY` transaction with a 60 s timeout and was rolled back. Nothing was written. Account A was matched by a SHA-256 hash of the sign-in email (exact form, `+alias` and dotless forms) so the address never appeared in the script or the output. A Sign in with Apple private-relay account cannot be matched that way. One account matched. Account B was matched by its known UID. The UIDs went to the lead in the session and are not in this file.

Privacy: counts, dates and flags only. No entry text, no emotion families, no crisis data. `ke_user_state.latest_entry_crisis` and the `crisis_at` cursor key were deliberately not read: a per-person crisis read is out of bounds, and the crisis window does not change how many entries there are.

## 1. Premium, consent, switches

| | A (operator) | B (Darek) |
|---|---|---|
| Account created | 2024-12-20 | 2024-12-19 |
| Last USER message | 2026-10-15 | 2026-10-09 |
| `user_subscription` | is_active false, granted_via purchase, ended 2026-10-16 | is_active false, granted_via purchase, ended 2026-10-09 |
| **Premium now** (`is_user_premium`, called live and recomputed in SQL) | **No** | **No** |
| ARTICLE9_HEALTH (latest record) | active | active |
| PROFILING (latest record) | no record | active |
| Blocked by PROFILING (opt-in off on prod) | no | no |
| `is_enabled_for` (CHARACTER_KE_ENABLED=true) | yes | yes |

Prod settings read from the running code: `CHARACTER_KE_REQUIRE_PROFILING_OPT_IN` false, `KE_DAILY_CALL_CAP` 60 (default), `BACKFILL_DAYS` 90, `ENTRIES_PER_JOB` 15.

## 2. `ke_user_state`

| | A | B |
|---|---|---|
| Row exists | yes | yes |
| activated_at (UTC) | 2026-10-19 12:56:58 | 2026-10-19 13:46:49 |
| last_opened_at | same instant as activation | same instant as activation |
| backfill_done_at | same instant as activation | same instant as activation |
| initial_sync_done | true | true |
| last_composed_at | NULL | NULL |
| updated_at | equal to created_at (row never rewritten) | equal to created_at (row never rewritten) |
| source_counts | NULL | NULL |
| `read_plan` | 2 (forward only) | 2 (forward only) |
| `fwd_from` | the activation instant | the activation instant |
| Source cursor keys present | reflect_talk, note, after_therapy, session, realization | reflect_talk, note, after_therapy, session, realization, todo_done |
| `hist_*`, `hist_done` | absent | absent |
| Among the 23 of the premium backfill | **no** | **no** |

**Neither account was activated by the premium backfill.** That run activated 23 people in the same second (2026-10-19 11:53:26 UTC, none of whom has opened the tab since). A and B are in the other 5 states: they opened the tab themselves about one and two hours later. They were not premium, so `sheet.record_open` gave them the forward-only plan. Every source cursor was set to the newest row created before the activation, and the empty forward read was marked done on the spot.

**KE jobs.** Not recorded per person by design: RQ results are not kept (`result_ttl=0`) and the job log line carries no user id. What the data does show: the state row was never rewritten after its creation, there are no KE model calls for either person, and there is no entry after either cursor. So no job has read anything for them. With `backfill_done_at` set, no new rows and premium false, the sweep will not pick them again until they write something new.

Fleet context: 28 state rows (23 from the backfill plus 5 tab opens). 26 have finished the first read. Since the rollout, 98 `ke_extract` calls for 13 people and 4 `ke_compose` calls have been made, for $0.26.

## 3. KE output so far

| Table | A | B |
|---|---|---|
| ke_paths | 0 | 0 |
| ke_skills | 0 | 0 |
| ke_tools | 0 | 0 |
| ke_hard | 0 | 0 |
| ke_moments | 0 | 0 |
| ke_ideas | 0 | 0 |

The composed map is not a table (it is computed on read from these tables plus a hash in `ke_user_state`). `last_composed_at` is NULL for both.

## 4. Source entries KE reads

The readers' own filters are applied: soft-deleted rows are excluded, and only realizations the person tagged are counted. Ages are by `created_at` (by `completed_at` for to-dos), the same column the reader's floor uses. "Ready" means the text column KE would send is non-empty ciphertext. That is an upper bound: an entry whose text decrypts to nothing, a crisis entry, or a repeat to-do inside 6 days is skipped without a model call.

**A (operator)**

| Source | Total | 0-90 d | 90-180 d | 180-365 d | >365 d | Oldest |
|---|---|---|---|---|---|---|
| reflect_talk (conversation_summaries) | 110 | 15 | 1 | 7 | 87 | 2025-01-09 |
| note | 6 | 0 | 2 | 4 | 0 | 2026-03-05 |
| after_therapy (Art. 9) | 4 | 1 | 0 | 3 | 0 | 2026-03-05 |
| session (Art. 9) | 4 | 0 | 3 | 1 | 0 | 2026-04-02 |
| realization | 0 | | | | | |
| todo_done | 0 | | | | | |
| **Total** | **124** | **16** | **6** | **15** | **87** | |

**B (Darek)**

| Source | Total | 0-90 d | 90-180 d | 180-365 d | >365 d | Oldest |
|---|---|---|---|---|---|---|
| reflect_talk (conversation_summaries) | 164 | 7 | 1 | 19 | 137 | 2025-01-13 |
| note | 30 | 16 | 5 | 9 | 0 | 2026-03-05 |
| after_therapy (Art. 9) | 30 | 12 | 12 | 6 | 0 | 2026-03-27 |
| session (Art. 9) | 2 | 2 | 0 | 0 | 0 | 2026-09-25 |
| realization | 6 | 6 | 0 | 0 | 0 | 2026-07-22 |
| todo_done (20 of them therapist homework, Art. 9; 10 on repeating items) | 34 | 32 | 2 | 0 | 0 | 2026-07-20 |
| **Total** | **266** | **75** | **20** | **34** | **137** | |

Every row was "ready" by the presence check. Against the KE floor (activation minus 90 days = 2026-07-21): A has 16 rows inside the 90-day window and 108 older; B has 75 inside and 191 older. **All 390 rows sit at or below the forward cursors**, so nothing is pending, the 90-day window included. Both people have ARTICLE9_HEALTH active, so the therapy rows would be read.

Also note that A has 120 conversations but 110 summaries, and B has 191 conversations but 164 summaries. The conversations without a `conversation_summaries` row are invisible to KE (known gap, see 2026-10-19-ke-backfill-sizing.md).

## 5. Today's model calls vs the cap

| | A | B |
|---|---|---|
| Redis counter `ke:calls:<uid>:2026-10-19` (read with MGET, nothing incremented) | no key = 0 of 60 | no key = 0 of 60 |
| `token_usage_log` ke_extract / ke_compose, last 7 days | 0 | 0 |

## 6. Size of a full-history read

How `extract.py` batches: one model call per ready entry. A job takes at most `ENTRIES_PER_JOB` = 15 ready entries, oldest first across the six sources; skipped rows do not count toward the 15. Compose (1 call) runs only after a job that caught up. The cap is 60 calls per person per UTC day, counted before each call. The sweep runs every 30 min and starts at most one job per person per tick (Redis claim).

| | A | B |
|---|---|---|
| Ready entries, full history (upper bound) | 124 | 266 |
| of which older than the 90-day window | 108 | 191 |
| Extraction jobs of 15 | 9 | 18 |
| Model calls (extract + 1 compose) | about 125 | about 267 |
| UTC days at cap 60 | 3 (60 + 60 + 5) | 5 (4 x 60 + 27) |
| Minimum wall time without the cap (1 job per 30-min tick) | about 4.5 h | about 9 h |
| Cost at today's $0.0025 per extract call | about $0.31 | about $0.66 |

## Findings and handoffs

1. **Both accounts lost premium before today, so KE treats them as forward-only.** A's purchase ended 2026-10-16 and B's ended 2026-10-09. Both have `is_active` false. Even the 90-day history is not being read for them, and no job will do anything until they write new entries.
2. **The backfill cannot be done by lowering a floor alone.** The forward cursors already sit at the newest row of every source, and the readers use `id > cursor`, so older rows are never read again. The only history path in the code is the `hist_*` read in `history.plan_read`. It runs only when the person is premium, and it covers only `BACKFILL_DAYS` (90) before `fwd_from`. Granting premium would reach A's 16 and B's 75 entries, but not the 108 and 191 older ones. **Owner `backend-api`:** a full-history read for named accounts needs a code path. Two options: (a) an operator-run, allowlisted one-off that seeds `hist_done=0` with empty `hist_*` cursors and makes `plan_read` use an epoch or explicit floor for these accounts, ignoring the premium check; (b) a per-state floor override key in `cursors`. It also needs `backfill_done_at` and `initial_sync_done` reset (`_restart_silently`), so the sweep picks the account and the history does not replay as live stage-ups. Keep it dry-run by default and limited to these two UIDs.
3. **The cap decides the pace.** At 60 calls a day, A takes 3 UTC days and B takes 5. "Processed now" requires a temporary cap exception for the two accounts (config or code, `backend-api` / operator). Even then the 30-minute sweep cadence means about 4.5 h and 9 h, unless the one-off runs the jobs back to back itself.
4. **A has no PROFILING record.** That is harmless while `CHARACTER_KE_REQUIRE_PROFILING_OPT_IN` is false. If opt-in is switched back on, A would be blocked and would lose processing.
5. Most of the history is old Reflect talk summaries from 2025: 87 of A's 124 entries and 137 of B's 266 are more than a year old. The therapy sources are all from 2026.
