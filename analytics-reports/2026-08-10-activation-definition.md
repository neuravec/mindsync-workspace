# Definicja aktywacji MindSync - raport insightowy

- **Data**: 2026-08-10
- **Analityk**: growth-analyst
- **Pytanie biznesowe**: Która wczesna akcja (lub minimalny zbiór akcji) najlepiej rozdziela nowych użytkowników, którzy wracają, od tych, którzy nie wracają nigdy - i jak to zmierzyć?
- **Metryka sukcesu**: powrót do aplikacji w dniach 2-7 od pierwszego otwarcia (potwierdzony na dniach 8-28)
- **Okno danych**: kohorta first-seen 2026-05-01 → 2026-07-26; zdarzenia do 2026-08-10
- **Źródła**: PostHog EU proj 141170 (`scripts/posthog_query.py`, HogQL read-only) · benchmarki zewnętrzne (linki w sekcji Benchmarki) · brak zapytań do Postgres (nie były potrzebne - metryka jest behawioralna)
- **Pewność**: **Średnia** - n=652 osób w kohorcie i wynik główny istotny na p<0.0001, ale efekt jest częściowo splątany z ogólną głębokością pierwszej sesji, a kilka kandydatów ma n<25

---

## Executive Summary

- **Aktywacja = pierwszy zapis w pętli terapeutycznej w ciągu 24h od pierwszego otwarcia aplikacji.** Nie ukończenie onboardingu. Onboarding jest warunkiem koniecznym, ale niewystarczającym: sam onboarding daje 11.4% powrotu (vs 7.1% baseline, nieistotne), a onboarding + pierwszy zapis daje **25.8%**.
- **Jeden zapis wystarczy.** Dose-response jest schodkiem, nie rampą: 0 kategorii zapisu → 7.4% powrotu, 1 → 24.4%, 2 → 21.6%, 3+ → 30.0%. Drugi i trzeci zapis nie dokłada nic istotnego (w kohorcie po onboardingu: `cap>=2` 25.0% vs `cap>=3` 25.0%). Progiem jest przekroczenie zera.
- **Efekt utrzymuje się długoterminowo**: aktywowani wracają w d8-28 w 21.7% vs 7.7% (2.83x, p<0.0001) i osiągają 2+ aktywne tygodnie w 35.7% vs 13.7% (2.61x, p<0.0001). To nie jest artefakt krótkiego okna.
- **Aktualna wartość: 41.5% zarejestrowanych nowych użytkowników aktywuje się (85/205); 17.0% wszystkich nowych osób w aplikacji (111/652).** 41.5% jest w benchmarkowym pasmie SMB SaaS (35-50%), ale **82.9% całej kohorty nigdy nie wykonuje żadnego zapisu** - i tu leży wynik.
- **Czas do wartości NIE jest problemem.** 93 ze 118 osób, które kiedykolwiek zrobiły pierwszy zapis, zrobiły go w pierwszej godzinie; mediana od `user_registered` do pierwszego zapisu = **4 minuty**. Ludzie albo przekraczają linię niemal natychmiast, albo nigdy. To zmienia rekomendację z "skróć TTV" na "postaw pytanie/CTA w pierwszej sesji".
- **Rekomendacja nr 1 dla instrumentacji: nie dodawać klienckiego `user_activated`.** Metryka ma być **wyliczana** (derived) z istniejących zdarzeń, bo 3 z 9 kategorii zapisu emituje wyłącznie backend. Dla `flutter-mobile` jest natomiast realna, blokująca luka: nie widzimy, czy 82.9% nieaktywowanych w ogóle **zostało zapytanych** o pierwszy zapis. Spec w sekcji Instrumentacja.

---

## Kluczowe metryki

| Metryka | Wartość | Benchmark | Odczyt |
|---|---|---|---|
| Kohorta (nowe osoby app-only, 05-01..07-26) | 652 | - | próba wystarczająca |
| Powrót d2-7 (cała kohorta) | 10.4% (68/652) | Health & Fitness D7 ~10% | na poziomie benchmarku, ale nasza miara jest **luźniejsza** (dowolny dzień 2-7, nie dokładnie D7) → faktycznie poniżej |
| Powrót d2-7 (tylko zarejestrowani) | 17.6% (36/205) | jak wyżej | akceptowalnie |
| Powrót d8-28 (cała kohorta, pełna obserwacja) | 10.1% (61/602) | Health & Fitness D30 ~4% | powyżej benchmarku (miara luźniejsza) |
| **Aktywacja (nowa definicja), zarejestrowani** | **41.5% (85/205)** | SMB SaaS 35-50%, mediana SaaS ~37%, top kwartyl 68% | w pasmie, daleko od top kwartyla |
| **Aktywacja (nowa definicja), wszystkie nowe osoby** | **17.0% (111/652)** | - | zdominowane przez odbicie na ekranie auth |
| Nigdy nieuwierzytelnieni w kohorcie | 66.0% (430/652) | - | **krytyczne**, upstream aktywacji |
| Mediana `user_registered` → pierwszy zapis | 4 min (p90 = 126 min) | TTV "same-session" = dobry | TTV nie jest problemem |
| Trend aktywacji tygodniowo | ~25-27% (maj) → 7-15% (lipiec) | - | **pogarsza się**, n/tydzień małe |

---

## Dyscyplina okna czasowego (przeciw tautologii)

Aktywność koreluje z powrotem trywialnie - powrót **jest** aktywnością. Dlatego:

- **Okno akcji**: `[first_ts, first_ts + 24h)`, gdzie `first_ts` = min(timestamp) po zdarzeniach `properties.$lib = 'posthog-flutter'` danej osoby (kanoniczna definicja "nowej osoby app-only" z pamięci projektu).
- **Okno powrotu d2-7**: `[first_ts + 48h, first_ts + 8d)`.
- **Okno powrotu d8-28**: `[first_ts + 8d, first_ts + 29d)`.

Okna **nie nachodzą na siebie** (24h akcji, 24h bufora, potem pomiar). Żaden kandydat nie może "wygrać" tylko dlatego, że użytkownik był aktywny w oknie pomiaru. Kandydaci mierzeni na oknie 48h są w tabelach oznaczeni `_d01` i zachowują 0h bufora - dlatego definicję finalną oparto na 24h (patrz Wrażliwość na okno).

Kohortę zamknięto na 2026-07-26, więc każda osoba miała >=14 dni na powrót d2-7. Dla d8-28 raportuję podkohortę `first_ts < 2026-07-12` (n=602), która ma pełne 29 dni obserwacji.

---

## Ustalenia

### F1 - Aktywacją jest pierwszy zapis, nie ukończenie onboardingu · Impact: Critical · Confidence: M

Macierz 2x2 (okno akcji 24h):

| onboarding_completed <=24h | pierwszy zapis <=24h | n | powrót d2-7 | powrót d8-28 (n28) |
|---|---|---|---|---|
| nie | nie | 506 | **7.1%** (36) | 7.3% (34/465) |
| nie | tak | 18 | 22.2% (4) | 22.2% (4/18) · **n<25, niska pewność** |
| tak | nie | 35 | **11.4%** (4) | 12.9% (4/31) |
| tak | tak | 93 | **25.8%** (24) | 21.6% (19/88) |

- **Onboarding sam w sobie**: 11.4% vs 7.1% baseline = +4.3 pp, n=35, **nieistotne**.
- **Zapis na wierzchu onboardingu**: 25.8% vs 11.4% = 2.26x, +14.4 pp, p=0.080, 95% CI dla różnicy [+0.6, +28.2] pp. Granicznie istotne przy tym n, ale kierunek i rozmiar efektu są jednoznaczne.
- Na oknie 48h ta sama para daje 26.6% (n=94) vs 11.4% (n=35), p=0.067.

**So what**: `onboarding_completed` wygląda mocno w surowym lifcie (22.5% vs 7.5%, 3.01x, p<0.0001) tylko dlatego, że jest bramką do zapisu. Ustawienie celu produktowego na "ukończ onboarding" optymalizowałoby instalację rur, nie wartość. Bramką wartości jest pierwszy zapis.

### F2 - Progiem jest JEDEN zapis, nie dwa ani trzy · Impact: High · Confidence: M

Dose-response po liczbie **odrębnych kategorii** zapisu w oknie 24h (okno 48h dla kolumn kinds - patrz Zapytania):

| kategorie zapisu (d0-1) | n | powrót d2-7 | powrót d8-28 |
|---|---|---|---|
| 0 | 540 | **7.4%** (40) | 7.7% (38/495) |
| 1 | 45 | **24.4%** (11) | 18.6% (8/43) |
| 2 | 37 | 21.6% (8) | 22.9% (8/35) |
| 3+ | 30 | 30.0% (9) | 24.1% (7/29) |

Wewnątrz podkohorty, która ukończyła onboarding (n=129):

| warunek | n (spełnia) | powrót | n (nie spełnia) | powrót |
|---|---|---|---|---|
| `cap_kinds >= 1` | 94 | **26.6%** | 35 | 11.4% |
| `cap_kinds >= 2` | 56 | 25.0% | 73 | 20.5% |
| `cap_kinds >= 3` | 24 | 25.0% · n<25 | 105 | 21.9% |
| `cap_events >= 3` | 53 | 22.6% | 76 | 22.4% |

**So what**: 0→1 to skok 3.30x (p=0.0001). 1→2 i 2→3 mieszczą się w szumie. Definicja z progiem 2+ byłaby trudniejsza do osiągnięcia i **nie** mierzyłaby nic więcej. Bierzemy 1. To też oznacza, że "feature breadth >= 2" (24.0%, n=121) nie jest lepszym kandydatem niż "any capture" (25.0%, n=112) - breadth to w tej kohorcie w praktyce ta sama populacja.

### F3 - Żaden pojedynczy typ zapisu nie bije zbioru · Impact: High · Confidence: L-M

Per typ zapisu, wewnątrz podkohorty po onboardingu (okno 48h). Kolumna "bez" zawiera osoby, które zrobiły **inny** zapis, dlatego jej baseline jest wysoki (~20-23%):

| typ | n | powrót | n (bez) | powrót (bez) | uwaga |
|---|---|---|---|---|---|
| `goal_created` | 6 | 66.7% | 123 | 20.3% | **n<25, suppressed - tylko kierunek** |
| `reflect_message_sent` | 23 | 30.4% | 106 | 20.8% | **n<25** |
| `health_check_*` | 33 | 30.3% | 96 | 19.8% | |
| `between_session_*` | 23 | 26.1% | 106 | 21.7% | **n<25** |
| `debrief_*` | 70 | 24.3% | 59 | 20.3% | najczęstszy zapis |
| `prep_*` | 33 | 24.2% | 96 | 21.9% | |
| `symptom_*` | 10 | 20.0% | 119 | 22.7% | **n<25** |

Na całej kohorcie (okno 48h, baseline "nie zrobił" ~9%): `reflect_message_sent` 35.7% n=28 (3.84x, p<0.0001), `between_session` 33.3% n=27 (3.53x, p=0.0001), `health_check` 28.9% n=38 (3.12x, p=0.0001), `prep` 25.0% n=44 (2.67x, p=0.0011), `debrief` 24.1% n=79 (2.81x, p<0.0001).

**So what**: wszystkie przedziały ufności typów zachodzą na siebie. Wybór jednego typu jako "the aha action" byłby przeuczeniem na n=23-79. Zbiór ("którykolwiek zapis") ma n=112, najwęższe CI i jest odporny na to, że produkt zmienia priorytety między prep / debrief / reflect z wydania na wydanie. **Definicja musi być zbiorem akcji, nie jedną akcją.**

### F4 - Efekt częściowo przeżywa kontrolę na głębokość sesji · Impact: High · Confidence: M

Największy confounder: ludzie robiący zapis to po prostu ludzie, którzy zrobili w aplikacji więcej. Stratyfikacja po liczbie zdarzeń w oknie 48h:

| liczba zdarzeń d0-1 | zapis? | n | powrót d2-7 |
|---|---|---|---|
| 1-5 | nie | 286 | 8.0% |
| 1-5 | tak | 0 | - |
| 6-20 | nie | 181 | 6.1% |
| 6-20 | tak | 1 | - · n<25 |
| **21-50** | **nie** | **54** | **5.6%** |
| **21-50** | **tak** | **28** | **25.0%** |
| 51+ | nie | 19 | 15.8% · n<25 |
| 51+ | tak | 83 | 25.3% |

W jedynym pasmie z sensownym n po obu stronach (21-50 zdarzeń): **25.0% vs 5.6%, 4.50x, p=0.011, CI [+2.3, +36.6] pp**. W pasmie 51+ lift spada do 1.6x, ale grupa kontrolna ma n=19 (suppressed).

Ta sama kontrola dla `onboarding_completed`: w pasmie 21-50 21.1% (n=38) vs 4.5% (n=44); w pasmie 51+ 23.3% (n=90) vs 25.0% (n=12) - czyli lift onboardingu **znika** przy wysokiej aktywności. Zapis trzyma się lepiej.

**So what**: zapis nie jest wyłącznie proxy na "był aktywny". Ale nie jest też dowodem przyczynowości - to najlepszy dostępny **wskaźnik wyprzedzający**. Dowodem byłby wyłącznie A/B na prompcie pierwszego zapisu (patrz R2/R4).

### F5 - 24h to właściwe okno · Impact: Medium · Confidence: H

| okno akcji | aktywowani | % kohorty | powrót d2-7 (akt.) | powrót d2-7 (nieakt.) | d8-28 (akt.) | d8-28 (nieakt.) |
|---|---|---|---|---|---|---|
| 6h | 109 | 16.7% | 24.8% | 7.6% | 21.0% | 7.8% |
| **24h** | **111** | **17.0%** | **25.2%** | **7.4%** | **21.7%** | **7.7%** |
| 48h | 112 | 17.2% | 25.0% | 7.4% | 21.5% | 7.7% |
| 72h | 115 | 17.6% | 27.0% | 6.9% | 21.8% | 7.5% |

**So what**: 24h łapie 96.5% wszystkich aktywacji widocznych w 72h. Rozszerzanie okna nie kupuje sygnału, tylko opóźnia pętlę zwrotną. 24h daje odczyt następnego dnia i jest zgodne z mentalnym modelem "pierwsza sesja".

### F6 - TTV jest krótkie; problem jest binarny · Impact: High · Confidence: M

Czas od pierwszego otwarcia do pierwszego zapisu (kiedykolwiek):

| bucket | n | powrót d2-7 | uwaga |
|---|---|---|---|
| <1h | 93 | 24.7% | |
| 1-6h | 16 | 25.0% | n<25 |
| 6-24h | 2 | - | n<25, suppressed |
| 24-48h | 1 | - | n<25, suppressed |
| 2-7d | 9 | 100% | **tautologiczne** - zapis w d2-7 oznacza powrót w d2-7; ignorować |
| >7d | 6 | - | n<25, suppressed |
| **nigdy** | **525** | **5.5%** | |

Podkohorta zarejestrowanych (n=205): 46.8% ma kiedykolwiek jakiś zapis; mediana `user_registered` → pierwszy zapis = **4.0 min**, p90 = 126 min; mediana `user_registered` → `onboarding_completed` = **3.0 min**.

**So what**: nie ma "wolno aktywujących się" do przyspieszenia. Jest 525 osób (80.5%), które nie robią zapisu **nigdy**, i 118, które robią go od razu. Interwencja to nie skracanie ścieżki, a postawienie pytania w pierwszej sesji.

### F7 - 66% kohorty nigdy się nie uwierzytelnia (upstream aktywacji) · Impact: Critical · Confidence: M

| segment | n | powrót d2-7 | ma zapis <=24h | średnio zdarzeń w 24h |
|---|---|---|---|---|
| zarejestrowani (`user_registered`) | 205 | 17.6% | 41.5% | 54.3 |
| tylko `user_logged_in`, bez rejestracji (reinstal / nowe urządzenie) | 17 | - | - | - · **n<25, suppressed** |
| **nigdy nieuwierzytelnieni** | **430** | **5.8%** | **4.0%** | **8.4** |

**So what**: 430 z 652 nowych osób otwiera aplikację, widzi splash/auth i wychodzi. To największy pojedynczy wyciek w liczbach absolutnych i leży **przed** aktywacją. Dlatego definicję aktywacji raportujemy z mianownikiem "zarejestrowani" (41.5%), a nie "wszystkie nowe osoby" (17.0%) - inaczej metryka aktywacji będzie się ruszać od zmian w akwizycji i ekranie logowania, nie od wartości produktu. Oba raportujemy obok siebie.

### F8 - Aktywacja spada tygodniowo · Impact: High · Confidence: L

| tydzień kohorty (start nd.) | nowe osoby app | aktywowani (>=1 zapis) | % aktywacji | powrót d2-7 |
|---|---|---|---|---|
| 2026-04-26 | 26 | 7 | 26.9% | 11.5% |
| 2026-05-03 | 56 | 14 | 25.0% | 26.8% |
| 2026-05-10 | 62 | 13 | 21.0% | 8.1% |
| 2026-05-17 | 78 | 21 | 26.9% | 7.7% |
| 2026-05-24 | 46 | 7 | 15.2% | 13.0% |
| 2026-05-31 | 72 | 13 | 18.1% | 11.1% |
| 2026-06-07 | 48 | 8 | 16.7% | 12.5% |
| 2026-06-14 | 45 | 5 | 11.1% | 0.0% |
| 2026-06-21 | 94 | 7 | 7.4% | 3.2% |
| 2026-06-28 | 37 | 6 | 16.2% | 18.9% |
| 2026-07-05 | 38 | 6 | 15.8% | 15.8% |
| 2026-07-12 | 20 | 3 | 15.0% | 0.0% |
| 2026-07-19 | 27 | 2 | 7.4% | 11.1% |
| 2026-07-26 | 3 | 0 | - | - (tydzień ucięty) |

**So what**: trend jest spadkowy (~25% → ~7-15%), ale n/tydzień to 20-94 osób, więc każdy punkt ma +/- kilka pp szumu. Tydzień 2026-06-21 (94 nowe osoby vs baseline 27-32/tyg.) jest anomalią i pokrywa się z odnotowanym w pamięci projektu pikiem QA 06-21..25 - nie czytać go jako pogorszenia produktu. Traktować cały trend jako sygnał do monitorowania po wdrożeniu definicji, nie jako ustalenie.

---

## Analiza przyczyn i hipotezy

- **H1 (POTWIERDZONA)**: "Aha" jest w pierwszym zapisie w pętli terapeutycznej, nie w ukończeniu onboardingu.
  *Za*: 2x2 - onboarding sam +4.3 pp (nieistotne), zapis na wierzchu onboardingu +14.4 pp; lift onboardingu znika po kontroli na głębokość sesji, lift zapisu nie (F4).
  *Przeciw*: graniczna istotność (p=0.08) przy n=35 w komórce "onboarding bez zapisu".
  *Werdykt*: przyjęta, pewność **średnia**.

- **H2 (POTWIERDZONA)**: Wystarczy jeden zapis; więcej nie dokłada.
  *Za*: dose-response 7.4% → 24.4% → 21.6% → 30.0%; `cap>=2` i `cap>=3` bez liftu wewnątrz onboardowanych.
  *Przeciw*: bucket 3+ (30.0%, n=30) sugeruje słabą rampę, ale CI zachodzi na bucket 1.
  *Werdykt*: przyjęta, pewność **średnia**.

- **H3 (ODRZUCONA)**: Istnieje jedna konkretna funkcja, która jest "the aha action".
  *Za*: `reflect_message_sent` i `between_session` mają najwyższe surowe lifty.
  *Przeciw*: n=23-28, CI wszystkich typów zachodzą; wewnątrz onboardowanych żaden typ nie odstaje istotnie od pozostałych zapisów.
  *Werdykt*: **odrzucona** - definicja musi być zbiorem. Pewność **średnia**.

- **H4 (CZĘŚCIOWO ODRZUCONA)**: Efekt zapisu to tylko proxy na "był bardziej aktywny w pierwszej sesji".
  *Za*: zapis występuje niemal wyłącznie u osób z 21+ zdarzeniami w 24h; w pasmie 51+ lift spada do 1.6x.
  *Przeciw*: w pasmie 21-50 zdarzeń, przy porównywalnej głębokości sesji, zapis daje 25.0% vs 5.6% (4.50x, p=0.011).
  *Werdykt*: efekt jest **częściowo** splątany z głębokością, ale nie sprowadza się do niej. Traktować jako wskaźnik wyprzedzający, nie związek przyczynowy. Pewność **średnia**.

- **H5 (ODRZUCONA)**: Problemem jest zbyt długi czas do pierwszej wartości.
  *Przeciw*: mediana rejestracja → pierwszy zapis = 4 minuty; 93/118 aktywacji <1h.
  *Werdykt*: **odrzucona**. Problem jest binarny (80.5% nigdy), nie czasowy. Pewność **wysoka**.

- **H6 (NIETESTOWALNA W TEJ KOHORCIE)**: Zgoda na notyfikacje w pierwszej dobie przewiduje powrót.
  `notification_permission_granted` / `_prompted` / `_denied` istnieją dopiero od **2026-08-04** (weryfikacja: `min(timestamp)`), więc mają zero pokrycia w kohorcie 05-01..07-26. Analogicznie `recording_started` / `recording_saved` od 2026-07-03 (0 trafień w oknie d0-1 kohorty) oraz `workspace_opened` / `quick_capture_*` od 2026-08-04..08-07. **Nie fabrykuję tych liczb** - retest po 2026-09-15.

---

## DEFINICJA AKTYWACJI (do przyjęcia)

> **Aktywowany** = nowy użytkownik, który w ciągu **24 godzin** od pierwszego otwarcia aplikacji rozpoczął lub utworzył **co najmniej jeden** artefakt w pętli terapeutycznej.
>
> **Kwalifikujący zbiór zdarzeń** (dowolne jedno):
> `debrief_started`, `debrief_created`,
> `prep_card_started`, `prep_card_created`, `prep_capture_started`, `prep_capture_submitted`,
> `between_session_started`, `between_session_created`,
> `reflect_message_sent`,
> `health_check_started`, `health_check_completed`,
> `symptom_created`, `symptom_scored`,
> `goal_created`,
> `recording_started`, `recording_saved`,
> `quick_capture_submitted`
>
> **Mianownik podstawowy**: nowi **zarejestrowani** użytkownicy (osoba z `user_registered`), kohortowani po tygodniu pierwszego otwarcia.
> **Mianownik wtórny (raportowany obok)**: wszystkie nowe osoby app-only (`properties.$lib = 'posthog-flutter'`) - pokazuje wyciek na ekranie auth.
> **Wykluczenia**: zdarzenia z `properties.$lib = 'web'` (ruch strony marketingowej) nigdy nie wchodzą ani do mianownika, ani do licznika.

**Wartość bazowa 2026-08-10** (kohorta 05-01..07-26): **41.5%** (85/205) zarejestrowanych; **17.0%** (111/652) wszystkich nowych osób.

**Walidacja predykcyjna definicji**:

| horyzont | aktywowani | nieaktywowani | lift | p | 95% CI różnicy |
|---|---|---|---|---|---|
| powrót d2-7, cała kohorta | 25.2% (28/111) | 7.4% (40/541) | 3.41x | <0.0001 | [+9.5, +26.2] pp |
| powrót d8-28, cała kohorta | 21.7% (23/106) | 7.7% (38/496) | 2.83x | <0.0001 | [+5.8, +22.2] pp |
| powrót d2-7, zarejestrowani | 24.7% (21/85) | 12.5% (15/120) | 1.98x | 0.024 | [+1.3, +23.1] pp |
| powrót d8-28, zarejestrowani | 21.2% (17/80) | 13.9% (15/108) | 1.53x | 0.184 | [-3.7, +18.4] pp |
| >=2 aktywne tygodnie | 35.7% (40/112) | 13.7% (74/540) | 2.61x | <0.0001 | [+12.7, +31.3] pp |
| >=3 aktywne tygodnie | 15.2% (17/112) | 4.8% (26/540) | 3.15x | 0.0001 | [+3.5, +17.3] pp |
| średnia liczba aktywnych dni | 2.67 | 1.43 | 1.87x | - | - |

Uwaga uczciwościowa: na mianowniku "zarejestrowani" lift spada do 1.98x (d2-7) i przestaje być istotny na d8-28 (p=0.18, n=80/108). Silniejsze 3.41x na całej kohorcie jest częściowo napompowane przez 430 osób, które odbijają się od ekranu auth i trywialnie ani nie zapisują, ani nie wracają. **Raportować oba; do celów OKR używać mianownika "zarejestrowani".**

**Kandydat na North Star** (do potwierdzenia osobną analizą): tygodniowa liczba ukończonych pętli terapeutycznych na WAU. Aktywacja wg powyższej definicji koreluje z 2+ aktywnymi tygodniami na poziomie 2.61x, więc jest wiarygodnym wskaźnikiem wyprzedzającym North Star, ale nim samym nie jest.

---

## Instrumentacja

### Decyzja: metryka **wyliczana** (derived), a nie kliencki `user_activated`

Rekomenduję **NIE** dodawać klienckiego zdarzenia `user_activated`. Trzy powody, każdy wystarczający:

1. **Zbiór kwalifikujący jest rozdzielony między dwa emitery.** Weryfikacja `properties.$lib` per zdarzenie (2026-05-01..08-10): `reflect_message_sent`, `symptom_created`, `symptom_scored`, `goal_created`, `debrief_created`, `prep_card_created`, `between_session_created`, `health_check_completed` emituje **wyłącznie backend** (`posthog-python`). Klient (`posthog-flutter`) widzi tylko `*_started`, `recording_*`, `quick_capture_*`. Kliencki `user_activated` systematycznie **przegapiłby 3 z 9 kategorii** (reflect, symptom, goal) - czyli akurat te z najwyższym surowym liftem.
2. **Brak retroaktywności.** Definicja wyliczana daje odczyt dla wszystkich 652 historycznych osób **dziś**. Nowe zdarzenie startuje od zera i jest czytelne po ~4-6 tygodniach, co blokuje jakikolwiek pomiar "przed/po" dla zmian wdrażanych teraz.
3. **Idempotencja "raz na użytkownika, na zawsze" jest gwarancją stanową.** Stan po stronie klienta ginie przy reinstalacji i wylogowaniu oraz duplikuje się między urządzeniami. W tych danych już widać ten problem: **17 osób ma zapis, ale nigdy nie ma `user_registered`** (artefakt scalania `person_id` przez `$identify`), a 17 kolejnych ma tylko `user_logged_in`.

### 1. Definicja wyliczana - do wdrożenia od razu (owner: `growth-analyst` / `posthog-data-extractor`, 0 pracy inżynierskiej)

Kanoniczny HogQL (pełna wersja w Załączniku). Do PostHog dołożyć zapisany insight + kohortę "Activated users" o tej samej logice. **Nie tworzę ich sam - ten agent jest read-only; wdrożenie artefaktów PostHog to zadanie operatora lub `integration-devops`.**

### 2. Person properties ustawiane raz, po stronie backendu (owner: `data-analytics`, emiter `posthog-python`)

Potrzebne, bo person property (inaczej niż zdarzenie) da się użyć jako filtr kohorty, warunek flagi i trigger notyfikacji.

| property | typ | semantyka |
|---|---|---|
| `activated_at` | ISO8601 UTC string | timestamp pierwszego kwalifikującego zapisu; ustawiać przez **`$set_once`** (nigdy nie nadpisywać) |
| `activation_action` | enum: `debrief` \| `prep` \| `between_session` \| `reflect` \| `health_check` \| `symptom` \| `goal` \| `recording` \| `quick_capture` | kategoria pierwszego zapisu (kategoria, nie treść) |
| `time_to_activation_hours` | float (1 miejsce) | `activated_at - user_registered_at`; do raportów **bucketować** (<1h / 1-6h / 6-24h / 1-7d / >7d) |
| `activation_within_24h` | bool | czy `time_to_activation_hours <= 24` licząc od pierwszego otwarcia |

### 3. Zdarzenie `user_activated` - po stronie backendu, nie klienta (owner: `data-analytics`)

Emitować **dokładnie raz** na użytkownika, w momencie utrwalenia pierwszego kwalifikującego artefaktu (ten sam commit, w którym ustawiane jest `activated_at` przez `$set_once`; idempotencję oprzeć na tym, że `activated_at` jest już ustawione).

```
event: user_activated
properties:
  activation_action        : string enum (jak wyżej)
  hours_since_signup       : float, 1 miejsce po przecinku
  hours_since_first_open   : float, 1 miejsce po przecinku
  is_within_24h            : bool
  surface                  : string  # ekran/flow, z którego przyszedł zapis
```

**Zabronione w properties**: treść zapisu, nazwy objawów, wyniki health-check, tytuły celów, jakikolwiek free text, e-mail, Firebase UID. Wyłącznie kategorie, flagi i liczby.

### 4. Spec dla `flutter-mobile` - to, czego tylko klient może dostarczyć

Trzy pozycje. Pozycja B jest najważniejsza: **blokuje diagnozę 82.9% kohorty**, bo dziś nie wiemy, czy nieaktywowani w ogóle zostali o zapis poproszeni.

**A. Dołożyć dwa property do istniejących klienckich zdarzeń zapisu** (`debrief_started`, `prep_card_started`, `prep_capture_started`, `between_session_started`, `health_check_started`, `recording_started`, `quick_capture_started`):

| property | typ | źródło |
|---|---|---|
| `hours_since_signup` | float, 1 miejsce | lokalnie zcache'owany `user_registered_at` z profilu; `null` gdy nieznany (nie zgadywać) |
| `is_first_capture` | bool | lokalna flaga "czy to pierwszy zapis tego użytkownika na tym urządzeniu"; traktowana jako wskazówka, prawdą pozostaje backend |

Cel: liczenie time-to-first-value bez joinów po `person_id` (który dryfuje przy scalaniu `$identify` o 2-24 osoby między przebiegami).

**B. NOWE zdarzenie `first_capture_prompt_shown`** - emitowane, gdy użytkownikowi zostaje **pokazana** propozycja pierwszego zapisu (ekran po onboardingu, empty state na home, karta zachęty):

```
event: first_capture_prompt_shown
properties:
  entry_point            : enum post_onboarding | home_empty_state | timeline_empty_state | moment_card
  prompt_variant          : string   # id wariantu, gotowe na A/B
  capture_types_offered   : array<string>  # np. ["debrief","prep","health_check"]
  hours_since_signup      : float
```

**C. NOWE zdarzenie `first_capture_prompt_dismissed`**:

```
event: first_capture_prompt_dismissed
properties:
  entry_point       : enum (jak wyżej)
  prompt_variant    : string
  dwell_ms          : int      # czas na ekranie przed odrzuceniem
  dismiss_method    : enum back | skip | swipe | app_background
```

**D. Domknięcie jedynej niewidocznej dla klienta kategorii zapisu** - `reflect_message_sent` emituje dziś tylko backend, więc kliencka awaria/latencja wysyłki wiadomości w Reflect jest niewidoczna. Dodać `reflect_message_submitted` (klient, w momencie tapnięcia wyślij) z `hours_since_signup`, `is_first_capture`, `input_mode` (`text` \| `voice`). **Bez treści wiadomości i bez `first_50_chars`** - w kohorcie już raz wyciekł free text przez `onboarding_lead_source_other_text`, tego wzorca nie powtarzać.

**Kryterium ukończenia dla `flutter-mobile`**: po wdrożeniu, dla dowolnego tygodnia kohorty daje się policzyć `first_capture_prompt_shown` → pierwszy zapis jako funnel per `entry_point` i `prompt_variant`, a `hours_since_signup` jest niepuste na >=90% klienckich zdarzeń zapisu.

### 5. Pomiar time_to_first_value (kanonicznie)

`time_to_first_value_hours` = godziny od `user_registered` (backend, `posthog-python`) do pierwszego zdarzenia z kwalifikującego zbioru. Raportować **medianę i p90 w bucketach** (<1h / 1-6h / 6-24h / 1-7d / >7d), nigdy per użytkownik. Bazowa wartość na dziś: mediana 4 min, p90 126 min, pokrycie 46.8% zarejestrowanych.

---

## Rekomendacje (ranking: wpływ x pewność x koszt)

1. **Przyjąć definicję wyliczaną i postawić ją na dashboardzie Activation & Time-to-Value.**
   Owner: operator / `integration-devops` (utworzenie insightu i kohorty w PostHog - `growth-analyst` jest read-only).
   Koszt: ~0. Oczekiwany efekt: jedna liczba tygodniowa zamiast intuicji; wykrywalność spadków aktywacji tydzień po tygodniu.
   Pomiar: `% aktywowanych` w kohorcie tygodniowej zarejestrowanych, baseline **41.5%**.

2. **Zinstrumentować prompt pierwszego zapisu (spec 4B/4C).**
   Owner: `flutter-mobile`.
   Uzasadnienie: 525 z 652 osób nie robi zapisu nigdy, a dziś nie da się rozstrzygnąć, czy to odmowa, czy brak pytania. To najtańsza rzecz, która odblokowuje przyczynę.
   Oczekiwany efekt: mierzalny funnel `prompt_shown` → zapis; brak bezpośredniego ruchu metryki.
   Pomiar: pokrycie `first_capture_prompt_shown` >=90% nowych zarejestrowanych w tygodniu wdrożenia + 2.

3. **Zaadresować wyciek na ekranie auth: 430/652 (66%) nigdy się nie uwierzytelnia.**
   Owner: audyt `ui-ux-designer` → implementacja `flutter-mobile`.
   Uzasadnienie: największy wyciek w liczbach absolutnych, leży przed aktywacją. Ta grupa ma 8.4 zdarzenia w 24h i 5.8% powrotu - to odbicie, nie użytkownicy.
   Oczekiwany efekt: przy obecnym wolumenie (~27-32 nowych osób app/tyg.) zmniejszenie odbicia z 66% do 55% to ~+45 zarejestrowanych na kwartał, co przy 41.5% aktywacji daje ~+19 aktywowanych na kwartał.
   Pomiar: `% nowych osób app z user_registered` w kohorcie tygodniowej, baseline **31.4%** (205/652).

4. **Postawić A/B na prompcie pierwszego zapisu po onboardingu (po wdrożeniu 2).**
   Owner: spec `ui-ux-designer` → implementacja `flutter-mobile` → analiza `growth-analyst`.
   Uzasadnienie: jedyny sposób, żeby przejść z korelacji (F4) na przyczynowość. Jeden zapis wystarczy (F2), więc wariant powinien proponować **jedną**, najniższą tarciowo akcję, nie menu.
   Oczekiwany efekt: aktywacja zarejestrowanych 41.5% → 50-55% (benchmark SMB SaaS 35-50%, top kwartyl 68%).
   Pomiar: aktywacja w 24h per `prompt_variant`, minimum ~250 użytkowników na wariant dla wykrycia +10 pp przy tym baseline.

5. **Dodać `user_activated` po stronie backendu + person properties (spec 2/3).**
   Owner: `data-analytics`.
   Uzasadnienie: potrzebne do targetowania (kohorty, triggery notyfikacji dla nieaktywowanych), nie do samego raportowania metryki.
   Pomiar: `count(user_activated)` w tygodniu zgadza się z definicją wyliczaną w granicach +/-5%; rozbieżność większa = błąd idempotencji.

6. **Powtórzyć tę analizę po 2026-09-15 z kandydatami, których dziś nie dało się przetestować.**
   Owner: `growth-analyst`.
   Zakres: `notification_permission_granted` (istnieje od 2026-08-04), `recording_started`/`recording_saved` (od 2026-07-03), `workspace_opened`, `quick_capture_*`, `app_tour_*`. Wtedy kohorta 08-04..09-01 będzie miała pełne 14 dni obserwacji.

---

## Segmenty i kohorty

| segment | n | aktywacja 24h | powrót d2-7 | status |
|---|---|---|---|---|
| zarejestrowani | 205 | 41.5% | 17.6% | mianownik kanoniczny |
| nigdy nieuwierzytelnieni | 430 | 4.0% | 5.8% | wykluczyć z OKR aktywacji, ścigać osobno (R3) |
| tylko login, bez rejestracji | 17 | - | - | **n<25, suppressed** (prawdopodobnie reinstal / nowe urządzenie) |
| ukończyli onboarding <=24h | 128 | 72.7% (93/128) | 22.7% | tu działa interwencja R4 |
| ukończyli onboarding, bez zapisu | 35 | 0% | 11.4% | **najcenniejszy target** - są w środku i nic nie zapisali |
| kohorta miesięczna maj | ~314 | ~22% | ~12% | |
| kohorta miesięczna czerwiec | ~224 | ~12% | ~8% | zawiera anomalny tydzień QA 06-21 |
| kohorta miesięczna lipiec | ~85 | ~13% | ~11% | n małe |

Segmenty poniżej 25 osób są oznaczone i nieraportowane liczbowo. Kandydaci z n<25 w tabelach liftu (`goal_created` n=10, `orca_named` n=14, `symptom_*` n=15, `subscription_screen_opened` n=21, `content_shared` n=9, komórka `onb=0|cap=1` n=18) pokazane są wyłącznie kierunkowo, na wyraźne polecenie zamawiającego dla wewnętrznego doboru metryki - **nie cytować ich poza tym dokumentem**.

---

## Zastrzeżenia i pewność

- **Korelacja nie jest przyczynowością.** Zapis w pierwszej dobie jest częściowo splątany z głębokością pierwszej sesji (F4). Test stratyfikowany przeżywa tylko w jednym pasmie z sensownym n (21-50 zdarzeń: 4.50x, p=0.011). Definicja jest wskaźnikiem wyprzedzającym; przyczynowość rozstrzygnie wyłącznie A/B (R4).
- **Wielkość próby.** Kohorta n=652, ale kluczowa komórka porównawcza "onboarding bez zapisu" ma n=35 (p=0.080 na d2-7, p=0.29 na d8-28). Wynik na mianowniku "zarejestrowani" traci istotność na d8-28 (p=0.184).
- **Zdarzenia nietestowalne w tej kohorcie** (potwierdzone przez `min(timestamp)`, nie zgadywane): `notification_permission_granted`/`_prompted`/`_denied` od 2026-08-04; `recording_started`/`recording_saved` od 2026-07-03 (0 w oknach d0-1 kohorty); `workspace_opened` od 2026-08-04; `quick_capture_*` od 2026-08-07; `app_tour_*`, `signup_*`, `consent_*`, `welcome_cta_tapped` od ~2026-07-27. Wszystkie zostały ujęte w definicji zbioru kwalifikującego tam, gdzie są semantycznie zapisem, ale nie wnoszą sygnału do tej kohorty.
- **Zdarzeń nie ma wcale**: `paywall_shown`, `subscription_purchase_completed`, `trial_started` - monetyzacja pozostaje niemierzalna w PostHog i nie wchodzi do tej analizy. Nie ma też zdarzenia "summary viewed", więc ostatni etap pętli terapeutycznej nie jest kandydatem, bo nie istnieje w danych.
- **Start ingestu 2026-04-22.** Kohortę otwarto 2026-05-01, co daje 9 dni buforu, ale osoby aktywne przed 04-22 mogły zostać zaklasyfikowane jako "nowe" na początku maja. `user_registered` (backend) zaczyna 2026-05-06, więc pierwszy tydzień kohorty niedoszacowuje rejestracji - to zaniża `41.5%` (mianownik "zarejestrowani" jest tam za mały) i zawyża udział segmentu "nigdy nieuwierzytelnieni".
- **Dryf `person_id`.** Scalanie przez `$identify` przesuwa liczniki osób o 2-24 między przebiegami. Wszystkie liczby absolutne czytać z tolerancją; stosunki i różnice są stabilne. Konkretny objaw w tych danych: 17 osób ma zapis bez `user_registered` (~3% szumu).
- **Testerzy QA / wewnętrzni nie są odfiltrowani** - nie da się ich zidentyfikować bez PII, a `$app_version` nie występuje na zdarzeniach backendowych. Tydzień 2026-06-21 (94 nowe osoby vs baseline 27-32/tyg.) jest niemal pewnie skażony QA.
- **Porównanie z benchmarkiem jest ostrożne**: nasza miara "powrót w dowolnym dniu 2-7" jest **luźniejsza** niż klasyczne D7 (powrót dokładnie w dniu 7), więc 10.4% na naszej miarze jest **gorsze** niż 10% D7 z benchmarku, nie równe.
- **Prywatność**: raport zawiera wyłącznie agregaty. Zero treści terapeutycznych, zero nazw objawów, zero surowych wyników health-check, zero e-maili i Firebase UID. Segmenty <25 osób oznaczone i nieraportowane. Żadne źródło nie było modyfikowane (tylko `SELECT` przez read-only query API); nie utworzono ani nie zmieniono żadnego artefaktu w PostHog.

## Benchmarki

- Retencja aplikacji mobilnych, kategoria Health & Fitness (najbliższa mental health): **D1 ~27%, D7 ~10%, D30 ~4%**; D7 jest punktem przegięcia formowania nawyku, a użytkownicy wracający w D7 są 4-5x bardziej skłonni być aktywni w D30. Źródła: [vmobify - App Retention Benchmarks 2026](https://vmobify.com/blog/app-retention-benchmarks), [Prooflytics - D7/D30 Retention Benchmarks by App Category](https://prooflytics.io/blog/d7-d30-retention-benchmarks-by-app-category), [Plotline - Retention Rates for Mobile Apps by Industry](https://www.plotline.so/blog/retention-rates-mobile-apps-by-industry).
- Activation rate: mediana SaaS **~36-37.5%**, cel dla SMB **35-50%**, top kwartyl **68%**, 90. percentyl **79%**; dwie trzecie nowych użytkowników nigdy nie dochodzi do "aha". Źródła: [Tandem - Activation rate benchmarks 2026](https://usetandem.ai/blog/activation-rate-benchmarks), [Perspective AI - 2026 Customer Onboarding Benchmark Report](https://getperspective.ai/blog/2026-customer-onboarding-benchmark-activation-rates-by-industry), [ProductQuant - SaaS Activation Benchmarks by Industry 2026](https://productquant.dev/blog/saas-activation-benchmarks-by-industry-2026/).

---

## Załącznik

### A. Kanoniczny HogQL definicji aktywacji (do wklejenia jako insight)

```sql
-- Aktywacja: >=1 kwalifikujacy zapis w 24h od pierwszego otwarcia aplikacji.
-- Mianownik: nowi ZAREJESTROWANI (usun 'WHERE reg = 1' dla wszystkich nowych osob app).
SELECT
  toStartOfWeek(fts)                                      AS cohort_week,
  count()                                                 AS n_new_registered,
  countIf(activated = 1)                                  AS n_activated,
  round(100.0 * countIf(activated = 1) / count(), 1)      AS pct_activated,
  round(100.0 * countIf(activated = 1 AND ret27 = 1)
        / nullIf(countIf(activated = 1), 0), 1)           AS pct_ret_d2_7_activated,
  round(100.0 * countIf(activated = 0 AND ret27 = 1)
        / nullIf(countIf(activated = 0), 0), 1)           AS pct_ret_d2_7_not
FROM (
  SELECT
    e.person_id AS pid,
    f.first_ts  AS fts,
    toInt(countIf(e.event = 'user_registered') > 0) AS reg,
    toInt(countIf(e.event IN (
        'debrief_started','debrief_created',
        'prep_card_started','prep_card_created','prep_capture_started','prep_capture_submitted',
        'between_session_started','between_session_created',
        'reflect_message_sent',
        'health_check_started','health_check_completed',
        'symptom_created','symptom_scored',
        'goal_created',
        'recording_started','recording_saved',
        'quick_capture_submitted')
      AND e.timestamp < f.first_ts + INTERVAL 24 HOUR) > 0)          AS activated,
    toInt(countIf(e.timestamp >= f.first_ts + INTERVAL 48 HOUR
                  AND e.timestamp <  f.first_ts + INTERVAL 8 DAY) > 0) AS ret27,
    toInt(countIf(e.timestamp >= f.first_ts + INTERVAL 8 DAY
                  AND e.timestamp <  f.first_ts + INTERVAL 29 DAY) > 0) AS ret828
  FROM events e
  INNER JOIN (
    -- kanoniczne "pierwsze otwarcie": tylko klient mobilny, nigdy ruch web
    SELECT person_id, min(timestamp) AS first_ts
    FROM events
    WHERE timestamp > toDateTime('2026-04-22 00:00:00')
      AND properties['$lib'] = 'posthog-flutter'
    GROUP BY person_id
  ) f ON e.person_id = f.person_id
  WHERE e.timestamp > toDateTime('2026-04-22 00:00:00')
    AND f.first_ts >= toDateTime('2026-05-01 00:00:00')
    AND f.first_ts <  toDateTime('2026-07-27 00:00:00')
  GROUP BY pid, fts
)
WHERE reg = 1
GROUP BY cohort_week
ORDER BY cohort_week
```

### B. Definicje metryk i segmentów

- `first_ts` (pierwsze otwarcie) = `min(timestamp)` po zdarzeniach `properties.$lib = 'posthog-flutter'`, dolna granica `2026-04-22` (start ingestu).
- `ret27` (powrót d2-7) = istnieje zdarzenie w `[first_ts + 48h, first_ts + 8d)`.
- `ret828` (powrót d8-28) = istnieje zdarzenie w `[first_ts + 8d, first_ts + 29d)`; raportowane tylko dla `first_ts < 2026-07-12` (pełna obserwacja).
- `cap_kinds` = liczba odrębnych **kategorii** zapisu (debrief / prep / between / reflect / health_check / symptom / goal / recording / quick_capture) w oknie akcji.
- `breadth` = liczba odrębnych kategorii funkcji w oknie akcji, z wyłączeniem onboardingu, zdarzeń systemowych `$*`, `tab_switched`, `api_error`, `client_error`, `profile_updated`, `therapy_context_updated`, zdarzeń auth i `app_tour_*`.
- "zarejestrowani" = osoba z co najmniej jednym `user_registered`. "nigdy nieuwierzytelnieni" = brak `user_registered` i brak `user_logged_in`.
- Test istotności: dwustronny z-test dla dwóch proporcji z wariancją pulowaną; CI dla różnicy proporcji niepulowane, 95%.

### C. Weryfikacja emiterów (kto emituje który zapis)

| zdarzenie | `$lib` | pierwsze wystąpienie |
|---|---|---|
| `debrief_started` | posthog-flutter | 2026-05-01 |
| `debrief_created` | posthog-python | 2026-05-01 |
| `prep_card_started` | posthog-flutter | 2026-05-01 |
| `prep_card_created` | posthog-python | 2026-05-01 |
| `between_session_started` | posthog-flutter | 2026-05-01 |
| `between_session_created` | posthog-python | 2026-05-01 |
| `reflect_message_sent` | **posthog-python (tylko)** | 2026-05-01 |
| `health_check_started` | posthog-flutter | 2026-05-01 |
| `health_check_completed` | posthog-python | 2026-05-01 |
| `symptom_created` / `symptom_scored` | **posthog-python (tylko)** | 2026-05-01 |
| `goal_created` | **posthog-python (tylko)** | 2026-05-01 |
| `recording_started` / `recording_saved` | posthog-flutter | 2026-07-03 |
| `quick_capture_submitted` | posthog-flutter | 2026-08-07 |
| `onboarding_completed` | posthog-flutter | 2026-05-01 |
| `user_registered` | posthog-python | 2026-05-06 |
| `notification_permission_granted` | posthog-flutter | **2026-08-04** |
| `workspace_opened` | posthog-flutter | **2026-08-04** |

Rozkład `$lib` w okresie 05-01..08-10: `posthog-flutter` 41 540 zdarzeń / 752 osoby; `posthog-python` 20 700 / 371; `web` 5 276 / 1 268. **0 z 852 osób app-first wyemitowało kiedykolwiek zdarzenie `web`** - dlatego dla osób z kohorty można bezpiecznie używać wszystkich ich zdarzeń (klient + backend) bez skażenia ruchem marketingowym.

### D. Pełna tabela liftu, okno akcji 48h, powrót d2-7 (cała kohorta n=652)

| kandydat (d0-1) | n zrobił | powrót | % | n nie zrobił | % | lift | uwaga |
|---|---|---|---|---|---|---|---|
| `goal_created` | 10 | 5 | 50.0 | 642 | 9.8 | 5.10x | **n<25** |
| powrót już w dniu 1 (12-48h) | 44 | 19 | 43.2 | 608 | 8.1 | 5.36x | pół-tautologiczne, nie kandydat |
| `orca_named` / `orca_color_changed` | 14 | 6 | 42.9 | 638 | 9.7 | 4.41x | **n<25** |
| `reflect_message_sent` | 28 | 10 | 35.7 | 624 | 9.3 | 3.84x | p<0.0001 |
| `between_session_*` | 27 | 9 | 33.3 | 625 | 9.4 | 3.53x | p=0.0001 |
| `subscription_screen_opened` | 21 | 7 | 33.3 | 631 | 9.7 | 3.45x | **n<25** |
| `health_check_*` | 38 | 11 | 28.9 | 614 | 9.3 | 3.12x | p=0.0001 |
| breadth >= 4 | 63 | 16 | 25.4 | 589 | 8.8 | 2.88x | |
| `prep_*` | 44 | 11 | 25.0 | 608 | 9.4 | 2.67x | p=0.0011 |
| **którykolwiek zapis** | **112** | **28** | **25.0** | **540** | **7.4** | **3.38x** | **p<0.0001 - wybrany** |
| breadth >= 3 | 90 | 22 | 24.4 | 562 | 8.2 | 2.99x | |
| `debrief_*` | 79 | 19 | 24.1 | 573 | 8.6 | 2.81x | p<0.0001 |
| breadth >= 2 | 121 | 29 | 24.0 | 531 | 7.3 | 3.26x | p<0.0001 |
| `character_card_viewed` | 87 | 20 | 23.0 | 565 | 8.5 | 2.71x | |
| `onboarding_completed` | 129 | 29 | 22.5 | 523 | 7.5 | 3.01x | p<0.0001, ale patrz F1 |
| `timeline_viewed` | 131 | 29 | 22.1 | 521 | 7.5 | 2.96x | pasywna konsumpcja |
| `tab_switched` >= 3 | 105 | 22 | 21.0 | 547 | 8.4 | 2.49x | |
| `symptom_*` | 15 | 3 | 20.0 | 637 | 10.2 | 1.96x | **n<25** |
| `therapy_context_updated` | 161 | 29 | 18.0 | 491 | 7.9 | 2.27x | |
| `onboarding_started` | 193 | 34 | 17.6 | 459 | 7.4 | 2.38x | |
| >2 odrębne ekrany `$screen` | 275 | 46 | 16.7 | 377 | 5.8 | 2.87x | |
| `profile_updated` | 187 | 31 | 16.6 | 465 | 8.0 | 2.08x | |
| `user_registered` | 196 | 31 | 15.8 | 456 | 8.1 | 1.95x | |
| `content_shared` | 9 | 1 | 11.1 | 643 | 10.4 | 1.07x | **n<25** |
| `recording_*` | 0 | 0 | - | 652 | 10.4 | - | zdarzenia od 2026-07-03, brak pokrycia |
| `notification_permission_granted` | - | - | - | - | - | - | zdarzenie od 2026-08-04, **nietestowalne** |

### E. Wykorzystane skrypty

Wszystkie zapytania wykonane read-only przez `scripts/posthog_query.py --sql-file` (POST na `/api/projects/141170/query/`, HogQL). Pliki wsadowe: `act1_discovery.sql` (weryfikacja emiterów i rozmiaru kohorty), `act2_lift.sql` (tabela liftu, załącznik D), `act3.sql` (2x2, dose-response, kontrola na głębokość sesji, TTFV, trend tygodniowy), `act4.sql` (wrażliwość na okno, lift per typ zapisu, wielotygodniowy powrót), `act5.sql` / `act6.sql` (skład kohorty, dokładne liczniki dla okna 24h). Gotcha HogQL napotkana i obejściem: **`toUInt8()` nie istnieje w HogQL - używać `toInt()`**.
