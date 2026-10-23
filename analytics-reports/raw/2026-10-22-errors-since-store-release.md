# Błędy od wydania sklepowego, osobno Android i iOS: raw PostHog extract

- **Date**: 2026-10-22 (stan na 18:24 UTC) · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: Android 2026-10-19 00:00 UTC -> 2026-10-22 18:24 UTC (build 188); iOS 2026-10-20 18:24 UTC -> 2026-10-22 18:24 UTC (wersja 2.0.117, build 184)
- **Question**: jakie błędy (wyjątki, zdarzenia *_failed, api_error, sygnały crasha) mają realni użytkownicy na buildzie sklepowym, osobno per platforma, i co jest nowe od przeglądu z 21.10 ~17:00 UTC.
- **Event verification**: `$exception` (definicja istnieje, last_seen 2026-10-19 19:03, ostatnie zdarzenia z automatu Play OnePlus8Pro na 2.0.117/188, więc przechwytywanie na buildzie sklepowym działa). `api_error` (backend) płynie, last 10-22 16:56. `follow_up_failed`, `first_week_plan_failed`, `login_failed`, `$rageclick` płyną 10-22. `$app_crash`, `Application Opened`, `Application Backgrounded` nie istnieją w projekcie (7d: 0, definicji brak). `subscription_purchase_failed`, `subscription_restore_failed` nadal nie płyną.
- **Buildy**: w PostHogu wersja 2.0.117 występuje wyłącznie jako Android build 188 i iOS build 184 (`$is_testflight=false`). **Buildów 189 i 190 nie ma w PostHogu ani jednego zdarzenia**, więc rozdział "sklep vs inne buildy 2.0.117" sprowadza się do testerów na tych samych buildach sklepowych.

Filtry: zdarzenia klienta `$lib='posthog-flutter'`; wykluczenie testerów po osobie makrem `{T}` z `2026-10-21-release-activity.md` (TestFlight, emulator, OnePlus8Pro / Pixel 6 Pro / sdk_gphone% / iPhone99%, albo dowolne zdarzenie z 2.0.113-2.0.116, okno 120d). Dziś makro wyklucza **69 osób** (wczoraj raportowano 92; okno 120d przesunęło się i część osób mogła zostać scalona, definicja bez zmian). Zdarzenia backendu przypisane do platformy przez osobę: osoba z co najmniej jednym zdarzeniem klienta na buildzie sklepowym w oknie platformy, zdarzenie backendu od początku okna tej platformy.

## Results

### 1. Mianownik: realni użytkownicy na buildzie sklepowym

| platforma | okno | osoby | nowe instalacje | aktualizujący | dotarli dalej niż splash/welcome | sesje | aktywni po 21.10 17:00 | z testerami |
|---|---|---|---|---|---|---|---|---|
| Android 2.0.117 (188) | od 10-19 00:00 (pierwszy realny 10-20 02:12) | 13 | 5 | 8 | 9 | 23 | 11 | 17 |
| iOS 2.0.117 (184) | od 10-20 18:24 (pierwszy realny 10-21 07:49) | 3 | 2 | 1 | 3 | 6 | 2 | 3 |

Realni na innych buildach w tym samym czasie (od 10-19): Android 2.0.110 (181) 12 osób, 2.0.100 4, 2.0.94 2, 2.0.95 2, 2.0.85 1; iOS 2.0.110 (177) 2.

### 2. `$exception`

| platforma | realni na buildzie sklepowym | testerzy / automaty na 2.0.117 | sygnatury |
|---|---|---|---|
| Android | **0** | 4 zdarzenia / 1 urządzenie (OnePlus8Pro, automat Play), 10-19 18:20-19:03 | te same co wczoraj (ProviderNotFoundException, ApiException, String, _TypeError), wszystkie znane od 2026-09-02 lub 2026-10-02 |
| iOS | **0** | 0 | brak |

Od 2026-10-19 19:03 UTC w całym projekcie nie ma żadnego `$exception`. Nowych sygnatur względem buildów sprzed 2.0.113: zero.

### 3. Zdarzenia błędów klienta, realni na buildzie sklepowym

| platforma | zdarzenie | powód / status | ekran | zdarz. | osób | pierwszy | ostatni | po 21.10 17:00 (zdarz./os.) |
|---|---|---|---|---|---|---|---|---|
| Android | first_week_plan_failed | error | mainPage / mainPageTab | 2 | 1 | 10-21 09:13 | 10-21 23:24 | 1 / 1 |
| Android | follow_up_failed | not_found | firstWeekFollowUp | 1 | 1 | 10-22 00:07 | 10-22 00:07 | **1 / 1 (nowe na Androidzie)** |
| iOS | $rageclick | | mainPage 11, healthCheckFlow 6, afterTherapyFlow 6, wow 2, therapyOnboarding 2 | 27 | 1 | 10-21 16:18 | 10-22 11:06 | 16 / 1 |
| iOS | follow_up_failed | not_found | firstWeekFollowUp | 10 | 1 | 10-21 16:46 | 10-22 11:04 | **6 / 1** (3 sesje w 2 dni) |
| iOS | login_failed | cancelled | auth | 3 | 1 | 10-21 16:17 | 10-21 16:17 | 0 |
| iOS | first_week_plan_failed | error | mainPage | 1 | 1 | 10-21 18:45 | 10-21 18:45 | **1 / 1** |

Wszystkie zdarzenia błędów iOS (41) pochodzą od **jednej osoby** (nowa instalacja z 10-21). Na Androidzie first_week_plan_failed to 1 osoba, follow_up_failed inna 1 osoba.

Testerzy na buildzie sklepowym Android (wykluczeni powyżej): client_error 10 / 1, paywall_load_failed 5 / 1 (ostatni 10-20 07:43), login_failed 1 / 1. iOS: brak.

Nie wystąpiły u realnych na buildzie sklepowym: client_error, paywall_load_failed, usage_load_failed, workspace_section_load_failed, character_sheet_load_failed, voice_session_failed, voice_transcription_failed, debrief_failed, recording_chunk_upload_failed, subscription_restore_empty, notification_permission_denied.

### 4. `api_error` (backend) osób z buildu sklepowego

| platforma | endpoint | status | is_expected | zdarz. | osób | na osobę | po 21.10 17:00 (zdarz./os.) |
|---|---|---|---|---|---|---|---|
| Android | /prep-cards/latest | 404 | true | 33 | 5 | 6.6 | 31 / 5 |
| Android | /debriefs/latest | 404 | true | 27 | 5 | 5.4 | 16 / 5 |
| Android | /health-check/latest | 404 | true | 15 | 5 | 3.0 | 10 / 5 |
| Android | /users/get_user_profile_and_subscription | 404 | false | 2 | 2 | 1.0 | 2 / 2 |
| Android | /users/therapy-context | 404 | false | 2 | 2 | 1.0 | 2 / 2 |
| Android | /between-sessions/latest | 404 | true | 1 | 1 | 1.0 | 0 |
| iOS | /debriefs/latest | 404 | true | 13 | 1 | 13.0 | 0 (wszystko 10-21 16:43-16:50) |
| iOS | /prep-cards/latest | 404 | true | 3 | 1 | 3.0 | 0 |
| iOS | /users/therapy-context | 404 | false | 2 | 2 | 1.0 | 0 |
| iOS | /users/get_user_profile_and_subscription | 404 | false | 2 | 2 | 1.0 | 0 |
| iOS | /health-check/latest | 404 | true | 1 | 1 | 1.0 | 0 |
| iOS | /debriefs/latest, /users/therapy-schedule, /prep-cards/latest | **401** | false | 1 + 1 + 1 | 1 | | **3 / 1 (nowe, 10-22 16:56:11, ta sama sekunda)** |

- **5xx w `api_error` od 10-19: 0** (w całym projekcie).
- 404 profilu i therapy-context przy pierwszym uruchomieniu: znany wzorzec "profil jeszcze nie utworzony" (2 nowe instalacje na każdej platformie).
- 401 na iOS: trzy endpointy w jednej sekundzie u jednej osoby, jednorazowo. Wygląda na wygasły token przy wznowieniu aplikacji; nie powtórzyło się do 18:24.

### 5. Zdarzenia *_failed z backendu: wszystkie nowe są ze środowiska testowego

Od 21.10 17:00 pojawiły się `recording_processing_failed` (6), `onboarding_symptom_sync_failed` (6), `recording_chunk_store_failed` (3, `postgres_store_failed` / 503), `subscription_verification_failed` (3, `apple_status_21002`). **Żadne nie dotyczy osoby z buildu sklepowego** (zapytanie z przypisaniem do platformy: 0 wierszy). Wszystkie mają `$os=Windows`, przyszły 2026-10-21 20:30-21:42 UTC, a treść błędów to fikstury testowe ("db exploded", "simulated poisoned session ..."). W tym samym oknie z Windows przyszło 427 zdarzeń backendu od 138 syntetycznych osób (0 z nich ma jakiekolwiek zdarzenie klienta), w tym 9 `subscription_purchase_completed`, 12 `subscription_receipt_received`, 18 `api_error`, 100 `moment.scheduled`.

Wyciek backendu z Windows do prod PostHog (znany P1 z 10-15) trwa: 30 dni = 9623 zdarzenia / 683 osoby, dni z ruchem 10-02..10-21, do 112 zdarzeń "pieniężnych" dziennie (10-05).

### 6. Sygnały crasha / ubicia (realni, build sklepowy)

| miara | Android | iOS |
|---|---|---|
| sesje / osoby | 23 / 13 | 6 / 3 |
| sesje z <= 3 zdarzeniami | 5 | 1 |
| sesje < 15 s | 6 | 1 |
| sesje kończące się na splash/welcome | 4 (nowe instalacje, które nie poszły dalej) | 0 |
| mediana długości sesji (s) / zdarzeń | 127 / 38 | 982.5 / 91 |
| ponowne otwarcie < 30 s / < 2 min / < 10 min po końcu poprzedniej sesji | 1 / 1 / 1 (z 10 przerw, 5 osób) | 0 / 0 / 0 (z 3 przerw) |
| `$app_crash` | nie istnieje | nie istnieje |

Jedyne szybkie ponowne otwarcie: Android, 16 s po sesji zakończonej na `prepTherapyFlow` (ostatnie zdarzenie `usage_snapshot`), następna sesja zaczyna się od `splash`, czyli zimny start. Zgodne z ubiciem procesu albo crashem natywnym, ale to 1 przypadek. Ostatnie zdarzenie sesji to najczęściej `mainPage` (`$screen`, `main_tile_viewed`, `main_sheet_closed`), czyli normalne wyjście. Po jednej sesji na każdej platformie kończy się na `recording_started` (nagrywanie w tle, bez dalszych zdarzeń w tej sesji; na Androidzie widać później `recording_recovered`).

### 7. Status otwartych punktów z 21.10

| punkt | wczoraj | dziś | zmiana |
|---|---|---|---|
| 0 `voice_chat_started` na 2.0.113-117 | 0 sesji głosowych | Android 2.0.117: **3 sesje Classic (`voice_engine=realtime`) / 2 osoby, wszystkie zakończone** (`voice_chat_ended` 3/2), 1 pierwsza rozmowa głosowa zakończona przez użytkownika; 0 `voice_session_failed`. iOS: nadal 0 sesji, 1 `voice_engine_changed` | częściowo zamknięte (Android) |
| follow_up_failed `not_found` | 4 zdarz. / 1 os. (iOS) | 11 / 2 (iOS 10 w 3 sesjach przez 2 dni, Android 1 nowa osoba) | **rośnie, obie platformy** |
| first_week_plan_failed | 2 / 2 | na buildzie sklepowym 3 / 2 (Android 2 / 1, iOS 1 / 1); 90d: 15 / 5 od 10-13 | utrzymuje się |
| paywall_load_failed `products_not_found` | 10 / 1 (tester) | 0 u realnych; tester 5, ostatnio 10-20 07:43 | bez nowych |
| polling `/health-check/latest` | 52 zdarz./os. na 2.0.117 (z testerami) | realni Android 3.0 / os.; najwięcej `/prep-cards/latest` 6.6 i `/debriefs/latest` 5.4 / os.; iOS jedna osoba 13x `/debriefs/latest` w 7 min | wczorajsza skala to głównie testerzy; seria 13x w 7 min na iOS warta sprawdzenia |

## Caveats

- **Bardzo małe n**: Android 13 osób, iOS 3 osoby. Próg k=25 nie jest spełniony dla żadnego segmentu. Liczby podane, bo dotyczą wyłącznie zdarzeń technicznych, bez danych zdrowotnych i identyfikatorów (osoby rozróżnione tylko hashem modulo 1000). Każdy wiersz z 1 osobą to anegdota.
- Cały obraz błędów iOS to jedna osoba. Nie ma sposobu, żeby w PostHogu odróżnić realnego użytkownika od członka zespołu na buildzie z App Store (brak flagi wewnętrznego konta).
- **Crashe natywne są niewidoczne**: `posthog-flutter` zgłasza tylko wyjątki Darta, a zdarzenia cyklu życia (`Application Opened/Backgrounded`) nie są włączone. Prawda o crashach: Play Console (Android vitals) i App Store Connect / Xcode Organizer.
- `api_error` nie niesie `$app_version` ani `$os`; platforma przypisana przez osobę.
- Liczba wykluczonych testerów spadła z 92 do 69 przy tej samej definicji (przesunięte okno 120d, możliwe scalenia osób).
- Ingest od 2026-04-22: bez wpływu na okno.

## Queries

Pliki robocze: `C:\Users\mikol\AppData\Local\Temp\claude\C--Users-mikol-Notebooks-MindSync-Heroku\e638dcd8-2c46-4beb-ba6a-ae3a728012be\scratchpad\e\p1.sql` ... `p5.sql`. Makra (wstawiane dosłownie):

```sql
-- {T} wykluczenie testerów po osobie
person_id NOT IN (SELECT DISTINCT person_id FROM events WHERE timestamp > now() - INTERVAL 120 DAY AND properties.$lib = 'posthog-flutter' AND (properties.$is_testflight = true OR properties.$is_emulator = true OR properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro') OR properties.$device_model LIKE 'sdk_gphone%' OR properties.$device_model LIKE 'iPhone99%' OR properties.$app_version IN ('2.0.113','2.0.114','2.0.115','2.0.116')))
-- {W} build sklepowy w oknie platformy
((toString(properties.$os)='Android' AND toString(properties.$app_build)='188' AND timestamp >= toDateTime('2026-10-19 00:00:00')) OR (toString(properties.$os)='iOS' AND toString(properties.$app_build)='184' AND toString(properties.$app_version)='2.0.117' AND timestamp >= toDateTime('2026-10-20 18:24:00')))
-- {P} osoby z buildu sklepowego -> platforma i początek okna
(SELECT person_id, argMax(toString(properties.$os), timestamp) pos, if(argMax(toString(properties.$os), timestamp)='iOS', toDateTime('2026-10-20 18:24:00'), toDateTime('2026-10-19 00:00:00')) wstart FROM events WHERE properties.$lib='posthog-flutter' AND {W} AND {T} GROUP BY person_id)
```

```sql
-- @@ ver_build_os_since_1019
SELECT toString(properties.$app_version) ver, toString(properties.$app_build) build, toString(properties.$os) os, toString(properties.$is_testflight) tf, count() c, count(DISTINCT person_id) u, min(timestamp) first_ts, max(timestamp) last_ts
FROM events WHERE timestamp > toDateTime('2026-10-19 00:00:00') AND properties.$lib='posthog-flutter'
GROUP BY ver, build, os, tf ORDER BY first_ts DESC LIMIT 60

-- @@ error_events_since_1019
SELECT event, toString(properties.$lib) lib, count() c, count(DISTINCT person_id) u, min(timestamp) f, max(timestamp) l,
 countIf(timestamp > toDateTime('2026-10-21 17:00:00')) c_new, count(DISTINCT if(timestamp > toDateTime('2026-10-21 17:00:00'), person_id, NULL)) u_new
FROM events WHERE timestamp > toDateTime('2026-10-19 00:00:00')
 AND (event ILIKE '%fail%' OR event ILIKE '%error%' OR event ILIKE '%exception%' OR event ILIKE '%crash%' OR event ILIKE '%rage%' OR event ILIKE '%timeout%' OR event ILIKE '%empty%' OR event ILIKE '%denied%' OR event ILIKE '%limit_hit%')
GROUP BY event, lib ORDER BY c DESC LIMIT 80

-- @@ denom_store_build
SELECT toString(properties.$os) os, count(DISTINCT person_id) persons, count() events, count(DISTINCT $session_id) sessions,
 count(DISTINCT if(event NOT IN ('$identify','$set','app_install_attributed','$feature_flag_called') AND NOT (event IN ('$screen','tab_switched') AND properties.$screen_name IN ('splash','welcome','auth','signUp','forgotPassword')), person_id, NULL)) persons_past_welcome,
 count(DISTINCT if(timestamp > toDateTime('2026-10-21 17:00:00'), person_id, NULL)) persons_since_1021_17, min(timestamp) f, max(timestamp) l
FROM events WHERE properties.$lib='posthog-flutter' AND {W} AND {T} GROUP BY os

-- @@ denom_new_vs_updaters
SELECT os, count() persons, countIf(first_ever >= w_start) new_installs, countIf(first_ever < w_start) updaters FROM (
 SELECT person_id, any(toString(properties.$os)) os, min(timestamp) first_ever,
  if(any(toString(properties.$os))='iOS', toDateTime('2026-10-20 18:24:00'), toDateTime('2026-10-19 00:00:00')) w_start
 FROM events WHERE properties.$lib='posthog-flutter' AND timestamp > toDateTime('2026-04-22 00:00:00') AND {T}
 GROUP BY person_id HAVING countIf({W}) > 0) GROUP BY os

-- @@ exception_all_since_1019
SELECT toString(properties.$os_name) os, toString(properties.$app_version) ver, toString(properties.$app_build) build, toString(properties.$device_model) dm, toString(properties.$is_emulator) emu, count() c, count(DISTINCT person_id) u, min(timestamp) f, max(timestamp) l
FROM events WHERE event='$exception' AND timestamp >= toDateTime('2026-10-19 00:00:00') GROUP BY os, ver, build, dm, emu ORDER BY l DESC LIMIT 30

-- @@ exception_store_real  (0 rows)
SELECT toString(properties.$os) os, substring(toString(properties.$exception_types),1,60) typ, substring(toString(properties.$exception_functions),1,160) funcs, count() c, count(DISTINCT person_id) u, min(timestamp) f
FROM events WHERE event='$exception' AND {W} AND {T} GROUP BY os, typ, funcs ORDER BY c DESC LIMIT 30

-- @@ client_fail_store_real
SELECT toString(properties.$os) os, event,
 coalesce(nullIf(toString(properties.reason),''), nullIf(toString(properties.status_class),''), nullIf(toString(properties.error_type),''), nullIf(toString(properties.failure_reason),''), nullIf(toString(properties.error_class),''), '') why,
 toString(properties.section_name) sec, toString(properties.$screen_name) scr, count() c, count(DISTINCT person_id) u, min(timestamp) f, max(timestamp) l,
 countIf(timestamp > toDateTime('2026-10-21 17:00:00')) c_new, count(DISTINCT if(timestamp > toDateTime('2026-10-21 17:00:00'), person_id, NULL)) u_new
FROM events WHERE properties.$lib='posthog-flutter' AND {W} AND {T}
 AND (event ILIKE '%fail%' OR event ILIKE '%error%' OR event IN ('$exception','$rageclick','subscription_restore_empty','notification_permission_denied'))
GROUP BY os, event, why, sec, scr ORDER BY os, c DESC LIMIT 60

-- @@ api_error_store_real
SELECT p.pos os, replaceRegexpAll(toString(e.properties.endpoint), '[0-9a-f]{8}-[0-9a-f-]{27,}|/[0-9]+(/|$)', '{id}') ep, toString(e.properties.status_code) st, toString(e.properties.is_expected) exp,
 count() c, count(DISTINCT e.person_id) u, round(count()/count(DISTINCT e.person_id),1) per_u, min(e.timestamp) f, max(e.timestamp) l,
 countIf(e.timestamp > toDateTime('2026-10-21 17:00:00')) c_new, count(DISTINCT if(e.timestamp > toDateTime('2026-10-21 17:00:00'), e.person_id, NULL)) u_new
FROM events e JOIN {P} p ON p.person_id = e.person_id
WHERE e.event='api_error' AND e.timestamp >= toDateTime('2026-10-19 00:00:00') AND e.timestamp >= p.wstart
GROUP BY os, ep, st, exp ORDER BY os, c DESC LIMIT 60

-- @@ api_error_5xx_all_since_1019  (0 rows)
SELECT toDate(timestamp) d, toString(properties.endpoint) ep, toString(properties.status_code) st, count() c, count(DISTINCT person_id) u
FROM events WHERE event='api_error' AND timestamp >= toDateTime('2026-10-19 00:00:00') AND toInt(properties.status_code) >= 500 GROUP BY d, ep, st ORDER BY d LIMIT 30

-- @@ backend_failed_store_real  (0 rows)
SELECT p.pos os, e.event ev, coalesce(nullIf(toString(e.properties.error_type),''), nullIf(toString(e.properties.reason),''), nullIf(toString(e.properties.failure_reason),''), substring(splitByChar(':', toString(e.properties.error))[1],1,60), '') why,
 count() c, count(DISTINCT e.person_id) u, min(e.timestamp) f, max(e.timestamp) l
FROM events e JOIN {P} p ON p.person_id = e.person_id
WHERE e.properties.$lib='posthog-python' AND e.event != 'api_error' AND (e.event ILIKE '%fail%' OR e.event ILIKE '%error%') AND e.timestamp >= p.wstart
GROUP BY os, ev, why ORDER BY os, c DESC LIMIT 40

-- @@ python_events_in_leak_window
SELECT event, count() c, count(DISTINCT person_id) u, any(toString(properties.$os)) os FROM events WHERE timestamp BETWEEN toDateTime('2026-10-21 20:25:00') AND toDateTime('2026-10-21 21:50:00') AND properties.$lib='posthog-python' GROUP BY event ORDER BY c DESC LIMIT 40

-- @@ python_os_split_30d
SELECT toString(properties.$os) os, count() c, count(DISTINCT person_id) u, min(timestamp) f, max(timestamp) l FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib='posthog-python' GROUP BY os

-- @@ sessions_store_real
SELECT os, count() sessions, count(DISTINCT pid) persons, countIf(n_ev <= 3) le3, countIf(dur_s < 15) lt15s, countIf(last_scr IN ('splash','welcome')) end_on_splash_welcome, quantile(0.5)(dur_s) med_s, quantile(0.5)(n_ev) med_ev FROM (
 SELECT $session_id sid, any(person_id) pid, any(toString(properties.$os)) os, count() n_ev, dateDiff('second', min(timestamp), max(timestamp)) dur_s, argMax(toString(properties.$screen_name), timestamp) last_scr
 FROM events WHERE properties.$lib='posthog-flutter' AND $session_id != '' AND {W} AND {T} GROUP BY sid) GROUP BY os

-- @@ quick_reopen_store_real
SELECT os, countIf(gap_s < 30) lt30s, countIf(gap_s < 120) lt120s, countIf(gap_s < 600) lt600s, count() gaps, count(DISTINCT pid) persons FROM (
 SELECT pid, os, dateDiff('second', prev_end, s_start) gap_s FROM (
  SELECT pid, os, s_start, lagInFrame(s_end) OVER (PARTITION BY pid ORDER BY s_start ROWS BETWEEN 1 PRECEDING AND CURRENT ROW) prev_end, row_number() OVER (PARTITION BY pid ORDER BY s_start) rn FROM (
   SELECT $session_id sid, any(person_id) pid, any(toString(properties.$os)) os, min(timestamp) s_start, max(timestamp) s_end
   FROM events WHERE properties.$lib='posthog-flutter' AND $session_id != '' AND {W} AND {T} GROUP BY sid)) WHERE rn > 1) GROUP BY os

-- @@ voice_chat_store_real
SELECT toString(properties.$os) os, event, toString(properties.voice_engine) eng, toString(properties.mode) mode, toString(properties.reason) r, count() c, count(DISTINCT person_id) u, min(timestamp) f
FROM events WHERE properties.$lib='posthog-flutter' AND {W} AND {T} AND (event LIKE 'voice_chat%' OR event LIKE 'voice_engine%' OR event LIKE 'voice_live%' OR event='voice_session_failed' OR event LIKE 'first_conversation%')
GROUP BY os, event, eng, mode, r ORDER BY os, f LIMIT 30

-- @@ rage_screen_store_ios
SELECT s.scr scr, count() c FROM (
 SELECT properties.$session_id sid, timestamp ts FROM events WHERE event='$rageclick' AND {W} AND {T}) r
 ASOF LEFT JOIN (SELECT properties.$session_id sid, timestamp ts, toString(properties.$screen_name) scr FROM events WHERE event='$screen' AND timestamp > toDateTime('2026-10-20 18:00:00') AND properties.$os='iOS') s
 ON r.sid = s.sid AND r.ts >= s.ts
GROUP BY scr ORDER BY c DESC LIMIT 20
```
