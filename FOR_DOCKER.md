# Reflex 폐쇄망(Linux) Docker 배포 가이드

**외부망**에서는 "환경"만 담은 베이스 이미지(`reflex-base`)를 만들고, **내부망**에서는 그 이미지 위에 **내부망 소스코드**를 넣어 인터넷 없이 빌드·실행합니다.

- `reflex-base` 안에 들어있는 것: Python 패키지(venv), Bun, Node/npm, nginx, **npm 오프라인 캐시**(`/opt/npm-cache`), nginx 설정, 시작 스크립트
- 소스코드는 베이스 이미지에 들어가지 않습니다 → 내부망 소스가 아무리 바뀌어도 내부망에서 다시 빌드하면 반영됩니다.
- npm 캐시에는 현재 앱이 쓰는 패키지 + **Reflex 내장 컴포넌트가 쓰는 npm 패키지 전부**(차트/마크다운/코드블록/plotly/moment 등)가 들어있어, 내부망 코드가 새 컴포넌트를 써도 오프라인 빌드가 됩니다.
- 컨테이너 하나 안에서 **nginx(80, 정적 프런트 + 프록시)** + **Reflex 백엔드(내부 8000, backend-only)** 가 함께 돕니다.
- 베이스 OS 이미지: `python:3.11-slim`

---

## 파일 구성

| 파일 | 용도 | 내부망 반입 |
| --- | --- | --- |
| `docker/base.Dockerfile` | 외부망에서 `reflex-base` 빌드 | ✗ (이미지 tar 로 대신 반입) |
| `docker/warm-npm-packages.txt` | npm 캐시에 미리 넣을 패키지 목록 | ✗ |
| `docker/nginx.conf`, `docker/start.sh` | 베이스 이미지 안에 포함됨 | ✗ |
| `Dockerfile` | 내부망 소스 빌드 (인터넷 없이) | ✅ 소스 루트에 |
| `.dockerignore` | 빌드에서 `.web/`, `.env`, 데이터 등 제외 | ✅ 소스 루트에 |
| `docker-compose.yml` | 빌드 + 실행 | ✅ 소스 루트에 |
| `reflex-base_1.0.0.tar` | 베이스 이미지 | ✅ 아무 곳에 |

`deploy_bundle/` 폴더에 반입할 4개가 모여 있습니다.

---

## ① 외부망 — 베이스 이미지 만들기

```powershell
docker build --platform linux/amd64 -f docker/base.Dockerfile -t reflex-base:1.0.0 .
docker save reflex-base:1.0.0 -o deploy_bundle/reflex-base_1.0.0.tar
```

`requirements.txt` 를 바꿨을 때만 다시 만들면 됩니다 (소스 변경은 상관없음).

## ② 내부망 — 최초 1회

```bash
docker load -i reflex-base_1.0.0.tar
```

`Dockerfile`, `.dockerignore`, `docker-compose.yml` 3개를 **내부망 소스 루트**(`rxconfig.py` 가 있는 폴더)에 복사합니다.

## ③ 내부망 — 빌드 + 실행 (소스 바꿀 때마다 이것만)

```bash
cd <소스 루트>
mkdir -p volumes/uploaded_files volumes/data
docker compose up -d --build
docker compose logs -f app        # "App running" 보이면 Ctrl+C
```

접속: `http://<서버IP>:8080`

- 포트 변경: `.env` 에 `PUBLIC_PORT=9000` 추가 후 `docker compose up -d` (재빌드 불필요)
- 중지: `docker compose down` / 재시작: `docker compose restart`

---

## 검증 내역 (외부망 PC에서 재현)

- 현재 소스에 `rx.recharts`, `rx.markdown`(수식·표), `rx.code_block`, `rx.moment` 페이지를 추가한 "변경된 소스"를 `docker build --network none`(인터넷 완전 차단)으로 빌드 → 성공
- 실행 후 모든 페이지 200, `/_event` 웹소켓 101, `PUBLIC_PORT=9100` 반영 확인

---

## 주의 사항

| 항목 | 내용 |
| --- | --- |
| 새 Python 패키지 | 내부망 `requirements.txt` 에 베이스에 없는 패키지가 있으면 빌드 첫 단계(`pip install --no-index`)에서 바로 실패 → 외부망에서 `requirements.txt` 갱신 후 베이스 재빌드·재반입 |
| `rx.data_editor` | Reflex 0.9.10 자체 문제로 **인터넷이 있어도** 빌드 실패(`marked` 누락). 쓰지 말 것 |
| `Dockerfile` 첫 줄 | `# syntax=docker/dockerfile:1` 를 넣으면 빌드 시 Docker Hub 접속을 시도해 내부망에서 실패 |
| 빌드 중 import | `reflex export` 가 앱 코드를 import 함. 모듈 최상단에서 Qdrant 접속 등을 하면 빌드 실패 → 함수/이벤트 안으로 |
| FastAPI 커스텀 엔드포인트 | 경로 prefix 를 `docker/nginx.conf` 의 `location ~ ^/(_event\|_upload\|...)` 에 추가하고 베이스 재빌드 |
| `.env` 주소 | `localhost`/`127.0.0.1` 은 컨테이너 자기 자신을 가리킴 → 서버 실제 IP 로 |
| 데이터 보존 | 업로드 파일·`data/` 는 `./volumes/` 에 저장되어 재빌드·재생성 후에도 유지 |
| CPU 아키텍처 | `linux/amd64` (= x86_64, Intel/AMD 공통). 서버에서 `uname -m` → `x86_64` 확인 |
