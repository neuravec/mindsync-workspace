# Dlaczego MindSync nie zarabia – diagnoza retencji, monetyzacji i kierunku produktu

- **Data**: 2026-09-12
- **Analityk**: growth-analyst
- **Pytanie biznesowe**: Czy MindSync nie zarabia dlatego, że ma źle ustawiony paywall i ludzie zostają na free, czy dlatego, że produkt nie utrzymuje użytkowników na tyle długo, by monetyzacja miała na czym stanąć?
- **Okno danych**: 2026-08-13 .. 2026-09-12 (30 dni), kohorty 12-13 tygodni wstecz, historia zakupów od 2025-03-31
- **Źródła**: `db-reports/2026-09-12-subscription-revenue-30d.md` (prod Postgres, read-only) · `analytics-reports/raw/2026-09-12-usage-retention-monetization-extract.md` (PostHog EU 141170) · benchmarki zewnętrzne (linki w sekcji 9)
- **Pewność**: **Wysoka** co do diagnozy kierunkowej (dwa niezależne źródła dają ten sam obraz w czterech różnych pomiarach), **niska** co do dokładnych kwot przychodu (baza nie przechowuje kwoty ani środowiska transakcji)

---

## 1. Odpowiedź na pytanie operatora, w trzech zdaniach

**To nie jest problem paywalla. To jest problem retencji, a dokładniej pierwszych 48 godzin.**

1. Paywall obsługuje ruch, którego nie ma: w 30 dni ekran subskrypcji otworzyło **15 osób ze 127 realnie aktywnych**, a 5 z 7 wyświetleń paywalla pochodziło z menu i ustawień, czyli od ludzi, którzy sami poszli go szukać, a nie od kogoś, kto odbił się od limitu.
2. Najmocniejszy dowód, że to nie cena i nie bramka: spośród **37 kont, które kiedykolwiek realnie ZAPŁACIŁY**, dziś ma aktywne premium **7 (19%)** – czyli ludzie, którzy już przeszli przez paywall i wyjęli pieniądze, też odchodzą, więc naprawianie paywalla naprawia coś, co nie jest zepsute.
3. Zepsute jest to, co dzieje się zaraz po instalacji: **D1 = 7,5%, D7 = 4,0%, D30 = 0,8% (2 osoby z 244)**, 68,5% aktywnych ma w miesiącu tylko jeden aktywny dzień, a 67,9% wszystkich kont (1259 z 1855) nigdy nie odbyło ani jednej rozmowy.

Twoja obawa "ludzie korzystają tylko z wersji free" jest w połowie trafna i w połowie myląca. Owszem, 99,03% bazy jest funkcjonalnie na free. Ale oni nie "korzystają z free" – oni w większości nie korzystają wcale. Free nie jest konkurencją dla premium. Konkurencją dla premium jest brak otwarcia aplikacji.

Twoja druga obawa, "zły kierunek rozwoju", też jest częściowo trafna, ale nie tak, jak myślisz. Kierunek nie jest głupi. On ma **złą częstotliwość** – o tym sekcja 4.

---

## 2. Kluczowe metryki na dziś

| Metryka | Wartość | Benchmark zewnętrzny | Odczyt |
|---|---|---|---|
| Konta ogółem | 1855 | – | – |
| MAU (realnie otwierający apkę, 30d) | **127** | – | 6,8% bazy kont |
| Konta "dotykane" przez backend (crony) | 1874 | – | **14,8x więcej niż MAU** |
| D1 retencja | **7,5%** (24/319) | ~26-35% (health/fitness) | krytycznie źle |
| D7 retencja | **4,0%** (12/303) | ~15-20% (fitness) | krytycznie źle |
| D30 retencja | **0,8%** (2/244) | ~4% mediana wszystkich kategorii | krytycznie źle |
| One-and-done (90d) | **66,2%** (253/382) | – | krytycznie źle |
| Jeden aktywny dzień w miesiącu | **68,5%** (87/127) | – | potwierdza powyższe |
| Ukończenie onboardingu | **76,7%** (43→33) | – | **dobrze, nie ruszać** |
| Stickiness (DAU/WAU) | 26-31% | – | dobrze dla tego, co zostaje |
| Konta bez ani jednej rozmowy | **67,9%** (1259/1855) | – | krytycznie źle |
| Aktywne premium | 18 / 1855 = 0,97% | freemium: 2,2% mediana download→paid | poniżej mediany |
| ...z tego realny zakup | **7 / 1855 = 0,38%** | – | poniżej dolnego kwartyla |
| Zakupy w 30 dniach | **2** | – | norma od marca 2026, nie anomalia |
| Zakupy łącznie od 03.2025 | 60 | – | płaskie 1-3/mies od pół roku |
| Retencja płacących | **7 z 37 kont z zakupem = 18,9%** | – | **to jest najważniejsza liczba w raporcie** |
| Open rate powiadomień | **1,4%** (26/1815 odbiorców) | ~7,8% średnia, 14,2% health/iOS | 5-10x poniżej rynku |
| Koszt AI 30d | 112,13 USD ≈ 449 zł | – | – |
| ...z tego treść generowana dla nieaktywnych | **108,54 USD = 96,8%** | – | **największy wyciek** |
| Nowe rejestracje | ~13/tydzień, bez trendu | – | stabilnie nisko |

---

## 3. Jednostkowa ekonomia: ile to naprawdę kosztuje na głowę

### 3.1 Koszty zweryfikowane

Twoje szacunki są bliskie prawdy. Zmierzony koszt AI z `token_usage_log` × `model_pricing` za 30 dni to **112,13 USD**, czyli przy kursie ~4 PLN/USD około **449 zł** wobec Twoich 400 zł. Reszta pozostaje Twoim szacunkiem, bo nie mam dostępu do faktur.

| Pozycja | Kwota/mies. | Źródło |
|---|---|---|
| Modele AI | **449 zł** (112,13 USD) | zmierzone, Postgres |
| Heroku (infra) | ~200 zł | szacunek operatora, niezweryfikowany |
| Loops (e-mail) | ~180 zł | szacunek operatora, niezweryfikowany |
| **Razem** | **~830 zł/mies.** | |

### 3.2 Koszt na głowę

| Podzielone przez | Liczba | Koszt/mies. |
|---|---|---|
| Wszystkie konta | 1855 | 0,45 zł |
| **MAU (realnie otwiera apkę)** | **127** | **6,53 zł** |
| Konta z realną rozmową w 30d | 25 | 33,16 zł |
| **Płacący (realny zakup, aktywni)** | **7** | **118,43 zł** |

Przeczytaj ostatni wiersz jeszcze raz. **Każdy z 7 płacących kosztuje Cię 118 zł miesięcznie**, a płaci prawdopodobnie 14-35 zł netto. To nie jest "niska marża", to jest ujemna marża rzędu minus 300-800%.

### 3.3 Ile subskrypcji na break-even

**Nie wiem, ile kosztuje `premium_m_01`, bo tabela `subscription_receipts` nie ma kolumny z kwotą ani walutą.** To trzeba odczytać z App Store Connect i Google Play Console (5 minut roboty) i podstawić do tabeli poniżej. Liczę netto dla wydawcy jako `cena_brutto / 1,23 × (1 - prowizja)`: sklep pobiera VAT 23%, potem prowizję 15% (program dla małych wydawców, przy Twoim obrocie niemal na pewno się kwalifikujesz) albo 30% (standard).

| Cena mies. brutto | Netto @15% | Netto @30% | **Subskrypcji na break-even @830 zł, 15%** | @830 zł, 30% | Po cięciu kosztów do ~450 zł, 15% |
|---|---|---|---|---|---|
| 19,99 zł | 13,81 zł | 11,38 zł | **61** | 73 | 33 |
| 29,99 zł | 20,73 zł | 17,07 zł | **41** | 49 | 22 |
| 39,99 zł | 27,64 zł | 22,76 zł | **31** | 37 | 17 |
| 49,99 zł | 34,55 zł | 28,45 zł | **25** | 30 | 13 |

Masz **7**. W zależności od ceny brakuje Ci **od 18 do 54 subskrypcji**, czyli trzeba pomnożyć obecną liczbę płacących przez **3,6 do 8,7 razy**.

### 3.4 Dlaczego tego nie da się nadrobić ruchem (najważniejsza liczba w tej sekcji)

Przy obecnej konwersji 0,38% bazy kont na aktywnego płacącego:

- żeby mieć **31 płacących** (break-even przy 39,99 zł), potrzeba **8158 kont** – czyli +6300 rejestracji, przy 13/tydzień to **9,3 roku**;
- żeby mieć **61 płacących** (break-even przy 19,99 zł), potrzeba **16 000 kont** – czyli **19 lat**.

Patrząc od drugiej strony: przy 127 MAU break-even przy 39,99 zł wymaga, żeby **24,4% wszystkich aktywnych użytkowników płaciło**. Benchmark dla freemium to 2,2% mediana download→paid, a górne 25% produktów robi 10-15%. Nawet gdybyś był w najlepszym kwartylu świata, przy 127 MAU nie osiągniesz break-even.

**Wniosek ekonomiczny jest jednoznaczny i nie zależy od tego, jaką cenę wstawisz w tabelę:** przy tej skali monetyzacja nie jest dźwignią. Dźwigniami są dwie i tylko dwie:

1. **Ciąć koszty** (natychmiastowe, pewne, bez ryzyka produktowego) – sekcja 7, koszyk NATYCHMIAST. Zbija break-even z 31 do 17 subskrypcji.
2. **Naprawić retencję, żeby MAU urosło z 127** (wolne, niepewne, ale to jedyna droga do dodatniego wyniku). Przy kosztach 450 zł i realistycznej konwersji 3% MAU break-even wypada przy **~560 MAU**, czyli 4,4x obecnego stanu.

I tu jest pointa: **MAU nie urośnie przez akwizycję, bo wiadro przecieka**. Do apki wchodzi ~25 nowych osób/tydzień (~108/mies.), a MAU wynosi 127, co oznacza średni czas życia użytkownika około **1,2 miesiąca**. Żeby dojść do 560 MAU przy tym samym napływie, średni czas życia musiałby urosnąć do ~5,2 miesiąca. Alternatywnie musiałbyś dosypać 4,2x więcej instalacji przy niezmienionej retencji, co kosztuje pieniądze, których nie masz, i spali je dokładnie tak samo.

---

## 4. Gdzie NAPRAWDĘ jest dziurawy lejek

### 4.1 Teza do sprawdzenia: onboarding działa, więc problem jest po nim

**Teza BRONI SIĘ.** Onboarding kończy 76,7% osób (43 start → 33 koniec), ma 9 kroków, a drop-off między krokami jest minimalny: `challenges` 32→29, `intensity` 29→28, `journey`, `modality`, `schedule` po 28→28, `lead_source` 25→25. Nie ma kroku-zabójcy. To jest robota zrobiona dobrze i **nie należy jej ruszać**.

Problem zaczyna się dokładnie w momencie, w którym kończy się ankieta i zaczyna produkt.

### 4.2 Kaskada, na 100 osób, które pierwszy raz otwierają aplikację

| Etap | Na 100 | Skąd liczba | Ubytek na tym kroku |
|---|---|---|---|
| Pierwsze otwarcie apki | 100 | PostHog: ~25 nowych person/tydz. | – |
| Zakłada konto | **~50** | Postgres ~13 rejestracji/tydz. vs PostHog ~25 nowych person/tydz. | **-50** |
| Kończy onboarding | ~38 | 76,7% ukończenia (43→33 w 30d) | -12 |
| Wykonuje pierwszą realną akcję w produkcie | **~10-19** | kohorta n=102: Reflect w W0 10,3%, prep 4,1%, nagranie **0,0%**, workspace **0,0%** | **-19 do -28** |
| Wraca następnego dnia (D1) | **7,5** | PostHog, n=319 | -2,5 do -11 |
| Wraca po 7 dniach (D7) | **4,0** | PostHog, n=303 | -3,5 |
| Jest w apce w 2. tygodniu (W2) | **4,9** | kohorta n=102 → 5 osób | ~płasko |
| Wraca po 30 dniach (D30) | **0,8** | PostHog, n=244 → **2 osoby** | -3,2 |

Osobno, bo paywall nie jest instrumentowany kohortowo (patrz sekcja 6), więc mierzę go na MAU, nie na kohorcie nowych:

| Etap monetyzacyjny | Liczba (30d) | % MAU (127) |
|---|---|---|
| Zobaczył `paywall_shown` | 7 | 5,5% |
| Otworzył ekran subskrypcji | 15 | 11,8% |
| Wybrał produkt | 7 | 5,5% |
| Rozpoczął zakup | 3 | 2,4% |
| Zakup nieudany | 2 | 1,6% |
| **Zweryfikowany paragon w Postgresie** | **2** | **1,6%** |

Wszystkie te segmenty mają n<25, więc są kierunkowe, nie statystyczne. Ale kierunek jest jednoznaczny.

### 4.3 Gdzie jest największa dziura

Trzy dziury, w kolejności wielkości:

**Dziura nr 1: ściana rejestracji, -50 na 100.** Około połowa osób, które otwierają aplikację, nie zakłada konta. To jest największy pojedynczy ubytek w całej kaskadzie. Zastrzeżenie: liczby pochodzą z dwóch różnych systemów o różnym sposobie zliczania (PostHog scala osoby przy `$identify`, Postgres liczy wiersze), więc traktuj to jako rząd wielkości 40-55%, nie jako precyzyjne 50%. To jest znane z poprzednich analiz (raport `2026-08-10-anonymous-users-analysis.md` policzył 41% realnego odbicia od ściany rejestracji) i **nadal nie jest naprawione**.

**Dziura nr 2: pierwsza akcja w produkcie, -19 do -28 na 100.** Z kohorty 102 nowych osób, tych 97, które odpadły, w pierwszym tygodniu: 10,3% odpaliło Reflect, 4,1% otworzyło prep card, **0,0% zrobiło nagranie i 0,0% otworzyło workspace**. Dwa zera przy funkcjach, które mają odpowiednio 6% i 33% adopcji w całym MAU, oznaczają jedno: **workspace i nagrywanie są powierzchniami dla wracających, nowy użytkownik nigdy ich nie widzi.**

**Dziura nr 3: pierwsze 24 godziny, z 10-19 zostaje 7,5.** Ale uwaga na interpretację. D1 = 7,5% jest niskie nie dlatego, że ludzie robią coś i im się nie podoba, tylko dlatego, że większość z tych 100 osób nigdy nic nie zrobiła. D1 to konsekwencja dziur 1 i 2, nie osobny problem.

### 4.4 Czego kaskada NIE pokazuje, a co jest równie ważne

**Retencja płacących jest równie zła jak darmowych.** 60 zweryfikowanych zakupów w historii, 37 kont z `granted_via='purchase'`, z czego dziś aktywnych **7**. To znaczy, że **81% osób, które kiedykolwiek zapłaciły, dziś nie płaci**. Nie znam dokładnego okresu, w którym odpadły, bo w bazie nie ma kwot ani historii odnowień, ale sam stosunek 7:37 wystarczy, żeby powiedzieć rzecz najważniejszą w tym raporcie:

> Gdybyś jutro naprawił paywall i sprzedał 30 subskrypcji, za kilka miesięcy zostałoby Ci z nich około 6.

Dlatego każda złotówka i każda godzina włożona w monetyzację przed naprawą retencji jest wyrzucona. To nie jest ostrożność, to arytmetyka.

### 4.5 Bramki free/premium są ustawione znacznie powyżej tego, gdzie użytkownik w ogóle dochodzi

Porównajmy limity z realnym użyciem:

| Bramka | Limit free | Realne użycie (30d) | Czy ktoś w ogóle dobija do limitu? |
|---|---|---|---|
| Debriefy | 5/miesiąc | "Your Session" (wszystkie 3 etapy razem): 28 osób, mediana **2,5** zdarzenia | Nie |
| Nagrania sesji | 2 łącznie | 7 osób, 11 zdarzeń, mediana **1,0** | Praktycznie nie |
| Hero Insight | odświeżenie raz na 7 dni | brak eventu adopcji | Nie wiemy |
| Snapshoty | 7d free, 30/90d premium | brak eventu | Nie wiemy |
| Habit Tracker | 1 aktywny nawyk | **zero instrumentacji** | Nie wiemy |
| Reflect | premium | 25 osób startuje sesje, 16 wysyła wiadomości | Tak, ale 1 osoba w 30d |

Dowód z lejka paywalla: z 7 osób, które w 30 dni zobaczyły `paywall_shown`, tylko **2 przyszły z bramki premium** (`premium_gate_session_recording` 1 osoba, `premium_gate_reflect_messages` 1 osoba). Pozostałe 5 przyszło z `drawer_menu` (5) i `settings` (1), czyli same poszły szukać oferty.

**Wniosek: zaostrzanie limitów free nic nie da, bo nikt do nich nie dochodzi.** Podnoszenie ceny też nic nie da, bo nikt oferty nie widzi. Free tier nie jest za hojny – on jest nieistotny.

---

## 5. Czy to zły kierunek produktu? Interpretacja adopcji funkcji

### 5.1 Co ludzie faktycznie robią

| Funkcja | % MAU (n=127) | Charakter |
|---|---|---|
| Statystyki / Timeline | **52,0%** | **czytanie** |
| Dashboard / Workspace | **33,1%** | **czytanie** |
| "Your Session" (prep/nagranie/debrief) | 22,0% | robienie |
| Threads (Reflect) | 21,3% | robienie |
| Reflect – rozpoczęte sesje | 19,7% | robienie |
| Reflect – wysłane wiadomości | 12,6% | robienie |
| Podsumowanie tygodniowe obejrzane | 11,0% | czytanie |
| Voice note | 7,1% | robienie |
| Nagrywanie sesji | 5,5% | robienie |
| Rozmowa/czat (stary model `conversation_*`) | **0%** | **martwe od 2026-08-11** |
| Habit Tracker | **niemierzalne** | – |

Dwie najpopularniejsze funkcje to powierzchnie **czytania**. Wszystko, co wymaga wysiłku, siedzi w przedziale 5-22%.

### 5.2 Twardy dowód, że ludzie przychodzą oglądać puste ekrany

To jest moim zdaniem najciekawsze znalezisko w całym materiale i wynika z danych o błędach, nie z danych o użyciu. Trzy najczęstsze `api_error` w 30 dni to zaprojektowane 404 typu "jeszcze nic tu nie ma":

| Endpoint | Zdarzenia | Użytkownicy | % MAU |
|---|---|---|---|
| `/prep-cards/latest` 404 | 2120 | 58 | **45,7%** |
| `/debriefs/latest` 404 | 1364 | 51 | **40,2%** |
| `/health-check/latest` 404 | 835 | 47 | **37,0%** |
| **Razem pustych stanów** | **4319** | | |

Porównaj: **4319 uderzeń w pusty stan** wobec **173 zdarzeń "Your Session"** w tym samym oknie. Stosunek **25:1**. Ludzie szukają treści dwadzieścia pięć razy częściej, niż ją tworzą.

### 5.3 Czym MindSync jest dla użytkownika, a czym miał być

**Miał być**: narzędziem do pracy między sesjami terapeutycznymi. Model: przygotuj się (prep card) → idź na sesję → opracuj ją (debrief) → dostaniesz wgląd. Pętla jest napędzana wysiłkiem użytkownika wokół zewnętrznego wydarzenia.

**Jest**: lustrem, w które ludzie zaglądają, i które prawie zawsze jest puste. Najczęściej używana powierzchnia (timeline, 52%) pokazuje historię, która powstaje z wysiłku, którego prawie nikt nie podejmuje (nagrania 5,5%, debriefy w medianie 2,5 zdarzenia).

I tu jest prawdziwa, niewygodna diagnoza kierunku. Nie brzmi ona "pomysł jest zły". Brzmi:

> **MindSync ma pętlę produktową o okresie 1-2 tygodni, zapakowaną w formę, która wymaga pętli dziennej.** Terapia odbywa się raz na tydzień albo raz na dwa tygodnie. Aplikacja mobilna, która daje powód do otwarcia raz na dwa tygodnie, w statystykach retencji wygląda dokładnie tak, jak wygląda MindSync: D1 7,5%, D30 0,8%, 68,5% z jednym aktywnym dniem w miesiącu.

To nie jest problem "brakuje funkcji". To jest **niedopasowanie częstotliwości**. Z tego wynikają trzy konsekwencje, każda poparta liczbą:

1. **Trial 4-dniowy jest krótszy niż pętla produktowa.** 554 konta (29,9%) kiedykolwiek dostały darmowy trial przy rejestracji. Jeśli sesja terapeutyczna odbywa się raz na tydzień lub dwa, to **większość użytkowników na 4-dniowym trialu nigdy nie doświadczy głównej wartości premium**, bo w czasie trwania trialu po prostu nie ma sesji do opracowania. Trial jest krótszy niż jeden obrót koła zamachowego produktu.
2. **Powierzchnia czytania jest bezwartościowa bez powierzchni robienia.** Nie da się "naprawić timeline'u", bo timeline to tylko widok danych. Pusty timeline w pierwszym tygodniu widzi 23,7% odpadających użytkowników – dostają obietnicę wglądu i pusty ekran.
3. **Jedyna funkcja z dzienną pętlą, jaką macie, jest niewidzialna.** Habit Tracker (wdrożony 2026-09-02) ma **zero eventów PostHog**, nie generuje nawet `$screen`, bo to widget na `mainPage`. Nie wiesz, czy ktokolwiek go używa. To jest jedyna rzecz w produkcie, która strukturalnie może dawać powód do codziennego otwarcia, i jest jedyną, o której nie masz żadnych danych.

### 5.4 Co faktycznie działa i czego nie wolno zepsuć

Uczciwość działa w dwie strony. Rzeczy, które są zrobione dobrze i których nie należy ruszać:

- **Onboarding, 76,7% ukończenia, 9 kroków, minimalny drop między krokami.** To jest dobry wynik i dobrze zbudowany flow.
- **Rollout wersji jest zdrowy** – trzon bazy siedzi na trzech najnowszych buildach (2.0.77 / 2.0.85 / 2.0.89), długi ogon to pojedyncze osoby.
- **Ludzie, którzy wchodzą w Reflect, wchodzą naprawdę** – mediana 6,5 wiadomości na osobę wśród 16 osób, które wysyłają. To nie jest przypadkowe klikanie, to realna rozmowa.
- **Prośba o pierwszy zapis działa mniej więcej w połowie przypadków.** `first_capture_prompt_shown` zobaczyło 60 osób, a jakiś etap "Your Session" wykonało 28. To nie jest dopasowana kohorta, więc traktuj to kierunkowo, ale sugeruje, że **kiedy prosicie, mniej więcej połowa robi**. Problem jest w tym, że prosicie tylko 47% MAU.
- **Stickiness DAU/WAU 26-31%** dla tego małego rdzenia, który zostaje, jest przyzwoity.
- **Sama terapeutyczna AI kosztuje grosze** (`CONVERSATION` 0,07 USD za 30 dni). Dostarczanie wartości nie jest drogie. Drogi jest mechanizm, który nie działa (sekcja 6).

Masz zdrowy rdzeń kilkudziesięciu osób i dobrze zrobione wejście. Nie masz powodu, żeby ktoś wrócił w dniu drugim.

---

## 6. Powiadomienia: jednocześnie największy wyciek pieniędzy i zepsuty główny mechanizm powrotu

### 6.1 Skala

| Metryka | Wartość |
|---|---|
| Wysłane (`moment.sent`) | **24 473** zdarzeń |
| Unikalni odbiorcy | **1815** |
| Powiadomień na odbiorcę / mies. | ~13,5 |
| Otwarte (`moment.opened`) | 47 zdarzeń |
| Unikalni otwierający | **26** |
| **Open rate (odbiorcy)** | **1,4%** |
| Open rate (zdarzenie do zdarzenia) | 0,19% |

Benchmark zewnętrzny: średnia reakcja na push w rynku to ~7,8% (4,9% iOS / 10,7% Android), a kategoria zdrowie/fitness na iOS należy do najlepszych z ~14,2%. **Jesteście 5 do 10 razy poniżej rynku, a w kategorii, która na rynku wypada najlepiej.**

### 6.2 Koszt

`NOTIFICATION` to **91,96 USD z 112,13 USD kosztu AI, czyli 82%**, przy 106 789 wpisach w `token_usage_log`. Doliczając `WEEKLY_SUMMARY` (11,88 USD) i `MONTHLY_AUDIT` (4,70 USD), czyli pozostałą treść generowaną automatycznie dla całej bazy, wychodzi **108,54 USD z 112,13 USD = 96,8% całego budżetu AI idzie na treść generowaną DLA użytkowników, a nie NA ICH ŻYCZENIE.**

Przelicznik na jednostkę wartości:

| Miara | Wartość |
|---|---|
| Koszt na odbiorcę powiadomień / mies. | 0,203 zł |
| **Koszt na jedno OTWARTE powiadomienie** | **7,83 zł** (91,96 USD / 47 otwarć) |
| **Koszt na osobę, która choć raz otworzyła** | **14,15 zł** (91,96 USD / 26 osób) |
| Wygenerowane podsumowania tygodniowe (30d) | 7233 |
| Obejrzane podsumowania tygodniowe (30d) | 49 zdarzeń przez 14 osób = **0,68%** |
| Obejrzane audyty miesięczne | 16 zdarzeń przez 5 osób z 3584 wygenerowanych = **0,45%** |

Płacisz **14 zł miesięcznie za jedną osobę, która otworzy jakiekolwiek powiadomienie**, przy subskrypcji, która daje Ci 14-35 zł netto. Generujesz 7233 podsumowania tygodniowe, żeby obejrzało je 14 osób.

### 6.3 Gdzie leży przyczyna: treść, częstotliwość, targetowanie czy dostarczalność

Rozstrzygam po kolei, bo to determinuje kolejność napraw.

**TARGETOWANIE – udowodnione, główna przyczyna.** Pięć głównych typów powiadomień idzie do **1700-1830 odbiorców każdy**, przy MAU **127**. To jest wysyłka do **14x większej bazy niż realnie aktywna**. Wśród odbiorców są 1259 kont, które **nigdy nie odbyły ani jednej rozmowy** – i te konta dostają `WEEKLY_SUMMARY_READY`, czyli powiadomienie o gotowym podsumowaniu tygodnia, w którym nie ma czego podsumowywać. To nie jest tylko marnotrawstwo pieniędzy, to jest aktywnie szkodliwe: uczy użytkownika, że powiadomienia z tej apki są puste. Tego nie trzeba dalej badać, to widać wprost w dwóch niezależnych liczbach.

**CZĘSTOTLIWOŚĆ – wspierająca przyczyna.** 13,5 powiadomienia na odbiorcę miesięcznie, czyli ~3,4/tydzień, samo w sobie nie jest skandaliczne dla zaangażowanego użytkownika. Dla uśpionego konta to spam. Problem częstotliwości jest wtórny wobec problemu targetowania: 3,4/tydzień do aktywnego to rozsądnie, 3,4/tydzień do kogoś, kto nie otworzył apki od 3 miesięcy, to powód do wyłączenia powiadomień albo odinstalowania.

**DOSTARCZALNOŚĆ – NIE WIEMY, i to jest luka pomiarowa, nie odpowiedź.** `notification_received` odpala się tylko gdy apka jest na pierwszym planie (18 zdarzeń / 5 osób), więc **nie mamy żadnego potwierdzenia doręczenia**. Nie da się dziś odróżnić "wysłane i zignorowane" od "wysłane i nigdy niedoręczone". Przy bazie, w której duża część kont jest nieaktywna od miesięcy, unieważnione tokeny FCM i odinstalowania są bardzo prawdopodobnym, dużym udziałem w tych 98,6% nieotwartych. **Zanim ktokolwiek zacznie przepisywać treść powiadomień, trzeba zmierzyć doręczalność** – bo jeśli realna doręczalność to na przykład 40%, to rzeczywisty open rate wynosi 3,5%, czyli nadal źle, ale zupełnie inna diagnoza.

**TREŚĆ – brak jakichkolwiek danych, i jest to ostatnia rzecz do obwiniania.** `moment.opened` **nie niesie property `moment_type`** (100% wartości null), więc nie da się powiedzieć, który typ powiadomienia konwertuje. Nie masz żadnego dowodu, że treść jest zła. Masz natomiast pewność, że idzie do niewłaściwych ludzi i że nie wiesz, czy w ogóle dochodzi.

**Kolejność napraw wynika wprost z powyższego: (1) przestać wysyłać do martwych kont, (2) zmierzyć doręczalność, (3) przypisać otwarcia do typu, (4) dopiero wtedy testować treść.** Krok 1 jest jednocześnie największą oszczędnością w całym raporcie i nie niesie ryzyka produktowego.

### 6.4 Ile da cięcie

| Scenariusz odbiorców | Liczba | Szacowany koszt AI/mies. | Oszczędność |
|---|---|---|---|
| Dziś (cała baza) | ~1815 | 112,13 USD ≈ 449 zł | – |
| Tylko konta z jakąkolwiek aktywnością w 90d | 382 | ~26 USD ≈ 104 zł | **~345 zł/mies.** |
| Tylko konta aktywne w apce w 30d | 127 | ~11 USD ≈ 44 zł | **~405 zł/mies.** |

Ryzyko: tracisz część z 26 osób, które cokolwiek otwierają. Nie wiem, ilu z nich mieści się w grupie 127 aktywnych, bo tego przecięcia nie ma w wyciągu. Ale nawet w najgorszym przypadku, gdyby połowa otwierających była poza grupą aktywnych, **tracisz 13 otwarć miesięcznie, żeby zaoszczędzić 345-405 zł**. Przy dzisiejszej cenie 14,15 zł za osobę-otwierającą to jest oczywisty zakup.

---

## 7. Ślepe plamy pomiarowe do zamknięcia PRZED większymi decyzjami

To nie jest lista życzeń analityka. To jest lista rzeczy, przez które **nie da się dziś odpowiedzialnie podjąć decyzji kierunkowej**, bo kluczowe wejścia do tej decyzji są niemierzalne.

| # | Luka | Dlaczego blokuje decyzję | Właściciel |
|---|---|---|---|
| L1 | **`trial_started` / `trial_ended` nigdy nie płynęły** (zero zdarzeń od początku ingestu 2026-04-22) | 554 konta kiedykolwiek weszły w trial. Nie wiesz, ile skonwertowało. Górne ograniczenie z krzyżowania dwóch źródeł: **≤37/554 = ≤6,7%**, i to zakładając hojnie, że każdy zakup poprzedził trial | `backend-api` + `flutter-mobile` |
| L2 | **`trial_outcome` NULL w 100%** (1852/1852 wierszy) | Kolumna istnieje pod tę właśnie instrumentację i nigdy nie jest zapisywana. To błąd zapisu w kodzie, nie brak danych | `backend-api` |
| L3 | **`paywall_shown` istnieje dopiero od 2026-08-16**, 10 zdarzeń / 7 osób w całej historii; `subscription_screen_opened` (15) systematycznie przewyższa `paywall_shown` (7) | Nie da się policzyć lejka "zobaczył ofertę → kupił". Event zaniża odsłony oferty i nie łapie większości wejść | `flutter-mobile` |
| L4 | **Brak eventu odbicia od bramki premium** z `trigger_feature` | 5 z 7 wyświetleń paywalla to ludzie, którzy sami poszli szukać. Nie wiesz, która zamknięta funkcja tworzy popyt, więc nie wiesz, co pakietować | `flutter-mobile` |
| L5 | **Habit Tracker: zero instrumentacji** (brak eventów, brak `$screen` – widget na `mainPage`) | To jedyna funkcja z potencjałem dziennej pętli i jedyna, o której nie wiesz nic. **Bez tego nie da się podjąć decyzji z sekcji 8** | `flutter-mobile` + `backend-api` |
| L6 | **`subscription_receipts` bez kwoty, waluty i środowiska** (sandbox/production) | Nie możesz policzyć własnego przychodu z własnej bazy, ani odróżnić TestFlight od realnej sprzedaży. Dwa zakupy z 30 dni mogą być prawdziwe albo mogą być testerami – **baza tego nie wie** | `backend-api` (model+migracja), `integration-devops` (weryfikacja) |
| L7 | **`moment.opened` bez `moment_type`** | Nie da się powiedzieć, który typ powiadomienia działa | `data-analytics` |
| L8 | **Brak potwierdzenia doręczenia push** | Nie da się odróżnić "nieotwarte" od "niedoręczone". Blokuje całą diagnozę powiadomień poza targetowaniem | `backend-api` + `integration-devops` |
| L9 | **`conversation_*` martwe od 2026-08-11** | Jeśli instrumentacja urwała się przy refaktorze, to "67,9% kont bez rozmowy" mierzy martwy event, a nie brak zaangażowania. Jeśli funkcja została wycofana świadomie, trzeba przedefiniować aktywację na Reflect. **Dziś nie wiemy, która wersja jest prawdziwa, a to zmienia interpretację głównej liczby raportu** | `flutter-mobile` + `data-analytics` |
| L10 | **4319 z 4639 `api_error` (93%) to zaprojektowane puste stany** | Zasłaniają realne błędy. Pod tym szumem siedzi nieoczekiwany 404 na `/users/get_user_profile_and_subscription` (38 osób) i `/users/therapy-context` (40 osób), razem ~1/3 aktywnej bazy w miesiącu | `backend-api` + `flutter-mobile` |

Zwróć uwagę na L9. To jedyna luka, która może **odwrócić** interpretację jednej z głównych liczb tego raportu. Zamknij ją pierwszą, bo jest tania (jedno sprawdzenie w kodzie) i wpływa na wszystko inne.

---

## 8. Rekomendacje, uporządkowane po stosunku efektu do wysiłku

### KOSZYK A: NATYCHMIAST – cięcie kosztów, zero ryzyka produktowego

| # | Działanie | Efekt | Wysiłek | Właściciel |
|---|---|---|---|---|
| **A1** | **Generować AI-powiadomienia tylko dla kont z aktywnością w apce w ostatnich 30 (lub 90) dniach.** Dla kont uśpionych: statyczna, niegenerowana treść w istniejącej drabince re-engagement (3d→7d→stop), albo nic | **-345 do -405 zł/mies.** = 42-49% całego budżetu operacyjnego | **Mały** (filtr w jobie generującym) | `data-analytics` (job) + `backend-api` |
| **A2** | **Przestać generować `WEEKLY_SUMMARY` i `MONTHLY_AUDIT` dla kont bez żadnej treści.** Dziś generujesz 7233 podsumowania tygodniowe, żeby obejrzało je 14 osób (0,68%), i 3584 audyty dla 5 osób (0,45%) | **-55 do -66 zł/mies.** | **Mały** (ten sam filtr) | `data-analytics` |
| **A3** | **Sprawdzić, czy Loops (180 zł/mies.) nie wysyła do tej samej martwej bazy.** Nie mam danych Loops, więc tego nie twierdzę – ale przy trzech kanałach wychodzących do tych samych 1855 kont, z których 1259 nigdy nic nie zrobiło, to jest oczywisty kandydat na trzecią kopię tej samej patologii | Potencjalnie **-180 zł/mies.** | **30 minut** (zalogować się, odczytać open/click rate) | Operator |
| **A4** | **Wyciszyć u źródła 404 typu "pusty stan"** na `/prep-cards/latest`, `/debriefs/latest`, `/health-check/latest` – zwracać 200 z pustym ciałem albo przestać raportować je jako `api_error` | Nie oszczędza pieniędzy, ale odsłania realne błędy pod szumem 93% | **Mały** | `backend-api` + `flutter-mobile` |

**Suma koszyka A: koszty spadają z ~830 zł do ~420-450 zł/mies. (bez Loops) lub ~250 zł (z Loops).** Break-even przy cenie 39,99 zł spada z **31 subskrypcji do 17** (lub 10). To jest największy pojedynczy ruch w kierunku dodatniego wyniku, jaki możesz zrobić w tym tygodniu, i nie wymaga zgadywania, co zadziała produktowo.

### KOSZYK B: W TYM MIESIĄCU – naprawa aktywacji i pomiaru

| # | Działanie | Efekt | Wysiłek | Właściciel |
|---|---|---|---|---|
| **B1** | **Rozstrzygnąć status `conversation_*`** (martwe od 2026-08-11): urwana instrumentacja czy świadome wycofanie? | Naprawia poprawność głównej metryki raportu (67,9% kont bez rozmowy). Najtańsza rzecz o największym wpływie na jakość decyzji | **Bardzo mały** (jedno sprawdzenie w kodzie) | `flutter-mobile` + `data-analytics` |
| **B2** | **Zainstrumentować Habit Tracker** (`habit_created`, `habit_completed`, ekspozycja widgetu) | **Odblokowuje decyzję kierunkową z sekcji 9.** Jedyna funkcja z dzienną pętlą, wdrożona 10 dni temu, kompletnie niewidzialna | **Mały** | `flutter-mobile` + `backend-api` |
| **B3** | **Naprawić nieoczekiwane 404** na `/users/get_user_profile_and_subscription` (38 osób) i `/users/therapy-context` (40 osób) | Dotyka ~1/3 aktywnej bazy miesięcznie, na endpointach profilu i kontekstu terapii, czyli dokładnie tych ładowanych zaraz po onboardingu. **Jedyny twardy kandydat na techniczną przyczynę odpadania w pierwszych dniach.** Miara efektu: D1 z 7,5% | **Średni** | `backend-api` |
| **B4** | **Wypełnić pierwszy ekran po onboardingu treścią, którą już macie.** Nie nowa funkcja: wygenerować pierwszy wpis timeline'u / kartę z 9 kroków onboardingu, które użytkownik właśnie wypełnił. Dowód potrzeby: 4319 uderzeń w pusty stan w 30 dni u 47-58 osób ze 127 | Atakuje dziurę nr 2 z kaskady (-19 do -28 na 100). Miara: % nowych z ≥1 `timeline_viewed` zakończonym treścią, oraz D1 | **Średni** | `ui-ux-designer` (spec) → `flutter-mobile` |
| **B5** | **Dodać `trial_started` / `trial_ended` i naprawić zapis `trial_outcome`** (dziś NULL w 100%) | Pierwsza w historii mierzalna konwersja trial→paid. 554 konta czekają na policzenie | **Mały** | `backend-api` (zapis) + `flutter-mobile` (eventy) |
| **B6** | **Dodać event odbicia od bramki premium z `trigger_feature`** na wszystkich znanych bramkach (nagrania, debriefy, snapshoty, cele, audyty, health-check, Reflect, Habit Tracker) | Jedyny sposób, żeby dowiedzieć się, która zamknięta funkcja tworzy popyt. Dziś 5 z 7 wyświetleń paywalla to samodzielne poszukiwanie | **Mały** | `flutter-mobile` |
| **B7** | **Dodać kolumnę środowiska (sandbox/production), kwoty i waluty do `subscription_receipts`** | Pierwszy wiarygodny MRR. Dziś nie możesz policzyć przychodu z własnej bazy | **Średni** (model + migracja + weryfikacja Apple/Google) | `backend-api` + `integration-devops` |
| **B8** | **Dodać potwierdzenie doręczenia push** (odpowiedź FCM, unieważnione tokeny) i `moment_type` w `moment.opened` | Bez tego cała diagnoza powiadomień poza targetowaniem to zgadywanie | **Średni** | `backend-api` + `data-analytics` |
| **B9** | **Rozważyć wydłużenie trialu przy rejestracji z 4 dni do co najmniej 14.** Uzasadnienie z danych: pętla produktowa ma okres 1-2 tygodni (sesja terapeutyczna), więc 4-dniowy trial strukturalnie nie mieści jednego obrotu pętli. Jednocześnie sprawdzić, czy trial w ogóle ma mechanizm konwersji: w bazie jest on nadawany backendowo (`granted_via='signup_trial'`), odrębnie od `granted_via='purchase'`, co sugeruje, że **na końcu 4 dni nie ma automatycznego momentu obciążenia**. Do potwierdzenia w App Store Connect / Play Console | Górna granica dzisiejszej konwersji trial→paid to ≤6,7%. Standardem rynkowym dla trialu zarządzanego przez sklep z kartą jest 30-50% | **Mały** (zmiana długości) / **Duży** (jeśli trzeba zbudować trial sklepowy) | `backend-api` + `integration-devops` |

**Czego świadomie NIE rekomenduję**: budowy nowych funkcji, przeprojektowania paywalla, podnoszenia ceny, zaostrzania limitów free, kampanii akwizycyjnej. Wszystkie pięć są przy 127 MAU i D30 = 0,8% wydawaniem pieniędzy na wypełnianie wiadra, które przecieka.

### KOSZYK C: DECYZJA KIERUNKOWA – co, jeśli za 2-3 miesiące liczby się nie ruszą

Trzy scenariusze. Nie są równorzędne i nie są rozłączne. **Koszyk A wykonaj niezależnie od tego, który wybierzesz** – on kupuje czas na podjęcie tej decyzji.

**Scenariusz A: przeprofilowanie na dzienną pętlę (domyślny, jeśli dane pozwolą).**
Dane mówią jasno, że ludzie przychodzą **patrzeć** (timeline 52%, workspace 33%), nie **robić** (Your Session 22%, nagrania 5,5%). Pętla terapeutyczna ma okres 1-2 tygodni i nigdy nie da dziennego powodu do otwarcia. Habit Tracker jest jedyną dzienną pętlą w produkcie i jest niezmierzony. **Decyzja: zmierzyć go (B2), dać mu 30 dni, i jeśli osiągnie adopcję >30% MAU oraz D7 wyraźnie wyższe niż reszta bazy – przestawić główny ekran i główną narrację na niego, a pętlę terapeutyczną zostawić jako warstwę premium dla tych, którzy realnie chodzą na terapię.** To nie jest budowanie nowej funkcji. To jest zmiana tego, co jest na wierzchu, i zmiana tego, komu sprzedajesz.
Uwaga uczciwa: to jest zarazem zmiana rynku, na którym konkurujesz, z "narzędzie dla osób w terapii" na "tracker nawyków ze wsparciem AI", gdzie konkurencja jest o rząd wielkości większa. To trzeba świadomie zaakceptować albo świadomie odrzucić. Osobna analiza konkurencyjna przed tym krokiem jest wskazana (`competitive-strategist`).

**Scenariusz B: tryb utrzymaniowy, "wolny ogień" (jeśli liczby się nie ruszą).**
Koszty do minimum (koszyk A: ~250-450 zł/mies.), zero nowych funkcji, zero nowych wydatków, apka utrzymywana dla obecnych 127 MAU i 7 płacących. Realnie: ~3000-5400 zł/rok kosztu utrzymania zamiast ~10 000 zł. **To nie jest porażka.** To jest zatrzymanie krwawienia i zachowanie opcji. Produkt jest zbudowany, działa, ma zdrowy onboarding i rdzeń kilkudziesięciu osób. Trzymanie go na wolnym ogniu przez rok kosztuje mniej niż jeden miesiąc źle wydanych pieniędzy na akwizycję.

**Scenariusz C: zmiana kanału, nie produktu (opcja do rozważenia osobno).**
Sygnalizuję, nie rekomenduję na tych danych. 1855 kont, 60 zakupów w historii, 13 rejestracji/tydzień bez trendu i bez działającego kanału akwizycji. Jedyna wersja zmiany kanału, która przy tej retencji ma sens ekonomiczny, to **B2B przez terapeutę**: portal kliniczny już istnieje i jest zbudowany, a jedna terapeutka to kilkunastu pacjentów, którzy mają zewnętrzny, autorytatywny powód, żeby używać pętli terapeutycznej. To rozwiązuje dokładnie ten problem, który zabija produkt w B2C: brak powodu do powrotu. Ale wymaga osobnej analizy (koszt sprzedaży, cykl, cena za miejsce) i nie da się jej zrobić na danych z tego raportu.

**Bramka decyzyjna: 2026-12-12.**
- **D1 (4-tygodniowe kroczące) ≥ 15% i D7 ≥ 8%** → produkt ma szansę, wracamy do rozmowy o monetyzacji.
- **D1 < 12%** → scenariusz B, tryb utrzymaniowy, koszty do minimum, koniec inwestowania czasu.
- **Habit Tracker >30% MAU i wyższe D7** → scenariusz A, przestawiamy produkt na dzienną pętlę.

---

## 9. Jedna metryka na cotygodniowy przegląd

### **Retencja D1 – odsetek nowych użytkowników, którzy otwierają aplikację następnego dnia. Czytana jako średnia krocząca z 4 tygodni.**

**Dziś: 7,5%** (24 z 319 osób w kohortach z ostatnich 90 dni).
**Próg do 2026-12-12: 15%.**
**Poniżej 12% – zmieniamy strategię na scenariusz B (tryb utrzymaniowy).**

**Dlaczego akurat ta, a nie żadna inna:**

1. **Jest najwyżej w łańcuchu przyczynowym.** Przy D1 = 7,5% 92,5% ludzi znika, zanim zobaczy jakąkolwiek ofertę. Dopóki ta liczba się nie ruszy, każda praca nad paywallem, ceną, pakietowaniem i treścią powiadomień jest optymalizacją czegoś, czego nikt nie widzi.
2. **Odpowiada w 48 godzin, nie w 30 dni.** D30 jest prawdziwsze, ale przy 2 osobach na 244 jest statystycznie martwe i daje odpowiedź za miesiąc. D1 daje sygnał od razu i jest jedyną metryką retencji z sensowną próbką przy Waszym napływie.
3. **Nie da się jej oszukać cięciem kosztów ani spamem.** MAU można podbić powiadomieniami, przychód przy 2 zakupach miesięcznie to czysty szum (jeden paragon to wahanie o 50%), a aktywacji nie da się dziś czysto zmierzyć, bo "Your Session" nie ma pojedynczego eventu wejścia, a Habit Tracker nie ma żadnego. D1 jest oparte na jednym, pewnym zdarzeniu: otworzył apkę czy nie.
4. **Jest metryką, w którą celują wszystkie rekomendacje z koszyka B.** B3 (nieoczekiwane 404 na profilu), B4 (pusty pierwszy ekran) i naprawa ściany rejestracji mierzą się dokładnie tym samym miernikiem. Jedna metryka, jedna decyzja.

**Jak ją czytać, żeby się nie oszukać:** przy ~25 nowych osobach tygodniowo pojedynczy tydzień jest bezwartościowy – 7,5% to 2 osoby, 15% to 4 osoby, a różnica dwóch osób to przypadek. **Czytaj wyłącznie jako średnią kroczącą z 4 tygodni** (n≈100), gdzie 7,5% to 7-8 osób, a 15% to 15 osób i to jest różnica, którą naprawdę widać. Jeden zły tydzień nic nie znaczy. Cztery złe tygodnie znaczą wszystko.

**Czego NIE patrzeć co tydzień:** przychodu (2 zdarzenia miesięcznie, czysty szum), MAU (lagguje 30 dni i miesza nowych ze starymi), liczby rejestracji (płaska od 12 tygodni, nic Ci nie powie), kosztów AI po wdrożeniu koszyka A (sprawdź raz, potwierdź spadek, zapomnij).

---

## 10. Zastrzeżenia i granice pewności

1. **Nie znamy ceny planu `premium_m_01`.** Wszystkie wyliczenia break-even są scenariuszowe. Odczytaj cenę z App Store Connect / Google Play Console i podstaw do tabeli w 3.3.
2. **Nie wiemy, czy 2 zakupy z 30 dni to produkcja, czy TestFlight/sandbox.** Tabela `subscription_receipts` nie ma kolumny środowiska, a Apple `verifyReceipt` przy statusie 21007 ponawia pod sandboxem i zapisuje wynik w tym samym kształcie. To twarde ograniczenie danych, nie ostrożność.
3. **Nie wiemy, czy 7 aktywnych płacących to 7 realnych klientów.** Baza nie ma flagi konta testowego, a wśród kont mogą być Twoje i znajomych.
4. **Ściana rejestracji (~50% ubytku) jest liczona przez porównanie dwóch systemów** o różnym sposobie zliczania osób (PostHog scala przy `$identify`, Postgres liczy wiersze) i przy przesuniętych o tydzień oknach. Rząd wielkości 40-55% jest solidny, dokładne 50% nie.
5. **Segment przeżywających do W2 (5 osób na 102) jest supresowany** zgodnie z progiem k-anonimowości 25. Nie da się dziś powiedzieć, co robią ci, którzy zostają – żeby to zmierzyć, potrzeba kohorty rzędu 500+ nowych użytkowników.
6. **`paywall_shown` ma 10 zdarzeń w całej historii** (od 2026-08-16). Nie ekstrapoluj z tego trendu ani konwersji.
7. **`subscription_purchase_completed` z PostHoga (5 osób) nie zgadza się z 2 paragonami z Postgresu.** Prawdą przychodową jest Postgres. Rozbieżność jest znana z wcześniejszych audytów i nie została tu zbadana.
8. **Korelacja to nie przyczynowość.** "Ludzie patrzą na timeline częściej, niż tworzą treść" opisuje zachowanie, nie dowodzi, że wypełnienie pustego stanu podniesie retencję. B4 trzeba wdrożyć jako zmianę mierzalną na D1, a najlepiej jako test A/B, jeśli próbka pozwoli (przy 25 nowych/tydzień test A/B na D1 potrzebuje kilkunastu tygodni na rozstrzygnięcie – to realne ograniczenie, o którym trzeba wiedzieć przed startem).
9. **Ingest PostHoga zaczął się 2026-04-22.** Nic wcześniejszego nie istnieje behawioralnie.
10. **Kurs 4 PLN/USD jest przybliżeniem**, nie odczytem z faktury.
11. **Szacunki Heroku (200 zł) i Loops (180 zł) pochodzą od operatora** i nie zostały zweryfikowane w żadnym źródle danych.

---

## Aneks

### A. Benchmarki zewnętrzne (NIE pochodzą z naszych danych)

| Metryka | MindSync | Benchmark | Źródło |
|---|---|---|---|
| D1 retencja | 7,5% | ~26-35% (health/fitness) | [Business of Apps](https://www.businessofapps.com/data/health-fitness-app-benchmarks/), [UXCam](https://uxcam.com/blog/mobile-app-retention-benchmarks/) |
| D7 retencja | 4,0% | ~15-20% (fitness) | [UXCam](https://uxcam.com/blog/mobile-app-retention-benchmarks/) |
| D30 retencja | 0,8% | ~4% mediana wszystkich kategorii, 3-4% health | [Business of Apps](https://www.businessofapps.com/data/health-fitness-app-benchmarks/), [apsteq](https://apsteq.com/blog/app-retention-benchmarks/) |
| Konwersja download→paid | 0,38% aktywnych płacących | 2,2% mediana freemium; górne 25% robi 10-15% | [RevenueCat State of Subscription Apps 2025](https://www.revenuecat.com/state-of-subscription-apps-2025), [Userpilot](https://userpilot.com/blog/freemium-to-premium/) |
| Trial→paid | ≤6,7% (górne ograniczenie) | 30-50% dla trialu zarządzanego przez sklep | [Adapty](https://adapty.io/blog/trial-conversion-rates-for-in-app-subscriptions/) |
| Open rate push | 1,4% | ~7,8% średnia; 14,2% health/fitness iOS | [Airship](https://www.airship.com/blog/your-guide-to-airships-mobile-app-push-notification-benchmarks-for-2026/), [Pushwoosh](https://www.pushwoosh.com/blog/push-notification-benchmarks/) |

Zastrzeżenie do benchmarku trial→paid: nasz trial jest 4-dniowy, nadawany backendowo przy rejestracji, bez karty płatniczej. Trial zarządzany przez sklep z kartą to zupełnie inny mechanizm i konwertuje wielokrotnie lepiej z definicji. Porównanie 6,7% do 30-50% jest nieuczciwe wobec naszego trialu i **jest tu po to, żeby pokazać, jakiego mechanizmu brakuje, a nie żeby ocenić istniejący**.

### B. Definicje użyte w raporcie

- **MAU** = unikalne `person_id` z `$lib='posthog-flutter'`, po odfiltrowaniu TestFlight, emulatorów i znanego ruchu botowego (`$device_model IN ('OnePlus8Pro','Pixel 6 Pro')`), w oknie 30 dni. **127.**
- **Konta dotknięte przez backend** = unikalne `person_id` z jakimkolwiek zdarzeniem `$lib='posthog-python'`. **1874.** To NIE są aktywni użytkownicy.
- **Realny płacący** = `user_subscription.is_active=true AND granted_via='purchase'`. **7.**
- **Konto z zakupem w historii** = `user_subscription.granted_via='purchase'`, aktywne lub wygasłe. **37.**
- **D1/D7/D30** = odsetek kohorty (pierwsze zdarzenie w PostHogu) z aktywnością dokładnie w dniu +1/+7/+30, okna przycięte tak, by nie ucinać prawego ogona.
- **One-and-done** = osoba z aktywnością tylko w jednym dniu kalendarzowym w całej historii w apce.
- **Netto dla wydawcy** = `cena_brutto / 1,23 × (1 - prowizja_sklepu)`; VAT 23% pobiera sklep, prowizja 15% (program dla małych wydawców) lub 30%.

### C. Zapytania źródłowe

Pełne zapytania HogQL i SQL, wraz z metodą dostępu, znajdują się w dwóch raportach źródłowych:
- `db-reports/2026-09-12-subscription-revenue-30d.md` (sekcje 1-8, wszystkie SELECT verbatim)
- `analytics-reports/raw/2026-09-12-usage-retention-monetization-extract.md` (sekcja "Zapytania HogQL (verbatim)")

Ten raport nie wykonał żadnych własnych zapytań do produkcji – wszystkie liczby pochodzą z powyższych dwóch ekstraktów, poza benchmarkami z aneksu A i przeliczeniami arytmetycznymi opisanymi w treści.

### D. Przekazania do właścicieli domen

| Znalezisko | Właściciel | Priorytet |
|---|---|---|
| Filtr odbiorców AI-powiadomień i podsumowań | `data-analytics` + `backend-api` | **Natychmiast** |
| Status `conversation_*` (martwe od 2026-08-11) | `flutter-mobile` + `data-analytics` | **Natychmiast** (tanie, zmienia interpretację) |
| Instrumentacja Habit Tracker | `flutter-mobile` + `backend-api` | Wysoki |
| Nieoczekiwane 404 na `/users/get_user_profile_and_subscription` i `/users/therapy-context` | `backend-api` | Wysoki |
| `trial_outcome` NULL w 100% + eventy `trial_started`/`trial_ended` | `backend-api` + `flutter-mobile` | Wysoki |
| Kolumna środowiska + kwota/waluta w `subscription_receipts` | `backend-api` + `integration-devops` | Wysoki |
| Event odbicia od bramki premium z `trigger_feature` | `flutter-mobile` | Średni |
| Potwierdzenie doręczenia push + `moment_type` w `moment.opened` | `backend-api` + `data-analytics` | Średni |
| Wyciszenie 404 pustych stanów | `backend-api` + `flutter-mobile` | Średni |
| Spec pierwszego ekranu z treścią z onboardingu | `ui-ux-designer` → `flutter-mobile` | Średni |
| Ściana rejestracji (~50% ubytku) – projekt wejścia bez konta | `ui-ux-designer` + `flutter-mobile`, ruling Art. 9 od `security-guardian` | Średni, zablokowany na rulingu |
| Analiza konkurencyjna przed scenariuszem A (dzienna pętla) | `competitive-strategist` | Przed decyzją 2026-12-12 |
