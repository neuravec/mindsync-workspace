# Post-onboarding Home behaviour (first 30 min, first week): raw PostHog extract

- **Date**: 2026-10-07 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window A**: `onboarding_completed` 2026-09-01 00:00 UTC -> 2026-10-07 (last one seen 2026-10-06 18:27 UTC) · **Window B**: `onboarding_completed` >= 2026-10-03 00:00 UTC
- **Question**: what do new users do right after onboarding lands them on Home, to validate a "first week" Home design.
- **Population** (person level, `person_id`): client `onboarding_completed` (`$lib = 'posthog-flutter'`) in window A = 46 persons. Excluded: TestFlight 2 (both in window B, reported only as a count), bot device model (`OnePlus8Pro`/`Pixel 6 Pro`) 1, emulator 1, tester heuristic (>= 3 lifetime `onboarding_completed` or >= 10 `$app_version`s) 1; one person matched two rules. **Kept n = 42** (Android 35, iOS 7). Every kept person has exactly one lifetime `onboarding_completed`.
- **Window B** n = 7 (Android 6, iOS 1). Only 4 of the 7 were on a build with the new post-onboarding flow (`$app_version` 2.0.100; new flow = 2.0.97+), the other 3 on 2.0.94/2.0.95. So window B is a date window with mixed flows, and the new-flow-only slice (n=4) is suppressed.
- **New-wave split** (Android + `$geoip_country_code` in CI, DZ, IR, IQ, PK, SA + onboarding_completed >= 2026-09-20): **n = 4, below the 5-person floor, so every new-wave split is suppressed.** Context from a separate, non-population query: 48 non-bot, non-emulator persons from that traffic fired any client event since 2026-09-20, 7 started onboarding, 4 completed it. The new wave mostly does not reach Home at all, which is why it cannot be split here.
- **Landing definition**: first `$screen` with `$screen_name = 'mainPage'` at or after the person's `onboarding_completed` (`onboarding_completed` itself fires on `$screen_name = therapyOnboarding`; the post-onboarding `wow` screen sits in between). 41 of 42 landed; median onboarding -> landing 12 s (pre-10-03 cohort, n=35) and 28.5 s (window B, n=6). All 41 landed within 30 min of onboarding.
- **Suppression**: any cell under 5 persons is shown as `<5`. Everything here is directional (n = 42 total).

## Event verification (Q7)

All traffic, no exclusions, last 30 days unless noted. `last_seen` = max event timestamp from a HogQL query (the event-definitions catalog lags by an hour or two).

| event | flowing? | lib | first seen | last seen (UTC) | 30d events | 30d persons | kept population, first 7d after onboarding |
|---|---|---|---|---|---|---|---|
| `first_conversation_ended` | yes, new (since 2026-10-05) | posthog-flutter | 2026-10-05 08:35 | 2026-10-06 18:38 | 11 | <5 | **0** (none of the 42) |
| `post_onboarding_offer_result` | yes, new (since 2026-10-04) | posthog-flutter | 2026-10-04 20:53 | 2026-10-06 18:38 | 13 | 6 | <5 |
| `push_prompt_result` | yes, new (since 2026-10-03) | posthog-flutter | 2026-10-03 07:52 | 2026-10-06 18:38 | 20 | 7 | <5 |
| `personal_reveal_viewed` | yes, new (since 2026-10-03) | posthog-flutter | 2026-10-03 07:51 | 2026-10-06 18:27 | 23 | 8 | <5 |
| `trial_reminder_sheet_shown` | **NO, never fired** (absent from event definitions and from a query since 2026-08-01; defined in `analytics_events.dart`) | n/a | n/a | n/a | 0 | 0 | 0 |
| `symptom_scored` | yes | **posthog-python (backend)** | 2026-04-27 | 2026-10-06 21:29 | 237 | 14 | 7 |
| `reflect_session_started` | yes | **posthog-python (backend)** | 2026-04-25 | 2026-10-06 21:17 | 193 | 23 | 13 |

`symptom_scored` and `reflect_session_started` are backend events: they do not carry `$lib = 'posthog-flutter'`, `$os` or `$is_testflight`, so they were matched to the kept population by `person_id`, not filtered by lib.

## Results

### Q1. First 30 min after landing on Home (n = 41 landed)

Top 20 non-noise client events, distinct persons, in `(landing, landing + 30 min)`. Noise excluded: `$screen`, `api_error`, `$set`, `$identify`, `$exception`, `client_error`, `usage_snapshot`, `usage_load_failed`, `$autocapture`, `$rageclick`, `app_install_attributed`, `$feature_flag_called`, `notification_received`. No app-lifecycle events exist in this project (the Flutter SDK does not send them). "Auto" = fired by the app on render, not a deliberate tap.

| # | event | persons (of 41) | events | window B persons (of 6 landed) | kind |
|---|---|---|---|---|---|
| 1 | `notification_permission_prompted` | 38 | 42 | <5 | auto (OS dialog on first Home render) |
| 2 | `timeline_viewed` | 37 | 85 | 5 | view |
| 3 | `first_capture_prompt_shown` | 36 | 180 | 6 | auto (GettingStartedCard + timeline empty state) |
| 4 | `app_tour_step_viewed` | 34 | 204 | <5 | auto (tour sheet) |
| 5 | `app_tour_started` | 34 | 35 | <5 | auto |
| 6 | `notification_permission_granted` | 33 | 37 | <5 | OS answer |
| 7 | `tab_switched` | 32 | 358 | 6 | action |
| 8 | `workspace_opened` | 27 | 76 | 5 | view |
| 9 | `character_card_viewed` | 24 | 32 | <5 | view |
| 10 | `bio_viewed` | 22 | 30 | <5 | view |
| 11 | `app_tour_completed` | 22 | 22 | <5 | action (tour) |
| 12 | `habit_tracker_viewed` | 20 | 50 | 6 | view |
| 13 | `reflect_thread_opened` | 10 | 15 | <5 | action |
| 14 | `health_check_question_answered` | 8 | 24 | <5 | action |
| 15 | `debrief_started` | 8 | 12 | <5 | action |
| 16 | `reflect_new_thread_tapped` | 8 | 11 | <5 | action |
| 17 | `reflect_mode_choice_shown` | 8 | 11 | <5 | auto |
| 18 | `health_check_started` | 8 | 8 | <5 | action |
| 19 | `reflect_message_submitted` | 7 | 64 | <5 | action |
| 20 | `reflect_mode_selected` | 7 | 11 | <5 | action |

Just below the cut (5-7 persons): `reflect_entry_sources_shown` 7, `between_session_started` 6, `reflect_ui_session_ended` 6, `app_tour_skipped` 6, `recording_saved` 6, `quick_capture_abandoned` 5, `reflect_entry_start_fresh` 5, `notification_permission_denied` 5.

Screens opened in the same 30 min (persons, of 41): `mainPage` 36, `healthCheckFlow` 9, `myTherapy` 9, `afterTherapyFlow` 8, `reflectModeChoice` 8, `betweenSessionsFlow` 7, `settings` 6, `splash` 5, everything else <5.

**"Does nothing" after landing** (n = 41; pre-10-03 n = 35, window B n = 6):

| definition (30 min after landing) | all | pre-10-03 | window B |
|---|---|---|---|
| zero events of any kind | 0 / 41 | 0 | 0 |
| zero product actions (excluding auto/view events and the app tour) | 5 / 41 (12%) | 5 | 0 |
| zero product actions AND never left Home (no other screen) | <5 / 41 | <5 | 0 |
| never switched tab and never opened another screen | 5 / 41 (12%) | 5 | 0 |
| did a core capture (debrief/prep/between-session/health check/Reflect message/recording/quick capture/symptom/habit/voice chat started) | 22 / 41 (54%) | 18 / 35 | <5 / 6 |
| landing session (same `$session_id`) ended < 60 s after landing | 13 / 41 (32%) | 11 | <5 |
| landing session ended < 180 s after landing | 22 / 41 (54%) | 19 | <5 |
| median landing-session length after landing | n/a | 145 s | 487 s |
| median time landing -> first product action | n/a | 12 s | 19.5 s |

The app tour sheet opens 1 s after Home renders: started by 34/41, completed 22, skipped 6, no outcome logged 7. Nobody is left with literally nothing on screen, because the OS notification dialog and the tour fire first.

### Q2. Push prompt and notification permission (first 7 days after onboarding, n = 42)

- `push_prompt_result` (in-flow pre-prompt, new flow only): 3 persons in the kept population, **distribution suppressed (n < 5)**. All traffic: 20 events / 7 persons in 30d, so it flows.
- OS permission, within `[onboarding - 1 h, onboarding + 7 d)`:

| | persons | OS dialog shown | granted | denied | granted, never denied |
|---|---|---|---|---|---|
| all | 42 | 40 (95%) | 36 (86%) | 5 (12%) | 35 (83%) |
| pre-10-03 | 35 | 35 | 31 | 5 | 30 |
| window B | 7 | 5 | 5 | 0 | 5 |
| Android | 35 | 33 | 30 | <5 | n/a |
| iOS | 7 | 7 | 6 | <5 | n/a |

### Q3. Return in the first week

| metric | eligible (right-censored) | value |
|---|---|---|
| any client event in `[onboarding + 24 h, onboarding + 8 d)` | 30 (onboarded before now - 8 d) | **9 / 30 (30%)** |
| active on 3+ distinct days in `[onboarding, onboarding + 7 d)`, day = 24 h period since onboarding | 32 (onboarded before now - 7 d) | **<5 / 32** (2 days: 6; 1 day: 22) |
| same, UTC calendar days (onboarding evening + next morning count as 2) | 32 | 7 / 32 (22%) |
| did a core capture within 7 days of onboarding | 32 | 19 / 32 (59%) |

"Client event" = any `posthog-flutter` event except `$set`, `$identify`, `app_install_attributed`, `notification_received`. Window B cannot be measured yet (all 7 onboarded less than 8 days ago).

### Q4. First tab and GettingStartedCard / FAB

First `tab_switched.tab_name` after landing (n = 41):

| first tab | within 30 min | within 7 days of onboarding |
|---|---|---|
| therapy | 16 | 17 |
| workspace | 7 | 7 |
| character | 6 | 7 |
| reflect | <5 | <5 |
| main | <5 | <5 |
| no tab switch | 9 | 6 |

Within 30 min, 29/41 visited the Reflect tab and 27/41 the Workspace tab at some point (they walk the tabs in order).

GettingStartedCard and FAB:
- The card renders for 34/41 within 30 min of landing (`first_capture_prompt_shown`, `entry_point = home_empty_state`; 36 persons in the first 7 days, 221 renders).
- **Card taps are not instrumented.** "Capture a session" opens `afterTherapyFlow`, "Track a symptom" calls `selectTab(3)` (logs `tab_switched` workspace), "Reflect" calls `selectTab(2)` (logs `tab_switched` reflect). None of these can be told apart from the FAB, the nav bar or a swipe.
- **The FAB is not instrumented either**: expanding it logs nothing, and `entry_point = fab` only labels `usage_chip_tapped_at_zero`, which fires only at a zero free counter (0 times in this population).
- Proxy: opened `afterTherapyFlow` within 30 min of landing 8/41; opened any FAB capture flow (`afterTherapyFlow`, `prepTherapyFlow`, `betweenSessionsFlow`, `recordSessionFlow`) 16/41. Previous screen for those flows (first 7 days) was `mainPage` in nearly every case, but `mainPage` is the tab shell, so this does not prove the tap came from the Home tab.
- The post-onboarding first-step screen (`entry_point = post_onboarding`, shown to 41 persons): `first_capture_prompt_dismissed` with `explicit_close` 12 persons (old flow); `take_me_to_app` <5 and `first_capture_prompt_option_tapped` <5 (new flow only, window B).

### Q5. Hour of `onboarding_completed`, person's local time (n = 42)

Local hour from the device `$timezone` property (present on 42/42), converted per row in Python with `zoneinfo` because HogQL `toTimeZone` needs a constant zone. The 06-09 and 09-12 buckets were both under 5 and are merged.

| local hour | persons | UTC hour (same people) |
|---|---|---|
| 00-03 | 5 | 9 |
| 03-06 | 5 | <5 |
| 06-12 (merged) | 6 | 11 |
| 12-15 | 6 | 7 |
| 15-18 | 6 | <5 |
| 18-21 | 5 | <5 |
| 21-24 | 9 | <5 |

19/42 (45%) finished onboarding between 18:00 and 03:00 local; 21-24 is the largest bucket. Window B by hour: every bucket <5, suppressed.

### Q6. Moments in the first 7 days after onboarding (n = 42)

39/42 persons got at least one `moment.sent` (103 sends, 26 persons with `has_token = true` on at least one send). Sends by day since onboarding (persons): d0 9, d1 10, d2 8, d3 14, d4 12, d5 7, d6 7.

| `moment_type` | persons sent (all 42) | sends | sends with `has_token = true` | persons sent, 7-day-eligible only (n = 32) |
|---|---|---|---|---|
| WEEKLY_SUMMARY_READY | 35 | 35 | 22 | 28 |
| REFLECTION_INVITATION | 20 | 20 | 14 | 16 |
| THERAPY_RELATIONSHIP_CHECKIN | 18 | 18 | 10 | 14 |
| MONTHLY_SUMMARY_READY | 9 | 9 | 6 | 8 |
| MOOD_UPDATE_REQUEST | 7 | 7 | 6 | <5 |
| ACCOUNT_SETUP_NUDGE | <5 | 6 | 3 | <5 |
| ADD_THERAPY_DATE, RE_ENGAGEMENT, THERAPY_APPOINTMENT, POST_SESSION_REFLECTION | <5 each | 8 | 7 | <5 each |

Opened: backend `moment.opened` 8 persons (17 opens), `moment.acted` 5 persons; client `notification_opened` 5 persons (6 opens). Opened by type: every type <5, suppressed. Also 12 of the 17 `moment.opened` events could not be matched to a `moment.sent` (`moment.opened` carries only `moment_id`, no `moment_type`).

## Caveats

- Ingest started 2026-04-22 (no effect here, windows start 2026-09-01).
- Tiny n: 42 persons, 41 landed. Treat every share as directional. Window B is mixed old/new flow; the new-flow-only slice (n=4) and the whole new-wave split (n=4) are suppressed.
- `$is_testflight` exists only on iOS; the Android tester signal is the heuristic (repeat onboarding / many versions).
- The kept population was materialized once as a person list (scratchpad only, not stored) so that each query fits PostHog's 10 s `max_execution_time` on `/query/`; the defining CTE is the `pop_summary` query below. Queries in pass 2-4 show `__POP_IDS__` where that literal list was substituted.
- "Auto" events (`notification_permission_prompted`, tour, card impression) fire on render, so "zero events after landing" is 0 by construction. Use the "zero product actions" rows.
- `notification_permission_granted` reflects the OS answer; on older Android versions the permission is granted without a dialog, so the grant rate may be inflated on Android.
- GettingStartedCard taps and the FAB have no events (see Q4). Missing instrumentation for `flutter-mobile`: a `getting_started_card_tapped` (prop `option`: capture_session | track_symptom | reflect) and a `fab_flow_selected` (prop `flow`: after_therapy | prepare_therapy | between_sessions | record_session, plus `tab_name` the FAB was opened on).
- `trial_reminder_sheet_shown` has never fired. The first new-flow users reached day 3 only on 2026-10-06, so this may be timing rather than a bug; re-check after 2026-10-10.
- `first_conversation_ended` flows but no kept person fired it (its 30d persons are outside the kept population: excluded testers, TestFlight or users without an `onboarding_completed` in window A).
- `moment.sent` with `has_token = false` probably did not produce a push. Only 26 of 39 persons had a tokened send.
- `symptom_scored` and `reflect_session_started` are backend (`posthog-python`) events.

## Queries

All HogQL below ran through `scripts/posthog_query.py --sql-file` (read-only `/query/`).

### Pass 1: population definition (exclusions applied here; also the source of the materialized person list)

```sql
-- @@ pop_summary
WITH onb AS (
  SELECT person_id,
    minIf(timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS onb_ts,
    count() AS n_onb_life,
    argMinIf(properties.$os, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS os,
    argMinIf(properties.$geoip_country_code, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS cc,
    argMinIf(properties.$timezone, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS tz,
    argMinIf(properties.$app_version, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS ver
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-04-22 00:00:00')
  GROUP BY person_id
  HAVING countIf(timestamp >= toDateTime('2026-09-01 00:00:00')) > 0
),
flags AS (
  SELECT person_id,
    countIf(properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro')) AS bot,
    countIf(properties.$is_emulator = true) AS emu,
    countIf(properties.$is_testflight = true) AS tf,
    count(DISTINCT properties.$app_version) AS n_ver
  FROM events
  WHERE properties.$lib = 'posthog-flutter' AND timestamp >= toDateTime('2026-08-25 00:00:00')
    AND person_id IN (SELECT person_id FROM events WHERE event = 'onboarding_completed'
                      AND timestamp >= toDateTime('2026-09-01 00:00:00'))
  GROUP BY person_id
),
pop AS (
  SELECT onb.person_id AS person_id, onb.onb_ts AS onb_ts, onb.os AS os, onb.cc AS cc, onb.tz AS tz, onb.ver AS ver,
    if(onb.os = 'Android' AND onb.cc IN ('CI','DZ','IR','IQ','PK','SA')
       AND onb.onb_ts >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(onb.onb_ts >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM onb INNER JOIN flags ON onb.person_id = flags.person_id
  WHERE flags.bot = 0 AND flags.emu = 0 AND flags.tf = 0 AND onb.n_onb_life < 3 AND flags.n_ver < 10
)
SELECT seg, win_b, os, count() AS persons, min(onb_ts) AS first_onb, max(onb_ts) AS last_onb
FROM pop GROUP BY seg, win_b, os ORDER BY seg, win_b, os
```

```sql
-- @@ landing_summary
WITH onb AS (
  SELECT person_id,
    minIf(timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS onb_ts,
    count() AS n_onb_life,
    argMinIf(properties.$os, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS os,
    argMinIf(properties.$geoip_country_code, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS cc,
    argMinIf(properties.$timezone, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS tz,
    argMinIf(properties.$app_version, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS ver
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-04-22 00:00:00')
  GROUP BY person_id
  HAVING countIf(timestamp >= toDateTime('2026-09-01 00:00:00')) > 0
),
flags AS (
  SELECT person_id,
    countIf(properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro')) AS bot,
    countIf(properties.$is_emulator = true) AS emu,
    countIf(properties.$is_testflight = true) AS tf,
    count(DISTINCT properties.$app_version) AS n_ver
  FROM events
  WHERE properties.$lib = 'posthog-flutter' AND timestamp >= toDateTime('2026-08-25 00:00:00')
    AND person_id IN (SELECT person_id FROM events WHERE event = 'onboarding_completed'
                      AND timestamp >= toDateTime('2026-09-01 00:00:00'))
  GROUP BY person_id
),
pop AS (
  SELECT onb.person_id AS person_id, onb.onb_ts AS onb_ts, onb.os AS os, onb.cc AS cc, onb.tz AS tz, onb.ver AS ver,
    if(onb.os = 'Android' AND onb.cc IN ('CI','DZ','IR','IQ','PK','SA')
       AND onb.onb_ts >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(onb.onb_ts >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM onb INNER JOIN flags ON onb.person_id = flags.person_id
  WHERE flags.bot = 0 AND flags.emu = 0 AND flags.tf = 0 AND onb.n_onb_life < 3 AND flags.n_ver < 10
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter'
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT seg, win_b, count() AS landed,
  quantile(0.5)(dateDiff('second', onb_ts, land_ts)) AS med_s_onb_to_land,
  countIf(dateDiff('second', onb_ts, land_ts) <= 1800) AS landed_within_30m
FROM land GROUP BY seg, win_b ORDER BY seg, win_b
```

### Pass 1: exclusion counts

```sql
-- @@ excluded_counts
WITH onb AS (
  SELECT person_id,
    minIf(timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS onb_ts,
    count() AS n_onb_life,
    argMinIf(properties.$os, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS os,
    argMinIf(properties.$geoip_country_code, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS cc,
    argMinIf(properties.$timezone, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS tz,
    argMinIf(properties.$app_version, timestamp, timestamp >= toDateTime('2026-09-01 00:00:00')) AS ver
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-04-22 00:00:00')
  GROUP BY person_id
  HAVING countIf(timestamp >= toDateTime('2026-09-01 00:00:00')) > 0
),
flags AS (
  SELECT person_id,
    countIf(properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro')) AS bot,
    countIf(properties.$is_emulator = true) AS emu,
    countIf(properties.$is_testflight = true) AS tf,
    count(DISTINCT properties.$app_version) AS n_ver
  FROM events
  WHERE properties.$lib = 'posthog-flutter' AND timestamp >= toDateTime('2026-08-25 00:00:00')
    AND person_id IN (SELECT person_id FROM events WHERE event = 'onboarding_completed'
                      AND timestamp >= toDateTime('2026-09-01 00:00:00'))
  GROUP BY person_id
)
SELECT
  countIf(flags.tf > 0) AS testflight_persons,
  countIf(flags.bot > 0) AS bot_device_persons,
  countIf(flags.emu > 0) AS emulator_persons,
  countIf(flags.tf = 0 AND flags.bot = 0 AND flags.emu = 0 AND (onb.n_onb_life >= 3 OR flags.n_ver >= 10)) AS tester_heuristic_persons,
  countIf(flags.tf = 0 AND flags.bot = 0 AND flags.emu = 0 AND onb.n_onb_life < 3 AND flags.n_ver < 10) AS kept,
  countIf(flags.tf > 0 AND onb.onb_ts >= toDateTime('2026-10-03 00:00:00')) AS testflight_win_b
FROM onb INNER JOIN flags ON onb.person_id = flags.person_id
```

### Pass 1: event verification, all traffic

```sql
-- @@ verify_events_all_traffic
SELECT event, properties.$lib AS lib, max(timestamp) AS last_seen,
  countIf(timestamp > now() - INTERVAL 30 DAY) AS vol_30d,
  count(DISTINCT if(timestamp > now() - INTERVAL 30 DAY, person_id, NULL)) AS persons_30d,
  min(timestamp) AS first_seen
FROM events
WHERE event IN ('first_conversation_ended','post_onboarding_offer_result','push_prompt_result',
                'personal_reveal_viewed','trial_reminder_sheet_shown','symptom_scored','reflect_session_started')
  AND timestamp > toDateTime('2026-08-01 00:00:00')
GROUP BY event, lib ORDER BY event
```

### Pass 2: main pull (`__POP_IDS__` = the 42 kept person_ids from the `pop_summary` CTE)

```sql
-- @@ events_30m_after_land
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT e.event AS event, count() AS c, count(DISTINCT e.person_id) AS persons,
  count(DISTINCT if(l.win_b = 0, e.person_id, NULL)) AS p_pre_1003,
  count(DISTINCT if(l.win_b = 1, e.person_id, NULL)) AS p_win_b
FROM events e INNER JOIN land l ON e.person_id = l.person_id
WHERE e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
  AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
  AND e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
  AND e.event NOT IN ('$screen','api_error','$set','$identify','$exception','client_error','usage_snapshot','usage_load_failed','$autocapture','$rageclick','app_install_attributed','$feature_flag_called','notification_received')
GROUP BY event ORDER BY persons DESC, c DESC LIMIT 60
```

```sql
-- @@ screens_30m_after_land
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT e.properties.$screen_name AS screen, count() AS c, count(DISTINCT e.person_id) AS persons,
  count(DISTINCT if(l.win_b = 1, e.person_id, NULL)) AS p_win_b
FROM events e INNER JOIN land l ON e.person_id = l.person_id
WHERE e.event = '$screen' AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
  AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
  AND e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
GROUP BY screen ORDER BY persons DESC LIMIT 30
```

```sql
-- @@ nothing_after_land
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT win_b, count() AS landed,
  countIf(n_nonnoise = 0) AS zero_nonnoise_30m,
  countIf(n_action = 0) AS zero_action_30m,
  countIf(n_other_screen = 0) AS zero_nav_away_30m,
  countIf(n_action = 0 AND n_other_screen = 0) AS zero_action_and_zero_nav_30m,
  countIf(n_any = 0) AS zero_any_event_30m,
  countIf(sess_len_s < 60) AS landing_session_lt_60s,
  countIf(sess_len_s < 180) AS landing_session_lt_180s,
  quantile(0.5)(sess_len_s) AS med_landing_session_s
FROM (
  SELECT l.person_id AS person_id, any(l.win_b) AS win_b,
    countIf(e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
            AND e.event NOT IN ('$screen','api_error','$set','$identify','$exception','client_error','usage_snapshot','usage_load_failed','$autocapture','$rageclick','app_install_attributed','$feature_flag_called','notification_received')) AS n_nonnoise,
    countIf(e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
            AND e.event NOT IN ('$screen','api_error','$set','$identify','$exception','client_error','usage_snapshot','usage_load_failed','$autocapture','$rageclick','app_install_attributed','$feature_flag_called','notification_received') AND e.event NOT IN ('first_capture_prompt_shown','trial_bar_viewed','usage_limit_panel_shown','notification_permission_prompted','notification_permission_granted','notification_permission_denied','paywall_shown','inapp_insight.shown','inapp_insight.generated','premium_view_shown','usage_last_free_note_shown','app_tour_started','app_tour_step_viewed','push_prompt_viewed','reflect_mode_choice_shown','reflect_entry_sources_shown','reflect_entry_sources_served','premium_welcome_viewed','timeline_viewed','workspace_opened','character_card_viewed','habit_tracker_viewed','bio_viewed','user_activated','realization_detected','orca_memory_viewed')) AS n_action,
    countIf(e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
            AND e.event = '$screen' AND e.properties.$screen_name NOT IN ('mainPage','mainPageTab','splash')) AS n_other_screen,
    countIf(e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE) AS n_any,
    dateDiff('second', any(l.land_ts), maxIf(e.timestamp, e.$session_id = l.land_sid)) AS sess_len_s
  FROM events e INNER JOIN land l ON e.person_id = l.person_id
  WHERE e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp >= l.land_ts AND e.timestamp < l.land_ts + INTERVAL 1 DAY
  GROUP BY l.person_id
)
GROUP BY win_b WITH TOTALS ORDER BY win_b
```

```sql
-- @@ push_prompt_result
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT e.properties.result AS result, e.properties.os_status AS os_status, count() AS c,
  count(DISTINCT e.person_id) AS persons
FROM events e INNER JOIN pop p ON e.person_id = p.person_id
WHERE e.event = 'push_prompt_result' AND e.person_id IN __POP_IDS__
  AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts - INTERVAL 1 HOUR
GROUP BY result, os_status ORDER BY persons DESC
```

```sql
-- @@ notif_permission_7d
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT p.win_b AS win_b, count() AS persons,
  countIf(x.viewed > 0) AS push_prompt_viewed,
  countIf(x.res > 0) AS push_prompt_result,
  countIf(x.prompted > 0) AS os_prompted,
  countIf(x.granted > 0) AS granted,
  countIf(x.denied > 0) AS denied,
  countIf(x.granted > 0 AND x.denied = 0) AS granted_only
FROM pop p LEFT JOIN (
  SELECT e.person_id AS person_id,
    countIf(e.event = 'push_prompt_viewed') AS viewed,
    countIf(e.event = 'push_prompt_result') AS res,
    countIf(e.event = 'notification_permission_prompted') AS prompted,
    countIf(e.event = 'notification_permission_granted') AS granted,
    countIf(e.event = 'notification_permission_denied') AS denied
  FROM events e INNER JOIN pop p2 ON e.person_id = p2.person_id
  WHERE e.event IN ('push_prompt_viewed','push_prompt_result','notification_permission_prompted',
                    'notification_permission_granted','notification_permission_denied')
    AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-08-31 00:00:00')
    AND e.timestamp >= p2.onb_ts - INTERVAL 1 HOUR AND e.timestamp < p2.onb_ts + INTERVAL 7 DAY
  GROUP BY e.person_id
) x ON p.person_id = x.person_id
GROUP BY win_b WITH TOTALS ORDER BY win_b
```

```sql
-- @@ notif_permission_by_os
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT p.os AS os, count() AS persons,
  countIf(x.granted > 0) AS granted, countIf(x.denied > 0) AS denied, countIf(x.prompted > 0) AS os_prompted
FROM pop p LEFT JOIN (
  SELECT e.person_id AS person_id,
    countIf(e.event = 'notification_permission_prompted') AS prompted,
    countIf(e.event = 'notification_permission_granted') AS granted,
    countIf(e.event = 'notification_permission_denied') AS denied
  FROM events e INNER JOIN pop p2 ON e.person_id = p2.person_id
  WHERE e.event IN ('notification_permission_prompted','notification_permission_granted','notification_permission_denied')
    AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-08-31 00:00:00')
    AND e.timestamp >= p2.onb_ts - INTERVAL 1 HOUR AND e.timestamp < p2.onb_ts + INTERVAL 7 DAY
  GROUP BY e.person_id
) x ON p.person_id = x.person_id
GROUP BY os ORDER BY os
```

```sql
-- @@ return_d1_7
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT count() AS eligible_onb_before_now_minus_8d,
  countIf(coalesce(x.ret, 0) > 0) AS returned_24h_to_8d
FROM pop p LEFT JOIN (
  SELECT e.person_id AS person_id, count() AS ret
  FROM events e INNER JOIN pop p2 ON e.person_id = p2.person_id
  WHERE e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.event NOT IN ('$set','$identify','app_install_attributed','notification_received')
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp >= p2.onb_ts + INTERVAL 1 DAY AND e.timestamp < p2.onb_ts + INTERVAL 8 DAY
  GROUP BY e.person_id
) x ON p.person_id = x.person_id
WHERE p.onb_ts < now() - INTERVAL 8 DAY
```

```sql
-- @@ return_d1_7_alltime_cohort_partial
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT count() AS all_pop, countIf(p.onb_ts >= now() - INTERVAL 8 DAY) AS censored_lt_8d,
  countIf(coalesce(x.ret, 0) > 0) AS returned_24h_plus_any
FROM pop p LEFT JOIN (
  SELECT e.person_id AS person_id, count() AS ret
  FROM events e INNER JOIN pop p2 ON e.person_id = p2.person_id
  WHERE e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.event NOT IN ('$set','$identify','app_install_attributed','notification_received')
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp >= p2.onb_ts + INTERVAL 1 DAY AND e.timestamp < p2.onb_ts + INTERVAL 8 DAY
  GROUP BY e.person_id
) x ON p.person_id = x.person_id
```

```sql
-- @@ active_days_first7
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT count() AS eligible_onb_before_now_minus_7d,
  countIf(coalesce(x.days24, 0) >= 3) AS days_3plus_24h_buckets,
  countIf(coalesce(x.days24, 0) = 2) AS days_2_24h_buckets,
  countIf(coalesce(x.days24, 0) <= 1) AS days_1_24h_buckets,
  countIf(coalesce(x.cal_days, 0) >= 3) AS days_3plus_utc_calendar
FROM pop p LEFT JOIN (
  SELECT e.person_id AS person_id,
    count(DISTINCT intDiv(dateDiff('second', p2.onb_ts, e.timestamp), 86400)) AS days24,
    count(DISTINCT toDate(e.timestamp)) AS cal_days
  FROM events e INNER JOIN pop p2 ON e.person_id = p2.person_id
  WHERE e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.event NOT IN ('$set','$identify','app_install_attributed','notification_received')
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp >= p2.onb_ts AND e.timestamp < p2.onb_ts + INTERVAL 7 DAY
  GROUP BY e.person_id
) x ON p.person_id = x.person_id
WHERE p.onb_ts < now() - INTERVAL 7 DAY
```

```sql
-- @@ first_tab_after_land_30m
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT first_tab, count() AS persons, countIf(win_b = 1) AS p_win_b
FROM (
  SELECT l.person_id AS person_id, any(l.win_b) AS win_b,
    argMinIf(e.properties.tab_name, e.timestamp, e.event = 'tab_switched') AS first_tab
  FROM events e INNER JOIN land l ON e.person_id = l.person_id
  WHERE e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
  GROUP BY l.person_id
)
GROUP BY first_tab ORDER BY persons DESC
```

```sql
-- @@ first_tab_after_land_7d
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT first_tab, count() AS persons
FROM (
  SELECT e.person_id AS person_id, argMin(e.properties.tab_name, e.timestamp) AS first_tab
  FROM events e INNER JOIN land l ON e.person_id = l.person_id
  WHERE e.event = 'tab_switched' AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp > l.land_ts AND e.timestamp < l.onb_ts + INTERVAL 7 DAY
  GROUP BY e.person_id
)
GROUP BY first_tab ORDER BY persons DESC
```

```sql
-- @@ first_capture_events_7d
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT e.event AS event, e.properties.entry_point AS entry_point,
  coalesce(e.properties.choice, e.properties.dismiss_method, '') AS choice_or_method,
  count() AS c, count(DISTINCT e.person_id) AS persons,
  count(DISTINCT if(p.win_b = 1, e.person_id, NULL)) AS p_win_b
FROM events e INNER JOIN pop p ON e.person_id = p.person_id
WHERE e.event IN ('first_capture_prompt_shown','first_capture_prompt_option_tapped','first_capture_prompt_dismissed',
                  'usage_chip_tapped_at_zero')
  AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
  AND e.timestamp >= p.onb_ts - INTERVAL 1 HOUR AND e.timestamp < p.onb_ts + INTERVAL 7 DAY
GROUP BY event, entry_point, choice_or_method ORDER BY event, persons DESC LIMIT 40
```

```sql
-- @@ flow_screens_origin_7d
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT screen, prev_screen, count() AS c, count(DISTINCT person_id) AS persons,
  count(DISTINCT if(ts < onb_plus_45m, person_id, NULL)) AS persons_within_45m_of_onb
FROM (
  SELECT e.person_id AS person_id, e.properties.$screen_name AS screen,
    lagInFrame(e.properties.$screen_name, 1, '') OVER (PARTITION BY e.person_id ORDER BY e.timestamp
      ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW) AS prev_screen,
    e.timestamp AS ts, p.onb_ts + INTERVAL 45 MINUTE AS onb_plus_45m
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp >= p.onb_ts AND e.timestamp < p.onb_ts + INTERVAL 7 DAY
)
WHERE screen IN ('afterTherapyFlow','prepTherapyFlow','betweenSessionsFlow','recordSessionFlow','healthCheckFlow','audioChat','reflectModeChoice')
GROUP BY screen, prev_screen ORDER BY screen, persons DESC LIMIT 60
```

```sql
-- @@ moment_sent_7d
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT e.properties.moment_type AS moment_type, count() AS sent, count(DISTINCT e.person_id) AS persons,
  countIf(e.properties.has_token = true) AS sent_with_token
FROM events e INNER JOIN pop p ON e.person_id = p.person_id
WHERE e.event = 'moment.sent' AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
  AND e.timestamp >= p.onb_ts AND e.timestamp < p.onb_ts + INTERVAL 7 DAY
GROUP BY moment_type WITH TOTALS ORDER BY persons DESC LIMIT 40
```

```sql
-- @@ moment_opened_7d_via_id
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT s.moment_type AS moment_type, count() AS opened, count(DISTINCT o.person_id) AS persons
FROM (
  SELECT e.person_id AS person_id, e.properties.moment_id AS moment_id
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = 'moment.opened' AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp >= p.onb_ts AND e.timestamp < p.onb_ts + INTERVAL 7 DAY
) o
LEFT JOIN (
  SELECT properties.moment_id AS moment_id, any(properties.moment_type) AS moment_type
  FROM events WHERE event = 'moment.sent' AND person_id IN __POP_IDS__
    AND timestamp >= toDateTime('2026-08-25 00:00:00')
  GROUP BY moment_id
) s ON o.moment_id = s.moment_id
GROUP BY moment_type ORDER BY persons DESC
```

```sql
-- @@ notification_opened_client_7d
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT e.properties.moment_type AS moment_type, count() AS opened, count(DISTINCT e.person_id) AS persons
FROM events e INNER JOIN pop p ON e.person_id = p.person_id
WHERE e.event = 'notification_opened' AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
  AND e.timestamp >= p.onb_ts AND e.timestamp < p.onb_ts + INTERVAL 7 DAY
GROUP BY moment_type ORDER BY persons DESC LIMIT 30
```

```sql
-- @@ verify_events_in_pop_7d
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT e.event AS event, count() AS c, count(DISTINCT e.person_id) AS persons,
  count(DISTINCT if(p.win_b = 1, e.person_id, NULL)) AS p_win_b
FROM events e INNER JOIN pop p ON e.person_id = p.person_id
WHERE e.event IN ('first_conversation_ended','post_onboarding_offer_result','push_prompt_result',
                  'personal_reveal_viewed','trial_reminder_sheet_shown','symptom_scored','reflect_session_started',
                  'first_conversation_started','post_onboarding_offer_not_shown','paywall_shown')
  AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
  AND e.timestamp >= p.onb_ts - INTERVAL 1 HOUR AND e.timestamp < p.onb_ts + INTERVAL 7 DAY
GROUP BY event ORDER BY event
```

```sql
-- @@ onb_hour_rows
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT tz, toStartOfHour(onb_ts) AS utc_hour, win_b, count() AS persons FROM pop
GROUP BY tz, utc_hour, win_b ORDER BY utc_hour LIMIT 200
```

```sql
-- @@ new_wave_reach
SELECT
  count(DISTINCT if(event = 'onboarding_started', person_id, NULL)) AS started_onb,
  count(DISTINCT if(event = 'onboarding_step_completed', person_id, NULL)) AS completed_a_step,
  count(DISTINCT if(event = 'onboarding_completed', person_id, NULL)) AS completed_onb,
  count(DISTINCT person_id) AS any_client_event
FROM events
WHERE properties.$lib = 'posthog-flutter' AND timestamp >= toDateTime('2026-09-20 00:00:00')
  AND properties.$os = 'Android' AND properties.$geoip_country_code IN ('CI','DZ','IR','IQ','PK','SA')
  AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND properties.$is_emulator != true
```

### Pass 3: follow-ups

```sql
-- @@ nothing_after_land_strict
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT win_b, count() AS landed,
  countIf(n_product_action = 0) AS zero_product_action_30m,
  countIf(n_product_action = 0 AND n_other_screen = 0) AS zero_product_action_zero_nav_30m,
  countIf(n_product_action = 0 AND sess_len_s < 180) AS zero_product_action_session_lt_180s,
  countIf(n_tab = 0 AND n_other_screen = 0) AS never_left_home_30m,
  quantile(0.5)(first_action_s) AS med_s_to_first_product_action
FROM (
  SELECT l.person_id AS person_id, any(l.win_b) AS win_b,
    countIf(e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
            AND e.event NOT IN ('$screen','api_error','$set','$identify','$exception','client_error','usage_snapshot','usage_load_failed','$autocapture','$rageclick','app_install_attributed','$feature_flag_called','notification_received') AND e.event NOT IN ('first_capture_prompt_shown','trial_bar_viewed','usage_limit_panel_shown','notification_permission_prompted','notification_permission_granted','notification_permission_denied','paywall_shown','inapp_insight.shown','inapp_insight.generated','premium_view_shown','usage_last_free_note_shown','app_tour_started','app_tour_step_viewed','push_prompt_viewed','reflect_mode_choice_shown','reflect_entry_sources_shown','reflect_entry_sources_served','premium_welcome_viewed','timeline_viewed','workspace_opened','character_card_viewed','habit_tracker_viewed','bio_viewed','user_activated','realization_detected','orca_memory_viewed') AND e.event NOT IN ('app_tour_completed','app_tour_skipped')) AS n_product_action,
    countIf(e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
            AND e.event = '$screen' AND e.properties.$screen_name NOT IN ('mainPage','mainPageTab','splash')) AS n_other_screen,
    countIf(e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE AND e.event = 'tab_switched') AS n_tab,
    dateDiff('second', any(l.land_ts), maxIf(e.timestamp, e.$session_id = l.land_sid)) AS sess_len_s,
    dateDiff('second', any(l.land_ts), minIf(e.timestamp, e.timestamp > l.land_ts
            AND e.event NOT IN ('$screen','api_error','$set','$identify','$exception','client_error','usage_snapshot','usage_load_failed','$autocapture','$rageclick','app_install_attributed','$feature_flag_called','notification_received') AND e.event NOT IN ('first_capture_prompt_shown','trial_bar_viewed','usage_limit_panel_shown','notification_permission_prompted','notification_permission_granted','notification_permission_denied','paywall_shown','inapp_insight.shown','inapp_insight.generated','premium_view_shown','usage_last_free_note_shown','app_tour_started','app_tour_step_viewed','push_prompt_viewed','reflect_mode_choice_shown','reflect_entry_sources_shown','reflect_entry_sources_served','premium_welcome_viewed','timeline_viewed','workspace_opened','character_card_viewed','habit_tracker_viewed','bio_viewed','user_activated','realization_detected','orca_memory_viewed') AND e.event NOT IN ('app_tour_completed','app_tour_skipped'))) AS first_action_s
  FROM events e INNER JOIN land l ON e.person_id = l.person_id
  WHERE e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp >= l.land_ts AND e.timestamp < l.land_ts + INTERVAL 1 DAY
  GROUP BY l.person_id
)
GROUP BY win_b ORDER BY win_b
```

```sql
-- @@ tour_outcome_30m
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT count() AS landed, countIf(started > 0) AS tour_started, countIf(completed > 0) AS tour_completed,
  countIf(skipped > 0) AS tour_skipped, countIf(started > 0 AND completed = 0 AND skipped = 0) AS tour_no_outcome
FROM (
  SELECT l.person_id AS person_id,
    countIf(e.event = 'app_tour_started') AS started,
    countIf(e.event = 'app_tour_completed') AS completed,
    countIf(e.event = 'app_tour_skipped') AS skipped
  FROM land l LEFT JOIN (
    SELECT person_id, event, timestamp FROM events
    WHERE event IN ('app_tour_started','app_tour_completed','app_tour_skipped')
      AND person_id IN __POP_IDS__ AND timestamp >= toDateTime('2026-09-01 00:00:00')
  ) e ON e.person_id = l.person_id
  WHERE e.timestamp >= l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
  GROUP BY l.person_id
)
```

```sql
-- @@ moment_totals_7d
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT
  count(DISTINCT if(e.event = 'moment.sent', e.person_id, NULL)) AS persons_sent,
  countIf(e.event = 'moment.sent') AS sends,
  count(DISTINCT if(e.event = 'moment.sent' AND e.properties.has_token = true, e.person_id, NULL)) AS persons_sent_with_token,
  count(DISTINCT if(e.event = 'moment.opened', e.person_id, NULL)) AS persons_opened_backend,
  countIf(e.event = 'moment.opened') AS opens_backend,
  count(DISTINCT if(e.event = 'moment.acted', e.person_id, NULL)) AS persons_acted_backend,
  count(DISTINCT if(e.event = 'notification_opened', e.person_id, NULL)) AS persons_notification_opened_client,
  countIf(e.event = 'notification_opened') AS notification_opened_client
FROM events e INNER JOIN pop p ON e.person_id = p.person_id
WHERE e.event IN ('moment.sent','moment.opened','moment.acted','notification_opened')
  AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
  AND e.timestamp >= p.onb_ts AND e.timestamp < p.onb_ts + INTERVAL 7 DAY
```

```sql
-- @@ moment_sent_by_day_since_onb
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT intDiv(dateDiff('second', p.onb_ts, e.timestamp), 86400) AS day_since_onb,
  count() AS sends, count(DISTINCT e.person_id) AS persons
FROM events e INNER JOIN pop p ON e.person_id = p.person_id
WHERE e.event = 'moment.sent' AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
  AND e.timestamp >= p.onb_ts AND e.timestamp < p.onb_ts + INTERVAL 7 DAY
GROUP BY day_since_onb ORDER BY day_since_onb
```

```sql
-- @@ moment_sent_7d_eligible_only
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT e.properties.moment_type AS moment_type, count(DISTINCT e.person_id) AS persons
FROM events e INNER JOIN pop p ON e.person_id = p.person_id
WHERE e.event = 'moment.sent' AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
  AND p.onb_ts < now() - INTERVAL 7 DAY
  AND e.timestamp >= p.onb_ts AND e.timestamp < p.onb_ts + INTERVAL 7 DAY
GROUP BY moment_type ORDER BY persons DESC LIMIT 20
```

```sql
-- @@ landing_tab_card
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT count() AS landed,
  countIf(card > 0) AS getting_started_card_shown_30m,
  countIf(tab_ws > 0) AS switched_to_workspace_30m,
  countIf(tab_reflect > 0) AS switched_to_reflect_30m,
  countIf(after_flow > 0) AS entered_after_therapy_flow_30m,
  countIf(any_flow > 0) AS entered_any_capture_flow_30m
FROM (
  SELECT l.person_id AS person_id,
    countIf(e.event = 'first_capture_prompt_shown' AND e.properties.entry_point = 'home_empty_state') AS card,
    countIf(e.event = 'tab_switched' AND e.properties.tab_name = 'workspace') AS tab_ws,
    countIf(e.event = 'tab_switched' AND e.properties.tab_name = 'reflect') AS tab_reflect,
    countIf(e.event = '$screen' AND e.properties.$screen_name = 'afterTherapyFlow') AS after_flow,
    countIf(e.event = '$screen' AND e.properties.$screen_name IN ('afterTherapyFlow','prepTherapyFlow','betweenSessionsFlow','recordSessionFlow')) AS any_flow
  FROM events e INNER JOIN land l ON e.person_id = l.person_id
  WHERE e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp >= l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
  GROUP BY l.person_id
)
```

### Pass 4: core capture

```sql
-- @@ core_capture_30m_after_land
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
),
land AS (
  SELECT e.person_id AS person_id, min(e.timestamp) AS land_ts,
         argMin(e.$session_id, e.timestamp) AS land_sid,
         any(p.seg) AS seg, any(p.win_b) AS win_b, any(p.onb_ts) AS onb_ts
  FROM events e INNER JOIN pop p ON e.person_id = p.person_id
  WHERE e.event = '$screen' AND e.properties.$screen_name = 'mainPage'
    AND e.properties.$lib = 'posthog-flutter' AND e.person_id IN __POP_IDS__
    AND e.timestamp >= toDateTime('2026-09-01 00:00:00') AND e.timestamp >= p.onb_ts
  GROUP BY e.person_id
)
SELECT win_b, count() AS landed, countIf(n_core > 0) AS did_core_capture_30m
FROM (
  SELECT l.person_id AS person_id, any(l.win_b) AS win_b,
    countIf(e.event IN ('debrief_started','between_session_started','prep_capture_started','health_check_started','reflect_message_submitted','recording_started','quick_capture_submitted','symptom_created','habit_created','voice_chat_started','first_conversation_started')) AS n_core
  FROM land l LEFT JOIN (
    SELECT person_id, event, timestamp FROM events
    WHERE event IN ('debrief_started','between_session_started','prep_capture_started','health_check_started','reflect_message_submitted','recording_started','quick_capture_submitted','symptom_created','habit_created','voice_chat_started','first_conversation_started') AND person_id IN __POP_IDS__ AND timestamp >= toDateTime('2026-09-01 00:00:00')
  ) e ON e.person_id = l.person_id AND e.timestamp > l.land_ts AND e.timestamp < l.land_ts + INTERVAL 30 MINUTE
  GROUP BY l.person_id
)
GROUP BY win_b ORDER BY win_b
```

```sql
-- @@ core_capture_7d_eligible
WITH pop AS (
  SELECT person_id,
    min(timestamp) AS onb_ts,
    argMin(properties.$os, timestamp) AS os,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$timezone, timestamp) AS tz,
    if(argMin(properties.$os, timestamp) = 'Android'
       AND argMin(properties.$geoip_country_code, timestamp) IN ('CI','DZ','IR','IQ','PK','SA')
       AND min(timestamp) >= toDateTime('2026-09-20 00:00:00'), 'new_wave', 'rest') AS seg,
    if(min(timestamp) >= toDateTime('2026-10-03 00:00:00'), 1, 0) AS win_b
  FROM events
  WHERE event = 'onboarding_completed' AND properties.$lib = 'posthog-flutter'
    AND timestamp >= toDateTime('2026-09-01 00:00:00') AND person_id IN __POP_IDS__
  GROUP BY person_id
)
SELECT count() AS eligible_onb_before_now_minus_7d, countIf(coalesce(x.n, 0) > 0) AS did_core_capture_7d
FROM pop p LEFT JOIN (
  SELECT e.person_id AS person_id, count() AS n
  FROM events e INNER JOIN pop p2 ON e.person_id = p2.person_id
  WHERE e.event IN ('debrief_started','between_session_started','prep_capture_started','health_check_started','reflect_message_submitted','recording_started','quick_capture_submitted','symptom_created','habit_created','voice_chat_started','first_conversation_started') AND e.person_id IN __POP_IDS__ AND e.timestamp >= toDateTime('2026-09-01 00:00:00')
    AND e.timestamp >= p2.onb_ts AND e.timestamp < p2.onb_ts + INTERVAL 7 DAY
  GROUP BY e.person_id
) x ON p.person_id = x.person_id
WHERE p.onb_ts < now() - INTERVAL 7 DAY
```

Local-hour conversion (Q5): rows of `onb_hour_rows` (`$timezone`, UTC hour, count) were converted with Python `datetime.astimezone(zoneinfo.ZoneInfo(tz))` and bucketed by 3 hours. Intermediate rows were not stored.
