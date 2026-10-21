#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render slajdow Instagrama MindSync: JSON z social/queue/ -> JPEG w social/media/<id>/.

Dla kazdego slajdu bierze szablon social/templates/<szablon>.html, wstawia pola (escapowane
HTML, nowa linia -> <br>), renderuje Playwrightem (chromium, offline: font Figtree i logo
leza w social/templates/assets/), dopasowuje dlugosc tekstu (fit.js), robi zrzut PNG
i konwertuje Pillowem do JPEG sRGB q=90 (baseline, bez alfy, z profilem ICC sRGB).
Na koniec aktualizuje pole `media` w JSON (reszta pliku i kolejnosc kluczy bez zmian)
i zapisuje social/media/<id>/_render.json (odcisk tresci, ostrzezenia renderu).

Uzycie:
    python scripts/social/render.py 2026-10-06-sunday-scaries
    python scripts/social/render.py social/queue/_przyklad-carousel.json
    python scripts/social/render.py _przyklad-carousel _przyklad-single
    python scripts/social/render.py --all-szkic        # wszystkie posty `szkic` (bez plikow `_`)

Nie publikuje niczego i nie dotyka sieci. Exit code 1, gdy ktorykolwiek post sie nie wyrenderowal.
"""
import argparse
import datetime
import glob
import html
import io
import json
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social_common as sc  # noqa: E402

JPEG_QUALITY = 90


def _zaleznosci():
    brak = []
    try:
        import playwright  # noqa: F401
    except ImportError:
        brak.append('playwright')
    try:
        import PIL  # noqa: F401
    except ImportError:
        brak.append('pillow')
    if brak:
        sys.exit('Brak pakietow: %s. Zainstaluj: pip install playwright pillow && '
                 'python -m playwright install chromium' % ', '.join(brak))


def _logo_svg():
    svg = io.open(os.path.join(sc.TEMPLATES, 'assets', 'logo.svg'), encoding='utf-8').read()
    svg = re.sub(r'\swidth="[^"]*"', '', svg, count=1)
    svg = re.sub(r'\sheight="[^"]*"', '', svg, count=1)
    return svg.replace('<svg', '<svg aria-hidden="true"', 1)


def typografia(s):
    """Typograficzne apostrofy i cudzyslowy (tylko w grafice; JSON zostaje bez zmian)."""
    s = re.sub(r"(?<=\w)'(?=\w)", '’', s)             # don't -> don't (typograficzny)
    s = re.sub(r"(^|[\s(])'", lambda m: m.group(1) + '‘', s)
    s = s.replace("'", '’')
    s = re.sub(r'(^|[\s(])"', lambda m: m.group(1) + '“', s)
    s = s.replace('"', '”')
    return s


def _wartosc(v):
    if v is None:
        return ''
    s = html.escape(typografia(str(v).strip()), quote=True)
    return s.replace('\r\n', '\n').replace('\n', '<br>')


def obraz_url(sciezka):
    """Adres file:// obrazu z pola `obraz` (sciezka repo-relative). Brak pliku = ValueError."""
    p = sc.abs_repo(sciezka)
    if not os.path.isfile(p):
        raise ValueError('brak pliku obrazu %s' % sciezka)
    if os.path.splitext(p)[1].lower() not in sc.OBRAZ_ROZSZERZENIA:
        raise ValueError('obraz %s: dozwolone %s' % (sciezka, ', '.join(sc.OBRAZ_ROZSZERZENIA)))
    return pathlib.Path(p).resolve().as_uri()


# Lupa (pola zoom_*): geometria per szablon w sc.SZABLONY[<szablon>]['lupa'] (ew telefonu,
# pozycja lupy wzgledem .scena, maksymalne wymiary). Domyslnie feature-step: scena zaczyna sie
# pod tekstem (x=88 slajdu), telefon z zoomem stoi od x=-18 sceny. Lupa staje na wysokosci
# obrysowanego fragmentu ekranu, w granicach gora_min..gora_max.
LUPA_DOMYSLNA = {'ew': 498, 'lewo': 502, 'gora_min': 30, 'gora_max': 520, 'max_w': 430, 'max_h': 520}


PASEK_IOS_UDZIAL = 0.135            # wysokosc doklejanego paska statusu / szerokosc ekranu (feature.css)
APP_SHOTS_PREFIX = 'social/images/app-shots/'


def ma_pasek(sciezka):
    """Zrzut z harnessu Fluttera nie ma paska statusu iOS: render go dokleja (klasa z-paskiem)."""
    return (sciezka or '').strip().replace(chr(92), '/').startswith(APP_SHOTS_PREFIX)


def pasek_statusu(sciezka, kadr=None):
    """(klasa, styl) dla .ekran.

    - `--dol-tlo`: kolor dolnych wierszy zrzutu; ekran w telefonie jest skalowany SZEROKOSCIA
      (bez przycinania bokow), wiec zrzut krotszy niz 1179:2556 (np. sam widget) konczy sie
      w tym kolorze zamiast pustej dziury,
    - zrzut z harnessu (app-shots) dostaje pasek statusu iOS: kolor tla = srednia gornych wierszy,
      tekst ciemny albo jasny wg luminancji (jak systemowy pasek na danym ekranie)."""
    from PIL import Image
    with Image.open(sc.abs_repo(sciezka)) as im:
        rgb = im.convert('RGB')
        w, h = rgb.size
        pas = rgb.crop((0, 0, w, max(1, min(12, h)))).resize((1, 1), Image.BOX).getpixel((0, 0))
        # kolor dolu POKAZANEJ czesci: przy `kadr` wiersze tuz nad linia ciecia
        y_dol = int(h * kadr) if kadr else h
        dol = rgb.crop((0, max(0, y_dol - 12), w, max(1, y_dol))).resize((1, 1), Image.BOX).getpixel((0, 0))
    styl = '--dol-tlo: rgb(%d, %d, %d);' % dol
    if not ma_pasek(sciezka):
        return '', html.escape(styl, quote=True)
    jasne = _luminancja(pas) > 0.4
    styl += ' --pasek-tlo: rgb(%d, %d, %d); --pasek-kolor: %s;' % (pas[0], pas[1], pas[2], '#0e1d1f' if jasne else '#f6fffd')
    return 'z-paskiem', html.escape(styl, quote=True)


def zoom_wartosci(pola):
    """(x, y, w, h) z pol zoom_* jako int albo None, gdy zoomu nie ma. Zle wartosci = ValueError."""
    vals = [(pola or {}).get(k) for k in sc.POLA_ZOOM]
    if all(v in (None, '') for v in vals):
        return None
    try:
        x, y, w, h = (int(float(str(v))) for v in vals)
    except (TypeError, ValueError):
        raise ValueError('zoom: podaj wszystkie cztery pola zoom_x, zoom_y, zoom_w, zoom_h (liczby px zrodla)')
    if w <= 0 or h <= 0 or x < 0 or y < 0:
        raise ValueError('zoom: zoom_w i zoom_h musza byc > 0, zoom_x i zoom_y >= 0')
    return x, y, w, h


def lupa_szablonu(szablon):
    return dict(LUPA_DOMYSLNA, **(sc.SZABLONY.get(szablon, {}).get('lupa') or {}))


def zoom_geometria(pola, src_w, src_h, geo=None):
    """Geometria lupy: skala powiekszenia (px slajdu na px zrodla), wymiary lupy i obrys na ekranie."""
    z = zoom_wartosci(pola)
    if not z:
        return None
    x, y, w, h = z
    if x + w > src_w or y + h > src_h:
        raise ValueError('zoom: prostokat %d,%d %dx%d wychodzi poza zrzut %dx%d' % (x, y, w, h, src_w, src_h))
    geo = geo or LUPA_DOMYSLNA
    skala = min(geo['max_w'] / float(w), geo['max_h'] / float(h))
    return {'x': x, 'y': y, 'w': w, 'h': h, 'skala': skala,
            'lw': round(w * skala), 'lh': round(h * skala), 'src_w': src_w, 'src_h': src_h}


def zoom_css(pola, szablon='feature-step'):
    """Style lupy i obrysu dla feature-step; bez zoomu puste (lupa ukryta klasa)."""
    pusty = {'zoom_klasa': '', 'lupa_style': '', 'ramka_zoom_style': ''}
    if not zoom_wartosci(pola):
        return pusty
    from PIL import Image
    ekran = sc.abs_repo((pola.get('ekran') or '').strip())
    with Image.open(ekran) as im:
        src_w, src_h = im.size
    geo = lupa_szablonu(szablon)
    g = zoom_geometria(pola, src_w, src_h, geo)
    ew = geo['ew']
    pasek = ew * PASEK_IOS_UDZIAL if ma_pasek(pola.get('ekran')) else 0.0
    px = ew / float(src_w)   # px slajdu na px zrodla w telefonie
    srodek_y = ew * 0.036 + pasek + (g['y'] + g['h'] / 2.0) * px
    gora = int(min(geo['gora_max'], max(geo['gora_min'], srodek_y - g['lh'] / 2.0)))
    lupa = ("left: %dpx; top: %dpx; width: %dpx; height: %dpx; background-image: url('%s'); "
            "background-size: %.1fpx %.1fpx; background-position: -%.1fpx -%.1fpx;"
            % (geo['lewo'], gora, g['lw'], g['lh'], obraz_url(pola['ekran'].strip()),
               src_w * g['skala'], src_h * g['skala'], g['x'] * g['skala'], g['y'] * g['skala']))
    # obrys w px obrazu ekranu (obraz skalowany szerokoscia, przyciety od dolu)
    ramka = ('left: %.1fpx; top: %.1fpx; width: %.1fpx; height: %.1fpx;'
             % (g['x'] * px, g['y'] * px, g['w'] * px, g['h'] * px))
    return {'zoom_klasa': 'z-zoomem', 'lupa_style': html.escape(lupa, quote=True),
            'ramka_zoom_style': html.escape(ramka, quote=True)}


def zbuduj_html(szablon, pola, nr, razem, typ, logo, motyw=None):
    tpl_path = os.path.join(sc.TEMPLATES, szablon + '.html')
    tpl = io.open(tpl_path, encoding='utf-8').read()
    systemowe = {'nr': str(nr), 'razem': str(razem), 'typ': html.escape(typ), 'logo': logo,
                 # pole posta `motyw`: klasa body tylko w szablonach z jasna wersja (sc.MOTYW_SZABLONY)
                 'motyw_klasa': sc.klasa_motywu(szablon, motyw)}
    spec = sc.SZABLONY[szablon]['pola']
    pola = pola or {}
    kadr = None
    if 'kadr' in spec and str(pola.get('kadr') or '').strip():
        kadr = float(pola['kadr'])
        if not (sc.KADR_MIN <= kadr <= 1.0):
            raise ValueError('`kadr` %s poza zakresem %.1f-1.0' % (pola['kadr'], sc.KADR_MIN))
    systemowe['kadr_styl'] = ('clip-path: inset(0 0 %.2f%% 0);' % ((1 - kadr) * 100)) if kadr and kadr < 1 else ''
    for k in sc.pola_obrazow_szablonu(szablon):
        v = (pola.get(k) or '').strip()
        if not v:
            if spec[k][1]:
                raise ValueError('szablon %s wymaga pola `%s`' % (szablon, k))
            systemowe[k + '_url'] = ''
            systemowe[k + '_klasa'] = systemowe[k + '_styl'] = ''
            systemowe[k + '_body'] = 'bez-' + k.replace('_', '-') + 'u'   # np. bez-ekranu
            continue
        systemowe[k + '_body'] = 'z-' + k.replace('_', '-') + 'em'
        systemowe[k + '_url'] = html.escape(obraz_url(v), quote=True)
        if k.startswith('ekran'):
            systemowe[k + '_klasa'], systemowe[k + '_styl'] = pasek_statusu(v, kadr)
    if 'obraz' in spec:
        poz = (pola.get('pozycja') or '').strip()
        # wartosc trafia do atrybutu style, wiec przechodzi tylko bezpieczny wzor (inaczej center)
        systemowe['pozycja_css'] = poz if poz and sc.pozycja_ok(poz) else 'center'
        uklad = (pola.get('uklad') or '').strip()
        systemowe['uklad'] = uklad if uklad in sc.UKLADY else sc.SZABLONY[szablon].get('uklad_domyslny', sc.UKLADY[0])
        # obraz opcjonalny (wariant D): tlo jako background-image, brak = klasa bez-obrazu
        if (pola.get('obraz') or '').strip():
            styl = "background-image: url('%s'); background-position: %s;" % (
                obraz_url(pola['obraz'].strip()), systemowe['pozycja_css'])
            systemowe['obraz_tlo'] = html.escape(styl, quote=True)
            systemowe['obraz_klasa'] = 'z-obrazem'
        else:
            systemowe['obraz_tlo'] = ''
            systemowe['obraz_klasa'] = 'bez-obrazu'
    if 'zoom_x' in spec:
        systemowe.update(zoom_css(pola, szablon))
    if 'tlo' in sc.SZABLONY[szablon]['pola']:
        tlo = ((pola or {}).get('tlo') or '').strip()
        systemowe['tlo'] = tlo if tlo in sc.TLA else sc.TLA[0]

    def podstaw(m):
        k = m.group(1)
        if k in systemowe:
            return systemowe[k]
        return _wartosc((pola or {}).get(k))

    return re.sub(r'\{\{(\w+)\}\}', podstaw, tpl)


def do_jpeg(png_bytes, out_path):
    from PIL import Image, ImageCms
    im = Image.open(io.BytesIO(png_bytes))
    if im.mode != 'RGB':
        tlo = Image.new('RGB', im.size, (255, 255, 255))
        if im.mode in ('RGBA', 'LA'):
            tlo.paste(im, mask=im.split()[-1])
        else:
            tlo.paste(im.convert('RGB'))
        im = tlo
    icc = ImageCms.ImageCmsProfile(ImageCms.createProfile('sRGB')).tobytes()
    im.save(out_path, 'JPEG', quality=JPEG_QUALITY, optimize=True, progressive=False,
            subsampling=0, icc_profile=icc)


# --- kontrast tekstu na zdjeciu (WCAG 2.x) -------------------------------------------------
# Tekst w szablonach ma co najmniej 27 px, wiec liczy sie jako "duzy" w WCAG: AA = 3:1.
# Celujemy wyzej (4.5:1, AA dla zwyklego tekstu); ponizej 3:1 bramka blokuje post.
KONTRAST_AA_DUZY = 3.0
KONTRAST_CEL = 4.5

# JS: prostokaty linii tekstu kazdego widocznego .fit (Range.getClientRects) + kolor tekstu.
# Elementy .fit z wlasnym kryjacym tlem (pigulki kicker i numer) maja kontrast niezalezny
# od zdjecia (staly kolor marki), wiec sa pomijane.
JS_LINIE = """() => {
  const out = [];
  document.querySelectorAll('.fit').forEach((el, idx) => {
    if (!el.textContent.trim()) return;
    const cs = getComputedStyle(el);
    if (cs.display === 'none' || cs.visibility === 'hidden') return;
    // wlasne tlo elementu znika razem z tekstem przy pomiarze, wiec takie elementy pomijamy;
    // tlo rodzica (karta cytatu, przycisk) zostaje na zrzucie i jest mierzone normalnie
    const m = cs.backgroundColor.match(/rgba?\\(([^)]+)\\)/);
    const p = m ? m[1].split(',').map(Number) : [0, 0, 0, 0];
    const tlo = p.length < 4 || p[3] > 0.6;
    const r = document.createRange();
    r.selectNodeContents(el);
    const linie = Array.from(r.getClientRects()).filter(b => b.width > 4 && b.height > 4)
      .map(b => [b.left, b.top, b.width, b.height]);
    out.push({klasa: el.className, kolor: cs.color, wlasne_tlo: tlo, linie: linie});
  });
  return out;
}"""


def _lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


_LIN = [_lin(i) for i in range(256)]


def _luminancja(rgb):
    return 0.2126 * _LIN[rgb[0]] + 0.7152 * _LIN[rgb[1]] + 0.0722 * _LIN[rgb[2]]


def _kolor_css(s):
    m = re.search(r'rgba?\(([^)]+)\)', s or '')
    if not m:
        return None
    p = [float(x) for x in m.group(1).split(',')[:3]]
    return tuple(int(round(x)) for x in p)


def zmierz_kontrast(png_bez_tekstu, elementy):
    """[(klasa, kontrast)] dla tekstu bez wlasnego tla. Tlo = najgorszy 5% pikseli pod liniami tekstu
    (dla ciemnego tekstu najjasniejsze nie przeszkadzaja, liczy sie najciemniejsze, i odwrotnie)."""
    from PIL import Image
    im = Image.open(io.BytesIO(png_bez_tekstu)).convert('RGB')
    W, H = im.size
    wyniki = []
    for el in elementy:
        if el.get('wlasne_tlo'):
            continue
        kol = _kolor_css(el.get('kolor'))
        if not kol:
            continue
        lt = _luminancja(kol)
        lum = []
        for x, y, w, h in el.get('linie') or []:
            box = (max(0, int(x)), max(0, int(y)), min(W, int(x + w)), min(H, int(y + h)))
            if box[2] - box[0] < 2 or box[3] - box[1] < 2:
                continue
            fr = im.crop(box)
            if fr.size[0] * fr.size[1] > 40000:  # probkowanie: wystarczy siatka, nie kazdy piksel
                skala = (40000.0 / (fr.size[0] * fr.size[1])) ** 0.5
                fr = fr.resize((max(2, int(fr.size[0] * skala)), max(2, int(fr.size[1] * skala))))
            dane = fr.get_flattened_data() if hasattr(fr, 'get_flattened_data') else fr.getdata()
            lum.extend(_luminancja(p) for p in dane)
        if not lum:
            continue
        lum.sort()
        mediana = lum[len(lum) // 2]
        if lt < mediana:      # ciemny tekst na jasnym tle: najgorsze sa najciemniejsze piksele tla
            lb = lum[int(len(lum) * 0.05)]
        else:                 # jasny tekst na ciemnym tle: najgorsze sa najjasniejsze
            lb = lum[min(len(lum) - 1, int(len(lum) * 0.95))]
        hi, lo = max(lt, lb), min(lt, lb)
        wyniki.append((el.get('klasa', '').replace(' fit', '').strip(), round((hi + 0.05) / (lo + 0.05), 2)))
    return wyniki


# --- etykieta AI (AI Act art. 50; operator 2026-10-02) ----------------------------------------
# Mala, ale czytelna pigulka "AI-generated image" na dole slajdu, wysrodkowana: poza rogami
# z logo/licznikiem/Swipe i poza bocznymi pasami przycinanymi w siatce profilu. Story/rolka:
# wyzej, nad interfejsem Instagrama (pole odpowiedzi). Kontrast tekstu do tla pigulki > 10:1.
JS_ETYKIETA_AI = """(cfg) => {
  const d = document.createElement('div');
  d.textContent = cfg.tekst;
  d.setAttribute('data-ai-label', '1');
  Object.assign(d.style, {position: 'fixed', left: '50%', transform: 'translateX(-50%)',
    bottom: cfg.dol + 'px', zIndex: 9999, padding: '7px 16px', borderRadius: '10px',
    background: 'rgba(14,29,31,0.72)', color: 'rgba(246,255,253,0.96)',
    font: '500 28px Figtree, sans-serif', letterSpacing: '0.2px', whiteSpace: 'nowrap',
    pointerEvents: 'none'});
  document.body.appendChild(d);
}"""


def dopisz_xmp_ai(jpg_path):
    """Wstawia segment APP1 XMP z IPTC DigitalSourceType (obraz z udzialem AI) po SOI/APP0 JPEG-a."""
    bom = chr(0xFEFF)
    xmp = ('<?xpacket begin="' + bom + '" id="W5M0MpCehiHzreSzNTczkc9d"?>'
           '<x:xmpmeta xmlns:x="adobe:ns:meta/"><rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#">'
           '<rdf:Description rdf:about="" xmlns:Iptc4xmpExt="http://iptc.org/std/Iptc4xmpExt/2008-02-29/">'
           '<Iptc4xmpExt:DigitalSourceType>%s</Iptc4xmpExt:DigitalSourceType>'
           '</rdf:Description></rdf:RDF></x:xmpmeta><?xpacket end="w"?>') % sc.AI_XMP_SOURCE
    naglowek = b'http://ns.adobe.com/xap/1.0/'
    payload = naglowek + bytes([0]) + xmp.encode('utf-8')
    seg = bytes([0xFF, 0xE1]) + (len(payload) + 2).to_bytes(2, 'big') + payload
    data = open(jpg_path, 'rb').read()
    if data[:2] != bytes([0xFF, 0xD8]) or naglowek in data[:65536]:
        return False
    pos = 2
    if data[2:4] == bytes([0xFF, 0xE0]):  # za JFIF APP0
        pos = 4 + int.from_bytes(data[4:6], 'big')
    open(jpg_path, 'wb').write(data[:pos] + seg + data[pos:])
    return True


class BladSlajdu(Exception):
    """Slajd nie da sie wyrenderowac (nieznany szablon, brak obrazu, niezaladowany plik)."""


def renderuj_slajd(page, pid, sl, i, razem, typ, logo, motyw=None):
    """Renderuje jeden slajd do PNG. Zwraca (png_bytes, ostrzezenia, kontrast|None).
    `motyw`: pole posta `motyw` (sc.motyw_posta), None = domyslny wyglad szablonu.

    Wspolne dla render.py (JPEG slajdow) i reel-render.py (sceny rolki). Bledy = BladSlajdu."""
    szablon = (sl or {}).get('szablon')
    if szablon not in sc.SZABLONY:
        raise BladSlajdu('slajd %d: nieznany szablon `%s`' % (i, szablon))
    w, h = sc.SZABLONY[szablon]['wh']
    if (w, h) != sc.wymiary_typu(typ):
        raise BladSlajdu('slajd %d: szablon `%s` nie pasuje do typu `%s`' % (i, szablon, typ))
    try:
        doc = zbuduj_html(szablon, sl.get('pola'), i, razem, typ, logo, motyw)
    except ValueError as e:
        raise BladSlajdu('slajd %d: %s' % (i, e))
    ostrz, kontrast = [], None
    # plik tymczasowy obok szablonow, zeby wzgledne sciezki (base.css, assets/) dzialaly z file://
    tmp = os.path.join(sc.TEMPLATES, '_tmp-%s-%02d.html' % (pid, i))
    io.open(tmp, 'w', encoding='utf-8').write(doc)
    try:
        page.set_viewport_size({'width': w, 'height': h})
        page.goto('file:///' + tmp.replace(os.sep, '/'), wait_until='load')
        page.wait_for_function('window.__fit !== undefined', timeout=15000)
        fit = page.evaluate('window.__fit')
        niezaladowane = page.evaluate(
            "() => Array.from(document.images).filter(i => i.getAttribute('src') && !(i.complete && i.naturalWidth > 0)).length")
        if niezaladowane:
            pola = sl.get('pola') or {}
            raise BladSlajdu('slajd %d: obraz sie nie zaladowal (%s)'
                             % (i, ', '.join(str(pola.get(k)) for k in sc.pola_obrazow_szablonu(szablon) if pola.get(k))))
        clip = {'x': 0, 'y': 0, 'width': w, 'height': h}
        if sc.slajd_ai(sl):
            page.evaluate(JS_ETYKIETA_AI, {'tekst': sc.AI_ETYKIETA, 'dol': 440 if h >= 1900 else 30})
        png = page.screenshot(type='png', full_page=False, clip=clip)
        if sc.pola_obrazow_szablonu(szablon):
            # drugi zrzut bez tekstu = tlo, na ktorym ten tekst stoi (zdjecie + welon/karta)
            linie = page.evaluate(JS_LINIE)
            page.add_style_tag(content='.fit { visibility: hidden !important; }')
            tlo_png = page.screenshot(type='png', full_page=False, clip=clip)
            pomiar = zmierz_kontrast(tlo_png, linie)
            if pomiar:
                najs = min(pomiar, key=lambda t: t[1])
                kontrast = {'min': najs[1], 'element': najs[0], 'elementy': {k: v for k, v in pomiar}}
                if najs[1] < KONTRAST_AA_DUZY:
                    ostrz.append('slajd %d: KONTRAST %.2f:1 (%s) ponizej WCAG AA 3:1 dla duzego tekstu, '
                                 'zmien kadr (pozycja) albo obraz' % (i, najs[1], najs[0]))
                elif najs[1] < KONTRAST_CEL:
                    ostrz.append('slajd %d: kontrast %.2f:1 (%s) spelnia AA dla duzego tekstu, ponizej celu 4.5:1'
                                 % (i, najs[1], najs[0]))
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass
    if not fit.get('font_ok', True):
        ostrz.append('slajd %d: font Figtree sie nie zaladowal, uzyty fallback (sprawdz social/templates/assets/)' % i)
    if fit.get('blad_haka'):
        ostrz.append('slajd %d: skrypt ukladu w szablonie (hak po fit.js) rzucil blad: %s' % (i, fit['blad_haka']))
    if fit.get('overflow'):
        ostrz.append('slajd %d: tekst nie miesci sie nawet przy minimalnym foncie, skroc go' % i)
    elif fit.get('skala', 1) < 1:
        ostrz.append('slajd %d: font zmniejszony do %d%% (tekst dlugi)' % (i, round(fit['skala'] * 100)))
    return png, ostrz, kontrast


def renderuj_post(path, page):
    d, _ = sc.wczytaj(path)
    pid = (d.get('id') or '').strip()
    if not pid:
        return False, ['brak pola `id`']
    typ = d.get('typ')
    slajdy = d.get('slajdy') or []
    if typ not in sc.TYPY:
        return False, ['nieznany typ `%s`' % typ]
    if typ == 'reel':
        return False, ['typ `reel` renderuje scripts/social/reel-render.py (sceny + MP4)']
    if not slajdy:
        return False, ['brak slajdow']

    out_dir = os.path.join(sc.MEDIA, pid)
    os.makedirs(out_dir, exist_ok=True)
    logo = _logo_svg()
    ostrz, media, kontrasty = [], [], {}
    razem = len(slajdy)
    motyw = sc.motyw_posta(d)
    for i, sl in enumerate(slajdy, 1):
        try:
            png, o, k = renderuj_slajd(page, pid, sl, i, razem, typ, logo, motyw)
        except BladSlajdu as e:
            return False, [str(e)]
        ostrz.extend(o)
        if k:
            kontrasty[str(i)] = k
        out = os.path.join(out_dir, '%02d.jpg' % i)
        do_jpeg(png, out)
        if sc.slajd_ai(sl):
            dopisz_xmp_ai(out)
        media.append(sc.rel(out))

    # sprzatanie: stare slajdy z poprzedniego renderu (np. bylo 7, jest 5)
    for stary in glob.glob(os.path.join(out_dir, '*.jpg')):
        if sc.rel(stary) not in media:
            os.remove(stary)

    manifest = {
        'id': pid,
        'hash_slajdow': sc.hash_slajdow(d),
        'wyrenderowano': datetime.datetime.now().isoformat(timespec='seconds'),
        'media': media,
        'ostrzezenia': ostrz,
    }
    obrazy = sc.obrazy_slajdow(d)
    if obrazy:
        # sciezka i odcisk zrodla kazdego zdjecia (hash_slajdow tez je zawiera, wiec podmiana
        # pliku po renderze = media nieaktualne w bramce) + zmierzony kontrast tekstu
        manifest['obrazy'] = [{'slajd': n, 'obraz': p, 'sha256_16': sc.odcisk_pliku(sc.abs_repo(p))}
                              for n, p in obrazy]
        manifest['kontrast'] = kontrasty
    sc.zapisz(os.path.join(out_dir, '_render.json'), manifest)

    d['media'] = media
    sc.zapisz(path, d)
    return True, ostrz


def main():
    ap = argparse.ArgumentParser(description='Render slajdow IG MindSync do JPEG')
    ap.add_argument('posty', nargs='*', help='id posta albo sciezka do JSON')
    ap.add_argument('--all-szkic', action='store_true', help='wszystkie posty o statusie szkic (bez plikow _)')
    a = ap.parse_args()

    sciezki = []
    for ref in a.posty:
        p = sc.znajdz(ref)
        if not p:
            print('X  nie znalazlem posta: %s' % ref)
            sys.exit(1)
        sciezki.append(p)
    if a.all_szkic:
        for p in sc.pliki_kolejki():
            try:
                d, _ = sc.wczytaj(p)
            except Exception:
                continue
            if d.get('typ') == 'reel':
                print('--  %s: rolka, renderuje ja reel-render.py' % os.path.basename(p))
                continue
            if d.get('status') == 'szkic' and p not in sciezki:
                sciezki.append(p)
    if not sciezki:
        ap.error('podaj id/sciezke posta albo --all-szkic')

    _zaleznosci()
    from playwright.sync_api import sync_playwright

    bledy = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--allow-file-access-from-files', '--force-color-profile=srgb'])
        page = browser.new_page(device_scale_factor=1)
        for p in sciezki:
            nazwa = os.path.basename(p)
            try:
                ok, ostrz = renderuj_post(p, page)
            except Exception as e:
                ok, ostrz = False, ['wyjatek: %s' % e]
            print('[%s] %s' % (' OK ' if ok else 'BLAD', nazwa))
            for o in ostrz:
                print('    %s  %s' % ('!' if ok else 'X', o))
            if not ok:
                bledy += 1
        browser.close()
    print('\nWyrenderowano %d/%d postow.' % (len(sciezki) - bledy, len(sciezki)))
    sys.exit(1 if bledy else 0)


if __name__ == '__main__':
    main()
