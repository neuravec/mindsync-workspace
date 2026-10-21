#!/usr/bin/env python3
# Konwersja wyrenderowanych banerow PNG -> WebP (PIL). ImageMagick niedostepny.
import glob, os
from PIL import Image

d = os.path.join(os.path.dirname(__file__), "..", "..", "szablon", "design-claude", "strona-glowna-2026-06", "banery")
d = os.path.abspath(d)
for p in sorted(glob.glob(os.path.join(d, "*.png"))):
    im = Image.open(p).convert("RGB")
    out = p[:-4] + ".webp"
    # quality 82, method 6 (najlepsza kompresja); banery sa nieprzezroczyste (RGB)
    im.save(out, "WEBP", quality=82, method=6)
    kb = os.path.getsize(out) // 1024
    print(f"{os.path.basename(out):42s} {kb} KB  ({im.width}x{im.height})")
    os.remove(p)  # PNG = produkt posredni
print("OK - WebP gotowe w:", d)
