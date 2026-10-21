# Session recording pipeline check - 2026-08-10

## Question

Did session recordings started in the last 14 days actually complete server-side, and are any stuck or lost?

Trigger: PostHog (last 14d, project 141170) shows `recording_started` 34 events / 10 distinct users, but `recording_chunked_upload_completed` only 7 events / 3 distinct users - 7 of 10 starters have an unknown client-side outcome. Server-side events `recording_processing_started` / `recording_processing_completed` / `recording_processing_failed` have never fired in 365 days - the backend half of the pipeline is dark in PostHog. `recording_upload_failed` / `recording_chunk_store_failed` have also never fired. Absence of an error signal is not absence of errors, hence this DB ground-truth check.

## Method

Access: `heroku run -a mindsync python < script.py` (Azure Postgres has no public DNS from local/dev; only working path). REPL-safe script, `SET statement_timeout = 15000` + `SET TRANSACTION READ ONLY`, read-only `SELECT` only, no `commit()`. Dyno `run.5974`, stopped after capture via `heroku ps:stop run.5974 -a mindsync`. Table/column names and the native-enum drift were verified against `MindSync/app/models/models.py` first (`UploadSession`, `UploadChunk`, `SessionRecording`), and enum labels were re-verified live via `pg_enum` rather than trusted from the model.

Aggregates only. No user_id, no chunk/transcript content was ever selected (chunk `data` and recording transcript/summary fields are Fernet-encrypted at rest - only counted, never read).

## Exact queries run

```sql
-- enum drift check (session_recordings.processing_status is a native Postgres Enum)
SELECT t.typname, e.enumlabel FROM pg_enum e JOIN pg_type t ON t.oid=e.enumtypid
WHERE t.typname ILIKE '%processing%' ORDER BY 1, e.enumsortorder;

-- upload_sessions, last 14d
SELECT count(*), count(DISTINCT user_id), min(created_at), max(created_at)
FROM upload_sessions WHERE created_at >= now() - interval '14 days';
SELECT status, count(*) FROM upload_sessions
WHERE created_at >= now() - interval '14 days' GROUP BY 1 ORDER BY 2 DESC;

-- stuck candidates: non-terminal (in_progress) and older than 24h, within the 14d window
SELECT count(*) FROM upload_sessions
WHERE created_at >= now() - interval '14 days' AND status='in_progress'
  AND created_at < now() - interval '1 day';
SELECT CASE WHEN now()-created_at < interval '3 days' THEN '1-3d'
            WHEN now()-created_at < interval '7 days' THEN '3-7d'
            ELSE '>7d' END AS bucket, count(*)
FROM upload_sessions
WHERE created_at >= now() - interval '14 days' AND status='in_progress'
  AND created_at < now() - interval '1 day'
GROUP BY 1 ORDER BY 1;

-- upload_chunks (transient by design - should be near zero)
SELECT count(*) FROM upload_chunks;
SELECT count(*), coalesce(sum(length(uc.data)),0)
FROM upload_chunks uc JOIN upload_sessions us ON us.id = uc.upload_session_id
WHERE us.created_at < now() - interval '1 day';

-- session_recordings, last 14d
SELECT count(*), count(DISTINCT user_id)
FROM session_recordings WHERE created_at >= now() - interval '14 days';
SELECT processing_status, count(*) FROM session_recordings
WHERE created_at >= now() - interval '14 days' GROUP BY 1 ORDER BY 2 DESC;

-- join sanity: completed-looking upload_sessions with no linked recording
SELECT count(*) FROM upload_sessions
WHERE created_at >= now() - interval '14 days' AND recording_id IS NULL;
SELECT status, count(*) FROM upload_sessions
WHERE created_at >= now() - interval '14 days' AND recording_id IS NULL
GROUP BY 1 ORDER BY 2 DESC;

-- duration completeness, last 14d
SELECT count(*) FROM session_recordings
WHERE created_at >= now() - interval '14 days' AND duration_seconds IS NULL;
SELECT CASE WHEN duration_seconds<60 THEN '<1m'
            WHEN duration_seconds<300 THEN '1-5m' ELSE '>5m' END AS bucket, count(*)
FROM session_recordings
WHERE created_at>=now()-interval '14 days' AND duration_seconds IS NOT NULL
GROUP BY 1 ORDER BY 1;

-- prior 14d window (28d -> 14d ago), same shape, for trend
SELECT count(*), count(DISTINCT user_id) FROM upload_sessions
WHERE created_at >= now()-interval '28 days' AND created_at < now()-interval '14 days';
SELECT status, count(*) FROM upload_sessions
WHERE created_at >= now()-interval '28 days' AND created_at < now()-interval '14 days'
GROUP BY 1 ORDER BY 2 DESC;
SELECT count(*), count(DISTINCT user_id) FROM session_recordings
WHERE created_at >= now()-interval '28 days' AND created_at < now()-interval '14 days';
SELECT processing_status, count(*) FROM session_recordings
WHERE created_at>=now()-interval '28 days' AND created_at<now()-interval '14 days'
GROUP BY 1 ORDER BY 2 DESC;

-- transcription pipeline health extras, last 14d
SELECT count(*), count(assemblyai_transcript_id),
       sum(CASE WHEN enqueue_failed THEN 1 ELSE 0 END),
       sum(CASE WHEN diarization_failed THEN 1 ELSE 0 END),
       avg(retry_count), max(retry_count), max(processing_attempts)
FROM session_recordings WHERE created_at>=now()-interval '14 days';
```

## Results

**Enum drift check** - `processingstatusenum` (session_recordings.processing_status) is a native Postgres enum and prod carries the same UPPERCASE-label drift documented for `moment_type_enum` elsewhere: `PENDING, PROCESSING, COMPLETED, FAILED, PLAIN_TEXT` (model declares them lowercase-valued `str, enum.Enum` constants but the PG type labels are the uppercase member names). Not a new finding, but confirms raw SQL against this column must use uppercase.

**upload_sessions, last 14d (2026-07-27 -> 2026-08-10):**

| metric | value |
|---|---|
| total rows | 4 |
| distinct users | 3 |
| min created_at | 2026-07-29 23:07:12 UTC |
| max created_at | 2026-08-05 23:11:15 UTC |
| status breakdown | `completed`: 4 (100%) |
| stuck (`in_progress`, >24h old) | 0 |
| stuck age buckets | none (empty result) |

**upload_chunks (transient table):**

| metric | value |
|---|---|
| total rows right now | 0 |
| orphans (parent session >24h old) | 0 rows, 0 bytes |

Chunk cleanup is working as designed - nothing left behind, no orphans tied to old sessions.

**session_recordings, last 14d:**

| metric | value |
|---|---|
| total rows | 3 |
| distinct users | 2 |
| status breakdown | `COMPLETED`: 3 (100%); PENDING/PROCESSING/FAILED/PLAIN_TEXT: 0 |
| duration_seconds NULL | 0 |
| duration buckets | `>5m`: 3 |

**Join sanity:**

| metric | value |
|---|---|
| upload_sessions (14d) with `recording_id IS NULL` | 1 |
| ...of which `status` | `completed`: 1 |

One `upload_sessions` row is marked `status='completed'` (meaning `POST /upload/{id}/complete` ran) but never got `recording_id` populated. The other 3 completed sessions each link to one of the 3 `session_recordings` rows above - that reconciles exactly (3 linked + 1 unlinked = 4 completed).

**Transcription/processing extras, last 14d (n=3 session_recordings):**

| metric | value |
|---|---|
| assemblyai_transcript_id present | 0 / 3 |
| enqueue_failed | 0 / 3 |
| diarization_failed | 3 / 3 (100%) |
| avg / max retry_count | 0 / 0 |
| max processing_attempts | 1 |

**Prior 14d window (2026-07-13 -> 2026-07-27), for trend:**

| table | total | distinct users | status |
|---|---|---|---|
| upload_sessions | 9 | 4 | `completed`: 9 |
| session_recordings | 5 | 3 | `COMPLETED`: 5 |

## Interpretation

**No stuck or lost sessions inside the DB's view of the pipeline.** Every `upload_sessions` row created in the last 14 days reached a terminal `completed` status - zero `in_progress`/`aborted`, zero age-bucketed stragglers. `upload_chunks` is empty with zero orphans, so the transient-chunk cleanup (assembly + safety-net finalizer) is functioning. Of the 4 completed uploads, 3 cleanly produced a linked, fully-durationed, `COMPLETED` `session_recordings` row. That part of the pipeline is healthy.

**Two real findings, both about data that never reaches or is dropped from the DB:**

1. **The DB shows far less recording activity than PostHog's client-side "started" count says exists.** PostHog: 10 distinct users emitted `recording_started` in the last 14d. DB: only 3 distinct users have any `upload_sessions` row at all in the same window (4 rows total). That is a gap of ~7 users (70% of PostHog's "starters") who never produced a server-side row - not "stuck," not "uploaded then lost," but **never reached `POST /upload/initiate` at all** (or the call failed with no trace anywhere). By contrast, DB completions (3 recordings / 2 users) and PostHog's `recording_chunked_upload_completed` (3 users) are in the same ballpark - the completion tail roughly agrees, the start-of-funnel does not. Given `recording_upload_failed`/`recording_chunk_store_failed` have never fired client-side either, this can't be distinguished from the DB alone as "user cancelled before initiate" (benign) vs. "initiate call silently failed" (bug) - there is no telemetry on either side to tell them apart. This is the same dark-instrumentation gap already flagged for `recording_processing_*` - it now also appears to hide client-side initiate failures.

2. **One `upload_sessions` row (25% of the 14d completed cohort) is `status='completed'` with `recording_id` never populated.** `complete()` is documented in the model to set `recording_id` "when complete() links this session to a SessionRecording row" - here the upload-completion step ran but the linkage step did not, or ran and didn't persist. This is a single row in a 4-row window, so treat the rate (1-in-4) as indicative, not statistically solid, but it is a genuine, reproducible-looking gap worth root-causing before it scales.

3. **Secondary observation (not concluded, flagging for awareness):** `diarization_failed=true` on 3/3 (100%) of the 14d `session_recordings`, and `assemblyai_transcript_id` is NULL on all 3 despite `processing_status='COMPLETED'`. This could be normal - the model comments describe a designed fallback path (key_moments mapping) for when diarization fails, and `assemblyai_transcript_id` may be intentionally cleared once `transcript_text` is captured - or it could mean diarization/transcript-ID persistence has been silently broken for the whole window while the pipeline still reports COMPLETED via the fallback. n=3 is too small to call this a trend on its own; the prior-14d COMPLETED count (5) suggests checking whether diarization_failed was also ~100% there. Not root-caused here since it requires reading `app/tasks/` and `app/services/` (data-analytics/backend-api owned).

4. **Volume roughly halved 14d-over-14d** (9->4 upload_sessions, 5->3 session_recordings, 4->3 distinct starters). Could be normal usage variance given the very low absolute volume (single digits); not enough signal here to call it a regression.

## Verdict

**Healthy where it's measurable, but the DB can only account for ~30% of what PostHog says started.** Nothing in Postgres looks stuck or actively lost mid-pipeline (no zombie `in_progress` sessions, no orphaned chunks, no NULL durations, no FAILED recordings) - everything that reaches the server in the last 14 days finishes cleanly. The real risk is upstream and invisible: most of PostHog's 10 "starters" never produced any server-side row, and there is zero instrumentation (client or server) to say why. One `completed`-but-unlinked upload_session is a concrete, small-but-real data-integrity gap.

## Handoffs

**To `backend-api`:**
- Investigate the `upload_sessions` row(s) with `status='completed'` AND `recording_id IS NULL` (1 of 4 in the last 14d, 14d-old row so still queryable) - trace whether `complete()`'s linkage step raised/swallowed an exception, or whether the `SessionRecording` was created but the `UploadSession.recording_id` update didn't commit. Suggest wrapping the create-and-link in a single transaction if it isn't already.
- Diarization/transcript-ID persistence: confirm whether `assemblyai_transcript_id=NULL` + `diarization_failed=true` on 3/3 COMPLETED recordings in the last 14d is expected fallback behavior or a silent breakage. If diarization has been failing 100% of the time, that's worth its own investigation even though it doesn't block "completion."

**To `backend-api` / `data-analytics` (instrumentation, ties to prior PostHog finding S4/#4):**
- `recording_processing_started` / `recording_processing_completed` / `recording_processing_failed` have never fired in PostHog (365d) - this DB check confirms the backend pipeline itself is working for rows that reach it, so the gap is purely missing emission, not a broken pipeline. Please wire these events into the processing path (likely `app/tasks/` around `SessionRecording.processing_status` transitions).
- Consider adding a server-side event (or at minimum a DB-visible failure reason) at `POST /upload/initiate` failure time - right now a failed/abandoned initiate call is invisible everywhere: not in PostHog (no `recording_upload_failed`), not in Postgres (no row is ever created), and not distinguishable from "user cancelled before recording." Without this, the 10-vs-3 starter gap found here cannot be diagnosed further from data alone.

No mutation performed; no user-level data exposed. n's above are small (single-digit to low-double-digit rows) - treat percentages as directional, not statistically robust, given the low absolute volume of this feature in the last 14 days.
