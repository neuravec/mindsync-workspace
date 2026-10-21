#!/usr/bin/env python3
"""Synchronizacja wspólnego workspace MindSync między osobami pracującymi z Claude.

Użycie (z katalogu workspace albo skądkolwiek):
  python scripts/workspace/sync.py pull           # pobierz zmiany partnera we wszystkich repo
  python scripts/workspace/sync.py pull --hook    # to samo, wynik jako JSON dla hooka SessionStart
  python scripts/workspace/sync.py status         # co jest do wypchnięcia (workspace + social)
  python scripts/workspace/sync.py push -m "opis" # commit + pull --rebase + push (workspace + social)
  python scripts/workspace/sync.py push -m "opis" --repo workspace

Zasady:
- pull dotyczy wszystkich repo z listy REPOS. Repo z kodem (backend, frontend, ...) są
  tylko przewijane do przodu (fast-forward), gdy nie mają lokalnych zmian. Nic nie jest
  nadpisywane ani usuwane.
- push dotyczy WYŁĄCZNIE repo stanu współdzielonego: workspace i social. Repo z kodem mają
  własne zasady (push na main backendu = deploy na produkcję, push na dev frontu = TestFlight)
  i ten skrypt ich nie wypycha.
- Przed commitem skrypt skanuje dodane linie i ścieżki pod kątem sekretów. Trafienie
  przerywa commit i zdejmuje pliki z indeksu.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# (folder względem ROOT, nazwa, czy to repo stanu współdzielonego wypychane przez `push`)
REPOS = [
    (".", "workspace", True),
    ("social", "social", True),
    ("MindSync", "backend", False),
    ("mindsync-frontend", "frontend", False),
    ("therapist-deck", "therapist-deck", False),
    ("Mindsync-fleet", "fleet", False),
]

SECRET_PATH_PATTERNS = [
    r"(^|/)\.env$", r"(^|/)\.env\.(?!example$)[^/]+$", r"\.pem$", r"\.p8$", r"\.p12$",
    r"\.jks$", r"\.keystore$", r"(^|/)token\.json$", r"(^|/)client_secret[^/]*\.json$",
    r"(^|/)key[^/]*\.properties$", r"(^|/)itmesh/",
]
SECRET_LINE_PATTERNS = [
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
    r"\"private_key\"\s*:",
    r"AKIA[0-9A-Z]{16}",
    r"\bsk-[A-Za-z0-9_\-]{20,}",
    r"\bsk_live_[A-Za-z0-9]{10,}",
    r"\bghp_[A-Za-z0-9]{30,}",
    r"\bgithub_pat_[A-Za-z0-9_]{30,}",
    r"\bxox[abpors]-[A-Za-z0-9\-]{10,}",
    r"\bAIza[0-9A-Za-z_\-]{30,}",
    r"\bEAA[A-Za-z0-9]{40,}",
    r"\bIGAA[A-Za-z0-9_\-]{40,}",
    r"\bpk_[A-Za-z0-9_\-]{20,}",
    r"postgres(ql)?://[^\s:@/]+:[^\s@/]+@",
    r"hooks\.slack\.com/services/T[A-Za-z0-9]+/",
    r"(?i)(password|passwd|hasło|haslo|pwd)\W{0,3}[`'\"](?=[^`'\"\s]*\d)(?=[^`'\"\s]*[A-Za-z])[^`'\"\s<>]{8,}[`'\"]",
    r"(?i)\b(api[_-]?key|api[_-]?token|access[_-]?token|secret|password|passwd)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-\.]{16,}",
]


def git(repo: Path, *args: str, timeout: int = 90) -> tuple[int, str]:
    try:
        p = subprocess.run(
            ["git", "-C", str(repo), *args],
            capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
        # rstrip, nie strip: `git status --porcelain` zaczyna linie od spacji (" M plik")
        return p.returncode, (p.stdout + p.stderr).rstrip()
    except subprocess.TimeoutExpired:
        return 124, "timeout"
    except FileNotFoundError:
        return 127, "git nie jest zainstalowany albo nie ma go w PATH"


def is_repo(path: Path) -> bool:
    return (path / ".git").exists()


def upstream_counts(repo: Path) -> tuple[str | None, int, int]:
    rc, up = git(repo, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}")
    if rc != 0:
        return None, 0, 0
    rc, out = git(repo, "rev-list", "--left-right", "--count", "HEAD...@{u}")
    if rc != 0:
        return up, 0, 0
    ahead, behind = (int(x) for x in out.split())
    return up, ahead, behind


def dirty_files(repo: Path, include_untracked: bool = True) -> list[str]:
    args = ["status", "--porcelain"]
    if not include_untracked:
        args.append("--untracked-files=no")
    rc, out = git(repo, *args)
    if rc != 0 or not out:
        return []
    return [line[3:] for line in out.splitlines() if line.strip()]


def cmd_pull() -> tuple[str, str]:
    lines: list[str] = []
    problems = 0
    for rel, name, shared in REPOS:
        repo = (ROOT / rel).resolve()
        if not is_repo(repo):
            if rel != ".":
                lines.append(f"- {name}: brak repo w {rel}/ (pominięte; sklonuj je, jeśli go potrzebujesz)")
            else:
                lines.append("- workspace: katalog nie jest repozytorium git")
                problems += 1
            continue
        rc, out = git(repo, "fetch", "--quiet", "--prune", timeout=120)
        if rc != 0:
            lines.append(f"- {name}: fetch nieudany ({out[:200]})")
            problems += 1
            continue
        rc, branch = git(repo, "branch", "--show-current")
        up, ahead, behind = upstream_counts(repo)
        if up is None:
            lines.append(f"- {name} [{branch or 'detached'}]: brak gałęzi śledzonej, pull pominięty")
            continue
        if behind == 0:
            extra = f", {ahead} lokalnych commitów do wypchnięcia" if ahead else ""
            lines.append(f"- {name} [{branch}]: aktualne{extra}")
            continue
        dirty = dirty_files(repo, include_untracked=False)
        if shared:
            rc, out = git(repo, "pull", "--rebase", "--autostash", timeout=180)
            if rc != 0:
                git(repo, "rebase", "--abort")
                lines.append(f"- {name} [{branch}]: KONFLIKT przy pull ({behind} nowych commitów partnera). "
                             f"Nic nie zmieniono, trzeba scalić ręcznie: {out[:300]}")
                problems += 1
            else:
                lines.append(f"- {name} [{branch}]: pobrano {behind} commitów partnera")
        else:
            if dirty:
                lines.append(f"- {name} [{branch}]: {behind} nowych commitów na {up}, ale masz lokalne zmiany "
                             f"({len(dirty)} plików), pull pominięty")
            elif ahead:
                lines.append(f"- {name} [{branch}]: rozjazd z {up} ({ahead} lokalnych, {behind} zdalnych), pull pominięty")
            else:
                rc, out = git(repo, "pull", "--ff-only", timeout=180)
                if rc == 0:
                    lines.append(f"- {name} [{branch}]: pobrano {behind} commitów (fast-forward)")
                else:
                    lines.append(f"- {name} [{branch}]: pull nieudany ({out[:200]})")
                    problems += 1
    header = "Synchronizacja na start sesji (scripts/workspace/sync.py pull):"
    summary = "Workspace zsynchronizowany" if problems == 0 else f"Synchronizacja: {problems} problem(y) do sprawdzenia"
    return header + "\n" + "\n".join(lines), summary


PII_PATTERNS = [
    (r"[A-Za-z0-9._%+-]+@(?!mindsync\.app\b|users\.noreply|example\.|anthropic\.com)[A-Za-z0-9.-]+\.[a-z]{2,}", "e-mail"),
    (r"(?<![A-Za-z0-9_/-])[A-Za-z0-9]{28}(?![A-Za-z0-9_/-])", "ciąg w kształcie Firebase UID"),
]


def pii_hints(repo: Path, files: list[str]) -> list[str]:
    """Miękkie ostrzeżenie: możliwe dane osobowe w zmienionych plikach tekstowych."""
    hints: list[str] = []
    for f in files:
        p = repo / f.strip().strip('"')
        if not p.is_file() or p.suffix.lower() not in {".md", ".txt", ".json", ".py", ".csv", ".sql", ".html", ".yaml", ".yml"}:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except Exception:
            continue
        for pat, label in PII_PATTERNS:
            found = {m.group(0) for m in re.finditer(pat, text) if not re.fullmatch(r"[a-z]+|[A-Z]+|[0-9]+", m.group(0))}
            if found:
                sample = sorted(found)[0]
                hints.append(f"{f}: {label} x{len(found)} (np. {sample[:4]}...)")
    return hints


def cmd_status() -> str:
    out_lines = []
    for rel, name, shared in REPOS:
        repo = (ROOT / rel).resolve()
        if not is_repo(repo):
            continue
        rc, branch = git(repo, "branch", "--show-current")
        up, ahead, behind = upstream_counts(repo)
        files = dirty_files(repo)
        kind = "STAN WSPÓLNY (push przez sync.py)" if shared else "kod (własne zasady commitów)"
        out_lines.append(f"## {name} [{branch}] {kind}: zmienionych plików {len(files)}, "
                         f"do wypchnięcia {ahead}, do pobrania {behind}")
        if shared:
            for f in files[:40]:
                out_lines.append(f"   {f}")
            if len(files) > 40:
                out_lines.append(f"   ... i {len(files) - 40} więcej")
            hints = pii_hints(repo, files)
            if hints:
                out_lines.append("   UWAGA, możliwe dane osobowe (pokaż użytkownikowi przed push, zredaguj albo dodaj do .gitignore):")
                out_lines.extend(f"     - {h}" for h in hints[:20])
    return "\n".join(out_lines)


def scan_staged(repo: Path) -> list[str]:
    hits: list[str] = []
    rc, names = git(repo, "diff", "--cached", "--name-only")
    for n in names.splitlines():
        for pat in SECRET_PATH_PATTERNS:
            if re.search(pat, n.replace("\\", "/")):
                hits.append(f"plik z sekretem w ścieżce: {n}")
                break
    rc, diff = git(repo, "diff", "--cached", "-U0", "--no-color", timeout=180)
    current = "?"
    for line in diff.splitlines():
        if line.startswith("+++ b/"):
            current = line[6:]
            continue
        if not line.startswith("+") or line.startswith("+++"):
            continue
        if re.search(r"\\n\.\.\.\\n|<[A-Z_ ]+>|YOUR[_-]|xxxx|\.\.\.\"", line):
            continue  # przykład z dokumentacji z placeholderem zamiast prawdziwej wartości
        if "pragma: allowlist secret" in line:
            continue  # jawnie oznaczony fałszywy sekret (np. w teście), konwencja detect-secrets
        for pat in SECRET_LINE_PATTERNS:
            if re.search(pat, line):
                hits.append(f"podejrzana linia w {current}: {line[:80]}...")
                break
    return hits


def cmd_push(message: str, only: str | None) -> int:
    rc_total = 0
    for rel, name, shared in REPOS:
        if not shared or (only and name != only):
            continue
        repo = (ROOT / rel).resolve()
        if not is_repo(repo):
            continue
        files = dirty_files(repo)
        up, ahead, behind = upstream_counts(repo)
        if not files and ahead == 0:
            print(f"{name}: nic do wypchnięcia")
            continue
        if files:
            git(repo, "add", "-A")
            hits = scan_staged(repo)
            if hits:
                git(repo, "reset", "-q")
                print(f"{name}: PRZERWANO, wykryto możliwe sekrety (nic nie zacommitowano):")
                for h in hits[:30]:
                    print("  - " + h)
                rc_total = 2
                continue
            rc, out = git(repo, "commit", "-m", message)
            if rc != 0:
                print(f"{name}: commit nieudany: {out[:300]}")
                rc_total = 1
                continue
            print(f"{name}: commit OK")
        if up is not None:
            rc, out = git(repo, "pull", "--rebase", "--autostash", timeout=180)
            if rc != 0:
                git(repo, "rebase", "--abort")
                print(f"{name}: KONFLIKT z commitami partnera, push wstrzymany. Scal ręcznie: {out[:300]}")
                rc_total = 1
                continue
            rc, out = git(repo, "push", timeout=180)
        else:
            rc, branch = git(repo, "branch", "--show-current")
            rc, out = git(repo, "push", "-u", "origin", branch, timeout=180)
        print(f"{name}: " + ("push OK" if rc == 0 else f"push nieudany: {out[:300]}"))
        if rc != 0:
            rc_total = 1
    return rc_total


def main() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p_pull = sub.add_parser("pull")
    p_pull.add_argument("--hook", action="store_true", help="wynik jako JSON dla hooka SessionStart")
    sub.add_parser("status")
    p_push = sub.add_parser("push")
    p_push.add_argument("-m", "--message", required=True)
    p_push.add_argument("--repo", choices=[n for _, n, s in REPOS if s])
    args = ap.parse_args()

    if args.cmd == "pull":
        try:
            report, summary = cmd_pull()
        except Exception as e:  # hook nigdy nie może wywrócić startu sesji
            report, summary = f"Synchronizacja nie powiodła się: {e}", "Synchronizacja nie powiodła się"
        if args.hook:
            context = (report + "\n\nZasada: przed pracą przejrzyj ten raport. Konflikt albo pominięty pull "
                       "zgłoś użytkownikowi na początku odpowiedzi.")
            print(json.dumps({
                "systemMessage": summary,
                "hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context},
            }, ensure_ascii=False))
        else:
            print(report)
        return 0
    if args.cmd == "status":
        print(cmd_status())
        return 0
    if args.cmd == "push":
        return cmd_push(args.message, args.repo)
    return 1


if __name__ == "__main__":
    sys.exit(main())
