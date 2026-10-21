# Partia 3 / 02: how-long-therapy-takes-to-work

**Wpis:** „How Long Therapy Takes to Work, According to the Session Numbers" (drip 2026-09-22,
klaster 6). **Wariant:** miękka abstrakcja (`hero-02-abstrakcja.md`).

**Dlaczego ta scena:** wpis stawia obok siebie krzywą z badań i liczby z realnych gabinetów,
więc naturalnym językiem wizualnym jest narastanie z malejącymi przyrostami. Kluczowe jest to,
czego tu nie ma: wpis mówi wprost, że krzywa opisuje rozkład, a nie czyjś harmonogram, więc
hero nie może udawać wykresu z danymi. Stąd miękkie pola bez osi, bez siatki i bez ani jednej
cyfry. Warstwy w tle czytają się jako kolejne tygodnie, a nie jako słupki.

⛔ **Największe ryzyko tego promptu:** model bardzo chętnie dorysowuje osie, podziałkę i liczby,
gdy wyczuje wykres. Zakaz jest w bloku wypisany wprost i rozbity na osobne przypadki, bo samo
„no charts" nie wystarcza.

⛔ **Wyjątek od reguły hairline, nie przeoczenie. Nie cofaj tego w partii 4.** Brand doc każe
używać cienkich hairline'ów zamiast cieni, ale w TYM jednym obrazie hairline nie występuje
w ogóle. Pierwsza wersja promptu zamawiała cienki łuk `#1f3d38` biegnący pod zboczem i mały
koralowy punkt w miejscu wypłaszczenia. Razem czytają się jako linia z markerem danych, czyli
dokładnie jako wykres, którego reszta promptu zabrania. Model rozstrzyga taką sprzeczność na
korzyść instrukcji pozytywnej, więc lista zakazów tego nie uratowała: trzy rendery, dwa na
`gemini-2.5-flash-image` i jeden na `gemini-3-pro-image`, dały tę samą strukturę. Zbocze buduje
się tu wyłącznie z nachodzących pól, a `#1f3d38` zostaje w palecie jako najciemniejszy ton
w dolnej warstwie, nigdy jako kreska.

```
Soft abstract composition suggesting slow progress accumulating over time: a gentle ascending slope built from a handful of overlapping translucent rounded fields that rise from the lower middle of the frame towards the right, each step smaller than the one before it, so the rise eases into an almost level calm band near the right edge, the rising fields in warm sand (#ffc88a) fading into sand beige (#ffefdd), their edges soft and slightly blurred where they overlap, the whole slope resting over wide soft horizontal strata of aqua (#dbf0ed) and lagoon (#bbe4de) that read as quiet weeks of light passing rather than as measured bands, deep teal forest (#1f3d38) present only as the deepest tone inside the lowest stratum and never as a line, a wide diffuse warm coral (#ff9f8a) glow sitting low in the background near the right edge, blurred into the strata and never a defined round shape. The slope is built from overlapping soft fields only: it carries no outline, no contour, no stroke, no hairline, no thin arc, no edge line of any kind running along it or underneath it, and no bright point, dot, marker, spark or highlight anywhere on it or near its upper edge. Matte, grainless, premium editorial illustration in a soft flat vector style with gently blurred gradients. Palette strictly limited to pale mint white (#f6fffd), aqua (#dbf0ed, #bbe4de), warm sand (#ffc88a, #ffefdd), soft coral (#ff9f8a) used sparingly and only as diffuse background light, and deep teal forest (#1f3d38) as the single darkest tone. Light and airy, generous negative space, the upper left third of the frame left as an almost empty pale mint field for a headline, the slope starting about a third of the way in from the left edge and the point where it eases sitting near the middle of the frame, so nothing important touches the left edge. Wide 16:9 landscape composition (1600x900), calm, quiet and reassuring. No text, no letters, no numbers, no digits, no percentages, no dates, no charts, no graphs, no bar charts, no line graphs, no curves drawn as lines, no continuous lines of any kind, no outlines, no strokes, no axes, no axis lines, no gridlines, no tick marks, no scale marks, no data points, no dots, no dots connected by a line, no arrows, no calendars, no clocks, no hourglasses, no icons of any kind, no logos, no watermark, no medical symbols, no brain imagery, no neon colors, no dark dramatic tones, no busy patterns, no photographic realism.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`,
zostawia prawe 75% szerokości i wycina lewą ćwiartkę. Dlatego prompt każe zacząć wzniesienie
dopiero około jednej trzeciej szerokości, a miejsce, w którym krzywizna się wypłaszcza, trzyma
w okolicach środka kadru. Po cropie miniatura ma nadal pokazywać i narastanie, i wypłaszczenie.
Jeśli render wypchnie całe wzniesienie na lewą połowę, miniatura zostanie z samym płaskim
pasem i trzeba regenerować, a nie kadrować ręcznie.

**`hero_image_alt`:** „Layered sand and mint shapes forming a gentle rising slope that levels off towards the right"

**Kontrola po generacji:** odrzuć render, na którym widać cokolwiek z gramatyki wykresu, czyli
oś, podziałkę, kropki połączone linią, strzałkę albo znaki, które udają cyfry. Ten wpis jest
o uczciwości wobec danych, więc hero udający dane jest sprzeczny z treścią.

**Warunek odrzucenia numer jeden przy tym wpisie:** jakakolwiek ciągła linia biegnąca wzdłuż
zbocza albo pod nim. Dotyczy to również linii bardzo jasnej, cienkiej jak włos i takiej,
która wygląda tylko na krawędź pola. Jedna kreska wzdłuż zbocza wystarczy, żeby cały obraz
przeczytał się jako wykres. Tak samo odrzucamy każdy zwarty jasny punkt na zboczu lub przy
jego górnej krawędzi, bo w tym układzie czyta się jako marker danych. Rozmyta koralowa poświata
nisko w tle jest w porządku, okrągła plamka nie. Samo zbocze z ostatnich prób wychodzi dobrze,
więc przy odrzuceniu regeneruj z `-Force` na tym samym promptcie, nie przepisuj kompozycji.

**Generacja (podgląd suchy, z katalogu `scripts/image-gen/`):** `powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 -PromptFile .\prompts-blog-mindsync\partia3-how-long-therapy-takes-to-work.md -OutDir ..\..\blog\images\how-long-therapy-takes-to-work -Slug hero`
