import reflex as rx

from app.components.settings_panels import (
    contracts_card,
    parser_registry_card,
    roadmap_card,
    storage_card,
    worker_card,
)
from app.components.shell import shell


def settings_page() -> rx.Component:
    return shell(
        "Settings",
        "운영 / 환경 설정",
        "Parser Registry, Worker/Queue, Storage 구성을 확인합니다. 현재 화면은 읽기 전용 목업입니다.",
        "Settings",
        rx.el.div(
            parser_registry_card(),
            rx.el.div(
                worker_card(),
                storage_card(),
                class_name="grid w-full min-w-0 grid-cols-1 gap-3 xl:grid-cols-2",
            ),
            rx.el.div(
                roadmap_card(),
                contracts_card(),
                class_name="grid w-full min-w-0 grid-cols-1 gap-3 xl:grid-cols-2",
            ),
            class_name="flex w-full min-w-0 flex-col gap-3",
        ),
    )
