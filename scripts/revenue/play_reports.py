#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Google Play: raporty finansowe i statystyki z bucketu Cloud Storage Play Console (tylko odczyt).

Raporty Play istnieją wyłącznie jako pliki w buckecie pubsite_prod_rev_<ID> (albo pubsite_prod_<ID>):
    earnings/earnings_RRRRMM_*.zip, sales/salesreport_RRRRMM.zip,
    financial-stats/subscriptions/..., stats/installs/...
Autoryzacja: konto serwisowe (JSON), zakres devstorage.read_only, czyste REST storage.googleapis.com.
Konfiguracja w scripts/revenue/.env (wzór: .env.example):
    PLAY_SERVICE_ACCOUNT_JSON (domyślnie scripts/revenue/play-service-account.json)
    PLAY_DEVELOPER_ID          (numer konta dewelopera, bucket = pubsite_prod_rev_<ID>)
    PLAY_BUCKET                (opcjonalnie: pełna nazwa bucketu albo gs://... z "Copy Cloud Storage URI"; ma pierwszeństwo)
Zależności: pip install --user google-auth requests

Komendy:
    python scripts/revenue/play_reports.py check                          # pierwsze 20 obiektów w buckecie
    python scripts/revenue/play_reports.py list [--prefix earnings/]
    python scripts/revenue/play_reports.py pull --month 2026-09 [--kinds earnings,sales,subscriptions,installs]

Wynik: analytics-reports/raw/revenue/play/RRRR-MM/<rodzaj>/ (pliki, rozpakowane zip, kopie *.utf8.csv)
"""
import sys, os, json, zipfile, datetime
import urllib.parse

HERE     = os.path.dirname(os.path.abspath(__file__))
ROOT     = os.path.abspath(os.path.join(HERE, '..', '..'))
ENV_FILE = os.path.join(HERE, '.env')
OUT_BASE = os.path.join(ROOT, 'analytics-reports', 'raw', 'revenue', 'play')
SCOPE    = 'https://www.googleapis.com/auth/devstorage.read_only'
GCS      = 'https://storage.googleapis.com/storage/v1'

KIND_PREFIX = {
    'earnings':      'earnings/',
    'sales':         'sales/',
    'subscriptions': 'financial-stats/subscriptions/',
    'installs':      'stats/installs/',
}

for _s in (sys.stdout, sys.stderr):
    try: _s.reconfigure(errors='replace')
    except Exception: pass


# ---------- .env (mini parser bez python-dotenv) ----------
def load_env(path=ENV_FILE):
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

def resolve_path(p):
    if os.path.isabs(p):
        return p
    for base in (HERE, ROOT, os.getcwd()):
        cand = os.path.abspath(os.path.join(base, p))
        if os.path.exists(cand):
            return cand
    return os.path.abspath(os.path.join(HERE, p))

def env_hint():
    return 'scripts/revenue/.env' if os.path.exists(ENV_FILE) else \
        'scripts/revenue/.env (plik nie istnieje, skopiuj .env.example jako .env)'

def bucket_name():
    b = os.environ.get('PLAY_BUCKET', '').strip()
    if b:
        if b.startswith('gs://'):
            b = b[5:]
        return b.strip('/').split('/')[0]
    dev = os.environ.get('PLAY_DEVELOPER_ID', '').strip()
    if not dev:
        sys.exit(f'Brak wartości: PLAY_DEVELOPER_ID (albo PLAY_BUCKET). Uzupełnij w {env_hint()}. '
                 'Instrukcja: scripts/revenue/README.md')
    return f'pubsite_prod_rev_{dev}'


# ---------- autoryzacja ----------
_session = None
def session():
    """requests.Session z tokenem konta serwisowego (google-auth robi wymianę JWT -> access token)."""
    global _session
    if _session is not None:
        return _session
    sa_path = resolve_path(os.environ.get('PLAY_SERVICE_ACCOUNT_JSON', '').strip() or 'play-service-account.json')
    if not os.path.exists(sa_path):
        sys.exit(f'Brak pliku klucza konta serwisowego: {sa_path}\n'
                 'Utwórz klucz JSON (Google Cloud -> IAM -> Service accounts -> Keys) i zapisz go jako '
                 'scripts/revenue/play-service-account.json albo ustaw PLAY_SERVICE_ACCOUNT_JSON w .env.')
    try:
        import requests
        from google.oauth2 import service_account
        from google.auth.transport.requests import Request
    except ImportError:
        sys.exit('Brak bibliotek google-auth / requests. Zainstaluj: pip install --user google-auth requests')
    try:
        creds = service_account.Credentials.from_service_account_file(sa_path, scopes=[SCOPE])
        creds.refresh(Request())
    except ValueError as e:
        sys.exit(f'Plik {os.path.basename(sa_path)} nie wygląda na klucz konta serwisowego ({e}).')
    except Exception as e:
        sys.exit(f'Nie udało się uzyskać tokenu dla konta serwisowego ({type(e).__name__}). '
                 'Sprawdź, czy klucz nie został usunięty w Google Cloud i czy jest dostęp do sieci.')
    s = requests.Session()
    s.headers['Authorization'] = 'Bearer ' + creds.token
    s._sa_email = getattr(creds, 'service_account_email', '?')
    _session = s
    return s

def fail_http(resp, what, bucket):
    detail = ' '.join((resp.text or '').split())[:400]
    if resp.status_code == 403:
        email = getattr(session(), '_sa_email', '?')
        sys.exit(f'HTTP 403 przy {what}: konto serwisowe {email} nie ma dostępu do bucketu {bucket}.\n'
                 'Najczęstsze przyczyny:\n'
                 '  1) konto serwisowe nie zostało zaproszone w Play Console (Users and permissions) z uprawnieniami '
                 '"View financial data" oraz "View app information";\n'
                 '  2) zaproszenie wysłano niedawno: uprawnienia do bucketu propagują się nawet do ~24 h;\n'
                 '  3) zła nazwa bucketu: skopiuj ją z Play Console -> Download reports -> "Copy Cloud Storage URI" '
                 'i wpisz do PLAY_BUCKET.\n' + detail)
    if resp.status_code == 404:
        sys.exit(f'HTTP 404 przy {what}: bucket {bucket} nie istnieje. Skopiuj właściwy adres z Play Console '
                 '-> Download reports -> "Copy Cloud Storage URI" i wpisz go do PLAY_BUCKET w .env.\n' + detail)
    if resp.status_code == 401:
        sys.exit(f'HTTP 401 przy {what}: token konta serwisowego odrzucony.\n' + detail)
    sys.exit(f'HTTP {resp.status_code} przy {what}: {detail}')


# ---------- GCS REST ----------
def list_objects(bucket, prefix='', limit=None):
    s = session()
    out, token = [], None
    while True:
        params = {'prefix': prefix, 'fields': 'items(name,size,updated),nextPageToken',
                  'maxResults': min(limit, 1000) if limit else 1000}
        if token: params['pageToken'] = token
        r = s.get(f'{GCS}/b/{urllib.parse.quote(bucket, safe="")}/o', params=params, timeout=120)
        if r.status_code != 200:
            fail_http(r, 'listowaniu obiektów', bucket)
        data = r.json()
        out.extend(data.get('items', []))
        token = data.get('nextPageToken')
        if not token or (limit and len(out) >= limit):
            break
    return out[:limit] if limit else out

def download(bucket, name, dest):
    s = session()
    url = f'{GCS}/b/{urllib.parse.quote(bucket, safe="")}/o/{urllib.parse.quote(name, safe="")}'
    with s.get(url, params={'alt': 'media'}, stream=True, timeout=300) as r:
        if r.status_code != 200:
            fail_http(r, f'pobieraniu {name}', bucket)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f:
            for chunk in r.iter_content(1 << 16):
                f.write(chunk)


# ---------- pliki ----------
def to_utf8_copy(path):
    """Play CSV bywają w UTF-16LE (z BOM). Tworzy obok kopię <nazwa>.utf8.csv; zwraca jej ścieżkę albo None."""
    with open(path, 'rb') as f:
        raw = f.read()
    if raw.startswith(b'\xff\xfe') or raw.startswith(b'\xfe\xff'):
        text = raw.decode('utf-16')
    elif len(raw) >= 4 and raw[1:2] == b'\x00' and raw[3:4] == b'\x00':
        text = raw.decode('utf-16-le')        # UTF-16LE bez BOM (heurystyka: co drugi bajt zerowy)
    else:
        return None                           # już UTF-8 / ASCII, nic nie trzeba robić
    base, _ = os.path.splitext(path)
    dest = base + '.utf8.csv'
    with open(dest, 'w', encoding='utf-8-sig', newline='') as f:
        f.write(text.replace('\r\n', '\n').replace('\r', '\n'))
    return dest

def safe_unzip(zpath, dest_dir):
    """Rozpakowuje zip, odrzucając ścieżki wychodzące poza katalog docelowy."""
    extracted = []
    root = os.path.abspath(dest_dir)
    with zipfile.ZipFile(zpath) as z:
        for m in z.infolist():
            if m.is_dir():
                continue
            target = os.path.abspath(os.path.join(root, m.filename))
            if not target.startswith(root + os.sep):
                print(f'    pomijam podejrzaną ścieżkę w zip: {m.filename}')
                continue
            os.makedirs(os.path.dirname(target), exist_ok=True)
            with z.open(m) as src, open(target, 'wb') as dst:
                dst.write(src.read())
            extracted.append(target)
    return extracted

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

def fmt_size(n):
    n = int(n or 0)
    return f'{n/1048576:.1f} MB' if n >= 1048576 else f'{n/1024:.1f} KB'


# ---------- komendy ----------
def cmd_check():
    bucket = bucket_name()
    items = list_objects(bucket, limit=20)
    print(f'Dostęp do gs://{bucket} działa. Pierwsze {len(items)} obiektów:')
    for it in items:
        print(f"  {fmt_size(it.get('size')):>10}  {it.get('updated', '')[:10]}  {it['name']}")
    if not items:
        print('  (bucket pusty: nowe konta dostają raporty dopiero po pierwszym miesiącu aktywności)')

def cmd_list(argv):
    opts = parse_args(argv)
    bucket = bucket_name()
    prefix = opts.get('prefix') if isinstance(opts.get('prefix'), str) else ''
    items = list_objects(bucket, prefix=prefix)
    for it in items:
        print(f"  {fmt_size(it.get('size')):>10}  {it.get('updated', '')[:10]}  {it['name']}")
    print(f'Razem: {len(items)} obiektów (prefiks: "{prefix}")')

def cmd_pull(argv):
    opts = parse_args(argv)
    month = opts.get('month')
    if not isinstance(month, str):
        sys.exit('Podaj miesiąc: --month RRRR-MM')
    try:
        datetime.datetime.strptime(month, '%Y-%m')
    except ValueError:
        sys.exit(f'Zły format --month: "{month}". Oczekiwany: RRRR-MM')
    kinds = (opts.get('kinds') if isinstance(opts.get('kinds'), str) else ','.join(KIND_PREFIX)).split(',')
    kinds = [k.strip() for k in kinds if k.strip()]
    bad = [k for k in kinds if k not in KIND_PREFIX]
    if bad:
        sys.exit(f'Nieznany rodzaj: {", ".join(bad)}. Dozwolone: {", ".join(KIND_PREFIX)}')
    bucket = bucket_name()
    yyyymm = month.replace('-', '')
    out_month = os.path.join(OUT_BASE, month)
    print(f'Bucket: gs://{bucket}\nMiesiąc: {month}\nKatalog wyjściowy: {out_month}\n')

    summary = {'bucket': bucket, 'month': month, 'pulledOn': datetime.date.today().isoformat(), 'files': {}}
    for kind in kinds:
        prefix = KIND_PREFIX[kind]
        items = [it for it in list_objects(bucket, prefix=prefix)
                 if yyyymm in os.path.basename(it['name'])]
        print(f'  {kind}: {len(items)} plików z {yyyymm} (prefiks {prefix})')
        summary['files'][kind] = []
        for it in items:
            name = it['name']
            dest = os.path.join(out_month, kind, os.path.basename(name))
            download(bucket, name, dest)
            summary['files'][kind].append(name)
            print(f'    pobrano {name} ({fmt_size(it.get("size"))})')
            produced = [dest]
            if dest.lower().endswith('.zip'):
                produced = safe_unzip(dest, os.path.dirname(dest))
                for p in produced:
                    print(f'      rozpakowano {os.path.basename(p)}')
            for p in produced:
                if p.lower().endswith('.csv') and not p.lower().endswith('.utf8.csv'):
                    conv = to_utf8_copy(p)
                    if conv:
                        print(f'      UTF-16 -> UTF-8: {os.path.basename(conv)}')
        if not items:
            print(f'    (brak plików: raport za {month} mógł jeszcze nie powstać albo ten rodzaj nie dotyczy konta)')
    os.makedirs(out_month, exist_ok=True)
    with open(os.path.join(out_month, 'summary.json'), 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    print('\nGotowe.')


def main():
    load_env()
    cmd = sys.argv[1] if len(sys.argv) > 1 else ''
    if   cmd == 'check': cmd_check()
    elif cmd == 'list':  cmd_list(sys.argv[2:])
    elif cmd == 'pull':  cmd_pull(sys.argv[2:])
    else:
        print(__doc__)

if __name__ == '__main__':
    main()
