---
name: airs-audit
description: Run a Palo Alto AI Runtime Security (AIRS) audit on the current project. Collects uncommitted file changes and the latest conversation transcript with the agent, then submits them to the AIRS sync scan API. Use when the user says "airs audit", "palo alto audit", "security scan" in the context of Palo Alto, "scan my changes", or "/airs-audit".
---

# AIRS Audit

Runs a security audit using Palo Alto AI Runtime Security (AIRS) SaaS `/v1/scan/sync/request` endpoint against:
1. **Uncommitted files** — anything `git diff HEAD` + untracked files would show.
2. **Conversation context** — the most recent Claude Code transcript for this project (`~/.claude/projects/<project-slug>/*.jsonl`).

## Prerequisites

The user must have these environment variables exported:

- `PANW_AIRS_API_KEY` — Palo Alto AIRS API token (sent as `x-pan-token` header).
- `PANW_AIRS_PROFILE_NAME` — AI security profile configured in Strata Cloud Manager.

If either is missing, stop and tell the user:

```
Missing AIRS credentials. Export:
  export PANW_AIRS_API_KEY=...
  export PANW_AIRS_PROFILE_NAME=...
```

## How to invoke

**Step 1 — get explicit user consent in-chat before running.** Tell the user:
- which uncommitted files will be included (list them from `git status --porcelain`),
- that the latest Claude Code transcript for this project will be concatenated and sent,
- that files matching the secrets denylist (`.env*`, Firebase creds, ssh keys, etc.) will be automatically skipped,
- the vendor destination (`service.api.aisecurity.paloaltonetworks.com`).

Then ask: *"Run the Palo Alto AIRS audit on these? (y/n)"* and wait for yes.

**Step 2 — run with `--yes`.** Because the script is invoked via the Bash tool (stdin is not a TTY), it requires `--yes` to proceed with the conversation scan; the in-chat confirmation above is the consent gate.

```bash
python .claude/skills/airs-audit/scripts/airs_audit.py --yes
```

Optional flags:

- `--no-conversation` — skip transcript scan, only scan uncommitted files.
- `--no-files` — skip file scan, only scan conversation.
- `--max-turns N` — limit transcript to last N user+assistant turns (default: 20).
- `--max-file-bytes N` — truncate each file diff to N bytes (default: 100000).
- `--transcript PATH` — use a specific `.jsonl` transcript instead of the latest.
- `--json` — emit full JSON report on stdout instead of the human summary.
- `--save` — persist the full JSON report under `.claude/airs-reports/<timestamp>.json` (auto-writes `.gitignore` so reports are never committed).

The script prints a per-scan verdict (`allow`/`block`), lists triggered detectors (injection, DLP, toxic content, malicious code, URL categories, etc.). Exit codes: `0`=all allow, `1`=at least one block, `2`=creds missing, `3`=all scans errored, `4`=nothing to scan, `5`=scan was truncated by the unit cap (results incomplete — re-run on a narrower changeset).

Extend the secrets denylist per-repo by creating `.claude/skills/airs-audit/ignore.txt` (one glob per line, `#` for comments).

## After running

1. If the script prints `CREDENTIALS MISSING`, ask the user to export the env vars and stop.
2. If any scan returns `action: block`, surface the finding to the user with:
   - which file / which turn triggered it,
   - which detector(s) fired (from `prompt_detected` / `response_detected`),
   - the AIRS `report_id` so they can look up details in the PANW console.
3. If all scans return `allow`, report the number of scanned units (files + conversation turns) and the profile name.
4. Never modify code, tests, or configuration as part of this skill — it is a read-only audit. If the user wants fixes applied, they will ask in a follow-up turn and you will delegate to the appropriate domain agent (`backend-api`, `data-analytics`, `flutter-mobile`, or `security-guardian` for deeper review).

## Notes

- Uses only the Python standard library (`urllib`, `json`, `subprocess`) — no `pip install` needed.
- Binary files and files larger than `--max-file-bytes` are truncated, not skipped entirely, so the user knows they were partially covered.
- The script respects AIRS payload limits by sending one scan request per file and one for the conversation chunk.
- Transcript extraction pulls only `message.content` text from `type: user` and `type: assistant` records, skipping tool uses, attachments, system reminders, and thinking blocks (those are noise for AIRS).
