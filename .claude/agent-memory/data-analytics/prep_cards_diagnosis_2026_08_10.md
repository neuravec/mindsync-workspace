---
name: prep-cards-diagnosis-2026-08-10
description: Prep-card auto-generation cron runs successfully forever but has produced zero rows in prod; manual capture is the only working path. Diagnosis-only, no fix applied.
metadata:
  type: project
---

Full report: `analytics-reports/2026-08-10-prep-cards-diagnosis.md`.

Facts (verified live against prod, 2026-08-10):
- `app/tasks/prep_card_auto_generate.py` (`auto_generate_prep_cards`, hourly cron at :30
  via `setup_hourly_prep_auto_generate()` in `app/core/rq_scheduler_setup.py`, called from
  `app/main.py` lifespan) is correctly registered in RQ Scheduler on prod and executes
  successfully every hour (confirmed via RQ `FinishedJobRegistry` — 92 retained runs since
  2026-03-30, 0 in `FailedJobRegistry`; watched a live tick at 10:30:58 UTC complete in
  1.8s with "Job OK"). Despite this, `session_prep_cards.generation_type='auto'` has
  **0 rows, ever** (total table: 115 rows, 86 manual + 29 legacy-null, 0 auto).
- The job's eligible population is tiny: `UserSubscription.is_active=True` (this IS the
  premium/in-trial gate — see `_create_initial_subscription` in `users.py`) AND
  `UserPreferences.therapy_schedule IS NOT NULL`. As of 2026-08-10: 9 users out of 1800
  total. Only 138/1800 users (7.7%) have `therapy_schedule` set at all.
- **Observability gap**: the worker process does not emit this module's `logger.info(...)`
  lines (not even the function's first-line "START" log) to Heroku logs at all — logging
  level filtering in the worker swallows INFO, only WARNING/ERROR surface (confirmed a
  sibling job's `logger.error` line WAS visible: `[WEEKLY_THERAPY_SUMMARY] Error for user
  ...: can't compare offset-naive and offset-aware datetimes`, live in worker logs
  2026-08-10 10:13-10:16 UTC — separate pre-existing bug in that job, not prep-cards).
  This means DB inspection was the only way to get ground truth; log tailing could not
  distinguish "0 users ever entered the per-user loop" from "N entered, all silently
  skipped/failed". Flagged to backend-api as a cross-cutting fix (affects debugging every
  `app/tasks/*` job, not just this one).
- `POST /prep-cards/auto-generate` (synchronous on-demand version, the ONLY place that
  emits the `prep_card_auto_generated` PostHog event) is dead code from the client's
  perspective — `PrepCardManager.autoGeneratePrepCard()` in
  `mindsync-frontend/.../prep_card_manager.dart` is defined but has zero call sites
  anywhere in `lib/`. This alone fully explains that event's 365-day silence in PostHog,
  independent of the cron.
- The manual capture flow (Main tab "Prepare" CTA -> `TherapyFlowLauncher` ->
  `getLatestPrepCard()` -> if no match, routes to `prep_question_flow_screen.dart` ->
  `POST /prep-cards/` or `/prep-cards/voice`) is the **only** path that has ever produced
  a prep card in prod, and it works correctly (111/115 rows COMPLETED). It's just used by
  few people — total lifetime distinct users nearly matches debrief (57 vs 47) but recent
  30d reach is lower (9 vs 11 users) and 14d PostHog reach much lower (6 vs 17).
- `app/utils/therapy_schedule_utils.py` (`compute_next_session_date` and friends) IS
  tz-aware end-to-end by code inspection — the naive/aware bug affecting
  WEEKLY_THERAPY_SUMMARY does not appear to be the same code path as prep-card auto-gen's
  date math (worth double-checking if this diagnosis is revisited, since both jobs use the
  same shared utility for other calls).
- The `SessionPrepCard` "already exists" skip-check in the cron (COMPLETED card within 48h
  before session) does NOT filter by `generation_type` — a manually-created card also
  suppresses the auto path for that session. Contributory but not proven as the sole
  cause (4 of the 9 currently-eligible users have never created ANY prep card, auto or
  manual, and still show 0 auto rows).

Handoffs recommended (not executed — diagnosis task only):
- backend-api: fix worker logging level so `app/tasks/*` INFO logs are actually visible
  (cross-cutting, not prep-card-specific).
- backend-api/data-analytics: once logging is fixed, watch one real tick against the
  live population before touching entry-window/skip logic — don't guess blind.
- flutter-mobile: wire up or delete `autoGeneratePrepCard()` + retire
  `prep_card_auto_generated` telemetry (currently pure dead code, misleading in PostHog).
- ui-ux-designer/lead: `therapy_schedule` setup gates the entire next-session card
  (prep+debrief+between-sessions) behind a step only 7.7% of users complete — a product
  reach question, not just a generation-pipeline bug.

Diagnostic technique notes for next time: RQ `FinishedJobRegistry`/`FailedJobRegistry`
(via `rq.registry`) on the `default` queue is a much more reliable way to check "has this
scheduled job actually executed and did it error" than tailing Heroku logs — the log
buffer only spans ~8-10 minutes of worker output in this app (high volume from
per-user FCM debug lines), nowhere near enough to catch an hourly job by chance. Query the
registries directly instead; filter `job.func_name` for the task's dotted path.
