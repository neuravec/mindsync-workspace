# Partia 6 / how-to-switch-therapists

**Wpis:** "Switching Isn't a Breakup: How to Switch Therapists, Online or Off" (drip 2026-10-10).
**Wariant:** codzienny moment w plenerze (`hero-01-codzienny-moment.md`, motyw "spacer" z brand doc §4).

**Dlaczego ta scena:** wpis mówi, że zmiana terapeuty to nie rozstanie ani krok wstecz, tylko
następny krok z lepszą wiedzą ("You're not starting over. You're starting better informed").
Kamienie przez płytki, spokojny strumień pokazują dokładnie to: przejście dalej po pewnym
gruncie, bez dramatu i bez obrazu "porzucania". Pierwotna propozycja z kolejki (dwa kubki)
odpadła, bo kubek przy oknie jest już w hero therapy-hangover i w równoległym hero
does-insurance-cover-therapy (stół, okno, rano). Ten kadr jako jedyny w partii jest plenerem,
więc trzy kolejne hero dripu (10-10, 10-11, 10-12) nie wyglądają jak jedna seria martwych natur.

Ryzyko: plener kusi model do zieleni nasyconej, jesieni albo dramatycznego zachodu słońca.
Dlatego paleta jest opisana przez mgiełkę i bladą szałwię, a negatywy wymieniają te warianty wprost.

```
A quiet outdoor scene told through light and landscape: a shallow, clear, slow stream crossing a pale open meadow early in the morning, a short line of five flat, smooth, sand colored stepping stones crossing the water, the nearest stone large in the lower right foreground and the others leading away toward the soft far bank in the right half of the frame, the water around them calm and glassy with a faint mint and aqua sheen and only gentle ripples, the far bank low grasses in pale sage softened by thin morning haze. Soft diffused golden morning light from behind the far bank, warm sand highlights on the tops of the stones, long gentle reflections in the water, an unhurried sense of moving on to the next step with steady footing. Calm, warm editorial photograph. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed) in the sky and the water, warm sand accents (#ffc88a, #ffefdd) on the stones and in the light, and deep teal forest (#1f3d38) only as the darkest tone in the wet edges of the stones and the shadows in the grass, never pure black. Airy, bright and hazy, gentle shallow depth of field with the nearest stone in crisp focus, generous empty space on the left third of the frame made of open calm water and soft sky reflection for a headline area that stays completely empty, every stone inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, reassuring mood, premium nature photography. No text, no letters, no numbers, no signs, no logos, no watermark, no people, no hands, no feet, no faces, no silhouettes, no bridge, no boat, no buildings, no fences, no animals, no waterfall, no rapids, no dark forest, no saturated green, no autumn red or orange foliage, no dramatic sunset, no storm clouds, no harsh contrast, no neon colors outside the palette, no clinical imagery, no stock photo despair poses.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`
(zostawia prawe 75% szerokości). Lewa trzecia kadru to pusta, gładka woda z odbiciem nieba,
kamienie siedzą w prawych dwóch trzecich. Po generacji sprawdź, czy najbliższy kamień nie
zaczyna się bliżej niż 30% szerokości od lewej krawędzi. Jeśli tak, regeneruj z `-Force`.

**`hero_image_alt`:** "Flat stepping stones crossing a calm, shallow stream in soft morning light"

**Kontrola po generacji (odrzuć render, jeśli):** w kadrze jest człowiek, sylwetka, ślad stopy,
most, łódka, tabliczka albo jakikolwiek napis; zieleń jest nasycona lub jesienna; niebo ma
dramatyczny zachód; woda jest wzburzona; cienie są czarne zamiast ciemnej zieleni; kamienie
tworzą równy "chodnik" przez cały kadr zamiast krótkiej linii po prawej.

**Generacja:** `blog/images/how-to-switch-therapists/PROMPT.md` (komenda LIVE).
