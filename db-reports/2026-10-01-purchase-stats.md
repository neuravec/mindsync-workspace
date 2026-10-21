# Statystyki zakupów MindSync (prod Postgres, read-only)

Data raportu: 2026-10-01
Źródło: Azure PostgreSQL (prod), dostęp przez `heroku run -a mindsync python` (run.6988, zatrzymany po odczycie), wyłącznie `SELECT`.
Tabele: `users`, `subscription_receipts`, `user_subscription`, `user_subscription_trial`, `user_promo_code`.

## Twarde ograniczenie na wstępie

W bazie **nie ma żadnej kolumny z kwotą, walutą ani środowiskiem (sandbox/production)** w `subscription_receipts` ani `user_subscription` (sprawdzone przez `information_schema.columns` filtrem po `amount`, `price`, `currency`, `environment`: zero wyników). To oznacza:

- **Nie da się policzyć przychodu w PLN/USD z danych** (tylko estymata po `product_sku`, patrz punkt 7).
- **Nie da się automatycznie odfiltrować TestFlight/sandbox** z `subscription_receipts` kolumną środowiska, bo jej nie ma. Jedyny dostępny sygnał jakości to `status` (VERIFIED/FAILED), który odróżnia udaną od nieudanej weryfikacji paragonu, ale nie odróżnia sandbox od produkcji. Zgodnie z wcześniejszym ustaleniem database-administrator (2026-08-18), TestFlight odnawia subskrypcje co 24h, więc wysoka liczba transakcji u jednego usera w krótkim okresie jest sygnałem ostrzegawczym, ale nie pewnikiem sandboxa.

## 1. Użytkownicy łącznie i nowi per miesiąc

**Łącznie userów: 1898**

Nowi userzy per miesiąc (ostatnie 13 miesięcy; wcześniejsza kohorta, sprzed września 2025, to 1898 - 1155 = **743 userów**, nieujętych w tabeli poniżej):

| Miesiąc | Nowi userzy |
|---|---|
| 2025-09 | 156 |
| 2025-10 | 69 |
| 2025-11 | 45 |
| 2025-12 | 44 |
| 2026-01 | 126 |
| 2026-02 | 120 |
| 2026-03 | 119 |
| 2026-04 | 97 |
| 2026-05 | 123 |
| 2026-06 | 80 |
| 2026-07 | 46 |
| 2026-08 | 65 |
| 2026-09 | 59 |
| 2026-10 (1 dzień) | 6 |

## 2. Ilu kiedykolwiek kupiło, ilu płaci dziś, konwersja

- **Unikalni userzy z co najmniej 1 paragonem w `subscription_receipts`: 45** (niezależnie od statusu VERIFIED/FAILED, to próby zakupu/weryfikacji).
- **Aktywna subskrypcja dziś (`user_subscription.is_active = true`): 26 userów łącznie**, ale tylko **8 z nich ma faktyczny paragon** w `subscription_receipts` (patrz tabela niżej, `granted_via`).
- **Konwersja user → kiedykolwiek próbował zapłacić: 45 / 1898 = 2,37%.**
- **Konwersja user → aktywny płatny dziś (tylko ci z realnym paragonem): 8 / 1898 = 0,42%.**

### Rozbicie aktywnych subskrypcji dziś wg `granted_via`

| granted_via | liczba aktywnych |
|---|---|
| signup_trial (auto 4-dniowy trial) | 15 |
| purchase (prawdziwy zakup) | 8 |
| promo | 2 |
| (null, sprzed wprowadzenia kolumny) | 1 |
| **razem** | **26** |

Czyli **tylko 8 z 26 "aktywnych premium" dziś to realni płacący (31%)**. Reszta to auto-trial, promo albo nieznane pochodzenie — zgodne z wcześniejszym ustaleniem (`project_signup_trial_premium_block_2026_08_17`), że auto-trial jest nieodróżnialny od prawdziwej subskrypcji bez przecięcia z `subscription_receipts`.

Jakość danych: 11 aktywnych subskrypcji ma `end_date` w przyszłości (> dziś+4 dni), 15 ma `end_date` w ciągu najbliższych 4 dni. Zero rekordów z `end_date` w przeszłości mimo `is_active=true` — brak sygnału "zombie aktywnych", dobry znak.

## 3. Oś czasu transakcji (wszystkie próby, VERIFIED + FAILED)

### Per miesiąc i platforma

| Miesiąc | Platforma | Transakcje |
|---|---|---|
| 2025-03 | apple | 2 |
| 2025-03 | google | 6 |
| 2025-04 | apple | 10 |
| 2025-05 | google | 1 |
| 2025-06 | google | 8 |
| 2025-07 | apple | 14 |
| 2025-07 | google | 8 |
| 2025-08 | google | 3 |
| 2025-09 | google | 7 |
| 2025-10 | google | 11 |
| 2025-11 | apple | 20 |
| 2025-11 | google | 2 |
| 2025-12 | google | 4 |
| 2026-01 | google | 1 |
| 2026-02 | apple | 6 |
| 2026-02 | google | 4 |
| 2026-03 | apple | 1 |
| 2026-03 | google | 3 |
| 2026-04 | google | 3 |
| 2026-05 | google | 1 |
| 2026-06 | google | 2 |
| 2026-07 | google | 2 |
| 2026-08 | apple | 1 |
| 2026-08 | google | 1 |
| 2026-09 | apple | 2 |
| 2026-09 | google | 1 |

**Razem: 124 wiersze w `subscription_receipts`** (62 VERIFIED, 62 FAILED — dokładnie po połowie, patrz punkt 8).

### Pierwszy zakup usera, per miesiąc (nowi płacący)

| Miesiąc pierwszego paragonu | Nowi płacący |
|---|---|
| 2025-03 | (nie liczony w tym zapytaniu, patrz oś wyżej) |
| 2025-04 | 4 |
| 2025-07 | 4 |
| 2025-08 | 1 |
| 2025-09 | 4 |
| 2025-10 | 9 |
| 2025-11 | 4 |
| 2025-12 | 4 |
| 2026-01 | 1 |
| 2026-02 | 2 |
| 2026-03 | 3 |
| 2026-04 | 1 |
| 2026-07 | 1 |
| 2026-08 | 2 |
| 2026-09 | 2 |

### Rozbicie produktów (wszystkie 124 paragony)

| Platforma | product_sku | liczba |
|---|---|---|
| apple | premium_m_01 | 47 |
| google | premium_m_01 | 32 |
| google | ms_starter_package | 30 |
| apple | premium_y_01 | 9 |
| google | premium_y_01 | 6 |

Uwaga jakościowa: `ms_starter_package` to 30 rekordów na Google, nazwa sugeruje inny/starszy produkt niż `premium_m_01`/`premium_y_01` — warto, żeby `backend-api` potwierdził, czy to wciąż aktywny SKU, czy relikt.

## 4. Cykliczność (recurring) i churn po pierwszym okresie

Liczona po liczbie paragonów na usera (VERIFIED + FAILED razem — patrz zastrzeżenie niżej):

| Liczba paragonów na usera | Liczba userów |
|---|---|
| 1 | 32 |
| 2 | 5 |
| 3 | 2 |
| 6 | 3 |
| 13 | 1 |
| 22 | 1 |
| 23 | 1 |
| **Razem unikalnych płacących** | **45** |

- **Cykliczni (≥2 paragony): 13 userów (13/45 = 29%).**
- **Jednorazowi (dokładnie 1 paragon): 32 userów (32/45 = 71%)** — to są kandydaci na "zapłacił i nie odnowił/anulował po 1. okresie", ALE uwaga niżej.

**Zastrzeżenie metodologiczne:** liczba paragonów na usera miesza próby VERIFIED i FAILED, a nie potwierdzone okresy rozliczeniowe. Dla userów z bardzo wysoką liczbą paragonów (22, 23, 13) w krótkim czasie — to niemal na pewno sygnatura **TestFlight/sandbox** (odnowienia co 24h), a nie 22-23 prawdziwych miesięcy subskrypcji. Nie da się tego mechanicznie odfiltrować (brak kolumny środowiska), więc **churn-po-pierwszym-okresie 71% jest zawyżony w dół (rzeczywisty churn wśród prawdziwych płatników jest prawdopodobnie inny) i wymaga review przez kogoś, kto zna te konkretne konta testowe**.

## 5. Lista płacących (zanonimizowana, hash MD5 user_id, pierwsze 200)

Pełna lista w surowym outpucie zapytania (nie publikowana w tym pliku w całości dla zwięzłości — dostępna na żądanie). Próbka skrajnych przypadków:

| hash usera | pierwszy zakup | platforma | liczba transakcji | ostatnia transakcja |
|---|---|---|---|---|
| 259e56a257 | 2025-04-22 | apple | 22 | 2026-02-21 |
| 72601ec0f9 | 2025-04-30 | apple | 23 | 2025-10-08 |
| 3eca57beec | 2025-11-28 | apple | 13 | 2025-11-29 |
| c1cf5af228 | 2025-03-25 | google | 6 | 2025-07-10 |
| b399eb2b6e | 2025-03-17 | apple | 3 | 2025-04-02 |

Trzy pierwsze (22, 23, 13 transakcji) — silny sygnał sandbox/TestFlight/konto testowe zespołu, nie realny użytkownik płacący 22-23 razy.

Pozostałe ~40 userów ma 1-6 transakcji w rozsądnych odstępach czasowych (tygodnie/miesiące) — bardziej prawdopodobne, że to realni płacący.

## 6. Trial

- **Userów z `had_trial = true`: 554** (z 1895 wierszy w `user_subscription_trial` — tabela ma rekord dla niemal każdego usera, nie tylko tych, co faktycznie mieli trial).
- **Trial → potem zapłacił (ma też wpis w `subscription_receipts`): 28 userów.**
- **Konwersja trial → płatny: 28 / 554 = 5,05%.**
- `trial_outcome` i `trial_platform`: **100% NULL na wszystkich 1895 wierszach** — kolumny istnieją, ale nigdy nie są zapisywane. To sygnał bugu zapisu (key-present-value-null), zgodny z wcześniejszym ustaleniem database-administrator (2026-09-12): `trial_outcome` 100% NULL. **Rekomendacja dla `backend-api`:** sprawdzić `app/services/subscription_service.py` / `_atomic_mark_trial_started` / `_atomic_mark_trial_ended` — czy warstwa zapisu faktycznie seta `trial_outcome`/`trial_platform`, bo dziś te pola nie niosą żadnej informacji mimo że istnieją w modelu.

## 7. Przychód — estymata (BEZ realnych kwot w bazie)

Baza nie przechowuje ceny ani waluty. Poniższa estymata zakłada orientacyjne ceny z App Store/Play (NIE zweryfikowane w tej sesji względem aktualnego cennika — operator/`integration-devops` powinien potwierdzić):

| Produkt | Przyjęta cena (orientacyjnie) | VERIFIED szt. | Estymowany przychód brutto |
|---|---|---|---|
| premium_m_01 (miesięczny) | ok. 9,99 USD/mies. (zgadywane) | nieznana liczba VERIFIED per SKU (nie liczone osobno w tej sesji) | **niepoliczalne wiarygodnie** |
| premium_y_01 (roczny) | ok. 59,99 USD/rok (zgadywane) | j.w. | **niepoliczalne wiarygodnie** |
| ms_starter_package | nieznana | j.w. | **niepoliczalne wiarygodnie** |

**Wniosek: nie podaję liczby przychodu — byłaby zmyślona.** Jeśli operator chce realny przychód, jedyne wiarygodne źródło to App Store Connect / Google Play Console (transaction reports), nie ta baza. Można to zlecić `growth-analyst`, który już wcześniej ustalił (`project_subscription_revenue_30d_2026_09_12`), że w oknie 30-dniowym były tylko 2 zweryfikowane paragony — ten raport teraz pokazuje szerszy, pełny obraz historyczny (124 paragony, 62 VERIFIED) i jest z nim spójny co do rzadkości realnych zakupów.

## 8. Uwagi o jakości danych

1. **Brak kolumny kwoty/waluty/środowiska** w `subscription_receipts` i `user_subscription` — patrz ograniczenie na wstępie.
2. **`order_id`**: Apple ma 0/56 wypełnionych (100% NULL), Google ma 42/68 wypełnionych (26 NULL). Brak duplikatów `order_id` między userami (sprawdzone, zero wyników) — nie ma sygnału nadużycia "jeden zakup na wielu kontach" po tym polu, ale dla Apple pole jest bezużyteczne.
3. **`platform_transaction_id`** (stabilny identyfikator transakcji, dodany w HIGH-001 2026-08-16): Google ma 68/68 wypełnione (100%), Apple ma tylko 3/56 (5%). To odwrotnie niż `order_id` — oznacza, że **pełne pokrycie identyfikatora transakcji istnieje tylko dla Google**, Apple w praktyce nie ma ani `order_id`, ani `platform_transaction_id` na większości rekordów. Rekomendacja dla `backend-api`: sprawdzić parsowanie `original_transaction_id` z odpowiedzi Apple verifyReceipt — czy faktycznie się nie udaje wyciągnąć, czy jest błąd w ścieżce zapisu.
4. **Status 50/50 VERIFIED/FAILED** (62/62) — wysoki odsetek FAILED (50%) jest zauważalny; może to być częściowo powtórzone próby weryfikacji tego samego zakupu (retry logic), a częściowo realne niepowodzenia. Nie badałem tego głębiej w tej sesji — warto, żeby `backend-api` sprawdził, czy FAILED-e grupują się u tych samych userów (retry) czy są rozproszone (realne niepowodzenia płatności).
5. **`trial_outcome`/`trial_platform` 100% NULL** mimo istnienia kolumn — patrz punkt 6, podejrzenie bugu zapisu.
6. **`user_subscription_trial` ma 1895 wierszy przy 1898 userach** — niemal każdy user dostaje wiersz w tej tabeli niezależnie od tego, czy faktycznie skorzystał z triala (stąd rozróżnienie `had_trial=true` jako jedyny wiarygodny filtr).
7. **Nie da się rozpoznać kont testowych zespołu** z samych danych w tym zapytaniu (nie czytałem e-maili — zgodnie z zasadami prywatności nie powinienem). Sygnał pośredni: userzy z 13-23 paragonami w `subscription_receipts` (patrz punkt 5) to najpewniejsi kandydaci na konta testowe/TestFlight, nie realni płatnicy.

## Lista wykonanych zapytań (wszystkie SELECT, bez mutacji)

Pełny REPL-safe skrypt uruchomiony przez `heroku run -a mindsync python < script.py` (run.6988, zatrzymany po odczycie `heroku ps:stop run.6988`):

- `SELECT count(*) FROM users`
- `SELECT to_char(created_at,'YYYY-MM'), count(*) FROM users WHERE created_at >= now() - interval '13 months' GROUP BY 1`
- `SELECT count(*) FROM subscription_receipts`
- `SELECT column_name, data_type FROM information_schema.columns WHERE table_name='subscription_receipts'`
- `SELECT platform, status, count(*) FROM subscription_receipts GROUP BY 1,2`
- `SELECT platform, product_sku, count(*) FROM subscription_receipts GROUP BY 1,2 ORDER BY 3 DESC`
- `SELECT count(DISTINCT user_id) FROM subscription_receipts`
- `SELECT to_char(created_at,'YYYY-MM'), platform, count(*) FROM subscription_receipts GROUP BY 1,2`
- pierwszy zakup per user, per miesiąc (subquery `min(created_at)` per `user_id`)
- rozkład liczby paragonów per user
- `order_id`/`platform_transaction_id` null-rate per platform
- duplikaty `order_id` cross-user
- `SELECT column_name, data_type FROM information_schema.columns WHERE table_name='user_subscription'`
- aktywne subskrypcje dziś, rozbicie po `granted_via`, przecięcie z `subscription_receipts`, rozkład `end_date`
- `SELECT column_name, data_type FROM information_schema.columns WHERE table_name='user_subscription_trial'`
- `had_trial`, `trial_outcome`, `trial_platform` rozkłady; trial→paid przecięcie
- `SELECT count(*) FROM user_promo_code`
- lista płacących (anonimizowana przez `md5(user_id)`, limit 200)
- userów z ≥2 paragonami
- sprawdzenie kolumn amount/price/currency/environment (zero wyników)

## Ograniczenia tego raportu

- Nie oszacowałem realnego przychodu w PLN/USD — dane do tego nie istnieją w tej bazie.
- Nie odfiltrowałem mechanicznie sandbox/TestFlight — brak kolumny środowiska; flagowałem tylko oczywiste przypadki (userzy z kilkunastoma+ paragonami).
- "Cykliczność" liczona po liczbie paragonów (VERIFIED+FAILED), nie po potwierdzonych okresach rozliczeniowych — realna liczba odnowień może być inna.
- Nie łączyłem z PostHog (platform/kampania akwizycji) — to osobne zapytanie dla `posthog-data-extractor`/`growth-analyst`, jeśli operator chce pełny obraz lejka.
