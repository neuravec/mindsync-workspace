# Partia 2 – briefy wpisów (10 pozycji, drip 2026-09-04..2026-09-13)

> Data: 2026-09-03. Autor briefów: `seo-content-writer`. Wykonawca prozy: `blog-writer`
> (+ `humanizer`, akcept `brand-voice-manager`, schema od `seo-tech-lead`, hero od
> `graphic-designer`). **Treść po ANGIELSKU.** Format pliku kolejki: `blog/queue/_format.md`.
> Głos marki i zakazy: `docs/blog/brand-mindsync.md`.
>
> **Status bramki KROK 0:** `blog/queue/_preflight-partia2.json` – **10× OK, 0 RYZYKO,
> 0 BRAK**. Żaden temat nie trafia do `docs/luki-funkcji.md`.
>
> **Status danych:** GSC właściwości mindsync.app jest na innym koncie Google (patrz
> `blog/README.md` §4), Ahrefs w tej sesji niedostępny. Frazy główne i poboczne pochodzą
> z researchu SERP (kto rankuje, jaka jest luka), **bez wolumenów i bez KD**. Pytania FAQ
> są przepisane z realnych brzmień zapytań widocznych w wynikach i w tytułach konkurencji,
> nie parafrazowane. Po odblokowaniu GSC: `scripts/gsc/blog-partia-frazy.py` i korekta
> H2 oraz FAQ na frazy z liczbami.

## Zasady wspólne dla wszystkich 10 briefów (nie powtarzam ich w każdym)

1. **Zakaz em-dash (U+2014)** w tytule, meta, zajawce i treści. Półpauza „–" ze spacjami
   albo przebudowa zdania. Bramka dripu odrzuca wpis z em-dash.
2. **YMYL:** zero diagnozowania, zero obietnic wyleczenia, zero zniechęcania do leków
   i terapii, zero porad prawnych. MindSync uzupełnia terapię, nie zastępuje. Zero tematów
   kryzysowych. Wpis 09 (leki) ma dodatkowe reguły w swoim briefie i jest najostrożniejszy
   w partii.
3. **Funkcje `planned` nie istnieją w treści:** `therapist-sharing` (portal ukryty,
   MSV3.4 CS-11) i `streaks` (brak UI). Nie sugerujemy wysyłania czegokolwiek terapeucie
   z apki ani odznak za wytrwałość, nawet jeśli landing `/pre-order/*` albo strona www
   to sugeruje.
4. **Zero cen MindSync w treści** (od cennika jest `/membership`). Ceny terapii we wpisie 03
   podajemy wyłącznie jako cudze, datowane, źródłowane przedziały rynkowe, nigdy jako naszą
   rekomendację. Zero wymyślonych zrzutów ekranu i zero wymyślonych nazw przycisków. Nazwa
   ekranu bez pokrycia w `blog/app-features.json` = znacznik `[VERIFY-UI: ...]`.
5. **Karty:** maksymalnie 3 na wpis (1-2 `[FEATURE:]` inline + ewentualnie jeden blok
   `[FEATURES:]` przed FAQ). Powód w karcie to jedno zdanie prozą, po angielsku. Tylko id
   o statusie `live` (16 sztuk w katalogu).
6. **FAQ:** nagłówek H2 dokładnie `Frequently asked questions`, pytania w H3, 4-5 sztuk,
   w brzmieniu realnego zapytania. Odpowiedź 40-70 słów, pierwsze zdanie to pełna odpowiedź
   (GEO), reszta to warunek albo zastrzeżenie.
7. **Badania:** każda liczba ma nazwisko, rok i czasopismo. Autor **weryfikuje źródło
   pierwotne** przed użyciem. Jeśli nie da się potwierdzić autorów, roku i liczby,
   twierdzenie wypada z tekstu. Linkujemy do publikacji albo do rekordu PubMed/PMC, nie
   do wtórnych blogów. **Ankiety firm komercyjnych** (np. „80% pracowników ma Sunday
   scaries") oznaczamy w zdaniu jako ankietę firmy X z roku Y, nie jako badanie naukowe.
8. **Struktura:** lead 40-60 słów (scena z życia, nie definicja), sekcje merytoryczne
   z badaniami, sekcja praktyczna, karty, FAQ. Bez sekcji „Conclusion" i bez waty.
   **Długość każdego wpisu w tej partii: 1600-2000 słów.**
9. **Linki wewnętrzne wyłącznie ścieżkami względnymi:** `<a href="/journal/slug">`,
   `<a href="/features">`, `<a href="/pre-order/...">`. **Nigdy `https://mindsync.app/...`**
   ani `https://www.mindsync.app/...` w treści wpisu: kanoniczny host to `www`, więc link
   bezwzględny na goły host generuje przekierowanie 301 i traci moc linku.
10. **Linki do wpisów tej partii, które wychodzą PÓŹNIEJ:** wyłącznie
    `[LINK-LATER: <slug> | <anchor EN>]`. Surowe `[LINK: ...]` = bramka dripu odrzuca wpis.
    Kolejność dat jest tak ułożona, żeby `[LINK-LATER:]` było jak najmniej.
11. **Slug wpisu** = pole `seo_url`; URL publiczny to `/journal/<slug>`.

## Kolejność publikacji, daty i topologia linkowania

Huby idą wcześnie, wpisy linkujące szeroko idą później. Dzięki temu w całej partii zostaje
tylko **5 znaczników `[LINK-LATER:]`** (01 ma dwa, 02 jeden, 05 jeden, 06 jeden), a wszystkie
pozostałe linki wewnątrz partii są normalnymi `<a href>` do wpisów już opublikowanych.

| data | # | slug (`seo_url`) | klaster | kategoria | `kolor` | rola |
|---|---|---|---|---|---|---|
| 2026-09-04 | 01 | `how-to-choose-a-therapist` | 4 | Therapy | `#339499` | HUB klastra 4 |
| 2026-09-05 | 02 | `what-to-do-when-your-therapist-is-not-the-right-fit` | 4 | Therapy | `#1f3d38` | wspierający |
| 2026-09-06 | 03 | `is-therapy-worth-the-money` | 4 | Therapy | `#e8af0a` | wspierający |
| 2026-09-07 | 05 | `journaling-vs-voice-notes` | 2 | MindSync Tips | `#3c67a5` | HUB metody |
| 2026-09-08 | 04 | `how-to-do-therapy-homework` | 2 | Therapy | `#ff9f8a` | wspierający |
| 2026-09-09 | 06 | `racing-thoughts-at-night` | 5 | Therapy | `#339499` | HUB klastra 5 |
| 2026-09-10 | 07 | `sunday-scaries` | 5 | Therapy | `#1f3d38` | wspierający |
| 2026-09-11 | 08 | `how-to-stop-doomscrolling` | 5 | Therapy | `#3c67a5` | wspierający |
| 2026-09-12 | 09 | `tracking-mood-on-antidepressants` | 6 | Therapy | `#e8af0a` | duet landingu |
| 2026-09-13 | 10 | `are-mental-health-apps-private` | 6 | MindSync Tips | `#339499` | zamyka partię |

Wpisy z partii 1 (już na żywo, linkujemy do nich normalnym `<a href>`):
`/journal/how-to-use-mindsync`, `/journal/how-to-prepare-for-a-therapy-session`,
`/journal/how-to-remember-what-you-talk-about-in-therapy`,
`/journal/how-to-know-if-therapy-is-working`, `/journal/which-coping-skills-actually-work`,
`/journal/how-to-identify-emotional-triggers`, `/journal/why-mood-tracking-stops-working`,
`/journal/what-to-do-between-therapy-sessions` (pillar klastra 2),
`/journal/digital-burnout-brain-rewiring`,
`/journal/regulate-nervous-system-between-therapy-sessions`.

---

# 01. How to choose a therapist (HUB klastra 4)

**1. Meta**
- `seo_url`: `how-to-choose-a-therapist`
- kategoria: `Therapy` | `kolor`: `#339499` | `planowana_data`: **2026-09-04**
- `tagi`: `["therapy-logistics", "hub"]`
- H1: „How to Choose a Therapist: The Questions That Actually Sort Them"
- `meta_title` (49 zn.): „How to Choose a Therapist: What to Ask | MindSync"
- `meta_description` (159 zn.): „A practical way to choose a therapist: what to ask on the
  consult call, which differences actually matter, and how to judge fit after the first
  three sessions."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `how to choose a therapist`
- poboczne: `how to find the right therapist`, `questions to ask a therapist before
  starting`, `how do I know if a therapist is right for me`, `what type of therapist do
  I need`, `how many therapists should I talk to`, `therapist consultation call questions`
- intencja: decyzyjna, przed pierwszą sesją. Człowiek ma listę nazwisk z katalogu albo
  z ubezpieczenia i nie wie, po czym wybrać. Wysoka niepewność, niski poziom wiedzy
  o modalnościach, duża wrażliwość na koszt pomyłki.
- luka: SERP to Harvard Health, ABCT, Psychology Today, ChoosingTherapy i Healthline.
  Wszyscy dają listę pytań do zadania. **Nikt nie mówi, co zrobić z odpowiedziami**: jak
  odróżnić odpowiedź dobrą od gładkiej, ile spotkań dać, po czym poznać, że to już fit,
  a nie tylko ulga z pierwszej rozmowy. To jest nasz kąt: decyzja i jej weryfikacja
  w czasie, nie kolejna lista pytań.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): masz w przeglądarce czternaście otwartych profili, wszyscy piszą
  „warm, collaborative, evidence based", i nie masz żadnego kryterium, żeby ich rozróżnić.
- H2: What actually predicts whether therapy helps
  - relacja robocza i badania nad nią; jedno uczciwe zastrzeżenie, że to korelacja
- H2: The three filters that come before personality
  - H3: Access and logistics (schedule, format, waitlist, insurance or self-pay)
  - H3: Experience with your specific problem
  - H3: Licence and scope (kto może pracować z czym; bez porad prawnych, ogólnie o tym,
    że tytuły znaczą różne rzeczy w różnych krajach)
- H2: The consultation call: six questions and what a good answer sounds like
  - H3: „How do you usually work with someone dealing with this?"
  - H3: „How will we know if this is working?"
  - H3: „What do you expect from me between sessions?"
  - H3: „What happens if I tell you something is not working?"
  - przy każdym pytaniu jedno zdanie „a good answer sounds like" i jedno
    „a vague answer sounds like". To jest sedno wpisu.
- H2: Modality: how much should it decide?
  - CBT/psychodynamic/EMDR w jednym akapicie każdy, po ludzku; uczciwie o tym, że różnice
    między nurtami są mniejsze niż marketing sugeruje, a przy konkretnych problemach
    protokół jednak ma znaczenie
- H2: The first three sessions are the real interview
  - H3: What to notice in session one (zrozumienie, tempo, kto prowadzi)
  - H3: What to notice by session three (czy jest plan, czy wracacie do tematu)
  - H3: Relief is not the same as fit
- H2: A simple way to keep score without turning it into a spreadsheet
  - sekcja praktyczna: trzy rzeczy notowane po każdej z pierwszych sześciu sesji
- H2: Frequently asked questions
  - H3: How do I choose a therapist?
  - H3: What questions should I ask a therapist before starting?
  - H3: How do I know if a therapist is right for me?
  - H3: How many therapists should I talk to before choosing one?
  - H3: Does the type of therapy matter more than the therapist?

**4. Karty funkcji** (werdykt: health-check, session-prep, goals, mood-trends)
- inline w „The first three sessions are the real interview":
  `[FEATURE: health-check | A short structured check on how the working relationship is going, so a vague sense that something is off turns into something you can name.]`
- inline w „A simple way to keep score":
  `[FEATURE: session-prep | The prep card pulls your week into one screen, which matters most in the first months, when you are still learning what to bring.]`
- blok przed FAQ:
  `[FEATURES: Judging fit with something more than a hunch || goals | What you came for, written down, with evidence collecting underneath it. || mood-trends | The areas you are working on, charted over weeks instead of recalled after a hard day. || health-check | A regular read on the working relationship itself.]`

**5. Mapa linkowania**
- `<a href="/journal/how-to-know-if-therapy-is-working">` anchor „how to tell whether
  therapy is working once you have started" (sekcja „The first three sessions")
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` anchor „walk into the first
  session with something to say"
- `[LINK-LATER: what-to-do-when-your-therapist-is-not-the-right-fit | what to do when the
  fit turns out to be wrong]`
- `[LINK-LATER: is-therapy-worth-the-money | what therapy costs, and how to judge what you
  get for it]`
- **Landing partner:** `/features` (anchor „the therapy relationship check"), pomocniczo
  `/audience` (anchor „who MindSync is built for").

**6. GEO (fragmenty cytowalne)**
- Odpowiedź na `how to choose a therapist`, 55-75 słów, w formie czterech kroków: filtry
  logistyczne, doświadczenie z twoim problemem, rozmowa wstępna z konkretnymi pytaniami,
  weryfikacja po trzech sesjach. Musi działać wyjęta z kontekstu.
- Cytowalna lista sześciu pytań na rozmowę wstępną (H3 wyżej), 60-80 słów, do przepisania
  w całości.

**7. Hero**
- Wariant „codzienny moment" (`scripts/image-gen/prompts-blog-mindsync/hero-01-codzienny-moment.md`):
  laptop zamknięty do połowy i kubek na stole przy oknie, notes z odręczną listą bez
  czytelnego tekstu, poranne światło.
- `hero_image_alt`: „A notebook and a cup beside a half closed laptop in morning light,
  choosing a therapist".

**8. Źródła do weryfikacji**
- „Relacja robocza wiąże się z wynikiem terapii" → metaanaliza Flückiger, Del Re, Wampold
  i Horvath, 2018, *Psychotherapy*. Podaj współczynnik tylko po weryfikacji i dopisz,
  że to związek korelacyjny.
- „Różnice między terapeutami są większe niż różnice między nurtami" → efekt terapeuty,
  Baldwin i Imel, 2013, *Bergin and Garfield's Handbook of Psychotherapy and Behavior
  Change*, albo Wampold i Imel, 2015, *The Great Psychotherapy Debate*. Zweryfikuj wydanie.
- „Nurty terapii dają zbliżone efekty w wielu problemach, ale nie we wszystkich"
  → Wampold i wsp., 1997, *Psychological Bulletin*. Zastrzeżenie obowiązkowe: przy
  niektórych rozpoznaniach protokoły różnią się skutecznością, więc nie pisz „nurt nie ma
  znaczenia".
- Praktyczne listy pytań (Harvard Health, ABCT) możesz przywołać jako źródła konsumenckie,
  wyraźnie oddzielone od badań.

**9. Czego NIE robić**
- Nie sugeruj, że czytelnik potrzebuje konkretnej terapii przy konkretnym objawie. Zero
  diagnozowania i zero „jeśli masz X, wybierz Y".
- Nie podawaj stawek ani nazw platform terapeutycznych jako rekomendacji.
- Nie wchodź w temat zmiany terapeuty w trakcie (to 02) ani w metodykę pomiaru postępu
  (opublikowany `/journal/how-to-know-if-therapy-is-working`). Po jednym akapicie i link.
- Nie obiecuj, że apka pomoże wybrać terapeutę. Pomaga po wyborze, przy ocenie fitu.

---

# 02. What to do when your therapist is not the right fit

**1. Meta**
- `seo_url`: `what-to-do-when-your-therapist-is-not-the-right-fit`
- kategoria: `Therapy` | `kolor`: `#1f3d38` | `planowana_data`: **2026-09-05**
- `tagi`: `["therapy-logistics", "alliance"]`
- H1: „What to Do When Your Therapist Is Not the Right Fit"
- `meta_title` (51 zn.): „When Your Therapist Is Not the Right Fit | MindSync"
- `meta_description` (151 zn.): „Therapy stopped feeling useful with this therapist. Here
  is how to tell a rough patch from a bad fit, how to raise it, and how to switch without
  drama."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `what to do when your therapist is not the right fit`
- poboczne: `how to know if your therapist is right for you`, `should I switch therapists`,
  `how to break up with your therapist`, `not clicking with my therapist`,
  `how to tell your therapist it is not working`, `is it normal to not like your therapist`
- intencja: rozterka plus wstyd. Człowiek chodzi od kilku miesięcy, coś nie gra, a odejście
  wydaje się niewdzięcznością albo porażką. Ton: normalizacja, potem rozróżnienie, potem
  konkretne zdania do wypowiedzenia.
- luka: SERP to teksty typu „4 signs you need to dump your therapist" i wątki z Reddita.
  Dominuje rada „powiedz to". **Nikt nie odróżnia zerwania relacji, które warto naprawić,
  od realnego braku dopasowania**, i nikt nie daje gotowych zdań na tę rozmowę. Do tego
  badania nad naprawą zerwań są w tym SERP-ie nieobecne, a to jest nasz konkret.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): wychodzisz z kolejnej sesji z uczuciem, że opowiedziałeś tydzień
  i nic z tego nie wynikło, a myśl o zmianie terapeuty wydaje się cięższa niż sam problem.
- H2: Not clicking is common, and it is not a verdict on you
  - dane o przerywaniu terapii; zdanie normalizujące bez lekceważenia
- H2: A rupture is not the same as a bad fit
  - H3: What a rupture looks like (nagła zmiana po konkretnej sesji, poczucie niezrozumienia
    w jednym temacie, unikanie tematu)
  - H3: What a bad fit looks like (miesiące bez kierunku, brak planu, powtarzalny brak
    bezpieczeństwa, wartości i styl pracy nie do pogodzenia)
  - H3: The two mistakes people make (zostają zbyt długo z uprzejmości, albo odchodzą
    dokładnie w momencie, w którym robi się trudno)
- H2: What the research says about repairing it
  - metaanaliza naprawy zerwań przymierza; uczciwe zastrzeżenie o sile dowodów
- H2: How to raise it, in actual sentences
  - H3: Opening lines that are not accusations
  - H3: What to ask for specifically (plan, tempo, więcej struktury, inny temat)
  - H3: What a good response from a therapist sounds like
  - H3: What a defensive response tells you
- H2: If you decide to leave
  - H3: How much notice, and why one closing session helps
  - H3: What to say in an email if talking feels impossible
  - H3: What to take with you to the next therapist (co działało, co nie, czego próbowaliście)
- H2: Before you decide: three things worth checking
  - sekcja praktyczna: czy problem jest w metodzie, w tempie, czy w relacji; ile sesji
    minęło od ostatniej zmiany tematu; co mówią twoje własne zapisy z ostatnich tygodni
- H2: Frequently asked questions
  - H3: How do I know if my therapist is not right for me?
  - H3: Is it normal to not click with your therapist?
  - H3: How do I tell my therapist I want to switch?
  - H3: Should I give my therapist another chance?
  - H3: Do I have to tell my therapist why I am leaving?

**4. Karty funkcji** (werdykt: health-check, workspace, session-debrief, mood-trends)
- inline w „A rupture is not the same as a bad fit":
  `[FEATURE: health-check | A short check on the working relationship, repeated over time, so you can see whether this is one bad month or a pattern.]`
- inline w „Before you decide":
  `[FEATURE: workspace | The thing you almost said in session goes on your agenda for next time instead of dissolving on the way home.]`
- blok przed FAQ (opcjonalny, tylko jeśli tekst tego nie przeciąży):
  `[FEATURES: Deciding with evidence, not on a bad Thursday || session-debrief | Five minutes after the session, while you still remember how it felt. || mood-trends | Weeks side by side, so one hard session stops standing in for the whole year. || health-check | The same questions about the relationship, asked again a month later.]`

**5. Mapa linkowania**
- `<a href="/journal/how-to-choose-a-therapist">` anchor „how to choose a therapist in the
  first place" (opublikowany 09-04, sekcja „If you decide to leave")
- `<a href="/journal/how-to-know-if-therapy-is-working">` anchor „measure whether therapy
  is working before you decide anything"
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` anchor „put it on the agenda
  for next time"
- `[LINK-LATER: is-therapy-worth-the-money | what you are paying for, and how to judge it]`
- **Landing partner:** `/features` (anchor „the therapy relationship check"), pomocniczo
  `/pre-order/tracking-therapy-effectiveness` (anchor „tracking whether therapy is
  actually working", jeden raz, naturalnie w zdaniu).

**6. GEO**
- Cytowalne rozróżnienie rupture kontra bad fit, 50-70 słów, w formie dwóch krótkich
  definicji z przykładem. To jest fragment z największą szansą na cytowanie.
- Cytowalny zestaw trzech zdań otwierających rozmowę z terapeutą, 40-60 słów, gotowy do
  przepisania.

**7. Hero**
- „Codzienny moment": dwa fotele pod kątem, jeden pusty, miękkie boczne światło, żadnych
  twarzy, żadnej kliszy kozetki.
- `hero_image_alt`: „Two chairs at a slight angle in a quiet room with soft daylight".

**8. Źródła do weryfikacji**
- „Naprawa zerwania przymierza wiąże się z lepszym wynikiem terapii" → metaanaliza
  Eubanks, Muran i Safran, 2018, *Psychotherapy*. Zweryfikuj wielkość efektu i napisz
  wprost, że liczba badań jest ograniczona.
- „Część osób przerywa terapię przed czasem" → Swift i Greenberg, 2012, *Journal of
  Consulting and Clinical Psychology*. Podaj odsetek tylko po weryfikacji w abstrakcie.
- „Informacja zwrotna od klienta poprawia wyniki, zwłaszcza gdy idzie gorzej" → Lambert
  i Shimokawa, 2011, *Psychotherapy*.
- „Przymierze przewiduje wynik" → Flückiger i wsp., 2018, *Psychotherapy* (to samo źródło
  co w 01, tu tylko jedno zdanie, bez powtarzania całej sekcji).

**9. Czego NIE robić**
- Nie namawiaj do odejścia ani do zostania. Wpis daje kryteria, decyduje czytelnik.
- Zero sugestii, że terapeuta zrobił coś nieetycznego, poza jednym akapitem: jeśli chodzi
  o naruszenie granic, to nie jest kwestia dopasowania, i tam kieruj do izby zawodowej
  albo instytucji licencjonującej w swoim kraju, bez podawania konkretnych procedur.
- Nie dubluj metodyki pomiaru z `/journal/how-to-know-if-therapy-is-working`. Jeden akapit
  i link.
- Nie sugeruj pokazywania terapeucie danych z apki (`therapist-sharing` = planned).

---

# 03. Is therapy worth the money

**1. Meta**
- `seo_url`: `is-therapy-worth-the-money`
- kategoria: `Therapy` | `kolor`: `#e8af0a` | `planowana_data`: **2026-09-06**
- `tagi`: `["therapy-logistics", "measurement"]`
- H1: „Is Therapy Worth the Money? How to Judge What You Are Getting"
- `meta_title` (38 zn.): „Is Therapy Worth the Money? | MindSync"
- `meta_description` (159 zn.): „Therapy costs real money. Here is how to judge what you
  get for it, what a full course usually runs, and how to make each session earn its place
  in the budget."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `is therapy worth the money`
- poboczne: `how much does therapy cost`, `is therapy worth it`, `how many therapy sessions
  do I need`, `how to get the most out of therapy`, `is online therapy cheaper`,
  `therapy cost per session`
- intencja: mieszana, kosztowo-decyzyjna. Dwie grupy: osoba przed startem, która liczy
  budżet, i osoba w terapii od pół roku, która zaczyna liczyć, ile już wydała. Piszemy
  dla obu, ale ciężar na drugiej.
- luka: cały SERP (Grow Therapy, Headway, Mental Health Match, Project Healthy Minds)
  odpowiada wyłącznie na „ile kosztuje" i kończy listą tańszych opcji. **Nikt nie pokazuje
  drugiej strony równania**: co dostajesz za tę godzinę i jak to sprawdzić. Nasza teza:
  cena jest znana, wartość jest niemierzona, i to wartość da się poprawić.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): przelew co tydzień od siedmiu miesięcy, i nadal nie umiesz powiedzieć,
  na co poszedł, poza tym, że „chyba pomaga".
- H2: What therapy actually costs (and why the number moves so much)
  - datowane przedziały rynkowe z podanym źródłem i rokiem, ubezpieczenie kontra
    self-pay, sliding scale, grupowa; wszystko jako cudze dane rynkowe, nie nasza tabela
  - H3: The number that matters is the course, not the session
    (arytmetyka: liczba sesji razy stawka, na przykładzie oznaczonym jako przykład)
- H2: What the research says about how long it takes
  - dose-effect, uczciwie: mediana poprawy, duże różnice indywidualne, część osób nie
    poprawia się w ogóle
- H2: The part nobody prices: the other 167 hours
  - godzina w gabinecie kontra reszta tygodnia; praca między sesjami jako mnożnik wartości,
    z metaanalizami
- H2: How to raise the value of a session you already paid for
  - H3: Come with one topic, not with a week to summarize
  - H3: Leave with one thing to try
  - H3: Close the loop at the start of the next session
- H2: How to judge value over a quarter, not over one bad session
  - sekcja praktyczna: trzy markery, ten sam dzień miesiąca, porównanie kwartałów
- H2: When it is honest to say it is not worth it
  - bez namawiania: kiedy warto rozmawiać o zmianie formatu, częstotliwości albo osoby;
    zawsze kierunek „porozmawiaj o tym z terapeutą"
- H2: Frequently asked questions
  - H3: How much does therapy cost?
  - H3: Is therapy worth the money?
  - H3: How many therapy sessions do I need?
  - H3: Is online therapy cheaper than in person?
  - H3: How do I get more out of each therapy session?

**4. Karty funkcji** (werdykt: session-prep, summaries, mood-trends, goals, health-check)
- inline w „How to raise the value of a session you already paid for":
  `[FEATURE: session-prep | The prep card turns seven days into one screen, so the first fifteen minutes stop going on a warm up you are paying for.]`
- inline w „How to judge value over a quarter":
  `[FEATURE: summaries | A monthly summary reads the month back to you, which is the only fair way to compare it with the one before.]`
- blok przed FAQ:
  `[FEATURES: Getting your money's worth || goals | What you came for, with evidence collecting underneath it. || mood-trends | Months next to each other, not a feeling on a Sunday night. || workspace | The topics you flagged during the week, waiting for the next session.]`

**5. Mapa linkowania**
- `<a href="/journal/how-to-know-if-therapy-is-working">` anchor „how to know if therapy
  is working" (sekcja „How to judge value over a quarter")
- `<a href="/journal/what-to-do-between-therapy-sessions">` anchor „the week between
  sessions costs nothing"
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` anchor „come in with one
  topic instead of a summary of the week"
- `<a href="/journal/how-to-choose-a-therapist">` anchor „choosing a therapist" (09-04)
- **Landing partner:** `/pre-order/tracking-therapy-effectiveness` (anchor „tracking talk
  therapy effectiveness over time", jeden raz). Pomocniczo `/membership` anchorem „what the
  free trial includes", **bez podawania cen w tekście**.

**6. GEO**
- Cytowalna odpowiedź na `is therapy worth the money`, 60-80 słów: trzy warunki, w których
  wydatek zwraca się w sposób sprawdzalny (mierzysz to samo w czasie, przychodzisz
  z tematem, wychodzisz z jednym zadaniem), plus uczciwe „u części osób nie".
- Cytowalna arytmetyka kursu terapii: sesja razy liczba spotkań, z wyraźną etykietą, że to
  przedział rynkowy z podanego źródła i roku, a nie nasza wycena.

**7. Hero**
- „Abstrakcja" (`hero-02-abstrakcja.md`): dwa miękkie pola w palecie sand i mint, jedno
  nieco większe, sugestia wagi i porównania, zero symboli waluty.
- `hero_image_alt`: „Two soft shapes balanced against each other in sand and mint tones".

**8. Źródła do weryfikacji**
- Ceny: użyj **dwóch** aktualnych źródeł branżowych z podanym rokiem (np. przeglądy kosztów
  terapii publikowane przez Grow Therapy i Headway) i napisz wprost, że to dane rynkowe
  z USA, że różnią się między stanami i że ubezpieczenie zmienia obraz. Zero ekstrapolacji
  na inne kraje.
- „Poprawa zależy od liczby sesji, z malejącym przyrostem" → Howard i wsp., 1986,
  *American Psychologist* (dose-effect). Sprawdź liczby, zanim je podasz.
- „Część osób nie poprawia się, a część pogarsza" → Hansen, Lambert i Forman, 2002,
  *Clinical Psychology: Science and Practice*. Podaj delikatnie, z ramką „dlatego mierzymy".
- „Praca między sesjami wiąże się z lepszym wynikiem" → metaanalizy prac domowych w CBT,
  Kazantzis i wsp. (zweryfikuj: 2010 *Clinical Psychology: Science and Practice*
  albo 2016 *Cognitive Therapy and Research*).
- Arytmetyka 1 do 167 godzin to arytmetyka, nie cytat z badania.

**9. Czego NIE robić**
- Nie sugeruj rezygnacji z terapii ze względów finansowych i nie porównuj terapii z apką
  jako tańszą alternatywą. To złamałoby pozycjonowanie i zasadę YMYL.
- Nie podawaj cen MindSync. Od tego jest `/membership`.
- Nie powtarzaj metodyki pomiaru z `/journal/how-to-know-if-therapy-is-working`, korzystaj
  z niej przez link.
- Nie obiecuj oszczędności ani zwrotu z inwestycji w liczbach.

---

# 05. Journaling vs voice notes (HUB metody, klaster 2)

**1. Meta**
- `seo_url`: `journaling-vs-voice-notes`
- kategoria: `MindSync Tips` | `kolor`: `#3c67a5` | `planowana_data`: **2026-09-07**
- `tagi`: `["between-sessions", "journaling"]`
- H1: „Journaling vs Voice Notes: Which One Will You Actually Keep Doing?"
- `meta_title` (50 zn.): „Journaling vs Voice Notes: Which Works? | MindSync"
- `meta_description` (156 zn.): „Writing it down or saying it out loud? What the research
  supports, when talking beats a blank page, and how to pick the format you will actually
  keep using."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `journaling vs voice notes`
- poboczne: `is journaling or talking better`, `voice journaling`, `audio journal app`,
  `what to do if I hate journaling`, `does journaling actually work`,
  `talking to yourself out loud benefits`
- intencja: wybór metody. Człowiek wie, że „powinien" journalować, próbował, odbił się od
  pustej strony. Szuka pozwolenia na inny format i dowodu, że to nie jest gorsza wersja.
- luka: SERP dzieli się na artykuły o expressive writing (APA, Harvard Health, VA) i na
  landing page'e aplikacji do voice journalingu. **Nikt nie zestawia obu formatów uczciwie**,
  łącznie z tym, czego badania o mówieniu nie mówią. Nasz kąt: kryterium wyboru zależne od
  sytuacji, plus uczciwość o sile dowodów (efekty expressive writing są realne, ale małe
  i niejednorodne).

**3. Struktura (H2/H3)**
- Lead (40-60 słów): kupiłeś ładny notes, zapisałeś cztery strony w styczniu, i od tamtej
  pory otwierasz go tylko po to, żeby poczuć się winnym.
- H2: What the writing research actually found
  - protokół Pennebakera, metaanaliza z uczciwą wielkością efektu, zastrzeżenie
    o niejednorodności wyników
- H2: What we know about saying it out loud
  - wczesne badania z warunkiem mówionym, afektywne etykietowanie; jasne postawienie
    granicy: dowodów dla mowy jest mniej niż dla pisma i tak to opisujemy
- H2: The differences that actually matter in practice
  - H3: Speed (ile treści powstaje w tej samej minucie)
  - H3: Filter (pismo porządkuje, mowa wypuszcza)
  - H3: Friction (kiedy telefon w ręku wygrywa z notesem w szufladzie)
  - H3: Privacy and place (czego nie powiesz na głos w kuchni z domownikami)
- H2: Choose by situation, not by identity
  - H3: Right after a session: usually voice
  - H3: A loop you cannot break: usually writing
  - H3: Two minutes before bed: whichever needs no decision
  - H3: A conversation you rehearse in your head: voice, then read it back
- H2: The hybrid that survives a bad week
  - sekcja praktyczna: mów w tygodniu, czytaj i porządkuj raz na tydzień
- H2: What to do with the pile afterwards
  - materiał tylko wtedy ma wartość, gdy ktoś do niego wraca; jedno zdanie o przeglądzie
    przed sesją
- H2: Frequently asked questions
  - H3: Is journaling or talking better for mental health?
  - H3: Does voice journaling work?
  - H3: How long should I journal for?
  - H3: What do I do if I hate writing?
  - H3: Can I use voice notes instead of a journal?

**4. Karty funkcji** (werdykt: voice-notes, reflect, session-debrief, timeline)
- inline w „Choose by situation, not by identity":
  `[FEATURE: voice-notes | Say it out loud when it comes up, and the note is transcribed for you to review and accept later.]`
- inline w „The hybrid that survives a bad week":
  `[FEATURE: reflect | A guided reflection asks the follow up question a blank page never will, in text or out loud, whichever you have in you that day.]`
- blok przed FAQ (opcjonalny):
  `[FEATURES: Keeping the material usable || session-debrief | The five minutes right after a session, while it is still warm. || timeline | Notes, sessions and check-ins in one place you can filter later. || workspace | The parts worth raising next time, already on your agenda.]`

**5. Mapa linkowania**
- `<a href="/journal/what-to-do-between-therapy-sessions">` anchor „a weekly rhythm between
  sessions"
- `<a href="/journal/how-to-remember-what-you-talk-about-in-therapy">` anchor „capture the
  session while it is still fresh"
- `<a href="/journal/how-to-identify-emotional-triggers">` anchor „catching a reaction in
  the moment"
- `[LINK-LATER: racing-thoughts-at-night | when the loop shows up at one in the morning]`
- **Landing partner:** `/pre-order/deep-emotional-analysis` (anchor „a deeper read on what
  you keep coming back to", jeden raz). Pomocniczo `/features`.

**6. GEO**
- Cytowalna odpowiedź na `is journaling or talking better`, 55-75 słów: oba mają wsparcie,
  pismo ma więcej badań, wybór zależy od sytuacji, a najlepszy format to ten, który
  przetrwa czwarty tydzień.
- Cytowalna tabela decyzyjna zapisana jako lista `ul` (RichText-safe, zero `table`):
  sytuacja, rekomendowany format, powód. Cztery pozycje, 60-80 słów.

**7. Hero**
- „Codzienny moment": notes i telefon leżące obok siebie na kocu, dłoń poza kadrem, ciepłe
  światło popołudnia. Bez ekranu apki.
- `hero_image_alt`: „A notebook and a phone side by side on a blanket in warm afternoon
  light".

**8. Źródła do weryfikacji**
- „Pisanie o trudnych doświadczeniach wiąże się z poprawą wskaźników zdrowia" → Pennebaker
  i Beall, 1986, *Journal of Abnormal Psychology*; metaanaliza Frattaroli, 2006,
  *Psychological Bulletin*. **Zastrzeżenie obowiązkowe:** wielkości efektu są małe,
  a wyniki niejednorodne. Podaj to wprost, to jest nasz wyróżnik wobec konkurencji.
- „Warunek mówiony dawał efekty zbliżone do pisanego" → wczesne badania z warunkiem
  mówionym (np. Donnelly i Murray, 1991, *Journal of Social and Clinical Psychology*,
  albo Esterling i wsp., 1994). Zweryfikuj i **nie uogólniaj**: napisz, ile badań to było.
- „Nazwanie emocji zmienia sposób ich przetwarzania" → Lieberman i wsp., 2007,
  *Psychological Science*. Opisuj mechanizm, nie obiecuj efektu terapeutycznego.
- Jakiekolwiek liczby o tempie mowy kontra pisma podawaj tylko ze źródłem, inaczej opisz
  różnicę jakościowo.

**9. Czego NIE robić**
- Nie sprzedawaj voice notes jako „lepszego journalingu". Wpis ma być uczciwym
  porównaniem, inaczej traci wiarygodność i pozycję.
- Nie obiecuj efektów zdrowotnych z samego pisania ani mówienia.
- Nie wchodź w metodykę check-inów i trendów (to `/journal/why-mood-tracking-stops-working`).
- Nie opisuj przebiegu transkrypcji technicznie ani nie obiecuj dokładności w procentach.

---

# 04. How to actually do your therapy homework

**1. Meta**
- `seo_url`: `how-to-do-therapy-homework`
- kategoria: `Therapy` | `kolor`: `#ff9f8a` | `planowana_data`: **2026-09-08**
- `tagi`: `["between-sessions", "homework"]`
- H1: „How to Actually Do Your Therapy Homework (When the Week Eats It)"
- `meta_title` (51 zn.): „How to Actually Do Your Therapy Homework | MindSync"
- `meta_description` (151 zn.): „Most therapy homework never gets done. Here is why that
  happens, and a way to make the between-session task actually fit into the week you really
  have."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `how to do therapy homework`
- poboczne: `therapy homework not doing it`, `why don't I do my therapy homework`,
  `cbt homework examples`, `what happens if you don't do therapy homework`,
  `therapy homework ideas`, `how to remember therapy homework`
- intencja: wina plus praktyka. Człowiek zgadza się w gabinecie, wychodzi z zadaniem
  i wraca po tygodniu z niczym. Ton: bez moralizowania, mechanizm zamiast dyscypliny.
- luka: SERP to strony praktyk i arkusze PDF z zadaniami („20 CBT worksheets"). Badania
  o niewykonywaniu zadań istnieją i są mocne, ale w treściach dla pacjentów nie występują.
  **Nikt nie pisze o tym z perspektywy klienta**, tylko o tym z perspektywy terapeuty.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): w gabinecie brzmiało prosto, w środę wieczorem zostało już tylko
  poczucie, że znowu nie zrobiłeś tego, na co się zgodziłeś.
- H2: How common this is (and what the numbers really say)
  - odsetki niewykonywania zadań w CBT z badań, z zaznaczeniem, że to szacunki z różnych
    prób i metod pomiaru
- H2: Why the task dies between Tuesday and Sunday
  - H3: It was never specific enough to start
  - H3: It cost more than it looked like it would cost
  - H3: Avoidance is the point (zadanie dotyka dokładnie tego, czego unikasz)
  - H3: Nobody was going to read it
- H2: What the research says helps
  - jasne uzasadnienie zadania, planowanie kiedy i gdzie (implementation intentions),
    omówienie zadania na następnej sesji; z metaanalizami i uczciwym zastrzeżeniem
- H2: Make the task smaller than your worst day
  - H3: The if-then version of the task
  - H3: The two minute floor
  - H3: One place where it lives
- H2: What to do when you did not do it
  - H3: Bring the failure as data, not as a confession
  - H3: The three questions worth answering before the next session
  - H3: When to renegotiate the task with your therapist
- H2: A week that fits a real week
  - sekcja praktyczna: kiedy zapisać zadanie, kiedy je zrobić, kiedy spojrzeć wstecz
- H2: Frequently asked questions
  - H3: What is therapy homework?
  - H3: Why can't I do my therapy homework?
  - H3: What happens if I don't do my therapy homework?
  - H3: How much therapy homework is normal?
  - H3: Should I tell my therapist I did not do the homework?

**4. Karty funkcji** (werdykt: homework, smart-reminders, workspace, session-prep, check-ins)
- inline w „Make the task smaller than your worst day":
  `[FEATURE: homework | What you agreed to try lands on your home screen as a to do for today, instead of surfacing guiltily at the next session.]`
- inline w „A week that fits a real week":
  `[FEATURE: smart-reminders | A nudge at the moment that fits your week, with a separate switch for every type, so you can keep one and turn the rest off.]`
- blok przed FAQ:
  `[FEATURES: Turning an agreement into something that happens || workspace | The task, the topics and the threads in one place between sessions. || check-ins | A one minute rating that shows what the task actually cost you. || session-prep | The honest report ready before you walk in.]`

**5. Mapa linkowania**
- `<a href="/journal/what-to-do-between-therapy-sessions">` anchor „a weekly rhythm between
  sessions" (pillar klastra 2)
- `<a href="/journal/which-coping-skills-actually-work">` anchor „test whether the exercise
  does anything for you"
- `<a href="/journal/journaling-vs-voice-notes">` anchor „say it instead of writing it"
  (opublikowany 09-07)
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` anchor „bring the honest
  report to the next session"
- **Landing partner:** `/features` (anchor „homework and to dos"). Pomocniczo
  `/pre-order/track-interventions` (anchor „see whether the small things actually help",
  jeden raz).

**6. GEO**
- Cytowalna odpowiedź na `why don't I do my therapy homework`, 50-70 słów: cztery powody
  z badań i z praktyki, każdy w jednym zdaniu, bez moralizowania.
- Cytowalny wzór zadania w formie „if X then Y", 40-60 słów, gotowy do przepisania,
  z jednym konkretnym przykładem.

**7. Hero**
- „Codzienny moment": karteczka z jednym odręcznym punktem przyklejona do lodówki, poranne
  światło, tekst nieczytelny.
- `hero_image_alt`: „A single handwritten note on a fridge door in morning light".

**8. Źródła do weryfikacji**
- „Niewykonywanie zadań między sesjami dotyczy dużej części klientów" → przegląd
  w *JMIR Mental Health*, 2017, „Supporting Homework Compliance in Cognitive Behavioural
  Therapy" (rekord PMC5481663). Zweryfikuj autorów i przedział procentowy, i napisz,
  z jakich prób pochodzi.
- „Wykonywanie zadań wiąże się z lepszym wynikiem terapii" → Kazantzis, Whittington
  i Dattilio, 2010, *Clinical Psychology: Science and Practice*, albo Kazantzis i wsp.,
  2016, *Cognitive Therapy and Research*. Podaj wielkość efektu tylko po weryfikacji.
- „Plany typu jeśli-to zwiększają szansę wykonania zamierzonego działania" → metaanaliza
  Gollwitzer i Sheeran, 2006, *Advances in Experimental Social Psychology*. Zweryfikuj
  wielkość efektu, zanim podasz liczbę.
- Komentarz praktyczny Beck Institute o statusie prac domowych w CBT możesz przywołać jako
  głos praktyków, wyraźnie oddzielony od metaanaliz.

**9. Czego NIE robić**
- Zero moralizowania i zero słowa „lazy". Niewykonanie zadania to informacja, nie wada
  charakteru.
- Nie wymyślaj zadań terapeutycznych za terapeutę i nie podawaj gotowych protokołów
  ekspozycji. Przykłady mają być neutralne i lekkie.
- Nie obiecuj, że przypomnienia zbudują nawyk. `streaks` jest planned, więc żadnych serii
  ani odznak.
- Nie wchodź w metodę testowania technik (to `/journal/which-coping-skills-actually-work`).

---

# 06. Racing thoughts at night (HUB klastra 5)

**1. Meta**
- `seo_url`: `racing-thoughts-at-night`
- kategoria: `Therapy` | `kolor`: `#339499` | `planowana_data`: **2026-09-09**
- `tagi`: `["modern-life", "sleep"]`
- H1: „Racing Thoughts at Night: Why Your Brain Waits Until You Lie Down"
- `meta_title` (47 zn.): „How to Stop Racing Thoughts at Night | MindSync"
- `meta_description` (157 zn.): „Your body is tired and your head will not stop. What
  research says about racing thoughts at bedtime, and a wind-down that gives the thoughts
  somewhere to go."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `how to stop racing thoughts at night`
- poboczne: `why do my thoughts race at night`, `can't sleep because of overthinking`,
  `why is my anxiety worse at night`, `how to quiet your mind before bed`,
  `brain won't shut off at night`, `what to do when you can't sleep because of stress`
- intencja: doraźna ulga, często o 1 w nocy, na telefonie. Pierwsza sekcja musi dawać
  wyjaśnienie, druga konkret. Bardzo wysoka intencja mobilna, więc krótkie akapity
  i skanowalne nagłówki.
- luka: SERP to Sleep Foundation, Calm i strony klinik, wszyscy powtarzają „sleep hygiene,
  no screens, breathe". Badania o **racing thoughts jako zjawisku odrębnym od zamartwiania
  się i ruminacji** w tych treściach nie występują, a to jest ciekawe i użyteczne
  rozróżnienie. Do tego nikt nie mówi wprost, kiedy odesłać czytelnika po CBT-I.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): ciało padnięte, światło zgaszone, i nagle rozmowa sprzed trzech dni
  wraca w wersji reżyserskiej.
- H2: Racing thoughts are not the same as worry
  - badania, które rozdzielają racing thoughts, ruminację i zamartwianie się; dlaczego to
    rozróżnienie zmienia to, co pomaga
- H2: Why the volume goes up when the lights go down
  - H3: Nothing left to distract you
  - H3: Cognitive arousal keeps the system online
  - H3: A tired brain regulates thoughts worse, not better
- H2: What actually helps, and what only sounds like it helps
  - H3: Getting the loop out of your head onto something else
  - H3: Constructive worry, done earlier in the evening
  - H3: Getting out of bed (dlaczego to nie jest porażka)
  - H3: What to skip (trying harder to fall asleep, scrolling to get sleepy)
- H2: A wind-down that takes ten minutes
  - sekcja praktyczna: sekwencja krok po kroku, z rozróżnieniem „przed łóżkiem"
    i „w łóżku o drugiej w nocy"
- H2: The daytime half of the fix
  - jedno zdanie o tym, że nocna głowa zwykle domyka dzień, plus zapisywanie w ciągu dnia
- H2: When this is worth taking to a professional
  - uczciwe skierowanie: przewlekła bezsenność ma leczenie pierwszego wyboru i jest nim
    CBT-I; bez diagnozowania i bez straszenia
- H2: Frequently asked questions
  - H3: Why do my thoughts race at night?
  - H3: How do I stop overthinking at night?
  - H3: Why does my anxiety get worse at night?
  - H3: Should I get out of bed if I can't sleep?
  - H3: Does writing down your thoughts before bed help you sleep?

**4. Karty funkcji** (werdykt: reflect, check-ins, voice-notes, mood-trends, daily-affirmation)
- inline w „Getting the loop out of your head onto something else":
  `[FEATURE: reflect | When the loop will not close, a guided reflection gives it somewhere to go, in text or out loud, without turning on a lamp and finding a pen.]`
- inline w „The daytime half of the fix":
  `[FEATURE: check-ins | Sleep is one of the areas you can rate in under a minute, which is how you find out what your bad nights have in common.]`
- blok przed FAQ (opcjonalny):
  `[FEATURES: Giving the night thoughts somewhere to go || voice-notes | Say it instead of writing it, and read it back in daylight. || mood-trends | Weeks of sleep ratings next to the rest of your week. || reflect | The guided version, for nights when you cannot name what is keeping you up.]`

**5. Mapa linkowania**
- `<a href="/journal/regulate-nervous-system-between-therapy-sessions">` anchor „settle the
  body first, then the head"
- `<a href="/journal/journaling-vs-voice-notes">` anchor „writing it down or saying it out
  loud" (opublikowany 09-07)
- `<a href="/journal/which-coping-skills-actually-work">` anchor „test one wind-down at
  a time"
- `[LINK-LATER: sunday-scaries | the Sunday night version of the same thing]`
- **Landing partner:** `/features`. Pomocniczo `/pre-order/track-interventions` (anchor
  „find out which wind-down actually does anything for you", jeden raz).

**6. GEO**
- Cytowalna odpowiedź na `why do my thoughts race at night`, 55-75 słów: trzy mechanizmy
  w jednym akapicie, z rozróżnieniem racing thoughts od zamartwiania się.
- Cytowalny protokół „ten minutes before bed", 50-70 słów, w krokach numerowanych, plus
  osobne dwa zdania „what to do if you are already awake at 2 a.m.".

**7. Hero**
- „Codzienny moment": nocna szafka z lampką o ciepłym świetle, notes i szklanka wody,
  bez osoby w kadrze, granatowe tło stonowane do palety.
- `hero_image_alt`: „A bedside table with a warm lamp, a glass of water and a notebook at
  night".

**8. Źródła do weryfikacji**
- „Racing thoughts przy zasypianiu wiążą się z nasileniem bezsenności silniej niż
  ruminacja i zamartwianie się" → badanie w *Comprehensive Psychiatry*, 2021,
  „Investigating racing thoughts in insomnia". Zweryfikuj autorów i sformułowanie wniosku.
- „Pobudzenie poznawcze tłumaczy więcej wariancji zaburzeń snu niż pobudzenie somatyczne"
  → praca w *Scientific Reports*, 2025, o mediacyjnej roli cognitive arousal. Zweryfikuj
  autorów, rok i to, czy wniosek nie jest nadinterpretacją.
- „Spisanie listy zadań przed snem skróciło czas zasypiania" → Scullin i wsp., 2018,
  *Journal of Experimental Psychology: General*. Podaj liczbę minut tylko po weryfikacji,
  i dopisz, że próba była mała.
- „CBT-I jest leczeniem pierwszego wyboru w przewlekłej bezsenności" → wytyczne American
  College of Physicians, Qaseem i wsp., 2016, *Annals of Internal Medicine*. To zdanie
  jest obowiązkowe w sekcji o profesjonalnej pomocy.

**9. Czego NIE robić**
- Zero porad o lekach nasennych, melatoninie i suplementach. Nawet „niektórzy stosują".
- Zero diagnozowania bezsenności, zaburzeń lękowych i ADHD. Racing thoughts w treści
  to zjawisko potoczne, nie objaw jednostki chorobowej.
- Nie obiecuj lepszego snu dzięki apce. Apka daje miejsce na myśli i obraz tygodnia, tyle.
- Nie dubluj wpisu o regulacji układu nerwowego. Jeden akapit i link.

---

# 07. The Sunday scaries

**1. Meta**
- `seo_url`: `sunday-scaries`
- kategoria: `Therapy` | `kolor`: `#1f3d38` | `planowana_data`: **2026-09-10**
- `tagi`: `["modern-life", "work-stress"]`
- H1: „The Sunday Scaries: Why Sunday Evening Feels Like That, and What Shortens It"
- `meta_title` (41 zn.): „How to Beat the Sunday Scaries | MindSync"
- `meta_description` (151 zn.): „The Sunday scaries are anticipatory anxiety with
  a schedule. Why Sunday evening does this, what the surveys show, and what actually
  shortens the dread."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `how to get rid of the sunday scaries`
- poboczne: `what are the sunday scaries`, `why do I get anxious on sunday night`,
  `sunday night dread`, `sunday scaries anxiety`, `how to enjoy sunday evening`,
  `work anxiety on sunday`
- intencja: rozpoznanie plus ulga, w niedzielę wieczorem. Duży wolumen sezonowy tygodniowo,
  bardzo wysoka intencja mobilna. Odbiorca szeroki (wellbeing), więc to nasz top of funnel.
- luka: SERP to Cleveland Clinic, Asana, Fast Company i raporty ankietowe firm HR. Wszyscy
  powtarzają procenty z ankiet i dają radę „zaplanuj coś miłego w niedzielę". **Nikt nie
  rozróżnia trzech różnych rzeczy** pod jedną nazwą: przewidywanego stresu przed konkretną
  sprawą, braku regeneracji w weekend, i sygnału, że praca jest nie do wytrzymania. To jest
  nasz kąt, plus badania o psychological detachment, których w tym SERP-ie nie ma.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): jest wpół do ósmej wieczorem, technicznie masz jeszcze cztery godziny
  wolnego, i już żadnej z nich nie umiesz wykorzystać.
- H2: What the Sunday scaries actually are
  - definicja robocza jako lęk antycypacyjny; jasne oznaczenie, że popularne procenty
    pochodzą z ankiet firm, nie z badań recenzowanych
- H2: Three different things wearing the same name
  - H3: A specific dread (jedno spotkanie, jedna rozmowa, jedno zadanie)
  - H3: A recovery problem (weekend, który nie odłączył cię od pracy)
  - H3: A signal about the job itself
  - to rozróżnienie decyduje o tym, co pomoże, i jest osią wpisu
- H2: Why recovery matters more than relaxing
  - badania nad psychological detachment; dlaczego weekend spędzony „w gotowości" nie
    regeneruje, nawet jeśli nic nie robisz
- H2: What shortens the dread on Sunday evening
  - H3: Name the actual item (zwykle jest jeden, nie „cały tydzień")
  - H3: Friday's fifteen minutes (dlaczego to piątek naprawia niedzielę)
  - H3: Sunday plan that starts, not ends, in the evening
  - H3: The two hour buffer before bed
- H2: When it is not the Sunday scaries
  - uczciwie: jeśli dread nie znika w poniedziałek do południa, jeśli ciągnie się przez
    tydzień, jeśli towarzyszy mu bezsenność, to temat na rozmowę z profesjonalistą;
    zero diagnozowania
- H2: Tracking it for a month (because you will not remember)
  - sekcja praktyczna: ocena niedzielnego wieczoru w skali, jedno zdanie o tym, co je
    napędziło, przegląd po miesiącu
- H2: Frequently asked questions
  - H3: What are the Sunday scaries?
  - H3: Why do I get anxious on Sunday nights?
  - H3: How do I stop the Sunday scaries?
  - H3: Do the Sunday scaries mean I hate my job?
  - H3: Is it normal to feel sick on Sunday evening?

**4. Karty funkcji** (werdykt: check-ins, reflect, mood-trends, voice-notes, workspace)
- inline w „Name the actual item":
  `[FEATURE: reflect | A guided reflection walks you from a heavy Sunday feeling to the one specific thing underneath it, which is usually smaller than the mood suggested.]`
- inline w „Tracking it for a month":
  `[FEATURE: check-ins | Rate Sunday evening the same way every week, and after a month you can see whether it is the job, the week or the weekend.]`
- blok przed FAQ (opcjonalny):
  `[FEATURES: Making Sunday evening readable || mood-trends | Weeks side by side, so you can tell a rough patch from a pattern. || voice-notes | Say the thing you are dreading out loud on the walk, before it gets bigger. || workspace | Whatever this turns into, waiting for your next session.]`

**5. Mapa linkowania**
- `<a href="/journal/racing-thoughts-at-night">` anchor „when it follows you to bed"
  (opublikowany 09-09)
- `<a href="/journal/digital-burnout-brain-rewiring">` anchor „the wider version of this,
  when the whole week feels flat"
- `<a href="/journal/how-to-identify-emotional-triggers">` anchor „the pattern underneath
  the dread"
- `<a href="/journal/regulate-nervous-system-between-therapy-sessions">` anchor „settle
  the body when the dread is physical"
- **Landing partner:** `/pre-order/understand-behavioural-patterns` (anchor „understand the
  pattern underneath it", jeden raz). Pomocniczo `/features`.

**6. GEO**
- Cytowalna definicja Sunday scaries, 40-55 słów, neutralna klinicznie, z jasnym
  zaznaczeniem, że to nie jest jednostka diagnostyczna.
- Cytowalna odpowiedź na `how to stop the sunday scaries`, 60-80 słów, w formie czterech
  kroków z ramami czasowymi (piątek, sobota, niedziela po południu, niedziela wieczorem).

**7. Hero**
- „Codzienny moment": kubek i otwarte okno o zmierzchu w niedzielę, złote światło
  przechodzące w granat, spokojna kompozycja bez dramaturgii.
- `hero_image_alt`: „A cup by an open window at dusk on a Sunday evening".

**8. Źródła do weryfikacji**
- Procenty z ankiet (np. 80% pracowników, 73% z objawami fizycznymi) **zawsze** z nazwą
  firmy, rokiem i liczebnością próby, i zawsze z ramką „to ankieta komercyjna, nie badanie
  recenzowane". Jeśli nie znajdziesz liczebności próby, nie podawaj procentu.
- „Psychologiczne odłączenie się od pracy w czasie wolnym wiąże się z lepszym samopoczuciem
  i regeneracją" → Sonnentag i Fritz, 2007, *Journal of Occupational Health Psychology*
  (Recovery Experience Questionnaire), plus nowszy przegląd, jeśli potwierdzisz.
- „Zamartwianie się pełni funkcję unikania" → Borkovec, Alcaine i Behar, 2004, model
  unikania w zamartwianiu. Zweryfikuj rozdział i tom.
- ⛔ **Nie używaj statystyk o zawałach w poniedziałek.** To straszenie i wątpliwa
  interpretacja, sprzeczna z regułami YMYL tego bloga.

**9. Czego NIE robić**
- Nie doradzaj rzucenia pracy ani zmiany pracodawcy. Wpis daje rozróżnienie, decyzja jest
  czytelnika.
- Nie nazywaj Sunday scaries zaburzeniem ani objawem depresji. To zjawisko potoczne.
- Nie dubluj mechanizmu przeciążenia cyfrowego (to `/journal/digital-burnout-brain-rewiring`).
- Zero alkoholu jako „sposobu na niedzielę", nawet w formie żartu.

---

# 08. How to stop doomscrolling

**1. Meta**
- `seo_url`: `how-to-stop-doomscrolling`
- kategoria: `Therapy` | `kolor`: `#3c67a5` | `planowana_data`: **2026-09-11**
- `tagi`: `["modern-life", "attention"]`
- H1: „How to Stop Doomscrolling (Without Deleting Everything)"
- `meta_title` (45 zn.): „How to Stop Doomscrolling for Good | MindSync"
- `meta_description` (156 zn.): „You did not decide to read forty minutes of bad news. Here
  is what doomscrolling does, why the loop is sticky, and how to swap it for something that
  helps."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `how to stop doomscrolling`
- poboczne: `what is doomscrolling`, `why do I doomscroll`, `doomscrolling effects`,
  `how to stop scrolling at night`, `doomscrolling anxiety`,
  `how to break the phone habit before bed`
- intencja: świadomy problem, chęć konkretu. Człowiek wie, jak to się nazywa, próbował
  timerów i nie zadziałało. Nie potrzebuje kolejnej listy ustawień telefonu.
- luka: SERP to Cleveland Clinic, Calm i dziesiątki list „10 tips" z tym samym zestawem
  (grayscale, app limits, phone in another room). **Nikt nie pokazuje, po czym poznać, że
  to działa u ciebie**, i nikt nie tłumaczy mechanizmu nietolerancji niepewności, który
  wyjaśnia, dlaczego przewijanie **wydaje się** produktywne.
- **Granica kanibalizacji:** `/journal/digital-burnout-brain-rewiring` trzyma temat
  przeciążenia cyfrowego i uwagi. Ten wpis trzyma wyłącznie pętlę przewijania złych
  wiadomości: mechanizm, przerwanie, podmiana. Bez powtarzania sekcji o uwadze i wypaleniu,
  jeden akapit i link.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): wziąłeś telefon, żeby sprawdzić godzinę, i czterdzieści minut później
  wiesz wszystko o katastrofie, na którą nie masz wpływu.
- H2: What doomscrolling actually is
  - definicja robocza, dane o rozpowszechnieniu oznaczone jako ankieta, nie badanie
- H2: Why the loop is stickier than other phone habits
  - H3: Negativity bias (dlaczego złe wiadomości wygrywają uwagę)
  - H3: Intolerance of uncertainty (czytanie dalej jako fałszywe domykanie)
  - H3: Variable reward (dlaczego kciuk nie chce przestać)
- H2: What the research links it to
  - przegląd zakresowy i badania nad lękiem egzystencjalnym; uczciwe zastrzeżenie: to są
    głównie badania korelacyjne i przekrojowe, więc nie pisz o przyczynie
- H2: Why app limits alone rarely hold
  - moment przechwycenia jest wcześniejszy niż moment odblokowania telefonu
- H2: The swap, not the ban
  - H3: Name the trigger moment (nuda, złość, unikanie, zasypianie)
  - H3: Pick a competing behaviour that uses the same hand
  - H3: Give the feeling somewhere else to go
  - H3: Keep one deliberate news window
- H2: Run it as a two week test
  - sekcja praktyczna: jedna zmiana, jedna miara, dwa tygodnie, porównanie tygodni;
    odesłanie do wpisu o testowaniu technik zamiast powtarzania metody
- H2: Frequently asked questions
  - H3: What is doomscrolling?
  - H3: Why do I doomscroll?
  - H3: How do I stop doomscrolling at night?
  - H3: Is doomscrolling bad for your mental health?
  - H3: How long does it take to break the doomscrolling habit?

**4. Karty funkcji** (werdykt: check-ins, mood-trends, reflect, personal-bio, smart-reminders)
- inline w „Give the feeling somewhere else to go":
  `[FEATURE: reflect | Two minutes of guided reflection uses the same hand and the same phone, and it gives the restlessness a target instead of a feed.]`
- inline w „Run it as a two week test":
  `[FEATURE: check-ins | Rate the two things you expect to change, at the same time every day, so the result is something you can read rather than argue about.]`
- blok przed FAQ (opcjonalny):
  `[FEATURES: Seeing whether the swap works || mood-trends | Two weeks next to each other, so a good day stops passing for progress. || summaries | The week read back to you, instead of recalled on a Sunday. || voice-notes | Say what set it off, in the moment, before it turns into an hour.]`

**5. Mapa linkowania**
- `<a href="/journal/digital-burnout-brain-rewiring">` anchor „what constant input does to
  attention" (jeden akapit, nie sekcja)
- `<a href="/journal/racing-thoughts-at-night">` anchor „scrolling in bed, and what
  replaces it" (opublikowany 09-09)
- `<a href="/journal/which-coping-skills-actually-work">` anchor „run it as a two week
  test"
- `<a href="/journal/sunday-scaries">` anchor „Sunday evening, when the scroll gets
  longest" (opublikowany 09-10)
- **Landing partner:** `/pre-order/track-interventions` (anchor „see whether the swap
  actually changes anything", jeden raz). Pomocniczo `/features`.

**6. GEO**
- Cytowalna definicja doomscrollingu, 35-50 słów, bez dramatyzowania.
- Cytowalna odpowiedź na `how to stop doomscrolling`, 60-80 słów, w formie czterech kroków
  opartych na podmianie zachowania, nie na zakazie. Musi działać wyjęta z kontekstu.

**7. Hero**
- „Abstrakcja": pionowy, miękki gradient przypominający nieskończoną taśmę, w palecie mint
  i sand, urwany u dołu jasnym polem. Zero telefonu w kadrze, zero tekstu.
- `hero_image_alt`: „A soft vertical gradient fading into light, a scroll that finally
  stops".

**8. Źródła do weryfikacji**
- „Doomscrolling wiąże się z gorszym samopoczuciem, lękiem i gorszym snem" → przegląd
  zakresowy z 2025 w *Mental Health and Digital Technologies* (Emerald). Zweryfikuj
  autorów i **napisz wprost, że to badania korelacyjne**.
- „Doomscrolling wiąże się z lękiem egzystencjalnym i pesymizmem" → praca z 2024
  (Computers in Human Behavior Reports, „Doomscrolling evokes existential anxiety").
  Zweryfikuj autorów, rok i projekt badania.
- „Nietolerancja niepewności pośredniczy w związku doomscrollingu z lękiem" → badanie
  z 2024 w *Personality and Individual Differences*. Zweryfikuj.
- „Ludzie reagują silniej na informacje negatywne niż pozytywne" → Rozin i Royzman, 2001,
  *Personality and Social Psychology Review*, albo Soroka, Fournier i Nir, 2019, *PNAS*
  (reakcje psychofizjologiczne na wiadomości). Wybierz jedno i zweryfikuj.
- Rozpowszechnienie (np. odsetek dorosłych, którzy regularnie doomscrollują) podawaj jako
  ankietę firmy badawczej z rokiem, nigdy jako wynik badania naukowego.

**9. Czego NIE robić**
- Nie strasz kortyzolem ani „uszkodzeniem mózgu". Zero neuro-mitów, nawet chwytliwych.
- Nie doradzaj śledzenia albo nieśledzenia konkretnych tematów i mediów. Zero polityki.
- Nie powtarzaj sekcji z `/journal/digital-burnout-brain-rewiring`.
- Nie sugeruj, że MindSync zastąpi telefon albo social media. Karta jest o podmianie
  zachowania, nie o cyfrowym detoksie.

---

# 09. Tracking whether a new medication is helping (duet → /pre-order/mood-on-antidepressants)

> **To jest najostrożniejszy wpis w partii.** Temat leków = pełny YMYL. Autor pisze
> wyłącznie o **obserwowaniu i raportowaniu**, nigdy o decyzjach terapeutycznych. Każda
> sekcja kończy się kierunkiem do osoby przepisującej lek. Jeśli którekolwiek zdanie da się
> przeczytać jako poradę medyczną, wypada z tekstu.

**1. Meta**
- `seo_url`: `tracking-mood-on-antidepressants`
- kategoria: `Therapy` | `kolor`: `#e8af0a` | `planowana_data`: **2026-09-12**
- `tagi`: `["measurement", "medication"]`
- H1: „How to Track Whether a New Antidepressant Is Helping"
- `meta_title` (51 zn.): „Is Your Antidepressant Working? Track It | MindSync"
- `meta_description` (156 zn.): „Starting a new antidepressant means weeks of guessing.
  Here is how to track sleep, energy and side effects so your prescriber gets facts instead
  of a shrug."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `how to know if your antidepressant is working`
- poboczne: `how long do antidepressants take to work`, `signs your antidepressant is
  working`, `what to track when starting an antidepressant`,
  `what to tell your doctor at a medication follow up`, `antidepressant side effects first
  weeks`, `feeling worse on antidepressants at first`
- intencja: niepewność w oknie 2-8 tygodni od startu leku. Człowiek nie wie, czy to,
  co czuje, to efekt leku, efekt tygodnia, czy nic. Bardzo wysoka wrażliwość, bardzo wysoka
  gotowość do zapisywania czegokolwiek, co da odpowiedź.
- luka: SERP należy do GoodRx, Healthline, ChoosingTherapy i Talkspace. Wszyscy odpowiadają
  na „ile to trwa" i wymieniają objawy poprawy. **Nikt nie daje metody obserwacji**, którą
  pacjent może przynieść na wizytę kontrolną, mimo że pomiar objawów przy leczeniu
  depresji ma własną literaturę (measurement-based care). To jest nasz konkret i nasz
  różnicujący klaster.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): trzeci tydzień, i codziennie zadajesz sobie to samo pytanie, na które
  pamięć z ostatnich dni odpowiada za każdym razem inaczej.
- H2: Why this is so hard to judge from memory
  - pamięć nastroju, dobre i złe dni, brak punktu odniesienia sprzed startu leku
- H2: What the timelines actually look like
  - okna czasowe z badań, uczciwie i z zastrzeżeniem indywidualnych różnic; wczesna
    poprawa jako sygnał prognostyczny, opisana ostrożnie
- H2: What is worth writing down (and what is noise)
  - H3: Sleep, appetite and energy usually move first
  - H3: The activity test (co znowu robisz, czego nie robiłeś)
  - H3: Side effects, with dates
  - H3: One line of context (bo tydzień z przeprowadzką to nie jest ten sam tydzień)
- H2: A simple two minute record
  - sekcja praktyczna: ta sama skala, ta sama pora, trzy markery plus lista działań
    niepożądanych z datami; wprost: to nie jest narzędzie diagnostyczne
- H2: How to turn four weeks into one page for your appointment
  - co powiedzieć na wizycie kontrolnej, w jakiej kolejności, i czego nie pomijać
  - **jedno zdanie obowiązkowe:** raport jest materiałem do rozmowy, nie podstawą do
    zmiany dawki
- H2: The honest caveats
  - efekt placebo i naturalny przebieg objawów; pomiar zmienia to, co mierzysz; część osób
    nie odpowiada na pierwszy lek i to jest znane w badaniach, więc nie jest to porażka
- H2: Frequently asked questions
  - H3: How long do antidepressants take to work?
  - H3: How do I know if my antidepressant is working?
  - H3: What should I track when starting a new medication?
  - H3: Is it normal to feel worse in the first weeks?
  - H3: What should I tell my doctor at the follow up appointment?

**4. Karty funkcji** (werdykt: check-ins, mood-trends, summaries, timeline)
- inline w „A simple two minute record":
  `[FEATURE: check-ins | Rate sleep, energy and the two things you are watching, in under a minute, at the same time every day.]`
- inline w „How to turn four weeks into one page":
  `[FEATURE: summaries | A weekly summary turns scattered entries into something you can actually read out at a follow up appointment.]`
- blok przed FAQ (opcjonalny):
  `[FEATURES: Four weeks you can actually look back on || mood-trends | Weeks charted next to each other, instead of a memory of yesterday. || timeline | Every note and check-in in one place, with dates attached. || check-ins | The two minute record that makes the rest possible.]`

**5. Mapa linkowania**
- `<a href="/journal/why-mood-tracking-stops-working">` anchor „tracking that survives past
  week two"
- `<a href="/journal/how-to-know-if-therapy-is-working">` anchor „the same question, asked
  about therapy"
- `<a href="/journal/which-coping-skills-actually-work">` anchor „the one variable rule"
  (jedno zdanie, w kontekście: przy lekach zmienną zmienia lekarz, nie ty)
- **Landing partner:** `/pre-order/mood-on-antidepressants` (duet, anchor „tracking your
  mood on antidepressants", jeden raz, naturalnie w zdaniu). Pomocniczo `/features`.

**6. GEO**
- Cytowalna odpowiedź na `how long do antidepressants take to work`, 50-70 słów, z podanym
  źródłem i wyraźnym „to zależy, a decyzje należą do osoby przepisującej".
- Cytowalna lista „what to track", 60-80 słów, gotowa do przepisania, z datami działań
  niepożądanych jako osobnym punktem.

**7. Hero**
- „Codzienny moment": kalendarz ścienny z kilkoma miękkimi zaznaczeniami i kubek na blacie,
  poranne światło. **Zero tabletek, blistrów i opakowań leków w kadrze** (zakaz z brand doc).
- `hero_image_alt`: „A wall calendar with a few soft marks and a cup on the counter in
  morning light".

**8. Źródła do weryfikacji**
- „Pełny efekt leku pojawia się zwykle w oknie kilku tygodni" → podaj wytyczne albo
  przegląd z rokiem, nie blog komercyjny. Kandydaci: wytyczne NICE dla depresji (2022)
  albo przegląd w recenzowanym czasopiśmie. Zweryfikuj i zacytuj dokładne okno.
- „Wczesna poprawa w pierwszych dwóch tygodniach przewiduje późniejszą odpowiedź"
  → Szegedi i wsp., 2009, *Journal of Clinical Psychiatry*. Zweryfikuj i podaj ostrożnie,
  jako prawidłowość grupową, nie jako prognozę dla czytelnika.
- „Systematyczny pomiar objawów przy leczeniu depresji poprawia wyniki (measurement-based
  care)" → Guo i wsp., 2015, *American Journal of Psychiatry*. To jest rdzeń wpisu,
  zweryfikuj starannie.
- „Część osób nie odpowiada na pierwszy lek" → Rush i wsp., 2006, *American Journal of
  Psychiatry* (STAR\*D). Podaj delikatnie i bez odsetków, jeśli nie potwierdzisz ich
  w abstrakcie.
- Wszystkie skale objawowe (PHQ-9 i podobne) opisuj jako narzędzia przesiewowe używane
  przez klinicystów, **bez progów punktowych** i bez instrukcji samooceny.

**9. Czego NIE robić**
- ⛔ Zero nazw leków, dawek, klas leków i porównań między lekami.
- ⛔ Zero sugestii odstawienia, zmiany dawki, pominięcia dawki albo „przeczekania".
  Zdanie „nie zmieniaj niczego bez rozmowy z osobą, która przepisała lek" musi paść wprost
  co najmniej raz i wybrzmieć w FAQ.
- ⛔ Zero tematów kryzysowych. Jeśli wątek myśli samobójczych ciśnie się do sekcji o gorszym
  samopoczuciu na starcie leczenia, autor **zatrzymuje pracę i pyta operatora**, zamiast
  improwizować. To wymaga decyzji operatora i informacji o liniach kryzysowych.
- Nie sugeruj, że apka zastąpi wizytę kontrolną ani że wyśle raport lekarzowi
  (`therapist-sharing` = planned). Raport czytasz ty, na wizycie.
- Nie powtarzaj metodyki z `/journal/why-mood-tracking-stops-working`, linkuj do niej.

---

# 10. Is your mental health app data private

**1. Meta**
- `seo_url`: `are-mental-health-apps-private`
- kategoria: `MindSync Tips` | `kolor`: `#339499` | `planowana_data`: **2026-09-13**
- `tagi`: `["data", "privacy"]`
- H1: „Is Your Mental Health App Data Private? A Checklist Before You Type Anything"
- `meta_title` (50 zn.): „Is Your Mental Health App Data Private? | MindSync"
- `meta_description` (156 zn.): „Mood data is health data. A checklist for reading a mental
  health app's privacy policy, the questions worth asking, and what to do before you type
  anything."
- długość: **1600-2000 słów**

**2. Frazy i intencja**
- główna: `are mental health apps private`
- poboczne: `do mental health apps sell your data`, `are mental health apps confidential`,
  `is my therapy app hipaa compliant`, `mental health app privacy policy`,
  `can my employer see my mental health app`, `how to delete mental health app data`
- intencja: nieufność przed pierwszym wpisem do apki albo tuż po nagłówku prasowym.
  Odbiorca ostrożny, często techniczny, wrogi wobec marketingu. Dlatego wpis musi być
  użyteczny nawet dla kogoś, kto nigdy nie zainstaluje MindSync, inaczej nie zadziała.
- luka: SERP to teksty publicystyczne o raporcie Mozilli i ogólniki „read the privacy
  policy". **Nikt nie daje wykonalnego protokołu czytania polityki prywatności** w dziesięć
  minut, z konkretnymi frazami do wyszukania w dokumencie. To jest nasz kąt.
- **Zasada wiarygodności:** wpis jest checklistą, nie autoreklamą. MindSync pojawia się raz,
  z linkiem do `/faq`, i wyłącznie w zakresie, który tam faktycznie stoi. Wszystko poza tym
  autor zostawia jako `[VERIFY-UI: ...]` dla operatora.

**3. Struktura (H2/H3)**
- Lead (40-60 słów): wpisujesz w apkę zdanie, którego nie powiedziałeś nikomu, i przez
  sekundę zastanawiasz się, gdzie ono właściwie ląduje.
- H2: Why mood data is a different kind of data
  - co można wywnioskować z serii ocen nastroju i notatek; bez straszenia, konkretnie
- H2: What research and regulators actually found
  - badanie o transmisji danych z aplikacji do stron trzecich, przegląd Mozilli, działania
    organów regulacyjnych wobec dużych marek; wszystko z rokiem i nazwą
- H2: The word „confidential" does not mean what you think here
  - H3: Therapy confidentiality is a professional obligation
  - H3: A consumer app usually operates under a privacy policy, not that obligation
  - H3: Where health privacy rules apply and where they usually do not
  - **zastrzeżenie obowiązkowe:** to nie jest porada prawna, przepisy różnią się
    między krajami i zmieniają się w czasie
- H2: The ten minute privacy policy read
  - H3: Search the document for these words (sell, share, third party, advertising,
    partners, retention, delete)
  - H3: Check what happens on account deletion
  - H3: Check whether analytics and advertising SDKs get the content or only the events
  - H3: Check who owns the company and what changes if it is sold
- H2: Questions worth asking support before you commit
  - cztery pytania z jednym zdaniem „a good answer sounds like"
- H2: What you control, whatever app you use
  - sekcja praktyczna: co warto zapisywać, co lepiej trzymać poza chmurą, jak korzystać
    z usuwania, po co przeglądać uprawnienia raz na kwartał
- H2: Frequently asked questions
  - H3: Are mental health apps confidential?
  - H3: Do mental health apps sell your data?
  - H3: Is my mental health app covered by HIPAA?
  - H3: Can my therapist see what I write in an app?
  - H3: How do I delete my data from a mental health app?

**4. Karty funkcji** (werdykt: timeline, check-ins, mood-trends, personal-bio)
- inline w „What you control, whatever app you use":
  `[FEATURE: timeline | Everything you have written sits on one filterable timeline with a recycle bin, so deleting something is a decision you can make calmly.]`
- inline w sekcji o tym, po co w ogóle zapisywać:
  `[FEATURE: check-ins | A one minute rating of the areas you are working on, which is the smallest useful footprint if you want the trend without the diary.]`
- **bez bloku `[FEATURES:]`.** Wpis o prywatności z katalogiem funkcji na końcu brzmiałby
  sprzedażowo i podkopałby cały tekst. Dwie karty wystarczą.

**5. Mapa linkowania**
- `<a href="/journal/tracking-mood-on-antidepressants">` anchor „if you are tracking
  medication effects, that is health data too" (opublikowany 09-12)
- `<a href="/journal/why-mood-tracking-stops-working">` anchor „what mood data can and
  cannot tell you"
- `<a href="/journal/how-to-use-mindsync">` anchor „how MindSync itself works"
- **Landing partner:** `/faq` (anchor „how your entries are stored and who can see them").
  Pomocniczo `/features`.
- ⛔ Zero linku do `/membership` w tym wpisie. Miks prywatności i cennika psuje ton.

**6. GEO**
- Cytowalna odpowiedź na `are mental health apps confidential`, 55-75 słów: rozróżnienie
  tajemnicy zawodowej i polityki prywatności, plus zdanie o tym, od czego zależy odpowiedź.
  Ten fragment ma największą szansę na cytowanie w AI Overviews w całej partii.
- Cytowalna lista siedmiu słów do wyszukania w polityce prywatności, 50-70 słów.

**7. Hero**
- „Abstrakcja": miękka, zamknięta forma w palecie mint i forest, sugestia osłony bez
  ikonografii kłódki i tarczy, spokojna kompozycja.
- `hero_image_alt`: „A soft enclosed shape in mint and forest tones, quiet and protected".

**8. Źródła do weryfikacji**
- „Wiele aplikacji zdrowia psychicznego przesyłało dane do stron trzecich, a polityki
  prywatności tego nie ujawniały" → Huckvale, Torous i Larsen, 2019, *JAMA Network Open*.
  Zweryfikuj liczby i sformułowanie.
- „Przegląd aplikacji zdrowia psychicznego wykazał powszechne problemy z prywatnością"
  → Mozilla Foundation, *Privacy Not Included*, edycja 2022 i aktualizacja 2023.
  Zweryfikuj, ile aplikacji z ilu dostało ostrzeżenie w danej edycji, i podaj rok przy
  liczbie. To jest raport organizacji pozarządowej, nie badanie recenzowane, i tak to opisz.
- Działania organów regulacyjnych wobec znanych marek (2023) opisuj **faktograficznie,
  z rokiem i nazwą organu**, bez ocen i bez wskazywania konkurencji palcem.
- Kwestie prawne (HIPAA, RODO) formułuj ogólnie, z linkiem do źródła urzędowego i ze
  zdaniem, że to nie jest porada prawna.

**9. Czego NIE robić**
- Nie porównuj się z nazwami konkurencyjnych aplikacji i nie sugeruj, że są nieuczciwe.
  Wpis daje kryteria, czytelnik ocenia sam, także nas.
- Nie deklaruj żadnych parametrów bezpieczeństwa MindSync, których nie ma na `/faq`:
  zero twierdzeń o szyfrowaniu, lokalizacji serwerów, certyfikatach i audytach bez
  potwierdzenia operatora. W razie potrzeby `[VERIFY-UI: ...]`.
- Nie obiecuj udostępniania danych terapeucie ani jego braku jako „funkcji prywatności":
  `therapist-sharing` jest planned, więc w FAQ odpowiadasz wprost, że dziś nie ma w apce
  włącznika udostępniania.
- Nie strasz i nie buduj poczucia zagrożenia. Ton: spokojna kompetencja.

---

## Checklista przed oddaniem partii do publikacji

1. Każdy wpis: `humanizer` → akcept `brand-voice-manager` → `schema_jsonld` od
   `seo-tech-lead` → hero od `graphic-designer` (frazy do alt są w briefach) →
   `status: gotowy`.
2. `python scripts/blog-queue-gate.py` przed pierwszym uruchomieniem dripu partii.
3. Kontrola em-dash na plikach kolejki i na briefach.
4. Kontrola kart: żaden wpis nie przekracza trzech, wszystkie id ze statusem `live`
   (`streaks` i `therapist-sharing` są zakazane w całej partii).
5. Kontrola linków: zero surowych `[LINK: ...]`, zero linków bezwzględnych na
   `https://mindsync.app/...` (301 na host `www`), zero linków do wpisów jeszcze
   nieopublikowanych poza `[LINK-LATER:]`.
6. Po publikacji 02, 03, 06 i 07: `webflow-publisher` dopina linki „w przód" z 01, 02, 05
   i 06 (pięć znaczników `[LINK-LATER:]` w całej partii).
7. Po miesiącu: `scripts/gsc/blog-tematy.py` i `blog-partia-frazy.py`, podmiana pytań FAQ
   na realne zapytania z liczbami, decyzje o rozbudowach zamiast nowych wpisów.
