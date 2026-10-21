# Usage Trend and Paywall Exposure: Business Insight Report

- **Date**: 2026-09-25
- **Analyst**: growth-analyst
- **Business question**: Is app usage growing and are users staying more often, and is the lack of revenue explained by a paywall that almost never shows because too much is free?
- **Data window**: 2026-05-01 to 2026-09-24 (September is a partial month, 24 days). Cohort retention: signup months May to September.
- **Sources**: PostHog EU project 141170 (HogQL via `scripts/posthog_query.py`, read-only) · code read of `MindSync/app` (premium checks) and `mindsync-frontend/mindsync_app/lib` (paywall entry points) · prod Postgres **not re-queried** (see Data caveats), prior DB baseline from `db-reports/2026-09-12-subscription-revenue-30d.md` · benchmarks from RevenueCat and earlier reports
- **Confidence**: **High** on the direction of both verdicts (several independent measures agree). **Low to medium** on anything at the level of single features or the premium segment, where n is 1 to 16 people.

All user counts are distinct PostHog persons on app events (`$lib='posthog-flutter'`), with the known device farm (`OnePlus8Pro`, `Pixel 6 Pro`) and emulators removed. Backend Reflect events (`$lib='posthog-python'`) are counted separately. One non-phone test client that fired 112 `reflect_session_started` on 2026-09-17 is excluded.

---

## Executive Summary

- **Claim 1, "usage has grown and users stay more often": PARTLY TRUE, and mostly the wrong way round.** The number of people fell hard: comparable 24-day MAU went 211 (May) -> 129 (Aug) -> 111 (Sep), which is -47%, and new app users per month fell from 213 to 101 (-53%, May to Aug). What went up is **intensity among the few who stay**. Active days per user rose from 1.6 to 2.1, sessions per user from 2.3 to 3.1, and DAU/MAU from 6.6% to 8.6%. The returning base, though, is flat at **30 to 42 people a month**. The August and September cohorts retain somewhat better (D1 10.7% vs 6.2% for May to July, p about 0.05), which is an early signal and is not proven yet.
- **Where the feeling of growth probably comes from:** raw PostHog volume jumped from 18.6k events and 183 persons in July to **97.5k events and 1,916 persons in August**. That jump is backend crons (notifications, summaries) touching the whole account base. It is not people using the app.
- **Claim 2a, "the paywall basically never shows": TRUE.** `paywall_shown` has fired **16 times in its whole history** (since 2026-08-16). In the last 30 days **5 of 127 active users (3.9%)** saw it, and 10 (7.9%) opened the subscription screen. Most views came from people who opened the drawer menu themselves. Premium gates sent at most **1 to 2 people a month** to the paywall.
- **Claim 2b, "because so much is free, nothing pushes people to pay": MOSTLY FALSE as the cause.** The paywall is invisible for three structural reasons, and a generous free tier is only the smallest of them:
  1. **Every new account gets 4 days of premium automatically, and during those days the app suppresses the paywall and every gate.** 71% of registered users (258 of 365) never open the app again after day 4, so most people only ever see the premium version of the app and never meet a gate.
  2. **Retained free users are too light to reach any limit.** They average **1.7 active days a month**, and mostly read the timeline and workspace. The limits (30 Reflect messages, 5 debriefs, 2 recordings, 1 habit) sit well above that.
  3. **The heavy users are already premium.** Among retained users, the 7 premium users average 11.4 active days a month and the 33 free users average 1.7.
- **Top recommendation:** put the paywall at the moments people actually pass through. That means the end of the auto trial (the day-3 and trial-ended popups already exist in code but are never called) and the soft-locked "insight" surfaces that light users look at. Then test the auto trial itself against an opt-in store trial of 7 days or longer. Do not tighten free limits across the board, because almost nobody reaches them.
- **What is at stake:** today about 2 verified purchases a month. Realistically, better paywall placement moves this to 4 to 8 a month, not to break-even (31 subscriptions at 39.99 zł, per the 2026-09-12 report). Retention is still the main constraint: only 7 of 37 accounts that ever paid still have premium.

---

## Key Metrics

| Metric | May | Jun | Jul | Aug | Sep (24d) | Trend | Benchmark | Read |
|---|---|---|---|---|---|---|---|---|
| MAU, full month | 246 | 218 | 162 | 144 | 111 | ▼ | - | concerning |
| MAU, first 24 days (like-for-like) | 211 | 189 | 130 | 129 | 111 | ▼ -47% | - | concerning |
| New app users | 213 | 174 | 116 | 101 | 73 | ▼ | - | concerning |
| Returning users (first seen in an earlier month), first 24 days | 30 | 42 | 37 | 39 | 38 | → flat | - | flat core |
| Avg WAU (Sun-start weeks) | ~68 | ~61 | ~47 | ~44 | ~42 | ▼ | - | concerning |
| Active days per active user | 1.63 | 1.57 | 2.02 | 2.14 | 2.05 | ▲ | - | improving |
| Sessions per active user | 2.27 | 2.46 | 3.27 | 3.17 | 3.11 | ▲ | - | improving |
| DAU/MAU (24-day window) | 6.6% | 6.2% | 8.2% | 8.3% | 8.6% | ▲ | ~10-20% typical consumer apps | low, improving |
| Users doing a core capture, % of MAU | 22.8% | 17.4% | 20.4% | 29.2% | 27.9% | ▲ | - | improving |
| Cohort D1 | 6.6% | 6.3% | 5.2% | 9.9% | 11.9% (n=67) | ▲ weak | 26-35% health/fitness | far below |
| Cohort W4 (day 22-28) | 6.1% | 2.9% | 3.4% | 8.4% (n=95) | n/a | ▲ weak | D30 ~3-4% | noisy |
| `paywall_shown`, users | n/a | n/a | n/a | ~6 | 4 | → | - | near zero |
| Active users who saw the paywall (last 30d) | | | | | 5/127 = 3.9% | | - | near zero |
| Verified purchases (DB, 30d to 09-12) | | | | | 2 | → | freemium 2.1% download-to-paid | far below |

---

## Findings

### F1: The user base shrank, intensity per user rose. · Impact: High · Confidence: High

- **Evidence**: comparable 24-day MAU went 211 -> 189 -> 130 -> 129 -> 111. New app users went 213 -> 174 -> 116 -> 101 -> 73 (Sep partial, a pace of about 91 per 30 days). The returning group stays at 30 to 42 people. Days per active user rose from 1.63 to 2.05-2.14, and sessions per user from 2.27 to 3.11. Query: `monthly_active`, `first24days_split_new_vs_returning`, `app_events_per_active_user` (Appendix A1-A3).
- **Part of the intensity gain is only a change in mix.** New users average 1.4 active days in their first month in every month except August (1.89). As new signups shrink, the average shifts toward the heavier returning users. Returning users themselves also got more active: 2.76 -> 2.41 -> 3.52 -> 2.72 -> **3.24 in only 24 days of September**. So the rise is partly real and partly mix.
- **So what**: "more usage per user" is true for a core of about 40 people. "Usage has grown" is false. The app is not growing. It is shrinking to a small, somewhat more engaged core.

### F2: Aug/Sep cohorts retain a bit better, but it is not proven yet. · Impact: Medium · Confidence: Low-Medium

- **Evidence**: D1 for Aug and Sep cohorts is 18/168 = 10.7%, against 31/503 = 6.2% for May to July (z about 1.9, p about 0.05). W4 for the August cohort is 8/95 = 8.4%, against 9/290 = 3.1% for June and July (p about 0.03), but May was 6.1%. The share of MAU doing any core capture rose from about 20% to 28-29%. Query: `cohort_retention` (A4).
- **So what**: this lines up with the August/September releases (first-capture prompt, workspace, app tour, Reflect entry). With single-digit numerators, 2 or 3 people can flip it. Re-read it on 2026-10-25 with the September and October cohorts before anyone calls it a trend.

### F3: The feeling of growth is a PostHog volume artifact. · Impact: Medium · Confidence: High

- **Evidence**: all non-web events went 15.1k (May) -> 18.6k (Jul) -> **97.5k (Aug)**, and persons went 183 -> **1,916**. Of the August persons, 1,859 exist only through backend events (`moment.sent`/`moment.expired` 17-24k, `weekly_summary_generated` 5.4k, `monthly_audit_generated` 2.8k). App events per user also doubled (39 -> 83), mostly because about 20 new client events were instrumented in August. Query: `raw_vs_app_monthly` (A5).
- **So what**: an unfiltered dashboard shows a 5x "growth" that does not exist. Read usage only from app persons (`$lib='posthog-flutter'`), and use days or sessions per user, not events per user.

### F4: The paywall almost never shows, and gates almost never send anyone to it. · Impact: High · Confidence: High

- **Evidence**:
  - `paywall_shown` has 16 events in its lifetime (first event 2026-08-16). August: drawer_menu 4 users, settings 1, premium_gate_reflect_messages 1. September: drawer_menu 3 users, premium_gate_session_recording 1.
  - `subscription_screen_opened` in September: drawer_menu 7 users, and premium_gate_reflect_voice, premium_gate_habits, premium_gate_monthly_audit and premium_gate_session_recording **1 user each**.
  - In the last 30 days, 5 of 127 active users (3.9%) saw the paywall and 10 (7.9%) opened the subscription screen.
  - Hours since signup at `paywall_shown`: <24h 2 users, 7-30 days 3, 30+ days 5. **Nobody sees it in onboarding.**
  - 403 gate hits on the backend: the Reflect monthly message limit was hit by 2 users in June and 2 in August, and 0 in September. Voice (realtime), habits and recording 403s each came from 1 user in September.
  - Queries: `paywall_by_month_trigger`, `reach_last30`, `paywall_hours_since_signup`, `api_403_by_endpoint_month` (A6-A8).
- **Code check**: there is **no onboarding paywall** (`triggerFeatureOnboarding` is defined but never used). `TrialPopupManager.handleTrialPopups()` and `canAddNote()` are **never called anywhere**, so the free-trial welcome, the "$5 14-day offer" and the trial-ended popup that routes to the paywall (`trial_ended_popup`) are all dead code. The only live entry points are the drawer menu, and the gate CTAs on Reflect voice and messages, recording, habits and monthly audit.
- **So what**: the operator's observation is correct. There is essentially no moment in the product where an average user meets an offer.

### F5: The automatic 4-day trial hides the free tier and the gates during the only days most people use the app. · Impact: Critical · Confidence: High on the mechanism, Medium on the size

- **Evidence (code)**: `POST /users/subscription` calls `_create_initial_subscription(db, uid, 4)` for every new account. This gives premium with `granted_via='signup_trial'` and no card or store trial. While premium is active, `SubscriptionCubit` suppresses `paywall_shown` (`_isPremiumAtOpen`), and every client gate and backend 403 passes.
- **Evidence (data)**: among registered users in the May to early-September cohorts, **only 107 of 365 (29.3%) are ever active on day 4 or later**. So **70.7% only ever experience the trial**, and 49% of all their active days fall inside the first 4 days. In September, among users whose events carry `is_premium` (n=23), **16 are premium, and 8 of those 16 are new this month**, which means they are on the trial.
- **So what**: the free version is not what most people use. What most people use is a premium trial that expires silently after they have already left. When the trial ends, nothing tells the few who come back that it ended or what they lost. There is also a design issue: the trial is shorter than one therapy cycle (1 to 2 weeks), which the 2026-09-12 report flagged.

### F6: Retained free users do not reach the limits. They mostly read. · Impact: High · Confidence: Medium (n=33)

- **Evidence**: take users first seen before 2026-08-20 and active 2026-08-26 to 09-24 (n=40). **33 free users average 1.73 active days in 30 days, and only 3 have 4 or more days.** 7 premium users average 11.4 days, and all 7 have 4 or more. What the free users did (distinct users out of 33): timeline 15, workspace 9, character card 8, bio 7, Reflect session 4, recording 3, subscription screen 3, paywall 2, prep card 2, habits 2, debrief 1, voice lock tap 1, Reflect limit hit 1. Query: `retained_free_vs_premium_feature_use` (A9).
- **So what**: a free user who opens the app on 1 or 2 days a month and reads their timeline never gets near 30 Reflect messages or 5 debriefs. Tightening those limits would change almost nothing. The part of the operator's intuition that holds up is that **what light users do get for free, reading their history, is never upsold**. The insight "depth" layer is soft-locked on the backend (`premium_locked` on goal AI narrative, health-check suggested questions, 30/90-day snapshots, hero insight cadence). In the client, I found an upgrade route only from monthly audit, habits, recording and Reflect. Those soft locks show no CTA.
- **Caveat**: the 7 heavy premium users may include team or test accounts (3 of the 16 September premium users are on TestFlight, and TestFlight subscriptions look like real ones in the DB). Treat "premium users are 6x more active" as a description of this group, not as an effect of premium.

### F7: Paying does not keep people either. · Impact: High · Confidence: Medium (DB baseline from 09-12)

- **Evidence**: 7 of 37 accounts that ever purchased still have active premium (18.9%). Active premium on 2026-09-12 was 18 accounts: 7 purchase, 8 signup_trial, 2 promo, 1 null. PostHog purchase completions were 5 users in August and 2 in September. The DB showed 2 verified receipts in the 30 days to 09-12.
- **So what**: more paywall exposure can raise first purchases, but with 19% paid retention each extra purchase is worth only a few months of revenue. Paywall work is worth doing because it is cheap. It will not rescue the business on its own.

---

## Root-Cause Analysis & Hypotheses

- **H1 (rejected): usage is growing.** Comparable MAU -47%, new users -53% (May to Aug), WAU 68 -> 42. What rose is per-user intensity in a flat core of about 40 people.
- **H2 (partly supported): users stay more often.** Days and sessions per user are up. Cohort D1 and W4 are up in August and September at borderline significance. Confidence is low until the October re-read.
- **H3 (supported): the paywall rarely shows.** 3.9% of MAU in 30 days, and 16 lifetime events.
- **H4 (mostly rejected as the main cause): a generous free tier removes the reason to pay.** Free users sit far below the limits. The dominant mechanisms are the auto trial (71% of registrants leave before it ends), missing offer moments (dead trial popups, no onboarding paywall, soft locks without a CTA) and early churn. Kept as a minor factor: the reading surfaces that light users value have no upsell.
- **H5 (supported, new): the auto trial suppresses the paywall exactly when most users are active.** Mechanism confirmed in code. Size confirmed in data (70.7% never active after day 4).
- **H6 (open): the gates are broken rather than unused.** Reflect limit hits come with 1,191 and 1,872 403 retries from 2 users a month, and recording initiate had 76 403 retries from 1 user. This looks like a client retry loop on 403 instead of a clean "limit reached" state. If so, users who do hit a gate may see an error instead of an offer. Needs a device check.

---

## Recommendations (prioritized by impact × confidence × effort)

1. **Put the paywall on the trial clock, which is the moment everyone passes through.** Wire the existing `TrialPopupManager` (it is fully built but never called):
   - on day 0, a "your 4 premium days" welcome that names what gets locked;
   - on day 3, a "trial ends tomorrow" prompt;
   - on the first open after expiry, a trial-ended screen that routes to the paywall with `trigger_feature=trial_ended_popup`.

   - **Expected effect**: paywall reach goes from 3.9% of MAU to most returning registrants. About 29% of roughly 70 registrants a month come back after day 4, and more are active on days 0 to 3. At a 2 to 5% conversion of those exposed, that is **+1 to +3 purchases a month on a base of about 2**.
   - **Owner**: `ui-ux-designer` (copy and timing, calm and non-coercive for a mental-health audience), then `flutter-mobile`.
   - **Measure**: share of each signup cohort with `paywall_shown`; purchases per 100 registrants from `subscription_receipts`; guardrail that D1 and W4 do not drop. Window: 2 monthly cohorts after release.
2. **Test the trial design: automatic 4-day premium vs no auto trial plus an opt-in store trial of 7 days or more, offered at the end of onboarding.** The current trial hides the product's limits during the only days most users are active, and it is shorter than one therapy cycle. Run a PostHog feature flag at 50/50 on new signups.
   - **Expected effect**: in the opt-in arm, paywall reach close to 100% of onboarding completers. Store trials with a payment method convert 30-50% trial -> paid (industry figure, not ours). Per RevenueCat, 55% of 3-day trial cancellations happen on day 0 and 39.8% of 7-day ones, so the first session decides.
   - **Risk**: first-session value drops for the control-less arm. Watch D1.
   - **Owner**: `backend-api` (grant logic behind a flag), `integration-devops` (store introductory offers), `flutter-mobile` (onboarding paywall with `trigger_feature=onboarding`, already in the taxonomy).
   - **Measure**: trial starts, trial -> paid from receipts, and D1/D7 per arm. Read after n of at least 100 per arm (about 3 months at the current inflow, so decide on direction, not on significance).
3. **Upsell where light users already look, instead of tightening limits they never reach.** Add an upgrade CTA with `premium_gate_<feature>` to the soft locks that already exist on the backend: goal AI narrative, health-check suggested questions, 30/90-day snapshots, and the hero insight refresh. Consider a "see the full picture" premium layer on timeline and workspace, which 15 of 33 retained free users open. Do **not** lower the 30-message, 5-debrief or 2-recording limits.
   - **Expected effect**: retained free users with at least 1 gate exposure in 30 days go from about 3/33 (9%) to more than 50%.
   - **Owner**: `ui-ux-designer` -> `flutter-mobile`.
   - **Measure**: that share, plus `paywall_shown` by `trigger_feature`.
4. **Fix the gate plumbing and the measurement holes before reading any conversion rate.**
   - (a) Investigate the 403 retry storms on `/reflect/{id}/message` and `/session-recordings/upload/initiate`. A gate should show an offer, not loop. Owner `flutter-mobile`.
   - (b) Emit `trial_started`/`trial_ended` (they have never flowed). Owner `backend-api`/`data-analytics`.
   - (c) Refresh the `subscription_tier` person property on every app open. Today it is stale and unset for 72% of MAU.
   - (d) Run the prepared prod query (below) so trial grants per signup month and the premium mix are confirmed from Postgres rather than from code.
   - **Expected effect**: a trustworthy paywall -> purchase funnel.
   - **Measure**: `trial_*` events flowing and `subscription_tier` set on at least 95% of MAU.
5. **Guardrail: keep retention as the North Star.** Every change above should be read against D1 on a 4-week rolling basis, with the existing target of 15% by 2026-12-12. Paying users churn too (7/37 kept), so the paywall only converts what retention delivers.

---

## Segments & Cohorts

| Segment (last 30d, first seen before 2026-08-20) | Users | Avg active days / 30d | Users with ≥4 days |
|---|---|---|---|
| Free | 33 | 1.73 | 3 (n<25, directional) |
| Premium (trial, promo or paid, incl. possible team/TestFlight) | 7 (n<25, directional) | 11.43 | 7 |

| Signup cohort (registered users) | n | Active on day 4+ (after trial) | % | Ever opened the subscription screen |
|---|---|---|---|---|
| May | 125 | 40 | 32.0% | 24 |
| Jun | 99 | 25 | 25.3% | 6 (n<25) |
| Jul | 51 | 13 (n<25) | 25.5% | 5 (n<25) |
| Aug | 72 | 24 (n<25) | 33.3% | 11 (n<25) |
| Sep (to 09-10) | 18 (n<25) | 5 | 27.8% | 1 |
| **Total** | **365** | **107** | **29.3%** | **47** |

Feature-level and gate-level counts in this report are almost all below 25 users. They are shown so the reader can see why no rate is claimed. Read them as directional only.

---

## Data Caveats & Confidence

- **Prod Postgres was not re-queried.** The read-only one-off dyno command was blocked by the session's permission system ("Production Reads"). The premium mix, receipts and paid retention come from the 2026-09-12 DB report. A ready read-only script (monthly signups, grants by `granted_via`, trial length, receipts, core-action tables, habits by premium) is at `C:\Users\mikol\AppData\Local\Temp\claude\C--Users-mikol-Notebooks-MindSync-Heroku\7668fffa-d4eb-47c7-9605-a84f1b1336d5\scratchpad\growth_20260925.py`. The operator can run it with `heroku run -a mindsync python < growth_20260925.py`.
- **The trial covering "every new account" is inferred from code** (`_create_initial_subscription(..., 4)` on `POST /users/subscription`). The DB check listed above would confirm the share per signup month.
- September is 24 days. Monthly comparisons use a first-24-days window where noted.
- PostHog ingest starts 2026-04-22, so the April and May "new users" include people who were already users. The May "returning" count is therefore understated.
- **Reflect message counts changed source mid-September.** Backend `reflect_message_sent` fell to 87 while client `reflect_message_submitted` rose to 384 (15 users, and the top 3 account for 58%). Reflect is compared on session starters (30/24/22/24/20 users a month), which is instrumented the same way throughout.
- `subscription_tier` and `is_premium` are partial and biased premium signals. They are set only on some events and include trials and possibly stale values.
- `paywall_shown` exists only from 2026-08-16. Earlier months cannot be compared.
- Correlation is not causation: the retention uptick and the higher premium activity are associations.

---

## Appendix

### Definitions
- **Active user**: a distinct `person_id` with at least one app event (`$lib='posthog-flutter'`), excluding `$device_model IN ('OnePlus8Pro','Pixel 6 Pro')` and `$is_emulator`.
- **Registered**: has a backend (`posthog-python`, excluding crons) event, or `user_registered`/`user_logged_in`.
- **D1**: active on first-seen day +1. **W1**: any day 1-7. **W4**: any day 22-28. A cohort is counted only once it is old enough for the window.
- **Core capture**: `reflect_session_started`, `debrief_created`, `prep_card_created`, `between_session_created`, `health_check_completed`, `symptom_scored`, `goal_created`.

### Queries (HogQL; `$F` = active-user filter above)
- **A1 monthly_active**: `SELECT m, uniq(pid), count(), count()/uniq(pid) FROM (SELECT toStartOfMonth(toDate(timestamp)) m, person_id pid, toDate(timestamp) d FROM events WHERE ... AND $F GROUP BY m,pid,d) GROUP BY m`
- **A2 first24days_split_new_vs_returning**: join daily activity (day of month ≤24) to `min(toDate(timestamp))` per person; new = first-seen month = activity month.
- **A3 app_events_per_active_user**: `count()`, `uniq(person_id)`, `uniq($session_id)` per month under `$F`.
- **A4 cohort_retention**: per person `max(if(dateDiff('day', f, d)=1,1,0))` for D1, `BETWEEN 1 AND 7` for W1, `BETWEEN 22 AND 28` for W4, with maturity cut-offs of 09-23, 09-17 and 08-27.
- **A5 raw_vs_app_monthly**: `count()`, `uniq(person_id)` split by `$lib`, excluding `web`.
- **A6 paywall_by_month_trigger**: events `paywall_shown`, `subscription_screen_opened`, `subscription_*`, `reflect_voice_locked_tapped`, `reflect_limit_hit` grouped by month and `trigger_feature`.
- **A7 reach_last30**: persons active 08-26 to 09-24 intersected with `paywall_shown` and `subscription_screen_opened` persons in the same window.
- **A8 api_403_by_endpoint_month**: `event='api_error' AND status_code='403'` by month and endpoint.
- **A9 retained_free_vs_premium_feature_use**: active 08-26 to 09-24, first seen before 08-20; premium = any `is_premium=true`, a backend `$set.subscription_tier='premium'` or a purchase since 08-20.
- **A10 post_trial_survival**: registered persons by first-seen month; `max(dateDiff('day', f, d) >= 4)`.

### Raw aggregates: core actions, distinct users per month (May / Jun / Jul / Aug / Sep 24d)
- `reflect_session_started`: 30 / 24 / 22 / 24 / 20
- `debrief_created`: 15 / 14 / 9 / 12 / 10
- `prep_card_created`: 14 / 13 / 8 / 7 / 5
- `between_session_created`: 9 / 9 / 11 / 11 / 11
- `health_check_completed`: 22 / 16 / 14 / 19 / 11
- `recording_saved`: n/a / n/a / 5 / 18 / 17
- `timeline_viewed`: 84 / 70 / 60 / 69 / 52
- `workspace_opened`: n/a / n/a / n/a / 37 / 36
- Habits (September only, instrumented 2026-09-13): 23 viewers, 6 check-togglers, and 5 habit creators, all 5 premium.

### Benchmarks
- Hard paywall vs freemium download-to-paid, 10.7% vs 2.1%, with one-year retention nearly identical; day-0 share of trial cancellations 55% (3-day), 39.8% (7-day): [RevenueCat State of Subscription Apps](https://www.revenuecat.com/state-of-subscription-apps), [RevenueCat 2026 trends](https://www.revenuecat.com/blog/growth/subscription-app-trends-benchmarks-2026)
- Health/fitness D1 26-35%, D30 3-4%: businessofapps.com health-fitness benchmarks (as used in the 2026-09-12 report)
- Store trial -> paid 30-50%: adapty.io trial conversion rates (as used in the 2026-09-12 report)
