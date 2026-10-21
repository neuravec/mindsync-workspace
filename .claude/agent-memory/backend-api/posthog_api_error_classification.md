---
name: posthog_api_error_classification
description: is_expected tagging for the PostHog api_error event, and the dependency-free-module pattern used to make main.py-adjacent classification logic unit-testable
metadata:
  type: project
---

## What (2026-08-10)

PostHog's `api_error` event (fired from `app/main.py::_capture_api_error`, wired
into the `StarletteHTTPException` / `RequestValidationError` / generic
`Exception` handlers) used to capture every response >= 400 identically. Live
data check (14d window): 4507 events / 60 users, but only ~20 were real
failures. The rest were designed behavior:
- 2617 events: 404 "no record yet" empty states on four `/latest` GET routes
  — `/api/v1/prep-cards/latest`, `/api/v1/debriefs/latest`,
  `/api/v1/between-sessions/latest`, `/api/v1/health-check/latest` (all raise
  `HTTPException(404, "not_found")` purely because the query returned no
  rows for a brand-new user).
- 1870 events: 403 on `POST /api/v1/reflect/{conversation_id}/message` when
  the daily/monthly message limit gate fires (`reflect.py:490`), plus the
  premium-required voice gate (`reflect.py:768`) — intentional policy
  responses, not auth failures. This codebase returns 404 (not 403) for
  cross-user access attempts, so **any** 403 raised as `HTTPException` in
  this app is a deliberate limit/permission gate, never a leaked security
  exception — that's why the 403 classification rule is route-agnostic.

## Fix

Added `app/services/api_error_classification.py` — a small, stdlib-only
module exposing `EXPECTED_EMPTY_STATE_404_ROUTES` (frozenset of route
templates) and `is_expected_api_error(status_code, endpoint, error_class)`.
Wired into `_capture_api_error` in `app/main.py` to add an `is_expected`
boolean property on every `api_error` event. **The HTTP response returned to
the client is completely unchanged** — this only tags the analytics event.

Classification rule: 404 is expected only on the four allowlisted routes OR
when no route matched at all (`endpoint == "<unmatched>"`, i.e. bot scans of
paths that were never part of this API). 403 is expected only when
`error_class == "HTTPException"`. Everything else (500s, 422s, 409s, 400s,
and 404s on any non-allowlisted route) stays `is_expected=False` so real
bugs and broken deep links keep full visibility.

## Reusable pattern: dependency-free classifier module for main.py logic

`app/main.py` cannot be imported under pytest (see MEMORY.md's "Never
`import app.main` directly under pytest" note) — conftest.py's dummy
`FIREBASE_CREDENTIALS` breaks `initialize_firebase()`, which runs
unconditionally at module scope. The established test-suite convention
(`test_main_lifespan_orchestrator.py`) works around this via source-level
`Path.read_text()` + string/AST assertions instead of a real import — fine
for verifying *wiring* ("is X called from lifespan") but useless for testing
actual *logic*.

For logic that needs real behavioral unit tests (branching, edge cases),
extract it into a small stdlib-only module under `app/services/` that
`main.py` imports from. This module can be imported directly and normally
in pytest (no rq/Firebase/DB mocking needed at all), giving fast, real
`assert` coverage instead of brittle string-matching. Verify the extracted
module truly stays dependency-free with an AST-based test (walk
`ast.parse(source).body` for top-level `Import`/`ImportFrom` nodes, assert
only `__future__`) — this also guards against the module accidentally
regaining an import that could make it a boot-time risk again.

## Offline verification recipe used

Same recipe as [[offline_verification]] but needed one extra step: the
direct `import app.main` (bare `python`, not pytest) only works because
`app.core.config` has a real fallback dummy-credentials-**file** default
(`app/firebase_dummy_credentials.json`, checked into the repo) when
`FIREBASE_CREDENTIALS` is unset — conftest.py's pytest-only override to a
literal (incomplete) JSON *string* is what breaks it under pytest, not a
general problem with the app's defaults.

To verify route-template strings actually match live route.path values
(needed here since PostHog data referenced human labels like
"health-check/latest" but the real registered path — worth double-checking
prefixes rather than guessing):
```
PYTHONPATH="." "/c/Users/mikol/AppData/Local/Programs/Python/Python312/python.exe" script.py
```
with `DB_URL=sqlite:///:memory:`, `MESSAGE_ENCRYPTION_KEY=<fernet key>`,
`REDISGREEN_URL=redis://localhost:6379/0` set, and `rq`/`rq_scheduler`/
`tiktoken`/`fpdf`/`assemblyai` stubbed via `sys.modules` — then inspect
`{r.path for r in app.routes if hasattr(r, "path")}`.
