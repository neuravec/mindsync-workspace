# Realizations Collection Feature (2026-03-03)

## Core Model
- `Realization`: id, user_id, realization_text (encrypted), source_type, source_id, source_field, source_item_index, is_auto_detected, dismissed, xp_awarded, created_at, deleted_at
- UniqueConstraint: (user_id, source_type, source_id, source_field, source_item_index)
- Index: ix_realization_user_created (user_id, created_at)

## AI Detection
- Pydantic models: `RealizationDetectionItem` (has_realization, realization_text) and `RealizationDetectionResult` (items) in `openai_service.py`.
- Default prompt: `_DEFAULT_REALIZATION_DETECTION_PROMPT` in `openai_service.py`. Config: `REALIZATION_DETECTION_PROMPT` (empty, uses module default).
- Service method: `detect_realizations()` on `OpenAIService` — uses `gpt_structured()` with `GPT_MODEL_41_MINI`, retry decorator (3 attempts). Pads/truncates result to match input length. Dummy key returns all-false.

## Background Task
- `app/tasks/realization_detection.py` — `detect_realizations_for_source(user_id, source_type, source_id, source_field)`. Fire-and-forget, opens own SessionLocal, catches all exceptions.
- Source types supported: debrief/key_insights (JSON array), between_session/summary (scalar text), recording/patient_insights (JSON array).
- Premium vs free: premium gets `dismissed=False`, XP award, RAG indexing. Free gets `dismissed=True` (upsell indicators), no XP or RAG.
- Duplicate guard: checks UniqueConstraint fields before creating each Realization row.

## Hooks
- Fire-and-forget `rq_queue.enqueue()` in debriefs.py (after RAG indexing in `_process_debrief_ai`), between_sessions.py (via `_enqueue_realization_detection` helper, COMPLETED only), session_recording.py (step 15, only if `diarization_reliable`).

## RAG
- `index_realization_to_rag(realization_id, user_id)` in `rag_indexing.py`. Skips deleted/dismissed. Text format: `"Therapy realization: {text}"`. Backfill section added with try/except guard.

## Config
- `REALIZATION_XP_POINTS: int = 5` in config.py (not used in current implementation, XP uses flag pattern).

## Cross-Feature Integration (2026-03-03)
- `gather_weekly_summary_data()` in crud.py: section 7 queries active, non-dismissed, non-deleted realizations in window. Decodes text, returns list of dicts with text/source_type/created_at.
- `has_user_activity_since()` in crud.py: checks Realization table for user activity detection.
- `generate_weekly_therapy_summary()` in openai_service.py: adds "Key realizations this week:" section with quoted text + source/date attribution.
- `generate_prep_card()` in openai_service.py: accepts `recent_realizations` param, adds "Recent realizations (key breakthroughs)" section.
- `generate_prep_guiding_questions()` in openai_service.py: accepts `recent_realizations` param, adds "Recent realizations (key breakthroughs)" section.
- `get_recent_realization_dicts()` in `_therapy_helpers.py`: queries last 30 days, limit 10, active/non-dismissed, returns decoded dicts.
- All 3 prep card endpoints (text, voice, retry) + guiding questions endpoint wire realizations through.
