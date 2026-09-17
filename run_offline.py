"""오프라인(폐쇄망) 서버에서 reflex run을 실행하기 위한 래퍼.

OFFLINE_SETUP.md 절차(①~③)를 먼저 끝낸 뒤 이걸로 실행하세요:

    python run_offline.py
    (또는 그 서버의 파이썬 실행 명령에 맞게: py -3.11 run_offline.py / python3.11 run_offline.py)

매번 손으로 설정하던 PATH/환경변수(REFLEX_USE_NPM, NPM_CONFIG_* 등)를
여기서 한 번에 처리한 뒤 `python -m reflex run`을 실행합니다.
Windows/Linux 둘 다 이 파일 하나로 동작합니다 (OS는 자동 감지).

경로가 아래 기본값과 다르게 배치됐다면 CONFIG 부분만 고치면 됩니다.
"""

from __future__ import annotations

import os
import platform
import subprocess
import sys
from pathlib import Path

IS_WINDOWS = platform.system() == "Windows"

# --- 환경에 맞게 필요하면 수정 ---
if IS_WINDOWS:
    NODE_DIR = Path(r"C:\node22\node-v22.23.2-win-x64")  # frontend-offline\node\node-v22.23.2-win-x64.zip 압축 해제 위치
    BUN_DIR = Path(r"C:\bun")                             # frontend-offline\bun\bun-windows-x64.zip 압축 해제 위치
    NPM_CACHE_DIR = Path(r"C:\npm-cache\win-cache")        # frontend-offline\npm-cache-win.tar.gz 압축 해제 위치
else:
    NODE_DIR = Path.home() / "node22"                      # frontend-offline/node/node-v22.23.2-linux-x64.tar.xz 압축 해제 위치
    BUN_DIR = Path("/opt/bun")                              # frontend-offline/bun/bun-linux-x64.zip 압축 해제 위치
    NPM_CACHE_DIR = Path.home() / "linux-cache"             # frontend-offline/npm-cache-linux.tar.gz 압축 해제 위치
# ---------------------------------


def main() -> int:
    env = os.environ.copy()

    path_parts = []
    if NODE_DIR.exists():
        path_parts.append(str(NODE_DIR))
    else:
        print(f"[경고] {NODE_DIR} 가 없습니다. Node.js 22.23.2 오프라인 zip/tar.xz를 그 경로에 풀어두세요.")
    if BUN_DIR.exists():
        path_parts.append(str(BUN_DIR))
    else:
        print(f"[경고] {BUN_DIR} 가 없습니다. Bun 오프라인 zip을 그 경로에 풀어두세요.")

    if path_parts:
        env["PATH"] = os.pathsep.join([*path_parts, env.get("PATH", "")])

    env["REFLEX_USE_NPM"] = "1"
    env["NPM_CONFIG_OFFLINE"] = "true"
    env["NPM_CONFIG_AUDIT"] = "false"
    env["NPM_CONFIG_FUND"] = "false"
    env["NPM_CONFIG_CACHE"] = str(NPM_CACHE_DIR)

    def version_of(cmd: list[str]) -> str:
        try:
            return subprocess.run(
                cmd, env=env, capture_output=True, text=True, timeout=10
            ).stdout.strip()
        except Exception:
            return "(확인 불가)"

    node_exe = "node.exe" if IS_WINDOWS else "node"
    bun_exe = "bun.exe" if IS_WINDOWS else "bun"
    print(f"node: {version_of([node_exe, '-v'])}   bun: {version_of([str(BUN_DIR / bun_exe), '--version'])}")

    return subprocess.run(
        [sys.executable, "-m", "reflex", "run", *sys.argv[1:]], env=env
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
