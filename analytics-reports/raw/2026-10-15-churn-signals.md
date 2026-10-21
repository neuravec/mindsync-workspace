# Churn i sygnały przed odejściem: surowy ekstrakt PostHog

- **Data**: 2026-10-15 · **Agent**: posthog-data-extractor
- **Projekt**: PostHog EU 141170 · **Okno**: 2026-07-17 → 2026-10-15 (90 dni, UTC); kohorta pierwszego tygodnia czyta zdarzenia od 2026-06-01
- **Pytanie**: ilu użytkowników odchodzi tygodniowo, gdzie kończą, czym ich pierwszy tydzień różni się od zostających, i czy pushe re-engagement ich wskrzeszają.
- **Weryfikacja zdarzeń** (90d, zdarzenie → `$lib`, zdarzenia/osoby):
  - `moment.sent` posthog-python 37 018 / 2 012 (w tym `moment_type=RE_ENGAGEMENT` 288 / 151); `moment.opened` posthog-python 235 / 73
  - `notification_opened` flutter 142 / 31; `$push_notification_opened` flutter 7 / 5 (ostatnio 2026-09-28)
  - `api_error` posthog-python 15 107 / 234; `reflect_session_started` python 328 / 69; `reflect_message_sent` python 944 / 44
  - `paywall_shown` flutter 82 / 33; `subscription_purchase_completed` python 278 / 11 + flutter 74 / 9
  - `account_deleted` python 8 / 8 (ostatnio 2026-09-26); `account_deletion_started` flutter 13 / 6; `user_logged_out` flutter 76 / 18
  - **Brak w katalogu**: żadnego zdarzenia anulowania ani wygaśnięcia subskrypcji (`subscription_cancelled`, `subscription_expired`, `trial_ended` jako zdarzenie odejścia)

## Definicja churnu

- **Aktywność świadoma** = zdarzenie klienta: `$lib='posthog-flutter'`, bez TestFlight/emulatora, bez urządzeń botów (`OnePlus8Pro`, `Pixel 6 Pro`), bez zdarzeń systemowych `$*` (poza `$screen`) i bez `Application Backgrounded/Installed/Updated`. Zdarzenia backendu (pushe, joby, `moment.*`) nie liczą się jako aktywność.
- **Churn** = osoba z aktywnością w oknie 90d, której ostatnia aktywność była przed `now() - 14 dni` (przed ok. 2026-10-01). 14 dni, bo pushe re-engagement idą po 3 i 7 dniach i potem milkną, więc 14 dni ciszy to stan po wyczerpaniu ścieżki odzysku; przy medianie 1 aktywnego dnia w pierwszym tygodniu krótsze okno myliłoby rzadkich użytkowników z odchodzącymi.
- "Aktywny wcześniej": raportuję osobno osoby z 1 dniem aktywności (w większości nie przeszły logowania) i z 2+ dniami; kohorta pierwszego tygodnia jest ograniczona do osób, które doszły do `mainPage` (zalogowane).

## Wyniki

### 1. Skala

| miara | osoby |
|---|---|
| aktywni w 90d (klient, filtry) | 470 |
| churn (cisza >= 14 dni) | 324 (69%) |
| aktywni w ostatnich 14 dniach | 146 |
| churn: tylko 1 dzień aktywności | 251 |
| churn: 2+ dni aktywności | 73 |
| churn: 4+ dni aktywności | 24 |

### 1b. Churn tygodniowo (tydzień OSTATNIEJ aktywności; wejście w churn = +14 dni)

| tydzień | WAU | churn | 1 dzień | 2+ dni | % WAU |
|---|---|---|---|---|---|
| 2026-07-12 | 6 | 1 | 1 | 0 | n<5 (okno ucięte) |
| 2026-07-19 | 45 | 24 | 23 | 1 | 53.3 |
| 2026-07-26 | 49 | 33 | 27 | 6 | 67.3 |
| 2026-08-02 | 45 | 26 | 17 | 9 | 57.8 |
| 2026-08-09 | 51 | 31 | 25 | 6 | 60.8 |
| 2026-08-16 | 51 | 28 | 20 | 8 | 54.9 |
| 2026-08-23 | 34 | 14 | 10 | 4 | 41.2 |
| 2026-08-30 | 38 | 23 | 14 | 9 | 60.5 |
| 2026-09-06 | 42 | 21 | 17 | 4 | 50.0 |
| 2026-09-13 | 40 | 26 | 19 | 7 | 65.0 |
| 2026-09-20 | 61 | 45 | 35 | 10 | 73.8 |
| 2026-09-27 | 102 | 52 | 43 | 9 | 51.0 (częściowo obserwowalny) |
| 2026-10-04, 10-11 | 88, 43 | n/d | | | jeszcze nieobserwowalne |

### 2. Gdzie kończą (ostatnie 10 zdarzeń klienta przed ostatnią aktywnością)

Wszyscy churnujący (n=324), ostatnie zdarzenie: `screen:auth` 67, `screen:welcome` 49, `screen:splash` 47 (razem 163 = 50%: koniec przed zalogowaniem), `screen:mainPage` 24, `tab_switched` 13, `onboarding_step_viewed` 13, `app_install_attributed` 11, `timeline_viewed` 8, `character_card_viewed` 7, `screen:settings` 6, `reflect_ui_session_ended` 5.

Tylko zalogowani (doszli do `mainPage`):

| zdarzenie/ekran | ostatnie u churn | w ostatnich 10 u churn | w ostatnich 10 u aktywnych |
|---|---|---|---|
| screen:mainPage | 24 | 75 | 29 |
| tab_switched | 13 | 68 | 23 |
| timeline_viewed | 8 | 50 | 19 |
| first_capture_prompt_shown | n<5 | 35 | 21 |
| workspace_opened | n<5 | 31 | 13 |
| character_card_viewed | 7 | 28 | 10 |
| screen:settings | 6 | 13 | 0 |
| app_tour_step_viewed | n<5 | 12 | n<5 |
| reflect_ui_session_ended | 5 | 9 | n<5 |
| screen:afterTherapyFlow | n<5 | 9 | n<5 |
| debrief_started | 0 | 9 | n<5 |
| onboarding_completed / app_tour_completed | 0 | 7 / 7 | 0 / 0 |
| habit_tracker_viewed | n<5 | 6 | 16 |
| subscription_screen_opened / screen:subscription | 0 | 5 / 5 | n<5 |
| screen:account | n<5 | 4 | 0 |

`paywall_shown` nie pojawia się wśród ostatnich 10 zdarzeń ani jednej zalogowanej osoby z top 40; paywall nie jest punktem wyjścia.

Nieoczekiwany `api_error` (bez `is_expected=true`) w oknie 24h przed ostatnią aktywnością do 1h po niej: churn 104/324 (32%) vs aktywni 34/146 (23%). W całym 90d: churn 130/324 (40%) vs aktywni 59/146 (40%).

### 3. Pierwszy tydzień: odchodzący vs zostający

Kohorta: zalogowani, pierwsza aktywność 2026-07-17..2026-09-24 (pełne 7 dni + 14 dni obserwacji), n=91.

| miara (dni 0-6) | churn n=79 | zostający n=12 |
|---|---|---|
| średnio dni aktywnych | 1.53 | 2.75 |
| mediana dni aktywnych | 1.0 | 2.5 |
| onboarding_completed | 58 (73%) | 11 (92%) |
| sesja Reflect (`reflect_session_started`) | 27 (34%) | n<5 (17%) |
| wiadomość Reflect | 19 (24%) | n<5 |
| nawyk (created/toggled) | n<5 | n<5 |
| otwarte powiadomienie (`notification_opened`/`moment.opened`) | 27 (34%) | 5 (42%) |
| nieoczekiwany api_error | 71 (90%) | 12 (100%) |
| paywall_shown | n<5 | n<5 |
| limit hit | n<5 | 0 |
| zakup | n<5 | n<5 |
| first_conversation_started | 0 | 0 (funkcja od 2026-10-05, po kohorcie) |

### 4. Churn płatnych

Kupujący (klienckie `subscription_purchase_completed`, bez TestFlight) w 90d: 8 osób; 2 (n<5) w churnie wg definicji aktywności. Brak zdarzeń anulowania/wygaśnięcia, więc churnu przychodowego PostHog nie mierzy.

### 5. Usunięcia konta i wylogowania (tygodniowo, osoby)

| tydzień | account_deleted | deletion_started | user_logged_out |
|---|---|---|---|
| 07-19..08-02 | 0 | 0 | 6 łącznie |
| 08-09 | n<5 (2) | n<5 | n<5 |
| 08-16 | n<5 (2) | n<5 | 7 |
| 08-30 | 0 | n<5 | n<5 |
| 09-13 | n<5 (1) | n<5 | n<5 |
| 09-20 | n<5 (3) | n<5 | n<5 |
| 09-27..10-11 | 0 | 0 | 7 łącznie |

Razem 90d: 8 usunięć (ostatnie 2026-09-26), 18 osób z wylogowaniem. Wylogowanie jako ostatnie zdarzenie przed churnem: 2 osoby (n<5).

### 6. Pushe re-engagement (`moment.sent`, `moment_type=RE_ENGAGEMENT`)

| token | otwarty (moment_id w `moment.opened`) | wysłane | osoby | powrót <72h | powrót <7d | aktywność dni 8-21 |
|---|---|---|---|---|---|---|
| false | nie | 16 | 15 | n<5 (2) | n<5 (2) | n<5 (2) |
| true | nie | 201 | 125 | 5 | 6 | 5 |
| true | tak | 71 | 13 | n<5 (1) | n<5 (1) | n<5 (1) |

Łącznie: 288 wysyłek do 151 osób, powrót do aplikacji w 72h po 8 wysyłkach (2.8%).

## Zastrzeżenia

- Ingest od 2026-04-22; tutaj okno 90d nie sięga tak daleko, ale tydzień 2026-07-12 jest ucięty oknem.
- Churn w tygodniach od 2026-09-27 jest jeszcze niepełny (cisza 14 dni nie mogła minąć).
- 251/324 churnujących to osoby z jednym dniem aktywności, połowa kończy na splash/welcome/auth: to głównie odpływ przed rejestracją albo duplikaty osób (anonimowe person_id przed identify), nie odejście aktywnych użytkowników.
- Grupa zostających w kohorcie pierwszego tygodnia ma tylko n=12, różnice procentowe są kruche.
- `moment.opened` otwarte z 71 wysyłek należy do 13 osób; dopasowanie po `moment_id` i brak powrotu klienta po "otwarciu" wskazuje, że `moment.opened` może być rejestrowane po stronie backendu bez otwarcia aplikacji, do sprawdzenia (data-analytics).
- `api_error` jest emitowany tylko przez backend; nieoczekiwane błędy dotykają prawie wszystkich nowych użytkowników, więc nie różnicują grup.
- Brak zdarzeń anulowania/wygaśnięcia subskrypcji; prawda o płatnościach w Postgres `subscription_receipts` (database-administrator).
- Progi prywatności: grupy < 5 osób oznaczone n<5 (próg zlecającego).

## Zapytania

Filtr klienta `{C}` użyty we wszystkich:
```sql
properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true
  AND ifNull(properties.$device_model,'') NOT IN ('OnePlus8Pro','Pixel 6 Pro')
  AND (NOT startsWith(event,'$') OR event = '$screen')
  AND event NOT IN ('Application Backgrounded','Application Installed','Application Updated')
```
Nieoczekiwany błąd `{ERR}`: `event = 'api_error' AND toString(properties.is_expected) NOT IN ('true','True','1')`

```sql
-- totals
SELECT count() AS persons, countIf(last_ts < now() - INTERVAL 14 DAY) AS churned,
  countIf(last_ts >= now() - INTERVAL 14 DAY) AS active_last14,
  countIf(last_ts < now() - INTERVAL 14 DAY AND days = 1) AS churned_one_day,
  countIf(last_ts < now() - INTERVAL 14 DAY AND days >= 2) AS churned_multi_day,
  countIf(last_ts < now() - INTERVAL 14 DAY AND days >= 4) AS churned_4plus_days
FROM (SELECT person_id, max(timestamp) AS last_ts, count(DISTINCT toDate(timestamp)) AS days
  FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND {C} GROUP BY person_id)

-- weekly_churn
SELECT wk, wau, churned, one_day, multi_day, round(churned * 100.0 / wau, 1) AS churn_pct_of_wau FROM (
  SELECT toStartOfWeek(timestamp) AS wk, count(DISTINCT person_id) AS wau
  FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND {C} GROUP BY wk) w
LEFT JOIN (
  SELECT toStartOfWeek(last_ts) AS wk2, count() AS churned, countIf(days = 1) AS one_day, countIf(days >= 2) AS multi_day
  FROM (SELECT person_id, max(timestamp) AS last_ts, count(DISTINCT toDate(timestamp)) AS days
    FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND {C} GROUP BY person_id)
  WHERE last_ts < now() - INTERVAL 14 DAY GROUP BY wk2) c ON w.wk = c.wk2
ORDER BY wk

-- last10_events (wariant signed-in: dodatkowo okno countIf(screen mainPage) OVER (PARTITION BY person_id) > 0)
SELECT label, countIf(rn = 1 AND churned) AS churned_last_event, count(DISTINCT if(churned, person_id, NULL)) AS churned_in_last10,
  countIf(rn = 1 AND NOT churned) AS retained_last_event, count(DISTINCT if(NOT churned, person_id, NULL)) AS retained_in_last10
FROM (
  SELECT person_id, if(event = '$screen', concat('screen:', ifNull(properties.$screen_name,'?')), event) AS label,
    row_number() OVER (PARTITION BY person_id ORDER BY timestamp DESC) AS rn,
    max(timestamp) OVER (PARTITION BY person_id) < now() - INTERVAL 14 DAY AS churned
  FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND {C})
WHERE rn <= 10 GROUP BY label ORDER BY churned_in_last10 DESC LIMIT 45

-- error_before_last_activity
SELECT churned, count() AS persons, countIf(err24 > 0), countIf(errall > 0) FROM (
  SELECT person_id, max(if(is_c, timestamp, NULL)) < now() - INTERVAL 14 DAY AS churned,
    countIf(NOT is_c AND timestamp >= last_c - INTERVAL 1 DAY AND timestamp <= last_c + INTERVAL 1 HOUR) AS err24,
    countIf(NOT is_c) AS errall
  FROM (SELECT person_id, timestamp, ({C}) AS is_c,
      max(if(({C}), timestamp, NULL)) OVER (PARTITION BY person_id) AS last_c
    FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND (({C}) OR ({ERR})))
  GROUP BY person_id HAVING max(if(is_c, 1, 0)) = 1)
GROUP BY churned

-- first_week_compare (fragment; pełne liczniki jak w tabeli 3)
SELECT churned, count() AS n, avg(days_w1), quantile(0.5)(days_w1), countIf(onb > 0), countIf(rs > 0), countIf(nop > 0), countIf(err > 0), countIf(pw > 0) ...
FROM (
  SELECT person_id, max(if(is_c, timestamp, NULL)) < now() - INTERVAL 14 DAY AS churned,
    count(DISTINCT if(is_c AND w1, toDate(timestamp), NULL)) AS days_w1,
    countIf(w1 AND event = '$screen' AND properties.$screen_name = 'mainPage') AS main,
    countIf(w1 AND event = 'onboarding_completed') AS onb, countIf(w1 AND event = 'reflect_session_started') AS rs,
    countIf(w1 AND event IN ('notification_opened','moment.opened','$push_notification_opened')) AS nop,
    countIf(w1 AND {ERR}) AS err, countIf(w1 AND event = 'paywall_shown') AS pw, ..., min(first_c) AS fts
  FROM (SELECT person_id, event, timestamp, properties, ({C}) AS is_c,
      min(if(({C}), timestamp, NULL)) OVER (PARTITION BY person_id) AS first_c,
      timestamp >= first_c AND timestamp < first_c + INTERVAL 7 DAY AS w1
    FROM events WHERE timestamp > toDateTime('2026-06-01 00:00:00')
      AND (({C}) OR event IN ('reflect_session_started','reflect_message_sent','moment.opened','api_error','reflect_limit_hit','subscription_purchase_completed')))
  GROUP BY person_id HAVING fts >= toDateTime('2026-07-17 00:00:00') AND fts < now() - INTERVAL 21 DAY AND main > 0)
GROUP BY churned

-- reengagement_push
SELECT has_token, opened, count() AS sent, count(DISTINCT pid) AS users, countIf(ret72 > 0), countIf(ret7 > 0), countIf(stay > 0)
FROM (
  SELECT s.pid AS pid, s.mid AS mid, s.has_token AS has_token,
    s.mid IN (SELECT toString(properties.moment_id) FROM events WHERE event = 'moment.opened' AND timestamp > now() - INTERVAL 90 DAY) AS opened,
    countIf(c.ts > s.ts AND c.ts < s.ts + INTERVAL 72 HOUR) AS ret72,
    countIf(c.ts > s.ts AND c.ts < s.ts + INTERVAL 7 DAY) AS ret7,
    countIf(c.ts > s.ts + INTERVAL 7 DAY AND c.ts < s.ts + INTERVAL 21 DAY) AS stay
  FROM (SELECT person_id AS pid, toString(properties.moment_id) AS mid, toString(properties.has_token) AS has_token, timestamp AS ts FROM events
        WHERE event = 'moment.sent' AND properties.moment_type = 'RE_ENGAGEMENT' AND timestamp > now() - INTERVAL 90 DAY) s
  LEFT JOIN (SELECT person_id AS pid, timestamp AS ts FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND {C}) c ON c.pid = s.pid
  GROUP BY s.pid, s.mid, s.has_token, s.ts)
GROUP BY has_token, opened

-- deletions_logouts_weekly
SELECT toStartOfWeek(timestamp) AS wk, count(DISTINCT if(event = 'account_deleted', person_id, NULL)),
  count(DISTINCT if(event = 'account_deletion_started', person_id, NULL)), count(DISTINCT if(event = 'user_logged_out', person_id, NULL))
FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND event IN ('account_deleted','account_deletion_started','user_logged_out')
GROUP BY wk ORDER BY wk

-- paid_churn
SELECT churned, count() FROM (
  SELECT b.pid, max(c.ts) < now() - INTERVAL 14 DAY AS churned FROM
   (SELECT DISTINCT person_id AS pid FROM events WHERE event = 'subscription_purchase_completed' AND properties.$lib = 'posthog-flutter'
      AND properties.$is_testflight != true AND properties.$is_emulator != true AND timestamp > now() - INTERVAL 90 DAY) b
  LEFT JOIN (SELECT person_id AS pid, timestamp AS ts FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND {C}) c ON c.pid = b.pid
  GROUP BY b.pid) GROUP BY churned
```
