#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Wspolne stale i helpery pipeline'u Instagrama MindSync (render.py, preview.py, social-gate.py).

Kontrakt kolejki: social/queue/<id>.json, id = YYYY-MM-DD-<slug> (opis pol: social/queue/_format.md).
Ten modul NIE zmienia kontraktu, tylko go koduje: typy, szablony, pola i limity znakow.
"""
import io
import json
import os
import glob
import re

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
SOCIAL = os.path.join(ROOT, 'social')
QUEUE = os.path.join(SOCIAL, 'queue')
MEDIA = os.path.join(SOCIAL, 'media')
PREVIEW = os.path.join(SOCIAL, 'preview')
TEMPLATES = os.path.join(SOCIAL, 'templates')

TYPY = ('carousel', 'single', 'story', 'reel')
STATUSY = ('szkic', 'gotowy', 'opublikowany', 'odrzucony')
PLATFORMY = ('instagram',)
GLOS = 'monika-v1'

FEED_WH = (1080, 1350)   # 4:5
STORY_WH = (1080, 1920)  # 9:16

# liczba slajdow i dozwolone szablony per typ
SLAJDY_TYPU = {
    'carousel': (2, 10, ('cover', 'body', 'cta', 'photo-cover', 'photo-split', 'app-screen',
                         'bold-cover', 'bold-photo-text', 'bold-statement', 'bold-myth', 'bold-save', 'bold-cta',
                         'feature-hero', 'feature-step', 'feature-before-after', 'aggro-hook', 'aggro-split')),
    'single': (1, 1, ('quote', 'cover', 'photo-cover', 'photo-quote', 'bold-cover',
                      'feature-hero', 'feature-before-after', 'aggro-hook')),
    'story': (1, 1, ('story', 'photo-story', 'bold-story', 'feature-story', 'aggro-story')),
    # reel: sceny 1080x1920 skladane w MP4 przez reel-render.py (slajd = scena)
    'reel': (2, 12, ('feature-story', 'bold-story', 'photo-story', 'story', 'reel-text', 'aggro-story')),
}

# szablony, ktore otwieraja / zamykaja karuzele (ostrzezenia bramki o kolejnosci)
OTWIERAJACE = ('cover', 'photo-cover', 'bold-cover', 'feature-hero', 'aggro-hook')
ZAMYKAJACE = ('cta', 'app-screen', 'bold-cta')

# --- Rolki (typ `reel`), kontrakt w social/queue/_format.md ---------------------------------
REEL_FPS = 30
REEL_SCENA_DOMYSLNA = 3.0          # s, gdy slajd nie ma `scena_sek` (zalecane 2.5-3.5)
REEL_SCENA_MIN, REEL_SCENA_MAX = 1.5, 10.0
REEL_CZAS_MIN, REEL_CZAS_MAX = 5.0, 90.0   # zakladka Reels: 5-90 s
REEL_MAX_BAJTOW = 300 * 1024 * 1024
REEL_PRZEJSCIA = ('cut', 'fade', 'slide')  # pierwszy = domyslny
REEL_PRZEJSCIE_SEK = 0.4                   # czas fade/slide
REEL_RUCHY = ('zoom-in', 'ken-burns')
REEL_AUDIO_ROZSZERZENIA = ('.mp3', '.m4a', '.aac', '.wav')
# pola slajdu-sceny (obok `szablon` i `pola`)
REEL_POLA_SCENY = ('scena_sek', 'przejscie', 'ruch')

# Wariant wizualny szablonu (strona tytulowa PDF, opis w _format.md):
# A = kolor i typografia, B = zdjecia z bloga, C = "bold" (kinowe kadry + duza typografia).
# D = nowosci w aplikacji (feature-*, reel-text): prawdziwe ekrany z harnessu Fluttera.
# E = nowosci w formacie agresywnym (aggro-*).
def wariant_szablonu(szablon):
    if (szablon or '').startswith('aggro-'):
        return 'E'
    if (szablon or '').startswith(('feature-', 'reel-')):
        return 'D'
    if (szablon or '').startswith('bold-'):
        return 'C'
    if 'obraz' in SZABLONY.get(szablon, {}).get('pola', {}):
        return 'B'
    return 'A'

# Szablony ze zdjeciem: pole `obraz` (sciezka repo-relative do JPG/PNG/WebP) i opcjonalne
# `pozycja` (CSS object-position, np. "center 30%"). `min_bok`: krotszy bok zrodla, ponizej
# ktorego bramka ostrzega, ze obraz bedzie powiekszany (full-bleed 1080, kadr gorny 640,
# ekran aplikacji 380).
OBRAZ_ROZSZERZENIA = ('.jpg', '.jpeg', '.png', '.webp')
POLE_OBRAZ = (240, True, 240)
POLE_POZYCJA = (40, False, 40)
POLE_UKLAD = (12, False, 12)
UKLADY = ('tekst-gora', 'tekst-dol')   # pierwszy = domyslny (chyba ze szablon ma `uklad_domyslny`)
TLA = ('ciemne', 'coral', 'piasek')    # pole `tlo` w bold-statement, pierwsze = domyslne
# Pole posta `motyw` (caly post naraz): `ciemny` = domyslny wyglad szablonow, `jasny` = jasna
# wersja (social/templates/motyw-jasny.css, prosba Darka 2026-10-19). Jasna wersje maja tylko
# szablony z MOTYW_SZABLONY; pozostale renderuja sie jak zawsze (bramka ostrzega).
MOTYWY = ('ciemny', 'jasny')           # pierwszy = domyslny
MOTYW_SZABLONY = ('feature-hero', 'feature-step', 'bold-cta')
POLE_OBRAZ_OPC = (240, False, 240)     # obraz opcjonalny (tlo-obraz w feature-hero, reel-text)
POLE_ZOOM = (5, False, 5)              # zoom_x/y/w/h: liczba px zrodla

# Pola ze sciezka do obrazu (wszystkie traktowane jak `obraz`: plik w repo, odcisk w hash_slajdow).
# `ekran*` = prawdziwy zrzut aplikacji (social/images/app-shots/<name>.png z harnessu Fluttera,
# 1179x2556, albo tymczasowo social/images/app/ios-N-ekran.png).
POLA_OBRAZOW = ('obraz', 'ekran', 'ekran_przed', 'ekran_po')
EKRAN_ZRODLO_W = 1179                  # szerokosc zrzutu z harnessu (iPhone, DPR 3)
POLA_ZOOM = ('zoom_x', 'zoom_y', 'zoom_w', 'zoom_h')
# `kadr`: jaka czesc wysokosci zrzutu pokazac w telefonie (0.3-1.0, od gory); reszta ekranu
# telefonu w kolorze dolu pokazanej czesci. Kadr, nie retusz: nic nie jest dorysowywane.
POLE_KADR = (4, False, 4)
KADR_MIN = 0.3


# --- oznaczanie tresci AI (AI Act art. 50, decyzja operatora 2026-10-02) ---------------------
# Obraz wygenerowany przez AI = plik z tych katalogow (Nano Banana Pro, hero bloga z Gemini).
# Prawdziwe zrzuty ekranu aplikacji (social/images/app-shots/, social/images/app/) NIE sa AI.
AI_PREFIKSY = ('social/assets/variant-c/', 'blog/images/')
AI_ETYKIETA = 'AI-generated image'
AI_XMP_SOURCE = 'http://cv.iptc.org/newscodes/digitalsourcetype/compositeWithTrainedAlgorithmicMedia'


def obrazy_ai_slajdu(sl):
    """Sciezki obrazow AI uzytych w slajdzie (pola z obrazem w szablonie)."""
    sl = sl or {}
    pola = sl.get('pola') or {}
    out = []
    for k in pola_obrazow_szablonu(sl.get('szablon')):
        v = str(pola.get(k) or '').replace(os.sep, '/').replace('\\', '/')
        if v.startswith(AI_PREFIKSY):
            out.append(v)
    return out


def slajd_ai(sl):
    """True, gdy slajd dostaje etykiete AI: override `ai_label` w slajdzie albo obraz AI w polach."""
    sl = sl or {}
    if isinstance(sl.get('ai_label'), bool):
        return sl['ai_label']
    return bool(obrazy_ai_slajdu(sl))


def post_ai(d):
    """True, gdy ktorykolwiek slajd posta ma etykiete AI (wtedy publikator ustawia is_ai_generated)."""
    return any(slajd_ai(sl) for sl in ((d or {}).get('slajdy') or []))


def motyw_posta(d):
    """Motyw posta z pola `motyw`; brak, pusty albo nieznany = domyslny (MOTYWY[0])."""
    m = (d or {}).get('motyw')
    return m if m in MOTYWY else MOTYWY[0]


def klasa_motywu(szablon, motyw):
    """Klasa body dla szablonu: `motyw-jasny` tylko w szablonach, ktore maja jasna wersje."""
    if motyw and motyw != MOTYWY[0] and motyw in MOTYWY and szablon in MOTYW_SZABLONY:
        return 'motyw-' + motyw
    return ''


def pola_obrazow_szablonu(szablon):
    """Pola obrazow, ktore szablon wyswietla (kolejnosc jak w POLA_OBRAZOW)."""
    pola = SZABLONY.get(szablon, {}).get('pola', {})
    return [k for k in POLA_OBRAZOW if k in pola]

# Szablony: rozmiar, pola (nazwa -> (limit_twardy, wymagane, zalecane)).
# limit_twardy: dobrany renderem testowym tak, zeby przy maksymalnej dlugosci tekst miescil sie
#   w szablonie przy minimalnym rozmiarze fontu; powyzej = BLOKER w social-gate.py.
# zalecane: dlugosc z social/queue/_format.md (pisz do tej dlugosci); powyzej = OSTRZEZENIE,
#   fit.js zmniejszy wtedy font.
SZABLONY = {
    'cover': {'wh': FEED_WH, 'pola': {
        'kicker': (32, False, 30), 'tytul': (80, True, 60), 'podtytul': (160, False, 100)}},
    'body': {'wh': FEED_WH, 'pola': {
        'numer': (3, False, 3), 'naglowek': (70, True, 50), 'tekst': (300, True, 220)}},
    'cta': {'wh': FEED_WH, 'pola': {
        'tytul': (60, True, 50), 'tekst': (180, False, 140), 'akcja': (36, True, 35)}},
    'quote': {'wh': FEED_WH, 'pola': {
        'cytat': (200, True, 160), 'autor': (50, False, 50), 'podpis': (80, False, 60)}},
    'story': {'wh': STORY_WH, 'pola': {
        'kicker': (32, False, 25), 'tytul': (70, True, 60), 'tekst': (220, False, 180)}},
    # --- warianty ze zdjeciem (limity sprawdzone renderem tekstu o maksymalnej dlugosci)
    'photo-cover': {'wh': FEED_WH, 'min_bok': 1080, 'pola': {
        'obraz': POLE_OBRAZ, 'pozycja': POLE_POZYCJA, 'uklad': POLE_UKLAD,
        'kicker': (32, False, 30), 'tytul': (70, True, 55), 'podtytul': (130, False, 90)}},
    'photo-split': {'wh': FEED_WH, 'min_bok': 640, 'pola': {
        'obraz': POLE_OBRAZ, 'pozycja': POLE_POZYCJA,
        'numer': (3, False, 3), 'naglowek': (60, True, 45), 'tekst': (200, True, 150)}},
    'photo-quote': {'wh': FEED_WH, 'min_bok': 1080, 'pola': {
        'obraz': POLE_OBRAZ, 'pozycja': POLE_POZYCJA, 'uklad': POLE_UKLAD,
        'cytat': (150, True, 120), 'podpis': (70, False, 55)}},
    'app-screen': {'wh': FEED_WH, 'min_bok': 380, 'pola': {
        'obraz': POLE_OBRAZ,
        'tytul': (50, True, 40), 'tekst': (140, False, 110), 'akcja': (30, True, 24)}},
    'photo-story': {'wh': STORY_WH, 'min_bok': 1080, 'pola': {
        'obraz': POLE_OBRAZ, 'pozycja': POLE_POZYCJA, 'uklad': POLE_UKLAD,
        'kicker': (32, False, 25), 'tytul': (70, True, 55), 'tekst': (200, False, 160)}},
    # --- wariant C "bold" (social/variant-c-koncepcja.md); szablony laduja bold.css + bold.js.
    # `akcent_dla`: pole, ktorego podciagiem musi byc `akcent` (marker); `linie`: pole
    # wielowierszowe (pozycja na linie) -> (min_linii, max_linii, limit_linii, zalecane_linii).
    'bold-cover': {'wh': FEED_WH, 'min_bok': 1080, 'uklad_domyslny': 'tekst-dol', 'akcent_dla': 'tytul', 'pola': {
        'obraz': POLE_OBRAZ, 'pozycja': POLE_POZYCJA, 'uklad': POLE_UKLAD,
        'kicker': (28, False, 24), 'tytul': (55, True, 45), 'akcent': (30, False, 20), 'podtytul': (90, False, 60)}},
    'bold-photo-text': {'wh': FEED_WH, 'min_bok': 640, 'akcent_dla': 'naglowek', 'pola': {
        'obraz': POLE_OBRAZ, 'pozycja': POLE_POZYCJA,
        'numer': (3, False, 2), 'naglowek': (50, True, 40), 'akcent': (24, False, 16), 'tekst': (150, True, 120)}},
    'bold-statement': {'wh': FEED_WH, 'akcent_dla': 'naglowek', 'pola': {
        'tlo': (8, False, 8),
        'numer': (3, False, 2), 'naglowek': (60, True, 45), 'akcent': (24, False, 16), 'tekst': (180, False, 140)}},
    'bold-myth': {'wh': FEED_WH, 'pola': {
        'numer': (3, False, 2), 'mit': (70, True, 50), 'fakt': (90, True, 70), 'podpis': (110, False, 90)}},
    'bold-save': {'wh': FEED_WH, 'linie': {'punkty': (3, 5, 40, 36)}, 'pola': {
        'kicker': (28, False, 24), 'tytul': (30, True, 26), 'punkty': (5 * 41, True, 5 * 37), 'podpis': (60, False, 45)}},
    'bold-cta': {'wh': FEED_WH, 'akcent_dla': 'tytul', 'pola': {
        'tytul': (45, True, 35), 'akcent': (20, False, 14), 'tekst': (140, False, 110), 'akcja': (24, True, 18)}},
    'bold-story': {'wh': STORY_WH, 'min_bok': 1080, 'akcent_dla': 'tytul', 'linie': {'opcje': (2, 4, 34, 30)}, 'pola': {
        'obraz': POLE_OBRAZ, 'pozycja': POLE_POZYCJA,
        'kicker': (28, False, 24), 'tytul': (55, True, 45), 'akcent': (24, False, 16),
        'opcje': (4 * 35, False, 4 * 31), 'tekst': (70, False, 50)}},
    # --- wariant D "nowosci w aplikacji": prawdziwe ekrany w mockupie telefonu (phone.css).
    # `ekran_px`: szerokosc ekranu telefonu w szablonie (bramka ostrzega, gdy zrodlo jest wezsze,
    # czyli bedzie powiekszane). Limity znakow sprawdzone renderem tekstu o maksymalnej dlugosci.
    'feature-hero': {'wh': FEED_WH, 'ekran_px': 548, 'min_bok': 1080, 'akcent_dla': 'tytul', 'pola': {
        'kadr': POLE_KADR,
        'ekran': POLE_OBRAZ, 'obraz': POLE_OBRAZ_OPC, 'pozycja': POLE_POZYCJA,
        'kicker': (28, False, 24), 'tytul': (50, True, 40), 'akcent': (24, False, 16), 'podtytul': (110, False, 80)}},
    'feature-step': {'wh': FEED_WH, 'ekran_px': 498, 'akcent_dla': 'naglowek', 'pola': {
        'kadr': POLE_KADR,
        'ekran': POLE_OBRAZ,
        'numer': (3, False, 2), 'naglowek': (50, True, 40), 'akcent': (24, False, 16), 'tekst': (160, False, 120),
        'zoom_x': POLE_ZOOM, 'zoom_y': POLE_ZOOM, 'zoom_w': POLE_ZOOM, 'zoom_h': POLE_ZOOM}},
    'feature-before-after': {'wh': FEED_WH, 'ekran_px': 398, 'akcent_dla': 'naglowek', 'pola': {
        'kadr': POLE_KADR,
        'ekran_przed': POLE_OBRAZ, 'ekran_po': POLE_OBRAZ,
        'naglowek': (50, True, 40), 'akcent': (24, False, 16), 'tekst': (140, False, 110),
        'etykieta_przed': (12, False, 10), 'etykieta_po': (12, False, 10)}},
    'feature-story': {'wh': STORY_WH, 'ekran_px': 598, 'min_bok': 1080, 'akcent_dla': 'tytul', 'pola': {
        'kadr': POLE_KADR,
        'ekran': POLE_OBRAZ, 'obraz': POLE_OBRAZ_OPC, 'pozycja': POLE_POZYCJA,
        'kicker': (28, False, 24), 'tytul': (55, True, 45), 'akcent': (24, False, 16), 'tekst': (120, False, 90)}},
    # --- wariant E "nowosci, format agresywny" (aggro.css): pattern interrupt, ogromna typografia,
    # pelne plamy coral/abyss/piasek, przechylony telefon z prawdziwym ekranem (ekran opcjonalny
    # w aggro-hook i aggro-story). `lupa`: geometria lupy zoomu dla render.py (px slajdu).
    'aggro-hook': {'wh': FEED_WH, 'ekran_px': 430, 'akcent_dla': 'tytul', 'pola': {
        'kadr': POLE_KADR,
        'tlo': (8, False, 8), 'ekran': POLE_OBRAZ_OPC,
        'kicker': (24, False, 20), 'tytul': (60, True, 45), 'akcent': (24, False, 16), 'podtytul': (110, False, 85)}},
    'aggro-split': {'wh': FEED_WH, 'ekran_px': 470, 'akcent_dla': 'naglowek',
                    'lupa': {'ew': 470, 'lewo': 455, 'gora_min': 20, 'gora_max': 470, 'max_w': 450, 'max_h': 520},
                    'pola': {
        'kadr': POLE_KADR,
                        'tlo': (8, False, 8), 'ekran': POLE_OBRAZ,
                        'numer': (3, False, 2), 'naglowek': (45, True, 34), 'akcent': (24, False, 16),
                        'tekst': (130, False, 100),
                        'zoom_x': POLE_ZOOM, 'zoom_y': POLE_ZOOM, 'zoom_w': POLE_ZOOM, 'zoom_h': POLE_ZOOM}},
    'aggro-story': {'wh': STORY_WH, 'ekran_px': 560, 'akcent_dla': 'tytul', 'pola': {
        'kadr': POLE_KADR,
        'tlo': (8, False, 8), 'ekran': POLE_OBRAZ_OPC,
        'kicker': (24, False, 20), 'tytul': (60, True, 45), 'akcent': (24, False, 16), 'tekst': (90, False, 70)}},
    'reel-text': {'wh': STORY_WH, 'min_bok': 1080, 'akcent_dla': 'tytul', 'pola': {
        'obraz': POLE_OBRAZ_OPC, 'pozycja': POLE_POZYCJA, 'tlo': (8, False, 8),
        'kicker': (28, False, 24), 'tytul': (70, True, 55), 'akcent': (30, False, 20), 'tekst': (120, False, 90)}},
}

# CSS object-position: 1-2 slowa kluczowe albo procenty/piksele, nic wiecej (wartosc trafia do stylu)
RE_POZYCJA = re.compile(r'^(?:left|right|top|bottom|center|-?\d{1,4}(?:\.\d+)?(?:%|px))'
                         r'(?:\s+(?:left|right|top|bottom|center|-?\d{1,4}(?:\.\d+)?(?:%|px)))?$')


def pozycja_ok(v):
    return bool(RE_POZYCJA.match((v or '').strip()))


def obrazy_slajdow(d):
    """[(nr_slajdu, sciezka_repo_relative)] dla slajdow z polem obrazu (`obraz`, `ekran`...)."""
    out = []
    for i, sl in enumerate(d.get('slajdy') or [], 1):
        if not isinstance(sl, dict) or not isinstance(sl.get('pola'), dict):
            continue
        for k in POLA_OBRAZOW:
            v = sl['pola'].get(k)
            if isinstance(v, str) and v.strip():
                out.append((i, v.strip().replace(chr(92), '/')))
    return out


def odcisk_pliku(path):
    """sha256 (16 znakow) zawartosci pliku albo None, gdy pliku nie ma."""
    import hashlib
    try:
        with open(path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()[:16]
    except OSError:
        return None


def wymiary_typu(typ):
    return STORY_WH if typ in ('story', 'reel') else FEED_WH


def reel_plan(d):
    """Plan rolki: ([(nr, szablon, czas_s, przejscie, ruch)], calkowity_czas_s).

    `przejscie` sceny = przejscie Z tej sceny do nastepnej (ostatnia scena go nie uzywa).
    Fade i slide nakladaja sceny na REEL_PRZEJSCIE_SEK, wiec skracaja calosc."""
    sceny = []
    slajdy = [s for s in (d.get('slajdy') or []) if isinstance(s, dict)]
    for i, sl in enumerate(slajdy, 1):
        try:
            t = float(sl.get('scena_sek') if sl.get('scena_sek') is not None else REEL_SCENA_DOMYSLNA)
        except (TypeError, ValueError):
            t = REEL_SCENA_DOMYSLNA
        prz = sl.get('przejscie') or REEL_PRZEJSCIA[0]
        sceny.append((i, sl.get('szablon'), t, prz, sl.get('ruch') or None))
    razem = sum(t for _, _, t, _, _ in sceny)
    for _, _, _, prz, _ in sceny[:-1]:
        if prz in ('fade', 'slide'):
            razem -= REEL_PRZEJSCIE_SEK
    return sceny, round(razem, 3)


def reel_media(pid):
    """Sciezki repo-relative mediow rolki: (mp4, cover.jpg)."""
    return 'social/media/%s/reel.mp4' % pid, 'social/media/%s/cover.jpg' % pid


def wczytaj(path):
    """Wczytuje JSON posta (toleruje BOM). Zwraca (dict, surowy_tekst)."""
    raw = io.open(path, encoding='utf-8-sig').read()
    return json.loads(raw), raw


def zapisz(path, d):
    """Zapis zgodny z konwencja kolejki: UTF-8 bez BOM, ensure_ascii=False, indent 2, kolejnosc kluczy zachowana."""
    tmp = path + '.tmp'
    with io.open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=2))
        f.write('\n')
    os.replace(tmp, path)


def pliki_kolejki(z_przykladami=False):
    """Pliki kolejki posortowane po nazwie. Pliki z prefiksem `_` pomijane, chyba ze z_przykladami."""
    out = []
    for p in sorted(glob.glob(os.path.join(QUEUE, '*.json'))):
        if os.path.basename(p).startswith('_') and not z_przykladami:
            continue
        out.append(p)
    return out


def znajdz(ref):
    """Zamienia <id> albo sciezke na sciezke pliku kolejki.

    Kolejnosc: istniejaca sciezka -> social/queue/<ref>.json -> social/queue/_<ref>.json ->
    plik, ktorego pole `id` == ref (takze pliki z `_`). Brak = None.
    """
    if os.path.isfile(ref):
        return os.path.abspath(ref)
    nazwa = ref[:-5] if ref.endswith('.json') else ref
    for kand in (os.path.join(QUEUE, nazwa + '.json'), os.path.join(QUEUE, '_' + nazwa + '.json')):
        if os.path.isfile(kand):
            return kand
    for p in pliki_kolejki(z_przykladami=True):
        try:
            d, _ = wczytaj(p)
        except Exception:
            continue
        if isinstance(d, dict) and d.get('id') == nazwa:
            return p
    return None


def rel(path):
    """Sciezka repo-relative z ukosnikami (forma zapisywana w polu `media`)."""
    return os.path.relpath(path, ROOT).replace(os.sep, '/')


def abs_repo(relpath):
    return os.path.join(ROOT, *relpath.replace('\\', '/').split('/'))


def hash_slajdow(d):
    """Odcisk tresci slajdow; render zapisuje go w social/media/<id>/_render.json,
    gate porownuje, zeby wykryc media starsze niz tresc."""
    import hashlib
    tresc = {'typ': d.get('typ'), 'slajdy': d.get('slajdy')}
    if d.get('typ') == 'reel':
        # okladka i muzyka zmieniaja MP4; posty innych typow maja odcisk bez zmian
        audio = d.get('audio') if isinstance(d.get('audio'), str) and d.get('audio') else None
        tresc['reel'] = {'audio': audio, 'cover_slajd': d.get('cover_slajd'),
                         'audio_sha': odcisk_pliku(abs_repo(audio)) if audio else None}
    obrazy = obrazy_slajdow(d)
    if obrazy:
        # sciezka jest juz w slajdach; odcisk zawartosci lapie podmiane pliku pod ta sama nazwa.
        # Posty bez zdjec maja odcisk bez zmian (zgodnosc ze starymi _render.json).
        tresc['obrazy'] = [[n, p, odcisk_pliku(abs_repo(p))] for n, p in obrazy]
    if motyw_posta(d) != MOTYWY[0]:
        # zmiana motywu zmienia grafiki; posty w domyslnym motywie maja odcisk bez zmian
        tresc['motyw'] = motyw_posta(d)
    payload = json.dumps(tresc, ensure_ascii=False, sort_keys=True)
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()[:16]


# --- ffmpeg / ffprobe (rolki) ----------------------------------------------------------------
def ffmpeg_exe():
    """Sciezka do ffmpeg: PATH, a w razie braku binarka z pakietu pip imageio-ffmpeg. Brak = None."""
    import shutil
    exe = shutil.which('ffmpeg')
    if exe:
        return exe
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:  # noqa: BLE001
        return None


def sonda_wideo(path):
    """Parametry pliku wideo przez ffprobe (albo `ffmpeg -i`, gdy ffprobe nie ma, np. imageio-ffmpeg).

    Zwraca dict: vcodec, profil, pix_fmt, w, h, fps, czas, acodec, audio_hz, kanaly, bajty.
    Brak narzedzi albo pliku = RuntimeError."""
    import shutil
    import subprocess
    if not os.path.isfile(path):
        raise RuntimeError('brak pliku %s' % path)
    info = {'bajty': os.path.getsize(path), 'vcodec': None, 'profil': None, 'pix_fmt': None, 'w': None,
            'h': None, 'fps': None, 'czas': None, 'acodec': None, 'audio_hz': None, 'kanaly': None}
    probe = shutil.which('ffprobe')
    if probe:
        out = subprocess.run([probe, '-v', 'error', '-show_streams', '-show_format', '-of', 'json', path],
                             capture_output=True, text=True, timeout=120)
        if out.returncode != 0:
            raise RuntimeError('ffprobe: %s' % out.stderr.strip()[:300])
        j = json.loads(out.stdout or '{}')
        for st in j.get('streams') or []:
            if st.get('codec_type') == 'video' and info['vcodec'] is None:
                num, _, den = (st.get('avg_frame_rate') or st.get('r_frame_rate') or '0/1').partition('/')
                info.update({'vcodec': st.get('codec_name'), 'profil': st.get('profile'),
                             'pix_fmt': st.get('pix_fmt'), 'w': st.get('width'), 'h': st.get('height'),
                             'fps': round(float(num) / float(den or 1), 3) if float(den or 1) else None})
            elif st.get('codec_type') == 'audio' and info['acodec'] is None:
                info.update({'acodec': st.get('codec_name'), 'audio_hz': int(st.get('sample_rate') or 0) or None,
                             'kanaly': st.get('channels')})
        try:
            info['czas'] = round(float((j.get('format') or {}).get('duration')), 3)
        except (TypeError, ValueError):
            pass
        return info
    exe = ffmpeg_exe()
    if not exe:
        raise RuntimeError('brak ffprobe i ffmpeg (zainstaluj ffmpeg albo: pip install imageio-ffmpeg)')
    err = subprocess.run([exe, '-hide_banner', '-i', path], capture_output=True, text=True, timeout=120).stderr
    m = re.search(r'Duration: (\d+):(\d+):([\d.]+)', err)
    if m:
        info['czas'] = round(int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3)), 3)
    m = re.search(r'Video: (\w+)(?: \((\w[\w ]*)\))?.*?, (\w+)(?:\([^)]*\))?, (\d+)x(\d+).*?, ([\d.]+) fps', err)
    if m:
        info.update({'vcodec': m.group(1), 'profil': m.group(2), 'pix_fmt': m.group(3),
                     'w': int(m.group(4)), 'h': int(m.group(5)), 'fps': float(m.group(6))})
    m = re.search(r'Audio: (\w+).*?, (\d+) Hz, (\w+)', err)
    if m:
        info.update({'acodec': m.group(1), 'audio_hz': int(m.group(2)),
                     'kanaly': 2 if m.group(3) == 'stereo' else (1 if m.group(3) == 'mono' else None)})
    return info


def problemy_wideo(info):
    """Lista problemow rolki wzgledem wymogow Instagrama (pusta = OK)."""
    p = []
    if info.get('vcodec') != 'h264':
        p.append('kodek wideo %s, wymagany H.264' % info.get('vcodec'))
    if info.get('pix_fmt') != 'yuv420p':
        p.append('pix_fmt %s, wymagany yuv420p' % info.get('pix_fmt'))
    if (info.get('w'), info.get('h')) != STORY_WH:
        p.append('wymiary %sx%s, wymagane 1080x1920' % (info.get('w'), info.get('h')))
    fps = info.get('fps') or 0
    if not (23 <= fps <= 60):
        p.append('fps %s poza zakresem 23-60' % fps)
    czas = info.get('czas') or 0
    if not (REEL_CZAS_MIN <= czas <= REEL_CZAS_MAX):
        p.append('czas %.1f s poza zakresem %d-%d s' % (czas, REEL_CZAS_MIN, REEL_CZAS_MAX))
    if (info.get('bajty') or 0) > REEL_MAX_BAJTOW:
        p.append('%.0f MB, limit 300 MB' % (info['bajty'] / 1048576.0))
    if not info.get('acodec'):
        p.append('brak sciezki audio (wymagana, choc cicha)')
    elif info.get('acodec') != 'aac':
        p.append('kodek audio %s, wymagany AAC' % info.get('acodec'))
    elif info.get('audio_hz') and info['audio_hz'] > 48000:
        p.append('audio %d Hz, maks. 48 kHz' % info['audio_hz'])
    return p
