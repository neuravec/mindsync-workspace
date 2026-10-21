#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Prawdziwe ekrany aplikacji do postow o nowosciach (wariant D): uruchamia harness Fluttera.

Harness lezy w repo frontu: mindsync-frontend/mindsync_app/test/marketing_shots/ (wlasciciel:
flutter-mobile). Kazdy test zapisuje PNG 1179x2556 (iPhone, DPR 3) do
social/images/app-shots/<name>.png. Ten skrypt go TYLKO uruchamia i prowadzi manifest
social/images/app-shots/_manifest.json (nazwa, plik, wymiary, rozmiar, data renderu,
commit frontu), zeby bylo wiadomo, z jakiej wersji aplikacji pochodzi ekran w poscie.

Uzycie:
    python scripts/social/app-shots.py run                     # wszystkie shoty (tag marketing)
    python scripts/social/app-shots.py run --name habit_tracker_weekly
    python scripts/social/app-shots.py list                    # dostepne shoty z data i rozmiarem
    python scripts/social/app-shots.py list --json

`run` dziala na pierwszym planie (flutter test na samym katalogu test/marketing_shots, nigdy
calego pakietu: pelny `flutter test` w tym repo potrafi skonczyc sie OOM). Nie zmienia niczego
w repo frontu. Exit code = kod flutter test (0 = wszystkie shoty OK).
"""
import argparse
import datetime
import glob
import io
import json
import os
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import social_common as sc  # noqa: E402

FRONT_REPO = os.path.join(sc.ROOT, 'mindsync-frontend')
FRONT_APP = os.path.join(FRONT_REPO, 'mindsync_app')
SHOTS_TEST_DIR = 'test/marketing_shots'
SHOTS_DIR = os.path.join(sc.SOCIAL, 'images', 'app-shots')
MANIFEST = os.path.join(SHOTS_DIR, '_manifest.json')
TIMEOUT_SEK = 1800


def commit_frontu():
    """Krotki sha HEAD repo frontu (+ '-dirty', gdy lib/ ma niezacommitowane zmiany) albo None."""
    try:
        sha = subprocess.run(['git', '-C', FRONT_REPO, 'rev-parse', '--short', 'HEAD'],
                             capture_output=True, text=True, timeout=30).stdout.strip()
        if not sha:
            return None
        brudny = subprocess.run(['git', '-C', FRONT_REPO, 'status', '--porcelain', '--', 'mindsync_app/lib'],
                                capture_output=True, text=True, timeout=30).stdout.strip()
        return sha + ('-dirty' if brudny else '')
    except (OSError, subprocess.SubprocessError):
        return None


def wczytaj_manifest():
    try:
        d = json.load(io.open(MANIFEST, encoding='utf-8-sig'))
        return d if isinstance(d, dict) and isinstance(d.get('shoty'), dict) else {'shoty': {}}
    except (OSError, ValueError):
        return {'shoty': {}}


def opis_pliku(path):
    info = {'plik': sc.rel(path), 'bajty': os.path.getsize(path),
            'zmodyfikowano': datetime.datetime.fromtimestamp(os.path.getmtime(path)).isoformat(timespec='seconds')}
    try:
        from PIL import Image
        with Image.open(path) as im:
            info['wymiary'] = '%dx%d' % im.size
    except Exception:  # noqa: BLE001
        info['wymiary'] = '?'
    return info


def aktualizuj_manifest(start_ts, commit, nazwa=None):
    """Dopisuje do manifestu shoty zapisane po `start_ts` (czyli w tym przebiegu)."""
    man = wczytaj_manifest()
    nowe = []
    for p in sorted(glob.glob(os.path.join(SHOTS_DIR, '*.png'))):
        n = os.path.splitext(os.path.basename(p))[0]
        if nazwa and n != nazwa:
            continue
        if os.path.getmtime(p) + 1 < start_ts:
            continue  # plik sprzed tego przebiegu (nie byl renderowany teraz)
        wpis = opis_pliku(p)
        wpis.update({'nazwa': n, 'wyrenderowano': wpis['zmodyfikowano'], 'frontend_commit': commit})
        man['shoty'][n] = wpis
        nowe.append(n)
    man['zaktualizowano'] = datetime.datetime.now().isoformat(timespec='seconds')
    os.makedirs(SHOTS_DIR, exist_ok=True)
    sc.zapisz(MANIFEST, man)
    return nowe


def flutter_cmd():
    exe = shutil.which('flutter') or shutil.which('flutter.bat')
    if not exe:
        raise SystemExit('X  nie znalazlem `flutter` w PATH')
    return exe


def cmd_run(a):
    if not os.path.isdir(os.path.join(FRONT_APP, *SHOTS_TEST_DIR.split('/'))):
        raise SystemExit('X  brak harnessu %s/%s (wlasciciel: flutter-mobile)' % (sc.rel(FRONT_APP), SHOTS_TEST_DIR))
    os.makedirs(SHOTS_DIR, exist_ok=True)
    cel = SHOTS_TEST_DIR
    if a.name:
        plik = os.path.join(FRONT_APP, *SHOTS_TEST_DIR.split('/'), a.name + '_shot_test.dart')
        cel = SHOTS_TEST_DIR + '/' + a.name + '_shot_test.dart' if os.path.isfile(plik) else SHOTS_TEST_DIR
    cmd = [flutter_cmd(), 'test', cel, '--tags', 'marketing', '--run-skipped']
    if a.name and cel == SHOTS_TEST_DIR:
        cmd += ['--name', a.name]
    env = dict(os.environ)
    env['MARKETING_SHOTS_DIR'] = SHOTS_DIR  # jawnie: shoty zawsze laduja w tym repo
    commit = commit_frontu()
    print('>> %s   (cwd %s, commit frontu %s)' % (' '.join(cmd[1:]), sc.rel(FRONT_APP), commit or '?'))
    start = datetime.datetime.now().timestamp()
    try:
        rc = subprocess.run(cmd, cwd=FRONT_APP, env=env, timeout=TIMEOUT_SEK).returncode
    except subprocess.TimeoutExpired:
        print('X  flutter test przekroczyl %d s' % TIMEOUT_SEK)
        rc = 1
    nowe = aktualizuj_manifest(start, commit, a.name)
    print('\nZapisane w tym przebiegu: %s' % (', '.join(nowe) if nowe else 'nic'))
    print('Manifest: %s' % sc.rel(MANIFEST))
    if rc == 0 and not nowe:
        print('!  flutter test zakonczyl sie OK, ale nie powstal zaden PNG (zla nazwa? brak testow z tagiem?)')
        rc = 2
    return rc


def cmd_list(a):
    man = wczytaj_manifest()['shoty']
    wiersze = []
    for p in sorted(glob.glob(os.path.join(SHOTS_DIR, '*.png'))):
        n = os.path.splitext(os.path.basename(p))[0]
        w = opis_pliku(p)
        m = man.get(n) or {}
        w.update({'nazwa': n, 'frontend_commit': m.get('frontend_commit'),
                  'wyrenderowano': m.get('wyrenderowano') or w['zmodyfikowano']})
        wiersze.append(w)
    if a.json:
        print(json.dumps(wiersze, ensure_ascii=False, indent=2))
        return 0
    if not wiersze:
        print('Brak shotow w %s. Uruchom: python scripts/social/app-shots.py run' % sc.rel(SHOTS_DIR))
        return 0
    print('%-30s %-10s %8s  %-19s  %s' % ('nazwa', 'wymiary', 'KB', 'wyrenderowano', 'commit frontu'))
    for w in wiersze:
        print('%-30s %-10s %8d  %-19s  %s' % (w['nazwa'], w['wymiary'], w['bajty'] // 1024,
                                            w['wyrenderowano'], w['frontend_commit'] or '?'))
    print('\nW poscie: "ekran": "%s/<nazwa>.png"' % sc.rel(SHOTS_DIR))
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description='Prawdziwe ekrany aplikacji (harness Fluttera) dla postow IG')
    sub = ap.add_subparsers(dest='cmd', required=True)
    r = sub.add_parser('run', help='uruchom flutter test --tags marketing (pierwszy plan)')
    r.add_argument('--name', help='jeden shot, np. habit_tracker_weekly')
    lst = sub.add_parser('list', help='dostepne shoty')
    lst.add_argument('--json', action='store_true')
    a = ap.parse_args(argv)
    return cmd_run(a) if a.cmd == 'run' else cmd_list(a)


if __name__ == '__main__':
    sys.exit(main())
