import reflex as rx

from app.components.badges import status_badge, type_chip
from app.states.dashboard_state import DashboardState, JobRow

_TH = "px-3 py-2 text-left text-[11px] font-semibold uppercase tracking-wider text-stone-500"
_TD = "px-3 py-2 text-[12px] text-stone-700 whitespace-nowrap"


def th(icon: str, label: str) -> rx.Component:
    return rx.el.th(
        rx.el.div(
            rx.icon(icon, class_name="h-3 w-3 text-stone-400"),
            label,
            class_name="flex items-center gap-1.5",
        ),
        class_name=_TH,
    )


def job_row(job: JobRow, index: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(
                job["id"], class_name="font-mono text-[11px] text-stone-500"
            ),
            class_name=_TD,
        ),
        rx.el.td(
            rx.el.div(
                rx.icon(
                    "file-text",
                    class_name="h-3.5 w-3.5 shrink-0 text-stone-400",
                ),
                rx.el.span(
                    job["file_name"],
                    class_name="max-w-[22rem] truncate font-medium text-stone-900",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-3 py-2 text-[12px]",
        ),
        rx.el.td(type_chip(job["file_type"]), class_name=_TD),
        rx.el.td(
            rx.el.span(
                job["parser"], class_name="font-mono text-[11px] text-stone-600"
            ),
            class_name=_TD,
        ),
        rx.el.td(job["pages"], class_name=f"{_TD} tabular-nums text-right"),
        rx.el.td(job["duration"], class_name=f"{_TD} tabular-nums text-right"),
        rx.el.td(job["requester"], class_name=_TD),
        rx.el.td(
            job["started_at"], class_name=f"{_TD} tabular-nums text-stone-500"
        ),
        rx.el.td(status_badge(job["status"]), class_name="px-3 py-2"),
        rx.el.td(
            rx.el.button(
                rx.icon("chevron-right", class_name="h-3.5 w-3.5"),
                class_name="text-stone-400 transition-colors hover:text-stone-800",
            ),
            class_name="px-3 py-2 text-right",
        ),
        class_name=rx.cond(
            index % 2 == 0,
            "border-b border-stone-100 bg-white transition-colors hover:bg-amber-50/40",
            "border-b border-stone-100 bg-stone-50/60 transition-colors hover:bg-amber-50/40",
        ),
    )


def jobs_table() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "최근 Parsing Job",
                    class_name="text-[13px] font-bold tracking-tight text-stone-900",
                ),
                rx.el.p(
                    "최근 10건의 작업 이력 (목업 데이터)",
                    class_name="text-[11px] text-stone-500",
                ),
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("funnel", class_name="h-3 w-3"),
                    "상태 필터",
                    class_name="flex items-center gap-1.5 border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-3 w-3"),
                    "CSV",
                    class_name="flex items-center gap-1.5 border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex flex-wrap items-center justify-between gap-3 border-b border-stone-200 px-3.5 py-2.5",
        ),
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        th("hash", "Job ID"),
                        th("file", "문서명"),
                        th("tag", "유형"),
                        th("cpu", "Parser"),
                        th("layers", "분량"),
                        th("timer", "소요"),
                        th("user", "요청자"),
                        th("clock", "시작"),
                        th("activity", "상태"),
                        rx.el.th("", class_name=_TH),
                    ),
                    class_name="border-b border-stone-200 bg-stone-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        DashboardState.recent_jobs,
                        lambda job, index: job_row(job, index),
                    )
                ),
                class_name="w-full table-auto border-collapse",
            ),
            class_name="w-full overflow-x-auto",
        ),
        rx.el.div(
            rx.el.p(
                "총 12,486건 중 10건 표시",
                class_name="text-[11px] font-medium text-stone-500",
            ),
            rx.el.div(
                rx.el.button(
                    "이전",
                    class_name="border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-500 transition-colors hover:bg-stone-100",
                ),
                rx.el.button(
                    "다음",
                    class_name="border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-700 transition-colors hover:bg-stone-100",
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name="flex items-center justify-between border-t border-stone-200 bg-stone-50 px-3.5 py-2",
        ),
        class_name="w-full overflow-hidden border border-stone-200 bg-white",
    )
