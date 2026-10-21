"""Drill into the 4 purchase_started / 4 purchase_failed events to see what really happened."""
import os, json, urllib.request, urllib.error

def env(name):
    for line in open(os.path.join(os.path.dirname(__file__), "..", "MindSync", ".env"), encoding="utf-8", errors="ignore"):
        line = line.strip()
        if line.startswith(name + "="):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return None

HOST = env("POSTHOG_HOST"); KEY = env("POSTHOG_PERSONAL_API_KEY"); PID = env("POSTHOG_PROJECT_ID")

def q(hog):
    req = urllib.request.Request(
        f"{HOST}/api/projects/{PID}/query/",
        data=json.dumps({"query": {"kind": "HogQLQuery", "query": hog}}).encode(),
        headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read())

def section(t): print(f"\n{'='*70}\n{t}\n{'='*70}")

# 1. Pełne dane wszystkich purchase_started + purchase_failed
section("1. ALL purchase_started events (full props)")
res = q("""
SELECT timestamp, distinct_id,
       properties.product_id, properties.product_price, properties.currency_code,
       properties.subscription_type, properties.product_type
FROM events
WHERE event = 'subscription_purchase_started'
ORDER BY timestamp ASC
""")
for row in res.get("results", []):
    print(f"  {row[0]} did={row[1][:20]} pid={row[2]} price={row[3]} {row[4]} type={row[5]} pt={row[6]}")

section("2. ALL purchase_failed events (full props — error_message kluczowe)")
res = q("""
SELECT timestamp, distinct_id,
       properties.product_id, properties.error_message,
       properties.subscription_type, properties.product_type
FROM events
WHERE event = 'subscription_purchase_failed'
ORDER BY timestamp ASC
""")
for row in res.get("results", []):
    print(f"  {row[0]} did={row[1][:20]} pid={row[2]} error={row[3]!r} type={row[4]} pt={row[5]}")

# 3. Czy started i failed dotyczą tych samych transakcji (po distinct_id+timestamp)
section("3. Czy 4 starts == 4 fails u tych samych userów?")
res = q("""
SELECT distinct_id,
       countIf(event='subscription_purchase_started') AS starts,
       countIf(event='subscription_purchase_failed') AS fails,
       countIf(event='subscription_purchase_completed') AS completes,
       countIf(event='subscription_product_selected') AS selects,
       min(timestamp) AS first_seen,
       max(timestamp) AS last_seen
FROM events
WHERE event IN ('subscription_purchase_started','subscription_purchase_failed','subscription_purchase_completed','subscription_product_selected','subscription_screen_opened')
GROUP BY distinct_id
ORDER BY starts DESC, selects DESC
""")
for row in res.get("results", []):
    print(f"  did={row[0][:24]:24s} starts={row[1]} fails={row[2]} completed={row[3]} selects={row[4]} first={row[5]} last={row[6]}")

# 4. Distinct_id w purchase_started vs distinct_id w product_selected — kto się zatrzymał
section("4. Funnel attempt per user (kto wybrał produkt ale nie kliknął kup)")
res = q("""
SELECT distinct_id,
       countIf(event='subscription_screen_opened') AS opened,
       countIf(event='subscription_product_selected') AS selected,
       countIf(event='subscription_purchase_started') AS started,
       countIf(event='subscription_purchase_failed') AS failed,
       countIf(event='subscription_purchase_completed') AS completed
FROM events
WHERE event ILIKE 'subscription%' OR event = 'paywall_shown'
GROUP BY distinct_id
HAVING opened > 0 OR selected > 0
ORDER BY opened DESC
""")
for row in res.get("results", []):
    print(f"  did={row[0][:24]:24s} opened={row[1]} selected={row[2]} started={row[3]} failed={row[4]} completed={row[5]}")

# 5. Person properties (jeśli identify) — aby zobaczyć czy user_id == firebase_uid
section("5. Person properties dla uczestników purchase flow")
res = q("""
SELECT distinct_id, person.properties.email, person.properties.subscription_tier, person.properties.user_id
FROM events
WHERE event = 'subscription_purchase_started'
GROUP BY distinct_id, person.properties.email, person.properties.subscription_tier, person.properties.user_id
""")
for row in res.get("results", []):
    print(f"  did={row[0][:24]:24s} email={row[1]} tier={row[2]} uid={row[3]}")
