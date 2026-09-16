from typing import TypedDict

import reflex as rx


class AdapterRow(TypedDict):
    display_format: str
    adapter: str
    engine: str
    version: str
    capability: str
    connection: str
    note: str


class ConfigRow(TypedDict):
    key: str
    value: str
    scope: str
    note: str


class RoadmapRow(TypedDict):
    current: str
    target: str
    stage: str
    note: str


class SettingsState(rx.State):
    """Settings 목업 전용 정적 상태."""

    adapters: list[AdapterRow] = [
        {
            "display_format": "PDF",
            "adapter": "PdfParserAdapter",
            "engine": "PyMuPDF / PdfPlumber",
            "version": "1.24.9",
            "capability": "텍스트 · 표 · 좌표",
            "connection": "연결 대기",
            "note": "ParserAdapter Protocol 구현체 미등록",
        },
        {
            "display_format": "HWP",
            "adapter": "HwpParserAdapter",
            "engine": "pyhwp (예정)",
            "version": "—",
            "capability": "텍스트 · 스타일",
            "connection": "연결 대기",
            "note": "바이너리 레코드 해석 모듈 연결 필요",
        },
        {
            "display_format": "HWPX",
            "adapter": "HwpxParserAdapter",
            "engine": "OWPML XML (예정)",
            "version": "—",
            "capability": "텍스트 · 표 · 개요 수준",
            "connection": "연결 대기",
            "note": "패키지 구조 매핑 규칙 확정 후 연결",
        },
        {
            "display_format": "DOCX",
            "adapter": "DocxParserAdapter",
            "engine": "python-docx (예정)",
            "version": "—",
            "capability": "텍스트 · 표 · 스타일 기반 Heading",
            "connection": "연결 대기",
            "note": "스타일 → Heading level 매핑표 필요",
        },
        {
            "display_format": "PPTX",
            "adapter": "PptxParserAdapter",
            "engine": "python-pptx (예정)",
            "version": "—",
            "capability": "슬라이드 텍스트 · 노트",
            "connection": "연결 대기",
            "note": "슬라이드 단위를 page 로 환산",
        },
    ]

    worker_config: list[ConfigRow] = [
        {
            "key": "실행 방식",
            "value": "In-process (동기)",
            "scope": "초기 구성",
            "note": "Reflex 이벤트 루프 내 처리",
        },
        {
            "key": "동시 실행 수",
            "value": "2",
            "scope": "초기 구성",
            "note": "CPU 코어 수 이하 권장",
        },
        {
            "key": "큐 백엔드",
            "value": "메모리 큐",
            "scope": "초기 구성",
            "note": "프로세스 재시작 시 소실",
        },
        {
            "key": "Job 타임아웃",
            "value": "900초",
            "scope": "초기 구성",
            "note": "초과 시 Failed 처리",
        },
        {
            "key": "재시도 정책",
            "value": "최대 2회 · 지수 backoff",
            "scope": "초기 구성",
            "note": "OCR fallback 은 1회",
        },
        {
            "key": "진행률 폴링 주기",
            "value": "3초",
            "scope": "초기 구성",
            "note": "ProgressSnapshot 조회 간격",
        },
    ]

    storage_config: list[ConfigRow] = [
        {
            "key": "메타데이터 저장소",
            "value": "SQLite (docparse.db)",
            "scope": "초기 구성",
            "note": "단일 파일 · 로컬 트랜잭션",
        },
        {
            "key": "원본 저장소",
            "value": "Local File System",
            "scope": "초기 구성",
            "note": "/srv/docparse/originals",
        },
        {
            "key": "결과 저장 경로",
            "value": "/srv/docparse/results/{doc_id}",
            "scope": "초기 구성",
            "note": "Markdown · JSON 동시 저장",
        },
        {
            "key": "Export 형식",
            "value": "Markdown · JSON",
            "scope": "초기 구성",
            "note": "Blocks JSON 은 스키마 v1",
        },
        {
            "key": "보존 기간",
            "value": "원본 5년 · 결과 3년",
            "scope": "정책",
            "note": "전자문서 보존기간 기준표 준용",
        },
        {
            "key": "외부 전송",
            "value": "차단",
            "scope": "정책",
            "note": "내부망 전용 · 프록시 미허용",
        },
    ]

    roadmap: list[RoadmapRow] = [
        {
            "current": "SQLite",
            "target": "PostgreSQL",
            "stage": "확장 예정",
            "note": "동시 검수 사용자 증가 시 전환 · 스키마 마이그레이션 준비",
        },
        {
            "current": "In-process 처리",
            "target": "Worker Service",
            "stage": "확장 예정",
            "note": "ParsingService 계약 유지한 채 별도 프로세스로 분리",
        },
        {
            "current": "메모리 큐",
            "target": "Redis Queue",
            "stage": "확장 예정",
            "note": "재시작 내구성 · 다중 Worker 분배",
        },
        {
            "current": "Local File System",
            "target": "객체 스토리지 (내부망 S3 호환)",
            "stage": "검토",
            "note": "대용량 스캔 PDF 누적 시 검토",
        },
    ]

    contract_items: list[ConfigRow] = [
        {
            "key": "DocumentInput",
            "value": "문서 입력 명세",
            "scope": "typed data",
            "note": "document_id · source_uri · format · byte_size",
        },
        {
            "key": "JobSubmission",
            "value": "job 제출 영수증",
            "scope": "typed data",
            "note": "job_id · parser_name · status",
        },
        {
            "key": "ProgressSnapshot",
            "value": "진행 스냅샷",
            "scope": "typed data",
            "note": "stage · progress_percent · page",
        },
        {
            "key": "ParseResult",
            "value": "파싱 산출물",
            "scope": "typed data",
            "note": "blocks · heading_tree · markdown",
        },
        {
            "key": "ParserAdapter",
            "value": "형식별 Parser 계약",
            "scope": "Protocol",
            "note": "supported_formats · can_handle · parse",
        },
        {
            "key": "ParsingService",
            "value": "오케스트레이션 계약",
            "scope": "Protocol",
            "note": "submit · progress · result · cancel",
        },
        {
            "key": "ParserRegistry",
            "value": "Adapter 등록 계약",
            "scope": "Protocol",
            "note": "register · adapters · resolve",
        },
    ]
