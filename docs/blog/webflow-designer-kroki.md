# Trzy jednorazowe kroki w Webflow Designerze (blog MindSync)

> **STAN 2026-08-25 (po sesji z MCP Bridge): kroki 2 i 3 WYKONANE przez agenta**
> (JSON-LD = element DOM w szablonie zbindowany do pola Schema JSONLD, patrz
> `blog/SCHEMA.md` §3; blok CTA „Blog CTA - Download App" zbudowany i zweryfikowany
> snapshotem). **Do zrobienia ręcznie został TYLKO krok 1** (podpięcie pól SEO
> w ustawieniach strony szablonu – tego page-settings API/bridge nie sięga) oraz
> **Publish całej strony** (przycisk w Designerze; zmiany są draftem do publishu).

> O co chodzi: publikator wpisuje dane do pól CMS, ale sam **szablon strony wpisu**
> (Blog Posts Template) musi raz zostać nauczony, ŻE i GDZIE te pola pokazywać.
> To 10-15 minut klikania w Designerze. Bez tego wpisy publikują się poprawnie,
> ale: Google widzi generyczny tytuł/opis zamiast naszych, nie dostaje danych
> strukturalnych, a pod wpisem nie ma bloku „pobierz apkę".
>
> Wykonanie: operator ręcznie wg poniższego ALBO sesja Claude przez **Webflow MCP
> Bridge App** – otwórz site w Designerze, uruchom w nim aplikację MCP Bridge
> i powiedz w sesji, że Designer jest otwarty; wtedy agent może klikać za Ciebie
> (krok 3 na pewno; kroki 1-2 to page settings – jeśli bridge ich nie sięga,
> zostaje ręcznie wg instrukcji).

## Krok 1. Meta title/description z pól CMS (SEO szablonu wpisu)

**Po co:** dziś każdy wpis ma w Google tytuł „MindSync Blog | <nazwa>" i jeden wspólny
opis. Po tym kroku każdy wpis dostaje własne meta z pól `SEO Title` / `SEO Description`,
które wypełnia pipeline.

1. Designer → Pages (ikona stron) → sekcja **Blog Posts Template** → ikona zębatki (Settings).
2. Sekcja **SEO settings**:
   - **Title tag** → skasuj obecną formułę → **+ Add field** → wybierz **SEO Title**.
   - **Meta description** → **+ Add field** → **SEO Description**.
3. (Opcjonalnie sekcja **Open Graph settings**: OG title/description „same as SEO",
   OG image → **+ Add field** → **Main Image**.)
4. Save. Zmiana obejmie wpisy przy najbliższym publish strony (patrz „Publikacja" niżej).

## Krok 2. Osadzenie JSON-LD (dane strukturalne per wpis)

**Po co:** rich resulty (Artykuł + FAQ) i cytowalność w AI. Pipeline wkłada goły JSON
do pola `Schema JSONLD`; szablon musi go opakować w `<script>` w `<head>`.

1. Te same ustawienia strony **Blog Posts Template** → sekcja **Custom code** →
   pole **Inside `<head>` tag**.
2. Wpisz dokładnie:
   ```
   <script type="application/ld+json">
   ```
   → kliknij **+ Add field** → wybierz **Schema JSONLD** → dopisz:
   ```
   </script>
   ```
3. Save.
4. **TEST WARUNKUJĄCY** (po pierwszej publikacji wpisu z wypełnioną schemą):
   view-source żywego wpisu → JSON musi być czysty (jeśli widzisz `&quot;` zamiast
   cudzysłowów = Webflow escapuje pole; wtedy wracamy do wariantu zapasowego
   z `blog/SCHEMA.md` §3). Walidacja: https://search.google.com/test/rich-results

## Krok 3. Blok CTA „pobierz apkę" pod treścią wpisu

**Po co:** RichText treści nie pozwala na ładny, stylowany blok z badge'ami App Store /
Google Play – więc siedzi on RAZ w szablonie i pokazuje się pod KAŻDYM wpisem.

1. Designer → otwórz stronę **Blog Posts Template** (canvas).
2. Pod elementem Rich Text (post body) dodaj Section z:
   - nagłówek (np. „Keep more from every session"),
   - 1-2 zdania (do uzgodnienia z brand-voice-manager),
   - dwa linki-badge: App Store → `https://apps.apple.com/us/app/mindsync-ai-health-journal/id6739644256`,
     Google Play → `https://play.google.com/store/apps/details?id=com.mindsync.app`.
3. Stylowanie w duchu brand doc (`docs/blog/brand-mindsync.md` §3): tło ocean mist/aqua,
   zaokrąglenia, forest jako kolor tekstu. To element szablonu – wystarczy zrobić raz.

## Publikacja zmian szablonu

Zmiany w Designerze wymagają **site publish** (cała strona) – to robi wyłącznie operator
przyciskiem Publish w Designerze (agenci mają zakaz site-publish). Najlepiej połączyć
z najbliższą planowaną publikacją zmian na stronie.
