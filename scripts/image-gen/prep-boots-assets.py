#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
prep-boots-assets.py – rozbiera gotowce Milwaukee „Kampania Obuwie" na elementy skladowe,
z ktorych banery PLASMET (web 1920x680 + mobile 1080x1350) sklada sie w HTML.

DLACZEGO ROZBIERAC, A NIE SKALOWAC GOTOWIEC:
  Gotowce maja proporcje 1.91:1 (1200x628) i 1:1 (1080x1080), a sklep potrzebuje 2.82:1 i 4:5.
  Rozciagniecie zdeformowaloby but i czapke, a wtopiony tekst po przeskalowaniu rozjechalby sie
  wzgledem kadru (za maly naglowek na 1920 px). Dlatego: zdjecia wycinamy, typografie skladamy
  na nowo w Barlow (ostra, poprawne ogonki), a kompozycje ukladamy pod kazdy format osobno.

CO ROBI (zrodla: assets/banner/boots_promo_13082026/):
  1. bg-tex.jpg   – czysty fragment tekstury ziemi (kwadrat x360..1080, y0..215), bez tekstu i produktow
  2. boot.png     – blok z butem z kadru 1200x628 (tam but jest NA WIERZCHU czerwonego paska,
                    w kadrze 1:1 pasek go przykrywa). Maska schodkowa omija wtopiony tekst:
                    gorna, wezsza czesc (cholewka) + szersza dolna. Krawedzie wygaszone (feather),
                    wiec blok wtapia sie w ciemne tlo banera zlozone z tej samej tekstury.
  3. cap.png      – czapka wycieta z alfa (jasny obiekt na ciemnym tle + odciecie czerwieni paska)
  4. logo-mil.png – bialy znak Milwaukee z kafla (maska bieli) -> czerwony kafel rysuje HTML

WYNIK: assets/banner/AI_creations/src/img/boots/
UZYCIE: python prep-boots-assets.py
"""
import os

import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
SRC = os.path.join(ROOT, 'assets', 'banner', 'boots_promo_13082026')
OUT = os.path.join(ROOT, 'assets', 'banner', 'AI_creations', 'src', 'img', 'boots')
WIDE = os.path.join(SRC, '26_07_MILWAUKEE_Kampania_Obuwie_reformaty_1200x628.jpg')
SQ = os.path.join(SRC, '26_07_MILWAUKEE_Kampania_Obuwie_reformaty_1080x1080.jpg')

os.makedirs(OUT, exist_ok=True)


def load(p):
    return Image.open(p).convert('RGB')


def feather_mask(mask, radius):
    """Rozmycie maski 0/255 -> miekka krawedz."""
    return Image.fromarray(mask).filter(ImageFilter.GaussianBlur(radius))


def kill_red_fringe(rgb, mask, band=9):
    """
    Zdejmuje czerwona obwodke, ktora zostaje po krawedzi stykajacej sie z czerwonym paskiem.
    Bez tego element da sie polozyc TYLKO na czerwieni; po zdjeciu obwodki kompozycja jest wolna.
    Dziala wylacznie w waskim pasie przy krawedzi maski, wiec czerwone akcenty w srodku produktu zostaja.
    """
    # pas po OBU stronach krawedzi – czerwien siedzi takze w strefie feather, tuz POZA maska binarna
    mb = mask.astype(bool)
    edge = ndimage.binary_dilation(mb, np.ones((band, band))) & ~ndimage.binary_erosion(mb, np.ones((band, band)))
    r, g, b = rgb[:, :, 0], rgb[:, :, 1], rgb[:, :, 2]
    fringe = edge & (r - g > 45) & (r - b > 35)
    if fringe.any():
        gray = (0.45 * r + 0.35 * g + 0.20 * b)[fringe]      # zachowaj jasnosc, zabij nasycenie
        for c in range(3):
            rgb[:, :, c][fringe] = gray
    return rgb


# ---------------------------------------------------------------- 1. tekstura tla
def make_bg_tex():
    sq = load(SQ)
    tex = sq.crop((360, 0, 1080, 215))          # czysty kawalek ziemi (bez logo/tekstu/produktow)
    tex.save(os.path.join(OUT, 'bg-tex.jpg'), quality=94)
    print('bg-tex.jpg', tex.size)


# ---------------------------------------------------------------- 2. blok z butem
def make_boot():
    """
    Kadr 1200x628. Wtopiony tekst w lewej kolumnie: naglowek y140..172 (od x=45),
    podtytul y228..252 (od x=193), dyskalimer od y=556 (od x=160). Maska omija wszystkie trzy:
    wezszy pas do x=176 od y=200 (tam jest sama cholewka) + pelna szerokosc do x=352 od y=264,
    obciete na y=554 tuz nad dyskalimerem.

    Krawedzie: lewa i DOLNA twarde (w banerze pokrywaja sie z krawedziami kadru – but wchodzi
    z lewego dolnego rogu), gorna i prawa wygaszone, zeby blok wtopil sie w tlo z tej samej tekstury.
    """
    im = load(WIDE)
    a = np.array(im).astype(np.int16)
    h, w = a.shape[:2]                           # 628 x 1200
    TOP, BOT = 222, 554                          # nad cholewka / tuz nad dyskalimerem

    # granica prawa: w pasie czerwieni czyta sie SAMA (lewa krawedz paska = obrys buta,
    # bo pasek biegnie ZA butem), poza nim punkty kontrolne odczytane z kadru
    red = (a[:, :, 0] > 150) & (a[:, :, 1] < 80) & (a[:, :, 2] < 80)
    ctrl = {222: 82, 232: 126, 245: 154, 262: 158, 274: 142,
            430: 214, 445: 226, 465: 222, 480: 250, 495: 270, 510: 300,
            520: 330, 530: 386, 540: 446, 548: 486, 554: 520}
    ys = np.array(sorted(ctrl)); xs = np.array([ctrl[y] for y in ys])

    xmax = np.zeros(h, np.float32)
    for y in range(TOP, BOT):
        r = np.where(red[y, :700])[0]
        if len(r) and 270 <= y <= 428:
            xmax[y] = r.min() - 4                # tuz przed czerwienia = krawedz buta
        else:
            xmax[y] = np.interp(y, ys, xs)
    # wygladzenie granicy (drobne zabki z JPEG-u i pojedyncze piksele czerwieni)
    xmax[TOP:BOT] = ndimage.uniform_filter1d(xmax[TOP:BOT], 9)

    m = np.zeros((h, w), np.uint8)
    xx = np.arange(w)[None, :]
    m[TOP:BOT] = np.where(xx <= xmax[TOP:BOT, None], 255, 0)

    soft = np.array(feather_mask(m, 3), np.float32)     # 5 px dawalo widoczna „chmure" tla przy cholewce
    soft[:, :6] = np.where(m[:, :6] > 0, 255, soft[:, :6])             # lewa krawedz twarda
    soft[BOT - 8:BOT] = np.where(m[BOT - 8:BOT] > 0, 255, soft[BOT - 8:BOT])   # dolna twarda
    soft[BOT:, :] = 0                            # nic ponizej (dyskalimer wypada)
    alpha = np.clip(soft, 0, 255).astype(np.uint8)

    rgb = kill_red_fringe(np.array(im).astype(np.float32), m)
    # jasny beton przy podeszwie wygasilby sie na ciemnym tle banera jak wycieta plama –
    # ciemnimy go progresywnie od y=500 w dol (but jest tam ciemna podeszwa, wiec nie traci detalu)
    yy = np.arange(h)[:, None]
    k = np.clip((yy - 500) / 54.0, 0, 1)
    lum = rgb.mean(axis=2, keepdims=True)
    over = np.clip((lum - 70) / 120.0, 0, 1)                  # ile piksel jest „za jasny"
    rgb *= (1 - 0.80 * k[:, :, None] * over)

    out = Image.fromarray(np.dstack([rgb.astype(np.uint8), alpha]), 'RGBA')
    out = out.crop((0, TOP - 8, 560, BOT))       # bbox maski + zapas na feather
    out.save(os.path.join(OUT, 'boot.png'))
    print('boot.png', out.size)


# ---------------------------------------------------------------- 3. czapka (cutout)
def make_cap():
    """
    Kadr 1:1, czapka x655..1045, y475..845. Tlo wokol ciemne, po lewej dolem wchodzi czerwony pasek.
    Maska: jasnosc > prog (czapka jasnoszara, daszek ciemnoszary ~70-95 vs tlo ~20-45),
    czerwien paska odcinana kolorem (R >> G,B). Potem zasklepienie dziur i usuniecie drobin.
    """
    x0, y0 = 640, 465
    im = load(SQ).crop((x0, y0, 1055, 855))
    a = np.array(im).astype(np.int16)
    lum = a.mean(axis=2)
    red = (a[:, :, 0] > 120) & (a[:, :, 0] - a[:, :, 1] > 60) & (a[:, :, 0] - a[:, :, 2] > 50)

    # prog zalezny od wysokosci: korona jasna (>78 odcina kamyki tla), daszek ciemnoszary (~60-95)
    prog = np.full(lum.shape, 78.0)
    prog[int(700 - y0):, :] = 52.0
    obj = (lum > prog) & ~red
    obj = ndimage.binary_opening(obj, np.ones((5, 5)))        # zrywa mostki do jasnych kamykow tla
    obj = ndimage.binary_closing(obj, np.ones((7, 7)))
    obj = ndimage.binary_fill_holes(obj)
    # zostaw obszar zawierajacy SRODEK czapki (nie „najwiekszy" – tlem bywa wieksze)
    lab, n = ndimage.label(obj)
    seed = lab[int(650 - y0), int(850 - x0)]                 # punkt w czubku czapki
    if seed:
        obj = lab == seed
    obj = ndimage.binary_closing(obj, np.ones((9, 9)))
    obj = ndimage.binary_fill_holes(obj)
    obj = ndimage.binary_erosion(obj, np.ones((3, 3)))       # zjada ciemne halo tla przy krawedzi

    alpha = np.array(feather_mask((obj * 255).astype(np.uint8), 1.1))
    rgb = kill_red_fringe(np.array(im).astype(np.float32), (obj * 255).astype(np.uint8), band=7)
    out = Image.fromarray(np.dstack([rgb.astype(np.uint8), alpha]), 'RGBA')
    bbox = out.getbbox()
    out = out.crop(bbox)
    out.save(os.path.join(OUT, 'cap.png'))
    print('cap.png', out.size, 'bbox', bbox)


# ---------------------------------------------------------------- 4. logo Milwaukee (bialy znak)
def make_logo():
    """
    Kafel logo w kadrze 1:1: x82..345, y0..169 (kafel wchodzi z gornej krawedzi).
    Wycinamy sam BIALY znak jako alfa -> czerwony kafel z wlasnymi marginesami rysuje HTML.
    Znak zostaje oryginalny (bez przemalowania) – biala wersja na czerwieni to wersja producenta.
    """
    im = load(SQ).crop((82, 0, 345, 169))
    a = np.array(im).astype(np.float32)
    # bialy znak na czerwieni: alfa = jak bardzo piksel jest jasny w kanalach G/B (czerwien ma G,B ~0)
    alpha = np.clip((a[:, :, 1] + a[:, :, 2]) / 2.0 / 235.0 * 255.0, 0, 255).astype(np.uint8)
    rgb = np.full(a.shape, 255, np.uint8)                     # czysta biel pod maska
    out = Image.fromarray(np.dstack([rgb, alpha]), 'RGBA')
    out.save(os.path.join(OUT, 'logo-mil.png'))
    print('logo-mil.png', out.size)


if __name__ == '__main__':
    make_bg_tex()
    make_boot()
    make_cap()
    make_logo()
    print('OK ->', OUT)
