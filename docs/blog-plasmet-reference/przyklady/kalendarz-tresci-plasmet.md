# Kalendarz treści — blog sklep.plasmet.pl

> **Cel:** zbudować topical authority w branży techniczno-budowlanej, zlikwidować lukę „brak bloga"
> (audyt treści 32/100), dostarczać magnesy SEO i ruch informacyjny, który spina się z kategoriami sklepu.
> **Tryb:** publikacja **co 2 dni** (drip-publisher), ciągły program treści — nie jednorazowe zapełnienie.
> **Źródła:** `docs/sklep-i-rynek.md`, `docs/seo-stan-obecny.md`, `..\seo\content-quality-report.md`,
> `..\seo\competitor-pages\strategia-stron-porownawczych.md`, `..\seo\fixes\10-category-meta-descriptions.md`.
>
> **Status danych (AKTUALIZACJA 2026-08-11): realne dane GSC są DOSTĘPNE i obowiązkowe.** Estymaty
> intencyjne z pierwotnej wersji tego pliku zastępują dane z GSC API: `scripts/gsc/blog-tematy.py`
> (frazy per wpis + luki tematyczne + frazy rankingowe → `seo/blog/gsc-frazy/BRIEF-blog.md`),
> `kategorie-frazy.py` (frazy kategorii) i `frazy-brief.py` (frazy kart). Procedura doboru tematów
> partii: `blog/queue/_format.md`, sekcja „Źródło tematów". Ahrefs MCP niedostępny (Insufficient plan)
> — nie planować wokół niego. Nadrzędny kierunek: `docs/strategia-seo-2026-08.md` (duety
> poradnik↔kategoria, blog mierzony cytowaniami/asystami, nie sesjami).

---

## 1. Strategia klastrów (topical authority)

Osiem klastrów spiętych z drzewem kategorii (8 kategorii głównych wg `10-category-meta-descriptions.md`).
Model **pillar + supporting**: każdy klaster ma stronę-filar (zwykle kategoria sklepu z rozbudowaną
treścią SEO LUB duży poradnik blogowy) oraz wpisy wspierające linkujące „w górę" do filaru i „w bok"
do siebie nawzajem. Blog **uzupełnia**, a nie duplikuje stron porównawczych z `..\seo\competitor-pages\`
(te targetują frazy „X vs Y / alternatywy / ranking sklepów" — blog targetuje „jak wybrać / how-to / FAQ").

### Klaster A — Milwaukee (akumulatorowe / systemy bateryjne) — PRIORYTET #1
- **Filar:** kategoria `/elektronarzedzia` (+ landing marki Milwaukee) z treścią SEO.
- **Linkuje do:** elektronarzędzia, narzędzia akumulatorowe, osprzęt do elektronarzędzi.
- **Intencja:** komercyjno-informacyjna (wybór systemu M12/M18, dobór akumulatorów, „czy warto").
- **Dlaczego potencjał:** Plasmet jest **autoryzowanym dystrybutorem Milwaukee** (3 369 poz. w feedzie) —
  najmocniejszy magnes E-E-A-T i intencji zakupowej. Marka generuje duży wolumen brandowy; konkurenci
  (bezprzewodu, e-milw, ECT) walczą o te frazy, ale autoryzacja + 45 lat to nasz wyróżnik. Wpisy zasilają
  też strony „Milwaukee vs Makita/DeWalt/Bosch" z planu competitor-pages (linkowanie wzajemne).

### Klaster B — Elektronarzędzia: poradniki zakupowe (jak wybrać / rankingi) — PRIORYTET #1
- **Filar:** kategoria `/elektronarzedzia`.
- **Linkuje do:** wiertarko-wkrętarki, szlifierki, pilarki, młotowiertarki, mieszadła (Collomix).
- **Intencja:** informacyjna z silną komercyjną „końcówką" (poradnik → kategoria → produkt).
- **Dlaczego potencjał:** „jak wybrać wiertarko-wkrętarkę", „ranking szlifierek" to evergreen o wysokim
  wolumenie — każdy konkurent ma taki poradnik (SERP potwierdza popyt). To nasze drzwi do ruchu TOFU,
  który konwertujemy linkowaniem do kategorii i produktów.

### Klaster C — Chemia budowlana / uszczelnianie i klejenie — PRIORYTET #1
- **Filar:** kategoria `/chemia-budowlana` (Den Braven, Bostik — autoryzacja Den Braven).
- **Linkuje do:** silikony, pianki montażowe, kleje montażowe, uszczelniacze, impregnaty.
- **Intencja:** informacyjna „jaki X do Y" o bardzo wysokiej intencji zakupowej (problem → produkt).
- **Dlaczego potencjał:** „jaki silikon do łazienki", „czym kleić lustro", „pianka pistoletowa czy wężyk"
  to klasyczne frazy problemowe z natychmiastową konwersją na konkretny SKU. Autoryzacja Den Braven +
  marka własna Polifarb Kalisz dają unikalny kąt ekspercki. Świetny materiał pod GEO (definicje, tabele).

### Klaster D — Technika zamocowań — PRIORYTET #2
- **Filar:** kategoria `/technika-zamocowan` (Wkręt-met).
- **Linkuje do:** kołki rozporowe, wkręty, kotwy, złącza ciesielskie, śruby.
- **Intencja:** informacyjna techniczna („jaki kołek do gazobetonu", „dobór wkrętów do drewna").
- **Dlaczego potencjał:** wąskie, ale wysoko-konwertujące frazy z małą konkurencją treściową; idealne pod
  AI Overviews (tabele dobór materiał → mocowanie). Buduje autorytet techniczny taniej niż klaster A/B.

### Klaster E — Materiały ścierne i osprzęt (Klingspor) — PRIORYTET #2
- **Filar:** kategoria `/osprzet-do-elektronarzedzi` (największa kategoria, ~2 000 poz.; Klingspor).
- **Linkuje do:** tarcze do cięcia, papier ścierny, wiertła, tarcze diamentowe, ściernice.
- **Intencja:** informacyjna („jaka tarcza do metalu/betonu", „gradacja papieru ściernego").
- **Dlaczego potencjał:** największa kategoria asortymentowa = największa pula podkategorii z thin
  contentem do zasilenia ruchem. Frazy „jaka tarcza do…" mają stały popyt i niedoinwestowaną treść u
  konkurencji regionalnej.

### Klaster F — Wentylacja (Awenta) — PRIORYTET #2
- **Filar:** kategoria `/systemy-wentylacyjne` (Awenta, 860 poz.).
- **Linkuje do:** wentylatory łazienkowe, kratki wentylacyjne, kanały, anemostaty.
- **Intencja:** informacyjna domowa („jaki wentylator do łazienki bez okna", „dobór wentylacji").
- **Dlaczego potencjał:** Awenta = drugi po Milwaukee wolumen pozycji, a temat „wentylator łazienkowy"
  ma duży popyt prosumencki i niemal zerową konkurencję treściową w naszym profilu. Nisza do zdominowania.

### Klaster G — BHP / ochrona indywidualna — PRIORYTET #3
- **Filar:** kategoria `/bhp`.
- **Linkuje do:** kaski ochronne, rękawice robocze, okulary ochronne, ochronniki słuchu.
- **Intencja:** informacyjna z elementem normatywnym („kategorie rękawic EN 388", „klasy kasków").
- **Dlaczego potencjał:** treść „compliance" (normy, kategorie ochrony) jest **idealnie cytowalna w AI**
  (definicje, tabele klas) i buduje E-E-A-T. Niższy wolumen, ale wysoka wartość B2B i autorytet.

### Klaster H — Sezonowe / ogród + okołoporadnikowe (rotacja) — PRIORYTET #3
- **Filar:** kategorie `/narzedzia-ogrodowe`, `/chemia-budowlana` (zależnie od sezonu).
- **Linkuje do:** sekatory, narzędzia ogrodowe; zimą: chemia/uszczelnianie, montaż.
- **Intencja:** informacyjna sezonowa (wiosna: ogród; jesień/zima: uszczelnianie, wentylacja).
- **Dlaczego potencjał:** łapie piki sezonowe (Google Trends), utrzymuje świeżość bloga, daje pretekst do
  aktualizacji evergreenów. Rotacyjny — temat wybierany pod aktualny miesiąc w kalendarzu.

### Klaster I — Narzędzia ręczne (NOWY, otwarty partią 45-51, lipiec 2026) — PRIORYTET #2
- **Filar:** kategoria `/narzedzia-reczne` (klucze, młotki, wkrętaki, poziomice, przymiary, zestawy).
- **Linkuje do:** klucze dynamometryczne, poziomice, zestawy narzędziowe (Richmann, marka własna Plasmet).
- **Intencja:** informacyjna → komercyjna (prosument + B2B/motoryzacja).
- **Dlaczego potencjał:** cała kategoria sklepu była w 0% pokryta treścią blogową — zerowa konkurencja
  treściowa w naszym profilu, największa dźwignia z dostępnych na lipiec 2026. Zaseedowany partią 45-51:
  pillar-hub „zestaw narzędzi do domu i warsztatu" (#49) + wpisy specjalistyczne „klucz dynamometryczny"
  (#47) i „poziomica" (#51).
- **Bank na przyszłe partie (niewykorzystane jeszcze):** nasadki i klucze nasadowe 1/4"-1/2", wkrętaki i
  groty PH/PZ/Torx, młotki (rodzaje i zastosowania), miary i przymiary, imadła i ściski, szczypce/kombinerki
  (dobór typów).

---

## 1a. Kategorie blogowe (wymiar FORMATU — od partii 52-71, lipiec 2026)

Klastry (wyżej) opisują TEMATYKĘ; kategorie blogowe opisują FORMAT wpisu. Do partii 51 wszystkie wpisy
szły do jednej kategorii „Poradnik" — od partii 52-71 blog ma **5 kategorii** (utworzone w `news-categories`
2026-07-16, id w nawiasie). Decyzja usera 2026-07-16; 13 starszych wpisów przepięto do pasujących kategorii.

| Kategoria (id) | Format | Struktura obowiązkowa |
|---|---|---|
| **Poradnik** (5) | klasyczne „jak wybrać X" | tabela doboru + FAQ |
| **Krok po kroku** (6) | instrukcja wykonania (HowTo) | lista narzędzi/materiałów → ponumerowane kroki H2/H3 → częste błędy → FAQ; kandydat na schema `HowTo` |
| **Problemy i porady** (7) | troubleshooting „dlaczego X / co zrobić gdy" | objaw → tabela objaw-przyczyna-rozwiązanie → naprawa → zapobieganie → FAQ |
| **Porównania** (8) | X vs Y (produkty, technologie, marki) | tabela porównawcza + werdykt „kiedy X, kiedy Y" |
| **Normy i BHP** (9) | compliance B2B (normy EN, klasy, przepisy) | tabele klas/norm, cytowalne definicje (GEO) |

Uzasadnienie (GSC 2026-06): popyt = chemia problem→produkt (Krok po kroku, Problemy), BHP compliance
(największy gap 14k wyśw./4 kliki), frazy „X czy Y" konwertują (kliny F1/F2 poz. 2-5). Kategoria
„Strefa marki/nowości" ODRZUCONA — brak popytu informacyjnego Milwaukee w danych.

---

## 1b. Partia 52-71 (24.07-12.08.2026, drip codzienny) — briefy: `blog/queue/_batch-2026-08-briefs.md`

Mix: 6× Krok po kroku, 5× Problemy i porady, 3× Porównania, 3× Normy i BHP, 3× Poradnik (klaster I).
Tematy z realnego popytu GSC: folia w płynie, malowanie metalu (Ferrobond/Polifarb Kalisz), akryle,
kliny F1/F2, mała szlifierka M12, kombinerki/obcinaki; końcówka partii łapie wczesną jesień (uszczelnianie,
kondensacja). Pełna tabela 20 tematów w pliku briefs.

---

## 2. Bank tematów (~30) — tabela

Legenda priorytetu: **W** = wysoki, **Ś** = średni, **N** = niski (długi ogon / uzupełnienie klastra).
Typ: PZ = poradnik zakupowy, HT = how-to, POR = porównanie X vs Y, FAQ = FAQ/GEO, LST = lista/ranking.

| # | Tytuł roboczy | Typ | Intencja | Fraza główna | Frazy poboczne | Prio | Linkowanie wewn. (kategoria → produkty) | Klaster |
|---|---|---|---|---|---|---|---|---|
| 1 | Milwaukee M12 czy M18 — który system akumulatorowy wybrać | PZ | kom-inf | milwaukee m12 czy m18 | różnica m12 m18, system akumulatorowy milwaukee, milwaukee 12v vs 18v | W | /elektronarzedzia → akumulatorowe Milwaukee, akumulatory M18 | A |
| 2 | Jak wybrać wiertarko-wkrętarkę — poradnik 2026 | PZ | inf→kom | jak wybrać wiertarko-wkrętarkę | wiertarko-wkrętarka jaką wybrać, moment obrotowy wkrętarki, 12v czy 18v | W | /elektronarzedzia → wiertarko-wkrętarki Milwaukee | B |
| 3 | Jaki silikon do łazienki — sanitarny czy uniwersalny | PZ | inf→kom | jaki silikon do łazienki | silikon sanitarny den braven, silikon do glazury, silikon przeciwgrzybiczny | W | /chemia-budowlana → silikony Den Braven | C |
| 4 | Ranking akumulatorowych narzędzi Milwaukee — przegląd serii | LST | kom-inf | narzędzia milwaukee ranking | najlepsze narzędzia milwaukee, milwaukee fuel co to, seria milwaukee | W | /elektronarzedzia → Milwaukee FUEL, zestawy M18 | A |
| 5 | Milwaukee FUEL — co oznacza i czy warto dopłacić | FAQ | kom-inf | milwaukee fuel co to | technologia fuel milwaukee, silnik bezszczotkowy milwaukee, fuel vs zwykłe | W | /elektronarzedzia → Milwaukee FUEL | A |
| 6 | Jaka tarcza do cięcia metalu, betonu i drewna — dobór | PZ | inf→kom | jaka tarcza do cięcia metalu | tarcza do betonu, tarcza diamentowa do czego, dobór tarczy do szlifierki | W | /osprzet-do-elektronarzedzi → tarcze Klingspor | E |
| 7 | Jaki kołek do gazobetonu, betonu i pustaka — tabela doboru | PZ | inf→kom | jaki kołek do gazobetonu | kołek rozporowy do betonu, dobór kołków, kołek do pustaka | W | /technika-zamocowan → kołki Wkręt-met | D |
| 8 | Jaki wentylator do łazienki bez okna — poradnik | PZ | inf→kom | wentylator do łazienki bez okna | wentylator łazienkowy z czujnikiem wilgotności, wentylator awenta, dobór wentylatora | W | /systemy-wentylacyjne → wentylatory Awenta | F |
| 9 | Pianka montażowa pistoletowa czy wężykowa — różnice | PZ | inf→kom | pianka montażowa pistoletowa czy wężykowa | piana montażowa den braven, jaka pianka do okien, niskoprężna pianka | W | /chemia-budowlana → pianki Den Braven | C |
| 10 | Jak wybrać szlifierkę kątową — średnica, moc, zastosowanie | PZ | inf→kom | jak wybrać szlifierkę kątową | szlifierka 125 czy 230, szlifierka akumulatorowa milwaukee, moc szlifierki | W | /elektronarzedzia → szlifierki kątowe | B |
| 11 | Czym kleić lustro, glazurę i panele — przewodnik po klejach | PZ | inf→kom | czym kleić lustro | klej montażowy bostik, klej do luster, klej mamut den braven | W | /chemia-budowlana → kleje montażowe Bostik | C |
| 12 | Jak wybrać młotowiertarkę (SDS-Plus vs SDS-Max) | PZ | inf→kom | jak wybrać młotowiertarkę | sds plus czy sds max, młotowiertarka do betonu, młot udarowo-obrotowy | Ś | /elektronarzedzia → młotowiertarki | B |
| 13 | Akumulatory Milwaukee M18 — pojemność, ładowanie, kompatybilność | FAQ | kom-inf | akumulatory milwaukee m18 | milwaukee m18 5ah czy 8ah, ładowarka milwaukee, kompatybilność baterii m18 | Ś | /elektronarzedzia → akumulatory i ładowarki M18 | A |
| 14 | Jaki impregnat do drewna na zewnątrz — dobór ochrony | PZ | inf→kom | jaki impregnat do drewna na zewnątrz | impregnat do tarasu, lakierobejca, ochrona drewna den braven | Ś | /chemia-budowlana → impregnaty | C |
| 15 | Gradacja papieru ściernego — jaką ziarnistość wybrać | FAQ | inf | gradacja papieru ściernego | ziarnistość papieru ściernego tabela, papier ścierny do drewna, klingspor papier | Ś | /osprzet-do-elektronarzedzi → papiery ścierne Klingspor | E |
| 16 | Rękawice robocze — kategorie ochrony i norma EN 388 | FAQ | inf | rękawice robocze en 388 | klasy rękawic roboczych, rękawice antyprzecięciowe, dobór rękawic bhp | Ś | /bhp → rękawice robocze | G |
| 17 | Jak dobrać wkręty do drewna, płyty i konstrukcji | PZ | inf→kom | jak dobrać wkręty do drewna | wkręty ciesielskie, długość wkręta, wkręty wkręt-met | Ś | /technika-zamocowan → wkręty Wkręt-met | D |
| 18 | Mieszadło do zapraw i kleju — jak dobrać (Collomix) | PZ | inf→kom | mieszadło do zapraw | mieszadło collomix, mieszarka do gładzi, koszyk mieszający dobór | Ś | /elektronarzedzia → mieszadła Collomix | B |
| 19 | Jaka kratka wentylacyjna i anemostat — dobór do pomieszczenia | PZ | inf→kom | jaka kratka wentylacyjna | kratka wentylacyjna awenta, anemostat nawiewny, dobór kratki | Ś | /systemy-wentylacyjne → kratki Awenta | F |
| 20 | Kask ochronny na budowę — klasy, normy, kiedy wymieniać | FAQ | inf | kask ochronny normy | kask budowlany en 397, data ważności kasku, dobór kasku bhp | Ś | /bhp → kaski ochronne | G |
| 21 | Jak wybrać pilarkę — łańcuchowa, tarczowa, szablasta | PZ | inf→kom | jak wybrać pilarkę | pilarka akumulatorowa milwaukee, piła szablasta do czego, pilarka tarczowa | Ś | /elektronarzedzia → pilarki Milwaukee | B |
| 22 | Silikon, akryl czy uszczelniacz MS — czym się różnią | FAQ | inf | silikon czy akryl | uszczelniacz ms polimer, akryl malarski den braven, kiedy silikon kiedy akryl | Ś | /chemia-budowlana → uszczelniacze | C |
| 23 | Jak wybrać kotwę i kiedy zamiast kołka — przewodnik | PZ | inf→kom | jak wybrać kotwę | kotwa chemiczna czy mechaniczna, kotwa do betonu, dobór kotwy | N | /technika-zamocowan → kotwy | D |
| 24 | Okulary i ochronniki słuchu — dobór ochrony przy elektronarzędziach | FAQ | inf | ochrona słuchu przy pracy | okulary ochronne norma, ochronniki słuchu snr, bhp przy szlifowaniu | N | /bhp → okulary, ochronniki słuchu | G |
| 25 | Tarcze diamentowe — segmentowa, ciągła, turbo: różnice | FAQ | inf→kom | tarcza diamentowa rodzaje | tarcza diamentowa do betonu, segmentowa czy ciągła, tarcza do glazury | N | /osprzet-do-elektronarzedzi → tarcze diamentowe | E |
| 26 | Jak przygotować ogród na wiosnę — sekatory i narzędzia (sezon) | LST | inf→kom | narzędzia ogrodowe na wiosnę | jaki sekator wybrać, narzędzia do ogrodu wiosna, przegląd narzędzi ogrodowych | N | /narzedzia-ogrodowe → sekatory | H |
| 27 | Jak uszczelnić okna i drzwi przed zimą (sezon) | HT | inf→kom | jak uszczelnić okna przed zimą | uszczelka do okien, pianka do okien, taśma uszczelniająca | N | /chemia-budowlana, /akcesoria-budowlane → uszczelki, pianki | H |
| 28 | Den Braven kontra Soudal — który silikon i pianka lepsze | POR | kom-inf | den braven czy soudal | porównanie silikonów, soudal vs den braven pianka, najlepszy silikon | Ś | /chemia-budowlana → Den Braven (link do str. porównawczej z competitor-pages) | C |
| 29 | Jak czytać oznaczenia akumulatorów (Ah, V, Li-Ion) — słowniczek | FAQ | inf | oznaczenia akumulatorów narzędzi | co znaczy ah w baterii, napięcie a pojemność, li-ion w narzędziach | N | /elektronarzedzia → akumulatory | A |
| 30 | Folie i taśmy budowlane — jaką folię ochronną wybrać | PZ | inf→kom | jaka folia ochronna budowlana | folia malarska, taśma malarska do czego, folia budowlana grubość | N | /akcesoria-budowlane → folie, taśmy | H |

> **Pokrycie klastrów:** A=6 (#1,4,5,13,29 + zasila POR Milwaukee vs X), B=6 (#2,10,12,18,21 + ranking),
> C=7 (#3,9,11,14,22,27,28), D=3 (#7,17,23), E=3 (#6,15,25), F=2 (#8,19), G=3 (#16,20,24), H=3 (#26,27,30).
> Rozkład świadomy: priorytet na klastry A/B/C (najwyższa intencja zakupowa + autoryzacje), reszta buduje
> szerokość topical authority i zasila thin-content podkategorie ruchem informacyjnym.

---

## 3. Pierwsza partia — 8 wpisów (kolejność publikacji, co 2 dni)

Mix zgodny z założeniem: 2–3 magnesy Milwaukee, 2 evergreen poradniki zakupowe, 1 porównanie,
1 sezonowy, 1 FAQ pod GEO. Start zakłada „mocne otwarcie" — najpierw najwyższa intencja i najsilniejszy
wyróżnik (Milwaukee + autoryzacje), żeby pierwsze zaindeksowane wpisy bloga od razu pracowały na konwersję.

| Kolejność | Dzień (T+) | # | Tytuł | Rola w partii | Uzasadnienie (1 zdanie) |
|---|---|---|---|---|---|
| 1 | T+0 | 2 | Jak wybrać wiertarko-wkrętarkę — poradnik 2026 | Evergreen PZ (magnes ruchu) | Najszerszy evergreen w branży i naturalny „pierwszy wpis bloga", który od razu linkuje do kategorii elektronarzędzi i produktów Milwaukee. |
| 2 | T+2 | 1 | Milwaukee M12 czy M18 — który system wybrać | Magnes Milwaukee #1 | Eksponuje autoryzację Milwaukee na frazie o wysokiej intencji zakupowej — najmocniejszy wyróżnik Plasmet wchodzi wcześnie. |
| 3 | T+4 | 3 | Jaki silikon do łazienki — sanitarny czy uniwersalny | Evergreen PZ + autoryzacja Den Braven | Klasyczna fraza problemowa z natychmiastową konwersją na SKU; otwiera klaster chemii i pokazuje drugą autoryzację. |
| 4 | T+6 | 5 | Milwaukee FUEL — co oznacza i czy warto dopłacić | Magnes Milwaukee #2 + FAQ/GEO | Krótkie, „cytowalne" wyjaśnienie pojęcia, którego szukają kupujący Milwaukee — idealne pod AI Overviews i upsell. |
| 5 | T+8 | 7 | Jaki kołek do gazobetonu, betonu i pustaka — tabela | FAQ pod GEO (passage-citable) | Tabela dobór materiał→mocowanie to wzorcowy format pod cytowanie w AI; niska konkurencja treściowa, szybkie wejście. |
| 6 | T+10 | 6 | Jaka tarcza do cięcia metalu, betonu i drewna | Evergreen PZ (osprzęt) | Zasila największą kategorię (osprzęt ~2 000 poz.) ruchem i linkuje do tarcz Klingspor — szeroki długi ogon „jaka tarcza do…". |
| 7 | T+12 | 8 | Jaki wentylator do łazienki bez okna | Sezonowy/niszowy magnes | Wysoki popyt prosumencki przy niemal zerowej konkurencji treściowej — szansa zdominowania niszy Awenta od startu. |
| 8 | T+14 | 28 | Den Braven kontra Soudal — silikon i pianka | Porównanie X vs Y | Domyka pierwszą partię formatem porównawczym; linkuje do strony competitor-pages „Den Braven vs Soudal" i wzmacnia klaster chemii. |

**Dlaczego ta kolejność (skrót):** otwieramy najszerszym evergreenem (ruch + wewnętrzne linkowanie),
zaraz po nim wchodzą dwa magnesy Milwaukee i autoryzacja Den Braven (intencja zakupowa + E-E-A-T), w
środku partii sadzimy dwa wpisy „GEO-first" (FAQ FUEL + tabela kołków) jako przynętę pod AI Overviews,
a domykamy porównaniem, które spina blog ze stronami porównawczymi. Każdy wpis linkuje **do kategorii**
(ciągłość SEO), nie tylko do pojedynczych produktów.

---

## 4. Wytyczne pod GEO / AI Overviews

**Zasada:** projektować wybrane wpisy jako **passage-level citable** — samodzielne fragmenty (40–60 słów),
które AI może zacytować bez kontekstu. Format, który wygrywa cytowania: **definicja + bezpośrednia
odpowiedź na pytanie w pierwszych 2 zdaniach + tabela porównawcza + sekcja FAQ z `FAQPage` schema**
(schema wdraża `seo-tech-lead`; my dostarczamy strukturę treści i pytania).

**Wpisy projektowane priorytetowo pod GEO (typ FAQ + tabele):**

| # | Wpis | Element cytowalny pod AI |
|---|---|---|
| 5 | Milwaukee FUEL — co oznacza | Definicja „FUEL" w 1. akapicie (40–50 słów) + tabela FUEL vs zwykłe (silnik, moc, cena). |
| 7 | Jaki kołek do gazobetonu/betonu/pustaka | **Tabela doboru** materiał podłoża → typ kołka → obciążenie; bezpośrednie odpowiedzi „do gazobetonu użyj…". |
| 16 | Rękawice robocze EN 388 | Tabela klas ochrony (ścieranie/przecięcie/rozdarcie/przebicie) + definicja oznaczeń normy. |
| 22 | Silikon czy akryl | Definicje obu + tabela „kiedy silikon / kiedy akryl" (wilgoć, malowanie, ruch spoiny). |
| 13 | Akumulatory Milwaukee M18 | FAQ: pojemność vs czas pracy, kompatybilność, „5Ah czy 8Ah" — krótkie pytania-odpowiedzi. |
| 15 | Gradacja papieru ściernego | **Tabela ziarnistości** (zakres → zastosowanie) — wzorcowy obiekt do cytowania. |
| 20 | Kask ochronny — normy | Definicja EN 397 + tabela „kiedy wymienić kask" + data ważności. |
| 29 | Oznaczenia akumulatorów (Ah, V, Li-Ion) | Słowniczek pojęć — każde hasło jako samodzielny, cytowalny mikro-passage. |

**Wytyczne formatu dla blog-writera (egzekwuje `humanizer` na prozie, akcept `brand-voice-manager`):**
- Pierwsze 2 zdania = bezpośrednia odpowiedź na frazę-pytanie (TL;DR przed rozwinięciem).
- Każdy wpis kończy sekcją **FAQ (3–5 pytań)** sformułowaną jak realne zapytania (pod `FAQPage` schema).
- Tam, gdzie jest „dobór / różnice / klasy" — **tabela** zamiast prozy (AI i ludzie wolą tabele).
- Konkrety techniczne **weryfikowane** (parametry, normy, oznaczenia), nie ogólniki — to E-E-A-T i ochrona
  przed błędnym cytowaniem w AI.
- Naturalne wzmianki marki w kontekście autoryzacji („jako autoryzowany dystrybutor Milwaukee / Den Braven")
  budują brand-mention signals dla LLM — bez keyword-stuffingu.

---

## Załącznik — zapytania do pobrania realnych danych (sesja główna)

Wolumeny w tabeli to estymaty. Przed finalizacją briefów potwierdzić w sesji głównej (narzędzia mogą być
niedostępne w subagencie):

- **Ahrefs Keywords Explorer** (rynek `pl`, język polski) — pobrać volume + KD + parent topic dla fraz
  głównych z kolumny „Fraza główna" (priorytet: wszystkie z prio **W**, następnie **Ś**).
- **Ahrefs Organic Keywords** — domeny konkurentów (narzedzia.pl, swiatnarzedzi.pl, seger.pl, bezprzewodu.pl)
  → identyfikacja luk: frazy poradnikowe, na które rankują, a my nie.
- **GSC (Search Analytics)** — dla `sklep.plasmet.pl`: frazy z impresjami bez kliknięć (pozycje 5–20) =
  gotowe tematy „content gap" z realnym popytem; sprawdzić, czy historia Mercatum jest dostępna.
- Po pobraniu: przeszeregować prio W/Ś/N wg realnego `volume × intencja × KD` i ewentualnie dorzucić 3–5
  fraz z najwyższym potencjałem do banku tematów.
