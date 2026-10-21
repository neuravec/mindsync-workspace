#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wycina sam ekran telefonu z grafik App Store (blog/images/app-screenshots/ios-N.webp).

Grafiki sklepowe maja juz naglowek i ramke telefonu, wiec do szablonu `app-screen` (ktory
rysuje wlasna ramke CSS) potrzebny jest czysty ekran. Skrypt wykrywa wewnetrzna krawedz
ramki (ciemniejszy obrys na jasnym tle), wycina ekran z marginesem 3 px, zaokragla rogi
przezroczystoscia i zapisuje PNG do social/images/app/ios-N-ekran.png.

Uzycie:
    python scripts/social/app-screens.py            # wszystkie ios-*.webp
    python scripts/social/app-screens.py 3 5        # tylko wybrane numery

Uwaga: ios-7 ma w tresci tekst po polsku, ios-8 to opinia (bez telefonu); nie uzywaj ich w postach EN.
"""
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social_common as sc  # noqa: E402

ZRODLO = os.path.join(sc.ROOT, 'blog', 'images', 'app-screenshots')
CEL = os.path.join(sc.ROOT, 'social', 'images', 'app')
PROG = 215      # jasnosc ponizej = ramka telefonu
MARGINES = 3


def _jasnosc(p):
    return sum(p[:3]) / 3.0


def _krawedz(piks, start, krok, limit):
    """Pierwszy piksel ekranu za obrysem ramki, idac od `start` w kierunku `krok`."""
    i, w_ramce = start, False
    while i != limit:
        ciemny = _jasnosc(piks(i)) < PROG
        if ciemny:
            w_ramce = True
        elif w_ramce:
            return i
        i += krok
    return None


def wytnij(src, dst):
    from PIL import Image, ImageDraw
    im = Image.open(src).convert('RGB')
    w, h = im.size
    y_mid, x_mid = int(h * 0.62), int(w * 0.33)
    lewa = _krawedz(lambda x: im.getpixel((x, y_mid)), int(w * 0.08), 1, w // 2)
    prawa = _krawedz(lambda x: im.getpixel((x, y_mid)), int(w * 0.92), -1, w // 2)
    gora = _krawedz(lambda y: im.getpixel((x_mid, y)), int(h * 0.26), 1, h // 2)
    dol = _krawedz(lambda y: im.getpixel((x_mid, y)), int(h * 0.995), -1, h // 2)
    if None in (lewa, prawa, gora, dol):
        raise ValueError('nie wykryto ramki telefonu w %s' % src)
    box = (lewa + MARGINES, gora + MARGINES, prawa - MARGINES + 1, dol - MARGINES + 1)
    ekran = im.crop(box).convert('RGBA')
    r = int(ekran.size[0] * 0.105)
    maska = Image.new('L', ekran.size, 0)
    ImageDraw.Draw(maska).rounded_rectangle((0, 0, ekran.size[0] - 1, ekran.size[1] - 1), radius=r, fill=255)
    ekran.putalpha(maska)
    ekran.save(dst, 'PNG', optimize=True)
    return box, ekran.size


def main():
    os.makedirs(CEL, exist_ok=True)
    numery = set(sys.argv[1:])
    for src in sorted(glob.glob(os.path.join(ZRODLO, 'ios-*.webp'))):
        n = re.search(r'ios-(\d+)', src).group(1)
        if numery and n not in numery:
            continue
        dst = os.path.join(CEL, 'ios-%s-ekran.png' % n)
        try:
            box, size = wytnij(src, dst)
            print('OK  %s -> %s  box=%s  %dx%d' % (sc.rel(src), sc.rel(dst), box, size[0], size[1]))
        except Exception as e:
            print('--  %s: %s' % (sc.rel(src), e))


if __name__ == '__main__':
    main()
