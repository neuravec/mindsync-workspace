# Diagnoza: dlaczego Google indeksuje blog MindSync tak rzadko

**Data:** 2026-09-15
**Zakres:** `mindsync.app` (właściwość GSC `sc-domain:mindsync.app`), 15 wpisów `/journal/` opublikowanych dripem 25.08–14.09
**Źródła danych:** GSC URL Inspection API (40 URL-i), GSC Search Analytics, żywa `sitemap.xml`, nagłówki HTTP, żywy HTML
**Metoda:** każdy URL z sitemapy plus 5 URL-i spoza niej przepuszczony przez URL Inspection API i zestawiony z datą ostatniego crawlu oraz listą `referringUrls`

---

## Wniosek w jednym zdaniu

Blog nie ma problemu technicznego. Ma **trzy nakładające się problemy z odkrywaniem i budżetem crawlu**: sitemapa mówi Google, że strona `/blog` się nie zmienia (więc Google nie odwiedził jej od 21 lipca i nie widzi linków do nowych wpisów), budżet crawlu całej domeny to około **1 URL dziennie**, a spora część tego budżetu idzie na 404-ki i strony z `noindex`.

---

## 1. Co zostało wykluczone (to NIE jest przyczyna)

Zanim przejdziemy do przyczyn, warto odhaczyć rzeczy, które ludzie zwykle podejrzewają. Każda z nich została sprawdzona i jest zdrowa:

| Podejrzany | Stan | Dowód |
|---|---|---|
| `robots.txt` blokuje | OK | `User-agent: * / Allow: /`, sitemapa zadeklarowana, boty AI wpuszczone |
| `noindex` na wpisach | OK | brak `meta robots` w `<head>` wpisów |
| Canonical | OK | self-canonical na `www`, `googleCanonical == userCanonical` |
| Wydajność serwera | Bardzo dobra | TTFB ~75 ms, `CF-Cache-Status: HIT`, Cloudflare |
| Renderowanie JS | OK | `/blog` listuje wszystkie 17 wpisów w HTML server-side, nie przez JS |
| Linkowanie wewnętrzne w kodzie | OK | `/blog` linkuje do 17/17 wpisów, strona główna linkuje do `/blog` |
| `lastmod` wpisów | Uczciwy | per-wpis, zgodny z realną datą publikacji |
| Przekierowanie bez-www → www | OK | 301 działa |

Strona jest technicznie czysta. Dlatego problem trzeba szukać gdzie indziej.

---

## 2. Przyczyna główna: `/blog` ma zamrożony `lastmod`, więc Google go nie odwiedza

To jest sedno sprawy.

- W sitemapie `/blog` ma **`lastmod = 2026-08-26T20:42:09Z`** i ta data **nie zmieniła się ani razu**, mimo że drip publikował całą stronę codziennie od 04.09 do 14.09.
- Powód: Webflow ustawia `lastmod` strony statycznej na moment edycji **tej strony**, a nie na moment dodania nowego itemu CMS, który się na niej wyświetla. Listing zmienia się codziennie, a sitemapa codziennie powtarza, że jest z 26 sierpnia.
- Efekt: **`/blog` był ostatnio scrawlowany 2026-07-21**, czyli 8 tygodni temu.

Dowód, że to realnie psuje odkrywanie, jest w polu `referringUrls` z URL Inspection API. To lista adresów, z których Google **faktycznie zna** dany URL:

```
/journal/how-to-choose-a-therapist   -> ['https://www.mindsync.app/sitemap.xml']
/journal/how-to-do-therapy-homework  -> ['https://www.mindsync.app/sitemap.xml']
/journal/therapy-progress-1          -> ['https://www.mindsync.app/blog']
```

Czytamy to tak: **żaden nowy wpis nie został odkryty przez `/blog`.** Wszystkie, które Google zna, przyszły wyłącznie z sitemapy. Za to skasowany wpis `therapy-progress-1` Google zna właśnie z `/blog`, bo jego obraz tej strony pochodzi z lipca.

Innymi słowy: **Google ma lipcową migawkę listingu bloga.** Widzi na niej 4 wpisy, których już nie ma, i nie widzi 15, które doszły. Całe linkowanie wewnętrzne, które zbudowaliśmy, jest dla Google niewidoczne.

---

## 3. Przyczyna druga: budżet crawlu to około 1 URL dziennie

Rozkład dat ostatniego crawlu dla 40 sprawdzonych URL-i:

| Miesiąc | Liczba URL-i scrawlowanych |
|---|---|
| 2025-12 | 1 |
| 2026-04 | 1 |
| 2026-05 | 1 |
| 2026-07 | 3 |
| 2026-08 | 7 |
| 2026-09 (15 dni) | **14** |

Czternaście URL-i w piętnaście dni, na całą domenę. Dla porównania: sam blog potrzebowałby tyle tylko na nowe wpisy.

Co dostaje ten budżet, w kolejności świeżości:

```
2026-09-15  /copy/sign-in                  <- HTTP 404
2026-09-14  /contact
2026-09-14  /
2026-09-13  /pre-order/understand-...      <- noindex
2026-09-13  5 wpisów bloga                 <- jedyny dzień, w którym blog dostał uwagę
2026-09-08  /faq
...
2026-07-21  /blog
```

Strona główna jest odwiedzana prawie codziennie i to jest jedyna strona z realnym priorytetem. Reszta czeka tygodniami. **13 URL-i z sitemapy nie zostało scrawlowanych nigdy**, w tym 8 wpisów bloga.

Ten poziom budżetu to bezpośrednia funkcja autorytetu domeny. Ahrefs na obecnym planie nie zwraca DR ani profilu linków (`Insufficient plan`), ale tempo crawlu mówi samo za siebie: domena jest dla Google mało istotna, więc przydziela jej minimum.

---

## 4. Przyczyna trzecia: część tego minimalnego budżetu jest marnowana

### 4a. Sześć stron z `noindex` siedzi w sitemapie

Sprawdziłem wszystkie 35 URL-i z sitemapy pod kątem kodu HTTP i `noindex`. Wynik:

```
/pre-order/understand-behavioural-patterns  -> NOINDEX
/pre-order/tracking-therapy-effectiveness   -> NOINDEX
/pre-order/track-interventions              -> NOINDEX
/pre-order/mood-on-antidepressants          -> NOINDEX
/pre-order/wearable-ai-journal              -> NOINDEX
/pre-order/deep-emotional-analysis          -> NOINDEX
```

**17% sitemapy to strony, które jednocześnie mówią „zaindeksuj mnie" (obecność w sitemapie) i „nie indeksuj mnie" (meta robots).** To sprzeczny sygnał wysyłany kanałem, który akurat u nas jest jedynym działającym kanałem odkrywania. GSC raportuje na tej sitemapie **145 ostrzeżeń** i to jest najbardziej prawdopodobne główne źródło.

Dodatkowo `/freebie` jest w sitemapie, ma 0 linków wewnętrznych i nigdy nie został scrawlowany.

### 4b. Skasowane wpisy dalej są w indeksie i dalej są odwiedzane

Cztery stare wpisy demo zwracają **HTTP 404**, a mimo to mają w GSC status **`Submitted and indexed`**:

| URL | HTTP | Ostatni crawl |
|---|---|---|
| `/journal/therapy-tracking-2` | 404 | 2026-08-12 |
| `/journal/therapy-and-progress-4` | 404 | 2026-08-06 |
| `/journal/wellbeing-in-therapy-3` | 404 | 2026-08-05 |
| `/journal/therapy-progress-1` | 404 | 2026-07-10 |

Do tego dwie kolejne martwe ścieżki, które Google odwiedza zaskakująco świeżo:

- `/copy/sign-in` – 404, scrawlowany **dzisiaj o 02:40**
- `/admin---under-construction/about-building` – 404, scrawlowany 09.09

Czyli przy budżecie rzędu 1 URL/dzień Google poświęcił dzisiejszą wizytę na nieistniejącą stronę, a `/blog` czeka od lipca.

### 4c. Dwie strony `pre-order` z werdyktem „obejrzane i odrzucone"

`/pre-order/track-interventions` (crawl 2026-04-04) i `/pre-order/wearable-ai-journal` (crawl 2025-12-03) mają status **`Crawled – currently not indexed`**. To nie jest kwestia budżetu, tylko oceny: Google je zobaczył i uznał, że nie warto ich indeksować. Przy małej domenie takie strony ciążą na ocenie całości.

---

## 5. Aktualny bilans 15 wpisów dripu

| Status | Liczba | Uwaga |
|---|---|---|
| `Submitted and indexed` | 5 | wszystkie scrawlowane 13.09 między 14:00 a 14:29 |
| `Discovered – currently not indexed` | 2 | Google zna, jeszcze nie odwiedził |
| `URL is unknown to Google` | 8 | Google w ogóle nie wie, że istnieją |

Wszystkie 5 zaindeksowanych ma `referringUrls = 1`. Wszystkie „nieznane" mają `0`. Korelacja jest doskonała i potwierdza diagnozę z punktu 2.

Google pobrał sitemapę **13.09 o 13:51** i to jedno zdarzenie odpowiada za całą dotychczasową indeksację bloga. Przed nim blog praktycznie nie istniał.

---

## 6. Co z tym zrobić, w kolejności zwrotu z nakładu

### Priorytet 1 – odblokować odkrywanie (tanie, szybkie)

1. **Ręcznie zgłosić `/blog` do indeksacji w GSC** („Request indexing"). To jednorazowo odświeży lipcową migawkę listingu i da Google od razu 17 linków do wpisów. Największy pojedynczy zysk w całym zestawieniu.
2. **Dodać sekcję „Najnowsze z bloga" na stronie głównej** z 3 najnowszymi wpisami. Strona główna jest crawlowana prawie codziennie i jest jedyną stroną z realnym priorytetem. Wpisy znalazłyby się jeden skok od niej, zamiast wisieć wyłącznie na sitemapie.
3. Po każdej partii zgłaszać ręcznie 2–3 najważniejsze wpisy (limit GSC to ok. 10 dziennie).

### Priorytet 2 – posprzątać sygnały (tanie, jednorazowe)

4. **Usunąć 6 stron `pre-order` z sitemapy** albo zdjąć z nich `noindex`. Trzeba się zdecydować, bo teraz mówią dwie sprzeczne rzeczy naraz. To powinno zlikwidować większość ze 145 ostrzeżeń.
5. **Przekierować 301 martwe URL-e** na `/blog`: 4 wpisy demo, `/copy/sign-in`, `/admin---under-construction/about-building`. Przestaną zjadać budżet crawlu.
6. **Usunąć `/freebie` z sitemapy** albo podlinkować ją z nawigacji, jeśli ma istnieć.

### Priorytet 3 – zaadresować prawdziwe ograniczenie (drogie, długie)

7. Budżet crawlu rzędu 1 URL/dzień to funkcja autorytetu domeny, a nie ustawień. **Żadna poprawka techniczna tego nie ruszy.** Ruszą to linki zewnętrzne i realny ruch. Dopóki ich nie ma, sufit indeksacji zostanie niski, nawet przy idealnej sitemapie.
8. Dokończyć dług `LINK-LATER` z `blog/queue/_link-fixup.md`. Wpisy linkujące do siebie nawzajem dają Google więcej ścieżek niezależnych od `/blog`.

---

## 7. Kiedy mierzyć efekt

GSC ma ~3 dni opóźnienia. Dane kończą się 12.09, a indeksacja ruszyła 13.09, więc obecne zera na blogu opisują stan **sprzed** indeksacji. Pierwszy uczciwy odczyt: **około 20.09**, porównując okna tej samej długości.

Metryka do pilnowania to nie kliknięcia (na to za wcześnie), tylko **liczba wpisów ze statusem `Submitted and indexed`**: dziś 5 z 15.

---

# Wykonanie, 2026-09-15

## Zrobione przez API Webflow (ZASTAGEOWANE, czeka na publikację strony)

### A. Odmrożenie `lastmod` strony `/blog` – naprawa przyczyny głównej

Potwierdzone twardo: `GET page_metadata` dla `/blog` zwracał `lastUpdated: 2026-08-26T20:42:09.971Z`, czyli **co do milisekundy to samo**, co `<lastmod>` tej strony w sitemapie. To dowodzi, że sitemapa Webflow bierze dla strony statycznej jej własny `lastUpdated`, a nie moment publikacji strony. Dlatego codzienne publikacje dripu nic nie zmieniały.

Weryfikacja mechanizmu: zapis **identycznych** wartości SEO **nie** ruszył `lastUpdated` (Webflow wykrywa no-op). Dopiero realna zmiana treści pola go przestawiła.

Wykonano realną aktualizację meta description `/blog`, która przy okazji jest merytorycznie lepsza (stara wymieniała „nervous system regulation", temat jednego starego wpisu; nowa wymienia tematy, które blog faktycznie pokrywa):

- **było:** `Research-backed articles on therapy progress, nervous system regulation, and getting more out of every session. Written by the MindSync team.`
- **jest:** `Research-backed articles on therapy progress, coping skills, mood tracking, and getting more out of every session. Written by the MindSync team.`

Efekt: `lastUpdated` → `2026-09-15T10:45:58.427Z`. Po publikacji sitemapa poda dla `/blog` dzisiejszą datę zamiast 26 sierpnia.

> **Uwaga na przyszłość:** to nie jest trwałe. Przy następnych wpisach `lastmod` `/blog` znowu się zestarzeje, bo dodanie itemu CMS nie rusza strony statycznej. Trwałym rozwiązaniem jest sekcja na stronie głównej (niżej) plus ewentualne dodanie do `blog-publish.ps1` kroku „dotknij ustawień `/blog`" przy każdej partii. Copy tej meta description warto oddać do akceptu `brand-voice-manager`.

### B. Sekcja „Latest from the journal" na stronie głównej

Wstawiona przez `data_whtml_builder` (działa bezgłowo, bez sesji Designera) jako `<section>` **przed stopką**, za komponentem „Community" i przed `Section Image Divider`. Celowo nie dotykano hero, cennika ani social proof, bo `/` odpowiada za 96 ze 102 kliknięć całej domeny.

Zawartość: `<h2>Latest from the journal</h2>`, podtytuł, 3 karty linkujące do najnowszych wpisów i link „Read all articles" → `/blog`. Wszystkie linki **względne** (`/journal/...`), żeby nie generować 301 przez brak `www`.

Wybrane wpisy to nieprzypadkowo te, których Google nie zna: `sunday-scaries` (unknown), `racing-thoughts-at-night` (unknown), `how-to-do-therapy-homework` (discovered, nie odwiedzony).

Styl: własny prefiks klas `ms-journal-*`, **wyłącznie płaskie selektory** (builder nie obsługuje zagnieżdżonych). Zero kolizji z istniejącymi klasami.

> **Uwaga:** blok jest statyczny, więc przy kolejnych wpisach trzeba podmienić 3 linki. Docelowo powinien to być Collection List z CMS (do zrobienia w Designerze) albo krok w skrypcie dripu.

### C. Sitemapa: 6 stron `pre-order` wyłączonych

`bulk_update_pages_sitemap_status` → `includeInSitemap: false` dla wszystkich sześciu (`deep-emotional-analysis`, `wearable-ai-journal`, `mood-on-antidepressants`, `track-interventions`, `tracking-therapy-effectiveness`, `understand-behavioural-patterns`). Zachowany `noindex` – teraz sitemapa i meta robots mówią to samo. Sitemapa spadnie z 35 do 29 URL-i.

---

## Czego NIE da się zrobić przez API

### 301 redirecty – blokada planu

Sprawdzone empirycznie: `GET /v2/sites/{id}/redirects` zwraca

```
403  {"message":"This site is not associated with an Enterprise plan",
      "code":"not_enterprise_plan_site"}
```

Endpointy 301 są Enterprise-only. **Muszą być ustawione ręcznie** w Webflow: `Site Settings → Publishing → 301 redirects`. Do wklejenia (źródło → cel):

| Old Path | Redirect To Page |
|---|---|
| `/journal/therapy-progress-1` | `/blog` |
| `/journal/therapy-tracking-2` | `/blog` |
| `/journal/wellbeing-in-therapy-3` | `/blog` |
| `/journal/therapy-and-progress-4` | `/blog` |
| `/copy/sign-in` | `/` |
| `/admin---under-construction/about-building` | `/about` |

### „Request indexing" w GSC – tylko ręcznie

Indexing API Google oficjalnie obsługuje wyłącznie `JobPosting` i `BroadcastEvent`, więc dla zwykłych stron nie ma drogi programistycznej. Kroki:

1. <https://search.google.com/search-console> → właściwość **mindsync.app**
2. Pasek **„Inspect any URL"** u góry → wklej `https://www.mindsync.app/blog` → Enter
3. Poczekaj na wynik → **„Request indexing"** → potwierdź
4. Powtórz dla wpisów, które Google zna najsłabiej (limit ok. 10/dobę):
   `https://www.mindsync.app/journal/sunday-scaries`
   `https://www.mindsync.app/journal/racing-thoughts-at-night`
   `https://www.mindsync.app/journal/journaling-vs-voice-notes`
   `https://www.mindsync.app/journal/what-to-do-when-your-therapist-is-not-the-right-fit`
   `https://www.mindsync.app/journal/how-to-use-mindsync`

**Kolejność ma znaczenie:** najpierw opublikuj stronę (żeby `/blog` miał świeży `lastmod` i sekcję na `/`), dopiero potem zgłaszaj. Zgłoszenie starej wersji marnuje limit.

---

## Punkt 5: linki zewnętrzne – plan

Budżet crawlu ~1 URL/dzień to sufit, którego nie ruszy żadna z powyższych poprawek. Poniżej realne opcje, uszeregowane wg stosunku efektu do wysiłku.

### Szybkie i pewne (dni)

1. **Bing Webmaster Tools** – załóż i zgłoś sitemapę. Bing indeksuje dużo łagodniej niż Google, a zasila też ChatGPT Search. Można zaimportować właściwość prosto z GSC, więc to jest kwestia kilkunastu minut.
2. **Katalogi produktowe.** Product Hunt, AlternativeTo, SaaSHub, There's An AI For That, Futurepedia. Część linków jest `nofollow`, ale dają realny ruch odsyłający i, co ważniejsze tutaj, ścieżki crawlu z często odwiedzanych domen.
3. **Profile z linkiem**, które i tak powinny istnieć: LinkedIn firmowy, Crunchbase, GitHub org, App Store i Google Play (te ostatnie już linkują).

### Średni wysiłek, realny zwrot (tygodnie)

4. **Wejście do istniejących zestawień.** Wyszukaj „best therapy companion apps", „therapy journal app", „mental health apps 2026" i napisz do autorów. Skuteczność rośnie, gdy masz konkret, którego brakuje w zestawieniu, na przykład portal dla terapeuty.
5. **Serwisy eksperckie dla dziennikarzy** (Featured.com, Qwoted, następcy HARO). Dziennikarze piszący o zdrowiu psychicznym ciągle szukają cytatów. Stąd biorą się linki z domen, których nie kupisz.
6. **Kanał kliniczny.** Portal dla terapeutów daje naturalny powód, żeby gabinety i poradnie linkowały do MindSync jako narzędzia, które polecają pacjentom. To najbardziej niedoceniony zasób, jaki mamy.

### Największy potencjał, największy nakład (miesiące)

7. **Własne dane.** To jest jedyny naprawdę linkowalny zasób, jaki ten produkt może wytworzyć. Zagregowana, anonimowa analiza typu „przeanalizowaliśmy N tysięcy wpisów i tak wygląda tydzień między sesjami" jest dokładnie tym, co cytują dziennikarze i blogerzy. Wymaga przejścia przez `security-guardian` i `growth-analyst` pod kątem RODO i k-anonimowości, zanim cokolwiek opuści bazę.

### Czego nie robić

Kupowanie linków, katalogi masowe i wymiany linków. Przy domenie o tym profilu ryzyko manualnej kary przewyższa jakikolwiek zysk, a wychodzenie z niej kosztuje więcej niż zbudowanie kilku uczciwych linków.
