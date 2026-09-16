"""Parser 연결 계약 경계 (구현체 없음).

이 모듈은 향후 실제 Parser(PyMuPDF, HWP, DOCX, PPTX 등)를 연결할 때 사용할
타입 계약만 정의한다. UI, 상태(rx.State), 가짜 Parser 구현과 결합하지 않으며
Reflex를 import 하지 않는다.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum
from typing import Protocol, runtime_checkable


class DocumentFormat(StrEnum):
    """Adapter 가 선언할 수 있는 입력 문서 형식."""

    PDF = "pdf"
    HWP = "hwp"
    HWPX = "hwpx"
    DOCX = "docx"
    PPTX = "pptx"


class JobStatus(StrEnum):
    """Job 수명 주기 상태."""

    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    WARNING = "warning"
    FAILED = "failed"
    CANCELLED = "cancelled"


class BlockKind(StrEnum):
    """파싱 결과 block 의 의미 분류."""

    HEADING = "heading"
    PARAGRAPH = "paragraph"
    TABLE = "table"
    LIST = "list"
    CAPTION = "caption"
    FOOTNOTE = "footnote"
    UNKNOWN = "unknown"


@dataclass(frozen=True, slots=True)
class DocumentInput:
    """파싱 대상 문서 입력 명세."""

    document_id: str
    source_uri: str
    file_name: str
    document_format: DocumentFormat
    byte_size: int
    checksum_sha256: str = ""
    page_hint: int | None = None


@dataclass(frozen=True, slots=True)
class ParseOptions:
    """Adapter 동작 조정 옵션."""

    parser_name: str
    page_range: tuple[int, int] | None = None
    detect_tables: bool = True
    detect_headings: bool = True
    ocr_fallback: bool = False
    preserve_layout: bool = True
    max_workers: int = 1


@dataclass(frozen=True, slots=True)
class JobSubmission:
    """job 제출 결과 (수락 영수증)."""

    job_id: str
    document_id: str
    parser_name: str
    submitted_at: str
    status: JobStatus = JobStatus.QUEUED


@dataclass(frozen=True, slots=True)
class ProgressSnapshot:
    """진행 상황의 단일 시점 스냅샷."""

    job_id: str
    status: JobStatus
    stage: str
    progress_percent: int
    current_page: int
    total_pages: int
    started_at: str = ""
    finished_at: str = ""
    message: str = ""


@dataclass(frozen=True, slots=True)
class TableCell:
    row: int
    column: int
    text: str
    row_span: int = 1
    column_span: int = 1
    is_header: bool = False


@dataclass(frozen=True, slots=True)
class TableBlock:
    block_id: str
    rows: int
    columns: int
    cells: tuple[TableCell, ...] = ()
    caption: str = ""


@dataclass(frozen=True, slots=True)
class ContentBlock:
    """문서 본문의 최소 구조 단위."""

    block_id: str
    kind: BlockKind
    text: str
    page: int
    order: int
    heading_level: int | None = None
    parent_block_id: str | None = None
    bbox: tuple[float, float, float, float] | None = None
    confidence: float = 1.0
    table: TableBlock | None = None


@dataclass(frozen=True, slots=True)
class HeadingNode:
    block_id: str
    level: int
    text: str
    page: int
    children: tuple["HeadingNode", ...] = ()


@dataclass(frozen=True, slots=True)
class ParseResult:
    """파싱 산출물 전체."""

    job_id: str
    document_id: str
    parser_name: str
    blocks: tuple[ContentBlock, ...] = ()
    heading_tree: tuple[HeadingNode, ...] = ()
    markdown: str = ""
    warnings: tuple[str, ...] = ()
    metadata: dict[str, str] = field(default_factory=dict)


@runtime_checkable
class ParserAdapter(Protocol):
    """개별 형식 Parser 가 만족해야 하는 계약."""

    name: str

    def supported_formats(self) -> tuple[DocumentFormat, ...]: ...

    def can_handle(self, document: DocumentInput) -> bool: ...

    def parse(
        self, document: DocumentInput, options: ParseOptions
    ) -> ParseResult: ...


@runtime_checkable
class ParsingService(Protocol):
    """job 제출·조회·취소를 담당하는 오케스트레이션 계약."""

    def supported_formats(self) -> tuple[DocumentFormat, ...]: ...

    def submit(
        self, document: DocumentInput, options: ParseOptions
    ) -> JobSubmission: ...

    def progress(self, job_id: str) -> ProgressSnapshot: ...

    def result(self, job_id: str) -> ParseResult | None: ...

    def cancel(self, job_id: str) -> ProgressSnapshot: ...


@runtime_checkable
class ParserRegistry(Protocol):
    """Adapter 등록·조회 계약."""

    def register(self, adapter: ParserAdapter) -> None: ...

    def adapters(self) -> tuple[ParserAdapter, ...]: ...

    def resolve(
        self, document_format: DocumentFormat
    ) -> ParserAdapter | None: ...


__all__ = [
    "BlockKind",
    "ContentBlock",
    "DocumentFormat",
    "DocumentInput",
    "HeadingNode",
    "JobStatus",
    "JobSubmission",
    "ParseOptions",
    "ParseResult",
    "ParserAdapter",
    "ParserRegistry",
    "ParsingService",
    "ProgressSnapshot",
    "TableBlock",
    "TableCell",
]
