# =====================================================================================
#  gemini-restyle.ps1 - image-to-image (restyle) przez Google Gemini API (Nano Banana Pro)
# -------------------------------------------------------------------------------------
#  CO ROBI:
#    Wysyla PROMPT + jeden lub wiele OBRAZOW WEJSCIOWYCH (referencja tresci/kompozycji,
#    wzorzec stylu, logotypy) do modelu obrazowego Gemini i zapisuje zwrocony obraz (PNG).
#    W odroznieniu od gemini-generate.ps1 (text->image) to tryb EDYCJI/RESTYLE (image->image),
#    ktory Nano Banana Pro obsluguje najlepiej - stad wierne logotypy i poprawny tekst.
#
#  SPEC API (v1beta generateContent):
#    POST https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent
#    Header: x-goog-api-key: <KLUCZ z scripts/image-gen/.env -> GEMINI_API_KEY>
#    Body: {"contents":[{"parts":[ {"text":"<prompt>"},
#             {"inlineData":{"mimeType":"image/jpeg","data":"<b64>"}}, ... ]}],
#           "generationConfig":{"responseModalities":["TEXT","IMAGE"],
#             "imageConfig":{"aspectRatio":"21:9","imageSize":"2K"}}}
#    Model domyslny: gemini-3-pro-image (Nano Banana Pro) - najlepszy do tekstu/brandingu.
#    Odpowiedz: obraz base64 w candidates[0].content.parts[].inlineData.data -> plik PNG.
#
#  [!] DOMYSLNIE -DryRun = TRUE (nic nie wysyla). Realna generacja: -DryRun:$false
#     (wymaga klucza; gemini-3-pro-image ~$0.12-0.24/obraz zaleznie od rozmiaru).
#
#  BEZPIECZENSTWO: klucz zyje TYLKO w .env; nigdy nie jest wypisywany (status [USTAWIONE]/[PUSTE]).
#
#  UZYCIE (banery: wynik ZAWSZE do assets/banner/AI_creations — jedno miejsce na wytworzone banery;
#  root assets/banner/ = referencyjne banery usera):
#    powershell -ExecutionPolicy Bypass -File .\gemini-restyle.ps1 `
#      -PromptFile ..\..\szablon\prompty-grafik\promo-akumulator-2zl-baner.md `
#      -RefImage "..\..\assets\banner\akumulator_za_2_zl_promocja 2.jpg",
#                "..\..\assets\banner\AI_creations\hero-3-forge-desktop.webp",
#                "..\..\assets\banner\AI_creations\src\img\plasmet.png" `
#      -OutDir ..\..\assets\banner\AI_creations -Slug promo-akumulator-2zl-gemini `
#      -AspectRatio 21:9 -Brand milwaukee -DryRun:$false
#
#  STYL MARKI (-Brand):
#    Kazdy baner ma miec styl KONKRETNEJ marki (albo 'ogolna' = styl sklepowy).
#    -Brand <slug> wczytuje palete z szablon/style-marek/style-marek.json i DOKLEJA
#    sekcje "BRAND STYLE" do promptu. Bez -Brand skrypt ostrzega (baner bez stylu
#    marki = blad procesu; lista slugow w ostrzezeniu).
# =====================================================================================
[CmdletBinding()]
param(
    [string]   $Prompt      = $null,
    [string]   $PromptFile  = $null,
    [string]   $Brand       = $null,                            # slug stylu marki z szablon/style-marek/style-marek.json
    [Parameter(Mandatory=$true)][string[]] $RefImage,           # >=1 obraz wejsciowy (kolejnosc wazna dla promptu)
    [Parameter(Mandatory=$true)][string]   $OutDir,
    [string]   $Slug        = 'restyle',
    [ValidateSet('','1:1','2:3','3:2','3:4','4:3','4:5','5:4','9:16','16:9','21:9')]
    [string]   $AspectRatio = '',                               # '' = nie wymuszaj (model idzie za referencja)
    [ValidateSet('1K','2K','4K')]
    [string]   $ImageSize   = '2K',
    [string]   $Model       = 'gemini-3-pro-image',
    [bool]     $DryRun      = $true,
    [int]      $TimeoutSec  = 180
)
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# --- prompt: -Prompt inline albo -PromptFile (pierwszy blok ``` z .md, inaczej caly plik) ---
function Get-PromptText {
    param([string]$Inline, [string]$File)
    if ($Inline) { return ($Inline -replace '\s+', ' ').Trim() }
    if (-not $File) { throw "Podaj -Prompt albo -PromptFile." }
    if (-not [IO.Path]::IsPathRooted($File)) { $File = Join-Path (Get-Location) $File }
    if (-not (Test-Path $File)) { throw "PromptFile nie istnieje: $File" }
    $md = Get-Content $File -Raw -Encoding utf8
    $m  = [regex]::Match($md, '(?s)```(.*?)```')
    $raw = if ($m.Success) { $m.Groups[1].Value } else { $md }
    return $raw.Trim()
}
$promptText = Get-PromptText -Inline $Prompt -File $PromptFile
if (-not $promptText) { throw "Pusty prompt." }

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
    $promptText += "`n`nBRAND STYLE - $($brandDef.nazwa) (PLASMET banner system, follow strictly):`n$($brandDef.promptStyle)"
} else {
    Write-Host "[!] Bez -Brand: prompt idzie BEZ stylu marki. Baner MUSI miec styl konkretnej marki" -ForegroundColor Yellow
    Write-Host "    (albo -Brand ogolna = styl sklepowy). Lista stylow: szablon/style-marek/style-marek.json" -ForegroundColor Yellow
}

# --- obrazy wejsciowe -> parts z inlineData (mime po rozszerzeniu) ---
function Get-Mime { param([string]$p)
    switch ([IO.Path]::GetExtension($p).ToLower()) {
        '.jpg'  { 'image/jpeg' } '.jpeg' { 'image/jpeg' }
        '.png'  { 'image/png' }  '.webp' { 'image/webp' }
        default { 'image/png' }
    }
}
$imgParts = @()
$imgReport = @()
foreach ($ref in $RefImage) {
    $rp = if ([IO.Path]::IsPathRooted($ref)) { $ref } else { Join-Path (Get-Location) $ref }
    if (-not (Test-Path $rp)) { throw "RefImage nie istnieje: $rp" }
    $bytes = [IO.File]::ReadAllBytes($rp)
    $b64   = [Convert]::ToBase64String($bytes)
    $mime  = Get-Mime $rp
    $imgParts += @{ inlineData = @{ mimeType = $mime; data = $b64 } }
    $imgReport += ("   - {0}  ({1}, {2} KB)" -f (Split-Path $rp -Leaf), $mime, [math]::Round($bytes.Length/1KB,1))
}

# --- OutDir + klucz ---
if (-not [IO.Path]::IsPathRooted($OutDir)) { $OutDir = Join-Path (Get-Location) $OutDir }
if (-not (Test-Path $OutDir)) { New-Item -ItemType Directory -Path $OutDir -Force | Out-Null }
$rawPng = Join-Path $OutDir "$Slug-raw.png"

$apiKey = $null
$envPath = Join-Path $PSScriptRoot '.env'
if (Test-Path $envPath) {
    Get-Content $envPath | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
        $parts = $_ -split '=', 2
        if ($parts[0].Trim() -eq 'GEMINI_API_KEY') { $apiKey = $parts[1].Trim().Trim('"') }
    }
}
$keyStatus = if ($apiKey) { '[USTAWIONE]' } else { '[PUSTE]' }

Write-Host "gemini-restyle.ps1 (image-to-image)" -ForegroundColor Cyan
Write-Host "  Model:        $Model" -ForegroundColor Gray
Write-Host "  Styl marki:   $(if($brandDef){ "$($brandDef.nazwa) (akcent $($brandDef.akcent))" } else { '(BRAK - bez -Brand)' })" -ForegroundColor $(if($brandDef){'Gray'}else{'Yellow'})
Write-Host "  AspectRatio:  $(if($AspectRatio){$AspectRatio}else{'(za referencja)'})   ImageSize: $ImageSize" -ForegroundColor Gray
Write-Host "  OutDir/Slug:  $OutDir  /  $Slug" -ForegroundColor Gray
Write-Host "  GEMINI_API_KEY: $keyStatus" -ForegroundColor Gray
Write-Host "  Obrazy wejsciowe ($($RefImage.Count)):" -ForegroundColor Gray
$imgReport | ForEach-Object { Write-Host $_ -ForegroundColor DarkGray }
Write-Host ("  Prompt: {0} zn." -f $promptText.Length) -ForegroundColor DarkGray

# --- Body builder ---
function New-Body {
    param([bool]$WithImageConfig)
    $parts = @( @{ text = $promptText } ) + $imgParts
    $gen = [ordered]@{ responseModalities = @('TEXT','IMAGE') }
    if ($WithImageConfig) {
        $ic = [ordered]@{ imageSize = $ImageSize }
        if ($AspectRatio) { $ic['aspectRatio'] = $AspectRatio }
        $gen['imageConfig'] = $ic
    }
    return [ordered]@{ contents = @( @{ parts = $parts } ); generationConfig = $gen }
}

if ($DryRun) {
    Write-Host "`n[DRY-RUN] NIE wolam Gemini. POST poszedlby na:" -ForegroundColor Magenta
    Write-Host "  https://generativelanguage.googleapis.com/v1beta/models/${Model}:generateContent" -ForegroundColor Magenta
    Write-Host "  parts: 1x text + $($imgParts.Count)x inlineData(obraz); imageConfig: imageSize=$ImageSize aspectRatio=$(if($AspectRatio){$AspectRatio}else{'brak'})" -ForegroundColor Magenta
    if (-not $apiKey) { Write-Host "  [!] Brak GEMINI_API_KEY w .env" -ForegroundColor Yellow }
    Write-Host "  Realna generacja: -DryRun:`$false" -ForegroundColor Magenta
    return
}
if (-not $apiKey) { throw "Brak GEMINI_API_KEY w scripts/image-gen/.env (status: [PUSTE])." }

function Invoke-Gemini {
    param([object]$BodyObj)
    $json  = $BodyObj | ConvertTo-Json -Depth 20 -Compress
    $bytes = [Text.Encoding]::UTF8.GetBytes($json)
    $ms    = $TimeoutSec * 1000
    $uri   = "https://generativelanguage.googleapis.com/v1beta/models/$Model" + ':generateContent'
    $req = [System.Net.HttpWebRequest]::Create($uri)
    $req.Method = 'POST'; $req.ContentType = 'application/json; charset=utf-8'; $req.Accept = 'application/json'
    $req.Headers['x-goog-api-key'] = $apiKey
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
            try { $req.Abort() } catch {}; return [pscustomobject]@{ ok=$false; code=$null; raw='HANG/TIMEOUT' }
        }
        $code = $null; $eb = $null
        try { $code = [int]$_.Exception.Response.StatusCode } catch {}
        try { $s = $_.Exception.Response.GetResponseStream(); $eb = (New-Object IO.StreamReader($s)).ReadToEnd() } catch {}
        return [pscustomobject]@{ ok=$false; code=$code; raw=$eb }
    } catch { return [pscustomobject]@{ ok=$false; code=$null; raw="EXC:$($_.Exception.Message)" } }
}

Write-Host "`n[LIVE] POST Gemini ($Model)..." -ForegroundColor Cyan
$r = Invoke-Gemini -BodyObj (New-Body -WithImageConfig $true)
if (-not $r.ok -and $r.code -eq 400 -and ("$($r.raw)" -match 'imageConfig|aspectRatio|imageSize|INVALID_ARGUMENT')) {
    Write-Host "  imageConfig nieobslugiwany -> ponawiam bez niego." -ForegroundColor Yellow
    $r = Invoke-Gemini -BodyObj (New-Body -WithImageConfig $false)
}
if (-not $r.ok) {
    $msg = if ("$($r.raw)" -match 'API key|API_KEY_INVALID|PERMISSION_DENIED') { ' (sprawdz GEMINI_API_KEY)' } else { '' }
    throw "Gemini POST nieudany: HTTP $($r.code)$msg :: $($r.raw)"
}

$obj = $r.raw | ConvertFrom-Json
$parts = $obj.candidates[0].content.parts
$imgPart = $parts | Where-Object {
    ($_.PSObject.Properties.Name -contains 'inlineData' -and $_.inlineData.data) -or
    ($_.PSObject.Properties.Name -contains 'inline_data' -and $_.inline_data.data)
} | Select-Object -First 1
if (-not $imgPart) {
    $textPart = ($parts | Where-Object { $_.text }) | Select-Object -First 1
    $hint = if ($textPart) { " Model zwrocil tekst: '$($textPart.text)'" } else { '' }
    throw "Odpowiedz Gemini bez obrazu.$hint Surowo: $($r.raw.Substring(0,[Math]::Min(500,$r.raw.Length)))"
}
$b64 = if ($imgPart.inlineData) { $imgPart.inlineData.data } else { $imgPart.inline_data.data }
[IO.File]::WriteAllBytes($rawPng, [Convert]::FromBase64String($b64))
$rawKb = [math]::Round((Get-Item $rawPng).Length / 1KB, 1)
Write-Host "  OK -> $rawPng (${rawKb}KB)" -ForegroundColor Green
Write-Host "`nGOTOWE. Podglad: $rawPng" -ForegroundColor Green
