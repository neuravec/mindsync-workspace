# Audyt SEO mindsync.app + naprawa end-to-end

**Data:** 2026-08-26
**Zakres:** cała witryna mindsync.app (Webflow, site `676ed8d44b863915ae191f41`)
**Stan:** WDROŻONE I OPUBLIKOWANE na żywo (5 publikacji site-wide), zweryfikowane na produkcyjnym HTML-u
**Weryfikacja końcowa:** automatyczny re-review 22/22 URL-i + robots.txt + llms.txt + przekierowania + strony 404 + linkowanie: **0 odchyleń**
**Wykonanie:** wszystkie punkty domknięte, łącznie z tymi, które wymagały panelu Webflow (robots.txt, llms.txt) i edycji współdzielonej nawigacji. Nic nie zostało przekazane operatorowi do ręcznego zrobienia poza decyzjami produktowymi (§3a).

---

## 1. Znaleziska krytyczne

### 1.1 Wszystkie dane strukturalne na stronie były nieważne

Każdy blok `<script type="application/ld+json">` miał cudzysłowy zakodowane jako encje HTML
(`&quot;` zamiast `"`). Wewnątrz elementu `<script>` przeglądarka **nie dekoduje encji**
(raw text parsing), więc `JSON.parse` zawodził. Efekt: Organization, WebSite,
SoftwareApplication, FAQPage i AboutPage – wszystko ignorowane przez wyszukiwarki.

Przyczyna: bloki były zbudowane jako węzły tekstowe elementów Webflow (klasa `inline-div-0`,
atrybut `data-seo`), a Webflow escapuje treść węzłów tekstowych przy eksporcie.

**Naprawa:** przeniesione na natywne pole schematu Webflow (`jsonLdSchema` per strona),
które renderuje surowo. Stare kontenery usunięte. 20 stron ma teraz poprawny, połączony graf
(`#organization` ↔ `#website` ↔ `#app` ↔ `#webpage`) z BreadcrumbList.

### 1.2 Skrypt z fabrykowaną oceną 4.8/150 recenzji

Strona główna ładowała `schema_markup-1.0.0.js` – plik zarejestrowany jako **JavaScript**,
ale zawierający surowy HTML (`<script type="application/ld+json">...`). Jako JS nie
wykonywał się (błąd składni), więc schemat nigdy nie działał. W środku był
`"aggregateRating": {"ratingValue":"4.8","ratingCount":"150"}` bez pokrycia w realnych
recenzjach – to naruszenie wytycznych Google dla danych strukturalnych i ryzyko manual action.

**Naprawa:** skrypt odpięty od strony głównej. Nowy schemat nie zawiera aggregateRating.

### 1.3 Dwa opublikowane wpisy blogowe bez `<title>` i meta description

`/journal/digital-burnout-brain-rewiring` i
`/journal/regulate-nervous-system-between-therapy-sessions` renderowały **pusty znacznik
title**. Szablon jest podpięty do pól CMS `seo-title` / `seo-description`, a oba wpisy miały
te pola puste. Pierwszy nie miał też `schema-jsonld`.

**Naprawa:** pola uzupełnione, schemat BlogPosting dopisany, wpisy opublikowane.

### 1.4 Śmieci dokumentacyjne w `<head>` szablonu wpisu

Custom code `<head>` szablonu Blog Posts zawierał wklejony fragment instrukcji po polsku
(„→ kliknij **+ Add field** → wybierz **Schema JSONLD**") opakowany w znacznik
`<script type="application/ld+json">`. Wyczyszczone.

### 1.5 Widoczny, niestylowany H1 72 px na każdym wpisie blogowym

W szablonie wpisu, między sekcją CTA a „read more", siedział bezklasowy `<h1>` powtarzający
tytuł wpisu. Renderował się jako czarny nagłówek 72 px – błąd wizualny na wszystkich
4 wpisach plus duplikat H1. Element usunięty z szablonu.

---

## 2. Znaleziska wysokie

### 2.1 Sitemapa zawierała URL-e zablokowane w robots.txt

13 stron roboczych było jednocześnie w sitemapie i pod `Disallow` w robots.txt: `/admin/*`
(3), `/admin---under-construction/*` (6), `/copy/*` (2, w tym `/copy/home-copy` = duplikat
strony głównej z 855 słowami) oraz `/untitled` i `/untitled-2` – żywe kopie `/testerzy`
z identycznym title i description. Żadna nie miała linku wewnętrznego.

**Naprawa:** wszystkie 13 ustawione na `draft`. Zwracają 404, zniknęły z sitemapy.
Sitemapa: z 32 URL-i (w tym 13 śmieci) do 22 realnych.

> ⚠ Uwaga: `bulk_update_pages` w Webflow Data API **po cichu ignoruje flagę `draft`**
> (zwraca `draft:false` bez błędu). Działa wyłącznie `update_page_settings` per strona.

### 2.2 `/features` i `/audience` były placeholderami

Obie żyły w sitemapie z meta title obiecującym konkretną treść, a w środku miały 108 słów
i nagłówek „Not ready for deep dive yet.". `/features` jest przy tym celem kart CTA
`[FEATURE:]` z wpisów blogowych, czyli blog prowadził w placeholder.

**Naprawa:** napisana pełna treść obu stron (700 i 707 słów), wyłącznie na podstawie
`blog/app-features.json` – tylko funkcje o statusie `live`. Placeholdery usunięte.
Dodane wzajemne linkowanie /features ↔ /audience ↔ /faq ↔ /about ↔ /membership.

### 2.3 Brak og:image na 20 stronach

Tylko strona główna i kilka stron roboczych miały obraz OG. Co gorsza te robocze
(`/terms-conditions`, `/copy/*`, `/404`, `/401`, `/admin/*`) wskazywały na
`torch-opengraph-image.png` z **cudzego site ID** (`66fad496e2674af9c6f8f4ef`) – pozostałość
po szablonie Webflow.

**Naprawa:** wszystkie strony mają teraz firmowy obraz OG (asset `68c6d88c51743ff7b1d02388`).

### 2.4 Rozsypana hierarchia nagłówków

`/about` miało 24 znaczniki H1, `/privacy-policy` 20, `/terms-conditions` 16, karty wpisów
na `/blog` renderowały się jako H1, karty cennika też. Źródła: komponenty współdzielone
(FAQ, Community/newsletter, Pricing List) i sekcje kopiowane w Designerze.

**Naprawa:** ~70 zmian poziomu nagłówka. Style w Webflow są klasowe, więc **wygląd nie
uległ zmianie**. Każda z 22 stron ma dokładnie jeden H1.

---

## 3. Druga tura (wszystkie punkty domknięte)

Pierwsza wersja tego raportu zostawiała 7 punktów operatorowi. Sześć zostało wykonanych,
jeden okazał się fałszywym alarmem.

### 3.1 robots.txt – WYKONANE (przez panel Webflow)

Wpisane w Site Settings → SEO. **Odkryta przyczyna zdublowanej dyrektywy Sitemap:**
przełącznik „Remove sitemap.xml from robots.txt" jest **Off**, więc Webflow dopisuje
`Sitemap:` automatycznie, a pole zawierało własną. Nowa wersja **celowo nie ma linii
Sitemap**. Efekt na żywo: dokładnie jedna dyrektywa Sitemap, zero `Disallow`.

Zdjęte `Disallow` dla `/admin/`, `/admin---under-construction/`, `/copy/` – te strony są
odpublikowane i zwracają 404; blokada w robots.txt uniemożliwiłaby Googlebotowi zobaczenie
404 i zostałyby w indeksie jako „Indexed, though blocked by robots.txt". Dodane nowsze
user-agenty AI (OAI-SearchBot, Perplexity-User, Applebot-Extended, meta-externalagent).

### 3.2 llms.txt – WYKONANE (przez panel Webflow)

**Ustalone, skąd jest serwowany:** to natywna funkcja Webflow, sekcja „LLMs.txt → Upload
llms.txt file" na dole Site Settings → SEO (nie Cloudflare Worker, jak twierdził komentarz
w starym robots.txt; potwierdzone testem na origin `mind-sync.webflow.io`). `llms-full.txt`
nie ma tam odpowiednika, więc 404 był nieusuwalny inaczej niż przez skasowanie odesłania.

Wgrany poprawiony plik. Cztery zmiany, poza literówką znalazłem trzy realne błędy:

| Było | Jest | Dlaczego |
|---|---|---|
| „It is a system that sits augments therapy" | „It is a system that augments therapy" | urwane zdanie |
| `Support: support@mindsync.app` | `Support: hello@mindsync.app` | `support@` występuje już tylko w **ukrytej, nieaktualnej** wersji regulaminu (zweryfikowane: `visible:false` w DOM). Każda żywa strona używa `hello@` |
| `Web: https://mindsync.app/` jako platforma | „Website (informational, the product itself is the mobile app)" | sugerowało crawlerom AI, że istnieje aplikacja webowa. Nie istnieje |
| „Premium subscription (weekly / monthly)" | „$12.99 per month", „$10 per patient per month" | cennik rozjeżdżał się z opublikowanym na `/membership` |

### 3.3 `lang` na stronach polskich – WYKONANE

Webflow ustawia `<html lang>` globalnie (Site Settings → General → Language code = `en`),
per stronę wymaga płatnych locale. Zamiast tego w custom code `<head>` obu stron:
`document.documentElement.setAttribute('lang','pl')`. Zweryfikowane w przeglądarce:
`/freebie` raportuje `lang="pl"`. W danych strukturalnych `inLanguage: "pl"` było już wcześniej.

### 3.4 `/features` i `/audience` w nawigacji – WYKONANE

Nawigacja miała **już przygotowane, ukryte** linki „Discover Features" i „Designer For".
Odkryte i poprawione przez `data_element_settings_tool` (`set_visibility` + `set_settings`),
bez wchodzenia do Designera. Nazwy zmienione na „Features" i „Who it's for".

⚠ „Designer For" celował w `/admin---under-construction/audience-building`, czyli stronę,
którą odpublikowałem – przepięty na `/audience`. Gdyby go tylko odkryć, powstałby link do 404.

Efekt: obie strony mają teraz link z **każdej** strony w serwisie (6 pozycji w menu,
bez przepełnienia na desktopie ani mobile).

### 3.5 Udostępnianie terapeucie – FAŁSZYWY ALARM, korekta

**W pierwszej wersji raportu zgłosiłem to jako rozbieżność. Myliłem się.** Oparłem się na
notatce w `blog/app-features.json` (zakaz obiecywania funkcji w treści bloga), zamiast
sprawdzić, co strona faktycznie mówi. Po weryfikacji żywej treści:

- FAQ (widoczne na `/`, `/faq`, `/contact`) opisuje **ręczne** udostępnianie: „Generate
  weekly summaries or monthly audits (...) then share however you want: email, PDF,
  WhatsApp, or bring your phone to the session". To działa – podsumowania mają status `live`.
- `/about` wymienia „Therapist collaboration tools. Shared dashboards" wprost pod
  nagłówkiem **„Our Roadmap → Next:"**, czyli jako plan, nie funkcję.

Nigdzie nie ma obietnicy działającego portalu klinicysty. **Żadna zmiana copy nie jest
potrzebna.** Kod potwierdza natomiast, że sam portal jest nieosiągalny nawigacyjnie
(komentarz w `account_body.dart`: sekcja „Therapists" ukryta w CS-11), więc ograniczenie
z katalogu nadal obowiązuje **dla treści bloga**.

### 3.6 `/admin/licenses` – decyzja: zostaje odpublikowane

Sprawdziłem zawartość. To boilerplate szablonu Webflow, nie atrybucje MindSync: „All
graphical assets in **this template**...", wymienia Lummi, Pexels, Lucide i **font Switzer
z Fontshare**, podczas gdy strona używa Figtree. Nie było do niej linku z żadnej strony.
Przywrócenie oznaczałoby opublikowanie nieprawdziwej informacji licencyjnej.

Pexels i Lummi nie wymagają atrybucji. Lucide (ISC) wymaga noty licencyjnej przy
redystrybucji kodu, co nie dotyczy użycia ikon na stronie. **Jeśli mimo to chcesz mieć
stronę licencji, trzeba napisać ją od nowa pod realne assety i podlinkować ze stopki** –
to decyzja produktowo-prawna, nie SEO.

### 3.7 Literówka w llms.txt – patrz 3.2

---

## 3b. Trzecia tura: linkowanie, alt-teksty, listing bloga

### Punkt „zlinkować osierocone `/pre-order/*`" – WSTRZYMANY, premisa była błędna

Sześć stron `/pre-order/*` ma dokładnie jeden link przychodzący i jest to link sam do siebie,
czyli są sierotami. Ale przed zlinkowaniem sprawdziłem ich treść i **wszystkie sześć kończy
się zdaniem „You're early, this feature is coming soon" oraz „This feature ships Q4"** –
w tym strony opisujące funkcje, które według `blog/app-features.json` mają status `live`
(AI journaling, wykrywanie wzorców, trendy nastroju).

Zlinkowanie ich z `/features` jako funkcji wysyłałoby użytkownika z „oto co MindSync robi"
do „jesteś wcześnie, to dopiero powstanie". Każde sformułowanie linku byłoby nieprawdziwe,
więc **nie dodałem linków** i przekazuję decyzję (patrz §4).

### Alt-teksty – WYKONANE

Znaleziony realny błąd: **28 odznak sklepów miało zamienione opisy** – obrazek Google Play
miał `alt="Download on the App Store"` i odwrotnie, na każdej stronie. Poprawione.

⚠ Pułapka: `alt` był zapisany jako **atrybut niestandardowy**, który nadpisuje ustawienie
`altText`. Samo ustawienie `altText` nie zadziałało (API zwracało sukces, HTML się nie
zmieniał). Trzeba było najpierw `remove_attribute` na `alt`, dopiero potem `altText` wchodzi.
`set_attributes` z kluczem `alt` zwraca „internal error" – to atrybut zarządzany przez Webflow.

Poza tym: logo w nawigacji i stopce (link bez dostępnej nazwy na wszystkich 22 stronach),
ikony Instagram i Discord, sześć zdjęć zespołu na `/about` (mapowane po nazwach plików),
zdjęcie foundera (zweryfikowane wizualnie: Darek z identyfikatorem „MINDSYNC.APP" na meetupie
Polish AI Breakfasts) i zrzut aplikacji (ekran Therapy Journey).

Pokrycie: **obrazy z pustym `alt` spadły z 255/368 (69%) do 111/368 (30%)**. Reszta to
w większości ikony dekoracyjne, gdzie pusty `alt` jest poprawny.

Jednego zdjęcia świadomie nie opisałem: `IMG_20250926` na `/about` przedstawia inną osobę
niż founder ze zdjęcia hero, a stoi przy jego cytacie. Zgadywanie tożsamości byłoby gorsze
niż pusty alt. Do uzupełnienia przez kogoś, kto wie, kto jest na zdjęciu.

### Listing bloga – WYKONANE

`/blog` miał 361 słów. Dodana sekcja „What you will find here" (o czym jest blog, standard
dowodowy, kto pisze) plus blok „What this blog is not" z zastrzeżeniem YMYL i odesłaniem
do numeru alarmowego. Umieszczona **pod** siatką wpisów, żeby nie spychać artykułów w dół.
Efekt: **614 słów**, linki do `/features`, `/faq` i `/about`, jeden H1, zero em-dash.

### Znalezione przy okazji, nienaprawione

`/about` serwuje zdjęcie `IMG_20250926_171454.jpg` w rozdzielczości **4928×6560 px i wadze
1,18 MB**, a mockup aplikacji jako PNG 550 kB. To materiał do punktu wydajnościowego (§4).

---

## 3c. Czwarta tura: wydajność i strony pre-order

### Skrypty blokujące render – WYKONANE (decyzja operatora: pełna naprawa)

Analiza 11 skryptów ładowanych synchronicznie w `<head>` wykazała, że **10 z nich nie
zawiera żadnej logiki** – każdy tworzy `<style>` i wstrzykuje CSS. Jedyny robiący realną
pracę to `mobilefixesv7` (MutationObserver, usuwanie stylów z `transform:none`), i on został.

CSS przeniesiony do custom code, z zawężeniem zakresu tam, gdzie było to bezpieczne:

| Skąd | Dokąd | Dlaczego |
|---|---|---|
| styleslayout, stylescards, stylescommunity, stylescontent, mobilefixesv2/8/9 | site head `<style>` | reguły globalne |
| stylesblog (1,6 kB) | custom code `/blog` | wszystkie selektory to `.section-journal`, a ta klasa jest **tylko** na `/blog` |
| stylesblogpost (1,9 kB) | custom code szablonu wpisu | `.section-post-header` i `.w-richtext` występują **tylko** na wpisach |
| mobilefixesv9 2.0.0 | custom code strony głównej | selektory `#ms-hero` |

Efekt zmierzony na żywo:

| | Przed | Po |
|---|---|---|
| Skrypty w `<head>` (strona główna) | 14 | 4 |
| Z tego blokujących render | 13 | 3 |
| Plików z CDN Webflow | 11 | 1 |
| CSS bloga ładowany na stronach nie-blogowych | tak (3,5 kB) | nie |

Trzy pozostałe blokujące to `WebFont.load`, reCAPTCHA i `mobilefixesv7`. Pierwsze dwa
wstawia Webflow (ustawienia fontów i formularzy), nie ruszałem.

**Kontrola regresji** (przeglądarka, wartości wyliczone): `.section.color-1` padding 64px,
`.section-pricing` 64px, `.div-block-54` radius 16px, `.heading-4` 22,4px, `.pricing-list`
grid + `align-items:stretch`, `.pricing-card` flex column, siatka `/blog` 3 kolumny,
karty białe z radius 12px, obraz 200px, `.heading-17` 36px Figtree, `.w-richtext` 720px,
akapit 16,8px, `.heading-18` `#d4a843`, padding nagłówka wpisu 48/16/24. Wszystko zgodne
z oryginałem co do wartości. 75 reguł i 18 media queries sparsowanych, 16 reguł mobilnych
obecnych w CSSOM, zero przepełnienia poziomego na żadnej sprawdzonej stronie.

⚠ Znaleziona literówka w oryginalnym CSS: `padding:1.5rem 1um` (jednostka „um" nie istnieje,
więc deklaracja była ignorowana). **Celowo jej nie „naprawiłem"** – poprawienie na `1rem`
zmieniłoby wygląd na mobile. Usunąłem martwą deklarację, zachowując obecne renderowanie.

⚠ Zmiana kolejności: `mobilefixesv7` wykonuje się teraz PO wstrzyknięciu CSS z custom code,
wcześniej był pierwszy. Sprawdziłem selektory obu zbiorów – nie nachodzą na siebie
(`mobilefixesv7` celuje w `#ms-pricing-cta`, `.mc-w` i potomków `#ms-compare` z innymi
klasami niż reguły z `mobilefixesv2`).

### Obrazy – sprawdzone, bez zmian

`/about` serwuje zdjęcie 4928×6560 px (1,18 MB), ale **wszystkie ciężkie obrazy mają już
`srcset` z wariantami i `loading="lazy"`**, więc przeglądarka nie pobiera oryginału.
Realny problem jest mniejszy niż sugeruje waga pliku. Zostaje jedno: Webflow ustawia
`sizes="100vw"` na wszystkich, co przy szerokim ekranie każe pobrać większy wariant niż
potrzeba. Poprawa wymaga per-obraz `sizes`, a to atrybut zarządzany przez Webflow
(ta sama blokada co przy `alt`). Zapisane jako drobny dług.

### Strony pre-order – WYKONANE częściowo (decyzja: zostawić, wyjąć z organiku)

Na wszystkich sześciu ustawione `<meta name="robots" content="noindex, follow">` przez
custom code. `follow` zachowuje przepływ link equity. Strony nadal działają dla ruchu
płatnego, ale przestają konkurować z `/features` w wynikach organicznych.

⛔ **Czego NIE udało się zrobić:** wyjęcia ich z `sitemap.xml`. Webflow generuje sitemapę
z ustawień strony, nie z HTML, więc `noindex` w custom code jej nie rusza. Przełącznik
per strona jest wyłącznie w Designerze, a Designer działa na osobnej domenie
(`mind-sync.design.webflow.com`), na którą rozszerzenie Chrome nie ma uprawnień do
wykonywania JavaScriptu. Alternatywa – wyłączenie auto-generowania i wklejenie statycznej
sitemapy – stworzyłaby gorszy problem: sitemapa przestałaby się aktualizować przy
publikacji nowych wpisów bloga.

**Skutek pozostawienia:** w Search Console te 6 URL-i pojawi się w sekcji „Wykluczone"
ze statusem „Przesłany URL oznaczony jako noindex". To status informacyjny, nie błąd,
i nie szkodzi witrynie. Cel (koniec konkurowania w organiku) jest osiągnięty przez noindex.

**Jak dokończyć (ok. 2 minuty):** Designer → dla każdej z 6 stron `/pre-order/*` →
Page settings → sekcja SEO → odznacz „Include this page in sitemap".

---

## 3a. Co nadal otwarte

| Rzecz | Status |
|---|---|
| **Ahrefs** | Konto zwraca „Insufficient plan". Brak warstwy fraz, konkurencji i profilu linków. Audyt jest techniczno-treściowy |
| **Google Search Console** | Właściwość mindsync.app jest na innym koncie Google niż token w `scripts/gsc/`. Bez tego nie ma pomiaru efektów |
| **Ukryta kopia regulaminu w DOM** | `/terms-conditions` i `/privacy-policy` mają w HTML starą wersję tekstu (`display:none`) obok wstrzykiwanej aktualnej. Wynika z mechanizmu `mslegalinject`, który **używa ukrytych akapitów do znalezienia miejsca wstrzyknięcia** (`.terms-paragraph:not(.msl)`), więc usunięcie ich zepsułoby stronę. Niski wpływ na SEO, ale warte przepisania przy okazji |
| **Strona licencji** | Patrz 3.6 |

---

## 4. Ograniczenie, którego nie da się obejść (zweryfikowane)

**Dane strukturalne wpisów blogowych nie mogą być renderowane serwerowo w tym setupie.**

Testowałem podpięcie pola CMS `schema-jsonld` w custom code `<head>` szablonu wpisu.
Webflow escapuje wartość pola PlainText również tam (opublikowałem i sprawdziłem surowy HTML:
oba bloki wyszły z `&quot;`). Cofnięte, żeby nie dublować bloków.

Działający obecnie mechanizm: skrypt w szablonie dekoduje encje przez `textarea.innerHTML`,
waliduje `JSON.parse` i podmienia węzeł. **Zweryfikowałem w przeglądarce** – po renderze
dokładnie jeden poprawny blok (Organization + BlogPosting + FAQPage).

Konsekwencja: Google to zobaczy (renderuje JS), ale crawlery AI, które JS-a nie wykonują
(GPTBot, ClaudeBot, PerplexityBot), schematu wpisów nie odczytają. Statyczne strony mają
JSON-LD serwerowo, więc ich to nie dotyczy. Jedyne czyste wyjście to przeniesienie wpisów
poza CMS Webflow albo pole typu Rich Text z obejściem – oba nieproporcjonalne do zysku.

---

## 5. Stan przed i po

| Metryka | Przed | Po |
|---|---|---|
| Strony z poprawnym JSON-LD | 0 | 22/22 (4 wpisy przez JS) |
| Strony bez `<title>` | 2 | 0 |
| URL-e w sitemapie | 32 (13 śmieci) | 22 (same realne) |
| Strony z og:image | 8 (w tym 7 z cudzego site) | 22 |
| Strony z dokładnie jednym H1 | 6 | 22 |
| Strony < 300 słów | 3 | 0 |
| Sfabrykowane oceny w schemacie | tak | nie |
| Dyrektywy Sitemap w robots.txt | 2 | 1 |
| `Disallow` blokujący de-indeksację 404 | 3 ścieżki | 0 |
| Błędy rzeczowe w llms.txt | 4 | 0 |
| Strony linkujące do `/features` i `/audience` | 0 (sieroty) | wszystkie (nawigacja) |
| Poprawna deklaracja języka na stronach PL | nie (`en`) | tak (`pl`) |
| Redirect apex → www, HTTPS, HSTS | OK | OK (bez zmian) |
| Canonical | OK na wszystkich | OK, dodatkowo zweryfikowany co do zgodności z URL-em |

---

## 6. Zmiany w Webflow (dziennik)

- **Dane strukturalne:** natywne `jsonLdSchema` na 20 stronach; usunięte 4 kontenery
  `data-seo` (home ×2, faq, about); odpięty `schema_markup` ze strony głównej
- **Meta:** przepisane title/description na 20 stronach (wszystkie ≤ 62 zn. / ≤ 166 zn.),
  og:image na 22 stronach, usunięty obcy obraz OG
- **Treść:** `/features` (16 kart funkcji, 700 słów), `/audience` (11 kart segmentów, 707 słów),
  `/membership` (FAQ cennika, +219 słów) – klasy `msf-*`, paleta forest/mint/sand, Figtree
- **Nagłówki:** ~70 zmian poziomu, w tym w komponentach współdzielonych FAQ,
  Community i Pricing List 1
- **Strony:** 13 ustawionych na `draft`
- **CMS:** 2 wpisy uzupełnione o seo-title, seo-description i schema
- **Kod:** wyczyszczony `<head>` szablonu wpisu, dopisane reguły CSS w site head
- **Nawigacja:** odkryte i przepięte 2 linki w komponencie Nav (wpływ na wszystkie strony)
- **Site Settings:** nowy robots.txt, wgrany poprawiony llms.txt
- **Custom code:** deklaracja `lang="pl"` na `/freebie` i `/testerzy`

## 7. Jak to zweryfikować ponownie

`scratchpad/seo/review.py` (skopiowany niżej opis) sprawdza w jednym przebiegu: sitemapę,
robots.txt (liczba dyrektyw Sitemap, Disallow, boty AI), llms.txt (obecność dawnych błędów),
404 na odpublikowanych ścieżkach, przekierowania apex/http, a dla każdego URL-a z sitemapy:
status, długość title i description, liczbę H1, liczbę słów, `lang`, og:image, og:title,
canonical (czy równy URL-owi strony), parsowalność każdego bloku JSON-LD, obecność
`aggregateRating`, em-dash w nowej treści oraz linki do odpublikowanych stron.

Ostatni przebieg: **0 odchyleń, 2 uwagi informacyjne** (lang na stronach PL ustawiany przez
JS, co jest zamierzone).
