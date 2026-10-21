#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pobieranie danych z Google Search Console dla sklep.plasmet.pl (baseline przed migracją na Shoper).

Tylko biblioteka standardowa Pythona — żadnego pip install (bezpieczne na Pythonie 3.14).
OAuth: przepływ "installed app" z PKCE, token zapisywany lokalnie i odświeżany automatycznie.

Komendy:
    python pull_gsc.py auth              # jednorazowa autoryzacja (otworzy przeglądarkę)
    python pull_gsc.py sites             # lista właściwości GSC dostępnych dla konta
    python pull_gsc.py pull              # pobierz dane (site z gsc.config.json)
    python pull_gsc.py pull --site sc-domain:plasmet.pl
    python pull_gsc.py pull --months 16 --full   # pełny zakres + wymiar query+page
    python pull_gsc.py submit-sitemap    # zgłoś sitemapę (GSC -> Sitemaps -> Submit), wymaga zakresu webmasters
    python pull_gsc.py submit-sitemap --site sc-domain:mindsync.app --feed https://www.mindsync.app/sitemap.xml

Wynik: migracja/gsc/baseline-RRRR-MM-DD/ (queries.csv, pages.csv, dates.csv, [query-page.csv], summary.json)
"""
import sys, os, json, time, base64, hashlib, secrets, webbrowser, csv, datetime
import urllib.parse, urllib.request, urllib.error, http.server

HERE          = os.path.dirname(os.path.abspath(__file__))
CLIENT_SECRET = os.path.join(HERE, 'client_secret.json')
TOKEN_FILE    = os.path.join(HERE, 'token.json')
CONFIG_FILE   = os.path.join(HERE, 'gsc.config.json')
OUT_BASE      = os.path.abspath(os.path.join(HERE, '..', '..', 'migracja', 'gsc'))

# Pelny zakres (2026-09-25): obejmuje odczyt (sites, pull, searchAnalytics) ORAZ zapis
# potrzebny do submit-sitemap. Token wydany wczesniej na .readonly dalej dziala do odczytu,
# ale submit-sitemap dostanie 403; wtedy raz: python scripts/gsc/pull_gsc.py auth
SCOPE     = 'https://www.googleapis.com/auth/webmasters'
DEFAULT_FEED = 'https://www.mindsync.app/sitemap.xml'
AUTH_URI  = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URI = 'https://oauth2.googleapis.com/token'
API       = 'https://www.googleapis.com/webmasters/v3'
ROW_LIMIT = 25000  # maksimum GSC na jedno zapytanie


# ---------- pomocnicze ----------
def load_client():
    if not os.path.exists(CLIENT_SECRET):
        sys.exit('Brak client_secret.json w scripts/gsc/. Patrz README.md (krok: utworzenie OAuth client typu Desktop).')
    with open(CLIENT_SECRET, encoding='utf-8') as f:
        data = json.load(f)
    node = data.get('installed') or data.get('web')
    if not node:
        sys.exit('client_secret.json nie ma sekcji "installed" — utwórz OAuth client TYPU "Aplikacja komputerowa" (Desktop).')
    return node['client_id'], node['client_secret']

class GscHttpError(Exception):
    """Rzucany przez http_json(..., raise_http=True) zamiast sys.exit (kod + tresc bledu)."""
    def __init__(self, code, url, detail):
        super().__init__(f'HTTP {code} przy {url}')
        self.code, self.url, self.detail = code, url, detail

def http_json(url, payload=None, form=None, headers=None, method=None, raise_http=False):
    headers = dict(headers or {})
    body = None
    if form is not None:
        body = urllib.parse.urlencode(form).encode()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    elif payload is not None:
        body = json.dumps(payload).encode()
        headers['Content-Type'] = 'application/json'
    elif method in ('PUT', 'POST'):
        body = b''   # pusty body z Content-Length: 0 (bez tego Google moze odpowiedziec 411)
    req = urllib.request.Request(url, data=body, headers=headers, method=method or ('POST' if body else 'GET'))
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read().decode('utf-8')
            return json.loads(raw) if raw.strip() else {}   # sitemaps.submit zwraca pusty body
    except urllib.error.HTTPError as e:
        detail = e.read().decode('utf-8', errors='replace')
        if raise_http:
            raise GscHttpError(e.code, url, detail)
        sys.exit(f'Błąd HTTP {e.code} przy {url}\n{detail}')

def save_token(tok):
    with open(TOKEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(tok, f, ensure_ascii=False, indent=2)


# ---------- OAuth ----------
def cmd_auth():
    cid, csecret = load_client()
    verifier  = base64.urlsafe_b64encode(secrets.token_bytes(40)).rstrip(b'=').decode()
    challenge = base64.urlsafe_b64encode(hashlib.sha256(verifier.encode()).digest()).rstrip(b'=').decode()
    state = secrets.token_urlsafe(16)

    holder = {}
    class Handler(http.server.BaseHTTPRequestHandler):
        def do_GET(self):
            qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
            holder.update({k: v[0] for k, v in qs.items()})
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write('<h2>Autoryzacja zakończona — możesz zamknąć to okno.</h2>'.encode('utf-8'))
        def log_message(self, *a): pass

    srv = http.server.HTTPServer(('127.0.0.1', 0), Handler)   # port efemeryczny — Google dopuszcza dowolny port loopback
    port = srv.server_address[1]
    redirect = f'http://127.0.0.1:{port}/'

    url = AUTH_URI + '?' + urllib.parse.urlencode({
        'client_id': cid, 'redirect_uri': redirect, 'response_type': 'code',
        'scope': SCOPE, 'access_type': 'offline', 'prompt': 'consent',
        'state': state, 'code_challenge': challenge, 'code_challenge_method': 'S256',
    })
    print('Otwieram przeglądarkę do logowania Google...')
    print('Jeśli się nie otworzy, wklej ręcznie ten adres:\n' + url + '\n')
    try: webbrowser.open(url)
    except Exception: pass
    srv.handle_request()   # obsłuż jedno przekierowanie zwrotne
    srv.server_close()

    if holder.get('error'):     sys.exit('Google zwrócił błąd: ' + holder['error'])
    if holder.get('state') != state: sys.exit('Niezgodny state (możliwy CSRF) — spróbuj ponownie.')
    if 'code' not in holder:    sys.exit('Brak parametru code w odpowiedzi: ' + json.dumps(holder))

    tok = http_json(TOKEN_URI, form={
        'client_id': cid, 'client_secret': csecret, 'code': holder['code'],
        'code_verifier': verifier, 'grant_type': 'authorization_code', 'redirect_uri': redirect,
    })
    if 'refresh_token' not in tok:
        print('UWAGA: brak refresh_token. Cofnij dostęp aplikacji na https://myaccount.google.com/permissions i uruchom auth ponownie.')
    tok['_obtained'] = int(time.time())
    save_token(tok)
    print('OK — token zapisany do token.json.')

def access_token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit('Brak token.json — uruchom najpierw: python pull_gsc.py auth')
    with open(TOKEN_FILE, encoding='utf-8') as f:
        tok = json.load(f)
    if tok.get('access_token') and time.time() < tok.get('_obtained', 0) + tok.get('expires_in', 3600) - 120:
        return tok['access_token']
    cid, csecret = load_client()
    new = http_json(TOKEN_URI, form={
        'client_id': cid, 'client_secret': csecret,
        'grant_type': 'refresh_token', 'refresh_token': tok['refresh_token'],
    })
    tok['access_token'] = new['access_token']
    tok['expires_in']   = new.get('expires_in', 3600)
    tok['_obtained']    = int(time.time())
    save_token(tok)
    return tok['access_token']


# ---------- API GSC ----------
def auth_header():
    return {'Authorization': 'Bearer ' + access_token()}

def cmd_sites():
    data = http_json(f'{API}/sites', headers=auth_header())
    entries = data.get('siteEntry', [])
    if not entries:
        print('Brak właściwości — czy konto, którym się zalogowałeś, ma dostęp do sklep.plasmet.pl w GSC?')
        return
    print('Dostępne właściwości GSC (użyj wartości w --site lub w gsc.config.json):')
    for s in entries:
        print(f"  {s.get('permissionLevel',''):24} {s.get('siteUrl','')}")

def query_all(site, dims, start, end):
    enc = urllib.parse.quote(site, safe='')
    rows, start_row = [], 0
    while True:
        data = http_json(
            f'{API}/sites/{enc}/searchAnalytics/query',
            payload={'startDate': start, 'endDate': end, 'dimensions': dims,
                     'rowLimit': ROW_LIMIT, 'startRow': start_row, 'dataState': 'all'},
            headers=auth_header())
        batch = data.get('rows', [])
        rows.extend(batch)
        if len(batch) < ROW_LIMIT:
            break
        start_row += ROW_LIMIT
    return rows

def write_csv(path, dims, rows):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:   # utf-8-sig => poprawne PL znaki w Excelu
        w = csv.writer(f)
        w.writerow(dims + ['clicks', 'impressions', 'ctr', 'position'])
        for r in rows:
            w.writerow(r.get('keys', []) + [
                r.get('clicks', 0), r.get('impressions', 0),
                round(r.get('ctr', 0.0), 4), round(r.get('position', 0.0), 2)])

def cmd_pull(argv):
    # parametry
    site = None; months = 16; full = False
    i = 0
    while i < len(argv):
        if argv[i] == '--site' and i + 1 < len(argv): site = argv[i+1]; i += 2
        elif argv[i] == '--months' and i + 1 < len(argv): months = int(argv[i+1]); i += 2
        elif argv[i] == '--full': full = True; i += 1
        else: i += 1
    if not site and os.path.exists(CONFIG_FILE):
        site = json.load(open(CONFIG_FILE, encoding='utf-8')).get('site_url')
    if not site:
        sys.exit('Podaj właściwość: --site <wartość z `sites`> albo ustaw site_url w gsc.config.json')

    end   = datetime.date.today() - datetime.timedelta(days=3)        # ~3 dni opóźnienia danych GSC
    start = max(end - datetime.timedelta(days=int(months * 30.4)),    # ~16 miesięcy wstecz
                end - datetime.timedelta(days=485))
    s, e = start.isoformat(), end.isoformat()
    today = datetime.date.today().isoformat()
    out = os.path.join(OUT_BASE, f'baseline-{today}')
    os.makedirs(out, exist_ok=True)
    print(f'Właściwość: {site}\nZakres: {s} … {e}\nKatalog wyjściowy: {out}\n')

    jobs = [('queries.csv', ['query']), ('pages.csv', ['page']), ('dates.csv', ['date'])]
    if full:
        jobs.append(('query-page.csv', ['query', 'page']))

    summary = {'site': site, 'startDate': s, 'endDate': e, 'pulledOn': today, 'rows': {}}
    for fname, dims in jobs:
        print(f'  pobieram {fname} (wymiary: {",".join(dims)}) ...', end=' ', flush=True)
        rows = query_all(site, dims, s, e)
        write_csv(os.path.join(out, fname), dims, rows)
        summary['rows'][fname] = len(rows)
        print(f'{len(rows)} wierszy')

    totals = query_all(site, [], s, e)   # bez wymiarów => sumy zbiorcze
    if totals:
        t = totals[0]
        summary['totals'] = {'clicks': t.get('clicks'), 'impressions': t.get('impressions'),
                             'ctr': round(t.get('ctr', 0), 4), 'position': round(t.get('position', 0), 2)}
    with open(os.path.join(out, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print('\nGotowe. Podsumowanie:')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def cmd_submit_sitemap(argv):
    """Odpowiednik GSC -> Sitemaps -> Submit: PUT sitemaps.submit, potem GET tej sitemapy.
    Wyjscie ASCII w jednej linii 'SUBMIT-SITEMAP OK ... lastDownloaded=...' (parsuje je
    scripts/webflow/blog-publish.ps1). Kod wyjscia != 0 przy kazdym bledzie."""
    site = None; feed = DEFAULT_FEED
    i = 0
    while i < len(argv):
        if argv[i] == '--site' and i + 1 < len(argv): site = argv[i+1]; i += 2
        elif argv[i] == '--feed' and i + 1 < len(argv): feed = argv[i+1]; i += 2
        else: i += 1
    if not site and os.path.exists(CONFIG_FILE):
        site = json.load(open(CONFIG_FILE, encoding='utf-8')).get('site_url')
    if not site:
        print('SUBMIT-SITEMAP BLAD: podaj --site albo ustaw site_url w gsc.config.json', file=sys.stderr)
        sys.exit(2)
    url = f"{API}/sites/{urllib.parse.quote(site, safe='')}/sitemaps/{urllib.parse.quote(feed, safe='')}"
    try:
        hdr = auth_header()
        http_json(url, headers=hdr, method='PUT', raise_http=True)
        info = http_json(url, headers=hdr, method='GET', raise_http=True)
    except GscHttpError as e:
        low = (e.detail or '').lower()
        if e.code == 403 and ('insufficient' in low or 'scope' in low):
            print('SUBMIT-SITEMAP BLAD: token ma tylko readonly, uruchom: python scripts/gsc/pull_gsc.py auth',
                  file=sys.stderr)
            sys.exit(3)
        if e.code == 403:
            print(f'SUBMIT-SITEMAP BLAD: HTTP 403 (brak uprawnien do wlasciwosci {site}?) {e.detail[:300]}',
                  file=sys.stderr)
            sys.exit(4)
        print(f'SUBMIT-SITEMAP BLAD: HTTP {e.code} {" ".join((e.detail or "").split())[:300]}', file=sys.stderr)
        sys.exit(5)
    except (urllib.error.URLError, OSError) as e:
        print(f'SUBMIT-SITEMAP BLAD: siec: {e}', file=sys.stderr)
        sys.exit(6)
    print(f"SUBMIT-SITEMAP OK site={site} feed={feed} "
          f"lastSubmitted={info.get('lastSubmitted', '?')} lastDownloaded={info.get('lastDownloaded', '?')} "
          f"isPending={info.get('isPending', '?')} errors={info.get('errors', '?')} warnings={info.get('warnings', '?')}")


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if   cmd == 'auth':  cmd_auth()
    elif cmd == 'sites': cmd_sites()
    elif cmd == 'pull':  cmd_pull(sys.argv[2:])
    elif cmd == 'submit-sitemap': cmd_submit_sitemap(sys.argv[2:])
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
