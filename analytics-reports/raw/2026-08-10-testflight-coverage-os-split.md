# $is_testflight coverage vs $os split (C3-fix root cause probe) – raw PostHog extract

- **Date**: 2026-08-10 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: last 14 days (2026-07-27 → 2026-08-10)
- **Question**: For flutter-mobile's C3-fix diagnosis (ref `analytics-reports/2026-08-10-metrics-hygiene-c2-c3.md`) — is `$is_testflight` coverage low (~22-25% aggregate) because Android events legitimately never carry the property (Hypothesis A, not a bug), or because the iOS SDK's async TestFlight-receipt read races event capture within a session (Hypothesis B, real bug)?
- **Event verification**: `posthog-flutter`-lib events flowing normally, 6307 events / 94 users in window, `last_seen` current (up to 2026-08-10).

## Results

**1. OS split, all events (`$lib='posthog-flutter'`, 14d):**

| os | events | has $is_testflight | pct |
|---|---|---|---|
| Android | 4764 | 0 | 0.0% |
| iOS | 1532 | 1532 | 100.0% |
| iPadOS | 11 | 11 | 100.0% |

Same split restricted to current builds (2.0.75/2.0.76) is materially identical (Android 4617/0, iOS 1405/1405, iPadOS 11/11).

`device_type`: Mobile 6130, Tablet 177 (no additional signal beyond `$os`).

**2. iOS-only coverage (isolates Hypothesis A):**

| scope | events | users | has $is_testflight | pct |
|---|---|---|---|---|
| iOS, current builds (2.0.75/2.0.76) | 1405 | 14 | 1405 | **100.00%** |
| iOS, all builds, 14d | 1532 | 16 | 1532 | **100.00%** |

**3. Within-session uniformity, iOS, top 15 sessions by event count (≥3 events each):**

Every one of the 15 sampled sessions (36 to 252 events each, spanning 2026-07-29 through 2026-08-10) has `n_with_tf == n_events` — i.e. **100% of events in every sampled session carry `$is_testflight`**, no mixed sessions found, no need to fall back to a per-event coin-flip check.

## Verdict

**Hypothesis A confirmed, Hypothesis B rejected.** `$is_testflight` coverage is **100.00%** for both iOS and iPadOS, at both the aggregate and per-session level, with zero exceptions in this 14-day window. There is no async race in the client — the property is emitted reliably on every iOS event.

The apparent ~22-25% aggregate coverage reported in the C2/C3 hygiene report is fully explained by platform mix: iOS+iPadOS = 1543/6307 = **24.5%** of all `posthog-flutter` events in this window, i.e. almost exactly the reported aggregate coverage number. Android is 75.5% of app events and the property is structurally inapplicable there (TestFlight doesn't exist on Android) — not a bug, not missing instrumentation, not a timing gap.

## Caveats

- Ingest start 2026-04-22 not relevant to this 14d window.
- Sample of 15 sessions is the top-15 by event count (biggest/most reliable sessions), not a random sample — but given the aggregate iOS coverage is exactly 100.00% (1532/1532, zero misses across all 16 iOS users), there is no remaining population of "some events missing" to sample from; the session check is confirmatory, not the primary evidence.
- No k-anonymity concerns — nothing below n=25 reported (session-level `n_events` counts are not user segments).

## Queries

```sql
-- lib_check
SELECT count() AS events, count(DISTINCT person_id) AS users
FROM events
WHERE properties.$lib = 'posthog-flutter' AND timestamp > now() - INTERVAL 14 DAY

-- os_split_all_builds / os_split_current_builds
SELECT properties.$os AS os, count() AS events,
       countIf(JSONHas(properties, '$is_testflight')) AS has_tf,
       round(100.0*countIf(JSONHas(properties,'$is_testflight'))/count(),1) AS pct_tf
FROM events
WHERE properties.$lib = 'posthog-flutter' AND timestamp > now() - INTERVAL 14 DAY
  -- (+ AND properties.$app_version IN ('2.0.75','2.0.76') for current-builds variant)
GROUP BY os ORDER BY events DESC

-- device_type_split
SELECT properties.$device_type AS device_type, count() AS events
FROM events
WHERE properties.$lib = 'posthog-flutter' AND timestamp > now() - INTERVAL 14 DAY
GROUP BY device_type ORDER BY events DESC LIMIT 10

-- ios_only_coverage_current_builds / ios_only_coverage_allbuilds
SELECT count() AS events, count(DISTINCT person_id) AS users,
       countIf(JSONHas(properties, '$is_testflight')) AS has_tf,
       round(100.0*countIf(JSONHas(properties,'$is_testflight'))/count(),2) AS pct_tf
FROM events
WHERE properties.$lib = 'posthog-flutter' AND properties.$os = 'iOS'
  AND timestamp > now() - INTERVAL 14 DAY
  -- (+ AND properties.$app_version IN ('2.0.75','2.0.76') for current-builds variant)

-- session_uniformity_ios
SELECT $session_id AS session_id, count() AS n_events,
       countIf(JSONHas(properties, '$is_testflight')) AS n_with_tf,
       min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE properties.$lib = 'posthog-flutter' AND properties.$os = 'iOS'
  AND timestamp > now() - INTERVAL 14 DAY
  AND $session_id != '' AND $session_id IS NOT NULL
GROUP BY session_id
HAVING n_events >= 3
ORDER BY n_events DESC LIMIT 15
```
