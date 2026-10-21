#!/usr/bin/env python3
"""Palo Alto AI Runtime Security (AIRS) audit for the current project.

Collects uncommitted file changes and the most recent Claude Code transcript,
then submits each unit to the AIRS SaaS sync scan endpoint.

Stdlib only. Invoked by the `airs-audit` skill.
"""
from __future__ import annotations

import argparse
import fnmatch
import json
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
import uuid
from dataclasses import dataclass, field
from pathlib import Path, PurePosixPath
from typing import Iterable

AIRS_ENDPOINT = "https://service.api.aisecurity.paloaltonetworks.com/v1/scan/sync/request"
AIRS_CONTENT_MAX_BYTES = 2_000_000  # per AIRS spec, single string <=2MB
DEFAULT_MAX_FILE_BYTES = 100_000
DEFAULT_MAX_TURNS = 20
REQUEST_TIMEOUT_S = 60
MAX_UNTRACKED_DIR_FILES = 50   # expansion cap per untracked directory
MAX_TOTAL_UNITS = 200          # total scan units per audit

# Never send these to an external vendor. Glob patterns, matched against the
# relative repo path using POSIX separators. Users can extend via
# `.claude/skills/airs-audit/ignore.txt` (one glob per line).
DEFAULT_DENYLIST = [
    ".env", ".env.*", "**/.env", "**/.env.*",
    "**/*.pem", "**/*.key", "**/*.p12", "**/*.pfx", "**/*.keystore", "**/*.jks",
    "**/service-account*.json", "**/firebase-adminsdk*.json",
    "**/google-services.json", "**/GoogleService-Info.plist",
    "**/credentials*.json", "**/client_secret*.json",
    "**/.aws/**", "**/.ssh/**", "secrets/**", "**/secrets/**",
    "**/*.ppk", "**/*.rsa", "**/*.dsa", "**/*.ecdsa", "**/*.ed25519",
]


@dataclass
class ScanUnit:
    """One thing to send to AIRS. prompt is mandatory, response optional."""
    label: str
    prompt: str
    response: str = ""


@dataclass
class ScanResult:
    label: str
    ok: bool
    action: str = ""
    category: str = ""
    report_id: str = ""
    scan_id: str = ""
    prompt_detected: dict = field(default_factory=dict)
    response_detected: dict = field(default_factory=dict)
    error: str = ""


# ---------- context collection ----------

def _run(cmd: list[str]) -> tuple[int, str, str]:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return p.returncode, p.stdout, p.stderr
    except (subprocess.TimeoutExpired, FileNotFoundError) as e:
        return 1, "", str(e)


def _load_denylist() -> list[str]:
    patterns = list(DEFAULT_DENYLIST)
    extra = Path(".claude/skills/airs-audit/ignore.txt")
    if extra.is_file():
        for line in extra.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                patterns.append(line)
    return patterns


def _is_denied(rel_path: str, patterns: list[str]) -> bool:
    # Normalize to POSIX-style and lowercase for platform-independent, case-insensitive matching.
    posix = str(PurePosixPath(*Path(rel_path).parts)).lower()
    for pat in patterns:
        pat_low = pat.lower()
        if fnmatch.fnmatchcase(posix, pat_low):
            return True
        if fnmatch.fnmatchcase(posix, pat_low.lstrip("*/")):  # allow bare "pattern"
            return True
    return False


def collect_uncommitted_files(max_bytes: int) -> tuple[list[ScanUnit], list[str], bool]:
    """Return (units, skipped_secret_paths, cap_hit).

    cap_hit is True when the global MAX_TOTAL_UNITS cap truncated the scan —
    callers MUST propagate this into the report so users don't get a false
    all-clear from a partial scan."""
    rc, _, _ = _run(["git", "rev-parse", "--git-dir"])
    if rc != 0:
        return [], [], False

    units: list[ScanUnit] = []
    skipped: list[str] = []
    denylist = _load_denylist()

    # Modified + staged: use `git diff HEAD -- <file>` so we get full patch context.
    # Default untracked-mode (no -uall): collapses untracked directories to one entry.
    rc, porcelain, _ = _run(["git", "status", "--porcelain"])
    if rc != 0:
        return [], [], False

    cap_hit = False
    for line in porcelain.splitlines():
        if not line.strip():
            continue
        if len(units) >= MAX_TOTAL_UNITS:
            cap_hit = True
            break
        status, _, path = line[:2], line[2], line[3:].strip()
        # Handle rename: "R  old -> new"
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path = path.strip('"')

        if _is_denied(path, denylist):
            skipped.append(path)
            continue

        if "?" in status:
            # Untracked. Could be a file or a collapsed directory (ending "/").
            if path.endswith("/") or Path(path).is_dir():
                # Expand the directory via git (honors .gitignore), then re-check denylist per file.
                rc2, listing, _ = _run(["git", "ls-files", "--others", "--exclude-standard", "--", path])
                if rc2 != 0:
                    continue
                sub_files = [s.strip().strip('"') for s in listing.splitlines() if s.strip()]
                if len(sub_files) > MAX_UNTRACKED_DIR_FILES:
                    print(
                        f"[airs-audit] Untracked dir {path!r} has {len(sub_files)} files — "
                        f"capped at {MAX_UNTRACKED_DIR_FILES}. Add it to .gitignore or narrow the audit.",
                        file=sys.stderr,
                    )
                    sub_files = sub_files[:MAX_UNTRACKED_DIR_FILES]
                for sub in sub_files:
                    if len(units) >= MAX_TOTAL_UNITS:
                        break
                    if _is_denied(sub, denylist):
                        skipped.append(sub)
                        continue
                    content = _read_file_truncated(sub, max_bytes)
                    if content is None:
                        continue
                    units.append(ScanUnit(label=f"untracked:{sub}", prompt=content))
                continue
            content = _read_file_truncated(path, max_bytes)
            if content is None:
                continue
            units.append(ScanUnit(label=f"untracked:{path}", prompt=content))
        else:
            # Tracked: send diff (captures both intent and new content).
            rc, diff, _ = _run(["git", "diff", "HEAD", "--", path])
            if rc != 0 or not diff.strip():
                continue
            if len(diff.encode("utf-8", errors="replace")) > max_bytes:
                diff = diff.encode("utf-8", errors="replace")[:max_bytes].decode("utf-8", errors="replace")
                diff += "\n\n[...truncated by airs-audit...]"
            units.append(ScanUnit(label=f"diff:{path}", prompt=diff))

    if cap_hit:
        print(
            f"[airs-audit] Reached global cap of {MAX_TOTAL_UNITS} scan units — "
            f"remaining files skipped. Commit or stash some files, add large untracked "
            f"dirs to .gitignore, or raise MAX_TOTAL_UNITS in the script.",
            file=sys.stderr,
        )

    return units, skipped, cap_hit


def _read_file_truncated(path: str, max_bytes: int) -> str | None:
    try:
        p = Path(path)
        if not p.is_file():
            return None
        raw = p.read_bytes()
    except OSError:
        return None
    if b"\x00" in raw[:8192]:
        # Binary heuristic — still include a header so AIRS sees the filename.
        return f"[binary file {path}, {len(raw)} bytes, not sent]"
    truncated = raw[:max_bytes]
    text = truncated.decode("utf-8", errors="replace")
    if len(raw) > max_bytes:
        text += "\n\n[...truncated by airs-audit...]"
    return text


def _project_transcript_dir() -> Path:
    """Claude Code encodes cwd as a slug: each `:`, `\\`, or `/` becomes `-`.
    Do NOT collapse runs — on Windows `C:\\Users` intentionally becomes `C--Users`."""
    cwd = os.getcwd()
    slug = re.sub(r"[:\\/]", "-", cwd)
    return Path.home() / ".claude" / "projects" / slug


def find_latest_transcript() -> Path | None:
    d = _project_transcript_dir()
    if not d.is_dir():
        return None
    candidates = sorted(d.glob("*.jsonl"), key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0] if candidates else None


_INJECTED_TAGS_RE = re.compile(
    r"<(system-reminder|command-name|command-message|command-args|local-command-stdout|local-command-stderr)\b[^>]*>.*?</\1>",
    re.DOTALL | re.IGNORECASE,
)


_LEFTOVER_INJECTED_MARKERS = (
    "<system-reminder", "</system-reminder",
    "<command-name", "<command-message", "<command-args",
    "<local-command-stdout", "<local-command-stderr",
)


def _strip_injected_context(text: str) -> str:
    """Remove system-reminder / command-* blocks that Claude Code injects
    into the user turn. These are NOT user-authored and must not be shipped
    to an external vendor.

    Two passes: (1) regex strip of well-formed tag pairs; (2) if any injected
    marker still appears (malformed / unclosed), drop the whole turn as a
    belt-and-suspenders guard (returns empty string)."""
    cleaned = _INJECTED_TAGS_RE.sub("", text).strip()
    lowered = cleaned.lower()
    if any(m in lowered for m in _LEFTOVER_INJECTED_MARKERS):
        return ""
    return cleaned


def extract_conversation(transcript: Path, max_turns: int, current_session: str | None) -> ScanUnit | None:
    """Extract user + assistant text content, skipping tools/thinking/injected context."""
    user_texts: list[str] = []
    assistant_texts: list[str] = []
    try:
        with transcript.open(encoding="utf-8") as f:
            for line in f:
                try:
                    obj = json.loads(line)
                except json.JSONDecodeError:
                    continue
                t = obj.get("type")
                msg = obj.get("message") or {}
                content = msg.get("content") if isinstance(msg, dict) else None

                if t == "user":
                    text = _user_content_to_text(content)
                    text = _strip_injected_context(text)
                    if text:
                        user_texts.append(text)
                elif t == "assistant":
                    text = _assistant_content_to_text(content)
                    if text:
                        assistant_texts.append(text)
    except OSError as e:
        return ScanUnit(label="conversation", prompt=f"[failed to read transcript: {e}]")

    # Trim to last N turns of each side.
    user_tail = user_texts[-max_turns:]
    assistant_tail = assistant_texts[-max_turns:]
    if not user_tail and not assistant_tail:
        return None

    prompt = "\n\n---\n\n".join(user_tail) if user_tail else ""
    response = "\n\n---\n\n".join(assistant_tail) if assistant_tail else ""
    label = f"conversation:{transcript.name}"
    if current_session and current_session in transcript.name:
        label += " (current)"

    return ScanUnit(label=label, prompt=prompt, response=response)


def _user_content_to_text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts = []
        for item in content:
            if isinstance(item, dict) and item.get("type") == "text":
                parts.append(str(item.get("text", "")))
            elif isinstance(item, dict) and item.get("type") == "tool_result":
                # Skip tool results — they're noise and bloat.
                continue
        return "\n".join(p for p in parts if p)
    return ""


def _assistant_content_to_text(content) -> str:
    if not isinstance(content, list):
        return ""
    parts = []
    for item in content:
        if isinstance(item, dict) and item.get("type") == "text":
            parts.append(str(item.get("text", "")))
        # Skip thinking, tool_use — scan only what the user would see.
    return "\n".join(p for p in parts if p)


# ---------- AIRS client ----------

def airs_scan(unit: ScanUnit, api_key: str, profile_name: str, app_user: str) -> ScanResult:
    prompt = _cap(unit.prompt, AIRS_CONTENT_MAX_BYTES)
    response = _cap(unit.response, AIRS_CONTENT_MAX_BYTES)
    if not prompt and not response:
        return ScanResult(label=unit.label, ok=False, error="empty content")

    body = {
        "tr_id": str(uuid.uuid4()),
        "ai_profile": {"profile_name": profile_name},
        "metadata": {
            "app_user": app_user,
            "ai_model": "claude-code",
            "app_name": "airs-audit-skill",
        },
        "contents": [{"prompt": prompt, "response": response}],
    }

    req = urllib.request.Request(
        AIRS_ENDPOINT,
        data=json.dumps(body).encode("utf-8"),
        headers={
            "Content-Type": "application/json",
            "x-pan-token": api_key,
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT_S) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_txt = e.read().decode("utf-8", errors="replace")[:500]
        return ScanResult(label=unit.label, ok=False, error=f"HTTP {e.code}: {body_txt}")
    except urllib.error.URLError as e:
        return ScanResult(label=unit.label, ok=False, error=f"URL error: {e.reason}")
    except (TimeoutError, json.JSONDecodeError) as e:
        return ScanResult(label=unit.label, ok=False, error=f"{type(e).__name__}: {e}")

    return ScanResult(
        label=unit.label,
        ok=True,
        action=payload.get("action", ""),
        category=payload.get("category", ""),
        report_id=payload.get("report_id", ""),
        scan_id=payload.get("scan_id", ""),
        prompt_detected=payload.get("prompt_detected") or {},
        response_detected=payload.get("response_detected") or {},
    )


def _cap(s: str, limit: int) -> str:
    if not s:
        return ""
    b = s.encode("utf-8", errors="replace")
    if len(b) <= limit:
        return s
    return b[:limit].decode("utf-8", errors="replace") + "\n[...truncated...]"


# ---------- reporting ----------

def format_human(results: Iterable[ScanResult], profile: str, meta: dict) -> str:
    lines = ["Palo Alto AIRS audit", f"  profile: {profile}", f"  scanned: {meta.get('unit_count', 0)} unit(s)"]
    if meta.get("files_count") is not None:
        lines.append(f"  uncommitted files: {meta['files_count']}")
    if meta.get("conversation_source"):
        lines.append(f"  conversation:       {meta['conversation_source']}")
    if meta.get("truncated"):
        lines.append("  WARNING: scan was TRUNCATED by unit cap — results are incomplete.")
    lines.append("")

    blocked = 0
    errored = 0
    for r in results:
        if not r.ok:
            errored += 1
            lines.append(f"  [ERROR] {r.label}: {r.error}")
            continue
        verdict = r.action.upper() or "?"
        flag = "BLOCK" if r.action == "block" else "allow"
        if r.action == "block":
            blocked += 1
        detectors = _summarize_detectors(r.prompt_detected, r.response_detected)
        det_str = f" — {detectors}" if detectors else ""
        lines.append(f"  [{flag}] {r.label} (category={r.category or '?'}){det_str}")
        if r.action == "block":
            lines.append(f"           report_id={r.report_id}")

    lines.append("")
    lines.append(f"Summary: {blocked} blocked, {errored} errored, {meta.get('unit_count', 0) - blocked - errored} allowed.")
    return "\n".join(lines)


def _summarize_detectors(prompt_det: dict, response_det: dict) -> str:
    triggered = []
    for side, det in (("prompt", prompt_det), ("response", response_det)):
        for k, v in det.items():
            if v:
                triggered.append(f"{side}.{k}")
    return ", ".join(triggered)


# ---------- main ----------

def _confirm(prompt: str, auto_yes: bool) -> bool:
    if auto_yes:
        return True
    if not sys.stdin.isatty():
        # Non-interactive: if running under Claude Code (which sets CLAUDECODE=1),
        # assume Claude has already obtained the user's consent in-chat before
        # invoking this script with --yes. If CLAUDECODE isn't set and --yes
        # wasn't passed, fail safe.
        print(f"{prompt} [aborting — pass --yes for non-interactive]", file=sys.stderr)
        return False
    try:
        answer = input(f"{prompt} [y/N] ").strip().lower()
    except EOFError:
        return False
    return answer in ("y", "yes")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--no-conversation", action="store_true")
    parser.add_argument("--no-files", action="store_true")
    parser.add_argument("--max-turns", type=int, default=DEFAULT_MAX_TURNS)
    parser.add_argument("--max-file-bytes", type=int, default=DEFAULT_MAX_FILE_BYTES)
    parser.add_argument("--transcript", type=str, default=None)
    parser.add_argument("--json", action="store_true", help="emit full JSON report on stdout")
    parser.add_argument("--save", action="store_true", help="save JSON report to .claude/airs-reports/")
    parser.add_argument("--yes", action="store_true", help="skip interactive confirmations (CI use)")
    args = parser.parse_args(argv)

    api_key = os.environ.get("PANW_AIRS_API_KEY", "").strip()
    profile = os.environ.get("PANW_AIRS_PROFILE_NAME", "").strip()
    if not api_key or not profile:
        print("CREDENTIALS MISSING: export PANW_AIRS_API_KEY and PANW_AIRS_PROFILE_NAME.", file=sys.stderr)
        return 2

    app_user = os.environ.get("USER") or os.environ.get("USERNAME") or "claude-code"

    units: list[ScanUnit] = []
    meta: dict = {}
    skipped_secrets: list[str] = []

    if not args.no_files:
        file_units, skipped_secrets, cap_hit = collect_uncommitted_files(args.max_file_bytes)
        units.extend(file_units)
        meta["files_count"] = len(file_units)
        meta["skipped_secrets"] = skipped_secrets
        meta["truncated"] = cap_hit

    if skipped_secrets:
        print(f"[airs-audit] Skipped {len(skipped_secrets)} file(s) matching the secrets denylist:", file=sys.stderr)
        for p in skipped_secrets[:20]:
            print(f"  - {p}", file=sys.stderr)
        if len(skipped_secrets) > 20:
            print(f"  ...and {len(skipped_secrets) - 20} more.", file=sys.stderr)
        print("  (if any of these are supposed to be public, extend .claude/skills/airs-audit/ignore.txt)", file=sys.stderr)

    if not args.no_conversation:
        transcript = Path(args.transcript) if args.transcript else find_latest_transcript()
        if transcript and transcript.is_file():
            size_kb = transcript.stat().st_size // 1024
            ok = _confirm(
                f"[airs-audit] Send conversation transcript {transcript.name} (~{size_kb} KB, last {args.max_turns} turns) to Palo Alto?",
                args.yes,
            )
            if not ok:
                meta["conversation_source"] = "(skipped by user)"
            else:
                current_session = os.environ.get("CLAUDE_SESSION_ID")
                conv = extract_conversation(transcript, args.max_turns, current_session)
                if conv:
                    units.append(conv)
                    meta["conversation_source"] = str(transcript)
                else:
                    meta["conversation_source"] = "(no user/assistant turns extracted)"
        else:
            meta["conversation_source"] = "(none found)"
            print(
                f"[airs-audit] No transcript found in {_project_transcript_dir()} — "
                f"conversation scan skipped.",
                file=sys.stderr,
            )

    meta["unit_count"] = len(units)

    if not units:
        print("Nothing to scan (no uncommitted files, no transcript).", file=sys.stderr)
        return 4  # HIGH-04: distinct code for empty scan

    results = [airs_scan(u, api_key, profile, app_user) for u in units]

    if args.save:
        out_dir = Path(".claude/airs-reports")
        out_dir.mkdir(parents=True, exist_ok=True)
        gi = out_dir / ".gitignore"
        if not gi.exists():
            gi.write_text("*\n!.gitignore\n", encoding="utf-8")
        out_path = out_dir / f"{time.strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:8]}.json"
        out_path.write_text(json.dumps({
            "profile": profile,
            "meta": meta,
            "results": [r.__dict__ for r in results],
        }, indent=2), encoding="utf-8")
        print(f"Report saved: {out_path}", file=sys.stderr)

    if args.json:
        print(json.dumps({
            "profile": profile,
            "meta": meta,
            "results": [r.__dict__ for r in results],
        }, indent=2))
    else:
        print(format_human(results, profile, meta))

    blocked = any(r.ok and r.action == "block" for r in results)
    all_errored = results and all(not r.ok for r in results)
    if blocked:
        return 1
    if all_errored:
        return 3
    if meta.get("truncated"):
        # Don't let a truncated scan be mistaken for a clean pass in CI / --json / --save.
        return 5
    return 0


if __name__ == "__main__":
    sys.exit(main())
