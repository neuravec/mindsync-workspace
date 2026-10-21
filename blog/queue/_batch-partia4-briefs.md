# Partia 4: briefy wpisów (3 pozycje, drip 2026-09-26..2026-09-28), pierwsza partia stylem Moniki

> Data: 2026-09-25. Autor briefów: `seo-content-writer`. Wykonawca prozy: `blog-writer` przez
> skill `blog-write` (+ `humanizer` z próbką `docs/blog/voice-sample-monika.md`, akcept
> `brand-voice-manager` wg checklisty §2.5, schema od `seo-tech-lead`, hero od
> `graphic-designer`). **Treść po ANGIELSKU.** Format pliku kolejki: `blog/queue/_format.md`.
> Głos: `docs/blog/brand-mindsync.md` §2 (szkielet §2.2, nagłówki §2.1 pkt 12).
>
> **Status bramki KROK 0:** `blog/queue/_preflight-partia4.json`, oczekiwany wynik **5x OK,
> 0 RYZYKO, 0 BRAK** (3 tematy + 2 rezerwy). ⚠ Wynik policzony ręcznie wg logiki skryptu
> (keywordy to dosłowne podciągi katalogu), bo sesja autora briefów nie miała dostępu do
> powłoki. Przed przekazaniem do `blog-writer` lider uruchamia jedną komendą:
> `python scripts/blog-coverage-preflight.py --temat blog/queue/_preflight-partia4.json`.
>
> **Status danych:** `scripts/gsc/blog-tematy.py` NIE został uruchomiony (brak powłoki w tej
> sesji); przy zerowym ruchu bloga i tak nie dałby popytu na nowe tematy. Frazy i pytania FAQ
> pochodzą z researchu SERP (brzmienia z tytułów konkurencji i z bloków pytań w wynikach),
> bez wolumenów i bez KD. Wszystkie trzy tematy mają w SERP wyraźny popyt masowy (Cleveland
> Clinic, Calm, Forbes, Greater Good, Medical News Today, dziesiątki gabinetów). Po pierwszych
> wyświetleniach: `scripts/gsc/blog-partia-frazy.py` i korekta H2 oraz FAQ na frazy z liczbami.

## Zasady wspólne dla wszystkich 3 briefów (nie powtarzam ich w każdym)

1. **Szkielet Moniki jest nadrzędny wobec starego szablonu briefów.** Kolejność: otwarcie-
   rozpoznanie (bez H2, 60-120 słów) → skąd to się bierze → jak to wygląda w życiu → co mówią
   badania → co możesz spróbować → akapit o apce w rytmie „This is what MindSync's [funkcja]
   is for. Log [3 konkrety z wpisu]. Give it time, and [funkcja] turns those entries into
   something you can see: [co]. Then [co dalej]." → jedno osobiste pytanie do czytelnika →
   blok `[FEATURES:]` → FAQ. Sekcje 2-4 wolno przestawić, apka i pytanie zawsze na końcu.
   **Długość: 900-1400 słów bez FAQ** (brand doc §2.2). Jeden H2 na sekcję. Fraza główna
   w H1 i w jednym H2, bez upychania.
2. **Nagłówki jak zdania z rozmowy, często z dwukropkiem** (§2.1 pkt 12). Propozycje H2
   niżej są wiążące co do sensu i miejsca frazy; autor może je doszlifować głosem Moniki, ale
   H2 z frazą zostaje dosłownie.
3. **Humor:** 2-4 konkretne, przesadzone obrazki z codzienności na wpis, najwięcej
   w otwarciu i w części praktycznej, zero w akapitach o badaniach i o cierpieniu. W każdym
   briefie podaję 2-3 „haczyki" jako materiał, nie gotowe zdania. Maksymalnie jedna etykieta
   „Fun fact:" albo „Disclaimer:" na wpis.
4. **Zero zmyślonej biografii Moniki.** „I" tylko jako opinia („I feel like..."). Żadnych
   anegdot w pierwszej osobie, żadnych „my client", „a friend of mine".
5. **Zakaz obu myślników.** Zero em-dash (U+2014) i zero półpauzy (U+2013) w tytule, meta,
   zajawce i treści. Przebuduj zdanie. Zakres liczbowy zwykłym łącznikiem: „4-6 weeks".
   Bramka dripu łapie tylko U+2014, półpauzę sprawdź wyszukiwarką po znaku.
6. **YMYL:** zero diagnozowania, zero interpretowania objawów czytelnika, zero obietnic
   zdrowotnych, zero zniechęcania do terapii i leków, zero treści kryzysowych. MindSync
   uzupełnia terapię, nie zastępuje. Każdy brief ma własną listę „czego NIE twierdzić".
7. **Funkcje `planned` nie istnieją w treści:** `therapist-sharing` i `streaks`. Rytm Moniki
   „bring it to your next session" jest dozwolony (czytelnik sam niesie notatki), zero
   sugestii wysyłania czegokolwiek terapeucie z apki. **Nazwy funkcji z katalogu**, nie
   z newslettera: „Between-session voice notes" (nie „Between-Session Notes"), „Wellbeing
   check-ins" i „Mood & focus-area trends" (nie „Symptom Tracking"), „Workspace".
8. **Karty:** jedna `[FEATURE:]` inline plus blok `[FEATURES:]` z trzema pozycjami przed FAQ.
   Tylko id z listy danego briefu, żadne id nie powtarza się w obrębie wpisu. Zdania kart są
   nowe (nie przepisuj sformułowań z partii 1-3). Zero cen w treści.
9. **FAQ:** H2 dokładnie `Frequently asked questions`, pytania w H3 dokładnie w brzmieniu
   z briefu, 4-5 sztuk. Odpowiedź 40-70 słów, pierwsze zdanie to pełna odpowiedź (GEO),
   dalej warunek albo zastrzeżenie. Głosem Moniki, ale bez humoru.
10. **Badania:** opowiadane jak historia z rokiem na początku („In 2024, Givi and Kirk...").
    Nazwa czasopisma albo instytucji w zdaniu, link w tę nazwę (RichText `a`), nigdy goły URL.
    Autor **weryfikuje każdą liczbę u źródła pierwotnego** (abstrakt, PDF). Pozycje oznaczone
    „liczba do potwierdzenia" idą jakościowo, jeśli liczby nie da się potwierdzić. Po każdym
    badaniu 1-2 krótkie zdania „co to znaczy dla ciebie".
11. **Linki wewnętrzne wyłącznie względne:** `<a href="/journal/slug">`, `<a href="/features">`,
    `<a href="/pre-order/...">`. Nigdy `https://mindsync.app/...` w treści.
12. **Linkowanie w partii biegnie wyłącznie wstecz** (02 → 01, 03 → 02), więc w tej partii nie
    ma `[LINK-LATER:]`. Warunek: 01 wychodzi 2026-09-26, 02 wychodzi 2026-09-27. Jeśli któryś
    się opóźni, link do niego w późniejszym wpisie zamień na
    `[LINK-LATER: <slug> | <ten sam anchor>]` i zgłoś liderowi.

## Kolejność publikacji, daty i topologia linkowania

| data | # | plik w kolejce | slug (`seo_url`) | klaster | kategoria | `kolor` | rola |
|---|---|---|---|---|---|---|---|
| 2026-09-26 | 01 | `2026-09-26_early-signs-of-burnout.json` | `early-signs-of-burnout` | 5 | Therapy | `#e8af0a` | szeroki top-of-funnel, cel linku z 02 |
| 2026-09-27 | 02 | `2026-09-27_how-to-stop-people-pleasing.json` | `how-to-stop-people-pleasing` | 3 | MindSync Tips | `#339499` | duet z /pre-order/understand-behavioural-patterns, cel linku z 03 |
| 2026-09-28 | 03 | `2026-09-28_anxious-attachment-style.json` | `anxious-attachment-style` | 3 | Therapy | `#3c67a5` | zamyka partię, otwiera przyszły duet z avoidant |

Kolory: ostatni opublikowany wpis (`how-to-name-what-you-feel`, 2026-09-23) ma `#ff9f8a`,
więc sekwencja `#ff9f8a` → `#e8af0a` → `#339499` → `#3c67a5`, sąsiednie różne.

**Wzmocnienie po partii (zadanie PATCH dla `webflow-publisher`, nie dla autora):**
z `digital-burnout-brain-rewiring` do `early-signs-of-burnout` (anchor „burnout that comes
from the job rather than the screen"), z `how-to-identify-emotional-triggers` do
`anxious-attachment-style` (anchor „when the trigger is someone going quiet").

---

# 01. Early signs of burnout

**1. Meta**
- `seo_url`: `early-signs-of-burnout` | plik: `blog/queue/2026-09-26_early-signs-of-burnout.json`
- kategoria: `Therapy` | `kolor`: `#e8af0a` | `planowana_data`: **2026-09-26**
- `tagi`: `["modern-life", "burnout"]`
- H1: „Burnout Doesn't Announce Itself: The Early Signs of Burnout Nobody Warns You About"
- `meta_title` (58 zn.): „Early Signs of Burnout (It's Not Just Tiredness) | MindSync"
- `meta_description` (151 zn.): „Burnout rarely starts with exhaustion alone. The early signs
  of burnout, what research says about going cold at work, and five places to start this
  week."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `early signs of burnout`
- poboczne: `signs of burnout`, `am I burnt out or just tired`, `burnout symptoms`, `how long
  does burnout last`, `how to recover from burnout`, `stages of burnout`
- intencja: podejrzenie, jeszcze bez nazwy. Człowiek czuje, że „coś jest nie tak" od kilku
  tygodni, weekend nie pomaga, i chce wiedzieć, czy to już to, czy tylko zmęczenie. Mobile,
  wieczór albo niedziela.
- luka: SERP (Cleveland Clinic, Calm, WebMD, Forbes, dziesiątki gabinetów) daje listę 15-22
  objawów, w której zmęczenie jest zawsze na pierwszym miejscu. **Nikt nie mówi, że według
  badań najbardziej wymownym wczesnym sygnałem nie jest zmęczenie, tylko „zimnienie"
  (cynizm, dystans).** Leiter i Maslach 2016 pokazali, że profil „tylko wyczerpany" jest
  dalej od burnoutu niż profil „tylko zdystansowany". To jest cały nasz kąt i najmocniejszy
  kandydat do GEO: „The early sign is going cold, not getting tired."
- ⚠ granica: `/journal/digital-burnout-brain-rewiring` sam odcina się od burnoutu
  zawodowego („isn't regular burnout with a screen attached"). Ten wpis to burnout wg WHO,
  związany z pracą. Jedno zdanie i link, bez przejmowania fraz „digital burnout".

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** forma „Do any of these sound familiar?" + trzy scenki, ostatnia
  krótka z mrugnięciem. Haczyki: odpowiadasz „whatever works" na pytanie, na którym kiedyś
  by ci zależało; weekend minął, a ty jesteś tak samo zmęczony jak w piątek; niedzielna
  chandra zaczyna się już w sobotę po obiedzie.
- **H2: „Why is it so easy to miss?"** (skąd to się bierze)
  - burnout narasta powoli, a organizm się adaptuje: to, co było wyjątkiem, staje się
    normą. Analogia (w duchu jej „software update on a device whose battery keeps dying"):
    telefon, który wciąż pokazuje 100%, choć kondycja baterii spadła do 70%, więc padasz
    o 15:00 i nie wiesz czemu.
  - definicja WHO jako fakt: zjawisko zawodowe, nie choroba, trzy wymiary. To jest fragment
    cytowalny, 40-60 słów.
  - slot na **„Fun fact:"**: WHO umieściło burnout w rozdziale „Factors influencing health
    status or contact with health services", czyli formalnie to nie jest diagnoza, tylko
    powód, dla którego ludzie trafiają do lekarza.
- **H2: „The early signs of burnout, as they actually show up:"** (fraza główna w H2; jak to
  wygląda w życiu)
  - lista w drugiej osobie, 5-6 punktów, po jednym dla wymiaru plus codzienne scenki:
    zmęczenie, którego nie naprawia weekend; ton „whatever" wobec rzeczy, które cię
    obchodziły; sarkazm na spotkaniach, który kiedyś był dowcipem; poczucie, że cokolwiek
    zrobisz, i tak niczego nie zmienia; odkładanie maili, które zajęłyby dwie minuty;
    wieczory, w których nie masz siły nawet na odpoczynek.
  - H3: „Tired, or burnt out?" (PAA): test weekendu i urlopu, jakościowo, jako obserwacja
    powszechnie opisywana, nie jako narzędzie diagnostyczne.
  - link do `/journal/sunday-scaries`.
- **H2: „What research turned up:"** (badania)
  - 2016, Maslach i Leiter, *World Psychiatry*: trzy wymiary (wyczerpanie, cynizm,
    poczucie nieskuteczności) i to, że burnout to przeciwieństwo zaangażowania, nie
    przeciwieństwo wypoczynku.
  - 2016, Leiter i Maslach, *Burnout Research*: pięć profili; profil „disengaged" (sam
    cynizm) wypadł bliżej pełnego burnoutu niż „overextended" (samo wyczerpanie). Wniosek dla
    czytelnika dwoma krótkimi zdaniami, np. „Tired is a signal. Cold is a louder one."
  - 2021, van Dam, *European Journal of Work and Organizational Psychology*: uczciwa granica,
    powrót z klinicznego burnoutu może trwać ponad rok. Od razu dlaczego to dobra wiadomość
    (to, co łapiesz wcześnie, zwykle kosztuje mniej).
- **H2: „Five places where you can start:"** (co spróbować; tryb rozkazujący, 1-3 zdania
  dlaczego)
  1. Name which of the three is loudest (wyczerpanie, dystans, „nic nie ma sensu"), bo każde
     prosi o coś innego; link do `/journal/how-to-name-what-you-feel`.
  2. Run the weekend test honestly, na dwóch kolejnych weekendach, nie jednym.
  3. Remove one demand before adding one habit. Haczyk: dodawanie jogi o 6:00 do pełnego
     kalendarza to „wellness as another deadline".
  4. Say the sentence: „I can do X by Friday or Y by Friday. Which one matters more?" To jest
     gotowe zdanie do powiedzenia na głos (wymóg §2.5).
  5. Watch for the first cold thought (pierwszy sarkazm, pierwsze „who cares") i zapisz go,
     zanim go zracjonalizujesz. Tu inline karta `check-ins`.
  - jeden akapit spokojnie: jeśli to trwa tygodniami albo przelewa się poza pracę, powiedz to
    lekarzowi albo terapeucie, bez straszenia; link do
    `/journal/regulate-nervous-system-between-therapy-sessions` przy uspokajaniu ciała.
  - puenta sekcji (jedna), w stylu „You can't rest your way out of something you haven't
    noticed yet."
- **Akapit o apce (rytm §2.1 pkt 9):** „This is what MindSync's Wellbeing check-ins are for.
  Log your energy on Friday and again on Sunday night, the meeting you got sarcastic in, and
  the task you pushed for the third day running. Give it time, and Mood & focus-area trends
  turns those entries into something you can see: [whether the weekend still refills you,
  which weeks go cold]. Then [read the weekly summary before your next session]." Konkrety
  mają zostać z treści wpisu.
- **Pytanie do czytelnika (1 zdanie):** np. „What's the first thing you stopped caring about,
  and when did you notice?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: What are the early signs of burnout?
  - H3: How do I know if I'm burnt out or just tired?
  - H3: What are the 5 stages of burnout?
  - H3: How long does burnout last?
  - H3: Can burnout go away on its own?
  - ⚠ odpowiedź o „5 stages": uczciwie, że modele etapów krążą w poradnikach, ale nie są
    zwalidowaną klasyfikacją; badania opisują trzy wymiary i profile. To jest nasz wyróżnik
    w SERP i fragment pod GEO.

**4. Karty funkcji** (bramka: check-ins, mood-trends, summaries, reflect, voice-notes,
session-debrief; używamy czterech)
- inline w „Five places where you can start" (punkt 5):
  `[FEATURE: check-ins | Thirty seconds on a Friday and thirty on a Sunday night, which is exactly how you find out whether the weekend still does its job.]`
- blok przed FAQ:
  `[FEATURES: Catching it while it is still early || mood-trends | Energy and mood across months on one screen, so a slow slide shows up before it turns into a cliff. || summaries | A weekly read of your own entries, useful on the Sunday you cannot tell whether this week was worse or just louder. || reflect | For the evening when you need to talk it through with something that asks one more question than you would ask yourself.]`

**5. Mapa linkowania** (tylko wpisy już na żywo)
- `<a href="/journal/digital-burnout-brain-rewiring">` anchor „when the overload comes from
  screens rather than the job" (sekcja „Why is it so easy to miss?", jedno zdanie granicy)
- `<a href="/journal/sunday-scaries">` anchor „the Sunday dread that starts earlier every
  week" (sekcja z objawami)
- `<a href="/journal/how-to-name-what-you-feel">` anchor „a more precise word than tired"
  (krok 1)
- `<a href="/journal/regulate-nervous-system-between-therapy-sessions">` anchor „bringing
  your body down a notch first" (część praktyczna)
- **Landing partner:** `/pre-order/track-interventions` (anchor „seeing which changes
  actually move your energy"), jeden raz, przy kroku 3.

**6. GEO**
- Definicja burnoutu wg WHO, 40-60 słów, z trzema wymiarami i zdaniem „not classified as
  a medical condition".
- Teza „the early sign is often going cold, not getting tired", 50-70 słów, z nazwiskami
  i rokiem (Leiter i Maslach 2016). Musi działać wyjęta z kontekstu.

**7. Hero**
- Wariant „codzienny moment" (`hero-01-codzienny-moment.md`): biurko o złotej godzinie,
  otwarty laptop z ekranem odwróconym od widza, nietknięty kubek herbaty, a obok okno
  z miękkim światłem; bez osoby.
- `hero_image_alt`: „A quiet desk at golden hour with an untouched mug of tea beside a laptop".
- nazwa pliku hero: `early-signs-of-burnout-hero.webp`.

**8. Źródła (zweryfikowane 2026-09-25)**
- **POTWIERDZONE.** World Health Organization, 28.05.2019, „Burn-out an 'occupational
  phenomenon': International Classification of Diseases".
  https://www.who.int/news/item/28-05-2019-burn-out-an-occupational-phenomenon-international-classification-of-diseases
  Trzy wymiary, „not classified as a medical condition", dotyczy wyłącznie kontekstu pracy.
  ⚠ Z tego ostatniego wynika: nie rozciągaj „burnoutu" na rodzicielstwo czy związek
  w zdaniach definicyjnych.
- **POTWIERDZONE.** Maslach C., Leiter M.P., 2016, *World Psychiatry* 15(2):103-111,
  „Understanding the burnout experience: recent research and its implications for
  psychiatry". https://onlinelibrary.wiley.com/doi/full/10.1002/wps.20311 (PMC4911781).
- **POTWIERDZONE (jakościowo).** Leiter M.P., Maslach C., 2016, *Burnout Research* 3:89-100,
  „Latent burnout profiles: A new approach to understanding the burnout experience".
  https://www.sciencedirect.com/science/article/pii/S2213058615300188
  Pięć profili (burnout, overextended, disengaged, ineffective, engaged); disengaged bliżej
  burnoutu niż overextended, co przemawia przeciw traktowaniu samego wyczerpania jako
  wskaźnika burnoutu. ⚠ Wielkości próby i odsetków profili nie podawaj bez abstraktu przed
  oczami (ScienceDirect blokuje automatyczny odczyt, sprawdź ręcznie).
- **POTWIERDZONE (jakościowo).** van Dam A., 2021, *European Journal of Work and
  Organizational Psychology* 30(5):732-741, „A clinical perspective on burnout: diagnosis,
  classification, and treatment of clinical burnout".
  https://www.tandfonline.com/doi/full/10.1080/1359432X.2021.1948400
  Powrót z klinicznego burnoutu „may take more than a year". ⚠ Użyj dokładnie tej granicy,
  bez przedziału „od czterech tygodni do trzech lat" z newslettera, bo nie ma go w tym
  źródle.
- **Czego autor ma NIE twierdzić:**
  - że burnout to depresja albo że się od niej odróżnia w konkretny sposób (diagnostyka),
  - że istnieje zwalidowany model „5 albo 12 etapów" (nie istnieje, piszemy to wprost),
  - żadnych skutków zdrowotnych ze Salvagioni i wsp. 2017 (cukrzyca, choroby serca,
    śmiertelność): to straszenie w top-of-funnel, nie pasuje do głosu,
  - żadnych liczb z ankiet firm (Gallup, Deloitte, platformy HR),
  - że MindSync wykrywa albo zapobiega burnoutowi. Apka pokazuje przebieg, człowiek wyciąga
    wnioski.

**9. Czego NIE robić**
- Nie dawaj quizu „czy masz burnout" ani skali punktowej.
- Nie namawiaj do rzucenia pracy ani do zwolnienia lekarskiego; to decyzje czytelnika
  z lekarzem.
- Nie dubluj `/journal/digital-burnout-brain-rewiring` (ekrany) ani `/journal/sunday-scaries`
  (kalendarz tygodnia). Po jednym zdaniu i link.

---

# 02. How to stop people pleasing

**1. Meta**
- `seo_url`: `how-to-stop-people-pleasing` | plik:
  `blog/queue/2026-09-27_how-to-stop-people-pleasing.json`
- kategoria: `MindSync Tips` | `kolor`: `#339499` | `planowana_data`: **2026-09-27**
- `tagi`: `["understanding-patterns", "boundaries"]`
- H1: „'No' Is Enough on Its Own: How to Stop People Pleasing"
- `meta_title` (57 zn.): „How to Stop People Pleasing (Without the Guilt) | MindSync"
- `meta_description` (153 zn.): „Why yes comes out before you think, what research says about
  how people react when you decline, and how to stop people pleasing one small no at a time."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `how to stop people pleasing`
- poboczne: `how to stop being a people pleaser`, `why am I a people pleaser`, `is people
  pleasing a trauma response`, `fawn response`, `how to say no without feeling guilty`,
  `setting boundaries`
- intencja: zmęczenie własnym „tak". Człowiek właśnie zgodził się na coś, czego nie chciał,
  i szuka, jak przestać, a przy okazji, skąd to się bierze. Druga grupa trafia przez modny
  termin „fawn response" i chce wiedzieć, czy to o nim.
- luka: SERP dzieli się na porady ogólne (Oprah, Greater Good, Medium: „set boundaries",
  „remember your worth") i teksty gabinetów o „fawn response", które często z każdego
  people-pleasera robią osobę po traumie. **Nikt nie podaje badania, które wprost uspokaja
  lęk przed odmową** (Givi i Kirk 2024: ludzie przeszacowują negatywne skutki odmowy), a to
  jest dokładnie to, czego potrzebuje ktoś, kto boi się powiedzieć „nie". Nasz kąt: poczucie
  winy przychodzi PRZED odmową (anticipatory guilt), więc jest prognozą, nie wyrokiem,
  a prognozy da się sprawdzać. Plus uczciwość: „fawn" to termin praktyka, nie rozpoznanie.

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** forma pytania o konkretny moment, jak u Moniki: „Can you remember
  the last time someone asked you for something? How fast did 'yeah, of course, no problem'
  come out?" Haczyki: „tak", które żałujesz przed obiadem; wiadomość z odmową przepisana
  cztery razy i ostatecznie niewysłana; przepraszanie krzesła, o które się potknąłeś.
- **H2: „Where does the automatic yes come from?"** (skąd to się bierze)
  - wyuczona strategia bezpieczeństwa: kiedyś zgoda utrzymywała spokój, więc układ nerwowy
    wybiera ją pierwszą. Monika ma to w DNA: „What was learned by force can be unlearned by
    decision" (to jej puenta, można jej użyć jako puenty sekcji, ale tylko raz i nie
    dosłownie w H2).
  - „fawn response" wyjaśniony uczciwie: termin z pracy klinicznej Pete'a Walkera, opisujący
    uspokajanie drugiej osoby jako odruch obronny; popularny, ale nie jest kategorią
    diagnostyczną, a zwykłe people-pleasing nie oznacza traumy.
  - anticipatory guilt: poczucie winy przychodzi, zanim cokolwiek zrobisz, więc jest
    prognozą.
  - slot na **„Disclaimer:"**, np. „Disclaimer: being kind is not the problem."
- **H2: „Signs you're a people pleaser (the everyday version):"** (jak to wygląda w życiu)
  - lista w drugiej osobie: mówisz „tak", zanim skończą pytać; masz w głowie gotowe
    wytłumaczenie każdej odmowy, nawet takiej, której nikt nie wymaga; czujesz ulgę, gdy ktoś
    odwoła spotkanie, na które się zgodziłeś; dopasowujesz się do innych nawet przy stole
    (haczyk pod Exline 2012: drugi kawałek ciasta, bo gospodyni patrzy).
- **H2: „What research turned up:"** (badania)
  - 2024, Givi i Kirk, *Journal of Personality and Social Psychology*: pięć eksperymentów,
    osoby odmawiające zaproszenia przeszacowywały, jak bardzo zdenerwuje to zapraszającego,
    jak bardzo zabrzmi to jak brak troski i czy zaproszenie się jeszcze powtórzy. W badaniu
    pilotażowym 77% ludzi przyznało, że choć raz przyjęli zaproszenie, na które nie chcieli
    iść, ze strachu przed skutkami odmowy (liczba do potwierdzenia w PDF APA, patrz źródła).
    Wniosek dwoma zdaniami: „The cost of no is real. It's just smaller than your brain
    quotes."
  - 2012, Exline i wsp., *Journal of Social and Clinical Psychology*: osoby z wysoką
    socjotropią (silna potrzeba zadowalania innych) jadły więcej, gdy sądziły, że rówieśnik
    tego od nich oczekuje. Wniosek: people-pleasing sięga dalej niż kalendarz.
  - uczciwa granica: nie ma badań, które testowałyby „oduczanie się people-pleasingu" jako
    metodę; to, co działa, opisują praktycy i terapia. Powiedz to wprost.
- **H2: „How to stop people pleasing without setting your whole life on fire:"** (fraza
  główna w H2; co spróbować; tryb rozkazujący)
  1. Put a pause between the question and the answer. Gotowe zdanie: „'Let me check and get
     back to you' is a complete response."
  2. Start where the stakes are low: kelner, sklep, znajomy z luźnym zaproszeniem, nie szef
     i nie mama.
  3. Treat the guilt as a forecast, then check it. Zapisz przed odmową, co się twoim zdaniem
     stanie, a dzień później, co się stało. Tu inline karta `voice-notes`.
  4. Give one reason, or none. Haczyk: odmowa z czterema akapitami tłumaczeń to „a legal
     defense nobody asked for".
  5. Expect the wobble. Pierwsze odmowy będą niezręczne i to nie jest dowód, że źle robisz.
  - link do `/journal/early-signs-of-burnout` przy zdaniu, że ciągłe „tak" ma swój koszt
    energetyczny.
- **Akapit o apce (rytm §2.1 pkt 9):** „This is what MindSync's Between-session voice notes
  are for. Log the yes you regretted by lunchtime, the guilt you felt before saying no, and
  what actually happened afterwards. Give it time, and Mood & focus-area trends turns those
  entries into something you can see: [the same people, the same kind of request, the same
  quick yes]. Then pin the one that keeps coming back to your Workspace and bring it to your
  next session."
- **Pytanie do czytelnika:** np. „Who gets your fastest yes, and what would happen if it took
  them an hour to get it?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: Why am I a people pleaser?
  - H3: Is people pleasing a trauma response?
  - H3: What is the fawn response?
  - H3: How do I say no without feeling guilty?
  - H3: Can you stop being a people pleaser?

**4. Karty funkcji** (bramka: voice-notes, reflect, mood-trends, workspace, session-prep,
check-ins; używamy czterech)
- inline w „How to stop people pleasing..." (krok 3):
  `[FEATURE: voice-notes | Say the prediction out loud before you decline, then say what really happened the next day, and let the gap between the two do the convincing.]`
- blok przed FAQ:
  `[FEATURES: Seeing your yes before it comes out || mood-trends | Weeks of your own entries side by side, where the requests that cost you most stop hiding among the ones that did not. || workspace | Park the person or the situation you keep bending around, so it is still there to work on when the session starts. || reflect | When you cannot tell whether you wanted to say yes or just could not say no, a guided conversation that asks the question for you.]`

**5. Mapa linkowania**
- `<a href="/journal/early-signs-of-burnout">` anchor „the slow drain that ends in burnout"
  (wstecz do 01, publikacja 2026-09-26; jeśli 01 się opóźni, `[LINK-LATER:]`)
- `<a href="/journal/how-to-identify-emotional-triggers">` anchor „what sets the automatic
  yes off" (sekcja „Where does the automatic yes come from?")
- `<a href="/journal/how-to-name-what-you-feel">` anchor „naming the feeling under the yes"
  (sekcja o anticipatory guilt)
- `<a href="/journal/how-to-prepare-for-a-therapy-session">` anchor „take it into your next
  session" (przy akapicie o apce albo w odpowiedzi FAQ o traumie)
- **Landing partner:** `/pre-order/understand-behavioural-patterns` (anchor „the patterns in
  how you respond to other people"), jeden raz.

**6. GEO**
- Definicja „fawn response", 40-60 słów: kto ukuł termin, co opisuje, że to nie rozpoznanie
  i że nie każde people-pleasing jest fawn. W SERP prawie nikt tego nie rozdziela, stąd szansa
  na cytowanie.
- Wynik Givi i Kirk 2024 w 40-60 słowach, z rokiem, czasopismem i jednym zdaniem wniosku.

**7. Hero**
- Wariant „codzienny moment": dłoń trzymająca telefon nad kubkiem, ekran niewidoczny,
  kalendarz papierowy z kilkoma skreśleniami w tle, miękkie poranne światło.
- `hero_image_alt`: „A hand holding a phone above a mug next to a paper planner in soft
  morning light".
- nazwa pliku hero: `how-to-stop-people-pleasing-hero.webp`.

**8. Źródła (zweryfikowane 2026-09-25)**
- **POTWIERDZONE, liczba do potwierdzenia.** Givi J., Kirk C.P., 2024, *Journal of
  Personality and Social Psychology* 126(6):1103-1115, „Saying no: The negative
  ramifications from invitation declines are less severe than we think".
  https://www.apa.org/pubs/journals/releases/psp-pspi0000443.pdf
  Pięć eksperymentów, ponad 2000 uczestników, przeszacowanie gniewu zapraszającego,
  sygnału „nie zależy mi" i szansy na kolejne zaproszenie. ⚠ 77% z badania pilotażowego
  potwierdzone tylko w omówieniu Psychology Today; sprawdź w PDF APA, a jeśli się nie zgadza,
  pisz „most people in a pilot survey" bez liczby.
- **POTWIERDZONE, lista autorów do potwierdzenia.** Exline J.J., Zell A.L., Bratslavsky E.,
  Hamilton M., Swenson A., 2012, *Journal of Social and Clinical Psychology* 31(2):169-193,
  „People-pleasing through eating: Sociotropy predicts greater eating in response to
  perceived social pressure". https://guilfordjournals.com/doi/10.1521/jscp.2012.31.2.169
  Wynik: socjotropia wiązała się z jedzeniem większej ilości cukierków tylko wtedy, gdy
  uczestnicy sądzili, że rówieśnik tego chce. W tekście wystarczy „Exline and colleagues".
  ⚠ Próba to studenci w laboratorium; nie uogólniaj na zaburzenia odżywiania.
- **KONCEPCJA PRAKTYKA, NIE BADANIE.** Pete Walker, terapeuta, termin „fawn" jako czwarta
  reakcja obok fight, flight, freeze (książka „Complex PTSD: From Surviving to Thriving",
  2013; tytuł i rok z pamięci, NIEZWERYFIKOWANE, sprawdź przed wymienieniem książki albo
  pisz samo „therapist Pete Walker"). W zdaniu opisz go jako termin z pracy klinicznej, nie
  jako wynik badań. Nie linkuj
  do sklepów z książką.
- **Czego autor ma NIE twierdzić:**
  - że people-pleasing jest objawem traumy albo C-PTSD u czytelnika,
  - że „fawn" jest w DSM albo ICD (nie jest),
  - że odmowa nie ma żadnych kosztów (Givi i Kirk mówią o przeszacowaniu, nie o zerze),
  - że MindSync „oduczy" people-pleasingu. Apka daje miejsce na zapis i obraz wzorca.

**9. Czego NIE robić**
- Nie rób z tego wpisu o granicach w związku przemocowym ani o manipulacji; to inna waga
  tematu i inne zasady bezpieczeństwa.
- Nie wchodź w mechanikę triggerów (`/journal/how-to-identify-emotional-triggers`) ani
  w szukanie zapewnień w bliskiej relacji (to wpis 03). Po jednym zdaniu i link.
- Nie powtarzaj puenty Moniki z newslettera dosłownie w H1 i w treści jednocześnie: „'No' is
  enough on its own" jest w H1, w treści już nie.

---

# 03. Anxious attachment style

**1. Meta**
- `seo_url`: `anxious-attachment-style` | plik:
  `blog/queue/2026-09-28_anxious-attachment-style.json`
- kategoria: `Therapy` | `kolor`: `#3c67a5` | `planowana_data`: **2026-09-28**
- `tagi`: `["understanding-patterns", "relationships"]`
- H1: „Asking Again Won't Change the Answer: Living With an Anxious Attachment Style"
- `meta_title` (59 zn.): „Anxious Attachment Style: Signs, Triggers, Change | MindSync"
- `meta_description` (146 zn.): „Why a slow reply feels like an alarm, what the research on
  anxious attachment actually found, and three things that help, in the order they help."
- długość: 900-1400 słów bez FAQ

**2. Frazy i intencja**
- główna: `anxious attachment style`
- poboczne: `can anxious attachment be healed`, `how to heal anxious attachment`, `anxious
  attachment triggers`, `signs of anxious attachment`, `how to stop being anxiously
  attached`, `anxious attachment in relationships`
- intencja: rozpoznanie siebie w opisie (najczęściej po TikToku albo po quizie) i jedno
  pytanie: czy da się to zmienić. Mocny komponent emocjonalny, wieczór, telefon.
- luka: SERP (Cleveland Clinic, Greater Good, Attachment Project, Medical News Today,
  dziesiątki gabinetów) obiecuje „fix" i „heal", daje listę porad i kończy. **Prawie nikt nie
  podaje badań, które odpowiadają wprost na pytanie „czy to się zmienia"**: Chopik i wsp. 2019
  (lęk w przywiązaniu średnio spada z wiekiem) i Taylor i wsp. 2015 (w trakcie terapii lęk
  w przywiązaniu spada, poczucie bezpieczeństwa rośnie). Nikt też nie mówi uczciwie, że
  „styl" to uproszczenie, a badacze mierzą dwa wymiary. Nasz kąt: radar jest prawdziwy
  (Fraley 2006), zawodzi moment, i to się da zmieniać.
- ⚠ **To jest temat newslettera Moniki #24** (pełny tekst w `docs/blog/voice-sample-monika.md`).
  Wpis ROZWIJA #24 do formy bloga (więcej badań, FAQ, fraza), nie przepisuje go. Wolno
  zachować jej strukturę i najwyżej 2-3 jej zdania-puenty („The radar is real.", „Your
  perception works fine. The timing is what trips it up."), resztę prozy pisz od nowa.

**3. Struktura (H2/H3) wg szkieletu §2.2**
- **Otwarcie (bez H2):** „Do any of these sound familiar?" + trzy scenki z #24, przepisane
  nowymi słowami, ostatnia krótka z mrugnięciem (drzwi zamknięte na klucz / żelazko /
  kuchenka). Haczyki: kropka na końcu „ok." czytana jak wyrok; trzecie „are we okay?" w tym
  tygodniu.
- **H2: „Where anxious attachment comes from:"** (skąd to się bierze)
  - nieprzewidywalna bliskość w dzieciństwie, strategia „walcz o więź", która czasem
    działała. Ainsworth w latach 70. jednym zdaniem, bez szczegółów procedury.
  - slot na **„Fun fact:"**: automat do gier i variable ratio schedule (z #24, wolno użyć,
    własnymi słowami).
  - uczciwie, 1-2 zdania: badacze nie zamykają ludzi w czterech szufladach, tylko mierzą dwa
    wymiary, lęk i unikanie; „styl" to skrót. Fragment cytowalny.
- **H2: „Signs of an anxious attachment style in adult life:"** (fraza główna w H2; jak to
  wygląda w życiu)
  - druga osoba, 4-5 punktów: każda zmiana tonu zauważona; bliskość z odliczaniem;
    zapewnienie, które działa do jutra; testowanie zamiast proszenia; ulga, która przychodzi
    dopiero po odpowiedzi. Jedno zdanie o czułości bez lukru: „None of this makes you needy
    or too much."
  - link do `/journal/how-to-stop-people-pleasing` przy zdaniu, że uspokajanie innych
    i szukanie zapewnień to kuzyni, ale nie to samo.
- **H2: „What research turned up:"** (badania)
  - 2006, Fraley i wsp., *Journal of Personality*: filmy z twarzami, które powoli zmieniają
    wyraz; osoby z wysokim lękiem w przywiązaniu widziały zmianę wcześniej, ale częściej się
    myliły, bo oceniały za szybko. Wniosek jej zdaniami („The radar is real...").
    ⚠ Szczegół „przy pełnym filmie różnica w trafności znika" podawaj tylko po sprawdzeniu
    w pełnym tekście; w abstrakcie jest sama wcześniejsza percepcja.
  - 2019, Chopik, Edelstein i Grimm, *Journal of Personality and Social Psychology*: dane
    z trzech badań podłużnych, wiek 13-72, 628 osób; lęk w przywiązaniu rósł do młodej
    dorosłości, potem średnio spadał, najbardziej w średnim i późnym wieku. Wniosek: to nie
    jest wyrok na całe życie. Zastrzeżenie: to średnie dla grup, nie prognoza dla jednej osoby.
  - 2015, Taylor, Rietzschel, Danquah i Berry, *Psychotherapy Research*: przegląd
    systematyczny; po terapii poczucie bezpieczeństwa w przywiązaniu rosło, a lęk
    w przywiązaniu spadał. Uczciwa granica: dowody dla unikania były słabsze, a badania
    różniły się metodą (sprawdź w abstrakcie, jak autorzy to formułują).
  - granica wiedzy jej głosem: zmiana jest powolna i przychodzi przez powtarzalne
    doświadczenia, nie przez jedno odkrycie.
- **H2: „The work comes down to three things, in this order:"** (co spróbować)
  1. Settle the body first. Link do `/journal/regulate-nervous-system-between-therapy-sessions`.
  2. Learn your specific triggers (odpowiedź po dniu, „sure" zamiast akapitu, plany bez
     ciebie). Link do `/journal/how-to-identify-emotional-triggers`. Tu inline karta
     `check-ins` (lęk jako obszar do oceniania).
  3. Say the need in its simplest form. Gotowe zdanie: „I'm feeling unsure about us today and
     could use a bit of warmth."
  - H3: „One thing for the people who love someone anxious" (jak u Moniki: bądź
    przewidywalny, „corrective experience" jako termin z literatury przywiązania, bez
    przerzucania na partnera odpowiedzialności za terapię).
  - humor dozwolony w krokach 1-2 (np. „drafting a reply to a reply that hasn't arrived").
- **Akapit o apce (rytm §2.1 pkt 9):** „This is what MindSync's Between-session voice notes
  are for. Log the message you reread, the moment the alarm went off, and what you did next.
  Give it time, and Mood & focus-area trends turns those entries into something you can see:
  [certain people, certain hours, the same switch every time]. Then flag what matters into
  your Workspace and bring it to your next session." (To jest rytm z #24 z poprawionymi
  nazwami funkcji; konkrety wolno zostawić, bo są z tego tematu.)
- **Pytanie do czytelnika:** np. „When someone goes quiet, what's the story your brain starts
  writing?"
- blok `[FEATURES:]`
- **H2: Frequently asked questions**
  - H3: Can anxious attachment be healed?
  - H3: What triggers anxious attachment?
  - H3: What are the signs of anxious attachment?
  - H3: How do I stop being anxiously attached?
  - H3: Does anxious attachment change with age?

**4. Karty funkcji** (bramka: voice-notes, check-ins, mood-trends, workspace, personal-bio;
używamy czterech)
- inline w „The work comes down to three things" (krok 2):
  `[FEATURE: check-ins | Rate the anxiety on the calm days too, because a trigger only looks like a pattern when you have the quiet evenings to compare it with.]`
- blok przed FAQ:
  `[FEATURES: Turning the alarm into something you can read || voice-notes | Thirty seconds out loud while the spiral is running, so tomorrow you can read back what it said instead of guessing. || mood-trends | Weeks of anxious evenings next to steady ones, which is where the real triggers stop hiding. || workspace | The one moment worth unpacking, set aside so it is waiting for you when the session begins.]`

**5. Mapa linkowania**
- `<a href="/journal/how-to-stop-people-pleasing">` anchor „the automatic yes and where it
  comes from" (wstecz do 02, publikacja 2026-09-27; jeśli 02 się opóźni, `[LINK-LATER:]`)
- `<a href="/journal/regulate-nervous-system-between-therapy-sessions">` anchor „settle your
  body before you answer" (krok 1)
- `<a href="/journal/how-to-identify-emotional-triggers">` anchor „finding the triggers that
  are specifically yours" (krok 2)
- `<a href="/journal/racing-thoughts-at-night">` anchor „the version of the spiral that shows
  up at 2 a.m." (sekcja z objawami, jedno zdanie)
- **Landing partner:** `/pre-order/deep-emotional-analysis` (anchor „reading the pattern
  behind the spiral"), jeden raz. Nie używaj anchorów zajętych w partii 3 („a closer read on
  the emotions that keep repeating") ani w `journaling-vs-voice-notes`.

**6. GEO**
- Definicja anxious attachment, 40-60 słów, z informacją o dwóch wymiarach (lęk, unikanie).
- Odpowiedź na „Can anxious attachment be healed?", 50-70 słów, z dwoma badaniami
  (Chopik 2019, Taylor 2015) i zastrzeżeniem, że to średnie, nie obietnica. Najmocniejszy
  kandydat do AI Overviews w partii, bo SERP odpowiada „yes" bez jednego źródła.

**7. Hero**
- Wariant „codzienny moment": telefon leżący ekranem w dół na pościeli, obok kubek, miękkie
  wieczorne światło lampki, paleta sand i mint; bez osoby.
- `hero_image_alt`: „A phone lying face down on bedding next to a mug in warm evening
  lamplight".
- nazwa pliku hero: `anxious-attachment-style-hero.webp`.

**8. Źródła (zweryfikowane 2026-09-25)**
- **POTWIERDZONE.** Fraley R.C., Niedenthal P.M., Marks M., Brumbaugh C., Vicary A., 2006,
  *Journal of Personality* 74:1163-1190, „Adult attachment and the perception of emotional
  expressions: Probing the hyperactivating strategies underlying anxious attachment".
  https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1467-6494.2006.00406.x
  Paradygmat „morph movie"; osoby z wysokim lękiem w przywiązaniu wcześniej dostrzegały
  pojawianie się i znikanie ekspresji emocji.
- **POTWIERDZONE.** Chopik W.J., Edelstein R.S., Grimm K.J., 2019, *Journal of Personality and
  Social Psychology* 116(4):598-611, „Longitudinal changes in attachment orientation over
  a 59-year period". https://pubmed.ncbi.nlm.nih.gov/28771022/ (DOI 10.1037/pspp0000167).
  N = 628, wiek 13-72; lęk w przywiązaniu rośnie do młodej dorosłości i średnio spada
  w średnim i późnym wieku; unikanie spada liniowo. ⚠ Wersja online z 2017, druk 2019: cytuj
  jako 2019.
- **POTWIERDZONE (jakościowo).** Taylor P.J., Rietzschel J., Danquah A., Berry K., 2015,
  *Psychotherapy Research* 25:222-238, „Changes in attachment representations during
  psychological therapy". https://pubmed.ncbi.nlm.nih.gov/24559454/
  (DOI 10.1080/10503307.2014.886791). Przegląd systematyczny: bezpieczeństwo rośnie, lęk
  spada po terapii. ⚠ Liczbę włączonych badań i zdanie o unikaniu podaj tylko po odczycie
  abstraktu (PubMed zwrócił CAPTCHA przy automatycznym odczycie).
- **Czego autor ma NIE twierdzić:**
  - że czytelnik „ma" anxious attachment; wpis opisuje wzorzec, czytelnik sam go rozpoznaje,
  - że da się to „naprawić" w określonym czasie albo określoną metodą (zero „CBT/EMDR leczy
    anxious attachment", co robi SERP),
  - niczego o partnerze czytelnika („your partner is avoidant"),
  - że przywiązanie w dzieciństwie „determinuje" dorosłe relacje (wpływ, nie wyrok),
  - że MindSync zmienia styl przywiązania. Apka daje zapis i obraz wzorca, zmiana dzieje się
    w relacjach i w terapii.

**9. Czego NIE robić**
- Zero quizów i testów stylu przywiązania.
- Zero treści o przemocy w związku i o relacjach, w których lęk jest adekwatną reakcją; to
  inny temat z inną odpowiedzialnością. Jeśli autor czuje potrzebę zastrzeżenia, jedno zdanie
  neutralne: „If the unpredictability is coming from the relationship itself, that's worth
  its own conversation with a professional."
- Nie wchodź w avoidant i disorganized szerzej niż jedno zdanie; to materiał na duet
  w kolejnej partii.
