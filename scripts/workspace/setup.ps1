# Setup wspolnego workspace MindSync dla nowej osoby (Windows, PowerShell 5.1+).
# Uruchom z katalogu workspace (sklonowanego repo neuravec/mindsync-workspace):
#   Set-ExecutionPolicy -Scope Process Bypass
#   & .\scripts\workspace\setup.ps1
# Skrypt jest idempotentny: niczego nie nadpisuje i niczego nie usuwa. Pliki, ktore juz
# istnieja, zostaja bez zmian. Opcja -Force nadpisuje tylko kopie agentow i skilli w ~/.claude.
param(
    [switch]$Force,
    [switch]$SkipPython
)
$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
Set-Location $Root
Write-Host "Workspace: $Root" -ForegroundColor Cyan

function Test-Cmd([string]$name) { return [bool](Get-Command $name -ErrorAction SilentlyContinue) }

# 1. Narzedzia
$tools = [ordered]@{ git = 'Git for Windows (z Git Bash): https://git-scm.com/download/win'; python = 'Python 3.12+: https://www.python.org/downloads/'; npx = 'Node.js LTS (dla MCP Heroku): https://nodejs.org/'; claude = 'Claude Code: https://claude.com/claude-code'; flutter = 'Flutter (tylko do pracy na froncie): https://docs.flutter.dev/get-started/install/windows' }
$missing = @()
foreach ($t in $tools.Keys) { if (Test-Cmd $t) { Write-Host "  [OK] $t" -ForegroundColor Green } else { Write-Host "  [BRAK] $t -> $($tools[$t])" -ForegroundColor Yellow; $missing += $t } }
if ($missing -contains 'git') { throw 'Bez gita nie da sie kontynuowac. Zainstaluj Git for Windows i uruchom skrypt ponownie.' }

# 2. Repozytoria kodu obok workspace (ten sam uklad folderow co u wspolnika)
$repos = @(
    @{ dir = 'MindSync';          url = 'https://github.com/neuravec/MindSync.git';          branch = 'main' },
    @{ dir = 'mindsync-frontend'; url = 'https://github.com/neuravec/mindsync-frontend.git'; branch = 'dev'  },
    @{ dir = 'social';            url = 'https://github.com/neuravec/mindsync-social.git';   branch = 'main' },
    @{ dir = 'therapist-deck';    url = 'https://github.com/neuravec/therapist-deck.git';    branch = 'main' },
    @{ dir = 'Mindsync-fleet';    url = 'https://github.com/neuravec/Mindsync-fleet.git';    branch = 'main' }
)
foreach ($r in $repos) {
    $p = Join-Path $Root $r.dir
    if (Test-Path (Join-Path $p '.git')) { Write-Host "  [OK] $($r.dir) juz jest" -ForegroundColor Green; continue }
    Write-Host "  klonuje $($r.url) -> $($r.dir) (galaz $($r.branch))..." -ForegroundColor Cyan
    git clone --branch $r.branch $r.url $p
    if ($LASTEXITCODE -ne 0) { Write-Host "  [BLAD] klonowanie $($r.dir) nieudane (brak dostepu do repo na GitHubie?)" -ForegroundColor Red }
}

# 3. Pliki z sekretami: puste kopie szablonow. Wartosci z menedzera hasel, nigdy z czatu ani gita.
$envPairs = @(
    @('.env.example', '.env'),
    @('scripts\webflow\.env.example', 'scripts\webflow\.env'),
    @('scripts\social\.env.example', 'scripts\social\.env'),
    @('scripts\image-gen\.env.example', 'scripts\image-gen\.env'),
    @('MindSync\.env.example', 'MindSync\.env')
)
$toFill = @()
foreach ($pair in $envPairs) {
    $src = Join-Path $Root $pair[0]; $dst = Join-Path $Root $pair[1]
    if (-not (Test-Path $src)) { continue }
    if (Test-Path $dst) { Write-Host "  [OK] $($pair[1]) istnieje" -ForegroundColor Green; continue }
    Copy-Item $src $dst
    $toFill += $pair[1]
    Write-Host "  [NOWY] $($pair[1]) utworzony z szablonu, uzupelnij wartosci" -ForegroundColor Yellow
}

# 4. Zaleznosci Pythona dla skryptow bloga, Instagrama i grafik
if (-not $SkipPython -and (Test-Cmd 'python')) {
    foreach ($req in @('social\requirements.txt', 'scripts\image-gen\requirements.txt')) {
        $rp = Join-Path $Root $req
        if (Test-Path $rp) { Write-Host "  pip install -r $req" -ForegroundColor Cyan; python -m pip install --user -q -r $rp }
    }
    python -m pip install --user -q pillow playwright requests
    python -m playwright install chromium
}

# 5. Agenci i skille z profilu Claude (SEO, therapist-deck) oraz globalne zasady pisania
$userClaude = Join-Path $env:USERPROFILE '.claude'
foreach ($kind in @('agents', 'skills')) {
    $src = Join-Path $Root "setup\claude-user\$kind"
    if (-not (Test-Path $src)) { continue }
    $dst = Join-Path $userClaude $kind
    New-Item -ItemType Directory -Force -Path $dst | Out-Null
    Get-ChildItem $src | ForEach-Object {
        $target = Join-Path $dst $_.Name
        if ((Test-Path $target) -and -not $Force) { return }
        Copy-Item $_.FullName $target -Recurse -Force
        Write-Host "  [OK] ~/.claude/$kind/$($_.Name)" -ForegroundColor Green
    }
}
$globalMd = Join-Path $userClaude 'CLAUDE.md'
$marker = '<!-- mindsync-workspace-global-rules -->'
$have = (Test-Path $globalMd) -and ((Get-Content $globalMd -Raw -Encoding UTF8) -match [regex]::Escape($marker))
if (-not $have) {
    $rules = Get-Content (Join-Path $Root 'setup\claude-user\CLAUDE.md') -Raw -Encoding UTF8
    Add-Content -Path $globalMd -Value "`n$marker`n$rules" -Encoding UTF8
    Write-Host '  [OK] globalne zasady pisania dopisane do ~/.claude/CLAUDE.md' -ForegroundColor Green
}

# 6. Pamiec Claude w repo: kazda osoba wskazuje ten sam folder claude-memory w swoim workspace
$local = Join-Path $Root '.claude\settings.local.json'
$memDir = (Join-Path $Root 'claude-memory') -replace '\\', '/'
if (Test-Path $local) { $cfg = Get-Content $local -Raw -Encoding UTF8 | ConvertFrom-Json } else { $cfg = New-Object PSObject }
if (-not ($cfg.PSObject.Properties.Name -contains 'autoMemoryDirectory')) {
    $cfg | Add-Member -NotePropertyName autoMemoryDirectory -NotePropertyValue $memDir
    ($cfg | ConvertTo-Json -Depth 10) | Out-File -FilePath $local -Encoding utf8
    Write-Host "  [OK] pamiec Claude -> $memDir" -ForegroundColor Green
}

Write-Host ''
Write-Host 'GOTOWE. Zostalo do zrobienia recznie (szczegoly: ONBOARDING.md):' -ForegroundColor Cyan
if ($toFill.Count -gt 0) { Write-Host "  1. Uzupelnij sekrety w: $($toFill -join ', ')" }
Write-Host '  2. Zmienna HEROKU_API_KEY (heroku auth:token), potem: setx HEROKU_API_KEY "<token>"'
Write-Host '  3. W Claude Code: /mcp i zaloguj Loops oraz ClickUp; zatwierdz pluginy firebase, posthog, chrome-devtools'
Write-Host '  4. Google Search Console: scripts\gsc\INSTRUKCJA-autoryzacja-mindsync.md (wlasny token.json)'
Write-Host '  5. NIE rejestruj dripow bloga ani Instagrama w Harmonogramie zadan: publikuje jedna maszyna.'
