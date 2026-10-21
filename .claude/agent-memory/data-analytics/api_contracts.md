---
name: api-contracts
description: Analytics/summary/gamification API contracts delivered to integration-devops/flutter-mobile — dashboard insight, weekly summaries, character card, monthly audits.
metadata:
  type: reference
---

- `GET /api/v1/dashboard/conversation/{id}/insight` — see `patterns.md` for full contract.
- `GET /api/v1/weekly-summaries/` (list, latest, get, update, retry) — see `features.md` for full schema.
- `GET /api/v1/gamification/character_card` — see `patterns.md` for full response schema.
- `GET /api/v1/monthly-audits/` (list, latest, get/{id}, retry/{id})
  - AUTH: required. Premium gating: free users see `activity_summary` only.
  - `MonthlyTherapyAuditResponse`: id, report_year, report_month, activity_summary|null, topic_frequency([{topic,mention_count}])|null, symptom_trends([{symptom_name,start_score,end_score,direction,description}])|null, breakthroughs([{date,text,source}])|null, patterns|null, movement_assessment|null, movement_type|null, limited_data:bool, is_first_audit:bool, premium_locked:bool, data_window_start/end:datetime, processing_status:str, created_at/updated_at:datetime.
  - `POST /api/v1/monthly-audits/{audit_id}/retry` — AUTH required, PREMIUM required (403 if not). STATUS: 202 success, 400 already_processed, 404 not_found, 500 AI failed.

## Character Card Feature (Phase 2)
- Service: `app/services/character_card_service.py` — 4 radar stats + therapeutic alliance + emotional delta.
- Endpoint: `GET /gamification/character_card`.
- Premium gate: `UserSubscription.is_active`. Unlock: `days_since_registration >= 7 AND finished_conversations >= 5`.
- XP: +10 base, +50 if in 2h debrief window. `award_xp`/`get_or_create_user_xp` in crud.py.
- Config defaults: `CHARACTER_STATS_PROMPT`, `THERAPEUTIC_ALLIANCE_PROMPT` have Python-level defaults.
