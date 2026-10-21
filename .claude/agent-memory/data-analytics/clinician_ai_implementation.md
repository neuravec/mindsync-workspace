---
name: clinician-ai-implementation
description: Clinician AI layer (clinician_ai.py) implementation patterns, test strategies, and patch target rules for lazy-import functions
metadata:
  type: project
---

## Clinician AI Layer — Therapist Deck V2 (2026-05-18)

**Files owned:**
- `app/services/clinician_ai.py` — 5 AI functions with full implementation
- `app/tasks/clinician_voice_notes.py` — RQ job for voice note pipeline
- `app/tests/test_clinician_ai.py` — 27 tests (all pass)
- `app/tests/test_clinician_voice_notes_task.py` — 19 tests (all pass)
- `app/core/config.py` — 6 new prompt keys added (CLINICIAN_*_PROMPT)

**AI function signatures (all in clinician_ai.py):**
- `generate_brief(patient_context: dict) -> BriefAIResult`
- `synthesize_golden_thread(patient_context: dict) -> list[dict]`
- `suggest_goals(patient_context: dict) -> list[AiGoal]`
- `assemble_session_note(raw_input, format, between_session_data) -> SessionNoteSections`
- `analyze_voice_note(transcript_text: str) -> VoiceNoteAnalysis`

**Implementation rules:**
- All functions use lazy imports (OpenAIService imported inside function body)
- All functions catch all exceptions, log at WARNING, return safe fallback — NEVER raise
- Data gates: `synthesize_golden_thread` and `suggest_goals` return `[]` immediately if insufficient data (no AI call)
- Model choice: `settings.GPT_MODEL_41_MINI` for all 5 functions
- Prompts: loaded from `settings.CLINICIAN_*_PROMPT`, fall back to module-level `_DEFAULT_*` constants when empty
- Config prompt keys added to `app/core/config.py` (all default `""`)

**Patch target rules (critical for tests):**
- `OpenAIService` is imported lazily (inside function body), so patch at source: `"app.services.openai_service.OpenAIService"` — NOT `"app.services.clinician_ai.OpenAIService"`
- `settings` is also imported lazily, so patch at source: `"app.core.config.settings"` — NOT `"app.services.clinician_ai.settings"`
- `ClinicianVoiceNote` is imported at module level in the task file — patch at: `"app.tasks.clinician_voice_notes.ClinicianVoiceNote"` using `_mock_cnv()` helper that sets `mock_cls.id = MagicMock()` (needed for SQLAlchemy filter expression)

**Voice note task pipeline (clinician_voice_notes.py):**
1. Load note; if `processing_status == "done"` → exit (idempotency)
2. If `assemblyai_transcript_id` already set → skip Redis + upload (resume path)
3. Load audio from Redis via `audio_storage_key`
4. Upload to AssemblyAI (`upload_audio`)
5. Submit transcription with `speaker_labels=False` (monologue), 2-attempt retry
6. Poll for result (`max_wait_seconds=900`), extract duration
7. Set `processing_status = "analyzing"`, encrypt + save transcript
8. Call `analyze_voice_note(transcript_text)`
9. Encrypt all analysis fields via `_persist_analysis()`
10. Set `processing_status = "done"`, cleanup Redis + delete AssemblyAI transcript

**Bootstrap pattern for task tests:**
Pre-inject mocks for modules that task imports at module level (before test module loads):
```python
sys.modules["app.services.assemblyai_service"] = _mock_aai_svc
sys.modules["app.services.clinician_ai"] = _mock_clinician_ai
sys.modules["app.services.encode_service"] = _mock_encode_svc
sys.modules["app.models.clinician_v2"] = _mock_clinician_v2
```
Then use `_mock_cnv()` context manager for any test that calls `_process` or `_mark_failed` (anything that does `db.query(ClinicianVoiceNote).filter(ClinicianVoiceNote.id == ...)`).

**Why:** `ClinicianVoiceNote` class from bootstrap is a `MagicMock` — SQLAlchemy filter expression accesses `.id` as a class attribute, which fails with `AttributeError: __name__` unless explicitly set.

**test_clinician_v2.py pre-existing failures:**
~18 tests fail with `AttributeError: __name__` on `TreatmentGoal` / `SessionNote` SQLAlchemy mocking — NOT caused by our changes; owned by backend-api.
