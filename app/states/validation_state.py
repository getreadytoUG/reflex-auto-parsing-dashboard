from typing import TypedDict

import reflex as rx

from app.parsers.contracts import BlockKind
from app.services import jobs_service, qdrant_service


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


class InspectorField(TypedDict):
    label: str
    value: str


class ValidationState(rx.State):
    """Validation 페이지 상태. 문서 선택/탭 전환/블록 조회는 Qdrant CHILD_COLLECTION에서 실제로 조회한다."""

    document_options: list[str] = []
    review_states: list[str] = ["검수 중", "검수 대기", "검수 완료", "반송"]

    document_id: str = ""
    document_name: str = ""
    parser_name: str = ""
    parsed_at: str = ""
    reviewer: str = ""
    review_state: str = ""
    change_count: int = 0
    unsaved_changes: bool = False

    tabs: list[str] = ["Markdown", "JSON", "Blocks", "Tables"]
    active_tab: str = "Markdown"

    markdown_lines: list[CodeLine] = []
    json_lines: list[CodeLine] = []
    blocks: list[BlockItem] = []
    tables: list[TableItem] = []
    heading_tree: list[HeadingItem] = []

    table_preview_header: list[str] = ["분야", "2023", "2024", "증감률"]
    table_preview_rows: list[list[str]] = [
        ["전략기술", "24,180", "29,640", "+22.6"],
        ["공공보건", "9,420", "10,110", "+7.3"],
        ["탄소중립", "11,650", "13,020", "+11.8"],
        ["기초연구", "26,300", "27,140", "+3.2"],
    ]

    selected_block_id: str = ""
    selected_block_text: str = ""
    inspector_fields: list[InspectorField] = []

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

    validation_loading: bool = True
    validation_error: str = ""
    reparse_error: str = ""

    @rx.event
    async def load_validation_document(self, document_id: str):
        """document_id는 항상 호출부(select_document, 이후 Part B의 reparse 완료 후
        재조회 등)가 명시적으로 넘긴다 — 이 함수 자체는 "어떤 문서가 기본값인지"를
        판단하지 않는다 (그 판단은 on_page_load가 담당)."""
        self.validation_loading = True
        self.validation_error = ""
        try:
            chunks = await qdrant_service.fetch_document_chunks(document_id)
            self.document_id = document_id
            self.markdown_lines = _chunks_to_markdown_lines(chunks)
            self.json_lines = _chunks_to_json_lines(chunks)
            self.blocks = _chunks_to_blocks(chunks)
            self.tables = _chunks_to_tables(chunks)
            self.heading_tree = _chunks_to_heading_tree(chunks)
            self.selected_block_id = ""
            self.selected_block_text = ""
            self.inspector_fields = []
        except Exception as e:
            self.validation_error = f"문서 구조를 불러오지 못했습니다: {e}"
        finally:
            self.validation_loading = False

    @rx.event
    async def select_document(self, value: str):
        # value는 "DOC-100482 · 파일명" 형태 — "·" 앞부분이 document_id
        document_id = value.split(" · ")[0].strip()
        self.document_name = value.split(" · ", 1)[1] if " · " in value else value
        await self.load_validation_document(document_id)

    @rx.event
    def set_active_tab(self, tab: str):
        self.active_tab = tab

    @rx.event
    def select_block(self, block: BlockItem):
        self.selected_block_id = block["block_id"]
        self.selected_block_text = block["excerpt"]
        self.inspector_fields = _block_to_inspector_fields(block)

    @rx.event
    def select_heading(self, heading: HeadingItem):
        self.selected_block_id = heading["block_id"]
        self.selected_block_text = heading["text"]
        self.inspector_fields = [
            {"label": "Block ID", "value": heading["block_id"]},
            {"label": "Kind", "value": "heading"},
            {"label": "Level", "value": str(heading["level"])},
            {"label": "Page", "value": heading["page"]},
        ]

    @rx.event
    async def submit_reparse(self):
        self.reparse_error = ""
        try:
            await jobs_service.submit_reparse_job(self.document_id, self.parser_name)
        except NotImplementedError as e:
            self.reparse_error = str(e)

    @rx.event
    def download_markdown(self):
        content = "\n".join(line["text"] for line in self.markdown_lines)
        return rx.download(data=content, filename=f"{self.document_id}.md")

    @rx.event
    def download_json(self):
        content = "\n".join(line["text"] for line in self.json_lines)
        return rx.download(data=content, filename=f"{self.document_id}.json")

    @rx.event
    async def on_page_load(self):
        try:
            docs = await qdrant_service.fetch_documents(limit=100)
            self.document_options = [f"{d['id']} · {d['file_name']}" for d in docs]
        except Exception as e:
            self.validation_error = f"문서 목록을 불러오지 못했습니다: {e}"
            self.validation_loading = False
            return
        if self.document_options:
            await self.select_document(self.document_options[0])
        else:
            self.validation_loading = False


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
