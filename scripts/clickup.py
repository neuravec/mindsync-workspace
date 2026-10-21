#!/usr/bin/env python3
"""ClickUp runner for MindSync's ticket-agent (stdlib only, no dependencies).

Reads the API token from Heroku/.env (CLICKUP_API) and never prints it.

Read:
    python scripts/clickup.py --check
    python scripts/clickup.py --spaces
    python scripts/clickup.py --lists <space_id>
    python scripts/clickup.py --tasks <list_id> [--status Open] [--include-closed]
    python scripts/clickup.py --task <task_id>
    python scripts/clickup.py --tree <task_id> [--full]
    python scripts/clickup.py --comments <task_id>

Write (all mutations honour --dry-run):
    python scripts/clickup.py --set-desc <task_id> --file body.md
    python scripts/clickup.py --set-name <task_id> --name "New title"
    python scripts/clickup.py --create --list <list_id> --name "Title" [--parent <task_id>] [--file body.md]
    python scripts/clickup.py --comment <task_id> --file note.md
    python scripts/clickup.py --set-status <task_id> --status "in progress"
    python scripts/clickup.py --bulk-desc <file>      # multi-section: `=====<task_id>=====` per block

Descriptions are always sent as `markdown_content` so ClickUp renders real
markdown. Sending them via the plain `description` field stores escaped
literals (\\## instead of ##) and looks broken.

Deletion is deliberately not implemented. Nothing here removes a task.
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request

API = "https://api.clickup.com/api/v2"
ENV_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")

# MindSync workspace constants (verified 2026-08-11)
TEAM_ID = "9015587939"
LIST_FEATURES = "901504408777"


def token():
    """Read CLICKUP_API from Heroku/.env. Never printed, only returned."""
    path = os.environ.get("CLICKUP_ENV_PATH", ENV_PATH)
    try:
        with open(path, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip()
                if line.startswith("CLICKUP_API") and "=" in line:
                    val = line.split("=", 1)[1].strip().strip('"').strip("'")
                    if val:
                        return val
    except OSError as exc:
        sys.exit(f"cannot read {path}: {exc}")
    sys.exit(f"CLICKUP_API not found in {path}")


def call(method, path, payload=None, quiet=False):
    req = urllib.request.Request(
        API + path,
        data=json.dumps(payload).encode("utf-8") if payload is not None else None,
        headers={"Authorization": token(), "Content-Type": "application/json"},
        method=method,
    )
    try:
        with urllib.request.urlopen(req) as resp:
            body = resp.read().decode("utf-8")
            return json.loads(body) if body else {}
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[:500]
        if quiet:
            return {"_error": exc.code, "_detail": detail}
        sys.exit(f"HTTP {exc.code} on {method} {path}\n{detail}")


def out(text=""):
    """Print without dying on a legacy console codepage."""
    enc = sys.stdout.encoding or "utf-8"
    sys.stdout.write(str(text).encode(enc, "replace").decode(enc) + "\n")


def read_body(args):
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            return fh.read().strip()
    if args.text:
        return args.text
    return None


def get_task(task_id, subtasks=False):
    q = "?include_markdown_description=true"
    if subtasks:
        q += "&include_subtasks=true"
    return call("GET", f"/task/{task_id}{q}")


def desc_of(task):
    return task.get("markdown_description") or task.get("description") or ""


def show_task(task, full=False, indent=""):
    out(f"{indent}ID:     {task.get('id')}")
    out(f"{indent}NAME:   {task.get('name')}")
    out(f"{indent}STATUS: {(task.get('status') or {}).get('status')}")
    out(f"{indent}URL:    {task.get('url')}")
    body = desc_of(task)
    out(f"{indent}DESC ({len(body)} chars):")
    out(body if full else body[:1200] + ("\n[...]" if len(body) > 1200 else ""))


def mutate(method, path, payload, dry_run, label):
    if dry_run:
        out(f"DRY-RUN {method} {path}")
        out(json.dumps(payload, ensure_ascii=False)[:600])
        return None
    res = call(method, path, payload)
    out(f"OK {label}")
    return res


def main():
    p = argparse.ArgumentParser(description="ClickUp read/write runner for ticket-agent")
    # read
    p.add_argument("--check", action="store_true", help="verify credentials + workspace reachability")
    p.add_argument("--spaces", action="store_true")
    p.add_argument("--lists", metavar="SPACE_ID")
    p.add_argument("--tasks", metavar="LIST_ID")
    p.add_argument("--task", metavar="TASK_ID")
    p.add_argument("--tree", metavar="TASK_ID", help="task + every subtask description")
    p.add_argument("--comments", metavar="TASK_ID")
    p.add_argument("--full", action="store_true", help="do not truncate descriptions")
    p.add_argument("--status", metavar="STATUS", help="filter (--tasks) or new value (--set-status)")
    p.add_argument("--include-closed", action="store_true")
    # write
    p.add_argument("--set-desc", metavar="TASK_ID")
    p.add_argument("--set-name", metavar="TASK_ID")
    p.add_argument("--set-status", metavar="TASK_ID")
    p.add_argument("--create", action="store_true")
    p.add_argument("--comment", metavar="TASK_ID")
    p.add_argument("--bulk-desc", metavar="FILE")
    p.add_argument("--list", metavar="LIST_ID", dest="list_id", default=LIST_FEATURES)
    p.add_argument("--parent", metavar="TASK_ID")
    p.add_argument("--name")
    p.add_argument("--file")
    p.add_argument("--text")
    p.add_argument("--dry-run", action="store_true")
    args = p.parse_args()

    if args.check:
        user = call("GET", "/user").get("user", {})
        out(f"authenticated as: {user.get('username')} <{user.get('email')}>")
        # NOTE: GET /team (list all workspaces) returns 404 SHARD_006 for this
        # token. Everything scoped under /team/{TEAM_ID}/... works fine, so the
        # workspace id is hard-coded above rather than discovered.
        for s in call("GET", f"/team/{TEAM_ID}/space").get("spaces", []):
            out(f"space: {s.get('name')} (id {s.get('id')})")
        out(f"default list for new tickets: Features ({LIST_FEATURES})")
        return

    if args.spaces:
        for s in call("GET", f"/team/{TEAM_ID}/space").get("spaces", []):
            out(f"{s.get('id')}  {s.get('name')}")
        return

    if args.lists:
        for f in call("GET", f"/space/{args.lists}/folder").get("folders", []):
            out(f"folder {f.get('id')}  {f.get('name')}")
            for l in f.get("lists", []):
                out(f"   list {l.get('id')}  {l.get('name')}")
        for l in call("GET", f"/space/{args.lists}/list").get("lists", []):
            out(f"list {l.get('id')}  {l.get('name')}")
        return

    if args.tasks:
        q = "?subtasks=true"
        if args.include_closed:
            q += "&include_closed=true"
        rows = call("GET", f"/list/{args.tasks}/task{q}").get("tasks", [])
        for t in rows:
            st = (t.get("status") or {}).get("status", "")
            if args.status and st.lower() != args.status.lower():
                continue
            parent = f"  (subtask of {t['parent']})" if t.get("parent") else ""
            out(f"{t['id']}  [{st}]  {t.get('name')}{parent}")
        out(f"-- {len(rows)} tasks in list {args.tasks}")
        return

    if args.task:
        show_task(get_task(args.task), full=args.full)
        return

    if args.tree:
        parent = get_task(args.tree, subtasks=True)
        show_task(parent, full=args.full)
        subs = parent.get("subtasks") or []
        out(f"\n===== {len(subs)} subtasks =====")
        for s in subs:
            out("")
            show_task(get_task(s["id"]), full=args.full, indent="  ")
        return

    if args.comments:
        for c in call("GET", f"/task/{args.comments}/comment").get("comments", []):
            who = (c.get("user") or {}).get("username")
            out(f"--- {who} ({c.get('date')})")
            out(c.get("comment_text", ""))
        return

    if args.bulk_desc:
        with open(args.bulk_desc, encoding="utf-8") as fh:
            raw = fh.read()
        parts = re.split(r"^=====([0-9a-zA-Z]+)=====$", raw, flags=re.M)
        items = [(parts[i], parts[i + 1].strip()) for i in range(1, len(parts), 2)]
        if not items:
            sys.exit("no `=====<task_id>=====` sections found")
        for task_id, body in items:
            mutate("PUT", f"/task/{task_id}", {"markdown_content": body},
                   args.dry_run, f"{task_id} ({len(body)} chars)")
        return

    if args.set_desc:
        body = read_body(args)
        if not body:
            sys.exit("--set-desc needs --file (preferred) or --text")
        mutate("PUT", f"/task/{args.set_desc}", {"markdown_content": body},
               args.dry_run, f"description of {args.set_desc} ({len(body)} chars)")
        return

    if args.set_name:
        if not args.name:
            sys.exit("--set-name needs --name")
        mutate("PUT", f"/task/{args.set_name}", {"name": args.name}, args.dry_run, "title")
        return

    if args.set_status:
        if not args.status:
            sys.exit("--set-status needs --status")
        mutate("PUT", f"/task/{args.set_status}", {"status": args.status}, args.dry_run,
               f"status -> {args.status}")
        return

    if args.create:
        if not args.name:
            sys.exit("--create needs --name")
        payload = {"name": args.name}
        body = read_body(args)
        if body:
            payload["markdown_content"] = body
        if args.parent:
            payload["parent"] = args.parent
        res = mutate("POST", f"/list/{args.list_id}/task", payload, args.dry_run, "created")
        if res:
            out(f"   {res.get('id')}  {res.get('url')}")
        return

    if args.comment:
        body = read_body(args)
        if not body:
            sys.exit("--comment needs --file or --text")
        mutate("POST", f"/task/{args.comment}/comment",
               {"comment_text": body, "notify_all": False}, args.dry_run, "comment posted")
        return

    p.print_help()


if __name__ == "__main__":
    main()
