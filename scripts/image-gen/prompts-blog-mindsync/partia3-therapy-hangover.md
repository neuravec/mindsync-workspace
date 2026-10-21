# Partia 3 / 01: therapy-hangover

**Wpis:** „Why You Feel Worse After a Therapy Session (the Therapy Hangover)" (drip 2026-09-21,
klaster 2, wejście partii). **Wariant:** codzienny moment (`hero-01-codzienny-moment.md`).

**Dlaczego ta scena:** wpis rozdziela trzy różne rzeczy nazywane jednym słowem i wprost nie
sprzedaje tezy „gorzej znaczy lepiej", więc hero nie może być obrazkiem cierpienia. Parapet
z kubkiem, telefonem odłożonym ekranem w dół i zsuniętym kocem pokazuje dokładnie to, co wpis
zaleca na godzinę po sesji: wieczór, w którym nic nie musi się wydarzyć. Późne popołudniowe
światło zamiast poranka odróżnia ten kadr od pozostałych dwóch hero partii i od porannych
scen partii 2, a jednocześnie trzyma tę samą paletę i to samo miękkie światło.

```
A quiet everyday scene told through objects and light: a wide pale windowsill in a calm living room, holding a warm ceramic mug of tea with a faint wisp of steam, a plain phone lying face down beside it with its blank featureless back facing up, and a soft mint wool blanket slipped to one side with its folds falling over the edge of the sill, a sheer linen curtain half drawn so low late afternoon sun falls across the sill in long gentle bands, the room behind settling into soft deep teal shadow rather than black. Calm, warm editorial photograph in low golden late afternoon light, restful and ordinary rather than sad or cinematic, an evening where nothing has to happen. Muted palette anchored in pale mint white (#f6fffd) and aqua (#dbf0ed), with warm sand and amber accents (#ffc88a, #ffefdd) and deep teal forest (#1f3d38) as the single darkest tone, never pure black. Airy almost white surfaces, hairline shadows, gentle shallow depth of field, generous quiet space on the left of the frame for a headline area that stays completely empty, every object placed inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, settled and reassuring mood, premium interior photography. No text, no letters, no numbers, no logos, no brand marks or camera branding on the phone, no watermark, no visible phone screen, no readable screen of any kind, no laptop, no application interface, no visible faces, no people in the frame, no crumpled tissues, no crying, no clinical or medical objects, no pills, no therapy couch, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo despair poses.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`, czyli
zostawia prawe 75% szerokości kadru i wycina lewą ćwiartkę. Kompozycja jest pod to napisana:
kubek, telefon i koc mają siedzieć w prawych dwóch trzecich, a lewa ćwiartka to samo światło
i pusta ściana pod nagłówek. Po generacji sprawdź na renderze, czy kubek nie wylądował bliżej
niż 30% szerokości od lewej krawędzi. Jeśli wylądował, regeneruj zamiast ratować kadrowaniem,
bo crop centralny wpuści pustą ścianę w środek miniatury.

**`hero_image_alt`:** „A mug of tea and a face down phone on a windowsill, a blanket slipped to one side in late afternoon light"

**Kontrola po generacji:** odrzuć każdy render, na którym telefon leży ekranem do góry, widać
logo producenta, w kadrze jest człowiek albo scena wygląda na noc i przygnębienie. To ma być
spokojny wieczór, nie zapaść.

**Generacja (podgląd suchy, z katalogu `scripts/image-gen/`):** `powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 -PromptFile .\prompts-blog-mindsync\partia3-therapy-hangover.md -OutDir ..\..\blog\images\therapy-hangover -Slug hero`
