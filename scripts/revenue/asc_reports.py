#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
App Store Connect: raporty sprzedaży, subskrypcji i finansowe (tylko odczyt).

Autoryzacja: klucz App Store Connect API (.p8), token JWT ES256 (aud appstoreconnect-v1, ważny 20 min).
Konfiguracja w scripts/revenue/.env (wzór: .env.example):
    ASC_ISSUER_ID, ASC_KEY_ID, ASC_PRIVATE_KEY_PATH (domyślnie scripts/revenue/AuthKey_<KEY_ID>.p8), ASC_VENDOR_NUMBER
Zależność: pip install --user "pyjwt[crypto]"

Komendy:
    python scripts/revenue/asc_reports.py check
    python scripts/revenue/asc_reports.py sales --date 2026-10-20                 # dzienny (DAILY)
    python scripts/revenue/asc_reports.py sales --month 2026-09                   # miesięczny (MONTHLY)
    python scripts/revenue/asc_reports.py sales --date 2026-10-19 --frequency WEEKLY   # data = niedziela kończąca tydzień
    python scripts/revenue/asc_reports.py subscriptions --date 2026-10-20         # tylko DAILY
    python scripts/revenue/asc_reports.py finance --month 2026-09 [--region ZZ] [--type FINANCIAL|FINANCE_DETAIL]
    Opcjonalnie dla sales/subscriptions: --version 1_0 / 1_3 (nadpisuje domyślną wersję raportu)

Wynik: analytics-reports/raw/revenue/asc/<sales|subscriptions|finance>/  (surowy .tsv + przetworzony .csv)
Bez --date/--month komendy sales i subscriptions biorą przedwczorajszy dzień (raport dzienny bywa gotowy dopiero następnego dnia).
"""
import sys, os, csv, json, gzip, time, datetime, io
import urllib.parse, urllib.request, urllib.error

HERE     = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.abspath(os.path.join(HERE, '..', '..'))
ENV_FILE = os.path.join(HERE, '.env')
OUT_BASE = os.path.join(ROOT, 'analytics-reports', 'raw', 'revenue', 'asc')
API      = 'https://api.appstoreconnect.apple.com'

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(errors='replace')
    except Exception: pass


# ---------- .env (mini parser bez python-dotenv) ----------
def load_env(path=ENV_FILE):
    """KEY=VALUE, komentarze '#', opcjonalne cudzysłowy. Zmienne już ustawione w systemie mają pierwszeństwo."""
    if not os.path.exists(path):
        return False
    with open(path, encoding='utf-8-sig') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('#') or '=' not in line:
                continue
            k, v = line.split('=', 1)
            k, v = k.strip(), v.strip()
            if k.startswith('export '):
                k = k[7:].strip()
            if len(v) >= 2 and v[0] == v[-1] and v[0] in '"\'':
                v = v[1:-1]
            elif ' #' in v:
                v = v.split(' #', 1)[0].rstrip()
            os.environ.setdefault(k, v)
    return True

def require_env(*keys):
    missing = [k for k in keys if not os.environ.get(k, '').strip()]
    if missing:
        where = 'scripts/revenue/.env' if os.path.exists(ENV_FILE) else 'scripts/revenue/.env (plik nie istnieje, skopiuj .env.example jako .env)'
        sys.exit(f'Brak wartości: {", ".join(missing)}. Uzupełnij je w {where}. Instrukcja: scripts/revenue/README.md')
    return [os.environ[k].strip() for k in keys]

def resolve_path(p):
    if os.path.isabs(p):
        return p
    for base in (HERE, ROOT, os.getcwd()):
        cand = os.path.abspath(os.path.join(base, p))
        if os.path.exists(cand):
            return cand
    return os.path.abspath(os.path.join(HERE, p))


# ---------- JWT ----------
def make_token():
    issuer, key_id = require_env('ASC_ISSUER_ID', 'ASC_KEY_ID')
    key_path = resolve_path(os.environ.get('ASC_PRIVATE_KEY_PATH', '').strip() or f'AuthKey_{key_id}.p8')
    if not os.path.exists(key_path):
        # Nie wypisuj wartości, jeśli ktoś wkleił w ASC_PRIVATE_KEY_PATH treść klucza zamiast ścieżki.
        shown = key_path if key_path.lower().endswith('.p8') else '(ASC_PRIVATE_KEY_PATH nie wygląda na ścieżkę do pliku .p8, wpisz ścieżkę albo zostaw puste)'
        sys.exit(f'Brak pliku klucza .p8: {shown}\n'
                 'Pobierz go z App Store Connect (Users and Access -> Integrations -> App Store Connect API) '
                 'i zapisz w scripts/revenue/ albo ustaw ASC_PRIVATE_KEY_PATH w .env.')
    try:
        import jwt  # PyJWT
    except ImportError:
        sys.exit('Brak biblioteki PyJWT. Zainstaluj: pip install --user "pyjwt[crypto]"')
    with open(key_path, encoding='utf-8') as f:
        private_key = f.read()
    now = int(time.time())
    payload = {'iss': issuer, 'iat': now, 'exp': now + 19 * 60, 'aud': 'appstoreconnect-v1'}   # Apple: maks. 20 min
    try:
        tok = jwt.encode(payload, private_key, algorithm='ES256', headers={'kid': key_id, 'typ': 'JWT'})
    except NotImplementedError:
        sys.exit('PyJWT bez obsługi ES256. Zainstaluj z dodatkiem crypto: pip install --user "pyjwt[crypto]"')
    except Exception as e:
        sys.exit(f'Nie udało się podpisać JWT kluczem {os.path.basename(key_path)} ({type(e).__name__}). '
                 'Czy to na pewno oryginalny plik .p8 z App Store Connect?')
    return tok if isinstance(tok, str) else tok.decode()


# ---------- HTTP ----------
class AscHttpError(Exception):
    def __init__(self, code, url, detail):
        super().__init__(f'HTTP {code}')
        self.code, self.url, self.detail = code, url, detail

def api_get(path, params=None, accept='application/json'):
    url = API + path + ('?' + urllib.parse.urlencode(params) if params else '')
    req = urllib.request.Request(url, headers={'Authorization': 'Bearer ' + make_token(), 'Accept': accept})
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            return r.read(), r.headers.get('Content-Type', '')
    except urllib.error.HTTPError as e:
        raise AscHttpError(e.code, url, e.read().decode('utf-8', errors='replace'))
    except urllib.error.URLError as e:
        sys.exit(f'Błąd sieci przy {API}: {e.reason}')

def error_text(e):
    try:
        errs = json.loads(e.detail).get('errors', [])
        return '; '.join(f"{x.get('code', '')}: {x.get('detail') or x.get('title', '')}" for x in errs) or e.detail[:400]
    except Exception:
        return ' '.join((e.detail or '').split())[:400]

def fail_http(e, what):
    txt = error_text(e)
    if e.code == 401:
        sys.exit(f'HTTP 401 przy {what}: Apple odrzucił token. Sprawdź ASC_ISSUER_ID, ASC_KEY_ID, czy klucz .p8 '
                 f'pasuje do Key ID, czy klucz nie został cofnięty i czy zegar systemowy jest poprawny.\n{txt}')
    if e.code == 403:
        sys.exit(f'HTTP 403 przy {what}: klucz API nie ma uprawnień. Raporty wymagają roli Finance '
                 f'(finanse) lub Sales (sprzedaż) przy kluczu zespołowym.\n{txt}')
    sys.exit(f'HTTP {e.code} przy {what}: {txt}')


# ---------- zapis raportów ----------
def save_report(raw_bytes, kind, stem):
    out = os.path.join(OUT_BASE, kind)
    os.makedirs(out, exist_ok=True)
    try:
        data = gzip.decompress(raw_bytes)
    except OSError:
        data = raw_bytes   # na wypadek gdyby odpowiedź nie była spakowana
    text = data.decode('utf-8-sig', errors='replace')
    tsv_path = os.path.join(out, stem + '.tsv')
    with open(tsv_path, 'w', encoding='utf-8', newline='') as f:
        f.write(text)
    csv_path = os.path.join(out, stem + '.csv')
    rows = list(csv.reader(io.StringIO(text), delimiter='\t'))
    with open(csv_path, 'w', encoding='utf-8-sig', newline='') as f:
        csv.writer(f).writerows(rows)
    data_rows = max(len([r for r in rows if any(c.strip() for c in r)]) - 1, 0)
    print(f'Zapisano:\n  {tsv_path}\n  {csv_path}\n  wierszy danych (bez nagłówka): {data_rows}')


def parse_args(argv):
    opts = {}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a.startswith('--') and i + 1 < len(argv) and not argv[i+1].startswith('--'):
            opts[a[2:]] = argv[i+1]; i += 2
        else:
            opts[a.lstrip('-')] = True; i += 1
    return opts

def check_date(s, fmt, label):
    try:
        datetime.datetime.strptime(s, fmt)
    except ValueError:
        sys.exit(f'Zły format {label}: "{s}". Oczekiwany: {fmt.replace("%Y", "RRRR").replace("%m", "MM").replace("%d", "DD")}')


# ---------- komendy ----------
def cmd_check():
    require_env('ASC_ISSUER_ID', 'ASC_KEY_ID')
    try:
        body, _ = api_get('/v1/apps', {'limit': 5, 'fields[apps]': 'name,bundleId'})
    except AscHttpError as e:
        fail_http(e, 'GET /v1/apps')
    apps = json.loads(body).get('data', [])
    print('Klucz API działa. Aplikacje (do 5):')
    for a in apps:
        at = a.get('attributes', {})
        print(f"  {a.get('id', ''):12} {at.get('name', '')}  ({at.get('bundleId', '')})")
    if not apps:
        print('  (brak aplikacji widocznych dla tego klucza)')
    if not os.environ.get('ASC_VENDOR_NUMBER', '').strip():
        print('UWAGA: brak ASC_VENDOR_NUMBER w .env, bez niego sales/subscriptions/finance nie zadziałają.')

def cmd_sales(argv, report_type):
    opts = parse_args(argv)
    vendor = require_env('ASC_ISSUER_ID', 'ASC_KEY_ID', 'ASC_VENDOR_NUMBER')[2]
    if report_type == 'SUBSCRIPTION':
        kind, subtype, version = 'subscriptions', 'SUMMARY', opts.get('version', '1_3')
    else:
        # 2026-10-22: Apple odrzuca 1_1 dla SALES/SUMMARY ("latest version for this report is 1_0")
        kind, subtype, version = 'sales', 'SUMMARY', opts.get('version', '1_0')

    if isinstance(opts.get('month'), str):
        check_date(opts['month'], '%Y-%m', '--month')
        report_date, freq = opts['month'], 'MONTHLY'
    else:
        report_date = opts.get('date') if isinstance(opts.get('date'), str) else \
            (datetime.date.today() - datetime.timedelta(days=2)).isoformat()
        check_date(report_date, '%Y-%m-%d', '--date')
        freq = 'DAILY'
    if isinstance(opts.get('frequency'), str):
        freq = opts['frequency'].upper()
    if freq not in ('DAILY', 'WEEKLY', 'MONTHLY', 'YEARLY'):
        sys.exit('--frequency musi być jednym z: DAILY, WEEKLY, MONTHLY, YEARLY')
    if report_type == 'SUBSCRIPTION' and freq != 'DAILY':
        sys.exit('Raport SUBSCRIPTION jest dostępny tylko dziennie: użyj --date RRRR-MM-DD.')
    if freq == 'MONTHLY' and len(report_date) == 10:
        report_date = report_date[:7]
    if freq == 'YEARLY':
        report_date = report_date[:4]

    params = {
        'filter[frequency]': freq, 'filter[reportType]': report_type, 'filter[reportSubType]': subtype,
        'filter[vendorNumber]': vendor, 'filter[reportDate]': report_date, 'filter[version]': version,
    }
    print(f'Pobieram {report_type}/{subtype} v{version}, {freq}, data {report_date} ...')
    try:
        body, _ = api_get('/v1/salesReports', params, accept='application/a-gzip')
    except AscHttpError as e:
        if e.code == 404:
            print(f'Brak raportu dla {report_date} ({freq}): {error_text(e)}\n'
                  'To normalne, jeśli tego dnia nie było sprzedaży albo raport jeszcze nie jest gotowy '
                  '(dzienne zwykle do rana czasu PT następnego dnia, miesięczne kilka dni po końcu miesiąca).')
            return
        fail_http(e, 'GET /v1/salesReports')
    save_report(body, kind, f'{report_type.lower()}_{subtype.lower()}_{freq.lower()}_{report_date}_v{version}')

def cmd_finance(argv):
    opts = parse_args(argv)
    vendor = require_env('ASC_ISSUER_ID', 'ASC_KEY_ID', 'ASC_VENDOR_NUMBER')[2]
    month = opts.get('month')
    if not isinstance(month, str):
        sys.exit('Podaj miesiąc fiskalny Apple: --month RRRR-MM')
    check_date(month, '%Y-%m', '--month')
    rtype = (opts.get('type') if isinstance(opts.get('type'), str) else 'FINANCIAL').upper()
    if rtype not in ('FINANCIAL', 'FINANCE_DETAIL'):
        sys.exit('--type musi być FINANCIAL albo FINANCE_DETAIL')
    region = opts.get('region') if isinstance(opts.get('region'), str) else ('Z1' if rtype == 'FINANCE_DETAIL' else 'ZZ')
    params = {'filter[regionCode]': region, 'filter[reportDate]': month,
              'filter[reportType]': rtype, 'filter[vendorNumber]': vendor}
    print(f'Pobieram {rtype}, region {region}, miesiąc fiskalny {month} ...')
    try:
        body, _ = api_get('/v1/financeReports', params, accept='application/a-gzip')
    except AscHttpError as e:
        if e.code == 404:
            print(f'Brak raportu finansowego dla {month} / {region}: {error_text(e)}\n'
                  'Raporty finansowe pojawiają się po zamknięciu miesiąca fiskalnego Apple (zwykle na początku '
                  'następnego miesiąca). Sprawdź kalendarz fiskalny w Payments and Financial Reports.')
            return
        fail_http(e, 'GET /v1/financeReports')
    save_report(body, 'finance', f'{rtype.lower()}_{region}_{month}')


def main():
    load_env()
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if   cmd == 'check':         cmd_check()
    elif cmd == 'sales':         cmd_sales(sys.argv[2:], 'SALES')
    elif cmd == 'subscriptions': cmd_sales(sys.argv[2:], 'SUBSCRIPTION')
    elif cmd == 'finance':       cmd_finance(sys.argv[2:])
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
