# Zachowanie istniejących użytkowników po aktualizacji do 2.0.117 (redesign) - raw PostHog extract

- **Date**: 2026-10-21 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: po wydaniu 2026-10-19 18:00 -> 2026-10-21 ok. 17:00 UTC (ok. 47 h); tydzień porównawczy 2026-10-12 00:00 -> 2026-10-19 00:00 UTC
- **Question**: co robią na nowej wersji osoby, które zaktualizowały (ekrany, czas, ścieżki), jak zmieniło się użycie funkcji, czy są sygnały frustracji i luki instrumentacji.
- **Event verification**: pełny katalog zdarzeń na buildach 2.0.113-2.0.117 pobrany 2026-10-21 (162 nazwy, 14 osób z testerami). Nowe zdarzenia Main (`main_viewed`, `main_tile_viewed`, `main_tile_tapped`, `main_sheet_closed`, `main_sheet_action`, `main_week_*`), kart (`card_viewed`, `card_text_expanded`, `card_item_bookmark_toggled`, `period_card_extras_viewed`), Timeline (`timeline_filter_changed/_selected`) i Character KD v2 (`skill_map_opened`, `skill_opened`, `skill_path_selected`, `companion_opened`, `skill_moment_*`) płyną od 2026-10-19 06:51 (pierwszy build testerski 2.0.113). Na żadnym buildzie 2.0.113-2.0.117 nie pojawiło się `voice_chat_started`, `voice_chat_ended`, `mic_permission_result` ani `voice_engine_selected` (backend). `$rageclick` istnieje, ale tylko na iOS (patrz Luki).

## 0. Kto jest na nowej wersji (najważniejsze zastrzeżenie)

Build sklepowy z redesignem = **2.0.117** (Android build 188, iOS build 184, `$is_testflight=false`), pierwsze zdarzenie 2026-10-19 18:13 UTC. Buildy 2.0.111-2.0.116 to testerzy (TestFlight + kilka urządzeń Android).

Testerzy wykluczeni: każda osoba z 30 dni, która miała `$is_testflight=true`, build 2.0.111-2.0.116, `$is_emulator=true` albo `$device_model IN ('OnePlus8Pro','Pixel 6 Pro')` (25 osób). Do tego domyślnie `$lib='posthog-flutter'`.

| kohorta | definicja | osoby | z tego istniejące konta (zdarzenia przed 10-19) | sesje | zdarzenia |
|---|---|---|---|---|---|
| NEW_2.0.117 | realni na 2.0.117 po 10-19 18:00 | 7 | 3 | 8 | 505 |
| OLD_concurrent | realni po 10-19 18:00, bez 2.0.117 (głównie 2.0.110) | 10 | 8 | 11 | 195 |
| PRE | realni 10-12..10-18, dowolna wersja | 50 | 50 | 92 | 2145 |

Realni aktywni dziennie (wszystkie wersje) i adopcja:

| dzień (UTC) | realni aktywni | na 2.0.117 | na 2.0.110 | inne |
|---|---|---|---|---|
| 10-14 | 17 | 0 | 5 | 12 |
| 10-15 | 6 | 0 | 3 | 3 |
| 10-16 | 12 | 0 | 7 | 5 |
| 10-17 | 7 | 0 | 7 | 0 |
| 10-18 | 14 | 0 | 9 | 5 |
| 10-19 | 15 | 0 | 11 | 4 |
| 10-20 | 8 | 3 | 4 | 1 |
| 10-21 (do ok. 17:00) | 6 | 5 | 0 | 1 |

Wniosek dla całego raportu: **istniejących użytkowników, którzy zaktualizowali, jest 3 (wszyscy Android)**. Pozostałe 4 osoby na 2.0.117 to nowe instalacje (onboarding). Porównanie "ci sami ludzie przed i po" przy n=3 jest niemożliwe i nie raportuję go. Poniżej porównuję kohorty (7 vs 10 vs 50), wszystkie liczby osób < 25 są małą próbą, a < 5 są ukryte jako n<5. Dzienna liczba aktywnych 10-20 i 10-21 (8 i 6) mieści się w zakresie poprzedniego tygodnia (6-17), więc nie ma dowodu na odpływ po wydaniu, ale też nie ma jeszcze danych, żeby go wykluczyć.

Kontrola "cichego klienta" (czy 2.0.117 mógł zgubić PostHoga): od 10-19 18:00 każda osoba z backendowym `reflect_session_started` (5 os.) i `api_error` (11 os., 10 z nich ma też zdarzenia klienta) ma zdarzenia klienta w tym samym oknie. Brak śladu, że nowy build przestał wysyłać zdarzenia.

## 1. Ekrany, zakładki, czas

`$screen` (osoby / zdarzenia na osobę liczone tylko tam, gdzie osób >= 5):

| ekran | NEW_2.0.117 | OLD_concurrent | PRE (50) |
|---|---|---|---|
| splash | 5 | 9 | 47 |
| welcome | n<5 | n<5 | 35 |
| mainPage | n<5 (61 zdarzeń) | n<5 | 19 (120 zdarzeń) |
| auth / signUp / wow / therapyOnboarding | n<5 | n<5 | 27 / 15 / 14 / 14 |
| betweenSessionsFlow, afterTherapyFlow, subscription, healthCheckFlow | n<5 | 0 | 5 / 4 / 5 / 2 |
| ke_map, ke_skill, workspaceAgenda, firstWeekRecap (nowe) | n<5 | 0 | 0 |
| mainPageTab, reflectModeChoice, firstWeekTrends, firstWeekHabits | 0 | n<5 | 4 / 4 / 3 / 3 |

`mainPageTab`, `firstWeekTrends`, `firstWeekHabits` zniknęły na 2.0.117 (stare ekrany, zastąpione nowym Main). `reflectModeChoice` też 0 na 2.0.117, ale `reflect_mode_selected` płynie (2 os.), więc to zmiana nazwy/trasy ekranu, nie brak Reflect.

Zakładki (`tab_switched`, surowe, z efektem przewijania przez PageView): na 2.0.117 każda zakładka n<5; PRE: therapy 12, reflect 11, main 11, workspace 10, character 10 osób. Na 2.0.117 Main jest liczony przez `main_viewed` (8 os. z testerami: regular 136 wyświetleń, first_week 7).

Sesje (zdarzenia szumu wyłączone: `usage_snapshot`, `$set`, `$identify`, `app_install_attributed`, `notification_permission_*`, błędy):

| kohorta | sesje | osoby | sesje/os. | mediana s | p90 s | mediana zdarzeń | < 10 s | >= 1 min | >= 5 min |
|---|---|---|---|---|---|---|---|---|---|
| NEW_2.0.117 | 8 | 7 | 1.1 | 149 | 2935 | 33 | 2 | 4 | 2 |
| OLD_concurrent | 11 | 10 | 1.1 | 104 | 366 | 8 | 4 | 6 | 2 |
| PRE | 92 | 50 | 1.8 | 38 | 524 | 7 | 32 | 39 | 17 |

Czas na osobę (suma sesji): mediana NEW 251 s, OLD_concurrent 109 s, PRE 65 s (mediana 1 aktywny dzień we wszystkich). Dłuższe sesje na 2.0.117 to głównie efekt składu: 4 z 7 osób to nowe instalacje przechodzące onboarding, a na nowym Main każde otwarcie arkusza generuje kilka zdarzeń. Nie da się z tego wnioskować o większym zaangażowaniu.

## 2. Ścieżki po starcie (pierwsze 4 kroki sesji, kafelki ładowania pominięte)

| kohorta | ścieżka | sesje |
|---|---|---|
| NEW_2.0.117 | splash > welcome > welcome_cta_tapped > auth (nowe konta) | 2 |
| NEW_2.0.117 | splash > mainPage > main_viewed > main_tile_tapped | 2-3 |
| NEW_2.0.117 | splash > mainPage > subscription | 1 |
| PRE | splash > welcome > welcome_cta_tapped > auth | 27 |
| PRE | splash > welcome (koniec) | 9 |
| PRE | splash > mainPage > first_capture_prompt_shown > ... | ok. 15 |
| PRE | notification_opened > mainPageTab / betweenSessionsFlow / myTherapy | ok. 7 |

Na nowej wersji zalogowana osoba zaczyna od Main i w pierwszych krokach tapie kafelek; na starej pierwszym krokiem był `first_capture_prompt_shown` albo `today_card_viewed`. Żadna sesja na 2.0.117 nie zaczęła się od otwarcia powiadomienia (n=7, okno 2 dni).

Koniec sesji (ostatnie zdarzenie): NEW: welcome 2, `main_sheet_closed` 2 (1 os.), reszta po 1 (mainPage, `quick_capture_abandoned`, `personal_reveal_viewed`, `bio_viewed`). PRE: welcome 12, splash 7, `first_capture_prompt_shown` 6, timeline 6, bio 6. Żaden ekran nie wyróżnia się jako miejsce porzucenia na 2.0.117.

## 3. Użycie funkcji (osoby; PRE = baza 50, z czego 21 zalogowanych w aplikacji; NEW zalogowani 4, OLD_concurrent zalogowani 4)

| funkcja | NEW_2.0.117 | OLD_concurrent | PRE | sygnał |
|---|---|---|---|---|
| Timeline (ładowanie) | n<5 | n<5 | 21 | bez zmian |
| Timeline filtr pigułki | 0 | 0 | n<5 | płynie u testerów (3 os.), realnie 0 |
| Workspace | n<5 (16 zd.) | 0 | 10 | płynie |
| Reflect tekst | n<5 | n<5 | 8 | płynie, backend `reflect_session_started` 3 os. na 2.0.117 |
| Threads | 0 | 0 | 6 | 0 realnych na 2.0.117; testerzy 2 os. (płynie) |
| Karty (A1-A11) | n<5 (18 zd.) | 0 | 5 | nowe zdarzenia płyną |
| Notatka głosowa | n<5 | 0 | 5 | płynie (`recording_saved` 3 os.) |
| Nawyki (tworzenie/odhaczanie) | n<5 | n<5 | 5 | płynie |
| Rozmowa głosowa Classic | **0** | n<5 | 5 | **0 na wszystkich nowych buildach**, patrz niżej |
| Rozmowa głosowa Live | 0 | 0 | 0 | 0 poza testerem 10-15 (2.0.112) |
| Debrief / Between session | n<5 | 0 | 4 / 5 | płynie |
| Health check | n<5 | 0 | n<5 | płynie |
| Nagrywanie sesji | 0 | 0 | n<5 | 0 na nowych buildach (testerzy też) |
| Before therapy (prep) | n<5 | 0 | n<5 | płynie |
| To-do (akcja) | n<5 | 0 | 0 | płynie (`main_sheet_action` todo, `workspace_item_action`) |
| Character KD v2 | n<5 | 0 | 0 | płynie (z testerami 8 os.) |
| Kafelki Main (tap) | n<5 | 0 | 0 | płynie |
| Stare karty Main (`today_card_*`, `side_card_*`) | 0 | n<5 | n<5 | usunięte zgodnie z redesignem |

**Głos**: `voice_chat_started` w ostatnich 10 dniach: 2.0.110 16 startów / 10 os., 2.0.107 6 / 4, 2.0.112 (Live, tester) 2 / 1. Na 2.0.113-2.0.117: **0**, także u testerów (14 os.), mimo że `reflect_mode_selected mode=voice` padł raz na 2.0.113. `mic_permission_result` też 0 na nowych buildach. Kod nadal emituje `voice_chat_started` z obu kubitów (`audio_chat_cubit.dart:232`, `live_chat_cubit.dart:766`), więc to nie jest usunięta instrumentacja w źródle. Pierwsza rozmowa na 2.0.117: 1 start, tryb `text`; na 2.0.110 było 6 voice / 2 text. Przy n=1 to nie dowód, ale to jedyny realny przypadek i poszedł tekstem. Do sprawdzenia na urządzeniu: czy na 2.0.117 da się wejść w rozmowę głosową z Reflect i z pierwszej rozmowy.

## 4. Nowy Main: kafelki i arkusze (z testerami, buildy 2.0.113-2.0.117, 10 osób; realni 2.0.117 w nawiasie)

| kafelek | wyświetlenia | tapy | os. tap | akcje w arkuszu | os. akcji |
|---|---|---|---|---|---|
| todo | 142 | 27 | 6 (n<5) | 2 | n<5 |
| focus | 141 | 26 | 6 (n<5) | 5 | n<5 |
| session | 132 | 25 | 7 (n<5) | 9 | n<5 |
| relationship | 143 | 22 | 5 (n<5) | 0 | 0 |
| habits | 142 | 19 | 7 (n<5) | 4 | n<5 |
| affirmation | 142 | 14 | 7 (n<5) | 0 | 0 |
| observations | 142 | 13 | 6 (n<5) | 0 | 0 |
| agenda | 132 | 11 | 6 (n<5) | 3 | n<5 |
| first_week | 7 | 10 | n<5 | 0 | 0 |

Wśród 7 realnych na 2.0.117: tapnęło kafelek n<5 osób (26 tapów), najczęściej `first_week` i `agenda`. Relationship, affirmation i observations: tapy są, akcji w arkuszu 0 (to arkusze do czytania, ale "relationship" bez żadnej akcji przy 22 tapach warto mieć na oku).

Zamykanie arkuszy (`main_sheet_closed`, 164 zamknięcia, 8 os. z testerami):

| metoda | < 2 s | 2-5 s | 5-30 s | 30 s+ |
|---|---|---|---|---|
| x | 34 | 17 | 22 | 6 |
| scrim (tap w tło) | 40 | 6 | 6 | 0 |
| swipe w dół | 10 | 1 | 1 | 0 |
| back | 3 | 0 | 3 | 1 |
| action | 0 | 5 | 7 | 2 |

Swipe w dół to tylko 12 / 164 zamknięć (7%). 53% zamknięć następuje w < 2 s, ale to prawie w całości testerzy (klikanie po wszystkich kafelkach). U realnych na 2.0.117: x 14 zamknięć (2 poniżej 2 s), back 3, action 9; scrim i swipe 0. Mediana czasu otwarcia arkusza: week_plan 11 s, agenda 4 s, reszta 0-2 s.

Ponowne otwieranie tego samego kafelka w jednej sesji: z testerami 29 z 88 par (sesja, kafelek) otwarte >= 2 razy, 15 >= 3 razy, 19 ponownie w ciągu 15 s (6 z 8 osób). Realni na 2.0.117: 4 z 18 par, n<5 osób. Przy testerach to wzorzec przeglądania, u realnych za mało danych.

## 5. Sygnały frustracji

- **Rage clicks** (`$rageclick`, autocapture SDK, tylko iOS): 30 dni 59 zdarzeń / 10 os. Tygodniowo: 09-20 4/2, 09-27 9/3, 10-04 1/1, 10-11 28/5, 10-18 17/3. Na 2.0.117 12 zdarzeń / n<5 (iOS, nowa instalacja w trakcie onboardingu 10-21). `$screen_name` na rage clicku zawsze "Flutter", więc nie wiadomo, na którym ekranie. Wzrost był już w tygodniu 10-11, przed wydaniem.
- **Dead clicks**: zdarzenie nie istnieje w projekcie (mobilny SDK go nie zbiera).
- **Szybkie cofanie** (`$screen` krócej niż 3 s / powrót na ten sam ekran w < 5 s): NEW 20 / 110 widoków (18%), 9 powrotów; OLD_concurrent 4 / 30, 4; PRE 51 / 366 (14%), 24. Bez wyraźnej zmiany przy tej próbie.
- **Błędy w nowej wersji** (realni 2.0.117, każde n<5): `follow_up_failed` 4 zd. (`status_class=not_found`), `first_week_plan_failed` 1 (`source=main_steps`, error), `login_failed` 3, `health_check_abandoned` 3, `quick_capture_abandoned` 2. U testerów dodatkowo `workspace_section_load_failed` 15 zd. / n<5 (sekcje questions, agenda, todo, threads, goals, realizations; build 2.0.113 i 2.0.116), `paywall_load_failed` 12 (`products_not_found`, `store_unavailable`, typowe dla buildów testowych), `character_sheet_load_failed` 3. `first_week_plan_failed` pojawia się na każdym buildzie od 2.0.109, także na starym 2.0.110 (3 zd. / n<5), więc to nie regresja redesignu.

## Caveats

- **Próba**: 3 istniejących użytkowników po aktualizacji, 7 realnych na 2.0.117 łącznie, okno ok. 47 h. Każda liczba osób w tym raporcie poza kohortą PRE jest poniżej 25. Raport mówi, co płynie i jak wygląda nowy Main, a nie jak zmieniło się zachowanie bazy. Powtórka ma sens po 7 dniach od wydania (ok. 2026-10-28) i po pełnym rolloucie w Google Play.
- Próg prywatności: osoby < 5 ukryte jako n<5 (próg zespołu, jak w serii 2026-10-15); < 25 bez odsetków.
- Android sklep vs ścieżka testowa Play nie dają się rozróżnić; testerów Android wyłapuję tylko przez to, że mieli buildy 2.0.111-2.0.116. Osoba testująca tylko 2.0.117 na Androidzie bez wcześniejszych buildów testowych byłaby policzona jako realna.
- `timeline_viewed`, `habit_tracker_viewed`, `character_card_viewed`, `bio_viewed`, `main_tile_viewed` to zdarzenia ładowania, nie świadomego otwarcia.
- `tab_switched` jest zawyżony przez przewijanie PageView (patrz pamięć agenta, 2026-10-13).
- `$rageclick` istnieje tylko na iOS (wszystkie 44 zdarzenia z 10 dni mają `$is_testflight`, czyli iOS); Android nie ma żadnego sygnału rage clicku.
- Ingest od 2026-04-22; okna raportu nie są obcięte.

## Luki instrumentacji

1. **Głos na nowych buildach**: 0 `voice_chat_started` / `mic_permission_result` na 2.0.113-2.0.117 (14 os. z testerami, 7 realnych). Nie wiadomo, czy to brak użycia, schowane wejście, czy zepsuty start. Właściciel weryfikacji: `flutter-mobile` (test na urządzeniu z buildem 2.0.117: Reflect voice, pierwsza rozmowa voice, Live Preview).
2. **Rage click bez ekranu i bez Androida**: `$screen_name` = "Flutter". Żeby rage clicki były użyteczne, `flutter-mobile` musiałby przekazać nazwę bieżącej trasy do natywnego SDK (np. `screen()` przy każdej zmianie trasy) albo emitować własne zdarzenie.
3. **Zamknięcie arkusza bez informacji o powtórce**: `main_sheet_closed` nie mówi, czy to pierwsze otwarcie w wizycie; powtórki liczę z `main_tile_tapped` w `$session_id`. Wystarcza, brak luki blokującej.
4. **`reflectModeChoice` zniknął z `$screen`** na 2.0.117, choć `reflect_mode_selected` płynie: do potwierdzenia przez `flutter-mobile`, czy ekran wyboru trybu ma nową trasę bez nazwy.
5. Brak zdarzenia "aplikacja otwarta z ikony" na kliencie poza `splash`; ścieżki zaczynam od pierwszego zdarzenia sesji.

## Queries

Wspólne CTE (wklejane na początek zapytań kohortowych):

```sql
WITH testers AS (SELECT DISTINCT person_id FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib='posthog-flutter'
 AND (properties.$is_testflight = true OR properties.$app_version IN ('2.0.111','2.0.112','2.0.113','2.0.114','2.0.115','2.0.116') OR properties.$is_emulator = true OR properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro'))),
newp AS (SELECT DISTINCT person_id FROM events WHERE timestamp > toDateTime('2026-10-19 18:00:00') AND properties.$lib='posthog-flutter' AND properties.$app_version='2.0.117' AND person_id NOT IN (SELECT person_id FROM testers)),
ev AS (SELECT person_id, event, timestamp, $session_id AS sid, properties.$screen_name AS scr, properties.$app_version AS ver,
  multiIf(timestamp >= toDateTime('2026-10-19 18:00:00') AND person_id IN (SELECT person_id FROM newp), 'NEW_2.0.117',
          timestamp >= toDateTime('2026-10-19 18:00:00'), 'OLD_concurrent',
          timestamp >= toDateTime('2026-10-12 00:00:00') AND timestamp < toDateTime('2026-10-19 00:00:00'), 'PRE_week_10-12..18', '') AS coh,
  properties AS p
 FROM events WHERE timestamp >= toDateTime('2026-10-12 00:00:00') AND properties.$lib='posthog-flutter' AND person_id NOT IN (SELECT person_id FROM testers))
```

```sql
-- adoption_by_day
SELECT toDate(timestamp) d, count(DISTINCT person_id) real_active, count(DISTINCT if(ver='2.0.117', person_id, NULL)) on_117,
 count(DISTINCT if(ver='2.0.110', person_id, NULL)) on_110, count(DISTINCT if(ver NOT IN ('2.0.117','2.0.110'), person_id, NULL)) on_other
FROM ev WHERE timestamp >= toDateTime('2026-10-14 00:00:00') GROUP BY d ORDER BY d

-- screens_by_cohort
SELECT scr, countIf(coh='NEW_2.0.117') c_new, count(DISTINCT if(coh='NEW_2.0.117', person_id, NULL)) u_new,
 countIf(coh='OLD_concurrent') c_oldc, count(DISTINCT if(coh='OLD_concurrent', person_id, NULL)) u_oldc,
 countIf(coh LIKE 'PRE%') c_pre, count(DISTINCT if(coh LIKE 'PRE%', person_id, NULL)) u_pre
FROM ev WHERE event='$screen' AND coh!='' GROUP BY scr ORDER BY u_new DESC, u_pre DESC LIMIT 40

-- sessions_by_cohort (NOISE = usage_snapshot, $set, $identify, app_install_attributed, notification_permission_prompted/_granted, $exception, client_error, notification_received, $pageview, $autocapture, api_error)
SELECT coh, count() sessions, count(DISTINCT person_id) users, round(count()/count(DISTINCT person_id),1) sess_per_user,
 quantile(0.5)(dur) med_s, quantile(0.9)(dur) p90_s, round(quantile(0.5)(n),0) med_events,
 countIf(dur < 10) under10s, countIf(dur >= 60) over1m, countIf(dur >= 300) over5m
FROM (SELECT coh, sid, any(person_id) person_id, dateDiff('second', min(timestamp), max(timestamp)) dur, countIf(event NOT IN NOISE) n
 FROM ev WHERE coh!='' AND sid IS NOT NULL AND sid != '' GROUP BY coh, sid HAVING n > 0) GROUP BY coh

-- first_steps (path = first 4 non-noise, non-load events of each session)
SELECT coh, path, count() sessions, count(DISTINCT person_id) users FROM (
 SELECT coh, sid, any(person_id) person_id, arrayStringConcat(arraySlice(arrayMap(x -> x.2, arraySort(x -> x.1, groupArray((timestamp, if(event='$screen', concat('S:', ifNull(scr,'?')), event))))), 1, 4), ' > ') path
 FROM ev WHERE coh!='' AND sid IS NOT NULL AND sid!='' AND event NOT IN NOISE
   AND event NOT IN ('main_tile_viewed','character_card_viewed','bio_viewed','habit_tracker_viewed','timeline_viewed')
 GROUP BY coh, sid) GROUP BY coh, path ORDER BY coh, sessions DESC LIMIT 60

-- session_exit
SELECT coh, last_ev, count() sessions, count(DISTINCT person_id) users FROM (
 SELECT coh, sid, any(person_id) person_id, argMax(if(event='$screen', concat('S:', ifNull(scr,'?')), event), timestamp) last_ev
 FROM ev WHERE coh!='' AND sid IS NOT NULL AND sid!='' AND event NOT IN NOISE GROUP BY coh, sid) GROUP BY coh, last_ev ORDER BY coh, sessions DESC LIMIT 60

-- feature_reach: multiIf mapping event -> feature (voice_chat_started split by voice_engine live/absent, recording_* by flow,
-- cards = card_viewed/card_text_expanded/card_item_bookmark_toggled/card_shared/card_edit_started/period_card_extras_viewed/summary_viewed,
-- character = character_sheet_viewed/skill_*/stat_opened/star_opened/tool_opened, todo = workspace_item_action section=todo OR main_sheet_action tile_id=todo)
SELECT f, count(DISTINCT if(coh='NEW_2.0.117',person_id,NULL)) u_new, countIf(coh='NEW_2.0.117') c_new,
 count(DISTINCT if(coh='OLD_concurrent',person_id,NULL)) u_oldc, countIf(coh='OLD_concurrent') c_oldc,
 count(DISTINCT if(coh LIKE 'PRE%',person_id,NULL)) u_pre, countIf(coh LIKE 'PRE%') c_pre
FROM (SELECT coh, person_id, multiIf(...) f FROM ev WHERE coh!='') WHERE f!='' GROUP BY f ORDER BY u_pre DESC, u_new DESC LIMIT 40

-- main_tiles_all_new_builds
SELECT toString(properties.tile_id) tile, countIf(event='main_tile_viewed') viewed, count(DISTINCT if(event='main_tile_viewed',person_id,NULL)) u_viewed,
 countIf(event='main_tile_tapped') tapped, count(DISTINCT if(event='main_tile_tapped',person_id,NULL)) u_tapped,
 countIf(event='main_sheet_action') actions, count(DISTINCT if(event='main_sheet_action',person_id,NULL)) u_action
FROM events WHERE timestamp > now() - INTERVAL 5 DAY AND properties.$lib='posthog-flutter' AND event IN ('main_tile_viewed','main_tile_tapped','main_sheet_action')
 AND properties.$app_version IN ('2.0.113','2.0.114','2.0.115','2.0.116','2.0.117')
GROUP BY tile ORDER BY tapped DESC LIMIT 20

-- sheet_close_method_dur
SELECT toString(properties.method) method, multiIf(toInt(properties.duration_s)<2,'a <2s',toInt(properties.duration_s)<5,'b 2-5s',toInt(properties.duration_s)<30,'c 5-30s',toInt(properties.duration_s)<120,'d 30s-2m','e 2m+') dur, count() c, count(DISTINCT person_id) u
FROM events WHERE timestamp > now() - INTERVAL 5 DAY AND event='main_sheet_closed' AND properties.$app_version IN ('2.0.113','2.0.114','2.0.115','2.0.116','2.0.117')
GROUP BY method, dur ORDER BY method, dur

-- repeat_tile_open_same_session
SELECT count() person_session_tile, countIf(n>=2) reopened2, countIf(n>=3) reopened3, countIf(min_gap<=15) reopen_within15s, count(DISTINCT person_id) u, count(DISTINCT if(n>=2,person_id,NULL)) u_reopen FROM (
 SELECT person_id, $session_id sid, toString(properties.tile_id) tile, count() n,
  if(count()>=2, arrayMin(arraySlice(arrayDifference(arraySort(groupArray(toUnixTimestamp(timestamp)))),2)), 99999) min_gap
 FROM events WHERE timestamp > now() - INTERVAL 5 DAY AND event='main_tile_tapped' AND properties.$app_version IN ('2.0.113','2.0.114','2.0.115','2.0.116','2.0.117')
 GROUP BY person_id, sid, tile)

-- rageclick_os_30d
SELECT properties.$os os, toStartOfWeek(timestamp) wk, count() c, count(DISTINCT person_id) u FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND event='$rageclick' GROUP BY os, wk ORDER BY wk, os

-- screen_dwell_quick_back
SELECT coh, count() screen_views, countIf(dwell < 3) under3s, countIf(prev_scr = next_scr AND dwell < 5) bounce_back_5s, count(DISTINCT person_id) u FROM (
 SELECT coh, person_id, scr, dateDiff('second', timestamp, leadInFrame(timestamp) OVER w) dwell,
  lagInFrame(scr) OVER (PARTITION BY sid ORDER BY timestamp ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) prev_scr,
  leadInFrame(scr) OVER w next_scr
 FROM ev WHERE coh!='' AND event='$screen' AND sid IS NOT NULL AND sid!=''
 WINDOW w AS (PARTITION BY sid ORDER BY timestamp ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING))
WHERE next_scr IS NOT NULL AND next_scr != '' GROUP BY coh

-- client_voice_10d
SELECT properties.$app_version v, ifNull(toString(properties.voice_engine),'absent') engine, count() c, count(DISTINCT person_id) u, max(timestamp) last_ts
FROM events WHERE timestamp > now() - INTERVAL 10 DAY AND event='voice_chat_started' AND properties.$lib='posthog-flutter' GROUP BY v, engine ORDER BY last_ts DESC LIMIT 20

-- first_conv_mode
SELECT properties.$app_version v, event, toString(properties.mode) mode, count() c, count(DISTINCT person_id) u FROM events WHERE timestamp > now() - INTERVAL 10 DAY
 AND event IN ('first_conversation_started','first_conversation_ended','mic_permission_result','reflect_mode_selected') AND properties.$lib='posthog-flutter' GROUP BY v, event, mode ORDER BY v DESC LIMIT 40

-- backend_user_actions_vs_client (silent-client check)
SELECT event, count(DISTINCT person_id) backend_u,
 count(DISTINCT if(person_id IN (SELECT person_id FROM events WHERE timestamp > toDateTime('2026-10-19 18:00:00') AND properties.$lib='posthog-flutter'), person_id, NULL)) with_client_since
FROM events WHERE timestamp > toDateTime('2026-10-19 18:00:00') AND properties.$lib='posthog-python'
 AND event IN ('reflect_session_started','reflect_message_sent','recording_processing_completed','voice_engine_selected','api_error','user_activated','debrief_created')
GROUP BY event ORDER BY backend_u DESC
```
