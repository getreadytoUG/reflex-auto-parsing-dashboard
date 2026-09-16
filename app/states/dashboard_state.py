from typing import TypedDict

import reflex as rx
import reflex_xy


class KpiItem(TypedDict):
    label: str
    value: str
    unit: str
    delta: str
    trend: str
    icon: str


class JobRow(TypedDict):
    id: str
    file_name: str
    file_type: str
    parser: str
    pages: str
    duration: str
    requester: str
    started_at: str
    status: str


class DashboardState(rx.State):
    kpis: list[KpiItem] = [
        {
            "label": "전체 문서",
            "value": "12,486",
            "unit": "건",
            "delta": "+184",
            "trend": "up",
            "icon": "files",
        },
        {
            "label": "파싱 성공",
            "value": "11,032",
            "unit": "건",
            "delta": "88.4%",
            "trend": "up",
            "icon": "circle-check",
        },
        {
            "label": "Warning",
            "value": "874",
            "unit": "건",
            "delta": "+37",
            "trend": "up",
            "icon": "triangle-alert",
        },
        {
            "label": "Failed",
            "value": "312",
            "unit": "건",
            "delta": "-12",
            "trend": "down",
            "icon": "circle-x",
        },
        {
            "label": "검수 필요",
            "value": "268",
            "unit": "건",
            "delta": "+21",
            "trend": "up",
            "icon": "clipboard-check",
        },
        {
            "label": "평균 파싱 시간",
            "value": "42.6",
            "unit": "초/문서",
            "delta": "-3.1초",
            "trend": "down",
            "icon": "timer",
        },
    ]

    file_types: list[str] = [
        "PDF",
        "HWP",
        "HWPX",
        "DOCX",
        "XLSX",
        "PPTX",
        "이미지",
    ]
    file_type_counts: list[int] = [5820, 2410, 1180, 1345, 842, 496, 393]

    parsers: list[str] = [
        "PdfPlumber",
        "PyMuPDF",
        "HwpAdapter",
        "DocxAdapter",
        "OCR-Tesseract",
        "TableFormer",
    ]
    parser_throughput: list[int] = [3120, 2480, 2110, 1360, 940, 620]

    recent_jobs: list[JobRow] = [
        {
            "id": "JOB-24713",
            "file_name": "2024년_국가연구개발사업_예산배분안.pdf",
            "file_type": "PDF",
            "parser": "PyMuPDF",
            "pages": "128 p",
            "duration": "1분 12초",
            "requester": "김서연",
            "started_at": "10:42",
            "status": "Completed",
        },
        {
            "id": "JOB-24712",
            "file_name": "행정정보_공동이용_협약서_최종본.hwp",
            "file_type": "HWP",
            "parser": "HwpAdapter",
            "pages": "34 p",
            "duration": "38초",
            "requester": "이준호",
            "started_at": "10:39",
            "status": "Parsing",
        },
        {
            "id": "JOB-24711",
            "file_name": "3분기_내부감사_결과보고서_v3.docx",
            "file_type": "DOCX",
            "parser": "DocxAdapter",
            "pages": "22 p",
            "duration": "19초",
            "requester": "박민정",
            "started_at": "10:35",
            "status": "Warning",
        },
        {
            "id": "JOB-24710",
            "file_name": "지방자치단체_보조금_집행내역.xlsx",
            "file_type": "XLSX",
            "parser": "TableFormer",
            "pages": "58 sheet",
            "duration": "1분 47초",
            "requester": "최도윤",
            "started_at": "10:31",
            "status": "Completed",
        },
        {
            "id": "JOB-24709",
            "file_name": "정보시스템_구축_제안요청서(RFP).pdf",
            "file_type": "PDF",
            "parser": "PdfPlumber",
            "pages": "212 p",
            "duration": "—",
            "requester": "정하늘",
            "started_at": "10:28",
            "status": "Queued",
        },
        {
            "id": "JOB-24708",
            "file_name": "민원처리_표준매뉴얼_스캔본.pdf",
            "file_type": "이미지",
            "parser": "OCR-Tesseract",
            "pages": "76 p",
            "duration": "4분 03초",
            "requester": "오세진",
            "started_at": "10:21",
            "status": "Failed",
        },
        {
            "id": "JOB-24707",
            "file_name": "부서별_인사발령_공고문_2024-09.hwpx",
            "file_type": "HWPX",
            "parser": "HwpAdapter",
            "pages": "12 p",
            "duration": "11초",
            "requester": "한지원",
            "started_at": "10:14",
            "status": "Completed",
        },
        {
            "id": "JOB-24706",
            "file_name": "클라우드_전환_사업_착수보고.pptx",
            "file_type": "PPTX",
            "parser": "DocxAdapter",
            "pages": "45 p",
            "duration": "—",
            "requester": "서지훈",
            "started_at": "10:02",
            "status": "Cancelled",
        },
        {
            "id": "JOB-24705",
            "file_name": "개인정보_영향평가_결과서_요약.pdf",
            "file_type": "PDF",
            "parser": "PyMuPDF",
            "pages": "63 p",
            "duration": "52초",
            "requester": "김서연",
            "started_at": "09:58",
            "status": "Warning",
        },
        {
            "id": "JOB-24704",
            "file_name": "전자문서_보존기간_기준표.xlsx",
            "file_type": "XLSX",
            "parser": "TableFormer",
            "pages": "9 sheet",
            "duration": "14초",
            "requester": "이준호",
            "started_at": "09:51",
            "status": "Completed",
        },
    ]

    queue_stages: list[tuple[str, str, int]] = [
        ("수집 대기", "Ingest", 42),
        ("파서 처리", "Parse", 18),
        ("구조 분석", "Structure", 11),
        ("검수 대기", "Review", 268),
    ]

    @reflex_xy.data
    def file_type_data(self) -> dict[str, list[str] | list[int]]:
        return {"file_type": self.file_types, "count": self.file_type_counts}

    @reflex_xy.data
    def parser_data(self) -> dict[str, list[str] | list[int]]:
        return {"parser": self.parsers, "documents": self.parser_throughput}
