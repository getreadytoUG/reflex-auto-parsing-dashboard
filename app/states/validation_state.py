from typing import TypedDict

import reflex as rx

from app.parsers.contracts import BlockKind


class CodeLine(TypedDict):
    no: str
    text: str
    indent: str
    kind: str
    selected: bool


class HeadingItem(TypedDict):
    block_id: str
    level: int
    text: str
    page: str
    status: str
    selected: bool


class BlockItem(TypedDict):
    block_id: str
    kind: str
    label: str
    excerpt: str
    page: str
    order: str
    confidence: str
    selected: bool


class TableItem(TypedDict):
    block_id: str
    caption: str
    size: str
    page: str
    status: str


class ViewerLine(TypedDict):
    text: str
    style: str


class InspectorField(TypedDict):
    label: str
    value: str


class ValidationState(rx.State):
    """Validation 목업 전용 정적 상태 (이벤트 연결 없음)."""

    document_options: list[str] = [
        "DOC-100482 · 2024년_국가연구개발사업_예산배분안.pdf",
        "DOC-100478 · 부서별_인사발령_공고문_2024-09.hwpx",
        "DOC-100474 · 전자문서_보존기간_기준표_개정안.docx",
        "DOC-100471 · 차세대_행정포털_요구사항_정의서.pptx",
    ]
    review_states: list[str] = ["검수 중", "검수 대기", "검수 완료", "반송"]

    document_id: str = "DOC-100482"
    document_name: str = "2024년_국가연구개발사업_예산배분안.pdf"
    parser_name: str = "PyMuPDF 1.24.9"
    parsed_at: str = "2024-09-18 10:42"
    reviewer: str = "김서연 · 문서운영팀"
    review_state: str = "검수 중"
    change_count: int = 7
    unsaved_changes: bool = True

    current_page: int = 12
    total_pages: int = 48
    zoom_label: str = "120%"

    tabs: list[str] = ["Markdown", "JSON", "Blocks", "Tables"]
    active_tab: str = "Markdown"

    viewer_header: str = "국가연구개발사업 예산배분·조정 지침"
    viewer_lines: list[ViewerLine] = [
        {"text": "제3장 예산배분의 기준", "style": "h1"},
        {
            "text": "제12조(배분 원칙) ① 중앙행정기관의 장은 소관 연구개발사업의 예산을 배분할 때 국가과학기술자문회의의 심의 결과와 사업 성과평가 결과를 우선 반영하여야 한다.",
            "style": "body",
        },
        {
            "text": "② 제1항에 따른 배분 결과는 사업별 투자 우선순위, 계속과제의 이행 상황, 신규과제의 기획 완성도를 종합하여 조정한다.",
            "style": "body",
        },
        {"text": "제13조(중점 투자 분야)", "style": "h2"},
        {
            "text": "① 중점 투자 분야는 다음 각 호와 같다.",
            "style": "body",
        },
        {"text": "1. 인공지능·반도체 등 전략기술 분야", "style": "list"},
        {"text": "2. 감염병 대응 및 공공보건 연구 분야", "style": "list"},
        {"text": "3. 탄소중립 이행 기반 기술 분야", "style": "list"},
        {
            "text": "② 중점 투자 분야의 투자 규모는 전년도 본예산 대비 증감률을 명시하여 별표 4에 따라 산정한다.",
            "style": "body",
        },
        {
            "text": "[표 3] 분야별 투자 증감률 (단위: 억원, %)",
            "style": "caption",
        },
        {
            "text": "제14조(조정 절차) 예산 조정이 필요한 경우 관계 기관 협의를 거쳐 조정안을 작성하고, 조정 사유와 근거 자료를 첨부하여 심의에 부친다.",
            "style": "body",
        },
        {
            "text": "— 12 —",
            "style": "footer",
        },
    ]

    markdown_lines: list[CodeLine] = [
        {
            "no": "041",
            "text": "## 제3장 예산배분의 기준",
            "indent": "0",
            "kind": "heading",
            "selected": False,
        },
        {
            "no": "042",
            "text": "",
            "indent": "0",
            "kind": "blank",
            "selected": False,
        },
        {
            "no": "043",
            "text": "### 제12조(배분 원칙)",
            "indent": "0",
            "kind": "heading",
            "selected": False,
        },
        {
            "no": "044",
            "text": "① 중앙행정기관의 장은 소관 연구개발사업의 예산을 배분할 때 국가과학기술자문회의의",
            "indent": "0",
            "kind": "text",
            "selected": False,
        },
        {
            "no": "045",
            "text": "심의 결과와 사업 성과평가 결과를 우선 반영하여야 한다.",
            "indent": "0",
            "kind": "text",
            "selected": False,
        },
        {
            "no": "046",
            "text": "",
            "indent": "0",
            "kind": "blank",
            "selected": False,
        },
        {
            "no": "047",
            "text": "### 제13조(중점 투자 분야)",
            "indent": "0",
            "kind": "heading",
            "selected": True,
        },
        {
            "no": "048",
            "text": "① 중점 투자 분야는 다음 각 호와 같다.",
            "indent": "0",
            "kind": "text",
            "selected": True,
        },
        {
            "no": "049",
            "text": "1. 인공지능·반도체 등 전략기술 분야",
            "indent": "1",
            "kind": "list",
            "selected": True,
        },
        {
            "no": "050",
            "text": "2. 감염병 대응 및 공공보건 연구 분야",
            "indent": "1",
            "kind": "list",
            "selected": True,
        },
        {
            "no": "051",
            "text": "3. 탄소중립 이행 기반 기술 분야",
            "indent": "1",
            "kind": "list",
            "selected": True,
        },
        {
            "no": "052",
            "text": "",
            "indent": "0",
            "kind": "blank",
            "selected": False,
        },
        {
            "no": "053",
            "text": "**[표 3] 분야별 투자 증감률 (단위: 억원, %)**",
            "indent": "0",
            "kind": "caption",
            "selected": False,
        },
        {
            "no": "054",
            "text": "| 분야 | 2023 | 2024 | 증감률 |",
            "indent": "0",
            "kind": "table",
            "selected": False,
        },
        {
            "no": "055",
            "text": "| --- | ---: | ---: | ---: |",
            "indent": "0",
            "kind": "table",
            "selected": False,
        },
        {
            "no": "056",
            "text": "| 전략기술 | 24,180 | 29,640 | +22.6 |",
            "indent": "0",
            "kind": "table",
            "selected": False,
        },
        {
            "no": "057",
            "text": "| 공공보건 | 9,420 | 10,110 | +7.3 |",
            "indent": "0",
            "kind": "table",
            "selected": False,
        },
        {
            "no": "058",
            "text": "",
            "indent": "0",
            "kind": "blank",
            "selected": False,
        },
        {
            "no": "059",
            "text": "### 제14조(조정 절차)",
            "indent": "0",
            "kind": "heading",
            "selected": False,
        },
        {
            "no": "060",
            "text": "예산 조정이 필요한 경우 관계 기관 협의를 거쳐 조정안을 작성한다.",
            "indent": "0",
            "kind": "text",
            "selected": False,
        },
    ]

    json_lines: list[CodeLine] = [
        {
            "no": "118",
            "text": "{",
            "indent": "0",
            "kind": "punct",
            "selected": False,
        },
        {
            "no": "119",
            "text": '"block_id": "BLK-0473",',
            "indent": "1",
            "kind": "key",
            "selected": True,
        },
        {
            "no": "120",
            "text": '"kind": "heading",',
            "indent": "1",
            "kind": "key",
            "selected": True,
        },
        {
            "no": "121",
            "text": '"heading_level": 3,',
            "indent": "1",
            "kind": "key",
            "selected": True,
        },
        {
            "no": "122",
            "text": '"page": 12,',
            "indent": "1",
            "kind": "key",
            "selected": True,
        },
        {
            "no": "123",
            "text": '"order": 473,',
            "indent": "1",
            "kind": "key",
            "selected": True,
        },
        {
            "no": "124",
            "text": '"text": "제13조(중점 투자 분야)",',
            "indent": "1",
            "kind": "key",
            "selected": True,
        },
        {
            "no": "125",
            "text": '"bbox": [72.0, 318.4, 523.6, 336.1],',
            "indent": "1",
            "kind": "key",
            "selected": False,
        },
        {
            "no": "126",
            "text": '"confidence": 0.91,',
            "indent": "1",
            "kind": "key",
            "selected": False,
        },
        {
            "no": "127",
            "text": '"parent_block_id": "BLK-0461"',
            "indent": "1",
            "kind": "key",
            "selected": False,
        },
        {
            "no": "128",
            "text": "},",
            "indent": "0",
            "kind": "punct",
            "selected": False,
        },
        {
            "no": "129",
            "text": "{",
            "indent": "0",
            "kind": "punct",
            "selected": False,
        },
        {
            "no": "130",
            "text": '"block_id": "BLK-0474",',
            "indent": "1",
            "kind": "key",
            "selected": False,
        },
        {
            "no": "131",
            "text": '"kind": "list",',
            "indent": "1",
            "kind": "key",
            "selected": False,
        },
        {
            "no": "132",
            "text": '"page": 12,',
            "indent": "1",
            "kind": "key",
            "selected": False,
        },
        {
            "no": "133",
            "text": '"items": ["인공지능·반도체", "공공보건", "탄소중립"]',
            "indent": "1",
            "kind": "key",
            "selected": False,
        },
        {
            "no": "134",
            "text": "}",
            "indent": "0",
            "kind": "punct",
            "selected": False,
        },
    ]

    blocks: list[BlockItem] = [
        {
            "block_id": "BLK-0461",
            "kind": "heading",
            "label": "H2",
            "excerpt": "제3장 예산배분의 기준",
            "page": "p.11",
            "order": "#461",
            "confidence": "0.98",
            "selected": False,
        },
        {
            "block_id": "BLK-0468",
            "kind": "heading",
            "label": "H3",
            "excerpt": "제12조(배분 원칙)",
            "page": "p.11",
            "order": "#468",
            "confidence": "0.96",
            "selected": False,
        },
        {
            "block_id": "BLK-0470",
            "kind": "paragraph",
            "label": "P",
            "excerpt": "① 중앙행정기관의 장은 소관 연구개발사업의 예산을 배분할 때 …",
            "page": "p.12",
            "order": "#470",
            "confidence": "0.99",
            "selected": False,
        },
        {
            "block_id": "BLK-0473",
            "kind": "heading",
            "label": "H3",
            "excerpt": "제13조(중점 투자 분야)",
            "page": "p.12",
            "order": "#473",
            "confidence": "0.91",
            "selected": True,
        },
        {
            "block_id": "BLK-0474",
            "kind": "list",
            "label": "LIST",
            "excerpt": "1. 인공지능·반도체 등 전략기술 분야 · 2. 감염병 대응 …",
            "page": "p.12",
            "order": "#474",
            "confidence": "0.88",
            "selected": False,
        },
        {
            "block_id": "BLK-0476",
            "kind": "table",
            "label": "TABLE",
            "excerpt": "[표 3] 분야별 투자 증감률",
            "page": "p.12",
            "order": "#476",
            "confidence": "0.74",
            "selected": False,
        },
        {
            "block_id": "BLK-0479",
            "kind": "paragraph",
            "label": "P",
            "excerpt": "제14조(조정 절차) 예산 조정이 필요한 경우 관계 기관 협의를 …",
            "page": "p.13",
            "order": "#479",
            "confidence": "0.97",
            "selected": False,
        },
    ]

    tables: list[TableItem] = [
        {
            "block_id": "BLK-0476",
            "caption": "[표 3] 분야별 투자 증감률",
            "size": "4열 × 6행",
            "page": "p.12",
            "status": "Warning",
        },
        {
            "block_id": "BLK-0491",
            "caption": "[표 4] 계속과제 이행 현황",
            "size": "6열 × 14행",
            "page": "p.15",
            "status": "Completed",
        },
        {
            "block_id": "BLK-0512",
            "caption": "[표 5] 기관별 배분 총액",
            "size": "5열 × 21행",
            "page": "p.19",
            "status": "Completed",
        },
    ]

    table_preview_header: list[str] = ["분야", "2023", "2024", "증감률"]
    table_preview_rows: list[list[str]] = [
        ["전략기술", "24,180", "29,640", "+22.6"],
        ["공공보건", "9,420", "10,110", "+7.3"],
        ["탄소중립", "11,650", "13,020", "+11.8"],
        ["기초연구", "26,300", "27,140", "+3.2"],
    ]

    heading_tree: list[HeadingItem] = [
        {
            "block_id": "BLK-0102",
            "level": 1,
            "text": "국가연구개발사업 예산배분·조정 지침",
            "page": "p.1",
            "status": "확정",
            "selected": False,
        },
        {
            "block_id": "BLK-0118",
            "level": 2,
            "text": "제1장 총칙",
            "page": "p.2",
            "status": "확정",
            "selected": False,
        },
        {
            "block_id": "BLK-0121",
            "level": 3,
            "text": "제1조(목적)",
            "page": "p.2",
            "status": "확정",
            "selected": False,
        },
        {
            "block_id": "BLK-0126",
            "level": 3,
            "text": "제2조(정의)",
            "page": "p.3",
            "status": "확정",
            "selected": False,
        },
        {
            "block_id": "BLK-0301",
            "level": 2,
            "text": "제2장 사업 기획",
            "page": "p.6",
            "status": "확정",
            "selected": False,
        },
        {
            "block_id": "BLK-0308",
            "level": 3,
            "text": "제7조(기획 절차)",
            "page": "p.6",
            "status": "수정",
            "selected": False,
        },
        {
            "block_id": "BLK-0461",
            "level": 2,
            "text": "제3장 예산배분의 기준",
            "page": "p.11",
            "status": "확정",
            "selected": False,
        },
        {
            "block_id": "BLK-0468",
            "level": 3,
            "text": "제12조(배분 원칙)",
            "page": "p.11",
            "status": "확정",
            "selected": False,
        },
        {
            "block_id": "BLK-0473",
            "level": 3,
            "text": "제13조(중점 투자 분야)",
            "page": "p.12",
            "status": "검토",
            "selected": True,
        },
        {
            "block_id": "BLK-0479",
            "level": 3,
            "text": "제14조(조정 절차)",
            "page": "p.13",
            "status": "확정",
            "selected": False,
        },
        {
            "block_id": "BLK-0530",
            "level": 2,
            "text": "제4장 성과 평가",
            "page": "p.21",
            "status": "확정",
            "selected": False,
        },
        {
            "block_id": "BLK-0534",
            "level": 3,
            "text": "제18조(평가 지표)",
            "page": "p.21",
            "status": "수정",
            "selected": False,
        },
        {
            "block_id": "BLK-0602",
            "level": 2,
            "text": "부칙",
            "page": "p.44",
            "status": "확정",
            "selected": False,
        },
    ]

    selected_block_id: str = "BLK-0473"
    selected_block_text: str = "제13조(중점 투자 분야)"
    inspector_fields: list[InspectorField] = [
        {"label": "Block ID", "value": "BLK-0473"},
        {"label": "Kind", "value": "heading"},
        {"label": "Heading Level", "value": "H3"},
        {"label": "Page / Order", "value": "12 / #473"},
        {"label": "Parent", "value": "BLK-0461 (H2)"},
        {"label": "BBox", "value": "72.0, 318.4, 523.6, 336.1"},
        {"label": "Confidence", "value": "0.91"},
        {"label": "Source Parser", "value": "PyMuPDF · text-span"},
    ]
    heading_levels: list[str] = ["H1", "H2", "H3", "H4", "본문(P)"]
    block_kinds: list[str] = [
        "heading",
        "paragraph",
        "list",
        "table",
        "caption",
        "footnote",
    ]

    change_log: list[str] = [
        "BLK-0308 · H2 → H3 수준 변경",
        "BLK-0470 · 문단 병합 (2건 → 1건)",
        "BLK-0476 · Table 로 지정",
        "BLK-0534 · 본문 → Heading 승격",
        "BLK-0491 · 표 헤더 행 재지정",
        "BLK-0512 · 셀 병합 해제",
        "BLK-0602 · 순서 1칸 위로 이동",
    ]

    warnings: list[str] = [
        "p.12 [표 3] 열 정렬 신뢰도 0.74 — 헤더 행 확인 필요",
        "p.27 각주 3건이 본문 문단으로 인식됨",
    ]

    @rx.var
    def page_label(self) -> str:
        return f"{self.current_page} / {self.total_pages}"


def _normalize_kind(raw_kind: str) -> str:
    """알 수 없는 kind 값은 BlockKind.UNKNOWN에 대응하는 값으로 방어적으로 처리한다."""
    try:
        return BlockKind(raw_kind).value
    except ValueError:
        return BlockKind.UNKNOWN.value


def _chunks_to_markdown_lines(chunks: list[dict]) -> list[CodeLine]:
    """청크들을 이어 붙인 뒤 줄 단위로 잘라 번호를 매긴다."""
    lines: list[CodeLine] = []
    line_no = 1
    kind_to_style = {
        BlockKind.HEADING.value: "h1",  # level별 h1/h2 구분은 Part B에서 다듬을 여지 있음 — 지금은 heading을 전부 h1으로 표시
        BlockKind.PARAGRAPH.value: "body",
        BlockKind.LIST.value: "list",
        BlockKind.TABLE.value: "table",
        BlockKind.CAPTION.value: "body",
        BlockKind.FOOTNOTE.value: "body",
        BlockKind.UNKNOWN.value: "body",
    }
    for chunk in chunks:
        kind = _normalize_kind(chunk["kind"])
        for text_line in str(chunk["text"]).splitlines() or [""]:
            lines.append(
                {
                    "no": f"{line_no:03d}",
                    "text": text_line,
                    "indent": "",
                    "kind": kind_to_style.get(kind, "body"),
                    "selected": False,
                }
            )
            line_no += 1
        lines.append({"no": f"{line_no:03d}", "text": "", "indent": "", "kind": "blank", "selected": False})
        line_no += 1
    return lines


def _chunks_to_json_lines(chunks: list[dict]) -> list[CodeLine]:
    """청크 리스트 전체를 pretty-print된 JSON 텍스트로 만들고 줄 단위로 자른다."""
    import json

    if not chunks:
        return []

    text = json.dumps(chunks, ensure_ascii=False, indent=2)
    return [
        {"no": f"{i + 1:03d}", "text": line, "indent": "", "kind": "json", "selected": False}
        for i, line in enumerate(text.splitlines())
    ]


def _chunks_to_blocks(chunks: list[dict]) -> list[BlockItem]:
    return [
        {
            "block_id": c["block_id"],
            "kind": _normalize_kind(c["kind"]),
            "label": _normalize_kind(c["kind"]).capitalize(),
            "excerpt": str(c["text"])[:80],
            "page": str(c["page"]),
            "order": str(c["order"]),
            "confidence": str(c["confidence"]),
            "selected": False,
        }
        for c in chunks
    ]


def _chunks_to_tables(chunks: list[dict]) -> list[TableItem]:
    return [
        {
            "block_id": c["block_id"],
            "caption": str(c["text"])[:40] or "(제목 없음)",
            "size": "-",  # 표 행/열 크기는 payload에 없으므로 플레이스홀더 — 실제 스키마 확인 시 채움
            "page": str(c["page"]),
            "status": "Completed",
        }
        for c in chunks
        if _normalize_kind(c["kind"]) == BlockKind.TABLE.value
    ]


def _chunks_to_heading_tree(chunks: list[dict]) -> list[HeadingItem]:
    return [
        {
            "block_id": c["block_id"],
            "level": int(c["level"]) if str(c["level"]).isdigit() else 1,
            "text": str(c["text"])[:80],
            "page": str(c["page"]),
            "status": "확정",  # 실제 검수 상태 필드가 CHILD_COLLECTION에 있는지 불명 — 있으면 매핑 교체
            "selected": False,
        }
        for c in chunks
        if _normalize_kind(c["kind"]) == BlockKind.HEADING.value
    ]


def _block_to_inspector_fields(block: BlockItem) -> list[InspectorField]:
    return [
        {"label": "Block ID", "value": block["block_id"]},
        {"label": "Kind", "value": block["kind"]},
        {"label": "Page", "value": block["page"]},
        {"label": "Order", "value": block["order"]},
        {"label": "Confidence", "value": block["confidence"]},
    ]
