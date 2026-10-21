---
name: period-card-endpoint-2026-10-18
description: GET /analytics/period_card (Weekly/Monthly card chart + Monthly stats), commit f3b00ac on feat/cards-v3, pushed to origin feature branch only; gotchas for weekly windows, Realization NULL default, tracked test_temp.db
metadata:
  type: project
---

Cards v3 (team cards, 18.10) backend task BE1: read-only `GET /api/v1/analytics/period_card?weekly_summary_id=|monthly_audit_id=`
in `app/services/analytics.py` ("Period card extras" section, `get_period_card_extras`), schemas `PeriodCardResponse`
in `app/schemas/analytics.py`, tests `app/tests/test_period_card.py` (62). Commit f3b00ac, pushed to
origin/feat/cards-v3 only (NOT main, not deployed). Final contract: team scratch `teams/cards/API.md`.

**Why:** Weekly/Monthly "How you felt" line + Monthly stats tiles of the 18.10 card redesign; client is PeriodCardCubit.

**How to apply:**
- Gate order: card lookup by id+user (404) -> monthly premium lock (`user_was_premium or is_user_premium`, same as
  GET /monthly_audits/{id}; nothing else read) -> raising PROFILING consent check (series locked, counts kept).
- Weekly window is stored `[Mon 00:00 local, next Mon 00:00 local)`: last day = local day of `end - 1us`. First card
  is signup-clamped (fewer buckets); legacy rolling windows give 8 days; capped at 14 most recent.
- Sessions count reuses `_load_session_events` + `collect_sessions` (loads all of the user's sessions per call, bounded
  5000/source). If the Timeline lists many cards and this gets slow, add optional window bounds to that loader.
- Test gotcha: `Realization(show_on_timeline=None)` is stored as TRUE (ORM applies the Python default to an explicit
  None). Write NULL with a raw `UPDATE` to exercise the legacy NULL case. A guard assertion caught a fake mutation pass.
- `test_temp.db` at the backend repo root is TRACKED and gets modified by pytest/boot checks: `git checkout -- test_temp.db`
  before committing.
- Offline boot check script that works: scratch `teams/cards/boot_check.py` (conftest env + rq mocks + firebase patch,
  asserts the route is mounted; 319 routes on 18.10).
- `test_after_card_progress_qa.py` now runs in ~15 s on py 3.14 (the 8-minute note in [[after-card-progress-2026-10-13]] is stale).
