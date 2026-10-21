# Acquisition Collapse After Week 2026-07-19 - Business Insight Report

- **Date**: 2026-08-10
- **Analyst**: growth-analyst
- **Business question**: Why did MindSync's new-user inflow collapse after the week of 2026-07-19, which channel drove the earlier level, and is it recoverable?
- **Data window**: 2026-06-07 → 2026-08-10 (weekly), 2026-07-01 → 2026-08-10 (daily); PostHog ingest starts 2026-04-22
- **Sources**: PostHog (proj 141170, EU) via read-only REST/HogQL · live marketing-site HTML + JS assets at `www.mindsync.app` (Webflow) · `db-reports/2026-08-10-subscription-pipeline-check.md` (revenue truth) · `analytics-reports/raw/2026-08-10-engagement-14d.md` · public consent-rate and Play-policy benchmarks
- **Confidence**: **High** on the cause (a timestamped artifact on the live site plus a perfectly aligned step change in exactly one data source). **Medium** on the size of any real traffic loss underneath it, because the unbiased counter (GA4) was not accessible from this session.

## Executive Summary

- **There was no acquisition collapse. A measurement channel was switched off.** On 2026-07-25 11:49 UTC a cookie-consent gate (`msconsent-1.0.0.js`) went live on the Webflow marketing site. It loads PostHog **only after the visitor clicks "Accept all" or ticks Analytics**. From 2026-07-26 onward, roughly 84% of marketing-site visitors stopped being recorded at all.
- **The "07-19 peak" was never an acquisition peak.** 102 of the 131 new persons in that week (78%) were marketing-site visitors (`$lib='web'`), not app users. Week 2026-07-19 (Sunday-start: 07-19 → 07-25) is simply **the last full week before the gate**, which is why the weekly series shows a clean cliff exactly at the week boundary.
- **App-side inflow did not fall - it rose.** New app persons per week: 27 (wk 07-19) → 26 (wk 07-26) → **32** (wk 08-02). Actives over 14d: app **80 → 92 (+15%)** while web went 183 → 27 (-85%). App WAU was flat at 49 → 50 → 48. `user_registered` went from a nine-week low of **7** in wk 07-19 to **24** in wk 08-02, the highest since 2026-06-07.
- **Top recommendation**: stop using PostHog `person_id` new-users/WAU as the acquisition metric - it conflates website visitors with app users and has produced a false alarm. Redefine acquisition as new persons with `$lib='posthog-flutter'` (or `user_registered`), and confirm real website traffic in GA4 (`G-DWNVZNWCT5`), which still fires **before** consent and therefore holds the unbiased series.
- **A real problem was found, but it is legal, not growth**: the consent gate is inverted. PostHog, Contentsquare, Google Ads and GTM are gated, while **GA4 and the Meta Pixel (`fbq('init', '1768966087001664')` + `fbq('track','PageView')`) still load unconditionally in `<head>` before any consent** - the higher-risk advertising category is the ungated one. This contradicts the site's own inline comment and needs a compliance ruling.
- Nothing here explains zero verified receipts since 2026-07-10. Monetization is a separate, still-open question (only 11 users opened `subscription_screen_opened` in 14d, and `paywall_shown` / `subscription_purchase_completed` do not exist as events).

## Key Metrics

| Metric | Wk 2026-07-19 | Wk 2026-08-02 | Trend | Benchmark | Read |
|--------|---------------|---------------|-------|-----------|------|
| New persons, all sources (PostHog `person_id`) | 131 | 46 | ▼ -65% | n/a | **misleading metric** |
| New persons, app only (`$lib='posthog-flutter'`) | 27 | 32 | ▲ +19% | n/a | healthy-but-small |
| New persons, web only | 102 | 11 | ▼ -89% | n/a | measurement artifact |
| WAU, all | 155 | 67 | ▼ -57% | n/a | misleading |
| WAU, app only | 49 | 48 | → -2% | n/a | flat |
| `user_registered` (distinct) | 7 | 24 | ▲ +243% | n/a | recovering |
| `onboarding_completed` (distinct) | 5 | 18 | ▲ +260% | n/a | recovering |
| Marketing-site visitors tracked / day | 13.4 (pre-gate mean, 07-13→07-25) | 2.1 (post-gate mean, 07-26→08-09) | ▼ -84% | avg banner accept-all 31%; bottom-bar banners 35-40% | **below benchmark** |
| Estimated analytics-consent rate | n/a | ~16% | new | 31% average, 25.4% accept-all on first interaction, 33.6% ignore the banner entirely | concerning |
| Measurable web → app attribution | 0 of 725 web-first persons since 06-07 | 0 | → | n/a | **not instrumented** |

Benchmarks: [Cookie Consent 2026 accept/reject rates](https://termsandconditionstemplate.com/cookie-consent-statistics-2026), [Cookie consent rates by industry 2026](https://kukie.io/blog/cookie-consent-rates-industry-benchmarks), [banner best practice / design effects](https://elementor.com/blog/cookie-consent-banner-best-practices/).

## Findings

### F1 - The inflow series was ~75% marketing-site visitors, and only that part collapsed · Impact: Critical · Confidence: High

**Evidence** - new persons per Sunday-start week, split by the SDK that emitted their first event:

| week | new persons | app (`posthog-flutter`) | web only | other |
|---|---|---|---|---|
| 2026-06-07 | 112 | 49 | 63 | 0 |
| 2026-06-14 | 123 | 43 | 76 | 4 |
| 2026-06-21 | 213 | 94 | 117 | 2 |
| 2026-06-28 | 137 | 37 | 98 | 2 |
| 2026-07-05 | 114 | 37 | 75 | 2 |
| 2026-07-12 | 98 | 20 | 78 | 0 |
| **2026-07-19** | **131** | **27** | **102** | 2 |
| **2026-07-26** | **41** | **27** | **13** | 1 |
| 2026-08-02 | 46 | 34 | 11 | 1 |
| 2026-08-09 (partial) | 10 | 7 | 2 | 1 |

Web-only new persons fell 102 → 13 (-87%) between consecutive weeks. App new persons fell 27 → 27 (0%). The same split on activity rather than first-seen (query `AB`/`AC`): actives over the last 14d = 126 total (92 app, 27 web) vs 265 in the previous 14d (80 app, 183 web). **App activity grew 15% across exactly the window in which the headline metric halved.**

**So what**: every downstream conclusion drawn from the all-sources series is wrong by construction. The reported "17/90 new users return (18.9%)" is also diluted: on the app-only cohort it is **14/61 = 23.0%** for the last 14d versus **9/47 = 19.1%** for the prior 14d - i.e. new-user return actually improved slightly.

### F2 - The cause is a cookie-consent gate that went live 2026-07-25 11:49 UTC · Impact: Critical · Confidence: High

**Evidence** - the live page at `https://www.mindsync.app/` contains this comment in `<head>`:

> `<!-- Analytics and advertising tags (PostHog, Contentsquare, Google Ads, GTM, Meta) now load only after cookie consent, via the MsConsent script in site settings. Do not paste tracker snippets here; add them to the consent script instead. -->`

and loads `https://cdn.prod.website-files.com/676ed8d44b863915ae191f41/6a64a2ac4d90955d5c396842_msconsent-1.0.0.js`. That script initialises PostHog **only inside `loadAnalytics()`**, which is called only from `applyC(c)` when `c.a` is truthy, and `c` is written only by a click on "Accept all" or "Save choices" with the Analytics checkbox ticked (the checkbox is **unticked by default**). A visitor who ignores the banner is never tracked.

The Webflow asset id `6a64a2ac...` is a MongoDB ObjectID whose 4-byte timestamp prefix decodes to **2026-07-25 11:49:00 UTC**. Daily tracked pageview users: `07-24: 6`, `07-25: 23`, **`07-26: 2`**, `07-27: 3`, `07-28: 1`. 2026-07-25 is the last day of the Sunday-start week labelled 2026-07-19 - which is exactly why the weekly series looks like a peak followed by a cliff.

Everything else about web tracking is unchanged, ruling out the alternatives:

| check | before 07-26 | after 07-26 | reading |
|---|---|---|---|
| `$session_entry_host` | `www.mindsync.app` (173 users) | `www.mindsync.app` (28 users) | same site, still live |
| `$lib` | `web` | `web` | SDK still present, not removed |
| entry paths | `/`, `/privacy-policy`, `/terms-conditions`, `/faq` | same set | no routing/site change |
| user-agent class | 100% "normal" (no headless/bot/python markers) | 100% "normal" | not a bot-filter change |
| `$os` / device | Desktop 174 users, Mobile 70 | Desktop 12, Mobile 17 | desktop -93%, mobile -76% |
| `posthog-flutter` events | 6,149 / 79 users | 6,424 / 97 users | app SDK unaffected, so not a project quota or billing limit |

**So what**: this is a self-inflicted blind spot, not lost demand. It also means the residual web numbers are a ~16% consented sample and must never be compared to pre-07-26 levels.

### F3 - The channel behind the pre-gate web volume was organic search plus direct, not a campaign · Impact: High · Confidence: High

**Evidence** - `$referring_domain` on `$pageview`, per week, was consistently `$direct` (37-46 users/wk) and `www.google.com` (23-35 users/wk), with a long tail of Bing/Brave/DuckDuckGo/Facebook at 1-5 users. Country/device for new web persons in 07-12→07-25: **US Desktop 82**, IN Mobile 16, US Mobile 15, IN Desktop 8, everything else ≤4. Paid attribution is effectively absent across the whole series: pageviews carrying `gclid` were 1, 1, 2, 5, 0, 1, **6**, 0, 2, 1 per week, and `utm_source` identical. `app_store_click` was 2-9 per week for the entire period.

**So what**: there is nothing to "bring back" - no campaign was switched off, and the 07-19 week (97 tracked web users) sits inside the normal band of the four preceding weeks (91, 74, 77, 97). Also: the Google Ads tag `AW-17877628667` and GTM `GTM-5CTMS8S7` are installed but there is essentially no `gclid` traffic, so paid acquisition is configured and unused.

### F4 - PostHog cannot attribute a single app install to the website · Impact: High · Confidence: High

**Evidence**: of 725 persons since 2026-06-07 whose first event came from `$lib='web'`, **0 ever emitted an app event**. Measurable store intent from the site was 1-9 `app_store_click` per week (and that event is itself now consent-gated, since `msconsent.js` fires it only when `window.__msA` is set). In-app self-reported `lead_source` (`onboarding_lead_source_selected.source_value`) names `app_store` as the top source every week, with `therapist` jumping to 7 users in wk 2026-08-02; the option set does not include a website/search option.

Caveat: the 0 is partly a mechanical limit - a visitor who installs the app gets a fresh `person_id`, so cross-device stitching is impossible without an install-referrer. Read it as "web contribution is unmeasurable", not "web contributes nothing".

**So what**: even with perfect web tracking, the website series was never an acquisition metric. The genuine gap is install attribution.

### F5 - The consent gate is inverted relative to risk · Impact: High (legal) · Confidence: High

**Evidence** - still loading unconditionally in `<head>`, before any consent interaction: GA4 (`gtag('config','G-DWNVZNWCT5')` plus a Google first-party tag proxy at `/nvhc9u4gxsag.../MOi6FWrF...`) and the **Meta Pixel** (`fbq('init','1768966087001664'); fbq('track','PageView')`). Inside `msconsent.js`, the store-click handler also fires `fbq('track','Purchase', {...})` guarded only by `window.fbq` existing - not by the advertising-consent flag `window.__msM`. Meanwhile the *analytics* tools (PostHog, Contentsquare) and Google Ads/GTM are correctly gated.

**So what**: the site is losing its own product analytics while still firing an advertising pixel pre-consent. That is the worst of both worlds and directly contradicts the comment the author left in the head. It needs a compliance ruling before the banner is "optimised" for higher opt-in.

### F6 - The one genuinely weak week was app-side and it already recovered · Impact: Medium · Confidence: Medium (small n)

**Evidence**: distinct `user_registered` per week: 20, 15, 18, 14, 11, 10, **7**, 10, **24**, 4(partial). `onboarding_started`: 18, 13, 17, 11, 11, 7, **6**, 8, **23**. So app-side signups declined gradually through July, bottomed in the very week being investigated, and then tripled. The 2.0.75 rollout (new app persons first seen on it from wk 07-26: Android 18, iOS 4) and 2.0.76 (from wk 08-02: Android 11, iOS 2) coincide with the recovery, not with a decline.

**So what**: whatever the 07-19 dip was, the last two weeks are the strongest app-side signup weeks since early June. There is no live fire here.

## Root-Cause Analysis & Hypotheses

- **H1 (SUPPORTED, high confidence) - a consent gate on the marketing site stopped PostHog web tracking.** Supporting: timestamped asset `msconsent-1.0.0.js` at 2026-07-25 11:49 UTC; code path proves PostHog init is consent-conditional with Analytics unticked by default; tracked web users drop 84% on 07-26 with identical host, paths, SDK and user-agent profile; app and backend SDKs unaffected. Contradicting: nothing found. **Verdict: this is the cause of the observed metric collapse.**
- **H2 (REJECTED) - app installs / store acquisition collapsed.** New app persons 27 → 27 → 34 across the boundary; app actives +15%; `user_registered` 7 → 10 → 24; `onboarding_completed` 5 → 6 → 18. Mid-July Play policy changes (announced 2026-07-15, covering child safety, health-claim disclosure and third-party store listings) would not produce a one-day cliff, and no app-side cliff exists to explain. **Verdict: rejected.**
- **H3 (REJECTED) - a release (2.0.75 on 07-25, 2.0.76 on 08-04) broke signup or consent.** The new signup events (`signup_started`, `signup_method_selected`, `consent_screen_viewed`, `consent_granted`, `welcome_cta_tapped`) only begin appearing 2026-08-04 to 08-05, i.e. **after** the drop, so they cannot have caused it; and where they do appear, `signup_started` → `user_registered` runs 1:1 per day (e.g. 08-06: 4 started, 4 registered; 08-07: 4 and 3). Registrations rose after both releases. **Verdict: rejected as a cause; the new signup instrumentation is a welcome addition, not a suspect.**
- **H4 (REJECTED) - PostHog ingest problem, quota limit, or bot filtering.** `posthog-flutter` volume rose (6,149 → 6,424 events) and `posthog-python` rose sharply (1,583 → 7,674) in the same windows, so ingest is healthy and no project-level cap is in force. All `$pageview` user-agents classify as "normal" on both sides of the boundary, so no bot filter removed a bot wave. **Verdict: rejected.**
- **H5 (OPEN, medium confidence) - some real website traffic was also lost.** A banner adds friction; a bottom-bar consent banner can plausibly depress store-click-through. Cannot be resolved inside PostHog because the only remaining web sample is the ~16% who consented. **It is resolvable in one step**: GA4 `G-DWNVZNWCT5` and the Meta Pixel still fire pre-consent, so they hold the unbiased 2026-07-01 → 2026-08-10 series. Until that is checked, assume the underlying traffic is roughly flat (the most likely case given nothing else about the site changed) but do not assert it.
- **H6 (NOT ADDRESSED HERE) - the revenue stall.** Zero verified receipts since 2026-07-10 is not explained by anything in this report; the acquisition and engagement series both improved across that boundary. Separate investigation needed.

## Recommendations (prioritized by impact × confidence × effort)

1. **Retire the all-sources `person_id` metric; define acquisition as app-only.** Any "new users", "WAU", "actives", "retention" or "activation" figure must filter `properties.$lib = 'posthog-flutter'` (or count `user_registered`). Publish the corrected series (new app persons/week: 37, 38, 20, 27, 26, 32) as the baseline. Owner: **growth-analyst** for the definitions, **data-analytics** if the 9 existing dashboards need the filter added to Account Health / Onboarding Health / Core Engagement tiles. Expected effect: removes a 3x distortion in the headline number and prevents repeat false alarms; measured by the corrected series appearing on the dashboards within one week.
2. **Confirm real website traffic in GA4 (`G-DWNVZNWCT5`) for 2026-07-01 → 2026-08-10, daily.** GA4 loads pre-consent, so it is the unbiased counter. If GA4 sessions are flat across 07-25/26, the collapse is 100% measurement and this file closes. If GA4 also drops, escalate to an SEO/traffic investigation. Owner: **integration-devops** (site/GA access) with the operator. Expected effect: converts H5 from open to resolved within a day; success = a daily sessions series pasted into this report's appendix.
3. **Get a compliance ruling on the inverted consent gate, then fix the ordering.** Meta Pixel (`fbq init` + `PageView`, and the `Purchase` event on store clicks) and GA4 currently fire before consent while analytics tools are gated. Owner: **security-guardian** to rule (GDPR Art. 6 / ePrivacy, EU visitors present: PL, DE, NL, IE, GB, FR in the pre-gate mix), then **integration-devops** to move `fbq` and GA4 behind the advertising/analytics flags in the Webflow site settings and to gate the `fbq('track','Purchase')` call on `window.__msM`. Expected effect: removes the pre-consent advertising-tracker exposure; success = no `connect.facebook.net` or `googletagmanager` request on a fresh load with no stored consent.
4. **Recover top-of-funnel measurement.** Two independent moves, both cheap: (a) restore a consent-exempt aggregate view counter (Webflow/Cloudflare edge logs or server-side aggregate counting - no cookies, no person profiles) so total sessions are always known regardless of consent; (b) once (3) is settled, improve banner opt-in - the current bottom bar with an unticked Analytics box yields ~16% versus a 35-40% bottom-bar and 55-60% centre-modal benchmark. Owner: **integration-devops** (site) + **ui-ux-designer** (banner layout/copy), gated on **security-guardian** sign-off. Expected effect: tracked-visitor share from ~16% toward 35%+; measured as weekly `$pageview` distinct persons against the GA4 session count from (2).
5. **Instrument install attribution - this is the real acquisition gap.** PostHog cannot connect a single web visit to an install (0 of 725). Add the Google Play Install Referrer API (and an iOS deferred deep link / campaign parameter) at first launch and set it as a person property, so `utm_source`/store-listing/referral becomes a weekly number. Complement it by extending the in-app `lead_source` option set (currently `app_store`, `friend`, `social_media`, `therapist`, `other`) with a website/search option. Owner: **flutter-mobile** (client capture + `$set`), **integration-devops** (deep-link infra). Expected effect: attribution coverage from 0% to >60% of new installs within two releases; measured by share of new app persons carrying a non-null install-source property.
6. **Open a separate monetization investigation.** Zero verified receipts since 2026-07-10 with only 11 users reaching `subscription_screen_opened` in 14d, and `paywall_shown` / `subscription_purchase_completed` not emitted at all. The paywall funnel is currently unmeasurable end to end. Owner: **flutter-mobile** to emit `paywall_shown` (with `trigger_feature`) and `subscription_purchase_completed`; then **growth-analyst** for the funnel read against `subscription_receipts`. Expected effect: makes paywall → purchase conversion measurable for the first time.

## Segments & Cohorts

Weekly cohort totals are business aggregates and are reported in full. Sub-segments below 25 users are reported only where they are event/property counts rather than identifiable cohorts, and are labelled.

- **Where the "collapse" lives**: web-first persons, i.e. marketing-site visitors. 102 of 131 new persons in wk 07-19 (78%); 13 of 41 in wk 07-26 (32%); 11 of 46 in wk 08-02 (24%).
- **Device inside the web segment**: the loss is concentrated in **US Desktop** new web persons, 82 (07-12→07-25) → 5 (07-26→08-09). Mobile fell less hard (IN Mobile 16 → 4, US Mobile 15 → 4; each n<25, directional only). Consistent with desktop visitors dismissing or ignoring a bottom-bar banner.
- **Where the app segment stands**: new app persons 26 (wk 07-26) and 32 (wk 08-02) versus 27 (wk 07-19). Platform mix of new app persons in wk 08-02: Android 15, iOS 5 (both n<25, directional). Version mix of new app persons: 2.0.75 dominant from wk 07-26, 2.0.76 from wk 08-02.
- **Suppressed**: per-country app-user cohorts, `lead_source` values (max 7 users per value per week), and all therapy-loop stage segments - all n<25.

## Data Caveats & Confidence

- **Person counts drift between query runs.** My weekly totals differ by 2-24 persons from the series in the task brief (e.g. wk 06-14: 123 here vs 147 there). PostHog retroactively merges `person_id`s when `$identify` fires, so absolute person counts are not stable across runs. The step change and all ratios are far larger than this drift and are unaffected.
- **`toStartOfWeek` in this project is Sunday-start.** "Week 2026-07-19" spans Sun 07-19 → Sat 07-25. The consent script landed on the final day of that week, which is the entire reason the weekly view reads as "peak then cliff". Anyone re-cutting this by ISO (Monday-start) weeks will see the boundary shift by one day.
- **The post-07-26 web sample is self-selected (~16% who consented) and small (2-4 users/day).** It cannot be compared to pre-gate levels, and cannot be used to answer whether real traffic changed.
- **H5 remains open.** GA4 and Meta were not queried from this session (no credentials in scope). The claim "underlying website traffic is roughly flat" is an inference from the absence of any other change, not a measurement. Ahrefs GSC and Web Analytics tools returned `Insufficient plan`, so no independent organic-traffic series was obtainable.
- **`$lib`-based classification is a proxy for platform.** `posthog-flutter` = app, `web` = marketing site, `posthog-python` = backend-emitted (no `$os`/`$app_version`). A handful of persons emit `$os='Linux'` with an `$app_version` (1-2/week) - most likely emulators or CI; too small to matter.
- **Correlation vs causation.** F2 is unusually strong for an observational finding: a dated code artifact, a mechanism visible in source, a one-day step change, and four falsified alternatives. It is still not an experiment. The decisive test is recommendation (2).
- **`app_store_click` is now consent-gated too**, so post-07-26 store-intent counts are not comparable either.
- No PII, therapy content, raw symptom or health scores, emails, UIDs, or secret values appear in this report. Public site identifiers (GA4 measurement id, Meta Pixel id, Google Ads id, PostHog public project token) are visible in the site's own client-side HTML and are not secrets; no personal API key value was read out.

## Appendix

### Queries used

All run read-only via `python scripts/posthog_query.py --sql-file <file>` against PostHog project 141170.

```sql
-- @@ A_weekly_new_users_web_vs_app  (F1)
SELECT toStartOfWeek(first_ts) AS wk, count() AS new_users,
  countIf(app_ev > 0) AS app_users,
  countIf(app_ev = 0 AND web_ev > 0) AS web_only_users,
  countIf(app_ev = 0 AND web_ev = 0) AS other_users
FROM (
  SELECT person_id, min(timestamp) AS first_ts,
    countIf(event IN ('$screen','user_registered','onboarding_started','app_tour_started',
      'welcome_cta_tapped','tab_switched','signup_started','user_logged_in',
      'onboarding_legal_gate_gate_ready')) AS app_ev,
    countIf(event IN ('$pageview','$pageleave','$web_vitals','$autocapture','app_store_click','$rageclick')) AS web_ev
  FROM events WHERE timestamp > toDateTime('2026-04-22 00:00:00') GROUP BY person_id
) WHERE first_ts >= toDateTime('2026-06-07 00:00:00') GROUP BY wk ORDER BY wk

-- @@ V_wau_by_week_split_by_lib  (F1)
SELECT toStartOfWeek(timestamp) AS wk, count(DISTINCT person_id) AS wau_all,
  count(DISTINCT if(properties.$lib = 'posthog-flutter', person_id, NULL)) AS wau_app_flutter,
  count(DISTINCT if(properties.$lib = 'web', person_id, NULL)) AS wau_web,
  count(DISTINCT if(properties.$lib = 'posthog-python', person_id, NULL)) AS wau_backend
FROM events WHERE timestamp >= toDateTime('2026-06-07 00:00:00') GROUP BY wk ORDER BY wk

-- @@ AB / AC_actives_14d_split  (F1)
SELECT count(DISTINCT person_id) AS all_14d,
  count(DISTINCT if(properties.$lib='posthog-flutter', person_id, NULL)) AS app_14d,
  count(DISTINCT if(properties.$lib='web', person_id, NULL)) AS web_14d
FROM events WHERE timestamp > now() - INTERVAL 14 DAY;
-- prev14d variant: WHERE timestamp <= now() - INTERVAL 14 DAY AND timestamp > now() - INTERVAL 28 DAY

-- @@ Y_new_app_persons_by_week  (F1, F6)
SELECT toStartOfWeek(first_ts) AS wk, count() AS new_app_persons FROM (
  SELECT person_id, min(timestamp) AS first_ts FROM events
  WHERE timestamp > toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter'
  GROUP BY person_id
) WHERE first_ts >= toDateTime('2026-06-07 00:00:00') GROUP BY wk ORDER BY wk

-- @@ AD / AE_app_only_new_cohort_retention  (F1)
SELECT count() AS cohort_size, countIf(distinct_days > 1) AS returned_any_later_day,
  countIf(days_span >= 7) AS active_7d_plus
FROM (
  SELECT person_id, min(timestamp) AS first_ts, count(DISTINCT toDate(timestamp)) AS distinct_days,
    dateDiff('day', toDate(min(timestamp)), toDate(max(timestamp))) AS days_span
  FROM events WHERE timestamp > toDateTime('2026-04-22 00:00:00') AND properties.$lib='posthog-flutter'
  GROUP BY person_id HAVING first_ts > now() - INTERVAL 14 DAY
)  -- prev14d: HAVING first_ts > now() - INTERVAL 28 DAY AND first_ts <= now() - INTERVAL 14 DAY

-- @@ G / Z_daily_web_events_around_cliff  (F2)
SELECT toDate(timestamp) AS d, countIf(event='$pageview') AS pv,
  count(DISTINCT if(event='$pageview', person_id, NULL)) AS pv_users,
  countIf(event='$autocapture') AS ac, countIf(event='$web_vitals') AS wv, countIf(event='$pageleave') AS pl
FROM events WHERE timestamp >= toDateTime('2026-07-05 00:00:00')
  AND event IN ('$pageview','$autocapture','$web_vitals','$pageleave')
GROUP BY d ORDER BY d

-- @@ H / I / J / K / P  before-vs-after 07-26 invariance checks  (F2)
SELECT if(timestamp < toDateTime('2026-07-26 00:00:00'),'before_0726','after_0726') AS period,
  properties.$session_entry_host AS host, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event='$pageview' AND timestamp >= toDateTime('2026-07-12 00:00:00')
GROUP BY period, host ORDER BY period, c DESC
-- same shape with: properties.$lib / properties.$lib_version, properties.$device_type,
-- properties.$session_entry_pathname, and a multiIf() classifier over
-- positionCaseInsensitive(toString(properties.$raw_user_agent), 'headless'|'bot'|'python'|'chrome-lighthouse')

-- @@ T_lib_inventory_before_after  (F2, rules out ingest/quota)
SELECT if(timestamp < toDateTime('2026-07-26 00:00:00'),'before_0726','after_0726') AS period,
  properties.$lib AS lib, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp >= toDateTime('2026-07-12 00:00:00') GROUP BY period, lib ORDER BY period, c DESC

-- @@ F / Q_pageview_referring_domain_by_week  (F3)
SELECT toStartOfWeek(timestamp) AS wk, properties.$referring_domain AS ref,
  count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event='$pageview' AND timestamp >= toDateTime('2026-06-28 00:00:00')
GROUP BY wk, ref ORDER BY wk, users DESC

-- @@ W_utm_and_gclid_by_week  (F3) -- note: JSONHas, not `!= ''`
SELECT toStartOfWeek(timestamp) AS wk, countIf(JSONHas(properties,'utm_source')) AS has_utm_source,
  countIf(JSONHas(properties,'gclid')) AS has_gclid, countIf(JSONHas(properties,'fbclid')) AS has_fbclid,
  count() AS pv_total
FROM events WHERE event='$pageview' AND timestamp >= toDateTime('2026-06-07 00:00:00') GROUP BY wk ORDER BY wk

-- @@ U_web_new_persons_by_country_before_after  (Segments)
SELECT if(first_ts < toDateTime('2026-07-26 00:00:00'),'before_0726','after_0726') AS period, cc, dt,
  count() AS new_web_persons
FROM (
  SELECT person_id, min(timestamp) AS first_ts,
    argMin(properties.$geoip_country_code, timestamp) AS cc,
    argMin(properties.$device_type, timestamp) AS dt, argMin(event, timestamp) AS first_event
  FROM events WHERE timestamp > toDateTime('2026-04-22 00:00:00') GROUP BY person_id
) WHERE first_ts >= toDateTime('2026-07-12 00:00:00')
  AND first_event IN ('$pageview','$autocapture','$web_vitals','$pageleave')
GROUP BY period, cc, dt ORDER BY period, new_web_persons DESC

-- @@ O_web_first_persons_conversion  (F4)
SELECT toStartOfWeek(first_ts) AS wk, count() AS web_first_persons,
  countIf(app_ev > 0) AS later_app, countIf(store_click > 0) AS clicked_store
FROM (
  SELECT person_id, min(timestamp) AS first_ts,
    countIf(properties.$lib='posthog-flutter') AS app_ev,
    countIf(event='app_store_click') AS store_click,
    argMin(properties.$lib, timestamp) AS first_lib
  FROM events WHERE timestamp > toDateTime('2026-04-22 00:00:00') GROUP BY person_id
) WHERE first_ts >= toDateTime('2026-06-07 00:00:00') AND first_lib='web' GROUP BY wk ORDER BY wk

-- @@ L_lead_source_by_week  (F4)
SELECT toStartOfWeek(timestamp) AS wk, properties.source_value AS src,
  count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event='onboarding_lead_source_selected' AND timestamp >= toDateTime('2026-06-07 00:00:00')
GROUP BY wk, src ORDER BY wk, users DESC

-- @@ AF_registered_and_onboarding_by_week  (F6)
SELECT toStartOfWeek(timestamp) AS wk,
  count(DISTINCT if(event='user_registered', person_id, NULL)) AS registered,
  count(DISTINCT if(event='onboarding_started', person_id, NULL)) AS onb_started,
  count(DISTINCT if(event='onboarding_completed', person_id, NULL)) AS onb_completed
FROM events WHERE timestamp >= toDateTime('2026-06-07 00:00:00')
  AND event IN ('user_registered','onboarding_started','onboarding_completed')
GROUP BY wk ORDER BY wk

-- @@ N_signup_and_consent_daily  (H3)
SELECT toDate(timestamp) AS d, event, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp >= toDateTime('2026-07-12 00:00:00')
  AND event IN ('signup_started','signup_method_selected','signup_failed','user_registered',
    'consent_screen_viewed','consent_granted','onboarding_started','onboarding_completed','welcome_cta_tapped')
GROUP BY d, event ORDER BY d, event
```

Non-PostHog evidence:

```bash
# F2 - live site + the consent asset (read-only fetches)
curl -sL https://www.mindsync.app/ -o site.html
curl -sL "https://cdn.prod.website-files.com/676ed8d44b863915ae191f41/6a64a2ac4d90955d5c396842_msconsent-1.0.0.js"

# F2 - date the asset: Webflow asset ids are MongoDB ObjectIDs; first 4 bytes = unix seconds
python -c "import datetime; print(datetime.datetime.utcfromtimestamp(int('6a64a2ac',16)))"
# -> 2026-07-25 11:49:00 (UTC)
```

### Metric & segment definitions

- **New person (week W)** = `person_id` whose earliest event in `events` (bounded to ingest start 2026-04-22) falls in week W. Weeks are `toStartOfWeek`, Sunday-start.
- **App person** = emits at least one event with `properties.$lib = 'posthog-flutter'`. **Web-only person** = emits web events (`$pageview`/`$pageleave`/`$web_vitals`/`$autocapture`/`$rageclick`/`app_store_click`) and never an app event.
- **Tracked visitor (post 2026-07-26)** = a marketing-site visitor who granted Analytics consent. Not comparable to a pre-gate visitor.
- **Estimated analytics-consent rate** = post-gate mean daily `$pageview` distinct persons (2.13, 07-26→08-09) / pre-gate mean (13.4, 07-13→07-25) = 15.9%. Assumes underlying traffic unchanged - see H5.

### Raw aggregates

Daily new persons, 2026-07-01 → 2026-08-10 (total / app / web-only):

`07-01 14/4/10 · 07-02 27/9/18 · 07-03 20/2/17 · 07-04 19/7/12 · 07-05 18/8/10 · 07-06 19/5/14 · 07-07 21/4/17 · 07-08 19/6/13 · 07-09 15/5/8 · 07-10 13/5/8 · 07-11 9/4/5 · 07-12 6/4/2 · 07-13 16/2/14 · 07-14 16/2/14 · 07-15 19/4/15 · 07-16 9/0/9 · 07-17 21/6/15 · 07-18 11/2/9 · 07-19 16/5/11 · 07-20 15/5/10 · 07-21 23/3/20 · 07-22 19/4/14 · 07-23 18/3/15 · 07-24 13/3/9 · 07-25 27/4/23 · **07-26 5/3/2** · 07-27 4/2/2 · 07-28 4/3/1 · 07-29 4/2/2 · 07-30 10/7/2 · 07-31 7/5/2 · 08-01 7/5/2 · 08-02 2/2/0 · 08-03 9/6/2 · 08-04 9/6/3 · 08-05 9/6/3 · 08-06 6/5/1 · 08-07 7/6/1 · 08-08 4/3/1 · 08-09 8/5/2 · 08-10 2/2/0 (partial)`

Daily tracked `$pageview` distinct persons, 2026-07-20 → 2026-08-05:

`07-20 10 · 07-21 21 · 07-22 15 · 07-23 12 · 07-24 6 · 07-25 23 · **07-26 2** · 07-27 3 · 07-28 1 · 07-29 2 · 07-30 2 · 07-31 2 · 08-01 2 · 08-03 3 · 08-04 4 · 08-05 3`

Raw extracts referenced: `analytics-reports/raw/2026-08-10-engagement-14d.md`, `analytics-reports/raw/2026-08-10-errors-quality-14d.md`, `db-reports/2026-08-10-subscription-pipeline-check.md`.
