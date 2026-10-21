# Format kolejki wpisów bloga MindSync (pipeline „partia + drip")

Każdy wpis bloga = **jeden plik JSON** w `blog/queue/`. Stack generujący wpisy zrzuca tu całe
partie; `scripts/webflow/blog-publish.ps1` (drip, Task Scheduler 07:00) bierze **najstarszy**
wpis o statusie `gotowy` z `planowana_data <= dziś` i publikuje go do kolekcji **Blog Posts**
na Webflow (wpis ląduje pod `https://mindsync.app/journal/<slug>`, listing na `/blog`).

**Treść wpisów po ANGIELSKU.** Nazwy pól kolejki zostają polskie (ciągłość narzędzi:
`blog-queue-gate.py`, `blog-tbd-*.py`, drip). Kadencja dripu: **1 wpis dziennie** (decyzja
operatora 2026-08-25).

## ⛔ KROK 0: BRAMKA POKRYCIA FUNKCJAMI — PRZED pisaniem, nie po (zasada twarda)

**Kolejność jest nieodwracalna: najpierw sprawdzamy, czy MindSync ma funkcję/ekran/plan,
do którego wpis może uczciwie prowadzić. Potem powstaje treść.**

Powód jest kosztowy, nie teoretyczny (lekcja PLASMET, partia D: bramka robiona równolegle
z pisaniem = 8 z 10 wpisów do przepisania).

**Procedura obowiązkowa:**

1. `seo-content-writer` proponuje tematy partii z danych (GSC gdy są; na starcie research
   konkurencji + frazownik – patrz „Źródło tematów" niżej).
2. **Bramka pokrycia na liście tematów, zanim powstanie brief:**
   `python scripts/blog-coverage-preflight.py --temat blog/queue/_preflight-<partia>.json`
   (plik tematów: `{ "temat": ["keyword EN", ...] }`). Katalog funkcji: `blog/app-features.json`
   (utrzymywany ręcznie; statusy live/beta/planned).
   Werdykty: **OK** (≥1 funkcja live) · **RYZYKO** (tylko beta/planned albo tylko strona
   zbiorcza) · **BRAK** (0 trafień).
3. **Temat z werdyktem BRAK nie idzie do pisania w tej formie.** Trzy wyjścia:
   (a) zmiana kąta na taki, który obsłużą istniejące funkcje;
   (b) temat zostaje, ale **z góry** planujemy sekcję bez karty, z linkiem do strony zbiorczej
       (`/features`), i nigdzie nie sugerujemy funkcji, której nie ma;
   (c) temat wypada i wraca, gdy funkcja powstanie.
   Każdy brak → `docs/luki-funkcji.md` (sygnał produktowy z liczbą z GSC).
4. Dopiero teraz: dyrektywy frazowe → briefy → pisanie → humanizer → akcept brand-voice →
   karty → schema → publikacja.

**Zasada nadrzędna:** wpis NIGDY nie prowadzi w ślepy zaułek. Brak idealnego celu = cel
pochodny (inna funkcja) albo strona zbiorcza. Nigdy donikąd.

**Źródło tematów (dane, nie burza mózgów):** przed KAŻDĄ partią uruchom skrypty GSC
(READ-ONLY, właściwość mindsync.app – patrz `scripts/gsc/`):
1. `scripts/gsc/blog-tematy.py` – wpisy do WZMOCNIENIA (pozycje 4-20), LUKI tematyczne,
   frazy rankingowe.
2. `scripts/gsc/blog-partia-frazy.py` – **frazy pod JUŻ WYBRANE tematy**: dosłowne zapytania,
   pozycje, kontrola kanibalizacji (nasz wpis w top 15 = linkujemy, nie dublujemy).
   Wynik → plik dyrektyw w kolejce (wzorzec formatu: referencja PLASMET).
Zasada: **fraza główna briefu = realne zapytanie z GSC** (z liczbą wyświetleń). Póki danych
mało (świeża właściwość), tematy z researchu konkurencji (Ahrefs/skille seo-*) – ale struktura
partii i bramka KROK 0 obowiązują tak samo. **Pytania FAQ przepisuj DOSŁOWNIE z realnych
zapytań**, nie parafrazuj.

Każdy tekst prozą przechodzi przez skill **`humanizer`** + akcept `brand-voice-manager`
PRZED statusem `gotowy`. Pole `schema_jsonld` generuje `seo-tech-lead` (patrz `blog/SCHEMA.md`).

## Konwencja nazw plików

`RRRR-MM-DD_slug-wpisu.json` – np. `2026-09-01_therapy-session-prep-checklist.json`.
Prefiks daty = sugerowana data publikacji (drip sortuje po `planowana_data`). Slug = `seo_url`.

## Pola pliku JSON (mapowanie na kolekcję Blog Posts w Webflow)

| pole | wymagane | pole CMS Webflow | uwagi |
|---|---|---|---|
| `tytul` | TAK | `name` | tytuł = H1 na stronie wpisu; fraza kluczowa z przodu; EN |
| `tresc_html` | TAK | `post-body` (RichText) | pełna treść HTML **RichText-safe**: tylko `p, h2-h6, ul/ol/li, blockquote, figure/img, a, strong, em, code`. **ZERO `div`, `style=""`, `<script>`** – Webflow je wytnie. Karty funkcji jako placeholdery `[FEATURE: ...]` (niżej) |
| `zajawka_html` | TAK | `post-summary` (PlainText) | lead na grid bloga + baza meta; skrypt zdejmuje tagi HTML |
| `kategoria` | TAK | `category` (Option) | **nazwa** z zestawu: `Therapy` \| `MindSync Tips` (skrypt mapuje na option id; `All` = filtr, nie przypisujemy) |
| `meta_title` | zalecane | `seo-title` | ≤ ~60 zn.; wymaga jednorazowego podpięcia pola w ustawieniach szablonu wpisu (Designer) |
| `meta_description` | zalecane | `seo-description` | ~150-160 zn.; jw. |
| `seo_url` | TAK | `slug` | slug wpisu (idempotencja publikacji idzie PO SLUGU); małe litery, myślniki |
| `hero_image` | opcjonalne | `main-image` | ścieżka lokalna do gotowego pliku; domyślnie skrypt szuka `blog/images/<slug>/hero-1600x900.(webp\|jpg\|png)`. Upload przez Webflow Assets API, w polu ląduje `{url, alt}` |
| (auto) | – | `thumbnail-image` | `blog/images/<slug>/hero-800x600.*`; brak = fallback na hero 1600x900 |
| `hero_prompt` | zalecane | (nie CMS) | ścieżka do `.md` z promptem albo inline – generacja PRZED dripem (`gemini-generate.ps1`); **drip NIE generuje grafik** |
| `hero_image_alt` | TAK | `hero-alt` + alt obrazka | alt hero (SEO + WCAG); EN |
| `featured` | opcjonalne | `featured` (Switch) | true = wpis wyróżniony na gridzie; odpowiednik `start_page` z PLASMET; domyślnie false |
| `kolor` | opcjonalne | `color` (Color) | akcent karty na gridzie; TYLKO z zestawu brandowego (`docs/blog/brand-mindsync.md` §3); domyślnie `#339499` |
| `schema_jsonld` | zalecane | `schema-jsonld` (PlainText) | goły JSON (BlogPosting+FAQPage graf, patrz `blog/SCHEMA.md`); **bez** `<script>` – wrapper daje szablon wpisu |
| `tagi` | opcjonalne | (brak pola w CMS) | zostaje w JSON jako metadane robocze (klastry); Webflow Blog Posts nie ma tagów |
| `planowana_data` | TAK | – (sterowanie dripem) | `YYYY-MM-DD`; drip publikuje gdy `dziś >= planowana_data`; **1 wpis dziennie – bez kolizji dat** |
| `status` | TAK | – (sterowanie kolejką) | `szkic` → `gotowy` → `opublikowany` (ustawia skrypt; dopisuje `item_id` + `permalink`) |
| `glos` | TAK dla nowych | brak (tylko kontrola jakości) | `"monika-v1"`: wpis napisany stylem Moniki ścieżką `/blog-write` (skill). Włącza `scripts/blog-voice-check.py` w bramce kolejki; wpis bez tego pola z datą od 2026-09-26 dostaje ostrzeżenie. Publikator pole ignoruje |

## Karty funkcji w `tresc_html` (odpowiednik kafelków produktowych – zasada twarda)

Wpis, który cokolwiek **porównuje, rekomenduje albo pokazuje „jak to robić"**, prowadzi do
konkretnej funkcji MindSync kartą, nie samym linkiem w tekście. W kolejce trzymamy
placeholdery; rozwiązuje je `blog-publish.ps1` z katalogu `blog/app-features.json`:

```
[FEATURE: <id z katalogu> | <powód, jedno zdanie EN>]
[FEATURES: <nagłówek sekcji> || <id> | <powód> || <id> | <powód> || <id> | <powód>]
```

Wzorzec rozmieszczenia: 1-2 karty `[FEATURE: ...]` inline przy akapitach o konkretnym
problemie + jeden blok `[FEATURES: ...]` z trzema pozycjami przed sekcją FAQ. Nie zamieniaj
artykułu w katalog: 2-3 karty na wpis to sufit.

- Funkcja musi zgadzać się z tym, co mówi akapit (id z `blog/app-features.json`, status live).
- Zdanie „powód" to proza → `humanizer` + zakaz em-dash.
- **Bez cen w treści** (cennik się zmienia; od cen jest `/membership`). CTA karty prowadzi do
  `cta_url` funkcji; etykieta domyślna: „Try it free in MindSync".
- Render jest RichText-safe (figure+img+p z linkami). Bogaty blok pobrania apki (badge
  App Store/Google Play) jest RAZ w szablonie wpisu (Designer) – nie wstawiaj go do treści.
- Nieznane id albo nierozwiązany placeholder = drip pomija wpis (bramka).

## Struktura wpisu (wzorzec jakości)

Od 2026-09-25 wzorcem jest styl Moniki (newslettery MindSync): pełna specyfikacja
w `docs/blog/brand-mindsync.md` §2, tekst wzorcowy w `docs/blog/voice-sample-monika.md`.
Szkielet (szczegóły i objętości: brand doc §2.2):

1. **Otwarcie-rozpoznanie** (60-120 słów): pytanie o konkretny moment, lista „Do any of
   these sound familiar?" z trzema scenkami albo obserwacja o codzienności. Nie definicja.
2. **H2 sekcje merytoryczne**: skąd to się bierze, jak to wygląda w życiu, co mówią badania
   (rok + autor/instytucja, opowiedziane jako historia, z wnioskiem dla czytelnika i uczciwym
   zdaniem o granicach wiedzy).
3. **Sekcja praktyczna**: 3-5 kroków w trybie rozkazującym, nagłówek z charakterem, co
   najmniej jedno gotowe zdanie do powiedzenia na głos.
4. **Akapit o apce + karta [FEATURE:]** w rytmie „This is what... Log... Give it time...
   Then...", z konkretami wziętymi z tematu wpisu.
5. **Pytanie do czytelnika**: jedno osobiste zdanie, ostatnie przed FAQ.
6. **FAQ** pod nagłówkiem dokładnie **„Frequently asked questions"** (H2), 4-5 pytań (H3)
   przepisanych dosłownie z zapytań GSC; zasila FAQPage schema i GEO. Odpowiedzi też jej głosem.
   **Odpowiedź do zacytowania (od 2026-09-28):** pierwsze 2-3 zdania każdej odpowiedzi
   odpowiadają wprost i są zrozumiałe bez reszty wpisu (bez „as above”, „this”, „it” odsyłających
   do tekstu wyżej). Asystenci AI (ChatGPT, Perplexity, AI Overviews) cytują pojedyncze
   akapity, a GSC już pokazuje zapytania w formie ich promptów (wpis o prywatności apek).
7. Bez sekcji „Podsumowanie-wata".

## Linki do wpisów, które jeszcze nie wyszły: `[LINK-LATER:]`

Link do wpisu z tej samej partii, który publikuje się PÓŹNIEJ, wstawiaj jako:
`[LINK-LATER: <slug-celu> | <anchor text EN>]`. Publikator przy publikacji: cel już
`opublikowany` → pełny `<a href="/journal/<slug>">`; cel jeszcze nie wyszedł → sam anchor
bez linku (zero 404) + notatka w logu do późniejszego fixupu. Zwykłe `[LINK: ...]`
pozostaje ZAKAZANE (bramka dripu). Linki do wpisów już opublikowanych i stron statycznych
wstawiaj normalnym `<a href>`.

## Statusy (cykl życia w kolejce)

- `szkic` – wpis w obróbce, **drip go pomija**.
- `gotowy` – po humanizerze + akcepcie brand-voice + schema; **kwalifikuje się do publikacji**.
- `opublikowany` – skrypt opublikował; dopisuje `item_id` i `permalink`, **nie publikuje ponownie**
  (idempotencja po slugu + `blog/published-log.json`).

## Bramki dripu (każda = pominięcie wpisu, nie błąd)

1. surowe `[LINK: ...]` w treści,
2. **długi myślnik U+2014** w `tresc_html`/`tytul`/`meta_title`/`meta_description`/`zajawka_html`,
3. błąd renderu kart / nierozwiązany `[FEATURE:]` po renderze / nieznane id funkcji,
4. brak pliku hero na dysku (`blog/images/<slug>/hero-1600x900.*`),
5. brak zajawki.

Walidacja całej kolejki przed dripem: `python scripts/blog-queue-gate.py`.

## Minimalny prawidłowy wpis

Patrz `blog/queue/_przyklad.json`.
