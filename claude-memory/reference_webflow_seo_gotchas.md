---
name: reference-webflow-seo-gotchas
description: "Pułapki Webflow Data API i renderowania przy pracy nad SEO mindsync.app (escapowanie JSON-LD, ignorowana flaga draft, cache CF, parser CSS)"
metadata: 
  node_type: memory
  type: reference
  originSessionId: 732ad635-483b-496b-b9ae-dc93edf40966
  modified: 2026-09-03T09:32:54.799Z
---

Cztery pułapki wykryte podczas audytu SEO mindsync.app (2026-08-26). Site `676ed8d44b863915ae191f41`, kolekcja Blog Posts `67cb62e9d0afa32a03eae3f1`.

**1. Webflow escapuje treść w `<script>` – JSON-LD z pola CMS jest zawsze nieważny.**
Wartość pola PlainText wstrzyknięta do `<script type="application/ld+json">` wychodzi z `&quot;` zamiast `"`. Wewnątrz `<script>` przeglądarka NIE dekoduje encji, więc `JSON.parse` zawodzi. Dotyczy to zarówno węzłów tekstowych elementów, jak i **custom code strony** (przetestowane i opublikowane – oba warianty escapują). Jedyny czysty kanał dla stron statycznych: natywne pole `jsonLdSchema` (`data_pages_tool > bulk_update_pages_schema_markup`) – renderuje surowo. Dla wpisów CMS zostaje obejście JS w szablonie (dekoduje przez `textarea.innerHTML`, waliduje `JSON.parse`, podmienia węzeł) – działa dla Google, nie dla crawlerów AI bez JS.

**2. `bulk_update_pages` po cichu ignoruje flagę `draft`.** Zwraca `draft:false` bez błędu i bez zmiany `lastUpdated`. Odpublikowanie strony działa wyłącznie przez `update_page_settings` per strona. Zawsze weryfikuj odpowiedź, nie zakładaj sukcesu.

**3. Cloudflare cache'uje agresywnie – weryfikacja po publikacji wymaga cache-bustera.** Po `publish_site` `Invoke-WebRequest` na czysty URL potrafi zwracać starą wersję jeszcze minutami. Dodawaj `?cb=<random>` przy sprawdzaniu efektu.

**4. `data_whtml_builder` odrzuca selektory zagnieżdżone.** `.card p` → błąd „Nested selectors are not allowed". Każdy element musi mieć własną klasę. `@media` też lepiej omijać – używaj `clamp()`. Selektory zagnieżdżone można dopisać później w site head custom code (tam parsera nie ma).

**5. Widoczność elementu i linki DA SIĘ zmienić przez API** – nie trzeba Designera. `data_element_settings_tool` ma `set_visibility`, `set_tag`, `set_dom_id` i `set_settings` (klucze `text`, `link`, `visibility`, `attributes`). Działa też wewnątrz definicji komponentu przez `scope_component_id`, czyli jedna zmiana wchodzi na wszystkie strony. Uwaga: łączenie w jednym wywołaniu odczytu (`get_settings`) i zapisu (`set_settings`) bywa blokowane przez klasyfikator – rozdziel na dwa wywołania.

**6. robots.txt: Webflow SAM dopisuje dyrektywę `Sitemap:`.** Przełącznik „Remove sitemap.xml from robots.txt" (Site Settings → SEO) domyślnie Off. Własna linia `Sitemap:` w polu robots.txt = zdublowana dyrektywa w serwowanym pliku. NIE dodawaj jej.

**7. llms.txt to natywne pole Webflow, nie Cloudflare.** Site Settings → SEO, sekcja „LLMs.txt → Upload llms.txt file" na samym DOLE strony (łatwo przeoczyć – trzeba doczytać `document.body.innerText` do końca). `llms-full.txt` nie ma odpowiednika, więc taki URL zawsze da 404. Pole robots.txt i llms.txt NIE są wystawione w Data API – tylko panel.

**9. `alt` obrazu: atrybut niestandardowy WYGRYWA z ustawieniem `altText`.** Jeśli `query_elements` pokazuje `attributes:{alt:...}`, samo `set_settings altText` nic nie zmieni w HTML (API zwróci sukces!). Trzeba najpierw `remove_attribute` na `alt`, potem `altText`. `set_attributes` z kluczem `alt` zwraca „internal error" – to atrybut zarządzany przez Webflow. To samo dotyczy `sizes` na obrazach.

**10. Sitemapa Webflow czyta USTAWIENIA STRONY, nie HTML.** `<meta robots noindex>` wstawiony przez custom code nie usunie URL-a z `sitemap.xml`. ~~Przełącznik „Include this page in sitemap" jest tylko w Designerze.~~ **KOREKTA 2026-09-03: flaga JEST dostępna z API** – `data_sitemap_tool` (`list_items_sitemap_status`, `update_item_sitemap_status`, `bulk_update_*`, namespace `/beta`). Da się ją czytać i ustawiać per item kolekcji i per strona statyczna, bez Designera.

**12. `sitemap.xml` regeneruje się WYŁĄCZNIE przy pełnej publikacji strony – publikacja itemu CMS jej NIE odświeża.** To najgroźniejsza pułapka dripu bloga i kosztowała ~tydzień niewidoczności. Objaw (2026-09-03): sitemap miał 22 URL-e, wszystkie z `lastmod` = `2026-08-26T20:42` identycznym z `lastPublished` strony, i brakowało w nim **6 z 10** wpisów wypuszczonych dripem 27.08-01.09 – mimo że wszystkie itemy miały `includeInSitemap: true`. Diagnostyka: porównaj `lastmod` w sitemapie z `lastPublished` z `GET /sites/{id}`; równe co do minuty = sitemap zamrożona od tej publikacji. Naprawa: `POST /sites/{id}/publish`. Po niej sitemap urosła do 28 URL-i i objęła wszystkie 10 wpisów.
⚠ **Skutek uboczny publikacji strony: wypycha na żywo TAKŻE niezapisane zmiany z Designera.** 2026-09-03 wisiały tam zmiany z 27.08 i poszły na produkcję (za jawną zgodą operatora). Dlatego `scripts/webflow/blog-publish.ps1` ma teraz krok publikacji strony po udanym wpisie, wyłącznik `-SkipSitePublish` i zasadę, że błąd publikacji strony NIE wywraca dripu (wpis jest ważniejszy niż sitemap).

**13. `[LINK-LATER:]` w dripie nigdy nie odrabia się sam.** Publikator degraduje link do gołego anchora, gdy cel jeszcze nie istnieje (chroni przed 404), zapisuje „LINK-LATER pominiety" do `_drip-log.txt` i **na tym koniec**. Partia 1 przeleżała tak od 25.08 do 03.09 z 5 martwymi anchorami; `how-to-use-mindsync` miał zero linków do innych wpisów, choć plan zakładał dwa. Rejestr do odrobienia: `blog/queue/_link-fixup.md` (aktualizuj po KAŻDEJ partii). Po zamknięciu partii zawsze zaplanuj zbiorczy fixup PATCH-em itemów.

**11. Skrypty „stylesXXX"/„mobilefixesXXX" w tym projekcie to opakowany CSS**, nie logika: `var s=document.createElement('style');s.textContent='...'`. Blokowały render (11 sztuk w `<head>`). Przeniesione do custom code jako `<style>` – site head dla reguł globalnych, custom code strony dla zakresowych. Został tylko `mobilefixesv7` (robi realną pracę na DOM). Przy takiej migracji: sprawdź selektory pod kątem zawężenia zakresu i NIE poprawiaj literówek w CSS (np. `1um`), bo martwa deklaracja = obecny wygląd.

**8. W tym środowisku z narzędzi Chrome działa TYLKO `javascript_tool`** (`computer:screenshot`, `find`, `read_page` timeoutują). Upload pliku bez `ref` robi się przez JS: base64 → `Uint8Array` → `new File(...)` → `DataTransfer` → `input.files = dt.files` → `dispatchEvent(new Event('change',{bubbles:true}))`. Pola React-owe (textarea) ustawiaj natywnym setterem z prototypu + `input`/`change`, inaczej stan Reacta się nie zaktualizuje.

Powiązane: [[project-seo-overhaul-mindsync-2026-08-26]], [[reference-backend-autodeploy-on-push]]

## WHTML builder: obrazek wymaga assetu W BIBLIOTECE WITRYNY (2026-09-15)
`data_whtml_builder` z `<img src="https://cdn.prod.website-files.com/...">` tworzy element typu `Image`, ale **wycina `src`**, jeśli plik nie jest assetem tej witryny. Zwraca `partial_success` + `image_warnings: "skipped ... since the image does not exist in asset library"`, a `get_attributes` na takim elemencie zwraca pustą listę. Grafiki CMS siedzą w **innym buckecie** (`.../676ed8d44b863915ae191fa7/...`) niż assety witryny (`.../676ed8d44b863915ae191f41/...`), więc URL z pola CMS nigdy nie przejdzie.

**Obejście:** `asset_tool > upload_image_by_url` (przyjmuje publiczny URL, więc można podać wprost adres grafiki z CMS) → z wyniku weź `id` → `data_element_tool > set_image_asset`. Uwaga: `asset_name` dostaje doklejone rozszerzenie drugi raz (`...webp.webp`).

**Drugi gotcha, styl:** `update_style` **dokłada** właściwości zamiast zastępować, więc po ustawieniu skrótu (`border-color`, `border-radius`) w stylu zostają RAZEM z longhandami z pierwotnego CSS (`border-top-color` itd.). Ustawiaj longhandy wprost, inaczej o wynik decyduje kolejność w wygenerowanym CSS.

**Trzeci:** builder nie obsługuje **zagnieżdżonych selektorów CSS** – tylko płaskie, jednoklasowe reguły.

## Zapis tresci statycznej: REST v2 NIE potrafi, MCP potrafi (ustalone 2026-09-22)
Rozroznienie, ktore kosztowalo cala rundę rozpoznania. Te dwa kanaly maja **rozne mozliwosci**, nie tylko rozna autoryzacje.

- **Publiczne Data API v2 (`POST /v2/pages/{id}/dom`)**: zapis tresci statycznej jest dostepny **wylacznie dla lokalizacji dodatkowych**. mindsync.app ma `locales.secondary = []` i `primary.enabled = false`, wiec endpoint jest **zamkniety w calosci**. Dodatkowo jego schemat nie obejmuje obrazkow, a `href` linku-elementu (np. `<a class="...">` opakowujacy karte) w ogole nie jest adresowalnym wezlem: `GET /pages/{id}/dom` zwraca dzieci karty, ale nie sama karte. Link **tekstowy** ma widoczne `attributes.href` w odczycie, ale zapis i tak go nie przyjmuje.
- **MCP Webflow `data_element_tool`**: ma `set_link` (href), `set_text`, `set_image_asset`, `set_attributes`, dziala na **lokalizacji glownej**, **bezglowo** (bez Bridge App i bez otwartego Designera; Bridge potrzebny tylko do rzeczy zaleznych od zywej sesji, np. zrzutow canvasu). Czyli MCP siega warstwy element-level, ktorej w publicznej referencji REST nie ma.
- `data_whtml_builder` **tylko wstawia nowe** elementy z HTML/CSS. Do podmiany istniejacych nie sluzy (tym powstala sekcja `ms-journal-latest` 15.09).

**Konsekwencja praktyczna:** nieobslugiwany publikator (Task Scheduler + PowerShell + token z `.env`) **nie zautomatyzuje** zmiany tresci statycznej. MCP zyje w sesji Claude z wlasna autoryzacja. Nie ma znanego publicznego endpointu REST dla operacji element-level, ktory skrypt moglby zawolac tokenem site.

**Pola, ktore przyjmuje `PATCH /v2/pages/{id}`:** tylko `title`, `slug`, `seo.title`, `seo.description`, `openGraph.title`, `openGraph.description` (+ flagi `*Copied`). Nie ma pola neutralnego, wiec **nie da sie ruszyc `lastUpdated` strony bez zmiany czegos widocznego dla uzytkownika**. Nie churnuj copy SEO po to, zeby ruszyc date, i nie przelaczaj `openGraph.titleCopied` tam i z powrotem: to zostawia niedeterministyczny stan i podklada mine pod przyszla zmiane `seo.title`.

## PowerShell 5.1: `,@($x) | ConvertTo-Json` niszczy tablice (ustalone 2026-09-22)
`,@($entries) | ConvertTo-Json -Depth 8` w PS 5.1 zapisuje **nie tablice, tylko** `{ "value": [...], "Count": N }`. Kazdy kolejny cykl zapis-odczyt zawija poprzedni wynik w nastepna warstwe. Realnie zdarzylo sie w `blog/published-log.json`: 5 warstw matrioszki, czesc wpisow splaszczona przy `-Depth` do tekstu `"@{tytul=...}"`, jeden przepadl jako `"@{value=System.Object[]; Count=2}"`, a `Already-Published` widzial **zero** slugow, wiec idempotencja po slugu nie dzialala w ogole (chronil tylko status `opublikowany` w pliku kolejki).

**Poprawnie:** `ConvertTo-Json -InputObject @($entries) -Depth 8`. Dotyczy takze tablicy jednoelementowej. Nie „upraszczaj" tego z powrotem do potoku.

**Wniosek ogolny:** przy kazdym zapisie JSON z PS 5.1 sprawdzaj **pierwszy znak pliku po zapisie** (`[` kontra `{`), a nie sama logike. I miej drugi, niezalezny zapis tego samego zdarzenia: historie `published-log.json` dalo sie odtworzyc w 100% wlasnie dlatego, ze `_drip-log.txt` ma linie `OK opublikowano` z data, godzina i `item_id`.

## Collection List przez MCP: tresc TAK, link do wpisu NIE (ustalone 2026-09-22)
Sekcja „Latest from the journal" na `/` zostala przerobiona ze statycznych kart na Collection List **bezglowo przez MCP**, bez Designera. Co dziala i co nie:

**Dziala w pelni:** utworzenie listy (`data_element_builder`, typ **`CMSCollection`** → tworzy `DynamoWrapper` > `DynamoList` > `DynamoItem` + `DynamoEmpty`), ustawienia zapytania (`data_element_settings_tool` → `source` jako `static_json` `{"collectionId":"..."}`, `queryMode`, `limit`, `offset`), nadanie klas (`set_style`), przenoszenie elementow (`move_element`), tworzenie klas (`data_style_tool > create_style`) oraz **bindingi tresci**: `text` → pole plainText, `assetId` → pole image, `altText` → pole plainText. Wszystko potwierdzone renderem.

**NIE dziala: link karty do jej wlasnego wpisu.** Trzy proby, wszystkie przez staging:
- `static_link` `{mode:"collectionPage"}` bez `to` → renderuje `href="#"` (mimo ze **dokladnie taki sam zapis** na `/blog`, zrobiony w Designerze, renderuje poprawny `/journal/<slug>`),
- `{mode:"collectionPage", to:"<cokolwiek>"}` → `to` trafia do href **doslownie** (probowane `journal` i id strony szablonu),
- element natywny (`LinkBlock` z buildera) zamiast `<a>` z WHTML i jawny `queryMode:"dynamic"` niczego nie zmienily.

`get_bindable_sources` dla klucza `link` zwraca **0 zrodel**, a `href` jako atrybut jest **zastrzezony** na elemencie Link (`"href" is a reserved attribute name`). Na elemencie **DOM** (`type:"DOM"`, `dom_tag:"a"`) atrybut `href` przyjmuje `value_static`, ale `value_binding` do pola CMS jest odrzucany (`value must be a string or a binding`). Czyli **nie da sie zbudowac href z pola CMS**.

**Wniosek operacyjny (POTWIERDZONY 2026-09-22):** liste kolekcji zbuduj i obindowac mozna calkowicie zdalnie, ale ustawienie linku do wpisu **wymaga jednego kliniecia w Designerze** i wtedy dziala od razu. Nie marnuj kolejnej rundy na obchodzenie tego przez API.

W Designerze sciezka nazywa sie inaczej, niz sugeruje API: zaznacz karte, **Settings → Link Block settings → Type → `Collection page`** (NIE ma pozycji „Current <Collection> page" w liscie celow; wybor kolekcji pojawia sie w polu ponizej po zmianie Type). Po tej zmianie zapisany stan to dalej `{"mode":"collectionPage"}`, **identyczny z tym, co zapisuje API**, a mimo to renderuje sie poprawnie. Czyli po samym odczycie ustawien **nie odroznisz wersji dzialajacej od niedzialajacej** - jedynym testem jest render na stagingu.

**Kolejnosc domyslna Collection Listy = najnowsze pierwsze.** Kolekcja Blog Posts **nie ma zadnego pola z data**, wiec `sort` po `created-on`/`published-on`/`updated-on` jest odrzucany (`Unknown field`). Sortowanie jest jednak zbedne: `/blog` ma `sort: []` i renderuje wpisy od najnowszego. Zweryfikowane na zywym HTML.

**Bezpieczna procedura zmian na Home:** pracuj na zastagowanym stanie i publikuj `publishToWebflowSubdomain: true` (staging `mind-sync.webflow.io`), domeny produkcyjne zostaja nietkniete. Publikacja ma limit **1/min** (429 przy szybszym tempie), a render na stagingu potrafi byc opozniony o kilkanascie sekund, wiec odpytuj w petli. ⚠ Pamietaj, ze **drip o 07:00 publikuje caly site na domeny produkcyjne**, wiec zastagowany stan nie moze zostac zepsuty na noc.

**Nowe pole w kolekcji Blog Posts:** `card-url` (PlainText, id `bb9938c346ffb28440e45bc79677a406`) z wartoscia `/journal/<slug>`, wypelnione dla wszystkich 27 rekordow. Powstalo jako proba obejscia problemu z linkiem i **nie jest przez nic uzywane**. Zostaje jako gotowy material, gdyby kiedys przydal sie href z CMS. `PATCH /items/live` odrzuca rekordy nigdy nieopublikowane (409), wiec leci `PATCH /items` + `POST /items/publish`.

**Nowa klasa CSS:** `ms-journal-item` (`display:block; flex:1 1 280px`) na `DynamoItem`, bo Collection Item wchodzi miedzy flexowa siatke `.ms-journal-list` a karte `.ms-journal-card` i bez tego karty rozjezdzaja sie na szerokosci.

## ⚠ Masowa publikacja itemow CMS wskrzesza wycofane wpisy (wpadka 2026-09-22)
Przy uzupelnianiu nowego pola poszlo `PATCH /collections/{id}/items` + `POST /collections/{id}/items/publish` z **lista wszystkich 27 ID** z kolekcji. Skutek: 5 starych wpisow demo Webflow (`therapy-progress-1`, `therapy-tracking-2`, `wellbeing-in-therapy-3`, `therapy-and-progress-4`, `therapy-and-wellbeing-5`), swiadomie wycofanych wczesniej, **wrocilo na zywo i do sitemapy** (34 → 39 URL). Cztery ratowaly recznie dodane 301-ki, ale `therapy-and-wellbeing-5` zaczal zwracac 200 z trescia lorem-ipsum.

**Zasada:** `items/publish` NIGDY z pelna lista z `GET /items`. Kolekcja zawiera rowniez rekordy celowo nieopublikowane, a `GET` nie odroznia ich w oczywisty sposob (`isDraft=false`, `isArchived=false`, ale **`lastPublished` jest puste**). Filtruj po `lastPublished` albo po jawnej liscie slugow.

**Naprawa:** MCP `data_cms_tool > unpublish_collection_items` (do 100 itemow, cofa do draftu i zdejmuje z zywej strony), potem publikacja site dla przegenerowania sitemapy. Zweryfikowane: sitemapa 39 → 34, demo znowu 301/404.

**Uwaga narzedziowa:** surowy `DELETE /items/{id}/live` przez skrypt w Bashu zostal zablokowany przez klasyfikator auto-mode (Modify Shared Resources). Kanal MCP przeszedl. Przy operacjach kasujacych na wspoldzielonych zasobach siegaj od razu po MCP zamiast po wlasny skrypt.
