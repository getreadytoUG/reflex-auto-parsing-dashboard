# DocParse Console

내부망 문서 파싱 업무(업로드 → Parser 실행 → Job 모니터링 → 검수/구조 편집 → Export)를 하나의 웹 UI로 통합하기 위한 **Reflex 기반 Document Parsing Platform**입니다.

기존 Streamlit 대시보드를 대체할 목적으로 만들어지고 있으며, 현재 상태는 **일부 실연동 + 일부 목업이 섞인 단계**입니다. Documents/Dashboard 페이지와 Jobs/Validation 페이지의 조회·탭 전환·Export는 Qdrant 기반으로 실제 동작하고, 업로드/파싱 실행/재파싱/구조 편집/Settings 저장은 아직 스텁이거나 시각화 전용입니다. 화면별 정확한 상태와 남은 작업은 [TODO.md](TODO.md)에 파일/라인 단위로 정리되어 있습니다.

## 주요 화면

| 라우트 | 페이지 | 설명 |
| --- | --- | --- |
| `/` | Dashboard | 전체 문서 KPI, 파일 유형별 분포, Parser별 처리량, 최근 Job 테이블 |
| `/documents` | Documents | 문서 업로드 영역, 문서 목록, Parser 선택, 상태/형식 필터 |
| `/jobs` | Parsing Jobs | 실행 중인 Job 큐, 진행률, 현재 단계/페이지, 오류 메시지 |
| `/validation` | Validation | 원본 미리보기 · Markdown/JSON/Blocks/Tables 탭 · Heading Tree · 구조 편집 도구 |
| `/settings` | Settings | Parser Adapter 등록 현황, Worker/Storage 설정, 향후 확장 로드맵 |

## 기술 스택

- [Reflex](https://reflex.dev) 0.9.x — Python 전용 풀스택 웹 프레임워크
- `reflex_xy` — Dashboard 차트(파일 유형 분포, Parser 처리량) 렌더링
- Tailwind CSS (`TailwindV4Plugin`) — 스타일링
- Noto Sans KR — 한국어 업무용 타이포그래피

## 프로젝트 구조

```text
app/
├── app.py                    # Reflex App 엔트리포인트, 라우트 등록
├── config.py                 # .env 로드, Qdrant 컬렉션 이름 등 설정값
├── pages/                    # 페이지별 레이아웃 (dashboard, documents, jobs, validation, settings)
├── components/               # 화면 단위 UI 컴포넌트 (sidebar, shell, 각 페이지 위젯)
├── states/                   # rx.State — 페이지별로 실연동/목업이 섞여 있음 (TODO.md 참고)
├── services/                 # DB/외부 API 없이 순수 함수로 작성된 서비스 계층
│   ├── qdrant_service.py     # 문서 목록/집계/청크 조회 (실동작)
│   ├── jobs_service.py       # Job 조회/재파싱 제출 (API 스펙 미확정, 스텁)
│   ├── job_log_service.py    # Dashboard 집계용 로컬 Job 로그 (data/job_log.jsonl)
│   ├── upload_service.py     # 업로드/삭제/DRM (내부망 API 스펙 미확정, 스텁)
│   └── llm_service.py        # Gemma 등 VLM/LLM 공용 클라이언트
└── parsers/
    ├── contracts.py          # Parser/Job 연결 시 사용할 타입 계약 (Protocol, dataclass)
    └── methods.py            # 파싱 방법(Gemma/MinerU/OpendataLoader) 레지스트리 — 실제 parse()는 미구현
rxconfig.py                    # Reflex 앱 설정 (app_name, db_url, plugins)
requirements.txt                # reflex[db], xy[reflex], qdrant-client 등 의존성
plan.md                         # 초기 목업 구현 계획 체크리스트
REFLEX_AI_BUILDER.md            # 전체 프로젝트 요구사항 및 아키텍처 설계 문서
```

## 시작하기

### 요구 사항

- Python 3.11+ (`StrEnum`, `dataclass(slots=True)` 사용 — 오프라인 배포 대상도 Python 3.11 기준, [OFFLINE_SETUP.md](OFFLINE_SETUP.md) 참고)
- pip

### 설치

```bash
pip install -r requirements.txt
```

### 초기화 (최초 1회)

```bash
reflex init
```

### 개발 서버 실행

```bash
reflex run
```

기본적으로 프론트엔드는 `http://localhost:3000`, 백엔드 API는 `http://localhost:8000`에서 실행됩니다.

### 인터넷이 차단된 내부망 서버에 설치하기

`wheelhouse/`, `frontend-offline/`에 Python 3.11 / Bun 1.3.14 기준 오프라인 설치 번들이 준비되어 있습니다(둘 다 `.gitignore`로 제외되어 있으므로 파일 전송으로 함께 옮겨야 합니다). 절차는 [OFFLINE_SETUP.md](OFFLINE_SETUP.md)를 참고하세요.

## 현재 한계 (중요)

화면별 상태는 다음과 같습니다 (자세한 근거는 [TODO.md](TODO.md) 참고):

- **Dashboard / Documents**: Qdrant에서 실제 문서 목록·KPI·파일 유형 분포를 조회합니다. 다만 업로드/삭제/DRM 호출과 각 파싱 방법(Gemma/MinerU/OpendataLoader)의 실제 `parse()`는 아직 스텁입니다.
- **Parsing Jobs**: 요약/목록 조회는 실제 호출 배관까지 연결되어 있으나, 내부망 Job 큐 API 스펙이 없어 `jobs_service.py`가 항상 `NotImplementedError`를 던집니다. 실시간 폴링/로그/재시도 버튼은 이번 범위 밖입니다.
- **Validation**: 문서 선택 → 청크 로드, 탭 전환, Blocks/Heading 클릭 → 인스펙터, Markdown/JSON Export는 실동작합니다. Reparse는 스텁, 원본 뷰어(Panel A)는 "연동 대기" 안내, Heading/블록 구조 편집은 여전히 시각화 전용입니다.
- **Settings**: 전부 읽기 전용 표시이며 저장 기능이 연결되어 있지 않습니다.

DB 연결(SQLModel), Parser 어댑터(PDF/HWP/HWPX/DOCX/PPTX) 구현체, Job Worker 분리는 아직 없습니다. 남은 작업은 [TODO.md](TODO.md)에 파일/라인 단위로 정리했습니다.

## 설계 문서

- [REFLEX_AI_BUILDER.md](REFLEX_AI_BUILDER.md) — 목적, 아키텍처, 화면별 요구사항, Parser/Job 모델, Migration 전략 등 전체 요구사항 명세
- [plan.md](plan.md) — 목업 구현 체크리스트
