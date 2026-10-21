---
name: notification-orchestrator-foundation
description: Notification Orchestrator + InAppInsightDetector Phase 1 foundation — file locations, key patterns, enums, test gotchas
metadata:
  type: project
---

## Phase 1 Foundation (2026-05-14)

### Key files created
- `app/services/notification_orchestrator.py` — orchestrator singleton, MomentCandidate, MomentGenerator protocol
- `app/services/in_app_insight_detector.py` — detector singleton, InsightCandidate, InsightDetector protocol, InsightTrigger enum
- `app/services/moment_text_generator.py` — AI text generator helper (GPT_MODEL_41_MINI), GeneratedMomentText schema
- `app/services/notification_observability.py` — structured logging + PostHog event helpers
- `app/schemas/notification_moment.py` — NotificationMomentResponse, MomentStatusUpdate
- `app/schemas/app_insight.py` — AppInsightResponse, InsightTriggerRequest
- `app/api/v1/endpoints/moments.py` — GET /moments/upcoming, POST /moments/{id}/opened|dismissed|acted
- `app/api/v1/endpoints/app_insights.py` — GET /insights/pending, POST /insights/trigger, POST /insights/{id}/shown|dismissed|acted
- `app/tasks/notification_orchestrator_job.py` — RQ hourly job (expires stale moments, purges insights, runs orchestrator)
- `app/core/rq_scheduler_setup.py` — added `setup_hourly_notification_orchestrator()`
- `app/api/v1/api.py` — registered /moments and /insights routers

### Files extended (by backend-api, then I added functions)
- `app/crud/notification_moment.py` — I added `count_moments_scheduled_today()` and `get_dismissal_counts_by_type()`
- `app/crud/app_insight_shown.py` — I added `get_shown_insights_in_window()` and `get_insight_by_dedup_key()`
- `app/core/config.py` — I added `MOMENT_TEXT_GENERATOR_PROMPT: str = ""`

### Actual model enums (confirmed from models)
- `MomentTypeEnum`: POST_SESSION_REFLECTION, MOOD_DIP_ALERT, STREAK_CELEBRATION, PATTERN_INSIGHT, THERAPY_PREP, REFLECTION_INVITATION, WEEKLY_RECAP, ACHIEVEMENT_UNLOCK
- `MomentStatusEnum`: PENDING, SENT, OPENED, DISMISSED, ACTED, EXPIRED
- `InsightTypeEnum`: REVEAL, PATTERN, NOTICE, CELEBRATE_TEASE, RECOVERY_MOMENT, COMPARATIVE
- `FormFactorEnum`: TOAST, INLINE_BANNER, BOTTOM_SHEET

### Rate limiting
- notification_intensity 0→limit 0, 1→limit 1, 2→limit 2
- Dismissal window: 7 days, threshold ≥3 → score × 0.5
- Insight session window: 30min, max 1 per session
- BOTTOM_SHEET form_factor extends cooldown to 60min

### Test patch gotchas
- `OpenAIService` must be at module level in `moment_text_generator.py` → patch `app.services.moment_text_generator.OpenAIService`
- `SessionLocal` in job is imported lazily inside function → patch `app.db.session.SessionLocal`
- `get_orchestrator` in job → patch `app.services.notification_orchestrator.get_orchestrator`
- `create_insight` in CRUD uses `server_default` for `generated_at` → never pass `generated_at` kwarg

### Feature flag
- `settings.notification_legacy_jobs_enabled = True` (default) — legacy jobs kept ON in Phase 1/2
- Phase 1: orchestrator runs hourly but creates 0 moments (empty registry) — this is CORRECT behaviour

**Why:** Foundation for notification redesign. Phase 2 will register first concrete generators.
**How to apply:** Phase 2 generators call `get_orchestrator().register(MyGenerator())` in rq_scheduler_setup.py before the hourly job fires.
