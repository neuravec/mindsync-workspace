---
name: recording-pipeline
description: Session recording chunked-upload pipeline — models, endpoints, GCS/Postgres chunk storage, Whisper transcription, recovery jobs, PostHog events, FCM patterns
metadata:
  type: reference
---

## Chunked Upload (Phase B) — Session Recordings
- Model: `UploadSession` in models.py — `upload_uploads` table, UUID PK, user_id FK (CASCADE), status (IN_PROGRESS/COMPLETED/ABORTED), total_bytes, bytes_received, content_type, sha256, storage_key, recording_id FK
- Migration: `tt0u1v2w3x4y` (idempotent, after `ss9t0u1v2w3x`)
- 4 endpoints on session_recordings router: POST /upload/initiate, PUT /upload/{id}/chunk, GET /upload/{id}/status, POST /upload/{id}/complete
- **Chunk storage: Postgres** (migration `vv2w3x4y5z0a`). GCS no longer required for chunked uploads — `_require_gcs_or_503()` removed from all 3 write paths. Single-shot POST /upload is unaffected (still uses GCS/recording_storage).
- Chunk protocol: Content-Range header (bytes start-end/total); idempotent on duplicate offset (< bytes_received); 409 on gap (start > bytes_received)
- **Complete (server-authoritative, 2026-06-21):** fast path — no GCS download/assembly or AssemblyAI in-request; creates session_recordings row + marks upload COMPLETED + enqueues `process_session_recording_whisper`; Timeline row created immediately in /complete (not deferred); returns 201 in <2s
- Worker assembles chunks from GCS (if assembled.audio doesn't exist yet), transcribes with Whisper, generates summary, sends FCM
- Cleanup: `cleanup_abandoned_upload_sessions()` in recording_recovery.py; registered as hourly job at minute 50
- CRUD: `create_upload_session`, `get_upload_session` (user-scoped), `get_abandoned_upload_sessions` (IN_PROGRESS older than N days), `get_fully_received_upload_sessions` (IN_PROGRESS + bytes_received >= total_bytes + recording_id IS NULL)
- Owner-auth: all endpoints scope by (session_id, user_id) → 404 (not 403) when not found

## Server-Authoritative Completion Safety-Net (2026-06-21)
- `finalize_complete_upload_sessions()` in recording_recovery.py: scans fully-received IN_PROGRESS UploadSessions with recording_id IS NULL; creates recording row + enqueues Whisper/GCS job; idempotent (db.refresh guard); fires every 15 min (minutes 5,20,35,50) via `setup_frequent_upload_finalizer()`
- NEVER finalizes partial sessions (bytes_received < total_bytes) — would create truncated audio
- Storage key in recording row points to `upload-sessions/{id}/assembled.audio` — worker assembles from chunk blobs if that object doesn't exist yet
- `process_session_recording_whisper` assembles from chunks when `"/assembled.audio"` is in storage_key and GCS fetch returns nothing (derives upload_session_id from key path `upload-sessions/{session_id}/assembled.audio`)
- `_assemble_chunks_from_gcs(session_id, total_bytes=0, content_type)` skips size check when total_bytes==0 (worker path)

## Recovery Hardening (2026-06-21)
- `get_stuck_recordings`: NULL `last_processing_attempt_at` no longer silently skips PROCESSING rows — falls back to `created_at < cutoff` for NULL case
- `recover_stuck_recordings`: GCS-first path — if recording has `storage_key`, enqueues `process_session_recording_whisper` (avoids stale AssemblyAI URLs); else falls back to `process_session_recording` (AssemblyAI path)
- `get_stuck_recordings` duplicate removed — one canonical version at ~line 1750 in crud.py
- FCM notification ("summary is ready") only fires from the worker (in `_post_success_jobs`), never from `/complete`

## GCS Bucket Name (BD4)
- `GCS_BUCKET_NAME=mindsync-8f534.firebasestorage.app` (set prod 2026-06-21) — GCS Python client `client.bucket(name)` accepts the raw bucket name regardless of domain suffix (*.appspot.com or *.firebasestorage.app); no code assumption about domain

## GCS Mocking Pattern for Tests (CRITICAL)
- `google.cloud.storage.Client.from_service_account_json` is a classmethod called inside endpoint bodies
- Correct patch: `patch("google.cloud.storage.Client.from_service_account_json", MagicMock(return_value=mock_client))`
- WRONG: `patch(..., mock_client)` directly — this replaces the function itself, not its return value, so calling it returns a MagicMock-of-MagicMock chain, never the blob you set up
- Chain: `from_service_account_json(creds)` → `client.bucket(name)` → `bucket.blob(key)` → `blob.download_as_bytes()` → bytes

## RQ enqueue arg order
- `rq_queue.enqueue(process_session_recording, recording_id, user_id, assemblyai_url, job_timeout=N)`
- `rq_queue.enqueue(process_session_recording_whisper, recording_id, user_id, assemblyai_url_or_empty, job_timeout=N)`

## FCM Notification Patterns
- `send_fcm_message_v1()` returns str: "sent" | "failed" | "token_invalid"
- Invalid tokens (404 or UNREGISTERED/INVALID_ARGUMENT in body): return "token_invalid", NOT retried
- `send_fcm_to_all_user_tokens()` calls `crud.remove_fcm_token(db, token)` when status == "token_invalid"
- FCM push for recording summary: fires from worker only (`_post_success_jobs`), NEVER from `/upload/{id}/complete`

## Whisper Chunked Transcription (Fallback Path)
- `app/services/wav_chunker.py` — WAV splitter + chunked transcription orchestrator
  - `split_wav_into_chunks(wav_bytes, chunk_size_bytes=20MB)` — pure-Python WAV split at frame boundaries
  - `split_compressed_into_chunks(audio_bytes, content_type, chunk_duration_ms=10min)` — pydub split; returns None when pydub unavailable
  - `transcribe_in_chunks(audio_bytes, content_type, openai_service, whisper_lang, size_threshold_bytes=24MB)` — orchestrator: small files → single-shot; large WAV → split_wav; large compressed → pydub or single-shot fallback
  - `ChunkTranscriptionError` — raised when a chunk fails after 1 retry
- `app/tasks/session_recording.py` — `process_session_recording_whisper`:
  - Audio source priority: GCS (recording.storage_key) → Redis cache (legacy)
  - For chunked-upload recordings: storage_key = `upload-sessions/{id}/assembled.audio`; if GCS fetch returns nothing AND key contains `/assembled.audio`, worker derives upload_session_id and calls `_assemble_chunks_from_gcs(session_id, 0, content_type)`
  - Calls `transcribe_in_chunks` instead of single `openai_service.speech_to_text` directly
  - `openai_service.py` NOT modified (data-analytics owns it)
- `app/tests/test_whisper_chunked.py` — 38 tests (all pass)

## PostHog Event Taxonomy — Recording Pipeline v2 (2026-06-29, on disk, not deployed)
- Backend emits 4 canonical events (exact names, shared contract with flutter-mobile):
  - `recording_chunk_store_failed` — in `upload_chunk` when `_store_chunk_to_pg` returns False; props: `http_status=503`, `reason='postgres_store_failed'`, `upload_session_id`, `chunk_index`
  - `recording_processing_started` — in Whisper worker, only when `processing_attempts == 1` (idempotent on retry); props: `upload_session_id` (None for single-shot), `recording_kind`, `transcription_provider='whisper'`
  - `recording_processing_completed` — after COMPLETED commit; props: `upload_session_id`, `duration_seconds`, `transcription_provider='whisper'`
  - `recording_processing_failed` — in except block; props: `upload_session_id`, `error_type`, `transcription_provider='whisper'`
- Flutter-mobile emits separately (NEVER duplicate): `recording_started`, `recording_stopped`, `upload_started`, `chunk_upload_failed`, `saved`, `processing_failed`, `recovered`
- All events wrapped in try/except — PostHog failure never crashes critical path
- Worker uses `user_id` as distinct_id (no HTTP context); chunk endpoint uses `get_posthog_distinct_id() or current_user_id`
- `upload_session_id` derived from `storage_key.split("/")[1]` when `/assembled.audio` in key; None for single-shot

## B10 audit findings (2026-08-10) — diarization_failed=100% + orphaned upload_session

**diarization_failed=true on every recent session_recordings row is EXPECTED, not a regression.**
The chunked-upload completion path (`complete_chunked_upload` in session_recordings.py, the ONLY
path any current app build's session-recording flow exercises per live DB evidence) always enqueues
`process_session_recording_whisper`, never `process_session_recording` (the AssemblyAI path) — see
docstring at session_recordings.py:704-710 ("No AssemblyAI upload happens in this request"). Whisper
has no diarization (`diarization_reliable = False` hardcoded at session_recording.py:710), and
`_save_summary_sections` sets `recording.diarization_failed = not diarization_reliable` (line 139) —
so `diarization_failed=True` and `assemblyai_transcript_id=NULL` on 100% of chunked-path recordings
by design. The legacy single-shot `/upload` endpoint (session_recordings.py:836) is the only path that
still uses AssemblyAI with diarization (`process_session_recording`) — kept for old app builds only.
The 2026-08-04 "STT AssemblyAI" batch (bf02d88) explicitly does NOT touch this pipeline — its
`app/services/stt_service.py` docstring says so outright; it only affects short-form voice notes
(prep/debrief/between-session/check-in).

**Deployment status correction:** the "STT AssemblyAI + PostHog + cleanup 2026-08-04" batch, listed
elsewhere as UNCOMMITTED, is actually committed to `main` (bf02d88 "phog + whisper") AND deployed to
Heroku as v528 (`heroku releases`), with a follow-up fix a7e5b98 ("lops fix") as current v529. Always
re-verify deploy status via `heroku releases -a mindsync` rather than trusting an old memory note.

**Prod config gap found while investigating this:** `ASSEMBLYAI_API_KEY` is NOT set in Heroku config
(`heroku config -a mindsync` — absent entirely; only `WHISPER_MODEL` is set among STT-related vars).
`stt_service.py` (short-form notes) guards for this (`bool(settings.ASSEMBLYAI_API_KEY)`) and silently
falls back to Whisper — safe. But `AssemblyAIService` (used directly by the legacy single-shot
session-recording path) has NO such guard — it would send an empty `authorization` header and get a
hard 401 from AssemblyAI on every call. Currently invisible (zero traffic hit that path in the last
28d per DB), but it's a landmine for any user still on an old app build using single-shot upload.
This is an env-var gap (integration-devops owns Procfile/.env.example) — flagged, not fixed here.

**`upload_sessions.recording_id` can legitimately be NULL on a `status='completed'` row** — this is
NOT a linking-step bug. `recording_id` has `ForeignKey("session_recordings.id", ondelete="SET NULL")`
(models.py:1798, matching migration tt0u1v2w3x4y:92). Both code paths that ever set
`status=COMPLETED` (session_recordings.py:777-778 and recording_recovery.py:260-261) set
`recording_id` in the exact same commit — there is no code path that writes `recording_id=None`. The
ONLY mechanism that can null it afterward is Postgres's FK cascade firing when the linked
`session_recordings` row is hard-deleted — which happens routinely via `purge_expired_soft_deletes`
(crud.py:4027, hourly job) 24h after a user soft-deletes a recording. So a `completed` upload_session
with `recording_id IS NULL` is proof-by-elimination evidence of "user deleted this recording later,"
not evidence of a broken completion flow. `status` and `recording_id` are independently-written
columns — the FK cascade only ever touches `recording_id`.

## Files Modified in Server-Authoritative Completion (2026-06-21)
- `app/api/v1/endpoints/session_recordings.py` — `/complete` rewritten: no in-request GCS/AAI, creates recording row immediately, enqueues whisper worker, returns 201 fast
- `app/tasks/recording_recovery.py` — added `finalize_complete_upload_sessions()`; hardened `recover_stuck_recordings` (GCS-first + NULL timestamp fix)
- `app/crud/crud.py` — added `get_fully_received_upload_sessions()`; fixed `get_stuck_recordings` NULL timestamp; removed duplicate `get_stuck_recordings`
- `app/core/rq_scheduler_setup.py` — added `setup_frequent_upload_finalizer()` (cron 5,20,35,50 * * * *)
- `app/main.py` — imported + called `setup_frequent_upload_finalizer()`
- `app/core/config.py` — updated GCS_BUCKET_NAME comment (*.firebasestorage.app not *.appspot.com)
- `app/tests/test_server_auth_completion.py` — NEW: 32 tests (all pass)
- `app/tests/test_chunked_upload.py` — updated TestCompleteChunkedUpload + TestChunkedUploadFullFlow for new fast-path /complete (removed GCS/AAI/Redis mocks from those tests)
