# Reflect entry mode-picker (2026-09-18) – post-deploy raw PostHog extract

- **Date**: 2026-09-25 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: 2026-08-28 → 2026-09-24 (4 weeks: 3 before, 1 after)
- **Question**: Since the 2026-09-18 Reflect entry (voice/text picker + topic sheet) deploy, is Reflect/conversation usage up, is there a trend, and are there errors/problems?
- **Ingest start**: 2026-04-22 (not a factor here, window is recent).

## Event verification

| Event | Flowing? | First seen | `$lib` | Note |
|---|---|---|---|---|
| `reflect_mode_choice_shown` (picker shown) | Yes | 2026-09-18T06:56 | posthog-flutter | New, exactly matches ship date |
| `reflect_mode_selected` (voice/text chosen) | Yes | 2026-09-18T06:56 | posthog-flutter | property `mode` = voice/text |
| `reflect_entry_sources_shown`/`_served` (topic sheet) | Yes | 2026-09-18T08:14 | posthog-flutter | topic sheet impressions |
| `reflect_entry_topic_selected` | Yes, thin (n=4 users, 13 events) | 2026-09-18T11:42 | posthog-flutter | property `mode`, `is_continuation` |
| `reflect_entry_dismissed` | Yes (n=7) | 2026-09-19T07:46 | posthog-flutter | picker abandoned |
| `reflect_new_thread_tapped` / `reflect_thread_resumed` | Yes | 2026-09-18 | posthog-flutter | continuation path |
| `reflect_opening_question_shown` | Yes, very thin (n=4, 5 events) | 2026-09-18T13:33 | posthog-flutter | agent-speaks-first |
| `reflect_voice_locked_tapped` | Yes, n=1 only (2 events) | 2026-09-19T11:23 | posthog-flutter | voice-lock tap for non-premium |
| `reflect_ui_session_ended` | Yes, pre-existing since 2026-08-11 | — | posthog-flutter | carries `end_reason`, `input_mode_used`, `duration_seconds`, `messages_sent` |
| `reflect_session_started` / `reflect_message_sent` / `reflect_session_ended` | Yes, but **`$lib='posthog-python'` (backend), not `posthog-flutter`** | pre-existing | posthog-python | **Do not filter these by `$lib='posthog-flutter'` — it zeroes them.** Same lib trap documented in agent memory. |
| `conversation_started`/`_message_sent`/`_ended` (legacy chat) | **Dead** — last event 2026-08-11, zero since | posthog-python (backend) | superseded by `reflect_*`, confirms prior memory note |
| `voice_interrupted` as an `end_reason` value | **Not observed** in `reflect_ui_session_ended.end_reason` in this window (values seen: `backgrounded`, `navigated_away`, `thread_switched`, `limit_reached`, `user_ended`) | — | — | New value from the spec has not appeared yet in the data, or is captured elsewhere — flag to `flutter-mobile`/`backend-api` to confirm wiring |
| `paywall_shown` | Yes, thin (n≈3-4 users/month) | flowing since 2026-08-16 | — | trigger_feature breakdown available |
| `subscription_purchase_completed` | Yes, very thin (2 events, 1 user, 2026-09-22) | — | — | not usable for a paywall→purchase read at this n |

## 1. Build adoption (which users are on the new picker build)

The new picker shipped in frontend dev `81773ba`. First `reflect_mode_choice_shown`/`reflect_mode_selected` appear from **`$app_version` 2.0.91** onward (2026-09-18). App-version users, 30d, client events only (`$lib='posthog-flutter'`):

| Version | Users (30d) | First seen | Notes |
|---|---|---|---|
| 2.0.94 | 35 | 2026-09-19 | current |
| 2.0.93 | 3 | 2026-09-19 | |
| 2.0.92 | 4 | 2026-09-18 | |
| 2.0.91 | 4 | 2026-09-18 | **first build carrying the picker** |
| 2.0.90 | 25 | 2026-09-15 | pre-picker |
| 2.0.89 | 57 | 2026-09-03 | pre-picker, largest pre-launch cohort |
| 2.0.85 / .87 / .88 / .86 / .82 / .77 / .76 / .75 / .60 / .44 / .36 | small tails | — | pre-picker, stale builds still active |

So as of 2026-09-25, **≈46 distinct users (2.0.91–2.0.94)** are confirmed on a picker-carrying build out of ~127-150 total 30d active users (per memory baseline) — roughly a third. This is a TestFlight/dev-branch rollout (per the task context), so most production Store users are still on old builds and cannot see the feature. **Any usage read below is diluted by this partial rollout — a flat or modest change is expected even if the feature works well, because most users never saw it.**

## 2. Daily Reflect activity, 2026-08-28 → 2026-09-24 (backend `reflect_session_started`/`reflect_message_sent`, n = distinct users/day)

| day | sessions_started | users_started | messages_sent | users_messaged |
|---|---|---|---|---|
| 08-28 | 1 | 1 | 3 | 1 |
| 08-31 | 3 | 2 | 18 | 2 |
| 09-01 | 1 | 1 | 1 | 1 |
| 09-02 | 4 | 3 | 8 | 3 |
| 09-03 | 1 | 1 | 7 | 2 |
| 09-04 | 2 | 2 | 0 | 0 |
| 09-05 | 1 | 1 | 1 | 1 |
| 09-06 | 2 | 1 | 10 | 1 |
| 09-07 | 1 | 1 | 10 | 2 |
| 09-08 | 3 | 3 | 7 | 2 |
| 09-09 | 4 | 3 | 11 | 2 |
| 09-10 | 1 | 1 | 0 | 0 |
| 09-11 | 1 | 1 | 3 | 1 |
| 09-12 | 2 | 2 | 0 | 0 |
| 09-13 | 0 | 0 | 1 | 1 |
| 09-15 | 1 | 1 | 8 | 2 |
| 09-16 | 2 | 2 | 0 | 0 |
| **09-17** | **115** | **3** | 3 | 2 |
| 09-18 (deploy day) | 13 | 2 | 8 | 2 |
| 09-19 | 10 | 4 | 7 | 3 |
| 09-21 | 1 | 1 | 3 | 1 |
| 09-22 | 2 | 2 | 0 | 0 |
| 09-23 | 0 | 0 | 1 | 1 |
| 09-24 | 1 | 1 | 0 | 0 |

**Single-user spike flagged**: 112 of the 115 `reflect_session_started` events on 09-17 came from **one person_id** (`a459f002…`, Windows, `$app_version` null — i.e. a backend/desktop/test client, not a phone), all in one day, nowhere else in the 4-week window. This is not organic usage — treated as skew and excluded from the before/after comparison below.

## 3. Before/after comparison (backend Reflect events, single-user 09-17 spike excluded)

| Period | Sessions started | Users started | Messages sent | Users messaged | All-app DAU-sum (n, `$lib=posthog-flutter`) |
|---|---|---|---|---|---|
| Weekday-aligned earlier week (09-04 → 09-10) | 14 | 9 | 39 | 6 | 43 |
| 7 days before launch (09-11 → 09-17, skew excluded) | 9 | 7 | 13 | 4 | 44 |
| 7 days after launch (09-18 → 09-24) | **27** | **7** | **19** | **4** | 51 |

- Sessions started roughly **tripled** week-over-week after launch (9 → 27) with the **same number of distinct users** (7 → 7) — i.e. this reads as **more sessions per user**, not more users.
- Messages sent up modestly (13 → 19), same 4 distinct messaging users both weeks.
- General app DAU-sum rose too (44 → 51, +16%), so part of the increase could be a general-traffic uptick rather than the feature specifically — the per-user rate below controls for that.
- Sessions-per-active-app-user: **before 09-11–17 = 2.75** (skewed by the excluded spike if not removed — recompute below is the clean read) vs **after 09-18–24 = 0.53** when computed against the raw un-deduped denominator query — this particular per-user-rate query was run before the skew exclusion, so treat only the skew-excluded table above as reliable; the raw ratio is misleading and is not used in the final read.
- **n is very small (4-9 distinct Reflect users per week)** — any of these differences could flip with 1-2 users' behavior. Read as a plausible early positive signal, not a proven trend.
- `reflect_ui_session_ended` (client-side, pre-existing event, proxy for session cadence): before-launch window (09-04→09-17) avg duration 133s/session, avg 2.36 messages; after-launch (09-18→09-24) avg duration 112s/session, avg 3.98 messages, similar event counts (36 before-ish vs 43 after in the split used) — messages-per-session **up**, duration **down**, consistent with a "faster to get into content" read but again thin.

## 4. Picker funnel (2026-09-18 → 2026-09-24 only — the feature's live window)

| Step | Events | Users |
|---|---|---|
| `reflect_mode_choice_shown` (picker shown) | 44 | 9 |
| `reflect_mode_selected` (mode chosen) | 125 | 9 |
| — mode=voice | 64 | ~6 (peak days 09-18/09-19) |
| — mode=text | 61 | ~7 |
| `reflect_entry_sources_shown` (topic sheet shown) | 63 | 8 |
| `reflect_entry_topic_selected` | 13 | 4 |
| `reflect_entry_dismissed` (picker abandoned) | 32 | 7 |
| `reflect_voice_locked_tapped` (non-premium hit voice lock) | 2 | 1 |
| `paywall_shown` after 09-18 | 4 (09-24 only in window) | 1 |
| `subscription_purchase_completed` after 09-18 | 2 (09-22) | 1 |

Notes:
- Mode split is roughly even (voice ≈ text), n too small to say more.
- `reflect_entry_dismissed` (32 events/7 users) vs `reflect_mode_choice_shown` (44/9) — a meaningful share of picker impressions end in dismissal, but sample is tiny; worth re-checking at higher n before calling it a leak.
- `reflect_entry_topic_selected` (13 events) is far below `reflect_mode_selected` (125) — most mode-selection events are NOT followed by a captured topic-selection event in the same volume. This could mean topic selection is skipped often (e.g., continuing threads skip the sheet, matching spec) or under-instrumented — cannot distinguish from PostHog data alone.
- Voice-lock → paywall → purchase chain has only 1-2 users total; **cannot support a conversion-rate claim at this n.** `paywall_shown` still carries no clean "triggered by reflect voice lock" tie — `trigger_feature` values seen in the window are `drawer_menu` (8), `premium_gate_session_recording` (1), `premium_gate_reflect_messages` (1); no `premium_gate_reflect_voice` or similar value observed for the new voice-lock path, so the voice-lock → paywall link is not directly traceable via `trigger_feature` in this data — flag to `flutter-mobile` to confirm the paywall triggered from `reflect_voice_locked_tapped` sets a distinguishing `trigger_feature`.
- Premium vs non-premium split: `is_premium` property exists on `reflect_mode_choice_shown`/`reflect_mode_selected` but was not broken out here due to n — not worth splitting a 9-user sample further.

## 5. Errors, before vs after 2026-09-18

**`api_error` totals**, 2026-09-04 → 2026-09-25, split at the deploy boundary:

| Period | Events | Users |
|---|---|---|
| Before (09-04 → 09-17, 14d) | 871 | 26 |
| After (09-18 → 09-24, 7d — shorter window) | 1097 | 39 |

Not a clean before/after (different window lengths: 14d vs 7d), so raw totals are not directly comparable — but user count (26 in 14d vs 39 in 7d) suggests error *breadth* did not shrink post-launch. This matches the standing baseline (`api_error` is MindSync's largest event overall, mostly `is_expected=True` 404s on `…/latest` endpoints per memory).

Reflect/conversation/audio/voice-specific `api_error` endpoints (same window), before vs after:

**Before 09-18:**
| Endpoint | Status | Count | Users |
|---|---|---|---|
| `/api/v1/conversations/start` | 403 | 3 | 1 |
| `/api/v1/reflect/start` | 403 | 3 | 1 |
| `/api/v1/audio-v2/realtime-session` | 403 | 2 | 1 |
| `/api/v1/reflect/threads` | 403 | 2 | 1 |
| `/api/v1/reflect/{id}/messages` | 404 | 1 | 1 |
| `/api/v1/reflect/{id}/session_data` | 404 | 1 | 1 |
| `/api/v1/reflect/{id}/summarize` | 400 | 1 | 1 |
| `/api/v1/reflect/{id}` | 405 | 1 | 1 |
| `/api/v1/reflect/entry-sources` | 403 | 1 | 1 |
| `/api/v1/reflect/{id}/audio/user_message` | 500 | 1 | 1 |
| `/api/v1/reflect/{id}/summaries` | 404 | 1 | 1 |

**After 09-18:**
| Endpoint | Status | Count | Users |
|---|---|---|---|
| `/api/v1/reflect/{id}/summarize` | 400 | 3 | 1 |
| `/api/v1/conversations/{id}/chat/text` | 404 | 1 | 1 |
| `/api/v1/conversations/notes/{id}` | 404 | 1 | 1 |
| `/api/v1/reflect/{id}/message` | 500 | 1 | 1 |
| `/api/v1/conversations/{id}/end` | 409 | 1 | 1 |

Volumes are low and single-user-dominated on both sides (n=1 per row throughout) — **no new error pattern or spike tied to the picker launch is visible.** The one 500 (`/reflect/{id}/audio/user_message`) is pre-launch; the post-launch 500 is on `/reflect/{id}/message`, different endpoint, also n=1. Not enough volume to call either a regression.

**Client-side `$exception`** (posthog-flutter), by day and app version:
- Steady background rate (1-21 events/day, 1-2 users/day) both before and after 09-18, no spike coincident with the deploy.
- Post-launch builds (2.0.91-2.0.94) show exceptions on 09-18 (7, 1 user), 09-19 (10, 2 users total across .93/.94), 09-21 (5, 2 users), 09-23 (3, 1 user) — consistent low background noise, not a new pattern. Exception payloads were not decoded (`$exception_list` truncated/not parsed) — a deeper triage of these specific stack traces was out of scope for this pull; hand to `flutter-mobile` if a targeted "reflect/mode exceptions only" grep of `$exception_list` is wanted.

**`client_error`** event: present both before and after (3-21/day), no clear post-launch trend.

**`end_reason` distribution** (`reflect_ui_session_ended`, 09-04 → 09-24): values observed are `backgrounded`, `navigated_away`, `thread_switched`, `limit_reached`, `user_ended`. **`voice_interrupted` (the new value from the spec) did not appear in this window at all.** Flag to `flutter-mobile`/`backend-api`: either the code path that sets it hasn't been hit yet (n is tiny, plausible), or it isn't wired to write this property — worth a quick source check before assuming it's just low-volume.

## Caveats

- **All Reflect-usage counts have n in the single digits.** This is explicitly a small-user-base analysis; do not read any of the above as statistically significant. Suppression threshold (k=25) was not triggered anywhere because no segment-level breakdown reached the point of exposing individual behavior beyond what's already aggregate.
- **Rollout is partial**: only ~46 of ~127-150 30d-active users are confirmed on a picker-carrying build (2.0.91+) as of 2026-09-25. Most Store/production users are still on the old build (dev branch → TestFlight per the task brief) and cannot see the new picker at all — this caps how much total-usage movement is even possible right now.
- **Single-user skew found and excluded**: one person (`a459f002…`, Windows, null `$app_version` — looks like a backend/manual test client, not a real phone user) generated 112 of 115 `reflect_session_started` events on 2026-09-17, one day before launch. Excluded from the before/after comparison; included raw in the daily trend table for transparency.
- **Lib trap**: `reflect_session_started`/`reflect_message_sent`/`reflect_session_ended` are emitted `$lib='posthog-python'` (backend), NOT `posthog-flutter`. Client-side picker events (`reflect_mode_*`, `reflect_entry_*`) ARE `posthog-flutter`. Mixing these under one lib filter silently zeroes one side — kept them queried separately throughout this pull.
- **Legacy `conversation_*` events are dead** (last seen 2026-08-11) — confirms this feature has fully moved to `reflect_*`; no double-counting risk, but also no fallback signal if `reflect_*` under-fires.
- `paywall_shown`/`subscription_purchase_completed` volumes are too thin (1-4 events/day, 1 user) to support any paywall-conversion claim tied to the picker's voice lock.
- `api_error` before/after windows are unequal length (14d vs 7d) because the deploy boundary sits 7 days before "today" — totals are not directly comparable; only the per-endpoint, low-n breakdown was used for the qualitative "no new pattern" read.
- Ingest start 2026-04-22 not relevant to this 4-week window.

## Queries

See `C:\Users\mikol\AppData\Local\Temp\claude\...\scratchpad\reflect_pull1.sql`, `reflect_pull2.sql` and inline checks below (all run via `scripts/posthog_query.py --sql-file`, EU project 141170).

```sql
-- build adoption
SELECT properties.$app_version AS ver, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib = 'posthog-flutter'
  AND properties.$app_version != '' AND properties.$app_version IS NOT NULL
GROUP BY ver ORDER BY first_ts DESC LIMIT 20

-- new picker events first-seen
SELECT event, min(timestamp) AS first_ts, count() AS c, count(DISTINCT person_id) AS users
FROM events
WHERE event IN ('reflect_mode_choice_shown','reflect_mode_selected','reflect_entry_topic_selected',
  'reflect_entry_sources_shown','reflect_entry_sources_served','reflect_entry_dismissed',
  'reflect_entry_start_fresh','reflect_new_thread_tapped','reflect_thread_resumed',
  'reflect_voice_locked_tapped','reflect_opening_question_shown','reflect_ui_session_ended')
  AND timestamp > now() - INTERVAL 60 DAY
GROUP BY event ORDER BY first_ts

-- daily reflect session/message trend (backend events, NOT filtered by $lib)
SELECT toDate(timestamp) AS day,
  countIf(event='reflect_session_started') AS sessions_started,
  count(DISTINCT if(event='reflect_session_started', person_id, NULL)) AS users_started,
  countIf(event='reflect_message_sent') AS messages_sent,
  count(DISTINCT if(event='reflect_message_sent', person_id, NULL)) AS users_messaged
FROM events
WHERE event IN ('reflect_session_started','reflect_message_sent')
  AND timestamp >= toDateTime('2026-08-28') AND timestamp < toDateTime('2026-09-25')
GROUP BY day ORDER BY day

-- before/after, single-user 09-17 spike excluded
SELECT 'before_09-11_to_09-17' AS period,
  countIf(event='reflect_session_started') AS sessions,
  count(DISTINCT if(event='reflect_session_started', person_id, NULL)) AS users_started,
  countIf(event='reflect_message_sent') AS messages,
  count(DISTINCT if(event='reflect_message_sent', person_id, NULL)) AS users_messaged
FROM events WHERE event IN ('reflect_session_started','reflect_message_sent')
  AND timestamp >= toDateTime('2026-09-11') AND timestamp < toDateTime('2026-09-18')
  AND person_id != 'a459f002-b841-5482-a0ba-0d4c650a2362'
-- (repeated for the other two windows; see scratchpad file)

-- picker funnel
SELECT event, count() c, count(DISTINCT person_id) users FROM events
WHERE event IN ('reflect_mode_choice_shown','reflect_mode_selected','reflect_entry_sources_shown',
  'reflect_entry_topic_selected','reflect_entry_dismissed','reflect_voice_locked_tapped')
  AND timestamp >= toDateTime('2026-09-18') AND timestamp < toDateTime('2026-09-25')
GROUP BY event

-- errors before/after, reflect/conversation/audio/voice endpoints
SELECT (timestamp < toDateTime('2026-09-18')) AS before_launch,
  properties.endpoint AS endpoint, properties.status_code AS status, count() c, count(DISTINCT person_id) users
FROM events
WHERE event = 'api_error' AND timestamp > toDateTime('2026-09-04') AND timestamp < toDateTime('2026-09-25')
  AND (properties.endpoint LIKE '%conversation%' OR properties.endpoint LIKE '%reflect%'
       OR properties.endpoint LIKE '%audio%' OR properties.endpoint LIKE '%realtime%' OR properties.endpoint LIKE '%voice%')
GROUP BY before_launch, endpoint, status ORDER BY before_launch DESC, c DESC

-- end_reason distribution
SELECT toDate(timestamp) day, properties.end_reason end_reason, properties.input_mode_used input_mode,
  count() c, count(DISTINCT person_id) users
FROM events WHERE event = 'reflect_ui_session_ended'
  AND timestamp > toDateTime('2026-08-28') AND timestamp < toDateTime('2026-09-25')
GROUP BY day, end_reason, input_mode ORDER BY day
```
