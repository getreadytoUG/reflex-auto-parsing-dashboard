# 오프라인(폐쇄망) 설치 가이드

인터넷이 차단된 내부망 서버에 이 프로젝트를 설치하기 위한 절차입니다. 필요한 오프라인 번들(`wheelhouse/`, `frontend-offline/`)은 이미 프로젝트 폴더 안에 준비되어 있으며, `.gitignore`에 의해 GitHub에는 올라가지 않습니다 — **USB/사내 파일 전송 등으로 프로젝트 폴더 전체를 함께 옮겨야** 아래 절차가 동작합니다.

전체 흐름: **① Python 패키지(wheelhouse) 설치 → ② Bun 실행 파일을 고정 경로에 배치 → ③ 프런트엔드 패키지(node_modules) + 설치 캐시 마커 배치 → ④ Node.js/npm으로 실행**

## 사전 준비물 (이미 프로젝트 안에 포함됨)

```text
wheelhouse/
├── win/                          # Python cp311-win_amd64 wheel 72개
└── linux/                        # Python cp311-manylinux_x86_64 wheel 72개

frontend-offline/
├── bun/
│   ├── bun-windows-x64.zip                        # Bun 1.3.14 실행 파일 (Windows)
│   └── bun-linux-x64.zip                          # Bun 1.3.14 실행 파일 (Linux)
├── node_modules-win-x64.tar.gz                    # Windows용 node_modules
├── node_modules-linux-x64.tar.gz                  # Linux용 node_modules (WSL Ubuntu 22.04에서 실제 실행 검증)
├── reflex.install_frontend_packages.cached.win    # 설치 성공 캐시 마커 (Windows)
├── reflex.install_frontend_packages.cached.linux  # 설치 성공 캐시 마커 (Linux)
├── package.win.json / package.linux.json          # 참고용 — 실제 실행 후 각 OS가 기록한 package.json (배치 시 안 씀)
├── bun.lock / bunfig.toml                          # 두 OS 공통
```

대상 서버의 OS에 맞는 세트(`win` 또는 `linux`)를 사용합니다. **두 세트 모두 오프라인 조건(node_modules + 캐시 마커 + `REFLEX_USE_NPM=1`)을 그대로 재현해서 `reflex run`이 `App running at: http://localhost:3000/`까지 뜨는 걸 실제로 확인했습니다** (Windows는 이 PC에서, Linux는 같은 PC의 WSL Ubuntu 22.04에서 검증).

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

---

## ③ 프런트엔드 패키지(node_modules) + 설치 캐시 마커 배치

Reflex는 `reflex run`을 실행할 때마다 자체 프레임워크 패키지(react, sonner, radix-ui 등)를 `bun add <이름>@<고정버전>`으로 **매번 다시 검증**합니다. `bun add`는 항상 npm 레지스트리에 접속하려고 시도하기 때문에, `node_modules`가 이미 채워져 있어도 인터넷이 없으면 `Connection Refused downloading package manifest ...` 에러가 납니다.

이 단계는 **한 번 성공하면** `.web/reflex.install_frontend_packages.cached`라는 마커 파일에 결과가 캐시되고, 이후 실행부터는 완전히 스킵됩니다(네트워크 재시도 없음). **이 프로젝트를 준비하면서 Windows(이 PC)와 Linux(WSL Ubuntu 22.04) 양쪽에서 이미 한 번씩 성공시켜뒀고, 그 결과물이 `frontend-offline/`에 포함되어 있습니다** — 오프라인 서버는 아래처럼 자기 OS에 맞는 결과물을 그대로 풀어 넣기만 하면 됩니다.

```bash
python -m reflex init          # .web/ 폴더 생성 (reflex.lock/에서 package.json·bun.lock 복원)

# Linux
tar -xzf frontend-offline/node_modules-linux-x64.tar.gz -C .web/
cp frontend-offline/reflex.install_frontend_packages.cached.linux .web/reflex.install_frontend_packages.cached

# Windows (PowerShell)
tar -xzf frontend-offline\node_modules-win-x64.tar.gz -C .web\
Copy-Item frontend-offline\reflex.install_frontend_packages.cached.win .web\reflex.install_frontend_packages.cached
```

풀어놓은 뒤 확인:

```bash
ls .web/node_modules | wc -l                       # 130개 내외면 정상
ls .web/reflex.install_frontend_packages.cached    # 있어야 함
```

> `bun install`을 다시 실행하면 인터넷이 없는 한 실패하니, `.web/`이 이미 만들어진 상태에서 **node_modules와 캐시 마커만 압축 해제/복사로 채워 넣고 재실행하지 않는 것**이 핵심입니다.
>
> 캐시 마커의 fingerprint에는 `bun_path`도 포함되는데, 기본값은 `C:\Users\<사용자명>\...`처럼 **사용자명이 들어간 경로**라 머신마다 달라집니다. 그래서 ②처럼 `rxconfig.py`에 고정 경로를 지정해둔 것이고, 이 경로가 빌드 환경과 오프라인 환경에서 **완전히 동일해야**(파일이 그 경로에 실제로 존재해야) 캐시가 재사용됩니다 — Bun 자체는 ④에서 실행에 쓰이지 않더라도, 이 fingerprint를 맞추기 위해 ②의 배치는 그대로 필요합니다.

---

## ④ Node.js/npm으로 실행 (★ Bun으로 직접 실행하면 안 됨)

`.web/node_modules/@react-router/dev`(react-router 8.3.0)를 **Bun으로 직접 실행하면 (Windows에서) 자체 재시작 로직 버그로 크래시**합니다 (`restartWithMergedOptions() ... This is likely a bug in @react-router/dev.`). Bun은 위 ③의 설치 캐시를 유효하게 만들기 위해서만 필요하고, **실제 프런트엔드 서버 실행은 npm(Node.js)으로 해야** 합니다. (Linux/WSL에서는 이 버그가 재현되지 않았지만, 캐시 마커 자체가 `REFLEX_USE_NPM=1` 상태로 만들어졌으니 Linux에서도 그대로 설정하고 실행하세요.)

내부망 서버에 **Node.js 22 이상**이 이미 있다고 하셨으니, 실행 전에 아래 환경변수만 설정하면 됩니다:

```bash
# Linux
export REFLEX_USE_NPM=1

# Windows (PowerShell)
$env:REFLEX_USE_NPM = "1"
```

```bash
python -m reflex run
```

- 프론트엔드: `http://<서버IP>:3000`
- 백엔드: `http://<서버IP>:8000`

매번 설정하기 번거로우면 시스템 환경변수로 `REFLEX_USE_NPM=1`을 영구 등록해두는 것을 권장합니다.

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
| Windows에서 `OSError: [WinError 1314] 클라이언트가 필요한 권한을 가지고 있지 않습니다` (symlink 관련) | Windows가 심볼릭 링크 생성 권한을 요구함. 설정 → 개발자 모드를 켜거나, 관리자 권한으로 터미널을 실행 |
| `error: restartWithMergedOptions() was called, but the process has already been restarted. This is likely a bug in @react-router/dev.` | Bun으로 프런트엔드를 직접 실행해서 생기는 버그. ④처럼 `REFLEX_USE_NPM=1`을 설정하고 Node.js(22+)로 실행할 것 |
| `Your version (20.x) of Node.js is out of date. Upgrade to 22.22.0 or higher.` | `node --version`으로 확인 후 Node.js 22 LTS로 업그레이드 |

## 참고

- 이 wheelhouse/frontend-offline은 **Python 3.11 / reflex 0.9.10.post2 / Bun 1.3.14** 기준으로 만들어졌습니다. `requirements.txt`의 버전을 올리면 두 번들 모두 다시 만들어야 합니다.
- 설치(패키지 검증)는 Bun이 하고, 실행은 npm/Node.js가 하는 **혼합 구조**입니다 — 둘 다 필요합니다. Bun만 있고 Node.js 22가 없다면 ④가 안 됩니다.
- 앱 자체의 미구현 부분(DB 연결, Parser 연동 등)은 [TODO.md](TODO.md)를 참고하세요.
