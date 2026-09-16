import reflex as rx

from app.components.documents_panel import mock_note
from app.states.validation_state import (
    BlockItem,
    CodeLine,
    HeadingItem,
    InspectorField,
    TableItem,
    ValidationState,
    ViewerLine,
)

_GHOST = "flex items-center gap-1.5 border border-stone-300 bg-white px-2.5 py-1.5 text-[12px] font-semibold text-stone-700 transition-colors hover:bg-stone-100"
_DARK = "flex items-center gap-1.5 border border-[#151d2c] bg-[#151d2c] px-2.5 py-1.5 text-[12px] font-semibold text-white transition-colors hover:bg-[#1f2a3f]"
_PANEL = "flex min-w-0 flex-col border border-stone-200 bg-white"
_PANEL_HEAD = "flex shrink-0 flex-wrap items-center justify-between gap-2 border-b border-stone-200 bg-stone-50 px-3 py-2"
_TOOL = "flex h-6 w-6 items-center justify-center border border-stone-300 bg-white text-stone-600 transition-colors hover:bg-stone-100"


def panel_label(index: str, title: str, sub: str) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            index,
            class_name="flex h-5 w-5 shrink-0 items-center justify-center border border-stone-300 bg-white text-[10px] font-bold text-stone-500",
        ),
        rx.el.div(
            rx.el.p(
                title,
                class_name="text-[12px] font-bold tracking-tight text-stone-900",
            ),
            rx.el.p(sub, class_name="text-[10px] text-stone-500"),
            class_name="min-w-0",
        ),
        class_name="flex min-w-0 items-center gap-2",
    )


def review_badge(state: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        rx.el.span(class_name="h-1.5 w-1.5 rounded-full bg-sky-600"),
        state,
        class_name="flex w-fit items-center gap-1.5 border border-sky-200 bg-sky-50 px-2 py-0.5 text-[11px] font-semibold text-sky-800",
    )


def validation_header() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "검수 대상 문서",
                    class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-500",
                ),
                rx.el.div(
                    rx.icon(
                        "file-text",
                        class_name="pointer-events-none absolute left-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-stone-400",
                    ),
                    rx.el.select(
                        rx.foreach(
                            ValidationState.document_options,
                            lambda o: rx.el.option(o, value=o),
                        ),
                        default_value=ValidationState.document_options[0],
                        class_name="w-full appearance-none border border-stone-300 bg-white py-1.5 pl-7 pr-7 text-[12px] font-medium text-stone-800 outline-hidden focus:border-stone-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="pointer-events-none absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-stone-400",
                    ),
                    class_name="relative mt-1",
                ),
                class_name="min-w-[16rem] flex-1",
            ),
            rx.el.div(
                rx.el.label(
                    "검수 상태",
                    class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-500",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            ValidationState.review_states,
                            lambda o: rx.el.option(o, value=o),
                        ),
                        default_value=ValidationState.review_state,
                        class_name="w-full appearance-none border border-stone-300 bg-white py-1.5 pl-2.5 pr-7 text-[12px] font-medium text-stone-800 outline-hidden focus:border-stone-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="pointer-events-none absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-stone-400",
                    ),
                    class_name="relative mt-1",
                ),
                class_name="min-w-[8rem]",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("rotate-ccw", class_name="h-3.5 w-3.5"),
                    "Reparse",
                    class_name=f"{_GHOST} mt-auto",
                ),
                rx.el.button(
                    rx.icon("file-down", class_name="h-3.5 w-3.5"),
                    "Markdown Export",
                    class_name=f"{_GHOST} mt-auto",
                ),
                rx.el.button(
                    rx.icon("braces", class_name="h-3.5 w-3.5"),
                    "JSON Export",
                    class_name=f"{_DARK} mt-auto",
                ),
                class_name="flex flex-wrap items-end gap-2",
            ),
            class_name="flex flex-wrap items-end gap-3 px-3.5 py-3",
        ),
        rx.el.div(
            rx.el.div(
                review_badge(ValidationState.review_state),
                rx.el.span(
                    rx.icon("pencil-line", class_name="h-3 w-3"),
                    "변경 "
                    + ValidationState.change_count.to_string()
                    + "건 미저장",
                    class_name="flex w-fit items-center gap-1.5 border border-amber-300 bg-amber-50 px-2 py-0.5 text-[11px] font-semibold text-amber-800",
                ),
                rx.el.span(
                    ValidationState.document_id
                    + " · "
                    + ValidationState.parser_name
                    + " · 파싱 "
                    + ValidationState.parsed_at,
                    class_name="font-mono text-[10px] tabular-nums text-stone-500",
                ),
                rx.el.span(
                    "검수자 " + ValidationState.reviewer,
                    class_name="text-[11px] text-stone-500",
                ),
                class_name="flex flex-wrap items-center gap-2",
            ),
            mock_note("목업 화면 · Reparse·Export·편집 동작 없음"),
            class_name="flex flex-wrap items-center justify-between gap-2 border-t border-stone-200 bg-stone-50 px-3.5 py-2",
        ),
        class_name="w-full border border-stone-200 bg-white",
    )


def viewer_line(line: ViewerLine) -> rx.Component:
    return rx.el.p(
        line["text"],
        class_name=rx.match(
            line["style"],
            (
                "h1",
                "mb-2 border-b border-stone-300 pb-1 text-center text-[13px] font-bold tracking-tight text-stone-900",
            ),
            ("h2", "mt-3 text-[12px] font-bold text-stone-900"),
            (
                "list",
                "pl-4 text-[11px] leading-[1.9] tracking-tight text-stone-700",
            ),
            (
                "caption",
                "mt-2 text-center text-[10px] font-semibold text-stone-600",
            ),
            (
                "footer",
                "mt-4 text-center text-[10px] tracking-widest text-stone-400",
            ),
            "text-justify text-[11px] leading-[1.9] tracking-tight text-stone-700",
        ),
    )


def viewer_toolbar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.button(
                rx.icon("chevron-left", class_name="h-3.5 w-3.5"),
                class_name=_TOOL,
            ),
            rx.el.span(
                ValidationState.page_label,
                class_name="min-w-[3.5rem] text-center font-mono text-[11px] font-semibold tabular-nums text-stone-700",
            ),
            rx.el.button(
                rx.icon("chevron-right", class_name="h-3.5 w-3.5"),
                class_name=_TOOL,
            ),
            class_name="flex items-center gap-1",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("zoom-out", class_name="h-3.5 w-3.5"), class_name=_TOOL
            ),
            rx.el.span(
                ValidationState.zoom_label,
                class_name="min-w-[2.8rem] text-center font-mono text-[11px] font-semibold tabular-nums text-stone-700",
            ),
            rx.el.button(
                rx.icon("zoom-in", class_name="h-3.5 w-3.5"), class_name=_TOOL
            ),
            rx.el.button(
                rx.icon("maximize", class_name="h-3.5 w-3.5"), class_name=_TOOL
            ),
            class_name="flex items-center gap-1",
        ),
        class_name="flex shrink-0 flex-wrap items-center justify-between gap-2 border-b border-stone-200 bg-white px-3 py-1.5",
    )


def panel_a() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            panel_label("A", "원본 뷰어", "보안 내부망 렌더링 · 다운로드 차단"),
            rx.el.span(
                rx.icon("lock", class_name="h-3 w-3"),
                "SECURE",
                class_name="flex w-fit items-center gap-1 border border-stone-300 bg-white px-1.5 py-0.5 text-[10px] font-bold tracking-widest text-stone-500",
            ),
            class_name=_PANEL_HEAD,
        ),
        viewer_toolbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.span(
                        "국가과학기술자문회의",
                        class_name="text-[9px] tracking-widest text-stone-400",
                    ),
                    rx.el.span(
                        "대외비 · 내부검토용",
                        class_name="text-[9px] tracking-widest text-stone-400",
                    ),
                    class_name="mb-3 flex items-center justify-between border-b border-dashed border-stone-200 pb-1.5",
                ),
                rx.el.p(
                    ValidationState.viewer_header,
                    class_name="mb-3 text-center text-[10px] font-semibold tracking-[0.2em] text-stone-500",
                ),
                rx.foreach(ValidationState.viewer_lines, viewer_line),
                rx.el.div(
                    rx.el.p(
                        "선택된 block 영역 (BLK-0473)",
                        class_name="text-[10px] font-semibold text-amber-700",
                    ),
                    class_name="mt-3 border-2 border-amber-400/70 bg-amber-50/50 px-2 py-1",
                ),
                class_name="mx-auto w-full max-w-[30rem] border border-stone-300 bg-white px-6 py-7 shadow-xs",
            ),
            rx.el.div(
                rx.el.span(
                    "페이지 썸네일",
                    class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-400",
                ),
                rx.el.div(
                    rx.el.div(
                        "11",
                        class_name="flex h-9 w-7 items-center justify-center border border-stone-300 bg-white text-[10px] font-semibold text-stone-500",
                    ),
                    rx.el.div(
                        "12",
                        class_name="flex h-9 w-7 items-center justify-center border-2 border-amber-400 bg-amber-50 text-[10px] font-bold text-amber-700",
                    ),
                    rx.el.div(
                        "13",
                        class_name="flex h-9 w-7 items-center justify-center border border-stone-300 bg-white text-[10px] font-semibold text-stone-500",
                    ),
                    rx.el.div(
                        "14",
                        class_name="flex h-9 w-7 items-center justify-center border border-stone-300 bg-white text-[10px] font-semibold text-stone-500",
                    ),
                    class_name="mt-1.5 flex items-center gap-1.5",
                ),
                class_name="mx-auto mt-4 w-full max-w-[30rem]",
            ),
            class_name="min-h-0 flex-1 overflow-y-auto bg-[#efece5] px-4 py-5",
        ),
        class_name=f"{_PANEL} h-[36rem]",
    )


def tab_button(tab: str) -> rx.Component:
    return rx.el.button(
        tab,
        class_name=rx.cond(
            tab == "Markdown",
            "border-b-2 border-amber-500 px-2.5 py-1.5 text-[12px] font-bold text-stone-900",
            "border-b-2 border-transparent px-2.5 py-1.5 text-[12px] font-semibold text-stone-500 transition-colors hover:text-stone-800",
        ),
    )


def code_line(line: CodeLine) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            line["no"],
            class_name="w-9 shrink-0 select-none border-r border-stone-200 pr-2 text-right font-mono text-[10px] tabular-nums text-stone-400",
        ),
        rx.el.span(
            line["text"],
            class_name=rx.cond(
                line["indent"] == "1",
                rx.match(
                    line["kind"],
                    (
                        "heading",
                        "pl-8 font-mono text-[11px] font-bold text-[#1d4ed8]",
                    ),
                    ("table", "pl-8 font-mono text-[11px] text-stone-600"),
                    ("key", "pl-8 font-mono text-[11px] text-stone-700"),
                    "pl-8 font-mono text-[11px] text-stone-700",
                ),
                rx.match(
                    line["kind"],
                    (
                        "heading",
                        "pl-3 font-mono text-[11px] font-bold text-[#1d4ed8]",
                    ),
                    (
                        "caption",
                        "pl-3 font-mono text-[11px] font-semibold text-stone-800",
                    ),
                    ("table", "pl-3 font-mono text-[11px] text-emerald-800"),
                    ("punct", "pl-3 font-mono text-[11px] text-stone-400"),
                    "pl-3 font-mono text-[11px] text-stone-700",
                ),
            ),
        ),
        class_name=rx.cond(
            line["selected"],
            "flex items-start border-l-2 border-amber-500 bg-amber-50/80 py-[1px]",
            "flex items-start border-l-2 border-transparent py-[1px] hover:bg-stone-50",
        ),
    )


def blocks_row(block: BlockItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                block["label"],
                class_name=rx.match(
                    block["kind"],
                    (
                        "heading",
                        "flex w-11 shrink-0 items-center justify-center border border-sky-200 bg-sky-50 px-1 py-0.5 text-[10px] font-bold text-sky-800",
                    ),
                    (
                        "table",
                        "flex w-11 shrink-0 items-center justify-center border border-amber-300 bg-amber-50 px-1 py-0.5 text-[10px] font-bold text-amber-800",
                    ),
                    (
                        "list",
                        "flex w-11 shrink-0 items-center justify-center border border-stone-300 bg-white px-1 py-0.5 text-[10px] font-bold text-stone-600",
                    ),
                    "flex w-11 shrink-0 items-center justify-center border border-stone-300 bg-white px-1 py-0.5 text-[10px] font-bold text-stone-600",
                ),
            ),
            rx.el.div(
                rx.el.p(
                    block["excerpt"],
                    class_name="truncate text-[12px] font-medium text-stone-800",
                ),
                rx.el.p(
                    block["block_id"]
                    + " · "
                    + block["page"]
                    + " · "
                    + block["order"]
                    + " · conf "
                    + block["confidence"],
                    class_name="font-mono text-[10px] tabular-nums text-stone-400",
                ),
                class_name="min-w-0",
            ),
            class_name="flex min-w-0 items-center gap-2",
        ),
        rx.icon(
            "chevron-right", class_name="h-3.5 w-3.5 shrink-0 text-stone-300"
        ),
        class_name=rx.cond(
            block["selected"],
            "flex items-center justify-between gap-2 border-b border-stone-100 border-l-2 border-l-amber-500 bg-amber-50/70 px-3 py-2",
            "flex items-center justify-between gap-2 border-b border-stone-100 border-l-2 border-l-transparent px-3 py-2 hover:bg-stone-50",
        ),
    )


def tables_row(table: TableItem) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon("table", class_name="h-3.5 w-3.5 shrink-0 text-stone-400"),
            rx.el.div(
                rx.el.p(
                    table["caption"],
                    class_name="truncate text-[12px] font-medium text-stone-800",
                ),
                rx.el.p(
                    table["block_id"]
                    + " · "
                    + table["page"]
                    + " · "
                    + table["size"],
                    class_name="font-mono text-[10px] tabular-nums text-stone-400",
                ),
                class_name="min-w-0",
            ),
            class_name="flex min-w-0 items-center gap-2",
        ),
        rx.el.span(
            table["status"],
            class_name=rx.cond(
                table["status"] == "Warning",
                "flex w-fit shrink-0 items-center border border-amber-300 bg-amber-50 px-1.5 py-0.5 text-[10px] font-semibold text-amber-800",
                "flex w-fit shrink-0 items-center border border-emerald-200 bg-emerald-50 px-1.5 py-0.5 text-[10px] font-semibold text-emerald-800",
            ),
        ),
        class_name="flex items-center justify-between gap-2 border-b border-stone-100 px-3 py-2",
    )


def preview_cell(value: str) -> rx.Component:
    return rx.el.td(
        value,
        class_name="border border-stone-200 px-2 py-1 text-right text-[11px] tabular-nums text-stone-700 first:text-left first:font-medium",
    )


def preview_row(row: list[str]) -> rx.Component:
    return rx.el.tr(rx.foreach(row, preview_cell))


def table_preview() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "선택 Table 미리보기 · BLK-0476",
            class_name="mb-1.5 text-[10px] font-semibold uppercase tracking-wider text-stone-500",
        ),
        rx.el.table(
            rx.el.thead(
                rx.el.tr(
                    rx.foreach(
                        ValidationState.table_preview_header,
                        lambda h: rx.el.th(
                            h,
                            class_name="border border-stone-200 bg-stone-50 px-2 py-1 text-left text-[10px] font-semibold uppercase tracking-wider text-stone-500",
                        ),
                    )
                )
            ),
            rx.el.tbody(
                rx.foreach(ValidationState.table_preview_rows, preview_row)
            ),
            class_name="w-full table-auto border-collapse",
        ),
        class_name="border-t border-stone-200 bg-white px-3 py-2.5",
    )


def panel_b() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            panel_label("B", "파싱 결과", "Markdown · JSON · Blocks · Tables"),
            rx.el.div(
                rx.el.button(
                    rx.icon("copy", class_name="h-3 w-3"),
                    "복사",
                    class_name="flex items-center gap-1 border border-stone-300 bg-white px-1.5 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
                ),
                rx.el.button(
                    rx.icon("wrap-text", class_name="h-3 w-3"),
                    "줄바꿈",
                    class_name="flex items-center gap-1 border border-stone-300 bg-white px-1.5 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name=_PANEL_HEAD,
        ),
        rx.el.div(
            rx.foreach(ValidationState.tabs, tab_button),
            class_name="flex shrink-0 items-center gap-1 border-b border-stone-200 bg-white px-2",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "MARKDOWN · docparse/results/DOC-100482/index.md",
                    class_name="mb-1 font-mono text-[10px] tracking-wide text-stone-400",
                ),
                rx.foreach(ValidationState.markdown_lines, code_line),
                class_name="border-b border-stone-200 bg-[#fcfbf8] py-2",
            ),
            rx.el.div(
                rx.el.p(
                    "BLOCKS JSON · schema v1 (발췌)",
                    class_name="mb-1 px-3 font-mono text-[10px] tracking-wide text-stone-400",
                ),
                rx.foreach(ValidationState.json_lines, code_line),
                class_name="border-b border-stone-200 bg-[#fcfbf8] py-2",
            ),
            rx.el.div(
                rx.el.p(
                    "BLOCK LIST",
                    class_name="border-b border-stone-100 px-3 py-1.5 font-mono text-[10px] tracking-wide text-stone-400",
                ),
                rx.foreach(ValidationState.blocks, blocks_row),
                class_name="bg-white",
            ),
            rx.el.div(
                rx.el.p(
                    "TABLES",
                    class_name="border-b border-stone-100 px-3 py-1.5 font-mono text-[10px] tracking-wide text-stone-400",
                ),
                rx.foreach(ValidationState.tables, tables_row),
                class_name="border-t border-stone-200 bg-white",
            ),
            table_preview(),
            class_name="min-h-0 flex-1 overflow-y-auto",
        ),
        class_name=f"{_PANEL} h-[36rem]",
    )


def heading_node(item: HeadingItem) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            rx.match(
                item["level"],
                (1, "H1"),
                (2, "H2"),
                "H3",
            ),
            class_name=rx.match(
                item["level"],
                (
                    1,
                    "flex w-7 shrink-0 items-center justify-center border border-[#151d2c] bg-[#151d2c] px-1 text-[9px] font-bold text-white",
                ),
                (
                    2,
                    "flex w-7 shrink-0 items-center justify-center border border-sky-300 bg-sky-50 px-1 text-[9px] font-bold text-sky-800",
                ),
                "flex w-7 shrink-0 items-center justify-center border border-stone-300 bg-white px-1 text-[9px] font-bold text-stone-500",
            ),
        ),
        rx.el.div(
            rx.el.p(
                item["text"],
                class_name=rx.match(
                    item["level"],
                    (1, "truncate text-[12px] font-bold text-stone-900"),
                    (2, "truncate text-[12px] font-semibold text-stone-800"),
                    "truncate text-[11px] font-medium text-stone-700",
                ),
            ),
            rx.el.p(
                item["block_id"] + " · " + item["page"],
                class_name="font-mono text-[10px] tabular-nums text-stone-400",
            ),
            class_name="min-w-0 flex-1",
        ),
        rx.el.span(
            item["status"],
            class_name=rx.match(
                item["status"],
                (
                    "검토",
                    "shrink-0 border border-amber-300 bg-amber-50 px-1.5 py-0.5 text-[9px] font-semibold text-amber-800",
                ),
                (
                    "수정",
                    "shrink-0 border border-sky-200 bg-sky-50 px-1.5 py-0.5 text-[9px] font-semibold text-sky-800",
                ),
                "shrink-0 border border-stone-200 bg-white px-1.5 py-0.5 text-[9px] font-semibold text-stone-500",
            ),
        ),
        class_name=rx.cond(
            item["selected"],
            rx.match(
                item["level"],
                (
                    1,
                    "flex items-center gap-2 border-b border-stone-100 border-l-2 border-l-amber-500 bg-amber-50/70 py-1.5 pl-2 pr-2",
                ),
                (
                    2,
                    "flex items-center gap-2 border-b border-stone-100 border-l-2 border-l-amber-500 bg-amber-50/70 py-1.5 pl-5 pr-2",
                ),
                "flex items-center gap-2 border-b border-stone-100 border-l-2 border-l-amber-500 bg-amber-50/70 py-1.5 pl-8 pr-2",
            ),
            rx.match(
                item["level"],
                (
                    1,
                    "flex items-center gap-2 border-b border-stone-100 border-l-2 border-l-transparent py-1.5 pl-2 pr-2 hover:bg-stone-50",
                ),
                (
                    2,
                    "flex items-center gap-2 border-b border-stone-100 border-l-2 border-l-transparent py-1.5 pl-5 pr-2 hover:bg-stone-50",
                ),
                "flex items-center gap-2 border-b border-stone-100 border-l-2 border-l-transparent py-1.5 pl-8 pr-2 hover:bg-stone-50",
            ),
        ),
    )


def inspector_field(field: InspectorField) -> rx.Component:
    return rx.el.div(
        rx.el.span(
            field["label"],
            class_name="w-[6.5rem] shrink-0 text-[10px] font-semibold uppercase tracking-wider text-stone-400",
        ),
        rx.el.span(
            field["value"],
            class_name="min-w-0 truncate font-mono text-[11px] tabular-nums text-stone-700",
        ),
        class_name="flex items-center gap-2 border-b border-stone-100 py-1",
    )


def ctl(icon: str, label: str) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="h-3 w-3 shrink-0"),
        label,
        class_name="flex w-full items-center gap-1.5 border border-stone-300 bg-white px-2 py-1.5 text-[11px] font-semibold text-stone-700 transition-colors hover:bg-stone-100",
    )


def ctl_group(title: str, *children) -> rx.Component:
    return rx.el.div(
        rx.el.p(
            title,
            class_name="mb-1.5 text-[10px] font-semibold uppercase tracking-wider text-stone-400",
        ),
        *children,
        class_name="border-t border-stone-100 px-3 py-2.5",
    )


def inspector() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "선택 Block",
                    class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-500",
                ),
                rx.el.span(
                    ValidationState.selected_block_id,
                    class_name="font-mono text-[11px] font-bold text-amber-700",
                ),
                class_name="flex items-center justify-between gap-2",
            ),
            rx.el.p(
                ValidationState.selected_block_text,
                class_name="mt-1 border-l-2 border-amber-400 bg-amber-50/60 px-2 py-1 text-[12px] font-semibold text-stone-800",
            ),
            class_name="px-3 py-2.5",
        ),
        rx.el.div(
            rx.foreach(ValidationState.inspector_fields, inspector_field),
            class_name="border-t border-stone-100 px-3 py-1.5",
        ),
        ctl_group(
            "Heading Level",
            rx.el.div(
                rx.foreach(
                    ValidationState.heading_levels,
                    lambda lv: rx.el.button(
                        lv,
                        class_name=rx.cond(
                            lv == "H3",
                            "border border-[#151d2c] bg-[#151d2c] px-2 py-1 text-[11px] font-bold text-white",
                            "border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
                        ),
                    ),
                ),
                class_name="flex flex-wrap items-center gap-1",
            ),
        ),
        ctl_group(
            "Block 유형",
            rx.el.div(
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            ValidationState.block_kinds,
                            lambda k: rx.el.option(k, value=k),
                        ),
                        default_value="heading",
                        class_name="w-full appearance-none border border-stone-300 bg-white py-1.5 pl-2 pr-7 text-[11px] font-medium text-stone-700 outline-hidden focus:border-stone-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="pointer-events-none absolute right-2 top-1/2 h-3 w-3 -translate-y-1/2 text-stone-400",
                    ),
                    class_name="relative",
                ),
                rx.el.div(
                    ctl("heading", "Paragraph → Heading"),
                    ctl("pilcrow", "Heading → Paragraph"),
                    ctl("table", "Table 로 지정"),
                    ctl("list", "List 로 지정"),
                    class_name="mt-1.5 grid grid-cols-1 gap-1.5 sm:grid-cols-2",
                ),
                class_name="min-w-0",
            ),
        ),
        ctl_group(
            "순서 · 구조",
            rx.el.div(
                ctl("arrow-up", "위로 이동"),
                ctl("arrow-down", "아래로 이동"),
                ctl("indent-increase", "하위로 내리기"),
                ctl("indent-decrease", "상위로 올리기"),
                ctl("combine", "이전 block 과 병합"),
                ctl("split", "커서 위치에서 분리"),
                class_name="grid grid-cols-1 gap-1.5 sm:grid-cols-2",
            ),
        ),
        ctl_group(
            "Text 수정",
            rx.el.textarea(
                default_value="제13조(중점 투자 분야)",
                rows="3",
                class_name="w-full resize-none border border-stone-300 bg-white px-2 py-1.5 font-mono text-[11px] leading-relaxed text-stone-800 outline-hidden focus:border-stone-500",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("check", class_name="h-3 w-3"),
                    "수정 반영",
                    class_name="flex items-center gap-1.5 border border-[#151d2c] bg-[#151d2c] px-2 py-1 text-[11px] font-semibold text-white transition-colors hover:bg-[#1f2a3f]",
                ),
                rx.el.button(
                    rx.icon("undo-2", class_name="h-3 w-3"),
                    "되돌리기",
                    class_name="flex items-center gap-1.5 border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-3 w-3"),
                    "Block 삭제",
                    class_name="flex items-center gap-1.5 border border-red-200 bg-red-50 px-2 py-1 text-[11px] font-semibold text-red-700 transition-colors hover:bg-red-100",
                ),
                class_name="mt-1.5 flex flex-wrap items-center gap-1.5",
            ),
        ),
        rx.el.div(
            mock_note("모든 편집 제어는 시각화 전용"),
            class_name="border-t border-stone-100 px-3 py-2.5",
        ),
        class_name="min-w-0",
    )


def change_item(text: str) -> rx.Component:
    return rx.el.li(
        rx.icon("dot", class_name="h-3 w-3 shrink-0 text-amber-500"),
        rx.el.span(text, class_name="min-w-0 text-[11px] text-stone-600"),
        class_name="flex items-start gap-1",
    )


def warning_item(text: str) -> rx.Component:
    return rx.el.li(
        rx.icon(
            "triangle-alert",
            class_name="mt-0.5 h-3 w-3 shrink-0 text-amber-600",
        ),
        rx.el.span(
            text,
            class_name="min-w-0 text-[11px] leading-relaxed text-stone-700",
        ),
        class_name="flex items-start gap-1.5",
    )


def panel_c() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            panel_label(
                "C", "구조 · Inspector", "Heading Tree 및 선택 block 제어"
            ),
            rx.el.span(
                ValidationState.heading_tree.length().to_string() + " nodes",
                class_name="font-mono text-[10px] tabular-nums text-stone-500",
            ),
            class_name=_PANEL_HEAD,
        ),
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    "HEADING TREE",
                    class_name="border-b border-stone-100 px-3 py-1.5 font-mono text-[10px] tracking-wide text-stone-400",
                ),
                rx.foreach(ValidationState.heading_tree, heading_node),
                class_name="bg-white",
            ),
            inspector(),
            rx.el.div(
                rx.el.p(
                    "변경 이력 ("
                    + ValidationState.change_count.to_string()
                    + "건)",
                    class_name="mb-1.5 text-[10px] font-semibold uppercase tracking-wider text-stone-400",
                ),
                rx.el.ul(
                    rx.foreach(ValidationState.change_log, change_item),
                    class_name="flex flex-col gap-0.5",
                ),
                class_name="border-t border-stone-100 bg-stone-50 px-3 py-2.5",
            ),
            rx.el.div(
                rx.el.ul(
                    rx.foreach(ValidationState.warnings, warning_item),
                    class_name="flex flex-col gap-1.5",
                ),
                class_name="border-t border-stone-100 bg-amber-50/60 px-3 py-2.5",
            ),
            class_name="min-h-0 flex-1 overflow-y-auto",
        ),
        class_name=f"{_PANEL} h-[36rem]",
    )


def validation_workbench() -> rx.Component:
    return rx.el.div(
        panel_a(),
        panel_b(),
        panel_c(),
        class_name="grid w-full min-w-0 grid-cols-1 gap-3 xl:grid-cols-[1fr_1.15fr_1fr]",
    )
