# Document Parsing Platform — Reflex AI Builder 요구사항

## 1. 프로젝트 목적

기존 Streamlit 기반의 내부망 문서 파싱 대시보드를 **Reflex 기반 웹 애플리케이션**으로 전환한다.

목표는 단순한 대시보드가 아니라 다음 업무를 하나의 UI에서 수행할 수 있는 **사내 Document Parsing Platform**을 만드는 것이다.

- PDF / HWP / HWPX / DOCX / PPTX 등 문서 업로드
- 문서 형식에 맞는 Parser 선택 및 실행
- 파싱 작업(Job)의 비동기 실행 및 상태 모니터링
- 파싱 중에도 다른 문서를 검수할 수 있는 멀티 Job 환경
- 원본 문서와 파싱 결과 비교
- Markdown 구조 및 Heading Tree 검수
- 파싱 결과 오류 수정
- 수정 후 재파싱
- 최종 Markdown / JSON 등 결과 Export

---

## 2. 핵심 UX

사용자가 `A.pdf`의 파싱을 시작한 뒤 파싱이 수십 초~수분 동안 실행되더라도 UI가 멈추면 안 된다.

예:

```text
A.pdf
  ↓
[파싱 시작]
  ↓
Job #123
  ↓
Parsing 37%
  ↓
사용자는 B.docx를 열어 검수
  ↓
A.pdf 파싱은 백그라운드에서 계속 실행
  ↓
A.pdf 완료
  ↓
UI에서 자동으로 Completed 상태 표시
```

따라서 UI와 무거운 Parser 실행을 분리한다.

중요:
- Reflex가 Parser 자체를 동기적으로 실행해서 UI를 막는 구조를 만들지 않는다.
- Parser는 별도의 Worker Process/Task에서 실행한다.
- 처음에는 서버 1대에서도 가능하지만, UI 프로세스와 Worker 프로세스는 논리적으로 분리한다.
- 추후 필요하면 Worker 서버를 별도 서버로 확장할 수 있도록 설계한다.

---

## 3. 권장 아키텍처

초기에는 내부망 단일 서버에서 다음 구조를 사용한다.

```text
                    Browser
                       │
                       ▼
               ┌────────────────┐
               │     Reflex     │
               │   Web App/UI   │
               └───────┬────────┘
                       │
                       ▼
                ┌──────────────┐
                │ Job Manager  │
                └───────┬──────┘
                        │
                        ▼
                 ┌────────────┐
                 │ Job Queue  │
                 └─────┬──────┘
                       │
          ┌────────────┼────────────┐
          ▼            ▼            ▼
      Worker 1      Worker 2      Worker 3
          │            │            │
         PDF          HWP          DOCX
       Parser        Parser        Parser
          │            │            │
          └────────────┼────────────┘
                       ▼
                 Result Storage
```

처음에는 복잡한 Redis/Celery 등을 반드시 도입하지 않는다.

초기 구현:
- Reflex
- Python Worker Process
- SQLite
- Local File System

향후 확장:
- SQLite → PostgreSQL
- Local Process → Worker Service
- 단순 Queue → Redis 기반 Queue
- 필요 시 Parser Worker 서버 분리

---

## 4. UI 전체 구조

왼쪽 Sidebar를 사용하는 관리자/업무용 UI로 만든다.

```text
┌─────────────────────────────────────────────────────────────┐
│ Document Parser                              ● Internal     │
├───────────────┬─────────────────────────────────────────────┤
│               │                                             │
│ Dashboard     │                                             │
│ Documents     │                                             │
│ Parsing Jobs  │              Main Content                   │
│ Validation    │                                             │
│ Settings      │                                             │
│               │                                             │
└───────────────┴─────────────────────────────────────────────┘
```

### 메뉴

1. Dashboard
2. Documents
3. Parsing Jobs
4. Validation
5. Settings

---

# 5. Dashboard

첫 화면은 문서 파싱 현황을 한눈에 보여준다.

### KPI

```text
┌────────────┐ ┌────────────┐ ┌────────────┐ ┌────────────┐
│ 전체 문서  │ │   성공     │ │  Warning   │ │   Failed   │
│    128     │ │    121     │ │     5      │ │     2      │
└────────────┘ └────────────┘ └────────────┘ └────────────┘
```

추가 통계:

- 전체 문서 수
- 성공 문서 수
- 실패 문서 수
- 검수 필요 문서 수
- 평균 파싱 시간
- 파일 타입별 문서 수
- Parser별 처리량

### Recent Parsing Jobs

테이블:

```text
파일명             Parser          상태          처리시간
----------------------------------------------------------
규정집.pdf         PyMuPDF         Completed      12.4s
업무매뉴얼.hwp     HWP Parser      Parsing        -
계약서.docx        python-docx     Warning         5.8s
```

상태는 색상/Badge로 명확하게 표시한다.

- Completed
- Parsing
- Queued
- Warning
- Failed
- Cancelled

---

# 6. Documents

문서 관리 화면.

기능:

- 파일 업로드
- 파일 목록
- 파일 형식 표시
- 파일 크기
- 업로드 날짜
- 마지막 파싱 날짜
- 현재 상태
- Parser 선택
- 파싱 실행
- 결과 보기
- Validation으로 이동

예:

```text
┌─────────────────────────────────────────────────────────────┐
│ Documents                                      [Upload]     │
├─────────────────────────────────────────────────────────────┤
│ 파일명          타입      상태       마지막 파싱            │
│ 규정집.pdf      PDF       ✓          2026-09-16             │
│ 매뉴얼.hwp      HWP       ⚠          2026-09-16             │
│ 계약서.docx     DOCX      ✓          2026-09-15             │
└─────────────────────────────────────────────────────────────┘
```

---

# 7. Parsing Jobs

현재 실행 중인 모든 파싱 Job을 보여준다.

중요한 화면이다.

```text
┌──────────────────────────────────────────────────────────────┐
│ Parsing Jobs                                                  │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│ contract.pdf                                                 │
│ PDF → Markdown                                                │
│ ███████████████░░░░░ 72%                                     │
│ Page 43 / 61                                                 │
│ Current step: Structure Detection                            │
│                                                              │
│ manual.hwp                                                   │
│ ████████████████████ 100%                                    │
│ ✓ Completed                                                  │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

각 Job에는 다음 정보가 필요하다.

- Job ID
- File ID
- File Name
- Parser
- Status
- Progress
- Current Page
- Total Page
- Current Step
- Started At
- Finished At
- Error Message
- Result Path

가능하면 실시간으로 상태를 갱신한다.

---

# 8. Validation

이 프로젝트의 핵심 화면.

문서 파싱 결과를 사람이 검수할 수 있어야 한다.

가능한 UI:

```text
┌──────────────────────────────────────────────────────────────┐
│ Validation: 규정집.pdf                         [Reparse]     │
├───────────────────────┬──────────────────────────────────────┤
│                       │                                      │
│ Original Document     │ Parsed Markdown                      │
│                       │                                      │
│ [PDF Viewer]          │ # 제1장 총칙                         │
│                       │                                      │
│ Page 12               │ ## 제1조 목적                        │
│                       │                                      │
│                       │ 본 규정은 ...                        │
│                       │                                      │
├───────────────────────┴──────────────────────────────────────┤
│ Structure Tree                                               │
│                                                              │
│ ▼ 제1장 총칙                                                │
│   ▼ 제1조 목적                                              │
│      ├── 제1항                                              │
│      └── 제2항                                              │
│   ▼ 제2조 정의                                              │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

가능하면 화면을 2~3개 패널로 구성한다.

### Panel A — Original

- PDF preview
- 페이지 이동
- 원본 문서 확인

### Panel B — Parsed Result

- Markdown
- JSON
- block 정보
- table 정보

### Panel C — Structure Tree

```text
H1
 ├── H2
 │    ├── H3
 │    └── H3
 └── H2
```

Heading hierarchy가 한눈에 보여야 한다.

---

# 9. Structure Editing

사용자가 파싱된 구조를 직접 수정할 수 있어야 한다.

예:

```text
H1
 ├── H2
 │    └── H3
```

사용자가 H3를 H2로 변경:

```text
H1
 ├── H2
 │    └── H2
```

지원하고 싶은 수정:

- Heading level 변경
- Paragraph ↔ Heading
- Block 순서 변경
- Table 지정
- Block 삭제
- Block 병합
- Block 분리
- Text 수정

수정 결과는 원본 Parser 결과와 별도로 관리한다.

---

# 10. Parser 구조

기존 Parser 구현을 최대한 재사용한다.

UI 코드 안에 Parser 로직을 넣지 않는다.

권장:

```text
backend/
├── parsers/
│   ├── pdf.py
│   ├── hwp.py
│   ├── hwpx.py
│   ├── docx.py
│   └── pptx.py
│
├── processing/
│   ├── extraction.py
│   ├── structure.py
│   ├── heading.py
│   └── validation.py
│
├── services/
│   ├── parsing_service.py
│   ├── document_service.py
│   └── job_service.py
│
└── models/
    ├── document.py
    ├── job.py
    └── parsing_result.py
```

Reflex UI는 `services`를 호출하고 실제 Parser 구현은 `parsers`에 둔다.

---

# 11. Job 모델

최소한 다음과 같은 Job 상태가 필요하다.

```text
QUEUED
RUNNING
COMPLETED
WARNING
FAILED
CANCELLED
```

예:

```python
class ParsingJob:
    id: str
    document_id: str
    parser_type: str
    status: str
    progress: int
    current_step: str
    current_page: int
    total_pages: int
    error_message: str | None
    result_path: str | None
```

---

# 12. 중요한 설계 원칙

### UI와 Parser를 강하게 분리한다.

나쁜 구조:

```text
Reflex Event
   ↓
PDF parsing 60초
   ↓
UI blocked
```

좋은 구조:

```text
Reflex Event
   ↓
Create Job
   ↓
Worker 실행
   ↓
Job 상태 업데이트
   ↓
Reflex UI 갱신
```

### UI는 Job의 상태를 보여주는 역할에 집중한다.

Parser가 UI를 직접 조작하거나 UI 상태를 직접 관리하지 않는다.

---

# 13. 기존 Streamlit 프로젝트 Migration

현재 프로젝트는 이미 Streamlit으로 구현되어 있다.

전체 코드를 새 프로젝트로 복사해서 한 번에 갈아엎지 않는다.

Git 전략:

```text
main
│
└── refactor/reflex
      │
      ├── feature/parser-service
      ├── feature/reflex-shell
      ├── feature/job-system
      ├── feature/document-viewer
      └── feature/validation-ui
```

기존 Streamlit 코드는 당분간 유지한다.

목표 구조:

```text
                Parser / Service
                 ▲           ▲
                 │           │
            Streamlit      Reflex
             (legacy)       (new)
```

먼저 기존 Streamlit에 섞여 있는 업무 로직을 분리한다.

그 다음 Reflex를 붙인다.

Reflex 구현이 안정화된 뒤 Streamlit UI를 제거한다.

---

# 14. 현재 프로젝트에서 가장 중요한 우선순위

다음 순서로 구현한다.

## Phase 1 — Reflex UI Skeleton

- Sidebar
- Dashboard
- Documents
- Parsing Jobs
- Validation
- Settings

먼저 전체적인 UI/UX를 만든다.

## Phase 2 — Existing Parser 연결

기존 Parser 코드를 최대한 수정하지 않고 Service Layer를 통해 연결한다.

## Phase 3 — Job System

파일 업로드 → Job 생성 → Worker 실행 → 상태 업데이트

## Phase 4 — Validation

원본 / Markdown / Structure Tree를 동시에 볼 수 있는 검수 UI 구현

## Phase 5 — Editing

Heading / Block / Text 수정 기능 구현

## Phase 6 — Reparse / Export

수정 결과 저장 및 재파싱, Markdown/JSON Export

---

# 15. 디자인 방향

전체적인 느낌은 다음을 목표로 한다.

**"사내 개발자가 사용하는 전문적인 Document Processing Platform"**

피해야 할 것:

- Streamlit 느낌의 단순한 위젯 나열
- 지나치게 큰 버튼
- 과도한 색상
- 불필요한 장식
- 모바일 앱 같은 UI

원하는 느낌:

- 깔끔한 SaaS 관리자 UI
- 충분한 whitespace
- 좌측 Sidebar
- 카드 기반 KPI
- 명확한 Status Badge
- Data Table
- Split Pane
- Tree View
- Dialog
- Toast / Notification
- Dark mode는 추후 고려

색상은 과도하게 사용하지 않고 상태 표현에만 제한적으로 사용한다.

---

# 16. 반응형 / 멀티페이지

데스크톱 사용을 우선한다.

주 사용 환경:

- 사내 PC
- 내부망
- Chrome 기반 브라우저

모바일 최적화는 우선순위가 낮다.

페이지 간 이동 시 상태가 안정적으로 유지되어야 한다.

특히 Parsing Job이 실행 중인 상태에서 Validation 페이지로 이동해도 Job이 중단되지 않아야 한다.

---

# 17. 향후 확장 가능성

향후 다음 기능을 추가할 수 있도록 구조를 열어둔다.

- OCR
- Layout Detection
- LLM 기반 구조 보정
- 문서 비교
- Parser 성능 비교
- Parsing Quality Score
- Batch Parsing
- Parser별 통계
- 사용자별 작업 이력
- 문서 버전 관리
- 결과 다운로드
- Qdrant 등 Vector DB 적재
- RAG Pipeline 연동

하지만 현재 MVP에서는 위 기능을 전부 구현하지 않는다.

---

# 18. AI Builder에게 요구하는 구현 방식

이 프로젝트는 처음부터 모든 기능을 구현하려 하지 말고 **실행 가능한 UI를 먼저 만든다.**

첫 번째 목표:

1. Reflex 앱 실행
2. 전문적인 Sidebar UI
3. Dashboard
4. Documents 페이지
5. Parsing Jobs 페이지
6. Validation 페이지의 기본 Split View
7. Mock Data로 전체 UI 확인

그 다음 실제 Parser와 연결한다.

**중요:** 기존 Parser 로직을 임의로 재작성하지 말고, 기존 프로젝트의 구조와 코드를 먼저 파악한 후 Service Layer를 통해 연결한다.

현재 목표는 단순한 Streamlit UI 복제가 아니다.

**최종 목표는 내부망에서 실제 업무자가 문서를 업로드하고, 파싱 작업을 실행하고, 다른 문서를 동시에 검수하고, 파싱 결과의 구조를 수정할 수 있는 Document Parsing Platform이다.**
