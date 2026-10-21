---
name: feature-implementations-2026-03
description: Personal Bio, Therapy Health Check, Prep Card auto-generation job internals, and the AI Card Content Quality Overhaul — implemented March 2026.
metadata:
  type: project
---

## Personal Bio (2026-03-04, extended 2026-05-19)
- `PersonalBioResult` in openai_service.py — 5 sections (progress, patterns, drivers, style, outlook) + limited_data. `BioProgressResult(progress: str)` for progress-only calls.
- Prompt `PERSONAL_BIO_PROMPT` (module default + config key). New: `BIO_PROGRESS_SECTION_PROMPT` (14d window), `RESTYLE_BIO_PROMPT` (tone change, no therapy data) — both `settings.X or X` fallback.
- `generate_bio_progress_section(data, therapy_context, tone_archetype, user_pronouns, user_language, previous_bio=None) -> str` — partial update, 14d window only.
- `restyle_personal_bio(previous_bio, tone_archetype, user_pronouns, user_language) -> PersonalBioResult` — never calls `_format_bio_data` (no therapy data sent).
- Job: `app/tasks/personal_bio.py` — `generate_personal_bios()` hourly cron (10 PM local, therapy-day trigger, 6h duplicate guard, 14d window) + `generate_single_personal_bio(user_id)` on-demand. Scheduler: `setup_weekly_personal_bio()`.
- CRUD: `create_personal_bio`, `get_latest_personal_bio`, `update_personal_bio`.

## Notification Preferences default keys
`_DEFAULT_NOTIFICATION_PREFS` in crud.py: `weekly_summary: True`, `monthly_audit: True`, `post_session_nudge: True`, `health_check: True`.

## Therapy Health Check (2026-03-04)
- `HealthCheckResult` in openai_service.py — observation, suggested_questions, is_safety_escalation, safety_observation, safety_questions. Fallback: `FALLBACK_HEALTH_CHECK`.
- `OpenAIService.generate_health_check_result()` uses `gpt_structured()` w/ `GPT_MODEL_41_MINI`, safety escalation detection (safety_score=1 or crisis language).
- RAG: `index_health_check_to_rag()`.
- Job: `app/tasks/health_check.py` `notify_health_check_due()` hourly, 10 PM local. Primary path (therapy day tomorrow): is_due+banner_suppressed+24h dedup→FCM. Fallback path (no schedule): banner_suppressed + 30d window (`_FALLBACK_WINDOW_DAYS`) + 14d activity gate→FCM (P0 fix 2026-05-14: was spamming daily).
- Model `TherapyHealthCheck`: safety_score, heard_score, direction_score, open_ended_prompt/response(encrypted), relationship_state, state_label, observation(encrypted), suggested_questions(encrypted JSON), is_safety_escalation, is_first_check_in, check_in_number, processing_status, xp_awarded.

## Prep Card Auto-Generation + Morning-of Notification (2026-03-28)
NOTE: as of 2026-08-10 this cron job runs successfully every hour but has produced ZERO
rows ever in prod — see [[prep-cards-diagnosis-2026-08-10]] for the full diagnosis before
relying on any of the mechanics below actually mattering in practice.
- `auto_generate_prep_cards()` in `app/tasks/prep_card_auto_generate.py`. Cron `30 * * * *` (before `notify_prep_reminder` at :00 next hour). Window: 23-25h before session; skips if COMPLETED card already in 48h pre-session window (not filtered by generation_type). Helpers: `_run_ai_generation()` (2 attempts), `_store_prep_card_result()`, `_enqueue_rag_indexing()`. Scheduler: `setup_hourly_prep_auto_generate()`.
- `notify_prep_reminder()`: when card exists, sends "card is ready" + deep-link; else sends create-prompt with `data={"type":"prep_card_notification","route":"prep_card_create"}`.
- `notify_prep_morning_of()`: 1-3h window, DND check, deep-links to card if exists. Time format `strftime("%I:%M %p").lstrip("0")`. Scheduler: `setup_hourly_prep_morning_of()`.
- FCM deep-link keys: `type:"prep_card_notification"`, `route`("prep_card"/"prep_card_create"), `prep_card_id`(str, when exists).

## AI Card Content Quality Overhaul (2026-03-29)
- `InputLength` enum (SHORT/MEDIUM/LONG) + `classify_input_length()` + `_MIN_OUTPUT_RATIO` dict, top of openai_service.py.
- `SessionCardTopic` gained optional `context`. `SessionCardResult` gained required `session_snapshot`+`reflection_prompt`. `BetweenSessionNoteResult` gained required `significance` + optional `thread_connection`.
- `DEBRIEF_SESSION_CARD_PROMPT` redesigned: 6 sections + principles + few-shot example (escape `{{}}` in JSON-like example text when using `.format()`).
- Length-tier addenda: `DEBRIEF_LENGTH_SHORT/MEDIUM/LONG_ADDENDUM`, `BSN_LENGTH_SHORT/MEDIUM/LONG_ADDENDUM`.
- `WEEKLY_THERAPY_SUMMARY_PROMPT`: word limit 300→500, richer sections, cross-week continuity instruction.
- `ENHANCED_PREP_CARD_PROMPT`: added CRITICAL QUALITY RULES block (quotes, specificity, traceability).
- Quality gate in `generate_session_card()`/`generate_between_session_note()`: if output_words < input_words*min_ratio AND input_words>50 → retry once, keep better output, never raises.
- RAG indexing extended: `index_debrief_to_rag()` now indexes `session_snapshot`; `index_between_session_to_rag()` indexes `significance`+`thread_connection` (COMPLETED path only).
