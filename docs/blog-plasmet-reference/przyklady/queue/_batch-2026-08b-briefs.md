# Briefy bloga - partia SIERPIEŃ/WRZESIEŃ 2026 (drip codzienny 07:00, 13.08-01.09, wpisy 72-91)

> **Autor:** seo-content-writer. **Odbiorca:** `blog-writer` (pisze prozę -> `humanizer` -> akcept `brand-voice-manager`),
> potem `seo-tech-lead` (schema FAQ/Article/HowTo), `graphic-designer` (hero wg `blog/images/_standard-grafiki-bloga.md`),
> `shoper-api` (publikacja przez webapi `news`, drip `blog-publish.ps1`, kafelki `product-cards.ps1`).
> **Źródło tematów:** `seo/gsc-analiza-2026-06.md` (REALNY popyt: chemia 37,6k wyśw., BHP 14,3k przy 4 klikach,
> wentylacja 6,6k, zamocowania 6,5k; Milwaukee-info bez popytu informacyjnego), sezonowość druga połowa sierpnia
> i wrzesień (uszczelnianie, hydroizolacja, wilgoć po lecie, start sezonu grzewczego, odzież na chłód, liście
> i zazimowanie sprzętu) oraz `seo/linkowanie-wewnetrzne/_dane-kategorie-luki.json` (nowe kategorie 131, 137,
> 259, 298-329 bez ruchu i bez linków wewnętrznych). Tematy 01-71 sprawdzone, zero powtórek.
> **Format docelowy:** każdy brief -> jeden plik JSON w `blog/queue/` wg `blog/queue/_format.md`.
>
> **Reguły partii (twarde):**
> - **Kategoria bloga:** dokładnie jedna z kanonicznych: „Porównania" (8) x6, „Krok po kroku" (6) x5,
>   „Problemy i porady" (7) x3, „Normy i BHP" (9) x3, „Poradnik" (5) x3. Struktura wpisu MUSI odpowiadać
>   kategorii (schematy jak w partii C).
> - **Kafelki produktowe (zasada twarda od 2026-08-03):** każdy wpis tej partii cokolwiek dobiera lub
>   rekomenduje, więc każdy ma zaplanowane placeholdery `[PRODUKT: ...]` / `[PRODUKTY: ...]` wg
>   `blog/queue/_format.md`. W briefach podane są **intencje kafelków** (jaki produkt, dlaczego, gdzie);
>   konkretne `id|SKU` domyka sesja główna przez `scripts/shoper-api/product-cards.ps1 -Rank "<fraza>"`
>   (sprzedaż, potem stan). Stan 0 i brak zdjęcia nie wchodzą.
> - **Nowe kategorie bez ruchu dostają linki.** Partia celowo kieruje linkowanie wewnętrzne do kategorii
>   131 (kurtki), 137 (koszulki), 259 (bluzy), 298 (uszczelniacze wysokotemperaturowe), 300 (pilarki
>   łańcuchowe), 301 (dmuchawy), 303 (kosiarki), 304 (detektory napięcia), 311 (wentylatory Milwaukee),
>   314 (przedłużacze bębnowe), 321 (kamizelki), 322 (czapki), 329 (buty robocze). Każda z nich ma
>   co najmniej jeden wpis, który do niej prowadzi.
> - Lead = samodzielna, cytowalna odpowiedź 40-60 słów (passage-citable pod AI Overviews) z frazą główną z przodu.
> - Tam gdzie „dobór / różnice / klasy / normy / objawy / temperatury" -> **tabela**, nie proza.
> - Każdy wpis kończy sekcją FAQ 4-5 pytań pod nagłówkiem **„Najczęściej zadawane pytania"** (dokładnie ta
>   fraza, parser schema `FAQPage` jej szuka).
> - Linkowanie: kategoria sklepu + 1-2 **opublikowane** wpisy; wewnątrz partii tylko „wstecz" po dacie.
> - Autoryzacje Milwaukee/Den Braven, marki Baum, Bostik, Awenta, Polifarb Kalisz i „od 1979 roku" naturalnie
>   (NIGDY „X-letni staż").
> - **ZERO długich myślników** w całej partii (tytuły, H2, meta, tabele, kafelki). Humanizer egzekwuje TOTAL BAN.
> - Hero: fotografia reportażowa „fachowiec przy pracy", paleta niebieska DS (#142A66 / #2E4A6B w cieniach),
>   czerwień tylko na korpusie narzędzia, bez logo i tekstu w grafice; `alt` per wpis.
> - Liczby techniczne (normy, temperatury, parametry) weryfikowane; wstępny stan wiedzy w sekcji „Źródła
>   weryfikacji faktów" na końcu, detale produktowe blog-writer domyka z kart produktów PLASMET.

## Uwagi operacyjne dla sesji głównej (przeczytaj przed zrzutem do kolejki)

1. **Numeracja plików: 72-91** (kolejność w pliku = numeracja = kolejność publikacji). Ostatni użyty numer to 71.
   Slug = bazowy `seo_url`.
2. **Kalendarz:** 20 wpisów, jeden dziennie, **2026-08-13 do 2026-09-01**. Bez kolizji: kolejka partii C
   kończy się 12.08 wpisem 71.
3. **Kategorie bloga istnieją na żywo** (Poradnik 5, Krok po kroku 6, Problemy i porady 7, Porównania 8,
   Normy i BHP 9). Nie tworzymy nowych, nie tworzymy wariantów pisowni.
4. **Schema:** wpisy 73, 77, 83, 86, 88 kwalifikują się pod **HowTo** (kroki + lista materiałów) obok
   `FAQPage`/`Article`; sygnał do `seo-tech-lead`.
5. **Kafelki:** przed przełączeniem wpisu na `gotowy` uruchomić `product-cards.ps1 -Rank` dla fraz podanych
   w polu „kafelki" i wstawić realne `id|SKU`. Wpisy 76, 77, 81, 82, 83, 86, 88, 91 celują w kategorie
   o małym asortymencie (1-25 pozycji), więc kafelek może wymagać sięgnięcia po produkt z kategorii
   nadrzędnej, jeśli w podkategorii nie ma stanu.
6. **Frazy:** MCP Ahrefs/DataForSEO niedostępne w kontekście subagenta, wolumeny to estymaty na bazie
   intencji, SERP i danych GSC z eksportu 2026-06-11. Lista zapytań do pobrania: sekcja „Do weryfikacji".
7. **Po zrzuceniu partii:** dopisać do `blog/kalendarz-tresci.md` klaster sezonowy H (jesień) i nowy wymiar
   „kategorie bez ruchu" w banku tematów; po 4 tygodniach sprawdzić w GSC wpisy 72-91 pod kątem fraz
   z pozycjami 5-20 (kandydaci na rozbudowę sekcji lub FAQ).
8. **Fact-check produktowy dla blog-writera:** wpisy 76 i 77 (uszczelniacze Baum, zakresy temperatur),
   79 (przedłużacze bębnowe: obciążalność zwinięty vs rozwinięty), 81 (odzież podgrzewana M12: strefy,
   poziomy grzania, czasy pracy), 82 (dmuchawy: m3/h i prędkość powietrza), 88 (detektory: kategoria
   pomiarowa), 91 (lampy: lumeny, IP) wymagają domknięcia danych z kart produktów.

---

## 1. „Hydroizolacja fundamentów i ścian piwnicy: dysperbit, masa KMB czy folia kubełkowa" (Porównania, klaster C)

- **Plik:** `72-hydroizolacja-fundamentow-dysperbit-kmb-folia.json` · **slug/seo_url:** `hydroizolacja-fundamentow-dysperbit-masa-kmb-folia-kubelkowa`
- **tytuł (H1):** Hydroizolacja fundamentów i ścian piwnicy: dysperbit, masa KMB czy folia kubełkowa
- **kategoria:** Porównania
- **klaster:** C (chemia budowlana) · **typ:** POR · **intencja:** komercyjna (remont odkopanego fundamentu, prosument + wykonawca)
- **planowana_data:** 2026-08-13
- **fraza główna:** hydroizolacja fundamentów
- **frazy poboczne:** dysperbit czy masa kmb, masa bitumiczna do fundamentów, izolacja przeciwwilgociowa ścian piwnicy, folia kubełkowa do czego, jak zabezpieczyć fundament przed wilgocią
- **struktura (schemat „Porównania": definicje, tabela porównawcza OBOWIĄZKOWA, kiedy X kiedy Y, werdykt, FAQ):**
  - *Lead 40-60 słów:* hydroizolacja fundamentów to warstwa chroniąca mur przed wilgocią z gruntu. Do izolacji lekkiej, przy gruncie przepuszczalnym i bez wody napierającej, wystarczy masa bitumiczna typu dysperbit. Przy większym obciążeniu wodą stosuje się grubowarstwową masę KMB, a folia kubełkowa to warstwa ochronna, nie izolacja sama w sobie.
  - H2: Trzy rodzaje obciążenia wodą (wilgoć gruntowa, woda niezalegająca, woda napierająca; od tego zależy cały dobór)
  - H2: **Tabela porównawcza** (dysperbit i masy rozpuszczalnikowe vs masy KMB grubowarstwowe vs powłoki mineralne sztywne i elastyczne vs folia kubełkowa: rola, obciążenie wodą, grubość warstwy, czas schnięcia, podłoże, kontakt ze styropianem, orientacyjne zużycie)
  - H2: Dysperbit i masy bitumiczne: kiedy wystarczą (izolacja pozioma i pionowa lekka, gruntowanie roztworem, 2-3 warstwy krzyżowo)
  - H2: Masa KMB: kiedy jest konieczna (woda napierająca, izolacja ciężka, warstwa pomiarowa i kontrola grubości, zbrojenie siatką w narożach)
  - H2: Folia kubełkowa: co naprawdę robi (ochrona mechaniczna izolacji i szczelina wentylacyjna, kubełkami do ściany, listwa zamykająca; sama folia nie zastąpi masy)
  - H2: Uwaga na styropian i rozpuszczalniki (masy rozpuszczalnikowe rozpuszczają XPS i EPS, do ocieplenia fundamentu tylko masy bezrozpuszczalnikowe lub wodne)
  - H2: Werdykt: co wybrać do typowej sytuacji (odkopany fundament domu jednorodzinnego, garaż, ściana piwnicy od wewnątrz, taras nad pomieszczeniem)
  - H2: Kolejność prac i częste błędy (izolacja na mokry mur, brak gruntowania, jedna gruba warstwa, zasypka gruzem, brak izolacji poziomej pod ścianą)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Czym różni się dysperbit od masy KMB? · Czy folia kubełkowa zastępuje hydroizolację? · Ile warstw dysperbitu na fundament? · Czy masę bitumiczną można kłaść na styropian? · Jak zaizolować ścianę piwnicy od wewnątrz?
- **kafelki produktowe:** inline przy sekcji o masach bitumicznych `[PRODUKT: <masa bitumiczna/dysperbit z oferty> | do izolacji lekkiej odkopanego fundamentu, nakładana wałkiem w dwóch warstwach | Izolacja lekka]`; inline przy sekcji o gruntowaniu `[PRODUKT: <roztwór asfaltowy gruntujący> | wiąże pył i poprawia przyczepność masy do muru | Grunt pod bitum]`; blok przed FAQ `[PRODUKTY: Zestaw do izolacji odkopanego fundamentu || <masa bitumiczna> | podstawowa warstwa izolacji || <folia kubełkowa lub listwa> | ochrona mechaniczna gotowej powłoki || <pędzel lub szczotka dekarska> | narzędzie do rozprowadzania masy]`. Rank: `-Rank "masa bitumiczna"`, `-Rank "dysperbit"`, `-Rank "folia kubełkowa"`.
- **linkowanie wewn.:** kategoria **Chemia budowlana** (id 64) -> hydroizolacje i masy bitumiczne; w bok: „Folia w płynie: hydroizolacja łazienki krok po kroku" (wpis 52, tu jako hydroizolacja wewnętrzna), „Grunt pod farbę, tynk i płytki" (wpis #38).
- **hero:** fachowiec nakłada szczotką dekarską czarną masę bitumiczną na odkopaną ścianę fundamentową, w wykopie widoczna folia kubełkowa oparta o ścianę, chłodne niebieskie światło poranka, bez logo.
  - `hero_image_alt`: „Fachowiec nakłada szczotką masę bitumiczną na odkopaną ścianę fundamentową, obok folia kubełkowa w wykopie"
- **uzasadnienie:** chemia to klaster nr 1 realnego popytu (37,6k wyśw. GSC), a hydroizolacja fundamentów to jego brakujące ogniwo: wpis 52 obsługuje wnętrze, tu wchodzimy w prace zewnętrzne, których pik przypada na koniec lata i wrzesień (sucho, przed deszczami). Tabela obciążeń wodą i porównanie mas to wzorcowy obiekt cytowalny, a koszyk jest wielopozycyjny (masa + grunt + folia + narzędzia).

---

## 2. „Przegląd dachu i rynien przed jesienią: co sprawdzić i czym uszczelnić" (Krok po kroku, klaster C/H, SEZON)

- **Plik:** `73-przeglad-dachu-i-rynien-przed-jesienia.json` · **slug/seo_url:** `przeglad-dachu-i-rynien-przed-jesienia-krok-po-kroku`
- **tytuł (H1):** Przegląd dachu i rynien przed jesienią: co sprawdzić i czym uszczelnić
- **kategoria:** Krok po kroku
- **klaster:** C (chemia budowlana) / H (sezonowy) · **typ:** HT · **intencja:** informacyjna sezonowa -> komercyjna
- **planowana_data:** 2026-08-14
- **fraza główna:** przegląd dachu przed zimą
- **frazy poboczne:** czyszczenie rynien, czym uszczelnić rynnę, przeciek przy kominie co robić, uszczelniacz dekarski do blachy, taśma naprawcza do rynien
- **struktura (schemat „Krok po kroku": narzędzia i materiały na starcie, ponumerowane kroki, częste błędy, FAQ):**
  - *Lead 40-60 słów:* przegląd dachu przed jesienią sprowadza się do czterech rzeczy: oczyszczenia rynien i wpustów z liści, sprawdzenia obróbek przy kominie i oknach dachowych, kontroli mocowań blachy lub dachówek oraz uszczelnienia miejsc, w których stara masa popękała. Prace warto zrobić w suchy dzień, zanim temperatury spadną poniżej zakresu z karty uszczelniacza.
  - H2: Narzędzia i materiały - **lista** (drabina i zabezpieczenie, rękawice, szczypce lub łopatka do rynien, szczotka, odtłuszczacz, uszczelniacz dekarski w kolorze dachu, taśma naprawcza bitumiczna, wkręty farmerskie z podkładką EPDM, pistolet do kartuszy)
  - H2: Bezpieczeństwo najpierw (kiedy w ogóle nie wchodzimy na dach, praca z ziemi i z drabiny, mokra blacha, asekuracja, samotna praca na wysokości)
  - H2: Krok 1: rynny i wpusty (usunięcie liści i mchu, przepłukanie, kontrola spadku, sitka na wpustach przed sezonem opadania liści)
  - H2: Krok 2: łączenia i szczelność rynien (rozszczelnione zatrzaski, pęknięte uszczelki, uszczelniacz dekarski na czystym i suchym profilu, taśma naprawcza jako rozwiązanie awaryjne)
  - H2: Krok 3: obróbki przy kominie, kominkach wentylacyjnych i oknach dachowych (najczęstsze źródło przecieku; stary silikon i masa do wymiany, nie do dokładania)
  - H2: Krok 4: mocowania i drobne dziury w blachotrapezie (wkręty z podkładką EPDM, dokręcenie bez zgniatania podkładki, punktowe uszczelnienie)
  - H2: Krok 5: sprawdzenie od środka (poddasze przy dniu słonecznym, zacieki na deskowaniu, folia wstępnego krycia)
  - H2: Częste błędy (uszczelnianie mokrej lub zapylonej blachy, silikon octowy na blachę ocynkowaną, masa dekarska zamiast wymiany obróbki, praca przy zbyt niskiej temperaturze, zaklejanie otworów wentylacyjnych połaci)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Kiedy zrobić przegląd dachu przed zimą? · Czym uszczelnić przeciekającą rynnę? · Jaki uszczelniacz do blachy dachowej? · Czy taśma naprawcza wystarczy na dłużej? · Jak często czyścić rynny?
- **kafelki produktowe:** inline przy kroku 2 `[PRODUKT: <uszczelniacz dekarski w kolorze antracyt> | trzyma na wilgotnym i chłodnym podłożu, dopasowany kolorem do blachy | Uszczelnienie rynny]`; inline przy kroku 4 `[PRODUKT: <wkręty farmerskie z podkładką EPDM> | wymiana zużytych mocowań bez uszkodzenia powłoki blachy | Mocowanie blachy]`; blok przed FAQ `[PRODUKTY: Na przegląd dachu przed jesienią || <uszczelniacz dekarski> | do łączeń i obróbek || <taśma naprawcza bitumiczna> | doraźna łata na pęknięcie || <rękawice robocze z chwytem> | praca na drabinie i przy ostrej blasze]`. Rank: `-Rank "uszczelniacz dekarski"`, `-Rank "taśma naprawcza"`, `-Rank "wkręty farmerskie"`.
- **linkowanie wewn.:** kategoria **Chemia budowlana** -> uszczelniacze dekarskie + **Akcesoria budowlane** -> taśmy; w bok: „Uszczelniacz dekarski: jak dobrać (antracyt RAL 7016 i inne)" (wpis #30), „Folie i taśmy budowlane" (wpis #34).
- **hero:** dekarz w rękawicach wyjmuje liście z rynny na drabinie przy krawędzi dachu z blachy, w tle chłodne niebieskie niebo końca lata, obok kartusza uszczelniacza na dachówce, bez logo.
  - `hero_image_alt`: „Fachowiec czyści rynnę z liści stojąc na drabinie przy krawędzi dachu, obok kartusza uszczelniacza dekarskiego"
- **uzasadnienie:** uszczelniacze dekarskie mają w GSC 2,3k i 0,84k wyświetleń (antracyt RAL 7016 i 7024), a wpis #30 obsługuje tylko dobór produktu. Sezonowa procedura przeglądu daje temu produktowi kontekst „kiedy i po co", trafia w pik zapytań przed jesiennymi opadami i buduje koszyk (uszczelniacz + taśma + wkręty + rękawice). Format HowTo kwalifikuje się pod schema.

---

## 3. „Preparat na pleśń, grzyb i glony: który wybrać do ściany, drewna i elewacji" (Porównania, klaster C)

- **Plik:** `74-preparat-na-plesn-grzyb-glony-ktory-wybrac.json` · **slug/seo_url:** `preparat-na-plesn-grzyb-glony-ktory-wybrac`
- **tytuł (H1):** Preparat na pleśń, grzyb i glony: który wybrać do ściany, drewna i elewacji
- **kategoria:** Porównania
- **klaster:** C (chemia budowlana) · **typ:** POR · **intencja:** problemowo-komercyjna (GSC: środki przeciw pleśni 10,8k wyśw., „savo przeciw pleśni" 3,2k, poz. 6)
- **planowana_data:** 2026-08-15
- **fraza główna:** preparat na pleśń
- **frazy poboczne:** środek na grzyba na ścianie, preparat na glony i mchy na elewacji, odgrzybiacz do drewna, czym umyć kostkę brukową z zielonego nalotu, savo przeciw pleśni zastosowanie
- **struktura (schemat „Porównania"):**
  - *Lead 40-60 słów:* preparaty przeciw pleśni dzielą się na trzy grupy. Do czarnej pleśni na ścianach i fugach służą środki na bazie podchlorynu lub czwartorzędowych soli amoniowych, do drewna preparaty grzybobójcze i owadobójcze wnikające w strukturę, a do glonów i mchów na elewacji i kostce preparaty algobójcze, często bez spłukiwania. Środki nie są zamienne.
  - H2: Pleśń, grzyb domowy, glony i mchy: cztery różne problemy (czym się różnią, jak wyglądają, gdzie występują, po lecie i przy pierwszej kondensacji jesienią)
  - H2: **Tabela porównawcza** (typ preparatu: chlorowy do pleśni, bezchlorowy do wnętrz i tkanin, impregnat grzybobójczy do drewna, preparat algobójczy do elewacji i kostki, farba lub grunt z dodatkiem biobójczym: podłoże, czas działania, spłukiwanie, bezpieczeństwo, czy można malować po zabiegu)
  - H2: Pleśń na ścianie i w fudze: co działa naprawdę (usunięcie zarodników mechanicznie, preparat, dopiero potem malowanie; sam preparat bez usunięcia przyczyny wilgoci to praca do powtórzenia)
  - H2: Drewno: więźba, altana, płot (odgrzybiacz vs impregnat dwufunkcyjny, kolejność: odgrzybianie, mycie, impregnacja)
  - H2: Elewacja, dach i kostka brukowa (zielony i czarny nalot, preparaty bez spłukiwania działające tygodniami, mycie ciśnieniowe: kiedy pomaga, kiedy szkodzi)
  - H2: Werdykt: dobór do sytuacji - **mini-tabela** (narożnik sypialni, fuga w kabinie prysznicowej, sufit w łazience, deska tarasowa, ściana północna elewacji, kostka przy garażu)
  - H2: Bezpieczeństwo pracy z biocydami (wentylacja, rękawice chemoodporne, okulary, półmaska przy rozpylaniu, nie mieszać preparatów chlorowych z innymi środkami)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Czym różni się preparat na pleśń od preparatu na glony? · Czy można malować ścianę zaraz po odgrzybianiu? · Czy preparat na pleśń zabija grzyb w murze? · Jak usunąć zielony nalot z kostki brukowej? · Czy potrzebne są rękawice do preparatów grzybobójczych?
- **kafelki produktowe:** inline przy sekcji o ścianach `[PRODUKT: <preparat do usuwania pleśni z oferty> | do czarnej pleśni na ścianie i fudze, działa bez szorowania | Pleśń we wnętrzu]`; inline przy sekcji o elewacji `[PRODUKT: <preparat algobójczy do elewacji i kostki> | usuwa zielony nalot z dużych powierzchni bez spłukiwania | Elewacja i kostka]`; blok przed FAQ `[PRODUKTY: Do odgrzybiania krok po kroku || <preparat na pleśń> | pierwszy etap, likwidacja zarodników || <grunt lub farba z dodatkiem biobójczym> | zabezpieczenie po wyschnięciu ściany || <rękawice chemoodporne> | ochrona rąk przy biocydach]`. Rank: `-Rank "pleśń"`, `-Rank "glony"`, `-Rank "grzybobójczy"`.
- **linkowanie wewn.:** kategoria **Chemia budowlana** -> środki czyszczące i grzybobójcze; w bok: „Jak usunąć pleśń ze ściany i fugi" (wpis #29, tam procedura, tu dobór środka), „Jaki impregnat do drewna na zewnątrz" (wpis #14), „Rękawice chemoodporne a norma EN 374" (wpis 64).
- **hero:** dłoń w rękawicy chemoodpornej rozpyla preparat na zaciemniony narożnik ściany z widocznym nalotem, obok szczotka i butla, chłodne niebieskie światło wnętrza, bez logo.
  - `hero_image_alt`: „Osoba w rękawicach rozpyla preparat grzybobójczy na narożnik ściany z czarnym nalotem pleśni"
- **uzasadnienie:** druga największa okazja w całym GSC (10,8k wyśw. na środkach przeciw pleśni, „savo" na poz. 6 bez treści wspierającej). Wpis #29 to procedura usuwania z jednej powierzchni, tu wchodzimy w dobór preparatu do czterech różnych problemów, więc kanibalizacji nie ma, a jest naturalne linkowanie w obie strony. Koniec lata to moment, gdy nalot po deszczach jest najbardziej widoczny, a przed sezonem kondensacji ludzie szukają rozwiązania.

---

## 4. „Chemia budowlana jesienią: w jakiej temperaturze można jeszcze malować, kleić i piankować" (Poradnik, klaster C/H, SEZON)

- **Plik:** `75-chemia-budowlana-jesienia-temperatura-stosowania.json` · **slug/seo_url:** `chemia-budowlana-jesienia-w-jakiej-temperaturze-malowac-kleic-piankowac`
- **tytuł (H1):** Chemia budowlana jesienią: w jakiej temperaturze można jeszcze malować, kleić i piankować
- **kategoria:** Poradnik
- **klaster:** C (chemia budowlana) / H (sezonowy) · **typ:** PZ/FAQ pod GEO · **intencja:** informacyjna sezonowa -> komercyjna
- **planowana_data:** 2026-08-16
- **fraza główna:** w jakiej temperaturze można malować na zewnątrz
- **frazy poboczne:** temperatura stosowania pianki montażowej, do ilu stopni można kleić klej montażowy, punkt rosy malowanie, pianka zimowa do -10, akryl w niskiej temperaturze
- **struktura (schemat „Poradnik": tabela zbiorcza, kryteria, dobór, FAQ):**
  - *Lead 40-60 słów:* większość chemii budowlanej pracuje od plus 5 stopni Celsjusza wzwyż, licząc temperaturę podłoża, a nie powietrza. Farby i akryle wymagają dodatkowo wilgotności poniżej ok. 80 procent oraz temperatury co najmniej 3 stopnie wyższej niż punkt rosy. Pianki zimowe schodzą do około minus 10 stopni, ale puszka musi być ciepła.
  - H2: Dlaczego liczy się temperatura podłoża i punkt rosy (chłodna ściana rano, rosa na blasze, wilgoć w porach; jak w praktyce oszacować punkt rosy)
  - H2: **Tabela zbiorcza: minimalne warunki stosowania** (pianka montażowa standardowa, pianka zimowa, silikon octowy i neutralny, akryl, klej montażowy rozpuszczalnikowy, klej MS i hybrydowy, farba akrylowa wodna, farba alkidowa do metalu, impregnat do drewna, masa bitumiczna, zaprawa i klej do płytek: minimalna temperatura, uwagi o wilgotności, co się dzieje po przekroczeniu w dół; wartości potwierdzić w kartach produktów)
  - H2: Co się psuje, gdy jest za zimno (pianka nie rośnie i kruszy się, akryl i farba wodna zamarzają przed wyschnięciem i tracą przyczepność, silikon wolniej wulkanizuje, klej dyspersyjny nie odparowuje, żywica kotwy wiąże wielokrotnie dłużej)
  - H2: Jak wydłużyć sezon o kilka tygodni (praca w oknie pogodowym południa, ogrzewanie puszek i kartuszy do temperatury pokojowej, osłony i namioty, podgrzewanie podłoża, wersje zimowe produktów)
  - H2: Kolejność prac na wrzesień i październik - **lista** (najpierw prace zewnętrzne wrażliwe na wilgoć: malowanie i impregnacja, potem uszczelnianie i pianki, na końcu prace wewnętrzne)
  - H2: Czego nie da się przełożyć na wiosnę bez konsekwencji (nieuszczelniony przeciek, niezaimpregnowane drewno, odkryta izolacja fundamentu)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Do ilu stopni można malować na zewnątrz? · Czy można używać pianki montażowej przy 0 stopni? · Co to jest punkt rosy przy malowaniu? · Czy akryl wytrzyma przymrozek przed wyschnięciem? · Jak przechowywać chemię budowlaną jesienią?
- **kafelki produktowe:** inline przy sekcji o piankach `[PRODUKT: <pianka montażowa zimowa Den Braven> | pracuje przy ujemnej temperaturze otoczenia, gdy standardowa już nie wiąże | Praca w chłodzie]`; inline przy sekcji o malowaniu `[PRODUKT: <farba do metalu 3w1> | tolerancyjna na chłodne, wilgotne podłoże w granicach z karty | Ostatnie malowanie sezonu]`; blok przed FAQ `[PRODUKTY: Chemia, która nie odpada we wrześniu || <pianka zimowa> | uszczelnianie stolarki przy niskich temperaturach || <uszczelniacz neutralny> | styk stolarki i muru na zewnątrz || <impregnat do drewna> | ostatnie okno pogodowe na ochronę desek]`. Rank: `-Rank "pianka zimowa"`, `-Rank "impregnat"`, `-Rank "silikon neutralny"`.
- **linkowanie wewn.:** kategoria **Chemia budowlana** (hub kategorii, wpis linkuje szeroko: pianki, uszczelniacze, farby, impregnaty); w bok: „Pianka montażowa nie wiąże albo się kruszy" (wpis 54), „Jak pomalować bramę i ogrodzenie z metalu" (wpis 59), „Jaki impregnat do drewna na zewnątrz" (wpis #14).
- **hero:** monter ogrzewa dłońmi puszkę pianki przy oknie w chłodny poranek, na parapecie termometr i kartusze, para oddechu w powietrzu, chłodne niebieskie światło, bez logo.
  - `hero_image_alt`: „Monter ogrzewa puszkę pianki montażowej w chłodny poranek przed uszczelnieniem okna, obok termometr na parapecie"
- **uzasadnienie:** jedna tabela odpowiada na kilkanaście osobnych zapytań „do ilu stopni można...", co czyni z wpisu wzorcowy obiekt pod AI Overviews i naturalny hub kategorii chemii przed sezonem. Fraza sezonowa rośnie od września, a publikacja w połowie sierpnia daje czas na indeksację. Wpis podpiera całą partię jesienną i jest naturalnym celem linkowania z 73, 76, 77 i 90.

---

## 5. „Silikon wysokotemperaturowy czy uszczelniacz kominkowy: 300 czy 1500 stopni" (Porównania, klaster C, SEZON)

- **Plik:** `76-silikon-wysokotemperaturowy-czy-uszczelniacz-kominkowy.json` · **slug/seo_url:** `silikon-wysokotemperaturowy-czy-uszczelniacz-kominkowy-300-czy-1500-stopni`
- **tytuł (H1):** Silikon wysokotemperaturowy czy uszczelniacz kominkowy: 300 czy 1500 stopni
- **kategoria:** Porównania
- **klaster:** C (chemia budowlana / Baum) · **typ:** POR · **intencja:** komercyjna (start sezonu grzewczego; nowa kategoria 298 bez ruchu)
- **planowana_data:** 2026-08-17
- **fraza główna:** silikon wysokotemperaturowy
- **frazy poboczne:** uszczelniacz kominkowy 1500, silikon do 300 stopni do czego, czym uszczelnić drzwiczki kominka, kit kominkowy do szamotu, uszczelniacz do rur spalinowych
- **struktura (schemat „Porównania"):**
  - *Lead 40-60 słów:* silikon wysokotemperaturowy wytrzymuje ok. 300 stopni Celsjusza i służy do uszczelnień w pobliżu ciepła: kołnierzy, uszczelek metalowych, elementów kotłów i piekarników. Uszczelniacz kominkowy to masa odporna do ok. 1500 stopni, przeznaczona do bezpośredniego kontaktu z ogniem: fug szamotowych, drzwiczek i szczelin wkładu kominkowego.
  - H2: Dwa różne materiały, nie dwa warianty tego samego (silikon sylikonowy elastyczny vs masa mineralna twardniejąca; elastyczność kontra odporność na płomień)
  - H2: **Tabela porównawcza** (silikon wysokotemperaturowy czerwony i czarny vs uszczelniacz kominkowy do 1500 stopni vs sznur ceramiczny z klejem: odporność temperaturowa, kontakt z płomieniem, elastyczność po utwardzeniu, podłoża, typowe zastosowania, sposób aplikacji, kolor; parametry z kart produktów Baum)
  - H2: Silikon do 300 stopni: gdzie ma sens (kołnierze i przewody, uszczelki drzwiczek metalowych, elementy w strefie ciepła, motoryzacja i piekarniki, uszczelnienia wokół rur spalinowych poza strefą płomienia)
  - H2: Uszczelniacz kominkowy do 1500 stopni: gdzie jest jedyną opcją (fugi szamotowe, pęknięcia w komorze paleniskowej, osadzenie drzwiczek, styk wkładu z obudową, kominy i piece kaflowe)
  - H2: Sznur ceramiczny i klej do sznura (uszczelka drzwiczek i szyby: kiedy wymiana sznura zamiast masy; jak dobrać średnicę)
  - H2: Werdykt: dobór do zadania - **mini-tabela** (drzwiczki wkładu, szyba kominka, pęknięta fuga szamotu, rura spalinowa kotła, uszczelka piekarnika, komin systemowy)
  - H2: Aplikacja i błędy (czyszczenie i odpylenie, wygrzewanie po aplikacji wg karty, silikon w komorze paleniskowej jako klasyczny błąd, przekraczanie zakresu temperatury, nakładanie na gorące elementy)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Czym różni się silikon wysokotemperaturowy od uszczelniacza kominkowego? · Czym uszczelnić drzwiczki kominka? · Czy silikon 300 stopni wytrzyma w komorze paleniskowej? · Czym wypełnić pęknięcie w szamocie? · Czy uszczelniacz kominkowy trzeba wygrzać po nałożeniu?
- **kafelki produktowe:** inline przy sekcji o 1500 stopniach `[PRODUKT: 298:<uszczelniacz kominkowy Baum do 1500 stopni, 280 ml> | masa do bezpośredniego kontaktu z ogniem, do fug szamotowych i drzwiczek | Do 1500 stopni]`; inline przy sekcji o 300 stopniach `[PRODUKT: 298:<silikon wysokotemperaturowy Baum czerwony 300 stopni, 280 ml> | elastyczne uszczelnienie w strefie ciepła, poza kontaktem z płomieniem | Do 300 stopni]`; blok przed FAQ `[PRODUKTY: Przed sezonem grzewczym || <uszczelniacz kominkowy 1500 stopni> | naprawa fug i osadzenie drzwiczek || <silikon wysokotemperaturowy 300 stopni> | uszczelnienia wokół kotła i rur || <sznur ceramiczny lub klej do sznura> | wymiana uszczelki drzwiczek]`. Rank: `-Rank "wysokotemperaturowy"`, `-Rank "kominkowy"`.
- **linkowanie wewn.:** kategoria **Chemia budowlana -> uszczelniacze wysokotemperaturowe (id 298)** jako główny cel; w bok: „Silikon, akryl czy uszczelniacz MS: czym się różnią" (wpis #22), „Jaki silikon do łazienki" (wpis #3).
- **hero:** dłoń w rękawicy nakłada szpachelką ciemną masę uszczelniającą na fugę szamotu w otwartej komorze wkładu kominkowego, obok kartusza, chłodne niebieskie światło pomieszczenia kontrastujące z ciemnym wnętrzem paleniska, bez logo.
  - `hero_image_alt`: „Dłoń w rękawicy nakłada uszczelniacz kominkowy na fugę szamotową w komorze wkładu kominkowego"
- **uzasadnienie:** kategoria 298 jest nowa, ma 3 produkty i zero linków wewnętrznych, a popyt na uszczelnianie kominka rusza z końcem sierpnia i kulminuje we wrześniu i październiku. Rozróżnienie 300 kontra 1500 stopni to konkretne, cytowalne wyjaśnienie, którego brakuje w sieci, a błąd w doborze kończy się wypaleniem masy w pierwszym paleniu. Wpis buduje też zaplecze linkowe dla HowTo 77.

---

## 6. „Przegląd kominka przed sezonem grzewczym krok po kroku" (Krok po kroku, klaster C/H, SEZON)

- **Plik:** `77-przeglad-kominka-przed-sezonem-grzewczym.json` · **slug/seo_url:** `przeglad-kominka-przed-sezonem-grzewczym-krok-po-kroku`
- **tytuł (H1):** Przegląd kominka przed sezonem grzewczym krok po kroku
- **kategoria:** Krok po kroku
- **klaster:** C (chemia budowlana) / H (sezonowy) · **typ:** HT · **intencja:** informacyjna sezonowa -> komercyjna
- **planowana_data:** 2026-08-18
- **fraza główna:** przegląd kominka przed sezonem
- **frazy poboczne:** wymiana sznura w drzwiczkach kominka, czyszczenie szyby kominka, jak sprawdzić szczelność kominka, kiedy przegląd kominiarski, uszczelnienie wkładu kominkowego
- **struktura (schemat „Krok po kroku"):**
  - *Lead 40-60 słów:* przegląd kominka przed sezonem obejmuje pięć czynności: wyczyszczenie paleniska i szyby, kontrolę sznura uszczelniającego w drzwiczkach i szybie, sprawdzenie szamotu i deflektora, przegląd kanału dymowego przez kominiarza oraz uzupełnienie ubytków masą kominkową. Test kartki w domkniętych drzwiczkach pokazuje, czy uszczelka jeszcze pracuje.
  - H2: Narzędzia i materiały - **lista** (szczotka i odkurzacz do popiołu, preparat do szyb kominkowych, sznur ceramiczny o właściwej średnicy, klej do sznura, uszczelniacz kominkowy, szpachelka, rękawice odporne na wysoką temperaturę, latarka)
  - H2: Kiedy zrobić przegląd (koniec lata i wrzesień: zimne palenisko, dostępny kominiarz, czas na dosuszenie masy przed pierwszym paleniem)
  - H2: Krok 1: czyszczenie paleniska i szyby (popiół, sadza, preparat do szkła kominkowego, kontrola stanu uszczelki szyby)
  - H2: Krok 2: test szczelności drzwiczek (kartka papieru przytrzaśnięta w kilku miejscach obwodu; luźna kartka oznacza sznur do wymiany)
  - H2: Krok 3: wymiana sznura uszczelniającego (usunięcie starego, oczyszczenie rowka, dobór średnicy, klej do sznura, docisk i wstępne wygrzanie)
  - H2: Krok 4: szamot, deflektor i fugi (pęknięcia włosowate a pęknięcia przelotowe, uzupełnianie masą kominkową, kiedy płyta szamotowa idzie do wymiany)
  - H2: Krok 5: kanał dymowy i przegląd kominiarski (obowiązek okresowej kontroli i czyszczenia, sadza szklista, czujnik czadu jako element wyposażenia domu)
  - H2: Pierwsze palenie po naprawie (stopniowe wygrzewanie, zapach z nowej masy, wentylacja pomieszczenia)
  - H2: Częste błędy (silikon budowlany zamiast masy kominkowej, sznur o za małej średnicy, zaklejanie kratek dolotu powietrza, palenie mokrym drewnem, pominięcie przeglądu kominiarskiego)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Jak sprawdzić, czy drzwiczki kominka są szczelne? · Jak często wymieniać sznur w kominku? · Czym uzupełnić pęknięty szamot? · Kiedy trzeba wykonać przegląd kominiarski? · Dlaczego szyba kominka szybko czernieje?
- **kafelki produktowe:** inline przy kroku 3 `[PRODUKT: <sznur ceramiczny lub klej do sznura z oferty> | wymiana uszczelki drzwiczek bez demontażu wkładu | Uszczelka drzwiczek]`; inline przy kroku 4 `[PRODUKT: 298:<uszczelniacz kominkowy do 1500 stopni> | uzupełnia fugi i pęknięcia w komorze paleniskowej | Naprawa szamotu]`; blok przed FAQ `[PRODUKTY: Zestaw na przegląd kominka || <uszczelniacz kominkowy> | naprawa fug i osadzeń || <preparat do szyb kominkowych> | usunięcie sadzy bez rysowania szkła || <rękawice robocze> | praca przy sadzy i ostrych krawędziach szamotu]`. Rank: `-Rank "kominkowy"`, `-Rank "sznur ceramiczny"`, `-Rank "do szyb"`.
- **linkowanie wewn.:** kategoria **Chemia budowlana -> uszczelniacze wysokotemperaturowe (id 298)**; w bok: „Silikon wysokotemperaturowy czy uszczelniacz kominkowy" (wpis 76, publikacja 17.08, link bezpieczny), „Chemia budowlana jesienią: temperatury" (wpis 75, publikacja 16.08).
- **hero:** fachowiec kucający przy otwartym wkładzie kominkowym wkleja nowy sznur ceramiczny w rowek drzwiczek, obok szpachelka i kartusza masy, chłodne niebieskie światło salonu, bez logo.
  - `hero_image_alt`: „Fachowiec wkleja nowy sznur uszczelniający w drzwiczki wkładu kominkowego podczas przeglądu przed sezonem"
- **uzasadnienie:** HowTo domykające parę z wpisem 76 („który materiał" i „jak zrobić"), wprost przed pikiem sezonu grzewczego. Prowadzi ruch do nowej kategorii 298 i buduje koszyk (masa + sznur + preparat do szyb + rękawice). Element bezpieczeństwa (przegląd kominiarski, czujnik czadu) to naturalny sygnał E-E-A-T i element, którego brakuje w poradnikach konkurencji.

---

## 7. „Obuwie ochronne po zmianie normy: co znaczy S1PS, S3S i S7L (EN ISO 20345:2022)" (Normy i BHP, klaster G)

- **Plik:** `78-obuwie-ochronne-s1ps-s3s-s7l-norma-2022.json` · **slug/seo_url:** `obuwie-ochronne-s1ps-s3s-s7l-norma-en-iso-20345-2022`
- **tytuł (H1):** Obuwie ochronne po zmianie normy: co znaczy S1PS, S3S i S7L
- **kategoria:** Normy i BHP
- **klaster:** G (BHP) · **typ:** FAQ/GEO (compliance) · **intencja:** informacyjna normatywna -> komercyjna (zaopatrzenie firm, sezon jesienny)
- **planowana_data:** 2026-08-19
- **fraza główna:** oznaczenia obuwia ochronnego
- **frazy poboczne:** s1ps co to znaczy, s3s buty robocze, en iso 20345 2022 zmiany, s7l obuwie, wkładka antyprzebiciowa niemetalowa
- **struktura (schemat „Normy i BHP": cytowalne definicje, tabele klas, dobór, FAQ):**
  - *Lead 40-60 słów:* nowa edycja normy EN ISO 20345 z 2022 roku zmieniła oznaczenia obuwia ochronnego. Litera P nadal oznacza wkładkę antyprzebiciową metalową, a nowe kody PL i PS opisują wkładki niemetalowe badane odpowiednio gwoździem 4,5 mm i 3 mm. Doszły też klasy wodoszczelne oraz oznaczenia SC i LG.
  - H2: Co zostało bez zmian (podnosek chroniący palce z energią 200 J to warunek konieczny każdego obuwia typu S; obuwie zawodowe bez podnoska to inna norma)
  - H2: **Tabela klas** (SB, S1, S1P, S1PL, S1PS, S2, S3, S3L, S3S, S6, S7, S7L, S7S: podnosek, zamknięta pięta, antystatyka, absorpcja energii, wodoodporność cholewki, wodoszczelność całego buta, odporność na przebicie, bieżnik; wersje z 2022 potwierdzić przy pisaniu)
  - H2: Wkładka antyprzebiciowa: metal czy tkanina - **tabela** (metalowa P: pełna ochrona powierzchni, zimniejsza, sztywniejsza, reaguje na detektory; niemetalowa PL i PS: lżejsza, cieplejsza, elastyczna, PS badana cieńszym gwoździem, czyli chroni także przed drobniejszymi przebiciami)
  - H2: Nowe i przydatne oznaczenia dodatkowe (SC ochrona noska przed ścieraniem, LG podeszwa z chwytem drabinowym, HRO odporność na kontakt z gorącym podłożem, CI i HI izolacja od zimna i ciepła, WR wodoszczelność, SR poślizg)
  - H2: Co to zmienia przy zakupie na jesień (S3 i S7 do pracy w błocie i deszczu, CI przy pracy na zimnym podłożu, LG dla dekarzy i instalatorów, bieżnik i odprowadzanie wody)
  - H2: Dobór do stanowiska - **mini-tabela** (budowa i wykop, hala i magazyn, instalacje i praca na drabinie, prace dekarskie, warsztat samochodowy, praca zimą na zewnątrz)
  - H2: Obowiązki pracodawcy i żywotność obuwia (obuwie ochronne jako ŚOI kategorii II, wymiana po utracie właściwości, kontrola podeszwy i podnoska po urazie)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Co oznacza S1PS w butach roboczych? · Czym różni się S3 od S3S? · Czy wkładka niemetalowa chroni tak samo jak metalowa? · Jakie buty robocze na jesień i zimę? · Czy pracodawca musi zapewnić obuwie ochronne?
- **kafelki produktowe:** inline przy tabeli klas `[PRODUKT: 329:<półbuty ochronne Milwaukee S1PS FLEXTRED> | lekka klasa z niemetalową wkładką antyprzebiciową do prac w hali i na instalacjach | Klasa S1PS]`; inline przy sekcji o jesieni `[PRODUKT: 329:<półbuty ochronne Milwaukee skóra S3S FLEXTRED> | skórzana cholewka i ochrona przed wodą oraz przebiciem na budowę | Klasa S3S]`; blok przed FAQ `[PRODUKTY: Obuwie i ochrona na jesienne prace || <but klasy S3 lub S7> | praca w błocie i deszczu || <skarpety lub wkładki robocze> | komfort przy całodziennej pracy || <rękawice robocze> | komplet ŚOI na stanowisko]`. Rank: `-Rank "S3"`, `-Rank "obuwie ochronne"`, `-Rank "półbuty"`.
- **linkowanie wewn.:** kategoria **BHP -> obuwie robocze (id 329)** jako główny cel; w bok: „Obuwie robocze S1, S2, S3: co oznaczają klasy i jak wybrać" (wpis #41, tam podstawy, tu zmiana normy), „Środki ochrony indywidualnej: kategorie I, II i III" (wpis 57).
- **hero:** zbliżenie na buty robocze pracownika stojącego na mokrej, błotnistej desce rusztowania, widoczny bieżnik i szycie cholewki, chłodne niebieskie światło jesiennego poranka, bez logo.
  - `hero_image_alt`: „Buty robocze z wyraźnym bieżnikiem na mokrej desce rusztowania podczas jesiennych prac budowlanych"
- **uzasadnienie:** BHP to największa luka GSC (14,3k wyświetleń przy 4 klikach), a kategoria 329 jest nowa i nie ma linków wewnętrznych. Zmiana normy z 2022 roku wciąż jest słabo opisana po polsku, a klienci widzą na metkach kody S1PS i S3S, których nie rozumieją. Tabela klas to wzorcowy obiekt cytowalny w AI, a intencja jest B2B (zamówienia obuwia dla ekipy przed jesienią).

---

## 8. „Przedłużacz bębnowy na budowę: przekrój żyły, IP44 i dlaczego trzeba rozwinąć bęben" (Problemy i porady, klaster B/H)

- **Plik:** `79-przedluzacz-bebnowy-przekroj-ip44-rozwijanie.json` · **slug/seo_url:** `przedluzacz-bebnowy-na-budowe-przekroj-ip44-rozwijanie-bebna`
- **tytuł (H1):** Przedłużacz bębnowy na budowę: przekrój żyły, IP44 i dlaczego trzeba rozwinąć bęben
- **kategoria:** Problemy i porady
- **klaster:** B (elektronarzędzia) / H (sezonowy) · **typ:** FAQ/troubleshooting · **intencja:** komercyjno-informacyjna (nowa kategoria 314 bez ruchu)
- **planowana_data:** 2026-08-20
- **fraza główna:** jaki przedłużacz bębnowy
- **frazy poboczne:** przedłużacz bębnowy 3x2 5 czy 3x1 5, przedłużacz się nagrzewa, ip44 co oznacza, przedłużacz do nagrzewnicy, spadek napięcia na długim przedłużaczu
- **struktura (schemat „Problemy i porady": objaw, przyczyny w tabeli, naprawa, zapobieganie, FAQ):**
  - *Lead 40-60 słów:* przedłużacz bębnowy dobiera się do mocy odbiornika i długości przewodu. Do narzędzi o dużym poborze i przewodów powyżej 25 metrów potrzeba żyły 2,5 mm kwadratowego, a na budowie i na zewnątrz gniazd w klasie IP44. Zwinięty bęben pod obciążeniem grzeje się jak grzałka, dlatego przy dużej mocy rozwija się go w całości.
  - H2: Objawy problemu - **tabela objaw, przyczyna, rozwiązanie** (bęben gorący w dotyku, zapach izolacji, narzędzie ma mniej mocy albo nie startuje, wyłącznik nadprądowy wybija, wtyczka topi się przy styku, zabezpieczenie termiczne bębna odcina zasilanie)
  - H2: Dlaczego zwinięty bęben się przegrzewa (ciasno nawinięty przewód nie oddaje ciepła, dodatkowo działa jak cewka; producenci podają dwie obciążalności, dla bębna zwiniętego i rozwiniętego, a różnica bywa kilkukrotna)
  - H2: Przekrój żyły a długość i moc - **tabela** (3x1,5 mm2 i 3x2,5 mm2 przy 25, 40 i 50 metrach: do jakich odbiorników, orientacyjny spadek napięcia, typowe zastosowanie; obciążalności potwierdzić z kart produktów)
  - H2: Co oznacza IP44 i kiedy jest konieczne (ochrona przed bryzgami wody i ciałami stałymi powyżej 1 mm, praca na zewnątrz, w deszczu i na wilgotnej posadzce, klapki gniazd, przewód w wykonaniu gumowym)
  - H2: Bezpieczniki, wyłączniki i praca na budowie (zabezpieczenie termiczne w bębnie, wyłącznik różnicowoprądowy w rozdzielnicy budowlanej, przewód poza traktem komunikacyjnym, żadnych gniazd w kałuży)
  - H2: Dobór do typowych odbiorników - **mini-tabela** (wiertarka i szlifierka, młot wyburzeniowy, mieszarka do zapraw, kompresor, nagrzewnica elektryczna, oświetlenie i ładowarki)
  - H2: Jak zapobiegać (rozwijanie przy dużej mocy, brak kaskady przedłużaczy, przegląd izolacji przed sezonem, przechowywanie bez zagięć, suszenie po pracy w deszczu)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Dlaczego trzeba rozwinąć przedłużacz bębnowy? · Jaki przekrój przedłużacza do 50 metrów? · Co oznacza IP44 na przedłużaczu? · Czy można łączyć dwa przedłużacze? · Jaki przedłużacz do nagrzewnicy elektrycznej?
- **kafelki produktowe:** inline przy tabeli przekrojów `[PRODUKT: 314:<przedłużacz bębnowy 25 m, 3x2,5 mm2, IP44> | zapas mocy dla narzędzi o dużym poborze przy typowej długości na budowie | Do mocnych narzędzi]`; inline przy sekcji o IP44 `[PRODUKT: 314:<przedłużacz bębnowy 50 m, 3x1,5 mm2, IP44> | zasięg na całą działkę do oświetlenia i lżejszych narzędzi | Duży zasięg]`; blok przed FAQ `[PRODUKTY: Zasilanie na jesienne prace || <przedłużacz bębnowy IP44> | podstawa zasilania na budowie i w garażu || <lampa lub naświetlacz warsztatowy> | krótsze dni i praca po zmroku || <rozgałęźnik budowlany> | rozdział zasilania bez kaskady przedłużaczy]`. Rank: `-Rank "przedłużacz bębnowy"`, `-Rank "naświetlacz"`.
- **linkowanie wewn.:** kategoria **Elektronarzędzia i akcesoria -> przedłużacze bębnowe (id 314)** jako główny cel; w bok: „Zestaw narzędzi do domu i warsztatu" (wpis #49), „Oznaczenia akumulatorów narzędzi: co znaczy Ah, V i Li-Ion" (wpis #33 jako most do zasilania akumulatorowego).
- **hero:** elektryk rozwija do końca przewód z bębna przedłużacza na placu budowy przed podłączeniem mieszarki, w tle rozdzielnica budowlana, chłodne niebieskie światło, czerwony akcent obudowy bębna, bez logo.
  - `hero_image_alt`: „Pracownik rozwija przewód z bębna przedłużacza budowlanego przed podłączeniem narzędzia o dużej mocy"
- **uzasadnienie:** kategoria 314 jest nowa (5 pozycji) i nie ma linków wewnętrznych, a „dlaczego przedłużacz się grzeje" to klasyczne zapytanie problemowe bez konkurencji treściowej w naszym profilu. Jesienią rośnie zapotrzebowanie na zasilanie w garażu i na budowie (nagrzewnice, oświetlenie), więc wpis wchodzi tuż przed sezonem. Tabela przekrój, długość, moc ma realną wartość dla wykonawcy i jest cytowalna.

---

## 9. „Odzież robocza na deszcz i chłód: normy EN 343, EN 342 i EN 14058" (Normy i BHP, klaster G, SEZON)

- **Plik:** `80-odziez-robocza-na-deszcz-i-chlod-en-343-en-342.json` · **slug/seo_url:** `odziez-robocza-na-deszcz-i-chlod-normy-en-343-en-342-en-14058`
- **tytuł (H1):** Odzież robocza na deszcz i chłód: normy EN 343, EN 342 i EN 14058
- **kategoria:** Normy i BHP
- **klaster:** G (BHP) · **typ:** FAQ/GEO (compliance) · **intencja:** informacyjna normatywna -> komercyjna (zaopatrzenie firm przed jesienią)
- **planowana_data:** 2026-08-21
- **fraza główna:** odzież robocza przeciwdeszczowa norma
- **frazy poboczne:** en 343 klasy, kurtka robocza wodoodporna czy wodoszczelna, en 342 odzież chroniąca przed zimnem, ret oddychalność kurtki, odzież robocza na jesień dla pracowników
- **struktura (schemat „Normy i BHP"):**
  - *Lead 40-60 słów:* odzież chroniącą przed deszczem i chłodem opisują trzy normy. EN 343 dotyczy ochrony przed deszczem i podaje klasę wodoszczelności oraz oddychalności, EN 342 obejmuje zestawy chroniące przed zimnem poniżej minus 5 stopni, a EN 14058 pojedyncze elementy odzieży do środowiska chłodnego, ale nie mroźnego.
  - H2: Wodoodporna, wodoszczelna, oddychająca: trzy różne obietnice (impregnat na powierzchni, membrana i klejone szwy, przepuszczalność pary wodnej)
  - H2: EN 343 - **tabela klas** (klasy 1 do 4 dla wodoszczelności i dla oporu pary wodnej Ret; co która klasa oznacza w praktyce: krótka praca w mżawce kontra cały dzień w deszczu; oznaczenie X przy teście deszczem)
  - H2: EN 342 i EN 14058: ochrona przed zimnem (EN 342 dla zestawów i temperatur poniżej minus 5 stopni, izolacyjność cieplna i przepuszczalność powietrza; EN 14058 dla pojedynczych kurtek i bluz do prac w chłodzie)
  - H2: Piktogramy na metce: jak je czytać (kropla i liczby, płatek śniegu, oznaczenia łączone z EN ISO 20471 dla odzieży ostrzegawczej)
  - H2: Warstwowe ubranie do pracy: zasada trzech warstw - **tabela** (warstwa bazowa odprowadzająca wilgoć, warstwa izolacyjna, warstwa zewnętrzna wiatroszczelna i wodoszczelna; co dobrać przy pracy statycznej, a co przy pracy w ruchu)
  - H2: Widoczność jesienią (skrócony dzień, deszcz i mgła, klasy odzieży ostrzegawczej przy pracy przy drodze)
  - H2: Obowiązki pracodawcy przy pracy na zewnątrz (odzież ochronna jako ŚOI, pomieszczenie do ogrzania się i przebrania, ciepłe napoje przy pracy w niskiej temperaturze; brzmienie przepisów potwierdzić przy pisaniu)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Co oznacza EN 343 klasa 3? · Czym różni się kurtka wodoodporna od wodoszczelnej? · Jaka norma dotyczy odzieży chroniącej przed zimnem? · Jak ubrać się warstwowo do pracy na zewnątrz? · Czy pracodawca musi zapewnić odzież przeciwdeszczową?
- **kafelki produktowe:** inline przy sekcji o warstwie zewnętrznej `[PRODUKT: 131:<kurtka robocza wodoodporna z oferty> | warstwa zewnętrzna na deszcz i wiatr przy pracy na zewnątrz | Warstwa zewnętrzna]`; inline przy sekcji o warstwie bazowej `[PRODUKT: 137:<koszulka robocza z długim rękawem> | baza pod bluzę, odprowadza wilgoć przy pracy w ruchu | Warstwa bazowa]`; blok przed FAQ `[PRODUKTY: Komplet na jesienne prace na zewnątrz || <kurtka robocza> | ochrona przed deszczem i wiatrem || <bluza robocza> | warstwa izolacyjna pod kurtkę || <czapka robocza> | ciepło tam, gdzie traci się go najwięcej]`. Rank: `-Rank "kurtka"`, `-Rank "bluza"`, `-Rank "czapka"`. Kategorie: 131 kurtki, 137 koszulki, 259 bluzy, 322 czapki.
- **linkowanie wewn.:** kategoria **BHP -> odzież robocza: kurtki (131), bluzy (259), koszulki (137), czapki (322)**; w bok: „Odzież robocza ostrzegawcza: klasy 1, 2, 3 wg normy EN ISO 20471" (wpis #50), „Środki ochrony indywidualnej: kategorie I, II i III" (wpis 57).
- **hero:** pracownik w kurtce roboczej z kapturem sprawdza plan na placu w drobnym deszczu, krople na tkaninie, chłodne niebieskie światło jesiennego popołudnia, bez logo i napisów na odzieży.
  - `hero_image_alt`: „Pracownik w wodoodpornej kurtce roboczej z kapturem podczas pracy na zewnątrz w deszczu"
- **uzasadnienie:** normy odzieżowe to naturalne przedłużenie klastra BHP (16, 20, 32, 40, 41, 50, 57, 64, 68) o wymiar sezonowy, a kategorie 131, 137, 259 i 322 są nowe i nie mają linków wewnętrznych. Zapytania o odzież roboczą na jesień rosną od końca sierpnia (zamówienia firmowe na sezon), tabela klas EN 343 jest gotowym obiektem cytowalnym, a wpis przygotowuje grunt pod porównanie odzieży podgrzewanej (81).

---

## 10. „Odzież podgrzewana Milwaukee M12: kurtka, bluza czy kamizelka" (Porównania, klaster G/A, SEZON)

- **Plik:** `81-odziez-podgrzewana-milwaukee-m12-kurtka-bluza-kamizelka.json` · **slug/seo_url:** `odziez-podgrzewana-milwaukee-m12-kurtka-bluza-czy-kamizelka`
- **tytuł (H1):** Odzież podgrzewana Milwaukee M12: kurtka, bluza czy kamizelka
- **kategoria:** Porównania
- **klaster:** G (BHP) / A (Milwaukee) · **typ:** POR · **intencja:** komercyjna (wysoka wartość koszyka, autoryzowany dystrybutor)
- **planowana_data:** 2026-08-22
- **fraza główna:** odzież podgrzewana milwaukee
- **frazy poboczne:** kurtka podgrzewana m12, bluza podgrzewana milwaukee, kamizelka podgrzewana akumulatorowa, jak działa odzież podgrzewana, ile działa kurtka podgrzewana na akumulatorze
- **struktura (schemat „Porównania"):**
  - *Lead 40-60 słów:* odzież podgrzewana Milwaukee M12 grzeje strefami zasilanymi z akumulatora 12 V, który wpina się w kieszeń przez adapter zasilania. Kamizelka daje ciepło korpusu przy pełnej swobodzie ramion, bluza sprawdza się jako warstwa środkowa, a kurtka łączy grzanie z ochroną przed wiatrem i opadem.
  - H2: Jak działa odzież podgrzewana (strefy grzewcze na klatce, plecach i w kieszeniach, poziomy grzania, akumulator M12 jako źródło zasilania i powerbank, czas pracy zależny od pojemności i poziomu grzania; konkretne wartości z kart produktów)
  - H2: **Tabela porównawcza** (kamizelka, bluza, kurtka, kurtka puchowa, koszulka bazowa Workskin: zakres ochrony, swoboda ruchu, miejsce w ubiorze, ochrona przed wiatrem i wodą, typowe zastosowanie, dla kogo; wersje damskie i męskie, rozmiarówka)
  - H2: Kamizelka: kiedy jest najlepszym wyborem (praca w ruchu, montaż, magazyn, warstwa pod kurtkę roboczą, najmniej krępuje ramiona)
  - H2: Bluza i koszulka bazowa: warstwa środkowa i pod spód (praca w hali i na zmianę wewnątrz i na zewnątrz, zgodność z odzieżą ostrzegawczą)
  - H2: Kurtka i kurtka puchowa: pełna ochrona (praca statyczna na zewnątrz, ekipy dekarskie i drogowe, zimowe budowy, wiatr i opad)
  - H2: Werdykt: co wybrać do rodzaju pracy - **mini-tabela** (praca fizyczna w ruchu, praca statyczna na mrozie, praca zmienna wewnątrz i na zewnątrz, praca w uprzęży lub w odzieży ostrzegawczej)
  - H2: Praktyka użytkowania (pranie po wyjęciu akumulatora, ładowanie w cieple, akumulator jako powerbank, wersje bez akumulatora i zestawy, rozmiar z zapasem na warstwę pod spodem)
  - H2: Czy to się opłaca w firmie (kilka warstw kontra jedno źródło ciepła, praca zimą bez utraty precyzji ruchów, jeden system M12 do narzędzi i odzieży)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Jak działa odzież podgrzewana Milwaukee M12? · Ile godzin działa kurtka podgrzewana na jednym akumulatorze? · Czy odzież podgrzewaną można prać? · Kamizelka czy kurtka podgrzewana: co wybrać? · Czy do odzieży podgrzewanej trzeba dokupić akumulator?
- **kafelki produktowe:** inline przy sekcji o kamizelce `[PRODUKT: 321:<kamizelka podgrzewana Milwaukee M12> | ciepło korpusu przy pełnej swobodzie ramion, wchodzi pod kurtkę roboczą | Największa swoboda]`; inline przy sekcji o kurtce `[PRODUKT: 131:<kurtka podgrzewana Milwaukee M12> | grzanie plus ochrona przed wiatrem przy pracy statycznej na zewnątrz | Pełna ochrona]`; blok przed FAQ `[PRODUKTY: System M12 na zimne dni || <bluza podgrzewana M12> | warstwa środkowa do pracy zmiennej || <akumulator M12> | zasilanie odzieży i narzędzi w jednym systemie || <czapka zimowa> | uzupełnienie kompletu na mróz]`. Rank: `-Rank "podgrzewana"`, `-Rank "akumulator M12"`, `-Rank "czapka zimowa"`. Kategorie: 321 kamizelki, 131 kurtki, 259 bluzy, 137 koszulki, 322 czapki.
- **linkowanie wewn.:** kategoria **BHP -> odzież podgrzewana: kamizelki (321), kurtki (131), bluzy (259)**; w bok: „Odzież robocza na deszcz i chłód: normy EN 343, EN 342 i EN 14058" (wpis 80, publikacja 21.08, link bezpieczny), „Akumulatory Milwaukee M18: pojemność, ładowanie, kompatybilność" (wpis #13), „Milwaukee M12 czy M18: który system akumulatorowy wybrać" (wpis #01b).
- **hero:** monter na placu w chłodny poranek wpina akumulator do kieszeni kamizelki podgrzewanej pod kurtką roboczą, para oddechu, chłodne niebieskie światło, czerwony akcent akumulatora, bez logo.
  - `hero_image_alt`: „Pracownik wpina akumulator do kieszeni odzieży podgrzewanej przed rozpoczęciem pracy w chłodny poranek"
- **uzasadnienie:** cztery nowe kategorie odzieżowe (131, 137, 259, 321) mają łącznie ponad 120 pozycji i zero linków wewnętrznych, a odzież podgrzewana to segment o wysokiej wartości koszyka, w którym autoryzacja Milwaukee działa jako argument zaufania. Zapytania rosną od września. Wpis nie kanibalizuje 80 (tam normy i warstwy, tu system i wybór kroju) i domyka ścieżkę: norma, warstwa, produkt.

---

## 11. „Dmuchawa do liści akumulatorowa: jak dobrać" (Poradnik, klaster B/H, SEZON)

- **Plik:** `82-dmuchawa-do-lisci-akumulatorowa-jak-dobrac.json` · **slug/seo_url:** `dmuchawa-do-lisci-akumulatorowa-jak-dobrac`
- **tytuł (H1):** Dmuchawa do liści akumulatorowa: jak dobrać
- **kategoria:** Poradnik
- **klaster:** B (elektronarzędzia) / H (sezonowy) · **typ:** PZ · **intencja:** informacyjna -> komercyjna (pik wrzesień i październik)
- **planowana_data:** 2026-08-23
- **fraza główna:** dmuchawa do liści akumulatorowa
- **frazy poboczne:** jaka dmuchawa do liści, dmuchawa m18 czy m12, wydajność dmuchawy m3/h, dmuchawa z odkurzaczem do liści, dmuchawa do osuszania kostki
- **struktura (schemat „Poradnik": parametry w tabeli, kryteria, dobór, FAQ):**
  - *Lead 40-60 słów:* dmuchawę do liści dobiera się według dwóch parametrów: przepływu powietrza w metrach sześciennych na godzinę, który decyduje o tym, ile liści przesuniemy naraz, oraz prędkości powietrza, która odrywa mokre liście od podłoża. Do małego ogrodu wystarczy model kompaktowy, do dużych powierzchni potrzebna jest wyższa klasa.
  - H2: Do czego naprawdę używa się dmuchawy (liście z trawnika i kostki, czyszczenie warsztatu i hali z pyłu, osuszanie powierzchni przed malowaniem lub klejeniem, sprzątanie po cięciu i szlifowaniu, świeży puch śniegu)
  - H2: **Tabela parametrów** (przepływ w m3/h, prędkość powietrza, tryb turbo, płynna regulacja, blokada spustu, waga, hałas, typ akumulatora: co każdy parametr oznacza dla użytkownika; wartości modeli z oferty do domknięcia)
  - H2: Kompaktowa czy pełnowymiarowa - **tabela** (dmuchawa 12 V do warsztatu i drobnych prac, dmuchawa 18 V do ogrodu, dmuchawa dwuakumulatorowa i wysokowydajna do dużych powierzchni: powierzchnia, czas pracy, waga, hałas)
  - H2: Akumulator i czas pracy (pojemność w Ah kontra tryb pracy, tryb turbo skraca czas wielokrotnie, drugi akumulator zamiast wyższego modelu, jeden system akumulatorów do narzędzi i sprzętu ogrodowego)
  - H2: Dmuchawa, odkurzacz do liści czy grabie (kiedy dmuchawa nie wystarczy, rozdrabnianie liści, mokre liście przyklejone do kostki)
  - H2: Praca kulturalna i bezpieczna (godziny pracy i sąsiedzi, okulary i ochronniki słuchu, kierunek nawiewu, uwaga na żwir i kamienie, maska przy pyle)
  - H2: Dobór do sytuacji - **mini-tabela** (mały ogród i taras, działka z drzewami, plac firmowy i parking, warsztat i hala, prace przygotowawcze przed klejeniem lub malowaniem)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Jaka wydajność dmuchawy do liści wystarczy? · Czym różni się przepływ powietrza od prędkości powietrza? · Ile działa dmuchawa akumulatorowa na jednym akumulatorze? · Czy dmuchawą można sprzątać mokre liście? · Czy dmuchawa nadaje się do czyszczenia warsztatu?
- **kafelki produktowe:** inline przy sekcji o modelach kompaktowych `[PRODUKT: 301:<dmuchawa Milwaukee M12> | lekki model do warsztatu, tarasu i szybkiego przedmuchania stanowiska | Kompakt]`; inline przy sekcji o dużych powierzchniach `[PRODUKT: 301:<dmuchawa Milwaukee M18 FUEL> | zapas przepływu i prędkości powietrza do liści na dużym terenie | Duży ogród]`; blok przed FAQ `[PRODUKTY: Na sezon opadania liści || <dmuchawa akumulatorowa> | podstawowe narzędzie do liści i pyłu || <akumulator o większej pojemności> | dłuższa praca bez przerwy na ładowanie || <ochronniki słuchu i okulary> | praca z dmuchawą to hałas i unoszony pył]`. Rank: `-Rank "dmuchawa"`, `-Rank "akumulator M18"`, `-Rank "ochronniki słuchu"`.
- **linkowanie wewn.:** kategoria **Narzędzia ogrodowe -> dmuchawy (id 301)** jako główny cel; w bok: „Podkaszarka, kosa spalinowa czy kosiarka: co wybrać do trawy" (wpis #36), „Hałas w pracy: normy dB, obowiązki i dobór ochronników słuchu" (wpis 68).
- **hero:** osoba w ochronnikach słuchu zdmuchuje mokre liście z kostki brukowej przed garażem, liście w ruchu, chłodne niebieskie światło jesiennego poranka, czerwony korpus urządzenia bez logo.
  - `hero_image_alt`: „Praca dmuchawą akumulatorową przy zdmuchiwaniu mokrych liści z kostki brukowej przed garażem"
- **uzasadnienie:** kategoria 301 jest nowa (13 pozycji) i nie ma linków wewnętrznych, a popyt na dmuchawy jest ostro sezonowy z pikiem od końca września. Publikacja w sierpniu daje przewagę indeksacji. Wpis ma kąt, którego nie mają poradniki ogrodowe: dmuchawa jako narzędzie warsztatowe do czyszczenia i osuszania powierzchni przed klejeniem, co spina go z klastrem chemii i grupą B2B.

---

## 12. „Drewno opałowe na sezon: cięcie, łupanie i sezonowanie krok po kroku" (Krok po kroku, klaster B/H, SEZON)

- **Plik:** `83-drewno-opalowe-ciecie-lupanie-sezonowanie.json` · **slug/seo_url:** `drewno-opalowe-ciecie-lupanie-sezonowanie-krok-po-kroku`
- **tytuł (H1):** Drewno opałowe na sezon: cięcie, łupanie i sezonowanie krok po kroku
- **kategoria:** Krok po kroku
- **klaster:** B (elektronarzędzia) / H (sezonowy) · **typ:** HT · **intencja:** informacyjna sezonowa -> komercyjna
- **planowana_data:** 2026-08-24
- **fraza główna:** jak sezonować drewno opałowe
- **frazy poboczne:** wilgotność drewna opałowego, jak ciąć drewno pilarką akumulatorową, układanie drewna w stos, ile schnie drewno opałowe, bhp przy pilarce łańcuchowej
- **struktura (schemat „Krok po kroku"):**
  - *Lead 40-60 słów:* drewno opałowe przygotowuje się w trzech etapach: cięciu na wałki o długości paleniska, łupaniu na polana i sezonowaniu w przewiewnym stosie. Suche drewno ma wilgotność poniżej 20 procent, a osiąga ją po roku lub dwóch, zależnie od gatunku. Palenie mokrym drewnem to sadza, zaklejona szyba i mniej ciepła.
  - H2: Narzędzia i materiały - **lista** (pilarka łańcuchowa z naostrzonym łańcuchem, olej do smarowania prowadnicy, kozioł do cięcia, siekiera lub łuparka, klin, wilgotnościomierz do drewna, ŚOI: kask z osłoną twarzy i ochronnikami, rękawice, obuwie ochronne, spodnie z wkładką antyprzecięciową)
  - H2: Krok 1: cięcie na wałki (długość dopasowana do komory paleniskowej z zapasem, stabilne podparcie na koźle, strefa cięcia wolna od osób, praca środkiem prowadnicy)
  - H2: Krok 2: łupanie (kiedy drewno łupie się najlepiej, technika i pozycja, klin przy sękach, dlaczego łupane polana schną szybciej niż okrąglaki)
  - H2: Krok 3: układanie stosu (podkład odrywający drewno od gruntu, przewiew między rzędami, zadaszenie góry bez zamykania boków, ekspozycja na wiatr i słońce)
  - H2: Krok 4: kontrola wilgotności (wilgotnościomierz na świeżym przełamie polana, cel poniżej 20 procent, typowe czasy sezonowania dla drewna miękkiego i twardego)
  - H2: Krok 5: przenoszenie do domu (zapas na kilka dni w pomieszczeniu, brak długiego składowania w salonie, owady i wilgoć z gruntu)
  - H2: Bezpieczeństwo pracy z pilarką - **lista** (pozycja stóp, odbicie prowadnicy, hamulec łańcucha, praca bez pośpiechu i nigdy w pojedynkę przy grubym drewnie, przerwy, ostry łańcuch to bezpieczniejszy łańcuch)
  - H2: Częste błędy (cięcie tępym łańcuchem, stos wprost na ziemi, zafoliowany stos od boków, palenie drewnem po roku bez pomiaru wilgotności, magazynowanie w wilgotnej piwnicy)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Jaka wilgotność drewna opałowego jest prawidłowa? · Ile sezonuje się drewno opałowe? · Czy pilarka akumulatorowa poradzi sobie z drewnem opałowym? · Jak układać stos drewna, żeby szybciej wysychało? · Jakie ŚOI są potrzebne przy pracy pilarką?
- **kafelki produktowe:** inline przy kroku 1 `[PRODUKT: 300:<pilarka łańcuchowa Milwaukee M18 FUEL> | cięcie wałków bez spalin i rozruchu linką, praca przy domu i w garażu | Cięcie]`; inline przy sekcji o BHP `[PRODUKT: <kask z osłoną twarzy i ochronnikami słuchu> | podstawowa ochrona przy pilarce, jeden element zamiast trzech | Ochrona głowy]`; blok przed FAQ `[PRODUKTY: Zestaw na przygotowanie opału || <pilarka łańcuchowa> | cięcie drewna na wymiar paleniska || <olej do prowadnicy lub łańcuch zapasowy> | eksploatacja bez przestojów || <rękawice robocze z chwytem> | praca z drewnem, korą i klinem]`. Rank: `-Rank "pilarka łańcuchowa"`, `-Rank "łańcuch"`, `-Rank "kask"`.
- **linkowanie wewn.:** kategoria **Elektronarzędzia i ogród -> pilarki łańcuchowe (id 300)** jako główny cel; w bok: „Jak wybrać pilarkę: łańcuchowa, tarczowa, szablasta" (wpis #21, tam wybór narzędzia, tu praca sezonowa), „Przegląd kominka przed sezonem grzewczym" (wpis 77, publikacja 18.08, link bezpieczny).
- **hero:** fachowiec w kasku z osłoną twarzy tnie pilarką akumulatorową wałek drewna na koźle, obok ułożony stos polan, chłodne niebieskie światło poranka, czerwony korpus pilarki bez logo.
  - `hero_image_alt`: „Fachowiec w kasku z osłoną twarzy tnie pilarką akumulatorową drewno opałowe na koźle, obok ułożony stos polan"
- **uzasadnienie:** kategoria 300 (pilarki, 21 pozycji) jest nowa i bez linków wewnętrznych, a przygotowanie opału to najbardziej masowa czynność sezonowa końca lata w naszym regionie. Wpis nie kanibalizuje #21 (tam dobór typu pilarki, tu praca sezonowa i sezonowanie drewna), a domyka logiczny łańcuch z wpisami 76 i 77: uszczelnij kominek, przygotuj drewno, pal suchym. Element BHP (kask, spodnie antyprzecięciowe) wzmacnia klaster G i E-E-A-T.

---

## 13. „Wilgoć w piwnicy i garażu po lecie: skąd się bierze i jak ją wyprowadzić" (Problemy i porady, klaster C/F)

- **Plik:** `84-wilgoc-w-piwnicy-i-garazu-po-lecie.json` · **slug/seo_url:** `wilgoc-w-piwnicy-i-garazu-po-lecie-przyczyny-i-rozwiazania`
- **tytuł (H1):** Wilgoć w piwnicy i garażu po lecie: skąd się bierze i jak ją wyprowadzić
- **kategoria:** Problemy i porady
- **klaster:** C (chemia budowlana) / F (wentylacja) · **typ:** FAQ/troubleshooting · **intencja:** problemowa sezonowa -> komercyjna
- **planowana_data:** 2026-08-25
- **fraza główna:** wilgoć w piwnicy
- **frazy poboczne:** mokra ściana w garażu, skraplanie na posadzce piwnicy, jak osuszyć piwnicę, wykwity solne na ścianie, wentylacja piwnicy latem czy zimą
- **struktura (schemat „Problemy i porady")**
  - *Lead 40-60 słów:* wilgoć w piwnicy ma trzy główne źródła: podciąganie kapilarne z gruntu przez ścianę bez izolacji poziomej, przeciek przez ścianę zewnętrzną oraz kondensację ciepłego powietrza na chłodnych murach. Latem najczęściej działa ta trzecia przyczyna, dlatego wietrzenie piwnicy w upalny dzień pogarsza sprawę, zamiast pomagać.
  - H2: Objawy i przyczyny - **tabela objaw, przyczyna, rozwiązanie** (mokra posadzka i krople na ścianie latem: kondensacja, wietrzyć nocą i chłodnym rankiem; ciemny pas u dołu ściany: podciąganie kapilarne, izolacja pozioma i tynk renowacyjny; mokra plama po deszczu: przeciek, izolacja pionowa i opaska; białe wykwity: sole z muru, szczotkowanie i preparat; zapach stęchlizny i pleśń na rzeczach: brak wymiany powietrza, kratka i przewietrzanie; rdza na narzędziach: wilgotność powyżej 60 procent)
  - H2: Dlaczego latem nie wietrzy się piwnicy w środku dnia (ciepłe wilgotne powietrze na zimnej ścianie oddaje wodę; kiedy wietrzyć, żeby osuszać, a nie dowilżać)
  - H2: Jak zmierzyć problem, zanim zaczniesz remont (higrometr w piwnicy i na zewnątrz, test folii przyklejonej do ściany: kondensacja pod folią kontra wilgoć od strony muru, obserwacja po deszczu)
  - H2: Co da się zrobić szybko (przewietrzanie sterowane porą doby, udrożnienie kratek i okienek, odsunięcie rzeczy od ścian, podkłady pod kartony, wentylator do wymuszenia obiegu, osuszacz w zamkniętym pomieszczeniu)
  - H2: Co wymaga roboty budowlanej (izolacja pionowa od zewnątrz, opaska i odprowadzenie wody z rynny, izolacja pozioma iniekcyjna, tynki renowacyjne, powłoka mineralna od wewnątrz jako półśrodek)
  - H2: Garaż: dodatkowe źródła wody (mokry samochód i śnieg, brak nawiewu przy szczelnej bramie, posadzka bez izolacji; kratka nawiewna i wywiewna po przeciwnych stronach)
  - H2: Jak zapobiegać przed jesienią (kolejność: odciąć źródło, potem wentylować, na końcu wykańczać; czego nie robić: farba wodoszczelna na wilgotną ścianę, styropian na mokry mur, zaklejanie kratek)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Dlaczego w piwnicy skrapla się woda latem? · Kiedy wietrzyć piwnicę, żeby ją osuszyć? · Jak sprawdzić, czy wilgoć jest z gruntu czy z powietrza? · Czy farba wodoszczelna rozwiąże problem wilgotnej ściany? · Jak zabezpieczyć garaż przed wilgocią jesienią?
- **kafelki produktowe:** inline przy sekcji o pracach budowlanych `[PRODUKT: <masa lub powłoka hydroizolacyjna z oferty> | odcina wodę od strony gruntu, gdy problem jest przeciekowy | Izolacja]`; inline przy sekcji o wentylacji `[PRODUKT: <kratka wentylacyjna Awenta lub wentylator wywiewny> | wymusza wymianę powietrza tam, gdzie grawitacja nie daje rady | Wentylacja]`; blok przed FAQ `[PRODUKTY: Pierwsze kroki przy wilgotnej piwnicy || <higrometr lub miernik wilgotności> | pomiar zamiast zgadywania || <preparat na pleśń> | usunięcie skutków przed naprawą przyczyny || <kratka lub wentylator> | stała wymiana powietrza]`. Rank: `-Rank "higrometr"`, `-Rank "kratka wentylacyjna"`, `-Rank "pleśń"`.
- **linkowanie wewn.:** kategorie **Chemia budowlana** (hydroizolacje) + **Systemy wentylacyjne** (kratki, wentylatory Awenta); w bok: „Hydroizolacja fundamentów i ścian piwnicy" (wpis 72, publikacja 13.08, link bezpieczny), „Preparat na pleśń, grzyb i glony" (wpis 74, publikacja 15.08), „Jak usunąć pleśń ze ściany i fugi" (wpis #29).
- **hero:** latarka oświetla ciemny pas wilgoci u dołu ściany piwnicy z widocznymi wykwitami, na posadzce higrometr, chłodne niebieskie światło, bez logo.
  - `hero_image_alt`: „Ciemny pas wilgoci i białe wykwity u dołu ściany piwnicy, na posadzce higrometr do pomiaru wilgotności"
- **uzasadnienie:** temat zbiera trzy nasze mocne klastry naraz (chemia, wentylacja, problem po lecie) i domyka trójkąt sezonowy z wpisami 72 i 74. Zapytania o wilgoć w piwnicy kulminują na przełomie lata i jesieni, gdy kondensacja jest najsilniejsza, a treść wprost prowadzi do dwóch koszyków: hydroizolacji i wentylacji. Kontrintuicyjna porada o wietrzeniu (nie w upalne południe) to unikalny, cytowalny fragment pod AI Overviews.

---

## 14. „Nawiewniki okienne: ciśnieniowe, higrosterowane czy ręczne" (Porównania, klaster F)

- **Plik:** `85-nawiewniki-okienne-cisnieniowe-higrosterowane-reczne.json` · **slug/seo_url:** `nawiewniki-okienne-cisnieniowe-higrosterowane-czy-reczne`
- **tytuł (H1):** Nawiewniki okienne: ciśnieniowe, higrosterowane czy ręczne
- **kategoria:** Porównania
- **klaster:** F (wentylacja / Awenta) · **typ:** POR · **intencja:** komercyjna (GSC: wentylacja 6,6k wyśw. przy pozycjach 39-61)
- **planowana_data:** 2026-08-26
- **fraza główna:** nawiewniki okienne
- **frazy poboczne:** nawiewnik higrosterowany czy ciśnieniowy, montaż nawiewnika w oknie pcv, czy nawiewnik wychładza mieszkanie, nawiewnik do okna cena montażu, wymagany nawiew powietrza w mieszkaniu
- **struktura (schemat „Porównania"):**
  - *Lead 40-60 słów:* nawiewnik okienny doprowadza świeże powietrze do pomieszczenia bez otwierania okna i jest warunkiem działania wentylacji grawitacyjnej w szczelnym budynku. Nawiewnik ciśnieniowy reaguje na różnicę ciśnień i wiatr, higrosterowany na wilgotność powietrza w pomieszczeniu, a ręczny otwiera i przymyka użytkownik.
  - H2: Po co w ogóle nawiewnik (wentylacja grawitacyjna potrzebuje napływu; szczelne okna zatrzymują wywiew, skutkiem jest kondensacja, pleśń i ciąg wsteczny przy urządzeniach spalających)
  - H2: **Tabela porównawcza** (ciśnieniowy, higrosterowany, ręczny, akustyczny: zasada działania, reakcja na warunki, sterowanie przez użytkownika, wpływ na hałas z zewnątrz, wychładzanie, typowe pomieszczenia, cena względna, montaż)
  - H2: Higrosterowany: kiedy wygrywa (sypialnia i mieszkanie z dużą produkcją pary, automatyczne ograniczanie napływu przy suchym powietrzu zimą, mniejsze straty ciepła)
  - H2: Ciśnieniowy: kiedy wystarczy (stabilny napływ, ograniczenie przewiewu przy silnym wietrze, budynki bardziej narażone na podmuchy)
  - H2: Ręczny i akustyczny: sytuacje szczególne (pełna kontrola użytkownika, ruchliwa ulica i tłumienie hałasu)
  - H2: Montaż: w ramie okna, w skrzydle czy nadokienny - **mini-tabela** (frezowanie ramy lub skrzydła, nawiewnik nadokienny bez ingerencji w profil, montaż w ścianie jako alternatywa; kiedy potrzebny fachowiec, gwarancja okna)
  - H2: Ile nawiewników i gdzie (pomieszczenia z napływem: pokoje i sypialnie; pomieszczenia z wywiewem: kuchnia, łazienka, WC; drzwi z podcięciem lub kratką jako warunek przepływu)
  - H2: Werdykt i częste błędy (zamykanie nawiewnika na zimę, nawiewnik w łazience zamiast w pokoju, nawiewnik przy niedrożnym kanale wywiewnym nie zadziała, kurz i brak czyszczenia filtra)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Czy nawiewnik okienny wychładza mieszkanie? · Nawiewnik higrosterowany czy ciśnieniowy: co wybrać? · Czy nawiewnik można zamontować w gotowym oknie? · Ile nawiewników potrzeba w mieszkaniu? · Czy nawiewnik pomoże na parę na oknach?
- **kafelki produktowe:** inline przy sekcji o higrosterowanych `[PRODUKT: <nawiewnik higrosterowany z oferty> | reaguje na wilgotność w pomieszczeniu i ogranicza napływ, gdy powietrze jest suche | Automatyczny]`; inline przy sekcji o montażu `[PRODUKT: <nawiewnik ciśnieniowy lub nadokienny> | stabilny napływ, montaż bez głębokiej ingerencji w profil okna | Prosty montaż]`; blok przed FAQ `[PRODUKTY: Komplet dla działającej wentylacji || <nawiewnik okienny> | napływ świeżego powietrza || <kratka wentylacyjna> | drożny wywiew z kuchni i łazienki || <wentylator z higrostatem> | wsparcie tam, gdzie grawitacja nie wystarcza]`. Rank: `-Rank "nawiewnik"`, `-Rank "kratka wentylacyjna"`, `-Rank "wentylator higrostat"`.
- **linkowanie wewn.:** kategoria **Systemy wentylacyjne** -> nawiewniki, kratki, wentylatory Awenta; w bok: „Para na oknach i wilgoć po lecie" (wpis 71), „Jaka kratka wentylacyjna i anemostat" (wpis #19), „Jak uszczelnić okna i drzwi przed jesienią" (wpis 70).
- **hero:** zbliżenie na nawiewnik zamontowany w górnej części ramy okna PCV, w tle jesienny widok za szybą, dłoń przestawia suwak, chłodne niebieskie światło, bez logo.
  - `hero_image_alt`: „Nawiewnik okienny w górnej ramie okna PCV, dłoń reguluje przepływ powietrza suwakiem"
- **uzasadnienie:** wentylacja ma w GSC 6,6k wyświetleń przy pozycjach 39-61, czyli popyt jest, a my nie istniejemy w wynikach. Nawiewniki to jedyny element tej niszy, którego jeszcze nie opisaliśmy (mamy wentylatory, kratki, anemostaty, wentylację letnią i parę na oknach), a jednocześnie to element, o który klient pyta wprost po przeczytaniu wpisu 70 i 71. Porównanie trzech typów z tabelą jest cytowalne i domyka klaster F przed sezonem kondensacji.

---

## 15. „Zazimowanie narzędzi ogrodowych: kosiarka, podkaszarka i pilarka krok po kroku" (Krok po kroku, klaster H/B, SEZON)

- **Plik:** `86-zazimowanie-narzedzi-ogrodowych-krok-po-kroku.json` · **slug/seo_url:** `zazimowanie-narzedzi-ogrodowych-kosiarka-podkaszarka-pilarka`
- **tytuł (H1):** Zazimowanie narzędzi ogrodowych: kosiarka, podkaszarka i pilarka krok po kroku
- **kategoria:** Krok po kroku
- **klaster:** H (sezonowy) / B (elektronarzędzia) · **typ:** HT · **intencja:** informacyjna sezonowa -> komercyjna
- **planowana_data:** 2026-08-27
- **fraza główna:** jak przygotować kosiarkę do zimy
- **frazy poboczne:** zazimowanie narzędzi ogrodowych, ostrzenie noża kosiarki, przechowywanie akumulatora zimą, konserwacja pilarki łańcuchowej, ostatnie koszenie trawy w sezonie
- **struktura (schemat „Krok po kroku"):**
  - *Lead 40-60 słów:* zazimowanie narzędzi ogrodowych to cztery czynności: dokładne czyszczenie z trawy i żywicy, ostrzenie lub wymiana ostrzy, konserwacja części ruchomych oraz właściwe przechowanie akumulatorów, czyli naładowanych częściowo i w dodatniej temperaturze. Sprzęt schowany brudny na sześć miesięcy wraca na wiosnę z rdzą i tępym nożem.
  - H2: Narzędzia i materiały - **lista** (szczotka i skrobak, preparat czyszczący, olej konserwujący lub spray penetrujący, pilnik lub ostrzałka, klucz do noża kosiarki, olej do prowadnicy pilarki, rękawice odporne na przecięcie, worki i pokrowce)
  - H2: Kiedy zacząć (po ostatnim koszeniu, jeszcze przy dodatnich temperaturach, żeby preparaty i smary pracowały zgodnie z kartą)
  - H2: Krok 1: kosiarka (opróżnienie kosza, czyszczenie tunelu wyrzutowego i spodu obudowy przy odłączonym zasilaniu, kontrola i ostrzenie noża, wyważenie ostrza, zabezpieczenie antykorozyjne)
  - H2: Krok 2: podkaszarka i trymer (wymiana żyłki lub noża, czyszczenie osłony, kontrola głowicy, przegląd przewodu lub gniazda akumulatora)
  - H2: Krok 3: pilarka łańcuchowa (opróżnienie oleju z układu smarowania wg instrukcji, czyszczenie prowadnicy i rowka, kontrola napięcia i ostrości łańcucha, hamulec łańcucha, przechowywanie w osłonie)
  - H2: Krok 4: akumulatory i ładowarki - **tabela** (stan naładowania do przechowania, temperatura przechowywania, czego nie robić: ładowanie zmarzniętego ogniwa, przechowywanie na mrozie w blaszanym garażu, pozostawienie akumulatora rozładowanego do zera)
  - H2: Krok 5: przechowywanie sprzętu (suche pomieszczenie, sprzęt odsunięty od podłoża i ścian, pokrowce, spisanie części do kupienia na wiosnę)
  - H2: Częste błędy (mycie silnikowych elementów strumieniem wody, chowanie mokrego sprzętu, tępe ostrze zostawione na wiosnę, akumulator zimujący w nieogrzewanym garażu, brak przeglądu przewodów)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Jak przygotować kosiarkę akumulatorową do zimy? · W jakiej temperaturze przechowywać akumulatory narzędzi? · Czy nóż kosiarki trzeba ostrzyć co sezon? · Jak zakonserwować pilarkę łańcuchową na zimę? · Kiedy zrobić ostatnie koszenie trawnika?
- **kafelki produktowe:** inline przy kroku 1 `[PRODUKT: 303:<ostrze do kosiarki Milwaukee> | wymiana taniej i szybciej niż ratowanie wyszczerbionego noża | Nowe ostrze]`; inline przy kroku 3 `[PRODUKT: 300:<łańcuch lub olej do prowadnicy> | zużyty łańcuch zostawiony na zimę wraca tępy i rozciągnięty | Serwis pilarki]`; blok przed FAQ `[PRODUKTY: Na koniec sezonu ogrodowego || <ostrze lub łańcuch zamienny> | wymiana zamiast walki ze starym || <preparat konserwujący lub olej> | ochrona metalu przed rdzą || <akumulator zapasowy> | wymiana zmęczonego ogniwa przed nowym sezonem]`. Rank: `-Rank "ostrze kosiarki"`, `-Rank "łańcuch"`, `-Rank "olej do prowadnicy"`.
- **linkowanie wewn.:** kategorie **Narzędzia ogrodowe -> kosiarki (id 303), pilarki (id 300), dmuchawy (id 301)**; w bok: „Dmuchawa do liści akumulatorowa: jak dobrać" (wpis 82, publikacja 23.08, link bezpieczny), „Podkaszarka, kosa spalinowa czy kosiarka" (wpis #36), „Drewno opałowe na sezon" (wpis 83, publikacja 24.08).
- **hero:** ręce w rękawicach czyszczą szczotką spód obudowy kosiarki postawionej na sztorc w garażu, obok klucz i nowe ostrze, chłodne niebieskie światło, bez logo.
  - `hero_image_alt`: „Czyszczenie spodu obudowy kosiarki szczotką przed zimowym przechowaniem, obok klucz i nowe ostrze"
- **uzasadnienie:** kategorie 303 (kosiarki) i 300 (pilarki) są nowe i bez linków wewnętrznych, a serwisowy poradnik końca sezonu sprzedaje części zamienne (ostrza, łańcuchy, oleje, akumulatory), czyli produkty o wysokiej rotacji i marży. Temat nie kanibalizuje #36 (tam wybór urządzenia), a naturalnie linkuje do 82 i 83 z tej samej partii, budując mikroklaster jesienny wokół narzędzi ogrodowych.

---

## 16. „Rękawice do pracy w chłodzie: norma EN 511 i dobór na jesień" (Normy i BHP, klaster G, SEZON)

- **Plik:** `87-rekawice-do-pracy-w-chlodzie-norma-en-511.json` · **slug/seo_url:** `rekawice-do-pracy-w-chlodzie-norma-en-511-dobor`
- **tytuł (H1):** Rękawice do pracy w chłodzie: norma EN 511 i dobór na jesień
- **kategoria:** Normy i BHP
- **klaster:** G (BHP) · **typ:** FAQ/GEO (compliance) · **intencja:** informacyjna normatywna -> komercyjna (zaopatrzenie firm)
- **planowana_data:** 2026-08-28
- **fraza główna:** rękawice ocieplane norma
- **frazy poboczne:** en 511 co oznacza, rękawice zimowe robocze wodoodporne, rękawice do pracy na mrozie, piktogram płatka śniegu na rękawicach, rękawice ocieplane a chwyt
- **struktura (schemat „Normy i BHP"):**
  - *Lead 40-60 słów:* norma EN 511 opisuje rękawice chroniące przed zimnem i podaje trzy cyfry pod piktogramem płatka śniegu. Pierwsza oznacza odporność na zimno konwekcyjne w skali od 0 do 4, druga na zimno kontaktowe od 0 do 4, a trzecia przenikanie wody: 0 znaczy, że rękawica przemaka, 1 że przez 30 minut nie.
  - H2: Trzy cyfry EN 511 - **tabela** (zimno konwekcyjne, zimno kontaktowe, przenikanie wody: co bada każdy parametr, jak przekłada się na pracę na zewnątrz i na kontakt z zimnym metalem, dlaczego X oznacza brak badania)
  - H2: EN 511 nie działa sama (rękawica zimowa niemal zawsze ma też EN 388 na odporność mechaniczną; jak czytać oba piktogramy razem, kiedy dochodzi EN 407 lub EN ISO 374)
  - H2: Ocieplenie kontra chwyt i czucie - **tabela** (rękawica gruba ocieplana, rękawica z cienką podszewką i powleczeniem, rękawica wodoodporna z membraną, rękawica z długim mankietem: ciepło, precyzja, chwyt na mokrym, typowe prace)
  - H2: Mokra rękawica przestaje grzać (dlaczego wodoodporność to często ważniejszy parametr niż izolacja; praca w deszczu, śniegu i przy mokrym drewnie)
  - H2: Dobór do stanowiska - **mini-tabela** (praca statyczna na zewnątrz, montaż wymagający precyzji, praca z mokrym materiałem, chwytanie zimnego metalu i rusztowań, magazyn chłodniczy, praca z chemią w chłodzie)
  - H2: Rozmiar i praktyka (za ciasna rękawica ocieplana marznie szybciej, dwie pary na zmianę, suszenie po pracy, kiedy rękawica idzie do wymiany)
  - H2: Obowiązki pracodawcy przy pracy w chłodzie (rękawice jako ŚOI, dobór na podstawie oceny ryzyka, nieodpłatne dostarczenie i wymiana po utracie właściwości)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Co oznaczają cyfry przy piktogramie płatka śniegu? · Czym różni się zimno konwekcyjne od kontaktowego? · Czy rękawice ocieplane muszą być wodoodporne? · Jakie rękawice do pracy na mrozie z metalem? · Czy pracodawca musi zapewnić rękawice ocieplane?
- **kafelki produktowe:** inline przy tabeli parametrów `[PRODUKT: <rękawice ocieplane z oferty> | ciepło i chwyt do prac na zewnątrz jesienią | Praca w chłodzie]`; inline przy sekcji o wodoodporności `[PRODUKT: <rękawice powlekane wodoodporne> | mokry materiał i deszcz bez utraty izolacji | Odporne na wodę]`; blok przed FAQ `[PRODUKTY: Ochrona rąk na jesienne prace || <rękawice ocieplane> | podstawowa ochrona przed zimnem || <rękawice powlekane> | chwyt na mokrym materiale || <kurtka robocza> | reszta kompletu na chłodne dni]`. Rank: `-Rank "rękawice ocieplane"`, `-Rank "rękawice powlekane"`, `-Rank "kurtka"`.
- **linkowanie wewn.:** kategoria **BHP -> rękawice robocze** (+ kurtki, id 131); w bok: „Rękawice robocze a norma EN 388" (wpis #16), „Rękawice chemoodporne a norma EN 374" (wpis 64), „Odzież robocza na deszcz i chłód: EN 343, EN 342 i EN 14058" (wpis 80, publikacja 21.08, link bezpieczny).
- **hero:** dłonie w ocieplanych rękawicach roboczych chwytają zimną stalową rurę rusztowania w mglisty poranek, krople na tkaninie, chłodne niebieskie światło, bez logo.
  - `hero_image_alt`: „Dłonie w ocieplanych rękawicach roboczych chwytają zimną rurę rusztowania w mglisty jesienny poranek"
- **uzasadnienie:** EN 511 zamyka trójkę norm ochrony rąk (EN 388 mechaniczna, EN 374 chemiczna, EN 511 zimno) i czyni z bloga kompletny hub tematyczny, którego nie ma żaden konkurent na Shoperze. BHP to największa luka GSC, a zapytania o rękawice zimowe zaczynają rosnąć we wrześniu. Tabela trzech cyfr jest krótka, jednoznaczna i idealnie cytowalna w AI Overviews.

---

## 17. „Jak sprawdzić, czy przewód jest pod napięciem: detektor bezdotykowy krok po kroku" (Krok po kroku, klaster B)

- **Plik:** `88-jak-sprawdzic-czy-przewod-jest-pod-napieciem.json` · **slug/seo_url:** `jak-sprawdzic-czy-przewod-jest-pod-napieciem-detektor-bezdotykowy`
- **tytuł (H1):** Jak sprawdzić, czy przewód jest pod napięciem: detektor bezdotykowy krok po kroku
- **kategoria:** Krok po kroku
- **klaster:** B (elektronarzędzia) · **typ:** HT · **intencja:** informacyjna -> komercyjna (nowa kategoria 304 bez ruchu)
- **planowana_data:** 2026-08-29
- **fraza główna:** jak sprawdzić czy przewód jest pod napięciem
- **frazy poboczne:** detektor napięcia bezdotykowy jak używać, próbnik napięcia który wybrać, cat iii czy cat iv, jak znaleźć przewód w ścianie, brak napięcia jak potwierdzić
- **struktura (schemat „Krok po kroku"):**
  - *Lead 40-60 słów:* obecność napięcia sprawdza się w trzech ruchach: testujemy detektor na znanym źródle napięcia, badamy przewód lub gniazdo, a potem ponownie sprawdzamy detektor na znanym źródle. Detektor bezdotykowy wykrywa pole wokół żyły i potrafi dać fałszywy wynik, dlatego brak napięcia potwierdza się przyrządem dwubiegunowym.
  - H2: Narzędzia - **lista** (detektor bezdotykowy z sygnalizacją dźwiękową i świetlną, próbnik dwubiegunowy lub miernik, latarka, rękawice, wkrętak izolowany; kategoria pomiarowa CAT III lub CAT IV dobrana do instalacji)
  - H2: Zanim zaczniesz: zasada ograniczonego zaufania (wyłączenie obwodu w rozdzielnicy nie zawsze odcina wszystko, opisy w rozdzielnicy bywają nieaktualne, przewód sterowany przełącznikiem schodowym, obwody oświetleniowe z przerwanym przewodem neutralnym)
  - H2: Krok 1: test detektora na znanym napięciu (dlaczego zaczyna się od sprawdzenia narzędzia, a nie instalacji)
  - H2: Krok 2: badanie przewodu lub gniazda (prowadzenie końcówki wzdłuż żyły, czułość, sygnał ciągły kontra przerywany, badanie przez izolację i przez tynk)
  - H2: Krok 3: potwierdzenie braku napięcia (próbnik dwubiegunowy na przewodzie fazowym i neutralnym, dopiero to daje podstawę do pracy)
  - H2: Krok 4: powtórny test narzędzia (kontrola, czy detektor nie padł w międzyczasie)
  - H2: Kiedy detektor bezdotykowy myli - **tabela objaw, przyczyna, co zrobić** (sygnał na przewodzie odłączonym: napięcie indukowane od sąsiedniej żyły; brak sygnału mimo napięcia: przewód ekranowany, głęboko w ścianie, w metalowej rurce lub trzymany bez odniesienia do ziemi; sygnał na całej ścianie: za wysoka czułość; brak reakcji: zużyta bateria)
  - H2: Szukanie przewodu w ścianie przed wierceniem (detektor napięcia kontra wykrywacz przewodów i profili, strefy prowadzenia instalacji, zasada wiercenia z zapasem odległości od gniazd i włączników)
  - H2: Granica samodzielnej pracy (wymiana źródła światła i badanie napięcia kontra ingerencja w instalację; prace w instalacji wykonuje osoba z uprawnieniami)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Jak działa bezdotykowy detektor napięcia? · Dlaczego detektor pokazuje napięcie na odłączonym przewodzie? · Czy detektor bezdotykowy wystarczy, żeby potwierdzić brak napięcia? · Co oznacza CAT III i CAT IV? · Jak znaleźć przewód w ścianie przed wierceniem?
- **kafelki produktowe:** inline przy liście narzędzi `[PRODUKT: 304:<detektor napięcia bezdotykowy Milwaukee z latarką> | szybka kontrola obecności napięcia bez rozkręcania osprzętu | Podstawa]`; inline przy sekcji o kategoriach pomiarowych `[PRODUKT: 304:<detektor napięcia Milwaukee CAT IV 1000 V> | wyższa kategoria pomiarowa do pracy przy rozdzielnicy i przyłączu | CAT IV]`; blok przed FAQ `[PRODUKTY: Zanim ruszysz instalację || <detektor napięcia> | kontrola przed dotknięciem przewodu || <próbnik dwubiegunowy lub miernik> | potwierdzenie braku napięcia || <wkrętaki izolowane VDE> | praca przy osprzęcie elektrycznym]`. Rank: `-Rank "detektor napięcia"`, `-Rank "próbnik"`, `-Rank "VDE"`.
- **linkowanie wewn.:** kategoria **Elektronarzędzia -> mierniki i detektory napięcia (id 304)** jako główny cel; w bok: „Jak zamontować wentylator łazienkowy krok po kroku" (wpis 56, tam praca przy zasilaniu 230 V), „Kombinerki, szczypce i obcinaki: jak dobrać do pracy" (wpis 53, szczypce VDE).
- **hero:** dłoń przykłada bezdotykowy detektor napięcia do przewodu wychodzącego z puszki w ścianie, dioda sygnalizacyjna świeci, obok wkrętak izolowany, chłodne niebieskie światło wnętrza w remoncie, bez logo.
  - `hero_image_alt`: „Dłoń przykłada bezdotykowy detektor napięcia do przewodu w puszce instalacyjnej podczas kontroli obwodu"
- **uzasadnienie:** kategoria 304 jest nowa (5 pozycji) i bez linków wewnętrznych, a fraza „jak sprawdzić, czy przewód jest pod napięciem" ma stały, szeroki popyt prosumencki i wprost prowadzi do taniego, łatwego do dołożenia produktu. Sekcja o fałszywych wskazaniach detektora to konkret ekspercki, którego nie ma w generycznych poradnikach, a element bezpieczeństwa (potwierdzenie brakiem napięcia przyrządem dwubiegunowym) to mocny sygnał E-E-A-T. Wpis wspiera też sezonowe montaże oświetlenia i wentylatorów.

---

## 18. „Montaż na elewacji i w ociepleniu: jak zamocować lampę, kamerę i uchwyt" (Poradnik, klaster D)

- **Plik:** `89-montaz-na-elewacji-i-w-ociepleniu-lampa-kamera-uchwyt.json` · **slug/seo_url:** `montaz-na-elewacji-i-w-ociepleniu-lampa-kamera-uchwyt`
- **tytuł (H1):** Montaż na elewacji i w ociepleniu: jak zamocować lampę, kamerę i uchwyt
- **kategoria:** Poradnik
- **klaster:** D (technika zamocowań) · **typ:** PZ · **intencja:** informacyjna techniczna -> komercyjna (montaż oświetlenia i monitoringu przed jesienią)
- **planowana_data:** 2026-08-30
- **fraza główna:** jak zamocować coś na ociepleniu
- **frazy poboczne:** montaż lampy na styropianie, kotwa dystansowa do ocieplenia, mocowanie kamery na elewacji, kołek do styropianu do zawieszenia, jak nie zrobić mostka termicznego
- **struktura (schemat „Poradnik": rodzaje rozwiązań w tabeli, kryteria, dobór, FAQ):**
  - *Lead 40-60 słów:* na ścianie z ociepleniem nie mocuje się nic bezpośrednio w styropianie. Lekkie przedmioty osadza się w specjalnych kotwach spiralnych do izolacji, a wszystko, co ma masę albo działa dźwignią, przenosi się na mur nośny za pomocą kotwy dystansowej lub tulei montażowej przechodzącej przez warstwę ocieplenia.
  - H2: Dlaczego zwykły kołek w ociepleniu nie trzyma (styropian i wełna nie przenoszą obciążenia, wilgoć w otworze, wyrwanie przy pierwszym mocniejszym obciążeniu, mostek termiczny i przemarzanie punktowe)
  - H2: **Tabela rozwiązań** (kotwa spiralna do styropianu, tuleja montażowa przechodząca przez ocieplenie, kotwa dystansowa z prętem gwintowanym, kołek ramowy długi w mur nośny, klejenie na masę hybrydową: obciążenie, typowe zastosowanie, ingerencja w ocieplenie, szczelność, poziom trudności)
  - H2: Dobór do przedmiotu - **mini-tabela** (lampa elewacyjna, kamera monitoringu, czujka ruchu, uchwyt na rower lub wąż, numer domu, skrzynka na listy, markiza i roleta, uchwyt anteny)
  - H2: Jak zamocować, żeby nie zalać ściany (uszczelnienie przejścia przewodu, kolejność: otwór, uszczelniacz, kotwa, kołnierz kapiący, przewód od dołu, silikon neutralny lub masa MS na styku z tynkiem)
  - H2: Przejście przewodu przez ocieplenie (peszel, rurka osłonowa, spadek na zewnątrz, uszczelnienie od strony muru, żeby wilgoć nie wchodziła do wnętrza)
  - H2: Czego nie robić (kołki rozporowe wbite w sam styropian, wiercenie udarem w miejscu z instalacją, mocowanie ciężaru do samego tynku cienkowarstwowego, brak uszczelnienia otworu przed zimą)
  - H2: Praktyka: kolejność prac i przygotowanie (wyznaczenie miejsca, sprawdzenie instalacji detektorem, dobór długości kotwy do grubości ocieplenia, kontrola po zimie)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Jak zamocować lampę na ścianie z ociepleniem? · Czy kołek rozporowy utrzyma się w styropianie? · Co to jest kotwa dystansowa i kiedy jej użyć? · Jak uszczelnić przejście przewodu przez elewację? · Jaką długość kotwy dobrać do 15 cm styropianu?
- **kafelki produktowe:** inline przy tabeli rozwiązań `[PRODUKT: <kotwa lub tuleja do montażu w ociepleniu z oferty> | przenosi obciążenie na mur nośny bez zgniatania izolacji | Do ocieplenia]`; inline przy sekcji o uszczelnianiu `[PRODUKT: <uszczelniacz neutralny lub masa MS> | szczelny styk z tynkiem i przejście przewodu przed jesiennymi deszczami | Szczelność]`; blok przed FAQ `[PRODUKTY: Do montażu na elewacji || <kotwa do ocieplenia> | pewne mocowanie przez warstwę izolacji || <uszczelniacz neutralny> | zabezpieczenie otworu i przejścia przewodu || <wiertło do muru> | otwór w warstwie nośnej bez rozbijania tynku]`. Rank: `-Rank "kotwa"`, `-Rank "uszczelniacz neutralny"`, `-Rank "wiertło do betonu"`.
- **linkowanie wewn.:** kategoria **Technika zamocowań** -> kotwy, kołki, tuleje; w bok: „Jak wybrać kotwę i kiedy zamiast kołka" (wpis #31), „Jaki kołek do gazobetonu, betonu i pustaka" (wpis #7), „Klej do styropianu i siatki" (wpis #39).
- **hero:** monter przykłada lampę elewacyjną do ściany z ociepleniem, w otworze widoczna tuleja montażowa, obok wiertarka i kartusza uszczelniacza, chłodne niebieskie światło późnego popołudnia, bez logo.
  - `hero_image_alt`: „Monter mocuje lampę elewacyjną do ściany z ociepleniem, w otworze widoczna tuleja montażowa przechodząca przez izolację"
- **uzasadnienie:** klaster D (zamocowania, 6,5k wyśw. GSC) ma w blogu trzy wpisy o doborze kołków i kotew, ale żadnego o najczęstszym realnym problemie prosumenta i instalatora: jak w ogóle mocować cokolwiek na ocieplonej ścianie. Temat wchodzi sezonowo (montaż oświetlenia i monitoringu przed krótkimi dniami, uszczelnienie przed deszczami), łączy trzy kategorie w jednym koszyku (kotwy, chemia, wiertła) i nie kanibalizuje istniejących wpisów, bo kąt jest inny: przegroda z izolacją, a nie rodzaj podłoża.

---

## 19. „Mróz i wilgoć w garażu: jak przechować chemię, akumulatory i narzędzia" (Problemy i porady, klaster C/A, SEZON)

- **Plik:** `90-mroz-i-wilgoc-w-garazu-przechowywanie-chemii-akumulatorow.json` · **slug/seo_url:** `mroz-i-wilgoc-w-garazu-przechowywanie-chemii-akumulatorow-narzedzi`
- **tytuł (H1):** Mróz i wilgoć w garażu: jak przechować chemię, akumulatory i narzędzia
- **kategoria:** Problemy i porady
- **klaster:** C (chemia budowlana) / A (Milwaukee) · **typ:** FAQ/troubleshooting · **intencja:** problemowa sezonowa -> komercyjna
- **planowana_data:** 2026-08-31
- **fraza główna:** czy pianka montażowa może zamarznąć
- **frazy poboczne:** przechowywanie akumulatorów zimą, czy farba może zamarznąć, jak przechowywać silikon, chemia budowlana w nieogrzewanym garażu, rdza na narzędziach w garażu
- **struktura (schemat „Problemy i porady"):**
  - *Lead 40-60 słów:* w nieogrzewanym garażu psują się trzy grupy rzeczy: chemia wodna, która po zamarznięciu traci właściwości, akumulatory litowo-jonowe, które w mrozie tracą pojemność i nie wolno ich wtedy ładować, oraz metalowe narzędzia, które rdzewieją od kondensacji. Wystarczy jedna zamykana szafka w cieple, żeby uratować większość.
  - H2: Co znosi mróz, a co nie - **tabela produkt, ryzyko, jak przechować** (farby i grunty wodne, akryle, kleje dyspersyjne, gładzie gotowe: zamarzają i po rozmrożeniu tracą spójność; silikony i masy MS: tolerancja zwykle szersza, ale karta rządzi; pianka PU: puszka nie znosi przegrzania ani długiego mrozu, przed pracą musi być ciepła; impregnaty i rozpuszczalnikowe: znoszą chłód, ale nie wilgoć w opakowaniu; zaprawy w workach: wilgoć zbryla je bezpowrotnie)
  - H2: Dlaczego to nie jest widoczne od razu (produkt po rozmrożeniu wygląda normalnie, a rozwarstwia się dopiero na ścianie; koszt to nie cena kartusza, tylko powtórzona robota)
  - H2: Akumulatory: trzy zasady (przechowywanie częściowo naładowanych w temperaturze dodatniej, brak ładowania zimnego akumulatora przed ogrzaniem, brak przechowywania rozładowanych do zera; zimą pojemność chwilowo spada i to normalne)
  - H2: Narzędzia i rdza (kondensacja na chłodnym metalu, sprzęt schowany mokry, olej lub spray konserwujący, silikażel i skrzynie systemowe, sprzęt odsunięty od betonowej posadzki)
  - H2: Jak urządzić kąt magazynowy w garażu - **lista** (półka zamknięta i ocieplona lub szafka w domu na chemię wrażliwą, paleta lub półka pod worki, oznaczenie dat ważności, rotacja: najstarsze na wierzch)
  - H2: Co zrobić z produktem, który przemarzł (kiedy próba ratowania ma sens, jak sprawdzić: wygląd, zapach, konsystencja po wymieszaniu, test na małej powierzchni; kiedy do utylizacji)
  - H2: Przed pierwszymi przymrozkami: lista kontrolna (przenieść chemię wodną, zabrać akumulatory, przejrzeć daty ważności, zakonserwować metal, sprawdzić szczelność opakowań)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Czy pianka montażowa może zamarznąć? · Czy farba po zamarznięciu nadaje się do użycia? · W jakiej temperaturze przechowywać akumulatory narzędzi? · Czy można ładować zimny akumulator? · Jak chronić narzędzia przed rdzą w garażu?
- **kafelki produktowe:** inline przy sekcji o piance `[PRODUKT: <pianka montażowa zimowa> | wersja do pracy przy niskich temperaturach, gdy standardowa już nie wiąże | Zimowa wersja]`; inline przy sekcji o narzędziach `[PRODUKT: <skrzynia lub organizer systemowy> | sprzęt suchy i odsunięty od zimnej posadzki | Przechowywanie]`; blok przed FAQ `[PRODUKTY: Przed pierwszymi przymrozkami || <preparat konserwujący lub spray penetrujący> | ochrona metalu przed rdzą || <akumulator zapasowy> | wymiana ogniwa, które nie dotrwa do wiosny || <skrzynia narzędziowa> | uporządkowany i suchy magazyn podręczny]`. Rank: `-Rank "spray konserwujący"`, `-Rank "skrzynia narzędziowa"`, `-Rank "pianka zimowa"`.
- **linkowanie wewn.:** kategorie **Chemia budowlana** + **Elektronarzędzia -> akumulatory i skrzynie PACKOUT**; w bok: „Chemia budowlana jesienią: w jakiej temperaturze można jeszcze malować, kleić i piankować" (wpis 75, publikacja 16.08), „Akumulatory Milwaukee M18: pojemność, ładowanie, kompatybilność" (wpis #13), „Milwaukee PACKOUT: system organizacji narzędzi" (wpis #45).
- **hero:** półka w garażu z ustawionymi kartuszami, puszkami i skrzynią narzędziową, na oknie garażu szron, chłodne niebieskie światło poranka, bez logo i czytelnych etykiet.
  - `hero_image_alt`: „Uporządkowana półka w garażu z chemią budowlaną i skrzynią narzędziową, na szybie widoczny szron"
- **uzasadnienie:** wpis domyka jesienną narrację partii („zrób prace, potem zabezpiecz sprzęt") i trafia w moment, gdy prognozy zaczynają mówić o pierwszych przymrozkach. Tabela „co znosi mróz, a co nie" jest unikalna: nikt w naszym profilu nie zebrał tego w jednym miejscu, a dla klienta to realna oszczędność. Naturalnie prowadzi do trzech koszyków (chemia zimowa, akumulatory, przechowywanie) i wzmacnia autorytet praktyczny sklepu działającego od 1979 roku.

---

## 20. „Lampa warsztatowa czy latarka akumulatorowa: co wybrać na krótsze dni" (Porównania, klaster B/A, SEZON)

- **Plik:** `91-lampa-warsztatowa-czy-latarka-akumulatorowa.json` · **slug/seo_url:** `lampa-warsztatowa-czy-latarka-akumulatorowa-co-wybrac`
- **tytuł (H1):** Lampa warsztatowa czy latarka akumulatorowa: co wybrać na krótsze dni
- **kategoria:** Porównania
- **klaster:** B (elektronarzędzia) / A (Milwaukee) · **typ:** POR · **intencja:** komercyjna (sezon krótszych dni, wrzesień i październik)
- **planowana_data:** 2026-09-01
- **fraza główna:** lampa warsztatowa akumulatorowa
- **frazy poboczne:** naświetlacz akumulatorowy na budowę, latarka warsztatowa led lumeny, ile lumenów do warsztatu, lampa robocza z akumulatorem m18, oświetlenie stanowiska pracy
- **struktura (schemat „Porównania"):**
  - *Lead 40-60 słów:* latarka oświetla punkt, na który patrzysz, a lampa i naświetlacz oświetlają całe stanowisko. Do pracy w rozdzielnicy, pod maską i w ciasnej przestrzeni wygrywa latarka lub lampka nagłowna, do pracy na budowie i w garażu naświetlacz na statywie o strumieniu liczonym w tysiącach lumenów.
  - H2: Lumeny, kąt świecenia i temperatura barwowa (co naprawdę oznacza deklarowany strumień, dlaczego kąt rozsyłu bywa ważniejszy niż lumeny, barwa 4000 do 5000 K przy pracy precyzyjnej, oddawanie barw przy malowaniu i doborze kolorów)
  - H2: **Tabela porównawcza** (latarka ręczna, lampka nagłowna, lampa warsztatowa kompaktowa, lampa obszarowa, naświetlacz na statywie, lampa magnetyczna do maski i rozdzielnicy: strumień, zasięg, czas pracy, mocowanie, odporność IP i na upadek, typowe zastosowanie)
  - H2: Kiedy latarka wystarcza, a kiedy szkodzi (praca dwiema rękami, cień od własnej dłoni, ostre kontrasty i zmęczenie wzroku)
  - H2: Zasilanie: akumulator systemowy, wbudowany czy sieć (jeden system akumulatorów do narzędzi i oświetlenia, tryb ekonomiczny i czas pracy, praca w deszczu i klasa IP, funkcja powerbanku)
  - H2: Mocowanie i praktyka (magnes, hak, statyw, uchwyt na kask, ustawienie światła z boku zamiast zza pleców, oświetlenie stanowiska a nie oczu współpracownika)
  - H2: Werdykt: co kupić najpierw - **mini-tabela** (warsztat samochodowy, instalacje i rozdzielnice, budowa i prace na zewnątrz, garaż i majsterkowanie, prace wykończeniowe i kontrola powierzchni)
  - H2: Oświetlenie a bezpieczeństwo pracy (praca po zmroku na zewnątrz, widoczność stanowiska, oświetlenie strefy ruchu, uzupełnienie odzieżą ostrzegawczą)
  - H2: Najczęściej zadawane pytania
- **FAQ:** Ile lumenów potrzeba do oświetlenia warsztatu? · Czym różni się lampa obszarowa od naświetlacza? · Czy warto kupić lampę na ten sam akumulator co narzędzia? · Jaka temperatura barwowa jest najlepsza do pracy? · Czy lampa akumulatorowa nadaje się na deszcz?
- **kafelki produktowe:** inline przy sekcji o pracy punktowej `[PRODUKT: <latarka lub lampa magnetyczna Milwaukee> | światło w ciasnej przestrzeni bez zajmowania drugiej ręki | Praca punktowa]`; inline przy sekcji o naświetlaczach `[PRODUKT: <naświetlacz lub lampa obszarowa akumulatorowa> | oświetlenie całego stanowiska przy pracy po zmroku | Całe stanowisko]`; blok przed FAQ `[PRODUKTY: Światło na krótsze dni || <lampa warsztatowa akumulatorowa> | podstawa oświetlenia stanowiska || <latarka robocza> | uzupełnienie do prac punktowych || <akumulator zapasowy> | światło nie kończy się razem z narzędziem]`. Rank: `-Rank "lampa"`, `-Rank "latarka"`, `-Rank "naświetlacz"`.
- **linkowanie wewn.:** kategoria **Elektronarzędzia -> oświetlenie warsztatowe i latarki** (+ akumulatory M12 i M18); w bok: „Przedłużacz bębnowy na budowę" (wpis 79, publikacja 20.08, link bezpieczny), „Milwaukee M12 czy M18: który system akumulatorowy wybrać" (wpis #01b), „Odzież robocza ostrzegawcza: klasy 1, 2, 3" (wpis #50).
- **hero:** naświetlacz akumulatorowy na statywie oświetla stanowisko z narzędziami w garażu o zmierzchu, w tle sylwetka fachowca przy pracy, chłodne niebieskie światło otoczenia kontra ciepły snop lampy, bez logo.
  - `hero_image_alt`: „Naświetlacz akumulatorowy na statywie oświetla stanowisko pracy w garażu o zmierzchu"
- **uzasadnienie:** wrzesień to moment, w którym prace zaczynają kończyć się po zmroku, a oświetlenie robocze przechodzi z kategorii „miło mieć" do „konieczne". Segment ma wysoką marżę i naturalny upsell do systemu akumulatorowego, którego jesteśmy autoryzowanym dystrybutorem. Wpis zamyka partię akcentem komercyjnym i domyka mikroklaster zasilania i oświetlenia razem z wpisem 79 (przedłużacze). Kategoria oświetlenia do potwierdzenia w drzewie przez sesję główną.

---

## Tabela zbiorcza - harmonogram partii (20 wpisów, drip codzienny 13.08-01.09.2026)

| Data (2026) | Plik | Kategoria | Tytuł | Klaster | Fraza główna |
|---|---|---|---|---|---|
| 08-13 | 72 | Porównania | Hydroizolacja fundamentów: dysperbit, masa KMB czy folia kubełkowa | C | hydroizolacja fundamentów |
| 08-14 | 73 | Krok po kroku | Przegląd dachu i rynien przed jesienią | C/H | przegląd dachu przed zimą |
| 08-15 | 74 | Porównania | Preparat na pleśń, grzyb i glony: który wybrać | C | preparat na pleśń |
| 08-16 | 75 | Poradnik | Chemia budowlana jesienią: w jakiej temperaturze malować, kleić i piankować | C/H | w jakiej temperaturze można malować na zewnątrz |
| 08-17 | 76 | Porównania | Silikon wysokotemperaturowy czy uszczelniacz kominkowy | C | silikon wysokotemperaturowy |
| 08-18 | 77 | Krok po kroku | Przegląd kominka przed sezonem grzewczym | C/H | przegląd kominka przed sezonem |
| 08-19 | 78 | Normy i BHP | Obuwie ochronne: co znaczy S1PS, S3S i S7L | G | oznaczenia obuwia ochronnego |
| 08-20 | 79 | Problemy i porady | Przedłużacz bębnowy na budowę: przekrój, IP44, rozwijanie bębna | B/H | jaki przedłużacz bębnowy |
| 08-21 | 80 | Normy i BHP | Odzież robocza na deszcz i chłód: EN 343, EN 342, EN 14058 | G | odzież robocza przeciwdeszczowa norma |
| 08-22 | 81 | Porównania | Odzież podgrzewana Milwaukee M12: kurtka, bluza czy kamizelka | G/A | odzież podgrzewana milwaukee |
| 08-23 | 82 | Poradnik | Dmuchawa do liści akumulatorowa: jak dobrać | B/H | dmuchawa do liści akumulatorowa |
| 08-24 | 83 | Krok po kroku | Drewno opałowe na sezon: cięcie, łupanie i sezonowanie | B/H | jak sezonować drewno opałowe |
| 08-25 | 84 | Problemy i porady | Wilgoć w piwnicy i garażu po lecie | C/F | wilgoć w piwnicy |
| 08-26 | 85 | Porównania | Nawiewniki okienne: ciśnieniowe, higrosterowane czy ręczne | F | nawiewniki okienne |
| 08-27 | 86 | Krok po kroku | Zazimowanie narzędzi ogrodowych: kosiarka, podkaszarka, pilarka | H/B | jak przygotować kosiarkę do zimy |
| 08-28 | 87 | Normy i BHP | Rękawice do pracy w chłodzie: norma EN 511 | G | rękawice ocieplane norma |
| 08-29 | 88 | Krok po kroku | Jak sprawdzić, czy przewód jest pod napięciem | B | jak sprawdzić czy przewód jest pod napięciem |
| 08-30 | 89 | Poradnik | Montaż na elewacji i w ociepleniu: lampa, kamera, uchwyt | D | jak zamocować coś na ociepleniu |
| 08-31 | 90 | Problemy i porady | Mróz i wilgoć w garażu: chemia, akumulatory, narzędzia | C/A | czy pianka montażowa może zamarznąć |
| 09-01 | 91 | Porównania | Lampa warsztatowa czy latarka akumulatorowa | B/A | lampa warsztatowa akumulatorowa |

### Rozkład kategorii i klastrów (kontrola dywersyfikacji)

- **Porównania (6):** 72, 74, 76, 81, 85, 91.
- **Krok po kroku (5):** 73, 77, 83, 86, 88 - wszystkie kandydują do schema HowTo.
- **Normy i BHP (3):** 78, 80, 87 - trzy różne obszary (obuwie, odzież, rękawice), każdy linkuje do huba ŚOI (57).
- **Poradnik (3):** 75, 82, 89.
- **Problemy i porady (3):** 79, 84, 90.
- **Klastry:** C=8 (72, 73, 74, 75, 76, 77, 84, 90 - odpowiada dominacji chemii w GSC), G=3 (78, 80, 87),
  B=6 (79, 82, 83, 88, 91 plus 86 jako B/H), F=2 (84 jako C/F, 85), D=1 (89), A=3 jako klaster wspierający
  (81, 90, 91), H=6 jako wymiar sezonowy nałożony na inne klastry.
- **Żadna kategoria blogowa nie występuje w dwa kolejne dni.** Bloki tematyczne celowo sąsiadują parami
  (76 i 77 kominek, 80 i 81 odzież, 82 i 83 oraz 86 sprzęt ogrodowy), żeby drugi wpis mógł linkować
  do pierwszego i budować mikroklaster.
- **Siatka wewnętrzna partii (linki tylko „wstecz"):** 72 <- 84 · 74 <- 84 · 75 <- 77, 90 · 76 <- 77 ·
  77 <- 83 · 79 <- 91 · 80 <- 81, 87 · 82 <- 86 · 83 <- 86 · 71 i 70 <- 85. Pozostałe linki idą do
  opublikowanych wpisów 01-71.
- **Pokrycie nowych kategorii bez ruchu:** 298 (76, 77), 300 (83, 86), 301 (82, 86), 303 (86), 304 (88),
  314 (79, 91), 131 (80, 81), 137 (80, 81), 259 (80, 81), 321 (81), 322 (80, 81), 329 (78).
  Kategorie 306, 307, 308, 318, 319, 323, 327, 328 (po 1-2 produkty) świadomie pominięte: nie mają masy
  na osobny wpis, do obsłużenia treścią kategorii, a nie blogiem.

---

## Kontrola kanibalizacji (co sprawdzono przed doborem tematów)

| Nowy wpis | Najbliższy istniejący | Dlaczego nie kanibalizuje |
|---|---|---|
| 72 hydroizolacja fundamentów | 52 folia w płynie (łazienka) | inne miejsce i inne materiały: grunt i woda napierająca kontra strefa mokra we wnętrzu |
| 73 dach i rynny | #30 uszczelniacz dekarski | tam dobór produktu, tu sezonowa procedura przeglądu |
| 74 preparaty na pleśń i glony | #29 jak usunąć pleśń ze ściany | tam procedura na jednej powierzchni, tu dobór środka do czterech różnych problemów |
| 75 temperatury stosowania | 54 pianka nie wiąże | tam jeden produkt i troubleshooting, tu tabela warunków dla całej chemii |
| 76 i 77 kominek | #22 silikon, akryl czy MS | inny materiał (masy ogniotrwałe), inna intencja i inna kategoria sklepu |
| 78 obuwie po zmianie normy | #41 obuwie S1, S2, S3 | tam podstawy klas, tu zmiana z 2022 i kody PL, PS, S6, S7 |
| 80 odzież na deszcz i chłód | #50 odzież ostrzegawcza | inna norma i inna funkcja: widoczność kontra ochrona przed deszczem i zimnem |
| 83 drewno opałowe | #21 jak wybrać pilarkę | tam dobór narzędzia, tu praca sezonowa i sezonowanie drewna |
| 84 wilgoć w piwnicy | 71 para na oknach | tam pomieszczenia mieszkalne i kondensacja na szybie, tu grunt, mur i piwnica |
| 85 nawiewniki | 70 uszczelnianie okien, #19 kratki | tam uszczelnianie i wywiew, tu urządzenie doprowadzające powietrze |
| 86 zazimowanie sprzętu | #36 podkaszarka czy kosiarka | tam wybór, tu konserwacja i przechowanie |
| 89 montaż w ociepleniu | #7 kołki, #31 kotwy | tam rodzaj podłoża, tu przegroda z warstwą izolacji |
| 91 oświetlenie | brak wpisu w temacie | nowy obszar produktowy w blogu |

---

## Do weryfikacji (frazy i parametry zapytań, realne wolumeny do pobrania w sesji głównej)

**Status danych:** MCP Ahrefs i DataForSEO niedostępne w kontekście subagenta. Wolumeny to estymaty na bazie
intencji, SERP i **danych GSC z eksportu 2026-06-11**. Przed przełączeniem wpisów na `gotowy` potwierdzić
wolumeny; jeśli fraza główna okaże się słaba, podmienić na potwierdzony wariant poboczny w tytule, H1 i meta
(reszta briefu zostaje bez zmian).

### Parametry do pobrania (Ahrefs Keywords Explorer, country `pl`; volume + KD + parent topic)

1. `hydroizolacja fundamentów`, `dysperbit`, `masa kmb`, `folia kubełkowa` (#72)
2. `przegląd dachu przed zimą`, `czyszczenie rynien`, `czym uszczelnić rynnę` (#73)
3. `preparat na pleśń`, `środek na grzyba na ścianie`, `preparat na glony elewacja`, `savo przeciw pleśni` (#74) - GSC pokazuje 10,8k wyśw. w tym klastrze, potwierdzić rozkład między pleśń a glony
4. `w jakiej temperaturze można malować na zewnątrz`, `temperatura stosowania pianki montażowej`, `punkt rosy malowanie` (#75)
5. `silikon wysokotemperaturowy`, `uszczelniacz kominkowy`, `czym uszczelnić drzwiczki kominka` (#76)
6. `przegląd kominka`, `wymiana sznura w kominku`, `czyszczenie szyby kominka` (#77)
7. `oznaczenia obuwia ochronnego`, `s1ps`, `s3s buty robocze`, `en iso 20345` (#78)
8. `przedłużacz bębnowy`, `jaki przedłużacz na budowę`, `przedłużacz się nagrzewa` (#79)
9. `odzież robocza przeciwdeszczowa`, `en 343`, `kurtka robocza wodoodporna` (#80)
10. `odzież podgrzewana milwaukee`, `kurtka podgrzewana m12`, `kamizelka podgrzewana` (#81) - **jeśli dominuje wariant „kurtka podgrzewana", przesunąć akcent H1 i meta**
11. `dmuchawa do liści akumulatorowa`, `jaka dmuchawa do liści`, `dmuchawa milwaukee` (#82)
12. `jak sezonować drewno opałowe`, `wilgotność drewna opałowego`, `pilarka akumulatorowa do drewna` (#83)
13. `wilgoć w piwnicy`, `mokra ściana w garażu`, `jak osuszyć piwnicę` (#84)
14. `nawiewniki okienne`, `nawiewnik higrosterowany`, `montaż nawiewnika` (#85)
15. `jak przygotować kosiarkę do zimy`, `zazimowanie narzędzi ogrodowych`, `ostrzenie noża kosiarki` (#86)
16. `rękawice ocieplane`, `en 511`, `rękawice zimowe robocze` (#87)
17. `jak sprawdzić czy przewód jest pod napięciem`, `detektor napięcia bezdotykowy`, `próbnik napięcia` (#88)
18. `jak zamocować coś na ociepleniu`, `montaż lampy na styropianie`, `kotwa dystansowa` (#89)
19. `czy pianka montażowa może zamarznąć`, `przechowywanie akumulatorów zimą`, `czy farba może zamarznąć` (#90)
20. `lampa warsztatowa akumulatorowa`, `naświetlacz akumulatorowy`, `latarka robocza` (#91)

- **Ahrefs Content Gap:** swiatnarzedzi.pl, centrumelektronarzedzi.pl, e-milw.pl na frazach sezonowych
  (kominek, odzież podgrzewana, dmuchawa, zazimowanie) i normowych (EN 343, EN 511, EN ISO 20345:2022).
  Konkurencja na Shoperze nie robi treści normowej ani sezonowej, to nasza przewaga do potwierdzenia danymi.
- **GSC (sklep.plasmet.pl):** po ~4 tygodniach od startu partii sprawdzić impresje wpisów 72-91; szczególnie
  74 (klaster pleśni ma 10,8k wyśw.), 78 i 80 (BHP: 14,3k wyśw. przy 4 klikach) oraz 85 (wentylacja:
  6,6k wyśw. przy pozycjach 39-61).

### Priorytet weryfikacji (decydują o tytule i H1)

1. **preparat na pleśń** (#74) - największy wolumen w partii wg GSC; potwierdzić, czy fraza główna nie
   powinna brzmieć „środek na pleśń" albo „savo przeciw pleśni", i czy nie rozbić wpisu na dwa (wnętrza
   kontra elewacja i kostka).
2. **odzież podgrzewana milwaukee** (#81) - potwierdzić wariant dominujący (kurtka, kamizelka, bluza)
   i domknąć parametry modeli M12 z kart produktów.
3. **oznaczenia obuwia ochronnego** (#78) - sprawdzić, czy większy wolumen ma „s3s" czy „s1ps", i czy
   fraza normowa nie przegrywa z prostym „buty robocze jakie wybrać".
4. **nawiewniki okienne** (#85) - potwierdzić, czy intencja jest zakupowa czy montażowa; jeśli montażowa,
   dołożyć sekcję krokową o montażu nadokiennym.
5. **hydroizolacja fundamentów** (#72) - potwierdzić proporcje między „dysperbit" a „masa bitumiczna"
   i domknąć nazwy produktów z oferty do tabeli.
6. **lampa warsztatowa akumulatorowa** (#91) - potwierdzić istnienie i id kategorii oświetlenia w drzewie
   sklepu przed publikacją; jeśli asortyment jest zbyt wąski, przenieść wpis na koniec kolejki partii E.

---

## Źródła weryfikacji faktów (E-E-A-T, dla blog-writera do domknięcia detali)

- **Hydroizolacja (#72):** podział na izolację lekką, średnią i ciężką wg obciążenia wodą (wilgoć gruntowa,
  woda niezalegająca, woda napierająca) to standard branżowy; masy rozpuszczalnikowe niszczą styropian
  i XPS, do ocieplenia fundamentu stosuje się masy bezrozpuszczalnikowe; folia kubełkowa to warstwa
  ochronna, nie izolacja. Zużycia i liczby warstw wyłącznie z kart produktów z oferty.
- **Uszczelniacze wysokotemperaturowe (#76, #77):** w ofercie (kategoria 298) są uszczelniacz kominkowy
  Baum odporny do 1500 stopni Celsjusza, 280 ml, oraz silikony wysokotemperaturowe Baum do 300 stopni
  (czerwony i czarny, 280 ml). Zakresy temperatur, sposób wygrzewania i dopuszczalny kontakt z płomieniem
  wyłącznie z kart produktów i etykiet, nie z pamięci. Obowiązek okresowego przeglądu i czyszczenia
  przewodów kominowych potwierdzić z aktualnymi przepisami przy pisaniu.
- **Obuwie ochronne (#78):** EN ISO 20345:2022 wprowadziła kody wkładek niemetalowych PL i PS (badanie
  gwoździem 4,5 mm i 3 mm) obok metalowej P, klasy wodoszczelne S6 i S7 oraz oznaczenia SC (ochrona noska)
  i LG (chwyt drabinowy). Pełną tabelę klas writer potwierdza z aktualnej treści normy lub materiałów
  producenta (Milwaukee FLEXTRED w ofercie ma m.in. S1PS i S3S) przed publikacją.
- **Odzież (#80):** EN 343 (ochrona przed deszczem, klasy 1-4 dla wodoszczelności i dla oporu pary wodnej
  Ret, oznaczenie X przy teście deszczem), EN 342 (zestawy chroniące przed zimnem, środowisko poniżej
  minus 5 stopni), EN 14058 (pojedyncze elementy odzieży do chłodu). Numery klas i progi writer potwierdza
  przed publikacją; obowiązki pracodawcy z Kodeksu pracy i rozporządzeń BHP cytować ostrożnie.
- **Rękawice (#87):** EN 511 podaje trzy cyfry: zimno konwekcyjne 0-4, zimno kontaktowe 0-4, przenikanie
  wody 0 lub 1; rękawica zimowa zwykle nosi równolegle oznaczenie EN 388. Potwierdzić przy pisaniu.
- **Odzież podgrzewana (#81):** wszystkie parametry (poziomy grzania, liczba stref, czasy pracy przy danym
  akumulatorze, wymagany adapter zasilania, wersje z akumulatorem i bez) wyłącznie z kart produktów
  Milwaukee w naszym asortymencie: kategorie 131 (kurtki, 41 poz.), 259 (bluzy, 15 poz.), 321 (kamizelki,
  14 poz.), 137 (koszulki, 54 poz.). Nie cytować liczb z pamięci.
- **Przedłużacze (#79):** obciążalność bębna zwiniętego i rozwiniętego to dane producenta z etykiety,
  różnica bywa kilkukrotna; IP44 oznacza ochronę przed ciałami stałymi powyżej 1 mm i bryzgami wody.
  Konkretne wartości prądu i mocy z kart produktów kategorii 314 (5 poz., przekroje 3x1,5 i 3x2,5 mm2,
  długości 20-50 m).
- **Akumulatory w chłodzie (#86, #90):** ogniwa litowo-jonowe w niskiej temperaturze mają chwilowo niższą
  dostępną pojemność, a ładowanie zimnego akumulatora jest szkodliwe; producenci podają dopuszczalne
  zakresy temperatur pracy, ładowania i przechowywania. Dokładne widełki wziąć z instrukcji Milwaukee,
  nie uogólniać.
- **Detektory napięcia (#88):** bezdotykowy detektor wykrywa pole elektryczne i daje wyniki fałszywie
  dodatnie (napięcie indukowane) oraz fałszywie ujemne (przewód ekranowany, w metalowej rurce, głęboko
  w ścianie), dlatego brak napięcia potwierdza się przyrządem dwubiegunowym. Kategorie pomiarowe CAT III
  i CAT IV z kart produktów kategorii 304 (m.in. detektor Milwaukee CAT IV 1000 V).
- **Drewno opałowe (#83):** wilgotność drewna do spalania powinna być poniżej 20 procent; typowe czasy
  sezonowania zależą od gatunku i sposobu ułożenia stosu. Wartości podać jako zakresy, nie jako pewniki.
- **Wentylacja i nawiewniki (#84, #85):** wymagania dotyczące strumienia powietrza wentylacyjnego
  w mieszkaniach reguluje PN-83/B-03430 ze zmianą Az3; nawiewnik jest warunkiem działania wentylacji
  grawitacyjnej przy szczelnej stolarce; zakaz zaklejania kratek i nawiewników ma bezpośredni związek
  z ryzykiem ciągu wstecznego przy urządzeniach spalających. Writer potwierdza brzmienie wymagań.
- **Chemia i temperatury (#75, #90):** minimalne temperatury stosowania są PRODUKTOWE i muszą pochodzić
  z kart technicznych konkretnych produktów z oferty (Den Braven, Bostik, Baum, Polifarb Kalisz).
  Zasada „temperatura podłoża co najmniej 3 stopnie powyżej punktu rosy" przy malowaniu to standard
  branżowy, ale i tak należy odesłać do karty wyrobu.
## ⚠ KOREKTA KALENDARZA (2026-08-11, zweryfikowane w plikach kolejki)

Nagłówek tej partii twierdzi, że kolejka C kończy się 12.08 - NIEPRAWDA. W kolejce jest 9 wpisów
`gotowy` (63-71) z datami **12.08-20.08**. Partia D zaczyna się więc **2026-08-21** (wpis 72),
kolejne dni +1; wpis 91 wypada 09.09. Daty per brief w tym pliku przesunąć o +8 dni przy zrzucie
do kolejki. Pilot Rankingów (R1/R2 z `_wzmocnienia-2026-08.md`): 10-11.09.

## ANEKS: rewizja danymi GSC na żywo (2026-08-11, okno 2026-07-14..2026-08-08)

> Krzyżówka fraz briefów z realnym korpusem zapytań (6009 fraz jawnych; Google anonimizuje ~70%,
> brak trafień NIE znaczy brak popytu - znaczy brak historii; tematy sezonowe zostają wg estymat).
> Zapytania poniżej wpisywać DOSŁOWNIE do FAQ/H2 wg zasady z `_format.md`.

### Brief 2 („Przegląd dachu i rynien przed jesienią: co sprawdzić i czym uszczelni)
- `uszczelniacz dekarski antracyt` - 133 wysw., poz. 10.9, 0 klik.
- `najlepszy uszczelniacz dekarski` - 24 wysw., poz. 25.6, 0 klik.
- `jaki uszczelniacz dekarski` - 12 wysw., poz. 40.0, 0 klik.
- `uszczelniacz dekarski biały` - 6 wysw., poz. 12.2, 0 klik.

### Brief 3 („Preparat na pleśń, grzyb i glony: który wybrać do ściany, drewna i el)
- `środek na grzyba na ścianie` - 6 wysw., poz. 2.0, 1 klik.

### Brief 5 („Silikon wysokotemperaturowy czy uszczelniacz kominkowy: 300 czy 1500 )
- `silikon 300 stopni` - 8 wysw., poz. 12.4, 0 klik.
- `silikon wysokotemperaturowy 300 stopni` - 7 wysw., poz. 13.6, 0 klik.
- `silikon do 300 stopni` - 5 wysw., poz. 13.0, 0 klik.

### Brief 8 („Przedłużacz bębnowy na budowę: przekrój żyły, IP44 i dlaczego trzeba )
- `przedłużacz bębnowy 25m` - 268 wysw., poz. 11.4, 1 klik.
- `przedłużacz na bębnie 25m` - 105 wysw., poz. 9.7, 0 klik.
- `przedluzacz bebnowy 25m` - 35 wysw., poz. 10.9, 0 klik.
- `przedłużacz bębnowy 25m 3x1 5` - 21 wysw., poz. 6.7, 0 klik.
- `przedluzacz na bebnie 25m` - 17 wysw., poz. 8.6, 0 klik.
- `przedłużacz na bębnie 25 m` - 12 wysw., poz. 10.9, 0 klik.
- `przedłużacz bębnowy 25 m` - 6 wysw., poz. 13.8, 0 klik.

### Brief 11 („Dmuchawa do liści akumulatorowa: jak dobrać" (Poradnik, klaster B/H, )
- `dmuchawa milwaukee m12` - 8 wysw., poz. 13.5, 0 klik.
- `milwaukee m12 vs m18` - 7 wysw., poz. 11.0, 0 klik.

### Brief 14 („Nawiewniki okienne: ciśnieniowe, higrosterowane czy ręczne" (Porównan)
- `nawiewniki okienne kraków` - 42 wysw., poz. 59.1, 0 klik.


---

## ⛔ BRAMKA ASORTYMENTOWA PARTII E (briefy 11-20, pliki 82-91) — wykonana 2026-08-17 PRZED pisaniem

> Nowy krok 0 pipeline'u (patrz `_format.md`): sprawdzamy pokrycie produktowe **zanim** ktokolwiek napisze
> tekst. Powód: w partii D osiem z dziesięciu gotowych wpisów dobierało produkty, których sklep nie ma,
> i trzeba było wycinać kafelki oraz przepisywać akapity po fakcie.
> Narzędzie: `python scripts/blog-asortyment-preflight.py --temat blog/queue/_preflight-partiaE.json`.
> Wynik: **OK 19 · RYZYKO 1 · BRAK 4** na 24 sprawdzone obszary produktowe.

### 🔴 Temat 85 „Nawiewniki okienne" — DO PRZEBUDOWY PRZED PISANIEM
W kategorii 278 są **dokładnie dwa** nawiewniki (Slimline 2000 i 4000) i **oba mają stan 0**.
Nawiewników higrosterowanych i ręcznych **nie mamy wcale**, więc brief („ciśnieniowe, higrosterowane
czy ręczne") porównuje dwie rzeczy, których nie sprzedajemy, i jedną, którą sprzedajemy w wersji
niedostępnej. Wszystkie anemostaty nawiewne (kat. 100) też mają stan 0.
**Popyt jest duży:** `nawiewniki okienne` ok. 452 wyśw. w GSC, `nawiewnik mechaniczny` 32 wyśw. (poz. 12,8).
**Dwie drogi, do wyboru przy pisaniu partii E:**
1. **Przebudowa kąta:** wpis zostaje przy frazie „nawiewniki okienne" (popyt), ale osią jest problem
   „szczelne okna kontra wentylacja grawitacyjna", a koszyk domykają produkty, które MAMY:
   wentylatory z higrostatem i czujnikiem wilgoci (4319, 3933, 4320), kratki i kanały. Nawiewnik opisany
   uczciwie jako wymagany element instalacji, bez kafelka i bez obietnicy dostępności.
2. **Zamiana tematu** na inny z banku, jeśli zarząd nie planuje dozamówienia.
**Sygnał zakupowy:** 452 wyświetlenia miesięcznie na kategorię z zerowym stanem to najtańsza sprzedaż,
jaką dziś tracimy. Dopisane do `docs/luki-asortymentowe-2026-08.md`.

### ⚠ Braki w dokupach (temat zostaje, kafelek nie)
- **83:** brak **oleju do prowadnicy i łańcucha** oraz **wilgotnościomierza do drewna**. Sam temat jest OK
  (pilarki 23 poz. ze stanem, siekiery 16), ale te dwie pozycje opisać bez kafelka. ⚠ Uwaga na wilgotność
  drewna poniżej 20%: bez wilgotnościomierza w ofercie nie sugerujemy, że go sprzedajemy.
- **88:** brak **mierników dwubiegunowych i multimetrów**. Za to **próbniki napięcia mamy mocno**
  (id 904 stan 88, 903 stan 49, 694 stan 24, 2178 VDE stan 20) plus szczypce i wkrętaki VDE. Zdanie
  „brak napięcia potwierdź przyrządem dwubiegunowym" zostaje jako zasada bezpieczeństwa, ale bez kafelka.
- **90:** RYZYKO. Jedyna pianka zimowa ze stanem to 5981 (24 szt.), ta sama co w partii D (wpis 75).
  Kafelek kruchy, sprawdzić stan w dniu publikacji.

### ✅ Tematy z potwierdzonym pokryciem (można pisać bez obaw)
82 dmuchawy (6 poz. ze stanem + akumulatory M18) · 83 pilarki i siekiery · 84 hydroizolacja wnętrz
i wentylacja piwnicy · 86 kosiarki, podkaszarki, smary i preparaty konserwujące · 87 rękawice ocieplane
(plus 108 poz. rękawic w kat. 45) · 88 detektory i próbniki napięcia · 89 kołki do ociepleń, kotwy
chemiczne (1362 szt.), wiertła do betonu (117 poz.) · 91 lampy, latarki i czołówki (26 poz. ze stanem).

### ⚠ Pułapka narzędzia
Dopasowanie idzie po **nazwach produktów**, więc produkt nazwany samą nazwą handlową nie wpadnie
w słowo rodzajowe (klasyczny przykład: „Boramon" zamiast „impregnat"). Przy każdym werdykcie BRAK
dopisz do listy słów nazwy handlowe i powtórz przebieg, zanim uznasz, że czegoś nie ma.
Drugi kierunek tego samego problemu: **wyszukiwarka sklepu też nie zna synonimów**, bo pole `booster`
(frazy alternatywne per produkt) jest puste w całym katalogu. To osobne zadanie, poza blogiem.
