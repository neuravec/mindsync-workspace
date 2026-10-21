# Partia 6: briefy wpisów (5 pozycji, drip 2026-10-08..2026-10-12), trzecia partia stylem Moniki

> Data: 2026-10-07. Autor briefów: `seo-content-writer`. Wykonawca prozy: `blog-writer` przez
> skill `blog-write` (+ `humanizer` z próbką `docs/blog/voice-sample-monika.md`, akcept
> `brand-voice-manager` wg checklisty §2.5, schema od `seo-tech-lead`, hero od
> `graphic-designer`). **Treść po ANGIELSKU.** Format pliku kolejki: `blog/queue/_format.md`.
> Głos: `docs/blog/brand-mindsync.md` §2 (szkielet §2.2, nagłówki §2.1 pkt 12).
>
> **Status bramki KROK 0:** `blog/queue/_preflight-partia6.json`, oczekiwany wynik **7x OK,
> 0 RYZYKO, 0 BRAK** (5 tematów + 2 rezerwy). ⚠ Wynik policzony ręcznie wg logiki skryptu
> (keywordy to dosłowne podciągi katalogu, sprawdzone też przeciw blobom `streaks`
> i `therapist-sharing`). Przed przekazaniem do `blog-writer` lider uruchamia:
> `python scripts/blog-coverage-preflight.py --temat blog/queue/_preflight-partia6.json`.
>
> **Skąd tematy:** pozycja 6 z `blog/queue/_gsc-odswiezenia.md`, zaakceptowana przez operatora
> 2026-09-28: nowe wpisy wokół trzech klastrów, które Google już łączy z nami (koszty terapii,
> zmiana terapeuty i platformy, prywatność aplikacji). Raport
> `seo/blog/gsc-wyniki/BLOG-WYNIKI-2026-10-07.md`.
>
> **Status danych (wprost):** żadna fraza główna tej partii **nie ma jeszcze wyświetleń w GSC**
> (to nowe intencje obok klastrów, które łapią). Jedyne dosłowne zapytanie z GSC użyte w partii
> to pytanie FAQ wpisu 03 (`what should i do if my betterhelp therapist isn't the right fit?`,
> 9 wyświetleń, poz. 23,1 na wpisie o dopasowaniu, czyli poza top 15, więc wolno je przejąć).
> Pozostałe frazy i pytania FAQ pochodzą z researchu SERP 2026-10-07 (tytuły stron i pytania,
> które SERP zwraca jako tytuły), **bez wolumenów i bez KD**. Ahrefs w subagencie niedostępny:
> zapytania do Keywords Explorer są na końcu pliku, do pobrania w sesji głównej przed pisaniem
> (jeśli wolumen którejś frazy głównej wyjdzie 0, a poboczna ma popyt, zamieniamy je miejscami
> w H1 i H2, reszta briefu bez zmian). Po pierwszych wyświetleniach:
> `scripts/gsc/blog-partia-frazy.py` i korekta H2 oraz FAQ na frazy z liczbami.
>
> ⚠ **Termin:** pierwszy wpis ma datę 2026-10-08, czyli jutro. Jeśli proza nie zdąży przed
> dripem o 07:00, przesuń CAŁĄ partię o tyle samo dni z zachowaniem kolejności (linki biegną
> tylko wstecz, więc przesunięcie całości niczego nie psuje).

## Zasady wspólne dla wszystkich 5 briefów (nie powtarzam ich w każdym)

1. **Szkielet Moniki jest nadrzędny.** Kolejność: otwarcie-rozpoznanie (bez H2, 60-120
   słów) → skąd to się bierze → jak to wygląda w życiu → co mówią badania → co możesz
   spróbować → akapit o apce w rytmie „This is what MindSync's [funkcja] is for. Log
   [3 konkrety z wpisu]. Give it time, and [funkcja] turns those entries into something you
   can see: [co]. Then [co dalej]." → jedno osobiste pytanie do czytelnika → blok
   `[FEATURES:]` → FAQ. Sekcje 2-4 wolno przestawić, apka i pytanie zawsze na końcu.
   **Długość: 900-1400 słów bez FAQ.** Jeden H2 na sekcję. Fraza główna w H1 i w jednym H2,
   bez upychania. Wpisy 01, 03 i 05 są praktyczne z natury: sekcja „co spróbować" może być
   najdłuższa (do 400 słów), ale „skąd to się bierze" i badania zostają.
2. **Nagłówki jak zdania z rozmowy, często z dwukropkiem** (§2.1 pkt 12). Propozycje H2 niżej
   są wiążące co do sensu i miejsca frazy; autor może je doszlifować głosem Moniki, ale H2
   z frazą zostaje dosłownie.
3. **Humor:** 2-4 konkretne, przesadzone obrazki na wpis, najwięcej w otwarciu i w części
   praktycznej, zero w akapitach o badaniach, pieniądzach w kryzysie i o cierpieniu. Haczyki
   w briefach to materiał, nie gotowe zdania. Maksymalnie jedna etykieta „Fun fact:" albo
   „Disclaimer:" na wpis.
4. **Zero zmyślonej biografii Moniki.** „I" tylko jako opinia („I feel like..."). Żadnych
   anegdot w pierwszej osobie, żadnych „my client", „a friend of mine". Jedyny prawdziwy fakt
   biograficzny dostępny dla marki: założyciel wydał około 130 000 USD na terapię przez 10 lat
   (już na żywo w `is-therapy-worth-the-money`); wolno go użyć raz w 01 albo 05, nie w obu.
5. **Zakaz obu myślników.** Zero U+2014 i zero U+2013 w tytule, meta, zajawce, treści,
   kartach i schema. Przebuduj zdanie. Zakres liczbowy zwykłym łącznikiem: „$30-$70",
   „3-6 sessions". Bramka dripu łapie tylko U+2014, półpauzę sprawdź wyszukiwarką po znaku.
6. **YMYL:** zero diagnozowania, zero obietnic zdrowotnych, zero zniechęcania do terapii i leków,
   zero treści kryzysowych. MindSync uzupełnia terapię, nie zastępuje jej. **Nowe w tej partii:
   pieniądze i prawo.** 01 i 05 to informacja, nie porada finansowa, podatkowa ani prawna; każdy
   z nich ma jedno zdanie „this is not financial or legal advice, and your plan or state may
   differ". **Każda kwota i każdy procent ze źródłem i datą** („according to Open Path's own
   site in October 2026"). Kontekst USA nazwany wprost w pierwszym akapicie z liczbami.
   Żadnych zgadywanych stawek, żadnych „usually around $X" bez źródła.
7. **Funkcje `planned` nie istnieją w treści:** `therapist-sharing` i `streaks`. „Bring it to
   your next session" i „show your new therapist" wolno tylko jako czynność czytelnika
   (czyta, opowiada, pokazuje telefon w gabinecie), zero sugestii wysyłania czegoś terapeucie
   z apki. Habit Tracker i ekran wyboru trybu w Reflect są poza katalogiem. **Eksportu danych
   w apce NIE MA:** żadne „export", „download your history", „send your notes as a file".
   **Nazwy funkcji z katalogu:** „Between-session voice notes", „Wellbeing check-ins",
   „Mood & focus-area trends", „Weekly & monthly summaries", „Therapy timeline", „Workspace",
   „Reflect", „Prep Card", „After-therapy debrief", „Session recording & summaries", „Goals",
   „Therapy relationship check", „Homework & to-dos".
8. **Dwie lekcje z partii 4 (twarde):** Mood & focus-area trends wykreśla tylko oceny
   z check-inów (nie notatki, nie ludzi, nie tematy); voice notes to transkrypcje bez
   odtwarzania (nigdy „listen back", zawsze „read back").
9. **Karty:** jedna `[FEATURE:]` inline plus blok `[FEATURES:]` z trzema pozycjami przed FAQ.
   Tylko id z listy danego briefu, żadne id nie powtarza się w obrębie wpisu. Zdania kart są
   nowe (nie przepisuj sformułowań z partii 1-5). Zero cen.
10. **FAQ:** H2 dokładnie `Frequently asked questions`, pytania w H3 dokładnie w brzmieniu
    z briefu, 4-5 sztuk. Odpowiedź 40-70 słów, pierwsze zdanie to pełna odpowiedź (GEO),
    dalej warunek albo zastrzeżenie. Głosem Moniki, bez humoru. Apostrof prosty (').
11. **Badania i źródła instytucjonalne:** opowiadane jak historia z rokiem na początku
    („In 2016, Burlingame and colleagues..."). Nazwa czasopisma albo instytucji w zdaniu, link
    w tę nazwę (RichText `a`), nigdy goły URL. Autor **weryfikuje każdą liczbę u źródła
    pierwotnego**; pozycje „do potwierdzenia" idą jakościowo, jeśli liczby nie da się
    potwierdzić. Po każdym badaniu 1-2 krótkie zdania „co to znaczy dla ciebie" i jedno uczciwe
    zdanie o granicy. Strony pomocy firm (BetterHelp, Talkspace, OpenAI) to źródło faktu
    o produkcie, nie badanie: „According to Talkspace's help center..."
12. **Linki wewnętrzne wyłącznie względne:** `<a href="/journal/slug">`, `<a href="/features">`,
    `<a href="/faq">`, `<a href="/privacy-policy">`, `<a href="/pre-order/...">`. Nigdy
    `https://mindsync.app/...` w treści.
13. **Każdy wpis linkuje do min. jednego wpisu NA-PROGU** (poz. 8-20 w GSC): `sunday-scaries`,
    `what-to-do-when-your-therapist-is-not-the-right-fit`, `therapy-hangover`,
    `what-to-do-between-therapy-sessions`, `regulate-nervous-system-between-therapy-sessions`,
    `are-mental-health-apps-private`, `how-to-prepare-for-a-therapy-session`. Konkretne slugi
    i anchory w mapach linkowania, oznaczone **[NA-PROGU]**. Najmocniejszy wpis
    `how-to-remember-what-you-talk-about-in-therapy` dostaje link z 01, 03 i 04.
14. **Linkowanie w partii biegnie wyłącznie wstecz** (tabela niżej), więc w tej partii nie ma
    `[LINK-LATER:]`. Jeśli wpis-cel się opóźni, a wpis linkujący nie, link zamień na
    `[LINK-LATER: <slug> | <ten sam anchor>]` i zgłoś liderowi.
15. **Pole `glos`: `"monika-v1"`** w każdym pliku kolejki (wymóg `blog-voice-check.py`).

## Kolejność publikacji, daty i topologia linkowania

| data | # | plik w kolejce | slug (`seo_url`) | klaster | kategoria | `kolor` | linki wstecz w partii |
|---|---|---|---|---|---|---|---|
| 2026-10-08 | 01 | `2026-10-08_how-to-afford-therapy.json` | `how-to-afford-therapy` | 4 | Therapy | `#339499` | brak (tylko wpisy na żywo) |
| 2026-10-09 | 02 | `2026-10-09_is-it-safe-to-talk-to-ai-about-mental-health.json` | `is-it-safe-to-talk-to-ai-about-mental-health` | 6 | MindSync Tips | `#1f3d38` | brak |
| 2026-10-10 | 03 | `2026-10-10_how-to-switch-therapists.json` | `how-to-switch-therapists` | 4 | Therapy | `#e8af0a` | → 01 |
| 2026-10-11 | 04 | `2026-10-11_starting-over-with-a-new-therapist.json` | `starting-over-with-a-new-therapist` | 1 | Therapy | `#3c67a5` | → 03 |
| 2026-10-12 | 05 | `2026-10-12_does-insurance-cover-therapy.json` | `does-insurance-cover-therapy` | 4 | Therapy | `#339499` | → 01, → 03 |

Kolory: ostatni opublikowany wpis (`when-to-stop-therapy`, 2026-10-05) ma `#ff9f8a`, więc
sekwencja `#ff9f8a` → `#339499` → `#1f3d38` → `#e8af0a` → `#3c67a5` → `#339499`, sąsiednie różne.

Klastry przeplatane (4, 6, 4, 1, 4), żaden klaster nie wychodzi dwa dni z rzędu.

**Wzmocnienie po partii (zadanie PATCH dla `webflow-publisher`, nie dla autora; dozwolone
przed 26.10, bo to tylko linki, por. „Zasada oceny" w `_gsc-odswiezenia.md`):**
- z `is-therapy-worth-the-money` do `how-to-afford-therapy` (anchor „ways to bring the cost
  down") i do `does-insurance-cover-therapy` (anchor „what your insurance will actually pay"),
  w akapicie o sliding scale i w FAQ o koszcie,
- z `how-to-afford-therapy` do `does-insurance-cover-therapy` (anchor „how to read your own
  coverage"), w miejscu zdania o ubezpieczeniu (forward link, dopiero po publikacji 05),
- z `what-to-do-when-your-therapist-is-not-the-right-fit` do `how-to-switch-therapists`
  (anchor „how switching actually works") i do `starting-over-with-a-new-therapist` (anchor
  „what to bring to the next therapist"), w sekcji „What to take with you to the next therapist",
- z `are-mental-health-apps-private` do `is-it-safe-to-talk-to-ai-about-mental-health`
  (anchor „what happens to what you tell a chatbot"), w akapicie o AI w sekcji o analityce,
- z `how-to-choose-a-therapist` do `does-insurance-cover-therapy` (anchor „checking your
  insurance before the first call") w H3 „Access and logistics".

---

# 01. How to afford therapy

**1. Meta**
- `seo_url`: `how-to-afford-therapy` | plik: `blog/queue/2026-10-08_how-to-afford-therapy.json`
- kategoria: `Therapy` | `kolor`: `#339499` | `planowana_data`: **2026-10-08**
- `tagi`: `["therapy-logistics", "cost"]`
- H1: „The Price Tag Isn't the Only Door: How to Afford Therapy"
- `meta_title` (ok. 50 zn.): „How to Afford Therapy: Ways to Pay Less | MindSync"
- `meta_description` (ok. 155 zn.): „Cost is one of the top reasons people skip therapy. Sliding
  scale fees, training clinics, group therapy, and the questions that get you a lower rate."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `how to afford therapy`
- poboczne: `affordable therapy`, `sliding scale therapy`, `low cost therapy`, `how to pay less
  for therapy`, `therapy without insurance`, `good faith estimate therapy`
- intencja: ktoś wie, że potrzebuje terapii (albo już chodzi i budżet pęka), widzi stawki
  i szuka realnych sposobów, żeby płacić mniej. Wieczór, aplikacja banku otwarta w drugiej
  karcie. Pyta „jak", nie „czy warto".
- luka: SERP (SIRUM „19 options", Simply Psychology, Kindermind, gabinety z własnym sliding
  scale) to listy opcji bez kontekstu. **Nikt nie mówi uczciwie o dwóch rzeczach:** (1) że
  terapia grupowa wypada tak samo jak indywidualna, gdy porównuje się tę samą metodę i dawkę
  (Burlingame i wsp. 2016), co czyni ją najmocniejszą tańszą opcją, a nie „gorszą wersją";
  (2) że oszczędzanie przez rzadsze sesje ma cenę (Bruijniks i wsp. 2020: dwie sesje
  tygodniowo dawały lepsze wyniki w depresji niż jedna), więc „chodź rzadziej" to rozmowa
  z terapeutą, nie samodzielna decyzja. Plus mało znane prawo USA: **Good Faith Estimate**
  (No Surprises Act, od 2022) dla płacących samodzielnie. Nasz kąt: cena za sesję to nie
  jedyne drzwi; da się zmienić format, miejsce i to, ile wyciągasz z każdej godziny.
- ⚠ granica: NIE odpowiadamy na „is therapy worth the money / is therapy expensive / how much
  is therapy a month" (to `is-therapy-worth-the-money`, poz. 6-19 w GSC). Średnie stawki
  (SimplePractice, Grow) najwyżej jednym zdaniem z linkiem, bez powtarzania liczb. Liczba
  sesji: link do `how-long-therapy-takes-to-work`. Ubezpieczenie: jedno zdanie bez linku
  (05 jest później; link dojdzie PATCH-em).

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** obserwacja o tym, jak żyjemy, spokojnie i trochę ironicznie,
  np. o tym, że do terapii przekonujesz się dwa lata, a potem zniechęca cię jedna liczba na
  stronie gabinetu. Haczyki: kalkulator w telefonie otwarty częściej niż kalendarz sesji;
  liczenie, ile kaw to jedna sesja (i dochodzenie do wniosku, że kawy też trzeba odstawić);
  zamykanie karty z cennikiem „na chwilę" na trzy miesiące.
- **H2: „Why does therapy cost what it does?"** (skąd to się bierze)
  - prostym językiem: płacisz za godzinę wykwalifikowanej osoby plus czas, którego nie widzisz
    (notatki, superwizja, licencja); część terapeutów nie przyjmuje ubezpieczeń, bo rozliczenia
    są niskie i papierowe. Jedno zdanie z Zhu i wsp. 2024 (około jedna trzecia terapeutów
    w prywatnej praktyce nie przyjmowała ubezpieczenia); szczegóły zostają na 05.
  - jedno zdanie o średnich cenach i link do `is-therapy-worth-the-money` (anchor niżej).
  - slot na **„Fun fact:"**: w USA, jeśli płacisz sam, od 2022 masz prawo do pisemnego
    kosztorysu przed pierwszą sesją (Good Faith Estimate), a jeśli rachunek przekroczy go
    o 400 USD lub więcej, możesz go zakwestionować (CMS). Brzmienie tylko w granicach źródła.
- **H2: „What 'I can't afford therapy' usually looks like:"** (jak to wygląda)
  - lista w drugiej osobie, 4-5 punktów: odkładasz szukanie, bo zakładasz najwyższą stawkę;
    chodzisz, ale co sesję liczysz w głowie, ile kosztuje każda minuta milczenia; skreślasz
    terapeutę po cenie na stronie, nie pytając o niższą stawkę; robisz przerwę „na miesiąc",
    która trwa rok; wybierasz najtańszą opcję, a potem czujesz, że „nie zasługujesz" na lepszą.
  - czułość bez lukru, w jej duchu: to nie jest brak determinacji, tylko rachunek.
- **H2: „What research turned up:"** (badania i dane)
  - SAMHSA, *National Survey on Drug Use and Health*: wśród dorosłych, którzy czuli, że
    potrzebują pomocy i jej nie dostali, koszt był jednym z najczęściej podawanych powodów.
    ⚠ Liczbę (wyszukiwanie wskazuje ok. 60% w NSDUH 2023) podaj WYŁĄCZNIE po potwierdzeniu
    w tabelach najnowszego wydania (SAMHSA opublikowała kolejne wydanie 2026-07-27); inaczej
    jakościowo: „cost was one of the most common reasons". Wniosek: „You're not the only one
    doing this math."
  - 2016, Burlingame, Seebeck, Janis i wsp., *Psychotherapy*: 25 lat badań, w których ta sama
    terapia była prowadzona indywidualnie i w grupie; przy tej samej metodzie, pacjentach
    i dawce wyniki były równoważne, bez różnic w poprawie, remisji ani rezygnacji. Wniosek
    dwoma zdaniami: „Group isn't therapy's budget version. For a lot of problems, it's the same
    therapy with more chairs." Granica: chodzi o porównania tej samej metody; grupa nie pasuje
    każdemu i nie do każdego problemu, o to pytaj terapeutę.
  - 2020, Bruijniks i wsp., *British Journal of Psychiatry*: osoby z depresją losowo przydzielone
    do jednej albo dwóch sesji tygodniowo (CBT albo IPT); przy dwóch sesjach objawy spadały
    szybciej i mniej osób rezygnowało. Wniosek: rzadsze sesje to też decyzja kliniczna, nie
    tylko budżetowa, więc rozmawiaj o niej z terapeutą. Granica: jedno badanie, depresja,
    Holandia.
- **H2: „How to afford therapy without giving up on it:"** (fraza główna w H2; co spróbować;
  tryb rozkazujący, 5 kroków)
  1. Ask for the sliding scale out loud. Wiele gabinetów ma kilka miejsc ze zniżką i ich nie
     reklamuje. Gotowe zdanie: „Do you offer a sliding scale, or do you keep any reduced-fee
     spots?" Haczyk: to pytanie zajmuje 4 sekundy i nikt jeszcze od niego nie umarł.
  2. Look where the fees are lower by design: uczelniane kliniki szkoleniowe (praktykanci pod
     superwizją), ośrodki środowiskowe i FQHC z opłatą zależną od dochodu, sieci typu Open Path
     Collective (stawki i jednorazowa opłata członkowska tylko z ich strony, z datą
     sprawdzenia). Bez rankingów, bez poleceń konkretnych gabinetów.
  3. Check what your job already pays for: Employee Assistance Program, często kilka
     darmowych, poufnych sesji (liczbę „3-6" podaj tylko ze źródłem, patrz §8; inaczej „a small
     number of free sessions"). Gotowe zdanie do HR nie jest potrzebne: numer zwykle jest
     w materiałach benefitowych.
  4. Ask about group, or about spacing sessions out, with your therapist, not instead of
     them. Tu Burlingame i Bruijniks w praktyce, jednym akapitem.
  5. Make each paid hour carry more: przyjdź z jednym tematem, wyjdź z jedną rzeczą do
     zrobienia, nie spędzaj 15 minut na streszczaniu tygodnia. Tu inline karta `session-prep`.
     Link do `how-to-prepare-for-a-therapy-session` **[NA-PROGU]** i do
     `what-to-do-between-therapy-sessions` **[NA-PROGU]**.
  - spokojny akapit: jedno zdanie o ubezpieczeniu („if you have insurance, the first question
    is whether your plan covers outpatient mental health, and that deserves its own guide"),
    bez linku; zdanie „this is not financial advice, and programs differ by state".
  - opcjonalnie jedno zdanie o lęku przed pieniędzmi w niedzielę wieczorem z linkiem do
    `sunday-scaries` **[NA-PROGU]** (tylko jeśli siada naturalnie; nie na siłę).
  - puenta, w stylu „The cheapest session is the one you actually use."
- **Akapit o apce:** „This is what MindSync's Prep Card is for. Log the one topic you can't
  stop circling, the question you want answered this week, and the homework you said you'd
  try. Give it time, and your Weekly & monthly summaries turn those entries into something you
  can read: [what each month of sessions actually moved]. Then walk into the next paid hour
  already at the point where the work starts." Bez cen MindSync, bez „cheaper than therapy",
  bez linku do /membership (nie w tym wpisie: czytelnik liczy każdego dolara).
- **Pytanie do czytelnika:** np. „If the price weren't the first thing you saw, which option
  would you have asked about first?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: How can I afford therapy with no money?
  - H3: What is sliding scale therapy?
  - H3: Can you ask a therapist for a lower rate?
  - H3: Is group therapy as effective as individual therapy?
  - H3: What is a good faith estimate for therapy?
  - ⚠ „with no money": bez obietnic „free therapy"; uczciwie: ośrodki środowiskowe, kliniki
    szkoleniowe i EAP bywają darmowe albo prawie, dostępność zależy od miejsca. Zero linii
    kryzysowych jako „taniej terapii" (to nie terapia; temat kryzysowy wymaga decyzji
    operatora).

**4. Karty funkcji** (bramka: session-prep, workspace, homework, goals, mood-trends, summaries,
session-recording; używamy czterech)
- inline w „How to afford therapy..." (krok 5):
  `[FEATURE: session-prep | The topic you picked on Wednesday, waiting on one card when the paid hour starts, so it does not go on remembering what happened.]`
- blok przed FAQ:
  `[FEATURES: Getting more from every paid hour || homework | The thing you agreed to try lands on today's list, which is where cheap progress usually happens. || summaries | A month of entries read back to you, useful when you are deciding with your therapist whether to change how often you meet. || workspace | Questions and threads you collect during the week, parked until the session instead of paid for twice.]`

**5. Mapa linkowania** (tylko wpisy na żywo)
- `<a href="/journal/is-therapy-worth-the-money">` anchor „what a course of therapy usually
  costs" (sekcja „Why does therapy cost what it does?")
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` **[NA-PROGU]** anchor „walk in
  with one topic instead of a recap" (krok 5)
- `<a href="/journal/what-to-do-between-therapy-sessions">` **[NA-PROGU]** anchor „the part of
  therapy that costs nothing: the week in between" (krok 5)
- `<a href="/journal/how-to-remember-what-you-talk-about-in-therapy">` anchor „keeping what you
  paid for after you leave the room" (krok 5 albo akapit o apce)
- `<a href="/journal/how-long-therapy-takes-to-work">` anchor „how many sessions change usually
  takes" (krok 4, jedno zdanie)
- `<a href="/journal/sunday-scaries">` **[NA-PROGU, opcjonalnie]** anchor „the Sunday-night
  money dread"
- **Landing partner:** brak (żaden landing nie pasuje bez sprzedażowego tonu).

**6. GEO**
- Definicja sliding scale therapy, 40-60 słów: opłata za sesję dopasowana do dochodu
  klienta, ustalana przez gabinet albo ośrodek; o dostępne miejsca trzeba zwykle zapytać.
- Odpowiedź na „How can I afford therapy?", 50-70 słów: 4 drogi (sliding scale, kliniki
  szkoleniowe i ośrodki środowiskowe, EAP, grupa) + zastrzeżenie USA.
- Definicja Good Faith Estimate, 40-60 słów (CMS, No Surprises Act, osoby bez ubezpieczenia
  i płacące samodzielnie, próg sporu 400 USD).

**7. Hero**
- Wariant „codzienny moment": słoik na drobne monety na parapecie obok kubka i notesu,
  miękkie poranne światło; paleta sand i mint; bez banknotów, bez kalkulatora, bez osoby.
- `hero_image_alt`: „A small glass jar of coins beside a mug and a notebook on a sunlit
  windowsill"
- nazwa pliku hero: `how-to-afford-therapy-hero.webp`

**8. Źródła (sprawdzone 2026-10-07; autor weryfikuje u źródła pierwotnego)**
- **POTWIERDZONE (strona CMS i materiały CMS).** No Surprises Act, Good Faith Estimate dla
  osób bez ubezpieczenia i płacących samodzielnie, od 2022-01-01; obejmuje psychoterapię;
  spór przy przekroczeniu o 400 USD lub więcej.
  https://www.cms.gov/files/document/gfe-and-ppdr-requirements-slides.pdf
  (dla czytelnika lepsza strona konsumencka: https://www.cms.gov/nosurprises, autor wybiera
  jedną i sprawdza brzmienie).
- **POTWIERDZONE (abstrakt).** Burlingame G.M., Seebeck J.D., Janis R.A. i wsp., 2016,
  *Psychotherapy* 53(4):446-461, „Outcome differences between individual and group formats
  when identical and nonidentical treatments, patients, and doses are compared: A 25-year
  meta-analytic perspective". https://doi.org/10.1037/pst0000090 ⚠ DOI potwierdź; 68 prac
  z obu formatami w jednej publikacji; brak różnic w akceptacji, remisji, poprawie
  i przedwczesnym kończeniu.
- **POTWIERDZONE (Cambridge).** Bruijniks S.J.E. i wsp., 2020, *British Journal of Psychiatry*
  216(4):222-230, „The effects of once- versus twice-weekly sessions on psychotherapy outcomes
  in depressed patients".
  https://www.cambridge.org/core/journals/the-british-journal-of-psychiatry/article/effects-of-once-versus-twiceweekly-sessions-on-psychotherapy-outcomes-in-depressed-patients/C43C681866F3663A5C55BAFA2A99B8CB
  d = 0.55 w 6. miesiącu, mniej rezygnacji (16 vs 32). W tekście wystarczy „faster, and fewer
  people dropped out".
- **POTWIERDZONE (pełny tekst).** Zhu J.M., Huntington A., Haeder S., Wolk C., McConnell K.J.,
  2024, *Health Affairs Scholar* 2(9):qxae110, „Insurance acceptance and cash pay rates for
  psychotherapy in the US". https://academic.oup.com/healthaffairsscholar/article/2/9/qxae110/7750928
  175 083 terapeutów z katalogu Psychology Today (IX-XII 2023); ok. 35% nie przyjmowało
  ubezpieczenia. W 01 tylko „about a third"; liczby stanowe i stawki zostają na 05.
- **DO POTWIERDZENIA (liczba).** SAMHSA, NSDUH 2023, powody nieskorzystania z leczenia mimo
  odczuwanej potrzeby (koszt). https://www.samhsa.gov/data/sites/default/files/reports/rpt47095/National%20Report/National%20Report/2023-nsduh-annual-national.pdf
  ⚠ Sprawdź, czy jest nowsze wydanie (komunikat SAMHSA 2026-07-27) i weź liczbę z tabeli,
  nie z wyszukiwarki.
- **POTWIERDZONE (strona organizacji, stan 2026-10).** Open Path Collective: jednorazowa
  opłata członkowska 65 USD, sesje 30-70 USD (pary i rodziny do 80 USD).
  https://openpathcollective.org/client/ ⚠ Stawki sprawdź w dniu pisania i podaj z datą.
- **DO POTWIERDZENIA (EAP).** Typowo 3-6 darmowych sesji na sprawę; źródło badawcze:
  Attridge M., „The Current State of Employee Assistance Programs in the United States:
  A Research-based Commentary" (2023, ResearchGate
  https://www.researchgate.net/publication/373160882). Jeśli nie da się potwierdzić, pisz
  jakościowo.
- **Czego autor ma NIE twierdzić:**
  - konkretnych stawek gabinetów, klinik czy platform bez źródła i daty,
  - że terapia grupowa „zawsze" działa tak samo; tylko przy tej samej metodzie i dawce,
  - że warto chodzić rzadziej, żeby oszczędzić (decyzja z terapeutą),
  - że aplikacje (w tym MindSync) są tańszym zamiennikiem terapii,
  - niczego o kredytach, ratach, kartach kredytowych na terapię,
  - linii kryzysowych jako „darmowej terapii".

**9. Czego NIE robić**
- Nie odpowiadaj na „czy warto"; to drugi wpis.
- Zero nazw płatnych platform online z cenami (BetterHelp, Talkspace): ich ceny zmieniają się
  i nie chcemy rankingu.

---

# 02. Is it safe to talk to AI about mental health?

**1. Meta**
- `seo_url`: `is-it-safe-to-talk-to-ai-about-mental-health` | plik:
  `blog/queue/2026-10-09_is-it-safe-to-talk-to-ai-about-mental-health.json`
- kategoria: `MindSync Tips` | `kolor`: `#1f3d38` | `planowana_data`: **2026-10-09**
- `tagi`: `["data", "privacy"]`
- H1: „Is It Safe to Talk to AI About Mental Health? Where the 2 a.m. Confession Goes"
- `meta_title` (ok. 56 zn.): „Is It Safe to Talk to AI About Mental Health? | MindSync"
- `meta_description` (ok. 158 zn.): „People tell chatbots things they never say out loud. What AI
  companies keep, what they train on, why there is no legal privilege, and the settings to
  check first."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `is it safe to talk to AI about mental health`
- poboczne: `is ChatGPT private`, `AI therapy privacy`, `does ChatGPT use my conversations for
  training`, `are AI chats confidential`, `is it safe to tell ChatGPT personal things`,
  `AI chatbot mental health data`
- intencja: ktoś już rozmawia z chatbotem o tym, co go gryzie (albo właśnie zamierza),
  i nagle pyta: gdzie to trafia, kto to czyta, czy ktoś może to kiedyś wyciągnąć. Często
  późny wieczór, po długiej rozmowie.
- luka: SERP (Healthgrades, Medical News Today, Northeastern, gabinety) miesza dwa tematy:
  czy AI jest dobrym „terapeutą" i czy jest prywatne. Prywatność dostaje akapit ogólników
  („avoid sharing personal data"). **Nikt nie opowiada badania, które wyjaśnia, dlaczego
  w ogóle mówimy chatbotom tak dużo** (Lucas i wsp. 2014: ludzie, którzy myśleli, że rozmawiają
  z komputerem, mniej się bali ujawniania i mniej się kreowali niż ci, którzy myśleli, że
  steruje człowiek) **ani nie zestawia trzech konkretów:** brak tajemnicy zawodowej (Altman,
  VII 2025), nakaz sądowy, który przez ponad cztery miesiące kazał OpenAI trzymać nawet
  usunięte czaty (sprawa NYT, 13.05-26.09.2025), i realne przełączniki (trening, czaty
  tymczasowe). Nasz kąt: chatbot jest wygodny, bo nie wygląda na świadka; prywatność zależy od
  ustawień i od firmy, a nie od tego, jak intymnie się czujesz.
- ⚠ granica: czytanie polityki prywatności aplikacji (7 słów, HIPAA, usuwanie konta, „which
  mental health apps do not sell data", „what ai mental health app will not share my personal
  conversations") należy do `are-mental-health-apps-private` (poz. 1-11 na tych zapytaniach;
  FAQ tam dopisuje pozycja 4 `_gsc-odswiezenia`). Tu: rozmowy z AI, ogólne chatboty
  i funkcje AI w aplikacjach. Jedno zdanie i link do checklisty.

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** „Do any of these sound familiar?" + trzy scenki, ostatnia krótka
  z mrugnięciem. Haczyki: o 1:40 w nocy piszesz do chatbota akapit, którego nie powiedziałeś
  przyjaciółce przez trzy lata; prosisz AI o „rozpisanie" kłótni z partnerem, z imionami
  i cytatami; potem zamykasz kartę z uczuciem, że to było „między nami". (Między wami i serwerem
  w innym stanie.)
- **H2: „Why it's so easy to tell a chatbot everything"** (skąd to się bierze)
  - mechanizm: brak twarzy, brak oceny, brak ryzyka, że ktoś zmieni o tobie zdanie; chatbot nie
    wzdycha i nie patrzy na zegarek. Analogia: rozmowa z obcym w pociągu, tylko że pociąg
    zapisuje każde słowo.
  - fragment cytowalny (GEO): dlaczego czujemy prywatność, której nie ma.
  - slot na **„Fun fact:"**: sam szef OpenAI powiedział publicznie w lipcu 2025, że rozmowy
    z ChatGPT nie mają tajemnicy prawnej, jaką mają rozmowy z terapeutą, lekarzem czy
    prawnikiem (TechCrunch). Brzmienie tylko w granicach źródła; to wypowiedź, nie przepis.
- **H2: „What actually happens to what you type:"** (jak to wygląda; ujęcie praktyczne)
  - lista w drugiej osobie, 4-5 punktów, każdy jako fakt + co to znaczy:
    zapis w historii konta, dopóki go nie usuniesz; możliwy udział w trenowaniu modeli, jeśli
    nie wyłączysz (w ChatGPT przełącznik „Improve the model for everyone"); czaty tymczasowe
    usuwane po 30 dniach i nietrenowane (OpenAI help); możliwy przegląd przez ludzi w celach
    bezpieczeństwa; funkcje „pamięci", które przenoszą szczegóły między rozmowami.
  - H3: „Deleted isn't always deleted" (nakaz sądowy w sprawie NYT, 13.05-26.09.2025,
    zniesiony 9.10.2025 z wyjątkami; spokojnie, bez straszenia, jako dowód, że usunięcie
    zależy też od prawa, nie tylko od przycisku).
  - jedno zdanie granicy z linkiem do `are-mental-health-apps-private` **[NA-PROGU]**
    („the ten minute privacy policy check").
- **H2: „What research turned up:"** (badania i raporty)
  - 2014, Lucas, Gratch, King i Morency, *Computers in Human Behavior*: wywiad zdrowotny
    z wirtualnym rozmówcą; osoby przekonane, że rozmawiają z automatem, mniej bały się
    ujawniania, mniej dbały o wrażenie i mocniej okazywały smutek. Wniosek: „The thing that
    makes it easier to talk is the same thing that makes you forget who's listening." Granica:
    wirtualny człowiek w laboratorium, przed erą ChatGPT.
  - 2024, Mozilla Foundation, *Privacy Not Included* o 11 „romantycznych" chatbotach: wszystkie
    dostały ostrzeżenie; większość mogła udostępniać albo sprzedawać dane osobowe, około połowa
    nie pozwalała ich usunąć. ⚠ Procenty tylko z raportu Mozilli, w brzmieniu „may share or
    sell"; to przegląd organizacji non-profit z opisaną metodą, nie badanie recenzowane.
  - 2025, American Psychological Association, *Health Advisory* o chatbotach i aplikacjach
    wellness: rozmowy z chatbotami to nie dokumentacja kliniczna i nie są chronione jak zapisy
    z terapii; APA wzywa do domyślnie bezpiecznych ustawień i jasnych zasad danych. Wniosek
    jej głosem: „Your therapist's notes have a law behind them. Your chat history has a terms
    of service."
  - uczciwe zdanie: reguły zmieniają się szybko (FTC wysłało we wrześniu 2025 zapytania do
    siedmiu firm o chatboty-towarzyszy), więc sprawdzaj ustawienia, a nie ten wpis.
- **H2: „Is it safe to talk to AI about mental health? Five things to do first:"** (fraza
  główna w H2; co spróbować; tryb rozkazujący)
  1. Find the training switch before the first heavy conversation. Gotowe zdanie do siebie:
     „Settings first, feelings second." (ChatGPT: Data Controls; w innych narzędziach szukaj
     „training", „improve the model".)
  2. Use the temporary or incognito mode for the hardest stuff. Haczyk: to tryb dla rozmów,
     których nie chcesz czytać za rok, ani ty, ani nikt inny.
  3. Leave out names, places and anything a stranger could match to a person. „My manager",
     nie imię i nazwisko. Inicjały wystarczą.
  4. Decide what goes into which tool: liczby i oceny (sen, lęk, energia) mają mały ślad,
     całe akapity mają duży. Tu inline karta `check-ins`. Link do
     `regulate-nervous-system-between-therapy-sessions` **[NA-PROGU]** przy zdaniu, że nie
     każdy trudny wieczór trzeba przegadać: czasem najpierw trzeba uspokoić ciało, bez pisania
     czegokolwiek (anchor niżej).
  5. Keep your therapist for the things that need a person and a legal duty of
     confidentiality. Bez zniechęcania do AI, bez polecania AI jako terapii.
  - akapit o MindSync, uczciwy i weryfikowalny (wymóg tej samej rzetelności co w checklistowym
    wpisie): Reflect korzysta z OpenAI jako procesora; polityka prywatności MindSync mówi, że
    wpisy nie są używane do trenowania modeli OpenAI i że apka nie ma reklam; usunięcie konta
    jest w aplikacji, z pełnym usunięciem danych w ciągu 30 dni łącznie z kopiami zapasowymi.
    ⚠ KAŻDE z tych zdań autor sprawdza w `/privacy-policy` w dniu pisania, a ścieżkę do
    przycisku Delete Account na froncie (redesign menu i subskrypcji 2026-10-03 mógł ją
    zmienić). Zero obietnicy eksportu danych. Zero zdań o retencji nagrań głosu z Reflect,
    jeśli polityka tego nie mówi wprost. Link do `/privacy-policy` i `/faq`.
  - puenta, w stylu „Privacy isn't a feeling you get from a chat window. It's a setting."
- **Akapit o apce:** „This is what MindSync's Wellbeing check-ins are for. Log your sleep,
  your anxiety and your energy as three numbers instead of three paragraphs. Give it time, and
  Mood & focus-area trends turns those ratings into something you can see: [the shape of your
  month, without a single sentence about who said what]. Then decide which part actually needs
  words, and where you want those words to live." (Tu trends jest poprawne: oceny, nie notatki.)
- **Pytanie do czytelnika:** np. „What's the last thing you typed to an AI that you'd be
  uncomfortable seeing printed on paper?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: Is it safe to talk to ChatGPT about mental health?
  - H3: Are conversations with AI chatbots confidential?
  - H3: Does ChatGPT use my conversations for training?
  - H3: Can AI chat logs be used in court?
  - H3: How can I use AI for journaling more privately?
  - ⚠ „in court": tylko fakty (brak przywileju wg wypowiedzi Altmana, nakaz zachowania logów
    w sprawie NYT), zdanie „this is not legal advice", bez spekulacji o konkretnych sprawach.
  - ⚠ „Is it safe...": pierwsze zdanie neutralne („It can be, if you know what is kept, who can
    read it and what you have switched off"), bez rekomendacji AI jako wsparcia w kryzysie.

**4. Karty funkcji** (bramka: reflect, mood-trends, timeline, voice-notes, check-ins; używamy
czterech)
- inline w „Five things to do first" (krok 4):
  `[FEATURE: check-ins | Three numbers a day give you the trend with almost nothing written down, which is the smallest footprint a mood record can have.]`
- blok przed FAQ:
  `[FEATURES: Deciding what to write, and where || reflect | A guided reflection that runs through OpenAI as a processor, under a privacy policy that keeps your entries out of model training. || voice-notes | Speech becomes text you read and accept before it is saved, so you see exactly what was kept. || timeline | Every entry on one line, with a recycle bin, so removing something is a decision you can make calmly.]`
  ⚠ Zdanie karty `reflect` autor dopasowuje do aktualnego brzmienia polityki; jeśli polityka
  mówi inaczej, karta mówi tak jak polityka.

**5. Mapa linkowania**
- `<a href="/journal/are-mental-health-apps-private">` **[NA-PROGU]** anchor „the ten minute
  privacy policy check" (H2 „What actually happens to what you type")
- `<a href="/journal/regulate-nervous-system-between-therapy-sessions">` **[NA-PROGU]** anchor
  „calming your body down without typing a word" (krok 4)
- `<a href="/journal/journaling-vs-voice-notes">` anchor „whether to write it or say it"
  (opcjonalnie, krok 4)
- `<a href="/privacy-policy">` anchor „MindSync's privacy policy" i `<a href="/faq">` anchor
  „how your entries are stored" (akapit o MindSync)
- **Landing partner:** `/faq` (site_targets: prywatność, bezpieczeństwo, jak działa), jeden raz.

**6. GEO**
- Odpowiedź na „Is it safe to talk to AI about mental health?", 50-70 słów: trzy rzeczy do
  sprawdzenia (trening, retencja i tryb tymczasowy, brak tajemnicy prawnej) + zdanie, że
  ustawienia zależą od firmy.
- Definicja „legal privilege" w kontekście rozmów z AI, 40-60 słów: ochrona, która pozwala
  odmówić ujawnienia rozmowy w sądzie, mają ją rozmowy z terapeutą, lekarzem i prawnikiem,
  rozmowy z chatbotem jej nie mają (stan na 2025, wypowiedź Altmana).

**7. Hero**
- Wariant „spokojna abstrakcja": miękka, zamknięta forma przypominająca dymek rozmowy
  w barwach forest i mint, w środku ciepłe światło; zero ekranu, zero logo, zero tekstu.
- `hero_image_alt`: „A soft rounded speech-bubble shape in forest and mint tones with warm
  light inside"
- nazwa pliku hero: `is-it-safe-to-talk-to-ai-about-mental-health-hero.webp`

**8. Źródła (sprawdzone 2026-10-07)**
- **POTWIERDZONE (opis badania, ACM DL).** Lucas G.M., Gratch J., King A., Morency L.-P., 2014,
  *Computers in Human Behavior* 37:94-100, „It's only a computer: Virtual humans increase
  willingness to disclose". https://doi.org/10.1016/j.chb.2014.04.043 ⚠ Strony potwierdź.
- **POTWIERDZONE (TechCrunch, 2025-07-25).** Wypowiedź Sama Altmana w podcaście *This Past
  Weekend with Theo Von*: brak tajemnicy prawnej dla rozmów z ChatGPT.
  https://techcrunch.com/2025/07/25/sam-altman-warns-theres-no-legal-confidentiality-when-using-chatgpt-as-a-therapist
- **POTWIERDZONE (Engadget, relacja z postanowienia).** Sprawa NYT przeciw OpenAI: nakaz
  zachowania logów (13.05.2025), zakończony postanowieniem z 9.10.2025; logi zachowane do
  26.09.2025 pozostają dostępne, wyjątki dla kont wskazanych przez NYT.
  https://www.engadget.com/ai/openai-no-longer-has-to-preserve-all-of-its-chatgpt-data-with-some-exceptions-192422093.html
  ⚠ Jeśli autor znajdzie oficjalny wpis OpenAI o nakazie, link idzie do niego.
- **POTWIERDZONE (OpenAI Help Center).** Data Controls FAQ (przełącznik „Improve the model for
  everyone") i Temporary Chat FAQ (usuwanie po 30 dniach, bez treningu, bez pamięci).
  https://help.openai.com/en/articles/7730893-data-controls-faq oraz
  https://help.openai.com/en/articles/8914046-temporary-chat-faq ⚠ Nazwy ustawień sprawdź
  w dniu pisania; interfejs się zmienia.
- **POTWIERDZONE (Mozilla Foundation, 2024-02).** „Creepy.exe": 11 romantycznych chatbotów,
  wszystkie z ostrzeżeniem.
  https://www.mozillafoundation.org/en/blog/creepyexe-mozilla-urges-public-to-swipe-left-on-romantic-ai-chatbots-due-to-major-privacy-red-flags/
  ⚠ Procenty (90% i 54% w relacjach prasowych) tylko w brzmieniu z raportu.
- **POTWIERDZONE (APA, 2025-11).** Health Advisory: Use of generative AI chatbots and wellness
  applications for mental health.
  https://www.apa.org/topics/artificial-intelligence-machine-learning/health-advisory-chatbots-wellness-apps
- **POTWIERDZONE (FTC, 2025-09-11).** Zapytania 6(b) do siedmiu firm o chatboty-towarzyszy.
  https://www.ftc.gov/news-events/news/press-releases/2025/09/ftc-launches-inquiry-ai-chatbots-acting-companions
  ⚠ To dochodzenie dotyczy głównie dzieci i nastolatków; pisz dokładnie tak, bez rozszerzania.
- **Źródło faktów o MindSync:** `/privacy-policy` (stan w dniu pisania) i wpis
  `are-mental-health-apps-private` (stan z 09.2026). Nic ponad to.
- **Czego autor ma NIE twierdzić:**
  - że AI może zastąpić terapeutę albo że jest „bezpieczne" bez zastrzeżeń,
  - że AI jest niebezpieczne i nie wolno go używać (zniechęcanie bez podstaw),
  - niczego o samobójstwach, pozwach rodzin, przypadkach kryzysowych (temat kryzysowy,
    decyzja operatora),
  - że MindSync jest „całkowicie prywatny", „szyfrowany end-to-end" albo że dane „nigdy nie
    opuszczają telefonu" (nie jest to prawda: OpenAI jest procesorem),
  - że MindSync oferuje eksport danych albo wyłączenie analityki w apce (nie oferuje),
  - że MindSync „nie jest jak ChatGPT" w sensie technicznym, bez dowodu z polityki.

**9. Czego NIE robić**
- Nie powtarzaj 7 słów do wyszukania w polityce ani sekcji HIPAA (to checklistowy wpis).
- Zero porównania z innymi aplikacjami mental health z nazwy (poza faktami o OpenAI
  i raportem Mozilli).

---

# 03. How to switch therapists

**1. Meta**
- `seo_url`: `how-to-switch-therapists` | plik: `blog/queue/2026-10-10_how-to-switch-therapists.json`
- kategoria: `Therapy` | `kolor`: `#e8af0a` | `planowana_data`: **2026-10-10**
- `tagi`: `["therapy-logistics", "alliance"]`
- H1: „Switching Isn't a Breakup: How to Switch Therapists, Online or Off"
- `meta_title` (ok. 54 zn.): „How to Switch Therapists (Including Online) | MindSync"
- `meta_description` (ok. 155 zn.): „Decided it's not the right fit? How switching works on
  online platforms and in private practice, what research says about switching, and what to
  bring along."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `how to switch therapists`
- poboczne: `changing therapists`, `how to change therapist on BetterHelp`, `switch provider on
  Talkspace`, `is it rude to switch therapists`, `how often can you switch therapists`,
  `switching therapists within the same practice`
- **zapytanie z GSC (dosłownie, jako FAQ):** `what should i do if my betterhelp therapist
  isn't the right fit?` (9 wyświetleń, poz. 23,1 na `what-to-do-when-your-therapist-is-not-the-right-fit`)
- intencja: decyzja już zapadła albo prawie zapadła; człowiek pyta „jak to technicznie
  zrobić" i „czy nie stracę tego, co już przepracowałem". Część osób jest na platformie online
  i szuka przycisku, część w prywatnym gabinecie i szuka sposobu bez niezręczności.
- luka: SERP (SonderMind, Spring Health, Psych Central, poradniki „how to change therapist on
  BetterHelp" z afiliacją) daje skrypty i „you don't owe anyone an explanation". **Nikt nie
  podaje badania, które mówi wprost, czego się spodziewać po zmianie:** Miggiels i wsp.
  (RCT, Holandia): u osób z depresją, którym pierwsza terapia nie pomogła, zmiana terapeuty
  (albo terapeuty i metody) nie dała lepszych ani gorszych wyników niż kontynuacja; wszyscy
  się trochę poprawili. Nasz kąt: zmiana to zmiana dostawcy, nie zerwanie i nie cudowny reset;
  działa najlepiej, gdy wiesz, czego szukasz w następnej osobie.
- ⚠ granica (twarda): rozpoznanie złego dopasowania, rupture vs bad fit, zdania do rozmowy
  z obecnym terapeutą i FAQ „How do I tell my therapist I want to switch?", „Do I have to tell
  my therapist why I am leaving?", „Should I give my therapist another chance?" należą do
  `what-to-do-when-your-therapist-is-not-the-right-fit`. Pytania na konsultację i „first
  three sessions" należą do `how-to-choose-a-therapist`. Wpis kończy się w momencie umówienia
  nowej osoby; pierwsza sesja z nią to 04.

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** pytanie o konkretny moment: „How long have you been rehearsing the
  switching conversation in the shower?" Haczyki: trzecia wersja maila „I hope this finds you
  well" do terapeuty; przycisk „change provider" otwarty i zamknięty pięć razy, jakby był
  drzwiami do sali egzaminacyjnej; poczucie winy, jakbyś zostawiał kogoś na stacji benzynowej.
- **H2: „Why switching feels so much bigger than it is"** (skąd to się bierze)
  - relacja terapeutyczna jest asymetryczna: ty mówisz najwięcej, więc odejście czuje się jak
    porzucenie bliskiej osoby, choć dla terapeuty to zwykła część zawodu. Lęk, że „zaczniesz od
    zera" i że to znaczy, że „zmarnowałeś" miesiące.
  - jedno zdanie: która osoba siedzi naprzeciwko, ma znaczenie (efekt terapeuty, już opisany
    w `how-to-choose-a-therapist`, link zamiast powtórzenia liczb).
  - slot na **„Disclaimer:"**: np. „Disclaimer: switching therapists is not a review you leave.
    Nobody gets one star."
- **H2: „How to switch therapists, depending on where you are:"** (fraza główna w H2; jak to
  wygląda; dwie H3)
  - H3: „On an online platform": fakty WYŁĄCZNIE ze stron pomocy. BetterHelp: „If you feel your
    therapist isn't a good fit for you, you may elect to be matched to a different therapist"
    (FAQ BetterHelp). Talkspace: zmiana dostawcy z konta, po kilku pytaniach o obszar i preferencje,
    w obrębie tej samej usługi (help center Talkspace; autor sprawdza aktualne kroki, bo strona
    zwróciła 403 w researchu). Zasady ogólne, które warto sprawdzić na każdej platformie: czy
    stary terapeuta dostaje powiadomienie, czy historia wiadomości przechodzi do nowej osoby,
    czy zmiana coś kosztuje. Bez ocen, bez porównania platform.
  - H3: „In private practice or a clinic": jedna sesja zamykająca albo krótki mail (szczegóły
    i zdania w wpisie o dopasowaniu, link), prośba o polecenie kolegi po fachu, prośba
    o podsumowanie leczenia (treatment summary) do zabrania; w klinice często można zmienić
    osobę w tym samym miejscu. Jedno zdanie: jeśli zmiana wiąże się z kosztami, link do 01.
  - lista w drugiej osobie, 3-4 punkty „signs you're ready to switch, not just tired": wiesz,
    czego chcesz inaczej; rozmowa o dopasowaniu już się odbyła i nic się nie zmieniło; sesje
    zamieniły się w relację z tygodnia. Link do wpisu o dopasowaniu („how to tell a bad fit
    from a rough patch").
- **H2: „What research turned up:"** (badania)
  - Miggiels i wsp., *Journal of Affective Disorders* (rok wydania: online 2025, numer 2026,
    autor potwierdza): 163 osoby z depresją, którym 16 sesji nie pomogło, losowo dalej z tym
    samym terapeutą, z nowym terapeutą albo z nowym terapeutą i nową metodą, kolejne 16 sesji.
    Wszystkie grupy trochę się poprawiły, różnic między nimi nie było. Wniosek dwoma zdaniami:
    „Switching isn't a magic reset. It isn't a step backwards either." Granica: depresja,
    wyspecjalizowane ośrodki w jednym kraju, losowy przydział zamiast własnego wyboru.
  - jedno zdanie z badań nad preferencjami (Swift i wsp. 2018, już opisany w
    `how-to-choose-a-therapist`): gdy klient dostaje to, czego chce, rzadziej rezygnuje; link,
    bez powtarzania liczb. Wniosek: dlatego warto wiedzieć, czego chcesz, zanim wybierzesz.
  - uczciwe zdanie: nikt nie bada, jak się czujesz, klikając „change provider" o 23:00; dane
    dotyczą leczenia, nie emocji przy zmianie.
- **H2: „Before you book the next person, do these four things:"** (co spróbować; tryb
  rozkazujący)
  1. Write down what you want done differently, in one line each: tempo, struktura, styl.
     Tu inline karta `health-check`. Haczyk: „more homework, less nodding" to też wymaganie.
  2. Save what you already learned before you leave: zdania, które zostały, narzędzia, które
     działały, zanim pamięć zacznie oceniać całość po ostatniej sesji. Link do
     `how-to-remember-what-you-talk-about-in-therapy` (anchor niżej).
  3. Ask for a treatment summary, or ask your new therapist to request records with your
     written permission (jedno zdanie; szczegóły praw do dokumentacji w 04, który jest później,
     więc bez linku).
  4. Don't judge the new person by session one. Jedno zdanie: ciężka pierwsza sesja to nie
     od razu zły wybór, link do `therapy-hangover` **[NA-PROGU]**.
  - gotowe zdanie do nowej osoby przy umawianiu: „I'm switching from another therapist, and
    I know what didn't work for me. Can we talk about that in the first session?"
  - puenta, w stylu „You're not starting over. You're starting better informed."
- **Akapit o apce:** „This is what MindSync's Therapy relationship check is for. Log how the
  last few sessions actually felt, the one thing you kept wishing your therapist would do, and
  whether that changed after you said it out loud. Give it time, and your Therapy timeline
  turns those entries into something you can see: [whether this is one bad month or the same
  note for half a year]. Then take that list into the first call with the next person." (Bez
  „share" z apki; czytelnik sam niesie.)
- **Pytanie do czytelnika:** np. „What's the one thing you'd want your next therapist to know
  about what didn't work last time?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: What should I do if my BetterHelp therapist isn't the right fit? (dosłownie z GSC)
  - H3: Is it rude to switch therapists?
  - H3: Will switching therapists set me back?
  - H3: How many times is it OK to switch therapists?
  - H3: Can I switch therapists within the same practice?
  - ⚠ odpowiedź o BetterHelp: pierwsze zdanie praktyczne (platforma pozwala poprosić o nowe
    dopasowanie, wg jej FAQ), drugie: zanim klikniesz, zapisz, czego chcesz inaczej; link do
    wpisu o dopasowaniu tylko w treści, nie w FAQ (FAQ bez linków).
  - ⚠ „set me back": Miggiels (brak różnicy) + zastrzeżenie, że badanie dotyczy depresji.

**4. Karty funkcji** (bramka: health-check, timeline, summaries, goals, session-prep; używamy
czterech)
- inline w „Before you book the next person..." (krok 1):
  `[FEATURE: health-check | The same short questions about the working relationship, answered a few times, so the list you take to the next therapist rests on more than one hard Tuesday.]`
- blok przed FAQ:
  `[FEATURES: Switching without losing the thread || timeline | Months of sessions and realizations on one line, readable in ten minutes before the first call with someone new. || summaries | A monthly read of what you worked on, which is a better handover than trying to remember it all in the first hour. || goals | What you came to therapy for, in your own words, so the new person hears the target and not just the history.]`

**5. Mapa linkowania**
- `<a href="/journal/what-to-do-when-your-therapist-is-not-the-right-fit">` **[NA-PROGU]**
  anchor „how to tell a bad fit from a rough patch" (H2 „How to switch therapists...")
- `<a href="/journal/therapy-hangover">` **[NA-PROGU]** anchor „the heavy day after a hard
  session" (krok 4)
- `<a href="/journal/how-to-remember-what-you-talk-about-in-therapy">` anchor „saving what each
  session gave you" (krok 2)
- `<a href="/journal/how-to-choose-a-therapist">` anchor „what to look for in the next one"
  (sekcja „Why switching feels..." albo badania)
- `<a href="/journal/how-to-afford-therapy">` anchor „if the switch changes what you pay"
  (wstecz do 01, publikacja 2026-10-08; H3 o gabinecie)
- `<a href="/journal/when-to-stop-therapy">` anchor „ending therapy on purpose" (opcjonalnie,
  jedno zdanie granicy: zmiana to nie koniec)
- **Landing partner:** brak.

**6. GEO**
- Odpowiedź na „How do I switch therapists?", 50-70 słów: platforma (prośba o nowe
  dopasowanie z konta) vs gabinet (sesja zamykająca albo mail, prośba o polecenie
  i podsumowanie) + jedno zdanie „write down what you want done differently".
- Teza z Miggiels i wsp., 40-60 słów, z granicą próby: zmiana terapeuty po braku poprawy nie
  dała lepszych ani gorszych wyników niż kontynuacja.

**7. Hero**
- Wariant „codzienny moment": dwa kubki na stole, jeden pusty odsunięty, drugi pełny
  z parującą herbatą bliżej kadru, miękkie światło dnia; bez osób.
- `hero_image_alt`: „Two mugs on a table, one empty and set aside, one full and steaming in
  soft daylight"
- nazwa pliku hero: `how-to-switch-therapists-hero.webp`

**8. Źródła (sprawdzone 2026-10-07)**
- **POTWIERDZONE (relacja HCPLive; abstrakt PubMed 41284541 niedostępny przez cookies).**
  Miggiels M., Ten Klooster P., Beekman A. i wsp., *Journal of Affective Disorders*, „A
  randomized controlled trial testing the effects of sequential psychotherapy in depression:
  Changing therapist, or both therapist and method?". https://pubmed.ncbi.nlm.nih.gov/41284541/
  N = 163, trzy ramiona, 16 sesji w 8 tygodni w drugiej fazie, brak różnic w spadku objawów,
  odpowiedzi i remisji. ⚠ Rok, tom i strony potwierdź na ScienceDirect
  (https://sciencedirect.com/science/article/abs/pii/S0165032725019986) przed cytatem.
- **POTWIERDZONE (FAQ BetterHelp, 2026-10-07).** „If you feel your therapist isn't a good fit
  for you, you may elect to be matched to a different therapist." https://www.betterhelp.com/faq/
- **DO POTWIERDZENIA (help center Talkspace, 403 w researchu).** „Matching With or Changing
  Providers". https://help.talkspace.com/hc/en-us/articles/360000287406-Matching-With-or-Changing-Providers
  Wg wyników wyszukiwania: zmiana z konta po pytaniach, w obrębie tej samej usługi. Autor
  otwiera stronę w przeglądarce i cytuje tylko to, co tam jest.
- **Już na żywo (link zamiast powtórki):** Swift J.K., Callahan J.L., Cooper M., Parkin S.R.,
  2018, *Journal of Clinical Psychology*, preferencje klienta (https://doi.org/10.1002/jclp.22680);
  Johns R.G. i wsp. 2019, efekt terapeuty. Oba w `how-to-choose-a-therapist`.
- **Czego autor ma NIE twierdzić:**
  - że zmiana terapeuty poprawi wyniki (badanie mówi: ani lepiej, ani gorzej),
  - niczego oceniającego o BetterHelp czy Talkspace (ani dobrze, ani źle), żadnych cen platform,
    żadnej wzmianki o sprawie FTC w tym wpisie,
  - że terapeuta „musi" przekazać notatki (prawa do dokumentacji opisuje 04, ostrożnie),
  - niczego o przekroczeniu granic przez terapeutę poza jednym zdaniem z linkiem do wpisu
    o dopasowaniu (tam jest akapit o organach licencyjnych).

**9. Czego NIE robić**
- Nie powtarzaj zdań do rozmowy z obecnym terapeutą ani sekcji rupture vs bad fit (link).
- Nie wchodź w pierwszą sesję z nową osobą (to 04).

---

# 04. Starting over with a new therapist

**1. Meta**
- `seo_url`: `starting-over-with-a-new-therapist` | plik:
  `blog/queue/2026-10-11_starting-over-with-a-new-therapist.json`
- kategoria: `Therapy` | `kolor`: `#3c67a5` | `planowana_data`: **2026-10-11**
- `tagi`: `["getting-more-from-therapy", "alliance"]`
- H1: „You Don't Have to Start From Zero: Starting Over With a New Therapist"
- `meta_title` (ok. 45 zn.): „Starting Over With a New Therapist | MindSync"
- `meta_description` (ok. 157 zn.): „New therapist, same story to tell? What to share in the
  first sessions, how to ask for your records, and how to carry what you learned so you don't
  start from zero."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `starting over with a new therapist`
- poboczne: `what to tell a new therapist`, `first session with a new therapist`,
  `transitioning to a new therapist`, `can I get my therapy records`, `should I tell my new
  therapist about my old therapist`, `retelling your story in therapy`
- intencja: nowa osoba jest już umówiona (po zmianie, przeprowadzce, przerwie, zmianie
  ubezpieczenia) i pojawia się zmęczenie na myśl o opowiadaniu wszystkiego od nowa. Pytanie:
  co powiedzieć, co zabrać, jak nie stracić tego, co już przepracowane.
- luka: SERP (Talkspace „Tips for Transitioning", Zocdoc, Psych Central, TherapyFinder,
  gabinety) radzi „be honest about what didn't work" i „request a summary". **Nikt nie
  opowiada, co badania mówią o samym przejściu:** Clark i wsp. 2014 (klienci przekazywani
  nowym terapeutom czuli lęk, smutek i złość, a przejścia oceniane jako udane to te, w których
  nowy terapeuta pomógł o tych uczuciach porozmawiać) i Marmarosh i wsp. 2017 (strona
  terapeutów: klienci porównują nową osobę ze starą). **Nikt też nie mówi uczciwie o prawie
  do dokumentacji:** w USA HIPAA daje prawo dostępu do dokumentacji, ale „psychotherapy notes"
  terapeuta może zatrzymać (HHS). Nasz kąt: nie zaczynasz od zera, jeśli przyniesiesz własną
  wersję historii; nowy terapeuta potrzebuje twojego streszczenia, nie twojego życiorysu.
- ⚠ granica: mechanika zmiany (03, link), pytania na konsultację (`how-to-choose-a-therapist`),
  technika agendy przed sesją (`how-to-prepare-for-a-therapy-session`: jedno zdanie i link),
  debrief po sesji (`how-to-remember-what-you-talk-about-in-therapy`: link, bez powtarzania
  czterech rzeczy do zapisania).

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** „Do any of these sound familiar?" + trzy scenki, ostatnia krótka
  z mrugnięciem. Haczyki: trzeci raz w życiu opowiadasz o dzieciństwie od momentu narodzin,
  z tymi samymi przypisami; łapiesz się na zdaniu „my old therapist used to say...", co brzmi
  jak wspominanie byłego na pierwszej randce; nowa osoba pyta „so what brings you here?",
  a ty masz ochotę oddać jej segregator.
- **H2: „Why the first sessions feel like a rerun"** (skąd to się bierze)
  - nowy terapeuta musi zbudować własny obraz (wywiad, cele, bezpieczeństwo), a ty już byłeś
    w tym miejscu; stąd zmęczenie i niecierpliwość. Do tego porównywanie: nowa osoba jest
    oceniana na tle starej, czasem nieuczciwie w obie strony.
  - jedno zdanie: więź z nową osobą liczy się od początku (link do `how-to-choose-a-therapist`
    zamiast powtarzania Flückigera).
  - slot na **„Fun fact:"**: w języku terapeutów taki klient to „transfer client", a o tym, jak
    przebiega przejście, piszą nawet osobne prace badawcze (Marmarosh 2017). Brzmienie tylko
    w granicach abstraktu.
- **H2: „Starting over with a new therapist, in real life:"** (fraza główna w H2; jak to
  wygląda)
  - lista w drugiej osobie, 4-5 punktów: streszczasz poprzednią terapię za długo albo w ogóle;
    nie mówisz, że coś nie działało, żeby nie „obgadywać" poprzedniej osoby; zakładasz, że nowa
    osoba „wie" z dokumentacji; testujesz nową osobę tym samym tematem, który utknął; czujesz
    ulgę i winę naraz.
  - H3: „What's worth telling, and what can wait": co działało, co nie działało, co już
    wiesz o swoich wzorcach, czego potrzebujesz teraz (np. „I need you to push me more").
    Całe życiorysy mogą poczekać.
- **H2: „What research turned up:"** (badania i prawo)
  - 2014, Clark i wsp., *Contemporary Family Therapy*: wywiady z klientami kliniki szkoleniowej
    przekazanymi nowym terapeutom. Ludzie opisywali lęk, smutek, złość; przejścia uznane za
    udane to te, w których nowy terapeuta pomógł przepracować reakcje na samą zmianę. Wniosek:
    „Say the awkward part out loud. That's the work, not a detour." Granica: mała próba
    jakościowa, klinika szkoleniowa, przejścia wymuszone końcem praktyk.
  - 2017, Marmarosh i wsp., *Psychotherapy*: wywiady z 12 terapeutami w trakcie szkolenia
    o pracy z przejętymi klientami; jedno ze źródeł trudności to porównania z poprzednim
    terapeutą. Wniosek: porównywanie jest normalne po obu stronach pokoju, lepiej je nazwać.
    ⚠ Szczegóły wyników tylko z abstraktu.
  - HHS o HIPAA: w USA masz prawo dostępu do swojej dokumentacji (m.in. rozpoznania, plan
    leczenia, podsumowania), ale prywatne notatki terapeuty („psychotherapy notes"),
    trzymane osobno, nie są nim objęte; prawo stanowe może dawać więcej. Wniosek: proś
    o podsumowanie leczenia, nie o „wszystkie notatki". Zdanie „this is not legal advice".
- **H2: „How to hand over your story in four steps:"** (co spróbować; tryb rozkazujący)
  1. Write a one-page version of your therapy so far: z czym przyszedłeś, co się zmieniło,
     co działało, co nie, czego chcesz teraz. Tu inline karta `timeline`. Haczyk: jedna strona,
     nie trylogia.
  2. Ask for a treatment summary, or sign a release so the new therapist can request records.
     Gotowe zdanie do poprzedniej osoby: „Could you send a short treatment summary to my new
     therapist? I'll sign whatever release you need."
  3. Say what didn't work, without making it a review of the person: gotowe zdanie: „Last time,
     I'd leave sessions feeling heard but not moved. I want to try something more structured."
  4. Bring your one page to the first session and read from it. Link do
     `how-to-prepare-for-a-therapy-session` **[NA-PROGU]** przy zdaniu o otwierającym zdaniu
     sesji (anchor niżej). Po sesji: link do `how-to-remember-what-you-talk-about-in-therapy`.
  - jedno zdanie: jeśli zmieniłeś terapeutę świeżo, link do 03 („the practical side of
    switching").
  - jedno zdanie o tygodniach między pierwszymi sesjami, link do
    `what-to-do-between-therapy-sessions` **[NA-PROGU]**.
  - puenta, w stylu „Your new therapist doesn't need your whole life. They need your best
    summary of it."
- **Akapit o apce:** „This is what MindSync's Therapy timeline is for. Log the realizations
  you don't want to lose, the tools that worked, and the one thing you never quite said in
  your last therapy. Give it time, and your Weekly & monthly summaries turn those entries into
  something you can read: [a short version of months of work, ready before session one with
  someone new]. Then open your Prep Card the night before." (Zero „export", zero „send";
  czytelnik czyta i opowiada.)
- **Pytanie do czytelnika:** np. „If your new therapist could only read one sentence about your
  last therapy, what would you want it to say?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: What should I tell a new therapist about my old therapist?
  - H3: Can I get my records from my old therapist?
  - H3: Do I have to start therapy over with a new therapist?
  - H3: How long does it take to feel comfortable with a new therapist?
  - H3: What should I bring to my first session with a new therapist?
  - ⚠ „records": HIPAA + wyjątek psychotherapy notes + prawo stanowe + „not legal advice";
    poza USA jedno zdanie, że zasady są inne (np. RODO daje prawo dostępu do danych).
  - ⚠ „How long...": bez liczby sesji jako normy; uczciwie, że różnie, i że warto o tym
    powiedzieć wprost, jeśli po kilku sesjach nadal jest obco.

**4. Karty funkcji** (bramka: timeline, check-ins, summaries, session-prep, session-recording,
workspace; używamy czterech)
- inline w „How to hand over your story..." (krok 1):
  `[FEATURE: timeline | Everything you worked through, in order, which turns writing the one-page version into reading and choosing instead of remembering.]`
- blok przed FAQ:
  `[FEATURES: Bringing your history with you || summaries | Weeks and months already condensed into something you can read in a waiting room. || session-prep | The night before session one, a card with your topics and the questions you want to ask this new person. || workspace | The realizations from last time, kept where you can find them, so the new work starts from them.]`

**5. Mapa linkowania**
- `<a href="/journal/how-to-remember-what-you-talk-about-in-therapy">` anchor „keeping what
  each new session gives you" (krok 4)
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` **[NA-PROGU]** anchor „what to
  bring into the first hour" (krok 4)
- `<a href="/journal/what-to-do-between-therapy-sessions">` **[NA-PROGU]** anchor „the weeks
  between your first sessions" (akapit po krokach)
- `<a href="/journal/how-to-switch-therapists">` anchor „the practical side of switching"
  (wstecz do 03, publikacja 2026-10-10)
- `<a href="/journal/how-to-choose-a-therapist">` anchor „why the first few sessions matter so
  much" (sekcja „Why the first sessions feel like a rerun")
- **Landing partner:** brak (opcjonalnie `/features` przy kartach, nie w treści).

**6. GEO**
- Odpowiedź na „What should I tell a new therapist about my old therapist?", 50-70 słów:
  co działało, co nie, czego potrzebujesz teraz + Clark 2014 (rozmowa o samej zmianie pomaga).
- Definicja „psychotherapy notes" vs dokumentacja, 40-60 słów, wg HHS, z „in the US".

**7. Hero**
- Wariant „codzienny moment": otwarty notes z jedną zapisaną stroną i zakładką, obok klucz
  na stole, ciepłe popołudniowe światło; bez osoby.
- `hero_image_alt`: „An open notebook with one handwritten page and a key resting beside it in
  warm afternoon light"
- nazwa pliku hero: `starting-over-with-a-new-therapist-hero.webp`

**8. Źródła (sprawdzone 2026-10-07)**
- **POTWIERDZONE (opis, Springer).** Clark i wsp., 2014, *Contemporary Family Therapy*,
  „Creating a Safety Net: Transferring to a New Therapist in a Training Setting".
  https://link.springer.com/article/10.1007/s10591-013-9282-2 ⚠ Pełną listę autorów, tom
  i strony potwierdź na stronie wydawcy; zdanie o lęku, smutku i złości oraz o roli nowego
  terapeuty pochodzi z omówień, sprawdź w abstrakcie.
- **POTWIERDZONE (PubMed 28263656, abstrakt niedostępny przez cookies).** Marmarosh C.L. i wsp.,
  2017, *Psychotherapy*, „Therapists-in-training experiences of working with transfer clients:
  One relationship terminates and another begins". https://pubmed.ncbi.nlm.nih.gov/28263656
  12 terapeutów, CQR. ⚠ Wynik o porównaniach potwierdź w abstrakcie; jeśli go tam nie ma,
  usuń to zdanie.
- **POTWIERDZONE (HHS).** Prawo dostępu do dokumentacji i wyjątek psychotherapy notes.
  https://www.hhs.gov/hipaa/for-professionals/faq/what-personal-health-information-do-individuals/index.html
  ⚠ Brzmienie dosłowne z HHS, nie z blogów kancelarii.
- **Już na żywo (link zamiast powtórki):** Flückiger i wsp. 2018 (więź terapeutyczna,
  `how-to-choose-a-therapist`).
- **Czego autor ma NIE twierdzić:**
  - że terapeuta „musi" wydać notatki albo przekazać je nowej osobie,
  - że jedna strona streszczenia zastępuje wywiad nowego terapeuty (on i tak zada pytania),
  - że MindSync przenosi dane do nowego terapeuty albo eksportuje historię,
  - niczego o przekroczeniu granic przez poprzedniego terapeutę (jedno zdanie z linkiem do
    `what-to-do-when-your-therapist-is-not-the-right-fit`, jeśli w ogóle).

**9. Czego NIE robić**
- Nie powtarzaj czterech rzeczy do zapisania po sesji ani dwulinijkowej reguły z wpisów
  o pamiętaniu i przygotowaniu (linki).
- Nie opisuj kroków zmiany na platformie (to 03).

---

# 05. Does insurance cover therapy?

**1. Meta**
- `seo_url`: `does-insurance-cover-therapy` | plik:
  `blog/queue/2026-10-12_does-insurance-cover-therapy.json`
- kategoria: `Therapy` | `kolor`: `#339499` | `planowana_data`: **2026-10-12**
- `tagi`: `["therapy-logistics", "cost"]`
- H1: „Does Insurance Cover Therapy? How to Find Out Before the First Bill"
- `meta_title` (ok. 53 zn.): „Does Insurance Cover Therapy? How to Check | MindSync"
- `meta_description` (ok. 157 zn.): „Your plan may cover therapy on paper. In-network vs
  out-of-network, superbills, HSA and FSA, and the five questions to ask your insurer before you
  book."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `does insurance cover therapy`
- poboczne: `how to use insurance for therapy`, `out-of-network therapy`, `superbill for
  therapy`, `in-network vs out-of-network therapist`, `can I use HSA for therapy`, `how many
  therapy sessions does insurance cover`, `mental health parity`
- intencja: człowiek z ubezpieczeniem w USA chce wiedzieć, ile naprawdę zapłaci, zanim się
  umówi, albo dostał pierwszy rachunek i nie rozumie, dlaczego. Karta ubezpieczenia na stole,
  numer infolinii w telefonie.
- luka: SERP (Rula, Grow Therapy, TherapyDen, gabinety, platformy przyjmujące ubezpieczenia)
  odpowiada „yes, usually" i daje listę pytań, często z interesem sprzedażowym („we take your
  insurance"). **Nikt nie mówi uczciwie, dlaczego „covered" na papierze nie znaczy „dostępne":**
  Zhu i wsp. 2024 (około jedna trzecia terapeutów w prywatnej praktyce nie przyjmowała
  ubezpieczenia), Bishop i wsp. 2014 (55,3% psychiatrów vs 88,7% innych specjalistów
  przyjmowało ubezpieczenie prywatne) i Senate Finance Committee 2023 (tajny klient: ponad
  80% wpisów w katalogach planów Medicare Advantage było „duchami", wizytę udało się umówić
  w 18% prób). Nasz kąt: zanim zapytasz „czy pokrywa", zapytaj „u kogo, za ile i ile razy",
  i zapisz odpowiedź.
- ⚠ granica: sposoby bez ubezpieczenia (sliding scale, kliniki, grupa, EAP) to 01; tu jedno
  zdanie i link wstecz. Wartość terapii i średnie ceny: `is-therapy-worth-the-money` (link).
  Ile sesji „potrzeba": `how-long-therapy-takes-to-work` (tu wyłącznie limity planu).

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** pytanie o konkretny moment: „Have you ever called the number on the
  back of your insurance card and hung up knowing less than before?" Haczyki: 40 minut muzyki
  na czekaniu, potem „it depends on your plan"; katalog „in-network" z terapeutą, który
  przeszedł na emeryturę w 2019; słowo „deductible" wymawiane tonem, jakbyś powinien je znać
  od urodzenia.
- **H2: „Why 'covered' doesn't always mean you can use it"** (skąd to się bierze)
  - prostym językiem: plan może pokrywać terapię, ale (1) terapeuta może nie być w sieci,
    (2) najpierw płacisz do wysokości deductible, (3) część kosztu zostaje jako copay albo
    coinsurance, (4) plan może wymagać rozpoznania i uzasadnienia medycznego. Do tego niskie
    stawki planów sprawiają, że część terapeutów woli rozliczać się gotówką.
  - fragment cytowalny (GEO): in-network vs out-of-network.
  - slot na **„Fun fact:"**: federalna ustawa o parytecie (MHPAEA, 2008) nie każe planowi
    pokrywać zdrowia psychicznego, ale jeśli pokrywa, dopłaty i limity nie mogą być bardziej
    restrykcyjne niż dla świadczeń medycznych (DOL). ⚠ Nowsze przepisy z 2024 nie są
    egzekwowane od 15.05.2025: nie opisuj ich jako obowiązujących.
- **H2: „Does insurance cover therapy? What the answer usually looks like:"** (fraza główna
  w H2; jak to wygląda)
  - lista w drugiej osobie, 4-5 punktów jako typowe scenariusze: in-network z copayem po
    spełnieniu deductible; out-of-network z częściowym zwrotem po superbillu; plan bez
    świadczeń out-of-network; limit sesji albo przegląd „medical necessity"; HSA albo FSA
    jako sposób na zapłatę z pieniędzy przed opodatkowaniem.
  - H3: „What a superbill is, and how to use one": definicja, kto ją wystawia, kto wysyła,
    że zwrot zależy od planu (bez podawania typowych procentów zwrotu, chyba że ze źródłem
    instytucjonalnym; poradnikowe „50-80%" z blogów gabinetów NIE).
  - jedno zdanie: rachunki zwykle zawierają kod rozpoznania (dlatego niektórzy płacą sami);
    bez oceniania tej decyzji.
- **H2: „What research turned up:"** (badania i raporty)
  - 2014, Bishop, Press, Keyhani i Pincus, *JAMA Psychiatry*: dane z krajowego badania
    gabinetów 2009-2010; 55,3% psychiatrów przyjmowało ubezpieczenie prywatne wobec 88,7%
    innych lekarzy. Wniosek: problem nie jest w tobie ani w twojej karcie. Granica: psychiatrzy,
    nie terapeuci, dane sprzed dekady.
  - 2024, Zhu i wsp., *Health Affairs Scholar*: 175 083 profile terapeutów z katalogu Psychology
    Today; około 65% przyjmowało ubezpieczenie, a średnia stawka gotówkowa wynosiła ok. 143 USD
    (końcówka 2023). Wniosek: przy jednej trzeciej rynku ubezpieczenie nie wchodzi w grę wcale.
    Granica: profile z jednego katalogu, deklaracje samych terapeutów.
  - 2023, Senate Finance Committee (raport tajnego klienta): 120 telefonów do terapeutów
    z katalogów 12 planów Medicare Advantage w 6 stanach; ponad 80% wpisów okazało się
    nieosiągalnych, nieprzyjmujących albo poza siecią, wizytę dało się umówić w 18% prób.
    Wniosek: katalog to punkt wyjścia, nie odpowiedź. Granica: Medicare Advantage, mała próba.
- **H2: „Five questions to ask your insurer, and write down the answers:"** (co spróbować;
  tryb rozkazujący)
  1. „Do I have outpatient mental health benefits, in network and out of network?"
  2. „What's my deductible, and how much of it have I met this year?"
  3. „What will I pay per session: copay or coinsurance?"
  4. „Is there a limit on sessions, or do you need prior authorization?"
  5. „Can you confirm these three therapists are in network and taking new patients?"
  - po liście: zapisz imię konsultanta, datę i numer referencyjny rozmowy (praktyka, nie
    porada prawna). Haczyk: notatka z rozmowy z ubezpieczycielem to jedyny pamiętnik, który
    może ci zwrócić pieniądze.
  - jedno zdanie o HSA i FSA: IRS Publication 502 zalicza do wydatków medycznych opłaty za
    psychologa i terapię jako leczenie; szczegóły zależą od planu, „not tax advice".
  - jedno zdanie: jeśli ubezpieczenie odpada, link wstecz do 01.
  - jedno zdanie: gdy plan liczy sesje, każda ma większą wagę; link do
    `what-to-do-between-therapy-sessions` **[NA-PROGU]** i do
    `how-long-therapy-takes-to-work`. Tu inline karta `goals`.
  - zdanie „this is not financial or legal advice, and your plan or state may differ".
  - puenta, w stylu „Ask three times, write it down once."
- **Akapit o apce:** „This is what MindSync's Goals are for. Log what you came to therapy for
  in your own words, the change you'd want to see before your covered sessions run out, and
  the evidence you notice along the way. Give it time, and Mood & focus-area trends turns your
  check-in ratings into something you can see: [whether the weeks are actually moving]. Then
  bring that picture to the session where you and your therapist plan how to use the visits you
  have left." ⚠ Trends opiera się na ocenach z check-inów, więc w „Log" ma być też ocena (np.
  „a weekly rating of the thing you came in for"); cele są dowodem z wpisów, nie wykresem.
  ⚠ Zero sugestii, że wpisy z apki są dokumentacją dla ubezpieczyciela.
- **Pytanie do czytelnika:** np. „What's the one question about your coverage you've been
  avoiding asking because you're afraid of the answer?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: Does insurance cover therapy?
  - H3: How do I find out if my insurance covers therapy?
  - H3: What is a superbill for therapy?
  - H3: Can I use my HSA or FSA for therapy?
  - H3: How many therapy sessions does insurance cover?
  - ⚠ „Does insurance cover therapy?": pierwsze zdanie „Often, if your plan includes mental
    health benefits", potem parytet (2008) i zastrzeżenie o sieci. Bez „always" i bez
    „required by law to cover" (MHPAEA tego nie wymaga; ACA wymaga dla planów indywidualnych
    i małych grup z rynku, autor sprawdza na healthcare.gov przed użyciem).
  - ⚠ „How many sessions...": limity zależą od planu; parytet zakazuje limitów
    bardziej restrykcyjnych niż medyczne; zero liczby jako normy.

**4. Karty funkcji** (bramka: summaries, mood-trends, goals, timeline, session-prep,
workspace; używamy czterech)
- inline w „Five questions to ask your insurer..." (zdanie o liczonych sesjach):
  `[FEATURE: goals | What you came for, written in your own words, so a limited number of visits has a clear target instead of a vague hope.]`
- blok przed FAQ:
  `[FEATURES: Making covered sessions count || mood-trends | Weekly ratings of what you came in for, charted so you and your therapist can see whether the visits are moving it. || timeline | Every session and note in one place, handy when you need to remember dates and what you worked on. || session-prep | Topics and questions ready before each visit, so none of the covered hours goes on catching up.]`

**5. Mapa linkowania**
- `<a href="/journal/how-to-afford-therapy">` anchor „ways to pay less without insurance"
  (wstecz do 01, publikacja 2026-10-08)
- `<a href="/journal/how-to-switch-therapists">` anchor „switching to someone in your network"
  (wstecz do 03, opcjonalnie przy pytaniu 5)
- `<a href="/journal/what-to-do-between-therapy-sessions">` **[NA-PROGU]** anchor „making the
  weeks between covered sessions count"
- `<a href="/journal/is-therapy-worth-the-money">` anchor „what a full course costs, and how to
  judge it" (sekcja „Why 'covered' doesn't always mean...")
- `<a href="/journal/how-long-therapy-takes-to-work">` anchor „how many sessions change usually
  takes"
- **Landing partner:** `/pre-order/tracking-therapy-effectiveness` (anchor „seeing what each
  covered session actually moved"), jeden raz, przy akapicie o liczonych sesjach.

**6. GEO**
- Definicja in-network vs out-of-network, 40-60 słów.
- Definicja superbill, 40-60 słów: szczegółowy rachunek od terapeuty spoza sieci, który
  pacjent sam wysyła do ubezpieczyciela, by dostać częściowy zwrot, jeśli plan ma świadczenia
  out-of-network.
- Odpowiedź na „How do I find out if my insurance covers therapy?", 50-70 słów: dokument
  Summary of Benefits and Coverage + telefon z pięcioma pytaniami + notatka z rozmowy.

**7. Hero**
- Wariant „codzienny moment": koperta i karta bez napisów obok kubka i długopisu na jasnym
  stole, miękkie światło, paleta mint i sand; zero logo, zero tekstu, zero dokumentów
  z liczbami.
- `hero_image_alt`: „A plain envelope and a blank card beside a mug and a pen on a bright table"
- nazwa pliku hero: `does-insurance-cover-therapy-hero.webp`

**8. Źródła (sprawdzone 2026-10-07)**
- **POTWIERDZONE (JAMA Network).** Bishop T.F., Press M.J., Keyhani S., Pincus H.A., 2014,
  *JAMA Psychiatry* 71(2):176-181, „Acceptance of insurance by psychiatrists and the
  implications for access to mental health care".
  https://jamanetwork.com/journals/jamapsychiatry/fullarticle/1785174 55,3% vs 88,7%
  (prywatne ubezpieczenie, 2009-2010). ⚠ Listę autorów potwierdź.
- **POTWIERDZONE (pełny tekst).** Zhu J.M. i wsp., 2024, *Health Affairs Scholar* 2(9):qxae110.
  https://academic.oup.com/healthaffairsscholar/article/2/9/qxae110/7750928 ok. 65% przyjmuje
  ubezpieczenie; średnia stawka gotówkowa 143,26 USD; Medicaid 82,77 USD.
- **POTWIERDZONE (Senate Finance Committee, 2023-05-03).** Raport tajnego klienta o „ghost
  networks" w Medicare Advantage.
  https://www.finance.senate.gov/imo/media/doc/050323%20Ghost%20Network%20Hearing%20-%20Secret%20Shopper%20Study%20Report.pdf
  120 telefonów, 12 planów, 6 stanów, umówienie w 18%, ponad 80% „duchów".
- **POTWIERDZONE (DOL).** MHPAEA: parytet dopłat i limitów, brak obowiązku pokrycia.
  https://www.dol.gov/agencies/ebsa/laws-and-regulations/laws/mental-health-and-substance-use-disorder-parity
- **POTWIERDZONE (komunikaty branżowe o stanowisku DOL, HHS, Treasury z 2025-05-15).**
  Wstrzymanie egzekwowania reguły z 2024. Np.
  https://www.truckerhuss.com/2025/05/the-agencies-press-pause-on-the-2024-final-mhpaea-rule/
  W tekście NIE cytujemy; to tylko powód, dla którego nie opisujemy reguły 2024.
- **POTWIERDZONE (IRS).** Publication 502, opłaty za psychologa i terapię jako wydatki
  medyczne. https://www.irs.gov/pub/irs-pdf/p502.pdf ⚠ Brzmienie z bieżącego wydania.
- **DO SPRAWDZENIA przed użyciem.** healthcare.gov, zdrowie psychiczne jako essential health
  benefit w planach z rynku: https://www.healthcare.gov/coverage/mental-health-substance-abuse-coverage/
- **Czego autor ma NIE twierdzić:**
  - że ubezpieczenie „musi" pokrywać terapię (tylko plany objęte ACA, i to autor sprawdza),
  - typowych procentów zwrotu out-of-network z blogów gabinetów,
  - że wpisy z MindSync są dokumentacją dla ubezpieczyciela albo pomagają uzyskać zwrot,
  - porad podatkowych ponad „IRS lists psychotherapy as a medical expense; check your plan",
  - niczego o konkretnych ubezpieczycielach z nazwy.

**9. Czego NIE robić**
- Nie dubluj opcji bez ubezpieczenia (01) ani dyskusji o wartości (worth-the-money).
- Zero „we take your insurance" w jakiejkolwiek formie: MindSync nie jest usługą medyczną.

---

## Rezerwy (bez briefów, bramka w `_preflight-partia6.json`)

- **06 KLASTER5: loneliness in adulthood** (`loneliness-in-adulthood`). Bez zmian względem
  partii 5: samotność to brak bliskości, nie liczba znajomych; karty reflect, voice-notes,
  check-ins. ⚠ Zero treści o izolacji skrajnej i kryzysie.
- **07 KLASTER5: imposter syndrome** (`imposter-syndrome`). Bez zmian względem partii 5:
  dowody sukcesu „nie liczą się"; karty timeline, workspace, goals. ⚠ Zero liczby „70%" bez
  źródła pierwotnego.

## Zapytania do Ahrefs (Keywords Explorer, US, do pobrania w sesji głównej)

Frazy główne: `how to afford therapy`, `is it safe to talk to ai about mental health`,
`how to switch therapists`, `starting over with a new therapist`, `does insurance cover therapy`.
Warianty do porównania wolumenu: `affordable therapy`, `sliding scale therapy`, `low cost
therapy`, `is chatgpt private`, `ai therapy privacy`, `how to change therapist on betterhelp`,
`changing therapists`, `new therapist first session`, `what to tell a new therapist`,
`out of network therapy`, `superbill for therapy`, `can i use hsa for therapy`.
Plus Organic keywords konkurencji (top 50, US) dla: `rula.com/blog`, `growtherapy.com`,
`talkspace.com/blog`, `sondermind.com/resources` z filtrem słów `insurance|afford|switch|change
therapist|sliding`. Reguła decyzji: jeśli fraza główna ma wolumen 0, a poboczna > 0, zamieniamy
je miejscami w H1 i H2; reszta briefu bez zmian.
