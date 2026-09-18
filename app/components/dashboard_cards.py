import reflex as rx

from app.states.dashboard_state import DashboardState, KpiItem


def kpi_card(item: KpiItem, **props) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(item["icon"], class_name="h-3.5 w-3.5 text-stone-400"),
            rx.el.span(
                item["label"],
                class_name="text-[11px] font-semibold tracking-tight text-stone-500",
            ),
            class_name="flex items-center gap-1.5",
        ),
        rx.el.div(
            rx.el.span(
                item["value"],
                class_name="text-[22px] font-bold leading-none text-stone-900",
            ),
            rx.el.span(
                item["unit"],
                class_name="text-[11px] font-medium text-stone-400",
            ),
            class_name="mt-2.5 flex items-baseline gap-1",
        ),
        rx.el.div(
            rx.icon(
                rx.cond(item["trend"] == "up", "trending-up", "trending-down"),
                class_name=rx.cond(
                    item["trend"] == "up",
                    "h-3 w-3 text-emerald-600",
                    "h-3 w-3 text-stone-500",
                ),
            ),
            rx.el.span(
                item["delta"],
                class_name=rx.cond(
                    item["trend"] == "up",
                    "text-[11px] font-semibold text-emerald-700",
                    "text-[11px] font-semibold text-stone-600",
                ),
            ),
            rx.el.span("전일 대비", class_name="text-[10px] text-stone-400"),
            class_name="mt-2 flex items-center gap-1",
        ),
        class_name="w-full border border-stone-200 bg-white px-3.5 py-3 transition-colors hover:border-stone-300",
        **props,
    )


def kpi_grid() -> rx.Component:
    return rx.cond(
        DashboardState.dashboard_loading,
        rx.el.div(
            "통계를 불러오는 중...",
            class_name="p-6 text-center text-[12px] text-stone-500",
        ),
        rx.cond(
            DashboardState.dashboard_error != "",
            rx.el.div(
                DashboardState.dashboard_error,
                class_name="p-6 text-center text-[12px] font-semibold text-red-600",
            ),
            rx.el.div(
                rx.foreach(
                    DashboardState.kpis,
                    lambda item: kpi_card(item, key=item["label"]),
                ),
                class_name="grid grid-cols-1 gap-3 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6",
            ),
        ),
    )


def stage_row(stage: tuple[str, str, int], **props) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                stage[0], class_name="text-[12px] font-semibold text-stone-800"
            ),
            rx.el.span(
                stage[1],
                class_name="text-[10px] font-medium uppercase tracking-wider text-stone-400",
            ),
            class_name="flex items-center gap-2",
        ),
        rx.el.span(
            f"{stage[2]} 건",
            class_name="text-[12px] font-bold tabular-nums text-stone-900",
        ),
        class_name="flex items-center justify-between border-b border-dashed border-stone-200 py-2 last:border-0",
        **props,
    )


def pipeline_panel() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.h2(
                "처리 파이프라인",
                class_name="text-[13px] font-bold tracking-tight text-stone-900",
            ),
            rx.el.span(
                "실시간 큐 연동 대기",
                class_name="text-[10px] font-medium text-stone-400",
            ),
            class_name="flex items-center justify-between border-b border-stone-200 px-3.5 py-2.5",
        ),
        rx.cond(
            DashboardState.queue_stages.length() == 0,
            rx.el.p(
                "파이프라인 단계별 카운트는 아직 연동되지 않았습니다.",
                class_name="px-3.5 py-4 text-[11px] text-stone-500",
            ),
            rx.el.div(
                rx.foreach(
                    DashboardState.queue_stages,
                    lambda stage: stage_row(stage, key=stage[1]),
                ),
                class_name="px-3.5 py-1.5",
            ),
        ),
        class_name="flex w-full flex-col border border-stone-200 bg-white",
    )
