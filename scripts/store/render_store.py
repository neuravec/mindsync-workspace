#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""MindSync store screenshots: store/slides.json -> PNG for the App Store and Google Play.

For every slide and every store in its `targets`, fills store/templates/<type>.html (screen or
testimonial), renders it with Playwright (Chromium, offline: Figtree from store/templates/assets/,
shots loaded as file://), lets fit.js size the text, takes a PNG screenshot and saves it as RGB
without alpha (Pillow).

Outputs (folders are created when missing):
    store/out/appstore/NN-<id>.png    1290x2796, iPhone frame, iOS render
    store/out/play/NN-<id>.png        1080x1920, neutral Android frame, Android render; without an
                                      Android render the iOS one is used with its status area and
                                      home indicator cut off
    store/out/_contact_appstore.png   all App Store slides side by side (review sheet)
    store/out/_contact_play.png       all Play slides side by side
    store/out/_render.json            per slide: shot used, placeholder flag, text scale, warnings

NN is the position of the slide among the slides of that store, counted on the full spec, so the
file names do not change when you render a subset with --only.

Shots: `shot_ios` / `shot_android` take a path or a list of paths (repo-relative). The first file
that exists wins; anything after the first entry is a placeholder and is reported as such. So the
spec can name the fresh render first (store/renders/ios/store_<name>.png) and an older render as a
fallback, and it switches by itself once the fresh file lands.

Status area (iOS clock row, Android status bar):
    fill  the shot already has its top area (real status bar or an empty safe area): pasted from y=0
    band  the shot starts with app content at y=0 (Flutter harness shots in social/images/app-shots/):
          an empty band in the shot's top colour goes above it, so the island/camera never covers UI
    auto  (default) band for social/images/app-shots/, fill for everything else
Override per slide with "ios_mode" / "android_mode". Optional "crop_top" (source px) skips the top
of a tall shot. The renderer never draws a clock, icons or any other UI on or over a shot.

Background decor (screen slides, opt-in): "decor": "bird_wave" turns it on for every store of the
slide, "decor": {"play": "bird_wave"} only for the stores named. bird_wave = a line bird beside the
headline and a line-chart wave behind the phone (store/templates/assets/decor-*.svg, placed by
store.css). The layer is painted under the text and the phone; fit.js warns when the bird comes near
the headline, the subtitle or the phone (the warning lands in _render.json).

Usage:
    python scripts/store/render_store.py
    python scripts/store/render_store.py --only main,reflect
    python scripts/store/render_store.py --format play
    python scripts/store/render_store.py --strict        # exit 1 if any slide uses a placeholder shot
    python scripts/store/render_store.py --spec store/slides.json --keep-html

Needs: pip install playwright pillow && python -m playwright install chromium
Writes only inside store/ (the first run copies Figtree into store/templates/assets/).
Exit code 1 when a slide fails, or with --strict when a placeholder was used.
"""
import argparse
import datetime
import html
import io
import json
import pathlib
import re
import shutil
import sys

REPO = pathlib.Path(__file__).resolve().parents[2]
STORE = REPO / 'store'
TEMPLATES = STORE / 'templates'
ASSETS = TEMPLATES / 'assets'
OUT = STORE / 'out'
SPEC_DEFAULT = STORE / 'slides.json'

FONT_FILES = ('Figtree-Regular.ttf', 'Figtree-Medium.ttf', 'Figtree-SemiBold.ttf', 'Figtree-Bold.ttf')
FONT_SOURCES = (REPO / 'social' / 'templates' / 'assets',
                REPO / 'mindsync-frontend' / 'mindsync_app' / 'assets' / 'fonts')

FORMATS = {
    'appstore': {'size': (1290, 2796), 'frame': 'ios', 'contact_h': 900},
    'play': {'size': (1080, 1920), 'frame': 'android', 'contact_h': 900},
}
TYPES = ('screen', 'testimonial')
MODES = (None, 'auto', 'band', 'fill')
# background decor sets: name -> (css class, asset file in store/templates/assets/), in paint order
DECORS = {
    'bird_wave': (('wave', 'decor-wave.svg'), ('bird', 'decor-bird.svg')),
}

# Fractions of the SCREEN width (the shot is scaled to the screen width).
IOS_BAND = 0.13          # empty band above a harness shot in the iPhone frame (island sits in it)
ANDROID_BAND = 0.08      # empty band in the Android frame (punch-hole camera sits in it)
IOS_STATUS_CROP = 0.12   # iOS status area cut off when an iOS shot goes into the Android frame
IOS_HOME_CUT = 0.06      # iOS home indicator cut off the bottom in the same case
BAND_PREFIXES = ('social/images/app-shots/',)
PLAY_TEXT_LIMIT = 0.20   # Google Play: text should cover at most ~20% of the image

DASHES = (chr(0x2014), chr(0x2013))   # banned in copy; written as code points on purpose
ID_RE = re.compile(r'^[a-z0-9][a-z0-9_-]*$')

STAR_SVG = ('<svg viewBox="0 0 100 100" aria-hidden="true"><polygon fill="currentColor" '
            'stroke="currentColor" stroke-width="4" stroke-linejoin="round" points="50,4.77 62.93,36.97 '
            '97.55,39.32 70.92,61.57 79.39,95.22 50,76.77 20.61,95.22 29.08,61.57 2.45,39.32 37.07,36.97"/>'
            '</svg>')

JS_BROKEN_IMAGES = ("() => Array.from(document.images)"
                    ".filter(i => i.getAttribute('src') && !(i.complete && i.naturalWidth > 0)).length")


class SlideError(Exception):
    """The slide cannot be rendered (bad spec, missing shot, template problem)."""


def _dependencies():
    missing = []
    try:
        import playwright  # noqa: F401
    except ImportError:
        missing.append('playwright')
    try:
        import PIL  # noqa: F401
    except ImportError:
        missing.append('pillow')
    if missing:
        sys.exit('Missing packages: %s. Install: pip install playwright pillow && '
                 'python -m playwright install chromium' % ', '.join(missing))


def ensure_fonts():
    """Copies Figtree into store/templates/assets/ when missing. Returns the names still missing."""
    ASSETS.mkdir(parents=True, exist_ok=True)
    missing = []
    for name in FONT_FILES:
        dst = ASSETS / name
        if dst.is_file():
            continue
        for src_dir in FONT_SOURCES:
            src = src_dir / name
            if src.is_file():
                shutil.copyfile(src, dst)
                break
        else:
            missing.append(name)
    return missing


# ---- text ------------------------------------------------------------------------------------

def typography(s):
    """Typographic apostrophes and quotes, only in the image (the JSON stays as written)."""
    rsq, lsq, ldq, rdq = chr(0x2019), chr(0x2018), chr(0x201C), chr(0x201D)
    s = re.sub(r"(?<=\w)'(?=\w)", rsq, s)
    s = re.sub(r"(^|[\s(])'", lambda m: m.group(1) + lsq, s)
    s = s.replace("'", rsq)
    s = re.sub(r'(^|[\s(])"', lambda m: m.group(1) + ldq, s)
    s = s.replace('"', rdq)
    return s


def markup_lines(text):
    """'**bold**' and line breaks -> list of HTML lines. Bold may continue across a line break."""
    text = (text or '').replace('\r\n', '\n')
    parts = typography(text).split('**')
    if len(parts) % 2 == 0:
        raise SlideError('unbalanced ** in: %s' % text)
    lines = [[]]
    for i, part in enumerate(parts):
        for j, seg in enumerate(part.split('\n')):
            if j:
                lines.append([])
            if seg:
                h = html.escape(seg, quote=False)
                lines[-1].append('<b>%s</b>' % h if i % 2 else h)
    return [''.join(x) for x in lines]


def forced_line(h):
    return '<span class="ln"><span class="tx">%s</span></span>' % h


def headline_html(lines):
    out = []
    for line in lines:
        hl = markup_lines(line.strip())
        if len(hl) != 1:
            raise SlideError('a headline line must not contain a line break: %s' % line)
        out.append(forced_line(hl[0]))
    return ''.join(out)


def subtitle_html(text):
    """(html, css class): forced lines when the text has line breaks, balanced wrap otherwise."""
    text = (text or '').strip()
    if not text:
        return '', 'empty'
    if '\n' in text:
        return ''.join(forced_line(h) for h in markup_lines(text) if h.strip()), 'lines'
    return markup_lines(text)[0], 'wrap'


def quote_html(quote, attribution):
    """Review text: one forced line per line of the spec, a blank line starts a new paragraph."""
    paras, cur = [], []
    for h in markup_lines(quote.strip()):
        if h.strip():
            cur.append(h)
        elif cur:
            paras.append(cur)
            cur = []
    if cur:
        paras.append(cur)
    body = ''.join('<p class="para">%s</p>' % ''.join(forced_line(h) for h in p) for p in paras)
    attribution = (attribution or '').strip()
    if attribution:
        att = markup_lines(attribution)
        if len(att) != 1:
            raise SlideError('attribution must be one line')
        body += '<p class="attrib">%s</p>' % forced_line(att[0])
    return body


# ---- spec ------------------------------------------------------------------------------------

def candidates(value):
    if not value:
        return []
    if isinstance(value, str):
        return [value]
    if isinstance(value, list) and all(isinstance(x, str) and x.strip() for x in value):
        return value
    raise SlideError('shot fields take a path or a list of paths')


def decor_error(value):
    """None when `decor` is absent or valid: a set name, or {store: set name} for some stores only."""
    if value is None:
        return None
    names = ', '.join(sorted(DECORS))
    if isinstance(value, str):
        return None if value in DECORS else 'decor must be one of %s' % names
    if isinstance(value, dict) and value:
        for fmt, name in value.items():
            if fmt not in FORMATS:
                return 'decor keys must be %s' % ', '.join(FORMATS)
            if name is not None and name not in DECORS:
                return 'decor must be one of %s' % names
        return None
    return 'decor takes a set name (%s) or {"play": ..., "appstore": ...}' % names


def decor_for(slide, fmt):
    """The decor set for this slide in this store, or None."""
    value = slide.get('decor')
    if isinstance(value, dict):
        return value.get(fmt)
    return value or None


def decor_html(name):
    """Background layer for the {{decor}} slot of screen.html ('' when the slide has none)."""
    if not name:
        return ''
    imgs = []
    for cls, fname in DECORS[name]:
        if not (ASSETS / fname).is_file():
            raise SlideError('decor %s: missing store/templates/assets/%s' % (name, fname))
        imgs.append('<img class="%s" src="assets/%s" alt="">' % (cls, fname))
    return '<div class="decor-layer decor-%s" id="decor" aria-hidden="true">%s</div>' % (name, ''.join(imgs))


def load_spec(path):
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as e:
        sys.exit('X  cannot read %s: %s' % (path, e))
    if isinstance(data, dict):
        data = data.get('slides')
    if not isinstance(data, list) or not data:
        sys.exit('X  %s: expected a non-empty JSON array of slides' % path)
    errors, seen = [], set()
    for i, s in enumerate(data, 1):
        if not isinstance(s, dict):
            errors.append('slide %d: not an object' % i)
            continue
        sid = str(s.get('id') or '')
        where = 'slide %d (%s)' % (i, sid or '?')
        if not ID_RE.match(sid):
            errors.append('%s: id must match [a-z0-9][a-z0-9_-]*' % where)
        if sid in seen:
            errors.append('%s: duplicate id' % where)
        seen.add(sid)
        s['type'] = s.get('type') or 'screen'
        if s['type'] not in TYPES:
            errors.append('%s: type must be one of %s' % (where, ', '.join(TYPES)))
            continue
        s['targets'] = s.get('targets') or list(FORMATS)
        if not isinstance(s['targets'], list) or any(t not in FORMATS for t in s['targets']):
            errors.append('%s: targets must be a list of %s' % (where, ', '.join(FORMATS)))
        for k in ('headline_lines', 'subtitle', 'quote', 'attribution'):
            v = s.get(k)
            for x in (v if isinstance(v, list) else [v]):
                if isinstance(x, str) and any(d in x for d in DASHES):
                    errors.append('%s: `%s` contains U+2014/U+2013, rewrite the sentence' % (where, k))
        try:
            if s['type'] == 'screen':
                hl = s.get('headline_lines')
                if (not isinstance(hl, list) or not 1 <= len(hl) <= 3
                        or not all(isinstance(x, str) and x.strip() for x in hl)):
                    errors.append('%s: headline_lines must be a list of 1-3 non-empty strings' % where)
                else:
                    headline_html(hl)
                subtitle_html(s.get('subtitle'))
                if not candidates(s.get('shot_ios')):
                    errors.append('%s: shot_ios is required' % where)
                candidates(s.get('shot_android'))
                for k in ('ios_mode', 'android_mode'):
                    if s.get(k) not in MODES:
                        errors.append('%s: %s must be auto, band or fill' % (where, k))
                ct = s.get('crop_top', 0)
                if not isinstance(ct, (int, float)) or ct < 0:
                    errors.append('%s: crop_top must be a number of source px >= 0' % where)
                err = decor_error(s.get('decor'))
                if err:
                    errors.append('%s: %s' % (where, err))
            else:
                if s.get('decor') is not None:
                    errors.append('%s: decor is only for screen slides' % where)
                if not str(s.get('quote') or '').strip():
                    errors.append('%s: testimonial needs `quote`' % where)
                else:
                    quote_html(s['quote'], s.get('attribution'))
                stars = s.get('stars', 5)
                if not isinstance(stars, int) or isinstance(stars, bool) or not 0 <= stars <= 5:
                    errors.append('%s: stars must be an integer 0-5' % where)
        except SlideError as e:
            errors.append('%s: %s' % (where, e))
    if errors:
        print('X  %s is not valid:' % path)
        for e in errors:
            print('   - %s' % e)
        sys.exit(1)
    return data


def numbering(slides):
    """{(format, id): NN} counted on the full spec, per store."""
    nr = {}
    for fmt in FORMATS:
        n = 0
        for s in slides:
            if fmt in s['targets']:
                n += 1
                nr[(fmt, s['id'])] = n
    return nr


# ---- shots -----------------------------------------------------------------------------------

def resolve_shot(value):
    """First existing candidate -> (repo-relative path, placeholder?). (None, False) when none exists."""
    for i, rel in enumerate(candidates(value)):
        rel = rel.strip().replace('\\', '/')
        if (REPO / rel).is_file():
            return rel, i > 0
    return None, False


def mode_for(override, rel):
    if override in ('band', 'fill'):
        return override
    return 'band' if rel.startswith(BAND_PREFIXES) else 'fill'


def sample_shot(path_abs, crop_frac, extra_px, bottom_cut=0.0):
    """Source size, total top crop and visible height (fractions of the source width) and the colours
    used around the shot: top = rows right under the crop (band colour), bottom = last visible rows
    (fill below a shot that ends before the screen does)."""
    from PIL import Image
    with Image.open(path_abs) as im:
        rgb = im.convert('RGB')
        w, h = rgb.size
        total = crop_frac + float(extra_px) / w
        y0 = int(round(total * w))
        y1 = h - int(round(bottom_cut * w))
        if y1 - y0 < 24:
            raise SlideError('crop leaves nothing of %s (%dx%d)' % (path_abs.name, w, h))
        top = rgb.crop((0, y0, w, y0 + 12)).resize((1, 1), Image.BOX).getpixel((0, 0))
        bottom = rgb.crop((0, y1 - 12, w, y1)).resize((1, 1), Image.BOX).getpixel((0, 0))
    vis = (y1 - y0) / float(w)
    return (w, h), total, vis, top[:3], bottom[:3]


def screen_setup(fmt, slide):
    """Which shot goes into the phone for this store and how (band, crop, colours)."""
    if fmt == 'appstore':
        rel, placeholder = resolve_shot(slide.get('shot_ios'))
        if not rel:
            raise SlideError('no shot_ios file exists (%s)' % ', '.join(candidates(slide.get('shot_ios'))))
        mode = mode_for(slide.get('ios_mode'), rel)
        band, crop, source = (IOS_BAND if mode == 'band' else 0.0), 0.0, 'ios'
    else:
        rel, placeholder = resolve_shot(slide.get('shot_android'))
        if rel:
            mode = mode_for(slide.get('android_mode'), rel)
            band, crop, source = (ANDROID_BAND if mode == 'band' else 0.0), 0.0, 'android'
        else:
            rel, placeholder = resolve_shot(slide.get('shot_ios'))
            if not rel:
                raise SlideError('no shot_android or shot_ios file exists')
            mode = mode_for(slide.get('ios_mode'), rel)
            # harness shot: nothing to cut, only the band; iOS shot with its own top and bottom: cut
            # the iOS status area and the home indicator so no iPhone chrome shows, add the Android band
            band, crop, source = ANDROID_BAND, (0.0 if mode == 'band' else IOS_STATUS_CROP), 'ios-in-android-frame'
    bottom_cut = IOS_HOME_CUT if (source == 'ios-in-android-frame' and mode == 'fill') else 0.0
    path_abs = REPO / rel
    size, total_crop, vis, top, bottom = sample_shot(path_abs, crop, slide.get('crop_top', 0) or 0, bottom_cut)
    style = ('--band: %.4f; --crop: %.4f; --vis: %.4f; --top-bg: rgb(%d, %d, %d); --bottom-bg: rgb(%d, %d, %d);'
             % ((band, total_crop, vis) + tuple(top) + tuple(bottom)))
    return {'rel': rel, 'placeholder': placeholder, 'mode': mode, 'source': source,
            'url': path_abs.resolve().as_uri(), 'style': style, 'size': '%dx%d' % size}


# ---- render ----------------------------------------------------------------------------------

def fill_template(name, values):
    tpl = (TEMPLATES / name).read_text(encoding='utf-8')

    def sub(m):
        k = m.group(1)
        if k not in values:
            raise SlideError('template %s: no value for {{%s}}' % (name, k))
        return values[k]

    return re.sub(r'\{\{(\w+)\}\}', sub, tpl)


def build_html(fmt, slide):
    """(html, record fields) for one slide in one store."""
    rec = {}
    if slide['type'] == 'screen':
        sub, sub_class = subtitle_html(slide.get('subtitle'))
        shot = screen_setup(fmt, slide)
        decor = decor_for(slide, fmt)
        doc = fill_template('screen.html', {
            'fmt': fmt,
            'decor': decor_html(decor),
            'frame': FORMATS[fmt]['frame'],
            'headline': headline_html(slide['headline_lines']),
            'subtitle': sub,
            'sub_class': sub_class,
            'shot_url': html.escape(shot['url'], quote=True),
            'screen_style': html.escape(shot['style'], quote=True),
        })
        rec.update({'shot': shot['rel'], 'shot_size': shot['size'], 'shot_source': shot['source'],
                    'status_mode': shot['mode'], 'placeholder': shot['placeholder']})
        if decor:
            rec['decor'] = decor
    else:
        doc = fill_template('testimonial.html', {
            'fmt': fmt,
            'quote': quote_html(slide['quote'], slide.get('attribution')),
            'stars': STAR_SVG * int(slide.get('stars', 5)),
        })
    return doc, rec


def save_png(png_bytes, out_path, size):
    """RGB PNG without alpha (App Store rejects alpha), 72 dpi."""
    from PIL import Image
    im = Image.open(io.BytesIO(png_bytes))
    im.load()
    if im.mode != 'RGB':
        bg = Image.new('RGB', im.size, (255, 255, 255))
        if im.mode in ('RGBA', 'LA'):
            bg.paste(im, mask=im.split()[-1])
        else:
            bg.paste(im.convert('RGB'))
        im = bg
    if im.size != size:
        raise SlideError('screenshot is %dx%d, expected %dx%d' % (im.size + size))
    out_path.parent.mkdir(parents=True, exist_ok=True)
    im.save(out_path, 'PNG', dpi=(72, 72), compress_level=6)


def render_slide(page, fmt, slide, nr, keep_html=False):
    """Renders one slide for one store. Returns the record for _render.json (raises SlideError)."""
    w, h = FORMATS[fmt]['size']
    out_path = OUT / fmt / ('%02d-%s.png' % (nr, slide['id']))
    doc, rec = build_html(fmt, slide)
    rec.update({'format': fmt, 'id': slide['id'], 'nr': nr, 'file': out_path.relative_to(REPO).as_posix()})
    warnings = []
    if rec.get('placeholder'):
        warnings.append('PLACEHOLDER shot %s (the fresh render is not there yet)' % rec['shot'])
    tmp = TEMPLATES / ('_tmp-%s-%s.html' % (fmt, slide['id']))
    tmp.write_text(doc, encoding='utf-8')
    try:
        page.set_viewport_size({'width': w, 'height': h})
        page.goto(tmp.resolve().as_uri(), wait_until='load')
        page.wait_for_function('window.__ready !== undefined', timeout=20000)
        ready = page.evaluate('window.__ready') or {}
        if page.evaluate(JS_BROKEN_IMAGES):
            raise SlideError('the shot did not load: %s' % rec.get('shot'))
        png = page.screenshot(type='png', clip={'x': 0, 'y': 0, 'width': w, 'height': h})
    finally:
        if not keep_html:
            tmp.unlink(missing_ok=True)
    if ready.get('error'):
        raise SlideError('fit.js: %s' % ready['error'])
    save_png(png, out_path, (w, h))

    if not ready.get('font_ok', True):
        warnings.append('Figtree did not load, a fallback font was used (check store/templates/assets/)')
    for block in ready.get('overflow') or []:
        warnings.append('%s does not fit even at 60%% size, shorten it' % block)
    for clash in ready.get('decor_clash') or []:
        warnings.append('decor %s, move it in store.css (--bird-* / --wave-t)' % clash)
    for block, s in sorted((ready.get('scales') or {}).items()):
        if s < 1:
            warnings.append('%s reduced to %d%% to fit' % (block, round(s * 100)))
    share = float(ready.get('text_share') or 0)
    if fmt == 'play' and share > PLAY_TEXT_LIMIT:
        warnings.append('text covers %.0f%% of the image, Play recommends at most %.0f%%'
                        % (share * 100, PLAY_TEXT_LIMIT * 100))
    rec.update({'scales': ready.get('scales') or {}, 'text_share': round(share, 3), 'warnings': warnings})
    return rec


def contact_sheet(paths, out_path, thumb_h, gap=24, pad=32, bg=(225, 233, 232)):
    """All slides side by side at the same height (for review only, not for upload)."""
    from PIL import Image
    thumbs = []
    for p in paths:
        with Image.open(p) as im:
            im = im.convert('RGB')
            tw = int(round(im.size[0] * thumb_h / float(im.size[1])))
            thumbs.append(im.resize((tw, thumb_h), Image.LANCZOS))
    if not thumbs:
        return False
    width = 2 * pad + sum(t.size[0] for t in thumbs) + gap * (len(thumbs) - 1)
    sheet = Image.new('RGB', (width, thumb_h + 2 * pad), bg)
    x = pad
    for t in thumbs:
        sheet.paste(t, (x, pad))
        x += t.size[0] + gap
    sheet.save(out_path, 'PNG', compress_level=6)
    return True


def main():
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(errors='replace')
    ap = argparse.ArgumentParser(description='Render MindSync App Store and Google Play screenshots')
    ap.add_argument('--spec', default=str(SPEC_DEFAULT), help='slides JSON (default store/slides.json)')
    ap.add_argument('--only', help='comma separated slide ids')
    ap.add_argument('--format', choices=('both', 'appstore', 'play'), default='both')
    ap.add_argument('--strict', action='store_true', help='exit 1 when a placeholder shot was used')
    ap.add_argument('--keep-html', action='store_true', help='keep the filled HTML in store/templates/')
    a = ap.parse_args()

    spec_path = pathlib.Path(a.spec)
    if not spec_path.is_absolute():
        spec_path = (pathlib.Path.cwd() / spec_path) if spec_path.exists() else (REPO / spec_path)
    slides = load_spec(spec_path)
    nr = numbering(slides)
    formats = list(FORMATS) if a.format == 'both' else [a.format]
    only = [x.strip() for x in (a.only or '').split(',') if x.strip()]
    unknown = [x for x in only if x not in {s['id'] for s in slides}]
    if unknown:
        sys.exit('X  unknown slide id(s): %s' % ', '.join(unknown))

    _dependencies()
    missing_fonts = ensure_fonts()
    if missing_fonts:
        print('!  Figtree files not found (%s): text will use a fallback font' % ', '.join(missing_fonts))
    from playwright.sync_api import sync_playwright

    records, failed, placeholders = [], 0, 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--allow-file-access-from-files', '--force-color-profile=srgb'])
        page = browser.new_page(device_scale_factor=1)
        for fmt in formats:
            print('== %s %dx%d' % (fmt, FORMATS[fmt]['size'][0], FORMATS[fmt]['size'][1]))
            for s in slides:
                if fmt not in s['targets'] or (only and s['id'] not in only):
                    continue
                n = nr[(fmt, s['id'])]
                try:
                    rec = render_slide(page, fmt, s, n, a.keep_html)
                except SlideError as e:
                    failed += 1
                    print('[FAIL] %02d-%s: %s' % (n, s['id'], e))
                    records.append({'format': fmt, 'id': s['id'], 'nr': n, 'error': str(e)})
                    continue
                except Exception as e:  # Playwright timeouts and the like: report, go on
                    failed += 1
                    print('[FAIL] %02d-%s: %s: %s' % (n, s['id'], type(e).__name__, e))
                    records.append({'format': fmt, 'id': s['id'], 'nr': n, 'error': str(e)})
                    continue
                placeholders += 1 if rec.get('placeholder') else 0
                print('[ OK ] %s' % rec['file'])
                for w in rec['warnings']:
                    print('       ! %s' % w)
                records.append(rec)
        browser.close()

    # stale files of an earlier, longer set (only on a full render of that store)
    for fmt in formats:
        expected = {'%02d-%s.png' % (nr[(fmt, s['id'])], s['id']) for s in slides if fmt in s['targets']}
        if not only:
            for old in (OUT / fmt).glob('[0-9][0-9]-*.png'):
                if old.name not in expected:
                    old.unlink()
        files = sorted(p for p in (OUT / fmt).glob('[0-9][0-9]-*.png') if p.name in expected)
        sheet = OUT / ('_contact_%s.png' % fmt)
        if contact_sheet(files, sheet, FORMATS[fmt]['contact_h']):
            print('Contact sheet: %s (%d slides)' % (sheet.relative_to(REPO).as_posix(), len(files)))

    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {
        'rendered': datetime.datetime.now().isoformat(timespec='seconds'),
        'spec': spec_path.resolve().relative_to(REPO).as_posix() if REPO in spec_path.resolve().parents else str(spec_path),
        'partial': bool(only) or a.format != 'both',
        'slides': records,
    }
    (OUT / '_render.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print('\nDone: %d rendered, %d failed, %d with a placeholder shot.' % (
        len(records) - failed, failed, placeholders))
    if failed or (a.strict and placeholders):
        sys.exit(1)


if __name__ == '__main__':
    main()
