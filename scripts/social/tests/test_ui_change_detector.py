"""Testy detektora zmian wizualnych frontu (tymczasowe repo git, zero sieci).

Uruchom:  python -m pytest scripts/social/tests/test_ui_change_detector.py -q
"""

from __future__ import annotations

import importlib.util
import io
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SOCIAL_DIR = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("ui_change_detector", SOCIAL_DIR / "ui-change-detector.py")
det = importlib.util.module_from_spec(spec)
sys.modules["ui_change_detector"] = det
spec.loader.exec_module(det)

pytestmark = pytest.mark.skipif(shutil.which("git") is None, reason="brak git")


def run(repo: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(repo)] + list(args), capture_output=True, text=True,
                          check=True).stdout


def write(repo: Path, rel: str, text: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def commit(repo: Path, msg: str) -> str:
    run(repo, "add", "-A")
    run(repo, "-c", "user.email=t@t", "-c", "user.name=t", "commit", "-q", "-m", msg)
    return run(repo, "rev-parse", "HEAD").strip()


@pytest.fixture
def repo(tmp_path, monkeypatch):
    r = tmp_path / "mindsync-frontend"
    r.mkdir()
    run(r, "init", "-q")
    write(r, "mindsync_app/lib/main.dart", "void main() {}\n")
    write(r, "mindsync_app/lib/l10n/app_en.arb", '{\n  "hello": "Hello"\n}\n')
    commit(r, "init")
    monkeypatch.setattr(det, "STATE", str(tmp_path / "social" / ".ui-detector-state.json"))
    return r


def lines(n: int) -> str:
    return "".join(f"// line {i}\n" for i in range(n))


def hook_stdin(cmd: str) -> io.StringIO:
    return io.StringIO(json.dumps({"tool_input": {"command": cmd}, "cwd": "x", "hook_event_name": "PostToolUse"}))


def call(repo: Path, argv: list[str] | None = None, stdin=None, capsys=None):
    rc = det.main((argv or []) + ["--repo", str(repo)], stdin=stdin or io.StringIO(""))
    out = capsys.readouterr().out if capsys else ""
    return rc, out


def test_new_screen_triggers_hook_json(repo, capsys):
    write(repo, "mindsync_app/lib/screens/habits/habit_tracker_screen.dart", lines(10))
    sha = commit(repo, "feat: habit tracker screen")
    rc, out = call(repo, stdin=hook_stdin('git commit -m "feat"'), capsys=capsys)
    assert rc == 0
    d = json.loads(out)
    hso = d["hookSpecificOutput"]
    assert hso["hookEventName"] == "PostToolUse"
    ctx = hso["additionalContext"]
    assert "habit_tracker_screen.dart" in ctx and "ZAPYTAJ operatora" in ctx and "app-shots.py" in ctx
    assert "habit_tracker" in ctx  # kandydat na shot
    assert sha[:7] in ctx
    stan = json.loads(Path(det.STATE).read_text(encoding="utf-8"))
    assert stan["ostatni_zgloszony"] == sha


def test_same_commit_not_reported_twice(repo, capsys):
    write(repo, "mindsync_app/lib/screens/a/a_screen.dart", lines(5))
    commit(repo, "a")
    _, out1 = call(repo, stdin=hook_stdin("git commit -am x"), capsys=capsys)
    _, out2 = call(repo, stdin=hook_stdin("git commit -am x"), capsys=capsys)
    assert out1.strip() and out2.strip() == ""


def test_many_lines_in_ui_triggers(repo, capsys):
    write(repo, "mindsync_app/lib/widgets/card.dart", lines(det.PROG_LINII))
    commit(repo, "big widget")
    _, out = call(repo, stdin=hook_stdin("git commit -m big"), capsys=capsys)
    assert "zmienionych linii kodu UI" in json.loads(out)["hookSpecificOutput"]["additionalContext"]


def test_three_widget_files_trigger_and_l10n_keys_listed(repo, capsys):
    for n in ("a", "b", "c"):
        write(repo, f"mindsync_app/lib/screens/main_tab/widgets/{n}_card.dart", lines(3))
    write(repo, "mindsync_app/lib/l10n/app_en.arb",
          '{\n  "hello": "Hello",\n  "habitsTitle": "Habits",\n  "@habitsTitle": {\n    "placeholders": {}\n  }\n}\n')
    commit(repo, "widgets")
    _, out = call(repo, stdin=hook_stdin("git commit -m w"), capsys=capsys)
    ctx = json.loads(out)["hookSpecificOutput"]["additionalContext"]
    assert "3 zmienionych plikow widgetow" in ctx
    assert "habitsTitle" in ctx and "placeholders" not in ctx


def test_small_change_is_silent(repo, capsys):
    write(repo, "mindsync_app/lib/widgets/card.dart", lines(10))
    commit(repo, "small")
    rc, out = call(repo, stdin=hook_stdin("git commit -m small"), capsys=capsys)
    assert rc == 0 and out == ""


def test_cubit_and_generated_code_not_counted(repo, capsys):
    write(repo, "mindsync_app/lib/screens/main_tab/cubit/habits_cubit.dart", lines(300))
    write(repo, "mindsync_app/lib/screens/main_tab/cubit/habits_state.freezed.dart", lines(300))
    write(repo, "mindsync_app/lib/widgets/x.g.dart", lines(300))
    commit(repo, "logic only")
    rc, out = call(repo, stdin=hook_stdin("git commit -m logic"), capsys=capsys)
    assert rc == 0 and out == ""


def test_non_commit_command_is_ignored(repo, capsys):
    write(repo, "mindsync_app/lib/screens/a/a_screen.dart", lines(5))
    commit(repo, "a")
    rc, out = call(repo, stdin=hook_stdin("git status"), capsys=capsys)
    assert rc == 0 and out == ""
    assert not Path(det.STATE).exists()


def test_manual_range(repo, capsys):
    base = run(repo, "rev-parse", "HEAD").strip()
    write(repo, "mindsync_app/lib/screens/a/one_screen.dart", lines(5))
    commit(repo, "one")
    write(repo, "mindsync_app/lib/screens/b/two_screen.dart", lines(5))
    commit(repo, "two")
    rc, out = call(repo, ["--range", f"{base}..HEAD"], capsys=capsys)
    ctx = json.loads(out)["hookSpecificOutput"]["additionalContext"]
    assert "one_screen.dart" in ctx and "two_screen.dart" in ctx
    # tryb reczny zglasza ponownie (operator sam pyta), hook juz nie
    _, again = call(repo, ["--range", f"{base}..HEAD"], capsys=capsys)
    assert again.strip()


def test_renamed_screen_is_not_new(repo, capsys):
    write(repo, "mindsync_app/lib/screens/a/old_screen.dart", lines(5))
    commit(repo, "a")
    run(repo, "mv", "mindsync_app/lib/screens/a/old_screen.dart", "mindsync_app/lib/screens/a/new_screen.dart")
    commit(repo, "rename")
    rc, out = call(repo, stdin=hook_stdin("git commit -m r"), capsys=capsys)
    assert out == ""


def test_assets_listed_as_context(repo, capsys):
    write(repo, "mindsync_app/lib/screens/a/a_screen.dart", lines(5))
    (repo / "mindsync_app" / "assets" / "images").mkdir(parents=True)
    (repo / "mindsync_app" / "assets" / "images" / "hero.png").write_bytes(b"\x89PNG")
    commit(repo, "screen + asset")
    _, out = call(repo, stdin=hook_stdin("git commit -m a"), capsys=capsys)
    assert "assets/images/hero.png" in json.loads(out)["hookSpecificOutput"]["additionalContext"]


def test_errors_never_block(tmp_path, capsys, monkeypatch):
    monkeypatch.setattr(det, "STATE", str(tmp_path / "s.json"))
    rc = det.main(["--repo", str(tmp_path / "nie-ma-repo")], stdin=hook_stdin("git commit -m x"))
    captured = capsys.readouterr()
    assert rc == 0 and captured.out == "" and "blad" in captured.err
    rc = det.main(["--repo", str(tmp_path)], stdin=io.StringIO("to nie jest json"))
    assert rc == 0
    rc = det.main(["--nieznany-argument"], stdin=io.StringIO(""))
    assert rc == 0


def test_commit_detection_variants():
    assert det.czy_hook_commit({"tool_input": {"command": 'git commit -m "x"'}})
    assert det.czy_hook_commit({"tool_input": {"command": "git -C mindsync-frontend commit -am x"}})
    assert det.czy_hook_commit({"tool_input": {"command": "cd a && git add f && git commit -m y"}})
    assert not det.czy_hook_commit({"tool_input": {"command": "git log --grep commit"}})
    assert not det.czy_hook_commit({"tool_input": {"command": "echo commit"}})
    assert not det.czy_hook_commit({})
