# Błędy funkcjonalne w przepływach po wydaniu redesignu: raw PostHog extract

- **Date**: 2026-10-21 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: ostatnie 48h (2026-10-19 ~17:00 -> 2026-10-21 ~17:00 UTC) vs poprzednie 7 dni (2026-10-12 -> 2026-10-19), UTC
- **Question**: jakie błędy funkcjonalne (nie crashe) występują w kluczowych przepływach na nowej wersji sklepowej vs starszych, per endpoint, status i osoba.
- **Wersja sklepowa**: `2.0.117` (first_seen Android 2026-10-19 18:13, iOS 2026-10-19 20:44, na iOS `$is_testflight=false`, czyli build z App Store). `2.0.113`-`2.0.116` to buildy z 19.10 z tym samym redesignem (iOS z `$is_testflight=true`), traktowane jako "pre-release". Starsze: `2.0.110` (największa kohorta) i niżej.
- **Event verification** (wszystkie płyną, last_seen 10-19..10-21): `api_error` (backend), `$exception`, `client_error`, `login_failed`, `first_week_plan_failed`, `paywall_load_failed`, `usage_load_failed`, `workspace_section_load_failed` (nowe, od 10-19), `character_sheet_load_failed` (nowe, 10-19), `follow_up_failed` (nowe, pierwszy raz 2026-10-21 16:47), `subscription_restore_empty`, `$rageclick`. W oknie 9d z zerem w 48h: `voice_session_failed`, `voice_transcription_failed`, `debrief_failed`, `recording_processing_failed`, `recording_chunk_store_failed`, `subscription_verification_failed`, `auth_validation_failed`, `password_reset_failed`, `onboarding_step_save_failed`. **Brak w ogóle w 9d**: `subscription_purchase_failed`, `subscription_restore_failed`, `$dead_click`, jakiekolwiek zdarzenie "empty state" ekranów Main/kart/Timeline (poza `orca_memory_empty_cta_tapped`, `subscription_restore_empty`).

## Skala ruchu (kontekst do normalizacji)

| miara | wartość |
|---|---|
| DAU aplikacji (flutter) 10-19 / 10-20 / 10-21 (częśc.) | 23 / 10 / 8 |
| aktywni w 48h na 2.0.113+ | 12 (2.0.117: Android 9, iOS 3, 1 bez $os) |
| aktywni w 48h na starszych | 12 |
| nowe instalacje (pierwsze zdarzenie flutter w 48h) | 7 |
| osób z jakimkolwiek zdarzeniem błędu klienta na 2.0.113-2.0.117 (3 dni) | 6, z czego **1 osoba = 79/101 zdarzeń** |

Ta jedna osoba (Android, 3112 zdarzeń w 3 dni, przeskakiwała przez 5 buildów 2.0.113 -> 2.0.117 w ciągu jednego dnia 19.10) prawie na pewno jest testerem z zespołu. Wszystkie poniższe "skoki" na nowych buildach trzeba czytać z tym zastrzeżeniem.

## Results

### A. api_error: endpoint x status, 48h vs poprzednie 7d

| endpoint | status | is_expected | zdarz. 48h | osób 48h | zdarz. prev7 | osób prev7 | ostatnio |
|---|---|---|---|---|---|---|---|
| /health-check/latest | 404 | true | 95 | 8 | 375 | 17 | 10-21 |
| /debriefs/latest | 404 | true | 40 | 7 | 358 | 17 | 10-21 |
| /prep-cards/latest | 404 | true | 15 | 5 | 195 | 17 | 10-21 |
| /users/get_user_profile_and_subscription | 404 | false | 6 | 5 | 36 | 14 | 10-21 |
| /users/therapy-context | 404 | false | 4 | 4 | 13 | 13 | 10-21 |
| /dashboard/calltoaction | 400 | false | 2 | 1 | 11 | 1 | 10-21 |
| /analytics/emotion_pie | 400 | false | 1 | 1 | 0 | 0 | 10-21 (nowe) |
| /reflect/{id}/message | 404 | false | 1 | 1 | 4 | 1 | 10-20 |
| /between-sessions/latest | 404 | true | 1 | 1 | 4 | 4 | 10-20 |
| **/gamification/ke/sheet** | **404** | false | 0 | 0 | **33** | **5** | 10-19 10:51 |
| /users/get_user_profile_and_subscription | 403 | true | 0 | 0 | 14 | 2 | 10-18 |
| /analytics/period_card | 422 / 404 / 401 | false | 0 | 0 | 12 / 6 / 6 | 1 | 10-18 |
| /users/therapy-schedule | 401 | false | 0 | 0 | 2 | 2 | 10-17 |
| /audio-v2/live-session (+ /end) | 403 | true | 0 | 0 | 2 + 2 | 1 | 10-15 |
| pozostałe (reflect audio/messages/summarize 404/409, debriefs 401, health-check/{id} 403) | | | 0 | 0 | 1-2 | 1 | do 10-19 |

- **5xx w api_error: 0 zdarzeń w całym oknie 9 dni.** (W raporcie z 10-15 były 500 na /users/profile i 503 na therapy-schedule; nie powtórzyły się.)
- Udział top-1 osoby w api_error 48h: 48% (165 zdarzeń, 11 osób), prawie w całości oczekiwane 404 "latest".
- 404 profilu przy pierwszym uruchomieniu: 3 z 7 nowych instalacji w 48h (wcześniej 35/35 nowych w 14d). Ten sam znany wzorzec "profil jeszcze nie utworzony", nadal oznaczony `is_expected=false`.

Niespodziewane api_error dziennie (is_expected != true): 10-18 to szczyt (34x 404 od 4 osób + 12x 422 + 6x 401 od 1 osoby, okno wdrożenia Character KD v2), 10-19 24x 404 od 8 osób (ke/sheet + profil), 10-20 1, 10-21 6x 404 od 3 osób.

### B. Błędy klienta (flutter) 48h vs prev7

| event | zdarz. 48h | osób 48h | zdarz. prev7 | osób prev7 | uwagi |
|---|---|---|---|---|---|
| client_error | 16 | 1 | 238 | 6 | 48h: `String` od testera; prev7: FirebaseAuthException 205 zdarz. / 5 osób na 2.0.107-2.0.111 (Android, znana pętla) |
| paywall_load_failed | 10 | 1 | 15 | 2 | tylko Android, `products_not_found` / `store_unavailable` |
| $exception | 9 | 1 | 21 | 2 | ProviderNotFoundException, ApiException, String, _TypeError |
| $rageclick | 9 | 1 | 32 | 6 | patrz F |
| login_failed | 4 | 2 | 11 | 5 | 2.0.117 iOS `cancelled` x3 (1 os.), Android `unknown` x1 |
| follow_up_failed | 4 | 1 | 0 | 0 | **nowe 10-21**, iOS 2.0.117, `status_class=not_found`, 4x w 2 min |
| first_week_plan_failed | 2 | 2 | 11 | 3 | `status_class=error`, na każdej wersji od 2.0.109 do 2.0.117 |
| workspace_section_load_failed | 2 | 1 | 13 | 2 | nowe od 10-19; sekcje threads, todo, agenda, questions, goals, realizations |
| usage_load_failed | 2 | 1 | 9 | 4 | `http_5xx` (Android, 10-19..10-20) i `network` |
| subscription_restore_empty | 1 | 1 | 1 | 1 | 2.0.111 Android |
| character_sheet_load_failed | 0 | 0 | 3 | 1 | `5xx`, 2.0.113 Android, 10-19 07:27-07:30 |
| debrief_failed + voice_transcription_failed | 0 | 0 | 2 + 2 | 1 | `ApiException`, 2.0.113 Android, 10-19 07:54 |
| subscription_verification_failed | 0 | 0 | 9 (+9 backend) | 1 | `expired`, iOS 2.0.114 TestFlight (sandbox) |
| auth_validation_failed | 0 | 0 | 20 | 3 | 17 z nich `email_invalid` od 1 osoby |
| password_reset_failed | 0 | 0 | 9 | 2 | bez powodu w zdarzeniu |
| voice_session_failed | 0 | 0 | 1 | 1 | `webrtc_failure`, iOS 2.0.110, 10-13 |

### C. Nowe buildy (2.0.113-2.0.117), 3 dni: osoby z błędem / aktywni

| wersja | os | aktywni | z błędem |
|---|---|---|---|
| 2.0.117 | Android | 9 | 2 |
| 2.0.117 | iOS | 3 | 1 |
| 2.0.116 | Android / iOS | 3 / 2 | 2 / 0 |
| 2.0.115 | Android / iOS | 2 / 1 | 1 / 0 |
| 2.0.114 | Android / iOS | 5 / 2 | 1 / 1 |
| 2.0.113 | Android / iOS | 3 / 1 | 2 / 0 |

Rozkład po osobach (hash, bez identyfikatorów): osoba A (tester) 79 zdarzeń, wszystkie typy (paywall_load, usage_load, workspace, character_sheet, first_week_plan, ProviderNotFoundException); osoba B 9 (verification expired, TestFlight); osoba C 7 (login cancelled + follow_up_failed, iOS 2.0.117); osoba D 4 (debrief/transcription ApiException); osoby E, F po 1 (first_week_plan_failed na 2.0.117, workspace threads na 2.0.116). **Poza testerem żaden typ błędu nie dotknął więcej niż 1 osoby na nowej wersji.**

### D. Przepływy

| przepływ | 48h (wszystkie wersje) | nowa wersja 2.0.117 | błędy |
|---|---|---|---|
| Rozmowa głosowa Classic (`voice_chat_started/ended`) | 2 os. start, 1 os. end | **0 sesji** (3 osoby na 2.0.117 miały Reflect, wszystkie w trybie `text`) | 0 w 48h; ostatni `voice_session_failed` 10-13 |
| Live Preview (`voice_engine_*`, `voice_live_session_ended`, `voice_chat_*` z `voice_engine=live`) | 0 | 0 | 0; w 9d tylko 1 osoba (2.0.112) użyła Live, 2 sesje zakończone, 403 na live-session 10-15 (oczekiwane, gate) |
| Pierwsza rozmowa (`first_conversation_*`) | 2-3 os. start/end | 1/1, zakończona przez usera | 0 |
| Nagrywanie sesji / voice notes (`recording_*`, `voice_transcription_*`) | 2 start, 4 saved, 3/3 transkrypcji ok | brak na 2.0.117 | 0 w 48h; 10-19 2x ApiException debrief + transcription (tester-like, 2.0.113) |
| Reflect | 8 sesji / 5 os. | 6 sesji / 3 os. (text) | 1x 404 /reflect/{id}/message (10-20) |
| Logowanie | 17 `user_logged_in` / 2 os., 25 `auth_method_tapped` / 6 os. | | 4 `login_failed` / 2 os. (cancelled, unknown); 0 FirebaseAuthException w 48h |
| Zakupy | paywall_shown 2.0.117: 2 os., obie odrzuciły | brak purchase_started | 0 `subscription_purchase_failed` w 9d (zdarzenie nie płynie). 2.0.111 Android 10-20: 8x `purchase_started` w 1 min + restore_empty, **bez completed i bez failed** |
| Powiadomienia | prompted 27 / granted 27, 8 os. | 15 / 15, 5 os. (3 na osobę) | 0 denied w 48h; `source=cold_prompt` odpala się ~3-4x na osobę z granted za każdym razem |

### E. Ekrany nowego redesignu (load failed / empty)

| ekran | zdarzenie | 9d | uwagi |
|---|---|---|---|
| Workspace | workspace_section_load_failed | 15 zdarz. / 2 os. | 13 z nich od testera na 2.0.113 (10-19 07:07-07:29), 2 od 2 osób na 2.0.116 (sekcja threads) |
| Character | character_sheet_load_failed `5xx` | 3 / 1 | 10-19 07:27, tester; równolegle backend `ke/sheet` 404 33x / 5 os. do 10-19 10:51 |
| Main (plan tygodnia) | first_week_plan_failed | 13 / 4 os. łącznie | utrzymuje się od 10-13, także na 2.0.117 (10-21 09:13) |
| Main (usage chip) | usage_load_failed `http_5xx` | 5 / 1 + network 4 / 3 | 5xx widziane przez klienta nie mają odpowiednika w api_error |
| Follow-up (nowe) | follow_up_failed `not_found` | 4 / 1 | pierwszy raz 10-21 16:47, iOS 2.0.117 |
| Timeline, karty | brak zdarzeń *_failed / *_empty | | nie zinstrumentowane albo brak błędów, nie da się rozróżnić |

### F. Rage clicks (9d)

| wersja | zdarz. | osób | sesji |
|---|---|---|---|
| 2.0.117 | 12 | 1 | 1 (iOS, 10-21 16:58) |
| 2.0.111 | 18 | 3 | 3 |
| 2.0.110 | 13 | 3 | 5 |
| 2.0.106 | 1 | 1 | 1 |

Ekran ostatniego `$screen` przed rage click (iOS, 9d, ASOF join po sesji): mainPage 22, afterTherapyFlow 5, firstWeekHabits 4, wow 3, therapyOnboarding 3, myTherapy 2, reszta 1. `$dead_click` nie istnieje w projekcie.

## Caveats

- **Bardzo mała próba.** DAU aplikacji 8-23, 12 osób na nowych buildach w 48h. Każdy wiersz z 1-2 osobami to anegdota, nie trend. Wydanie sklepowe ma niecałe 2 doby, a Android 2.0.117 pojawił się 19.10 wieczorem (rollout trwa).
- **k-anonimowość**: zgodnie z praktyką z ekstraktu 10-15 pokazano dokładne liczby osób także poniżej 25, bo są to wyłącznie zdarzenia techniczne (błędy, statusy), bez danych zdrowotnych, treści i identyfikatorów. Osoby rozróżnione tylko hashem modulo 1000 w sekcji C. Jeśli raport ma iść dalej, segmenty < 5 osób należy oznaczyć "n<5".
- **Tester**: jedna osoba Android generuje ~78% błędów klienta na nowych buildach. Nie ma flagi wewnętrznego konta w PostHog (`$is_testflight` na Androidzie zawsze null), więc wykluczenie jest wnioskiem z zachowania (5 buildów w 1 dzień, 3112 zdarzeń / 3 dni).
- `api_error` (backend) nie niesie `$app_version`/`$os`: podziału na wersje dla endpointów nie da się zrobić.
- **Luka pomiaru 5xx**: klient raportuje `http_5xx` (`usage_load_failed`, `character_sheet_load_failed`) 10-19..10-20, a `api_error` ma 0 zdarzeń 5xx w 9d. Prawdopodobnie 5xx z routera Heroku (restart/deploy) albo wyjątek poza middleware; potwierdzić w logach Heroku (integration-devops).
- `subscription_purchase_failed`, `subscription_restore_failed` nie płyną w 9d, więc wynik zakupu "bez completed i bez failed" (2.0.111) jest niewidoczny w PostHog. Prawda o płatnościach: `subscription_receipts` w Postgres (database-administrator).
- Na 2.0.117 nie było ani jednej sesji głosowej (Classic ani Live), więc o stabilności głosu na nowej wersji nie da się nic powiedzieć.
- Ingest od 2026-04-22: bez wpływu na okno.

## Queries

Pliki robocze: `C:\Users\mikol\AppData\Local\Temp\claude\C--Users-mikol-Notebooks-MindSync-Heroku\b6f3940a-d5d1-4f79-a0d3-90675bd0a564\scratchpad\a2-errors\p1.sql` ... `p9.sql`. Kluczowe zapytania verbatim:

```sql
-- versions
SELECT properties.$app_version AS ver, properties.$os AS os, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events WHERE timestamp > now() - INTERVAL 10 DAY AND properties.$lib='posthog-flutter' AND properties.$app_version != '' AND properties.$app_version IS NOT NULL
GROUP BY ver, os ORDER BY first_ts DESC LIMIT 25

-- error_events (48h vs prev 7d)
SELECT event, properties.$lib AS lib,
 countIf(timestamp > now() - INTERVAL 48 HOUR) AS c48, count(DISTINCT if(timestamp > now() - INTERVAL 48 HOUR, person_id, NULL)) AS u48,
 countIf(timestamp <= now() - INTERVAL 48 HOUR AND timestamp > now() - INTERVAL 9 DAY) AS cprev7, count(DISTINCT if(timestamp <= now() - INTERVAL 48 HOUR AND timestamp > now() - INTERVAL 9 DAY, person_id, NULL)) AS uprev7,
 min(timestamp) AS first_in_window
FROM events WHERE timestamp > now() - INTERVAL 9 DAY
 AND (event ILIKE '%fail%' OR event ILIKE '%error%' OR event ILIKE '%exception%' OR event ILIKE '%rage%' OR event ILIKE '%dead%' OR event ILIKE '%empty%' OR event ILIKE '%timeout%' OR event ILIKE '%disconnect%' OR event ILIKE '%denied%' OR event ILIKE '%limit_hit%')
GROUP BY event, lib ORDER BY u48 DESC, c48 DESC LIMIT 80

-- api_endpoint_status
SELECT replaceRegexpAll(toString(properties.endpoint), '[0-9a-f]{8}-[0-9a-f-]{27,}|/[0-9]+(/|$)', '{id}') AS ep, properties.status_code AS st, properties.is_expected AS exp,
 countIf(timestamp > now() - INTERVAL 48 HOUR) c48, count(DISTINCT if(timestamp > now() - INTERVAL 48 HOUR, person_id, NULL)) u48,
 countIf(timestamp <= now() - INTERVAL 48 HOUR) cprev7, count(DISTINCT if(timestamp <= now() - INTERVAL 48 HOUR, person_id, NULL)) uprev7, max(timestamp) last_ts
FROM events WHERE event='api_error' AND timestamp > now() - INTERVAL 9 DAY
GROUP BY ep, st, exp ORDER BY u48 DESC, c48 DESC, uprev7 DESC LIMIT 60

-- api_5xx_detail (0 rows)
SELECT toDate(timestamp) d, toString(properties.endpoint) ep, properties.status_code st, properties.error_class ec, count() c, count(DISTINCT person_id) u
FROM events WHERE event='api_error' AND timestamp > now() - INTERVAL 9 DAY AND toInt(properties.status_code) >= 500 GROUP BY d, ep, st, ec ORDER BY d LIMIT 50

-- client_err_detail
SELECT event, properties.$app_version ver, properties.$os os,
 coalesce(toString(properties.reason), toString(properties.error_type), toString(properties.status_class), toString(properties.section_name), toString(properties.failure_reason), toString(properties.error_class), '') why,
 toString(properties.section_name) sec, count() c, count(DISTINCT person_id) u, min(timestamp) f, max(timestamp) l
FROM events WHERE timestamp > now() - INTERVAL 9 DAY AND properties.$lib='posthog-flutter' AND (event ILIKE '%fail%' OR event IN ('client_error','$exception','subscription_restore_empty'))
GROUP BY event, ver, os, why, sec ORDER BY event, l DESC LIMIT 100

-- exception_types
SELECT properties.$app_version ver, properties.$os os, toString(properties.$exception_list[1].type) t, count() c, count(DISTINCT person_id) u, max(timestamp) l
FROM events WHERE event='$exception' AND timestamp > now() - INTERVAL 9 DAY GROUP BY ver, os, t ORDER BY l DESC LIMIT 30

-- new_ver_err_by_person (hash only)
SELECT cityHash64(toString(person_id)) % 1000 p, groupUniqArray(toString(properties.$app_version)) vers, groupUniqArray(event) evs, count() c
FROM events WHERE timestamp > now() - INTERVAL 3 DAY AND properties.$app_version IN ('2.0.113','2.0.114','2.0.115','2.0.116','2.0.117') AND (event ILIKE '%fail%' OR event IN ('client_error','$exception'))
GROUP BY p ORDER BY c DESC LIMIT 10

-- voice_mode_new_ver
SELECT ver, toString(mode) mode, count() sessions, count(DISTINCT person_id) u, sum(vc) persons_voice_chat_evt FROM (
 SELECT e.person_id person_id, e.properties.mode mode, v.ver ver, v.vc vc FROM events e
 JOIN (SELECT person_id, argMaxIf(toString(properties.$app_version), timestamp, properties.$lib='posthog-flutter' AND properties.$app_version != '') ver, countIf(event IN ('voice_chat_started','voice_chat_ended','voice_session_failed','voice_live_session_ended')) vc
       FROM events WHERE timestamp > now() - INTERVAL 3 DAY GROUP BY person_id) v ON v.person_id = e.person_id
 WHERE e.event='reflect_session_started' AND e.timestamp > now() - INTERVAL 3 DAY)
GROUP BY ver, mode ORDER BY ver DESC

-- notif_source
SELECT toString(properties.$app_version) ver, toString(properties.source) src, count() c, count(DISTINCT person_id) u
FROM events WHERE event='notification_permission_prompted' AND timestamp > now() - INTERVAL 9 DAY GROUP BY ver, src ORDER BY ver DESC LIMIT 30

-- rage_screen (ASOF join, iOS)
SELECT s.scr scr, count() c FROM (
 SELECT properties.$session_id sid, timestamp ts FROM events WHERE event='$rageclick' AND timestamp > now() - INTERVAL 9 DAY) r
 ASOF LEFT JOIN (SELECT properties.$session_id sid, timestamp ts, toString(properties.$screen_name) scr FROM events WHERE event='$screen' AND timestamp > now() - INTERVAL 9 DAY AND properties.$os='iOS') s
 ON r.sid = s.sid AND r.ts >= s.ts
GROUP BY scr ORDER BY c DESC LIMIT 20
```
