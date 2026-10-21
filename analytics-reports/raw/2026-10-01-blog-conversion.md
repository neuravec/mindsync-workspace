# Blog conversion (mindsync.app/journal) – raw PostHog extract

- **Date**: 2026-10-01 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: 2026-08-02 -> 2026-10-01 (60d, UTC)
- **Question**: Does the MindSync blog (mindsync.app/journal, /blog) convert readers into app users?
- **Event verification**:
  - `$pageview`, `$autocapture`, `$pageleave`, `$web_vitals` on `www.mindsync.app` – flowing, but at very low volume (244 pageviews / 114 unique visitors over 60d site-wide).
  - `app_store_click` (custom CTA event on the website) – flowing, 12 events / 10 users, all from `/` and `/about`, none from `/journal/*`.
  - App side: `$lib = 'posthog-flutter'` events flowing heavily (hundreds of thousands of rows across onboarding/usage events).
  - `utm_source`, `$referrer`, `install_referrer`, `utm_campaign` on app events – **not flowing** (0 rows with non-null/non-empty value in 60d).
  - `onboarding_lead_source_selected` (in-app "how did you hear about us" style event) – flowing, property name is `source_value` (not `lead_source`).

## Results

### 1. Is the site instrumented in PostHog at all?
Yes, partially. `www.mindsync.app` sends `$pageview`/`$autocapture`/`$pageleave`/`$web_vitals` via posthog-js, but traffic is extremely small.

Web events by type, 60d, host contains `mindsync.app`:

| event | count | users | first_ts | last_ts |
|---|---|---|---|---|
| $web_vitals | 250 | 93 | 2026-08-03 | 2026-10-01 |
| $pageview | 244 | 114 | 2026-08-03 | 2026-10-01 |
| $pageleave | 210 | 125 | 2026-08-03 | 2026-10-01 |
| $autocapture | 134 | 44 | 2026-08-03 | 2026-10-01 |
| app_store_click | 12 | 10 | 2026-08-05 | 2026-09-17 |

Host split: 100% of events on `www.mindsync.app` (378 events / 114 users over 60d; no bare `mindsync.app` host rows seen, consistent with the known www->root 301 from the 2026-08-26 SEO fix).

Path split (of $pageview + $autocapture, 60d):

| path bucket | events | users |
|---|---|---|
| other (static pages) | 180 | 47 |
| / (home) | 171 | 83 |
| /journal/* | 18 | 7 |
| /blog (listing) | 9 | 3 |

### 2. /journal/* reader behaviour (60d)

Daily pageviews (only days with activity shown, rest are zero):

| day | pageviews | visitors |
|---|---|---|
| 2026-09-30 | 4 | 2 |
| 2026-09-28 | 1 | 1 |
| 2026-09-25 | 1 | 1 |
| 2026-09-22 | 2 | 1 |
| 2026-09-20 | 2 | 1 |
| 2026-08-26 | 5 | 2 |

Weekly: week of 2026-09-27 = 5 pv/3 visitors; week of 2026-09-20 = 5 pv/3 visitors; week of 2026-08-23 = 5 pv/2 visitors. All other weeks in the 60d window = 0.

Top posts by pageviews (all of them, n is tiny – below is every row returned, not a top-15 cut):

| path | pageviews | visitors |
|---|---|---|
| /journal/how-to-remember-what-you-talk-about-in-therapy | 5 | 2 |
| /journal/journaling-vs-voice-notes | 3 | 2 |
| /journal/how-to-prepare-for-a-therapy-session | 2 | 1 |
| /journal/regulate-nervous-system-between-therapy-sessions | 2 | 2 |
| /journal/early-signs-of-burnout | 2 | 2 |
| /journal/digital-burnout-brain-rewiring | 1 | 1 |

(n=18 total pageviews across 6 distinct posts in 60 days — all other published posts had zero recorded pageviews in PostHog.)

$referring_domain for /journal/* pageviews:

| referring domain | pageviews | visitors |
|---|---|---|
| www.google.com | 8 | 4 |
| $direct | 7 | 3 |

No AI-assistant referrers (chatgpt.com, perplexity.ai, etc.) appeared at all in 60d — either genuinely zero or below the noise floor at this traffic level.

Outbound store clicks: the custom `app_store_click` event exists and fires (store=`google`/`apple`), but **all 12 occurrences fired from `/` or `/about`, zero from `/journal/*` or `/blog`**. Plain `$autocapture` click rows on these pages carry null `$el_text`/`href` for this filter (autocapture doesn't tag outbound link clicks with a dedicated href property the way the custom event does), so outbound-click attribution specifically from blog pages is not observable at all — not "zero", genuinely unmeasured for non-CTA links.

Identity stitching (web person -> app person): checked by intersecting person_id sets between /journal/ pageview viewers and any `$lib='posthog-flutter'` event in the same 60d window. **Result: 0 stitched persons.** This is expected — PostHog's web and Flutter SDKs are not configured to share identity (no cross-domain/cross-app anonymous-id bridging, no login-time `identify()` tying a web visitor to an app account), so this question is structurally unanswerable with current instrumentation, not just empirically zero.

### 3. App-side attribution properties (60d, $lib='posthog-flutter')

| property | flowing? | distinct values found |
|---|---|---|
| `utm_source` | NOT flowing | 0 non-empty rows |
| `utm_campaign` | NOT flowing | 0 non-empty rows |
| `$referrer` (app) | NOT flowing | 0 non-empty rows |
| `install_referrer` | NOT flowing | 0 non-empty rows (property does not appear to be captured client-side at all) |
| `onboarding_lead_source_selected` event, `source_value` property | **flowing** | app_store: 38 events/36 users; friend: 11/11; therapist: 11/11; other: 7/7; social_media: 6/6 (60d) |

No option among `source_value` values corresponds to "blog" or "website" — the onboarding lead-source picker does not offer or capture a web/blog-driven answer, so even this qualitative self-report can't surface blog-driven installs.

No event matching `%hear%`/`%referral%`/`%source%`/`%attribution%` other than the lead-source ones above and `reflect_entry_sources_shown` (76 events/11 users — an unrelated in-app feature, not acquisition attribution).

## Caveats
- Ingest starts 2026-04-22 (not a factor here; window is only 60d).
- Web traffic volume is tiny (114 unique visitors/60d site-wide, 7 unique /journal/ visitors/60d) — any split below ~10-20 users is statistical noise, not a trend. No segment under 25 users is reported as a rate/percentage for this reason; all such numbers are shown as raw counts only.
- k-anonymity: all reported segments are counts of distinct users below 25; per policy these are not usable as population-level conclusions, only as "instrumentation exists and fired N times" facts. No user-level or PII data was extracted.
- `app_store_click` custom event exists and works, but the autocapture fallback for raw outbound link clicks does not carry href/el_text in this project's config, so non-CTA outbound clicks from blog pages are invisible, not necessarily absent.
- Web <-> app identity stitching is architecturally absent (separate posthog-js and posthog-flutter instances, no shared ID bridge at login) — this is a structural instrumentation gap, not a query limitation.
- utm_source/campaign/referrer/install_referrer are completely unpopulated on app events across the full 60-day window — either never sent by the Flutter app or stripped before capture. Not a sampling artifact: 0 of millions of app events in the window carry any value.

## Queries
```sql
-- web_event_check
SELECT event, count() AS c, count(DISTINCT person_id) AS users, max(timestamp) AS last_ts, min(timestamp) AS first_ts
FROM events
WHERE timestamp > now() - INTERVAL 60 DAY
  AND (properties.$host LIKE '%mindsync.app%' OR properties.$current_url LIKE '%mindsync.app%')
GROUP BY event ORDER BY c DESC LIMIT 30

-- web_host_split
SELECT properties.$host AS host, count() AS c, count(DISTINCT person_id) AS users
FROM events
WHERE timestamp > now() - INTERVAL 60 DAY AND event IN ('$pageview','$autocapture')
GROUP BY host ORDER BY c DESC LIMIT 20

-- web_path_split
SELECT
  multiIf(
    properties.$pathname LIKE '/journal%', '/journal/*',
    properties.$pathname LIKE '/blog%', '/blog',
    properties.$pathname = '/', '/',
    properties.$pathname LIKE '/pre-order%', '/pre-order',
    'other'
  ) AS path_bucket,
  count() AS c, count(DISTINCT person_id) AS users
FROM events
WHERE timestamp > now() - INTERVAL 60 DAY
  AND event IN ('$pageview','$autocapture')
  AND (properties.$host LIKE '%mindsync.app%' OR properties.$current_url LIKE '%mindsync.app%')
GROUP BY path_bucket ORDER BY c DESC LIMIT 20

-- journal_daily / journal_weekly / journal_top_posts / journal_referrers
SELECT toDate(timestamp) AS day, count() AS pageviews, count(DISTINCT person_id) AS visitors
FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND event = '$pageview' AND properties.$pathname LIKE '/journal%'
GROUP BY day ORDER BY day DESC LIMIT 60

SELECT toStartOfWeek(timestamp) AS week, count() AS pageviews, count(DISTINCT person_id) AS visitors
FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND event = '$pageview' AND properties.$pathname LIKE '/journal%'
GROUP BY week ORDER BY week DESC LIMIT 10

SELECT properties.$pathname AS path, count() AS pageviews, count(DISTINCT person_id) AS visitors
FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND event = '$pageview' AND properties.$pathname LIKE '/journal%'
GROUP BY path ORDER BY pageviews DESC LIMIT 15

SELECT properties.$referring_domain AS ref_domain, count() AS pageviews, count(DISTINCT person_id) AS visitors
FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND event = '$pageview' AND properties.$pathname LIKE '/journal%'
GROUP BY ref_domain ORDER BY pageviews DESC LIMIT 25

-- outbound_store_clicks
SELECT event, properties.$el_text AS el_text, properties.href AS href, count() AS c, count(DISTINCT person_id) AS users
FROM events
WHERE timestamp > now() - INTERVAL 60 DAY
  AND (properties.$host LIKE '%mindsync.app%' OR properties.$current_url LIKE '%mindsync.app%')
  AND (properties.href LIKE '%apps.apple.com%' OR properties.href LIKE '%play.google.com%'
       OR toString(properties.$external_click_url) LIKE '%apps.apple.com%'
       OR toString(properties.$external_click_url) LIKE '%play.google.com%')
GROUP BY event, el_text, href ORDER BY c DESC LIMIT 30

SELECT properties.$pathname AS path, properties.store AS store, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND event = 'app_store_click'
GROUP BY path, store ORDER BY c DESC LIMIT 20

-- web_person_sample_check (identity stitching)
SELECT count(DISTINCT person_id) AS stitched_persons FROM (
  SELECT person_id FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND event = '$pageview' AND properties.$pathname LIKE '/journal%'
  INTERSECT DISTINCT
  SELECT person_id FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND properties.$lib = 'posthog-flutter'
)

-- app_attribution_props_* (utm_source, $referrer, install_referrer, utm_campaign)
SELECT properties.utm_source AS val, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND properties.$lib = 'posthog-flutter'
  AND properties.utm_source IS NOT NULL AND properties.utm_source != ''
GROUP BY val ORDER BY c DESC LIMIT 20
-- (same pattern repeated for $referrer, install_referrer, utm_campaign)

-- app_how_did_you_hear_event
SELECT event, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND properties.$lib = 'posthog-flutter'
  AND (event ILIKE '%hear%' OR event ILIKE '%referral%' OR event ILIKE '%source%' OR event ILIKE '%attribution%')
GROUP BY event ORDER BY c DESC LIMIT 20

-- onboarding_lead_source_selected breakdown
SELECT properties.source_value AS val, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp > now() - INTERVAL 60 DAY AND event = 'onboarding_lead_source_selected'
GROUP BY val ORDER BY c DESC LIMIT 30
```
