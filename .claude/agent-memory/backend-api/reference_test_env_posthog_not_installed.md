---
name: test-env-posthog-not-installed
description: Local `py -3.12` has no posthog package, so two worker-import subprocess probes fail on any branch; not a regression
metadata:
  type: reference
---

On the operator's Windows machine, `py -3.12 -c "import posthog"` fails with ModuleNotFoundError (verified 2026-10-19). As a result, `init_posthog()` cannot create a client locally, and these two subprocess probes fail on an untouched base commit (75d1f0d) as well:

- `test_worker_posthog_init.py::TestWorkerOnlyImportPathInitialisesPostHog::test_worker_import_path_initialises_posthog_without_app_main`
- `test_subscription_job_worker_wiring.py::TestWorkerOnlyImportOfSubscriptionsJobInitialisesPostHog::test_worker_import_path_for_subscription_job_initialises_posthog`

The SDK contract test in `test_posthog_identify_sdk3.py` is skipped for the same reason (importorskip).

**How to apply:** treat these two failures as environmental. They are not regressions. Confirm on a clean base worktree if in doubt. To exercise PostHog delivery in tests, set `posthog_service._client` to a fake that records `set` / `set_once` / `flush` calls (pattern in `test_posthog_person_props_consent.py`).

Gotcha: `has_accepted_agreements(MagicMock(), uid)` returns True (a MagicMock row is non-None). Routed mock DBs that return `None` from `.first()` for unknown queries make it False. When the consent gate makes a mock-based test go silent, that is the reason.
