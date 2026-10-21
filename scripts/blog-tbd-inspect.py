#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""READ-ONLY: zestawia placeholdery TBD/[KAT:] z plikow kolejki z kandydatami z rekonesansu.

Wypisuje per wpis:
  - kazdy placeholder [PRODUKT: TBD:...] / [PRODUKTY: ...] w kolejnosci wystapienia,
    razem z krotkim kontekstem (naglowek sekcji, w ktorej stoi),
  - kandydatow z blog/queue/_kafelki-partiaD-72-81.json (slot -> glowny + zapasowe),
  - luki: slot bez kandydata (glowny = null).

Sluzy do zbudowania mapy podmiany, ktora nastepnie stosuje blog-tbd-apply.py.

Uzycie: python blog-tbd-inspect.py [numery...]
"""
import json, io, os, re, sys, glob

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
QUEUE = os.path.join(ROOT, 'blog', 'queue')
RECON = os.path.join(QUEUE, '_kafelki-partiaD-72-81.json')


def bez_html(s):
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def naglowek_przed(html, poz):
    frag = html[:poz]
    m = None
    for m in re.finditer(r'(?is)<h([23])[^>]*>(.*?)</h\1>', frag):
        pass
    return bez_html(m.group(2))[:70] if m else '(przed pierwszym naglowkiem)'


def main():
    numery = sys.argv[1:]
    recon = json.load(io.open(RECON, encoding='utf-8-sig'))['wpisy']
    pliki = sorted(p for p in glob.glob(os.path.join(QUEUE, '*.json'))
                   if not os.path.basename(p).startswith('_'))
    for p in pliki:
        nr = os.path.basename(p).split('-')[0]
        if nr not in recon:
            continue
        if numery and nr not in numery:
            continue
        d = json.load(io.open(p, encoding='utf-8-sig'))
        html = d.get('tresc_html') or ''
        print('\n' + '=' * 78)
        print('WPIS %s  %s' % (nr, os.path.basename(p)))
        print('=' * 78)
        print('-- PLACEHOLDERY W TRESCI (kolejnosc wystapienia):')
        for m in re.finditer(r'\[PRODUKT(?:Y)?:[^\]]+\]', html):
            tekst = m.group(0)
            print('  * sekcja "%s"' % naglowek_przed(html, m.start()))
            for czesc in tekst.split('||'):
                print('      %s' % czesc.strip()[:150])
        katph = re.findall(r'\[KAT:[^\]]+\]', html)
        if katph:
            print('-- PLACEHOLDERY KATEGORII: %s' % ', '.join(sorted(set(katph))))
        print('-- KANDYDACI Z REKONESANSU:')
        for slot, v in recon[nr]['slots'].items():
            g = v.get('glowny')
            if not g:
                print('  %-9s BRAK KANDYDATA  (intencja: %s)' % (slot, str(v.get('intencja'))[:80]))
                continue
            print('  %-9s %s | id %s | stan %s | sprzedaz %s | gsc_kliki %s | kat %s'
                  % (slot, g['nazwa'][:66], g['product_id'], g.get('stan'),
                     g.get('sprzedaz'), g.get('gsc_kliki'), g.get('kategoria_id')))
            for z in (v.get('zapasowe') or [])[:2]:
                print('            zapas: %s | id %s | stan %s' % (z['nazwa'][:60], z['product_id'], z.get('stan')))
            if v.get('uwaga'):
                print('            uwaga: %s' % str(v['uwaga'])[:160])
        for u in (recon[nr].get('uwagi_wpisu') or []):
            print('-- UWAGA WPISU: %s' % str(u)[:220])


if __name__ == '__main__':
    main()
