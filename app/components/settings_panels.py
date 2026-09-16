import reflex as rx

from app.components.documents_panel import mock_note
from app.states.settings_state import (
    AdapterRow,
    ConfigRow,
    RoadmapRow,
    SettingsState,
)

_TH = "px-3 py-2 text-left text-[11px] font-semibold uppercase tracking-wider text-stone-500 whitespace-nowrap"
_TD = "px-3 py-2 text-[12px] text-stone-700"


def card(
    title: str, sub: str, icon: str, *children, note: str = ""
) -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.icon(icon, class_name="h-4 w-4 shrink-0 text-stone-400"),
                rx.el.div(
                    rx.el.h2(
                        title,
                        class_name="text-[13px] font-bold tracking-tight text-stone-900",
                    ),
                    rx.el.p(sub, class_name="text-[11px] text-stone-500"),
                    class_name="min-w-0",
                ),
                class_name="flex min-w-0 items-center gap-2",
            ),
            rx.cond(note != "", mock_note(note), rx.fragment()),
            class_name="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 px-3.5 py-2.5",
        ),
        *children,
        class_name="w-full min-w-0 border border-stone-200 bg-white",
    )


def connection_chip(value: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        rx.el.span(class_name="h-1.5 w-1.5 rounded-full bg-amber-500"),
        value,
        class_name="flex w-fit items-center gap-1.5 border border-amber-300 bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-800",
    )


def adapter_row(row: AdapterRow, index: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.span(
                row["display_format"],
                class_name="flex w-fit items-center border border-stone-300 bg-white px-1.5 py-0.5 text-[10px] font-bold tracking-widest text-stone-600",
            ),
            class_name="px-3 py-2",
        ),
        rx.el.td(
            rx.el.p(
                row["adapter"],
                class_name="font-mono text-[11px] font-semibold text-stone-800",
            ),
            rx.el.p(row["note"], class_name="text-[10px] text-stone-400"),
            class_name="px-3 py-2",
        ),
        rx.el.td(row["engine"], class_name=f"{_TD} whitespace-nowrap"),
        rx.el.td(
            row["version"],
            class_name=f"{_TD} font-mono tabular-nums text-stone-500",
        ),
        rx.el.td(row["capability"], class_name=f"{_TD} text-stone-600"),
        rx.el.td(connection_chip(row["connection"]), class_name="px-3 py-2"),
        class_name=rx.cond(
            index % 2 == 0,
            "border-b border-stone-100 bg-white",
            "border-b border-stone-100 bg-stone-50/60",
        ),
    )


def parser_registry_card() -> rx.Component:
    return card(
        "Parser Registry",
        "형식별 Adapter 등록 상태 · ParserAdapter Protocol 기준",
        "cpu",
        rx.el.div(
            rx.el.table(
                rx.el.thead(
                    rx.el.tr(
                        rx.el.th("형식", class_name=_TH),
                        rx.el.th("Adapter", class_name=_TH),
                        rx.el.th("엔진", class_name=_TH),
                        rx.el.th("버전", class_name=_TH),
                        rx.el.th("지원 범위", class_name=_TH),
                        rx.el.th("연결 상태", class_name=_TH),
                    ),
                    class_name="border-b border-stone-200 bg-stone-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        SettingsState.adapters,
                        lambda row, index: adapter_row(row, index),
                    )
                ),
                class_name="w-full table-auto border-collapse",
            ),
            class_name="w-full overflow-x-auto",
        ),
        rx.el.p(
            "5개 형식 모두 계약(Protocol)만 정의된 상태입니다. 실제 Parser 구현체를 등록하면 이 표의 연결 상태가 전환됩니다.",
            class_name="border-t border-stone-200 bg-stone-50 px-3.5 py-2 text-[11px] text-stone-500",
        ),
        note="목업 화면 · 실제 등록·설정 저장 없음",
    )


def config_table(rows: rx.Var[list[ConfigRow]], key_label: str) -> rx.Component:
    return rx.el.div(
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.el.th(key_label, class_name=_TH),
                    rx.el.th("값", class_name=_TH),
                    rx.el.th("구분", class_name=_TH),
                    rx.el.th("비고", class_name=_TH),
                ),
                class_name="border-b border-stone-200 bg-stone-50",
            ),
            rx.el.tbody(
                rx.foreach(
                    rows,
                    lambda row: rx.el.tr(
                        rx.el.td(
                            row["key"],
                            class_name=f"{_TD} whitespace-nowrap font-medium text-stone-800",
                        ),
                        rx.el.td(
                            row["value"],
                            class_name=f"{_TD} font-mono text-[11px] tabular-nums text-stone-700",
                        ),
                        rx.el.td(
                            rx.el.span(
                                row["scope"],
                                class_name=rx.cond(
                                    row["scope"] == "정책",
                                    "flex w-fit items-center border border-stone-300 bg-white px-1.5 py-0.5 text-[10px] font-semibold text-stone-500",
                                    "flex w-fit items-center border border-emerald-200 bg-emerald-50 px-1.5 py-0.5 text-[10px] font-semibold text-emerald-800",
                                ),
                            ),
                            class_name="px-3 py-2",
                        ),
                        rx.el.td(
                            row["note"],
                            class_name=f"{_TD} text-[11px] text-stone-500",
                        ),
                        class_name="border-b border-stone-100",
                    ),
                )
            ),
            class_name="w-full table-auto border-collapse",
        ),
        class_name="w-full overflow-x-auto",
    )


def worker_card() -> rx.Component:
    return card(
        "Worker / Queue",
        "초기 구성은 단일 프로세스 · 메모리 큐",
        "list-checks",
        config_table(SettingsState.worker_config, "항목"),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "현재 Worker",
                    class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-500",
                ),
                rx.el.span(
                    "2 / 2 slot",
                    class_name="text-[11px] font-semibold text-sky-700",
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.div(
                rx.el.div(class_name="h-full w-full bg-sky-500"),
                class_name="mt-1.5 h-1 w-full bg-stone-200",
            ),
            class_name="border-t border-stone-200 bg-stone-50 px-3.5 py-2.5",
        ),
        note="설정 저장 미연결",
    )


def storage_card() -> rx.Component:
    return card(
        "Storage / Export",
        "SQLite · Local File System 초기 구성",
        "database",
        config_table(SettingsState.storage_config, "항목"),
        note="설정 저장 미연결",
    )


def roadmap_item(row: RoadmapRow) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                row["current"],
                class_name="border border-stone-300 bg-white px-1.5 py-0.5 text-[11px] font-semibold text-stone-600",
            ),
            rx.icon(
                "arrow-right", class_name="h-3 w-3 shrink-0 text-stone-400"
            ),
            rx.el.span(
                row["target"],
                class_name="border border-sky-200 bg-sky-50 px-1.5 py-0.5 text-[11px] font-semibold text-sky-800",
            ),
            rx.el.span(
                row["stage"],
                class_name=rx.cond(
                    row["stage"] == "검토",
                    "ml-auto border border-stone-200 bg-white px-1.5 py-0.5 text-[10px] font-semibold text-stone-500",
                    "ml-auto border border-amber-300 bg-amber-50 px-1.5 py-0.5 text-[10px] font-semibold text-amber-800",
                ),
            ),
            class_name="flex flex-wrap items-center gap-1.5",
        ),
        rx.el.p(
            row["note"],
            class_name="mt-1 text-[11px] leading-relaxed text-stone-500",
        ),
        class_name="border-b border-stone-100 px-3.5 py-2.5",
    )


def roadmap_card() -> rx.Component:
    return card(
        "확장 경로",
        "계약을 유지한 상태에서의 단계적 전환 계획",
        "route",
        rx.el.div(rx.foreach(SettingsState.roadmap, roadmap_item)),
    )


def contracts_card() -> rx.Component:
    return card(
        "Parser 연결 계약",
        "app/parsers/contracts.py · 구현체 없는 경계 정의",
        "file-code",
        config_table(SettingsState.contract_items, "타입"),
        rx.el.p(
            "계약 모듈은 UI·상태·가짜 Parser 구현과 결합하지 않습니다. 실제 Parser는 ParserAdapter 를 구현하고 ParserRegistry 에 등록하는 방식으로만 연결됩니다.",
            class_name="border-t border-stone-200 bg-stone-50 px-3.5 py-2 text-[11px] leading-relaxed text-stone-500",
        ),
    )
