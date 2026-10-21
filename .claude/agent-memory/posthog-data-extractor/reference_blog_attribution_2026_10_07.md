---
name: reference-blog-attribution-2026-10-07
description: Blog -> app install attribution in PostHog: which events/props to query, what flows (2026-10-07), web PostHog is consent-gated, google-play referrer is the Play default
metadata:
  type: reference
---

Blog -> app attribution taxonomy, verified 2026-10-07 (first week after blog store links were tagged 2026-10-01).

- `app_install_attributed` (posthog-flutter, app 2.0.86+): props `install_source`/`install_medium`/`install_campaign`/`install_referrer_raw`/`platform`, also `$set_once` person props of the same names. Fires once per install, INCLUDING existing users after upgrade and reinstalls (297 events / 197 people over 5 weeks), so it is not a clean new-install count. ~5-17 people/day.
- `install_source='google-play'`, medium `organic` = Play's DEFAULT referrer for an untagged store install. Dominant value. iOS is always `organic_or_unknown` (no referrer API); `apps.facebook.com`/`fb4a` small.
- Blog tag would show as `install_source='blog'`, campaign = post slug. As of 2026-10-07: 0 ever (events and persons table).
- Onboarding survey: `onboarding_lead_source_selected.properties.source_value='blog'` first seen week 2026-10-04 (n<25).
- Web: PostHog on www.mindsync.app exists (`$lib='web'`), but loads only after cookie consent -> ~30 pageviews/week total, journal posts single digits. Far below GSC. `app_store_click` (prop `store` only, no slug) is the legacy site event; `blog_store_click` (from Webflow script, needs `window.__msA`) never registered as of 2026-10-07.
- web person_ids never overlap app person_ids (0/74) - cross-device join impossible by design.

**How to apply:** re-run `analytics-reports/raw/2026-10-07-blog-attribution.md` queries; iOS blog installs only via App Store Connect Campaigns (`ct=blog-<slug>`), not PostHog.
