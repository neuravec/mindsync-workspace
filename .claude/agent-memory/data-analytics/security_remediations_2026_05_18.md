---
name: security-remediations-2026-05-18
description: Clinician AI Layer implementation + its security fixes, and Hero Insight security remediations, all from 2026-05-18.
metadata:
  type: project
---

## Clinician AI Layer — see `clinician_ai_implementation.md` for full detail
- 5 AI functions in `clinician_ai.py`: generate_brief, synthesize_golden_thread, suggest_goals, assemble_session_note, analyze_voice_note.
- New RQ job `app/tasks/clinician_voice_notes.py` — AssemblyAI pipeline (upload→submit→poll→analyze→done).
- Patch rule: `settings` + `OpenAIService` imported lazily → patch at source (`app.core.config.settings`, `app.services.openai_service.OpenAIService`).
- `_mock_cnv()` helper required for any test calling `_process`/`_mark_failed` (SQLAlchemy filter needs `mock_cls.id = MagicMock()`).
- 46 tests, all pass. Config keys: CLINICIAN_BRIEF/GOLDEN_THREAD/GOALS/SESSION_NOTE_SOAP/SESSION_NOTE_DAP/VOICE_NOTE_ANALYSIS_PROMPT.

## Clinician AI Security Fixes
- HIGH-002 (transcript leak) in `clinician_voice_notes.py`: `_mark_failed(error_code: str)` — safety filter rejects values with spaces/>64 chars, falls back to `_ERR_UNKNOWN`. Constants `_ERR_AUDIO_MISSING/_ERR_TRANSCRIPTION_FAILED/_ERR_AI_ANALYSIS_FAILED/_ERR_UNKNOWN` are the ONLY values allowed into `processing_error`. All logger calls use `exc_info=True` without interpolating exception text.
- HIGH-004 (prompt injection) in `clinician_ai.py`: `_sanitise_patient_text(text, max_chars)` strips 9 injection patterns + hard-caps length; `_wrap_patient_block()` wraps untrusted content in BEGIN/END markers; `_ANTI_INJECTION_SYSTEM_CLAUSE` appended to every prompt touching patient content (all 5 functions). `analyze_voice_note` sanitises transcript at max_chars=8000.
- Tests: 69 total (23 injection-defence + 3 transcript-leak + 3 category-code).

## Hero Insight Security Remediations
- HIGH-001 cooldown: `HERO_INSIGHT_REFRESH_MIN_INTERVAL_SECONDS=3600` in config.py; endpoint checks elapsed<min_interval after hash-miss (premium=3600s, free=FREE_CADENCE_DAYS); returns cached row, not 429.
- MED-001: `context_variable` removed from `PremiumTeaserResponse` schema (CRUD still returns it in dict; endpoint interpolates `headline` server-side only).
- MED-002: free users get `timedelta(days=FREE_CADENCE_DAYS)` cooldown.
- MED-003: all 3 exception log sites use `type(e).__name__` (not `str(e)`) to avoid leaking OpenAI SDK payloads.
- LOW-001: `id: int` removed from `HeroInsightData` schema (ORM objects can still have `.id`; schema just doesn't serialize it).
- Tests: 48 total (was 42), new `TestRefreshCooldown` class (6 tests).
