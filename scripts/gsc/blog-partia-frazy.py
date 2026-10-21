#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""READ-ONLY: frazy GSC pod KONKRETNE tematy nowej partii bloga.

blog-tematy.py odpowiada na pytanie "o czym pisac" (luki + wzmocnienia).
Ten skrypt odpowiada na pytanie "jakimi SLOWAMI pisac" dla tematow, ktore juz sa
wybrane: dla kazdego wpisu partii wyciaga realne zapytania z korpusu GSC
(dosłowne brzmienie do FAQ i H2 wg zasady z blog/queue/_format.md), pozycje,
wyswietlenia oraz URL, ktory dziś na te frazy rankuje (kontrola kanibalizacji).

Uzycie:
    python blog-partia-frazy.py                      # okno domyslne: 90 dni do (dzis-3)
    python blog-partia-frazy.py --from 2026-05-01 --to 2026-08-14
    python blog-partia-frazy.py --topics <plik.json> # wlasna definicja tematow

Wynik: seo/blog/gsc-frazy/PARTIA-<tag>-frazy.md + .csv
"""
import json, os, sys, csv, datetime, unicodedata, argparse, collections

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pull_gsc

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
SITE = json.load(open(os.path.join(HERE, 'gsc.config.json'), encoding='utf-8'))['site_url']
OUT = os.path.join(ROOT, 'seo', 'blog', 'gsc-frazy')

# --- tematy partii D (wpisy 72-81). Klucz = numer pliku kolejki.
#     "any": fraza pasuje, gdy zawiera KTORYKOLWIEK z tych ciagow (bez ogonkow, lowercase).
TOPICS_DEFAULT = {
    "72 Hydroizolacja fundamentow (dysperbit / KMB / folia kubelkowa)": [
        "hydroizolacj", "dysperbit", "masa kmb", "kmb", "masa bitumiczn", "bitumiczn",
        "folia kubelkow", "izolacja fundament", "fundament przed wilgoc", "abizol",
        "izolacja przeciwwilgociow", "sciana piwnicy", "roztwor asfaltow", "lepik"],
    "73 Przeglad dachu i rynien przed jesienia": [
        "rynn", "dachu", "dach ", "dekarsk", "przeciek", "blachodachow", "blachotrapez",
        "obrobka blacharsk", "tasma naprawcz", "wkret farmersk", "wkrety farmersk", "papa"],
    "74 Preparat na plesn, grzyb i glony": [
        "plesn", "plesni", "grzyb", "grzybobojcz", "glon", "nalot", "mchu", "mech na",
        "savo", "odgrzybia", "zielony osad", "kostke", "kostka bruk"],
    "75 Chemia budowlana jesienia (temperatury stosowania)": [
        "w jakiej temperaturze", "temperatura stosowan", "minimalna temperatur",
        "temperatura schniec", "punkt rosy", "mroz", "przymrozk", "zimowa pianka",
        "pianka zimow", "malowac na zewnatrz", "kiedy malowac", "ile schnie",
        "jak dlugo schnie", "czas schniec", "moze zamarzn"],
    "76 Silikon wysokotemperaturowy czy uszczelniacz kominkowy": [
        "wysokotemperaturow", "kominkow", "300 stopni", "1500 stopni", "do 300 c",
        "ogniotrwal", "szamot", "do kominka", "zaroodporn", "termiczn uszczel"],
    "77 Przeglad kominka przed sezonem grzewczym": [
        "kominka", "kominek", "sznur ceramiczn", "szyba kominkow", "sadz",
        "uszczelka kominka", "wklad kominkow", "sezon grzewcz", "przewod kominow",
        "czyszczenie komina", "drzwiczki kominow", "drzwiczki rewizyjn"],
    "78 Obuwie ochronne S1PS, S3S, S7L (EN ISO 20345:2022)": [
        "obuwie", "buty robocz", "buty ochronn", "polbut", "trzewik", "s1p", "s3 ", "s3s",
        "s1ps", "s7", "en iso 20345", "20345", "podnosek", "wkladka antyprzebiciow", "flextred"],
    "79 Przedluzacz bebnowy na budowe (przekroj, IP44)": [
        "przedluzacz", "przedluzac", "beben", "bebnow", "bebnie", "ip44", "3x1 5", "3x2 5",
        "rozgalezni", "kabel budowlan", "naswietlacz", "przewod zasilaj"],
    "80 Odziez robocza na deszcz i chlod (EN 343, EN 342, EN 14058)": [
        "kurtk", "bluz", "czapk", "koszulk", "odziez robocz", "przeciwdeszczow",
        "wodoodporn", "ocieplan", "en 343", "en 342", "14058", "softshell",
        "spodnie robocz", "kombinezon", "odziez ochronn", "ubranie robocz"],
    "81 Odziez podgrzewana Milwaukee M12": [
        "podgrzewan", "ogrzewan", "heated", "kamizelka m12", "kurtka m12", "bluza m12",
        "kamizelka milwaukee", "kurtka milwaukee", "bluza milwaukee"],
    "81b Kontekst: akumulatory i system M12 (do sekcji o zasilaniu)": [
        "akumulator m12", "bateria m12", "m12 vs m18", "m12 czy m18", "ladowarka m12"],
}


def strip_pl(s):
    s = unicodedata.normalize('NFKD', s)
    s = ''.join(c for c in s if not unicodedata.combining(c))
    return s.replace('ł', 'l').replace('Ł', 'L').lower()


def pull(dims, start, end):
    url = ('https://searchconsole.googleapis.com/webmasters/v3/sites/'
           + pull_gsc.urllib.parse.quote(SITE, safe='') + '/searchAnalytics/query')
    rows, offset = [], 0
    while True:
        payload = {'startDate': start.isoformat(), 'endDate': end.isoformat(),
                   'dimensions': dims, 'rowLimit': 25000, 'startRow': offset, 'type': 'web'}
        d = pull_gsc.http_json(url, payload=payload, headers=pull_gsc.auth_header())
        b = d.get('rows', [])
        rows.extend(b)
        if len(b) < 25000:
            break
        offset += 25000
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--from', dest='dfrom')
    ap.add_argument('--to', dest='dto')
    ap.add_argument('--topics')
    ap.add_argument('--tag', default='D')
    ap.add_argument('--limit', type=int, default=40)
    a = ap.parse_args()

    end = datetime.date.fromisoformat(a.dto) if a.dto else datetime.date.today() - datetime.timedelta(days=3)
    start = datetime.date.fromisoformat(a.dfrom) if a.dfrom else end - datetime.timedelta(days=90)
    topics = json.load(open(a.topics, encoding='utf-8')) if a.topics else TOPICS_DEFAULT

    print('GSC: %s  %s .. %s' % (SITE, start, end))
    qrows = pull(['query'], start, end)
    qprows = pull(['query', 'page'], start, end)
    print('  zapytan jawnych: %d ; par query+page: %d' % (len(qrows), len(qprows)))

    # najlepiej rankujaca strona per zapytanie (max wyswietlen)
    best = {}
    for r in qprows:
        q, p = r['keys'][0], r['keys'][1]
        cur = best.get(q)
        if not cur or r['impressions'] > cur[1]:
            best[q] = (p, r['impressions'], r['position'])

    index = [(strip_pl(r['keys'][0]), r) for r in qrows]
    os.makedirs(OUT, exist_ok=True)
    md = [
        '# Frazy GSC pod partie bloga %s (wpisy z TOPICS)' % a.tag,
        '',
        '> Zrodlo: Search Console `%s`, okno **%s .. %s** (%d dni). Wygenerowane przez'
        ' `scripts/gsc/blog-partia-frazy.py` (READ-ONLY).' % (SITE, start, end, (end - start).days),
        '> Google anonimizuje wiekszosc zapytan, wiec **brak trafien nie znaczy brak popytu**'
        ' - znaczy brak historii dla tej frazy w naszym korpusie.',
        '> **Zasada z `_format.md`:** pytania FAQ przepisuj DOSLOWNIE z kolumny "zapytanie",'
        ' nie parafrazuj. Kolumna "dzis rankuje" pilnuje kanibalizacji: jesli tam stoi juz'
        ' nasz wpis na pozycji < 15, wzmacniamy TEN wpis, a nowy tekst nie powtarza jego tematu.',
        '',
    ]
    csv_rows = []
    for name, keys in topics.items():
        keysn = [strip_pl(k) for k in keys]
        hits = []
        for qn, r in index:
            if any(k in qn for k in keysn):
                hits.append(r)
        hits.sort(key=lambda r: (-r['impressions'], r['position']))
        md.append('## %s' % name)
        md.append('')
        if not hits:
            md.append('_Zero jawnych zapytan w oknie. Temat prowadzimy na estymatach (sezonowy/nowy)._')
            md.append('')
            continue
        tot_i = sum(r['impressions'] for r in hits)
        tot_c = sum(r['clicks'] for r in hits)
        md.append('Trafien: **%d** zapytan, **%d** wyswietlen, **%d** klikniec (CTR %.2f%%).'
                  % (len(hits), tot_i, tot_c, (100.0 * tot_c / tot_i) if tot_i else 0))
        md.append('')
        md.append('| zapytanie | wysw. | klik. | poz. | dzis rankuje |')
        md.append('|---|---:|---:|---:|---|')
        for r in hits[:a.limit]:
            q = r['keys'][0]
            b = best.get(q)
            page = ''
            if b:
                page = b[0].replace('https://sklep.plasmet.pl', '') or '/'
                page = '%s (poz. %.1f)' % (page, b[2])
            md.append('| %s | %d | %d | %.1f | %s |'
                      % (q, r['impressions'], r['clicks'], r['position'], page))
            csv_rows.append([name, q, r['impressions'], r['clicks'], round(r['position'], 1), page])
        if len(hits) > a.limit:
            md.append('')
            md.append('_...oraz %d dalszych zapytan (pelna lista w CSV)._' % (len(hits) - a.limit))
        md.append('')

    mdp = os.path.join(OUT, 'PARTIA-%s-frazy.md' % a.tag)
    with open(mdp, 'w', encoding='utf-8') as f:
        f.write('\n'.join(md))
    csvp = os.path.join(OUT, 'PARTIA-%s-frazy.csv' % a.tag)
    with open(csvp, 'w', encoding='utf-8-sig', newline='') as f:
        w = csv.writer(f, delimiter=';')
        w.writerow(['temat', 'zapytanie', 'wyswietlenia', 'klikniecia', 'pozycja', 'dzis_rankuje'])
        w.writerows(csv_rows)
    print('  zapisano: %s' % mdp)
    print('  zapisano: %s' % csvp)


if __name__ == '__main__':
    main()
