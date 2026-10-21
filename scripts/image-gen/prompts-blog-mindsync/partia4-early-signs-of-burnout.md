# Partia 4 / 01: early-signs-of-burnout

**Wpis:** „Burnout Doesn't Announce Itself: The Early Signs of Burnout Nobody Warns You About"
(drip 2026-09-26, wejście partii). **Wariant:** codzienny moment (`hero-01-codzienny-moment.md`).

**Dlaczego ta scena:** kąt wpisu to „wczesnym sygnałem jest często stygnięcie, a nie
zmęczenie" (Leiter i Maslach 2016), więc hero pokazuje ostygnięcie w przedmiotach, a nie
wyczerpanie w człowieku. Pełny kubek herbaty bez pary stoi obok laptopa, do którego nikt
nie wrócił, w złotym świetle późnego popołudnia. Scena jest spokojna i zwyczajna, bez
dramatu, bo wpis opisuje objawy, które łatwo przeoczyć. Dominanta to ciepły bursztyn i piasek,
w zgodzie z kolorem karty wpisu `#e8af0a`; pozostałe dwa hero partii mają dominantę turkusową
(02) i wieczorną z przygaszonym błękitem (03).

Laptop jest odwrócony ekranem od widza, więc w kadrze widać tylko gładką, pustą pokrywę.
W części pozytywnej nie ma żadnych kartek, karteczek, notatek ani ekranów, bo każda z tych
rzeczy zaprasza model do dopisania tekstu.

```
A quiet everyday scene told through objects and light: a pale oak desk beside a tall window at golden hour, on it an open slim laptop seen from behind with its lid raised and its plain smooth back facing the viewer, and next to it a full ceramic mug of tea in warm sand glaze that has gone still, no steam, a small pale linen napkin folded under the mug, low late afternoon sun coming through the window on the right and laying long warm amber bands of light across the desk surface, a sheer linen curtain softening the light, the wall behind the desk plain and softly lit. Calm, warm editorial photograph in low golden late afternoon light, still and ordinary rather than sad, a desk someone stepped away from a while ago. Warm amber and honey dominant light (#e8af0a used only as the color of the sunlight, never as a solid shape), muted palette of warm sand (#ffc88a, #ffefdd), pale mint white (#f6fffd) and aqua (#dbf0ed) in the cool side of the room, and deep teal forest (#1f3d38) as the single darkest tone in the shadows, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field, generous empty wall space on the left of the frame for a headline area that stays completely empty, the laptop and the mug placed inside the right two thirds of the frame with the mug slightly right of center. Wide 16:9 landscape composition (1600x900), main subject off center to the right, settled and reassuring mood, premium interior photography. No text, no letters, no numbers, no logos, no brand marks on the laptop, no apple logo, no watermark, no visible laptop screen, no readable screen of any kind, no application interface, no paper notes, no sticky notes, no documents, no calendar, no clock, no people in the frame, no hands, no faces, no crumpled paper, no clutter, no coffee spills, no clinical or medical objects, no pills, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo exhaustion or despair poses.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`,
czyli zostawia prawe 75% szerokości i wycina lewą ćwiartkę. Lewa ćwiartka to pusta, ciepło
oświetlona ściana pod nagłówek; laptop i kubek siedzą w prawych dwóch trzecich, okno po
prawej. Po generacji sprawdź, czy kubek nie wylądował bliżej niż 30% szerokości od lewej
krawędzi. Jeśli tak, regeneruj zamiast ratować kadrowaniem.

**`hero_image_alt`:** „A quiet desk at golden hour with an untouched mug of tea beside a laptop" (bez zmian, zgodny z kolejką)

**Kontrola po generacji:** odrzuć render z widocznym ekranem laptopa, logo producenta na
pokrywie, parą nad kubkiem (psuje „ostygnięcie"), kartkami z pismem albo człowiekiem w kadrze.
Odrzuć też render, w którym bursztyn zamienił się w żółte plamy albo pomarańczowy neon.

**Generacja (podgląd suchy, z katalogu `scripts/image-gen/`):** `powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 -PromptFile .\prompts-blog-mindsync\partia4-early-signs-of-burnout.md -OutDir ..\..\blog\images\early-signs-of-burnout -Slug hero`
