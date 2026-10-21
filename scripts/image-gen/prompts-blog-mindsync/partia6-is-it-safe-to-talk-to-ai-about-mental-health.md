# Partia 6 / is-it-safe-to-talk-to-ai-about-mental-health

**Wpis:** "Is It Safe to Talk to AI About Mental Health? Where the 2 a.m. Confession Goes"
(drip 2026-10-09). **Wariant:** codzienny moment (`hero-01-codzienny-moment.md`), scena bez ludzi.

**Dlaczego ta scena:** wpis pyta, dokąd trafia nocne zwierzenie, i kończy się zdaniem
"prywatność to nie uczucie, tylko ustawienie". Hero pokazuje to przedmiotem: małe zamknięte
ceramiczne pudełko w głębokiej leśnej glazurze (kolor karty wpisu `#1f3d38`) z drobnym
mosiężnym kluczykiem obok, na stoliku przy fotelu o świcie. Lampka jeszcze się świeci po
nocy, a do pokoju wchodzi pierwsze blade światło dnia: noc z tytułu się skończyła, spokojnie.
Pudełko mówi "co włożysz, zostaje tam, gdzie zdecydujesz", klucz mówi "to ty decydujesz".
Bez telefonu, ekranu, czatu, robota ani logo AI: temat AI jest w tekście, nie w pikselach,
a każdy ekran zaprasza model do fałszywego interfejsu.

Pierwotna propozycja z kolejki (miękka abstrakcja w kształcie dymka) odpadła, bo niemal
dubluje hero are-mental-health-apps-private ("soft enclosed shape in mint and forest tones")
z tego samego klastra prywatności, a dymek łatwo czytać jako ikonę czatu. Różnice wobec
does-insurance-cover-therapy: stolik przy fotelu zamiast stołu przy oknie, świt z lampką
zamiast pełnego poranka, światło z lewej (insurance ma z prawej), zero papieru, zero kubka,
jedyny głęboki kolor to ciemna zieleń pudełka zamiast turkusu.

Ryzyko: pudełko kusi model do grawerunku, wzoru lub ornamentu z literami, kluczyk do
przywieszki z napisem, lampa do widocznego logo. Drugie ryzyko: świt z lampką może zjechać
w ciemny, nocny kadr, dlatego prompt wymusza jasny, przewiewny kadr i zakazuje ciemności.

```
A quiet everyday scene told through objects and light: a low round pale birch side table beside the softly rounded arm of a pale linen armchair, on the table a small closed lidded ceramic box with a smooth matte glaze in deep forest green (#1f3d38), its lid resting firmly shut, a small plain brass key lying flat beside it, and a softly folded pale mint linen throw draped over the armchair arm, the moment just after a long night when things feel settled and kept safe, calm and private rather than secretive or anxious. At the right edge of the scene a simple small table lamp with a plain linen shade still glowing a warm sand light (#ffc88a), while the first pale clear morning daylight comes in from a window out of frame on the left, the two lights meeting gently on the tabletop, the room already bright and airy. Calm, warm editorial photograph. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed, #bbe4de) with warm sand accents (#ffc88a, #ffefdd), the deep forest green of the ceramic box (#1f3d38) as the one deep color note, and the same deep teal forest as the single darkest tone in the shadows, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field with the box and the key in crisp focus, generous empty space on the left third of the frame made of plain softly lit wall for a headline area that stays completely empty, the table, the box, the key and the lamp grouped inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, reassuring mood, premium interior photography. No text, no letters, no handwriting, no numbers, no engraving, no monogram, no ornament on the box, no key tag, no label, no padlock, no chains, no logos, no brand marks, no watermark, no AI logos, no robots, no chatbot icons, no speech bubbles, no glowing circuits, no microphones, no phone, no smartphone, no laptop, no tablet, no screens of any kind, no application interface, no paper, no notebook, no envelope, no pen, no mug, no cup, no people, no hands, no faces, no clinical or medical objects, no pills, no clutter, no night darkness, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo stress or despair poses.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`
(zostawia prawe 75% szerokości). Lewa trzecia kadru to jasna, pusta ściana, stolik
z pudełkiem i lampa siedzą w prawych dwóch trzecich. Po generacji sprawdź, czy pudełko nie
zaczyna się bliżej niż 30% szerokości od lewej krawędzi. Jeśli tak, regeneruj z `-Force`.

**`hero_image_alt`:** "A small closed forest green ceramic box with a little brass key beside it on a side table at dawn"
(ZMIENIONY wobec kolejki: stary alt opisywał abstrakcyjny dymek, którego w obrazie nie ma;
pole `hero_image_alt` i `hero_prompt` w
`blog/queue/2026-10-09_is-it-safe-to-talk-to-ai-about-mental-health.json` zaktualizowane).

**Kontrola po generacji (odrzuć render, jeśli):** na pudełku, kluczu, lampie lub ścianie jest
jakikolwiek napis, grawer, ornament przypominający litery albo logo; pojawił się telefon,
ekran, dymek, robot, kłódka albo dłoń; pudełko jest otwarte; kadr jest ciemny i nocny zamiast
jasnego świtu; zieleń pudełka przeszła w czerń albo w nasycony szmaragd; cienie są czarne
zamiast ciemnej zieleni.

**Generacja:** `blog/images/is-it-safe-to-talk-to-ai-about-mental-health/PROMPT.md` (komenda LIVE).
