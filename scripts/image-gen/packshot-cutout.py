#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
packshot-cutout.py — precyzyjne wycinanie tla z packshotow sklepowych (JPG na jasnym gradiencie)
pod banery na ciemnym tle.

DLACZEGO NIE FLOODFILL Z ImageMagick:
  `-fuzz N% -draw "color 0,0 floodfill"` porownuje kazdy piksel do koloru ZIARNA. Na gradiencie
  albo nie dochodzi do konca (zostaje szara plyta w ciemniejszym rogu), albo przy wiekszym fuzz
  zzera jasne fragmenty etykiety. Zostawia tez „duchy" po przezroczystym plastiku (nasadki, aplikatory).

ALGORYTM (flood z tolerancja LOKALNA — porownanie do SASIADA, nie do ziarna):
  1. ziarno = piksele krawedzi kadru (tam gdzie jest tlo),
  2. propagacja: piksel wpada do tla, jesli rozni sie od juz zaakceptowanego SASIADA mniej niz --tol
     -> gladki gradient tla i miekki cien przechodza w calosci, ostra krawedz produktu zatrzymuje flood,
  3. dziury w produkcie zasklepiamy (binary_fill_holes),
  4. wyrzucamy drobiny < --min-area (duchy po przezroczystym plastiku, artefakty JPG),
  5. erozja o --erode px zjada jasne halo po antyaliasingu,
  6. alfa wygladzona gaussem (--feather) i zaostrzona -> miekka, ale czysta krawedz,
  7. crop do bboxa + skala do --height.

UZYCIE:
  python packshot-cutout.py <in.jpg> <out.png> [--tol 0.05] [--min-area 0.0015]
                            [--erode 1] [--feather 0.7] [--height 900]
"""
import argparse

import numpy as np
from PIL import Image
from scipy import ndimage


def flood_background(a, tol, max_iter=4000):
    """Region-growing od krawedzi kadru z tolerancja wzgledem sasiada."""
    h, w = a.shape[:2]

    # roznica do sasiada w 4 kierunkach (max po kanalach RGB)
    d_up = np.zeros((h, w), np.float32)      # |p(y,x) - p(y-1,x)|
    d_dn = np.zeros((h, w), np.float32)      # |p(y,x) - p(y+1,x)|
    d_lf = np.zeros((h, w), np.float32)      # |p(y,x) - p(y,x-1)|
    d_rt = np.zeros((h, w), np.float32)      # |p(y,x) - p(y,x+1)|
    d_up[1:, :] = np.abs(a[1:, :] - a[:-1, :]).max(axis=2)
    d_dn[:-1, :] = np.abs(a[:-1, :] - a[1:, :]).max(axis=2)
    d_lf[:, 1:] = np.abs(a[:, 1:] - a[:, :-1]).max(axis=2)
    d_rt[:, :-1] = np.abs(a[:, :-1] - a[:, 1:]).max(axis=2)

    mask = np.zeros((h, w), bool)
    mask[0, :] = mask[-1, :] = True
    mask[:, 0] = mask[:, -1] = True

    for _ in range(max_iter):
        grow = np.zeros_like(mask)
        # z gory w dol: piksel (y,x) dolacza, jesli (y-1,x) jest w tle i roznica < tol
        grow[1:, :] |= mask[:-1, :] & (d_up[1:, :] < tol)
        grow[:-1, :] |= mask[1:, :] & (d_dn[:-1, :] < tol)
        grow[:, 1:] |= mask[:, :-1] & (d_lf[:, 1:] < tol)
        grow[:, :-1] |= mask[:, 1:] & (d_rt[:, :-1] < tol)
        new = grow & ~mask
        if not new.any():
            break
        mask |= new
    return mask


def cutout(src, dst, tol=0.05, min_area=0.0015, erode=1, feather=0.7, height=900, punch=False, punch_depth=None):
    raw = Image.open(src)

    # ZDJECIE MA JUZ ALFE (czesc packshotow Shopera to PNG z przezroczystoscia) -> nie wycinamy niczego
    if raw.mode in ("RGBA", "LA") or "transparency" in raw.info:
        rgba = raw.convert("RGBA")
        if np.asarray(rgba)[..., 3].min() < 250:
            out = rgba.crop(rgba.getbbox() or (0, 0, rgba.width, rgba.height))
            if height:
                out = out.resize((max(1, round(out.width * height / out.height)), height), Image.LANCZOS)
            out.save(dst)
            print(f"{src} -> {dst}  {out.width}x{out.height}px  (natywna alfa, bez wycinania)")
            return

    im = raw.convert("RGB")
    a = np.asarray(im).astype(np.float32) / 255.0
    h, w = a.shape[:2]

    bg = flood_background(a, tol)
    fg = ~bg

    # KIESZENIE TLA ZAMKNIETE W PRODUKCIE: otwory eurozawieszek, uchwyt kanistra, oczko narzedzia.
    # Flood od krawedzi tam nie wejdzie, wiec bez tego zostaja BIALE PLAMY na ciemnym banerze.
    # Wycinamy tylko to, co spelnia WSZYSTKIE trzy warunki:
    #   (a) kolor tla (jasne + nienasycone), (b) gladkie (bez nadruku/tekstu), (c) NIE styka sie z tlem
    #       zewnetrznym — inaczej ryzykowalibysmy zjedzenie jasnej powierzchni samego produktu.
    if punch and bg.any():
        lum = a.max(axis=2)
        mx, mn = a.max(axis=2), a.min(axis=2)
        sat = np.where(mx > 0, (mx - mn) / np.maximum(mx, 1e-6), 0.0)
        bg_lum = float(np.median(lum[bg]))
        cand = fg & (lum > bg_lum - 0.05) & (sat < 0.12)
        # odleglosc kazdego piksela produktu od tla zewnetrznego — kieszen musi lezec GLEBOKO w srodku,
        # inaczej punch zjada jasna/srebrna POWIERZCHNIE produktu przy jego krawedzi
        dist = ndimage.distance_transform_edt(~bg)
        min_depth = punch_depth if punch_depth is not None else max(6.0, 0.012 * min(h, w))
        lab_p, npx = ndimage.label(cand)
        min_px = max(40, int(0.00004 * h * w))
        for i in range(1, npx + 1):
            sel = lab_p == i
            if sel.sum() < min_px:
                continue
            if lum[sel].std() > 0.05:            # nadruk / tekst -> to produkt
                continue
            if dist[sel].min() < min_depth:      # przy krawedzi -> to powierzchnia produktu, nie dziura
                continue
            fg &= ~sel

    lab, n = ndimage.label(fg)
    if n > 1:
        sizes = ndimage.sum(fg, lab, range(1, n + 1))
        keep = [i + 1 for i, s in enumerate(sizes) if s >= min_area * h * w]
        fg = np.isin(lab, keep)

    if erode > 0:
        fg = ndimage.binary_erosion(fg, iterations=int(erode))

    alpha = fg.astype(np.float32)
    if feather > 0:
        alpha = ndimage.gaussian_filter(alpha, sigma=feather)
        alpha = np.clip((alpha - 0.35) / 0.45, 0, 1)

    out = Image.fromarray(
        np.dstack([np.asarray(im).astype(np.float32), alpha * 255.0]).astype(np.uint8), "RGBA"
    )
    bbox = out.getbbox()
    if bbox:
        out = out.crop(bbox)
    if height:
        out = out.resize((max(1, round(out.width * height / out.height)), height), Image.LANCZOS)
    out.save(dst)
    print(f"{src} -> {dst}  {out.width}x{out.height}px  (tlo {bg.mean()*100:.1f}% kadru)")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("src")
    ap.add_argument("dst")
    ap.add_argument("--tol", type=float, default=0.05)
    ap.add_argument("--min-area", type=float, default=0.0015)
    ap.add_argument("--erode", type=int, default=1)
    ap.add_argument("--feather", type=float, default=0.7)
    ap.add_argument("--height", type=int, default=900)
    ap.add_argument("--punch", action="store_true",
                    help="wytnij zamkniete kieszenie tla (otwory eurozawieszek, uchwyty). "
                         "UWAGA: potrafi zjesc BIALY NADRUK na etykiecie — wlaczac swiadomie "
                         "i zawsze obejrzec wynik na kontrastowym tle.")
    ap.add_argument("--punch-depth", type=float, default=None,
                    help="min. odleglosc kieszeni od tla zewnetrznego w px (domyslnie ~1.2%% krotszego boku). "
                         "Nizej = wycina tez plytsze otwory, ale rosnie ryzyko zjedzenia powierzchni produktu.")
    args = ap.parse_args()
    cutout(args.src, args.dst, args.tol, args.min_area, args.erode, args.feather, args.height,
           punch=args.punch, punch_depth=args.punch_depth)
