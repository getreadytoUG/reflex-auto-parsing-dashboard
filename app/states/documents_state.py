from typing import TypedDict

import reflex as rx

from app.parsers.methods import PARSING_METHODS
from app.services import qdrant_service, upload_service


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
    """Documents 페이지 상태. 목록은 Qdrant에서 실제로 조회한다."""

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

    documents: list[DocumentRow] = []
    documents_loading: bool = True
    documents_error: str = ""

    selected_parser: str = "PyMuPDF"
    show_method_options: bool = False
    selected_parsing_method: str = "Gemma"
    parsing_methods: list[str] = list(PARSING_METHODS.keys())

    upload_error: str = ""

    @rx.event
    async def load_documents(self):
        self.documents_loading = True
        self.documents_error = ""
        try:
            self.documents = await qdrant_service.fetch_documents()
        except Exception as e:
            self.documents_error = f"문서 목록을 불러오지 못했습니다: {e}"
        finally:
            self.documents_loading = False

    @rx.event
    def set_parser(self, value: str):
        self.selected_parser = value

    @rx.event
    def toggle_method_options(self):
        self.show_method_options = not self.show_method_options

    @rx.event
    def set_parsing_method(self, value: str):
        self.selected_parsing_method = value

    @rx.event
    async def upload_selected_file(self, files: list[rx.UploadFile]):
        self.upload_error = ""
        for file in files:
            content = await file.read()
            try:
                await upload_service.upload_document(file.name, content)
            except NotImplementedError as e:
                self.upload_error = str(e)
