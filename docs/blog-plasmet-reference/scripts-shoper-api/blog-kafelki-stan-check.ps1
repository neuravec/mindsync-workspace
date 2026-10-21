# blog-kafelki-stan-check.ps1 - READ-ONLY kontrola kafelkow produktowych w kolejce bloga.
#
# PO CO: `product-cards.ps1` (renderer kafelkow wolany przez blog-publish.ps1) PRZERYWA publikacje,
# gdy produkt z kafelka ma stan 0 albo nie ma zdjecia. Wpis z takim kafelkiem nie opublikuje sie
# o 07:00 i blog milczy tego dnia. Ten skrypt sprawdza to Z WYPRZEDZENIEM.
#
# Uruchom recznie przed publikacja albo z harmonogramu (codziennie, przed dripem):
#   powershell -File .\blog-kafelki-stan-check.ps1
#   powershell -File .\blog-kafelki-stan-check.ps1 -Dni 3      # tylko wpisy z najblizszych 3 dni
#
# Kod wyjscia: 1 gdy jakikolwiek kafelek jest zablokowany (stan 0 / nieaktywny / brak produktu).
# ZERO POST/PUT/DELETE.
param(
    [int] $Dni = 0,                 # 0 = wszystkie wpisy 'gotowy'; N = tylko publikowane w najblizszych N dniach
    [switch] $TylkoProblemy
)
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

$repoRoot = Resolve-Path (Join-Path $PSScriptRoot '..\..')
$queueDir = Join-Path $repoRoot 'blog\queue'
$reconPath = Join-Path $queueDir '_kafelki-partiaD-72-81.json'

# --- auth ---
$envPath = Join-Path $PSScriptRoot '.env'
$cfg = @{}
Get-Content $envPath | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
    $p = $_ -split '=', 2; $cfg[$p[0].Trim()] = $p[1].Trim().Trim('"')
}
$url = ($cfg['SHOPER_URL']).TrimEnd('/')
$basic = [Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($cfg['SHOPER_LOGIN']):$($cfg['SHOPER_PASSWORD'])"))
$auth = Invoke-RestMethod -Method Post -Uri "$url/webapi/rest/auth" -Headers @{ Authorization = "Basic $basic" }
$hdr = @{ Authorization = "Bearer $($auth.access_token)" }

# --- kafelki z kolejki ---
$dzis = Get-Date
$uzycie = @{}   # id -> lista "nr(data)"
$wpisy = @()
Get-ChildItem $queueDir -Filter '*.json' | Where-Object { $_.Name -notlike '_*' } | ForEach-Object {
    try { $o = Get-Content $_.FullName -Raw -Encoding UTF8 | ConvertFrom-Json } catch { return }
    if ("$($o.status)" -ne 'gotowy') { return }
    $data = [datetime]::Parse(("$($o.planowana_data)".Substring(0, 10)))
    if ($Dni -gt 0 -and ($data - $dzis).TotalDays -gt $Dni) { return }
    $h = "$($o.tresc_html)"
    $ids = @()
    foreach ($m in [regex]::Matches($h, '\[PRODUKT:\s*(\d+)')) { $ids += $m.Groups[1].Value }
    foreach ($m in [regex]::Matches($h, '\|\|\s*(\d+)\s*\|')) { $ids += $m.Groups[1].Value }
    $nr = $_.Name.Substring(0, 2)
    foreach ($i in $ids) {
        if (-not $uzycie.ContainsKey($i)) { $uzycie[$i] = @() }
        $uzycie[$i] += ("{0} ({1:yyyy-MM-dd})" -f $nr, $data)
    }
    $wpisy += [pscustomobject]@{ nr = $nr; data = $data; plik = $_.Name; ids = $ids }
}

if (-not $wpisy) { Write-Host "Brak wpisow 'gotowy' w zakresie." -ForegroundColor Yellow; exit 0 }
Write-Host ("Wpisow 'gotowy' w zakresie: {0} | unikalnych produktow w kafelkach: {1}" -f $wpisy.Count, $uzycie.Keys.Count) -ForegroundColor Cyan

# --- zapasowi kandydaci z rekonesansu (jesli plik istnieje) ---
$zapas = @{}
if (Test-Path $reconPath) {
    try {
        $r = Get-Content $reconPath -Raw -Encoding UTF8 | ConvertFrom-Json
        foreach ($nr in $r.wpisy.PSObject.Properties.Name) {
            foreach ($slot in $r.wpisy.$nr.slots.PSObject.Properties.Name) {
                $s = $r.wpisy.$nr.slots.$slot
                if ($s.glowny -and $s.zapasowe) {
                    $zapas["$($s.glowny.product_id)"] = ($s.zapasowe | ForEach-Object { "$($_.product_id) ($($_.nazwa)), stan $($_.stan)" })
                }
            }
        }
    } catch { }
}

# --- weryfikacja live ---
$problemy = @()
foreach ($id in ($uzycie.Keys | Sort-Object { [int]$_ })) {
    $nazwa = '?'; $stan = $null; $akt = '?'; $blad = $null
    # throttling: webapi Shopera zwraca 429 przy szybkiej serii GET-ow, a 429 to NIE brak stanu.
    # Bez tego skrypt raportowalby falszywe blokady (zlapane przy pierwszym przebiegu 2026-08-17).
    for ($proba = 1; $proba -le 4; $proba++) {
        try {
            $p = Invoke-RestMethod -Method Get -Uri "$url/webapi/rest/products/$id" -Headers $hdr
            $tr = $p.translations.PSObject.Properties | Select-Object -First 1
            if ($tr) { $nazwa = $tr.Value.name }
            $stan = [double]$p.stock.stock
            $akt = "$($p.stock.active)"
            $blad = $null
            break
        } catch {
            $kod = if ($_.Exception.Response) { [int]$_.Exception.Response.StatusCode } else { 0 }
            $blad = $_.Exception.Message
            if ($kod -eq 429 -or $kod -eq 504 -or $kod -eq 502) {
                Start-Sleep -Seconds (3 * $proba)   # backoff: 3, 6, 9 s
            } else { break }
        }
    }
    Start-Sleep -Milliseconds 350

    $zle = $blad -or ($stan -le 0) -or ($akt -eq '0')
    if (-not $zle -and $TylkoProblemy) { continue }
    $kolor = if ($zle) { 'Red' } elseif ($stan -le 3) { 'Yellow' } else { 'Green' }
    $opis = if ($blad) { "BLAD: $blad" } else { ("stan {0,-6} aktywny {1}  {2}" -f $stan, $akt, $nazwa) }
    Write-Host ("  id {0,-6} {1}" -f $id, $opis) -ForegroundColor $kolor
    Write-Host ("           uzywany w: {0}" -f ($uzycie[$id] -join ', ')) -ForegroundColor DarkGray
    if ($zle) {
        $problemy += $id
        if ($zapas.ContainsKey($id)) {
            Write-Host ("           ZAPAS z rekonesansu: {0}" -f ($zapas[$id] -join ' | ')) -ForegroundColor Magenta
        } else {
            Write-Host "           brak zapasowego kandydata w rekonesansie - kafelek do usuniecia albo recznego doboru" -ForegroundColor Magenta
        }
    }
}

Write-Host ''
if ($problemy.Count -gt 0) {
    Write-Host ("BLOKADA: {0} produktow zablokuje publikacje ({1})." -f $problemy.Count, ($problemy -join ', ')) -ForegroundColor Red
    Write-Host "Napraw kafelek w pliku kolejki PRZED data publikacji wpisu." -ForegroundColor Red
    exit 1
} else {
    Write-Host "OK: wszystkie kafelki maja stan > 0 i sa aktywne." -ForegroundColor Green
    exit 0
}
