# -*- coding: utf-8 -*-
"""Pelny re-review SEO mindsync.app - wszystko naraz, na zywym HTML-u."""
import re, json, html, sys, urllib.request, urllib.error, random, xml.etree.ElementTree as ET
sys.stdout.reconfigure(encoding='utf-8')

BASE = "https://www.mindsync.app"
UA = {"User-Agent": "Mozilla/5.0 (compatible; SEOReview/1.0)"}
issues, notes = [], []

def get(url, allow_redirect=True):
    req = urllib.request.Request(url, headers=UA)
    op = urllib.request.build_opener()
    if not allow_redirect:
        class NR(urllib.request.HTTPRedirectHandler):
            def redirect_request(self, *a, **k): return None
        op = urllib.request.build_opener(NR)
    try:
        r = op.open(req, timeout=45)
        return r.getcode(), r.read().decode("utf-8", "replace"), dict(r.headers)
    except urllib.error.HTTPError as e:
        return e.code, (e.read().decode("utf-8", "replace") if e.fp else ""), dict(e.headers)
    except Exception as e:
        return -1, str(e), {}

def cb(u):
    return u + ("&" if "?" in u else "?") + "cb=" + str(random.randint(1, 10**9))

def meta(hs, attr, val):
    for p in (r'<meta[^>]*\b%s="%s"[^>]*\bcontent="([^"]*)"' % (attr, re.escape(val)),
              r'<meta[^>]*\bcontent="([^"]*)"[^>]*\b%s="%s"' % (attr, re.escape(val))):
        m = re.search(p, hs, re.I)
        if m: return html.unescape(m.group(1))
    return ""

def link(hs, rel):
    for p in (r'<link[^>]*\brel="%s"[^>]*\bhref="([^"]*)"' % rel,
              r'<link[^>]*\bhref="([^"]*)"[^>]*\brel="%s"' % rel):
        m = re.search(p, hs, re.I)
        if m: return m.group(1)
    return ""

def text_of(hs):
    b = re.sub(r'(?is)<(script|style|head)\b.*?</\1>', ' ', hs)
    b = re.sub(r'<[^>]+>', ' ', b)
    return re.sub(r'\s+', ' ', html.unescape(b)).strip()

print("=" * 100)
print("1. SITEMAPA")
code, sm, _ = get(cb(BASE + "/sitemap.xml"))
urls = [e.text for e in ET.fromstring(sm).iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")]
print(f"   status={code}  URL-i={len(urls)}")
for u in urls:
    if re.search(r"/admin|/copy/|/untitled|/401|/404", u):
        issues.append(f"sitemap zawiera smieciowy URL: {u}")
if len({u for u in urls}) != len(urls): issues.append("sitemap ma duplikaty")
if any(not u.startswith("https://www.") for u in urls): issues.append("sitemap ma URL-e spoza kanonicznej domeny www")

print("=" * 100)
print("2. ROBOTS.TXT")
code, rb, _ = get(cb(BASE + "/robots.txt"))
smaps = re.findall(r'(?mi)^\s*Sitemap:\s*(\S+)', rb)
disallows = re.findall(r'(?mi)^\s*Disallow:\s*(\S+)', rb)
print(f"   status={code}  dyrektyw Sitemap={len(smaps)} -> {smaps}")
print(f"   Disallow={disallows or '(brak)'}")
if len(smaps) != 1: issues.append(f"robots.txt: {len(smaps)} dyrektyw Sitemap (ma byc dokladnie 1)")
if smaps and smaps[0] != BASE + "/sitemap.xml": issues.append(f"robots.txt: zly URL sitemapy {smaps}")
if "llms-full" in rb: issues.append("robots.txt nadal odsyla do llms-full.txt (404)")
if disallows: notes.append(f"robots.txt ma Disallow: {disallows}")
for bot in ["GPTBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "OAI-SearchBot"]:
    if bot not in rb: issues.append(f"robots.txt: brak wpisu dla {bot}")

print("=" * 100)
print("3. LLMS.TXT")
code, lm, _ = get(cb(BASE + "/llms.txt"))
print(f"   status={code}  bytes={len(lm)}")
for bad, why in [("sits augments", "urwane zdanie"), ("support@mindsync.app", "nieaktualny adres"),
                 ("https://mindsync.app", "URL bez www"), ("Pricing (indicative)", "stary naglowek cennika")]:
    if bad in lm: issues.append(f"llms.txt nadal zawiera '{bad}' ({why})")
for good in ["augments therapy", "hello@mindsync.app", "https://www.mindsync.app/", "$12.99 per month"]:
    if good not in lm: issues.append(f"llms.txt: brak oczekiwanego '{good}'")
if "—" in lm: issues.append("llms.txt zawiera em-dash")
code2, _, _ = get(cb(BASE + "/llms-full.txt"))
print(f"   /llms-full.txt -> {code2} (oczekiwane 404, juz nieodsylany)")

print("=" * 100)
print("4. ODPUBLIKOWANE STRONY (oczekiwane 404)")
for p in ["/admin/changelog", "/admin/licenses", "/admin/styleguide", "/copy/home-copy",
          "/copy/sign-in", "/untitled", "/untitled-2",
          "/admin---under-construction/building", "/admin---under-construction/faq-building"]:
    c, _, _ = get(BASE + p)
    if c != 404: issues.append(f"{p} zwraca {c}, oczekiwane 404")
    print(f"   {p:45} {c}")

print("=" * 100)
print("5. PRZEKIEROWANIA")
for u, exp in [("http://mindsync.app/", 301), ("https://mindsync.app/", 301), ("http://www.mindsync.app/", 301)]:
    c, _, h = get(u, allow_redirect=False)
    loc = h.get("Location", "")
    print(f"   {u:32} {c} -> {loc}")
    if c != exp: issues.append(f"{u}: status {c}, oczekiwane {exp}")
    if c == 301 and not loc.startswith("https://"): issues.append(f"{u}: przekierowanie nie na https")

print("=" * 100)
print("6. STRONY")
hdr = f"{'URL':<58}{'st':>4}{'ttl':>5}{'dsc':>5}{'h1':>4}{'words':>7}{'lang':>6}  OG can  JSON-LD"
print(hdr); print("-" * 110)
nav_missing = []
for u in urls:
    code, hs, _ = get(cb(u))
    short = u.replace(BASE, "") or "/"
    if code != 200:
        issues.append(f"{short}: status {code}"); print(f"   {short:<55}{code:>4}"); continue
    title = html.unescape((re.search(r'(?is)<title[^>]*>(.*?)</title>', hs) or re.match("", "")).group(1).strip()) if re.search(r'(?is)<title[^>]*>(.*?)</title>', hs) else ""
    desc = meta(hs, "name", "description")
    ogi = meta(hs, "property", "og:image")
    ogt = meta(hs, "property", "og:title")
    can = link(hs, "canonical")
    h1s = re.findall(r'(?is)<h1[^>]*>(.*?)</h1>', hs)
    lang = (re.search(r'<html[^>]*\blang="([^"]*)"', hs) or [None, ""])[1] if re.search(r'<html[^>]*\blang="([^"]*)"', hs) else ""
    words = len(text_of(hs).split())
    blocks = re.findall(r'(?is)<script[^>]*application/ld\+json[^>]*>(.*?)</script>', hs)
    ok = esc = bad = 0
    types = set()
    for b in blocks:
        s = b.strip()
        if "&quot;" in s:
            esc += 1
            try:
                o = json.loads(html.unescape(s))
                for n in (o.get("@graph") or [o]):
                    t = n.get("@type");  types.update(t if isinstance(t, list) else [t])
            except Exception: bad += 1
        else:
            try:
                o = json.loads(s); ok += 1
                for n in (o.get("@graph") or [o]):
                    t = n.get("@type");  types.update(t if isinstance(t, list) else [t])
            except Exception: bad += 1
    ld = f"{ok}ok" + (f"/{esc}js" if esc else "") + (f"/{bad}BAD" if bad else "")
    print(f"   {short:<55}{code:>4}{len(title):>5}{len(desc):>5}{len(h1s):>4}{words:>7}{lang:>6}  {'y' if ogi else 'NO':<3}{'y' if can else 'NO':<4} {ld}")

    if not title: issues.append(f"{short}: brak <title>")
    elif len(title) > 62: issues.append(f"{short}: title {len(title)} znakow")
    if not desc: issues.append(f"{short}: brak meta description")
    elif len(desc) > 165: issues.append(f"{short}: description {len(desc)} znakow")
    if len(h1s) != 1: issues.append(f"{short}: h1={len(h1s)}")
    if not ogi: issues.append(f"{short}: brak og:image")
    if not ogt: issues.append(f"{short}: brak og:title")
    if not can: issues.append(f"{short}: brak canonical")
    elif can.rstrip("/") != u.rstrip("/"): issues.append(f"{short}: canonical '{can}' != '{u}'")
    if words < 300: issues.append(f"{short}: tylko {words} slow")
    if bad: issues.append(f"{short}: {bad} nieparsowalnych blokow JSON-LD")
    if ok == 0 and esc == 0: issues.append(f"{short}: brak JSON-LD")
    if "aggregateRating" in hs and "/journal/" not in u: issues.append(f"{short}: wystepuje aggregateRating (sprawdz czy realne)")
    if "—" in text_of(hs) and short in ("/features", "/audience", "/membership"):
        issues.append(f"{short}: em-dash w nowej tresci")
    exp_lang = "pl" if short in ("/freebie", "/testerzy") else "en"
    if lang != exp_lang: notes.append(f"{short}: lang='{lang}' w surowym HTML, oczekiwane '{exp_lang}' (moze byc ustawiane przez JS)")
    if '/features"' not in hs: nav_missing.append(short + " (brak linku do /features)")
    if '/audience"' not in hs: nav_missing.append(short + " (brak linku do /audience)")
    # linki do odpublikowanych stron
    for m in re.findall(r'href="(/(?:admin|copy|untitled)[^"]*)"', hs):
        issues.append(f"{short}: link do odpublikowanej strony {m}")

print("=" * 100)
print("7. LINKOWANIE WEWNETRZNE")
if nav_missing:
    print("   strony bez linku nawigacyjnego:")
    for x in sorted(set(nav_missing)): print("     -", x)
else:
    print("   OK: /features i /audience linkowane z kazdej strony")

print("=" * 100)
print("PODSUMOWANIE")
print(f"   ODCHYLENIA: {len(issues)}")
for i in issues: print("   [!]", i)
print(f"   UWAGI: {len(notes)}")
for n in notes: print("   [i]", n)
