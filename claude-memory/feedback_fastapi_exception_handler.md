---
name: FastAPI exception handler doesn't catch HTTPException
description: FastAPI's @app.exception_handler(Exception) does NOT catch HTTPException — must register dedicated handlers for HTTPException + RequestValidationError
type: feedback
originSessionId: 4ba60075-8a3b-4f21-945a-b81a50d5c9a4
---
`@app.exception_handler(Exception)` catch-all in FastAPI/Starlette **does NOT fire for `HTTPException` or `RequestValidationError`**. Each has its own dedicated built-in handler that intercepts before the generic one. Must register explicit `@app.exception_handler(StarletteHTTPException)` and `@app.exception_handler(RequestValidationError)` if you want centralized behavior on 4xx.

**Why:** Discovered 2026-05-04 while diagnosing why PostHog `api_error` event had 0 occurrences despite 30+ capture sites. The catch-all was registered but only fired for raw 5xx exceptions (rare in prod). All 401/403/404/422 went through FastAPI's built-in handlers and bypassed our analytics. Fix in `app/main.py` — three explicit handlers + shared `_capture_api_error` helper.

**How to apply:**
- For analytics/logging cross-cutting on errors: register all three handlers — `StarletteHTTPException`, `RequestValidationError`, `Exception`.
- Use `starlette.exceptions.HTTPException as StarletteHTTPException` (FastAPI HTTPException subclasses Starlette's, so this catches both).
- For PostHog property `endpoint`: ALWAYS use `request.scope.get("route").path` (route template like `/api/v1/conversations/{conversation_id}/end`), NEVER `request.url.path`. Raw URL path leaks resource IDs (PII risk for mental-health domain) and explodes PostHog property cardinality. Fall back to `"<unmatched>"` when scope has no route (404 bot scans of `/wp-admin/` etc).
- For 422 body: mirror FastAPI's stock shape via `jsonable_encoder({"detail": exc.errors()})` and only add `body` key when `exc.body is not None` — don't always emit `body: null`.
- In exception handlers: read distinct_id directly from `request.headers.get("x-posthog-distinct-id")` instead of contextvar — Starlette `BaseHTTPMiddleware` contextvar propagation is fragile across exception-handler task boundaries.
- NEVER forward `exc.detail`, `str(exc)` or exception messages to PostHog — therapy content can leak. Only metadata: method, route template, status_code, and `type(exc).__name__` as `error_class`.
