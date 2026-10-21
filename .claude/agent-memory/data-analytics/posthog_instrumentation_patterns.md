---
name: posthog-instrumentation-patterns
description: How PostHog event instrumentation is structured in this codebase (posthog_service.py helpers, shared-function-for-multiple-triggers pattern, generated-vs-read event design) - reference before adding any new server-side event.
metadata:
  type: project
---

## Shared-emission-point pattern (2026-08-10, summaries domain)

When the same logical event ("X was generated") can be triggered from more
than one code path (an auto/cron path and a manual/on-demand endpoint path),
put the actual `capture()` call behind ONE function in
`app/services/posthog_service.py` that takes the varying bits as parameters
(e.g. `trigger: "auto"|"manual"`, `is_regeneration: bool`). Every call site
just calls that one function. This is what makes the property shape
impossible to drift between paths - discovered this was already a problem
before the fix: `weekly_summaries.py`/`monthly_audits.py` had ad hoc
`posthog_capture(event="X_generated", properties={"summary_id":...,
"on_demand": True})` at /generate and a DIFFERENT event name
("X_regenerated") with a different property shape at /retry, while the
auto-cron job in `app/tasks/*.py` emitted nothing at all for the same
logical action. Found by actually reading all the call sites, not by
trusting the task description's "this event has never fired" framing (it
was half right - true for the auto path, false for the manual path, which
already fired an old, differently-shaped event).

Concrete pattern added: `capture_summary_generated(distinct_id, *,
period_type, trigger, period_start, is_regeneration, record_id=None)` in
`app/services/posthog_service.py` (see [[api_contracts]] sibling file for
this domain's other contracts). Selects the event name from `period_type`
internally so callers can't typo two different event strings for the same
concept. `period_start` is deliberately reduced to a bare ISO **date**
(never a datetime with time-of-day) since it identifies the reporting
PERIOD, not a creation timestamp - callers pass whatever they have (date or
datetime) and the helper normalizes.

## Auto-job internal-retry gotcha

Both `weekly_therapy_summary.py::_process_user` and
`monthly_therapy_audit.py::_process_user` have an in-job AI retry (one retry
before marking FAILED) that is a SEPARATE success branch in the same
function, not a caller-level retry. Any post-generation hook (moment/FCM,
RAG enqueue, and now the PostHog emission) needs to fire from BOTH the
primary success branch and the retry-success branch, or the ~5-10% of
generations that only succeed on the second attempt silently skip
instrumentation. Grep for the job's own docstring/log line
("Retry succeeded") to find the second branch - it's easy to miss since
it's ~150 lines below the primary success block.

## Testing an emission point without a live PostHog

Patch the CALLING module's imported name (`patch.object(task_module,
"capture_summary_generated")` or `patch.object(endpoint_module,
"capture_summary_generated")`), not `posthog_service.capture_summary_generated`
directly - every call site does `from app.services.posthog_service import
capture_summary_generated`, which binds a local name in that module's
namespace. Patching the source module only affects call sites that look it
up dynamically (`posthog_service.capture_summary_generated(...)`), not
call sites using the imported local name. Mirrors the existing convention
in this codebase for `crud`/`openai_service`/etc (see [[Testing Patterns]]
in MEMORY.md for the `_ensure_rq_importable()` Windows fork-mock pattern
these same test files need alongside this).

For the auto-job full-`_process_user`-run tests specifically: `is_user_premium`
is imported LOCALLY inside `monthly_therapy_audit.py::_process_user` via
`from app.api.v1.endpoints._therapy_helpers import is_user_premium` (not a
module-level import) - patch the source
`app.api.v1.endpoints._therapy_helpers.is_user_premium`, not
`task.is_user_premium` (the latter doesn't exist as a module attribute on
the task module at all).

## Diagnostic recipe: "event X fired once/never" (2026-08-10, realizations domain, B5)

Same "half right" trap as the summaries case above, worse: `grep -rn
"<event_name>" app/` first, before touching detection/threshold theories.
If there is exactly ONE call site emitting the event, that call site's
trigger condition IS the full explanation for the count - don't reach for
"threshold too high" or "job not deployed" until you've ruled out "the
emitting code path is simply the wrong/minor one of several that create the
underlying row." Found: `realization_detected` had one emitter
(`app/api/v1/endpoints/realizations.py:175`, the MANUAL tagging endpoint),
while the AI auto-detection job (`app/tasks/realization_detection.py
::detect_realizations_for_source`, the thing the event name actually
describes) creates rows directly via `db.add()/commit()` with zero posthog
import. Two other silent creators exist too
(`app/crud/workspace.py::get_or_create_realization_for_triage`). Whenever a
row-creating action has >1 code path, expect at most one of them to be
instrumented until proven otherwise.

Three-step verification order that settled this fast: (1) code grep for the
event string, count emitters; (2) `git merge-base --is-ancestor <commit>
heroku/main` per relevant commit to separate "not deployed" from "deployed
but buggy" - Fix2 (8a80e81) and Fix4 (3c55f8d) were NOT on heroku/main, but
the base Realizations commit (4d8388b) with the actual gap WAS, so deploy-lag
was a red herring for this specific event even though it's real for other
undeployed code in the same files; (3) prod DB row counts by the
distinguishing column (`is_auto_detected`) via database-administrator -
149 auto rows vs 12 manual, most recent auto row hours old, proved the
"job never actually runs" hypothesis wrong where an RQ FinishedJobRegistry
sample (200-job window, high-volume shared queue) was inconclusive. DB row
timestamps beat RQ registry sampling when the queue is busy/shared - the
registry only gives you the last N jobs across ALL job types, easy to
scroll past a low-frequency job's entries.

Ownership note: emission-point files for a given feature are not
automatically data-analytics's even when the story is "an event never
fires" - check the File Ownership Map per file. `app/tasks/realization_detection.py`
and `app/api/v1/endpoints/realizations.py` both belong to backend-api (not
in the data-analytics `app/tasks/{summaries,charts,notifications}.py` /
`app/api/v1/endpoints/{analytics,summaries,dashboard}.py` list) - diagnosed
but handed off, not patched directly.
