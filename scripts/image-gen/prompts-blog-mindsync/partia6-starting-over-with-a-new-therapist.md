# Partia 6 / starting-over-with-a-new-therapist

**Wpis:** "You Don't Have to Start From Zero: Starting Over With a New Therapist" (drip 2026-10-11).
**Wariant:** codzienny moment (`hero-01-codzienny-moment.md`).

**Dlaczego ta scena:** teza wpisu brzmi "nie zaczynasz od zera, bierzesz ze sobą to, czego się
nauczyłeś". Sadzonka ukorzeniająca się w słoiku z wodą to dokładnie ta myśl: nowa roślina,
która wyrasta z poprzedniej, z widocznymi świeżymi korzeniami. Dwa zamknięte notatniki obok
to "jednostronicowe podsumowanie" i zapisane wnioski, ale bez otwartej strony. Pierwotna
propozycja z kolejki (otwarty notatnik z odręcznym pismem i klucz) odpadła z dwóch powodów:
odręczna strona zaprasza model do wpisania pseudo-tekstu, a stół z papierem jest już w
równoległym hero does-insurance-cover-therapy. Tu zamiast stołu jest półka przy ścianie,
zamiast poranka późne popołudnie, światło z lewej (insurance ma z prawej), a jedyny żywy
kolor to zieleń liścia zamiast turkusowego kubka.

Ryzyko: notatniki kuszą model do tytułów na okładkach i grzbietach, słoik do etykiety.
Negatywy wymieniają je wprost.

```
A quiet everyday scene told through objects and light: a low pale birch wall shelf against a softly lit mint white wall in the late afternoon, on the shelf a small clear glass jar of water holding a single pothos cutting with two heart shaped leaves in a soft muted green and fine new pale roots clearly visible through the glass, and beside the jar two closed notebooks stacked slightly askew, their plain linen covers in warm sand (#ffc88a) and pale aqua (#dbf0ed), a thin ribbon bookmark trailing from the top one, the cutting a quiet sign of something growing on from what came before. Low warm late afternoon sun from a window out of frame on the left, casting a soft diagonal band of light across the wall and the gentle shadow of the leaves, the water in the jar catching a small warm glint. Calm, warm editorial photograph, settled and hopeful rather than sentimental. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed) with warm sand accents (#ffc88a, #ffefdd), the soft green of the two leaves as the one living color note, and deep teal forest (#1f3d38) as the single darkest tone in the shadows, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field with the roots in crisp focus, generous empty space on the left third of the frame made of sunlit plain wall for a headline area that stays completely empty, the jar and the notebooks grouped inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, reassuring mood, premium interior photography. No text, no letters, no handwriting, no numbers, no label on the jar, no titles, labels or embossing on the notebook covers or spines, no open pages, no paper sheets, no logos, no brand marks, no watermark, no keys, no cardboard boxes, no mug, no cup, no envelope, no pen, no phone, no laptop, no screens of any kind, no application interface, no people, no hands, no faces, no clinical or medical objects, no pills, no extra potted plants, no clutter, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo despair poses.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`
(zostawia prawe 75% szerokości). Lewa trzecia kadru to oświetlona, pusta ściana, słoik
i notatniki siedzą w prawych dwóch trzecich. Po generacji sprawdź, czy słoik nie zaczyna się
bliżej niż 30% szerokości od lewej krawędzi. Jeśli tak, regeneruj z `-Force`.

**`hero_image_alt`:** "A plant cutting rooting in a glass jar of water beside two closed notebooks on a sunlit shelf"

**Kontrola po generacji (odrzuć render, jeśli):** na słoiku, okładce albo grzbiecie notatnika
jest jakikolwiek napis, etykieta lub pseudo-pismo; notatnik jest otwarty; w kadrze pojawił się
kubek, klucz, karton, telefon albo dłoń; nie widać korzeni w wodzie (wtedy scena traci sens);
zieleń jest nasycona i dominuje kadr; cienie są czarne zamiast ciemnej zieleni.

**Generacja:** `blog/images/starting-over-with-a-new-therapist/PROMPT.md` (komenda LIVE).
