# Partia 3 / 03: how-to-name-what-you-feel

**Wpis:** „How to Name What You Are Feeling When All You Have Is Bad" (drip 2026-09-23,
klaster 3, zamyka partię). **Wariant:** miękka abstrakcja (`hero-02-abstrakcja.md`).

**Dlaczego ta scena:** kąt wpisu brzmi „precyzja bierze się z kontekstu, nie ze słownika",
więc hero pokazuje samo przejście od nieokreślonego do wyraźnego, a nie zestaw nazwanych
kategorii. Jedno rozmyte pole rozdziela się na kilka mniejszych form o czystych krawędziach:
to ten sam ruch, co cztery pytania w sekcji praktycznej. Rozdzielenie idzie w prawo, więc
czyta się w tym samym kierunku co wzniesienie w hero wpisu 02 i wspólnie z nim buduje
rodzeństwo, choć motyw jest inny.

⛔ **Zakaz kategoryczny z briefu:** żadnego koła emocji ani niczego, co je przypomina. Wpis
w całości argumentuje, że koło emocji nie rozwiązuje problemu, więc koło w hero podważyłoby
tezę tekstu. Zakaz jest w bloku rozpisany na kilka wariantów, bo model lubi zamykać emocje
w okrąg.

```
Soft abstract composition suggesting one vague feeling resolving into several precise ones: a single large soft cloudlike field with blurred undefined edges sitting a little left of center in pale aqua (#dbf0ed) and lagoon (#bbe4de), gradually separating towards the right into several smaller rounded forms with clean crisp edges, each of the smaller forms in its own tone of the palette, warm sand (#ffc88a), sand beige (#ffefdd) and one small soft coral (#ff9f8a), the whole movement reading from left to right as something diffuse becoming something clearly outlined, thin hairline contours of deep teal forest (#1f3d38) drawn only around the two clearest small forms, everything floating on an almost white pale mint white (#f6fffd) ground. Matte, grainless, premium editorial illustration in a soft flat vector style with gently blurred gradients. Palette strictly limited to pale mint white (#f6fffd), aqua (#dbf0ed, #bbe4de), warm sand (#ffc88a, #ffefdd), soft coral (#ff9f8a) used sparingly, and deep teal forest (#1f3d38) as the single darkest tone. Light and airy, generous negative space, the composition sitting low in the frame with the whole upper third left as an almost empty pale mint field for a headline, the large soft field placed about a third of the way in from the left edge so the entire separation sits inside the right three quarters of the frame and nothing important touches the left edge. Wide 16:9 landscape composition (1600x900), calm, quiet and reassuring. No text, no letters, no numbers, no labels, no word clouds, no speech bubbles, no emotion wheel, no feelings wheel, no color wheel, no pie chart, no circular diagram, no radial segments, no spectrum strip, no icons, no emoji, no smiley shapes, no faces, no human figures, no logos, no watermark, no medical symbols, no brain imagery, no neon colors, no dark dramatic tones, no busy patterns, no photographic realism.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`,
zostawia prawe 75% szerokości i wycina lewą ćwiartkę. Prompt trzyma duże rozmyte pole około
jednej trzeciej szerokości od lewej, więc po cropie w miniaturze zostaje i ono, i rozdzielone
formy, czyli cała treść obrazu. Puste jest za to górne pasmo, a nie lewa krawędź, bo tu
kompozycja siedzi nisko. Jeśli render wypchnie rozmyte pole na samą lewą krawędź, miniatura
pokaże wyłącznie gotowe małe formy i zgubi sens „z jednego na kilka", czyli regenerujemy.

**`hero_image_alt`:** „A single blurred mint shape separating into several smaller, clearer forms in sand and coral"

**Kontrola po generacji:** odrzuć render z jakimkolwiek okręgiem podzielonym na wycinki,
z paskiem widma, z podpisami przy kształtach i ze wszystkim, co wygląda na ikonę emocji.

**Generacja (podgląd suchy, z katalogu `scripts/image-gen/`):** `powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 -PromptFile .\prompts-blog-mindsync\partia3-how-to-name-what-you-feel.md -OutDir ..\..\blog\images\how-to-name-what-you-feel -Slug hero`
