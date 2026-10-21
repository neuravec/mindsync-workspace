#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kontaktowka partii postow Instagrama MindSync do akceptu operatora (READ-ONLY wobec kolejki).

Generuje social/preview/<nazwa>.html: dla kazdego posta typ, data i godzina ET (plus czas
polski), status, wynik bramki (social-gate.py), miniatury slajdow w kolejnosci, caption
z hashtagami i alt-y. Plik otwiera sie lokalnie w przegladarce (sciezki wzgledne do JPEG
w social/media/), niczego nie wysyla.

Uzycie:
    python scripts/social/preview.py --status szkic --nazwa partia-1
    python scripts/social/preview.py --all                       # nazwa = dzisiejsza data
    python scripts/social/preview.py --id _przyklad-carousel --id _przyklad-single --id _przyklad-story --nazwa przyklady
"""
import argparse
import datetime
import html
import importlib.util
import io
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social_common as sc  # noqa: E402


def _gate():
    spec = importlib.util.spec_from_file_location(
        'social_gate', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'social-gate.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def czas_pl(data, godz):
    """Godzina ET przeliczona na Europe/Warsaw (pomocniczo dla operatora); brak tzdata = None."""
    try:
        from zoneinfo import ZoneInfo
        dt = datetime.datetime.fromisoformat('%s %s' % (data, godz)).replace(tzinfo=ZoneInfo('America/New_York'))
        return dt.astimezone(ZoneInfo('Europe/Warsaw')).strftime('%d.%m %H:%M')
    except Exception:
        return None


def e(s):
    return html.escape('' if s is None else str(s), quote=True)


CSS = """
@font-face { font-family: Figtree; font-weight: 400; src: url('../templates/assets/Figtree-Regular.ttf'); }
@font-face { font-family: Figtree; font-weight: 600; src: url('../templates/assets/Figtree-SemiBold.ttf'); }
@font-face { font-family: Figtree; font-weight: 700; src: url('../templates/assets/Figtree-Bold.ttf'); }
:root { --forest:#1f3d38; --ocean:#113237; --teal:#339499; --mist:#f6fffd; --aqua:#dbf0ed; --lagoon:#bbe4de;
        --sand:#ffc88a; --beige:#ffefdd; --coral:#ff9f8a; --err:#aa2b2b; --amber:#e8af0a; }
* { box-sizing: border-box; }
body { margin: 0; background: var(--mist); color: var(--forest); font: 15px/1.5 Figtree, 'Segoe UI', Arial, sans-serif; }
header.top { padding: 28px 32px 8px; }
h1 { margin: 0 0 4px; font-size: 26px; letter-spacing: -0.3px; }
.meta { color: var(--ocean); opacity: .8; }
.post { background: #fff; border: 1px solid var(--lagoon); border-radius: 16px; margin: 20px 32px; padding: 22px 24px; }
.post h2 { margin: 0; font-size: 19px; }
.row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; margin: 6px 0 14px; }
.pill { border-radius: 999px; padding: 2px 12px; font-size: 13px; font-weight: 600; background: var(--aqua); }
.pill.typ { background: var(--beige); }
.pill.st-gotowy { background: var(--teal); color: #fff; }
.pill.st-opublikowany { background: var(--forest); color: #fff; }
.pill.st-odrzucony { background: #eee; color: #777; }
.pill.kryz { background: var(--coral); }
.pill.ok { background: #e3f4ea; color: #1d6b3a; }
.pill.warn { background: #fff4d6; color: #7a5a00; }
.pill.bad { background: #f8e0e0; color: var(--err); }
.slajdy { display: flex; gap: 14px; overflow-x: auto; padding-bottom: 8px; }
figure { margin: 0; flex: 0 0 216px; }
figure.story { flex-basis: 170px; }
figure img { width: 100%; display: block; border-radius: 10px; border: 1px solid var(--lagoon); background: var(--aqua); }
figure .brak { aspect-ratio: 4/5; border-radius: 10px; border: 1px dashed var(--coral); display: grid; place-items: center; color: var(--err); font-size: 13px; }
figure.story .brak { aspect-ratio: 9/16; }
figcaption { font-size: 12.5px; color: var(--ocean); margin-top: 6px; }
figcaption b { color: var(--teal); }
.cols { display: grid; grid-template-columns: minmax(0, 3fr) minmax(0, 2fr); gap: 22px; margin-top: 12px; }
@media (max-width: 900px) { .cols { grid-template-columns: 1fr; } .post { margin: 16px; } }
.caption { white-space: pre-wrap; background: var(--mist); border-radius: 12px; padding: 14px 16px; }
.tags { color: var(--teal); font-weight: 600; margin-top: 8px; }
.licz { font-size: 12.5px; opacity: .7; margin-top: 6px; }
ul.gate { margin: 0; padding-left: 18px; }
ul.gate li.b { color: var(--err); }
ul.gate li.o { color: #7a5a00; }
h3 { font-size: 14px; margin: 0 0 6px; text-transform: uppercase; letter-spacing: .6px; color: var(--teal); }
a { color: var(--teal); }
"""


def sceny_rolki(d, slajdy):
    """Rolka: odtwarzacz MP4 z okladka + sceny (social/media/<id>/sceny/NN.jpg) z czasami."""
    out = []
    media = d.get('media') or []
    pid = d.get('id') or ''
    rel = lambda p: os.path.relpath(sc.abs_repo(p), sc.PREVIEW).replace(os.sep, '/')  # noqa: E731
    if len(media) == 2 and os.path.isfile(sc.abs_repo(media[0])):
        out.append('<figure class="story"><video src="%s" poster="%s" controls muted playsinline '
                   'style="width:100%%;border-radius:10px"></video><figcaption><b>reel.mp4</b> '
                   '(okladka: scena %s)</figcaption></figure>'
                   % (e(rel(media[0])), e(rel(media[1])), e(d.get('cover_slajd') or 1)))
    else:
        out.append('<div class="brak">brak renderu (reel-render.py)</div>')
    sceny, razem = sc.reel_plan(d)
    t0 = 0.0
    for i, (nr, sz, t, prz, ruch) in enumerate(sceny):
        jpg = 'social/media/%s/sceny/%02d.jpg' % (pid, nr)
        img = ('<img src="%s" alt="" loading="lazy">' % e(rel(jpg))) if os.path.isfile(sc.abs_repo(jpg))             else '<div class="brak">brak sceny</div>'
        out.append('<figure class="story">%s<figcaption><b>%d/%d &middot; %s</b><br>%.1f-%.1f s'
                   '%s%s</figcaption></figure>'
                   % (img, nr, len(sceny), e(sz), t0, t0 + t, ' &middot; ruch: %s' % e(ruch) if ruch else '',
                      ' &middot; dalej: %s' % e(prz) if i < len(sceny) - 1 else ''))
        t0 += t - (sc.REEL_PRZEJSCIE_SEK if i < len(sceny) - 1 and prz in ('fade', 'slide') else 0)
    out.append('<p class="meta">Rolka: %.1f s, audio: %s</p>' % (razem, e(d.get('audio') or 'cicha sciezka AAC')))
    return out


def karta(w):
    nazwa, blok, ostrz, d, path = w
    d = d or {}
    pid = d.get('id') or nazwa
    typ = d.get('typ') or '?'
    status = d.get('status') or '?'
    data, godz = d.get('planowana_data') or '?', d.get('planowana_godzina_et') or '?'
    pl = czas_pl(data, godz)
    if blok:
        gate_pill = '<span class="pill bad">bramka: %d blokerow</span>' % len(blok)
    elif ostrz:
        gate_pill = '<span class="pill warn">bramka: %d ostrzezen</span>' % len(ostrz)
    else:
        gate_pill = '<span class="pill ok">bramka: OK</span>'
    out = ['<article class="post" id="%s">' % e(pid)]
    out.append('<h2>%s</h2>' % e(d.get('temat') or pid))
    out.append('<div class="row"><span class="pill typ">%s</span><span class="pill st-%s">%s</span>'
               '<span class="pill">%s %s ET%s</span>%s%s<span class="meta">%s</span></div>'
               % (e(typ), e(status), e(status), e(data), e(godz),
                  (' &middot; PL %s' % e(pl)) if pl else '',
                  '<span class="pill kryz">kryzysowy (988)</span>' if d.get('kryzysowy') else '',
                  gate_pill, e(nazwa)))

    slajdy = d.get('slajdy') or []
    media = d.get('media') or []
    alty = d.get('alt_text') or []
    out.append('<div class="slajdy">')
    if typ == 'reel':
        out.extend(sceny_rolki(d, slajdy))
        slajdy_feed = []
    else:
        slajdy_feed = slajdy
    for i, sl in enumerate(slajdy_feed):
        sz = (sl or {}).get('szablon', '?')
        klasa = ' class="story"' if typ in ('story', 'reel') else ''
        if i < len(media) and os.path.isfile(sc.abs_repo(media[i])):
            src = os.path.relpath(sc.abs_repo(media[i]), sc.PREVIEW).replace(os.sep, '/')
            img = '<a href="%s" target="_blank"><img src="%s" alt="%s" loading="lazy"></a>' % (
                e(src), e(src), e(alty[i] if i < len(alty) else ''))
        else:
            img = '<div class="brak">brak renderu</div>'
        alt = alty[i] if i < len(alty) else ''
        out.append('<figure%s>%s<figcaption><b>%d/%d &middot; %s</b><br>alt: %s</figcaption></figure>'
                   % (klasa, img, i + 1, len(slajdy), e(sz), e(alt) if alt else '<i>brak</i>'))
    out.append('</div>')

    cap = d.get('caption') or ''
    tagi = ' '.join(d.get('hashtagi') or [])
    dl = len(cap) + (len(tagi) + 2 if tagi else 0)
    out.append('<div class="cols"><div>')
    out.append('<h3>Caption</h3>')
    if typ == 'story':
        out.append('<div class="caption"><i>story: Instagram nie pokazuje caption</i></div>')
    else:
        out.append('<div class="caption">%s</div>' % (e(cap) or '<i>pusta</i>'))
    if tagi:
        out.append('<div class="tags">%s</div>' % e(tagi))
    out.append('<div class="licz">%d/2200 znakow z hashtagami</div>' % dl)
    zr = d.get('zrodlo')
    if isinstance(zr, dict) and zr.get('url'):
        out.append('<div class="licz">zrodlo: <a href="%s" target="_blank">%s</a></div>' % (e(zr['url']), e(zr['url'])))
    out.append('</div><div><h3>Bramka</h3>')
    if blok or ostrz:
        out.append('<ul class="gate">%s%s</ul>' % (
            ''.join('<li class="b">X %s</li>' % e(b) for b in blok),
            ''.join('<li class="o">! %s</li>' % e(o) for o in ostrz)))
    else:
        out.append('<p>Bez uwag.</p>')
    out.append('</div></div></article>')
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser(description='Kontaktowka partii IG do akceptu (HTML)')
    ap.add_argument('--all', action='store_true', help='cala kolejka (bez plikow z prefiksem _)')
    ap.add_argument('--id', action='append', default=[], help='id posta albo nazwa pliku (mozna wiele razy)')
    ap.add_argument('--status', choices=sc.STATUSY, help='posty o danym statusie (bez plikow _)')
    ap.add_argument('--nazwa', help='nazwa partii = nazwa pliku w social/preview/ (domyslnie dzisiejsza data)')
    a = ap.parse_args()
    if not (a.all or a.id or a.status):
        a.all = True  # bez argumentow = cala kolejka (bez plikow `_`), jak blog-queue-gate.py

    gate = _gate()
    wyniki = gate.zbadaj(gate.wybierz(a.id, a.all, a.status))
    wyniki.sort(key=lambda w: (str((w[3] or {}).get('planowana_data')), str((w[3] or {}).get('planowana_godzina_et')), w[0]))

    nazwa = a.nazwa or datetime.date.today().isoformat()
    nazwa = re.sub(r'[^A-Za-z0-9_.-]+', '-', nazwa).strip('-') or 'partia'
    os.makedirs(sc.PREVIEW, exist_ok=True)
    out_path = os.path.join(sc.PREVIEW, nazwa + '.html')

    blokery = sum(len(w[1]) for w in wyniki)
    ostrz = sum(len(w[2]) for w in wyniki)
    teraz = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
    doc = ['<!doctype html><html lang="pl"><head><meta charset="utf-8">',
           '<meta name="viewport" content="width=device-width, initial-scale=1">',
           '<title>Instagram: %s</title><style>%s</style></head><body>' % (e(nazwa), CSS),
           '<header class="top"><h1>Partia Instagrama: %s</h1>' % e(nazwa),
           '<div class="meta">%d postow &middot; blokerow %d &middot; ostrzezen %d &middot; wygenerowano %s'
           ' &middot; godziny w US Eastern (ET)</div></header>' % (len(wyniki), blokery, ostrz, teraz)]
    doc.extend(karta(w) for w in wyniki)
    doc.append('</body></html>')
    io.open(out_path, 'w', encoding='utf-8').write('\n'.join(doc))
    print('Preview: %s  (%d postow, blokerow %d, ostrzezen %d)' % (sc.rel(out_path), len(wyniki), blokery, ostrz))


if __name__ == '__main__':
    main()
