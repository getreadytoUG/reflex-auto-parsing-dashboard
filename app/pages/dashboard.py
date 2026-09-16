import reflex as rx

from app.components.dashboard_cards import kpi_grid, pipeline_panel
from app.components.dashboard_charts import charts_row
from app.components.jobs_table import jobs_table
from app.components.shell import shell


def dashboard_page() -> rx.Component:
    return shell(
        "Dashboard",
        "문서 파싱 운영 / 현황",
        "문서 수집부터 구조 검수까지의 처리 상태를 한눈에 확인합니다.",
        "Dashboard",
        rx.el.div(
            kpi_grid(),
            rx.el.div(
                rx.el.div(charts_row(), class_name="min-w-0 flex-1"),
                rx.el.div(
                    pipeline_panel(), class_name="w-full xl:w-72 xl:shrink-0"
                ),
                class_name="flex w-full flex-col gap-3 xl:flex-row",
            ),
            jobs_table(),
            class_name="flex w-full flex-col gap-4",
        ),
    )
