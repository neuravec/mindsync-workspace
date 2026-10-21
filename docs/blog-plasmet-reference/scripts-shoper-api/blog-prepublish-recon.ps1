# Shoper webapi REST - ROZEZNANIE PRZED PUBLIKACJA wpisu #1 - TYLKO ODCZYT (GET)
# Cel: zebrac dane do podmiany linkow (kategorie produktowe + permalinki) oraz do idempotencji publikacji
#      (czy wpis o tym 'name' juz istnieje, stan news-categories, stan news-tags).
# ZERO POST/PUT/DELETE. Bezpieczenstwo: NIE wypisuje loginu/hasla/tokenu.
# Uruchom:  powershell -ExecutionPolicy Bypass -File .\blog-prepublish-recon.ps1

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$envPath = Join-Path $PSScriptRoot '.env'
if (-not (Test-Path $envPath)) { throw "Brak .env" }
$cfg = @{}
Get-Content $envPath | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
    $parts = $_ -split '=', 2
    $cfg[$parts[0].Trim()] = $parts[1].Trim().Trim('"')
}
$url   = ($cfg['SHOPER_URL']).TrimEnd('/')
$login = $cfg['SHOPER_LOGIN']
$pass  = $cfg['SHOPER_PASSWORD']
$permToken = $cfg['SHOPER_TOKEN']

if ($permToken) {
    $token = $permToken
    Write-Host "AUTH: token permanentny z .env (zredagowany)" -ForegroundColor Green
} else {
    $basic = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($login):$($pass)"))
    $auth = Invoke-RestMethod -Method Post -Uri "$url/webapi/rest/auth" -Headers @{ Authorization = "Basic $basic" }
    $token = $auth.access_token
    if (-not $token) { throw "Brak tokenu" }
    Write-Host "AUTH OK (token zredagowany, wazny $($auth.expires_in)s)" -ForegroundColor Green
}
$hdr = @{ Authorization = "Bearer $token" }
$sleepMs = 300

function Invoke-Get($path) {
    try {
        $r = Invoke-RestMethod -Method Get -Uri "$url/webapi/rest/$path" -Headers $hdr
        Start-Sleep -Milliseconds $sleepMs
        return $r
    } catch {
        $code = $null; try { $code = [int]$_.Exception.Response.StatusCode } catch {}
        Write-Host "  BLAD GET $path : HTTP $code" -ForegroundColor Red
        return $null
    }
}

# ===== 1. KATEGORIE PRODUKTOWE (plaski) - szukamy 'wiertarko-wkretarki', 'elektronarzedzia', 'Milwaukee' =====
Write-Host "`n[1] categories (plaski) - nazwa + permalink" -ForegroundColor Cyan
$page = 1; $allCats = @()
do {
    $c = Invoke-Get "categories?limit=50&page=$page"
    if (-not $c) { break }
    if ($c.list) { $allCats += $c.list }
    $pages = [int]$c.pages
    $page++
} while ($page -le $pages)
Write-Host "  Pobrano kategorii: $($allCats.Count)" -ForegroundColor Green
foreach ($cat in $allCats) {
    $nm = $cat.translations.pl_PL.name
    $pl = $cat.translations.pl_PL.permalink
    Write-Host ("  id={0,-4} name='{1}'  perm={2}" -f $cat.category_id, $nm, $pl)
}

# ===== 2. PRODUCENCI - szukamy Milwaukee =====
Write-Host "`n[2] producers - nazwa + permalink (szukamy Milwaukee)" -ForegroundColor Cyan
$prod = Invoke-Get "producers?limit=50&page=1"
if ($prod -and $prod.list) {
    foreach ($p in $prod.list) {
        $nm = $p.translations.pl_PL.name; if (-not $nm) { $nm = $p.name }
        $pl = $p.translations.pl_PL.permalink
        Write-Host ("  id={0,-4} name='{1}'  perm={2}" -f $p.producer_id, $nm, $pl)
    }
} else { Write-Host "  brak/zero producentow" -ForegroundColor DarkGray }

# ===== 3. NEWS - idempotencja po name =====
# tytul czytamy z pliku kolejki (UTF-8), zeby nie wpisywac polskich znakow w kod skryptu
$queuePath = Join-Path $PSScriptRoot '..\..\blog\queue\01-jak-wybrac-wiertarko-wkretarke.json'
$queueObj  = Get-Content $queuePath -Raw -Encoding UTF8 | ConvertFrom-Json
$TITLE = $queueObj.tytul
Write-Host "`n[3] news - czy wpis o tytule juz istnieje (idempotencja)" -ForegroundColor Cyan
$page = 1; $allNews = @(); $pages = 1
do {
    $n = Invoke-Get "news?limit=50&page=$page"
    if (-not $n) { break }
    if ($n.list) { $allNews += $n.list }
    $pages = [int]$n.pages
    $page++
} while ($page -le $pages)
Write-Host "  count news: $($allNews.Count)" -ForegroundColor Green
$existing = $allNews | Where-Object { $_.name -eq $TITLE }
if ($existing) {
    Write-Host "  !!! ISTNIEJE wpis o tym tytule: news_id=$($existing.news_id) active=$($existing.active)" -ForegroundColor Yellow
} else {
    Write-Host "  brak wpisu o tym tytule - mozna tworzyc nowy" -ForegroundColor Green
}

# ===== 4. NEWS-CATEGORIES - szukamy Poradnik/Porady =====
Write-Host "`n[4] news-categories" -ForegroundColor Cyan
$ncat = Invoke-Get "news-categories?limit=50&page=1"
if ($ncat -and $ncat.list) {
    foreach ($nc in $ncat.list) {
        $nm = $nc.name; if (-not $nm) { $nm = $nc.translations.pl_PL.name }
        Write-Host ("  category_id={0,-4} name='{1}' active={2}" -f $nc.category_id, $nm, $nc.active)
    }
} else { Write-Host "  brak kategorii bloga" -ForegroundColor DarkGray }

# ===== 5. NEWS-TAGS - do find-or-create =====
Write-Host "`n[5] news-tags (do find-or-create)" -ForegroundColor Cyan
$ntag = Invoke-Get "news-tags?limit=100&page=1"
if ($ntag -and $ntag.list) {
    foreach ($t in $ntag.list) {
        $nm = $t.name; if (-not $nm) { $nm = $t.translations.pl_PL.name }
        Write-Host ("  tag_id={0,-4} name='{1}'" -f $t.tag_id, $nm)
    }
} else { Write-Host "  brak tagow" -ForegroundColor DarkGray }

Write-Host "`nROZEZNANIE GOTOWE (TYLKO ODCZYT)." -ForegroundColor Green
