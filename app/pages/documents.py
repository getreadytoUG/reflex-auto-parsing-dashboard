import reflex as rx

from app.components.documents_panel import documents_table, upload_panel
from app.components.shell import shell


def documents_page() -> rx.Component:
    return shell(
        "Documents",
        "운영 / 문서 등록",
        "원본 문서를 등록하고 Parser를 지정합니다. 현재 화면은 UI 검토용 목업입니다.",
        "Documents",
        rx.el.div(
            upload_panel(),
            documents_table(),
            class_name="flex w-full min-w-0 flex-col gap-4",
        ),
    )
