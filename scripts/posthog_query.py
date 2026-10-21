#!/usr/bin/env python
"""Generic READ-ONLY PostHog query runner for MindSync (stdlib only, no deps).

Owned by the `posthog-data-extractor` agent. Never mutates anything: the only
HTTP verbs used are POST to the read-only /query/ endpoint and GET for metadata.

Credentials come from MindSync/.env (POSTHOG_HOST, POSTHOG_PERSONAL_API_KEY,
POSTHOG_PROJECT_ID) or from the process environment. Secret values are never
printed.

Usage
-----
  # sanity check credentials + project (prints no secrets)
  python scripts/posthog_query.py --check

  # which events actually flow (optionally filtered by substring)
  python scripts/posthog_query.py --events
  python scripts/posthog_query.py --events paywall

  # property keys seen on an event (last 90d)
  python scripts/posthog_query.py --props subscription_purchase_completed

  # HogQL, inline / from file / from stdin
  python scripts/posthog_query.py --sql "SELECT count() FROM events WHERE timestamp > now() - INTERVAL 7 DAY"
  python scripts/posthog_query.py --sql-file scratch/funnel.sql
  python scripts/posthog_query.py --sql - < scratch/funnel.sql

  # many queries in one round-trip: separate them with a `-- @@ label` line
  python scripts/posthog_query.py --sql-file scratch/batch.sql

  # raw REST metadata (GET only)
  python scripts/posthog_query.py --get /event_definitions/?search=session

Output: aligned text table by default; --format csv|json|tsv; --out FILE to save.
Exit codes: 0 ok, 2 bad usage / blocked query, 3 API or transport error.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.join(REPO_ROOT, "MindSync", ".env")

# Statements that could mutate. The PostHog query API is read-only, but we refuse
# them locally so a bad query never even leaves the machine.
FORBIDDEN = re.compile(
    r"\b(insert|update|delete|drop|truncate|alter|create|grant|revoke|attach|detach|optimize|rename)\b",
    re.IGNORECASE,
)
# Fields that would drag personal data into an output file. Mental-health app:
# aggregate only. We warn loudly rather than silently returning PII.
PII_HINT = re.compile(r"(\$?email|phone|full_?name|first_?name|last_?name|ip_address|\$ip)\b", re.IGNORECASE)


def _stdout_utf8() -> None:
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass


def load_env(name: str) -> str | None:
    """Process env wins; otherwise parse MindSync/.env. Values are never logged."""
    val = os.environ.get(name)
    if val:
        return val.strip().strip('"').strip("'")
    if not os.path.exists(ENV_PATH):
        return None
    with open(ENV_PATH, encoding="utf-8", errors="ignore") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith(name + "="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None


class PostHog:
    def __init__(self, timeout: int = 120):
        self.host = (load_env("POSTHOG_HOST") or "https://eu.i.posthog.com").rstrip("/")
        self.key = load_env("POSTHOG_PERSONAL_API_KEY")
        self.pid = load_env("POSTHOG_PROJECT_ID")
        self.timeout = timeout
        if not self.key or not self.pid:
            die(
                "Missing POSTHOG_PERSONAL_API_KEY and/or POSTHOG_PROJECT_ID "
                f"(looked in the environment and {ENV_PATH}).",
                2,
            )

    # -- transport ---------------------------------------------------------
    def _open(self, req: urllib.request.Request) -> dict:
        req.add_header("Authorization", f"Bearer {self.key}")
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                body = resp.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", errors="replace")[:2000]
            die(f"HTTP {exc.code} from PostHog: {detail}", 3)
        except urllib.error.URLError as exc:
            die(f"Transport error reaching {self.host}: {exc.reason}", 3)
        try:
            return json.loads(body)
        except json.JSONDecodeError:
            die(f"Non-JSON response from PostHog: {body[:500]}", 3)

    def get(self, path: str) -> dict:
        if not path.startswith("/"):
            path = "/" + path
        url = f"{self.host}/api/projects/{self.pid}{path}"
        return self._open(urllib.request.Request(url, method="GET"))

    def get_url(self, url: str) -> dict:
        return self._open(urllib.request.Request(url, method="GET"))

    def hogql(self, sql: str) -> dict:
        sql = sql.strip().rstrip(";")
        if FORBIDDEN.search(sql):
            die("Refused: query contains a mutating statement. This tool is read-only.", 2)
        if PII_HINT.search(sql):
            warn("query references a personal-data field (email/phone/name/ip) – aggregate only, do not persist PII.")
        if "limit" not in sql.lower() and not re.search(r"\b(count|sum|avg|min|max|quantile|uniq|group by)\b", sql, re.I):
            warn("query has no LIMIT and no aggregate – add one to avoid pulling a huge result set.")
        req = urllib.request.Request(
            f"{self.host}/api/projects/{self.pid}/query/",
            data=json.dumps({"query": {"kind": "HogQLQuery", "query": sql}}).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        return self._open(req)

    # -- paging helper -----------------------------------------------------
    def get_all(self, path: str, max_pages: int = 20) -> list[dict]:
        out: list[dict] = []
        page = self.get(path)
        while True:
            out.extend(page.get("results") or [])
            nxt = page.get("next")
            if not nxt or max_pages <= 1:
                break
            max_pages -= 1
            page = self.get_url(nxt)
        return out


def die(msg: str, code: int) -> "NoReturn":  # type: ignore[valid-type]
    print(f"ERROR: {msg}", file=sys.stderr)
    raise SystemExit(code)


def warn(msg: str) -> None:
    print(f"WARNING: {msg}", file=sys.stderr)


# -- rendering -------------------------------------------------------------
def _cell(value, width: int) -> str:
    if value is None:
        text = "(null)"
    elif isinstance(value, (dict, list)):
        text = json.dumps(value, ensure_ascii=False, default=str)
    else:
        text = str(value)
    text = text.replace("\n", " ").replace("\r", " ").replace("\t", " ")
    if width and len(text) > width:
        text = text[: width - 1] + "…"
    return text


def render(columns: list[str], rows: list[list], fmt: str, width: int) -> str:
    if fmt == "json":
        return json.dumps(
            [dict(zip(columns, r)) for r in rows], ensure_ascii=False, indent=2, default=str
        )
    if fmt in ("csv", "tsv"):
        sep = "," if fmt == "csv" else "\t"
        buf = io.StringIO()
        import csv as _csv

        writer = _csv.writer(buf, delimiter=sep, lineterminator="\n")
        writer.writerow(columns)
        for r in rows:
            writer.writerow([_cell(v, 0) for v in r])
        return buf.getvalue().rstrip("\n")
    # table
    cells = [[_cell(v, width) for v in r] for r in rows]
    widths = [len(c) for c in columns]
    for row in cells:
        for i, c in enumerate(row):
            if i < len(widths):
                widths[i] = max(widths[i], len(c))
    line = "  ".join(c.ljust(widths[i]) for i, c in enumerate(columns))
    out = [line, "  ".join("-" * w for w in widths)]
    for row in cells:
        out.append("  ".join(c.ljust(widths[i]) if i < len(widths) else c for i, c in enumerate(row)))
    out.append(f"({len(rows)} row{'s' if len(rows) != 1 else ''})")
    return "\n".join(out)


def result_to_table(res: dict) -> tuple[list[str], list[list]]:
    rows = res.get("results")
    if rows is None:
        rows = res.get("result") or []
    columns = res.get("columns") or []
    if not columns and rows and isinstance(rows[0], dict):
        columns = list(rows[0].keys())
        rows = [[r.get(c) for c in columns] for r in rows]
    if not columns:
        widest = max((len(r) for r in rows if isinstance(r, (list, tuple))), default=0)
        columns = [f"col{i}" for i in range(widest)]
    rows = [list(r) if isinstance(r, (list, tuple)) else [r] for r in rows]
    return [str(c) for c in columns], rows


# -- sql file parsing ------------------------------------------------------
def split_batch(text: str) -> list[tuple[str, str]]:
    """Split a .sql file into (label, query) sections on `-- @@ label` lines."""
    sections: list[tuple[str, str]] = []
    label = "query"
    buf: list[str] = []
    for line in text.splitlines():
        marker = re.match(r"^\s*--\s*@@\s*(.*)$", line)
        if marker:
            if "".join(buf).strip():
                sections.append((label, "\n".join(buf)))
            label = marker.group(1).strip() or f"query{len(sections) + 1}"
            buf = []
        else:
            buf.append(line)
    if "".join(buf).strip():
        sections.append((label, "\n".join(buf)))
    return sections


# -- shortcuts -------------------------------------------------------------
def cmd_check(ph: PostHog) -> str:
    res = ph.hogql("SELECT count() AS events_last_24h FROM events WHERE timestamp > now() - INTERVAL 1 DAY")
    cols, rows = result_to_table(res)
    total = rows[0][0] if rows else "?"
    return (
        f"host={ph.host}\nproject_id={ph.pid}\ncredentials=OK (key loaded, value not shown)\n"
        f"events_last_24h={total}"
    )


def cmd_events(ph: PostHog, needle: str | None) -> tuple[list[str], list[list]]:
    path = "/event_definitions/?limit=500"
    if needle:
        path += "&search=" + urllib.parse.quote(needle)
    defs = ph.get_all(path)
    rows = [
        [d.get("name"), d.get("last_seen_at"), d.get("created_at"), d.get("volume_30_day"), d.get("query_usage_30_day")]
        for d in defs
    ]
    rows.sort(key=lambda r: (r[1] or ""), reverse=True)
    return ["event", "last_seen_at", "created_at", "volume_30d", "queries_30d"], rows


def cmd_props(ph: PostHog, event: str, days: int) -> tuple[list[str], list[list]]:
    safe = event.replace("'", "''")
    res = ph.hogql(
        "SELECT arrayJoin(JSONExtractKeys(toString(properties))) AS prop, count() AS c, "
        f"count(DISTINCT distinct_id) AS users FROM events WHERE event = '{safe}' "
        f"AND timestamp > now() - INTERVAL {int(days)} DAY GROUP BY prop ORDER BY c DESC LIMIT 200"
    )
    return result_to_table(res)


def main(argv: list[str]) -> int:
    _stdout_utf8()
    ap = argparse.ArgumentParser(description="Read-only PostHog query runner (MindSync).")
    src = ap.add_mutually_exclusive_group(required=True)
    src.add_argument("--sql", help="HogQL to run; use '-' to read from stdin")
    src.add_argument("--sql-file", help="file with HogQL; sections split on '-- @@ label' lines")
    src.add_argument("--get", dest="get_path", help="raw GET on /api/projects/{id}<PATH> (metadata only)")
    src.add_argument("--events", nargs="?", const="", help="list event definitions (optional substring filter)")
    src.add_argument("--props", help="property keys seen on EVENT")
    src.add_argument("--check", action="store_true", help="verify credentials + project reachability")
    ap.add_argument("--days", type=int, default=90, help="lookback for --props (default 90)")
    ap.add_argument("--format", choices=["table", "csv", "tsv", "json"], default="table")
    ap.add_argument("--width", type=int, default=48, help="max cell width in table mode (0 = unlimited)")
    ap.add_argument("--timeout", type=int, default=120)
    ap.add_argument("--out", help="also write the rendered output to this file (utf-8)")
    args = ap.parse_args(argv)

    ph = PostHog(timeout=args.timeout)
    chunks: list[str] = []
    failed = 0

    if args.check:
        chunks.append(cmd_check(ph))
    elif args.events is not None:
        cols, rows = cmd_events(ph, args.events or None)
        chunks.append(render(cols, rows, args.format, args.width))
    elif args.props:
        cols, rows = cmd_props(ph, args.props, args.days)
        chunks.append(render(cols, rows, args.format, args.width))
    elif args.get_path:
        payload = ph.get(args.get_path)
        results = payload.get("results")
        if isinstance(results, list) and results and isinstance(results[0], dict):
            cols = sorted({k for r in results for k in r.keys()})
            keep = [c for c in ("name", "id", "last_seen_at", "property_type", "created_at") if c in cols]
            cols = keep or cols
            chunks.append(render(cols, [[r.get(c) for c in cols] for r in results], args.format, args.width))
        else:
            chunks.append(json.dumps(payload, ensure_ascii=False, indent=2, default=str))
    else:
        if args.sql:
            text = sys.stdin.read() if args.sql == "-" else args.sql
            sections = [("query", text)]
        else:
            with open(args.sql_file, encoding="utf-8") as fh:
                sections = split_batch(fh.read())
        if not sections:
            die("no query found", 2)
        for label, sql in sections:
            if not sql.strip():
                continue
            header = f"=== {label} " + "=" * max(0, 66 - len(label))
            try:
                res = ph.hogql(sql)
            except SystemExit as exc:
                # Keep going: one slow/invalid section must not discard the
                # results of the other sections (the ERROR is on stderr).
                if len(sections) == 1:
                    raise
                failed += 1
                chunks.append(header + f"\n(section failed, exit {exc.code}; see ERROR on stderr)")
                continue
            cols, rows = result_to_table(res)
            chunks.append(header + "\n" + render(cols, rows, args.format, args.width))

    output = "\n\n".join(chunks)
    print(output)
    if args.out:
        os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
        with open(args.out, "w", encoding="utf-8") as fh:
            fh.write(output + "\n")
        print(f"\n[written to {args.out}]", file=sys.stderr)
    if failed:
        print(f"WARNING: {failed} section(s) failed; partial results above.", file=sys.stderr)
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
