# Kanał publikacji: Webflow CMS (blog MindSync)

Odpowiednik `scripts/shoper-api/` z PLASMET (tamte skrypty zostały jako referencja w
`docs/blog-plasmet-reference/`). Tu żyje jedyny skrypt, który ZAPISUJE do żywego Webflow.

## Pliki

| Plik | Rola |
|---|---|
| `blog-publish.ps1` | Drip-publikator: kolejka `blog/queue/` → bramki → karty `[FEATURE:]` → upload hero (Assets API) → create/update item (idempotencja po slugu) → publish itemu → **kontrola odkrywania** (sekcja na `/`, odświeżenie lastmod `/blog`) → **publikacja całej strony** (sitemap.xml) → **zgłoszenie sitemapy w GSC** → logi. Od 2026-10-21 także **odświeżanie opublikowanych wpisów** (`-Republish`, `-BodyOnly`, `-KeepHero`) i **upload assetów z katalogu** (`-UploadAssets`), opis w sekcji niżej. **DryRun domyślnie TRUE.** |
| `.env` | `WEBFLOW_API_TOKEN` + `WEBFLOW_SITE_ID` + `WEBFLOW_COLLECTION_ID` (wzór: `.env.example`). ⚠ DO UZUPEŁNIENIA RĘCZNIE przez operatora – bez tokenu skrypt nie działa (MCP Webflow w sesji Claude ma własną autoryzację, ale Task Scheduler potrzebuje tokenu API). |
| `_drip-log.txt` / `_drip-error.txt` | 1 wiersz/przebieg + pełne zrzuty błędów (tryb nienadzorowany). |

## Cele w Webflow (potwierdzone przez MCP, 2026-08-25)

- Site: **Mind Sync** `676ed8d44b863915ae191f41` (mindsync.app + www)
- Kolekcja: **Blog Posts** `67cb62e9d0afa32a03eae3f1` (slug `journal` → wpisy pod `/journal/<slug>`; listing bloga to statyczna strona `/blog`)
- Pola dodane 2026-08-25: `seo-title`, `seo-description`, `hero-alt`, `schema-jsonld` (PlainText)
- Pole `category` (Option): `All` / `Therapy` / `MindSync Tips` – mapowanie nazwa→id w stałych skryptu

## Ograniczenie Webflow RichText (WAŻNE)

Pole `post-body` to RichText: **nie przepuszcza `div`, `style=""`, `<script>`**. Dozwolone:
`p, h2-h6, ul/ol/li, blockquote, figure/img, a, strong, em, code`. Dlatego:

- Karty `[FEATURE:]` renderują się do RichText-safe HTML (figure+img, akapit z linkiem);
  bogaty blok CTA pobrania apki (badge App Store/Google Play) siedzi RAZ w **szablonie wpisu**
  (Designer, strona `Blog Posts Template`), nie w treści.
- JSON-LD idzie do pola `schema-jsonld` (goły JSON), a szablon wpisu osadza je w `<head>`
  custom code jako `<script type="application/ld+json">` z polem CMS – jednorazowa robota
  w Designerze (właściciel: `seo-tech-lead`), patrz `blog/SCHEMA.md`.

## Publikacja całej strony po wpisie (sitemap.xml) – dodane 2026-09-03

Po **udanej** publikacji wpisu skrypt woła dodatkowo `POST /v2/sites/{site_id}/publish`
z `customDomains` obu domen (`www.mindsync.app`, `mindsync.app`). ID domen czyta na żywo
z `GET /v2/sites/{site_id}`; stałe w skrypcie to tylko awaryjny fallback.

**Dlaczego:** Webflow generuje `sitemap.xml` wyłącznie przy pełnej publikacji strony.
Publikacja pojedynczego itemu CMS stawia wpis na żywo, ale sitemapy nie odbudowuje.
Dowód z 2026-09-03: sitemapa miała 22 URL-e, wszystkie z `lastmod` 2026-08-26T20:42
(= `lastPublished` strony), i brakowało w niej 6 z 10 wpisów bloga wypuszczonych dripem
między 27.08 a 01.09, choć wszystkie itemy miały `includeInSitemap: true`. Po ręcznej
publikacji strony sitemapa urosła do 28 URL-i i objęła wszystkie 10 wpisów.

### ⚠ Skutek uboczny, który musisz znać przed włączeniem dripu

Pełna publikacja strony wypycha na żywo **także wszystko, co wisi niezapisane lub
nieopublikowane w Designerze**. Czyjeś pół skończone zmiany layoutu pojadą na produkcję
razem z wpisem, o 07:00, bez nadzoru. To nie jest ryzyko teoretyczne: 2026-09-03
w Designerze wisiały zmiany z 27.08 i poszły na żywo przy ręcznej publikacji (wykonanej
za jawną zgodą operatora). Jeśli w Designerze trwa robota, puść drip
z `-SkipSitePublish` i opublikuj stronę ręcznie, gdy Designer będzie czysty.

### Zachowanie kroku

| Sytuacja | Co robi skrypt |
|---|---|
| Wpis opublikowany (LIVE) | `POST /sites/{id}/publish`, wpis w logu: `... \| SITE-PUBLISH OK (domeny=...)` |
| Publikacja strony padła (429 / 5xx / timeout) | **exit 0**, wpis w logu `... \| SITE-PUBLISH BLAD: <powód>`. Item jest ważniejszy niż sitemapa, więc drip się nie wywraca; sitemapa dogoni się przy następnym przebiegu albo ręcznie |
| `-DryRun` (domyślnie) | tylko podgląd URL-a i body, zero requestów; log `SITE-PUBLISH DRY: pominiete wyslanie` |
| `-SkipSitePublish` | pomija krok, log `SITE-PUBLISH POMINIETO (-SkipSitePublish)`; sitemapa **nie** obejmie nowego wpisu do czasu ręcznej publikacji |
| Brak wpisów gotowych / wszystkie pominięte | strony **nie** publikuje (żadnej publikacji bez powodu raz dziennie) |

W trybie interaktywnym z `-All` strona publikuje się raz na cały przebieg, nie po każdym wpisie.

## Zgłoszenie sitemapy w Google Search Console (dodane 2026-09-25)

Po **udanej** publikacji całej strony skrypt czeka `-GscSubmitDelaySec` sekund (domyślnie 20,
Webflow w tym czasie przegenerowuje `sitemap.xml`) i woła
`python scripts/gsc/pull_gsc.py submit-sitemap`, czyli odpowiednik ręcznego
GSC -> Sitemaps -> Submit dla `https://www.mindsync.app/sitemap.xml`. Ścieżka do skryptu
liczona jest od `$PSScriptRoot`, więc działa też z Task Schedulera. Wyłącznik: `-SkipGscSubmit`.

**Po co:** pomiar z `seo-reports/2026-09-25-wyniki-bloga-i-kontrola-indeksacji.md`. Ręczny
resubmit 22.09 dał pobranie sitemapy sekundę później i indeksację 7 wpisów w około 4 h.
Od tamtej pory Google sam sitemapy nie pobrał (`lastDownloaded` 2026-09-22T09:34), a wpis
z 23.09 był `unknown to Google`.

**Wymaga jednorazowej reautoryzacji GSC** z pełnym zakresem `webmasters` (dotychczasowy token
ma `webmasters.readonly`, więc zgłoszenie kończy się 403). Raz, w przeglądarce operatora:

```powershell
python C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\gsc\pull_gsc.py auth
```

| Sytuacja | `_drip-log.txt` |
|---|---|
| zgłoszenie przeszło | `GSC-SUBMIT OK (lastDownloaded=...)` |
| token tylko readonly, brak pythona, HTTP != 2xx | `GSC-SUBMIT BLAD: <powód, do 300 znaków>` i **exit 0** |
| publikacja strony padła albo `-SkipSitePublish` | `GSC-SUBMIT POMINIETO: publikacja strony nieudana/pominieta` |
| `-DryRun` | `GSC-SUBMIT DRY: pominiete wyslanie` |
| `-SkipGscSubmit` | `GSC-SUBMIT POMINIETO (-SkipGscSubmit)` |
| nic nie poszło na żywo | krok się nie uruchamia, tylko komunikat w konsoli |

Kolejność kroków po wpisie: kontrola odkrywania (w tym odświeżenie `lastmod` `/blog`),
publikacja całej strony, zgłoszenie sitemapy w GSC.

## Kontrola odkrywania nowych wpisów: sekcja na `/` i lastmod `/blog` (dodane 2026-09-22)

Po **udanej** publikacji wpisu, **tuż przed** publikacją całej strony, skrypt sprawdza dwa
kanały, którymi Google znajduje nowe wpisy, i przy rozjeździe zostawia konkretną listę do
podmiany w konsoli oraz jedną linię w `_drip-log.txt`. Wyłącznik: `-SkipDiscoveryRefresh`
(symetryczny do `-SkipSitePublish`).

**Skąd to się wzięło:** pomiar GSC z 2026-09-22
(`seo-reports/2026-09-22-kontrola-indeksacji-po-naprawie.md`) pokazał, że od 15.09 nie
zaindeksował się ani jeden nowy wpis, a 5 najnowszych ma status `URL is unknown to Google`.
Sekcja „Latest from the journal" na stronie głównej wciąż pokazuje ręczny wybór z 15.09
i nie linkuje żadnego nowego wpisu, a `lastmod` strony `/blog` w sitemapie stoi na
`2026-09-15T10:45`, mimo pięciu publikacji po tej dacie.

### Czego ten krok NIE robi, i dlaczego (rozpoznanie 2026-09-22, wyłącznie GET-y)

| Czego chcieliśmy | Kanał | Werdykt |
|---|---|---|
| podmienić 3 karty na `/` na 3 najnowsze wpisy | `POST /v2/pages/{id}/dom` | **niewykonalne tym kanałem** |
| odświeżyć `lastUpdated` strony `/blog` | `PUT /v2/pages/{id}` z samym `title` | **działa od 2026-09-25** (werdykt z 22.09 był błędny, patrz niżej) |

Dowody, żeby nikt nie próbował tego drugi raz:

- Zapis treści statycznej (`Update Static Content`) działa **wyłącznie w lokalizacjach
  dodatkowych**. Dokumentacja Webflow: „API-based updates to page and component content are
  limited to secondary locales. Primary locale content for pages and components must be
  updated through the Webflow Designer." `GET /v2/sites/676ed8d44b863915ae191f41` zwraca
  `locales.secondary = []`, więc ten endpoint jest dla mindsync.app zamknięty.
- Nawet gdyby był otwarty, nie wystarczyłby. Lista typów węzłów przyjmowanych przez zapis
  (text, component-instance, select, text-input, submit-button, search-button) nie obejmuje
  obrazków, a samego linku karty `<a class="ms-journal-card">` `GET /v2/pages/{home}/dom`
  w ogóle nie zwraca. Widać tylko jego dzieci: obrazek, `div.ms-journal-card-title`
  i `p.ms-journal-card-desc`, czyli `href` nie ma jak zostać przepięty.
- **Rewizja 2026-09-25: pole neutralne jednak jest.** Zapis metadanych strony to
  `PUT /v2/pages/{id}` (`PATCH` zwraca `404 RouteNotFound`), body przyjmuje `title`, `slug`,
  `seo.title`, `seo.description` oraz `openGraph.title` / `openGraph.description` (plus flagi
  `*Copied`). Zapis identycznej wartości to no-op (potwierdzone 15.09), ale `title` to
  **wewnętrzna nazwa strony w Designerze** ("Blog"). Publiczny `<title>` na `/blog` pochodzi
  z `seo.title`, a `og:title` z `openGraph.title` (`titleCopied=false`), więc zmiana `title`
  nie dotyka niczego, co widzi Google albo udostępnienie. Test na żywo 2026-09-25:
  `PUT { "title": "Blog listing" }` przesunął `lastUpdated` z `2026-09-15T10:45:58.427Z`
  na `2026-09-25T11:32:16.542Z`, `seo.*` i `openGraph.*` bez zmian; powrót na "Blog" dał
  `2026-09-25T11:32:32.417Z`. Copy SEO `/blog` nadal nie jest churnowane.
- Że `lastmod` w sitemapie to dokładnie `lastUpdated` strony: sitemapa podaje dla `/blog`
  `2026-09-15T10:45:58.427Z`, a `GET /v2/pages/67ccb2a66069c30ddcc93974` zwraca
  `lastUpdated: 2026-09-15T10:45:58.427Z`. Dla `/` odpowiednio `2026-09-15T11:06:26.172Z`.

### Co robi

1. Bierze 3 najnowsze wpisy z `blog/published-log.json` (to, co faktycznie poszło na żywo),
   a dane karty (tytuł, alt, plik `hero-800x600`) dociąga z pliku kolejki po polu `plik`.
2. Czyta żywy HTML `https://www.mindsync.app/` (zwykły GET, bez tokenu) i wyciąga slugi
   z `<a class="ms-journal-card" href="/journal/...">`. To jedyny odczyt spoza Webflow API
   w całym skrypcie, bo API nie pokazuje linków kart.
3. Porównuje oba zestawy. **Zgadzają się, to nic nie wypisuje poza jedną linią OK** i nic
   nie wysyła. Rozjeżdżają się, to wypisuje gotową listę do podmiany w Designerze: `href`,
   tytuł wpisu, ścieżkę do pliku `hero-800x600`, `alt` i nazwę pliku kolejki.
4. Czyta `GET /v2/pages/67ccb2a66069c30ddcc93974` i porównuje `lastUpdated` (UTC) z datą
   ostatniej publikacji z `published-log.json` (czas lokalny, przeliczany na UTC). Gdy
   `lastUpdated` jest starszy, wysyła `PUT /v2/pages/67ccb2a66069c30ddcc93974` z **samym**
   polem `title`, przełączając nazwę między dwiema stałymi: "Blog" i "Blog listing" (zawsze
   na tę drugą niż obecna, żeby zapis nie był no-opem; nazwa spoza pary wraca na "Blog").
   `seo.*` i `openGraph.*` nigdy nie są wysyłane. W `-DryRun` tylko podgląd payloadu.
   Zmiana jest zastagowana i dopiero publikacja całej strony (krok następny) wypycha nowy
   `lastmod` do `sitemap.xml`; z `-SkipSitePublish` czeka na najbliższą publikację.

Krótkiego tytułu i opisu karty skrypt **nie wymyśla**: są krótsze niż tytuł i zajawka wpisu,
więc pisze je autor, nie publikator.

### Wpisy w logu

| Sytuacja | `_drip-log.txt` |
|---|---|
| sekcja zgadza się z 3 najnowszymi | `DISCOVERY OK: sekcja na Home aktualna (nic nie wyslano)` |
| sekcja odstaje | `DISCOVERY UWAGA: Home linkuje [a,b,c], powinno [x,y,z]` |
| nie ma kart `.ms-journal-card` w HTML | `DISCOVERY UWAGA: brak kart .ms-journal-card na stronie glownej` |
| `/blog` miał starszy `lastUpdated`, PUT przeszedł | `DISCOVERY OK: /blog lastUpdated odswiezony <stary> -> <nowy> (title 'Blog' -> 'Blog listing')` |
| to samo w `-DryRun` | `DISCOVERY DRY: /blog title '...' -> '...' (pominiete wyslanie)` |
| PUT przeszedł, ale data stoi | `DISCOVERY UWAGA: /blog PUT title bez zmiany lastUpdated (...)` |
| nieczytelna data w API albo w logu | `DISCOVERY UWAGA: /blog nieczytelne daty (...)` |
| strona nie odpowiada, 429, 5xx, timeout | `DISCOVERY BLAD: <powód, do 300 znaków>` i **exit 0** |
| `-SkipDiscoveryRefresh` | `DISCOVERY POMINIETO (-SkipDiscoveryRefresh)` |
| nic nie poszło na żywo w tym przebiegu | krok się nie uruchamia, tylko komunikat w konsoli |

Krok nigdy nie wywraca dripu: wpis jest już opublikowany i zalogowany, więc błąd kontroli
kończy się ostrzeżeniem i kodem wyjścia 0, dokładnie jak przy publikacji całej strony.
W `-DryRun` część o Home zachowuje się identycznie (to same odczyty, `PAYLOAD ZAPISU: BRAK`,
bo kanału zapisu nie ma), a część o `/blog` pokazuje payload `PUT` i niczego nie wysyła.

### Trwałe rozwiązanie: jedna robota w Designerze

Zamiana 3 statycznych kart w sekcji `.ms-journal-latest` na stronie Home
(`676ed8d44b863915ae191f82`) na **Collection List** z kolekcji Blog Posts, sortowanie po
dacie malejąco, limit 3, z polami `name`, `post-summary`, `thumbnail-image` i linkiem do
wpisu. Wtedy strona główna linkuje 3 najnowsze wpisy sama, bez niczyjego udziału, a ta
kontrola zamilknie, bo sekcja zacznie się zgadzać po każdej publikacji. Do czasu tej zmiany
podmiana kart jest ręczna, a skrypt tylko przypomina, co i na co podmienić.

`lastmod` `/blog` od 2026-09-25 odświeża drip sam (przełączenie nazwy strony, opis wyżej),
więc tu nic ręcznego nie zostaje.

### Uściślenie: Designer to nie jedyny kanał, ale drip i tak go nie ma

Blokada opisana wyżej dotyczy **publicznego Data API v2**, czyli tego, czym mówi ten skrypt.
Serwer MCP Webflow sięga po element-level API, którego w publicznej referencji REST nie ma,
i jego `data_element_tool` potrafi w lokalizacji **głównej** zmienić istniejący element:
`set_link` (href), `set_text` (tytuł, opis), `set_image_asset` (obrazek), `set_attributes`.
Tą drogą ta sekcja w ogóle powstała 15.09, bezgłowo, i widać to po stronie: karty to prawdziwe
elementy Webflow z prawdziwymi assetami (`GET /pages/{home}/dom` pokazuje je jako osobne węzły
z `assetId`), a klasy `ms-journal-*` siedzą w arkuszu strony, nie w `<style>` na stronie.
To **nie jest** HTML embed.

Praktycznie nic to jednak nie zmienia dla dripu: MCP żyje w sesji Claude z własną autoryzacją,
a zadanie w Task Schedulerze ma tylko token z `.env` i PowerShell, więc o 07:00 bez nadzoru
nikt tam nie sięgnie. Podmiana kart przez MCP jest możliwa **na żądanie, w sesji**, i wtedy
gotowa lista z tego kroku (3 slugi, tytuły, alty, ścieżki hero) jest dokładnie tym, czego
taka sesja potrzebuje na wejściu. Collection List zostaje rekomendacją, bo zdejmuje ten
problem na zawsze, zamiast wymagać pamiętania o nim po każdej partii.

## `blog/published-log.json`: zawijał się sam w sobie, naprawione 2026-09-22

Log publikacji przez kilka tygodni **zawijał się w matrioszkę**. `Save-Log` zapisywał go
jako `,@($entries) | ConvertTo-Json -Depth 8`, a w PowerShell 5.1 taki potok produkuje nie
tablicę, tylko obiekt `{ "value": [...], "Count": N }`. `Load-Log` wczytywał ten obiekt jako
pojedynczy element, dopisywał do niego nowy wpis i zapisywał całość jeszcze raz, więc każdy
przebieg dokładał kolejną warstwę. Po ośmiu warstwach `-Depth 8` zaczynał spłaszczać
najgłębsze wpisy do tekstu `"@{tytul=...; slug=...}"`, a jeszcze głębsze do
`"@{value=System.Object[]; Count=2}"`, czyli do niczego.

Stan zastany 22.09: na najwyższym poziomie pliku **jeden obiekt bez ani jednego sluga**,
w środku 5 odzyskiwalnych wpisów (4 jako struktura, 1 jako tekst), a 15 starszych zniknęło
w spłaszczonym `System.Object[]`. Skutek praktyczny: `Already-Published` nie widział żadnego
opublikowanego sluga, więc **idempotencja po slugu nie działała w ogóle**. Przed ponowną
publikacją chronił wyłącznie status `opublikowany` w pliku kolejki.

Co zostało zrobione:

- `Save-Log` używa teraz `ConvertTo-Json -InputObject @($entries) -Depth 8`, co serializuje
  tablicę jako tablicę, także jednoelementową. Sprawdzone odczytem pliku po zapisie i po
  dwóch kolejnych cyklach `Load-Log` plus `Save-Log`, nie samym rozumowaniem.
  **Nie wracaj do wersji z potokiem i przecinkiem**, w skrypcie stoi przy tym ostrzeżenie.
- `Load-Log` przepuszcza plik przez `Expand-LogEntries`, więc czyta tak samo płaską tablicę
  i starą matrioszkę. Nikt ze starym plikiem nie musi niczego migrować.
- Sam plik został jednorazowo spłaszczony i uzupełniony do 20 wpisów, chronologicznie, bez
  duplikatów. Kopia sprzed naprawy leży obok jako
  `blog/published-log.2026-09-22-przed-naprawa.json` i nie została skasowana.

Odzyskanie historii nie wymagało zgadywania. Datę publikacji i `item_id` każdego wpisu ma
`scripts/webflow/_drip-log.txt` (linie `OK opublikowano`), a tytuł, slug, permalink i nazwę
pliku ma `blog/queue/*.json` ze statusem `opublikowany`. Dla wpisów, które przeżyły jako
struktura, `data` z obu źródeł zgadza się co do sekundy, co potwierdza, że reszta jest
odtworzeniem, a nie szacunkiem. Wpisy odtworzone mają dodatkowe pole `odtworzony` z opisem
źródła, żeby za pół roku nikt nie zgadywał, skąd się wzięły. Wpisów nie do odtworzenia było
zero.

W logu nie ma i nie będzie `digital-burnout-brain-rewiring` ani
`regulate-nervous-system-between-therapy-sessions`. To dwa wpisy zrobione ręcznie przed
uruchomieniem pipeline'u: nie mają plików w kolejce, nie przeszły przez drip i nie należą
do jego logu publikacji.

## Odświeżanie opublikowanych wpisów i upload assetów (dodane 2026-10-21)

Zwykły tryb nie wyśle drugi raz wpisu, który już wyszedł: pilnuje tego `published-log.json`
i status `opublikowany`. Do przepisanego wpisu i do podmiany zrzutów aplikacji są osobne
przełączniki. Wszystkie mają **DryRun domyślnie**, a DryRun robi wyłącznie odczyty (GET).

### Składnia

```powershell
$s = 'C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\webflow\blog-publish.ps1'

# podgląd: jeden wpis, tylko post-body
& $s -Republish -Plik 2026-08-28_how-to-know-if-therapy-is-working.json -BodyOnly
# podgląd: wszystkie opublikowane, tylko post-body (masowa podmiana zrzutów)
& $s -Republish -All -BodyOnly
# podgląd: pełne odświeżenie przepisanego wpisu (treść, meta, schema; hero tylko gdy plik się zmienił)
& $s -Republish -Plik 2026-08-25_how-to-use-mindsync.json
# to samo, ale main-image i thumbnail-image zostają nietknięte
& $s -Republish -Plik 2026-08-25_how-to-use-mindsync.json -KeepHero
# podgląd: lista plików *.webp do wgrania, z MD5
& $s -UploadAssets blog\images\app-screenshots-v2

# LIVE: ta sama linia z -DryRun:$false, wyłącznie za zgodą operatora, w otwartej sesji PS
& $s -Republish -All -BodyOnly -DryRun:$false
```

| Przełącznik | Co robi |
|---|---|
| `-Republish` + `-Plik <plik>` albo `-All` | odświeża wpis o statusie `opublikowany`: PATCH istniejącego itemu, potem publish tego jednego itemu. Pomija **wyłącznie** bramkę Already-Published |
| `-BodyOnly` (tylko z `-Republish`) | PATCH zawiera **tylko** `fieldData.post-body` (bez `isDraft`, `isArchived`, meta, hero) |
| `-KeepHero` (tylko z `-Republish`) | pełny PATCH bez pól `main-image` i `thumbnail-image`, czyli obrazki zostają, jakie są |
| `-ItemPauseSec <s>` (domyślnie 3) | przerwa między wpisami. W LIVE `-BodyOnly` to 4 wywołania API na wpis, razem około 40 na minutę przy limicie Webflow 60 |
| `-UploadAssets <katalog>` | wgrywa wszystkie `*.webp` z katalogu przez Assets API i zapisuje mapę nazwa pliku do URL-a CDN w `<katalog>\_webflow-urls.json` |

Złe kombinacje (`-BodyOnly` albo `-KeepHero` bez `-Republish`, `-Republish` bez `-Plik`/`-All`
albo z obydwoma naraz, `-Republish` z `-DripOne`, `-UploadAssets` z czymkolwiek z tej listy)
kończą się komunikatem `BLAD PARAMETROW` i kodem 2, zanim padnie jakiekolwiek wywołanie API.
Bez nowych przełączników skrypt działa dokładnie jak wcześniej (porównane wyjście DryRun
trybów `-Plik`, `-All` i `-DripOne` przed zmianą i po niej: zero różnic).

### Czego pilnuje `-Republish`

- **Tylko wpisy `opublikowany`.** Wpis o innym statusie podany przez `-Plik` jest pomijany
  z komunikatem; przy `-All` inne statusy w ogóle nie są rozpatrywane.
- **Item musi istnieć w Webflow.** GET po `item_id` z kolejki (albo z logu) z kontrolą sluga,
  a bez `item_id` GET po slugu. Brak itemu oznacza pominięcie: ten tryb **nigdy nie tworzy**
  nowego itemu.
- **Item musi być już opublikowany i aktywny:** puste `lastPublished`, `isDraft` albo
  `isArchived` oznacza pominięcie. Publikacja takiego rekordu wskrzesiłaby coś, co ktoś
  świadomie trzyma poza stroną (wpadka z 22.09 z wpisami demo).
- **Bramki jak przy publikacji:** surowe `[LINK:]`, długi myślnik, render kart. Hero i zajawka
  blokują w trybie pełnym, a w `-BodyOnly` tylko informują, bo tych pól się wtedy nie wysyła.
- **Render identyczny jak przy publikacji:** obie ścieżki wołają tę samą funkcję
  (`Invoke-QueueItemGates`: LINK-LATER, potem karty `[FEATURE:]` z `blog/app-features.json`).
- **Zero efektów ubocznych poza itemem:** bez publikacji całej strony, bez kontroli odkrywania,
  bez zgłoszenia w GSC. Plik kolejki nie jest przepisywany, status zostaje `opublikowany`.
- **Publish dostaje zawsze jeden `itemId`**, nigdy listę z `GET /items`.
- **Seria w LIVE zatrzymuje się na pierwszym błędzie**, żeby nie powtarzać go na kolejnych
  wpisach. Gdy PATCH przeszedł, a publish padł, komunikat mówi wprost, że zmiana czeka
  zastagowana w CMS i nie jest jeszcze na żywo.

### Co pokazuje DryRun

Dla każdego wpisu: liczbę `<img>` w `tresc_html`, liczbę kart i liczbę obrazków po renderze,
potem porównanie post-body z itemem w Webflow w czterech warstwach:

| Warstwa | Zapis w konsoli |
|---|---|
| obrazki | lista wyrównana jak w diffie: `=` bez zmian, `~` stary URL, a pod nim nowy, `+` doszedł, `-` zniknął |
| linki z `[LINK-LATER:]` | linki, których na żywo brak, bo cel wyszedł później. PATCH je doda i to jest oczekiwane |
| inne linki | `UWAGA linki`: link jest na żywo, a w renderze go nie ma, albo odwrotnie |
| struktura | `UWAGA struktura HTML`: inna sekwencja tagów (bez `a`, `img`, `figure`), np. `h3` zamiast `h2` przy tym samym tekście |
| tekst | `UWAGA tekst`: pierwszy różniący się fragment, na żywo i po renderze |

W trybie pełnym dochodzi lista pól, które PATCH zmieni (stara i nowa wartość), oraz decyzja
o `main-image` i `thumbnail-image`. Na końcu przebiegu jest podsumowanie z listami plików,
a w `_drip-log.txt` jedna linia `REPUBLISH ... DRY-RUN: ...`.

**Różnica poza obrazkami** (tekst, struktura albo linki spoza LINK-LATER) oznacza, że PATCH
zmieni na żywo coś więcej niż zrzuty. Przyczyny są dwie: ktoś poprawił wpis w CMS poza kolejką
(PATCH nadpisze tę poprawkę) albo ktoś poprawił plik kolejki po publikacji. Każdy taki wpis
trzeba wyjaśnić przed LIVE. Ostrzeżenie `niepublikowane zmiany w CMS` (lastUpdated późniejsze
niż lastPublished) znaczy, że publish itemu wypchnie na żywo także cudze zapisane zmiany.

**Dlaczego obrazki porównujemy po nazwie pliku, a nie po URL-u.** Webflow przy zapisie RichText
kopiuje każdy obrazek do bucketu CMS i zmienia adres na
`.../676ed8d44b863915ae191fa7/<24 znaki hex>_<nazwa pliku źródła>` (sprawdzone 21.10: na żywo
`.../6a8ddde2cebc26512efd660a_6a8ddddcbbb8ef48bf3639c2_app-ios-4.webp`, w kolejce
`.../676ed8d44b863915ae191f41/6a8ddddcbbb8ef48bf3639c2_app-ios-4.webp`). Poza tym prefiksem
znacznik zapisuje się dosłownie, dlatego porównanie struktury ma sens. Skutek uboczny: każdy
PATCH post-body robi nowe kopie wszystkich obrazków wpisu, także niezmienionych. Assetów
przybywa, nic nie znika.

### Hero w trybie pełnym

Plik hero i miniatury wgrywa się ponownie **tylko wtedy, gdy się zmienił**. Poprzedni MD5
pochodzi z `published-log.json` (pola `hero_md5` i `hero_url`, o ile `hero_url` zgadza się
z obecnym adresem w Webflow), a w przeciwnym razie z pliku pobranego z CDN. CDN serwuje
oryginał bajt w bajt, także kopie w buckecie CMS (sprawdzone 21.10 na hero 1600x900, 800x600
i zrzucie ekranu). Zgodny MD5 oznacza, że pole nie idzie w PATCH i Webflow trzyma obecny
obrazek. Wyjątek: ten sam plik z nowym `hero_image_alt` jest wgrywany jeszcze raz, bo alt siedzi
w polu obrazka. Nieudane pobranie z CDN kończy się uploadem dla pewności. `-KeepHero` wyłącza
całą tę logikę i oba pola zostają bez zmian, nawet przy innym alcie (DryRun to zaznacza).

### Log

`published-log.json`: aktualizowany jest **istniejący** wpis o tym slugu, nowy nie powstaje.
Dochodzą pola `odswiezono` (data), `odswiezono_tryb` (`body-only` albo `pelny`),
`odswiezono_ok`, `odswiezen` (licznik), a po trybie pełnym także `hero_md5`, `hero_url`,
`thumb_md5`, `thumb_url` i bieżący `tytul`. **Pole `data` zostaje bez zmian:** to data pierwszej
publikacji i czyta ją kontrola odkrywania (trzy najnowsze wpisy na stronie głównej, lastmod
`/blog`), więc stary wpis z nową datą udawałby najnowszy. Gdy sluga w logu nie ma, wpis jest
dopisywany raz, z datą `createdOn` itemu z Webflow i polem `odtworzony`. Zapis idzie przez
`Save-Log` (`-InputObject`), więc matrioszka opisana niżej nie wraca. W `_drip-log.txt`
każdy wpis w LIVE zostawia linię `OK odswiezono (republish ..., obrazki zmienione=N, ...)`.

### Upload assetów (`-UploadAssets`)

Wgrywa wszystkie `*.webp` z katalogu tą samą funkcją co hero (`Publish-WfAsset`). Katalog
można podać bezwzględnie albo względem repo (`blog\images\...`). W LIVE mapa
`<katalog>\_webflow-urls.json` zapisuje się po każdym pliku, więc przerwany przebieg nie gubi
URL-i już wgranych. Ma postać `{ "map": { "<plik>": "<URL CDN>" }, "pliki": [ { plik, md5, url,
bajty, wgrano } ] }`. Plik z tym samym MD5 co w mapie nie jest wgrywany drugi raz. DryRun
wypisuje tylko nazwy, rozmiary i MD5, nie woła API i nie zapisuje mapy. Nic nie jest usuwane.

### Podmiana zrzutów aplikacji krok po kroku

1. `-UploadAssets <katalog z nowymi zrzutami>` w DryRun, potem LIVE za zgodą operatora.
   Wynik: `_webflow-urls.json` z URL-ami CDN.
2. Podmiana URL-i w plikach źródłowych: pole `screenshot` w `blog/app-features.json` (karty)
   oraz `<img src>` w `tresc_html` pięciu wpisów z obrazkami inline (`how-to-use-mindsync`,
   `how-to-know-if-therapy-is-working`, `which-coping-skills-actually-work`,
   `why-mood-tracking-stops-working`, `what-to-do-between-therapy-sessions`).
3. `-Republish -All -BodyOnly` w DryRun. W podsumowaniu `obrazki inne niz na zywo` powinno
   objąć oczekiwane wpisy, a `ROZNICA POZA OBRAZKAMI` musi wynosić 0.
4. Ta sama komenda z `-DryRun:$false`, za zgodą operatora.
5. Kontrola na żywo z cache-busterem (`?cb=<losowa liczba>`, Cloudflare trzyma stare wersje),
   przynajmniej na jednym wpisie z kartą i jednym z obrazkiem inline.

### Stan z 2026-10-21 (DryRun `-Republish -All -BodyOnly`)

36 wpisów `opublikowany`, wszystkie istnieją w Webflow, opublikowane, bez niezapisanych
zmian w CMS. 5 ma obrazki inline, 36 ma karty, 22 mają po renderze co najmniej jeden obrazek.
Różnic poza obrazkami: 0, czyli nikt nie edytował treści na żywo poza kolejką.
**8 wpisów nie ma na żywo 11 linków z `[LINK-LATER:]`** (cel wyszedł później, fixup ich nie
objął): `how-to-use-mindsync` (2), `how-to-prepare-for-a-therapy-session` (2),
`how-to-remember-what-you-talk-about-in-therapy` (1), `how-to-know-if-therapy-is-working` (1),
`how-to-choose-a-therapist` (2), `what-to-do-when-your-therapist-is-not-the-right-fit` (1),
`journaling-vs-voice-notes` (1), `racing-thoughts-at-night` (1). Potwierdzone na publicznych
stronach. Każde odświeżenie post-body tych wpisów doda te linki.

### Ostrzeżenia

- `-BodyOnly` wysyła **całe** post-body z kolejki, nie same obrazki. Każda różnica tekstu albo
  linków między kolejką a stroną pójdzie na żywo, dlatego DryRun przed LIVE jest obowiązkowy.
- Przepisany wpis zostaje w kolejce ze statusem `opublikowany`. Status `gotowy` nic by nie dał:
  drip pominąłby wpis jako już opublikowany, dorzucając tylko szum w logu.
- Bez publikacji całej strony `lastmod` w `sitemap.xml` się nie odświeży. Dla istniejących,
  zaindeksowanych URL-i to nie przeszkadza; jeśli ma się odświeżyć, publikację strony robi
  operator.
- W LIVE nie wywołuj przez `powershell -File` z `-DryRun:$false` (pułapka niżej).

## ⚠ Pułapka wywołania: `-DryRun:$false` NIE działa z `powershell -File`

`powershell -File skrypt.ps1 -DryRun:$false` przekazuje boola jako STRING i wywala
parametr (potwierdzone 2026-08-25). Poprawnie:
- w otwartej sesji PS: `& scripts\webflow\blog-publish.ps1 -Plik <plik>.json -DryRun:$false`
- z cmd/Task Scheduler: `powershell -NoProfile -NonInteractive -ExecutionPolicy Bypass
  -Command "& 'C:\...\blog-publish.ps1' -DripOne -DryRun:$false"`
Zadanie „MindSync Blog Drip" w Task Schedulerze (założone 2026-08-25, codziennie 07:00,
StartWhenAvailable) używa formy `-Command`.

## Test przed pierwszym dripem (checklist)

1. `.env` uzupełniony; `powershell -File blog-publish.ps1` (DryRun) na 1 wpisie testowym.
2. LIVE na 1 wpisie: `-Plik <plik>.json -DryRun:$false` → sprawdź `/journal/<slug>` na żywo:
   render body (czy karty przeżyły RichText), hero, thumbnail na `/blog`, meta title/desc
   (wymaga podpięcia pól SEO w ustawieniach szablonu – Designer), JSON-LD (Rich Results Test).
3. Dopiero po udanym teście: Task Scheduler codziennie 07:00
   (`-DripOne -DryRun:$false`, "Run task as soon as possible after a scheduled start is missed").

## Czego ten kanał NIE robi

- Nie generuje grafik (drip publikuje tylko gotowe hero z `blog/images/<slug>/`).
- Nie zmienia designu/szablonów (Designer = ręcznie operator albo MCP w sesji), ale
  **publikuje całą stronę** po udanym wpisie, więc niezapisane zmiany z Designera i tak
  trafią na żywo – patrz sekcja o `sitemap.xml` wyżej i przełącznik `-SkipSitePublish`.
- Nie podmienia kart w sekcji „Latest from the journal" na stronie głównej: tylko
  **sprawdza i zgłasza**, bo Data API nie ma na to kanału zapisu (dowody w sekcji o kontroli
  odkrywania wyżej). `lastmod` `/blog` odświeża (od 2026-09-25), zmieniając wyłącznie
  wewnętrzną nazwę strony.
- Niczego nie usuwa z Webflow.
