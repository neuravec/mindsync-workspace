# 02. ROZBUDOWA – lista zmian

> Wpis: `regulate-nervous-system-between-therapy-sessions` (item CMS `69c039b1bf339e69ca1e9d49`).
> Tryb: **edycja żywego itemu w CMS**, nie kolejka dripu. Zmiany addytywne.
> Nowe body: `blog/queue/_02-rozbudowa-output.html`. Źródło: `blog/queue/_02-current-body.html`.
> Data: 2026-08-25. Status prozy: **post-humanizer, po rundzie B4 brand-voice**.
> Werdykt `brand-voice-manager`: DO-POPRAWY (B4) → poprawki naniesione, patrz §7.

---

## 1. Co zostało DODANE i gdzie

Kolejność nowych sekcji zgodna z briefem §3. Wstawki są rozdzielone, nie sklejone w jeden blok,
żeby nie rozerwać istniejącego łuku narracyjnego (badania → praktyka → tracking → CTA).

| # | Nowa sekcja | Miejsce wstawienia | ~słów |
|---|---|---|---|
| A | H2 `What dysregulation actually feels like` (+H3 `In the body`, +H3 `In your head`, + zastrzeżenie) | zaraz po sekcji wprowadzającej `Your nervous system doesn't wait...`, przed `What "nervous system regulation" actually means` | ~340 |
| B | H2 `How long does it take?` | po `4. Vagus nerve stimulation`, czyli po całej sekcji `What actually works: four techniques with real data` | ~340 |
| C | H2 `A quick comparison of what to try` (lista `ul`, 4 pozycje + akapit z uczciwym zastrzeżeniem + akapit domykający) | bezpośrednio po B | ~570 |
| D | H2 `Before and after a session` (+H3 `Twenty minutes before`, +H3 `The hour after`) | bezpośrednio po C, przed istniejącym `The bigger picture: somatic approaches...` | ~430 |
| E | H2 `Frequently asked questions` (5× H3, odpowiedzi 55-70 słów) | na samym końcu wpisu, po `Why tracking changes everything` | ~350 |

Razem ok. **2000 słów nowej treści**; wpis po rozbudowie ma ok. 3900 słów. To świadomie powyżej
widełek z `_format.md` (1100-1600), bo to rozbudowa striking-distance, nie nowy wpis.

### Dlaczego D stoi przed „The bigger picture", a nie na końcu
Brief podaje kolejność nowych sekcji względem siebie, nie każe wstawiać ich ciągiem na końcu.
Gdyby `Before and after a session` trafiło między `What to use when` a `Why tracking changes
everything`, powstałyby **trzy CTA pod rząd** (istniejące zdanie „use MindSync to track your
activation patterns" → nowa karta → istniejąca sekcja CTA). Przesunięcie w górę rozrzedza CTA
i zachowuje istniejące domknięcie wpisu w całości.

### Pokrycie fraz z briefu §2
- `signs of a dysregulated nervous system` → sekcja A + FAQ 2
- `how long does it take to regulate your nervous system` → sekcja B + FAQ 3
- `nervous system regulation exercises`, `somatic exercises for anxiety at home` → sekcja C
- `how to calm your nervous system fast` → FAQ 1 + sekcja C (pozycja „Cold on the face")
- `vagus nerve exercises for anxiety` → FAQ 4 (uczciwie: rozdziela oddech/zimno od klinicznego VNS
  i od „humming/gargling/ear massage")
- `nervous system regulation before therapy session` → sekcja D + FAQ 5
- `window of tolerance` → już było w istniejącej treści (Siegel), nowe sekcje wracają do terminu
  bez powtarzania definicji

### GEO (fragmenty cytowalne)
- Lista objawów dysregulacji: pierwszy akapit sekcji A, 53 słowa, z zastrzeżeniem „a description,
  not a diagnosis" **w tym samym akapicie** (żeby wyjęty z kontekstu nie brzmiał diagnostycznie).
- Odpowiedź „ile to trwa": pierwszy akapit sekcji B, 55 słów, z rozróżnieniem doraźne kontra bazowe.

---

## 2. Czego NIE ruszono (przeniesione znak w znak)

Cała istniejąca treść jest w wyniku **verbatim**, w trzech ciągłych blokach (linie 4-8, 16 i 42
pliku wynikowego), **z dwoma wyjątkami autoryzowanymi przez brand-voice w rundzie B4**
(nazwa czasopisma przy Laborde i wsp. 2022 oraz „a free app" → patrz §7, pozycje 3 i 4).
Poza tymi dwiema poprawkami: zero przeredagowań, zero zmian interpunkcji.

- H1, slug, hero, data publikacji, kategoria: **poza plikiem, nie dotykamy** (publisher edytuje
  wyłącznie `post-body`).
- Sekcja wprowadzająca `Your nervous system doesn't wait for your next appointment`.
- `What "nervous system regulation" actually means` (Siegel, Corrigan/Fisher/Nutt 2010).
- `What polyvagal theory tells us (and what it doesn't)` wraz z zastrzeżeniem „clinically useful
  but scientifically debated" i krytyką 39 ekspertów.
- `What actually works: four techniques with real data` z cytowaniem Laborde i wsp. 2022, Spiegel
  i Yilmaz Balban 2023, przeglądami cold-exposure i trialem VNS.
- `The bigger picture`, `How do you know what's working?`, `What to use when`,
  `Why tracking changes everything` – **łącznie z trzema istniejącymi akapitami o MindSync**.

Istniejąca proza NIE przeszła przez humanizera (jest opublikowana, przepisanie zresetowałoby
dorobek i złamało zasadę addytywności z briefu §7).

---

## 3. Karty funkcji: rachunek i decyzja

**Stan przed rozbudową:** 0 placeholderów `[FEATURE:]`, ale **3 prozatorskie CTA MindSync**
w opublikowanej treści:
1. akapit „MindSync was built for exactly this..." (`How do you know what's working?`),
2. zdanie „If you want to bring real data... use MindSync..." (`What to use when`),
3. cała sekcja `Why tracking changes everything`.

Sufit po rozbudowie: **3 karty/CTA na wpis**. Istniejące 3 CTA są nieusuwalne (brief §7 zakazuje
ruszania istniejących akapitów o MindSync), więc budżet jest formalnie wyczerpany zanim cokolwiek
dodam.

**Decyzja: wstawiam JEDNĄ kartę zamiast dwóch z briefu §4.**

| karta z briefu | decyzja | uzasadnienie |
|---|---|---|
| `[FEATURE: check-ins \| Rate how wound up you were before and after...]` w sekcji C | **ODPUSZCZONA** | Duplikuje istniejący akapit „You check in after stress responses throughout the day", który już stoi w tekście dwa razy. Idea została **w czystej prozie**: akapit domykający sekcję C mówi wprost, żeby oceniać stan przed i po, na tej samej skali, i czytać to po dwóch tygodniach. |
| `[FEATURE: session-debrief \| Catch what came up right after the session...]` w sekcji D | **WSTAWIONA** | Jedyny kąt nierealizowany przez istniejącą prozę (debrief po sesji nie pada nigdzie w opublikowanej wersji), leży w całkowicie nowej sekcji, a `session-debrief` ma status `live` i dokładnie odpowiada akapitowi o godzinie po sesji. |
| blok `[FEATURES:]` | **NIE dodany** | Brief §4 wprost zakazuje przy istniejących kartach/CTA. |

Bilans końcowy: **3 istniejące CTA prozą + 1 karta + 1 zwykły link tekstowy do `/features`**.
Jeśli operator chce trzymać sufit 3 **absolutnie** (licząc kartę jak CTA), do wycięcia jest
jedna linia: `[FEATURE: session-debrief | ...]` w pliku wynikowym (linia 40). Reszta tekstu
zostaje spójna bez niej.

⛔ `therapist-sharing` i `streaks` (status `planned`) nie pojawiają się nigdzie. Nowa treść nie
sugeruje wysyłania czegokolwiek terapeucie z apki ani serii/odznak. Zdania typu „tell your
therapist" i „raise it with a professional" mówią o **rozmowie**, nie o funkcji.

---

## 4. Linkowanie wewnętrzne dodane

| cel | forma | miejsce |
|---|---|---|
| 05 `how-to-prepare-for-a-therapy-session` | `[LINK-LATER: ... \| walking into the session with something to say]` | H3 `Twenty minutes before` |
| 06 `how-to-remember-what-you-talk-about-in-therapy` | `[LINK-LATER: ... \| keeping what the session gave you]` | H3 `The hour after` |
| 07 `what-to-do-between-therapy-sessions` | `[LINK-LATER: ... \| the rest of the week between sessions]` | domknięcie sekcji D |
| `/features` | zwykły `<a href>` | akapit domykający sekcję C |

Wszystkie trzy wpisy partii idą jako `[LINK-LATER:]`, bo okno wykonania rozbudowy (2026-08-28..30)
nie gwarantuje, że 05 i 06 są już opublikowane, a 07 na pewno nie jest (planowany 09-03).
Publisher sam zdecyduje: link albo goły anchor. Zero surowych `[LINK: ...]`.

---

## 5. Źródła nowych twierdzeń (weryfikacja w źródle pierwotnym)

### POTWIERDZONE i użyte

**Heide, F. J., & Borkovec, T. D. (1983). Relaxation-induced anxiety: paradoxical anxiety
enhancement due to relaxation training. *Journal of Consulting and Clinical Psychology*, 51(2),
171-182.**
Zweryfikowane w rekordzie publikacji Penn State (pure.psu.edu) + ERIC EJ280724. Z abstraktu
dosłownie: „30.8% of the total group under progressive relaxation and 53.8% under focused
relaxation reported increased tension due to the relaxation session"; próba: 14 osób z chronicznym
napięciem; progresywna relaksacja dała większe redukcje miar subiektywnych i fizjologicznych oraz
mniej reakcji paradoksalnych. Użyte w sekcji C: (a) pozycja „Progressive muscle relaxation",
(b) akapit o relaxation-induced anxiety. **Liczebność próby podana w tekście**, a procenty opisane
jako „a flag rather than a rate" – bez tego byłoby to nadużycie na n=14.

**Lehrer, P. M., & Gevirtz, R. (2014). Heart rate variability biofeedback: how and why does it
work? *Frontiers in Psychology*, 5, 756.**
Zweryfikowane na frontiersin.org (pełny tekst). Potwierdzone: częstotliwość rezonansowa ok. 0,1 Hz
(sześć oddechów na minutę), poprawa spoczynkowego baroreflex gain przy praktyce dwa razy dziennie
w domu przez ok. trzy miesiące. Użyte w sekcji B i w FAQ 3. Sformułowanie „describe resting
baroreflex gain improving" celowo referuje, nie obiecuje.

### WYCIĘTE / NIEUŻYTE

- **Jakakolwiek liczba „ile tygodni do regulacji"** jako twardy parametr. Nie ma źródła
  pierwotnego, które podaje taki czas dla przeżywanego stanu (nie dla HRV). Zamiast liczby jest
  jawny caveat: literatura mierzy HRV i baroreflex, bo to da się zmierzyć, a „jak szybko przestajesz
  się spinać na widok nazwiska szefa" nie ma czystej liczby.
- **Grossman i Taylor 2007** (krytyka teorii poliwagalnej). Nie dopisane: zastrzeżenie o statusie
  teorii **już jest** w istniejącej treści (39 ekspertów, 2025), a brief §7 zakazuje go osłabiać
  albo dublować.
- **Efekt „humming / gargling / ear massage"**. W FAQ 4 opisane wprost jako „much thinner on
  evidence" bez przypisywania im badania, bo takiego nie potwierdziłem.
- **Skuteczność orientowania się w otoczeniu / nazywania przedmiotów** (grounding). W sekcji C
  podane wyłącznie jako opcja kierująca uwagę na zewnątrz, **bez** twierdzenia o skuteczności.

### ✅ FLAGA ZAMKNIĘTA (poprawka autoryzowana przez brand-voice, runda B4 – patrz §7)

Istniejący akapit mówi: „A 2022 systematic review and meta-analysis published in *Psychophysiology*
by Laborde and colleagues". Weryfikacja: metaanaliza Laborde i wsp. z 2022 („Effects of voluntary
slow breathing on heart rate and heart rate variability: A systematic review and a meta-analysis")
ukazała się w ***Neuroscience & Biobehavioral Reviews*, 138, 104711** (PMID 35623448).
W *Psychophysiology* (2022, 59(1), e13952) Laborde i wsp. opublikowali **badanie**, nie przegląd.
Brand-voice zweryfikował i **autoryzował poprawkę**: nazwa czasopisma zmieniona na
*Neuroscience &amp; Biobehavioral Reviews*, reszta akapitu nietknięta. Nowa proza nigdzie tej
atrybucji nie powiela (sekcja C mówi o efekcie bez podawania czasopisma).

---

## 6. Zgodność z zasadami twardymi

- **Humanizer:** cała nowa proza przeszła przez skill `humanizer` przed zapisem. Wycięte w drugim
  przebiegu: akapit-rozgrzewka pod H2 `A quick comparison`, trzy triady wyliczeniowe, identyczny
  otwieracz „The catch is..." w każdej pozycji listy (teraz cztery różne konstrukcje), kilka
  domknięć akapitu w formie aforyzmu. Sanity check po humanizacji: nazwiska, lata, czasopisma,
  procenty (30.8 / 53.8), n=14 i „three months" nienaruszone; karta i wszystkie `[LINK-LATER:]`
  na miejscu; sens sekcji zachowany.
  *Uwaga:* nie dodawałem pierwszej osoby („I..."), którą skill sugeruje domyślnie, bo opublikowana
  część wpisu jest konsekwentnie w drugiej osobie i mieszanka brzmiałaby jak dwóch autorów.
- **Em-dash:** zero. Sprawdzone mechanicznie na całym pliku wynikowym (U+2014 oraz U+2013), zero
  trafień. Zero krzywych cudzysłowów.
- **HTML RichText-safe:** wyłącznie `h2, h3, p, ul, li, strong, em, a`. Zero `div`, `span`, `table`,
  `style=`, `class=`, `<script>`, `<br>` (sprawdzone grepem).
- **YMYL:** sekcja A ma zastrzeżenie „not a diagnostic checklist" w treści i w akapicie
  domykającym; FAQ 2 powtarza je w skróconej formie (bo FAQ trafia do schema i AI Overviews
  wyjęte z kontekstu). Zimno ma notkę „if you have a heart condition, ask your doctor".
  Zero diagnozowania, zero obietnic leczniczych, zero „resetu układu nerwowego", zero tematów
  kryzysowych, zero odradzania terapii lub leków.
- **Bez cen**, bez wymyślonych nazw ekranów, bez `[VERIFY-UI: ...]` (nowa treść nie nazywa żadnego
  ekranu apki).

---

## 7. Runda B4 (werdykt brand-voice: DO-POPRAWY) – naniesione zmiany

### 1. Kontrakcje w nowych sekcjach A-E (31 podmian, mechanicznie, bez ponownego humanizera)
`will not settle` → `won't settle` · `That is a description` → `That's a description` ·
`before you have remembered` → `before you've remembered` · `There is often` → `There's often` ·
`would not normally register` → `wouldn't normally register` · `it is not meant` → `it's not meant` ·
`If it is persistent` → `If it's persistent` · `you are reading` → `you're reading` ·
`that is a conversation` → `that's a conversation` · `while you are doing it` (2×) →
`while you're doing it` · `you cannot feel` → `you can't feel` · `whatever else you are carrying` →
`you're carrying` · `what you are working on` → `what you're working on` · `you do not have` →
`you don't have` · `you will cough` → `you'll cough` · `you are too activated` (2×, sekcja C i FAQ 1) →
`you're too activated` · `It is also unpleasant` → `It's also unpleasant` · `you are not doing it wrong` →
`you're not doing it wrong` · `what is in it` → `what's in it` · `That is the idea behind` →
`That's the idea behind` · `you will agree` → `you'll agree` · `now you are in the parking lot` →
`now you're in the parking lot` · `you would use anywhere else` → `you'd use anywhere else` ·
`it is also the first thing` → `it's also the first thing` · `will not look like` → `won't look like` ·
`is not the same thing` → `isn't the same thing` · `Arriving calm is not the target` →
`Arriving calm isn't the target` · plus 2 kontrakcje w zdaniach z pozycji 2 niżej.

Nietknięte celowo (kontrakcja niegramatyczna albo nienaturalna): `rate how wound up you are before
and after`, `neither is meant to`, `This is a description, not a diagnostic list` (FAQ 2),
`Which of these does anything for you is a question about you`. Cytaty, nazwiska, lata, czasopisma
i liczby bez zmian.

### 2. Comma splice (sekcja D, H3 `Twenty minutes before`)
przed: `This is not the moment to try a technique you read about this morning, it is the moment to run one you already know.`
po: `This isn't the moment to try a technique you read about this morning. It's the moment to run one you already know.`
(rozbicie na dwa zdania zamiast średnika: pasuje do rytmu „zdanie długie, zdanie krótkie" z reszty
wpisu). Akapit przepuszczony przez `humanizer` na poziomie akapitu: bez zastrzeżeń, brak AI-tells.

### 3. Autoryzowana poprawka w STARYM tekście: atrybucja Laborde 2022
przed: `A 2022 systematic review and meta-analysis published in <em>Psychophysiology</em> by Laborde and colleagues found`
po: `A 2022 systematic review and meta-analysis published in <em>Neuroscience &amp; Biobehavioral Reviews</em> by Laborde and colleagues found`
Podstawa: metaanaliza slow breathing = *Neuroscience &amp; Biobehavioral Reviews* 2022;138:104711
(PMID 35623448); w *Psychophysiology* 2022;59(1):e13952 ukazało się ich **badanie**, nie przegląd.
Ampersand zapisany jako `&amp;` (wzorzec z istniejącej treści: „Baylor Scott &amp; White").
Reszta akapitu nietknięta.

### 4. Autoryzowana poprawka w STARYM tekście: „free app"
przed: `MindSync is a free app built for this specific gap:`
po: `MindSync is built for this specific gap:`
Wybrane zamiast wariantu z „free trial", bo krótsze, nie wprowadza do treści tematu cennika
(zasada „zero cen w treści") i nie wymaga przebudowy zdania. **Do potwierdzenia przez operatora
przy publikacji** (poprawka idzie na żywo razem z rozbudową).

### 5. Karta `[FEATURE: session-debrief]` ZOSTAJE (decyzja brand-voice)
Sekcja §3 tego dokumentu opisuje ją jako opcjonalną do wycięcia przy twardym sufcie 3 CTA.
**Ta opcja jest nieaktualna: karta zostaje.** Bilans końcowy: 3 istniejące CTA prozą + 1 karta
+ 1 zwykły link do `/features`.
Dublet frazy: nowa proza miała `The honest caveat:` w sekcji B, a ta fraza jest już w opublikowanym
tekście tej samej strony (sekcja o teorii poliwagalnej).
przed: `The honest caveat: this literature measures heart rate variability and baroreflex function, because those can be measured.`
po: `This is where the numbers run out. The literature measures heart rate variability and baroreflex function, because those can be measured.`
Akapit przepuszczony przez `humanizer` na poziomie akapitu (nowy opener nie jest signpostem ani
frazą z listy AI-vocabulary; treść i caveat bez zmian). Kontrola: `The honest caveat` występuje
teraz w pliku **dokładnie raz**, w starym tekście.

### 6. Ruling dywizów, cyfr i procentów w nowej prozie
- `Ten to fifteen minutes` → `10 to 15 minutes` (reguła: powyżej dziewięciu cyframi; dodatkowo lista
  porównawcza ma być skanowalna)
- `ten quiet minutes` → `10 quiet minutes` (ta sama reguła)
- `A boring twice-a-day one` → `A boring one, twice a day,` (zbędny dywiz w parze wyrazowej;
  „twice daily" zostaje w zdaniu obok, bo referuje protokół z badania)
- Bez zmian, świadomie: `30.8%` / `53.8%` (procenty zawsze cyframi, OK), `15 to 30 seconds`,
  `20 minutes`, `4am`, `10pm`, `14 adults`, `twice-daily practice` (złożenie techniczne),
  `meditation-style`, `mid-crisis`, `relaxation-induced anxiety` (termin własny).
- H3 `Twenty minutes before` zostaje słownie: nagłówek, pozycja inicjalna zdania, brzmienie
  z briefu §3; w prozie tej samej sekcji jest `20 minutes` i to jest zamierzone.

### Kontrola po rundzie B4
Zero U+2014 i U+2013, zero krzywych cudzysłowów i apostrofów (wszystkie kontrakcje na prostym `'`),
zero `free app`, zero `Psychophysiology`, `The honest caveat` = 1 wystąpienie (stary tekst).
Tagi nadal wyłącznie `h2, h3, p, ul, li, strong, em, a`.

---

## 8. Co dalej

1. Akcept `brand-voice-manager` (tekst EN, wersja post-humanizer).
2. `seo-tech-lead`: item ma teraz FAQ, więc `schema-jsonld` wymaga **dopisania grafu FAQPage**
   do istniejącego BlogPosting (5 pytań, brzmienie H3 dokładnie jak w pliku wynikowym).
   Warto też odświeżyć `dateModified`.
3. `webflow-publisher`: podmiana **wyłącznie pola `post-body`** w itemie
   `69c039b1bf339e69ca1e9d49`. Slug, `name` (H1), `main-image`, `category` i data publikacji
   bez zmian. Karta `[FEATURE:]` i trzy `[LINK-LATER:]` rozwiązywane normalną ścieżką
   `scripts/webflow/blog-publish.ps1`.
4. Po ok. miesiącu: `scripts/gsc/blog-partia-frazy.py` na tym slugu, podmiana pytań FAQ na realne
   zapytania z GSC i sprawdzenie, czy pozycja ruszyła z 14.7.
