---
name: Token Usage Tracking System
description: Comprehensive OpenAI token tracking with cost calculation, admin API, and monthly email reports — implemented 2026-04-01
type: project
---

Token usage tracking system implemented across the full backend.

**Why:** CEO needs visibility into OpenAI API costs per feature/model/month, with automated monthly email reports.

**How to apply:** All OpenAI calls now auto-log to `token_usage_log` table. Admin endpoints at `/admin/usage/` (secured by X-Admin-Key header). Monthly report emails on 1st of each month.

Key components:
- Migration `aa1b2c3d4e5f`: creates `token_usage_log` + `model_pricing` tables (down from `z6u7v8w9x0y1`)
- `app/services/usage_tracking.py`: `track_usage()` context manager (contextvars) + `log_token_usage()` fire-and-forget
- `app/services/openai_service.py`: 5 base methods instrumented (gpt_function, gpt_structured, generate_embeddings, tts_response, speech_to_text)
- `app/services/openai_audio_service.py`: 3 methods instrumented
- 30+ endpoint/task/service files wrapped with `track_usage()`
- `app/crud/usage.py`: aggregation queries (overview, daily, trends, top-users, pricing upsert)
- `app/schemas/usage.py`: Pydantic response models
- `app/api/v1/endpoints/admin_usage.py`: 6 admin endpoints (overview, daily, trends, top-users, pricing, report/send)
- `app/tasks/usage_report.py`: monthly HTML email report via SMTP
- Config: ADMIN_API_KEY, ADMIN_REPORT_EMAILS, SMTP_* settings
- Scheduler: `setup_monthly_usage_report()` cron `0 6 1 * *`
- Pricing seed data: gpt-5.4-mini, text-embedding-3-small, gpt-4o-mini-tts, gpt-4o-mini-transcribe, gpt-realtime-1.5
- SMTP credentials moved from hardcoded in email_service.py to config
