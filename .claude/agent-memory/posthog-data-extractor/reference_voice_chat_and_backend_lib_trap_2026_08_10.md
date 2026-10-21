---
name: voice-chat-and-backend-lib-trap
description: reflect_* events are backend-emitted (posthog-python), not client (posthog-flutter) - a blanket app-filter zeroes them silently. Plus voice-chat B7 baselines, $session_id field name, subscription_screen_opened missing trigger property.
metadata:
  type: reference
---

# The reflect_* lib trap (found 2026-08-10, task B7)

[[default-exclusion-filters]] documents the canonical app filter as
`properties.$lib = 'posthog-flutter'`. **That filter is wrong for the whole
`reflect_*` event family** - `reflect_message_sent`, `reflect_session_started`,
`reflect_thread_opened`, `reflect_thread_deleted`, `reflect_prompt_selected`,
`reflect_session_ended`, `reflect_limit_hit` are all emitted **server-side**
(`$lib = 'posthog-python'`), even though Reflect is a client-facing chat
feature. Applying the blanket app filter to them returns **zero rows silently**
- not an error, just a wrong "not flowing" result. Verified lifetime split:

| event | lib | events | users |
|---|---|---|---|
| reflect_message_sent | posthog-python | 1310 | 62 |
| reflect_session_started | posthog-python | 192 | 78 |

Before filtering ANY event by `$lib`, check its actual lib first with a quick
`SELECT event, properties.$lib, count(), count(DISTINCT person_id) FROM events
WHERE event IN (...) GROUP BY event, lib` - do not assume "this is a
user-facing feature" implies client-side instrumentation. For reflect_*
specifically, use `properties.$lib != 'web'` (excludes only the marketing
site) instead of `= 'posthog-flutter'`.

# `$session_id` is a top-level field, not a property

`properties.$session_id` fails HogQL resolution (`Unable to resolve field`).
The correct accessor is the bare top-level field **`$session_id`** (same
family as `$session_id_uuid`, `session`). Confirmed working with window
functions for session-ordered analysis:

```sql
lagInFrame(properties.$screen_name) OVER (PARTITION BY $session_id ORDER BY timestamp) AS prev_screen
leadInFrame(properties.$screen_name) OVER (PARTITION BY $session_id ORDER BY timestamp) AS next_screen
```

Both `lagInFrame`/`leadInFrame` work in HogQL exactly like ClickHouse. Useful
for "what screen came before/after X in the same session" without needing
session-replay data.

# subscription_screen_opened has no trigger/source property

Full `JSONExtractKeys` enumeration on `subscription_screen_opened` (220
events, full history) found only the standard client/device/geoip envelope +
`user_id` - **no key containing "trigger", "source", "feature", or "origin"
exists at all**. If a future ask wants to break the paywall down by what
triggered it (e.g. `premium_gate_reflect_voice` vs `settings` vs
`onboarding`), that property does not exist in PostHog today; it would need
`flutter-mobile` to add it to the capture call. Don't assume a property named
in a feature-gate code path (e.g. a `trigger_feature` route argument) is
actually forwarded into the analytics event - verify with `JSONExtractKeys`
before promising a breakdown.

# Voice chat (B7) baselines, 2026-08-10, lifetime (project start 2026-04-22)

- `voice_chat_started`: 65 events / **11 lifetime users** (client, posthog-flutter). Last fired 2026-08-04 - nothing in the 6 days to 2026-08-10.
- `voice_chat_ended`: 51/10. `voice_agent_changed`: 25/13. `voice_transcription_started`/`_completed`: 8/3 each, both only appeared starting the 2026-08-02 week (added ~2026-08-05 per `created_at` - not evidence the underlying flow is new, just the event).
- **`voice_transcription_failed` has never fired, any lib, full history** - confirmed via unfiltered `GROUP BY event` scan, not a lib-filter artifact.
- The only `$screen_name` matching audio/voice/chat is **`audioChat`** (74 views / 11 users lifetime). It ranks **18th of 22** screens by distinct users in the last 60d - below every other named feature flow except a couple of rarely-hit detail screens.
- Entry: 64/74 `audioChat` views are preceded by `mainPage` in the same `$session_id` (Reflect tab apparently doesn't emit its own distinct `$screen_name` - it's bucketed under `mainPage`). Exit: **74/74** have zero subsequent `$screen` event in that session - PostHog cannot show what happens after a voice session ends from `$screen` data alone (not proof of bounce, just an observability gap).
- `voice_chat_ended` carries `duration_seconds` (100% coverage) + `conversation_id`; no other custom keys on either start/end event. Duration buckets, all-time n=51: <30s=20, 30s-2m=14, 2-5m=5, >5m=12 (39% under 30s).
- App-version reachability: `voice_chat_started` has fired on 16 distinct versions since 2.0.34; most recent was 2.0.75 (2026-08-04). **Never once fired on 2.0.76** (31 active users in the last 30d as of 2026-08-10) - can't tell from PostHog alone whether that's decline or a regression in the entry point on newer builds; needs a code check.
- `subscription_purchase_completed`/`subscription_receipt_received`: only **2 distinct persons, all-time, project-wide** ever completed a purchase per PostHog (dual-emitted client+backend, last fired 2026-07-22 - stale 19d as of 2026-08-10). Do not treat as revenue truth - cross-check `subscription_receipts` in Postgres via `database-administrator`; this PostHog number is very likely an undercount. (Corrects an earlier memory note that called `subscription_purchase_completed` "absent as of 2026-08-10" - it wasn't absent, just hadn't fired in the recent window checked at the time; lifetime it has 8 events / 2 users, last 2026-07-22.)
- `reflect_limit_hit` lifetime: 3,141 events from only **4 distinct persons**, top1 = 1,870 (59.5% of all-time volume from one account). Monthly: Apr 80/1u, Jun 1191/2u, Aug 1870/1u. Thin, heavily-skewed signal - not a broad "hitting the free-tier cap" story.
- Full extract + all queries: `analytics-reports/raw/2026-08-10-voice-chat-b7.md`.

See also [[default-exclusion-filters]], [[posthog-flowing-events-baselines]].
