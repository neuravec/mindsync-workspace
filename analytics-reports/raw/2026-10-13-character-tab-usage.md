# Character tab usage vs other bottom tabs: raw PostHog extract

- **Date**: 2026-10-13 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: last 30d (2026-09-13 → 2026-10-13) and last 90d (2026-07-15 → 2026-10-13), UTC
- **Question**: How much is the Character bottom tab used compared with Main, Therapy (Timeline), Reflect and Workspace?
- **Filters (all queries)**: `properties.$lib = 'posthog-flutter'`, `$is_testflight != true`, `$is_emulator != true`, `$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')`
- **Event verification** (unfiltered, 90d):

| event | lib | 90d events / users | 30d events / users | first in window | last seen | role |
|---|---|---|---|---|---|---|
| `tab_switched` (prop `tab_name`) | posthog-flutter | 10,465 / 121 | 3,571 / 56 | 07-15 (window start) | 2026-10-13 | **primary tab-open signal** |
| `character_card_viewed` | posthog-flutter | 1,273 / 99 | 493 / 46 | 07-15 | 2026-10-13 | card load, NOT a tab-open signal (also fires on init, after every capture flow, after Settings edits) |
| `bio_viewed` | posthog-flutter | 862 / 67 | 475 / 44 | 08-11 | 2026-10-13 | fires on the same loads when bio has content |
| `bio_refreshed` | posthog-flutter | 64 / 5 | 29 / 1 | 07-17 | 2026-10-13 | in-tab action |
| `orca_color_changed` | posthog-flutter | 113 / 15 | 74 / 9 | 07-21 | 2026-10-13 | in-tab action |
| `orca_named` | posthog-flutter | 17 / 11 | 9 / 7 | 07-21 | 2026-10-13 | in-tab action |
| `content_shared` (`content_type`) | posthog-flutter | 77 / 9 | 43 / 3 | 07-18 | 2026-10-13 | `Personal Bio` = Character share |

- No `$screen` exists for any bottom tab (tabs live inside `mainPage`). No events named `*stats*`, `*streak*`, `*achievement*`. `orca_memory_*` is reached from Settings, not Character; `personal_reveal_*` is the post-onboarding wow flow. Both excluded.
- `tab_name` values: `main, therapy, reflect, workspace, character`; legacy `stats` (pre-Workspace, last 2026-09-22, 1 user in 30d) ignored.

## Results

### Base
| metric | 30d | 90d |
|---|---|---|
| any filtered app event (incl. splash/welcome/auth only) | 255 | 468 |
| **reached the app shell** (`$screen mainPage` or any `tab_switched`) = base for % | **55** | **143** |

### 1-2. Tab opens, raw `tab_switched`
| tab | users 30d | % of 55 | opens 30d | mean opens/user | median opens/user | users 2+ days | users 90d | opens 90d | top1 user 30d |
|---|---|---|---|---|---|---|---|---|---|
| therapy | 50 | 91% | 530 | 10.6 | 5 | 21 | 108 | 1,867 | 115 |
| reflect | 48 | 87% | 547 | 11.4 | 5 | 21 | 106 | 1,878 | 111 |
| workspace | 44 | 80% | 395 | 9.0 | 4 | 19 | 90 | 1,408 | 95 |
| main | 39 | 71% | 272 | 7.0 | 3 | 15 | 80 | 976 | 69 |
| **character** | **38** | **69%** | **211** | **5.6** | **2** | **10** | **83** | **706** | 47 |

### 1-2b. "Settled" opens (stayed >= 3 s before next tab switch; removes PageView pass-through)
| tab | users 30d | % of 55 | settled opens 30d | opens/user | user-days 30d | user-days/user | users 90d | settled opens 90d |
|---|---|---|---|---|---|---|---|---|
| therapy | 43 | 78% | 190 | 4.4 | 91 | 2.1 | 92 | 626 |
| reflect | 40 | 73% | 168 | 4.2 | 91 | 2.3 | 88 | 534 |
| main | 39 | 71% | 160 | 4.1 | 82 | 2.1 | 77 | 557 |
| workspace | 39 | 71% | 164 | 4.2 | 82 | 2.1 | 80 | 594 |
| **character** | **35** | **64%** | **114** | **3.3** | **68** | **1.9** | **81** | **366** |

Main is the landing tab; arrival on it is not tracked as `tab_switched`, so all 55 shell users effectively saw Main.

### Weekly distinct users per tab (raw `tab_switched`, 90d)
| week | character | therapy | reflect | workspace | main | any switch |
|---|---|---|---|---|---|---|
| 07-12* | 5 | 7 | 7 | 1 | 6 | 8 |
| 07-19 | 8 | 10 | 10 | 2 | 7 | 11 |
| 07-26 | 13 | 14 | 13 | 10 | 11 | 14 |
| 08-02 | 15 | 19 | 19 | 18 | 15 | 19 |
| 08-09 | 16 | 22 | 21 | 18 | 14 | 22 |
| 08-16 | 12 | 22 | 22 | 17 | 17 | 22 |
| 08-23 | 6 | 11 | 12 | 10 | 8 | 13 |
| 08-30 | 13 | 17 | 15 | 15 | 13 | 17 |
| 09-06 | 14 | 19 | 23 | 18 | 13 | 24 |
| 09-13 | 8 | 12 | 11 | 9 | 9 | 12 |
| 09-20 | 12 | 18 | 15 | 13 | 13 | 19 |
| 09-27 | 13 | 19 | 20 | 18 | 17 | 21 |
| 10-04 | 13 | 19 | 18 | 18 | 16 | 19 |
| 10-11* | 9 | 11 | 10 | 9 | 7 | 11 |
\* partial week

### 3. Character reach among shell users
| metric | 30d (base 55) | 90d (base 143) |
|---|---|---|
| opened Character >= 1 (raw) | 38 (69%) | 83 (58%) |
| opened Character >= 1 (settled >= 3 s) | 35 (64%) | 81 (57%) |
| opened Character on 2+ different days | 10 (18%) | 29 (20%) |

### 4. Interactions inside Character (filtered)
| event | 30d events / users | 90d events / users | top1 user (90d) |
|---|---|---|---|
| `character_card_viewed` (load, not a tap) | 188 / 43 | 667 / 92 | n/a |
| `bio_viewed` (load with bio content) | 184 / 41 | 389 / 61 | n/a |
| `orca_color_changed` | 52 / 6 | 85 / 12 | 25 |
| `orca_named` | 8 / 6 | 15 / 10 | 4 |
| `bio_refreshed` | 4 / 1 | 23 / 4 | 11 |
| `content_shared` `Personal Bio` | 3 / 2 | 3 / 2 | n/a |

All active interactions are n<25 users in both windows (low confidence; counts are product-usage only, no health attributes).

### 5. Time on tab and next destination (30d)
Dwell = seconds from a `tab_switched` to the next `tab_switched` in the same `$session_id`, capped at 30 min. It does not see backgrounding or sub-screens pushed on top, so it is a lower bound.

| tab | opens | measured | median s | p25 s | p75 s | share < 3 s | share >= 30 s | median of per-user medians s |
|---|---|---|---|---|---|---|---|---|
| reflect | 547 | 496 | 0 | 0 | 2 | 76% | 9% | 0 |
| therapy | 530 | 491 | 0 | 0 | 4 | 69% | 6% | 0.5 |
| workspace | 395 | 365 | 1 | 0 | 8 | 63% | 15% | 1 |
| main | 272 | 227 | 3 | 0 | 19 | 49% | 19% | 4 |
| **character** | 211 | 180 | **2** | 0 | **12** | **54%** | **13%** | **4** |

Next destination after opening Character (first following nav event in session):
| next | events | users |
|---|---|---|
| tab: therapy | 52 | 20 |
| tab: workspace | 51 | 18 |
| tab: main | 29 | 16 |
| tab: reflect | 23 | 12 |
| screen: mainPage | 21 | 8 |
| none (session ended) | 19 | 14 |
| other screens (recordSessionFlow, subscription, settings, ...) | ≤4 each | ≤3 |

First event of any kind after a Character open: another `tab_switched` 105/27u, `character_card_viewed` 63/36u, `bio_viewed` 17/7u, `$screen` 11/7u.

### 6. Week-2 return by week-1 Character open (correlation only)
Cohort: first filtered app event 2026-07-15 → 2026-09-29 (≥14 d of follow-up), reached the shell in days 0-6. Return = any app event days 7-13.

| group | users | returned W2 | W2 rate |
|---|---|---|---|
| opened Character in week 1 | 49 | 16 | 32.7% |
| did not open Character in week 1 (combined) | 44 | 7 | 15.9% |

Sub-groups "switched tabs but not Character" (21) and "no tab switch" (23) are under 25 users each and are not reported separately.

## Caveats
- **PageView pass-through inflates middle tabs.** `MainNavCubit.selectTab` is also called from `PageView.onPageChanged`, so a tap from Main to Character fires `tab_switched` for the destination and then for every intermediate page during the 300 ms animation. In 30d, pairs of `tab_switched` under 1 s apart are dominated by therapy↔reflect (181/179), reflect→workspace (135), therapy→main (100). Therapy/Reflect/Workspace raw counts are therefore inflated; use the "settled" table for comparison. Character (index 4) and Main (index 0) are endpoints and are less affected. Instrumentation fix belongs to `flutter-mobile`.
- **Main is under-counted** in `tab_switched` (landing on it is not tracked, since 2026-10-07 via `track:false`, and app start lands there anyway).
- **`character_card_viewed` is not an open signal**: fires on cubit init, after every capture flow, and after Settings edits. Its 43 users/30d exceeds the 38 actual openers.
- **Single-user skew**: top tab_switched user = 1,281 of 6,937 filtered events in 90d; per-tab top1 in 30d is 47-115 opens. Means are skewed, medians reported alongside. `orca_color_changed` 25/85 and `bio_refreshed` 11/23 from one person.
- **Small n**: base is 55 shell users in 30d. Testers matter: unfiltered `tab_switched` 30d = 3,571 events vs 1,960 after filters.
- **Retention is correlation, not cause**: Character openers are also the people who explore more tabs in week 1. Cohort is clamped at the 90d window start (2026-07-15); ingest started 2026-04-22.
- Dwell is a lower bound (does not include time after the last switch of a session, backgrounding, or pushed sub-screens).

## Queries

```sql
-- base
SELECT
  count(DISTINCT if(timestamp > now() - INTERVAL 30 DAY, person_id, NULL)) AS any_app_30,
  count(DISTINCT if(timestamp > now() - INTERVAL 30 DAY AND ((event='$screen' AND properties.$screen_name='mainPage') OR event='tab_switched'), person_id, NULL)) AS reached_main_30,
  count(DISTINCT person_id) AS any_app_90,
  count(DISTINCT if((event='$screen' AND properties.$screen_name='mainPage') OR event='tab_switched', person_id, NULL)) AS reached_main_90
FROM events
WHERE timestamp > now() - INTERVAL 90 DAY
  AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
  AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')

-- raw tab opens
SELECT tab,
  sum(c30) AS opens_30, countIf(c30 > 0) AS users_30, round(sum(c30) / nullIf(countIf(c30 > 0), 0), 1) AS opens_per_user_30,
  round(avgIf(d30, c30 > 0), 2) AS avg_days_30, countIf(d30 >= 2) AS users_2plus_days_30, max(c30) AS top1_30,
  sum(c90) AS opens_90, countIf(c90 > 0) AS users_90, round(sum(c90) / nullIf(countIf(c90 > 0), 0), 1) AS opens_per_user_90,
  countIf(d90 >= 2) AS users_2plus_days_90, max(c90) AS top1_90
FROM (
  SELECT person_id, properties.tab_name AS tab,
    countIf(timestamp > now() - INTERVAL 30 DAY) AS c30,
    count(DISTINCT if(timestamp > now() - INTERVAL 30 DAY, toDate(timestamp), NULL)) AS d30,
    count() AS c90, count(DISTINCT toDate(timestamp)) AS d90
  FROM events
  WHERE event = 'tab_switched' AND timestamp > now() - INTERVAL 90 DAY
    AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
    AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  GROUP BY person_id, tab
)
GROUP BY tab ORDER BY users_30 DESC

-- medians (30d)
SELECT tab, count() AS users, quantile(0.5)(c) AS median_opens, quantile(0.5)(d) AS median_days
FROM (
  SELECT person_id, properties.tab_name AS tab, count() AS c, count(DISTINCT toDate(timestamp)) AS d
  FROM events
  WHERE event = 'tab_switched' AND timestamp > now() - INTERVAL 30 DAY
    AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
    AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  GROUP BY person_id, tab
) GROUP BY tab ORDER BY users DESC

-- settled opens (>= 3 s before next switch)
SELECT cur_tab,
  countIf(in30) AS settled_opens_30, count(DISTINCT if(in30, pid, NULL)) AS users_30,
  count(DISTINCT if(in30, concat(toString(pid), toString(toDate(ts))), NULL)) AS user_days_30,
  count() AS settled_opens_90, count(DISTINCT pid) AS users_90
FROM (
  SELECT pid, ts, cur_tab, ts > now() - INTERVAL 30 DAY AS in30, dateDiff('second', ts, next_ts) AS d, next_ts FROM (
    SELECT person_id AS pid, timestamp AS ts, toString(properties.tab_name) AS cur_tab,
      leadInFrame(toNullable(timestamp)) OVER (PARTITION BY $session_id ORDER BY timestamp ASC ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS next_ts
    FROM events
    WHERE timestamp > now() - INTERVAL 90 DAY AND event = 'tab_switched'
      AND $session_id IS NOT NULL AND $session_id != ''
      AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
      AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  )
)
WHERE (next_ts IS NULL OR d >= 3) AND cur_tab IN ('character','therapy','reflect','workspace','main')
GROUP BY cur_tab ORDER BY users_30 DESC

-- character reach (raw); settled variant = same window filter + d >= 3 as above
SELECT
  countIf(m30) AS reached_main_30, countIf(m30 AND ch30 >= 1) AS char_1plus_30, countIf(m30 AND chd30 >= 2) AS char_2plus_days_30,
  countIf(m90) AS reached_main_90, countIf(m90 AND ch90 >= 1) AS char_1plus_90, countIf(m90 AND chd90 >= 2) AS char_2plus_days_90
FROM (
  SELECT person_id,
    countIf(timestamp > now() - INTERVAL 30 DAY AND ((event='$screen' AND properties.$screen_name='mainPage') OR event='tab_switched')) > 0 AS m30,
    countIf((event='$screen' AND properties.$screen_name='mainPage') OR event='tab_switched') > 0 AS m90,
    countIf(timestamp > now() - INTERVAL 30 DAY AND event='tab_switched' AND properties.tab_name='character') AS ch30,
    count(DISTINCT if(timestamp > now() - INTERVAL 30 DAY AND event='tab_switched' AND properties.tab_name='character', toDate(timestamp), NULL)) AS chd30,
    countIf(event='tab_switched' AND properties.tab_name='character') AS ch90,
    count(DISTINCT if(event='tab_switched' AND properties.tab_name='character', toDate(timestamp), NULL)) AS chd90
  FROM events
  WHERE timestamp > now() - INTERVAL 90 DAY AND event IN ('$screen','tab_switched')
    AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
    AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  GROUP BY person_id
)

-- interactions
SELECT event, if(event='content_shared', toString(properties.content_type), '') AS sub,
  countIf(timestamp > now() - INTERVAL 30 DAY) AS c30,
  count(DISTINCT if(timestamp > now() - INTERVAL 30 DAY, person_id, NULL)) AS u30,
  count() AS c90, count(DISTINCT person_id) AS u90
FROM events
WHERE timestamp > now() - INTERVAL 90 DAY
  AND event IN ('character_card_viewed','bio_viewed','bio_refreshed','orca_color_changed','orca_named','content_shared')
  AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
  AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
GROUP BY event, sub ORDER BY c90 DESC LIMIT 30

-- dwell tab-to-tab (30d)
SELECT cur_tab, count() AS opens, countIf(next_ts IS NOT NULL AND d <= 1800) AS measured,
  quantileIf(0.5)(d, next_ts IS NOT NULL AND d <= 1800) AS median_s,
  quantileIf(0.25)(d, next_ts IS NOT NULL AND d <= 1800) AS p25_s,
  quantileIf(0.75)(d, next_ts IS NOT NULL AND d <= 1800) AS p75_s,
  round(countIf(next_ts IS NOT NULL AND d < 3) / countIf(next_ts IS NOT NULL AND d <= 1800), 3) AS share_under_3s,
  round(countIf(next_ts IS NOT NULL AND d >= 30 AND d <= 1800) / countIf(next_ts IS NOT NULL AND d <= 1800), 3) AS share_30s_plus
FROM (
  SELECT pid, ts, cur_tab, next_ts, dateDiff('second', ts, next_ts) AS d FROM (
    SELECT person_id AS pid, timestamp AS ts, toString(properties.tab_name) AS cur_tab,
      leadInFrame(toNullable(timestamp)) OVER (PARTITION BY $session_id ORDER BY timestamp ASC ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS next_ts
    FROM events
    WHERE timestamp > now() - INTERVAL 30 DAY AND event = 'tab_switched'
      AND $session_id IS NOT NULL AND $session_id != ''
      AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
      AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  )
)
WHERE cur_tab IN ('character','therapy','reflect','workspace','main')
GROUP BY cur_tab ORDER BY opens DESC

-- next nav after character (30d)
SELECT next_label, count() AS c, count(DISTINCT pid) AS users
FROM (
  SELECT person_id AS pid, event, toString(properties.tab_name) AS tab,
    leadInFrame(if(event = 'tab_switched', concat('tab:', toString(properties.tab_name)), concat('screen:', toString(properties.$screen_name)))) OVER (PARTITION BY $session_id ORDER BY timestamp ASC ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS next_label
  FROM events
  WHERE timestamp > now() - INTERVAL 30 DAY AND event IN ('tab_switched','$screen')
    AND $session_id IS NOT NULL AND $session_id != ''
    AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
    AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
)
WHERE event = 'tab_switched' AND tab = 'character'
GROUP BY next_label ORDER BY c DESC LIMIT 15

-- pass-through signature (pairs < 1 s apart)
SELECT cur_tab, next_tab, count() AS c FROM (
  SELECT toString(properties.tab_name) AS cur_tab, timestamp AS ts,
    leadInFrame(toString(properties.tab_name)) OVER (PARTITION BY $session_id ORDER BY timestamp ASC ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS next_tab,
    leadInFrame(toNullable(timestamp)) OVER (PARTITION BY $session_id ORDER BY timestamp ASC ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) AS next_ts
  FROM events
  WHERE timestamp > now() - INTERVAL 30 DAY AND event = 'tab_switched'
    AND $session_id IS NOT NULL AND $session_id != ''
    AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
    AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
) WHERE next_ts IS NOT NULL AND dateDiff('millisecond', ts, next_ts) < 1000
GROUP BY cur_tab, next_tab ORDER BY c DESC LIMIT 15

-- week-2 return by week-1 character open
WITH ev AS (
  SELECT person_id AS pid, timestamp AS ts, event, toString(properties.tab_name) AS tab, toString(properties.$screen_name) AS scr
  FROM events
  WHERE timestamp >= toDateTime('2026-04-22 00:00:00')
    AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
    AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
),
per AS (SELECT pid, min(ts) AS first_ts FROM ev GROUP BY pid),
flags AS (
  SELECT ev.pid AS pid,
    countIf(ev.ts < per.first_ts + INTERVAL 7 DAY AND (ev.event = 'tab_switched' OR (ev.event = '$screen' AND ev.scr = 'mainPage'))) > 0 AS reached_main_w1,
    countIf(ev.ts < per.first_ts + INTERVAL 7 DAY AND ev.event = 'tab_switched') > 0 AS switched_w1,
    countIf(ev.ts < per.first_ts + INTERVAL 7 DAY AND ev.event = 'tab_switched' AND ev.tab = 'character') > 0 AS char_w1,
    countIf(ev.ts >= per.first_ts + INTERVAL 7 DAY AND ev.ts < per.first_ts + INTERVAL 14 DAY) > 0 AS ret_w2
  FROM ev INNER JOIN per ON ev.pid = per.pid
  WHERE per.first_ts >= now() - INTERVAL 90 DAY AND per.first_ts < now() - INTERVAL 14 DAY
    AND ev.ts < per.first_ts + INTERVAL 14 DAY
  GROUP BY ev.pid
)
SELECT multiIf(char_w1, '1_opened_character_w1', switched_w1, '2_switched_tabs_but_not_character_w1', '3_reached_main_no_tab_switch_w1') AS grp,
  count() AS users, countIf(ret_w2) AS returned_w2, round(countIf(ret_w2) / count(), 3) AS w2_rate
FROM flags WHERE reached_main_w1
GROUP BY grp ORDER BY grp
```
