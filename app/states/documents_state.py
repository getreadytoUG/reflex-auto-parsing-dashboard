from typing import TypedDict

import reflex as rx


class DocumentRow(TypedDict):
    id: str
    file_name: str
    file_type: str
    size: str
    uploaded_at: str
    parsed_at: str
    status: str
    parser: str
    owner: str
    pages: str


class DocumentsState(rx.State):
    """정적 목업 데이터 전용 상태 (실제 업로드·파싱 없음)."""

    supported_formats: list[str] = ["PDF", "HWP", "HWPX", "DOCX", "PPTX"]

    type_filters: list[str] = [
        "전체 형식",
        "PDF",
        "HWP",
        "HWPX",
        "DOCX",
        "PPTX",
    ]
    status_filters: list[str] = [
        "전체 상태",
        "Uploaded",
        "Queued",
        "Parsing",
        "Completed",
        "Warning",
        "Failed",
    ]
    parser_options: list[str] = [
        "PyMuPDF",
        "PdfPlumber",
        "HwpAdapter",
        "DocxAdapter",
        "PptxAdapter",
        "OCR-Tesseract",
        "TableFormer",
    ]

    documents: list[DocumentRow] = [
        {
            "id": "DOC-100482",
            "file_name": "2024년_국가연구개발사업_예산배분안.pdf",
            "file_type": "PDF",
            "size": "18.4 MB",
            "uploaded_at": "2024-09-18 09:12",
            "parsed_at": "2024-09-18 10:42",
            "status": "Completed",
            "parser": "PyMuPDF",
            "owner": "김서연",
            "pages": "128 p",
        },
        {
            "id": "DOC-100481",
            "file_name": "행정정보_공동이용_협약서_최종본.hwp",
            "file_type": "HWP",
            "size": "3.1 MB",
            "uploaded_at": "2024-09-18 09:31",
            "parsed_at": "진행 중",
            "status": "Parsing",
            "parser": "HwpAdapter",
            "owner": "이준호",
            "pages": "34 p",
        },
        {
            "id": "DOC-100480",
            "file_name": "3분기_내부감사_결과보고서_v3.docx",
            "file_type": "DOCX",
            "size": "1.7 MB",
            "uploaded_at": "2024-09-18 08:55",
            "parsed_at": "2024-09-18 10:35",
            "status": "Warning",
            "parser": "DocxAdapter",
            "owner": "박민정",
            "pages": "22 p",
        },
        {
            "id": "DOC-100479",
            "file_name": "정보시스템_구축_제안요청서(RFP).pdf",
            "file_type": "PDF",
            "size": "42.9 MB",
            "uploaded_at": "2024-09-18 08:40",
            "parsed_at": "—",
            "status": "Queued",
            "parser": "PdfPlumber",
            "owner": "정하늘",
            "pages": "212 p",
        },
        {
            "id": "DOC-100478",
            "file_name": "부서별_인사발령_공고문_2024-09.hwpx",
            "file_type": "HWPX",
            "size": "842 KB",
            "uploaded_at": "2024-09-17 17:22",
            "parsed_at": "2024-09-18 10:14",
            "status": "Completed",
            "parser": "HwpAdapter",
            "owner": "한지원",
            "pages": "12 p",
        },
        {
            "id": "DOC-100477",
            "file_name": "클라우드_전환_사업_착수보고.pptx",
            "file_type": "PPTX",
            "size": "26.3 MB",
            "uploaded_at": "2024-09-17 16:48",
            "parsed_at": "—",
            "status": "Uploaded",
            "parser": "PptxAdapter",
            "owner": "서지훈",
            "pages": "45 slide",
        },
        {
            "id": "DOC-100476",
            "file_name": "민원처리_표준매뉴얼_스캔본.pdf",
            "file_type": "PDF",
            "size": "88.7 MB",
            "uploaded_at": "2024-09-17 15:03",
            "parsed_at": "2024-09-18 10:25",
            "status": "Failed",
            "parser": "OCR-Tesseract",
            "owner": "오세진",
            "pages": "76 p",
        },
        {
            "id": "DOC-100475",
            "file_name": "개인정보_영향평가_결과서_요약.pdf",
            "file_type": "PDF",
            "size": "6.2 MB",
            "uploaded_at": "2024-09-17 14:11",
            "parsed_at": "2024-09-18 09:58",
            "status": "Warning",
            "parser": "PyMuPDF",
            "owner": "김서연",
            "pages": "63 p",
        },
        {
            "id": "DOC-100474",
            "file_name": "전자문서_보존기간_기준표_개정안.docx",
            "file_type": "DOCX",
            "size": "980 KB",
            "uploaded_at": "2024-09-17 11:26",
            "parsed_at": "2024-09-17 11:40",
            "status": "Completed",
            "parser": "DocxAdapter",
            "owner": "이준호",
            "pages": "9 p",
        },
        {
            "id": "DOC-100473",
            "file_name": "지방재정_투자심사_운영지침.hwp",
            "file_type": "HWP",
            "size": "4.6 MB",
            "uploaded_at": "2024-09-16 18:02",
            "parsed_at": "2024-09-16 18:09",
            "status": "Completed",
            "parser": "HwpAdapter",
            "owner": "최도윤",
            "pages": "51 p",
        },
        {
            "id": "DOC-100472",
            "file_name": "정보화사업_사전협의_검토의견서.hwpx",
            "file_type": "HWPX",
            "size": "1.2 MB",
            "uploaded_at": "2024-09-16 15:44",
            "parsed_at": "2024-09-16 15:52",
            "status": "Warning",
            "parser": "HwpAdapter",
            "owner": "박민정",
            "pages": "17 p",
        },
        {
            "id": "DOC-100471",
            "file_name": "차세대_행정포털_요구사항_정의서.pptx",
            "file_type": "PPTX",
            "size": "31.5 MB",
            "uploaded_at": "2024-09-16 10:19",
            "parsed_at": "2024-09-16 10:38",
            "status": "Completed",
            "parser": "PptxAdapter",
            "owner": "정하늘",
            "pages": "72 slide",
        },
    ]
