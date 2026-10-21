---
name: project-general-fixes-2026-06-20
description: "Three-topic batch — remove notif Intensity, pull frustration out of onboarding, and a comprehensive crash-safe session-recording reliability overhaul (Phases A–C + Whisper chunking)"
metadata: 
  node_type: memory
  type: project
  originSessionId: e89f4590-de92-4714-b01d-1a4e86ef3d6a
---

Session "general_fixes" (2026-06-20→21, remote-control). Three independent topics, run sequentially. CONCURRENCY: multiple sessions were live on these repos simultaneously; a session switched the frontend branch to `fix/voice-note-dataloss` mid-run.

COMMITTED + PUSHED 2026-06-21 (user said: commit+push on the main branch, other sessions already pushed theirs):
- **Backend** `MindSync` `main`: commit **dcc779d** (a6f5a2b..dcc779d, 30 files) = Topic 1 BE + ALL Topic 3 BE (migrations rr8s9t0u1v2w/ss9t0u1v2w3x/tt0u1v2w3x4y, recording_storage.py, wav_chunker.py, admin_recordings.py, recording_recovery.py, orchestrator). Pushed origin/main. Staged with explicit paths `app/ alembic/ .env.example` — excluded `.claude/agent-memory/` scratchpads. NEVER `git add .`.
- **Frontend** `mindsync-frontend` `dev` (= origin HEAD / main branch): commit **0e01298** (cherry-picked from d1f57e4 on fix/voice-note-dataloss) = Topic 3 FE recording_pipeline_v2. Cherry-pick onto dev was CLEAN (my ARB changes were purely additive recording_v2_* keys — no overlap with de-clinic's intensity-key removal). Regenerated l10n (no diff), analyze 0 err, 46/46 pipeline tests pass on merged dev. Pushed origin/dev → triggers Codemagic auto-versioning→TestFlight.
- Topic 1 FE + Topic 2 FE were ALREADY on origin/dev via concurrent de-clinic commit 6541248 (my agents converged to same end-state, working tree had no diff for those files). voice-note already merged to dev (f2d7845).
- Non-destructive backup still at repo-root `_work_backup_2026_06_20/` (git-diff patches + untracked tgz; now redundant, safe to delete).

See [[feedback-memory-write-after-commit]], runbook RECORDING_ROLLOUT_RUNBOOK.md.

## DEPLOYMENT STATUS (update here as steps complete) — last touched 2026-06-21
Code = committed+pushed (main / dev). Heroku rollout is OPERATOR-gated and PARTIAL:
- [x] **Set `GCS_BUCKET_NAME=mindsync-8f534.firebasestorage.app`** in Heroku config vars — DONE by operator 2026-06-21.
- [ ] **Run migrations on Heroku** (MANUAL — deploy ≠ migrate, no release phase in Procfile): `heroku run "alembic upgrade head"`. Brings DB to HEAD `tt0u1v2w3x4y` (adds storage_key/enqueue_failed/processing_attempts/last_processing_attempt_at cols + `upload_sessions` table). WITHOUT this the new recording endpoints break. ← NEXT CRITICAL STEP
- [ ] **Deploy backend** `dcc779d` to Heroku (if not auto-deployed from GitHub main).
- [ ] **Verify** logs after first recording: `[RecordingStorage] Stored N bytes…`. If `403/permission` warning → grant the FIREBASE_CREDENTIALS service account (`mindsync-8f534-…json`) role **Storage Object Admin** on project `mindsync-8f534` in GCP IAM. (Storage is best-effort; won't 500 uploads, just won't persist durably until perms fixed.)
- [ ] **Tier 2:** create PostHog flag `recording_pipeline_v2` (default OFF) → enable for TestFlight/beta → ramp prod after new app ships. Recommend **Standard-2X dyno** before ramping (chunked `/complete` holds ~206MB in RAM).

### Config facts (for future sessions)
- Firebase project id = `mindsync-8f534`; GCS/Storage bucket = `mindsync-8f534.firebasestorage.app` (from google-services.json + firebase_options.dart).
- `FIREBASE_CREDENTIALS` is a FILE PATH (e.g. `app/mindsync-8f534-839e8464e684.json`), NOT inline JSON — used by `gcs.Client.from_service_account_json(...)` and `credentials.Certificate(...)`. recording_storage.py reuses this same path pattern.
- Heroku config vars are app-level → one `config:set` covers web/worker/scheduler. Backend GitHub repo = `neuravec/MindSync` (origin/main); frontend = `neuravec/mindsync-frontend` (origin/dev).

## Topic 1 — Remove notification "Intensity" (DONE, verified)
- Intensity (0/1/2 = off/1-per-day/2-per-day) was REDUNDANT and was the ONLY daily rate-cap in the orchestrator. Removed FE+BE.
- BE: dropped `notification_intensity` from `UserPreferences` model/schemas/crud; orchestrator now uses fixed `_DEFAULT_DAILY_PROACTIVE_LIMIT = 1` (preserves old default). Master-toggle "off" verified independent: orchestrator's `_is_notifications_enabled()` (reads `notification_enabled`) runs as step 0 before the cap, so users still mute everything. Migration `rr8s9t0u1v2w_drop_notification_intensity` (idempotent, down_revision `qq7r8s9t0u1v`). 294/294 affected tests pass.
- FE: removed `_IntensityPicker`, `notificationIntensity` state, `setNotificationIntensity`, ARB keys (`notifSettings_intensity*` + `notifSettings_recommended`). settings tests green (6/6 + 14/14), analyze 0 err.

## Topic 2 — Frustration question out of onboarding (DONE, verified)
- Therapist guidance: don't ask a patient about frustration at the START of therapy. Step 1 ("Challenges" = "What do you want more of?") was ALREADY positive; the negatively-framed element was the FRUSTRATION block (`onboarding_biggestFrustration` chips + `onboarding_frustrationFreeText`) in the Journey step (step 3).
- FE-only: removed that block from `onboarding_journey_view.dart`; preserved duration, goals, crisis-banner (moved to goals text), and Art.9 `currently_in_therapy` logic. `saveJourneyAndAdvance` no longer sends frustration fields.
- Frustration ARB keys + backend fields (`frustration_chips`/`frustration_text`, nullable) INTENTIONALLY KEPT for a future "later in the journey" re-surfacing (no clean existing home found, so not re-placed). No backend change. onboarding journey tests 17/17, analyze 0 err.

## Topic 3 — Crash-safe session recording (DONE on disk; staged rollout)
Plan docs at repo root: `SESSION_RECORDING_RELIABILITY_PLAN.md`, `RECORDING_ROLLOUT_RUNBOOK.md`.
Root causes: moov-atom/WAV-header corruption on mid-recording kill; Whisper 25MB single-shot; Heroku 30s H12 on big uploads; 24h local auto-delete (the ACTIVE cause of the real user's loss); recovery trusted a single SharedPreferences key; server kept audio only ~days (AssemblyAI) + 48h (Redis).

**Two deployment tiers** (backend deploys in min; app stores 1–2 days):
- **Tier 1 — backend, additive, backward-compatible, PROD-SAFE NOW** (helps current users incl. the affected one). integration-devops verdict: SAFE. Old app's `/upload`→poll→delete-on-COMPLETED path unaffected; enqueue-failure now returns 201+id (was 503+delete) and the safety-net job recovers it.
  - Durable GCS audio retention until COMPLETED (`recording_storage.py`; reuses Firebase service acct; **new env `GCS_BUCKET_NAME`**, no-op when unset). Migration `ss9t0u1v2w3x` (durability cols: storage_key, enqueue_failed, processing_attempts, last_processing_attempt_at).
  - Resumable CHUNKED upload endpoints (`/upload/initiate|chunk|status|complete`, resume via `next_expected_offset`, GCS compose-ish assembly). Migration `tt0u1v2w3x4y` (`upload_sessions` table). **NEW MIGRATION HEAD = `tt0u1v2w3x4y`** (chain qq7r8s9t0u1v→rr→ss→tt).
  - Reprocess endpoint `POST /{id}/reprocess`; hourly safety-net job (`recording_recovery.py`, :45) recovers stuck PENDING/PROCESSING/FAILED + cleans abandoned upload sessions (:50, >7d); admin diagnose/recover endpoints (X-Admin-API-Key) for support.
  - Whisper fallback chunking (`wav_chunker.py`, pure-Python WAV splitter + pydub for compressed; GCS-first audio source; fail-fast retains audio). `openai_service.py` untouched.
  - GOTCHA: chunked `/complete` loads the whole assembled audio in RAM (~206MB for 75-min iOS WAV) → recommend **Standard-2X dyno** before Tier 2 ramps; future streaming-SHA optimization.
- **Tier 2 — needs new app → TestFlight first, prod via PostHog flag** `recording_pipeline_v2` (default OFF = exact current behaviour; safe-default when flag unknown/not-loaded).
  - Crash-safe capture: `record.startStream(pcm16bits)` → 5-min rolling append-only `.pcm` segments under `{appDocs}/recordings/{sessionId}/`. Battery death/kill leaves readable PCM; `WavBuilder` prepends a 44-byte header. **Continue** via `resumeSessionV2` (appends new segments, earlier untouched). Disk-scan recovery + JSON manifest (`recordingManifestV2`) instead of single prefs key; WAV header repair; 4-option recovery sheet (Continue/Finish&Process/Save-share/Discard). **24h stale auto-delete neutralized for ALL users** (flag on/off).
  - Chunked upload client (`chunked_upload_manager.dart`): streamed SHA-256, server-driven chunk size, 5× backoff, connectivity auto-resume, 409→status→resume, resume-after-kill via manifest `uploadSessionId`/`bytesUploaded`, 503→single-shot fallback. Added `crypto` dep.
  - Tests: Phase A 38/38, chunked client 20/20 (46/46 dir), analyze 0 err.

## Recovery of the user's specific lost recording (her follow-up question)
- Honest: a ~month-old recording is likely unrecoverable if both device file AND server audio are gone (legacy retention expired). Best shots: (1) disk-scan recovery in the new build if her device still has the file; (2) admin diagnose endpoint on prod (needs her email + operator) — regenerate summary if a transcript already exists. Going forward this class of loss is eliminated.
