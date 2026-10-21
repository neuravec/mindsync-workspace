# Blog mindsync.app -> instalacja / aktywnosc w aplikacji: raw PostHog extract

- **Date**: 2026-10-07 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: 2026-09-01 00:00 UTC -> 2026-10-07 (biezacy dzien niepelny); okno "po wdrozeniu linkow" = od 2026-10-01
- **Question**: czy ruch z bloga (wpisy /journal/*) przeklada sie na instalacje i aktywnosc w aplikacji, po dodaniu oznaczonych linkow do sklepow 2026-10-01?
- **Event verification**:
  - `app_install_attributed` (client, `posthog-flutter`, Android referrer + iOS fallback): flowing, last_seen 2026-10-07 06:58 UTC, ok. 5-17 osob/dzien. Wlasciwosci `install_source`, `install_medium`, `install_campaign`, `install_referrer_raw`, `platform` obecne.
  - `blog_store_click` (skrypt Webflow, wymaga zgody cookies): **nigdy nie zarejestrowany** w event_definitions (`--events blog` = 0 wierszy).
  - `app_store_click` (starsze zdarzenie strony, `$lib=web`): flowing, last_seen 2026-10-05; lifetime 96 zdarzen / 71 osob od 2026-04-13. Ma tylko wlasciwosc `store`, brak sluga/medium.
  - `$pageview` z `$lib=web`, host `www.mindsync.app`: flowing, last_seen 2026-10-06 20:28.
  - `onboarding_lead_source_selected` (ankieta onboardingu, `source_value`): flowing, last_seen 2026-10-06; wartosc `blog` pojawia sie od tygodnia 2026-10-04.

## Results

### 1. Atrybucja instalacji (Android Play Install Referrer)

Osoby z `app_install_attributed` od 2026-10-01 (person_id):

| platform | install_source | users |
|---|---|---|
| android | google-play (medium `organic`) | 71 |
| ios | organic_or_unknown | n<25 |
| android | apps.facebook.com | n<25 |
| android | organic_or_unknown | n<25 |
| any | **blog** | **0** |

Ksztalt surowego referrera, caly okres 09-01..10-07: `utm_source=google-play` (domyslny Play, organiczny) 197 osob; pusty n<25; gclid/ads n<25; inne n<25; **zawierajacy `blog`: 0**. Lifetime (365 dni) zdarzen z referrerem `%blog%` lub kampania inna niz `fb4a`: **0**. Osoby z person property `install_source='blog'`: **0**.

Instalacje z atrybucja dziennie (wszystkie zrodla), 09-25..10-07: 8, 9, 10, 7, 14, 15, 14, 12, 17, 7, 16, 13, 5 (10-07 niepelny). Brak skoku po 10-01.

### 2. Ankieta onboardingu (`onboarding_lead_source_selected.source_value`)

Wartosc `blog` wystepuje w tygodniu 2026-10-04: niezerowa, **n<25 (suppressed)**. Wczesniej 0. Pozostale wartosci w tym tygodniu: app_store, other, friend, social_media (wszystkie n<25). Przejscie dalej (pierwsza sesja) nie raportowane z powodu k-anonimowosci.

### 3. Ruch web (PostHog na mindsync.app, `$lib=web`)

PostHog na stronie istnieje, ale laduje sie dopiero po zgodzie na cookies, wiec liczby to dolna granica.

| sekcja | pageviews 09-01..09-30 | pageviews 10-01..10-07 | users |
|---|---|---|---|
| home `/` | 56 | 23 | 52 |
| inne strony | 35 | 19 | n<25 |
| wpisy `/journal/*` | 10 | 2 | n<25 |
| listing `/blog` | 1 | 0 | n<25 |

Pageviews per wpis (09-01..10-07; users kazdego wpisu n<25):

| path | pv | pierwszy | ostatni |
|---|---|---|---|
| /journal/how-to-remember-what-you-talk-about-in... | 5 | 09-22 | 09-30 |
| /journal/journaling-vs-voice-notes | 3 | 09-20 | 09-30 |
| /journal/early-signs-of-burnout | 2 | 09-25 | 09-28 |
| /journal/therapy-hangover | 1 | 10-05 | 10-05 |
| /journal/same-argument-over-and-over | 1 | 10-06 | 10-06 |

Referring domain wpisow: www.google.com 10 pv, $direct 2 pv.

Klikniecia w sklep z webu w oknie: `app_store_click` 7 zdarzen, wszystkie na `/` lub `/about`, **0 z `/journal/*`**. `blog_store_click`: **0, nigdy**.

Osoby z eventami web i app jednoczesnie (09-01..10-07): **0** z 74 web / 267 app (oczekiwane: instalacja tworzy nowy anonimowy person_id).

## Caveats

- Linki z bloga oznaczone od 2026-10-01: okno po wdrozeniu ma 7 dni, a z PostHoga widac tylko 2 pageviewy wpisow w tym czasie (tylko sesje ze zgoda na cookies). Brak sygnalu `blog` w referrerze jest spojny z bardzo malym ruchem, a nie dowodem, ze mechanizm nie dziala.
- PostHog web jest consent-gated (`blog_store_click` wymaga `__msA`), wiec pageviews sa mocno zanizone wobec GSC.
- iOS: brak referrera, zawsze `organic_or_unknown`. Instalacje iOS z bloga widac tylko w App Store Connect (Campaigns, `ct=blog-<slug>`), nie w PostHogu.
- `app_install_attributed` strzela raz na instalacje aplikacji 2.0.86+, takze u starych userow po aktualizacji; count > users (297/197) oznacza reinstalacje lub wyczyszczone prefs. To nie jest czysta liczba nowych instalacji.
- `install_source=google-play / medium=organic` to domyslny referrer Play przy instalacji ze sklepu bez parametru `referrer`; nie da sie z niego wyczytac, czy czlowiek wczesniej czytal bloga.
- Ingest od 2026-04-22; okno nie siega tak daleko.
- k-anonimowosc: segmenty <25 osob zgloszone jako n<25.

## Queries

```sql
-- @@ attributed_by_source_platform
SELECT toStartOfWeek(timestamp) AS wk, properties.install_source AS src, properties.platform AS plat, properties.$lib AS lib, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'app_install_attributed' AND timestamp >= toDateTime('2026-09-01') AND timestamp < toDateTime('2026-10-08')
GROUP BY wk, src, plat, lib ORDER BY wk, users DESC LIMIT 100

-- @@ attributed_non_organic_detail
SELECT properties.install_source AS src, properties.install_medium AS med, properties.install_campaign AS camp, properties.platform AS plat, count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events WHERE event = 'app_install_attributed' AND timestamp >= toDateTime('2026-09-01') AND timestamp < toDateTime('2026-10-08')
  AND properties.install_source != 'organic_or_unknown'
GROUP BY src, med, camp, plat ORDER BY users DESC LIMIT 50

-- @@ referrer_raw_shapes_android
SELECT multiIf(properties.install_referrer_raw IS NULL OR properties.install_referrer_raw = '', 'empty',
               properties.install_referrer_raw LIKE '%utm_source=google-play%', 'google-play default',
               properties.install_referrer_raw LIKE '%utm_source=blog%', 'blog',
               properties.install_referrer_raw LIKE '%gclid%', 'gclid/ads', 'other') AS shape,
       count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'app_install_attributed' AND timestamp >= toDateTime('2026-09-01') AND timestamp < toDateTime('2026-10-08')
GROUP BY shape ORDER BY users DESC

-- @@ lead_source_selected
SELECT toStartOfWeek(timestamp) AS wk, properties.source_value AS v, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'onboarding_lead_source_selected' AND timestamp >= toDateTime('2026-09-01') AND timestamp < toDateTime('2026-10-08')
GROUP BY wk, v ORDER BY wk, users DESC LIMIT 100

-- @@ pageviews_by_path_section
SELECT multiIf(properties.$pathname LIKE '/journal/%', 'journal_post', properties.$pathname IN ('/blog','/blog/'), 'blog_listing', properties.$pathname IN ('/', ''), 'home', 'other') AS section,
       countIf(timestamp < toDateTime('2026-10-01')) AS pv_before_1001, countIf(timestamp >= toDateTime('2026-10-01')) AS pv_from_1001,
       count(DISTINCT person_id) AS users
FROM events WHERE event = '$pageview' AND properties.$lib = 'web' AND timestamp >= toDateTime('2026-09-01') AND timestamp < toDateTime('2026-10-08')
GROUP BY section ORDER BY users DESC

-- @@ pageviews_per_journal_post
SELECT properties.$pathname AS path, count() AS pv, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events WHERE event = '$pageview' AND properties.$lib = 'web' AND properties.$pathname LIKE '/journal/%'
  AND timestamp >= toDateTime('2026-09-01') AND timestamp < toDateTime('2026-10-08')
GROUP BY path ORDER BY pv DESC LIMIT 50

-- @@ app_store_click_detail
SELECT toDate(timestamp) AS d, properties.$pathname AS path, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'app_store_click' AND timestamp >= toDateTime('2026-09-01') AND timestamp < toDateTime('2026-10-08')
GROUP BY d, path ORDER BY d LIMIT 50

-- @@ store_click_lifetime
SELECT event, count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events WHERE event IN ('app_store_click', 'blog_store_click') AND timestamp > now() - INTERVAL 365 DAY
GROUP BY event

-- @@ journal_referring_domain
SELECT properties.$referring_domain AS ref, count() AS pv, count(DISTINCT person_id) AS users
FROM events WHERE event = '$pageview' AND properties.$lib = 'web' AND properties.$pathname LIKE '/journal/%'
  AND timestamp >= toDateTime('2026-09-01') AND timestamp < toDateTime('2026-10-08')
GROUP BY ref ORDER BY pv DESC LIMIT 20

-- @@ web_to_app_person_overlap
SELECT countIf(has_web AND has_app) AS both, countIf(has_web) AS web_people, countIf(has_app) AS app_people
FROM (SELECT person_id, countIf(properties.$lib = 'web') > 0 AS has_web, countIf(properties.$lib = 'posthog-flutter') > 0 AS has_app
      FROM events WHERE timestamp >= toDateTime('2026-09-01') AND timestamp < toDateTime('2026-10-08') GROUP BY person_id)

-- @@ installs_since_1001
SELECT properties.platform AS plat, properties.install_source AS src, count(DISTINCT person_id) AS users
FROM events WHERE event = 'app_install_attributed' AND timestamp >= toDateTime('2026-10-01') AND timestamp < toDateTime('2026-10-08')
GROUP BY plat, src ORDER BY users DESC

-- @@ referrer_any_blog_lifetime
SELECT count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE event = 'app_install_attributed' AND timestamp > now() - INTERVAL 365 DAY
  AND (properties.install_referrer_raw LIKE '%blog%' OR properties.install_source = 'blog' OR properties.install_campaign IS NOT NULL AND properties.install_campaign != '' AND properties.install_campaign != 'fb4a')

-- @@ person_prop_install_source_blog
SELECT count() AS persons FROM persons WHERE properties.install_source = 'blog'
```
