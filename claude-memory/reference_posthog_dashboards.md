---
name: PostHog Dashboards
description: 9 dashboards + 50 insights provisioned 2026-04-23 from POSTHOG_ANALYTICS_PLAN.md; script at scripts/posthog_build_dashboards.py is idempotent
type: reference
originSessionId: f4fa2b36-88c7-452b-b375-353183c3a0fb
---
## State (2026-04-23)
9 dashboards created in PostHog EU project 141170 via `scripts/posthog_build_dashboards.py`.

- Onboarding Health — dashboard/638505 (7 insights, 9-step funnel ordered not strict)
- Activation & Time-to-Value — dashboard/638506 (5 insights)
- Core Engagement — dashboard/638507 (6 insights, 7d retention)
- Therapy Loop Health — dashboard/638508 (5 insights)
- Monetization — dashboard/638509 (5 insights, funnel stops at product_selected)
- Feature Adoption Matrix — dashboard/638510 (4 insights)
- Health & Quality — dashboard/638511 (6 insights: 4 marketing web-vitals + 2 mobile)
- Gamification Impact — dashboard/638512 (6 insights)
- Account Health — dashboard/638513 (6 insights)

## Script behavior
- Idempotent — `find_dashboard_by_name()` checks existence before creating
- `--dry-run` prints plan, `--force` creates duplicates
- Requires env vars POSTHOG_PERSONAL_API_KEY + POSTHOG_PROJECT_ID (no hardcoded keys)

## Insights pending backend events (not yet emitted by backend — dashboards will populate when they flow)
- `debrief_created`, `prep_card_created`, `between_session_created` (activation funnel uses *_started proxies)
- `subscription_purchase_completed`, `paywall_shown`, `promo_code_applied` (monetization funnel stops early)
- `account_deleted`, `profile_updated`, `therapy_context_updated` (churn signals)
- `api_error`, `client_error` (quality dashboard incomplete)
- `level_up`, `user_registered` (gamification + auth signals)
- `notification_opened`, `health_check_*`, `symptom_*`, `goal_*`, `reflect_*` (no events flowing yet — whole domains missing from dashboards)

## Data caveat
PostHog ingest started 2026-04-22. Retention windows clamped to 7 days on -14d window. Web-vitals insights source from marketing site www.mindsync.app (mobile doesn't emit them).

## Useful API paths
- `GET /api/projects/141170/event_definitions/` — list flowing events
- `GET /api/projects/141170/property_definitions/?type=event` — event properties
- `PATCH /api/projects/141170/dashboards/{id}/ {"deleted":true}` — soft delete (hard DELETE returns 405)
