# 오프라인(폐쇄망) 설치 가이드

인터넷이 차단된 내부망 서버에 이 프로젝트를 설치하기 위한 절차입니다. 필요한 오프라인 번들(`wheelhouse/`, `frontend-offline/`)은 이미 프로젝트 폴더 안에 준비되어 있으며, `.gitignore`에 의해 GitHub에는 올라가지 않습니다 — **USB/사내 파일 전송 등으로 프로젝트 폴더 전체를 함께 옮겨야** 아래 절차가 동작합니다.

전체 흐름: **① Python 패키지(wheelhouse) 설치 → ② Bun 실행 파일을 고정 경로에 배치 → ③ 프런트엔드 패키지(node_modules) + npm 오프라인 캐시 배치 → ④ Node.js/npm으로 실행**

## 사전 준비물 (이미 프로젝트 안에 포함됨)

```text
wheelhouse/
├── win/                          # Python cp311-win_amd64 wheel 72개
└── linux/                        # Python cp311-manylinux_x86_64 wheel 72개

frontend-offline/
├── bun/
│   ├── bun-windows-x64.zip                        # Bun 1.3.14 실행 파일 (Windows)
│   └── bun-linux-x64.zip                          # Bun 1.3.14 실행 파일 (Linux)
├── node/
│   ├── node-v22.23.2-win-x64.zip                  # Node.js 22.23.2 (Windows, Reflex 최소 요구 22.22.0 충족)
│   └── node-v22.23.2-linux-x64.tar.xz              # Node.js 22.23.2 (Linux)
├── node_modules-win-x64.tar.gz                    # Windows용 node_modules
├── node_modules-linux-x64.tar.gz                  # Linux용 node_modules (WSL Ubuntu 22.04에서 실제 실행 검증)
├── npm-cache-win.tar.gz                           # ★ npm 오프라인 캐시 (Windows) — 실제 크래시 재현 후 이걸로 해결 확인
├── npm-cache-linux.tar.gz                         # ★ npm 오프라인 캐시 (Linux)
├── reflex.install_frontend_packages.cached.win    # 설치 성공 캐시 마커 (있으면 더 빠르게 스킵되지만, 없어도 위 npm 캐시로 동작함)
├── reflex.install_frontend_packages.cached.linux  # 설치 성공 캐시 마커 (Linux)
├── package-lock.win.json / package-lock.linux.json  # npm이 실제로 생성한 lockfile
├── package.win.json / package.linux.json          # 참고용 — 실제 실행 후 각 OS가 기록한 package.json (배치 시 안 씀)
├── bun.lock / bunfig.toml                          # 두 OS 공통
```

대상 서버의 OS에 맞는 세트(`win` 또는 `linux`)를 사용합니다. **인터넷을 완전히 차단한 채로(`NPM_CONFIG_OFFLINE=true`) `reflex run`이 `App running at: http://localhost:3000/`까지 뜨는 걸 실제로 재현·검증했습니다** (Windows는 이 PC에서, Linux는 같은 PC의 WSL Ubuntu 22.04에서).

> **왜 마커만으로는 부족했나:** Reflex의 설치 성공 캐시(`reflex.install_frontend_packages.cached`)는 fingerprint 안에 "그 순간 감지된 npm 실행 파일의 절대경로"까지 포함합니다. npm은 Node.js를 어디에 설치했느냐에 따라 서버마다 경로가 달라질 수 있어서, 마커만 믿으면 서버가 바뀔 때마다 다시 깨질 수 있습니다. 그래서 **npm 자체의 로컬 패키지 캐시(`npm-cache-*.tar.gz`)를 통째로 제공**해서, 설사 캐시 마커가 안 맞아 `npm install`이 진짜로 실행되더라도 네트워크 없이 성공하도록 만들었습니다. 마커는 "맞으면 더 빠르게 스킵되는 보너스", npm 캐시가 "실제 안전망"입니다.

---

## ① Python 3.11 패키지 설치

대상 서버에 **Python 3.11**이 설치되어 있어야 합니다 (가상환경 권장).

```bash
python3.11 -m venv .venv
source .venv/bin/activate            # Windows: .venv\Scripts\activate
```

인터넷 없이 wheelhouse만으로 설치:

```bash
# Linux 서버
pip install --no-index --find-links=./wheelhouse/linux -r requirements.txt
```

```powershell
# Windows 서버
pip install --no-index --find-links=.\wheelhouse\win -r requirements.txt
```

- `--no-index`: PyPI 등 외부 인덱스를 아예 조회하지 않음
- `--find-links`: 지정한 로컬 폴더에서만 wheel을 찾아 설치

설치가 끝나면 확인:

```bash
python -m reflex --version
```

---

## ② Bun 실행 파일을 고정 경로에 배치

Reflex는 프런트엔드 빌드를 위해 **Bun**(Node.js 대체 런타임)이 필요합니다.

`rxconfig.py`는 Bun을 다음 **고정 경로**에서 찾도록 설정되어 있습니다 (해당 경로가 없으면 자동으로 시스템 `PATH`의 `bun`을 대신 씁니다 — 다른 개발자 PC에는 영향 없음):

- Windows: `C:\bun\bun.exe`
- Linux: `/opt/bun/bun`

이 경로를 **반드시 그대로** 맞춰서 배치해야 합니다 (④에서 설명하는 설치 캐시가 이 경로를 기준으로 계산되기 때문).

### Linux

```bash
mkdir -p /opt/bun
unzip -j frontend-offline/bun/bun-linux-x64.zip -d /opt/bun   # -j: 폴더 구조 없이 실행 파일만 풀기
chmod +x /opt/bun/bun
/opt/bun/bun --version   # 1.3.14 확인
```

### Windows

```powershell
mkdir C:\bun
Expand-Archive frontend-offline\bun\bun-windows-x64.zip -DestinationPath C:\temp-bun
Move-Item C:\temp-bun\bun-windows-x64\bun.exe C:\bun\bun.exe
C:\bun\bun.exe --version
```

최소 요구 버전은 **1.3.0**이며, `rxconfig.py`가 요구하는 실제 버전은 **1.3.14**입니다 (`frontend-offline/bun/`에 담긴 버전과 동일).

> 편의상 `bun`을 시스템 PATH에도 등록해두면 터미널에서 바로 `bun ...` 명령을 쓸 수 있지만, Reflex 자체는 `rxconfig.py`의 고정 경로만 봅니다.

**★ 중요:** ③의 설치 캐시가 유효하려면 이 고정 경로의 Bun **뿐 아니라 npm(Node.js에 내장)도 동시에 정상적으로 PATH에서 잡혀야** 합니다 (안 맞아도 npm 캐시 안전망이 있어서 결국 동작은 하지만, 아래 Node 버전 요구사항은 필수입니다).

### Node.js 버전 요구사항 (필수, 22.22.0 이상)

Reflex가 `REFLEX_USE_NPM=1`일 때 **Node 22.22.0 미만이면 아예 실행을 거부**합니다. 서버에 이미 다른 버전의 Node가 깔려있어도 **시스템 Node를 건드리지 않고, 이 프로젝트를 실행할 때만** 새 버전을 앞에 끼워 넣을 수 있습니다:

```powershell
# Windows — 압축만 풀어두면 됨 (설치 아님, 기존 Node와 별개로 존재)
Expand-Archive frontend-offline\node\node-v22.23.2-win-x64.zip -DestinationPath C:\node22
```

```bash
# Linux — 압축만 풀어두면 됨
mkdir -p ~/node22
tar -xf frontend-offline/node/node-v22.23.2-linux-x64.tar.xz -C ~/node22 --strip-components=1
```

이걸 실제로 PATH 맨 앞에 넣어서 기존 Node보다 먼저 잡히게 하는 건 ④의 실행 스크립트가 자동으로 해줍니다 — 손으로 매번 설정할 필요 없습니다.

---

## ③ 프런트엔드 패키지(node_modules) + npm 오프라인 캐시 배치

Reflex는 `reflex run`을 실행할 때마다 자체 프레임워크 패키지(react, sonner, radix-ui 등)를 `npm add`/`bun add`로 **매번 다시 검증**합니다. 이건 항상 레지스트리에 접속하려고 시도하는 동작이라, `node_modules`가 이미 채워져 있어도 인터넷이 없으면 실패합니다. 이 검증 자체를 완전히 생략시키는 "캐시 마커"가 있긴 하지만(아래 참고), **서버마다 npm 설치 위치가 달라지면 마커가 깨질 수 있어서**, 마커가 깨져도 무조건 성공하도록 **npm 자체의 로컬 캐시를 통째로 제공**합니다.

```bash
python -m reflex init          # .web/ 폴더 생성 (reflex.lock/에서 package.json·bun.lock 복원)

# Linux
tar -xzf frontend-offline/node_modules-linux-x64.tar.gz -C .web/
tar -xzf frontend-offline/npm-cache-linux.tar.gz -C ~/                 # ~/linux-cache 로 풀림
cp frontend-offline/reflex.install_frontend_packages.cached.linux .web/reflex.install_frontend_packages.cached
cp frontend-offline/package-lock.linux.json .web/package-lock.json

# Windows (PowerShell)
tar -xzf frontend-offline\node_modules-win-x64.tar.gz -C .web\
mkdir C:\npm-cache -ErrorAction SilentlyContinue
tar -xzf frontend-offline\npm-cache-win.tar.gz -C C:\npm-cache        # C:\npm-cache\win-cache 로 풀림
Copy-Item frontend-offline\reflex.install_frontend_packages.cached.win .web\reflex.install_frontend_packages.cached
Copy-Item frontend-offline\package-lock.win.json .web\package-lock.json
```

풀어놓은 뒤 확인:

```bash
ls .web/node_modules | wc -l                       # 135개 내외면 정상 (Windows는 PowerShell Get-ChildItem 기준 150대 나올 수 있음 — 정상)
ls .web/reflex.install_frontend_packages.cached    # 있어야 함
ls .web/package-lock.json                          # 있어야 함
```

> `bun install`을 다시 실행하면 인터넷이 없는 한 실패하니, `.web/`이 이미 만들어진 상태에서 **압축 해제/복사로만 채워 넣고 재실행하지 않는 것**이 핵심입니다.
>
> **캐시 마커 vs npm 캐시, 뭐가 뭔지**: 마커(`reflex.install_frontend_packages.cached`)는 "이 조건이면 검증 자체를 건너뛰어도 됨"이라는 Reflex 전용 스냅샷이라 fingerprint(설정값 · 패키지 목록 · **그 순간 감지된 bun/npm의 절대경로**)가 정확히 일치해야 동작합니다. `bun_path`는 ②에서 고정 경로로 맞췄지만, **npm 경로는 Node.js를 어디에 설치했느냐에 달려 있어서 서버마다 다를 수 있고, 그러면 마커가 무효화**됩니다. 이때 마커가 깨져서 `npm install`이 진짜로 실행되더라도, ④에서 배치한 **npm 캐시(`NPM_CONFIG_CACHE`)** 덕분에 네트워크 없이 성공합니다 — 즉 마커는 최적화, npm 캐시가 진짜 보험입니다.

---

## ④ 실행 (Bun으로 직접 실행하면 안 됨 — 래퍼 스크립트 사용)

`.web/node_modules/@react-router/dev`(react-router 8.3.0)를 **Bun으로 직접 실행하면 (Windows에서) 자체 재시작 로직 버그로 크래시**합니다 (`restartWithMergedOptions() ... This is likely a bug in @react-router/dev.`). Bun은 위 ③의 설치 캐시를 유효하게 만들기 위해서만 필요하고, **실제 프런트엔드 서버 실행은 npm(Node.js)으로 해야** 합니다.

매번 PATH·환경변수를 손으로 설정하지 않도록, 필요한 걸 전부 알아서 세팅해주는 래퍼 스크립트를 프로젝트 루트에 준비해뒀습니다 (`run-offline.ps1` / `run-offline.sh`). **이것만 실행하면 됩니다:**

```powershell
# Windows
.\run-offline.ps1
```

```bash
# Linux
chmod +x run-offline.sh   # 최초 1회
./run-offline.sh
```

이 스크립트가 하는 일:
- Node 22.23.2(②에서 압축 해제한 `C:\node22` / `~/node22`)와 Bun을 이번 실행에만 PATH 맨 앞에 끼워 넣음 (시스템 PATH·다른 프로그램은 그대로)
- `REFLEX_USE_NPM=1`, `NPM_CONFIG_OFFLINE=true`, `NPM_CONFIG_AUDIT=false`, `NPM_CONFIG_FUND=false`, `NPM_CONFIG_CACHE=<③에서 푼 npm 캐시 경로>` 설정
- 마지막에 `python -m reflex run` 실행 (인자를 그대로 넘기므로 `.\run-offline.ps1 --loglevel debug`처럼 옵션 추가 가능)

스크립트 맨 위 변수(`$PythonCmd`, `$NodeDir`, `$BunDir`, `$NpmCacheDir` / `PYTHON_CMD`, `BUN_DIR`, `NPM_CACHE_DIR`)가 실제로 압축을 푼 경로와 다르면 그 부분만 고쳐서 쓰면 됩니다.

- 프론트엔드: `http://<서버IP>:3000`
- 백엔드: `http://<서버IP>:8000`

---

## 문제 해결

| 증상 | 원인 / 해결 |
| --- | --- |
| `pip install` 중 `FileNotFoundError` (경로 없음) | Windows 260자 경로(MAX_PATH) 제한. wheelhouse 폴더를 `C:\wh` 처럼 짧은 경로로 옮겨서 설치 |
| `bun: command not found` | ②에서 PATH 등록이 안 됨. `which bun` / `where bun`으로 확인 |
| `reflex run` 시 npm 패키지 관련 에러 | `.web/node_modules`가 비어 있거나 잘못된 OS용 tar를 풀었을 가능성. `rm -rf .web`후 ①②③ 재실행 |
| Bun 버전 경고 (`bun_version < MIN_VERSION`) | Bun 1.3.0 미만. `bun --version`으로 확인 후 ②의 zip을 다시 풀기 |
| `ModuleNotFoundError: No module named 'reflex_xy'` | `requirements.txt`의 `xy[reflex]`가 wheelhouse에서 설치되지 않음. `pip list`로 `xy` 패키지 설치 여부 확인 |
| `Connection Refused downloading package manifest <패키지명>` (예: sonner) | ③(설치 캐시 마커)가 없거나 fingerprint가 안 맞는 상태. `.web/reflex.install_frontend_packages.cached`를 `frontend-offline/`에서 복사했는지, ②의 Bun 고정 경로가 실제로 존재하는지 확인 |
| `npm error Exit handler never called!` / `npm silly audit report null` | npm이 설치 후 자동 취약점 감사(audit)를 하려다 네트워크가 없어서 npm 자체 버그로 죽음. ④의 `NPM_CONFIG_AUDIT=false`, `NPM_CONFIG_OFFLINE=true` 설정 |
| `npm error code ENOTCACHED` / `cache mode is 'only-if-cached' but no cached response is available` | 캐시 마커 fingerprint가 이 서버와 안 맞아서 `npm install`이 진짜로 실행됨. `NPM_CONFIG_CACHE`가 ③에서 실제로 압축을 푼 경로(`C:\npm-cache\win-cache` / `~/linux-cache`)를 정확히 가리키는지 확인 — `npm config get cache`로 실제 적용된 값을 볼 수 있음. 경로가 맞는데도 계속 나면 `frontend-offline/package.win.json`(또는 `.linux.json`)의 dependencies/devDependencies 중 npm 캐시에 없는 패키지가 있다는 뜻이니 알려주세요 |
| Windows에서 `OSError: [WinError 1314] 클라이언트가 필요한 권한을 가지고 있지 않습니다` (symlink 관련) | Windows가 심볼릭 링크 생성 권한을 요구함. 설정 → 개발자 모드를 켜거나, 관리자 권한으로 터미널을 실행 |
| `error: restartWithMergedOptions() was called, but the process has already been restarted. This is likely a bug in @react-router/dev.` | Bun으로 프런트엔드를 직접 실행해서 생기는 버그. ④처럼 `REFLEX_USE_NPM=1`을 설정하고 Node.js(22+)로 실행할 것 |
| `Your version (20.x) of Node.js is out of date. Upgrade to 22.22.0 or higher.` (경고만, 계속 진행됨) | 오래된 Node 경고. `Reflex requires...` 에러와 달리 즉시 죽지는 않지만 결국 아래 항목처럼 실패하니 미리 업그레이드 권장 |
| `Reflex requires node version 22.22.0 or higher to run, but the detected version is X.X.X` 뜨고 조용히 종료됨(멈춘 것처럼 보임) | `REFLEX_USE_NPM=1`일 때 Node 22.22.0 미만이면 하드 실패(`SystemExit(1)`) — 화면이 안 멈춘 거고 그냥 끝난 것. `run-offline.ps1`/`run-offline.sh`를 쓰면 ②에서 받은 Node 22.23.2가 자동으로 먼저 잡혀서 해결됨 |
| PowerShell `(Get-ChildItem .web/node_modules).Count`가 bash `ls \| wc -l`보다 훨씬 큼 | 정상 — PowerShell은 점(`.`)으로 시작하는 폴더(`.bin` 등)도 세지만 bash `ls`는 기본적으로 숨김. 실제 내용물 문제 아님 |

## 참고

- 이 wheelhouse/frontend-offline은 **Python 3.11 / reflex 0.9.10.post2 / Bun 1.3.14** 기준으로 만들어졌습니다. `requirements.txt`의 버전을 올리면 (특히 `package.json`의 dependencies가 바뀌면) `npm-cache-*.tar.gz`를 포함해 전체 번들을 다시 만들어야 합니다.
- 설치(패키지 검증)는 Bun이 하고, 실행은 npm/Node.js가 하는 **혼합 구조**입니다 — 둘 다 필요합니다. Bun만 있고 Node.js 22가 없다면 ④가 안 됩니다.
- 이 전체 오프라인 방식은 **완전 차단된 네트워크 환경에서 실제로 재현·검증**했습니다 (`NPM_CONFIG_OFFLINE=true`로 등록된 레지스트리 접속을 강제 차단한 뒤 `App running`까지 확인).
- 앱 자체의 미구현 부분(DB 연결, Parser 연동 등)은 [TODO.md](TODO.md)를 참고하세요.
