#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Post-process renderów ikon kategorii (Nano Banana Pro) -> WebP 256 do kafli home.
Dla kazdego kat-*-raw.png z _master/:
  1) splaszcza na bialym tle,
  2) przycina do bboxa OBIEKTU (prog odcina delikatny cien),
  3) padduje do kwadratu, wysrodkowany, z marginesem -> spojny rozmiar w serii,
  4) resize 256x256 LANCZOS, zapis WebP q90 do assets/icons/<name>.webp.
"""
import os, glob
from PIL import Image, ImageChops

ROOT   = r"C:\Users\mikol\OneDrive\Desktop\plasmet\shopper-sklep"
MASTER = os.path.join(ROOT, r"assets\icons\_master")
OUT    = os.path.join(ROOT, r"assets\icons")
SIZE   = 256
MARGIN = 0.12          # margines z kazdej strony -> obiekt ~76% kadru
THRESH = 28            # prog "nie-biel": odcina delikatny cien, lapie obiekt

os.makedirs(OUT, exist_ok=True)
white = (255, 255, 255)

for p in sorted(glob.glob(os.path.join(MASTER, "kat-*-raw.png"))):
    name = os.path.basename(p).replace("-raw.png", "")
    im = Image.open(p).convert("RGBA")
    bg = Image.new("RGBA", im.size, white + (255,))
    im = Image.alpha_composite(bg, im).convert("RGB")

    diff = ImageChops.difference(im, Image.new("RGB", im.size, white)).convert("L")
    mask = diff.point(lambda x: 255 if x > THRESH else 0)
    bbox = mask.getbbox()
    if bbox:
        im = im.crop(bbox)

    w, h = im.size
    side = max(w, h)
    canvas = int(round(side / (1 - 2 * MARGIN)))
    sq = Image.new("RGB", (canvas, canvas), white)
    sq.paste(im, ((canvas - w) // 2, (canvas - h) // 2))
    sq = sq.resize((SIZE, SIZE), Image.LANCZOS)

    out = os.path.join(OUT, name + ".webp")
    sq.save(out, "WEBP", quality=90, method=6)
    kb = round(os.path.getsize(out) / 1024, 1)
    print(f"{name}.webp  {SIZE}x{SIZE}  {kb} KB  (bbox={bbox})")

print("OUT:", OUT)
