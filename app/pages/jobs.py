import reflex as rx

from app.components.job_queue import job_list, queue_toolbar, summary_row
from app.components.shell import shell


def jobs_page() -> rx.Component:
    return shell(
        "Parsing Jobs",
        "운영 / 작업 큐",
        "파싱 작업의 상태와 진행률을 확인합니다. Job 큐 API 연동 대기 중입니다.",
        "Parsing Jobs",
        rx.el.div(
            summary_row(),
            queue_toolbar(),
            job_list(),
            class_name="flex w-full min-w-0 flex-col gap-4",
        ),
    )
