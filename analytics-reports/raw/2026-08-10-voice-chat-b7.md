# Voice chat (B7) – raw PostHog extract

- **Date**: 2026-08-10 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: full history (ingest start 2026-04-22) → 2026-08-10, plus 60d/30d/14d slices as noted per table
- **Question**: Is realtime voice chat worth further investment? (growth-analyst task B7; expanded mid-task with premium-gating context from Flutter code recon)
- **Requested by**: growth-analyst (original ask + mid-task addendum re: `reflect_tab_screen.dart:616-640` premium gate)

## Critical correction to the brief

The task instructed filtering **every** app-metric query by `properties.$lib = 'posthog-flutter'`. That is correct for `voice_*` events and `$screen` — they are client-only. **It is wrong for `reflect_message_sent` and `reflect_session_started`: both are emitted server-side (`$lib = 'posthog-python'`), never `posthog-flutter`.** Applying the instructed filter to them returns **zero rows** — a false "not flowing" signal, not a real zero. Verified via a lib breakdown:

| event | lib | events | users (lifetime) |
|---|---|---|---|
| reflect_message_sent | posthog-python | 1310 | 62 |
| reflect_session_started | posthog-python | 192 | 78 |
| voice_chat_started | posthog-flutter | 65 | 11 |
| voice_chat_ended | posthog-flutter | 51 | 10 |
| voice_agent_changed | posthog-flutter | 25 | 13 |
| voice_transcription_started | posthog-flutter | 8 | 3 |
| voice_transcription_completed | posthog-flutter | 8 | 3 |
| **voice_transcription_failed** | — | **0 — never fired, any lib, full history** | — |

All reflect_* numbers below use `$lib != 'web'` (excludes only the Webflow marketing site) instead of `= 'posthog-flutter'`. All voice_* and `$screen` numbers use `$lib = 'posthog-flutter'` as instructed.

## Event verification

All 7 events above are flowing (see table). `voice_transcription_failed` has never fired in project history (2026-04-22 → 2026-08-10) — checked with no lib filter, so this isn't a lib-filter artifact. `paywall_shown` also never fired (checked full history); only `paywall_dismissed` exists, first seen 2026-08-07, 5 events / 4 users. `subscription_screen_opened` carries **no `trigger_feature` (or any trigger/source/feature/origin-named) property** anywhere in its 220-event history — see Q10 note.

## Q1 — Full-history weekly volume (Sunday-start weeks, UTC)

Users (distinct person_id) per week. Full events+users detail (71 rows) is in the query output this file's Queries section reproduces; run `q1_weekly` to regenerate.

| week (Sun) | voice_chat_started | voice_chat_ended | voice_agent_changed | voice_transcr_started | voice_transcr_completed | reflect_message_sent | reflect_session_started |
|---|---|---|---|---|---|---|---|
| 2026-04-19 | 2 | 1 | – | – | – | – | 1 |
| 2026-04-26 | 1 | 1 | 2 | – | – | 6 | 9 |
| 2026-05-03 | 1 | 1 | – | – | – | 8 | 8 |
| 2026-05-10 | 3 | 2 | 2 | – | – | 6 | 8 |
| 2026-05-17 | 5 | 4 | 2 | – | – | 11 | 14 |
| 2026-05-24 | 2 | 2 | – | – | – | 3 | 5 |
| 2026-05-31 | 1 | 1 | 2 | – | – | 6 | 9 |
| 2026-06-07 | 1 | 1 | – | – | – | 6 | 7 |
| 2026-06-14 | – | – | – | – | – | 5 | 4 |
| 2026-06-21 | 2 | 2 | 1 | – | – | 8 | 12 |
| 2026-06-28 | 2 | 2 | 1 | – | – | 3 | 7 |
| 2026-07-05 | 2 | 2 | – | – | – | 9 | 8 |
| 2026-07-12 | 1 | 1 | 1 | – | – | 3 | 2 |
| 2026-07-19 | 2 | 2 | – | – | – | 2 | 5 |
| 2026-07-26 | – | – | – | – | – | 6 | 6 |
| 2026-08-02 | 1 | 1 | 2 | 3 | 3 | 11 | 11 |
| 2026-08-09 (partial) | – | – | – | – | – | 2 | 3 |

Columns are **distinct users**, not event counts. Note `voice_transcription_started/completed` only ever appear in the 2026-08-02 week (3 users) — they were added to instrumentation ~2026-08-05 per event `created_at`, not because the flow didn't exist before.

### Lifetime summary (all-time, corrected lib filter)

| event | first_seen | last_seen | total events | total persons |
|---|---|---|---|---|
| voice_chat_started | 2026-04-22 | 2026-08-04 | 65 | 11 |
| voice_chat_ended | 2026-04-24 | 2026-08-04 | 51 | 10 |
| voice_agent_changed | 2026-04-27 | 2026-08-04 | 25 | 13 |
| voice_transcription_started | 2026-08-05 | 2026-08-07 | 8 | 3 |
| voice_transcription_completed | 2026-08-05 | 2026-08-07 | 8 | 3 |
| reflect_message_sent | 2026-04-26 | 2026-08-09 | 1310 | 62 |
| reflect_session_started | 2026-04-25 | 2026-08-10 | 192 | 78 |

**voice_chat_started last fired 2026-08-04 — no voice chat session anywhere in the following 6 days to 2026-08-10.** Not proven dead (small numbers = high variance), but flag it.

## Q2 — Lifetime unique users, frequency distribution

| event | lifetime users | total events | did it 1x | 2x | 3-5x | 6+x |
|---|---|---|---|---|---|---|
| voice_chat_started | 11 | 65 | 2 | 1 | 2 | 6 |
| voice_transcription_started | 3 | 8 | 0 | 1 | 2 | 0 |

11 lifetime users is the entire population that has ever opened voice chat, in 4 months. n<25 — every voice-chat number in this file is a small-n read, not a statistically reliable one.

## Q3 — Discoverability: the voice-chat screen

Only **one** `$screen_name` value matches audio/voice/chat: **`audioChat`**. (No separate "reflect" screen matched — the Reflect tab itself does not appear to emit a distinct `$screen_name` containing those substrings.)

| $screen_name | events | distinct persons | first_seen | last_seen |
|---|---|---|---|---|
| audioChat | 74 | 11 | 2026-04-22 | 2026-08-04 |

Weekly distinct persons viewing `audioChat` (all-time): 04-19:2, 04-26:1, 05-03:1, 05-10:3, 05-17:5, 05-24:2, 05-31:1, 06-07:1, 06-21:2, 06-28:2, 07-05:2, 07-12:1, 07-19:2, 08-02:1. (Zero weeks omitted; 06-14, 07-26, 08-09 had none.)

## Q4 — Entry / exit path around the voice-chat screen (all-time, session-ordered)

**Entering `audioChat`** (previous `$screen_name` in same `$session_id`):

| prev_screen | sessions |
|---|---|
| mainPage | 64 |
| audioChat (re-entry) | 6 |
| mainPageTab | 2 |
| splash | 1 |
| (none — first screen in session) | 1 |

**Leaving `audioChat`** (next `$screen_name` in same session):

| next_screen | sessions |
|---|---|
| (none — no further `$screen` event in that session) | 74 |

**Every single one of the 74 `audioChat` views has zero subsequent `$screen` event in that session.** Either the app is backgrounded/closed right after, or whatever the user does next isn't instrumented as a `$screen` event. This is a real gap for understanding what happens after a voice session ends, not necessarily evidence people "bounce" — but it does mean we cannot see the return path from PostHog alone.

## Q5 — Top 25 screens by distinct users, last 60d (app only)

| rank | screen | users | events |
|---|---|---|---|
| 1 | splash | 386 | 1593 |
| 2 | auth | 287 | 900 |
| 3 | signUp | 129 | 156 |
| 4 | mainPage | 123 | 4186 |
| 5 | therapyOnboarding | 103 | 280 |
| 6 | healthCheckFlow | 42 | 217 |
| 7 | afterTherapyFlow | 39 | 223 |
| 8 | settings | 36 | 414 |
| 9 | account | 30 | 142 |
| 10 | prepTherapyFlow | 28 | 149 |
| 11 | betweenSessionsFlow | 26 | 238 |
| 12 | forgotPassword | 23 | 25 |
| 13 | recordSessionFlow | 20 | 347 |
| 14 | subscription | 19 (n<25, suppress) | 98 |
| 15 | therapists | 17 (n<25, suppress) | 33 |
| 16 | mainPageTab | 11 (n<25, suppress) | 177 |
| 17 | about | 9 (n<25, suppress) | 28 |
| **18** | **audioChat** | **4 (n<25, suppress)** | **22** |
| 19 | momentDetail | 4 (n<25, suppress) | 31 |
| 20 | consentCodeEntry | 3 (n<25, suppress) | 3 |
| 21 | recordingDetail | 2 (n<25, suppress) | 2 |
| 22 | changePassword | 2 (n<25, suppress) | 4 |

`audioChat` ranks **18th of 22** screens by 60d reach — below every other named feature flow except a couple of rarely-hit detail/utility screens.

## Q6 — voice_chat_started / voice_chat_ended property keys + duration

Both events carry the standard PostHog client/device/geoip envelope (`$app_version`, `$os`, `$device_*`, `$geoip_*`, etc. — same ~30 keys on ~100% of events) plus one custom key: **`conversation_id`** (100% of events, both start and end). `voice_chat_ended` additionally carries **`duration_seconds`** (100% of its 51 events). No other custom keys found on either event (top-40 key list showed no `agent`, `error`, `reason`, or similar).

Bucketed `duration_seconds` on `voice_chat_ended` (all-time, n=51 events / lifetime max 10 users):

| bucket | events | users |
|---|---|---|
| <30s | 20 | 6 |
| 30s–2m | 14 | 7 |
| 2–5m | 5 | 5 |
| >5m | 12 | 4 |

39% of all voice-chat sessions end in under 30 seconds.

## Q7 — App version reachability

**Ever emitted `voice_chat_started`** (all-time, 16 distinct versions, oldest→newest by last_seen):

| version | events | users | first_seen | last_seen |
|---|---|---|---|---|
| 2.0.34 | 1 | 1 | 2026-04-22 | 2026-04-22 |
| 2.0.36 | 5 | 2 | 2026-04-24 | 2026-04-30 |
| 2.0.38 | 1 | 1 | 2026-05-12 | 2026-05-12 |
| 2.0.39 | 2 | 1 | 2026-05-15 | 2026-05-15 |
| 2.0.40 | 1 | 1 | 2026-05-18 | 2026-05-18 |
| 2.0.37 | 8 | 4 | 2026-05-09 | 2026-05-19 |
| 2.0.45 | 3 | 2 | 2026-05-25 | 2026-05-25 |
| 2.0.47 | 1 | 1 | 2026-05-29 | 2026-05-29 |
| 2.0.44 | 22 | 4 | 2026-05-20 | 2026-06-10 |
| 2.0.51 | 1 | 1 | 2026-06-21 | 2026-06-21 |
| 2.0.52 | 3 | 1 | 2026-06-22 | 2026-06-22 |
| 2.0.64 | 1 | 1 | 2026-07-04 | 2026-07-04 |
| 2.0.68 | 5 | 1 | 2026-07-07 | 2026-07-09 |
| 2.0.60 | 9 | 2 | 2026-07-04 | 2026-07-22 |
| 2.0.72 | 1 | 1 | 2026-07-23 | 2026-07-23 |
| **2.0.75** | 1 | 1 | 2026-08-04 | 2026-08-04 |

**Active app versions, last 30d** (`$screen`/any client event, all users):

| version | users |
|---|---|
| 2.0.60 | 84 |
| 2.0.75 | 60 |
| **2.0.76** | **31** |
| 2.0.44 | 6 |
| 2.0.71 | 4 |
| 2.0.74 | 4 |
| 2.0.73 | 3 |
| 2.0.69 | 3 |
| 2.0.70 | 3 |
| 2.0.68 | 2 |
| 2.0.72 | 2 |
| 2.0.36 | 1 |
| 2.0.37 | 1 |

**The entry point has never once fired `voice_chat_started` on build 2.0.76 — the newest build, with 31 active users in the last 30d — nor is there any `voice_chat_started` at all in the last 6 days across any build.** The most recent voice_chat_started (2026-08-04) was on 2.0.75. This is consistent with either (a) real decline in usage, or (b) the entry point regressing/breaking in recent builds — PostHog alone cannot distinguish these; a code check of the mic-tap path in the builds ≥2.0.76 is the way to tell.

## Q8 — Retention: voice-chat users vs. reflect-only users

Cohort = persons whose first-ever app event (`$lib='posthog-flutter'`) was on/after 2026-05-01.

| cohort | n | avg active days (28d post-first-event) | median active days | % returned days 2-7 | % returned days 8-28 |
|---|---|---|---|---|---|
| A: ever `voice_chat_started` | **6 (n<25 — suppress in any published report)** | 6.67 | 3.5 | 100.0% | 66.7% |
| B: `reflect_message_sent`, never `voice_chat_started` | 47 | 2.81 | 2.0 | 100.0% | 31.9% |

**Cohort A is n=6 — do not treat as statistically meaningful.** Directionally it looks more engaged than cohort B, but with 6 people this could be one or two power users skewing the average; it is not evidence that voice chat *causes* retention. Selection bias also cuts the other way here: people who try a premium-gated feature at all have likely already demonstrated intent/means to be more engaged, so A vs. B isn't a clean causal comparison even ignoring sample size.

## Q9 — Denominator context

| window | scope | events | persons |
|---|---|---|---|
| last 14d | app-client only (`$lib='posthog-flutter'`) | 6,307 | 94 |
| prior 14d | app-client only | 6,231 | 81 |
| last 14d | app-inclusive (`$lib != 'web'`, adds backend-only reflect/subscription/api events) | 13,883 | 102 |
| prior 14d | app-inclusive | 7,965 | 83 |

11 lifetime voice-chat users against ~90-100 active app users in any given 14d window, and against several hundred total signups over the project's 4-month life.

## Q10 — subscription_screen_opened trigger breakdown (growth-analyst addendum)

**`subscription_screen_opened` does not carry a `trigger_feature` property, or any property with "trigger", "source", "feature", or "origin" in its name, anywhere in its 220-event history.** Full property-key enumeration returned only the standard client/device/geoip envelope plus `user_id`. The `premium_gate_reflect_voice` vs. other-trigger breakdown you asked for **is not measurable from PostHog today** — this is an instrumentation gap, not a small-n issue. If the trigger is known client-side (per your code recon of `reflect_tab_screen.dart`), it is not being passed into the PostHog event properties; that's a `flutter-mobile` fix (add `trigger_feature` to the `subscription_screen_opened` capture call), not something recoverable from existing data.

`paywall_shown` confirmed **never fired**, any lib, full history. `paywall_dismissed`: first_seen 2026-08-07, last_seen 2026-08-10, 5 events / 4 users — essentially no history (9 days), consistent with prior project memory that it's a brand-new event.

## Q11 — Premium denominator

| metric | value |
|---|---|
| distinct persons ever `subscription_purchase_completed` (all-time) | **2 (n<25 — suppress)** |
| distinct persons `subscription_purchase_completed`, last 90d | 2 |
| distinct persons ever `subscription_receipt_received` (all-time) | 2 |

**PostHog shows only 2 distinct persons ever completing a purchase, project-wide, in 4 months.** This number is almost certainly incomplete as a revenue source — `subscription_purchase_completed` is dual-emitted (client `posthog-flutter` AND backend `posthog-python`, not always both for the same purchase) and PostHog is not the system of record for purchases. **Hand off to `database-administrator`** for the true count from `subscription_receipts` in Postgres before anyone treats "2" as the real premium base.

## Q12 — Voice-chat users × premium × internal-tester overlap

Of the 11 lifetime `voice_chat_started` users:

| flag | count |
|---|---|
| total voice-chat users | 11 |
| also ever `subscription_purchase_completed` | 2 |
| ever carried `$is_testflight = true` | 4 |
| ever carried `$is_emulator = true` | 0 |

**4 of the 11 lifetime voice-chat users (36%) are TestFlight testers**, and only 2 of 11 ever converted to paid — consistent with a mostly-internal, mostly-unmonetized usage pattern, though 11 is too small to generalize with confidence (both numbers reported as raw counts per your request, not as percentages we'd publish un-suppressed).

## Q13 — reflect_limit_hit (free-tier message cap vs. voice gate)

| month | events | distinct persons |
|---|---|---|
| 2026-04 | 80 | 1 |
| 2026-06 | 1191 | 2 |
| 2026-08 | 1870 | 1 |

Skew check (all-time): 3,141 total events across **4 distinct persons**, with the single largest person accounting for 1,870 of them (59.5% of all `reflect_limit_hit` events, all-time, from one account). **`reflect_limit_hit` is not a broad "people are hitting the free-message-cap" signal — it is 4 people, one of whom loops it heavily** (matches project memory: a single account hammering the 403 daily-limit endpoint). It does not support a claim that the free-tier message limit is a major, wide-reaching friction point versus the voice gate; both are thin signals from very few accounts.

## Caveats (apply throughout)

- Ingest started 2026-04-22 — full-history queries are bounded there, not artificially truncated further.
- `$lib` handling: `voice_*` + `$screen` = `posthog-flutter` only (correct, client-only instrumentation); `reflect_*` = server-side (`posthog-python`), filtered as `$lib != 'web'` instead, per the correction noted at the top. Applying the brief's blanket `$lib='posthog-flutter'` filter to `reflect_*` silently zeroes them — flagged explicitly so it isn't repeated.
- Every voice-chat-specific number in this file is small-n (11 lifetime users, cohort A n=6, purchase overlap n=2). None of these should be presented un-suppressed in a report to non-agent audiences; n<25 segments are marked "suppress" inline per project k-anonymity rule, but raw n is given here since this is an agent-to-agent extract, not a published report.
- `subscription_purchase_completed`/`subscription_receipt_received` are not reliable revenue truth in PostHog (n=2 all-time is almost certainly an undercount of real subscribers) — cross-check `subscription_receipts` in Postgres via `database-administrator` before using "2" as a premium base.
- `subscription_screen_opened` has no trigger/source property at all — the requested trigger_feature breakdown could not be produced; this is a gap for `flutter-mobile` to close, not a data-pull failure.
- Q4's "no next screen" result (74/74) means PostHog cannot show what users do immediately after a voice session from `$screen` events alone; it is not proof of "bounce," just an observability gap in the current `$screen` instrumentation around that flow.

## Queries

```sql
-- @@ q1_weekly
SELECT event, toStartOfWeek(timestamp) AS week, count() AS events, count(DISTINCT person_id) AS users
FROM events
WHERE event IN ('voice_chat_started','voice_chat_ended','voice_agent_changed','voice_transcription_started','voice_transcription_completed','voice_transcription_failed','reflect_message_sent','reflect_session_started')
  AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
  AND (
    (event IN ('voice_chat_started','voice_chat_ended','voice_agent_changed','voice_transcription_started','voice_transcription_completed','voice_transcription_failed') AND properties.$lib = 'posthog-flutter')
    OR
    (event IN ('reflect_message_sent','reflect_session_started') AND properties.$lib != 'web')
  )
GROUP BY event, week ORDER BY event, week

-- @@ q1_summary  (same WHERE, no week bucket, min/max timestamp + count() + count(DISTINCT person_id) GROUP BY event)

-- @@ q1_events_never_flowed_check
SELECT event, count() AS c FROM events
WHERE event IN (...) AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
GROUP BY event ORDER BY event
-- (no lib filter at all — confirms voice_transcription_failed is absent regardless of lib)

-- @@ q2_voice_chat_started_dist / q2_voice_transcription_started_dist
SELECT count() AS users, sum(cnt) AS total_events,
  countIf(cnt=1) AS x1, countIf(cnt=2) AS x2, countIf(cnt BETWEEN 3 AND 5) AS x3_5, countIf(cnt>=6) AS x6plus
FROM (SELECT person_id, count() AS cnt FROM events WHERE event='<event>' AND properties.$lib='posthog-flutter'
      AND timestamp > toDateTime('2026-04-22') AND timestamp <= now() GROUP BY person_id)

-- @@ q3_screen_names / q3_weekly_voice_screen
SELECT properties.$screen_name AS screen, count() c, count(DISTINCT person_id) u, min(timestamp), max(timestamp)
FROM events WHERE event='$screen' AND properties.$lib='posthog-flutter'
  AND (lower(toString(properties.$screen_name)) LIKE '%audio%' OR ... LIKE '%voice%' OR ... LIKE '%chat%')
  AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
GROUP BY screen ORDER BY u DESC

-- @@ q4_entry / q4_exit  (window functions — note $session_id is a top-level field, NOT properties.$session_id)
SELECT prev_screen, count() AS sessions_entering FROM (
  SELECT $session_id AS sid, timestamp, properties.$screen_name AS screen,
    lagInFrame(properties.$screen_name) OVER (PARTITION BY $session_id ORDER BY timestamp) AS prev_screen
  FROM events WHERE event='$screen' AND properties.$lib='posthog-flutter'
    AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
)
WHERE lower(toString(screen)) LIKE '%audio%' OR ... LIKE '%voice%' OR ... LIKE '%chat%'
GROUP BY prev_screen ORDER BY sessions_entering DESC
-- (leadInFrame for q4_exit, symmetric)

-- @@ q5_top_screens_60d
SELECT properties.$screen_name AS screen, count(DISTINCT person_id) AS users, count() AS c
FROM events WHERE event='$screen' AND properties.$lib='posthog-flutter' AND timestamp > now() - INTERVAL 60 DAY
GROUP BY screen ORDER BY users DESC LIMIT 25

-- @@ q6_keys_voice_chat_started / q6_keys_voice_chat_ended
SELECT arrayJoin(JSONExtractKeys(toString(properties))) AS key, count() c
FROM events WHERE event='<event>' AND properties.$lib='posthog-flutter'
  AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
GROUP BY key ORDER BY c DESC LIMIT 40

-- @@ q6_duration_bucket
SELECT multiIf(toFloat64OrNull(toString(properties.duration_seconds)) < 30, '<30s',
               toFloat64OrNull(toString(properties.duration_seconds)) < 120, '30s-2m',
               toFloat64OrNull(toString(properties.duration_seconds)) < 300, '2-5m', '>5m') AS bucket,
  count() c, count(DISTINCT person_id) u
FROM events WHERE event='voice_chat_ended' AND properties.$lib='posthog-flutter'
  AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
GROUP BY bucket ORDER BY bucket

-- @@ q7_versions_ever_voice / q7_versions_active_30d
SELECT properties.$app_version AS ver, count() c, count(DISTINCT person_id) users, min(timestamp), max(timestamp)
FROM events WHERE event='voice_chat_started' AND properties.$lib='posthog-flutter'
  AND properties.$app_version != '' AND properties.$app_version IS NOT NULL
  AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
GROUP BY ver ORDER BY last_seen DESC
-- (active_30d: same shape, any client event, timestamp > now() - INTERVAL 30 DAY)

-- @@ q8_cohort_retention
WITH first_seen AS (
  SELECT person_id, min(timestamp) AS first_ts FROM events
  WHERE properties.$lib='posthog-flutter' AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
  GROUP BY person_id HAVING first_ts >= toDateTime('2026-05-01')
),
flags AS (
  SELECT person_id,
    countIf(event='voice_chat_started' AND properties.$lib='posthog-flutter') > 0 AS has_voice,
    countIf(event='reflect_message_sent') > 0 AS has_reflect
  FROM events WHERE timestamp > toDateTime('2026-04-22') AND timestamp <= now()
    AND event IN ('voice_chat_started','reflect_message_sent')
  GROUP BY person_id
),
cohort AS (
  SELECT fs.person_id, fs.first_ts, multiIf(fl.has_voice,'A_voice', fl.has_reflect,'B_reflect_no_voice','other') AS cohort_name
  FROM first_seen fs JOIN flags fl ON fs.person_id = fl.person_id WHERE fl.has_voice OR fl.has_reflect
),
per_person AS (
  SELECT c.cohort_name, c.person_id,
    count(DISTINCT toDate(e.timestamp)) AS active_days_28d,
    countIf(e.timestamp > c.first_ts AND e.timestamp <= c.first_ts + INTERVAL 7 DAY) > 0 AS returned_2_7,
    countIf(e.timestamp > c.first_ts + INTERVAL 7 DAY AND e.timestamp <= c.first_ts + INTERVAL 28 DAY) > 0 AS returned_8_28
  FROM cohort c JOIN events e ON c.person_id = e.person_id
  WHERE e.timestamp >= c.first_ts AND e.timestamp <= c.first_ts + INTERVAL 28 DAY
  GROUP BY c.cohort_name, c.person_id
)
SELECT cohort_name, count() n, avg(active_days_28d), median(active_days_28d),
  avg(returned_2_7)*100, avg(returned_8_28)*100
FROM per_person GROUP BY cohort_name ORDER BY cohort_name

-- @@ q9_sanity_app_lib_only / q9_sanity_app_inclusive
SELECT countIf(timestamp > now() - INTERVAL 14 DAY) events_last14d,
  count(DISTINCT if(timestamp > now() - INTERVAL 14 DAY, person_id, NULL)) persons_last14d,
  countIf(timestamp <= now() - INTERVAL 14 DAY AND timestamp > now() - INTERVAL 28 DAY) events_prior14d,
  count(DISTINCT if(timestamp <= now() - INTERVAL 14 DAY AND timestamp > now() - INTERVAL 28 DAY, person_id, NULL)) persons_prior14d
FROM events WHERE properties.$lib = 'posthog-flutter' AND timestamp > now() - INTERVAL 28 DAY
-- (app_inclusive variant: WHERE properties.$lib != 'web')

-- @@ q10_trigger_feature_alltime / q10_trigger_feature_60d
SELECT ifNull(nullIf(JSONExtractString(toString(properties), 'trigger_feature'), ''), 'unknown') AS trigger_feature,
  count() c, count(DISTINCT person_id) u
FROM events WHERE event='subscription_screen_opened' AND properties.$lib='posthog-flutter'
  AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()   -- (60d variant: timestamp > now() - INTERVAL 60 DAY)
GROUP BY trigger_feature ORDER BY c DESC
-- followed up with a full JSONExtractKeys enumeration on subscription_screen_opened to confirm no trigger/source/feature/origin key exists at all

-- @@ q10_paywall_check
SELECT event, min(timestamp), max(timestamp), count() c, count(DISTINCT person_id) u
FROM events WHERE event IN ('paywall_shown','paywall_dismissed') AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
GROUP BY event

-- @@ q11_premium_denominator
SELECT count(DISTINCT if(event='subscription_purchase_completed', person_id, NULL)) purchase_completed_alltime,
  count(DISTINCT if(event='subscription_purchase_completed' AND timestamp > now() - INTERVAL 90 DAY, person_id, NULL)) purchase_completed_90d,
  count(DISTINCT if(event='subscription_receipt_received', person_id, NULL)) receipt_received_alltime
FROM events WHERE event IN ('subscription_purchase_completed','subscription_receipt_received')
  AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()

-- @@ q12_voice_users_overlap
WITH voice_persons AS (
  SELECT DISTINCT person_id FROM events WHERE event='voice_chat_started' AND properties.$lib='posthog-flutter'
    AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
),
per_person AS (
  SELECT person_id,
    countIf(event='subscription_purchase_completed') > 0 AS has_purchase,
    countIf(properties.$is_testflight = true) > 0 AS has_testflight,
    countIf(properties.$is_emulator = true) > 0 AS has_emulator
  FROM events WHERE person_id IN (SELECT person_id FROM voice_persons)
    AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
  GROUP BY person_id
)
SELECT count() total_voice_users, countIf(has_purchase) with_purchase,
  countIf(has_testflight) with_testflight, countIf(has_emulator) with_emulator
FROM per_person

-- @@ q13_reflect_limit_hit_monthly / q13_reflect_limit_hit_skew
SELECT toStartOfMonth(timestamp) AS month, count() c, count(DISTINCT person_id) u
FROM events WHERE event='reflect_limit_hit' AND timestamp > toDateTime('2026-04-22') AND timestamp <= now()
GROUP BY month ORDER BY month
-- skew: SELECT sum(cnt), max(cnt), count() FROM (SELECT person_id, count() cnt FROM events WHERE event='reflect_limit_hit' ... GROUP BY person_id)
```
