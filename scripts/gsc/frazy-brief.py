#!/usr/bin/env python3
"""READ-ONLY: brief frazowy per karta produktu z danych GSC.

Wejscie:  seo/produkty/gsc-frazy/produkt-frazy.csv (z product-queries.py)
Wyjscie:  seo/produkty/gsc-frazy/BRIEF-frazowy.md   - do czytania i do promptow agentow
          seo/produkty/gsc-frazy/brief.csv          - maszynowo (1 wiersz = 1 karta)

Sedno: pokazuje, ktorych slow z realnych zapytan NIE MA w tytule karty.
To jest wejscie dla tytulu, meta description, leadu opisu i pola booster.
"""
import csv, collections, re, os, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
DIR = os.path.join(ROOT, 'seo', 'produkty', 'gsc-frazy')
SRC = os.path.join(DIR, 'produkt-frazy.csv')

# polskie znaki -> ascii (unicodedata NIE rozklada l z kreska)
PL = str.maketrans('ąćęłńóśźżĄĆĘŁŃÓŚŹŻ', 'acelnoszzACELNOSZZ')
STOP = {'do', 'na', 'w', 'z', 'i', 'ze', 'bez', 'jaki', 'jaka', 'jakie', 'czy',
        'mm', 'cm', 'ml', 'szt', 'l', 'kg', 'm', 'the', 'a', 'o', 'u'}


def norm(s):
    return re.sub(r'[^a-z0-9 ]', ' ', s.translate(PL).lower())


def words(s):
    return {w for w in norm(s).split() if w and w not in STOP and len(w) > 1}


def rdzen(w):
    """zgrubny rdzen: tnie polska koncowke fleksyjna"""
    for suf in ('ami', 'ach', 'owi', 'ego', 'emu', 'ych', 'ymi', 'ie', 'y', 'a', 'e', 'i', 'u', 'o'):
        if len(w) - len(suf) >= 4 and w.endswith(suf):
            return w[:-len(suf)]
    return w


def main():
    if not os.path.exists(SRC):
        sys.exit('Brak %s - najpierw uruchom product-queries.py' % SRC)
    rows = list(csv.DictReader(open(SRC, encoding='utf-8-sig'), delimiter=';'))
    per = collections.defaultdict(list)
    for r in rows:
        if r['product_id']:
            per[r['product_id']].append(r)

    from urllib.parse import unquote
    briefs = []
    for pid, rs in per.items():
        impr = sum(int(r['impressions']) for r in rs)
        clicks = sum(int(r['clicks']) for r in rs)
        if impr < 15:
            continue
        m = re.search(r'/p/([^/]+)/\d+', rs[0]['url'])
        tytul = unquote(m.group(1)).replace('-', ' ') if m else ''
        trdz = {rdzen(w) for w in words(tytul)}

        rs.sort(key=lambda x: -int(x['impressions']))
        luki, frazy = collections.Counter(), []
        for r in rs[:25]:
            q, qi, qp = r['query'], int(r['impressions']), float(r['position'])
            brak = sorted({w for w in words(q) if rdzen(w) not in trdz})
            frazy.append((q, qi, qp, brak))
            for w in brak:
                luki[w] += qi
        briefs.append({
            'product_id': pid, 'tytul': tytul.strip(), 'url': rs[0]['url'],
            'impressions': impr, 'clicks': clicks,
            'ctr': round(100 * clicks / impr, 2),
            'poz_najlepsza': min(float(r['position']) for r in rs),
            'n_fraz': len(rs),
            'fraza_glowna': rs[0]['query'],
            'brakujace_slowa': ', '.join(w for w, _ in luki.most_common(6)),
            '_frazy': frazy,
        })

    briefs.sort(key=lambda b: -b['impressions'])
    os.makedirs(DIR, exist_ok=True)

    with open(os.path.join(DIR, 'brief.csv'), 'w', newline='', encoding='utf-8-sig') as f:
        cols = ['product_id', 'tytul', 'impressions', 'clicks', 'ctr', 'poz_najlepsza',
                'n_fraz', 'fraza_glowna', 'brakujace_slowa', 'url']
        w = csv.DictWriter(f, fieldnames=cols, delimiter=';', extrasaction='ignore')
        w.writeheader()
        w.writerows(briefs)

    with open(os.path.join(DIR, 'BRIEF-frazowy.md'), 'w', encoding='utf-8') as f:
        f.write('# Brief frazowy per karta produktu (dane GSC)\n\n')
        f.write('Zrodlo: Google Search Console, wymiar `page` + `query`, wlasciwosc `https://sklep.plasmet.pl/`.\n')
        f.write('Wygenerowane przez `scripts/gsc/frazy-brief.py`. **Frazy sa faktem, nie propozycja** - tak ludzie realnie szukaja.\n\n')
        f.write('- kart z danymi frazowymi (>=15 wysw.): **%d**\n' % len(briefs))
        f.write('- kart z zerem klikniec mimo >=50 wysw.: **%d**\n\n' %
                sum(1 for b in briefs if b['clicks'] == 0 and b['impressions'] >= 50))
        f.write('## Jak tego uzywac\n\n')
        f.write('`brakujace_slowa` = slowa z realnych zapytan, ktorych NIE MA w tytule karty.\n')
        f.write('Kolejnosc dzialania: tytul -> meta description -> lead opisu -> `booster`.\n')
        f.write('⚠ Slowo z zapytania wchodzi do tytulu TYLKO, gdy jest prawdziwe dla produktu.\n')
        f.write('Klient szukajacy "silikon dekarski" moze trafic na uszczelniacz kauczukowy, ale w tytule\n')
        f.write('nie wolno nazwac go silikonem. Takie frazy ida do `booster` i do opisu, nie do nazwy.\n\n')
        f.write('---\n\n')
        for b in briefs[:120]:
            f.write('### id %s | %d wysw. | %d klik | CTR %.2f%% | najlepsza poz. %.1f\n\n'
                    % (b['product_id'], b['impressions'], b['clicks'], b['ctr'], b['poz_najlepsza']))
            f.write('**Tytul:** %s\n\n' % b['tytul'])
            for q, qi, qp, brak in b['_frazy'][:6]:
                f.write('- `%s` - %d wysw., poz. %.1f%s\n'
                        % (q, qi, qp, ('  → brak w tytule: **%s**' % ', '.join(brak)) if brak else ''))
            f.write('\n')
    print('kart w briefie: %d' % len(briefs))
    print('zapisano: %s' % DIR)


if __name__ == '__main__':
    main()
