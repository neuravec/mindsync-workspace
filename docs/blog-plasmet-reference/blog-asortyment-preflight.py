#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KROK 0 pipeline'u bloga: bramka asortymentowa PRZED pisaniem wpisow.

PO CO ISTNIEJE: w partii D okazalo sie, ze 8 z 10 gotowych wpisow dobieralo produkty,
ktorych sklep nie ma. Poprawianie tego po napisaniu tekstu jest droga robota: trzeba
wycinac kafelki, przepisywac akapity, ratowac tabele. Ten skrypt odpowiada na pytanie
"czy w ogole mamy czym obsluzyc ten temat" ZANIM ktokolwiek napisze zdanie.

Wejscie:
  --temat  plik JSON: { "nazwa tematu": ["slowo", "slowo", ...], ... }
           slowa dopasowywane sa do NAZW produktow (bez ogonkow, lowercase)
  --dump   zrzut katalogu (JSON, lista obiektow z product_id/name/stock).
           Swiezy zrzut: scripts/shoper-api/products-dump.ps1

Wyjscie: verdykt per temat
  OK      >= 3 pozycje ze stanem  -> temat da sie obsluzyc kafelkami
  RYZYKO  1-2 pozycje ze stanem   -> pisz, ale kafelek jest kruchy (jedna sprzedaz = 0)
  BRAK    0 pozycji ze stanem     -> ZMIEN TEMAT albo z gory zaplanuj sam link do kategorii

Uzycie:
  python blog-asortyment-preflight.py --temat blog/queue/_preflight-partiaE.json
  python blog-asortyment-preflight.py --temat ... --dump scripts/shoper-api/_products-fresh.json
"""
import json, io, os, re, sys, glob, argparse, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
DOMYSLNE_DUMPY = [
    os.path.join(ROOT, 'scripts', 'shoper-api', '_products-fresh.json'),
    os.path.join(ROOT, 'scripts', 'shoper-api', '_b2g-catalog-dump.json'),
]


def bez_ogonkow(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.replace('ł', 'l').replace('Ł', 'L').lower()


def liczba(x):
    try:
        return float(str(x).replace(',', '.'))
    except Exception:
        return 0.0


def wczytaj_dump(sciezka):
    if not sciezka:
        for k in DOMYSLNE_DUMPY:
            if os.path.exists(k):
                sciezka = k
                break
    if not sciezka or not os.path.exists(sciezka):
        sys.exit('Brak zrzutu katalogu. Zrob swiezy: scripts/shoper-api/products-dump.ps1')
    d = json.load(io.open(sciezka, encoding='utf-8-sig'))
    if isinstance(d, dict) and 'list' in d:
        d = d['list']
    prod = []
    for p in d:
        nazwa = p.get('name')
        if not nazwa and isinstance(p.get('translations'), dict):
            for v in p['translations'].values():
                if isinstance(v, dict) and v.get('name'):
                    nazwa = v['name']
                    break
        stan = p.get('stock')
        if isinstance(stan, dict):
            stan = stan.get('stock')
        prod.append({
            'id': p.get('product_id'),
            'nazwa': nazwa or '',
            'norm': bez_ogonkow(nazwa or ''),
            'stan': liczba(stan),
            'aktywny': str(p.get('active', '1')),
        })
    return sciezka, prod


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--temat', required=True)
    ap.add_argument('--dump')
    ap.add_argument('--min-ok', type=int, default=3)
    a = ap.parse_args()

    sciezka, prod = wczytaj_dump(a.dump)
    tematy = json.load(io.open(a.temat, encoding='utf-8-sig'))
    wiek = ''
    try:
        import datetime
        ts = datetime.datetime.fromtimestamp(os.path.getmtime(sciezka))
        wiek = ts.strftime(' (zrzut z %Y-%m-%d %H:%M)')
    except Exception:
        pass

    print('=' * 84)
    print('BRAMKA ASORTYMENTOWA (krok 0 pipeline bloga)%s' % wiek)
    print('katalog: %d produktow | zrodlo: %s' % (len(prod), os.path.basename(sciezka)))
    print('=' * 84)

    braki, ryzyka = [], []
    tematy = {k: v for k, v in tematy.items() if not k.startswith('_')}   # klucze _opis itp. to metadane
    for nazwa, slowa in tematy.items():
        slowan = [bez_ogonkow(s) for s in slowa]
        trafienia = [p for p in prod if any(s in p['norm'] for s in slowan)]
        ze_stanem = [p for p in trafienia if p['stan'] > 0 and p['aktywny'] != '0']
        if len(ze_stanem) >= a.min_ok:
            werdykt, znak = 'OK', '  '
        elif ze_stanem:
            werdykt, znak = 'RYZYKO', '! '
            ryzyka.append(nazwa)
        else:
            werdykt, znak = 'BRAK', 'XX'
            braki.append(nazwa)
        print('\n%s[%-6s] %s' % (znak, werdykt, nazwa))
        print('      trafien w nazwach: %d, ze stanem: %d' % (len(trafienia), len(ze_stanem)))
        for p in sorted(ze_stanem, key=lambda x: -x['stan'])[:5]:
            print('        id %-6s stan %-7.0f %s' % (p['id'], p['stan'], p['nazwa'][:64]))
        if not ze_stanem and trafienia:
            print('        (sa nazwy, ale wszystkie ze stanem 0 - sprawdz, czy to nie sezonowe wyczerpanie)')

    print('\n' + '=' * 84)
    print('PODSUMOWANIE: OK %d | RYZYKO %d | BRAK %d'
          % (len(tematy) - len(ryzyka) - len(braki), len(ryzyka), len(braki)))
    if braki:
        print('\nZMIEN TEMAT albo zaplanuj sam link do kategorii (bez kafelka):')
        for b in braki:
            print('  - %s' % b)
    if ryzyka:
        print('\nPISZ, ale kafelek kruchy (1-2 szt.) - sprawdz stan w dniu publikacji:')
        for r in ryzyka:
            print('  - %s' % r)
    print('\nUWAGA: dopasowanie idzie po NAZWACH produktow. Produkt nazwany sama marka handlowa')
    print('(np. "Boramon" zamiast "impregnat") nie zostanie znaleziony slowem rodzajowym.')
    print('Dlatego przy werdykcie BRAK dopisz do listy slow nazwy handlowe i powtorz.')
    sys.exit(1 if braki else 0)


if __name__ == '__main__':
    main()
