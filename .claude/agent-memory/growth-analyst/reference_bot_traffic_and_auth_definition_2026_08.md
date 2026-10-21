---
name: bot-traffic-and-auth-definition-2026-08
description: THE two biggest denominator traps in MindSync PostHog - automated device-farm traffic (OnePlus8Pro/Pixel 6 Pro, 24% of the cohort) and the wrong "authenticated" definition. Plus the signup-wall funnel baselines.
metadata:
  type: reference
---

# Bot traffic + correct auth definition (verified 2026-08-10, task B11)

Report: `analytics-reports/2026-08-10-anonymous-users-analysis.md`

## TRAP 1 - automated (non-human) traffic inflates every top-of-funnel number by ~26%

**Always exclude `$device_model IN ('OnePlus8Pro','Pixel 6 Pro')` from any app cohort before 2026-07-26.**

- `OnePlus8Pro`: **131 person_ids on ONE model**, 94.7% never authenticate, avg session **223 s**,
  Android 11, US geoip, **locale rotated** across en-NZ/en-SG/en-US/en-BE/en-TT/en-CA/en-AU/en-NG/en-ZA/en-IE/en-JM/en-PH/en-GB.
  Screens visited: only `splash`, `auth`, `signUp`(3), `forgotPassword`(3). Zero product screens.
- `Pixel 6 Pro`: 28 persons, 27 anon, en-US/US/Android 12.
- **The killer evidence: `OnePlus8Pro` appears on 28 distinct `$app_version`, `Pixel 6 Pro` on 25,
  while ALL 556 real-device persons combined appear on only 19.** One robot run per uploaded build,
  including builds no human ever installed. Versions 2.0.38-2.0.43 / 2.0.45-2.0.58 have 0-1 real users
  and 3-7 bot persons each.
- Arrival clusters at 11:00 UTC. Traffic **stopped after 2026-07-19** (0 from week 07-26).
- Behaviour matches Google's documented pre-launch report (US devices, locale rotation, ~5 min crawl,
  one run per release) BUT **neither model is in the Feb-2026 public Firebase Test Lab catalog** -
  source is unconfirmed. Settle it by opening Play Console -> Pre-launch report device list.
- Official suppression hook if it IS Test Lab: `Settings.System.getString(cr,"firebase.test.lab")=="true"`.
- Emulator/TestFlight flags exist but are tiny: only 15 persons in the whole 652 cohort
  (`$is_emulator` 11, `$is_testflight` 4). They are NOT the problem; the device farm is.

## TRAP 2 - "authenticated" must include backend events

Wrong: `has user_registered OR user_logged_in`. Right: **`... OR any event with $lib='posthog-python'`**.
- `user_registered` is **backend-only, starts 2026-05-06**; `user_logged_in` is **client-only**.
  A user who registered before 05-06 or logged in on an old build emits NEITHER.
- 62 of the 652 cohort were misclassified this way. Proof they are real accounts: their `api_error`
  rows are **404** on token-required endpoints (`/prep-cards/latest`, `/debriefs/latest`,
  `/health-check/latest`) - 404 means "no card yet", not "no user"; only 1x 403 in the whole group.
- Backend emits ONLY in the context of a recognised user - that is why the rule works.

## $identify merge artifact is SMALL (~4%), do not spend effort on it

- `AuthCubit` calls `Posthog().identify()` (`auth_cubit.dart:43-74`) and the client passes its
  distinct_id to the backend, so client+backend land on ONE person_id. Verified: **0 registered persons
  have orphaned backend events**. 145 registered have one shared UUID id; 60 have UUID + 28-char
  Firebase UID merged under one person.
- Residual artifact = 19 of 478 (4.0%): anon persons with `onboarding_*` / `user_logged_out` /
  `onboarding_completed`, i.e. re-installs and post-logout identities.
- **`$device_id` is NOT collected** (0 of 24 412 client events) - per-device dedup is impossible.
  Estimate the artifact structurally: distinct_id shape (`match(did,'^[0-9a-f]{8}-')` = anon UUID vs
  `length(did)=28` = Firebase UID) + post-auth event footprint.

## Corrected baselines, cohort 2026-05-01..07-26 (clean, human-only)

| metric | old (dirty) | CORRECT |
|---|---|---|
| new app-first persons | 652 | **478** |
| never authenticated | 66.0% (430/652) | **45.0% (215/478)** |
| genuine signup-wall bounce (minus 19 artifacts) | - | **41.0% (196/478)** |
| authenticated | 31.4% | **55.0% (263/478)** |
| activation 24h / all new persons | 17.0% (111/652) | **22.6% (108/478)** - above Amplitude P90 (21%) |
| activation 24h / authenticated | 41.5% | **41.1%** (robust, keep for OKR) |

Clean funnel: open 478 -> reach `auth` screen 343 (71.8%) -> account 263 (76.7% of those reaching auth).
**The bigger leak is BEFORE the auth screen (28.2%), not on it (23.3%).**
Anon profile: 58.1% stay <15 s / 1.4 events; 69.8% one session; **30.2% return 2+ times and still never register**.
Of the authenticated, 39.2% authenticate later than 1 h after first open (46 after >7 days).
Geography of the bounce: India 75/215 (34.9% of all bounces, 60% of the IN cohort), BD 18/25, US 21/75.
India reaches `auth` MORE often (54.7% vs 37.9% RoW) but almost nobody continues - they see the wall and stop.

## Signup wall: there is ZERO value before auth (code-verified)

- `/` -> `splash` (forced >=3 s, `splash_screen.dart:56-59,95`) -> `user==null` -> `/welcome`.
- Welcome = logo + ONE tagline + "Log in" + "Sign up". No guest/skip/preview.
  **Zero hits for `signInAnonymously|isAnonymous|guest|demoMode|skipAuth` in all of `lib/`.**
- Onboarding (legal gate + 8 profiling steps) is AFTER account creation (`sign_up_cubit.dart:144-224`).
- Email path also forces: Terms checkbox, personalise form, **mandatory email verification (5 s polling)**,
  4 s success splash, legal gate with 2 checkboxes.
- iOS shows Apple only, Android Google only (`animated_google_apple_widgets.dart:100-104`).

## $screen_name gotcha - the welcome screen is INVISIBLE

`PosthogObserver` reads `route.settings.name`; routes built with `pageBuilder:` have no `name:`.
**`welcome` and `wow` emit NO `$screen` at all** (`ms_routes.dart:208-228`, `:384-402`), so welcome-screen
activity is attributed to `$screen_name='splash'`. A splash->auth drop IS the welcome drop, but you cannot
split "never saw welcome" from "rejected welcome". `signUp` covers 3 sub-views; `therapyOnboarding` covers 9 pages.

## Pre-auth funnel events - only usable from 2026-08-05

`welcome_cta_tapped` (2026-08-04, has `cta`=log_in|sign_up), `signup_started`, `signup_method_selected`
(has `method`=oauth|email; Aug split 11 oauth vs n<6 email), `consent_screen_viewed` (2026-08-05),
`signup_failed` (2026-08-10). **`login_failed` does not exist** - so we cannot tell whether the 80 people
who reached the auth screen and left failed or chose not to.

## HogQL gotchas added this session

- An aggregate cannot contain an aggregate: compute per-person flags in a subquery, `sum()` outside.
- The outer alias must NOT repeat the inner column name (`sum(saw_splash) AS saw_splash` -> `illegal_aggregation`).
- `greatest()` takes exactly 2 args; for OR over many flags use `if(a+b+c+d>0,1,0)`.
- `toInt()` works, `toUInt8()` does not (re-confirmed).

## Benchmarks worth reusing (and the fakes to refuse)

- Amplitude 2025: D1 activation median 5%, P90 21%. Mixpanel 2024: week-1 retention 28%.
- CleverTap 2023: 21% of installers sign up within a week; **70% of signups happen within 75 s of first launch**.
- Duolingo via First Round 2017: moving the signup screen back a few steps = **~20% DAU increase**. Best citation for delaying a wall.
- Baymard: 18% of abandoners cite "wanted me to create an account" (older waves said 24-26%).
- NN/g optional-registration: authoritative for the PRINCIPLE, publishes **no number** - anyone quoting "NN/g says X%" is fabricating.
- **NO credible benchmark exists** for: Android vs iOS signup completion, mandatory email-verification cost,
  number of social providers (Corbado says so explicitly). Argue qualitatively, measure in-house.
- Refuse these (no primary source, SEO blogs citing each other): "signup wall loses 20-40%",
  "registration requirement +56% abandonment", "social login +20-40%", "Duolingo 8.2% DAU".
