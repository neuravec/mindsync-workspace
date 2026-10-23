# First week 2.0.117: follow-up 404 przy aktywnym kroku rozmowy oraz błąd /first-week/steps na starym koncie

Data: 2026-10-22 (odczyt prod ok. 18:47 UTC). Autor: database-administrator. Tylko SELECT, połączenie w trybie `SET SESSION CHARACTERISTICS AS TRANSACTION READ ONLY` (sprawdzone `SHOW transaction_read_only = on`), dyno `--no-tty` zakończył się sam, brak pozostawionych one-off dynos.

Konta oznaczone A, B, C (bez UID i adresów email).

## Pytanie

1. Dlaczego Main (MC v3) pokazuje krok rozmowy (`talk`, CTA `follow_up`) jako aktywny, a `GET /api/v1/first-week/follow-up` zwraca `404 not_found`? Czy brakuje kotwicy?
2. Dlaczego `GET /api/v1/first-week/steps` dał błąd dla starego konta bez pierwszego tygodnia (C)?

## Granica prywatności tej analizy

Zgodnie z regułą agenta (audyty bezpieczeństwa 2026-10-11, H-1 i D-L1) NIE czytałem dla tych kont `first_week_plan_state`, `first_week_follow_ups`, wierszy `FIRST_WEEK_STEP` w `notification_moments`, `notification_logs`, tonu pierwszego tygodnia ani nie uruchamiałem dla nich silnika planu (`plan_engine`, `step_plan`, `resolve_follow_up`). Ton łagodny wynika z sygnału kryzysowego, więc odczyt planu per osoba może go ujawnić. Wnioski poniżej opierają się na zwykłych kolumnach (users, preferencje, rozmowy, wiadomości, zgody, debriefy, karty) oraz na kodzie. Dla dnia 0 to wystarcza do pełnego dowodu, bo gałąź dnia 0 w starym silniku nie zależy od tonu ani stanu planu.

## Zapytania (skrót)

```sql
SELECT created_at, first_week_started_at, first_conversation_claimed_at,
       <klasa domeny email: apple_private_relay | TEAM_DOMAIN | public_mailbox | other_domain>
FROM users WHERE id = :u;
SELECT time_zone FROM user_preferences WHERE user_id = :u;
SELECT onboarding_completed, created_at FROM user_therapy_context WHERE user_id = :u;
SELECT subscription_type, is_active, end_date FROM user_subscription WHERE user_id = :u;
SELECT consent_type, granted_at, withdrawn_at FROM consent_records WHERE user_id = :u;
SELECT conversation_type, status, entry_origin, seed_source, created_at, last_message_at,
       (liczba wiadomości USER), (pierwsza wiadomość USER)
FROM conversations WHERE user_id = :u AND (ostatnie 10 dni) LIMIT 40;
SELECT input_type, processing_status, created_at FROM session_debriefs / session_prep_cards
WHERE user_id = :u AND created_at >= now() - interval '3 days';
```

Typy kolumn na prodzie: `users.created_at`, `conversations.created_at` i `messages.created_at` to `timestamp without time zone` (naive UTC); `users.first_week_started_at`, `first_conversation_claimed_at`, `conversations.last_message_at`, `consent_records.*` to `timestamptz`; `user_subscription.end_date` to `date`.

## Wyniki

| | A | B | C |
|---|---|---|---|
| Platforma (od zlecającego) | iOS | Android | Android |
| users.created_at (naive UTC) | 21.10 16:18 | 21.10 22:27 | 02.07 01:37 |
| Kotwica `first_week_started_at` | 21.10 16:31 UTC (13 min po rejestracji) | 21.10 22:30 UTC (2,5 min po rejestracji) | NULL |
| `first_conversation_claimed_at` | 21.10 16:32 | 21.10 22:31 | NULL |
| Strefa w preferencjach | Europe/London (BST, UTC+1) | America/New_York (EDT, UTC-4) | America/Los_Angeles (PDT, UTC-7) |
| onboarding_completed | true | true | true (od 02.07) |
| Subskrypcja | PREMIUM aktywna, end_date 25.10 | PREMIUM aktywna, end_date 25.10 | PREMIUM aktywna, end_date 14.11 |
| Zgody | ART9 od 21.10 16:21; PROFILING od 22.10 07:44 | ART9 od 21.10 22:28; brak PROFILING | ART9 od 02.07; PROFILING od 10.07 (dwa wiersze, ten sam moment) |
| Domena email | Apple private relay (nie da się stwierdzić, czy to ktoś z zespołu; brak domeny zespołu) | publiczna skrzynka | publiczna skrzynka |
| Rozmowy łącznie | 1 Reflect, FINISHED | 1 Reflect, FINISHED | 6 Reflect: 5 ACTIVE, 1 FINISHED |
| Wątek pierwszej rozmowy (`entry_origin = onboarding_first_conversation`) | tak, 6 wiadomości użytkownika, start 16:32, koniec 16:42 (dzień 0) | tak, 5 wiadomości użytkownika, start 22:31, koniec 22:41 (dzień 0) | brak |
| Inne wątki Reflect od kotwicy | 0 | 0 | nie dotyczy (ostatni wątek 14.10, `seed_source = between_session`, ACTIVE) |
| Wątek z `seed_source = first_week_followup` | 0 | 0 | 0 |
| Debriefy, ostatnie 3 dni | 2 (TEXT, COMPLETED: 21.10 16:50 i 22.10 10:44) | 0 | 1 (TEXT, COMPLETED, 21.10 23:18) |
| Prep cards, ostatnie 3 dni | 1 (AUTO, COMPLETED, 21.10 16:43) | 0 | 1 (AUTO, COMPLETED, 20.10 21:30) |

Dzień planu (granica dnia 04:00 czasu lokalnego, `plan_engine.plan_date_of`):

| Konto | Data planu kotwicy | Dzień 1 zaczyna się | Teraz (22.10 18:47 UTC) | W chwili błędu |
|---|---|---|---|---|
| A | 21.10 (17:31 lokalnie) | 22.10 03:00 UTC | dzień 1 | 404 zgłoszone w dniu 0 i w dniu 1 |
| B | 21.10 (18:30 lokalnie) | 22.10 08:00 UTC | dzień 1 | ok. 00:10 UTC 22.10 = 20:10 lokalnie 21.10, dzień 0 |
| C | brak kotwicy | | | 21.10 09:13 UTC = 02:13 lokalnie; 21.10 23:24 UTC = 16:24 lokalnie (6 min po utworzeniu debriefu) |

Kontekst zbiorczy: 13 kont dostało kotwicę w ostatnich 7 dniach; w ostatnich 30 dniach 37 rozmów ma `entry_origin = onboarding_first_conversation`.

## Interpretacja

### 1. Follow-up 404: kotwica JEST, nie zgadza się warunek "dzisiejszej karty"

Hipoteza "brak kotwicy" jest fałszywa: A i B mają `users.first_week_started_at` zapisane kilka minut po rejestracji, przed startem pierwszej rozmowy (tak jak zakłada `anchor.py`). `404 not_found` z follow-upu ma dwie przyczyny w kodzie i to jest ta druga.

Dwa resolvery liczą krok rozmowy z różnych źródeł:

* `GET /first-week/steps` (`step_service.load_steps` + `step_plan.cta_for`): krok `talk` ma CTA `follow_up`, gdy `has_first_talk` jest prawdą (wątek `onboarding_first_conversation` ma co najmniej jedną wiadomość użytkownika), i jest niewykonany, dopóki od kotwicy nie ma wątku Reflect innego niż pierwsza rozmowa. Plan kroków nie zna dni. Dla A i B oba fakty są spełnione od 16:35 i 22:38 UTC w dniu 0: pierwsza rozmowa z wiadomościami jest, innych wątków Reflect brak. Main pokazuje więc krok rozmowy otwarty z przyciskiem follow-up już w dniu 0.
* `GET /first-week/follow-up` (`follow_up.resolve_follow_up`, wersja wdrożona): zwraca pytanie tylko wtedy, gdy `todays_talk_step` zwraca `talk`/`talk2`, czyli gdy karta Today STAREGO silnika (`plan_engine.build_plan`) ma `state == "today"` i `step in (talk, talk2)`. W przeciwnym razie `None`, czyli 404.

Konkretny warunek: w `plan_engine.build_plan` gałąź `if today == 0:` tworzy kartę `TodayCard(state=TODAY_STATE_DAY0, step=None)` bezwarunkowo. W dniu 0 `todays_talk_step` zwraca więc `None` (`today.state != TODAY_STATE_TODAY`), a resolver zwraca 404, choć plan kroków już oferuje follow-up. Dla B (błąd w dniu 0) i dla pierwszego błędu A (dzień 0) to jest pełne wyjaśnienie, zależne wyłącznie od kotwicy i strefy czasowej, które sprawdziłem w danych.

Drugi błąd A (dzień 1): w starym silniku krok `talk` leży w dniu 1 tylko w wariantach B/C; w wariancie A (osoba w terapii z harmonogramem, przy aktywnej zgodzie ART9) dzień 1 może zająć krok `after`/`prep` z wyższym priorytetem albo krok rozmowy może mieć stan inny niż `today` (`deferred`, `done`). Wtedy karta Today nie jest rozmową i znowu jest 404. Którą gałąź trafiło A, nie ustalałem, bo wymagałoby to odtworzenia planu tej osoby (patrz granica prywatności). Ograniczenie limitem (`quota_out`) jest mało prawdopodobne, bo A ma aktywny PREMIUM. Niezależnie od gałęzi warunek po stronie planu kroków był w dniu 1 dalej spełniony (zero wątków Reflect poza pierwszą rozmową), więc rozjazd jest ten sam.

Uwaga dla `backend-api`: kopia robocza `app/services/first_week/follow_up.py` (niezacommitowana, "fix 2026-10-22") dodaje fallback `steps_offer_follow_up`: gdy stary silnik nie daje rozmowy, a plan kroków pokazuje `talk` niewykonany z CTA `follow_up`, endpoint zwraca pytanie ogólne (`quoted: false`). Dla danych A i B (pierwsza rozmowa z wiadomościami, brak innych wątków Reflect, kotwica obecna) ten fallback zwróciłby 200 zarówno w dniu 0, jak i w dniu 1. Dane z produ potwierdzają, że poprawka trafia w faktyczną przyczynę. Do rozważenia: ścieżka voice `resolve_thread_opening` wywołuje `resolve_follow_up` bez `steps_reader`, więc korzysta z domyślnego czytnika i dostanie ten sam fallback (OK); pytanie cytowane nadal tylko w dniu kroku `talk` starego silnika.

### 2. /first-week/steps dla C: dane prowadzą do 204, nie do błędu

C ma `first_week_started_at = NULL` (konto z 02.07, przed wydaniem pierwszego tygodnia, bez `first_conversation_claimed_at`). `get_first_week_anchor` zwraca wtedy `None`, `load_steps` zwraca `NO_ANCHOR`, endpoint odpowiada `204` bez treści. Klient 2.0.117 obsługuje 204 poprawnie (`DioClient.getMapWithStatus` zwraca `data: null` dla pustej odpowiedzi, `FirstWeekManager.getSteps` zwraca `null`, `McWeekCubit` przechodzi w `McWeekStatus.none`); ta obsługa jest w repo od 08.10, więc jest w buildzie 2.0.117.

Wniosek: z danych w bazie nie wynika żaden błąd pierwszego tygodnia dla C. Odpowiedź inna niż 204 i inna niż 503 musiała powstać przed logiką endpointu albo poza nim: `401` z `deps.get_current_user` (przeterminowany token po wznowieniu aplikacji), timeout klienta (`planTimeout` = 6 s) albo brak sieci. Pierwszy błąd przypada na 02:13 czasu lokalnego C, drugi 6 minut po tym, jak C utworzył debrief (aplikacja była aktywna i zalogowana chwilę wcześniej), co pasuje do wzorca "stary token na wznowieniu". W kopii roboczej frontu (`lib/api/dio_client.dart`, niezacommitowane) jest właśnie dodawane ponowienie po 401 z odświeżonym tokenem ("three requests 401'd in the same second on iOS"). Rozstrzygnięcie daje właściwość `http_status` / `failure_reason` zdarzenia błędu w PostHog dla tych dwóch chwil (zadanie dla `posthog-data-extractor`); logi Heroku z 21.10 już wypadły z bufora.

## Poziom pewności

* Kotwica obecna u A i B, brak u C: pewne (odczyt bezpośredni).
* Przyczyna 404 w dniu 0 (A, B): wysoka. Gałąź `today == 0` jest bezwarunkowa, a dzień 0 wynika z kotwicy i strefy.
* Przyczyna 404 w dniu 1 (A): średnia co do konkretnej gałęzi starego silnika (celowo nieodtwarzanej), wysoka co do samego rozjazdu z planem kroków.
* C: wysoka, że serwer z tymi danymi daje 204; średnia, że błąd to 401 na wznowieniu (potrzebne potwierdzenie z PostHog).

## Przekazania

* `backend-api`: fallback `steps_offer_follow_up` w kopii roboczej pasuje do danych; dodać test dnia 0 (karta `day0`, pierwsza rozmowa z wiadomościami, zero innych wątków Reflect, oczekiwane 200 z `quoted: false`). Bez migracji.
* `flutter-mobile`: ponowienie po 401 w `dio_client.dart` obejmie też `/first-week/steps` (GET, bez FormData). Warto upewnić się, że `firstWeekPlanFailed` zachowuje `http_status`, żeby kolejny taki przypadek dało się rozpoznać bez bazy.
* `posthog-data-extractor`: `http_status` i `failure_reason` zdarzeń błędu `/first-week/steps` dla konta C o 21.10 09:13:05 i 23:24:16 UTC.

Nie zmieniłem żadnych danych ani kodu.
