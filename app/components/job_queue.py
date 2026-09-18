import reflex as rx

from app.components.badges import status_badge, type_chip
from app.states.jobs_state import JobsState, JobSummary, ParsingJob

_BAR = "h-1.5 w-full bg-stone-200"


def summary_tile(item: JobSummary) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                item["icon"],
                class_name=rx.match(
                    item["label"],
                    ("Running", "h-3.5 w-3.5 text-sky-600"),
                    ("Completed", "h-3.5 w-3.5 text-emerald-600"),
                    ("Warning", "h-3.5 w-3.5 text-amber-600"),
                    ("Failed", "h-3.5 w-3.5 text-red-600"),
                    "h-3.5 w-3.5 text-stone-400",
                ),
            ),
            rx.el.span(
                item["label"],
                class_name="text-[11px] font-semibold uppercase tracking-wider text-stone-500",
            ),
            class_name="flex items-center gap-1.5",
        ),
        rx.el.p(
            item["count"],
            class_name="mt-1.5 text-[20px] font-bold leading-none tabular-nums tracking-tight text-stone-900",
        ),
        class_name="w-full border border-stone-200 bg-white px-3 py-2.5",
    )


def summary_row() -> rx.Component:
    return rx.cond(
        JobsState.jobs_loading,
        rx.el.div(
            "요약을 불러오는 중...",
            class_name="w-full p-6 text-center text-[12px] text-stone-500",
        ),
        rx.cond(
            JobsState.jobs_error != "",
            rx.el.div(
                JobsState.jobs_error,
                class_name="w-full p-6 text-center text-[12px] font-semibold text-red-600",
            ),
            rx.el.div(
                rx.foreach(JobsState.summary, summary_tile),
                class_name="grid w-full grid-cols-2 gap-2.5 sm:grid-cols-3 lg:grid-cols-6",
            ),
        ),
    )


def status_filter_chip(label: str) -> rx.Component:
    return rx.el.button(
        label,
        on_click=lambda: JobsState.set_status_filter(label),
        class_name=rx.cond(
            JobsState.selected_status_filter == label,
            "border border-[#151d2c] bg-[#151d2c] px-2.5 py-1 text-[11px] font-semibold text-white",
            "border border-stone-300 bg-white px-2.5 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
        ),
    )


def queue_toolbar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                "상태 필터",
                class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-500",
            ),
            rx.el.div(
                rx.foreach(JobsState.status_filters, status_filter_chip),
                class_name="mt-1 flex flex-wrap items-center gap-1.5",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("refresh-cw", class_name="h-3.5 w-3.5 text-stone-400"),
                rx.el.span(
                    "Auto refresh",
                    class_name="text-[11px] font-semibold text-stone-700",
                ),
                rx.el.span(
                    JobsState.auto_refresh_label,
                    class_name="text-[11px] text-stone-500",
                ),
                class_name="flex flex-wrap items-center gap-1.5",
            ),
            rx.el.p(
                "최근 갱신 "
                + JobsState.last_refreshed_at
                + " · 다음 예정 "
                + JobsState.next_refresh_at,
                class_name="mt-0.5 font-mono text-[10px] tabular-nums text-stone-400",
            ),
            class_name="border-l border-stone-200 pl-3",
        ),
        class_name="flex flex-wrap items-start justify-between gap-3 border border-stone-200 bg-white px-3.5 py-3",
    )


def meta_cell(label: str, value: rx.Var[str], mono: bool) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            label,
            class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-400",
        ),
        rx.el.p(
            value,
            class_name=rx.cond(
                mono,
                "mt-0.5 truncate font-mono text-[11px] tabular-nums text-stone-700",
                "mt-0.5 truncate text-[12px] font-medium text-stone-800",
            ),
        ),
        class_name="min-w-0",
    )


def progress_bar(job: ParsingJob) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                job["stage"],
                class_name="truncate text-[11px] font-medium text-stone-600",
            ),
            rx.el.span(
                f"{job['progress']}%",
                class_name="shrink-0 text-[11px] font-bold tabular-nums text-stone-800",
            ),
            class_name="flex items-center justify-between gap-3",
        ),
        rx.el.div(
            rx.el.div(
                style={"width": f"{job['progress']}%"},
                class_name=rx.match(
                    job["status"],
                    ("Running", "h-full bg-sky-500"),
                    ("Completed", "h-full bg-emerald-500"),
                    ("Warning", "h-full bg-amber-500"),
                    ("Failed", "h-full bg-red-500"),
                    ("Cancelled", "h-full bg-stone-400"),
                    "h-full bg-stone-300",
                ),
            ),
            class_name=f"mt-1 {_BAR}",
        ),
        rx.el.div(
            rx.el.span(
                "페이지 "
                + job["current_page"].to_string()
                + " / "
                + job["total_pages"].to_string(),
                class_name="font-mono text-[10px] tabular-nums text-stone-500",
            ),
            rx.el.span(
                "시작 " + job["started_at"] + " · 종료 " + job["finished_at"],
                class_name="font-mono text-[10px] tabular-nums text-stone-400",
            ),
            class_name="mt-1 flex flex-wrap items-center justify-between gap-2",
        ),
        class_name="min-w-0",
    )


def job_card(job: ParsingJob, **props) -> rx.Component:
    return rx.el.article(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    job["id"],
                    class_name="font-mono text-[11px] font-semibold text-stone-500",
                ),
                type_chip(job["file_type"]),
                status_badge(job["status"]),
                class_name="flex flex-wrap items-center gap-2",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("eye", class_name="h-3 w-3"),
                    "로그",
                    class_name="flex items-center gap-1 border border-stone-300 bg-white px-1.5 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
                ),
                rx.el.button(
                    rx.icon("rotate-ccw", class_name="h-3 w-3"),
                    "재시도",
                    class_name="flex items-center gap-1 border border-stone-300 bg-white px-1.5 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name="flex flex-wrap items-center justify-between gap-2 border-b border-stone-100 px-3.5 py-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.icon(
                        "file-text",
                        class_name="h-3.5 w-3.5 shrink-0 text-stone-400",
                    ),
                    rx.el.p(
                        job["file_name"],
                        class_name="truncate text-[13px] font-semibold text-stone-900",
                    ),
                    class_name="flex min-w-0 items-center gap-2",
                ),
                rx.el.div(
                    meta_cell("Parser", job["parser"], True),
                    meta_cell("요청자", job["requester"], False),
                    class_name="mt-2.5 grid grid-cols-2 gap-3",
                ),
                class_name="min-w-0",
            ),
            progress_bar(job),
            class_name="grid grid-cols-1 gap-3.5 px-3.5 py-3 lg:grid-cols-2",
        ),
        rx.cond(
            job["error"] != "",
            rx.el.div(
                rx.icon(
                    "triangle-alert",
                    class_name=rx.cond(
                        job["status"] == "Failed",
                        "mt-0.5 h-3.5 w-3.5 shrink-0 text-red-600",
                        "mt-0.5 h-3.5 w-3.5 shrink-0 text-amber-600",
                    ),
                ),
                rx.el.p(
                    job["error"],
                    class_name="text-[11px] leading-relaxed text-stone-700",
                ),
                class_name=rx.cond(
                    job["status"] == "Failed",
                    "flex items-start gap-2 border-t border-stone-100 bg-red-50/70 px-3.5 py-2",
                    "flex items-start gap-2 border-t border-stone-100 bg-amber-50/70 px-3.5 py-2",
                ),
            ),
            rx.fragment(),
        ),
        rx.el.div(
            rx.el.div(
                rx.icon("folder", class_name="h-3 w-3 text-stone-400"),
                rx.el.span(
                    job["output_path"],
                    class_name="truncate font-mono text-[10px] text-stone-500",
                ),
                class_name="flex min-w-0 items-center gap-1.5",
            ),
            rx.el.button(
                rx.icon("clipboard-check", class_name="h-3 w-3"),
                "Validation 이동",
                class_name="flex shrink-0 items-center gap-1 border border-stone-300 bg-white px-1.5 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
            ),
            class_name="flex flex-wrap items-center justify-between gap-2 border-t border-stone-100 bg-stone-50 px-3.5 py-2",
        ),
        class_name="w-full min-w-0 border border-stone-200 bg-white",
        **props,
    )


def job_list() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "작업 큐 상세",
                    class_name="text-[13px] font-bold tracking-tight text-stone-900",
                ),
                rx.el.p(
                    "진행률 · 현재 단계 · 오류 메시지 · 결과 경로",
                    class_name="text-[11px] text-stone-500",
                ),
            ),
            class_name="flex flex-wrap items-center justify-between gap-2",
        ),
        rx.cond(
            JobsState.jobs_loading,
            rx.el.div(
                "Job 목록을 불러오는 중...",
                class_name="mt-2.5 p-6 text-center text-[12px] text-stone-500",
            ),
            rx.cond(
                JobsState.jobs_error != "",
                rx.el.div(
                    JobsState.jobs_error,
                    class_name="mt-2.5 p-6 text-center text-[12px] font-semibold text-red-600",
                ),
                rx.el.div(
                    rx.foreach(
                        JobsState.jobs, lambda job: job_card(job, key=job["id"])
                    ),
                    class_name="mt-2.5 flex w-full flex-col gap-2.5",
                ),
            ),
        ),
        class_name="w-full min-w-0",
    )
