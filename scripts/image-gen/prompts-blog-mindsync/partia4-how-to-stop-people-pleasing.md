# Partia 4 / 02: how-to-stop-people-pleasing

**Wpis:** „'No' Is Enough on Its Own: How to Stop People Pleasing" (drip 2026-09-27, środek
partii). **Wariant:** codzienny moment (`hero-01-codzienny-moment.md`).

**Dlaczego ta scena:** wpis dotyczy chwili tuż przed odpowiedzią na czyjąś prośbę, kiedy
jeszcze można odpisać krótko. Dłoń trzyma telefon nad kubkiem, ekranem od widza, i nic się
jeszcze nie stało: to jest ta pauza. Zamknięty papierowy planer w tle mówi „mój czas" bez
pokazywania czegokolwiek, co da się przeczytać. Dominanta to chłodny poranny turkus i aqua,
w zgodzie z kolorem karty wpisu `#339499`, więc na gridzie ten kadr odcina się od bursztynowego
hero 01 i wieczornego hero 03.

**Odejście od briefu (lekcja 1 z partii 3):** brief chciał planer „z kilkoma skreśleniami".
Skreślone wpisy to pismo, a pozytywne zamówienie pisma model wykona mimo zakazu tekstu. Planer
jest więc zamknięty, z płócienną okładką i tasiemką zakładki. Alt z kolejki nadal jest prawdziwy
(„next to a paper planner"), więc nie wymaga zmiany.

```
A quiet everyday scene told through objects and light: a pale kitchen table by a window in soft cool morning light, a relaxed hand entering the frame from the right edge and holding a plain phone upright just above a ceramic mug of tea, the phone turned so that only its plain featureless back faces the viewer, the hand calm and unhurried with no tension in the fingers, the mug in a deep lagoon teal glaze (#339499) with a faint wisp of steam, and slightly behind them a closed paper planner with a smooth pale aqua linen cover and a thin sand colored ribbon bookmark lying loose on the table, a small sprig of green eucalyptus in a glass beside it. Calm, fresh editorial photograph in soft cool morning light with a gentle warm touch where the sun reaches the table, a pause before answering rather than a moment of stress. Cool teal and aqua dominant palette: lagoon teal (#339499), aqua (#dbf0ed, #bbe4de) and pale mint white (#f6fffd), with warm sand accents (#ffc88a, #ffefdd) on the ribbon and in the sunlight, and deep teal forest (#1f3d38) as the single darkest tone, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field with the hand and mug in sharp focus and the planner softly blurred, generous empty space on the left of the frame for a headline area that stays completely empty, the hand, phone and mug placed inside the right two thirds of the frame, the hand coming in from the right edge only, wrist and a soft knit sleeve in muted sand visible, nothing else of the person. Wide 16:9 landscape composition (1600x900), main subject off center to the right, settled and reassuring mood, premium lifestyle photography. No text, no letters, no numbers, no handwriting, no writing on the planner cover, no logos, no brand marks or camera branding on the phone, no watermark, no visible phone screen, no readable screen of any kind, no notifications, no application interface, no faces, no full person, no second hand, no rings with engravings, no clutter, no crumpled paper, no clinical or medical objects, no pills, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo stress or despair poses.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`,
czyli zostawia prawe 75% szerokości i wycina lewą ćwiartkę. Dłoń wchodzi z prawej krawędzi,
kubek i planer stoją w prawych dwóch trzecich, lewa ćwiartka to jasny blat i okno bez
przedmiotów. Po generacji sprawdź, czy planer nie odjechał do lewej ćwiartki. Jeśli tak,
w miniaturze zostanie urwany, więc regeneruj.

**`hero_image_alt`:** „A hand holding a phone above a mug next to a paper planner in soft morning light" (bez zmian, zgodny z kolejką)

**Kontrola po generacji:** odrzuć render z widocznym ekranem telefonu, z logo na obudowie,
z pismem albo liniami tekstu na planerze, z twarzą lub drugą dłonią w kadrze, i taki,
w którym dłoń wygląda na zaciśniętą lub drżącą. To ma być spokojna pauza, nie napięcie.

**Generacja (podgląd suchy, z katalogu `scripts/image-gen/`):** `powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 -PromptFile .\prompts-blog-mindsync\partia4-how-to-stop-people-pleasing.md -OutDir ..\..\blog\images\how-to-stop-people-pleasing -Slug hero`
