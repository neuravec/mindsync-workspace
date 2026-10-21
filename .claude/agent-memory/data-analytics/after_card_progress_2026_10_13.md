---
name: after-card-progress-2026-10-13
description: After card "Your progress in therapy" panel backend (branch feat/after-card-progress, NOT pushed 2026-10-13): formula v1, min-data guard, triage already covers recording/reflect_summary
metadata:
  type: project
---

GET /api/v1/analytics/therapy_progress (commit 66d5f4f, worktree MindSync-wt-cards-progress). Logic lives in `app/services/analytics.py` (this was the first content in that file), schema in `app/schemas/analytics.py`. The client gates it with the PostHog flag `after_card_progress_panel` (default off). There is no backend kill switch, because config.py is owned by backend-api.

**Why:** card redesign iteration 5 (Darek, 13.10). YMYL: the labels are descriptive only, there is no numeric score in copy and no red.

**How to apply:**
- Formula v1: sessions are non-deleted `session_debriefs` ordered by session_date. Each session's stretch is (previous session, this session]. The first stretch defaults to 14 days. wellbeing = (10 - mean of per-symptom means) / 9. engagement = min(notes+recordings+talks, 4) / 4. value = 0.75*wellbeing + 0.25*engagement. A stretch with no check-ins carries the last wellbeing forward. Label = least-squares slope times (n - 1), with a threshold of +/-0.08.
- Minimum data: 3 sessions, check-ins in 2 or more stretches, 3 or more ratings, and 3 or more points with a value. Otherwise it returns 200 with status insufficient_data. A missing, deleted or foreign card returns 404.
- "Talks" counts ALL conversations (JOURNAL + REFLECT). `conversations.user_id` has no index in the migrations; ask database-administrator to check pg_indexes before scaling.
- Triage save-to-Workspace already supports card_type `recording` and `reflect_summary` (all 4 kinds). Timeline item "reflect" maps to ReflectSummaryCard.
- Pre-existing failure: test_reflect_summary::test_upgrade_downgrade_roundtrip_on_sqlite (SQLite syntax error in a migration), not caused by this work. Importing the full app.api.v1.api locally hangs; import single endpoint modules instead.

**v2 (2026-10-14, commit 4431568 on feat/progress-panel-v2, NOT pushed):** v1 guards above are SUPERSEDED. The panel is shown to everyone with no flag. `status` is ok or locked, and it is locked below 3 sessions of any kind. Sessions are deduped by the user's local day (UserPreferences.time_zone) and come from debriefs, recordings (session_date, falling back to created_at) and prep cards where generation_type is not "auto" and session_date is in the past. Auto prep cards are excluded because they are no proof a session happened. Stretches are local days `[start, end)`. Null-free fill works in this order: carry forward (also from ratings in the 28 days before the window), back-fill from the first in-window check-in, then neutral 0.5. When the window has no check-ins, harder_stretch is turned into holding_steady. The window is padded forward to 3 points for early cards. The full v1 router-mount QA test took about 8 minutes on py 3.14 on 10-14 (15 s on 10-18).

## Consent gate (2026-10-14, commit 7b73892 on feat/progress-panel-v2)
- Withdrawn PROFILING (latest record withdrawn_at set; no record = allowed) -> 200 locked, locked_reason "profiling_consent_required", zero data reads. Uses raising `consent_crud.is_consent_withdrawn` (NOT `is_profiling_consent_withdrawn`, which fails closed and would turn a DB error into a false lock); DB error -> 500.
- Precedence: consent before debrief_id 404 (no existence oracle) before too_few_sessions.
- Test trick: SQLAlchemy `before_cursor_execute` spy on db.get_bind() to prove no data tables are queried.
- L-3 log rule: exception type only; also don't pass user_id to parse_timezone (its warning logs the id).
