#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Mechaniczna kontrola glosu bloga MindSync: styl Moniki (READ-ONLY, nic nie zmienia).

Dotyczy wpisow z polem `"glos": "monika-v1"` w JSON-ie kolejki (wszystkie wpisy pisane
od 2026-09-25 przez skill /blog-write). Specyfikacja stylu: docs/blog/brand-mindsync.md §2,
wzorzec: docs/blog/voice-sample-monika.md.

Skrypt lapie to, co da sie sprawdzic maszynowo. Nie zastepuje akceptu `brand-voice-manager`
(checklist §2.5), tylko pilnuje, zeby wpis w ogole mial jej szkielet.

  BLOKERY
    - em-dash U+2014 albo polpauza U+2013 w dowolnym polu tekstowym
    - emoji w tytule, zajawce albo tresci
    - brak osobistego pytania do czytelnika w ostatnim akapicie przed FAQ
    - brak akapitu o apce (wzmianka "MindSync" w sekcji przed FAQ) albo brak karty [FEATURE:]
    - stopka newslettera przeniesiona na blog ("hit reply", "reply and tell us", ...)

  OSTRZEZENIA
    - otwarcie (tekst przed pierwszym H2) bez pytania i bez listy scenek
    - otwarcie 60-120 slow poza zakresem
    - tresc bez FAQ poza zakresem 800-1600 slow
    - brak roku badania (19xx/20xx) w tresci
    - brak listy krokow (<ul>/<ol>) w tresci przed FAQ
    - zdania wygladajace na zmyslona anegdote w pierwszej osobie (do recznej oceny)

Uzycie:
    python scripts/blog-voice-check.py blog/queue/2026-10-01_slug.json [...]
    python scripts/blog-voice-check.py --wszystkie     # kazdy JSON kolejki z glos=monika-v1
Kod wyjscia 1, gdy jest choc jeden bloker.
"""
import glob, io, json, os, re, sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
QUEUE = os.path.join(ROOT, 'blog', 'queue')
GLOS = 'monika-v1'
FAQ_H = 'Frequently asked questions'
POLA_TEKSTOWE = ('tytul', 'tresc_html', 'zajawka_html', 'meta_title', 'meta_description',
                 'hero_image_alt')
EMOJI = re.compile('[\U0001F300-\U0001FAFF\U00002600-\U000027BF\U0001F000-\U0001F2FF]')
STOPKA = re.compile(r'(?i)hit reply|reply and tell us|hit and tell us|we promise to only send you'
                    r'|share your experience|curious what we.ve been building')
ANEGDOTA = re.compile(r"(?i)\b(I (have|had|was|used to|remember|spent|tried|went|told)|I've been"
                      r"|I'm not good at|my (therapist|partner|mom|mother|dad|friend|habit|husband|wife))\b")


def bez_html(s):
    s = re.sub(r'(?s)<[^>]+>', ' ', s or '')
    return re.sub(r'\s+', ' ', s).strip()


def sprawdz_glos(d):
    """Zwraca (blokery, ostrzezenia) dla slownika wpisu z kolejki."""
    blok, ostrz = [], []

    for pole in POLA_TEKSTOWE:
        v = d.get(pole) or ''
        if not isinstance(v, str):
            continue
        for znak, nazwa in ((chr(0x2014), 'em-dash U+2014'), (chr(0x2013), 'polpauza U+2013')):
            if znak in v:
                blok.append('%s x%d w polu `%s` (przebuduj zdanie, nie podmieniaj znaku)'
                            % (nazwa, v.count(znak), pole))
        if pole in ('tytul', 'tresc_html', 'zajawka_html') and EMOJI.search(v):
            blok.append('emoji w polu `%s` (na blogu zero emoji, brand doc §2.3)' % pole)

    html = d.get('tresc_html') or ''
    poz_faq = html.find(FAQ_H)
    przed_faq = html[:poz_faq] if poz_faq > -1 else html

    if STOPKA.search(bez_html(html)):
        blok.append('stopka newslettera na blogu ("hit reply" itp.), brand doc §2.3')

    # ostatni akapit przed FAQ = pytanie do czytelnika
    akapity = re.findall(r'(?is)<p[^>]*>(.*?)</p>', przed_faq)
    akapity = [bez_html(a) for a in akapity if bez_html(a) and not bez_html(a).startswith('[FEATURE')]
    if not akapity or not akapity[-1].rstrip().endswith('?'):
        blok.append('ostatni akapit przed FAQ nie jest pytaniem do czytelnika (brand doc §2.1 pkt 10)')

    # apka na koncu: MindSync w ostatnich ~40% tresci przed FAQ + karta
    tekst_przed = bez_html(przed_faq)
    if 'MindSync' not in tekst_przed[int(len(tekst_przed) * 0.6):]:
        blok.append('brak akapitu o apce pod koniec wpisu, przed FAQ (brand doc §2.1 pkt 9)')
    if '[FEATURE' not in html:
        blok.append('brak karty [FEATURE:] (apka zawsze na koncu wpisu)')

    # otwarcie = wszystko przed pierwszym H2
    m = re.search(r'(?is)<h2\b', przed_faq)
    otwarcie_html = przed_faq[:m.start()] if m else przed_faq
    otwarcie = bez_html(otwarcie_html)
    slow = len(otwarcie.split())
    if '?' not in otwarcie and '<ul' not in otwarcie_html.lower():
        ostrz.append('otwarcie bez pytania i bez listy scenek (brand doc §2.1 pkt 1)')
    if not (60 <= slow <= 120):
        ostrz.append('otwarcie ma %d slow (cel 60-120)' % slow)

    slow_tresci = len(tekst_przed.split())
    if not (800 <= slow_tresci <= 1600):
        ostrz.append('tresc bez FAQ ma %d slow (cel 900-1400, tolerancja 800-1600)' % slow_tresci)

    if not re.search(r'\b(19[5-9]\d|20[0-2]\d)\b', tekst_przed):
        ostrz.append('brak roku badania w tresci (badania opowiadane z rokiem, §2.1 pkt 3)')
    if not re.search(r'(?i)<(ul|ol)\b', przed_faq[len(otwarcie_html):]):
        ostrz.append('brak listy krokow w czesci praktycznej (§2.1 pkt 7)')

    for z in sorted(set(x.group(0) for x in ANEGDOTA.finditer(tekst_przed))):
        ostrz.append('pierwsza osoba "%s": sprawdz, czy to nie zmyslona anegdota (§2.3)' % z)

    return blok, ostrz


def main(argv):
    if not argv or argv == ['-h'] or argv == ['--help']:
        print(__doc__)
        return 0
    if argv == ['--wszystkie']:
        pliki = []
        for p in sorted(glob.glob(os.path.join(QUEUE, '*.json'))):
            if os.path.basename(p).startswith('_'):
                continue
            try:
                d = json.load(io.open(p, encoding='utf-8-sig'))
            except Exception:
                continue
            if isinstance(d, dict) and d.get('glos') == GLOS:
                pliki.append(p)
    else:
        pliki = argv
    if not pliki:
        print('Brak wpisow z "glos": "%s" w kolejce.' % GLOS)
        return 0

    bledy = 0
    for p in pliki:
        d = json.load(io.open(p, encoding='utf-8-sig'))
        blok, ostrz = sprawdz_glos(d)
        if d.get('glos') != GLOS:
            blok.insert(0, 'brak pola "glos": "%s" (wpis nie przeszedl sciezki /blog-write)' % GLOS)
        znak = 'BLAD' if blok else ('uwagi' if ostrz else ' OK ')
        print('\n[%s] %s' % (znak, os.path.basename(p)))
        for b in blok:
            print('   BLOKER  %s' % b)
        for o in ostrz:
            print('   uwaga   %s' % o)
        bledy += bool(blok)
    print('\nPODSUMOWANIE: plikow %d, z blokerami %d' % (len(pliki), bledy))
    return 1 if bledy else 0


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main(sys.argv[1:]))
