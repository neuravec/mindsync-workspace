# Feature Implementation Details

## Pre-Session Prep Card (Phase 2 - 2026-02-28)

- Pydantic models: `PrepCardTopic` (label, from_open_thread) and `PrepCardResult` (week_in_brief, unresolved_topics, themes_this_week, therapist_questions, limited_data) in `openai_service.py`.
- Prompts: `PREP_GUIDING_QUESTIONS_PROMPT`, `PREP_CARD_PROMPT`, `_DEFAULT_PREP_GUIDING_QUESTIONS` in `openai_service.py`.
- Service methods: `generate_prep_guiding_questions()` (uses GPT_MODEL_41_MINI) and `generate_prep_card()` (uses GPT_MODEL with gpt_structured()).
- Pattern mirrors debrief: same retry decorator (3 attempts), same fallback-to-defaults pattern, same user_parts message assembly.
- `generate_prep_card` enriches user message with debrief summaries (topics + emotional tone per session) AND open threads as a separate section for cross-referencing.
- Dummy key returns mock data (same pattern as debrief).

## Prep Reminder Notification (Phase 3 - 2026-02-28)

- Function: `notify_prep_reminder()` in `notification_service.py` -- hourly RQ job.
- Scheduler: `setup_hourly_prep_notification()` in `rq_scheduler_setup.py`, cron `0 * * * *`, timeout 1800s.
- Wired in `main.py` lifespan as `setup_hourly_prep_notification()`.
- Logic: query users with active subscription + non-null `therapy_schedule`, parse schedule JSON, compute next session in user local TZ, send FCM if 23-25h away AND no COMPLETED SessionPrepCard within 48h AND not in DND (22:00-08:00 local).

## Reflect Chat (2026-03-01)

- `Conversation` model does NOT have `xp_awarded` -- only `SessionDebrief` and `SessionPrepCard` do.
- Config setting overrides for prompts: use `(settings.X or MODULE_CONSTANT).format(...)` pattern.
- `ConversationSummary` has `summary_long` and `summary_short` (both encrypted Text). No `summary_text` field.
- RAG recency weighting: `_recency_weight()` in crud.py uses exponential decay with 30-day half-life. Must use `datetime.now(timezone.utc)` not `datetime.utcnow()`.

## Weekly Therapy Summary (2026-03-01)

- Background job: `app/tasks/weekly_therapy_summary.py` -- `generate_weekly_therapy_summaries()` runs hourly.
- Trigger: user's local hour == 22, then checks if tomorrow is a therapy day (or Sunday fallback).
- Data window: from previous summary's `data_window_end` to now. Duplicate guard: skip if <2h since last.
- AI call: `openai_service.generate_weekly_therapy_summary()` returns `WeeklyTherapySummaryResult`.
- All 5 sections encrypted before storage.
- Notification: respects `weekly_summary` pref from `notification_preferences` JSON column.
- RAG: `index_weekly_therapy_summary_to_rag()` in `rag_indexing.py` + backfill section.
- Endpoints: `app/api/v1/endpoints/weekly_summaries.py` -- GET /, GET /latest, GET /{id}, PUT /{id}, POST /{id}/retry.
- Import pattern: `from app.db.session import SessionLocal` (NOT `app.core.database`).
- Import pattern: `from app.utils import parse_timezone, utc_now` (via utils __init__.py re-exports).

## Symptom Tracking (2026-03-02)

- AI description: `generate_symptom_description()` in `openai_service.py` wraps `gpt_function()` with `SYMPTOM_DESCRIPTION_PROMPT`. Uses `GPT_MODEL_41_MINI`.
- RAG: `index_symptom_data_to_rag(user_id)` -- aggregates ALL symptoms into one RAG document with `source_id=0`.
- Weekly summary: `gather_weekly_summary_data()` includes `"symptom_scores"` key with formatted score changes.
- Activity check: `has_user_activity_since()` checks `SymptomScore` table too.

## Between-Session Notes (2026-03-02)

- Config: `BETWEEN_SESSION_GUIDING_QUESTIONS_PROMPT`, `BETWEEN_SESSION_NOTE_PROMPT` in `config.py`.
- Pydantic model: `BetweenSessionNoteResult` (topic, summary, emotional_tone_internal) in `openai_service.py`.
- Service methods: `generate_between_session_guiding_questions()` (GPT_MODEL_41_MINI) and `generate_between_session_note()` (GPT_MODEL, gpt_structured()).
- Fallback on exception: returns BetweenSessionNoteResult with topic="Untitled note" + truncated raw text.

## Realizations Collection (2026-03-03)

- See `realizations_feature.md` for full details (detection, hooks, RAG, XP).
- Key integration: `gather_weekly_summary_data()` includes `"realizations"` key, `has_user_activity_since()` checks Realization table.
- Prep card and weekly summary both include realizations in AI prompt context.

## Monthly Therapy Audit (2026-03-03)

- Background job: `app/tasks/monthly_therapy_audit.py` -- `generate_monthly_therapy_audits()` runs hourly.
- Trigger: user's local day == 1 AND local hour == 6 (6 AM on 1st of month).
- Previous month window: `first_of_current - timedelta(seconds=1)` for month_end, month_end.replace(day=1) for month_start.
- Data window adjusted for new users (start = max(month_start, user.created_at)).
- Duplicate guard: `get_monthly_therapy_audit_by_period(db, user_id, year, month)`.
- First audit detection: latest_audit is None or not COMPLETED.
- Premium status: `user_was_premium` flag preserves access after downgrade.
- Deterministic sections (no AI): activity_summary (counts of debriefs/notes/reflects/recordings), breakthroughs (from realizations).
- AI sections: topic_frequency, symptom_trends, patterns, movement_assessment, movement_type.
- Limited data: debrief_count < 2 AND symptom_score_count < 2.
- Retry pattern: retry-once on AI failure, mark FAILED on second failure.
- Notification: respects `monthly_audit` pref from `notification_preferences` JSON column.
- RAG: `index_monthly_therapy_audit_to_rag()` in `rag_indexing.py` + backfill.
- Endpoints: `app/api/v1/endpoints/monthly_audits.py` -- GET /, GET /latest, GET /{id}, POST /{id}/retry.
- Premium gating in endpoints: free users see activity_summary only, premium sections locked. `show_full = is_premium or audit.user_was_premium`.
- Retry endpoint: premium-only (403 if not), checks FAILED/PENDING status.
- Pydantic models in openai_service.py: `MonthlyAuditTopicItem`, `MonthlyAuditSymptomItem`, `MonthlyTherapyAuditResult`.
- Prompt: `MONTHLY_THERAPY_AUDIT_PROMPT` config + module-level default.
- CRUD: 6 functions (create, get, get_by_period, list, latest, update) + timeline integration.
- Timeline: `"monthly_audit"` type added to `get_timeline_page()`, FAILED records excluded, activity_summary decoded for preview.
- Schemas: `MonthlyAuditTopicFrequencyItem`, `MonthlyAuditSymptomTrendItem`, `MonthlyAuditBreakthroughItem`, `MonthlyTherapyAuditResponse`.
- Tests: 34 tests in `test_monthly_therapy_audit.py` (all pass).
