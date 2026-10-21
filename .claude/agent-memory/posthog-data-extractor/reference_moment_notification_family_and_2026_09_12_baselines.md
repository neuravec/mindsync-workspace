---
name: moment-notification-family-and-2026-09-12-baselines
description: The backend moment.* notification family (sent/opened/scheduled/expired) reaches a population 14x larger than active app users - the single most load-bearing finding for growth reporting. Plus corrected instrumentation status and 2026-09-12 baselines (30d).
metadata:
  type: reference
---

# The `moment.*` family and the backend-touched-vs-active-app-user gap (found 2026-09-12)

This is the most important structural fact discovered so far for reading ANY
"how many users" number in this project: there are two very different
populations, and conflating them silently produces wildly wrong reads.

- **Client app users** (`properties.$lib = 'posthog-flutter'`, bot-filtered):
  people who actually opened the app. 30d (2026-08-13..2026-09-13): **127**.
- **Backend-touched users** (any `properties.$lib = 'posthog-python'` event,
  e.g. a scheduled/sent notification, a generated summary): 30d: **1874**.

The backend notification/summary crons fire for essentially the WHOLE
historical registered base regardless of whether that person has opened the
app recently. Concretely, `moment.sent`/`moment.scheduled`/`moment.expired`
each reach **~1800-1830 distinct recipients** in a 30d window (24473/16683/
21499 events respectively), and `weekly_summary_generated`/
`monthly_audit_generated` reach **~1800-1817 recipients** too (7233/3584
events). **None of these numbers are "active users" - do not report them as
such.** The real active-app population in the same window is 127, i.e.
roughly **1/14th** the backend-touched population. This ratio (or its
inverse, "backend touches ~14x more accounts than open the app monthly") is
itself a headline finding for a churn/direction conversation - it is
independent corroboration of harsh retention numbers (D30 retention 0.8%,
one-and-done 66% at 30d / 66.2% at 90d - see below) found the same session.

## `moment.*` is the actual "notifications sent vs opened" instrumentation

`moment.sent` / `moment.opened` / `moment.scheduled` / `moment.dismissed` /
`moment.expired` / `moment.acted` (all `posthog-python`, emitted via
`posthog_track_moment(...)` in `app/services/notification_orchestrator.py`)
are the correct events for a "sent vs opened" pull - NOT the client-side
`notification_received`/`notification_opened` alone (those exist too, much
lower volume, and roughly corroborate the backend number at 1/10th scale:
30d client `notification_opened` = 47 events/16 users vs backend
`moment.opened` = 47 events/26 users - same order of magnitude, useful
cross-check but not the primary signal).

**30d (2026-08-13..2026-09-13) open rate: 26 recipients opened out of 1815
sent to = 1.4%.** Event-level: 47/24473 = 0.19%. This is a severe result -
the primary re-engagement mechanism has a ~1-in-70 open rate at the
recipient level.

`moment.sent` carries `properties.moment_type` (breakdown available: top 5
types - WEEKLY_SUMMARY_READY, ADD_THERAPY_DATE, REFLECTION_INVITATION,
THERAPY_RELATIONSHIP_CHECKIN, MONTHLY_SUMMARY_READY - each sent to
1700-1830 recipients, dwarfing a long tail of 13 other types each under 25
recipients). **`moment.opened` carries NO `moment_type` (100% null on all 47
rows checked)** - you cannot attribute opens back to a specific notification
type from PostHog data alone; only the "sent" side is typed.

# Instrumentation status corrections (things that changed since 2026-08-10)

Re-verify-before-trust paid off again - several facts recorded 2026-08-10 are
now stale:

- **`paywall_shown` now exists and flows** (created_at 2026-08-16, still
  correctly absent before that). Very thin: lifetime-to-date (as of
  2026-09-12) = 10 events / 7 users, identical in a 30d and 90d window
  because 2026-08-16 is inside both. Carries `properties.trigger_feature`
  (values seen: `drawer_menu`, `settings`, `premium_gate_session_recording`,
  `premium_gate_reflect_messages`) - the trigger breakdown the 2026-08-10
  memory said was impossible for `subscription_screen_opened` IS now possible
  via `paywall_shown`, just on a very small n. Note `subscription_screen_opened`
  users (15, 30d) exceed `paywall_shown` users (7) - most subscription-screen
  visits do NOT go through a `paywall_shown`-emitting trigger path, so this
  event still undercounts total premium-screen exposure.
- **`recording_processing_started`/`_completed` now fire** (first_seen
  2026-08-12, contradicting the 2026-08-10 memory note "never fired, ever").
  Still low volume: 46 started / 37 completed, 5 users, 30d. The 2026-08-10
  "recording pipeline backend half is completely dark" finding is now
  outdated - re-verify current pipeline completion rate if this comes up again.
- **`voice_transcription_failed` now fires** (created_at 2026-08-20, first
  event after the 2026-08-10 "never fired" check) - 11 events / 2 users, 30d.
- **`conversation_started`/`_message_sent`/`_ended` (legacy chat model) are
  now DEAD** - last_seen 2026-08-11 project-wide, **zero events in the
  2026-08-13..2026-09-13 window** despite existing in the event catalog.
  Live successor for "chat/conversation usage" is the `reflect_*` family
  (`reflect_session_started`, `reflect_message_sent`). Flag to
  `flutter-mobile`/`backend-api` to confirm this is an intentional
  deprecation (Reflect replacing Conversations) and not an accidentally
  broken capture call.
- **Onboarding now has 9 named steps, not 8**: `personalise` joined
  `legal_gate, challenges, intensity, journey, modality, schedule, companion,
  lead_source` (the 2026-08-10 memory's "spec says 9, only 8 emit step_name"
  gap is closed).

# Confirmed-still-absent (unchanged)

- `trial_started`/`trial_ended`: zero events, full project history, checked
  2026-09-12 against the complete `event_definitions` catalog (168 event
  names enumerated) - not just a windowed check.
- **Habit Tracker (shipped 2026-09-02, MSV3.12) has ZERO PostHog
  instrumentation** - no event name containing "habit" anywhere in the full
  event catalog, and it does not even surface as a `$screen_name` (the
  widget lives on `mainPage`, not a dedicated screen, per
  `habits_card.dart`/`main_tab_screen.dart` - this is architecturally why
  `$screen` can't catch it either, not a missed `capture()` call
  necessarily). Adoption of this feature is entirely unanswerable from
  PostHog; Postgres (`habits`/`habit_logs` tables, via
  `database-administrator`) is the only source of truth.
- **No single "Your Session" entry event exists.** The 2026-09-03 MSV3.13
  "Your Session flow" rename did not add a dedicated capture call (or it
  exists under a name not yet found). Usable proxy: union of
  `prep_capture_started`/`prep_card_started` (prep stage) +
  `recording_started` (recording stage) + `debrief_started`/`debrief_created`
  (debrief stage) - matching `$screen_name` values `prepTherapyFlow` (12 users
  30d) / `recordSessionFlow` (10 users) / `afterTherapyFlow` (23 users,
  highest of the three - worth noting people reach the "after" screen more
  than the recording screen itself, possibly via a different entry route).
- "Threads" has no standalone event - it is part of Reflect
  (`reflect_thread_opened`/`_deleted`), matching the MSV3.11 "Threads,
  Reflect & Grace" project scope.
- `summary_viewed.properties.period_type` only ever takes values `weekly` and
  `monthly_audit` - **no `daily` value exists**, confirming daily-summary
  viewing is unmeasurable in PostHog (matches the already-known absence of
  any `daily_summary_generated`/`_viewed` event).

# Baselines, 2026-09-12, 30d window (2026-08-13..2026-09-13) unless noted

- MAU (app, bot-filtered) = 127. WAU by week: 08-09 28(partial) · 08-16 51 ·
  08-23 34 · 08-30 35 · 09-06 37(partial). DAU range 4-16/day.
- $os split (30d, one value per person via `any()`): Android 108, iOS 19
  (sums to MAU exactly - the `any()`-per-person trick avoids the double
  counting that a naive `GROUP BY properties.$os` with `count(DISTINCT
  person_id)` produces when some of a person's events lack `$os`).
- $app_version split (30d): 2.0.77 (56) / 2.0.85 (45) / 2.0.89 (38, newest)
  dominate; long tail of 2.0.36 through 2.0.88 at 1-9 users each. Sums to
  >127 because a person can appear under 2 versions if they updated mid-window
  - do not read the per-version sum as additive against MAU.
- D1/D7/D30 retention (right-censoring-safe cohort eligibility windows, i.e.
  each cohort's cutoff is chosen so the full follow-up period has already
  elapsed): D1 = 24/319 = 7.5%. D7 = 12/303 = 4.0%. **D30 = 2/244 = 0.8%.**
  This D30 number is the hardest evidence in the whole 2026-09-12 pull.
- One-and-done: 66.2% of 382 users active in the trailing 90d have activity
  on exactly one calendar day, lifetime. Cross-checked via a second method
  (30d frequency histogram): 68.5% of the 127 30d-active users have exactly 1
  active day in that 30d window. Same conclusion, two independent windows.
- New-user-per-week (12wk) returned-next-week rate: bounces between 5% and
  23%, no visible trend, median ~12%.
- Retention-vs-features (cohort 2026-07-05..2026-07-26, n=102): only
  **5 people (4.9%) survived to W2** - too small a segment to break down by
  feature (k-anonymity threshold 25) so only the n=97 "churned by W1"
  segment's week-0 feature mix is reportable. If this comparison needs to be
  redone with a large-enough survivor segment, widen the cohort span
  (multiple months) rather than reusing a 3-week window - at ~5% survival you
  need 500+ new users in the cohort to clear n=25 survivors.
- Feature adoption ranking (30d, % of 127 MAU): Timeline/stats 52.0% >
  Workspace/dashboard 33.1% > "Your Session" any-stage 22.0% > Threads 21.3%
  > Reflect session-started 19.7% > backend moment.opened 20.5% > Reflect
  message-sent 12.6% > voice_note 7.1% > session_recording 5.5%. Dashboard
  and Timeline/stats usage beats every "active" feature (chat, recording,
  threads) - people come back mostly to look at their history/hub, not to
  generate new content.
- api_error (30d): 4639 events / 82 users (64.6% of MAU hit at least one).
  Top1-user share 23.3% (1083 events) but NOT the dominant driver this time
  (contrast with the 2026-08-10 reflect_limit_hit single-user 59.5% skew).
  93% of volume is `is_expected=True` 404s on `/prep-cards/latest`,
  `/debriefs/latest`, `/health-check/latest` (deliberate empty-state
  responses, confirms the 2026-08-10 root-cause theory). The
  `is_expected=False` remainder is concentrated on `/users/
  get_user_profile_and_subscript…` (38 users) and `/users/therapy-context`
  (40 users) 404s - together ~30% of all 127 MAU hit one of these two
  "unexpected" 404s in 30 days. Worth a `backend-api` look; out of scope for
  this extraction task.

See also [[reference_default_exclusion_filters]],
[[reference_voice_chat_and_backend_lib_trap_2026_08_10]]. Full extract with
all queries: `analytics-reports/raw/2026-09-12-usage-retention-monetization-extract.md`.
