#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Podmiana placeholderow TBD w plikach kolejki bloga na realne ID produktow.

Wejscie: mapa podmiany (JSON), ktora autoryzuje czlowiek po przejrzeniu wydruku
z `blog-tbd-inspect.py`. Format mapy:

{
  "77": {
    "inline_1": "USUN",              # brak produktu w ofercie -> kafelek wylatuje
    "inline_2": 7583,
    "blok_1":  7583,
    "blok_2":  "USUN",              # pozycja bloku wylatuje, blok zostaje krotszy
    "blok_3":  1093
  }
}

Kolejnosc slotow = kolejnosc wystapienia placeholderow w tresci:
inline_1, inline_2, ... (kafelki `[PRODUKT: ...]`), potem blok_1..blok_N
(pozycje wewnatrz `[PRODUKTY: ...]`, po separatorze `||`).

Zasady:
  - `TBD:<fraza>` zamieniane jest na samo ID (format `[PRODUKT: <id> | powod | kicker]`
    wg blog/queue/_format.md),
  - "USUN" na kafelku inline usuwa CALY placeholder wraz z otaczajacym go akapitem,
    jesli akapit nie zawiera nic poza kafelkiem,
  - "USUN" na pozycji bloku usuwa tylko ten segment `|| ...`,
  - jesli po usunieciu w bloku zostaje mniej niz 2 pozycje, skrypt ostrzega
    (blok jednopozycyjny lepiej zamienic na kafelek inline),
  - domyslnie DRY-RUN: nic nie zapisuje bez `--zapisz`,
  - backup pliku przed zapisem: <plik>.bak-tbd.

Uzycie:
  python blog-tbd-apply.py mapa.json              # podglad
  python blog-tbd-apply.py mapa.json --zapisz      # zapis + backup
"""
import json, io, os, re, sys, glob, shutil

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
QUEUE = os.path.join(ROOT, 'blog', 'queue')


def znajdz_plik(nr):
    for p in glob.glob(os.path.join(QUEUE, '%s-*.json' % nr)):
        return p
    return None


def podmien(html, mapa, raport):
    # 1) kafelki inline w kolejnosci wystapienia
    inline_idx = 0

    def _inline(m):
        nonlocal inline_idx
        inline_idx += 1
        klucz = 'inline_%d' % inline_idx
        cel = mapa.get(klucz)
        if cel is None:
            raport.append('  ! %s bez wpisu w mapie, zostawiam bez zmian' % klucz)
            return m.group(0)
        if str(cel).upper() == 'USUN':
            raport.append('  - %s USUNIETY (%s)' % (klucz, m.group(0)[:60]))
            return ''
        nowy = re.sub(r'TBD:[^|\]]+', str(cel) + ' ', m.group(0), count=1)
        raport.append('  + %s -> id %s' % (klucz, cel))
        return nowy

    html = re.sub(r'\[PRODUKT:[^\]]+\]', _inline, html)

    # 2) pozycje wewnatrz blokow [PRODUKTY: ...]
    def _blok(m):
        tekst = m.group(0)
        czesci = tekst.split('||')
        naglowek, pozycje, out = czesci[0], czesci[1:], []
        for i, poz in enumerate(pozycje, start=1):
            klucz = 'blok_%d' % i
            cel = mapa.get(klucz)
            if cel is None:
                raport.append('  ! %s bez wpisu w mapie, zostawiam' % klucz)
                out.append(poz)
                continue
            if str(cel).upper() == 'USUN':
                raport.append('  - %s USUNIETY z bloku' % klucz)
                continue
            out.append(re.sub(r'TBD:[^|\]]+', str(cel) + ' ', poz, count=1))
            raport.append('  + %s -> id %s' % (klucz, cel))
        if len(out) < 2:
            raport.append('  !! blok ma po czystce %d pozycji - rozwaz zamiane na kafelek inline' % len(out))
        if not out:
            return ''
        return naglowek + '||' + '||'.join(out)

    html = re.sub(r'\[PRODUKTY:[^\]]+\]', _blok, html)

    # 3) puste akapity po usunieciu kafelka
    html = re.sub(r'(?is)<p[^>]*>\s*</p>', '', html)
    return html


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    mapa_all = json.load(io.open(sys.argv[1], encoding='utf-8-sig'))
    zapisz = '--zapisz' in sys.argv

    for nr, mapa in sorted(mapa_all.items()):
        p = znajdz_plik(nr)
        if not p:
            print('WPIS %s: nie znalazlem pliku' % nr)
            continue
        d = json.load(io.open(p, encoding='utf-8-sig'))
        raport = []
        nowy = podmien(d.get('tresc_html') or '', mapa, raport)
        print('\nWPIS %s  %s' % (nr, os.path.basename(p)))
        for r in raport:
            print(r)
        zostalo = re.findall(r'TBD:[^|\]]+', nowy)
        if zostalo:
            print('  !! ZOSTALY placeholdery TBD: %s' % ', '.join(t.strip()[:40] for t in zostalo))
        if zapisz:
            shutil.copy2(p, p + '.bak-tbd')
            d['tresc_html'] = nowy
            with io.open(p, 'w', encoding='utf-8') as f:
                json.dump(d, f, ensure_ascii=False, indent=1)
            print('  zapisano (backup: %s.bak-tbd)' % os.path.basename(p))
    if not zapisz:
        print('\n[DRY-RUN] nic nie zapisane. Dodaj --zapisz, zeby utrwalic.')


if __name__ == '__main__':
    main()
