# 오프라인(폐쇄망) 설치 가이드

인터넷이 차단된 내부망 서버에 이 프로젝트를 설치하기 위한 절차입니다. 필요한 오프라인 번들(`wheelhouse/`, `frontend-offline/`)은 이미 프로젝트 폴더 안에 준비되어 있으며, `.gitignore`에 의해 GitHub에는 올라가지 않습니다 — **USB/사내 파일 전송 등으로 프로젝트 폴더 전체를 함께 옮겨야** 아래 절차가 동작합니다.

전체 흐름: **① Python 패키지(wheelhouse) 설치 → ② Bun 실행 파일 배치 → ③ 프런트엔드 패키지(node_modules) 배치 → ④ 실행**

## 사전 준비물 (이미 프로젝트 안에 포함됨)

```text
wheelhouse/
├── win/                          # Python cp311-win_amd64 wheel 72개
└── linux/                        # Python cp311-manylinux_x86_64 wheel 72개

frontend-offline/
├── bun/
│   ├── bun-windows-x64.zip       # Bun 1.3.14 실행 파일 (Windows)
│   └── bun-linux-x64.zip         # Bun 1.3.14 실행 파일 (Linux)
├── node_modules-win-x64.tar.gz   # bun install 결과 (Windows용)
├── node_modules-linux-x64.tar.gz # bun install --os=linux --cpu=x64 결과 (Linux용)
├── package.json / bun.lock / bunfig.toml
```

대상 서버의 OS에 맞는 세트(`win` 또는 `linux`)만 사용하면 됩니다.

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

## ② Bun 실행 파일 배치

Reflex는 프런트엔드 빌드를 위해 **Bun**(Node.js 대체 런타임)이 필요합니다. `rxconfig.py`에 별도 `bun_path`를 지정하지 않는 한, Reflex는 시스템 `PATH`에서 `bun`을 찾아 그대로 사용합니다 — 즉 **PATH에만 올려두면** Reflex 전용 설치 경로에 맞출 필요가 없습니다.

### Linux

```bash
mkdir -p /opt/bun
unzip frontend-offline/bun/bun-linux-x64.zip -d /opt/bun
chmod +x /opt/bun/bun-linux-x64/bun
sudo ln -s /opt/bun/bun-linux-x64/bun /usr/local/bin/bun
bun --version   # 1.3.14 확인
```

### Windows

```powershell
Expand-Archive frontend-offline\bun\bun-windows-x64.zip -DestinationPath C:\bun
# C:\bun\bun-windows-x64\bun.exe 를 시스템 PATH 환경변수에 추가
bun --version
```

최소 요구 버전은 **1.3.0**입니다 (`reflex[db]==0.9.10.post2` 기준).

---

## ③ 프런트엔드 패키지(node_modules) 배치

먼저 `reflex init`으로 `.web/` 스캐폴딩을 생성한 뒤(네트워크 없이도 파일 구조만 만드는 단계라 동작함), 미리 받아둔 `node_modules`를 그대로 풀어 넣습니다.

```bash
python -m reflex init          # .web/ 폴더 생성 (bun install은 자동 실행되지 않을 수 있음)

# Linux
tar -xzf frontend-offline/node_modules-linux-x64.tar.gz -C .web/

# Windows (PowerShell)
tar -xzf frontend-offline\node_modules-win-x64.tar.gz -C .web\
```

풀어놓은 뒤 `.web/node_modules`가 생겼는지 확인:

```bash
ls .web/node_modules | wc -l   # 130개 내외면 정상
```

> `bun install`을 다시 실행하면 인터넷이 없는 한 실패하니, `.web/`이 이미 만들어진 상태에서 **node_modules만 압축 해제로 채워 넣고 재실행하지 않는 것**이 핵심입니다.

---

## ④ 실행

```bash
python -m reflex run
```

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

## 참고

- 이 wheelhouse/frontend-offline은 **Python 3.11 / reflex 0.9.10.post2 / Bun 1.3.14** 기준으로 만들어졌습니다. `requirements.txt`의 버전을 올리면 두 번들 모두 다시 만들어야 합니다.
- 앱 자체의 미구현 부분(DB 연결, Parser 연동 등)은 [TODO.md](TODO.md)를 참고하세요.
