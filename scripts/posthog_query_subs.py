"""Quick PostHog query for subscription-related events. Read-only."""
import os, sys, json, urllib.request, urllib.error

def env(name):
    for line in open(os.path.join(os.path.dirname(__file__), "..", "MindSync", ".env"), encoding="utf-8", errors="ignore"):
        line = line.strip()
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

HOST = env("POSTHOG_HOST")
KEY  = env("POSTHOG_PERSONAL_API_KEY")
PID  = env("POSTHOG_PROJECT_ID")

def q(hog):
    req = urllib.request.Request(
        f"{HOST}/api/projects/{PID}/query/",
        data=json.dumps({"query": {"kind": "HogQLQuery", "query": hog}}).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode(errors="ignore")[:500]}

def get(path):
    req = urllib.request.Request(
        f"{HOST}/api/projects/{PID}{path}",
        headers={"Authorization": f"Bearer {KEY}"},
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        return {"error": e.code, "body": e.read().decode(errors="ignore")[:500]}

def section(title):
    print(f"\n{'='*70}\n{title}\n{'='*70}")

# 1. Which subscription-related events have been seen?
section("1. Subscription-related event definitions (any name with sub/paywall/purchase/promo)")
defs = get("/event_definitions/?search=sub")
defs2 = get("/event_definitions/?search=paywall")
defs3 = get("/event_definitions/?search=purchase")
defs4 = get("/event_definitions/?search=promo")
defs5 = get("/event_definitions/?search=product")
seen = {}
for d in (defs, defs2, defs3, defs4, defs5):
    for r in d.get("results", []) if isinstance(d, dict) else []:
        seen[r["name"]] = r.get("last_seen_at")
for n, ls in sorted(seen.items()):
    print(f"  {n:50s}  last_seen={ls}")

# 2. Counts per event in last 30 days
section("2. Counts per subscription event (last 30 days)")
res = q("""
SELECT event, count() AS c, max(timestamp) AS last_ts, min(timestamp) AS first_ts
FROM events
WHERE timestamp > now() - INTERVAL 30 DAY
  AND (event ILIKE '%subscr%' OR event ILIKE '%paywall%' OR event ILIKE '%purchas%' OR event ILIKE '%promo%' OR event ILIKE '%product_selected%' OR event ILIKE '%product_clicked%' OR event ILIKE '%trial%' OR event ILIKE '%premium%')
GROUP BY event ORDER BY c DESC
""")
for row in res.get("results", []) if isinstance(res, dict) else []:
    print(f"  {row[0]:45s}  count={row[1]:6d}  first={row[2]}  last={row[3]}")
if "error" in res: print("ERR:", res)

# 3. Funnel sample: paywall_shown -> product_selected -> subscription_purchase_completed
section("3. Monetization funnel users in last 30d")
res = q("""
SELECT
  countIf(event='paywall_shown') AS paywall_shown,
  countIf(event='product_selected') AS product_selected,
  countIf(event='product_clicked') AS product_clicked,
  countIf(event='subscription_purchase_completed') AS purchase_completed,
  countIf(event='subscription_purchase_failed') AS purchase_failed,
  countIf(event='subscription_restored') AS restored,
  countIf(event='trial_started') AS trial_started,
  countIf(event='subscription_cancelled') AS cancelled,
  countDistinctIf(distinct_id, event='paywall_shown') AS users_paywall,
  countDistinctIf(distinct_id, event='product_selected') AS users_selected,
  countDistinctIf(distinct_id, event='subscription_purchase_completed') AS users_completed
FROM events
WHERE timestamp > now() - INTERVAL 30 DAY
""")
for row in res.get("results", []) if isinstance(res, dict) else []:
    cols = ["paywall_shown","product_selected","product_clicked","purchase_completed","purchase_failed","restored","trial_started","cancelled","users_paywall","users_selected","users_completed"]
    for k, v in zip(cols, row):
        print(f"  {k:30s}: {v}")
if "error" in res: print("ERR:", res)

# 4. Recent subscription events with their properties (last 30d, sample)
section("4. Recent subscription events sample (last 14d, up to 50)")
res = q("""
SELECT timestamp, event, distinct_id, properties
FROM events
WHERE timestamp > now() - INTERVAL 14 DAY
  AND (event ILIKE '%subscr%' OR event ILIKE '%paywall%' OR event ILIKE '%purchas%' OR event ILIKE '%product_selected%' OR event ILIKE '%trial%')
ORDER BY timestamp DESC
LIMIT 50
""")
for row in res.get("results", []) if isinstance(res, dict) else []:
    ts, ev, did, props = row
    p = json.loads(props) if isinstance(props, str) else (props or {})
    keys = sorted([k for k in p.keys() if not k.startswith("$")])[:10]
    print(f"  {ts} {ev:35s} {did[:16]:16s} props={keys}")
if "error" in res: print("ERR:", res)

# 5. Property keys ever attached to monetization events
section("5. Property keys on subscription_purchase_completed / paywall_shown / product_selected (90d)")
for ev_name in ["subscription_purchase_completed","paywall_shown","product_selected","product_clicked","subscription_purchase_failed","subscription_restored","trial_started"]:
    res = q(f"""
    SELECT arrayDistinct(arrayFlatten(groupArray(JSONExtractKeys(toString(properties))))) AS keys, count() AS c
    FROM events
    WHERE timestamp > now() - INTERVAL 90 DAY AND event = '{ev_name}'
    """)
    rows = res.get("results", []) if isinstance(res, dict) else []
    if rows and rows[0][1] > 0:
        keys = [k for k in rows[0][0] if not k.startswith("$")]
        print(f"  {ev_name:40s} count={rows[0][1]:5d} keys={sorted(keys)[:25]}")
    else:
        print(f"  {ev_name:40s} count=0")
