# Hero: does-insurance-cover-therapy

Źródło promptu (uzasadnienie, kontrola kadru, kryteria odrzucenia):
`scripts/image-gen/prompts-blog-mindsync/partia6-does-insurance-cover-therapy.md`.
Poniższy blok jest identyczny; `gemini-generate.ps1` bierze pierwszy blok kodu z pliku.

```
A quiet everyday scene told through objects and light: a bright pale oak table beside a tall window in the morning, on it a plain unmarked cream envelope lying flat with its flap closed, a blank uncoated card in a soft warm sand tone resting half over the envelope, a simple matte pen lying parallel beside them, and a ceramic mug of coffee in a muted teal glaze (#339499) with a faint wisp of steam, an ordinary moment of sitting down to sort things out, unhurried and settled rather than stressed. Soft diffused morning light from a window on the right, a sheer linen curtain softening it, gentle long shadows across the tabletop, the wall behind the table plain and softly lit. Calm, warm editorial photograph. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed) with warm sand accents (#ffc88a, #ffefdd), the teal glaze of the mug (#339499) as the one saturated color note, and deep teal forest (#1f3d38) as the single darkest tone in the shadows, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field, generous empty space on the left third of the frame for a headline area that stays completely empty, the envelope, card, pen and mug grouped inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, reassuring mood, premium interior photography. No text, no letters, no handwriting, no numbers, no address on the envelope, no stamps, no postmarks, no printed forms, no bills, no invoices, no insurance cards, no credit cards, no logos, no brand marks, no watermark, no phone, no laptop, no screens of any kind, no application interface, no calculator, no money, no coins, no people, no hands, no faces, no clinical or medical objects, no pills, no stethoscope, no clutter, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo stress or despair poses.
```

## Specyfikacja

- Model: `gemini-3-pro-image`, 16:9, 2K.
- Wyjście (nazwy, których szuka `scripts/blog-queue-gate.py`, wzór `blog/images/when-to-stop-therapy/`):
  `hero-raw.png`, `hero-1600x900.webp` (budżet 150 KB), `hero-1600x900.jpg`,
  `hero-800x600.webp` (budżet 90 KB), `hero-800x600.jpg`.
- Konwersję robi ImageMagick wewnątrz `gemini-generate.ps1`. NIE używać `png-to-webp.py`.
- Alt (`hero_image_alt`, bez zmian): "A plain envelope and a blank card beside a mug and a pen on a bright table"

## Komenda (PowerShell, LIVE, płatna ~0.04 USD)

```powershell
$env:PATH = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI;" + $env:PATH
& "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\gemini-generate.ps1" `
  -PromptFile "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\prompts-blog-mindsync\partia6-does-insurance-cover-therapy.md" `
  -OutDir "C:\Users\mikol\Notebooks\MindSync\Heroku\blog\images\does-insurance-cover-therapy" `
  -Slug "hero" -Model "gemini-3-pro-image" -DryRun:$false
```

Po generacji: obejrzeć `hero-1600x900.jpg` i `hero-800x600.jpg` wg kryteriów odrzucenia
(napis/adres/znaczek na papierze, dłoń, telefon, karta, neon, czarne cienie, koperta bliżej
niż 30% od lewej). Regeneracja: ta sama komenda z `-Force`. Wagi WebP ponad budżet:
skrypt to zgłasza na żółto.
