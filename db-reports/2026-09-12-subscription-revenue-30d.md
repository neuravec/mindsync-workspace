# Prawda o zakupach subskrypcji – ostatnie 30 dni (2026-08-13 .. 2026-09-12)

**Data raportu:** 2026-09-12
**Autor:** database-administrator
**Dostęp:** `heroku run -a mindsync python < skrypt.py` (run.3154), zapytania wyłącznie SELECT, `SET TRANSACTION READ ONLY`, dyno zatrzymany po odczycie (`heroku ps:stop run.3154`)
**Okno czasowe danych z bazy:** `now()` w momencie odczytu = 2026-09-12 10:44:41 UTC

## Odpowiedź wprost na pytanie operatora

**Czy były jakiekolwiek zakupy w ostatnich 30 dniach? TAK, ale tylko DWA.**

W oknie 2026-08-13 .. 2026-09-12 w tabeli `subscription_receipts` znajdują się dokładnie **2 zweryfikowane (status VERIFIED) paragony**, od **2 różnych użytkowników**:

| data (UTC) | platforma | product_sku | status | uwagi |
|---|---|---|---|---|
| 2026-08-19 05:32:45 | apple | premium_m_01 | VERIFIED | brak order_id (typowe dla Apple), platform_transaction_id obecny |
| 2026-09-07 15:06:39 | google | premium_m_01 | VERIFIED | order_id obecny, platform_transaction_id obecny |

To nie jest zero, ale to praktycznie szum: **2 zakupy na 1855 użytkowników i 158 nowych rejestracji w ostatnich ~12 tygodniach**. Nie ma w bazie kolumny z kwotą/ceną (patrz sekcja 1) – więc nie da się z DB policzyć przychodu w PLN/USD, tylko liczbę zdarzeń zakupowych.

**Nie da się jednoznacznie potwierdzić z bazy, że te 2 paragony to prawdziwe produkcyjne zakupy, a nie TestFlight/sandbox** – patrz sekcja 3, to jest twarde ograniczenie danych, nie moja interpretacja.

---

## 1. Rekonesans schematu (real prod, nie model)

Zapytanie:
```sql
SELECT table_name FROM information_schema.tables WHERE table_schema='public'
  AND table_name IN ('user_subscription','subscription_receipts','user_subscription_trial',
  'promo_code','user_promo_code','token_usage_log','model_pricing','users','conversations',
  'messages','user_profile');
```
Wszystkie 11 tabel istnieją na produkcji.

**`user_subscription`** (real kolumny, zgodne z modelem – potwierdzone wcześniej przez zespół 2026-08-18):
`id, user_id, subscription_type (enum: BASIC/PREMIUM), start_date (date), end_date (date), is_active (bool), granted_via (varchar(20), wartości: 'signup_trial' | 'promo' | 'purchase' | NULL)`

**`subscription_receipts`**:
`id, user_id, platform (varchar), product_sku (varchar), base64_receipt, purchase_token, order_id, purchase_time (bigint, ms – tylko Android), status (varchar: PENDING/VERIFIED/FAILED), created_at (timestamp BEZ strefy), platform_transaction_id (varchar)`

**Kluczowy fakt: w tej tabeli nie ma ŻADNEJ kolumny z kwotą/ceną/walutą ani kolumny środowiska (sandbox/production/TestFlight).** Nie da się z bazy odtworzyć przychodu w pieniądzu ani wprost odróżnić TestFlight od produkcji – to samo dotyczy potwierdzonej wcześniej luki (memory HI-001, 2026-08-16).

**`user_subscription_trial`**: `id, user_id, had_trial (bool), trial_started_at, trial_platform, trial_product_sku, trial_ended_at, trial_outcome (varchar: 'converted'/'expired' w teorii)`

**`promo_code`** / **`user_promo_code`**: standardowe, zgodne z modelem.

**`token_usage_log`** / **`model_pricing`**: zgodne z modelem, obie tabele NIE są puste (`model_pricing` ma 7 wierszy).

---

## 2. Zakupy w ostatnich 30 dniach – szczegóły

Zapytania (bez pokazywania user_id, zgodnie z zasadami prywatności):
```sql
SELECT created_at, platform, product_sku, status, purchase_time,
       (order_id IS NOT NULL), (platform_transaction_id IS NOT NULL)
FROM subscription_receipts
WHERE created_at >= '2026-08-13' AND created_at < '2026-09-13'
ORDER BY created_at;

SELECT platform, status, count(*) FROM subscription_receipts
WHERE created_at >= '2026-08-13' AND created_at < '2026-09-13' GROUP BY 1,2;

SELECT count(DISTINCT user_id) FROM subscription_receipts
WHERE created_at >= '2026-08-13' AND created_at < '2026-09-13';
```

Wynik: **2 wiersze, oba VERIFIED** (apple x1, google x1), **2 różnych użytkowników**. Zero PENDING, zero FAILED w tym oknie. Zero innych product_sku niż `premium_m_01` (czyli plan miesięczny – w bazie nie widać osobnego SKU rocznego wśród tych dwóch).

---

## 3. Prawdziwy przychód vs sandbox/TestFlight vs promo/granted

To jest sedno pytania operatora, więc rozpisuję wprost, co baza WIE i czego NIE WIE.

**Czego baza nie wie:** `subscription_receipts` nie ma kolumny środowiska. Apple `verifyReceipt` w kodzie backendu (`subscription_service.py`) przy statusie 21007 automatycznie próbuje ponownie pod adresem sandboxa i **zapisuje wynik do tej samej tabeli, w tym samym kształcie** – nie ma śladu, które API faktycznie zwróciło sukces. TestFlight korzysta z Apple sandbox, więc **paragon z TestFlight wygląda w tej tabeli identycznie jak paragon produkcyjny**. To potwierdzona wcześniej (memory: TestFlight sub-renewal audit 2026-08-18) charakterystyka: suby TestFlight odnawiają się co ~24h.

**Heurystyka, którą sprawdziłem:** jeśli TestFlight odnawia się co 24h, oczekiwałbym wielu paragonów Apple od tego samego użytkownika w krótkich odstępach.
```sql
SELECT dense_rank() OVER (ORDER BY user_id), count(*),
       EXTRACT(EPOCH FROM (max(created_at)-min(created_at)))/3600.0,
       ...
FROM subscription_receipts
WHERE platform='apple' AND created_at >= '2026-08-13' AND created_at < '2026-09-13'
GROUP BY user_id;
```
Wynik: **tylko 1 wiersz Apple w całym oknie, od 1 użytkownika, bez żadnej powtórki.** To NIE pasuje do wzorca "renewal co 24h" – ale jedna, izolowana weryfikacja też nie dowodzi produkcji: jeśli apka odpytuje/weryfikuje paragon tylko przy starcie aplikacji (a nie przy każdym renewal), to TestFlight-owy tester mógł wygenerować tylko 1 wiersz mimo cyklicznych odnowień w tle. **Wniosek: nie da się z tej bazy w 100% wykluczyć ani potwierdzić, że ten 1 zakup Apple to prawdziwy klient czy tester na TestFlight.** To jest jawne "nie wiem" wynikające z braku kolumny środowiska, a nie moja niechęć do odpowiedzi.

Paragon Google (09-07) ma `order_id` i `purchase_token` – Google Play nie ma odpowiednika "sandbox" w tym samym sensie co Apple (testerzy wewnętrzni Google Play generują realne, ale zerowe-kosztowo transakcje o odrębnych `order_id`; bez listy testerów/e-maili nie da się tego odróżnić w samej bazie).

**Rozdzielenie wg `granted_via`/`premium_source`** (kolumna istnieje od migracji `oo6p7q8r9s0t`/`pp7q8r9s0t1u`, 2026-08-17/18) – to jest jedyne pole w bazie, które NAPRAWDĘ rozdziela mechanizm nadania premium:

```sql
SELECT COALESCE(granted_via,'(null)'), subscription_type, is_active, count(*)
FROM user_subscription GROUP BY 1,2,3;
```

| granted_via | typ | is_active | liczba |
|---|---|---|---|
| (null) | BASIC | false | 645 |
| (null) | PREMIUM | false | 1116 |
| (null) | PREMIUM | **true** | 1 |
| promo | BASIC | false | 4 |
| promo | PREMIUM | false | 5 |
| promo | PREMIUM | **true** | 2 |
| purchase | PREMIUM | false | 30 |
| purchase | PREMIUM | **true** | 7 |
| signup_trial | PREMIUM | false | 34 |
| signup_trial | PREMIUM | **true** | 8 |

**Obecnie aktywne premium (18 kont) wg źródła:**
- `signup_trial` (darmowy 4-dniowy trial przy rejestracji, NIE jest przychodem): **8** (44%)
- `purchase` (realnie zweryfikowany zakup): **7** (39%)
- `promo` (kod promocyjny, rozdany): **2** (11%)
- `(null)` (sprzed wdrożenia kolumny, nieznane pochodzenie): **1** (6%)

Czyli **tylko 7 z 18 obecnie "premium" kont ma to premium z realnego zakupu** – reszta to trial albo promo. To jest dokładnie ten pomiar, o który prosił operator.

**Nowe wiersze `user_subscription` powstałe w ostatnich 30 dniach (wg `start_date`), wg mechanizmu:**
```sql
SELECT COALESCE(granted_via,'(null)'), count(*) FROM user_subscription
WHERE start_date >= '2026-08-13' AND start_date < '2026-09-13' GROUP BY 1;
```
| granted_via | liczba |
|---|---|
| signup_trial | 42 |
| (null) | 5 |
| promo | 1 |
| purchase | **1** |

Widać rozbieżność: w oknie 30-dniowym są **2 zweryfikowane paragony**, ale tylko **1 nowy wiersz `user_subscription` z granted_via='purchase'** i `start_date` w oknie. Najbardziej prawdopodobne wytłumaczenie (niepotwierdzone dodatkowym JOIN-em, bo wymagałoby to pokazania user_id): jeden z dwóch paragonów to nowy zakup (nowy wiersz), a drugi to odnowienie istniejącej, już aktywnej premium (aktualizuje tylko `end_date`, nie `start_date`, więc nie pojawia się jako "nowy" w tym zestawieniu). Nie traktuję tego jako pewnik – to interpretacja, nie zmierzony fakt.

---

## 4. Stan bazy użytkowników na dziś (2026-09-12)

```sql
SELECT count(*) FROM users;                                            -- 1855
SELECT count(*) FROM users u LEFT JOIN user_subscription s
  ON s.user_id=u.id WHERE s.id IS NULL;                                -- 3 (bez wiersza subskrypcji w ogóle)
SELECT subscription_type, is_active, count(*) FROM user_subscription
  GROUP BY 1,2;
```

| stan | liczba | % wszystkich (1855) |
|---|---|---|
| Total użytkowników | **1855** | 100% |
| Aktywne premium (`is_active=true`) | **18** | 0,97% |
| ...z tego realny zakup (`granted_via='purchase'`) | **7** | 0,38% |
| ...z tego darmowy trial (`granted_via='signup_trial'`) | **8** | 0,43% |
| ...z tego promo | **2** | 0,11% |
| ...z tego nieznane (null) | **1** | 0,05% |
| BASIC, nieaktywne | 645 | 34,8% |
| PREMIUM-typu, ale wygasłe (`is_active=false`) | 1185 | 63,9% |
| Brak wiersza `user_subscription` w ogóle | 3 | 0,16% |

**Uwaga interpretacyjna:** 1185 kont ma `subscription_type='PREMIUM'` ale `is_active=false` – to konta, które KIEDYŚ miały premium (trial/zakup/promo) i wygasło; job godzinowy (`deactivate_expired_subscriptions`) gasi `is_active`, ale nie cofa `subscription_type` do BASIC. Czyli **funkcjonalnie na "free" jest dziś 1837 z 1855 użytkowników (99,03%)**, dokładnie zgodnie z podejrzeniem operatora.

**Skala próbowania trialu:**
```sql
SELECT count(*) FILTER (WHERE had_trial=true), count(*) FROM user_subscription_trial;
```
554 z 1852 wierszy trialu ma `had_trial=true` (29,9% wszystkich użytkowników kiedykolwiek uruchomiło darmowy trial).

**Znalezisko – instrumentacja trial_outcome martwa:**
```sql
SELECT COALESCE(trial_outcome,'(null)'), count(*) FROM user_subscription_trial GROUP BY 1;
```
Wynik: **100% (1852/1852) wierszy ma `trial_outcome = NULL`.** Kolumna istnieje (dodana w ramach instrumentacji PostHog B12, ma przyjmować `'converted'`/`'expired'`), ale nigdy nie jest zapisywana. To klasyczny wzorzec "pole jest w payloadzie/schemacie, ale wartość nigdy nie ląduje" – nie interpretuję tego jako "użytkownicy nie konwertują", tylko jako **prawdopodobny brak zapisu w kodzie** (job godzinowy `deactivate_expired_subscriptions` albo ścieżka przy zakupie po trialu nie ustawia tej kolumny). Do zweryfikowania i naprawy przez `backend-api` – poza zakresem tego raportu, ale zgłaszam, bo to sygnał błędu zapisu, nie braku danych.

**`promo_code` / `user_promo_code`:** 17 aktywnych kodów, sumaryczny `used_count` z tabeli `promo_code` = 29, ale liczba faktycznych wierszy w `user_promo_code` (rejestr każdego wykorzystania) = 23 (2025-06-05 .. 2026-09-02), z czego **1 wykorzystanie w ostatnich 30 dniach**. Rozbieżność 29 vs 23 nie jest wyjaśniona w tym raporcie (drobna, niekrytyczna dla pytania o przychód).

---

## 5. Trend rejestracji – ostatnie 12 tygodni

```sql
SELECT date_trunc('week', created_at)::date, count(*) FROM users
WHERE created_at >= now() - interval '12 weeks' GROUP BY 1 ORDER BY 1;
```

| tydzień od | nowi użytkownicy |
|---|---|
| 2026-06-15 | 5 |
| 2026-06-22 | 18 |
| 2026-06-29 | 13 |
| 2026-07-06 | 12 |
| 2026-07-13 | 10 |
| 2026-07-20 | 8 |
| 2026-07-27 | 9 |
| 2026-08-03 | 25 |
| 2026-08-10 | 18 |
| 2026-08-17 | 13 |
| 2026-08-24 | 6 |
| 2026-08-31 | 8 |
| 2026-09-07 | 13 (tydzień niepełny – tylko 6 dni do 2026-09-12) |

Suma z 12 tygodni: **158 nowych rejestracji**, średnio ~13/tydzień, bez wyraźnego trendu wzrostowego ani spadkowego poza jednorazowym pikiem w tygodniu 2026-08-03 (25).

---

## 6. Aktywność transakcyjna z bazy (nie z PostHoga)

```sql
SELECT count(DISTINCT user_id) FROM conversations WHERE created_at >= now() - interval '7 days';   -- 9
SELECT count(DISTINCT user_id) FROM conversations WHERE created_at >= now() - interval '30 days';  -- 25
SELECT count(*) FROM (SELECT user_id FROM conversations GROUP BY user_id HAVING count(*)=1) t;     -- 360
SELECT count(*) FROM users u LEFT JOIN conversations c ON c.user_id=u.id WHERE c.id IS NULL;        -- 1259
SELECT count(*) FROM conversations;                                                                 -- 1765
```

| miara | liczba | % z 1855 |
|---|---|---|
| Użytkownicy z >=1 rozmową w ostatnich 7 dniach | 9 | 0,49% |
| Użytkownicy z >=1 rozmową w ostatnich 30 dniach | 25 | 1,35% |
| Użytkownicy z DOKŁADNIE 1 rozmową w całej historii | 360 | 19,4% wszystkich / **60,4% tych, którzy w ogóle kiedykolwiek zaczęli rozmowę** |
| Użytkownicy z 0 rozmów w całej historii | 1259 | **67,9%** |
| Rozmowy łącznie (cała historia) | 1765 | – |

To jest chyba najostrzejszy wynik w całym raporcie: **prawie 68% zarejestrowanych kont nigdy nie odbyło ani jednej rozmowy**, a w ostatnich 30 dniach jakąkolwiek rozmowę miało zaledwie **25 z 1855 kont (1,35%)**. Brak przychodu jest w pełni spójny z brakiem zaangażowania – to nie jest osobny problem, to ten sam problem widziany z dwóch stron.

---

## 7. Koszty AI (token_usage_log x model_pricing) – ostatnie 30 dni

Obie tabele istnieją i nie są puste (`model_pricing`: 7 wierszy cennika).

```sql
SELECT sum(cost_usd), count(*), count(DISTINCT user_id) FROM token_usage_log
WHERE created_at >= '2026-08-13' AND created_at < '2026-09-13';
```
**Suma kosztów AI za 30 dni: $112,13 USD**, 132 773 wpisów, 1826 unikalnych user_id.

Uwaga: 1826 użytkowników "z kosztem AI" vs tylko 25 użytkowników z realną rozmową w tym samym oknie (sekcja 6) – patrz rozbicie per feature niżej, to wyjaśnia rozbieżność.

**Koszt per model:**
| model | koszt USD | wiersze |
|---|---|---|
| gpt-5.4-mini | 112,110139 | 119 995 |
| text-embedding-3-small | 0,020431 | 12 720 |
| gpt-realtime-mini | 0,000000 | 10 |
| whisper-1 | 0,000000 | 48 |

`gpt-5.4-mini` to **99,98% całego kosztu AI**. `gpt-realtime-mini` i `whisper-1` pokazują koszt zaokrąglony do $0,000000 przy 6 miejscach po przecinku – albo koszt realnie jest znikomy, albo w `model_pricing` brakuje aktywnego wiersza cennika dla tych modeli w tym okresie; nie weryfikowałem zawartości `model_pricing` wiersz po wierszu w tym przebiegu (poza zliczeniem 7 wierszy) – to osobny, drobny follow-up, nie wpływa na wynik główny.

**Koszt per feature (TOP pozycje):**
| feature | koszt USD | wiersze |
|---|---|---|
| **NOTIFICATION** | **91,957657** | 106 789 |
| WEEKLY_SUMMARY | 11,879213 | 7 233 |
| MONTHLY_AUDIT | 4,698551 | 3 561 |
| REFLECT | 1,321952 | 1 321 |
| PERSONAL_BIO | 0,553111 | 289 |
| GOAL | 0,272855 | 993 |
| CHART_EXPLANATION | 0,302273 | 72 |
| RAG_INDEXING | 0,019344 | 11 174 |
| CONVERSATION | 0,072244 | 38 |
| (pozostałe, każde <0,1 USD) | ~0,7 łącznie | – |

**Fakt z bazy, bez interpretacji biznesowej wykraczającej poza dane:** feature `NOTIFICATION` odpowiada za **91,96 USD z 112,13 USD (82% całego 30-dniowego kosztu AI)**, przy 106 789 wpisach – to zdecydowanie największy koszt, znacznie większy niż koszt samych rozmów terapeutycznych (`CONVERSATION`: 0,07 USD / 38 wpisów) czy podsumowań. To tłumaczy, dlaczego 1826 (niemal cała baza) użytkowników ma jakiś koszt AI w 30 dniach, mimo że tylko 25 miało realną rozmowę – job generujący powiadomienia najwyraźniej działa dla większości/całej bazy niezależnie od aktywności.

**Koszt na "aktywnego" użytkownika – zależy od definicji:**
- $112,13 / 1826 (każdy z jakimkolwiek wpisem w token_usage_log) = **$0,061/użytkownika**
- $112,13 / 25 (użytkownicy z realną rozmową w 30 dniach, sekcja 6) = **$4,49/faktycznie aktywnego użytkownika**

Dla kontekstu (poza bazą, przybliżenie kursowe, NIE dane z DB): $112,13 USD to przy orientacyjnym kursie ~4 PLN/USD w okolicach ~450 zł – rząd wielkości zbliżony do budżetowanych przez operatora ~400 zł/mies. na modele AI.

---

## 8. Historia zakupów CAŁOŚCIOWO (czy zero w 30 dniach to anomalia czy norma)

```sql
SELECT platform, count(*), min(created_at), max(created_at)
FROM subscription_receipts WHERE status='VERIFIED' GROUP BY 1;
```
| platforma | zweryfikowane zakupy (cała historia) | pierwszy | ostatni |
|---|---|---|---|
| google | 48 | 2025-03-31 | 2026-09-07 |
| apple | 12 | 2025-04-02 | 2026-08-19 |

**Łącznie 60 zweryfikowanych zakupów w całej historii aplikacji, 122 wiersze paragonów łącznie (VERIFIED+FAILED+PENDING)** – zgodne z wcześniejszym audytem HI-001 z 2026-08-16 (wtedy 120 wierszy; przybyło dokładnie 2, czyli te same 2 z tego raportu – spójność potwierdzona).

**Rozkład miesięczny zweryfikowanych zakupów (ostatnie miesiące):**
| miesiąc | apple VERIFIED | google VERIFIED |
|---|---|---|
| 2025-10 | – | 11 |
| 2025-11 | 1 | 2 |
| 2025-12 | – | 4 |
| 2026-01 | – | 1 |
| 2026-02 | – | 1 |
| 2026-03 | 1 | 2 |
| 2026-04 | – | 2 |
| 2026-05 | – | 1 |
| 2026-06 | – | 1 |
| 2026-07 | – | 2 |
| 2026-08 | 1 | 1 |
| 2026-09 (do 12.) | – | 1 |

**Wniosek: ostatnie 30 dni (2 zakupy) NIE są anomalią w dół – to kontynuacja trendu, który trwa od co najmniej marca 2026.** Od marca 2026 żaden miesiąc nie miał więcej niż 3 zweryfikowane zakupy łącznie (apple+google). Jedyny wyraźny "dobry" okres to październik-listopad 2025 (11+2), prawdopodobnie kampania/promocja, ale to sprzed ~11 miesięcy. Od tamtej pory sprzedaż jest strukturalnie płaska, blisko zera – nie ma sensu szukać "co się zepsuło w ostatnim miesiącu", bo baza pokazuje, że to stan trwający od dawna.

**Obecnie aktywne premium z realnego zakupu (`granted_via='purchase'`, wszystkie, aktywne i wygasłe):** 37 kont (7 aktywnych + 30 wygasłych) – czyli spośród 60 zweryfikowanych zakupów w historii, dziś realnie płaci/ma aktywne premium z zakupu tylko 7 osób.

---

## Podsumowanie liczbowe (do raportu biznesowego)

- **Zakupy w ostatnich 30 dniach: 2** (1 Apple, 1 Google, oba plan miesięczny `premium_m_01`), od 2 różnych użytkowników. Nie zero, ale statystycznie nieistotne.
- **Nie da się z bazy potwierdzić, że oba te zakupy to produkcja, a nie TestFlight/sandbox** – brak kolumny środowiska w schemacie, to twarde ograniczenie danych.
- **Aktywne premium dziś: 18 z 1855 użytkowników (0,97%)**, z czego tylko **7 z realnego zakupu**, 8 z darmowego signup-trialu, 2 z promo, 1 nieznane pochodzenie (sprzed wdrożenia trackingu).
- **Funkcjonalnie na free jest 1837 z 1855 użytkowników (99,03%)** – potwierdza podejrzenie operatora.
- **67,9% wszystkich zarejestrowanych kont (1259/1855) nigdy nie odbyło ani jednej rozmowy w aplikacji**; w ostatnich 30 dniach jakąkolwiek rozmowę miało tylko 25 kont (1,35%).
- **Nowych rejestracji w ostatnich 12 tygodniach: 158** (~13/tydzień), bez wyraźnego trendu.
- **Koszt AI za 30 dni: 112,13 USD**, z czego **82% (91,96 USD) to feature NOTIFICATION** (nie rozmowy) – rzeczywisty koszt rozmów terapeutycznych to grosze (0,07 USD).
- **Historia: 60 zweryfikowanych zakupów łącznie od marca 2025**, sprzedaż płaska (1-3/miesiąc) od co najmniej marca 2026 – ostatni miesiąc nie jest anomalią, to trwały stan.
- **Nie da się policzyć przychodu w PLN/USD z bazy** – w `subscription_receipts` nie ma żadnej kolumny z kwotą.

## Otwarte pozycje / handoff

- **`backend-api` / `data-analytics`:** `user_subscription_trial.trial_outcome` jest NULL w 100% wierszy (1852/1852) mimo że kolumna istnieje pod instrumentację PostHog (B12) – prawdopodobny brak zapisu w kodzie przy konwersji/wygaśnięciu trialu. Do zdiagnozowania, poza zakresem tego raportu.
- **`backend-api`:** 3 konta użytkowników bez żadnego wiersza `user_subscription` – brzegowy przypadek, do sprawdzenia czy to celowe (np. konta w trakcie usuwania) czy luka w onboardingu.
- **Operator:** jeśli chce policzyć "prawdziwych klientów" z pominięciem swojego konta i znajomych testujących appkę, baza sama tego nie odróżni (brak flagi `is_test_account`/środowiska) – potrzebna lista e-maili/UID do wykluczenia, jeśli ma to sens dla dalszej analizy.
- **Integration-devops / backend-api:** rozważyć dodanie kolumny środowiska (sandbox/production) do `subscription_receipts` przy weryfikacji Apple – dziś to jedyny sposób, żeby przyszłe raporty przychodowe mogły w ogóle odróżnić TestFlight od realnej sprzedaży.
