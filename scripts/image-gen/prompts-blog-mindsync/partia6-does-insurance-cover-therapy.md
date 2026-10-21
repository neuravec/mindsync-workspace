# Partia 6 / does-insurance-cover-therapy

**Wpis:** "Does Insurance Cover Therapy? How to Find Out Before the First Bill"
(drip 2026-10-12). **Wariant:** codzienny moment (`hero-01-codzienny-moment.md`).

**Dlaczego ta scena:** wpis otwiera się 40 minutami czekania na infolinii i kończy obietnicą,
że następny telefon zajmie pięć minut. Hero pokazuje ten drugi moment: spokojne usiądnięcie
do papierowych spraw przy kawie, bez stresu. Koperta i pusta kartka mówią "sprawy
ubezpieczeniowe" bez pokazywania rachunku, karty ubezpieczenia czy liczb (to wszystko
zaprasza model do wpisania tekstu). Jedyny nasycony akcent to turkusowa glazura kubka
w kolorze karty wpisu `#339499`.

Ryzyko: koperta i kartka to papier, a papier kusi model do dopisania adresu, znaczka albo
pisma. Dlatego negatywy wymieniają je wprost.

```
A quiet everyday scene told through objects and light: a bright pale oak table beside a tall window in the morning, on it a plain unmarked cream envelope lying flat with its flap closed, a blank uncoated card in a soft warm sand tone resting half over the envelope, a simple matte pen lying parallel beside them, and a ceramic mug of coffee in a muted teal glaze (#339499) with a faint wisp of steam, an ordinary moment of sitting down to sort things out, unhurried and settled rather than stressed. Soft diffused morning light from a window on the right, a sheer linen curtain softening it, gentle long shadows across the tabletop, the wall behind the table plain and softly lit. Calm, warm editorial photograph. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed) with warm sand accents (#ffc88a, #ffefdd), the teal glaze of the mug (#339499) as the one saturated color note, and deep teal forest (#1f3d38) as the single darkest tone in the shadows, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field, generous empty space on the left third of the frame for a headline area that stays completely empty, the envelope, card, pen and mug grouped inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, reassuring mood, premium interior photography. No text, no letters, no handwriting, no numbers, no address on the envelope, no stamps, no postmarks, no printed forms, no bills, no invoices, no insurance cards, no credit cards, no logos, no brand marks, no watermark, no phone, no laptop, no screens of any kind, no application interface, no calculator, no money, no coins, no people, no hands, no faces, no clinical or medical objects, no pills, no stethoscope, no clutter, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo stress or despair poses.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`
(zostawia prawe 75% szerokości). Lewa trzecia kadru to pusta, jasna ściana i blat, grupa
przedmiotów siedzi w prawych dwóch trzecich. Po generacji sprawdź, czy koperta nie zaczyna
się bliżej niż 30% szerokości od lewej krawędzi. Jeśli tak, regeneruj z `-Force` zamiast
ratować kadrowaniem.

**`hero_image_alt`:** "A plain envelope and a blank card beside a mug and a pen on a bright table"
(bez zmian, zgodny z kolejką).

**Kontrola po generacji (odrzuć render, jeśli):** na kopercie lub kartce jest jakikolwiek
napis, adres, znaczek, stempel albo pseudo-pismo; w kadrze jest dłoń, telefon, karta
płatnicza lub banknoty; turkus kubka przeszedł w neon albo zdominował kadr; cienie są czarne
zamiast ciemnej zieleni.

**Generacja:** `blog/images/does-insurance-cover-therapy/PROMPT.md` (komenda LIVE).
