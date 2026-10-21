# Lejek onboardingu i aktywacji, przed i po redesignie 03.10: surowy wyciąg z PostHog

- **Data**: 2026-10-15 · **Agent**: posthog-data-extractor
- **Projekt**: PostHog EU 141170 · **Okno**: 2026-09-15 → 2026-10-15 (30 dni, UTC)
- **Pytanie**: gdzie odpadają nowi użytkownicy w onboardingu i co robią w pierwszym tygodniu; porównanie przed i po 03.10 (redesign onboardingu + głosowy Reflect + paywall, od 05.10 pierwsza rozmowa v2, od ok. 09-10.10 plan pierwszego tygodnia).
- **Weryfikacja zdarzeń** (30 dni, `$lib`, użytkownicy):
  - płyną: `onboarding_started` (flutter, 69 os.), `onboarding_step_viewed` (84), `onboarding_step_completed` (73, prop `outcome` = saved/skipped dla kroków pomijalnych), `onboarding_completed` (50), `post_onboarding_build_viewed`/`_finished` (31, od 03.10), `first_conversation_intro_viewed` (22) / `_started` (20) / `_ended` (16) / `_recap_result` (15), wszystkie od 05.10; `post_onboarding_offer_shown` (9, od 09.10), `post_onboarding_offer_result` (14), `paywall_shown` (26), `voice_chat_started` (17), `reflect_message_submitted` (flutter, 23), `habit_created` (13), `habit_check_toggled` (11), `debrief_started` (24), `recording_saved` (18), `quick_capture_submitted` (8), `prep_capture_submitted` (8), `workspace_opened` (46), `trial_started` i `user_registered` (backend).
  - właściwości kroku: `step_name` i `step_index` na 734/734 `onboarding_step_viewed`. Język: brak właściwości języka aplikacji na krokach, użyto `$locale` urządzenia (2 pierwsze znaki). `onboarding_language_changed` tylko 2 os.
  - plan pierwszego tygodnia: `first_week_plan_toggled` 3 os., `_hidden`/`_hide_undone` po 1, `first_week_plan_failed` 2 os. Za mało do analizy (n<5). Zdarzenia ekspozycji (`first_week_plan_shown`/`_viewed`) nie ma w danych, więc nie da się policzyć, ile osób plan zobaczyło.

## Definicja kohorty

Osoba (`person_id`) ze zdarzeniem `onboarding_started` lub `onboarding_step_viewed` (`$lib='posthog-flutter'`) w oknie. Okres = data pierwszego takiego zdarzenia: **A = przed 03.10** (15.09-02.10), **B = od 03.10**. Wykluczeni: osoby z jakimkolwiek zdarzeniem `$is_testflight=true`, `$is_emulator=true`, `$device_model IN ('OnePlus8Pro','Pixel 6 Pro')` (9 os.), testerzy: `onboarding_reset` albo `onboarding_completed` >= 3 (3 os.). Zostaje 74 (A 36, B 38).

## 1. Lejek krok po kroku (użytkownicy)

`step_index` -1 = `personalise` (przed bramką prawną). Kroki `modality` i `schedule` w B są warunkowe (pokazywane tylko części osób po `journey`), w A widzieli je wszyscy.

| krok (index) | A widziało | A ukończyło | A pominęło | A mediana s | B widziało | B ukończyło | B pominęło | B mediana s |
|---|---|---|---|---|---|---|---|---|
| start onboardingu | 36 | | | | 38 | | | |
| personalise (-1) | 35 | 31 | 0 | 23 | 38 | 35 | 0 | 17 |
| legal_gate (0) | 28 | 23 | 0 | 18 | 32 | 29 | 0 | 10 |
| challenges (1) | 24 | 22 | 0 | 21 | 29 | 29 | 0 | 20 |
| intensity (2) | 22 | 22 | 0 | 13 | 29 | 29 | 0 | 16 |
| journey (3) | 22 | 22 | 0 | 14 | 29 | 29 | 9 | 11 |
| modality (4) | 22 | 22 | 0 | 10 | 10 | 10 | 0 | 15 |
| schedule (5) | 22 | 22 | 0 | 6 | 10 | 10 | n<5 | 9 |
| companion (6) | 22 | 17 | 0 | 38 | 29 | 28 | 0 | 42 |
| lead_source (7) | 17 | 17 | 0 | 6 | 28 | 28 | n<5 | 8 |
| `onboarding_completed` | **17 (47%)** | | | | **28 (74%)** | | | |

Mediana czasu = mediana (pierwsze `completed` minus pierwsze `viewed`) per osoba, tylko osoby, które ukończyły krok, z odcięciem > 1 h.

Ciąg dalszy po onboardingu (tylko B, w A te zdarzenia nie istniały):

| etap B | użytkownicy | % startów (38) |
|---|---|---|
| `onboarding_completed` | 28 | 74% |
| `post_onboarding_build_viewed` | 26 | 68% |
| `first_conversation_intro_viewed` | 17 | 45% |
| `first_conversation_started` | 15 | 39% |
| `first_conversation_ended` | 11 | 29% |
| `first_conversation_recap_result` | 10 | 26% |
| `paywall_shown` trigger `post_onboarding*` | 12 | 32% |
| `post_onboarding_offer_shown` (od 09.10) | 8 | 21% |
| `post_onboarding_offer_result` | 9 | 24% |
| `post_onboarding_offer_not_shown` | 0 | 0% |
| `subscription_purchase_completed` | n<5 | |

A: `subscription_purchase_completed` n<5.

**Największe porzucenia:**
- A: `personalise` → `legal_gate` (35 → 28 widzi, 20%), `legal_gate` nieukończony (28 → 23), `companion` (22 → 17, 23%, najdłuższy krok, 38 s).
- B: `personalise` → `legal_gate` (38 → 32, 16%), `legal_gate` → `challenges` (32 → 29). `companion` w B prawie bez strat (29 → 28), choć dalej najdłuższy (42 s).
- B po onboardingu: **build → intro pierwszej rozmowy: 26 → 17 (35% strat)**, dziś największa pojedyncza dziura; potem start → koniec rozmowy 15 → 11.

## 2. Platforma i język (`$locale` urządzenia), start → `onboarding_completed`

| okres | OS | język | startów | ukończyło |
|---|---|---|---|---|
| A | Android | en | 16 | 8 |
| A | Android | fr | 7 | n<5 |
| A | Android | ar | 5 | n<5 |
| A | iOS | en | n<5 | n<5 |
| A | iPadOS | en | n<5 | n<5 |
| A | Android | it / tr / ru | n<5 każdy | n<5 |
| B | Android | en | 20 | 15 |
| B | Android | pl, sv, pt, fr, ro, fa, bn, tr, zh, ru | n<5 każdy | n<5 |
| B | iOS | en | n<5 | n<5 |

Sumarycznie: Android 67 z 74 startów, iOS + iPadOS 7. Za mało, żeby mówić o różnicy platform lub języków; jedyny porównywalny segment to Android/en: 8/16 (50%) w A vs 15/20 (75%) w B.

## 3. Aktywacja (od pierwszego zdarzenia onboardingu)

Definicje: rozmowa = `voice_chat_started` / `first_conversation_started` / `reflect_message_submitted` / `reflect_session_started`; głos = `voice_chat_started` / `first_conversation_started`; Reflect tekst = `reflect_message_submitted`; wpis = `recording_saved` / `quick_capture_submitted` / `prep_capture_submitted` / `debrief_started`; nawyk = `habit_created` / `habit_check_toggled`. "Nic" = brak rozmowy, wpisu i nawyku (obejmuje też osoby, które nie skończyły onboardingu).

24 h (kwalifikują się osoby z pierwszym zdarzeniem > 24 h temu):

| okres | n | dowolna rozmowa | głos | Reflect tekst | wpis | nawyk | nic |
|---|---|---|---|---|---|---|---|
| A | 36 | 5 (14%) | n<5 | n<5 | n<5 | n<5 | 30 (83%) |
| B | 36 | 15 (42%) | 14 (39%) | 11 (31%) | 5 (14%) | n<5 | 18 (50%) |

7 dni (kwalifikują się osoby z pierwszym zdarzeniem > 7 dni temu; B = tylko 03.10-08.10):

| okres | n | dowolna rozmowa | głos | Reflect tekst | wpis | nawyk | nic |
|---|---|---|---|---|---|---|---|
| A | 36 | 5 (14%) | n<5 | n<5 | 6 (17%) | n<5 | 28 (78%) |
| B | 14 | n<5 | 0 | n<5 | n<5 | n<5 | 10 (71%) |

Kontrola: ta sama 14-osobowa podgrupa B w 24 h: `onboarding_completed` 6, rozmowa n<5, nic 10. Wczesna grupa B (03-08.10) wypadła słabo, bo pierwsza rozmowa v2 weszła 05.10 i docierała stopniowo z nowymi buildami; poprawa w tabeli 24 h pochodzi z osób z 08-14.10. Siedmiodniowej aktywacji dla nowego przepływu jeszcze nie da się zmierzyć.

Wczesny powrót w B (onboarding > 3 dni temu; powrót = dowolne zdarzenie klienta w innym dniu kalendarzowym w ciągu 3 dni):

| rozmowa w 24 h | n | wróciło D1-D3 |
|---|---|---|
| tak | 13 | 5 (38%) |
| nie | 20 | 5 (25%) |

## 4. Kandydat na moment "aha": tydzień 1 vs powrót w tygodniu 2

Kohorta: onboarding > 14 dni temu, czyli **wyłącznie okres A** (15.09-30.09), n = 33. Powrót = dowolne zdarzenie klienta w dniach 7-14. Bazowo wróciło 6/33 (18%).

| działanie w tygodniu 1 | zrobiło | z nich wróciło | nie zrobiło | z nich wróciło |
|---|---|---|---|---|
| ukończony onboarding | 17 | 6 (35%) | 16 | 0 |
| ≥ 2 aktywne dni w tyg. 1 | 25 | 6 (24%) | 8 | 0 |
| `timeline_viewed` | 17 | 6 (35%) | 16 | 0 |
| `workspace_opened` | 15 | 5 (33%) | 18 | n<5 |
| **wpis (głównie `debrief_started`)** | **6** | **5 (83%)** | 27 | n<5 |
| dowolna rozmowa | 5 | n<5 | 28 | n<5 |
| głos / Reflect tekst / nawyk | n<5 każde | n<5 | 30 | n<5 |

Rozbicie wpisów w tyg. 1: `debrief_started` 6 os. (5 wróciło), `recording_saved` n<5, `prep_capture_submitted` n<5, `quick_capture_submitted` n<5.

`timeline_viewed` pokrywa się 1:1 z ukończeniem onboardingu (17/17), więc wygląda na zdarzenie odpalane przy wejściu na ekran główny, a nie na świadome działanie. Nie traktować go jako kandydata.

## Zastrzeżenia

- Bardzo małe liczby: 74 osoby w kohorcie, procenty mają szerokie przedziały niepewności. Wynik "aha" (wpis po sesji) stoi na 6 osobach: to hipoteza, nie dowód.
- Analiza tygodnia 2 obejmuje tylko kohortę sprzed redesignu; dla B za wcześnie (najstarsze osoby B mają 12 dni).
- Okres B obejmuje mieszankę buildów: nowy onboarding od `$app_version` 2.0.97, pierwsza rozmowa v2 od 05.10. Część osób B mogła mieć starszy build.
- `$locale` to język urządzenia, nie wybrany język aplikacji.
- Plan pierwszego tygodnia: brak zdarzenia ekspozycji, 3 osoby z interakcją, nie do zmierzenia.
- Ingest od 2026-04-22 nie ogranicza tego okna. Osoby, które zaczęły onboarding przed 15.09 i kontynuowały w oknie, trafiają do A z datą pierwszego zdarzenia w oknie.
- `reflect_message_submitted` może też padać w pierwszej rozmowie, więc kategorie "głos" i "Reflect tekst" mogą się nakładać.
- Wykluczenia testerów są heurystyczne (reset onboardingu, ≥ 3 ukończenia).

## Zapytania (HogQL, dosłownie)

```sql
-- Every section below starts with the same cohort CTE `coh` (written out in full in the
-- act_24h_among_7d_eligible / aha sections further down); here it is abbreviated as WITH coh AS (...).

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
) GROUP BY period, si, sn ORDER BY period, si, viewed_users DESC LIMIT 80

-- @@ cohort_flow
WITH coh AS (...)
SELECT period, count() AS starters, countIf(c_done) AS onb_completed, countIf(build) AS post_build_viewed,
  countIf(fc_intro) AS fc_intro_viewed, countIf(fc_start) AS fc_started, countIf(fc_end) AS fc_ended,
  countIf(fc_recap) AS fc_recap, countIf(pw_po) AS paywall_post_onb, countIf(offer_shown) AS offer_shown_ev, countIf(offer_res) AS offer_result_ev, countIf(not_shown) AS offer_not_shown, countIf(purchase) AS purchase_ev
FROM (
  SELECT e.person_id AS pid, any(coh.period) AS period,
    countIf(e.event='onboarding_completed')>0 AS c_done,
    countIf(e.event='post_onboarding_build_viewed')>0 AS build,
    countIf(e.event='first_conversation_intro_viewed')>0 AS fc_intro,
    countIf(e.event='first_conversation_started')>0 AS fc_start,
    countIf(e.event='first_conversation_ended')>0 AS fc_end,
    countIf(e.event='first_conversation_recap_result')>0 AS fc_recap,
    countIf(e.event='paywall_shown' AND e.properties.trigger_feature IN ('post_onboarding','post_onboarding_all_plans'))>0 AS pw_po,
    countIf(e.event='post_onboarding_offer_shown')>0 AS offer_shown,
    countIf(e.event='post_onboarding_offer_result')>0 AS offer_res,
    countIf(e.event='post_onboarding_offer_not_shown')>0 AS not_shown,
    countIf(e.event='subscription_purchase_completed')>0 AS purchase
  FROM events e INNER JOIN coh ON e.person_id = coh.person_id
  WHERE e.timestamp > now() - INTERVAL 30 DAY
  GROUP BY pid
) GROUP BY period ORDER BY period

-- @@ split_os_lang
WITH coh AS (...)
SELECT period, os, lang, count() AS starters, countIf(c_done) AS completed
FROM (
  SELECT coh.person_id AS pid, any(coh.period) AS period, any(coh.os) AS os, any(coh.lang) AS lang,
    countIf(e.event='onboarding_completed')>0 AS c_done
  FROM events e INNER JOIN coh ON e.person_id = coh.person_id
  WHERE e.timestamp > now() - INTERVAL 30 DAY AND e.event IN ('onboarding_completed','onboarding_started','onboarding_step_viewed')
  GROUP BY pid
) GROUP BY period, os, lang ORDER BY period, starters DESC LIMIT 60

-- @@ act_24h  (act_7d = identical with INTERVAL 7 DAY in every place where 1 DAY appears)
WITH coh AS (...)
SELECT period, count() AS eligible, countIf(f_conv) AS any_conversation, countIf(f_voice) AS voice_conv, countIf(f_rt) AS reflect_text_msg, countIf(f_cap) AS capture_entry, countIf(f_hab) AS habit, countIf(NOT f_conv AND NOT f_cap AND NOT f_hab) AS did_nothing_core
FROM (
  SELECT coh.person_id AS pid, any(coh.period) AS period,
    countIf(e.event IN ('voice_chat_started','first_conversation_started','reflect_message_submitted','reflect_session_started') AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_conv,
    countIf(e.event IN ('voice_chat_started','first_conversation_started') AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_voice,
    countIf(e.event = 'reflect_message_submitted' AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_rt,
    countIf(e.event IN ('recording_saved','quick_capture_submitted','prep_capture_submitted','debrief_started') AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_cap,
    countIf(e.event IN ('habit_created','habit_check_toggled') AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_hab
  FROM coh LEFT JOIN events e ON e.person_id = coh.person_id
  WHERE coh.ob_ts < now() - INTERVAL 1 DAY AND e.timestamp > now() - INTERVAL 31 DAY AND e.timestamp >= coh.ob_ts
  GROUP BY pid
) GROUP BY period ORDER BY period

-- @@ act_24h_among_7d_eligible
WITH coh AS (
  SELECT person_id, minIf(timestamp, event IN ('onboarding_started','onboarding_step_viewed')) AS ob_ts,
    if(ob_ts < toDateTime('2026-10-03 00:00:00'), 'A_pre_0310', 'B_post_0310') AS period,
    any(properties.$os) AS os, any(substring(properties.$locale,1,2)) AS lang
  FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib = 'posthog-flutter'
  GROUP BY person_id
  HAVING countIf(event IN ('onboarding_started','onboarding_step_viewed')) > 0
     AND countIf(properties.$is_testflight = true OR properties.$is_emulator = true OR properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro')) = 0
     AND countIf(event = 'onboarding_reset') = 0 AND countIf(event = 'onboarding_completed') < 3
)
SELECT period, count() AS eligible, countIf(onbc) AS onb_completed_24h, countIf(f_conv) AS any_conversation, countIf(f_voice) AS voice_conv, countIf(f_rt) AS reflect_text_msg, countIf(f_cap) AS capture_entry, countIf(f_hab) AS habit, countIf(NOT f_conv AND NOT f_cap AND NOT f_hab) AS did_nothing_core
FROM (
  SELECT coh.person_id AS pid, any(coh.period) AS period,
    countIf(e.event IN ('voice_chat_started','first_conversation_started','reflect_message_submitted','reflect_session_started') AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_conv,
    countIf(e.event IN ('voice_chat_started','first_conversation_started') AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_voice,
    countIf(e.event = 'reflect_message_submitted' AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_rt,
    countIf(e.event IN ('recording_saved','quick_capture_submitted','prep_capture_submitted','debrief_started') AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_cap,
    countIf(e.event IN ('habit_created','habit_check_toggled') AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS f_hab,
    countIf(e.event='onboarding_completed' AND e.timestamp <= coh.ob_ts + INTERVAL 1 DAY)>0 AS onbc
  FROM coh LEFT JOIN events e ON e.person_id = coh.person_id
  WHERE coh.ob_ts < now() - INTERVAL 7 DAY AND e.timestamp > now() - INTERVAL 31 DAY AND e.timestamp >= coh.ob_ts
  GROUP BY pid
) GROUP BY period ORDER BY period

-- @@ aha
WITH coh AS (
  SELECT person_id, minIf(timestamp, event IN ('onboarding_started','onboarding_step_viewed')) AS ob_ts,
    if(ob_ts < toDateTime('2026-10-03 00:00:00'), 'A_pre_0310', 'B_post_0310') AS period,
    any(properties.$os) AS os, any(substring(properties.$locale,1,2)) AS lang
  FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib = 'posthog-flutter'
  GROUP BY person_id
  HAVING countIf(event IN ('onboarding_started','onboarding_step_viewed')) > 0
     AND countIf(properties.$is_testflight = true OR properties.$is_emulator = true OR properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro')) = 0
     AND countIf(event = 'onboarding_reset') = 0 AND countIf(event = 'onboarding_completed') < 3
), pp AS (
  SELECT coh.person_id AS pid,
    countIf(e.event='onboarding_completed' AND e.timestamp < coh.ob_ts + INTERVAL 7 DAY)>0 AS a_onb,
    countIf(e.event IN ('voice_chat_started','first_conversation_started','reflect_message_submitted','reflect_session_started') AND e.timestamp < coh.ob_ts + INTERVAL 7 DAY)>0 AS a_conv,
    countIf(e.event IN ('voice_chat_started','first_conversation_started') AND e.timestamp < coh.ob_ts + INTERVAL 7 DAY)>0 AS a_voice,
    countIf(e.event='reflect_message_submitted' AND e.timestamp < coh.ob_ts + INTERVAL 7 DAY)>0 AS a_rt,
    countIf(e.event IN ('recording_saved','quick_capture_submitted','prep_capture_submitted','debrief_started') AND e.timestamp < coh.ob_ts + INTERVAL 7 DAY)>0 AS a_cap,
    countIf(e.event IN ('habit_created','habit_check_toggled') AND e.timestamp < coh.ob_ts + INTERVAL 7 DAY)>0 AS a_hab,
    countIf(e.event='workspace_opened' AND e.timestamp < coh.ob_ts + INTERVAL 7 DAY)>0 AS a_ws,
    countIf(e.event='timeline_viewed' AND e.timestamp < coh.ob_ts + INTERVAL 7 DAY)>0 AS a_tl,
    count(DISTINCT if(e.timestamp < coh.ob_ts + INTERVAL 7 DAY, toDate(e.timestamp), NULL)) AS d1,
    countIf(e.properties.$lib='posthog-flutter' AND e.timestamp >= coh.ob_ts + INTERVAL 7 DAY AND e.timestamp < coh.ob_ts + INTERVAL 14 DAY)>0 AS ret
  FROM events e INNER JOIN coh ON e.person_id = coh.person_id
  WHERE coh.ob_ts < now() - INTERVAL 14 DAY AND e.timestamp > now() - INTERVAL 31 DAY AND e.timestamp >= coh.ob_ts
  GROUP BY pid
)
SELECT count() AS n_all, countIf(ret) AS ret_all, countIf(a_onb) AS onb_n, countIf(a_onb AND ret) AS onb_r, countIf(NOT a_onb AND ret) AS onb_r_wo, countIf(a_conv) AS conv_n, countIf(a_conv AND ret) AS conv_r, countIf(NOT a_conv AND ret) AS conv_r_wo, countIf(a_voice) AS voice_n, countIf(a_voice AND ret) AS voice_r, countIf(NOT a_voice AND ret) AS voice_r_wo, countIf(a_rt) AS rt_n, countIf(a_rt AND ret) AS rt_r, countIf(NOT a_rt AND ret) AS rt_r_wo, countIf(a_cap) AS cap_n, countIf(a_cap AND ret) AS cap_r, countIf(NOT a_cap AND ret) AS cap_r_wo, countIf(a_hab) AS hab_n, countIf(a_hab AND ret) AS hab_r, countIf(NOT a_hab AND ret) AS hab_r_wo, countIf(a_ws) AS ws_n, countIf(a_ws AND ret) AS ws_r, countIf(NOT a_ws AND ret) AS ws_r_wo, countIf(a_tl) AS tl_n, countIf(a_tl AND ret) AS tl_r, countIf(NOT a_tl AND ret) AS tl_r_wo, countIf(d1 >= 2) AS d2_n, countIf(d1 >= 2 AND ret) AS d2_r, countIf(d1 < 2 AND ret) AS d2_r_wo, countIf((a_conv AND d1 >= 2)) AS convd2_n, countIf((a_conv AND d1 >= 2) AND ret) AS convd2_r, countIf(NOT (a_conv AND d1 >= 2) AND ret) AS convd2_r_wo FROM pp

-- @@ aha_capture_parts
WITH coh AS (
  SELECT person_id, minIf(timestamp, event IN ('onboarding_started','onboarding_step_viewed')) AS ob_ts,
    if(ob_ts < toDateTime('2026-10-03 00:00:00'), 'A_pre_0310', 'B_post_0310') AS period,
    any(properties.$os) AS os, any(substring(properties.$locale,1,2)) AS lang
  FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib = 'posthog-flutter'
  GROUP BY person_id
  HAVING countIf(event IN ('onboarding_started','onboarding_step_viewed')) > 0
     AND countIf(properties.$is_testflight = true OR properties.$is_emulator = true OR properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro')) = 0
     AND countIf(event = 'onboarding_reset') = 0 AND countIf(event = 'onboarding_completed') < 3
)
SELECT ev, count() AS users_w1, countIf(ret) AS returned_w2 FROM (
  SELECT e.person_id AS pid, e.event AS ev,
    any(coh.ob_ts) AS obt
  FROM events e INNER JOIN coh ON e.person_id = coh.person_id
  WHERE coh.ob_ts < now() - INTERVAL 14 DAY AND e.timestamp > now() - INTERVAL 31 DAY AND e.timestamp >= coh.ob_ts
    AND e.timestamp < coh.ob_ts + INTERVAL 7 DAY AND e.event IN ('recording_saved','quick_capture_submitted','prep_capture_submitted','debrief_started','workspace_opened')
  GROUP BY pid, ev
) x INNER JOIN (
  SELECT e.person_id AS rpid, countIf(e.properties.$lib='posthog-flutter' AND e.timestamp >= coh.ob_ts + INTERVAL 7 DAY AND e.timestamp < coh.ob_ts + INTERVAL 14 DAY)>0 AS ret
  FROM events e INNER JOIN coh ON e.person_id = coh.person_id
  WHERE coh.ob_ts < now() - INTERVAL 14 DAY AND e.timestamp > now() - INTERVAL 31 DAY AND e.timestamp >= coh.ob_ts
  GROUP BY rpid
) r ON x.pid = r.rpid
GROUP BY ev ORDER BY users_w1 DESC
-- @@ post_early_return_by_first_conv
WITH coh AS (
  SELECT person_id, minIf(timestamp, event IN ('onboarding_started','onboarding_step_viewed')) AS ob_ts,
    if(ob_ts < toDateTime('2026-10-03 00:00:00'), 'A_pre_0310', 'B_post_0310') AS period,
    any(properties.$os) AS os, any(substring(properties.$locale,1,2)) AS lang
  FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib = 'posthog-flutter'
  GROUP BY person_id
  HAVING countIf(event IN ('onboarding_started','onboarding_step_viewed')) > 0
     AND countIf(properties.$is_testflight = true OR properties.$is_emulator = true OR properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro')) = 0
     AND countIf(event = 'onboarding_reset') = 0 AND countIf(event = 'onboarding_completed') < 3
)
SELECT fc, count() AS n, countIf(ret) AS returned_d1_d3 FROM (
  SELECT e.person_id AS pid,
    countIf(e.event IN ('first_conversation_started','voice_chat_started','reflect_message_submitted') AND e.timestamp < coh.ob_ts + INTERVAL 1 DAY)>0 AS fc,
    countIf(e.properties.$lib='posthog-flutter' AND toDate(e.timestamp) > toDate(coh.ob_ts) AND e.timestamp < coh.ob_ts + INTERVAL 3 DAY)>0 AS ret
  FROM events e INNER JOIN coh ON e.person_id = coh.person_id
  WHERE coh.period = 'B_post_0310' AND coh.ob_ts < now() - INTERVAL 3 DAY AND e.timestamp > now() - INTERVAL 31 DAY AND e.timestamp >= coh.ob_ts
  GROUP BY pid
) GROUP BY fc
```
