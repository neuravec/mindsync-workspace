# =====================================================================================
#  render-banery.ps1 - render banerow HERO slidera strony glownej PLASMET (skin 16)
# -------------------------------------------------------------------------------------
#  CO ROBI:
#    Renderuje 6 plikow HTML (3 slajdy x desktop/mobile) z assets/banner/AI_creations/src/
#    do ostrych PNG przez Chrome headless (--headless --screenshot), a nastepnie konwertuje
#    do WebP (ImageMagick) z budzetem wagi. Tekst jest CZYSTYM HTML (Barlow) -> ostry, poprawny
#    polski, bez belkotu generatorow AI. Zdjecia produktow = realne URL z CDN Shoper.
#    WSZYSTKIE wytworzone banery laduja w assets/banner/AI_creations/ (jedno miejsce;
#    root assets/banner/ = referencyjne banery usera).
#
#  DLACZEGO TAK, A NIE GEMINI:
#    Banery niosa krytyczny tekst (naglowki, ceny "910,20 zl", CTA, badge). Modele
#    obrazowe psuja tekst i polskie znaki. Render HTML->PNG daje 1:1 z designem.
#
#  WYMAGANIA:
#    - Google Chrome / Edge (headless screenshot). Skrypt sam szuka chrome.exe/msedge.exe.
#    - ImageMagick (magick) do WebP. Bez niego zostaje sam PNG + ostrzezenie.
#    - Polaczenie z siecia (zdjecia produktow z CDN Shoper laduja sie przy renderze).
#
#  UZYCIE:
#    powershell -ExecutionPolicy Bypass -File .\render-banery.ps1            # render wszystkich 6 hero home
#    powershell -ExecutionPolicy Bypass -File .\render-banery.ps1 -Only hero-1-milwaukee-desktop
#
#  TRYB GENERYCZNY (-Html) — DOWOLNY baner HTML (np. banery innych marek, patrz
#  szablon/style-marek/): render pojedynczego pliku HTML w zadanym wymiarze.
#  Wymiar: -W/-H jawnie, albo automat z nazwy pliku (*mobile* => 1080x1350, inaczej 1920x680).
#  Wyjscie: obok pliku HTML (a gdy HTML lezy w folderze \src => folder wyzej), chyba ze -OutDir.
#  KONWENCJA: zrodla nowych banerow do assets/banner/AI_creations/src/ => webp wyladuje w AI_creations/.
#    powershell -ExecutionPolicy Bypass -File .\render-banery.ps1 -Html ..\..\assets\banner\AI_creations\src\promo-denbraven-desktop.html
# =====================================================================================
[CmdletBinding()]
param(
    [string] $Only      = $null,                          # render tylko jednego z listy hero home (nazwa bez .html)
    [string] $Html      = $null,                          # TRYB GENERYCZNY: sciezka do dowolnego banera .html
    [int]    $W         = 0,                              # szerokosc renderu (tylko z -Html; 0 = automat z nazwy)
    [int]    $H         = 0,                              # wysokosc renderu (tylko z -Html; 0 = automat z nazwy)
    [string] $OutDir    = $null,                          # katalog wyjsciowy (tylko z -Html; domyslnie automat)
    [int]    $WaitMs     = 2500,                           # czas na zaladowanie fontow+zdjec (Chrome --virtual-time-budget)
    [int]    $QualityWebp= 82
)
$ErrorActionPreference = 'Stop'

# UWAGA: wewnetrzna zmienna to $outRoot (NIE $outDir) — PowerShell jest case-insensitive,
# a $outDir nadpisalby parametr -OutDir trybu generycznego.
$srcDir  = Join-Path $PSScriptRoot '..\..\assets\banner\AI_creations\src'
$outRoot = Join-Path $PSScriptRoot '..\..\assets\banner\AI_creations'
$srcDir  = [IO.Path]::GetFullPath($srcDir)
$outRoot = [IO.Path]::GetFullPath($outRoot)

if ($Html) {
    # --- tryb generyczny: jeden dowolny plik HTML ---
    if (-not [IO.Path]::IsPathRooted($Html)) { $Html = Join-Path (Get-Location) $Html }
    $Html = [IO.Path]::GetFullPath($Html)
    if (-not (Test-Path $Html)) { throw "Plik HTML nie istnieje: $Html" }
    $name = [IO.Path]::GetFileNameWithoutExtension($Html)
    if ($W -le 0 -or $H -le 0) {
        if ($name -match 'mobile') { $W = 1080; $H = 1350 } else { $W = 1920; $H = 680 }   # standard banerow PLASMET
    }
    $srcDir = Split-Path $Html -Parent
    if ($OutDir) {
        if (-not [IO.Path]::IsPathRooted($OutDir)) { $OutDir = Join-Path (Get-Location) $OutDir }
        $outRoot = [IO.Path]::GetFullPath($OutDir)
        if (-not (Test-Path $outRoot)) { New-Item -ItemType Directory -Path $outRoot -Force | Out-Null }
    } else {
        $outRoot = if ((Split-Path $srcDir -Leaf) -eq 'src') { Split-Path $srcDir -Parent } else { $srcDir }
    }
    $jobs = @( @{ name=$name; w=$W; h=$H } )
} else {
    # --- tryb klasyczny: 6 banerow hero slidera home (skin 16) ---
    # slajd -> wymiar renderu (natywny wymiar pliku HTML)
    $jobs = @(
        @{ name='hero-1-milwaukee-desktop'; w=1920; h=680  }
        @{ name='hero-2-denbraven-desktop'; w=1920; h=680  }
        @{ name='hero-3-forge-desktop';     w=1920; h=680  }
        @{ name='hero-1-milwaukee-mobile';  w=1080; h=1350 }
        @{ name='hero-2-denbraven-mobile';  w=1080; h=1350 }
        @{ name='hero-3-forge-mobile';      w=1080; h=1350 }
    )
    if ($Only) { $jobs = $jobs | Where-Object { $_.name -eq $Only } }
    if (-not $jobs) { throw "Brak zadania '$Only'. Dostepne: hero-1/2/3-milwaukee/denbraven/forge -{desktop,mobile}" }
}

# --- znajdz Chrome/Edge ---
$chrome = $null
$cands = @(
    "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
    "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
    "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
    "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe",
    "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
)
foreach ($c in $cands) { if (Test-Path $c) { $chrome = $c; break } }
if (-not $chrome) { throw "Nie znaleziono Chrome ani Edge. Zainstaluj Chrome albo podaj sciezke recznie w skrypcie." }

# --- ImageMagick (PATH, a gdy sesja ma nieodswiezony PATH — typowa lokalizacja instalacji) ---
$magickCmd = Get-Command magick -ErrorAction SilentlyContinue
$magick = if ($magickCmd) { $magickCmd.Source } else { $null }
if (-not $magick) {
    $mm = Get-Item "$env:ProgramFiles\ImageMagick*\magick.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($mm) { $magick = $mm.FullName }
}

# --- PRE-FETCH zdjec produktow do src/img/ (tylko tryb klasyczny hero home; render offline-safe) ---
if (-not $Html) {
    $imgDir = Join-Path $srcDir 'img'
    if (-not (Test-Path $imgDir)) { New-Item -ItemType Directory -Path $imgDir -Force | Out-Null }
    $prodImgs = @(
        @{ url='https://sklep261208.shoparena.pl/userdata/public/gfx/8703/25351_16372.jpg'; file='milwaukee-fdd3-0.jpg' }
        @{ url='https://sklep261208.shoparena.pl/environment/cache/images/productGfx_13678_750_750/26703_24884.webp'; file='forge-m18-fb8.webp' }
    )
    foreach ($pi in $prodImgs) {
        $dest = Join-Path $imgDir $pi.file
        if (-not (Test-Path $dest)) {
            try { Invoke-WebRequest -Uri $pi.url -OutFile $dest -UseBasicParsing -TimeoutSec 30 } catch {
                Write-Host "  [!] nie pobrano $($pi.file) - HTML uzyje URL CDN przy renderze" -ForegroundColor Yellow
            }
        }
    }
}

Write-Host "render-banery.ps1" -ForegroundColor Cyan
Write-Host "  Chrome:      $chrome" -ForegroundColor Gray
Write-Host "  ImageMagick: $(if($magick){"OK ($magick)"}else{'BRAK - zostanie sam PNG'})" -ForegroundColor $(if($magick){'Gray'}else{'Yellow'})
Write-Host "  src:         $srcDir" -ForegroundColor Gray
Write-Host "  out:         $outRoot" -ForegroundColor Gray

foreach ($j in $jobs) {
    $html = Join-Path $srcDir "$($j.name).html"
    if (-not (Test-Path $html)) { Write-Host "  [pomijam] brak $html" -ForegroundColor Yellow; continue }
    $png  = Join-Path $outRoot "$($j.name).png"
    $webp = Join-Path $outRoot "$($j.name).webp"
    $url  = ([Uri]$html).AbsoluteUri

    Write-Host "`n  -> $($j.name)  ($($j.w)x$($j.h))" -ForegroundColor White
    # Chrome headless screenshot w dokladnym wymiarze, deterministycznie (virtual-time-budget czeka na fonty/zdjecia)
    $args = @(
        '--headless=new','--disable-gpu','--hide-scrollbars','--force-device-scale-factor=1',
        "--window-size=$($j.w),$($j.h)",
        "--screenshot=$png",
        "--virtual-time-budget=$WaitMs",
        '--default-background-color=00000000',
        $url
    )
    & $chrome @args | Out-Null
    if (-not (Test-Path $png)) { Write-Host "     [!] Chrome nie zapisal PNG (sprawdz dostep do CDN/zdjec)." -ForegroundColor Yellow; continue }
    $pngKb = [math]::Round((Get-Item $png).Length/1KB,1)
    Write-Host "     PNG: $pngKb KB" -ForegroundColor DarkGray

    if ($magick) {
        & $magick $png -strip -quality $QualityWebp $webp
        $webpKb = [math]::Round((Get-Item $webp).Length/1KB,1)
        $budget = 250   # baner full-width wg zalecenia Shoper 150-250 KB
        $flag = if ($webpKb -gt $budget) { "  [!] >$budget KB -> obniz q lub uprosc" } else { '' }
        $col  = if ($webpKb -gt $budget) { 'Yellow' } else { 'Green' }
        Write-Host "     WebP: $webpKb KB$flag" -ForegroundColor $col
        Remove-Item $png -Force   # PNG to tylko produkt posredni
    }
}

Write-Host "`nGOTOWE. Banery .webp w: $outRoot" -ForegroundColor Green
Write-Host "Nastepny krok: wgranie w panelu Shoper -> modul Slider (per slajd desktop+mobile). Specyfikacja: assets/banner/AI_creations/SPEC.md" -ForegroundColor DarkCyan
