#!/bin/bash
# 오프라인(폐쇄망) Linux 서버에서 reflex run을 실행하기 위한 래퍼 스크립트.
# OFFLINE_SETUP.md 절차(①~③)를 먼저 끝낸 뒤 이 스크립트로 실행하세요:
#
#     ./run-offline.sh
#
# 매번 손으로 설정하던 환경변수를 여기서 한 번에 처리합니다.
# 경로가 문서와 다르게 배치됐다면 아래 변수만 수정하면 됩니다.
set -e

# --- 환경에 맞게 필요하면 수정 ---
PYTHON_CMD="python3.11"
BUN_DIR="/opt/bun"                       # frontend-offline/bun/bun-linux-x64.zip 압축 해제 위치
NPM_CACHE_DIR="$HOME/linux-cache"        # frontend-offline/npm-cache-linux.tar.gz 압축 해제 위치
# ---------------------------------

export PATH="$BUN_DIR:$PATH"
export REFLEX_USE_NPM=1
export NPM_CONFIG_OFFLINE=true
export NPM_CONFIG_AUDIT=false
export NPM_CONFIG_FUND=false
export NPM_CONFIG_CACHE="$NPM_CACHE_DIR"

echo "node: $(node -v 2>/dev/null)   npm: $(npm -v 2>/dev/null)   bun: $("$BUN_DIR/bun" --version 2>/dev/null)"

exec "$PYTHON_CMD" -m reflex run "$@"
