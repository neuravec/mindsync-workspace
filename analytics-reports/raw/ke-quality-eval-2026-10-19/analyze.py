"""Review view of the 2026-10-19 KE gate run: entries -> moments -> final map, extra text checks, cost."""

import json
import re
import sys
from pathlib import Path

OUT = Path(__file__).resolve().parent
FIX = Path(r"C:/Users/mikol/Notebooks/MindSync/Heroku/MindSync-wt-integration-v3-final/app/tests/fixtures/ke_synthetic_stories.json")
PRICE = {"prompt": 0.75, "cached": 0.075, "completion": 4.50}
DASHES = ("\u2014", "\u2013")
RISKY = re.compile(
    r"\b(panic\w*|anxi\w*|depress\w*|medic\w*|pills?|dose|weight|food|eat\w*|body image|disorder|diagnos\w*|"
    r"beat(ing)?|fix(ing)?|cure|die|suicid\w*|safety plan|psychiatr\w*|tom|anna|kasia|overreact\w*|useless|fraud|"
    r"trauma|accident|grief|death|died)\b",
    re.I,
)

stories = {s["id"]: s for s in json.loads(FIX.read_text(encoding="utf-8"))["stories"]}
files = sys.argv[1:] or ["chunk1.json", "chunk2.json", "chunk3.json", "chunk4.json"]
results = []
for f in files:
    results += json.loads((OUT / f).read_text(encoding="utf-8"))


def cost(u):
    return ((u["prompt"] - u["cached"]) * PRICE["prompt"] + u["cached"] * PRICE["cached"] + u["completion"] * PRICE["completion"]) / 1e6


tot = {"calls": 0, "prompt": 0, "cached": 0, "completion": 0}
for r in results:
    sid = r["id"]
    st = stories[sid]
    print("=" * 110)
    print(f"{sid} [{r['language']}] {r['theme']} | expect {r['expect']}")
    by_day = {}
    for m in r["moments"]:
        by_day.setdefault(m["days_ago"], []).append(m)
    for e in sorted(st["entries"], key=lambda e: -e["days_ago"]):
        print(f"  ENTRY d-{e['days_ago']} {e['kind']}: {e['text']}")
        for m in by_day.get(e["days_ago"], []):
            if m["source_kind"] == "after_therapy" and e["kind"] != "after_therapy" and any(x["kind"] == "after_therapy" for x in st["entries"] if x["days_ago"] == e["days_ago"]):
                pass
            print(f"      -> [{m['family']}/{m['kind']}/{m['anchor']}] c{m['confidence']} hs={m['hard_situation']} s={m['strengths']} :: {m['text']}")
    fm = r["checkpoints"][-1]["map"]
    for i, cp in enumerate(r["checkpoints"]):
        mp = cp["map"]
        print(f"  CP{i} {cp['now']}: lvl {mp['level']} steps {mp['steps']} support_row {mp['support_row']} "
              f"ideas {mp.get('idea_count')} pending {mp.get('pending_stages')} jobs {[ (j.get('status'), j.get('compose')) for j in cp['jobs']]}")
        for p in mp["paths"]:
            print(f"     PATH [{p['family']}] {p['name']} | focus: {p['focus']}")
            for s in p["skills"]:
                print(f"        skill {s}")
            for h in p["hard"]:
                print(f"        hard {h}")
        if mp["forming"]:
            print(f"     forming {mp['forming']}")
        for t in mp["tools"]:
            print(f"     tool {t}")
        for idea in mp["ideas"]:
            print(f"     idea {idea}")
        for pr in cp["problems"]:
            print(f"     !! {pr}")
    for s in r["skills_full"]:
        print(f"  WORDS s{s['id']} {s['name']}: {s['in_your_words']}")
    for t in r["tools_full"]:
        print(f"  TOOL {t}")
    for h in r["hard_full"]:
        print(f"  HARD {h}")
    for i in r["ideas_full"]:
        print(f"  IDEA {i}")
    print(f"  stability {r['stability']}  state {r['state']}")
    texts = [m["text"] for m in r["moments"]] + [s["name"] for s in r["skills_full"]] + [s["in_your_words"] or "" for s in r["skills_full"]]
    texts += [p["name"] for p in r["paths_full"]] + [p["focus"] or "" for p in r["paths_full"]]
    texts += [t["name"] for t in r["tools_full"]] + [t["what"] or "" for t in r["tools_full"]] + [t["origin_note"] or "" for t in r["tools_full"]]
    texts += [h["label"] for h in r["hard_full"]] + [h["context"] or "" for h in r["hard_full"]]
    texts += [i["text"] for i in r["ideas_full"]] + [i["why"] or "" for i in r["ideas_full"]]
    flags = sorted({f"{m.group(0)!r} in: {t}" for t in texts for m in RISKY.finditer(t)})
    flags += [f"DASH in: {t}" for t in texts if any(d in t for d in DASHES)]
    for fl in flags:
        print(f"  ?? {fl}")
    u = r["usage_split"]["total"]
    for k in tot:
        tot[k] += u[k]
    print(f"  usage {u}")

print("=" * 110)
print("TOTAL", tot, f"usd={cost(tot):.4f}", f"per story={cost(tot)/len(results):.5f}", f"stories={len(results)}")
