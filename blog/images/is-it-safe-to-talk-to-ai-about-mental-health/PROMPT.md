# Hero: is-it-safe-to-talk-to-ai-about-mental-health

Źródło promptu (uzasadnienie, kontrola kadru, kryteria odrzucenia):
`scripts/image-gen/prompts-blog-mindsync/partia6-is-it-safe-to-talk-to-ai-about-mental-health.md`.
Poniższy blok jest identyczny; `gemini-generate.ps1` bierze pierwszy blok kodu z pliku.

```
A quiet everyday scene told through objects and light: a low round pale birch side table beside the softly rounded arm of a pale linen armchair, on the table a small closed lidded ceramic box with a smooth matte glaze in deep forest green (#1f3d38), its lid resting firmly shut, a small plain brass key lying flat beside it, and a softly folded pale mint linen throw draped over the armchair arm, the moment just after a long night when things feel settled and kept safe, calm and private rather than secretive or anxious. At the right edge of the scene a simple small table lamp with a plain linen shade still glowing a warm sand light (#ffc88a), while the first pale clear morning daylight comes in from a window out of frame on the left, the two lights meeting gently on the tabletop, the room already bright and airy. Calm, warm editorial photograph. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed, #bbe4de) with warm sand accents (#ffc88a, #ffefdd), the deep forest green of the ceramic box (#1f3d38) as the one deep color note, and the same deep teal forest as the single darkest tone in the shadows, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field with the box and the key in crisp focus, generous empty space on the left third of the frame made of plain softly lit wall for a headline area that stays completely empty, the table, the box, the key and the lamp grouped inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, reassuring mood, premium interior photography. No text, no letters, no handwriting, no numbers, no engraving, no monogram, no ornament on the box, no key tag, no label, no padlock, no chains, no logos, no brand marks, no watermark, no AI logos, no robots, no chatbot icons, no speech bubbles, no glowing circuits, no microphones, no phone, no smartphone, no laptop, no tablet, no screens of any kind, no application interface, no paper, no notebook, no envelope, no pen, no mug, no cup, no people, no hands, no faces, no clinical or medical objects, no pills, no clutter, no night darkness, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo stress or despair poses.
```

## Specyfikacja

- Model: `gemini-3-pro-image`, 16:9, 2K.
- Wyjście (nazwy, których szuka `scripts/blog-queue-gate.py`):
  `hero-raw.png`, `hero-1600x900.webp` (budżet 150 KB), `hero-1600x900.jpg`,
  `hero-800x600.webp` (budżet 90 KB), `hero-800x600.jpg`.
- Konwersję robi ImageMagick wewnątrz `gemini-generate.ps1`. NIE używać `png-to-webp.py`.
- Alt (`hero_image_alt`, zaktualizowany w kolejce): "A small closed forest green ceramic box with a little brass key beside it on a side table at dawn"

## Komenda (PowerShell, LIVE, płatna ~0.04 USD)

```powershell
$env:PATH = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI;" + $env:PATH
& "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\gemini-generate.ps1" `
  -PromptFile "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\prompts-blog-mindsync\partia6-is-it-safe-to-talk-to-ai-about-mental-health.md" `
  -OutDir "C:\Users\mikol\Notebooks\MindSync\Heroku\blog\images\is-it-safe-to-talk-to-ai-about-mental-health" `
  -Slug "hero" -Model "gemini-3-pro-image" -DryRun:$false
```

Po generacji: obejrzeć `hero-1600x900.jpg` i `hero-800x600.jpg` wg kryteriów odrzucenia
(napis/grawer/logo na pudełku, kluczu lub lampie; telefon, ekran, dymek, robot, kłódka, dłoń;
otwarte pudełko; ciemny nocny kadr; zieleń w czerń lub szmaragd; czarne cienie; pudełko
bliżej niż 30% od lewej). Regeneracja: ta sama komenda z `-Force`. Wagi WebP ponad budżet:
skrypt to zgłasza na żółto.
