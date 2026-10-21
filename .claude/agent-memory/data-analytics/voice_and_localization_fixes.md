---
name: voice-and-localization-fixes
description: Voice RAG/new-user-detection fixes, voice note output quality enhancement, AI language naturalness instruction (BUG-L04), and Polish/7-language label fix — all backend AI-prompt work.
metadata:
  type: project
---

## Voice Fixes (2026-03-25)

### BUG-VA03: Voice RAG Injection + New User Detection
- `_therapy_helpers.py`: `get_user_data_richness(db, user_id)` → "new"/"developing"/"established" (0-2/3-5/6+ combined conversations+debriefs+notes+symptom_scores).
- `_therapy_helpers.py`: `NEW_USER_GUARDRAIL`, `DEVELOPING_USER_GUARDRAIL` prompt constants.
- `reflect.py` `get_reflect_session_data` and `conversations.py` `get_session_data`: now gather real RAG context (last 3 user msgs, or therapy_context seed for new conversations) instead of replacing `{RAG_CONTEXT}` with empty string; append user-richness guardrail.

### BUG-VA04: Voice Note Output Quality Enhancement
- openai_service.py: `VOICE_LONG_RECORDING_ENHANCEMENT` prompt, `VOICE_ENHANCEMENT_THRESHOLD_SECONDS=120`, `VOICE_OUTPUT_MIN_RATIO=0.15`.
- `generate_session_card()`, `generate_between_session_note()`, `generate_prep_card()`: new optional `input_type`/`input_duration_seconds` params; VOICE+>120s appends enhanced prompt; quality gate logs warning if output<15% of input words.
- `debriefs.py`/`between_sessions.py`/`prep_cards.py`: `_estimate_audio_duration_seconds()` (16KB/s heuristic), `_log_transcription_completeness()` (<50wpm warning).
- Tests: 40 in test_voice_fixes.py.

## BUG-L04: AI Language Naturalness Instruction (2026-03-29)
- All prompt templates append: "Use natural, native-sounding {language} — not a direct translation from English. Therapy-related terms should follow locally accepted conventions in {language}."
- Applied in: conversations.py (text+voice), periodic_summary.py (daily+weekly), chart_explanations.py, notification_service.py (journal+inactivity), profile_service.py.
- Pattern: check `.lower() != 'english'` before injecting; English path unchanged so nothing breaks.

## Polish Localization — AI Label Fix (2026-05-11)
- `crud.py`: `_THERAPY_SIGNAL_LABELS` + `_HEALTH_CHECK_LABELS` dicts (7 languages) + `_get_therapy_signal_label()`/`_get_health_check_label()` helpers.
- `compute_deterministic_signal(inputs, language="English")` and `compute_relationship_state(..., language="English")`: new optional param, default preserves existing test assertions.
- `therapy_tracking_signal.py`: moved profile+language resolution BEFORE `compute_deterministic_signal` call (was after → NameError).
- Known NOT fixed (other agents' files): hardcoded labels in `health_check.py` lines 787-791/1005-1009 (backend-api); "Untitled reflection"/"Auto-detected" are Flutter-side constants, no backend string involved.
- `ai_language` values are full English names ("English","Polish","German","French","Norwegian","Swedish","Spanish") matching `SupportedLocale.backendName`; model column default "en" is legacy only.
