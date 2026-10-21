# Retencja i zaangażowanie (kohorty 90 dni) - raw PostHog extract

- **Date**: 2026-10-15 · **Agent**: posthog-data-extractor
- **Project**: PostHog EU 141170 · **Window**: 2026-07-17 → 2026-10-14 (pełne dni UTC; pierwsze wystąpienie liczone od startu ingestu 2026-04-22)
- **Question**: DAU/WAU/MAU, retencja kohort tygodniowych W0..W8, D1/D7/D30 przed i po 03.10, retencja per platforma i status, lifecycle tygodniowy, stickiness funkcji.
- **Event verification**: wszystkie użyte zdarzenia płyną z `$lib = posthog-flutter` (90d, filtry domyślne): `$screen` 459 os., `timeline_viewed` 148, `workspace_opened` 79, `habit_tracker_viewed` 53 (od 09-15), `reflect_message_submitted` 35, `summary_viewed` 22, `recording_started` 22, `voice_chat_started` 16, `habit_check_toggled` 10, `stat_opened` 1 os. (pierwszy raz 10-14). Brak dedykowanego zdarzenia dla Trends (patrz Luki).

## Definicje

- **Filtry domyślne** (każde zapytanie): `properties.$lib = 'posthog-flutter'`, `$is_testflight != true`, `$is_emulator != true`, `$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro')`. Liczone po `person_id`, czas UTC.
- **Aktywny (szeroko)**: dowolne zdarzenie klienta poza pasywnymi/systemowymi (`$identify`, `$set`, `$exception`, `client_error`, `notification_received`, `usage_snapshot`, `app_install_attributed`, `notification_banner_shown` itd.). Zdarzenia klienta odpalają się tylko przy otwartej aplikacji, więc sam push (backend) się nie liczy. Obejmuje jednak osoby, które otworzyły tylko splash/welcome/auth.
- **Aktywny (ściśle)**: jak wyżej, minus ekrany i zdarzenia sprzed wejścia do aplikacji: `$screen` splash/welcome/auth/signUp/forgotPassword/therapyOnboarding/wow, wszystkie `onboarding_*`, `signup_*`, `auth_*`, `consent_*`, `login_*`, `password_reset_*`, `notification_permission_*`, `user_logged_in/out`, `welcome_cta_tapped`. To jest "otwarcie aplikacji + działanie po zalogowaniu".
- **Kohorta**: tydzień (poniedziałek) albo dzień pierwszej aktywności od 2026-04-22.
- **Prywatność**: liczniki < 5 jako "n<5". Podstawy < 25 osób: same liczby, bez odsetka (domyślny próg k-anonimowości agenta to 25; zespół poprosił o próg 5, stosuję oba w ten sposób).

## 1. DAU / WAU / MAU (średnie dzienne w tygodniu, okna kroczące 7 i 30 dni)

| tydzień od | DAU szer. | WAU szer. | MAU szer. | DAU/MAU szer. | DAU ściśle | WAU ściśle | MAU ściśle | DAU/MAU ściśle |
|---|---|---|---|---|---|---|---|---|
| 07-13 (3 dni) | 10.0 | 42.3 | 163.3 | 0.061 | 4.0 | 16.7 | 60.7 | 0.066 |
| 07-20 | 8.1 | 45.4 | 156.6 | 0.052 | 4.6 | 17.0 | 60.6 | 0.075 |
| 07-27 | 9.1 | 42.3 | 150.9 | 0.061 | 5.1 | 22.0 | 61.3 | 0.084 |
| 08-03 | 10.7 | 53.1 | 152.0 | 0.070 | 7.6 | 30.3 | 68.0 | 0.111 |
| 08-10 | 10.9 | 50.1 | 154.4 | 0.070 | 8.0 | 32.0 | 73.1 | 0.109 |
| 08-17 | 9.7 | 49.9 | 156.4 | 0.062 | 6.6 | 31.3 | 82.1 | 0.080 |
| 08-24 | 7.1 | 36.4 | 149.4 | 0.048 | 5.1 | 23.7 | 80.3 | 0.064 |
| 08-31 | 8.6 | 35.9 | 134.9 | 0.064 | 5.7 | 20.0 | 74.1 | 0.077 |
| 09-07 | 8.9 | 42.0 | 126.9 | 0.070 | 6.3 | 26.1 | 71.4 | 0.088 |
| 09-14 | 7.6 | 39.3 | 118.6 | 0.064 | 4.9 | 23.4 | 65.6 | 0.074 |
| 09-21 | 14.0 | 52.0 | 130.6 | 0.107 | 7.4 | 25.9 | 65.0 | 0.114 |
| 09-28 | 20.4 | 88.4 | 182.1 | 0.112 | 7.3 | 24.6 | 66.7 | 0.109 |
| 10-05 | 15.6 | 96.6 | 234.6 | 0.066 | 8.4 | 29.6 | 73.0 | 0.115 |
| 10-12 (3 dni) | 13.0 | 63.7 | 249.7 | 0.052 | 9.7 | 35.7 | 82.7 | 0.117 |

Unikalne osoby aktywne (szeroko) w 90 dniach: 461 (33 947 zdarzeń).

## 2. Retencja kohort tygodniowych (szeroka definicja, kohorty łączone do n>=25)

Wk = osoby aktywne w k-tym tygodniu po tygodniu kohorty (nie kumulatywnie). "niepełne" = tydzień jeszcze nie minął.

| kohorta | n | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 |
|---|---|---|---|---|---|---|---|---|---|
| 07-13..07-27 | 67 | 8 (11.9%) | n<5 | n<5 | n<5 | n<5 | n<5 | n<5 | n<5 (0) |
| 08-03..08-10 | 57 | 10 (17.5%) | 8 (14.0%) | 6 (10.5%) | n<5 | n<5 | n<5 | n<5 | n<5 |
| 08-17..08-31 | 47 | 6 (12.8%) | 7 (14.9%) | 5 (10.6%) | 6 (12.8%) | n<5 | niepełne | niepełne | niepełne |
| 09-07..09-14 | 38 | n<5 | 5 (13.2%) | n<5 | niepełne | | | | |
| 09-21 | 46 | 7 (15.2%) | n<5 | niepełne | | | | | |
| 09-28 | 78 | 6 (7.7%) | niepełne | | | | | | |
| 10-05 | 57 | niepełne (5 do dziś) | | | | | | | |
| 10-12 | 18 | tylko W0 | | | | | | | |

Tylko osoby, które ukończyły onboarding w PostHogu (`onboarding_completed`):

| kohorta | n | W1 | W2 | W3 | W4 |
|---|---|---|---|---|---|
| 07-13..08-31 | 55 | 15 (27.3%) | 14 (25.5%) | 9 (16.4%) | 5 (9.1%) |
| 09-07..09-28 | 32 | 10 (31.3%) | n<25 w pełnym oknie (5 z 22) | niepełne | |
| 10-05 | 15 | n<25, niepełne | | | |

Udział kohort, które w ogóle ukończyły onboarding: 07-13..08-31: 55/197; 09-21: 10/46; 09-28: 10/78; 10-05: 15/57.

## 3. D1 / D7 / D30 przed i po 2026-10-03

D1 = aktywny dokładnie w dniu +1. D7 = jakakolwiek aktywność w dniach +1..+7 (kumulatywnie). D30 = w dniach +1..+30; "D30 okno" = aktywność w dniach +23..+30. Kwalifikują się tylko kohorty z w pełni minionym oknem.

Szeroka definicja:

| grupa (pierwszy dzień) | segment | n D1 | D1 | n D7 | D7 | n D30 | D30 | D30 okno |
|---|---|---|---|---|---|---|---|---|
| 07-17..09-02 | wszyscy | 153 | 11 (7.2%) | 153 | 33 (21.6%) | 153 | 47 (30.7%) | 10 (6.5%) |
| 07-17..09-02 | po onboardingu | 49 | 8 (16.3%) | 49 | 21 (42.9%) | 49 | 27 (55.1%) | 6 (12.2%) |
| 07-17..09-02 | bez onboardingu | 104 | n<5 | 104 | 12 (11.5%) | 104 | 20 (19.2%) | n<5 |
| 09-03..10-02 | wszyscy | 152 | 17 (11.2%) | 152 | 26 (17.1%) | 33 | 10 (30.3%) | n<5 |
| 09-03..10-02 | po onboardingu | 32 | 7 (21.9%) | 32 | 11 (34.4%) | 15 | n<25 | n<25 |
| 09-03..10-02 | bez onboardingu | 120 | 10 (8.3%) | 120 | 15 (12.5%) | 18 | n<25 | n<25 |
| od 10-03 | wszyscy | 85 | 8 (9.4%) | 51 | 9 (17.6%) | 0 | brak | brak |
| od 10-03 | po onboardingu | 23 | 5 (n<25) | 7 | n<25 | 0 | brak | brak |
| od 10-03 | bez onboardingu | 62 | n<5 | 44 | n<5 | 0 | brak | brak |

Ścisła definicja (tylko aktywność po zalogowaniu):

| grupa | n D1 | D1 | n D7 | D7 | n D30 | D30 | D30 okno |
|---|---|---|---|---|---|---|---|
| 07-17..09-02 | 74 | 9 (12.2%) | 74 | 20 (27.0%) | 74 | 28 (37.8%) | 5 (6.8%) |
| 09-03..10-02 | 48 | 8 (16.7%) | 48 | 14 (29.2%) | 21 | n<25 | n<25 |
| od 10-03 | 28 | 6 (21.4%) | 9 | n<25 | 0 | brak | brak |

## 4. Retencja per platforma i per status (kohorty 07-17..10-07, szeroka definicja)

| wymiar | wartość | n | D1 | D7 | aktywny po D7 | śr. dni aktywnych |
|---|---|---|---|---|---|---|
| platforma | Android | 319 | 29 (9.1%) | 55 (17.2%) | 37 (11.6%) | 1.66 |
| platforma | iOS | 34 | n<5 | 13 (38.2%) | 15 (44.1%) | 3.38 |
| platforma | iPadOS | n<5 | | | | |
| status | brak właściwości | 303 | 17 (5.6%) | 39 (12.9%) | 28 (9.2%) | 1.31 |
| status | premium | 38 | 13 (34.2%) | 22 (57.9%) | 14 (36.8%) | 4.84 |
| status | basic | 9 (n<25) | | | | |
| status | free | 6 (n<25) | | | | |
| status, tylko po onboardingu | brak właściwości | 43 | n<5 | 10 (23.3%) | 8 (18.6%) | 1.65 |
| status, tylko po onboardingu | premium | 36 | 12 (33.3%) | 21 (58.3%) | 14 (38.9%) | 5.03 |

Właściwość osoby `subscription_tier` (cały projekt): premium 113, basic 31, free 17, brak 3 983. `premium_source`: signup_trial 52, purchase 4, starter_pack 1. `plan`: trial 52, premium 5, free 4. Status to stan OBECNY (ostatnia wartość), nie stan w dniu wejścia do kohorty; "premium" w większości oznacza trial nadawany przy rejestracji od 03.10.

## 5. Lifecycle tygodniowy (szeroka definicja)

nowi = pierwszy tydzień; powracający = aktywni w W i W-1; wskrzeszeni = aktywni w W, nieaktywni w W-1, nie nowi; uśpieni = aktywni w W-1, nieaktywni w W.

| tydzień od | nowi | powracający | wskrzeszeni | uśpieni |
|---|---|---|---|---|
| 07-20 | 21 | 10 | 10 | 33 |
| 07-27 | 25 | 13 | 12 | 28 |
| 08-03 | 31 | 12 | 8 | 38 |
| 08-10 | 26 | 11 | 13 | 40 |
| 08-17 | 21 | 12 | 12 | 38 |
| 08-24 | 10 | 11 | 11 | 34 |
| 08-31 | 16 | 11 | 12 | 21 |
| 09-07 | 20 | 13 | 8 | 26 |
| 09-14 | 18 | 12 | 7 | 29 |
| 09-21 | 46 | 12 | 12 | 25 |
| 09-28 | 78 | 15 | 7 | 55 |
| 10-05 | 57 | 15 | 7 | 85 |
| 10-12 (niepełny, pn-czw) | 18 | 14 | n<5 | 65 (zawyżone, tydzień trwa) |

Quick ratio (nowi+wskrzeszeni)/uśpieni: poniżej 1 w każdym pełnym tygodniu poza 09-21 (2.3) i 09-28 (1.5).

## 6. Stickiness funkcji wśród aktywnych (28 dni: 09-17..10-14)

Baza: 244 osoby aktywne (szeroko). "dzienni/28d" = średnia liczba dziennych użytkowników funkcji podzielona przez jej użytkowników w 28 dniach (odpowiednik DAU/MAU funkcji).

| funkcja (zdarzenia) | użytkownicy 28d | śr. dni z funkcją | >=3 dni | >=2 tygodnie | dzienni/28d |
|---|---|---|---|---|---|
| dowolna aktywność | 244 | 1.70 | 32 (13.1%) | 31 (12.7%) | 0.061 |
| timeline (`timeline_viewed`, wczytanie Home) | 57 | 3.18 | 20 (35.1%) | 18 (31.6%) | 0.113 |
| nawyki, widok (`habit_tracker_viewed`) | 50 | 2.88 | 16 (32.0%) | 15 (30.0%) | 0.103 |
| Workspace (`workspace_opened`) | 40 | 2.52 | 9 (22.5%) | 12 (30.0%) | 0.090 |
| pętla terapii (prep/debrief/between/health_check start) | 28 | 2.36 | 8 (28.6%) | 6 (21.4%) | 0.084 |
| Reflect (wiadomość, wątek, tryb) | 28 | 2.11 | 8 (28.6%) | 8 (28.6%) | 0.075 |
| rozmowa głosowa (`voice_chat_started`, `first_conversation_started`) | 23 (n<25) | 1.57 | n<5 | n<5 | 0.056 |
| nawyki, akcja (odhaczenie/utworzenie) | 17 (n<25) | 2.53 | 5 | 5 | 0.090 |
| podsumowania (`summary_viewed`) | 12 (n<25) | 2.25 | n<5 | 6 | 0.080 |
| nagranie sesji (`recording_started`) | 11 (n<25) | 2.91 | n<5 | n<5 | 0.104 |
| quick capture | 5 (n<25) | | n<5 | n<5 | |
| Trends (`stat_opened`, ekran `firstWeekTrends`) | n<5 | | | | |

Użycie funkcji w okresie 1 (09-17..09-30) a powrót w okresie 2 (10-01..10-14); baza: 118 osób aktywnych w okresie 1, z nich wróciło 25 (21.2%):

| funkcja w okresie 1 | użytkownicy | wrócili | nieużytkownicy | nieużytkownicy, wrócili |
|---|---|---|---|---|
| timeline | 30 | 13 (43.3%) | 88 | 12 (13.6%) |
| nawyki, widok | 24 (n<25) | 10 | 94 | 15 (16.0%) |
| Workspace | 21 (n<25) | 9 | 97 | 16 (16.5%) |
| pętla terapii | 14 (n<25) | 9 | 104 | 16 (15.4%) |
| Reflect | 13 (n<25) | 8 | 105 | 17 (16.2%) |
| nawyki, akcja | 9 (n<25) | 7 | 109 | 18 (16.5%) |
| podsumowania | 9 (n<25) | 6 | 109 | 19 (17.4%) |
| nagranie sesji | 9 (n<25) | 6 | 109 | 19 (17.4%) |
| rozmowa głosowa | 8 (n<25) | 6 | 110 | 19 (17.3%) |
| quick capture | n<5 | n<5 | 115 | 24 |
| Trends | 0 | 0 | 118 | 25 |

To jest korelacja. Osoby, które w ogóle weszły głębiej w aplikację, wracają częściej niezależnie od tego, której funkcji dotknęły (efekt selekcji: zaangażowanie poprzedza użycie funkcji, a nie odwrotnie). Brak tu kontroli na liczbę dni aktywności w okresie 1, więc żadna z różnic nie jest dowodem, że funkcja *powoduje* powrót.

## Caveats

- **Ingest od 2026-04-22.** "Nowy" = pierwsza aktywność klienta od tej daty. Osoby nieaktywne od kwietnia, ale zarejestrowane wcześniej (przed ingestem) liczą się jako nowe, jeśli wróciły dopiero teraz; dotyczy głównie kohort lipcowych.
- **MAU szerokie jest zawyżone przez odbicia przed logowaniem.** W tygodniu 10-05 MAU szerokie 234.6 vs ściśle 73.0: ok. 2/3 "aktywnych w miesiącu" nie przeszło dalej niż splash/welcome/auth/onboarding. Wzrost szerokiego MAU od 09-21 to napływ instalacji (nowi 46/78/57 tygodniowo), a nie wzrost zaangażowania. Ściśle: MAU 61-83, DAU/MAU rośnie z 0.066-0.084 (lipiec) do 0.115-0.117 (październik).
- **Przed/po 03.10**: kohorta po redesignie ma 12 dni; D7 kwalifikuje się tylko 9 osób (ściśle) albo 51 (szeroko), D30 nikt. D1 ściśle 21.4% vs 16.7% (wrzesień) vs 12.2% (lipiec-sierpień) to różnica rzędu 1-2 osób na podstawie 28-74; mieści się w szumie. Nie da się jeszcze stwierdzić wpływu redesignu.
- **Dzielnik się zmienił**: redesign przeniósł część ekranów (np. trial przy rejestracji, `post_onboarding_*`), więc "ukończył onboarding" przed i po 03.10 to nie do końca ten sam krok.
- **Platforma**: iOS (34) ma wyraźnie lepszą retencję niż Android (319), ale populacje różnią się składem (Android ma znacznie więcej odbić przed rejestracją i ruch z Play pre-launch, częściowo odfiltrowany). To korelacja, nie efekt platformy. TestFlight wyłączony, więc iOS nie zawiera testerów.
- **Status premium/trial/free** jest odwrotną przyczynowością w dużym stopniu: trial dostaje każdy, kto przejdzie rejestrację od 03.10, a `subscription_tier` jest ustawiany tylko dla osób, które doszły do zalogowania. "brak właściwości" to głównie osoby, które nigdy się nie zarejestrowały. Brak historii statusu w czasie, więc nie da się odtworzyć statusu w dniu wejścia. Trial vs płatny: tylko 4 zakupy w `premium_source`; rozbicie niemożliwe przy progu prywatności. Prawda o płatnościach: Postgres (`subscription_receipts`) przez `database-administrator`.
- **Skew pojedynczej osoby**: w 28 dniach najaktywniejsza osoba ma 1 755 z 13 961 zdarzeń (12.6%); w Reflect 182/1 036 (17.6%); w nawykach-akcji 51/97 (53%). Metryki w tabelach liczone po osobach i dniach, więc skew nie zawyża liczby użytkowników, ale "średnia dni" dla nawyków-akcji jest wrażliwa.
- **`timeline_viewed`** to wczytanie osi czasu na Home, nie świadoma akcja; jego "stickiness" mierzy zasadniczo powrót do aplikacji po zalogowaniu (prawie tautologia z retencją). `habit_tracker_viewed` może też być wczytaniem karty. Do porównań funkcji wiarygodniejsze są zdarzenia akcji.
- `tab_switched` celowo pominięty jako sygnał funkcji (zawyżenie przez przewijanie PageView, patrz notatka z 2026-10-13).

## Luki instrumentacji

- **Trends**: brak zdarzenia otwarcia zakładki/ekranu Trends. Jedyne ślady: `stat_opened` (od 2026-10-14, 1 osoba) i ekran `firstWeekTrends` (3 osoby/30d). Stickiness Trends niemierzalna. Właściciel: `flutter-mobile` (np. `trends_viewed` z `source`).
- **Status subskrypcji w czasie**: brak właściwości zdarzenia z tierem (super-property), więc retencji per status w momencie wejścia nie da się policzyć. Propozycja dla `flutter-mobile`: rejestrować `subscription_tier` i `is_trial` jako super-property na zdarzeniach klienta.
- **Rozmowa głosowa po 10-05**: `first_conversation_started` liczona razem z `voice_chat_started`; brak jednego zdarzenia "voice session started" dla wszystkich ścieżek wejścia.

## Queries

Filtr `$F` (szeroki) jest rozwinięty w każdym zapytaniu poniżej dosłownie. Pliki uruchamiane przez `scripts/posthog_query.py --sql-file`.


### r3.sql

```sql
-- @@ dau_wau_mau_weekly
SELECT toStartOfWeek(d, 1) AS wk, round(avg(dau),1) AS avg_dau, round(avg(wau),1) AS avg_wau, round(avg(mau),1) AS avg_mau, round(avg(dau)/avg(mau),3) AS dau_mau, count() AS days_in_wk
FROM (
  SELECT addDays(day, n) AS d, uniqExactIf(person_id, n = 0) AS dau, uniqExactIf(person_id, n < 7) AS wau, uniqExact(person_id) AS mau
  FROM (SELECT DISTINCT person_id, toDate(timestamp) AS day FROM events WHERE timestamp >= now() - INTERVAL 125 DAY AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received'))
  ARRAY JOIN range(30) AS n
  GROUP BY d HAVING d >= today() - 90 AND d <= today() - 1
) GROUP BY wk ORDER BY wk

-- @@ uniques_90d
SELECT count(DISTINCT person_id) AS users_90d, countIf(timestamp > now() - INTERVAL 30 DAY) AS ev30 , count() AS ev90
FROM events WHERE timestamp > now() - INTERVAL 90 DAY AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received')

-- @@ cohort_weekly
SELECT cohort_wk, count() AS size,
  countIf(has(wks, addWeeks(cohort_wk,1))) AS w1, countIf(has(wks, addWeeks(cohort_wk,2))) AS w2,
  countIf(has(wks, addWeeks(cohort_wk,3))) AS w3, countIf(has(wks, addWeeks(cohort_wk,4))) AS w4,
  countIf(has(wks, addWeeks(cohort_wk,5))) AS w5, countIf(has(wks, addWeeks(cohort_wk,6))) AS w6,
  countIf(has(wks, addWeeks(cohort_wk,7))) AS w7, countIf(has(wks, addWeeks(cohort_wk,8))) AS w8,
  countIf(onb) AS size_onboarded
FROM (
  SELECT person_id, toStartOfWeek(min(timestamp), 1) AS cohort_wk, groupUniqArray(toStartOfWeek(timestamp, 1)) AS wks,
         countIf(event = 'onboarding_completed') > 0 AS onb
  FROM events WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received') GROUP BY person_id
) WHERE cohort_wk >= toStartOfWeek(today() - 90, 1)
GROUP BY cohort_wk ORDER BY cohort_wk

-- @@ cohort_weekly_onboarded_only
SELECT cohort_wk, count() AS size,
  countIf(has(wks, addWeeks(cohort_wk,1))) AS w1, countIf(has(wks, addWeeks(cohort_wk,2))) AS w2,
  countIf(has(wks, addWeeks(cohort_wk,3))) AS w3, countIf(has(wks, addWeeks(cohort_wk,4))) AS w4,
  countIf(has(wks, addWeeks(cohort_wk,6))) AS w6, countIf(has(wks, addWeeks(cohort_wk,8))) AS w8
FROM (
  SELECT person_id, toStartOfWeek(min(timestamp), 1) AS cohort_wk, groupUniqArray(toStartOfWeek(timestamp, 1)) AS wks,
         countIf(event = 'onboarding_completed') > 0 AS onb
  FROM events WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received') GROUP BY person_id
) WHERE cohort_wk >= toStartOfWeek(today() - 90, 1) AND onb
GROUP BY cohort_wk ORDER BY cohort_wk

-- @@ d_retention_pre_post
SELECT grp, onb,
  countIf(first_day <= today() - 2) AS n_d1, countIf(first_day <= today() - 2 AND has(days, addDays(first_day,1))) AS d1,
  countIf(first_day <= today() - 8) AS n_d7, countIf(first_day <= today() - 8 AND has(days, addDays(first_day,7))) AS d7_exact,
  countIf(first_day <= today() - 8 AND arrayExists(x -> x > first_day AND x <= addDays(first_day,7), days)) AS d7_within,
  countIf(first_day <= today() - 31) AS n_d30, countIf(first_day <= today() - 31 AND has(days, addDays(first_day,30))) AS d30_exact,
  countIf(first_day <= today() - 31 AND arrayExists(x -> x >= addDays(first_day,23) AND x <= addDays(first_day,30), days)) AS d30_wk_window,
  countIf(first_day <= today() - 31 AND arrayExists(x -> x > first_day AND x <= addDays(first_day,30), days)) AS d30_within
FROM (
  SELECT person_id, min(toDate(timestamp)) AS first_day, groupUniqArray(toDate(timestamp)) AS days,
         countIf(event = 'onboarding_completed') > 0 AS onb,
         multiIf(min(toDate(timestamp)) >= toDate('2026-10-03'), '3_post_1003',
                 min(toDate(timestamp)) >= toDate('2026-09-03'), '2_pre_0903_1002',
                 min(toDate(timestamp)) >= toDate('2026-07-17'), '1_pre_0717_0902', '0_older') AS grp
  FROM events WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received') GROUP BY person_id
) WHERE grp != '0_older'
GROUP BY grp, onb ORDER BY grp, onb

-- @@ lifecycle_weekly
SELECT W, countIf(has(wks, W) AND first_wk = W) AS new_users,
  countIf(has(wks, W) AND first_wk < W AND has(wks, addWeeks(W,-1))) AS returning,
  countIf(has(wks, W) AND first_wk < W AND NOT has(wks, addWeeks(W,-1))) AS resurrected,
  countIf(NOT has(wks, W) AND has(wks, addWeeks(W,-1))) AS dormant
FROM (
  SELECT person_id, toStartOfWeek(min(timestamp), 1) AS first_wk, groupUniqArray(toStartOfWeek(timestamp, 1)) AS wks
  FROM events WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received') GROUP BY person_id
) ARRAY JOIN arrayMap(i -> addWeeks(toStartOfWeek(today(), 1), -i), range(0, 13)) AS W
GROUP BY W ORDER BY W
```

### r5.sql

```sql
-- @@ person_status_values
SELECT k, v, persons FROM (
  SELECT 'subscription_tier' AS k, toString(properties.subscription_tier) AS v, count() AS persons FROM persons GROUP BY v
  UNION ALL SELECT 'premium_source' AS k, toString(properties.premium_source) AS v, count() AS persons FROM persons GROUP BY v
  UNION ALL SELECT 'plan' AS k, toString(properties.plan) AS v, count() AS persons FROM persons GROUP BY v
) ORDER BY k, persons DESC LIMIT 40

-- @@ retention_by_os_and_tier
SELECT tupleElement(t,1) AS dim, tupleElement(t,2) AS val, count() AS n, countIf(has(days, addDays(first_day,1))) AS d1,
  countIf(arrayExists(x -> x > first_day AND x <= addDays(first_day,7), days)) AS d7_within,
  countIf(arrayExists(x -> x > addDays(first_day,7), days)) AS active_after_d7,
  round(avg(length(days)),2) AS avg_active_days
FROM (
  SELECT first_day, days, arrayJoin([('os', os), ('tier', tier), ('tier_onboarded', if(onb, tier, '_not_onboarded'))]) AS t
  FROM (
    SELECT person_id, min(toDate(timestamp)) AS first_day, groupUniqArray(toDate(timestamp)) AS days,
           toString(argMax(properties.$os, timestamp)) AS os,
           ifNull(nullIf(toString(argMax(person.properties.subscription_tier, timestamp)), ''), '(brak)') AS tier,
           countIf(event = 'onboarding_completed') > 0 AS onb
    FROM events WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received') GROUP BY person_id
  ) WHERE first_day >= toDate('2026-07-17') AND first_day <= today() - 8
)
GROUP BY dim, val ORDER BY dim, n DESC

-- @@ feature_stickiness_28d
SELECT feature, count() AS users, round(avg(fdays),2) AS avg_feature_days, countIf(fdays >= 3) AS users_3plus_days,
  countIf(fweeks >= 2) AS users_2plus_weeks, round(sum(fdays) / 28, 2) AS avg_daily_users, round(sum(fdays) / 28 / count(), 3) AS dau_over_28d_users,
  max(fevents) AS top1_events, sum(fevents) AS total_events
FROM (
  SELECT person_id, f AS feature, uniqExact(toDate(timestamp)) AS fdays, uniqExact(toStartOfWeek(timestamp, 1)) AS fweeks, count() AS fevents
  FROM events
  ARRAY JOIN if(multiIf(event IN ('voice_chat_started','first_conversation_started'), 'voice_chat', event IN ('reflect_message_submitted','reflect_thread_opened','reflect_mode_selected','reflect_entry_start_fresh','reflect_thread_resumed'), 'reflect', event IN ('habit_check_toggled','habit_created'), 'habits_action', event = 'habit_tracker_viewed', 'habits_view', event = 'workspace_opened', 'workspace', event = 'summary_viewed', 'summaries', event IN ('stat_opened') OR properties.$screen_name = 'firstWeekTrends', 'trends', event = 'recording_started', 'session_recording', event IN ('debrief_started','prep_card_started','between_session_started','health_check_started'), 'therapy_loop_flows', event = 'quick_capture_submitted', 'quick_capture', event = 'timeline_viewed', 'timeline_load', '') != '', [multiIf(event IN ('voice_chat_started','first_conversation_started'), 'voice_chat', event IN ('reflect_message_submitted','reflect_thread_opened','reflect_mode_selected','reflect_entry_start_fresh','reflect_thread_resumed'), 'reflect', event IN ('habit_check_toggled','habit_created'), 'habits_action', event = 'habit_tracker_viewed', 'habits_view', event = 'workspace_opened', 'workspace', event = 'summary_viewed', 'summaries', event IN ('stat_opened') OR properties.$screen_name = 'firstWeekTrends', 'trends', event = 'recording_started', 'session_recording', event IN ('debrief_started','prep_card_started','between_session_started','health_check_started'), 'therapy_loop_flows', event = 'quick_capture_submitted', 'quick_capture', event = 'timeline_viewed', 'timeline_load', ''), '_ANY_ACTIVE'], ['_ANY_ACTIVE']) AS f
  WHERE timestamp >= toDateTime('2026-09-17 00:00:00') AND timestamp < toDateTime('2026-10-15 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received')
  GROUP BY person_id, feature
) GROUP BY feature ORDER BY users DESC

-- @@ feature_use_vs_next_period_return
SELECT f AS feature, countIf(has(feats1, f)) AS users_p1, countIf(has(feats1, f) AND active2) AS returned_p2,
  countIf(NOT has(feats1, f)) AS nonusers_p1, countIf(NOT has(feats1, f) AND active2) AS nonusers_returned_p2
FROM (
  SELECT person_id, groupUniqArrayIf(multiIf(event IN ('voice_chat_started','first_conversation_started'), 'voice_chat', event IN ('reflect_message_submitted','reflect_thread_opened','reflect_mode_selected','reflect_entry_start_fresh','reflect_thread_resumed'), 'reflect', event IN ('habit_check_toggled','habit_created'), 'habits_action', event = 'habit_tracker_viewed', 'habits_view', event = 'workspace_opened', 'workspace', event = 'summary_viewed', 'summaries', event IN ('stat_opened') OR properties.$screen_name = 'firstWeekTrends', 'trends', event = 'recording_started', 'session_recording', event IN ('debrief_started','prep_card_started','between_session_started','health_check_started'), 'therapy_loop_flows', event = 'quick_capture_submitted', 'quick_capture', event = 'timeline_viewed', 'timeline_load', ''), timestamp < toDateTime('2026-10-01 00:00:00')) AS feats1,
         countIf(timestamp >= toDateTime('2026-10-01 00:00:00')) > 0 AS active2,
         countIf(timestamp < toDateTime('2026-10-01 00:00:00')) > 0 AS active1
  FROM events WHERE timestamp >= toDateTime('2026-09-17 00:00:00') AND timestamp < toDateTime('2026-10-15 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received')
  GROUP BY person_id
) ARRAY JOIN ['voice_chat','reflect','habits_action','habits_view','workspace','summaries','trends','session_recording','therapy_loop_flows','quick_capture','timeline_load'] AS f
WHERE active1
GROUP BY feature ORDER BY users_p1 DESC
```

### r6.sql

```sql
-- @@ strict_dau_wau_mau_weekly
SELECT toStartOfWeek(d, 1) AS wk, round(avg(dau),1) AS avg_dau, round(avg(wau),1) AS avg_wau, round(avg(mau),1) AS avg_mau, round(avg(dau)/avg(mau),3) AS dau_mau
FROM (
  SELECT addDays(day, n) AS d, uniqExactIf(person_id, n = 0) AS dau, uniqExactIf(person_id, n < 7) AS wau, uniqExact(person_id) AS mau
  FROM (SELECT DISTINCT person_id, toDate(timestamp) AS day FROM events WHERE timestamp >= now() - INTERVAL 125 DAY AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received','welcome_cta_tapped','signup_started','signup_method_selected','auth_method_tapped','auth_validation_failed','auth_mode_switched','login_failed','signup_failed','password_reset_requested','password_reset_failed','signup_email_verification_viewed','signup_email_verified','consent_screen_viewed','consent_granted','notification_permission_prompted','notification_permission_granted','notification_permission_denied','user_logged_in','user_logged_out') AND NOT startsWith(event, 'onboarding_') AND NOT (event IN ('$screen','tab_switched') AND properties.$screen_name IN ('splash','welcome','auth','signUp','forgotPassword','therapyOnboarding','wow')))
  ARRAY JOIN range(30) AS n
  GROUP BY d HAVING d >= today() - 90 AND d <= today() - 1
) GROUP BY wk ORDER BY wk

-- @@ strict_d_retention_pre_post
SELECT grp,
  countIf(first_day <= today() - 2) AS n_d1, countIf(first_day <= today() - 2 AND has(days, addDays(first_day,1))) AS d1,
  countIf(first_day <= today() - 8) AS n_d7, countIf(first_day <= today() - 8 AND arrayExists(x -> x > first_day AND x <= addDays(first_day,7), days)) AS d7_within,
  countIf(first_day <= today() - 31) AS n_d30, countIf(first_day <= today() - 31 AND arrayExists(x -> x > first_day AND x <= addDays(first_day,30), days)) AS d30_within,
  countIf(first_day <= today() - 31 AND arrayExists(x -> x >= addDays(first_day,23) AND x <= addDays(first_day,30), days)) AS d30_wk_window
FROM (
  SELECT person_id, min(toDate(timestamp)) AS first_day, groupUniqArray(toDate(timestamp)) AS days,
         multiIf(min(toDate(timestamp)) >= toDate('2026-10-03'), '3_post_1003',
                 min(toDate(timestamp)) >= toDate('2026-09-03'), '2_pre_0903_1002',
                 min(toDate(timestamp)) >= toDate('2026-07-17'), '1_pre_0717_0902', '0_older') AS grp
  FROM events WHERE timestamp >= toDateTime('2026-04-22 00:00:00') AND properties.$lib = 'posthog-flutter' AND properties.$is_testflight != true AND properties.$is_emulator != true AND properties.$device_model NOT IN ('OnePlus8Pro','Pixel 6 Pro') AND event NOT IN ('$identify','$set','$exception','client_error','notification_received','usage_snapshot','app_install_attributed','$create_alias','$groupidentify','$feature_flag_called','notification_banner_shown','$push_notification_received','welcome_cta_tapped','signup_started','signup_method_selected','auth_method_tapped','auth_validation_failed','auth_mode_switched','login_failed','signup_failed','password_reset_requested','password_reset_failed','signup_email_verification_viewed','signup_email_verified','consent_screen_viewed','consent_granted','notification_permission_prompted','notification_permission_granted','notification_permission_denied','user_logged_in','user_logged_out') AND NOT startsWith(event, 'onboarding_') AND NOT (event IN ('$screen','tab_switched') AND properties.$screen_name IN ('splash','welcome','auth','signUp','forgotPassword','therapyOnboarding','wow')) GROUP BY person_id
) WHERE grp != '0_older'
GROUP BY grp ORDER BY grp
```
