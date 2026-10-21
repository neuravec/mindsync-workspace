# Backend-emitted event volume verification (task C1) – raw PostHog extract

- **Date**: 2026-08-10 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: all-time since ingest start (2026-04-22) → 2026-08-10
- **Question**: for a data-analytics "dead instrumentation" review, does each of 13 named backend-emitted events have any all-time volume, and if so how much / from how many people / over what date range?
- **Event verification**: queried directly against `events` with `timestamp > toDateTime('2026-04-22')` (full project history) grouped by event name. An event absent from the grouped result set has zero rows in the entire project history — no separate `--events` check needed, this is a stronger all-time confirmation.

## Results

| # | Event | Total events (all-time) | Distinct persons | First seen | Last seen | Status |
|---|---|---|---|---|---|---|
| 1 | `inapp_insight.generated` | 4 | 3 | 2026-06-29 | 2026-07-23 | Flowed, then **stopped** — nothing since 2026-07-23 (18 days silent as of 2026-08-10) |
| 2 | `inapp_insight.shown` | 14 | 5 | 2026-07-04 | 2026-08-08 | Still flowing, most recent of the four |
| 3 | `inapp_insight.dismissed` | 1 | 1 | 2026-07-16 | 2026-07-16 | Fired once, never again |
| 4 | `inapp_insight.acted` | 5 | 2 | 2026-07-20 | 2026-08-07 | Still flowing (thin) |
| 5 | `weekly_summary_generated` | 0 | 0 | — | — | **Never fired, ever** |
| 6 | `monthly_audit_generated` | 0 | 0 | — | — | **Never fired, ever** |
| 7 | `report_generated` | 0 | 0 | — | — | **Never fired, ever** — consistent with your code-search finding that the name doesn't exist in the backend |
| 8 | `report_exported` | 0 | 0 | — | — | **Never fired, ever** |
| 9 | `recording_processing_started` | 0 | 0 | — | — | **Never fired, ever** |
| 10 | `recording_processing_completed` | 0 | 0 | — | — | **Never fired, ever** |
| 11 | `recording_processing_failed` | 0 | 0 | — | — | **Never fired, ever** |
| 12 | `recording_chunk_store_failed` | 0 | 0 | — | — | **Never fired, ever** |
| 13 | `prep_card_auto_generated` | 0 | 0 | — | — | **Never fired, ever** |

### `inapp_insight.generated` vs `.shown` — weekly breakdown (all-time)

`generated`:

| week (UTC, Mon start) | count | distinct users |
|---|---|---|
| 2026-06-28 | 1 | 1 |
| 2026-07-12 | 1 | 1 |
| 2026-07-19 | 2 | 2 |

Nothing in any week after 2026-07-19.

`shown`:

| week (UTC, Mon start) | count | distinct users |
|---|---|---|
| 2026-06-28 | 1 | 1 |
| 2026-07-05 | 2 | 1 |
| 2026-07-12 | 1 | 1 |
| 2026-07-19 | 2 | 2 |
| 2026-07-26 | 3 | 3 |
| 2026-08-02 | 5 | 5 |

**Read on the generated-vs-shown question**: this is not a timing/backfill artifact. `generated` and `shown` ran in the same weeks through 2026-07-19 (both present, roughly matched volume), then `generated` went completely silent while `shown` kept growing through the most recent week (2026-08-02, 5 users). If `shown` genuinely depended on a prior `generated` event, `shown` volume would have stopped too — it didn't. Two explanations consistent with the data: (a) `shown` fires from a different/decoupled code path than the one that emits `generated` (e.g. `shown` fires on every insight render including cached/already-generated insights, while `generated` only fires on fresh generation, and generation itself broke or stopped being called ~2026-07-23), or (b) the `generated` emitter call was removed/refactored out around that date while the `shown` emitter was left in place. Only the backend code can distinguish these — recommend `data-analytics` check `git log` on the insight-generation code path around 2026-07-23 for a refactor that dropped the `posthog.capture` call.

## Caveats

- All counts are all-time totals since PostHog ingest start (2026-04-22); nothing exists before that date so this window is already the maximum possible.
- n is very small for every one of the four `inapp_insight.*` events (1–5 distinct persons) — these are directional signals of "does the code path ever run," not statistically meaningful usage numbers. Not suppressed under the k-anonymity rule because this is raw instrumentation-verification (same category as reporting single-user event skew elsewhere in this project), not a demographic/behavioral segment breakdown.
- The 9 zero-volume events were confirmed via a single grouped query against the full event table (`GROUP BY event` over all history) — an event name absent from that result set has categorically never appeared in any ingested row, this is not a sampling/lookback-window artifact.
- `report_generated` zero-PostHog-volume finding corroborates your backend code-search result (event name not found in codebase) — two independent methods agree it's simply not implemented anywhere, not a "implemented but silently failing" case.
- For the other 8 zero-volume events, I did not check whether the code path that should emit them exists/is called — that determination (dead emitter code vs. code path never reached vs. name typo vs. never implemented) is exactly what task C1 is for and is data-analytics' call, not something PostHog data can resolve on its own.

## Queries

```sql
-- @@ all_events_summary
SELECT
  event,
  count() AS total_events,
  count(DISTINCT person_id) AS distinct_users,
  min(timestamp) AS first_seen,
  max(timestamp) AS last_seen
FROM events
WHERE timestamp > toDateTime('2026-04-22')
  AND event IN (
    'inapp_insight.generated', 'inapp_insight.shown', 'inapp_insight.dismissed', 'inapp_insight.acted',
    'weekly_summary_generated', 'monthly_audit_generated',
    'report_generated', 'report_exported',
    'recording_processing_started', 'recording_processing_completed', 'recording_processing_failed',
    'recording_chunk_store_failed', 'prep_card_auto_generated'
  )
GROUP BY event
ORDER BY event

-- @@ weekly_summary_by_week
SELECT toStartOfWeek(timestamp) AS week, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'weekly_summary_generated' AND timestamp > toDateTime('2026-04-22')
GROUP BY week ORDER BY week

-- @@ monthly_audit_by_week
SELECT toStartOfWeek(timestamp) AS week, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'monthly_audit_generated' AND timestamp > toDateTime('2026-04-22')
GROUP BY week ORDER BY week

-- @@ inapp_insight_generated_by_week
SELECT toStartOfWeek(timestamp) AS week, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'inapp_insight.generated' AND timestamp > toDateTime('2026-04-22')
GROUP BY week ORDER BY week

-- @@ inapp_insight_shown_by_week
SELECT toStartOfWeek(timestamp) AS week, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'inapp_insight.shown' AND timestamp > toDateTime('2026-04-22')
GROUP BY week ORDER BY week
```
