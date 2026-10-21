# Partia 2 / 09 – tracking-mood-on-antidepressants

**Wpis:** „How to Track Whether a New Antidepressant Is Helping" (drip 2026-09-12, klaster 6).
**Wariant:** codzienny moment (`hero-01-codzienny-moment.md`).

**Dlaczego ta scena:** wpis jest o obserwowaniu siebie w czasie, więc kadr trzyma kalendarz
i poranny kubek, czyli rytm tygodni, a nie lek. ⛔ **Zakaz kategoryczny (brief + brand doc):
żadnych tabletek, blistrów, buteleczek, opakowań i czegokolwiek farmaceutycznego w kadrze**,
zakaz jest wpisany w prompt dwa razy.

```
A quiet everyday scene told through objects and light: a single plain sheet of pale paper lying flat on a light stone kitchen counter, marked only with one short column of small hand drawn pencil ticks and nothing else, a warm ceramic cup beside it and a small sprig of eucalyptus, clean morning sunlight from a window on the right casting long soft shadows across the counter. Calm, warm editorial photograph in soft golden morning light. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed), with warm sand accents (#ffc88a, #ffefdd) and deep teal forest (#1f3d38) as the darkest tone in the shadows. Airy, almost white surfaces, hairline shadows, gentle shallow depth of field, generous empty counter space on the left of the frame that stays completely empty. Wide 16:9 landscape composition, main subject off center to the right, quiet and reassuring mood, premium interior photography. The paper carries no grid, no ruled squares, no calendar, no printed rows, only a few small pencil tick marks. Absolutely no pills, no tablets, no capsules, no blister packs, no medicine bottles, no pill organisers, no pharmacy packaging, no prescription slips, no syringes, no clinical or medical objects of any kind anywhere in the frame. No text, no letters, no numbers, no dates, no month names, no readable handwriting, no logos, no watermark, no readable phone screens, no visible faces, no people in the frame, no dramatic dark tones, no neon colors outside the palette, no stock photo despair poses.
```


> **Korekta 2026-09-03 (lider):** pierwsza wersja promptu trzymala kalendarz scienny
> i mimo zakazu model dorysowal na siatce znieksztalcone nazwy dni i bezsensowne cyfry.
> Siatka kalendarza sama w sobie prowokuje model do wpisywania liczb, wiec kalendarz
> wypadl z kadru. Powyzszy blok to wersja, ktora zeszla czysta: kartka z kolumna
> olowkowych ptaszkow zamiast kalendarza. Alt bez zmian.

**`hero_image_alt`:** „A sheet of paper with a few pencil ticks beside a cup on a kitchen counter in morning light"

**Kontrola po generacji (obowiązkowa):** obejrzyj render i odrzuć każdy kadr, w którym pojawi
się cokolwiek farmaceutycznego albo czytelne cyfry na kalendarzu. Ten wpis jest najostrożniejszy
w partii.

**Generacja (podgląd suchy, z katalogu `scripts/image-gen/`):** `powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 -PromptFile .\prompts-blog-mindsync\partia2-tracking-mood-on-antidepressants.md -OutDir ..\..\blog\images\tracking-mood-on-antidepressants -Slug hero`
