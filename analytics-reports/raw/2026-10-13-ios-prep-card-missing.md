# Karta "Before therapy" po pierwszej rozmowie: iOS vs Android, surowy wyciąg z PostHoga

- **Data**: 2026-10-13 · **Agent**: posthog-data-extractor
- **Projekt**: PostHog EU 141170 · **Okno**: 2026-10-01 00:00 UTC -> 2026-10-13 ~15:50 UTC; "po fixie" = onboarding od 2026-10-11 20:40 UTC (m317)
- **Pytanie**: czy na iOS, po onboardingu nowego konta, karta przygotowania do terapii po pierwszej rozmowie się nie tworzy, a na Androidzie tak, i na którym kroku iOS odpada.
- **Weryfikacja zdarzeń**:
  - klient (`posthog-flutter`), płyną: `onboarding_completed`, `first_conversation_intro_viewed`, `first_conversation_started`, `first_conversation_ended` (props `mode`, `reached_open`, `started`), `first_conversation_recap_result` (prop `status`: ready/short), `post_onboarding_offer_shown`, `today_card_viewed`, `prep_card_opened` (props `source`, `processing_status`), `art9_consent_step_shown`/`art9_consent_declined` (nowe, pierwszy raz 2026-10-13 13:57, tylko iOS 2.0.110).
  - backend (`posthog-python`, bez `$os`/`$app_version`, ale z person_id): `reflect_session_ended` (prop `entry_origin=onboarding_first_conversation` = dowód, że POST `/reflect/{id}/end` dla pierwszej rozmowy doszedł i przeszedł do miejsca, gdzie kolejkuje się karta), `orca_memory_items_saved`, `consent_granted` (prop `consent_type`: ARTICLE9_HEALTH / PROFILING; klient wysyła `gdpr`), `api_error` (endpoint, status_code).
  - backend, ślepe: `prep_card_auto_generated` jest celowo bezosobowe (losowy distinct_id, security review H-1/M-1), więc nie da się go przypiąć do platformy ani osoby. W całej historii ma **zero** zdarzeń z `source=first_conversation`; tylko `auto_cron` (ostatnie 2026-10-11 17:48 UTC). `first_conversation_prep_card_outcome` **nigdy nie pojawiło się** w event_definitions. Wyniki crisis/short/not_in_therapy z założenia nie emitują nic.
  - brak zdarzeń cyklu życia aplikacji (Application Backgrounded/Opened itp.) w projekcie: nie da się sprawdzić "aplikacja w tle tuż po zakończeniu rozmowy".

## Wyniki

### 1. Lejek per platforma (osoby z `onboarding_completed`, klient flutter, okno wg pierwszego onboardingu)

| okno | OS | onboarding | intro | rozmowa start | rozmowa koniec (klient) | recap (dowolny) | recap ready | oferta | today_card_viewed | prep_card_opened |
|---|---|---|---|---|---|---|---|---|---|---|
| po fixie | Android | 4 | 3 | 3 | 3 | 3 | 2 | 3 | 1 | 1 |
| po fixie | iOS | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| przed fixem (10-01..10-11 20:40) | Android | 23 | 13 | 12 | 10 | 9 | 7 | 4 | 0 | 0 |
| przed fixem | iOS | 3 | 1 | 1 | 1 | 1 | 1 | 0 | 0 | 0 |

Wersje po fixie: Android 2.0.107 (3 os.), 2.0.109 (1); iOS 2.0.110 (1). Wszystkie segmenty n<25: to są pojedyncze przypadki, nie statystyka.

### 2. Kluczowy sygnał: zgoda ARTICLE9_HEALTH zapisana przez backend przed końcem rozmowy

| OS | wersja | onboarding | ART9 przed końcem 1. rozmowy | ART9 kiedykolwiek | 1. rozmowa zakończona |
|---|---|---|---|---|---|
| Android | 2.0.94 / 2.0.95 | 4 | 4 | 4 | 0 |
| Android | 2.0.97 / 2.0.100 / 2.0.103 | 7 | 1 | 1 | 3 |
| Android | 2.0.107 | 15 | 7 | 7 | 9 |
| Android | 2.0.109 | 1 | 1 | 1 | 1 |
| iOS | 2.0.94 / 2.0.97 / 2.0.110 | 4 | **0** | **0** | 2 |

Od 2026-10-01 **żadna** osoba onboardowana na iOS nie ma backendowego `consent_granted` z `consent_type=ARTICLE9_HEALTH`. Na Androidzie ma ją mniej więcej połowa. Osoba iOS po fixie dostała krok zgody ART9 dopiero na ekranie głównym, 2 min po rozmowie (`art9_consent_step_shown` 13:57:07), i go odrzuciła (`art9_consent_declined` 13:57:10). Docstring `_enqueue_first_conversation_prep_card` mówi: karta tylko dla osób w terapii **z zgodą Art. 9**.

### 3. Czy karta powstała: odpytywanie `GET /api/v1/prep-cards/latest` po końcu rozmowy (404 = brak karty)

| etykieta | OS / wersja | ART9 przed końcem | koniec 1. rozmowy (UTC) | 404 po końcu | ostatni 404 | prep_card_opened |
|---|---|---|---|---|---|---|
| AND-1 | Android 2.0.109 | tak (10:47:34) | 2026-10-12 10:49:56 | 1 (10:50:09), potem cisza mimo dalszego używania do 10-13 | 10-12 10:50:09 | 5 (timeline, completed) |
| AND-5 | Android 2.0.107 | tak | 2026-10-11 13:09:55 | 1 | 13:11:17 (koniec sesji) | 0 |
| AND-6 | Android 2.0.107 | tak | 2026-10-11 07:57:07 | 2 | 08:29:38 (koniec sesji) | 0 |
| AND-7 | Android 2.0.107 | tak | 2026-10-11 18:23:56 | 0 | brak (wyszedł 2 s po końcu) | 0 |
| AND-3 | Android 2.0.107 | nie | 2026-10-11 05:40:16 | 21 | 2026-10-11 19:17:37 | 0 |
| AND-2 | Android 2.0.107 | nie | 2026-10-09 23:20:02 (przed fixem) | 11 | 2026-10-12 13:54:41 | 0 |
| AND-4 | Android 2.0.107 | nie | 2026-10-12 18:16:49 | 4 | 18:23:10 (koniec sesji) | 0 |
| **iOS-A** | **iOS 2.0.110** | **nie** | **2026-10-13 13:54:58** | **26** | **2026-10-13 15:47:43 (~2 h, ciągle 404)** | 0 |
| iOS-B | iOS 2.0.97 | nie | 2026-10-05 08:35:10 (przed fixem) | n/d | 2026-10-11 16:37:41 | 0 |

Wzorzec: brak karty dłużej niż kilka minut występuje u osób **bez** zgody ART9, niezależnie od OS (AND-3, AND-2 też jej nie dostali). Jedyny pewny sukces (AND-1) miał ART9 zapisane w trakcie onboardingu.

### 4. Oś czasu iOS-A (2.0.110, po fixie), skrót

| UTC | zdarzenie | uwagi |
|---|---|---|
| 13:37:02 | signup_email_verified, onboarding_started | |
| 13:37:06 | consent_granted (klient, `gdpr`) | brak backendowego ARTICLE9_HEALTH w całym onboardingu |
| 13:37:50 | onboarding_completed | |
| 13:38:05 | first_conversation_intro_viewed | |
| 13:38:19 | mic_permission_result, reflect_session_started (backend, voice) | |
| 13:38:23 | first_conversation_started (voice) | |
| 13:54:58 | first_conversation_ended (voice, reason=user, reached_open=true) | |
| 13:54:59 | reflect_session_ended (backend, entry_origin=onboarding_first_conversation) | /end doszedł do backendu, bez api_error |
| 13:55:02 | orca_memory_items_saved (backend), first_conversation_recap_result=ready, post_onboarding_offer_shown | |
| 13:55:07-13:55:42 | paywall_shown -> paywall_dismissed | |
| 13:55:42 | mainPage, today_card_viewed (plan_active=true), GET prep-cards/latest **404** x2 | |
| 13:56-13:57 | kolejne prep-cards/latest 404, first_week_plan_toggled | |
| 13:57:07 | art9_consent_step_shown -> 13:57:10 art9_consent_declined | zgoda ART9 pytana dopiero tu, po rozmowie |
| 15:37-15:47 | powrót do aplikacji, timeline_viewed, kolejne prep-cards/latest 404 (łącznie 26 po końcu rozmowy) | karta nie powstała |
| 15:39:07 | voice_session_failed (webrtc_failure) | osobna sprawa |

Dla porównania AND-1 (Android 2.0.109): consent_granted ARTICLE9_HEALTH + PROFILING (backend) 10:47:34 w trakcie onboardingu -> rozmowa 10:48:33-10:49:56 -> reflect_session_ended 10:49:57 -> recap ready 10:49:59 -> ostatni 404 na prep-cards/latest 10:50:09 -> od 10:50:18 tylko 404 na debriefs/latest, prep-cards już nie -> prep_card_opened 10:51:47 (timeline, completed).

### 5. Błędy wokół zakończenia rozmowy

`api_error` od 2026-10-01 na endpointach /end, /close, /recap, /prep, /therapy, /reflect: brak błędów na `POST /reflect/{id}/end` w ogóle. Jedyny błąd /end to `POST /conversations/{id}/end` 409 (1 zdarzenie, 2026-10-01, stary czat). Reszta to oczekiwane 404 na `prep-cards/latest` (308 zdarzeń / 32 os.) i `users/therapy-context` (51 / 37), 403 na `reflect/{id}/session_data` (313 / 2 os., skew). `client_error` iOS: 4 zdarzenia / 1 os. w całym oknie.

## Wnioski ekstrakcyjne (interpretacja zostaje dla lead/backend)

- Spadek iOS **nie** leży po stronie klienta ani sieci: rozmowa kończy się, /end dochodzi do backendu (reflect_session_ended z entry_origin pierwszej rozmowy), recap jest `ready`, klient poprawnie odpytuje o kartę przez ~2 h. Karta po prostu nie istnieje (ciągłe 404).
- Najsilniejszy korelat to **brak zgody ARTICLE9_HEALTH zapisanej przed końcem rozmowy**: 0/4 osób iOS vs ~50% Androida. Ten sam objaw (ciągłe 404) mają też osoby z Androida bez ART9. To wygląda na różnicę w ścieżce zgody (iOS 2.0.110 pyta o ART9 dopiero na ekranie głównym po rozmowie), a nie na błąd generowania specyficzny dla iOS. To hipoteza do potwierdzenia w DB i w kodzie, nie dowód.
- Czy job w ogóle się zakolejkował/uruchomił, PostHog nie powie: telemetria joba pierwszej rozmowy nigdy nie dotarła (0 zdarzeń `source=first_conversation`, 0 `first_conversation_prep_card_outcome`, także dla udanego AND-1). Albo zdarzenia z tego joba giną (np. brak flush w procesie workera RQ), albo bramki odcinają wcześniej. Do sprawdzenia w logach `[FC-PREP]` i w DB.

## Zastrzeżenia

- Wszystkie segmenty n<25 (iOS po fixie = 1 osoba, prawdopodobnie konto testowe na TestFlight 2.0.110). Liczby są anegdotyczne; reguła k-anonimowości złagodzona tylko dla zliczeń kroków lejka produktowego w triage błędu, bez atrybutów zdrowotnych. Osoby opisane etykietami, bez identyfikatorów.
- Ingest od 2026-04-22 (nie dotyczy tego okna).
- `prep_card_auto_generated` i outcome są bezosobowe z założenia: brak podziału platformy po stronie backendu.
- Brak eventu sukcesu klienta "karta pokazana" poza `prep_card_opened` (wymaga tapnięcia) i `today_card_viewed` (nie mówi, czy karta była w środku). "Brak 404 po końcu" to pośredni sygnał istnienia karty i działa tylko, gdy użytkownik dalej korzysta z aplikacji.
- Zgoda ART9 mierzona backendowym `consent_granted`; jeśli zgoda bywa zapisywana inną ścieżką bez tego eventu, korelat będzie zawyżony. Prawdę ma tabela zgód w Postgresie.
- Osoby `posthog-flutter` z repeated onboarding przypisane do okna wg pierwszego `onboarding_completed`.

## Zapytania

```sql
-- @@ volumes_since_1001
SELECT event, properties.$os AS os, count() AS c, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events
WHERE timestamp >= toDateTime('2026-10-01 00:00:00') AND event IN ('onboarding_completed','first_conversation_intro_viewed','first_conversation_started','first_conversation_ended','first_conversation_recap_result','first_conversation_start_failed','first_conversation_connection_lost','prep_card_opened','today_card_viewed','prep_card_auto_generated','prep_card_created','post_onboarding_offer_shown','reflect_session_ended','orca_memory_items_saved','first_week_plan_failed')
GROUP BY event, os ORDER BY event, os LIMIT 100

-- @@ auto_generated_by_source_day
SELECT toDate(timestamp) AS d, properties.source AS source, properties.processing_status AS ps, count() AS c
FROM events WHERE event='prep_card_auto_generated' AND timestamp >= toDateTime('2026-10-01 00:00:00')
GROUP BY d, source, ps ORDER BY d LIMIT 100

-- @@ funnel_by_platform_window
WITH ob AS (
  SELECT person_id, argMin(properties.$os, timestamp) AS os, min(timestamp) AS ob_ts,
         if(min(timestamp) >= toDateTime('2026-10-11 20:40:00'), 'post_fix', 'pre_fix') AS win
  FROM events WHERE event='onboarding_completed' AND timestamp >= toDateTime('2026-10-01 00:00:00') AND properties.$lib='posthog-flutter'
  GROUP BY person_id
),
ev AS (
  SELECT person_id,
    minIf(timestamp, event='first_conversation_intro_viewed') AS intro_ts,
    minIf(timestamp, event='first_conversation_started') AS start_ts,
    minIf(timestamp, event='first_conversation_ended') AS end_ts,
    minIf(timestamp, event='first_conversation_recap_result') AS recap_ts,
    countIf(event='first_conversation_recap_result' AND properties.status='ready') AS recap_ready,
    minIf(timestamp, event='post_onboarding_offer_shown') AS offer_ts,
    minIf(timestamp, event='today_card_viewed') AS today_ts,
    minIf(timestamp, event='prep_card_opened') AS prep_open_ts,
    countIf(event='api_error') AS api_errs
  FROM events WHERE timestamp >= toDateTime('2026-10-01 00:00:00') GROUP BY person_id
)
SELECT ob.win, ob.os, count() AS onboarded,
  countIf(ev.intro_ts > toDateTime('2000-01-01')) AS intro,
  countIf(ev.start_ts > toDateTime('2000-01-01')) AS conv_started,
  countIf(ev.end_ts > toDateTime('2000-01-01')) AS conv_ended,
  countIf(ev.recap_ts > toDateTime('2000-01-01')) AS recap_any,
  countIf(ev.recap_ready > 0) AS recap_ready,
  countIf(ev.offer_ts > toDateTime('2000-01-01')) AS offer_shown,
  countIf(ev.today_ts > toDateTime('2000-01-01')) AS today_card_viewed,
  countIf(ev.prep_open_ts > toDateTime('2000-01-01')) AS prep_card_opened,
  countIf(ev.api_errs > 0) AS any_api_error
FROM ob LEFT JOIN ev ON ob.person_id = ev.person_id
GROUP BY ob.win, ob.os ORDER BY ob.win, ob.os

-- @@ art9_by_platform
SELECT os, ver, count() AS onboarded, countIf(art9_before_end > 0) AS art9_before_fc_end, countIf(art9_any > 0) AS art9_any, countIf(fc_end > toDateTime('2026-01-01')) AS fc_ended
FROM (
  SELECT person_id,
    argMinIf(properties.$os, timestamp, event='onboarding_completed' AND properties.$lib='posthog-flutter') AS os,
    argMinIf(properties.$app_version, timestamp, event='onboarding_completed' AND properties.$lib='posthog-flutter') AS ver,
    minIf(timestamp, event='onboarding_completed' AND properties.$lib='posthog-flutter') AS ob_ts,
    minIf(timestamp, event='first_conversation_ended') AS fc_end,
    countIf(event='consent_granted' AND toString(properties.consent_type)='ARTICLE9_HEALTH') AS art9_any,
    minIf(timestamp, event='consent_granted' AND toString(properties.consent_type)='ARTICLE9_HEALTH') AS art9_ts,
    if(art9_any > 0 AND (fc_end < toDateTime('2026-01-01') OR art9_ts <= fc_end), 1, 0) AS art9_before_end
  FROM events WHERE timestamp >= toDateTime('2026-10-01 00:00:00')
  GROUP BY person_id
) WHERE ob_ts > toDateTime('2026-01-01')
GROUP BY os, ver ORDER BY os, ver LIMIT 40

-- @@ latest404_after_end
SELECT pid, fc_end, n404_after, last_404 FROM (
SELECT e.person_id AS pid, f.fc_end AS fc_end,
  countIf(e.event='api_error' AND e.properties.endpoint='/api/v1/prep-cards/latest' AND e.timestamp > f.fc_end) AS n404_after,
  maxIf(e.timestamp, e.event='api_error' AND e.properties.endpoint='/api/v1/prep-cards/latest') AS last_404
FROM events e INNER JOIN (
  SELECT person_id, min(timestamp) AS fc_end FROM events WHERE event='first_conversation_ended' AND timestamp >= toDateTime('2026-10-11 00:00:00') GROUP BY person_id
) f ON e.person_id = f.person_id
WHERE e.timestamp >= toDateTime('2026-10-11 00:00:00')
GROUP BY pid, fc_end) ORDER BY fc_end LIMIT 20

-- @@ api_error_endpoints_reflect
SELECT properties.endpoint AS ep, properties.method AS m, properties.status_code AS sc, properties.error_class AS ec, count() AS c, count(DISTINCT person_id) AS users, min(timestamp), max(timestamp)
FROM events WHERE event='api_error' AND timestamp >= toDateTime('2026-10-01 00:00:00')
  AND (properties.endpoint ILIKE '%/end%' OR properties.endpoint ILIKE '%close%' OR properties.endpoint ILIKE '%recap%' OR properties.endpoint ILIKE '%prep%' OR properties.endpoint ILIKE '%therapy%' OR properties.endpoint ILIKE '%reflect%' OR properties.endpoint ILIKE '%first%')
GROUP BY ep, m, sc, ec ORDER BY c DESC LIMIT 40

-- @@ timeline (per osoba; person_id podstawiany lokalnie, nie w repo)
SELECT timestamp, event, properties.$os AS os, properties.$app_version AS ver, coalesce(toString(properties.$screen_name),'') AS screen,
  concat(coalesce(toString(properties.status),''),' ',coalesce(toString(properties.mode),''),' ',coalesce(toString(properties.source),''),' ',coalesce(toString(properties.processing_status),''),' ',coalesce(toString(properties.endpoint),''),' ',coalesce(toString(properties.status_code),''),' ',coalesce(toString(properties.reason),''),' ',coalesce(toString(properties.plan_active),'')) AS info
FROM events WHERE person_id = '<person_uuid>' AND timestamp BETWEEN toDateTime('<onboarding_start>') AND toDateTime('<end + 2h>')
  AND event NOT IN ('$set','$identify','tab_switched','$rageclick')
ORDER BY timestamp LIMIT 300
```


---

# Uzupełnienie 2026-10-13 (pytania lead po potwierdzeniu w DB)

Kontekst z DB (od lead): karta trafia do kolejki tylko przy zgodzie ART9 + `currently_in_therapy = yes_*` w chwili /end. Od 2026-08-01 zero rekordów ART9 na kontach iOS. 16 z 18 kont iOS od 10-01 nie ma wiersza `user_therapy_context`.

**Weryfikacja zdarzeń**: `onboarding_step_viewed` / `onboarding_step_completed` płyną (props `step_name`, `step_index`, `total_steps`, `outcome` saved/skipped; klucz to `outcome`, nie `step_outcome`). **`onboarding_step_save_failed` nie istnieje** w event_definitions (nigdy nie wysłane). Najbliższe zdarzenie to `onboarding_symptom_sync_failed` (95 zdarzeń / 2 os.), ale wyłącznie z Windows bez `$app_version`, więc nie pochodzi z aplikacji mobilnej. `art9_consent_step_shown`/`_declined` występują tylko na iOS 2.0.110.

## U1. Wersje iOS: App Store vs TestFlight (`$is_testflight`, od 2026-09-15)

| wersja iOS | TestFlight | osoby | pierwsze zdarzenie | ostatnie |
|---|---|---|---|---|
| 2.0.90 | nie (App Store) | 7 | 09-15 | 10-08 |
| 2.0.94 | nie (App Store) | 12 | 09-19 | 10-04 |
| 2.0.100 | nie (App Store) | 8 | 10-03 12:59 | 10-10 |
| 2.0.106 | nie (App Store) | 4 | 10-07 13:55 | 10-13 |
| 2.0.97..2.0.105, 2.0.108..2.0.110 | tak | po 1-2 | 10-03..10-13 | |

Wersje iOS osób aktywnych od 10-01 (ostatnia widziana wersja na osobę, klient): 2.0.100: 5, 2.0.94: 4, 2.0.106: 3, 2.0.90: 1, 2.0.109: 1, 2.0.110: 1, iPadOS 2.0.94: 1. Razem 16 osób iOS/iPadOS, na Androidzie około 146.

`onboarding_started` na iOS od 10-01: 2.0.94 (2 os.), 2.0.105 (2), po 1 osobie na 2.0.97, 2.0.100, 2.0.101, 2.0.102, 2.0.103, 2.0.104, 2.0.106, 2.0.108, 2.0.110. `onboarding_completed` na iOS: 2.0.94 (2), 2.0.105 (2), po 1 na 2.0.97, 2.0.101, 2.0.102, 2.0.103, 2.0.104, 2.0.108, 2.0.110. Na buildach App Store 2.0.100 i 2.0.106 onboarding zaczęło po 1 osobie i **nikt go nie skończył**. Cały onboarding na iOS po 10-03 przechodzą w praktyce 2-3 osoby testowe na kolejnych buildach TestFlight.

Odpowiedź na pytanie, czy iOS jest na buildzie sprzed kroku Journey/ART9: nie wprost. Kod buildów z App Store 2.0.100/2.0.106 już zawiera krok `journey` (indeks 3); widać go na TF 2.0.101+. Tyle że w PostHogu prawie nikt z App Store nie przechodzi onboardingu: PostHog widzi około 11 osób iOS z `onboarding_started` od 10-01, a w DB jest 18 kont iOS. Brak wiersza therapy_context u 16 z 18 pasuje do tego, że te osoby nie dochodzą do kroku journey albo w ogóle nie zaczynają onboardingu.

## U2. Krok Journey (`step_name='journey'`, `step_index=3`) per OS i wersja, od 2026-10-03

| OS | wersja | viewed (os.) | completed saved (os.) | completed skipped (os.) | total_steps przy completed |
|---|---|---|---|---|---|
| iOS | 2.0.101 / 102 / 103 / 104 / 108 (TF) | 1 każda | 1 każda | 0 | 5 |
| iOS | 2.0.105 (TF) | 2 | 2 | 0 | 5 |
| iOS | 2.0.110 (TF) | 1 | 0 | 1 (2 zdarzenia) | 5 |
| iOS | 2.0.100 / 2.0.106 (App Store) | 0 (doszli tylko do `intensity`) | 0 | 0 | |
| iOS | 2.0.94 (App Store, stary flow) | 1 | 1 (bez outcome) | | brak, dalej modality/schedule |
| Android | 2.0.100 | 7 | 5 (total 5), 3 (total 7) | 2 (total 5), 1 (total 7) | 5 i 7 |
| Android | 2.0.107 | 15 | 5 (total 5), 3 (total 7) | 7 (total 5) | 5 i 7 |
| Android | 2.0.97 / 103 / 106 / 108 / 109 | 1-2 | 1-2 (głównie total 7) | 0 | |

`outcome` w ostatnich 90 dniach: journey saved na Androidzie 32 zdarzenia / 17 os., skipped 12 / 9. Na iOS journey saved 11 zdarzeń / **2 os.**, skipped 2 / 1 os. (to iOS-A).

**Rozgałęzienie po Journey a ART9** (osoba = ostatnie ukończenie journey, od 10-03):

| OS | outcome | total_steps | osoby | z ART9 | widzieli `modality` |
|---|---|---|---|---|---|
| Android | saved | 5 | 9 | 5 | 0 |
| Android | saved | 7 | 6 | 5 | 6 |
| Android | skipped | 5 | 8 | 0 | 0 |
| Android | skipped | 7 | 1 | 1 | 1 |
| iOS | saved | 5 | 2 | 0 | 1 (stary build 2.0.94) |
| iOS | skipped | 5 | 1 | 1, ale z Home po rozmowie (zob. U3) | 0 |

`total_steps=7` oznacza gałąź "w terapii", w której pojawiają się `modality` i `schedule`. **Na iOS od 2.0.97 nikt nie trafił do gałęzi 7 kroków**. Obie osoby z `saved` miały `total_steps=5`: albo wybrały odpowiedź spoza terapii, albo gałąź się nie przełączyła. PostHog nie pokazuje wybranej odpowiedzi, bo jej wartość (słusznie) nie jest wysyłana.

**Kiedy Android zapisuje ART9**: przed backendowym `consent_granted ARTICLE9_HEALTH` ostatnim ukończonym krokiem onboardingu był `intensity` (12 os.) albo `lead_source` (1 os.). Na Androidzie zgoda ART9 zapisuje się więc przy kroku `intensity` (oceny objawów), **przed** Journey. Na iOS od 10-03 krok `intensity` ukończyły 4 osoby i żadna nie dostała ART9 w onboardingu (DB: zero od 08-01). Na Androidzie ART9 ma 12 z 25 takich osób.

## U3. `api_error` na zgodzie / profilu, od 2026-08-01

| endpoint | metoda | status | zdarzenia | osoby | od | do |
|---|---|---|---|---|---|---|
| /users/get_user_profile_and_subscription | GET | 404 | 232 | 128 | 08-01 | 10-13 |
| /users/therapy-context | GET | 404 | 159 | 134 | 08-01 | 10-13 |
| /users/get_user_profile_and_subscription | GET | 403 | 15 | 4 | 08-19 | 09-26 |
| /users/profile | POST | 500 | 14 | 5 | 08-18 | 10-05 |

Od 08-01 nie ma **ani jednego** `api_error` na `/users/consent/art9_health`, na żadnym innym endpoincie z `consent`/`art9` w nazwie ani na PUT profilu. `api_error` to zdarzenie backendowe bez `$os`, a skoro na zgodzie nie ma żadnego trafienia, nie było czego dzielić na platformy. Wniosek: na iOS żądanie zapisu ART9 w onboardingu najpewniej **w ogóle nie jest wysyłane**. Gdyby było wysyłane i odrzucane, widzielibyśmy błędy. Sama backendowa ścieżka zgody ART9 dla iOS działa: iOS-A dostał backendowe `consent_granted ARTICLE9_HEALTH` 2026-10-13 15:54:18. Stało się to po kolejnym pokazaniu kroku ART9 na Home (łącznie `art9_consent_step_shown` 7x, `declined` 6x), czyli już po pierwszej rozmowie i za późno na kartę.

## U4. Czy osoby iOS w ogóle widzą Journey

Tak. Od 2026-10-03 **4 osoby iOS** miały `onboarding_step_viewed step_name=journey` (TF 2.0.101-2.0.110 i stary 2.0.94). Osoby na buildach App Store 2.0.100 i 2.0.106 (po 1 os.) **nie doszły** do Journey, ich ostatnim krokiem był `intensity`. Żadna osoba iOS na buildzie nowszym niż 2.0.94 nie przeszła gałęzi "w terapii" (`modality`/`schedule`).

## Zastrzeżenia uzupełnienia

- Na iOS n = 2-4 osoby, w większości testerzy na TestFlight. To wskazówki, nie statystyka.
- Jedna osoba ma zdarzenia z iOS i z Androida (PostHog scalił ją po zalogowaniu na dwóch urządzeniach). OS przypisuję wg ostatniego zdarzenia kroku, więc jej ART9 może pochodzić z Androida.
- PostHog widzi mniej osób iOS (około 11 z `onboarding_started`) niż jest kont iOS w DB (18). Część kont nie wysyła zdarzeń onboardingu albo w ogóle go nie zaczyna. PostHog nie rozstrzyga, który z tych przypadków zachodzi.

## Zapytania uzupełnienia

```sql
-- @@ versions_active_since_1001
SELECT os, ver, count() AS users FROM (
  SELECT person_id, argMax(properties.$os, timestamp) AS os, argMax(properties.$app_version, timestamp) AS ver
  FROM events WHERE timestamp >= toDateTime('2026-10-01 00:00:00') AND properties.$lib='posthog-flutter' GROUP BY person_id
) GROUP BY os, ver ORDER BY os, ver LIMIT 80

-- @@ ios_testflight_by_version
SELECT properties.$app_version AS ver, toString(properties.$is_testflight) AS tf, count(DISTINCT person_id) AS users, min(timestamp) AS first_ts, max(timestamp) AS last_ts
FROM events WHERE timestamp >= toDateTime('2026-09-15 00:00:00') AND properties.$lib='posthog-flutter' AND properties.$os IN ('iOS','iPadOS')
GROUP BY ver, tf ORDER BY first_ts LIMIT 40

-- @@ step_names_by_os_ver
SELECT event, properties.$os AS os, properties.$app_version AS ver, toString(properties.step_index) AS idx, toString(properties.step_name) AS step, coalesce(toString(properties.outcome),'') AS outcome, coalesce(toString(properties.total_steps),'') AS total, count() AS c, count(DISTINCT person_id) AS users
FROM events WHERE timestamp >= toDateTime('2026-10-01 00:00:00') AND event IN ('onboarding_step_viewed','onboarding_step_completed') AND properties.$lib='posthog-flutter'
GROUP BY event, os, ver, idx, step, outcome, total ORDER BY os, ver, event, idx LIMIT 300

-- @@ journey_branch_vs_art9
SELECT os, journey_outcome, branch_total, count() AS persons, countIf(art9 > 0) AS with_art9, countIf(saw_modality > 0) AS saw_modality
FROM (
  SELECT person_id,
    argMaxIf(properties.$os, timestamp, event='onboarding_step_completed') AS os,
    argMaxIf(toString(properties.outcome), timestamp, event='onboarding_step_completed' AND toString(properties.step_name)='journey') AS journey_outcome,
    argMaxIf(toString(properties.total_steps), timestamp, event='onboarding_step_completed' AND toString(properties.step_name)='journey') AS branch_total,
    countIf(event='consent_granted' AND toString(properties.consent_type)='ARTICLE9_HEALTH') AS art9,
    countIf(event='onboarding_step_viewed' AND toString(properties.step_name)='modality') AS saw_modality,
    countIf(event='onboarding_step_completed' AND toString(properties.step_name)='journey') AS jc
  FROM events WHERE timestamp >= toDateTime('2026-10-03 00:00:00')
  GROUP BY person_id
) WHERE jc > 0
GROUP BY os, journey_outcome, branch_total ORDER BY os, journey_outcome, branch_total LIMIT 40

-- @@ step_before_art9
SELECT prev_step, count() AS c FROM (
  SELECT a.person_id AS pid, a.ts AS art9_ts, argMax(toString(s.properties.step_name), s.timestamp) AS prev_step
  FROM (SELECT person_id, min(timestamp) AS ts FROM events WHERE event='consent_granted' AND toString(properties.consent_type)='ARTICLE9_HEALTH' AND timestamp >= toDateTime('2026-10-03 00:00:00') GROUP BY person_id) a
  INNER JOIN (SELECT person_id, timestamp, properties FROM events WHERE event='onboarding_step_completed' AND timestamp >= toDateTime('2026-10-03 00:00:00')) s ON s.person_id = a.person_id
  WHERE s.timestamp <= a.ts
  GROUP BY pid, art9_ts
) GROUP BY prev_step LIMIT 20

-- @@ api_error_consent_profile
SELECT properties.endpoint AS ep, properties.method AS m, properties.status_code AS sc, count() AS c, count(DISTINCT person_id) AS users, min(timestamp), max(timestamp)
FROM events WHERE event='api_error' AND timestamp >= toDateTime('2026-08-01 00:00:00')
  AND (properties.endpoint ILIKE '%consent%' OR properties.endpoint ILIKE '%art9%' OR properties.endpoint ILIKE '%profile%' OR properties.endpoint ILIKE '%therapy-context%')
GROUP BY ep, m, sc ORDER BY c DESC LIMIT 40
```
