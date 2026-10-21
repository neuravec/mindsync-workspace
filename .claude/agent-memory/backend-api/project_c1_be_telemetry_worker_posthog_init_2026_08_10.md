---
name: project-c1-be-telemetry-worker-posthog-init-2026-08-10
description: C1-BE handoff (recording_processing_*/prep_card_auto_generated wiring) uncovered that the RQ worker dyno never called init_posthog() at all -- root-caused and fixed, plus the RQ func.__module__ gotcha that made the fix incomplete on first pass
metadata:
  type: project
---

Commit `177c026` (main, local, NOT pushed). Task: two "small" wiring fixes
from analytics-reports/2026-08-10-c1-dead-instrumentation-review.md
("Backend" section), which turned into a real root-cause fix after
reconciling with a parallel B10 report and a mid-task coordinator escalation
citing db-reports/2026-08-10-insight-job-check.md.

## What actually happened (short version)

1. `recording_processing_started/completed/failed` were reported as "only
   wired into a path that doesn't execute" (Whisper fallback, assuming
   AssemblyAI is primary per a stale docstring). Cross-checking against B10
   (`.claude/agent-memory/backend-api/recording_pipeline.md`, same-day, real
   DB evidence) showed the opposite: chunked upload -- the only path with
   real traffic -- always enqueues the Whisper worker, never AssemblyAI.
   **Lesson**: when two same-day reports disagree about "which code path is
   live," trust the one backed by live DB/traffic evidence over one backed
   by a docstring or an assumption. No code change was needed for this half
   -- the instrumentation was already in the right function.

2. So why was PostHog volume still zero for an event correctly wired into
   the actually-executing function? Root cause: `app.services.posthog_service
   .capture()` silently no-ops whenever its module-level `_client` is
   `None`, and `_client` is only ever set by `init_posthog()` -- which was
   ONLY called from `app/main.py`'s lifespan. The Heroku `worker` dyno runs
   bare `rq worker` (Procfile) and never imports `app.main`. This is the
   exact same class of bug as the same-day
   [prep-card worker-logging fix](project_prep_card_zero_rows_logging_fix_2026_08_10.md)
   (`app/core/logging_config.py` / `app/tasks/__init__.py`), just for
   PostHog instead of logging. Fixed by also calling `init_posthog()` from
   `app/tasks/__init__.py`.

3. **The `app/tasks/__init__.py` fix alone was NOT sufficient** -- a
   coordinator message (relaying `database-administrator`'s
   `db-reports/2026-08-10-insight-job-check.md`) caught this before the
   task was marked done. `app/tasks/__init__.py` only runs when Python
   imports the `app.tasks` PACKAGE, which only happens if the scheduled
   job's function is *defined* in a module under `app.tasks`. **RQ resolves
   a job on the worker via `func.__module__` + `func.__qualname__` --
   determined by where the function is DEFINED, not by which module
   happened to `import` and schedule it.** Audited every `func=` in
   `app/core/rq_scheduler_setup.py`: every scheduled job was already defined
   under `app.tasks.*` EXCEPT `deactivate_expired_subscriptions` (hourly
   job, source of the `trial_ended` `outcome="expired"` event from B12),
   which lived in `app.services.subscription_service`. Fixed by adding
   `app/tasks/subscriptions.py` -- a thin wrapper function (delegates,
   doesn't reimplement) whose only purpose is to give the RQ func_name a
   home under `app.tasks` -- and rewiring `rq_scheduler_setup.py` to import
   the wrapper instead of the service function directly.

## Reusable gotcha for any future worker/RQ wiring task

**A "from X import Y; schedule(func=Y)" re-export does NOT change what RQ
resolves on the worker.** `func.__module__` is fixed at function DEFINITION
time; importing the name into a different namespace before scheduling it
changes nothing. To make an RQ-scheduled function resolve through
`app.tasks.__init__` (or any other package-level init), the function itself
must be DEFINED in a module under that package -- a wrapper function that
delegates to the real implementation works and is the pattern used here;
merely re-importing the name does not.

**Before trusting any worker-side singleton-init fix (PostHog, logging,
anything gated behind `app/tasks/__init__.py`) is complete, audit every
`func=` in `app/core/rq_scheduler_setup.py` for which module each one is
actually defined in** -- not just the one job the current task happens to
be about. This task only caught the `subscriptions.py` gap because a
different agent (`database-administrator`) independently traced a DIFFERENT
symptom (`inapp_insight.generated` silence) back to the same root cause and
flagged it before the task was marked done.

## Endpoint deprecation-not-deletion pattern (reused from
[[msv32-fix1-gfix-2026-07-17]] backward-compat lesson)

`POST /prep-cards/auto-generate` (`app/api/v1/endpoints/prep_cards.py`) had
its sole Flutter client removed same-day (C1-FE). Chose to keep the
endpoint (docstring-annotated `DEPRECATED`, telemetry removed) rather than
delete it, because a removed endpoint 404s for any pre-C1-FE app build still
in the field -- consistent with the standing policy that "no live
consumer" grep results only prove the CURRENT client tree has none, not
that no shipped build calls it.

## Files touched this task
- `app/tasks/__init__.py` -- added `init_posthog()` alongside
  `configure_logging()`
- `app/tasks/subscriptions.py` -- NEW, thin wrapper (this file was already
  named in CLAUDE.md's ownership map but never actually existed until now)
- `app/core/rq_scheduler_setup.py` -- import `deactivate_expired_subscriptions`
  from `app.tasks.subscriptions` instead of `app.services.subscription_service`
- `app/tasks/prep_card_auto_generate.py` -- emits `prep_card_auto_generated`
  (`source="auto_cron"`) after `generated += 1`
- `app/api/v1/endpoints/prep_cards.py` -- removed the dead capture, added
  `DEPRECATED` docstring to `auto_generate_prep_card`
- `app/tests/test_worker_posthog_init.py`,
  `test_subscription_job_worker_wiring.py`,
  `test_prep_card_auto_generate_posthog.py` -- NEW
- `app/tests/test_recording_posthog_events.py`,
  `test_scheduler_idempotency.py` -- updated (header reconciliation note;
  patch-target path for the moved subscription job)

No code change to `app/tasks/session_recording.py` -- confirmed already
correct.

## Verification
Full suite: 20 failed / 5022 passed -- matches the known pre-existing
baseline composition exactly (custom-therapy-sessions x2, first-impression
x1, notification-improvements x4, onboarding-v2 x1, symptom-suggestions x1,
therapy-frequency x5, voice-fixes x5, walkthrough x1). No regressions.
