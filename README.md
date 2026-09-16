# DocParse Console

내부망 문서 파싱 업무(업로드 → Parser 실행 → Job 모니터링 → 검수/구조 편집 → Export)를 하나의 웹 UI로 통합하기 위한 **Reflex 기반 Document Parsing Platform**입니다.

기존 Streamlit 대시보드를 대체할 목적으로 만들어지고 있으며, 현재 상태는 **UI/UX 목업(Mockup) 단계**입니다. 실제 업로드, 파싱, DB 연결, 백그라운드 Job 실행은 아직 구현되어 있지 않습니다. 목업 범위와 다음 단계는 [TODO.md](TODO.md)를 참고하세요.

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
├── pages/                    # 페이지별 레이아웃 (dashboard, documents, jobs, validation, settings)
├── components/                # 화면 단위 UI 컴포넌트 (sidebar, shell, 각 페이지 위젯)
├── states/                    # rx.State — 현재는 하드코딩된 목업 데이터만 보유
└── parsers/
    └── contracts.py          # 실제 Parser/Job 연결 시 사용할 타입 계약 (Protocol, dataclass) — 구현체 없음
rxconfig.py                    # Reflex 앱 설정 (app_name, plugins)
requirements.txt                # reflex[db], xy[reflex] 의존성
plan.md                         # 목업 구현 계획 체크리스트
REFLEX_AI_BUILDER.md            # 전체 프로젝트 요구사항 및 아키텍처 설계 문서
```

## 시작하기

### 요구 사항

- Python 3.12+ (`from __future__ import annotations`, `StrEnum`, `slots=True` 사용)
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

이 저장소는 **정적 목업**입니다. 모든 화면의 데이터는 각 `app/states/*.py`에 하드코딩되어 있고, 업로드/파싱 실행/저장/재파싱 버튼은 시각적으로만 존재하며 실제 동작과 연결되어 있지 않습니다. 실제로 동작하는 애플리케이션으로 만들기 위해 필요한 작업은 [TODO.md](TODO.md)에 파일/라인 단위로 정리했습니다.

## 설계 문서

- [REFLEX_AI_BUILDER.md](REFLEX_AI_BUILDER.md) — 목적, 아키텍처, 화면별 요구사항, Parser/Job 모델, Migration 전략 등 전체 요구사항 명세
- [plan.md](plan.md) — 목업 구현 체크리스트
