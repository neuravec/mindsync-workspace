## Security Audit Report — MSV3.3 Batch (23 items, both repos) — 2026-08-14

Scope: uncommitted working-tree diffs only (`git diff` / `git status`), not the whole codebase.
- Backend: `C:\Users\mikol\Notebooks\MindSync\Heroku\MindSync` (branch main, HEAD 67b1bdc + ~30 modified files + 3 new migrations)
- Frontend: `C:\Users\mikol\Notebooks\MindSync\Heroku\mindsync-frontend` (branch dev, HEAD 34f2af9 + ~94 modified files)

### Executive Summary

The batch is well-engineered from a horizontal-privilege-escalation standpoint: every endpoint and CRUD read/write touched in this diff (weekly/monthly summary generate+retry, `/moments/upcoming`, the two new `therapist_questions` columns, the therapy-schedule resolver) scopes strictly to `current_user_id` derived from a verified Firebase token, and no user-controlled ID is trusted for data ownership anywhere in the diff. Encryption-at-rest is consistent for all newly-added encrypted columns. GDPR cascade-delete coverage is intact for every new column (all live on tables with `ondelete="CASCADE"` FKs to `users`, unchanged by this batch). Dead-route cleanup (CS-19/CS-21) removes several "Page Not Found" traps without introducing any cross-user identifier leakage.

One **High** finding blocks deployment of the CS-23 piece as currently written: moving weekly/monthly summary generation to an RQ background job (correctly, to avoid the H12 router-timeout problem) also moved the **already-decrypted** therapy content (debrief notes, prep-card content, recording overviews, between-session notes, realizations, journal/reflect summaries) into the RQ job payload, which Redis now stores in plaintext. This is a deviation from this codebase's own established pattern — every other RQ job in the repo (RAG indexing, conversation analysis, realization detection) passes only IDs and re-fetches+decrypts inside the worker. No other Critical or High findings were found in the reviewed diff.

### Critical Findings

None found in the reviewed diff.

### High Findings

#### HIGH-001: CS-23 async summary jobs pass already-decrypted mental-health content through Redis, breaking the codebase's own ID-only job pattern
- **Severity**: High
- **Location**:
  - `MindSync/app/api/v1/endpoints/weekly_summaries.py` — `generate_weekly_summary()` (enqueue call ~line 288-298) and `retry_weekly_summary()` (enqueue call ~line 508-518)
  - `MindSync/app/api/v1/endpoints/monthly_audits.py` — `generate_monthly_audit()` (enqueue call ~line 502-517) and `retry_monthly_audit()` (enqueue call ~line 651-666)
  - `MindSync/app/tasks/weekly_therapy_summary.py::run_weekly_summary_ai_job()` (signature: `summary_id, user_id, data: dict, therapy_context: str, ...`)
  - `MindSync/app/tasks/monthly_therapy_audit.py::run_monthly_audit_ai_job()` (same shape)
  - `MindSync/app/core/rq_queue.py` (default `Queue(connection=redis_client)`, no serializer override → RQ's default pickle serializer)
  - `MindSync/app/core/redis.py` — `Redis.from_url(os.getenv("REDISGREEN_URL"))`, scheme not enforced in code
- **Description**: Before this batch, `generate_weekly_therapy_summary()` / `generate_monthly_therapy_audit()` ran synchronously inside the request; the decrypted `data` dict built by `crud.gather_weekly_summary_data()` (debrief `main_topics`/`emotional_tone`/`key_insights`, prep-card content, recording overview/action items/emotional arc, between-session notes, realizations, journal/reflect summaries — i.e. raw therapeutic content, explicitly `decode()`d before this call) lived only in application-process memory for the duration of one request. CS-23 correctly moves the OpenAI call off the request path to avoid Heroku's 30s H12 router timeout, but the endpoint now does `rq_queue.enqueue(run_weekly_summary_ai_job, summary.id, current_user_id, data, therapy_context, user_pronouns, user_language, window_days, ...)` — the full decrypted `data` dict and `therapy_context` string are passed as job **arguments**. RQ's default job serializer is `pickle`; job args are stored as a Redis hash (`rq:job:<id>`) until the job's `result_ttl`/`failure_ttl` expires (RQ defaults: ~500s after a successful run with no explicit override; these enqueue calls set `job_timeout=600` but do not set `result_ttl`/`failure_ttl`). This means plaintext crisis disclosures and emotional-pattern content — the single most sensitive data class this app holds — now transits and briefly rests in Redis, a shared piece of infrastructure whose TLS-in-transit and encryption-at-rest posture is not verified or enforced anywhere in this diff (`os.getenv("REDISGREEN_URL")` is passed straight to `Redis.from_url()` with no scheme check).

  This is a clear regression from the codebase's own established secure pattern. Every other background job touched by or adjacent to this batch takes only IDs and re-fetches + re-decrypts inside the worker: `rq_queue.enqueue(index_weekly_therapy_summary_to_rag, summary.id, user_id)`, `rq_queue.enqueue(index_conversation_summary_to_rag, conversation_summary.id, user_id)`, `rq_queue.enqueue(run_conversation_analysis, open_conv.id, user.id)`, `rq_queue.enqueue(index_realization_to_rag, realization.id, user_id)`. `run_weekly_summary_ai_job`/`run_monthly_audit_ai_job` are the only jobs in this diff (and, on this pass, in the codebase) that push bulk decrypted therapy content through the queue instead of a row ID.
- **Impact**: Anyone with read access to the RedisGreen instance (a compromised Redis credential, an insider with ops access, another add-on/service sharing the same Redis instance, or — if `REDISGREEN_URL` is ever non-TLS — a network position between the web/worker dynos and Redis) can read plaintext therapy content for the window between enqueue and TTL expiry, without needing database access or the app's field-level encryption key at all. This bypasses the "encrypted at rest" guarantee CLAUDE.md's own checklist asks for, for exactly the content class (`therapist_questions`, debrief/recording/prep-card content) this audit is asked to hold to the highest standard.
- **Reproduction / verification steps**: With `RQ_REDIS_URL` pointed at a test Redis, call `POST /api/v1/weekly-summaries/generate` for a user with debrief/prep-card history, then before the worker picks up the job run `redis-cli HGETALL rq:job:<id>` (or inspect the RQ `StartedJobRegistry`/`Queue` payload) — the job's serialized `data` args contain the plaintext (decoded) debrief/prep-card/recording text.
- **Remediation** (assign: **data-analytics**, coordinate with **backend-api** on the endpoint call sites and **integration-devops** on Redis TLS/network verification):
  1. **Preferred fix**: change `run_weekly_summary_ai_job`/`run_monthly_audit_ai_job` signatures to `(summary_id/audit_id, user_id, window_start, window_end, ...)` only, and have the job call `crud.gather_weekly_summary_data(db, user_id, window_start, window_end)` itself (re-decrypting inside the worker), mirroring every other job in this file and in `rag_indexing.py`/`conversation_analysis.py`. This also removes the (smaller) duplicate-decode cost concern and keeps the pattern uniform for the next engineer who copies this job as a template.
  2. If (1) is deferred for a later pass, at minimum before shipping: (a) confirm `REDISGREEN_URL` actually resolves to `rediss://` (TLS) in the Heroku config — this is exactly the CLAUDE.md "Background Jobs Security" checklist item ("Redis connection uses SSL") and it is unverified by this diff; (b) set an explicit short `result_ttl` (and `failure_ttl`, even though the current code never lets the job raise) on these two enqueue calls so any Redis-resident copy of the payload expires within minutes, not the RQ default; (c) confirm the RedisGreen instance is not shared with any component outside MindSync's own trust boundary.
  3. Either way, `database-administrator`/`integration-devops` should confirm no `rq-dashboard` or similar admin UI is exposed on this Redis instance (none was found in this repo's `requirements.txt`/`Procfile` during this audit, which is good — keep it that way).

### Medium Findings

None found in the reviewed diff.

### Low Findings

- **LOW-001 — `custom_sessions` has no server-side length cap (pre-existing, widened blast radius by CS-18).** `app/schemas/schemas.py::CustomTherapySession`/`TherapyScheduleUpdateRequest.custom_sessions` accepts an unbounded `List[CustomTherapySession]` from the client; `crud.update_therapy_schedule()` persists it verbatim as JSON with no size/count validation. This predates this batch (not introduced here), but CS-18 (`app/utils/therapy_schedule_utils.py`) newly wires this list into `compute_next_session_date`/`compute_last_session_datetime`, and per the task brief six notification generators now consume the resolver's output — so an unbounded list is iterated more places than before. Not exploitable for injection (ORM-parameterized, pure Python date math), but worth a backlog item: cap `custom_sessions` length (e.g. 100) at the Pydantic layer for resource-exhaustion hardening. Owner: backend-api (schema owner for `users.py`'s therapy-schedule endpoint, out of this batch's file scope).
- **LOW-002 — Share-export temp JPEG is never explicitly deleted (pre-existing pattern, unchanged by CS-22).** `mindsync-frontend/mindsync_app/lib/utils/card_share_util.dart::shareWithBranding()` writes the rendered card to `getTemporaryDirectory()/${config.filename}.jpg` and hands it to `Share.shareXFiles()`, but never deletes the file afterward — it relies on the OS purging the app's temp directory. This is unchanged from the prior PNG-based implementation (not a regression introduced by CS-22's JPEG/`captureFromLongWidget` rework), but given the file's content is a therapy-card export, explicit cleanup (`file.delete()` after the share sheet resolves, in a `finally`) would be a reasonable hardening step for a mental-health app. Owner: flutter-mobile.
- **LOW-003 — Migration `kk2l3m4n5o6p` follow-up is a manual, log-watching process, not an automated gate.** The migration correctly refuses to add `uq_weekly_summary_user_period` when duplicate `(user_id, data_window_end)` rows already exist on prod, logging a warning instead of failing — this is the *right* failure mode (no silent corruption, no aborted migration chain) and is not a code defect. Flagging only as a process note: nothing currently alerts a human to that warning automatically. Recommend `database-administrator` run the duplicate-row check proactively right after this migration deploys, rather than waiting to notice the log line. Owner: database-administrator (follow-up task, not a code fix).

### GDPR Compliance Status

| Requirement | Status | Notes |
|-------------|--------|-------|
| Right to erasure | OK | New columns (`session_debriefs.therapist_questions`, `session_recordings.therapist_questions`, `notification_moments.push_delivered`) all live on tables whose `user_id` FK already has `ondelete="CASCADE"` (unchanged by this batch, verified in `app/models/models.py` and `app/models/notification_moment.py`) — no new deletion gap introduced. |
| Data minimization | OK, with the HIGH-001 caveat | No new PII fields collected beyond what's functionally needed (therapist questions are a direct feature requirement). The concern is *where the existing decrypted data now transits* (Redis), not new collection — see HIGH-001. |
| Right to portability | Not assessed | Not touched by this diff; out of scope for this pass. |
| Consent for processing | Not assessed | No consent-flow files appear in this diff. |
| Data encryption at rest | Conditional pass | All newly-added encrypted-content columns (`therapist_questions` ×2, widened `emotional_temperature`) are consistently `encode()`d before persistence and `decode()`d on read — verified in `app/tasks/session_recording.py:145`, `app/api/v1/endpoints/debriefs.py:312-314`, `app/api/v1/endpoints/prep_cards.py:370-372`. However, the *same content* now also passes through Redis in plaintext during CS-23's async generation window (HIGH-001) — the DB-at-rest guarantee is intact, but a new unencrypted-in-transit/at-rest copy exists outside the database. |
| Retention policy | Not assessed | Not touched by this diff. |

### Horizontal Privilege Escalation Audit

All endpoints and CRUD functions touched in this diff were checked for user-scoping. None found vulnerable.

| Endpoint / function | Scoping mechanism | Verdict |
|---|---|---|
| `POST /weekly-summaries/generate`, `POST /weekly-summaries/{id}/retry` | `current_user_id = Depends(deps.get_current_user)`; `crud.get_weekly_therapy_summary(db, summary_id, current_user_id)` filters by both id and user | Clean |
| `POST /monthly-audits/generate`, `POST /monthly-audits/{id}/retry` | Same pattern; retry additionally checks `is_user_premium()` before the ownership lookup (403 either way, no existence leak) | Clean |
| `run_weekly_summary_ai_job` / `run_monthly_audit_ai_job` (RQ job) | Re-queries `WHERE id == summary_id AND user_id == user_id` before acting — defense-in-depth even though `user_id` here only ever originates from the verified-token endpoint, never client input | Clean |
| `crud.lock_user_for_summary_generation(db, user_id)` | `SELECT ... FOR UPDATE` filtered to the caller's own `user_id`; Postgres row-level lock cannot affect another user's row | Clean |
| `GET /moments/upcoming` → `get_pending_or_sent_moment_for_user` | Endpoint itself unchanged in this diff; still calls with `current_user_id`; CRUD filters `NotificationMoment.user_id == user_id` | Clean |
| `mark_moment_push_delivered` | Raw `UPDATE ... WHERE id = :id`, called only from the delivery job with a server-generated `moment.id`, never client input; parameterized (no injection) | Clean |
| Debrief/recording `therapist_questions` read paths (`debriefs.py`, `session_recordings.py`) | Read off an already-ownership-scoped `debrief`/`recording` object fetched earlier in the (unchanged) handler | Clean |
| `crud.update_therapy_schedule` / `therapy_schedule_utils` (CS-18) | Operates only on the `user_id` passed by the (unmodified-in-this-batch) caller in `users.py`; no new endpoint surface added | Clean |
| Insight/moment CTA route changes (CS-19/CS-21) | Route strings changed, payload additions (e.g. `symptom_id`) are the acting user's own record IDs, not cross-user | Clean |

### Remediation Priority List

1. **Critical** — none.
2. **High** — HIGH-001: refactor `run_weekly_summary_ai_job`/`run_monthly_audit_ai_job` to pass IDs only and re-fetch/decrypt inside the worker (preferred), or, at minimum, verify `REDISGREEN_URL` is TLS (`rediss://`) and set short `result_ttl`/`failure_ttl` on these two enqueue calls before shipping CS-23. **This blocks deployment of the CS-23 async-generation change per CLAUDE.md's High-finding rule** — the rest of the 22-item batch is not implicated by this finding and is not blocked on it.
3. **Medium** — none.
4. **Low** — LOW-001 (custom_sessions length cap, backlog), LOW-002 (share-export temp-file cleanup, backlog), LOW-003 (operator follow-up to watch for the migration's duplicate-row warning, process not code).

### Deployment Recommendation

**Do not ship the CS-23 async-generation piece (weekly/monthly `/generate` and `/retry` enqueueing `run_weekly_summary_ai_job`/`run_monthly_audit_ai_job`) until HIGH-001 is remediated or explicitly risk-accepted by the operator with verified mitigations (TLS confirmed + TTLs set).** Every other reviewed item in this batch (CS-11, CS-18, CS-19/CS-20/CS-21, CS-22, and the three new migrations) is clean from a security/GDPR standpoint and is not blocked by this report.
