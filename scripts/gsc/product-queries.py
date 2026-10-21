#!/usr/bin/env python3
"""READ-ONLY: frazy wyszukiwania per KARTA PRODUKTU (wymiar page + query).

Odpowiada na pytanie "pod jakimi frazami ludzie szukaja tego produktu" -
z wlasnych danych GSC, a nie z narzedzia zewnetrznego.

Domyslnie zakres = od cutoveru (2026-07-14) do dzis-3, tylko URL-e /pl/p/.

Wynik: seo/produkty/gsc-frazy/
  produkt-frazy.csv    fraza x URL produktu (+ product_id wyluskany z URL)
  produkt-agg.csv      agregat per produkt (wyswietlenia, klikniecia, top frazy)
  okazje.csv           striking distance: pozycja 5-25 i wyswietlenia >= 30
  summary.json

Uzycie:
    python product-queries.py [--from RRRR-MM-DD] [--to RRRR-MM-DD]
"""
import json, os, sys, csv, datetime, re, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pull_gsc

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SITE = json.load(open(os.path.join(HERE, 'gsc.config.json'), encoding='utf-8'))['site_url']
OUT = os.path.join(ROOT, 'seo', 'produkty', 'gsc-frazy')

# /pl/p/<slug>/<id>  -> id
RE_PID = re.compile(r'/p/[^/]+/(\d+)')


def pull(dimensions, start, end, page_filter='/pl/p/'):
    url = ('https://searchconsole.googleapis.com/webmasters/v3/sites/'
           + pull_gsc.urllib.parse.quote(SITE, safe='') + '/searchAnalytics/query')
    rows, offset = [], 0
    while True:
        payload = {
            'startDate': start.isoformat(), 'endDate': end.isoformat(),
            'dimensions': dimensions, 'rowLimit': 25000, 'startRow': offset,
            'type': 'web',
        }
        if page_filter:
            payload['dimensionFilterGroups'] = [{'filters': [
                {'dimension': 'page', 'operator': 'contains', 'expression': page_filter}]}]
        data = pull_gsc.http_json(url, payload=payload, headers=pull_gsc.auth_header())
        batch = data.get('rows', [])
        rows.extend(batch)
        print('  pobrano %d (razem %d)' % (len(batch), len(rows)))
        if len(batch) < 25000:
            break
        offset += len(batch)
    return rows


def main():
    args = sys.argv[1:]
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = datetime.date(2026, 7, 14)          # cutover na Shoper
    if '--from' in args:
        start = datetime.date.fromisoformat(args[args.index('--from') + 1])
    if '--to' in args:
        end = datetime.date.fromisoformat(args[args.index('--to') + 1])

    print('Wlasciwosc: %s' % SITE)
    print('Zakres: %s .. %s' % (start, end))
    print('Pobieram wymiar page+query dla /pl/p/ ...')
    rows = pull(['page', 'query'], start, end)

    os.makedirs(OUT, exist_ok=True)
    recs = []
    for r in rows:
        page, query = r['keys'][0], r['keys'][1]
        m = RE_PID.search(page)
        recs.append({
            'product_id': m.group(1) if m else '',
            'url': page,
            'query': query,
            'clicks': r.get('clicks', 0),
            'impressions': r.get('impressions', 0),
            'ctr': round(r.get('ctr', 0) * 100, 2),
            'position': round(r.get('position', 0), 1),
        })

    with open(os.path.join(OUT, 'produkt-frazy.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['product_id', 'url', 'query', 'clicks',
                                          'impressions', 'ctr', 'position'], delimiter=';')
        w.writeheader()
        w.writerows(sorted(recs, key=lambda x: -x['impressions']))

    # agregat per produkt
    per = collections.defaultdict(lambda: {'impr': 0, 'clicks': 0, 'q': []})
    for r in recs:
        if not r['product_id']:
            continue
        p = per[r['product_id']]
        p['impr'] += r['impressions']
        p['clicks'] += r['clicks']
        p['url'] = r['url']
        p['q'].append((r['impressions'], r['query'], r['position']))

    agg = []
    for pid, p in per.items():
        top = sorted(p['q'], reverse=True)[:5]
        agg.append({
            'product_id': pid, 'url': p['url'],
            'impressions': p['impr'], 'clicks': p['clicks'],
            'ctr': round(100 * p['clicks'] / p['impr'], 2) if p['impr'] else 0,
            'n_fraz': len(p['q']),
            'top_frazy': ' | '.join('%s (%d wysw., poz. %.1f)' % (q, i, pos) for i, q, pos in top),
        })
    agg.sort(key=lambda x: -x['impressions'])
    with open(os.path.join(OUT, 'produkt-agg.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['product_id', 'url', 'impressions', 'clicks',
                                          'ctr', 'n_fraz', 'top_frazy'], delimiter=';')
        w.writeheader()
        w.writerows(agg)

    # striking distance
    okazje = [r for r in recs if r['impressions'] >= 30 and 5 <= r['position'] <= 25]
    okazje.sort(key=lambda x: -x['impressions'])
    with open(os.path.join(OUT, 'okazje.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['product_id', 'url', 'query', 'clicks',
                                          'impressions', 'ctr', 'position'], delimiter=';')
        w.writeheader()
        w.writerows(okazje)

    summary = {
        'site': SITE, 'od': str(start), 'do': str(end),
        'wierszy_fraza_x_url': len(recs),
        'produktow_z_danymi': len(per),
        'suma_wyswietlen': sum(r['impressions'] for r in recs),
        'suma_klikniec': sum(r['clicks'] for r in recs),
        'okazji_striking_distance': len(okazje),
    }
    with open(os.path.join(OUT, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    print('Zapisano do: %s' % OUT)


if __name__ == '__main__':
    main()
