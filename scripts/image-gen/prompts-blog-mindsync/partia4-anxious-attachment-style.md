# Partia 4 / 03: anxious-attachment-style

**Wpis:** „Asking Again Won't Change the Answer: Living With an Anxious Attachment Style"
(drip 2026-09-28, zamyka partię). **Wariant:** codzienny moment (`hero-01-codzienny-moment.md`).

**Dlaczego ta scena:** kąt wpisu brzmi „radar jest prawdziwy, ale nie musisz za nim iść",
czyli chodzi o chwilę, w której nie sprawdzasz telefonu drugi raz. Telefon leży ekranem
w dół na pościeli i nikt po niego nie sięga, obok stoi kubek, lampka daje ciepłe światło,
a za oknem zapada spokojny, przygaszony błękit wieczoru. Ten błękit (akcent w kolorze karty
wpisu `#3c67a5`, tylko w niebie i w jednej złożonej narzucie) odróżnia kadr od bursztynowego
hero 01 i porannego turkusu hero 02.

**Różnica wobec partii 3:** hero `therapy-hangover` też ma kubek i telefon ekranem w dół,
tyle że na parapecie w słońcu późnego popołudnia. Tu scena przenosi się do sypialni, światło
pochodzi z lampki, a za oknem jest zmierzch, więc na gridzie te dwa obrazy nie wyglądają jak
duplikat. Kompozycja jest też niższa i bliższa: widać fakturę pościeli, nie wnętrze pokoju.

```
A quiet everyday scene told through objects and light: a close, low view across a softly rumpled bed with pale sand linen bedding, a plain phone lying face down on the duvet with its blank featureless back facing up, resting still and untouched, a warm ceramic mug of tea in pale mint glaze standing on a small bedside table right next to the bed, a small bedside lamp with a linen shade glowing warm honey light over the scene, a neatly folded throw in muted dusk blue (#3c67a5) in the lower right corner of the frame, and a window in the soft background on the right showing a calm dusky blue evening sky, blurred and without any view of buildings. Calm, warm editorial photograph in soft evening lamplight, restful and quiet rather than lonely or sad, a moment of leaving the phone alone. Warm lamplight dominant: warm sand (#ffc88a, #ffefdd) and honey tones on the bedding, pale mint white (#f6fffd) and aqua (#dbf0ed) on the mug and the lampshade edges, muted dusk blue (#3c67a5) used only in the evening sky and the folded throw, and deep teal forest (#1f3d38) as the single darkest tone in the shadows, never pure black. Airy light surfaces, hairline shadows, gentle shallow depth of field with the phone and mug in focus, generous calm space on the left of the frame made of soft blurred bedding for a headline area that stays completely empty, the phone slightly right of center and the mug, lamp and window inside the right two thirds of the frame. Wide 16:9 landscape composition (1600x900), main subject off center to the right, settled and reassuring mood, premium interior photography. No text, no letters, no numbers, no logos, no brand marks or camera branding on the phone, no watermark, no visible phone screen, no glowing screen, no notification light, no readable screen of any kind, no application interface, no people in the frame, no hands, no faces, no silhouettes, no second pillow dent suggesting an absent partner, no crumpled tissues, no crying, no clinical or medical objects, no pills, no night darkness, no dark dramatic tones, no harsh contrast, no neon colors outside the palette, no stock photo loneliness or despair poses.
```

**Kadr na wariant 800x600 (thumbnail na gridzie /blog):** skrypt robi crop `gravity East`,
czyli zostawia prawe 75% szerokości i wycina lewą ćwiartkę. Lewa ćwiartka to miękko rozmyta
pościel pod nagłówek; telefon leży lekko na prawo od środka, kubek, lampka i okno siedzą
w prawych dwóch trzecich. Po generacji sprawdź, czy telefon nie wylądował bliżej niż 30%
szerokości od lewej krawędzi. Jeśli tak, regeneruj, bo miniatura straci główny przedmiot.

**`hero_image_alt`:** „A phone lying face down on bedding next to a mug in warm evening lamplight" (bez zmian, zgodny z kolejką)

**Kontrola po generacji:** odrzuć render z telefonem ekranem do góry albo z poświatą spod
telefonu, z logo producenta, z człowiekiem lub jego zarysem, z nocną ciemnością zamiast
zmierzchu i taki, w którym błękit zalał cały kadr zamiast zostać akcentem w oknie i narzucie.
Scena ma czytać się jako spokojny wieczór, nie jako samotność.

**Generacja (podgląd suchy, z katalogu `scripts/image-gen/`):** `powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 -PromptFile .\prompts-blog-mindsync\partia4-anxious-attachment-style.md -OutDir ..\..\blog\images\anxious-attachment-style -Slug hero`
