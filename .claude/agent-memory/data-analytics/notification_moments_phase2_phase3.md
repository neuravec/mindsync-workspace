---
name: notification-moments-phase2-phase3
description: Phase 2/3 push-moment generators + in-app insight detectors + adaptive scoring for the Notification Orchestrator (2026-05-15), plus the 2026-05-15 audit remediation that followed.
metadata:
  type: project
---

## Phase 2 (COMPLETE)
- `app/services/moments/post_session_reflection_generator.py`: base_score=9.0, 26h debrief window, anti-double via scoring_signals.debrief_id, delay from notification_preferences.post_session_nudge_delay_minutes (default 30), expires_at=scheduled_at+24h, 7-language static fallback.
- `app/services/moments/__init__.py` / `app/services/insights/__init__.py`: import all generators/detectors to auto-register.
- `app/services/insights/reveal_insight_detector.py`: STATS_TAB_OPENED only, 14d data gate, 20% delta threshold, TOAST, dedup="REVEAL:{name}:{iso_week}-{year}", is_ai_generated=False.
- `app/services/insights/celebrate_tease_insight_detector.py`: triggers=[APP_OPENED,DEBRIEF_SAVED,NOTE_ADDED], tease_streaks={2,6,29}, INLINE_BANNER, dedup="CELEBRATE_TEASE:{target}:{user_id}:{date}", expires EOD next day.
- 89 tests across 4 files, all pass. Dedup method is `_is_duplicate` (not `_is_dedup_blocked`).

## Phase 3 (COMPLETE)
Push generators:
- `mood_dip_alert_generator.py`: base_score=8.0, AI-generated, fires when ≥3 recent negative-symptom scores all ≥7, anti-spam 5d/symptom_id, scheduled_at=now+1h.
- `streak_celebration_generator.py`: base_score=7.0, TEMPLATED, milestones={3,7,30,100,365}, anti-dup via scoring_signals.target_milestone, scheduled_at=now+5min.
- `pattern_insight_generator.py`: base_score=7.5, AI-generated, ≥10 entries/30d + recurring topic (≥3/14d) + no PATTERN_INSIGHT in 14d, scheduled_at=now+2h, expires+48h.

In-app detectors:
- `notice_insight_detector.py`: APP_OPENED only, INLINE_BANNER, TEMPLATED, best-time-of-day(>60%) or most-active-weekday(>40%), dedup="NOTICE:{observation_type}:{user_id}:{iso_week}-{year}", expires end of ISO week, _MIN_ENTRIES=5.
- `recovery_moment_insight_detector.py`: [STATS_TAB_OPENED,APP_OPENED], BOTTOM_SHEET, AI-generated, old_avg≥7(28-56d ago) AND new_avg≤4(14d), _MIN_SCORES_PER_WINDOW=3, dedup="RECOVERY:{symptom_name}:{user_id}:{quarter}", expires+7d.
- `comparative_insight_detector.py`: [DEBRIEF_SAVED,NOTE_ADDED], TOAST, TEMPLATED, milestones=[10,25,50,100] cumulative entries/month, dedup="COMPARATIVE:{count}:{user_id}:{year_month}", expires+6h.

Adaptive scoring on NotificationOrchestrator:
- `notification_categories.py` (NEW): MOMENT_TYPE_TO_CATEGORY + INSIGHT_TYPE_TO_CATEGORY + ALL_CATEGORIES.
- `crud/notification_moment.py`: `get_action_rates_by_type(db, user_id, since)`.
- `notification_orchestrator.py`: (0) notification_enabled guard, (2.5) interest filter via notification_interests (before is_eligible), (5) action-rate boost: acted/sent≥0.60 AND sent≥3 → score×1.5.
- notification_enabled/intensity/interests read from UserPreferences w/ JSON fallback.

Tests: 7 files, 179 new tests, all pass. Full suite at the time: 2895 passed / 69 pre-existing failures (unrelated).

## Audit Remediation (2026-05-15, COMPLETE)
- CRIT-01+04: `deliver_due_moments()` in `notification_orchestrator_job.py` — claim-before-send atomic FCM delivery. Scheduler `setup_frequent_moment_delivery()` (*/15 cron).
- CRIT-03: Redis lock on `run_daily_orchestrator` + `deliver_due_moments` via `_acquire_redis_lock()`.
- dedup_key added to `MomentCandidate` dataclass; all 4 generators set it; `_persist_moment` forwards/generates fallback.
- HIGH-04: `POST /insights/trigger` → 202+{queued:True}, enqueues `run_insight_detection` RQ task (contract change for integration-devops).
- HIGH-01: `_load_eligible_users` uses `joinedload(User.preferences)`, SQL filter notification_enabled=True.
- HIGH-05: crisis safety clause in `_DEFAULT_MOMENT_TEXT_GENERATOR_PROMPT`; MoodDipAlertGenerator suppresses when all 3 scores ≥9 (`_SEVERE_DISTRESS_THRESHOLD=9`).
- HIGH-07: `_is_session_rate_limited` counts both `get_shown_insights_in_window` AND `get_generated_insights_in_window` (burst-trigger race fix).
- New tests: test_moment_delivery.py(13), test_dedup_key_generators.py(14), test_insight_detection_async.py(3); several existing files extended.

## Foundation (2026-05-14) — see `notification_orchestrator_foundation.md` for full detail
- Key CRUD: `count_moments_scheduled_today`, `get_dismissal_counts_by_type`, `get_shown_insights_in_window`, `get_insight_by_dedup_key`.
- Config key `MOMENT_TEXT_GENERATOR_PROMPT`. Scheduler `setup_hourly_notification_orchestrator()`.
- Endpoints: GET /moments/upcoming, POST /moments/{id}/opened|dismissed|acted, GET /insights/pending, POST /insights/trigger, POST /insights/{id}/shown|dismissed|acted.

## Still pending as of last check — verify before relying on
1. backend-api: UserPreferences columns `notification_enabled`(bool,True), `notification_intensity`(int 0/1/2), `notification_interests`(JSON list=ALL_CATEGORIES) + migration.
2. backend-api: `app/main.py` lifespan imports `app.services.moments` and `app.services.insights` (noqa F401) to trigger auto-registration.
