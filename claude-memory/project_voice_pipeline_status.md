---
name: Voice pipeline status (2026-03-26)
description: Current state of voice features — what works, what's pending, known issues
type: project
---

**Working (production, 2026-03-26):**
- Realtime voice agent (Reflect + Conversations): uses `/v1/realtime/sessions` with flat body `{model, voice, input_audio_noise_reduction}`
- Backend speech_to_text: retry excludes 400 errors, diagnostic logging (file size + header hex)
- `conversations.py /chat/audio`: fixed `.name` on BytesIO + `.text` extraction + error handling

**Pending frontend build:**
- Recording fix: `_recorder.stop()` must run BEFORE `_stopRecordingServices()` — otherwise Android kills the recording process and the M4A file is truncated to 28 bytes (header only). Fixed in: `debrief_capture_cubit.dart`, `health_check_flow_cubit.dart` (2 methods), `record_session_cubit.dart`
- Reflect mic error feedback: snackbar when `getSessionData()` fails (was silent)
- File size validation: reject files < 1KB before upload

**Not yet done — future migration:**
- OpenAI Realtime API GA migration (`/v1/realtime/client_secrets` with `session` wrapper). Correct GA body format: `{"session": {"type": "realtime", "model": "..."}}`. Voice must NOT go in body — set via WebRTC data channel `session.update`. `input_audio_noise_reduction` also not valid for `client_secrets`. Must be tested offline before production deploy.

**Why:** Migrating to `client_secrets` broke production for 24h. Reverted to `sessions` which works.
