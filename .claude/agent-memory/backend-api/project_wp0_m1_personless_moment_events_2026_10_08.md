---
name: project-wp0-m1-personless-moment-events-2026-10-08
description: WP-0 security M-1/L-1/L-3 fix (branch fw/be0-sec, commit 8eb8d3f, not pushed); person-less moment.* rules, residual client leak via deep_link_route, dashboard breakage, test gotchas
metadata:
  type: project
---

Security review WP-0 M-1 closed on branch `fw/be0-sec` (commit 8eb8d3f, from feat/first-week-home 68d62fa), NOT pushed as of 2026-10-08.

- Single source: `app/services/moment_privacy.py` (`HEALTH_REVEALING_MOMENT_TYPES`, 11 fixed values + WP-1 plan step via `push_cadence.PLAN_STEP_MOMENT_TYPE`). `posthog_track_moment` (in notification_observability.py, NOT posthog_service.py, despite lead task text) decides person-less; every call site must pass `account_anchor=` (AST guard test enforces it). Unknown type or age = person-less (fail closed).
- Person-less interaction events (opened/dismissed/acted) carry NO moment_type on purpose: they fire inside the user's own request, so identified client events land within ms and a type would be trivially re-joinable by time.
- **Why:** an in-therapy-only type on an identified PostHog person is an Art. 9 inference.
- **How to apply:** a new MomentTypeEnum member fails `test_every_enum_member_is_classified` until classified; WP-1 must set PLAN_STEP_MOMENT_TYPE (the set picks it up). The decision uses the WALL CLOCK, so tests must set `created_at` relative to real now, not to a fixed orchestrator `now`.

Residuals reported to lead (not fixable backend-only):
- Flutter `notification_opened` also carries `deep_link_route` (`/fab/prepare-therapy`, `/health-check`, ...), which reveals the type even without `moment_type`. Needs a flutter-mobile change.
- Timing correlation between person-less backend events and identified client/backend events is possible in principle.
- `scripts/posthog_build_dashboards.py` "[Jobs] Users the notification job touched" (math=dau on moment.scheduled) inflates: each person-less event is its own random distinct_id.

Env gotcha: local py3.12 has no `posthog` package, so `test_worker_posthog_init.py` fails on base too (pre-existing, not a regression). See [[test_baseline_pytest_history]].
