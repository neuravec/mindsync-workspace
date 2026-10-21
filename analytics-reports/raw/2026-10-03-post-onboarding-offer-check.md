# Oferta po onboardingu (starter / Annual / Monthly): czy się pokazuje. Raw PostHog extract

- **Date**: 2026-10-03 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: 2026-10-01 00:00 UTC do 2026-10-03 ok. 14:22 UTC (ostatnie zdarzenie w oknie); zapytania o "pierwsze wystąpienie" od 2026-09-01, historia osób od 2026-04-22 (start ingestu)
- **Question**: Ilu kończących onboarding zobaczyło ofertę po onboardingu na nowych buildach, a jeśli nikt, to dlaczego (powód, błąd ładowania, konta testowe)?
- **Filtr**: zdarzenia klienckie `properties.$lib = 'posthog-flutter'` (wyjątek: `post_onboarding_offer_not_shown` i `paywall_load_failed` liczone bez filtra `$lib`, oba są wyłącznie klienckie; `user_registered` i `trial_started` są backendowe, `posthog-python`)

## Jak oferta jest zinstrumentowana (z kodu, `mindsync_app/lib`)

| Fakt | Zdarzenie | Gdzie |
|---|---|---|
| Koniec onboardingu | `onboarding_completed` (props `total_duration_seconds`, `total_steps`) | `therapy_onboarding_cubit.dart` `_markOnboardingComplete` |
| Oferta pokazana | **brak osobnego zdarzenia `post_onboarding_offer_shown`**. Pokazanie = `paywall_shown` z `trigger_feature = post_onboarding` (odroczone do `revealPaywall()`, gdy ekran oferty jest na ekranie) | `wow_screen.dart` + `subscription_cubit.dart` |
| Oferta pominięta | `post_onboarding_offer_not_shown` z `reason` in {`not_just_onboarded`, `status_unavailable`, `already_premium`, `no_active_trial`, `already_seen`, `products_unavailable`} | `wow_cubit.dart` `_offerSkipReason` |
| Wybór opcji / wynik | `post_onboarding_offer_option_selected` (`option`), `post_onboarding_offer_result` (`result`, `skip_method`, `option_selected`, `dwell_ms`) | `wow_cubit.dart` |
| Produkty sklepu nie załadowały się | `paywall_load_failed` (`error_type` = `e.runtimeType`, `trigger_feature`) | `subscription_cubit.dart` `loadSubscriptionsProducts` |

Uwaga z kodu: `already_premium` = `subscriptionIsActive` ORAZ `premium_source` in {`null`, `purchase`, `starter_pack`}. Świeże konto z 4-dniowym trialem ma `signup_trial` i NIE wpada w `already_premium`.

## Event verification

| Zdarzenie | W event_definitions? | first seen | last seen | Okno 10-01..10-03 |
|---|---|---|---|---|
| `onboarding_completed` | tak | 2026-04-22 | 2026-10-03 09:27 | 7 zdarzeń / 7 osób |
| `post_onboarding_offer_not_shown` | tak | 2026-10-03 07:52 | 2026-10-03 10:22 | 2 / 2 |
| `paywall_shown` z `trigger_feature=post_onboarding` | `paywall_shown` tak, wartość `post_onboarding` **nigdy** (od 09-01) | brak | brak | 0 / 0 |
| `subscription_screen_opened` z `trigger_feature=post_onboarding` | nigdy | brak | brak | 0 / 0 |
| `post_onboarding_offer_option_selected` | **nie istnieje** (nigdy nie wystrzelił) | brak | brak | 0 |
| `post_onboarding_offer_result` | **nie istnieje** (nigdy nie wystrzelił) | brak | brak | 0 |
| `paywall_load_failed` | tak | 2026-10-03 10:13 | 2026-10-03 11:26 | 6 / 1 |
| `post_onboarding_build_viewed`, `personal_reveal_viewed`, `personal_reveal_cta_tapped` | tak | 2026-10-03 07:51-07:53 | 2026-10-03 10:21 | po 2 / 2 |

## Results

### 1. Które buildy mają nowy onboarding (pierwsze wystąpienie per wersja)

Commit FE `02f8d0b` = 2026-10-03 07:17 UTC. Pierwszy bump wersji po nim (`a52607b`, 07:21 UTC) = **2.0.97**. Wersja 2.0.96 (bump 2026-10-02 05:09 UTC) jest sprzed commita i nie wysyła żadnego nowego zdarzenia.

| `$app_version` | iOS build / Android build | pierwsze zdarzenie w PostHog | osób w oknie (iOS / Android) | nowe zdarzenia przepływu? |
|---|---|---|---|---|
| 2.0.94 | 162 / 165 | 10-01 00:37 | 6 (+1 iPadOS) / 25 | nie (stary WOW bez oferty) |
| 2.0.95 | brak / 166 | 10-01 10:00 | 0 / 22 | nie |
| 2.0.96 | brak / 167 | 10-02 05:27 | 0 / 2 | nie |
| **2.0.97** | 164 / 168 | 10-03 07:39 | 1 / 3 | **tak**: `usage_snapshot` 07:40, `post_onboarding_build_viewed` iOS 07:51 / Android 10:20, `post_onboarding_offer_not_shown` iOS 07:52 / Android 10:21 |
| **2.0.98** | 165 / 169 | 10-03 10:05 | 1 / 1 | tak (`usage_snapshot`; `paywall_load_failed` Android 10:12) |
| **2.0.99** | 166 / 170 | 10-03 11:19 | 1 / 1 | tak (`usage_snapshot`, `premium_welcome_viewed`; `paywall_load_failed` Android 11:24) |
| **2.0.100** | 167 / 171 | 10-03 12:00 | 3 / 3 | tak (`usage_snapshot`, `premium_welcome_viewed`) |

Nowe buildy (2.0.97-2.0.100) łącznie: **7 osób**, wszystkie sklasyfikowane niżej (pkt 3). Produkcyjny ruch (Android 2.0.94/2.0.95, iOS 2.0.94) jest na buildach bez oferty.

### 2a. `onboarding_completed` od 2026-10-01

| `$os` | `$app_version` | zdarzeń | osób | TestFlight | emulator | nowy onboarding? |
|---|---|---|---|---|---|---|
| iOS | 2.0.94 | 2 | 2 | 0 | 0 | nie |
| Android | 2.0.94 | 2 | 2 | 0 | 0 | nie |
| Android | 2.0.95 | 1 | 1 | 0 | 0 | nie |
| iOS | 2.0.97 | 1 | 1 | 1 | 0 | **tak** |
| Android | 2.0.97 | 1 | 1 | 0 | 0 | **tak** |
| **Razem** | | **7** | **7** | | | **nowe buildy: 2 osoby** |

Na 2.0.98, 2.0.99, 2.0.100 nikt nie ukończył onboardingu.

### 2b. Oferta: pokazana vs pominięta (tylko nowe buildy, bo tylko tam istnieje)

| Metryka | iOS | Android | Razem |
|---|---|---|---|
| Ukończyli onboarding na nowym buildzie | 1 | 1 | 2 |
| `paywall_shown` z `trigger_feature=post_onboarding` (oferta na ekranie) | 0 | 0 | **0** |
| `post_onboarding_offer_not_shown` | 1 (`already_premium`) | 1 (`already_premium`) | **2 / 2 osoby** |
| `post_onboarding_offer_option_selected` / `_result` | 0 | 0 | 0 (zdarzenia nigdy nie istniały) |

`post_onboarding_offer_not_shown` po `reason`:

| reason | `$os` | `$app_version` | zdarzeń | osób | TestFlight |
|---|---|---|---|---|---|
| `already_premium` | iOS | 2.0.97 (164) | 1 | 1 | tak |
| `already_premium` | Android | 2.0.97 (168) | 1 | 1 | nie dotyczy (Android) |

Pozostałe powody (`no_active_trial`, `already_seen`, `products_unavailable`, `status_unavailable`, `not_just_onboarded`): 0.

### 2c. `paywall_load_failed`

| `$os` | `$app_version` | `error_type` | `trigger_feature` | zdarzeń | osób | urządzenie | emulator |
|---|---|---|---|---|---|---|---|
| Android | 2.0.98 (169) | `_Exception` | `drawer_menu` | 4 | 1 | OnePlus8Pro | false |
| Android | 2.0.99 (170) | `_Exception` | `premium_gate_habits` | 1 | 1 | OnePlus8Pro | false |
| Android | 2.0.99 (170) | `_Exception` | `drawer_menu` | 1 | 1 | OnePlus8Pro | false |

Wszystkie 6 zdarzeń od jednej osoby (konto automatów, pkt 3). Żadne nie ma `trigger_feature = post_onboarding`. iOS: 0. Kod błędu: brak, `error_type` niesie tylko typ wyjątku Darta (`_Exception`), bez kodu sklepu.

### 2d. `paywall_shown` w oknie po `trigger_feature` (kontekst)

| trigger | iOS | Android |
|---|---|---|
| `premium_gate_reflect_voice` | 6 zdarzeń / wersje 2.0.97-2.0.100 | 3 / 2.0.97, 2.0.100 |
| `drawer_menu` | 4 / 2.0.97, 2.0.98 | 1 / 2.0.94 |
| `premium_gate_monthly_audit` | 0 | 1 / 2.0.94 |
| `post_onboarding` | **0** | **0** |

Paywall jako taki ładuje się i loguje na nowych buildach (iOS i Android), więc problem nie jest w samym `paywall_shown`.

### 3. Konta testowe czy prawdziwi użytkownicy (wszystkie 7 osób z nowych buildów, bez identyfikatorów)

| # | Platforma | Pierwszy raz w PostHog | Wersji aplikacji w historii | distinct_id | `onboarding_completed` w historii | zakupy w historii | Rola w tym pytaniu | Klasyfikacja |
|---|---|---|---|---|---|---|---|---|
| 1 | iOS, TestFlight | 2026-04-24 | 34 | 4 | 5 | 4 | onboarding na 2.0.97, `not_shown: already_premium` | **tester wewnętrzny** |
| 2 | Android | 2026-04-23 | 41 | 6 | 6 | 4 | onboarding na 2.0.97, `not_shown: already_premium` | **tester wewnętrzny** (Android nie ma flagi TestFlight) |
| 3 | iOS + Android, część zdarzeń z emulatora, OnePlus8Pro | 2026-04-22 | 67 | 411 | 0 | 0 | wszystkie 6 x `paywall_load_failed` | **konto automatów** (farma pre-launch Google Play / konto do przeglądu; zlane w jedną osobę) |
| 4 | Android OnePlus8Pro, 2.0.96 | 2026-10-02 | 1 | 2 | 0 | 0 | 13 widoków kroków onboardingu, bez ukończenia, bez `user_registered` | **bot** (sygnatura pre-launch) |
| 5 | Android OnePlus8Pro, 2.0.97 | 2026-10-03 | 1 | 1 | 0 | 0 | tylko splash/welcome/auth/forgotPassword | **bot** |
| 6 | Android OnePlus8Pro, 2.0.100 | 2026-10-03 | 1 | 1 | 0 | 0 | tylko splash/welcome/auth | **bot** |
| 7 | iOS, nie TestFlight, nie emulator, 2.0.100 | 2026-10-03 | 1 | 1 | 0 | 0 | 1 zdarzenie | **niejasne**, najpewniej build deweloperski (Xcode); 2.0.100 nie jest publicznie dostępny |

Prawdziwi użytkownicy na nowych buildach: **0 potwierdzonych**.

Rejestracje 2026-10-03 (backend `user_registered`): 3 osoby. 2 przed 09:00 UTC (przed wdrożeniem backendowego `trial_started`), 1 o 09:xx z `trial_started`. Żadna z nich nie używa nowego buildu (ta z 09:xx ukończyła onboarding na Android 2.0.95 o 09:26, więc oferty w swojej wersji aplikacji nie ma).

## Werdykt

Za mało danych, bo nowy build ma 0 prawdziwych użytkowników. Nowy onboarding wysyłają tylko buildy 2.0.97-2.0.100 (od 2026-10-03 07:39 UTC). Ukończyły go na nich 2 osoby i obie to wewnętrzni testerzy z 4 zakupami w historii, więc ofertę pominięto zgodnie z kodem (`already_premium`). Oferta pokazała się 0% kończących onboarding na nowych buildach (0 z 2), ale na tych 2 kontach to zachowanie poprawne, a nie dowód błędu. Ścieżka "świeże konto z trialem kończy onboarding" nie wystąpiła w PostHog ani razu, więc hipotezy "oferta nikomu się nie pokazuje" nie da się z tych danych ani potwierdzić, ani obalić.

## Caveats

- **Ingest start 2026-04-22**: historia osób (pierwsze wejście, liczba wersji) nie sięga dalej.
- **Brak zdarzenia `post_onboarding_offer_shown`**. Pokazanie oferty mierzy się przez `paywall_shown` + `trigger_feature=post_onboarding`. To działa, ale tylko jeśli `revealPaywall()` zostanie wywołane; jeśli oferta wyrenderuje się bez załadowanych produktów, `paywall_shown` nie wystrzeli. Po wejściu w krok oferty nie ma osobnego sygnału "ekran oferty na ekranie".
- **`paywall_load_failed.error_type` jest mało informatywny** (`_Exception`, typ wyjątku zamiast kodu sklepu/`IAPError.code`). Z PostHoga nie da się odczytać przyczyny błędu ładowania produktów.
- **Małe n**: wszystkie liczności są pojedyncze. Raportuję je mimo progu k-anonimowości 25, bo to liczniki zdarzeń lejka zakupowego bez atrybutów zdrowotnych i bez identyfikatorów. Tabela osób w pkt 3 nie zawiera ID ani modeli urządzeń testerów.
- **`$is_testflight` istnieje tylko na iOS**; na Androidzie testerów rozpoznaję po historii (dziesiątki wersji, wielokrotny onboarding, zakupy), a boty po `$device_model = OnePlus8Pro` (stały filtr wykluczający farmę pre-launch).
- **Osoba #3 to zlanie wielu urządzeń w jedną osobę** (411 distinct_id). To typowe dla współdzielonego konta logowania automatów (np. dane "App access" w Play Console); nie traktować jako użytkownika.
- **Ryzyko do sprawdzenia poza PostHogiem**: `already_premium` traktuje `premium_source = null` jak płatne premium. Jeśli backend zwraca `null` dla świeżego konta (brak wiersza `UserSubscription` albo trial przyznany bez `granted_via='signup_trial'`), oferta zostanie pominięta u każdego nowego użytkownika z powodem `already_premium`. Weryfikacja: `database-administrator`, rozkład `user_subscriptions.granted_via` dla kont utworzonych 2026-10-03 po wdrożeniu backendu f5ea34d.

## Queries

```sql
-- @@ A_versions_in_window
SELECT properties.$os AS os, properties.$app_version AS ver, properties.$app_build AS build,
       properties.$app_namespace AS ns,
       count() AS events, count(DISTINCT person_id) AS users,
       count(DISTINCT if(properties.$is_testflight = true, person_id, NULL)) AS tf_users,
       count(DISTINCT if(properties.$is_emulator = true, person_id, NULL)) AS emu_users,
       count(DISTINCT if(properties.$is_sideloaded = true, person_id, NULL)) AS sideload_users,
       min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp >= toDateTime('2026-10-01 00:00:00')
  AND properties.$lib = 'posthog-flutter'
GROUP BY os, ver, build, ns
ORDER BY first_ts DESC
LIMIT 60

-- @@ B_new_flow_first_seen_per_version
SELECT event, properties.$os AS os, properties.$app_version AS ver, properties.$app_build AS build,
       count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp >= toDateTime('2026-09-01 00:00:00')
  AND properties.$lib = 'posthog-flutter'
  AND (event IN ('post_onboarding_build_viewed', 'post_onboarding_build_finished', 'personal_reveal_viewed',
                 'personal_reveal_cta_tapped', 'post_onboarding_offer_not_shown',
                 'post_onboarding_offer_option_selected', 'post_onboarding_offer_result',
                 'paywall_load_failed', 'usage_snapshot', 'first_capture_prompt_option_tapped',
                 'push_prompt_viewed', 'push_prompt_result', 'premium_welcome_viewed', 'trial_bar_viewed')
       OR (event IN ('paywall_shown', 'subscription_screen_opened') AND properties.trigger_feature = 'post_onboarding'))
GROUP BY event, os, ver, build
ORDER BY ver, build, first_ts
LIMIT 200

-- @@ C_onboarding_completed_by_os_ver
SELECT properties.$os AS os, properties.$app_version AS ver, properties.$app_build AS build,
       count() AS c, count(DISTINCT person_id) AS users,
       count(DISTINCT if(properties.$is_testflight = true, person_id, NULL)) AS tf_users,
       count(DISTINCT if(properties.$is_emulator = true, person_id, NULL)) AS emu_users,
       count(DISTINCT if(properties.$is_sideloaded = true, person_id, NULL)) AS sideload_users,
       min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp >= toDateTime('2026-10-01 00:00:00')
  AND properties.$lib = 'posthog-flutter'
  AND event = 'onboarding_completed'
GROUP BY os, ver, build
ORDER BY first_ts
LIMIT 50

-- @@ D_offer_not_shown_by_reason
SELECT properties.reason AS reason, properties.$os AS os, properties.$app_version AS ver, properties.$app_build AS build,
       count() AS c, count(DISTINCT person_id) AS users,
       count(DISTINCT if(properties.$is_testflight = true, person_id, NULL)) AS tf_users,
       min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp >= toDateTime('2026-10-01 00:00:00')
  AND event = 'post_onboarding_offer_not_shown'
GROUP BY reason, os, ver, build
ORDER BY first_ts
LIMIT 50

-- @@ E_paywall_shown_by_trigger
SELECT properties.trigger_feature AS trig, properties.$os AS os, properties.$app_version AS ver,
       count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp >= toDateTime('2026-10-01 00:00:00')
  AND properties.$lib = 'posthog-flutter'
  AND event IN ('paywall_shown')
GROUP BY trig, os, ver
ORDER BY first_ts
LIMIT 60

-- @@ F_paywall_load_failed
SELECT properties.$os AS os, properties.$app_version AS ver, properties.$app_build AS build,
       properties.error_type AS error_type, properties.trigger_feature AS trig,
       count() AS c, count(DISTINCT person_id) AS users,
       count(DISTINCT if(properties.$is_testflight = true, person_id, NULL)) AS tf_users,
       count(DISTINCT if(properties.$is_sideloaded = true, person_id, NULL)) AS sideload_users,
       min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp >= toDateTime('2026-10-01 00:00:00')
  AND event = 'paywall_load_failed'
GROUP BY os, ver, build, error_type, trig
ORDER BY first_ts
LIMIT 50

-- @@ P_new_build_persons  (output without person_id)
SELECT
  groupUniqArrayIf(toString(properties.$os), timestamp >= toDateTime('2026-10-01 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$os IS NOT NULL) AS oses,
  arraySort(groupUniqArrayIf(toString(properties.$app_version), timestamp >= toDateTime('2026-10-01 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$app_version IS NOT NULL)) AS versions_since_1001,
  countIf(properties.$is_testflight = true AND timestamp >= toDateTime('2026-10-01 00:00:00')) > 0 AS any_tf,
  countIf(properties.$is_testflight = false AND properties.$os = 'iOS' AND timestamp >= toDateTime('2026-10-01 00:00:00')) > 0 AS any_ios_not_tf,
  countIf(properties.$is_emulator = true AND timestamp >= toDateTime('2026-10-01 00:00:00')) > 0 AS any_emu,
  toDate(min(timestamp)) AS first_seen_day,
  count(DISTINCT distinct_id) AS n_distinct_ids,
  count(DISTINCT toString(properties.$app_version)) AS n_versions_lifetime,
  countIf(event = 'onboarding_completed') AS onb_completed_lifetime,
  countIf(event = 'subscription_purchase_completed') AS purchases_lifetime,
  countIf(event = 'premium_welcome_viewed') AS premium_welcome_since_1003,
  countIf(event = 'post_onboarding_offer_not_shown') AS offer_not_shown,
  countIf(event = 'paywall_load_failed') AS paywall_load_failed_n,
  countIf(event = 'onboarding_completed' AND timestamp >= toDateTime('2026-10-01 00:00:00')) AS onb_completed_since_1001,
  countIf(timestamp >= toDateTime('2026-10-01 00:00:00')) AS events_since_1001
FROM events
WHERE timestamp >= toDateTime('2026-04-22 00:00:00')
  AND person_id IN (
    SELECT DISTINCT person_id FROM events
    WHERE timestamp >= toDateTime('2026-10-01 00:00:00')
      AND properties.$lib = 'posthog-flutter'
      AND properties.$app_version IN ('2.0.96', '2.0.97', '2.0.98', '2.0.99', '2.0.100')
  )
GROUP BY person_id
ORDER BY first_seen_day
LIMIT 50

-- @@ T_new_persons_on_new_builds  (output without person_id)
SELECT
  any(toString(properties.$os)) AS os,
  arraySort(groupUniqArray(toString(properties.$app_version))) AS versions,
  groupUniqArray(toString(properties.$device_model)) AS device_models,
  countIf(properties.$is_emulator = true) AS emu_events,
  countIf(properties.$is_testflight = true) AS tf_events,
  toDate(min(timestamp)) AS first_day,
  dateDiff('second', min(timestamp), max(timestamp)) AS span_s,
  count() AS events,
  countIf(event = 'user_registered') AS registered,
  countIf(event = 'onboarding_started') AS onb_started,
  countIf(event = 'onboarding_step_viewed') AS onb_steps_viewed,
  arrayStringConcat(arraySort(groupUniqArrayIf(toString(properties.step_name), event = 'onboarding_step_viewed')), ',') AS steps_seen,
  arrayStringConcat(arraySort(groupUniqArrayIf(toString(properties.$screen_name), event = '$screen')), ',') AS screens_seen,
  countIf(event = 'onboarding_completed') AS onb_completed
FROM events
WHERE timestamp >= toDateTime('2026-10-01 00:00:00')
  AND properties.$lib = 'posthog-flutter'
  AND person_id IN (
    SELECT person_id FROM events
    WHERE timestamp >= toDateTime('2026-04-22 00:00:00')
    GROUP BY person_id
    HAVING min(timestamp) >= toDateTime('2026-10-01 00:00:00')
       AND countIf(properties.$app_version IN ('2.0.96', '2.0.97', '2.0.98', '2.0.99', '2.0.100')) > 0
  )
GROUP BY person_id
ORDER BY first_day
LIMIT 20

-- @@ U_load_failed_flags
SELECT properties.$is_emulator AS emu, properties.$device_model AS model, properties.$app_version AS ver,
       count() AS c, count(DISTINCT person_id) AS users
FROM events
WHERE timestamp >= toDateTime('2026-10-01 00:00:00')
  AND event = 'paywall_load_failed'
GROUP BY emu, model, ver
LIMIT 20

-- @@ W_registrations_1003_with_client_context
SELECT toStartOfHour(r.ts) AS hour,
       count() AS registrations,
       countIf(t.has_trial) AS with_trial_started,
       countIf(c.ver IN ('2.0.97','2.0.98','2.0.99','2.0.100')) AS on_new_build,
       countIf(c.bot) AS bot_device
FROM (
  SELECT person_id, min(timestamp) AS ts FROM events
  WHERE event = 'user_registered' AND timestamp >= toDateTime('2026-10-03 00:00:00')
  GROUP BY person_id
) AS r
LEFT JOIN (
  SELECT person_id, count() > 0 AS has_trial FROM events
  WHERE event = 'trial_started' AND timestamp >= toDateTime('2026-10-03 00:00:00')
  GROUP BY person_id
) AS t ON r.person_id = t.person_id
LEFT JOIN (
  SELECT person_id, any(toString(properties.$app_version)) AS ver,
         countIf(properties.$device_model IN ('OnePlus8Pro', 'Pixel 6 Pro')) > 0 AS bot
  FROM events
  WHERE timestamp >= toDateTime('2026-10-03 00:00:00') AND properties.$lib = 'posthog-flutter'
  GROUP BY person_id
) AS c ON r.person_id = c.person_id
GROUP BY hour
ORDER BY hour
LIMIT 30
```
