# Użycie funkcji i ścieżka głosowa (30 dni) - raw PostHog extract

- **Date**: 2026-10-15 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: 2026-09-15 -> 2026-10-15 (now() - 30 DAY, UTC); trend: ostatnie 15 dni vs poprzednie 15 dni
- **Question**: zasięg i częstotliwość głównych funkcji wśród aktywnych w 30 dniach, jakość ścieżki głosowej, pierwsze dane GPT-Live-1, otwarcia powiadomień wg typu, funkcje martwe i rosnące.
- **Event verification**: katalog `event_definitions` pobrany 2026-10-15 (289 zdarzeń). Wszystkie użyte zdarzenia mają `last_seen_at` 2026-10-14 lub 2026-10-15, poza `voice_session_failed` (ostatnio 2026-10-07), `first_conversation_connection_lost`/`_start_failed` (2026-10-05). Nowe od 2026-10-15: `voice_engine_selected` (backend), `voice_engine_changed` (klient), `voice_live_session_ended` (backend). Brak jakiegokolwiek zdarzenia `todo_*`.

## Baza aktywnych

Aktywny = >= 1 zdarzenie `posthog-flutter`, bez `$is_testflight`, `$is_emulator`, `$device_model IN ('OnePlus8Pro','Pixel 6 Pro')`.

| okno | aktywni |
|---|---|
| 30 dni | 257 (Android 234, iOS 19, iPadOS 4) |
| ostatnie 15 dni | 161 |
| poprzednie 15 dni | 121 |

Baza urosła o ok. 33% między połówkami, więc wzrost funkcji trzeba porównywać z tym tempem.

## 1. Zasięg funkcji (aktywni, 30 dni)

| funkcja | zdarzenia definiujące | użytk. 30d | % z 257 | zdarzeń | zdarz./użytk. | ost. 15d | poprz. 15d |
|---|---|---|---|---|---|---|---|
| Timeline / Trends | `timeline_viewed` | 62 | 24.1% | 1216 | 19.6 | 42 | 33 |
| Habit Tracker (dowolne) | `habit_tracker_viewed`, `habit_created`, `habit_check_toggled` | 52 | 20.2% | 1067 | 20.5 | 38 | 24 |
| Workspace | `workspace_opened`, `workspace_item_action` | 43 | 16.7% | 737 | 17.1 | 28 | 24 |
| Personal Bio | `bio_viewed` | 40 | 15.6% | 486 | 12.2 | 26 | 24 |
| Debrief | `debrief_started`, `debrief_created` | 23 | 8.9% | 56 | 2.4 | 17 | 11 |
| Reflect tekst (wiadomości) | `reflect_message_submitted` | 22 | 8.6% | 912 | 41.5 | 19 | 9 |
| Reflect wybór trybu | `reflect_mode_choice_shown`, `reflect_mode_selected` | 21 | 8.2% | 355 | 16.9 | 13 | 14 |
| Threads | `reflect_thread_opened`, `_resumed`, `_preview_opened` | 20 | 7.8% | 293 | 14.6 | 13 | 13 |
| Pierwsza rozmowa (onboarding) | `first_conversation_started` | 19 | 7.4% | 33 | 1.7 | 19 | 0 |
| Rozmowa głosowa realtime | `voice_chat_started` | 16 | 6.2% | 72 | 4.5 | 12 | 8 |
| Otwarcie powiadomienia (klient) | `notification_opened` | 14 | 5.4% | 50 | 3.6 | 7 | 10 |
| Podsumowania | `summary_viewed` | 13 | 5.1% | 108 | 8.3 | 10 | 8 |
| Before therapy (prep) | `prep_card_opened/_created/_started`, `prep_capture_submitted` | 13 | 5.1% | 44 | 3.4 | 10 | 5 |
| Notatka głosowa | `recording_started` flow=`voice_note` | 10 | 3.9% | 38 | 3.8 | 6 | 9 |
| Quick capture | `quick_capture_submitted` | 8 | 3.1% | 18 | 2.2 | n<5 | 5 |
| Nagrywanie sesji terapii | `recording_started` flow=`session_recording` | 8 | 3.1% | 15 | 1.9 | 6 | 6 |
| Your Session | `session_sheet_completed`, `therapy_schedule_updated` | 6 | 2.3% | 122 | 20.3 | n<5 | n<5 |
| Character (nowy arkusz, od 14.10) | `character_sheet_viewed`, `skill_opened`, `stat_opened`, `character_tool_opened`, `star_opened` | n<5 | <2% | 162 | - | n<5 | 0 |
| Orca memory | `orca_memory_viewed` | n<5 | <2% | 15 | - | n<5 | 0 |
| Today card (tap) | `today_card_tapped` | n<5 | <2% | 3 | - | n<5 | 0 |
| To-do | `workspace_item_action` section=`todo` | n<5 | <2% | 3 | - | - | - |

Rozbicie Habit Tracker (30d, bez TF/emulatora): `habit_tracker_viewed` 55 osób / 782 zdarzeń, `habit_created` 12 / 13, `habit_check_toggled` 10 / 107, `habit_limit_reached` n<5. Realnie używa (tworzy albo odhacza) ok. 10-12 osób; 55 to wyświetlenia.

## 2. Ścieżka głosowa

Rozmowa realtime, klient, bez TF/emulatora, 30d:

| platforma | użytk. ze startem | `voice_chat_started` | `voice_chat_ended` | `voice_session_failed` |
|---|---|---|---|---|
| Android | 13 | 44 | 47 | 2 |
| iOS | n<5 | 3 | 4 | 0 |

Czas trwania (`voice_chat_ended.duration_seconds`, 51 sesji, 14 osób): mediana 127 s, p90 499 s.

| koszyk | sesje | `end_drain_timed_out` |
|---|---|---|
| < 30 s | 13 | 1 |
| 30 s - 2 min | 11 | 1 |
| 2 - 5 min | 14 | 0 |
| 5 - 15 min | 11 | 4 |
| 15 min + | 2 | 0 |

`transcription_failed_count` = 0 we wszystkich sesjach, gdzie pole jest (42 z 81 zdarzeń 30d; starsze buildy go nie mają).

Wejście (`voice_chat_started.entry_point`): `mode_choice` 20 / 9 osób, `onboarding_first_conversation` 12 / 9, `reflect_continuation` 11 / 5, null 4 / n<5.

Błędy (30d, bez filtra TF): `voice_session_failed` 4 zdarzenia / n<5 osób (connect `webrtc_failure` iOS 2, Android 1; dropped `ice_failed` Android 1); `first_conversation_connection_lost` 1, `first_conversation_start_failed` 1. Ok. 5% startów kończy się błędem. Ostatni `voice_session_failed` 2026-10-07.

Mikrofon (`mic_permission_result`, tylko źródło `first_conversation`): granted 26 (Android 15 / 9 osób, iOS 11 / n<5), denied 3, permanently_denied 1 (wszystkie Android, n<5).

Pierwsza rozmowa (`first_conversation_ended`, 30d): voice 19 zakończeń, 19 z co najmniej jedną wypowiedzią użytkownika, średnio ok. 330 s; text 9 zakończeń, 4 z wypowiedzią. `reached_open` voice 10/10 w filtrowanej próbie, text 3/7.

Reflect wybór trybu (`reflect_mode_selected`): voice+premium 54 / 10 osób, text+premium 52 / 12, text bez premium 30 / n<5, voice bez premium (zablokowane) 28 / n<5.

`reflect_ui_session_ended.end_reason`: navigated_away 99 / 15, backgrounded 57 / 11, user_ended 8 / n<5, thread_switched 6 / n<5, limit_reached 2 / n<5, voice_interrupted 1 / n<5 (pierwsze wystąpienie tego powodu).

## 3. GPT-Live-1 (od 2026-10-15)

| zdarzenie | lib | dzień | wartość | zdarz. | osoby |
|---|---|---|---|---|---|
| `voice_engine_selected` | posthog-python | 10-15 | engine=live, session_kind=reflect, reason=client_live_request | 2 | n<5 (1) |
| `voice_engine_changed` | posthog-flutter, TestFlight | 10-15 | engine=live | 1 | n<5 (1) |
| `voice_chat_started` z `voice_engine` | posthog-flutter, TestFlight | 10-15 | live | 2 | n<5 (1) |
| `voice_chat_ended` z `voice_engine` | posthog-flutter, TestFlight | 10-15 | live, close_requested | 3 | n<5 (1) |
| `voice_live_session_ended` | posthog-python | 10-15 | model=gpt-live-1, close_requested | 2 | n<5 (1) |

Zdarzenia płyną po obu stronach, ale to jedna osoba na TestFlight (test wewnętrzny). Classic z `voice_engine=classic`: 0 zdarzeń. Porównania silników nie da się zrobić.

## 4. Powiadomienia: otwarcia wg typu momentu

Klient (`notification_opened.moment_type`, 30d, 50 zdarzeń / 14 osób): WEEKLY_SUMMARY_READY 10 / 5, brak typu 8 / 6, pozostałe typy po n<5 (RECORD_SESSION, GOALS_WEEKLY, THERAPY_PREP, THERAPY_APPOINTMENT, MONTHLY_SUMMARY_READY, POST_SESSION_REFLECTION, RE_ENGAGEMENT, HOMEWORK_REMINDER, THERAPY_RELATIONSHIP_CHECKIN, ADD_THERAPY_DATE, MOOD_UPDATE_REQUEST, REFLECTION_INVITATION).

Backend (`moment.sent` 31d vs `moment.opened` 30d przez `moment_id`):

| moment_type | wysłane | odbiorcy | otwarte (dopasowane) |
|---|---|---|---|
| WEEKLY_SUMMARY_READY | 5204 | 1831 | 6 |
| MONTHLY_SUMMARY_READY | 1738 | 1738 | 1 |
| RE_ENGAGEMENT | 166 | 95 | 1 |
| REFLECTION_INVITATION | 82 | 60 | 0 |
| THERAPY_RELATIONSHIP_CHECKIN | 77 | 57 | 0 |
| THERAPY_APPOINTMENT | 43 | 15 | 0 |
| THERAPY_PREP | 21 | 11 | 0 |
| GOALS_WEEKLY | 17 | 11 | 0 |
| MOOD_UPDATE_REQUEST | 12 | 11 | 2 |
| ADD_THERAPY_DATE | 10 | 10 | 0 |
| ACCOUNT_SETUP_NUDGE | 10 | 8 | 0 |
| inne | po 1-5 | - | 0 |

`moment.opened` łącznie: 62 zdarzenia / 24 osoby, ale tylko 10 łączy się z `moment.sent` przez `moment_id`. Populacja odbiorców (ok. 1800) to cała baza kont, nie aktywni.

## Caveats

- Ingest od 2026-04-22, okno 30d nie jest obcięte.
- `reflect_message_sent`, `reflect_session_*`, `moment.*`, `voice_engine_selected`, `voice_live_session_ended` to zdarzenia backendu (`posthog-python`); w zasięgu użyto klientowych odpowiedników.
- Skew (najaktywniejsza osoba / suma, 30d, klient): `therapy_schedule_updated` 107/122, `stat_opened` 63/80, `bio_viewed` 303/490, `summary_viewed` 67/112, `character_sheet_viewed` 19/32, `habit_check_toggled` 51/114, `workspace_opened` 276/726, `timeline_viewed` 420/1243. Liczby osób są wiarygodne, liczby zdarzeń dla tych funkcji nie.
- `voice_chat_ended` (51) > `voice_chat_started` (47) w filtrowanej próbie: część sesji nie emituje startu albo koniec emituje się podwójnie.
- `habit_tracker_viewed` i `character_card_viewed` wyglądają na zdarzenia ładowania, nie świadomego otwarcia.
- Próg prywatności z briefu: grupy < 5 osób oznaczone n<5.

## Queries

```sql
-- active_base
SELECT count(DISTINCT person_id) AS active_30d,
  count(DISTINCT if(timestamp > now() - INTERVAL 15 DAY, person_id, NULL)) AS active_last15,
  count(DISTINCT if(timestamp <= now() - INTERVAL 15 DAY, person_id, NULL)) AS active_prior15
FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib = 'posthog-flutter'
  AND properties.$is_testflight != true AND properties.$is_emulator != true
  AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')

-- feature_reach (skrót: multiIf mapuje zdarzenie -> funkcja, patrz tabela 1)
WITH act AS (SELECT person_id FROM events WHERE <okno 30d + filtry jak wyżej> GROUP BY person_id),
fe AS (SELECT person_id, timestamp, multiIf(event='voice_chat_started','voice_realtime', ..., '') AS f
  FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib='posthog-flutter'
  AND event IN (...) AND person_id IN (SELECT person_id FROM act))
SELECT f, count(DISTINCT person_id) users_30d, count() events_30d,
  count(DISTINCT if(timestamp > now() - INTERVAL 15 DAY, person_id, NULL)) users_last15,
  count(DISTINCT if(timestamp <= now() - INTERVAL 15 DAY, person_id, NULL)) users_prior15
FROM fe WHERE f != '' GROUP BY f ORDER BY users_30d DESC LIMIT 40

-- voice_funnel_by_os
SELECT os, count() persons, countIf(started>0) started_u, sum(started), sum(ended), sum(failed) FROM (
  SELECT person_id, any(properties.$os) os, countIf(event='voice_chat_started') started,
    countIf(event='voice_chat_ended') ended, countIf(event='voice_session_failed') failed
  FROM events WHERE timestamp > now() - INTERVAL 30 DAY AND properties.$lib='posthog-flutter'
    AND properties.$is_testflight != true AND properties.$is_emulator != true
    AND event IN ('voice_chat_started','voice_chat_ended','voice_session_failed') GROUP BY person_id) GROUP BY os

-- voice_duration_median
SELECT quantile(0.5)(toFloat(properties.duration_seconds)), quantile(0.9)(toFloat(properties.duration_seconds)), count(), count(DISTINCT person_id)
FROM events WHERE event='voice_chat_ended' AND timestamp > now() - INTERVAL 30 DAY AND properties.$lib='posthog-flutter'
  AND properties.$is_testflight != true AND properties.$is_emulator != true

-- engine_events_raw
SELECT event, toDate(timestamp) d, properties.engine, properties.voice_engine, properties.model, properties.session_kind,
  properties.reason, properties.close_reason, properties.$lib, properties.$is_testflight, count(), count(DISTINCT person_id)
FROM events WHERE timestamp > now() - INTERVAL 7 DAY AND (event IN ('voice_engine_selected','voice_engine_changed','voice_live_session_ended')
  OR (event IN ('voice_chat_started','voice_chat_ended') AND JSONHas(properties,'voice_engine')))
GROUP BY 1,2,3,4,5,6,7,8,9,10 LIMIT 40

-- moment_sent_vs_opened_by_type
WITH s AS (SELECT toString(properties.moment_id) mid, any(toString(properties.moment_type)) mt, any(person_id) pid FROM events
  WHERE event='moment.sent' AND timestamp > now() - INTERVAL 31 DAY GROUP BY mid),
o AS (SELECT DISTINCT toString(properties.moment_id) mid FROM events WHERE event='moment.opened' AND timestamp > now() - INTERVAL 30 DAY)
SELECT s.mt, count() sent, count(DISTINCT s.pid) recipients, countIf(o.mid = s.mid) opened
FROM s LEFT JOIN o ON s.mid = o.mid GROUP BY s.mt ORDER BY sent DESC LIMIT 20

-- skew_sweep
SELECT event, sum(cnt) total, max(cnt) top1, count() users FROM (
  SELECT event, person_id, count() cnt FROM events WHERE timestamp > now() - INTERVAL 30 DAY
    AND properties.$lib='posthog-flutter' AND event IN (...) GROUP BY event, person_id)
GROUP BY event ORDER BY top1*1.0/total DESC LIMIT 20
```

Pełne pliki zapytań (q1-q5) były w scratchpadzie sesji; pozostałe sekcje (koszyki czasu, entry_point, błędy, mikrofon, first_conversation, reflect_mode_selected, end_reason, notification_opened wg moment_type, workspace sections, habit split) to proste `GROUP BY` po wymienionych właściwościach z tym samym oknem i filtrami.
