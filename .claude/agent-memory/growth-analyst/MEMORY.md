# growth-analyst memory

Persistent, project-scoped notes for the Growth & Product Analyst. Keep this file
under 200 lines; move detail into topic files in this directory.

## What to record here (one line each, link to topic files for detail)
- Which planned events ACTUALLY flow vs only exist in POSTHOG_ANALYTICS_PLAN.md.
- Baseline metrics per period (activation %, D7/D30 retention, paywall→purchase,
  trial→paid, MRR, AI gross margin) so anomalies are detectable next time.
- Reusable HogQL / SQL query patterns that worked.
- Canonical segment/cohort definitions (e.g. "activated" = first debrief within 3d).
- Trusted external benchmark sources.
- Recurring findings + which recommendations shipped and what they moved.

## Verified facts
- PostHog: EU Cloud, project 141170. 9 dashboards exist (see reference_posthog_dashboards).
- **Never count users without splitting `properties.$lib`** – the same project ingests the
  Webflow marketing site (`web`, ~75% of "new persons" pre-2026-07-26) alongside the app
  (`posthog-flutter`) and the backend (`posthog-python`). See topic file; this trap already
  produced one false "acquisition collapse" alarm.
- **But `$lib='posthog-flutter'` is NOT a universal app filter**: `reflect_message_sent` /
  `reflect_session_started` (and other backend-emitted events) are `posthog-python` – that filter
  silently zeroes them and fakes a "not flowing" result. For app-inclusive counts use `$lib != 'web'`.
- **`moment.sent` recipients (1815) are NOT active users.** Crons fan out to the whole historical
  account base; backend-touched population runs ~15x MAU. Same class of trap as `$lib`.
- **Before calling a feature "unused", grep the client for `isPremium` on its entry path** – a
  premium-gated feature judged against all-users is guaranteed to look dead. Real premium base
  is **16-18** (`is_active AND end_date > now()`), not 34. See premium-gate topic file.
- Revenue ground truth = `subscription_receipts` (Apple/Google verified). AI cost
  ground truth = `token_usage_log` × `model_pricing` – **except realtime voice, which is
  architecturally unmeasurable** (client→OpenAI direct); $0 there means unmeasured, not free.
- **`subscription_receipts` has NO amount, NO currency, NO environment column** – you cannot compute
  MRR from the DB, and a TestFlight/sandbox receipt is indistinguishable from a production one.
- Map of intended instrumentation: `POSTHOG_ANALYTICS_PLAN.md` (12 scenarios, ~89 events).
- **Exclude `$device_model IN ('OnePlus8Pro','Pixel 6 Pro')` from every app cohort before 2026-07-26** –
  159 person_ids (24% of the 652 cohort) are an automated device farm, not humans. One robot run per
  uploaded build: OnePlus8Pro appears on 28 distinct `$app_version` vs 19 for ALL real devices combined.
  `$is_emulator`/`$is_testflight` catch only 15 persons and are NOT sufficient. See bot-traffic topic file.
- **"Authenticated" = `user_registered` OR `user_logged_in` OR ANY `$lib='posthog-python'` event.**
  The first two alone misclassify 62 real accounts as anonymous (`user_registered` is backend-only from
  2026-05-06; `user_logged_in` is client-only). Backend emits only for recognised users, so it is the tell.
- **`$device_id` is NOT collected** (0 of 24 412 client events) – per-device dedup is impossible;
  estimate `$identify` merge artifacts from distinct_id SHAPE (uuid vs 28-char Firebase UID) instead.

## Topic files (index)
- [Multi-angle baselines 2026-10-15](reference_multi_angle_baselines_2026_10_15.md) - 8-extract synthesis: strict MAU ~80, 60d funnel 296->94->71, fr/ar/fa wave, post-03.10 gains, moment.opened/purchase double-count traps.
- [Retention priorities 2026-10-03](reference_retention_priorities_2026_10_03.md) - day-0 lift table, push spent on summary-ready (97%), new low-intent Play wave since 09-20 (segment!), offer-skip risk.
- [Usage trend + paywall exposure 2026-09-25](reference_usage_trend_paywall_2026_09_25.md) - MAU -47% May->Sep but flat ~40 returning core; paywall reach 3.9% MAU; auto 4-day trial hides gates (71% leave before it ends); trial popups dead code.
- [Baselines + unit economics 2026-09-12](reference_baselines_2026_09_12.md) – **START HERE for any money/retention question.** D1 7.5/D7 4.0/D30 0.8; 7 real payers; paid-user retention 7/37=19% (kills the "fix the paywall" reflex); 97% of AI spend on push-generated content; break-even formula + scenarios; the frequency-mismatch thesis.
- [PostHog access fallback](reference_posthog_access.md) – MCP OAuth BROKEN here; query HogQL read-only via REST `/query/` + `POSTHOG_PERSONAL_API_KEY` from `MindSync/.env` (never print it). Prefer `scripts/posthog_query.py --sql-file` (sections split on `-- @@ label`). GOTCHAS: `properties.X != ''` matches MISSING keys (use JSONHas); `persons` table count unreliable; no PG driver in session.
- [Flowing events + baselines](reference_posthog_flowing_events_baselines.md) – ~81 events flow; gaps (paywall_shown, conversation_*, level_up, account_deleted, v2 recording funnel); `api_error` ~80% benign 404; onboarding 8-step taxonomy; 2026-06 baselines; app_version telemetry.
- [Web vs app person split + 2026-07-25 consent gate](reference_posthog_web_vs_app_split.md) – THE metric trap; `$lib` filter mandatory; Sunday-start weeks; person counts drift on `$identify` merges; web tracking consent-gated from 2026-07-26 (never compare `$pageview` across that date); GA4/Meta still fire pre-consent; Ahrefs GSC = "Insufficient plan".
- [App-only acquisition baselines 2026-06..08](reference_acquisition_baselines_2026_08.md) – corrected weekly new-app-persons / app WAU / registrations series + consent-rate benchmark sources.
- [Activation definition + lift table 2026-08](reference_activation_definition_2026_08.md) – CANONICAL activation = >=1 therapy-loop capture within 24h of first open (41.5% of registered); window discipline, per-candidate lift, emitter map (backend-only captures), `toInt()` not `toUInt8()`.
- [Premium gates + correct denominators](reference_premium_gated_features_2026_08.md) – 4 known `premiumGateTrigger` gates; premium base 16 (NOT 34, NOT PostHog's 2); gate hits emit NOTHING and `subscription_screen_opened` has no `trigger_feature` → demand for gated features is unmeasurable today.
- [Bot traffic + correct auth definition 2026-08](reference_bot_traffic_and_auth_definition_2026_08.md) – THE denominator trap: OnePlus8Pro/Pixel 6 Pro device farm (24% of cohort, 28 app versions); correct `authenticated` rule; clean baselines (478 cohort, 41% signup-wall bounce, 22.6% activation); `welcome`/`wow` emit NO `$screen`; signup-wall benchmarks + the fake ones to refuse.
- [AI cost model + traps 2026-08](reference_ai_cost_model_2026_08.md) – 30d AI spend $117.30; `SYSTEM` = 93% unaudited; text baseline $0.524/user/60d; realtime cost invisible (estimate from duration × $0.06–0.11/min); `REALTIME_VOICE` label over-attributes text Reflect; missing `model_pricing` rows silently cost $0.

## Analyses run
- 2026-06-29 – Post-update health check (build 2.0.60+133, published ~06-27).
  Report: `analytics-reports/posthog_post_update_2026_06_29.md`. Verdict: no fire, no
  rollback; update niemierzalny po 2 dniach (new build was on testers pre-27, public
  still on 2.0.44; calendar before/after confounded by weekend + QA spike 06-21..25).
  Positives: `/chunk` 503 and voice 500s vanished. Top reco: instrument the v2
  recording funnel (only `recording_chunked_upload_completed` flows).
- 2026-06-29 – Onboarding: are added profiling fields filled?
  Report: `analytics-reports/posthog_onboarding_fields_2026_06_29.md`. Answer: core
  steps filled (88–99% step→step); **`lead_source` effectively NOT filled (~6 users)**;
  data lands in POSTGRES not PostHog – `currently_in_therapy`/`lead_source` deliberately
  NOT sent to PostHog (Art.9 consent / re-identification, per models.py). PostHog shows
  only that a field was IN the write payload, not that its VALUE is non-empty → per-field
  fill truth needs a Postgres `user_profile` SELECT (given in report; not run – no PG driver).
  Gaps: `therapy_context_updated.updated_section` null for all 808 ev; no Art.9/consent event.
- 2026-08-10 – "New-user inflow collapsed after week 07-19": **FALSE ALARM, cause found.**
  Report: `analytics-reports/2026-08-10-acquisition-collapse.md`. The collapse is entirely
  marketing-site persons disappearing from PostHog because a cookie-consent gate
  (`msconsent-1.0.0.js`, live 2026-07-25 11:49 UTC) now loads PostHog only after "Accept all".
  App-side inflow FLAT-TO-UP across the boundary (new app persons 27→26→32; app actives
  80→92; `user_registered` 7→10→24). No campaign ever existed (gclid ≤6 pv/week). Web→app
  attribution is 0/725, i.e. not instrumented. Top recos: (1) redefine acquisition as
  `$lib='posthog-flutter'`; (2) verify true site traffic in GA4 `G-DWNVZNWCT5` (pre-consent,
  owner integration-devops) – **still open**; (3) security-guardian to rule on the inverted
  gate (Meta Pixel + GA4 fire pre-consent while analytics is gated); (5) add Play Install
  Referrer attribution (flutter-mobile). Revenue stall since 07-10 is NOT acquisition-related
  and needs its own investigation (paywall funnel unmeasurable: no `paywall_shown`, no
  `subscription_purchase_completed`).
- 2026-08-10 – Activation metric defined empirically (cohort n=652 app persons, 05-01..07-26).
  Report: `analytics-reports/2026-08-10-activation-definition.md`. Answer: **Activated = >=1
  therapy-loop capture within 24h of first app open** (set of 17 events across 9 categories).
  Baseline 41.5% of registered / 17.0% of all new app persons. Activated return d2-7 25.2% vs
  7.4% (3.41x, p<0.0001), d8-28 21.7% vs 7.7%, >=2 active weeks 35.7% vs 13.7%. **`onboarding_completed`
  REJECTED as activation** (onb-only 11.4% vs onb+capture 25.8%); threshold is ONE capture (dose-response
  is a step, not a ramp); no single capture type beats the set. TTFV is NOT the problem (median 4 min);
  80.5% never capture and 66% never even authenticate. Instrumentation verdict: **derived metric, NOT a
  client-side `user_activated`** (3 of 9 capture categories are backend-only). Top recos: (1) ship derived
  insight+cohort; (2) `flutter-mobile` add `first_capture_prompt_shown/_dismissed` – we cannot tell if the
  non-capturers were ever asked; (3) fix the 66% auth-screen bounce (ui-ux-designer + flutter-mobile);
  (4) A/B the first-capture prompt to prove causality; (5) server-side `user_activated` + `activated_at`
  person props (data-analytics); (6) retest notification-permission + recording candidates after 2026-09-15.
- 2026-08-10 – **B7: is realtime voice chat worth further investment? → KEEP, DON'T INVEST; block Gemini Live.**
  Report: `analytics-reports/2026-08-10-voice-chat-assessment.md`. Detail: [[voice-chat-b7-verdict]].
  11 lifetime users / 65 sessions (4 are TestFlight testers, 2 ever paid); `audioChat` 18th of 22 screens;
  39% of sessions <30s; nothing since 2026-08-04 and never on build 2.0.76. **Root cause is NOT
  discoverability** (mic sits permanently in the Reflect composer) – it is a **premium gate** against
  16 active subscriptions, on a feature absent from all 10 paywall benefit strings. Cost: realtime is
  UNMEASURED (client→OpenAI direct); estimated $10–80 lifetime from ~140–175 min × $0.06–0.11/min ⇒
  **$1–7 per voice user lifetime** vs $0.524/user/60d for text ⇒ migration ROI is deeply negative.
  Top recos: (1) freeze Gemini Live; (2) `flutter-mobile` emit `premium_gate_hit` + `trigger_feature`
  (the only number that decides the feature); (3) 30-min check for a 2.0.76 entry-point regression;
  (4) **gate 2026-09-10**: ≥25 gate-hitters/mo → promote, <10 → sunset; (5) `data-analytics` split the
  mis-attributed `REALTIME_VOICE` label; (7) deliberately DEFER building realtime cost instrumentation
  until the feature survives the gate. Separate bigger lead: `SYSTEM` = 93% of AI spend, unaudited.
- 2026-08-10 – **B11: the "66% never authenticate" figure is WRONG → real signup-wall bounce is 41%.**
  Report: `analytics-reports/2026-08-10-anonymous-users-analysis.md`. Detail: [[bot-traffic-and-auth-definition-2026-08]].
  Decomposition of the 430 "anonymous": 151 automated device-farm persons (OnePlus8Pro 124 + Pixel 6 Pro 27,
  35.1%), 62 misclassified authenticated users (14.4%), 2 emulator/TestFlight, **215 real humans (50%)** of whom
  19 are `$identify` re-install artifacts ⇒ **196/478 = 41.0% genuine bounce**. The `$identify` artifact feared in
  the audit plan is real but only 4% – `AuthCubit` does call `identify()` and merging works (0 registered persons
  have orphaned backend events). Clean funnel: 478 open → 343 reach `auth` (71.8%) → 263 accounts (76.7%);
  **the bigger leak (28.2%) is BEFORE the auth screen** and is invisible because the `welcome` route has no
  `name:` so it emits no `$screen`. Signup wall stands before ALL value (zero `signInAnonymously|guest|demoMode`
  in `lib/`; onboarding is post-account; email path forces mandatory verification). Corrected activation:
  22.6% (108/478) of all new persons – **above Amplitude's P90 (21%)**, so activation is fine, admission is not.
  Top recos: (1) `integration-devops` read the Play Console pre-launch device list, then filter the farm;
  (2) `flutter-mobile` add `name:'welcome'`/`name:'wow'` to the routes (blocks any before/after measurement);
  (3) `ui-ux-designer`+`flutter-mobile` rebuild the welcome screen as a 50/50 A/B, then Firebase anonymous
  trial (`signInAnonymously`+`linkWithCredential`) – **blocked on a `security-guardian` Art.9 ruling**;
  (4) drop mandatory email verification; (6) add `login_failed` (does not exist – we cannot tell refusal
  from failure for the 80 who reached the wall and left). Also corrects two earlier reports' denominators.
- 2026-09-12 – **Operator's core question: "why don't we earn, is the direction wrong, do people only use free?"
  → NOT a paywall problem, a retention problem, and specifically a FREQUENCY MISMATCH.**
  Report: `analytics-reports/2026-09-12-diagnoza-retencja-monetyzacja.md`. Baselines: [[baselines-and-unit-economics-2026-09-12]].
  Decisive evidence: **7 of 37 accounts that ever PAID still have premium (18.9%)** – people who cleared the
  paywall churn too, so monetization work is wasted until retention moves. D1 7.5 / D7 4.0 / D30 0.8% (2 of 244);
  68.5% have one active day per month; 67.9% of accounts never had a conversation. Onboarding is FINE (76.7%,
  minimal step drop) – the leak is after it: ~50% never create an account, then 0.0% of churners touched
  workspace or recording in W0. **96.8% of AI spend ($108.54 of $112.13) generates content FOR users**
  (NOTIFICATION 82%) opened by 1.4%; therapeutic AI costs $0.07. 4319 empty-state 404s vs 173 "Your Session"
  events = 25:1 – people come to LOOK at a mirror that is empty. Free gates sit above where users ever reach
  (5 debriefs/mo vs median 2.5 events; 2 free recordings vs median 1.0), and 5 of 7 paywall views came from
  people hunting for it in the menu ⇒ tightening free or raising price changes nothing. Break-even needs
  25-61 subs depending on price (unknown – no amount column); at 0.38% conversion that is 9+ years of
  acquisition, so **cost-cutting is the only fast lever**. Top recos: (A1) stop generating AI notifications
  for accounts inactive 30/90d = **-345 to -405 zł/mo, ~45% of total burn, zero product risk**; (A2) same for
  weekly/monthly summaries (7233 generated, 49 viewed); (B1) resolve `conversation_*` dead since 2026-08-11
  – **the only gap that can invert a headline number**; (B2) instrument Habit Tracker (only daily-loop feature,
  zero events); (B3) fix unexpected 404s on `/users/get_user_profile_and_subscription` (38 users) and
  `/users/therapy-context` (40); (B9) 4-day trial is SHORTER than the 1-2 week product loop. North Star set:
  **D1 on a 4-week rolling basis, threshold 15% by 2026-12-12, below 12% → maintenance mode.**
- 2026-09-25 - **Operator: "usage grew + paywall never shows because free is too generous?"** -> usage PARTLY (people -47%, intensity up); paywall-never-shows TRUE (3.9% MAU); free-too-generous MOSTLY FALSE: auto 4-day trial + dead trial popups + light free users. Report `analytics-reports/2026-09-25-usage-trend-and-paywall-exposure.md`. Detail: [[usage-trend-and-paywall-exposure-2026-09-25]].
- 2026-10-03 - **Operator: what to fix for retention + subscriptions?** -> retention loses in days 2-7: 80% do nothing on day 0, push spent on summary-ready to dormant accounts, Home not adapted for non-therapy users, no daily loop/reward. Monetization: verify post-onboarding offer actually shows, outcome-led paywall + CTAs on read surfaces, Reflect is the only binding limit. Report `analytics-reports/2026-10-03-retencja-subskrypcje-priorytety.md`. Detail: [[retention-priorities-2026-10-03]].
- 2026-10-15 - **8 PostHog extracts merged** -> biggest loss is pre-onboarding (68% of new), then day 2; redesign 03.10 lifted onboarding 47->74% but retention not yet measurable; 09-15.10 changes TestFlight-only. Report `analytics-reports/2026-10-15-posthog-multi-angle.md`. Detail: [[multi-angle-baselines-2026-10-15]].
