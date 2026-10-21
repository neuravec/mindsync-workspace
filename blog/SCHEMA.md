# Dane strukturalne JSON-LD bloga MindSync (BlogPosting + FAQPage)

Właściciel: `seo-tech-lead`. Cel: rich resulty (Article, FAQ) + cytowalność w AI (GEO)
dla wpisów na `mindsync.app/journal/<slug>`.

> Wzorzec projektu grafu przeniesiony z PLASMET (tam zweryfikowany na 24 wpisach);
> kanał wstrzyknięcia przepisany pod Webflow. Referencja: `docs/blog-plasmet-reference/`.

---

## 1. Projekt schematu

Dla każdego wpisu **jeden** blok `<script type="application/ld+json">` z grafem `@graph`:

1. **Organization** (`@id` = `https://mindsync.app/#organization`) – publisher i autor:
   MindSync, `https://mindsync.app`, logo (URL z CDN Webflow), `sameAs` (App Store,
   Google Play, Instagram, Discord).
2. **BlogPosting** (`@id` = `<url>#article`):
   - `headline` = `tytul`, `description` = zajawka bez HTML, `inLanguage` = `en`
   - `datePublished`/`dateModified` = `planowana_data` / data publikacji (ISO 8601)
   - `author` + `publisher` = referencja `@id` Organization
   - `mainEntityOfPage` = WebPage `@id` = `https://mindsync.app/journal/<slug>`
   - `articleSection` = kategoria (`Therapy` / `MindSync Tips`)
   - `image` = ImageObject 1600×900 z `caption` = `hero_image_alt` – tylko gdy hero istnieje
3. **FAQPage** (`@id` = `<url>#faq`): `mainEntity` = pary Question/Answer **1:1** z sekcją
   „Frequently asked questions" w treści (H3 = pytanie, następujący `<p>` = odpowiedź),
   oczyszczone do czystego tekstu.

Jeden `<script>` z `@graph` (współdzielona encja Organization) – nie dwa osobne bloki.
AggregateRating/opinie: NIE dodajemy do wpisów (to artykuły, nie produkty).

## 2. Generowanie

Graf buduje `seo-tech-lead` per wpis (ręcznie lub skryptem, gdy powstanie odpowiednik
`blog-schema-gen.ps1` – referencyjny skrypt PLASMET parsował FAQ z `tresc_html`; do
przeniesienia 1:1 ze zmianą: nagłówek FAQ = „Frequently asked questions", URL =
`https://mindsync.app/journal/<seo_url>`, język `en`). Wynik trafia do pola
**`schema_jsonld`** w pliku kolejki jako **goły JSON (string), bez `<script>`**.

## 3. Kanał wstrzyknięcia — WDROŻONY 2026-08-25 (element DOM zbindowany do pola CMS)

Webflow RichText **nie przepuszcza `<script>`** w treści wpisu, więc wariant „dokleić do
content" z PLASMET tu nie działa. Kanał wdrożony przez MCP (lepszy niż planowany
custom code w head – zero kroków ręcznych):

1. Kolekcja Blog Posts ma pole **`schema-jsonld`** (PlainText, dodane 2026-08-25).
   Publikator (`scripts/webflow/blog-publish.ps1`) wpisuje tam goły JSON z kolejki.
2. W szablonie **Blog Posts Template** siedzi element DOM `<script
   type="application/ld+json">` (Navigator: „Blog Post JSON-LD"), którego **Text Content
   jest ZBINDOWANY do pola Schema JSONLD** (ustawienie `text`, binding cms →
   field 6854520190fa4adf02bad0f890efb253). Renderuje się per wpis, na końcu `<body>`
   (Google akceptuje JSON-LD w body). Puste pole = pusty `<script>` – nieszkodliwe.
3. **TEST WARUNKUJĄCY po pierwszej publikacji wpisu z wypełnioną schemą:** view-source
   żywego wpisu → czy JSON przeżył bez escapowania encji (`&quot;` zamiast `"` = problem).
   Walidacja: Rich Results Test + validator.schema.org. Jeśli binding escapuje, wariant
   zapasowy: Page settings szablonu → Custom code w `<head>` z „+ Add field → Schema
   JSONLD" (ręcznie w Designerze).

Dodatkowo (niezależnie od wpisów): statyczne strony (`/`, `/features`, `/membership`, `/blog`)
mogą dostać schema Organization/WebSite przez MCP `data_pages_tool →
bulk_update_pages_schema_markup` – to osobny backlog `seo-tech-lead`.

## 4. Jak walidować

1. **Po publikacji:** https://search.google.com/test/rich-results → URL wpisu → oczekiwane
   „Article" + „FAQ".
2. **Przed publikacją:** zakładka „Kod" w Rich Results Test → wklej graf.
3. **Offline:** każdy `schema_jsonld` musi parsować się jako poprawny JSON
   (sprawdza `blog-queue-gate.py` jako ostrzeżenie przy braku).
4. FAQ w schema = 1:1 z widoczną sekcją FAQ w treści (warunek Google).
