"""Compact review view of a KE gate run: entry -> moments, final map, items, problems.

Usage: python review.py full_it1_c1.json [more.json ...] [--only S05 S26]
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
args = sys.argv[1:]
only = set()
if "--only" in args:
    i = args.index("--only")
    only = set(args[i + 1:])
    args = args[:i]
results = [r for f in args for r in json.loads((HERE / f).read_text(encoding="utf-8"))]
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
for r in results:
    if only and r["id"] not in only:
        continue
    print("=" * 100)
    print(f'{r["id"]} [{r["language"]}] {r["theme"]} | expect {r["expect"].get("families_any")}')
    by = {}
    for m in r["moments"]:
        by.setdefault((m["source_kind"], m["source_id"]), []).append(m)
    for e in r["entries"]:
        print(f'  E d-{e["days_ago"]} {e["kind"]}{" [CRISIS]" if e["crisis"] else ""}: {e["text"]}')
        for m in by.get((e["source_kind"], e["source_id"]), []):
            link = "".join(k[0] for k in ("path_id", "skill_id", "tool_id", "hard_id") if m.get(k))
            print(f'     -> {m["id"]} [{m["family"]}/{m["kind"]}/{m["anchor"]}] {link} :: {m["text"]}')
    for i, cp in enumerate(r["checkpoints"]):
        mp = cp["map"]
        print(f'  CP{i} {cp["now"]} support_row={mp["support_row"]} ideas={len(mp["ideas"])} pending={mp["pending_stages"]} '
              f'forming={mp["forming"]}')
    mp = r["checkpoints"][-1]["map"]
    for p in mp["paths"]:
        print(f'     PATH [{p["family"]}] {p["name"]} | {p["focus"]}')
        for s in p["skills"]:
            print(f'        skill {s}')
        for h in p["hard"]:
            print(f'        hard {h}')
    for t in mp["tools"]:
        print(f'     tool {t}')
    for s in r["skills"]:
        kinds = sorted({m["kind"] for m in r["moments"] if m.get("skill_id") == s["id"]})
        print(f'  WORDS s{s["id"]} {s["name"]} {kinds}: {s["in_your_words"]}')
    for t in r["tools"]:
        print(f'  TOOL t{t["id"]} {t["name"]} [{t["origin"]}]: {t["what"]} | {t["origin_note"]}')
    for h in r["hard"]:
        print(f'  HARD h{h["id"]} {h["label"]} | {h["context"]}')
    for i in r["ideas"]:
        print(f'  IDEA [{i["reason"]}/{i["cta"]}/{i["state"]}] {i["text"]} | why: {i["why"]}')
    print(f'  stability {r["stability"]} usage ${r["usage"].get("usd")}')
    v = r.get("validator") or {}
    if v.get("drops") or v.get("name_hits"):
        print(f'  validator drops {v.get("drops")} name_hits {v.get("name_hits")}')
    for p in r["problems"]:
        print(f'  !! {p}')
