# Prep Cards Diagnosis - Why They're Nearly Absent From the Therapy Loop

Date: 2026-08-10
Author: data-analytics (diagnosis only, no fixes applied)
Backend HEAD examined: main 02bdce9. Frontend HEAD examined: dev dc5b340.

## Verdict

**Both, but for different reasons, and the balance is "the built auto-generation pipeline
never generates" rather than "generated cards go undiscovered".**

- The automatic, no-effort path ("we generate your prep card ~24h before your session")
  is **completely dead in production**: the cron job has run successfully (no exceptions,
  "Job OK" every time) roughly hourly since March 2026, but has produced **zero** rows
  ever. This is a generation failure, not a discovery failure - there is nothing for the
  user to discover.
- The manual path (user taps "Prepare" and types/records their own prep) **works
  correctly** and is in fact the *only* path that has ever produced a prep card in prod.
  It is just used by very few people, both because its population is small (schedule +
  premium/trial gating on the smart auto path; the manual path itself is ungated for
  creation) and because the "Prepare" CTA has a narrower, less persistent exposure window
  on the Main tab than "Debrief" does.

## Evidence

### 1. Code: two separate "auto-generate" mechanisms exist, one of them is orphaned

`MindSync/app/tasks/prep_card_auto_generate.py` - the actual cron job:
- Registered via `setup_hourly_prep_auto_generate()` in `app/core/rq_scheduler_setup.py`
  (cron `"30 * * * *"`), which **is** called from `app/main.py` lifespan (line 125). This
  rules out the "registered only in the web dyno, never in the worker" bug pattern that
  previously bit Notification Moments (2026-07-03) - confirmed live: RQ Scheduler on prod
  currently holds the job (`mindsync_hourly_prep_card_auto_generate | Prep card
  auto-generation (hourly) | cron_string: '30 * * * *'`).
- Entry population: `User JOIN UserSubscription (is_active=True) JOIN UserPreferences
  (therapy_schedule IS NOT NULL)`. `is_active=True` on `UserSubscription` is exactly the
  premium/in-trial gate (`_create_initial_subscription` in `users.py` sets
  `subscription_type=PREMIUM, is_active=True` only on the trial-days path; the no-trial
  path gets `BASIC, is_active=False`; the hourly deactivation cron flips `is_active` to
  False when a trial/subscription lapses) - i.e. this job **only ever looks at
  premium-or-trialing users who have also configured a therapy schedule**.
- Entry window: `23.0 <= hours_until <= 25.0` computed against
  `app/utils/therapy_schedule_utils.compute_next_session_date`, checked at minute :30
  every hour. The utility functions are tz-aware end-to-end (confirmed by reading the
  full file) - this is not the same naive/aware datetime bug seen live in a *different*
  job (`[WEEKLY_THERAPY_SUMMARY] Error ... can't compare offset-naive and offset-aware
  datetimes`, observed in worker logs at 2026-08-10T10:13-10:16 UTC), so that specific bug
  class does not appear to reach this job's date math.
- Skip condition: an existing **COMPLETED** `SessionPrepCard` in the 48h window before the
  session **blocks generation, regardless of `generation_type`** (i.e. a manually-created
  card also suppresses the auto path for that session).
- `POST /prep-cards/auto-generate` (in `app/api/v1/endpoints/prep_cards.py`) is a second,
  independent, on-demand version of "auto-generate" - synchronous, premium/free-tier
  gated via `can_use_ai()`, and the **only** place that fires the
  `prep_card_auto_generated` PostHog event.

### 2. Client: the on-demand REST endpoint is unreachable from the UI

`mindsync-frontend/mindsync_app/lib/api/api_managers/prep_card_manager.dart` defines
`autoGeneratePrepCard()` (POST `/prep-cards/auto-generate`). Grepped the entire `lib/`
tree - **no call site exists anywhere in the app.** The button/flow that would trigger it
was never wired up (or was removed). This alone explains why `prep_card_auto_generated`
has never fired in PostHog: the code path that emits it is dead code from the client's
perspective, independent of whether the cron job works.

The surface users actually reach is the Main-tab "Prepare" CTA
(`main_tab_screen.dart` / `main_tab_cubit.dart`), which calls
`TherapyFlowLauncher` with `getLatest: () => PrepCardManager().getLatestPrepCard()`. If no
prep card matches the upcoming session (`prepCardMatchesNextSession`, comparing
`sessionDate`/`createdAt` against the computed next session, mirroring the backend's
23-25h/48h windows), it routes into the **manual capture flow**
(`prep_question_flow_screen.dart` -> `POST /prep-cards/` or `/prep-cards/voice`), which is
what produces the newly-appeared `prep_capture_started` / `prep_capture_submitted`
PostHog events. This is the feature working as built for the manual path - it is simply
the *only* path that has ever fired.

### 3. Production DB (session_prep_cards vs session_debriefs, read-only, aggregates only)

```
session_prep_cards:
  total=115 | generation_type='auto'=0 | 'manual'=86 | NULL(legacy pre-overhaul)=29
  distinct_users=57 | first_row=2026-02-28 | last_row=2026-08-10
  by input_type: TEXT=90, VOICE=25
  by status: COMPLETED=111, PENDING=3, FAILED=1
  last 30d: 19 rows / 9 distinct users

session_debriefs (comparison, same window):
  total=115 | distinct_users=47 | first_row=2026-02-28 | last_row=2026-08-10
  last 30d: 23 rows / 11 distinct users
```

Prep and debrief have nearly identical *total* row counts (115 vs 115) and similar total
distinct users (57 vs 47) over the product's lifetime, but debrief pulls slightly more
users in any given 30-day window (11 vs 9) - consistent with the PostHog 14-day read
(debrief 17 vs prep 6) showing debrief with meaningfully broader current reach, not with
prep being structurally unusable.

**Population feeding the auto-gen job, right now:** of 1800 total users, only **9** have
an active subscription/trial AND a configured `therapy_schedule` - the exact population
the cron job iterates. Of those 9, 5 have created at least one prep card manually at some
point (of any status/date, not necessarily inside the cron's blocking 48h window); the
manual-capture user base as a whole (57 users) mostly does **not** have a therapy_schedule
configured (only 17 of 57 do) - i.e. most manual prep-card creators are outside the
auto-gen job's eligibility criteria entirely, and most auto-gen-eligible users have at
least dabbled in manual capture. `therapy_schedule` itself is configured by only 138 of
1800 users (7.7%) - the "next session" card, and therefore both prep paths, is invisible
to the other 92%.

### 4. Live confirmation the job runs and does nothing

- RQ `FinishedJobRegistry` on the `default` queue: **92 retained entries** for
  `app.tasks.prep_card_auto_generate.auto_generate_prep_cards`, spanning 2026-03-30
  through 2026-08-10 (registry is capped/rotated; true historical run count is higher),
  every one at `:30` past the hour, **zero** in `FailedJobRegistry`.
- Watched a live tick: at `2026-08-10T10:30:58Z` the worker dequeued
  `mindsync_hourly_prep_card_auto_generate` and RQ logged `Successfully completed Prep
  card auto-generation (hourly) job in 0:00:01.821209s` / `Job OK` at `10:31:00.41Z`.
  Consistent with a run that iterates a handful of users and finds none inside the 2-hour
  window - no OpenAI calls, no DB writes, ~1.8s.
- **No `[AUTO-GEN]` log lines appear anywhere in the worker logs**, including the module's
  own `logger.info("... START")` that is the very first statement in the function body.
  Given the job provably executes (RQ's own wrapper confirms elapsed time and outcome),
  this means the worker process's logging configuration is filtering out this logger's
  INFO-level output - so **log inspection alone cannot distinguish "0 users ever entered
  the loop" from "N users entered, all skipped/failed silently"**; the Postgres row count
  (0 ever) is the only reliable ground truth here, and other jobs' `logger.warning`/`.error`
  calls (e.g. the WEEKLY_THERAPY_SUMMARY tz error) remain visible because they're above
  the filtered level - a secondary observability gap worth flagging to backend-api/devops
  independently of the prep-card issue itself.

## Root-cause read

The auto-generation *pipeline* (cron -> AI -> stored card -> surfaced via
`prepCardMatchesNextSession`) is not a design failure and is not obviously broken by a
single bug we could pin down and reproduce - it is registered correctly, runs on schedule,
never throws, and its date math is tz-safe by inspection. What's broken is upstream of any
single line: the entry population is minuscule (9 users today; needs BOTH an
active premium/trial subscription AND a manually-configured therapy_schedule, two
independent, low-adoption gates multiplying together to a near-empty set out of 1800
users), and even within that tiny population the DB shows zero successful generations
across ~5 months and 92+ observed successful runs - which is far more consistent with
"the entry conditions (window + no-existing-card) are essentially never simultaneously
satisfied for this population" than with bad luck. We could not fully close this last
gap without either (a) restoring INFO-level logging for this job to see real
checked/generated/errors counts per run, or (b) instrumenting a one-off diagnostic run -
both of which are code changes, out of scope for this diagnosis task.

Separately and unambiguously: the `POST /prep-cards/auto-generate` on-demand endpoint and
its `prep_card_auto_generated` telemetry are dead code from the client's perspective - no
UI action calls it. That accounts for that specific event's 365-day silence independent of
whatever the cron does.

The manual capture path works and is the sole source of every prep card ever created in
prod. Its lower reach vs. debrief/recording/between_session most plausibly comes from (a)
the same `therapy_schedule` gate limiting who ever sees a "Prepare" CTA at all, and (b) the
CTA's exposure window on Main tab being narrower/more conditional (prep only surfaces
within the 72h pre-session window per `betweenSessionsPrepWindow`, whereas the Debrief CTA
takes priority and persists any time a just-had session lacks a debrief) - not from any
defect in the manual creation flow itself (111/115 rows COMPLETED).

## Recommended fix, with owner

This is a diagnosis-only task; the following is a recommendation, not applied:

1. **backend-api** (owns `app/main.py`, general services, logging config): restore
   INFO-level output for `app.tasks.prep_card_auto_generate` (and likely other `app/tasks/*`
   loggers - this looks like a worker-wide logging-level configuration issue, not specific
   to this module) so `checked=/generated=/errors=` counts are actually visible per run.
   Without this, nobody can tell "0 eligible" from "eligible but always skipped" from
   inside the running system - the DB was the only way to get an answer here.
2. **backend-api or data-analytics** (coordinate via lead - touches
   `prep_card_auto_generate.py`, owned by data-analytics): once (1) lands, watch one real
   `:30` tick against the current 9-user population and read the actual
   checked/generated/errors numbers before deciding whether to touch the entry-window or
   the "existing card" skip logic. Don't guess at a fix blind - the logging gap needs
   fixing first.
3. **flutter-mobile**: either wire `PrepCardManager.autoGeneratePrepCard()` into a real UI
   action (an explicit "auto-generate mine now" affordance) or delete it and the associated
   `prep_card_auto_generated` PostHog event as retired/never-shipped - it is currently pure
   dead code that would mislead anyone reading PostHog data into thinking a feature exists
   that does not.
4. **ui-ux-designer / lead**: worth a product decision, not just a bug fix - the
   `therapy_schedule` prerequisite gates the entire "next session" card (prep AND debrief
   AND between-sessions) behind a setup step only 7.7% of users complete. Widening prep's
   reach is more a "get more people to set a therapy_schedule, and consider whether prep
   should require premium/trial at all for the auto path" product question than a
   generation-pipeline bug question.

No code was modified. No prod data was mutated (all queries were read-only `SELECT`s under
`SET TRANSACTION READ ONLY`, aggregates/counts only, no PII). Two one-off diagnostic
Heroku dynos used for querying (`run.3063`, `run.4182`) were stopped after use.
