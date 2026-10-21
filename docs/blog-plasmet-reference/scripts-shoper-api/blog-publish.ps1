# =====================================================================================
#  blog-publish.ps1 — DRIP-PUBLISH wpisow bloga na Shoper (zasob `news`) przez webapi
# -------------------------------------------------------------------------------------
#  Bierze NAJSTARSZY wpis o statusie `gotowy` z blog/queue/*.json, ktorego planowana_data <= dzis,
#  i publikuje go: (find-or-create tagi) -> POST /news -> (przypiecie kategorii) -> log permalinku
#  -> przestawienie statusu na `opublikowany`. Throttling + retry/backoff (429/5xx) + idempotencja
#  (nie publikuje wpisu juz obecnego w blog/published-log.json) + odswiezanie tokenu.
#
#  ⚠️ DOMYSLNIE -DryRun = TRUE: buduje payload i pokazuje co BY zrobil, ale NIE wysyla zadnego POST/PUT.
#     Realna publikacja: jawnie  -DryRun:$false  (zmienia ZYWY sklep — wymaga swiadomej decyzji).
#
#  Uruchom (podglad):  powershell -ExecutionPolicy Bypass -File .\blog-publish.ps1
#  Uruchom (LIVE):     powershell -ExecutionPolicy Bypass -File .\blog-publish.ps1 -DryRun:$false
#  Jeden konkretny:    ...\blog-publish.ps1 -Plik 2026-06-12_milwaukee.json -DryRun:$false
#  Cala kolejka naraz: ...\blog-publish.ps1 -All -DryRun:$false   (drip: zwykle BEZ -All, 1 wpis/przebieg)
#
#  -------------------------------------------------------------------------------------
#  TRYB DRIP (Windows Task Scheduler, codziennie 07:00) — JEDEN wpis dziennie, nienadzorowany:
#    Podglad:  powershell -NonInteractive -ExecutionPolicy Bypass -File .\blog-publish.ps1 -DripOne
#    LIVE:     powershell -NonInteractive -ExecutionPolicy Bypass -File .\blog-publish.ps1 -DripOne -DryRun:$false
#  -DripOne: bierze NASTEPNY wpis 'gotowy' wg planowana_data ASC (przy rownych: nazwa pliku ASC),
#    publikuje go w pelni (hero image base64 + image_name, categories:[5], tagi find-or-create,
#    active=1, start_page, seo_*; wzorzec anty-'wiszacy zapis'; idempotencja po name), oznacza
#    'opublikowany', dopisuje news_id+permalink, published-log.json oraz _drip-log.txt.
#    BRAK 'gotowy' -> log "BRAK wpisow gotowych" i exit 0 (nie blad). Surowe [LINK:...] albo brak
#    pliku hero -> ostrzezenie + pomin (nastepny gotowy lub koniec). NIE generuje grafik (bez
#    Gemini/ImageMagick) — publikuje tylko gotowe hero z dysku. Exit: 0 OK / pominieto, 1 blad.
# =====================================================================================

[CmdletBinding()]
param(
    [bool]   $DryRun = $true,                 # DOMYSLNIE bezpiecznie: tylko podglad payloadu
    [string] $Plik   = $null,                 # opcjonalnie: opublikuj konkretny plik z kolejki
    [switch] $All,                            # opublikuj wszystkie kwalifikujace sie (nie tylko 1)
    [switch] $DripOne,                        # TRYB DRIP (Task Scheduler): 1 NASTEPNY 'gotowy', nienadzorowany
    [int]    $ThrottleMs = 400,               # opoznienie miedzy zadaniami (throttling webapi)
    [int]    $MaxRetry   = 5,                 # liczba prob przy 429/5xx (backoff wykladniczy)
    [int]    $WriteDeadlineSec = 45           # twardy deadline zapisu (anty-'wiszacy zapis'; hero base64 = wieksze)
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# =====================================================================================
#  SCIEZKI LOGOW — liczone od $PSScriptRoot OD RAZU (nie z cwd, nie z reszty inicjalizacji).
#  KLUCZOWE dla odpornosci: musza byc znane ZANIM cokolwiek innego (.env/queue/auth) moze rzucic,
#  zeby try/catch trybu -DripOne ZAWSZE zdazyl zapisac log o cichej awarii (np. plik OneDrive offline).
# =====================================================================================
$script:dripLogPath   = Join-Path $PSScriptRoot '_drip-log.txt'    # 1 wiersz/przebieg (jak dotad)
$script:dripErrorPath = Join-Path $PSScriptRoot '_drip-error.txt'  # pelny zrzut wyjatku (stack/pozycja)

# --- sciezki repo (samo liczenie sciezek NIE rzuca; istnienie katalogu sprawdzamy pozniej w retry) ---
$repoRoot  = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent   # ...\shopper-sklep
$queueDir  = Join-Path $repoRoot 'blog\queue'
$logPath   = Join-Path $repoRoot 'blog\published-log.json'

# =====================================================================================
#  AUTH — token permanentny z .env (SHOPER_TOKEN) LUB login+haslo (POST /auth). Sekrety: tylko .env.
#  UWAGA: odczyt .env NIE jest juz robiony na top-level (mogl rzucic WCZESNIE, przed logiem przy
#  pliku 'tylko w chmurze' OneDrive). Robi go Initialize-Env z retry+hydratacja, wolane w try/catch.
# =====================================================================================
$script:envCfg      = @{}
$script:baseUrl     = $null
$script:token       = $null
$script:tokenExpiry = [datetime]::MinValue

# =====================================================================================
#  RETRY ODCZYTU PLIKU + HYDRATACJA OneDrive (Files On-Demand)
#  Pliki repo bywaja "tylko w chmurze" o 07:00 (scheduler) -> chwilowo niedostepne / Get-Content rzuca.
#  Wzorzec: 3 proby z backoff 2/5/10 s; przy KAZDEJ probie WYMUS hydratacje realnym odczytem bajtow
#  ([IO.File]::ReadAllBytes) -> to "sciaga" plik z chmury. Zwraca bajty (do hero) lub rzuca po wyczerpaniu.
# =====================================================================================
$script:FileRetryBackoff = @(2, 5, 10)   # sekundy miedzy probami (po 1.,2. probie)
function Read-FileBytesWithRetry {
    param([string]$Path, [string]$Etykieta = 'plik')
    $last = $null
    for ($i = 0; $i -lt $script:FileRetryBackoff.Count; $i++) {
        try {
            if (-not [IO.File]::Exists($Path)) { throw "nie istnieje: $Path" }
            # realny odczyt bajtow = wymuszenie hydratacji OneDrive (Files On-Demand)
            $bytes = [IO.File]::ReadAllBytes($Path)
            if ($null -eq $bytes) { throw "odczyt zwrocil null: $Path" }
            return $bytes
        } catch {
            $last = $_
            $wait = $script:FileRetryBackoff[$i]
            Write-Host "  RETRY-FILE ($Etykieta) proba $($i+1)/$($script:FileRetryBackoff.Count) nieudana: $($_.Exception.Message) -> backoff ${wait}s" -ForegroundColor Yellow
            Start-Sleep -Seconds $wait
        }
    }
    # ostatnia (4.) proba bez czekania
    if (-not [IO.File]::Exists($Path)) { throw "Plik niedostepny po retry ($Etykieta): $Path :: $($last.Exception.Message)" }
    return [IO.File]::ReadAllBytes($Path)
}
function Read-TextWithRetry {
    param([string]$Path, [string]$Etykieta = 'plik')
    $bytes = Read-FileBytesWithRetry -Path $Path -Etykieta $Etykieta
    # UTF-8. UWAGA: [Text.Encoding]::UTF8.GetString NIE usuwa BOM (inaczej niz Get-Content/StreamReader)
    # -> przy pliku UTF-8 z BOM zostaje wiodacy U+FEFF i ConvertFrom-Json rzuca "Nieprawidlowy element
    # pierwotny JSON: .". Wycinamy BOM (EF BB BF) jawnie przed dekodowaniem.
    if ($bytes.Length -ge 3 -and $bytes[0] -eq 0xEF -and $bytes[1] -eq 0xBB -and $bytes[2] -eq 0xBF) {
        return [Text.Encoding]::UTF8.GetString($bytes, 3, $bytes.Length - 3)
    }
    return [Text.Encoding]::UTF8.GetString($bytes)
}

# =====================================================================================
#  Initialize-Env: odczyt .env z retry+hydratacja, ustawia $script:envCfg/$script:baseUrl.
#  Wolane W TRY/CATCH (tryb -DripOne) -> ewentualny blad jest LOGOWANY, nie cichy.
# =====================================================================================
function Initialize-Env {
    $envPath = Join-Path $PSScriptRoot '.env'
    $raw = Read-TextWithRetry -Path $envPath -Etykieta '.env'   # rzuci z jasnym komunikatem jesli brak/offline
    $script:envCfg = @{}
    $raw -split "`r?`n" | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
        $parts = $_ -split '=', 2
        $script:envCfg[$parts[0].Trim()] = $parts[1].Trim().Trim('"')
    }
    $script:baseUrl = ($script:envCfg['SHOPER_URL']).TrimEnd('/')
    if (-not $script:baseUrl) { throw "Brak SHOPER_URL w .env (plik odczytany, ale klucz pusty/brak)" }
}

function Get-Token {
    # Wymaga wczesniejszego Initialize-Env (ustawia $script:envCfg/$script:baseUrl).
    if (-not $script:baseUrl) { Initialize-Env }
    # Token permanentny ma pierwszenstwo. Inaczej login+haslo -> bearer ~30 dni.
    if ($script:envCfg['SHOPER_TOKEN']) {
        $script:token = $script:envCfg['SHOPER_TOKEN']
        $script:tokenExpiry = [datetime]::MaxValue
        Write-Host "AUTH: token permanentny z .env (zredagowany)" -ForegroundColor Green
        return
    }
    $login = $script:envCfg['SHOPER_LOGIN']; $pass = $script:envCfg['SHOPER_PASSWORD']
    if (-not $login -or -not $pass) { throw "Brak SHOPER_LOGIN/SHOPER_PASSWORD i SHOPER_TOKEN w .env" }
    $basic = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($login):$($pass)"))
    # RETRY autoryzacji: 3 proby z backoff na blad sieci / 5xx / timeout (transient o 07:00).
    # 401/403/inne kody klienta = blad konfiguracji, NIE ponawiamy (od razu rzucamy).
    $maxAuth = 3; $backoff = @(2, 5, 10)
    for ($a = 1; $a -le $maxAuth; $a++) {
        try {
            $auth = Invoke-RestMethod -Method Post -Uri "$($script:baseUrl)/webapi/rest/auth" `
                        -Headers @{ Authorization = "Basic $basic" } -TimeoutSec 30
            if (-not $auth.access_token) { throw "Nie otrzymano access_token" }
            $script:token = $auth.access_token
            $script:tokenExpiry = (Get-Date).AddSeconds([int]$auth.expires_in - 300)   # 5-min zapas
            Write-Host "AUTH OK (token zredagowany, wazny $($auth.expires_in)s)" -ForegroundColor Green
            return
        } catch {
            $code = $null
            try { $code = [int]$_.Exception.Response.StatusCode } catch {}
            $transient = ($null -eq $code) -or ($code -eq 429) -or ($code -ge 500 -and $code -lt 600)
            if ($transient -and $a -lt $maxAuth) {
                $w = $backoff[$a - 1]
                Write-Host "  AUTH transient (kod=$code) -> backoff ${w}s (proba $a/$maxAuth)" -ForegroundColor Yellow
                Start-Sleep -Seconds $w
                continue
            }
            throw "AUTH nieudany (kod=$code): $($_.Exception.Message)"
        }
    }
}

function Ensure-Token {
    if (-not $script:token -or (Get-Date) -ge $script:tokenExpiry) { Get-Token }
}

# =====================================================================================
#  Uniwersalny wrapper webapi: throttling + retry/backoff (429/5xx) + odswiezanie tokenu (401)
# =====================================================================================
function Invoke-Api {
    param([string]$Method, [string]$Path, $Body = $null)
    Ensure-Token
    $uri = "$($script:baseUrl)/webapi/rest/$Path"
    $attempt = 0
    while ($true) {
        $attempt++
        try {
            $hdr = @{ Authorization = "Bearer $($script:token)" }
            $params = @{ Method = $Method; Uri = $uri; Headers = $hdr }
            if ($null -ne $Body) {
                $params.ContentType = 'application/json'
                $params.Body = ($Body | ConvertTo-Json -Depth 12 -Compress)
            }
            $r = Invoke-RestMethod @params
            Start-Sleep -Milliseconds $ThrottleMs
            return $r
        } catch {
            $code = $null
            try { $code = [int]$_.Exception.Response.StatusCode } catch {}
            if ($code -eq 401 -and $attempt -le 2) {
                Write-Host "  HTTP 401 -> odswiezam token i ponawiam" -ForegroundColor Yellow
                $script:token = $null; Ensure-Token; continue
            }
            if (($code -eq 429 -or ($code -ge 500 -and $code -lt 600)) -and $attempt -lt $MaxRetry) {
                $wait = [math]::Pow(2, $attempt)
                Write-Host "  HTTP $code -> backoff ${wait}s (proba $attempt/$MaxRetry)" -ForegroundColor Yellow
                Start-Sleep -Seconds $wait
                continue
            }
            # wyciagnij tresc bledu (do diagnozy walidacji / Missing MODULE)
            $errBody = $null
            try { $s=$_.Exception.Response.GetResponseStream(); $errBody=(New-Object IO.StreamReader($s)).ReadToEnd() } catch {}
            throw "API $Method $Path -> HTTP $code $($_.Exception.Message) :: $errBody"
        }
    }
}

# =====================================================================================
#  ZAPIS ODPORNY NA "WISZACY ZAPIS" (host PLASMET) — zweryfikowany na zywo 2026-06-10
#  (news_id 8/9/10/11). POST/PUT przez Invoke-RestMethod WISI na tym hoscie; wzorzec pewny:
#  System.Net.HttpWebRequest + .Timeout + .ReadWriteTimeout + .KeepAlive=$false (twardy deadline).
#  Po HANG/TIMEOUT operacja po stronie serwera i tak sie wykonuje -> efekt weryfikujemy GET-em.
#  Uzywany TYLKO w trybie -DripOne (nienadzorowany). Tryb interaktywny zostaje na Invoke-Api.
# =====================================================================================
function Invoke-WriteWithDeadline {
    param([string]$Method, [string]$Path, $Obj)
    Ensure-Token
    $json  = $Obj | ConvertTo-Json -Depth 12 -Compress
    $bytes = [Text.Encoding]::UTF8.GetBytes($json)
    $ms    = $WriteDeadlineSec * 1000
    $req = [System.Net.HttpWebRequest]::Create("$($script:baseUrl)/webapi/rest/$Path")
    $req.Method = $Method.ToUpper()
    $req.ContentType = 'application/json; charset=utf-8'
    $req.Accept = 'application/json'
    $req.Headers['Authorization'] = "Bearer $($script:token)"
    $req.Timeout = $ms; $req.ReadWriteTimeout = $ms; $req.KeepAlive = $false
    try {
        $rs = $req.GetRequestStream(); $rs.Write($bytes,0,$bytes.Length); $rs.Close()
        $resp = $req.GetResponse()
        $sr = New-Object IO.StreamReader($resp.GetResponseStream())
        $body = $sr.ReadToEnd(); $sr.Close(); $code = [int]$resp.StatusCode; $resp.Close()
        return [pscustomobject]@{ returned=$true; code=$code; raw=$body.Trim() }
    } catch [System.Net.WebException] {
        if ($_.Exception.Status -eq [System.Net.WebExceptionStatus]::Timeout) {
            try { $req.Abort() } catch {}
            return [pscustomobject]@{ returned=$false; code=$null; raw='HANG/TIMEOUT' }
        }
        $code=$null; $eb=$null
        try { $code=[int]$_.Exception.Response.StatusCode } catch {}
        try { $s=$_.Exception.Response.GetResponseStream(); $eb=(New-Object IO.StreamReader($s)).ReadToEnd() } catch {}
        return [pscustomobject]@{ returned=$true; code=$code; raw=$eb }
    } catch {
        return [pscustomobject]@{ returned=$false; code=$null; raw="EXC:$($_.Exception.Message)" }
    }
}

# Pobranie pelnej kolekcji z paginacja (limit=50, iteruj po pages) — uzywany przez drip do
# find-or-create tagow i idempotencji po `name`.
function Get-AllPaged {
    param([string]$Resource)
    $all=@(); $page=1; $pages=1
    do {
        $sep = if ($Resource -match '\?') { '&' } else { '?' }
        $r = Invoke-Api -Method Get -Path ("$Resource$sep" + "limit=50&page=$page")
        if ($r.list) { $all += $r.list }
        $pages = if ($r.pages) { [int]$r.pages } else { 1 }
        $page++
    } while ($page -le $pages)
    return $all
}

# =====================================================================================
#  LOG RUNOW DRIP — scripts/shoper-api/_drip-log.txt (data-godzina | tryb | plik | news_id | wynik)
#  Dopisuje 1 wiersz na przebieg. NIE zawiera sekretow. Sciezka liczona z $PSScriptRoot (gora pliku).
#  ODPORNY: nigdy nie rzuca (logowanie bledu nie moze samo wywrocic skryptu). $DryRun moze byc
#  jeszcze nieustawione przy bardzo wczesnym bledzie -> bezpieczny fallback na 'LIVE'.
# =====================================================================================
function Write-DripLog {
    param([string]$Plik, [string]$NewsId, [string]$Wynik)
    try {
        $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        $tryb  = 'LIVE'
        try { if ($DryRun) { $tryb = 'DRY' } } catch {}
        if (-not $Plik)   { $Plik = '?' }
        if (-not $NewsId) { $NewsId = '-' }
        $line  = "$stamp | $tryb | plik=$Plik | news_id=$NewsId | $Wynik"
        Add-Content -Path $script:dripLogPath -Value $line -Encoding utf8
        Write-Host "  DRIP-LOG: $line" -ForegroundColor DarkGray
    } catch {
        # ostatnia deska: nie wywracaj skryptu z powodu samego logowania
        Write-Host "  (Write-DripLog nie zdolal zapisac: $($_.Exception.Message))" -ForegroundColor DarkYellow
    }
}

# =====================================================================================
#  PELNY ZRZUT BLEDU — scripts/shoper-api/_drip-error.txt (diagnostyka cichych awarii 07:00).
#  Zapisuje: data-godzina, tryb, plik, Exception.Message, ScriptStackTrace, PositionMessage.
#  Wolany z catch trybu -DripOne dla KAZDEGO bledu (tez wczesnego: .env/hero/auth/wyjatek).
#  NIE zawiera sekretow (komunikaty webapi nie odbijaja loginu/hasla; token nie jest logowany).
#  Nigdy nie rzuca.
# =====================================================================================
function Write-DripError {
    param($ErrRecord, [string]$Plik = '?')
    try {
        $stamp = Get-Date -Format 'yyyy-MM-dd HH:mm:ss'
        $tryb  = 'LIVE'
        try { if ($DryRun) { $tryb = 'DRY' } } catch {}
        $msg = ''; $stack = ''; $pos = ''
        try { $msg   = "$($ErrRecord.Exception.Message)" } catch {}
        try { $stack = "$($ErrRecord.ScriptStackTrace)" } catch {}
        try { $pos   = "$($ErrRecord.InvocationInfo.PositionMessage)" } catch {}
        $block = @(
            '======================================================================'
            "[$stamp] tryb=$tryb plik=$Plik"
            "Exception.Message    : $msg"
            "ScriptStackTrace     :"
            $stack
            "InvocationInfo (pozycja):"
            $pos
            ''
        ) -join "`r`n"
        Add-Content -Path $script:dripErrorPath -Value $block -Encoding utf8
        Write-Host "  DRIP-ERROR zapisany -> $($script:dripErrorPath)" -ForegroundColor DarkYellow
    } catch {
        Write-Host "  (Write-DripError nie zdolal zapisac: $($_.Exception.Message))" -ForegroundColor DarkYellow
    }
}

# =====================================================================================
#  LOG publikacji (idempotencja) — published-log.json: [{ tytul, news_id, permalink, data, plik }]
# =====================================================================================
function Load-Log {
    if (Test-Path $logPath) {
        # odczyt z retry+hydratacja (published-log.json bywa "tylko w chmurze" o 07:00)
        $raw = Read-TextWithRetry -Path $logPath -Etykieta 'published-log.json'
        if ($raw.Trim()) { return @(($raw | ConvertFrom-Json)) }
    }
    return @()
}
function Save-Log($entries) {
    ,@($entries) | ConvertTo-Json -Depth 8 | Set-Content $logPath -Encoding utf8
}
function Already-Published($log, $tytul) {
    return [bool]($log | Where-Object { $_.tytul -eq $tytul })
}

# =====================================================================================
#  find-or-create: news-tags (po name) i news-categories (po name)
#  W DryRun: NIE tworzy, tylko raportuje "[DRY] utworzylbym".
# =====================================================================================
function Resolve-TagIds {
    param([string[]]$Names)
    if (-not $Names) { return @() }
    $existing = @{}
    $page = 1
    do {
        $resp = Invoke-Api -Method Get -Path "news-tags?limit=50&page=$page"
        foreach ($t in @($resp.list)) { $existing[$t.name] = [int]$t.tag_id }
        $pages = if ($resp.pages) { [int]$resp.pages } else { 1 }
        $page++
    } while ($page -le $pages)

    $ids = @()
    foreach ($n in $Names) {
        if ($existing.ContainsKey($n)) {
            $ids += $existing[$n]
        } else {
            if ($DryRun) {
                Write-Host "    [DRY] utworzylbym tag '$n' (POST news-tags)" -ForegroundColor DarkYellow
                $ids += "(nowy:$n)"
            } else {
                $new = Invoke-Api -Method Post -Path 'news-tags' -Body @{ name = $n; lang_id = 1 }
                $newId = if ($new.tag_id) { [int]$new.tag_id } elseif ($new -is [int] -or $new -match '^\d+$') { [int]$new } else { $null }
                Write-Host "    + utworzono tag '$n' -> tag_id=$newId" -ForegroundColor Green
                if ($newId) { $ids += $newId }
            }
        }
    }
    return $ids
}

function Resolve-CategoryId {
    param([string]$Name)
    if (-not $Name) { return $null }
    $page = 1
    do {
        $resp = Invoke-Api -Method Get -Path "news-categories?limit=50&page=$page"
        foreach ($c in @($resp.list)) { if ($c.name -eq $Name) { return [int]$c.category_id } }
        $pages = if ($resp.pages) { [int]$resp.pages } else { 1 }
        $page++
    } while ($page -le $pages)

    if ($DryRun) {
        Write-Host "    [DRY] utworzylbym kategorie '$Name' (POST news-categories)" -ForegroundColor DarkYellow
        return "(nowa:$Name)"
    }
    $new = Invoke-Api -Method Post -Path 'news-categories' -Body @{ name = $Name; lang_id = 1; active = 1 }
    $newId = if ($new.category_id) { [int]$new.category_id } else { $null }
    Write-Host "    + utworzono kategorie '$Name' -> category_id=$newId" -ForegroundColor Green
    return $newId
}

# =====================================================================================
#  SCHEMA JSON-LD per-post -> doklejana na KONIEC content (przezywa 1:1 w news.content, zweryf. 2026-06-11).
#  Zrodlo bloku (priorytet): blog/queue/<slug>.schema.html (gotowy <script ld+json>, usuwamy komentarz HTML)
#  -> fallback: pole schema_jsonld w pliku kolejki (goly JSON -> owijamy w <script ld+json>).
#  Slug = hero_slug -> seo_url -> z tytulu. Idempotencja: NIE dokleja, jesli content juz ma <script ld+json>.
#  Dzieki temu KAZDY wpis z dripu (POST /news) dostaje scheme automatycznie. Funkcja czysta (nie zapisuje).
# =====================================================================================
function Get-SchemaBlock {
    param($item)
    # slug zrodla schemy: ta sama logika co hero (hero_slug -> seo_url -> z tytulu)
    $slug = $null
    if ($item.PSObject.Properties.Name -contains 'hero_slug' -and $item.hero_slug) { $slug = "$($item.hero_slug)".Trim() }
    elseif ($item.seo_url) { $slug = "$($item.seo_url)".Trim() }
    else { $slug = ($item.tytul -replace '[^\p{L}\p{Nd}]+','-').Trim('-').ToLower() }

    $raw = $null
    $schemaHtml = Join-Path $queueDir "$slug.schema.html"
    if (Test-Path $schemaHtml) {
        try { $raw = Read-TextWithRetry -Path $schemaHtml -Etykieta "schema/$slug" } catch { $raw = $null }
    }
    if (-not $raw -and $item.schema_jsonld) { $raw = "$($item.schema_jsonld)" }
    if (-not $raw) { return $null }

    # gotowy <script ...>...</script> -> wytnij sam blok (bez komentarza HTML/otaczajacych bializnaki)
    $m = [regex]::Match($raw, '(?is)<script\b[^>]*type\s*=\s*["'']application/ld\+json["''][^>]*>.*?</script>')
    if ($m.Success) { return $m.Value.Trim() }
    # goly JSON -> owin w <script ld+json>
    return "<script type=`"application/ld+json`">`r`n$($raw.Trim())`r`n</script>"
}
# Dokleja blok schemy na koniec content, o ile pole niepuste i content jeszcze go nie ma (idempotencja).
function Add-SchemaToContent {
    param([string]$Content, $item)
    if ($Content -match '<script[^>]*type\s*=\s*["'']application/ld\+json["'']') {
        Write-Host "  SCHEMA: content juz ma <script ld+json> -> NIE dokleam (idempotencja)." -ForegroundColor DarkGray
        return $Content
    }
    $block = Get-SchemaBlock -item $item
    if (-not $block) {
        Write-Host "  SCHEMA: brak zrodla (.schema.html ani schema_jsonld) -> pomijam doklejenie." -ForegroundColor DarkGray
        return $Content
    }
    Write-Host "  SCHEMA: dokleam blok JSON-LD na koniec content (+$($block.Length) zn.)." -ForegroundColor DarkCyan
    return ($Content.TrimEnd() + "`r`n" + $block)
}

# =====================================================================================
#  Budowa payloadu `news` z pliku kolejki
# =====================================================================================
function Build-NewsPayload {
    param($item, $tagIds, $categoryId)
    $contentWithSchema = Add-SchemaToContent -Content $item.tresc_html -item $item
    $payload = @{
        name          = $item.tytul
        content       = $contentWithSchema
        short_content = $item.zajawka_html
        lang_id       = 1
        active        = if ($item.PSObject.Properties.Name -contains 'active') { [int]$item.active } else { 1 }
        author        = if ($item.autor) { $item.autor } else { 'Plasmet' }
        start_page    = if ($item.PSObject.Properties.Name -contains 'start_page') { [int]$item.start_page } else { 1 }
        date          = if ($item.planowana_data) { $item.planowana_data } else { (Get-Date -Format 'yyyy-MM-dd') }
        seo_title     = $item.meta_title
        seo_description = $item.meta_description
        seo_keywords  = $item.meta_keywords
    }
    if ($item.seo_url)        { $payload.seo_url   = $item.seo_url }
    # UWAGA: image_name (alt) NIE idzie do POST /news samodzielnie - bez pola 'image' serwer zwraca
    # 400 "must first add image". Alt ustawia sie RAZEM z obrazem w kroku hero (news-hero-upload.ps1).
    # (Mechanizm zweryfikowany krzyzowo 2026-06-10: glowne zdjecie = pole 'image' base64; image_name = jego alt.)
    # tagi: tylko realne (liczbowe) id; placeholdery (nowy:...) odpadaja w LIVE bo sa juz utworzone
    $realTags = @($tagIds | Where-Object { $_ -is [int] })
    if ($realTags.Count -gt 0) { $payload.tags = $realTags }
    # category_id: relacja wpis->kategoria (do potwierdzenia realnym zapisem; bezpieczne w DryRun)
    if ($categoryId -is [int]) { $payload.category_id = $categoryId }
    return $payload
}

# =====================================================================================
#  Hero image: GENERACJA (gemini-generate.ps1) -> UPLOAD (news-hero-upload.ps1). Respektuje $DryRun.
#  Zrodla obrazu wpisu (priorytet):
#    1) hero_image  = sciezka do GOTOWEGO pliku (wzgledna do repoRoot albo absolutna) -> tylko upload.
#    2) hero_prompt = sciezka do .md/.txt z promptem ALBO inline prompt -> najpierw GENERUJ, potem upload.
#       (alias: hero_image_prompt) Slug folderu = seo_url (bazowy slug wpisu).
#  Po generacji oczekiwany plik hero = blog/images/<slug>/hero-1600x900.(webp|jpg|png) — jak w
#  news-hero-upload.ps1 (auto ze sluga). Gemini-generate zapisuje wlasnie '<Slug>-1600x900.*'.
# =====================================================================================
function Get-HeroSlug($item) {
    # slug folderu grafik: preferuj jawny hero_slug, potem seo_url; przytnij ewentualny ogon "-poradnik-..."
    if ($item.PSObject.Properties.Name -contains 'hero_slug' -and $item.hero_slug) { return "$($item.hero_slug)".Trim() }
    if ($item.seo_url) { return "$($item.seo_url)".Trim() }
    return ($item.tytul -replace '[^\p{L}\p{Nd}]+','-').Trim('-').ToLower()
}
function Find-HeroFile($dir) {
    if (-not (Test-Path $dir)) { return $null }
    foreach ($cand in @('hero-1600x900.webp','hero-1600x900.jpg','hero-1600x900.png')) {
        $p = Join-Path $dir $cand
        if (Test-Path $p) { return $p }
    }
    return $null
}
function Resolve-HeroPath($item) {
    if (-not $item.hero_image) { return $null }
    $p = "$($item.hero_image)".Trim()
    if (-not $p) { return $null }
    if ([IO.Path]::IsPathRooted($p)) { return $p }
    return (Join-Path $repoRoot $p)
}
function Get-HeroPrompt($item) {
    foreach ($field in @('hero_prompt','hero_image_prompt')) {
        if ($item.PSObject.Properties.Name -contains $field -and $item.$field) {
            return "$($item.$field)".Trim()
        }
    }
    return $null
}
# Generacja hero z promptu, jesli pliku jeszcze nie ma. Zwraca sciezke do hero albo $null.
function Generate-HeroIfNeeded($item) {
    $prompt = Get-HeroPrompt $item
    if (-not $prompt) { return $null }
    $slug   = Get-HeroSlug $item
    $outDir = Join-Path $repoRoot "blog\images\$slug"
    # juz wygenerowane? nie regeneruj (idempotencja; gemini-generate sam tez tego pilnuje)
    $have = Find-HeroFile $outDir
    if ($have) {
        Write-Host "  HERO-GEN: hero juz istnieje ($([IO.Path]::GetFileName($have))) -> pomijam generacje." -ForegroundColor DarkGray
        return $have
    }
    $genScript = Join-Path (Join-Path $repoRoot 'scripts') 'image-gen\gemini-generate.ps1'
    if (-not (Test-Path $genScript)) {
        Write-Host "  HERO-GEN: brak $genScript -> pomijam generacje (dostarcz skrypt image-gen)." -ForegroundColor Yellow
        return $null
    }
    # -PromptFile gdy prompt wskazuje istniejacy plik; inaczej -Prompt inline
    $promptPath = if ([IO.Path]::IsPathRooted($prompt)) { $prompt } else { Join-Path $repoRoot $prompt }
    $useFile = ($prompt -match '\.(md|txt)$') -and (Test-Path $promptPath)
    $model = if ($item.PSObject.Properties.Name -contains 'hero_model' -and $item.hero_model) { $item.hero_model } else { 'gemini-2.5-flash-image' }

    Write-Host "  HERO-GEN: gemini-generate.ps1 -OutDir blog\images\$slug -Slug hero (DryRun=$DryRun)" -ForegroundColor DarkCyan
    if ($useFile) {
        & $genScript -PromptFile $promptPath -OutDir $outDir -Slug 'hero' -Model $model -DryRun:$DryRun
    } else {
        & $genScript -Prompt $prompt -OutDir $outDir -Slug 'hero' -Model $model -DryRun:$DryRun
    }
    # po generacji (tylko LIVE realnie tworzy pliki) — sprobuj znalezc hero
    return (Find-HeroFile $outDir)
}
function Upload-Hero {
    param($item, [int]$NewsId)
    # 1) gotowy plik z hero_image ma pierwszenstwo
    $heroPath = Resolve-HeroPath $item
    # 2) inaczej: jesli jest prompt grafiki i pliku brak -> wygeneruj
    if (-not $heroPath -or -not (Test-Path $heroPath)) {
        $gen = Generate-HeroIfNeeded $item
        if ($gen) { $heroPath = $gen }
    }
    if (-not $heroPath) {
        Write-Host "  HERO: brak pola hero_image i hero_prompt -> pomijam (wpis bez zdjecia)." -ForegroundColor DarkGray
        return
    }
    if (-not (Test-Path $heroPath)) {
        Write-Host "  HERO: plik '$heroPath' NIE istnieje (DryRun nie tworzy plikow / generacja jeszcze nieodpalona) -> pomijam upload." -ForegroundColor Yellow
        Write-Host "        Po pojawieniu sie pliku: news-hero-upload.ps1 -NewsId $NewsId -ImagePath <plik> -DryRun:`$false" -ForegroundColor DarkGray
        return
    }
    $heroScript = Join-Path $PSScriptRoot 'news-hero-upload.ps1'
    $alt = if ($item.hero_image_alt) { $item.hero_image_alt } else { '' }
    Write-Host "  HERO: news-hero-upload.ps1 -NewsId $NewsId -ImagePath '$heroPath' (DryRun=$DryRun)" -ForegroundColor DarkCyan
    & $heroScript -NewsId $NewsId -ImagePath $heroPath -Alt $alt -DryRun:$DryRun
}

# =====================================================================================
#  Publikacja pojedynczego wpisu
# =====================================================================================
function Publish-One {
    param($file, [ref]$log)
    $item = Get-Content $file.FullName -Raw -Encoding utf8 | ConvertFrom-Json
    $tytul = $item.tytul
    Write-Host "`n=== $($file.Name) :: '$tytul' ===" -ForegroundColor Cyan

    if ($item.status -ne 'gotowy') {
        Write-Host "  POMIJAM: status='$($item.status)' (publikujemy tylko 'gotowy')" -ForegroundColor DarkGray
        return $false
    }
    if (Already-Published $log.Value $tytul) {
        Write-Host "  POMIJAM: juz w published-log.json (idempotencja)" -ForegroundColor DarkGray
        return $false
    }
    $planned = $null
    if ($item.planowana_data) { try { $planned = [datetime]::Parse($item.planowana_data) } catch {} }
    if ($planned -and $planned.Date -gt (Get-Date).Date) {
        Write-Host "  POMIJAM: planowana_data $($item.planowana_data) jeszcze nie nadeszla" -ForegroundColor DarkGray
        return $false
    }

    # 1) tagi + kategoria (find-or-create)
    Write-Host "  [1/3] tagi/kategoria..." -ForegroundColor DarkCyan
    $tagIds = Resolve-TagIds -Names @($item.tagi)
    $catId  = Resolve-CategoryId -Name $item.kategoria

    # 2) payload
    $payload = Build-NewsPayload -item $item -tagIds $tagIds -categoryId $catId

    # SCHEMA: blok JSON-LD doklejany na koniec content w Build-NewsPayload (przezywa 1:1 w news.content).
    # (Wczesniej notatka mowila, ze schema idzie poza webapi - JUZ NIE: doklejamy do content per-post.)

    # 3) POST /news
    if ($DryRun) {
        Write-Host "  [DRY-RUN] NIE wysylam. Payload POST /news ktory BY poszedl:" -ForegroundColor Magenta
        ($payload | ConvertTo-Json -Depth 8) | Write-Host
        Write-Host "  [DRY-RUN] permalink (przewidywany): /pl/blog/$($item.seo_url)/<news_id>" -ForegroundColor Magenta
        # podglad kroku hero (nic nie wysyla - news-hero-upload tez jest w DryRun)
        Upload-Hero -item $item -NewsId 0
        return $false
    }

    Write-Host "  [2/3] POST /news (LIVE)..." -ForegroundColor DarkCyan
    $resp = Invoke-Api -Method Post -Path 'news' -Body $payload
    $newsId = if ($resp.news_id) { $resp.news_id } elseif ($resp -is [int] -or "$resp" -match '^\d+$') { "$resp" } else { $null }
    if (-not $newsId) { throw "POST /news nie zwrocil news_id. Odpowiedz: $($resp | ConvertTo-Json -Compress)" }
    Write-Host "  OK -> news_id=$newsId" -ForegroundColor Green

    # hero image: podpiecie po utworzeniu wpisu (potrzebny news_id)
    Upload-Hero -item $item -NewsId ([int]$newsId)

    # permalink: preferuj seo_url; fallback na slug z tytulu (Shoper i tak generuje z name+id)
    $slug = if ($item.seo_url) { $item.seo_url } else { ($item.tytul -replace '[^\p{L}\p{Nd}]+','-').Trim('-') }
    $permalink = "$($script:baseUrl)/pl/blog/$slug/$newsId"

    # 3) log + status
    Write-Host "  [3/3] log + status=opublikowany..." -ForegroundColor DarkCyan
    $entry = [pscustomobject]@{
        tytul     = $tytul
        news_id   = $newsId
        permalink = $permalink
        data      = (Get-Date -Format 'yyyy-MM-dd HH:mm:ss')
        plik      = $file.Name
    }
    $log.Value = @($log.Value) + $entry
    Save-Log $log.Value

    # przestaw status w pliku kolejki na 'opublikowany' (+ dopisz news_id/permalink)
    $item | Add-Member -NotePropertyName news_id   -NotePropertyValue $newsId   -Force
    $item | Add-Member -NotePropertyName permalink -NotePropertyValue $permalink -Force
    $item.status = 'opublikowany'
    ($item | ConvertTo-Json -Depth 12) | Set-Content $file.FullName -Encoding utf8

    Write-Host "  ZROBIONE: $permalink" -ForegroundColor Green
    return $true
}

# =====================================================================================
#  TRYB DRIP (-DripOne): nienadzorowany run pod Windows Task Scheduler (codziennie 07:00).
#  Bierze JEDEN nastepny wpis 'gotowy' wg planowana_data ASC (przy rownych: nazwa pliku ASC),
#  publikuje go w pelni (hero image base64 + image_name, categories:[5], tagi find-or-create),
#  oznacza 'opublikowany', dopisuje news_id+permalink, published-log.json i _drip-log.txt.
#  Zero zaleznosci interaktywnych. Brak 'gotowy' -> log "BRAK wpisow gotowych" + exit 0.
#  NIE generuje grafik (bez Gemini/ImageMagick) — publikuje tylko gotowe hero z dysku.
# =====================================================================================
$script:BLOG_CAT_NAME = 'Poradnik'   # kategoria bloga (find-or-create; na zywo id=5)

function Find-DripHeroFile {
    param($item)
    # priorytet: jawna sciezka hero_image (wzgledna do repo / absolutna), potem auto z hero_slug/seo_url
    $cands = @()
    if ($item.hero_image -and "$($item.hero_image)".Trim()) {
        $p = "$($item.hero_image)".Trim()
        $cands += $(if ([IO.Path]::IsPathRooted($p)) { $p } else { Join-Path $repoRoot $p })
    }
    $slug = Get-HeroSlug $item
    if ($slug) {
        $dir = Join-Path $repoRoot "blog\images\$slug"
        foreach ($c in @('hero-1600x900.jpg','hero-1600x900.png','hero-1600x900.webp')) { $cands += (Join-Path $dir $c) }
    }
    foreach ($c in $cands) { if ($c -and (Test-Path $c)) { return $c } }
    return $null
}

function Select-NextGotowy {
    # zwraca posortowana liste plikow 'gotowy' (planowana_data ASC, potem nazwa ASC) z dolaczonym obiektem
    if (-not (Test-Path $queueDir)) { throw "Brak katalogu kolejki (moze offline w OneDrive): $queueDir" }
    $cand = @()
    Get-ChildItem $queueDir -Filter '*.json' | Where-Object { $_.Name -notlike '_*' } | ForEach-Object {
        $obj = $null
        # odczyt z retry+hydratacja (plik kolejki bywa "tylko w chmurze" o 07:00); blad parsowania = pomin
        try { $obj = (Read-TextWithRetry -Path $_.FullName -Etykieta "queue/$($_.Name)") | ConvertFrom-Json } catch {
            Write-Host "  UWAGA: nie moge odczytac/sparsowac $($_.Name) ($($_.Exception.Message)) -> pomijam." -ForegroundColor Yellow; return
        }
        if ($obj.status -ne 'gotowy') { return }
        $pd = [datetime]::MaxValue
        if ($obj.planowana_data) { try { $pd = [datetime]::Parse($obj.planowana_data) } catch {} }
        $cand += [pscustomobject]@{ file=$_; obj=$obj; pd=$pd; name=$_.Name }
    }
    return @($cand | Sort-Object pd, name)
}

function Invoke-DripOne {
    Write-Host "`n=== TRYB DRIP (-DripOne): wybor nastepnego 'gotowy' ===" -ForegroundColor Cyan
    $queue = @(Select-NextGotowy)
    if ($queue.Count -eq 0) {
        Write-Host "  BRAK wpisow gotowych (zaden plik blog/queue/*.json nie ma status='gotowy')." -ForegroundColor Yellow
        Write-DripLog -Plik '-' -NewsId '-' -Wynik 'BRAK wpisow gotowych'
        return 0
    }
    Write-Host ("  kandydaci 'gotowy' (wg planowana_data ASC): " + (($queue | ForEach-Object { "$($_.name)[$($_.obj.planowana_data)]" }) -join ', ')) -ForegroundColor DarkCyan

    $log = Load-Log
    foreach ($cand in $queue) {
        $file = $cand.file; $item = $cand.obj; $tytul = $item.tytul
        $script:currentDripFile = $file.Name   # do raportu bledu (catch wie, na ktorym pliku padlo)
        Write-Host "`n--- KANDYDAT: $($file.Name) :: '$tytul' (planowana_data=$($item.planowana_data)) ---" -ForegroundColor Cyan

        # idempotencja po tytule (published-log)
        if (Already-Published $log $tytul) {
            Write-Host "  POMIJAM: '$tytul' juz w published-log.json (idempotencja) -> nastepny." -ForegroundColor DarkGray
            Write-DripLog -Plik $file.Name -NewsId '-' -Wynik 'POMINIETO: juz w published-log'
            continue
        }
        # BRAMKA 1: surowe [LINK:...] -> nie publikuj, pomin
        $content = $item.tresc_html
        $leftover = [regex]::Matches("$content", '\[LINK:[^\]]*\]')
        if ($leftover.Count -gt 0) {
            $names = ($leftover | ForEach-Object { $_.Value }) -join ' '
            Write-Host "  OSTRZEZENIE: surowe placeholdery linkow w tresci ($names) -> NIE publikuje, pomijam." -ForegroundColor Yellow
            Write-DripLog -Plik $file.Name -NewsId '-' -Wynik "POMINIETO: surowe [LINK:] ($($leftover.Count))"
            continue
        }
        # BRAMKA 1b: dlugie myslniki -> zakaz twardy (decyzja usera); nie publikuj
        $EMDASH = [char]0x2014; $ENDASH = [char]0x2013
        $polaDoSprawdzenia = @{ 'tresc_html' = "$content"; 'tytul' = "$($item.tytul)";
                                'meta_title' = "$($item.meta_title)"; 'meta_description' = "$($item.meta_description)";
                                'zajawka_html' = "$($item.zajawka_html)" }
        $zleMyslniki = @()
        foreach ($k in $polaDoSprawdzenia.Keys) {
            $v = $polaDoSprawdzenia[$k]
            if ($v -and (($v.Contains($EMDASH)) -or ($v.Contains($ENDASH)))) { $zleMyslniki += $k }
        }
        if ($zleMyslniki.Count -gt 0) {
            Write-Host "  OSTRZEZENIE: dlugi myslnik w polach: $($zleMyslniki -join ', ') -> NIE publikuje, pomijam." -ForegroundColor Yellow
            Write-DripLog -Plik $file.Name -NewsId '-' -Wynik "POMINIETO: dlugi myslnik ($($zleMyslniki -join ','))"
            continue
        }

        # KAFELKI PRODUKTOWE: rozwin [PRODUKT:]/[PRODUKTY:] na HTML z danymi NA ZYWO z webapi
        if ("$content" -match '\[PRODUKT[Y]?:') {
            $pcScript = Join-Path $PSScriptRoot 'product-cards.ps1'
            if (-not (Test-Path $pcScript)) {
                Write-Host "  OSTRZEZENIE: brak product-cards.ps1, a tresc ma kafelki -> NIE publikuje, pomijam." -ForegroundColor Yellow
                Write-DripLog -Plik $file.Name -NewsId '-' -Wynik 'POMINIETO: brak product-cards.ps1'
                continue
            }
            $tmpIn  = Join-Path $env:TEMP ("pcards-in-"  + [Guid]::NewGuid().ToString('N') + '.html')
            $tmpOut = Join-Path $env:TEMP ("pcards-out-" + [Guid]::NewGuid().ToString('N') + '.html')
            [IO.File]::WriteAllText($tmpIn, "$content", (New-Object Text.UTF8Encoding($false)))
            try {
                & $pcScript -InFile $tmpIn -OutFile $tmpOut | Out-Null
                $content = [IO.File]::ReadAllText($tmpOut, [Text.Encoding]::UTF8)
            } catch {
                Write-Host "  OSTRZEZENIE: render kafelkow nieudany ($($_.Exception.Message)) -> NIE publikuje, pomijam." -ForegroundColor Yellow
                Write-DripLog -Plik $file.Name -NewsId '-' -Wynik 'POMINIETO: blad renderu kafelkow'
                Remove-Item $tmpIn,$tmpOut -ErrorAction SilentlyContinue
                continue
            }
            Remove-Item $tmpIn,$tmpOut -ErrorAction SilentlyContinue
            $zostaly = [regex]::Matches("$content", '\[PRODUKT[Y]?:[^\]]*\]')
            if ($zostaly.Count -gt 0) {
                Write-Host "  OSTRZEZENIE: surowe placeholdery kafelkow po renderze ($($zostaly.Count)) -> NIE publikuje, pomijam." -ForegroundColor Yellow
                Write-DripLog -Plik $file.Name -NewsId '-' -Wynik "POMINIETO: surowe [PRODUKT:] ($($zostaly.Count))"
                continue
            }
            $ileKafelkow = [regex]::Matches("$content", 'w sklepie</span>').Count
            Write-Host "  kafelki produktowe: $ileKafelkow" -ForegroundColor DarkGray
        }

        # BRAMKA 2: hero musi istniec (nie publikujemy bez zdjecia)
        $heroPath = Find-DripHeroFile $item
        if (-not $heroPath) {
            Write-Host "  OSTRZEZENIE: brak pliku hero (hero-1600x900.jpg w blog/images/<slug>/) -> NIE publikuje, pomijam." -ForegroundColor Yellow
            Write-DripLog -Plik $file.Name -NewsId '-' -Wynik 'POMINIETO: brak pliku hero'
            continue
        }
        Write-Host "  hero: $heroPath" -ForegroundColor DarkGray

        # --- SCHEMA JSON-LD: doklej blok <script ld+json> na koniec content (idempotentnie) ---
        # Po bramce [LINK:] (dziala na surowej tresc_html), zeby kazdy wpis z dripu dostal scheme.
        $content = Add-SchemaToContent -Content $content -item $item

        # --- tagi find-or-create (idempotencja po name, z paginacja) ---
        Write-Host "  [1/4] tagi (find-or-create)..." -ForegroundColor DarkCyan
        $tagList = Get-AllPaged 'news-tags'
        $tagIds = @()
        foreach ($tn in @($item.tagi)) {
            $found = $tagList | Where-Object { $_.name -eq $tn } | Select-Object -First 1
            if ($found) { $tagIds += [int]$found.tag_id; continue }
            if ($DryRun) { Write-Host "      [DRY] utworzylbym tag '$tn'" -ForegroundColor DarkYellow; continue }
            $null = Invoke-WriteWithDeadline 'Post' 'news-tags' ([ordered]@{ name=$tn; lang_id=1 })
            Start-Sleep -Milliseconds $ThrottleMs
            $tagList = Get-AllPaged 'news-tags'
            $created = $tagList | Where-Object { $_.name -eq $tn } | Select-Object -First 1
            if ($created) { $tagIds += [int]$created.tag_id; Write-Host "      + tag '$tn' -> $($created.tag_id)" -ForegroundColor Green }
            else { Write-Host "      ! nie utworzono tagu '$tn'" -ForegroundColor Red }
        }
        Write-Host "      tag_ids: $($tagIds -join ', ')" -ForegroundColor DarkCyan

        # --- kategoria bloga (find-or-create) ---
        $catName = if ($item.kategoria) { $item.kategoria } else { $script:BLOG_CAT_NAME }
        $catId = $null
        foreach ($c in (Get-AllPaged 'news-categories')) { if ($c.name -eq $catName) { $catId = [int]$c.category_id; break } }
        if (-not $catId -and -not $DryRun) {
            $null = Invoke-WriteWithDeadline 'Post' 'news-categories' ([ordered]@{ name=$catName; lang_id=1; active=1 })
            Start-Sleep -Milliseconds $ThrottleMs
            foreach ($c in (Get-AllPaged 'news-categories')) { if ($c.name -eq $catName) { $catId = [int]$c.category_id; break } }
        }
        Write-Host "      kategoria '$catName' -> category_id=$catId" -ForegroundColor DarkCyan

        # --- hero base64 + payload POST /news ---
        # odczyt hero z retry+hydratacja (plik bywa "tylko w chmurze" o 07:00 -> wymus sciagniecie bajtow)
        $imgBytes = Read-FileBytesWithRetry -Path $heroPath -Etykieta 'hero'
        $imgB64   = [Convert]::ToBase64String($imgBytes)
        $sizeKB   = [math]::Round($imgBytes.Length/1KB,1)
        $alt      = if ($item.hero_image_alt) { $item.hero_image_alt } else { $tytul }
        $payload = [ordered]@{
            name=$tytul; content=$content; short_content=$item.zajawka_html
            lang_id=1
            active=$(if ($item.PSObject.Properties.Name -contains 'active') { [int]$item.active } else { 1 })
            start_page=$(if ($item.PSObject.Properties.Name -contains 'start_page') { [int]$item.start_page } else { 1 })
            date=$(if ($item.planowana_data) { $item.planowana_data } else { (Get-Date -Format 'yyyy-MM-dd') })
            author=$(if ($item.autor) { $item.autor } else { 'Plasmet' })
            seo_title=$item.meta_title; seo_description=$item.meta_description
            seo_keywords=$item.meta_keywords; seo_url=$item.seo_url
            image=$imgB64; image_name=$alt
        }
        if ($catId) { $payload['categories'] = @($catId) }
        if ($tagIds.Count -gt 0) { $payload['tags'] = @($tagIds) }

        if ($DryRun) {
            $hasSchema  = "$content" -match '<script[^>]*type\s*=\s*["'']application/ld\+json["'']'
            $endsScript = "$content".TrimEnd().EndsWith('</script>')
            $tail = "$content".TrimEnd(); $tail = $tail.Substring([math]::Max(0,$tail.Length-60))
            Write-Host "  [DRY-RUN] NIE wysylam POST /news. Payload zbudowany:" -ForegroundColor Magenta
            Write-Host ("      name='$tytul'  active=$($payload.active)  start_page=$($payload.start_page)  date=$($payload.date)") -ForegroundColor Magenta
            Write-Host ("      image=base64(${sizeKB}KB)  image_name='$alt'  categories=[$catId]  tags=[$($tagIds -join ',')]") -ForegroundColor Magenta
            Write-Host ("      seo_url='$($item.seo_url)'  -> permalink: $($script:baseUrl)/pl/news/$($item.seo_url)") -ForegroundColor Magenta
            Write-Host ("      content_len=$("$content".Length)  ma_script_ldjson=$hasSchema  konczy_sie_</script>=$endsScript") -ForegroundColor Magenta
            Write-Host ("      content TAIL: ...$tail") -ForegroundColor DarkGray
            Write-DripLog -Plik $file.Name -NewsId '-' -Wynik "DRY-RUN: WYBRANO do publikacji (hero ${sizeKB}KB, cat=$catId, tagi=$($tagIds.Count), schema=$hasSchema)"
            return 0   # drip: dokladnie 1 wpis na przebieg
        }

        # --- LIVE: POST /news (idempotencja po name) ---
        Write-Host "  [2/4] POST /news (LIVE)..." -ForegroundColor DarkCyan
        $allNews  = Get-AllPaged 'news'
        $existing = $allNews | Where-Object { $_.name -eq $tytul } | Select-Object -First 1
        $newsId = $null
        if ($existing) {
            $newsId = [int]$existing.news_id
            Write-Host "      ISTNIEJE news_id=$newsId -> PUT (aktualizacja, NIE duplikuje)" -ForegroundColor Yellow
            $null = Invoke-WriteWithDeadline 'Put' "news/$newsId" $payload
        } else {
            $w = Invoke-WriteWithDeadline 'Post' 'news' $payload
            Write-Host "      returned=$($w.returned) code=$($w.code) raw=$($w.raw)" -ForegroundColor DarkGray
            if ($w.returned -and ("$($w.raw)" -match '^\d+$')) { $newsId = [int]$w.raw }
            Start-Sleep -Milliseconds $ThrottleMs
            if (-not $newsId) {
                # HANG/TIMEOUT lub brak body -> weryfikacja GET (anti-'wiszacy zapis')
                $made = (Get-AllPaged 'news') | Where-Object { $_.name -eq $tytul } | Select-Object -First 1
                if ($made) { $newsId = [int]$made.news_id; Write-Host "      GET potwierdzil news_id=$newsId" -ForegroundColor Green }
            } else { Write-Host "      POST OK -> news_id=$newsId" -ForegroundColor Green }
        }
        if (-not $newsId) {
            Write-Host "  BLAD: POST/PUT nie zwrocil i GET nie potwierdzil news_id -> przerywam ten wpis." -ForegroundColor Red
            Write-DripLog -Plik $file.Name -NewsId '-' -Wynik 'BLAD: brak news_id po POST (sprawdz panel)'
            return 1
        }
        Start-Sleep -Milliseconds $ThrottleMs

        # --- [3/4] weryfikacja hero + fallback PUT, twardy test obecnosci obrazu ---
        Write-Host "  [3/4] weryfikacja hero + kategoria..." -ForegroundColor DarkCyan
        $news = Invoke-Api -Method Get -Path "news/$newsId"
        if (-not $news.image_name) {
            Write-Host "      image_name PUSTE -> fallback PUT { image, image_name }" -ForegroundColor Yellow
            $null = Invoke-WriteWithDeadline 'Put' "news/$newsId" ([ordered]@{ image=$imgB64; image_name=$alt })
            Start-Sleep -Milliseconds $ThrottleMs
            $news = Invoke-Api -Method Get -Path "news/$newsId"
        }
        $tw = Invoke-WriteWithDeadline 'Put' "news/$newsId" ([ordered]@{ image_name=$alt })
        $imgPresent = ($tw.code -eq 200) -or ($tw.returned -and -not $tw.code -and "$($tw.raw)" -notmatch 'must first add image')
        Write-Host "      obraz_obecny=$imgPresent (PUT image_name SOLO -> code=$($tw.code))" -ForegroundColor $(if($imgPresent){'Green'}else{'Yellow'})
        Start-Sleep -Milliseconds $ThrottleMs

        # weryfikacja/dowiazanie kategorii (POST categories[] zwykle wiaze; fallback PUT)
        $catBound = $false
        if ($catId) {
            $enc = [System.Uri]::EscapeDataString('{"category_id":"' + $catId + '"}')
            $inCat = (Invoke-Api -Method Get -Path "news?filters=$enc&limit=50").list | ForEach-Object { [int]$_.news_id }
            if ($inCat -contains $newsId) { $catBound = $true }
            else {
                $null = Invoke-WriteWithDeadline 'Put' "news/$newsId" ([ordered]@{ categories=@($catId) })
                Start-Sleep -Milliseconds $ThrottleMs
                $inCat2 = (Invoke-Api -Method Get -Path "news?filters=$enc&limit=50").list | ForEach-Object { [int]$_.news_id }
                if ($inCat2 -contains $newsId) { $catBound = $true }
            }
        }
        Write-Host "      active=$($news.active) start_page=$($news.start_page) kategoria_powiazana=$catBound" -ForegroundColor Green

        # --- [4/4] log + status=opublikowany ---
        Write-Host "  [4/4] log + status=opublikowany..." -ForegroundColor DarkCyan
        $slug = if ($item.seo_url) { $item.seo_url } else { ($tytul -replace '[^\p{L}\p{Nd}]+','-').Trim('-') }
        $permalink = "$($script:baseUrl)/pl/news/$slug"

        $entry = [pscustomobject]@{
            tytul=$tytul; news_id="$newsId"; permalink=$permalink
            data=(Get-Date -Format 'yyyy-MM-dd HH:mm:ss'); plik=$file.Name
            image_present=$imgPresent; category_bound=$catBound; tag_ids=$tagIds
            opublikowano_przez='blog-publish.ps1 -DripOne'
        }
        $log = @($log) + $entry
        Save-Log $log

        $item | Add-Member -NotePropertyName news_id        -NotePropertyValue "$newsId"  -Force
        $item | Add-Member -NotePropertyName permalink_front -NotePropertyValue $permalink -Force
        $item.status = 'opublikowany'
        ($item | ConvertTo-Json -Depth 12) | Set-Content $file.FullName -Encoding utf8

        Write-Host "  ZROBIONE: news_id=$newsId  $permalink" -ForegroundColor Green
        Write-DripLog -Plik $file.Name -NewsId "$newsId" -Wynik "OK opublikowano (img=$imgPresent, cat=$catBound, tagi=$($tagIds.Count))"
        return 0   # drip: dokladnie 1 wpis na przebieg
    }

    # wszystkie kandydaty pominiete (linki/hero/idempotencja) — to nie blad
    Write-Host "`n  Wszystkie wpisy 'gotowy' pominieto (surowe [LINK:], brak hero lub juz opublikowane)." -ForegroundColor Yellow
    Write-DripLog -Plik '-' -NewsId '-' -Wynik 'BRAK publikowalnych (wszystkie gotowe pominieto)'
    return 0
}

# =====================================================================================
#  MAIN
# =====================================================================================
$trybTxt = if ($DryRun) { 'DRY-RUN (podglad, ZERO zapisu)' } else { 'LIVE (zapis do zywego sklepu!)' }
$trybKol = if ($DryRun) { 'Cyan' } else { 'Red' }
Write-Host ("blog-publish.ps1 - tryb: " + $trybTxt) -ForegroundColor $trybKol

# ----- TRYB DRIP: 1 nastepny 'gotowy', nienadzorowany (Task Scheduler 07:00). Konczy z exit code. -----
#  CALY przebieg w jednym try/catch. KAZDY blad (tez wczesny: .env/hero/auth/wyjatek) jest LOGOWANY
#  do _drip-log.txt (wiersz BLAD) ORAZ _drip-error.txt (pelny zrzut: msg/stack/pozycja) -> kolejna
#  cicha awaria 07:00 bedzie udokumentowana. Sciezki logow z $PSScriptRoot (znane od gory pliku).
$script:currentDripFile = '?'
if ($DripOne) {
    try {
        Initialize-Env            # odczyt .env z retry+hydratacja OneDrive (przedtem rzucal CICHO na top-level)
        Get-Token | Out-Null      # auth z retry sieci/5xx/timeout
        $rc = Invoke-DripOne
        Write-Host "`nDRIP zakonczony (exit=$rc)." -ForegroundColor $(if ($rc -eq 0) { 'Green' } else { 'Red' })
        exit $rc
    } catch {
        # nienadzorowany run: ZAWSZE zaloguj (oba pliki) i wyjdz 1 (Task Scheduler odnotuje).
        $msg  = $_.Exception.Message
        $plik = $script:currentDripFile
        Write-Host "DRIP BLAD KRYTYCZNY (plik=$plik): $msg" -ForegroundColor Red
        Write-DripLog   -Plik $plik -NewsId '-' -Wynik "BLAD: $msg"   # wiersz: LIVE | plik=<lub ?> | news_id=- | BLAD: ...
        Write-DripError -ErrRecord $_ -Plik $plik                     # pelny zrzut do _drip-error.txt
        exit 1
    }
}

Initialize-Env
Get-Token | Out-Null
$log = Load-Log

# wybor plikow: konkretny -Plik, albo cala kolejka posortowana po planowana_data/nazwie
$files = if ($Plik) {
    @(Get-Item (Join-Path $queueDir $Plik))
} else {
    Get-ChildItem $queueDir -Filter '*.json' | Where-Object { $_.Name -notlike '_*' } | Sort-Object Name
}

if (-not $files -or $files.Count -eq 0) { Write-Host "Kolejka pusta (blog/queue/*.json)." -ForegroundColor Yellow; return }

$logRef = [ref]$log
$published = 0
foreach ($f in $files) {
    $ok = Publish-One -file $f -log $logRef
    if ($ok) {
        $published++
        if (-not $All) { break }   # drip: domyslnie 1 wpis na przebieg
    }
}

$podsKol = if ($DryRun) { 'Cyan' } else { 'Green' }
Write-Host "`nPODSUMOWANIE: opublikowano $published wpisow. Log: $logPath" -ForegroundColor $podsKol
if ($DryRun) {
    $hint = 'To byl DRY-RUN - nic nie wyslano. Realna publikacja: -DryRun:$false'
    Write-Host $hint -ForegroundColor Magenta
}
