# Partia 3: briefy wpisów (3 pozycje, drip 2026-09-21..2026-09-23)

> Data: 2026-09-21. Autor briefów: `seo-content-writer`. Wykonawca prozy: `blog-writer`
> (+ `humanizer`, akcept `brand-voice-manager`, schema od `seo-tech-lead`, hero od
> `graphic-designer`). **Treść po ANGIELSKU.** Format pliku kolejki: `blog/queue/_format.md`.
> Głos marki i zakazy: `docs/blog/brand-mindsync.md`.
>
> **Status bramki KROK 0:** `blog/queue/_preflight-partia3.json`, wynik **6x OK, 0 RYZYKO,
> 0 BRAK** na sześciu kandydatach. Do realizacji weszła trójka 01, 02, 03. Kandydaci 04
> (morning anxiety), 05 (restart check-in habit), 06 (the same argument) zostają w pliku
> bramki jako materiał na partię 4, bez briefów.
>
> **Status danych:** GSC właściwości mindsync.app działa, ale blog ma zerowy ruch (baseline
> 2026-09-15: 5 z 15 wpisów zaindeksowanych, 0 kliknięć), więc **nie ma własnych danych
> o popycie na te tematy**. Frazy główne i poboczne pochodzą z researchu SERP, bez wolumenów
> i bez KD. Pytania FAQ są przepisane z realnych brzmień zapytań widocznych w wynikach
> i w tytułach konkurencji, nie parafrazowane. Po pierwszych wyświetleniach w GSC:
> `scripts/gsc/blog-partia-frazy.py` i korekta H2 oraz FAQ na frazy z liczbami.
>
> **Luka w katalogu funkcji (zgłoszona operatorowi, nie blokuje partii):** `app-features.json`
> nie zna Habit Trackera (w apce od 2026-09-02) ani ekranu wyboru trybu w Reflect (od
> 2026-09-18). Żaden brief w tej partii nie opiera karty na tych funkcjach.

## Zasady wspólne dla wszystkich 3 briefów (nie powtarzam ich w każdym)

1. **Zakaz obu myślników.** Zero em-dash (U+2014) i zero półpauzy (U+2013) w tytule, meta,
   zajawce i treści, także jako wtrącenie czy separator. Przebudowuj zdanie: przecinek,
   dwukropek, nawias albo dwa zdania. Zakres liczbowy zwykłym łącznikiem: „13-18 sessions".
   ⚠ Bramka dripu wyłapuje tylko U+2014, więc półpauzę musisz sprawdzić sam, wyszukiwarką
   po znaku, przed oddaniem pliku.
2. **YMYL:** zero diagnozowania, zero interpretowania objawów czytelnika, zero obietnic
   zdrowotnych, zero zniechęcania do terapii i leków, zero tematów kryzysowych i numerów
   pomocowych. MindSync uzupełnia terapię, nie zastępuje. Wpis 01 jest w tej partii
   najostrożniejszy i ma dodatkowe reguły w swoim briefie.
3. **Funkcje `planned` nie istnieją w treści:** `therapist-sharing` (portal ukryty, MSV3.4
   CS-11) i `streaks` (brak UI). Zero sugestii wysyłania czegokolwiek terapeucie z apki
   i zero odznak ani serii za wytrwałość.
4. **Zero cen MindSync w treści** (od cennika jest `/membership`). Zero wymyślonych zrzutów
   ekranu i nazw przycisków. Nazwa ekranu bez pokrycia w `blog/app-features.json` = znacznik
   `[VERIFY-UI: ...]`.
5. **Karty:** 2-3 na wpis (1-2 `[FEATURE:]` inline + jeden blok `[FEATURES:]` z trzema
   pozycjami przed FAQ). Tylko id potwierdzone bramką dla danego wpisu, lista w sekcji 4
   każdego briefu. Powód w karcie to jedno zdanie prozą po angielsku. **Żadne id nie
   powtarza się w obrębie jednego wpisu** (inline i blok się nie dublują).
6. **Zdania w kartach mają być nowe.** Partia 1 i 2 już używają sformułowań w rodzaju „The
   prep card pulls your week into one screen" i „What you came for, written down, with
   evidence collecting underneath it". Nie przepisuj ich. Ten sam sens, inne zdanie.
7. **FAQ:** nagłówek H2 dokładnie `Frequently asked questions`, pytania w H3, 4-5 sztuk,
   w brzmieniu realnego zapytania (dokładnie tak, jak podano w briefie, bez wygładzania).
   Odpowiedź 40-70 słów, pierwsze zdanie to pełna odpowiedź (GEO), reszta to warunek albo
   zastrzeżenie.
8. **Badania:** każda liczba ma nazwisko, rok i czasopismo. Autor **weryfikuje źródło
   pierwotne** (abstrakt albo pełny tekst) przed użyciem liczby. Jeśli nie da się potwierdzić
   autorów, roku i liczby, twierdzenie wypada albo idzie w wersji jakościowej, bez liczby.
   Linkujemy do publikacji albo do rekordu PubMed/PMC, nigdy do wtórnych blogów i do
   streszczeń z wyszukiwarki. Obserwacje praktyków oznaczamy w zdaniu jako obserwacje
   praktyków, nie jako badanie.
9. **Struktura:** lead 40-60 słów (scena z życia, nie definicja), sekcje merytoryczne
   z badaniami, sekcja praktyczna, karty, FAQ. Bez sekcji „Conclusion" i bez waty.
   **Długość: 1600-2000 słów** (wyjątek: wpis 02 może mieć 1800-2200, bo jest gęsty od danych).
10. **Linki wewnętrzne wyłącznie ścieżkami względnymi:** `<a href="/journal/slug">`,
    `<a href="/features">`, `<a href="/pre-order/...">`. **Nigdy `https://mindsync.app/...`**
    ani `https://www.mindsync.app/...` w treści: kanoniczny host to `www`, więc link
    bezwzględny na goły host generuje przekierowanie 301 i traci moc linku.
11. **W tej partii nie ma ani jednego `[LINK-LATER:]`.** Kolejność dat jest tak ułożona, że
    wszystkie linki wewnątrz partii biegną wstecz, do wpisów już opublikowanych. Jedyny
    warunek: wpis 01 musi faktycznie wyjść 2026-09-21. Jeśli jego publikacja się opóźni,
    zamień w 02 i 03 link `<a href="/journal/therapy-hangover">` na
    `[LINK-LATER: therapy-hangover | <ten sam anchor>]` i zgłoś to liderowi.
12. **Slug wpisu** = pole `seo_url`; URL publiczny to `/journal/<slug>`. Nazwa pliku
    w kolejce jest narzucona przez lidera i musi się zgadzać ze slugiem.

## Kolejność publikacji, daty i topologia linkowania

| data | # | plik w kolejce | slug (`seo_url`) | klaster | kategoria | `kolor` | rola |
|---|---|---|---|---|---|---|---|
| 2026-09-21 | 01 | `2026-09-21_therapy-hangover.json` | `therapy-hangover` | 2 | Therapy | `#1f3d38` | wejście partii, cel linków 02 i 03 |
| 2026-09-22 | 02 | `2026-09-22_how-long-therapy-takes-to-work.json` | `how-long-therapy-takes-to-work` | 6 | Therapy | `#e8af0a` | wpis danych, duet landingu |
| 2026-09-23 | 03 | `2026-09-23_how-to-name-what-you-feel.json` | `how-to-name-what-you-feel` | 3 | MindSync Tips | `#ff9f8a` | zamyka partię |

⚠ Wpis 01 jest publikowany **ręcznie** 2026-09-21 (kolejka stała od 2026-09-18), więc
publikacja idzie przez `scripts/webflow/blog-publish.ps1 -DripOne` z jawną zgodą operatora,
a nie z Task Schedulera.

Wpisy już na żywo, do których linkujemy normalnym `<a href>` (20 sztuk):
`are-mental-health-apps-private`, `digital-burnout-brain-rewiring`, `how-to-choose-a-therapist`,
`how-to-do-therapy-homework`, `how-to-identify-emotional-triggers`,
`how-to-know-if-therapy-is-working`, `how-to-prepare-for-a-therapy-session`,
`how-to-remember-what-you-talk-about-in-therapy`, `how-to-stop-doomscrolling`,
`how-to-use-mindsync`, `is-therapy-worth-the-money`, `journaling-vs-voice-notes`,
`racing-thoughts-at-night`, `regulate-nervous-system-between-therapy-sessions`,
`sunday-scaries`, `tracking-mood-on-antidepressants`, `what-to-do-between-therapy-sessions`,
`what-to-do-when-your-therapist-is-not-the-right-fit`, `which-coping-skills-actually-work`,
`why-mood-tracking-stops-working`.

**Dług linkowania do odrobienia po partii (zadanie dla `webflow-publisher`, nie dla autora):**
po 2026-09-23 warto dopiąć PATCH-em dwa linki w druga stronę, z `how-to-know-if-therapy-is-working`
do `how-long-therapy-takes-to-work` i z `how-to-identify-emotional-triggers` do
`how-to-name-what-you-feel`. To nie jest dług wygenerowany przez tę partię, tylko wzmocnienie.
Osobno wciąż czeka 10 pozycji z partii 1 i 2 w `blog/queue/_link-fixup.md`.

---

# 01. Why you feel worse after a therapy session (the therapy hangover)

**1. Meta**
- `seo_url`: `therapy-hangover` | plik: `blog/queue/2026-09-21_therapy-hangover.json`
- kategoria: `Therapy` | `kolor`: `#1f3d38` | `planowana_data`: **2026-09-21**
- `tagi`: `["between-sessions", "after-session"]`
- H1: „Why You Feel Worse After a Therapy Session (the Therapy Hangover)"
- `meta_title` (43 zn.): „Why You Feel Worse After Therapy | MindSync"
- `meta_description` (155 zn.): „Drained or foggy after a session? What research says about
  feeling worse after therapy, how long the dip usually lasts, and what to do with the hours
  after."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `why do I feel worse after therapy`
- poboczne: `therapy hangover`, `is it normal to feel worse after therapy`, `how long does
  a therapy hangover last`, `why am I so tired after therapy`, `emotional hangover after
  therapy`, `crying after therapy sessions`, `drained after therapy`
- intencja: doraźna, tego samego wieczoru, w dużej części na telefonie. Człowiek chce trzech
  rzeczy w tej kolejności: czy to normalne, czy to znaczy, że terapia nie działa, i co teraz
  zrobić z tym wieczorem. Krótkie akapity, skanowalne nagłówki, odpowiedź w pierwszych
  dwóch ekranach.
- luka: SERP to GoodRx, blogi gabinetów (Cityscape, Space Between, Liberation Healing)
  i treści masowe (neurolaunch). Wszyscy powtarzają jedno zdanie: „to normalne, to znaczy,
  że pracujesz", i zwykle dorzucają radę o kąpieli i herbacie. **Nikt nie rozdziela trzech
  różnych rzeczy, które ludzie nazywają tym samym słowem**, i prawie nikt nie podaje badań.
  Nasz kąt: zmęczenie po godzinie skupionej pracy emocjonalnej, przejściowe nasilenie po
  trudnym temacie i zgrzyt w relacji z terapeutą to trzy osobne sytuacje, każda ma inną
  odpowiedź. Druga część kąta: uczciwość. Nie piszemy, że gorzej zawsze znaczy lepiej.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): w samochodzie było w porządku, a o siódmej wieczorem nie masz siły
  odpisać na wiadomość i płaczesz nad zmywarką.
- H2: „Therapy hangover" is a nickname, not a diagnosis
  - jedno miejsce, gdzie stawiamy sprawę jasno: nie ma tego w żadnej klasyfikacji, nie ma
    badań nad „therapy hangover" jako zjawiskiem, są badania nad rzeczami sąsiednimi.
    To jest fragment cytowalny, 40-60 słów, napisz go tak, żeby działał wyjęty z kontekstu.
- H2: Three different things people call the same thing
  - H3: Plain tiredness after an hour of concentrated work
  - H3: A temporary rise in what you came in with
  - H3: Something that happened between you and your therapist
  - każdy podpunkt kończy jedno zdanie „what this one usually asks of you"
- H2: What the research actually shows
  - Foa i wsp. 2002: przejściowe nasilenie u mniejszości uczestników, bez związku z gorszym
    wynikiem i bez związku z porzuceniem terapii; obowiązkowe zastrzeżenie o kontekście
  - Crawford i wsp. 2016: około jedna osoba na dwadzieścia w dużej ankiecie NHS zgłosiła
    trwałe złe efekty; to jest druga strona i powód, dla którego nie sprzedajemy pocieszenia
  - Eubanks i wsp. 2018: jedno zdanie o naprawie zerwania w relacji, z linkiem
- H2: How long it usually lasts
  - uczciwie: nie ma danych o rozkładzie czasu trwania, więc opisujemy jakościowo
    i oznaczamy jako obserwacje praktyków, nie jako wynik badania
  - H3: What tends to stretch it out (jazda prosto na spotkanie, wieczór na telefonie,
    domykanie sprawy alkoholem, rozmowa o sesji z osobą, której dotyczyła)
- H2: The hour after the session
  - sekcja praktyczna: dziesięć minut zanim wrócisz do świata, jedno zdanie zapisane albo
    nagrane, coś fizycznego i powolnego, żadnych decyzji dzisiaj
  - karta `session-debrief`
- H2: The next day is where the useful part is
  - to, co wygląda na kaca, bywa materiałem na następną sesję; jedno pytanie do zapisania
    rano; ostrzeżenie przed oceną całej terapii po jednym czwartku
  - karta `check-ins`
- H2: When the dip is worth raising with your therapist
  - neutralnie i bez straszenia: gdy nie mija przez kilka sesji z rzędu, gdy narasta, gdy
    zaczynasz przekładać sesje, gdy dotyczy samej relacji. Kierunek zawsze ten sam: powiedz
    to na sesji, to jest normalna część pracy, nie skarga.
- blok `[FEATURES:]`
- H2: Frequently asked questions
  - H3: Is it normal to feel worse after therapy?
  - H3: How long does a therapy hangover last?
  - H3: Why am I so tired after therapy?
  - H3: Does feeling worse after therapy mean it is working?
  - H3: Should I tell my therapist that I feel worse after sessions?

**4. Karty funkcji** (bramka potwierdziła: session-debrief, voice-notes, check-ins,
mood-trends, timeline)
- inline w „The hour after the session":
  `[FEATURE: session-debrief | Five minutes while it is still warm, so the hour you just paid for does not dissolve somewhere on the way home.]`
- inline w „The next day is where the useful part is":
  `[FEATURE: check-ins | Rating the day after a session takes under a minute, and it is how you find out whether the dip lasts an evening or a week.]`
- blok przed FAQ:
  `[FEATURES: Making the day after a session usable || voice-notes | Say it out loud on the evenings when typing is too much, and read it back when it is not. || mood-trends | The days after your sessions, sitting next to the rest of your weeks instead of standing in for them. || timeline | Sessions, notes and check-ins in one place, so a hard month is something you can look at rather than something you have to remember.]`

**5. Mapa linkowania** (wszystko wstecz, zero `[LINK-LATER:]`)
- `<a href="/journal/how-to-know-if-therapy-is-working">` anchor „whether therapy is actually
  working" (w sekcji „The next day", przy zdaniu, że jeden zły wieczór nie jest werdyktem)
- `<a href="/journal/regulate-nervous-system-between-therapy-sessions">` anchor „settle your
  body before you go back to the day" (sekcja „The hour after the session")
- `<a href="/journal/how-to-remember-what-you-talk-about-in-therapy">` anchor „keep what the
  session gave you"
- `<a href="/journal/what-to-do-when-your-therapist-is-not-the-right-fit">` anchor „when it is
  the relationship and not the topic" (sekcja o zgrzycie z terapeutą)
- **Landing partner:** `/features` (anchor „the after-session debrief"), jeden raz.

**6. GEO (fragmenty cytowalne)**
- Definicja „therapy hangover", 40-60 słów: co to znaczy potocznie, że nie jest rozpoznaniem,
  i trzy najczęstsze mechanizmy w jednym zdaniu każdy. To jest fragment z największą szansą
  na cytowanie, bo w SERP nikt nie stawia granicy między nazwą potoczną a rozpoznaniem.
- Odpowiedź na `is it normal to feel worse after therapy`, 55-75 słów, z uczciwym „czasem to
  zwykłe zmęczenie po pracy, czasem sygnał do rozmowy, i te dwie rzeczy rozróżnia się po tym,
  czy mija".

**7. Hero**
- Wariant „codzienny moment" (`scripts/image-gen/prompts-blog-mindsync/hero-01-codzienny-moment.md`):
  kubek i odwrócony ekranem w dół telefon na parapecie, koc zsunięty z boku, późne
  popołudniowe światło, bez osoby w kadrze.
- `hero_image_alt`: „A mug and a face down phone on a windowsill in late afternoon light".

**8. Źródła**
- **POTWIERDZONE.** Foa, Zoellner, Feeny, Hembree, Alvarez-Conrad, 2002, *Journal of
  Consulting and Clinical Psychology*, „Does imaginal exposure exacerbate PTSD symptoms?"
  (PubMed 12182265). Wynik: w próbie 76 osób przejściowe nasilenie objawów wystąpiło
  u mniejszości uczestników, osoby te korzystały z terapii porównywalnie, a nasilenie nie
  wiązało się ani z gorszym wynikiem, ani z porzuceniem terapii. ⚠ Zweryfikuj dokładny
  przedział procentowy w abstrakcie (w omówieniach krąży 9-21% zależnie od miary) i podaj go
  tylko wtedy, gdy się zgadza. **Zastrzeżenie obowiązkowe w zdaniu:** to była terapia
  ekspozycyjna w PTSD, a nie zwykła rozmowa, więc nie uogólniaj na każdą sesję.
- **POTWIERDZONE.** Crawford i wsp., 2016, *The British Journal of Psychiatry*, „Patient
  experience of negative effects of psychological treatment: results of a national survey".
  Wynik: około 5%, czyli mniej więcej jedna osoba na dwadzieścia, zgłosiło trwałe złe efekty
  leczenia psychologicznego. ⚠ Wielkość próby podawana jest w omówieniach jako „około
  15 000"; zweryfikuj ją w abstrakcie, a jeśli nie potwierdzisz, napisz „a large national NHS
  survey" bez liczby uczestników.
- **POTWIERDZONE jako pozycja, liczby do sprawdzenia.** Eubanks, Muran, Safran, 2018,
  *Psychotherapy*, metaanaliza naprawy zerwań przymierza. Tu wystarczy jedno zdanie
  jakościowe plus link wewnętrzny; nie podawaj wielkości efektu, bo to nie jest temat wpisu.
- **Czego autor ma NIE twierdzić:**
  - że „therapy hangover" ma udokumentowany czas trwania (nie ma takich danych),
  - że gorsze samopoczucie po sesji jest dowodem postępu (to jest dokładnie ta teza
    z SERP-u, której nie powtarzamy),
  - żadnej neurobiologii jako wyjaśnienia: zero kortyzolu, zero „aktywacji sieci mózgowych",
    zero zużycia glukozy, nawet gdy inne artykuły to podają,
  - że sesja „otwiera rany", które trzeba „zamknąć" (to metafora, nie mechanizm),
  - żadnych liczb z ankiet firm komercyjnych.

**9. Czego NIE robić**
- Zero diagnozowania i zero interpretowania stanu czytelnika. Nie nazywamy tego objawem,
  nie sugerujemy, że to depresja, wypalenie ani reakcja traumatyczna.
- Zero treści kryzysowych, zero numerów pomocowych, zero opisów nasilenia, które miałyby
  czytelnika przestraszyć. Sekcja „When the dip is worth raising" ma być spokojna
  i kierować do terapeuty, nigdzie indziej.
- Nie namawiaj do przerwania ani do kontynuowania terapii.
- Nie obiecuj, że apka skróci albo złagodzi kaca po sesji. Apka daje miejsce na to, co
  zostało po sesji, i obraz kolejnych dni. Tyle i tylko tyle.
- Nie dubluj `/journal/how-to-remember-what-you-talk-about-in-therapy`: tam chodzi o zapis
  treści sesji, tu o stan po niej. Jeden akapit i link.
- Nie wchodź w metodykę pomiaru postępu, od tego jest `/journal/how-to-know-if-therapy-is-working`.

---

# 02. How long therapy takes to work

**1. Meta**
- `seo_url`: `how-long-therapy-takes-to-work` | plik:
  `blog/queue/2026-09-22_how-long-therapy-takes-to-work.json`
- kategoria: `Therapy` | `kolor`: `#e8af0a` | `planowana_data`: **2026-09-22**
- `tagi`: `["measurement", "therapy-progress"]`
- H1: „How Long Therapy Takes to Work, According to the Session Numbers"
- `meta_title` (46 zn.): „How Long Does Therapy Take to Work? | MindSync"
- `meta_description` (158 zn.): „The research on how many therapy sessions it takes: what the
  dose-response curve shows, why real clinic numbers look different, and how to judge your
  own pace."
- długość: **1800-2200 słów** (jedyny wpis w partii z takim limitem, bo niesie cztery źródła)

**2. Frazy i intencja**
- główna: `how long does therapy take to work`
- poboczne: `how many therapy sessions do I need`, `how long should I be in therapy`, `when
  will therapy start working`, `how many sessions before therapy helps`, `is 6 sessions
  enough`, `how long does therapy last on average`
- intencja: niecierpliwość plus rachunek sumienia, najczęściej między trzecią a dziesiątą
  sesją. „Chodzę od dwóch miesięcy, wydałem konkretne pieniądze i nie wiem, czy to normalne,
  że jeszcze nic". Druga, mniejsza grupa: osoba przed startem, planująca czas.
- luka: SERP to strony praktyk i platform terapeutycznych, które odpowiadają „to zależy",
  plus kilka tekstów cytujących krzywą Howarda bez jednego zastrzeżenia. **Nikt nie zestawia
  liczby z badań z liczbą z rzeczywistych gabinetów.** To jest cały nasz kąt: klasyczna
  krzywa mówi, że około połowa osób ma mierzalną poprawę w okolicach ósmej sesji, a dane
  z praktyki pokazują, że przeciętny pacjent nie dochodzi nawet do piątej. Z tego zestawienia
  wynika jedyna uczciwa rada, jakiej ten SERP nie daje: krzywa opisuje rozkład, nie twój
  harmonogram, więc jedyne, co masz, to własny pomiar.
- ⚠ **kolizja frazowa do pilnowania:** `how many therapy sessions do I need` jest już pytaniem
  FAQ w opublikowanym `/journal/is-therapy-worth-the-money`. Tutaj ta fraza jest rdzeniem
  wpisu, więc 02 ją przejmuje i rozwija, a do tamtego wpisu linkuje w kontekście kosztu.
  Nie powtarzaj tamtej odpowiedzi słowo w słowo, napisz pełniejszą.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): ósma sesja, osiem przelewów, i nadal nie umiesz powiedzieć, czy
  cokolwiek się ruszyło, poza tym, że chodzisz.
- H2: The number everyone quotes, and where it comes from
  - Howard i wsp. 1986, krzywa dawka-efekt: około połowa pacjentów z mierzalną poprawą
    w okolicach ósmej sesji, około trzy czwarte po dwudziestu sześciu. Od razu kontekst:
    to reanaliza danych z wielu wcześniejszych badań, poprawa była oceniana inaczej niż
    ocenia się ją dzisiaj, i nie jest to recepta na liczbę wizyt.
- H2: What the curve actually says, and what it does not
  - H3: Most of the movement happens early (kształt krzywoliniowy, malejące przyrosty)
  - H3: It is a distribution, not a schedule (połowa osób to nie znaczy ty w ósmym tygodniu)
  - H3: „Improvement" meant different things in different studies
- H2: The number from real clinics looks different
  - Hansen, Lambert i Forman 2002: w danych z praktyki przeciętna liczba odbytych sesji jest
    jednocyfrowa i niska, a odsetek osób z poprawą znacznie niższy niż w badaniach; do tego
    szacunek, ile sesji potrzeba, żeby połowa pacjentów osiągnęła klinicznie istotną zmianę.
    To jest najważniejsze zestawienie całego wpisu, daj mu osobny akapit i prostą arytmetykę.
- H2: What newer reviews found
  - Robinson, Delgadillo i Kellett 2020: przegląd badań z rutynowej praktyki, powtarzalne
    wsparcie dla zależności krzywoliniowej, z wyjątkami, które trzeba wymienić uczciwie.
  - jeden akapit o modelu „good enough level", jakościowo i bez liczb: ludzie zostają
    w terapii tak długo, jak im to jest potrzebne, więc porównywanie się z kimś po liczbie
    sesji jest z założenia mylące.
- H2: What moves your own timeline
  - H3: What you came in with (jedno konkretne wydarzenie kontra wzorzec ciągnący się latami)
    bez diagnozowania i bez przypisywania czytelnikowi czegokolwiek
  - H3: Frequency, and what gaps do to the thread
  - H3: What happens between the sessions (jeden akapit, reszta przez link)
  - H3: Fit with the therapist (jeden akapit, reszta przez linki)
- H2: How to tell whether your own therapy is moving
  - sekcja praktyczna i najważniejsza dla konwersji: mierz to samo, w tym samym rytmie,
    porównuj miesiące, nie czwartki; trzy markery; wyraźne odesłanie do wpisu o metodyce
    zamiast powtarzania jej
  - karty `mood-trends` i `summaries`
- H2: When it is fair to ask about the plan
  - spokojnie i bez namawiania do odejścia: po jakim czasie normalne jest zapytać „jaki mamy
    plan i po czym poznamy, że działa", i że dobry terapeuta traktuje to jako część pracy
- blok `[FEATURES:]`
- H2: Frequently asked questions
  - H3: How long does therapy take to work?
  - H3: How many therapy sessions do I need?
  - H3: Is it normal to feel no change after 6 sessions?
  - H3: How long should you stay in therapy?
  - H3: Why does therapy take so long?

**4. Karty funkcji** (bramka potwierdziła: mood-trends, summaries, timeline, health-check,
goals)
- inline w „How to tell whether your own therapy is moving":
  `[FEATURE: mood-trends | The areas you are working on, charted across weeks, so the question stops depending on how last Thursday happened to go.]`
- inline tamże, przy akapicie o porównywaniu miesięcy:
  `[FEATURE: summaries | Month by month in your own words, so a slow stretch is something you can read back instead of something you have to trust your memory about.]`
- blok przed FAQ:
  `[FEATURES: Judging the pace with something other than patience || goals | The reason you started, written down once, with evidence gathering underneath it. || timeline | Every session and note on one line you can scroll back through when a month feels like nothing happened. || health-check | A regular read on the working relationship, which is one of the few things known to move the timeline.]`

**5. Mapa linkowania** (wszystko wstecz, zero `[LINK-LATER:]`)
- `<a href="/journal/how-to-know-if-therapy-is-working">` anchor „how to tell whether therapy
  is working" (sekcja praktyczna, zamiast dublowania metodyki)
- `<a href="/journal/is-therapy-worth-the-money">` anchor „what a course of therapy costs"
  (sekcja o arytmetyce liczby sesji)
- `<a href="/journal/therapy-hangover">` anchor „a session that leaves you wrung out"
  (opublikowany 2026-09-21, normalny link)
- `<a href="/journal/what-to-do-between-therapy-sessions">` anchor „what you do between
  sessions" (H3 o pracy między sesjami)
- `<a href="/journal/what-to-do-when-your-therapist-is-not-the-right-fit">` anchor „when the
  fit is the thing holding it up" (H3 o dopasowaniu)
- **Landing partner:** `/pre-order/tracking-therapy-effectiveness` (anchor „tracking whether
  therapy is working over time"), jeden raz, naturalnie w zdaniu.

**6. GEO**
- Odpowiedź na `how long does therapy take to work`, 60-80 słów, z dwiema liczbami i jednym
  zastrzeżeniem: co pokazuje klasyczna krzywa, co pokazują dane z gabinetów, i że różnice
  indywidualne są większe niż obie te liczby razem wzięte. Musi działać wyjęta z kontekstu,
  bo to najlepszy kandydat do AI Overviews w całej partii.
- Lista czterech rzeczy, które zmieniają czyjś przebieg, 50-70 słów, po jednym zdaniu każda.

**7. Hero**
- Wariant „abstrakcja" (`scripts/image-gen/prompts-blog-mindsync/hero-02-abstrakcja.md`):
  miękka wznosząca się krzywa złożona z kilku rozmytych pól w palecie sand i mint,
  wypłaszczająca się po prawej stronie, zero osi, zero cyfr, zero wykresu dosłownie.
- `hero_image_alt`: „A soft rising curve made of layered shapes in sand and mint tones,
  flattening towards the right".

**8. Źródła** (to jest rdzeń wpisu, więc weryfikacja jest obowiązkowa przy każdej liczbie)
- **POTWIERDZONE.** Howard, Kopta, Krause, Orlinsky, 1986, *American Psychologist*, 41(2),
  159-164, „The dose-effect relationship in psychotherapy" (rekord APA PsycNet
  1986-17818-001, pełny tekst PDF dostępny publicznie). Omówienia podają: około 30% poprawy
  po 2 sesjach, 41% po 4, 53% po 8 i 75% po 26. ⚠ **Weź liczby z pierwotnego PDF-a, nie
  z omówień.** W obiegu są dwie wersje tych danych, jedna punktowa i jedna przedziałowa
  (rzędu 48-58% po ośmiu sesjach). Jeśli po lekturze zostaje wątpliwość, podaj wersję
  bezpieczną i jawnie przybliżoną: „about half by session 8 and about three quarters by
  session 26", i tak opisz źródło.
- **POTWIERDZONE.** Hansen, Lambert, Forman, 2002, *Clinical Psychology: Science and
  Practice*, 9(3), 329-343, „The psychotherapy dose-response effect and its implications for
  treatment delivery services". Z omówień i abstraktu: konsensus badawczy mówi o 13-18
  sesjach potrzebnych, by połowa pacjentów osiągnęła poprawę, natomiast w bazie ponad 6000
  pacjentów z rutynowej praktyki przeciętna liczba odbytych sesji wynosiła mniej niż pięć,
  a odsetek poprawy około 20%. ⚠ Zweryfikuj obie liczby w abstrakcie przed podaniem
  i **zaznacz w zdaniu, że to dane amerykańskie sprzed ponad dwóch dekad**.
- **POTWIERDZONE.** Robinson, Delgadillo, Kellett, 2020, *Psychotherapy Research*, 30(1),
  79-96, „The dose-response effect in routinely delivered psychological therapies:
  A systematic review". Wynik: 26 badań, powtarzalne i spójne wsparcie dla zależności
  krzywoliniowej między długością leczenia a wynikiem, z nielicznymi wyjątkami, wśród
  których wymieniane są zaburzenia odżywiania i ciężkie populacje psychiatryczne.
  **Wyjątki wymień**, bo to jest dokładnie ta uczciwość, której nie ma konkurencja.
- **DO WERYFIKACJI, BEZ LICZB DOPÓKI NIE POTWIERDZISZ.** Model „good enough level" (prace
  Barkhama i wsp. oraz Stulza i wsp. w *Journal of Consulting and Clinical Psychology*).
  Ideę możesz opisać jakościowo w jednym akapicie: liczba sesji w danych odzwierciedla to,
  kiedy komu wystarczyło, a nie to, ile potrzeba. Bez wielkości efektu i bez odsetków,
  dopóki nie masz abstraktu przed oczami.
- **Czego autor ma NIE twierdzić:**
  - że istnieje zalecana liczba sesji przy konkretnym problemie (zero „przy X potrzebujesz
    Y sesji", to byłaby porada medyczna),
  - że osiem sesji „wystarcza" albo że po jakiejś liczbie sesji terapia „przestaje działać",
  - że dane amerykańskie przekładają się na inne kraje i systemy opieki,
  - że któryś nurt terapii działa szybciej (to inny wpis i inne dowody),
  - że praca między sesjami przyspiesza terapię o konkretną liczbę sesji; związek prac
    domowych z wynikiem jest opisany w `/journal/how-to-do-therapy-homework`, tu wystarczy
    zdanie jakościowe i link.

**9. Czego NIE robić**
- Zero diagnozowania i zero przypisywania czytelnikowi rozpoznania na podstawie tego, jak
  długo już chodzi.
- Nie namawiaj ani do zakończenia, ani do przedłużenia terapii. Wpis daje liczby i sposób
  pomiaru, decyduje czytelnik razem z terapeutą.
- Nie dubluj metodyki pomiaru z `/journal/how-to-know-if-therapy-is-working` ani kosztów
  z `/journal/is-therapy-worth-the-money`. Po jednym akapicie i link.
- Zero cen, żadnych, także terapii. Arytmetyka dotyczy liczby sesji, nie kwot.
- **Nie sugeruj, że MindSync przyspiesza terapię.** To jest najważniejsze zdanie tego briefu.
  Apka pokazuje przebieg i daje materiał do rozmowy, nie zmienia tempa leczenia. Jedno
  nieostrożne zdanie w tym wpisie łamie i YMYL, i pozycjonowanie marki.

---

# 03. How to name what you are feeling

**1. Meta**
- `seo_url`: `how-to-name-what-you-feel` | plik:
  `blog/queue/2026-09-23_how-to-name-what-you-feel.json`
- kategoria: `MindSync Tips` | `kolor`: `#ff9f8a` | `planowana_data`: **2026-09-23**
- `tagi`: `["understanding-patterns", "emotions"]`
- H1: „How to Name What You Are Feeling When All You Have Is Bad"
- `meta_title` (43 zn.): „How to Name What You Are Feeling | MindSync"
- `meta_description` (151 zn.): „When the only words you have are fine, bad and tired: what
  the research on emotional granularity shows, and four questions that get you to a better
  word."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `how to name your emotions`
- poboczne: `emotional granularity`, `I don't know what I'm feeling`, `how to describe your
  feelings`, `why can't I identify my emotions`, `how to be more specific about your
  emotions`, `does a feelings wheel work`
- intencja: mieszana, praktyczno-informacyjna. Dwie grupy: osoba w terapii, która słyszy
  „a co wtedy czułeś" i nie ma odpowiedzi, oraz osoba, która trafiła na termin „emotional
  granularity" w mediach i chce wiedzieć, co z nim zrobić. Piszemy dla pierwszej, drugą
  obsługujemy definicją na początku.
- luka: SERP dzieli się na dwie części. Z jednej strony solidne wyjaśnienia bez praktyki
  (Time z sierpnia 2026, Psychology Today). Z drugiej dziesiątki stron z kołem emocji
  i treścią masową, które dają listę słów i kończą. **Nikt nie pisze, co robić, kiedy koło
  emocji nie pomaga**, a to jest najczęstszy realny problem: człowiek patrzy na sto słów
  i żadne nie pasuje. Nasz kąt: precyzja nie bierze się ze słownika, tylko z kontekstu,
  z ciała i z tego, czego się chciało. Do tego uczciwość: to umiejętność budowana tygodniami,
  nie ćwiczenie na jeden wieczór.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): terapeuta pyta, co czułeś w tamtym momencie, a jedyne słowo, jakie masz,
  to „dziwnie", i słyszysz, jak marnie to brzmi.
- H2: What emotional granularity means
  - definicja robocza, cytowalna, 40-60 słów: różnica między „czuję się źle" a „jestem
    zawiedziony i trochę zawstydzony". Zaznacz, że to opisowa cecha badana w psychologii,
    a nie test, który się zdaje, i nie coś, co się ma albo czego się nie ma.
- H2: Why a bigger vocabulary is not the point
  - teza wpisu: koło emocji daje słowa, nie daje kontekstu. Ludzie utykają nie dlatego, że
    brakuje im słownictwa, tylko dlatego, że nie mają czego do tych słów przyłożyć.
- H2: What the research links it to
  - Kashdan i wsp. 2010: osoby lepiej różnicujące emocje piły mniej alkoholu w momentach
    silnych emocji negatywnych, w badaniu z pomiarem w codziennym życiu. Zastrzeżenie
    obowiązkowe: to obserwacja na wąskiej próbie, nie dowód, że nauka nazywania emocji
    zmniejszy czyjeś picie.
  - Kashdan, Barrett, McKnight 2015: przegląd, wyższa granularność wiąże się z lepszą
    regulacją emocji. Napisz wprost, że to związki korelacyjne.
  - Barrett i wsp. 2001: praca źródłowa pokazująca, że ludzie realnie różnią się tym, jak
    różnicują własne stany.
  - Hoemann i wsp. 2021: granularność rosła w trakcie intensywnego, powtarzanego opisywania
    własnych stanów. To jest najciekawszy wynik dla naszego czytelnika i jednocześnie ten,
    przy którym najłatwiej przesadzić, patrz zastrzeżenia w sekcji 8.
  - afektywne etykietowanie (Lieberman i wsp. 2007) jednym zdaniem, bez rozwijania
- H2: The four questions that get you past „bad"
  - sekcja praktyczna i rdzeń użytkowy wpisu, każde pytanie z jednym przykładem przejścia od
    „bad" do konkretnego słowa
  - H3: Where is it in your body?
  - H3: What did you want that you did not get?
  - H3: Who is it pointed at?
  - H3: What would have to change for it to stop?
- H2: Two words are usually more accurate than one
  - mieszanki: ulga razem z poczuciem winy, złość razem ze wstydem, czułość razem
    z irytacją. Krótko, trzy przykłady, bez teorii.
- H2: Practise where the stakes are low
  - kiedy ćwiczyć: nie w środku najgorszego wieczoru, tylko na drobnych sytuacjach,
    trzydzieści sekund, dwa razy dziennie, przez kilka tygodni
  - karta `reflect`
- H2: What to do with the words once you have them
  - po co to w terapii: jedno precyzyjne zdanie otwierające sesję zmienia pierwsze
    piętnaście minut; link do wpisu o przygotowaniu
- blok `[FEATURES:]`
- H2: Frequently asked questions
  - H3: What is emotional granularity?
  - H3: Why can't I identify my emotions?
  - H3: How do I describe my feelings to my therapist?
  - H3: Does a feelings wheel actually help?
  - H3: How long does it take to get better at naming emotions?

**4. Karty funkcji** (bramka potwierdziła: reflect, check-ins, mood-trends, personal-bio)
- inline w „Practise where the stakes are low":
  `[FEATURE: reflect | When the only word you have is bad, the guided version keeps asking, in writing or out loud, until the word gets closer.]`
- blok przed FAQ:
  `[FEATURES: Getting more precise over weeks, not in one evening || check-ins | A one minute rating of the areas you are working on, which gives the words something to attach to. || mood-trends | Weeks of your own ratings side by side, where the difference between a flat month and one hard week becomes visible. || personal-bio | A living picture of what you keep coming back to, written from your own entries rather than from a questionnaire.]`
- ⚠ Tylko dwie karty w tym wpisie (jedna inline plus blok). To jest celowe: tekst jest
  gęsty od badań i czterech pytań praktycznych, trzecia karta zrobiłaby z niego katalog.

**5. Mapa linkowania** (wszystko wstecz, zero `[LINK-LATER:]`)
- `<a href="/journal/how-to-identify-emotional-triggers">` anchor „what set the reaction off
  in the first place" (sekcja z czterema pytaniami)
- `<a href="/journal/journaling-vs-voice-notes">` anchor „writing it down or saying it out
  loud" (sekcja o ćwiczeniu)
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` anchor „turn it into an opening
  sentence for the next session" (ostatnia sekcja merytoryczna)
- `<a href="/journal/therapy-hangover">` anchor „the evening after a heavy session"
  (opublikowany 2026-09-21, normalny link)
- **Landing partner:** `/pre-order/deep-emotional-analysis` (anchor „a closer read on the
  emotions that keep repeating"), jeden raz. Nie używaj anchora „a deeper read on what you
  keep coming back to", bo jest już zajęty przez `/journal/journaling-vs-voice-notes`.

**6. GEO**
- Definicja `emotional granularity`, 40-60 słów, z przykładem kontrastowym w jednym zdaniu.
- Cztery pytania z sekcji praktycznej, 60-80 słów, zapisane tak, żeby dały się przepisać
  w całości jako gotowa procedura. To jest najmocniejszy kandydat do cytowania w tym wpisie,
  bo w SERP wszyscy dają listę słów, a nikt nie daje procedury.

**7. Hero**
- Wariant „abstrakcja" (`hero-02-abstrakcja.md`): jedno duże rozmyte pole po lewej, które ku
  prawej stronie rozdziela się na kilka mniejszych, wyraźniejszych kształtów, paleta mint
  i sand, zero symboli, zero twarzy, zero koła emocji.
- `hero_image_alt`: „One soft shape separating into several distinct smaller forms in mint
  and sand tones".

**8. Źródła**
- **POTWIERDZONE.** Kashdan, Ferssizidis, Collins, Muraven, 2010, *Psychological Science*,
  „Emotion differentiation as resilience against excessive alcohol use: an ecological
  momentary assessment in underage social drinkers" (PubMed 20696854). Wynik: 106 młodych
  osób pijących towarzysko monitorowało spożycie przez trzy tygodnie; osoby lepiej
  różnicujące emocje piły mniej w momentach silnych emocji negatywnych. ⚠ **Nie podawaj
  liczby „o 40% mniej alkoholu"**, jeśli nie znajdziesz jej w abstrakcie albo w pełnym
  tekście; w omówieniach krąży, ale w streszczeniu badania jest ujęcie jakościowe. Opisz
  wynik jakościowo, chyba że potwierdzisz liczbę u źródła.
- **POTWIERDZONE jako pozycja.** Kashdan, Barrett, McKnight, 2015, *Current Directions in
  Psychological Science*, „Unpacking emotion differentiation". Użyj jako przeglądu i napisz
  wprost, że opisywane związki są korelacyjne.
- **DO WERYFIKACJI.** Barrett, Gross, Christensen, Benvenuto, 2001, *Cognition and Emotion*,
  „Knowing what you're feeling and knowing what to do about it: mapping the relation between
  emotion differentiation and emotion regulation". Zweryfikuj tytuł i rok przed cytowaniem;
  jeśli się nie zgadza, oprzyj sekcję na przeglądzie z 2015 i pomiń pracę źródłową.
- **POTWIERDZONE, ale z twardym zastrzeżeniem.** „Emotional Granularity Increases With
  Intensive Ambulatory Assessment: Methodological and Individual Factors Influence How Much",
  2021, *Frontiers in Psychology* (PubMed 34393942), zespół z udziałem Hoemann. ⚠ Zweryfikuj
  pełną listę autorów przed podaniem nazwisk. **Zastrzeżenie obowiązkowe:** sami autorzy
  opisują to jako efekt związany z metodą pomiaru, a nie jako dowód skuteczności
  interwencji. Nie wolno z tego zrobić zdania „badania pokazują, że codzienne opisywanie
  emocji poprawia twoje zdrowie psychiczne".
- **POTWIERDZONE jako pozycja, jedno zdanie.** Lieberman i wsp., 2007, *Psychological
  Science*, „Putting feelings into words". ⚠ Ten sam mechanizm jest już cytowany
  w opublikowanym `/journal/journaling-vs-voice-notes`. Tutaj wolno go użyć w jednym zdaniu
  i z innego ujęcia (tam: mówienie kontra pisanie, tu: precyzja słowa). Nie przepisuj tamtej
  sekcji, bo zjemy własny wpis.
- **Czego autor ma NIE twierdzić:**
  - że nazywanie emocji obniża lęk albo leczy cokolwiek (afektywne etykietowanie opisuje
    zmiany w aktywności mózgu w warunkach laboratoryjnych, nie efekt kliniczny),
  - że wyższa granularność powoduje lepszą regulację emocji; dowody są korelacyjne
    i tak mają być opisane,
  - że czytelnik ma aleksytymię albo jakikolwiek deficyt. Termin można wymienić najwyżej
    raz, jako cechę badaną w psychologii, nigdy w zdaniu skierowanym do czytelnika,
  - że koło emocji nie działa. Piszemy tylko tyle, że samo słownictwo nie wystarcza,
    bo na „nie działa" nie ma dowodów,
  - że da się to opanować w tydzień, i żadnych liczb typu „po 14 dniach".

**9. Czego NIE robić**
- Zero diagnozowania, zero testów w rodzaju „sprawdź, czy masz niską granularność", zero
  sugerowania czytelnikowi deficytu.
- Nie rób z tego wpisu o journalingu jako metodzie, bo to jest
  `/journal/journaling-vs-voice-notes`. Tu chodzi o precyzję słowa, nie o wybór formatu.
- Nie wchodź w mechanikę triggerów, od tego jest `/journal/how-to-identify-emotional-triggers`.
  Jeden akapit i link.
- Nie obiecuj, że apka nauczy czytelnika nazywać emocje. Daje pytania, rytm i materiał do
  przejrzenia, a umiejętność buduje się przez powtarzanie.
- Nie wstawiaj listy stu emocji ani koła emocji jako grafiki. Wpis ma dawać procedurę,
  a nie kolejny słownik.
