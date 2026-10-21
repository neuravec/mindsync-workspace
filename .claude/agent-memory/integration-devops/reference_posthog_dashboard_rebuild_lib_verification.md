---
name: posthog-dashboard-rebuild-lib-verification
description: How to safely apply the $lib='posthog-flutter' hygiene filter across a whole dashboard-build script without silently zeroing backend or dual-sourced events. Read before editing scripts/posthog_build_dashboards.py or any script that filters PostHog insights by $lib.
metadata:
  type: feedback
---

# $lib verification before applying hygiene filters to dashboard scripts

**Rule**: never assign an event's client/backend origin (and therefore whether it
gets the `$lib='posthog-flutter'` + testflight/emulator hygiene filter) from
where its name appears in the codebase (filename, doc comment, constant
definition location). Verify with a fresh, per-event query:

```sql
SELECT event, properties.$lib AS lib, count() n
FROM events
WHERE timestamp > now() - INTERVAL 90 DAY AND event IN (...)
GROUP BY event, lib ORDER BY event
```

**Why**: doing the 2026-08-10 PostHog dashboard rebuild (task C4,
`analytics-reports/2026-08-10-dashboards-rebuild-plan.md`), a first draft
classified `notification_received` as backend because the string appeared in
`app/tasks/notification_orchestrator_job.py` — but that was only a doc-comment
*naming* the client event; the actual capture call is in the Flutter
`main.dart` FCM handler. A fresh `$lib` query caught it (100% `posthog-flutter`)
before the wrong client=False was shipped. This was caught mid-task by a
parallel B7 finding — do the verification proactively, don't wait for someone
else to catch it.

## Three classes an event can fall into

1. **Client-only** (`posthog-flutter` 100%) → apply the full hygiene filter
   (`client=True` in `scripts/posthog_build_dashboards.py`'s `event_series()`).
2. **Backend-only** (`posthog-python` 100%) → apply NO filter (`client=False`).
   Backend events never carry `$lib='posthog-flutter'`, `$is_testflight`, or
   `$is_emulator` at all — filtering them the same way as client events zeroes
   them out completely, it doesn't clean them up. Confirmed backend-only in
   this project as of 2026-08-10: `reflect_session_started`,
   `reflect_session_ended`, `api_error`, `realization_detected`,
   `consent_revoked`, `user_activated` (code-inspection only, 0 live events to
   verify against — see below), `weekly_summary_generated`,
   `monthly_audit_generated`.
3. **Dual-sourced** — fires independently from BOTH client and backend for the
   same logical action. Also needs `client=False` (no filter), but for a
   different reason: dropping the `$lib` filter here isn't "skip the hygiene
   check", it's "count both legitimate sources instead of silently discarding
   one of them". Confirmed dual-sourced in this project as of 2026-08-10:
   `subscription_purchase_completed` (5 flutter + 3 python /90d — client fires
   optimistically, backend confirms after receipt verification) and
   `consent_granted` (16 flutter + 18 python /90d).

A 4th, easy-to-miss case: **web SDK events** (`$pageview`, `$web_vitals`,
`$lib='web'`) are neither of the above — also `client=False` (no app filter),
but because they're marketing-site traffic by construction, not because
they're backend or dual-sourced. Don't reuse `client=False` reasoning
uninspected between these two very different cases; document which one applies
per insight (see the rebuild-plan report's per-dashboard tables for the
pattern).

## When an event has zero live volume

If an event's code exists but it has 0 events in the last 90d, you cannot
verify its `$lib` empirically — fall back to code inspection (which module
calls `capture()` vs `AnalyticsEvents.logEvent()`) and say so explicitly in
the insight description/report rather than presenting it as verified. Track
these separately as "awaiting deploy" (code shipped, not live yet — a
solvable, time-bound state) vs. "awaiting instrumentation" (task C1, no code
at all yet) — conflating the two undersells how close the awaiting-deploy ones
are to being useful.

See also [[posthog-default-exclusion-filters]] (owned by posthog-data-extractor,
`.claude/agent-memory/posthog-data-extractor/reference_default_exclusion_filters.md`)
for the underlying filter mechanics and NULL-safety verification this builds on.
