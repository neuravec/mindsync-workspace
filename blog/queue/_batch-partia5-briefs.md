# Partia 5: briefy wpisów (7 pozycji, drip 2026-09-29..2026-10-05), druga partia stylem Moniki

> Data: 2026-09-28. Autor briefów: `seo-content-writer`. Wykonawca prozy: `blog-writer` przez
> skill `blog-write` (+ `humanizer` z próbką `docs/blog/voice-sample-monika.md`, akcept
> `brand-voice-manager` wg checklisty §2.5, schema od `seo-tech-lead`, hero od
> `graphic-designer`). **Treść po ANGIELSKU.** Format pliku kolejki: `blog/queue/_format.md`.
> Głos: `docs/blog/brand-mindsync.md` §2 (szkielet §2.2, nagłówki §2.1 pkt 12).
>
> **Status bramki KROK 0:** `blog/queue/_preflight-partia5.json`, oczekiwany wynik **9x OK,
> 0 RYZYKO, 0 BRAK** (7 tematów + 2 rezerwy). ⚠ Wynik policzony ręcznie wg logiki skryptu
> (keywordy to dosłowne podciągi katalogu, sprawdzone też przeciw blobom `streaks`
> i `therapist-sharing`). Przed przekazaniem do `blog-writer` lider uruchamia:
> `python scripts/blog-coverage-preflight.py --temat blog/queue/_preflight-partia5.json`.
>
> **Status danych:** `scripts/gsc/blog-tematy.py` uruchomiony 2026-09-28
> (`seo/blog/gsc-frazy/`): 0 luk, 124 wyświetlenia i 0 kliknięć bloga w roku, więc GSC nie
> daje popytu na nowe tematy. Frazy i pytania FAQ pochodzą z researchu SERP (brzmienia
> z tytułów konkurencji i z zapytań w formie pytań, które SERP zwraca jako tytuły stron),
> **bez wolumenów i bez KD** (Ahrefs niedostępny w tej sesji). Po pierwszych wyświetleniach:
> `scripts/gsc/blog-partia-frazy.py` i korekta H2 oraz FAQ na frazy z liczbami.
>
> ⚠ **Termin:** pierwszy wpis ma datę 2026-09-29, czyli jutro. Jeśli proza nie zdąży przed
> dripem o 07:00, przesuń CAŁĄ partię o tyle samo dni z zachowaniem kolejności (linki
> biegną tylko wstecz, więc przesunięcie całości niczego nie psuje).

## Zasady wspólne dla wszystkich 7 briefów (nie powtarzam ich w każdym)

1. **Szkielet Moniki jest nadrzędny.** Kolejność: otwarcie-rozpoznanie (bez H2, 60-120
   słów) → skąd to się bierze → jak to wygląda w życiu → co mówią badania → co możesz
   spróbować → akapit o apce w rytmie „This is what MindSync's [funkcja] is for. Log
   [3 konkrety z wpisu]. Give it time, and [funkcja] turns those entries into something you
   can see: [co]. Then [co dalej]." → jedno osobiste pytanie do czytelnika → blok
   `[FEATURES:]` → FAQ. Sekcje 2-4 wolno przestawić, apka i pytanie zawsze na końcu.
   **Długość: 900-1400 słów bez FAQ.** Jeden H2 na sekcję. Fraza główna w H1 i w jednym H2,
   bez upychania.
2. **Nagłówki jak zdania z rozmowy, często z dwukropkiem** (§2.1 pkt 12). Propozycje H2 niżej
   są wiążące co do sensu i miejsca frazy; autor może je doszlifować głosem Moniki, ale H2
   z frazą zostaje dosłownie.
3. **Humor:** 2-4 konkretne, przesadzone obrazki na wpis, najwięcej w otwarciu i w części
   praktycznej, zero w akapitach o badaniach i o cierpieniu. Haczyki w briefach to materiał,
   nie gotowe zdania. Maksymalnie jedna etykieta „Fun fact:" albo „Disclaimer:" na wpis.
4. **Zero zmyślonej biografii Moniki.** „I" tylko jako opinia („I feel like..."). Żadnych
   anegdot w pierwszej osobie, żadnych „my client", „a friend of mine".
5. **Zakaz obu myślników.** Zero U+2014 i zero U+2013 w tytule, meta, zajawce, treści,
   kartach i schema. Przebuduj zdanie. Zakres liczbowy zwykłym łącznikiem: „30-45 minutes".
   Bramka dripu łapie tylko U+2014, półpauzę sprawdź wyszukiwarką po znaku.
6. **YMYL:** zero diagnozowania, zero interpretowania objawów czytelnika, zero obietnic
   zdrowotnych, zero zniechęcania do terapii i leków, zero treści kryzysowych. MindSync
   uzupełnia terapię, nie zastępuje. Każdy brief ma własną listę „czego NIE twierdzić".
7. **Funkcje `planned` nie istnieją w treści:** `therapist-sharing` i `streaks`. „Bring it to
   your next session" wolno (czytelnik sam niesie notatki), zero sugestii wysyłania czegoś
   terapeucie z apki. Habit Tracker i ekran wyboru trybu w Reflect są poza katalogiem: nie
   opisuj ich i nie opieraj na nich zdań. **Nazwy funkcji z katalogu:** „Between-session voice
   notes", „Wellbeing check-ins", „Mood & focus-area trends", „Weekly & monthly summaries",
   „Therapy timeline", „Workspace", „Reflect", „Prep Card", „After-therapy debrief", „Session
   recording & summaries", „Goals", „Therapy relationship check".
8. **Dwie lekcje z partii 4 (twarde):**
   - **Mood & focus-area trends wykreśla tylko oceny z check-inów.** Nie wykrywa ludzi,
     tematów ani wzorców w notatkach. Gdy akapit o apce mówi o notatkach głosowych, „Give it
     time" opiera się na Weekly & monthly summaries albo Therapy timeline, a trends pojawia
     się tylko przy ocenach (np. „rate your anxiety each morning").
   - **Voice notes to transkrypcje bez odtwarzania.** Nigdy „listen back", „hear yourself",
     „replay". Zamiast tego „read back", „see what you said".
9. **Karty:** jedna `[FEATURE:]` inline plus blok `[FEATURES:]` z trzema pozycjami przed FAQ.
   Tylko id z listy danego briefu, żadne id nie powtarza się w obrębie wpisu. Zdania kart są
   nowe (nie przepisuj sformułowań z partii 1-4). Zero cen.
10. **FAQ:** H2 dokładnie `Frequently asked questions`, pytania w H3 dokładnie w brzmieniu
    z briefu, 4-5 sztuk. Odpowiedź 40-70 słów, pierwsze zdanie to pełna odpowiedź (GEO),
    dalej warunek albo zastrzeżenie. Głosem Moniki, bez humoru.
11. **Badania:** opowiadane jak historia z rokiem na początku („In 2013, Finkel and
    colleagues..."). Nazwa czasopisma albo instytucji w zdaniu, link w tę nazwę (RichText `a`),
    nigdy goły URL. Autor **weryfikuje każdą liczbę u źródła pierwotnego**. Pozycje „liczba do
    potwierdzenia" idą jakościowo, jeśli liczby nie da się potwierdzić. Po każdym badaniu 1-2
    krótkie zdania „co to znaczy dla ciebie" i jedno uczciwe zdanie o granicy badania.
12. **Linki wewnętrzne wyłącznie względne:** `<a href="/journal/slug">`, `<a href="/features">`,
    `<a href="/pre-order/...">`. Nigdy `https://mindsync.app/...` w treści.
13. **Linkowanie w partii biegnie wyłącznie wstecz** (tabela niżej), więc w tej partii nie ma
    `[LINK-LATER:]`. Jeśli wpis-cel się opóźni, a wpis linkujący nie, link zamień na
    `[LINK-LATER: <slug> | <ten sam anchor>]` i zgłoś liderowi.
14. **Pole `glos`: `"monika-v1"`** w każdym pliku kolejki (wymóg `blog-voice-check.py`).

## Kolejność publikacji, daty i topologia linkowania

| data | # | plik w kolejce | slug (`seo_url`) | klaster | kategoria | `kolor` | linki wstecz w partii |
|---|---|---|---|---|---|---|---|
| 2026-09-29 | 01 | `2026-09-29_morning-anxiety.json` | `morning-anxiety` | 5 | Therapy | `#339499` | brak (tylko wpisy na żywo) |
| 2026-09-30 | 02 | `2026-09-30_how-to-stop-overthinking.json` | `how-to-stop-overthinking` | 3 | MindSync Tips | `#ff9f8a` | → 01 |
| 2026-10-01 | 03 | `2026-10-01_online-vs-in-person-therapy.json` | `online-vs-in-person-therapy` | 4 | Therapy | `#1f3d38` | brak |
| 2026-10-02 | 04 | `2026-10-02_avoidant-attachment-style.json` | `avoidant-attachment-style` | 3 | Therapy | `#e8af0a` | brak (duet z żywym anxious) |
| 2026-10-03 | 05 | `2026-10-03_play-for-adults.json` | `play-for-adults` | 5 | MindSync Tips | `#3c67a5` | → 01 |
| 2026-10-04 | 06 | `2026-10-04_same-argument-over-and-over.json` | `same-argument-over-and-over` | 3 | Therapy | `#339499` | → 04, → 02 |
| 2026-10-05 | 07 | `2026-10-05_when-to-stop-therapy.json` | `when-to-stop-therapy` | 1 | Therapy | `#ff9f8a` | → 03 |

Kolory: ostatni opublikowany wpis (`anxious-attachment-style`, 2026-09-28) ma `#3c67a5`, więc
sekwencja `#3c67a5` → `#339499` → `#ff9f8a` → `#1f3d38` → `#e8af0a` → `#3c67a5` → `#339499` →
`#ff9f8a`, sąsiednie różne.

Klastry przeplatane (5, 3, 4, 3, 5, 3, 1), żaden klaster nie wychodzi dwa dni z rzędu.

**Wzmocnienie po partii (zadanie PATCH dla `webflow-publisher`, nie dla autora):**
- z `racing-thoughts-at-night` do `morning-anxiety` (anchor „the morning version of the same
  alarm") i do `how-to-stop-overthinking` (anchor „the daytime loop"),
- z `anxious-attachment-style` do `avoidant-attachment-style` (anchor „the other side of the
  same dance"), bo tamten wpis zapowiada duet,
- z `how-long-therapy-takes-to-work` i `how-to-know-if-therapy-is-working` do
  `when-to-stop-therapy` (anchor „what a good ending looks like"),
- z `how-to-choose-a-therapist` do `online-vs-in-person-therapy` (anchor „whether to meet in
  a room or on a screen").

---

# 01. Morning anxiety

**1. Meta**
- `seo_url`: `morning-anxiety` | plik: `blog/queue/2026-09-29_morning-anxiety.json`
- kategoria: `Therapy` | `kolor`: `#339499` | `planowana_data`: **2026-09-29**
- `tagi`: `["modern-life", "anxiety"]`
- H1: „Anxious Before Your Feet Hit the Floor: What Morning Anxiety Is Actually Doing"
- `meta_title` (51 zn.): „Morning Anxiety: Why You Wake Up Anxious | MindSync"
- `meta_description` (159 zn.): „Waking up anxious before anything has happened? What the
  cortisol awakening response is, how yesterday shapes it, and five ways to make the first
  hour gentler."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `morning anxiety`
- poboczne: `waking up with anxiety`, `why do I wake up anxious`, `anxiety worse in the morning`,
  `cortisol awakening response`, `how to stop morning anxiety`, `waking up with anxiety for no
  reason`
- intencja: ktoś budzi się ze ściśniętym żołądkiem, zanim cokolwiek się wydarzyło, i szuka
  wyjaśnienia „dlaczego rano" oraz sposobu na pierwszą godzinę. Telefon, łóżko, 6:30.
- luka: SERP (Healthline, Cleveland Clinic, Talkspace, Nurx, dziesiątki gabinetów) powtarza
  „cortisol peaks in the morning" jako całe wyjaśnienie i daje listę porad (oddech, kofeina,
  ruch). **Nikt nie opowiada badania, które łączy poranek z wczorajszym wieczorem** (Adam
  i wsp. 2006: samotność, smutek, poczucie zagrożenia i braku kontroli poprzedniego dnia szły
  w parze z wyższym porannym wyrzutem kortyzolu następnego dnia), **ani nie mówi uczciwie,
  że poranny wyrzut to nie usterka** (Powell i Schlotz 2012: wyższy wyrzut wiązał się
  ze słabszą reakcją na stres w ciągu dnia). Nasz kąt: poranny alarm to ciało, które
  przygotowuje cię na dzień, z pamięcią wczoraj; nie trzeba go gasić, trzeba mu dać coś
  do roboty.

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** „Do any of these sound familiar?" + trzy scenki, ostatnia krótka
  z mrugnięciem. Haczyki: serce bije jak przed egzaminem, choć dziś jest zwykły wtorek;
  sprawdzasz maila, zanim otworzysz oczy do końca, „just to know what you're dealing with";
  budzik zadzwonił, ale twój układ nerwowy był na nogach 20 minut wcześniej.
- **H2: „Why is it worse in the morning?"** (skąd to się bierze)
  - cortisol awakening response prostym językiem: w pierwszym mniej więcej pół godziny po
    przebudzeniu kortyzol gwałtownie rośnie, niezależnie od dobowego rytmu. To mechanizm
    „wstawania", nie awaria. Analogia: silnik, który zawsze się grzeje przed jazdą; u osoby
    zestresowanej grzeje się jak przed rajdem.
  - fragment cytowalny 40-60 słów (definicja CAR, patrz GEO).
  - slot na **„Fun fact:"**: poranny wyrzut kortyzolu to stała cecha osi stresu u zdrowych
    ludzi, nie sygnał, że coś jest nie tak (brzmienie tylko w granicach Fries 2009; bez
    dopowiedzeń typu „even if you slept perfectly", których źródło nie mówi).
  - jedno zdanie o nocy z linkiem do `/journal/racing-thoughts-at-night` (to, co nie
    dokończyło się wieczorem, często czeka rano).
- **H2: „Morning anxiety, as it actually shows up:"** (fraza główna w H2; jak to wygląda)
  - lista w drugiej osobie, 4-5 punktów: ucisk w klatce przed otwarciem oczu; lista zadań
    odtwarzana w głowie jeszcze w łóżku; mdłości na widok śniadania; telefon jako pierwszy
    ruch dnia; ulga koło 10:00, kiedy dzień już „ruszył".
  - H3: „When it's worse on certain days" (niedziela wieczorem, poniedziałek rano, dzień po
    trudnej rozmowie). Link do `/journal/sunday-scaries` jednym zdaniem.
- **H2: „What research turned up:"** (badania)
  - 2006, Adam, Hawkley, Kudielka i Cacioppo, *PNAS*: 156 osób, trzy dni dziennika
    wieczorem i ślina rano. Samotność, smutek, poczucie zagrożenia i braku kontroli
    poprzedniego dnia wiązały się z wyższym porannym wyrzutem następnego dnia, a poranny
    wyrzut nie przewidywał tych stanów później tego samego dnia. Wniosek jej głosem:
    „Your morning is carrying yesterday's mail." Granica: osoby 50-68 lat, trzy dni, związek,
    nie dowód przyczyny.
  - 2012, Powell i Schlotz, *PLOS ONE*: 23 osoby. Nie znaleźli związku między
    przewidywanym stresem a porannym wyrzutem, za to w dniach z wyższym wyrzutem ludzie
    słabiej reagowali stresem na to, co się wydarzyło. Wniosek: ten poranny skok może być
    przygotowaniem, nie wrogiem. Granica: bardzo mała próba, traktuj jako ciekawą wskazówkę.
  - uczciwe zdanie: badania mierzą kortyzol w ślinie, nie lęk, który czujesz; to dwie różne
    rzeczy i nie należy ich utożsamiać.
- **H2: „Five places to start tomorrow morning:"** (co spróbować; tryb rozkazujący)
  1. Give the alarm a job. Wstań i zrób jedną fizyczną rzecz (woda, okno, schody), zanim
     otworzysz telefon. Haczyk: czytanie maili w łóżku to „attending a meeting in your
     pajamas that nobody invited you to".
  2. Rate it before you explain it. Oceń lęk w skali, zanim zaczniesz szukać powodu. Tu
     inline karta `check-ins`.
  3. Close yesterday the night before: dwa zdania wieczorem o tym, co zostało otwarte.
     Link do `/journal/regulate-nervous-system-between-therapy-sessions` przy wyciszaniu
     ciała.
  4. Move the phone out of reach of the bed (bez moralizowania, z uzasadnieniem).
  5. Say the sentence: „This is my body getting ready, not proof that today will go badly."
     Gotowe zdanie do powiedzenia na głos (wymóg §2.5).
  - jeden spokojny akapit: jeśli poranny lęk trwa tygodniami albo zabiera ci poranki,
    powiedz o tym lekarzowi albo terapeucie; link do `/journal/early-signs-of-burnout` przy
    zdaniu, że przewlekły stres w pracy też bywa za tym.
  - puenta sekcji, w stylu „The alarm isn't the problem. Having nothing to do with it is."
- **Akapit o apce:** „This is what MindSync's Wellbeing check-ins are for. Log your anxiety
  within ten minutes of waking, how you slept, and one line about what yesterday evening
  held. Give it time, and Mood & focus-area trends turns those ratings into something you
  can see: [which mornings run loud, and whether a bad night's sleep comes before them].
  Then [bring the loudest week to your next session]." Uwaga: trends wykreśla oceny (lęk,
  sen), notatkę o wieczorze czytasz sam na osi czasu.
- **Pytanie do czytelnika:** np. „What's the first thought you have in the morning, before
  you've decided to have it?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: Why do I wake up with anxiety every morning?
  - H3: Why is my anxiety worse in the morning?
  - H3: Is morning anxiety normal?
  - H3: How long does morning anxiety last?
  - H3: How do I stop waking up with anxiety?
  - ⚠ odpowiedź o „How long": uczciwie, że dla wielu osób słabnie w pierwszych godzinach
    dnia, bez podawania liczby minut jako normy; jeśli nie mija albo narasta, to temat na
    rozmowę z profesjonalistą.

**4. Karty funkcji** (bramka: check-ins, daily-affirmation, mood-trends, voice-notes, reflect,
session-debrief, smart-reminders; używamy czterech)
- inline w „Five places to start tomorrow morning" (krok 2):
  `[FEATURE: check-ins | A number between one and ten, logged before the story about why arrives, so the story has something honest to answer to.]`
- blok przed FAQ:
  `[FEATURES: A gentler first hour || mood-trends | A few weeks of morning ratings on one screen, where the rough mornings start to line up with the nights before them. || voice-notes | Say the leftover worry out loud the evening before, so it is written down somewhere other than your chest at 6 a.m. || daily-affirmation | One grounded line waiting on the home screen, which is a better first read than the inbox.]`

**5. Mapa linkowania** (tylko wpisy na żywo)
- `<a href="/journal/racing-thoughts-at-night">` anchor „the thoughts that kept you up last
  night" (sekcja „Why is it worse in the morning?")
- `<a href="/journal/sunday-scaries">` anchor „the Monday version starts on Sunday" (H3)
- `<a href="/journal/regulate-nervous-system-between-therapy-sessions">` anchor „bringing
  your body down before bed" (krok 3)
- `<a href="/journal/early-signs-of-burnout">` anchor „stress that follows you home from
  work" (akapit spokojny)
- **Landing partner:** `/pre-order/track-interventions` (anchor „seeing which morning change
  actually makes a difference"), jeden raz, przy krokach.

**6. GEO**
- Definicja cortisol awakening response, 40-60 słów: wzrost kortyzolu w pierwszych
  kilkudziesięciu minutach po przebudzeniu, osobny od dobowego rytmu, normalny mechanizm
  przygotowania na dzień.
- Odpowiedź na „Why do I wake up with anxiety every morning?", 50-70 słów, z Adam 2006
  (wczorajszy dzień widać w porannym wyrzucie) i zastrzeżeniem, że to związek.

**7. Hero**
- Wariant „codzienny moment": szklanka wody na parapecie w pierwszym porannym świetle,
  uchylone okno, zwinięta pościel w tle; bez osoby, bez telefonu.
- `hero_image_alt`: „A glass of water on a windowsill in early morning light next to an open
  window"
- nazwa pliku hero: `morning-anxiety-hero.webp`

**8. Źródła (zweryfikowane 2026-09-28)**
- **POTWIERDZONE (WebFetch PMC).** Adam E.K., Hawkley L.C., Kudielka B.M., Cacioppo J.T.,
  2006, *PNAS* 103(45):17058-17063, „Day-to-day dynamics of experience-cortisol associations
  in a population-based sample of older adults". https://pmc.ncbi.nlm.nih.gov/articles/PMC1636578/
  N = 156, wiek 50-68, trzy dni; zdanie z abstraktu: prior-day loneliness, sadness, threat
  and lack of control associated with a higher cortisol awakening response the next day.
- **POTWIERDZONE (WebFetch).** Powell D.J., Schlotz W., 2012, *PLOS ONE* 7(12):e52067,
  „Daily life stress and the cortisol awakening response: testing the anticipation
  hypothesis". https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0052067
  N = 23; brak związku z przewidywanym stresem; wyższy wyrzut = słabsza reakcja na stres
  tego dnia.
- **POTWIERDZONE (istnienie i zakres), liczby do potwierdzenia.** Fries E., Dettenborn L.,
  Kirschbaum C., 2009, *International Journal of Psychophysiology* 72(1):67-73, „The cortisol
  awakening response (CAR): facts and future directions".
  https://pubmed.ncbi.nlm.nih.gov/18854200/ Źródło do definicji. ⚠ Procentu wzrostu i okna
  minut nie podawaj bez abstraktu przed oczami (PubMed zwrócił CAPTCHA); jakościowo:
  „rises sharply in roughly the first half hour after waking".
- **Czego autor ma NIE twierdzić:**
  - że poranny lęk to objaw zaburzenia lękowego albo depresji (diagnostyka),
  - że kortyzol „powoduje" lęk albo że trzeba go „obniżyć" suplementami, dietą czy
    „cortisol detox" (SERP jest tym zalany),
  - żadnych porad o lekach, alkoholu, kofeinie w dawkach,
  - że MindSync zmniejsza poranny lęk. Apka pokazuje przebieg ocen, człowiek wyciąga wnioski.

**9. Czego NIE robić**
- Nie dubluj wieczornego rytuału z `/journal/racing-thoughts-at-night` (tam „move the thinking
  earlier"); tu jeden krok o zamknięciu dnia i link.
- Zero rutyny porannej „5 a.m. club": to wellness jako kolejny deadline.

---

# 02. How to stop overthinking

**1. Meta**
- `seo_url`: `how-to-stop-overthinking` | plik: `blog/queue/2026-09-30_how-to-stop-overthinking.json`
- kategoria: `MindSync Tips` | `kolor`: `#ff9f8a` | `planowana_data`: **2026-09-30**
- `tagi`: `["understanding-patterns", "overthinking"]`
- H1: „The Loop That Feels Like Problem-Solving: How to Stop Overthinking"
- `meta_title` (54 zn.): „How to Stop Overthinking Without Forcing It | MindSync"
- `meta_description` (155 zn.): „Overthinking feels like problem-solving, but it rarely
  solves anything. Why the loop starts, what research found about why versus how, and how to
  step out."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `how to stop overthinking`
- poboczne: `why do I overthink everything`, `how to stop overthinking a situation`,
  `rumination`, `how to stop ruminating`, `overthinking and anxiety`, `overthinking vs
  problem solving`
- intencja: ktoś od godziny „analizuje" jedną rozmowę albo decyzję, wie, że się kręci w kółko,
  i chce przestać. Dzień, praca, telefon w przerwie.
- luka: SERP (Rula, Healthline, Psychology Today, CTRI, dziesiątki gabinetów) daje zestaw
  „identify triggers, mindfulness, thought-stopping, distraction". **Prawie nikt nie podaje
  badania, które mówi, JAK myśleć zamiast „nie myśleć"**: Watkins i Moulds 2005 (konkretne
  „how" dawało więcej i lepsze rozwiązania niż abstrakcyjne „why") oraz Kross i wsp. 2014
  (mówienie do siebie po imieniu albo „you" zamiast „I" dawało dystans pod stresem).
  Nasz kąt: overthinking udaje rozwiązywanie problemu; nie trzeba przestać myśleć, trzeba
  zmienić pytanie z „why" na „what next".
- ⚠ granica: `/journal/racing-thoughts-at-night` ma już trójpodział worry / rumination /
  racing thoughts i FAQ „How do I stop overthinking at night?". Tu zero nocy, jedno zdanie
  i link.

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** pytanie o konkretny moment, jak u Moniki: „When did you last replay
  a conversation that ended hours ago? How many versions of your reply have you written
  since?" Haczyki: wiadomość „ok" analizowana dłużej, niż trwała cała rozmowa; wybór
  restauracji, który wymaga trzech zakładek z recenzjami i konsultacji z przyjaciółką;
  mózg z 46 otwartymi kartami (obraz Moniki z §2.1, wolno użyć raz, własnymi słowami).
- **H2: „Why does your brain keep doing this?"** (skąd to się bierze)
  - overthinking to próba odzyskania kontroli: mózg traktuje niepewność jak problem do
    rozwiązania i obiecuje, że jeszcze jedno okrążenie da odpowiedź. Analogia: GPS, który
    „recalculating" w kółko, bo stoisz na parkingu.
  - rumination prostym językiem: powtarzalne myślenie o tym, co się czuje i dlaczego,
    bez przejścia do działania. Fragment cytowalny (GEO).
  - slot na **„Disclaimer:"**, np. „Disclaimer: thinking things through is not the problem.
    Thinking them through for the fourteenth time is."
- **H2: „Signs you're overthinking, not problem-solving:"** (jak to wygląda)
  - druga osoba, 4-5 punktów: pytanie w głowie zaczyna się od „why" i nie ma końca;
    kolejne okrążenie nie daje nowej informacji; im dłużej myślisz, tym gorzej się czujesz,
    a nie jaśniej; szukasz pewności, której sytuacja nie może dać; odkładasz decyzję „aż
    będziesz pewny".
  - link do `/journal/morning-anxiety` (wstecz do 01) jednym zdaniem: czasem pętla zaczyna
    się, zanim wstaniesz.
- **H2: „What research turned up:"** (badania)
  - 2008, Nolen-Hoeksema, Wisco i Lyubomirsky, *Perspectives on Psychological Science*:
    przegląd badań; ruminacja pogłębia negatywne myślenie, psuje rozwiązywanie problemów
    i utrudnia działanie. Wniosek: czucie, że „pracujesz nad tym", to nie dowód, że pracujesz.
  - 2005, Watkins i Moulds, *Emotion*: osoby z depresją, losowo skierowane do myślenia
    „abstrakcyjnego" (dlaczego, co to znaczy) albo „konkretnego" (jak, co dokładnie się
    stało, co teraz). Oba tryby psuły nastrój, ale konkretny dał więcej i lepszych rozwiązań
    problemów. Wniosek dwoma zdaniami: „Why keeps the loop open. How starts closing it."
    Granica: badanie na osobach z depresją; mechanizm opisuje się szerzej, ale to nie jest
    test na ogólnej populacji.
  - 2014, Kross i wsp., *Journal of Personality and Social Psychology*: siedem badań, 585
    osób. Mówienie do siebie po imieniu albo w drugiej osobie zamiast „I" dawało więcej
    dystansu i lepszą regulację emocji pod stresem społecznym. Wniosek: mała zmiana w języku
    robi miejsce między tobą a pętlą.
- **H2: „How to stop overthinking without trying to stop thinking:"** (fraza główna w H2;
  co spróbować; tryb rozkazujący)
  1. Swap „why" for „what next". Gotowe zdanie: „What's one thing I can do about this
     before tonight?"
  2. Talk to yourself by name for one minute. Haczyk: brzmi jak coś, co robią sportowcy
     w reklamach butów, i trochę tak jest.
  3. Get it out of your head and into words: powiedz pętlę na głos w 60 sekund, a potem
     przeczytaj, co powiedziałeś. Tu inline karta `voice-notes`. Link do
     `/journal/journaling-vs-voice-notes` przy wyborze formy.
  4. Set a stopping point for decisions that have no perfect answer (wybierz „good enough"
     i datę). Haczyk: menu restauracji nie jest egzaminem z charakteru.
  5. Name the feeling under the loop. Link do `/journal/how-to-name-what-you-feel`.
  - spokojny akapit: jeśli pętla zabiera ci dni, sen albo apetyt, to temat na rozmowę
    z terapeutą; link do `/journal/how-to-prepare-for-a-therapy-session` („take the loop
    into your next session").
  - puenta, w stylu „You can't think your way out of a loop that thinking built."
- **Akapit o apce:** „This is what MindSync's Between-session voice notes are for. Log the
  loop in sixty seconds, the question you keep asking, and the one next step you picked
  instead. Give it time, and your Weekly & monthly summaries turn those entries into
  something you can read: [which questions keep coming back, week after week]. Then pin the
  one that won't let go in your Workspace and bring it to your next session." (Tu NIE
  trends: to notatki, nie oceny.)
- **Pytanie do czytelnika:** np. „What's the question your brain keeps asking that nobody
  could actually answer?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: Why do I overthink everything?
  - H3: How do I stop overthinking a situation?
  - H3: What is the difference between overthinking and rumination?
  - H3: Is overthinking a sign of anxiety?
  - H3: Does writing things down help with overthinking?
  - ⚠ „Is overthinking a sign of anxiety?": uczciwie, że overthinking występuje przy lęku
    i depresji, ale sam w sobie nie jest rozpoznaniem; zmartwienie, które nie odpuszcza, to
    powód do rozmowy z profesjonalistą, nie do autodiagnozy.

**4. Karty funkcji** (bramka: voice-notes, reflect, mood-trends, personal-bio, workspace,
summaries; używamy czterech: voice-notes, reflect, summaries, workspace)
- inline w „How to stop overthinking..." (krok 3):
  `[FEATURE: voice-notes | Sixty seconds out loud, then the loop is sitting there as text, which is usually shorter and less convincing than it sounded in your head.]`
- blok przed FAQ:
  `[FEATURES: Turning why into what next || reflect | For the question you keep circling, a guided conversation that keeps asking what you could actually do about it. || summaries | A weekly read of what took up your head, so the questions that repeat stop pretending to be new. || workspace | Park the one that will not let go, so it has somewhere to wait that is not your afternoon.]`

**5. Mapa linkowania**
- `<a href="/journal/morning-anxiety">` anchor „the loop that starts before you get out of
  bed" (wstecz do 01, publikacja 2026-09-29)
- `<a href="/journal/racing-thoughts-at-night">` anchor „the night shift of the same loop"
  (sekcja „Why does your brain keep doing this?", jedno zdanie granicy)
- `<a href="/journal/journaling-vs-voice-notes">` anchor „whether to write it or say it"
  (krok 3)
- `<a href="/journal/how-to-name-what-you-feel">` anchor „the feeling under the loop" (krok 5)
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` anchor „take the loop into your
  next session" (akapit spokojny)
- **Landing partner:** brak (żaden landing nie pasuje bez naciągania; karty wystarczą).

**6. GEO**
- Definicja rumination, 40-60 słów: powtarzalne, bierne myślenie o tym, co czujesz,
  jego przyczynach i skutkach, bez przejścia do działania (za Nolen-Hoeksema 2008).
- Teza „concrete how beats abstract why", 50-70 słów, z Watkins i Moulds 2005 i granicą
  próby. Musi działać wyjęta z kontekstu.

**7. Hero**
- Wariant „spokojna abstrakcja" albo „codzienny moment": ołówek leżący na kartce z jedną
  zakreśloną linijką, obok kubek, miękkie popołudniowe światło; paleta mint i sand.
- `hero_image_alt`: „A pencil resting on a notepad with a single circled line beside a mug in
  soft afternoon light"
- nazwa pliku hero: `how-to-stop-overthinking-hero.webp`

**8. Źródła (zweryfikowane 2026-09-28)**
- **POTWIERDZONE (WebSearch, strona wydawcy).** Nolen-Hoeksema S., Wisco B.E., Lyubomirsky S.,
  2008, *Perspectives on Psychological Science* 3(5):400-424, „Rethinking Rumination".
  https://journals.sagepub.com/doi/10.1111/j.1745-6924.2008.00088.x
- **POTWIERDZONE (abstrakt).** Watkins E., Moulds M.L., 2005, *Emotion* 5(3):319-328,
  „Distinct modes of ruminative self-focus: impact of abstract versus concrete rumination on
  problem solving in depression". https://doi.org/10.1037/1528-3542.5.3.319
  Konkretna ruminacja = więcej i skuteczniejszych rozwiązań; oba tryby obniżały nastrój.
- **POTWIERDZONE (abstrakt, PubMed 24467424).** Kross E., Bruehlman-Senecal E., Park J.,
  Burson A., Dougherty A., Shablack H., Bremner R., Moser J., Ayduk O., 2014, *Journal of
  Personality and Social Psychology* 106(2):304-324, „Self-talk as a regulatory mechanism:
  How you do it matters". https://pubmed.ncbi.nlm.nih.gov/24467424/ Siedem badań, N = 585.
- **Czego autor ma NIE twierdzić:**
  - że overthinking to objaw lęku, ADHD czy OCD u czytelnika (SERP często tak robi),
  - że „thought-stopping" działa (to technika z kiepskimi dowodami; po prostu jej nie
    polecaj),
  - że mówienie do siebie po imieniu „leczy" cokolwiek; to narzędzie dystansu,
  - że MindSync przerywa pętlę. Apka daje miejsce na zapis i obraz tego, co się powtarza.

**9. Czego NIE robić**
- Zero nocy i zasypiania (to `/journal/racing-thoughts-at-night`).
- Nie wchodź w metodykę triggerów (`/journal/how-to-identify-emotional-triggers`).

---

# 03. Online vs in-person therapy

**1. Meta**
- `seo_url`: `online-vs-in-person-therapy` | plik:
  `blog/queue/2026-10-01_online-vs-in-person-therapy.json`
- kategoria: `Therapy` | `kolor`: `#1f3d38` | `planowana_data`: **2026-10-01**
- `tagi`: `["therapy-logistics", "online-therapy"]`
- H1: „The Room or the Laptop: Online vs In-Person Therapy, Honestly Compared"
- `meta_title` (59 zn.): „Online vs In-Person Therapy: Which Works Better? | MindSync"
- `meta_description` (158 zn.): „Is online therapy as effective as in-person? What 54 trials
  found, what a screen changes about the room, and how to pick the one you will keep showing
  up for."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `online vs in-person therapy`
- poboczne: `is online therapy as effective as in-person`, `online therapy vs in person`,
  `pros and cons of online therapy`, `disadvantages of online therapy`, `teletherapy vs
  in-person`, `video therapy`
- intencja: decyzja przed pierwszą sesją albo przy zmianie (przeprowadzka, nowa praca, koniec
  umowy z gabinetem). Człowiek chce wiedzieć, czy online „się liczy" i co traci.
- luka: SERP (Two Chairs, Psychology Today, Psychology.org, gabinety, platformy) odpowiada
  „both work, it depends". **Mało kto podaje konkretną liczbę badań i uczciwą granicę**
  (Zandieh i wsp. 2024: 54 badania RCT, 5463 osoby, praktycznie brak różnicy dla CBT
  prowadzonej przez terapeutę; Hedman-Lagerlöf i wsp. 2023: 31 badań, to samo),
  **i nikt nie mówi o rzeczy, którą online zabiera po cichu: drodze do domu po sesji**,
  czyli czasie na przetrawienie, oraz o lustrze we własnym okienku (Bailenson 2021). Nasz
  kąt: skuteczność to w dużej mierze remis, różnica leży w logistyce wokół sesji, a tę da się
  zaprojektować.
- ⚠ granica: koszt i FAQ „Is online therapy cheaper than in person?" należą do
  `/journal/is-therapy-worth-the-money` (jedno zdanie i link, bez liczb o cenach).

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** obserwacja o tym, jak żyjemy, spokojnie i trochę ironicznie:
  „Somewhere around 2020, therapy moved into the same laptop as your spreadsheets." Haczyki:
  płaczesz o dzieciństwie, a obok migocze powiadomienie ze Slacka; sesja kończy się
  kliknięciem „Leave meeting" i po 40 sekundach jesteś w kuchni przy zmywarce; pies, który
  zawsze wie, kiedy mówisz coś ważnego.
- **H2: „What changes when the room is a screen?"** (skąd to się bierze: mechanizm różnic)
  - w gabinecie jest droga tam i z powrotem: bufor, w którym głowa zaczyna i kończy pracę.
    Online bufor znika, jeśli go nie zbudujesz. Link do `/journal/therapy-hangover` przy
    zdaniu o tym, co zostaje po sesji.
  - lustro: w wideo widzisz siebie przez godzinę. Bailenson 2021 opisał to jako jedno ze
    źródeł zmęczenia wideo („mirror anxiety"), obok patrzenia z bliska i unieruchomienia
    przed kamerą. Uczciwie: to argument teoretyczny, nie wynik badania terapii.
  - slot na **„Fun fact:"**: większość komunikatorów pozwala ukryć własny podgląd, a mało kto
    o tym wie (bez nazw marek i bez instrukcji klikania).
- **H2: „Online vs in-person therapy, side by side:"** (fraza główna w H2; jak to wygląda)
  - lista w drugiej osobie, nie tabela (RichText bez `table`): online wygrywa, gdy dojazd
    zjada godzinę, gdy mieszkasz daleko od specjalisty, którego potrzebujesz, gdy wychodzenie
    z domu jest trudne; stacjonarnie wygrywa, gdy w domu nie ma prywatnego miejsca, gdy
    potrzebujesz granicy „tam pracuję, tu żyję", gdy ekran cię rozprasza.
  - H3: „What about privacy at home?" (słuchawki, zamknięte drzwi, sesja w samochodzie
    jako realny, choć mało elegancki wybór; bez straszenia).
- **H2: „What research turned up:"** (badania)
  - 2024, Zandieh i wsp., *CMAJ*: 54 badania RCT, 5463 osoby; CBT prowadzona przez terapeutę
    zdalnie (wideo, telefon, internet z terapeutą) i na żywo dawały praktycznie te same
    efekty, dowody o umiarkowanej pewności. Wniosek: „The screen isn't the weak link."
  - 2023, Hedman-Lagerlöf i wsp., *World Psychiatry*: 31 badań, 3053 osoby, terapia
    internetowa ze wsparciem terapeuty dawała podobne efekty jak twarzą w twarz.
  - 2014, Simpson i Reid, *Australian Journal of Rural Health*: przegląd 23 prac o więzi
    terapeutycznej w wideo; silną więź da się zbudować od pierwszych sesji.
  - uczciwa granica, jej głosem: większość badań dotyczy CBT i częstych problemów (lęk,
    obniżony nastrój, bezsenność), a nie każdego rodzaju terapii i nie każdej sytuacji;
    aplikacje bez terapeuty to inna kategoria i te wyniki ich nie dotyczą.
- **H2: „How to choose, and how to make either one work:"** (co spróbować)
  1. Pick the format you will actually show up for. Regularność bije idealny format.
     Link do `/journal/how-to-choose-a-therapist`.
  2. Build a fake commute. 10 minut przed i po sesji online: spacer wokół bloku, herbata,
     zero ekranu. Haczyk: „walking to nowhere so your brain knows therapy has ended".
  3. Hide your own video if the mirror distracts you, i powiedz terapeucie, że to robisz.
     Gotowe zdanie: „I'm going to turn off my self-view, it helps me focus on you."
  4. Keep the minutes after the session for yourself: zapisz, co zostało, zanim wrócisz
     do maili. Tu inline karta `session-debrief`.
  5. Try the other format once before you decide it's not for you.
  - jeden akapit: nagrywanie sesji (online czy w gabinecie) tylko za zgodą terapeuty; zapytaj
    na początku, zanim cokolwiek włączysz.
  - puenta, w stylu „The format matters less than what you do with the ten minutes after."
- **Akapit o apce:** „This is what MindSync's After-therapy debrief is for. Log what surprised
  you, the sentence your therapist said that you want to keep, and what you felt when the
  call ended. Give it time, and your Therapy timeline turns those entries into something you
  can see: [every session in one place, whichever room it happened in]. Then open your Prep
  Card before the next one." (Nazwy z katalogu.)
- **Pytanie do czytelnika:** np. „Where do you actually say the hard things out loud: in
  a room with someone, or in your own kitchen?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: Is online therapy as effective as in-person?
  - H3: What are the disadvantages of online therapy?
  - H3: Is it harder to open up in online therapy?
  - H3: Can you switch from online to in-person therapy?
  - H3: How do I prepare for an online therapy session?
  - ⚠ ostatnie pytanie: tylko logistyka (miejsce, słuchawki, bufor), treść przygotowania
    linkiem do `/journal/how-to-prepare-for-a-therapy-session`.

**4. Karty funkcji** (bramka: session-recording, session-prep, session-debrief, health-check;
używamy czterech; `timeline` z akapitu o apce nie ma karty, bo limit 4 i unikalność)
- inline w „How to choose..." (krok 4):
  `[FEATURE: session-debrief | The ten minutes after a video call are the easiest to lose, and the best place to write down what you want to keep.]`
- blok przed FAQ:
  `[FEATURES: Whichever room you choose || session-recording | With your therapist's permission, a transcript and key takeaways, so the session does not vanish with the call window. || session-prep | Walk in, or log in, with your topics already waiting instead of starting from how was your week. || health-check | A short check on how the working relationship feels, useful when you cannot tell whether it is the format or the fit.]`

**5. Mapa linkowania** (tylko wpisy na żywo)
- `<a href="/journal/therapy-hangover">` anchor „the heavy hour after a session" (sekcja
  „What changes when the room is a screen?")
- `<a href="/journal/how-to-choose-a-therapist">` anchor „finding the right person first"
  (krok 1)
- `<a href="/journal/is-therapy-worth-the-money">` anchor „what the cost difference really
  looks like" (jedno zdanie granicy)
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` anchor „what to bring into the
  session itself" (FAQ)
- `<a href="/journal/how-to-remember-what-you-talk-about-in-therapy">` anchor „keeping more of
  what was said" (krok 4)
- **Landing partner:** brak (tracking-therapy-effectiveness trzyma 07; nie dubluj duetu).

**6. GEO**
- Odpowiedź na „Is online therapy as effective as in-person?", 50-70 słów: Zandieh 2024
  (54 RCT, CMAJ) + zastrzeżenie o CBT i terapeucie w roli prowadzącego.
- Lista 3 rzeczy, które online zmienia poza skutecznością (bufor, lustro, prywatność w domu),
  40-60 słów.

**7. Hero**
- Wariant „codzienny moment": otwarty laptop na stole kuchennym z ekranem odwróconym od widza,
  obok słuchawki i kubek, miękkie światło z okna; bez osoby, bez kozetki.
- `hero_image_alt`: „An open laptop on a kitchen table with headphones and a mug in soft
  window light"
- nazwa pliku hero: `online-vs-in-person-therapy-hero.webp`

**8. Źródła (zweryfikowane 2026-09-28)**
- **POTWIERDZONE (WebFetch CMAJ).** Zandieh S., Abdollahzadeh S.M., Sadeghirad B., Wang L.,
  McCabe R.E., Yao L., Inness B.E., Pathak A., Couban R.J., Crandon H., Torabiardakani K.,
  Bieling P., Busse J.W., 2024, *CMAJ* 196(10):E327-E340, „Therapist-guided remote versus
  in-person cognitive behavioural therapy: a systematic review and meta-analysis of
  randomized controlled trials". https://www.cmaj.ca/content/196/10/E327
  54 RCT, N = 5463; „little to no difference", moderate-certainty evidence; zdalnie = wideo,
  telefon, internet z terapeutą. W tekście wystarczy „Zandieh and colleagues".
- **POTWIERDZONE (WebFetch PMC).** Hedman-Lagerlöf E., Carlbring P., Svärdman F., Riper H.,
  Cuijpers P., Andersson G., 2023, *World Psychiatry* 22(2):305-314, „Therapist-supported
  Internet-based cognitive behaviour therapy yields similar effects as face-to-face therapy
  for psychiatric and somatic disorders". https://pmc.ncbi.nlm.nih.gov/articles/PMC10168168/
  31 RCT, N = 3053, g = 0.02. ⚠ Pełną listę autorów potwierdź na stronie; w tekście
  „Hedman-Lagerlöf and colleagues".
- **POTWIERDZONE (abstrakt).** Simpson S.G., Reid C.L., 2014, *Australian Journal of Rural
  Health* 22(6):280-299, „Therapeutic alliance in videoconferencing psychotherapy: a review".
  https://onlinelibrary.wiley.com/doi/10.1111/ajr.12149 23 prace.
- **POTWIERDZONE jako argument teoretyczny.** Bailenson J.N., 2021, *Technology, Mind, and
  Behavior* 2(1), „Nonverbal overload: A theoretical argument for the causes of Zoom
  fatigue". https://vhil.stanford.edu/sites/g/files/sbiybj29011/files/media/file/bailenson-apa-nonverbal-overload.pdf
  ⚠ Pisz „argued", nie „found". Nazwę „Zoom" zostaw tylko w tytule pracy, w zdaniu „video
  calls".
- **Czego autor ma NIE twierdzić:**
  - że online jest gorsze albo lepsze „w ogóle"; dane dotyczą głównie CBT z terapeutą,
  - że aplikacje (w tym MindSync) są formą terapii online; MindSync nie prowadzi terapii,
  - niczego o sytuacjach kryzysowych i bezpieczeństwie (to temat wymagający decyzji
    operatora); jeśli autor czuje potrzebę, jedno neutralne zdanie „some situations call for
    in-person care, and your therapist can tell you if yours is one",
  - że nagrywanie sesji jest w porządku bez zgody terapeuty.

**9. Czego NIE robić**
- Zero rankingów platform i nazw marek (BetterHelp, Talkspace): to nie jest wpis porównawczy
  usług.
- Zero cen i ubezpieczeń (to `/journal/is-therapy-worth-the-money`).

---

# 04. Avoidant attachment style

**1. Meta**
- `seo_url`: `avoidant-attachment-style` | plik:
  `blog/queue/2026-10-02_avoidant-attachment-style.json`
- kategoria: `Therapy` | `kolor`: `#e8af0a` | `planowana_data`: **2026-10-02**
- `tagi`: `["understanding-patterns", "relationships"]`
- H1: „'I'm Fine, I'll Handle It': Understanding an Avoidant Attachment Style"
- `meta_title` (58 zn.): „Avoidant Attachment Style: Signs, Roots, Change | MindSync"
- `meta_description` (150 zn.): „Calm on the outside, busy underneath. Why avoidant
  attachment forms, what research found when avoidant people were stressed, and what helps
  it soften."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `avoidant attachment style`
- poboczne: `signs of avoidant attachment`, `can avoidant attachment change`, `what causes
  avoidant attachment`, `dismissive avoidant`, `hyper-independence`, `how to love someone with
  avoidant attachment`
- intencja: dwie grupy. (a) ktoś rozpoznaje siebie („I pull away when it gets serious")
  i pyta, czy to się zmienia; (b) ktoś kocha osobę, która się wycofuje, i szuka zrozumienia.
  Wieczór, telefon, często po quizie albo TikToku.
- luka: SERP (Attachment Project, therapist.com, Medical News Today, Psychology Today „telltale
  clues of an avoidant partner", gabinety) daje listę znaków i „yes, it can heal", często
  z tonem oceny wobec „avoidant partnera". **Nikt nie opowiada badań, które pokazują, że
  spokój na zewnątrz to nie brak uczuć**: Dozier i Kobak 1992 (przewodnictwo skóry rosło przy
  pytaniach o odrzucenie, choć słowa były spokojne), Mikulincer, Dolev i Shaver 2004 (pod
  obciążeniem poznawczym tłumienie myśli o rozstaniu przestawało działać). Nasz kąt: unikanie
  to strategia, która kosztuje energię, i dlatego pęka pod zmęczeniem; czułość bez lukru
  wobec osoby unikającej i wobec tej, która ją kocha.
- ⚠ **Duet z `/journal/anxious-attachment-style`** (tekst oparty na newsletterze Moniki #24).
  Ten wpis używa tego samego rytmu (sound familiar, three things in this order, „One thing for
  the people..."), ale NIE powtarza definicji dwóch wymiarów ani Fraleya 2006. Link zamiast.

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** „Do any of these sound familiar?" + trzy scenki, ostatnia krótka
  z mrugnięciem. Haczyki: po naprawdę dobrej randce czujesz ulgę, że wracasz do pustego
  mieszkania; „I'm fine" mówione tak często, że samo się wypowiada; niezależność, którą
  „we consider sexy enough to put in dating profiles" (obraz z §2.1, wolno raz).
- **H2: „Where avoidant attachment comes from:"** (skąd to się bierze)
  - dziecko, którego potrzeby bliskości spotykały się z chłodem albo zniecierpliwieniem,
    uczy się ich nie pokazywać: „if asking doesn't work, stop asking". Ainsworth jednym
    zdaniem (dzieci, które przy powrocie mamy odwracały wzrok), bez szczegółów procedury.
  - strategia ma sens: chroni przed rozczarowaniem. Kosztuje: wymaga ciągłego pilnowania.
  - slot na **„Fun fact:"**: w procedurze Ainsworth dzieci „unikające" wyglądały na
    spokojne, a późniejsze badania fizjologiczne sugerowały, że pod spodem nie były (tylko
    jeśli autor potwierdzi źródło; jeśli nie, slot przechodzi na Dozier i Kobak w badaniach).
  - jedno zdanie: badacze mierzą unikanie jako wymiar, nie szufladę; link do
    `/journal/anxious-attachment-style` („the other half of the picture").
- **H2: „Signs of an avoidant attachment style in adult life:"** (fraza główna w H2)
  - druga osoba, 4-5 punktów: wycofujesz się, gdy relacja robi się poważna; łatwiej ci pomagać
    niż prosić o pomoc (hyper-independence jako fraza poboczna, jednym zdaniem, uczciwie, że
    to nie rozpoznanie); w kłótni wychodzisz z pokoju, zanim temat się skończy; pamiętasz wady
    byłych partnerów lepiej niż to, za czym tęsknisz; potrzebujesz dnia ciszy po weekendzie
    razem.
  - czułość bez lukru, jej zdanie w tym duchu: „None of this makes you cold, or selfish, or
    difficult."
- **H2: „What research turned up:"** (badania)
  - 1992, Dozier i Kobak, *Child Development*: 50 studentów, wywiad o dzieciństwie
    i pomiar przewodnictwa skóry. U osób, które mówiły o dzieciństwie w stylu „deactivating",
    przewodnictwo rosło przy pytaniach o rozłąkę, odrzucenie i zagrożenie. Wniosek: „Calm
    words, busy body."
  - 1992, Simpson, Rholes i Nelligan, *Journal of Personality and Social Psychology*: 83 pary
    w poczekalni przed stresującym zadaniem; kobiety z wyższym unikaniem szukały mniej
    wsparcia u partnera, im bardziej rósł ich lęk. Wniosek: im trudniej, tym mocniej działa
    „I'll handle it".
  - 2004, Mikulincer, Dolev i Shaver, *Journal of Personality and Social Psychology*: osoby
    unikające potrafiły odsunąć myśli o rozstaniu, dopóki nie dostały dodatkowego zadania
    obciążającego pamięć; wtedy myśli wracały, razem z gorszym obrazem siebie. Wniosek:
    strategia działa, dopóki masz na nią siłę. Zmęczenie ją wyłącza.
  - uczciwa granica jej głosem („Avoidance is where the research runs out of answers."):
    badania nad terapią pokazują słabsze i mniej spójne zmiany dla unikania niż dla lęku
    w przywiązaniu (Taylor i wsp. 2015, już opisani w wpisie o anxious; jedno zdanie).
    Chopik i wsp. 2019: unikanie średnio spada z wiekiem. To średnie, nie obietnica.
- **H2: „The work comes down to three things, in this order:"** (co spróbować; jej nagłówek
  z #24 wolno powtórzyć, bo to duet)
  1. Notice the exit before you take it: moment, w którym chcesz wyjść z pokoju, zmienić
     temat, sięgnąć po telefon. Haczyk: nagła, pilna potrzeba zrobienia prania w środku
     rozmowy o uczuciach.
  2. Stay ten percent longer. Nie cała rozmowa, dziesięć procent dłużej niż zwykle. Tu inline
     karta `reflect` (prywatne miejsce, żeby nazwać to, czego nie mówisz na głos).
  3. Say the need in its smallest form. Gotowe zdanie: „I need an hour to myself, and then
     I want to come back to this."
  - H3: „One thing for the people who love someone avoidant" (jak u Moniki): nie goń, nie
    karz ciszą, umawiaj powrót do rozmowy; przestrzeń dana bez kary to też „corrective
    experience". Bez etykietowania partnera czytelnika.
  - link do `/journal/how-to-name-what-you-feel` przy kroku 2.
- **Akapit o apce:** „This is what MindSync's Between-session voice notes are for. Log the
  moment you wanted to leave the room, the message you left unanswered, and what you told
  yourself about why. Give it time, and your Weekly & monthly summaries turn those entries
  into something you can read: [the same exit, showing up in different places]. Then flag the
  one worth unpacking into your Workspace and bring it to your next session."
- **Pytanie do czytelnika:** np. „What's the moment you usually decide you'd rather handle it
  alone?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: What are the signs of avoidant attachment?
  - H3: What causes avoidant attachment?
  - H3: Can avoidant attachment change?
  - H3: How do you love someone with avoidant attachment?
  - H3: Is hyper-independence a trauma response?
  - ⚠ ostatnie pytanie: uczciwie, że hyper-independence nie jest rozpoznaniem; bywa związana
    z trudnymi wczesnymi doświadczeniami, ale nie każda samodzielność ma takie źródło
    i czytelnik nie powinien sam sobie przypisywać traumy. Zero listy objawów traumy.

**4. Karty funkcji** (bramka: voice-notes, reflect, check-ins, mood-trends, personal-bio,
workspace, summaries; używamy czterech)
- inline w „The work comes down to three things" (krok 2):
  `[FEATURE: reflect | A private conversation that asks one gentle follow-up question, for the things you would rather not say to a person yet.]`
- blok przed FAQ:
  `[FEATURES: Seeing the exit before you take it || voice-notes | Thirty seconds after you pulled back, while you still remember what the pull felt like. || summaries | A weekly read of your own entries, where the same retreat stops looking like a coincidence. || workspace | Set aside the moment worth unpacking, so it is waiting when the session starts and not only when you feel ready.]`

**5. Mapa linkowania** (tylko wpisy na żywo)
- `<a href="/journal/anxious-attachment-style">` anchor „the anxious side of the same pattern"
  (sekcja „Where avoidant attachment comes from")
- `<a href="/journal/how-to-name-what-you-feel">` anchor „putting a word on what you would
  rather not feel" (krok 2)
- `<a href="/journal/how-to-stop-people-pleasing">` anchor „the opposite reflex, saying yes
  to everyone" (jedno zdanie przy hyper-independence)
- `<a href="/journal/early-signs-of-burnout">` anchor „handling everything alone until it runs
  out" (przy hyper-independence)
- **Landing partner:** `/pre-order/deep-emotional-analysis` (anchor „what sits under 'I'm
  fine'"), jeden raz. Nie używaj anchorów z partii 3 i 4.

**6. GEO**
- Definicja avoidant attachment, 40-60 słów: wysoki poziom unikania bliskości i zależności,
  opisywany jako wymiar; strategia „deactivating", nie brak uczuć.
- Odpowiedź na „Can avoidant attachment change?", 50-70 słów: Chopik 2019 (spadek z wiekiem,
  średnio) + uczciwie, że dowody z terapii są słabsze niż dla lęku (Taylor 2015).

**7. Hero**
- Wariant „codzienny moment": dwa kubki na stole, jeden bliżej krawędzi, drugi odsunięty,
  miękkie popołudniowe światło; bez osób.
- `hero_image_alt`: „Two mugs on a table set slightly apart in soft afternoon light"
- nazwa pliku hero: `avoidant-attachment-style-hero.webp`

**8. Źródła (zweryfikowane 2026-09-28)**
- **POTWIERDZONE (abstrakt).** Dozier M., Kobak R.R., 1992, *Child Development*
  63(6):1473-1480, „Psychophysiology in attachment interviews: converging evidence for
  deactivating strategies". https://pubmed.ncbi.nlm.nih.gov/1446563/ N = 50 studentów.
- **POTWIERDZONE (abstrakt).** Simpson J.A., Rholes W.S., Nelligan J.S., 1992, *Journal of
  Personality and Social Psychology* 62(3):434-446, „Support seeking and support giving within
  couples in an anxiety-provoking situation: The role of attachment styles".
  https://www.semanticscholar.org/paper/Support-seeking-and-support-giving-within-couples-Simpson-Rholes/bcf583da2efdefa4e196e13fa8593a77f9c8a6af
  83 pary. ⚠ Wynik dla mężczyzn (dawanie wsparcia) podaj tylko po odczycie abstraktu;
  potwierdzony jest wynik dla kobiet (mniej szukania wsparcia przy rosnącym lęku).
- **POTWIERDZONE (abstrakt).** Mikulincer M., Dolev T., Shaver P.R., 2004, *Journal of
  Personality and Social Psychology* 87(6):940-956, „Attachment-related strategies during
  thought suppression: ironic rebounds and vulnerable self-representations".
  https://pubmed.ncbi.nlm.nih.gov/15598116/
- **POTWIERDZONE w partii 4.** Chopik W.J., Edelstein R.S., Grimm K.J., 2019, *JPSP*
  116(4):598-611. https://pubmed.ncbi.nlm.nih.gov/28771022/ (unikanie spada liniowo z wiekiem).
- **POTWIERDZONE jakościowo w partii 4.** Taylor P.J. i wsp., 2015, *Psychotherapy Research*
  25:222-238. https://pubmed.ncbi.nlm.nih.gov/24559454/ ⚠ Zdanie o słabszych dowodach dla
  unikania podaj w brzmieniu autorów po odczycie abstraktu.
- **Czego autor ma NIE twierdzić:**
  - że czytelnik albo jego partner „jest avoidant" (zero „signs your partner is avoidant"),
  - że unikanie wynika z traumy albo zaniedbania u konkretnej osoby,
  - że jest „najtrudniejszy do zmiany" styl jako fakt (to uproszczenie z SERP),
  - że dana terapia (EFT, CBT) „leczy" unikanie,
  - że MindSync zmienia styl przywiązania.

**9. Czego NIE robić**
- Zero quizów, zero „red flags" wobec partnera.
- Fearful avoidant (disorganized) najwyżej jednym zdaniem, bez rozwijania.
- Nie powtarzaj „The radar is real" ani innych puent z #24; to był wpis o lęku.

---

# 05. Benefits of play for adults

**1. Meta**
- `seo_url`: `play-for-adults` | plik: `blog/queue/2026-10-03_play-for-adults.json`
- kategoria: `MindSync Tips` | `kolor`: `#3c67a5` | `planowana_data`: **2026-10-03**
- `tagi`: `["modern-life", "play"]`
- H1: „Who Decided Adults Don't Get to Play? The Benefits of Play for Adults"
- `meta_title` (56 zn.): „Benefits of Play for Adults (and Why We Stop) | MindSync"
- `meta_description` (154 zn.): „Play is not something you grow out of. What research on
  adult playfulness found about stress, why it fades after your first job, and how to get
  some back."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `benefits of play for adults`
- poboczne: `why adults stop playing`, `play for adults`, `how do adults play`, `adult
  playfulness`, `play and stress`, `fun activities for adults to reduce stress`
- ⚠ **nie używaj frazy „adult play"** w tytule, H2 ani slugu: ma w SERP konotację seksualną.
- intencja: ktoś zauważa, że „what do you do for fun" wymaga namysłu, i szuka pozwolenia
  oraz pomysłu. Wieczór, weekend, lekki ton.
- luka: SERP (HelpGuide, UW Health, Psychology Today, The Conversation, blogi sprzętowe)
  daje „play reduces stress" plus listę gier. **Mało kto opowiada badanie z interwencją:**
  Proyer i wsp. 2021 (tydzień zapisywania „three playful things" podniósł dobrostan, efekt do
  12 tygodni) i Clifford i wsp. 2022 (694 dorosłych w pandemii, zabawowość wiązała się
  z lepszym radzeniem sobie). Nasz kąt: zabawa to nie hobby do monetyzacji, tylko sposób
  patrzenia na zwykłą chwilę; i da się ją ćwiczyć jak nawyk myślenia, a nie jak projekt.
- ⚠ **To jest temat newslettera Moniki #17** (pełny tekst w `docs/blog/voice-sample-monika.md`).
  Wpis ROZWIJA #17 do formy bloga (więcej badań, FAQ, fraza), nie przepisuje go. Wolno
  zachować jej tytuł jako H1, strukturę i najwyżej 2-3 jej zdania-obrazki („a phase like loose
  teeth and afternoon naps", „developing genuine feelings about a single orchid",
  „Disclaimer: don't turn fun into a to-do list!"). ⛔ Jej akapit w pierwszej osobie („I have a
  documented habit...") jest prawdą tylko w newsletterze: na blogu NIE używamy go ani jego
  przeróbki (§2.3).

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** obserwacja z #17, nowymi słowami: gdzieś między pierwszą pracą
  a dziś zabawa zniknęła. Haczyki: spotkania ze znajomymi umawiane z miesięcznym
  wyprzedzeniem; odpowiedź „I watch things in the evening" na pytanie o zabawę.
- **H2: „Why do adults stop playing?"** (skąd to się bierze)
  - zabawa wypychana przez rzeczy „ważniejsze"; kultura produktywności każe, żeby hobby było
    „productive, monetizable, or at least improving you in some measurable way" (jej myśl).
  - mechanizm prostym językiem: zabawa przestawia układ nerwowy z trybu niskiego zagrożenia.
    ⚠ Jej zdanie o endorfinach i kortyzolu z #17 idzie tylko jeśli autor znajdzie źródło
    pierwotne; bez źródła pisz jakościowo („play seems to help the body step out of threat
    mode"), bez nazw hormonów.
  - slot na **„Disclaimer:"** z jej #17: „don't turn fun into a to-do list" (jedyna etykieta
    we wpisie).
- **H2: „What play looks like for adults (it's not only board games):"** (jak to wygląda)
  - „I feel like in adulthood, play is less about..." jako opinia jest dozwolona (§2.3), ale
    napisana na nowo.
  - lista w drugiej osobie, 5 punktów, jej rodzaj konkretu: jakaś onieśmielająca aktywność
    fizyczna po trzydziestce (z nawiasem-puentą); rośliny; darmowe wydarzenia w okolicy;
    wolontariat; spacer do sklepu jako mała wyprawa. Nie kopiuj jej listy słowo w słowo.
  - link do `/journal/how-to-stop-doomscrolling` jednym zdaniem: przewijanie wygląda jak
    odpoczynek, ale rzadko jest zabawą.
- **H2: „The benefits of play for adults, according to research:"** (fraza główna w H2;
  badania)
  - 2013, Magnuson i Barnett, *Leisure Sciences*: 898 studentów; bardziej zabawowe osoby
    zgłaszały mniej stresu i częściej wybierały sposoby radzenia sobie nastawione na problem,
    rzadziej ucieczkę. Granica: badanie przekrojowe, młodzi dorośli, związek, nie przyczyna.
  - 2022, Clifford i wsp., *Current Psychology*: 694 dorosłych w pandemii; zabawowość
    wiązała się z większym poczuciem sprawczości i bardziej adaptacyjnym radzeniem sobie
    (to jest badanie „nearly 700 adults" z jej #17, teraz z nazwiskiem i czasopismem).
  - 2021, Proyer, Gander, Brauer i Chick, *Applied Psychology: Health and Well-Being*: 533
    osoby, tydzień prostych ćwiczeń (np. zapisywanie trzech zabawowych rzeczy z dnia) albo
    placebo; ćwiczenia podniosły zabawowość i dobrostan, efekty utrzymywały się do 12
    tygodni. Wniosek: „Playfulness is trainable, and a week is enough to notice." Granica:
    online, samoopis.
- **H2: „How to get some play back without making it a project:"** (co spróbować)
  1. Write down three playful moments from today. Wprost z Proyer 2021, bez oceniania ich
     wielkości. Tu inline karta `voice-notes`.
  2. Pick something you'd be bad at. Haczyk: „the freedom of being the worst person in the
     pottery class".
  3. Add play to something you already do (droga do sklepu, gotowanie).
  4. Protect it from productivity: zero celów, zero liczników, zero „progress". Gotowe
     zdanie do powiedzenia na głos: „I'm not doing this to get better at it. I'm doing it
     because it's fun."
  - link do `/journal/early-signs-of-burnout` przy zdaniu, że brak zabawy bywa jednym
    z pierwszych rzeczy, które znikają przy przeciążeniu.
  - link do `/journal/morning-anxiety` (wstecz do 01) jednym zdaniem przy „a playful first
    ten minutes of the day".
  - puenta, w stylu „Fun that has to justify itself isn't fun yet."
- **Akapit o apce:** „This is what MindSync's Wellbeing check-ins are for. Log your energy and
  stress each evening, and add a quick note on the day you did something just for fun, the
  bouldering session, the orchid, the walk that took the long way. Give it time, and Mood &
  focus-area trends turns those ratings into something you can see: [whether the playful days
  sit higher on the chart]. Then [pick one more of those for next week]." Uwaga: trends
  pokazuje oceny energii i stresu; które dni były „zabawowe", czytelnik widzi, zestawiając
  wykres ze swoimi notatkami. Nie pisz, że apka sama łączy jedno z drugim.
- **Pytanie do czytelnika:** jej zamknięcie z #17 w nowej formie, np. „What did fun look like
  for you at ten, and what's the grown-up version you haven't tried yet?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: Why do adults stop playing?
  - H3: What are the benefits of play for adults?
  - H3: How do adults play?
  - H3: Can play reduce stress?
  - H3: What counts as play for adults?

**4. Karty funkcji** (bramka: check-ins, mood-trends, voice-notes, summaries,
daily-affirmation; używamy czterech)
- inline w „How to get some play back..." (krok 1):
  `[FEATURE: voice-notes | Three playful moments said out loud before bed, which takes less time than deciding what to watch.]`
- blok przed FAQ:
  `[FEATURES: Keeping fun on the radar || check-ins | Energy and stress rated in under a minute, so the evenings after something fun have numbers next to them. || mood-trends | Weeks of those ratings on one chart, where you can check whether the playful days really sit higher. || summaries | A weekly read of your own entries that shows, honestly, whether anything fun made it into the week.]`
- ⚠ zero kart `goals` i `homework`: zabawa nie jest zadaniem (sprzeczne z „Disclaimer").

**5. Mapa linkowania**
- `<a href="/journal/morning-anxiety">` anchor „a lighter first ten minutes" (wstecz do 01,
  publikacja 2026-09-29)
- `<a href="/journal/how-to-stop-doomscrolling">` anchor „the scroll that feels like rest"
  (sekcja „What play looks like for adults")
- `<a href="/journal/early-signs-of-burnout">` anchor „one of the first things burnout takes"
  (część praktyczna)
- `<a href="/journal/digital-burnout-brain-rewiring">` anchor „a brain that never gets offline
  time" (opcjonalnie, jedno zdanie)
- **Landing partner:** brak (track-interventions trzyma 01; nie dubluj w sąsiednich
  wpisach).

**6. GEO**
- Definicja adult playfulness, 40-60 słów: skłonność do przekształcania codziennych sytuacji
  w coś zabawnego, ciekawego albo interesującego (w duchu definicji Proyera; sprawdź
  brzmienie w artykule przed parafrazą).
- Wynik Proyer 2021 w 40-60 słowach, z rokiem, czasopismem i jednym zdaniem wniosku.

**7. Hero**
- Wariant „codzienny moment": doniczka z pojedynczą orchideą na parapecie obok pary
  rękawiczek do wspinaczki albo kredy w woreczku, jasne poranne światło.
- `hero_image_alt`: „A single orchid on a sunny windowsill beside a small chalk bag"
- nazwa pliku hero: `play-for-adults-hero.webp`

**8. Źródła (zweryfikowane 2026-09-28)**
- **POTWIERDZONE (abstrakt).** Magnuson C.D., Barnett L.A., 2013, *Leisure Sciences*
  35(2):129-144, „The playful advantage: How playfulness enhances coping with stress".
  https://www.tandfonline.com/doi/abs/10.1080/01490400.2013.761905 N = 898 studentów.
- **POTWIERDZONE (abstrakt, PubMed 35221637).** Clifford C., Paulk E., Lin Q., Cadwallader J.,
  Lubbers K., Frazier L.D., 2022, *Current Psychology*, „Relationships among adult
  playfulness, stress, and coping during the COVID-19 pandemic".
  https://link.springer.com/article/10.1007/s12144-022-02870-0 N = 694.
- **POTWIERDZONE (abstrakt).** Proyer R.T., Gander F., Brauer K., Chick G., 2021, *Applied
  Psychology: Health and Well-Being* 13(1):129-151, „Can playfulness be stimulated?
  A randomised placebo-controlled online playfulness intervention study on effects on trait
  playfulness, well-being, and depression".
  https://iaap-journals.onlinelibrary.wiley.com/doi/10.1111/aphw.12220 N = 533, tydzień,
  efekty do 12 tygodni. ⚠ Wynik dla objawów depresji podawaj ostrożnie albo wcale (to wpis
  top-of-funnel; „well-being" wystarczy).
- **Czego autor ma NIE twierdzić:**
  - że zabawa leczy depresję albo lęk,
  - endorfiny i kortyzol bez źródła pierwotnego,
  - „adults need X hours of play" (nie ma takiej normy),
  - że MindSync „przypomni ci o zabawie" jako funkcja nawyków (Habit Tracker poza katalogiem).

**9. Czego NIE robić**
- Nie rób z wpisu listy 30 gier planszowych ani poradnika zakupowego.
- Nie wchodź w ekrany dłużej niż jedno zdanie (to wpisy o doomscrollingu i digital burnout).

---

# 06. The same argument over and over

**1. Meta**
- `seo_url`: `same-argument-over-and-over` | plik:
  `blog/queue/2026-10-04_same-argument-over-and-over.json`
- kategoria: `Therapy` | `kolor`: `#339499` | `planowana_data`: **2026-10-04**
- `tagi`: `["understanding-patterns", "relationships"]`
- H1: „It's Never Really About the Dishes: Why You Keep Having the Same Argument Over and Over"
- `meta_title` (50 zn.): „Same Argument Over and Over? Here's Why | MindSync"
- `meta_description` (160 zn.): „Same fight, different dishes. Why couples repeat the same
  argument, what research says about the pursue and withdraw loop, and a 21-minute exercise
  that helped."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `same argument over and over`
- poboczne: `why do we keep having the same fight`, `same fight over and over`, `recurring
  arguments in relationships`, `perpetual problems`, `demand withdraw pattern`, `how to stop
  having the same argument`
- intencja: ktoś właśnie skończył (albo zawiesił) tę samą kłótnię po raz dziesiąty i chce
  zrozumieć, czemu wraca. Najczęściej osoba w związku, czasem o rodzicu albo współlokatorze.
  Wieczór po kłótni.
- luka: SERP (Psychology Today, ReachLink, dziesiątki gabinetów par) mówi „it's not about the
  dishes, it's about unmet needs" i cytuje 69% Gottmana. **Nikt nie daje narzędzia
  sprawdzonego w badaniu z losowaniem:** Finkel i wsp. 2013 (21 minut pisania o konflikcie
  z perspektywy neutralnej osoby trzeciej, trzy razy w roku, zatrzymało spadek jakości
  małżeństwa). Mało kto podaje metaanalizę „pursue and withdraw" (Schrodt i wsp. 2014: 74
  badania). Nasz kąt: kłótnia się powtarza, bo wzorzec jest ważniejszy niż temat, a wzorzec
  najłatwiej zobaczyć z zewnątrz, zapisany.
- ⚠ granica: pursue/withdraw łączy się z przywiązaniem, ale tu jedno zdanie i dwa linki
  (04 avoidant, anxious-attachment-style). Zero metodyki triggerów (link).

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** „Do any of these sound familiar?" + trzy scenki, ostatnia krótka
  z mrugnięciem. Haczyki: kłótnia o zmywarkę, która po 12 minutach jest o tym, kto bardziej
  się stara; możesz wyrecytować obie role z pamięci, łącznie z westchnieniem; ta sama kłótnia,
  tylko tym razem o ręczniki.
- **H2: „Why does the same argument keep coming back?"** (skąd to się bierze)
  - temat to opakowanie; w środku jest potrzeba (uznanie, bezpieczeństwo, autonomia), która
    nie została usłyszana.
  - Gottman Institute: większość konfliktów w parach dotyczy stałych różnic (osobowość,
    styl życia), a nie problemów do rozwiązania raz na zawsze. 69% jako liczba z materiałów
    instytutu (patrz źródła). Wniosek: celem nie jest wygrać, tylko umieć o tym rozmawiać.
  - slot na **„Fun fact:"**: w badaniach nad parami ten sam „perpetual problem" potrafi
    wracać latami, a pary, którym dobrze się wiedzie, i tak go mają; różnią się tym, jak
    o nim rozmawiają (bez liczb, jeśli autor nie potwierdzi).
- **H2: „The same argument over and over, seen from the inside:"** (fraza główna w H2; jak
  to wygląda)
  - druga osoba, 4-5 punktów: jedno naciska, drugie się wycofuje, i każde widzi w tym
    dowód na swoją rację; po 5 minutach nikt nie pamięta, o co poszło; zdanie „you always"
    pada w pierwszej minucie; kłótnia kończy się nie rozwiązaniem, tylko zmęczeniem.
  - link do `/journal/avoidant-attachment-style` (wstecz do 04) i do
    `/journal/anxious-attachment-style` jednym zdaniem: czasem jedno z was goni, a drugie
    ucieka, i oba ruchy mają swoją historię.
  - link do `/journal/how-to-stop-overthinking` (wstecz do 02) jednym zdaniem: odtwarzanie
    kłótni w głowie po fakcie to osobna pętla.
- **H2: „What research turned up:"** (badania)
  - 2014, Schrodt, Witt i Shimkowski, *Communication Monographs*: metaanaliza 74 badań,
    ponad 14 tysięcy osób. Wzorzec „jedno naciska, drugie się wycofuje" wiązał się wyraźnie
    z niższym zadowoleniem ze związku i gorszą komunikacją, bez względu na to, kto naciska.
    Wniosek: „It's not a gender thing. It's a loop thing."
  - 2013, Finkel, Slotter, Luchies, Walton i Gross, *Psychological Science*: 120 par, dwa
    lata. W pierwszym roku jakość małżeństwa spadała u wszystkich. W drugim połowa par trzy
    razy pisała po 7 minut o ostatniej kłótni z perspektywy neutralnej osoby, która chce dobra
    obojga. U nich spadek się zatrzymał. Wniosek: „Twenty-one minutes a year. Less than one
    argument."
  - uczciwa granica: to pary małżeńskie z USA, efekt dotyczył przeżywania konfliktu, nie
    tego, czy kłótnie znikły.
- **H2: „How to stop having the same argument (or at least have a better one):"** (fraza
  poboczna w H2; co spróbować; tryb rozkazujący)
  1. Name the loop, not the person. Gotowe zdanie: „I think we're doing the thing again.
     Can we pause for twenty minutes?"
  2. Write the fight from the outside. Wprost z Finkel 2013: jak opisałaby to życzliwa
     osoba trzecia. Tu inline karta `voice-notes` (powiedz to na głos po kłótni, przeczytaj
     następnego dnia).
  3. Find the need under the topic. „This isn't about the towels. I want to feel like
     I'm not the only one who notices." Link do `/journal/how-to-identify-emotional-triggers`.
  4. Agree on a return time for the conversation, zamiast wychodzić bez słowa albo
     dociskać do skutku. Haczyk: „the 11 p.m. summit that solves nothing".
  - H3: „When it's worth bringing to therapy" (twoja część wzorca to dobry materiał na sesję;
    link do `/journal/how-to-prepare-for-a-therapy-session`). Bez obietnic terapii par.
  - puenta, w stylu „You can't win an argument that keeps changing its topic."
- **Akapit o apce:** „This is what MindSync's Between-session voice notes are for. Log what
  the fight was about on the surface, what it was about underneath, and who moved away
  first. Give it time, and your Therapy timeline turns those entries into something you can
  see: [the same argument in five different outfits]. Then keep it as a thread in your
  Workspace and bring it to your next session." (Tu NIE trends: to notatki.)
- **Pytanie do czytelnika:** np. „If your last argument had a title that wasn't about the
  topic, what would it be?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: Why do we keep having the same argument?
  - H3: Is it normal to have the same fight over and over?
  - H3: What are perpetual problems in a relationship?
  - H3: What is the demand-withdraw pattern?
  - H3: How do you stop the same argument from repeating?

**4. Karty funkcji** (bramka: workspace, timeline, check-ins, voice-notes, reflect,
session-prep; używamy czterech)
- inline w „How to stop having the same argument..." (krok 2):
  `[FEATURE: voice-notes | Tell the fight the way a kind stranger would, right after it ends, and read it again the next morning when you are both calmer.]`
- blok przed FAQ:
  `[FEATURES: Seeing the loop instead of the topic || timeline | Every argument you logged in one line of time, which is where five different topics turn out to be one. || workspace | Keep the recurring one as a thread, so it builds up between sessions instead of starting from zero each time. || reflect | For the evening after, a guided conversation that asks what you needed, not who was right.]`

**5. Mapa linkowania**
- `<a href="/journal/avoidant-attachment-style">` anchor „the partner who needs to leave the
  room" (wstecz do 04, publikacja 2026-10-02)
- `<a href="/journal/how-to-stop-overthinking">` anchor „replaying the fight long after it
  ended" (wstecz do 02, publikacja 2026-09-30)
- `<a href="/journal/anxious-attachment-style">` anchor „the partner who needs to hear it's
  okay"
- `<a href="/journal/how-to-identify-emotional-triggers">` anchor „what sets the argument off
  in the first place" (krok 3)
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` anchor „taking your side of the
  loop into a session" (H3)
- **Landing partner:** `/pre-order/understand-behavioural-patterns` (anchor „the pattern
  underneath the topic"), jeden raz.

**6. GEO**
- Definicja perpetual problems, 40-60 słów, z atrybucją do Gottman Institute i zastrzeżeniem
  „according to the institute's research" (nie „studies show").
- Wynik Finkel 2013 w 50-70 słowach, z liczbą par, czasem ćwiczenia i granicą. Najmocniejszy
  kandydat do cytowania w partii (SERP go nie ma).

**7. Hero**
- Wariant „codzienny moment": dwa ręczniki przewieszone nierówno przez krawędź wanny albo
  suszarkę, miękkie poranne światło; bez osób. Alternatywa: zlew z jednym niedomytym kubkiem.
- `hero_image_alt`: „Two towels hanging unevenly over a drying rack in soft morning light"
- nazwa pliku hero: `same-argument-over-and-over-hero.webp`

**8. Źródła (zweryfikowane 2026-09-28)**
- **POTWIERDZONE (abstrakt, strona wydawcy).** Finkel E.J., Slotter E.B., Luchies L.B.,
  Walton G.M., Gross J.J., 2013, *Psychological Science* 24(8):1595-1601, „A brief
  intervention to promote conflict reappraisal preserves marital quality over time".
  https://journals.sagepub.com/doi/abs/10.1177/0956797612474938 120 par, 21 minut rocznie.
  ⚠ „trzy razy po 7 minut" potwierdź w pełnym tekście (PDF dostępny na stronie Stanford
  SPARQ); jeśli się nie zgadza, pisz tylko „21 minutes over a year".
- **POTWIERDZONE (abstrakt).** Schrodt P., Witt P.L., Shimkowski J.R., 2014, *Communication
  Monographs* 81(1):28-58, „A meta-analytical review of the demand/withdraw pattern of
  interaction and its associations with individual, relational, and communicative outcomes".
  https://www.tandfonline.com/doi/abs/10.1080/03637751.2013.813632 74 badania, N = 14 255,
  r = .36.
- **MATERIAŁ INSTYTUTU, NIE ARTYKUŁ RECENZOWANY.** The Gottman Institute, „Managing Conflict:
  Solvable vs. Perpetual Problems". https://www.gottman.com/blog/managing-conflict-solvable-vs-perpetual-problems/
  69% konfliktów par to „perpetual problems". ⚠ Pisz „according to the Gottman Institute",
  nie „a study found".
- **Czego autor ma NIE twierdzić:**
  - niczego o przemocy, kontroli, groźbach: jeśli autor czuje potrzebę, jedno neutralne
    zdanie „If arguments leave you afraid rather than frustrated, that's a different
    situation, and worth talking to a professional about.",
  - że wzorzec zależy od płci (metaanaliza mówi, że nie),
  - że terapia par jest konieczna albo że MindSync ją zastępuje (apka jest do pracy
    indywidualnej),
  - kto ma rację w przykładach (żadna strona nie jest „winna").

**9. Czego NIE robić**
- Nie diagnozuj partnera czytelnika („your partner is avoidant").
- Nie opisuj stylów przywiązania szerzej niż jedno zdanie (są wpisy 04 i anxious).

---

# 07. When to stop therapy

**1. Meta**
- `seo_url`: `when-to-stop-therapy` | plik: `blog/queue/2026-10-05_when-to-stop-therapy.json`
- kategoria: `Therapy` | `kolor`: `#ff9f8a` | `planowana_data`: **2026-10-05**
- `tagi`: `["getting-more-from-therapy", "ending-therapy"]`
- H1: „Ending Well Is Part of the Work: How to Know When to Stop Therapy"
- `meta_title` (56 zn.): „When to Stop Therapy (and How to End It Well) | MindSync"
- `meta_description` (157 zn.): „Not every ending is a failure. How to know when to stop
  therapy, what research found about endings that were planned, and how to keep what you
  learned after."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `when to stop therapy`
- poboczne: `how to end therapy`, `how do you know when you're ready to stop therapy`,
  `ending therapy`, `graduating from therapy`, `taking a break from therapy`, `how to tell
  your therapist you want to stop`
- intencja: terapia działa albo działała, sesje robią się lżejsze, i pojawia się pytanie
  „czy już?", często z poczuciem winy („czy to nie ucieczka?"). Druga grupa rozważa przerwę
  z powodów życiowych (pieniądze, przeprowadzka).
- luka: SERP (ColumbiaDoctors, Grow Therapy, Two Chairs, Psychology Today, Lyra) daje listę
  znaków gotowości i „talk to your therapist". **Nikt nie opowiada, co badania mówią
  o dobrym zakończeniu:** Knox i wsp. 2011 (dobre zakończenia były planowane i omówione
  z wyprzedzeniem, złe przychodziły nagle po zerwaniu relacji), Norcross i wsp. 2017 (65
  ekspertów z sześciu szkół zgadzało się co do rdzenia: utrwalić postęp, docenić własną
  kompetencję, przygotować „po"). Nasz kąt: koniec terapii to etap pracy, a nie jej brak;
  pozycjonowanie marki („Keep more from every session") pasuje tu dosłownie: chodzi o to,
  żeby zabrać ze sobą to, czego się nauczyłeś.
- ⚠ granice: sygnały postępu → link do `/journal/how-to-know-if-therapy-is-working`; liczba
  sesji → `/journal/how-long-therapy-takes-to-work`; odejście, bo terapeuta nie pasuje,
  i FAQ „Do I have to tell my therapist why I am leaving?" →
  `/journal/what-to-do-when-your-therapist-is-not-the-right-fit`. Tu wyłącznie koniec
  zaplanowany albo przerwa.

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** pytanie o konkretny moment: „Have you ever sat down in a session and
  realized you didn't really have anything to bring?" Haczyki: opowiadasz terapeucie
  o tygodniu jak znajomemu przy kawie; sam rozwiązałeś problem, zanim zdążyłeś go przynieść;
  płacisz za godzinę, w której oboje odrobinę za długo patrzycie w okno.
- **H2: „Why ending feels harder than starting:"** (skąd to się bierze)
  - koniec relacji, która była wyjątkowo bezpieczna, uruchamia stare wzorce rozstań
    (link do `/journal/anxious-attachment-style` jednym zdaniem); poczucie winy, że
    „rezygnujesz"; lęk, że bez sesji wszystko wróci.
  - fragment cytowalny: termination jako normalna, zaplanowana faza terapii (GEO).
  - slot na **„Fun fact:"**: w języku psychoterapii koniec terapii nazywa się „termination",
    co brzmi jak film akcji, a opisuje zwykle spokojną rozmowę o tym, co się udało.
- **H2: „When to stop therapy: the signs you might be ready"** (fraza główna w H2; jak to
  wygląda)
  - druga osoba, 4-5 punktów, bez powtarzania wpisu o postępie: sam stosujesz narzędzia,
    zanim przyjdzie sesja; opowiadasz o problemach w czasie przeszłym; cele, z którymi
    przyszedłeś, są osiągnięte albo przestały być ważne; masz wsparcie poza gabinetem;
    sesje robią się „miłe", ale nie pracujące.
  - link do `/journal/how-to-know-if-therapy-is-working` („the signs of progress, in more
    detail").
  - H3: „When it's a break, not an ending" (pieniądze, przeprowadzka, życie; przerwa też może
    być zaplanowana). Link do `/journal/is-therapy-worth-the-money` jednym zdaniem.
- **H2: „What research turned up:"** (badania)
  - 2011, Knox i wsp., *Psychotherapy Research*: wywiady z 12 klientami. Ci, którzy dobrze
    wspominali zakończenie, mieli silną relację z terapeutą, a zakończenie, plany na potem
    i uczucia z nim związane były omówione z wyprzedzeniem. Trudne zakończenia przychodziły
    nagle, po pęknięciu w relacji. Wniosek: „A good ending is usually a planned one."
    Granica: 12 osób, badanie jakościowe.
  - 2017, Norcross, Zimmerman, Greenberg i Swift, *Psychotherapy*: 65 doświadczonych
    terapeutów z sześciu nurtów oceniało 80 zadań na koniec terapii. Najsilniejsza zgoda:
    wspierać postęp klienta, utrwalić to, co osiągnięte, przygotować rozwój po terapii
    i pomóc klientowi zobaczyć własną kompetencję. Wniosek: dobry koniec to sesje o tym,
    co zabierasz, a nie tylko pożegnanie.
  - opcjonalnie jedno zdanie: 2012, Swift i Greenberg, *Journal of Consulting and Clinical
    Psychology*: około 1 na 5 osób kończy terapię przedwcześnie, zanim uzgodni to
    z terapeutą. Wniosek bez straszenia: rozmowa o końcu to różnica między zniknięciem
    a zakończeniem.
- **H2: „How to end therapy well, in four steps:"** (co spróbować; tryb rozkazujący)
  1. Say it out loud before you're sure. Gotowe zdanie: „I've been wondering if I'm getting
     close to being done. Can we talk about what that would look like?"
  2. Look back before you look forward: przeczytaj, skąd zaczynałeś, zanim zdecydujesz.
     Tu inline karta `goals`.
  3. Taper instead of cliff-edging: rzadsze sesje przez jakiś czas, jeśli terapeuta uzna
     to za sensowne (bez ustalania schematu za czytelnika). Haczyk: „therapy doesn't need a
     dramatic final episode".
  4. Write down your own manual: co działa, jakie są twoje wczesne sygnały ostrzegawcze
     i kiedy wracasz. Link do `/journal/which-coping-skills-actually-work`.
  - jedno zdanie: powrót do terapii po latach to nie porażka, tylko korzystanie z czegoś,
    co już raz zadziałało.
  - link do `/journal/online-vs-in-person-therapy` (wstecz do 03) przy zdaniu, że po
    przeprowadzce przerwa bywa zbędna, bo zmienia się tylko format.
  - puenta, w stylu „The goal of therapy was never more therapy."
- **Akapit o apce:** „This is what MindSync's Therapy timeline is for. Log what you handled
  on your own this month, the tool you reached for without thinking, and the sentence from
  therapy you keep coming back to. Give it time, and your Weekly & monthly summaries turn
  those entries into something you can read: [where you started, and how far that is from
  here]. Then bring the last few months to the session where you talk about ending." To
  jest najmocniejsze miejsce na hasło marki w treści (bez cytowania go dosłownie jako
  sloganu).
- **Pytanie do czytelnika:** np. „What's one thing you'd want to still be doing a year after
  your last session?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: How do you know when you're ready to stop therapy?
  - H3: How do you end therapy with your therapist?
  - H3: Is it OK to take a break from therapy?
  - H3: What happens in the last session of therapy?
  - H3: Can you go back to therapy after ending?
  - ⚠ zero pytania „Do I have to tell my therapist why I'm leaving?" (należy do wpisu
    o dopasowaniu).

**4. Karty funkcji** (bramka: summaries, timeline, goals, mood-trends, health-check;
używamy czterech)
- inline w „How to end therapy well..." (krok 2):
  `[FEATURE: goals | Each goal you set at the start, with the entries that moved it, which is a better basis for deciding than a feeling on a Tuesday.]`
- blok przed FAQ:
  `[FEATURES: Keeping what you learned || summaries | Months of entries turned into a story you can reread after the last session, not just before the next one. || timeline | Every session, note and realization in one line, so the distance you covered is something you can scroll. || health-check | A short look at how the work together feels right now, useful when you cannot tell whether you are done or just stuck.]`

**5. Mapa linkowania**
- `<a href="/journal/online-vs-in-person-therapy">` anchor „switching the format instead of
  stopping" (wstecz do 03, publikacja 2026-10-01)
- `<a href="/journal/how-to-know-if-therapy-is-working">` anchor „the signs of progress, in
  more detail" (sekcja ze znakami)
- `<a href="/journal/how-long-therapy-takes-to-work">` anchor „how many sessions change
  usually takes" (sekcja „Why ending feels harder than starting", jedno zdanie)
- `<a href="/journal/what-to-do-when-your-therapist-is-not-the-right-fit">` anchor „leaving
  because the fit is wrong" (jedno zdanie granicy)
- `<a href="/journal/which-coping-skills-actually-work">` anchor „the skills that worked for
  you" (krok 4)
- `<a href="/journal/anxious-attachment-style">` anchor „old goodbyes" (opcjonalnie)
- **Landing partner:** `/pre-order/tracking-therapy-effectiveness` (anchor „a clear record of
  how far therapy took you"), jeden raz. To jest duet z pillarem klastra 1.

**6. GEO**
- Definicja termination w psychoterapii, 40-60 słów: zaplanowana, omówiona faza końcowa
  terapii, w której utrwala się postęp i przygotowuje czas po terapii.
- Odpowiedź na „How do you know when you're ready to stop therapy?", 50-70 słów, z 3 znakami
  i Knox 2011 (zakończenie omówione z wyprzedzeniem).

**7. Hero**
- Wariant „codzienny moment": zamknięty notatnik z tasiemką na stoliku przy oknie, obok
  długopis i kubek, złota godzina; bez osoby.
- `hero_image_alt`: „A closed notebook with a ribbon marker beside a mug on a table at
  golden hour"
- nazwa pliku hero: `when-to-stop-therapy-hero.webp`

**8. Źródła (zweryfikowane 2026-09-28)**
- **POTWIERDZONE (abstrakt).** Knox S., Adrians N., Everson E., Hess S., Hill C.,
  Crook-Lyon R., 2011, *Psychotherapy Research* 21(2):154-167, „Clients' perspectives on
  therapy termination". https://pubmed.ncbi.nlm.nih.gov/21229469/ N = 12, badanie
  jakościowe (CQR).
- **POTWIERDZONE (abstrakt).** Norcross J.C., Zimmerman B.E., Greenberg R.P., Swift J.K.,
  2017, *Psychotherapy* 54(1):66-75, „Do all therapists do that when saying goodbye? A study
  of commonalities in termination behaviors".
  https://www.researchgate.net/publication/314269329_Do_all_therapists_do_that_when_saying_goodbye_A_study_of_commonalities_in_termination_behaviors
  65 ekspertów, 80 zadań, 51 z pozytywnym konsensusem.
- **POTWIERDZONE (abstrakt, opcjonalne).** Swift J.K., Greenberg R.P., 2012, *Journal of
  Consulting and Clinical Psychology* 80(4):547-559, „Premature discontinuation in adult
  psychotherapy: a meta-analysis". https://pubmed.ncbi.nlm.nih.gov/22506792/ 669 badań,
  N = 83 834, dropout 19.7%. ⚠ Strony potwierdź przed cytatem; w tekście wystarczy „about
  one in five".
- **Czego autor ma NIE twierdzić:**
  - że czytelnik jest gotowy (to decyzja z terapeutą),
  - niczego o odstawianiu leków razem z końcem terapii (osobna decyzja z lekarzem;
    najlepiej w ogóle nie poruszać),
  - że koniec terapii to „sukces", a przerwanie „porażka" (obie ścieżki bez oceny),
  - że MindSync zastępuje terapię po jej zakończeniu. Apka pomaga zachować to, co
    wypracowane, i zauważyć, kiedy warto wrócić.

**9. Czego NIE robić**
- Nie powtarzaj list sygnałów postępu ani liczby sesji z wpisów 2026-08 i 2026-09 (linki).
- Zero sugestii, że terapię „warto skończyć, bo jest droga"; koszty tylko jednym zdaniem
  i linkiem.

---

## Rezerwy (bez briefów, bramka w `_preflight-partia5.json`)

- **08 KLASTER5: loneliness in adulthood** (`loneliness-in-adulthood`). Kąt: samotność to nie
  liczba znajomych, tylko brak bliskości; strukturalne przyczyny (brak przypadkowych,
  powtarzalnych spotkań). Karty: reflect, voice-notes, check-ins. ⚠ Uważaj na granicę
  z kryzysem: zero treści o izolacji skrajnej.
- **09 KLASTER5: imposter syndrome** (`imposter-syndrome`). Kąt: dowody sukcesu „nie liczą
  się", bo przypisujemy je szczęściu; zapisywanie dowodów w czasie. Karty: timeline,
  workspace, goals. ⚠ Zero liczby „70% people" bez źródła pierwotnego (krąży bez atrybucji).
