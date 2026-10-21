---
name: blog-publish
description: >
  Runbook publikacji wpisu bloga MindSync na Webflow CMS (kolekcja Blog Posts,
  mindsync.app/journal/<slug>) end-to-end: walidacja kolejki, generacja hero (Gemini),
  optymalizacja grafiki, publikacja przez scripts/webflow/blog-publish.ps1 (Data API v2)
  z kartami [FEATURE:], polami SEO i schema. Używaj, gdy trzeba opublikować/zaktualizować
  wpis bloga, dodać/poprawić hero wpisu, albo skonfigurować drip 1 wpis/dzień.
  Zrodlo prawdy formatu: blog/queue/_format.md; kanal: scripts/webflow/README.md.
---

# Publikacja bloga MindSync (Webflow CMS) — runbook

Proces „partia + drip": treść powstaje partiami (z bramkami jakości), publikacja idzie przez
Data API v2. Każdy wpis: **brief → blog-writer (⛔ humanizer) → queue JSON → hero (Gemini) →
schema (seo-tech-lead) → publikacja skryptem**.

## 0. Wymagania wstępne (jednorazowo)

- **Webflow API**: `scripts/webflow/.env` (`WEBFLOW_API_TOKEN` + site/collection id; wzór
  `.env.example`). Token: Site Settings → Apps & Integrations → API access (CMS + Assets,
  read+write). Sekrety NIGDY do czatu/repo.
- **Gemini**: `scripts/image-gen/.env` → `GEMINI_API_KEY`. ⚠ Wymaga włączonego billingu
  (darmowy tier ma limit:0 na modele graficzne → HTTP 429).
- **ImageMagick**: `C:\Program Files\ImageMagick-7.1.2-Q16-HDRI\` – NIE jest na PATH:
  `$env:PATH = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI;" + $env:PATH`
- **Jednorazowo w Designerze (operator / seo-tech-lead):** (1) podpięcie pól `seo-title`/
  `seo-description` w ustawieniach SEO strony „Blog Posts Template"; (2) custom code `<head>`
  szablonu: `<script type="application/ld+json">` + Add field `Schema JSONLD` + `</script>`;
  (3) statyczny blok CTA pobrania apki (badge App Store/Google Play) pod treścią wpisu
  w szablonie. Bez (1)-(2) wpisy publikują się poprawnie, ale bez własnych meta/schema.

## 1. Treść (blog-writer)

- Brief od `seo-content-writer` (po bramce KROK 0: `scripts/blog-coverage-preflight.py`).
- Struktura wg `blog/queue/_format.md`: lead-scena 40-60 słów, H2 sekcje badawcze, sekcja
  praktyczna, FAQ pod nagłówkiem dokładnie **„Frequently asked questions"** (4-5 pytań
  dosłownie z GSC).
- ⚠ **HTML RichText-safe**: tylko `p, h2-h6, ul/ol/li, blockquote, figure/img, a, strong,
  em, code`. Zero div/style/table/script – Webflow wytnie.
- **Karty funkcji** jako `[FEATURE: <id> | <powód>]` / `[FEATURES: ...]` – id z
  `blog/app-features.json` (status live). Bez cen.
- ⛔ **BRAMKA TWARDA: cała proza przez skill `humanizer`** + akcept `brand-voice-manager`
  przed statusem `gotowy`. Zakaz em-dash „—" wszędzie.
- Output = queue JSON wg `_format.md` (+ `hero_prompt` wg
  `scripts/image-gen/prompts-blog-mindsync/`), status `szkic` → po akceptach `gotowy`.

## 2. Hero (Gemini → optymalizacja)

```powershell
$env:PATH = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI;" + $env:PATH
& "scripts\image-gen\gemini-generate.ps1" -Prompt "<hero_prompt>" `
  -OutDir "blog\images\<slug>" -Slug "hero" -Model "gemini-3-pro-image" -DryRun:$false
```

- Wynik: `hero-1600x900.webp|jpg` (≤150 KB WebP) + `hero-800x600.webp|jpg` (≤90 KB).
- Styl wg `docs/blog/brand-mindsync.md` §4: spokój, ciepłe światło, paleta forest/mint/sand,
  **zero tekstu w grafice, zero fałszywych screenshotów apki**, ludzie bez twarzy w centrum.
- ⚠ Drip NIE generuje grafik – hero musi istnieć na dysku PRZED publikacją (bramka).

## 3. Schema (seo-tech-lead)

Graf BlogPosting+FAQPage+Organization wg `blog/SCHEMA.md` → **goły JSON** do pola
`schema_jsonld` w pliku kolejki (bez `<script>`; wrapper daje szablon). FAQ 1:1 z treścią.

## 4. Walidacja + publikacja

```powershell
python scripts/blog-queue-gate.py                       # cala kolejka: blokery/ostrzezenia
powershell -File scripts\webflow\blog-publish.ps1       # DRY-RUN (domyslny) - podglad
powershell -File scripts\webflow\blog-publish.ps1 -Plik <plik>.json -DryRun:$false   # LIVE
```

Skrypt: bramki (em-dash, [LINK:], karty, hero, zajawka) → render kart → upload hero/thumb
(Assets API) → create/update item po slugu → publish item → `published-log.json` + status
`opublikowany` + permalink `https://mindsync.app/journal/<slug>`.

⚠ Publikacja itemu CMS działa bez publikowania całej strony. **Site publish tylko operator.**

## 5. Po publikacji (weryfikacja obowiązkowa)

- Żywy URL `/journal/<slug>`: render body (czy karty [FEATURE:] przeżyły RichText jako
  figure/link), hero, thumbnail na `/blog`.
- View-source: meta title/description (wymaga podpięcia pól w szablonie – krok 0.3),
  JSON-LD obecny i nieescapowany → Rich Results Test (pierwsze wpisy obowiązkowo).
- Pierwsza publikacja = TEST WARUNKUJĄCY schema (blog/SCHEMA.md §3) – wynik odnotuj.

## Harmonogram (drip 1 wpis/dzień)

Windows Task Scheduler, codziennie 07:00 (zakładać DOPIERO po udanym teście DryRun + LIVE
na 1 wpisie):

```
powershell -NonInteractive -ExecutionPolicy Bypass -File scripts\webflow\blog-publish.ps1 -DripOne -DryRun:$false
```

„Run task as soon as possible after a scheduled start is missed" = łapie pominięte
uruchomienia. Brak `gotowy` → exit 0 (nie błąd). Logi: `scripts/webflow/_drip-log.txt`
(+ `_drip-error.txt` przy awarii).

## Reguły twarde

- Każda **proza** przez `humanizer` przed publikacją. Przegląd jakości raz na partię.
- Tekst SEO-istotny = realny HTML (nigdy wtopiony w grafikę).
- DryRun domyślnie TRUE w każdym skrypcie zapisującym; LIVE tylko jawnym przełącznikiem.
- Karty bez cen i danych, które statyczny HTML by zamroził; CTA z `blog/app-features.json`.
