#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bramka kontrolna plikow kolejki bloga MindSync (READ-ONLY, nic nie zmienia).

Sprawdza to, co przy publikacji przez `scripts/webflow/blog-publish.ps1` albo psuje
wpis, albo lamie zasady z blog/queue/_format.md:

  BLOKERY (publikacja niemozliwa lub zasada twarda zlamana)
    - plik nie jest poprawnym JSON-em
    - brak pola wymaganego (tytul, tresc_html, planowana_data, status)
    - dlugi myslnik U+2014 gdziekolwiek w pliku (TOTAL BAN)
    - brak naglowka FAQ dokladnie "Frequently asked questions"
    - brak grafiki hero na dysku dla hero_slug (drip NIE generuje grafik)
    - kategoria poza kanonicznym zestawem
    - kolizja seo_url z innym wpisem w kolejce
    - kolizja albo dziura w planowana_data (drip = jeden wpis na dzien)
    - nierozwiazany placeholder TBD: / [KAT: przy statusie 'gotowy'

  OSTRZEZENIA (do decyzji czlowieka)
    - lead poza zakresem 40-60 slow
    - mniej niz 4 pytania FAQ
    - tresc krotsza niz 6000 znakow tekstu
    - brak kart funkcji [FEATURE:]
    - HTML niedozwolony w Webflow RichText (div / style= / <script> w tresc_html)
    - brak schema_jsonld
    - wpis z planowana_data >= 2026-09-26 bez pola "glos": "monika-v1"

  Wpisy z "glos": "monika-v1" przechodza dodatkowo scripts/blog-voice-check.py
  (blokery i ostrzezenia z prefiksem [glos]); stary warunek leadu 40-60 slow ich nie dotyczy.

Uzycie:
    python blog-queue-gate.py                       # wszystkie pliki kolejki
    python blog-queue-gate.py 72 73 74              # tylko wybrane numery
    python blog-queue-gate.py --od 2026-08-21       # wpisy od daty
"""
import json, os, sys, glob, re, io, argparse, datetime, collections

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
QUEUE = os.path.join(ROOT, 'blog', 'queue')
IMAGES = os.path.join(ROOT, 'blog', 'images')
KATEGORIE_OK = {'Therapy', 'MindSync Tips'}
FAQ_H = 'Frequently asked questions'
WYMAGANE = ('tytul', 'tresc_html', 'planowana_data', 'status')
GLOS_MONIKA = 'monika-v1'
GLOS_OD = '2026-09-26'  # od tej planowanej daty wpis bez pola `glos` dostaje ostrzezenie


def _voice_check():
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'blog_voice_check', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'blog-voice-check.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def bez_html(s):
    s = re.sub(r'(?is)<(script|style).*?</\1>', ' ', s)
    s = re.sub(r'(?s)<[^>]+>', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def sprawdz(path):
    blok, ostrz = [], []
    nazwa = os.path.basename(path)
    try:
        raw = io.open(path, encoding='utf-8-sig').read()
    except Exception as e:
        return nazwa, ['nie da sie odczytac pliku: %s' % e], [], None
    try:
        d = json.loads(raw)
    except Exception as e:
        return nazwa, ['niepoprawny JSON: %s' % e], [], None

    for p in WYMAGANE:
        if not d.get(p):
            blok.append('brak wymaganego pola `%s`' % p)

    if '—' in raw:
        ile = raw.count('—')
        gdzie = [k for k, v in d.items() if isinstance(v, str) and '—' in v]
        blok.append('DLUGI MYSLNIK U+2014 x%d (pola: %s)' % (ile, ', '.join(gdzie) or 'zagniezdzone'))

    html = d.get('tresc_html') or ''
    tekst = bez_html(html)

    if FAQ_H not in html:
        blok.append('brak naglowka FAQ dokladnie "%s"' % FAQ_H)

    kat = (d.get('kategoria') or '').strip()
    if kat and kat not in KATEGORIE_OK:
        blok.append('kategoria "%s" poza kanonicznym zestawem' % kat)

    slug = (d.get('hero_slug') or d.get('seo_url') or '').strip()
    hero_ok = False
    if slug:
        for nm in ('hero-1600x900.jpg', 'hero-1600x900.png', 'hero-1600x900.webp'):
            if os.path.exists(os.path.join(IMAGES, slug, nm)):
                hero_ok = True
                break
    if not hero_ok:
        blok.append('brak pliku hero na dysku dla slug "%s" (drip nie generuje grafik)' % slug)
    if not (d.get('hero_image_alt') or '').strip():
        ostrz.append('brak hero_image_alt (alt obrazka, SEO + WCAG)')

    status = (d.get('status') or '').strip()
    tbd = re.findall(r'TBD:[^|\]]+', html)
    katph = re.findall(r'\[KAT:[^\]]+\]', html)
    if status == 'gotowy':
        if tbd:
            blok.append('status `gotowy`, a w tresci %d placeholderow TBD: %s'
                        % (len(tbd), ', '.join(sorted(set(t.strip() for t in tbd))[:4])))
        if katph:
            blok.append('status `gotowy`, a w tresci %d placeholderow [KAT:]' % len(katph))
    else:
        if tbd:
            ostrz.append('%d placeholderow TBD do podmiany na ID produktow' % len(tbd))
        if katph:
            ostrz.append('%d placeholderow [KAT:] do podmiany na URL kategorii' % len(katph))

    # lead = pierwszy akapit (wpisy w glosie Moniki maja dluzsze otwarcie; sprawdza je
    # blog-voice-check.py nizej)
    m = re.search(r'(?is)<p[^>]*>(.*?)</p>', html)
    if d.get('glos') == GLOS_MONIKA:
        pass
    elif m:
        lead_slow = len(bez_html(m.group(1)).split())
        if not (36 <= lead_slow <= 66):
            ostrz.append('lead ma %d slow (cel 40-60, tolerancja 36-66)' % lead_slow)
    else:
        ostrz.append('nie znalazlem leadu (pierwszego <p>)')

    # Webflow RichText nie przepuszcza div/style/script - to psuje render wpisu
    zakazany = re.findall(r'(?is)<div\b|style\s*=|<script\b|<table\b', html)
    if zakazany:
        blok.append('HTML niedozwolony w Webflow RichText: %s (dozwolone: p,h2-h6,ul/ol/li,'
                    'blockquote,figure/img,a,strong,em,code)' % ', '.join(sorted(set(z.strip().lower() for z in zakazany))))

    # FAQ: policz pytania po naglowku FAQ
    poz = html.find(FAQ_H)
    if poz > -1:
        ogon = html[poz:]
        pyt = len(re.findall(r'(?is)<h3[^>]*>', ogon)) or len(re.findall(r'\?', bez_html(ogon)))
        if pyt < 4:
            ostrz.append('FAQ ma %d pytan (cel 4-5)' % pyt)

    if len(tekst) < 6000:
        ostrz.append('tresc ma %d znakow tekstu (cel 6000-10000; wzorzec: wpisy live na /journal)' % len(tekst))

    if '[FEATURE' not in html:
        ostrz.append('brak kart funkcji [FEATURE:]/[FEATURES:]')
    if not d.get('schema_jsonld'):
        ostrz.append('brak schema_jsonld (goly JSON grafu; generuje seo-tech-lead)')
    if not (d.get('kolor') or '').strip():
        ostrz.append('brak pola kolor (akcent karty; zestaw brandowy w docs/blog/brand-mindsync.md)')

    # glos bloga (od 2026-09-25 styl Moniki): wpisy z glos=monika-v1 przechodza kontrole
    # glosu; nowy wpis bez tego pola dostaje ostrzezenie, stare wpisy zostaja bez zmian
    if d.get('glos') == GLOS_MONIKA:
        gb, go = _voice_check().sprawdz_glos(d)
        blok.extend('[glos] ' + x for x in gb)
        ostrz.extend('[glos] ' + x for x in go)
    elif (d.get('planowana_data') or '') >= GLOS_OD and status != 'opublikowany':
        ostrz.append('brak "glos": "%s": wpis nie przeszedl sciezki /blog-write (stary styl?)' % GLOS_MONIKA)

    return nazwa, blok, ostrz, d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('numery', nargs='*')
    ap.add_argument('--od')
    a = ap.parse_args()

    pliki = sorted(p for p in glob.glob(os.path.join(QUEUE, '*.json'))
                   if not os.path.basename(p).startswith('_'))
    if a.numery:
        pliki = [p for p in pliki if os.path.basename(p).split('-')[0] in a.numery]

    wyniki, daty, slugi = [], collections.defaultdict(list), collections.defaultdict(list)
    for p in pliki:
        nazwa, blok, ostrz, d = sprawdz(p)
        if d:
            data = str(d.get('planowana_data') or '')[:10]
            if a.od and data and data < a.od:
                continue
            daty[data].append(nazwa)
            s = (d.get('seo_url') or '').strip()
            if s:
                slugi[s].append(nazwa)
            if a.od and not data:
                continue
        elif a.od:
            continue
        wyniki.append((nazwa, blok, ostrz, d))

    for data, nz in sorted(daty.items()):
        if len(nz) > 1:
            for n in nz:
                for w in wyniki:
                    if w[0] == n:
                        w[1].append('KOLIZJA DATY %s z: %s' % (data, ', '.join(x for x in nz if x != n)))
    for s, nz in slugi.items():
        if len(nz) > 1:
            for n in nz:
                for w in wyniki:
                    if w[0] == n:
                        w[1].append('KOLIZJA seo_url "%s" z: %s' % (s, ', '.join(x for x in nz if x != n)))

    blokery = ostrzezenia = 0
    print('=' * 78)
    print('BRAMKA KOLEJKI BLOGA  (%d plikow)' % len(wyniki))
    print('=' * 78)
    for nazwa, blok, ostrz, d in wyniki:
        status = (d or {}).get('status', '?')
        data = str((d or {}).get('planowana_data') or '?')[:10]
        znak = 'BLAD' if blok else ('uwagi' if ostrz else ' OK ')
        print('\n[%s] %-58s %s  %s' % (znak, nazwa, data, status))
        for b in blok:
            print('    X  %s' % b)
            blokery += 1
        for o in ostrz:
            print('    !  %s' % o)
            ostrzezenia += 1
    print('\n' + '=' * 78)
    print('PODSUMOWANIE: blokerow %d, ostrzezen %d, plikow %d' % (blokery, ostrzezenia, len(wyniki)))
    ciag = sorted(d for d in daty if d)
    if ciag:
        print('Zakres dat: %s .. %s' % (ciag[0], ciag[-1]))
        try:
            d0 = datetime.date.fromisoformat(ciag[0])
            dziury = [str(d0 + datetime.timedelta(days=i)) for i in range(
                (datetime.date.fromisoformat(ciag[-1]) - d0).days + 1)
                if str(d0 + datetime.timedelta(days=i)) not in daty]
            if dziury:
                print('DZIURY w harmonogramie (drip = jeden wpis na dzien): %s' % ', '.join(dziury))
        except Exception:
            pass
    sys.exit(1 if blokery else 0)


if __name__ == '__main__':
    main()
