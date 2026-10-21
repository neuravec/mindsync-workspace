# Wpływ wydań 03.10-15.10.2026 na zachowanie użytkowników: surowy wyciąg PostHog

- **Data**: 2026-10-15 · **Agent**: posthog-data-extractor
- **Projekt**: PostHog EU 141170 · **Okno**: 2026-09-19 00:00 UTC -> 2026-10-15 ~18:00 UTC (oś wersji od 2026-09-15)
- **Pytanie**: czy wydania od 03.10 (subskrypcje + onboarding -> głosowy Reflect -> paywall, pierwsza rozmowa v2, first-week guidance, redesign kart, GPT-Live-1) zmieniły zachowanie i czy ich zdarzenia płyną.
- **Tygodnie** (UTC): W1 = 09-19..09-25, W2 = 09-26..10-02 (oba "przed"), W3 = 10-03..10-09, W4 = 10-10..10-15 (**tylko 6 dni, niepełny**).
- **Filtry domyślne**: `$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')` (boty Play), `$is_emulator` != true; metryki aplikacji `properties.$lib = 'posthog-flutter'`; użytkownicy = `count(DISTINCT person_id)`. Kolumna `non_tf` wyklucza iOS TestFlight (Android nie ma takiej flagi).
- **Prywatność**: tylko agregaty; grupy poniżej 5 osób oznaczone `n<5` (próg z polecenia zlecającego; domyślny próg agenta to 25, przy tym wolumenie zablokowałby cały raport).
- **Weryfikacja zdarzeń**: katalog `event_definitions` pobrany 15.10 (292 linie). Wszystkie zdarzenia użyte w tabelach mają `last_seen_at` w ostatnich 7 dniach, wyjątki opisane w sekcji 3.

## 1. Oś wersji `$app_version` x kanał

Kanał: `iOS_TF` = iOS z `$is_testflight=true`; `iOS_store_or_dev` = iOS bez flagi TestFlight (App Store albo build z Xcode); `Android` = sklep lub ścieżka testowa Play (nie da się rozdzielić w PostHog); `other` = `$os` inny/pusty.

| wersja | kanał | pierwsze zdarzenie (UTC) | użytk. od 09-15 | użytk. 7d (od 10-08) | odczyt |
|---|---|---|---|---|---|
| 2.0.94 | Android | 09-19 | 104 | 0 | poprzednia wersja sklepowa |
| 2.0.94 | iOS_store_or_dev | 09-19 | 12 | 0 | poprzednia wersja App Store |
| 2.0.95 | Android | 10-01 | 27 | n<5 | sklep, przed redesignem |
| 2.0.97-2.0.99 | iOS_TF / Android | 10-03 | n<5 na build | 0 | testy redesignu subskrypcji |
| **2.0.100** | **Android** | **10-03 12:11** | **53** | 5 | **pierwszy build sklepowy z redesignem 03.10** |
| 2.0.100 | iOS_store_or_dev | 10-03 12:59 | 8 | n<5 | App Store z redesignem 03.10 |
| 2.0.101-2.0.105 | iOS_TF / Android | 10-05..10-06 | n<5 na build | 0 | testy pierwszej rozmowy v2 |
| **2.0.106** | iOS_store_or_dev | 10-07 13:55 | 6 | 5 | App Store z pierwszą rozmową v2 |
| **2.0.107** | **Android** | **10-07 14:56** | **42** | **41** | **główna wersja sklepowa Android teraz** |
| 2.0.108 | Android / iOS_TF | 10-07 | n<5 | n<5 | testerzy |
| 2.0.109 | Android / iOS_TF | 10-12 10:44 | n<5 | n<5 | first-week guidance (pierwsze `today_card_viewed`) |
| 2.0.110 | Android | 10-13 11:39 | 9 | 9 | prawdopodobnie ścieżka testowa Play lub etapowe wdrożenie; nie da się rozstrzygnąć z PostHog |
| 2.0.110 | iOS_TF / iOS_store_or_dev | 10-13 | n<5 | n<5 | testerzy / build z Xcode |
| 2.0.111 | iOS_TF / Android | 10-14 14:44 | n<5 | n<5 | redesign kart/Workspace/Character |
| 2.0.112 | iOS_TF | 10-15 05:40 | n<5 | n<5 | GPT-Live-1 |

Wniosek z osi: zmiany z 03.10 trafiły do sklepu w 2.0.100 tego samego dnia. Pierwsza rozmowa głosowa v2 (05.10) dotarła do sklepowych użytkowników dopiero w 2.0.107 Android (pierwsze `onboarding_completed` na tej wersji 10-09 04:40, pierwsze `first_conversation_started` 10-09 23:11) i 2.0.106 iOS. **Zmiany z 09.10-15.10 (first-week guidance, redesign kart, Live) są w praktyce tylko u testerów** (TestFlight + garstka Android na 2.0.109-2.0.112).

## 2. Przed / po: kluczowe wskaźniki tygodniowo

### 2a. Aktywni i nowi (aplikacja)

| tydzień | aktywni | aktywni non_tf | Android | iOS | nowi użytk. (pierwsze zdarzenie flutter) |
|---|---|---|---|---|---|
| W1 09-19 | 54 | 53 | 47 | 9 | 33 |
| W2 09-26 | 97 | 96 | 88 | 9 | 76 |
| W3 10-03 | 94 | 94 | 84 | 12 | 66 |
| W4 10-10 (6 dni) | 54 | 52 | 45 | 11 | 34 |

### 2b. Lejek tygodniowo (users / zdarzenia)

| zdarzenie (lib) | W1 | W2 | W3 | W4 (6 dni) |
|---|---|---|---|---|
| `signup_started` (flutter) | 11 | 17 | 14 | 22 |
| `onboarding_started` (flutter) | 12 | 16 | 16 | 22 |
| `onboarding_completed` (flutter) | 6 | 10 | 13 (35 zd., 1 tester = 10) | 20 |
| `post_onboarding_build_viewed` | brak zdarzenia | brak zdarzenia | 10 | 20 |
| `first_conversation_intro_viewed` | brak | brak | n<5 | 17 |
| `first_conversation_started` | brak | brak | n<5 (18 zd., tylko testerzy) | 15 |
| `first_conversation_ended` | brak | brak | n<5 | 11 |
| `voice_chat_started` (flutter, każde wejście) | 5 | n<5 | n<5 (27 zd.) | 11 |
| `reflect_session_started` (backend) | 7 | 7 | 8 | 21 |
| `trial_started` (backend) | brak zdarzenia | brak zdarzenia | 21 | 33 |
| `paywall_shown` (flutter) | n<5 | n<5 | 12 (41 zd.) | 13 |
| `subscription_screen_opened` | n<5 | n<5 | 13 (68 zd.) | 10 |
| `subscription_purchase_started` | 0 | n<5 | 5 (35 zd., top1 = 64%) | n<5 |
| `subscription_purchase_completed` (flutter + backend, łącznie) | n<5 | n<5 | 6 (291 zd., top1 = 140) | 5 |
| `subscription_purchase_failed` | 0 | n<5 | n<5 (23 zd., 1 osoba) | 0 |

Proporcje (przybliżone, `onboarding_completed` / `signup_started`): W1 0.55, W2 0.59, W3 0.93, W4 0.91.

### 2c. Kohorta nowych użytkowników, zdarzenia w 7 dni od pierwszego zdarzenia

| kohorta | nowi | z pełnym oknem 7d | onboarding | pierwsza rozmowa | voice (dowolny) | sesja Reflect (BE) | paywall | trial (BE) | zakup | powrót d1-d7 |
|---|---|---|---|---|---|---|---|---|---|---|
| W1 09-19 | 33 | 33 | 7 (21%) | 0 | n<5 | n<5 | 0 | 0 | 0 | n<5 |
| W2 09-26 | 76 | 76 | 9 (12%) | 0 | n<5 | n<5 | n<5 | 0 | n<5 | 9 (12%) |
| W3 10-03 | 66 | 56 | 9 (14%) | n<5 | n<5 | n<5 | 7 (11%) | 12 (18%) | n<5 | 11 (17%) |
| W4 10-10 | 34 | **0** | 19 (56%) | 15 (44%) | 8 (24%) | 15 (44%) | 10 (29%) | 22 (65%) | n<5 | 6 (cenzura) |

### 2d. Rozbicia (flutter)

`paywall_shown` po `trigger_feature`, użytkownicy:

| trigger | W1 | W2 | W3 | W4 |
|---|---|---|---|---|
| post_onboarding | 0 | 0 | 5 | 7 |
| post_onboarding_all_plans | 0 | 0 | n<5 | n<5 |
| drawer_menu | n<5 | n<5 | n<5 (14 zd.) | 0 |
| premium_gate_reflect_voice | 0 | 0 | n<5 (12 zd.) | n<5 |
| trial_banner / trial_ended_popup / trial_reminder | 0 | 0 | n<5 każdy | n<5 każdy |
| inne bramki (habits, after_therapy, session_recording, reflect_messages, monthly_audit) | 0 | n<5 | n<5 | n<5 |

`post_onboarding_offer_result` W4: continued_to_plans n<5, closed_plans n<5, closed_offer n<5, purchased_starter n<5 (10 zdarzeń, 6 osób). W3 dominują `skipped_ineligible` i `skipped` (testerzy, `onboarding_rerun`/`already_premium`).

`first_conversation_started` po `mode/entry_point`: W4 voice/intro 8, text/type_instead n<5, text/mic_denied n<5. `first_conversation_ended` W4: 11 zakończeń (11 osób), mediana czasu 358 s, mediana wypowiedzi użytkownika 8, `reached_open` 9 z 11. W3 (testerzy): mediana 134 s, 4 wypowiedzi.

`voice_chat_started` po `entry_point`: W4 onboarding_first_conversation 8, mode_choice 5, reflect_continuation n<5.

## 3. Czy nowe zdarzenia płyną (od 2026-10-01)

| funkcja | zdarzenie | zdarzenia | użytk. | kanał | wersje | pierwsze |
|---|---|---|---|---|---|---|
| First-week guidance | `today_card_viewed` | 12 | n<5 | Android + iOS_TF | 2.0.109-2.0.111 | 10-12 |
| | `today_card_tapped` | 3 | n<5 | Android | 2.0.110-2.0.111 | 10-13 |
| | `first_week_plan_toggled` | 31 | n<5 | Android + iOS_TF | 2.0.109-2.0.110 | 10-12 |
| | `first_week_plan_hidden` / `_hide_undone` / `_failed` | 1 / 1 / 2 | n<5 | iOS_TF | 2.0.109-2.0.112 | 10-13 |
| | `side_card_tapped` / `side_card_dismiss_undone` | 8 / 1 | n<5 | Android + iOS_TF | 2.0.109-2.0.110 | 10-12 |
| | `reminder_optin_result` / `reminder_time_changed` | 12 / 1 | n<5 | Android + iOS_TF | 2.0.109-2.0.110 | 10-12 |
| | `session_sheet_completed` | 2 | n<5 | Android + iOS_TF | 2.0.109-2.0.110 | 10-12 |
| | `follow_up_started` | 2 | n<5 | Android | 2.0.110 | 10-13 |
| | `fab_menu_opened` / `fab_flow_selected` / `fab_menu_dismissed` | 14 / 6 / 8 | 5 / n<5 / n<5 | Android + iOS dev | 2.0.109-2.0.110 | 10-12 |
| | `trial_reminder_sheet_shown` / `_result` | 3 / 3 | n<5 | Android | 2.0.107, 2.0.111 | 10-09 |
| | `trial_bar_viewed` | 39 | 16 | Android (15) + iOS_TF | 2.0.100+ | 10-04 |
| | `art9_consent_step_shown` / `_declined` | 7 / 6 | n<5 | iOS_TF | 2.0.110 | 10-13 |
| Redesign kart/Workspace/Character | `workspace_item_action` | 17 | n<5 | Android + iOS_TF | 2.0.111 | 10-14 |
| | `after_card_progress_viewed` | 2 | n<5 | Android + iOS_TF | 2.0.111 | 10-14 |
| | `profiling_unlock_tapped` / `_consent_confirmed` / `_consent_cancelled` | po 1 | n<5 | iOS_TF | 2.0.112 | 10-15 |
| | `prep_card_opened` | 14 | n<5 | Android + iOS_TF | 2.0.109-2.0.111 | 10-12 |
| GPT-Live-1 | `voice_engine_changed` | 1 | n<5 | iOS_TF | 2.0.112 | 10-15 05:40 |
| | `voice_engine_selected` (backend) | 2 | n<5 | backend | | 10-15 05:40 |
| | `voice_live_session_ended` (backend) | 2 | n<5 | backend | | 10-15 05:41 |
| | `voice_chat_started` z `voice_engine=live` | 2 | n<5 | iOS_TF | 2.0.112 | 10-15 |

**Zdefiniowane w kodzie (origin/dev), nigdy nie widziane w PostHog** (brak w `event_definitions`): `first_week_recap_viewed`, `first_week_recap_dismissed`, `first_week_recap_failed`, `first_week_recap_retry_tapped`, `first_week_action_failed`, `today_card_deferred`, `today_card_defer_undone`, `side_card_dismissed`, `quick_checkin_completed`, `quick_checkin_abandoned`, `quick_checkin_load_failed`, `quick_checkin_retry_tapped`, `session_sheet_opened`, `session_sheet_dismissed`, `follow_up_dismissed`, `follow_up_failed`, `follow_up_check_in_tapped`, `checkin_next_step_tapped`, `checkin_empty_trends_tapped`, `rhythm_sheet_opened`, `rhythm_selected`, `getting_started_card_tapped`, `reminder_open_settings_tapped`, `voice_live_fallback`, `voice_moderation_event`, `voice_delegation_attempted`, `user_fragments_merged`, `art9_consent_onboarding_shown`. Przy tej liczbie testerów to raczej brak okazji niż defekt, ale nie jest to jeszcze zweryfikowane.

Właściwości nowych zdarzeń (potwierdzone `JSONExtractKeys`): `voice_engine_selected` {engine, reason, session_kind}; `voice_engine_changed` {engine, previous_engine}; `voice_live_session_ended` {agent_turns, user_turns, billed_seconds, close_reason, model, session_kind}; `today_card_viewed` {plan_active}; `first_week_plan_toggled` {expanded}; `workspace_item_action` {action, section_name}; `after_card_progress_viewed` {state, sessions_bucket, has_carry_forward, lock_reason}; `first_conversation_ended` {mode, reason, duration_s, user_turns, reached_open, started, input/output/cached_tokens, user_fragments}.

## Zastrzeżenia

- **Okna po zmianie są za krótkie na wnioski.** W4 ma 6 dni, kohorta W4 nie ma ani jednej osoby z pełnym oknem 7 dni. Funkcje z 09-15.10 nie są w sklepie, więc w PostHog nie ma żadnego "po" dla prawdziwych użytkowników; to tylko potwierdzenie, że instrumentacja żyje.
- **Rozjazd czasowy 05.10**: pierwsza rozmowa v2 dotarła do sklepowych użytkowników Android ~09.10 (2.0.107), więc efekt "po 05.10" widać dopiero w W4. W3 dla `first_conversation_*` to prawie wyłącznie testerzy.
- **Brak bazy "przed"** dla `post_onboarding_build_viewed`, `first_conversation_*`, `trial_started` (backend, pierwszy raz 10-03): wartości przed 03.10 to "zdarzenie nie istniało", nie zero zachowania.
- **Mianownik nowych użytkowników jest zaszumiony**: W2 ma 76 nowych osób, ale tylko 17 `signup_started`, więc duża część "nowych" to instalacje bez rejestracji (możliwe też boty Play na innych modelach niż wykluczone). Stąd skok udziału onboardingu W4 (56% vs 12-21%) jest częściowo efektem mniejszego mianownika (34 nowych w W4). Stabilniejsza proporcja `onboarding_completed`/`signup_started` też rośnie (0.55-0.59 -> 0.91-0.93), ale W3 zawiera testerów powtarzających onboarding.
- **Skew pojedynczych osób**: `subscription_purchase_completed` W3 291 zdarzeń / 6 osób (jedna osoba 140, pętla testowa przy naprawie płatności iOS), `user_activated` W3 197 / 6 (top1 127), `subscription_purchase_failed` W3 23 zdarzenia od 1 osoby, `reflect_mode_selected` top1 40-56%. Liczby zakupów z PostHog nie są prawdą przychodową; do tego `subscription_receipts` w Postgres przez `database-administrator`.
- **Android: sklep vs testy nie do odróżnienia** (brak odpowiednika `$is_testflight`). Klasyfikacja 2.0.110 Android (9 osób) jako "ścieżka testowa lub etapowe wdrożenie" jest wnioskiem z liczebności, nie z danych.
- **`voice_engine`** jest tylko na 2 z 53 `voice_chat_started`; sesje Classic na starszych buildach nie mają tej właściwości, więc podział Live vs Classic można liczyć wyłącznie jako "live" vs "brak", i tylko od 2.0.112.
- Ingest od 2026-04-22; first-seen nowych użytkowników liczony od tej daty.

## Zapytania (HogQL, dosłownie)

Wspólny fragment filtrów (wstawiony w każde zapytanie):
```sql
coalesce(properties.$device_model, '') NOT IN ('OnePlus8Pro','Pixel 6 Pro')
AND coalesce(toString(properties.$is_emulator), '') NOT IN ('true','1')
-- kanał:
multiIf(properties.$os IN ('iOS','iPadOS') AND toString(properties.$is_testflight) IN ('true','1'), 'iOS_TF',
        properties.$os IN ('iOS','iPadOS'), 'iOS_store_or_dev', properties.$os = 'Android', 'Android', 'other')
-- tydzień:
multiIf(timestamp < toDateTime('2026-09-26'), 'W1_0919', timestamp < toDateTime('2026-10-03'), 'W2_0926',
        timestamp < toDateTime('2026-10-10'), 'W3_1003', 'W4_1010p')
```

```sql
-- @@ q1_versions
SELECT properties.$app_version AS ver, <kanał> AS chan, min(timestamp) AS first_ts, max(timestamp) AS last_ts,
  count(DISTINCT person_id) AS users,
  count(DISTINCT if(timestamp >= toDateTime('2026-10-08 00:00:00'), person_id, NULL)) AS users_7d
FROM events WHERE timestamp >= toDateTime('2026-09-15 00:00:00') AND properties.$lib = 'posthog-flutter'
  AND <filtry> AND properties.$app_version != '' AND properties.$app_version IS NOT NULL
GROUP BY ver, chan ORDER BY first_ts DESC LIMIT 80

-- @@ q2_weekly_events
SELECT <tydzień> AS wk, event, properties.$lib AS lib, count() AS c, count(DISTINCT person_id) AS users,
  count(DISTINCT if(NOT (properties.$os IN ('iOS','iPadOS') AND toString(properties.$is_testflight) IN ('true','1')), person_id, NULL)) AS users_non_tf
FROM events WHERE timestamp >= toDateTime('2026-09-19 00:00:00') AND <filtry>
  AND event IN ('onboarding_started','onboarding_completed','post_onboarding_build_viewed','post_onboarding_offer_shown',
    'post_onboarding_offer_not_shown','post_onboarding_offer_result','paywall_shown','paywall_dismissed','subscription_screen_opened',
    'subscription_purchase_started','subscription_purchase_completed','subscription_purchase_failed','subscription_purchase_pending',
    'one_time_purchase_completed','trial_started','first_conversation_intro_viewed','first_conversation_started','first_conversation_ended',
    'first_conversation_skipped','first_conversation_start_failed','voice_chat_started','reflect_session_started','reflect_mode_selected',
    'signup_started','user_activated')
GROUP BY wk, event, lib ORDER BY event, wk LIMIT 300

-- @@ q3_weekly_active
SELECT <tydzień> AS wk, count(DISTINCT person_id) AS active_app_users,
  count(DISTINCT if(NOT (<iOS TF>), person_id, NULL)) AS active_non_tf,
  count(DISTINCT if(properties.$os = 'Android', person_id, NULL)) AS android,
  count(DISTINCT if(properties.$os IN ('iOS','iPadOS'), person_id, NULL)) AS ios
FROM events WHERE timestamp >= toDateTime('2026-09-19 00:00:00') AND properties.$lib = 'posthog-flutter' AND <filtry>
GROUP BY wk ORDER BY wk

-- @@ q4_new_users_weekly
SELECT <tydzień po first_ts> AS wk, count() AS new_users, countIf(os = 'Android') AS android,
  countIf(os IN ('iOS','iPadOS')) AS ios, countIf(tf) AS ios_tf
FROM (SELECT person_id, min(timestamp) AS first_ts, argMin(properties.$os, timestamp) AS os, max(<iOS TF>) AS tf
      FROM events WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter' AND <filtry>
      GROUP BY person_id)
WHERE first_ts >= toDateTime('2026-09-19 00:00:00') GROUP BY wk ORDER BY wk

-- @@ q5_new_events_by_chan
SELECT event, multiIf(properties.$lib != 'posthog-flutter', 'backend', <kanał>) AS chan, count() AS c,
  count(DISTINCT person_id) AS users, min(timestamp) AS first_ts,
  arrayStringConcat(arraySort(groupUniqArray(toString(properties.$app_version))), ',') AS vers
FROM events WHERE timestamp >= toDateTime('2026-10-01 00:00:00') AND <filtry>
  AND (event LIKE 'first_week%' OR event LIKE 'today_card%' OR event LIKE 'side_card%' OR event LIKE 'voice_engine%'
       OR event LIKE 'voice_live%' OR event = 'voice_moderation_event' OR event LIKE 'quick_checkin%' OR event LIKE 'session_sheet%'
       OR event LIKE 'follow_up%' OR event LIKE 'art9%' OR event LIKE 'profiling_%' OR event LIKE 'fab_%' OR event = 'getting_started_card_tapped'
       OR event = 'after_card_progress_viewed' OR event LIKE 'checkin_%' OR event LIKE 'reminder_%' OR event LIKE 'rhythm_%'
       OR event = 'workspace_item_action' OR event IN ('trial_reminder_sheet_shown','trial_reminder_sheet_result','trial_bar_viewed',
       'first_capture_prompt_shown','user_fragments_merged','voice_delegation_attempted','prep_card_opened','character_card_viewed','workspace_opened'))
GROUP BY event, chan ORDER BY event, chan LIMIT 300

-- @@ q6_skew_top1
SELECT wk, event, sum(cnt) AS total, max(cnt) AS top1, count() AS users, round(max(cnt) / sum(cnt), 2) AS top1_share
FROM (SELECT <tydzień> AS wk, event, person_id, count() AS cnt FROM events
      WHERE timestamp >= toDateTime('2026-09-19 00:00:00')
        AND event IN ('subscription_purchase_completed','user_activated','subscription_purchase_started','subscription_purchase_failed',
                      'paywall_shown','subscription_screen_opened','reflect_mode_selected','voice_chat_started','reflect_session_started','onboarding_completed')
      GROUP BY wk, event, person_id)
GROUP BY wk, event ORDER BY event, wk LIMIT 100

-- @@ q7_breakdowns
SELECT <tydzień> AS wk, event,
  toString(multiIf(event = 'paywall_shown', properties.trigger_feature, event = 'post_onboarding_offer_result', properties.result,
          event = 'post_onboarding_offer_not_shown', properties.reason,
          event = 'first_conversation_started', concat(toString(properties.mode), '/', toString(properties.entry_point)),
          event = 'first_conversation_ended', concat(toString(properties.mode), '/', toString(properties.reason)),
          event = 'voice_chat_started', concat(toString(properties.entry_point), '/', coalesce(toString(properties.voice_engine), '-')), '')) AS val,
  count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp >= toDateTime('2026-09-19 00:00:00') AND properties.$lib = 'posthog-flutter' AND <filtry>
  AND event IN ('paywall_shown','post_onboarding_offer_result','post_onboarding_offer_not_shown','first_conversation_started','first_conversation_ended','voice_chat_started')
GROUP BY wk, event, val ORDER BY event, wk, users DESC LIMIT 200

-- @@ q8_first_conv_quality
SELECT multiIf(timestamp < toDateTime('2026-10-10'), 'W3_1003', 'W4_1010p') AS wk, count() AS ended, count(DISTINCT person_id) AS users,
  quantile(0.5)(toFloat(properties.duration_s)) AS med_duration_s, quantile(0.5)(toFloat(properties.user_turns)) AS med_user_turns,
  countIf(toString(properties.reached_open) IN ('true','1')) AS reached_open, countIf(toFloat(properties.user_turns) >= 1) AS with_user_turn
FROM events WHERE timestamp >= toDateTime('2026-10-03 00:00:00') AND event = 'first_conversation_ended'
  AND properties.$lib = 'posthog-flutter' AND coalesce(properties.$device_model, '') NOT IN ('OnePlus8Pro','Pixel 6 Pro')
GROUP BY wk ORDER BY wk

-- @@ q9_new_cohort_7d
SELECT <tydzień po f.first_ts> AS wk, count() AS new_users, countIf(f.first_ts < now() - INTERVAL 7 DAY) AS full_7d_window,
  countIf(p.onb >= f.first_ts AND p.onb < f.first_ts + INTERVAL 7 DAY) AS onboarded_7d,
  countIf(p.fcs >= f.first_ts AND p.fcs < f.first_ts + INTERVAL 7 DAY) AS first_conv_7d,
  countIf(p.vcs >= f.first_ts AND p.vcs < f.first_ts + INTERVAL 7 DAY) AS voice_any_7d,
  countIf(p.rss >= f.first_ts - INTERVAL 1 HOUR AND p.rss < f.first_ts + INTERVAL 7 DAY) AS reflect_session_7d,
  countIf(p.pws >= f.first_ts AND p.pws < f.first_ts + INTERVAL 7 DAY) AS paywall_7d,
  countIf(p.trl >= f.first_ts - INTERVAL 1 HOUR AND p.trl < f.first_ts + INTERVAL 7 DAY) AS trial_7d,
  countIf(p.buy >= f.first_ts - INTERVAL 1 HOUR AND p.buy < f.first_ts + INTERVAL 7 DAY) AS purchase_7d,
  countIf(p.ret >= toStartOfDay(f.first_ts) + INTERVAL 1 DAY AND p.ret < f.first_ts + INTERVAL 7 DAY) AS returned_d1_d7
FROM (SELECT person_id, min(timestamp) AS first_ts FROM events
      WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter' AND <filtry>
      GROUP BY person_id HAVING first_ts >= toDateTime('2026-09-19 00:00:00')) AS f
LEFT JOIN (SELECT person_id,
    minIf(timestamp, event = 'onboarding_completed') AS onb, minIf(timestamp, event = 'first_conversation_started') AS fcs,
    minIf(timestamp, event = 'voice_chat_started') AS vcs, minIf(timestamp, event = 'reflect_session_started') AS rss,
    minIf(timestamp, event = 'paywall_shown') AS pws, minIf(timestamp, event = 'trial_started') AS trl,
    minIf(timestamp, event = 'subscription_purchase_completed') AS buy, maxIf(timestamp, properties.$lib = 'posthog-flutter') AS ret
  FROM events WHERE timestamp >= toDateTime('2026-09-19 00:00:00')
    AND event IN ('onboarding_completed','first_conversation_started','voice_chat_started','reflect_session_started','paywall_shown',
                  'trial_started','subscription_purchase_completed','$screen','app_opened','tab_switched','$app_opened')
  GROUP BY person_id) AS p ON f.person_id = p.person_id
GROUP BY wk ORDER BY wk

-- @@ q10_first_conv_by_version
SELECT toString(properties.$app_version) AS ver, <kanał> AS chan, event, count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts
FROM events WHERE timestamp >= toDateTime('2026-10-03 00:00:00') AND properties.$lib = 'posthog-flutter'
  AND coalesce(properties.$device_model, '') NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  AND event IN ('first_conversation_started','post_onboarding_build_viewed','onboarding_completed')
GROUP BY ver, chan, event ORDER BY event, ver LIMIT 120
```

Uwaga do q9: `returned_d1_d7` liczy ostatnie zdarzenie z listy (`$screen`, `tab_switched` itd.), więc to przybliżenie powrotu w dniach 1-7, nie pełna retencja.
