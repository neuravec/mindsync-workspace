# =====================================================================================
#  gemini-generate.ps1 - generacja grafik HERO bloga przez Google Gemini API (Nano Banana)
# -------------------------------------------------------------------------------------
#  CO ROBI:
#    text -> image przez REST Gemini (generativelanguage.googleapis.com), dekoduje base64
#    z candidates[0].content.parts[].inlineData.data, zapisuje PNG, a nastepnie (jesli jest
#    ImageMagick) konwertuje/resize do WebP+JPG wg standardu grafik bloga
#    (blog/images/_standard-grafiki-bloga.md): 1600x900 desktop + 800x600 mobile, budzet wagi.
#
#  SPEC API (zweryfikowana wobec ai.google.dev/gemini-api/docs/image-generation 2026-06-10):
#    POST https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent
#    Auth: naglowek  x-goog-api-key: <KLUCZ>   (klucz z scripts/image-gen/.env -> GEMINI_API_KEY)
#    Body: {"contents":[{"parts":[{"text":"<prompt>"}]}],
#           "generationConfig":{"responseModalities":["TEXT","IMAGE"],
#             "responseFormat":{"image":{"aspectRatio":"16:9","imageSize":"2K"}}}}
#    Modele: gemini-2.5-flash-image (Nano Banana, tanszy, DOMYSLNY do wariantow),
#            gemini-3-pro-image (Nano Banana Pro, pod flagowe hero/banery; -Model).
#    Odpowiedz: obraz base64 (mime image/png) w inlineData.data -> dekoduj -> plik.
#    Jesli model nie wspiera responseFormat -> fallback bez tego pola (obraz i tak wraca).
#
#  [!] DOMYSLNIE -DryRun = TRUE: pokazuje co BY wyslal (model, ar, prompt, pliki wyjsciowe),
#     ale NIE wola Gemini i NIC nie zapisuje. Realna generacja: jawnie -DryRun:$false
#     (wymaga klucza w .env; kazde wywolanie kosztuje ~$0.02-0.04 za obraz na flash).
#
#  BEZPIECZENSTWO: klucz API zyje TYLKO w scripts/image-gen/.env (w .gitignore).
#     NIE jest wypisywany do konsoli/logow/plikow. Status klucza: tylko [USTAWIONE]/[PUSTE].
#
#  Uruchom (podglad/sucho): powershell -ExecutionPolicy Bypass -File .\gemini-generate.ps1 `
#                             -PromptFile ..\..\szablon\prompty-grafik\blog-01-hero-wiertarko-wkretarka.md `
#                             -OutDir ..\..\blog\images\01-jak-wybrac-wiertarko-wkretarke -Slug hero
#  Uruchom (LIVE, po kluczu): ...\gemini-generate.ps1 -PromptFile <md> -OutDir <dir> -Slug hero -DryRun:$false
# =====================================================================================

[CmdletBinding()]
param(
    [string] $Prompt      = $null,                       # tresc promptu inline
    [string] $PromptFile  = $null,                       # albo plik .md/.txt z promptem (np. z szablon/prompty-grafik/)
    [string] $Brand       = $null,                       # slug stylu marki (szablon/style-marek/style-marek.json) — dokleja BRAND STYLE do promptu
    [Parameter(Mandatory=$true)][string] $OutDir,        # katalog docelowy na grafiki (np. blog/images/<slug>/)
    [string] $Slug        = 'hero',                      # baza nazwy pliku: <Slug>-1600x900.webp itd. (zwykle 'hero')
    [ValidateSet('1:1','3:2','2:3','3:4','4:3','4:5','5:4','9:16','16:9','21:9')]
    [string] $AspectRatio = '16:9',                      # standard hero bloga = 16:9 (mobile crop robi magick)
    [string] $Model       = 'gemini-2.5-flash-image',    # tanszy default; flagowe: gemini-3-pro-image
    [ValidateSet('1K','2K','4K')]
    [string] $ImageSize   = '2K',                        # 2K wystarcza na 1600x900 z zapasem na crop mobile
    [bool]   $DryRun      = $true,                        # DOMYSLNIE: tylko podglad, ZERO wywolania API
    [switch] $Force,                                      # nadpisz istniejace pliki hero (idempotencja off)
    [int]    $TimeoutSec  = 120                           # twardy deadline na odpowiedz API (anty-'wiszacy zapis')
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# =====================================================================================
#  1. PROMPT — z -Prompt albo -PromptFile. Czyscimy dyrektywy CLI graphic-designera
#     ("/seo image-gen hero", "--ar 16:9", "--resolution 2K"), zostawiamy sam opis sceny.
# =====================================================================================
function Get-PromptText {
    param([string]$Inline, [string]$File)
    $raw = $null
    if ($Inline) {
        $raw = $Inline
    } elseif ($File) {
        if (-not [IO.Path]::IsPathRooted($File)) { $File = Join-Path (Get-Location) $File }
        if (-not (Test-Path $File)) { throw "PromptFile nie istnieje: $File" }
        $md = Get-Content $File -Raw -Encoding utf8
        # Z pliku .md graphic-designera bierzemy PIERWSZY blok ``` po naglowku "PROMPT" (desktop 16:9).
        $block = $null
        $m = [regex]::Match($md, '(?s)```(.*?)```')
        if ($m.Success) { $block = $m.Groups[1].Value }
        $raw = if ($block) { $block } else { $md }
    } else {
        throw "Podaj -Prompt (tekst) albo -PromptFile (sciezka do .md/.txt)."
    }
    # usun dyrektywy CLI/flagi, ktore NIE sa czescia opisu sceny dla modelu
    $lines = $raw -split "`r?`n"
    $clean = foreach ($ln in $lines) {
        $t = $ln
        $t = $t -replace '^\s*/seo\s+image-gen\s+\w+\s*', ''   # prefiks komendy CLI
        $t = $t -replace '\-\-ar\s+\S+', ''                     # --ar 16:9
        $t = $t -replace '\-\-resolution\s+\S+', ''             # --resolution 2K
        $t = $t -replace '\-\-\w+(\s+\S+)?', ''                 # inne flagi --xxx
        $t
    }
    $text = ($clean -join ' ') -replace '\s+', ' '
    return $text.Trim()
}

$promptText = Get-PromptText -Inline $Prompt -File $PromptFile
if (-not $promptText) { throw "Pusty prompt po oczyszczeniu — sprawdz -Prompt/-PromptFile." }

# --- styl marki: wstrzykniecie palety z szablon/style-marek/style-marek.json ---
$brandDef  = $null
$stylePath = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..\..\szablon\style-marek\style-marek.json'))
if ($Brand) {
    if (-not (Test-Path $stylePath)) { throw "Brak pliku stylow marek: $stylePath" }
    $styles = Get-Content $stylePath -Raw -Encoding utf8 | ConvertFrom-Json
    # UWAGA: nie uzywac nazwy $slug/$slugs — PowerShell jest case-insensitive i nadpisaloby to parametr $Slug
    $brandSlugs = @($styles.PSObject.Properties.Name | Where-Object { $_ -notlike '_*' })
    $brandSlug  = $Brand.ToLower()
    if ($brandSlugs -notcontains $brandSlug) { throw "Nieznany styl marki '$Brand'. Dostepne: $($brandSlugs -join ', ')" }
    $brandDef = $styles.$brandSlug
    $promptText += " BRAND STYLE - $($brandDef.nazwa) (PLASMET banner system, follow strictly): $($brandDef.promptStyle)"
}
$promptPreview = if ($promptText.Length -gt 220) { $promptText.Substring(0,220) + ' [...]' } else { $promptText }

# =====================================================================================
#  2. SCIEZKI WYJSCIOWE + idempotencja
# =====================================================================================
if (-not [IO.Path]::IsPathRooted($OutDir)) { $OutDir = Join-Path (Get-Location) $OutDir }
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }

$rawPng   = Join-Path $OutDir "$Slug-raw.png"
$desktopW = Join-Path $OutDir "$Slug-1600x900.webp"
$desktopJ = Join-Path $OutDir "$Slug-1600x900.jpg"
$mobileW  = Join-Path $OutDir "$Slug-800x600.webp"
$mobileJ  = Join-Path $OutDir "$Slug-800x600.jpg"
$finalTargets = @($desktopW, $desktopJ, $mobileW, $mobileJ)

$existing = @($finalTargets | Where-Object { Test-Path $_ })
if ($existing.Count -gt 0 -and -not $Force) {
    Write-Host "IDEMPOTENCJA: pliki hero dla '$Slug' juz istnieja w $OutDir :" -ForegroundColor Yellow
    $existing | ForEach-Object { Write-Host ("   - " + (Split-Path $_ -Leaf)) -ForegroundColor DarkGray }
    Write-Host "   -> NIE nadpisuje. Aby wymusic regeneracje: dodaj -Force." -ForegroundColor Yellow
    return
}

# =====================================================================================
#  3. KLUCZ API z .env (TYLKO status [USTAWIONE]/[PUSTE], nigdy wartosc)
# =====================================================================================
$apiKey = $null
$envPath = Join-Path $PSScriptRoot '.env'
if (Test-Path $envPath) {
    Get-Content $envPath | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
        $parts = $_ -split '=', 2
        if ($parts[0].Trim() -eq 'GEMINI_API_KEY') { $apiKey = $parts[1].Trim().Trim('"') }
    }
}
$keyStatus = if ($apiKey) { '[USTAWIONE]' } else { '[PUSTE]' }

# =====================================================================================
#  4. WYKRYCIE ImageMagick (nie zakladamy — sprawdzamy realnie)
# =====================================================================================
$magick = $null
$mc = Get-Command magick -ErrorAction SilentlyContinue
if ($mc) { $magick = $mc.Source }
if (-not $magick) {
    # sesje PowerShell miewaja nieodswiezony PATH po instalacji winget — sprawdz typowa lokalizacje
    $mm = Get-Item "$env:ProgramFiles\ImageMagick*\magick.exe" -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($mm) { $magick = $mm.FullName }
}

# --- raport startowy ---
Write-Host "gemini-generate.ps1" -ForegroundColor Cyan
Write-Host "  Model:       $Model" -ForegroundColor Gray
if ($brandDef) { Write-Host "  Styl marki:  $($brandDef.nazwa) (akcent $($brandDef.akcent))" -ForegroundColor Gray }
Write-Host "  AspectRatio: $AspectRatio   ImageSize: $ImageSize" -ForegroundColor Gray
Write-Host "  OutDir:      $OutDir" -ForegroundColor Gray
Write-Host "  Slug:        $Slug" -ForegroundColor Gray
Write-Host "  GEMINI_API_KEY: $keyStatus  (scripts/image-gen/.env)" -ForegroundColor Gray
Write-Host "  ImageMagick: $(if ($magick) { "OK ($magick)" } else { 'BRAK' })" -ForegroundColor $(if ($magick) { 'Gray' } else { 'Yellow' })
Write-Host "  Prompt:      $promptPreview" -ForegroundColor DarkGray

# =====================================================================================
#  5. POST-PROCESS: PNG -> WebP+JPG (1600x900 + 800x600). Wymaga ImageMagick.
#     Bez magick: zostaje surowy PNG + ostrzezenie jak doinstalowac.
# =====================================================================================
function Convert-Outputs {
    param([string]$SrcPng)
    if (-not $magick) {
        Write-Host "`n[!] ImageMagick (magick) NIEDOSTEPNY - pomijam konwersje do WebP/JPG i resize." -ForegroundColor Yellow
        Write-Host "    Zapisany tylko surowy render: $SrcPng" -ForegroundColor Yellow
        Write-Host "    Aby uzyskac WebP+JPG wg standardu (1600x900 + 800x600) doinstaluj ImageMagick:" -ForegroundColor Yellow
        Write-Host "      winget install ImageMagick.ImageMagick    (lub: choco install imagemagick)" -ForegroundColor DarkGray
        Write-Host "      po instalacji ponow z -Force, albo konwertuj recznie poleceniami ze standardu." -ForegroundColor DarkGray
        return
    }
    Write-Host "`n[magick] konwersja + resize wg standardu grafik bloga..." -ForegroundColor DarkCyan
    # desktop/tablet 1600x900 (16:9) — WebP q82 (cel <=150KB) + JPG q80 fallback
    & $magick $SrcPng -resize '1600x900^' -gravity center -extent 1600x900 -quality 82 $desktopW
    & $magick $SrcPng -resize '1600x900^' -gravity center -extent 1600x900 -quality 80 $desktopJ
    # mobile 800x600 (4:3) — kadr zacisniety na prawej-srodkowej czesci (dlon+wkret), art-direction crop
    & $magick $SrcPng -gravity East -resize '1200x900^' -extent 1200x900 -resize 800x600 -quality 82 $mobileW
    & $magick $SrcPng -gravity East -resize '1200x900^' -extent 1200x900 -resize 800x600 -quality 80 $mobileJ

    Write-Host "  Wygenerowane pliki + wagi (budzet: WebP desktop <=150KB, mobile <=90KB):" -ForegroundColor Green
    foreach ($f in $finalTargets) {
        if (Test-Path $f) {
            $kb = [math]::Round((Get-Item $f).Length / 1KB, 1)
            $budget = if ($f -like '*800x600*') { 90 } elseif ($f -like '*.webp') { 150 } else { 200 }
            $flag = if ($kb -gt $budget) { "  [!] ponad budzet ${budget}KB -> rozwaz q78/uproszczenie tla" } else { '' }
            $col  = if ($kb -gt $budget) { 'Yellow' } else { 'Green' }
            Write-Host ("   - " + (Split-Path $f -Leaf) + "  ${kb}KB$flag") -ForegroundColor $col
        }
    }
}

# =====================================================================================
#  6. DRY-RUN: nic nie wola, nic nie zapisuje
# =====================================================================================
if ($DryRun) {
    $endpoint  = "https://generativelanguage.googleapis.com/v1beta/models/$Model" + ':generateContent'
    $promptLen = $promptText.Length
    $outLeafs   = ($finalTargets | ForEach-Object { Split-Path $_ -Leaf }) -join ', '
    Write-Host "`n[DRY-RUN] NIE wolam Gemini i NIC nie zapisuje." -ForegroundColor Magenta
    Write-Host "  POST ktory BY poszedl:" -ForegroundColor Magenta
    Write-Host "    POST $endpoint" -ForegroundColor Magenta
    Write-Host "    Header: x-goog-api-key: <KLUCZ $keyStatus>" -ForegroundColor Magenta
    Write-Host "    Body  : contents[].parts[].text=<prompt $promptLen zn.>, " -ForegroundColor Magenta
    Write-Host "            generationConfig.responseModalities=[TEXT,IMAGE], responseFormat.image={aspectRatio:$AspectRatio, imageSize:$ImageSize}" -ForegroundColor Magenta
    Write-Host "  Po LIVE powstaloby: $rawPng -> (magick) $outLeafs" -ForegroundColor Magenta
    if (-not $apiKey) {
        Write-Host "`n  [!] Brak GEMINI_API_KEY w .env - przed -DryRun:`$false wpisz klucz do scripts/image-gen/.env" -ForegroundColor Yellow
    }
    if (-not $magick) {
        Write-Host "  [!] ImageMagick niedostepny - po LIVE powstanie tylko surowy PNG (bez WebP/JPG). Doinstaluj: winget install ImageMagick.ImageMagick" -ForegroundColor Yellow
    }
    Write-Host "`n  To byl DRY-RUN. Realna generacja: -DryRun:`$false (wymaga klucza; kosztuje ~`$0.02-0.04/obraz)." -ForegroundColor Magenta
    return
}

# =====================================================================================
#  7. LIVE — walidacja, wywolanie REST, dekodowanie base64, zapis PNG
# =====================================================================================
if (-not $apiKey) {
    throw "Brak GEMINI_API_KEY w scripts/image-gen/.env (status: [PUSTE]). Wpisz klucz i ponow. (DryRun pozostaje domyslnie bezpieczny.)"
}

# Body wg spec. responseFormat moze nie byc wspierany na czesci modeli -> fallback bez niego.
function New-Body {
    param([bool]$WithResponseFormat)
    $gen = [ordered]@{ responseModalities = @('TEXT','IMAGE') }
    if ($WithResponseFormat) {
        $gen['responseFormat'] = @{ image = @{ aspectRatio = $AspectRatio; imageSize = $ImageSize } }
    }
    return [ordered]@{
        contents         = @( @{ parts = @( @{ text = $promptText } ) } )
        generationConfig = $gen
    }
}

# Wzorzec anty-'wiszacy zapis': HttpWebRequest + Timeout/ReadWriteTimeout + KeepAlive=$false.
function Invoke-Gemini {
    param([object]$BodyObj)
    $json  = $BodyObj | ConvertTo-Json -Depth 12 -Compress
    $bytes = [Text.Encoding]::UTF8.GetBytes($json)
    $ms    = $TimeoutSec * 1000
    $uri   = "https://generativelanguage.googleapis.com/v1beta/models/$Model" + ':generateContent'
    $req = [System.Net.HttpWebRequest]::Create($uri)
    $req.Method = 'POST'
    $req.ContentType = 'application/json; charset=utf-8'
    $req.Accept = 'application/json'
    $req.Headers['x-goog-api-key'] = $apiKey      # klucz NIE jest logowany
    $req.Timeout = $ms; $req.ReadWriteTimeout = $ms; $req.KeepAlive = $false
    try {
        $rs = $req.GetRequestStream(); $rs.Write($bytes, 0, $bytes.Length); $rs.Close()
        $resp = $req.GetResponse()
        $sr = New-Object IO.StreamReader($resp.GetResponseStream())
        $body = $sr.ReadToEnd(); $sr.Close()
        $code = [int]$resp.StatusCode; $resp.Close()
        return [pscustomobject]@{ ok=$true; code=$code; raw=$body }
    } catch [System.Net.WebException] {
        if ($_.Exception.Status -eq [System.Net.WebExceptionStatus]::Timeout) {
            try { $req.Abort() } catch {}
            return [pscustomobject]@{ ok=$false; code=$null; raw='HANG/TIMEOUT' }
        }
        $code = $null; $eb = $null
        try { $code = [int]$_.Exception.Response.StatusCode } catch {}
        try { $s = $_.Exception.Response.GetResponseStream(); $eb = (New-Object IO.StreamReader($s)).ReadToEnd() } catch {}
        return [pscustomobject]@{ ok=$false; code=$code; raw=$eb }
    } catch {
        return [pscustomobject]@{ ok=$false; code=$null; raw="EXC:$($_.Exception.Message)" }
    }
}

Write-Host "`n[LIVE] POST Gemini ($Model, ar=$AspectRatio, $ImageSize)..." -ForegroundColor Cyan
$r = Invoke-Gemini -BodyObj (New-Body -WithResponseFormat $true)

# Fallback: jesli 400/INVALID_ARGUMENT na responseFormat -> ponow bez tego pola.
if (-not $r.ok -and $r.code -eq 400 -and ("$($r.raw)" -match 'responseFormat|response_format|aspectRatio|imageSize|INVALID_ARGUMENT')) {
    Write-Host "  responseFormat nieobslugiwany na tym modelu -> ponawiam BEZ niego (model i tak zwroci obraz)." -ForegroundColor Yellow
    $r = Invoke-Gemini -BodyObj (New-Body -WithResponseFormat $false)
}
if (-not $r.ok) {
    $msg = if ("$($r.raw)" -match 'API key|API_KEY_INVALID|PERMISSION_DENIED') { ' (sprawdz GEMINI_API_KEY w .env — klucz nieprawidlowy/bez dostepu)' } else { '' }
    throw "Gemini POST nieudany: HTTP $($r.code)$msg :: $($r.raw)"
}

# --- parsowanie odpowiedzi: base64 z inlineData.data ---
$obj = $r.raw | ConvertFrom-Json
$parts = $obj.candidates[0].content.parts
$imgPart = $parts | Where-Object {
    ($_.PSObject.Properties.Name -contains 'inlineData' -and $_.inlineData.data) -or
    ($_.PSObject.Properties.Name -contains 'inline_data' -and $_.inline_data.data)
} | Select-Object -First 1
if (-not $imgPart) {
    $textPart = ($parts | Where-Object { $_.text }) | Select-Object -First 1
    $hint = if ($textPart) { " Model zwrocil tylko tekst: '$($textPart.text)'" } else { '' }
    throw "Odpowiedz Gemini bez obrazu (brak inlineData.data).$hint Surowa odpowiedz: $($r.raw.Substring(0,[Math]::Min(400,$r.raw.Length)))"
}
$b64 = if ($imgPart.inlineData) { $imgPart.inlineData.data } else { $imgPart.inline_data.data }
[IO.File]::WriteAllBytes($rawPng, [Convert]::FromBase64String($b64))
$rawKb = [math]::Round((Get-Item $rawPng).Length / 1KB, 1)
Write-Host "  OK -> surowy render: $rawPng (${rawKb}KB)" -ForegroundColor Green

# --- post-process do WebP/JPG (lub ostrzezenie braku magick) ---
Convert-Outputs -SrcPng $rawPng

Write-Host "`nGOTOWE. Hero '$Slug' w: $OutDir" -ForegroundColor Green
if ($magick) {
    Write-Host "Nastepny krok (upload do Shoper): scripts/shoper-api/news-hero-upload.ps1 -NewsId <id> -ImagePath '$desktopW' -DryRun:`$false" -ForegroundColor DarkCyan
}
