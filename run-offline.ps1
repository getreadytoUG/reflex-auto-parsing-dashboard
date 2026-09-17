<#
오프라인(폐쇄망) Windows 서버에서 reflex run을 실행하기 위한 래퍼 스크립트.
OFFLINE_SETUP.md 절차(①~③)를 먼저 끝낸 뒤 이 스크립트로 실행하세요:

    .\run-offline.ps1

매번 손으로 설정하던 PATH/환경변수를 여기서 한 번에 처리합니다.
경로가 문서와 다르게 배치됐다면 아래 변수만 수정하면 됩니다.
#>

$ErrorActionPreference = "Stop"

# --- 환경에 맞게 필요하면 수정 ---
$PythonCmd   = "py"
$PythonArgs  = @("-3.11")
$NodeDir     = "C:\node22\node-v22.23.2-win-x64"   # frontend-offline\node\node-v22.23.2-win-x64.zip 압축 해제 위치
$BunDir      = "C:\bun"                             # frontend-offline\bun\bun-windows-x64.zip 압축 해제 위치
$NpmCacheDir = "C:\npm-cache\win-cache"              # frontend-offline\npm-cache-win.tar.gz 압축 해제 위치
# ---------------------------------

if (Test-Path $NodeDir) {
    $env:PATH = "$NodeDir;$BunDir;" + $env:PATH
} else {
    Write-Warning "$NodeDir 가 없습니다. frontend-offline\node\node-v22.23.2-win-x64.zip 을 그 경로에 풀어두세요."
}

$env:REFLEX_USE_NPM     = "1"
$env:NPM_CONFIG_OFFLINE = "true"
$env:NPM_CONFIG_AUDIT   = "false"
$env:NPM_CONFIG_FUND    = "false"
$env:NPM_CONFIG_CACHE   = $NpmCacheDir

Write-Host "node: $(node -v 2>$null)   npm: $(npm -v 2>$null)   bun: $(& "$BunDir\bun.exe" --version 2>$null)"

& $PythonCmd @PythonArgs -m reflex run @args
