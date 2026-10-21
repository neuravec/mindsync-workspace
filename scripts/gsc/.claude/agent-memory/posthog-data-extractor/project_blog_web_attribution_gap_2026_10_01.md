---
name: project-blog-web-attribution-gap-2026-10-01
description: Blog (mindsync.app/journal) traffic is tiny and cannot be tied to app installs in PostHog; what flows vs doesn't on web+attribution side
metadata:
  type: project
---

Verified 2026-10-01 (60d window, 2026-08-02 -> 2026-10-01): mindsync.app sends web events
(`$pageview`, `$autocapture`, `$pageleave`, `$web_vitals`) via posthog-js, all on host
`www.mindsync.app` (no bare `mindsync.app` rows — consistent with the www->root 301 from the
2026-08-26 SEO fix, [[reference-webflow-seo-gotchas]]). Volume is very low: 114 unique visitors
site-wide / 60d, only 7 unique visitors on `/journal/*` / 60d, 3 on `/blog` listing.

**Custom CTA event `app_store_click` exists and fires** (store=google/apple, 12 events/10 users
in 60d) but every single occurrence came from `/` or `/about` — zero from `/journal/*` or
`/blog`. Plain `$autocapture` on outbound store links carries null `$el_text`/`href` for this
project's config, so non-CTA outbound link clicks from blog pages are structurally invisible
(not "zero", just unmeasured).

**Identity stitching web->app is architecturally absent.** Intersected person_id between
/journal/ pageview viewers and any `$lib='posthog-flutter'` event in the same 60d window:
0 matches. posthog-js (web) and posthog-flutter (app) are separate instances with no shared
anonymous-id bridge or `identify()` call tying a web visit to an app account. This question is
unanswerable from PostHog as currently instrumented, not just empirically zero — don't re-run
this check expecting a different structural answer without a known instrumentation change.

**App-side acquisition attribution properties are NOT flowing at all**, 0 of millions of app
events in 60d: `utm_source`, `utm_campaign`, `$referrer` (app-side), `install_referrer`. The
Flutter app does not send or capture these.

**What DOES exist for self-reported source**: `onboarding_lead_source_selected` event,
property `source_value` (NOT `lead_source` — check props before guessing property names).
Values seen 60d: app_store 38/36, friend 11/11, therapist 11/11, other 7/7, social_media 6/6.
No "blog"/"website" option exists in this picker, so even qualitative self-report can't surface
blog-driven installs.

**Why:** operator asked "does the blog convert readers into app users" — verdict was
"not measurable" (traffic too low for any split, and no instrumentation path, web or app-side,
connects a blog reader to an app install). See full extract/report at
analytics-reports/raw/2026-10-01-blog-conversion.md.

**How to apply:** Any future blog-ROI or blog-attribution question hits the same wall until
either (a) someone adds a UTM-passthrough + app-side utm capture on install, or (b) a shared
identity bridge (e.g. web visitor clicks store link with a unique param, app captures it at
first-open) is built. Don't re-derive this from scratch — point to this memory and the extract,
then re-verify only the volume numbers (they'll have grown) if asked again.
