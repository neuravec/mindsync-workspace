# Efekt update'u z 27.06.2026 — Post-Release Health Check (PostHog) — Business Insight Report

- **Data**: 2026-06-29
- **Analityk**: growth-analyst
- **Pytanie biznesowe**: Co zmienił update aplikacji opublikowany w sobotę 2026-06-27 (build **2.0.60+133**) i czy coś się zepsuło / poprawiło w pierwszych ~2 dniach po wydaniu?
- **Okno danych**: BEFORE `2026-06-13 → 2026-06-26` (14 dni) vs AFTER `2026-06-27 → 2026-06-29` (2 pełne dni weekendu + 06-29 częściowy). Kontekst sięga 06-09.
- **Źródła**: PostHog (proj. 141170, EU) — HogQL przez REST query API (read-only, personal API key); `mindsync-frontend/.../pubspec.yaml` (wersja buildu). Postgres/`subscription_receipts` NIE odpytywane (rewolucja revenue drugorzędna dla okna 2-dniowego — patrz Rekomendacje).
- **Confidence**: **LOW** (ilość danych) / **HIGH** (wniosek metodyczny). Powód: realna baza aktywnych userów to ~3–13 dziennie na publicznym buildzie; 2 dni po wydaniu + weekend; nowy build jeszcze nie dotarł do publiczności. Większość liczb jest **kierunkowa, nie istotna statystycznie**.

---

## TL;DR

- **Nic się nie pali.** W pierwszych ~2 dniach po publikacji 2.0.60 nie ma w danych żadnej regresji o szerokim zasięgu: brak skoku crashy/errorów per-user, rejestracje i onboarding na poziomie wcześniejszych weekendów, zero nowych „twardych" błędów dotykających wielu userów.
- **Update jest praktycznie NIEWIDOCZNY w danych** — i to jest najważniejszy finding metodyczny. (1) Publiczność wciąż siedzi na **2.0.44** (App Store, 257 userów/30d); nowy build (rodzina 2.0.58/59/60) to ~**8–9 aktywnych userów dziennie** po 27.06, w większości testerzy. (2) Nowy build pojawił się w telemetrii **06-23/24, czyli PRZED 27.06** (TestFlight) — więc nie istnieje czysta granica „before/after" po dacie. Kalendarzowy podział 27.06 ≠ stary-build vs nowy-build.
- **Uwaga na fałszywy „spike" przed wydaniem**: skok DAU 06-21…06-25 (41–54 DAU) to **wewnętrzne QA** na buildach TestFlight 2.0.49–2.0.57 (40–52 testerów/dzień), a nie realny ruch. Liczenie tego jako „baseline before" zaniżyłoby efekt update'u.
- **Pozytywne (kierunkowo)**: dwa błędy, które update/migracje miały naprawić, **zniknęły po stronie eventów**: `503 ... /chunk` „store chunk" (12 → 0) — dokładnie błąd, który adresowała migracja recording-chunks→Postgres — oraz serwerowe `500` na endpointach głosowych (`between-sessions/voice` 27→0, `prep-cards/voice` 23→0). UWAGA: spadek jest częściowo wyjaśniony spadkiem użycia po QA, nie tylko fixem.
- **Czerwone flagi (niskie/średnie)**: (a) **`/users/notification-preferences` 500** utrzymuje się (14 przed, 13 po; 2 userzy, 06-28) — błąd PRE-ISTNIEJĄCY, nie z update'u; (b) garść NOWYCH-po-27 `404/403` na `/users/*` i `/gamification/orca_name`, ale każdy dotyczy 1–2 userów = szum pojedynczego testera, nie regresja masowa.
- **Krytyczny GAP instrumentacji**: nowy pipeline nagrań loguje **tylko `recording_chunked_upload_completed`** — brak eventów start/stop/upload/processing/saved/failed. Funnel nagrań sesji, o który prosi brief, **fizycznie nie da się zbudować z PostHog**. To blokuje odpowiedź „czy nagrywanie sesji jest teraz stabilniejsze".
- **Werdykt**: za wcześnie na ocenę efektu. Brak sygnałów do rollbacku/hotfixa. Następny rzetelny odczyt dopiero gdy 2.0.60 wejdzie do publiczności (~7–10 dni) — i dopiero PO dołożeniu eventów funnela nagrań.

---

## Identyfikacja update'u (które buildy = „update z 27.06")

`pubspec.yaml` = `version: 2.0.60+133`. Telemetria `$app_version` (ostatnie 30d):

| Build | first_seen | last_seen | unikalni userzy (30d) | Interpretacja |
|-------|-----------|-----------|----:|---|
| **2.0.44** | 2026-05-19 | 2026-06-28 | **257** | Publiczny build App Store — większość realnych userów |
| 2.0.49–2.0.57 | 06-02 … 06-26 | … | 8–10 każdy | Buildy TestFlight (QA), krótkożyjące |
| 2.0.58 | 06-23 | 06-28 | 7 | Precursor (session-rec fixy) |
| 2.0.59 | 06-23 | 06-28 | 20 | Precursor |
| **2.0.60** | 06-24 | **06-29** | **26** | „Update z 27.06" — jedyny aktywny 06-29 |

**Wniosek**: update = **2.0.60 (+133)**, wydany do App Store ~27.06; w TestFlight był u testerów już od 06-24. Stąd brak ostrej granicy 27.06 w danych i dominacja 2.0.44 po wydaniu (App Store review + staged rollout → adopcja opóźniona o dni/tygodnie; zgodne z `CLAUDE.md`: stare apki żyją tygodniami).

### Adopcja nowego buildu (dzienni unikalni userzy z client-eventów)

| Dzień | 2.0.44 (stary, publiczny) | rodzina 2.0.58/59/60 (nowy) | inne TestFlight (QA) |
|------|----:|----:|----:|
| 06-20 | 12 | 0 | 17 |
| 06-21 | 9 | 0 | 40 |
| 06-22 | 8 | 0 | 52 |
| 06-23 | 6 | 18 | 30 |
| 06-24 | 8 | 11 | 32 |
| 06-25 | 13 | 6 | 39 |
| 06-26 | 2 | 7 | 20 |
| **06-27** | 3 | **9** | 23 |
| **06-28** | 1 | **8** | 20 |
| 06-29 (część.) | 0 | 3 | 9 |

Czytanie: po 27.06 nowy build to ~8–9 userów/dzień — **ci sami testerzy co przed 27.06**. Publiczność (2.0.44) jeszcze nie zmigrowała. „DAU 40–54" w okolicy 21–25.06 to kolumna „inne TestFlight" = QA, nie rynek.

---

## Key Metrics — Before / After

Liczby surowe per-okno + per-dzień (bo okna mają różną długość). „After" liczone na 06-27/06-28 (2 pełne dni, weekend); 06-29 częściowy podany osobno gdzie istotne.

| Metryka | BEFORE 06-13…26 (14d) | per-dzień | AFTER 06-27…28 (2d, weekend) | per-dzień | Trend | Read |
|---|---:|---:|---:|---:|:--:|---|
| Rejestracje (`user_registered`) | 34 | 2.43 | 6 | 3.0 | → | OK — akwizycja stabilna |
| Onboarding start (userzy) | 31 | — | 3 | — | → | n za małe, brak zmiany |
| Onboarding completion % | 19/31 = **61%** | — | 2/3 = 67% | — | → | trzyma się (n=3 po — nieistotne) |
| Aktywacja: pierwsza notatka (debrief/prep/between, userzy) | 17 | 1.2 | 1 | 0.5 | ↓? | n=1 po = szum |
| `debrief_created` | 23 (cały 30d=23) | <1 | 0 | 0 | → | wolumen bazowo bliski zera |
| `reflect_message_sent` | spiky (45,62 = power users) | — | 1 | — | → | zdominowane przez 1–2 userów |
| api_error (zob. niżej) | dominują benign 404 | — | dominują benign 404 | — | → | wolumen ≈ funkcja użycia |
| Monetyzacja (`subscription_*`, `promo`) | screen 29 / selected 16 / **completed 4** | — | **0** | 0 | →* | *0 zakupów w 2.5 dnia weekendu = szum przy bazie 0.3/dzień |

### Weekend-do-weekendu (korekta sezonowości; Sob+Niedz)

| Para Sob/Niedz | Rejestracje | Onboarding start | Onboarding done | debrief_started | DAU (Sob/Niedz) |
|---|---:|---:|---:|---:|---|
| 06-13 / 06-14 | 5 | 3 | 3 | 4 | 24 / 30 |
| 06-20 / 06-21 | 7 | 7 | 4 | 5 | 24 / 41¹ |
| **06-27 / 06-28** | **6** | **3** | **2** | **1** | 26 / 22 |

¹ 06-21 zawyżone przez QA. **Czytanie**: rejestracje (6) i onboarding-start (3) post-update mieszczą się w paśmie wcześniejszych weekendów (5–7 / 3–7). `debrief_started` niżej (1 vs 4–5), ale przy n=1–5 to nie sygnał. **Brak weekendowego załamania core-usage po update.**

---

## Findings

### F1 — Update niemierzalny po 2 dniach; brak czystej granicy before/after · Impact: High (metodyczny) · Confidence: High
- **Evidence**: nowy build (2.0.58/59/60) first_seen 06-23/24 (przed 27.06); po 27.06 ~8–9 nowych-build userów/dzień, to ci sami testerzy; publiczność na 2.0.44 (257 userów/30d) niezmigrowana. Tabela adopcji wyżej.
- **So what**: każda interpretacja „efektu update'u" z kalendarzowego cięcia 27.06 jest myląca — porównujesz w większości starý build ze starým buildem, na tle weekendu, z zaszumieniem QA. Realny odczyt efektu wymaga (a) czasu na adopcję 2.0.60 i (b) cięcia po `app_version`, nie po dacie.

### F2 — `api_error` jest w 80%+ benign (404 „brak danych jeszcze"), nie błędami · Impact: Medium · Confidence: High
- **Evidence**: top api_error to `404` na endpointach `/latest`: `prep-cards/latest` 240→35, `health-check/latest` 141→34, `debriefs/latest` 121→39, `therapy-tracking/latest` 120→8, `<unmatched>` 219→22 (before→after). To oczekiwany pusty-stan (user nie ma jeszcze danego artefaktu). `api_error` = 2. najczęstszy event w projekcie (3535/30d) głównie przez te 404.
- **So what**: Dashboard „Health & Quality" jest zanieczyszczony — „error rate" rośnie wraz z liczbą nowych/aktywnych userów (więcej pustych-stanów), nie z jakością. Spadek tych 404 po 27.06 odzwierciedla niższe użycie, nie poprawę.

### F3 — Błędy, które update/migracje miały naprawić, zniknęły z eventów · Impact: Medium (pozytyw) · Confidence: Low/Medium
- **Evidence**: `/session-recordings/upload/{...}/chunk` **503** „store chunk": 12 (before) → **0** (after). Głosowe `500`: `between-sessions/voice` 27→0, `prep-cards/voice` 23→0, `debriefs/voice` 2→0. `recording_upload_failed`: 3 (≤06-21) → 0.
- **So what**: kierunek zgodny z intencją (chunks→Postgres usuwa 503 „Failed to store chunk to durable storage"; fixy głosówki usuwają 500). **ALE** confound: użycie nagrań/głosówki też spadło po QA, więc część spadku to mniejszy mianownik. Nie potwierdza jeszcze „naprawione", tylko „brak nawrotu przy niskim wolumenie".

### F4 — Pre-istniejący `500` na `/users/notification-preferences` · Impact: Medium · Confidence: High
- **Evidence**: 14 (before) i 13 (after); po 27.06 — 2 userów, wszystkie 06-28 w ~1h (10:52–11:50). Stały przed i po → **nie z update'u**.
- **So what**: realny błąd serwera (5xx) na zapisie preferencji powiadomień, niezależny od wydania. Do naprawy bez względu na update.

### F5 — Garść NOWYCH-po-27 `404/403`, ale 1–2 userów każdy = szum · Impact: Low · Confidence: Medium
- **Evidence**: `/users/preferences` 404 ×10 (2 userów, 06-28), `/users/profile` 404 ×3 (1 user), `/gamification/orca_name` 404 ×4 (1 user), `get_user_profile_and_subscription` 403 ×6 (1 user). `get_user_profile_and_subscription` 404 (13 before, 18 after, 7 userów) — to ta sama klasa „profil nie utworzony jeszcze" co /latest (race nowego usera), nie regresja.
- **So what**: pojedynczy tester eksplorujący nowy build potrafi wygenerować całość. Warto rzucić okiem w kodzie czy 2.0.60 nie woła `/users/preferences` (nowy route?) który 404-uje, ale to nie blokuje wydania.

### F6 — GAP: brak funnela nagrań sesji w PostHog (tylko completion) · Impact: High (blokuje pytanie z briefu) · Confidence: High
- **Evidence**: jedyny event nowego pipeline'u = `recording_chunked_upload_completed` (15 total, 4 userzy ever, last 06-27 19:01). Brak `*_started`, stop, `processing`, `saved`, `failed` dla v2. Stary pipeline (`recording_upload_started/completed/failed`) zamilkł po 06-22 (migracja).
- **So what**: nie da się zmierzyć „start→stop→upload→processing→saved/failed" ani wykryć „zaciętego Processing/Transcribing" — a to był rdzeń update'u. Health nagrań jest dziś nieobserwowalny analitycznie.

---

## Regresje / Red flags (sortowane po severity)

| Sev | Co | Dowód | Czy z update'u? | Akcja |
|---|---|---|---|---|
| **Med** | `/users/notification-preferences` **500** stały | 14 before / 13 after, 2 userzy 06-28 | **Nie** (pre-istniejący) | `backend-api`: zdebugować 500 na zapisie notif-prefs |
| **Med** | `api_error` zanieczyszczony benign 404 | top 404 na `/latest`, 3535 ev/30d | Nie | `flutter-mobile`/`data-analytics`: nie logować oczekiwanych 404 (`/latest`, profil-not-created) jako `api_error` lub tagować `expected:true` |
| **Low** | Nowe `404/403` na `/users/*`,`orca_name` po 27.06 | po 1–2 userów każdy | Możliwe (1 tester) | `backend-api`: sprawdzić czy 2.0.60 woła `/users/preferences` (route exists?) |
| **Low** | `client_error` (FirebaseAuthException) skupiony na nowych buildach | 2.0.59 ×13/2u, 2.0.60 ×9/4u + `_Exception` ×7/1u (06-27) | Niejasne, 1–4 userów | Obserwować po wzroście adopcji; teraz n za małe |
| **Info** | `reflect_limit_hit` 1191 ev / **2 userzy** (06-03…07) | 1 konto w pętli limitu | Nie (poza oknem) | `backend-api`: rate-limit/abuse guard; pominąć w metrykach |

**Brak findingu Critical/High-severity biznesowo.** Żaden sygnał nie uzasadnia rollbacku ani hotfixa.

---

## Pozytywne sygnały

- **Akwizycja stabilna**: rejestracje 6 w weekend po-update vs 5–7 w poprzednie weekendy; per-dzień 2.4–3.0 (bez zmian). Update nie zepsuł wejścia do lejka.
- **Onboarding completion ~61%** utrzymane (kontekstowo zdrowy poziom dla wielokrokowego onboardingu mental-health; pełny benchmark zewnętrzny = follow-up, nie zmyślam liczby).
- **Zniknięcie `503 /chunk` i głosowych `500`** (F3) — kierunek zgodny z celami migracji chunks→Postgres i fixów głosówki.
- **Pokrycie instrumentacją znacząco urosło** od kwietnia: realnie płynie ~81 eventów, w tym wcześniej brakujące `debrief_created`, `prep_card_created`, `between_session_created`, `user_registered`, `subscription_purchase_completed`, `therapy_context_updated`, `health_check_completed`. To zwiększa zdolność analityczną na przyszłe wydania.
- **Brak skoku crashy**: `client_error` pozostaje niski (głównie transient FirebaseAuth), bez nowej dominującej sygnatury wyjątku na 2.0.60 dotykającej wielu userów.

---

## Za wcześnie / potrzeba więcej danych

- **Efekt 2.0.60 na publiczność** — niemierzalny, póki App Store rollout nie przesunie userów z 2.0.44 (szac. ~7–10 dni). Powtórzyć analizę wtedy, cięcie po `app_version`.
- **Stabilność nagrań sesji** — niemierzalna bez funnela (F6). Najpierw instrumentacja, potem ocena.
- **Aktywacja/retencja świeżych kohort po update** — n=1–6 userów; retencja D1/D7 dla kohorty 27.06 wymaga 7+ dni i większej próby.
- **Monetyzacja** — 0 zdarzeń po 27.06 to przy bazie ~0.3 zakupu/dzień i weekendzie szum; revenue-truth (MRR, trial→paid, refundy) jest w Postgres `subscription_receipts`, nieodpytane (poza zakresem 2-dniowego okna).
- **„Stuck Transcribing/Processing"** — zgłaszane historycznie (patrz pamięć projektu), ale dziś niewidoczne, bo brak eventu stanu przetwarzania. Nieobserwowalne ≠ nieobecne.

---

## Rekomendacje (priorytet = impact × confidence × effort)

1. **Nie robić rollbacku/hotfixa na podstawie tych danych.** Brak regresji o szerokim zasięgu. Owner: lead. Miara: utrzymanie braku Critical/High w kolejnym odczycie.
2. **Domknąć funnel nagrań sesji v2 (NAJWYŻSZY priorytet analityczny).** Dodać eventy: `recording_started` (duration_bucket), `recording_stopped`, `recording_chunk_upload_failed` (error_type, http_status — w tym 503/Postgres), `recording_processing_started`, `recording_saved`/`recording_processing_failed`. Owner: **flutter-mobile** (klient) + **data-analytics**/`backend-api` (backend `session_recordings.py`). Miara: kompletny funnel start→saved widoczny w PostHog; oczekiwany efekt: możliwość wykrycia „stuck processing" i policzenia success-rate nagrań.
3. **Odszumić `api_error`.** Wykluczyć oczekiwane `404` (`/latest`, `get_user_profile_and_subscription` dla nowego usera) z `api_error` lub oznaczyć `properties.expected=true`. Owner: **flutter-mobile** (klient loguje api_error) + **data-analytics** (definicja w Health dashboard). Miara: spadek wolumenu `api_error` o ~70–80% przy zachowaniu realnych 4xx/5xx; „error rate" przestaje rosnąć z użyciem.
4. **Naprawić `500` na `/users/notification-preferences`.** Owner: **backend-api**. Miara: 0 × 5xx na tym endpoincie w 7 dni.
5. **Re-run tej analizy ~2026-07-07**, cięcie po `app_version` (2.0.44 vs 2.0.60), gdy adopcja 2.0.60 ≥ ~50 userów. Owner: growth-analyst. Miara: porównanie error-per-user, aktywacji i retencji D1/D7 stary vs nowy build na próbie ≥25/segment.
6. **Dołożyć brakujące eventy biznesowe**: `paywall_shown` (top lejka monetyzacji — dziś brak), `conversation_started/ended` (journaling nieinstrumentowany; płynie tylko `voice_chat_*`), `level_up`, `account_deleted` (sygnał churnu). Owner: **flutter-mobile** + **backend-api**/`data-analytics` wg taksonomii w `POSTHOG_ANALYTICS_PLAN.md`. Miara: lejek paywall→purchase i sygnały churnu stają się mierzalne.
7. **Dla twardego revenue-readu** (jeśli potrzebny): osobna analiza z Postgres `subscription_receipts` × `token_usage_log`×`model_pricing` (MRR, trial→paid, marża AI). Owner: growth-analyst. Nie dla okna 2-dniowego.

---

## Segmenty & kohorty

Cały zbiór jest small-n: realnie aktywni publiczni userzy to ~3–13/dzień (2.0.44), testerzy ~20–30/dzień rozproszeni po buildach. **Segmentacja po atrybutach wrażliwych (symptomy/scores) świadomie pominięta** — żaden taki segment nie zbliża się do progu 25 userów, raportowanie groziłoby re-identyfikacją. Najważniejsza „kohorta" to podział po `app_version` (stary 2.0.44 vs nowy 2.0.58–60), ale nowy-build segment ma <30 userów i jest zdominowany przez testerów — stąd brak twardych porównań per-segment w tym odczycie.

---

## Data Caveats & Confidence

- **Small-n na całej linii**: ~20–54 DAU (z czego duża część to web `$pageview` + testerzy QA). Wszystkie liczby **kierunkowe**, nie istotne statystycznie. Nie nadinterpretować spadków/wzrostów rzędu 1–5 zdarzeń.
- **Brak czystej granicy 27.06** (F1) + **zaszumienie QA 06-21…25** + **weekend 27/28** — trzy nakładające się confoundery. Korekta weekendowa zastosowana (tabela Sob/Niedz); QA oznaczone i wyłączone z „realnego baseline".
- **`api_error` ≠ błędy** (F2) — nie mylić wolumenu z jakością.
- **Spadki errorów (F3) częściowo = spadek użycia**, nie tylko fix. Correlation ≠ causation.
- **Brak funnela nagrań (F6)** — kluczowy obszar update'u jest nieobserwowalny; „brak błędów" = w dużej mierze „brak instrumentacji", nie dowód stabilności.
- **`app_version` jest property client-eventów**; eventy backendowe (`api_error`, `*_created`) nie noszą buildu → splitu po buildzie nie da się zrobić dla błędów serwerowych (użyto podziału po endpoint/status + czasie).
- **PostHog person-properties** (np. agregaty feature_used_*) nie użyte do kohort z powodu małej próby.
- **Revenue PostHog ≠ revenue-truth** — `subscription_purchase_completed` (4/14d) to za mało na MRR; prawda jest w Postgres receipts (nieodpytane).
- **Dostęp**: PostHog odpytany read-only przez REST query API z personal API key (MCP OAuth padał: `invalid_scope`, potem `No OAuth flow in progress` ×2 — opisane w Appendix). Scope ograniczony do `query:read` + odczyty; nie ruszono żadnego artefaktu PostHog.

---

## Appendix

### A. Instrumentacja — co FAKTYCZNIE płynie (wybór z 30d, 81 eventów)
Płyną m.in.: `$screen`, `api_error`(3535), `tab_switched`, `timeline_viewed`, `onboarding_*`, `therapy_context_updated`, `character_card_viewed`, `reflect_message_sent`, `symptom_scored`, `debrief_started/created/failed`, `between_session_started/created`, `prep_card_started/created`, `health_check_started/completed`, `user_registered/logged_in/out`, `profile_updated`, `subscription_screen_opened/product_selected/purchase_started/completed/failed`, `subscription_receipt_received`, `promo_code_applied`, `recording_upload_started/completed/failed`, **`recording_chunked_upload_completed`**, `voice_chat_started/ended`, `goal_created/status_changed`, `orca_named/color_changed`, `bio_refreshed`, `content_shared`, `client_error`, `inapp_insight.generated`(nowy 06-29).

**NIE płyną / brak** (gap): `paywall_shown`, `conversation_started/message_sent/ended`, `level_up`, `account_deleted`, `recording_*_started/processing/saved/failed` (v2 chunked), `prep_card_auto_generated`. Anomalia: `reflect_limit_hit` 1191 ev / 2 userzy.

### B. Główne zapytania (HogQL, read-only przez `/api/projects/141170/query/`)
```sql
-- 1) Taksonomia: co płynie (30d)
SELECT event, count() AS cnt, count(DISTINCT person_id) AS users,
       min(timestamp) AS first_seen, max(timestamp) AS last_seen
FROM events WHERE timestamp >= now() - INTERVAL 30 DAY
GROUP BY event ORDER BY cnt DESC LIMIT 200;

-- 2) Timeline buildów (identyfikacja update'u)
SELECT properties['$app_version'] AS v, min(timestamp) AS first_seen, max(timestamp) AS last_seen,
       count(DISTINCT person_id) AS users, count() AS cnt
FROM events WHERE timestamp >= now() - INTERVAL 30 DAY AND properties['$app_version'] != ''
GROUP BY v ORDER BY first_seen;

-- 3) Dzienna adopcja: stary 2.0.44 vs nowy 2.0.58/59/60 vs inne TF
SELECT toDate(timestamp) AS d,
  count(DISTINCT if(properties['$app_version']='2.0.44', person_id, NULL)) AS old_2044,
  count(DISTINCT if(properties['$app_version'] IN ('2.0.58','2.0.59','2.0.60'), person_id, NULL)) AS new_family,
  count(DISTINCT if(properties['$app_version'] NOT IN ('2.0.44','2.0.58','2.0.59','2.0.60')
                    AND properties['$app_version']!='', person_id, NULL)) AS other_tf
FROM events WHERE timestamp >= toDateTime('2026-06-20 00:00:00') AND properties['$app_version']!=''
GROUP BY d ORDER BY d;

-- 4) api_error po endpoint+status, before vs after 27.06
SELECT properties.endpoint AS endpoint, properties.status_code AS status,
  countIf(timestamp < toDateTime('2026-06-27 00:00:00')) AS before_14d,
  countIf(timestamp >= toDateTime('2026-06-27 00:00:00')) AS after_3d
FROM events WHERE event='api_error' AND timestamp >= toDateTime('2026-06-13 00:00:00')
GROUP BY endpoint, status ORDER BY after_3d DESC, before_14d DESC LIMIT 35;

-- 5) Dzienna tabela health/recording (api_error, client_error, debrief_failed, rec_*)
-- 6) Onboarding/activation before/after; 7) Recording events before/after;
-- 8) Monetyzacja before/after; 9) client_error po buildzie.
-- (pełne treści jak w przebiegu sesji)
```

### C. Definicje
- **BEFORE** = `2026-06-13…06-26`; **AFTER** = `2026-06-27…06-29` (06-27/28 = pełny weekend, 06-29 częściowy).
- **„Update z 27.06"** = build 2.0.60+133 (App Store ~27.06; w TestFlight od 06-24).
- **Aktywacja** = pierwsza notatka terapeutyczna (`debrief_created` ∨ `prep_card_created` ∨ `between_session_created`).
- **Benign 404** = oczekiwany pusty-stan (`/latest`, profil nowego usera) logowany jako `api_error`.

### D. Nota o dostępie (dla powtarzalności)
MCP PostHog OAuth nie zadziałał w tej sesji: pełny scope pluginu → `invalid_scope`; po zawężeniu do read-only scope autoryzacja przechodziła, ale `complete_authentication` 2× zwracał `No OAuth flow is in progress` (stan pending-flow wygasał między turami). Fallback: bezpośrednie HogQL przez REST query API z `POSTHOG_PERSONAL_API_KEY` (z `MindSync/.env`, wartość nigdy nie wypisana), host `POSTHOG_HOST`, projekt `POSTHOG_PROJECT_ID=141170`. Wyłącznie odczyty; zero mutacji.
```
```
