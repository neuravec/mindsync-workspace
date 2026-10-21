# product-cards.ps1 - kafelki produktowe do wpisow bloga PLASMET.
#
# Zamienia placeholdery w tresci wpisu na gotowy HTML kafelka produktu
# (zdjecie + nazwa + powod + CTA "Sprawdz w sklepie"), z danymi pobranymi
# NA ZYWO z webapi (nazwa, permalink, glowne zdjecie).
#
# Skladnia placeholderow w `tresc_html` (queue JSON):
#   [PRODUKT: <id|SKU> | <powod, 1 zdanie> | <kicker, opcjonalny>]
#   [PRODUKTY: <naglowek> || <id|SKU> | <powod> || <id|SKU> | <powod> || ... ]
#
# Tryby:
#   -Rank <fraza>          READ-ONLY: ranking kandydatow (stan + sprzedaz) do wyboru produktu
#   -InFile <plik.html>    render placeholderow z pliku HTML -> -OutFile
#   -QueueFile <plik.json> render placeholderow w polu tresc_html queue JSON -> -OutFile
#
# ZASADY (bramki twarde):
#   - BEZ CENY w kafelku (tresc wpisu to statyczny HTML - cena by zamarzla).
#   - Produkt musi byc aktywny; stan 0 -> ostrzezenie (domyslnie pomijany, chyba ze -AllowOutOfStock).
#   - URL zdjecia jest weryfikowany HTTP-em; brak zdjecia -> blad (kafelek bez zdjecia nie ma sensu).
param(
    [string]$Rank,
    [string]$InFile,
    [string]$QueueFile,
    [string]$OutFile,
    [string]$PublicHost = 'https://sklep.plasmet.pl',
    [switch]$AllowOutOfStock,
    [int]$ImageSize = 300
)
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# ---------- auth ----------
function Get-Ctx {
    $cfg=@{}
    Get-Content (Join-Path $PSScriptRoot '.env') | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object {
        $p=$_ -split '=',2; $cfg[$p[0].Trim()]=$p[1].Trim().Trim('"')
    }
    $u=($cfg['SHOPER_URL']).TrimEnd('/')
    if ($cfg['SHOPER_TOKEN']) { $t=$cfg['SHOPER_TOKEN'] } else {
        $basic=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($cfg['SHOPER_LOGIN']):$($cfg['SHOPER_PASSWORD'])"))
        $t=(Invoke-RestMethod -Method Post -Uri "$u/webapi/rest/auth" -Headers @{Authorization="Basic $basic"}).access_token
    }
    return @{ url=$u; hdr=@{Authorization="Bearer $t"} }
}

function Test-Http200([string]$u) {
    try {
        $req=[Net.HttpWebRequest]::Create($u); $req.Method='GET'; $req.Timeout=25000
        $req.ReadWriteTimeout=25000; $req.KeepAlive=$false
        $req.UserAgent='Mozilla/5.0 (compatible; PlasmetBot/1.0)'
        $resp=$req.GetResponse(); $resp.Close(); return $true
    } catch { return $false }
}

function HtmlEnc([string]$s) {
    if ($null -eq $s) { return '' }
    return ($s -replace '&','&amp;' -replace '<','&lt;' -replace '>','&gt;' -replace '"','&quot;')
}

# ---------- pobranie produktu ----------
function Get-ProductCard($ctx, [string]$key) {
    $key = $key.Trim()
    if ($key -match '^\d+$') {
        $p = Invoke-RestMethod -Method Get -Uri "$($ctx.url)/webapi/rest/products/$key" -Headers $ctx.hdr
    } else {
        $q = '{"code":"KEY"}'.Replace('KEY', $key)
        $f = [System.Uri]::EscapeDataString($q)
        $r = Invoke-RestMethod -Method Get -Uri "$($ctx.url)/webapi/rest/products?filters=$f&limit=2" -Headers $ctx.hdr
        if ([int]$r.count -lt 1) { throw "Nie znaleziono produktu o SKU '$key'." }
        $p = $r.list[0]
    }
    $tr = $p.translations.pl_PL
    if (-not $tr.permalink) { throw "Produkt $($p.product_id): brak permalinku (translations.pl_PL)." }
    $img = $p.main_image
    if (-not $img -or -not $img.unic_name) { throw "Produkt $($p.product_id) '$($tr.name)': brak glownego zdjecia (main_image)." }

    $base = "$PublicHost/environment/cache/images/productGfx_$($img.unic_name)_${ImageSize}_${ImageSize}/$($img.name)"
    $imgUrl = "$base.webp"
    if (-not (Test-Http200 $imgUrl)) {
        $imgUrl = "$base.$($img.extension)"
        if (-not (Test-Http200 $imgUrl)) { throw "Produkt $($p.product_id): URL zdjecia nie zwraca 200 ($base.*)." }
    }
    $stock = [int]$p.stock.stock
    if ($stock -le 0 -and -not $AllowOutOfStock) {
        throw "Produkt $($p.product_id) '$($tr.name)': stan 0 - nie wstawiam kafelka (uzyj -AllowOutOfStock, jesli swiadomie)."
    }
    if ($stock -le 0) { Write-Host ("  UWAGA: stan 0 dla " + $tr.name) -ForegroundColor Yellow }

    return [pscustomobject]@{
        product_id=$p.product_id; code=$p.code; name=$tr.name
        url=$tr.permalink; img=$imgUrl; stock=$stock
    }
}

# ---------- HTML kafelkow ----------
$CTA = [char]0x53 + 'prawd' + [char]0x017A + ' w sklepie'   # "Sprawdz w sklepie" z polskim 'z'

function New-CardInline($p, [string]$reason, [string]$kicker) {
    $name = HtmlEnc $p.name; $rs = HtmlEnc $reason; $kk = HtmlEnc $kicker
    $sb = New-Object Text.StringBuilder
    [void]$sb.Append('<a href="' + (HtmlEnc $p.url) + '" style="box-sizing:border-box;display:flex;flex-wrap:wrap;align-items:center;gap:18px;margin:28px 0;padding:16px 18px;border:1px solid #E3E6EA;border-left:4px solid #D6001C;border-radius:10px;background:#FAFBFC;text-decoration:none;color:#14171B;">')
    [void]$sb.Append('<img src="' + (HtmlEnc $p.img) + '" alt="' + $name + '" width="110" height="110" loading="lazy" style="width:110px;height:110px;object-fit:contain;flex:0 0 110px;background:#FFFFFF;border-radius:6px;">')
    [void]$sb.Append('<span style="display:block;flex:1 1 220px;min-width:0;">')
    if ($kicker) { [void]$sb.Append('<span style="display:block;font-size:.78em;letter-spacing:.08em;text-transform:uppercase;color:#D6001C;font-weight:700;">' + $kk + '</span>') }
    [void]$sb.Append('<span style="display:block;font-weight:700;font-size:1.06em;margin:2px 0 6px;">' + $name + '</span>')
    [void]$sb.Append('<span style="display:block;color:#5A626B;font-size:.94em;margin-bottom:12px;">' + $rs + '</span>')
    [void]$sb.Append('<span style="display:inline-block;background:#D6001C;color:#FFFFFF;padding:14px 20px;border-radius:5px;font-weight:600;font-size:.94em;line-height:1.2;">' + $CTA + '</span>')
    [void]$sb.Append('</span></a>')
    return $sb.ToString()
}

function New-CardGridItem($p, [string]$reason) {
    $name = HtmlEnc $p.name; $rs = HtmlEnc $reason
    $sb = New-Object Text.StringBuilder
    [void]$sb.Append('<a href="' + (HtmlEnc $p.url) + '" style="box-sizing:border-box;flex:1 1 200px;min-width:200px;display:flex;flex-direction:column;align-items:center;padding:18px 16px;border:1px solid #E3E6EA;border-radius:10px;background:#FAFBFC;text-decoration:none;color:#14171B;text-align:center;">')
    [void]$sb.Append('<img src="' + (HtmlEnc $p.img) + '" alt="' + $name + '" width="150" height="150" loading="lazy" style="width:100%;max-width:150px;height:150px;object-fit:contain;background:#FFFFFF;border-radius:6px;">')
    [void]$sb.Append('<span style="display:block;font-weight:700;margin:12px 0 6px;font-size:.98em;line-height:1.35;">' + $name + '</span>')
    [void]$sb.Append('<span style="display:block;color:#5A626B;font-size:.9em;margin-bottom:14px;line-height:1.45;">' + $rs + '</span>')
    [void]$sb.Append('<span style="display:inline-block;background:#D6001C;color:#FFFFFF;padding:14px 18px;border-radius:5px;font-weight:600;font-size:.9em;line-height:1.2;margin-top:auto;">' + $CTA + '</span>')
    [void]$sb.Append('</a>')
    return $sb.ToString()
}

function New-CardGrid([string]$heading, $items) {
    $sb = New-Object Text.StringBuilder
    if ($heading) { [void]$sb.Append('<h2>' + (HtmlEnc $heading) + '</h2>') }
    [void]$sb.Append('<div style="display:flex;flex-wrap:wrap;gap:14px;margin:24px 0 32px;">')
    foreach ($i in $items) { [void]$sb.Append($i) }
    [void]$sb.Append('</div>')
    return $sb.ToString()
}

# ---------- render ----------
function Convert-Placeholders($ctx, [string]$html) {
    $count = 0
    # [PRODUKTY: naglowek || key | powod || key | powod ]
    $html = [regex]::Replace($html, '\[PRODUKTY:(.+?)\]', {
        param($m)
        $parts = $m.Groups[1].Value -split '\|\|'
        $heading = $parts[0].Trim()
        $items = @()
        for ($i=1; $i -lt $parts.Count; $i++) {
            $seg = $parts[$i] -split '\|'
            $p = Get-ProductCard $ctx $seg[0]
            $reason = if ($seg.Count -gt 1) { $seg[1].Trim() } else { '' }
            Write-Host ("  [grid] " + $p.product_id + "  " + $p.name) -ForegroundColor Green
            $items += (New-CardGridItem $p $reason)
        }
        $script:count++
        return (New-CardGrid $heading $items)
    }, [Text.RegularExpressions.RegexOptions]::Singleline)

    # [PRODUKT: key | powod | kicker]
    $html = [regex]::Replace($html, '\[PRODUKT:(.+?)\]', {
        param($m)
        $seg = $m.Groups[1].Value -split '\|'
        $p = Get-ProductCard $ctx $seg[0]
        $reason = if ($seg.Count -gt 1) { $seg[1].Trim() } else { '' }
        $kicker = if ($seg.Count -gt 2) { $seg[2].Trim() } else { '' }
        Write-Host ("  [inline] " + $p.product_id + "  " + $p.name) -ForegroundColor Green
        $script:count++
        return (New-CardInline $p $reason $kicker)
    }, [Text.RegularExpressions.RegexOptions]::Singleline)

    return $html
}

# ---------- ranking kandydatow ----------
function Invoke-Rank($ctx, [string]$phrase) {
    $q = '{"translations.pl_PL.name":{"like":"%PHRASE%"}}'.Replace('PHRASE', $phrase)
    $f = [System.Uri]::EscapeDataString($q)
    $r = Invoke-RestMethod -Method Get -Uri "$($ctx.url)/webapi/rest/products?filters=$f&limit=50" -Headers $ctx.hdr

    # SYGNAL 1 (najmocniejszy): popyt z Google Search Console, per URL produktu.
    # Plik generuje: python scripts/gsc/product_pages.py  (wymaga waznego tokenu OAuth).
    $gscFile = Join-Path $PSScriptRoot '..\gsc\product_pages.json'
    $gscKlik = @{}; $gscWyswietl = @{}
    $maGsc = $false
    if (Test-Path $gscFile) {
        $maGsc = $true
        # UWAGA: jeden produkt bywa w GSC pod kilkoma URL-ami (przecinek zakodowany %2C
        # i niezakodowany) - trzeba SUMOWAC, nie nadpisywac.
        (Get-Content $gscFile -Raw -Encoding UTF8 | ConvertFrom-Json) | ForEach-Object {
            if ($_.product_id) {
                $k = [string]$_.product_id
                if (-not $gscKlik.ContainsKey($k))     { $gscKlik[$k] = 0 }
                if (-not $gscWyswietl.ContainsKey($k)) { $gscWyswietl[$k] = 0 }
                $gscKlik[$k]     += [int]$_.clicks
                $gscWyswietl[$k] += [int]$_.impressions
            }
        }
    }
    # SYGNAL 2: sprzedaz z order-products
    $salesFile = Join-Path $PSScriptRoot '_pcard-sales-agg.json'
    $sales = @{}
    if (Test-Path $salesFile) {
        (Get-Content $salesFile -Raw -Encoding UTF8 | ConvertFrom-Json) | ForEach-Object { $sales[[string]$_.product_id] = [int]$_.sztuk }
    }

    Write-Host ("kandydaci dla '" + $phrase + "': " + $r.count) -ForegroundColor Cyan
    if ($maGsc) { Write-Host "  sygnal GSC: TAK (klikniecia > wyswietlenia > sprzedaz > stan)" -ForegroundColor Green }
    else { Write-Host "  sygnal GSC: BRAK pliku ..\gsc\product_pages.json (sortuje po sprzedazy i stanie)" -ForegroundColor Yellow }

    $lista = $r.list | ForEach-Object {
        $prodId = [string]$_.product_id
        [pscustomobject]@{
            id=$_.product_id; stan=[int]$_.stock.stock
            klik=$(if ($gscKlik.ContainsKey($prodId)) { $gscKlik[$prodId] } else { 0 })
            wysw=$(if ($gscWyswietl.ContainsKey($prodId)) { $gscWyswietl[$prodId] } else { 0 })
            sprzedaz=$(if ($sales.ContainsKey($prodId)) { $sales[$prodId] } else { 0 })
            sku=$_.code; nazwa=$_.translations.pl_PL.name
        }
    }
    if ($maGsc) { $lista = $lista | Sort-Object klik, wysw, sprzedaz, stan -Descending }
    else        { $lista = $lista | Sort-Object sprzedaz, stan -Descending }
    $lista | Format-Table -AutoSize | Out-String -Width 200 | Write-Host
}

# ---------- main ----------
$ctx = Get-Ctx
if ($Rank) { Invoke-Rank $ctx $Rank; return }

if ($InFile) {
    $html = [IO.File]::ReadAllText($InFile, [Text.Encoding]::UTF8)
    $out  = Convert-Placeholders $ctx $html
    if (-not $OutFile) { $OutFile = $InFile + '.rendered.html' }
    [IO.File]::WriteAllText($OutFile, $out, (New-Object Text.UTF8Encoding($false)))
    Write-Host ("`nzapisano -> " + $OutFile) -ForegroundColor Cyan
    return
}

if ($QueueFile) {
    $json = Get-Content $QueueFile -Raw -Encoding UTF8 | ConvertFrom-Json
    $json.tresc_html = Convert-Placeholders $ctx $json.tresc_html
    if (-not $OutFile) { $OutFile = $QueueFile }
    ($json | ConvertTo-Json -Depth 12) | Out-File $OutFile -Encoding UTF8
    Write-Host ("`nzapisano -> " + $OutFile) -ForegroundColor Cyan
    return
}

Write-Host "Uzycie: -Rank <fraza> | -InFile <html> | -QueueFile <json>  [-OutFile ...] [-AllowOutOfStock]" -ForegroundColor Yellow
