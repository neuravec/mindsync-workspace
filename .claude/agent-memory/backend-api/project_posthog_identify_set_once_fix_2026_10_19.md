---
name: posthog-identify-set-once-fix-2026-10-19
description: Backend PostHog identify() never delivered person props (TypeError on set_once kwarg, 2026-04-25..10-19); fixed via SDK set/set_once in 75d1f0d, unpushed; SDK version traps on this box
metadata:
  type: project
---

`posthog_service.identify()` called `_client.identify(..., set_once=...)`; posthog-python 3.x (pin `>=3.7.0,<4.0.0`, resolves 3.25.0) has no such kwarg, so every backend identify raised TypeError (swallowed) from c5ee63d (2026-04-25) until the fix. Fix 75d1f0d on `fix/posthog-identify-set-once` (worktree MindSync-wt-posthog-identify, upstream unset, NOT pushed as of 2026-10-19): `$set` via `_client.set`, set-once via `_client.set_once`, each only when non-empty, warning logs method + exception type only (no uid, no exc message, no exc_info: SDK `require()` echoes values).

**Why:** person props from the backend (subscription_tier, plan, premium_source, onboarding_completed, age_band, gender, signup_date, auth_provider, streak_max, conversations_last_30d, premium_intent_score) never reached PostHog; every `$identify` in PostHog is posthog-flutter. After deploy they start arriving for the first time, and event volume rises (one `$set` per POST /users/ cold start, one per user per weekly premium_intent run).

**How to apply:**
- SDK traps here: py3.12 has NO posthog (tests are mock-only; worker-init subprocess tests `test_worker_posthog_init` + `test_subscription_job_worker_wiring` fail on base for that reason); py3.14 has posthog 7.10.3 where `identify` does not exist at all. Never trust local SDK for signature checks.
- Real-SDK offline check: `pip download "posthog>=3.7.0,<4.0.0" backoff monotonic --no-deps`, extract wheels, put on sys.path/PYTHONPATH, stub `Client._enqueue(self, msg, disable_geoip)` to record messages. Running `test_posthog_identify_sdk3.py` with that PYTHONPATH un-skips the installed-SDK contract tests.
- `_client` is the `posthog` module (module-level API), not a `Client` instance.
- Related: [[posthog-api-error-classification]]
