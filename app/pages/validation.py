import reflex as rx

from app.components.shell import shell
from app.components.validation_workbench import (
    validation_header,
    validation_workbench,
)


def validation_page() -> rx.Component:
    return shell(
        "Validation",
        "운영 / 구조 검수",
        "원본과 파싱 결과를 대조하여 문서 구조를 검수합니다. 문서 구조 데이터는 Qdrant에서 실시간 조회합니다. 구조 편집은 다음 단계에서 지원됩니다.",
        "Validation",
        rx.el.div(
            validation_header(),
            validation_workbench(),
            class_name="flex w-full min-w-0 flex-col gap-3",
        ),
    )
