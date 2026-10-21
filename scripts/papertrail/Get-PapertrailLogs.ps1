<#
.SYNOPSIS
  Pobiera logi z Papertrail (classic HTTP API) BEZ ujawniania tokena.

.DESCRIPTION
  Token jest czytany z pliku .env dopiero w trakcie dzialania i nigdy nie jest
  wypisywany na ekran. Skrypt sam wykrywa nazwe klucza tokena (domyslnie probuje
  PAPERTRAIL_API_TOKEN, SOLARWINDS_TOKEN, PAPERTRAIL_TOKEN) lub uzyj -TokenKey.

.PARAMETER Query
  Fraza do wyszukania (Papertrail search), np. "error", "500", "traceback".

.PARAMETER Since
  Okno czasowe wstecz: np. 30m, 2h, 1d, 90s. Domyslnie 1h.

.PARAMETER Limit
  Maks. liczba zdarzen (1-1000). Domyslnie 200.

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File Get-PapertrailLogs.ps1 -Since 2h

.EXAMPLE
  powershell -NoProfile -ExecutionPolicy Bypass -File Get-PapertrailLogs.ps1 -Query "error" -Since 24h -Limit 500
#>
[CmdletBinding()]
param(
  [string]$Query = "",
  [string]$Since = "1h",
  [int]$Limit = 200,
  [string]$TokenKey = "",
  [string]$EnvFile = "",
  [switch]$Raw
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

# --- ustal sciezke do .env (odpornie na pusty $PSScriptRoot) ---
if (-not $EnvFile) {
  $root = $PSScriptRoot
  if (-not $root) { $root = Split-Path -Parent $MyInvocation.MyCommand.Definition }
  $EnvFile = [System.IO.Path]::GetFullPath((Join-Path $root '..\..\.env'))
} else {
  $EnvFile = [System.IO.Path]::GetFullPath($EnvFile)
}

function Get-DotEnvValue {
  param([string]$Path, [string[]]$Keys)
  if (-not (Test-Path -LiteralPath $Path)) { throw ".env nie znaleziony: $Path" }
  $lines = Get-Content -LiteralPath $Path
  foreach ($key in $Keys) {
    foreach ($line in $lines) {
      if ($line -match ('^\s*(export\s+)?' + [regex]::Escape($key) + '\s*[:=](.*)$')) {
        $v = $Matches[2].Trim()
        if ($v.Length -ge 2 -and (($v[0] -eq '"' -and $v[-1] -eq '"') -or ($v[0] -eq "'" -and $v[-1] -eq "'"))) {
          $v = $v.Substring(1, $v.Length - 2)
        }
        if ($v) { return @{ Key = $key; Value = $v } }
      }
    }
  }
  return $null
}

# --- token (wartosc NIGDY nie jest wypisywana) ---
$candidates = if ($TokenKey) { @($TokenKey) } else { @('PAPERTRAIL_API_TOKEN','SOLARWINDS_TOKEN','PAPERTRAIL_TOKEN') }
$found = Get-DotEnvValue -Path $EnvFile -Keys $candidates
if (-not $found) { throw "Nie znaleziono tokena w $EnvFile (szukane klucze: $($candidates -join ', '))" }
$token = $found.Value

# --- okno czasowe -> min_time (epoch sekundy, UTC) ---
if ($Since -match '^\s*(\d+)\s*([smhd])\s*$') {
  $n = [int]$Matches[1]; $u = $Matches[2]
  $delta = switch ($u) {
    's' { [TimeSpan]::FromSeconds($n) }
    'm' { [TimeSpan]::FromMinutes($n) }
    'h' { [TimeSpan]::FromHours($n) }
    'd' { [TimeSpan]::FromDays($n) }
  }
} else { throw "Nieprawidlowy -Since '$Since' (uzyj np. 30m, 2h, 1d)" }
$minTime = [int][Math]::Floor(((Get-Date).ToUniversalTime() - $delta - [datetime]'1970-01-01').TotalSeconds)

if ($Limit -gt 1000) { $Limit = 1000 }
if ($Limit -lt 1)    { $Limit = 1 }

Add-Type -AssemblyName System.Web | Out-Null
$qs = "limit=$Limit&min_time=$minTime"
if ($Query) { $qs += "&q=" + [System.Web.HttpUtility]::UrlEncode($Query) }
$uri = "https://papertrailapp.com/api/v1/events/search.json?$qs"
$headers = @{ 'X-Papertrail-Token' = $token }

try {
  $resp = Invoke-RestMethod -Uri $uri -Headers $headers -Method Get
} catch {
  $code = $null
  try { $code = [int]$_.Exception.Response.StatusCode } catch {}
  if ($code -eq 401 -or $code -eq 403) {
    throw "Papertrail odrzucil token (HTTP $code). Potrzebny jest 'API token' z Papertrail -> Settings -> Profile (naglowek X-Papertrail-Token) -- nie token syslog/drain ani token SolarWinds Observability."
  } elseif ($code) {
    throw "Papertrail API blad HTTP $code."
  } else {
    throw "Blad polaczenia z Papertrail API: $($_.Exception.Message)"
  }
}

$events = @($resp.events)
if ($Raw) {
  foreach ($e in $events) { $e | ConvertTo-Json -Compress }
} else {
  foreach ($e in $events) {
    "{0}  [{1}/{2}]  {3}" -f $e.display_received_at, $e.source_name, $e.program, $e.message
  }
}

$hitLimit = $false
try { $hitLimit = [bool]$resp.reached_record_limit } catch {}
""
"--- {0} zdarzen | okno: ostatnie {1} | q: '{2}' | klucz tokena: {3} ---" -f $events.Count, $Since, $Query, $found.Key
if ($hitLimit) { "UWAGA: osiagnieto limit rekordow ($Limit) - zawez -Since albo dodaj -Query, zeby nie gubic danych." }
