# Engagement / Funnel / Retention / Monetization – 14d pull, raw PostHog extract

- **Date**: 2026-08-10 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: last14d = `now()-INTERVAL 14 DAY` → now (~2026-07-27 → 2026-08-10 UTC); prev14d = `now()-INTERVAL 28 DAY` → `now()-INTERVAL 14 DAY` (~2026-07-13 → 2026-07-27 UTC)
- **Question**: Full engagement/funnel/retention/monetization picture for the last 14d vs the preceding 14d.
- **Event verification**: full inventory pulled directly from `events` table for both windows (see Queries) — this doubles as flow verification: every event listed below has rows in the stated window; anything not listed had zero rows.

## Results

### 1–2. Full event inventory, last14d vs prev14d (person_id-based users)

Sorted by last14d count desc. `∅` = zero in that window. New/regressed events are called out below the table.

| event | c (last14d) | users (last14d) | c (prev14d) | users (prev14d) |
|---|---|---|---|---|
| api_error | 4507 | 60 | 1319 | 38 |
| reflect_limit_hit | 1870 | 1 (single-user skew) | ∅ | ∅ |
| $screen | 1838 | 89 | 2254 | 79 |
| tab_switched | 1689 | 35 | 1886 | 20 |
| timeline_viewed | 510 | 46 | 621 | 25 |
| reflect_message_sent | 432 | 15 | 54 | 6 |
| onboarding_step_viewed | 273 | 33 | 90 | 12 |
| onboarding_step_completed | 252 | 33 | 85 | 11 |
| therapy_context_updated | 226 | 33 | 91 | 13 |
| character_card_viewed | 162 | 33 | 198 | 15 |
| workspace_opened | 124 | 16 | ∅ | ∅ (new) |
| $set | 114 | 32 | 161 | 22 |
| timeline_filter_changed | 77 | 14 | 203 | 7 |
| profile_updated | 75 | 37 | 28 | 10 |
| app_tour_step_viewed | 72 | 12 | ∅ | ∅ (new) |
| moment.opened | 71 | 26 | 36 | 8 |
| notification_permission_prompted | 55 | 20 | ∅ | ∅ (new) |
| $identify | 51 | 38 | 63 | 19 |
| $pageview | 49 | 26 | 231 | 173 |
| $web_vitals | 44 | 22 | 149 | 69 |
| notification_permission_granted | 44 | 14 | ∅ | ∅ (new) |
| recording_saved | 42 | 14 | 35 | 3 |
| symptom_scored | 39 | 4 (small-n) | 31 | 6 |
| user_registered | 36 | 35 | 17 | 16 |
| between_session_started | 35 | 11 | 38 | 9 |
| recording_started | 34 | 10 | 46 | 3 |
| $rageclick | 33 | 5 | 74 | 2 |
| consent_granted | 33 | 18 | ∅ | ∅ (new) |
| onboarding_started | 33 | 33 | 14 | 12 |
| onboarding_legal_gate_gate_ready | 33 | 33 | 11 | 10 |
| debrief_started | 32 | 17 | 43 | 9 |
| welcome_cta_tapped | 32 | 19 | ∅ | ∅ (new) |
| $pageleave | 30 | 20 | 177 | 90 |
| recording_stopped | 28 | 10 | 43 | 3 |
| between_session_created | 27 | 8 | 23 | 8 |
| onboarding_completed | 27 | 27 | 10 | 9 |
| reflect_thread_opened | 26 | 9 | ∅ | ∅ (new) |
| account_screen_opened | 26 | 7 | ∅ | ∅ (new) |
| onboarding_lead_source_selected | 26 | 26 | 8 | 8 |
| subscription_screen_opened | 25 | 11 | 12 | 5 |
| moment.acted | 25 | 14 | 17 | 3 |
| health_check_started | 25 | 15 | 34 | 8 |
| reflect_session_started | 24 | 16 | 15 | 9 |
| user_logged_in | 22 | 8 | 55 | 10 |
| notification_opened | 22 | 9 | 18 | 4 |
| app_tour_started | 18 | 12 | ∅ | ∅ (new) |
| client_error | 17 | 6 | 38 | 6 |
| health_check_question_answered | 17 | 3 (small-n) | ∅ | ∅ (new) |
| signup_method_selected | 16 | 14 | ∅ | ∅ (new) |
| signup_started | 16 | 14 | ∅ | ∅ (new) |
| health_check_completed | 16 | 12 | 21 | 7 |
| consent_screen_viewed | 15 | 15 | ∅ | ∅ (new) |
| conversation_message_sent | 14 | 1 (single-user skew) | ∅ | ∅ (new) |
| notification_received | 12 | 5 | 8 | 3 |
| bio_refreshed | 12 | 3 (small-n) | 6 | 3 |
| realization_viewed | 11 | 4 (small-n) | 19 | 4 |
| $autocapture | 11 | 6 | 368 | 35 |
| notification_permission_denied | 11 | 6 | ∅ | ∅ (new) |
| onboarding_step_back | 10 | 2 (small-n) | ∅ | ∅ (new) |
| quick_capture_abandoned | 10 | 5 | ∅ | ∅ (new) |
| orca_color_changed | 9 | 4 (small-n) | 8 | 3 |
| prep_card_started | 9 | 6 | 34 | 8 |
| health_check_abandoned | 9 | 4 (small-n) | ∅ | ∅ (new) |
| app_tour_completed | 8 | 8 | ∅ | ∅ (new) |
| voice_transcription_completed | 8 | 3 (small-n) | ∅ | ∅ (new) |
| voice_transcription_started | 8 | 3 (small-n) | ∅ | ∅ (new) |
| inapp_insight.shown | 8 | 5 | 3 | 2 |
| debrief_created | 7 | 7 | 14 | 4 |
| recording_chunked_upload_completed | 7 | 3 (small-n) | 14 | 4 |
| user_logged_out | 6 | 4 (small-n) | 5 | 2 |
| language_changed | 6 | 5 | 5 | 3 |
| content_shared | 6 | 3 (small-n) | 7 | 4 |
| timeline_item_deleted | 6 | 3 (small-n) | 12 | 4 |
| quick_capture_submitted | 6 | 4 (small-n) | ∅ | ∅ (new) |
| conversation_started | 6 | 2 (small-n) | ∅ | ∅ (new) |
| symptom_created | 6 | 3 (small-n) | 4 | 3 |
| account_deletion_confirmed | 5 | 2 (small-n) | ∅ | ∅ (new) |
| subscription_product_selected | 5 | 4 (small-n) | 4 | 3 |
| account_deletion_started | 5 | 2 (small-n) | ∅ | ∅ (new) |
| prep_card_created | 5 | 4 (small-n) | 13 | 5 |
| app_tour_skipped | 5 | 2 (small-n) | ∅ | ∅ (new) |
| recording_recovered | 4 | 3 (small-n) | 34 | 2 |
| consent_revoked | 4 | 2 (small-n) | ∅ | ∅ (new) |
| prep_capture_submitted | 4 | 3 (small-n) | ∅ | ∅ (new) |
| voice_agent_changed | 4 | 2 (small-n) | 7 | 1 |
| inapp_insight.acted | 4 | 2 (small-n) | 1 | 1 |
| goal_created | 4 | 2 (small-n) | 5 | 2 |
| paywall_dismissed | 4 | 3 (small-n) | ∅ | ∅ (new) |
| notification_row_toggled | 4 | 1 (single-user skew) | ∅ | ∅ (new) |
| prep_capture_started | 4 | 3 (small-n) | ∅ | ∅ (new) |
| reflect_thread_deleted | 3 | 3 (small-n) | 9 | 3 |
| app_store_click | 3 | 1 (small-n) | 5 | 5 |
| recording_upload_started | 3 | 3 (small-n) | 5 | 2 |
| quick_capture_started | 3 | 2 (small-n) | ∅ | ∅ (new) |
| orca_named | 3 | 3 (small-n) | 2 | 2 |
| symptom_archived | 2 | 2 (small-n) | 6 | 2 |
| timeline_item_restored | 2 | 1 (small-n) | ∅ | ∅ |
| prep_capture_abandoned | 2 | 1 (small-n) | ∅ | ∅ (new) |
| therapy_schedule_updated | 2 | 1 (small-n) | 35 | 3 |
| password_reset_failed | 2 | 1 (small-n) | ∅ | ∅ (new) |
| reflect_session_ended | 2 | 2 (small-n) | ∅ | ∅ (new) |
| password_reset_requested | 2 | 1 (small-n) | ∅ | ∅ (new) |
| conversation_ended | 2 | 1 (small-n) | ∅ | ∅ (new) |
| subscription_purchase_started | 2 | 2 (small-n) | 1 | 1 |
| realization_dismissed | 1 | 1 (small-n) | 4 | 1 |
| debrief_failed | 1 | 1 (small-n) | 13 | 4 |
| realization_detected | 1 | 1 (small-n) | ∅ | ∅ (new) |
| account_deleted | 1 | 1 (small-n) | ∅ | ∅ (new) |
| signup_failed | 1 | 1 (small-n) | ∅ | ∅ (new) |
| voice_chat_ended | 1 | 1 (small-n) | 6 | 2 |
| subscription_purchase_failed | 1 | 1 (small-n) | 1 | 1 |
| voice_chat_started | 1 | 1 (small-n) | 6 | 2 |
| $push_notification_opened | 1 | 1 (small-n) | ∅ | ∅ (new) |
| timeline_generate_now | ∅ | ∅ | 20 | 4 |
| notification_interest_toggled | ∅ | ∅ | 13 | 2 |
| goal_status_changed | ∅ | ∅ | 9 | 2 |
| promo_code_applied | ∅ | ∅ | 3 | 2 |
| inapp_insight.generated | ∅ | ∅ | 3 | 3 |
| notification_banner_tapped | ∅ | ∅ | 2 | 1 |
| notification_master_toggled | ∅ | ∅ | 2 | 1 |
| inapp_insight.dismissed | ∅ | ∅ | 1 | 1 |

**Present in prev14d, ZERO in last14d (possible regression / renamed / removed):** `timeline_generate_now` (20/4), `notification_interest_toggled` (13/2, likely superseded by `notification_row_toggled`), `goal_status_changed` (9/2), `promo_code_applied` (3/2), `inapp_insight.generated` (3/3), `notification_banner_tapped` (2/1), `notification_master_toggled` (2/1), `inapp_insight.dismissed` (1/1).

**New in last14d (not in prev14d) — matches recently shipped work:** `workspace_opened` (MSV3.2 workspace), `app_tour_*` (4 events, new onboarding app tour), `notification_permission_prompted/granted/denied` (notification overhaul), `consent_granted/revoked`, `consent_screen_viewed` (GDPR consent flow), `welcome_cta_tapped`, `signup_method_selected/started/failed`, `account_screen_opened`, `account_deletion_started/confirmed`, `account_deleted`, `password_reset_requested/failed`, `health_check_question_answered/abandoned`, `quick_capture_started/submitted/abandoned`, `prep_capture_started/submitted/abandoned` (distinct from `prep_card_*`), `onboarding_step_back`, `notification_row_toggled`, `paywall_dismissed`, `reflect_session_ended`, `reflect_thread_opened`, `realization_detected`, `voice_transcription_started/completed` (voice notes v2/Whisper), `conversation_message_sent/started/ended` (legacy conversation events, 1–2 users, likely web/testing), `$push_notification_opened`.

### 3. Daily activity, last14d

| day | DAU (person_id) | events | new users |
|---|---|---|---|
| 2026-07-27 | 10 | 165 | 2 |
| 2026-07-28 | 9 | 45 | 4 |
| 2026-07-29 | 11 | 476 | 4 |
| 2026-07-30 | 18 | 961 | 10 |
| 2026-07-31 | 16 | 382 | 7 |
| 2026-08-01 | 11 | 123 | 7 |
| 2026-08-02 | 5 | 158 | 2 |
| 2026-08-03 | 15 | 846 | 9 |
| 2026-08-04 | 20 | 5517 | 9 |
| 2026-08-05 | 17 | 746 | 9 |
| 2026-08-06 | 9 | 458 | 6 |
| 2026-08-07 | 18 | 2261 | 7 |
| 2026-08-08 | 13 | 650 | 4 |
| 2026-08-09 | 16 | 525 | 8 |
| 2026-08-10 | 3 (partial day) | 366 | 2 |

Total events last14d = 13,679. Total new users last14d = 90 (matches retention cohort_size below exactly — cross-check passes). 2026-08-04 event spike (5517) driven almost entirely by the single-user `reflect_limit_hit` skew (1870 events from 1 person) plus a general `api_error` peak that day.

### 4. WAU per ISO week (`toStartOfWeek`, last 5 weeks) + stickiness

| week starting | WAU |
|---|---|
| 2026-08-09 (partial, 2 days of data) | 19 |
| 2026-08-02 | 67 |
| 2026-07-26 | 68 |
| 2026-07-19 | 155 |
| 2026-07-12 | 123 |
| 2026-07-05 (partial, window-clamped) | 113 |

Stickiness (avg DAU / WAU) for complete weeks:
- Week 2026-08-02: avg DAU 13.9 / WAU 67 = **20.7%**
- Week 2026-07-26: avg DAU 13.0 / WAU 68 = **19.1%**
- Week 2026-07-19: avg DAU 25.9 / WAU 155 = **16.7%**
- Week 2026-07-12: avg DAU 20.9 / WAU 123 = **17.0%**

### 5. Retention — cohort = people whose first-ever event fell in last14d

| cohort_size | returned any later calendar day (D1+) | active 7+ days after first seen |
|---|---|---|
| 90 | 17 (18.9%) | 2 (2.2%, small-n) |

Bounded to `timestamp > toDateTime('2026-04-22')` (ingest start) for the global first-seen computation, then filtered to people whose first event is in the last 14d — so the right tail (people who could still return 7+ days later, since 14 days is a short observation window for a 7-day-later behavior) is inherently truncated for the most recent ~7 days of the cohort. Read the 7+ day figure as a lower bound.

### 6. Onboarding funnel (windowFunnel, 86400s window) + step breakdown, last14d

Funnel (person-level, sequential): step viewed → step completed → onboarding_completed

| ≥1 (viewed) | ≥2 (completed a step) | ≥3 (onboarding_completed) | total people with any onboarding event |
|---|---|---|---|
| 33 | 33 | 27 | 33 |

Per-step breakdown (`step_index`/`step_name`, viewed vs completed):

| step_index | step_name | viewed (c/users) | completed (c/users) | avg duration (s) | median duration (s) |
|---|---|---|---|---|---|
| 0 | legal_gate | 33/33 | 33/33 | 18.5 | 10.0 |
| 1 | challenges | 39/33 | 37/31 | 27.3 | 18.0 |
| 2 | intensity | 39/31 | 33/31 | 15.3 | 11.0 |
| 3 | journey | 34/31 | 31/30 | 50.5 | 28.0 |
| 4 | modality | 33/30 | 31/29 | 21.9 | 11.0 |
| 5 | schedule | 32/29 | 30/29 | 17.1 | 10.0 |
| 6 | companion | 33/29 | 30/27 | 75.0 | 46.0 |
| 7 | lead_source | 30/27 | 27/27 | 10.3 | 7.0 |

Steps 0–7 = 8 named steps observed in data (spec calls for 9; only these 8 emit `step_name`/`step_index` in the window). `onboarding_completed` fires for 27/33 people who started (82%). Users lost between step 0 (33) and step 7 completion (27) = 6 people (18%), spread thinly across steps rather than one cliff; step "companion" has the longest median dwell time (46s).

### 7. Feature adoption, last14d (event → feature-category mapping) + breadth histogram

| feature | events | users |
|---|---|---|
| timeline | 595 | 46 |
| onboarding | 654 | 33 |
| character_orca | 174 | 33 |
| notifications | 148 | 24 (small-n) |
| debrief | 40 | 17 |
| reflect | 2362 | 17 (events dominated by the 1-user `reflect_limit_hit` skew — real reflect engagement is closer to the 15 users on `reflect_message_sent`) |
| workspace | 124 | 16 |
| session_recording | 118 | 16 |
| health_check | 67 | 15 |
| monetization | 37 | 11 |
| between_session | 62 | 11 |
| symptoms | 47 | 7 (small-n) |
| voice_notes | 22 | 6 (small-n) |
| therapy_prep | 24 | 6 (small-n) |
| quick_capture | 19 | 6 (small-n) |
| goals | 4 | 2 (small-n) |

No mapped events found for "stats" (no distinct `stats_*` event exists) or "gamification/streaks" (no `streak_*`/`achievement_*` events exist at all — matches CLAUDE.md noting gamification is still planned).

Feature-breadth histogram (distinct feature categories touched per person, last14d):

| breadth (# distinct features) | n_users |
|---|---|
| 1 | 14 |
| 2 | 3 |
| 3 | 4 |
| 4 | 8 |
| 5+ (bucketed: 5,6,7,8,10,11,13,14) | 25 |

Total users with ≥1 mapped feature-event = 54.

### 8. Therapy-loop stage completion, last14d (distinct users per stage)

| prep | recording | debrief | between_session | timeline_viewed (weak proxy for "summary viewed") |
|---|---|---|---|---|
| 6 | 16 | 17 | 11 | 46 |

No dedicated summary-view/summary-generated PostHog event exists — the loop's "summary" stage is **not directly measurable** in PostHog. `timeline_viewed` is listed as a loose proxy only (people view the timeline for many reasons besides reading a summary), not a substitute.

Note the ordering: more distinct users touch `recording` (16) and `debrief` (17) than `prep` (6) — most people who record/debrief a session in this window did not emit a `prep_card_*`/`prep_capture_*` event first in the same window (could mean the prep stage is skipped, was done in a prior window, or is under-instrumented — data alone can't distinguish these).

### 9. Notifications, last14d vs prev14d

| event | last14d (c/users) | prev14d (c/users) |
|---|---|---|
| notification_permission_prompted | 55/20 | ∅ (new) |
| notification_permission_granted | 44/14 | ∅ (new) |
| notification_opened | 22/9 | 18/4 |
| notification_received | 12/5 | 8/3 |
| notification_permission_denied | 11/6 | ∅ (new) |
| notification_row_toggled | 4/1 (single-user) | ∅ (new, likely replaces notification_interest_toggled) |
| $push_notification_opened | 1/1 (small-n) | ∅ (new) |
| notification_interest_toggled | ∅ | 13/2 |
| notification_banner_tapped | ∅ | 2/1 |
| notification_master_toggled | ∅ | 2/1 |

Permission-prompt→grant: 20 prompted, 14 granted, 6 denied in last14d (granted+denied=20=prompted, consistent). `notification_received` (12/5) vs `notification_opened` (22/9) last14d — more "opened" than "received" events is odd for a delivery→open pipeline and is worth a flag: either `notification_opened` also fires for non-push-triggered opens (e.g. deep-linking into a moment from in-app), or `notification_received` under-fires relative to actual delivery. Cannot resolve which from PostHog data alone.

### 10. Monetization, last14d

| event | c | users |
|---|---|---|
| subscription_screen_opened | 25 | 11 |
| subscription_product_selected | 5 | 4 (small-n) |
| paywall_dismissed | 4 | 3 (small-n) |
| subscription_purchase_started | 2 | 2 (small-n) |
| subscription_purchase_failed | 1 | 1 (small-n) |

**Does NOT exist at all (zero rows in last14d or prev14d, or ever, per this pull):** `paywall_shown`, `subscription_purchase_completed`, `trial_started`, `trial_ended`. `promo_code_applied` existed in prev14d (3/2) but is zero in last14d.

Paywall→purchase conversion is **not measurable** from PostHog (no `paywall_shown`, no purchase-completed event). Revenue truth (who actually paid) lives in Postgres `subscription_receipts` — hand off to `database-administrator`.

### 11. Platform / app-version split, last14d (client events only)

| $os | users |
|---|---|
| Android | 86 |
| Linux | 66 |
| iOS | 25 |
| Windows | 6 |
| Mac OS X | 5 |
| iPadOS | 1 |

Caveat: `Linux` (66 users) is almost certainly desktop/web marketing-site traffic (`$pageview`/`$autocapture`/`$web_vitals` events), not the Flutter mobile app — MindSync has no Linux desktop client. Treat Android+iOS+iPadOS (112 users) as the mobile-app platform split.

| $app_version | users | first_ts | last_ts |
|---|---|---|---|
| 2.0.76 | 29 | 2026-08-04 | 2026-08-10 |
| 2.0.75 | 56 | 2026-07-27 | 2026-08-09 |
| 2.0.60 | 15 | 2026-07-27 | 2026-08-09 |
| 2.0.44 | 3 (small-n) | 2026-07-29 | 2026-08-07 |
| 2.0.36 | 1 (small-n) | 2026-08-01 | 2026-08-01 |

18 users (15+3) are on builds 2+ minor versions behind (2.0.60/2.0.44/2.0.36) and still active in the last14d window — a meaningful stale-build tail (relevant for anyone attributing a behavior change to a recent release, per the stale-build triage pattern already in project memory).

### 12. Top 20 `$screen_name` values by distinct users, last14d

| screen | events | users |
|---|---|---|
| splash | 216 | 80 |
| auth | 110 | 57 |
| mainPage | 835 | 45 |
| signUp | 44 | 35 |
| therapyOnboarding | 116 | 33 |
| settings | 148 | 19 |
| healthCheckFlow | 42 | 16 |
| afterTherapyFlow | 47 | 16 |
| prepTherapyFlow | 21 | 12 |
| account | 47 | 11 |
| subscription | 27 | 11 |
| betweenSessionsFlow | 44 | 11 |
| mainPageTab | 76 | 9 |
| recordSessionFlow | 33 | 9 |
| forgotPassword | 7 | 7 (small-n) |
| therapists | 15 | 6 (small-n) |
| about | 6 | 4 (small-n) |
| consentCodeEntry | 2 | 2 (small-n) |
| audioChat | 1 | 1 (small-n) |
| recordingDetail | 1 | 1 (small-n) |

## Caveats

- Ingest started 2026-04-22; the retention query's global first-seen computation is bounded to that date, no clamping issue observed for this 14d/28d window (well inside available history).
- `reflect_limit_hit` = 1870 events from 1 person_id — this single user dominates both the `reflect` feature-adoption event count and much of the 2026-08-04 daily spike. Do not read `reflect` engagement off the events column; use `reflect_message_sent` users (15) instead.
- `conversation_message_sent`/`conversation_started`/`conversation_ended` and `notification_row_toggled` are each 1-user in last14d — likely test/dev traffic or a single early adopter of a new legacy-named event, not a real usage signal yet.
- `Linux` in the `$os` platform split is web/marketing traffic, not the mobile app — see caveat under section 11.
- No PostHog event exists for "summary viewed/generated" (therapy-loop final stage) or for gamification/streaks/achievements — both are instrumentation gaps, not zero-usage findings. Hand off to `data-analytics` (summaries) / `backend-api` (gamification, still marked "planned" in CLAUDE.md) if these need to become measurable.
- `paywall_shown` and any purchase-completed event do not exist — paywall→purchase funnel is not measurable in PostHog; use Postgres `subscription_receipts` via `database-administrator` for revenue truth.
- All counts are aggregate; no PII, therapy content, or raw per-user data included. Segments under 25 users are labeled "(small-n)" rather than suppressed, since these are aggregate feature/screen/event counts, not identifying cohorts.

## Queries

See `batch1_inventory.sql` and `batch2_full.sql` sections executed via `scripts/posthog_query.py --sql-file`, reproduced below.

```sql
-- @@ event_inventory_last14d
SELECT event, count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp > now() - INTERVAL 14 DAY
GROUP BY event
ORDER BY c DESC
LIMIT 200

-- @@ event_inventory_prev14d
SELECT event, count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp <= now() - INTERVAL 14 DAY AND timestamp > now() - INTERVAL 28 DAY
GROUP BY event
ORDER BY c DESC
LIMIT 200

-- @@ daily_activity_14d
SELECT toDate(timestamp) AS day, count(DISTINCT person_id) AS dau, count() AS events
FROM events WHERE timestamp > now() - INTERVAL 14 DAY
GROUP BY day ORDER BY day

-- @@ new_users_by_day_14d
SELECT toDate(first_ts) AS day, count() AS new_users
FROM (
  SELECT person_id, min(timestamp) AS first_ts
  FROM events
  WHERE timestamp > toDateTime('2026-04-22')
  GROUP BY person_id
)
WHERE first_ts > now() - INTERVAL 14 DAY
GROUP BY day ORDER BY day

-- @@ wau_by_week_5w
SELECT toStartOfWeek(timestamp) AS week, count(DISTINCT person_id) AS wau
FROM events WHERE timestamp > now() - INTERVAL 35 DAY
GROUP BY week ORDER BY week DESC

-- @@ daily_dau_5w_for_stickiness
SELECT toStartOfWeek(timestamp) AS week, toDate(timestamp) AS day, count(DISTINCT person_id) AS dau
FROM events WHERE timestamp > now() - INTERVAL 35 DAY
GROUP BY week, day ORDER BY week DESC, day

-- @@ retention_new_cohort_14d
SELECT
  count() AS cohort_size,
  countIf(distinct_days > 1) AS returned_any_day,
  countIf(days_span >= 7) AS active_7d_plus
FROM (
  SELECT person_id,
    min(timestamp) AS first_ts,
    max(timestamp) AS last_ts,
    count(DISTINCT toDate(timestamp)) AS distinct_days,
    dateDiff('day', toDate(min(timestamp)), toDate(max(timestamp))) AS days_span
  FROM events
  WHERE timestamp > toDateTime('2026-04-22')
  GROUP BY person_id
  HAVING first_ts > now() - INTERVAL 14 DAY
)

-- @@ onboarding_funnel_14d
SELECT countIf(steps >= 1) AS s1_viewed, countIf(steps >= 2) AS s2_completed, countIf(steps >= 3) AS s3_onboarding_completed, count() AS total_people
FROM (
  SELECT person_id, windowFunnel(86400)(toDateTime(timestamp),
    event = 'onboarding_step_viewed',
    event = 'onboarding_step_completed',
    event = 'onboarding_completed') AS steps
  FROM events
  WHERE timestamp > now() - INTERVAL 14 DAY
    AND event IN ('onboarding_step_viewed','onboarding_step_completed','onboarding_completed')
  GROUP BY person_id
)

-- @@ onboarding_step_breakdown_14d
SELECT properties.step_index AS step_index, properties.step_name AS step_name, event, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event IN ('onboarding_step_viewed','onboarding_step_completed') AND timestamp > now() - INTERVAL 14 DAY
GROUP BY step_index, step_name, event ORDER BY step_index, event

-- @@ onboarding_step_duration_14d
SELECT properties.step_index AS step_index, properties.step_name AS step_name, count() AS c,
  avg(toFloat64OrNull(toString(properties.duration_seconds))) AS avg_duration_s,
  median(toFloat64OrNull(toString(properties.duration_seconds))) AS median_duration_s
FROM events WHERE event = 'onboarding_step_completed' AND timestamp > now() - INTERVAL 14 DAY
  AND properties.duration_seconds IS NOT NULL AND toString(properties.duration_seconds) != ''
GROUP BY step_index, step_name ORDER BY step_index

-- @@ feature_adoption_14d / feature_breadth_histogram_14d
-- (multiIf event->feature category map; see scratchpad batch2_full.sql for full text)

-- @@ therapy_loop_stages_14d
SELECT
  count(DISTINCT if(event IN ('prep_card_started','prep_card_created','prep_capture_started','prep_capture_submitted'), person_id, NULL)) AS prep_users,
  count(DISTINCT if(event IN ('recording_started','recording_saved'), person_id, NULL)) AS recording_users,
  count(DISTINCT if(event IN ('debrief_started','debrief_created'), person_id, NULL)) AS debrief_users,
  count(DISTINCT if(event IN ('between_session_started','between_session_created'), person_id, NULL)) AS between_session_users,
  count(DISTINCT if(event = 'timeline_viewed', person_id, NULL)) AS timeline_viewed_users
FROM events WHERE timestamp > now() - INTERVAL 14 DAY

-- @@ notifications_14d / notifications_prev14d
SELECT event, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp > now() - INTERVAL 14 DAY
  AND event IN ('notification_permission_prompted','notification_permission_granted','notification_permission_denied','notification_received','notification_opened','notification_row_toggled','notification_interest_toggled','notification_banner_tapped','notification_master_toggled','$push_notification_opened')
GROUP BY event ORDER BY c DESC

-- @@ monetization_14d
SELECT event, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp > now() - INTERVAL 14 DAY
  AND event IN ('paywall_shown','paywall_dismissed','subscription_screen_opened','subscription_product_selected','subscription_purchase_started','subscription_purchase_completed','subscription_purchase_failed','promo_code_applied','trial_started','trial_ended')
GROUP BY event ORDER BY c DESC

-- @@ platform_split_14d
SELECT properties.$os AS os, count(DISTINCT person_id) AS users
FROM events WHERE timestamp > now() - INTERVAL 14 DAY AND properties.$os IS NOT NULL AND properties.$os != ''
GROUP BY os ORDER BY users DESC

-- @@ app_version_split_14d
SELECT properties.$app_version AS ver, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events WHERE timestamp > now() - INTERVAL 14 DAY AND properties.$app_version IS NOT NULL AND properties.$app_version != ''
GROUP BY ver ORDER BY last_ts DESC

-- @@ top_screens_14d
SELECT properties.$screen_name AS screen, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = '$screen' AND timestamp > now() - INTERVAL 14 DAY AND properties.$screen_name IS NOT NULL AND properties.$screen_name != ''
GROUP BY screen ORDER BY users DESC LIMIT 20
```
