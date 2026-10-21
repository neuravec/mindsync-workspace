#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bramka kontrolna kolejki Instagrama MindSync (READ-ONLY, nic nie zmienia).

Wzorzec: scripts/blog-queue-gate.py. Kontrakt pol: social/queue/_format.md.

  BLOKERY (publikacja niemozliwa albo zasada twarda zlamana)
    - niepoprawny JSON, brak pola wymaganego, wartosc spoza enumu (platforma, typ, status)
    - zle `id` (wzor YYYY-MM-DD-<slug>), zla data albo godzina ET
    - liczba slajdow niezgodna z typem (carousel 2-10, single 1, story 1)
    - szablon niezgodny z typem, brak wymaganego pola slajdu, pole ponad limit znakow
    - szablon ze zdjeciem: `obraz` nie istnieje, sciezka absolutna albo poza repo, format inny
      niz JPG/PNG/WebP, plik nieczytelny; zla `pozycja` (CSS object-position) albo `uklad`;
      kontrast tekstu na zdjeciu z aktualnego renderu ponizej 3:1 (WCAG AA, duzy tekst)
    - wariant C: `akcent` nie jest fragmentem tytulu/naglowka; `punkty` (3-5) albo `opcje` (2-4)
      z inna liczba linii albo linia ponad limit; `tlo` spoza ciemne/coral/piasek
    - caption + hashtagi ponad 2200 znakow; hashtagi: wiecej niz 5, zly format, duplikaty
    - brak alt_text dla ktoregokolwiek slajdu feed
    - DLUGI MYSLNIK U+2014 albo POLPAUZA U+2013 w dowolnym polu tekstowym (TOTAL BAN)
    - `kryzysowy: true` bez "988" w caption
    - slowa kryzysowe w tresci przy `kryzysowy: false` (oznacz post jako kryzysowy)
    - zakazane obietnice medyczne (cure, diagnose, replace therapy, guaranteed...)
    - feed bez "glos": "monika-v1"
    - status `gotowy`: media niezgodne z liczba slajdow, brak pliku, nie-JPEG, zly tryb,
      zle wymiary/proporcje, ponad 8 MB, profil ICC inny niz sRGB, media starsze niz tresc
    - wariant D (feature-*): brak pliku `ekran`/`ekran_przed`/`ekran_po`; zoom_* niepelny,
      nieliczbowy albo poza zrzutem; `zrodlo.app_feature` pusty
    - rolka (`reel`): `scena_sek` poza 1.5-10 s, `przejscie` spoza cut/fade/slide, `ruch` spoza
      zoom-in/ken-burns, czas calosci poza 5-90 s, `cover_slajd` poza zakresem, `audio` bez pliku
      albo bez `audio_licencja`; przy `gotowy`: media != [reel.mp4, cover.jpg], ffprobe (H.264
      yuv420p, 1080x1920, 23-60 fps, 5-90 s, <= 300 MB, AAC), okladka JPEG 1080x1920, render
      starszy niz tresc
  OSTRZEZENIA (do decyzji czlowieka)
    - pole slajdu ponad dlugosc zalecana z _format.md (fit.js zmniejszy font), nieznane pola
    - obraz za maly: krotszy bok ponizej 1080 px dla pelnego kadru (photo-cover, photo-quote,
      photo-story), 640 dla photo-split, 380 dla app-screen; kontrast 3-4.5:1
    - kolizja: dwa posty feed o tej samej dacie i godzinie ET
    - pierwszy slajd karuzeli nie `cover`/`photo-cover`, ostatni nie `cta`/`app-screen`
    - surowy URL albo #hashtag wpisany w caption, pusta caption w feedzie
    - zrodlo wskazuje wpis, ktorego nie ma w blog/published-log.json
    - `gotowy` z data w przeszlosci, `opublikowany` bez ig_media_id
    - story bez glosu monika-v1, story z caption (IG ja ignoruje)
    - wariant D: zrzut wezszy niz ekran telefonu w szablonie (powiekszanie), zoom powiekszajacy
      ponad 1.25x, ekran spoza social/images/app-shots/ (tymczasowy), slajd bez szablonu feature-*
      w poscie z `zrodlo.app_feature`
    - rolka: wideo nie przechodzi ffprobe przy statusie szkic (bloker dopiero przy gotowy)

Uzycie:
    python scripts/social/social-gate.py --all                    # cala kolejka (bez plikow `_`)
    python scripts/social/social-gate.py --id 2026-10-06-sunday-scaries
    python scripts/social/social-gate.py --id _przyklad-carousel --id _przyklad-story
    python scripts/social/social-gate.py --status gotowy          # tylko posty gotowe (bez `_`)

Exit code 1, gdy jest choc jeden bloker.
"""
import argparse
import collections
import datetime
import io
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social_common as sc  # noqa: E402

WYMAGANE = ('id', 'platforma', 'typ', 'status', 'planowana_data', 'planowana_godzina_et',
            'glos', 'temat', 'kryzysowy', 'slajdy', 'caption', 'hashtagi', 'alt_text',
            'media', 'publikacja')
ZNANE_POLA = set(WYMAGANE) | {'zrodlo', 'audio', 'audio_licencja', 'cover_slajd', 'motyw'}
POLA_REEL = {'audio', 'audio_licencja', 'cover_slajd'}
PUSTE_OK = {'caption', 'hashtagi', 'media', 'alt_text', 'kryzysowy', 'publikacja', 'glos'}

CAPTION_MAX = 2200
HASHTAGI_MAX = 5
MAX_BAJTOW = 8 * 1024 * 1024
ZAKAZANE_ZNAKI = {chr(0x2014): 'DLUGI MYSLNIK U+2014', chr(0x2013): 'POLPAUZA U+2013'}

# pola slajdu, ktore nie sa tekstem widocznym na grafice
POLA_TECHNICZNE = {'obraz', 'pozycja', 'uklad', 'tlo', 'ekran', 'ekran_przed', 'ekran_po',
                   'zoom_x', 'zoom_y', 'zoom_w', 'zoom_h', 'kadr'}
APP_SHOTS_PREFIX = 'social/images/app-shots/'
ZOOM_MAX_SKALA = 1.25   # powiekszenie wycinka w lupie (px slajdu na px zrodla) ponad to = ostrzezenie
OBRAZ_MIN_BOK_PELNY = 1080

RE_ID = re.compile(r'^\d{4}-\d{2}-\d{2}-[a-z0-9]+(?:-[a-z0-9]+)*$')
RE_GODZ = re.compile(r'^([01]\d|2[0-3]):[0-5]\d$')
RE_HASHTAG = re.compile(r'^#[A-Za-z0-9_]+$')

# Heurystyka kryzysowa: trafienie przy `kryzysowy: false` = bloker. Lepiej falszywy alarm
# (czlowiek oznaczy post albo przeformuluje) niz post o samobojstwie bez numeru 988.
SLOWA_KRYZYSOWE = [
    r'suicid\w*', r'self[\s-]?harm\w*', r'kill(?:ing)?\s+(?:my|your|him|her|them)sel(?:f|ves)',
    r'end(?:ing)?\s+(?:my|your|their)\s+li(?:fe|ves)', r'take\s+(?:my|your)\s+own\s+life',
    r'want(?:ed|s)?\s+to\s+die', r'overdos\w*', r'cutting\s+(?:my|your)sel(?:f|ves)',
    r'hurt(?:ing)?\s+(?:my|your)sel(?:f|ves)', r'no\s+reason\s+to\s+live',
    r'better\s+off\s+dead', r'self[\s-]?injur\w*',
]
RE_KRYZYS = re.compile(r'\b(?:%s)\b' % '|'.join(SLOWA_KRYZYSOWE), re.I)

# Zakazane obietnice medyczne (YMYL). Frazy z listy NEGOWALNE nie lapia sie, gdy tuz przed
# nimi stoi przeczenie ("not a replacement for therapy" to uczciwy disclaimer).
OBIETNICE = [
    r'cur(?:e|es|ed|ing)', r'diagnos(?:e|es|ed|ing)', r'guarantee[ds]?', r'guaranteeing',
    r'clinically\s+proven', r'scientifically\s+proven', r'miracle', r'100\s?%\s+(?:effective|guaranteed)',
    r'treat(?:s|ing)?\s+(?:your\s+)?(?:depression|anxiety|ptsd|adhd|ocd|bipolar|trauma|panic)',
    r'heal(?:s|ing)?\s+(?:your\s+)?(?:depression|anxiety|trauma|ptsd)',
    r'fix(?:es)?\s+(?:your\s+)?(?:depression|anxiety|trauma)',
    r'get\s+rid\s+of\s+(?:your\s+)?(?:depression|anxiety)', r'no\s+more\s+(?:anxiety|depression|panic)',
]
NEGOWALNE = [
    r'replac(?:e|es|ed|ing)\s+(?:your\s+)?(?:therapy|therapist|treatment|medication)',
    r'(?:a\s+)?replacement\s+for\s+(?:therapy|a\s+therapist|treatment)',
    r'substitute\s+for\s+(?:therapy|a\s+therapist|treatment)',
    r'instead\s+of\s+(?:therapy|a\s+therapist|medication|treatment)',
    r'(?:you\s+)?(?:don\'t|do\s+not)\s+need\s+(?:therapy|a\s+therapist)',
]
RE_OBIETNICE = re.compile(r'\b(?:%s)\b' % '|'.join(OBIETNICE), re.I)
RE_NEGOWALNE = re.compile(r'\b(?:%s)\b' % '|'.join(NEGOWALNE), re.I)
RE_PRZECZENIE = re.compile(r"\b(?:not|never|no|isn't|is\s+not|won't|doesn't|aren't|can't)\b[\w\s,']{0,14}$", re.I)
# "you don't need therapy" sama w sobie jest przeczeniem, wiec dla niej przeczenia nie szukamy
RE_ZAWSZE = re.compile(r"(?:don't|do\s+not)\s+need", re.I)


def teksty(obj, sciezka=''):
    """Wszystkie stringi z JSON-a razem ze sciezka pola (do raportu)."""
    if isinstance(obj, str):
        yield sciezka or '(root)', obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from teksty(v, '%s.%s' % (sciezka, k) if sciezka else k)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from teksty(v, '%s[%d]' % (sciezka, i))


def tresc_widoczna(d):
    """Tekst, ktory zobaczy odbiorca: temat, slajdy, caption, hashtagi, alty."""
    out = [('temat', d.get('temat') or ''), ('caption', d.get('caption') or '')]
    for i, sl in enumerate(d.get('slajdy') or [], 1):
        for k, v in ((sl or {}).get('pola') or {}).items():
            if k in POLA_TECHNICZNE:
                continue  # sciezka obrazu i ustawienia kadru nie sa tekstem dla odbiorcy
            if isinstance(v, str):
                out.append(('slajd %d.%s' % (i, k), v))
    for i, a in enumerate(d.get('alt_text') or [], 1):
        if isinstance(a, str):
            out.append(('alt_text[%d]' % i, a))
    out.append(('hashtagi', ' '.join(h for h in (d.get('hashtagi') or []) if isinstance(h, str))))
    return out


def obietnice(tekst):
    trafienia = [m.group(0) for m in RE_OBIETNICE.finditer(tekst)]
    for m in RE_NEGOWALNE.finditer(tekst):
        if RE_ZAWSZE.search(m.group(0)):
            trafienia.append(m.group(0))
            continue
        if not RE_PRZECZENIE.search(tekst[max(0, m.start() - 40):m.start()]):
            trafienia.append(m.group(0))
    return trafienia


def sprawdz_media(d, blok, ostrz):
    """Wymogi Meta dla mediow (sprawdzane twardo przy `gotowy`)."""
    try:
        from PIL import Image
    except ImportError:
        blok.append('brak Pillow, nie da sie sprawdzic mediow (pip install pillow)')
        return
    typ = d.get('typ')
    media = d.get('media') or []
    slajdy = d.get('slajdy') or []
    if len(media) != len(slajdy):
        blok.append('media: %d plikow na %d slajdow (uruchom render.py)' % (len(media), len(slajdy)))
    oczek_w, oczek_h = sc.wymiary_typu(typ)
    for i, m in enumerate(media, 1):
        if not isinstance(m, str) or not m:
            blok.append('media[%d]: pusta sciezka' % i)
            continue
        p = sc.abs_repo(m)
        if not os.path.isfile(p):
            blok.append('media[%d]: brak pliku %s' % (i, m))
            continue
        if os.path.getsize(p) > MAX_BAJTOW:
            blok.append('media[%d]: %.1f MB (limit Meta 8 MB)' % (i, os.path.getsize(p) / 1048576))
        try:
            with Image.open(p) as im:
                fmt, mode, (w, h) = im.format, im.mode, im.size
                icc = im.info.get('icc_profile')
        except Exception as e:
            blok.append('media[%d]: nie da sie otworzyc obrazu (%s)' % (i, e))
            continue
        if fmt != 'JPEG':
            blok.append('media[%d]: format %s, Meta przyjmuje tylko JPEG' % (i, fmt))
        if mode != 'RGB':
            blok.append('media[%d]: tryb %s, wymagany RGB (sRGB)' % (i, mode))
        if not (320 <= w <= 1440):
            blok.append('media[%d]: szerokosc %d poza zakresem 320-1440' % (i, w))
        if abs(w / float(h) - oczek_w / float(oczek_h)) > 0.01:
            blok.append('media[%d]: proporcje %dx%d, dla typu %s wymagane %d:%d (%dx%d)'
                        % (i, w, h, typ, oczek_w, oczek_h, oczek_w, oczek_h))
        elif (w, h) != (oczek_w, oczek_h):
            ostrz.append('media[%d]: %dx%d zamiast standardowego %dx%d' % (i, w, h, oczek_w, oczek_h))
        if icc:
            try:
                from PIL import ImageCms
                opis = ImageCms.getProfileDescription(ImageCms.ImageCmsProfile(io.BytesIO(icc))) or ''
                if 'srgb' not in opis.lower().replace(' ', ''):
                    blok.append('media[%d]: profil ICC "%s", wymagany sRGB' % (i, opis.strip()))
            except Exception:
                ostrz.append('media[%d]: nie da sie odczytac profilu ICC' % i)
    # media starsze niz tresc slajdow (render zapisuje odcisk w _render.json)
    if media:
        man = os.path.join(sc.MEDIA, d.get('id') or '', '_render.json')
        try:
            m = json.load(io.open(man, encoding='utf-8-sig'))
            if m.get('hash_slajdow') != sc.hash_slajdow(d):
                blok.append('media starsze niz tresc slajdow (slajdy zmienione po renderze), uruchom render.py')
        except Exception:
            ostrz.append('brak social/media/<id>/_render.json, nie da sie potwierdzic, ze media sa aktualne')


def ekran_bledu_fluttera(path):
    """True, gdy zrzut to czerwony ekran bledu Fluttera (ErrorWidget w testach: tlo ok. #8b0000,
    zolty tekst). Heurystyka: ponad 35% probek ciemnoczerwonych."""
    try:
        from PIL import Image
        with Image.open(path) as im:
            mala = im.convert('RGB').resize((60, 120))
            dane = mala.get_flattened_data() if hasattr(mala, 'get_flattened_data') else mala.getdata()
            px = list(dane)
    except Exception:  # noqa: BLE001
        return False
    czerwone = sum(1 for r, g, b in px if r > 110 and g < 40 and b < 40)
    return czerwone > 0.35 * len(px)


def sprawdz_obraz(i, sz, pola, blok, ostrz, pole='obraz'):
    """Pole obrazu (`obraz`, `ekran`, `ekran_przed`, `ekran_po`) szablonu; przy `obraz`
    takze `pozycja` i `uklad`. Zwraca (w, h) zrodla albo None."""
    spec = sc.SZABLONY[sz]
    v = pola.get(pole)
    v = v.strip().replace(chr(92), '/') if isinstance(v, str) else ''
    if not v:
        return None  # brak wymaganego pola zglasza petla pol
    if os.path.isabs(v) or re.match(r'^[A-Za-z]:', v) or v.startswith('/'):
        blok.append('slajd %d (%s): `%s` musi byc sciezka wzgledem repo, nie absolutna: %s' % (i, sz, pole, v))
        return None
    p = os.path.normpath(sc.abs_repo(v))
    if not p.startswith(os.path.normpath(sc.ROOT) + os.sep):
        blok.append('slajd %d (%s): `%s` wychodzi poza repo: %s' % (i, sz, pole, v))
        return None
    if os.path.splitext(p)[1].lower() not in sc.OBRAZ_ROZSZERZENIA:
        blok.append('slajd %d (%s): `%s` %s, dozwolone %s' % (i, sz, pole, v, ', '.join(sc.OBRAZ_ROZSZERZENIA)))
        return None
    if not os.path.isfile(p):
        blok.append('slajd %d (%s): brak pliku obrazu `%s` %s' % (i, sz, pole, v))
        return None
    try:
        from PIL import Image
        with Image.open(p) as im:
            w, h = im.size
    except ImportError:
        ostrz.append('brak Pillow, nie sprawdzono rozmiaru obrazu slajdu %d' % i)
        w = h = None
    except Exception as e:
        blok.append('slajd %d (%s): nie da sie otworzyc obrazu %s (%s)' % (i, sz, v, e))
        return None
    if pole.startswith('ekran'):
        # prawdziwy zrzut w telefonie: ostrzezenie, gdy zrodlo wezsze niz ekran w szablonie
        ew = spec.get('ekran_px', 0)
        if w and w < ew:
            ostrz.append('slajd %d (%s): `%s` %dx%d wezszy niz ekran telefonu (%d px), bedzie powiekszany; '
                         'uzyj zrzutu z harnessu (app-shots.py, 1179 px)' % (i, sz, pole, w, h, ew))
        if ekran_bledu_fluttera(p):
            blok.append('slajd %d (%s): `%s` %s to czerwony ekran bledu Fluttera (shot sie wywalil); '
                        'napraw test w harnessie i uruchom app-shots.py run' % (i, sz, pole, v))
        if v.startswith(APP_SHOTS_PREFIX) and w and (w, h) != (sc.EKRAN_ZRODLO_W, 2556):
            ostrz.append('slajd %d (%s): `%s` %dx%d zamiast 1179x2556 z harnessu (wyciety widget?)' % (i, sz, pole, w, h))
        if not v.startswith(APP_SHOTS_PREFIX):
            ostrz.append('slajd %d (%s): `%s` spoza %s (ekran tymczasowy?); w poscie o nowosci uzyj '
                         'shotu z harnessu: python scripts/social/app-shots.py list' % (i, sz, pole, APP_SHOTS_PREFIX))
        return (w, h) if w else None
    min_bok = spec.get('min_bok', 0)
    if w and min(w, h) < min_bok:
        rodzaj = 'pelny kadr' if min_bok >= OBRAZ_MIN_BOK_PELNY else 'kadr szablonu'
        ostrz.append('slajd %d (%s): obraz %dx%d, krotszy bok %d < %d (%s), bedzie powiekszany; '
                     'sprawdz ostrosc na renderze' % (i, sz, w, h, min(w, h), min_bok, rodzaj))
    poz = pola.get('pozycja')
    if poz not in (None, '') and not sc.pozycja_ok(str(poz)):
        blok.append('slajd %d (%s): `pozycja` "%s" to nie CSS object-position (np. "center 30%%", "70%% center")'
                    % (i, sz, poz))
    uk = pola.get('uklad')
    if uk not in (None, '') and uk not in sc.UKLADY:
        blok.append('slajd %d (%s): `uklad` "%s" poza zestawem %s' % (i, sz, uk, '/'.join(sc.UKLADY)))
    return (w, h) if w else None


def sprawdz_zoom(i, sz, pola, wymiary, blok, ostrz):
    """Pola zoom_* (feature-step): wszystkie albo zadne, liczby, prostokat w granicach zrzutu."""
    vals = [pola.get(k) for k in sc.POLA_ZOOM]
    if all(v in (None, '') for v in vals):
        return
    try:
        x, y, w, h = (int(float(str(v))) for v in vals)
    except (TypeError, ValueError):
        blok.append('slajd %d (%s): zoom wymaga wszystkich pol zoom_x, zoom_y, zoom_w, zoom_h jako liczb px zrodla'
                    % (i, sz))
        return
    if w <= 0 or h <= 0 or x < 0 or y < 0:
        blok.append('slajd %d (%s): zoom_w/zoom_h musza byc > 0, zoom_x/zoom_y >= 0' % (i, sz))
        return
    if wymiary and (x + w > wymiary[0] or y + h > wymiary[1]):
        blok.append('slajd %d (%s): prostokat zoomu %d,%d %dx%d wychodzi poza zrzut %dx%d'
                    % (i, sz, x, y, w, h, wymiary[0], wymiary[1]))
        return
    lupa = dict({'max_w': 430, 'max_h': 520}, **(sc.SZABLONY[sz].get('lupa') or {}))
    skala = min(float(lupa['max_w']) / w, float(lupa['max_h']) / h)
    if skala > ZOOM_MAX_SKALA:
        ostrz.append('slajd %d (%s): lupa powieksza wycinek %.2fx (ponad %.2fx bedzie miekko); '
                     'wez wiekszy prostokat albo zrzut z harnessu' % (i, sz, skala, ZOOM_MAX_SKALA))


def sprawdz_bold(i, sz, pola, blok, ostrz):
    """Pola specjalne wariantu C: `akcent` (podciag pola), listy wielowierszowe, `tlo`."""
    szab = sc.SZABLONY[sz]
    cel = szab.get('akcent_dla')
    akcent = pola.get('akcent')
    if cel and isinstance(akcent, str) and akcent.strip():
        tekst = str(pola.get(cel) or '')
        if akcent.strip().lower() not in tekst.lower():
            blok.append('slajd %d (%s): `akcent` "%s" nie jest fragmentem pola `%s` (marker sie nie pojawi)'
                        % (i, sz, akcent.strip(), cel))
    for pole, (mn, mx, lim, zal) in (szab.get('linie') or {}).items():
        v = pola.get(pole)
        if v in (None, ''):
            continue  # brak wymaganego pola zglasza petla pol
        linie = [x.strip() for x in str(v).split('\n') if x.strip()]
        if not (mn <= len(linie) <= mx):
            blok.append('slajd %d (%s): `%s` ma %d linii, wymagane %d-%d (jedna pozycja na linie, rozdzielone \\n)'
                        % (i, sz, pole, len(linie), mn, mx))
        for n, linia in enumerate(linie, 1):
            if len(linia) > lim:
                blok.append('slajd %d (%s): `%s` linia %d ma %d znakow, limit %d' % (i, sz, pole, n, len(linia), lim))
            elif len(linia) > zal:
                ostrz.append('slajd %d (%s): `%s` linia %d ma %d znakow, zalecane do %d' % (i, sz, pole, n, len(linia), zal))
    tlo = pola.get('tlo')
    if 'tlo' in szab['pola'] and tlo not in (None, '') and tlo not in sc.TLA:
        blok.append('slajd %d (%s): `tlo` "%s" poza zestawem %s' % (i, sz, tlo, '/'.join(sc.TLA)))
    if 'uklad' in szab['pola'] and szab.get('uklad_domyslny') and not pola.get('uklad'):
        ostrz.append('slajd %d (%s): brak `uklad`, uzyty domyslny %s (ustawiaj jawnie)' % (i, sz, szab['uklad_domyslny']))


def sprawdz_kontrast(d, blok, ostrz):
    """Kontrast tekstu na zdjeciu zmierzony przez render.py (social/media/<id>/_render.json).
    Liczy sie tylko render aktualny wzgledem tresci; ponizej 3:1 (WCAG AA, duzy tekst) = bloker."""
    if not sc.obrazy_slajdow(d):
        return
    man = os.path.join(sc.MEDIA, d.get('id') or '', '_render.json')
    try:
        m = json.load(io.open(man, encoding='utf-8-sig'))
    except Exception:
        return
    if m.get('hash_slajdow') != sc.hash_slajdow(d):
        return
    for nr, k in sorted((m.get('kontrast') or {}).items(), key=lambda t: int(t[0])):
        try:
            v = float(k.get('min'))
        except (TypeError, ValueError):
            continue
        if v < 3.0:
            blok.append('slajd %s: kontrast tekstu na zdjeciu %.2f:1 (%s) ponizej WCAG AA 3:1; '
                        'zmien `pozycja`, `uklad` albo obraz' % (nr, v, k.get('element')))
        elif v < 4.5:
            ostrz.append('slajd %s: kontrast %.2f:1 (%s) ponizej celu 4.5:1' % (nr, v, k.get('element')))


def sprawdz_reel(d, slajdy, blok, ostrz):
    """Kontrakt rolki: sceny (czas, przejscie, ruch), czas calosci, okladka, audio."""
    for i, sl in enumerate(slajdy, 1):
        if not isinstance(sl, dict):
            continue
        t = sl.get('scena_sek')
        if t is not None:
            try:
                t = float(t)
                if not (sc.REEL_SCENA_MIN <= t <= sc.REEL_SCENA_MAX):
                    blok.append('scena %d: scena_sek %.2f poza zakresem %.1f-%.1f s'
                                % (i, t, sc.REEL_SCENA_MIN, sc.REEL_SCENA_MAX))
                elif not (1.5 <= t <= 4.0) and i not in (1, len(slajdy)):
                    ostrz.append('scena %d: scena_sek %.2f, zalecane 2.5-3.5 s (szybkie ciecia 1.5-2.5 s)' % (i, t))
            except (TypeError, ValueError):
                blok.append('scena %d: scena_sek "%s" nie jest liczba sekund' % (i, sl.get('scena_sek')))
        prz = sl.get('przejscie')
        if prz not in (None, '') and prz not in sc.REEL_PRZEJSCIA:
            blok.append('scena %d: przejscie "%s" poza zestawem %s' % (i, prz, '/'.join(sc.REEL_PRZEJSCIA)))
        ruch = sl.get('ruch')
        if ruch not in (None, '') and ruch not in sc.REEL_RUCHY:
            blok.append('scena %d: ruch "%s" poza zestawem %s' % (i, ruch, '/'.join(sc.REEL_RUCHY)))
    _, razem = sc.reel_plan(d)
    if not (sc.REEL_CZAS_MIN <= razem <= sc.REEL_CZAS_MAX):
        blok.append('rolka trwa %.1f s, wymagane %d-%d s (zakladka Reels)' % (razem, sc.REEL_CZAS_MIN, sc.REEL_CZAS_MAX))
    elif razem > 30:
        ostrz.append('rolka trwa %.1f s; rolki o nowosciach najlepiej 12-20 s' % razem)
    cov = d.get('cover_slajd', 1)
    if not isinstance(cov, int) or isinstance(cov, bool) or not (1 <= cov <= max(1, len(slajdy))):
        blok.append('cover_slajd "%s" musi byc numerem sceny 1-%d' % (cov, len(slajdy)))
    audio = d.get('audio')
    if audio not in (None, ''):
        if not isinstance(audio, str):
            blok.append('`audio` musi byc sciezka do pliku albo null (cicha sciezka)')
        else:
            p = os.path.normpath(sc.abs_repo(audio))
            if os.path.isabs(audio) or not p.startswith(os.path.normpath(sc.ROOT) + os.sep):
                blok.append('`audio` musi byc sciezka wzgledem repo: %s' % audio)
            elif os.path.splitext(p)[1].lower() not in sc.REEL_AUDIO_ROZSZERZENIA:
                blok.append('`audio` %s, dozwolone %s' % (audio, ', '.join(sc.REEL_AUDIO_ROZSZERZENIA)))
            elif not os.path.isfile(p):
                blok.append('brak pliku audio %s' % audio)
            if not str(d.get('audio_licencja') or '').strip():
                blok.append('`audio` bez `audio_licencja` (skad licencja na muzyke: zrodlo, numer licencji); '
                            'bez licencji zostaw audio null')
    if d.get('alt_text'):
        ostrz.append('rolka: alt_text nie jest wysylany do API (pole tylko jako opis)')


def sprawdz_media_reel(d, blok, ostrz, twardo):
    """Wideo rolki: social/media/<id>/reel.mp4 + cover.jpg, ffprobe i swiezosc renderu.
    `twardo` (status gotowy) = problemy sa blokerami; inaczej ostrzezeniami."""
    cel = blok if twardo else ostrz
    media = d.get('media') or []
    mp4, cover = sc.reel_media(d.get('id') or '')
    if media != [mp4, cover]:
        cel.append('media rolki: oczekiwane ["%s", "%s"] (uruchom reel-render.py), jest %s' % (mp4, cover, media))
        return
    p = sc.abs_repo(mp4)
    if not os.path.isfile(p):
        cel.append('brak pliku %s (uruchom reel-render.py)' % mp4)
        return
    try:
        info = sc.sonda_wideo(p)
    except RuntimeError as e:
        cel.append('nie da sie sprawdzic wideo: %s' % e)
        return
    for prob in sc.problemy_wideo(info):
        cel.append('reel.mp4: %s' % prob)
    pc = sc.abs_repo(cover)
    try:
        from PIL import Image
        with Image.open(pc) as im:
            if im.format != 'JPEG' or im.size != sc.STORY_WH:
                cel.append('cover.jpg: %s %dx%d, wymagany JPEG 1080x1920' % (im.format, im.size[0], im.size[1]))
            elif os.path.getsize(pc) > MAX_BAJTOW:
                cel.append('cover.jpg ponad 8 MB')
    except Exception as e:  # noqa: BLE001
        cel.append('cover.jpg: %s' % e)
    man = os.path.join(sc.MEDIA, d.get('id') or '', '_render.json')
    try:
        m = json.load(io.open(man, encoding='utf-8-sig'))
        if m.get('hash_slajdow') != sc.hash_slajdow(d):
            cel.append('rolka starsza niz tresc (sceny, okladka albo audio zmienione po renderze), uruchom reel-render.py')
    except Exception:  # noqa: BLE001
        ostrz.append('brak social/media/<id>/_render.json, nie da sie potwierdzic, ze rolka jest aktualna')


def sprawdz_zrodlo_feature(d, slajdy, zr, blok, ostrz):
    """`zrodlo` w wariancie {app_feature, frontend_commit} (post o nowosci w aplikacji)."""
    if not str(zr.get('app_feature') or '').strip():
        blok.append('`zrodlo.app_feature` pusty (nazwa funkcji, np. "habit-tracker")')
    fc = str(zr.get('frontend_commit') or '').strip()
    if not fc:
        ostrz.append('`zrodlo.frontend_commit` pusty: z jakiej wersji aplikacji sa ekrany? (app-shots.py list)')
    elif not re.match(r'^[0-9a-f]{7,40}(?:-dirty)?$', fc):
        ostrz.append('`zrodlo.frontend_commit` "%s" nie wyglada na sha commita' % fc)
    elif fc.endswith('-dirty'):
        ostrz.append('ekrany z niezacommitowanej wersji frontu (%s); przed publikacja przerenderuj z commita' % fc)
    if not any(sc.wariant_szablonu((sl or {}).get('szablon')) in ('D', 'E') for sl in slajdy if isinstance(sl, dict)):
        ostrz.append('`zrodlo.app_feature` ustawione, ale post nie ma slajdu wariantu D/E (feature-*, aggro-*)')


def opublikowane_slugi():
    p = os.path.join(sc.ROOT, 'blog', 'published-log.json')
    try:
        log = json.load(io.open(p, encoding='utf-8-sig'))
        return {x.get('slug') for x in log if isinstance(x, dict)}
    except Exception:
        return None


def sprawdz(path, slugi_bloga=None):
    blok, ostrz = [], []
    nazwa = os.path.basename(path)
    try:
        d, raw = sc.wczytaj(path)
    except Exception as e:
        return nazwa, ['niepoprawny JSON albo plik nieczytelny: %s' % e], [], None
    if not isinstance(d, dict):
        return nazwa, ['plik nie jest obiektem JSON'], [], None

    # --- TOTAL BAN myslnikow: kazde pole tekstowe, takze zagniezdzone
    for znak, opis in ZAKAZANE_ZNAKI.items():
        # po sparsowaniu, zeby zlapac tez zapis \u-escape w JSON
        trafione = [(p, s.count(znak)) for p, s in teksty(d) if znak in s]
        if trafione or znak in raw:
            blok.append('%s x%d (pola: %s). Przebuduj zdanie, nie podmieniaj znaku'
                        % (opis, sum(n for _, n in trafione) or raw.count(znak),
                           ', '.join(sorted(p for p, _ in trafione)) or 'klucze JSON'))

    # --- pola wymagane i enumy
    for p in WYMAGANE:
        if p not in d:
            blok.append('brak wymaganego pola `%s`' % p)
        elif p not in PUSTE_OK and (d[p] is None or d[p] == '' or d[p] == []):
            blok.append('puste wymagane pole `%s`' % p)
    if 'zrodlo' not in d:
        ostrz.append('brak pola `zrodlo` (null, gdy post nie pochodzi z bloga)')
    nieznane = sorted(set(d) - ZNANE_POLA)
    if nieznane:
        ostrz.append('pola spoza kontraktu: %s' % ', '.join(nieznane))
    motyw = d.get('motyw')
    if motyw not in (None, '') and motyw not in sc.MOTYWY:
        blok.append('motyw "%s" poza zestawem %s' % (motyw, '/'.join(sc.MOTYWY)))
    elif sc.motyw_posta(d) != sc.MOTYWY[0]:
        bez = [str(i) for i, sl in enumerate(d.get('slajdy') or [], 1)
               if isinstance(sl, dict) and sl.get('szablon') not in sc.MOTYW_SZABLONY]
        if bez:
            ostrz.append('motyw `%s`: slajdy %s maja szablony bez tej wersji (zostaja w domyslnym wygladzie; '
                         'motyw obsluguja: %s)' % (sc.motyw_posta(d), ', '.join(bez), ', '.join(sc.MOTYW_SZABLONY)))
    if d.get('typ') != 'reel' and set(d) & POLA_REEL:
        ostrz.append('pola rolki (%s) w poscie typu %s nic nie zmieniaja'
                     % (', '.join(sorted(set(d) & POLA_REEL)), d.get('typ')))

    pid = d.get('id') or ''
    if pid and not RE_ID.match(pid):
        blok.append('id "%s" nie pasuje do wzoru YYYY-MM-DD-<slug> (male litery, cyfry, myslniki)' % pid)
    if not nazwa.startswith('_') and pid and nazwa != pid + '.json':
        ostrz.append('nazwa pliku "%s" rozna od id "%s"' % (nazwa, pid))

    if d.get('platforma') not in sc.PLATFORMY:
        blok.append('platforma "%s" poza zestawem %s' % (d.get('platforma'), '/'.join(sc.PLATFORMY)))
    typ = d.get('typ')
    if typ not in sc.TYPY:
        blok.append('typ "%s" poza zestawem %s' % (typ, '/'.join(sc.TYPY)))
    status = d.get('status')
    if status not in sc.STATUSY:
        blok.append('status "%s" poza zestawem %s' % (status, '/'.join(sc.STATUSY)))

    data = d.get('planowana_data') or ''
    dzien = None
    try:
        dzien = datetime.date.fromisoformat(str(data))
    except ValueError:
        blok.append('planowana_data "%s" nie jest data YYYY-MM-DD' % data)
    if dzien and pid[:10] != str(dzien):
        ostrz.append('data w id (%s) rozna od planowana_data (%s)' % (pid[:10], dzien))
    godz = d.get('planowana_godzina_et') or ''
    if not RE_GODZ.match(str(godz)):
        blok.append('planowana_godzina_et "%s" nie jest godzina HH:MM (US Eastern)' % godz)
    if dzien and status == 'gotowy' and dzien < datetime.date.today():
        ostrz.append('status `gotowy`, a planowana_data %s jest w przeszlosci' % dzien)

    if not isinstance(d.get('kryzysowy'), bool):
        blok.append('pole `kryzysowy` musi byc true/false')

    feed = typ in ('carousel', 'single')
    reel = typ == 'reel'
    if (feed or reel) and d.get('glos') != sc.GLOS:
        blok.append('post feed bez "glos": "%s" (styl Moniki obowiazuje)' % sc.GLOS)
    elif typ == 'story' and d.get('glos') != sc.GLOS:
        ostrz.append('story bez "glos": "%s"' % sc.GLOS)

    # --- slajdy
    slajdy = d.get('slajdy') if isinstance(d.get('slajdy'), list) else []
    if typ in sc.SLAJDY_TYPU:
        mn, mx, dozwolone = sc.SLAJDY_TYPU[typ]
        if not (mn <= len(slajdy) <= mx):
            blok.append('typ %s wymaga %s slajdow, jest %d'
                        % (typ, str(mn) if mn == mx else '%d-%d' % (mn, mx), len(slajdy)))
        for i, sl in enumerate(slajdy, 1):
            if not isinstance(sl, dict):
                blok.append('slajd %d: nie jest obiektem' % i)
                continue
            sz = sl.get('szablon')
            if sz not in sc.SZABLONY:
                blok.append('slajd %d: nieznany szablon "%s"' % (i, sz))
                continue
            if sz not in dozwolone:
                blok.append('slajd %d: szablon "%s" niedozwolony dla typu %s (dozwolone: %s)'
                            % (i, sz, typ, ', '.join(dozwolone)))
            pola = sl.get('pola') if isinstance(sl.get('pola'), dict) else {}
            spec = sc.SZABLONY[sz]['pola']
            for pole, (limit, wymagane, zalecane) in spec.items():
                v = pola.get(pole)
                v = '' if v is None else str(v)
                if wymagane and not v.strip():
                    blok.append('slajd %d (%s): brak wymaganego pola `%s`' % (i, sz, pole))
                if len(v) > limit:
                    blok.append('slajd %d (%s): `%s` ma %d znakow, limit %d' % (i, sz, pole, len(v), limit))
                elif len(v) > zalecane:
                    ostrz.append('slajd %d (%s): `%s` ma %d znakow, zalecane do %d (limit %d), font zostanie zmniejszony'
                                 % (i, sz, pole, len(v), zalecane, limit))
            wymiary = {}
            for pole in sc.pola_obrazow_szablonu(sz):
                wymiary[pole] = sprawdz_obraz(i, sz, pola, blok, ostrz, pole)
            kd = pola.get('kadr')
            if 'kadr' in spec and kd not in (None, ''):
                try:
                    if not (sc.KADR_MIN <= float(kd) <= 1.0):
                        raise ValueError
                except (TypeError, ValueError):
                    blok.append('slajd %d (%s): `kadr` "%s" musi byc liczba %.1f-1.0 (czesc wysokosci zrzutu od gory)'
                                % (i, sz, kd, sc.KADR_MIN))
            if 'zoom_x' in spec:
                sprawdz_zoom(i, sz, pola, wymiary.get('ekran'), blok, ostrz)
            sprawdz_bold(i, sz, pola, blok, ostrz)
            if 'ai_label' in sl and not isinstance(sl.get('ai_label'), bool):
                blok.append('slajd %d: `ai_label` musi byc true albo false' % i)
            if sc.obrazy_ai_slajdu(sl) and sl.get('ai_label') is False:
                ostrz.append('slajd %d: obraz wygenerowany przez AI bez etykiety (ai_label: false); AI Act art. 50 '
                             'wymaga oznaczenia, wylacz tylko swiadomie' % i)
            extra = sorted(set(sl) - {'szablon', 'pola', 'ai_label'} - (set(sc.REEL_POLA_SCENY) if typ == 'reel' else set()))
            if extra:
                ostrz.append('slajd %d: klucze spoza kontraktu slajdu: %s%s' % (
                    i, ', '.join(extra), ' (pola scen tylko w typie reel)' if set(extra) & set(sc.REEL_POLA_SCENY) else ''))
            obce = sorted(set(pola) - set(spec))
            if obce:
                ostrz.append('slajd %d (%s): pola, ktorych szablon nie wyswietla: %s' % (i, sz, ', '.join(obce)))
        if typ == 'carousel' and slajdy:
            if (slajdy[0] or {}).get('szablon') not in sc.OTWIERAJACE:
                ostrz.append('pierwszy slajd karuzeli nie jest `cover` ani `photo-cover`')
            if (slajdy[-1] or {}).get('szablon') not in sc.ZAMYKAJACE:
                ostrz.append('ostatni slajd karuzeli nie jest `cta` ani `app-screen` (post nie prowadzi dalej)')
        if typ == 'reel':
            sprawdz_reel(d, slajdy, blok, ostrz)

    # --- alt_text
    alty = d.get('alt_text') if isinstance(d.get('alt_text'), list) else []
    if feed:
        if len(alty) != len(slajdy):
            blok.append('alt_text: %d altow na %d slajdow (kazdy slajd feed musi miec alt)' % (len(alty), len(slajdy)))
        for i, a in enumerate(alty, 1):
            if not isinstance(a, str) or not a.strip():
                blok.append('alt_text[%d] pusty' % i)
            elif len(a) > 1000:
                ostrz.append('alt_text[%d] ma %d znakow (zwiezle, do ~250)' % (i, len(a)))

    # --- caption i hashtagi
    caption = d.get('caption') if isinstance(d.get('caption'), str) else ''
    hashtagi = d.get('hashtagi') if isinstance(d.get('hashtagi'), list) else []
    if not isinstance(d.get('hashtagi'), list):
        blok.append('hashtagi musza byc lista')
    if (feed or reel) and not caption.strip():
        ostrz.append('pusta caption w poscie feed/rolce')
    if typ == 'story' and caption.strip():
        ostrz.append('story ma caption, Instagram ja zignoruje')
    pelna = caption + ('\n\n' + ' '.join(str(h) for h in hashtagi) if hashtagi else '')
    if len(pelna) > CAPTION_MAX:
        blok.append('caption z hashtagami ma %d znakow (limit IG %d)' % (len(pelna), CAPTION_MAX))
    if len(hashtagi) > HASHTAGI_MAX:
        blok.append('%d hashtagow (limit %d)' % (len(hashtagi), HASHTAGI_MAX))
    zle = [h for h in hashtagi if not isinstance(h, str) or not RE_HASHTAG.match(h)]
    if zle:
        blok.append('hashtagi w zlym formacie (wymagane #[A-Za-z0-9_]+): %s' % ', '.join(map(str, zle)))
    lower = [h.lower() for h in hashtagi if isinstance(h, str)]
    dupl = sorted({h for h in lower if lower.count(h) > 1})
    if dupl:
        blok.append('zduplikowane hashtagi: %s' % ', '.join(dupl))
    if re.search(r'(?<![\w&])#[A-Za-z]\w*', caption):
        ostrz.append('#hashtag wpisany w caption; hashtagi trzymaj w polu `hashtagi`')
    if re.search(r'https?://|www\.', caption, re.I):
        ostrz.append('URL w caption nie jest klikalny na IG; uzyj "link in bio"')

    # --- kryzys i obietnice medyczne
    kryz = d.get('kryzysowy') is True
    if kryz and '988' not in caption:
        blok.append('`kryzysowy: true`, a caption nie zawiera zasobu 988 (US Suicide & Crisis Lifeline)')
    if kryz and typ == 'story':
        ostrz.append('story kryzysowe: caption jest ignorowana, numer 988 musi byc na slajdzie')
        if not any('988' in v for k, v in tresc_widoczna(d) if k.startswith('slajd')):
            blok.append('story `kryzysowy: true` bez "988" na slajdzie')
    for pole, tekst in tresc_widoczna(d):
        if not kryz:
            hit = sorted({m.group(0).lower() for m in RE_KRYZYS.finditer(tekst)})
            if hit:
                blok.append('slowa kryzysowe w %s (%s): oznacz `kryzysowy: true` i dodaj 988, albo przeformuluj'
                            % (pole, ', '.join(hit)))
        ob = obietnice(tekst)
        if ob:
            blok.append('zakazana obietnica medyczna w %s: %s' % (pole, ', '.join(sorted({o.lower() for o in ob}))))

    # --- zrodlo
    zr = d.get('zrodlo')
    if zr is not None:
        if not isinstance(zr, dict):
            blok.append('`zrodlo` musi byc obiektem {blog_slug, url}, {app_feature, frontend_commit} albo null')
        elif 'app_feature' in zr:
            sprawdz_zrodlo_feature(d, slajdy, zr, blok, ostrz)
        else:
            slug, url = (zr.get('blog_slug') or ''), (zr.get('url') or '')
            if not url.startswith('https://www.mindsync.app/'):
                ostrz.append('zrodlo.url nie zaczyna sie od https://www.mindsync.app/')
            if slug and not url.rstrip('/').endswith('/' + slug):
                ostrz.append('zrodlo.url nie konczy sie na blog_slug "%s"' % slug)
            if slug and slugi_bloga is not None and slug not in slugi_bloga:
                ostrz.append('wpis "%s" nie jest (jeszcze) w blog/published-log.json; "link in bio" moze prowadzic donikad' % slug)

    # --- publikacja i media
    pub = d.get('publikacja') if isinstance(d.get('publikacja'), dict) else {}
    if status == 'opublikowany' and not pub.get('ig_media_id'):
        ostrz.append('status `opublikowany` bez publikacja.ig_media_id')
    sprawdz_kontrast(d, blok, ostrz)
    if not isinstance(d.get('media'), list):
        blok.append('`media` musi byc lista')
    elif reel:
        if status == 'gotowy' or d.get('media'):
            sprawdz_media_reel(d, blok, ostrz, twardo=(status == 'gotowy'))
    elif status == 'gotowy':
        sprawdz_media(d, blok, ostrz)
    elif d.get('media') and len(d['media']) != len(slajdy):
        ostrz.append('media: %d plikow na %d slajdow (przerenderuj)' % (len(d['media']), len(slajdy)))

    return nazwa, blok, ostrz, d


def zbadaj(pliki):
    """Sprawdza liste plikow i dokleja ostrzezenia o kolizjach slotow. Uzywa tez preview.py.

    Zwraca liste [nazwa, blokery, ostrzezenia, dict|None, sciezka].
    """
    slugi = opublikowane_slugi()
    wyniki = []
    for p in pliki:
        nazwa, blok, ostrz, d = sprawdz(p, slugi)
        wyniki.append([nazwa, blok, ostrz, d, p])

    # kolizje: dwa posty feed o tej samej dacie i godzinie (cala kolejka bez `_` + sprawdzane)
    sloty = collections.defaultdict(list)
    for p in sorted(set(sc.pliki_kolejki()) | set(pliki)):
        try:
            d, _ = sc.wczytaj(p)
        except Exception:
            continue
        if isinstance(d, dict) and d.get('typ') in ('carousel', 'single', 'reel') and d.get('status') != 'odrzucony':
            sloty[(str(d.get('planowana_data')), str(d.get('planowana_godzina_et')))].append(os.path.basename(p))
    for w in wyniki:
        d = w[3] or {}
        k = (str(d.get('planowana_data')), str(d.get('planowana_godzina_et')))
        inne = [n for n in sloty.get(k, []) if n != w[0]]
        if d.get('typ') in ('carousel', 'single', 'reel') and inne:
            w[2].append('KOLIZJA: ten sam slot %s %s ET co: %s' % (k[0], k[1], ', '.join(inne)))
    return wyniki


def wybierz(ids, wszystkie=False, status=None):
    """Lista sciezek wg trybow --id / --all / --status (wspolne z preview.py)."""
    pliki = []
    for ref in ids:
        p = sc.znajdz(ref)
        if not p:
            raise SystemExit('X  nie znalazlem posta: %s' % ref)
        if p not in pliki:
            pliki.append(p)
    if wszystkie or status:
        for p in sc.pliki_kolejki():
            if p in pliki:
                continue
            if status:
                try:
                    d, _ = sc.wczytaj(p)
                except Exception:
                    d = {}
                if not isinstance(d, dict) or d.get('status') != status:
                    continue
            pliki.append(p)
    return pliki


def main():
    ap = argparse.ArgumentParser(description='Bramka kolejki Instagrama MindSync (read-only)')
    ap.add_argument('--all', action='store_true', help='cala kolejka (bez plikow z prefiksem _)')
    ap.add_argument('--id', action='append', default=[], help='id posta albo nazwa pliku (mozna wiele razy)')
    ap.add_argument('--status', choices=sc.STATUSY, help='posty o danym statusie (bez plikow _)')
    a = ap.parse_args()
    if not (a.all or a.id or a.status):
        a.all = True  # bez argumentow = cala kolejka (bez plikow `_`), jak blog-queue-gate.py

    wyniki = zbadaj(wybierz(a.id, a.all, a.status))

    blokery = ostrzezenia = 0
    print('=' * 78)
    print('BRAMKA KOLEJKI INSTAGRAMA  (%d plikow)' % len(wyniki))
    print('=' * 78)
    for nazwa, blok, ostrz, d, _p in wyniki:
        d = d or {}
        znak = 'BLAD' if blok else ('uwagi' if ostrz else ' OK ')
        print('\n[%s] %-46s %s %s  %s  %s' % (znak, nazwa, d.get('planowana_data', '?'),
                                            d.get('planowana_godzina_et', '?'), d.get('typ', '?'), d.get('status', '?')))
        for b in blok:
            print('    X  %s' % b)
            blokery += 1
        for o in ostrz:
            print('    !  %s' % o)
            ostrzezenia += 1
    print('\n' + '=' * 78)
    print('PODSUMOWANIE: blokerow %d, ostrzezen %d, plikow %d' % (blokery, ostrzezenia, len(wyniki)))
    sys.exit(1 if blokery else 0)


if __name__ == '__main__':
    main()
