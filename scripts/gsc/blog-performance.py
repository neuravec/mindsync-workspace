#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""READ-ONLY: jak radzi sobie JUZ OPUBLIKOWANY blog w Google (krok 0 kazdej nowej partii).

blog-tematy.py mowi "o czym pisac dalej", blog-partia-frazy.py "jakimi slowami".
Ten skrypt odpowiada na pytanie "co z tego, co juz stoi, trzeba poprawic, zanim dopiszemy
nowe": sumy bloga, trend tygodniowy, ranking wpisow, frazy per wpis i automatyczne flagi.

Flagi (progi na gorze pliku):
  SNIPPET  - duzo wyswietlen, pozycja <= 10, CTR ~0  -> przepisz meta_title/description
  KLASTER  - >= 3 warianty tej samej frazy (>= 2 wspolne slowa)    -> dopisz H2/FAQ pod warianty
  NA-PROGU - pozycja 8-20 i sensowne wyswietlenia     -> rozbudowa tresci + linki wewnetrzne
  INTENCJA - glowna fraza wpisu nie zawiera slowa ze sluga -> sprawdz, czy trafiamy w intencje

Uzycie:
    python blog-performance.py                       # od 2026-03-01 do (dzis-3)
    python blog-performance.py --from 2026-09-01 --to 2026-09-25

Wynik: seo/blog/gsc-wyniki/BLOG-WYNIKI-<data>.md (+ surowe .json obok)
Uwaga: GSC anonimizuje rzadkie zapytania, wiec suma wyswietlen z fraz jest zwykle
duzo mniejsza niz suma wyswietlen stron. To normalne, raport podaje oba numery.
"""
import argparse, collections, datetime, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pull_gsc

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SITE = json.load(open(os.path.join(HERE, 'gsc.config.json'), encoding='utf-8'))['site_url']
OUT = os.path.join(ROOT, 'seo', 'blog', 'gsc-wyniki')

SNIPPET_MIN_IMPR, SNIPPET_MAX_POS, SNIPPET_MAX_CTR = 80, 10.0, 0.01
KLASTER_MIN_WARIANTOW = 3
PROG_POS_OD, PROG_POS_DO, PROG_MIN_IMPR = 8.0, 20.0, 30


def is_blog(url):
    return '/journal/' in url or url.rstrip('/').endswith('/blog')


def slug(url):
    return url.rstrip('/').split('/')[-1]


STOP = {'what', 'when', 'does', 'with', 'your', 'that', 'this', 'how', 'the', 'and',
        'for', 'is', 'it', 'do', 'to', 'a', 'my', 'i', 'of', 'in', 'if', 'should', 'actually'}


def warianty(qs):
    """Frazy, ktore dziela >= 2 znaczace slowa z najczestsza fraza wpisu (wlacznie z nia)."""
    if not qs:
        return []
    core = {w for w in qs[0]['keys'][0].lower().split() if w not in STOP}
    return [q for q in qs
            if len(core & {w for w in q['keys'][0].lower().split() if w not in STOP}) >= 2]


def agg(rows):
    c = sum(r['clicks'] for r in rows)
    i = sum(r['impressions'] for r in rows)
    p = sum(r['position'] * r['impressions'] for r in rows) / i if i else 0.0
    return c, i, (c / i if i else 0.0), p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from', dest='start', default='2026-03-01')
    ap.add_argument('--to', dest='end',
                    default=(datetime.date.today() - datetime.timedelta(days=3)).isoformat())
    a = ap.parse_args()

    pages = pull_gsc.query_all(SITE, ['page'], a.start, a.end)
    qp = pull_gsc.query_all(SITE, ['query', 'page'], a.start, a.end)
    dp = pull_gsc.query_all(SITE, ['date', 'page'], a.start, a.end)

    os.makedirs(OUT, exist_ok=True)
    tag = datetime.date.today().isoformat()
    json.dump({'pages': pages, 'qp': qp, 'dp': dp},
              open(os.path.join(OUT, f'BLOG-WYNIKI-{tag}.json'), 'w', encoding='utf-8'))

    site = agg(pages)
    blog = [r for r in pages if is_blog(r['keys'][0])]
    posts = [r for r in blog if '/journal/' in r['keys'][0]]
    b = agg(blog)

    L = [f'# Blog w GSC: {a.start} .. {a.end}', '', f'Pobrano {tag}, wlasciwosc {SITE}.', '',
         '## Sumy', '', '| | Wysw. | Klik. | CTR | Poz. |', '|---|---|---|---|---|']
    for name, t in [('Blog (wpisy + /blog)', b), ('Same wpisy', agg(posts)), ('Cala witryna', site)]:
        L.append(f'| {name} | {t[1]:.0f} | {t[0]:.0f} | {t[2]*100:.1f}% | {t[3]:.1f} |')

    wk = collections.defaultdict(lambda: [0, 0, 0, 0])
    for r in dp:
        d = datetime.date.fromisoformat(r['keys'][0])
        y, w, _ = d.isocalendar()
        k = f'{y}-W{w:02d}'
        wk[k][2] += r['impressions']
        if is_blog(r['keys'][1]):
            wk[k][0] += r['clicks']
            wk[k][1] += r['impressions']
    L += ['', '## Trend tygodniowy (ostatnie 8 tygodni)', '',
          '| Tydzien | Wysw. bloga | Klik. bloga | Udzial w wysw. witryny |', '|---|---|---|---|']
    for k in sorted(wk)[-8:]:
        v = wk[k]
        L.append(f'| {k} | {v[1]} | {v[0]} | {v[1] / v[2] * 100 if v[2] else 0:.0f}% |')

    per_post = collections.defaultdict(list)
    for r in qp:
        if is_blog(r['keys'][1]):
            per_post[slug(r['keys'][1])].append(r)
    widoczne = sum(r['impressions'] for rs in per_post.values() for r in rs)

    L += ['', '## Wpisy (wg wyswietlen)', '',
          '| Wpis | Wysw. | Klik. | CTR | Poz. | Flagi |', '|---|---|---|---|---|---|']
    flagged = []
    for r in sorted(blog, key=lambda r: -r['impressions']):
        s = slug(r['keys'][0])
        qs = sorted(per_post.get(s, []), key=lambda x: -x['impressions'])
        flags = []
        if r['impressions'] >= SNIPPET_MIN_IMPR and r['position'] <= SNIPPET_MAX_POS and r['ctr'] <= SNIPPET_MAX_CTR:
            flags.append('SNIPPET')
        if s != 'blog' and len(warianty(qs)) >= KLASTER_MIN_WARIANTOW:
            flags.append('KLASTER')
        if s != 'blog' and PROG_POS_OD <= r['position'] <= PROG_POS_DO and r['impressions'] >= PROG_MIN_IMPR:
            flags.append('NA-PROGU')
        if qs and s != 'blog':
            words = [w for w in s.split('-') if len(w) > 3]
            if words and not any(w in qs[0]['keys'][0].lower() for w in words):
                flags.append('INTENCJA')
        L.append(f"| {s} | {r['impressions']:.0f} | {r['clicks']:.0f} | {r['ctr']*100:.1f}% | "
                 f"{r['position']:.1f} | {' '.join(flags)} |")
        if flags:
            flagged.append((s, flags, qs))

    L += ['', f'## Frazy per wpis (widoczne {widoczne:.0f} z {b[1]:.0f} wysw., reszta zanonimizowana)', '']
    for s, rs in sorted(per_post.items(), key=lambda x: -sum(r['impressions'] for r in x[1])):
        L.append(f'### {s}')
        for r in sorted(rs, key=lambda x: -x['impressions'])[:10]:
            L.append(f"- `{r['keys'][0]}`: {r['impressions']:.0f} wysw., {r['clicks']:.0f} klik., poz. {r['position']:.1f}")
        L.append('')

    L += ['## Do zrobienia przed nowa partia', '']
    co = {'SNIPPET': 'przepisz meta_title i meta_description pod realne zapytania',
          'KLASTER': 'dopisz H2 lub pytanie FAQ pod warianty frazy z listy wyzej',
          'NA-PROGU': 'rozbuduj tresc i dodaj linki wewnetrzne z nowych wpisow partii',
          'INTENCJA': 'sprawdz SERP glownej frazy: czy wpis odpowiada na to, czego szukaja'}
    for s, flags, _ in flagged:
        L.append(f"- **{s}**: " + '; '.join(co[f] for f in flags))
    if not flagged:
        L.append('- brak flag')

    path = os.path.join(OUT, f'BLOG-WYNIKI-{tag}.md')
    open(path, 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print(f'Blog: {b[1]:.0f} wysw., {b[0]:.0f} klik., CTR {b[2]*100:.1f}%, poz. {b[3]:.1f}')
    print(f'Flagi: {len(flagged)} wpisow. Raport: {path}')


if __name__ == '__main__':
    main()
