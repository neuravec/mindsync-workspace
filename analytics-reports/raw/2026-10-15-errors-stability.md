# Błędy i stabilność aplikacji (30 dni, nacisk na 14 dni): raw PostHog extract

- **Date**: 2026-10-15 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: 2026-09-15 -> 2026-10-15 (30d), główny kąt 2026-10-01 -> 2026-10-15 (14d), UTC
- **Question**: ile błędów, u ilu osób, gdzie (endpoint, platforma, wersja), czy skoczyły po wdrożeniach 03.10 / 05.10 / 14.10 / 15.10, i które najbardziej szkodzą użytkownikowi.
- **Event verification** (event_definitions `last_seen_at`, wszystkie poniższe płyną): `api_error` (backend, `posthog-python`, last 10-15), `client_error` (flutter, 10-15), `$exception` (flutter, 10-15), `auth_validation_failed`, `login_failed`, `password_reset_failed`, `usage_load_failed`, `first_week_plan_failed`, `paywall_load_failed`, `reflect_thread_preview_failed` (flutter, 10-15); `subscription_verification_failed`, `recording_processing_failed`, `recording_chunk_store_failed`, `onboarding_symptom_sync_failed` (backend, 10-14); `voice_session_failed` (10-13), `signup_failed` (10-10), `subscription_purchase_failed` (10-06), `first_conversation_start_failed` (10-05, 1 zdarzenie). Zdefiniowane w `analytics_events.dart`, ale **0 zdarzeń w 30d**: `subscription_restore_failed`, `onboarding_step_save_failed`, `onboarding_load_failed`, `backend_provisioning_failed`, `first_conversation_send_failed`, `error_occurred`. Martwe w oknie: `voice_transcription_failed` (ostatnio 08-29), `recording_upload_failed` (06-21), `debrief_failed` (09-18).

## Results

### A. Wolumen zdarzeń błędów (30d / 14d / poprzednie 14d) i udział top-1 osoby (14d)

| event | lib | 30d zdarz. | 30d osób | 14d zdarz. | 14d osób | prev14 zdarz. | prev14 osób | top-1 osoba 14d |
|---|---|---|---|---|---|---|---|---|
| api_error | python | 4117 | 100 | 2280 | 59 | 1837 | 54 | 26% |
| client_error | flutter | 1596 | 20 | 534 | 13 | 1062 | 11 | 39% |
| subscription_verification_failed | python | 628 | n<5 | 628 | n<5 | 0 | 0 | **90%** |
| $exception | flutter | 157 | 16 | 86 | 10 | 71 | 8 | **81%** |
| recording_processing_failed | python | 137 | n<5 | 136 | n<5 | 1 | n<5 | **100%** |
| onboarding_symptom_sync_failed | python | 91 | n<5 | 91 | n<5 | 0 | 0 | 52% |
| auth_validation_failed | flutter | 62 | 22 | 62 | 22 | 0 (nowe od 10-03) | 0 | 27% |
| login_failed | flutter | 51 | 11 | 51 | 11 | 0 (nowe od 10-03) | 0 | 33% |
| paywall_load_failed | flutter | 51 | n<5 | 51 | n<5 | 0 | 0 | **98%** |
| password_reset_failed | flutter | 39 | 12 | 16 | 5 | 23 | 7 | 50% |
| recording_chunk_store_failed | python | 38 | n<5 | 38 | n<5 | 0 | 0 | 100% |
| subscription_purchase_failed | flutter | 25 | n<5 | 23 | n<5 | 2 | n<5 | 100% |
| usage_load_failed | flutter | 18 | n<5 | 18 | n<5 | 0 | 0 | 67% |
| signup_failed | flutter | 14 | n<5 | 14 | n<5 | 0 | 0 | 93% |
| voice_session_failed | flutter | 4 | n<5 | 4 | n<5 | 0 | 0 | 50% |
| first_week_plan_failed | flutter | 4 | n<5 | 4 | n<5 | 0 | 0 | 50% |
| first_conversation_start_failed | flutter | 1 | n<5 | 1 | n<5 | 0 | 0 | 100% |

Uwaga: `auth_validation_failed`, `login_failed`, `usage_load_failed`, `paywall_load_failed` istnieją dopiero od 2026-10-03 (nowe zdarzenia z redesignu), więc "prev14 = 0" to brak instrumentacji, nie poprawa.

### B. Dziennie (30d): aktywni w aplikacji vs błędy

`app_dau` = osoby z dowolnym zdarzeniem `posthog-flutter` (bez filtrów testflight/emulator/bot). `api_unexp` = `api_error` z `is_expected != true`. `other_fail` = wszystkie `*_failed` + `client_error` (bez `$exception`).

| dzień | app_dau | api_error (os.) | api unexp (os.) | $exception (os.) | other_fail (os.) |
|---|---|---|---|---|---|
| 09-16 | 10 | 51 (3) | 6 (1) | 12 (1) | 21 (1) |
| 09-21 | 18 | 293 (9) | 7 (4) | 5 (2) | 12 (3) |
| 09-23 | 14 | 43 (7) | 5 (3) | 3 (1) | 171 (3) |
| 09-28 | 14 | 305 (6) | 10 (3) | 7 (1) | 13 (2) |
| 09-29 | 20 | 78 (5) | 13 (5) | 0 | 81 (7) |
| 09-30 | 25 | 292 (4) | 1 (1) | 1 (1) | 743 (3) |
| 10-01 | 27 | 167 (13) | 32 (9) | 23 (2) | 3 (1) |
| 10-02 | 24 | 87 (7) | 12 (6) | 6 (1) | 28 (7) |
| **10-03** | 28 | 257 (11) | 13 (9) | 18 (3) | **910 (13)** |
| 10-04 | 20 | 130 (6) | 4 (2) | 1 (1) | 5 (3) |
| **10-05** | 26 | **482 (10)** | 23 (7) | 13 (1) | 129 (10) |
| 10-06 | 25 | 168 (9) | 19 (6) | 13 (2) | 172 (15) |
| 10-07 | 19 | 123 (5) | 7 (3) | 10 (2) | 59 (13) |
| 10-08 | 10 | 48 (5) | 7 (1) | 0 | 91 (7) |
| 10-09 | 17 | 44 (6) | 12 (4) | 1 (1) | 28 (4) |
| 10-10 | 16 | 121 (8) | 15 (7) | 2 (1) | 36 (4) |
| 10-11 | 13 | 139 (11) | 32 (8) | 5 (2) | 75 (8) |
| 10-12 | 17 | 138 (10) | 26 (7) | 4 (2) | 16 (1) |
| 10-13 | 14 | 306 (6) | 8 (2) | 9 (1) | 49 (6) |
| **10-14** | 25 | 142 (14) | 9 (5) | 1 (1) | 23 (9) |
| 10-15 (częśc.) | 9 | 93 (7) | 10 (4) | 3 (1) | 51 (4) |

(Dni 09-17..09-27 bez anomalii pominięte w tabeli, pełne w zapytaniu B.)

### I. Skład dni-skoków (other_fail, wiersze >= 10 zdarzeń)

| dzień | event | typ/powód | zdarz. | osób |
|---|---|---|---|---|
| 09-23 | client_error | FirebaseAuthException | 171 | n<5 |
| 09-30 | client_error | FirebaseAuthException | 741 | n<5 |
| 10-03 | subscription_verification_failed | expired | 478 | n<5 (1 osoba) |
| 10-03 | client_error | FirebaseAuthException | 249 | n<5 |
| 10-03 | subscription_verification_failed | (brak) | 89 | n<5 |
| 10-03 | login_failed | unknown | 22 | n<5 |
| 10-03 | subscription_purchase_failed | store_error | 12 | n<5 |
| 10-05..10-11 | onboarding_symptom_sync_failed | (brak) | 13-25/dzień | n<5 |
| 10-05..10-06 | subscription_verification_failed | apple_status_21002 | 13-16/dzień | n<5 |
| 10-05..10-06 | recording_chunk_store_failed | postgres_store_failed | 12/dzień | n<5 |
| 10-06 | recording_processing_failed | ValueError / ChunkTranscriptionError / RuntimeError | 20+20+20 | n<5 |
| 10-06 | auth_validation_failed | email_empty | 17 | 6 |
| 10-06 | paywall_load_failed | products_not_found | 10 | n<5 |
| 10-08 / 10-11 / 10-13 | client_error | FirebaseAuthException | 48 / 28 / 30 | n<5 |

### C. api_error: endpoint x status (14d), sortowane po osobach

| endpoint | status | is_expected | zdarz. | osób | tydz. 1 | tydz. 2 |
|---|---|---|---|---|---|---|
| /users/get_user_profile_and_subscription | 404 | false | 66 | 37 | 23 | 43 |
| /users/therapy-context | 404 | false | 37 | 36 | 12 | 25 |
| /prep-cards/latest | 404 | true | 373 | 34 | 175 | 198 |
| /debriefs/latest | 404 | true | 542 | 32 | 180 | 362 |
| /health-check/latest | 404 | true | 786 | 31 | 512 | 274 |
| /moments/{id}/dismissed | 404 | false | 10 | 5 | 8 | 2 |
| /between-sessions/latest | 404 | true | 6 | 5 | 3 | 3 |
| /users/profile | **500** | false | 10 | n<5 | 10 | 0 |
| /reflect/{id}/session_data | 403 | true | 313 | n<5 | 313 | 0 |
| /reflect/{id}/audio/agent_m… i user_me… | 404 | false | 3+3 | n<5 | 0 | 6 |
| /dashboard/calltoaction | 400 | false | 25 | n<5 | 10 | 15 |
| /users/therapy-schedule/change | **503** | false | 9 | n<5 | 0 | 9 |
| /users/preferences | 422 | false | 8 | n<5 | 8 | 0 |
| /habits/{id}/checks/{date} | 404 | false | 6 | n<5 | 0 | 6 |
| pozostałe (reflect message/messages/summarize, symptoms scores, audio-v2/live-session 403, debriefs 401, therapy-schedule 401) | różne | | 1-4 | n<5 | | |

Niespodziewane (`is_expected=false`) wg dnia i statusu (14d): 500 tylko 10-02 (1), 10-03 (2), **10-05 (8 zdarz., n<5)**; 503 tylko 10-11 (9, n<5); 401 10-11 i 10-15; 400 codziennie 1-9 zdarzeń od jednej osoby (calltoaction). Reszta to 404.

### K. Kohorta 404 na `get_user_profile_and_subscription` (14d)

| osób z 404 | nowi w oknie | 404 <= 30 min od pierwszego zdarzenia | ukończyli onboarding | aktywni w aplikacji > 10 min po 404 |
|---|---|---|---|---|
| 35 | 35 | 35 | 25 | 15 |

Wszyscy to świeże instalacje w pierwszych minutach: to ścieżka "profil jeszcze nie utworzony" przy pierwszym uruchomieniu, tylko oznaczona jako `is_expected=false`. 25/35 (71%) przechodzi onboarding mimo 404.

### E. $exception wg typu (30d)

| typ | zdarz. | osób | platforma | wersje (przykłady) | okres |
|---|---|---|---|---|---|
| FirebaseAuthException | 40 | 8 | Android | 2.0.94, 2.0.95, 2.0.107, 2.0.109 | 09-21 -> 10-12 |
| _TypeError | 39 | n<5 | iOS + Android | 2.0.92 -> 2.0.105 | 09-16 -> 10-13 |
| ApiException | 21 | n<5 | Android | 2.0.92 -> 2.0.101 | 09-18 -> 10-13 |
| ProviderNotFoundException | 46 | n<5 | Android | 2.0.94 -> 2.0.105 | 09-17 -> **10-15** |
| LateError | 2 | n<5 | Android | 2.0.94, 2.0.100 | 09-25 -> 10-07 |
| String | 8 | n<5 | iOS + Android | do 2.0.112 | 09-19 -> 10-15 |

### J. client_error = FirebaseAuthException wg ekranu (30d), tylko Android

| ekran | zdarz. | osób |
|---|---|---|
| mainPage | 921 | 11 |
| splash | 21 | 5 |
| recordSessionFlow | 195 | n<5 |
| mainPageTab | 270 | n<5 |
| settings | 48 | n<5 |
| therapyOnboarding, auth, afterTherapyFlow | 1-3 | n<5 |

Razem `client_error` 30d: FirebaseAuthException 1462 zdarz. / 18 osób, `String` 104 / n<5, `_Exception` 27 / 5. Zero iOS.

### D. Powody błędów klienta i zakupów (30d)

| event | powód | zdarz. | osób |
|---|---|---|---|
| auth_validation_failed | email_empty | 42 | 20 |
| auth_validation_failed | email_invalid | 19 | n<5 |
| login_failed | unknown | 36 | 7 |
| login_failed | invalid_credentials / cancelled / network | 8 / 5 / 2 | n<5 |
| password_reset_failed | (brak właściwości powodu) | 39 | 12 |
| signup_failed | register_failed | 14 | n<5 |
| voice_session_failed | webrtc_failure | 3 | n<5 |
| voice_session_failed | ice_failed | 1 | n<5 |
| paywall_load_failed | products_not_found / store_unavailable / _Exception / timeout | 30 / 12 / 8 / 1 | n<5 (prawie wszystko 1 osoba) |
| subscription_purchase_failed | store_error / user_cancelled / pending | 13 / 8 / 4 | n<5 |
| subscription_verification_failed | expired / (brak) / apple_status_21002 | 478 / 89 / 61 | n<5 (2 osoby) |
| recording_processing_failed | ValueError / RuntimeError / ChunkTranscriptionError | 46 / 45 / 45 | n<5 (1 osoba) |
| recording_chunk_store_failed | postgres_store_failed | 38 | n<5 (1 osoba) |
| onboarding_symptom_sync_failed | (brak) | 91 | n<5 |
| usage_load_failed | http_5xx / network | 12 / 6 | n<5 |

### F/L/M/G. Odsetek dotkniętych (14d, aktywni = osoby z dowolnym zdarzeniem flutter)

| miara | wartość |
|---|---|
| aktywni w aplikacji 14d | 165 (Android 148, iOS 17) |
| dowolny błąd (wszystkie powyższe zdarzenia + api unexpected) | 79 / 165 = 48% (Android 73/148 = 49%, iOS 6/17 = 35%) |
| "realny" błąd (bez walidacji formularza, anulowania przez usera, oczekiwanych 404/403) | 63 / 165 = 38% |
| realny błąd bez 404 profilu/therapy-context przy pierwszym uruchomieniu | **35 / 165 = 21%** |
| $exception | 10 / 165 = 6% |
| sesje klienta (`$session_id`) z >= 1 zdarzeniem błędu klienta | 124 / 492 = 25% (zawiera `auth_validation_failed`) |
| błąd głosu (`voice_session_failed`, `first_conversation_start_failed`) vs osoby próbujące rozmowy | n<5 / 26 |
| błąd płatności (paywall_load / purchase / verification) vs osoby z `paywall_shown` | n<5 / 24 |

### H. Wersje x platforma (14d, wersje z >= 3 aktywnymi; błędy = zdarzenia klienta z listy, z walidacją)

| wersja | os | aktywni | osób z błędem | zdarz. błędów | od |
|---|---|---|---|---|---|
| 2.0.111 | iOS / Android | 3 / 6 | n<5 / n<5 | 1 / 1 | 10-14 |
| 2.0.110 | iOS / Android | 3 / 11 | n<5 / n<5 | 1 / 9 | 10-13 |
| 2.0.109 | Android | 6 | n<5 | 31 | 10-12 |
| 2.0.108 | Android | 3 | n<5 | 66 | 10-07 |
| 2.0.107 | Android | 45 | 9 (20%) | 126 | 10-07 |
| 2.0.106 | iOS / Android | 7 / 3 | 0 / n<5 | 0 / 9 | 10-07 |
| 2.0.105 | Android | 5 | n<5 | 43 | 10-06 |
| 2.0.100 | Android / iOS | 55 / 9 | 19 (35%) / n<5 | 72 / 6 | 10-03 |
| 2.0.95 | Android | 27 | n<5 | 54 | 10-01 |
| 2.0.94 | Android / iOS | 15 / 6 | n<5 / 0 | 198 / 0 | 10-01 |

Żadna wersja nie pokazuje nagłego skoku liczby **osób** z błędami. Skoki zdarzeń (2.0.94: 198, 2.0.108: 66) to 2-3 osoby w pętli. Najwyższy odsetek osób: 2.0.100 Android 35% (wersja z redesignu 03.10, największa kohorta).

## Caveats

- `api_error` i wszystkie zdarzenia `posthog-python` nie mają `$app_version`/`$os`/`$session_id`: podział na wersje i sesje dotyczy tylko błędów klienta. Endpointy backendu dzielone wg ścieżki/statusu/dnia.
- Wiele "dużych" wolumenów to **pojedyncze osoby w pętli** (verification 90%, recording 100%, paywall_load 98%, $exception 81%). Liczyć w osobach, nie w zdarzeniach.
- `auth_validation_failed`, `login_failed`, `usage_load_failed`, `paywall_load_failed` wprowadzone 10-03: brak porównania z wcześniejszym okresem.
- `password_reset_failed` i `onboarding_symptom_sync_failed` nie niosą powodu błędu.
- Filtry testflight/emulator/bot-device nie zostały zastosowane (dane klientów od wielu wersji; zysk z filtra przy n<5 marginalny). Część pętli może pochodzić od kont testowych.
- 15.10 (GPT-Live-1) to dzień częściowy; FE tylko w TestFlight. Brak zdarzeń błędów głosu po 10-13 i tylko 2 zdarzenia 403 `audio-v2/live-session` (is_expected=true), więc jeszcze nic nie można powiedzieć o stabilności nowego silnika.
- Ingest od 2026-04-22: bez wpływu na okno 30d.

## Queries

Lista `$EV` użyta niżej:
`('$exception','client_error','first_week_plan_failed','usage_load_failed','login_failed','password_reset_failed','auth_validation_failed','reflect_thread_preview_failed','paywall_load_failed','recording_processing_failed','onboarding_symptom_sync_failed','subscription_verification_failed','recording_chunk_store_failed','signup_failed','voice_session_failed','subscription_purchase_failed','first_conversation_start_failed','recording_chunk_upload_failed','debrief_failed','voice_transcription_failed','subscription_restore_failed','onboarding_step_save_failed','onboarding_load_failed','backend_provisioning_failed','first_conversation_send_failed','error_occurred')` (w A dodatkowo `'api_error'`).

```sql
-- @@ A_error_events_summary
SELECT event, any(properties.$lib) lib,
 countIf(timestamp > now() - INTERVAL 30 DAY) c30, count(DISTINCT if(timestamp > now() - INTERVAL 30 DAY, person_id, NULL)) u30,
 countIf(timestamp > now() - INTERVAL 14 DAY) c14, count(DISTINCT if(timestamp > now() - INTERVAL 14 DAY, person_id, NULL)) u14,
 countIf(timestamp <= now() - INTERVAL 14 DAY) cprev14, count(DISTINCT if(timestamp <= now() - INTERVAL 14 DAY, person_id, NULL)) uprev14,
 max(timestamp) last_ts
FROM events WHERE timestamp > now() - INTERVAL 28 DAY - INTERVAL 2 DAY AND event IN $EV_plus_api_error
GROUP BY event ORDER BY c30 DESC LIMIT 40

-- @@ A2_top1_share_14d
SELECT event, sum(cnt) total, max(cnt) top1, round(max(cnt)/sum(cnt),2) top1_share FROM (
 SELECT event, person_id, count() cnt FROM events WHERE timestamp > now() - INTERVAL 14 DAY AND event IN $EV_plus_api_error GROUP BY event, person_id)
GROUP BY event ORDER BY total DESC LIMIT 40

-- @@ B_daily
SELECT toDate(timestamp) d,
 count(DISTINCT if(properties.$lib='posthog-flutter', person_id, NULL)) app_dau,
 countIf(event='api_error') api_err, count(DISTINCT if(event='api_error', person_id, NULL)) api_err_u,
 countIf(event='api_error' AND toString(properties.is_expected) != 'true') api_unexp, count(DISTINCT if(event='api_error' AND toString(properties.is_expected) != 'true', person_id, NULL)) api_unexp_u,
 countIf(event='$exception') exc, count(DISTINCT if(event='$exception', person_id, NULL)) exc_u,
 countIf(event IN $EV AND event != '$exception') other_fail, count(DISTINCT if(event IN $EV AND event != '$exception', person_id, NULL)) other_fail_u
FROM events WHERE timestamp > now() - INTERVAL 30 DAY
GROUP BY d ORDER BY d

-- @@ C_api_error_endpoints_14d
SELECT substring(replaceRegexpAll(toString(properties.endpoint), '[0-9a-fA-F-]{16,}|/[0-9]+', '/:id'),1,70) ep, toString(properties.status_code) st, toString(properties.is_expected) exp,
 count() c, count(DISTINCT person_id) u, countIf(timestamp <= now() - INTERVAL 7 DAY) c_wk1, countIf(timestamp > now() - INTERVAL 7 DAY) c_wk2
FROM events WHERE event='api_error' AND timestamp > now() - INTERVAL 14 DAY
GROUP BY ep, st, exp ORDER BY u DESC, c DESC LIMIT 30

-- @@ C2_api_error_status_class_by_day14
SELECT toDate(timestamp) d, toString(properties.status_code) st, count() c, count(DISTINCT person_id) u
FROM events WHERE event='api_error' AND timestamp > now() - INTERVAL 14 DAY AND toString(properties.is_expected) != 'true'
GROUP BY d, st ORDER BY d, c DESC LIMIT 120

-- @@ D_client_error_reasons_30d
SELECT event, substring(coalesce(nullIf(JSONExtractString(toString(properties),'error_type'),''), nullIf(JSONExtractString(toString(properties),'error_code'),''), nullIf(JSONExtractString(toString(properties),'failure_reason'),''), nullIf(JSONExtractString(toString(properties),'reason'),''), nullIf(JSONExtractString(toString(properties),'error_class'),''), nullIf(JSONExtractString(toString(properties),'stage'),''), '(none)'),1,50) reason,
 count() c, count(DISTINCT person_id) u, max(timestamp) last_ts
FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND event IN $EV AND event != '$exception'
GROUP BY event, reason ORDER BY event, u DESC LIMIT 80

-- @@ E_exception_types_30d
SELECT substring(toString(properties.$exception_types),1,60) typ, count() c, count(DISTINCT person_id) u, groupUniqArray(5)(toString(properties.$app_version)) vers, groupUniqArray(3)(toString(properties.$os_name)) oses, min(timestamp) first_ts, max(timestamp) last_ts
FROM events WHERE event='$exception' AND timestamp > now() - INTERVAL 30 DAY
GROUP BY typ ORDER BY u DESC, c DESC LIMIT 20

-- @@ F_affected_share_14d
SELECT os, count() active_u, countIf(any_err) err_u, countIf(unexp_api) unexp_api_u, countIf(cli_err) cli_err_u, countIf(exc) exc_u FROM (
 SELECT person_id,
  anyIf(toString(properties.$os), properties.$lib='posthog-flutter') os,
  countIf(properties.$lib='posthog-flutter') > 0 app_active,
  countIf(event='api_error' AND toString(properties.is_expected) != 'true') > 0 unexp_api,
  countIf(event IN $EV) > 0 cli_err,
  countIf(event='$exception') > 0 exc,
  (countIf(event='api_error' AND toString(properties.is_expected) != 'true') + countIf(event IN $EV)) > 0 any_err
 FROM events WHERE timestamp > now() - INTERVAL 14 DAY GROUP BY person_id
) WHERE app_active GROUP BY os WITH ROLLUP ORDER BY active_u DESC

-- @@ G_session_share_14d
SELECT count() sessions, countIf(has_err) err_sessions FROM (
 SELECT $session_id sid, countIf(event IN $EV) > 0 has_err FROM events
 WHERE timestamp > now() - INTERVAL 14 DAY AND properties.$lib='posthog-flutter' AND $session_id != '' AND $session_id IS NOT NULL GROUP BY sid)

-- @@ H_version_client_errors_14d
SELECT toString(properties.$app_version) ver, toString(properties.$os) os, count(DISTINCT person_id) active_u,
 count(DISTINCT if(event IN $EV, person_id, NULL)) err_u, countIf(event IN $EV) err_c, countIf(event='$exception') exc_c, min(timestamp) first_ts
FROM events WHERE timestamp > now() - INTERVAL 14 DAY AND properties.$lib='posthog-flutter'
GROUP BY ver, os HAVING active_u >= 3 ORDER BY first_ts DESC LIMIT 40

-- @@ I_spike_days_composition
SELECT toDate(timestamp) d, event, substring(coalesce(nullIf(JSONExtractString(toString(properties),'error_type'),''), nullIf(JSONExtractString(toString(properties),'failure_reason'),''), nullIf(JSONExtractString(toString(properties),'reason'),''), nullIf(JSONExtractString(toString(properties),'error_class'),''), '-'),1,30) r, count() c, count(DISTINCT person_id) u
FROM events WHERE toDate(timestamp) IN ('2026-09-23','2026-09-29','2026-09-30','2026-10-03','2026-10-05','2026-10-06','2026-10-07','2026-10-08','2026-10-11','2026-10-13')
 AND timestamp > now() - INTERVAL 30 DAY AND event NOT IN ('api_error','$exception') AND (event LIKE '%_failed' OR event = 'client_error')
GROUP BY d, event, r HAVING c >= 10 ORDER BY d, c DESC LIMIT 60

-- @@ J_firebase_auth_client_error_screens_30d
SELECT substring(toString(properties.$screen_name),1,40) scr, toString(properties.$os) os, count() c, count(DISTINCT person_id) u, min(timestamp) first_ts, max(timestamp) last_ts
FROM events WHERE event='client_error' AND timestamp > now() - INTERVAL 30 DAY AND toString(properties.error_type)='FirebaseAuthException'
GROUP BY scr, os ORDER BY u DESC LIMIT 15

-- @@ K_profile404_cohort_14d
SELECT count() u_404, countIf(first_ts > now() - INTERVAL 14 DAY) new_in_window, countIf(abs(dateDiff('minute', first_ts, t404)) <= 30) within_30min_of_first_seen, countIf(onb_done) onboarding_completed, countIf(last_app > t404 + INTERVAL 10 MINUTE) app_active_10min_after FROM (
 SELECT person_id, min(timestamp) first_ts,
  minIf(timestamp, event='api_error' AND toString(properties.endpoint)='/api/v1/users/get_user_profile_and_subscription' AND toString(properties.status_code)='404') t404,
  countIf(event='onboarding_completed') > 0 AS onb_done,
  maxIf(timestamp, properties.$lib='posthog-flutter') last_app
 FROM events WHERE timestamp > now() - INTERVAL 20 DAY GROUP BY person_id
) WHERE t404 > now() - INTERVAL 14 DAY

-- @@ L_real_error_share_14d
SELECT count() active_u, countIf(real_err) real_err_u, countIf(voice_err) voice_err_u, countIf(voice_try) voice_try_u, countIf(pay_err) pay_err_u, countIf(pay_seen) paywall_seen_u FROM (
 SELECT person_id, countIf(properties.$lib='posthog-flutter') > 0 app_active,
  countIf((event='api_error' AND toString(properties.is_expected) != 'true') OR event IN ('$exception','client_error','first_week_plan_failed','usage_load_failed','paywall_load_failed','recording_processing_failed','onboarding_symptom_sync_failed','recording_chunk_store_failed','signup_failed','voice_session_failed','first_conversation_start_failed','reflect_thread_preview_failed','password_reset_failed') OR (event='login_failed' AND toString(properties.reason) IN ('unknown','network')) OR (event='subscription_purchase_failed' AND toString(properties.failure_reason) != 'user_cancelled')) > 0 real_err,
  countIf(event IN ('voice_session_failed','first_conversation_start_failed')) > 0 voice_err,
  countIf(event IN ('reflect_session_started','voice_session_started','first_conversation_started','reflect_mode_selected')) > 0 voice_try,
  countIf(event IN ('paywall_load_failed','subscription_purchase_failed','subscription_verification_failed')) > 0 pay_err,
  countIf(event='paywall_shown') > 0 pay_seen
 FROM events WHERE timestamp > now() - INTERVAL 14 DAY GROUP BY person_id) WHERE app_active

-- @@ M_real_error_share_excl_profile404_14d
-- jak L.real_err, ale api_error dodatkowo z endpoint NOT IN ('/api/v1/users/get_user_profile_and_subscription','/api/v1/users/therapy-context')
```
