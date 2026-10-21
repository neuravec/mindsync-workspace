# Shoper webapi REST — dokumentacja robocza (kanał DANE)

> Lokalne źródło prawdy dla agenta **`shoper-api`**. Rdzeń (przepływ autoryzacji, bazowy URL,
> kształt odpowiedzi) jest **zweryfikowany działającym skryptem** `scripts/shoper-api/connect-test.ps1`.
> Listę zasobów i szczegóły pól **potwierdzaj na żywo** w oficjalnej dokumentacji (SPA — patrz niżej).

## Czym to jest (i czym NIE jest)

- **webapi REST** = kanał **DANYCH** sklepu: produkty, kategorie, producenci, atrybuty, zamówienia,
  klienci, przekierowania 301, strony/aktualności CMS, konfiguracja. To **pkt 1 i 6** zakresu projektu
  oraz import ~7 900 produktów. Bazuje na koncie administratora z uprawnieniem **„dostęp do webapi"**.
- **To NIE jest** kanał szablonu graficznego. Motyw Storefront (Twig/LESS/moduły) obsługuje **Shoper CLI**
  → agent `shoper-cli`, doc `.claude/docs/shoper-cli.md`. Nie mylić kanałów.

## Uwierzytelnianie (zweryfikowane)

1. `POST https://<DOMENA>/webapi/rest/auth` z nagłówkiem **Basic Auth** = `base64(login:hasło)`
   konta administratora z dostępem do webapi.
2. Odpowiedź: `{ "access_token": "...", "expires_in": 3600, "token_type": "bearer" }`.
3. Każde kolejne żądanie: nagłówek **`Authorization: Bearer <access_token>`**.
4. Token żyje **1 godzinę (3600 s)** → po wygaśnięciu pobrać nowy. Skrypt zapisuje token do
   `scripts/shoper-api/.token.json` (gitignore) do ponownego użycia przez ~1h.

- Bazowy URL zasobów: `https://<DOMENA>/webapi/rest/<zasób>`.
- Dane dostępowe: **wyłącznie** `scripts/shoper-api/.env` (`SHOPER_URL`, `SHOPER_LOGIN`, `SHOPER_PASSWORD`),
  plik w `.gitignore`. **Nigdy** nie wpisuj loginu/hasła/tokenu do odpowiedzi ani do plików repo.

### Token permanentny (alternatywa — zweryfikowane 2026-06-08)

Shoper oferuje też **token permanentny** (nie wygasa), generowany w panelu:
**Aplikacje i integracje > Aplikacje zewnętrzne** → wybór narzędzia/„Inne" → nazwa+opis →
zakres uprawnień (odczyt / +tworzenie / +edycja / +usuwanie) → „Zapisz i utwórz token".
Cytat z dok.: *„Raz wygenerowany token nie traci ważności i nie wygasa"*. Token jest **odwoływalny**
(wygenerowanie nowego unieważnia poprzedni) i ma **granularne uprawnienia**.
Stary przepływ login+hasło (`POST /webapi/rest/auth`) **nadal działa** (wsteczna zgodność).
→ Dla długich operacji (import ~7 900 produktów) token permanentny eliminuje odświeżanie co 1h;
   jeśli user go wygeneruje, można go trzymać w `.env` jako `SHOPER_TOKEN` i pominąć krok `auth`.

## Operacje i kształt odpowiedzi

- Metody: `GET` (lista/pojedynczy), `POST` (utwórz), `PUT` (aktualizuj), `DELETE` (usuń).
- Pojedynczy obiekt: `GET /webapi/rest/products/{id}`.
- Listy zwykle zwracają obiekt z polami **`count`**, **`pages`**, **`page`**, **`list`** (paginacja).
- Parametry list (potwierdź zakres w dok.): **`limit`** (rozmiar strony, typowo do 50),
  **`page`** (numer strony), **`filters`** (URL-encoded JSON, np. `{"stock.stock":{">":0}}`),
  **`order`**. Przy ~7 900 produktach **zawsze paginuj** i **throttluj**.

## Najczęstsze zasoby (potwierdzaj nazwy/pola na żywo)

`products`, `product-images`, `product-stocks`, `categories`, `categories-tree` (hierarchia),
`producers`, `attributes`, `attribute-groups`, `availabilities`, `units`, `taxes`, `currencies`,
`languages`, `shippings`, `payments`, `orders`, `order-products`, `statuses`, `users` (klienci),
`redirects` (301), `news` (CMS/aktualności), `pages` (strony CMS), `webhooks`, `parcels`, `gauges`,
`option`/`config`.

### Wzorce URL (potwierdzone na żywo 2026-06-08, host testowy)

URL niesie pole **`translations.pl_PL.permalink`** (pełny URL). Pole **`seo_url`** to *opcjonalny
ręczny slug* — gdy puste (domyślnie), Shoper generuje URL z `name` + ID. Schemat:

- **Produkt:**   `/pl/p/<Nazwa-z-myslnikami>/<product_id>`   (np. `/pl/p/Sukienka-Malaga/35`)
- **Kategoria:** `/pl/c/<Nazwa-z-myslnikami>/<category_id>`  (np. `/pl/c/Sukienki/16`) — **PŁASKI**,
  bez ścieżki rodziców, niezależnie od zagnieżdżenia w drzewie. Hierarchię (parent→children) zwraca
  osobny zasób `categories-tree`; płaski `categories` ma tylko flagę `root` (0/1) i `order`, **bez
  `parent_id`** w obiekcie GET.
- **Producent:** `/pl_PL/producer/<Nazwa>/<producer_id>` (uwaga: locale `pl_PL`, nie `pl`).
- Język w URL = krótki kod `pl` (produkt/kategoria) — wynika z aktywnego locale `pl_PL` (`languages`).

> ⚠️ Eksporter Mercatum jest ubogi (brak EAN/SKU/kategorii) — mapowanie do pól Shopera planować świadomie.
> Przy imporcie normalizować kodowanie (windows-1250 → UTF-8) i myśleć o ciągłości SEO (301, canonical).

## Blog / aktualności — zasób `news` (+ `news-categories`, `news-tags`) — zweryfikowane na żywo 2026-06-10

Blog Shopera = zasób **`news`** (NIE `pages`). Na koncie TEST `sklep261208` **ZAPIS przez webapi
jest DOSTĘPNY** (inaczej niż `pages`, które zwraca „Missing MODULE 'pages'"). Rozeznanie: skrypt
`scripts/shoper-api/rozeznanie-news-readonly.ps1` (TYLKO GET) → zrzuty w `_rozeznanie/news-*.json`.

### Realne pola wpisu `news` (GET `/webapi/rest/news/{id}` — z żywych 4 wpisów)

| pole | typ | uwagi |
|---|---|---|
| `news_id` | string (liczba) | PK; nadawany przy POST, w URL wpisu |
| `name` | string | tytuł wpisu (= H1/`<title>` źródłowy) |
| `content` | string (HTML) | pełna treść; HTML, escapowany w JSON. **`<script type="application/ld+json">` PRZEŻYWA 1:1 (NIE sanityzowany)** — inaczej niż `aboutpages.content`, gdzie `<script>` jest wycinany. Szczegóły: sekcja „JSON-LD w `news.content`" niżej |
| `short_content` | string (HTML) | zajawka/lead (lista bloga, OG description bazowy) |
| `date` | `YYYY-MM-DD HH:MM:SS` | data publikacji widoczna na froncie (sortowanie) |
| `author` | string | podpis autora (dowolny tekst, np. „Plasmet") |
| `start_page` | `0/1` | czy wpis pokazywany na stronie głównej |
| `lang_id` | string (liczba) | język; `1` = polski na tym koncie (zgodne z `languages`) |
| `order` | string (liczba) | kolejność |
| `seo_title` | string | meta title (pusty → fallback na `name`) |
| `seo_description` | string | meta description (pusty → fallback na `short_content`) |
| `seo_keywords` | string | meta keywords (marginalne SEO) |
| `seo_url` | string\|null | **ręczny slug**; `null` → Shoper generuje URL z `name`+`id` |
| `image` | string (base64) | **GŁÓWNE ZDJĘCIE wpisu** (hero/miniatura) — **TYLKO w PUT/POST, NIE odbijane w GET**. Wartość = **base64 binarki pliku** (NIE data-URI, NIE URL; data-URI → „Cannot decode the contents of the file”). PUT `news/{id}` `{image:<base64>}` → HTTP 200 i obraz zostaje zapisany. Usunięcie: `image:''`. **To pole motyw renderuje** jako miniaturę na liście + zdjęcie w treści wpisu. (ZWERYFIKOWANE krzyżowo 2026-06-10 — patrz niżej) |
| `image_name` | string | **OPIS/ALT głównego zdjęcia** (w demo = tytuł wpisu). **Zapisywalny PUT-em TYLKO gdy obraz już istnieje** — PUT `image_name` SOLO bez obrazu → **HTTP 400 „If you want to add an image description you must first add image”**. Dlatego alt wysyłaj RAZEM z `image` w jednym PUT/POST. Niepuste `image_name` w GET = sygnał, że wpis MA obraz główny (`news` GET nie odbija samego `image`). |
| `active` | `0/1` | widoczność; **`0` = szkic/ukryty** (bezpieczny tryb do testów) |
| `box` | `0/1` | czy wpis w „boxie"/widgecie |
| `tags` | array[int] | **lista `tag_id`** (relacja wpis→tagi zaszyta wprost w obiekcie news) |

> ⚠️ Obiekt `news` GET **NIE zawiera** pola `category_id` — relacja wpis↔kategoria **nie jest**
> zwracana w obiekcie, ale **jest filtrowalna**: `GET /news?filters={"category_id":"4"}` zwraca wpisy
> tej kategorii (zweryfikowane: cat 3 „Stylizacje"→wpisy 4,5; cat 4 „Porady"→wpisy 2,3).
> ⚠️ **POTWIERDZONE 2026-06-10 smoke-testem:** pole `category_id` (l. poj.) w payload POST `/news` **NIE wiąże**
> wpisu z kategorią (test: `category_id:4` w POST → wpis NIE pojawił się w filtrze kat. 4).
> ✅ **ROZWIĄZANE 2026-06-10 (realna publikacja wpisu #1, `news_id=7`):** pole **`categories:[id]` (l. mnoga,
> tablica)** w POST `/news` **WIĄŻE** wpis z kategorią bloga — potwierdzone filtrem
> `GET /news?filters={"category_id":"5"}` → zwrócił `news_id=7`. **Wzorzec wiązania kategorii:** użyj
> `categories:[category_id]` w payload POST (nie `category_id` l. poj.). Fallback gdyby nie zadziałało:
> PUT `/news/{id}` z `categories:[id]`, potem `category_id` l. poj.
> ✅ **POTWIERDZONE NA PRODUKCJI 2026-07-16 (13 wpisów):** **PUT `news/{id}` z `{categories:[<id>]}` ZASTĘPUJE**
> dotychczasowe przypisanie kategorii (wpis znika ze starej, jest w nowej — weryfikacja filtrem `category_id`
> przed/po). PUT z samym `categories` nie rusza innych pól (hero/`image` nietknięte). POST `news-categories`
> `{name, lang_id, active}` zwraca w body nowe `category_id`. Skrypt wzorcowy: `recategorize-news-2026-07-16.ps1`.
> `tags` w POST przyjmuje **istniejące `tag_id`** → tagi trzeba najpierw utworzyć/odszukać w `news-tags`.

### `news-categories` (GET — 2 kategorie: „Stylizacje" id 3, „Porady" id 4)

Pola: `category_id`, `name`, `order`, `active` (0/1), `lang_id`, `seo_title`, `seo_description`,
`seo_keywords`, `seo_url`. Brak `parent_id` (płaska struktura, jak kategorie produktowe w GET).

### `news-tags` (GET — 9 tagów)

Pola: **`tag_id`**, `name`, `lang_id`. Minimalne. Wpis wiąże się z tagiem przez tablicę `tags:[id,…]`
w obiekcie `news`. Idempotencja przy publikacji: przed POST sprawdź `news-tags` po `name`, użyj
istniejącego `tag_id` albo utwórz nowy tag (POST `news-tags`) i dopiero wstaw jego id do `news.tags`.
POST `news-tags` zwraca w body **nowe `tag_id`** (gdy połączenie się domknie). PUT `news/{id}` z `tags:[…]`
**nadpisuje** zestaw tagów wpisu (potwierdzone: doczepienie 5 tagów do `news_id=7`).
> ⚠️ **PAGINACJA `news-tags` (pułapka find-or-create, 2026-06-10):** lista ma **domyślny rozmiar strony
> ~10** mimo `limit=100` — przy `count>10` (np. 14) `page=1` zwraca tylko 10 rekordów, a świeżo utworzone
> tagi mogą wpaść na `page=2` i **find-or-create ich nie znajdzie** (fałszywe „NIE utworzono", a w praktyce
> duplikat/`ERR:400` przy ponownym POST tej samej nazwy). **Zawsze paginuj `news-tags` po `pages`** zanim
> uznasz tag za nieistniejący.

### ✅ GŁÓWNE ZDJĘCIE (hero/miniatura) wpisu = pole `image` (base64) w PUT/POST `news` — ZWERYFIKOWANE KRZYŻOWO 2026-06-10 (news_id=7)

> ⚠️ **KOREKTA wcześniejszej błędnej notatki.** Poprzednio twierdziliśmy, że hero/miniatura = pierwszy plik
> galerii `news-files` (`order=0`). **TO BYŁO BŁĘDNE.** Plik wgrany do `news-files` (file_id=4 pod news_id=7)
> **NIE renderował się** ani jako miniatura listy, ani jako zdjęcie wpisu (pusty slot na froncie). `news-files`
> to **galeria/załączniki**, NIE główne zdjęcie. **Główne zdjęcie wpisu to pole `image` (base64) na obiekcie
> `news`**, ustawiane PUT/POST — to ono jest renderowane przez motyw.

**Mechanizm (potwierdzony logiką krzyżową, nie tylko HTTP 200):**

- **`PUT /webapi/rest/news/{id}` z `{ "image": "<base64 binarki pliku>" }`** ustawia główne zdjęcie. Zwraca
  HTTP 200, raw `1`. **`image` to base64 zawartości pliku, NIE data-URI, NIE URL** — data-URI
  (`data:image/png;base64,…`) → **HTTP 400 „Cannot decode the contents of the file”** (czysty base64 przechodzi).
- **`image_name` = OPIS/ALT** głównego zdjęcia. Da się go zapisać PUT-em **TYLKO gdy obraz już istnieje**:
  PUT `image_name` SOLO bez obrazu → **HTTP 400 „If you want to add an image description you must first add
  image”**. → alt wysyłaj **RAZEM** z `image` w jednym PUT (`{image:<base64>, image_name:<alt>}`).
- **Usunięcie głównego zdjęcia:** `PUT news/{id}` z `image:''` (pusty string) → HTTP 200; po tym `image_name`
  znów się blokuje (potwierdza, że obraz zniknął).
- **`news` GET NIE odbija `image`** (stałe 17 pól, bez `image`). **Dowód obecności obrazu bez frontu:** GET
  `news/{id}` → `image_name` niepuste **albo** PUT `image_name` SOLO → 200 (gdy 200 = obraz jest; gdy 400
  „must first add image” = obrazu brak). Tym testem zweryfikowano naprawę #7 bez dostępu do frontu (front TEST
  `shoparena.pl` odrzuca zewnętrzne HTTP).
- **Dowód krzyżowy (skrypt `test-news-image-confirm.ps1`):** (A) `image_name` SOLO bez obrazu → 400; (B) PUT
  `image=<base64>` → 200; (C) `image_name` SOLO PO obrazie → 200 + zapisane. A∧C ⇒ pole `image` realnie DODAJE
  obraz (zmienia stan serwera), nie tylko zwraca 200.
- **Zgodność ze wzorcem demo:** wpisy demo (news_id 2–5, z motywem) mają `image_name`=tytuł (alt) i **zero
  rekordów w `news-files`** — a renderują obraz. To potwierdza, że obraz idzie pod `image`, nie do `news-files`.
- **Format pliku:** JPG/PNG pewne (demo i nasz hero). **WebP** nie był walidowany na żywo dla `image` — dla hero
  używaj **JPG** (`hero-1600x900.jpg`), bezpieczny i tożsamy z demo. Rozmiar hero ≤ ~150 KB (budżet LCP) — OK;
  base64 ~+33%, w razie dużych plików zwiększ `WriteDeadlineSec`.
- **Zapis** wykonuj **wzorcem odpornym na „wiszący zapis”** (`HttpWebRequest` + `.Timeout`/`.ReadWriteTimeout`/
  `.KeepAlive=$false`) — patrz niżej.
- **Skrypt produkcyjny:** `scripts/shoper-api/news-hero-upload.ps1` (domyślnie `-DryRun`; PUT `news/{id}`
  `{image, image_name}`; `-RemoveImage` usuwa; auto-szuka `hero-1600x900.(webp|jpg|png)` po `-Slug` lub bierze
  `-ImagePath`). Weryfikacja + sprzątanie: `verify-and-cleanup-hero.ps1`. Diagnostyka (reverse-engineering):
  `diag-news-mainimage.ps1`, `diag-news-imgsource.ps1`, `diag-news-image-put-probe.ps1`, `test-news-image-confirm.ps1`.

**Zasób `news-files` (galeria/załączniki — NIE hero):** istnieje (`POST {news_id, name, content(base64),
[description], [order]}` → `file_id`; GET-owalny `news-files/{id}`: `file_name`=hash na dysku), ale pliki w nim
**NIE są renderowane jako główne zdjęcie/miniatura wpisu**. Używać tylko do faktycznych załączników/galerii
inline, gdyby motyw je wspierał. Sonda zasobów obrazu wpisu (GET, news_id=7): `news-image`, `news-img`,
`news-photo`, `news-gfx`, `news-main`, `news-cover`, `news-media`, `blog` itd. → wszystkie **HTTP 400 „Missing
MODULE”** (nie istnieją); jedyne realne zasoby to `news` (z polem `image`) i `news-files` (galeria).

### Minimalny payload POST `/news` (z oficjalnej dok. developers.shoper.pl)

Wymagane minimum: `name`, `content`, `lang_id`. Reszta pól opcjonalna (defaulty Shopera).
Bezpieczny szkic do testu uprawnień: `{"name":"…","content":"…","lang_id":1,"active":0}` (`active=0`
= niewidoczny na froncie).

### ✅ JSON-LD w `news.content` — `<script type="application/ld+json">` PRZEŻYWA 1:1 — ZWERYFIKOWANE NA ŻYWO 2026-06-11 (za zgodą usera)

**WERDYKT: TAK — `<script type="application/ld+json">…</script>` PRZEŻYWA w `news.content` przez webapi
bez żadnej modyfikacji (1:1).** To **odwrotnie niż `aboutpages.content`**, gdzie `<script>` jest WYCINANY
(sanityzacja). Blog (`news`) ma INNĄ politykę treści niż strony informacyjne (`aboutpages`) — **nie zakładaj
tego samego zachowania dla obu zasobów**.

Test kontrolowany 1-wpis (`active=0`, od razu skasowany), skrypt `scripts/shoper-api/test-news-script-jsonld.ps1`:

- **POST `/news`** z `content` = `<p>…</p>` + `<script type="application/ld+json">{"@context":"https://schema.org","@type":"BlogPosting","headline":"Test"}</script>`
  → HTTP 200, `news_id=13`.
- **GET `/news/13`** → zwrócony `content` **bit-w-bit identyczny** z wysłanym (163 zn. = 163 zn.):
  pełny blok `<script ld+json>` zachowany 1:1, payload (`schema.org`/`@type:BlogPosting`) nienaruszony,
  **ZERO encjowania** (`&lt;script` = False, nie zamieniony na widoczny tekst), HTML body `<p>` zachowany.
- **DELETE `/news/13`** → HTTP 200, GET → HTTP 404, brak sierot po `name`. Sprzątanie kompletne.

**Wniosek operacyjny dla schemy bloga (BlogPosting + FAQPage):**

- **Schemę JSON-LD wstrzykuj per-post na końcu pola `content` przez webapi** — to działa, jest automatyzowalne
  (POST/PUT `news`), idempotentne (możesz nadpisać `content` PUT-em) i nie wymaga motywu ani panelu.
  ⚠️ **Front nie był weryfikowany na żywo** (front instancji TEST blokuje zewnętrzne HTTP) — render `<script>`
  w `<body>` strony wpisu potwierdzić na produkcji `sklep.plasmet.pl`. JSON-LD w `<body>` jest **ważny dla
  Google** (Google parsuje JSON-LD niezależnie od pozycji w DOM), więc umieszczenie na końcu `content` jest OK.
- **Alternatywy (gdyby front jednak nie renderował lub wolisz `<head>`):** (a) globalny `<head>` motywu
  (panel: Dodatki i integracje > Integracje własne > „Nagłówek `<head>`") z warunkiem na URL wpisu —
  ale to NIE jest per-post-automatyzowalne przez webapi; (b) szablon wpisu bloga w motywie (`shoper-cli`) —
  wstrzyknięcie bloku schemy w Twig listy/wpisu (jednorazowa zmiana motywu obejmująca wszystkie wpisy,
  z danymi z kontekstu wpisu). **Rekomendacja: per-post w `content` przez webapi** (najprostsze, w pełni
  w kanale DANE) — droga motywu tylko jeśli chcemy schemę dla WSZYSTKICH wpisów jednym szablonem.
- **Uwaga przy łączeniu z opisem wpisu:** JSON-LD doklejony do `content` zwiększa rozmiar pola i pojawia się
  w treści — trzymaj go na samym końcu, jako jeden blok `<script>`, żeby nie kolidował z WYSIWYG panelu
  (panel może go pokazać w trybie źródła; WYSIWYG zwykle go nie tknie, ale przy edycji w panelu warto
  zweryfikować, że nie został usunięty ręcznie).

### ✅ SMOKE-TEST ZAPISU — POTWIERDZONY NA ŻYWO 2026-06-10 (za zgodą usera)

Wykonany kontrolowany 1-wpis (szkic `active=0`, od razu skasowany) skryptem
`scripts/shoper-api/smoke-test-news.ps1` (+ pomocnicze `verify-and-cleanup-news.ps1`,
`check-news-orphan.ps1`). **Werdykt jednoznaczny:**

- **ZAPIS `news` DZIAŁA (TAK).** POST `/webapi/rest/news` z payloadem
  `{"name":"…","content":"<p>…</p>","lang_id":1,"active":0,"category_id":4}` **utworzył wpis**
  (`news_id=6`, `active=0`, `lang_id=1`) — żadnego „Missing MODULE"/403. Konto webapi PLASMET **ma**
  uprawnienie tworzenia/usuwania aktualności. DELETE `/webapi/rest/news/6` **usunął wpis** (count 4→5→4,
  GET potwierdził brak). Pole `category_id` w obiekcie GET wpisu **nie występuje** (zgodne z wcześniejszą obserwacją).
- **`category_id` w POST NIE WIĄŻE wpisu z kategorią (NIE).** Mimo `category_id:4` w payload, filtr
  `GET /news?filters={"category_id":"4"}` zwrócił **tylko 2,3** (bez nowego 6) → kategoria zignorowana
  przy POST. **Wniosek operacyjny dla realnej publikacji:** powiązania wpis↔kategoria **nie da się ustawić
  jednym polem `category_id` w POST `/news`**. Do ustalenia przy pierwszej realnej publikacji: czy działa
  pole `categories:[id]` (l. mnoga), osobny PUT po utworzeniu, albo dedykowany sub-zasób. **Fallback pewny:**
  ustawić kategorię ręcznie w panelu (Blog) lub potwierdzić alternatywne pole kolejnym mini-testem za zgodą.
- **⚠️ PUŁAPKA „wiszący zapis" (host PLASMET).** POST i DELETE na tym koncie **nie domykają połączenia
  szybko** — klient (`Invoke-WebRequest`, nawet z `-TimeoutSec 30`) **wisi i nie odczytuje ciała odpowiedzi**,
  ale **operacja po stronie serwera WYKONUJE SIĘ** (wpis powstał / został skasowany). Skutek: skrypt nie
  zwróci `news_id` z odpowiedzi POST i może utknąć. **Wzorzec bezpieczny dla zapisów `news`:** po POST/DELETE
  **nie polegaj na odczycie odpowiedzi** — zweryfikuj efekt osobnym, krótkim **GET listy** (po `name` lub
  `count`), z którego odczytasz realne `news_id` (idempotencja po `name`). Dla importu/drip publikacji:
  krótki timeout + weryfikacja przez GET zamiast czekania na body zapisu + retry idempotentny (sprawdź,
  czy wpis o danym `name` już istnieje, zanim ponowisz POST).
- **✅ ROZWIĄZANIE „wiszącego zapisu" — POTWIERDZONE realną publikacją 2026-06-10 (`news_id=7`).** Trzy
  podejścia testowane: (1) `Invoke-WebRequest -TimeoutSec` **NIE odpala niezawodnie** — wisi w nieskończoność
  na pierwszym POST (musiał być ubity). (2) `Start-Job` + `Wait-Job -Timeout` → **deadlock**
  („jobs are blocked waiting for user interaction" — `Invoke-WebRequest` w jobie blokuje się na strumieniu
  progresu). (3) **DZIAŁA:** `System.Net.HttpWebRequest` z **`.Timeout` ORAZ `.ReadWriteTimeout`** (oba
  ustawione, np. 12 s) + `.KeepAlive=$false` — `ReadWriteTimeout` przerywa odczyt odpowiedzi na poziomie
  socketu, więc skrypt **nigdy nie wisi**, a po `WebExceptionStatus.Timeout` przechodzi do weryfikacji GET.
  W praktyce na czystym POST połączenie **domyka się** i body zwraca **nowe ID** (np. tag_id, news_id) —
  twardy deadline jest zabezpieczeniem na wypadek zwisu. **To jest zalecany wzorzec zapisu webapi na tym
  hoście.** Implementacja: `scripts/shoper-api/blog-publish-01.ps1` (funkcja `Invoke-WriteWithDeadline`).

### URL wpisu bloga (permalink) — flagi konfiguracji + oficjalna dok.

- ✅ **PRODUKCJA `sklep.plasmet.pl` — POTWIERDZONE 2026-07-16:** wpis z ustawionym `seo_url` żyje pod
  **`https://sklep.plasmet.pl/<seo_url>`** (slug w ROOCIE domeny, bez żadnego prefiksu) — to jest canonical
  strony wpisu i zwraca HTTP 200 (zweryfikowane na 24 wpisach). **`/pl/news/<seo_url>` zwraca 404** (lub
  zrywa połączenie — pułapka pomiarowa jak przy `.xml`) — **NIE budować linków w tym formacie**, mimo że
  stare wpisy logu publikacji go niosą. Krótki URL `/pl/n/<news_id>` działa (200) i canonicalem wskazuje
  root-slug. Linki wewnętrzne w treściach buduj ZAWSZE jako `https://sklep.plasmet.pl/<seo_url>`.
- Wzorzec (Shoper Learn, zalecany SEO): **`/:lang/blog/:newsName/:newsId`** (np. `/pl/blog/Tytul-wpisu/2`).
  Stary namespace używa litery **`n`**: `/pl/news/<slug>-<id>` lub `/pl/n/<id>`.
- Sterują tym pola `application-config` (READ-ONLY przez webapi — zmiana tylko w panelu
  **Wygląd i treści > Blog > Ustawienia bloga > SEO**):
  - `blog_use_new_url_namespace` — na koncie TEST = **`0`** (stary namespace). Na produkcji **włączyć**
    nowy namespace dla czystych URL `/pl/blog/...` (decyzja SEO przed startem; potem 301 jeśli zmiana).
  - `blog_news_default_url_format` = `1`, `blog_category_default_url_format` = `2` (na TEST).
  - `blog_items_per_page` = 20 (paginacja listingu → istotne pod sitemap/paginację SEO).
- **`seo_url`** per-wpis nadpisuje slug → daje pełną kontrolę nad URL pod 301/linkowanie wewnętrzne.
- ⚠️ Front instancji TEST `sklep261208.shoparena.pl` **odrzuca zewnętrzne żądania HTTP** (połączenie
  zrywane) → realny URL renderowany potwierdzić dopiero na produkcji `sklep.plasmet.pl` (lub w panelu).

### Pipeline „partia + drip" (publikacja co 2 dni)

Kolejka wpisów: `blog/queue/*.json` (format w `blog/queue/_format.md`), log: `blog/published-log.json`.
Skrypt: `scripts/shoper-api/blog-publish.ps1` (**domyślnie `-DryRun`** = buduje payload, nie wysyła).
Kroki publikacji: tagi (find-or-create) → POST `/news` (`categories:[id]`) → **hero (`news-hero-upload.ps1`:
PUT `news/{id}` z `{image:<base64>, image_name:<alt>}` — GŁÓWNE zdjęcie, NIE `news-files`)** → zapis permalinku
do logu → status `opublikowany`. Throttling + retry/backoff (429/5xx) + idempotencja (po `tytul`/`news_id`
w logu; hero — sprawdź `image_name` niepuste lub PUT `image_name` SOLO → 200 = obraz już jest).
Hero można też podpiąć **od razu w POST `/news`** (`image`+`image_name` w payload tworzenia), bo to pola obiektu
`news`; w pipeline robimy to osobnym PUT po utworzeniu (potrzebny `news_id` do logu/idempotencji). `blog-publish.ps1`
wywołuje upload, jeśli w pliku kolejki jest `hero_image` (ścieżka) i plik istnieje; inaczej ostrzega i pomija.

## ✅ Strony informacyjne CMS — zasób `aboutpages` (NIE `pages`) — PRZEŁOM zweryfikowany na żywo 2026-06-10

**Strony informacyjne (storefront `/pl/i/<slug>/<id>`, np. „O firmie" `/pl/i/O-firmie/8`) to zasób
`aboutpages`, NIE `pages`.** Nazwa `pages` była błędna — stąd całe „Missing MODULE 'pages'" było
**pomyłką nazwy zasobu, a nie brakiem uprawnień**. Uprawnienie „Zawartość" na koncie webapi PLASMET jest
**pełne** (odczyt/dodawanie/edycja/usuwanie). Źródło nazwy: sitemap oficjalnej dok. Shopera (`#tag/Aboutpages`,
`developers.shoper.pl/.../resources/aboutpages/get`).

- **`GET /webapi/rest/aboutpages?limit=1`** → HTTP 200, na koncie PLASMET **`count=12`** stron informacyjnych
  (było 11 do 2026-08-12).
- **`GET /webapi/rest/aboutpages/{id}`** → pojedynczy rekord. `aboutpages/8` = **„O firmie"**.
- Inne strony (id→name): 1 Pytania i odpowiedzi, 2 Jak kupować?, 4 Czas i koszty dostawy, 5 Czas realizacji
  zamówienia, 7 Zwroty i reklamacje, 8 O firmie, 9 Kontakt i dane firmy, 10 Metody płatności, 12 Nagrody
  i wyróżnienia, 13 Regulamin sklepu, 14 Polityka prywatności,
  **16 Sklep dla instytucji i samorządów** (podstrona B2G, `seo_url=Dla-instytucji-i-samorzadow`,
  `active=1` od 2026-08-12, cel reguły wanity `/instytucje`).
- **AKTUALIZACJA 2026-07-15 (`aboutpages/7` „Zwroty i reklamacje"):** stara adnotacja audytu 2026-06-11
  „[active=0!]" (linia „Uzupełnienie 2026-06-11" niżej) jest **NIEAKTUALNA** — na żywo GET `aboutpages/7`
  = **`active=1`**, `seo_url=null` (slug auto = `Zwroty-i-reklamacje`), publiczny URL
  `https://sklep.plasmet.pl/pl/i/Zwroty-i-reklamacje/7` renderuje prawdziwą stronę (title „Zwroty i reklamacje
  - PLASMET sp. z o.o", H1 „Zwroty i reklamacje" — NIE miękkie 404). Treść to **natywny szablon Shopera**
  „Zwroty i reklamacje" (5440 zn. HTML): prawo odstąpienia 14 dni, link do portalu szybkich zwrotów
  `zwroty-shoper.pl`, link do PDF **„Formularz odstąpienia od umowy" już hostowany na CDN Shopera**
  (`regulaminy.saasecommerceapps.com/pdf/formularz_odstapienia_od_umowy.pdf` — upload własnego PDF zbędny),
  adres zwrotów/reklamacji przez placeholdery `{shop_*}`, polityka zwrotu i procedura reklamacji. Bramka
  cutoveru G9 = **domknięta**. Żaden PUT nie był potrzebny (weryfikacja READ-ONLY). Skrypt:
  `scripts/shoper-api/zwroty-page7-recon.ps1`, backup: `backup/zwroty-page-7_backup_2026-07-15.json`.

### Realne pola rekordu `aboutpages` (GET — PŁASKIE, bez `translations`)

Rekord jest **PŁASKI** (jak `news`) — pola siedzą bezpośrednio na obiekcie, **NIE** w `translations.pl_PL`:
`page_id`, `name`, `content` (HTML), `lang_id`, `active` (0/1), `seo_title`, `seo_description`,
`seo_keywords`, `seo_url` (`null` → auto-slug). To wszystkie pola top-level GET.

### ⚠️ OGRANICZENIA ZAPISU przez webapi (zweryfikowane na żywo PUT-ami 2026-06-10, page 8)

PUT `aboutpages/{id}` zwraca zawsze **HTTP 200 / body `1`** — ale **nie wszystkie pola realnie się zapisują**:

| pole | zapis przez webapi | uwaga |
|---|---|---|
| `content` | ✅ **TAK** | HTML treści; **ALE patrz sanityzacja `<script>` niżej** |
| `seo_url` | ✅ **TAK** | potwierdzone markerem (zapisał się i odczytał) |
| `name` / `active` / `lang_id` | (zapisywalne — `name` celowo NIE ruszany w zadaniu „O firmie") | |
| **`seo_title`** | ❌ **NIE** | PUT 200, pole **ignorowane** — zostaje puste |
| **`seo_description`** | ❌ **NIE** | jw. |
| **`seo_keywords`** | ❌ **NIE** | jw. |

- **Pola SEO meta (`seo_title`/`seo_description`/`seo_keywords`) są efektywnie READ-ONLY przez webapi**
  dla `aboutpages`. Przetestowano **5 wariantów** nazwy/struktury — wszystkie 200, żaden nie zapisał:
  (A) płasko `seo_title`, (B) `translations.pl_PL.seo_*`, (C) płasko z `lang_id`, (D) `{seo:{title,…}}`,
  (E) `{meta_title,meta_description,meta_keywords}`, (F) `{title,description,keywords}`. → **meta title/desc/keywords
  strony informacyjnej ustawiaj w PANELU** (Wygląd i treści > Strony informacyjne > strona > zakładka SEO/Pozycjonowanie).
- **`<script>` jest WYCINANY z `content`** (sanityzacja HTML serwera). Potwierdzone sondą: `<script type="application/ld+json">…`
  ORAZ `<script>…` (bez type) → **oba usuwane** (zostaje sam pozostały HTML). Encjowany `&lt;script&gt;` przetrwa,
  ale renderuje się jako **widoczny tekst**, nie wykonywalny JSON-LD (bezużyteczne dla danych strukturalnych).
  → **JSON-LD na stronie informacyjnej NIE da się wstrzyknąć przez webapi w `content`.** Drogi alternatywne:
  (a) wkleić ręcznie w panelu w **trybie źródła HTML** edytora (WYSIWYG też może ciąć — sprawdzić „Podgląd źródła"),
  (b) globalny `<head>` motywu (panel: Dodatki i integracje > Integracje własne > Nagłówek `<head>`) z warunkiem na URL,
  (c) przez motyw (`shoper-cli`). Sam HTML treści (`<p>`, `<h2>`, `<ul>`, `<strong>` itd.) przechodzi bez problemu.
- **Render `<title>`:** motyw dokleja **sufiks nazwy sklepu** („ - PLASMET sp. z o.o") do `name` (fallback, gdy
  `seo_title` puste). META keywords ma auto-fallback motywu („<nazwa>,  sklep"). Bo `seo_*` niezapisywalne webapi,
  pełna kontrola `<title>`/meta tej strony jest tylko w panelu.
- **Wzorzec zapisu** = ten sam anti-„wiszący zapis" co `news`: `System.Net.HttpWebRequest` + `.Timeout` +
  `.ReadWriteTimeout` + `.KeepAlive=$false`. Na czystym PUT połączenie domyka się i zwraca `1`.
- **Front stagingu `sklep261208.shoparena.pl` ODPOWIADA** na zewnętrzne HTTP (HTTP 200) — weryfikację renderu
  da się zrobić bez panelu, dekodując odpowiedź jako UTF-8 (`RawContentStream` → `Encoding.UTF8.GetString`).
  Cache frontu odświeżał się natychmiast po PUT. (Uwaga: to inaczej niż instancja TEST `news`, gdzie front
  bywał odrzucany — `aboutpages` na froncie czytelny.)
- **Natywny JSON-LD strony:** motyw sam renderuje 6 bloków (OnlineStore ×3, BreadcrumbList, Article ×2) —
  to nie nasz pakiet Store+AboutPage. Nasz musi iść drogą panel/motyw (patrz wyżej).
- Skrypty: `aboutpages-recon-backup.ps1` (KROK 1-3: dostęp+backup+rozpoznanie pól), `build-payload.py`
  (buduje payload z pliku FINAL, waliduje JSON-LD), `write-aboutpages-8.ps1` (PUT pełnego pakietu + weryfikacja),
  `restore-final-content.ps1` (zapis samego BODY HTML), diagnostyka: `diag-seo-fields.ps1`,
  `diag-aboutpages-seofields.ps1`, `diag-seo-variants.ps1`, `diag-jsonld-content.ps1`, `check-frontend-jsonld.ps1`,
  `fetch-front-before.ps1`, `reset-seourl-null.ps1`. Backup rekordu: `backup/o-firmie-page-8_backup_2026-06-10.json`.

### ✅ POST / DELETE `aboutpages` DZIAŁAJĄ + pełna mapa sanitizera HTML (sonda na żywo 2026-08-12)

Kontrolowana sonda na stronie testowej (`active=0`, losowy slug, DELETE po teście; sklep wrócił do
`count=11`, URL testowy → 404). Skrypty: `sonda-sanitizer-aboutpages.ps1`, `sonda-sanitizer-markery.ps1`,
`sonda-put-html.ps1`, `sonda-diag-500.ps1`. Pełna tabela wyników: `docs/b2g/podstrona/sonda-sanitizer.md`.

- **`POST /webapi/rest/aboutpages` DZIAŁA** — HTTP 200, **body = nowe `page_id`** (bez „wiszącego zapisu"
  znanego z `news`). Payload minimalny: `{"name","content","lang_id":1,"active":0,"seo_url"}`.
  **`DELETE /webapi/rest/aboutpages/{id}` DZIAŁA** (200/`1`, rekord znika, front 404).
- **`seo_url` daje URL w ROOCIE domeny** (`https://sklep.plasmet.pl/<seo_url>`), a `/pl/i/<slug>/<id>`
  na niego przekierowuje — tak samo jak wpisy bloga.
- **Sanitizer `content` — co WYCINA (tag i zawartość znikają):** `<svg>`+`<path>`/`<circle>`, `<script>`
  (w tym `ld+json`), `<style>`, `<input>` (też `hidden`), `<picture>`, atrybuty `on*`,
  `href="javascript:"`, `loading="lazy"`, `download`, `type` na `<a>`, **komentarze HTML `<!-- … -->`**
  (uzupełnienie 2026-08-12), oraz z `<img>`: **`sizes`, `decoding`**.
  ⚠️ **KOREKTA 2026-08-12: `srcset` na gołym `<img>` PRZEŻYWA 1:1** (5/5 na stronie B2G, pełne listy `300w/600w`).
  Wcześniejszy zapis „`srcset` wycinany" dotyczył `srcset` wewnątrz `<picture>` (wycinany razem z tagiem).
  Responsywne obrazki na stronie informacyjnej robi się więc `<img src+srcset+width+height+alt>` (bez `sizes`).
- 🔴 **`<script>` w TEKŚCIE ucina resztę dokumentu.** Jeśli w wysyłanym `content` pojawi się literalny ciąg
  `<script>` (choćby w komentarzu/instrukcji, nie jako realny tag), sanitizer wywala WSZYSTKO od tego miejsca
  do końca — 40 182 zn. zapisało się jako 518 zn., HTTP 200/`1` bez ostrzeżenia (złapane przy wdrożeniu B2G).
  → Body wycinaj kotwicą na początku linii (`(?ms)^<div class="…">.*$`), a przed PUT-em **waliduj**, że nie
  zawiera `<script|<style|<svg|<form|<input|<textarea|<select|<button|<label`, i zawsze porównuj długość GET-em.
- **Co „rozpakowuje" (tag ginie, tekst zostaje):** `<form>`, `<details>`, `<summary>`, `<textarea>`,
  `<select>`/`<option>`, `<button>`, `<label>`. → **Formularza NIE DA SIĘ osadzić w `content`.**
- **Co przeżywa 1:1:** `<p>`, `<h1>`-`<h4>`, listy, `<table>` z `<thead>/<th scope>`, `<section>`,
  `<figure>`, `<blockquote>`, `<hr>`, `<div>`/`<span>` z `class`, **`data-*`**, `aria-*`, `role`,
  `tabindex`, `title`, `hidden`, **`target="_blank"` na `<a>`** (potwierdzone 8/8 na stronie 16,
  2026-08-12 — ale `rel` jest normalizowany do `rel="noreferrer"`), `<img>` z `width`/`height`,
  `<iframe>`, `<video>`, `<a href="mailto:…?subject=&body=">`
  (z `%`-encodingiem, `%0D%0A`), `<a href="tel:">`, polskie znaki UTF-8, **pusty `<div>` (mount-point)**.
- **Co MODYFIKUJE:** `id="x"` → **`id="user_x"`** (⚠️ kotwice i `data-target` się rozjeżdżają — pisz
  `href="#user_x"`), surowe `&` → `&amp;`, `rel="noopener nofollow"` → **`rel="noreferrer"`** (nofollow
  przepada), `<u>` → `<span style="text-decoration:underline">`, `<br>`/`<hr>` → self-closing, encje
  `&nbsp;/&quot;/&copy;/&ndash;` dekodowane do znaków, **atrybuty sortowane alfabetycznie**.
- **`style` inline = whitelista właściwości.** Przeżywają: `margin`, `padding`, `background(-color)`,
  `color`, `border(-left)`, `text-align`, `font-size`, `font-weight`, `line-height`, `width`, `height`,
  `float`, `overflow`, `align-items`, `display:flex|none`. **Wycinane:** `display:grid`,
  `grid-template-columns`, `gap`, `max-width`, `border-radius`, `box-shadow`, `position`, `z-index`,
  `flex-wrap`, `justify-content` → layout tylko klasami z motywu.
- **Front renderuje dokładnie to, co zwraca GET** (moduł `info_page_content`, `data-module-id=49`,
  `<section class="info-page-content fr-view resetcss grid-mobile-wrap">`); treść **nie jest** zagnieżdżona
  w `<form>` motywu; motyw dorabia JSON-LD `Article` z `description` = tekst treści.

### 🔴 PUŁAPKA POWERSHELL: `Get-Content -Raw` + `ConvertTo-Json` → HTTP 500 (dotyczy WSZYSTKICH zapisów)

`Get-Content` dokleja do stringa właściwości ETS (`PSPath`, `PSDrive`, `PSProvider`, `PSChildName`,
`ReadCount`). `@{content=$html} | ConvertTo-Json` serializuje wtedy **obiekt**
`{"content":{"value":"…","PSPath":"…","PSDrive":{…}}}` zamiast stringa → Shoper zwraca
**`500 server_error` i NIC nie zapisuje** (deterministycznie, 4/4 próby; zmyliło to sondę na 40 minut).
**Fix obowiązkowy: `[string](Get-Content ... -Raw -Encoding UTF8)`.** Dodatkowo `ConvertTo-Json -Depth N`
na takim stringu rozwija go w strukturę wielkości megabajtów (payload przechodzi jako 200, ale zapis jest
nieprzewidywalny) — do płaskich payloadów **nie używaj `-Depth`** i zawsze weryfikuj zapis GET-em.
⚠️ Pokrewna pułapka: skrypt `.ps1` bez BOM z polskimi znakami w kodzie psuje się w PS 5.1 (czyta ANSI) —
polski tekst trzymaj w osobnym pliku UTF-8 i wczytuj.

## Konfiguracja sklepu / SEO home (zweryfikowane na żywo 2026-06-08)

- **`GET /webapi/rest/application-config`** zwraca **pojedynczy obiekt** (NIE listę: brak `count`/`list`/`pages`)
  z konfiguracją sklepu. Istotne pola **danych firmy** (zasilają natywny JSON-LD `OnlineStore`/stopkę):
  `shop_name`, `shop_company_name`, `shop_email`, `shop_phone`, `shop_tax_id` (NIP), `shop_regon`,
  `shop_address_1`, `shop_address_2`, `shop_city`, `shop_zip_code`, `shop_province`, `shop_country`,
  `shop_full_address`, `shop_trade`, `shop_url`, `technical_url`, `is_facebook`, `is_mobile`,
  `storefront_enabled`, `warehouses_enabled`. Dalej: domyślne produktu (`product_defaults_*`),
  zakupy (`shopping_*`), rejestracja, wyszukiwarka (`product_search_*`), blog (`blog_*`), locale.
- **`application-config` jest READ-ONLY przez webapi** — `PUT` i `POST` zwracają **HTTP 501 Not Implemented**
  (zweryfikowane PUT-em idempotentnym `shop_country="PL"` na koncie TEST `sklep261208`). Danych firmy ani
  `shop_name` **nie da się zmienić przez webapi** → tylko **panel: Ustawienia > Dane sklepu** (zasila to
  JSON-LD `OnlineStore` ×3). Webapi tu służy wyłącznie do **odczytu/weryfikacji** stanu.
- **Brak zasobu konfiguracji do zapisu** — próby `config`, `option`, `options`, `configuration`, `shop`,
  `metafields`, `seo` zwracają **HTTP 400** (Missing MODULE / nie istnieją). Nie ma w webapi pól
  **meta title/description strony głównej** — to ustawienie **panelowe**: `Ustawienia > Zaawansowane > SEO >
  Ustawienia podstawowe` (osobne meta dla strony głównej; placeholder domyślny „Twój sklep internetowy").
- **Własny kod w `<head>` (JSON-LD WebSite/SearchAction, OG/Twitter, `<link rel=preload>`)** — webapi tego
  NIE obsługuje. Panel: **Dodatki i integracje > Integracje własne** (a.k.a. „Inne własne") → pole
  **„Nagłówek strony `<head>`"** (oraz „Stopka strony"). To samo miejsce, gdzie wkleja się GTM/GA4.
- Rozeznanie konfiguracji: `scripts/shoper-api/rozeznanie-config-seo.ps1` (TYLKO GET; zrzut nazw pól bez
  wypisywania wartości/PII).

## ⛔ `robots.txt` i `sitemap.xml` — NIE MA ich w webapi (zweryfikowane na żywo 2026-07-14, po cutoverze domeny)

- **Brak zasobu webapi dla robots/sitemap.** Sonda GET (wszystkie → HTTP 400 „Missing MODULE"):
  `robots`, `robotstxt`, `robots-txt`, `sitemap`, `sitemaps`, `google-sitemap`, `seo`, `seo-config`,
  `config`, `configs`, `configuration`, `settings`, `shop`, `shops`, `domains`, `domain`, `shop-domains`,
  `urls`, `integrations`, `integration`, `application`, `applications`. (`metafields` → HTTP 500.)
  Istnieją tylko: **`application-config`** (READ-ONLY, PUT/POST → 501) i **`application-version`**.
  → **robots.txt edytuje się WYŁĄCZNIE w panelu:** `Ustawienia > Zaawansowane > SEO` → zakładka
  **„Zaawansowane"** (starsze nazewnictwo panelu: `Konfiguracja > Marketing > Pozycjonowanie > Zaawansowane`).
  Sitemapa: ta sama sekcja SEO → zakładka **„Google Sitemap"** (treści sitemapy nie da się edytować).
- **Base URL sklepu = `application-config.shop_url`** (po cutoverze: `https://sklep.plasmet.pl`).
  `technical_url` = domena techniczna (`…shoparena.pl`) i **zostaje na stałe** (przez nią loguje się panel,
  od 5.20.20 to jedyna droga logowania) — jej obecność w konfiguracji **nie jest** ogonem cutoveru.
- **`robots.txt` jest plikiem STATYCZNYM** (`Server: DCSaaS/httpd`, `ETag`, `Last-Modified` — nie PHP),
  **jeden dla obu hostów** (identyczna treść serwowana z domeny technicznej i produkcyjnej; linia `Sitemap:`
  ma **twardo zapisany host**, nie host żądania). Po cutoverze domeny platforma **regeneruje go z opóźnieniem**
  (2026-07-14: `Last-Modified` = dzień cutoveru, host w `Sitemap:` sam zmienił się na produkcyjny). ⚠️ Jeśli po
  zmianie domeny robots wskazuje stary host — **najpierw sprawdź `Last-Modified` + cache-buster**, zanim uznasz
  to za błąd konfiguracji; dopiero potem panel.
- **`/sitemap.xml` NIE ISTNIEJE na Shoperze** (HEAD → **404**). Sitemapa żyje wyłącznie pod URL-em integracji:
  **`/console/integration/execute/name/GoogleSitemap`** (HTTP 200, `sitemapindex`, `Content-Type:
  application/force-download`). Ten URL podaje się w `robots.txt` i w GSC. ⚠️ **Pułapka pomiarowa:** GET na
  nieistniejący plik `.xml` na tym serwerze **zrywa połączenie** (klient widzi „timeout / HTTP 0", nie 404) —
  kontrola: `/nieistniejacy-plik.xml` zachowuje się identycznie, a **HEAD** na tych samych URL-ach zwraca czyste
  **404**. Nie myl tego z awarią sitemapy.

## ⚠️ Ogon cutoveru: twardy host techniczny w treściach (skan READ-ONLY 2026-07-14)

Po zmianie domeny **treści zapisane wcześniej niosą stary host** (`sklep261208.shoparena.pl`) i **żaden
mechanizm platformy ich nie przepisuje** — przekierowania 301 tylko maskują problem. Pełny skan webapi:

| zasób | przeskanowano | trafień hosta technicznego |
|---|---|---|
| `products` (name/description/short_description) | 7 810 | **0** |
| `categories` | 285 | **0** |
| `aboutpages` | 11 | **0** |
| `producers` | 51 | **0** |
| `news-categories` | 3 | **0** |
| `redirects` `type=0` (target tekstowy) | 0 reguł | **0** (cała mapa 8 210 to `type=1/2/4` + `object_id`) |
| feed Merchant (`GoogleProductSearch`) | 7 8xx poz. | **0** (`<link>` z hostem produkcyjnym) |
| **`news` (blog)** | 38 | 🔴 **38 wpisów / 468 wystąpień, wyłącznie w polu `content`** → ✅ **WYCZYSZCZONE 2026-07-16** (patrz niżej) |

- **Blog to jedyne miejsce wycieku** (wpisy generowane pipeline'em z twardymi URL-ami): linki wewnętrzne
  `<a href="https://sklep261208…/pl/c/…">` **oraz JSON-LD** (`@id` Organization/BlogPosting/FAQPage, `url`, `logo`).
  JSON-LD wskazujący inny host niż canonical = niespójność encji dla Google; linki wewnętrzne idą przez 301.
- **Fix jest w webapi** (`news.content` jest zapisywalny, JSON-LD w nim przeżywa 1:1): `PUT /news/{id}`
  z `{content}` po podmianie stringa hosta. Skrypt: **`scripts/shoper-api/fix-news-host-shoparena.ps1`**
  (domyślnie `-DryRun`; backup rekordu przed PUT; weryfikacja GET-em; `-Only <id>` do testu jednostkowego;
  wzorzec anti-„wiszący zapis"). Dry-run (wpis 8): 12 → 0 wystąpień, `content` -96 zn. (12 × 8 zn. = spójne).
- ✅ **DOMKNIĘTE 2026-07-16 (zadanie „linkfix"):** pełna naprawa martwych linków we WSZYSTKICH 40 żywych
  wpisach (staging + `/pl/news/`=404 + martwe logo/hero w JSON-LD + absolutyzacja relatywnych) — finalny skan
  40 wpisów: **0 wystąpień** wszystkich złych wzorców. Skrypty: `linkfix-news-recon.ps1` (backup+zrzut),
  `linkfix-news-apply.ps1` (PUT tylko `{content}`); backup: `_backup-news-linkfix-2026-07-16.json`.
  Szczegóły i nowe fakty techniczne → „Metadane weryfikacji" (2026-07-16 LINKFIX).

## ✅ Przekierowania 301 — zasób `redirects` — TEST FIDELITY zweryfikowany na żywo 2026-06-11 (host TEST `sklep261208`)

**Silnik 301 Shopera dopasowuje stary format URL Mercatum z rozszerzeniem `.html` i strzela poprawny 301.**
To było główne pytanie strategii masowego 301 — **POTWIERDZONE empirycznie** (4 reguły, 4× PASS).

### Pola obiektu `redirects` (potwierdzone POST-em + GET-em + oficjalną dok.)

| pole | typ | uwagi |
|---|---|---|
| `redirect_id` | string (liczba) | PK; nadawany przy POST (POST zwraca samo ID w body, np. `1`) |
| `route` | string | **stary, względny URL źródłowy** (np. `/produkty/.../xxx.html`); to po nim silnik dopasowuje |
| `target` | string | nowy URL **tekstem** — wypełniane **TYLKO dla `type=0`**; dla `type=1-6` zostaje puste |
| `type` | int | **0**=własny URL (`target`), **1**=produkt, **2**=kategoria, **3**=producent, **4**=strona informacyjna (`aboutpages`), **5**=wpis bloga (`news`), **6**=kategoria bloga |
| `object_id` | int | ID obiektu docelowego — **TYLKO dla `type=1-6`**; dla `type=0` puste |
| `lang_id` | int | język; `1` = polski |

- **Minimalny payload POST:** `type` + `route` + `lang_id` + (`object_id` dla 1-6 **albo** `target` dla 0).
- **REKOMENDACJA dla mapy PLASMET:** `type=1`/`object_id` (produkt) i `type=2`/`object_id` (kategoria),
  **nie** `type=0`/`target` — cel śledzi obiekt po ID, więc 301 jest **odporny na zmiany slugów przez Leo**
  (gdy Leo przegeneruje permalink produktu, ID zostaje, więc reguła nadal kieruje poprawnie).
- **Idempotencja:** przed POST sprawdź, czy `route` już istnieje (GET `redirects`, paginacja po `pages`,
  `limit=50`) — nie duplikuj. Na starcie konta TEST było `count=0`.
- **Wzorzec zapisu** = ten sam anti-„wiszący zapis" co `news`/`aboutpages`: `HttpWebRequest` + `.Timeout` +
  `.ReadWriteTimeout` + `.KeepAlive=$false`. Na czystym POST `redirects` połączenie domyka się szybko
  i body zwraca nowe `redirect_id` (inaczej niż POST `news`, który potrafił wisieć).

### Wynik testu fidelity (2026-06-11, `redirect_id` 1-4 na koncie TEST — JEDNORAZOWE, do skasowania w panelu)

| reguła | type/object_id | route (stary Mercatum) | HTTP | Location | follow | PASS |
|---|---|---|---|---|---|---|
| R1 produkt | 1 / 93 | `/produkty/.../01wkcs8400-...-8x400mm.html` (REAL) | **301** | `/pl/p/SCHARF-WKRETY-.../93` | 200 | ✅ |
| R2 produkt | 1 / 94 | `/produkty/.../01ko08040-...-kpx-8x40.html` (REAL) | **301** | `/pl/p/KOSZULKA-KOLEK-.../94` | 200 | ✅ |
| R3 kategoria | 2 / 61 | `/produkty/elektronarzedzia` (bez `.html`) | **301** | `/pl/c/Elektronarzedzia/61` | 200 | ✅ |
| R4 kontrolna | 0 / target | `/test-redirect-plasmet-301` (bez `.html`) | **301** | `/pl/c/Elektronarzedzia/61` | 200 | ✅ |

### Wnioski operacyjne dla masowego 301 (~8 200 reguł)

- **`.html` NIE jest problemem** — silnik dopasowuje route dosłownie (z rozszerzeniem i bez). Stary format
  Mercatum (`/produkty/<ścieżka>/<symbol>-...-<slug>.html` dla produktów, `/produkty/<ścieżka>` dla kategorii)
  jest przyjmowany 1:1 jako `route`.
- **Opcja „Przekierowania" (Ustawienia > Zaawansowane > Przekierowania) jest WŁĄCZONA na koncie TEST** —
  dowiedzione przez R4: reguła kontrolna `type=0` strzeliła 301, więc silnik działa (gdyby był wyłączony,
  ŻADNA reguła by nie zadziałała). ⚠️ `application-config` **nie eksponuje** tej flagi przez webapi
  (sprawdzone — brak pola `redirect*` w konfiguracji) → stan silnika **potwierdzaj reguł kontrolną type=0**,
  nie odczytem konfiguracji. Na produkcji `sklep.plasmet.pl` upewnij się, że opcja jest włączona.
- **Join po SKU działa** — kod produktu Shopera (`code`, np. `01WKCS8400`) odnajduje się dosłownie w starym
  URL Mercatum (`...01wkcs8400-01wkcs8400-...`, podwójny symbol w slugu). To pewna oś joinu stary↔nowy URL.
  Pułapka: slug w URL bywa dłuższy/inny niż symbol — matchuj po `code` (case-insensitive) jako podciągu URL,
  potem waliduj. Lista starych URL: `migracja/stary-sklep/url-produkty-2026-06-01.txt` (7938 URL).
- **Brak `pages`/cache problemu** — reguła działała natychmiast po POST (test po ~0.8 s).
- **Limity:** webapi throttluje — przy ~8 200 POST stosuj opóźnienie (≥200 ms), retry/backoff na 429/5xx,
  idempotencję po `route`. Oficjalny artykuł Shopera „Masowy import przekierowań 301 przez API" potwierdza
  ten scenariusz jako wspierany.
- Skrypty: `redirect-fidelity-step0-recon.ps1` (READ-ONLY rozeznanie + kandydaci), `redirect-fidelity-step3-test.ps1`
  (POST 4 reguł + test HTTP `AllowAutoRedirect=$false`).

### ✅ ROZSTRZYGNIĘTE: `route` z procent-kodowaniem (`%20`, `%5B`) DZIAŁA — ale webapi ZAPISUJE route ZDEKODOWANY (zweryfikowane na żywo 2026-07-14, produkcja, 1 reguła SDS)

**Werdykt: percent-encoding w `route` jest BEZPIECZNY — plany 301 z `%20`/`%5B` wgrywaj as-is, bez przebudowy.**

Mechanizm (dwa niezależne dekodowania, oba działają):

1. **Zapis: webapi URL-DEKODUJE `route`.** POST `/redirects` z
   `route = /_data/attachments/07bsnb/SDS%20DEN_BRAVEN%20SILICONE_NAF_KOLORY%202022.pdf` → HTTP 200,
   ale **GET zwraca `route` ZE SPACJAMI**: `/_data/attachments/07bsnb/SDS DEN_BRAVEN SILICONE_NAF_KOLORY 2022.pdf`.
   → route **NIE jest zapisany 1:1** (inaczej niż `*`, które przechodzi bez zmian).
2. **Dopasowanie: silnik też dekoduje request** → URL wołany z `%20` **trafia** w zapisany route ze spacją.

Wynik na żywo (reguła 8214, `type=1` → produkt 2776, 123 kliki GSC):

| URL wołany | HTTP |
|---|---|
| `…/SDS%20DEN_BRAVEN%20SILICONE_NAF_KOLORY%202022.pdf` (forma z indeksu Google) | ✅ **301** → `/pl/p/…/2776` → **200** |
| `…/SDS+DEN_BRAVEN+…+2022.pdf` (plusy zamiast `%20`) | ✅ **301** (plus też dekodowany do spacji) |
| `…%202022.pdf?srsltid=TEST789` | 🔴 **404** (brak `*` — zgodne z pułapką query stringa niżej) |

**Potwierdzenie krzyżowe na mapie głównej (już żywej):** reguły z `%5B…%5D` (nawiasy w slugu taśm, np.
`…-5cmx20m-%5Bsa51l%5D.html`) zostały zapisane ze zdekodowanymi `[` `]` — i **działają** (curl z `%5B` → 301 → 200).
Ten sam mechanizm, kilkaset żywych reguł.

#### 🔴 PUŁAPKA IMPORTU MASOWEGO: dekodowanie ROZWALA IDEMPOTENCJĘ po `route`

Skrypt importu porównuje `route` z planu (**encoded**, `%20`) z `route` ze sklepu (**decoded**, spacja)
→ **nigdy nie trafi** → uzna regułę za nieistniejącą i **utworzy DUPLIKAT** przy każdym ponownym biegu.
Dotyczy każdego route z percent-encodingiem (w planie GSC: **114 wierszy**, w tym cały bucket SDS).
**Fix (wdrożony w `redirects-301-apply.ps1`):** klucz porównania = `[Uri]::UnescapeDataString(route).ToLower()`
po **obu** stronach (+ forma surowa jako bezpiecznik). Zweryfikowane dry-runem: po fixie importer poprawnie
rozpoznaje wgraną regułę SDS jako istniejącą (`juz istnieja: 1`), przed fixem widział `0`.
⚠️ Log wznowienia (`_301/apply-log*.jsonl`) trzyma route **z planu** (encoded) — też normalizowany tym samym kluczem.

#### ⏳ Niezweryfikowane (reszta): percent-encoding znaków **wielobajtowych** (`%C5%BA` = ź, `%C5%82` = ł)

Testowaliśmy `%20` (spacja) i `%5B` (nawias) — **jednobajtowe ASCII**. Znaki polskie w URL-ach SDS
(`gwo%C5%BAdzie%20czarne%202,8.pdf`) to **UTF-8 wielobajtowy** — dekodowanie powinno być tym samym `urldecode`,
ale round-trip przez charset bazy **nie był potwierdzony**. Skala: **25 wierszy planu SDS** (~55 klików GSC).
→ Rollout SDS puszczaj as-is, a potem **zweryfikuj te 25 reguł curlem (READ-ONLY)**; jeśli 404, wgraj je
ponownie z route **zdekodowanym** (dosłowne `ź`/`ł` w polu `route`) — wariant `-Variant decoded`
w `redirect-test2-sds.ps1`.

### 🔴 PUŁAPKA: reguła BEZ gwiazdki NIE łapie URL-i z query stringiem (`?srsltid`, `?gclid`, `utm`) — i FIX gwiazdką (zweryfikowane na żywo 2026-07-14, produkcja)

**Problem (realnie tnie ruch płatny i Shopping):** reguła `redirects` z „gołym" `route` dopasowuje **exact-match po
pełnym URL łącznie z query stringiem**. Skutek: stary, zaindeksowany URL Mercatum **z jakimkolwiek parametrem**
dostaje **twardy 404** zamiast 301 — a Google Merchant/Shopping automatycznie doklejają **`srsltid`**, a Google Ads
**`gclid`**. Klient klika reklamę → ląduje na 404, mimo poprawnej reguły 301.

Baseline na produkcji (produkt 1909, reguła 7555 bez gwiazdki):

| URL | HTTP |
|---|---|
| `/produkty/.../01klinspf1_5-…-5szt.html` | **301** → `/pl/p/…/1909` (200) |
| ten sam + `?srsltid=…` | 🔴 **404** |
| ten sam + `?test=123` | 🔴 **404** (nie chodzi o `srsltid` — o JAKIKOLWIEK parametr) |

Natywne URL-e Shopera (`/pl/p/…/1909?test=123`, home `?utm_source=…`) obsługują query string normalnie (200)
→ wada jest **izolowana do mechanizmu dopasowania w `redirects`**.

**✅ FIX: `*` na końcu `route` — webapi PRZYJMUJE gwiazdkę i to DZIAŁA.** (Oficjalny artykuł Shoper Learn
„Przekierowania 301" opisuje `*` tylko od strony panelu: *„przekierowanie podanego adresu URL i wszystkich jego
odmian występujących po znaku `*`"* — **że webapi przyjmie `*` w `route`, potwierdziliśmy empirycznie.**)

- **POST `/redirects`** z `route` = `…-5szt.html*`, `type=1`, `object_id=1909`, `lang_id=1` → **HTTP 200**,
  nowe `redirect_id` w body (8213). **Gwiazdka zapisuje się 1:1** — GET zwraca `route` zakończony `*`
  (zero sanityzacji/obcinania). Payload i wzorzec zapisu **identyczne jak dla reguły zwykłej**.
- **Wynik na żywo po dodaniu reguły z `*` (curl.exe, produkt 1909):**

| wariant | przed | po |
|---|---|---|
| bez parametru | 301 → 1909 | ✅ **301** → 1909 → 200 (brak regresji) |
| `?srsltid=…` | 🔴 404 | ✅ **301** → 1909 → **200** |
| `?test=123` | 🔴 404 | ✅ **301** → 1909 |
| `?utm_source=google&gclid=…` | 🔴 404 | ✅ **301** → 1909 |

- **Semantyka `*` (scharakteryzowana na żywo):** dopasowanie **prefiksowe na granicy ścieżki/query**, nie „dowolne
  znaki":
  - `…5szt.html?cokolwiek` → **301** ✅ (query string — o to chodziło)
  - `…5szt.html/extra-segment` → **301** (sufiks ścieżki też łapie)
  - `…5szt.htmlZZZ` → **404** ❌ (NIE dokleja się w środku segmentu → **nie ma ryzyka over-matchu** na sąsiednie
    produkty o wspólnym prefiksie)
- **Współistnienie reguł:** reguła z `*` (8213) i istniejąca bez `*` (7555) na tej samej ścieżce **żyją obok siebie
  bez konfliktu** — brak błędu przy POST, oba przypadki (z parametrem i bez) kierują na właściwy obiekt 1909.

#### ✅ ROZSTRZYGNIĘTE: reguła z `*` SAMA obsługuje TEŻ URL bez parametru → mapę się PRZEPISUJE, nie dokłada (zweryfikowane na żywo 2026-07-14, reguła 8212)

**Werdykt: `*` NIE jest „tylko dla wariantów z ogonem" — reguła z gwiazdką obsługuje pełen zakres
(URL goły + URL z query stringiem).** Czyli istniejące reguły można **PRZEPISAĆ** (PUT, dopisanie `*`),
bez podwajania mapy do ~16 tys.

Test na regule **8212** (alt-ścieżka tego samego produktu 1909, jedyna reguła pokrywająca tę ścieżkę —
potwierdzone pełnym skanem 8 212 reguł, więc **brak confounda**):

| wariant alt-ścieżki | przed (bez `*`) | po PUT (route z `*`) |
|---|---|---|
| bez parametru | 301 → 1909 | ✅ **301** → 1909 → 200 (**zero regresji** — to było pytanie testu) |
| `?srsltid=TEST789` | 🔴 404 | ✅ **301** → 1909 → 200 |
| `?gclid=…&utm_source=google` | 🔴 404 | ✅ **301** → 1909 |
| `…html` **ZZZ** (doklejone w segmencie) | 404 | ✅ **404** (brak over-matchu — granica segmentu trzyma) |

- **`PUT /webapi/rest/redirects/{id}` DZIAŁA** (wcześniej nietestowane — znaliśmy tylko POST). Payload jak w POST
  (`route`+`type`+`object_id`+`lang_id`), HTTP **200**, body `1`, `route` nadpisany, `redirect_id` zachowany.
  → Przepisanie mapy = **8 212 PUT-ów**, mapa zostaje tej samej wielkości (żadnych nowych ID, żadnych duplikatów).
- **Gwiazdka zapisuje się 1:1** (bez sanityzacji) — inaczej niż percent-encoding, który webapi dekoduje (patrz wyżej).
- **Higiena mapy (skan 2026-07-14):** 8 212 reguł, **0 duplikatów `route`**, 2 reguły z `*` (8212, 8213).
- ⚠️ **Filtr `?filters={"route":{"~":"…"}}` na `redirects` NIE DZIAŁA** (zwraca `count=0` mimo istniejących trafień,
  bez błędu) → nie polegaj na nim przy idempotencji/wyszukiwaniu; **paginuj całą listę** (`redirects-scan-dupes.ps1`).
- **Kontrola poprawności eksperymentu:** ścieżka ALT tego samego produktu (reguła 8212, **bez** `*`) z parametrem
  **nadal zwraca 404** → dowód, że poprawę daje **reguła**, a nie jakaś globalna zmiana zachowania platformy.
- **Location gubi query string** (`?srsltid` nie jest przenoszony do celu) — dla `srsltid`/`gclid` to bez znaczenia
  dla klienta (ląduje na produkcie); atrybucja Ads i tak działa na docelowym URL-u przez `gclid` w sesji tylko jeśli
  parametr przetrwa → **przy `gclid` warto to zmierzyć osobno przed rolloutem na kampanie**.
- **Skrypt:** `redirect-wildcard-test.ps1` (domyślnie DRY-RUN; `-Apply` = POST reguły z `*`, `-Delete <id>` = rollback).

#### 🔴 TWARDA GRANICA: `*` WOLNO dopisać TYLKO do reguł `type=1` (produkt). NIGDY do `type=2` (kategoria) ani `type=4` (CMS)

**Powód (potwierdzony oficjalną dokumentacją Shopera):** route kategorii jest **PREFIKSEM** route'ów produktów
leżących w tej kategorii:

```
type=2  /produkty/technika-zamocowan                                  <- kategoria (id 258 -> obj 39)
type=1  /produkty/technika-zamocowan/wkrety/.../01wkcs8400-...html    <- produkt   (id 1   -> obj 93)
```

Gwiazdka na regule kategorii złapałaby **wszystkie produkty tej gałęzi** i przekierowała je na kategorię
zamiast na kartę produktu (utrata trafności = utrata SEO/konwersji). To **nie jest teoria** — Shoper Learn
(„Przekierowania 301") podaje dokładnie ten scenariusz jako **intencjonalne zastosowanie** `*`: *„jeśli admin
usunął kategorię i chce przekierować wszystkie adresy URL, jakie mogą wystąpić po nazwie kategorii, na nową
kategorię"*. Czyli wildcard na kategorii **z definicji** zagarnia całe poddrzewo.
⚠️ **Pierwszeństwo reguł (dokładna vs wildcard) NIE jest przetestowane** — nie zakładaj, że reguła dokładna
wygra z wildcardem. Dlatego `type=2`/`type=4` zostają **exact-match**, bez `*`.

- **Konsekwencja (znana, świadoma luka):** reguły `type=2` **nie łapią URL-i z query stringiem** → stary URL
  kategorii z `?srsltid`/`?gclid` nadal daje 404. To akceptowany koszt bezpieczeństwa.
- ⚠️ **DOPRECYZOWANIE 2026-08-10:** granica przebiega nie po `type`, tylko po **kształcie route'a**. Zakaz dotyczy
  reguł, których route **jest prefiksem innej reguły** (realne ścieżki drzewa kategorii — 257 z 1 460 reguł `type=2`).
  Pozostałe reguły `type=2`/`type=4` (route produktowe `.html` celujące w kategorię-fallback, forma pojedyncza
  `/produkt/<slug>`, pliki SDS `.pdf`, strony CMS) **nie są prefiksem niczego** → gwiazdka jest tam dowodliwie
  bezpieczna (**1 217 reguł**). Analiza + lista: `migracja/przekierowania/gwiazdki-bezpieczne-2026-08.{csv,md}`,
  skrypt `scripts/shoper-api/redirects-star-safety-scan.ps1`. Każdy skrypt zapisujący MUSI działać z listy
  `redirect_id` z tego CSV (nie z filtra po `type`).
- **Egzekwowane w kodzie:** `redirects-wildcard-rewrite.ps1` filtruje twardo po `type=1`, ma asercję w pętli
  (PUT na `type!=1` → przerwanie) i **odrzuca kandydatów, których route jest prefiksem innej reguły**
  (na granicy `/` lub `?`) — dodatkowy bezpiecznik anty-over-match.

#### Dodatkowe parametry `route` z oficjalnej dok. (nieużywane u nas — pod bucket listingów/paginacji)

Poza `*` reguła `redirects` przyjmuje w adresie źródłowym placeholdery:
**`{page}`** (element paginacji), **`{sort}`** (sortowanie), **`{view}`** (typ widoku).
→ To jest właściwe narzędzie dla **bucketu 4 z GSC** (listingi z parametrami), którego jeszcze nie robiliśmy.

> **Recon READ-ONLY 2026-07-07 (inwentaryzacja pod tytuły):** potwierdzono na żywo — katalog `products`
> **count=8013** (161 stron przy limit=50). ⚠️ **Pułapka nazw:** nazwa **producenta** = pole **TOP-LEVEL `name`**
> (np. „BUD-MET GROUP…"), a `producers.translations.pl_PL.name` jest **PUSTE**; nazwa **kategorii** odwrotnie —
> w **`translations.pl_PL.name`**, top-level `name` puste. `producers count=50`, `categories count=284`.
> **`producer_id` produktu bywa PUSTY** (np. prod. 156 = rękawice) → mapuj na „(brak producenta)". Skrypt
> inwentaryzacyjny (READ-ONLY, reużywalny): `scripts/shoper-api/inwentarz-tytuly-full.ps1`.

## ✅ Pola opisu produktu (`short_description` / `description`) — charakterystyka realnego katalogu (zweryf. na żywo 2026-06-12, READ-ONLY)

**WAŻNE odkrycie:** konto TEST `sklep261208` ma już wgrany **REALNY katalog PLASMET — `count=7938`** (a nie
demo-sukienki; te są tylko na producentach id 14–20). Producenci id 23–41 to prawdziwe marki (Bostik/Den Braven 30,
Awenta 34, Polifarb Kalisz 33, Richmann 36, Klingspor 29, Klimas Wkręt-met 41, Collomix 40, Baum 26,
Milwaukee=Techtronic 35, Sched-Pol 37). To dane z **Leo Synchronizator (Subiekt GT)** — stąd ich kształt.

Oba pola siedzą w **`translations.pl_PL`** (`short_description`, `description`). Statystyki (próba 600–766 prod.):

- **`short_description` niepuste: 100%.** ⚠️ ALE to **NIE jest opis produktu** — to **STAŁY blok GPSR per-marka**:
  `1. Producent<br/>…adres/email…<br/>2. Informacje o bezpieczeństwie<br/>…` (dane podmiotu odpowiedzialnego + CE).
  Powtarzalny dla całej marki, ~200–260 zn. **Nie nadaje się na „wycinek opisu" na karcie listy** (to metadane GPSR,
  nie marketing). Część rekordów zaczyna się od `Producent:` zamiast `1. Producent` (np. Sched-Pol).
- **`description` niepuste: ~95%** (94,7% na próbie 600). To **realny opis produktu**, HTML. ~83% zaczyna się od
  znacznika HTML; **0% ma format „1. Producent…"** (to NIE trafia do `description`); mojibake **0%** (UTF-8 czyste,
  ś/ż/ł/ą poprawne). Zanieczyszczenia: wiodące nagłówki `<p><strong>OPIS</strong></p>` + `<p><strong>MARKA</strong></p>`,
  u Milwaukee bloki `<b><span style='Arial-BoldMT'>`, u **Sched-Pol pełne śmieci MSHTML** (`<!DOCTYPE>` + `<META charset=windows-1250>`
  + `MSHTML 11…` — relikt windows-1250). Inline-style/`<span style=…>` częste.
- **Wykonalność „wycinka 1–2 zdań z `description`": ŁATWE/RYZYKOWNE pogranicze → realnie WYKONALNE.** Symulacja pipeline
  (usuń DOCTYPE/head/script/style/komentarze → `<br>`/`</p>`→separator → striptags → odrzuć wiodące nagłówki „OPIS"/marka
  → weź 1–2 zdania) dała **99,5% użytecznych snippetów (≥4 słowa)** na 766 prod., 0,1% pustych, 0,4% za krótkich.
  Ok. 5,5% snippetów zaczyna się od nazwy marki/„Dystrybutor …" (do dodatkowego odfiltrowania). Wniosek: pole `description`
  to dobre źródło wycinka; `short_description` (GPSR) świadomie pomijać. Skrypty diagnostyczne (READ-ONLY):
  `diag-opis-karta-readonly.ps1`, `diag-opis-firstsentence-readonly.ps1`.

## ✅ Masowa podmiana NAZW i OPISÓW produktu (`name`/`description`) — WYKONALNOŚĆ zweryfikowana testem 1-produktowym na żywo 2026-07-07

Pod projekt masowej podmiany nazw + opisów (~7 900 prod.). Test kontrolowany na produkcie **156** (tanie
rękawice, nie-Milwaukee): GET+backup → PUT `name+=" TEST"` i `description+=marker` → GET-porównanie → RESTORE.
Skrypty: `nazwy-opisy-recon.ps1` (READ-ONLY, statystyki+kandydat+próbki marek), `nazwy-opisy-permalink-test.ps1`
(test permalink + izolacji pól, `-DryRun` domyślnie), `nazwy-opisy-marker-set.ps1` (marker trwałości pod sync Leo).
Backup + wyniki: `backup/test-nazwy-opisy/` (`prod-156-before.json`, `permalink-test-result.json`, `marker.md`).

### ⚠️ PERMALINK ZMIENIA SIĘ przy zmianie `name` — ale `product_id` w URL zostaje stały (zweryfikowane empirycznie)

- Slug produktu jest **generowany z `name`** (gdy `seo_url` puste — a puste jest na CAŁYM katalogu z Leo).
  PUT `name` „RR RĘKAWICE… wampirki" → „…wampirki **TEST**" zmienił permalink
  `/pl/p/RR-REKAWICE-…-wampirki-/156` → `/pl/p/RR-REKAWICE-…-wampirki-**TEST**/156`. **Slug się zmienia.**
- **ALE `product_id` (156) na końcu URL jest NIEZMIENNY** i to on jest kanonicznym resolverem produktu.
- **Oficjalna pomoc Shoper (WebSearch 2026-07-07):** „zmiana nazwy produktu/kategorii/strony **automatycznie
  zmienia adres**, a Shoper **zakłada 301 ze starego adresu na nowy**". ⇒ zmiana nazwy nie tworzy „martwego" URL.
- **Wpływ na naszą mapę 301 Mercatum→Shoper = ZEROWY:** nasze reguły `redirects` są `type=1`/`type=2` z
  **`object_id`** (target puste) — celują w produkt/kategorię **po ID**, więc zmiana sluga ich nie psuje
  (potwierdzone GET-em: `redirects` id 1-2 `type=1 object_id=93/94`, id 3 `type=2 object_id=61`).
- **`seo_url` przy PUT `name` NIE zmienia się** (pozostaje puste — auto-slug). Gdyby ustawić `seo_url` ręcznie,
  slug byłby zablokowany na tej wartości (dźwignia do „zamrożenia" URL, gdyby kiedyś potrzebna).
- **Kontekst SEO cutoveru:** na razie sitemap=404 i 0 sprzedaży organicznej → nowe URL Shopera NIE są jeszcze
  zaindeksowane. **Podmiana nazw PRZED cutoverem ma praktycznie zerowy koszt SEO** (Google i tak dopiero
  zaindeksuje docelowe slugi; wewnątrz Shopera stary slug 301-uje na nowy po samym ID).

### ✅ PARTIAL-PUT `translations.pl_PL.{name, description}` NIE rusza innych pól (0 różnic)

Po PUT samego `name`+`description` porównano BEFORE/AFTER **wszystkie** pozostałe pola: `stock.price`, `stock.stock`,
`categories`, `category_id`, `main_image`, `attributes`, `bestseller`, `newproduct`, `is_product_of_day`,
`promo_price`, `unit_price_calculation`, `tax_id`, `stock.delivery_id`, `ean`, `code`, **`short_description`**,
`seo_title`, `seo_description` → **0 różnic (wszystkie nietknięte)**. Partial-PUT w `translations.pl_PL` **merge'uje**
podany podzbiór kluczy, reszta zostaje. To samo dotyczy pól top-level i `stock` (spójne z rolloutem `delivery_id`).
⇒ **bezpiecznie zapisywać wyłącznie `name` i/lub `description`**, nie ruszając cen/stanów/kategorii/flag.

### ⚠️ `description` = HTML z SANITYZACJĄ: komentarz `<!-- -->` JEST WYCINANY; `<span style>` przeżywa

- **`<!-- komentarz -->` znika** z `description` po PUT (470→po restore znów 470 zn., marker-komentarz usunięty).
  ⇒ **niewidocznego markera / notatki NIE trzymaj w komentarzu HTML** (zniknie). Inaczej niż `news.content`
  (gdzie `<script>` przeżywa) i inaczej niż surowy HTML body.
- **`<span style="display:none">…</span>` PRZEŻYWA** (Shoper normalizuje `display:none`→`display:none;`, tekst
  zachowany). Zwykły HTML treści (`<p>`, `<b>`, `<strong>`, `<span style=…>`, `<br>`) przechodzi. UTF-8 (ś/ż/ł/„")
  czyste, **mojibake 0%**. Nazwa przyjęła spacje/cudzysłowy 1:1. ⇒ opisy pisz czystym HTML bez komentarzy.
- **Limit nazwy:** Shoper standardowo ~255 zn. (nie testowano granicy zapisem — trzymaj nazwy < 255).
  `name` bez sanityzacji problematycznej (cudzysłowy/spacje OK).
- **✅ `<a href target rel>` PRZEŻYWA w `description`, ale Shoper GO NORMALIZUJE — zweryf. na żywo 2026-07-07 (prod. 5991).**
  Wysłano `<a href="https://…/eservice/" target="_blank" rel="noopener">…</a>` → zapisano
  `<a href="https://…/eservice/" rel="noreferrer" target="_blank">…</a>`. **Zachowane:** tag `<a>`+`</a>`, pełny `href`,
  `target="_blank"`, tekst kotwicy (link klikalny i poprawny). **Zmienione przez Shoper:** `rel="noopener"` →
  **`rel="noreferrer"`** (przepisanie atrybutu) + **zmiana KOLEJNOŚCI atrybutów** (href, rel, target).
  `noreferrer` implikuje `noopener` w przeglądarkach → bezpieczeństwo równoważne. ⇒ przy zapisie linków w `description`
  **nie zakładaj bit-w-bit `rel`/kolejności atrybutów** — Shoper je porządkuje; href/target/tekst są pewne.
  ⚠️ **Skutek dla weryfikacji zapisu przez `String.Contains`:** porównuj href/tekst/`target`, NIE cały ciąg `<a …>`
  (przestawiona kolejność atrybutów da fałszywy negatyw). Append bloku na koniec `description` = partial-PUT
  `description` = descBefore + "\n\n" + blok (reszta opisu nietknięta, prefix==descBefore potwierdzony).

### 📊 Statystyka `description` (próba 300 prod., po zdjęciu HTML)

- **puste: 4,0%** (12/300) · **krótkie <300 zn.: 17,7%** (53/300) · **sensowne ≥300 zn.: 78,3%** (235/300) ·
  **mediana 552 zn.** ⇒ ~78% katalogu ma realny opis do **poprawy**, ~22% (puste+krótkie) do **napisania/rozbudowy**.

### ⛔ `short_description` = STAŁY BLOK GPSR — NIE RUSZAĆ przy podmianie opisów

Potwierdzone na 5 markach (2026-07-07): Milwaukee/Techtronic, Bostik/Den Braven, Klimas Wkręt-met, Flexa(EUBRIDGE),
Awenta — `short_description` = „**1. Producent … 2. Informacje o bezpieczeństwie …**" (dane podmiotu
odpowiedzialnego GPSR + CE, per-marka, ~180–260 zn.). To **metadane prawne GPSR z Leo/Subiektu, NIE opis
marketingowy** → przy masowej podmianie **pole `short_description` zostawić nietknięte** (zapisujemy tylko
`name` i `description`).

### ❗ Ryzyko Leo (do domknięcia nocnym syncem) — MARKER TRWAŁOŚCI ustawiony

User: Leo NIE aktualizuje `name`/`description` (poza kolumną „A-Aktualizacja"). **Z API tego nie da się
udowodnić w 100%** (webapi nie widzi konfiguracji mapowania pól Leo). Weryfikacja empiryczna: na produkcie 156
w `description` osadzono niewidoczny **`<span style="display:none">leo-marker-20260707</span>`**. **Po nocnym
syncu Leo** GET `products/156` → jeśli marker OBECNY = Leo nie nadpisuje opisu (masowa podmiana BEZPIECZNA);
jeśli marker ZNIKNĄŁ = Leo nadpisuje `description` (BLOKER — pisać u źródła w Subiekcie/Leo albo wykluczyć pole).
Analogiczne ryzyko dotyczyło `unit_id`/`order`/`delivery_id` (Leo potrafił nadpisać). Szczegóły: `marker.md`.

## ✅ Dostępność / sprzedaż przy zerowym stanie (OOS) — `availabilities` + `deliveries` + `stock.*` — zweryf. na żywo 2026-06-17 (READ-ONLY)

**Mechanizm „czy można kupić produkt" NIE jest polem produktu w webapi.** Produkt (`GET /products/{id}`,
pełny obiekt) **NIE ma** pól `can_buy`, `availability`, ani `delivery` (potwierdzone listą 38 kluczy
top-level: brak wszystkich trzech). Pola `can_buy` / „tymczasowo niedostępny" widoczne na FRONCIE i w panelu
pochodzą ze **STANU DOSTĘPNOŚCI** (`availabilities`), a NIE z flagi na produkcie. To kluczowa korekta założeń.

### Jak produkt dziedziczy dostępność (łańcuch danych)

- Na produkcie: `stock.stock` (ilość, może być ułamkowa) → Shoper **wylicza** `stock.calculated_availability_id`
  (np. `stock=0` → `calculated_availability_id=1`; `stock=3.25` → `2`; `stock=45` → `5`).
- `stock.availability_id` = **ręczne nadpisanie** dostępności (gdy ustawione, bije wyliczone). W PLASMET
  **PUSTE na całym katalogu** (`''`/null) — sonda `{"stock.availability_id":"6/7"}` → **count=0**. Czyli
  **każdy produkt jedzie na `calculated_availability_id` (automat ze stanu)**, nikt nie ma ręcznego statusu.
- `stock.delivery_id` = **ręczne nadpisanie terminu wysyłki** per produkt. W PLASMET też PUSTE.
- O tym, czy produkt **wpada do koszyka**, decyduje **flaga `can_buy` na REKORDZIE `availabilities`**, który
  jest aktualnie przypisany produktowi (czyli pośrednio: wyliczony ze stanu). To jest „przełącznik per stan
  dostępności" z panelu (Ustawienia > Produkty > Statusy dostępności).

### Zasób `availabilities` (słownik stanów dostępności) — `count=9`, z DUBLAMI Leo

Pola rekordu: **`availability_id`**, **`can_buy`** (`0`/`1` — CZY ZAMAWIALNY), **`notifier`** (`0`/`1` — formularz
„powiadom o dostępności"), **`ranges`** (`0`/`1` — czy auto-wyliczany z przedziału stanu), **`from`** (próg dolny
stanu dla przedziału; `-1`/`0`/`10`/`20`…), **`visibility_config`** (JSON: `status`/`search_status`/`cart_status`/
`flags`/`cart{gallery_and_name_gray, additional_text, link_behaviour}` — sterowanie wyświetlaniem karty), `photo`,
`translations.pl_PL.name`. Pełny słownik PLASMET (id | name | can_buy | ranges | from):

| id | name (pl_PL) | can_buy | ranges | from | uwaga |
|---|---|---|---|---|---|
| 1 | tymczasowo niedostępny | **0** | 1 | -1 | **stan ≤ 0 = TEN status** (próg `from=-1`); notifier=1; cart_status=1 (karta zostaje, ale bez zakupu) |
| 2 | średnia ilość | 1 | 1 | 0 | przedział od 0 (po wyczerpaniu specjalnego progu) |
| 3 | spodziewana dostawa | 0 | 0 | – | ręczny (ranges=0) |
| 4 | **średnia ilość (DUBEL)** | **1** | 1 | 10 | ⚠️ duplikat nazwy „średnia ilość" (Leo); `from=10` (inny próg niż id 2). **can_buy=1 od 2026-07-02** (wcześniej 0 — zmienione w panelu; potwierdzone GET) |
| 5 | duża ilość | 1 | 1 | 20 | |
| 6 | dostępny na zamówienie | **1** | 0 | – | **ZAMAWIALNY, ręczny — kandydat na „OOS ale do kupienia"** |
| 7 | wycofany z oferty | 0 | 0 | – | ręczny — dla realnie wycofanych |
| 8 | brak informacji | 0 | 0 | – | notifier=1 |
| 9 | trwale niedostępny | 0 | 0 | – | visibility: status=0/search=0 (ukryty na froncie) |

⚠️ **Dubel:** id 2 i id 4 to oba „średnia ilość" (Leo zdublował) — różnią się progiem `from` (0 vs 10); **oba mają can_buy=1** (id 4 od 2026-07-02).
⚠️ **`ranges`/`from` to przedziały automatu** (Shoper auto-przypisuje status wg progu stanu). Pole `default`
NIE występuje na rekordzie `availabilities` (jest `from`, które pełni rolę progu).

### ✅ AUDYT FEEDU pod Merchant Center — blanket `out_of_stock→backorder` BEZPIECZNY — zweryf. na żywo 2026-07-02 (READ-ONLY)

Pełny skan katalogu (`products` paginacja, count=**8008**, aktywne=**7815**) skryptem
`scripts/shoper-api/feed-oos-canbuy-audit-readonly.ps1`. Kontekst: reguła w GMC ma zamienić cały feedowy
`out_of_stock` na `backorder` (bo OOS PLASMET jest zamawialny). Pytanie: czy jakiś **aktywny** produkt
o statusie **can_buy=0** (id 3/7/8/9) trafia do feedu jako `out_of_stock`.

- **Ręczne nadpisanie `stock.availability_id` = 0 rekordów w CAŁYM katalogu** → każdy produkt jedzie na
  `calculated_availability_id` (automat ze stanu). To domyka logikę: automat przypisuje TYLKO statusy `ranges=1`
  (id 1/2/4/5), a statusy can_buy=0 (3/7/8/9, wszystkie `ranges=0`) są **nieosiągalne bez ręcznego override'a**.
- **Rozkład efektywnej dostępności wśród 7815 aktywnych:** status 1 = 2758, status 2 = 2732, status 4 = 744,
  status 5 = 1581 — **wyłącznie statusy can_buy=1**.
- **Aktywnych z efektywnym statusem can_buy=0 (3/7/8/9): 0.** Feedowy `out_of_stock` = aktywne + stock≤0 = **2758**,
  **wszystkie can_buy=1** (status 1 „Dostępny na zamówienie"). Produkty realnie wycofane PLASMET oznacza jako
  **nieaktywne** (`translations.pl_PL.active=0`, ~193 poz.) → wypadają z feedu, nie idą jako can_buy=0 OOS.
- **WERDYKT: blanket-override `out_of_stock→backorder` jest BEZPIECZNY** przy obecnym stanie. Niezmiennik do
  monitorowania: (a) `availability_id` override pozostaje pusty w katalogu; (b) Leo nie zaczyna nadawać statusów
  can_buy=0 aktywnym; (c) id 4 pozostaje can_buy=1. Jeśli którykolwiek pęknie — patrz reguła węższa niżej.

### Zasób `deliveries` (słownik TERMINÓW WYSYŁKI) — ISTNIEJE i DOSTĘPNY, `count=7`

> ⚠️ Pułapka sondy: `deliveries` zwraca **OK count=7**. Wcześniejsze „Missing MODULE '=1'" było **artefaktem
> złego sklejenia URL w pętli** (`?` gubione), NIE brakiem zasobu/uprawnień. `delivers`/`shippings`/`shipping-times`
> NIE istnieją — poprawna nazwa to **`deliveries`** (zgodna z `developers.shoper.pl/.../resources/deliveries/get`).

Pola rekordu: **`delivery_id`**, **`hours`**, **`days`**, **`translations.pl_PL.name`**. Słownik PLASMET
(id | name | days): 1 „24 godziny" (1), 2 „48 godzin" (2), 3 „3 dni" (3), 4 „4 dni" (4), 5 „5 dni" (5),
6 „10 dni" (10), 7 „14 dni" (14). **NIE MA etykiety „7 dni"/„do 7 dni"/„na zamówienie"** → trzeba ją UTWORZYĆ
(panel: Ustawienia > Produkty > Czas wysyłki > „Dodaj czas wysyłki"; nazwa np. „do 7 dni", `days=7`) albo użyć
istniejącej „10 dni". Termin wysyłki przypina się per produkt (`stock.delivery_id`) — w PLASMET wszędzie PUSTE.

### Mechanizm „zakup przy zerowym stanie" wg OFICJALNEJ dok. (pomoc.shoper.pl, zweryf. 2026-06-17)

- **Decyduje USTAWIENIE PER STAN DOSTĘPNOŚCI**, NIE globalny przełącznik ani pole produktu. Panel:
  **Ustawienia > Produkty > Statusy dostępności produktów** → klik na status przypisany do zerowego stanu
  (w PLASMET = id 1 „tymczasowo niedostępny") → sekcja **„Ustawienia dodatkowe"**: flaga „czy klient może
  zamówić produkt" (= pole `can_buy`) + tryb karty (aktywna z formularzem „Powiadom o dostępności" /
  wyszarzenie / „produkt niedostępny" / nieaktywna: 404/redirect).
- To wprost mapuje się na `availabilities.can_buy`. `can_buy=0` na id 1 = przyczyna blokady koszyka dla całego OOS.

### Dźwignie, by OOS stał się zamawialny z dłuższą dostawą (do potwierdzenia w panelu / NIE testowane zapisem)

1. **Przełączyć `can_buy=0→1` na statusie „tymczasowo niedostępny" (id 1)** — globalnie odblokuje koszyk dla
   CAŁEGO OOS (2 895 prod.). Najszybsze, ale nie rozróżnia „wróci w 7 dni" od „wycofane".
2. **Per-produkt: ustawić `stock.availability_id=6` („dostępny na zamówienie", can_buy=1) + `stock.delivery_id`
   = termin (np. nowy „do 7 dni")** dla tych OOS, które realnie wrócą; realnie wycofanym dać id 7/9. To czyste
   przez webapi (PUT na `stock`), ale ⚠️ **ryzyko Leo**: sync z Subiekta może nadpisać `availability_id`/stan.
3. **Czy `availabilities` jest zapisywalny przez webapi (PUT)** — ❌ **NIE (zweryfikowane 2026-06-18).**
   `PUT /webapi/rest/availabilities/{id}` zwraca **HTTP 500 `server_error` / „Internal server error" NIEZALEŻNIE
   od kształtu body** (przetestowano 7 wariantów idempotentnych `can_buy=0`: skalary int, `can_buy` solo int,
   `can_buy` solo string, `visibility_config` jako obiekt, `visibility_config` jako string, `translations` inline,
   pełny obiekt). To **NIE** błąd payloadu: **PUT na nieistniejący `availabilities/99999` też daje 500** (gdyby
   handler zapisu działał, byłoby 404) → **handler zapisu `availabilities` jest niesprawny/niezaimplementowany —
   zasób jest READ-ONLY przez webapi.** Rekord id 1 po wszystkich próbach **pozostał 1:1** (żadna próba nie zmieniła
   stanu — bezpieczne). ⇒ **Zmianę `can_buy` / nazwy statusu / trybu karty rób w PANELU:**
   **Ustawienia > Produkty > Statusy dostępności produktów** → klik status (id 1 „tymczasowo niedostępny") →
   sekcja **„Ustawienia dodatkowe"**: flaga **„czy klient może zamówić produkt"** = ON (`can_buy=1`); tryb karty =
   **aktywna z koszykiem** (wyłącz „Powiadom o dostępności" → `notifier`/`additional_text`); zmień **nazwę** statusu
   na „Dostępny na zamówienie". Skrypty diagnozy: `oos-flip-01-backup.ps1` (backup+zrzut id 1), `oos-flip-02-writeprobe.ps1`,
   `oos-flip-02b-shapeprobe.ps1`, `oos-flip-02c-method-and-sample.ps1`. Backup: `backup/availabilities-przed-oos-flip-20260618.json`.
   Utworzenie etykiety „do 7 dni" (`deliveries`) — analogicznie najpewniej tylko panel (NIE testowane zapisem).

> ✅ **POTWIERDZONE NA ŻYWO 2026-06-18 (zmiana usera w PANELU zadziałała — weryfikacja READ-ONLY):** user przełączył
> status id 1 w panelu i GET `availabilities/1` zwrócił **`can_buy=1`**, **`notifier=0`**, `from=-1`, `ranges=1`,
> `name="Dostępny na zamówienie"`, `visibility_config` → `flags:0`, `cart.gallery_and_name_gray:0`,
> `cart.additional_text:0` (formularz „Powiadom o dostępności" WYŁĄCZONY, karta niewyszarzona, `cart_status:1`
> = karta zostaje, teraz z koszykiem). Delta vs backup `availabilities-przed-oos-flip-20260618.json`: can_buy 0→1,
> notifier 1→0, name „tymczasowo niedostępny"→„Dostępny na zamówienie", flags 3→0, additional_text 1→0; `from`/`ranges`
> bez zmian. Cały OOS (`calculated_availability_id=1`, stock≤0) jest teraz zamawialny. Skrypt weryfikacji:
> `oos-flip-verify-readonly.ps1` (tylko GET).

Skrypty (READ-ONLY): `oos-diag-readonly.ps1` (availabilities + deliveries-probe + próbka prod.),
`oos-diag2-readonly.ps1` (pełny obiekt produktu + sondy filtrów), `oos-diag4-readonly.ps1` (czysta sonda
`deliveries`). Zrzuty: `_rozeznanie/oos-diag.json`, `_rozeznanie/deliveries.json`.

### ✅ Czas wysyłki per produkt = `stock.delivery_id` — partial-PUT DZIAŁA; POST `deliveries` READ-ONLY — zweryf. na żywo 2026-06-18

**Cel:** ustawić czas wysyłki produktom — wszystkim 48h, a OOS (`stock.stock <= 0`) termin dłuższy.
Test kontrolowany na 2 produktach (94 dostępny stock=45; 98 OOS stock=0), backup
`backup/delivery-set-20260618/` (pełne obiekty PRZED/PO). Skrypt: `delivery-set-recon.ps1`.

- **`stock.delivery_id` jest ZAPISYWALNY przez webapi partial-PUT — POTWIERDZONE.** Minimalne, bezpieczne body:
  **`PUT /webapi/rest/products/{id}` z `{"stock":{"delivery_id":"<ID>"}}`** → HTTP 200, body `1`.
  Pełna różnica PRZED↔PO (40/39 pól top-level + 38/37 pól `stock`, porównane 1:1): zmienił się **WYŁĄCZNIE
  `stock.delivery_id`** (`null`→"2" / `null`→"7") **plus automatyczny `edit_date`** (znacznik czasu nadawany
  przez Shoper przy każdym zapisie — nieszkodliwy). **`stock.stock`, `availability_id`,
  `calculated_availability_id`, `price` i wszystkie ceny porównawcze, `code`, `ean`, `historical_lowest_price`
  (Omnibus), `calculation_unit_*`, `active`, `translations.pl_PL.active`, `producer_id`, `category_id`, nazwa
  — BEZ ZMIAN.** ⇒ partial-PUT na `stock` NIE zeruje reszty `stock` (kontrast do typowego ryzyka „PUT nadpisuje
  cały obiekt"). **To jest bezpieczny kształt do użycia masowo.** Wzorzec zapisu: `HttpWebRequest` +
  `.Timeout`/`.ReadWriteTimeout`/`.KeepAlive=$false` (anti-„wiszący zapis"); PUT domyka się szybko, body `1`.
- **Słownik `deliveries` (PLASMET, 2026-06-18): brak „7 dni"/„7-14 dni".** id→(name/hours/days): 1 „24 godziny"
  24/1; **2 „48 godzin" 48/2** ← target dla dostępnych; 3 „3 dni" 72/3; 4 „4 dni" 96/4; 5 „5 dni" 120/5;
  6 „10 dni" 240/10; **7 „14 dni" 336/14** ← target dla OOS.
- **POST `deliveries` (utworzenie etykiety „7-14 dni") → ❌ HTTP 500 `server_error`** (payload
  `{hours:336,days:14,translations:{pl_PL:{name:"7-14 dni"}}}`) — **identycznie jak `availabilities`: handler
  zapisu `deliveries` jest niesprawny/niezaimplementowany → zasób READ-ONLY przez webapi.** Rekord NIE powstał
  (GET potwierdził brak). ⇒ **Nowy termin „7-14 dni" trzeba utworzyć w PANELU** (Ustawienia > Produkty >
  Czas wysyłki > „Dodaj czas wysyłki"), albo użyć istniejącego. **Decyzja operacyjna: OOS → istniejący „14 dni"
  (delivery_id 7)** (alternatywa „10 dni" id 6). Etykieta „14 dni" pokrywa wymóg „7-14 dni" (górna granica).
- **Zakres etapu 2 (filtry, 2026-06-18):** TOTAL `products` count=**7944**; OOS `{"stock.stock":{"<=":0}}` =
  `{"stock.stock":"0"}` = **2896**; dostępne (stock>0) = **5048**. ⇒ koszyk 48h (id 2): ~5048; koszyk „14 dni"
  (id 7): ~2896. Plan masowy: paginuj `products` (limit 50, ~159 stron), per produkt licz `stock.stock<=0`
  i PUT `{"stock":{"delivery_id":"2"}}` lub `"7"`. ⚠️ **Idempotencja:** pomiń produkty, które już mają poprawny
  `delivery_id` (produkty 94→2, 98→7 są już ustawione z tego testu). ⚠️ **Ryzyko Leo:** sync z Subiekta może
  nadpisać `stock` (w tym `delivery_id`) — ustalić, czy Leo przenosi czas wysyłki, by wybór nie został zresetowany.

## ✅ Jednostka sprzedaży produktu — pole `unit_id` + zasób `units` (słownik) — zweryf. na żywo 2026-06-12 (READ-ONLY)

**Jednostka sprzedaży („za co się płaci": /szt, /opak, /100szt) = pole `unit_id` (top-level) na produkcie,
referencja do zasobu `units`.** To NIE „cena jednostkowa" unijna (przelicznik za jednostkę miary — to osobny
mechanizm, patrz niżej `unit_price_calculation` / `stock.calculation_unit_*`).

### Zasób `units` (słownik jednostek miary sklepu) — `count=16` na koncie TEST

- **`GET /webapi/rest/units?limit=50`** → lista, `count=16`, `pages=1`. Pola rekordu: **`unit_id`**,
  **`floating_point`** (`0`/`1` — czy jednostka ułamkowa, np. kg/litr; `1` pozwala na ilości dziesiętne),
  **`translations.pl_PL.name`** (wyświetlana nazwa jednostki). Nazwa siedzi w `translations`, NIE top-level.
- **Pełny słownik (unit_id → name):** 1 `szt.`, 2 `kg`, 3 `lbs`, 4 `zestaw`, 5 `wielopak`, 6 `100szt`,
  7 `szt`, 8 `para`, 9 `opak`, 10 `100szt.`, 11 `litr`, 12 `rolka`, 13 `blister`, 14 `10szt.`, 15 `5szt`,
  16 `200szt.`. ⚠️ Słownik ma **DUBLE/wariacje** wprowadzone przez Leo/Subiekt: dwa „szt" (1 `szt.` vs 7 `szt`),
  dwa „100szt" (6 `100szt` vs 10 `100szt.`) — różnią się tylko kropką. Realnie używany jest **7 `szt`** i **6
  `100szt`** (nie domyślne 1/10) — patrz rozkład. Przy ewentualnym ujednolicaniu uważać na duble.

### Pole na produkcie

- **`unit_id`** (top-level produktu) — ID jednostki sprzedaży. **NIEPUSTE w 100% próbki** (1238 prod. z 2 próbek,
  0 pustych/0). Nigdy nie jest 0/null na tym katalogu — Leo zasila je zawsze.
- **`unit_price_calculation`** (top-level, `0`/`1` = włącznik) ORAZ **`stock.calculation_unit_id`** /
  **`stock.calculation_unit_ratio`** — to **unijna „cena jednostkowa za jedn. miary"** (np. „59,71 zł/litr");
  cena za jedn. = `stock.price / calculation_unit_ratio`. OSOBNY mechanizm, NIE pytana podstawowa jednostka
  sprzedaży `unit_id`. ⚠️ **KOREKTA 2026-07-01: NIE jest „nieużywane w PLASMET” — JEST włączone na ~14% katalogu
  i dla części produktów DAJE BŁĘDNĄ cenę za kg/litr** (objaw zgłaszany z integratorem Leo). Chemia płynna
  (Den Braven/Bostik): `calculation_unit_id=11` (litr) + `ratio`=objętość w litrach (280ML→0,28, 400ML→0,4) →
  **poprawnie**. Narzędzia/BHP (kaski/okulary/kamery/piły) błędnie mają `unit_price_calculation=1` z jednostką
  `15`(5szt)/`14`(10szt.) i `ratio` 0,2/0,1 → absurdalne „per 5szt/10szt” (setki–tysiące zł). `stock.weight`
  nadal ~0% → kalkulację zasila `calculation_unit_*`, nie waga. Szczegóły + próbka: „Metadane weryfikacji” (2026-07-01).

### Rozkład jednostek w katalogu (REALNE zróżnicowanie — Leo/Subiekt)

Dwie niezależne próbki (600 kolejnych + 638 rozproszonych po wszystkich 159 stronach / 7938 prod.):

| unit_id | nazwa | ~udział w katalogu |
|---|---|---|
| 7 | `szt` | **~76–84%** (dominanta) |
| 9 | `opak` | ~7–16% |
| 6 | `100szt` | ~3,5–3,8% |
| 13 | `blister` | ~0,2–3,1% |
| 8 | `para` | ~1,3–5,2% |
| 12 | `rolka` | ~0,2–0,8% |

- **Katalog JEST zróżnicowany** (nie tylko „szt"): regularnie występują `opak`, `100szt`, `para`, `blister`,
  `rolka`. Wkręty/kołki ciesielskie idą na **`100szt`** (np. prod_id 93/94), rękawice na **`para`**,
  łączniki/akcesoria na **`opak`**. Jednostka realnie niesie informację handlową → warto ją pokazać przy cenie.
- **% niepustych = 100%** (każdy produkt ma `unit_id`).

### Natywne wyświetlanie „jednostka przy cenie" + skąd to zasilane

- **Panel:** jednostki = **Ustawienia > Produkty > Jednostki miar** (= zasób `units`); domyślna jednostka
  nowego produktu = `application-config.product_defaults_unit_id` (na TEST = `1` „szt."), bundle =
  `product_defaults_bundle_unit_id` (= `4` „zestaw"). Te pola `application-config` są **READ-ONLY przez webapi**
  (cała konfiguracja zwraca 501 na PUT — patrz sekcja konfiguracji). Jednostkę PER PRODUKT zmienia się PUT-em
  na `products/{id}` (`unit_id`) **albo** w panelu (Produkt > Dane podstawowe > Jednostka miary).
- **Render „/szt" przy cenie to warstwa MOTYWU (Storefront), nie webapi.** webapi dostarcza tylko `unit_id` +
  słownik `units`; to, czy i jak motyw doklei jednostkę do ceny (np. `38,81 zł/szt`), zależy od szablonu Twig
  (kanał `shoper-cli`). Brak globalnego przełącznika „pokaż jednostkę przy cenie" w `application-config`
  (sprawdzone — jedyne pola unit to `product_defaults_unit_id`/`_bundle_unit_id`). Decyzja wyświetlania:
  edycja szablonu (`shoper-cli`), ewentualnie z konsultacją SEO/UX. Dane (`unit_id`) są gotowe i kompletne.
- **⚠️ Ryzyko Leo/Subiekt:** katalog (w tym `unit_id`) zasila **Leo Synchronizator z Subiekt GT** — jednostka
  pochodzi z kartoteki towaru w Subiekcie (stąd duble w słowniku `units` i zróżnicowanie). **Zmiany `unit_id`
  robione przez webapi/panel mogą zostać NADPISANE przy następnej synchronizacji Leo** (jak reszta katalogu) →
  jeśli trzeba poprawić/ujednolicić jednostki, robić to **u źródła w Subiekcie**, nie na Shoperze. Sam render
  „/szt" przy cenie (motyw) jest BEZPIECZNY (Leo nie tyka szablonu).
- Skrypty (READ-ONLY): `diag-unit-sprzedazy-readonly.ps1` (units + pola produktu + próbka 15 marek + rozkład 600),
  `diag-unit-rozklad-szeroki-readonly.ps1` (rozkład po rozproszonych stronach całego katalogu).

## ⛔ Publiczny upload plików (hosting obrazów do `<img src>`) — NIE MA go w webapi — ZWERYFIKOWANE NA ŻYWO 2026-06-12 (READ-ONLY)

**Werdykt: webapi REST Shopera NIE udostępnia zasobu do publicznego uploadu dowolnych plików** (typu „wgraj
WebP/PNG → dostań stabilny URL `/userdata/public/assets/<plik>.webp` do `<img src>` w bloku HTML home).
Sonda READ-ONLY (`scripts/shoper-api/probe-fileupload-readonly.ps1`, GET `?limit=1`) na 20 nazw-kandydatów:
`attachments`, `attachment`, `files`, `file`, `media`, `gallery`, `galleries`, `images`, `image`, `uploads`,
`upload`, `assets`, `userdata`, `documents`, `document`, `downloads`, `resources`, `static`, `public-files`
→ **wszystkie HTTP 400 „Missing MODULE"** (nie istnieją). Jedyny istniejący zasób plików to **`product-files`**.

- **`product-files`** (`probe-productfiles-shape.ps1`) = **pliki do pobrania POWIĄZANE z produktem** (karty
  bezpieczeństwa PDF itp.), NIE wolny hosting obrazów. Pola: `file_id`, `translation_id` (wiąże z produktem),
  `name`, `description`, **`file_name` = wewnętrzny HASH na dysku** (np. `2146db8c…`), `file_size`, `type`,
  `order`, `active`. **Brak publicznego URL nadającego się do `<img>`** — plik serwuje kontroler pobierania
  produktu, nie jako zasób w `/userdata/public/assets/`. Analogicznie `news-files` = galeria/załączniki wpisu
  bloga (też hash `file_name`, nie renderuje się nawet jako hero — patrz sekcja `news`).
- **Obrazy w webapi są ZAWSZE WIĄZANE z zasobem** (nie wolnostojące): `product-images` (zdjęcia produktu),
  `news.image` (base64, główne zdjęcie wpisu), `news-files` (galeria wpisu), `categories` `image_*`,
  `product-files` (downloads produktu). **Żaden nie daje dowolnie-linkowalnego URL pliku publicznego.**

## ✅ `product-files` — UPLOAD plików „do pobrania" produktu (PDF/karty bezpieczeństwa) — ZAPIS ZWERYFIKOWANY NA ŻYWO 2026-06-15 (1 kontrolny POST + front)

**`product-files` = sekcja „Pliki do pobrania" na karcie produktu (PDF itp.). ZAPIS przez webapi DZIAŁA**
(POST tworzy rekord, plik ląduje na dysku, front renderuje natywnie). Zweryfikowane 1 kontrolnym uploadem
(`file_id=73`, produkt BAUM WIERTŁO X4 5x110mm) — skrypty `productfiles-recon-readonly.ps1` (READ-ONLY),
`productfiles-test-upload.ps1` (`-DryRun` domyślnie, `-Apply` = realny POST), `baum-wiertla-recon.ps1`.

### Pola rekordu (GET `/product-files/{id}`) + DZIAŁAJĄCY payload POST

| pole | w POST | uwagi |
|---|---|---|
| `file_id` | — | PK, nadawany przy POST; **POST zwraca SAMO ID w body** (np. `73`) — połączenie domyka się szybko (nie wisi jak `news`) |
| `translation_id` | ✅ **WYMAGANE** | **WIĄŻE z produktem przez `translations.pl_PL.translation_id`, NIE `product_id`!** (to osobne pole; np. produkt `product_id=6974` ma `translation_id=6965`) |
| `name` | ✅ | nazwa wyświetlana w „Plikach do pobrania". ⚠️ **SANITYZOWANA DO ASCII** — serwer transliteruje polskie znaki i em-dash (`ń→n`, `ł→l`, `—→-`); potwierdzone POST-em i PUT-em (oba zwracają 200, ale `name` zostaje ASCII). Trzymaj `name` ASCII-safe (to de facto nazwa pliku do `download=`) |
| `description` | ✅ | tekst opisu — **POLSKIE ZNAKI PRZECHODZĄ** (`„Karta bezpieczeństwa"` zachowane z `ń`). Render na froncie pod nazwą pliku |
| `content` | ✅ (przy tworzeniu) | **CZYSTY base64 zawartości pliku** (`[Convert]::ToBase64String([IO.File]::ReadAllBytes(...))`), **NIE data-URI** (jak `news-files`/`news.image`). NIE odbijane w GET |
| `file_name` | ✅ **WYMAGANE w POST** | ⚠️ **KOREKTA 2026-06-15 (masowy apply):** serwer **WYMAGA** `file_name` w body POST — bez niego **HTTP 400 `{"error":"invalid_request","error_description":"Key 'file_name' is required"}`** (potwierdzone na żywo: payload bez `file_name` → 400 dla KAŻDEGO POST; po dodaniu `file_name` → 200 + `file_id`). W POST podaj nazwę źródłową (użyto `'Karta bezpieczenstwa - wiertla 4-ostrzowe (PDF)'`). W **GET** to pole odbija **wewnętrzny HASH MD5 na dysku** nadany przez serwer (np. `c17750f3…`), który buduje URL pobrania `/pl/p/file/<hash>/<slug>` — czyli `file_name` ma INNĄ rolę w POST (nazwa wej.) niż w GET (hash). Test 1-produktowy z 2026-06-15 przeszedł, bo `productfiles-test-upload.ps1` MIAŁ `file_name` w payloadzie; pierwsza wersja skryptu masowego go pominęła → stąd 400 |
| `file_size` | — (GET) | rozmiar w bajtach = **dokładnie rozmiar wysłanego pliku** (weryfikacja integralności: 1494031 B = 1494031) |
| `type` | ✅ | `1` w realnych rekordach (typ pliku „do pobrania"); użyte przez ręcznie dodane rekordy admina (file_id 2/3) |
| `active` | ✅ | `1` = widoczny na karcie |
| `order` | ✅ | kolejność (`1` w realnych) |
| `date_add` | — (GET) | `YYYY-MM-DD HH:MM:SS`, nadawane serwerem |

- **Minimalny działający payload POST:** `{translation_id, name, description, file_name, content(base64), type:1, active:1, order:1}`.
  ⚠️ **`file_name` JEST OBOWIĄZKOWE** (jego brak → HTTP 400 „Key 'file_name' is required") — patrz tabela pól wyżej.
- 🚨 **`name` (i `file_name`) MUSI kończyć się rzeczywistym rozszerzeniem pliku (np. `.pdf`)** — INACZEJ **pobranie nie ma
  rozszerzenia i się nie otwiera**. Zweryfikowane na żywo 2026-06-15 (naprawa 81 kart Baum): **serwowana nazwa pobrania
  (`Content-Disposition: filename="…"`) = SLUG zbudowany z `name`** (NIE z hash GET, NIE z `file_name` GET, NIE zależy od
  treści). `Content-Type` pobrania = `application/force-download`, więc przeglądarka zapisuje plik dokładnie pod nazwą z
  `Content-Disposition`. Slugowanie: **kropka przed rozszerzeniem ZACHOWANA** (`"…-4-ostrzowe.pdf"` → CD kończy się `.pdf`),
  ale spacje/kropki wewnętrzne/znaki specjalne → `-` (więc `"Karta … (PDF)"` → slug `Karta-…-PDF` → pobranie **bez `.pdf`**,
  user nie otworzy). **Buduj `name` jako `<ASCII-myślniki>.<ext>`, gdzie `<ext>` = `[IO.Path]::GetExtension($FilePath)`.**
  Nie wstawiaj „(PDF)" w środek nazwy. `productfiles-bulk-apply.ps1` (poprawiony 2026-06-15) **sam dokleja rozszerzenie źródła**.
- 🔧 **NAPRAWA już-wgranych plików bez rozszerzenia:** `PUT /product-files/{file_id}` z `{name:"<…>.pdf", file_name:"<…>.pdf"}`
  — **sam PUT regeneruje slug** w URL pliku, więc serwowana nazwa zaczyna kończyć się `.pdf` **BEZ ponownego uploadu treści**
  (zweryfikowane na żywo, file_id=73: CD `filename="…-4-ostrzowe.pdf"` + magic `%PDF`). **NIE rób DELETE+POST:**
  (1) **DELETE `product-files/{id}` → HTTP 403 `insufficient_scope`** (token webapi PLASMET NIE ma uprawnienia delete plików);
  (2) re-POST tworzy **DUPLIKAT** (drugi plik na karcie), którego nie da się skasować — tylko ukryć `PUT {active:0}`.
  ⚠️ **Po PUT front karty może chwilowo cache'ować stary link** (serwowana nazwa = slug w URL → cache HTML linkuje do starego
  slugu bez `.pdf`); baza poprawna, cache odświeża się sam, weryfikuj bezpośrednim pobraniem nowego URL. ⚠️ **`409 Object is
  locked`** na PUT bywa trwały (rekord/produkt zablokowany — prawdopodobnie Leo Sync); ponów po dłuższej przerwie, nie blokuje
  reszty zbioru. Skrypty: `productfiles-fix-pdf-ext-bulk.ps1` (masowa naprawa PUT, idempotentna, retry 429/409),
  `productfiles-diag-pdf-ext.ps1` (diagnoza CD+%PDF), `productfiles-verify-front-pdf.ps1` (weryfikacja na froncie).
- **Wzorzec zapisu anti-„wiszący zapis":** `HttpWebRequest` + `.Timeout` + `.ReadWriteTimeout` + `.KeepAlive=$false`.
  Na POST `product-files` połączenie **domyka się** i body zwraca nowe `file_id` (jak `redirects`, inaczej niż `news`).
- **Idempotencja:** przed POST paginuj `GET /product-files?limit=50&page=N` (lista globalna wszystkich plików,
  bez filtra po produkcie!) i sprawdź, czy dla danego `translation_id` nie ma już pliku o tej nazwie/rozmiarze.
- **`name` w weryfikacji po POST:** porównuj po `translation_id` + `file_size` (NIE po `name` z polskimi znakami —
  bo serwer go transliteruje, więc dopasowanie po dokładnym polskim `name` nie zadziała).

### ✅ Front renderuje natywnie (motyw, BEZ zmian) — zweryfikowane 2026-06-15

Karta produktu (`permalink` z `translations.pl_PL.permalink`) renderuje natywną sekcję
**`<h3>Pliki do pobrania</h3>`** z kafelkiem `file-box`: `<a class="file-box__header" download
href="/pl/p/file/<hash>/<slug>">` + tytuł = `name`. **Moduł jest NATYWNY w motywie — nie trzeba nic włączać
w Storefront.** (Ikona rozszerzenia = `icon-generic.webp` — Shoper nie zmapował ikony PDF; funkcjonalnie link
serwuje plik. Do ew. poprawy ikony PDF: motyw/`shoper-cli`, kosmetyka.) Front stagingu `sklep261208.shoparena.pl`
odpowiada na zewnętrzne HTTP (dekoduj `RawContentStream`→UTF-8).

### ⚠️ Mapowanie produkt → translation_id + pułapka filtra `producer_id`

- **`translation_id` bierz z produktu:** `GET /products/{id}` → `translations.pl_PL.translation_id` (osobne pole,
  ≠ `product_id`). Albo filtrem: `GET /products?filters={"translations.translation_id":"<tid>"}` (działa, zwraca produkt).
- **⚠️ FILTR `producer_id` JEST IGNOROWANY na tej instancji (2026-06-15)** — `{"producer_id":"46"}` zwraca CAŁY
  katalog (7938), nie podzbiór. **To regresja względem notatki z 2026-06-13** (gdzie rzekomo działał, Baum=26→198).
  Działa za to **`{"producers.producer_id":"46"}`** (count=198) — ale do pewności i tak **skanuj cały katalog**
  (159 stron × 50) i filtruj `producer_id` po stronie klienta (jak `baum-wiertla-recon.ps1`).
- **⚠️ Baum ma DWA wpisy producenta po re-syncu Leo:** id=26 `'Baum'` (stary/pusty) i **id=46 `'BAUM'` = realne 198
  produktów**. Producenci 23–50 to nowy zestaw z Subiektu (pełne nazwy prawne + krótkie). **Realne produkty Baum
  = `producer_id=46`.** Wiertła Baum = **81 szt., wszystkie „WIERTŁO DO BETONU SDS PLUS X4" (X4 = 4-ostrzowe),
  `category_id=173`** → zbiór A (wszystkie wiertła) == zbiór B (4-ostrzowe) == 81. Lista:
  `_rozeznanie/baum-wiertla-kandydaci.json`.

### ✅ Jak NAPRAWDĘ trafiają pliki do `/userdata/public/assets/` (loga marek na home) — przez PANEL, nie webapi

Loga marek na home (`<img src="/userdata/public/assets/<slug>.webp">`) wgrano **NIE przez webapi**, tylko przez
**Froala File Manager (elFinder) w edytorze modułu/SVE w panelu** (potwierdzone notatką pamięci
`home-przebudowa-natywna.md`, sekcja „HOSTING OBRAZÓW W MODULE", 2026-06-10). Przepływ panelowy (reużywalny):
**Froala „Wstaw obraz" → „Browse" → File manager (elFinder) → „Upload" → „Wybierz pliki"** (input plików;
`upload_file` APPENDuje do kolejki — dodać wszystkie, potem „Upload"). Pliki lądują w folderze „user" → URL
**`/userdata/public/assets/<nazwa>` (HTTP 200, stabilny)**. Można pominąć wstawianie obrazu i wziąć sam URL
do własnego HTML w „Widok kodu". **To jest jedyna droga hostingu publicznych obrazów dla bloku HTML home** —
kanał PANEL/SVE (agent `shoper-cli` lub user ręcznie), poza webapi (kanał DANE).

## ✅ Pola produktu pod BOGATĄ KARTĘ PRODUKTU (PDP) — rozeznanie READ-ONLY 2026-06-15

Rozeznanie pod projekt nowej karty produktu (`pdp-feasibility-recon.ps1` + `-recon2.ps1`, TYLKO GET).
Produkt referencyjny **`products/2000` = Milwaukee „MM WIERTARKO-WKRĘTARKA FUEL M18 FDD3-0"** (potwierdzony,
`category_id=114`, `producer_id=44`). Próbka z różnych kategorii: 152 (silikon Den Braven), 144 (klej DB X-Polymer),
99 (rękawice BHP), 384 (kask Milwaukee BOLT 200). Skala liczona na 300–500 produktach (pierwsze strony).

### Realne pola top-level obiektu `products/{id}` (z żywych GET)

`add_date, additional_producer, attributes, bestseller, categories, category_id, code, collections, currency_id,
dimension_h, dimension_l, dimension_w, ean, edit_date, feeds_excludes, gauge_id, group_id, in_loyalty, is_digital,
is_product_of_day, loyalty_price, loyalty_score, main_image, newproduct, options, other_price, pkwiu, producer_id,
product_id, promo_price, related, safety_information, stock, tags, tax_id, translations, type, unit_id,
unit_price_calculation, vol_weight`. Treść (`name`/`short_description`/`description`/`seo_*`/`permalink`) siedzi
w `translations.pl_PL`. Cena/stan/EAN/SKU **dublują się** w `stock` (zagnieżdżony obiekt; patrz niżej).

### Co JEST w danych (zasila bogatą kartę)

| pole projektu | źródło webapi | stan w katalogu |
|---|---|---|
| **EAN/GTIN** | `ean` (top-level i `stock.ean`) | ✅ **~98%** wypełnione (Milwaukee/Den Braven/Bostik mają; rękawice BHP bez producenta — puste) |
| **Symbol/SKU** | `code` (i `stock.code`) | ✅ **100%** — format z Leo/Subiekt (ze spacjami, np. `06MM4933 4980 59`) |
| **Cena brutto** | `stock.price` | ✅ 100% |
| **Stan magazynowy (ilość)** | `stock.stock` (string liczba) | ✅ obecny; **~70%** ma `stock>0` (np. FDD3-0=6, silikon=768, kask=0) |
| **Dostępność (auto)** | `stock.calculated_availability_id` → zasób `availabilities` | ✅ wyliczane ze stanu (FDD3-0=`2` „średnia ilość"). To etykiety ILOŚCI, NIE czasu wysyłki |
| **Opis** | `translations.pl_PL.description` | ✅ ~95% niepuste (FDD3-0=2063 zn.); **realny opis** |
| **„Short description"** | `translations.pl_PL.short_description` | ✅ niepuste, ale to **stały blok GPSR producenta** (~250 zn.), NIE marketing-lead |
| **Producent (nazwa)** | `producer_id` → zasób `producers` (`translations.pl_PL.name`) | ✅ przypisany (ale duble z Leo, niżej) |
| **Wymiary/waga** | `dimension_l/w/h`, `vol_weight`, `stock.weight` | ⚠️ pola istnieją, ale **= 0.0000** (nieuzupełnione) |
| **GPSR / bezpieczeństwo** | `safety_information` (`gpsr_*`), `product-files` (PDF) | ⚠️ struktura jest, wartości puste; PDF kart Baum dograne (81/81) |

### Czego NIE MA w danych (sekcje projektu, które będą PUSTE)

| pole projektu | źródło webapi | stan — **werdykt** |
|---|---|---|
| **Atrybuty / „Dane techniczne" / pasek parametrów** | `attributes` (top-level) + zasoby `attributes`/`attribute-groups` | ❌ **PUSTO W CAŁOŚCI.** `attribute-groups` **count=0**, `attributes` **count=0** (zero zdefiniowanych atrybutów w sklepie). Na KAŻDYM produkcie pole `attributes` = `[]`. **0/500** produktów ma atrybuty. → projektowy pasek 12+ parametrów (moment, obroty, waga…) **nie ma żadnego pokrycia w danych.** `products/{id}/attributes` jako ścieżka **NIE działa** (zwraca cały katalog — ignorowana). |
| **Cena promocyjna / stara cena / „-15%"** | `promo_price` (top-level), `stock.price_special`, zasób `specialoffers` | ❌ **BRAK PROMOCJI.** `promo_price`=`null`, `stock.price_special` **= `stock.price`** (równe, brak rabatu), zasób **`specialoffers` count=0** (zero promocji w sklepie). Pola `special_offer` NA PRODUKCIE brak (promocja to OSOBNY zasób `specialoffers`, NIE pole produktu). **0/500** produktów ma promocję. ⚠️ **KOREKTA (2026-07-03, prod. 1949):** `stock.historical_lowest_price` (Omnibus) **potrafi różnić się od ceny bieżącej** (34,42 vs 34,00) — Shoper śledzi realne 30-dniowe minimum; NIE zawsze „= cena bieżąca". **Plakietka „najniższa cena z 30 dni" pokazuje się TYLKO przy aktywnej promocji (`specialoffers`), NIE przy zmianie ceny bazowej** — motyw trzyma blok `product-price__lowest-historical-price` w `hidden` na `js__special-offer-container`. |
| **Opinie / oceny / licznik** | zasób `product-reviews` | ❌ **HTTP 403** (zasób istnieje, ale konto webapi **NIE ma uprawnień / moduł niedostępny przez API**; `/list`→405). Brak pola `rating`/`reviews_count` na produkcie. → „48 opinii, 5,0" **brak danych i brak dostępu przez webapi** (nawet do odczytu). |
| **Produkty powiązane / cross-sell / „Klienci kupowali również"** | `related` (top-level) | ❌ **PUSTO.** `related` = `[]` na produkcie referencyjnym; **0/500** ma powiązania. Brak zasobów `related-products`/`accessories`/`cross-sells` (wszystkie „Missing MODULE" 400). |
| **Logo marki** | `producers.gfx` | ❌ **0/28 producentów** ma `gfx` (puste dla wszystkich, w tym Milwaukee/Bostik/Baum/Richmann). → kafle marek = osobne pliki w panelu (`/userdata/public/assets/`), nie webapi. |
| **Flagi „bestseller/nowość/produkt dnia"** | `bestseller`, `newproduct`, `is_product_of_day` | ❌ **0/500** ustawione (`'0'`/`false`). |
| **Czas wysyłki („wysyłka 24h")** | brak natywnego pola | ❌ `availabilities` to etykiety ILOŚCI („średnia ilość", „duża ilość"), nie czasu dostawy; `stock.availability_id`=null, `delivery_id`=null. „Wysyłka 24h" musiałaby iść z motywu/stałego tekstu. |

### ⚠️ Pułapki danych producentów (duble z Leo/Subiekt)

`producers` count **28**, ale to zestaw z DUBLAMI po re-syncu Leo — każda realna marka ma 2 wpisy (krótka nazwa
„marketingowa" + pełna nazwa prawna z Subiektu), a **produkty wiążą się z wpisem pełno-prawnym**:
- Milwaukee: id **35** „Milwaukee" (pusty) vs id **44** „TECHTRONIC INDUSTRIES…" — **FDD3-0 ma `producer_id=44`**.
- Bostik / Den Braven: ⚠️ **KOREKTA 2026-06-15** — po kolejnym re-syncu Leo `producers` count=**49**, a realne
  produkty Bostik/Den Braven **NIE wiszą już pod 30/43**, lecz pod NOWYMI id: **51 „BOSTIK NIEAKTUALNE" (176 prod.)**
  i **66 „BOSTIK" (45 prod.)** — plus szczątkowo 1 prod. pod 30. Producent **43 „BOSTIK SPÓŁKA Z O.O." = 0 produktów**
  (osierocony). **Den Braven NADAL NIE jest osobnym producentem** — brak wpisu „Braven"/„Den Braven"/„DB" wśród 49
  producentów; produkty „DB …" w nazwie = Den Braven dystrybuowany jako Bostik (183 szt.). **TECTANE = 0** (brak takiej
  podmarki w katalogu). **MAMUT = 2** prod. „Bostik MAMUT GLUE" pod id 51. Wniosek: id producentów Bostik **migrują przy
  każdym sync Leo** (jak Baum 26→46) → nie polegaj na stałym id; identyfikuj markę po `name` (`DB`/`BOSTIK`/`MAMUT`)
  ORAZ skanuj cały katalog. Pełny zbiór 222 prod. „nasze" w `_rozeznanie/bostik-denbraven-nasze.json`.
- Baum: id 26 „Baum" vs id **46** „BAUM” (realne); Richmann 36 vs 45; Klingspor 29 vs 47; Polifarb 33/42/48.
→ Do nazwy marki na karcie używaj **`producer_id` z produktu** (np. 44), a do ładnej nazwy mapuj na krótki wpis
(35) — bo pełna nazwa prawna brzydko wygląda na froncie. Pola producenta: `gfx, in_loyalty, isdefault, name,
producer_id, sort_type, translations, web`.

### Wniosek dla projektu PDP

Bogactwo danych **NIE jest regułą — pusto jest regułą** dla sekcji „premium". Mają pokrycie: **EAN, SKU, cena,
stan, opis, producent (nazwa), zdjęcie główne**. Nie mają żadnego pokrycia: **atrybuty/parametry techniczne,
promocje/stara cena, opinie, produkty powiązane, logo marki, flagi bestseller/nowość, czas wysyłki**.
**⚠️ Ryzyko Leo:** katalog zasila Leo Synchronizator z Subiekt GT — ręczne uzupełnianie atrybutów/powiązań przez
webapi może być **nadpisane przy najbliższym sync** (jak `unit_id`/`order`). Atrybuty należy uzupełniać **u źródła
(Subiekt/Leo)** lub przyjąć, że PDP renderuje te sekcje warunkowo (ukrywa puste). Skrypty:
`pdp-feasibility-recon.ps1`, `pdp-feasibility-recon2.ps1`; zrzuty `_rozeznanie/pdp-feasibility*.json`.
Deliverable: `szablon/design-claude/strona-produktu-2026-06/feasibility-dane.md`.

## Pułapki

- **Limity zapytań** — webapi ma throttling; przy masowych operacjach dodać opóźnienia, retry z backoff
  i obsługę HTTP 429/5xx. Najpierw test na `limit=1` / pojedynczym rekordzie, dopiero potem masa.
- **Zapisy zmieniają żywy sklep** — `POST`/`PUT`/`DELETE` działają od razu. Operacje masowe i kasowanie
  tylko za zgodą użytkownika; preferuj `GET` na rozeznanie i dry-run.
- **Token** — konto PLASMET zwraca `expires_in: 2592000` (**30 dni**, nie 3600 s) → token długożyjący,
  ale i tak warto odświeżać w długich zadaniach. Stary przepływ login+hasło działa.
- **`"Missing MODULE 'xxx'"` (HTTP 400)** — **najczęściej oznacza BŁĘDNĄ NAZWĘ ZASOBU, nie brak uprawnień.**
  ⚠️ **ROZWIĄZANE 2026-06-10:** wcześniejsze „Missing MODULE 'pages'" przy stronach informacyjnych CMS było
  **pomyłką nazwy** — **`pages` NIE ISTNIEJE w webapi Shopera; właściwy zasób to `aboutpages`** (patrz sekcja
  „Strony informacyjne CMS — zasób `aboutpages`" wyżej). `GET/PUT aboutpages` działają (HTTP 200), uprawnienie
  „Zawartość" konta webapi PLASMET jest pełne. **Wniosek ogólny:** zanim uznasz „Missing MODULE" za brak
  uprawnień/modułu, **zweryfikuj realną nazwę zasobu w oficjalnej dok.** (sitemap/`#tag/…`) — `pages`/`cms-pages`/
  `static-pages` itp. to nieistniejące nazwy, a nie zablokowane moduły. Dopiero gdy poprawna nazwa zasobu też
  zwraca „Missing MODULE", podejrzewaj uprawnienie/moduł. (Stare skrypty `rozeznanie-pages-*.ps1` celowały
  w nieistniejący `pages` — używaj `aboutpages-recon-backup.ps1`.)
- **Paginacja `limit`** — przy `limit=1` API i tak zwraca `pages` policzone dla **domyślnego** rozmiaru
  strony (np. `count=56, pages=56` przy limit=1, ale `pages=6` przy domyślnym ~10). Iteruj po `pages`
  z ustalonym `limit=50`, nie polegaj na `pages` ze zwrotu z `limit=1`.
- **Hierarchia kategorii** — `categories` jest płaska (`root`, `order`); pełne drzewo parent→children
  zwraca `categories-tree`. URL kategorii i tak jest płaski (`/pl/c/Nazwa/ID`).
- **Opis + SEO kategorii (ZAPISYWALNE webapi, zweryf. 2026-06-11; potwierdzone PONOWNIE partią 2 — 12 kat. 2026-06-11)** —
  pole opisu = `translations.pl_PL.description`
  (HTML, WYSIWYG). **PUT `categories/{id}` z `translations.pl_PL.{description, seo_title, seo_description, seo_keywords}`
  zapisuje WSZYSTKIE te pola** (HTTP 200 `raw=1`, GET potwierdza len>0). Partia 2 (ID 192,279,71,68,75,93,85,159,180,285,165,142):
  12/12 desc OK, 12/12 meta OK, zero zwisów; UTF-8 (ś/ż/ł/–) zachowane; anty-404 zachował link kat. 142→news_id 12.
  Skrypty: `category-seo-publish-p2.ps1` (filtr po 12 ID partii 2 + priorytet CTR + anti-hang + anty-404). ⚠️ To **INACZEJ niż `aboutpages`**, gdzie `seo_title`/
  `seo_description` były efektywnie READ-ONLY przez webapi — **nie generalizuj polityki SEO między zasobami** (każdy zasób
  testuj osobno). Top-level kategorii ma `category_id`/`root`/`order`/`sort_type`/`image_*`/`translations`; treściowe pola
  są w `translations.pl_PL` (`description`, `description_bottom`, `name`, `permalink`, `seo_*`, `active`).
- **✅ „Opis dół" kategorii = `translations.pl_PL.description_bottom` — ZAPISYWALNY przez webapi (zweryf. na żywo 2026-06-16, kat. 61).**
  Motyw renderuje `description` jako „opis góra" (nad listą produktów) i **`description_bottom` jako „opis dół" (pod listą)** —
  to standardowy split SEO kategorii Shopera. PUT `categories/{id}` z `translations.pl_PL.description_bottom` → **HTTP 200 `raw=1`,
  ZAPISUJE** (sonda markerem na pustym polu: zapis + GET-odczyt + przywrócenie do pustego, `description` nienaruszony). UTF-8 (ś/ż/ł)
  i HTML (`<div class="...">`, `<h3>`, `<a>`) przechodzą bez sanityzacji/mojibake. **Wzorzec splitu (gdy cała treść siedzi w
  `description`):** pisz ATOMOWO — najpierw PUT `description_bottom` (rozwinięcie), GET-weryfikacja, że dół zapisany ORAZ `description`
  wciąż pełny, **dopiero potem** PUT `description` (krótki wstęp). Tak nie ma okna z utraconą treścią, jeśli pierwszy PUT padnie.
  Skrypty (kat. 61): `cat61-desc-split-recon.ps1` (KROK1 GET+backup), `cat61-bottom-writeprobe.ps1` (sonda zapisu, samoprzywracająca),
  `cat61-desc-split-apply.ps1` (`-DryRun` domyślnie; atomowy split + backup starej `description` + INFO o linkach `/pl/news/`),
  `cat61-verify.ps1` (niezależna weryfikacja świeżym tokenem). Backup starej treści: `backup/cat61-description-old_*.html`.
- **Dane osobowe klientów (RODO)** — `users`/`orders` zawierają PII (`email`, `delivery_address`,
  `billing_address`); nie pobieraj/nie wypisuj zbędnie w odpowiedziach.

## ✅ Klienci — zasób `users` + `user-addresses` (+ `user-groups`) — ROZEZNANIE READ-ONLY 2026-06-18

Klient sklepu = zasób **`users`** (NIE `customers`). Konto klienta i dane teleadresowe/firmowe są
**ROZDZIELONE na dwa zasoby**: `users` (tożsamość/login/newsletter/grupa) + `user-addresses`
(książka adresowa: telefon, firma, NIP, adres). Wiązanie po **`user_id`**.

### `users` — pola obiektu (GET `users/{id}`, PŁASKIE, zweryfikowane na żywo)

`user_id` (PK, string), `login`, `date_add`, `lastvisit`, `verify_email` (0/1), `origin`,
`registered` (0/1), `groups` (array — przynależność do grup), `group_id` (string\|`null` → grupa
domyślna), `additional_fields` (array — pola dodatkowe rejestracji), `tags` (array), **`firstname`**,
**`lastname`**, **`email`**, `discount` (string `"0.00"`), **`newsletter`** (string `"0"`/`"1"`),
`active` (0/1), `lang_id` (string; `1`=polski), `comment`.

> ⚠️ Obiekt `users` **NIE ma** pól `phone`, `company`, `pesel`, `tax_identification_number` —
> te idą do `user-addresses` (niżej). `password` NIE jest odbijane w GET (write-only).

### POST `users` — pola tworzenia (developers.shoper.pl `#tag/Users` → `users/insert`, SPA za loginem)

- **Wymagane minimum:** `email`. Hasło: pole **`pass`** ✅ **POTWIERDZONE EMPIRYCZNIE 2026-06-18**
  (POST testowy `user_id=7` → HTTP 200, konto utworzone). `password` nie testowano bo `pass` zadziałało
  od razu. Write-only (GET nie odbija); brak twardej walidacji długości — klient zresetuje mailem.
  `firstname`, `lastname`, `newsletter`, `group_id`, `active`, `lang_id`, `comment` — opcjonalne.
- **`newsletter`** = string `"0"`/`"1"` (dla importu PLASMET = `"0"` u wszystkich). **`group_id`** = ID
  z `user-groups` albo `null` = grupa domyślna (testowo `null` → GET zwrócił `group_id=''`, `registered=0`).
  `active` = `"1"`. `lang_id` = `"1"`. Wszystkie przyjęte jako string.
- ✅ **DZIAŁAJĄCY payload POST `users` (1:1 do masy, zweryfikowany GET-em):**
  `{ "email":"…", "firstname":"…", "lastname":"…", "newsletter":"0", "active":"1", "lang_id":"1", "group_id":null, "pass":"<≥12 zn. losowe>" }`
  → GET potwierdził: firstname/lastname/email/newsletter/active zapisane 1:1.

### `user-addresses` — firma/telefon/NIP/adres (GET zweryfikowany na żywo, count=5)

Pola: `address_book_id` (PK), **`user_id`** (FK do `users`), `address_name`, **`company_name`**,
`pesel`, `firstname`, `lastname`, `street_1`, `street_2`, `city`, `zip_code`, `state`, `country`,
`default` (0/1), `shipping_default` (0/1), **`phone`**, `sortkey`, `country_code`,
**`tax_identification_number`** (= NIP).

> **Telefon i firma klienta NIE idą w obiekt `users`** — trzeba utworzyć powiązany rekord
> `user-addresses` (POST, `user_id` = ID świeżo utworzonego klienta). To **dwa żądania na klienta** (throttle).

> ⚠️⚠️ **POLA WYMAGANE w POST `user-addresses` — ODKRYTE EMPIRYCZNIE 2026-06-18 (test, NIE było w rozeznaniu GET):**
> POST z samym `phone`+`company_name`+`firstname`+`lastname`+`default` → **HTTP 400**:
> *„Wartość pola 'street_1'/'city'/'zip_code'/'country_code' jest niepoprawna: Pole wymagane"*.
> **`street_1`, `city`, `zip_code`, `country_code` SĄ WYMAGANE** (GET ich wymagalności NIE pokazuje!).
> Pusty string `''` w tych polach też **NIE przechodzi** (nadal „Pole wymagane"). To **KRYTYCZNE dla masy**:
> Mercatum dostarcza tylko telefon+firmę, BEZ adresu pocztowego → adresu nie da się utworzyć „czysto".
> ✅ **DZIAŁAJĄCY payload (zweryfikowany — `address_book_id=6` powiązany z `user_id=7`):** placeholdery
> w polach adresowych + `country_code='PL'`:
> `{ "user_id":7, "company_name":"…", "phone":"…", "firstname":"…", "lastname":"…", "default":"1", "street_1":"-", "city":"-", "zip_code":"00-000", "country_code":"PL" }`
> → HTTP 200, body = nowe `address_book_id`. GET `user-addresses/{id}` potwierdził: telefon, firma,
> `user_id` (powiązanie), placeholdery zapisane.
> **DECYZJA DO PODJĘCIA PRZED MASĄ:** czy importować adresy z placeholderami (`street_1='-'`,`city='-'`,
> `zip_code='00-000'`,`cc='PL'`), czy **pominąć `user-addresses` całkowicie** (importować tylko konta `users`
> z emailem/imieniem; telefon+firma przepadają). Placeholdery = sztuczny adres w książce adresowej klienta
> (klient i tak uzupełni przy 1. zamówieniu); pominięcie = brak telefonu/firmy w sklepie. Wymaga decyzji usera.
> ⚠️ **Quirk weryfikacji:** filtr `user-addresses?filters={"user_id":"X"}` bywa **opóźniony** zaraz po POST
> (świeży rekord nie od razu w wyniku filtra) → w masie czytaj `address_book_id` z **body POST** (zwraca samo ID)
> albo dodaj krótki retry/`Start-Sleep` przed weryfikacją filtrem. POST `user-addresses` **NIE wisi**
> (domyka się szybko, zwraca ID — inaczej niż POST `news`).

### ⚠️ `default`/`shipping_default` na JEDYNYM adresie klienta = WYMUSZONE `1` (NIE da się ustawić 0) — ZWERYFIKOWANE NA ŻYWO 2026-06-18 (1 PUT za zgodą)

**Gdy klient ma DOKŁADNIE JEDEN adres w `user-addresses`, Shoper trzyma `default='1'` ORAZ
`shipping_default='1'` i NIE pozwala ich nadpisać na `0` przez webapi.** Mimo że POST/PUT przyjmują
`default`/`shipping_default`, jedyny adres jest auto-promowany na domyślny (logika serwera: klient
musi mieć adres domyślny, więc jedyny = domyślny).

Test feasibility (po imporcie 425 klientów, każdy z 1 adresem; w POST wysyłano `default="0"` a GET
pokazywał `default="1"`):
- **GET** `user-addresses` przez filtr `{"user_id":"X"}` dla user_id 8/220/432 → każdy `count=1`,
  oba pola `default='1'`, `shipping_default='1'` (surowo).
- **PUT** `user-addresses/8` (user_id=8) z `{"default":"0","shipping_default":"0"}` → **HTTP 200, body `1`**
  (serwer akceptuje request bez błędu), ALE **GET po PUT → `default='1'`, `shipping_default='1'`** —
  oba pola **wróciły do 1**. Zapis nie został odrzucony błędem; po prostu serwer wymusił domyślność.
- **WNIOSEK: `default=0` na jedynym adresie klienta jest NIEOSIĄGALNE** przez webapi (PUT „przechodzi"
  HTTP 200, ale wartość się nie utrzymuje). To **NIE błąd payloadu** — to wymuszenie biznesowe Shopera.
  Aby adres mógł być `default=0`, klient musiałby mieć ≥2 adresy (wtedy jeden z nich może być niedomyślny).
- Skutek dla importu: nie warto walczyć o `default="0"` w masie — jedyny adres i tak będzie domyślny.
  W payloadzie POST/PUT można zostawić `default` (Shoper i tak ustawi 1) bez generowania błędu.
- Skrypty (read-only recon + 1-PUT test): `useraddr-default-recon.ps1`, `useraddr-default-puttest.ps1`
  (wzorzec anti-„wiszący zapis": `HttpWebRequest`+`.Timeout`/`.ReadWriteTimeout`/`KeepAlive=false`;
  backup rekordu przed PUT → `backup/useraddr-8-before-*.json`). Stan user_id=8 po teście = wyjściowy
  (`1`/`1`), bo Shoper sam przywrócił — żadna trwała zmiana nie pozostała.

### `user-groups` — grupy klientów (GET, count=**0** na koncie PLASMET)

Zasób istnieje (poprawna nazwa: **`user-groups`**, NIE `customer-groups`/`customer-group` → 400
„Missing MODULE"). Na żywym sklepie **0 grup zdefiniowanych** → wszyscy klienci w **grupie domyślnej**
(`group_id=null`). Nie ma osobnych grup detal/hurt/B2B przez webapi → importowanych zostawić
`group_id=null` (grupa domyślna) chyba że user wcześniej utworzy grupy w panelu.

### ⛔ DELETE `users`/`user-addresses` przez webapi = HTTP 403 `insufficient_scope` — BRAK ZAKRESU USUWANIA na koncie PLASMET (zweryfikowane na żywo 2026-06-19)

**Konto webapi PLASMET z `.env` NIE MA uprawnienia „usuwanie" (delete scope).** Próba sprzątania
po imporcie (usunięcie konta testowego `user_id=7` + adresów `address_book_id` 6/7) zwróciła
**HTTP 403** z body `{"error":"insufficient_scope","error_description":"The request requires higher
privileges than provided by the access token"}` na **wszystkich trzech** DELETE:
`user-addresses/6`, `user-addresses/7`, `users/7`.

- **Przyczyna = zakres uprawnień tokenu, NIE zła nazwa zasobu ani błąd payloadu.** GET na te same ID
  działa (recon potwierdził tożsamość), więc zasób/ID są poprawne. Brakuje wyłącznie scope `delete`.
- **Token oba przepływy = ten sam efekt:** zarówno permanentny token z `.token.json`, jak i token
  z **starego przepływu `POST /auth` (Basic Auth login+hasło z `.env`)** zwróciły 403. Oba ważne
  ~30 dni (2592000s) → konto ma długotrwały token, ale z zakresem **odczyt+tworzenie(POST)+edycja(PUT)
  BEZ usuwania(DELETE)**. To spójne z historią: POST `users`/`user-addresses` (tworzenie) i PUT
  (edycja) działały, DELETE — nie.
- **403 odrzuca żądanie PRZED wykonaniem** — po 3× 403 stan sklepu nienaruszony (GET potwierdził:
  `users/7` + adresy 6/7 nadal istnieją, `users count` = 432 bez zmian, realne konta 8/432 żyją).
  Bezpieczne: nic się nie skasowało.
- **Jak odblokować usuwanie (panel, akcja usera):** `Ustawienia > Ogólne > Administratorzy sklepu`
  → grupa konta webapi → **Uprawnienia** → przy zasobie „Klienci" (i pozostałych) zaznaczyć poziom
  **z usuwaniem (delete)**. Jeśli używany jest **token permanentny** (Aplikacje i integracje >
  Aplikacje zewnętrzne) — przy tworzeniu/edycji tokenu wybrać zakres obejmujący **„+usuwanie"**;
  zmiana zakresu może wymagać **wygenerowania nowego tokenu** (nowy unieważnia stary → wpisać do `.env`).
- **Wniosek operacyjny:** **kasowanie rekordów (`DELETE`) przez webapi na tym koncie jest dziś
  niemożliwe.** Do potwierdzenia, czy dotyczy WSZYSTKICH zasobów, czy tylko „Klientów" — ale wzorzec
  `insufficient_scope` jest globalny dla scope tokenu. Alternatywy do czasu nadania scope: (a) user
  nadaje uprawnienie delete w panelu i ponawiamy skrypt `cleanup-test-user-step2b-delete-basicauth.ps1`;
  (b) usunięcie konta testowego ręcznie w panelu (Klienci > Klient `user_id=7` > usuń).
- Skrypty: `cleanup-test-user-step1-recon.ps1` (GET, guard tożsamości po emailu),
  `cleanup-test-user-step2-delete.ps1` / `...-step2b-delete-basicauth.ps1` (DELETE z guardem emaila +
  anti-„wiszący zapis"; idempotentnie traktują 404 jako sukces — gotowe do ponowienia po nadaniu scope),
  `cleanup-test-user-step3-verify.ps1` (GET, potwierdza brak zmian).

### Stan na żywym sklepie (GET 2026-06-18)

- **`users` count = 6** — wszystko konta testowe/właścicielskie: `sample@example.com`,
  `email@example.com`, `example@example.com` (3× demo Shopera) + 2 konta właścicielskie (Gmail) +
  1 wykonawcze (`@welikeit.pl`). **Zero kolizji z importem** prawdziwych klientów Mercatum (poza
  ewentualnie kontami właściciela, jeśli były też w starym sklepie — sprawdzić email-em).
- Skrypty rozeznania (TYLKO GET): `rozeznanie-klienci-readonly.ps1` (count+emaile+schemat),
  `rozeznanie-klienci-readonly2.ps1`, `rozeznanie-klienci-readonly3.ps1` (grupy + user-addresses).
  Zrzuty PII → `_rozeznanie/klienci-*.json`, `user-addresses-jeden.json` (gitignore).

## ✅ Newsletter — zasób `subscribers` — ROZEZNANIE READ-ONLY 2026-07-14 (przed 1. mailingiem)

Lista newslettera = zasób **`subscribers`** (potwierdzony sondą GET: HTTP 200). Nazwy alternatywne
**NIE istnieją** (wszystkie → HTTP 400 „Missing MODULE"): `subscriber`, `newsletter`, `newsletters`,
`newsletter-subscribers`, `mailing`, `mailings`, `subscriptions`, `subscribe`, `newsletter-users`,
`contacts`.

- **`GET /webapi/rest/subscribers?limit=50` → `{"count":"0","pages":0,"page":1,"list":[]}`** —
  **ZERO rekordów** na żywym sklepie. Zasób jest pusty, więc **schematu pól nie da się odczytać z danych**
  (brak rekordu wzorcowego); dok. oficjalna jest SPA za loginem → pola (czy jest flaga potwierdzenia
  double opt-in / data zapisu) **pozostają niezweryfikowane** do czasu pojawienia się 1. subskrybenta
  albo dostępu do dok. z panelu. **Nie zakładaj, że pole potwierdzenia istnieje.**
- **Zgoda marketingowa zarejestrowanych klientów** = pole **`users.newsletter`** (string `"0"`/`"1"`).
  Stan na 2026-07-14: **440 kont, `newsletter="1"` → 0 kont** (rozkład surowy: `'0'`: 440).
  Import klientów z Mercatum (2026-06-18 / 07-13) leciał z `newsletter:"0"` → **zgody NIE zostały
  przeniesione** (bo nie było ich w eksporcie starego sklepu).
- **`users.origin`** rozróżnia pochodzenie konta: **`4` = utworzone przez webapi** (nasz import Mercatum,
  433 konta), **`0` = panel/sklep** (7 kont: demo + właścicielskie + techniczne). To wiarygodniejszy
  marker migracji niż sama `date_add`.
- ⚖️ **Wniosek prawny (RODO/PUŚE):** legalna baza mailingowa = **0 adresów**. Konta klientów bez
  `newsletter=1` **nie są** zgodą marketingową — wysyłka do nich jest niedopuszczalna. Bazę trzeba
  zbudować od zera (double opt-in), a zgody zbierać na froncie/w koncie klienta.

## ⚠️ KOREKTA: producent produktu = **top-level `products.producer_id`** — `stock` NIE MA pola `producer_id` (zweryfikowane na żywo 2026-07-14)

Wcześniejsza notatka („czytaj `stock.producer_id`") była **myląca**. Realny obiekt `stock` (39 pól:
`stock_id, extended, price, price_type, price_buying, …, calculated_availability_id, additional_codes`)
**w ogóle nie zawiera `producer_id`** — GET `products/2000` i GET listy zwracają `stock.producer_id` = pusty.
**Producent siedzi WYŁĄCZNIE w top-level `products.producer_id`.** Intencja starej notatki była taka:
agreguj markę po **realnym `producer_id` z PRODUKTÓW**, a nie po liście `producers` (bo Leo dubluje wpisy) —
i to nadal obowiązuje, tylko pole jest top-level.

- **`producers` count = 51** (2026-07-14). Nazwa marki = **top-level `name`** (`translations.pl_PL` **NIE ma
  pola `name`** — ma `translation_id, producer_id, description, lang_id, seo_*, permalink`).
- **ID producentów znów zmigrowały po sync Leo:** Milwaukee = **52** (było 44 → wcześniej 35).
  **Nie polegaj na stałym `producer_id`** — mapuj po `name` + agreguj po produktach.
- Realnie używanych producentów: **20** (mają ≥1 produkt); **31 to sieroty** (0 produktów) — stare/zdublowane
  wpisy Leo, które nadal generują indeksowalne strony `/pl_PL/producer/<Nazwa>/<id>`.
- ⚠️ **`categories.translations.pl_PL.items` NIE jest licznikiem produktów** (kat. 61 → `items = 0` mimo
  produktów w kategorii). Liczbę produktów w kategorii licz z **pełnego skanu `products`** (pola
  `category_id` + tablica `categories`), nie z `items`.
- ✅ **RE-WERYFIKACJA 2026-07-21 (READ-ONLY, skan 7813 prod.):** metoda „pełny skan `products`" potwierdzona.
  Dodatkowe pułapki potwierdzone na żywo: `categories/{id}/products` **NIE jest** endpointem produktów kategorii —
  **ignoruje `{id}`** (nawet `999999`) i zwraca **listę KATEGORII** (`count=285` = łączna liczba kategorii,
  pozycje mają pola kategorii: `category_id/order/root/...`), więc daje fałszywą stałą. Zasób `product-categories`
  → HTTP 400 (nieużywalny). Jedyna wiarygodna droga = paginacja `products?limit=50` + zliczanie przynależności
  z `category_id` (główna) ∪ `categories` (wszystkie). Skrypt wzorcowy: `scripts/shoper-api/booster-fala1-count-scan.ps1`
  (Fala 1 booster: 12 kategorii = 540 produktów, wszystkie liście `categories-tree`). Dok. oficjalna bez zmian
  (WebFetch developers.shoper.pl = SPA/menu; WebSearch potwierdził `filters`+`count/pages/page/list` — zgodne).

## ✅ Zamówienia — zasób `orders` (+ `statuses`, `payments`) — ROZEZNANIE READ-ONLY 2026-07-14

Zamówienie sklepu = zasób **`orders`**. **List endpoint `GET /orders?limit=50` zwraca PEŁNY obiekt**
(z `delivery_address`/`billing_address`, `is_paid`, `additional_fields`) — do przeglądu NIE trzeba GET
per zamówienie. Lista domyślnie **rosnąco po `order_id`** (najnowsze = najwyższe ID = ostatnia strona).
⚠️ **`orders` niesie PII (RODO):** `email`, imię/nazwisko, adres, telefon, `ip_address` w `delivery_address`/
`billing_address` — pobieraj/wypisuj tylko to, co potrzebne; pełny obiekt trzymaj w `_rozeznanie/` (gitignore).

### Pola obiektu (GET `orders/{id}`, PŁASKIE — zweryfikowane na żywo, konto PLASMET)

| pole | znaczenie |
|---|---|
| `order_id` | PK (string) |
| `date` | data **utworzenia** zamówienia `YYYY-MM-DD HH:MM:SS` |
| `status_date` | data **ostatniej zmiany statusu** (dla świeżego = równa `date`) |
| `confirm_date` | data potwierdzenia; **`0000-00-00 00:00:00` = nigdy nie potwierdzone** |
| `delivery_date` | planowana data dostawy `YYYY-MM-DD` |
| `status_id` | ID statusu → nazwa z zasobu **`statuses`** (patrz niżej); nowe zamówienie = **`1` „złożone"** |
| `payment_id` | ID metody płatności → nazwa z zasobu **`payments`** (patrz niżej) |
| `shipping_id` / `shipping_cost` | metoda i koszt wysyłki |
| `sum` | **kwota łączna brutto** (string, np. `"29.94"`) |
| `paid` | **kwota już zapłacona** (`"0.00"` = nic nie wpłacono) |
| `is_paid` | bool — **czy opłacone** (`false` = nieopłacone) |
| `is_cash_on_delivery` / `is_overpayment` / `is_underpayment` | flagi rozliczenia |
| `confirm` | `0/1` — flaga potwierdzenia zamówienia |
| `email` | e-mail klienta (PII) |
| `notes_pub` | **uwagi klienta** (widoczne) — tu ląduje np. wpisane „test" |
| `notes_priv` / `notes` | notatki prywatne / wewnętrzne |
| `ip_address` | IP składającego (PII) |
| `registered` | `0/1` — czy złożone z konta (zalogowany) |
| `origin` | źródło zamówienia (`0` = sklep) |
| `order_url` | link do zamówienia **w panelu** (`…/pl/panel/order/{id}`) — NIE strona podziękowania frontu |
| `payment_url` | URL bramki płatności online (**pusty = brak redirectu do bramki**, typowe dla płatności offline) |
| `total_products` / `total_parcels` | liczba pozycji / paczek |
| `delivery_address` / `billing_address` | obiekty adresu (firstname, lastname, city, postcode, street1, phone, `tax_identification_number`, `country_code`…) — **PII** |
| `additional_fields` | pola dodatkowe formularza (np. zgody `field_value`) |
| `user_id`, `currency_id`, `currency_rate`, `lang_id`, `code`, `discount_*`, `promo_code`, `tags`, `properties`, `children`, `loyalty_*`, `vat_eu`, `shipping_tax_*` | pozostałe |

> ⚠️ **API NIE eksponuje faktu dotarcia na stronę podziękowania/potwierdzenia frontu** (to zdarzenie
> przeglądarki, na którym pali się GA4 `purchase`). Najbliższe sygnały z danych zamówienia: samo istnienie
> rekordu (klient nacisnął „Zamawiam" → zamówienie powstało), `status_id`, `confirm`/`confirm_date`,
> `is_paid`/`paid`. Braku/obecności widoku strony „dziękujemy" **nie da się z API potwierdzić**.

### `statuses` (mapa `status_id` → nazwa, konto PLASMET, 10 statusów)

`1` złożone · `2` zamówienie przyjęte · `3` oczekiwanie na dostawę · `4` w trakcie kompletowania ·
`5` oczekiwanie na płatność · `6` gotowe do wysłania · `7` przesyłka wysłana · `8` anulowane ·
`9` odrzucone · `11` zwrócone.

### 🔴 KOREKTA 2026-07-14: `payments` ma **19** rekordów, a Przelewy24 to **`payment_id=18`** (NIE 7)

**Poprzedni zapis („10 metod", „P24 = `payment_id=7`") był BŁĘDNY.** Zweryfikowane na żywo (produkcja,
`GET /payments` → `count=19`) + potwierdzone dok. Shopera (stara integracja P24 wygaszona 2024-04-15).

**Flaga aktywności NIE jest na top-levelu.** Rekord `payments` ma:
`payment_id`, `name` (nazwa **silnika**, np. `shoperP24`), `order`, `install`, **`visible`** (0/1),
`translations`, `currencies`. **Realny stan metody = `translations.pl_PL.active` (0/1)** + `visible`.
`translations.pl_PL` niesie też `title` (nazwa widoczna dla klienta) i `vendor_description`.
→ **Metoda jest włączona ⟺ `visible=1` ORAZ `translations.pl_PL.active=1`.** Sam `visible=1` nie wystarcza
(np. PayU/DotPay/PayPal/Stripe: `visible=1`, ale `active=0` = zainstalowane, nieaktywne).

| payment_id | `name` (silnik) | `title` (PL) | visible | active | stan |
|---|---|---|---|---|---|
| **1** | `cash` | Gotówka | 1 | **1** | ✅ AKTYWNA |
| **2** | `cod` | Pobranie | 1 | **1** | ✅ AKTYWNA |
| **13** | `zero` | Darmowe zamówienie | 1 | **1** | ✅ AKTYWNA (systemowa, koszyk 0 zł) |
| **18** | `shoperP24` | **Przelewy24** *(pełna integracja, PayPro S.A.)* | 1 | **1** | ✅ **AKTYWNA — to jest P24** |
| 7 | `przelewy24.pl` | Przelewy24.pl *(ograniczona)* | 0 | 0 | ⛔ stara integracja, wygaszona przez Shopera |
| 3,4,5,6,10,11,14,15,16,19,20 | onlinePayment(Autopay), mraty, platnosci.pl(PayU), dotpay.shoper, zagiel, paypal, paypalec, sofort, braintree, inpostPay, stripe | — | 1 | 0 | zainstalowane, NIEaktywne |
| 12, 17, 21 | Allegro, klarna, giftCard | — | 0 | 0 | nieaktywne |

⚠️ **Rozpoznanie zamówienia przez bramkę online:** `payment_id == 18` (a nie 7) **oraz** `payment_url` niepusty.

### `shippings` — 10 metod, tu siedzi **wiązanie dostawa → dopuszczalne płatności**

Rekord: `shipping_id`, `cost`, `engine`, **`active`** (0/1), `visible`, `is_default`, `translations.pl_PL.name`,
`countries`, `ranges`, **`payments`** = tablica `{payment_id, cost, percent}`. **To `shippings[].payments`
decyduje, co klient realnie zobaczy w kasie przy danej dostawie** — metoda płatności `active=1`, ale
niepodpięta pod żadną aktywną dostawę, jest dla klienta niewidoczna. Stan produkcji 2026-07-14:

| shipping_id | nazwa | active | koszt | dopuszczalne płatności |
|---|---|---|---|---|
| 1 | InPost Paczkomaty 24/7 (**domyślna**) | ✅ 1 | 20.69 | **18** (P24) |
| 2 | InPost Kurier | ✅ 1 | 20.69 | **18** (P24) |
| 10 | InPost Kurier (pobranie) | ✅ 1 | 30.00 | **2** (Pobranie) |
| 8 | Odbiór osobisty | ✅ 1 | 0.00 | **1** (Gotówka), **18** (P24) |
| 3,4,5,6,7,9 | Paczka w Weekend, Poczta Polska, DPD, DHL, Orlen Paczka, InPost International | ⛔ 0 | — | — |

`deliveries` (7 rekordów: `delivery_id`, `hours`, `days`, `translations`) = **czasy realizacji**, nie metody wysyłki.
Sonda `payments-channels` → **HTTP 403** (kanały P24 niedostępne dla tego konta webapi); `payment-methods` → 400 (nie istnieje).

Skrypt rozeznania (TYLKO GET, paginacja + retry, PII redagowane w konsoli):
`scripts/shoper-api/orders-recon-readonly.ps1` → pełny obiekt najnowszego zamówienia do
`_rozeznanie/orders-najnowszy-{id}.json` (gitignore).

## ⛔/✅ Opinie o produktach (gwiazdki, `aggregateRating`) - Warstwa 2 SEO (rozeznanie 2026-08-17, domknięte 2026-08-18)

**Podsumowanie: opinii NIE odczytasz przez webapi, ale konfigurację modułu — TAK (`application-config`),
a stan faktyczny — z frontu.** Silnik Storefront sam wystawia `aggregateRating`, gdy oceny istnieją
(dowód na obcym sklepie, niżej) — po naszej stronie nie trzeba nic programować.

### Sonda zasobów (świeży token, GET)

| zasób | odpowiedź | wniosek |
|---|---|---|
| `product-reviews` (i `?limit=1`) | **HTTP 403** `{"error":"insufficient_scope","error_description":"The request requires higher privileges than provided by the access token"}` | zasób **ISTNIEJE** (403 ≠ 400), ale konto webapi PLASMET nie ma zakresu. To **nie** jest błędna nazwa. |
| `comments`, `reviews`, `product-comments`, `opinions` | HTTP 400 `Missing MODULE '<nazwa>'` | nazwy nie istnieją — nie szukać dalej aliasów |

> Uprawnienie do opinii jest odrębne od „Zawartość"/„Produkty". Gdyby kiedyś było potrzebne czytanie
> opinii przez API — trzeba rozszerzyć zakres konta webapi w panelu (albo wygenerować token permanentny
> z szerszym zakresem) i **ponownie zsondować** `product-reviews`.

### Konfiguracja opinii JEST w `application-config` (READ-ONLY; PUT → 501)

Z 97 pól `application-config` opinii dotyczą **dokładnie trzy** (+ trzy blogowe):

| klucz | 2026-08-17 | **stan od 2026-08-18** | odpowiednik w panelu |
|---|---|---|---|
| `comment_enable` | 1 | **1** | „Włącz opinie o produktach" |
| `comment_for_users` | 1 | **0** | „Tylko zalogowani mogą dodawać opinie" |
| `comment_moderation` | 1 | **1** | „Pokazuj opinie dopiero po zatwierdzeniu" (moderacja) |
| `blog_comments_enable` / `_for_users` / `_moderation` | 1 / 0 / 0 | bez zmian | komentarze pod wpisami bloga (osobny zestaw!) |

> **Historia zmiany 2026-08-18** (obie w panelu, bo pola są read-only przez webapi): user najpierw
> zdjął OBIE bariery (`comment_for_users` i `comment_moderation` na 0), a po kilku godzinach włączył
> moderację z powrotem. Stan docelowy to `for_users=0` + `moderation=1`, czyli **bariera wejścia
> zdjęta, kontrola treści zachowana**. Wartości weryfikowane GET-em po każdej zmianie.
>
> ⚠ **W `application-config` NIE MA klucza powiadamiania o opinii oczekującej na zatwierdzenie.**
> Przeszukane wszystkie 97 pól pod `mail|notif|powiad|admin|alert|send`: jedyne trafienia to
> `product_notifies_enable` (powiadomienie o DOSTĘPNOŚCI produktu, nie o opinii), `shop_email`
> i `shopping_parcel_send_status_id`. Przy włączonej moderacji opinia może więc czekać niezauważona;
> czy panel wysyła maila do obsługi, trzeba sprawdzić w panelu.

Panel: **Ustawienia > Zarządzanie produktami > Ustawienia opinii** (starsze nazewnictwo:
`Obsługa sklepu > Opinie nt. produktów` — tam się je moderuje/edytuje). W `application-config`
**NIE MA** przełącznika maila „prośba o opinię" ani reCAPTCHA — to warstwa panelu, poza webapi.

### Jak czytać stan opinii bez webapi (front, renderowany SERWEROWO)

Moduły Storefront `product_rating` i `product_review` renderują liczby **w statycznym HTML** (nie w JS),
więc wystarczy `GET` karty produktu i regex:

- `product-rating__score">0.00<` → średnia ocena,
- `product-rating__number-of-votes">(Oceny: 0 Recenzje: 0)` → licznik ocen i recenzji,
- `product-review__rate-count">Liczba ocen: 0` → licznik w zakładce „Opinie".

### `aggregateRating` w JSON-LD — Shoper robi to NATYWNIE (dowód z obcego sklepu Storefront)

Karta produktu Shopera składa schema.org **z wielu fragmentów `<script type="application/ld+json">`
sklejanych po `@id`** (każdy moduł dokłada swój kawałek: `image`, `name`, `description`, `sku/gtin`,
`offers`, `Brand`, `potentialAction`). Moduł `product_rating` **przy zerowych ocenach nie emituje
żadnego fragmentu** (zweryfikowane: 0 bloków w module id 93 na PLASMET), a przy istniejących ocenach
emituje `aggregateRating` — potwierdzone na żywym sklepie demo Storefront `demo-445325.shoparena.pl`
(42 oceny, 1 recenzja), gdzie moduł `product_rating` wypluwa:
`{"@id":"/pl/p/…/160","aggregateRating":{"@type":"AggregateRating","ratingValue":"5","reviewCount":"42"}}`,
a moduł `product_review` osobny fragment `"review":[{"@type":"Review","author":…,"reviewBody":…,"datePublished":…}]`.
→ **Nie trzeba dorabiać JSON-LD w motywie.** ⚠️ Fragment `review[]` Shopera **nie ma `reviewRating`** —
to potencjalne ostrzeżenie w Rich Results Test (gwiazdki i tak niesie `aggregateRating`).

### Pułapki techniczne złapane przy tym rozeznaniu (oszczędzają godziny)

1. **Filtr listy po wielu ID:** `filters={"product_id":["a","b"]}` jest **po cichu IGNOROWANY** —
   API zwraca `count=7888` (cały katalog) i pierwsze 50 rekordów. Działa **`filters={"product_id":{"in":["a","b"]}}`**
   (zweryfikowane: `count=3` dla 3 ID; 117 ID w 5 paczkach po 25). Zawsze sprawdzaj `count`, zanim uznasz filtr za działający.
2. **`Invoke-WebRequest`/`HttpWebRequest` wieszają się na permalinkach kończących się kropką przed ukośnikiem**
   (np. `…-100-szt./1909`): .NET kanonizuje ścieżkę → sklep odbija **301** na URL kanoniczny → pętla
   przekierowań (albo wielominutowe zwisy). Lek: **`curl.exe --path-as-is -L`** (HTTP 200) albo ręczne
   śledzenie `Location`. Wzorzec gotowy: `scripts/shoper-api/w2_scan_front.py`.
3. Front sklepu odpowiada wolno (~8 s/kartę, HTML karty ~830 kB) — skan katalogu planuj **sekwencyjnie,
   przyrostowo (JSONL) i wznawialnie**, nie jednym przebiegiem w pamięci.

Skrypty (TYLKO GET): `w2-opinie-recon.ps1` (sonda zasobów + `application-config` + ranking kupionych z `order-products`),
`w2-permalinki-all.ps1` (permalinki filtrem `in`), `w2-pdp-probe.ps1` (zrzut 1 karty + wykaz bloków JSON-LD),
`w2_scan_front.py` (masowy skan frontu). Zrzuty: `scripts/shoper-api/_w2-opinie/`.

## Jak utworzyć dostęp w panelu (jeśli trzeba odtworzyć)

`Ustawienia > Ogólne > Administratorzy sklepu` → grupa z typem **„dostęp do webapi"** → zakładka
**Uprawnienia** (produkty, kategorie, producenci, atrybuty, zamówienia, klienci, przekierowania,
strony CMS, konfiguracja) → **Administratorzy → Dodaj administratora** (login+hasło) → wpisz do `.env`.

## Oficjalna dokumentacja (źródła do weryfikacji)

- **REST API reference:** https://developers.shoper.pl/ (sekcja „REST API" — produkty, zamówienia,
  klienci, wysyłka). Strona jest **SPA** — `WebFetch` często zwraca samo menu; wtedy `WebSearch`
  na zmiany/changelog (np. „Shoper REST API changelog 2026", „developers.shoper.pl products endpoint").
- **Getting started:** https://developers.shoper.pl/developers/api/getting-started
- **Webhooks / OAuth 2.0 / AppStore / Front API:** sekcje na developers.shoper.pl.
- Pomocniczo (panel/operacyjne): https://www.shoper.pl/learn — „Jak utworzyć dostęp po API".

## Metadane weryfikacji

- **Ostatnio zweryfikowano:** 2026-08-17 (**rekonesans danych pod partię D bloga – READ-ONLY, zero zapisów**).
  **Dokumentacja oficjalna: bez zmian merytorycznych.** Weryfikacja: `WebFetch` na `developers.shoper.pl/`
  oraz `/developers/api/resources/products` i `/resources/news` → **SPA + panel logowania** (zwraca samo menu
  i formularz „Sign In", wprost odmawia pól); `WebSearch` na changelog REST → brak nowego changelogu Shopera
  (wyniki to Shoptet/Shopify). Wniosek bez zmian: **źródłem prawdy pozostaje żywe API**.
  **Nowe fakty (potwierdzone na żywo, produkcja):**
  1. **Skala katalogu 2026-08-17:** `products` **7 888**, `categories` **286**, `producers` **52**
     (poprzednio w dumpach: 7 885 / 252 / 49) → liczby rosną przy każdym sync Leo, nie hardkodować.
  2. **`news` na produkcji: 64 wpisy, wszystkie `active=1`** (`news_id` 8…73, daty 2026-06-10 → 2026-08-17).
     Obiekt `news` GET **nie ma pola `permalink` ani `translations`** (pola: `active, author, box, content, date,
     image_name, lang_id, name, news_id, order, seo_description, seo_keywords, seo_title, seo_url, short_content,
     start_page, tags`) → **URL wpisu składa się ręcznie: `https://<host>/<seo_url>`** (root domeny).
     Sprawdzone HTTP na wszystkich 64 wpisach: **64/64 = 200**, zero 404 (potwierdza [[blog-url-i-grupa-tresci-ga4]]).
  3. **`news-categories` ma PŁASKIE `name`** (nie `translations.pl_PL.name` – czytanie przez translations daje
     `null`). Kanoniczne 6 kategorii bloga: 5 Poradnik, 6 Krok po kroku, 7 Problemy i porady, 8 Porównania,
     9 Normy i BHP, 10 Rankingi. Mapowanie wpis→kategoria tylko filtrem `GET /news?filters={"category_id":"N"}`
     (rozkład 64 wpisów: 36/6/9/7/6/0).
  4. **`categories-tree` zwraca WYŁĄCZNIE `{id, children}`** – bez nazw i bez `parent_id`; hierarchię trzeba
     złożyć samemu (join z płaskim `categories`). Drzewo: 9 korzeni (38 Podstawowa, 39, 42, 44, 58, 61, 64, 96, 116).
  5. **Pułapka semantyki kategorii (SEO/treść):** `298` = **Silikony wysokotemperaturowe** (dziecko `80 Silikony`),
     a `74` = **Uszczelniacze wysokotemperaturowe** (dziecko `67 Uszczelniacze`) – to DWIE różne kategorie o
     podobnej nazwie; `314 Przedłużacze` wisi pod **`58 Narzędzia ręczne`**, nie pod `61 Elektronarzędzia`;
     folie kubełkowe leżą w `95 Folie fundamentowe` (pod `88`), a nie w `84 Hydroizolacje`. Zanim opiszesz
     kategorię w treści – sprawdź rodzica i zawartość, nie samą nazwę.
  6. **Throttling na `GET products/{id}`:** przy ciągu ~80 żądań sekwencyjnych **11/77 padło** (timeout/przerwane
     połączenie) i **wszystkie 11 przeszło przy retry** → nawet czysty odczyt wymaga retry z backoff.
     Dodatkowo: w PowerShell nieudany `HttpWebRequest` trzeba **domknąć** (`$_.Exception.Response.Close()`),
     bo przy `DefaultConnectionLimit=2` wycieki połączeń wywracają kolejne żądania.
  7. **Pułapka PowerShell 5.1 (nie API):** `$tab | ConvertTo-Json` na tablicy obiektów potrafi zapisać
     `{"value":[…],"Count":N}` zamiast czystej tablicy → **używaj `ConvertTo-Json -InputObject $tab`**,
     a przy czytaniu obcych zrzutów sprawdzaj `if ($o.PSObject.Properties.Name -contains 'value')`.
     Druga pułapka: `$N = @{}` + `foreach ($n in …)` to **ta sama zmienna** (case-insensitive) → nadpisuje mapę.
  8. **Weryfikacja URL zdjęcia produktu** (wzorzec z `product-cards.ps1`) działa 1:1 na produkcji:
     `…/environment/cache/images/productGfx_<unic_name>_300_300/<name>.webp` → 200 dla **77/77** kandydatów.
  Skrypty (READ-ONLY): `b2g-katalog-dump.ps1` (reużyty z `-OutDir`), zrzuty i buildery w scratchpadzie sesji;
  produkty rekonesansu: `blog/queue/_kafelki-partiaD-72-81.json`, `blog/queue/_linki-partiaD.json`.
- **Poprzednio zweryfikowano (ten sam dzień):** 2026-08-17 (**Warstwa 2 SEO — audyt opinii/`aggregateRating`, READ-ONLY**).
  **Dokumentacja oficjalna: bez zmian merytorycznych dla naszych zasobów.** Weryfikacja: `WebFetch`
  `developers.shoper.pl/developers/api/resources/product-reviews/get` oraz `/resources` → **SPA, samo menu
  i panel logowania** (wprost odmawia zwrócenia pól); próba pobrania specyfikacji maszynowej
  (`/docs/openapi.json`, `/openapi.json`, `/docs/spec.json`, `/sitemap.xml`) → **HTTP 403** (ochrona przed
  botami) → dokumentacji zasobu `product-reviews` **nie da się zweryfikować zdalnie**; opieramy się na
  odpowiedziach żywego API. Uzupełniająco `WebSearch` + `shoper.pl/learn` (artykuł „Opinie o produkcie")
  potwierdzają nazwy opcji panelu 1:1 z kluczami `application-config`.
  **Nowe fakty dopisane (sekcja „Opinie o produktach")**: `product-reviews` = 403 `insufficient_scope`
  (zasób istnieje, brak zakresu); `comments`/`reviews`/`product-comments`/`opinions` = 400 Missing MODULE;
  3 klucze opinii w `application-config` (`comment_enable`/`comment_for_users`/`comment_moderation` = 1/1/1);
  natywny `aggregateRating` emitowany przez moduł `product_rating` (dowód: sklep demo Storefront);
  filtr `{"product_id":{"in":[…]}}` działa, a `{"product_id":[…]}` jest cicho ignorowany;
  pętla 301 w .NET na permalinkach typu `…szt./ID` (lek: `curl --path-as-is`).
- **Poprzednio zweryfikowano:** 2026-08-12 (**AKTUALIZACJA treści strony B2G `aboutpages/16` — dopisana sekcja
  „Broszury dla jednostek"**). **Dok. API bez zmian merytorycznych** (WebFetch
  `developers.shoper.pl/.../resources/aboutpages` → SPA, samo menu, wprost odmawia zwrócenia pól; WebSearch:
  nadal wersja **2026.1** z 2026-03-07, wsteczna zgodność, zero zmian w `aboutpages`). Fakty z żywej edycji:
  1. **PUT pełnej treści na ISTNIEJĄCEJ stronie działa tak samo jak przy tworzeniu:** 42 713 zn. źródła /
     53 kB payloadu → HTTP 200/`1`, live **41 304 zn.** (poprzednio 34 147). Ubytek 1 409 zn. = **tylko**
     komentarze HTML (0 w live) + `sizes` (5) + `decoding` (5). `name` nietknięty (`-ceq` PASS) → FAQPage
     z modułu 237 dalej renderuje się **1×**.
  2. **`target="_blank"` PRZEŻYWA sanitizer** (8/8 linków PDF), `rel="noopener"` → **`rel="noreferrer"`**
     (nofollow/noopener przepada; JS modułu 237 i tak dokłada `target` obronnie, więc bez dubla).
     `data-*` (`data-broszura` 6/6) i `<img width/height>` (11/11) przechodzą 1:1.
  3. **Diff tokenowy stara↔nowa treść = 17 bloków, wszystkie ADDITIVE** (zero ubytków): sekcja
     `b2g-broch` (3 762 zn. w live), 10× `aria-hidden="true"` na numerkach, 6× dekoracyjny
     `<span class="b2g-ico …">`, `role="region"`+`aria-label` na sticky barze. Wzorzec kontrolny wart
     powtarzania: **GET przed PUT → wycięcie nowej sekcji z live → diff tokenowy z backupem** (łapie ciche
     ubytki, których nie widać w samej długości).
  4. Warstwa wyglądu (kanał `shoper-cli`) była gotowa **przed** wgraniem treści: skin ma reguły
     `.b2g-broch*` (25 wystąpień) i wszystkie 6 wariantów `.b2g-ico_*` z data-URI SVG → nowa sekcja od razu
     wygląda docelowo, bez pustych kafli.
  5. Zasoby broszur (6 PDF + 6 miniatur WebP) leżą w `/userdata/public/assets/` — HEAD 200 na **12/12**
     (PDF-y 0,77–1,86 MB, `application/pdf`; miniatury 19–36 kB, `image/webp`).
  Skrypty: `scripts/shoper-api/b2g-page-publish.ps1` — dodany **`-Step backup`** (GET → `backup/b2g-page-{id}_backup_<stamp>.json` + `.html`);
  backup przed tą edycją: `backup/b2g-page-16_backup_20260812-164552.{json,html}`.
- **Ostatnio zweryfikowano (poprz.):** 2026-08-12 (**PUBLIKACJA PODSTRONY B2G — pierwszy realny `POST aboutpages`
  + przepięcie reguły 301 na stronę informacyjną**). **Dok. API bez zmian merytorycznych** (WebFetch
  `developers.shoper.pl/.../resources/aboutpages` i `.../redirects` → SPA, samo menu; WebSearch: nadal
  wersja **2026.1**, wsteczna zgodność, `redirects` wymaga wyższych uprawnień API — mamy je). Fakty z żywego wdrożenia:
  1. **`POST /aboutpages` utworzył stronę `page_id=16`** („Sklep dla instytucji i samorządów",
     `seo_url=Dla-instytucji-i-samorzadow`, `active=0` → potem `1`). `aboutpages` count **11 → 12**.
     **`name` z polskimi znakami wraca z GET 1:1** (porównanie case-sensitive `-ceq` PASS) — bezpieczne dla
     warunków Twig porównujących nazwę strony znak w znak.
  2. **Duży `content` (38 768 zn. / 48 kB payloadu) zapisuje się jednym PUT-em** — HTTP 200/`1`, bez dzielenia
     na części. Po sanitizerze 37 531 zn.; **tekst treści identyczny ze źródłem** (49/49 nagłówków, 18/18 linków,
     8/8 kotwic `data-anchor`, mount-point zachowany), ubytek = komentarze HTML + `sizes`/`decoding`.
  3. **Korekta mapy sanitizera:** `srcset` na `<img>` **przeżywa**; wycinane są `sizes`, `decoding`
     i **komentarze HTML**; `rel="noopener"` → `rel="noreferrer"` (potwierdzone ponownie).
  4. 🔴 **Literalny `<script>` w tekście ucina resztę treści** (patrz sekcja `aboutpages`) — cichy ubytek przy
     HTTP 200, wykrywalny wyłącznie porównaniem długości GET-em.
  5. **Front:** strona informacyjna z `seo_url` żyje w roocie (`/Dla-instytucji-i-samorzadow`), `/pl/i/<slug>/<id>`
     przekierowuje na root, canonical = wersja root. Motyw renderuje **2 znaczniki `<h1>`** (natywny moduł
     `info_page_title`, `data-module-id=50` + H1 z treści) — natywny chowa się CSS-em motywu
     (`.grid__col:has(.b2g-page) .module[data-module-name="info_page_title"]{display:none}`), oba moduły siedzą
     w tym samym `.grid__col`, więc `:has()` działa. `<title>` = `name` + sufiks nazwy sklepu (bo `seo_title`
     nadal READ-ONLY przez webapi).
  6. **`redirects` `type=4` (strona informacyjna) potwierdzony na żywej mapie i HTTP:** 14 reguł `type=4`
     (np. `/o-nas*` → `type=4`/`object_id=8` = „O firmie", HEAD → 301 → `/pl/i/O-firmie/8` → 200).
     **PUT na istniejącej regule zmienia `type` + `object_id`** (reguła 12890 `/instytucje`: `type=2`/61 →
     `type=4`/16; HEAD → 301 → `/Dla-instytucji-i-samorzadow` → 200). ⚠️ Po PUT `lang_id` wraca z GET **pusty**
     (mimo wysłania `1`) — reguła mimo to działa; identycznie wyglądają starsze reguły `type=4` z importu.
     Rozkład typów w mapie na dziś: `type=1` **11 411**, `type=2` **1 461**, `type=4` **14**, reszta 0.
  7. ⚠️ **Testy 301 rób metodą HEAD.** GET/HEAD na ścieżce bez reguły (`/nie-ma-takiej-sciezki`, `/instytucje?utm_…`)
     **zrywa połączenie → HTTP 0**, nie 404 — kontrola na losowej ścieżce odróżnia to od awarii reguły.
  Skrypty: `scripts/shoper-api/b2g-page-publish.ps1` (create/put/get/activate/front), `b2g-vanity-repoint.ps1`
  (recon/probe/apply/rollback/check); backup reguły: `_backup-redirect-12890-20260812-124529.json`.
- **Ostatnio zweryfikowano (poprz.):** 2026-08-12 (**SONDA SANITIZERA `aboutpages.content` — kontrolowany zapis na
  stronie testowej, posprzątany DELETE-em**). **Dok. API bez zmian merytorycznych** (WebFetch
  `developers.shoper.pl/.../resources/aboutpages` → SPA, samo menu; WebSearch nie ujawnia schematu pól POST —
  weryfikacja musiała iść empirycznie). Nowe fakty (szczegóły w sekcji `aboutpages` wyżej + tabela
  `docs/b2g/podstrona/sonda-sanitizer.md`):
  1. **`POST` i `DELETE` na `aboutpages` DZIAŁAJĄ** (POST zwraca nowe `page_id` w body; DELETE czyści rekord
     i front → 404). Sklep przed i po sondzie: `count=11`, zero sierot.
  2. **Pełna mapa sanitizera HTML** `content`: wycinane `<script>`, `<style>`, inline `<svg>`, `<input>`,
     `<picture>`/`srcset`, `on*`, `javascript:`, `loading`, `download`; rozpakowywane (tag ginie, tekst zostaje)
     `<form>`, `<details>/<summary>`, `<textarea>`, `<select>/<option>`, `<button>`, `<label>`;
     przeżywają 1:1 `<table>`, listy, `div/span` z `class` + `data-*` + `aria-*`/`role`, `<img>`, `<iframe>`,
     `mailto:`/`tel:` z parametrami, **pusty div jako mount-point**.
  3. **`id` w treści dostaje prefiks `user_`** (kotwice i `data-target` trzeba pisać jako `#user_…`),
     `rel="nofollow"` jest nadpisywany na `noreferrer`, atrybuty sortowane alfabetycznie.
  4. **`style` inline filtrowany whitelistą** (bez `grid`, `gap`, `max-width`, `border-radius`, `box-shadow`,
     `position`, `z-index`, `justify-content`) → layout wyłącznie klasami motywu.
  5. **Front renderuje 1:1 zawartość z GET** (moduł `info_page_content` 49), treść nie jest w `<form>` motywu;
     `seo_url` daje URL w roocie domeny.
  6. 🔴 **Pułapka PowerShell: `Get-Content -Raw` + `ConvertTo-Json` → HTTP 500** (content leci jako obiekt
     z `PSPath`/`PSDrive`); obowiązkowe rzutowanie `[string]`, zakaz `-Depth` dla płaskich payloadów.
  Skrypty: `scripts/shoper-api/sonda-sanitizer-aboutpages.ps1`, `sonda-sanitizer-markery.ps1`,
  `sonda-put-html.ps1`, `sonda-diag-500.ps1`; dane surowe `_sonda-markery.json`, `_sonda-*.html`.
- **Ostatnio zweryfikowano (poprz.):** 2026-08-12 (**BAZA PRODUKTOWA POD PAKIETY B2G – pełny skan katalogu, 100% READ-ONLY,
  zero zapisów do API**). **Dok. API bez zmian merytorycznych** (WebFetch `developers.shoper.pl/.../resources/products`
  → SPA za loginem, samo menu; WebSearch: Shoper API **2026.1** z 7.03.2026 – „rozszerzony dostęp do danych zamówień
  i produktów, poprawiona obsługa limitów zapytań", **wsteczna zgodność zachowana**; `limit` max **50**, `page`,
  `filters`, kształt `count/pages/page/list` bez zmian). Fakty potwierdzone na żywo:
  1. **Katalog: `products` count = 7 885** (158 stron × `limit=50`), `categories` **286**, `producers` **52**.
  2. **`stock.price` = cena BRUTTO** – potwierdzone krzyżowo na froncie karty produktu (prod. 93: API 406.53
     vs front „406,53 zł" i „330,51 zł bez 23% VAT"). Nie mylić z `price_buying_net`/`price_wholesale`.
  3. **URL zdjęcia głównego** działa w 4 wariantach (wszystkie HTTP 200): cache
     `/environment/cache/images/productGfx_<unic_name>_<W>_<H>/<name>.<ext>` (rozmiar generowany **na żądanie** –
     `400_400` też 200), ten sam z `.webp`, oraz surowe `/userdata/public/gfx/<unic_name>.<ext>` i
     `/userdata/gfx/<unic_name>.<ext>`. Do zestawień danych najbezpieczniejszy jest wariant cache z oryginalnym `ext`.
  4. **Producent = top-level `products.producer_id`** (potwierdza korektę z 2026-07-14). Rozkład marek w podzbiorze
     B2G (2 114 poz.): MILWAUKEE 1 370, RICHMANN 608, „SCHEDPOL NIEAKTUALNE" 70, brak producenta 24,
     „CONKRET TREJDEROWSCY" 23, BAUM 18, MASTERPLAST 1 → **duble/śmieci Leo nadal żywe w `producers`**,
     nazwę marki do prezentacji trzeba czyścić (sufiks „NIEAKTUALNE", pełne nazwy prawne).
  5. **Pole `stock.sold` jest znikome** (max 10 szt. na produkcie) – sklep żyje od lipca 2026, więc **`sold` nie
     nadaje się jako główne kryterium rankingu** produktów; sensowniejszy jest stan + cena + marka.
  6. ⚠️ **Duble kategorii po Leo są nadal żywe i jedna kopia bywa PUSTA** – potwierdzone liczeniem produktów:
     „Dmuchawy" 155 = **0** / 301 = 13; „Piły łańcuchowe" 118 = **0** / 300 = 21; „Kosiarki" 204 = **0** / 303 = 7;
     „Podkaszarki i wykaszarki" 154 = **0** / 293 = 14; „Elektronarzędzia ogrodowe" 117 i 287 = **0/0**;
     „Inne narzędzia ręczne" 195 = **0** (kategoria-widmo). ⇒ **nigdy nie filtruj po jednym `category_id`
     „bo nazwa pasuje"** – zawsze sprawdź obie kopie, inaczej wyjdzie fałszywe „nie mamy tego w katalogu".
  7. **`redirects` – filtry serwerowe (rozeznanie 2026-08-12):** `filters={"route":"/instytucje"}` **działa**
     (jedno żądanie zamiast 258 stron paginacji) i jest właściwym testem idempotencji; `filters={"type":"2"}`
     też działa (zwrócił `count=1460`), ale **kombinacja `{"type":"2","object_id":"61"}` → HTTP 404**
     (nieobsługiwana). ⚠️ **Paginacja całej mapy 301 bez throttlingu = HTTP 429** już po kilkunastu stronach –
     przy `redirects` zawsze filtruj serwerowo albo dodaj opóźnienie + backoff.
  8. **Wzorzec żywej reguły kategorii** (do kopiowania przy wanity URL): `redirect_id=3`, `type=2`,
     `object_id=61`, `lang_id=1`, `target=''`, `route=/produkty/elektronarzedzia` (wiodący slash, **bez `*`**).
     Kategoria główna „Elektronarzędzia" = **id 61**, `root=1`, permalink `/pl/c/Elektronarzedzia/61`.
  9. **Dane firmy do stopek/broszur są w `application-config`** (READ-ONLY): `shop_company_name`,
     `shop_address_1`, `shop_zip_code`, `shop_city`, `shop_province`, `shop_phone`, `shop_tax_id`.
     ⚠️ `shop_full_address` jest **percent-encoded** (`Radoszewskiego%2019-21%2C%20Kalisz%2C%20PL`) –
     do prezentacji dekodować albo składać adres z pól atomowych.
  Deliverables: `docs/b2g/dane/pakiety-produkty.json` + `docs/b2g/dane/pakiety-produkty.md`.
  Skrypty (READ-ONLY, reużywalne): `scripts/shoper-api/b2g-katalog-dump.ps1` (zrzut katalogu + słowniki),
  `scripts/shoper-api/b2g-klasyfikacja.py` (klasyfikacja + raport), `scripts/shoper-api/b2g-weryfikacja.ps1`
  (kontrola próbki wobec żywego API + test HTTP kart i zdjęć), `scripts/shoper-api/b2g-explore.py` (grep po zrzucie).
- **Ostatnio zweryfikowano (poprz.):** 2026-08-10 (**ANALIZA BEZPIECZNEGO PODZBIORU GWIAZDEK w `redirects` — 100% READ-ONLY,
  zero zapisów do API**). **Dok. API bez zmian** (WebFetch `developers.shoper.pl/.../resources/redirects` → SPA za
  loginem, samo menu; WebSearch potwierdził istnienie endpointu `redirects` + artykuł „Masowy import przekierowań 301
  przez API"; pola `route`/`type`/`object_id`/`lang_id` i throttling bez zmian). Nowe fakty operacyjne:
  1. **Bug query stringa ŻYJE (potwierdzone HEAD-em na produkcji 2026-08-10, 3 buckety):** `/kontakt.html`,
     `/produkt/<slug>` i `/produkty/…/<slug>.html` (reguły `type=2`/`type=4` bez `*`) dają **301 bez parametru
     i 404 z `?srsltid=`**. Reguły `type=1` z `*` działają.
  2. **Żywa mapa: 12 885 reguł** (258 stron × `limit=50`; było 12 888 w lipcu — różnica 3, bez śladu kasowania
     po naszej stronie). Rozkład: `type=1` 11 411 (**100 % z `*`**), `type=2` 1 460 (0 z `*`), `type=4` 14 (0 z `*`).
  3. **`type=2` ≠ „kategoria" w sensie ścieżki:** tylko **259** z 1 460 reguł `type=2` to realne ścieżki drzewa
     kategorii Mercatum. Reszta to route'y produktowe celujące w kategorię-fallback: **960** `…​.html`,
     **199** forma pojedyncza `/produkt/<slug>` (zgadza się z bucketem GSC), **42** pliki SDS `/_data/attachments/….pdf`.
     ⇒ zakaz gwiazdki „bo `type=2`" był **zbyt szeroki**; ryzyko over-matchu ma tylko ta mniejszość, która realnie
     jest prefiksem innych reguł.
  4. **Wynik analizy:** z 1 474 reguł bez `*` **1 217 jest bezpiecznych** (1 209 = pod route nie zaczyna się ŻADNA
     inna reguła; 8 = wszystkie rozszerzenia prowadzą na TEN SAM cel, np. `/kontakt` vs `/kontakt.html` → obj 9),
     **257 zostaje** (ścieżki drzewa kategorii — luka po stronie silnika Shopera).
  5. 🔴 **PUŁAPKA POWERSHELL (kosztowała fałszywy wynik):** `[Array]::Sort($keys, $items, [StringComparer]::Ordinal)`
     w PS 5.1 **NIE permutuje tablicy `items`** (sortuje tylko klucze) → tablice równoległe się rozjeżdżają i trafienia
     lądują na złych rekordach. Zweryfikowane testem 3-elementowym. **Wzorzec bezpieczny:** sortuj samą tablicę kluczy
     + mapa `hashtable bare → List[reguła]`, albo sortuj obiekty własnym `Comparison`. Zawsze waliduj wynik skanu
     kontrolnym zliczeniem na surowych danych (tu: `/produkty/elektronarzedzia` ma 3 406 rozszerzeń, a skan mówił „0").
  6. **Higiena:** 1 duplikat route (7555 i 8213, oba `*` → produkt 1909) — pozostałość eksperymentu, do `DELETE 8213`.
  Deliverables: `migracja/przekierowania/gwiazdki-bezpieczne-2026-08.csv` (+ `.md`),
  dump `migracja/przekierowania/_dump-redirects-2026-08-10.json`.
  Skrypt (READ-ONLY, reużywalny): `scripts/shoper-api/redirects-star-safety-scan.ps1` (`-SkipFetch` = analiza z dumpu).
- **Ostatnio zweryfikowano (poprz.):** 2026-07-20 (**POLE `booster` = „Hasła w wyszukiwarce sklepu" / Frazy alternatywne —
  ODKRYCIE + no-op smoke-test + TEST DŁUGOŚCI 500 zn. (pilot Packout); READ + idempotentne PUT-y za zgodą zadania**). **Obala** wniosek reconu
  2026-07-19, że frazy alternatywne „NIE są w webapi" (patrz KOREKTA przy mechanizmie 1 wyżej). Ustalenia na żywo:
  1. **`translations.pl_PL.booster` = „Hasła w wyszukiwarce sklepu" (Frazy alternatywne).** Potwierdzenie krzyżowe:
     (a) user wpisał frazy w panelu → eksport CSV nazwał kolumnę **`booster`**; (b) oficjalny Shoper Learn „Pola CSV
     produktów" opisuje **`booster` = „Frazy alternatywne""** (typ: tekst/liczby); (c) GET webapi prod. **1720**
     („Skrzynia Milwaukee Packout 3") zwrócił `translations.pl_PL.booster` = `" walizka, walizka na narzędzia,
     skrzynka transportowa"` (53 zn., **z wiodącą spacją** hex 0020 — artefakt panelu/CSV, do przycięcia przy imporcie).
  2. **Separator = `, ` (przecinek+spacja).** Zgodne z dok. („frazy oddzielone przecinkami"). Niewidoczne dla klienta.
  3. **ZAPIS przez webapi DZIAŁA (potwierdzony na żywo):** PUT `products/1720` z `{translations:{pl_PL:{booster:<ta sama
     wartość>}}}` → **HTTP 200, body `1`**; GET po zapisie = wartość identyczna bit-w-bit; sąsiedzi (`name`,`seo_title`,
     `seo_url`, `description` len 1077, `short_description` len 258, `seo_keywords`) **niezmienieni** — partial-PUT
     `translations.pl_PL.booster` merge'uje (spójne z regułą partial-PUT). Wzorzec zapisu: HttpWebRequest + deadline (anti-zwis).
  4. **Stan katalogu:** próbka 30 prod. z 6 rozłożonych stron → **0/30 niepuste `booster`** (poza testowym 1720) ⇒
     pole faktycznie czyste w całym katalogu, gotowe do zapełnienia; nie jest używane do innego celu.
  5. **Ryzyko nazwy „booster" = NISKIE.** Oficjalny Shoper Learn („Frazy alternatywne") wprost: *„To nie jest mechanizm
     płatny ani sponsorowany"* — mimo anglojęzycznej nazwy to zwykłe dodatkowe frazy wyszukiwania (Premium), NIE płatne
     wybijanie w wynikach. Brak w dok. osobnego mechanizmu „booster" jako sponsoringu.
  6. **Limit długości:** **brak udokumentowanego twardego limitu** (dok. CSV/Learn nie podaje). ⚠️ W Shoperze bywają
     pola z cichym obcięciem (por. pole zgody newsletter = 255 zn., „cicho nie zapisuje") → **przed bulkiem** zrobić
     mały, ograniczony test długości (np. 255 vs 1000 zn., idempotentny, za zgodą) zanim wyślemy długie frazy na skalę.
     ✅ **TEST 500 ZN. WYKONANY 2026-07-20 (prod. 1720, za zgodą, oryginał przywrócony):** PUT `translations.pl_PL.booster`
     = string **dokładnie 500 znaków** (= 500 bajtów UTF-8) → **HTTP 200, body `1`**; GET po zapisie = **500/500 znaków,
     bit-w-bit, ZERO obcięcia** (`was_truncated=false`). Oryginał (53 zn.) przywrócony PUT-em, `restored_ok=true`.
     ⇒ **pole `booster` przyjmuje ≥500 zn. bez cichego truncate** — 255 NIE jest limitem tego pola (inaczej niż zgoda
     newslettera). Dla realnych fraz alternatywnych (kilkanaście–kilkadziesiąt zn.) margines jest ogromny; gdyby kiedyś
     potrzebne były dłuższe payloady (>1000 zn.), powtórzyć test na wyższej granicy. Skrypt: `booster-length-test-1720.ps1`
     (buduje string 500 zn., PUT+GET+pomiar, przywraca oryginał — HttpWebRequest+deadline). Zrzut: `_rozeznanie`/scratchpad.
  7. **Drift auth:** `POST /webapi/rest/auth` na koncie PLASMET zwraca teraz `expires_in=2592000` (**30 dni**), nie 3600 s —
     token żyje dużo dłużej (wygodne dla operacji masowych; i tak odświeżać w długich zadaniach). Skrypty:
     `booster-recon.ps1` (READ-ONLY), `booster-noop-test.ps1` (1 no-op PUT + weryfikacja). Zrzut: `_rozeznanie` w scratchpad.
  8. **BULK REALNY 6 produktów (491–495, 513) — WYKONANY 2026-07-20 (za zgodą zadania):** PUT `products/{id}`
     `{translations:{pl_PL:{booster:<fraza>}}}` na 6 produktach (skrzynki/torby/pianka Milwaukee Packout) → **6/6 HTTP 200**,
     GET po zapisie **6/6 verified bit-w-bit** (`-ceq`), sąsiedzi (`name`, `seo_url`) niezmienieni. Wszystkie miały `booster`
     PUSTY przed zapisem. ⚠️ **KLUCZOWE: webapi PUT NIE dokleja wiodącej spacji** — `after_value` == wysłany string co do bajtu
     (hex bez `0020` na początku); artefakt wiodącej spacji z pkt 1 pochodzi z **panelu/CSV**, NIE z zapisu przez webapi
     (TrimStart nie był potrzebny). Bulk-skrypt: `booster-bulk-update.ps1` (`-DryRun` domyślnie, `-Live` = zapis; retry/backoff
     429/5xx, throttling ~400ms, dane wejściowe czytane jawnie jako UTF-8, wyniki → JSON).
  8. **⚠️ PUŁAPKA KODOWANIA przy bulku `booster` (złapana 2026-07-20 na 6 prod. 1277/1311/1319/1323/1365/1391).**
     Polskie frazy alternatywne (`ę`, `ś`, …) **NIE mogą siedzieć jako literały w pliku `.ps1`** — PowerShell 5.1
     czyta skrypt **bez BOM jako CP1250**, więc literał `narzędzia` (UTF-8 `C4 99`) zamienia się w mojibake
     `narzÄ™dzia` **jeszcze przed wysłaniem**; PUT idzie z uszkodzonym stringiem, a naiwna weryfikacja
     (uszkodzony literał `-ceq` uszkodzona wartość z API) **fałszywie zwraca `exact=True`**. Objaw wykrywalny:
     **długość** zapisanej wartości > oczekiwanej (każde `ę`→`Ä™` = +1 zn.) oraz obecność znaków `0x00C4`/`0x2122`
     w GET. **Wzorzec bezpieczny:** trzymaj frazy w **osobnym pliku JSON UTF-8** i czytaj je
     **`[IO.File]::ReadAllText($path,[Text.Encoding]::UTF8) | ConvertFrom-Json`** (jawny UTF-8), a weryfikuj
     GET-em, który dekoduje **surowe bajty odpowiedzi jako UTF-8** (`MemoryStream`→`UTF8.GetString`) — nie polegaj
     na `Invoke-RestMethod`/literałach. Skrypty wzorcowe: `booster-write-batch-2026-07-20.ps1` (+ `booster-targets-2026-07-20.json`).
     Po naprawie wszystkie 6 = dokładne dopasowanie, bez wiodącej spacji, bez mojibake (long-len zgodne z targetem).
- **Ostatnio zweryfikowano (poprz.):** 2026-07-19 (**RECON WYSZUKIWARKA WEWNĘTRZNA — synonimy / frazy alternatywne / tagi
  pod projekt „alt-frazy na każdy produkt"; READ-ONLY, ZERO zapisów**). Dok. oficjalna: strony `developers.shoper.pl`
  za loginem/SPA, ale **artykuły shoper.pl/learn potwierdziły mechanizmy** (WebFetch/WebSearch). **Trzy mechanizmy
  wyszukiwarki Premium i ich dostępność przez webapi:**
  1. **Frazy alternatywne** (Premium) = **jedyny mechanizm PER PRODUKT** pasujący do celu. Panel: *Ustawienia >
     Zarządzanie produktami > Ustawienia wyszukiwarki* (włączenie), wpis na *karcie produktu → zakładka „Dane
     podstawowe" → sekcja „Hasła w wyszukiwarce sklepu"*, frazy **oddzielone przecinkami**, **niewidoczne dla klienta**
     (cytat learn: „wyrażenia, po których klienci mogą dodatkowo wyszukać dany produkt").
     🔴 **KOREKTA 2026-07-20 (ten recon był BŁĘDNY w tym punkcie): „Hasła w wyszukiwarce sklepu" = pole
     `translations.pl_PL.booster` — JEST wystawione i ZAPISYWALNE przez webapi.** Poprzednie zdanie „NIE jest
     wystawiona w webapi / obiekt products/{id} NIE ma żadnego pola fraz" było przeoczeniem — recon nie sprawdził
     pola `booster` (jest w `translations.pl_PL` obok `seo_*`, patrz sekcja produktów). Potwierdzenie: user wpisał
     w panelu frazy testowe na prod. 1720 „Skrzynia Milwaukee Packout 3", eksport CSV nazwał kolumnę **`booster`**,
     a oficjalny artykuł Shoper Learn „Pola CSV produktów" opisuje kolumnę **`booster` = „Frazy alternatywne""**.
     GET/PUT webapi potwierdzone na żywo (niżej, wpis 2026-07-20). ⇒ **Bulk fraz alternatywnych = webapi PUT
     `products/{id}` z `translations.pl_PL.booster` (NIE tylko CSV)** — to odblokowuje zapełnienie ~7 900 produktów
     przez kanał DANE. `tags`/`seo_keywords` dalej ≠ wyszukiwarka. **CSV import** pozostaje alternatywą (kolumna `booster`).
  2. **Synonimy** (Premium) = **GLOBALNY słownik** grup słów (dwustronne + jednostronne „węższe znaczenia"),
     nielimitowany, „od razu pojawią się na sklepie". Panel: *Konfiguracja > Wyszukiwarka*. **NIE per produkt**,
     **NIE w webapi** (sonda: `synonyms`/`search-synonyms`/`product-search-synonyms`/`dictionary`/`search-dictionary`
     → wszystkie **HTTP 400 „Missing MODULE"**).
  3. **Tagi produktów** = zasób **`product-tags` ISTNIEJE w webapi (HTTP 200, `count=0`)** + pole **`products.tags`**
     = tablica `tag_id` (analog `news.tags`↔`news-tags`, więc **prawdopodobnie zapisywalne** POST `product-tags`
     {name,lang_id} → `tag_id`, potem PUT `products/{id}` {tags:[...]}; **NIE testowane zapisem**). **ALE** artykuł
     „Tagi produktów" ramuje je jako **organizację w panelu** (Ustawienia > Produkty > Tagi produktów; przypisanie
     zbiorcze „Przypisz tagi"), **NIE wymienia wpływu na wyszukiwarkę klienta**; tagi **NIE są** na liście enhancerów
     wyszukiwarki Premium; natywna konfiguracja szuka tylko w `product_search_code/short_description/description`
     (brak flagi `product_search_tags`). **Werdykt: tagi = łatwe przez webapi, ale najpewniej NIE zasilają frontowej
     wyszukiwarki → zły lewar (do potwierdzenia w panelu).**
  **Sonda zasobów (18 nazw):** istnieje **tylko `product-tags`**; `tags`,`producttags`,`search-phrases`,
  `alternative-phrases`,`phrases`,`product-phrases`,`synonyms`,`search-synonyms`,`product-search-synonyms`,
  `dictionary`,`search-dictionary`,`search-exclusions`,`search-config`,`search-settings`,`search-suggestions`,
  `search-terms` → **HTTP 400 „Missing MODULE"**. **Pole `tags` = pusta tablica na 300/300 produktów** (0 tagów
  w katalogu). **`attribute-groups`/`attributes` = count 0** (bez zmian od 2026-06-15). `products/2000/tags` jako
  subresource → count=7814 = **artefakt „ignorowany filtr" (cały katalog)**, nie realny endpoint. **Wyszukiwarka
  front:** URL kanoniczny **`https://sklep.plasmet.pl/pl/s?search=<fraza>`** (form action `/pl/s`, input `name="search"`,
  potwierdzone JSON-LD `SearchAction`) — **wyniki renderowane JS-em**; surowy GET zwraca sam szablon SSR bez kafli
  produktów (nie da się zmierzyć wyników bez przeglądarki/wewn. API JS). **Dane katalogu (webapi, dowód luki):**
  „Packout" w nazwie = **137 prod.**, ale „walizka" w nazwie = **13**, „skrzyni" = 20, „organizer" = 7; „walizka" w
  `description` = 466, w `short_description` = 0; „systainer"/„kufer"/„pakout" = 0. ⚠️ `product_search_all_tokens=0`
  (tryb OR) → wielowyrazowe frazy potoczne rozmywają wyniki. **Rekomendacja: Frazy alternatywne (per produkt) przez
  IMPORT CSV** jako główny lewar (webapi tego pola nie wystawia) + garść **Synonimów** globalnych na
  potoczne↔markowe („walizka"↔„Packout"). Skrypt: `scripts/shoper-api/search-alt-phrases-recon.ps1`; zrzuty
  `_rozeznanie/search-alt-phrases-recon.json`, `search-product-2000-full.json`. **Bez zmian łamiących pola/parametry
  istniejących zasobów — dopisano stan wiedzy o wyszukiwarce.**
- **Ostatnio zweryfikowano (poprz.):** 2026-07-17 (**RECON BUDMET/SCHARF — gwoździe/wkręty pod dopisek marki; READ-ONLY,
  ZERO zapisów**). Dok. oficjalna bez zmian (WebFetch developers.shoper.pl = SPA/login; WebSearch potwierdził
  istnienie zasobów `producers`, `categories-tree`, `products`). **Zasoby `producers`/`categories`/`categories-tree`/`products`
  zachowują się jak udokumentowano — dokumentacja aktualna.** Potwierdzone ponownie na żywo: (1) nazwa producenta =
  **top-level `name`** (`translations.pl_PL` puste); (2) filtr `producer_id` **IGNOROWANY** server-side → pełny skan
  katalogu + filtr klienta; (3) relacja produkt↔kategoria = `category_id` + tablica `categories[]` NA produkcie;
  (4) `categories-tree` zwraca `[{id,children}]`; nazwa kategorii = `translations.pl_PL.name`. **Stan liczb (2026-07-17):**
  `products count=7811` (157 stron), `producers count=51`, `categories count=285`. **BUDMET:** dwa wpisy producenta —
  **id 63 „BUDMET GROUP" = 35 produktów** (marka handlowa SCHARF), **id 23 „BUD-MET GROUP SP. Z O.O." = 0 (sierota Leo)**.
  Wszystkie 35 = gwoździe/wkręty w poddrzewie kat. **39 „Technika zamocowań"** (320 Gwoździe pierścieniowe ×7, 266 Wkręty
  ciesielskie konstrukcyjne ×23, 275 Wkręty ciesielskie regulacyjne ×5). ⚠️ **Pułapka kodowania skryptu:** literały regex
  z polskimi znakami (`ę`/`ź`) w `.ps1` bez BOM ładowane przez Windows PowerShell 5.1 są **mojibake** → dopasowanie po
  nazwie z `wkręt`/`gwóźdź` zawodzi cicho (dane z API są OK, UTF-8). Klasyfikuj po `code`/`cat_name` albo czytaj JSON
  przez `Get-Content -Encoding UTF8 | ConvertFrom-Json`. Skrypt: `scripts/shoper-api/scharf-budmet-recon.ps1`; zrzuty
  `_rozeznanie/scharf-budmet-*.json`. **Bez zmian łamiących pola/parametry.**
- **Ostatnio zweryfikowano:** 2026-07-16 (**LINKFIX — naprawa martwych linków we wpisach bloga; za zgodą
  usera 40× PUT `news/{id}` z samym `{content}`**). Dok. oficjalna bez zmian (WebFetch developers.shoper.pl =
  SPA/login; WebSearch: wzmianka o „API 2026.1" dotyczy zamówień/produktów/limitów — nic o `news`). Wykonanie:
  backup pełnych rekordów `_backup-news-linkfix-2026-07-16.json` → 260 podmian w 40 wpisach (188× `/pl/news/`→
  root-slug, 23× staging host, 40× martwe logo, 3× martwe hero, 6× absolutyzacja `/pl/c/`) → weryfikacja GET
  po każdym PUT (0 złych wzorców + zgodność długości) → finalny skan 40/40 czysty; kategorie bloga przetrwały
  (suma filtrów `category_id` 5-9 = 40/40), hero nietknięte. Skrypty: `linkfix-news-recon.ps1`,
  `linkfix-news-apply.ps1`. Równolegle naprawiono pliki kolejki `blog/queue/45-51` (49 podmian, tylko pola
  `tresc_html`/`zajawka_html`/`schema_jsonld`). **NOWE fakty techniczne (produkcja):**
  (1) **hero wpisu na froncie = `https://sklep.plasmet.pl/userdata/public/news/images/<news_id>.jpg`**
  (stabilny URL, HTTP 200) — to jest żywy odpowiednik do JSON-LD `image`; NIE da się go zbudować „w przód"
  przed publikacją (wymaga `news_id`). (2) **`/userdata/gfx/logo.png` NIE istnieje na produkcji (404)** —
  logo do JSON-LD brać z globalnej schemy Organization motywu:
  `/environment/cache/images/storefrontImages_8ce682f7-8707-41f2-9a78-bd2c5c554c0f_236_0.png` (200; URL cache
  storefrontu — może się kiedyś przegenerować, ale jest tożsamy z tym, co publikuje sam sklep). (3) **PUT
  `news/{id}` z samym `{content}` nie rusza kategorii ani hero** (potwierdzone 40×). (4) Pułapka pomiarowa:
  `Invoke-WebRequest` **bez `-UseBasicParsing`** w PS 5.1 wisi na silniku IE (NonInteractive) — testy frontu
  ZAWSZE z `-UseBasicParsing` + UA przeglądarki. (5) GET na nieistniejący statyk **`.jpg` też zrywa
  połączenie** (jak `.xml`) — czysty kod daje dopiero **HEAD** (404).
- **Ostatnio zweryfikowano:** 2026-07-16 (**RESOLVER LINKÓW WEWNĘTRZNYCH partii C bloga — READ-ONLY do API,
  zapisy tylko do plików lokalnych `blog/queue/`**). Dok. API bez zmian (WebFetch developers.shoper.pl = SPA/samo
  menu — znana pułapka). **NOWE potwierdzone na żywo (produkcja):** (1) **permalink wpisu bloga z ustawionym
  `seo_url` = `https://sklep.plasmet.pl/<seo_url>` (slug w ROOCIE domeny)** — potwierdzone canonicalem strony
  wpisu i HTTP 200 na 24 wpisach; **format `/pl/news/<seo_url>` NIE działa na produkcji (404 / zerwane
  połączenie)** — szczegóły w sekcji „URL wpisu bloga". (2) Krótki URL `/pl/n/<news_id>` działa (200), canonical
  wskazuje root-slug. (3) Front produkcyjny **blokuje curl** (zrywa połączenie) — testy frontu robić
  `Invoke-WebRequest` z UA przeglądarki. (4) Filtr `products?filters={"category_id":X}` → **404** (pole
  niefiltrowalne), a `?category_id=X` jest **ignorowany** (zwraca cały katalog) — liczności produktów w kategorii
  NIE da się czytać przez webapi; obecność produktów sprawdzać na froncie (kafelki `product-tile__name`).
  (5) W treściach opublikowanych wpisów siedzą martwe linki: stary host staging (news 49), format
  `/pl/news/<seo_url>`=404 (news 46), relatywne (news 33) — ogon do posprzątania osobnym zadaniem.
- **Ostatnio zweryfikowano:** 2026-07-16 (**RE-KATEGORYZACJA BLOGA — za zgodą usera; 4 POST `news-categories`
  + 13 PUT `news`**). Skrypt: `recategorize-news-2026-07-16.ps1` (+ mapa `.map.json`, backup
  `_backup-news-recategorize-2026-07-16.json`). **Dok. API bez zmian** (`WebFetch` developers.shoper.pl = SPA/samo
  menu — znana pułapka; `WebSearch` potwierdził istnienie stron `news-categories/list|update`, brak sygnałów zmian).
  **NOWE potwierdzone na żywo (produkcja):** (1) **PUT `news/{id}` z `{categories:[id]}` ZASTĘPUJE przypisanie
  kategorii** (wpis znika ze starej kategorii, pojawia się w nowej — zweryfikowane filtrem `category_id` przed/po,
  13/13 OK); wzorzec `categories` l. mnoga z POST działa identycznie w PUT. (2) **POST `news-categories`
  zwraca w body nowe `category_id`** (raw np. `6`), payload `{name, lang_id:1, active:1}` wystarcza.
  (3) Kategorie bloga na produkcji: `Poradnik`=5 (było 40 wpisów), **nowe: `Krok po kroku`=6,
  `Problemy i porady`=7, `Porównania`=8, `Normy i BHP`=9** (utworzone 2026-07-16). (4) `news-categories`
  paginuje poprawnie przy `limit=50` (5 rekordów = 1 strona).
- **Ostatnio zweryfikowano:** 2026-07-14 (**INWENTARYZACJA NEWSLETTER + PUSTE PODSTRONY — READ-ONLY,
  zero zapisów do sklepu**). Zakres: sonda 12 nazw zasobu newslettera, `users` (440), `categories` (285)
  + `categories-tree`, `producers` (51), `aboutpages` (11), pełny skan `products` (157 stron, 7 810 poz.).
  **Co NOWE:** (1) zasób **`subscribers` ISTNIEJE** (GET 200) — ale **count=0**, więc schematu pól (double
  opt-in?) nie da się odczytać; pozostałe 11 nazw = „Missing MODULE". (2) **`users.newsletter="1"` → 0/440
  kont** = zerowa legalna baza mailingowa. (3) **KOREKTA:** `stock` **nie ma** pola `producer_id` —
  producent to **top-level `products.producer_id`** (stara notatka myląca). (4) `producers.translations.pl_PL`
  **nie ma pola `name`** (nazwa = top-level `name`); Milwaukee `producer_id` = **52** (kolejna migracja ID
  po sync Leo). (5) **`categories…items` to NIE licznik produktów** (zawsze 0). Weryfikacja wobec dok.
  oficjalnej: `WebFetch` na developers.shoper.pl + `WebSearch` → SPA za loginem, brak publicznej referencji
  `subscribers` → nazwę zasobu potwierdzono **sondą GET na żywo**. Deliverable:
  `docs/inwentaryzacja-newsletter-i-puste-strony.md`.
- **Ostatnio zweryfikowano:** 2026-07-14 (**AUDYT POCUTOVEROWY — READ-ONLY, zero zapisów do sklepu**).
  Skrypty: `audyt-pocutover-A.ps1` (payments/shippings/orders/producers/categories/news),
  `audyt-pocutover-B.ps1` (agregat zamówień bez PII + pełny zrzut 12 888 reguł 301),
  `audyt-pocutover-C.ps1` (skan 7 810 produktów: długość opisu × producent),
  `audyt-pocutover-D.ps1` (atrybucja zamówień do kont, bez PII).
  **Co ZMIENIONE w tej dok. (błąd wykryty na żywo):** sekcja `payments` — było „10 metod, P24 = `payment_id=7`",
  jest **19 metod, P24 = `payment_id=18` (`shoperP24`)**; flaga aktywności to `translations.pl_PL.active`,
  nie top-level. **Co DOPISANE:** pełna tabela `shippings` z wiązaniem dostawa→płatności (`shippings[].payments`)
  — to ono decyduje, co klient widzi w kasie. Reszta dok. (redirects, news, aboutpages, application-config)
  **potwierdzona bez zmian**. Weryfikacja wobec dok. oficjalnej: `WebFetch` na developers.shoper.pl = SPA (samo menu,
  znana pułapka) → `WebSearch` potwierdził, że **stara integracja Przelewy24 jest wygaszona od 2024-04-15**
  (zastąpiona „Shoper Płatności × Przelewy24" = silnik `shoperP24`), co pokrywa się ze stanem na żywo.
  Istnieje endpoint `payments/{payment_id}/channels/{id}` (kanały P24) — na naszym koncie **403**.
- **Ostatnio zweryfikowano (poprz.):** 2026-07-14 (**PEŁNY ROLLOUT GWIAZDKI NA ŻYWEJ MAPIE 301 — za zgodą usera; 4 675 POST + 7 728 PUT**).
  **Dok. API bez zmian** (`WebSearch`: „Masowy import przekierowań 301 przez API" + „Przekierowania 301" — pola
  `route`/`type`/`object_id`/`lang_id`/`target` bez zmian). **NOWE z dok. oficjalnej:** poza `*` route przyjmuje
  placeholdery **`{page}` / `{sort}` / `{view}`** (paginacja/sortowanie/widok) → narzędzie pod **bucket 4 z GSC**
  (listingi z parametrami), jeszcze nie wykorzystane. Oficjalny przykład użycia `*` (usunięta kategoria → wildcard
  łapie **wszystko po nazwie kategorii**) **potwierdza twardą granicę**: `*` tylko na `type=1`.
  **Wynik rolloutu (mapa 8 213 → 12 888 reguł, 0 błędów HTTP):**
  1. **Backfill 4 675 POST** (domknięcie GSC: alt-ścieżka + forma pojedyncza + SDS) — 3 684 `type=1` (z `*`)
     + 991 `type=2` (bez `*`). ERR=0.
  2. **Przepisanie 7 728 PUT** (`redirects-wildcard-rewrite.ps1`) — **100 % reguł `type=1` ma teraz `*`**
     (11 414/11 414), `type=2` (1 460) i `type=4` (14) **nietknięte, 0 gwiazdek**. ERR=0.
  3. ✅ **Kodowanie WIELOBAJTOWE w `route` DZIAŁA** (otwarte pytanie z poprz. sesji — ZAMKNIĘTE): SDS z `%C4%98` (Ę)
     → produkt 135 i `%C5%83` (Ń) → produkt 5504, **301 → 200 w OBU wariantach** (goły i `?srsltid`). Round-trip przez
     bazę nie psuje polskich znaków → **fallback „route zdekodowany" NIEPOTRZEBNY**.
  4. ✅ **BRAK OVER-MATCHU potwierdzony na żywo:** produkty leżące pod kategorią z regułą `type=2` (np.
     `/produkty/technika-zamocowan/...`) trafiają na **PRODUKT** (93, 94), nie na kategorię 39.
  5. ⚠️ **Rate limit:** przy throttle 200-300 ms Shoper sypie **429** (łapane backoffem, 0 strat); przy **250-400 ms
     — ZERO 429**. → dla operacji masowych na `redirects` używaj **250-400 ms**.
  6. ⚠️ **Pułapka narzędziowa (nie API):** `Add-Content` do logu wznowienia **wywala się** („Nie można odczytać
     strumienia"), gdy równolegle ktoś czyta ten plik `Get-Content`-em (monitor postępu) → `ErrorActionPreference=Stop`
     ubija import w połowie. **Nie czytaj pliku logu w trakcie biegu** — monitoruj proces (`Get-WmiObject Win32_Process`)
     albo log przekierowany `*>` (persistent handle). Import wznowił się z logu bez duplikatów (idempotencja po API).
  **Znana, świadoma luka:** 1 460 reguł `type=2` (kategorie) **nie łapie URL-i z query stringiem** (`?srsltid`/`?gclid`
  → 404). To cena bezpieczeństwa (patrz „TWARDA GRANICA"). **Ogon:** 1 para duplikatów (`7555` + `8213`, oba `type=1`
  → produkt 1909, oba z `*`) — pozostałość po eksperymencie, nieszkodliwa (ten sam cel), do skasowania (`DELETE 8213`).
  Skrypty: **`redirects-wildcard-rewrite.ps1`** (nowy: PUT `*` tylko na `type=1`, backup+rollback, wznawialny,
  asercje anty-over-match), **`redirects-dump-live.ps1`** (nowy: zrzut mapy + pre-flight kolizji planu),
  `redirects-301-apply.ps1` (backfill). Backupy: `_301/backup-rewrite-20260714-133840.json` (7 728 reguł)
  + `_301/backup-rewrite-20260714-143930.json` (1 549, wznowienie).
- **Ostatnio zweryfikowano (poprz.):** 2026-07-14 (**2 testy diagnostyczne 301 NA ŻYWO za zgodą usera — 1 PUT + 1 POST, odwracalne**).
  **Dok. API bez zmian** (`WebSearch`: `redirects` `list`/`get` + artykuły „Masowy import przekierowań 301 przez API"
  i „Przekierowania 301" — semantyka `*` opisana tylko od strony panelu; pola `route`/`type`/`object_id`/`lang_id` bez zmian).
  **Co NOWE (zachowanie API, wykryte empirycznie — 3 rzeczy):**
  1. ✅ **Reguła z `*` obsługuje TEŻ URL bez parametru** (test na regule 8212, PUT dopisujący `*`; brak regresji na
     wariancie gołym, `?srsltid`/`?gclid` naprawione, brak over-matchu). ⇒ mapę 301 się **PRZEPISUJE** (8 212 PUT-ów),
     **nie dokłada** drugiego kompletu. **`PUT /redirects/{id}` DZIAŁA** (wcześniej znaliśmy tylko POST).
  2. 🔴 **webapi ZAPISUJE `route` PO URL-DEKODOWANIU** (`%20` → spacja, `%5B` → `[`). Silnik i tak dopasowuje request
     z `%20` → **percent-encoding w planach jest bezpieczny, bucket SDS wgrywaj as-is** (test: reguła 8214,
     `/_data/attachments/07bsnb/SDS%20…pdf` → 301 → produkt 2776 → 200). **ALE** to **rozwala idempotencję po `route`**
     w imporcie masowym (plan encoded vs sklep decoded → duplikaty przy re-runie) → **fix wdrożony**
     w `redirects-301-apply.ps1` (klucz = `UnescapeDataString(route).ToLower()` po obu stronach).
  3. ⚠️ **Filtr `?filters={"route":{"~":"…"}}` na `redirects` nie działa** (cicho zwraca `count=0`) → paginuj całą listę.
  **Stan mapy po testach:** 8 213 reguł, 0 duplikatów, 3 z `*` (8212, 8213 — produkt 1909; 8214 = SDS bez `*`).
  ⏳ **Otwarte:** percent-encoding **wielobajtowy** (`%C5%BA`/`%C5%82` — 25 wierszy SDS, ~55 klików) — niesprawdzony;
  weryfikacja curlem PO rolloucie, fallback = route zdekodowany.
  Skrypty: `redirect-test1-8212-rewrite.ps1`, `redirect-test2-sds.ps1`, `redirects-scan-dupes.ps1`.
- **Ostatnio zweryfikowano (poprz.):** 2026-07-14 (**domknięcie mapy 301 o URL-e z GSC — buckety 1-3, READ-ONLY + DRY-RUN, ZERO zapisu**).
  **Dok. API bez zmian** (`WebFetch` developers.shoper.pl = SPA/login; `WebSearch` potwierdził istnienie `redirects/list`
  + `redirects/get` i artykuł „Masowy import przekierowań 301 przez API" — pola `route`/`type`/`object_id`/`lang_id` bez zmian).
  **Co NOWE (dane, nie API):** mapa 8 212 reguł pokrywa tylko URL-e z feedu eksportera — GSC pokazuje **5 693 dalszych
  zaindeksowanych URL-i** w 3 wzorcach: (1) **alt-ścieżka** `/produkty/<INNA-gałąź>/<slug>.html` (2 237 URL / 894 kliki) —
  Mercatum serwował ten sam produkt pod wieloma gałęziami, feed dawał tylko jedną; (2) **forma pojedyncza**
  `/produkt/<slug>` (3 313 / 588) — **100 % zaindeksowanych Z `?m=<id>`** → bez gwiazdki w `route` nie odzyska ANI JEDNEGO
  klika (patrz sekcja o `*`); (3) **pliki SDS** `/_data/attachments/<code>/*.pdf` (143 / 536, najwyższy CTR) — folder
  attachmentu = **`code` produktu** (join 1:1, 99/143 dokładne trafienie w żywy katalog).
  **Oś joinu potwierdzona:** SKU w slugu jest **PODWOJONE** (`/07bkc-07bkc-db-kotwa…`) → da się je wyłuskać nawet dla
  produktów **skasowanych przez Leo** (nie ma ich w katalogu) i po nich odzyskać kategorię z formy mnogiej.
  ⚠️ **Kody live mają SPACJE** (`06MO4932 3525 79`), w URL są myślniki → normalizuj `[\s\-_.]` (bez tego join = 0 trafień).
  **Wynik DRY-RUN: 4 676 reguł** (3 685 `type=1` produkt / 991 `type=2` kategoria), **0 kolizji** z 8 212 żywymi regułami,
  0 duplikatów, 0 błędnych celów. 864 URL-e (111 klików) BEZ celu = martwy produkt w **martwej gałęzi Mercatum**
  (stare drzewo markowe: `czesci-zamienne-milwaukee` 97, `elementy-mocujace` 88, `narzedzia-reczne-richmann` 32…) —
  świadomie zostawione na 404 (mapowanie gałęzi = decyzja SEO usera). ⚠️ **Niezweryfikowane:** czy silnik dopasowuje
  `route` z **procent-kodowaniem** (`%20` w nazwach plików SDS) → przed masowym importem sprawdź 1 regułą.
  Skrypty: **`redirects-301-gsc-build.ps1`** (nowy, READ-ONLY, `-WildcardB2`), `redirects-301-apply.ps1` (dodany `-PlanPath`
  + log wznowienia per-plan). Plany: `_301/plan-301-gsc-extra.csv`, `_301/plan-301-gsc-extra-b2wildcard.csv`. **BEZ `-Apply`.**
- **Ostatnio zweryfikowano (poprz.):** 2026-07-14 (**`redirects` + query string — EKSPERYMENT NA ŻYWO za zgodą usera, 1 nowa reguła**).
  **Dok. API bez zmian**; `WebFetch` na shoper.pl/learn („Przekierowania 301") potwierdził obsługę `*` **od strony panelu**
  (*„przekierowanie podanego adresu URL i wszystkich jego odmian występujących po znaku `*`"*) + parametry `{page}/{sort}/{view}`;
  o zachowaniu przy query stringu dokumentacja **milczy**. **Co NOWE (odkryte empirycznie, nigdzie nieudokumentowane):**
  (1) 🔴 reguła `redirects` **bez gwiazdki NIE łapie URL-i z JAKIMKOLWIEK query stringiem** → twardy **404** na
  `?srsltid` (Google Shopping) i `?gclid` (Ads) — realna dziura w ruchu płatnym; (2) ✅ **webapi PRZYJMUJE `*` w polu
  `route`** (POST 200, gwiazdka zapisana 1:1, bez sanityzacji) i to **rozwiązuje problem** (301 → produkt → 200 dla
  wszystkich wariantów z parametrem, **bez regresji** na wariancie bez parametru); (3) semantyka `*` = prefiks na
  granicy ścieżki/query (`.htmlZZZ` → 404 → **brak over-matchu**); (4) reguła z `*` i bez `*` **współistnieją**.
  Nowa sekcja: „PUŁAPKA: reguła BEZ gwiazdki NIE łapie URL-i z query stringiem". Skrypt: `redirect-wildcard-test.ps1`.
  **Zapis: 1 reguła (`redirect_id=8213`, produkt 1909) — ZOSTAWIONA (działa, naprawia żywy URL). Decyzja o rollout: user.**
- **Ostatnio zweryfikowano (poprz.):** 2026-07-14 (**zasób `orders` — rozeznanie READ-ONLY pod diagnozę testowego zamówienia P24/GA4**).
  **Dok. API bez zmian** (oficjalny developers.shoper.pl = SPA, `WebFetch` zwraca menu; `WebSearch` potwierdził
  endpoint `orders/get` + pola `order_id/sum/date/payment_id`). **Co NOWE (udokumentowane po raz pierwszy):**
  realny kształt obiektu `orders` z listy (55 pól, w tym `date`/`status_date`/`confirm_date`, `is_paid`/`paid`,
  `payment_url`, `notes_pub`, `delivery_address`/`billing_address`), mapy `statuses` (10) i `payments` (10:
  `1 cash`…`7 przelewy24.pl`), oraz że **list endpoint zwraca pełny obiekt** i **domyślnie rośnie po `order_id`**.
  Nowa sekcja „Zamówienia — zasób `orders`". Skrypt: `orders-recon-readonly.ps1`. **Bez zapisu.**
- **Ostatnio zweryfikowano (poprz.):** 2026-07-14 (**robots.txt / sitemap / ogon cutoveru domeny** — READ-ONLY, bez zapisu).
  **Dok. API bez zmian** (`WebFetch` shoper.pl/learn + `WebSearch`: robots.txt = panel `Ustawienia > Zaawansowane > SEO`,
  sitemap = zakładka „Google Sitemap"; Shoper oficjalnie „nie zaleca modyfikacji robots.txt"). **Co NOWE:**
  (1) **Nie ma zasobu webapi dla robots/sitemap/domeny** — 22 nazwy przesondowane, wszystkie „Missing MODULE";
  jedyne konfiguracyjne to `application-config` (READ-ONLY) i `application-version` (`5.26.36`).
  (2) **robots.txt = plik statyczny, jeden dla obu hostów, z twardo zapisanym hostem w `Sitemap:`**; po cutoverze
  platforma regeneruje go z opóźnieniem (host sam wskoczył na produkcyjny; `shop_url` był poprawny cały czas).
  (3) **`/sitemap.xml` = 404** (sitemapa tylko pod `/console/integration/execute/name/GoogleSitemap`); GET na
  nieistniejący `.xml` **zrywa połączenie** (fałszywy „timeout") — mierz **HEAD-em**.
  (4) **Ogon cutoveru = TYLKO blog:** `news` 38/38 wpisów, **468 wystąpień** hosta technicznego w `content`
  (linki + JSON-LD); `products` (7 810), `categories` (285), `aboutpages` (11), `producers` (51), `redirects`
  `type=0` (0 reguł) i feed Merchant — **czyste**. Skrypt naprawczy (czeka na zgodę): `fix-news-host-shoparena.ps1`.
- **Ostatnio zweryfikowano (poprz.):** 2026-07-13 (`product-files` — DOPASOWANIE 4 KART CHARAKTERYSTYKI MSDS POLIFARB KALISZ + DRY-RUN, READ-ONLY, BEZ zapisu). **Dok. API bez zmian — sekcja `product-files` aktualna** (`WebSearch` potwierdził istnienie endpointu `product-files/insert` na developers.shoper.pl; `WebFetch` = SPA za loginem, samo menu). **Zbiory (pełny skan `products` `limit=50`, `count`=7806, 157 stron; filtr klienta po `translations.pl_PL.name`; `translation_id` czytany wprost z listy — GET per produkt zbędny):** wszystkie 4 linie = **`producer_id=61` „POLIFARB KALISZ"** (nazwa marki w polu **top-level `name`** producenta, `translations.pl_PL.name` PUSTE — czytaj `name`, nie translation). Wyniki: **Akrylbond 13** (kod `07BDA065/*`, „Akrylbond emalia akrylowa 0,65L <kolor>"), **Ferrobond Ultra 1** (pid 7093, kod `07BDUD025PM6005`, „Farba do metalu 3w1 na rdzę Ferrobond Ultra…"), **Ferrobond bazowy 33** (kod `07BDF*`, „FERROBOND <poj.> <kolor> RAL…"), **Unichron 6** (kod `07BDGF*`, „UNICHRON GRUNT FTALOWY…"). **Rozróżnienie Ferrobond/Ultra CZYSTE:** tylko 1 SKU ma „Ultra" w nazwie (inny format nazwy i kod `07BDUD` vs `07BDF`) → 0 ryzyka pomyłki. **DRY-RUN** (`productfiles-bulk-apply.ps1`, listy z tablicą root, `name`/`file_name`=`Karta-charakterystyki-<linia>.pdf` z rozszerzeniem, opis PL w `description`): POST-ów do wykonania 13/1/33/6 (razem **53**), **0 pominiętych idempotentnie** (żaden z tych produktów nie ma jeszcze tej karty; istniejące 402 rekordy `product-files` to poprzednie migracje). **NIE wykonano `-Apply`** — czeka na decyzję usera. Skrypt recon: `msds-polifarb-recon.ps1` (cache skanu `_rozeznanie/msds-katalog-skan.json`); listy: `_rozeznanie/{akrylbond,ferrobond-ultra,ferrobond,unichron}-kandydaci.json`. ⚠️ **Pułapka PS 5.1:** `ConvertFrom-Json` na tablicy-JSON zwraca ją jako 1 obiekt → wczytując cache użyj `if ($x -isnot [Array]) { $x=@($x) }`, inaczej filtr `Where-Object { $_.name -match … }` dopasuje CAŁY katalog (pojedynczy element = cała tablica, member-enum `.name`). Also: nie nazywaj parametru funkcji `$pid` (automatyczna read-only = PID procesu).
- **Ostatnio zweryfikowano (poprz.):** 2026-07-07 (WYKONALNOŚĆ MASOWEJ PODMIANY NAZW+OPISÓW — test 1-produktowy na żywo, prod. 156, za zgodą zadania; + WebSearch oficjalnej pomocy).
  **Co NOWE/KRYTYCZNE:**
  - **Zmiana `name` ZMIENIA permalink (slug), ale `product_id` w URL zostaje** — resolver po ID; oficjalna pomoc Shoper: zmiana nazwy auto-zakłada 301 stary→nowy slug. Nasze `redirects` (`type=1/2` + `object_id`) są odporne na zmianę sluga. Przed cutoverem (sitemap 404, 0 org.) koszt SEO podmiany nazw ~zerowy.
  - **Partial-PUT `translations.pl_PL.{name,description}` = 0 różnic w pozostałych polach** (cena/stan/kategorie/zdjęcie/atrybuty/flagi/promo/unit_calc/tax/delivery/ean/code/short_description/seo_* nietknięte). Bezpieczny zapis wyłącznie name+description.
  - **`description` sanityzuje `<!-- komentarz HTML -->` (WYCINA)**; `<span style="display:none">` przeżywa (Shoper dopisuje `;`). Marker trwałości pod sync Leo = span, NIE komentarz. UTF-8 czyste, mojibake 0%.
  - **`short_description` = blok GPSR (Producent + Informacje o bezpieczeństwie), 5/5 marek** — NIE ruszać przy podmianie opisów.
  - **Statystyka `description` (n=300):** puste 4,0% / <300 zn. 17,7% / ≥300 zn. 78,3% / mediana 552 zn. `products count=8013`.
  - **Marker trwałości ustawiony** na prod. 156 (`<span style="display:none">leo-marker-20260707</span>`) → po nocnym syncu Leo sprawdzić obecność (patrz sekcja „Masowa podmiana NAZW i OPISÓW" + `backup/test-nazwy-opisy/marker.md`).
  - Skrypty: `nazwy-opisy-recon.ps1`, `nazwy-opisy-permalink-test.ps1`, `nazwy-opisy-marker-set.ps1`.
  - **✅ PUBLIKACJA PILOTA 10 PRODUKTÓW (name+description) — WYKONANA NA ŻYWO 2026-07-07** (za zgodą zadania). ID: 2904, 2002,
    101, 2912, 5216, 1327, 5991, 7353, 4616, 7093. Partial-PUT `translations.pl_PL.{name,description}` → **10/10 HTTP 200**,
    `name` zapisany 1:1 (znaki `× ³ ² Ø` OK), **mojibake 0%**, **0 ubytków tagów strukturalnych** (p/h2/h3/ul/li/table/tr/td/th).
    **⚠️ Sanityzacja `description` DEKODUJE ENCJE HTML → Unicode:** `&times;`→`×`, `&deg;`→`°` (potwierdzone na prod. 7353/4616:
    po `HtmlDecode`+strip-whitespace wysłane==zapisane) — renderuje się identycznie, ale jeśli chcesz encje 1:1 w bazie, licz się
    z ich normalizacją. Whitespace też normalizowany (prod. 7093: -5 zn., sama spacja). **Permalink regeneruje się z `name`**,
    znaki spoza ASCII wypadają ze sluga (`8×23`→`823`, `400 g/m²`→`400-gm`), przecinki→`%2C`; `product_id` stabilny, 301 auto.
    Skrypt: `pilot-publikacja.ps1` (`-DryRun` domyślnie; parser MD → payload → GET-compare-backup → PUT → GET-verify → log+payloady).
    Payloady „co wgraliśmy": `backup/pilot-2026-07/payloads/prod-<id>.json`. Log: `tresc/produkty/pilot-2026-07/publikacja-log.md`.
  - **✅ INWENTARZ CHEMII BOSTIK+DEN BRAVEN (partia „chemia" fabryki opisów) — READ-ONLY 2026-07-07.** Skrypt `chemia-inwentarz-recon.ps1`,
    dane w `tresc/produkty/chemia-2026-07/`. **225 produktów** (Bostik + Den Braven + linie TIGER/Mamut; Tectane nieobecny). **Ustalenia:**
    - **List endpoint `GET /products?limit=50` zwraca PEŁNY obiekt produktu** (kompletny `translations.pl_PL.description`, `short_description`,
      `stock.*`, `category_id`, `producer_id`, `code`, `ean`, `active`) — do inwentaryzacji NIE trzeba GET-ów per produkt, wystarczy skan listy.
    - **⚠️ KONSOLIDACJA producentów Bostik przez Leo:** wszystkie trafienia są teraz pod **`producer_id=66` „BOSTIK" (224)** + `30` „Bostik" (1);
      **`51` „BOSTIK NIEAKTUALNE" = 0 produktów** (w czerwcu miał 176 — Leo przeniósł). Producenci 43/51 z nazwą „BOSTIK" = osierocone. `products count=8013`.
    - **⚠️ ENCODING — `Invoke-RestMethod` w PS 5.1 dekoduje UTF-8 POPRAWNIE**; znaki `�` widoczne przy `python print()` na konsoli Windows (cp1250) to
      TYLKO artefakt renderowania konsoli, NIE uszkodzenie danych (zweryfikowane bajtowo: `BIA\xc5\x81Y`=„BIAŁY", 0 rekordów z U+FFFD w zbiorze 225).
    - **BRANDING Den Braven→Bostik = trzy warstwy, trzy stany:** producent 100% Bostik (done) · podmiot GPSR w `short_description` „BOSTIK Sp. z o.o.,
      ul. Poznańska 11b, Sady, Tarnowo Podgórne" dla 224/225, „Den Braven"=0 (done prawnie) · **NAZWA** wciąż `DB ` prefiks (183), „Bostik" jawnie 30,
      „Den Braven" literalnie 0 · **OPIS body** wciąż „Den Braven" w 93/225 (41%), „Bostik" 38. ⇒ marka w tytule = „Bostik" dla całości bez researchu
      per produkt; rewrite nazwy/opisu = wykonanie rebrandu w warstwie widocznej (usuń `DB `, zachowaj nazwy linii Mamut/X-Polymer/Super Color/FixPro/Tiger).
    - **Rozkład opisu (n=225 po zdjęciu HTML):** pusty 7 / <300 zn. 2 / ≥300 zn. 216 (96%) — tylko 9 do napisania od zera, reszta do redakcji. ean 224/225, code 225/225.

- **Ostatnio zweryfikowano (poprz.):** 2026-07-03 (DIAGNOZA OMNIBUS — dlaczego brak plakietki „najniższa cena z 30 dni" na produkcie 1949 — READ-ONLY, tylko GET + HTML frontu).
  **Co NOWE/KRYTYCZNE:**
  - **Plakietka Omnibus pojawia się TYLKO przy AKTYWNEJ PROMOCJI (`specialoffers`), NIE przy zmianie ceny bazowej.**
    Sama zmiana `stock.price` (np. nocny sync Leo/Subiekt) NIE jest „obniżką/promocją" w modelu Shopera → brak plakietki.
    Motyw bramkuje CAŁY blok `product-price__lowest-historical-price` atrybutem `hidden` na `js__special-offer-container`
    (odsłaniany JS-em dopiero gdy istnieje special offer). Zgodne z dyrektywą Omnibus (obowiązek info tylko przy komunikowaniu obniżki).
  - **Zasób `specialoffers` (bez myślnika!) ISTNIEJE w REST API** — `GET /webapi/rest/specialoffers` → HTTP 200. Na koncie PLASMET
    **`count=0`** (ZERO promocji w całym sklepie → żaden produkt nie ma special offer). ⚠️ Wariant z myślnikiem `special-offers` → **HTTP 400**.
    Sub-ścieżki `products/{id}/omnibus`, `products/{id}/special-offers`, `products/{id}/specialoffers` **IGNOROWANE** (zwracają cały katalog `count=8009`) — brak sub-zasobu per-produkt.
  - **NOWE pola `stock` (Omnibus/ceny):** `historical_lowest_price`, `special_historical_lowest_price`, `wholesale_historical_lowest_price`,
    `price_special`, `price_type`, `price_type_special`, `price_type_wholesale`, `price_wholesale`, `price_buying`, `price_buying_net`,
    `comp_price`, `comp_price_special`, `comp_promo_price`, `comp_price_wholesale`, `comp_promo_price_special` itd. **`stock` NIE ma pola `promo_price`**
    (top-level `promo_price` istnieje, tu był `null`). **KOREKTA:** `historical_lowest_price` **potrafi RÓŻNIĆ się od ceny bieżącej** —
    prod. 1949: `price=34.00`, `historical_lowest_price=34.42` (Shoper realnie śledzi 30-dniowe minimum, wbrew wcześniejszej notatce „= cena bieżąca" z próbki 500).
  - **`application-config` NIE eksponuje flagi wyświetlania Omnibus** — jedyne pasujące pole to `shopping_promo_codes_enable=1` (kody rabatowe, NIE Omnibus).
    Włącznik „Pokaż najniższą cenę z 30 dni przed obniżką" = tylko PANEL (Ustawienia > Produkty > Ustawienia produktów). Że blok Omnibus RENDERUJE się w HTML (choć `hidden`) ⇒ opcja w panelu JEST włączona.
  - **Front pokazuje ceny NETTO gdy panel produktu w trybie netto:** 34,00 zł brutto → `27,64 zł` netto (`/1,23`, `tax_id=1`); hist. 34,42 → `27,98 zł` netto; „-1%" liczone poprawnie ale ukryte.
  - Skrypty: `scripts/shoper-api/diag-omnibus-1949.ps1` (produkt+sondy+config+front), `diag-omnibus-1949-front.ps1` (pełny blok ceny z HTML).

- **Ostatnio zweryfikowano (poprz.):** 2026-07-02 (AUDYT FEEDU pod GMC blanket `out_of_stock→backorder` — READ-ONLY, pełny skan 8008 prod.).
  **Co NOWE/KRYTYCZNE:**
  - **Blanket-override `out_of_stock→backorder` w Merchant Center = BEZPIECZNY.** 0 aktywnych produktów o statusie
    can_buy=0 (3/7/8/9); `stock.availability_id` (ręczne nadpisanie) = 0 w całym katalogu → statusy can_buy=0
    (wszystkie `ranges=0`) są nieosiągalne bez override'a. Cały feedowy `out_of_stock` (2758 poz.) = status 1
    „Dostępny na zamówienie" (can_buy=1). Szczegóły + niezmienniki: sekcja „AUDYT FEEDU pod Merchant Center".
  - **KOREKTA słownika: status id 4 („średnia ilość" DUBEL Leo, `from=10`) ma can_buy=1** (GET na żywo 2026-07-02;
    wcześniej dok. notowała 0). 744 aktywnych produktów siedzi na id 4 — zamawialne.
  - **Brak webapi zasobu feedu porównywarek/wykluczeń** — `feeds`/`feed`/`comparison-*`/`feeds-excludes`/`product-feeds`
    → wszystkie HTTP 400 (Missing MODULE). Mapowanie dostępności do feedu i wykluczenia = tylko PANEL.
  - Skrypt: `scripts/shoper-api/feed-oos-canbuy-audit-readonly.ps1`.

- **Ostatnio zweryfikowano (poprz.):** 2026-07-02 (DOMKNIĘCIE `stock.delivery_id` DO 100% NA AKTYWNYCH — PEŁNY SKAN + ZAPIS 64 prod. za zgodą).
  **Co NOWE/KRYTYCZNE:**
  - **Flaga aktywności produktu = `translations.pl_PL.active` (0/1). Produkt NIE ma top-level `active`** — GET
    `products/{id}` i lista `products` NIE zwracają `active` na poziomie top-level (potwierdzone: 38-40 kluczy bez
    `active`). ⇒ „produkt aktywny" filtruj **`{"translations.active":"1"}`** (na żywo `count=7815`), a w skanie czytaj
    `p.translations.pl_PL.active`. (Korekta wcześniejszej notatki sugerującej top-level `active`.)
  - **⚠️ ROZBIEŻNOŚĆ SKALI vs założenie „~20% pustego delivery_id": PEŁNY SKAN katalogu (8008 prod.) = tylko 64
    puste `delivery_id` (0,8%), NIE ~1600.** Rozkład populacji z `delivery_id` (7944 prod.) dokładnie odpowiada
    stanowi z 2026-06-18 → **masowy rollout czasu wysyłki BYŁ już wykonany**; 64 puste to **maruderzy dodani przez
    Leo PO rollouccie** (wszystkie ID w górnym zakresie **8109–8467**, wszystkie `active=1`, 0 na nieaktywnych).
    Wcześniejsze „~20%" (próbka 458 z GMC-recon) było przeszacowaniem/odnosiło się do stanu sprzed rolloutu.
  - **Rozkład `delivery_id` (populacja z ustawionym):** in-stock (stock>0, n=5033): **id 2 „48 godzin" = 4967 (98,7%)**,
    id 7 = 66; OOS (stock≤0, n=2911): **id 7 „14 dni" = 2830 (97,2%)**, id 2 = 81. ⇒ potwierdza politykę PLASMET:
    **in-stock → id 2 (48h), OOS → id 7 (14 dni)** (moda populacji). Słownik `deliveries` bez zmian (1..7:
    24h/48h/3/4/5/10/14 dni; brak „7 dni").
  - **Filtry pustego `delivery_id`:** `{"stock.delivery_id":null}` **DZIAŁA** (przed=64 / po=0), ale
    `{"stock.delivery_id":""}` (pusty string) → **count=0 = nieużyteczny** (nie łapie pustych). Do zliczania pustych
    używaj `null` **lub** pełnego skanu (autorytatywny; puste = `null`/`''`/`'0'`).
  - **ZAPIS (za zgodą, bulk):** partial-PUT `{"stock":{"delivery_id":"X"}}` na **64 aktywnych** produktach z pustym
    `delivery_id` (42× id 2 dla stock>0, 22× id 7 dla stock≤0) → **64/64 HTTP 200, 0 błędów**, każdy zweryfikowany
    GET-em `after==target`. Weryfikacja końcowa: filtr `null` = 0 (100% pokrycia na aktywnych). Backup + lista zmian +
    logi: `scripts/shoper-api/backup/delivery-id-20260702/` (`change-list.csv`, `inventory-all.csv`, `apply-log.csv`,
    `manifest-recon.json`, `deliveries-slownik.json`). Skrypty: `delivery-fill-recon.ps1` (READ-ONLY skan+backup),
    `delivery-fill-apply.ps1` (`-Execute`, throttling+retry 429/5xx+idempotencja), `delivery-fill-verify.ps1`,
    `delivery-probe-active.ps1`. **Ryzyko Leo:** kolejny sync Subiekt→Shoper MOŻE nadpisać/wyczyścić `delivery_id`
    (fix doraźny pod start feedu GMC); docelowo `delivery_id` powinien pochodzić z Subiekta/Leo. **Bez zmian
    łamiących pola/parametry; jedyny zapis = `delivery_id` (+ auto `edit_date`).**
  **Dok. oficjalna** = SPA za loginem (`WebFetch` → menu); `WebSearch` potwierdził `delivery_id` = czas realizacji
  wariantu (`product-stocks`). Mechanizm `stock.delivery_id`/`deliveries` zgodny z zapisem z 2026-06-18.
- **Ostatnio zweryfikowano (poprz.):** 2026-07-02 (GOTOWOŚĆ NATYWNEGO FEEDU GOOGLE MERCHANT CENTER — READ-ONLY, próbka 458+250 prod.; dowód przestrzeni ID).
  **Co NOWE/KRYTYCZNE:**
  - **`g:id` natywnego feedu Shopera = `product_id` (wewnętrzny numer ID), NIE `code`/SKU — POTWIERDZONE.** Dowód
    z żywego API: `products/2102` → `product_id=2102`, `permalink=.../pl/p/.../2102`, `code='06MM4932 4921 31'`,
    `ean='4058546414986'` (ID w URL == `product_id`, `code` to osobny symbol ze spacjami). Oficjalna dok. Shopera
    (help/integracja-z-google-merchant-center) wprost: **„g:id — the product's internal ID number in Shoper, not the
    SKU/symbol"**. ⇒ **feed `GoogleProductSearch` i `item_id` natywnego dataLayera GA4 dzielą TĘ SAMĄ przestrzeń
    (`product_id`)** → dynamic remarketing dopasuje się bez remapu. `g:mpn`←`code`, `g:gtin`←`ean` (do potwierdzenia
    w wygenerowanym pliku — API nie eksponuje kształtu feedu).
  - **Pokrycie atrybutów GMC (próbka 458, strony rozproszone 1..161):** EAN/GTIN **97,8%**, `code`/SKU **100%**,
    `producer_id` **99,6%**, `category_id` **100%**, `stock.price>0` **100%** (brutto), `main_image` **98,5%**,
    `active=1` **98%**, `stock.stock>0` **58,5%** (⇒ ~41% OOS), **`stock.weight` = 0% i `dimension_l` = 0%**
    (waga/wymiary NIEUZUPEŁNIONE w całym katalogu — luka dla `g:shipping_weight`), **`feeds_excludes` = 0%**
    (nikt nie wykluczony → cały aktywny katalog wejdzie do feedu).
  - **⛔ DRIFT vs sekcja OOS: `availabilities` id=4 („średnia ilość" DUBEL) ma teraz `can_buy=1`** (dok. z 2026-06-15
    notowała `0`). Żywy słownik 2026-07-02: can_buy=1 → id **1,2,4,5,6**; can_buy=0 → id **3,7,8,9**. Próbka join
    `calculated_availability_id`→`can_buy`: **250/250 = 100% efektywnie ZAMAWIALNE** (cały OOS jedzie na id 1
    „Dostępny na zamówienie", can_buy=1). ⇒ dla `g:availability`: nie ma już produktów in-stock zablokowanych
    dublem id4.
  - **`stock.delivery_id` (czas realizacji = TWARDY wymóg feedu): ~80% ustawione** (rozkład: id 2 „48 godzin"
    dla stock>0, id 7 „14 dni" dla OOS), **~20% PUSTE** → rollout czasu wysyłki NIEDOKOŃCZONY. Produkty bez
    efektywnego czasu realizacji Shoper oznacza w feedzie jako „niedostępne" (o ile nie łapią globalnego defaultu)
    → **domknąć delivery_id do 100% przed startem feedu.** Słowniki: `taxes` (1=23%, 2=8%, 6=5%, 3/4/5=0%),
    `deliveries` (1..7: 24h/48h/3/4/5/10/14 dni — brak etykiety „7 dni").
  - **Warunki wejścia do feedu (oficjalna dok.):** produkt aktywny + czas realizacji + (producent — ale **feed
    Google jest ZWOLNIONY z wymogu producenta**, wg shoper.pl/learn) + zaznaczony „widoczny" w porównywarce.
    Panel: **Zwiększaj sprzedaż > Porównywarki cen > wiersz GoogleProductSearch** (suwak Aktywność → adres XML).
    Odświeżanie: „w ciągu godziny od ostatniej modyfikacji produktu". Weryfikacja domeny w GMC: panel Shopera
    **Wygląd i treści > Wygląd sklepu > Integracje > Weryfikacja witryny** (metoda HTML-tag). Skrypty próbkujące
    READ-ONLY w scratchpadzie sesji (`gmc-sample.ps1`, `gmc-sample2.ps1`).
  **Bez zmian łamiących pola/parametry GET; ZERO zapisów do sklepu.**
- **Ostatnio zweryfikowano (poprz.):** 2026-07-01 (DIAGNOSTYKA 3 OBJAWÓW LEO — READ-ONLY, tylko GET; dowód „to DANE, nie CSS”).
  **Co NOWE/KRYTYCZNE:**
  - **`product-images` — kształt + mechanizm głównego zdjęcia POTWIERDZONY.** Pola rekordu GET: `gfx_id`,
    `product_id`, `name`, `unic_name`, `order`, `hidden`, **`main` (0/1)**, `translations`, `extension`.
    `count` globalny = 16872. Filtr **`?filters={"product_id":"<id>"}` DZIAŁA** (zwraca zdjęcia produktu).
    **GŁÓWNE zdjęcie = rekord z `main=1`**; produktowe `main_image` (obiekt) = ten sam obraz. W próbce (Milwaukee,
    Den Braven, Bostik, kołki) `main=1` **zawsze na obrazie o NAJNIŻSZYM `order`**, ale `order` startuje od
    dziwnych wartości (3/4/7/12, NIE od 1) i rośnie razem z `gfx_id` → **`order` = artefakt kolejności importu
    Leo, nie zamierzona kolejność galerii**. Wniosek: „które zdjęcie jest główne” = pole DANYCH (`main`),
    ustawiane przez Leo na pierwszym zaimportowanym obrazie; jeśli w Subiekcie „główne” to inny plik → Leo
    ustawia `main=1` na złym rekordzie. Motyw tego nie liczy (renderuje `main=1`/`main_image`).
  - **⛔ KOREKTA sekcji „Jednostka sprzedaży”: `unit_price_calculation` NIE jest 0 w całym katalogu — JEST
    używane na ~14% (427/3000 skanu) i DLA CZĘŚCI PRODUKTÓW GENERUJE BŁĘDNĄ „cenę za jednostkę”.** Pola:
    `unit_price_calculation` (top-level 0/1 = włącznik), `stock.calculation_unit_id` (jednostka miary kalkulacji),
    `stock.calculation_unit_ratio` (przelicznik = ilość w tej jednostce); cena za jedn. = `price / ratio`.
    Chemia płynna (Den Braven/Bostik/silikony/pianki): `calculation_unit_id=11` (litr) + `ratio` = objętość
    (280ML→0,28; 400ML→0,4; 750ML→0,75) → **poprawnie**. ALE narzędzia/BHP Milwaukee (kaski, okulary, kamery
    inspekcyjne, piły, osłony) mają `unit_price_calculation=1` z **`calculation_unit_id=15` (5szt) / `14` (10szt.)
    i `ratio` 0,2 / 0,1** → `price/0,2` lub `price/0,1` = absurd (kask 450,92 → **2254,60 zł/5szt**; kamera
    1347,65 → 6738,25; piła SAWZALL 97,87 → 978,70). Kotwy stalowe: `100szt` + `ratio 0,01` → `×100` (10,18 →
    1018 zł/100szt). Wzorzec: `ratio ≈ 1/N` przy jednostce `Nszt` → wygląda na wagę/przelicznik pomocniczy
    z Subiektu wciśnięty w pola „ceny jednostkowej”. **`stock.weight` nadal ~0% (15/1500, 0/222 chemii)** →
    to NIE waga zasila kalkulację, tylko `calculation_unit_*`. **To DANE z Leo/Subiekt, nie CSS.**
  - **Słownik `units` urósł do count=23** (było 16) — kolejne duble z Leo: `17=100s`, `18=100s.`, `19=200szt`,
    `20=150szt`, `21=butla`, `22=200butla`, `23=kg.` (obok `2=kg`). `calculation_unit_id` referuje ten sam słownik.
  - **`categories` count=283** (rosło 252→268→283). **14 zduplikowanych NAZW** (`Dmuchawy` 155/301, `Kosiarki`
    204/303, `Piły łańcuchowe` 118/300, `Elektronarzędzia ogrodowe` 117/287, `Klucze dynamometryczne` 140/233,
    `Narzędzia pomiarowe` 134/138, `Nitownice` 127/214, `Wentylatory` 105/311, `Inne` 148/286 i in.) — nowsze
    duplikaty = wyższe ID, głównie zdublowana gałąź ogrodowa/narzędzia (order często 0 = utworzone po sortowaniu
    A→Z). **Relacja produkt↔kategoria = pola `category_id` (główna) + `categories[]` NA PRODUKCIE** (potwierdzone:
    prod 2000→114, 384→192, 94→41 itd.), **niezależne** od opisu/nazwy/`order` kategorii. Drzewo `categories-tree`
    (parent→children, zagnieżdżone `id`/`children`) **NIENARUSZONE**, **0 pustych nazw** → rollout opisów
    (`description`/`description_bottom`) i sort A→Z **NIE uszkodziły** struktury (PUT był częściowy). Duplikaty
    nazw = realne ryzyko dla mapowania Leo „grupa Subiektu → kategoria po nazwie” (dwuznaczność → produkt może
    „wracać” do starej kategorii po sync). Skrypty diagnostyczne (READ-ONLY) w scratchpadzie sesji.
  **Bez zmian łamiących pola/parametry GET; ZERO zapisów do sklepu.**
- **Ostatnio zweryfikowano (poprz.):** 2026-06-19 (KLIENCI — próba sprzątania po imporcie: DELETE konta testowego).
  **Co NOWE/KRYTYCZNE:** **DELETE `users`/`user-addresses` przez webapi = HTTP 403 `insufficient_scope`** —
  konto webapi PLASMET (`.env`) **nie ma zakresu „usuwanie"**. 3× DELETE (`users/7`, `user-addresses/6`,
  `user-addresses/7`) → 403 zarówno tokenem permanentnym, jak i z `POST /auth` (Basic Auth). Żądania
  odrzucone PRZED wykonaniem → stan nienaruszony (`users count`=432, recon GET potwierdził tożsamość
  testowego `user_id=7` po emailu `mikolaj.jesion+plasmettest@gmail.com`). Odblokowanie = nadanie
  uprawnienia delete w panelu (Administratorzy / token permanentny „+usuwanie") albo usunięcie ręczne
  w panelu. Skrypty `cleanup-test-user-step1..3` + `step2b` (gotowe do ponowienia po nadaniu scope).
  Nowa podsekcja „⛔ DELETE … insufficient_scope". **Bez zmian łamiących pola/parametry GET/POST/PUT.**
- **Ostatnio zweryfikowano (poprz.):** 2026-06-18 (KLIENCI — TEST FEASIBILITY `default`/`shipping_default`, 1 PUT za zgodą).
  **Co NOWE:** na **jedynym adresie klienta `default='1'`/`shipping_default='1'` są WYMUSZONE przez Shopera** —
  PUT `user-addresses/8` z `default="0"`/`shipping_default="0"` → HTTP 200/body `1`, ale GET po PUT pokazuje
  oba pola znów `'1'` (serwer auto-promuje jedyny adres na domyślny; nie błąd payloadu, lecz wymuszenie biznesowe).
  → `default=0` na jedynym adresie **NIEOSIĄGALNE** webapi; wymaga ≥2 adresów u klienta. Recon: 3 użytkowników
  (8/220/432) każdy `count=1`, `1`/`1`. Skrypty `useraddr-default-recon.ps1`, `useraddr-default-puttest.ps1`.
  **Bez zmian łamiących pola/parametry.**
- **Ostatnio zweryfikowano (poprz.):** 2026-06-18 (KLIENCI — KROK TESTOWY ZAPISU, 1 konto utworzone za zgodą).
  **Co NOWE/POTWIERDZONE EMPIRYCZNIE:** (1) pole hasła w POST `users` = **`pass`** (HTTP 200, `user_id=7`;
  `password` nie testowano bo `pass` zadziałało). Payload `users` (string-y `"0"/"1"`, `group_id=null`,
  `pass`) zapisuje się 1:1 (GET potwierdził firstname/lastname/email/newsletter/active). (2) **POST
  `user-addresses` ma 4 pola WYMAGANE nieujawnione przez GET: `street_1`,`city`,`zip_code`,`country_code`**
  — bez nich (lub z pustym `''`) → HTTP 400 „Pole wymagane". Działa dopiero z placeholderami + `country_code='PL'`
  (`address_book_id=6` → `user_id=7`). To **blocker masy**: Mercatum nie ma adresów pocztowych → decyzja usera
  (placeholdery vs pominięcie `user-addresses`). (3) Filtr `user-addresses` opóźniony po POST → czytaj ID z body
  POST. **Bez zmian łamiących w `users`.** Skrypty: `import-klienci-test.ps1`, `import-klienci-test-addr.ps1`.
- **Ostatnio zweryfikowano (poprz.):** 2026-06-18 (KLIENCI — ROZEZNANIE READ-ONLY pod import 438 kont z Mercatum, BEZ zapisu).
  **Co NOWE:** klient = zasób **`users`** (NIE `customers`); dane rozdzielone: `users` (tożsamość, `email` wymagany,
  `firstname`/`lastname`/`newsletter`(0/1)/`group_id`/`active`/`lang_id`/`comment`; hasło = pole `pass` write-only,
  niewalidowane długością — do POTWIERDZENIA 1 POST-em) + **`user-addresses`** (telefon=`phone`, firma=`company_name`,
  NIP=`tax_identification_number`, `pesel`, adres; FK `user_id`). Grupy = **`user-groups`** (count=0 → grupa domyślna,
  brak detal/hurt/B2B). **Telefon/firma NIE w `users`** → 2 żądania na klienta (POST users → POST user-addresses).
  Na żywo **`users` count=6** (3 demo + 2 właścicielskie + 1 wykonawcze → zero kolizji z realnymi klientami Mercatum).
  Nazwy `customer*`/`customer-groups` → 400 „Missing MODULE". Dok. oficjalna = SPA/login (`WebFetch`→menu) → pola
  potwierdzone empirycznie GET-em. Nowa sekcja „Klienci". **Bez zmian łamiących pola/parametry.**
- **Ostatnio zweryfikowano (poprz.):** 2026-06-18 (CZAS WYSYŁKI per produkt — ETAP 1 RECON + TEST, partial-PUT na 2 prod. za zgodą).
  **Co NOWE:** **`stock.delivery_id` ZAPISYWALNY** partial-PUT `{"stock":{"delivery_id":"X"}}` → 200; różnica PRZED↔PO
  (40/39 top-level + 38/37 pól `stock`) = **TYLKO `delivery_id`** (+ auto `edit_date`), reszta `stock` (stock/avail/ceny/
  ean/code/Omnibus) i top-level BEZ ZMIAN → bezpieczny kształt do masowego zapisu. **POST `deliveries` → HTTP 500 server_error
  = READ-ONLY** (jak `availabilities`) → nowy termin „7-14 dni" tylko w panelu; OOS używa istniejącego „14 dni" (id 7).
  Słownik `deliveries`: 48h=id 2, 14 dni=id 7, 10 dni=id 6. Zakres: TOTAL 7944, OOS(stock≤0)=2896, dostępne=5048.
  Skrypt: `delivery-set-recon.ps1`; backup `backup/delivery-set-20260618/`. **Bez zmian łamiących pola/parametry.**
- **Ostatnio zweryfikowano (poprz.):** 2026-06-18 (PRÓBA FLIP OOS → zamawialny, wariant A globalny: zmiana `can_buy` na statusie id 1).
  **Co NOWE:** **Zasób `availabilities` jest READ-ONLY przez webapi** — `PUT /availabilities/{id}` → **HTTP 500 `server_error`
  dla KAŻDEGO kształtu body** (7 wariantów idempotentnych) ORAZ dla nieistniejącego ID (99999 → 500, nie 404) ⇒ handler
  zapisu niesprawny, nie błąd payloadu. **Backup wykonany** (`backup/availabilities-przed-oos-flip-20260618.json`, 9 rekordów);
  rekord id 1 nietknięty po próbach. **Flip `can_buy=0→1` + nazwa + tryb karty = DO ZROBIENIA W PANELU** (Ustawienia >
  Produkty > Statusy dostępności > „Ustawienia dodatkowe"). Próbka READ-ONLY potwierdza mechanizm: prod 98/143 (stock=0) →
  `calculated_availability_id=1`; prod 93 (stock=3.25)→2; prod 94 (stock=45)→5 (dostępne nie dotyka status 1). Dok. oficjalna
  niedostępna (SPA+login) — nazwę/metody potwierdzono empirycznie. **Bez zmian łamiących pola/parametry.**
- **Ostatnio zweryfikowano (poprz.):** 2026-06-17 (DIAGNOZA MECHANIZMU OOS / sprzedaży przy zerowym stanie — READ-ONLY, BEZ zapisu).
  **Co ustalono / co NOWE w API:** (1) produkt **NIE ma** pól `can_buy`/`availability`/`delivery` (38 kluczy top-level) —
  zakup steruje **flaga `can_buy` na rekordzie `availabilities`**, dziedziczona przez `stock.calculated_availability_id`
  (auto ze stanu); `stock.availability_id`/`stock.delivery_id` (ręczne nadpisania) **PUSTE na całym katalogu** PLASMET.
  (2) Zasób **`deliveries` ISTNIEJE i jest dostępny** (count=7: 24h/48h/3/4/5/10/14 dni; **brak „7 dni"**); poprawna nazwa
  to `deliveries` (NIE `delivers`/`shippings`). (3) `availabilities` count=9 z **dublem** „średnia ilość" (id 2 vs 4, różny
  `can_buy`); stan≤0 → id 1 „tymczasowo niedostępny" (`can_buy=0`) = przyczyna blokady koszyka. (4) Oficjalna dok.
  (pomoc.shoper.pl): zakup przy zerowym stanie = ustawienie **per status dostępności** (Ustawienia > Produkty > Statusy
  dostępności > „Ustawienia dodatkowe"), NIE globalne/per-produkt. Nowa sekcja „Dostępność / sprzedaż przy zerowym stanie".
  **Dok. oficjalna** = SPA za loginem (`WebFetch` na developers.shoper.pl → menu); nazwę `deliveries`/`availabilities`
  i mechanizm OOS potwierdzono `WebSearch` (shoper.pl/help) + empirycznie GET. **Bez zmian łamiących pola/parametry.**
- **Ostatnio zweryfikowano (poprz.):** 2026-06-16 (ROLLOUT SPLITU OPISU KATEGORII góra/dół na CAŁY KATALOG — WDROŻENIE NA ŻYWO za zgodą usera).
  **Zakres:** wszystkie **252 kategorie** z treścią w `description` zawierającą `<h3>` (kat. 61 już zrobiona wcześniej → pominięta
  przez idempotencję). Cięcie na **pierwszym `<h3>`**: GÓRA (wstęp `<h2>`) → `translations.pl_PL.description`, DÓŁ (od `<h3>`) →
  `translations.pl_PL.description_bottom`. **BEZ wrappera** `.plasmet-cat-seo` (decyzja usera — kartę dołu daje klasa kontenera
  motywu `.category-additional-description`). Per kategoria ATOMOWO: świeży GET + backup (cały rekord + stara `description`) →
  PUT DÓŁ → GET-weryf (dół bit-w-bit ORAZ góra pełna) → PUT GÓRA → GET-weryf końcowa (góra od `<h2>`, bez `<h3>`, bez mojibake).
  **Wynik: 249/252 SPLIT za pierwszym przebiegiem; 3 dograne osobno** (kat. 84, 249 = BLAD-DOL: dół nie utrwalił się mimo PUT 200
  — najpewniej 429 w GET-weryf; GÓRA NIE ruszona → stan wyjściowy bezpieczny, dograne `-OnlyIds 84,249`; kat. 255 = BLAD-WERYF:
  dół zapisany, ale PUT GÓRY nie utrwalił — dograna sam PUT GÓRY, bo idempotencja pomijała ją po niepustym `description_bottom`).
  **Końcowo 252/252 SPLIT, 0 ubytków treści.** **⚠️ Limit żądań API = 10/jednostkę** (`429 temporarily_unavailable: requests limit
  10/10`) — przy throttle 400 ms i tak pojawiło się 31 retry, wszystkie naprawione backoffem 500ms→8s; przy masie zapisów to NORMA,
  nie błąd. **⚠️ Pułapka:** PUT `categories/{id}` potrafi zwrócić `200 raw=1`, a treść NIE utrwala się bit-w-bit (race z 429) →
  **zawsze weryfikuj GET-em po zapisie**, a kolejny PUT zależny (GÓRA po DOLE) rób tylko po potwierdzeniu poprzedniego.
  Skrypty: `cat-desc-split-rollout-apply.ps1` (`-DryRun` domyślnie; `-OnlyIds` do dogrywek), inwentaryzacja
  `cat-desc-split-rollout-recon.ps1` → `_rollout-inwentaryzacja.json` (252 kand.). Backupy per kategoria:
  `backup/rollout-20260616/cat<ID>-record.json` + `cat<ID>-description-old.html` (252+252), raport `_rollout-raport.json`.
  Rollback kat.: PUT `categories/{id}` z `{translations:{pl_PL:{description:<cat<ID>-description-old.html>, description_bottom:''}}}`.
  Dok. oficjalna nadal SPA/login — `description`/`description_bottom` potwierdzone empirycznie. **Bez innych zmian API.**
- **Ostatnio zweryfikowano (poprz.):** 2026-06-16 (SPLIT OPISU KATEGORII na góra/dół — WDROŻENIE NA ŻYWO za zgodą usera, kat. 61 „Elektronarzędzia").
  **NOWE USTALENIE:** pole **`translations.pl_PL.description_bottom` („opis dół") jest ZAPISYWALNE przez webapi** (PUT 200 `raw=1`;
  sonda markerem na pustym polu + atomowy split: DÓŁ→GET-weryf→GÓRA). Split kat. 61: GÓRA 470 zn. (krótki wstęp `<h2>`),
  DÓŁ 1669 zn. (wrapper `plasmet-cat-seo` + „Co znajdziesz"/„Jak wybrać"), bit-w-bit OK, zero mojibake, 4 linki `/pl/news/` do
  opublikowanych poradników (active=1). Backup: `backup/cat61_backup_*.json` + `backup/cat61-description-old_*.html`. Nowa sekcja
  „Opis dół kategorii" wyżej. Dok. oficjalna nadal SPA/login — pole potwierdzone empirycznie. **Bez innych zmian API.**
- **Ostatnio zweryfikowano (poprz.):** 2026-06-16 (SKAN OOS PER MARKA/KATEGORIA — bramka 0.4 Fazy 0 — READ-ONLY, BEZ zapisu).
  **Dokumentacja API aktualna** (dok. oficjalna za loginem/SPA — pola potwierdzone na żywo, bez zmian w zasobach/polach).
  **Zakres:** GET `products` (`limit=50`, **pełny skan 159 stron**, `count`=**7943**), `producers` (`count`=**50**), `categories`
  (`count`=**268**), `categories-tree` (**9 węzłów top-level = 9 rootów**), `availabilities`. **Potwierdzone pola pod OOS:**
  produkt ma top-level `producer_id` (int), `category_id` (główna, int), `categories` (tablica id), `stock.stock`
  (ilość — **MOŻE BYĆ UŁAMKOWA**, np. `3.25` → OOS = `stock.stock <= 0`), `stock.active`, `translations.pl_PL.active`.
  **Nazwa producenta = pole top-level `name`** (NIE `translations.pl_PL.name`, które jest puste dla producentów!);
  **nazwa kategorii = `translations.pl_PL.name`** (kategorie odwrotnie niż producenci). `categories-tree` zwraca `[{id,children}]`
  → mapowanie każdej kategorii do 1 z 9 rootów robi się przez przejście drzewa. **⚠️ Potwierdzona regresja:** filtr
  `{"producer_id":...}` IGNOROWANY (zwraca cały katalog) — agregacja per marka **wyłącznie po skanie całości + grupowanie
  po stronie klienta**. **⚠️ Duble producentów po re-syncach Leo** (Milwaukee 35 vs 44, Baum 26 vs 46, BUDMET 63 vs 23,
  BOSTIK 30/51/66) — agreguj po REALNYM `producer_id` z produktów + nazwa z `producers`; wpisy producenta bez produktów = osierocone.
  Filtr `{"stock.stock":"0"}` DZIAŁA (count=**2895** OOS — spójne z raportem 04: 2 883). Skrypty: `oos-scan-readonly.ps1`
  (główny skan + agregacja), `oos-probe-fields.ps1`/`oos-probe-names.ps1` (rozeznanie pól). Raport: `migracja/faza-0/0.4-raport-oos.md`.

- **Ostatnio zweryfikowano (poprz.):** 2026-06-15 (ROZEZNANIE ZBIORU BOSTIK + DEN BRAVEN + podmarki pod karty SDS — READ-ONLY, BEZ zapisu).
  **Zakres:** GET `producers` (count=**49**) + pełny skan `products` (`limit=50`, 159 stron, `count`=**7943**) z filtrem
  po stronie klienta (`producer_id` IN markowe id **LUB** `name` ~ `DB`/`BOSTIK`/`MAMUT`/`TECTANE`, case-insensitive).
  **Wynik:** **222 produktów** „nasze" Bostik/Den Braven (rozbicie marka: **DEN BRAVEN 183, BOSTIK 37, MAMUT 2, TECTANE 0**);
  pokrycie identyfikatorów: **ean 99,5% (221/222, brak 1: `07DKC` BOSTIK FIXPRO KOTWA CHEMICZNA)**, **code 100%**.
  **Den Braven NIE jest osobnym producentem** (brak wpisu „Braven"/„DB" w 49 producentach; „DB …" w nazwie = Den Braven
  jako Bostik). **⚠️ ZMIANA id producentów Bostik (regresja vs notatki):** realne produkty wiszą teraz pod **id 51 „BOSTIK
  NIEAKTUALNE" (176) i 66 „BOSTIK" (45)**, NIE pod 30/43 (43 = 0 prod., osierocony) — kolejna migracja id po re-syncu Leo
  (jak Baum 26→46). **⚠️ FILTR `producers.producer_id` TEŻ JUŻ IGNOROWANY** (zwraca 7943 dla 30/43/51/66) — regresja względem
  notatki 2026-06-15, gdzie ten wariant rzekomo działał; **jedyna pewna metoda = pełny skan katalogu + filtr po stronie
  klienta.** Dok. oficjalna = SPA (`WebFetch`→samo menu); `WebSearch` bez sygnałów o zmianach łamiących pola/parametry.
  Skrypt: `bostik-denbraven-recon.ps1`; zrzuty: `_rozeznanie/bostik-denbraven-nasze.json` (222 rek.),
  `bostik-denbraven-producenci.json` (49), `bostik-denbraven-meta.json` (statystyki przebiegu).
- **Ostatnio zweryfikowano (poprz.):** 2026-06-15 (DOPASOWANIE PRODUKTÓW DO 3 KART CPR BUD-MET — READ-ONLY, BEZ zapisu/uploadu).
  **Zakres:** pełny skan `products` (`limit=50`, 159 stron, `count`=7943) z `translations.pl_PL.translation_id`;
  klasyfikacja po nazwie `translations.pl_PL.name` (typ: `regulacyjn|dystansow` vs `talerzow|ciesielsk|konstr.drew`;
  średnica = liczba przed `x`/`×` w tokenie wymiaru). **Dok. API bez zmian** — GET produktu zwraca `translations.pl_PL`
  (`name`, `translation_id`, `permalink`) zgodnie z dotychczasowym opisem; `WebFetch` na developers.shoper.pl = SPA (samo
  menu), `WebSearch` potwierdził pole `translations->pl_PL->name`. **Wynik:** BUD-MET = `producer_id=23` (bez dubli);
  KARTA A (regulacyjne 6x)=5, KARTA B (talerzowe ciesielskie 6x)=5, KARTA C (talerzowe ciesielskie 8x)=18, DO WERYFIKACJI=0;
  wszystkie 28 dopasowań ma `producer_id=23` (100% zgodność producent↔nazwa); katalog używa „regulacyjny" (5×), NIE „dystansowy" (0×).
  ⚠️ **Pułapka PowerShell:** operator `$tab += $rec` na `@()` w pętli z funkcjami `return [bool]/@(...)` GUBIŁ elementy
  (wynik 0/0/0) → użyć `System.Collections.ArrayList` + `[void]$list.Add()`. Skrypty: `wkrety-cpr-recon.ps1` (skan API),
  `wkrety-cpr-classify.ps1` (klasyfikacja ze zrzutu); listy: `_rozeznanie/wkrety-*-kandydaci.json` + `wkrety-do-weryfikacji.json`.
- **Ostatnio zweryfikowano (poprz.):** 2026-06-15 (`product-files` NAPRAWA ROZSZERZENIA `.pdf` w pobraniu — 81 kart Baum, za zgodą usera).
  **Problem:** karty PDF wgrane wcześniej **pobierały się bez rozszerzenia** (user: „Typ pliku: Plik", nie otwiera).
  **Diagnoza (READ-ONLY, file_id=73):** treść OK (magic `%PDF`, `file_size`=1494031), ale `Content-Disposition:
  filename="Karta-bezpieczenstwa-wiertla-4-ostrzowe-PDF"` (bez `.pdf`), `Content-Type: application/force-download`.
  **Przyczyna ustalona:** **serwowana nazwa pobrania = SLUG zbudowany z `name`** (NIE hash GET, NIE `file_name` GET, NIE treść).
  Stare `name='Karta bezpieczenstwa - wiertla 4-ostrzowe (PDF)'` → slug `…-PDF` → brak `.pdf`. **Metoda naprawy = PUT**
  `product-files/{id}` `{name:"Karta-bezpieczenstwa-wiertla-4-ostrzowe.pdf", file_name:"…"}` — sam PUT regeneruje slug
  (kropka przed rozszerzeniem zachowana) → CD `filename="…-4-ostrzowe.pdf"` + `%PDF` (potwierdzone na żywo na file_id=73,
  bez re-uploadu treści). **DELETE+POST ODRZUCONE:** DELETE `product-files/{id}` = **HTTP 403 `insufficient_scope`**
  (brak uprawnienia delete), a re-POST tworzy duplikat (powstał file_id=177 — ukryty `PUT {active:0}`). **Wynik:**
  PUT na 80 pozostałych (79 OK + 1 `409 Object is locked` = file_id=133, trwały lock prod. 7035 — Leo Sync?);
  **pokrycie name-z-`.pdf` = 80/81** (file_id=133 do dokończenia po zwolnieniu locka). Front: bezpośrednie pobranie
  `/pl/p/file/<hash>/<slug.pdf>` serwuje `.pdf`+`%PDF`; ⚠️ **cache HTML karty** chwilowo linkuje stary slug (baza OK,
  cache odświeża się sam). Rate-limit instancji ostry → throttle 350–500 ms + retry/backoff na 429/409. **Naprawiono
  źródło:** `productfiles-bulk-apply.ps1` (`name`/`file_name` = ASCII-myślniki + `[IO.Path]::GetExtension($FilePath)`;
  domyślny `-DocName` bez „(PDF)"); reguła twarda dopisana do `SKILL.md` i sekcji `product-files` wyżej. Skrypty:
  `productfiles-diag-pdf-ext.ps1`, `productfiles-fix-pdf-ext.ps1` (test 1), `productfiles-fix-pdf-ext-bulk.ps1` (masowy PUT),
  `productfiles-verify-front-pdf.ps1`. Log: `_rozeznanie/productfiles-fix-pdf-ext-log.json`. Dok. oficjalna = SPA za loginem
  (`WebFetch`→login); `WebSearch` potwierdził endpoint `product-files/update` (PUT) — szczegóły zweryfikowane empirycznie.
- **Ostatnio zweryfikowano (poprz.):** 2026-06-15 (ROZEZNANIE DANYCH POD BOGATĄ KARTĘ PRODUKTU — READ-ONLY, BEZ zapisu).
  **Werdykt:** dane „premium" PDP **mają zerowe pokrycie**. ✅ Mają pokrycie: `ean`(~98%), `code`(100%), `stock.price`,
  `stock.stock`(~70% >0), `description`(~95%), `producer_id`, `main_image`. ❌ PUSTE w całości: **atrybuty/parametry**
  (`attribute-groups` count=0, `attributes` count=0, pole `attributes`=`[]` na 0/500 prod.), **promocje** (`promo_price`=null,
  `special_offer` brak pola, `stock.price_special`==`price`, 0/500), **opinie** (`product-reviews`→**HTTP 403** brak dostępu
  webapi nawet do odczytu), **powiązane** (`related`=`[]`, 0/500; `accessories`/`cross-sells`→Missing MODULE), **logo marki**
  (`producers.gfx` 0/28), flagi `bestseller`/`newproduct`/`is_product_of_day` (0/500), wymiary (0.0000). Produkt 2000
  potwierdzony = FDD3-0 (cat 114, **producer 44** — nie 35; duble producentów z Leo). `availabilities` count=9 = etykiety
  ilości, NIE czasu wysyłki. **⚠️ Ryzyko Leo:** ręczne uzupełnianie atrybutów/powiązań webapi może być nadpisane przy sync
  (uzupełniać u źródła w Subiekt/Leo). Nowa sekcja „Pola produktu pod BOGATĄ KARTĘ PRODUKTU (PDP)" wyżej. Oficjalna dok.
  = SPA (`WebFetch` redirect→login); `WebSearch` potwierdził istnienie zasobów `attributes`/`attribute-groups` + modułu
  Storefront `product_review` (nazwa zasobu REST potwierdzona empirycznie = `product-reviews`, 403 na tym koncie).
  Skrypty: `pdp-feasibility-recon.ps1`, `pdp-feasibility-recon2.ps1`. Deliverable:
  `szablon/design-claude/strona-produktu-2026-06/feasibility-dane.md`.
- **Ostatnio zweryfikowano (poprz.):** 2026-06-15 (`product-files` MASOWY APPLY — karta bezpieczeństwa PDF na wszystkie wiertła Baum, za zgodą usera).
  **Wynik:** **pokrycie 81/81 wierteł Baum** (`category_id=173`, `producer_id=46`) ma kartę PDF (`file_size=1494031` B).
  79 POST-ów wykonanych (79 OK / 0 timeout / 0 error), 2 pominięte idempotencją (tid 6965 testowy `file_id=73`, tid 6967
  diagnostyczny `file_id=74`). Throttle 200–300 ms, retry 3× backoff (429/5xx) — nie wystąpiły żadne 429/5xx.
  **⚠️ KLUCZOWE USTALENIE:** **`file_name` jest WYMAGANE w body POST `product-files`** — bez niego HTTP 400
  `{"error":"invalid_request","error_description":"Key 'file_name' is required"}` (cała pierwsza próba masowa: 400 ×N,
  ZERO rekordów utworzonych — sklep niezmieniony do czasu poprawki). Po dodaniu `file_name` → 200 + `file_id`.
  Pułapka PS 5.1: zmienna **`$pid` jest read-only** (PID procesu) — używać innej nazwy (`$prodId`).
  Skrypty: `baum-wiertla-bulk-apply.ps1` (masowy, `-DryRun` domyślnie / `-Apply`), `_diag-productfile-400.ps1` (diagnoza 400).
  Log wyniku: `_rozeznanie/baum-wiertla-apply-log.json` (81 wpisów: translation_id, product_id, file_id, file_size, status).
- **Ostatnio zweryfikowano (poprz.):** 2026-06-15 (`product-files` UPLOAD — rozeznanie READ-ONLY + 1 KONTROLNY POST, BEZ masowego zapisu).
  **Co ustalono (zweryfikowane na żywo):** (1) **ZAPIS `product-files` DZIAŁA** — POST `{translation_id, name, description,
  content(base64), type:1, active:1, order:1}` utworzył `file_id=73`, POST zwrócił samo ID (nie wisi). (2) **Wiązanie przez
  `translation_id`** (= `translations.pl_PL.translation_id`, ≠ `product_id`; produkt 6974 → tid 6965). (3) **`content` = czysty
  base64** zawartości pliku (nie data-URI); `file_size` = dokładny rozmiar (1494031 B), `file_name` = hash MD5 nadany serwerem.
  (4) **`name` SANITYZOWANE do ASCII** (ł/ń/— → l/n/-), `description` ZACHOWUJE polskie znaki. (5) **Front renderuje natywnie**
  sekcję „Pliki do pobrania" (`file-box`, `<a download href=/pl/p/file/<hash>/<slug>>`) — bez zmian motywu. (6) **Filtr
  `producer_id` IGNOROWANY** (zwraca 7938) — działa `producers.producer_id`; do pewności skan całego katalogu + filtr po stronie
  klienta. (7) **Baum = `producer_id=46`** (NIE 26 — id 26 to stary/pusty duplikat po re-syncu Leo); **81 wierteł „SDS PLUS X4"
  = całość 4-ostrzowych**, `category_id=173`. **⚠️ KOREKTA notatki 2026-06-13** („producer_id filtr działa, Baum=26") — nieaktualna.
  Skrypty: `productfiles-recon-readonly.ps1`, `baum-wiertla-recon.ps1`, `productfiles-test-upload.ps1`. Dok. oficjalna SPA (WebFetch
  zwrócił login); endpoint `product-files/insert` potwierdzony przez WebSearch (developers.shoper.pl), payload zweryfikowany empirycznie.

- **Ostatnio zweryfikowano (poprz.):** 2026-06-13 (PLAN DANYCH home — rozeznanie READ-ONLY pod natywne moduły strony głównej, BEZ zapisu).
  **Ustalenia (potwierdzone na żywo GET):** (1) **Flaga „polecane/main_page" produktu = `translations.pl_PL.main_page`** (`0/1`) +
  `main_page_order` (kolejność). Na koncie TEST **0 produktów** ma `main_page=1` (filtr `{"translations.main_page":"1"}` zwrócił
  `count=0`). To pole zasila natywny moduł „Polecane/Bestsellery". (2) **⚠️ FILTR PO KATEGORII NA `products` NIE DZIAŁA na tej
  instancji** — `filters={"category_id":...}` (string/int/operator), `{"categories.category_id":...}`, `{"categories":{"in/="}}`,
  `main_category_id` → **wszystkie HTTP 404** (jak filtr `code`, patrz część B/2026-06-11); a `{"categories.category_id":"61"}`
  oraz parametr `?category=61` zwracają **CAŁY katalog (7938)** = filtr ignorowany. **→ Webapi tej instancji NIE pozwala policzyć
  produktów per-kategoria filtrem** (do licznika kafla trzeba liczyć po stronie front/motywu albo iterować cały katalog mapując
  `category_id`). (3) **Produkt wisi na LIŚCIU drzewa, nie na root** — `products/2000` (Milwaukee FDD3-0) ma `category_id=114`
  (podkat. „Wiertarko-wkrętarki"), nie 61 (root „Elektronarzędzia") → licznik roota wymaga sumy całego poddrzewa. (4) **Filtr
  `producer_id` DZIAŁA** (Milwaukee=35 → 3369, Richmann=36 → 2280, Baum=26 → 198, Klingspor=29 → 235, Collomix=40 → 31). ⚠️ Liczby
  kategorii/marek z prototypu home (Milwaukee 2311, Richmann 422…) **NIE zgadzają się z realnymi** — były szacunkowe. (5) **Logo
  producenta = pole `gfx`** (top-level `producers`), na koncie TEST **PUSTE dla 0/20 producentów** → żadna marka nie ma wgranego
  logo w katalogu; loga marek na home to osobne pliki `/userdata/public/assets/<slug>.webp` wgrane PANELEM (nie webapi). (6) **Den
  Braven NIE istnieje jako osobny producent** (brak w 20 producentach; brak produktów z „Braven" w nazwie) — klej Mamut figuruje
  jako „Bostik MAMUT GLUE" pod `producer_id=30` (Bostik). (7) **Blog: 7 wpisów `news`** (id 8-12,14,15), wszystkie `active=1`,
  `start_page=1`, `image_name` niepuste (= mają główne zdjęcie). Wpisy z prototypu istnieją: M12 vs M18 = `news_id=12`, wybór
  wkrętarki = `news_id=8`, silikon = `news_id=14`. Skrypty (READ-ONLY): `home-plan-dane-recon.ps1`, `-recon2.ps1`, `-recon3.ps1`;
  zrzut `_rozeznanie/home-plan-dane.json`. Deliverable: `szablon/design-claude/main-page-2026-06/plan-dane.md`. **Dok. webapi
  AKTUALNA, ZERO zmian API** — `WebFetch` developers.shoper.pl nadal SPA; `WebSearch` potwierdził natywne moduły „Kolekcja"/
  „Polecane produkty" (oznaczanie flagą), „Producenci" + „Rotator logotypów producentów" (loga wgrywane w panelu, nie webapi).

- **Ostatnio zweryfikowano (poprz.):** 2026-06-12 (JEDNOSTKA SPRZEDAŻY produktu — diagnostyka READ-ONLY, BEZ zapisu).
  **Ustalenia:** jednostka sprzedaży = pole **`unit_id`** (top-level produktu) → zasób **`units`** (`count=16`,
  pola `unit_id`/`floating_point`/`translations.pl_PL.name`). **`unit_id` niepuste w 100%** (próbka 1238 prod.).
  Katalog **zróżnicowany**: `szt`(7) ~76–84%, `opak`(9) ~7–16%, `100szt`(6) ~3,5%, `para`(8), `blister`(13),
  `rolka`(12). Słownik ma **duble z Leo/Subiekt** (1`szt.`vs 7`szt`, 6`100szt`vs 10`100szt.`); realnie używane 7 i 6.
  `unit_price_calculation`/`stock.calculation_unit_*` = OSOBNY mechanizm „ceny jednostkowej" unijnej (w PLASMET
  puste/0). Render „/szt" przy cenie = **MOTYW (Storefront/`shoper-cli`)**, brak globalnej flagi w `application-config`
  (jedyne pola unit: `product_defaults_unit_id`=1, `product_defaults_bundle_unit_id`=4 — READ-ONLY webapi). **Ryzyko
  Leo:** `unit_id` zasilany z Subiekt GT → zmiany na Shoperze mogą być nadpisane przy sync (poprawiać u źródła).
  Nowa sekcja „Jednostka sprzedaży produktu" wyżej. Skrypty: `diag-unit-sprzedazy-readonly.ps1`,
  `diag-unit-rozklad-szeroki-readonly.ps1`. Oficjalna dok. = SPA (zwraca menu/login); `WebSearch` potwierdził
  pole `unit_id` + zasób `units` + panel „Ustawienia > Produkty > Jednostki miar" — dok. zasobu `units` aktualna.

- **Ostatnio zweryfikowano (poprz.):** 2026-06-12 (PUBLICZNY UPLOAD PLIKÓW przez webapi — sonda READ-ONLY, BEZ zapisu).
  **Werdykt: webapi NIE ma zasobu publicznego uploadu plików** (hosting obrazów do `<img src>` z wolnym URL).
  Sonda 20 nazw-kandydatów (`attachments`/`files`/`media`/`gallery`/`images`/`uploads`/`assets`/`userdata`/…) →
  wszystkie **„Missing MODULE"**; jedyny istniejący zasób plików = **`product-files`** (downloads PRODUKTU:
  `file_name`=hash na dysku, wiązany `translation_id`, BEZ publicznego URL do `<img>`). Loga marek w
  `/userdata/public/assets/` trafiły **przez PANEL (Froala File Manager/elFinder w SVE), NIE webapi** — to
  jedyna droga hostingu publicznych obrazów dla bloku HTML home. Nowa sekcja „Publiczny upload plików" wyżej.
  Skrypty (READ-ONLY): `probe-fileupload-readonly.ps1`, `probe-productfiles-shape.ps1`. Oficjalna dok. = SPA
  (zwraca samo menu; `WebSearch` nie ujawnił zasobu uploadu publicznego) — dok. zasobów plików aktualna.

- **Ostatnio zweryfikowano:** 2026-06-12 (SORT KATEGORII A→Z — backup+plan READ-ONLY + PROBA zapisu `order`, BEZ masowego zapisu).
  **Ustalenia:** (1) **Top-level pole `order` kategorii JEST zapisywalne przez webapi** — proba samoprzywracajaca na kat. 102:
  `PUT /categories/{id} {order:7}` → HTTP 200 raw=1, GET potwierdzil 0→7, `PUT {order:0}` przywrocil 0→0 (sklep czysty).
  To pole steruje pozycja kategorii wsrod RODZENSTWA. (2) **`parent_id` istnieje w POST/PUT kategorii** (potwierdzone
  oficjalna dok./WebSearch: integer, `0`=kat. glowna), ale **GET `categories` go NIE zwraca** — hierarchie czytaj z
  `categories-tree` (zagniezdzony `{id,children[]}`). (3) **Realny katalog PLASMET: 260 kat., 9 korzeni, glebokosc 3 poziomy**;
  prawie wszystkie `order=0` (Leo/Subiekt nie ustawia pozycji → menu bez jawnej kolejnosci). (4) **Polska kolacja**: sort
  rodzenstwa per-parent przez `[CultureInfo]::GetCultureInfo('pl-PL').CompareInfo.Compare(a,b,IgnoreCase)` — poprawnie
  (ł po l, ó po o, ś po s, ż po z; case-insensitive). (5) **⚠️ RYZYKO „Menu" w pasku:** poziome menu kategorii NIE jest
  zawsze drzewem — to konfigurowalny modul **Wyglad i tresci > Linki w naglowku i stopce**; gdy wybrana pozycja
  **`[Wszystkie kategorie]`** → menu odzwierciedla drzewo+`order` dynamicznie (sort zadziala); gdy reczne pozycje →
  sam sort kategorii NIE zmieni paska (trzeba poprawic modul w panelu — NIE ruszac bez zgody). (6) **⚠️ RYZYKO Leo:**
  Leo Synchronizator zasila katalog z Subiekt GT — czy nadpisuje `order` przy synchronizacji = OTWARTE (do potwierdzenia
  przez usera/obserwacji po nast. sync). Skrypty: `categories-sort-backup-plan.ps1` (READ-ONLY backup+plan),
  `categories-sort-apply.ps1` (`-DryRun` domyslnie; `-ProbeId` samoprzywracajaca proba). Backup:
  `backup/categories-order_backup_2026-06-12.json`, plan: `_rozeznanie/categories-sort-plan.json`. **Masowy PUT (220 kat.)
  CZEKA NA ZGODE usera.** Oficjalna dok. = SPA (login/menu), pola potwierdzone empirycznie + WebSearch — dok. `categories` aktualna.)
- **Ostatnio zweryfikowano (poprz.):** 2026-06-12 (DIAGNOSTYKA READ-ONLY pól opisu produktu pod funkcję „wycinek na karcie listy":
  potwierdzono na żywo, że konto TEST `sklep261208` ma **REALNY katalog 7938 produktów PLASMET** z Leo/Subiekta;
  `short_description` = stały blok GPSR „1. Producent…" per-marka (nie opis), `description` = realny opis produktu (~95%
  niepuste, UTF-8 czyste, część rekordów ze śmieciami MSHTML windows-1250 u Sched-Pol). Symulacja pipeline wycinka:
  99,5% użytecznych snippetów z `description`. Nowa sekcja „Pola opisu produktu" wyżej; skrypty `diag-opis-karta-readonly.ps1`,
  `diag-opis-firstsentence-readonly.ps1`. **Bez zapisów do sklepu.** Oficjalna dok. = SPA (zwraca samo menu), kształt pól
  potwierdzony empirycznie z żywych GET — dokumentacja rdzenia produktów aktualna.)
- **Ostatnio zweryfikowano (poprz.):** 2026-06-11 (WDROŻENIE NA ŻYWO za zgodą usera: opisy SEO + meta **WSZYSTKICH 253 KATEGORII**
  — domknięcie thin content na całym katalogu). PUT `categories/{id}` z `translations.pl_PL.{description, seo_title,
  seo_description}` na wszystkich plikach `seo/kategorie/<id>-*.json` (253 plików, 253 unikalnych ID, zero braków pól).
  **WYNIK: 253/253 OK, 0 BŁĘDÓW** (każdy GET-weryfikacja od ręki: `description_len>0` + `seo_title`/`seo_description`
  niepuste; zero zwisów dzięki wzorcowi anti-„wiszący zapis"). Re-PUT 42 wcześniej wgranych był idempotentny (spójność).
  Anty-404 zneutralizował **13 linków** do nieopublikowanych wpisów bloga (w 9 kat.; zostawia tekst kotwicy, usuwa `<a>`),
  surowych `[LINK:` **ZERO** (długi ogon używa gotowych `/pl/c/<slug>/<id>`). **32 kandydatów noindex** (pole `uwaga`)
  dostało opis NORMALNIE — noindex to OSOBNA decyzja panelu/`seo-tech-lead`, NIE ustawiany przez webapi. Niezależna
  weryfikacja GET 6 kat. z różnych partii (61/80/124/169/295/297): description+seo_title+seo_description zapisane,
  polskie znaki OK, **mojibake=False**, `<a>`==`</a>` zbalansowane, **zero martwych linków do bloga**. Skrypty:
  `category-seo-publish-all.ps1` (DryRun domyślnie; retry 2× na 429/5xx/timeout; log per-kat `_category-deploy-log.txt`),
  `category-seo-verify-all.ps1`. **Dok. `categories` AKTUALNA, ZERO zmian API** (developers.shoper.pl nadal SPA/login).
- **Wcześniej 2026-06-11** (WDROŻENIE NA ŻYWO za zgodą usera, A→B→C sekwencyjnie: (A) opisy SEO + meta
  **15 kategorii partii 3**; (B) **meta SEO 20/21 produktów**; (C) domknięcie wpisów bloga #29/#30 → `gotowy`, BEZ publikacji).
  **Dok. `categories`/`products`/`news` AKTUALNA, ZERO zmian API** — `WebFetch` developers.shoper.pl nadal SPA/login (zgodnie
  z notatką), `WebSearch` (Centrum Pomocy `product.translations.save` + `developers.shoper.pl/bulk`) potwierdził strukturę
  `translations.pl_PL` zasobów `categories` ORAZ `products` bez zmian pól/parametrów.
  **CZĘŚĆ A — 15 kategorii partii 3 (ID 81,83,294,84,66,57,124,141,249,106,107,98,295,169,242):** PUT `categories/{id}`
  z `translations.pl_PL.{description, seo_title, seo_description}` → **15/15 desc OK, 15/15 meta OK** (HTTP 200 raw=1, GET
  od ręki potwierdził len>0), zero zwisów. Kolejność priorytet CTR (295/84/66/57 najpierw, wg `_README.md`). **Anty-404
  zneutralizował 0** — partia 3 NIE linkuje do bloga (wszystkie `linki_wewn` to `/pl/c/`); bezpiecznik i tak działał.
  Niezależna weryfikacja GET 3 kat. (295/66/124): niesieroty `<a>`, UTF-8 (ś/ż/ł/–) bez mojibake (zero U+FFFD), seo_title/desc
  zgodne bit-w-bit z plikiem. Skrypty: `category-seo-publish-p3.ps1` (`-DryRun` domyślnie), `category-seo-verify-p3.ps1`.
  **CZĘŚĆ B — meta SEO produktów (`products`) — 2 NOWE USTALENIA NA ŻYWO:**
  (1) **Pola SEO produktu siedzą w `translations.pl_PL`** (jak kategorie, INACZEJ niż `aboutpages`): potwierdzone GET-em —
  `translations.pl_PL` ma `translation_id, product_id, name, short_description, description, active, lang_id, isdefault,`
  **`seo_title, seo_description, seo_keywords`**`, order, main_page, main_page_order, booster, seo_url, permalink`. PUT
  `products/{id}` z `translations.pl_PL.{seo_title, seo_description}` → **HTTP 200 raw=1, ZAPISUJE** (20/20 zweryfikowane
  GET-em bit-w-bit). (2) **⚠️ FILTR PO POLU `code` ZWRACA HTTP 404 (niewspierany na tej instancji)** — `filters={"code":"X"}`,
  `{"code":{"=":"X"}}`, `{"code":{"LIKE":"%X%"}}` **wszystkie → 404** (nie pusta lista!). Filtr `{"translations.name":{"LIKE":"%…%"}}`
  DZIAŁA. **Wzorzec joinu po `code`:** pobierz CAŁY katalog (paginacja `limit=50`, 159 stron / 7938 prod.), zbuduj mapę
  **znormalizowany_code → product_id**. **Normalizacja KRYTYCZNA:** uppercase + usuń `[\s\-_/.,]` — katalog trzyma `code` ze
  **spacjami** (`06MM4933 4646 18`) i **ukośnikami** (`01KLINSPF2/100`, `07BDF5/7016`), a snippety/slugi Mercatum z **myślnikami**
  (`06mm4933-4646-18`) i **podkreślnikami** (`01klinspf2_100`, `07bdf5_7016`). Bez usunięcia `/` 3 produkty fałszywie wypadły
  jako „brak". Match po DOKŁADNYM znormalizowanym code (nie LIKO — np. `07BCMG` vs `07BCMG25` to różne produkty: Mamut 290ml vs 25ml).
  **Wynik B:** 20/21 produktów istnieje i dostało meta; 1 luka = `06mo4932-3525-79` (młotek tytanowy Stiletto — NIE w katalogu,
  potwierdzone: name LIKE %Stiletto% = 0) → do importu. Skrypty: `product-code-map.ps1` (READ-ONLY katalog→mapa,
  zrzut `_rozeznanie/product-code-map.json`), `product-meta-publish.ps1` (`-DryRun` domyślnie), `product-seo-recon*.ps1`,
  `product-missing-check.ps1`. ⚠️ PowerShell 5.1 czyta skrypt UTF-8-bez-BOM jako Windows-1250 → polskie znaki w literałach
  regex się psują; w weryfikatorach używaj kodów Unicode (`[char]0x0105`…), nie literałów PL.
  **CZĘŚĆ C — wpisy #29/#30 do `gotowy` (edycja plików kolejki, BEZ publikacji):** podmieniono `[LINK:]`/placeholdery href na
  realne `<a href="/pl/c/…">` (#29: Srodki-czyszczace/279, Chemia-budowlana/64, Systemy-wentylacyjne/96; #30: Uszczelniacze-dekarskie/75,
  Chemia-budowlana/64, Farby-do-metalu/93 — permalinki potwierdzone z żywego drzewa). Link do nieopublikowanego wpisu #03 (silikon)
  → `<strong>` (anty-404; opublikowane = news_id 8-12). Status `tresc-gotowa`→`gotowy`. Walidacja: JSON OK, 0 surowych `[LINK:`,
  niesieroty `<a>` 3=3, hero+schema.html obecne. Skrypt: `blog-2930-verify.ps1`.
- **Ostatnio zweryfikowano (poprz.):** 2026-06-11 (WDROŻENIE NA ŻYWO za zgodą usera: (1) JSON-LD do 5 opublikowanych wpisów
  + wpięcie schemy w drip-publisher; (2) opisy SEO + meta 15 kategorii). **Dok. `news`/`categories` AKTUALNA, ZERO zmian API**
  — `WebFetch` developers.shoper.pl nadal SPA/login (zgodnie z notatką), `WebSearch` potwierdził strukturę `translations.pl_PL`
  zasobu `categories` bez zmian pól/parametrów.
  **CZĘŚĆ 1 — JSON-LD `BlogPosting+FAQPage+Organization` doklejony do `content` 5 wpisów (news_id 8,9,10,11,12):**
  GET przed zapisem potwierdził, że żaden z 5 NIE miał jeszcze `<script ld+json>` → PUT `news/{id}` z `content`+blok schemy
  na końcu (źródło bloku: `blog/queue/<slug>.schema.html`, gotowy `<script type="application/ld+json">…</script>`; komentarz
  HTML usuwany; fallback: owinięcie gołego `schema_jsonld` z queue JSON). **Wszystkie 5 = HTTP 200, GET potwierdził
  blok bit-w-bit (`@graph` obecny, ZERO encjowania `&lt;script`=False, content kończy się `</script>`, blok 1:1=True).**
  Wzorzec anti-„wiszący zapis" (PUT zwracał `1` od ręki, bez zwisu). **Drip-publisher (`blog-publish.ps1`) wpięty:** nowa
  funkcja `Get-SchemaBlock`/`Add-SchemaToContent` dokleja blok JSON-LD na koniec `content` przy POST `/news` (idempotentnie:
  pomija, gdy content już ma `<script ld+json>`) — w `Build-NewsPayload` (tryb interaktywny) ORAZ w `-DripOne`. Zweryfikowano
  `-DripOne -DryRun`: następny `gotowy` (`03-jaki-silikon-do-lazienki`) → log „SCHEMA: dokleam blok (+8077 zn.)",
  `ma_script_ldjson=True`, `konczy_sie_</script>=True`, content TAIL = `…</script>`; ZERO zapisu.
  **⚠️ Pułapka źródła schemy:** pole `schema_jsonld` w queue JSON to **goły JSON** (bez `<script>`); gotowy blok z `<script>`
  jest w pliku `<slug>.schema.html`. Skrypt bierze `.schema.html` priorytetowo, fallback owija goły JSON — bo goły JSON
  w `<body>` Google NIE sparsuje. Skrypty: `schema-inject-published.ps1` (5 wpisów, `-DryRun` domyślnie),
  `schema-cat-recon.ps1` (READ-ONLY rozeznanie content+schemat kategorii).
  **CZĘŚĆ 2 — opisy SEO 15 kategorii (partia 1):** pole opisu = **`translations.pl_PL.description`** (potwierdzone GET-em
  kat. 61: top-level ma `category_id`/`root`/`order`/`translations`; `translations.pl_PL` ma `description`, `description_bottom`,
  `seo_title`, `seo_description`, `seo_keywords`, `permalink`, `name` itd.). **✅ KLUCZOWE — kategorie ZAPISUJĄ pola SEO przez
  webapi (INACZEJ niż `aboutpages`!):** PUT `categories/{id}` z `translations.pl_PL.{description, seo_title, seo_description}`
  → wszystkie 15 zapisane (GET: `description_len`>0, `seo_title_len`>0, `seo_desc_len`>0). Czyli `seo_title`/`seo_description`
  kategorii są **zapisywalne webapi** (dla `aboutpages` były READ-ONLY — NIE generalizuj polityki SEO między zasobami).
  **Reguła ANTY-404 (z `seo/kategorie/_README.md`):** link `<a href="/pl/news/<slug>">` do wpisu, którego `seo_url` NIE jest
  na żywej liście `news` (GET, active=1: tylko 8-12), → neutralizowany (usuwany `<a>`, zostaje tekst kotwicy); linki do kategorii
  `/pl/c/` i do 5 opublikowanych wpisów zostają. **Zneutralizowano 13 linków** (39:2, 40:1, 44:1, 63:2, 64:3, 77:1, 80:2, 96:1),
  zostawiono 9 do opublikowanych wpisów (61:4, 114:2, 126:2, 149:1). Weryfikacja niezależna GET (kat 64/61/80): `<a>`=`</a>`
  (brak sierot), zero linków do nieopublikowanych, linki kategorii zachowane. Skrypty: `category-seo-publish.ps1`
  (`-DryRun` domyślnie; ANTY-404 + PUT + weryfikacja), `news-published-check.ps1` (READ-ONLY lista żywych `news`),
  `category-seo-verify.ps1` (niezależna weryfikacja 3 kategorii). Front render JSON-LD/meta potwierdzić na produkcji.
- **Ostatnio zweryfikowano (poprz.):** 2026-06-11 (DIAGNOSTYKA: czy `<script type="application/ld+json">` PRZEŻYWA w `news.content`
  — ZA ZGODĄ usera, 1 wpis testowy `active=0`, od razu skasowany). **WERDYKT: TAK — przeżywa 1:1, BEZ sanityzacji.**
  POST `/news` (`content` = `<p>…</p>` + blok `<script ld+json>` z `BlogPosting`) → HTTP 200, `news_id=13`; GET → `content`
  **bit-w-bit identyczny** z wysłanym (163=163 zn.), pełny blok `<script>` zachowany, ZERO encjowania (`&lt;script`=False);
  DELETE → 200, GET → 404, brak sierot. **To ODWROTNIE niż `aboutpages.content`** (tam `<script>` jest WYCINANY) →
  blog ma inną politykę treści niż strony informacyjne. **Wniosek: schemę JSON-LD (BlogPosting+FAQPage) wstrzykuj
  per-post na końcu `news.content` przez webapi** (automatyzowalne, idempotentne); front renderu NIE potwierdzono na żywo
  (TEST blokuje zewn. HTTP) — sprawdzić na produkcji, ale JSON-LD w `<body>` Google parsuje niezależnie od pozycji.
  Dodano sekcję „JSON-LD w `news.content`" + adnotację przy polu `content` w tabeli pól `news`. **Dok. zasobu `news`
  AKTUALNA, zero zmian API** — `WebFetch` developers.shoper.pl/.../resources/news nadal SPA/login (zgodnie z notatką),
  `WebSearch` nie ujawnił publicznej dokumentacji polityki sanityzacji `content` (jedyne wiarygodne źródło = ten test
  empiryczny). Skrypt: `scripts/shoper-api/test-news-script-jsonld.ps1` (zrzut diagnostyczny `_jsonld-news-test.json`).
- **Ostatnio zweryfikowano (poprz.):** 2026-06-11 (domknięcie 16 niezmapowanych produktów mapy 301 + noga CMS — READ-ONLY,
  ZERO zapisu). **Dok. `products`/`aboutpages`/`redirects` AKTUALNA, zero zmian API.** `WebFetch` developers.shoper.pl
  nadal SPA/login (zgodnie z notatką), `WebSearch` potwierdził istnienie zasobu `products` + filtrów/paginacji bez zmian.
  **Potwierdzone na żywo (GET):** (1) filtr `products?filters={"translations.name":{"LIKE":"%…%"}}` ORAZ
  `{"code":{"LIKE":"%…%"}}` ORAZ `{"producer_id":"35",…}` działają (Milwaukee = producer_id **35**); (2) numery
  katalogowe Milwaukee ze slugów Mercatum (np. `4932 4514 86`) **NIE występują** jako `code` w katalogu Shopera →
  join po `code` dla tych 16 niemożliwy, match MUSI iść po nazwie; (3) `aboutpages` count **11** bez zmian (mapa
  id→nazwa zgodna); (4) wiele produktów ze starego sklepu (6 cienkich tarcz Milwaukee, prowadnica 400ml, 3 kleje
  sekundowe 2g) **NIE istnieje** w katalogu Shopera → to LUKI, nie błąd joinu. **Wynik:** 3/16 PEWNY (match po nazwie,
  GET by id), 2/16 AMBIGUOUS rozstrzygnięte (uchwyt bita 1szt id 5297 / 100szt id 8036 — slugi różne, do akceptacji),
  10/16 luka→fallback 301 na kategorię (Tarcze id 63 / Listwy id 190 / Kleje techniczne id 70), 1/16 odrzucony (home).
  CMS: 7/7 starych stron → aboutpages (Regulamin→13, RODO→14, wysyłka→4, formularz-zwrotu→7 [active=0!], o-nas→8,
  kontakt→9, dostawa→4), zero luk; wszystkie `redirect type=4`+`object_id`. Pliki: `migracja/przekierowania/
  coverage-produkty-uzupelnienie.csv`, `coverage-cms.csv`, sekcja „Uzupełnienie 2026-06-11" w `coverage-raport.md`.
  Skrypty (READ-ONLY): `coverage-uzupelnienie-recon.ps1`, `-score.ps1`, `-precyzja.ps1`, `-tarcze.ps1`,
  `-weryfikacja.ps1`, `-katfallback.ps1`. (Aktualne `expires_in` konta = 2592000 / 30 dni.)
- **Ostatnio zweryfikowano (poprz.):** 2026-06-11 (TEST FIDELITY silnika 301 — zasób `redirects`, ZA ZGODĄ usera, 4 reguły
  na koncie TEST `sklep261208`). **Werdykt: silnik 301 Shopera dopasowuje stary format Mercatum z `.html` i strzela
  poprawny 301 — 4× PASS** (R1/R2 produkt type=1 z REAL Mercatum URL .html, R3 kategoria type=2 bez .html,
  R4 kontrolna type=0). Opcja „Przekierowania" WŁĄCZONA (dowód: kontrolna type=0 = 301). `application-config` NIE
  eksponuje flagi włączenia silnika przez webapi → stan potwierdza się regułą kontrolną. Katalog na TEST PEŁNY
  (7938 produktów, 260 kategorii / 9 root, `categories-tree` OK — Leo zsynchronizował). Join po SKU (`code` Shopera ↔
  symbol w slugu Mercatum) działa dosłownie. **Dok. `redirects` zweryfikowana:** `WebFetch` na developers.shoper.pl
  zwraca SPA/login (zgodnie z notatką), `WebSearch` + oficjalny artykuł „Masowy import przekierowań 301 przez API"
  (shoper.pl/learn) potwierdziły pola `type`/`route`/`target`/`object_id`/`lang_id` i wartości type 0-6 — zgodne
  z implementacją. Dodano nową sekcję „Przekierowania 301 — zasób `redirects`". Skrypty:
  `redirect-fidelity-step0-recon.ps1`, `redirect-fidelity-step3-test.ps1`.
- **Ostatnio zweryfikowano (poprz.):** 2026-06-11 (uodpornienie drip-publishera na ciche awarie 07:00 — BEZ publikacji,
  tylko hardening + DryRun; **dok. zasobu `news`/auth aktualna, ZERO zmian API** — `WebFetch` na
  developers.shoper.pl/.../resources/news nadal zwraca samą stronę logowania (SPA, zgodnie z notatką),
  `WebSearch` potwierdził istnienie oficjalnego endpointu `news` bez zmian pól/parametrów; pola
  `name`/`content`/`lang_id` (wymagane POST) + `image`/`image_name`/`categories`/`tags`/`seo_*`/`active`/`start_page`/`date`
  bez zmian względem żywej weryfikacji 2026-06-10)
- **Co zmieniono 2026-06-11 (drip-publisher — odporność na ciche awarie Task Scheduler 07:00, BEZ publikacji):**
  diagnoza: run 07:00 dał exit 1 i NIC nie zalogował (wywalił się WCZEŚNIE — przed logowaniem), ręczny run 07:32
  przeszedł (`news_id=12`). Przyczyna strukturalna: odczyt `.env` (`Get-Content`) i sprawdzenia katalogów były na
  **top-level** pliku, PRZED blokiem `try/catch` trybu `-DripOne` → throw na pliku „tylko w chmurze" (OneDrive Files
  On-Demand) lub transientnym auth = exit 1 bez logu. **Naprawiono w `scripts/shoper-api/blog-publish.ps1`:**
  (1) **ścieżki logów liczone z `$PSScriptRoot` na samej górze** (`_drip-log.txt`, **nowy `_drip-error.txt`**) — znane
  zanim cokolwiek może rzucić; (2) **cały `-DripOne` w jednym `try/catch`** — `Initialize-Env` (odczyt `.env`) i
  `Get-Token` (auth) przeniesione DO try; każdy błąd (też wczesny: `.env`/hero/queue/auth/wyjątek) dopisuje wiersz
  `… | plik=<lub ?> | news_id=- | BLAD: <msg>` do `_drip-log.txt` ORAZ pełny zrzut (data-godzina, `Exception.Message`,
  `ScriptStackTrace`, `InvocationInfo.PositionMessage`) do `_drip-error.txt`; (3) **retry odczytu plików 3× backoff
  2/5/10 s z wymuszoną hydratacją OneDrive** (`[IO.File]::ReadAllBytes` = realny odczyt bajtów „ściąga" plik z chmury)
  dla `.env`, hero `hero-1600x900.jpg`, plików kolejki i `published-log.json`; (4) **retry auth 3× backoff** na
  sieć/5xx/timeout (401/4xx nie ponawiane); (5) **pułapka BOM:** `[Text.Encoding]::UTF8.GetString` NIE usuwa BOM (inaczej
  niż `Get-Content`) → trzeba wyciąć `EF BB BF` przed `ConvertFrom-Json`, inaczej „Nieprawidłowy element pierwotny JSON: .".
  `_drip-error.txt` dodany do `.gitignore`. Idempotencja/bramki (brak hero, surowe `[LINK:`)/kod wyjścia (0 OK/pusto,
  1 błąd) bez zmian. **Zweryfikowano `-DripOne -DryRun`** (read-only GET auth/tags/categories, ZERO zapisu): 19
  kandydatów `gotowy` ASC, następny = `03-jaki-silikon-do-lazienki.json` (06-12, hero 107.5KB, cat=5), exit 0; ścieżka
  błędu potwierdzona empirycznie (catch zapisał oba logi w wymaganym formacie). NIE publikowano.
- **Ostatnio zweryfikowano (poprz.):** 2026-06-10 (przygotowanie fal 2-4 bloga do dripu — podmiana placeholderów `[LINK:]`
  na realne permalinki kategorii/wpisów + status `gotowy` w 15 plikach kolejki; **dok. `categories`/`news` aktualna,
  bez zmian API** — `WebFetch` na developers.shoper.pl nadal zwraca tylko nagłówek+login (SPA, zgodnie z notatką),
  `WebSearch` potwierdził istnienie zasobów `categories`/`languages`/`translations` bez zmian pól/parametrów;
  permalink kategorii `/pl/c/<Nazwa>/<id>` i namespace wpisów `/pl/news/<slug>` potwierdzone żywym zrzutem 260
  kategorii + published-log; zero zmian w API)
- **Co zmieniono 2026-06-10 (fale 2-4 bloga — podmiana linków + status `gotowy`, BEZ publikacji):** w 15 plikach
  `blog/queue/*.json` (04, 08, 09, 11, 13, 14, 15, 16, 17, 18, 19, 20, 22, 25, 28) podmieniono WSZYSTKIE placeholdery
  `[LINK:...]` w `tresc_html` na realne `<a href>` na permalinki kategorii (z żywego zrzutu `_recon-categories-fala1.json`,
  260 kat.) ALBO permalinki OPUBLIKOWANYCH wpisów (#1 wiertarko `/pl/news/jak-wybrac-wiertarko-wkretarke-poradnik-2026`
  w 17/18; szlifierka `/pl/news/jak-wybrac-szlifierke-katowa` w 25). Użyte id kategorii: Elektronarzędzia 61,
  Wentylatory ścienne 106, Systemy wentylacyjne 96, Piany poliuretanowe 77, Chemia budowlana 64, Kleje montażowe 71,
  Farby 65, Materiały ścierne 59, Akcesoria do elektronarzędzi 62, Rękawice robocze 45, Bhp 44, Wkręty 265,
  Technika zamocowań 39, Mieszadła 249, Kratki wentylacyjne 98, Kaski ochronne 192, Uszczelniacze 67,
  Tarcze tnące i ścierne 63 — KAŻDY zweryfikowany krzyżowo wobec zrzutu (zero martwych linków). Linki do
  NIEopublikowanych wpisów-rodzeństwa (silikon #3, kołek #7, tarcza #6, M12/M18 #01b, FUEL #05 oraz wpisy z tej samej
  partii: wentylator #08, klej #11, pianka #09, rękawice #16) → `<strong>` pogrubiony tekst bez linku (unik 404 w
  trakcie rolloutu; published-log = jedyne źródło „opublikowane"). Status `tresc-gotowa`→`gotowy`, `planowana_data`
  rosnąco 2026-06-16..30 z przeplatanymi klastrami (drip ASC). **Zero surowych `[LINK:` w `tresc_html`** (regex
  per-plik + JSON parse OK dla wszystkich 15). Hero każdego potwierdzony (`blog/images/<hero_slug>/hero-1600x900.jpg`);
  **plik 19 nie miał `hero_slug` ani `planowana_data` — DODANO oba** (slug `19-jaka-kratka-wentylacyjna`, inaczej drip
  szukałby hero pod `seo_url` i POMINĄŁBY wpis przez bramkę hero). `blog-publish.ps1 -DripOne -DryRun` potwierdził:
  20 kandydatów `gotowy` ASC (5 fali 1 + 15 tych), następny = `01b-milwaukee-m12-czy-m18.json` (06-11), ZERO zapisu.
  NIE publikowano — to robi scheduler 07:00.
- **Ostatnio zweryfikowano (poprz.):** 2026-06-10 (przygotowanie fali 1 bloga do dripu — podmiana placeholderów `[LINK:]` na realne permalinki kategorii + status `gotowy` w 5 plikach kolejki; **dok. `categories`/`news` aktualna, bez zmian API** — `WebFetch` na developers.shoper.pl zwraca samo menu (SPA, zgodnie z notatką), `WebSearch` potwierdził istnienie zasobów `categories` + `categories-tree` bez zmian pól/parametrów; permalink kategorii nadal w `translations.pl_PL.permalink`, schemat `/pl/c/<Nazwa>/<id>` potwierdzony na żywo — GET 260 kategorii)
- **Co zmieniono 2026-06-10 (fala 1 bloga — podmiana linków + status `gotowy`, BEZ publikacji):** w 5 plikach `blog/queue/*.json`
  (01b M12/M18, 03 silikon, 05 FUEL, 06 tarcza, 07 kołek) podmieniono wszystkie placeholdery `[LINK:...]` w `tresc_html` na realne
  `<a href>` na permalinki kategorii produktowych z żywego GET `categories` (Elektronarzędzia 61, Silikony 80, Chemia budowlana 64,
  Piany poliuretanowe 77, Akcesoria do elektronarzędzi 62, Tarcze tnące i ścierne 63, Kołki rozporowe 40, Technika zamocowań 39)
  oraz na permalinki OPUBLIKOWANYCH wpisów (#1 wiertarko-wkrętarka news_id=8 `/pl/news/jak-wybrac-wiertarko-wkretarke-poradnik-2026`,
  szlifierka news_id=9 `/pl/news/jak-wybrac-szlifierke-katowa`). Linki do NIEopublikowanych wpisów (M12/M18, FUEL wzajemnie, wkręty
  do drewna #17) → pogrubiony tekst bez linku / zdanie bez odnośnika (unik 404 w trakcie rolloutu). Status `tresc-gotowa`→`gotowy`,
  `planowana_data` rosnąco 2026-06-11..15 (drip ASC). **Zero surowych `[LINK:` w `tresc_html`** (regex per-plik + JSON parse OK).
  Hero każdego potwierdzony (`blog/images/<hero_slug>/hero-1600x900.jpg`). `blog-publish.ps1 -DripOne -DryRun` potwierdził: 5
  kandydatów `gotowy` ASC, następny = `01b-milwaukee-m12-czy-m18.json` (hero 174 KB, cat=5, 4 tagi), ZERO zapisu. Rozeznanie
  kategorii: `scripts/shoper-api/recon-categories-blog-fala1.ps1` (TYLKO GET) → zrzut `_recon-categories-fala1.json`. NIE
  publikowano — to robi scheduler.
- **Co zmieniono 2026-06-10 (drip-publisher 1 wpis/dzień — BEZ realnej publikacji, tylko DryRun + harmonogram):** dodano
  tryb **`-DripOne`** do `scripts/shoper-api/blog-publish.ps1` (Windows Task Scheduler, codziennie 07:00, nienadzorowany,
  zadanie „PLASMET-Blog-Drip"). Bierze NASTĘPNY wpis `status='gotowy'` z `blog/queue/*.json` wg `planowana_data` ASC
  (przy równych: nazwa pliku ASC), publikuje pełnie (POST `/news` z `image` base64 + `image_name`, `categories:[id]`,
  tagi find-or-create z paginacją, `active=1`, `start_page`, `seo_*`), oznacza `opublikowany`, dopisuje `news_id`+permalink,
  `blog/published-log.json` ORAZ wiersz do `scripts/shoper-api/_drip-log.txt`. **Wzorzec zapisu = zweryfikowany
  anti-„wiszący zapis"** (`HttpWebRequest`+`.Timeout`+`.ReadWriteTimeout`+`.KeepAlive=$false`, deadline 45 s) z idempotencją
  po `name` (GET listy po HANG/TIMEOUT). **Bramki:** surowe `[LINK:...]` w treści → NIE publikuje, pomija (następny gotowy);
  brak pliku hero `blog/images/<slug>/hero-1600x900.(jpg|png|webp)` → NIE publikuje, pomija. **Brak `gotowy`** →
  log „BRAK wpisów gotowych" + exit 0 (nie błąd). Tryb domyślny `-DryRun:$true`; LIVE = `-DryRun:$false`. Bez Gemini/
  ImageMagick (publikuje gotowe hero, nie generuje). **Zweryfikowano DryRun** (read-only GET-y auth/tags/categories,
  zero zapisów): (1) pusty stan kolejki → „BRAK wpisów gotowych" exit 0; (2) sortowanie `planowana_data` ASC poprawne;
  (3) bramka surowe `[LINK:]` pomija; (4) bramka brak hero pomija; (5) pełny payload zbudowany dla wpisu z realnym hero
  (139.5 KB, `categories=[5]`, tagi reużyte 13/11). **Dok. zasobu `news` bez zmian** — mechanizm tożsamy z publikacją
  klastra B. Uwaga operacyjna: na 2026-06-10 żywa kolejka ma **0** wpisów `gotowy` (5 ma pośredni status `tresc-gotowa`,
  który drip celowo POMIJA) — drip działa, ale do publikacji trzeba najpierw przestawić status na `gotowy` (po hero +
  podmianie `[LINK:]`).
- **Co zmieniono 2026-06-10 (ZAPIS nazw producentów — PUT `producers/{id}` DZIAŁA):** (poprzedni wpis — bez zmian poniżej)
- **Co zmieniono 2026-06-10 (ZAPIS nazw producentów: KRS → marka handlowa, za zgodą usera — 8× PUT):** zmieniono
  nazwy 8 producentów z pełnych nazw firmowych KRS na czytelne marki handlowe pod H1/`<title>`/permalink stron marek
  linkowanych ze strony głównej. **POTWIERDZONO NA ŻYWO:** `PUT /webapi/rest/producers/{id}` **DZIAŁA** (HTTP 200,
  body `1`) — żadnego 501 (inaczej niż `application-config`); konto webapi PLASMET ma uprawnienie edycji producentów.
  **Mechanizm permalinku:** wystarczy zmienić top-level `name` → **Shoper auto-generuje nowy `translations.pl_PL.permalink`**
  (np. `BAUM`→`Baum` dał `/pl_PL/producer/Baum/26`); `seo_url` zostawiony pusty (auto). Wysyłany payload:
  `{name:<marka>, translations:{pl_PL:{name:<marka>}}}`. **Pole `name` NIE jest zwracane w `translations.pl_PL` przy GET**
  (GET zwraca tam tylko `seo_*`, `permalink`, `description`) — wyświetlana nazwa producenta to **top-level `name`**, z niego
  liczy się permalink. Zmienione (id→marka→nowy permalink): 35→Milwaukee `/producer/Milwaukee/35`, 30→Bostik
  `/producer/Bostik/30`, 26→Baum `/producer/Baum/26`, 34→Awenta `/producer/Awenta/34`, 36→Richmann `/producer/Richmann/36`,
  40→Collomix `/producer/Collomix/40`, 29→Klingspor `/producer/Klingspor/29`, 33→Polifarb Kalisz `/producer/Polifarb-Kalisz/33`.
  **⚠️ producent 37 NIE zmieniony (wstrzymane):** „SCHED-POL-SH PPHU Stefan Schaedler" miał być „Schedpol", ale GET produktów
  (`filters={"producer_id":"37"}`, 84 szt.) ujawnił, że to **wyłącznie poziomnice i kątownice budowlane marki „SL" (SOLA)**,
  NIE brodziki/prefabrykaty Schedpol → tożsamość obalona, czeka na decyzję usera. **Pozostali producenci (CONKRET, BUD-MET,
  Klimas, STOMIL SANOK, MASTERPLAST, EUBRIDGE, SEMIRAMIDA, PGD POLSKA, MOSCO, KLIMAS WKRĘT-MET) NIE ruszani** (czekają na
  decyzję). Wzorzec zapisu = anti-„wiszący zapis" (`HttpWebRequest`+`.Timeout`+`.ReadWriteTimeout`+`.KeepAlive=$false`),
  throttling 700-800 ms, idempotencja (pomija PUT gdy `name` już == cel), backup surowego rekordu per producent przed PUT.
  Skrypt: `scripts/shoper-api/producers-rename.ps1` (`-DryRun` domyślnie / `-Live` / `-OnlyId <id>`); backupy:
  `scripts/shoper-api/backup/producer-<id>_backup_2026-06-10.json`; wynik: `_producers-rename-result.json`. Nowe permalinki
  przekazane do podmiany linków kafli marek na stronie głównej (uniknięcie 301).
- **Co zmieniono 2026-06-10 (auto-publikacja klastra B bloga, za zgodą usera — `news_id` 9/10/11):** opublikowano
  3 wpisy poradnikowe (szlifierka kątowa=9, młotowiertarka=10, pilarka=11) jednym POST `/news` każdy, z głównym
  zdjęciem w polu `image` (base64 hero-1600x900.jpg) + `image_name` (alt), `categories:[5]` (Poradnik) i `tags[]`
  w tym samym POST — **HTTP 200, raw=`9`/`10`/`11`**, bez fallbackowego PUT. **Potwierdza w pełni dotychczasowy
  mechanizm `news`** (zero rozbieżności): (1) `image`+`image_name`+`categories`+`tags` w jednym POST działają;
  (2) twardy test PUT `image_name` SOLO → 200 dla wszystkich 3 (obraz fizycznie obecny); (3) filtr
  `{"category_id":"5"}` zwrócił 8,9,10,11; (4) paginacja `news-tags` istotna — find-or-create utworzył nowe tagi
  `szlifierki kątowe`(15), `młotowiertarki`(16), `SDS-Plus`(17), `pilarki`(18), reużył 11-14; (5) wzorzec
  anty-„wiszący zapis" (`HttpWebRequest`+`.Timeout`+`.ReadWriteTimeout`+`.KeepAlive=$false`, deadline 40 s)
  domknął każdy POST i zwrócił nowe `news_id`. **Podmiana linków wewnętrznych:** placeholdery `[LINK:...]` →
  realne `<a href>` na permalinki kategorii produktowych (Szlifierki kątowe id=126, Młotowiertarki id=149,
  Piły i pilarki id=112, Narzędzia ogrodowe id=116, Elektronarzędzia id=61) i permalink wpisu #1 (news_id=8);
  link do nieopublikowanego rodzeństwa (#6 „tarcza do cięcia") zamieniony na pogrubiony tekst bez linku. **Zero
  surowych `[LINK:` w opublikowanej treści** (zweryfikowane GET-em na żywym serwerze). **Dok. zasobu `news`
  pozostaje aktualna — żadnych zmian pól/parametrów API.** Skrypty: `blogB-recon.ps1` (TYLKO GET: drzewo
  kategorii + tagi + idempotencja), `blogB-publish.ps1` (publikacja, `-DryRun` domyślnie / `-Live`), mapa
  podmian linków `_blogB-linkmap.json`, `blogB-verify.ps1` (niezależna weryfikacja GET), `blogB-update-queue-log.ps1`
  + `blogB-fix-log.ps1` (aktualizacja queue/log). Front render potwierdzić w panelu/na produkcji.
- **Co zmieniono 2026-06-10 (PRZEŁOM `aboutpages` + publikacja „O firmie" page 8, za zgodą usera, staging):**
  Ustalono, że **strony informacyjne CMS to zasób `aboutpages` (NIE `pages`)** — `pages` w webapi nie istnieje,
  całe wcześniejsze „Missing MODULE 'pages'" było **pomyłką nazwy**, nie brakiem uprawnień (uprawnienie
  „Zawartość" pełne). `GET aboutpages?limit=1` → 200, `count=11`; `aboutpages/8` = „O firmie". **Backup pełnego
  surowego rekordu zrobiony** (`backup/o-firmie-page-8_backup_2026-06-10.json`) — nadpisał stary placeholder
  z zablokowanego `pages`. **Rozpoznanie pól:** rekord PŁASKI (jak `news`): `page_id`, `name`, `content`,
  `lang_id`, `active`, `seo_title`, `seo_description`, `seo_keywords`, `seo_url`. **Zapis (PUT, 200/`1`) —
  wynik częściowy:** (1) **`content` zapisał się** — finalny BODY HTML „O firmie" (4×`<h2>`: Marki i autoryzacje,
  Dla kogo pracujemy, Nasza misja, Cel i rozwój) JEST na żywo, UTF-8 bez mojibake (potwierdzone GET-em rekordu
  ORAZ żywym frontem `/pl/i/O-firmie/8`). (2) **`<script>` JSON-LD WYCINANY z `content`** (sanityzacja serwera —
  potwierdzone sondą: script z type i bez type oba usuwane) → **nasz blok Store+AboutPage NIE przetrwał** (front
  ma tylko natywne 6 bloków motywu). (3) **`seo_title`/`seo_description`/`seo_keywords` NIEZAPISYWALNE przez webapi**
  — 5 wariantów (płasko / `translations.pl_PL` / `lang_id` / `seo:{}` / `meta_*` / `title/desc/keywords`), wszystkie
  200, żaden nie zapisał; `seo_url` natomiast ZAPISYWALNY (potwierdzone markerem, przywrócony do `null`). **Skutek:**
  `<title>` nadal „O firmie - PLASMET sp. z o.o" (fallback `name`+sufiks sklepu), meta desc „O firmie", keywords
  „O firmie,  sklep" — **bez zmian, bo pól SEO nie da się ruszyć webapi**. **Do ręcznego dokończenia w PANELU**
  (Wygląd i treści > Strony informacyjne > „O firmie" > SEO): meta title (cel render ~„O firmie – PLASMET Kalisz,
  od 1979 | Sklep techniczny", uważać na podwójną markę z sufiksem), meta description (sekcja 2 FINAL), keywords
  wyczyścić; JSON-LD wkleić w trybie źródła HTML lub w `<head>` motywu/`shoper-cli` (NIE przez webapi `content`).
  Skrypty: `aboutpages-recon-backup.ps1`, `build-payload.py`, `write-aboutpages-8.ps1`, `restore-final-content.ps1`,
  `diag-seo-fields.ps1`, `diag-aboutpages-seofields.ps1`, `diag-seo-variants.ps1`, `diag-jsonld-content.ps1`,
  `check-frontend-jsonld.ps1`, `fetch-front-before.ps1`, `reset-seourl-null.ps1`. Front stagingu odpowiada na HTTP
  (weryfikacja renderu bez panelu możliwa), cache odświeżał się natychmiast.
- **Co zmieniono 2026-06-10 (republikacja wpisu #1 od zera, za zgodą usera — `news_id=8`):** user usunął stary
  `news_id=7` i zlecił dodanie CAŁEGO wpisu od zera OD RAZU z głównym zdjęciem w polu `image` (base64), NIE
  `news-files`. **Potwierdzono na żywo, że `image` ORAZ `image_name` przechodzą w JEDNYM POST `/news`** (nie tylko
  osobnym PUT): POST z payloadem `{name, content, short_content, lang_id, active=1, start_page=1, seo_*, author,
  image=<base64 hero-1600x900.jpg>, image_name=<alt>, categories:[5], tags:[10..14]}` → **HTTP 200, raw=`8`**
  (nowe `news_id`), bez potrzeby fallbackowego PUT. **Weryfikacja:** GET `news/8` → `image_name` niepuste (alt),
  `active=1`, `start_page=1`, `tags=10,11,12,13,14`; twardy test PUT `image_name` SOLO → **HTTP 200** (= obraz
  fizycznie obecny, zgodne ze wzorcem demo); kategoria „Poradnik" (id 5) powiązana przez `categories:[5]` w POST
  (filtr `{"category_id":"5"}` zwrócił `news_id=8`). **Idempotencja zadziałała:** rozeznanie GET przed zapisem
  potwierdziło, że kategoria id=5 i tagi id 10-14 już istniały (reużyte, zero duplikatów), a wpis o tytule nie
  istniał (user faktycznie usunął #7). Skrypty: `republish-01-recon.ps1` (TYLKO GET — idempotencja/kategoria/tagi),
  `republish-01.ps1` (publikacja jednym POST z hero + fallback PUT + twardy test obecności obrazu). Front URL
  deterministyczny z `seo_url` (TEST `blog_use_new_url_namespace=0`, stary namespace `news`); `permalink` w GET puste.
- **Co zmieniono 2026-06-10 (publikacja „O firmie" page 8 — ZABLOKOWANE, uprawnienie `pages` nie weszło):**
  user zadeklarował nadanie grupie webapi uprawnienia „strony CMS", po czym zlecono publikację gotowej
  treści. **Weryfikacja na żywo (świeży token login+hasło, `SHOPER_TOKEN` puste → zakres zawsze aktualny):**
  `GET /webapi/rest/pages?limit=1` ORAZ `GET /webapi/rest/pages/8` → **HTTP 400 `Missing MODULE 'pages'`**
  (bez zmian względem stanu sprzed deklaracji). **Izolacja problemu (diagnostyka, ten sam token):**
  `GET /news?limit=1` → HTTP 200 (count 5), `GET /products?limit=1` → HTTP 200 (count 2303) → **auth jest
  OK, problem to WYŁĄCZNIE uprawnienie modułu `pages`.** Wykluczono pułapkę „stary token z zamrożonym
  zakresem" — auth idzie świeżym `POST /auth`, nie tokenem permanentnym. **Wniosek:** uprawnienie „strony
  CMS" albo (a) nie zapisano dla **właściwej grupy/konta** webapi z `.env`, albo (b) wymaga aktywacji
  **modułu** „Strony informacyjne", nie tylko checkboxa uprawnień, albo (c) propaguje z opóźnieniem.
  **Backup page 8 NIE powstał** (brak odczytu). Skrypty: `pages-recon-and-backup.ps1` (KROK 1-3:
  weryfikacja+backup+rozpoznanie pól, zatrzymuje się na Missing MODULE), `pages-access-diag.ps1`
  (izolacja: `pages` vs `news`/`products` tym samym tokenem). **Do usera:** potwierdzić, że uprawnienie
  nadano grupie administratora powiązanej z loginem z `.env` (nie inną), oraz że moduł CMS jest aktywny.
- **Co zmieniono 2026-06-10 (KOREKTA hero wpisu bloga — pole `image`, za zgodą usera, naprawa news_id=7):**
  Wcześniejsza notatka „hero = pierwszy plik `news-files` (`order=0`)” okazała się **BŁĘDNA** (plik w `news-files`
  NIE renderował się na froncie — pusty slot). **Reverse-engineering na żywych danych** (skrypty
  `diag-news-mainimage.ps1`, `diag-news-imgsource.ps1`, `diag-news-image-put-probe.ps1`, `test-news-image-confirm.ps1`):
  (1) wpisy demo 2–5 mają `image_name`=tytuł i **ZERO** rekordów w `news-files`, a renderują obraz → obraz NIE jest
  w `news-files`. (2) Wszystkie alternatywne zasoby (`news-image`/`news-gfx`/`news-main`/…) → „Missing MODULE”.
  (3) PUT `image_name` SOLO bez obrazu → **400 „must first add image”** → `image_name` to ALT, a obraz idzie osobnym
  polem. (4) PUT `news/{id}` `{image:<base64>}` → 200; **dowód krzyżowy**: po nim PUT `image_name` SOLO → 200 (przed
  → 400), data-URI w `image` → „Cannot decode the contents of the file” (czyli `image` realnie parsuje binarkę).
  **WERDYKT: główne zdjęcie wpisu = pole `image` (base64) na obiekcie `news`; `image_name` = jego alt (zapisywalny
  tylko gdy obraz istnieje).** Naprawa: PUT `news/7` `{image=hero-1600x900.jpg(base64), image_name=alt}` → 200,
  `image_name` zapisane (potwierdza obecność obrazu); błędny `news-files/4` usunięty (`news-files count` 1→0).
  Weryfikacja bez frontu: stan pól #7 == wzorzec demo + twardy test PUT `image_name` SOLO → 200. Skrypty:
  `news-hero-upload.ps1` (przepisany na pole `image`), `verify-and-cleanup-hero.ps1`. Render pikseli potwierdzi user
  w panelu/na produkcji (front TEST odrzuca zewnętrzne HTTP).
- **Co zmieniono 2026-06-10 (kategorie + producenci pod linki strony głównej — TYLKO ODCZYT):** pobrano na żywo
  z konta PLASMET (`sklep261208`) pełne kolekcje: **`categories` = 260** (paginacja `limit=50`), **`categories-tree`**
  (hierarchia → mapa `parent_id`, bo płaski `categories` GET nie ma `parent_id`), **`producers` = 19**. Potwierdzono
  wzorce URL z `translations.pl_PL.permalink`: kategoria `/pl/c/Nazwa/ID` (płaska), producent `/pl_PL/producer/Nazwa/ID`.
  **Dok. zasobów `categories`/`producers` aktualna** (zgodna z oficjalną, bez zmian pól/parametrów). Producenci to
  **pełne nazwy firm z KRS, nie marki handlowe** (np. Milwaukee = `producer_id 35` „TECHTRONIC INDUSTRIES…"; Wkręt-met
  = 41 „KLIMAS WKRĘT-MET…"; brak osobnych wpisów dla marek Den Braven, Plasmet, Schedpol). **Strona kontaktowa:**
  natywny formularz Storefront pod stałym URL `/pl/contact` (potwierdzone wyszukiwarką na demo/innych instancjach);
  zasób CMS `pages` (gdzie żyłaby ewent. strona „Kontakt i dane firmy" `/pl/i/…`) **NADAL `Missing MODULE 'pages'`**
  → przez webapi nieczytelny. Skrypty (read-only): `fetch-cat-prod-readonly.ps1`, `probe-contact-readonly.ps1`;
  zrzuty: `_rozeznanie/LIVE-categories-all.json`, `LIVE-categories-tree.json`, `LIVE-producers-all.json`.
- **Co zmieniono 2026-06-10 (strony CMS `pages` / „O firmie" page 8 — TYLKO ODCZYT):** próba rozeznania+backupu
  strony informacyjnej „O firmie" (`/pl/i/O-firmie/8`) pod planowaną aktualizację treści/SEO. **Potwierdzono
  ponownie blokadę:** `pages` (lista i `pages/8`) → HTTP 400 „Missing MODULE 'pages'"; warianty nazwy
  (`cms-pages`/`page`/`cms`/`information-pages`/`static-pages`/`content-pages`) też „Missing MODULE";
  `news/8` → 404 i lista `news` bez „O firmie" → wykluczono pomyłkę zasobu (to strona CMS `pages`, nie blog).
  OPTIONS `pages` → 400 (brak wsparcia OPTIONS → uprawnień zapisu nie potwierdzono bezpiecznie). **Backup
  rekordu NIE powstał** (brak dostępu do odczytu). **Akcja po stronie usera:** nadać grupie webapi „API"
  uprawnienie „strony CMS" (panel) — wtedy GET/PUT `pages` ruszą. Skrypty: `rozeznanie-pages-readonly.ps1`
  (sonda zasobu + paginacja + backup + OPTIONS), `rozeznanie-pages-diag.ps1` (pełne body błędu + wykluczenie `news`).
- **Co zmieniono 2026-06-10 (zdjęcie hero wpisu — `news-files`, za zgodą usera):** ustalono i potwierdzono na
  żywo (news_id=7, upload→odczyt→DELETE, sklep czysty) **DZIAŁAJĄCY, automatyzowalny mechanizm osadzania
  grafiki hero**: **POST `/webapi/rest/news-files` z `{news_id, name, content(base64), [description], [order]}`**.
  Kluczowe: (1) `content` = **base64 binarki pliku, NIE URL** (zły content → „Cannot decode the contents of the
  file”); `news_id`+`name`+`content` wymagane. (2) `news-files` to **galeria** wpisu — hero/miniatura = pierwszy
  plik (`order=0`); obiekt `news` NIE ma własnego pola obrazu (`main`/`image` w PUT ignorowane), `image_name`
  niezapisywalne czystym PUT. (3) Sondą rozróżniono: `news-images`/`gfx`/`files`/`media`/`attachments` =
  „Missing MODULE”; `news/{id}/images` = **echo wpisu (pułapka)**, nie sub-zasób. (4) Rekord ma `file_name`
  (hash pliku na dysku) → bazę URL publicznego (prefiks do potwierdzenia na produkcji; dla hero URL niepotrzebny,
  motyw renderuje z galerii). Skrypt produkcyjny: `news-hero-upload.ps1` (DryRun, idempotentny, wzorzec
  anty-„wiszący zapis”). Rozeznanie: `rozeznanie-news-image.ps1`, `rozeznanie-news-files-schema.ps1`,
  `rozeznanie-news-files-content.ps1`, `test-news-files-upload.ps1`, `test-news-hero-link.ps1`,
  `test-news-gallery-render.ps1`. Czego brakuje do realnego podpięcia pod news_id=7: **pliku hero od
  graphic-designera** (`blog/images/01-jak-wybrac-wiertarko-wkretarke/hero-1600x900.jpg|webp`, jeszcze niewygenerowany).
- **Co zmieniono 2026-06-10 (realna publikacja wpisu #1, za zgodą usera):** opublikowano pierwszy wpis bloga
  (`news_id=7`, `active=1`, `start_page=1`) przez POST `/news`. **Ustalono na żywo 3 rzeczy:** (1) **wiązanie
  kategorii bloga DZIAŁA przez `categories:[id]` (l. mnoga)** w POST — potwierdzone filtrem (kat. 5 „Poradnik"
  zawiera wpis 7); to domyka otwartą kwestię ze smoke-testu (`category_id` l. poj. nie wiązał). (2) **Wzorzec
  zapisu odporny na „wiszący zapis": `System.Net.HttpWebRequest` z `.Timeout`+`.ReadWriteTimeout`+`.KeepAlive=$false`**
  — jedyne z trzech podejść, które nie wisi (Invoke-WebRequest -TimeoutSec zawiódł, Start-Job → deadlock).
  (3) **Pułapka paginacji `news-tags`**: `page=1` przy `limit=100` zwraca tylko ~10 z 14 → find-or-create musi
  paginować po `pages`, inaczej nie znajdzie świeżych tagów (fałszywe „NIE utworzono"/ERR:400 na duplikacie).
  5 tagów (id 10-14) utworzono i powiązano (PUT `tags:[…]` nadpisuje zestaw). Skrypty: `blog-publish-01.ps1`,
  `finalize-tags-01.ps1`, `blog-prepublish-recon.ps1`, `verify-final-01.ps1`. Pole `permalink` w GET puste
  (TEST `blog_use_new_url_namespace=0`); front URL deterministyczny z `seo_url`.
- **Co zmieniono 2026-06-10 (smoke-test zapisu `news`, za zgodą usera):** wykonano kontrolowany 1-wpis
  (szkic `active=0`, od razu skasowany). **Potwierdzono na żywo:** (1) **ZAPIS `news` DZIAŁA** — POST
  utworzył `news_id=6`, DELETE go usunął (count 4→5→4), brak „Missing MODULE"/403; konto webapi ma
  uprawnienie tworzenia/usuwania aktualności. (2) **`category_id` w POST NIE wiąże** wpisu z kategorią
  (filtr kat. 4 nie pokazał nowego wpisu) → mechanizm relacji kategorii do ustalenia osobno. (3) Odkryto
  **pułapkę „wiszący zapis"**: POST/DELETE na hoście PLASMET nie domykają połączenia (klient wisi mimo
  `-TimeoutSec`), ale operacja wykonuje się serwerowo → weryfikować efekt osobnym GET listy, nie polegać
  na odczycie body zapisu (idempotencja po `name`). Skrypty: `smoke-test-news.ps1`, `verify-and-cleanup-news.ps1`,
  `check-news-orphan.ps1`. Sklep posprzątany (zero wpisów testowych).
- **Co zmieniono 2026-06-10 (blog/`news`):** dodano sekcję „Blog / aktualności — zasób `news`". Na żywych
  4 wpisach udokumentowano REALNE pola wpisu (`name`, `content`, `short_content`, `date`, `author`,
  `start_page`, `seo_title/description/keywords/url`, `image_name`, `active`, `box`, `tags[]`, `lang_id`,
  `order`) — w obiekcie GET **brak `category_id`**, relacja wpis↔kategoria filtrowana
  (`filters={"category_id":N}`, potwierdzone). Zasoby `news-categories` (płaskie, 2 kat.) i `news-tags`
  (`tag_id`,`name`,`lang_id`, 9 tagów) istnieją i są czytelne. Ustalono z `application-config` flagi URL
  bloga (`blog_use_new_url_namespace=0`, `blog_news_default_url_format=1`, `blog_items_per_page=20`) i
  wzorzec permalinku `/:lang/blog/:newsName/:newsId` (oficjalny Shoper Learn). **UWAGA dot. zapisu:**
  minimalny payload POST `/news` = `name`+`content`+`lang_id` (oficjalna dok.) — `news` **NIE** zgłasza
  „Missing MODULE" (inaczej niż `pages`); realny POST testowy nie wykonany (czeka na zgodę usera).
  Front instancji TEST odrzuca zewnętrzne HTTP → render URL potwierdzić na produkcji.
- **Co zmieniono 2026-06-08 (konfiguracja/SEO home):** dodano sekcję „Konfiguracja sklepu / SEO home".
  Odkryto i udokumentowano zasób **`application-config`** (GET → pojedynczy obiekt; pełna lista pól danych
  firmy `shop_*`). Ustalono na żywo, że **`application-config` jest READ-ONLY** (PUT/POST → **HTTP 501**),
  więc danych firmy/`shop_name` nie da się zapisać przez webapi — tylko panel (Ustawienia > Dane sklepu).
  Potwierdzono brak webapi-owych pól meta title/description home (panel: Ustawienia > Zaawansowane > SEO) i
  brak API do własnego kodu w `<head>` (panel: Dodatki i integracje > Integracje własne > Nagłówek `<head>`).
  Próby zasobów `config/option/options/configuration/shop/metafields/seo` → HTTP 400.
- **Co zmieniono 2026-06-08 (rozeznanie konta):** potwierdzono **na żywych danych** wzorce URL
  (produkt `/pl/p/Nazwa/ID`, kategoria `/pl/c/Nazwa/ID` płaski, producent `/pl_PL/producer/Nazwa/ID`)
  z pola `translations.pl_PL.permalink`; udokumentowano realny schemat produktu (ceny w `stock`,
  `tax_id`, `code`=SKU, `ean` puste, `weight` w `stock.weight`); odkryto zasób `categories-tree`
  (hierarchia); odnotowano `expires_in: 2592000` (30 dni) na koncie PLASMET; opisano błąd
  `"Missing MODULE 'pages'"` (CMS bez uprawnienia webapi); poprawiono uwagę o paginacji `pages`/`limit`.
- **Co zmieniono 2026-06-08 (wcześniej):** dodano sekcję o **tokenie permanentnym** (panel: Aplikacje
  i integracje > Aplikacje zewnętrzne; token nie wygasa, granularne uprawnienia, odwoływalny) —
  alternatywa dla bearer; stary przepływ login+hasło nadal działa. Rdzeń auth/URL/zasobów bez zmian.
- **Rdzeń auth/URL/odpowiedzi:** potwierdzony skryptem `scripts/shoper-api/connect-test.ps1` (działa).
  Potwierdzony też wyszukiwarką: `/webapi/rest/auth` → bearer, `expires_in: 3600`, `/webapi/rest/products`,
  zasób `redirects` obecny w oficjalnej dok. (developers.shoper.pl/.../resources/redirects).
- **Źródło dokumentacji:** developers.shoper.pl (SPA — `WebFetch` zwraca samo menu; szczegóły pól
  endpointów potwierdzać na żywo `WebSearch`/przy pierwszym realnym użyciu konkretnego zasobu).
- **Token:** ważny 3600 s (tymczasowy, zapis do `.token.json`) **lub** permanentny z panelu (nie wygasa).
