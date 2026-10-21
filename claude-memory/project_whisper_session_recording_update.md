---
name: Whisper fallback needs update after session recording raised to 75 min
description: Follow-up — session recording max raised to 75 min (2026-04-22), but Whisper fallback path still has 25MB/~15-20 min file limit; must be chunked in a future session
type: project
originSessionId: 46a60cbc-1d55-4508-9248-790d817ca344
---
**PREREQUISITES BEFORE STARTING THIS WORK:** Devil's-advocate review on 2026-04-22 flagged 3 CRITICAL blockers for the 75-min main path itself:
- **CRIT-01**: RQ `job_timeout=1800` (30 min) at enqueue sites in `app/api/v1/endpoints/session_recordings.py:265,403,423` is shorter than 2×2400s AssemblyAI polling budget — worker SIGKILLs mid-poll on retry. Fix: raise job_timeout to ≥5700s.
- **CRIT-02**: `record_session_cubit.dart` has NO auto-save timer (unlike `debrief_capture_cubit.dart:678-713`). Process death mid-recording loses the entire audio. Fix: port the `_autoSaveTimer` pattern.
- **CRIT-03**: `assemblyai_service.py:42-47` `requests.post` for upload has NO timeout and runs inside the web request — Heroku router H12 timeout at 30s for large 75-min files. Fix: move upload to worker OR add explicit timeout + keep device file until terminal success.

Whisper fallback chunking is MOOT until CRIT-01/02/03 are resolved — both paths share the same RQ worker and endpoint flow. Do not start Whisper work before those are fixed.

---

Session recording max duration raised from 15 to 75 minutes on 2026-04-22 (frontend change in `record_session_cubit.dart`, backend `poll_for_result` bumped to 2400s). Main transcription path uses AssemblyAI which handles long audio natively (up to 5GB, ~10h).

The **Whisper fallback path** (`process_session_recording_whisper` in `app/tasks/session_recording.py`) was NOT updated. Whisper has a hard 25MB file-size limit. Max audio that fits depends on codec/bitrate (m4a 64kbps ≈ 50 min, m4a 128kbps ≈ 25 min, WAV 16kHz mono ≈ 13 min). Any recording whose file exceeds 25MB falling back to Whisper (when AssemblyAI fails or is unavailable) will **fail on the single-shot `speech_to_text` call** near line 427.

**Why:** Fallback must also work for long recordings. Otherwise the whole "75-min session recording" feature silently breaks when AssemblyAI has an outage or a rate-limit error. Main path is robust, fallback is not — divergence bug.

**How to apply:** In a future session, implement audio chunking inside `process_session_recording_whisper`:
- Use ffmpeg (or pydub) to split audio into ~10-min chunks (stay well under 25MB)
- Call `openai_service.speech_to_text()` per chunk
- Concatenate transcripts (consider overlap strategy to preserve sentence boundaries)
- Whisper has no diarization, so fallback transcript stays single-speaker (existing behavior)
- Verify `diarization_reliable=False` still set in the fallback branch
- Add a test in `test_scalability_fixes.py` or similar covering long-audio Whisper fallback

User confirmed this is deferred — NOT in the session where the 75-min limit was introduced. Flag it before next session recording-related work.
