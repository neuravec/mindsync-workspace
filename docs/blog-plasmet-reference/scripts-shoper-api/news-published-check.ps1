# =====================================================================================
#  news-published-check.ps1 — ROZEZNANIE (TYLKO GET): jakie wpisy news SA na zywo (active=1)
#  Zwraca mape seo_url -> news_id dla wszystkich wpisow. Sluzy regule ANTY-404 w opisach kategorii:
#  link do wpisu zostaje TYLKO gdy jego seo_url jest na tej liscie. ZERO zapisu.
# =====================================================================================
$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
$envPath = Join-Path $PSScriptRoot '.env'; $cfg=@{}
Get-Content $envPath | Where-Object { $_ -match '^\s*[^#].*=' } | ForEach-Object { $p=$_ -split '=',2; $cfg[$p[0].Trim()]=$p[1].Trim().Trim('"') }
$url = ($cfg['SHOPER_URL']).TrimEnd('/')
if ($cfg['SHOPER_TOKEN']) { $token=$cfg['SHOPER_TOKEN'] } else {
    $basic=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes("$($cfg['SHOPER_LOGIN']):$($cfg['SHOPER_PASSWORD'])"))
    $token=(Invoke-RestMethod -Method Post -Uri "$url/webapi/rest/auth" -Headers @{Authorization="Basic $basic"} -TimeoutSec 30).access_token
}
$hdr=@{Authorization="Bearer $token"}
$page=1; $pages=1; $all=@()
do {
    $r = Invoke-RestMethod -Method Get -Uri "$url/webapi/rest/news?limit=50&page=$page" -Headers $hdr -TimeoutSec 30
    if ($r.list) { $all += $r.list }
    $pages = if ($r.pages) { [int]$r.pages } else { 1 }
    $page++
} while ($page -le $pages)
Write-Host "WPISY news na zywo (count=$($all.Count)):" -ForegroundColor Cyan
$all | Sort-Object { [int]$_.news_id } | ForEach-Object {
    Write-Host ("  news_id={0,2}  active={1}  seo_url='{2}'" -f $_.news_id, $_.active, $_.seo_url)
}
