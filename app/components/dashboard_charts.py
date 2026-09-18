import reflex as rx
import reflex_xy

from app.states.dashboard_state import DashboardState


def chart_card(
    title: str, subtitle: str, chart: rx.Component, badge: str
) -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    title,
                    class_name="text-[13px] font-bold tracking-tight text-stone-900",
                ),
                rx.el.p(subtitle, class_name="text-[11px] text-stone-500"),
            ),
            rx.el.span(
                badge,
                class_name="w-fit border border-stone-300 bg-stone-50 px-1.5 py-0.5 text-[10px] font-semibold text-stone-500",
            ),
            class_name="flex items-start justify-between border-b border-stone-200 px-3.5 py-2.5",
        ),
        rx.el.div(chart, class_name="min-w-[300px] shrink-0 px-2 py-2"),
        class_name="flex min-w-0 flex-1 flex-col border border-stone-200 bg-white",
    )


def file_type_chart() -> rx.Component:
    return chart_card(
        "파일 유형별 문서 수",
        "등록된 원본 포맷 분포",
        reflex_xy.chart(
            reflex_xy.column(
                "file_type",
                "count",
                name="문서 수",
                color="#2f4468",
                corner_radius=2,
            ),
            reflex_xy.x_axis(label="파일 유형"),
            reflex_xy.y_axis(label="문서 수"),
            reflex_xy.modebar(False),
            reflex_xy.interaction_config(navigation=False),
            data=DashboardState.file_type_data,
            height="280px",
            class_name="w-full",
        ),
        badge="전체 기간",
    )


def parser_chart() -> rx.Component:
    return chart_card(
        "Parser별 처리량",
        "Adapter 단위 누적 처리 문서",
        reflex_xy.chart(
            reflex_xy.bar(
                "parser",
                "documents",
                name="처리 문서",
                color="#b4801f",
                orientation="horizontal",
                corner_radius=2,
            ),
            reflex_xy.x_axis(label="처리 문서 수"),
            reflex_xy.y_axis(label="Parser"),
            reflex_xy.modebar(False),
            reflex_xy.interaction_config(navigation=False),
            data=DashboardState.parser_data,
            height="280px",
            class_name="w-full",
        ),
        badge="누적",
    )


def charts_row() -> rx.Component:
    return rx.el.div(
        rx.cond(
            DashboardState.dashboard_loading,
            rx.el.div(
                "차트를 불러오는 중...",
                class_name="w-full p-6 text-center text-[12px] text-stone-500",
            ),
            rx.cond(
                DashboardState.dashboard_error != "",
                rx.el.div(
                    DashboardState.dashboard_error,
                    class_name="w-full p-6 text-center text-[12px] font-semibold text-red-600",
                ),
                file_type_chart(),
            ),
        ),
        rx.cond(
            DashboardState.parsers.length() == 0,
            rx.el.div(
                "아직 기록된 Job이 없습니다.",
                class_name="p-6 text-center text-[12px] text-stone-500",
            ),
            parser_chart(),
        ),
        class_name="flex w-full flex-col gap-3 xl:flex-row",
    )
