# Feature Details (Archived from MEMORY.md)

## Key Model: UserProfile
- Table: `user_profile`
- Columns: id, user_id, age, full_name, pronouns, gender, first_day_of_week, device_type, has_used_promo_code, last_promo_code

## Key Model: UserStreak (added 2026-02-21)
- Table: `user_streaks`
- CRUD: `get_or_create_user_streak`, `update_streak_on_conversation`, `break_streak_if_missed`, `backfill_user_streaks`

## Gamification Router (completed 2026-02-21)
- Endpoint: `gamification.py` — GET /journey_summary
- Background job: `tasks/gamification.py` — `run_daily_streak_break_check()` + `setup_daily_streak_check()`

## Therapy Companion + Character Card (NOT YET ON DISK — see audit note)
- Models: `TherapySession`, `UserXP`, `UserCharacterStats`
- XP rank logic: `XP_RANKS` list + `_resolve_xp_tier(total_xp)` helper in crud.py

## Session Prep Cards (added 2026-02-28)
- Model: `SessionPrepCard` in models.py
- Shared helpers: `_therapy_helpers.py`
- Shared free tier limit: `count_ai_notes_this_month` counts BOTH debriefs + prep cards

## Reflect Chat (added 2026-03-01)
- Endpoint: `reflect.py` — 10 endpoints
- CRITICAL route ordering: /starters and /usage BEFORE /{conversation_id} paths
- RAG: `find_similar_combined` for context injection

## Weekly Therapy Summary (added 2026-03-01)
- Model: `WeeklyTherapySummary`
- Migration: `h8c9d0e1f2g3`

## Session Recordings (added 2026-03-02)
- Model: `SessionRecording` — 7 encrypted summary sections + fallback fields
- AssemblyAI service, background job with 30min timeout
- Migration: `i9d0e1f2g3h4`

## Security Fix Patterns (2026-02-22)
- Per-resource cap: raise ValueError in CRUD; endpoint catches → HTTP 400
- Idempotency via bool flag: `xp_awarded` column pattern
- Pydantic v2 temporal validator: `@field_validator("field", mode="before")`
