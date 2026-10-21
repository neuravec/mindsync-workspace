# Hero: how-to-afford-therapy

Źródło promptu (uzasadnienie, kontrola kadru, kryteria odrzucenia):
`scripts/image-gen/prompts-blog-mindsync/partia6-how-to-afford-therapy.md`.
Poniższy blok jest identyczny; `gemini-generate.ps1` bierze pierwszy blok kodu z pliku.

```
A quiet everyday scene told through light and space: a bright, simple entryway seen from inside on a calm morning, a wooden panel door painted in a soft muted teal (#339499) standing slightly ajar, a narrow gap of warm golden morning light spilling through the opening and stretching in a long soft band across pale oak floorboards toward the viewer, beside the door a plain pale linen runner on the floor and a small low birch bench with nothing on it, the open gap hinting at a way in that was there all along, hopeful and unhurried rather than dramatic. Warm sand daylight (#ffc88a, #ffefdd) coming from outside through the gap, the rest of the entryway lit softly and evenly, walls in pale mint white (#f6fffd) and soft aqua (#dbf0ed), gentle shadows. Calm, warm editorial photograph. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed, #bbe4de) with warm sand accents (#ffc88a, #ffefdd), the teal paint of the door (#339499) as the one saturated color note, and deep teal forest (#1f3d38) as the single darkest tone in the shadows, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field, generous empty space on the left third of the frame made of plain softly lit wall for a headline area that stays completely empty, the door, the band of light and the bench grouped inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, reassuring mood, premium interior photography. No text, no letters, no handwriting, no numbers, no house number, no door sign, no nameplate, no letterbox, no mail slot, no doormat with words, no stickers, no posters, no framed pictures, no price tags, no labels, no money, no coins, no banknotes, no piggy bank, no jar, no wallet, no credit cards, no calculator, no receipts, no bills, no envelope, no paper, no mug, no cup, no logos, no brand marks, no watermark, no phone, no laptop, no screens of any kind, no application interface, no people, no silhouettes in the doorway, no hands, no faces, no shoes, no coats, no clinical or medical objects, no pills, no clutter, no dark dramatic tones, no harsh contrast, no blown out white glare, no neon colors outside the palette, no stock photo stress or despair poses.
```

## Specyfikacja

- Model: `gemini-3-pro-image`, 16:9, 2K.
- Wyjście (nazwy, których szuka `scripts/blog-queue-gate.py`):
  `hero-raw.png`, `hero-1600x900.webp` (budżet 150 KB), `hero-1600x900.jpg`,
  `hero-800x600.webp` (budżet 90 KB), `hero-800x600.jpg`.
- Konwersję robi ImageMagick wewnątrz `gemini-generate.ps1`. NIE używać `png-to-webp.py`.
- Alt (`hero_image_alt`, zaktualizowany w kolejce): "A teal door standing slightly ajar with warm morning light spilling across a pale wooden floor"

## Komenda (PowerShell, LIVE, płatna ~0.04 USD)

```powershell
$env:PATH = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI;" + $env:PATH
& "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\gemini-generate.ps1" `
  -PromptFile "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\prompts-blog-mindsync\partia6-how-to-afford-therapy.md" `
  -OutDir "C:\Users\mikol\Notebooks\MindSync\Heroku\blog\images\how-to-afford-therapy" `
  -Slug "hero" -Model "gemini-3-pro-image" -DryRun:$false
```

Po generacji: obejrzeć `hero-1600x900.jpg` i `hero-800x600.jpg` wg kryteriów odrzucenia
(napis/numer/tabliczka na drzwiach, sylwetka w progu, monety/słoik/kubek, neonowy turkus,
przepalone światło, czarne cienie, futryna bliżej niż 30% od lewej). Regeneracja: ta sama
komenda z `-Force`. Wagi WebP ponad budżet: skrypt to zgłasza na żółto.
