# TODO — 목업을 실제 동작하는 앱으로 만들기

이 문서는 현재 저장소가 **정적 목업(Mockup)**이며, 실제로 문서를 업로드·파싱·검수·저장하려면 어떤 설정/구현이 추가로 필요한지 파일과 줄 번호 단위로 정리한 것입니다. 배경 설계는 [REFLEX_AI_BUILDER.md](REFLEX_AI_BUILDER.md)를 참고하세요.

전체 상태를 한 문장으로 요약하면: **Documents/Dashboard 페이지는 Qdrant 기반으로 실연동되었고(3, 7번 항목), 나머지(Jobs/Validation/Settings)는 아직 UI 레이아웃과 타입 계약(`contracts.py`)만 존재하며 데이터베이스·Parser 구현체·Job Worker·State의 이벤트 핸들러가 비어 있습니다.**

---

## 1. Database 연결

- 아직 어떤 DB에도 연결되어 있지 않습니다. [rxconfig.py:20-31](rxconfig.py)의 `rx.Config`에 `db_url`이 설정되어 있지 않습니다.
- `requirements.txt:2`에 `reflex[db]`가 이미 포함되어 있으므로 SQLModel 기반 DB 기능은 사용 가능한 상태입니다.
- 필요한 작업:
  1. `rxconfig.py`에 `db_url="sqlite:///docparse.db"` (요구사항 문서상 초기 저장소, [REFLEX_AI_BUILDER.md:123](REFLEX_AI_BUILDER.md) 참조) 추가.
  2. `app/models/` 패키지를 새로 만들어 `rx.Model` 기반 `Document`, `ParsingJob`, `ParseResult` 테이블 정의 ([REFLEX_AI_BUILDER.md:382-386, 407-419](REFLEX_AI_BUILDER.md)의 필드 구조 참고).
  3. `reflex db init` / `reflex db makemigrations` / `reflex db migrate` 실행.
  4. 각 State(`DashboardState`, `DocumentsState`, `JobsState`, `ValidationState`)가 하드코딩된 리스트 대신 DB 쿼리 결과를 로드하도록 변경 (아래 2~5번 항목 참고).

## 2. Parser 구현체 연결 (Adapter 미등록)

- 계약(타입)만 정의되어 있고 구현체가 전혀 없습니다: [app/parsers/contracts.py:159-201](app/parsers/contracts.py)에 `ParserAdapter`, `ParsingService`, `ParserRegistry`가 `Protocol`로만 선언되어 있습니다.
- `app/parsers/__init__.py`는 완전히 비어 있습니다 — PDF/HWP/HWPX/DOCX/PPTX 어댑터 구현체가 하나도 없습니다.
- [app/states/settings_state.py:33-79](app/states/settings_state.py)의 `adapters` 테이블에 5개 형식이 모두 `"connection": "연결 대기"` 로 표시되어 있는데, 이는 실제 등록 상태가 아니라 하드코딩된 문자열입니다.
- 필요한 작업:
  1. `app/parsers/pdf.py`, `hwp.py`, `hwpx.py`, `docx.py`, `pptx.py`를 만들고 각각 `ParserAdapter` Protocol(`name`, `supported_formats()`, `can_handle()`, `parse()`)을 구현 ([contracts.py:159-170](app/parsers/contracts.py)).
     - PDF: PyMuPDF 또는 pdfplumber (설정값 참고: [settings_state.py:37](app/states/settings_state.py))
     - HWP: pyhwp (아직 미도입, [settings_state.py:46](app/states/settings_state.py)에 "예정"으로 표시)
     - DOCX/PPTX: python-docx, python-pptx
  2. `app/services/parsing_service.py`에 `ParsingService` Protocol 구현체 작성 ([contracts.py:174-187](app/parsers/contracts.py): `submit`, `progress`, `result`, `cancel`).
  3. `app/services/registry.py` 등에 `ParserRegistry` 구현체 작성 후 위 어댑터들을 등록.
  4. 기존 Streamlit 프로젝트에 이미 구현된 Parser 로직이 있다면 재작성하지 말고 그대로 이 Adapter 안에서 호출하도록 감싸기 ([REFLEX_AI_BUILDER.md:356-388, 622](REFLEX_AI_BUILDER.md)의 "기존 Parser 재사용" 원칙).

## 3. 업로드 기능 (Documents 페이지)

**2026-09-17 갱신: 아래 항목 중 목록 조회/파싱 방법 선택/업로드 호출까지는 실연동되었습니다.**
(설계 근거: [docs/superpowers/specs/2026-09-17-documents-real-integration-design.md](docs/superpowers/specs/2026-09-17-documents-real-integration-design.md))

- ✅ 문서 목록은 더 이상 하드코딩이 아니라 Qdrant(`PARENT_COLLECTION`)에서 실제로 조회합니다 — [app/services/qdrant_service.py](app/services/qdrant_service.py), [app/states/documents_state.py:66-75](app/states/documents_state.py)의 `load_documents`. **주의**: 이 목록은 1번 항목(Database 연결)에서 말하는 SQLModel `Document` 테이블이 아니라 Qdrant를 그대로 소스로 씁니다 — 이 프로젝트는 문서 목록에 한해 SQL DB 대신 Qdrant를 쓰는 쪽으로 방향이 정해졌습니다.
- ✅ 업로드 영역이 `rx.upload.root(...)`로 교체되어 드래그/클릭 업로드가 실제로 `DocumentsState.upload_selected_file`을 호출합니다 ([documents_panel.py:71-96](app/components/documents_panel.py)).
- ✅ "기본 Parser 프로필" 드롭다운과 그 아래 파싱 방법(Gemma/MinerU/OpendataLoader) 토글·라디오가 State에 실제로 바인딩되어 있습니다 ([documents_panel.py:105-151](app/components/documents_panel.py), [app/parsers/methods.py](app/parsers/methods.py)).
- ⛔ 업로드/삭제/DRM 호출은 여전히 스텁입니다 — [app/services/upload_service.py](app/services/upload_service.py)의 세 함수가 실제 내부망 API 스펙이 확정될 때까지 `NotImplementedError`를 던지도록 되어 있고, 업로드 시 이 에러가 `upload_error` 배너로 그대로 노출됩니다.
- ⛔ Gemma/MinerU/OpendataLoader의 실제 `.parse()` 구현은 여전히 없습니다 ([app/parsers/methods.py](app/parsers/methods.py)) — 선택 UI만 동작하고 실행 버튼과는 아직 연결되지 않았습니다.
- 문서 행의 액션 버튼(파싱 실행/결과 보기/Validation 이동)은 여전히 클릭 이벤트가 없습니다: [documents_panel.py:290-298](app/components/documents_panel.py).
- 필요한 작업:
  1. `UPLOAD_BASE_URL`/`DELETE_BASE_URL`/`DRM_BASE_URL` API 스펙이 정해지면 `app/services/upload_service.py`의 세 함수 본문만 채우기.
  2. `check_drm()`을 업로드 흐름 어느 지점에서 호출할지 결정 (업로드 전 검사인지, 별도 단계인지 — 스펙 문서 11절 "미해결 사항" 참고).
  3. Gemma/MinerU/OpendataLoader 각 클래스의 `parse()`를 실제 구현으로 교체.
  4. 각 행의 "파싱 실행" 버튼에 `on_click` 핸들러를 추가해 Job 제출 로직(4번 항목)과 연결.
  5. `qdrant-client`/`langchain-openai`를 오프라인 배포용 `wheelhouse/`에 추가 (아직 반영 안 됨, OFFLINE_SETUP.md도 갱신 필요).

## 4. Job 실행 / Worker 분리 (Parsing Jobs 페이지)

- [app/states/jobs_state.py:32-34](app/states/jobs_state.py)의 `auto_refresh_label`, `last_refreshed_at`, `next_refresh_at`이 고정 문자열이며 실제 타이머/폴링이 없습니다.
- `jobs` 리스트 전체([jobs_state.py:55-216](app/states/jobs_state.py))가 진행률·현재 페이지·오류 메시지가 모두 하드코딩된 샘플입니다. 실제 Job이 생성/갱신되는 코드가 없습니다.
- 요구사항상 Parser 실행은 Reflex 이벤트 루프를 막지 않는 별도 Worker에서 돌아야 합니다 ([REFLEX_AI_BUILDER.md:45-51, 423-453](REFLEX_AI_BUILDER.md)). 현재는 UI와 분리된 Worker/Queue 코드가 전혀 없습니다.
- [settings_state.py:83-86](app/states/settings_state.py)에도 현재 실행 방식이 `"In-process (동기)"`로 명시되어 있어, Reflex 이벤트 내에서 동기 실행하면 UI가 멈추는 구조임을 스스로 경고하고 있습니다.
- 필요한 작업:
  1. `app/services/job_service.py`에 Job 생성/조회/취소 로직 구현 (`ParsingService.submit/progress/result/cancel`, [contracts.py:179-187](app/parsers/contracts.py)).
  2. 파싱 자체는 `asyncio.create_task` 기반 백그라운드 태스크 또는 별도 Python 프로세스(Worker)에서 실행하고, 진행률은 DB(`ParsingJob` 테이블)에 기록.
  3. `JobsState`에 `rx.event(background=True)` 또는 `yield`로 주기 폴링하는 이벤트를 추가해 3초 간격으로 `ProgressSnapshot`을 가져와 `jobs` 리스트를 갱신 ([settings_state.py:113-117](app/states/settings_state.py)에 명시된 "진행률 폴링 주기: 3초" 반영).
  4. Documents 페이지의 "파싱 실행" 버튼(3번 항목) → `job_service.submit()` 호출로 연결.
  5. **2026-09-18 추가**: 이 기능이 붙으면 Job 시작/완료 시점에 [app/services/job_log_service.py](app/services/job_log_service.py)의 `append_job_event()`도 함께 호출해야 한다 — Dashboard의 "최근 Job"/"Parser별 처리량"/"평균 파싱 시간"이 이 로그를 읽어 집계하는데, 현재는 아무도 호출하지 않아 항상 빈 상태다 (7번 항목 참고).

## 5. Validation / 구조 편집 (가장 핵심 화면, 현재 전부 시각화 전용)

- [app/states/validation_state.py](app/states/validation_state.py) 전체가 정적 목업입니다: `viewer_lines`(80-114행), `markdown_lines`/`json_lines`(116-379행), `blocks`(381-452행), `heading_tree`(486-591행) 모두 하드코딩된 한 개 문서 예시입니다.
- 상단 툴바의 핵심 버튼들이 클릭해도 아무 동작을 하지 않습니다: [app/components/validation_workbench.py:99-113](app/components/validation_workbench.py) (`Reparse`, `Markdown Export`, `JSON Export`), 이를 [validation_workbench.py:142](app/components/validation_workbench.py)에서 `mock_note("목업 화면 · Reparse·Export·편집 동작 없음")`로 명시.
- Heading level 변경, block 병합/분리/삭제 등 구조 편집 도구도 시각화만 되어 있음: [validation_workbench.py:749](app/components/validation_workbench.py) `mock_note("모든 편집 제어는 시각화 전용")`.
- 필요한 작업:
  1. Documents/Jobs에서 완료된 Job의 `ParseResult` ([contracts.py:145-155](app/parsers/contracts.py))를 DB 또는 파일에서 읽어와 `ValidationState`에 로드하는 이벤트 추가 (현재는 `document_id`가 [validation_state.py:63](app/states/validation_state.py)에 고정값으로 박혀 있음).
  2. 원본 미리보기(Panel A)를 실제 PDF/문서 렌더러(예: pdf.js iframe, 또는 페이지별 이미지)로 교체 — 현재 `viewer_lines`는 텍스트를 흉내 낸 것뿐, 실제 페이지 이미지/좌표(bbox) 연동 없음.
  3. `Reparse` 버튼에 Job 재제출 이벤트 연결 (4번 Job 항목과 동일 경로).
  4. `Markdown Export` / `JSON Export` 버튼에 실제 파일 다운로드(`rx.download`) 이벤트 연결, 저장 경로는 [settings_state.py:134-138](app/states/settings_state.py) 참고.
  5. Heading level 변경, Paragraph↔Heading 전환, Block 순서/병합/분리/삭제, Table 지정 등 편집 동작을 `ValidationState`의 이벤트 핸들러로 구현하고, 수정 결과를 원본 Parser 결과와 별도 테이블에 저장 ([REFLEX_AI_BUILDER.md:339-350](REFLEX_AI_BUILDER.md) "수정 결과는 원본과 별도 관리").
  6. `change_log`([validation_state.py:615-623](app/states/validation_state.py))를 실제 편집 이력 누적 리스트로 전환.

## 6. Settings 저장 미연결

- Parser/Worker/Storage 설정 화면이 전부 읽기 전용 표시입니다.
  - [app/components/settings_panels.py:112](app/components/settings_panels.py): `note="목업 화면 · 실제 등록·설정 저장 없음"`
  - [settings_panels.py:189](app/components/settings_panels.py), [settings_panels.py:199](app/components/settings_panels.py): 각각 Worker/Storage 섹션에 `note="설정 저장 미연결"`
- 필요한 작업:
  1. 설정값을 코드 상수가 아니라 DB 테이블(`AppConfig` 등) 또는 설정 파일(`.env`/`config.toml`)로 이전.
  2. `SettingsState`에 저장/수정 이벤트 핸들러 추가 (`worker_config`, `storage_config`가 현재는 [settings_state.py:81-157](app/states/settings_state.py)에 하드코딩된 표시용 값).

## 7. Dashboard 지표 실데이터 연동

**2026-09-18 갱신: 아래 항목 중 문서 수 KPI/파일 유형 차트, 그리고 Job 로그 연동 배관까지는 실연동되었습니다.**

- ✅ 전체 문서/파싱 성공/Warning/Failed/검수 필요 KPI와 "파일 유형별 문서 수" 차트는 더 이상 하드코딩이 아니라 Qdrant 집계 결과([app/services/qdrant_service.py](app/services/qdrant_service.py))에서 채워집니다 — [app/states/dashboard_state.py](app/states/dashboard_state.py)의 `load_dashboard`, `_build_kpis`.
- ✅ "최근 Job" 테이블, "Parser별 처리량" 차트, "평균 파싱 시간" KPI를 위한 배관도 완성되었습니다 — 새로 추가된 로컬 `data/job_log.jsonl`(JSON Lines)을 [app/services/job_log_service.py](app/services/job_log_service.py)가 읽어 `DashboardState.load_dashboard`에 넘겨줍니다. 다만 **이 로그 파일에는 아직 아무도 쓰지 않아 항상 비어 있습니다** — 그래서 이 세 위젯은 현재도 "기록 없음" 빈 상태로 보입니다.
- ⛔ 파이프라인 단계별 큐 카운트(`queue_stages`)는 여전히 스텁입니다 — 실시간 큐 시스템이 없어 [dashboard_state.py](app/states/dashboard_state.py)에서 항상 빈 리스트를 반환하고, UI가 "실시간 큐 연동 대기" 안내로 대체합니다.
- ⛔ `job_log_service.append_job_event()`를 호출하는 곳이 아직 없습니다 — 함수 시그니처와 파일 포맷만 확정되어 있으며, 실제로 로그를 채우려면 4번 항목("Job 실행 / Worker 분리")의 Job 시작/완료 지점에서 이 함수를 호출하도록 배선해야 합니다 (4번 항목에 메모 추가함).
- 필요한 작업:
  1. 4번 항목(Job 실행/Worker 분리) 구현 시 `append_job_event()` 호출 배선.
  2. 파이프라인 단계별 큐 카운트를 채우려면 실시간 큐/Worker 상태 조회 API가 먼저 필요 (4번 항목과 연계).

## 8. 배포/실행 환경

- `apt-packages.txt`가 비어 있습니다 — HWP 등 바이너리 파싱에 필요한 시스템 패키지(예: LibreOffice headless, 폰트 등)가 정해지면 채워야 합니다.
- 현재 `reflex run`으로 프론트/백엔드가 뜨는지만 확인된 상태이며, 프로덕션 배포(WSGI/ASGI 서버, 리버스 프록시, 내부망 인증) 설정은 없습니다.

---

## 우선순위 제안 (REFLEX_AI_BUILDER.md 15장 Phase와 매칭)

1. **Phase 2**: DB 연결(1) + Parser Adapter 최소 1종(PDF) 구현(2)
2. **Phase 3**: 업로드(3) + Job 시스템/Worker 분리(4)
3. **Phase 4**: Validation 실데이터 로드(5-1, 5-2)
4. **Phase 5**: 구조 편집 기능(5-5)
5. **Phase 6**: Reparse/Export(5-3, 5-4)
6. 나머지: Settings 저장(6), Dashboard 집계(7), 배포 설정(8)
