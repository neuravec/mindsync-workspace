---
name: acquisition-baselines-2026-08
description: App-only acquisition/activation baselines per week (Jun-Aug 2026) - the corrected series to compare future pulls against, plus trusted consent-rate benchmarks.
metadata:
  type: reference
---

# App-only acquisition baselines, 2026-06 -> 2026-08

Corrected series (filter `properties.$lib = 'posthog-flutter'`; Sunday-start weeks).
Use THESE, not the all-sources person counts - see [[posthog-web-vs-app-split]].

| week (Sun) | new app persons | app WAU | user_registered | onboarding_started | onboarding_completed |
|---|---|---|---|---|---|
| 2026-06-07 | 48 | 68 | 20 | 18 | 14 |
| 2026-06-14 | 45 | 72 | 15 | 13 | 6 |
| 2026-06-21 | 94 | 118 | 18 | 17 | 11 |
| 2026-06-28 | 37 | 60 | 14 | 11 | 9 |
| 2026-07-05 | 38 | 58 | 11 | 11 | 8 |
| 2026-07-12 | 20 | 42 | 10 | 7 | 5 |
| 2026-07-19 | 27 | 49 | **7 (9-week low)** | 6 | 5 |
| 2026-07-26 | 26 | 50 | 10 | 8 | 6 |
| 2026-08-02 | 32 | 48 | **24 (high)** | 23 | 18 |

- Actives 14d, app only: 80 (prev14d) -> **92** (last14d ending 2026-08-10). Web: 183 -> 27.
- New-app-cohort D1+ return: **14/61 = 23.0%** (last14d) vs 9/47 = 19.1% (prev14d). The
  frequently quoted "18.9% (17/90)" was diluted by web persons - do not reuse it.
- Self-reported `lead_source` (`onboarding_lead_source_selected.source_value`): `app_store`
  is #1 every week (1-7 users/wk); `therapist` spiked to 7 users in wk 2026-08-02. Option set
  = app_store / friend / social_media / therapist / other (**no website/search option**).
- `app_store_click` from the marketing site: only 1-9 per week all period (and consent-gated from 07-26).
- App-version adoption by NEW app persons: 2.0.60 through wk 07-19, 2.0.75 from wk 07-26, 2.0.76 from wk 08-02.

## Trusted benchmark sources
- Cookie-consent accept rates: <https://termsandconditionstemplate.com/cookie-consent-statistics-2026> (avg 31%; 25.4% accept-all on first interaction; 33.6% ignore the banner), <https://kukie.io/blog/cookie-consent-rates-industry-benchmarks>, <https://elementor.com/blog/cookie-consent-banner-best-practices/> (bottom bar 35-40% vs centre modal 55-60%; US lowest at 32%, PL highest at 64%).
- Google Play policy announcement 2026-07-15 (child safety, health-claim disclosure, third-party store listings) - checked and **not** a cause of any mid-July app-side change.

## Reports
- `analytics-reports/2026-08-10-acquisition-collapse.md` - verdict: the "collapse" was the
  2026-07-25 consent gate hiding marketing-site traffic; app inflow flat-to-up. Open follow-up:
  verify true site traffic in GA4 `G-DWNVZNWCT5` (loads pre-consent).
