#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""KROK 0 pipeline'u bloga MindSync: bramka POKRYCIA FUNKCJAMI przed pisaniem wpisow.

Adaptacja blog-asortyment-preflight.py z PLASMET (tam: czy sklep ma produkty; tu: czy
aplikacja MindSync ma funkcje/ekran/plan, do ktorego wpis moze uczciwie prowadzic).
Lekcja z PLASMET (partia D): bramka robiona ROWNOLEGLE z pisaniem = 8 z 10 wpisow do
przepisania. Dlatego bramka idzie na LISCIE TEMATOW, zanim powstanie brief.

Wejscie:
  --temat   plik JSON: { "nazwa tematu": ["keyword", "keyword", ...], ... }
            keywordy EN dopasowywane do katalogu funkcji (id, name, short, keywords)
  --katalog opcjonalnie inny plik katalogu (domyslnie blog/app-features.json)

Werdykty per temat:
  OK      >= 1 funkcja LIVE pasuje      -> temat da sie obsluzyc kartami [FEATURE:]
  RYZYKO  tylko funkcje beta/planned    -> pisz ostroznie, karta krucha albo bez karty,
          albo pasuje tylko site_target    z linkiem do strony zbiorczej
  BRAK    0 trafien                     -> ZMIEN KAT tematu albo temat wypada;
                                           dopisz do docs/luki-funkcji.md

Uzycie:
  python scripts/blog-coverage-preflight.py --temat blog/queue/_preflight-<partia>.json
"""
import json, io, os, sys, argparse, unicodedata

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
KATALOG_DOMYSLNY = os.path.join(ROOT, 'blog', 'app-features.json')
REJESTR_LUK = 'docs/luki-funkcji.md'


def norm(s):
    s = unicodedata.normalize('NFKD', s or '')
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.lower().strip()


def wczytaj_katalog(sciezka):
    if not os.path.exists(sciezka):
        sys.exit('Brak katalogu funkcji: %s (utrzymywany recznie, wzor w blog/app-features.json)' % sciezka)
    d = json.load(io.open(sciezka, encoding='utf-8-sig'))
    feats = []
    for f in d.get('features', []):
        blob = ' '.join([f.get('id', ''), f.get('name', ''), f.get('short', '')]
                        + list(f.get('keywords', [])))
        feats.append({
            'id': f.get('id'),
            'name': f.get('name'),
            'status': (f.get('status') or 'planned').lower(),
            'cta': f.get('cta_url') or '',
            'norm': norm(blob),
        })
    targets = []
    for t in d.get('site_targets', []):
        targets.append({'url': t.get('url'), 'temat': t.get('temat', ''),
                        'norm': norm((t.get('url', '') + ' ' + t.get('temat', '')))})
    return feats, targets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--temat', required=True)
    ap.add_argument('--katalog', default=KATALOG_DOMYSLNY)
    a = ap.parse_args()

    feats, targets = wczytaj_katalog(a.katalog)
    tematy = json.load(io.open(a.temat, encoding='utf-8-sig'))
    tematy = {k: v for k, v in tematy.items() if not k.startswith('_')}   # _opis itp. = metadane

    print('=' * 84)
    print('BRAMKA POKRYCIA FUNKCJAMI (krok 0 pipeline bloga MindSync)')
    print('katalog: %d funkcji (%d live) + %d celow na stronie | zrodlo: %s'
          % (len(feats), sum(1 for f in feats if f['status'] == 'live'),
             len(targets), os.path.basename(a.katalog)))
    print('=' * 84)

    braki, ryzyka = [], []
    for nazwa, slowa in tematy.items():
        slowan = [norm(s) for s in slowa if s]
        traf = [f for f in feats if any(s in f['norm'] for s in slowan)]
        live = [f for f in traf if f['status'] == 'live']
        kruche = [f for f in traf if f['status'] != 'live']
        traf_t = [t for t in targets if any(s in t['norm'] for s in slowan)]

        if live:
            werdykt, znak = 'OK', '  '
        elif kruche or traf_t:
            werdykt, znak = 'RYZYKO', '! '
            ryzyka.append(nazwa)
        else:
            werdykt, znak = 'BRAK', 'XX'
            braki.append(nazwa)

        print('\n%s[%-6s] %s' % (znak, werdykt, nazwa))
        for f in live[:5]:
            print('        LIVE   %-22s %s' % (f['id'], f['name']))
        for f in kruche[:3]:
            print('        %-6s %-22s %s' % (f['status'].upper(), f['id'], f['name']))
        for t in traf_t[:3]:
            print('        STRONA %-42s (%s)' % (t['url'], t['temat']))
        if werdykt == 'BRAK':
            print('        -> zmien kat tematu, albo z gory planuj wpis bez karty (link do'
                  ' %s), albo temat wypada.' % (targets[0]['url'] if targets else '/features'))

    print('\n' + '=' * 84)
    print('PODSUMOWANIE: OK %d | RYZYKO %d | BRAK %d'
          % (len(tematy) - len(ryzyka) - len(braki), len(ryzyka), len(braki)))
    if braki:
        print('\nBRAK pokrycia (dopisz do %s jako sygnal produktowy z liczba z GSC):' % REJESTR_LUK)
        for b in braki:
            print('  - %s' % b)
    if ryzyka:
        print('\nRYZYKO (funkcja nie-live albo tylko strona zbiorcza) - planuj karte ostroznie:')
        for r in ryzyka:
            print('  - %s' % r)
    print('\nUWAGA: dopasowanie idzie po keywordach z katalogu. Przy werdykcie BRAK najpierw')
    print('sprawdz, czy to nie kwestia slownictwa (dopisz synonimy EN do listy slow i powtorz),')
    print('dopiero potem uznaj, ze funkcji nie ma.')
    sys.exit(1 if braki else 0)


if __name__ == '__main__':
    main()
