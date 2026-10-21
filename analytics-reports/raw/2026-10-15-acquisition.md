# Pozyskanie nowych użytkowników, 60 dni: surowy wyciąg z PostHog

- **Data**: 2026-10-15 · **Agent**: posthog-data-extractor
- **Projekt**: PostHog EU 141170 · **Okno**: 2026-08-16 -> 2026-10-15 (UTC), tydzień liczony od poniedziałku
- **Pytanie**: ilu nowych użytkowników przychodzi, skąd (platforma, kraj, język, źródło instalacji, blog, web) i którzy z nich kończą onboarding oraz wracają.
- **Weryfikacja zdarzeń (60 dni)**:
  - `onboarding_step_viewed` (posthog-flutter) 1103 zd. / 127 osób, płynie do 10-15
  - `app_install_attributed` (posthog-flutter) 570 / 331, płynie do 10-15; klucze `install_source`, `install_medium`, `install_referrer_raw`, `install_campaign`, `platform` obecne
  - `onboarding_started` 163 / 106, `onboarding_completed` 105 / 80, `onboarding_lead_source_selected` 98 / 74, `user_logged_in` 302 / 29: wszystkie płyną do 10-15
  - `user_registered` **backend** (`posthog-python`) 146 / 146
  - `$pageview` (`web`) 241 / 118, `app_store_click` (`web`) 16 / 15, ostatnio 10-14
  - `$geoip_country_code` i `$locale` na 100% zdarzeń flutter (44 462/44 462); `$device_language` nie istnieje (język = 2 pierwsze znaki `$locale`)
  - `blog_store_click`, `blog_cta_click`, `install_source='blog'`: **0 zdarzeń w ciągu 365 dni**

## Definicja "nowego użytkownika"

**Nowy użytkownik = osoba (`person_id`), której pierwsze zdarzenie aplikacji (`$lib='posthog-flutter'`) od początku ingestu (2026-04-22) wypada w oknie.** To jest "pierwsze otwarcie aplikacji", czyli najbliższy odpowiednik instalacji.

Wykluczone na poziomie osoby: boty (`$device_model IN ('OnePlus8Pro','Pixel 6 Pro')`, 24 osoby) i testerzy (`$is_testflight`/`$is_emulator`, 5 osób). Z 325 osób zostaje **296 "czystych" nowych**.

Dlaczego nie `user_registered`: to zdarzenie backendu, a 38 z 146 rejestracji (26%) nie ma ani jednego zdarzenia aplikacji pod tym samym `person_id` (tożsamość nie scalona). Do segmentacji po platformie/kraju/źródle się nie nadaje. Dlaczego nie `app_install_attributed`: odpala też przy aktualizacji i reinstalacji (331 osób w 60 dni, więcej niż nowych).

Lejek jakości: nowy -> `onboarding_started` -> `onboarding_completed`. Powrót: osobne zdarzenie aplikacji w dniach 1-7 po pierwszym dniu (R7, kwalifikują się osoby z pierwszym dniem <= 10-07) oraz w dniach 7-13 (R14, pierwszy dzień <= 10-01).

## Wyniki

### 1. Nowi użytkownicy tygodniowo (czyści)

| tydzień | nowi | start onb. | onb. ukończony | % ukończ. | R7 (kwal.) | R14 (kwal.) | rejestracje backend |
|---|---|---|---|---|---|---|---|
| 08-10 (1 dzień) | n<5 | n<5 | n<5 | | | | n<5 |
| 08-17 | 23 | 10 | 6 | 26% | 4/23 | n<5 /23 | 12 |
| 08-24 | 11 | 6 | n<5 | 27% | 0/11 | n<5 /11 | 6 |
| 08-31 | 16 | 6 | 6 | 38% | 5/16 | n<5 /16 | 8 |
| 09-07 | 21 | 12 | 11 | 52% | n<5 /21 | n<5 /21 | 17 |
| 09-14 | 19 | 5 | n<5 | 5% | n<5 /19 | n<5 /19 | 10 |
| 09-21 | 47 | 14 | 10 | 21% | 9/47 (19%) | 5/47 (11%) | 18 |
| 09-28 | 78 | 14 | 10 | 13% | 14/78 (18%) | n<5 /46 | 23 |
| 10-05 | 60 | 18 | 15 | 25% | 6/32 (19%) | brak kwal. | 33 |
| 10-12 (4 dni) | 18 | 9 | 9 | 50% | brak kwal. | brak kwal. | 17 |
| **razem** | **296** | **94** | **71** | **24%** | **45/250 (18%)** | **19/186 (10%)** | 146 |

Dziennie: 1-10 nowych do 09-24, potem skok do 9-15 dziennie między 09-25 a 10-06, od 10-07 spadek do 3-8 dziennie. Pełna seria dzienna w sekcji Zapytania (`daily_new_clean`); w ostatnich 7 dniach ukończony onboarding 0-5 osób dziennie.

### 2. Skok 09-21..10-05 to głównie ruch nieanglojęzyczny o niskiej jakości

| tydzień | nowi en | ukończ. en | nowi nie-en | ukończ. nie-en |
|---|---|---|---|---|
| 09-14 | 15 | n<5 | n<5 | 0 |
| 09-21 | 20 | 7 | 27 | n<5 |
| 09-28 | 27 | 5 | 51 | 5 |
| 10-05 | 28 | 9 | 32 | 6 |

Wszystkie z `install_source='google-play'` (domyślny referrer Play, więc kanał nieznany), Android, języki `fr`/`ar`/`fa`, kraje CI, IR, DZ, SN, IQ, BF, CM. Wygląda na zewnętrzny bodziec w Google Play (np. widoczność w wyszukiwaniu lub polecenie w sklepie w regionie); PostHog nie pozwala ustalić źródła.

### 3. Podział nowych (60 dni)

**Platforma**

| platforma | nowi | % ukończ. onb. | R7 | R14 |
|---|---|---|---|---|
| Android | 269 | 22% (60) | 16% (37/225) | 8% (13/165) |
| iOS | 24 | 46% (11) | 36% (8/22) | 33% (6/18) |
| iPadOS | n<5 | | | |

**Kraj** (kraje z >= 5 nowymi; reszta w "inne")

| kraj | nowi | ukończ. onb. | % | R7 | R14 |
|---|---|---|---|---|---|
| US | 66 | 26 | 39% | 9/51 | 10/45 (22%) |
| PL | 13 | 8 | 62% | n<5 /10 | n<5 /9 |
| CI | 13 | n<5 | 8% | n<5 | 0 |
| IR | 11 | 0 | 0% | n<5 | n<5 |
| DE | 11 | n<5 | 9% | 0 | 0 |
| IQ | 10 | n<5 | 20% | 0 | 0 |
| DZ | 10 | 0 | 0% | n<5 | 0 |
| PH | 9 | n<5 | 11% | n<5 | 0 |
| SA | 8 | n<5 | 25% | 0 | 0 |
| SN, PK | po 7 | 0 | 0% | | |
| TR, SE | po 6 | n<5 | 50-67% | | |
| IN, CA, EG, BD, AU | po 5 | n<5 | 0-60% | | |
| inne (47 krajów) | 92 | | | | |

Grupowanie rynków: US + Europa Zach./UE + CA/AU/GB = 133 nowych, 53 ukończyło onboarding (40%), R14 16/82 (20%). Pozostałe kraje = 163 nowych, 18 ukończyło (11%), R14 3/104 (3%).

**Język urządzenia** (`$locale`, 2 litery)

| język | nowi | % ukończ. | R7 | R14 |
|---|---|---|---|---|
| en | 144 | 33% (47) | 24% (29/119) | 18% (17/97) |
| fr | 60 | 5% (n<5) | 12% (7/57) | n<5 /38 |
| ar | 23 | 17% (n<5) | n<5 | 0 |
| fa | 16 | 0% | n<5 | 0 |
| de, ru | po 7 | | | |
| tr, pl, sv, pt | po 5 | 40-80% | | |
| inne | 19 | | | |

### 4. Źródło instalacji (`app_install_attributed.install_source`)

| install_source | nowi | % ukończ. onb. | R7 | R14 |
|---|---|---|---|---|
| google-play (medium `organic`, domyślny referrer Play) | 241 | 21% (51) | 18% (37/204) | 9% (13/146) |
| organic_or_unknown (iOS, brak API referrera) | 24 | 42% (10) | 29% (6/21) | 35% (6/17) |
| brak zdarzenia atrybucji | 23 | 22% (5) | 11% | 0 |
| (not set) | 7 | 71% (5) | 0 | 0 |
| apps.facebook.com | n<5 | | | |
| **blog** | **0** | | | |

Wartości `install_source` od 2026-08-01 (wszystkie zdarzenia, także aktualizacje): google-play 307 osób, organic_or_unknown 43, (not set) 8, apps.facebook.com n<5 (campaign `fb4a`), google n<5. **`install_source='blog'` = 0, `install_campaign` z przypisanym slugiem wpisu = 0.** Pomiar blog -> instalacja na Androidzie nadal nie zarejestrował żadnej instalacji.

### 5. Deklarowane źródło (ankieta w onboardingu, `onboarding_lead_source_selected.source_value`)

Odpowiadają tylko osoby, które przeszły onboarding (71 czystych nowych + kilku powracających).

| źródło (deklaracja) | nowi | R7 | R14 |
|---|---|---|---|
| app_store (wyszukiwanie w sklepie) | 38 | 9/25 (36%) | 7/22 (32%) |
| friend | 9 | n<5 /8 | n<5 /8 |
| therapist | 7 | n<5 | n<5 |
| other | 7 | n<5 | n<5 |
| social_media | 5 | n<5 | n<5 |
| blog | n<5 | brak kwal. | brak kwal. |

Tygodniowo `blog` pojawia się tylko w tygodniu 10-05 (n<5, 2 osoby wśród wszystkich odpowiadających; 1 w kohorcie czystych nowych). "therapist" rośnie od 09-28 (n<5 tygodniowo).

### 6. Ruch web na mindsync.app (`$lib='web'`, zbierany tylko po zgodzie na cookies)

| tydzień | pageview | odwiedzający | pv /journal | odw. /journal | app_store_click |
|---|---|---|---|---|---|
| 08-17 | 23 | 16 | 0 | 0 | n<5 |
| 08-24 | 34 | 14 | 5 | n<5 | 0 |
| 08-31 | 15 | 8 | 0 | 0 | 0 |
| 09-07 | 23 | 9 | 0 | 0 | n<5 |
| 09-14 | 24 | 12 | n<5 | n<5 | n<5 |
| 09-21 | 26 | 15 | n<5 | n<5 | 0 |
| 09-28 | 37 | 22 | 5 | n<5 | n<5 |
| 10-05 | 35 | 22 | 5 | 5 | n<5 |
| 10-12 | 24 | 8 | 0 | 0 | n<5 |

Referrery (60 dni, odwiedzający): google.com 65, direct 30, mindsync.app (wewn.) 17, bing.com 5, reszta n<5 (facebook, chatgpt.com, linkedin, instagram, yandex, ecosia). UTM: prawie cały ruch bez UTM; `utm_source=instagram` n<5, `chatgpt.com` n<5. `app_store_click`: google 10, apple 6 (bez sluga wpisu). Osoby web nie łączą się z osobami aplikacji, więc ścieżki web -> instalacja nie da się złożyć w PostHog.

## Ustalenia

1. **Nowi**: 296 czystych nowych osób w 60 dni (śr. ~35/tydz.), z czego tylko **71 (24%) ukończyło onboarding**, a 94 (32%) go w ogóle zaczęło. Dwie trzecie nowych odpada przed onboardingiem (otwarcie -> ekran logowania -> nic).
2. **Wzrost wolumenu od 09-21 to ruch niskiej jakości**: tygodnie 09-21..10-05 dały 185 nowych, ale 60% z nich to Android w językach fr/ar/fa z Afryki Zach. i Bliskiego Wschodu, z ukończeniem onboardingu 5-11% i R14 bliskim zera. Liczba nowych **anglojęzycznych** rosła łagodniej (12-15/tydz. we wrześniu -> 27-28 na przełomie IX/X).
3. **Kto zostaje**: iOS (46% ukończ., R14 33%) wyraźnie lepszy niż Android (22%, 8%). US + rynki zachodnie: 40% ukończenia i R14 20%, pozostałe kraje 11% i 3%. Język `en` R14 18% vs `fr` poniżej 5%. Najwięcej aktywnych po 2 tygodniach dają US (10 osób) i iOS ogółem (6).
4. **Kanały**: atrybucja techniczna jest prawie bezużyteczna: 81% nowych ma `install_source='google-play'`, czyli domyślny referrer Play bez kampanii. Jedyny sygnał kanału to deklaracja w ankiecie: wyszukiwanie w sklepie dominuje (38 z 71 onboardowanych) i ma najlepszy R14 przy sensownym n (32%).
5. **Blog -> instalacja**: **0 instalacji przypisanych blogowi** w PostHog (ani `install_source='blog'`, ani kampanii ze slugiem, ani `blog_store_click`). Jedyny ślad bloga to n<5 deklaracji "blog" w ankiecie w tygodniu 10-05. Ruch na /journal widziany przez PostHog to 0-5 odwiedzających tygodniowo (zaniżone przez bramkę cookies).

## Zastrzeżenia

- Ingest od 2026-04-22: "pierwsze zdarzenie" liczone od tej daty; okno 60 dni jest daleko od granicy, więc brak obcinania.
- Nowy użytkownik = nowy `person_id` w aplikacji. Reinstalacja bez zalogowania, nowe urządzenie albo nie scalona tożsamość daje "nowego" sztucznie; 26% rejestracji backendu nie ma zdarzeń aplikacji pod tym samym `person_id` (tydzień 10-05: 13/33), więc część nowych to fragmenty tożsamości, a nie osobne osoby. Twarda liczba nowych kont: tabela `users` w Postgres przez `database-administrator`.
- R7/R14 liczą dowolne zdarzenie aplikacji (także samo otwarcie z powiadomienia). Dla ostatnich tygodni brak pełnego okna obserwacji, stąd "brak kwal.".
- Filtr botów po modelu urządzenia może pominąć nowe modele farm testowych. Tygodniowy skok niekoniecznie jest ruchem botów: część tych osób zaczęła onboarding.
- Próg prywatności: w tym raporcie zgodnie z poleceniem zadania grupy < 5 osób oznaczone "n<5". Standard agenta to k = 25; przy tej skali danych większość segmentów krajowych i kanałowych byłaby wtedy ukryta. To dane o pozyskaniu (kraj, platforma), bez treści zdrowotnych.
- Wszystkie odsetki na małych n (dziesiątki osób) są orientacyjne.
- iOS nie ma referrera instalacji; atrybucja iOS z bloga istnieje tylko w App Store Connect (Campaigns, `ct=blog-<slug>`), nie w PostHog.
- Web PostHog ładuje się dopiero po zgodzie na cookies, więc pageviews są ułamkiem ruchu z GSC.

## Zapytania

```sql
-- @@ candidate_events_60d
SELECT event, properties.$lib AS lib, count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp > now() - INTERVAL 60 DAY
  AND event IN ('user_registered','user_logged_in','app_install_attributed','onboarding_started','onboarding_step_viewed','onboarding_completed','onboarding_lead_source_selected','$pageview','app_store_click','blog_store_click','$identify','Application Installed','Application Opened','first_open','app_opened')
GROUP BY event, lib ORDER BY c DESC LIMIT 50

-- @@ prop_coverage_flutter_60d
SELECT count() AS ev,
  countIf(properties.$geoip_country_code != '' AND properties.$geoip_country_code IS NOT NULL) AS has_country,
  countIf(properties.$locale != '' AND properties.$locale IS NOT NULL) AS has_locale,
  countIf(properties.$device_language != '' AND properties.$device_language IS NOT NULL) AS has_devlang,
  countIf(properties.$os != '' AND properties.$os IS NOT NULL) AS has_os
FROM events
WHERE timestamp > now() - INTERVAL 60 DAY AND properties.$lib = 'posthog-flutter'

-- @@ newuser_cube  (wynik agregowany lokalnie do tabel 1-5)
SELECT
  toStartOfWeek(fd, 1) AS wk, os, cc, loc, src, lead,
  bot, tester, reg, logged, onb_start, onb_done,
  count() AS persons,
  countIf(elig7) AS e7, countIf(elig7 AND ret_d1_7) AS r7,
  countIf(elig14) AS e14, countIf(elig14 AND ret_d7_13) AS r14
FROM (
  SELECT person_id,
    toDate(minIf(timestamp, properties.$lib = 'posthog-flutter')) AS fd,
    argMinIf(properties.$os, timestamp, properties.$lib = 'posthog-flutter') AS os,
    argMinIf(properties.$geoip_country_code, timestamp, properties.$lib = 'posthog-flutter') AS cc,
    substring(argMinIf(properties.$locale, timestamp, properties.$lib = 'posthog-flutter'), 1, 2) AS loc,
    argMinIf(properties.install_source, timestamp, event = 'app_install_attributed') AS src,
    argMaxIf(properties.source_value, timestamp, event = 'onboarding_lead_source_selected') AS lead,
    countIf(properties.$device_model IN ('OnePlus8Pro', 'Pixel 6 Pro')) > 0 AS bot,
    countIf(properties.$is_testflight = true OR properties.$is_emulator = true) > 0 AS tester,
    countIf(event = 'user_registered') > 0 AS reg,
    countIf(event = 'user_logged_in') > 0 AS logged,
    countIf(event = 'onboarding_started') > 0 AS onb_start,
    countIf(event = 'onboarding_completed') > 0 AS onb_done,
    groupUniqArrayIf(toDate(timestamp), properties.$lib = 'posthog-flutter') AS ds,
    fd <= today() - 8 AS elig7,
    fd <= today() - 14 AS elig14,
    arrayExists(x -> x >= fd + 1 AND x <= fd + 7, ds) AS ret_d1_7,
    arrayExists(x -> x >= fd + 7 AND x <= fd + 13, ds) AS ret_d7_13
  FROM events
  WHERE timestamp >= toDateTime('2026-04-22 00:00:00')
    AND (properties.$lib = 'posthog-flutter' OR event = 'user_registered')
  GROUP BY person_id
  HAVING countIf(properties.$lib = 'posthog-flutter') > 0
)
WHERE fd >= toDate('2026-08-16')
GROUP BY wk, os, cc, loc, src, lead, bot, tester, reg, logged, onb_start, onb_done
ORDER BY wk LIMIT 5000

-- @@ daily_new_clean
SELECT fd, count() AS new_clean, countIf(onb_done) AS onboarded
FROM (
  SELECT person_id, toDate(min(timestamp)) AS fd,
    countIf(properties.$device_model IN ('OnePlus8Pro', 'Pixel 6 Pro')) > 0 AS bot,
    countIf(properties.$is_testflight = true OR properties.$is_emulator = true) > 0 AS tester,
    countIf(event = 'onboarding_completed') > 0 AS onb_done
  FROM events
  WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter'
  GROUP BY person_id
)
WHERE fd >= toDate('2026-08-16') AND NOT bot AND NOT tester
GROUP BY fd ORDER BY fd

-- @@ registered_merge_check
SELECT toStartOfWeek(reg_ts, 1) AS wk, count() AS registered,
  countIf(has_flutter) AS with_app_events, countIf(has_onb) AS with_onb_done
FROM (
  SELECT person_id,
    minIf(timestamp, event = 'user_registered') AS reg_ts,
    countIf(properties.$lib = 'posthog-flutter') > 0 AS has_flutter,
    countIf(event = 'onboarding_completed') > 0 AS has_onb
  FROM events
  WHERE timestamp >= toDateTime('2026-08-01 00:00:00')
    AND (event = 'user_registered' OR properties.$lib = 'posthog-flutter')
  GROUP BY person_id
  HAVING countIf(event = 'user_registered') > 0
)
WHERE reg_ts >= toDateTime('2026-08-16 00:00:00')
GROUP BY wk ORDER BY wk

-- @@ attribution_values_all_time
SELECT properties.install_source AS src, properties.install_medium AS med, properties.install_campaign AS camp,
  count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE event = 'app_install_attributed' AND timestamp >= toDateTime('2026-08-01 00:00:00')
GROUP BY src, med, camp ORDER BY users DESC LIMIT 40

-- @@ lead_source_by_week
SELECT toStartOfWeek(timestamp, 1) AS wk, properties.source_value AS v, count(DISTINCT person_id) AS users
FROM events
WHERE event = 'onboarding_lead_source_selected' AND timestamp > now() - INTERVAL 60 DAY
GROUP BY wk, v ORDER BY wk, users DESC LIMIT 200

-- @@ web_weekly
SELECT toStartOfWeek(timestamp, 1) AS wk,
  countIf(event = '$pageview') AS pv, count(DISTINCT if(event = '$pageview', person_id, NULL)) AS visitors,
  countIf(event = '$pageview' AND properties.$pathname LIKE '/journal/%') AS pv_journal,
  count(DISTINCT if(event = '$pageview' AND properties.$pathname LIKE '/journal/%', person_id, NULL)) AS vis_journal,
  countIf(event = 'app_store_click') AS store_clicks, count(DISTINCT if(event = 'app_store_click', person_id, NULL)) AS store_clickers
FROM events
WHERE properties.$lib = 'web' AND timestamp > now() - INTERVAL 60 DAY
GROUP BY wk ORDER BY wk

-- @@ web_referrers
SELECT coalesce(nullIf(properties.$referring_domain, ''), '(brak)') AS ref, count() AS pv, count(DISTINCT person_id) AS visitors
FROM events
WHERE properties.$lib = 'web' AND event = '$pageview' AND timestamp > now() - INTERVAL 60 DAY
GROUP BY ref ORDER BY visitors DESC LIMIT 20

-- @@ web_utm_and_paths
SELECT multiIf(properties.$pathname LIKE '/journal/%', 'journal', properties.$pathname = '/blog', 'blog listing', properties.$pathname = '/' OR properties.$pathname = '', 'home', 'other') AS section,
  coalesce(nullIf(properties.utm_source, ''), '(brak)') AS utm_source,
  count() AS pv, count(DISTINCT person_id) AS visitors
FROM events
WHERE properties.$lib = 'web' AND event = '$pageview' AND timestamp > now() - INTERVAL 60 DAY
GROUP BY section, utm_source ORDER BY visitors DESC LIMIT 30

-- @@ blog_events_ever
SELECT event, count() AS c, count(DISTINCT person_id) AS users, max(timestamp) AS last_ts
FROM events
WHERE timestamp > now() - INTERVAL 365 DAY
  AND (event IN ('blog_store_click', 'blog_cta_click') OR (event = 'app_install_attributed' AND properties.install_source = 'blog'))
GROUP BY event LIMIT 10
```
