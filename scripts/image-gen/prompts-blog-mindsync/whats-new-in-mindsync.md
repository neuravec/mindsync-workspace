# Wpis produktowy / whats-new-in-mindsync

**Wpis:** "What's New in MindSync: Your Whole Therapy Week on One Screen" (slug `whats-new-in-mindsync`,
kategoria MindSync Tips). Nowa wersja aplikacji: ekran startowy z kolorowymi kafelkami, plan
pierwszego tygodnia, nowe karty przed i po terapii, Character z mocnymi stronami, Orca jako
asystent AI między sesjami. **Wariant:** codzienny moment (`hero-01-codzienny-moment.md`),
martwa natura bez ludzi. **Model:** `gemini-3-pro-image`, 16:9, 2K.

**Dlaczego ta scena:** tytuł obiecuje "cały tydzień terapii na jednym ekranie", a najbardziej
widoczna nowość to start z kolorowymi kafelkami. Hero pokazuje to przedmiotem, nie interfejsem:
płytka drewniana taca (jedno miejsce na wszystko) z świeżo ułożonym zestawem małych ręcznie
robionych płytek ceramicznych o zaokrąglonych rogach, w kilku rozmiarach, w glazurach z palety
marki. Jedna koralowa płytka leży jeszcze obok tacy, lekko krzywo, jakby ktoś przed chwilą ją
odłożył: to "nowe", bez dłoni w kadrze. Kubek herbaty z parą daje poranek i codzienność.
Płytki to fizyczne, matowe, nierówne obiekty z cieniem i fakturą, więc nie czytają się jako
zrzut ekranu, a jednocześnie rymują się z kafelkami nowego ekranu startowego.

Odróżnienie od serii: parapet z kubkiem, zamkniętym notatnikiem i telefonem ekranem w dół
już jest w how-to-use-mindsync, what-to-do-between-therapy-sessions, therapy-hangover
i journaling-vs-voice-notes, dlatego tu nie ma parapetu, notatnika ani telefonu. Jest stół,
taca i kolor płytek jako główny akcent. Światło z lewej i z tyłu (kontra na glazurach), kąt
3/4 z lekkiej góry, nigdy prosto z góry (flat lay siatki kwadratów za bardzo przypomina
makietę UI). Orca, Character i AI zostają w tekście wpisu, nie w pikselach: żadnej figurki
orki, robota ani dymka.

Ryzyko: płytki kuszą model do cyfr (kalendarz), liter (Scrabble, mahjong), ikon (siatka
"aplikacji") albo wzorów malowanych; siatka może też zjechać w kafelki na ścianie lub
podłodze z fugą. Drugie ryzyko: ciemne płytki (teal, forest) zdominują kadr, dlatego prompt
ogranicza je do jednej-dwóch sztuk. Negatywy wymieniają to wprost.

```
A quiet everyday scene told through objects and light: a wide pale oak table on a fresh calm morning, and on it a shallow rounded tray of pale birch wood holding a neat, freshly arranged set of small loose handmade ceramic tiles with softly rounded corners, in two or three different sizes fitted together in a calm loose grid like a tidy plan for the week ahead, each tile plain and smooth in a soft matte glaze, mostly pale aqua (#dbf0ed), lagoon mint (#bbe4de), warm sand (#ffc88a), sand beige (#ffefdd) and soft coral (#ff9f8a), with only one or two tiles in mid teal (#339499) and deep forest green (#1f3d38). One last coral tile rests on the table just in front of the tray, slightly askew, as if it had only just been set down. Slightly behind the tray on its right side stands a plain off white ceramic mug of tea with a faint wisp of steam. The whole arrangement feels new, ordered and unhurried, a small fresh start rather than a chore. Seen from a slightly raised three quarter angle, about thirty five degrees above the tabletop, never straight overhead. Soft clear morning daylight from a tall window out of frame behind and to the left, filtered through a sheer curtain, glancing across the glazes so each tile shows a gentle sheen and the uneven handmade texture of its surface, soft short shadows falling toward the front right. Calm, warm editorial photograph. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed) with warm sand accents (#ffc88a, #ffefdd), the tiles as the only color notes in the scene, chalky and gentle rather than saturated, and deep teal forest (#1f3d38) as the single darkest tone in the shadows, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field with the tiles in crisp focus and the pale wall behind softly blurred, generous empty space on the left third of the frame made of plain sunlit tabletop and pale wall for a headline area that stays completely empty, the tray, the loose tile and the mug grouped inside the right two thirds of the frame with a little air before the right edge. Wide 16:9 landscape composition (1600x900), main subject off center to the right, reassuring mood, premium interior photography. No text, no letters, no handwriting, no numbers, no dates, no symbols, icons, drawings or painted patterns on the tiles, no calendar, no planner, no game tiles, no Scrabble or mahjong tiles, no dominoes, no dice, no tiled wall, no tiled floor, no grout, no labels, no logos, no brand marks, no watermark, no phone, no smartphone, no tablet, no laptop, no screens of any kind, no application interface, no paper, no notebook, no sticky notes, no pen, no people, no hands, no faces, no animals, no figurines, no clinical or medical objects, no pills, no clutter, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo despair poses.
```

**Negative / avoid (wbudowane w prompt, Gemini nie ma osobnego pola negative):**
- tekst w każdej postaci: litery, cyfry, daty, pismo odręczne, etykiety, logo, znak wodny;
- cokolwiek na płytkach: symbole, ikony, rysunki, wzory malowane (płytki mają być gładkie, jednobarwne);
- skojarzenia, w które model lubi zjechać: kalendarz, planer, Scrabble, mahjong, domino, kości,
  kafelki na ścianie lub podłodze z fugą;
- urządzenia i UI: telefon, tablet, laptop, jakikolwiek ekran, interfejs aplikacji;
- papier: kartki, notatnik, karteczki, długopis (model wpisuje na nie czytelny tekst);
- ludzie, dłonie, twarze, zwierzęta, figurki (w tym orka);
- klinika i dramat: pigułki, obiekty medyczne, ciemne kadry, ostry kontrast, neon, pozy rozpaczy, bałagan.

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** `gemini-generate.ps1` robi crop
`gravity East` (`-resize 1200x900^ -extent 1200x900`), czyli zostawia prawe 75% szerokości
i pełną wysokość. Lewa trzecia kadru to pusta, jasna powierzchnia stołu i ściany pod nagłówek;
taca, luźna płytka i kubek siedzą w prawych dwóch trzecich, więc w miniaturze lądują
w środku kadru 4:3. Po generacji sprawdź na `hero-1600x900.jpg`, czy lewa krawędź tacy nie
zaczyna się bliżej niż 30% szerokości od lewej krawędzi i czy kubek nie dotyka prawej
krawędzi. Jeśli tak, regeneruj z `-Force` zamiast ratować kadrowaniem.

**`hero_image_alt` (EN, 114 znaków):** "Rounded ceramic tiles in mint, sand, coral and teal arranged in a wooden tray beside a mug of tea in morning light"

Jeśli w renderze nie ma żadnej płytki w turkusie, alt bez "and teal": "Rounded ceramic tiles in
mint, sand and coral arranged in a wooden tray beside a mug of tea in morning light".
Alt opisuje obraz, nie funkcje aplikacji (kafelki nie udają ekranu, więc alt też nie).

**Pliki wyjściowe:** `blog/images/whats-new-in-mindsync/hero-raw.png`, `hero-1600x900.webp`
(budżet 150 KB), `hero-1600x900.jpg`, `hero-800x600.webp` (budżet 90 KB), `hero-800x600.jpg`.
W kolejce: `"hero_prompt": "scripts/image-gen/prompts-blog-mindsync/whats-new-in-mindsync.md"`.

**Kontrola po generacji (odrzuć render, jeśli):** na którejkolwiek płytce, tacy albo kubku jest
napis, cyfra, ikona, rysunek lub wzór przypominający litery; płytki wyglądają jak siatka ikon
aplikacji albo kafelki przyklejone do ściany lub podłogi; pojawił się telefon, ekran, papier,
notatnik, dłoń, figurka albo zwierzę; kadr jest zrobiony prosto z góry jak flat lay; ciemne
płytki dominują i kadr robi się ciężki; kolory są nasycone zamiast kredowych; cienie są czarne
zamiast ciemnej zieleni; taca zaczyna się bliżej niż 30% od lewej krawędzi.

**Generacja (PowerShell, LIVE, płatna ~0.04 USD; bez `-DryRun:$false` skrypt robi tylko podgląd):**
`$env:PATH = "C:\Program Files\ImageMagick-7.1.2-Q16-HDRI;" + $env:PATH; & "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\gemini-generate.ps1" -PromptFile "C:\Users\mikol\Notebooks\MindSync\Heroku\scripts\image-gen\prompts-blog-mindsync\whats-new-in-mindsync.md" -OutDir "C:\Users\mikol\Notebooks\MindSync\Heroku\blog\images\whats-new-in-mindsync" -Slug "hero" -Model "gemini-3-pro-image" -DryRun:$false`
