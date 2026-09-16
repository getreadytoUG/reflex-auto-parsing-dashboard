from typing import TypedDict

import reflex as rx


class JobSummary(TypedDict):
    label: str
    count: str
    icon: str


class ParsingJob(TypedDict):
    id: str
    file_name: str
    file_type: str
    parser: str
    status: str
    progress: int
    current_page: int
    total_pages: int
    stage: str
    started_at: str
    finished_at: str
    requester: str
    error: str
    output_path: str


class JobsState(rx.State):
    """작업 큐 목업 데이터 (실제 background task·timer 없음)."""

    auto_refresh_label: str = "5초 주기 (목업 · 실제 갱신 없음)"
    last_refreshed_at: str = "2024-09-18 10:43:12"
    next_refresh_at: str = "2024-09-18 10:43:17"

    summary: list[JobSummary] = [
        {"label": "Queued", "count": "42", "icon": "inbox"},
        {"label": "Running", "count": "6", "icon": "loader"},
        {"label": "Completed", "count": "11,032", "icon": "circle-check"},
        {"label": "Warning", "count": "874", "icon": "triangle-alert"},
        {"label": "Failed", "count": "312", "icon": "circle-x"},
        {"label": "Cancelled", "count": "128", "icon": "ban"},
    ]

    status_filters: list[str] = [
        "전체",
        "Queued",
        "Running",
        "Completed",
        "Warning",
        "Failed",
        "Cancelled",
    ]

    jobs: list[ParsingJob] = [
        {
            "id": "JOB-24713",
            "file_name": "2024년_국가연구개발사업_예산배분안.pdf",
            "file_type": "PDF",
            "parser": "PyMuPDF",
            "status": "Running",
            "progress": 72,
            "current_page": 92,
            "total_pages": 128,
            "stage": "3/5 · 표 구조 추출 (TableFormer 보정)",
            "started_at": "10:42:03",
            "finished_at": "—",
            "requester": "김서연",
            "error": "",
            "output_path": "/storage/parsed/2024/09/JOB-24713/ (생성 중)",
        },
        {
            "id": "JOB-24712",
            "file_name": "행정정보_공동이용_협약서_최종본.hwp",
            "file_type": "HWP",
            "parser": "HwpAdapter",
            "status": "Running",
            "progress": 37,
            "current_page": 13,
            "total_pages": 34,
            "stage": "2/5 · 본문 텍스트 블록 추출",
            "started_at": "10:39:41",
            "finished_at": "—",
            "requester": "이준호",
            "error": "",
            "output_path": "/storage/parsed/2024/09/JOB-24712/ (생성 중)",
        },
        {
            "id": "JOB-24711",
            "file_name": "3분기_내부감사_결과보고서_v3.docx",
            "file_type": "DOCX",
            "parser": "DocxAdapter",
            "status": "Warning",
            "progress": 100,
            "current_page": 22,
            "total_pages": 22,
            "stage": "5/5 · 완료 (구조 검수 권고)",
            "started_at": "10:35:12",
            "finished_at": "10:35:31",
            "requester": "박민정",
            "error": "머리글 레벨 추정 실패 3건 · 표 병합 셀 7건 미해석",
            "output_path": "/storage/parsed/2024/09/JOB-24711/result.md",
        },
        {
            "id": "JOB-24710",
            "file_name": "지방자치단체_보조금_집행내역.xlsx",
            "file_type": "XLSX",
            "parser": "TableFormer",
            "status": "Completed",
            "progress": 100,
            "current_page": 58,
            "total_pages": 58,
            "stage": "5/5 · 완료",
            "started_at": "10:31:08",
            "finished_at": "10:32:55",
            "requester": "최도윤",
            "error": "",
            "output_path": "/storage/parsed/2024/09/JOB-24710/result.json",
        },
        {
            "id": "JOB-24709",
            "file_name": "정보시스템_구축_제안요청서(RFP).pdf",
            "file_type": "PDF",
            "parser": "PdfPlumber",
            "status": "Queued",
            "progress": 0,
            "current_page": 0,
            "total_pages": 212,
            "stage": "0/5 · Worker 배정 대기 (대기열 4번째)",
            "started_at": "—",
            "finished_at": "—",
            "requester": "정하늘",
            "error": "",
            "output_path": "—",
        },
        {
            "id": "JOB-24708",
            "file_name": "민원처리_표준매뉴얼_스캔본.pdf",
            "file_type": "PDF",
            "parser": "OCR-Tesseract",
            "status": "Failed",
            "progress": 64,
            "current_page": 49,
            "total_pages": 76,
            "stage": "3/5 · OCR 처리 중 중단",
            "started_at": "10:21:44",
            "finished_at": "10:25:47",
            "requester": "오세진",
            "error": "TesseractError: 49p 이미지 해상도 부족(96dpi) · Worker 메모리 초과로 프로세스 종료",
            "output_path": "/storage/failed/2024/09/JOB-24708/partial.log",
        },
        {
            "id": "JOB-24707",
            "file_name": "부서별_인사발령_공고문_2024-09.hwpx",
            "file_type": "HWPX",
            "parser": "HwpAdapter",
            "status": "Completed",
            "progress": 100,
            "current_page": 12,
            "total_pages": 12,
            "stage": "5/5 · 완료",
            "started_at": "10:14:02",
            "finished_at": "10:14:13",
            "requester": "한지원",
            "error": "",
            "output_path": "/storage/parsed/2024/09/JOB-24707/result.md",
        },
        {
            "id": "JOB-24706",
            "file_name": "클라우드_전환_사업_착수보고.pptx",
            "file_type": "PPTX",
            "parser": "PptxAdapter",
            "status": "Cancelled",
            "progress": 18,
            "current_page": 8,
            "total_pages": 45,
            "stage": "1/5 · 요청자 취소",
            "started_at": "10:02:19",
            "finished_at": "10:03:02",
            "requester": "서지훈",
            "error": "사용자 취소 요청 (재업로드 예정)",
            "output_path": "—",
        },
        {
            "id": "JOB-24705",
            "file_name": "개인정보_영향평가_결과서_요약.pdf",
            "file_type": "PDF",
            "parser": "PyMuPDF",
            "status": "Warning",
            "progress": 100,
            "current_page": 63,
            "total_pages": 63,
            "stage": "5/5 · 완료 (경고 2건)",
            "started_at": "09:58:11",
            "finished_at": "09:59:03",
            "requester": "김서연",
            "error": "각주 링크 2건 손실 · 이미지 캡션 위치 추정 불확실",
            "output_path": "/storage/parsed/2024/09/JOB-24705/result.md",
        },
        {
            "id": "JOB-24704",
            "file_name": "차세대_행정포털_요구사항_정의서.pptx",
            "file_type": "PPTX",
            "parser": "PptxAdapter",
            "status": "Running",
            "progress": 91,
            "current_page": 66,
            "total_pages": 72,
            "stage": "4/5 · Markdown 직렬화",
            "started_at": "10:41:26",
            "finished_at": "—",
            "requester": "정하늘",
            "error": "",
            "output_path": "/storage/parsed/2024/09/JOB-24704/ (생성 중)",
        },
    ]
