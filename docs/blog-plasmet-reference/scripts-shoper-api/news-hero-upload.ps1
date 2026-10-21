# =====================================================================================
#  news-hero-upload.ps1 - ustawia GLOWNE ZDJECIE (hero/miniature) wpisu bloga (news)
# -------------------------------------------------------------------------------------
#  MECHANIZM (potwierdzony na zywo 2026-06-10 logika krzyzowa, news_id=7):
#    GLOWNE ZDJECIE wpisu = pole `image` (base64 BINARKI pliku) w PUT /webapi/rest/news/{id}
#    ALT/opis tego zdjecia = pole `image_name` (PUT) - dziala TYLKO gdy obraz juz istnieje
#       (PUT image_name SOLO bez obrazu -> 400 "must first add image").
#    To pole motyw renderuje jako MINIATURE na liscie bloga + ZDJECIE w tresci wpisu.
#
#  WAZNE - to NIE jest `news-files`:
#    Zasob `news-files` to OSOBNA galeria/zalaczniki wpisu i NIE jest renderowany jako hero.
#    (Wczesniejsze zalozenie "pierwszy plik news-files = hero" bylo BLEDNE - zweryfikowane na froncie.)
#
#  Format pola `image`: czysty base64 zawartosci pliku (NIE data-URI, NIE URL).
#    data-URI -> 400 "Cannot decode the contents of the file".
#  Usuniecie obrazu: PUT news/{id} image='' (pusty string).
#
#  Ten skrypt:
#    - bierze plik hero (-ImagePath lub auto z blog/images/<slug>/),
#    - PUT news/{id} { image=<base64>, [image_name=<alt>] } (alt razem z obrazem - inaczej 400),
#    - wzorzec anty-'wiszacy zapis' (HttpWebRequest + .Timeout/.ReadWriteTimeout/.KeepAlive=$false),
#    - DOMYSLNIE -DryRun = TRUE.
#  Bezpieczenstwo: NIE wypisuje loginu/hasla/tokenu. Zmienia zywy sklep tylko gdy -DryRun:$false.
#
#  Podglad:  powershell -ExecutionPolicy Bypass -File .\news-hero-upload.ps1 -NewsId 7 -Slug 01-jak-wybrac-wiertarko-wkretarke
#  LIVE:     ...\news-hero-upload.ps1 -NewsId 7 -Slug 01-jak-wybrac-wiertarko-wkretarke -Alt "..." -DryRun:$false
#  Usun hero:...\news-hero-upload.ps1 -NewsId 7 -RemoveImage -DryRun:$false
# =====================================================================================
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][int] $NewsId,
    [string] $ImagePath = $null,                 # konkretny plik obrazu (jpg/png/webp)
    [string] $Slug      = $null,                 # albo slug -> auto z blog/images/<slug>/hero-1600x900.(jpg|webp|png)
    [string] $Alt       = $null,                 # alt/opis -> pole 'image_name' (SEO/WCAG)
    [switch] $RemoveImage,                        # usun glowny obraz (PUT image='')
    [bool]   $DryRun    = $true,
    [int]    $WriteDeadlineSec = 25,              # twardy deadline na zapis (anty-'wiszacy zapis'); wieksze pliki = wiecej
    [int]    $ThrottleMs = 400
)
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# --- .env + auth (sekrety tylko z .env) ---
$envPath = Join-Path $PSScriptRoot '.env'
if (-not (Test-Path $envPath)) { throw "Brak .env" }
$cfg = @{}
Get-Content $envPath | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
    $p = $_ -split '=', 2; $cfg[$p[0].Trim()] = $p[1].Trim().Trim('"')
}
$url=($cfg['SHOPER_URL']).TrimEnd('/'); $login=$cfg['SHOPER_LOGIN']; $pass=$cfg['SHOPER_PASSWORD']; $permToken=$cfg['SHOPER_TOKEN']
if ($permToken) { $token=$permToken; Write-Host "AUTH: token permanentny (zredagowany)" -ForegroundColor Green }
else {
    $basic=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($login):$($pass)"))
    $token=(Invoke-RestMethod -Method Post -Uri "$url/webapi/rest/auth" -Headers @{Authorization="Basic $basic"}).access_token
    Write-Host "AUTH OK (zredagowany)" -ForegroundColor Green
}
if (-not $token){throw "Brak tokenu"}
$hdr=@{Authorization="Bearer $token"}

function Invoke-WriteWithDeadline($method, $path, $obj) {
    $json=$obj|ConvertTo-Json -Depth 8 -Compress; $bytes=[Text.Encoding]::UTF8.GetBytes($json); $ms=$WriteDeadlineSec*1000
    $req=[System.Net.HttpWebRequest]::Create("$url/webapi/rest/$path")
    $req.Method=$method.ToUpper(); $req.ContentType='application/json; charset=utf-8'; $req.Accept='application/json'
    $req.Headers['Authorization']=$hdr['Authorization']; $req.Timeout=$ms; $req.ReadWriteTimeout=$ms; $req.KeepAlive=$false
    try { $rs=$req.GetRequestStream(); $rs.Write($bytes,0,$bytes.Length); $rs.Close()
        $resp=$req.GetResponse(); $sr=New-Object IO.StreamReader($resp.GetResponseStream()); $body=$sr.ReadToEnd(); $sr.Close(); $code=[int]$resp.StatusCode; $resp.Close()
        return [pscustomobject]@{ returned=$true; code=$code; raw=$body.Trim() }
    } catch [System.Net.WebException] {
        if ($_.Exception.Status -eq [System.Net.WebExceptionStatus]::Timeout) { try{$req.Abort()}catch{}; return [pscustomobject]@{ returned=$false; code=$null; raw='HANG/TIMEOUT' } }
        $code=$null;$eb=$null; try{$code=[int]$_.Exception.Response.StatusCode}catch{}; try{$s=$_.Exception.Response.GetResponseStream(); $eb=(New-Object IO.StreamReader($s)).ReadToEnd()}catch{}
        return [pscustomobject]@{ returned=$true; code=$code; raw=$eb }
    } catch { return [pscustomobject]@{ returned=$false; code=$null; raw="EXC:$($_.Exception.Message)" } }
}

# --- TRYB USUNIECIA OBRAZU ---
if ($RemoveImage) {
    Write-Host "USUWANIE glownego obrazu news_id=$NewsId (PUT image='')" -ForegroundColor Cyan
    if ($DryRun) { Write-Host "[DRY-RUN] NIE wysylam. PUT news/$NewsId { image = '' }" -ForegroundColor Magenta; return }
    $r = Invoke-WriteWithDeadline 'Put' "news/$NewsId" @{ image = '' }
    Write-Host "  HTTP $($r.code) raw='$($r.raw)'" -ForegroundColor DarkGray
    $after = (Invoke-RestMethod -Method Get -Uri "$url/webapi/rest/news/$NewsId" -Headers $hdr).image_name
    Write-Host "  GET image_name = '$after' (po usunieciu zwykle puste)" -ForegroundColor Green
    return
}

# --- rozwiazanie sciezki obrazu ---
$repoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
if (-not $ImagePath -and $Slug) {
    $dir = Join-Path $repoRoot "blog\images\$Slug"
    foreach ($cand in @('hero-1600x900.webp','hero-1600x900.jpg','hero-1600x900.png')) {
        $p = Join-Path $dir $cand
        if (Test-Path $p) { $ImagePath = $p; break }
    }
    if (-not $ImagePath) { throw "Nie znaleziono hero-1600x900.(webp|jpg|png) w $dir. Podaj -ImagePath." }
}
if (-not $ImagePath) { throw "Podaj -ImagePath (plik) albo -Slug (auto z blog/images/<slug>/), albo -RemoveImage." }
if (-not [IO.Path]::IsPathRooted($ImagePath)) { $ImagePath = Join-Path (Get-Location) $ImagePath }
if (-not (Test-Path $ImagePath)) { throw "Plik obrazu nie istnieje: $ImagePath" }

$imgBytes  = [IO.File]::ReadAllBytes($ImagePath)
$sizeKB    = [math]::Round($imgBytes.Length/1KB,1)
$contentB64= [Convert]::ToBase64String($imgBytes)
$leaf      = Split-Path $ImagePath -Leaf
Write-Host "HERO (glowne zdjecie): '$leaf' ($sizeKB KB) -> news_id=$NewsId" -ForegroundColor Cyan
if ($Alt) { Write-Host "  alt (image_name): $Alt" -ForegroundColor DarkGray }

# --- payload: image (base64) + image_name (alt) razem (alt SOLO bez obrazu -> 400) ---
$payload = [ordered]@{ image = $contentB64 }
if ($Alt) { $payload['image_name'] = $Alt }

if ($DryRun) {
    Write-Host "`n[DRY-RUN] NIE wysylam. PUT /news/$NewsId ktory BY poszedl:" -ForegroundColor Magenta
    Write-Host ("  { image = base64(${sizeKB}KB)$(if($Alt){"; image_name = '$Alt'"}) }") -ForegroundColor Magenta
    Write-Host "  [DRY-RUN] po LIVE: motyw renderuje to jako miniature listy + zdjecie wpisu." -ForegroundColor Magenta
    return
}

# --- LIVE: PUT news/{id} image+alt ---
Write-Host "`n[LIVE] PUT /news/$NewsId (image + alt) ..." -ForegroundColor Cyan
$r = Invoke-WriteWithDeadline 'Put' "news/$NewsId" $payload
Write-Host "  HTTP $($r.code) returned=$($r.returned) raw='$($r.raw)'" -ForegroundColor DarkGray
Start-Sleep -Milliseconds $ThrottleMs

# weryfikacja GET: po wgraniu obrazu image_name (alt) jest zapisane (dowod, ze obraz istnieje)
$n = Invoke-RestMethod -Method Get -Uri "$url/webapi/rest/news/$NewsId" -Headers $hdr
Write-Host "  GET image_name = '$($n.image_name)'" -ForegroundColor Green
if ($Alt -and $n.image_name -ne $Alt) {
    Write-Host "  UWAGA: image_name != podany alt - sprawdz odpowiedz serwera (raw wyzej)." -ForegroundColor Yellow
} else {
    Write-Host "  OK -> glowny obraz ustawiony (image_name=alt potwierdza, ze obraz istnieje)." -ForegroundColor Green
}
Write-Host "`nGOTOWE. Render miniatury/zdjecia potwierdzic w panelu/na produkcji." -ForegroundColor Green
