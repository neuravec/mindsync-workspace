# Partia 6 / how-to-afford-therapy

**Wpis:** "The Price Tag Isn't the Only Door: How to Afford Therapy" (drip 2026-10-08).
**Wariant:** codzienny moment (`hero-01-codzienny-moment.md`), scena bez ludzi.

**Dlaczego ta scena:** tytuł sam podaje metaforę: cena to nie jedyne drzwi. Hero pokazuje
drzwi w muted teal (kolor karty wpisu `#339499`), lekko uchylone, z ciepłym porannym światłem
wpadającym przez szparę na jasną podłogę. To mówi "jest wejście, którego nie widziałeś" bez
pokazywania pieniędzy, rachunków ani kalkulatora. Pierwotna propozycja z kolejki (słoik
z monetami, kubek i notatnik na parapecie) odpadła z trzech powodów: monety są zakazane
w negatywach tej partii (pieniądze zamieniają wpis w poradnik oszczędzania), słoik na
parapecie z notatnikiem dubluje hero starting-over-with-a-new-therapist (słoik na półce),
a kubek z notatnikiem na jasnym blacie za bardzo przypomina does-insurance-cover-therapy.
Tu nie ma stołu, kubka ani papieru: jest architektura, światło i jeden kolor.

Różnice wobec does-insurance-cover-therapy: przedpokój zamiast stołu, pionowa bryła drzwi
zamiast płaskich przedmiotów na blacie, światło wpada zza drzwi (z głębi kadru), a turkus
jest na dużej płaszczyźnie farby, nie na kubku.

Ryzyko: drzwi kuszą model do numeru domu, tabliczki, wizjera z napisem, wycieraczki
z hasłem albo skrzynki na listy. Negatywy wymieniają je wprost. Drugie ryzyko: sylwetka
człowieka w progu, dlatego "no people, no silhouettes".

```
A quiet everyday scene told through light and space: a bright, simple entryway seen from inside on a calm morning, a wooden panel door painted in a soft muted teal (#339499) standing slightly ajar, a narrow gap of warm golden morning light spilling through the opening and stretching in a long soft band across pale oak floorboards toward the viewer, beside the door a plain pale linen runner on the floor and a small low birch bench with nothing on it, the open gap hinting at a way in that was there all along, hopeful and unhurried rather than dramatic. Warm sand daylight (#ffc88a, #ffefdd) coming from outside through the gap, the rest of the entryway lit softly and evenly, walls in pale mint white (#f6fffd) and soft aqua (#dbf0ed), gentle shadows. Calm, warm editorial photograph. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed, #bbe4de) with warm sand accents (#ffc88a, #ffefdd), the teal paint of the door (#339499) as the one saturated color note, and deep teal forest (#1f3d38) as the single darkest tone in the shadows, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field, generous empty space on the left third of the frame made of plain softly lit wall for a headline area that stays completely empty, the door, the band of light and the bench grouped inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, reassuring mood, premium interior photography. No text, no letters, no handwriting, no numbers, no house number, no door sign, no nameplate, no letterbox, no mail slot, no doormat with words, no stickers, no posters, no framed pictures, no price tags, no labels, no money, no coins, no banknotes, no piggy bank, no jar, no wallet, no credit cards, no calculator, no receipts, no bills, no envelope, no paper, no mug, no cup, no logos, no brand marks, no watermark, no phone, no laptop, no screens of any kind, no application interface, no people, no silhouettes in the doorway, no hands, no faces, no shoes, no coats, no clinical or medical objects, no pills, no clutter, no dark dramatic tones, no harsh contrast, no blown out white glare, no neon colors outside the palette, no stock photo stress or despair poses.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`
(zostawia prawe 75% szerokości). Lewa trzecia kadru to pusta, jasna ściana, drzwi i pas
światła siedzą w prawych dwóch trzecich. Po generacji sprawdź, czy futryna drzwi nie zaczyna
się bliżej niż 30% szerokości od lewej krawędzi. Jeśli tak, regeneruj z `-Force` zamiast
ratować kadrowaniem.

**`hero_image_alt`:** "A teal door standing slightly ajar with warm morning light spilling across a pale wooden floor"
(ZMIENIONY wobec kolejki: stary alt opisywał słoik z monetami, którego w obrazie nie ma;
pole `hero_image_alt` i `hero_prompt` w `blog/queue/2026-10-08_how-to-afford-therapy.json`
zaktualizowane).

**Kontrola po generacji (odrzuć render, jeśli):** na drzwiach, ścianie lub podłodze jest
jakikolwiek napis, numer, tabliczka albo pseudo-pismo; w progu albo za drzwiami widać
sylwetkę, dłoń, buty lub płaszcz; pojawiły się monety, słoik, kubek lub papier; turkus drzwi
przeszedł w neon albo zalewa cały kadr; światło zza drzwi jest przepalone do bieli; cienie są
czarne zamiast ciemnej zieleni.

**Generacja:** `blog/images/how-to-afford-therapy/PROMPT.md` (komenda LIVE).
