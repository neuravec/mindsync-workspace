---
name: posthog-web-vs-app-split
description: CRITICAL metric trap - PostHog person_id counts mix marketing-site visitors with app users; always split by properties.$lib. Plus the 2026-07-25 cookie-consent gate that killed web tracking.
metadata:
  type: reference
---

# PostHog person counts are NOT app users - always split by `$lib`

## The trap (cost one full false-alarm investigation, 2026-08-10)
Project 141170 ingests **three** SDKs into the same `events` table:
- `properties.$lib = 'posthog-flutter'` -> the mobile app (real users)
- `properties.$lib = 'web'` -> the **Webflow marketing site** `www.mindsync.app` (visitors, never installers)
- `properties.$lib = 'posthog-python'` -> backend-emitted (no `$os`/`$app_version`)

Marketing-site visitors were **~75% of all "new persons"** through July 2026. Any
`count(DISTINCT person_id)` metric (new users, WAU, actives, retention cohorts,
activation denominators) is therefore ~3x inflated and can move for reasons that have
nothing to do with the app. **Every user-count query MUST carry a `$lib` filter or a
`$lib` split.** `$os = 'Linux'/'Windows'/'Mac OS X'` is the same signal by a weaker proxy.

Web persons and app persons **never** stitch: 0 of 725 web-first persons since 2026-06-07
ever emitted an app event (fresh `person_id` after install). So PostHog cannot attribute
a single install to the website - install attribution is simply not instrumented.

## Canonical definitions to reuse
- new app persons (week W) = `person_id` whose min(timestamp) over `$lib='posthog-flutter'` falls in W, bounded `timestamp > toDateTime('2026-04-22')` (ingest start).
- `toStartOfWeek` here is **Sunday-start** (verified: 2026-08-02 is a Sunday). Week "2026-07-19" = Sun 07-19 .. Sat 07-25.
- person counts **drift 2-24 between runs** because `$identify` retroactively merges `person_id`s. Never treat absolute person counts as reproducible; ratios and step changes are.

## 2026-07-25: cookie-consent gate broke web tracking (permanent, by design)
`msconsent-1.0.0.js` (Webflow asset id `6a64a2ac...` = **2026-07-25 11:49 UTC**) now loads
PostHog + Contentsquare + Google Ads + GTM **only after a click on "Accept all"** (Analytics
checkbox unticked by default; ignoring the banner = never tracked). Effect from 2026-07-26:
tracked web visitors -84% (13.4 -> 2.1/day), i.e. an estimated **~16% analytics-consent rate**
(benchmark: 31% average, 35-40% for bottom-bar banners). `app_store_click` is consent-gated too.
=> **Never compare web `$pageview` numbers across 2026-07-26.** Post-gate web data is a
self-selected ~16% sample.

Still firing **pre-consent** (so usable as an unbiased traffic counter, and a compliance
problem): GA4 `G-DWNVZNWCT5` + Google first-party tag proxy, and Meta Pixel
`fbq('init','1768966087001664')` + `fbq('track','PageView')`. Webflow asset ObjectIDs are
datable: `python -c "import datetime;print(datetime.datetime.utcfromtimestamp(int('<first8hex>',16)))"`.

## Tooling notes
- Ahrefs MCP GSC + Web Analytics + management-projects tools return `Insufficient plan` on this account. No independent organic-traffic series available from Ahrefs.
- `JSONHas(properties,'utm_source')` for presence (NOT `!= ''`). `gclid`/`utm_source` appear on <=6 pageviews/week: there is effectively **no paid traffic**, despite `AW-17877628667` + `GTM-5CTMS8S7` being installed.

See also [[posthog-access-fallback]], [[posthog-flowing-events-baselines]], [[acquisition-baselines-2026-08]].
