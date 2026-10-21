#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Eksport postow Instagrama MindSync do PDF dla grafika (A4 pionowo, READ-ONLY wobec kolejki).

Strona tytulowa (opis + spis postow podzielony na warianty), potem kazdy post na osobnej
stronie: naglowek (typ, data, temat), slajdy w siatce 3 kolumny (karuzela 7+ slajdow: 4; story pojedynczo, single
wiekszy), pod spodem caption z hashtagami i alt-y. Caption ma `break-inside: avoid`, wiec
nie dzieli sie miedzy strony, jesli tylko miesci sie na jednej.

Warianty (strona tytulowa + strona-przekladka przed kazdym wariantem):
    A: kolor i typografia             (cover, body, cta, quote, story)
    B: zdjecia z bloga                (photo-*, app-screen)
    C: odwazny, obrazy Nano Banana Pro (bold-*)
    D: nowosci w aplikacji, prawdziwe ekrany z harnessu Fluttera (feature-*, reel-text)
    E: nowosci, format agresywny (aggro-*)
Post nalezy do najwyzszego wariantu, ktorego szablon zawiera (E > D > C > B > A).
Rolka (typ reel): storyboard scen (social/media/<id>/sceny/NN.jpg) z czasami na osi, okladka,
sciezka do reel.mp4 i parametry wideo z _render.json.

Uzycie:
    python scripts/social/pdf-export.py --all-przyklady
    python scripts/social/pdf-export.py --id _przyklad-carousel --id _przyklad-story-photo --nazwa probka
    python scripts/social/pdf-export.py --status szkic --nazwa partia-1

Wynik: social/preview/<nazwa>.pdf (domyslnie przy --all-przyklady: MindSync-Instagram-przyklady).
HTML jest zapisywany do pliku obok i otwierany przez file:// (set_content nie laduje obrazow
file://), po wydruku plik HTML jest usuwany (--zostaw-html zostawia go do podgladu).
Media musza byc wyrenderowane (render.py); brak JPEG albo niezaladowany obraz = exit 1.
"""
import argparse
import datetime
import html
import importlib.util
import io
import os
import pathlib
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social_common as sc  # noqa: E402

DOMYSLNA_NAZWA = 'MindSync-Instagram-przyklady'
WARIANTY = (
    ('A', 'Wariant A: kolor i typografia',
     'Jasne tła w palecie marki i sama typografia Figtree, bez zdjęć: najszybsze w produkcji '
     'i spokojne na siatce profilu.'),
    ('B', 'Wariant B: zdjęcia z bloga',
     'Ilustracje z hero wpisów bloga i prawdziwe zrzuty ekranu aplikacji, zdjęcie przechodzi '
     'w jasną mgłę, a tekst stoi na jasnym tle.'),
    ('C', 'Wariant C: odważny, obrazy Nano Banana Pro',
     'Ciemne, kinowe kadry generowane pod post, ogromny tytuł z piaskowym markerem i slajdy '
     'do zapisania, żeby zatrzymać kciuk w feedzie.'),
    ('D', 'Wariant D: nowości w aplikacji (prawdziwe ekrany)',
     'Posty i rolki o nowych funkcjach i zmianach. Ekrany renderuje automat prosto z kodu aplikacji '
     '(harness Fluttera, 1179x2556), a szablon wkłada je w mockup telefonu, dodaje lupę na detal '
     'albo zestawienie przed i teraz. Zero makiet i zero fałszywych zrzutów.'),
    ('E', 'Wariant E: nowości, format agresywny',
     'Ten sam materiał co D, podany najgłośniej w całym zestawie: hook typu pattern interrupt, '
     'pełne plamy coral i piasku, typografia do 190 px, przechylony telefon z prawdziwym ekranem '
     'i szybkie cięcia w rolce. Bez straszenia, bez obietnic medycznych, bez zmyślonych funkcji.'),
)
TYPY_PL = {'carousel': 'Karuzela', 'single': 'Pojedynczy post', 'story': 'Story', 'reel': 'Rolka'}


def _gate():
    spec = importlib.util.spec_from_file_location(
        'social_gate', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'social-gate.py'))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def e(s):
    return html.escape('' if s is None else str(s), quote=True)


def wariant(d):
    """Najwyzszy wariant szablonow posta (E > D > C > B > A), wg sc.wariant_szablonu."""
    return max([sc.wariant_szablonu((sl or {}).get('szablon')) for sl in d.get('slajdy') or []] or ['A'])


CSS = """
@font-face { font-family: Figtree; font-weight: 400; src: url('../templates/assets/Figtree-Regular.ttf'); }
@font-face { font-family: Figtree; font-weight: 600; src: url('../templates/assets/Figtree-SemiBold.ttf'); }
@font-face { font-family: Figtree; font-weight: 700; src: url('../templates/assets/Figtree-Bold.ttf'); }
@page { size: A4 portrait; margin: 14mm 14mm 14mm 14mm; }
:root { --forest:#1f3d38; --ocean:#113237; --teal:#339499; --mist:#f6fffd; --aqua:#dbf0ed; --lagoon:#bbe4de;
        --sand:#ffc88a; --beige:#ffefdd; }
* { box-sizing: border-box; }
html, body { margin: 0; padding: 0; }
body { font: 9.5pt/1.45 Figtree, 'Segoe UI', Arial, sans-serif; color: var(--forest); background: #fff;
       -webkit-print-color-adjust: exact; print-color-adjust: exact; }
.strona { page-break-after: always; break-after: page; }
.strona:last-child { page-break-after: auto; break-after: auto; }
h1 { font-size: 26pt; line-height: 1.1; letter-spacing: -0.5px; margin: 8mm 0 3mm; }
h2 { font-size: 15pt; margin: 0 0 1.5mm; letter-spacing: -0.2px; }
h3 { font-size: 8pt; text-transform: uppercase; letter-spacing: 0.8px; color: var(--teal); margin: 0 0 1.5mm; }
.lead { font-size: 11pt; color: var(--ocean); max-width: 165mm; margin: 0 0 6mm; }
.meta { color: var(--ocean); opacity: .75; font-size: 8.5pt; }
.wariant { border: 0.3mm solid var(--lagoon); border-radius: 4mm; padding: 4mm 6mm; margin: 0 0 4mm; break-inside: avoid; }
.wariant p { margin: 0 0 3mm; color: var(--ocean); }
.miniatury { display: flex; gap: 4mm; flex-wrap: wrap; align-items: flex-end; }
.mini { width: 22mm; }
.mini.pion { width: 17mm; }
.mini img { width: 100%; display: block; border-radius: 1.5mm; border: 0.2mm solid var(--lagoon); }
.mini span { display: block; font-size: 7.5pt; color: var(--ocean); margin-top: 1mm; line-height: 1.25; }
.znak { display: flex; align-items: center; gap: 3mm; font-weight: 600; font-size: 12pt; color: var(--ocean); }
.znak svg { width: 9mm; height: 9mm; }
.naglowek { display: flex; justify-content: space-between; align-items: baseline; gap: 6mm;
            border-bottom: 0.3mm solid var(--lagoon); padding-bottom: 2.5mm; margin-bottom: 4mm; }
.pill { display: inline-block; border-radius: 99px; padding: 0.4mm 2.6mm; font-size: 7.5pt; font-weight: 600;
        background: var(--aqua); margin-right: 1.5mm; }
.pill.b { background: var(--beige); }
.siatka { display: grid; grid-template-columns: repeat(3, 1fr); gap: 3mm 4mm; width: 158mm; }
.siatka.single { grid-template-columns: 1fr 1fr; width: 100%; }
figure { margin: 0; break-inside: avoid; }
figure img { width: 100%; display: block; border-radius: 1.5mm; border: 0.2mm solid var(--lagoon); }
figcaption { font-size: 7pt; color: var(--ocean); margin-top: 0.8mm; opacity: .85; }
.story { display: grid; grid-template-columns: 82mm 1fr; gap: 7mm; align-items: start; }
.opis { margin-top: 4mm; }
.blok-caption { break-inside: avoid; page-break-inside: avoid; }
.caption { white-space: pre-wrap; background: var(--mist); border: 0.2mm solid var(--aqua); border-radius: 2.5mm;
           padding: 3mm 4mm; font-size: 8.8pt; line-height: 1.42; }
.tags { color: var(--teal); font-weight: 600; margin-top: 1.5mm; font-size: 8.8pt; }
.alty { margin: 2mm 0 0; padding-left: 4.5mm; font-size: 7pt; line-height: 1.35; color: var(--ocean); opacity: .85; columns: 2; column-gap: 8mm; }
.siatka.dluga { grid-template-columns: repeat(4, 1fr); width: 100%; }
.alty li { margin-bottom: 0.6mm; break-inside: avoid; }
.przekladka { display: flex; flex-direction: column; justify-content: center; min-height: 262mm; }
.przekladka .litera { font-size: 120pt; font-weight: 700; line-height: 1; color: var(--teal); letter-spacing: -4px; }
.przekladka h1 { margin: 4mm 0 4mm; }
.przekladka.c { background: #0e1d1f; color: #f6fffd; padding: 0 16mm; border-radius: 6mm; min-height: 268mm; }
.przekladka.c .litera { color: #ffc88a; }
.przekladka.c .lead { color: #bbe4de; }
.przekladka.d { background: #0e1d1f; color: #f6fffd; padding: 0 16mm; border-radius: 6mm; min-height: 268mm; }
.przekladka.d .litera { color: #339499; }
.przekladka.d .lead { color: #dbf0ed; }
.przekladka.e { background: #ff9f8a; color: #0e1d1f; padding: 0 16mm; border-radius: 6mm; min-height: 268mm; }
.przekladka.e .litera { color: #0e1d1f; letter-spacing: -8px; }
.przekladka.e .lead { color: #0e1d1f; }
.storyboard { display: grid; grid-template-columns: repeat(4, 1fr); gap: 3mm 4mm; width: 100%; }
.storyboard.k5 { grid-template-columns: repeat(5, 1fr); }
/* strona tytulowa przy pieciu wariantach: ciasniej, zeby zmiescila sie na jednej stronie */
.tytul h1 { margin: 2mm 0 1.5mm; font-size: 20pt; }
.tytul .lead { font-size: 9.5pt; margin: 0 0 3mm; }
.tytul .wariant { padding: 1.8mm 5mm; margin: 0 0 1.8mm; }
.tytul .wariant h2 { font-size: 11.5pt; margin: 0 0 0.6mm; }
.tytul .wariant p { margin: 0 0 1.4mm; font-size: 8pt; line-height: 1.28; }
.tytul .mini { width: 12.5mm; }
.tytul .mini.pion { width: 9.5mm; }
.tytul .miniatury { gap: 3mm; }
.przekladka.d .meta, .przekladka.c .meta { color: #bbe4de; opacity: 1; }
.tytul .mini span { font-size: 6.5pt; }
.storyboard figcaption b { color: var(--teal); }
.wideo { background: var(--mist); border: 0.2mm solid var(--aqua); border-radius: 2.5mm; padding: 2.5mm 4mm;
         font-size: 8.5pt; margin: 0 0 3mm; }
.wideo code { font-size: 8pt; }
"""


def _logo():
    svg = io.open(os.path.join(sc.TEMPLATES, 'assets', 'logo.svg'), encoding='utf-8').read()
    svg = re.sub(r'\swidth="[^"]*"', '', svg, count=1)
    return re.sub(r'\sheight="[^"]*"', '', svg, count=1)


def src(m):
    return os.path.relpath(sc.abs_repo(m), sc.PREVIEW).replace(os.sep, '/')


def _manifest(d):
    import json
    try:
        return json.load(io.open(os.path.join(sc.MEDIA, d.get('id') or '', '_render.json'), encoding='utf-8-sig'))
    except (OSError, ValueError):
        return {}


def sceny_rolki(d):
    """[(nr, sciezka_repo_rel, start_s, koniec_s, szablon, przejscie, ruch)] scen wyrenderowanej rolki."""
    man = _manifest(d)
    plan = {nr: (sz, prz, ruch) for nr, sz, _t, prz, ruch in sc.reel_plan(d)[0]}
    out = []
    for s_ in man.get('sceny') or []:
        sz, prz, ruch = plan.get(s_.get('scena'), ('?', None, None))
        out.append((s_.get('scena'), s_.get('plik'), s_.get('start_s'), s_.get('koniec_s'), sz, prz, ruch))
    return out


def strona_rolki(d, nr, razem):
    """Rolka: storyboard (klatki scen z czasami), okladka, sciezka MP4, parametry wideo, caption."""
    w = wariant(d)
    man = _manifest(d)
    sceny = sceny_rolki(d)
    wid = man.get('wideo') or {}
    out = ['<section class="strona post">']
    out.append('<div class="naglowek"><div><h2>%s</h2><div>'
               '<span class="pill">Rolka</span><span class="pill b">Wariant %s</span>'
               '<span class="meta">%d scen &middot; %s %s ET &middot; status: %s</span></div></div>'
               '<div class="meta">%d/%d</div></div>'
               % (e(d.get('temat') or d.get('id')), w, len(sceny), e(d.get('planowana_data')),
                  e(d.get('planowana_godzina_et')), e(d.get('status')), nr, razem))
    mp4 = (d.get('media') or [''])[0]
    out.append('<div class="wideo"><b>Wideo:</b> <code>%s</code><br>%s s &middot; %sx%s &middot; %s fps &middot; '
               '%s/%s &middot; audio %s %s Hz (%s) &middot; %.1f MB &middot; okładka: scena %s</div>'
               % (e(mp4), e(wid.get('czas')), e(wid.get('w')), e(wid.get('h')), e(wid.get('fps')),
                  e(wid.get('vcodec')), e(wid.get('pix_fmt')), e(wid.get('acodec')), e(wid.get('audio_hz')),
                  e(d.get('audio') or 'cicha ścieżka'), (wid.get('bajty') or 0) / 1048576.0, e(d.get('cover_slajd') or 1)))
    figury = []
    for nr_s, plik, a, b, sz, prz, ruch in sceny:
        opis = '%s-%s s &middot; %s' % (e(a), e(b), e(sz))
        if ruch:
            opis += ' &middot; %s' % e(ruch)
        if prz and nr_s != len(sceny):
            opis += ' &middot; &rarr; %s' % e(prz)
        figury.append('<figure><img src="%s" alt=""><figcaption><b>%d.</b> %s</figcaption></figure>'
                      % (e(src(plik)), nr_s, opis))
    n = len(figury)
    out.append('<div class="storyboard%s">%s</div>' % (' k5' if n == 5 or n > 8 else '', ''.join(figury)))
    tagi = ' '.join(d.get('hashtagi') or [])
    out.append('<div class="opis"><div class="blok-caption"><h3>Caption</h3><div class="caption">%s</div>%s</div></div>'
               % (e(d.get('caption') or ''), '<div class="tags">%s</div>' % e(tagi) if tagi else ''))
    out.append('</section>')
    return '\n'.join(out)


def strona_posta(d, nr, razem):
    if d.get('typ') == 'reel':
        return strona_rolki(d, nr, razem)
    typ = d.get('typ') or '?'
    media = d.get('media') or []
    slajdy = d.get('slajdy') or []
    alty = d.get('alt_text') or []
    w = wariant(d)
    out = ['<section class="strona post">']
    out.append('<div class="naglowek"><div><h2>%s</h2><div>'
               '<span class="pill">%s</span><span class="pill b">Wariant %s</span>'
               '<span class="meta">%d %s &middot; %s %s ET &middot; status: %s</span></div></div>'
               '<div class="meta">%d/%d</div></div>'
               % (e(d.get('temat') or d.get('id')), e(TYPY_PL.get(typ, typ)), w, len(slajdy),
                  'slajd' if len(slajdy) == 1 else 'slajdów', e(d.get('planowana_data')),
                  e(d.get('planowana_godzina_et')), e(d.get('status')), nr, razem))
    figury = []
    for i, m in enumerate(media):
        sz = (slajdy[i] or {}).get('szablon', '?') if i < len(slajdy) else '?'
        figury.append('<figure><img src="%s" alt="%s"><figcaption>%d/%d &middot; %s</figcaption></figure>'
                      % (e(src(m)), e(alty[i] if i < len(alty) else ''), i + 1, len(media), e(sz)))
    tagi = ' '.join(d.get('hashtagi') or [])
    cap = d.get('caption') or ''
    opis = ['<div class="opis">']
    if typ == 'story':
        opis.append('<h3>Caption</h3><div class="caption"><i>Story: Instagram nie publikuje caption, '
                    'cała treść jest na grafice.</i></div>')
    else:
        # caption z hashtagami to jeden blok, ktory nie dzieli sie miedzy strony
        opis.append('<div class="blok-caption"><h3>Caption</h3><div class="caption">%s</div>%s</div>'
                    % (e(cap), '<div class="tags">%s</div>' % e(tagi) if tagi else ''))
    if alty:
        opis.append('<h3 style="margin-top:3mm">Alt text</h3><ol class="alty">%s</ol>'
                    % ''.join('<li>%s</li>' % e(a) for a in alty))
    opis.append('</div>')
    if typ == 'story':
        out.append('<div class="story">%s%s</div>' % (''.join(figury), ''.join(opis)))
    else:
        # karuzela 7+ slajdow: 4 kolumny (2 rzedy zamiast 3), zeby caption i alty zmiescily sie na tej samej stronie
        klasa = ' single' if typ == 'single' else (' dluga' if len(figury) > 6 else '')
        out.append('<div class="siatka%s">%s</div>' % (klasa, ''.join(figury)))
        out.extend(opis)
    out.append('</section>')
    return '\n'.join(out)


def przekladka(kod, grupa):
    tytul, opis = [(t, o) for k, t, o in WARIANTY if k == kod][0]
    return ('<section class="strona przekladka%s"><div class="litera">%s</div><h1>%s</h1>'
            '<p class="lead">%s</p><p class="meta">%d %s</p></section>'
            % ({'C': ' c', 'D': ' d', 'E': ' e'}.get(kod, ''), kod, e(tytul.split(': ', 1)[-1]), e(opis), len(grupa),
               'post' if len(grupa) == 1 else 'posty'))


def strona_tytulowa(posty, nazwa):
    dzis = datetime.date.today().strftime('%d.%m.%Y')
    out = ['<section class="strona tytul">',
           '<div class="znak">%s<span>MindSync</span></div>' % _logo(),
           '<h1>%s</h1>' % ('Instagram: przykłady szablonów' if all('przyklad' in (d.get('id') or '') for d in posty)
                            else 'Instagram: partia postów'),
           '<p class="lead">Podgląd postów dla nowego konta MindSync (EN, rynek USA). Każdy post jest '
           'na osobnej stronie: slajdy w kolejności publikacji (1080x1350, story 1080x1920), pod nimi '
           'caption z hashtagami i teksty alternatywne. Grafiki generuje automat z szablonów HTML, '
           'więc uwagi do układu, kolorów i typografii dotyczą od razu wszystkich przyszłych postów.</p>']
    for kod, tytul, opis in WARIANTY:
        grupa = [d for d in posty if wariant(d) == kod]
        if not grupa:
            continue
        out.append('<div class="wariant"><h2>%s</h2><p>%s</p><div class="miniatury">' % (e(tytul), e(opis)))
        for d in grupa:
            m = (d.get('media') or [None])[0]
            if d.get('typ') == 'reel':
                m = (d.get('media') or [None, None])[1]  # okladka zamiast MP4
            if m:
                out.append('<div class="mini%s"><img src="%s" alt=""><span>%s, %d sl.</span></div>'
                           % (' pion' if d.get('typ') in ('story', 'reel') else '', e(src(m)),
                              e(TYPY_PL.get(d.get('typ'), d.get('typ'))), len(d.get('slajdy') or [])))
        out.append('</div></div>')
    statusy = {}
    for d in posty:
        statusy[d.get('status')] = statusy.get(d.get('status'), 0) + 1
    opis_st = ', '.join('%s: %d' % (k, v) for k, v in sorted(statusy.items(), key=lambda x: str(x[0])))
    terminy = sorted('%s %s ET' % (d.get('planowana_data'), d.get('planowana_godzina_et')) for d in posty
                     if 'przyklad' not in (d.get('id') or ''))
    out.append('<p class="meta">Wygenerowano %s &middot; plik %s.pdf &middot; statusy postów: %s%s.</p>'
               % (dzis, e(nazwa), e(opis_st), (' &middot; terminy: ' + e(', '.join(terminy))) if terminy else ''))
    out.append('</section>')
    return '\n'.join(out)


def main():
    ap = argparse.ArgumentParser(description='PDF z postami IG MindSync dla grafika (A4)')
    ap.add_argument('--id', action='append', default=[], help='id posta albo nazwa pliku (mozna wiele razy)')
    ap.add_argument('--all-przyklady', action='store_true', help='wszystkie social/queue/_przyklad-*.json')
    ap.add_argument('--status', choices=sc.STATUSY, help='posty o danym statusie (bez plikow _)')
    ap.add_argument('--nazwa', help='nazwa pliku w social/preview/ (bez .pdf)')
    ap.add_argument('--zostaw-html', action='store_true', help='nie usuwaj posredniego HTML')
    a = ap.parse_args()

    gate = _gate()
    sciezki = gate.wybierz(a.id, False, a.status)
    if a.all_przyklady:
        import glob
        for p in sorted(glob.glob(os.path.join(sc.QUEUE, '_przyklad-*.json'))):
            if p not in sciezki:
                sciezki.append(p)
    if not sciezki:
        ap.error('podaj --id, --status albo --all-przyklady')

    posty = []
    for p in sciezki:
        d, _ = sc.wczytaj(p)
        media = d.get('media') or []
        brak = [m for m in media if not os.path.isfile(sc.abs_repo(m))]
        if d.get('typ') == 'reel':
            sceny = sceny_rolki(d)
            brak += [s_[1] for s_ in sceny if not os.path.isfile(sc.abs_repo(s_[1] or ''))]
            if len(media) != 2 or brak or len(sceny) != len(d.get('slajdy') or []):
                sys.exit('X  %s: brak aktualnej rolki, uruchom najpierw reel-render.py' % os.path.basename(p))
        elif not media or brak or len(media) != len(d.get('slajdy') or []):
            sys.exit('X  %s: brak aktualnych mediow, uruchom najpierw render.py' % os.path.basename(p))
        posty.append(d)
    # kolejnosc: wariant A, B, C, D, E; w wariancie karuzela, single, story, rolka
    kol_typu = {'carousel': 0, 'single': 1, 'story': 2, 'reel': 3}
    posty.sort(key=lambda d: (wariant(d), kol_typu.get(d.get('typ'), 9), str(d.get('planowana_data'))))

    nazwa = a.nazwa or (DOMYSLNA_NAZWA if a.all_przyklady else datetime.date.today().isoformat())
    nazwa = re.sub(r'[^A-Za-z0-9_.-]+', '-', nazwa).strip('-') or 'eksport'
    os.makedirs(sc.PREVIEW, exist_ok=True)
    html_path = os.path.join(sc.PREVIEW, '_pdf-%s.html' % nazwa)
    pdf_path = os.path.join(sc.PREVIEW, nazwa + '.pdf')

    doc = ['<!doctype html><html lang="pl"><head><meta charset="utf-8">',
           '<title>%s</title><style>%s</style></head><body>' % (e(nazwa), CSS),
           strona_tytulowa(posty, nazwa)]
    biezacy = None
    for i, d in enumerate(posty, 1):
        w = wariant(d)
        if w != biezacy:
            biezacy = w
            doc.append(przekladka(w, [x for x in posty if wariant(x) == w]))
        doc.append(strona_posta(d, i, len(posty)))
    doc.append('</body></html>')
    io.open(html_path, 'w', encoding='utf-8').write('\n'.join(doc))

    from playwright.sync_api import sync_playwright
    try:
        with sync_playwright() as pw:
            browser = pw.chromium.launch(args=['--allow-file-access-from-files'])
            page = browser.new_page()
            page.goto(pathlib.Path(html_path).resolve().as_uri(), wait_until='load')
            page.evaluate('document.fonts.ready.then(() => true)')
            stan = page.evaluate("""() => {
                const imgs = Array.from(document.images);
                return {razem: imgs.length,
                        brak: imgs.filter(i => !(i.complete && i.naturalWidth > 0)).map(i => i.getAttribute('src'))};
            }""")
            if stan['brak']:
                browser.close()
                sys.exit('X  niezaladowane obrazy (%d/%d): %s' % (len(stan['brak']), stan['razem'], ', '.join(stan['brak'])))
            page.pdf(path=pdf_path, format='A4', print_background=True, prefer_css_page_size=True)
            browser.close()
    finally:
        if not a.zostaw_html:
            try:
                os.remove(html_path)
            except OSError:
                pass

    strony = None
    try:
        with open(pdf_path, 'rb') as f:
            strony = len(re.findall(rb'/Type\s*/Page[^s]', f.read()))
    except OSError:
        pass
    print('PDF: %s  (postow %d, obrazow %d, niezaladowanych 0, stron %s)'
          % (sc.rel(pdf_path), len(posty), stan['razem'], strony if strony is not None else '?'))


if __name__ == '__main__':
    main()
