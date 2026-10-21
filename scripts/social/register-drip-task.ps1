# =====================================================================================
#  register-drip-task.ps1 - rejestruje zadanie Task Schedulera "MindSync-IG-Drip"
# -------------------------------------------------------------------------------------
#  Co godzine od 13:00 do 03:00 czasu PL (15 uruchomien), czyli 07:00-21:00 ET przy
#  przesunieciu 6 h (z marginesem na tygodnie, gdy zmiana czasu w USA i UE wypada
#  w rozne niedziele i roznica spada do 5 h). Kazde uruchomienie: ig-drip.ps1, czyli
#  ig-token.py check (auto refresh < 20 dni) + ig-publish.py --due.
#
#  DOMYSLNIE NIC NIE REJESTRUJE: bez -Apply tylko wypisuje definicje zadania.
#  Uruchamia OPERATOR, nie agent:
#     powershell -ExecutionPolicy Bypass -File .\register-drip-task.ps1               # podglad
#     powershell -ExecutionPolicy Bypass -File .\register-drip-task.ps1 -Apply        # zadanie w trybie DRY
#     powershell -ExecutionPolicy Bypass -File .\register-drip-task.ps1 -Apply -Live  # publikacja na zywo
#  Usuniecie: Unregister-ScheduledTask -TaskName 'MindSync-IG-Drip'
#
#  Ustawienia skopiowane z "MindSync Blog Drip": uzytkownik interaktywny, poziom Limited,
#  StartWhenAvailable, IgnoreNew, limit 30 min. Roznica: zadanie startuje tez na baterii.
# =====================================================================================
[CmdletBinding()]
param(
    [switch] $Apply,
    [switch] $Live,
    [string] $TaskName = 'MindSync-IG-Drip',
    [string] $StartAt  = '13:00',
    [int]    $Hours    = 15,
    [string] $Python   = $null
)

$ErrorActionPreference = 'Stop'
$runner = Join-Path $PSScriptRoot 'ig-drip.ps1'
if (-not (Test-Path $runner)) { throw "Brak $runner" }
if (-not $Python) {
    $cmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $cmd) { throw 'Nie znaleziono python w PATH; podaj -Python <pelna sciezka>' }
    $Python = $cmd.Source   # pelna sciezka: Task Scheduler nie musi miec tego samego PATH
}

$liveArg = if ($Live) { ' -Live' } else { '' }
$arguments = "-NoProfile -NonInteractive -ExecutionPolicy Bypass -Command `"& '$runner' -Python '$Python'$liveArg`""

$action  = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument $arguments
$trigger = New-ScheduledTaskTrigger -Daily -At $StartAt
# Powtarzanie co 1 h przez ($Hours) h: 13:00 ... 03:00 dnia nastepnego.
$rep = New-ScheduledTaskTrigger -Once -At $StartAt -RepetitionInterval (New-TimeSpan -Hours 1) `
        -RepetitionDuration (New-TimeSpan -Hours $Hours)
$trigger.Repetition = $rep.Repetition
$settings = New-ScheduledTaskSettingsSet -StartWhenAvailable -MultipleInstances IgnoreNew `
        -ExecutionTimeLimit (New-TimeSpan -Minutes 30) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Limited

Write-Host "Zadanie : $TaskName" -ForegroundColor Cyan
Write-Host "Tryb    : $(if ($Live) { 'LIVE (publikacja na Instagram!)' } else { 'DRY (podglad, zero wysylki)' })"
Write-Host "Start   : codziennie $StartAt, co 1 h przez $Hours h"
Write-Host "Akcja   : powershell.exe $arguments"

if (-not $Apply) {
    Write-Host 'PODGLAD: nic nie zarejestrowano. Dodaj -Apply (i -Live dla publikacji na zywo).' -ForegroundColor Magenta
    exit 0
}

Register-ScheduledTask -TaskName $TaskName -Action $action -Trigger $trigger -Settings $settings `
    -Principal $principal -Description 'MindSync: drip Instagrama (scripts/social/ig-drip.ps1)' -Force | Out-Null
Write-Host "OK: zarejestrowano '$TaskName'." -ForegroundColor Green
