#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detektor wiekszych zmian wizualnych w aplikacji (repo mindsync-frontend) pod hook Claude Code.

Tryby:
  1. Hook PostToolUse (Bash): JSON hooka na stdin ({"tool_input": {"command": ...}, "cwd": ...}).
     Dziala tylko, gdy komenda zawiera `git commit`; sprawdza OSTATNI commit repo frontu.
  2. Recznie: python scripts/social/ui-change-detector.py --range A..B   (albo --range HEAD~3..HEAD)
     Recznie bez --range = ostatni commit (HEAD~1..HEAD).

"Wieksza zmiana wizualna" (progi nizej) = nowy plik ekranu (*_screen.dart) LUB co najmniej
PROG_LINII zmienionych linii kodu UI LUB co najmniej PROG_WIDGETOW zmienionych
plikow widgetow w lib/ui/** (realnie: lib/screens/** i lib/widgets/**, bez cubitow/blocow
i kodu generowanego). Liczone sa tez zmienione assety graficzne i nowe klucze l10n (ARB),
jako kontekst dla operatora.

Gdy zmiana jest wieksza: wypisuje na stdout JSON zgodny z hookami Claude Code
({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": "..."}}), ktory
prosi sesje, zeby ZAPYTALA operatora o tresc na Instagram. W przeciwnym razie nic nie wypisuje.
NIGDY nie blokuje: zawsze exit 0, takze przy bledach (log na stderr). Ostatnio zgloszony commit
zapisuje w social/.ui-detector-state.json, zeby nie pytac dwa razy o to samo.

Hooka NIE konfiguruje ten skrypt (settings.json ustawia sesja glowna). Przyklad wpisu:
  "PostToolUse": [{"matcher": "Bash", "hooks": [{"type": "command",
     "command": "python scripts/social/ui-change-detector.py"}]}]
"""
import argparse
import datetime
import io
import json
import os
import re
import subprocess
import sys

# ---- progi (stale, zmieniaj tutaj) --------------------------------------------------------
PROG_LINII = 80          # zmienione linie (dodane + usuniete) w lib/ui/**
PROG_WIDGETOW = 3        # zmienione pliki .dart w lib/ui/** (poza nowymi ekranami)
APP = 'mindsync_app'
# Kod UI: lib/ui/ (nazwa z CLAUDE.md) ORAZ realna struktura repo: lib/screens/ i lib/widgets/.
UI_PREFIXES = (APP + '/lib/ui/', APP + '/lib/screens/', APP + '/lib/widgets/')
# poza UI: logika stanu i kod generowany (zmiana cubita to nie zmiana wizualna)
NIE_UI_RE = re.compile(r'(/cubit/|/bloc/|/blocs/|_cubit\.dart$|_bloc\.dart$|_state\.dart$|_event\.dart$|'
                       r'\.freezed\.dart$|\.g\.dart$|\.gr\.dart$|\.mocks\.dart$)')
EKRAN_RE = re.compile(r'_screen\.dart$')
EKRAN_PREFIXES = (APP + '/lib/',)              # nowe *_screen.dart gdziekolwiek w lib/ (lib/screens/ tez)
ASSET_RE = re.compile(r'^' + re.escape(APP) + r'/assets/.*\.(png|jpe?g|webp|svg|gif|json|riv|lottie)$', re.I)
ARB_RE = re.compile(r'^' + re.escape(APP) + r'/lib/l10n/.*\.arb$|^' + re.escape(APP) + r'/l10n/.*\.arb$', re.I)
# klucz najwyzszego poziomu ARB (wciecie 0-2 spacje); zagniezdzone "placeholders" itp. pomijane
ARB_KLUCZ_RE = re.compile(r'^\+ {0,2}"([A-Za-z][A-Za-z0-9_]*)"\s*:')

ROOT = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..'))
FRONT_REPO = os.path.join(ROOT, 'mindsync-frontend')
STATE = os.path.join(ROOT, 'social', '.ui-detector-state.json')


def log(msg):
    sys.stderr.write('[ui-change-detector] %s\n' % msg)


def git(repo, *args):
    p = subprocess.run(['git', '-C', repo] + list(args), capture_output=True, text=True,
                       encoding='utf-8', errors='replace', timeout=60)
    if p.returncode != 0:
        raise RuntimeError('git %s: %s' % (' '.join(args), p.stderr.strip()[:300]))
    return p.stdout


def rozwin_zakres(repo, zakres):
    """'A..B' -> (A, B) jako pelne sha. Pierwszy commit repo (brak rodzica) = pusty drzewo."""
    if '..' not in zakres:
        zakres = '%s~1..%s' % (zakres, zakres)
    a, b = zakres.split('..', 1)
    b_sha = git(repo, 'rev-parse', b or 'HEAD').strip()
    try:
        a_sha = git(repo, 'rev-parse', a).strip()
    except RuntimeError:
        a_sha = git(repo, 'hash-object', '-t', 'tree', os.devnull).strip()  # pusty drzewo
    return a_sha, b_sha


def zbierz_zmiany(repo, a, b):
    """Statystyka zmian A..B: pliki ui (z liczba linii), nowe ekrany, assety, nowe klucze ARB."""
    numstat = git(repo, 'diff', '--numstat', '-M', a, b)
    status = git(repo, 'diff', '--name-status', '-M', a, b)
    nowe = set()
    for line in status.splitlines():
        cz = line.split('\t')
        # tylko dodane pliki; rename (R) istniejacego ekranu to nie nowy ekran
        if cz and cz[0].startswith('A') and len(cz) >= 2:
            nowe.add(cz[-1])
    ui_pliki, ui_linie, assety, ekrany = [], 0, [], []
    for line in numstat.splitlines():
        cz = line.split('\t')
        if len(cz) < 3:
            continue
        dod, usu, sciezka = cz[0], cz[1], cz[2]
        if '=>' in sciezka:  # rename w numstat: "a/{x => y}.dart"
            sciezka = re.sub(r'\{[^{}]* => ([^{}]*)\}', r'\1', sciezka).replace('//', '/')
        linie = (int(dod) if dod.isdigit() else 0) + (int(usu) if usu.isdigit() else 0)
        if ASSET_RE.match(sciezka):
            assety.append(sciezka)
        if sciezka.startswith(EKRAN_PREFIXES) and EKRAN_RE.search(sciezka) and sciezka in nowe:
            ekrany.append(sciezka)
        if sciezka.startswith(UI_PREFIXES) and sciezka.endswith('.dart') and not NIE_UI_RE.search(sciezka):
            ui_pliki.append((sciezka, linie))
            ui_linie += linie
    klucze = []
    pliki_arb = [p for p in status.splitlines() if ARB_RE.search(p.split('\t')[-1])]
    if pliki_arb:
        # klucze dodane w angielskim ARB (albo w pierwszym zmienionym ARB, gdy en nie ma)
        sciezki = [p.split('\t')[-1] for p in pliki_arb]
        cel = next((s for s in sciezki if re.search(r'_en\.arb$', s)), sciezki[0])
        diff = git(repo, 'diff', '-U0', a, b, '--', cel)
        usuniete = {m.group(1) for m in (re.match(r'^-\s*"([A-Za-z][A-Za-z0-9_]*)"\s*:', ln)
                                          for ln in diff.splitlines()) if m}
        for ln in diff.splitlines():
            m = ARB_KLUCZ_RE.match(ln)
            if m and not m.group(1).startswith('@') and m.group(1) not in usuniete:
                klucze.append(m.group(1))
    widgety = [p for p, _ in ui_pliki if p not in ekrany]
    return {'ui_pliki': ui_pliki, 'ui_linie': ui_linie, 'ekrany': ekrany, 'widgety': widgety,
            'assety': assety, 'klucze_l10n': klucze}


def wieksza_zmiana(z):
    """(bool, [powody])."""
    powody = []
    if z['ekrany']:
        powody.append('nowy ekran: %s' % ', '.join(os.path.basename(e) for e in z['ekrany']))
    if z['ui_linie'] >= PROG_LINII:
        powody.append('%d zmienionych linii kodu UI (prog %d)' % (z['ui_linie'], PROG_LINII))
    if len(z['widgety']) >= PROG_WIDGETOW:
        powody.append('%d zmienionych plikow widgetow (prog %d)' % (len(z['widgety']), PROG_WIDGETOW))
    return bool(powody), powody


def nazwy_shotow(z):
    """Propozycje nazw shotow harnessu z nazw ekranow/widgetow (habit_tracker_screen.dart -> habit_tracker)."""
    out = []
    for p in z['ekrany'] + [p for p, _ in sorted(z['ui_pliki'], key=lambda t: -t[1])]:
        n = re.sub(r'(_screen|_widget|_card|_view|_sheet)?\.dart$', '', os.path.basename(p))
        if n and n not in out:
            out.append(n)
    return out[:5]


def tekst_kontekstu(b, z, powody, opisy):
    pliki = [p for p, _ in sorted(z['ui_pliki'], key=lambda t: -t[1])][:8]
    czesci = [
        'Wykryto wieksza zmiane wizualna w aplikacji MindSync (repo mindsync-frontend, commit %s).' % b[:7],
        'Powody: %s.' % '; '.join(powody),
    ]
    if opisy:
        czesci.append('Commity: %s.' % ' | '.join(opisy[:5]))
    if z['ekrany']:
        czesci.append('Nowe ekrany: %s.' % ', '.join(z['ekrany']))
    if pliki:
        czesci.append('Najwieksze zmiany w kodzie UI: %s.' % ', '.join(
            '%s (%d linii)' % (p, dict(z['ui_pliki'])[p]) for p in pliki))
    if z['assety']:
        czesci.append('Zmienione assety graficzne: %s.' % ', '.join(z['assety'][:6]))
    if z['klucze_l10n']:
        czesci.append('Nowe klucze tekstow UI (l10n): %s.' % ', '.join(z['klucze_l10n'][:10]))
    shoty = nazwy_shotow(z)
    czesci.append(
        'ZAPYTAJ operatora (nie rob tego sam), czy przygotowac tresc na Instagram o tej zmianie: '
        'post o nowosci (karuzela feature-hero/feature-step albo before/after) i/lub rolke, przez '
        '/social-write w trybie feature. Zaproponuj, ktore ekrany wyrenderowac harnessem: '
        'python scripts/social/app-shots.py run --name <shot> (harness: mindsync-frontend/mindsync_app/'
        'test/marketing_shots/, nowy shot dopisuje flutter-mobile)%s.'
        % ('; kandydaci na shoty: %s' % ', '.join(shoty) if shoty else ''))
    return ' '.join(czesci)


def wczytaj_stan():
    try:
        return json.load(io.open(STATE, encoding='utf-8'))
    except (OSError, ValueError):
        return {}


def zapisz_stan(stan):
    os.makedirs(os.path.dirname(STATE), exist_ok=True)
    tmp = STATE + '.tmp'
    with io.open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        f.write(json.dumps(stan, ensure_ascii=False, indent=2) + '\n')
    os.replace(tmp, STATE)


def czy_hook_commit(dane):
    cmd = ((dane or {}).get('tool_input') or {}).get('command') or ''
    return bool(re.search(r'\bgit\b(?:\s+-\S+(?:\s+\S+)?)*\s+commit\b', cmd))


def wykryj(repo, zakres, recznie=False):
    """Zwraca slownik hooka do wypisania albo None."""
    a, b = rozwin_zakres(repo, zakres)
    stan = wczytaj_stan()
    if not recznie and stan.get('ostatni_zgloszony') == b:
        log('commit %s juz zgloszony, pomijam' % b[:7])
        return None
    z = zbierz_zmiany(repo, a, b)
    duza, powody = wieksza_zmiana(z)
    if not duza:
        return None
    opisy = [ln.strip() for ln in git(repo, 'log', '--format=%h %s', '%s..%s' % (a, b)).splitlines()
             if ln.strip()] if a != b else []
    stan.update({'ostatni_zgloszony': b, 'zgloszono': datetime.datetime.now().isoformat(timespec='seconds'),
                 'powody': powody})
    zapisz_stan(stan)
    return {'hookSpecificOutput': {'hookEventName': 'PostToolUse',
                                   'additionalContext': tekst_kontekstu(b, z, powody, opisy)}}


def main(argv=None, stdin=None):
    try:
        ap = argparse.ArgumentParser(description='Detektor zmian wizualnych frontu (hook Claude Code)')
        ap.add_argument('--range', dest='zakres', help='zakres commitow A..B (tryb reczny)')
        ap.add_argument('--repo', default=FRONT_REPO, help=argparse.SUPPRESS)
        a = ap.parse_args(argv)
        if a.zakres:
            wynik = wykryj(a.repo, a.zakres, recznie=True)
        else:
            stdin = sys.stdin if stdin is None else stdin
            raw = '' if stdin.isatty() else stdin.read()
            dane = json.loads(raw) if raw.strip() else None
            if dane is not None and not czy_hook_commit(dane):
                return 0  # hook z inna komenda Bash: cisza
            wynik = wykryj(a.repo, 'HEAD', recznie=dane is None)
        if wynik:
            sys.stdout.write(json.dumps(wynik, ensure_ascii=False) + '\n')
    except SystemExit as e:  # argparse: zly argument tez nie blokuje
        log('argumenty: %s' % e)
    except Exception as e:  # noqa: BLE001 - nigdy nie blokujemy sesji
        log('blad (ignoruje, exit 0): %s: %s' % (type(e).__name__, e))
    return 0


if __name__ == '__main__':
    sys.exit(main())
