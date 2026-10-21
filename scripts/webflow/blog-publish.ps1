# =====================================================================================
#  blog-publish.ps1 - DRIP-PUBLISH wpisow bloga MindSync na WEBFLOW CMS (Data API v2)
# -------------------------------------------------------------------------------------
#  Adaptacja publikatora PLASMET (scripts referencyjne: docs/blog-plasmet-reference/).
#  Bierze NAJSTARSZY wpis o statusie `gotowy` z blog/queue/*.json, ktorego planowana_data
#  <= dzis, i publikuje go: bramki jakosci -> render kart [FEATURE:] -> upload hero jako
#  asset Webflow -> create/update item (idempotencja po slugu) -> publish item -> log.
#
#  !! DOMYSLNIE -DryRun = TRUE: buduje payload i pokazuje co BY zrobil, NIE wysyla zadnego
#     zapisu. Realna publikacja: jawnie -DryRun:$false (zmienia ZYWA strone mindsync.app).
#
#  Uruchom (podglad):  powershell -ExecutionPolicy Bypass -File .\blog-publish.ps1
#  Uruchom (LIVE):     powershell -ExecutionPolicy Bypass -File .\blog-publish.ps1 -DryRun:$false
#  Jeden konkretny:    ...\blog-publish.ps1 -Plik 2026-09-01_slug.json -DryRun:$false
#  TRYB DRIP (Task Scheduler, codziennie 07:00, 1 wpis/dzien):
#    powershell -NonInteractive -ExecutionPolicy Bypass -File .\blog-publish.ps1 -DripOne -DryRun:$false
#
#  Wymaga scripts/webflow/.env (wzor: .env.example): WEBFLOW_API_TOKEN (site token
#  z Webflow Site Settings -> Apps & Integrations), WEBFLOW_SITE_ID, WEBFLOW_COLLECTION_ID.
#
#  MAPOWANIE POL kolejki (blog/queue/_format.md) -> pola kolekcji Blog Posts:
#    tytul            -> name            | tresc_html      -> post-body (RichText-safe HTML!)
#    zajawka_html/txt -> post-summary    | seo_url         -> slug
#    meta_title       -> seo-title       | meta_description-> seo-description
#    hero (1600x900)  -> main-image      | hero (800x600)  -> thumbnail-image
#    hero_image_alt   -> hero-alt (+alt) | kategoria       -> category (mapa nazwa->option id)
#    featured         -> featured        | kolor           -> color
#    schema_jsonld    -> schema-jsonld (goly JSON, bez <script>; wrapper daje szablon)
#
#  BRAMKI dripu (kazda konczy sie POMINIECIEM wpisu, nie bledem):
#    1. surowe [LINK:...] w tresci             2. dlugi myslnik U+2014 w polach tekstowych
#    3. blad renderu kart [FEATURE:]/[FEATURES:] albo nierozwiazany placeholder
#    4. brak pliku hero na dysku               5. brak zajawki (post-summary)
#
#  KONTROLA ODKRYWANIA NOWYCH WPISOW (dodane 2026-09-22): po udanej publikacji, tuz PRZED
#  publikacja calej strony, skrypt sprawdza dwa kanaly, ktorymi Google znajduje nowe wpisy:
#  sekcje "Latest from the journal" na stronie glownej oraz lastmod strony /blog. Sekcji
#  na Home NIE DA SIE zapisac przez Data API, wiec przy rozjezdzie skrypt zostawia liste
#  do podmiany w _drip-log.txt. lastmod /blog odswieza (od 2026-09-25) przelaczeniem
#  wewnetrznej nazwy strony (dowody: sekcja "ODKRYWANIE NOWYCH WPISOW" nizej).
#  Wylacza to -SkipDiscoveryRefresh.
#
#  ZGLOSZENIE SITEMAPY W GSC (dodane 2026-09-25): po udanej publikacji calej strony skrypt
#  odczekuje chwile (Webflow przegenerowuje sitemap.xml) i wola
#  scripts/gsc/pull_gsc.py submit-sitemap, czyli odpowiednik GSC -> Sitemaps -> Submit.
#  Pomiar z 22.09: po takim zgloszeniu Google pobral sitemape w sekunde i zaindeksowal
#  7 wpisow w ~4 h, a sam z siebie nie pobiera jej od tygodnia. Wylacza -SkipGscSubmit.
#
#  PUBLIKACJA CALEJ STRONY PO WPISIE (dodane 2026-09-03): Webflow generuje sitemap.xml
#  wylacznie przy pelnej publikacji strony, wiec po udanej publikacji itemu skrypt wola
#  POST /sites/{id}/publish. Wylacza to przelacznik -SkipSitePublish.
#  UWAGA: pelna publikacja wypycha na zywo TAKZE niezapisane zmiany z Designera.
#  Szczegoly i dowody: sekcja "PUBLIKACJA CALEJ STRONY" nizej w tym pliku.
#
#  TRYBY DODANE 2026-10-21 (wszystkie z DryRun domyslnie, opis: sekcja "ODSWIEZANIE
#  OPUBLIKOWANYCH" nizej oraz scripts/webflow/README.md):
#    -Republish -Plik <plik> | -All   odswieza JUZ OPUBLIKOWANY wpis: PATCH istniejacego
#                                     itemu + publish item, bez publikacji calej strony
#    -Republish ... -BodyOnly         PATCH wylacznie post-body (np. podmiana zrzutow apki)
#    -Republish ... -KeepHero         pelny PATCH, ale main-image/thumbnail-image bez zmian
#    -UploadAssets <katalog>          wgrywa *.webp do Webflow Assets, mapa nazwa -> URL CDN
#                                     w <katalog>\_webflow-urls.json
# =====================================================================================

[CmdletBinding()]
param(
    [bool]   $DryRun = $true,                 # DOMYSLNIE bezpiecznie: tylko podglad
    [string] $Plik   = $null,                 # opcjonalnie: konkretny plik z kolejki
    [switch] $All,                            # wszystkie kwalifikujace sie (nie tylko 1)
    [switch] $DripOne,                        # TRYB DRIP (Task Scheduler): 1 wpis, nienadzorowany
    [switch] $SkipSitePublish,                # NIE publikuj calej strony po wpisie (sitemap.xml sie NIE odswiezy)
    [switch] $SkipDiscoveryRefresh,           # NIE sprawdzaj sekcji 'Latest from the journal' ani lastmod /blog
    [switch] $SkipGscSubmit,                  # NIE zglaszaj sitemapy w Google Search Console po publikacji strony
    [int]    $GscSubmitDelaySec = 20,         # ile czekac po publikacji strony, zanim zglosimy sitemape
    [int]    $ThrottleMs = 600,               # limit Webflow: 60 req/min -> ~1 req/s z zapasem
    [int]    $MaxRetry   = 5,                 # retry na 429/5xx (backoff wykladniczy + Retry-After)
    [int]    $WriteDeadlineSec = 60,          # twardy deadline zapisu/uploadu
    # --- tryby dodane 2026-10-21 (sekcja "ODSWIEZANIE OPUBLIKOWANYCH" nizej) ---
    [switch] $Republish,                      # odswiez JUZ OPUBLIKOWANE wpisy (z -Plik albo -All); bez publikacji calej strony
    [switch] $BodyOnly,                       # z -Republish: PATCH wylacznie pola post-body
    [switch] $KeepHero,                       # z -Republish: main-image i thumbnail-image zostaja bez zmian
    [int]    $ItemPauseSec = 3,               # z -Republish: przerwa miedzy wpisami (limit Webflow 60 req/min)
    [string] $UploadAssets = $null            # katalog: wgraj *.webp do Webflow Assets (mapa -> <katalog>\_webflow-urls.json)
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# --- sciezki logow OD RAZU z PSScriptRoot (musza istniec zanim cokolwiek moze rzucic) ---
$script:dripLogPath   = Join-Path $PSScriptRoot '_drip-log.txt'
$script:dripErrorPath = Join-Path $PSScriptRoot '_drip-error.txt'

# --- sciezki repo ---
$repoRoot   = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent   # ...\Heroku
$queueDir   = Join-Path $repoRoot 'blog\queue'
$imagesDir  = Join-Path $repoRoot 'blog\images'
$logPath    = Join-Path $repoRoot 'blog\published-log.json'
$featsPath  = Join-Path $repoRoot 'blog\app-features.json'

# --- stale Webflow (potwierdzone przez MCP 2026-08-25) ---
$script:ApiBase = 'https://api.webflow.com/v2'
$script:CategoryMap = @{                       # pole Option `category` w kolekcji Blog Posts
    'All'           = '7b64b596db0297db6abd52c266d54b08'
    'Therapy'       = '0093a31076e66408265a9d0907d028c2'
    'MindSync Tips' = '9b1d0f4d9dc03f001a8409e1fd7c29c6'
}
$script:DefaultColor = '#339499'               # brand mid teal (docs/blog/brand-mindsync.md)
$script:sitePublishNeeded = $false             # ustawiane po udanej publikacji wpisu (patrz Invoke-WfSitePublish)
$script:sitePublishOk     = $false             # ustawiane po udanym POST /sites/{id}/publish (warunek zgloszenia GSC)

# =====================================================================================
#  ODCZYT PLIKOW Z RETRY + HYDRATACJA (OneDrive Files On-Demand) - wzorzec z PLASMET
# =====================================================================================
$script:FileRetryBackoff = @(2, 5, 10)
function Read-FileBytesWithRetry {
    param([string]$Path, [string]$Etykieta = 'plik')
    $last = $null
    for ($i = 0; $i -lt $script:FileRetryBackoff.Count; $i++) {
        try {
            if (-not [IO.File]::Exists($Path)) { throw "nie istnieje: $Path" }
            $bytes = [IO.File]::ReadAllBytes($Path)
            if ($null -eq $bytes) { throw "odczyt zwrocil null: $Path" }
            return $bytes
        } catch {
            $last = $_
            $wait = $script:FileRetryBackoff[$i]
            Write-Host "  RETRY-FILE ($Etykieta) proba $($i+1): $($_.Exception.Message) -> backoff ${wait}s" -ForegroundColor Yellow
            Start-Sleep -Seconds $wait
        }
    }
    if (-not [IO.File]::Exists($Path)) { throw "Plik niedostepny po retry ($Etykieta): $Path :: $($last.Exception.Message)" }
    return [IO.File]::ReadAllBytes($Path)
}
function Read-TextWithRetry {
    param([string]$Path, [string]$Etykieta = 'plik')
    $bytes = Read-FileBytesWithRetry -Path $Path -Etykieta $Etykieta
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        return [Text.Encoding]::UTF8.GetString($bytes, 3, $bytes.Length - 3)   # wytnij BOM
    }
    return [Text.Encoding]::UTF8.GetString($bytes)
}

# =====================================================================================
#  ENV + AUTH (token statyczny Webflow; sekret TYLKO w .env)
# =====================================================================================
$script:envCfg = @{}; $script:token = $null; $script:siteId = $null; $script:collectionId = $null
function Initialize-Env {
    $envPath = Join-Path $PSScriptRoot '.env'
    $raw = Read-TextWithRetry -Path $envPath -Etykieta '.env'
    $script:envCfg = @{}
    $raw -split "`r?`n" | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
        $parts = $_ -split '=', 2
        $script:envCfg[$parts[0].Trim()] = $parts[1].Trim().Trim('"')
    }
    $script:token        = $script:envCfg['WEBFLOW_API_TOKEN']
    $script:siteId       = $script:envCfg['WEBFLOW_SITE_ID']
    $script:collectionId = $script:envCfg['WEBFLOW_COLLECTION_ID']
    if (-not $script:token)        { throw 'Brak WEBFLOW_API_TOKEN w scripts/webflow/.env' }
    if (-not $script:siteId)       { throw 'Brak WEBFLOW_SITE_ID w scripts/webflow/.env' }
    if (-not $script:collectionId) { throw 'Brak WEBFLOW_COLLECTION_ID w scripts/webflow/.env' }
    Write-Host "AUTH: token Webflow z .env (zredagowany), site=$($script:siteId)" -ForegroundColor Green
}

# =====================================================================================
#  WRAPPER API: throttling + retry/backoff (429 z Retry-After, 5xx) + twardy deadline
# =====================================================================================
function Invoke-WfApi {
    param([string]$Method, [string]$Path, $Body = $null)
    $uri = "$($script:ApiBase)$Path"
    $attempt = 0
    while ($true) {
        $attempt++
        $req = [System.Net.HttpWebRequest]::Create($uri)
        $req.Method = $Method.ToUpper()
        $req.Accept = 'application/json'
        $req.Headers['Authorization'] = "Bearer $($script:token)"
        $ms = $WriteDeadlineSec * 1000
        $req.Timeout = $ms; $req.ReadWriteTimeout = $ms; $req.KeepAlive = $false
        try {
            if ($null -ne $Body) {
                $json  = $Body | ConvertTo-Json -Depth 14 -Compress
                $bytes = [Text.Encoding]::UTF8.GetBytes($json)
                $req.ContentType = 'application/json; charset=utf-8'
                $rs = $req.GetRequestStream(); $rs.Write($bytes, 0, $bytes.Length); $rs.Close()
            }
            $resp = $req.GetResponse()
            $sr = New-Object IO.StreamReader($resp.GetResponseStream())
            $raw = $sr.ReadToEnd(); $sr.Close(); $resp.Close()
            Start-Sleep -Milliseconds $ThrottleMs
            if ($raw.Trim()) { return ($raw | ConvertFrom-Json) } else { return $null }
        } catch [System.Net.WebException] {
            $code = $null; $errBody = $null; $retryAfter = 0
            try { $code = [int]$_.Exception.Response.StatusCode } catch {}
            try { $retryAfter = [int]$_.Exception.Response.Headers['Retry-After'] } catch {}
            try { $s = $_.Exception.Response.GetResponseStream(); $errBody = (New-Object IO.StreamReader($s)).ReadToEnd() } catch {}
            $isTimeout = ($_.Exception.Status -eq [System.Net.WebExceptionStatus]::Timeout)
            if (($code -eq 429 -or ($code -ge 500 -and $code -lt 600) -or $isTimeout) -and $attempt -lt $MaxRetry) {
                $wait = [math]::Max([math]::Pow(2, $attempt), $retryAfter)
                Write-Host "  HTTP $code$(if($isTimeout){' TIMEOUT'}) -> backoff ${wait}s (proba $attempt/$MaxRetry)" -ForegroundColor Yellow
                Start-Sleep -Seconds $wait
                continue
            }
            throw "API $Method $Path -> HTTP $code :: $errBody"
        }
    }
}

# =====================================================================================
#  ASSETY: upload hero do Webflow Assets (2 kroki: metadane+md5 -> multipart na S3)
#  Zwraca hostedUrl assetu (do pol Image w fieldData jako { url, alt }).
# =====================================================================================
function Get-FileMd5Hex {
    param([byte[]]$Bytes)
    $md5 = [System.Security.Cryptography.MD5]::Create()
    return ([BitConverter]::ToString($md5.ComputeHash($Bytes)) -replace '-', '').ToLower()
}
function Publish-WfAsset {
    param([string]$FilePath, [string]$Etykieta = 'hero')
    $bytes = Read-FileBytesWithRetry -Path $FilePath -Etykieta $Etykieta
    $fname = [IO.Path]::GetFileName($FilePath)
    $hash  = Get-FileMd5Hex -Bytes $bytes
    $meta  = Invoke-WfApi -Method Post -Path "/sites/$($script:siteId)/assets" -Body @{ fileName = $fname; fileHash = $hash }
    if (-not $meta -or -not $meta.uploadUrl) { throw "Asset: brak uploadUrl w odpowiedzi (plik $fname)" }

    # multipart/form-data na S3: NAJPIERW pola z uploadDetails, na koncu 'file'
    $boundary = '----wfb' + [Guid]::NewGuid().ToString('N')
    $nl = "`r`n"
    $sb = New-Object System.IO.MemoryStream
    $enc = [Text.Encoding]::UTF8
    function _wr([System.IO.MemoryStream]$stream, [string]$s) { $b = $enc.GetBytes($s); $stream.Write($b, 0, $b.Length) }
    foreach ($p in $meta.uploadDetails.PSObject.Properties) {
        _wr $sb "--$boundary$nl"
        _wr $sb "Content-Disposition: form-data; name=`"$($p.Name)`"$nl$nl$($p.Value)$nl"
    }
    $ctype = if ($fname -match '\.webp$') { 'image/webp' } elseif ($fname -match '\.png$') { 'image/png' } else { 'image/jpeg' }
    _wr $sb "--$boundary$nl"
    _wr $sb "Content-Disposition: form-data; name=`"file`"; filename=`"$fname`"$nl"
    _wr $sb "Content-Type: $ctype$nl$nl"
    $sb.Write($bytes, 0, $bytes.Length)
    _wr $sb "$nl--$boundary--$nl"
    $payload = $sb.ToArray(); $sb.Close()

    $req = [System.Net.HttpWebRequest]::Create($meta.uploadUrl)
    $req.Method = 'POST'
    $req.ContentType = "multipart/form-data; boundary=$boundary"
    $ms = $WriteDeadlineSec * 1000
    $req.Timeout = $ms; $req.ReadWriteTimeout = $ms; $req.KeepAlive = $false
    $rs = $req.GetRequestStream(); $rs.Write($payload, 0, $payload.Length); $rs.Close()
    $resp = $req.GetResponse(); $s3code = [int]$resp.StatusCode; $resp.Close()
    if ($s3code -lt 200 -or $s3code -ge 300) { throw "Asset: S3 upload zwrocil HTTP $s3code (plik $fname)" }
    Start-Sleep -Milliseconds $ThrottleMs

    $hosted = $meta.hostedUrl
    if (-not $hosted -and $meta.assetUrl) { $hosted = $meta.assetUrl }
    if (-not $hosted -and $meta.id) {
        $asset = Invoke-WfApi -Method Get -Path "/assets/$($meta.id)"
        $hosted = $asset.hostedUrl
    }
    if (-not $hosted) { throw "Asset: nie udalo sie ustalic hostedUrl (plik $fname)" }
    Write-Host "      ASSET OK: $fname -> $hosted" -ForegroundColor Green
    return $hosted
}

# =====================================================================================
#  KARTY FUNKCJI [FEATURE:] / [FEATURES:] -> HTML zgodny z Webflow RichText
#  (RichText NIE przepuszcza div/style! Dozwolone: p, h2-h6, ul/li, blockquote, figure/img,
#   a, strong, em. Karta = figure z screenshotem (jesli jest) + p z linkiem i powodem.
#   Duzy blok CTA pobrania apki jest w SZABLONIE wpisu w Designerze, nie w tresci.)
#  Skladnia w tresc_html:
#    [FEATURE: <id> | <powod, 1 zdanie EN>]
#    [FEATURES: <naglowek sekcji> || <id> | <powod> || <id> | <powod> || <id> | <powod>]
# =====================================================================================
function Get-FeatureCatalog {
    if (-not (Test-Path $featsPath)) { throw "Brak katalogu funkcji: $featsPath" }
    $cat = (Read-TextWithRetry -Path $featsPath -Etykieta 'app-features.json') | ConvertFrom-Json
    $map = @{}
    foreach ($f in $cat.features) { $map[$f.id] = $f }
    return @{ map = $map; cta = $cat.cta }
}
function Render-FeatureCardHtml {
    param($feat, [string]$Reason, $Cta)
    $url = if ($feat.cta_url) { $feat.cta_url } else { $Cta.features_page }
    $img = ''
    if ($feat.screenshot -and "$($feat.screenshot)".Trim()) {
        $img = "<figure><img src=`"$($feat.screenshot)`" alt=`"$($feat.name) in MindSync`"></figure>"
    }
    $label = if ($Cta.cta_label_default) { $Cta.cta_label_default } else { 'Try it free in MindSync' }
    return "$img<p><strong><a href=`"$url`">$($feat.name)</a></strong><br>$Reason <a href=`"$url`">$label &rarr;</a></p>"
}
function Expand-FeatureCards {
    param([string]$Content)
    $catalog = Get-FeatureCatalog
    $map = $catalog.map; $cta = $catalog.cta

    # blok [FEATURES: naglowek || id | powod || ...]
    $Content = [regex]::Replace($Content, '\[FEATURES:\s*([^\]|]+?)\s*\|\|(.+?)\]', {
        param($m)
        $heading = $m.Groups[1].Value.Trim()
        $items = $m.Groups[2].Value -split '\|\|'
        $lis = foreach ($it in $items) {
            $parts = $it -split '\|', 2
            $fid = $parts[0].Trim()
            $reason = if ($parts.Count -gt 1) { $parts[1].Trim() } else { '' }
            if (-not $map.ContainsKey($fid)) { throw "Karta FEATURES: nieznane id funkcji '$fid' (katalog: blog/app-features.json)" }
            $f = $map[$fid]
            $url = if ($f.cta_url) { $f.cta_url } else { $cta.features_page }
            "<li><strong><a href=`"$url`">$($f.name)</a></strong> - $reason</li>"
        }
        "<h3>$heading</h3><ul>$($lis -join '')</ul>"
    })
    # pojedyncze [FEATURE: id | powod]
    $Content = [regex]::Replace($Content, '\[FEATURE:\s*([^\]|]+?)\s*\|\s*([^\]]+?)\s*\]', {
        param($m)
        $fid = $m.Groups[1].Value.Trim()
        $reason = $m.Groups[2].Value.Trim()
        if (-not $map.ContainsKey($fid)) { throw "Karta FEATURE: nieznane id funkcji '$fid' (katalog: blog/app-features.json)" }
        Render-FeatureCardHtml -feat $map[$fid] -Reason $reason -Cta $cta
    })
    return $Content
}

# =====================================================================================
#  LOGI DRIP + LOG PUBLIKACJI (idempotencja) - wzorce z PLASMET bez zmian
# =====================================================================================
function Write-DripLog {
    param([string]$Plik, [string]$ItemId, [string]$Wynik)
    try {
        $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        $tryb = 'LIVE'; try { if ($DryRun) { $tryb = 'DRY' } } catch {}
        if (-not $Plik) { $Plik = '?' }; if (-not $ItemId) { $ItemId = '-' }
        $line = "$stamp | $tryb | plik=$Plik | item_id=$ItemId | $Wynik"
        Add-Content -Path $script:dripLogPath -Value $line -Encoding utf8
        Write-Host "  DRIP-LOG: $line" -ForegroundColor DarkGray
    } catch { Write-Host "  (Write-DripLog nie zapisal: $($_.Exception.Message))" -ForegroundColor DarkYellow }
}
function Write-DripError {
    param($ErrRecord, [string]$Plik = '?')
    try {
        $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        $tryb = 'LIVE'; try { if ($DryRun) { $tryb = 'DRY' } } catch {}
        $msg = ''; $stack = ''; $pos = ''
        try { $msg = "$($ErrRecord.Exception.Message)" } catch {}
        try { $stack = "$($ErrRecord.ScriptStackTrace)" } catch {}
        try { $pos = "$($ErrRecord.InvocationInfo.PositionMessage)" } catch {}
        $block = @('======================================================================',
            "[$stamp] tryb=$tryb plik=$Plik", "Exception.Message    : $msg",
            'ScriptStackTrace     :', $stack, 'InvocationInfo (pozycja):', $pos, '') -join "`r`n"
        Add-Content -Path $script:dripErrorPath -Value $block -Encoding utf8
        Write-Host "  DRIP-ERROR zapisany -> $($script:dripErrorPath)" -ForegroundColor DarkYellow
    } catch { Write-Host "  (Write-DripError nie zapisal: $($_.Exception.Message))" -ForegroundColor DarkYellow }
}
function Load-Log {
    # Toleruje obie postacie pliku: plaska tablice (zapis od 2026-09-22) oraz stara
    # matrioszke { value = ...; Count = ... }, ktora produkowal poprzedni Save-Log.
    # Expand-LogEntries splaszcza jedno i drugie, wiec Already-Published znowu widzi
    # WSZYSTKIE opublikowane slugi, a nie tylko dwa elementy najwyzszego poziomu.
    if (Test-Path $logPath) {
        $raw = Read-TextWithRetry -Path $logPath -Etykieta 'published-log.json'
        if ($raw.Trim()) { return @(Expand-LogEntries -Node ($raw | ConvertFrom-Json)) }
    }
    return @()
}
# UWAGA na potok: ",@($entries) | ConvertTo-Json" w PowerShell 5.1 NIE daje tablicy, tylko
# obiekt { "value": [...], "Count": N }. Kazdy przebieg zawijal wtedy poprzedni log w kolejna
# warstwe, az -Depth 8 zaczynal splaszczac starsze wpisy do tekstu i gubic je bezpowrotnie
# (naprawione 2026-09-22, opis w README). -InputObject serializuje tablice jako tablice,
# takze jednoelementowa. NIE wracaj do wersji z potokiem.
function Save-Log($entries) { ConvertTo-Json -InputObject @($entries) -Depth 8 | Set-Content $logPath -Encoding utf8 }
function Already-Published($log, $slug) { return [bool]($log | Where-Object { $_.slug -eq $slug }) }

# =====================================================================================
#  PUBLIKACJA CALEJ STRONY (odswiezenie sitemap.xml) - krok PO udanej publikacji wpisu
# -------------------------------------------------------------------------------------
#  DLACZEGO: Webflow generuje sitemap.xml WYLACZNIE przy pelnej publikacji strony.
#  Publish pojedynczego itemu CMS (krok [3/4]) stawia wpis na zywo, ale sitemapy NIE
#  odswieza. Dowod z 2026-09-03: sitemap.xml mial 22 URL-e, wszystkie z lastmod
#  2026-08-26T20:42 (= lastPublished strony), i brakowalo w nim 6 z 10 wpisow bloga
#  wypuszczonych dripem 27.08-01.09, mimo ze wszystkie itemy mialy includeInSitemap=true.
#  Po recznej publikacji strony sitemap urosla do 28 URL-i i objela wszystkie 10 wpisow.
#
#  UWAGA, SKUTEK UBOCZNY (przeczytaj zanim wlaczysz drip): pelna publikacja strony
#  wypycha na zywo TAKZE wszystko, co wisi niezapisane/nieopublikowane w Designerze.
#  Czyjes pol-skonczone zmiany layoutu pojda na produkcje razem z wpisem. To nie jest
#  ryzyko teoretyczne: 2026-09-03 w Designerze wisialy zmiany z 27.08 i poszly na zywo
#  przy recznej publikacji (za jawna zgoda operatora). Jesli w Designerze trwa robota,
#  puszczaj drip z -SkipSitePublish i opublikuj strone recznie, gdy Designer bedzie czysty.
#
#  ODPORNOSC: ten krok NIGDY nie wywraca dripu. Wpis jest juz opublikowany i zalogowany,
#  wiec blad publikacji strony (429 / 5xx / timeout) konczy sie ostrzezeniem w
#  _drip-log.txt i kodem wyjscia 0. Item jest wazniejszy niz sitemap.
# =====================================================================================

# ID domen bierzemy na zywo z GET /sites/{id}. Ponizsze stale to TYLKO awaryjny fallback,
# gdyby GET nie zwrocil listy (odczytane z Webflow 2026-09-03).
$script:FallbackCustomDomainIds = @(
    '67daea32f822edc69c426583',   # www.mindsync.app
    '67daea32f822edc69c426578'    # mindsync.app
)

function Get-WfSiteDomainIds {
    $ids = @()
    try {
        $site = Invoke-WfApi -Method Get -Path "/sites/$($script:siteId)"
        foreach ($d in @($site.customDomains)) { if ($d -and $d.id) { $ids += "$($d.id)" } }
    } catch {
        Write-Host "      (GET /sites nie zwrocil domen: $($_.Exception.Message)) -> stale awaryjne" -ForegroundColor DarkYellow
    }
    if ($ids.Count -eq 0) { $ids = $script:FallbackCustomDomainIds }
    return ,([string[]]$ids)
}

function Invoke-WfSitePublish {
    param([string]$Plik = '-')

    if (-not $script:sitePublishNeeded) {
        Write-Host '  PUBLIKACJA STRONY: pomijam swiadomie - w tym przebiegu nie opublikowano zadnego wpisu.' -ForegroundColor DarkGray
        return
    }
    if ($SkipSitePublish) {
        Write-Host '  PUBLIKACJA STRONY: pomijam (-SkipSitePublish). Sitemap.xml NIE obejmie nowego wpisu do czasu recznej publikacji strony.' -ForegroundColor Yellow
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik 'SITE-PUBLISH POMINIETO (-SkipSitePublish)'
        return
    }
    if ($DryRun) {
        $preview = @{ customDomains = $script:FallbackCustomDomainIds } | ConvertTo-Json -Depth 4 -Compress
        Write-Host '  [DRY-RUN] PUBLIKACJA STRONY: NIE wysylam. Na zywo poszloby:' -ForegroundColor Magenta
        Write-Host "      POST $($script:ApiBase)/sites/$($script:siteId)/publish" -ForegroundColor Magenta
        Write-Host "      body: $preview" -ForegroundColor Magenta
        Write-Host "      (LIVE bierze id domen z GET /sites/$($script:siteId); powyzsze to fallback)" -ForegroundColor Magenta
        Write-Host '      efekt: przegenerowanie sitemap.xml ORAZ wypchniecie niezapisanych zmian z Designera.' -ForegroundColor Magenta
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik 'SITE-PUBLISH DRY: pominiete wyslanie'
        return
    }

    try {
        $ids = Get-WfSiteDomainIds
        Write-Host "  [SITE] publikacja calej strony (odswiezenie sitemap.xml), domeny=$($ids.Count)..." -ForegroundColor DarkCyan
        $null = Invoke-WfApi -Method Post -Path "/sites/$($script:siteId)/publish" -Body @{ customDomains = $ids }
        Write-Host '      SITE-PUBLISH OK - Webflow przegeneruje sitemap.xml.' -ForegroundColor Green
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik "SITE-PUBLISH OK (domeny=$($ids -join ','))"
        $script:sitePublishOk = $true
    } catch {
        $powod = "$($_.Exception.Message)" -replace '\s+', ' '
        if ($powod.Length -gt 300) { $powod = $powod.Substring(0, 300) }
        Write-Host "      SITE-PUBLISH BLAD: $powod" -ForegroundColor Yellow
        Write-Host '      To NIE jest blad dripu: wpis jest opublikowany i zalogowany. Sitemap dogoni sie przy nastepnym przebiegu albo recznie.' -ForegroundColor Yellow
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik "SITE-PUBLISH BLAD: $powod"
    }
}

# =====================================================================================
#  ZGLOSZENIE SITEMAPY W GOOGLE SEARCH CONSOLE - krok PO udanej publikacji calej strony
# -------------------------------------------------------------------------------------
#  PO CO: pomiar GSC (seo-reports/2026-09-25-wyniki-bloga-i-kontrola-indeksacji.md): reczny
#  resubmit 22.09 = pobranie sitemapy w sekunde i indeksacja 7 wpisow w ~4 h. Bez niego
#  Google nie pobral sitemapy od 22.09, a wpis z 23.09 byl "unknown to Google".
#  JAK: python scripts/gsc/pull_gsc.py submit-sitemap (Search Console API sitemaps.submit,
#  potem GET tej sitemapy). Wymaga tokenu GSC z zakresem webmasters (nie .readonly);
#  reautoryzacja raz, recznie: python scripts/gsc/pull_gsc.py auth.
#  WARUNKI: w tym przebiegu poszedl wpis na zywo ORAZ publikacja strony sie udala.
#  Czekamy $GscSubmitDelaySec s, zeby Webflow zdazyl przegenerowac sitemap.xml.
#  ODPORNOSC: brak pythona, brak zakresu, HTTP != 2xx -> "GSC-SUBMIT BLAD: ..." w
#  _drip-log.txt, nigdy nie wywraca dripu. Wylacznik: -SkipGscSubmit.
# =====================================================================================
$script:GscScript = Join-Path $repoRoot 'scripts\gsc\pull_gsc.py'

function Invoke-GscSitemapSubmit {
    param([string]$Plik = '-')

    if (-not $script:sitePublishNeeded) {
        Write-Host '  GSC: pomijam swiadomie - w tym przebiegu nie opublikowano zadnego wpisu.' -ForegroundColor DarkGray
        return
    }
    if ($SkipGscSubmit) {
        Write-Host '  GSC: pomijam (-SkipGscSubmit). Sitemapa nie zostanie zgloszona w Search Console.' -ForegroundColor Yellow
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik 'GSC-SUBMIT POMINIETO (-SkipGscSubmit)'
        return
    }
    if ($DryRun) {
        Write-Host '  [DRY-RUN] GSC: NIE zglaszam. Na zywo, po udanej publikacji strony i odczekaniu' -ForegroundColor Magenta
        Write-Host "      ${GscSubmitDelaySec}s, poszloby: python `"$($script:GscScript)`" submit-sitemap" -ForegroundColor Magenta
        Write-Host '      (PUT webmasters/v3/sites/sc-domain%3Amindsync.app/sitemaps/https%3A%2F%2Fwww.mindsync.app%2Fsitemap.xml)' -ForegroundColor Magenta
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik 'GSC-SUBMIT DRY: pominiete wyslanie'
        return
    }
    if (-not $script:sitePublishOk) {
        Write-Host '  GSC: pomijam - publikacja strony nie przeszla, sitemap.xml jest stara.' -ForegroundColor Yellow
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik 'GSC-SUBMIT POMINIETO: publikacja strony nieudana/pominieta'
        return
    }

    try {
        if (-not (Test-Path $script:GscScript)) { throw "brak skryptu $($script:GscScript)" }
        $py = Get-Command python -ErrorAction SilentlyContinue
        if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
        if (-not $py) { throw 'nie znaleziono pythona w PATH (python/py)' }
        Write-Host "  [GSC] czekam ${GscSubmitDelaySec}s na przegenerowanie sitemap.xml, potem zglaszam..." -ForegroundColor DarkCyan
        Start-Sleep -Seconds $GscSubmitDelaySec
        $oldEap = $ErrorActionPreference
        $ErrorActionPreference = 'Continue'   # stderr pythona nie moze rzucic jako NativeCommandError
        try {
            $env:PYTHONIOENCODING = 'utf-8'
            $out = & $py.Source $script:GscScript submit-sitemap 2>&1 | ForEach-Object { "$_" }
            $kod = $LASTEXITCODE
        } finally {
            $ErrorActionPreference = $oldEap
            $global:LASTEXITCODE = 0          # kod pythona nie moze przeciec jako kod wyjscia dripu
        }
        $tekst = (@($out) -join ' ') -replace '\s+', ' '
        if ($kod -ne 0) { throw "exit=$kod :: $tekst" }
        $ld = [regex]::Match($tekst, 'lastDownloaded=(\S+)')
        $ldTxt = if ($ld.Success) { $ld.Groups[1].Value } else { '?' }
        Write-Host "      GSC-SUBMIT OK (lastDownloaded=$ldTxt)" -ForegroundColor Green
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik "GSC-SUBMIT OK (lastDownloaded=$ldTxt)"
    } catch {
        $powod = "$($_.Exception.Message)" -replace '\s+', ' '
        if ($powod.Length -gt 300) { $powod = $powod.Substring(0, 300) }
        Write-Host "      GSC-SUBMIT BLAD: $powod" -ForegroundColor Yellow
        Write-Host '      To NIE jest blad dripu: wpis i sitemap sa na zywo, Google pobierze sitemape sam albo po recznym Submit.' -ForegroundColor Yellow
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik "GSC-SUBMIT BLAD: $powod"
    }
}

# =====================================================================================
#  ODKRYWANIE NOWYCH WPISOW: sekcja "Latest from the journal" na / oraz lastmod /blog
# -------------------------------------------------------------------------------------
#  PO CO: pomiar GSC z 2026-09-22 (seo-reports/2026-09-22-kontrola-indeksacji-po-naprawie.md)
#  pokazal, ze od 15.09 Google nie zaindeksowal ani jednego nowego wpisu, a 5 najnowszych
#  ma status "URL is unknown to Google". Oba kanaly odkrywania stoja w miejscu:
#    1. sekcja "Latest from the journal" na stronie glownej pokazuje reczny wybor z 15.09
#       i nie linkuje zadnego nowego wpisu (a / jest crawlowane co 1-3 dni),
#    2. lastmod strony /blog w sitemapie stoi na 2026-09-15T10:45, bo Webflow bierze go
#       z lastUpdated TEJ strony, a dodanie itemu CMS ani publikacja strony tego nie rusza
#       (dowod: sitemap.xml podaje dla /blog 2026-09-15T10:45:58.427Z, czyli dokladnie
#       lastUpdated z GET /v2/pages/67ccb2a66069c30ddcc93974).
#
#  ROZPOZNANIE KANALU (2026-09-22, wylacznie GET, zero zapisu). Czego SIE NIE DA:
#  A) Podmiana 3 kart na stronie glownej przez Data API: NIEMOZLIWA.
#     Zapis tresci statycznej to POST /v2/pages/{id}/dom, ktory dziala wylacznie dla
#     lokalizacji DODATKOWYCH. Dokumentacja Webflow: "API-based updates to page and
#     component content are limited to secondary locales. Primary locale content for pages
#     and components must be updated through the Webflow Designer." GET /v2/sites/{id}
#     zwraca dla mindsync.app locales.secondary = [] (zero lokalizacji dodatkowych), wiec
#     ten endpoint jest tu zamkniety. Nawet gdyby byl otwarty, nie wystarczylby: lista
#     typow wezlow przyjmowanych przez zapis (text, component-instance, select, text-input,
#     submit-button, search-button) nie obejmuje obrazkow, a samego linku karty
#     <a class="ms-journal-card"> GET /v2/pages/{home}/dom w ogole nie zwraca (widac tylko
#     jego dzieci: obrazek, tytul, opis), wiec href nie ma jak zostac przepiety.
#  B) Odswiezenie lastUpdated strony /blog: DZIALA (zweryfikowane na zywo 2026-09-25).
#     Zapis to PUT /v2/pages/{id} (PATCH zwraca 404 RouteNotFound), body przyjmuje title,
#     slug, seo.title/description oraz openGraph.title/description (+ flagi *Copied).
#     Zapis identycznych wartosci to no-op (potwierdzone 15.09), ale pole `title` jest
#     publicznie NEUTRALNE: to wewnetrzna nazwa strony w Designerze ("Blog"). Publiczny
#     <title> na /blog pochodzi z seo.title, a og:title z openGraph.title (titleCopied=false),
#     wiec zmiana `title` nie dotyka niczego, co widzi Google albo udostepnienie.
#     Dowod 2026-09-25: PUT { title: "Blog listing" } przesunal lastUpdated z
#     2026-09-15T10:45:58.427Z na 2026-09-25T11:32:16.542Z, seo.* i openGraph.* bez zmian;
#     powrot na "Blog" dal 2026-09-25T11:32:32.417Z.
#     Skrypt przelacza wiec `title` miedzy dwiema stalymi nazwami ($script:BlogPageNames),
#     zawsze na te druga niz obecna, i wysyla WYLACZNIE to pole.
#
#  CO WIEC ROBI TEN KROK: kontroluje sekcje na Home (sam odczyt, glosny wpis w
#  _drip-log.txt z lista do podmiany, gdy odstaje od 3 najnowszych wpisow; milknie sama
#  po zamianie 3 kart na Collection List, opis w scripts/webflow/README.md) oraz, gdy
#  lastUpdated /blog jest starszy niz ostatnia publikacja, przelacza nazwe strony /blog.
#  DryRun: tylko podglad payloadu PUT, zero zapisu.
#
#  KOLEJNOSC: krok leci ZAWSZE przed Invoke-WfSitePublish. Zmiana nazwy strony jest
#  zastagowana i dopiero POST /sites/{id}/publish wypycha nowy lastmod do sitemap.xml.
#  Z -SkipSitePublish nowa data poczeka na najblizsza publikacje strony.
#
#  ODPORNOSC: krok NIGDY nie wywraca dripu (wzorzec z Invoke-WfSitePublish): calosc
#  w try/catch, powod skrocony do 300 znakow, wpis do logu, exit 0. Wpis na blogu jest
#  wazniejszy niz kontrola sekcji. Wylacznik: -SkipDiscoveryRefresh.
# =====================================================================================

$script:HomePageId    = '676ed8d44b863915ae191f82'   # strona Home (GET /sites/{id}/pages, 2026-09-22)
$script:BlogPageId    = '67ccb2a66069c30ddcc93974'   # strona /blog (listing bloga)
$script:HomePublicUrl = 'https://www.mindsync.app/'  # host www: goly mindsync.app odpowiada 301
# Dwie stale nazwy wewnetrzne strony /blog (pole `title` w PUT /pages, widoczne tylko w
# Designerze). Odswiezenie lastmod przelacza na te druga niz obecna.
$script:BlogPageNames = @('Blog', 'Blog listing')

function ConvertFrom-LogEntryString {
    # Ratunek dla starych wpisow z published-log.json, ktore PowerShell zapisal jako tekst
    # "@{tytul=...; slug=...; ...}" zamiast obiektu (historia awarii logu: README).
    param([string]$S)
    try {
        $t = "$S".Trim()
        if ($t -notmatch '^@\{.*\}$') { return $null }
        $t = $t.Substring(2, $t.Length - 3)
        $o = [ordered]@{}
        foreach ($para in ($t -split ';\s')) {
            $kv = $para -split '=', 2
            if ($kv.Count -eq 2) { $o[$kv[0].Trim()] = $kv[1].Trim() }
        }
        if (-not $o.Contains('slug')) { return $null }
        return [pscustomobject]$o
    } catch { return $null }
}

function Expand-LogEntries {
    # Splaszcza stara matrioszke { value = ...; Count = ... } i zwykla plaska tablice.
    # Uzywane przez Load-Log oraz przez krok kontroli odkrywania.
    param($Node, [int]$Glebokosc = 0)
    $out = @()
    if ($null -eq $Node -or $Glebokosc -gt 40) { return $out }
    if ($Node -is [string]) {
        $rec = ConvertFrom-LogEntryString $Node
        if ($rec) { $out += $rec }
        return $out
    }
    if ($Node -is [System.Collections.IEnumerable]) {
        foreach ($x in $Node) { $out += @(Expand-LogEntries -Node $x -Glebokosc ($Glebokosc + 1)) }
        return $out
    }
    $pola = @($Node.PSObject.Properties.Name)
    if ($pola -contains 'slug')  { return @($Node) }
    if ($pola -contains 'value') { return @(Expand-LogEntries -Node $Node.value -Glebokosc ($Glebokosc + 1)) }
    return $out
}

function Get-TopPublishedPosts {
    # N najnowszych wpisow, ktore FAKTYCZNIE poszly na zywo (zrodlo: published-log.json,
    # nie kolejka), wzbogaconych o dane z pliku kolejki: zajawka, alt hero, plik 800x600.
    param([int]$Ile = 3)
    $raw = @()
    if (Test-Path $logPath) {
        $txt = Read-TextWithRetry -Path $logPath -Etykieta 'published-log.json'
        if ($txt.Trim()) { $raw = @(Expand-LogEntries -Node ($txt | ConvertFrom-Json)) }
    }
    $uniq = @{}
    foreach ($e in $raw) {
        $s = "$($e.slug)".Trim()
        if (-not $s) { continue }
        if (-not $uniq.ContainsKey($s) -or "$($uniq[$s].data)" -lt "$($e.data)") { $uniq[$s] = $e }
    }
    $top = @($uniq.Values | Sort-Object { "$($_.data)" } -Descending | Select-Object -First $Ile)
    $res = @()
    foreach ($e in $top) {
        $tytul = "$($e.tytul)"; $zaj = ''; $alt = ''; $thumb = $null; $plik = "$($e.plik)"
        if ($plik) {
            $qp = Join-Path $queueDir $plik
            if (Test-Path $qp) {
                try {
                    $q = (Read-TextWithRetry -Path $qp -Etykieta "queue/$plik") | ConvertFrom-Json
                    if ($q.tytul) { $tytul = "$($q.tytul)" }
                    if ($q.zajawka_html) { $zaj = ($q.zajawka_html -replace '<[^>]+>', ' ' -replace '\s+', ' ').Trim() }
                    if ($q.hero_image_alt) { $alt = "$($q.hero_image_alt)" }
                    $thumb = Find-HeroFile $q '800x600'
                } catch {
                    Write-Host "      (nie odczytalem $plik z kolejki: $($_.Exception.Message))" -ForegroundColor DarkYellow
                }
            }
        }
        $res += [pscustomobject]@{
            slug = "$($e.slug)"; tytul = $tytul; data = "$($e.data)"
            plik = $plik; zajawka = $zaj; alt = $alt; thumb = $thumb
        }
    }
    return @($res)
}

function Get-PublicHtml {
    # Jedyny odczyt spoza Webflow API w tym skrypcie. Sekcja "Latest from the journal" to
    # statyczne linki, ktorych GET /pages/{id}/dom nie zwraca (widzi tylko tekst i obrazki
    # w srodku kart), wiec prawde o tym, KTORE wpisy sa podlinkowane, da tylko wyrenderowana
    # strona. Czysty GET, bez tokenu, bez zapisu.
    param([string]$Url)
    $req = [System.Net.HttpWebRequest]::Create($Url)
    $req.Method = 'GET'
    $req.UserAgent = 'MindSync-blog-publish/1.0 (kontrola sekcji Latest from the journal)'
    $ms = $WriteDeadlineSec * 1000
    $req.Timeout = $ms; $req.ReadWriteTimeout = $ms; $req.KeepAlive = $false
    $resp = $req.GetResponse()
    $sr = New-Object IO.StreamReader($resp.GetResponseStream(), [Text.Encoding]::UTF8)
    $html = $sr.ReadToEnd(); $sr.Close(); $resp.Close()
    return $html
}

function Get-HomeJournalSlugs {
    # Z zywego HTML: slugi z kart <a class="ms-journal-card ..." href="/journal/...">.
    param([string]$Html)
    $slugi = @()
    foreach ($m in [regex]::Matches($Html, '<a\b[^>]*class="[^"]*ms-journal-card[^"]*"[^>]*>')) {
        $h = [regex]::Match($m.Value, 'href="([^"]*)"')
        if (-not $h.Success) { continue }
        $u = [regex]::Match($h.Groups[1].Value, '/journal/([^/"#?]+)')
        if ($u.Success) { $slugi += $u.Groups[1].Value }
    }
    return @($slugi)
}

function ConvertTo-UtcOrNull {
    # lastUpdated z Webflow to ISO UTC ("2026-09-15T10:45:58.427Z"); pole `data` w
    # published-log.json to czas LOKALNY ("2026-09-23 07:00:17"). Oba sprowadzamy do UTC.
    param([string]$S, [switch]$Local)
    if (-not "$S".Trim()) { return $null }
    $ci = [Globalization.CultureInfo]::InvariantCulture
    try {
        if ($Local) { return ([datetime]::Parse($S, $ci, [Globalization.DateTimeStyles]::AssumeLocal)).ToUniversalTime() }
        return [datetime]::Parse($S, $ci, ([Globalization.DateTimeStyles]::AdjustToUniversal -bor [Globalization.DateTimeStyles]::AssumeUniversal))
    } catch { return $null }
}

function Get-BlogNameToggle {
    # Zwraca nazwe, na ktora przelaczyc strone /blog: ZAWSZE te druga niz obecna, zeby
    # zapis nie byl no-opem. Obca nazwa (ktos zmienil w Designerze) -> pierwsza z pary.
    param([string]$Obecna)
    if ($Obecna -eq $script:BlogPageNames[0]) { return $script:BlogPageNames[1] }
    return $script:BlogPageNames[0]
}

function Invoke-WfBlogLastmodRefresh {
    # Odswieza lastUpdated strony /blog (= jej lastmod w sitemap.xml) przez PUT samego pola
    # `title`, czyli wewnetrznej nazwy strony w Designerze. seo.* i openGraph.* NIE sa
    # wysylane. Wolane z Invoke-WfDiscoveryRefresh, wewnatrz jego try/catch.
    param([string]$Plik = '-', [string]$OstatniWpis = '')
    $page = Invoke-WfApi -Method Get -Path "/pages/$($script:BlogPageId)"
    $lu = "$($page.lastUpdated)"
    $luUtc  = ConvertTo-UtcOrNull -S $lu
    $ostUtc = ConvertTo-UtcOrNull -S $OstatniWpis -Local
    if ($null -eq $luUtc -or $null -eq $ostUtc) {
        Write-Host "      LASTMOD /blog: nie porownuje, nieczytelne daty (lastUpdated='$lu', ostatni wpis='$OstatniWpis')." -ForegroundColor DarkYellow
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik "DISCOVERY UWAGA: /blog nieczytelne daty (lastUpdated='$lu', wpis='$OstatniWpis')"
        return
    }
    if ($luUtc -ge $ostUtc) {
        Write-Host "      LASTMOD /blog OK: lastUpdated=$lu (nie starszy niz ostatnia publikacja $OstatniWpis)." -ForegroundColor Green
        return
    }

    $obecna = "$($page.title)"
    $nowa = Get-BlogNameToggle -Obecna $obecna
    $body = @{ title = $nowa }
    Write-Host "      LASTMOD /blog: lastUpdated=$lu starszy niz ostatnia publikacja ($OstatniWpis)." -ForegroundColor Yellow
    if ($DryRun) {
        Write-Host '      [DRY-RUN] ODSWIEZENIE /blog: NIE wysylam. Na zywo poszloby:' -ForegroundColor Magenta
        Write-Host "        PUT $($script:ApiBase)/pages/$($script:BlogPageId)" -ForegroundColor Magenta
        Write-Host "        body: $($body | ConvertTo-Json -Compress)   (nazwa '$obecna' -> '$nowa'; seo.* i openGraph.* nie ruszane)" -ForegroundColor Magenta
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik "DISCOVERY DRY: /blog title '$obecna' -> '$nowa' (pominiete wyslanie)"
        return
    }
    $r = Invoke-WfApi -Method Put -Path "/pages/$($script:BlogPageId)" -Body $body
    $nowyLu = "$($r.lastUpdated)"
    if (-not $nowyLu) {
        $po = Invoke-WfApi -Method Get -Path "/pages/$($script:BlogPageId)"
        $nowyLu = "$($po.lastUpdated)"
    }
    if ($nowyLu -and $nowyLu -ne $lu) {
        Write-Host "      DISCOVERY OK: /blog lastUpdated $lu -> $nowyLu (nazwa '$obecna' -> '$nowa'). Publikacja strony wypchnie nowy lastmod." -ForegroundColor Green
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik "DISCOVERY OK: /blog lastUpdated odswiezony $lu -> $nowyLu (title '$obecna' -> '$nowa')"
    } else {
        Write-Host "      DISCOVERY UWAGA: PUT /pages przeszedl, ale lastUpdated sie nie ruszyl ($lu -> '$nowyLu')." -ForegroundColor Yellow
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik "DISCOVERY UWAGA: /blog PUT title bez zmiany lastUpdated ($lu -> '$nowyLu')"
    }
}

function Invoke-WfDiscoveryRefresh {
    param([string]$Plik = '-')

    if (-not $script:sitePublishNeeded) {
        Write-Host '  ODKRYWANIE: pomijam swiadomie - w tym przebiegu nie opublikowano zadnego wpisu.' -ForegroundColor DarkGray
        return
    }
    if ($SkipDiscoveryRefresh) {
        Write-Host '  ODKRYWANIE: pomijam (-SkipDiscoveryRefresh). Sekcja na Home i lastmod /blog NIE zostana sprawdzone.' -ForegroundColor Yellow
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik 'DISCOVERY POMINIETO (-SkipDiscoveryRefresh)'
        return
    }

    try {
        $top = @(Get-TopPublishedPosts -Ile 3)
        if ($top.Count -eq 0) {
            Write-Host '  ODKRYWANIE: published-log.json nie ma ani jednego czytelnego wpisu, nie mam czego porownac.' -ForegroundColor Yellow
            Write-DripLog -Plik $Plik -ItemId '-' -Wynik 'DISCOVERY POMINIETO: pusty published-log'
            return
        }
        $etykieta = ''
        if ($DryRun) { $etykieta = '[DRY-RUN] ' }
        Write-Host "  ${etykieta}ODKRYWANIE: sprawdzam sekcje 'Latest from the journal' na $($script:HomePublicUrl) (GET, zero zapisu)..." -ForegroundColor DarkCyan

        # --- czesc A: 3 karty na stronie glownej ---
        $zywe = @(Get-HomeJournalSlugs -Html (Get-PublicHtml -Url $script:HomePublicUrl))
        $chce = @($top | ForEach-Object { $_.slug })
        if ($top.Count -lt 3) {
            Write-Host "      UWAGA: published-log ma tylko $($top.Count) czytelnych wpisow, porownuje tyle, ile mam." -ForegroundColor DarkYellow
        }

        if ($zywe.Count -eq 0) {
            Write-Host '      ODKRYWANIE: nie znalazlem kart .ms-journal-card na stronie glownej (zmienil sie szablon?), nic nie robie.' -ForegroundColor Yellow
            Write-DripLog -Plik $Plik -ItemId '-' -Wynik 'DISCOVERY UWAGA: brak kart .ms-journal-card na stronie glownej'
        }
        elseif ((($zywe | Sort-Object) -join ',') -eq (($chce | Sort-Object) -join ',')) {
            Write-Host "      ODKRYWANIE OK: strona glowna linkuje juz 3 najnowsze wpisy ($($zywe -join ', ')). Nic nie wysylam." -ForegroundColor Green
            Write-DripLog -Plik $Plik -ItemId '-' -Wynik 'DISCOVERY OK: sekcja na Home aktualna (nic nie wyslano)'
        }
        else {
            Write-Host '      ODKRYWANIE: sekcja na stronie glownej jest NIEAKTUALNA.' -ForegroundColor Yellow
            Write-Host "        na zywo linkuje  : $($zywe -join ', ')" -ForegroundColor Yellow
            Write-Host "        powinna linkowac : $($chce -join ', ')" -ForegroundColor Yellow
            Write-Host '        PAYLOAD ZAPISU: BRAK. Webflow Data API nie zapisuje tresci statycznej w lokalizacji' -ForegroundColor Yellow
            Write-Host '        glownej (tylko w dodatkowych, a ta strona ich nie ma), wiec skrypt nie ma czym tego' -ForegroundColor Yellow
            Write-Host '        podmienic ani na zywo, ani w DryRun. Szczegoly: naglowek tej sekcji w skrypcie.' -ForegroundColor Yellow
            Write-Host '        Do podmiany recznie w Designerze (Home, sekcja .ms-journal-latest), od najnowszej:' -ForegroundColor Yellow
            $nr = 0
            foreach ($p in $top) {
                $nr++
                $hero = '(BRAK pliku hero-800x600 na dysku)'
                if ($p.thumb) { $hero = $p.thumb }
                $altTxt = '(brak hero_image_alt w kolejce)'
                if ($p.alt) { $altTxt = $p.alt }
                $plikTxt = '(nieznany)'
                if ($p.plik) { $plikTxt = $p.plik }
                Write-Host "          [$nr] href = /journal/$($p.slug)" -ForegroundColor Yellow
                Write-Host "               wpis : $($p.tytul)" -ForegroundColor DarkYellow
                Write-Host "               hero : $hero" -ForegroundColor DarkYellow
                Write-Host "               alt  : $altTxt" -ForegroundColor DarkYellow
                Write-Host "               plik : $plikTxt" -ForegroundColor DarkYellow
            }
            Write-Host '        Tytul i opis karty sa krotsze niz tytul i zajawka wpisu, wiec pisze je autor, nie skrypt.' -ForegroundColor DarkYellow
            Write-Host '        Trwale rozwiazanie (raz, recznie w Designerze): zamien 3 statyczne karty na Collection' -ForegroundColor DarkYellow
            Write-Host '        List z kolekcji Blog Posts, sortowanie po dacie malejaco, limit 3. Wtedy ta kontrola' -ForegroundColor DarkYellow
            Write-Host '        zamilknie sama, bo sekcja bedzie sie zgadzac po kazdej publikacji.' -ForegroundColor DarkYellow
            $w = "DISCOVERY UWAGA: Home linkuje [$($zywe -join ',')], powinno [$($chce -join ',')]"
            if ($w.Length -gt 300) { $w = $w.Substring(0, 300) }
            Write-DripLog -Plik $Plik -ItemId '-' -Wynik $w
        }

        # --- czesc B: lastmod strony /blog (odswiezenie przez przelaczenie nazwy strony) ---
        Invoke-WfBlogLastmodRefresh -Plik $Plik -OstatniWpis "$($top[0].data)"
    } catch {
        $powod = "$($_.Exception.Message)" -replace '\s+', ' '
        if ($powod.Length -gt 300) { $powod = $powod.Substring(0, 300) }
        Write-Host "      ODKRYWANIE BLAD: $powod" -ForegroundColor Yellow
        Write-Host '      To NIE jest blad dripu: wpis jest opublikowany i zalogowany, kontrola dogoni sie jutro.' -ForegroundColor Yellow
        Write-DripLog -Plik $Plik -ItemId '-' -Wynik "DISCOVERY BLAD: $powod"
    }
}

# =====================================================================================
#  POMOCNICZE: hero na dysku, slug, kategoria, walidacje
# =====================================================================================
function Get-HeroSlug($item) {
    if ($item.PSObject.Properties.Name -contains 'hero_slug' -and $item.hero_slug) { return "$($item.hero_slug)".Trim() }
    if ($item.seo_url) { return "$($item.seo_url)".Trim() }
    return ($item.tytul -replace '[^\p{L}\p{Nd}]+', '-').Trim('-').ToLower()
}
function Find-HeroFile($item, [string]$Size = '1600x900') {
    $cands = @()
    if ($Size -eq '1600x900' -and $item.hero_image -and "$($item.hero_image)".Trim()) {
        $p = "$($item.hero_image)".Trim()
        $cands += $(if ([IO.Path]::IsPathRooted($p)) { $p } else { Join-Path $repoRoot $p })
    }
    $slug = Get-HeroSlug $item
    if ($slug) {
        $dir = Join-Path $imagesDir $slug
        foreach ($ext in @('webp', 'jpg', 'png')) { $cands += (Join-Path $dir "hero-$Size.$ext") }
    }
    foreach ($c in $cands) { if ($c -and (Test-Path $c)) { return $c } }
    return $null
}
function Resolve-CategoryOptionId([string]$Name) {
    if (-not $Name) { return $null }
    if ($script:CategoryMap.ContainsKey($Name)) { return $script:CategoryMap[$Name] }
    throw "Kategoria '$Name' poza zestawem kolekcji (dozwolone: $($script:CategoryMap.Keys -join ', ')). Zmiana zestawu = decyzja operatora w Webflow."
}
function Get-ItemBySlug([string]$Slug) {
    $r = Invoke-WfApi -Method Get -Path "/collections/$($script:collectionId)/items?slug=$([Uri]::EscapeDataString($Slug))&limit=2"
    if ($r -and $r.items) {
        foreach ($it in @($r.items)) { if ($it.fieldData.slug -eq $Slug) { return $it } }
    }
    return $null
}

# =====================================================================================
#  BUDOWA fieldData z pliku kolejki (+ hero jako { url, alt } po uploadzie assetu)
# =====================================================================================
function Build-FieldData {
    param($item, [string]$Content, [string]$HeroUrl, [string]$ThumbUrl)
    $alt = if ($item.hero_image_alt) { "$($item.hero_image_alt)" } else { "$($item.tytul)" }
    $summary = if ($item.zajawka_html) { ($item.zajawka_html -replace '<[^>]+>', ' ' -replace '\s+', ' ').Trim() } else { '' }
    $fd = [ordered]@{
        name              = "$($item.tytul)"
        slug              = "$($item.seo_url)"
        'post-body'       = $Content
        'post-summary'    = $summary
        'seo-title'       = "$($item.meta_title)"
        'seo-description' = "$($item.meta_description)"
        'hero-alt'        = $alt
        featured          = [bool]$(if ($item.PSObject.Properties.Name -contains 'featured') { $item.featured } else { $false })
        color             = $(if ($item.kolor) { "$($item.kolor)" } else { $script:DefaultColor })
    }
    $catId = Resolve-CategoryOptionId $item.kategoria
    if ($catId) { $fd['category'] = $catId }
    if ($item.schema_jsonld) {
        $sj = if ($item.schema_jsonld -is [string]) { $item.schema_jsonld } else { ($item.schema_jsonld | ConvertTo-Json -Depth 14 -Compress) }
        $fd['schema-jsonld'] = $sj
    }
    if ($HeroUrl)  { $fd['main-image']      = @{ url = $HeroUrl;  alt = $alt } }
    if ($ThumbUrl) { $fd['thumbnail-image'] = @{ url = $ThumbUrl; alt = $alt } }
    return $fd
}

# =====================================================================================
#  WYBOR KANDYDATOW: status 'gotowy', planowana_data ASC, nazwa ASC
# =====================================================================================
function Select-NextGotowy {
    if (-not (Test-Path $queueDir)) { throw "Brak katalogu kolejki: $queueDir" }
    $cand = @()
    Get-ChildItem $queueDir -Filter '*.json' | Where-Object { $_.Name -notlike '_*' } | ForEach-Object {
        $obj = $null
        try { $obj = (Read-TextWithRetry -Path $_.FullName -Etykieta "queue/$($_.Name)") | ConvertFrom-Json } catch {
            Write-Host "  UWAGA: nie moge sparsowac $($_.Name) -> pomijam." -ForegroundColor Yellow; return
        }
        if ($obj.status -ne 'gotowy') { return }
        $pd = [datetime]::MaxValue
        if ($obj.planowana_data) { try { $pd = [datetime]::Parse($obj.planowana_data) } catch {} }
        if ($pd.Date -gt (Get-Date).Date) { return }   # jeszcze nie czas
        $cand += [pscustomobject]@{ file = $_; obj = $obj; pd = $pd; name = $_.Name }
    }
    return @($cand | Sort-Object pd, name)
}

# =====================================================================================
#  BRAMKI 1-5 + RENDER TRESCI (LINK-LATER, karty [FEATURE:])
# -------------------------------------------------------------------------------------
#  Wspolne dla publikacji nowego wpisu (Publish-QueueItem) i odswiezenia opublikowanego
#  (Republish-QueueItem), zeby obie sciezki renderowaly post-body IDENTYCZNIE.
#  Wydzielone 2026-10-21 bez zmiany logiki: te same bramki, komunikaty, wpisy w logu
#  i kolejnosc co wczesniej w Publish-QueueItem.
#  Zwraca @{ rc; content; heroPath; thumbPath }: rc=0 przeszlo, rc=2 pomin wpis.
#  -BodyOnly (tylko z -Republish): bramki 4 (hero) i 5 (zajawka) wylacznie informuja,
#  bo w tym trybie ani hero, ani post-summary nie sa wysylane.
# =====================================================================================
function Invoke-QueueItemGates {
    param($file, $item, [switch]$BodyOnly)

    # BRAMKA 1: surowe [LINK:...]
    $content = "$($item.tresc_html)"
    $leftover = [regex]::Matches($content, '\[LINK:[^\]]*\]')
    if ($leftover.Count -gt 0) {
        Write-Host "  OSTRZEZENIE: surowe [LINK:] ($($leftover.Count)) -> NIE publikuje." -ForegroundColor Yellow
        Write-DripLog -Plik $file.Name -ItemId '-' -Wynik "POMINIETO: surowe [LINK:] ($($leftover.Count))"
        return @{ rc = 2 }
    }
    # BRAMKA 2: dlugi myslnik U+2014 (zakaz twardy)
    $EMDASH = [char]0x2014
    $pola = [ordered]@{ tresc_html = $content; tytul = "$($item.tytul)"; meta_title = "$($item.meta_title)";
                        meta_description = "$($item.meta_description)"; zajawka_html = "$($item.zajawka_html)" }
    $zle = @(); foreach ($k in $pola.Keys) { if ($pola[$k] -and $pola[$k].Contains($EMDASH)) { $zle += $k } }
    if ($zle.Count -gt 0) {
        Write-Host "  OSTRZEZENIE: em-dash w polach: $($zle -join ', ') -> NIE publikuje." -ForegroundColor Yellow
        Write-DripLog -Plik $file.Name -ItemId '-' -Wynik "POMINIETO: em-dash ($($zle -join ','))"
        return @{ rc = 2 }
    }
    # LINK-LATER: [LINK-LATER: <slug> | <anchor>] -> jesli cel juz opublikowany (status
    # 'opublikowany' w kolejce), render <a href=/journal/<slug>>; inaczej sam anchor (bez 404)
    # + wpis do logu (fixup recznie/przy rozbudowie). Skladnia celowo INNA niz [LINK:] (bramka).
    if ($content -match '\[LINK-LATER:') {
        $content = [regex]::Replace($content, '\[LINK-LATER:\s*([^\]|]+?)\s*\|\s*([^\]]+?)\s*\]', {
            param($m)
            $slug2 = $m.Groups[1].Value.Trim(); $anchor = $m.Groups[2].Value.Trim()
            $published = $false
            Get-ChildItem $queueDir -Filter "*_$slug2.json" -ErrorAction SilentlyContinue | ForEach-Object {
                try { $o = (Read-TextWithRetry -Path $_.FullName -Etykieta 'linklater') | ConvertFrom-Json
                      if ($o.status -eq 'opublikowany') { $published = $true } } catch {}
            }
            if ($published) { "<a href=`"https://mindsync.app/journal/$slug2`">$anchor</a>" }
            else {
                Write-Host "  LINK-LATER: cel '$slug2' jeszcze nieopublikowany -> sam anchor (fixup pozniej)." -ForegroundColor Yellow
                Write-DripLog -Plik $file.Name -ItemId '-' -Wynik "LINK-LATER pominiety: $slug2"
                $anchor
            }
        })
    }

    # BRAMKA 3: render kart funkcji
    if ($content -match '\[FEATURES?:') {
        try { $content = Expand-FeatureCards -Content $content } catch {
            Write-Host "  OSTRZEZENIE: render kart nieudany ($($_.Exception.Message)) -> NIE publikuje." -ForegroundColor Yellow
            Write-DripLog -Plik $file.Name -ItemId '-' -Wynik 'POMINIETO: blad renderu kart FEATURE'
            return @{ rc = 2 }
        }
        $rest = [regex]::Matches($content, '\[FEATURES?:[^\]]*\]')
        if ($rest.Count -gt 0) {
            Write-Host "  OSTRZEZENIE: nierozwiazane karty po renderze ($($rest.Count)) -> NIE publikuje." -ForegroundColor Yellow
            Write-DripLog -Plik $file.Name -ItemId '-' -Wynik "POMINIETO: surowe [FEATURE:] ($($rest.Count))"
            return @{ rc = 2 }
        }
    }
    # BRAMKA 4: hero na dysku (drip NIE generuje grafik)
    $heroPath  = Find-HeroFile $item '1600x900'
    $thumbPath = Find-HeroFile $item '800x600'
    if (-not $heroPath) {
        if ($BodyOnly) {
            Write-Host '  INFO: brak pliku hero-1600x900 na dysku (bez znaczenia w -BodyOnly: hero nie jest wysylane).' -ForegroundColor DarkGray
        } else {
            Write-Host '  OSTRZEZENIE: brak pliku hero-1600x900 -> NIE publikuje.' -ForegroundColor Yellow
            Write-DripLog -Plik $file.Name -ItemId '-' -Wynik 'POMINIETO: brak pliku hero'
            return @{ rc = 2 }
        }
    }
    if (-not $thumbPath) { $thumbPath = $heroPath }   # fallback: thumbnail = hero
    # BRAMKA 5: zajawka
    if (-not ($item.zajawka_html -and "$($item.zajawka_html)".Trim())) {
        if ($BodyOnly) {
            Write-Host '  INFO: brak zajawki w kolejce (bez znaczenia w -BodyOnly: post-summary nie jest wysylane).' -ForegroundColor DarkGray
        } else {
            Write-Host '  OSTRZEZENIE: brak zajawki (post-summary) -> NIE publikuje.' -ForegroundColor Yellow
            Write-DripLog -Plik $file.Name -ItemId '-' -Wynik 'POMINIETO: brak zajawki'
            return @{ rc = 2 }
        }
    }
    return @{ rc = 0; content = $content; heroPath = $heroPath; thumbPath = $thumbPath }
}

# =====================================================================================
#  PUBLIKACJA JEDNEGO WPISU (wspolna dla trybow; zwraca 0 = opublikowano/DRY, 2 = pomin, 1 = blad)
# =====================================================================================
function Publish-QueueItem {
    param($file, $item, [ref]$log)
    $tytul = $item.tytul; $slug = "$($item.seo_url)".Trim()
    Write-Host "`n--- $($file.Name) :: '$tytul' (planowana=$($item.planowana_data)) ---" -ForegroundColor Cyan

    if (-not $slug) {
        Write-Host '  POMIJAM: brak seo_url (slug wymagany w Webflow).' -ForegroundColor Yellow
        Write-DripLog -Plik $file.Name -ItemId '-' -Wynik 'POMINIETO: brak seo_url'
        return 2
    }
    if (Already-Published $log.Value $slug) {
        Write-Host '  POMIJAM: slug juz w published-log.json (idempotencja).' -ForegroundColor DarkGray
        Write-DripLog -Plik $file.Name -ItemId '-' -Wynik 'POMINIETO: juz w published-log'
        return 2
    }

    # BRAMKI 1-5 + render LINK-LATER i kart [FEATURE:] (wspolne z -Republish, patrz Invoke-QueueItemGates)
    $g = Invoke-QueueItemGates -file $file -item $item
    if ($g -is [array]) { $g = $g[-1] }
    if ($g.rc -ne 0) { return $g.rc }
    $content = $g.content; $heroPath = $g.heroPath; $thumbPath = $g.thumbPath

    if ($DryRun) {
        $fd = Build-FieldData -item $item -Content $content -HeroUrl '(DRY: upload pominiety)' -ThumbUrl '(DRY)'
        Write-Host '  [DRY-RUN] NIE wysylam. fieldData ktore BY poszlo:' -ForegroundColor Magenta
        Write-Host ("      name='$($fd.name)'  slug='$($fd.slug)'  category=$($item.kategoria)  featured=$($fd.featured)  color=$($fd.color)") -ForegroundColor Magenta
        Write-Host ("      seo-title='$($fd['seo-title'])'") -ForegroundColor Magenta
        Write-Host ("      seo-description='$($fd['seo-description'])'") -ForegroundColor Magenta
        Write-Host ("      hero=$heroPath") -ForegroundColor Magenta
        Write-Host ("      thumb=$thumbPath") -ForegroundColor Magenta
        Write-Host ("      body_len=$($content.Length)  schema=$([bool]$item.schema_jsonld)") -ForegroundColor Magenta
        Write-Host ("      URL po publikacji: https://mindsync.app/journal/$slug") -ForegroundColor Magenta
        Write-DripLog -Plik $file.Name -ItemId '-' -Wynik "DRY-RUN: WYBRANO do publikacji (hero=$([IO.Path]::GetFileName($heroPath)))"
        $script:sitePublishNeeded = $true      # po tym wpisie szedlby krok publikacji calej strony
        return 0
    }

    # --- LIVE: upload assetow ---
    Write-Host '  [1/4] upload hero do Webflow Assets...' -ForegroundColor DarkCyan
    $heroUrl  = Publish-WfAsset -FilePath $heroPath -Etykieta 'hero'
    $thumbUrl = if ($thumbPath -eq $heroPath) { $heroUrl } else { Publish-WfAsset -FilePath $thumbPath -Etykieta 'thumb' }

    # --- LIVE: create lub update (idempotencja po slugu) ---
    Write-Host '  [2/4] create/update item (idempotencja po slugu)...' -ForegroundColor DarkCyan
    $fd = Build-FieldData -item $item -Content $content -HeroUrl $heroUrl -ThumbUrl $thumbUrl
    $existing = Get-ItemBySlug $slug
    $itemId = $null
    if ($existing) {
        $itemId = $existing.id
        Write-Host "      ISTNIEJE item $itemId -> PATCH (aktualizacja, NIE duplikuje)" -ForegroundColor Yellow
        $null = Invoke-WfApi -Method Patch -Path "/collections/$($script:collectionId)/items/$itemId" -Body @{ isDraft = $false; isArchived = $false; fieldData = $fd }
    } else {
        $created = Invoke-WfApi -Method Post -Path "/collections/$($script:collectionId)/items" -Body @{ isDraft = $false; isArchived = $false; fieldData = $fd }
        if ($created -and $created.id) { $itemId = $created.id }
        if (-not $itemId) {
            # weryfikacja GET (wzorzec anty-'wiszacy zapis': serwer mogl zapisac mimo braku odpowiedzi)
            $made = Get-ItemBySlug $slug
            if ($made) { $itemId = $made.id; Write-Host "      GET potwierdzil item $itemId" -ForegroundColor Green }
        }
    }
    if (-not $itemId) {
        Write-Host '  BLAD: create/update nie zwrocil id i GET nie potwierdzil.' -ForegroundColor Red
        Write-DripLog -Plik $file.Name -ItemId '-' -Wynik 'BLAD: brak item id po zapisie'
        return 1
    }

    # --- LIVE: publish item (na zywa strone) ---
    Write-Host "  [3/4] publish item $itemId..." -ForegroundColor DarkCyan
    $null = Invoke-WfApi -Method Post -Path "/collections/$($script:collectionId)/items/publish" -Body @{ itemIds = @($itemId) }

    # weryfikacja: GET item -> lastPublished niepuste
    $check = Invoke-WfApi -Method Get -Path "/collections/$($script:collectionId)/items/$itemId"
    $publishedOk = [bool]($check -and $check.lastPublished)
    Write-Host "      lastPublished=$($check.lastPublished)  isDraft=$($check.isDraft)" -ForegroundColor $(if ($publishedOk) { 'Green' } else { 'Yellow' })

    # --- [4/4] log + status=opublikowany ---
    Write-Host '  [4/4] log + status=opublikowany...' -ForegroundColor DarkCyan
    $permalink = "https://mindsync.app/journal/$slug"
    $entry = [pscustomobject]@{
        tytul = $tytul; slug = $slug; item_id = "$itemId"; permalink = $permalink
        data = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss'); plik = $file.Name
        published_ok = $publishedOk; opublikowano_przez = 'webflow/blog-publish.ps1'
    }
    $log.Value = @($log.Value) + $entry
    Save-Log $log.Value

    $item | Add-Member -NotePropertyName item_id   -NotePropertyValue "$itemId"  -Force
    $item | Add-Member -NotePropertyName permalink -NotePropertyValue $permalink -Force
    $item.status = 'opublikowany'
    ($item | ConvertTo-Json -Depth 14) | Set-Content $file.FullName -Encoding utf8

    Write-Host "  ZROBIONE: $permalink" -ForegroundColor Green
    Write-DripLog -Plik $file.Name -ItemId "$itemId" -Wynik "OK opublikowano (published=$publishedOk)"
    $script:sitePublishNeeded = $true          # wpis stoi na zywo -> strona wymaga publikacji (sitemap.xml)
    return 0
}

# =====================================================================================
#  ODSWIEZANIE OPUBLIKOWANYCH WPISOW: -Republish [-BodyOnly] [-KeepHero]  (dodane 2026-10-21)
# -------------------------------------------------------------------------------------
#  PO CO: idempotencja (published-log.json + status 'opublikowany') nie pozwala wyslac
#  opublikowanego wpisu drugi raz, a czasem trzeba: przepisany wpis (tresc, meta, schema,
#  hero) albo nowe zrzuty aplikacji. Zrzuty siedza w dwoch miejscach: inline <img>
#  w tresc_html oraz karty [FEATURE:], ktore przy publikacji biora `screenshot`
#  z blog/app-features.json i zostaja WPIECZONE w post-body. Zmiana katalogu funkcji nie
#  zmienia wiec niczego na zywo, dopoki post-body nie zostanie wyslane ponownie.
#
#  CO ROBI: tylko wpisy ze statusem 'opublikowany', ktorych item ISTNIEJE w Webflow (GET po
#  item_id z kolejki albo logu + kontrola sluga; bez item_id GET po slugu), ma niepuste
#  lastPublished i nie jest draft/archived. Pomija WYLACZNIE bramke Already-Published.
#  Bramki 1-3 (LINK, em-dash, karty) bez zmian; 4-5 (hero, zajawka) tez, a w -BodyOnly
#  tylko informuja. Render post-body: ta sama funkcja co przy publikacji
#  (Invoke-QueueItemGates: LINK-LATER + karty FEATURE).
#  Zapis: PATCH istniejacego itemu + POST items/publish dla JEDNEGO itemId.
#  NIGDY: tworzenie itemu, publikacja calej strony, kontrola odkrywania, GSC, zmiana kolejki
#  (status zostaje 'opublikowany', plik kolejki nie jest przepisywany).
#    -BodyOnly : PATCH { fieldData: { post-body } } i nic wiecej (bez isDraft/isArchived).
#    pelny     : PATCH jak przy publikacji (wszystkie pola z kolejki). main-image
#                i thumbnail-image wgrywane TYLKO gdy plik sie zmienil: MD5 z published-log
#                (hero_md5 + hero_url zgodny z obecnym) albo MD5 pliku pobranego z CDN.
#                CDN serwuje oryginal bajt w bajt, takze kopie w buckecie CMS (sprawdzone
#                21.10 na hero i zrzutach). Plik bez zmian, ale inny alt = upload, bo alt
#                siedzi w polu obrazka. -KeepHero: oba obrazki bez zmian, bez wyjatkow.
#  DryRun (domyslnie): GET itemu (sam odczyt) i porownanie post-body na zywo z renderem:
#  obrazki (wyrownane jak w diffie, old -> new), linki, tekst widoczny dla czytelnika.
#  Obrazki porownujemy po nazwie pliku zrodla: Webflow przy zapisie RichText kopiuje kazdy
#  obrazek do bucketu CMS jako <bucket>/<24 hex>_<nazwa zrodla> (sprawdzone 21.10).
#  Roznica tekstu albo linkow (poza linkami z LINK-LATER) = UWAGA: PATCH nadpisze tresc
#  na zywo, czyli edycje zrobiona w CMS poza kolejka albo poprawke kolejki po publikacji.
#  LOG: published-log.json, aktualizacja ISTNIEJACEGO wpisu o tym slugu (odswiezono,
#  odswiezono_tryb, odswiezono_ok, odswiezen, po pelnym tez hero_md5/hero_url/thumb_*).
#  Pole `data` (pierwsza publikacja) NIE jest ruszane: czyta je kontrola odkrywania
#  (3 najnowsze wpisy na Home, lastmod /blog) i stary wpis z nowa data udawalby najnowszy.
#  Tempo: $ItemPauseSec miedzy wpisami + $ThrottleMs po kazdym wywolaniu API; 4 wywolania
#  na wpis w LIVE -BodyOnly daja ok. 40 req/min przy limicie Webflow 60 req/min.
# =====================================================================================

function Get-UrlFileKey {
    # Ostatni segment sciezki URL-a (bez query i fragmentu), zdekodowany. Klucz porownania obrazkow.
    param([string]$Url)
    if (-not "$Url".Trim()) { return '' }
    $u = ("$Url".Trim() -split '[?#]', 2)[0]
    $seg = ($u -split '/')[-1]
    try { $seg = [Uri]::UnescapeDataString($seg) } catch {}
    return $seg
}

function Test-SameImage {
    # Czy obrazek na zywo i obrazek z renderu kolejki to ten sam plik zrodlowy.
    # Na zywo: <bucket CMS>/<24 hex>_<nazwa zrodla>; z kolejki: <bucket>/<nazwa zrodla>.
    param([string]$LiveUrl, [string]$NewUrl)
    if (-not "$LiveUrl".Trim() -or -not "$NewUrl".Trim()) { return $false }
    if ($LiveUrl -eq $NewUrl) { return $true }
    $l = Get-UrlFileKey $LiveUrl
    $n = Get-UrlFileKey $NewUrl
    if (-not $n) { return $false }
    if ($l -eq $n) { return $true }
    return [bool]($l -match ('^[0-9a-f]{24}_' + [regex]::Escape($n) + '$'))
}

function Get-HtmlImgSrcs {
    param([string]$Html)
    foreach ($m in [regex]::Matches("$Html", '<img\b[^>]*?\bsrc\s*=\s*"([^"]*)"', 'IgnoreCase')) {
        [Net.WebUtility]::HtmlDecode($m.Groups[1].Value)
    }
}

function Get-HtmlHrefs {
    param([string]$Html)
    foreach ($m in [regex]::Matches("$Html", '<a\b[^>]*?\bhref\s*=\s*"([^"]*)"', 'IgnoreCase')) {
        ([Net.WebUtility]::HtmlDecode($m.Groups[1].Value)).Trim()
    }
}

function ConvertTo-PlainText {
    # Tekst widoczny dla czytelnika: bez tagow, encje zdekodowane, bez znakow zerowej
    # szerokosci (Webflow wstawia U+200D w puste akapity), biale znaki scisniete.
    param([string]$Html)
    # tagi inline znikaja bez spacji (inaczej "<a>slowo</a>." dalby "slowo ."), blokowe -> spacja
    $t = "$Html" -replace '</?(a|strong|em|b|i|u|code|span|sup|sub|small|mark)\b[^>]*>', ''
    $t = $t -replace '<[^>]+>', ' '
    $t = [Net.WebUtility]::HtmlDecode($t)
    $t = $t -replace ('[' + [char]0x200B + [char]0x200C + [char]0x200D + [char]0x2060 + [char]0xFEFF + ']'), ''
    $t = $t.Replace([string][char]0x00A0, ' ')
    return (($t -replace '\s+', ' ').Trim())
}

function Get-TextDiffSnippet {
    # Wspolny prefiks i sufiks dwoch tekstow -> fragment, ktory sie rozni (z kontekstem).
    param([string]$Zywy, [string]$Nowy, [int]$Ctx = 40, [int]$Max = 220)
    $n = [Math]::Min($Zywy.Length, $Nowy.Length)
    $p = 0
    while ($p -lt $n -and $Zywy[$p] -ceq $Nowy[$p]) { $p++ }
    $s = 0
    while ($s -lt ($n - $p) -and $Zywy[$Zywy.Length - 1 - $s] -ceq $Nowy[$Nowy.Length - 1 - $s]) { $s++ }
    $wytnij = {
        param([string]$T, [int]$Od, [int]$Do)
        $poczatek = [Math]::Max(0, $Od - $Ctx)
        $koniec = [Math]::Min($T.Length, $Do + $Ctx)
        $frag = $T.Substring($poczatek, [Math]::Max(0, $koniec - $poczatek))
        if ($frag.Length -gt $Max) { $frag = $frag.Substring(0, $Max) + '...' }
        $frag
    }
    return [pscustomobject]@{
        pozycja  = $p
        zywy     = (& $wytnij $Zywy $p ($Zywy.Length - $s))
        nowy     = (& $wytnij $Nowy $p ($Nowy.Length - $s))
        zywyDlug = $Zywy.Length - $s - $p
        nowyDlug = $Nowy.Length - $s - $p
    }
}

function Compare-Multiset {
    # Roznica dwoch list z powtorzeniami: co doszlo w New, czego ubylo z Old.
    param([string[]]$Old, [string[]]$New)
    $cnt = New-Object 'System.Collections.Generic.Dictionary[string,int]'
    foreach ($x in @($Old)) {
        if ($null -eq $x) { continue }
        if ($cnt.ContainsKey($x)) { $cnt[$x] = $cnt[$x] + 1 } else { $cnt[$x] = 1 }
    }
    $added = @()
    foreach ($x in @($New)) {
        if ($null -eq $x) { continue }
        if ($cnt.ContainsKey($x) -and $cnt[$x] -gt 0) { $cnt[$x] = $cnt[$x] - 1 } else { $added += $x }
    }
    $removed = @()
    foreach ($k in @($cnt.Keys)) { for ($i = 0; $i -lt $cnt[$k]; $i++) { $removed += $k } }
    return [pscustomobject]@{ added = $added; removed = $removed }
}

function Get-ImageAlignment {
    # Wyrownanie list obrazkow (na zywo -> po renderze) jak w diffie: same/changed/added/removed.
    # Dodanie zrzutu w srodku wpisu nie oznacza wtedy wszystkich kolejnych jako zmienionych.
    param([string[]]$Old, [string[]]$New)
    $Old = @($Old | Where-Object { $_ })
    $New = @($New | Where-Object { $_ })
    $n = $Old.Count; $m = $New.Count
    $d = @{}
    for ($i = 0; $i -le $n; $i++) { $d["$i|0"] = $i }
    for ($j = 0; $j -le $m; $j++) { $d["0|$j"] = $j }
    for ($i = 1; $i -le $n; $i++) {
        for ($j = 1; $j -le $m; $j++) {
            $c = 1; if (Test-SameImage ($Old[$i - 1]) ($New[$j - 1])) { $c = 0 }
            $v = [Math]::Min($d["$($i - 1)|$j"] + 1, $d["$i|$($j - 1)"] + 1)
            $d["$i|$j"] = [Math]::Min($v, $d["$($i - 1)|$($j - 1)"] + $c)
        }
    }
    $ops = New-Object System.Collections.ArrayList
    $i = $n; $j = $m
    while ($i -gt 0 -or $j -gt 0) {
        if ($i -gt 0 -and $j -gt 0) {
            $same = Test-SameImage ($Old[$i - 1]) ($New[$j - 1])
            $c = 1; if ($same) { $c = 0 }
            if ($d["$i|$j"] -eq ($d["$($i - 1)|$($j - 1)"] + $c)) {
                $op = 'changed'; if ($same) { $op = 'same' }
                [void]$ops.Insert(0, [pscustomobject]@{ op = $op; old = $Old[$i - 1]; new = $New[$j - 1] })
                $i--; $j--; continue
            }
        }
        if ($i -gt 0 -and $d["$i|$j"] -eq ($d["$($i - 1)|$j"] + 1)) {
            [void]$ops.Insert(0, [pscustomobject]@{ op = 'removed'; old = $Old[$i - 1]; new = $null })
            $i--; continue
        }
        [void]$ops.Insert(0, [pscustomobject]@{ op = 'added'; old = $null; new = $New[$j - 1] })
        $j--
    }
    foreach ($o in $ops) { $o }
}

function Get-HtmlTagSequence {
    # Sekwencja nazw tagow (bez atrybutow), BEZ a/img/figure: te ocenia porownanie linkow
    # i obrazkow. Webflow zapisuje znacznik RichText doslownie (sprawdzone 21.10: jedyna
    # roznica po zapisie to prefiks kopii w src obrazka), wiec inna sekwencja = inna struktura
    # (np. h3 zamiast h2, lista zamiast akapitow) nawet przy identycznym tekscie.
    param([string]$Html)
    $pomin = @('a', '/a', 'img', 'figure', '/figure')
    foreach ($m in [regex]::Matches("$Html", '<\s*(/?)([a-zA-Z][a-zA-Z0-9]*)')) {
        $t = ($m.Groups[1].Value + $m.Groups[2].Value).ToLower()
        if ($pomin -notcontains $t) { $t }
    }
}

function Compare-PostBody {
    # Porownanie post-body na zywo (item w Webflow) z renderem z kolejki w czterech warstwach:
    # obrazki, linki (z podzialem na odrobione LINK-LATER), struktura tagow i tekst widoczny.
    param([string]$Live, [string]$New, [string]$QueueHtml)
    $ops = @(Get-ImageAlignment -Old @(Get-HtmlImgSrcs $Live) -New @(Get-HtmlImgSrcs $New))
    $imgChanged = @($ops | Where-Object { $_.op -ne 'same' }).Count
    $hd = Compare-Multiset -Old @(Get-HtmlHrefs $Live) -New @(Get-HtmlHrefs $New)
    $ll = @{}
    foreach ($m in [regex]::Matches("$QueueHtml", '\[LINK-LATER:\s*([^\]|]+?)\s*\|')) {
        $ll["https://mindsync.app/journal/$($m.Groups[1].Value.Trim())"] = $true
    }
    $addedLL    = @(@($hd.added) | Where-Object { $_ -and $ll.ContainsKey($_) })
    $addedOther = @(@($hd.added) | Where-Object { $_ -and -not $ll.ContainsKey($_) })
    $removed    = @(@($hd.removed) | Where-Object { $_ })
    $lt = ConvertTo-PlainText $Live
    $nt = ConvertTo-PlainText $New
    $textSame = [string]::Equals($lt, $nt, [StringComparison]::Ordinal)
    $snip = $null
    if (-not $textSame) { $snip = Get-TextDiffSnippet -Zywy $lt -Nowy $nt }
    $sl = @(Get-HtmlTagSequence $Live)
    $sn = @(Get-HtmlTagSequence $New)
    $structSame = [string]::Equals(($sl -join ','), ($sn -join ','), [StringComparison]::Ordinal)
    $structInfo = ''
    if (-not $structSame) {
        $k = 0
        while ($k -lt $sl.Count -and $k -lt $sn.Count -and $sl[$k] -ceq $sn[$k]) { $k++ }
        $od = [Math]::Max(0, $k - 3)
        $zyw = @($sl | Select-Object -Skip $od -First 8) -join ' '
        $now = @($sn | Select-Object -Skip $od -First 8) -join ' '
        $structInfo = "tagow na zywo $($sl.Count), po renderze $($sn.Count); pierwsza roznica przy tagu nr $($k + 1): na zywo [$zyw], po renderze [$now]"
    }
    $beyond = (-not $textSame) -or (-not $structSame) -or ($removed.Count -gt 0) -or ($addedOther.Count -gt 0)
    return [pscustomobject]@{
        ops = $ops; imgChanged = $imgChanged
        addedLL = $addedLL; addedOther = $addedOther; removed = $removed
        textSame = $textSame; snip = $snip; liveTextLen = $lt.Length; newTextLen = $nt.Length
        structSame = $structSame; structInfo = $structInfo
        beyond = $beyond
    }
}

function Get-FieldDiffs {
    # Pola poza post-body i obrazkami, ktore pelny PATCH zmieni wzgledem itemu w Webflow.
    param($Fd, $LiveFd)
    $liveNames = @()
    if ($LiveFd) { $liveNames = @($LiveFd.PSObject.Properties.Name) }
    foreach ($k in @($Fd.Keys)) {
        if (@('post-body', 'main-image', 'thumbnail-image') -contains $k) { continue }
        $nv = $Fd[$k]; $lv = $null
        if ($liveNames -contains $k) { $lv = $LiveFd.$k }
        $ns = "$nv"; $ls = "$lv"
        if ($nv -is [bool]) { $ns = $ns.ToLower(); if ($null -eq $lv) { $ls = 'false' } }
        if ($lv -is [bool]) { $ls = $ls.ToLower() }
        if (-not [string]::Equals($ns, $ls, [StringComparison]::Ordinal)) {
            [pscustomobject]@{ pole = $k; zywy = $ls; nowy = $ns }
        }
    }
}

function Get-RemoteMd5 {
    # MD5 pliku z CDN Webflow (publiczny GET, bez tokenu, zero zapisu). Blad -> $null.
    param([string]$Url)
    if (-not "$Url".Trim()) { return $null }
    try {
        $req = [System.Net.HttpWebRequest]::Create($Url)
        $req.Method = 'GET'
        $req.UserAgent = 'MindSync-blog-publish/1.0 (republish: porownanie MD5 hero)'
        $tms = $WriteDeadlineSec * 1000
        $req.Timeout = $tms; $req.ReadWriteTimeout = $tms; $req.KeepAlive = $false
        $resp = $req.GetResponse()
        $buf = New-Object IO.MemoryStream
        $resp.GetResponseStream().CopyTo($buf)
        $resp.Close()
        return (Get-FileMd5Hex -Bytes $buf.ToArray())
    } catch { return $null }
}

function Get-ImageUploadPlan {
    # Decyzja dla jednego pola obrazka w pelnym -Republish: 'zostaw' (pole NIE idzie w PATCH,
    # Webflow trzyma obecny obrazek) albo 'upload' (nowy asset przez Publish-WfAsset).
    param([string]$Etykieta, [string]$LocalPath, $LiveImage, [string]$NewAlt, [string]$LogMd5, [string]$LogUrl)
    $liveUrl = ''; $liveAlt = ''
    if ($LiveImage) { $liveUrl = "$($LiveImage.url)"; $liveAlt = "$($LiveImage.alt)" }
    $plan = [pscustomobject]@{ pole = $Etykieta; akcja = 'zostaw'; powod = ''; md5 = $null; liveUrl = $liveUrl; plik = $LocalPath }
    if ($KeepHero) {
        $plan.powod = '-KeepHero'
        if ($liveUrl -and $liveAlt -cne $NewAlt) { $plan.powod += " (UWAGA: alt w polu obrazka zostaje stary: '$liveAlt')" }
        return $plan
    }
    if (-not $LocalPath) { $plan.powod = 'brak pliku na dysku, zostaje obecny obrazek'; return $plan }
    $plan.md5 = Get-FileMd5Hex -Bytes (Read-FileBytesWithRetry -Path $LocalPath -Etykieta $Etykieta)
    if (-not $liveUrl) { $plan.akcja = 'upload'; $plan.powod = 'item nie ma tego obrazka'; return $plan }
    $prev = $null; $zrodlo = 'CDN'
    if ($LogMd5 -and $LogUrl -and $LogUrl -eq $liveUrl) { $prev = $LogMd5; $zrodlo = 'published-log' }
    else { $prev = Get-RemoteMd5 -Url $liveUrl }
    if (-not $prev) {
        $plan.akcja = 'upload'; $plan.powod = "nie ustalilem MD5 obecnego pliku (zrodlo: $zrodlo), wgrywam dla pewnosci"
        return $plan
    }
    if ($prev -ne $plan.md5) {
        $plan.akcja = 'upload'; $plan.powod = "plik zmieniony (MD5 $prev -> $($plan.md5), zrodlo: $zrodlo)"
        return $plan
    }
    if ($liveAlt -cne $NewAlt) {
        $plan.akcja = 'upload'; $plan.powod = "plik bez zmian (MD5 zgodne, zrodlo: $zrodlo), ale alt sie zmienil ('$liveAlt' -> '$NewAlt'), a alt siedzi w polu obrazka"
        return $plan
    }
    $plan.powod = "plik bez zmian (MD5 zgodne, zrodlo: $zrodlo), nie wgrywam"
    return $plan
}

function Get-WfItemForRepublish {
    # Item do odswiezenia: najpierw GET po item_id (kontrola sluga), potem GET po slugu.
    # Zwraca $null, gdy itemu nie ma. Republish NIGDY nie tworzy itemu.
    param([string]$ItemId, [string]$Slug)
    if ($ItemId) {
        $it = $null
        try { $it = Invoke-WfApi -Method Get -Path "/collections/$($script:collectionId)/items/$ItemId" }
        catch { if ("$($_.Exception.Message)" -match 'HTTP 404') { $it = $null } else { throw } }
        if ($it) {
            if ("$($it.fieldData.slug)" -ne $Slug) {
                throw "item $ItemId ma w Webflow slug '$($it.fieldData.slug)', a kolejka '$Slug' (niespojnosc, nie ruszam)"
            }
            return $it
        }
    }
    return (Get-ItemBySlug $Slug)
}

function Update-LogAfterRepublish {
    # Odswiezenie wpisu w published-log.json BEZ duplikowania sluga. Pole `data` zostaje
    # (patrz naglowek sekcji). Zapis wylacznie przez Save-Log (-InputObject, nie potok).
    param([ref]$log, $file, $item, $wf, [string]$Tryb, [bool]$PublishedOk, [hashtable]$Extra)
    $slug = "$($item.seo_url)".Trim()
    $teraz = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
    $hit = @($log.Value | Where-Object { $_.slug -eq $slug } | Sort-Object { "$($_.data)" }) | Select-Object -Last 1
    if (-not $hit) {
        $dataPierwsza = $teraz
        $c = ConvertTo-UtcOrNull -S "$($wf.createdOn)"
        if ($c) { $dataPierwsza = $c.ToLocalTime().ToString('yyyy-MM-dd HH:mm:ss') }
        $hit = [pscustomobject]@{
            tytul = "$($item.tytul)"; slug = $slug; item_id = "$($wf.id)"; permalink = "https://mindsync.app/journal/$slug"
            data = $dataPierwsza; plik = $file.Name; published_ok = $PublishedOk; opublikowano_przez = 'webflow/blog-publish.ps1'
            odtworzony = "${teraz}: sluga nie bylo w logu, dopisany przy -Republish; data = createdOn itemu z Webflow"
        }
        $log.Value = @($log.Value) + $hit
    }
    $n = 0
    try { $n = [int]"$($hit.odswiezen)" } catch {}
    $hit | Add-Member -NotePropertyName odswiezono      -NotePropertyValue $teraz -Force
    $hit | Add-Member -NotePropertyName odswiezono_tryb -NotePropertyValue $Tryb -Force
    $hit | Add-Member -NotePropertyName odswiezono_ok   -NotePropertyValue $PublishedOk -Force
    $hit | Add-Member -NotePropertyName odswiezen       -NotePropertyValue ($n + 1) -Force
    if ($Tryb -eq 'pelny') { $hit | Add-Member -NotePropertyName tytul -NotePropertyValue "$($item.tytul)" -Force }
    if ($Extra) {
        foreach ($k in @($Extra.Keys)) {
            if ($null -ne $Extra[$k]) { $hit | Add-Member -NotePropertyName $k -NotePropertyValue $Extra[$k] -Force }
        }
    }
    Save-Log $log.Value
}

function Republish-QueueItem {
    # Zwraca 0 = odswiezono albo DRY, 2 = pominieto, 1 = blad. Statystyki przebiegu w $stats.
    param($file, $item, [ref]$log, $stats)
    $slug = "$($item.seo_url)".Trim()
    $trybTag = 'PELNY'
    if ($BodyOnly) { $trybTag = 'BODY-ONLY' }
    Write-Host "`n--- $($file.Name) :: '$($item.tytul)' [REPUBLISH $trybTag] ---" -ForegroundColor Cyan
    $stats.wpisy = $stats.wpisy + 1

    # WARUNEK WEJSCIA: Already-Published pomijamy WYLACZNIE dla wpisow 'opublikowany'
    if ("$($item.status)" -ne 'opublikowany') {
        Write-Host "  POMIJAM: status '$($item.status)'. -Republish odswieza tylko wpisy 'opublikowany'; nowy wpis idzie zwyklym trybem (bez -Republish)." -ForegroundColor Yellow
        $stats.pominiete += $file.Name
        return 2
    }
    if (-not $slug) {
        Write-Host '  POMIJAM: brak seo_url (slug wymagany w Webflow).' -ForegroundColor Yellow
        $stats.pominiete += $file.Name
        return 2
    }
    $logHit = @($log.Value | Where-Object { $_.slug -eq $slug } | Sort-Object { "$($_.data)" }) | Select-Object -Last 1
    $itemId = "$($item.item_id)".Trim()
    if ($logHit -and "$($logHit.item_id)".Trim()) {
        if (-not $itemId) { $itemId = "$($logHit.item_id)".Trim() }
        elseif ("$($logHit.item_id)".Trim() -ne $itemId) {
            Write-Host "  UWAGA: item_id w kolejce ($itemId) rozni sie od published-log ($($logHit.item_id)); biore z kolejki i sprawdzam slug w Webflow." -ForegroundColor Yellow
        }
    }
    if (-not $logHit) { Write-Host '  UWAGA: sluga nie ma w published-log.json; po udanym odswiezeniu wpis zostanie dopisany (bez duplikatu).' -ForegroundColor Yellow }

    # BRAMKI + render (ta sama funkcja co przy publikacji nowego wpisu)
    $g = Invoke-QueueItemGates -file $file -item $item -BodyOnly:$BodyOnly
    if ($g -is [array]) { $g = $g[-1] }
    if ($g.rc -ne 0) { $stats.pominiete += $file.Name; return $g.rc }
    $content = $g.content; $heroPath = $g.heroPath; $thumbPath = $g.thumbPath

    $qImg    = [regex]::Matches("$($item.tresc_html)", '<img\b', 'IgnoreCase').Count
    $qCards  = [regex]::Matches("$($item.tresc_html)", '\[FEATURES?:').Count
    $newImgs = @(Get-HtmlImgSrcs $content)
    if ($qImg -gt 0)          { $stats.zInlineImg += $file.Name }
    if ($qCards -gt 0)        { $stats.zKartami += $file.Name }
    if ($newImgs.Count -gt 0) { $stats.zObrazkami += $file.Name }
    Write-Host "  kolejka: inline <img> = $qImg | karty [FEATURE(S):] = $qCards | obrazkow w post-body po renderze = $($newImgs.Count)" -ForegroundColor Gray

    # ITEM W WEBFLOW (GET, takze w DryRun: sam odczyt)
    $wf = $null
    try { $wf = Get-WfItemForRepublish -ItemId $itemId -Slug $slug } catch {
        $powod = "$($_.Exception.Message)" -replace '\s+', ' '
        if ($powod.Length -gt 300) { $powod = $powod.Substring(0, 300) }
        Write-Host "  POMIJAM: nie odczytalem itemu z Webflow ($powod)." -ForegroundColor Yellow
        if (-not $DryRun) { Write-DripLog -Plik $file.Name -ItemId $itemId -Wynik "REPUBLISH POMINIETO: odczyt itemu ($powod)" }
        $stats.pominiete += $file.Name
        return 2
    }
    if (-not $wf) {
        Write-Host "  POMIJAM: itemu nie ma w Webflow (item_id='$itemId', slug='$slug'). -Republish nigdy nie tworzy nowego itemu." -ForegroundColor Yellow
        if (-not $DryRun) { Write-DripLog -Plik $file.Name -ItemId $itemId -Wynik 'REPUBLISH POMINIETO: brak itemu w Webflow' }
        $stats.pominiete += $file.Name
        return 2
    }
    if ($itemId -and "$($wf.id)" -ne $itemId) {
        Write-Host "  UWAGA: item_id $itemId nie istnieje, ale slug '$slug' ma item $($wf.id); odswiezam ten znaleziony po slugu." -ForegroundColor Yellow
    }
    $itemId = "$($wf.id)"
    if (-not "$($wf.lastPublished)".Trim()) {
        Write-Host '  POMIJAM: item nigdy nie byl opublikowany (lastPublished puste). Publish wypchnalby rekord trzymany poza strona (wpadka 22.09: wskrzeszone wpisy demo).' -ForegroundColor Yellow
        if (-not $DryRun) { Write-DripLog -Plik $file.Name -ItemId $itemId -Wynik 'REPUBLISH POMINIETO: item bez lastPublished' }
        $stats.pominiete += $file.Name
        return 2
    }
    if ($wf.isDraft -or $wf.isArchived) {
        Write-Host "  POMIJAM: item ma isDraft=$($wf.isDraft), isArchived=$($wf.isArchived); odswiezenie przywrociloby go na strone. To decyzja operatora." -ForegroundColor Yellow
        if (-not $DryRun) { Write-DripLog -Plik $file.Name -ItemId $itemId -Wynik 'REPUBLISH POMINIETO: item draft/archived' }
        $stats.pominiete += $file.Name
        return 2
    }
    Write-Host "  Webflow: item $itemId | lastPublished=$($wf.lastPublished) | lastUpdated=$($wf.lastUpdated)" -ForegroundColor Gray
    $luU = ConvertTo-UtcOrNull -S "$($wf.lastUpdated)"
    $lpU = ConvertTo-UtcOrNull -S "$($wf.lastPublished)"
    if ($luU -and $lpU -and ($luU - $lpU).TotalSeconds -gt 5) {
        Write-Host '  UWAGA: item ma w CMS zmiany zapisane, ale NIEOPUBLIKOWANE (lastUpdated > lastPublished). Publish tego itemu wypchnie je na zywo razem z PATCH-em.' -ForegroundColor Yellow
        $stats.staged += $file.Name
    }

    # POROWNANIE post-body: na zywo (item w Webflow) vs render z kolejki
    $liveBody = "$($wf.fieldData.'post-body')"
    $cmp = Compare-PostBody -Live $liveBody -New $content -QueueHtml "$($item.tresc_html)"
    Write-Host "  post-body: po renderze $($content.Length) zn. | na zywo $($liveBody.Length) zn. | tekst widoczny: $($cmp.newTextLen) / $($cmp.liveTextLen) zn." -ForegroundColor Gray
    if (@($cmp.ops).Count -eq 0) {
        Write-Host '  obrazki: brak (ani na zywo, ani po renderze)' -ForegroundColor Gray
    } else {
        Write-Host "  obrazki (na zywo -> po renderze), zmienionych: $($cmp.imgChanged)" -ForegroundColor Gray
        $nr = 0
        foreach ($o in @($cmp.ops)) {
            $nr++
            switch ($o.op) {
                'same'    { Write-Host "    [$nr] =  $(Get-UrlFileKey $o.new)  (bez zmian)" -ForegroundColor DarkGray }
                'changed' { Write-Host "    [$nr] ~  $($o.old)" -ForegroundColor Magenta
                            Write-Host "          -> $($o.new)" -ForegroundColor Magenta }
                'added'   { Write-Host "    [$nr] +  (brak) -> $($o.new)" -ForegroundColor Magenta }
                'removed' { Write-Host "    [$nr] -  $($o.old) -> (usuniety)" -ForegroundColor Magenta }
            }
        }
    }
    if ($cmp.addedLL.Count -gt 0) {
        Write-Host "  linki z LINK-LATER, ktorych na zywo brak (cel opublikowany pozniej, PATCH je doda): $($cmp.addedLL -join ', ')" -ForegroundColor DarkCyan
    }
    if ($cmp.addedOther.Count -gt 0 -or $cmp.removed.Count -gt 0) {
        Write-Host '  UWAGA linki: inne niz na zywo.' -ForegroundColor Yellow
        foreach ($h in $cmp.removed)    { Write-Host "    - na zywo jest, po renderze brak: $h" -ForegroundColor Yellow }
        foreach ($h in $cmp.addedOther) { Write-Host "    + po renderze jest, na zywo brak: $h" -ForegroundColor Yellow }
    }
    if (-not $cmp.textSame) {
        Write-Host "  UWAGA tekst: rozni sie od pozycji $($cmp.snip.pozycja) (zmieniony odcinek: na zywo $($cmp.snip.zywyDlug) zn., po renderze $($cmp.snip.nowyDlug) zn.)" -ForegroundColor Yellow
        Write-Host "    na zywo     : ...$($cmp.snip.zywy)..." -ForegroundColor Yellow
        Write-Host "    po renderze : ...$($cmp.snip.nowy)..." -ForegroundColor Yellow
    }
    if (-not $cmp.structSame) {
        Write-Host "  UWAGA struktura HTML: $($cmp.structInfo)" -ForegroundColor Yellow
    }
    if ($cmp.imgChanged -gt 0) { $stats.zmianaObrazkow += $file.Name }
    if ($cmp.addedLL.Count -gt 0) { $stats.linkLater += $file.Name }
    if ($cmp.beyond) {
        $stats.pozaObrazkami += $file.Name
        Write-Host '  WERDYKT: ROZNICA POZA OBRAZKAMI. PATCH nadpisze tresc na zywo: edycje zrobiona w CMS poza kolejka albo poprawke kolejki po publikacji. Sprawdz przed LIVE.' -ForegroundColor Yellow
    } elseif ($cmp.imgChanged -gt 0 -or $cmp.addedLL.Count -gt 0) {
        $co = @()
        if ($cmp.imgChanged -gt 0) { $co += "obrazki ($($cmp.imgChanged))" }
        if ($cmp.addedLL.Count -gt 0) { $co += "linki LINK-LATER ($($cmp.addedLL.Count))" }
        Write-Host "  WERDYKT: zmiana tylko w zakresie: $($co -join ', '). Tekst i struktura identyczne." -ForegroundColor Green
    } else {
        Write-Host '  WERDYKT: post-body po renderze = to, co na zywo (obrazki, linki, struktura i tekst bez zmian).' -ForegroundColor Green
    }

    # PELNY tryb: pola poza post-body + plan hero/thumbnail
    $hp = $null; $tp = $null
    $fieldsTxt = "post-body ($($content.Length) zn.)"
    if (-not $BodyOnly) {
        $altNew = "$($item.tytul)"
        if ($item.hero_image_alt) { $altNew = "$($item.hero_image_alt)" }
        $fdPrev = Build-FieldData -item $item -Content $content -HeroUrl $null -ThumbUrl $null
        $diffs = @(Get-FieldDiffs -Fd $fdPrev -LiveFd $wf.fieldData)
        if ($diffs.Count -eq 0) {
            Write-Host '  pola poza post-body: bez zmian wzgledem Webflow' -ForegroundColor Gray
        } else {
            Write-Host "  pola poza post-body, ktore PATCH zmieni ($($diffs.Count)):" -ForegroundColor Magenta
            foreach ($df in $diffs) {
                if ($df.pole -eq 'schema-jsonld' -or $df.zywy.Length -gt 140 -or $df.nowy.Length -gt 140) {
                    Write-Host "    $($df.pole): $($df.zywy.Length) zn. -> $($df.nowy.Length) zn." -ForegroundColor Magenta
                } else {
                    Write-Host "    $($df.pole): '$($df.zywy)' -> '$($df.nowy)'" -ForegroundColor Magenta
                }
            }
        }
        $lhm = ''; $lhu = ''; $ltm = ''; $ltu = ''
        if ($logHit) { $lhm = "$($logHit.hero_md5)"; $lhu = "$($logHit.hero_url)"; $ltm = "$($logHit.thumb_md5)"; $ltu = "$($logHit.thumb_url)" }
        $hp = Get-ImageUploadPlan -Etykieta 'main-image' -LocalPath $heroPath -LiveImage $wf.fieldData.'main-image' -NewAlt $altNew -LogMd5 $lhm -LogUrl $lhu
        $tp = Get-ImageUploadPlan -Etykieta 'thumbnail-image' -LocalPath $thumbPath -LiveImage $wf.fieldData.'thumbnail-image' -NewAlt $altNew -LogMd5 $ltm -LogUrl $ltu
        foreach ($pl in @($hp, $tp)) {
            $kol = 'Gray'; if ($pl.akcja -eq 'upload') { $kol = 'Magenta' }
            Write-Host "  $($pl.pole): $($pl.akcja.ToUpper()), $($pl.powod)" -ForegroundColor $kol
            if ($pl.plik) { Write-Host "      plik: $($pl.plik)" -ForegroundColor DarkGray }
        }
        $polaTxt = @($fdPrev.Keys) -join ', '
        $fieldsTxt = "$polaTxt, main-image=$($hp.akcja), thumbnail-image=$($tp.akcja), isDraft=false, isArchived=false"
    }

    if ($DryRun) {
        Write-Host '  [DRY-RUN] NIE wysylam. Na zywo poszloby:' -ForegroundColor Magenta
        Write-Host "      PATCH $($script:ApiBase)/collections/$($script:collectionId)/items/$itemId" -ForegroundColor Magenta
        Write-Host "            pola: $fieldsTxt" -ForegroundColor Magenta
        Write-Host "      POST  $($script:ApiBase)/collections/$($script:collectionId)/items/publish  { itemIds: [$itemId] }" -ForegroundColor Magenta
        Write-Host '      bez publikacji calej strony; published-log: odswiezenie wpisu o tym slugu, bez nowego wpisu' -ForegroundColor Magenta
        $stats.ok += $file.Name
        return 0
    }

    # --- LIVE ---
    $prevPublished = "$($wf.lastPublished)"
    if ($BodyOnly) {
        $patch = @{ fieldData = [ordered]@{ 'post-body' = $content } }
    } else {
        Write-Host '  [1/4] hero/thumbnail: upload tylko gdy plik sie zmienil...' -ForegroundColor DarkCyan
        $heroUrl = $null; $thumbUrl = $null
        if ($hp.akcja -eq 'upload') { $heroUrl = Publish-WfAsset -FilePath $heroPath -Etykieta 'hero' }
        if ($tp.akcja -eq 'upload') {
            if ($thumbPath -eq $heroPath -and $heroUrl) { $thumbUrl = $heroUrl }
            else { $thumbUrl = Publish-WfAsset -FilePath $thumbPath -Etykieta 'thumb' }
        }
        $fd = Build-FieldData -item $item -Content $content -HeroUrl $heroUrl -ThumbUrl $thumbUrl
        $patch = @{ isDraft = $false; isArchived = $false; fieldData = $fd }
    }
    Write-Host "  [2/4] PATCH item $itemId ($fieldsTxt)..." -ForegroundColor DarkCyan
    $null = Invoke-WfApi -Method Patch -Path "/collections/$($script:collectionId)/items/$itemId" -Body $patch
    Write-Host "  [3/4] publish item $itemId..." -ForegroundColor DarkCyan
    try {
        $null = Invoke-WfApi -Method Post -Path "/collections/$($script:collectionId)/items/publish" -Body @{ itemIds = @($itemId) }
    } catch {
        throw "PATCH przeszedl, ale publish itemu $itemId padl (zmiana czeka zastagowana w CMS, nie na zywo): $($_.Exception.Message)"
    }
    $check = Invoke-WfApi -Method Get -Path "/collections/$($script:collectionId)/items/$itemId"
    $lpNew = ConvertTo-UtcOrNull -S "$($check.lastPublished)"
    $lpOld = ConvertTo-UtcOrNull -S $prevPublished
    $publishedOk = [bool]($lpNew -and ((-not $lpOld) -or ($lpNew -gt $lpOld)))
    $kolP = 'Yellow'; if ($publishedOk) { $kolP = 'Green' }
    Write-Host "      lastPublished $prevPublished -> $($check.lastPublished)" -ForegroundColor $kolP
    $po = @(Get-ImageAlignment -Old @(Get-HtmlImgSrcs "$($check.fieldData.'post-body')") -New $newImgs)
    $poZle = @($po | Where-Object { $_.op -ne 'same' }).Count
    if ($poZle -gt 0) {
        Write-Host "      UWAGA: po zapisie $poZle obrazkow w post-body nie zgadza sie z renderem (sprawdz wpis na zywo)." -ForegroundColor Yellow
    } else {
        Write-Host "      obrazki w post-body po zapisie zgodne z renderem ($($newImgs.Count))." -ForegroundColor Green
    }

    Write-Host '  [4/4] published-log.json: odswiezenie wpisu (bez duplikatu sluga)...' -ForegroundColor DarkCyan
    $trybLog = 'body-only'
    if (-not $BodyOnly) { $trybLog = 'pelny' }
    $extra = @{}
    if (-not $BodyOnly) {
        if ($hp -and $hp.md5) { $extra['hero_md5'] = $hp.md5; $extra['hero_url'] = "$($check.fieldData.'main-image'.url)" }
        if ($tp -and $tp.md5) { $extra['thumb_md5'] = $tp.md5; $extra['thumb_url'] = "$($check.fieldData.'thumbnail-image'.url)" }
    }
    Update-LogAfterRepublish -log $log -file $file -item $item -wf $check -Tryb $trybLog -PublishedOk $publishedOk -Extra $extra
    Write-DripLog -Plik $file.Name -ItemId $itemId -Wynik "OK odswiezono (republish $trybLog, obrazki zmienione=$($cmp.imgChanged), poza obrazkami=$($cmp.beyond), published=$publishedOk)"
    Write-Host "  ZROBIONE: https://mindsync.app/journal/$slug" -ForegroundColor Green
    $stats.ok += $file.Name
    return 0
}

function Invoke-RepublishRun {
    # Przebieg -Republish: -Plik (jeden wpis) albo -All (wszystkie 'opublikowany' z kolejki).
    # Zwraca kod wyjscia: 0 = bez bledow, 1 = blad.
    $trybTag = 'pelny'
    $trybOpis = 'PELNY (wszystkie pola z kolejki; hero i thumbnail tylko gdy plik sie zmienil)'
    if ($BodyOnly) { $trybTag = 'body-only'; $trybOpis = 'BODY-ONLY (wylacznie post-body)' }
    elseif ($KeepHero) { $trybOpis = 'PELNY z -KeepHero (main-image i thumbnail-image bez zmian)' }
    Write-Host "REPUBLISH: $trybOpis. Bez publikacji calej strony, kontroli odkrywania i zgloszenia GSC." -ForegroundColor Cyan
    Initialize-Env
    $log = Load-Log
    $logRef = [ref]$log
    if ($Plik) { $files = @(Get-Item (Join-Path $queueDir $Plik)) }
    else { $files = @(Get-ChildItem $queueDir -Filter '*.json' | Where-Object { $_.Name -notlike '_*' } | Sort-Object Name) }
    $stats = @{
        wpisy = 0; innyStatus = 0
        ok = @(); pominiete = @(); bledy = @()
        zInlineImg = @(); zKartami = @(); zObrazkami = @()
        zmianaObrazkow = @(); linkLater = @(); pozaObrazkami = @(); staged = @()
    }
    $rcAll = 0
    $pierwszy = $true
    foreach ($f in $files) {
        $obj = $null
        try { $obj = (Read-TextWithRetry -Path $f.FullName -Etykieta "queue/$($f.Name)") | ConvertFrom-Json } catch {
            Write-Host "  UWAGA: nie moge sparsowac $($f.Name) -> pomijam." -ForegroundColor Yellow
            continue
        }
        if (-not $Plik -and "$($obj.status)" -ne 'opublikowany') { $stats.innyStatus = $stats.innyStatus + 1; continue }
        if (-not $pierwszy -and $ItemPauseSec -gt 0) { Start-Sleep -Seconds $ItemPauseSec }
        $pierwszy = $false
        $script:currentDripFile = $f.Name
        $rc = 1
        try { $rc = Republish-QueueItem -file $f -item $obj -log $logRef -stats $stats }
        catch {
            $msg = "$($_.Exception.Message)" -replace '\s+', ' '
            if ($msg.Length -gt 300) { $msg = $msg.Substring(0, 300) }
            Write-Host "  BLAD (plik=$($f.Name)): $msg" -ForegroundColor Red
            Write-DripLog -Plik $f.Name -ItemId '-' -Wynik "REPUBLISH BLAD: $msg"
            Write-DripError -ErrRecord $_ -Plik $f.Name
            $stats.bledy += $f.Name
            $rc = 1
        }
        if ($rc -is [array]) { $rc = $rc[-1] }
        if ($rc -eq 1) {
            $rcAll = 1
            if (-not $DryRun) {
                Write-Host '  STOP: blad przy zapisie na zywo, przerywam serie, zeby nie powtarzac go na kolejnych wpisach.' -ForegroundColor Red
                break
            }
        }
    }

    $etykieta = 'LIVE'
    if ($DryRun) { $etykieta = 'DRY-RUN' }
    $lista = { param($a) if (@($a).Count -eq 0) { '' } else { ': ' + (@($a) -join ', ') } }
    Write-Host "`nPODSUMOWANIE REPUBLISH ($trybTag, $etykieta)" -ForegroundColor Cyan
    Write-Host "  wpisy rozpatrzone                             : $($stats.wpisy) (inne statusy pominiete bez rozpatrywania: $($stats.innyStatus))"
    Write-Host "  z inline <img> w tresc_html                   : $(@($stats.zInlineImg).Count)$(& $lista $stats.zInlineImg)"
    Write-Host "  z kartami [FEATURE(S):]                       : $(@($stats.zKartami).Count)"
    Write-Host "  z obrazkami w post-body po renderze           : $(@($stats.zObrazkami).Count)"
    Write-Host "  obrazki inne niz na zywo                      : $(@($stats.zmianaObrazkow).Count)$(& $lista $stats.zmianaObrazkow)"
    Write-Host "  linki LINK-LATER do odrobienia (oczekiwane)   : $(@($stats.linkLater).Count)$(& $lista $stats.linkLater)"
    $kolB = 'Gray'; if (@($stats.pozaObrazkami).Count -gt 0) { $kolB = 'Yellow' }
    Write-Host "  ROZNICA POZA OBRAZKAMI (PATCH nadpisze tresc) : $(@($stats.pozaObrazkami).Count)$(& $lista $stats.pozaObrazkami)" -ForegroundColor $kolB
    Write-Host "  niepublikowane zmiany w CMS (staged)          : $(@($stats.staged).Count)$(& $lista $stats.staged)"
    $okTxt = 'odswiezone'
    if ($DryRun) { $okTxt = 'gotowe do odswiezenia' }
    Write-Host "  $($okTxt.PadRight(46)): $(@($stats.ok).Count)"
    Write-Host "  pominiete                                     : $(@($stats.pominiete).Count)$(& $lista $stats.pominiete)"
    $kolE = 'Gray'; if (@($stats.bledy).Count -gt 0) { $kolE = 'Red' }
    Write-Host "  bledy                                         : $(@($stats.bledy).Count)$(& $lista $stats.bledy)" -ForegroundColor $kolE
    $podsum = "REPUBLISH $trybTag $($etykieta): wpisy=$($stats.wpisy), ok=$(@($stats.ok).Count), pominiete=$(@($stats.pominiete).Count), bledy=$(@($stats.bledy).Count), obrazki_zmienione=$(@($stats.zmianaObrazkow).Count), poza_obrazkami=$(@($stats.pozaObrazkami).Count)"
    Write-DripLog -Plik $(if ($Plik) { $Plik } else { '-' }) -ItemId '-' -Wynik $podsum
    if ($DryRun) { Write-Host 'To byl DRY-RUN: nic nie wyslano (tylko odczyty GET). LIVE: ten sam przebieg z -DryRun:$false w otwartej sesji PS.' -ForegroundColor Magenta }
    return $rcAll
}

# =====================================================================================
#  UPLOAD ASSETOW Z KATALOGU: -UploadAssets <katalog>  (dodane 2026-10-21)
# -------------------------------------------------------------------------------------
#  Wgrywa wszystkie *.webp z katalogu przez Publish-WfAsset (ta sama sciezka co hero)
#  i zapisuje mape nazwa pliku -> URL CDN w <katalog>\_webflow-urls.json (po kazdym pliku,
#  wiec przerwany przebieg nie gubi URL-i juz wgranych). Idempotencja po MD5: plik o tym
#  samym MD5 co w mapie nie jest wgrywany drugi raz. DryRun: tylko lista plikow i MD5,
#  zero wywolan API, mapa nie jest zapisywana. Niczego nie usuwa z Webflow.
# =====================================================================================
function Save-AssetMap {
    param([string]$Path, [string]$Dir, $Wyniki)
    $map = [ordered]@{}
    $pliki = @()
    foreach ($k in @($Wyniki.Keys | Sort-Object)) { $map[$k] = "$($Wyniki[$k].url)"; $pliki += $Wyniki[$k] }
    $obj = [ordered]@{
        _opis          = 'Mapa plik -> URL CDN Webflow (Assets API), generowana przez scripts/webflow/blog-publish.ps1 -UploadAssets. Klucz idempotencji: md5.'
        katalog        = $Dir
        site           = $script:siteId
        zaktualizowano = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
        map            = $map
        pliki          = $pliki
    }
    ConvertTo-Json -InputObject $obj -Depth 6 | Set-Content -LiteralPath $Path -Encoding utf8
}

function Invoke-UploadAssetsRun {
    param([string]$Dir)
    $kat = $Dir
    if (-not (Test-Path -LiteralPath $kat -PathType Container)) {
        $wzgl = Join-Path $repoRoot $Dir
        if (Test-Path -LiteralPath $wzgl -PathType Container) { $kat = $wzgl }
    }
    if (-not (Test-Path -LiteralPath $kat -PathType Container)) {
        Write-Host "BLAD: nie ma katalogu '$Dir' (sprawdzilem tez wzgledem $repoRoot)." -ForegroundColor Red
        return 2
    }
    $kat = (Resolve-Path -LiteralPath $kat).Path
    $pliki = @(Get-ChildItem -LiteralPath $kat -Filter '*.webp' -File | Sort-Object Name)
    $mapPath = Join-Path $kat '_webflow-urls.json'
    Write-Host "UPLOAD ASSETS: katalog $kat, plikow *.webp: $($pliki.Count)" -ForegroundColor Cyan
    if ($pliki.Count -eq 0) { Write-Host '  Brak plikow *.webp, nic do zrobienia.' -ForegroundColor Yellow; return 0 }

    $wyniki = [ordered]@{}
    if (Test-Path -LiteralPath $mapPath) {
        try {
            $j = (Read-TextWithRetry -Path $mapPath -Etykieta '_webflow-urls.json') | ConvertFrom-Json
            foreach ($p in @($j.pliki)) { if ($p -and $p.plik) { $wyniki["$($p.plik)"] = $p } }
            Write-Host "  mapa z poprzednich uploadow: $mapPath ($($wyniki.Count) plikow)" -ForegroundColor Gray
        } catch {
            Write-Host "  UWAGA: nie odczytalem $mapPath ($($_.Exception.Message)); wszystkie pliki traktuje jako nowe." -ForegroundColor Yellow
        }
    }
    if (-not $DryRun) { Initialize-Env }

    $nowe = 0; $juz = 0
    foreach ($f in $pliki) {
        $md5 = Get-FileMd5Hex -Bytes (Read-FileBytesWithRetry -Path $f.FullName -Etykieta $f.Name)
        $stary = $null
        if ($wyniki.Contains($f.Name)) { $stary = $wyniki[$f.Name] }
        if ($stary -and "$($stary.md5)" -eq $md5 -and "$($stary.url)") {
            Write-Host ("  =     {0,-36} {1,8} B  md5={2}  juz wgrany: {3}" -f $f.Name, $f.Length, $md5, $stary.url) -ForegroundColor DarkGray
            $juz++
            continue
        }
        if ($DryRun) {
            Write-Host ("  [DRY] {0,-36} {1,8} B  md5={2}  -> do wgrania" -f $f.Name, $f.Length, $md5) -ForegroundColor Magenta
            continue
        }
        $url = Publish-WfAsset -FilePath $f.FullName -Etykieta $f.Name
        $wyniki[$f.Name] = [pscustomobject]@{ plik = $f.Name; md5 = $md5; url = $url; bajty = $f.Length; wgrano = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') }
        $nowe++
        Save-AssetMap -Path $mapPath -Dir $kat -Wyniki $wyniki
    }

    if ($DryRun) {
        Write-Host "`nPODSUMOWANIE UPLOAD (DRY-RUN): do wgrania $($pliki.Count - $juz), juz wgranych (ten sam MD5 w mapie): $juz. Nic nie wyslano, mapa nie zapisana." -ForegroundColor Cyan
        Write-Host "  LIVE: & '$PSCommandPath' -UploadAssets '$kat' -DryRun:`$false   (w otwartej sesji PS)" -ForegroundColor Magenta
        return 0
    }
    if ($nowe -eq 0 -and $wyniki.Count -gt 0) { Save-AssetMap -Path $mapPath -Dir $kat -Wyniki $wyniki }
    Write-Host "`nPODSUMOWANIE UPLOAD (LIVE): wgrano $nowe, pominieto (ten sam MD5): $juz. Mapa: $mapPath" -ForegroundColor Green
    foreach ($f in $pliki) { if ($wyniki.Contains($f.Name)) { Write-Host "  $($f.Name) -> $($wyniki[$f.Name].url)" } }
    Write-DripLog -Plik '-' -ItemId '-' -Wynik "UPLOAD-ASSETS OK: katalog=$kat, wgrano=$nowe, pominieto=$juz"
    return 0
}

# =====================================================================================
#  MAIN
# =====================================================================================
$trybTxt = if ($DryRun) { 'DRY-RUN (podglad, ZERO zapisu)' } else { 'LIVE (zapis na zywa strone mindsync.app!)' }
$trybKol = if ($DryRun) { 'Cyan' } else { 'Red' }
Write-Host ("webflow/blog-publish.ps1 - tryb: " + $trybTxt) -ForegroundColor $trybKol

# --- tryby dodane 2026-10-21: walidacja kombinacji i wyjscie PRZED dripem/trybem interaktywnym.
#     Bez -Republish/-BodyOnly/-KeepHero/-UploadAssets nic tu sie nie dzieje (stare tryby bez zmian).
$bledyParam = @()
if ($BodyOnly -and -not $Republish) { $bledyParam += '-BodyOnly dziala tylko razem z -Republish.' }
if ($KeepHero -and -not $Republish) { $bledyParam += '-KeepHero dziala tylko razem z -Republish.' }
if ($Republish -and $DripOne)       { $bledyParam += '-Republish nie laczy sie z -DripOne (drip publikuje wylacznie nowe wpisy).' }
if ($Republish -and -not $Plik -and -not $All) { $bledyParam += '-Republish wymaga -Plik <plik> albo -All.' }
if ($Republish -and $Plik -and $All) { $bledyParam += '-Republish: podaj -Plik ALBO -All, nie oba naraz.' }
if ($UploadAssets -and ($Republish -or $DripOne -or $Plik -or $All)) { $bledyParam += '-UploadAssets dziala samodzielnie (bez -Republish, -DripOne, -Plik, -All).' }
if ($bledyParam.Count -gt 0) {
    foreach ($bp in $bledyParam) { Write-Host "BLAD PARAMETROW: $bp" -ForegroundColor Red }
    exit 2
}
if ($UploadAssets) {
    $rcU = Invoke-UploadAssetsRun -Dir $UploadAssets
    if ($rcU -is [array]) { $rcU = $rcU[-1] }
    exit $rcU
}
if ($Republish) {
    $rcR = 1
    try { $rcR = Invoke-RepublishRun } catch {
        Write-Host "REPUBLISH BLAD KRYTYCZNY: $($_.Exception.Message)" -ForegroundColor Red
        Write-DripLog -Plik $(if ($Plik) { $Plik } else { '-' }) -ItemId '-' -Wynik "REPUBLISH BLAD KRYTYCZNY: $($_.Exception.Message)"
        Write-DripError -ErrRecord $_ -Plik $(if ($Plik) { $Plik } else { '-' })
        exit 1
    }
    if ($rcR -is [array]) { $rcR = $rcR[-1] }
    exit $rcR
}

$script:currentDripFile = '?'
if ($DripOne) {
    try {
        Initialize-Env
        $queue = @(Select-NextGotowy)
        if ($queue.Count -eq 0) {
            Write-Host '  BRAK wpisow gotowych z data <= dzis.' -ForegroundColor Yellow
            Write-DripLog -Plik '-' -ItemId '-' -Wynik 'BRAK wpisow gotowych'
            Invoke-WfDiscoveryRefresh -Plik '-'
            Invoke-WfSitePublish -Plik '-'     # nic nie poszlo na zywo -> tylko komunikat o pominieciu
            Invoke-GscSitemapSubmit -Plik '-'
            exit 0
        }
        Write-Host ("  kandydaci: " + (($queue | ForEach-Object { "$($_.name)[$($_.obj.planowana_data)]" }) -join ', ')) -ForegroundColor DarkCyan
        $log = Load-Log
        $logRef = [ref]$log
        foreach ($cand in $queue) {
            $script:currentDripFile = $cand.file.Name
            $rc = Publish-QueueItem -file $cand.file -item $cand.obj -log $logRef
            if ($rc -eq 0) {
                Invoke-WfDiscoveryRefresh -Plik $script:currentDripFile
                Invoke-WfSitePublish -Plik $script:currentDripFile
                Invoke-GscSitemapSubmit -Plik $script:currentDripFile   # PO publikacji strony (nowa sitemap.xml)
                Write-Host "`nDRIP zakonczony (exit=0)." -ForegroundColor Green
                exit 0
            }
            if ($rc -eq 1) { exit 1 }
            # rc=2 -> pominieto, probuj nastepnego kandydata
        }
        Write-Host "`n  Wszystkie 'gotowe' pominieto (bramki/idempotencja) - to nie blad." -ForegroundColor Yellow
        Write-DripLog -Plik '-' -ItemId '-' -Wynik 'BRAK publikowalnych (wszystkie pominieto)'
        Invoke-WfDiscoveryRefresh -Plik '-'
        Invoke-WfSitePublish -Plik '-'         # nic nie poszlo na zywo -> tylko komunikat o pominieciu
        Invoke-GscSitemapSubmit -Plik '-'
        exit 0
    } catch {
        $msg = $_.Exception.Message
        Write-Host "DRIP BLAD KRYTYCZNY (plik=$($script:currentDripFile)): $msg" -ForegroundColor Red
        Write-DripLog -Plik $script:currentDripFile -ItemId '-' -Wynik "BLAD: $msg"
        Write-DripError -ErrRecord $_ -Plik $script:currentDripFile
        exit 1
    }
}

# tryb interaktywny
Initialize-Env
$log = Load-Log
$files = if ($Plik) { @(Get-Item (Join-Path $queueDir $Plik)) }
         else { Get-ChildItem $queueDir -Filter '*.json' | Where-Object { $_.Name -notlike '_*' } | Sort-Object Name }
if (-not $files -or $files.Count -eq 0) { Write-Host 'Kolejka pusta (blog/queue/*.json).' -ForegroundColor Yellow; return }

$logRef = [ref]$log
$published = 0
foreach ($f in $files) {
    $obj = $null
    try { $obj = (Read-TextWithRetry -Path $f.FullName -Etykieta "queue/$($f.Name)") | ConvertFrom-Json } catch {
        Write-Host "  UWAGA: nie moge sparsowac $($f.Name) -> pomijam." -ForegroundColor Yellow; continue
    }
    if ($obj.status -ne 'gotowy' -and -not $Plik) { continue }
    $pd = $null
    if ($obj.planowana_data) { try { $pd = [datetime]::Parse($obj.planowana_data) } catch {} }
    if ($pd -and $pd.Date -gt (Get-Date).Date -and -not $Plik) { continue }
    $rc = Publish-QueueItem -file $f -item $obj -log $logRef
    if ($rc -eq 0 -and -not $DryRun) {
        $published++
        if (-not $All) { break }
    }
    if ($rc -eq 0 -and $DryRun -and -not $All) { break }
}

# kontrola kanalow odkrywania (+ odswiezenie lastmod /blog) ZAWSZE przed publikacja calej strony
Invoke-WfDiscoveryRefresh -Plik $(if ($Plik) { $Plik } else { '-' })

# publikacja calej strony RAZ na przebieg (nie po kazdym wpisie) - odswieza sitemap.xml
Invoke-WfSitePublish -Plik $(if ($Plik) { $Plik } else { '-' })

# zgloszenie sitemapy w GSC PO publikacji strony (tylko gdy ta sie udala)
Invoke-GscSitemapSubmit -Plik $(if ($Plik) { $Plik } else { '-' })

$podsKol = if ($DryRun) { 'Cyan' } else { 'Green' }
Write-Host "`nPODSUMOWANIE: opublikowano $published wpisow. Log: $logPath" -ForegroundColor $podsKol
if ($DryRun) { Write-Host 'To byl DRY-RUN - nic nie wyslano. Realna publikacja: -DryRun:$false' -ForegroundColor Magenta }
