# Nowi użytkownicy, onboarding i aktywacja po wydaniu 2.0.117 (20-21.10): surowy wyciąg z PostHog

- **Data**: 2026-10-21 · **Agent**: posthog-data-extractor
- **Projekt**: PostHog EU 141170 · **Okno**: napływ 2026-10-01 → 2026-10-21 ok. 17:00 UTC; kohorty onboardingu 2026-10-10 → 2026-10-21 (UTC)
- **Pytanie**: czy wydanie z redesignem (App Store i Google Play ok. 20-21.10, nowe zrzuty) zmieniło napływ, przebieg onboardingu i aktywację nowych osób, w porównaniu z kohortą 10-19.10 i baseline z 15.10.
- **Weryfikacja zdarzeń** (od 16.10, użytkownicy, `last_seen`):
  - płyną (klient): `onboarding_started` 12, `onboarding_step_viewed` 14 (`step_name`/`step_index` obecne), `onboarding_step_completed` 13 (`outcome`), `onboarding_completed` 11, `post_onboarding_build_viewed`/`_finished` 11, `first_conversation_intro_viewed` 7, `_started` 6, `_ended` 7, `_recap_result` 6, `post_onboarding_offer_shown` 5, `_result` 7, `_not_shown` 2, `paywall_shown` 14, `paywall_dismissed` 10, `paywall_load_failed` 2, `notification_permission_prompted`/`_granted` 13/12, `mic_permission_result` 6 (prop `result`, `source`), `push_prompt_result`, `first_capture_prompt_shown` 14, `app_install_attributed` 27 (prop `install_source`, `platform`); wszystkie z `last_seen` 20-21.10.
  - płyną (backend): `user_registered` 20 (prop `auth_provider`), `trial_started` 20 (prop `platform`), `profile_updated` (`write_path`, `is_first_save`), `consent_granted` (`consent_type`), `reflect_session_started` (`mode` voice/text), `user_activated` (`is_within_24h`).
  - **`first_week_plan_shown` nie istnieje** (ani `_viewed`). Z rodziny `first_week_*` płyną tylko `first_week_plan_failed` (4 os./30 dni), `_toggled` (3), `_recap_viewed` (2), `_hide_undone` (2), `_hidden` (1), `_recap_dismissed` (1). Ekspozycji planu pierwszego tygodnia nie da się policzyć.
  - `Application Installed`/`first_open` nie płyną. "Pierwsze otwarcie" = pierwsze zdarzenie `$lib='posthog-flutter'` osoby (lookback 200 dni).

## 0. Najważniejsze: iOS z logowaniem Google jest dla klienta PostHog niewidoczny

Rejestracje (backend `user_registered`) połączone z platformą z `trial_started.platform` i z obecnością jakiegokolwiek zdarzenia klienta (`$lib='posthog-flutter'`) na tej samej osobie:

| tydzień (od niedz.) | platforma | logowanie | rejestracje | bez zdarzeń klienta |
|---|---|---|---|---|
| 2026-10-04 | android | google / email | 12 / 4 | 0 / 0 |
| 2026-10-04 | ios | google | 9 | **9** |
| 2026-10-04 | ios | email | n<5 | 0 |
| 2026-10-11 | android | google / email | 14 / 5 | 0 / 0 |
| 2026-10-11 | ios | google | 15 | **15** |
| 2026-10-11 | ios | email | n<5 | 0 |
| 2026-10-18 | android | google | n<5 | 0 |
| 2026-10-18 | ios | google | 6 | **6** |
| 2026-10-18 | ios | apple / email | n<5 | 0 |

30 z 30 rejestracji iOS + Google od 04.10 nie ma ani jednego zdarzenia klienta (także sprzed logowania: brak `splash`/`welcome` na anonimowych osobach iOS w tej skali). Rejestracje iOS przez Apple i e-mail są widoczne.

Co te osoby robią po stronie backendu (C, 10.10-19.10, iOS, bez zdarzeń klienta, n = 20 + 2 w R):

| zdarzenie backendu | widoczni iOS (n<5 osób w C) | niewidoczni iOS (22) |
|---|---|---|
| `profile_updated` `write_path=post_create` (tworzenie profilu przy rejestracji) | wszyscy | 22 |
| `profile_updated` `write_path=put` (zapis odpowiedzi onboardingu) | wszyscy | n<5 |
| `therapy_context_updated` | wszyscy | 0 |
| `consent_granted` `ARTICLE9_HEALTH` | wszyscy | 0 |
| `reflect_session_started` | wszyscy | 0 |
| `user_activated`, `subscription_purchase_completed` | | 0 |
| `time_zone_saved` / `character_history_read` | | 11 / 5 |

Odczyt wprost: 22 nowe konta iOS z Google w 12 dni przechodzą rejestrację, a potem nie zapisują onboardingu, nie dają zgody ART9 i nie zaczynają żadnej rozmowy. Klient nie wysyła z tych urządzeń nic. W kodzie `PostHogService.init()` wyłącza analitykę całkowicie, gdy build nie dostał `POSTHOG_API_KEY` (`lib/core/analytics/posthog_service.dart`, linie 95-101). PostHog nie rozstrzyga, czy to (a) build produkcyjny iOS bez klucza i przy okazji użytkownicy utknięci za logowaniem Google, (b) konta testowe lub automatyczne, czy (c) problem po zalogowaniu przez Google na iOS. To jest największa niewiadoma tej analizy: po stronie iOS mierzymy praktycznie tylko zespół i pojedyncze konta Apple/e-mail.

## 1. Napływ: nowe osoby per dzień

Nowe osoby klienta = pierwsze zdarzenie `posthog-flutter` w danym dniu (lookback 200 dni), bez urządzeń testowych. Rejestracje = backend `user_registered` (obejmuje niewidoczne iOS).

| dzień | nowe osoby klienta | Android | iOS | z onboardingiem | rejestracje (backend) | rej. iOS | rej. Android |
|---|---|---|---|---|---|---|---|
| 01-06.10 (śr./dzień) | 11,7 | 10,8 | 0,8 | 3,5 | 3,8 | | |
| 10.10 | 8 | 7 | n<5 | 6 | 7 | n<5 | 6 |
| 11.10 | 8 | 8 | 0 | 6 | 10 | n<5 | 6 |
| 12.10 | 5 | 5 | 0 | n<5 | 5 | n<5 | n<5 |
| 13.10 | n<5 | | | 0 | n<5 | | |
| 14.10 | 7 | 7 | 0 | n<5 | 5 | | n<5 |
| 15.10 | n<5 | | 0 | | 6 | 5 | n<5 |
| 16.10 | 5 | 5 | 0 | n<5 | n<5 | 0 | n<5 |
| 17.10 | n<5 | | 0 | | n<5 | | |
| 18.10 | 6 | n<5 | n<5 | n<5 | n<5 | | |
| 19.10 | n<5 | | | | 5 | n<5 | n<5 |
| **20.10** | n<5 | | 0 | 0 | **0** | 0 | 0 |
| **21.10** (do ok. 17 UTC) | n<5 | | | | n<5 | n<5 (2 niewidoczne) | 0 |

Średnio 13-19.10: 4,1 nowej osoby klienta dziennie i 4,3 rejestracji; 20-21.10: 2,5 i 2. **Wydanie nie dało widocznego wzrostu napływu**; 20.10 to pierwszy dzień w październiku bez żadnej rejestracji. Rozkład godzinowy od 18.10: najwyżej 1 nowa osoba na godzinę, brak skoku po wydaniu.

Wersje: `$app_version` 2.0.117 widoczna od 19.10 18:13 UTC (Android), 19.10 20:44 (iOS); 2.0.113-2.0.116 to buildy z 19.10 (głównie zespół). Nowe osoby na 2.0.117 do teraz: Android n<5, iOS n<5.

Kraj i język nowych osób od 18.10 (`$geoip_country_code`, `$locale`): rozproszone, każdy kraj n<5 (US, GB, IT, AU, PL, GE, DE, KG, TD, BD); język głównie en, pojedynczo ru, it, ar, da.

`install_source` (`app_install_attributed`, od 10.10, wszystkie zdarzenia, także aktualizacje): google-play 52 os. (Android), organic_or_unknown 8 iOS + 5 Android, apps.facebook.com n<5, (not set) n<5. Atrybucja nadal nie rozróżnia kanałów; `blog` = 0.

**Ekran powitalny i logowanie na Androidzie 2.0.117** (od 10.10, osoby):

| | welcome | CTA | ekran auth | wybór metody | `signup_started` | `login_failed` | `onboarding_started` |
|---|---|---|---|---|---|---|---|
| Android, starsze wersje | 59 | 47 | 51 | 38 | 28 | n<5 | 28 |
| Android, 2.0.117 | n<5 | n<5 | n<5 | n<5 | **0** | n<5 | **0** |
| iOS, 2.0.117 | n<5 | n<5 | n<5 | n<5 | n<5 | n<5 | n<5 |

Na Androidzie 2.0.117 nikt (0 z n<5 osób na welcome) nie doszedł do rejestracji. Przy bazowym 47% (28/59) szansa na samo 0 z 4 przypadkiem to ok. 8%, więc to sygnał do obserwacji, nie dowód błędu. Od 19.10 21:00 UTC nie ma żadnej rejestracji Android.

## 2. Lejek onboardingu krok po kroku

Kohorta jak w baseline 15.10: osoba (`person_id`) z pierwszym `onboarding_started`/`onboarding_step_viewed` (`$lib='posthog-flutter'`), bez urządzeń testowych, bez `onboarding_reset`, < 3 ukończeń. **C** = pierwsze zdarzenie onboardingu 10.10 00:00 → 19.10 18:00 UTC (n = 29, 27 Android). **R** = od 19.10 18:00 (wydanie 2.0.117 w sklepach; n = 4: 2 iOS, 2 Android). Baseline **B** z 15.10 = 03.10-14.10 (n = 38). C i B zachodzą na siebie w dniach 10-14.10.

| krok (index) | C widziało | C ukończyło | C pominęło | C mediana s | B widziało (15.10) | B ukończyło | B mediana s |
|---|---|---|---|---|---|---|---|
| start onboardingu | 29 | | | | 38 | | |
| personalise (-1) | 29 | 28 | 0 | 14 | 38 | 35 | 17 |
| legal_gate (0) | 26 | 24 | 0 | 10 | 32 | 29 | 10 |
| challenges (1) | 24 | 24 | 0 | 18 | 29 | 29 | 20 |
| intensity (2) | 24 | 24 | 0 | 13 | 29 | 29 | 16 |
| journey (3) | 24 | 23 | 8 | 11 | 29 | 29 | 11 |
| modality (4, warunkowy) | 8 | 8 | 0 | 14 | 10 | 10 | 15 |
| schedule (5, warunkowy) | 8 | 8 | n<5 | 10 | 10 | 10 | 9 |
| companion (6) | 24 | 24 | 0 | 40 | 29 | 28 | 42 |
| lead_source (7) | 24 | 24 | 0 | 8 | 28 | 28 | 8 |
| `onboarding_completed` | **24 (83%)** | | | | **28 (74%)** | | |

R (n = 4): wszystkie wartości n<5. Mediany czasu w R są dłuższe (challenges 52 s, schedule 94 s, companion 56 s), ale przy 4 osobach, z czego 2 na iOS, nie da się tego interpretować.

**Miejsca wycieku w C:** jedyne straty są na początku: `personalise` → `legal_gate` (29 → 26, 10%) i nieukończona bramka prawna (26 → 24). Od `challenges` do `lead_source` zero strat. Gałąź "pominięto": `journey` pominęło 8 z 24 (33%, w B 9 z 29, 31%); `schedule` n<5.

## 3. Po onboardingu i aktywacja

| etap | C (n = 29) | % startów C | B (15.10, n = 38) | % startów B |
|---|---|---|---|---|
| `onboarding_completed` | 24 | 83% | 28 | 74% |
| `post_onboarding_build_viewed` | 24 | 83% | 26 | 68% |
| `first_conversation_intro_viewed` | 18 | 62% | 17 | 45% |
| `first_conversation_intro_dismissed` | n<5 | | | |
| `first_conversation_started` | 17 | 59% | 15 | 39% |
| `first_conversation_ended` | 13 | 45% | 11 | 29% |
| `first_conversation_recap_result` | 12 | 41% | 10 | 26% |
| `paywall_shown` (dowolny) | 17 | 59% | | |
| `paywall_shown` trigger `post_onboarding*` | 11 | 38% | 12 | 32% |
| `post_onboarding_offer_shown` | 10 | 34% | 8 | 21% |
| `post_onboarding_offer_result` | 8 | 28% | 9 | 24% |
| `post_onboarding_offer_not_shown` | 0 | | 0 | |
| `subscription_purchase_completed` | n<5 | | n<5 | |
| `notification_permission_prompted` / `_granted` / `_denied` | 13 / 9 / n<5 | | | |
| `mic_permission_result` (source `first_conversation`) | 13 (granted 10, denied n<5, permanently_denied n<5) | | | |
| `first_capture_prompt_shown` | 14 | 48% | | |
| dowolne `first_week_*` | n<5 | | n<5 | |

Wyniki oferty w C (osoby, mogą się powtarzać): `continued_to_plans` 5, `closed_plans` n<5, `closed_offer` n<5, `skipped` n<5, `purchased_starter` n<5.

R (n = 4): `onboarding_completed`, build, intro, start rozmowy, oferta, mikrofon, powiadomienia: każde n<5. `first_capture_prompt_shown` w R = 0 (w C 14 z 29), `post_onboarding_offer_not_shown` w R = 0.

**Aktywacja od pierwszego zdarzenia onboardingu** (rozmowa = `voice_chat_started` / `first_conversation_started` / `reflect_message_submitted` / `reflect_session_started`, wpis = `recording_saved` / `quick_capture_submitted` / `prep_capture_submitted` / `debrief_started`):

| kohorta | n | kwalifikuje się do 24 h | rozmowa ≤ 6 h | głos ≤ 6 h | rozmowa ≤ 24 h | głos ≤ 24 h | wpis ≤ 24 h | mediana min. do 1. rozmowy |
|---|---|---|---|---|---|---|---|---|
| C | 29 | 29 | 17 (59%) | 17 (59%) | 18 (62%) | 17 (59%) | n<5 | 4 |
| R | 4 | n<5 | n<5 | n<5 | n<5 | n<5 | 0 | 8 |
| B (15.10) | 36 | 36 | | | 15 (42%) | 14 (39%) | 5 (14%) | |

Krzyżowo z backendem (rejestracje C widoczne dla klienta, n = 29): `reflect_session_started` w 24 h 19 (66%), w tym głos 11; `consent_granted ARTICLE9_HEALTH` 15; `user_activated` z `is_within_24h` 7. Zgadza się z wynikiem klienta (62%).

## Zastrzeżenia

- **Bardzo małe liczby.** C = 29 osób, R = 4. Kohorty po wydaniu nie da się ocenić; najstarsza osoba R ma ok. 47 h. Procenty C mają szerokie przedziały (83% przy n = 29 to mniej więcej 65-94%).
- **iOS jest prawie ślepy**: rejestracje iOS przez Google nie mają zdarzeń klienta (sekcja 0). Wszystkie liczby lejka klienta to w praktyce Android (27 z 29 w C). Wartość "83% ukończyło onboarding" nie obejmuje 20 niewidocznych kont iOS, które według backendu onboardingu nie zapisały.
- `profile_updated.is_first_save` pada przy `post_create`, czyli przy tworzeniu profilu przy rejestracji, a nie przy końcu onboardingu. Nie używać go jako "onboarding ukończony"; właściwy sygnał backendu to `write_path=put` albo `therapy_context_updated`.
- C (10-19.10) to mieszanka buildów 2.0.107-2.0.110; R to 2.0.117. Do C należą osoby z 10-14.10, które były też w B.
- `$locale` to język urządzenia; kraj to GeoIP.
- Próg prezentacji: wartości poniżej 5 osób zapisane jako n<5 (konwencja poprzednich wyciągów z 15.10, żeby tabele dało się porównać). Wiersze z wartościami w przedziale 5-24 nie zawierają cech wrażliwych (tylko zdarzenia produktu).
- Wykluczenia testerów heurystyczne (`$is_testflight`, `$is_emulator`, dwa modele urządzeń zespołu, reset onboardingu, ≥ 3 ukończenia). `$is_testflight` ma niepełne pokrycie.
- Okno nie sięga do startu ingestu (2026-04-22), brak przycinania.
- Ostatnie dane: ok. 2026-10-21 16:50 UTC; dzień 21.10 niepełny.

## Zapytania (HogQL, dosłownie)

```sql
-- Wspólne CTE kohorty onboardingu (C / R), używane w step_funnel, cohort_flow, activation_windows, split_os_lang_cc, permission_values
WITH coh AS (
  SELECT person_id, minIf(timestamp, event IN ('onboarding_started','onboarding_step_viewed')) AS ob_ts,
    multiIf(ob_ts >= toDateTime('2026-10-19 18:00:00'), 'R_since_1019_18h', 'C_1010_1019') AS period,
    argMinIf(properties.$os, timestamp, event IN ('onboarding_started','onboarding_step_viewed')) AS os,
    argMinIf(substring(properties.$locale,1,2), timestamp, event IN ('onboarding_started','onboarding_step_viewed')) AS lang,
    argMinIf(properties.$geoip_country_code, timestamp, event IN ('onboarding_started','onboarding_step_viewed')) AS cc
  FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib = 'posthog-flutter'
  GROUP BY person_id
  HAVING countIf(event IN ('onboarding_started','onboarding_step_viewed')) > 0
     AND countIf(properties.$is_testflight = true OR properties.$is_emulator = true OR properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro')) = 0
     AND countIf(event = 'onboarding_reset') = 0 AND countIf(event = 'onboarding_completed') < 3
     AND ob_ts >= toDateTime('2026-10-10 00:00:00')
)

-- @@ step_funnel
WITH coh AS (...)
SELECT period, si, sn, count() AS viewed_users, countIf(done) AS completed_users, countIf(skipped) AS skipped_users,
  round(quantileIf(0.5)(dwell_s, done AND dwell_s >= 0 AND dwell_s < 3600)) AS median_dwell_s
FROM (
  SELECT e.person_id AS pid, coh.period AS period, toString(e.properties.step_index) AS si, toString(e.properties.step_name) AS sn,
    countIf(e.event='onboarding_step_completed') > 0 AS done,
    countIf(e.event='onboarding_step_completed' AND e.properties.outcome='skipped') > 0 AS skipped,
    dateDiff('second', minIf(e.timestamp, e.event='onboarding_step_viewed'), minIf(e.timestamp, e.event='onboarding_step_completed')) AS dwell_s
  FROM events e INNER JOIN coh ON e.person_id = coh.person_id
  WHERE e.timestamp > now() - INTERVAL 30 DAY AND e.event IN ('onboarding_step_viewed','onboarding_step_completed') AND e.properties.$lib='posthog-flutter'
  GROUP BY pid, period, si, sn
) GROUP BY period, si, sn ORDER BY period, toIntOrZero(si), viewed_users DESC LIMIT 80

-- @@ cohort_flow
WITH coh AS (...)
SELECT period, count() AS starters, countIf(c_done) AS onb_completed, countIf(build) AS build_viewed, countIf(fc_intro) AS fc_intro, countIf(fc_dism) AS fc_intro_dismissed, countIf(fc_start) AS fc_started, countIf(fc_end) AS fc_ended, countIf(fc_recap) AS fc_recap,
  countIf(pw) AS paywall_any, countIf(pw_po) AS paywall_post_onb, countIf(offer_shown) AS offer_shown, countIf(offer_res) AS offer_result, countIf(not_shown) AS offer_not_shown, countIf(purchase) AS purchase,
  countIf(np) AS notif_prompted, countIf(ng) AS notif_granted, countIf(nd) AS notif_denied, countIf(mic) AS mic_result, countIf(fcp) AS first_capture_prompt, countIf(fwf) AS fw_plan_failed, countIf(fwr) AS fw_recap_viewed, countIf(fwa) AS fw_any
FROM (
  SELECT e.person_id AS pid, any(coh.period) AS period,
    countIf(e.event='onboarding_completed')>0 AS c_done, countIf(e.event='post_onboarding_build_viewed')>0 AS build,
    countIf(e.event='first_conversation_intro_viewed')>0 AS fc_intro, countIf(e.event='first_conversation_intro_dismissed')>0 AS fc_dism,
    countIf(e.event='first_conversation_started')>0 AS fc_start, countIf(e.event='first_conversation_ended')>0 AS fc_end, countIf(e.event='first_conversation_recap_result')>0 AS fc_recap,
    countIf(e.event='paywall_shown')>0 AS pw, countIf(e.event='paywall_shown' AND e.properties.trigger_feature IN ('post_onboarding','post_onboarding_all_plans'))>0 AS pw_po,
    countIf(e.event='post_onboarding_offer_shown')>0 AS offer_shown, countIf(e.event='post_onboarding_offer_result')>0 AS offer_res, countIf(e.event='post_onboarding_offer_not_shown')>0 AS not_shown,
    countIf(e.event='subscription_purchase_completed')>0 AS purchase,
    countIf(e.event='notification_permission_prompted')>0 AS np, countIf(e.event='notification_permission_granted')>0 AS ng, countIf(e.event='notification_permission_denied')>0 AS nd,
    countIf(e.event='mic_permission_result')>0 AS mic, countIf(e.event='first_capture_prompt_shown')>0 AS fcp,
    countIf(e.event='first_week_plan_failed')>0 AS fwf, countIf(e.event='first_week_recap_viewed')>0 AS fwr, countIf(e.event LIKE 'first_week%')>0 AS fwa
  FROM events e INNER JOIN coh ON e.person_id = coh.person_id
  WHERE e.timestamp > now() - INTERVAL 30 DAY GROUP BY pid
) GROUP BY period ORDER BY period

-- @@ activation_windows
WITH coh AS (...)
SELECT period, count() AS n, countIf(ob_ts < now() - INTERVAL 24 HOUR) AS elig24,
  countIf(conv6) AS conv_6h, countIf(voice6) AS voice_6h, countIf(conv24 AND ob_ts < now() - INTERVAL 24 HOUR) AS conv_24h, countIf(voice24 AND ob_ts < now() - INTERVAL 24 HOUR) AS voice_24h,
  countIf(cap24 AND ob_ts < now() - INTERVAL 24 HOUR) AS capture_24h, round(quantileIf(0.5)(min_to_conv, min_to_conv >= 0)) AS median_min_to_first_conv
FROM (
  SELECT e.person_id AS pid, any(coh.period) AS period, any(coh.ob_ts) AS ob_ts,
    countIf(e.event IN ('voice_chat_started','first_conversation_started','reflect_message_submitted','reflect_session_started') AND e.timestamp <= coh.ob_ts + INTERVAL 6 HOUR)>0 AS conv6,
    countIf(e.event IN ('voice_chat_started','first_conversation_started') AND e.timestamp <= coh.ob_ts + INTERVAL 6 HOUR)>0 AS voice6,
    countIf(e.event IN ('voice_chat_started','first_conversation_started','reflect_message_submitted','reflect_session_started') AND e.timestamp <= coh.ob_ts + INTERVAL 24 HOUR)>0 AS conv24,
    countIf(e.event IN ('voice_chat_started','first_conversation_started') AND e.timestamp <= coh.ob_ts + INTERVAL 24 HOUR)>0 AS voice24,
    countIf(e.event IN ('recording_saved','quick_capture_submitted','prep_capture_submitted','debrief_started') AND e.timestamp <= coh.ob_ts + INTERVAL 24 HOUR)>0 AS cap24,
    dateDiff('minute', any(coh.ob_ts), minIf(e.timestamp, e.event IN ('voice_chat_started','first_conversation_started','reflect_message_submitted','reflect_session_started'))) AS min_to_conv
  FROM events e INNER JOIN coh ON e.person_id = coh.person_id
  WHERE e.timestamp > now() - INTERVAL 30 DAY AND e.timestamp >= coh.ob_ts
  GROUP BY pid
) GROUP BY period ORDER BY period

-- @@ permission_values
WITH coh AS (...)
SELECT coh.period AS period, e.event AS event, toString(e.properties.result) AS result, toString(e.properties.source) AS src, count(DISTINCT e.person_id) AS users
FROM events e INNER JOIN coh ON e.person_id = coh.person_id
WHERE e.timestamp > now() - INTERVAL 30 DAY AND e.event IN ('mic_permission_result','notification_permission_prompted','notification_permission_granted','notification_permission_denied','push_prompt_result','post_onboarding_offer_result','first_week_plan_failed')
GROUP BY period, event, result, src ORDER BY period, event, users DESC LIMIT 60

-- @@ new_client_daily_os_since_1001
WITH nw AS (
  SELECT person_id, minIf(timestamp, properties.$lib='posthog-flutter') AS fts,
    argMinIf(properties.$os, timestamp, properties.$lib='posthog-flutter') AS os,
    countIf(event IN ('onboarding_started','onboarding_step_viewed'))>0 AS onb,
    countIf(event='user_registered')>0 AS reg,
    countIf(properties.$is_testflight = true OR properties.$is_emulator = true OR properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro'))>0 AS tdev
  FROM events WHERE timestamp > now() - INTERVAL 200 DAY
  GROUP BY person_id HAVING countIf(properties.$lib='posthog-flutter')>0 AND fts >= toDateTime('2026-10-01 00:00:00')
)
SELECT toDate(fts) AS d, countIf(NOT tdev) AS new_clients, countIf(NOT tdev AND os='Android') AS android, countIf(NOT tdev AND os IN ('iOS','iPadOS')) AS ios, countIf(NOT tdev AND onb) AS with_onb, countIf(NOT tdev AND reg) AS with_reg, countIf(tdev) AS tester_dev
FROM nw GROUP BY d ORDER BY d

-- @@ new_client_by_hour_since_1018  (ta sama CTE nw z dodatkowymi polami cc, lang, ver, src; grupowanie po toStartOfHour(fts))

-- @@ be_reg_by_day
WITH r AS (SELECT person_id, min(timestamp) AS rts FROM events WHERE event='user_registered' AND timestamp >= toDateTime('2026-10-01 00:00:00') GROUP BY person_id),
t AS (SELECT person_id, any(properties.platform) AS plat FROM events WHERE event='trial_started' AND timestamp >= toDateTime('2026-09-30 00:00:00') GROUP BY person_id)
SELECT toDate(r.rts) AS d, count() AS reg, countIf(t.plat='ios') AS ios, countIf(t.plat='android') AS android, countIf(t.plat IS NULL OR t.plat='') AS no_trial
FROM r LEFT JOIN t ON r.person_id = t.person_id GROUP BY d ORDER BY d

-- @@ reg_by_week_platform_client
WITH r AS (SELECT person_id, toStartOfWeek(min(timestamp)) AS w, any(properties.auth_provider) AS ap FROM events WHERE event='user_registered' AND timestamp >= toDateTime('2026-09-20 00:00:00') GROUP BY person_id),
t AS (SELECT person_id, any(properties.platform) AS plat FROM events WHERE event='trial_started' AND timestamp >= toDateTime('2026-09-20 00:00:00') GROUP BY person_id),
x AS (SELECT person_id FROM events WHERE timestamp >= toDateTime('2026-09-15 00:00:00') AND properties.$lib='posthog-flutter' GROUP BY person_id)
SELECT r.w AS week, t.plat AS plat, r.ap AS auth, count() AS registered, countIf(r.person_id NOT IN (SELECT person_id FROM x)) AS no_client_events
FROM r LEFT JOIN t ON r.person_id = t.person_id GROUP BY week, plat, auth ORDER BY week, plat, auth

-- @@ be_registrant_funnel
WITH r AS (SELECT person_id, min(timestamp) AS rts, any(properties.auth_provider) AS ap FROM events WHERE event='user_registered' AND timestamp >= toDateTime('2026-10-10 00:00:00') GROUP BY person_id),
t AS (SELECT person_id, any(properties.platform) AS plat FROM events WHERE event='trial_started' AND timestamp >= toDateTime('2026-10-09 00:00:00') GROUP BY person_id),
x AS (SELECT person_id FROM events WHERE timestamp >= toDateTime('2026-10-05 00:00:00') AND properties.$lib='posthog-flutter' GROUP BY person_id),
e AS (SELECT r.person_id AS pid, any(r.rts) AS reg_ts,
   countIf(ev.event='profile_updated' AND toString(ev.properties.is_first_save) IN ('true','1'))>0 AS onb_saved,
   countIf(ev.event='consent_granted' AND ev.properties.consent_type='ARTICLE9_HEALTH')>0 AS art9,
   countIf(ev.event='reflect_session_started' AND ev.timestamp <= r.rts + INTERVAL 6 HOUR)>0 AS rs6,
   countIf(ev.event='reflect_session_started' AND ev.properties.mode='voice' AND ev.timestamp <= r.rts + INTERVAL 6 HOUR)>0 AS rsv6,
   countIf(ev.event='reflect_session_started' AND ev.timestamp <= r.rts + INTERVAL 24 HOUR)>0 AS rs24,
   countIf(ev.event='reflect_session_started' AND ev.properties.mode='voice' AND ev.timestamp <= r.rts + INTERVAL 24 HOUR)>0 AS rsv24,
   countIf(ev.event='user_activated' AND toString(ev.properties.is_within_24h) IN ('true','1'))>0 AS act24,
   countIf(ev.event='subscription_purchase_completed')>0 AS purch
  FROM events ev INNER JOIN r ON ev.person_id = r.person_id
  WHERE ev.timestamp >= toDateTime('2026-10-10 00:00:00') AND ev.timestamp >= r.rts - INTERVAL 1 HOUR
  GROUP BY pid)
SELECT if(e.reg_ts >= toDateTime('2026-10-19 18:00:00'), 'R_since_1019_18h', 'C_1010_1019') AS coh,
  coalesce(t.plat, 'none') AS plat, e.pid IN (SELECT person_id FROM x) AS client_visible,
  count() AS reg, countIf(e.reg_ts < now() - INTERVAL 24 HOUR) AS elig24,
  countIf(onb_saved) AS onb_saved, countIf(art9) AS art9, countIf(rs6) AS reflect_6h, countIf(rsv6) AS voice_6h,
  countIf(rs24 AND e.reg_ts < now() - INTERVAL 24 HOUR) AS reflect_24h_elig, countIf(rsv24 AND e.reg_ts < now() - INTERVAL 24 HOUR) AS voice_24h_elig,
  countIf(act24) AS activated24, countIf(purch) AS purchased
FROM e LEFT JOIN t ON e.pid = t.person_id
GROUP BY coh, plat, client_visible ORDER BY coh, plat, client_visible

-- @@ dark_vs_visible_backend_mix
WITH r AS (SELECT person_id FROM events WHERE event='user_registered' AND timestamp >= toDateTime('2026-10-10 00:00:00') GROUP BY person_id),
t AS (SELECT person_id FROM events WHERE event='trial_started' AND properties.platform='ios' AND timestamp >= toDateTime('2026-10-09 00:00:00') GROUP BY person_id),
x AS (SELECT person_id FROM events WHERE timestamp >= toDateTime('2026-10-05 00:00:00') AND properties.$lib='posthog-flutter' GROUP BY person_id)
SELECT ev.person_id IN (SELECT person_id FROM x) AS visible, ev.event AS event, if(ev.event='profile_updated', toString(ev.properties.write_path), if(ev.event='api_error', toString(ev.properties.endpoint), '')) AS detail, count() AS c, count(DISTINCT ev.person_id) AS users
FROM events ev WHERE ev.timestamp >= toDateTime('2026-10-10 00:00:00') AND ev.person_id IN (SELECT person_id FROM r) AND ev.person_id IN (SELECT person_id FROM t)
  AND ev.event NOT IN ('moment.expired','moment.scheduled','$set','$set_once')
GROUP BY visible, event, detail ORDER BY visible, users DESC LIMIT 60

-- @@ welcome_auth_by_version
SELECT properties.$os AS os, properties.$app_version = '2.0.117' AS v117,
  countDistinctIf(person_id, event='$screen' AND properties.$screen_name='welcome') AS welcome, countDistinctIf(person_id, event='welcome_cta_tapped') AS cta,
  countDistinctIf(person_id, event='$screen' AND properties.$screen_name='auth') AS auth_screen, countDistinctIf(person_id, event='auth_method_tapped') AS auth_tap,
  countDistinctIf(person_id, event='signup_started') AS signup, countDistinctIf(person_id, event='login_failed') AS login_failed, countDistinctIf(person_id, event='onboarding_started') AS onb
FROM events WHERE timestamp >= toDateTime('2026-10-10 00:00:00') AND properties.$lib='posthog-flutter' AND properties.$os IN ('Android','iOS')
GROUP BY os, v117 ORDER BY os, v117
```
