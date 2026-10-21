# Main tab usage (tabs, elements, first action, viewer mix, scroll) - raw PostHog extract

- **Date**: 2026-10-14 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: last 30 days (2026-09-14 -> 2026-10-14 ~17:00 UTC), 90 days only where noted. All times UTC.
- **Question**: how do people actually use the Main tab (input for the Main screen redesign)?
- **Population filter (every query)**: `$lib = 'posthog-flutter'`, `$is_testflight != true`, `$is_emulator != true`, `$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')`, and persons with >= 10 distinct `$app_version` in 180 days excluded (internal testers; 7 such persons were active in the last 30 days). Same filter family as the 2026-10-07 and 2026-10-13 extracts.
- **Main viewers (base n)**: **45 persons** with `habit_tracker_viewed` `surface = 'card'` in 30d (229 Main visits in 106 sessions). This event fires once per Main tab visit, on load, so it is the best "Main viewed" proxy available. Cross-check: 49 persons opened the `mainPage` route (`$screen`) in 30d, 251 persons sent any client event (most of those never get past welcome/auth).
- **Suppression**: cells under 5 persons are shown as `<5`. See caveat 1 on why the floor is 5, not 25.

## Podsumowanie (PL)

1. Main ogląda 45 osób w 30 dniach (229 wejść, 106 sesji); 32 z nich to konta w pierwszym tygodniu, 36 to Android, 30 ma premium (głównie 4-dniowy trial).
2. Main jest punktem startu, nie celem: w pasku zakładek to tylko 14% przełączeń (Reflect 28%, Timeline 27%, Workspace 21%, Character 10%).
3. Z Main ludzie idą najczęściej do Timeline (44% wyjść), potem Reflect (26%), Workspace (22%), Character (8%); na Main wracają głównie z Timeline (81 przejść, 33 osoby).
4. 24% sesji (31 z 130) kończy się bez żadnego przełączenia zakładki, czyli wizyta zaczyna się i kończy na Main.
5. Pierwsza znacząca akcja w sesji: flow terapii (prep, debrief, między sesjami, check-in) 26%, Reflect tekstowy 18%, nawyki 7%, rozmowa głosowa 7%, karta lub CTA na Main 5%, notatka głosowa 3%; 35% sesji nie ma żadnej akcji.
6. Najmocniejszy element Main to karta następnej sesji / FAB: debrief startuje z Main 28 razy, między sesjami 14, prep 5, ale nie da się rozdzielić karty od FAB (brak entry_point).
7. Karta Getting Started wyświetla się 48 osobom (244 razy), a jej tap nie istnieje w danych: `getting_started_card_tapped` nigdy nie wystrzelił, opcje kliknęły <5 osób.
8. Nawyki: 12 z 45 widzów (27%) odhaczyło lub dodało nawyk; pasek trialu kliknęły <5 z 13 osób, które go widziały.
9. Niemierzone na Main: awatar (szuflada), przycisk info, Mood trend, Weekly observations, afirmacja, karta relacji terapeutycznej, "Schedule" na karcie sesji, widok karty sesji; nowe karty pierwszego tygodnia i FAB mają <5 osób (wydane 12.10).
10. Scrolla nie ma w PostHog wcale (brak eventu, brak widoczności kart), więc głębokości przewijania Main nie da się zmierzyć; termin sesji terapii też nie jest w PostHog (pytanie do database-administrator).

## Event verification

30d / 90d with the population filter. `last_seen` from HogQL `max(timestamp)`.

| event | flowing? | 30d events / persons | 90d events / persons | first seen (90d) | last seen | role on Main |
|---|---|---|---|---|---|---|
| `habit_tracker_viewed` | yes | 511 / 51 (all surfaces, before tester exclusion) | same (first 2026-09-15) | 2026-09-15 | 2026-10-14 15:49 | Main visit proxy (`surface=card`) |
| `tab_switched` | yes | 966 / 40 (filtered) | 3394 / up to 102 per tab | 2026-07-16 | 2026-10-14 15:49 | bottom nav |
| `first_capture_prompt_shown` | yes | 474 / 54 | 966 / 96 | 2026-08-11 | 2026-10-14 15:49 | Getting Started card shown (`entry_point=home_empty_state`) |
| `first_capture_prompt_option_tapped` | yes, thin | 5 / <5 | 5 / <5 | 2026-10-03 | 2026-10-06 | Getting Started option tap |
| `first_capture_prompt_dismissed` | yes | 7 / 7 | 25 / 21 | 2026-08-17 | 2026-10-06 | Getting Started dismiss |
| `getting_started_card_tapped` | **NO, never fired** (absent from event definitions and from 200d of events; defined in `analytics_events.dart`) | 0 | 0 | n/a | n/a | Getting Started card tap |
| `prep_card_opened` | yes, thin | 8 / <5 | 8 / <5 | 2026-10-12 | 2026-10-14 | only `source=timeline` seen; **`source=main_next_session` never seen** |
| `debrief_started`, `between_session_started`, `prep_card_started`, `health_check_started` | yes | see Q2 | 155/53, 174/40, n/a, 86/45 | 2026-07 | 2026-10-14 | next-session card buttons and FAB (no entry_point) |
| `trial_bar_viewed` / `trial_bar_tapped` | yes, new | 32 / 13 ; 5 / <5 | same | 2026-10-04 | 2026-10-14 / 10-11 | trial bar |
| `today_card_viewed` / `_tapped`, `first_week_plan_toggled`, `side_card_tapped` | yes, new, thin | 8 / <5 ; 2 / <5 ; 24 / <5 ; 1 / <5 | same | 2026-10-12 | 2026-10-14 | first-week Home cards |
| `fab_menu_opened` / `fab_flow_selected` | yes, new, thin | 11 / <5 ; 4 / <5 | same | 2026-10-12 / 10-13 | 2026-10-14 | FAB |
| `habit_check_toggled` / `habit_created` | yes | 84 / 10 ; 13 / 12 (before tester exclusion) | same | 2026-09-15 | 2026-10-14 | habits card |
| any scroll event (`$scroll`, `*scroll*`) | **NO** | 0 | 0 | n/a | n/a | n/a |
| `$autocapture` from Flutter | **NO** (only `web`, i.e. the website) | 0 | 0 | n/a | n/a | n/a |

## Results

### Q1. Tab views and transitions

Tab names in code (`MainNavCubit._tabNames`): `main`, `therapy` (= Timeline), `reflect`, `workspace`, `character`. `stats` = old builds only. There is no per-tab `$screen`: every tab sits inside `$screen_name = mainPage`. The app opens on Main (index 0), so Main views are not in `tab_switched` except when people come back to Main.

**1a. `tab_switched` by destination tab**

| tab (destination) | 30d switches | share | 30d persons | 90d switches | 90d persons |
|---|---|---|---|---|---|
| reflect | 271 | 28% | 40 | 937 | 100 |
| therapy (Timeline) | 259 | 27% | 42 | 896 | 102 |
| workspace | 206 | 21% | 37 | 672 | 84 |
| main (return to Main) | 132 | 14% | 34 | 436 | 75 |
| character | 93 | 10% | 31 | 384 | 77 |
| stats (old builds) | 5 | 0.5% | <5 | 69 | 11 |

Per-tab view events, 30d (same filter): `timeline_viewed` 297 / 54 persons, `habit_tracker_viewed` card (Main) 229 / 45, `workspace_opened` 190 / 37, `character_card_viewed` 105 / 36. Reflect has no tab-view event.

**1b. Where people go from Main (30d)**

"From Main" = previous `tab_switched` in the same session was `main`, plus the first switch of a session (the app starts on Main, see caveat 4).

| next tab | after an explicit return to Main: switches / persons | as first switch of a session: sessions / persons | combined switches | share of combined exits |
|---|---|---|---|---|
| therapy (Timeline) | 53 / 23 | 40 / 25 | 93 | 44% |
| workspace | 27 / 18 | 19 / 14 | 46 | 22% |
| reflect | 23 / 18 | 32 / 19 | 55 | 26% |
| character | 10 / 9 | 7 / 7 | 17 | 8% |
| stats | 1 / <5 | 0 | 1 | <1% |

Shares are on combined switches (93+55+46+17+1 = 212). Restricted to explicit returns to Main only (114 switches): Timeline 46%, Workspace 24%, Reflect 20%, Character 9%. Both orders put Timeline first.

**1c. Sessions with no tab switch at all**: 31 of 130 app sessions (24%), 23 persons. The visit starts and ends on Main (or on a pushed flow).

**1d. How people arrive back on Main (30d)**

| from | switches to main | persons |
|---|---|---|
| therapy (Timeline) | 81 | 33 |
| workspace | 19 | 14 |
| character | 16 | 14 |
| reflect | 14 | 10 |

Main visits per person (30d, n=45): 1 visit 12 persons, 2-3 visits 14, 4-7 visits 12, 8+ visits 7 (those 7 persons make 112 of 229 visits, 49%).

### Q2. Interactive elements on Main

Base: 45 Main viewers, 229 Main visits, 30d. "On Main" = event fired while the last `tab_switched` in the session was `main`, or before any switch (app starts on Main). The two columns are kept separate because the second also catches pushed routes (caveat 4). Persons rate = persons / 45 Main viewers.

Card order on the normal Home (`mainTabDefaultWidgetOrder`): hero greeting (avatar, info), trial bar, [Getting Started card for new users], next-session card, habits, mood trend, therapy-relationship prompt (only when a check-in is pending), weekly observations, daily affirmation, usage-resets line. First-week Home replaces the cards with today card, plan card, side card. FAB and bottom nav sit on top.

| element | event | events on Main (last tab = main / before any switch) | persons (per column) | persons rate vs 45 viewers | note |
|---|---|---|---|---|---|
| Hero avatar (opens drawer) | **none** | n/a | n/a | n/a | GAP |
| Hero info button (section sheet) | **none** | n/a | n/a | n/a | GAP |
| Trial bar | `trial_bar_viewed` / `trial_bar_tapped` | taps 3 / 2 | <5 / <5 | tap <5 of 13 who saw it | 32 views, 13 persons, 30d |
| Getting Started card, shown | `first_capture_prompt_shown` `entry_point=home_empty_state` | 244 shown | 48 | n/a | also fires on Timeline empty state (56 / 27) and post-onboarding (22 / 22) |
| Getting Started card, tap | `getting_started_card_tapped` | **0, never fired** | 0 | 0% | defined but dead |
| Getting Started option tap | `first_capture_prompt_option_tapped` | 0 / 1 | <5 | <5 | 5 events, <5 persons across all entry points |
| Getting Started dismiss | `first_capture_prompt_dismissed` | 0 / 7 | 7 | 16% | |
| Next-session card, view / state | **none** | n/a | n/a | n/a | GAP: no event says which of the 4 states (schedule, prepare, debrief, between) was shown |
| Next-session "Schedule" (SessionSetupScreen) | **none** (`session_sheet_completed` 2 events, <5 persons, completion only) | n/a | n/a | n/a | GAP |
| Next-session "Debrief" (or FAB) | `debrief_started` | 15 / 13 | 11 / 10 | about 47% max (21 of 45, upper bound) | card and FAB not separable |
| Next-session "Between sessions" (or FAB) | `between_session_started` | 6 / 8 | 5 / 6 | upper bound 11 | same |
| Next-session "Prepare" (or FAB) | `prep_card_started` | 2 / 3 | <5 / <5 | <5 | same |
| Next-session "View prep card" | `prep_card_opened` `source=main_next_session` | 0 | 0 | 0% | never seen; the 8 opens are all from Timeline, <5 persons |
| Therapy-relationship prompt / check-in (or FAB, or Workspace) | `health_check_started` | 4 / 7 | <5 / 6 | n/a | no card view event; 5 more starts from Workspace |
| Habits card, view | `habit_tracker_viewed` `surface=card` | 229 | 45 | 100% (definition) | fires on load, not on visibility |
| Habits card, check-in | `habit_check_toggled` | 1 / 9 | <5 / <5 | <5 | |
| Habits card, add habit | `habit_created` | 3 / 9 | <5 / 8 | about 24% max | |
| Habits card, any (check or add) | both | n/a | 12 | 27% | person level, any surface |
| Habits limit | `habit_limit_reached` | 0 / 1 | <5 | <5 | |
| Mood trend card | **none** | n/a | n/a | n/a | GAP |
| Weekly observations card | **none** | n/a | n/a | n/a | GAP |
| Daily affirmation card | **none** | n/a | n/a | n/a | GAP |
| Usage-resets line | **none** | n/a | n/a | n/a | GAP (text only) |
| First-week today card | `today_card_viewed` / `today_card_tapped` / `today_card_deferred` | taps 0 / 2 | <5 | <5 | shipped 2026-10-12 (2.0.109+), too new |
| First-week plan card | `first_week_plan_toggled` / `_hidden` | 21 / 3 | <5 | <5 | 21 toggles by a single person |
| First-week side card | `side_card_tapped` / `_dismissed` | 0 / 1 | <5 | <5 | most volume was TestFlight (excluded) |
| FAB menu | `fab_menu_opened` / `fab_flow_selected` | open 2 / 1, flow 2 / 0 | <5 | <5 | shipped 2026-10-12 |
| Bottom nav | `tab_switched` | see Q1 | | | |

Person-level any-activity rates among the 45 Main viewers (30d, any surface): habit check or add 12 (27%), any therapy capture flow start 22 (49%), trial bar tap <5, Getting Started option tap <5, first-week card tap <5.

**Gap list (no event at all)**: hero avatar/drawer open, hero info button, next-session card impression and its state, next-session "Schedule", mood trend card (view and tap), weekly observations card, daily affirmation card, therapy-relationship prompt card impression, usage-resets line, scroll/visibility of any card. **Broken/dead**: `getting_started_card_tapped` (never fired), `prep_card_opened source=main_next_session` (never seen). **Not attributable**: `debrief_started`, `between_session_started`, `prep_card_started`, `health_check_started` carry no `entry_point`, so next-session card vs FAB vs Timeline cannot be told apart. Owner for all: `flutter-mobile`.

### Q3. First meaningful action after app open (30d)

No app-open event exists (the Flutter SDK sends no lifecycle events), so "app open" = a PostHog session (`$session_id`) that contains a Main visit, a `mainPage` screen or a tab switch: **130 sessions, 50 persons**. First meaningful action = earliest event of the groups below; FAB opens, dismisses, plan toggles and limit events do not count.

| first meaningful action in the session | sessions | share | persons |
|---|---|---|---|
| therapy capture flow (prep, debrief, between, check-in) | 34 | 26% | 19 |
| nothing: only switched tabs | 29 | 22% | 19 |
| reflect, text (new thread, open thread, message) | 23 | 18% | 10 |
| nothing: opened and left | 16 | 12% | 13 |
| habit check-in or add | 9 | 7% | 6 |
| voice conversation (`voice_chat_started`, `first_conversation_started`) | 9 | 7% | 9 |
| opened a Main card or CTA (trial bar, today/side card, Getting Started option, prep card) | 6 | 5% | 5 |
| voice note or session recording (`recording_started`, `quick_capture_started`) | 4 | 3% | <5 |
| **total "nothing"** | **45** | **35%** | |

Person level (first session in window that had a Main visit or tab switch, n=50): nothing 14, therapy capture 14, reflect text 9, voice conversation 9, Main card/CTA <5, voice note <5.

Time from session start to first meaningful action (83 sessions with an action): under 30 s 31 sessions (17 persons), 30 s to 2 min 16 (12), 2 to 10 min 33 (25), 10 min+ 3 (<5).

### Q4. Who views Main (45 persons, 30d)

| dimension | segment | persons | share |
|---|---|---|---|
| platform (latest `$os`) | Android | 36 | 80% |
| | iOS | 9 | 20% |
| plan (latest `is_premium` on `habit_tracker_viewed`) | premium (incl. sign-up trial) | 30 | 67% |
| | free | 15 | 33% |
| account age at first Main visit in window (since first PostHog event) | first week (<7 d) | 32 | 71% |
| | 7-29 d | 5 | 11% |
| | 30 d+ | 8 | 18% |
| first-week Home mode (`today_card_viewed` in 30d) | yes | <5 | |
| | no | 41+ | |
| therapy capture history (lifetime client events) | prep + debrief | 10 | 22% |
| | debrief only | 8 | 18% |
| | between-session only | <5 | |
| | prep only | <5 | |
| | none | 21 | 47% |
| therapy session scheduled | **not in PostHog** | n/a | n/a |

Cross-cuts: of the 32 first-week persons, 27 are premium (sign-up trial) and 5 free. Visit level: first-week accounts make 152 of 229 Main visits (66%, 32 persons), 7-29 d 38 visits (8 persons), 30 d+ 39 visits (10 persons) (a person can fall in two buckets over 30 days). Visits by plan and platform: premium Android 127 (29 persons), premium iOS 48 (5), free Android 47 (11), free iOS 7 (5).

Not derivable from PostHog: whether a therapy session is scheduled (no event or person property carries it; only `session_sheet_completed`, <5 persons) and whether a prep card for the next session exists. Truth lives in Postgres (sessions/prep tables) -> `database-administrator`.

### Q5. Scroll depth on Main

**Not measurable.** No scroll event of any kind exists in the project (no `$scroll`, nothing matching `*scroll*`), the Flutter SDK sends no `$autocapture` (all 461 autocapture events in 90 d are `web`), and no Main card has a visibility/impression event (`habit_tracker_viewed` fires on data load, `trial_bar_viewed` and `first_capture_prompt_shown` on render, regardless of whether the card is on screen). Session replay is mask-all and is not a source for this extract. Proposal for `flutter-mobile`: a single `main_tab_scrolled` (max depth bucket 25/50/75/100 per visit) or per-card `main_card_viewed` with `card_id` and `position` fired on first 50% visibility.

## Caveats

1. **Suppression floor**: cells under 5 persons are shown `<5`, matching the earlier raw extracts (2026-10-07, 2026-10-13). The agent spec says 25; at 25 nearly every row here would be suppressed because the whole Main population is 45 persons. No health content, scores or free text is reported, only behaviour counts. Operator to confirm if 25 must apply.
2. **Small n**: 45 Main viewers in 30 d. Every share is directional. 90 d does not help for Main-specific events: the Main visit proxy only exists since 2026-09-15 and most card events since 2026-10-04 or 2026-10-12.
3. **Main visit proxy**: `habit_tracker_viewed surface=card` fires once per Main tab visit when habits load. A failed habits load or the first-week body may skip it, so 45 is a floor (49 persons opened `mainPage`).
4. **Tab context is inferred**: an action counts "on Main" if the last `tab_switched` in the same `$session_id` was `main`, or there was none yet. A PostHog session can start while the app is already on another tab (after 30 min idle in background) or inside a pushed route (e.g. 213 `reflect_message_submitted` before any switch are almost certainly the first-conversation/Reflect route, not the Main tab). The "before any switch" column is therefore an upper bound.
5. **Card vs FAB**: next-session card buttons and FAB flows launch the same routes and fire the same `*_started` events with no entry point; FAB events only exist since 2026-10-12.
6. **Premium = trial mostly**: `is_premium` is true during the 4-day sign-up trial, so "premium" here is not paying.
7. **Account age** uses the first PostHog event of the person (ingest started 2026-04-22; older accounts look younger than they are, which only affects the 30 d+ bucket).
8. **Mixed builds**: Main viewers span 2.0.97 to 2.0.111 in 30 d; first-week cards and FAB events only exist on 2.0.109+.
9. Platform split is client-side `$os`; backend events were not used.

## Queries

Macro `F` (pasted into every `WHERE`):

```sql
properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
AND coalesce(properties.$device_model,'') NOT IN ('OnePlus8Pro','Pixel 6 Pro')
AND person_id NOT IN (SELECT person_id FROM events WHERE timestamp > now() - INTERVAL 180 DAY
  AND properties.$lib = 'posthog-flutter' GROUP BY person_id HAVING uniq(properties.$app_version) >= 10)
```

Macro `ACT` (meaningful-action events):

```sql
'reflect_new_thread_tapped','reflect_thread_opened','reflect_message_submitted','voice_chat_started','first_conversation_started',
'recording_started','quick_capture_started','prep_card_started','debrief_started','between_session_started','health_check_started',
'habit_check_toggled','habit_created','prep_card_opened','today_card_tapped','today_card_deferred','side_card_tapped','side_card_dismissed',
'getting_started_card_tapped','trial_bar_tapped','first_capture_prompt_option_tapped','first_capture_prompt_dismissed',
'first_week_plan_toggled','first_week_plan_hidden','fab_menu_opened','fab_flow_selected','habit_limit_reached','usage_chip_tapped_at_zero'
```

`EXCL` (not counted as a first meaningful action): `'fab_menu_opened','first_capture_prompt_dismissed','first_week_plan_toggled','today_card_deferred','side_card_dismissed','first_week_plan_hidden','habit_limit_reached','usage_chip_tapped_at_zero','fab_flow_selected'`.

`CAT` = `multiIf(event IN (reflect events),'reflect (text)', event IN ('voice_chat_started','first_conversation_started'),'voice conversation', event IN ('recording_started','quick_capture_started'),'voice note / session recording', event IN ('prep_card_started','debrief_started','between_session_started','health_check_started'),'therapy capture flow', event IN ('habit_check_toggled','habit_created'),'habit check-in', event IN ('prep_card_opened','today_card_tapped','side_card_tapped','getting_started_card_tapped','trial_bar_tapped','first_capture_prompt_option_tapped'),'opened a Main card / CTA','other')`

```sql
-- @@ main_viewers
SELECT uniqIf(person_id, event='$screen' AND properties.$screen_name='mainPage' AND timestamp > now() - INTERVAL 30 DAY) AS p_mainpage_30,
 uniqIf(person_id, event='habit_tracker_viewed' AND properties.surface='card' AND timestamp > now() - INTERVAL 30 DAY) AS p_maincard_30,
 countIf(event='habit_tracker_viewed' AND properties.surface='card' AND timestamp > now() - INTERVAL 30 DAY) AS main_visits_30,
 uniqIf($session_id, event='habit_tracker_viewed' AND properties.surface='card' AND timestamp > now() - INTERVAL 30 DAY) AS sessions_with_main_30,
 uniqIf(person_id, timestamp > now() - INTERVAL 30 DAY) AS p_any_client_30
FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND F

-- @@ tab_dist
SELECT properties.tab_name AS tab, countIf(timestamp > now() - INTERVAL 30 DAY) AS ev30, uniqIf(person_id, timestamp > now() - INTERVAL 30 DAY) AS p30,
 count() AS ev90, uniq(person_id) AS p90
FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND event='tab_switched' AND F GROUP BY tab ORDER BY ev30 DESC LIMIT 20

-- @@ transitions_30d
SELECT prev_tab, tab, count() AS ev, uniq(pid) AS p FROM (
 SELECT person_id AS pid, toString(properties.tab_name) AS tab,
  ifNull(lagInFrame(toNullable(toString(properties.tab_name)), 1) OVER (PARTITION BY person_id, properties.$session_id ORDER BY timestamp ASC
    ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING), '(session start)') AS prev_tab
 FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND event='tab_switched' AND F
) GROUP BY prev_tab, tab ORDER BY ev DESC LIMIT 40

-- @@ sessions_first_switch_30d
SELECT first_tab, count() AS sessions, uniq(pid) AS p FROM (
 SELECT $session_id AS sid, any(person_id) AS pid,
  ifNull(argMinIf(toString(properties.tab_name), timestamp, event='tab_switched'), '') AS ft,
  countIf(event='tab_switched') AS n_sw, if(n_sw = 0, '(no tab switch in session)', ft) AS first_tab
 FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND $session_id != '' AND F
 GROUP BY sid HAVING countIf(event='habit_tracker_viewed' AND properties.surface='card') > 0 OR countIf(event='tab_switched') > 0
   OR countIf(event='$screen' AND properties.$screen_name='mainPage') > 0
) GROUP BY first_tab ORDER BY sessions DESC LIMIT 20

-- @@ actions_by_current_tab_30d
SELECT event, cur_tab, count() AS ev, uniq(pid) AS p FROM (
 SELECT person_id AS pid, event, timestamp,
  ifNull(anyLast(if(event='tab_switched', toNullable(toString(properties.tab_name)), NULL)) OVER (PARTITION BY person_id, $session_id
    ORDER BY timestamp ASC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW), 'main (no switch yet)') AS cur_tab
 FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND (event='tab_switched' OR event IN (ACT)) AND F
) WHERE event != 'tab_switched' GROUP BY event, cur_tab ORDER BY event, ev DESC LIMIT 200

-- @@ element_props_30d
SELECT event, coalesce(toString(properties.entry_point), toString(properties.source), toString(properties.surface),
  toString(properties.tab_name), toString(properties.plan_active), '') AS dim, count() AS ev, uniq(person_id) AS p
FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND F AND event IN ('first_capture_prompt_shown','prep_card_opened','habit_tracker_viewed',
  'fab_flow_selected','today_card_viewed','reflect_new_thread_tapped','voice_chat_started','first_conversation_started','trial_bar_viewed','usage_chip_tapped_at_zero')
GROUP BY event, dim ORDER BY event, ev DESC LIMIT 100

-- @@ first_action_per_session_30d
SELECT first_cat, count() AS sessions, uniq(pid) AS p FROM (
 SELECT $session_id AS sid, any(person_id) AS pid,
  countIf(event IN (ACT) AND event NOT IN (EXCL)) AS n_act,
  argMinIf(CAT, timestamp, event IN (ACT) AND event NOT IN (EXCL)) AS c1,
  countIf(event='tab_switched') AS n_sw,
  if(n_act > 0, c1, if(n_sw > 0, 'nothing: only switched tabs', 'nothing: opened and left')) AS first_cat
 FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND $session_id != '' AND F
 GROUP BY sid HAVING countIf(event='habit_tracker_viewed' AND properties.surface='card') > 0 OR countIf(event='tab_switched') > 0
   OR countIf(event='$screen' AND properties.$screen_name='mainPage') > 0
) GROUP BY first_cat ORDER BY sessions DESC LIMIT 20

-- @@ time_to_first_action_sessions_30d
SELECT multiIf(secs < 30,'<30s', secs < 120,'30s-2min', secs < 600,'2-10min','10min+') AS b, count() AS sessions, uniq(pid) AS p FROM (
 SELECT $session_id AS sid, any(person_id) AS pid,
  dateDiff('second', min(timestamp), minIf(timestamp, event IN (ACT) AND event NOT IN (EXCL))) AS secs, countIf(event IN (ACT)) AS n
 FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND $session_id != '' AND F
 GROUP BY sid HAVING n > 0 AND (countIf(event='habit_tracker_viewed' AND properties.surface='card') > 0 OR countIf(event='tab_switched') > 0)
) WHERE secs >= 0 GROUP BY b ORDER BY b LIMIT 10

-- @@ viewer_state
SELECT os, premium, age_bucket, first_week_mode, therapy_capture_hist, count() AS persons FROM (
 SELECT v.pid AS pid, v.os AS os, if(v.prem, 'premium', 'free') AS premium,
  multiIf(dateDiff('day', l.first_seen, v.first_visit) < 7, 'first week (<7d)', dateDiff('day', l.first_seen, v.first_visit) < 30, '7-29d', '30d+') AS age_bucket,
  if(l.fw > 0, 'yes', 'no') AS first_week_mode,
  multiIf(l.prep > 0 AND l.deb > 0, 'prep + debrief', l.prep > 0, 'prep only', l.deb > 0, 'debrief only', l.btw > 0, 'between only', 'none') AS therapy_capture_hist
 FROM (SELECT person_id AS pid, argMax(toString(properties.$os), timestamp) AS os, argMax(properties.is_premium, timestamp) = true AS prem,
         min(timestamp) AS first_visit
       FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND event='habit_tracker_viewed' AND properties.surface='card' AND F GROUP BY person_id) AS v
 LEFT JOIN (SELECT person_id AS pid, min(timestamp) AS first_seen, countIf(event='today_card_viewed' AND timestamp > now() - INTERVAL 30 DAY) AS fw,
         countIf(event='prep_card_started') AS prep, countIf(event='debrief_started') AS deb, countIf(event='between_session_started') AS btw
       FROM events WHERE timestamp > now() - INTERVAL 200 DAY GROUP BY person_id) AS l ON v.pid = l.pid
) GROUP BY os, premium, age_bucket, first_week_mode, therapy_capture_hist ORDER BY persons DESC LIMIT 100

-- @@ visits_by_premium
SELECT if(properties.is_premium = true,'premium','free') AS prem, toString(properties.$os) AS os, count() AS visits, uniq(person_id) AS p
FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND event='habit_tracker_viewed' AND properties.surface='card' AND F
GROUP BY prem, os ORDER BY visits DESC LIMIT 10

-- @@ main_actor_rate_30d
SELECT count() AS main_viewers, countIf(n_habit > 0) AS p_habit, countIf(n_flow > 0) AS p_therapy_flow_any,
 countIf(n_trial > 0) AS p_trial_bar_tap, countIf(n_cap > 0) AS p_getting_started_option, countIf(n_fw > 0) AS p_first_week_card_tap
FROM (SELECT person_id, countIf(event IN ('habit_check_toggled','habit_created')) AS n_habit,
  countIf(event IN ('prep_card_started','debrief_started','between_session_started','health_check_started')) AS n_flow,
  countIf(event='trial_bar_tapped') AS n_trial, countIf(event='first_capture_prompt_option_tapped') AS n_cap,
  countIf(event IN ('today_card_tapped','side_card_tapped')) AS n_fw,
  countIf(event='habit_tracker_viewed' AND properties.surface='card') AS n_view
 FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND F GROUP BY person_id HAVING n_view > 0)

-- @@ zero_check_lifetime
SELECT event, count() AS ev, uniq(person_id) AS p, max(timestamp) AS last_ts FROM events
WHERE timestamp > now() - INTERVAL 200 DAY AND event IN ('getting_started_card_tapped','prep_card_opened','$scroll','$autocapture', ...)
GROUP BY event ORDER BY ev DESC LIMIT 30
```
