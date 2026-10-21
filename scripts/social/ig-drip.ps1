# =====================================================================================
#  ig-drip.ps1 - jeden przebieg dripu Instagrama MindSync (wolany przez Task Scheduler)
# -------------------------------------------------------------------------------------
#  1. ig-token.py check --auto-refresh-below 20 : token odswiezany z wyprzedzeniem;
#     exit 2 (< 10 dni / nieznana data) albo 1 (refresh padl) = OSTRZEZENIE w logu,
#     publikacja i tak rusza (token wciaz moze byc wazny).
#  2. ig-publish.py --due [--live] : max 1 post feed + 1 story, ktorych termin ET minal.
#
#  DOMYSLNIE DRY-RUN. Na zywo tylko z -Live (tak rejestruje zadanie register-drip-task.ps1
#  wywolany z -Live). Log: social/_drip-log.txt (wspolny z ig-publish.py).
# =====================================================================================
[CmdletBinding()]
param(
    [switch] $Live,
    [string] $Python = 'python'
)

$ErrorActionPreference = 'Continue'
$repoRoot = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$logPath  = Join-Path $repoRoot 'social\_drip-log.txt'
$tryb     = if ($Live) { 'LIVE' } else { 'DRY' }
$env:PYTHONIOENCODING = 'utf-8'

function Write-Line([string]$msg) {
    $line = "$(Get-Date -Format 'yyyy-MM-dd HH:mm:ss') | $tryb | id=- | media_id=- | $msg"
    try { Add-Content -Path $logPath -Value $line -Encoding utf8 } catch {}
    Write-Host $line
}

# --- 1. token ---
if ($Live) {
    & $Python (Join-Path $PSScriptRoot 'ig-token.py') check --warn-days 10 --auto-refresh-below 20
} else {
    & $Python (Join-Path $PSScriptRoot 'ig-token.py') check --warn-days 10
}
$tokRc = $LASTEXITCODE
if ($tokRc -eq 2) { Write-Line 'TOKEN UWAGA: wygasa za < 10 dni albo data nieznana (ig-token.py status)' }
elseif ($tokRc -ne 0) { Write-Line "TOKEN BLAD: ig-token.py check exit $tokRc (odswiezenie nieudane?)" }

# --- 2. publikacja ---
$pubArgs = @((Join-Path $PSScriptRoot 'ig-publish.py'), '--due')
if ($Live) { $pubArgs += '--live' }
& $Python @pubArgs
$pubRc = $LASTEXITCODE
if ($pubRc -ne 0 -and $pubRc -ne 3) { Write-Line "DRIP: ig-publish.py exit $pubRc" }
exit $pubRc
