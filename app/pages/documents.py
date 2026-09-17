import reflex as rx

from app.components.documents_panel import documents_table, upload_panel
from app.components.shell import shell


def documents_page() -> rx.Component:
    return shell(
        "Documents",
        "운영 / 문서 등록",
        "원본 문서를 등록하고 Parser를 지정합니다. 문서 목록은 Qdrant에서 실시간 조회하며, 업로드/삭제/DRM 연동은 API 스펙 확정 후 반영됩니다.",
        "Documents",
        rx.el.div(
            upload_panel(),
            documents_table(),
            class_name="flex w-full min-w-0 flex-col gap-4",
        ),
    )
