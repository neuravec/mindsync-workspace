#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pobieranie danych z Google Analytics 4 dla mindsync.app (ruch na stronie i blogu /journal/).

Tylko biblioteka standardowa Pythona, żadnego pip install.
OAuth: przepływ "installed app" z PKCE, token zapisywany lokalnie i odświeżany automatycznie.
Klient OAuth jest WSPÓLNY z GSC: scripts/gsc/client_secret.json (projekt mindsync-8f534), nie kopiujemy go.
Token GA4 jest osobny: scripts/ga4/token.json (zakres analytics.readonly).

Komendy:
    python scripts/ga4/pull_ga4.py auth                 # jednorazowa autoryzacja (otworzy przeglądarkę)
    python scripts/ga4/pull_ga4.py properties           # lista kont i właściwości GA4 dostępnych dla konta
    python scripts/ga4/pull_ga4.py pull                 # pobierz dane (property_id z ga4.config.json)
    python scripts/ga4/pull_ga4.py pull --days 90 --property properties/123456789
    python scripts/ga4/pull_ga4.py pull --blog-prefix /journal/

Wynik: analytics-reports/raw/ga4/RRRR-MM-DD/
    overview_by_date.csv, landing_pages.csv, channels.csv, source_medium.csv,
    countries.csv, devices.csv, blog_pages.csv, summary.json
"""
import sys, os, json, time, base64, hashlib, secrets, webbrowser, csv, datetime
import urllib.parse, urllib.request, urllib.error, http.server

HERE          = os.path.dirname(os.path.abspath(__file__))
ROOT          = os.path.abspath(os.path.join(HERE, '..', '..'))
CLIENT_SECRET = os.path.join(ROOT, 'scripts', 'gsc', 'client_secret.json')   # wspólny klient Desktop z GSC
TOKEN_FILE    = os.path.join(HERE, 'token.json')
CONFIG_FILE   = os.path.join(HERE, 'ga4.config.json')
OUT_BASE      = os.path.join(ROOT, 'analytics-reports', 'raw', 'ga4')

SCOPE      = 'https://www.googleapis.com/auth/analytics.readonly'
AUTH_URI   = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URI  = 'https://oauth2.googleapis.com/token'
DATA_API   = 'https://analyticsdata.googleapis.com/v1beta'
ADMIN_API  = 'https://analyticsadmin.googleapis.com/v1beta'
GCP_PROJECT = 'mindsync-8f534'
PAGE_LIMIT = 100000   # GA4 Data API pozwala do 250000 wierszy na zapytanie; bierzemy bezpieczne 100k

API_NAMES = {
    'analyticsdata.googleapis.com':  ('Google Analytics Data API',  'analyticsdata.googleapis.com'),
    'analyticsadmin.googleapis.com': ('Google Analytics Admin API', 'analyticsadmin.googleapis.com'),
}

# Konsola Windows bez UTF-8 nie może wysypać się na polskich znakach.
for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(errors='replace')
    except Exception: pass


# ---------- pomocnicze ----------
def load_client():
    if not os.path.exists(CLIENT_SECRET):
        sys.exit('Brak pliku scripts/gsc/client_secret.json (wspólny klient OAuth Desktop z projektu '
                 f'{GCP_PROJECT}). Patrz scripts/gsc/README.md, a potem scripts/ga4/README.md.')
    with open(CLIENT_SECRET, encoding='utf-8') as f:
        data = json.load(f)
    node = data.get('installed') or data.get('web')
    if not node:
        sys.exit('client_secret.json nie ma sekcji "installed": potrzebny jest OAuth client TYPU "Aplikacja komputerowa" (Desktop).')
    return node['client_id'], node['client_secret']

class ApiHttpError(Exception):
    def __init__(self, code, url, detail):
        super().__init__(f'HTTP {code} przy {url}')
        self.code, self.url, self.detail = code, url, detail

def explain_http_error(e):
    """Zamienia błąd HTTP na czytelny komunikat po polsku (bez tokenów)."""
    low = (e.detail or '').lower()
    host = urllib.parse.urlparse(e.url).netloc
    if e.code == 403 and ('service_disabled' in low or 'has not been used' in low or 'it is disabled' in low):
        name, api_id = API_NAMES.get(host, (host, host))
        return (f'API "{name}" nie jest włączone w projekcie {GCP_PROJECT}.\n'
                f'Włącz je tutaj: https://console.cloud.google.com/apis/library/{api_id}?project={GCP_PROJECT}\n'
                'Po włączeniu odczekaj 1 do 5 minut i uruchom komendę ponownie.')
    if e.code == 403 and ('insufficient' in low and 'scope' in low or 'access_token_scope_insufficient' in low):
        return 'Token nie ma zakresu analytics.readonly. Uruchom ponownie: python scripts/ga4/pull_ga4.py auth'
    if e.code == 403:
        return ('HTTP 403: konto, którym się zalogowałeś, nie ma dostępu do tej właściwości GA4 '
                '(GA4 -> Administracja -> Zarządzanie dostępem do usługi, wymagana rola co najmniej "Wyświetlający").\n'
                + ' '.join((e.detail or '').split())[:400])
    if e.code == 401:
        return 'HTTP 401: token nieważny. Uruchom ponownie: python scripts/ga4/pull_ga4.py auth'
    if e.code == 400:
        return 'HTTP 400 (złe zapytanie do API): ' + ' '.join((e.detail or '').split())[:600]
    return f'Błąd HTTP {e.code} przy {e.url}\n' + ' '.join((e.detail or '').split())[:600]

def http_json(url, payload=None, form=None, headers=None, method=None, raise_http=False):
    headers = dict(headers or {})
    body = None
    if form is not None:
        body = urllib.parse.urlencode(form).encode()
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
    elif payload is not None:
        body = json.dumps(payload).encode()
        headers['Content-Type'] = 'application/json'
    req = urllib.request.Request(url, data=body, headers=headers, method=method or ('POST' if body else 'GET'))
    try:
        with urllib.request.urlopen(req, timeout=120) as r:
            raw = r.read().decode('utf-8')
            return json.loads(raw) if raw.strip() else {}
    except urllib.error.HTTPError as e:
        err = ApiHttpError(e.code, url, e.read().decode('utf-8', errors='replace'))
        if raise_http:
            raise err
        sys.exit(explain_http_error(err))
    except urllib.error.URLError as e:
        sys.exit(f'Błąd sieci przy {url}: {e.reason}')

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
            self.wfile.write('<h2>Autoryzacja GA4 zakończona, możesz zamknąć to okno.</h2>'.encode('utf-8'))
        def log_message(self, *a): pass

    srv = http.server.HTTPServer(('127.0.0.1', 0), Handler)   # port efemeryczny, Google dopuszcza dowolny port loopback
    port = srv.server_address[1]
    redirect = f'http://127.0.0.1:{port}/'

    url = AUTH_URI + '?' + urllib.parse.urlencode({
        'client_id': cid, 'redirect_uri': redirect, 'response_type': 'code',
        'scope': SCOPE, 'access_type': 'offline', 'prompt': 'consent',
        'state': state, 'code_challenge': challenge, 'code_challenge_method': 'S256',
    })
    print('Otwieram przeglądarkę do logowania Google (zakres: analytics.readonly)...')
    print('Jeśli się nie otworzy, wklej ręcznie ten adres:\n' + url + '\n')
    try: webbrowser.open(url)
    except Exception: pass
    srv.handle_request()   # obsłuż jedno przekierowanie zwrotne
    srv.server_close()

    if holder.get('error'):     sys.exit('Google zwrócił błąd: ' + holder['error'])
    if holder.get('state') != state: sys.exit('Niezgodny state (możliwy CSRF), spróbuj ponownie.')
    if 'code' not in holder:    sys.exit('Brak parametru code w odpowiedzi przekierowania.')

    tok = http_json(TOKEN_URI, form={
        'client_id': cid, 'client_secret': csecret, 'code': holder['code'],
        'code_verifier': verifier, 'grant_type': 'authorization_code', 'redirect_uri': redirect,
    })
    if 'refresh_token' not in tok:
        print('UWAGA: brak refresh_token. Cofnij dostęp aplikacji na https://myaccount.google.com/permissions i uruchom auth ponownie.')
    tok['_obtained'] = int(time.time())
    save_token(tok)
    print('OK, token zapisany do scripts/ga4/token.json.')

def access_token():
    if not os.path.exists(TOKEN_FILE):
        sys.exit('Brak scripts/ga4/token.json. Uruchom najpierw: python scripts/ga4/pull_ga4.py auth')
    with open(TOKEN_FILE, encoding='utf-8') as f:
        tok = json.load(f)
    if tok.get('access_token') and time.time() < tok.get('_obtained', 0) + tok.get('expires_in', 3600) - 120:
        return tok['access_token']
    if not tok.get('refresh_token'):
        sys.exit('token.json nie ma refresh_token. Uruchom ponownie: python scripts/ga4/pull_ga4.py auth')
    cid, csecret = load_client()
    try:
        new = http_json(TOKEN_URI, form={
            'client_id': cid, 'client_secret': csecret,
            'grant_type': 'refresh_token', 'refresh_token': tok['refresh_token'],
        }, raise_http=True)
    except ApiHttpError as e:
        if 'invalid_grant' in (e.detail or ''):
            sys.exit('Refresh token wygasł lub został cofnięty (aplikacja OAuth w trybie "Testing" ważna 7 dni). '
                     'Uruchom ponownie: python scripts/ga4/pull_ga4.py auth')
        sys.exit(explain_http_error(e))
    tok['access_token'] = new['access_token']
    tok['expires_in']   = new.get('expires_in', 3600)
    tok['_obtained']    = int(time.time())
    save_token(tok)
    return tok['access_token']

def auth_header():
    return {'Authorization': 'Bearer ' + access_token()}


# ---------- Admin API: lista właściwości ----------
def cmd_properties():
    hdr = auth_header()
    page_token, found = None, 0
    print('Konta i właściwości GA4 (wartość "properties/NNN" wpisz do ga4.config.json lub --property):\n')
    while True:
        q = {'pageSize': 200}
        if page_token: q['pageToken'] = page_token
        data = http_json(f'{ADMIN_API}/accountSummaries?' + urllib.parse.urlencode(q), headers=hdr)
        for acc in data.get('accountSummaries', []):
            print(f"Konto: {acc.get('displayName', '?')}  ({acc.get('account', '?')})")
            for p in acc.get('propertySummaries', []):
                found += 1
                print(f"    {p.get('property', '?'):24} {p.get('displayName', '')}  [{p.get('propertyType', '')}]")
        page_token = data.get('nextPageToken')
        if not page_token:
            break
    if not found:
        print('Brak właściwości. Czy konto, którym się zalogowałeś, ma dostęp do GA4 mindsync.app?')


# ---------- Data API: raporty ----------
def run_report(prop, hdr, body, paginate=True):
    """runReport z paginacją limit/offset. Zwraca (nagłówki, wiersze)."""
    rows, offset, headers = [], 0, None
    while True:
        req = dict(body)
        req.setdefault('limit', PAGE_LIMIT)
        req['offset'] = offset
        data = http_json(f'{DATA_API}/{prop}:runReport', payload=req, headers=hdr, raise_http=True)
        if headers is None:
            headers = ([h['name'] for h in data.get('dimensionHeaders', [])] +
                       [h['name'] for h in data.get('metricHeaders', [])])
        batch = data.get('rows', [])
        for r in batch:
            rows.append([v.get('value', '') for v in r.get('dimensionValues', [])] +
                        [v.get('value', '') for v in r.get('metricValues', [])])
        total = int(data.get('rowCount', 0) or 0)
        offset += len(batch)
        if not paginate or not batch or offset >= total:
            break
    if headers is None:
        headers = [d['name'] for d in body.get('dimensions', [])] + [m['name'] for m in body.get('metrics', [])]
    return headers, rows

def run_report_with_fallback(prop, hdr, body, optional_metric_sets, paginate=True):
    """Próbuje kolejno dołożyć opcjonalne metryki (np. keyEvents, potem conversions); przy HTTP 400 schodzi niżej."""
    base = list(body['metrics'])
    for extra in optional_metric_sets + [[]]:
        b = dict(body)
        b['metrics'] = base + [{'name': m} for m in extra]
        try:
            return run_report(prop, hdr, b, paginate)
        except ApiHttpError as e:
            if e.code == 400 and extra:
                print(f'(metryka {",".join(extra)} niedostępna, próbuję bez niej) ', end='', flush=True)
                continue
            sys.exit(explain_http_error(e))

def write_csv(path, headers, rows):
    with open(path, 'w', newline='', encoding='utf-8-sig') as f:   # utf-8-sig => poprawne znaki w Excelu
        w = csv.writer(f)
        w.writerow(headers)
        w.writerows(rows)

def normalize_property(p):
    p = (p or '').strip()
    if p.isdigit():
        p = 'properties/' + p
    return p

def cmd_pull(argv):
    prop = None; days = 28; blog_prefix = '/journal/'
    i = 0
    while i < len(argv):
        if argv[i] == '--property' and i + 1 < len(argv): prop = argv[i+1]; i += 2
        elif argv[i] == '--days' and i + 1 < len(argv): days = int(argv[i+1]); i += 2
        elif argv[i] == '--blog-prefix' and i + 1 < len(argv): blog_prefix = argv[i+1]; i += 2
        else: i += 1
    if not prop and os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, encoding='utf-8') as f:
            prop = json.load(f).get('property_id')
    prop = normalize_property(prop)
    if not prop.startswith('properties/'):
        sys.exit('Podaj właściwość GA4: --property properties/NNN (wartość z komendy `properties`) '
                 'albo utwórz scripts/ga4/ga4.config.json z {"property_id": "properties/NNN"}.')
    hdr = auth_header()

    end   = datetime.date.today() - datetime.timedelta(days=1)          # wczoraj (dzisiejsze dane są niepełne)
    start = end - datetime.timedelta(days=days - 1)
    s, e = start.isoformat(), end.isoformat()
    today = datetime.date.today().isoformat()
    out = os.path.join(OUT_BASE, today)
    os.makedirs(out, exist_ok=True)
    print(f'Właściwość: {prop}\nZakres: {s} ... {e} ({days} dni)\nKatalog wyjściowy: {out}\n')

    dr = [{'startDate': s, 'endDate': e}]
    def dims(*names): return [{'name': n} for n in names]
    def mets(*names): return [{'name': n} for n in names]
    core = ('sessions', 'activeUsers', 'newUsers', 'screenPageViews', 'engagementRate', 'averageSessionDuration')
    by_sessions = [{'metric': {'metricName': 'sessions'}, 'desc': True}]
    key_events = [['keyEvents'], ['conversions']]   # keyEvents to nowa nazwa; conversions jako starszy wariant

    jobs = [
        ('overview_by_date.csv', {'dimensions': dims('date'), 'metrics': mets(*core),
                                  'orderBys': [{'dimension': {'dimensionName': 'date'}}]}, [], True),
        ('landing_pages.csv',    {'dimensions': dims('landingPage'),
                                  'metrics': mets('sessions', 'activeUsers', 'engagementRate'),
                                  'orderBys': by_sessions, 'limit': 500}, key_events, False),
        ('channels.csv',         {'dimensions': dims('sessionDefaultChannelGroup'),
                                  'metrics': mets('sessions', 'activeUsers', 'newUsers', 'engagementRate'),
                                  'orderBys': by_sessions}, key_events, True),
        ('source_medium.csv',    {'dimensions': dims('sessionSource', 'sessionMedium'),
                                  'metrics': mets('sessions', 'activeUsers', 'newUsers', 'engagementRate'),
                                  'orderBys': by_sessions}, key_events, True),
        ('countries.csv',        {'dimensions': dims('country'),
                                  'metrics': mets('sessions', 'activeUsers', 'newUsers', 'engagementRate'),
                                  'orderBys': by_sessions}, [], True),
        ('devices.csv',          {'dimensions': dims('deviceCategory'),
                                  'metrics': mets('sessions', 'activeUsers', 'newUsers', 'engagementRate',
                                                  'averageSessionDuration'),
                                  'orderBys': by_sessions}, [], True),
        ('blog_pages.csv',       {'dimensions': dims('pagePath'),
                                  'metrics': mets('screenPageViews', 'activeUsers', 'sessions', 'engagementRate',
                                                  'userEngagementDuration'),
                                  'dimensionFilter': {'filter': {'fieldName': 'pagePath',
                                                                 'stringFilter': {'matchType': 'BEGINS_WITH',
                                                                                  'value': blog_prefix}}},
                                  'orderBys': [{'metric': {'metricName': 'screenPageViews'}, 'desc': True}]},
         [], True),
    ]

    summary = {'property': prop, 'startDate': s, 'endDate': e, 'days': days, 'pulledOn': today,
               'blogPrefix': blog_prefix, 'rows': {}}
    for fname, body, optional, paginate in jobs:
        body = dict(body); body['dateRanges'] = dr
        print(f'  pobieram {fname} ...', end=' ', flush=True)
        headers, rows = run_report_with_fallback(prop, hdr, body, optional, paginate)
        write_csv(os.path.join(out, fname), headers, rows)
        summary['rows'][fname] = len(rows)
        print(f'{len(rows)} wierszy')

    # sumy zbiorcze (bez wymiarów)
    headers, rows = run_report_with_fallback(prop, hdr, {'dateRanges': dr, 'metrics': mets(*core)}, key_events, False)
    if rows:
        summary['totals'] = dict(zip(headers, rows[0]))
    with open(os.path.join(out, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print('\nGotowe. Podsumowanie:')
    print(json.dumps(summary, ensure_ascii=False, indent=2))


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if   cmd == 'auth':       cmd_auth()
    elif cmd == 'properties': cmd_properties()
    elif cmd == 'pull':       cmd_pull(sys.argv[2:])
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
