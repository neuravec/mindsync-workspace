# Aktywność, powroty i powiadomienia po wydaniu 2.0.117 - raw PostHog extract

- **Date**: 2026-10-21 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: 2026-09-30 00:00 UTC do 2026-10-21 ok. 17:00 UTC (DAU dzienne), ostatnie 72h (godzinowe), okno "po wydaniu" od 2026-10-19 18:00 UTC
- **Question**: czy wydanie z redesignem (sklepy ok. 19-21.10) zmieniło DAU, powroty uśpionych, sesje, otwarcia pushy i wczesny churn. **Stan PRZED mailem Loops o nowej wersji (21.10 23:30 UTC).**
- **Event verification**: zdarzenia klienta `$lib = posthog-flutter` płyną (460-5438/dzień). `$session_id` obecny na 99% zdarzeń klienta (7d). `notification_opened` płynie (21d: 35 zdarzeń / 9 os., ostatnie 2026-10-20 03:59, tylko starsze wersje). `moment.sent/scheduled/expired` płyną (backend, ostatnie 21.10). `moment.opened` ostatnio 2026-10-18. `user_logged_out` płynie. `account_deleted` (backend): 0 w 21 dniach (ostatnie 2026-09-26 wg raportu z 15.10). Brak zdarzeń `Application Opened/Backgrounded`.

## Definicje

- **Wersja nowa** = `$app_version = '2.0.117'` (Android build 188, iOS build 184, `$is_testflight = false`). Pierwsze zdarzenia na produkcji: Android 2026-10-19 18:13, iOS 2026-10-19 20:44 UTC. Buildy 2.0.113-2.0.116 z 19.10 to wyłącznie buildy wewnętrzne/testowe.
- **Testerzy wykluczeni na poziomie osoby** (ostrzej niż raporty z 15.10, które filtrowały zdarzenia): każda osoba, która w 120d miała zdarzenie z TestFlight, emulatora, `$device_model` w (`OnePlus8Pro`, `Pixel 6 Pro`, `sdk_gphone%`, `iPhone99%`) albo z buildów 2.0.113-2.0.116. Wykluczono 92 osoby.
- **Aktywny (ściśle)** = definicja z `2026-10-15-retention-engagement.md`: zdarzenie klienta po zalogowaniu (bez splash/welcome/auth, `onboarding_*`, `signup_*`, `consent_*`, uprawnień do powiadomień, zdarzeń systemowych). Liczone po `person_id`, czas UTC.
- **Uśpiony, który wrócił** = aktywny w oknie, z ostatnią wcześniejszą aktywnością starszą niż 7 dni przed początkiem okna.
- **Sesja** = `$session_id`; długość = max-min timestamp zdarzeń ścisłych w sesji; wersja sesji = najwyższa `$app_version` w sesji.
- **Prywatność**: jak w raportach z 15.10, liczniki < 5 to n<5 tam, gdzie wskazują grupę; przy podstawach < 25 osób tylko liczby, bez odsetków. Same liczby w tym raporcie to agregaty całej populacji, nie segmenty.

## 1. DAU dzienne (ściśle, bez testerów)

| dzień | DAU | iOS | Android | na 2.0.117 |
|---|---|---|---|---|
| 09-30 | 5 | 2 | 3 | 0 |
| 10-01 | 8 | 2 | 6 | 0 |
| 10-02 | 6 | 1 | 5 | 0 |
| 10-03 | 7 | 3 | 4 | 0 |
| 10-04 | 7 | 3 | 4 | 0 |
| 10-05 | 8 | 1 | 7 | 0 |
| 10-06 | 8 | 2 | 6 | 0 |
| 10-07 | 6 | 2 | 4 | 0 |
| 10-08 | 1 | 1 | 0 | 0 |
| 10-09 | 7 | 1 | 6 | 0 |
| 10-10 | 7 | 1 | 6 | 0 |
| 10-11 | 11 | 1 | 10 | 0 |
| 10-12 | 8 | 1 | 7 | 0 |
| 10-13 | 2 | 1 | 1 | 0 |
| 10-14 | 12 | 4 | 8 | 0 |
| 10-15 | 2 | 0 | 2 | 0 |
| 10-16 | 7 | 0 | 7 | 0 |
| 10-17 | 7 | 1 | 6 | 0 |
| 10-18 | 8 | 1 | 7 | 0 |
| 10-19 | 9 | 2 | 7 | 0 |
| 10-20 | 5 | 0 | 5 | 2 |
| 10-21 (do ok. 17 UTC) | 4 | 2 | 2 | 4 |

Średnie: 10-08..10-14 = 6.9/dzień, 10-15..10-21 = 6.0/dzień. Dni 10-08, 10-13, 10-15 są niskie naprawdę (ingest z obu bibliotek działał, zdarzenia klienta w te dni pochodziły głównie od testerów).

Okna kroczące (ściśle, bez testerów): **WAU 27** (iOS 6, Android 21), poprzednie 7 dni **33**, **MAU 81**. Baseline 15.10 (filtr zdarzeniowy): WAU 29.6-35.7, MAU 73-82.7. MAU stabilne, WAU lekko w dół.

## 2. DAU godzinowe, ostatnie 72h

W żadnej godzinie nie było więcej niż 2 aktywnych osób (22 godziny z aktywnością na 72). iOS: 1 osoba w 4 godzinach (10-19 11h, 15h, 16h; 10-21 7h, 16h, 17h), reszta Android. Nie ma widocznego skoku po publikacji w sklepach (Android 10-19 18h, iOS 10-20). Pełna tabela w zapytaniu `dau_hourly`.

## 3. Powroty uśpionych (okno 2.9 dnia od 19.10 18:00 vs to samo okno 7 i 14 dni wcześniej)

| okno | aktywni | pierwszy raz | wrócili <7d | uśpieni >=7d, którzy wrócili | uśpieni >=14d | aktywni na 2.0.117 |
|---|---|---|---|---|---|---|
| po wydaniu (10-19 18:00 do teraz) | 10 | 5 | 5 | **0** | 0 | 5 |
| -7 dni | 10 | 5 | 4 | n<5 (1) | n<5 (1) | 0 |
| -14 dni | 12 | 4 | 6 | n<5 (2) | n<5 (2) | 0 |

Wydanie nie przyniosło żadnego powrotu uśpionej osoby. Po wydaniu 10 aktywnych: 8 Android (3 na 2.0.117), 2 iOS (obie na 2.0.117).

## 4. Sesje

| okres | wersja | sesje | osoby | sesje/os. | mediana s | p75 s | śr. s | sesje <30 s | zdarzeń/sesję |
|---|---|---|---|---|---|---|---|---|---|
| ostatnie 7d | 2.0.117 | 6 | 5 | 1.2 | 186 | 1932 | 1115 | 0 | 66 |
| ostatnie 7d | starsze | 56 | 25 | 2.24 | 23.5 | 166 | 319 | 29 | 20 |
| poprzednie 7d | starsze (tylko) | 63 | 33 | 1.91 | 55 | 346 | 383 | 26 | 26 |
| po wydaniu | 2.0.117 | 6 | 5 | 1.2 | 186 | 1932 | 1115 | 0 | 66 |
| po wydaniu | starsze | 6 | 5 | 1.2 | 65.5 | 104 | 102 | 3 | 16 |

Sesje na 2.0.117 są dłuższe i gęstsze, ale n=5 osób (2 z nich to nowi, w pierwszej sesji, gdzie pierwsza rozmowa wydłuża czas). To nie jest jeszcze sygnał efektu redesignu.

## 5. Powiadomienia push

### Wysyłki (backend, `moment.sent` z `has_token = true`) i otwarcia (klient, `notification_opened`, bez testerów)

| okno | typ | wysłane z tokenem | osoby | otwarcia | osoby otwierające |
|---|---|---|---|---|---|
| ostatnie 48h | THERAPY_APPOINTMENT | 3 | 3 | 0 | 0 |
| ostatnie 48h | RE_ENGAGEMENT | 1 | 1 | 0 | 0 |
| ostatnie 48h | (brak typu) | 0 | 0 | 1 | 1 |
| 48h tydzień wcześniej (10-12/13) | RE_ENGAGEMENT | 76 | 72 | 0 | 0 |
| 48h tydzień wcześniej | THERAPY_APPOINTMENT | 3 | 3 | 0 | 0 |
| 48h tydzień wcześniej | MOOD_UPDATE_REQUEST | 3 | 3 | 0 | 0 |
| 48h tydzień wcześniej | THERAPY_PREP | 1 | 1 | 0 | 0 |

Wysyłki dzienne z tokenem: 10-12: 160, 10-13: 20, 10-14: 5, 10-15: 3, 10-16: 0, 10-17: 1, 10-18: 25, 10-19: 15, **10-20: 2, 10-21: 1**. Kadencja jest "skokowa" (paczki RE_ENGAGEMENT 10-12, REFLECTION_INVITATION 10-18), więc porównanie 48h vs tydzień wcześniej mierzy głównie paczkę z 10-12. Planowanie trwa (`moment.scheduled` 31 w 10-20, 17 w 10-21), ale większość momentów wygasa (`moment.expired` 38 i 21).

`notification_opened` w 21 dniach (bez testerów): 35 zdarzeń / 9 osób, 1-6 dziennie. **Zero otwarć na 2.0.117** (także wśród testerów). Na iOS `notification_opened` w 90 dniach: 6 zdarzeń / 4 osoby, wszystkie testerskie (ostatnie 10-19 na buildzie TestFlight). `moment.opened` (backend) ostatnio 2026-10-18.

### Deep linki (21d, wszystkie wersje sprzed 2.0.117, bez testerów)

Następny `$screen` po `notification_opened` w większości zgadza się z `deep_link_route`: `/fab/record-session` do `recordSessionFlow` (2), `/therapy/weekly-summary/*` do `weeklySummaryDetail` (3), `/therapy/recording/*` do `recordingDetail` (2), `/health-check` do `healthCheckFlow`, `/fab/prepare-therapy` do `prepTherapyFlow`. Rozjazdy (pojedyncze): `/fab/record-session` i `.../workspace?section=goals` do `splash` (cold start), `/therapy/recording/2047` do `mainPageTab`, `/therapy/monthly-audit/5341` do `subscription` (bramka premium). 10 z 30 otwarć bez `deep_link_route` (głównie `background_resume` do `mainPageTab`). **Na nowej wersji deep linków nie da się jeszcze ocenić: brak danych.**

## 6. Wczesny churn na nowej wersji

| miara | wartość |
|---|---|
| osoby z dowolnym zdarzeniem klienta na 2.0.117 (bez testerów) | 7 (iOS 2, Android 5) |
| w tym nowi (pierwsze zdarzenie od razu na 2.0.117) | 4 |
| w tym aktualizujący z wcześniejszej wersji | 3 (żaden nie był uśpiony >=7d) |
| zaktualizowali ponad 24h temu | 2 |
| z nich wrócili po >=12h | 0 |
| aktywni ściśle na 2.0.117 | 5 (2 nowi, 3 aktualizujący) |
| `account_deleted` / `account_deletion_started`, 21d | 0 / 0 |
| `user_logged_out`, 21d, osobo-dni | 19, z czego 17 to testerzy; prawdziwe tylko 10-15 i 10-16 (po 1), przed wydaniem |

Okno jest za krótkie na churn (2 osoby po 24h). Żadnego sygnału usunięcia konta ani wylogowań u prawdziwych użytkowników.

## Caveats

- **Stan przed mailem Loops** (21.10 23:30 UTC). Mail jest pierwszym bodźcem, który może obudzić uśpionych; aktualizacja w sklepie sama nikogo nie powiadamia.
- Wydanie trwa niecałe 3 dni, adopcja 2.0.117 to 7 prawdziwych osób. Wszystkie porównania wersji to n<25: liczby, nie wnioski.
- Wykluczanie testerów po osobie jest ostrzejsze niż w raportach z 15.10, dlatego DAU tu (6-7/dzień) wychodzi niżej niż baseline 8.4-9.7. Trend porównuj w ramach tego raportu.
- `notification_opened` na iOS praktycznie nie pojawia się od prawdziwych użytkowników (90d: 0), więc otwarcia pushy są mierzalne tylko na Androidzie. Albo iOS-owi użytkownicy nie otwierają pushy, albo zdarzenie nie odpala się na iOS poza buildem testowym; do sprawdzenia na urządzeniu (flutter-mobile).
- `moment.sent` z `has_token=false` to wysyłki bez urządzenia; liczone tylko z tokenem.
- Ingest od 2026-04-22: wcześniejsza aktywność do definicji "uśpiony" liczona od tej daty.
- Powtórka zalecana 23.10 i 28.10 (po mailu): okno 7 dni po wydaniu, powroty uśpionych, otwarcia pushy na 2.0.117.

## Queries

Makra (wstawiane dosłownie w miejsce `{T}`, `{S}`):

```sql
-- {T} wykluczenie testerów po osobie
person_id NOT IN (SELECT DISTINCT person_id FROM events WHERE timestamp > now() - INTERVAL 120 DAY AND properties.$lib = 'posthog-flutter' AND (properties.$is_testflight = true OR properties.$is_emulator = true OR properties.$device_model IN ('OnePlus8Pro','Pixel 6 Pro') OR properties.$device_model LIKE 'sdk_gphone%' OR properties.$device_model LIKE 'iPhone99%' OR properties.$app_version IN ('2.0.113','2.0.114','2.0.115','2.0.116')))
-- {S} aktywność ściśle
properties.$lib = 'posthog-flutter' AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received','$pageleave','welcome_cta_tapped','signup_started','signup_method_selected','auth_method_tapped','auth_validation_failed','auth_mode_switched','login_failed','signup_failed','password_reset_requested','password_reset_failed','signup_email_verification_viewed','signup_email_verified','consent_screen_viewed','consent_granted','notification_permission_prompted','notification_permission_granted','notification_permission_denied','user_logged_in','user_logged_out') AND NOT startsWith(event, 'onboarding_') AND NOT (event IN ('$screen','tab_switched') AND properties.$screen_name IN ('splash','welcome','auth','signUp','forgotPassword','therapyOnboarding','wow'))
-- {R} = toDateTime('2026-10-19 18:00:00')
```

```sql
-- @@ dau_daily
SELECT toDate(timestamp) d, count(DISTINCT person_id) dau, count(DISTINCT if(properties.$os='iOS', person_id, NULL)) ios, count(DISTINCT if(properties.$os='Android', person_id, NULL)) android, count(DISTINCT if(properties.$app_version='2.0.117', person_id, NULL)) on117, count() ev
FROM events WHERE timestamp >= toDateTime('2026-09-30 00:00:00') AND {S} AND {T} GROUP BY d ORDER BY d

-- @@ dau_hourly
SELECT toStartOfHour(timestamp) h, count(DISTINCT person_id) u, count(DISTINCT if(properties.$os='iOS', person_id, NULL)) ios, count(DISTINCT if(properties.$os='Android', person_id, NULL)) android
FROM events WHERE timestamp > now() - INTERVAL 72 HOUR AND {S} AND {T} GROUP BY h ORDER BY h

-- @@ wau_windows
SELECT count(DISTINCT if(timestamp > now() - INTERVAL 7 DAY, person_id, NULL)) wau_now, count(DISTINCT if(timestamp > now() - INTERVAL 14 DAY AND timestamp <= now() - INTERVAL 7 DAY, person_id, NULL)) wau_prev, count(DISTINCT if(timestamp > now() - INTERVAL 30 DAY, person_id, NULL)) mau_now,
 count(DISTINCT if(timestamp > now() - INTERVAL 7 DAY AND properties.$os='iOS', person_id, NULL)) wau_ios, count(DISTINCT if(timestamp > now() - INTERVAL 7 DAY AND properties.$os='Android', person_id, NULL)) wau_and
FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND {S} AND {T}

-- @@ returners (jeden blok na okno; off = 0, 7, 14; a = {R} - INTERVAL off DAY, b = now() - INTERVAL off DAY; łączone UNION ALL)
SELECT '<label>' w, count() active, countIf(prev_ts = toDateTime(0)) first_time, countIf(prev_ts > toDateTime(0) AND prev_ts >= a - INTERVAL 7 DAY) recent, countIf(prev_ts > toDateTime(0) AND prev_ts < a - INTERVAL 7 DAY) dormant7, countIf(prev_ts > toDateTime(0) AND prev_ts < a - INTERVAL 14 DAY) dormant14, countIf(prev_ts > toDateTime(0) AND prev_ts < a - INTERVAL 7 DAY AND has117 > 0) dormant7_on117, countIf(has117 > 0) on117
FROM (SELECT person_id, maxIf(timestamp, timestamp < a) prev_ts, countIf(timestamp >= a AND timestamp < b) inw, countIf(timestamp >= a AND timestamp < b AND properties.$app_version='2.0.117') has117
 FROM events WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND timestamp < b AND {S} AND {T} GROUP BY person_id HAVING inw > 0)

-- @@ sessions (okna: ostatnie 7d, poprzednie 7d, od {R})
SELECT grp, count() sessions, count(DISTINCT pid) persons, round(count()/count(DISTINCT pid),2) sess_per_person, quantile(0.5)(dur) med_s, quantile(0.75)(dur) p75_s, round(avg(dur)) avg_s, countIf(dur < 30) under30s, round(avg(ev),1) ev_per_sess
FROM (SELECT properties.$session_id sid, any(person_id) pid, if(max(properties.$app_version)='2.0.117','2.0.117','older') grp, dateDiff('second', min(timestamp), max(timestamp)) dur, count() ev
 FROM events WHERE timestamp > <a> AND timestamp <= <b> AND {S} AND {T} AND properties.$session_id != '' GROUP BY sid)
GROUP BY grp ORDER BY grp

-- @@ notif_opened_daily
SELECT toDate(timestamp) d, count() c, count(DISTINCT person_id) u, countIf(properties.$app_version='2.0.117') c117, countIf(NOT ({T})) c_testers
FROM events WHERE event='notification_opened' AND timestamp > now() - INTERVAL 21 DAY GROUP BY d ORDER BY d

-- @@ moment_daily
SELECT toDate(timestamp) d, countIf(event='moment.sent') sent, countIf(event='moment.sent' AND properties.has_token = true) sent_tok, count(DISTINCT if(event='moment.sent' AND properties.has_token = true, person_id, NULL)) sent_tok_u, countIf(event='moment.opened') opened, count(DISTINCT if(event='moment.opened', person_id, NULL)) opened_u, countIf(event='moment.acted') acted
FROM events WHERE event IN ('moment.sent','moment.opened','moment.acted') AND timestamp > now() - INTERVAL 21 DAY GROUP BY d ORDER BY d

-- @@ moment_lifecycle_daily
SELECT toDate(timestamp) d, countIf(event='moment.scheduled') sched, countIf(event='moment.sent') sent, countIf(event='moment.expired') expired, countIf(event='moment.skipped') skipped, count(DISTINCT if(event='moment.scheduled', person_id, NULL)) sched_u
FROM events WHERE event LIKE 'moment.%' AND timestamp > now() - INTERVAL 14 DAY GROUP BY d ORDER BY d

-- @@ push_48h_vs_wk
SELECT w, mt, countIf(event='moment.sent' AND tok) sent_tok, count(DISTINCT if(event='moment.sent' AND tok, person_id, NULL)) sent_users, countIf(event='notification_opened') opened, count(DISTINCT if(event='notification_opened', person_id, NULL)) opened_users
FROM (SELECT event, person_id, properties.moment_type mt, properties.has_token = true tok, if(timestamp > now() - INTERVAL 48 HOUR, 'last48h', 'wk_before') w FROM events
 WHERE event IN ('moment.sent','notification_opened') AND ((timestamp > now() - INTERVAL 48 HOUR) OR (timestamp > now() - INTERVAL 216 HOUR AND timestamp <= now() - INTERVAL 168 HOUR)) AND (event='moment.sent' OR {T}))
GROUP BY w, mt ORDER BY w, sent_tok DESC

-- @@ notif_route_next_screen
SELECT route, app_state, next_screen, countIf(gap <= 60) within60s, count() c, count(DISTINCT pid) u FROM (
 SELECT event, person_id pid, properties.deep_link_route route, properties.app_state app_state, timestamp ts,
  leadInFrame(properties.$screen_name) OVER (PARTITION BY person_id ORDER BY timestamp ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING) next_screen,
  dateDiff('second', timestamp, leadInFrame(timestamp) OVER (PARTITION BY person_id ORDER BY timestamp ROWS BETWEEN CURRENT ROW AND 1 FOLLOWING)) gap
 FROM events WHERE timestamp > now() - INTERVAL 21 DAY AND event IN ('notification_opened','$screen') AND {T})
WHERE event='notification_opened' GROUP BY route, app_state, next_screen ORDER BY c DESC LIMIT 30

-- @@ push_open_ios_90d
SELECT event, properties.$os os, count() c, count(DISTINCT person_id) u, max(timestamp) l FROM events WHERE event IN ('notification_opened','$push_notification_opened','notification_banner_tapped') AND timestamp > now() - INTERVAL 90 DAY GROUP BY event, os LIMIT 20

-- @@ adopters_117_broad
SELECT count() adopters, countIf(prev_ts = toDateTime(0)) new_on_117, countIf(prev_ts > toDateTime(0)) upgraders, countIf(prev_ts > toDateTime(0) AND prev_ts < f117 - INTERVAL 7 DAY) upgraders_dormant7, countIf(f117 < now() - INTERVAL 24 HOUR) adopted_24h_plus, countIf(f117 < now() - INTERVAL 24 HOUR AND last_ts > f117 + INTERVAL 12 HOUR) back_after_12h, countIf(os='iOS') ios, countIf(os='Android') android
FROM (SELECT person_id, minIf(timestamp, properties.$app_version='2.0.117') f117, max(timestamp) last_ts, maxIf(timestamp, properties.$app_version != '2.0.117') prev_ts, any(properties.$os) os
 FROM events WHERE timestamp > now() - INTERVAL 120 DAY AND properties.$lib='posthog-flutter' AND event NOT IN ('$identify','$set','$exception','$pageleave','$feature_flag_called') AND {T} GROUP BY person_id HAVING countIf(properties.$app_version='2.0.117') > 0)

-- @@ logout_delete_daily
SELECT toDate(timestamp) d, count(DISTINCT if(event='account_deleted', person_id, NULL)) deleted, count(DISTINCT if(event='account_deletion_started', person_id, NULL)) del_started, count(DISTINCT if(event='user_logged_out', person_id, NULL)) logout, count(DISTINCT if(event='user_logged_out' AND NOT ({T}), person_id, NULL)) logout_testers
FROM events WHERE event IN ('account_deleted','account_deletion_started','user_logged_out') AND timestamp > now() - INTERVAL 21 DAY GROUP BY d ORDER BY d
```
