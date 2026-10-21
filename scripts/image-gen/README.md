# scripts/image-gen — generacja grafik HERO bloga przez Gemini API

Automatyzacja grafik hero wpisów bloga PLASMET przez **Google Gemini API** (Nano Banana).
Część pipeline'u publikacji bloga: `gemini-generate.ps1` (generacja) → `news-hero-upload.ps1`
(upload do Shopera) — spina je `scripts/shoper-api/blog-publish.ps1`.

> Standard wymiarów/wagi/stylu grafik: `blog/images/_standard-grafiki-bloga.md` (1600×900 desktop +
> 800×600 mobile, WebP+JPG, paleta niebieska DS, zero tekstu w grafice).
> Konwencje promptów: `szablon/prompty-grafik/`.

## 1. Konfiguracja klucza (jednorazowo)

1. Wygeneruj klucz API w **Google AI Studio**: https://aistudio.google.com/apikey
2. Skopiuj wzorzec i wpisz klucz:
   ```powershell
   Copy-Item .env.example .env
   # otwórz .env i wpisz: GEMINI_API_KEY=AIza...   (NIE commituj — .env jest w .gitignore)
   ```
3. Skrypt **nigdy nie wypisuje** wartości klucza — tylko status `[USTAWIONE]` / `[PUSTE]`.

## 2. Zależność: ImageMagick (do WebP/JPG + resize)

Konwersja surowego PNG z Gemini do **WebP+JPG** i resize do 1600×900 / 800×600 wymaga
**ImageMagick** (polecenie `magick`). Skrypt **wykrywa go sam**:

- **Jest** → generuje komplet 4 plików wg standardu + raportuje wagi vs budżet.
- **Brak** → zapisuje sam surowy PNG i **wyraźnie ostrzega** + podaje jak doinstalować:
  ```powershell
  winget install ImageMagick.ImageMagick     # albo: choco install imagemagick
  ```
  (po instalacji ponów generację z `-Force`, albo skonwertuj ręcznie poleceniami ze standardu).

## 3. Użycie

**Domyślnie `-DryRun` = `$true`** — pokazuje co BY wysłał (model, aspect ratio, prompt, pliki),
ale **NIE woła Gemini i NIC nie zapisuje**. Realna generacja: jawnie `-DryRun:$false`
(wymaga klucza; każde wywołanie kosztuje ~$0,02–0,04 za obraz na modelu flash).

```powershell
# PODGLĄD (sucho) — z gotowego promptu graphic-designera:
powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 `
  -PromptFile ..\..\szablon\prompty-grafik\blog-01-hero-wiertarko-wkretarka.md `
  -OutDir ..\..\blog\images\01-jak-wybrac-wiertarko-wkretarke -Slug hero

# LIVE (po dostarczeniu klucza):
powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 `
  -PromptFile ..\..\szablon\prompty-grafik\blog-01-hero-wiertarko-wkretarka.md `
  -OutDir ..\..\blog\images\01-jak-wybrac-wiertarko-wkretarke -Slug hero -DryRun:$false

# Prompt inline + model flagowy (Nano Banana Pro) pod ważne hero/banery:
.\gemini-generate.ps1 -Prompt "Realistyczna fotografia warsztatu..." `
  -OutDir ..\..\blog\images\<slug> -Model gemini-3-pro-image -DryRun:$false
```

### Parametry

| parametr | domyślnie | opis |
|---|---|---|
| `-Prompt` / `-PromptFile` | — | treść promptu inline ALBO ścieżka do `.md`/`.txt`. Z `.md` skrypt bierze pierwszy blok ` ``` ` i czyści dyrektywy CLI (`/seo image-gen`, `--ar`, `--resolution`) |
| `-OutDir` | (wymagany) | katalog docelowy, np. `blog/images/<slug>/` |
| `-Slug` | `hero` | baza nazwy: `<Slug>-1600x900.webp`, `<Slug>-800x600.jpg`… |
| `-AspectRatio` | `16:9` | proporcja hero (standard). Mobile 4:3 robi crop ImageMagick |
| `-Model` | `gemini-2.5-flash-image` | tańszy (Nano Banana, ~$0,02–0,04). Flagowe: `gemini-3-pro-image` |
| `-ImageSize` | `2K` | `1K`/`2K`/`4K`. 2K wystarcza na 1600×900 z zapasem na crop |
| `-DryRun` | `$true` | **bezpieczny default**. Realnie: `-DryRun:$false` |
| `-Force` | (off) | nadpisz istniejące pliki hero (domyślnie idempotentne — nie nadpisuje) |
| `-TimeoutSec` | `120` | twardy deadline na odpowiedź API (anty-„wiszący zapis") |

## 4. Pliki wynikowe (wg standardu)

```
<OutDir>/<Slug>-1600x900.webp   # desktop/tablet (LCP), WebP q82, budżet ≤150 KB
<OutDir>/<Slug>-1600x900.jpg    # fallback <picture>, q80
<OutDir>/<Slug>-800x600.webp    # mobile (crop art-direction), q82, budżet ≤90 KB
<OutDir>/<Slug>-800x600.jpg     # fallback mobile, q80
<OutDir>/<Slug>-raw.png         # surowy render z Gemini (źródło; w .gitignore)
```

## 5. Wpięcie w pipeline bloga

`scripts/shoper-api/blog-publish.ps1` (krok hero): jeśli wpis ma w JSON **prompt grafiki**
(`hero_prompt` — ścieżka do `.md` lub inline) a pliku hero **brak**, publikacja:
1. woła `gemini-generate.ps1` (generuje hero do `blog/images/<slug>/`),
2. woła `news-hero-upload.ps1` (upload jako `news-files`, base64, `order=0`).

Wszystko respektuje `-DryRun` przekazany do `blog-publish.ps1`. Pole `hero_image` (ścieżka do
gotowego pliku) ma pierwszeństwo; `hero_prompt` to ścieżka generacji „od zera".

## 6. Bezpieczeństwo

- Klucz API **tylko** w `.env` (w `.gitignore`); nigdy w repo/czacie/logach.
- Surowe PNG (`*-raw.png`) w `.gitignore` — nie pchamy ciężkich renderów do repo.
- DryRun jest domyślny wszędzie — żaden przebieg nie wyda pieniędzy ani nie nadpisze plików bez świadomej decyzji.
