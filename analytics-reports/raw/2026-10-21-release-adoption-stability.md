# Adopcja wydania 2.0.117 i stabilność: raw PostHog extract

- **Date**: 2026-10-21 (stan na 16:58 UTC) · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: 2026-09-01 -> 2026-10-21 16:58 UTC (główne porównania od 2026-10-06 i od 2026-10-19 18:00)
- **Question**: która wersja jest nowym wydaniem sklepowym (iOS/Android), ile osób już na niej jest, czy jest stabilniejsza od poprzedniej, czy zaktualizowani wracają.
- **Event verification**: `$screen`, `$exception`, `client_error`, `*_failed`, `$rageclick`, `user_registered` (backend), `api_error` (backend) płyną 10-21. `$exception` niesie `$app_version`, `$app_build`, `$os_name`, `$exception_types`, `$exception_functions`, `$exception_fingerprint`, `$exception_handled`; `$exception_values` przychodzi jako `<redacted>` (treść błędu niedostępna). Właściwość `$build` nie istnieje, build to `$app_build`. `follow_up_failed` pojawił się pierwszy raz w historii 2026-10-21 16:46.

Filtry "czyste" (o ile nie napisano inaczej): `$lib='posthog-flutter'`, `$is_testflight != true`, `$is_emulator != true`, `$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')`, wykluczone osoby z >= 15 różnymi `$app_version` w 120d (wewnętrzni testerzy). Wszystkie liczby osób przez `person_id`.

## Results

### A. Identyfikacja wydania

| platforma | wersja (build) | first_seen ogółem | pierwszy realny użytkownik sklepu | dowód |
|---|---|---|---|---|
| Android | 2.0.117 (188) | 2026-10-19 18:13 UTC (testerzy + bot Play pre-launch) | 2026-10-20 02:12 UTC (nowa instalacja); pierwsi aktualizujący 2026-10-20 12:34 UTC | od 10-20 każda nowa instalacja Android startuje na 2.0.117 (poza 1 osobą na starym 2.0.85); 2.0.113-2.0.116 z 10-19 to buildy testowe (2-5 osób, emulator, OnePlus8Pro) |
| iOS | 2.0.117 (184) | 2026-10-19 20:44 UTC | 2026-10-21 07:49 UTC (nowa instalacja) | 2.0.117 iOS ma `$is_testflight=false` na 100% zdarzeń (277/277, 3 osoby), a 2.0.113-2.0.116 iOS były wyłącznie TestFlight |

Poprzednie sklepowe: Android 2.0.110 (181) (31 osób od 10-13), wcześniej 2.0.107; iOS 2.0.110 (177) (9 osób), wcześniej 2.0.106.

Uwaga: numery buildów iOS i Android są niezależne (Android 2.0.113 = build 184, iOS 2.0.117 = build 184).

### B. Osoby na 2.0.117 (wszystkie, przed filtrami), n = 12 (Android 9, iOS 3)

| klasa | osób | opis |
|---|---|---|
| bot / automat Play (OnePlus8Pro, emulator) | 2 | 737 + 45 zdarzeń, wszystkie `$exception` na 2.0.117 |
| tester wewnętrzny (>= 15 wersji, wielokrotny onboarding) | 2 | Android |
| realny aktualizujący (miał wcześniejszą wersję) | 3 | Android (2 z dokładnie 2 wersjami, 1 z 5-14 wersjami) |
| nowa instalacja Android | 2 | tylko `splash` + `welcome` + `app_install_attributed` (6 zdarzeń łącznie), odpadli na ekranie powitalnym |
| nowa instalacja iOS | 2 | przeszli onboarding (2x `onboarding_completed`), 191 zdarzeń |
| iOS, nieprzypisany (prawdopodobnie build deweloperski/review 10-19 20:44) | 1 | brak flagi TestFlight |

### C. Adopcja w czasie (czyste osoby na 2.0.117 dziennie)

| dzień (UTC) | Android 2.0.117 | iOS 2.0.117 | wszyscy aktywni w aplikacji (czyści, wszystkie wersje) |
|---|---|---|---|
| 2026-10-19 | 1 | 1 | 19 |
| 2026-10-20 | 4 | 0 | 10 |
| 2026-10-21 (do 17:00) | 4 | 2 | 7 |

Godzinowo: od 10-20 02:00 UTC na 2.0.117 jest najwyżej 1-2 osoby na godzinę (tabela `hourly_117` w zapytaniach).

### D. Odsetek zaktualizowanych (aktywni od 2026-10-20 00:00 UTC, czyści, bez testerów)

| OS | aktywni | na 2.0.117 | % | w tym nowe instalacje na 2.0.117 |
|---|---|---|---|---|
| Android | 11 | 5 | 45% | 2 |
| iOS | 2 | 2 | 100% | 2 |
| razem | 13 | 7 | 54% | 4 |

Istniejący użytkownicy sklepowi (aktywni 10-13 -> 10-19 18:00, czyści): Android 43, iOS 9. Od 10-20: aktywnych Android 6 (14%), iOS 0. Zaktualizowało do 2.0.117: Android 3 z 43 (7%), iOS 0 z 9.
Baza porównawcza: z 73 aktywnych 10-06 -> 10-12 wróciło 14 (19%) w pierwsze 2 dni kolejnego tygodnia (10-13 -> 10-14). Dzisiejsze 6/52 (12%) w ok. 41 h to podobny rząd wielkości, przy n za małym na wniosek o spadku.

Tło: DAU aplikacji (czyste) spada od początku października: 22-25 (10-01 -> 10-06), 8-19 (10-07 -> 10-19), 10 (10-20), 7 (10-21, niepełny dzień). Spadek zaczął się przed wydaniem 2.0.117.

### E. Stabilność: `$exception` per wersja (od 2026-10-01, wszystkie osoby)

| wersja | OS | zdarzeń | osób | unhandled | uwagi |
|---|---|---|---|---|---|
| 2.0.117 | Android | 4 | 1 | 4 | 100% z urządzenia OnePlus8Pro (automat Play) |
| 2.0.113-2.0.116 | Android | 12 | 1 na build | 12 | 100% OnePlus8Pro |
| 2.0.110 | Android | 7 | 2 | 7 | |
| 2.0.110 | iOS | 1 | 1 | 1 | |
| 2.0.107 | Android | 8 | 4 | 8 | |

Realni użytkownicy (czyści) na 2.0.117: **0 `$exception`, 0 `client_error`**. Na 2.0.110: `$exception` 8 zdarzeń / 2 osoby, `client_error` FirebaseAuthException 130 zdarzeń / 2 osoby (pętla), łącznie 2 z 31 osób Android dotknięte wyjątkiem (6%).

Sygnatury `$exception` na 2.0.113-2.0.117 (wszystkie od automatu OnePlus8Pro) i czy są nowe:

| typ | funkcja (początek stosu) | ekran | zdarzeń 2.0.113-117 | pierwszy raz w historii | nowa? |
|---|---|---|---|---|---|
| ProviderNotFoundException | `ErrorView.build.<fn>` -> `ReadContext.read` | subscription | 10 | 2026-09-02 (70 zdarzeń, 1 osoba łącznie) | nie |
| ApiException | `SettingsBodyState.build.<fn>` / `SettingsCubit` | settings | 1 | 2026-10-13 (2.0.110) | nie |
| ApiException | `UsersManager.editUserPreferences` -> `DioClient` | settings | 1 | 2026-09-02 | nie |
| String | `UrlLaunchHelper.openApp` | about | 2 | 2026-09-02 | nie |
| _TypeError | `VoiceListState.initState.<fn>` | settings | 1 | 2026-09-02 | nie |
| ApiException | `TherapyContextManager.upsertTherapyContext` | myTherapy | 1 | 2026-10-02 | nie |

**Nowych sygnatur w 2.0.117: zero.** Top 10 nie da się wypełnić, bo w nowych buildach jest tylko 6 sygnatur i wszystkie są starsze.

### F. Inne zdarzenia błędów na 2.0.117 (czyste osoby, od 10-19 18:00)

| zdarzenie | szczegół | zdarzeń | osób | na 2.0.110? |
|---|---|---|---|---|
| `follow_up_failed` | `status_class=not_found`, ekran `firstWeekFollowUp`, iOS, nowa osoba, 4x w 2 min (10-21 16:46) | 4 | 1 | nie, pierwsze w historii |
| `first_week_plan_failed` | `status_class=error`, `mainPage`, Android | 1 | 1 | tak (3/2) |
| `login_failed` | `cancelled` (Apple, iOS) 3x; `unknown` (email, Android) 1x | 4 | 2 | tak |
| `$rageclick` | iOS, 12 zdarzeń, ekran nieoznaczony (`Flutter`) | 12 | 1 | tak (13/3) |

Backend `api_error` osób, których ostatnia wersja to 2.0.117 (7d): `GET /health-check/latest` 404 (is_expected) 260 zdarzeń / 5 osób = **52 na osobę** vs 2.0.110: 35 / 7 = 5 na osobę; `/debriefs/latest` 20.8 vs 11.9 na osobę. Nowy Main odpytuje te endpointy dużo częściej. Szczyty były 10-19 (dzień testów), 10-20 07:00 25 zdarzeń od 1 osoby.

### G. Sesje (czyste osoby, od 2026-10-06)

| wersja | OS | sesji | osób | sesje <= 3 zdarzeń | sesje < 15 s | sesje >= 60 s | mediana czasu (s) | mediana zdarzeń |
|---|---|---|---|---|---|---|---|---|
| 2.0.117 | Android | 6 | 5 | 2 | 2 | 2 | 47.5 | 31 |
| 2.0.117 | iOS | 2 | 2 | 0 | 0 | 2 | 1424.5 | 103.5 |
| 2.0.110 | Android | 55 | 26 | 6 | 17 | 29 | 104 | 14 |
| 2.0.110 | iOS | 7 | 6 | 4 | 4 | 3 | 7 | 2 |
| 2.0.107 | Android | 74 | 44 | 10 | 25 | 36 | 58.5 | 12.5 |
| 2.0.100 | Android | 53 | 30 | 23 | 25 | 14 | 19 | 5 |

Dwie krótkie sesje Android 2.0.117 to dwie nowe instalacje, które zobaczyły `splash` i `welcome` i wyszły. Brak wzorca "aplikacja startuje i się zamyka" u osób zaktualizowanych.

### H. Rejestracje bez zdarzeń z aplikacji (kontrola instrumentacji)

`user_registered` (backend) w 72 h: 9 osób, z czego 4 bez żadnego zdarzenia `posthog-flutter`. To nie regresja wydania: tydzień 10-18: 6/13, 10-11: 16/36, 10-04: 9/26, 09-27: 5/25.

## Caveats

- **Bardzo małe n.** Na 2.0.117 jest 7 realnych osób (5 Android, 2 iOS); próg k=25 nie jest spełniony dla żadnego segmentu. Liczby podaję, bo dotyczą wersji i błędów technicznych, nie danych zdrowotnych, ale żadna różnica procentowa między wersjami nie jest statystycznie znacząca.
- **Natywne crashe są niewidoczne.** `posthog-flutter` łapie tylko wyjątki Darta (`$exception`). Crash natywny (iOS/Android) zabija proces bez zdarzenia. Odpowiedź na "czy aplikacja się crashuje" wymaga Play Console (Android vitals) i App Store Connect / Xcode Organizer. Pośredni sygnał (sesje kończące się po 1-3 zdarzeniach u osób zaktualizowanych) jest czysty, ale przy n=3 zaktualizowanych mało mówi.
- iOS sklepowy dotarł do realnych osób dopiero 2026-10-21 07:49 UTC (ok. 9 h danych). Android od 10-20 02:12 UTC (ok. 39 h).
- PostHog nie rozróżnia ścieżki Play produkcja vs staged rollout vs test track; wnioskuję z tego, że od 10-20 nowe instalacje Android trafiają wyłącznie na 2.0.117.
- `$exception_values` jest zredagowane, więc treści komunikatów błędów nie ma; sygnatury opisane przez typ, funkcję i ekran.
- Spadek ogólnej aktywności (DAU 22-25 na początku października -> 7-11 teraz) zaczął się przed wydaniem; to temat dla `growth-analyst`, nie efekt 2.0.117.

## Queries

Pełne pliki: `C:\Users\mikol\AppData\Local\Temp\claude\C--Users-mikol-Notebooks-MindSync-Heroku\b6f3940a-d5d1-4f79-a0d3-90675bd0a564\scratchpad\a1-release\q1.sql` ... `q13.sql`. Najważniejsze, dosłownie:

```sql
-- @@ ver_build_os_since_1017
SELECT toString(properties.$app_version) ver, toString(properties.$app_build) build, toString(properties.$os) os, count() c, count(DISTINCT person_id) u, min(timestamp) first_ts, max(timestamp) last_ts
FROM events WHERE timestamp > toDateTime('2026-10-17 00:00:00') AND properties.$lib='posthog-flutter'
GROUP BY ver, build, os ORDER BY first_ts DESC LIMIT 60

-- @@ share_on_117_since_1020_clean
SELECT os, count() active, countIf(on117) on117, countIf(new_since) new_persons, countIf(new_since AND first_v='2.0.117') new_on_117 FROM (
 SELECT person_id, any(toString(properties.$os)) os, countIf(toString(properties.$app_version)='2.0.117') > 0 on117, argMin(toString(properties.$app_version), timestamp) first_v
 , min(timestamp) >= toDateTime('2026-10-20 00:00:00') new_since
 FROM events WHERE timestamp > toDateTime('2026-09-01 00:00:00') AND properties.$lib='posthog-flutter'
  AND properties.$is_emulator != true AND properties.$is_testflight != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  AND person_id NOT IN (SELECT person_id FROM events WHERE timestamp > now() - INTERVAL 120 DAY AND properties.$lib='posthog-flutter' GROUP BY person_id HAVING uniqExact(toString(properties.$app_version)) >= 15)
 GROUP BY person_id HAVING countIf(timestamp >= toDateTime('2026-10-20 00:00:00')) > 0) GROUP BY os

-- @@ prior_store_users_return
SELECT prev_os, count() active_1013_1019, countIf(active_after) active_since_1020, countIf(on117) on_117, countIf(on117 AND after117_sessions >= 2) on117_2plus_sessions FROM (
 SELECT person_id, any(toString(properties.$os)) prev_os,
  countIf(timestamp >= toDateTime('2026-10-20 00:00:00')) > 0 active_after,
  countIf(toString(properties.$app_version)='2.0.117') > 0 on117,
  uniqExactIf($session_id, toString(properties.$app_version)='2.0.117') after117_sessions,
  countIf(timestamp < toDateTime('2026-10-19 18:00:00') AND timestamp >= toDateTime('2026-10-13 00:00:00')) pre
 FROM events WHERE timestamp >= toDateTime('2026-10-13 00:00:00') AND properties.$lib='posthog-flutter'
  AND properties.$is_emulator != true AND properties.$is_testflight != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  AND person_id NOT IN (SELECT person_id FROM events WHERE timestamp > now() - INTERVAL 120 DAY AND properties.$lib='posthog-flutter' GROUP BY person_id HAVING uniqExact(toString(properties.$app_version)) >= 15)
 GROUP BY person_id HAVING pre > 0) GROUP BY prev_os

-- @@ exc_by_version_since_1001
SELECT toString(properties.$app_version) ver, toString(properties.$os_name) os, count() c, count(DISTINCT person_id) u, countIf(toString(properties.$exception_handled)='false') unhandled_c, min(timestamp) f, max(timestamp) l
FROM events WHERE event='$exception' AND timestamp > toDateTime('2026-10-01 00:00:00') GROUP BY ver, os ORDER BY f DESC LIMIT 50

-- @@ exc_signatures_since_0901
SELECT substring(toString(properties.$exception_types),1,50) typ, toString(properties.$exception_fingerprint) fp,
 count() c, count(DISTINCT person_id) u, groupUniqArray(8)(toString(properties.$app_version)) vers, groupUniqArray(3)(toString(properties.$os_name)) oses, min(timestamp) f, max(timestamp) l
FROM events WHERE event='$exception' AND timestamp > toDateTime('2026-09-01 00:00:00') GROUP BY typ, fp ORDER BY l DESC LIMIT 60

-- @@ exc_new_builds_detail
SELECT toString(properties.$app_version) ver, substring(toString(properties.$exception_types),1,40) typ, substring(toString(properties.$exception_functions),1,160) funcs, substring(toString(properties.$screen_name),1,30) scr, toString(properties.$is_emulator) emu, toString(properties.$device_model) dm, count() c, count(DISTINCT person_id) u
FROM events WHERE event='$exception' AND timestamp > toDateTime('2026-10-19 00:00:00') GROUP BY ver, typ, funcs, scr, emu, dm ORDER BY ver DESC LIMIT 30

-- @@ sessions_by_version_clean
SELECT v, os, count() sessions, count(DISTINCT pid) persons, countIf(n_ev <= 3) le3_ev, countIf(dur_s < 15) lt15s, countIf(dur_s >= 60) ge60s, quantile(0.5)(dur_s) med_dur_s, quantile(0.5)(n_ev) med_ev FROM (
 SELECT $session_id sid, any(person_id) pid, any(toString(properties.$app_version)) v, any(toString(properties.$os)) os, count() n_ev, dateDiff('second', min(timestamp), max(timestamp)) dur_s
 FROM events WHERE timestamp > toDateTime('2026-10-06 00:00:00') AND properties.$lib='posthog-flutter' AND $session_id != ''
  AND properties.$is_emulator != true AND properties.$is_testflight != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  AND toString(properties.$app_version) IN ('2.0.117','2.0.110','2.0.107','2.0.106','2.0.100')
  AND person_id NOT IN (SELECT person_id FROM events WHERE timestamp > now() - INTERVAL 120 DAY AND properties.$lib='posthog-flutter' GROUP BY person_id HAVING uniqExact(toString(properties.$app_version)) >= 15)
 GROUP BY sid) GROUP BY v, os ORDER BY v DESC, os

-- @@ latest_404_per_person_ratio
SELECT v, ep, count() c, count(DISTINCT person_id) u, round(count()/count(DISTINCT person_id),1) per_person FROM (
 SELECT e.person_id person_id, pv.v v, substring(toString(e.properties.endpoint),1,40) ep FROM events e
 JOIN (SELECT person_id, argMax(toString(properties.$app_version), timestamp) v FROM events WHERE timestamp > now() - INTERVAL 7 DAY AND properties.$lib='posthog-flutter' GROUP BY person_id) pv ON pv.person_id = e.person_id
 WHERE e.event='api_error' AND e.timestamp > now() - INTERVAL 7 DAY AND toString(e.properties.status_code)='404' AND toString(e.properties.endpoint) LIKE '%latest%')
GROUP BY v, ep HAVING u >= 1 ORDER BY v DESC, c DESC LIMIT 20
```
