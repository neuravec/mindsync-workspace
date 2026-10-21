---
name: Voice session config moved from Flutter to backend (2026-05-12)
description: Backend now returns full client_session_config blob; Flutter consumes it. Future model/VAD/transcription tweaks are backend-only deploys, no mobile release.
type: project
originSessionId: e0a21b28-7faf-451d-b706-7d47cd73a071
---
Refactor done on 2026-05-12 right after the gpt-realtime-2 migration. The trigger was user frustration that swapping a model required a mobile App Store release.

**Architecture:**
- `POST /api/v1/audio-v2/realtime-session` response now carries `voice` + `client_session_config` blob (transcription_model, transcription_language, turn_detection, output_modalities, max_output_tokens, optional reasoning).
- `reasoning` is conditionally injected by the backend ONLY for `model.startswith("gpt-realtime-2")` — gpt-realtime-1.5 rejects this field. Helper: `_model_supports_reasoning()` in `openai_audio_service.py`.
- Flutter's `_sendSessionUpdate` builds the OpenAI WebRTC `session.update` event from this blob; omits the `reasoning` key entirely (NOT sends null) when config.reasoning is null.

**Why:** Backend changes ship same-day via Heroku restart; mobile changes need App Store/Play review. Putting opaque config in backend response eliminates mobile-release coupling for OpenAI param tweaks.

**How to apply:** When tweaking OpenAI realtime session params (turn_detection eagerness, max_output_tokens, reasoning effort, transcription model), change `settings.*` env vars or `_resolve_*()` helpers in `app/services/openai_audio_service.py`. Do NOT add new hardcoded values to `audio_chat_cubit.dart` — extend `VoiceSessionConfig` schema on both sides instead.

**New backend env vars (Heroku must set or accept defaults):**
- `REALTIME_TRANSCRIPTION_MODEL=gpt-4o-mini-transcribe`
- `REALTIME_REASONING_EFFORT=low` (valid: minimal/low/medium/high/xhigh; invalid silently falls back to "low" with ERROR log)

**Critical bugs found by devils-advocate and FIXED in the same session:**
- `service_locator.dart:133`: `registerFactory(() => AppCubit())` → `registerLazySingleton(() => AppCubit())`. PRE-EXISTING bug — every `sl<AppCubit>()` was a fresh instance with default `Voice.marin`. The refactor exposed it because FE now actually sends voice to backend. Fix: singleton + defensive `await sl<AppCubit>().getSelectedVoice()` in both `ConversationsManager.getSessionData()` and `ReflectChatCubit.getSessionData()` before reading selectedVoice.
- `RealtimeSessionModel.clientSessionConfig`: was `required` → made `nullable` with fallback in `audio_chat_cubit._kFallbackClientSessionConfig`. Otherwise backend rollback or partial response would crash voice chat. Fallback intentionally omits `reasoning` to be safe for any model.

**Pure helper for testability**: `AudioChatCubit.buildSessionUpdatePayload(...)` is `@visibleForTesting static` — 5 tests in `audio_chat_cubit_test.dart` verify payload shape (TC-1..TC-5: full config w/ reasoning, null reasoning omits key, language fallback, language override, null clientSessionConfig uses fallback).

**Known follow-ups (NOT done — deferred):**
- HIGH-01 (devils-advocate): `_VALID_REASONING_EFFORTS` is a hardcoded set in `openai_audio_service.py` — adding new OpenAI values (e.g. future `none`) requires code change. Consider accepting any string and letting OpenAI 400 surface loudly. Per-request validation; not cached.
- HIGH-02: `_AudioChatErrorView.onRetry` reuses stale ephemeral key (TTL 600s). Idle >10min then retry → silent failure. Fix: re-fetch on retry, OR add createdAt timestamp + expiry check, OR map OpenAI 401 to `error_voiceSessionExpired` ARB key.
- MED-03: `RealtimeSessionRequest.voice: str = "coral"` in `audio_v2.py:47` short-circuits `settings.AUDIO_V2_DEFAULT_VOICE`. Change to `voice: Optional[str] = None`. 1-liner backend PR.
- LOW-01: `_post_client_secrets_raw` retry loop can wall-clock ~30s+ when chaining timeouts + 502 retries. Could exceed Heroku 30s router timeout. Consider lowering per-attempt timeout to 10s.

**Test coverage:**
- Backend `test_audio_v2_config.py`: 65 tests pass (covers reasoning conditional, transcription model, voice echo, VAD eagerness, fallback validation).
- Frontend `test/bloc/audio_chat_cubit_test.dart`: 8 tests pass (3 DV06 barge-in + 5 payload shape).
- 5 pre-existing failures in `test_voice_fixes.py` are unrelated (`reflect._is_premium` missing — pre-dated this work).
