#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render rolki Instagrama MindSync (typ `reel`): sceny 1080x1920 -> MP4 + okladka.

1. Kazda scena (`slajdy[]`) renderowana jak slajd w render.py (te same szablony 1080x1920:
   feature-story, bold-story, photo-story, story, reel-text; fit.js, bold.js, pomiar kontrastu)
   do social/media/<id>/sceny/NN.jpg.
2. ffmpeg sklada MP4: H.264 (profil high, yuv420p), 30 fps, AAC 48 kHz stereo, faststart.
   - `scena_sek` (domyslnie 3.0 s) = czas sceny, `przejscie` = przejscie Z tej sceny do nastepnej:
     cut (domyslnie), fade albo slide (xfade 0.4 s, nakladka skraca calosc),
   - `ruch`: zoom-in (powolne przyblizenie 1.0 -> 1.08) albo ken-burns (przyblizenie + przesuw),
     zoompan na obrazie 2x wiekszym, wiec bez drgan,
   - `audio`: sciezka do pliku muzyki Z LICENCJA (pole `audio_licencja`) albo null = cicha
     sciezka AAC (czesc pipeline'ow Instagrama zle znosi wideo bez audio). Bez licencji = null.
3. Okladka `cover.jpg` (JPEG 1080x1920 sRGB) ze sceny `cover_slajd` (domyslnie 1).
4. Kontrola ffprobe (te same progi co bramka: H.264, yuv420p, 1080x1920, 23-60 fps, 5-90 s,
   <= 300 MB, AAC), zapis social/media/<id>/_render.json i pola `media` = [reel.mp4, cover.jpg].

Uzycie:
    python scripts/social/reel-render.py _przyklad-reel-feature
    python scripts/social/reel-render.py <id> --klatki C:/tmp/klatki     # + 4 klatki PNG do obejrzenia
    python scripts/social/reel-render.py --all-szkic                      # wszystkie rolki `szkic`

ffmpeg: z PATH, a gdy go nie ma, z pakietu pip `imageio-ffmpeg` (binarka w pakiecie).
Nie publikuje niczego i nie dotyka sieci. Exit code 1, gdy ktorakolwiek rolka sie nie udala.
"""
import argparse
import datetime
import importlib.util
import io
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social_common as sc  # noqa: E402

_spec = importlib.util.spec_from_file_location(
    'social_render', os.path.join(os.path.dirname(os.path.abspath(__file__)), 'render.py'))
render = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(render)

SCENA_JPEG_Q = 92
CRF = 20
ZOOM_KONIEC = 1.08


def filtr_sceny(n, t, ruch):
    """Filtr ffmpeg dla wejscia n (zapetlony JPEG): wideo 1080x1920@30 dlugosci t sekund."""
    w, h = sc.STORY_WH
    klatki = max(1, int(round(t * sc.REEL_FPS)))
    if ruch in sc.REEL_RUCHY:
        z = "min(1+%.4f*on/%d,%.3f)" % (ZOOM_KONIEC - 1, klatki, ZOOM_KONIEC)
        if ruch == 'ken-burns':
            x = "(iw-iw/zoom)*on/%d" % klatki      # przesuw w prawo w trakcie przyblizania
            y = "(ih-ih/zoom)/2"
        else:
            x, y = "iw/2-(iw/zoom/2)", "ih/2-(ih/zoom/2)"
        return ("[%d:v]scale=%d:%d:flags=lanczos,zoompan=z='%s':x='%s':y='%s':d=1:s=%dx%d:fps=%d,"
                "trim=duration=%.3f,setpts=PTS-STARTPTS,setsar=1,format=yuv420p,fps=%d[s%d]"
                % (n, w * 2, h * 2, z, x, y, w, h, sc.REEL_FPS, t, sc.REEL_FPS, n))
    return ("[%d:v]scale=%d:%d,fps=%d,trim=duration=%.3f,setpts=PTS-STARTPTS,setsar=1,format=yuv420p,fps=%d[s%d]"
            % (n, w, h, sc.REEL_FPS, t, sc.REEL_FPS, n))


def zbuduj_ffmpeg(exe, sceny_jpg, plan, audio, razem, out):
    """Komenda ffmpeg (lista argumentow). plan = sc.reel_plan(d)[0]."""
    cmd = [exe, '-hide_banner', '-loglevel', 'error', '-y']
    for (nr, _sz, t, _prz, _ruch), jpg in zip(plan, sceny_jpg):
        cmd += ['-loop', '1', '-framerate', str(sc.REEL_FPS), '-t', '%.3f' % t, '-i', jpg]
    a_idx = len(plan)
    if audio:
        cmd += ['-i', audio]
    else:
        cmd += ['-f', 'lavfi', '-t', '%.3f' % razem, '-i', 'anullsrc=channel_layout=stereo:sample_rate=48000']
    filtry = [filtr_sceny(i, t, ruch) for i, (_nr, _sz, t, _prz, ruch) in enumerate(plan)]
    biezacy, dlugosc = '[s0]', plan[0][2]
    for i in range(1, len(plan)):
        prz = plan[i - 1][3]
        wyj = '[v%d]' % i
        if prz in ('fade', 'slide'):
            T = sc.REEL_PRZEJSCIE_SEK
            filtry.append('%s[s%d]xfade=transition=%s:duration=%.3f:offset=%.3f%s'
                          % (biezacy, i, 'fade' if prz == 'fade' else 'slideleft', T, dlugosc - T, wyj))
            dlugosc += plan[i][2] - T
        else:
            # concat gubi informacje o stalym fps, a xfade jej wymaga: ustawiamy ja jawnie
            filtry.append('%s[s%d]concat=n=2:v=1:a=0,fps=%d%s' % (biezacy, i, sc.REEL_FPS, wyj))
            dlugosc += plan[i][2]
        biezacy = wyj
    filtry.append('%sformat=yuv420p[vout]' % biezacy)
    if audio:
        filtry.append('[%d:a]aresample=48000,atrim=0:%.3f,afade=t=out:st=%.3f:d=1,asetpts=PTS-STARTPTS[aout]'
                      % (a_idx, razem, max(0.0, razem - 1.0)))
        amap = '[aout]'
    else:
        amap = '%d:a' % a_idx
    cmd += ['-filter_complex', ';'.join(filtry), '-map', '[vout]', '-map', amap,
            '-c:v', 'libx264', '-profile:v', 'high', '-level:v', '4.1', '-pix_fmt', 'yuv420p',
            '-r', str(sc.REEL_FPS), '-g', str(sc.REEL_FPS * 2), '-crf', str(CRF), '-preset', 'medium',
            '-c:a', 'aac', '-b:a', '128k', '-ar', '48000', '-ac', '2',
            '-movflags', '+faststart', '-t', '%.3f' % razem, out]
    return cmd


def czasy_scen(plan):
    """[(nr, start_s, koniec_s)] na osi rolki (do storyboardu w PDF i podgladu)."""
    out, t0 = [], 0.0
    for i, (nr, _sz, t, _prz, _ruch) in enumerate(plan):
        out.append((nr, round(t0, 2), round(t0 + t, 2)))
        nakladka = sc.REEL_PRZEJSCIE_SEK if i < len(plan) - 1 and plan[i][3] in ('fade', 'slide') else 0.0
        t0 += t - nakladka
    return out


def klatki(exe, mp4, katalog, czasy):
    os.makedirs(katalog, exist_ok=True)
    out = []
    for t in czasy:
        p = os.path.join(katalog, 'klatka-%05.2fs.png' % t)
        subprocess.run([exe, '-hide_banner', '-loglevel', 'error', '-y', '-ss', '%.2f' % t, '-i', mp4,
                        '-frames:v', '1', p], check=True, timeout=120)
        out.append(p)
    return out


def renderuj_rolke(path, page, exe, katalog_klatek=None):
    d, _ = sc.wczytaj(path)
    pid = (d.get('id') or '').strip()
    if not pid:
        return False, ['brak pola `id`']
    if d.get('typ') != 'reel':
        return False, ['typ `%s`: reel-render.py renderuje tylko rolki (reszta: render.py)' % d.get('typ')]
    slajdy = [s for s in (d.get('slajdy') or []) if isinstance(s, dict)]
    if len(slajdy) < 2:
        return False, ['rolka wymaga co najmniej 2 scen']
    plan, razem = sc.reel_plan(d)
    if not (sc.REEL_CZAS_MIN <= razem <= sc.REEL_CZAS_MAX):
        return False, ['rolka trwalaby %.1f s, wymagane %d-%d s' % (razem, sc.REEL_CZAS_MIN, sc.REEL_CZAS_MAX)]
    for nr, _sz, t, prz, ruch in plan:
        if prz not in sc.REEL_PRZEJSCIA:
            return False, ['scena %d: przejscie `%s` poza %s' % (nr, prz, '/'.join(sc.REEL_PRZEJSCIA))]
        if ruch and ruch not in sc.REEL_RUCHY:
            return False, ['scena %d: ruch `%s` poza %s' % (nr, ruch, '/'.join(sc.REEL_RUCHY))]
    audio = d.get('audio')
    if audio:
        if not str(d.get('audio_licencja') or '').strip():
            return False, ['`audio` bez `audio_licencja`: bez licencji zostaw audio null (cicha sciezka)']
        audio = sc.abs_repo(audio)
        if not os.path.isfile(audio):
            return False, ['brak pliku audio %s' % d.get('audio')]
    cov = d.get('cover_slajd') or 1
    if not isinstance(cov, int) or not (1 <= cov <= len(slajdy)):
        return False, ['cover_slajd `%s` poza 1-%d' % (cov, len(slajdy))]

    out_dir = os.path.join(sc.MEDIA, pid)
    sceny_dir = os.path.join(out_dir, 'sceny')
    os.makedirs(sceny_dir, exist_ok=True)
    logo = render._logo_svg()
    ostrz, kontrasty, sceny_jpg = [], {}, []
    for i, sl in enumerate(slajdy, 1):
        try:
            png, o, k = render.renderuj_slajd(page, pid, sl, i, len(slajdy), 'reel', logo)
        except render.BladSlajdu as e:
            return False, [str(e)]
        ostrz.extend(o)
        if k:
            kontrasty[str(i)] = k
        jpg = os.path.join(sceny_dir, '%02d.jpg' % i)
        render.do_jpeg(png, jpg)
        sceny_jpg.append(jpg)
        if i == cov:
            render.do_jpeg(png, os.path.join(out_dir, 'cover.jpg'))
    for stary in os.listdir(sceny_dir):  # sceny z poprzedniego renderu (bylo 7, jest 5)
        if os.path.join(sceny_dir, stary) not in sceny_jpg:
            os.remove(os.path.join(sceny_dir, stary))

    mp4_rel, cover_rel = sc.reel_media(pid)
    mp4 = sc.abs_repo(mp4_rel)
    tmp = mp4 + '.tmp.mp4'
    cmd = zbuduj_ffmpeg(exe, sceny_jpg, plan, audio, razem, tmp)
    proc = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    if proc.returncode != 0:
        return False, ['ffmpeg: %s' % (proc.stderr or '').strip()[-600:]]
    os.replace(tmp, mp4)
    try:
        info = sc.sonda_wideo(mp4)
    except RuntimeError as e:
        return False, ['ffprobe: %s' % e]
    problemy = sc.problemy_wideo(info)
    if problemy:
        return False, ['reel.mp4: %s' % p for p in problemy]

    manifest = {
        'id': pid,
        'hash_slajdow': sc.hash_slajdow(d),
        'wyrenderowano': datetime.datetime.now().isoformat(timespec='seconds'),
        'media': [mp4_rel, cover_rel],
        'sceny': [{'scena': nr, 'plik': sc.rel(j), 'start_s': a, 'koniec_s': b}
                  for (nr, a, b), j in zip(czasy_scen(plan), sceny_jpg)],
        'wideo': info,
        'audio': d.get('audio') or None,
        'ostrzezenia': ostrz,
    }
    obrazy = sc.obrazy_slajdow(d)
    if obrazy:
        manifest['obrazy'] = [{'slajd': n, 'obraz': p, 'sha256_16': sc.odcisk_pliku(sc.abs_repo(p))}
                              for n, p in obrazy]
        manifest['kontrast'] = kontrasty
    sc.zapisz(os.path.join(out_dir, '_render.json'), manifest)
    d['media'] = [mp4_rel, cover_rel]
    sc.zapisz(path, d)

    opis = ['%.2f s, %dx%d, %s fps, %s/%s, audio %s %s Hz, %.1f MB' % (
        info['czas'], info['w'], info['h'], info['fps'], info['vcodec'], info['pix_fmt'],
        info['acodec'], info['audio_hz'], info['bajty'] / 1048576.0)]
    if katalog_klatek:
        t = [min(info['czas'] - 0.05, max(0.05, x)) for x in
             [a + (b - a) * 0.6 for _nr, a, b in czasy_scen(plan)]]
        for p in klatki(exe, mp4, katalog_klatek, t[:4] if len(t) <= 4 else [t[0], t[1], t[len(t) // 2 + 1], t[-1]]):
            opis.append('klatka: %s' % p)
    return True, opis + ostrz


def main():
    ap = argparse.ArgumentParser(description='Render rolki IG MindSync: sceny -> MP4 + okladka')
    ap.add_argument('posty', nargs='*', help='id rolki albo sciezka do JSON')
    ap.add_argument('--all-szkic', action='store_true', help='wszystkie rolki o statusie szkic (bez plikow _)')
    ap.add_argument('--klatki', help='katalog na 4 klatki PNG z gotowego MP4 (kontrola wizualna)')
    a = ap.parse_args()

    sciezki = []
    for ref in a.posty:
        p = sc.znajdz(ref)
        if not p:
            sys.exit('X  nie znalazlem posta: %s' % ref)
        sciezki.append(p)
    if a.all_szkic:
        for p in sc.pliki_kolejki():
            try:
                d, _ = sc.wczytaj(p)
            except Exception:  # noqa: BLE001
                continue
            if d.get('typ') == 'reel' and d.get('status') == 'szkic' and p not in sciezki:
                sciezki.append(p)
    if not sciezki:
        ap.error('podaj id/sciezke rolki albo --all-szkic')

    exe = sc.ffmpeg_exe()
    if not exe:
        sys.exit('Brak ffmpeg. Zainstaluj ffmpeg (PATH) albo: pip install imageio-ffmpeg')
    render._zaleznosci()
    from playwright.sync_api import sync_playwright

    bledy = 0
    with sync_playwright() as pw:
        browser = pw.chromium.launch(args=['--allow-file-access-from-files', '--force-color-profile=srgb'])
        page = browser.new_page(device_scale_factor=1)
        for p in sciezki:
            try:
                ok, info = renderuj_rolke(p, page, exe, a.klatki)
            except Exception as e:  # noqa: BLE001
                ok, info = False, ['wyjatek: %s' % e]
            print('[%s] %s' % (' OK ' if ok else 'BLAD', os.path.basename(p)))
            for o in info:
                print('    %s  %s' % ('-' if ok else 'X', o))
            bledy += 0 if ok else 1
        browser.close()
    print('\nWyrenderowano %d/%d rolek. ffmpeg: %s' % (len(sciezki) - bledy, len(sciezki), shutil.which('ffmpeg') or exe))
    sys.exit(1 if bledy else 0)


if __name__ == '__main__':
    main()
