# Hero: how-to-switch-therapists

Źródło promptu (uzasadnienie, kontrola kadru, kryteria odrzucenia):
`scripts/image-gen/prompts-blog-mindsync/partia6-how-to-switch-therapists.md`.
Komenda poniżej wskazuje ten plik; `gemini-generate.ps1` bierze z niego pierwszy blok kodu.

## Specyfikacja

- Model: `gemini-3-pro-image`, 16:9, 2K.
- Scena: krótka linia płaskich, piaskowych kamieni przez płytki, spokojny strumień o poranku,
  plener (odróżnia się od stołu z kopertą w does-insurance-cover-therapy i od sadzonki na półce
  w starting-over-with-a-new-therapist).
- Wyjście (nazwy, których szuka `scripts/blog-queue-gate.py`, wzór `blog/images/when-to-stop-therapy/`):
  `hero-raw.png`, `hero-1600x900.webp` (budżet 150 KB), `hero-1600x900.jpg`,
  `hero-800x600.webp` (budżet 90 KB), `hero-800x600.jpg`.
- Konwersję robi ImageMagick wewnątrz `gemini-generate.ps1`. NIE używać `png-to-webp.py`.
- Alt (`hero_image_alt`, zaktualizowany w kolejce): "Flat stepping stones crossing a calm, shallow stream in soft morning light"

## Komenda (PowerShell, LIVE, płatna ~0.04 USD)

```powershell
$env:PATH = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI;" + $env:PATH
& "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\gemini-generate.ps1" `
  -PromptFile "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\prompts-blog-mindsync\partia6-how-to-switch-therapists.md" `
  -OutDir "C:\Users\mikol\Notebooks\MindSync\Heroku\blog\images\how-to-switch-therapists" `
  -Slug "hero" -Model "gemini-3-pro-image" -DryRun:$false
```

Po generacji: obejrzeć `hero-1600x900.jpg` i `hero-800x600.jpg` wg kryteriów odrzucenia
(człowiek, sylwetka, most, łódka, tabliczka, napis, nasycona lub jesienna zieleń, dramatyczny
zachód, czarne cienie, kamienie bliżej niż 30% od lewej). Regeneracja: ta sama komenda z `-Force`.
Wagi WebP ponad budżet: skrypt to zgłasza na żółto.
