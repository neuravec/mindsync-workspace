#!/usr/bin/env python3
"""READ-ONLY: analityka bloga + kopalnia tematow z danych GSC (duety W1/W3 strategii).

Robi trzy rzeczy:
  1. wpis-frazy.csv       frazy per WPIS bloga (permalink w roocie domeny)
  2. BRIEF-blog.md        wpisy do wzmocnienia (frazy poz. 4-20 = rozbudowa sekcji/FAQ)
  3. tematy-luki.csv      zapytania INFORMACYJNE/RANKINGOWE z wyswietleniami, na ktore
                          zaden nasz URL nie rankuje w top 12 = kandydaci na nowe wpisy

MindSync (adaptacja 2026-08-25): wpisy bloga zyja pod /journal/<slug> na mindsync.app.
Wpis = kazdy URL o sciezce journal/... (live CMS) plus slugi z blog/queue/*.json (przyszle).
Markery intencji przestawione na ANGIELSKIE (tresc i frazy bloga sa EN).

Uzycie: python blog-tematy.py [--from RRRR-MM-DD] [--to RRRR-MM-DD]
"""
import json, os, sys, csv, datetime, re, glob, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pull_gsc

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SITE = json.load(open(os.path.join(HERE, 'gsc.config.json'), encoding='utf-8'))['site_url']
OUT = os.path.join(ROOT, 'seo', 'blog', 'gsc-frazy')

INFO_MARKERS = ('how ', 'what ', 'why ', 'when ', 'where ', 'which ', 'can ', 'should ',
                'is ', 'are ', 'does ', 'do i ', ' vs ', 'versus', 'difference', 'guide',
                'tips', 'ways to', 'meaning', 'examples', 'checklist', 'prepare')
RANK_MARKERS = ('best ', ' top ', 'top ', 'review', 'reviews', 'alternatives', 'ranked',
                'comparison', 'compare', 'worth it', 'recommended')
BLOG_PREFIX = 'journal/'   # sciezka wpisow bloga na mindsync.app


def blog_slugs():
    slugs = set()
    for p in glob.glob(os.path.join(ROOT, 'blog', 'queue', '*.json')):
        if os.path.basename(p).startswith('_'):
            continue
        try:
            d = json.load(open(p, encoding='utf-8-sig'))
            s = (d.get('seo_url') or '').strip().strip('/')
            if s:
                slugs.add(s.lower())
        except Exception:
            pass
    return slugs


def pull(dims, start, end, flt=None):
    url = ('https://searchconsole.googleapis.com/webmasters/v3/sites/'
           + pull_gsc.urllib.parse.quote(SITE, safe='') + '/searchAnalytics/query')
    rows, offset = [], 0
    while True:
        payload = {'startDate': start.isoformat(), 'endDate': end.isoformat(),
                   'dimensions': dims, 'rowLimit': 25000, 'startRow': offset, 'type': 'web'}
        if flt:
            payload['dimensionFilterGroups'] = [{'filters': flt}]
        d = pull_gsc.http_json(url, payload=payload, headers=pull_gsc.auth_header())
        b = d.get('rows', [])
        rows.extend(b)
        if len(b) < 25000:
            break
        offset += len(b)
    return rows


def main():
    args = sys.argv[1:]
    end = datetime.date.today() - datetime.timedelta(days=3)
    start = end - datetime.timedelta(days=365)
    if '--from' in args:
        start = datetime.date.fromisoformat(args[args.index('--from') + 1])
    if '--to' in args:
        end = datetime.date.fromisoformat(args[args.index('--to') + 1])
    os.makedirs(OUT, exist_ok=True)
    slugs = blog_slugs()
    print('Slugow wpisow z kolejki: %d | zakres %s..%s' % (len(slugs), start, end))

    print('Pobieram page+query (caly serwis)...')
    rows = pull(['page', 'query'], start, end)
    print('  wierszy: %d' % len(rows))

    blog_rows, best_pos = [], {}
    for r in rows:
        page, q = r['keys'][0], r['keys'][1]
        path = re.sub(r'^https?://[^/]+', '', page).split('?')[0].strip('/')
        pos = r.get('position', 99)
        # najlepsza pozycja dowolnego URL-a na fraze (do detekcji luk)
        if q not in best_pos or pos < best_pos[q][0]:
            best_pos[q] = (pos, path)
        pl = path.lower()
        is_blog = pl.startswith(BLOG_PREFIX) or (pl.split('/')[-1] in slugs)
        if is_blog:
            slug = pl[len(BLOG_PREFIX):] if pl.startswith(BLOG_PREFIX) else pl
            blog_rows.append({'slug': slug, 'query': q, 'clicks': r.get('clicks', 0),
                              'impressions': r.get('impressions', 0),
                              'position': round(pos, 1)})

    with open(os.path.join(OUT, 'wpis-frazy.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['slug', 'query', 'clicks', 'impressions', 'position'],
                           delimiter=';')
        w.writeheader()
        w.writerows(sorted(blog_rows, key=lambda x: -x['impressions']))

    # --- luki tematyczne: frazy info/rankingowe bez naszego top12 ---
    qagg = collections.defaultdict(lambda: [0, 0])
    for r in rows:
        q = r['keys'][1]
        qagg[q][0] += r.get('impressions', 0)
        qagg[q][1] += r.get('clicks', 0)
    luki = []
    for q, (impr, clicks) in qagg.items():
        if impr < 10:
            continue
        ql = ' ' + q.lower() + ' '
        is_info = any(m in ql for m in INFO_MARKERS)
        is_rank = any(m in ql for m in RANK_MARKERS)
        if not (is_info or is_rank):
            continue
        bp, bpath = best_pos.get(q, (99, ''))
        if bp <= 12:
            continue  # cos juz rankuje sensownie
        luki.append({'query': q, 'impressions': impr, 'clicks': clicks,
                     'typ': 'RANKING' if is_rank else 'INFO',
                     'best_pos': round(bp, 1), 'best_url': bpath})
    luki.sort(key=lambda x: -x['impressions'])
    with open(os.path.join(OUT, 'tematy-luki.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        w = csv.DictWriter(f, fieldnames=['query', 'impressions', 'clicks', 'typ',
                                          'best_pos', 'best_url'], delimiter=';')
        w.writeheader()
        w.writerows(luki)

    # --- frazy rankingowe OGOLEM (nawet jesli cos rankuje) ---
    rankq = []
    for q, (impr, clicks) in qagg.items():
        ql = ' ' + q.lower() + ' '
        if impr >= 5 and any(m in ql for m in RANK_MARKERS):
            bp, bpath = best_pos.get(q, (99, ''))
            rankq.append((impr, clicks, q, round(bp, 1), bpath))
    rankq.sort(reverse=True)

    # --- brief ---
    per = collections.defaultdict(list)
    for r in blog_rows:
        per[r['slug']].append(r)
    with open(os.path.join(OUT, 'BRIEF-blog.md'), 'w', encoding='utf-8') as f:
        f.write('# Blog wg danych GSC - wzmocnienia i kopalnia tematow\n\n')
        f.write('Zrodlo: GSC page+query %s..%s. Skrypt: `scripts/gsc/blog-tematy.py`.\n\n' % (start, end))
        f.write('- wpisow z danymi: **%d** | wierszy fraza x wpis: %d\n' % (len(per), len(blog_rows)))
        f.write('- lacznie na wpisach: %d wysw. / %d klik.\n' % (
            sum(r['impressions'] for r in blog_rows), sum(r['clicks'] for r in blog_rows)))
        f.write('- luk tematycznych (INFO/RANKING bez top12): **%d**\n\n' % len(luki))

        f.write('## 1. Wpisy do WZMOCNIENIA (frazy poz. 4-20, sort po wysw.)\n\n')
        f.write('Dzialanie: rozbudowa sekcji/FAQ pod fraze, tytul/H2, link do kategorii.\n\n')
        cands = [r for r in blog_rows if 4 <= r['position'] <= 20 and r['impressions'] >= 15]
        cands.sort(key=lambda x: -x['impressions'])
        cur = None
        for r in cands[:60]:
            if r['slug'] != cur:
                f.write('\n### /%s\n\n' % r['slug'])
                cur = r['slug']
            f.write('- `%s` - %d wysw., poz. %.1f, %d klik.\n' % (
                r['query'], r['impressions'], r['position'], r['clicks']))

        f.write('\n## 2. LUKI TEMATYCZNE - kandydaci na nowe wpisy (best_pos > 12)\n\n')
        for l in luki[:50]:
            f.write('- [%s] `%s` - %d wysw., nasz best: poz. %.1f (%s)\n' % (
                l['typ'], l['query'], l['impressions'], l['best_pos'], l['best_url'][:60]))

        f.write('\n## 3. FRAZY RANKINGOWE (intencja "best/top/review/alternatives")\n\n')
        f.write('Kandydaci pod format porownawczy/listowy (karty [FEATURE:] + ItemList).\n\n')
        for impr, clicks, q, bp, bpath in rankq[:40]:
            f.write('- `%s` - %d wysw., best poz. %.1f (%s)\n' % (q, impr, bp, bpath[:60]))

    summary = {'od': str(start), 'do': str(end), 'wpisy_z_danymi': len(per),
               'luk_tematycznych': len(luki), 'fraz_rankingowych': len(rankq)}
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
