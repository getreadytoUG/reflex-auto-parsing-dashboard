import reflex as rx

from app.components.badges import status_badge, type_chip
from app.states.documents_state import DocumentRow, DocumentsState

_TH = "px-3 py-2 text-left text-[11px] font-semibold uppercase tracking-wider text-stone-500 whitespace-nowrap"
_TD = "px-3 py-2 text-[12px] text-stone-700 whitespace-nowrap"


def mock_note(text: str) -> rx.Component:
    return rx.el.span(
        rx.icon("info", class_name="h-3 w-3"),
        text,
        class_name="flex w-fit items-center gap-1 border border-stone-300 bg-stone-100 px-2 py-0.5 text-[10px] font-semibold tracking-wide text-stone-500",
    )


def format_pill(fmt: str) -> rx.Component:
    return rx.el.span(
        fmt,
        class_name="flex w-fit items-center border border-stone-300 bg-white px-2 py-0.5 text-[10px] font-bold tracking-widest text-stone-600",
    )


def method_radio_option(method_name: str) -> rx.Component:
    return rx.el.label(
        rx.el.input(
            type="radio",
            name="parsing_method",
            value=method_name,
            checked=DocumentsState.selected_parsing_method == method_name,
            on_change=lambda: DocumentsState.set_parsing_method(method_name),
            class_name="h-3 w-3 accent-[#151d2c]",
        ),
        method_name,
        class_name="flex items-center gap-1.5 text-[12px] font-medium text-stone-700",
    )


def method_radio_group() -> rx.Component:
    return rx.el.div(
        rx.el.p(
            "파싱 방법",
            class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-500",
        ),
        rx.el.div(
            rx.foreach(DocumentsState.parsing_methods, method_radio_option),
            class_name="mt-1.5 flex flex-wrap items-center gap-3",
        ),
        class_name="mt-2.5 border-t border-stone-200 pt-2.5",
    )


def upload_panel() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "문서 업로드",
                    class_name="text-[13px] font-bold tracking-tight text-stone-900",
                ),
                rx.el.p(
                    "내부망 스토리지에 원본을 적재한 뒤 Parser를 지정합니다.",
                    class_name="text-[11px] text-stone-500",
                ),
            ),
            mock_note("업로드/삭제/DRM 연동 대기 중 · API 스펙 확정 전"),
            class_name="flex flex-wrap items-center justify-between gap-2 border-b border-stone-200 px-3.5 py-2.5",
        ),
        rx.el.div(
            rx.upload.root(
                rx.el.div(
                    rx.icon("cloud-upload", class_name="h-7 w-7 text-stone-400"),
                    rx.el.p(
                        "파일을 이 영역으로 끌어다 놓거나 클릭하여 선택",
                        class_name="mt-2 text-[13px] font-semibold text-stone-700",
                    ),
                    rx.el.p(
                        "1회 최대 20개 · 개별 200MB 이하 · 원본은 변경 없이 보존",
                        class_name="mt-0.5 text-[11px] text-stone-500",
                    ),
                    rx.el.div(
                        rx.foreach(DocumentsState.supported_formats, format_pill),
                        class_name="mt-3 flex flex-wrap items-center justify-center gap-1.5",
                    ),
                    rx.el.p(
                        "지원 형식: PDF · HWP · HWPX · DOCX · PPTX",
                        class_name="mt-2 text-[11px] font-medium text-stone-500",
                    ),
                    class_name="flex flex-col items-center justify-center border-2 border-dashed border-stone-300 bg-[#faf9f6] px-4 py-8 text-center",
                ),
                id="doc_upload",
                multiple=True,
                on_drop=DocumentsState.upload_selected_file,
                class_name="block cursor-pointer",
            ),
            rx.cond(
                DocumentsState.upload_error != "",
                rx.el.p(
                    DocumentsState.upload_error,
                    class_name="mt-2 border-l-2 border-red-400 bg-red-50 px-2.5 py-1.5 text-[11px] leading-relaxed text-red-700",
                ),
                rx.fragment(),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "기본 Parser 프로필",
                        class_name="text-[11px] font-semibold uppercase tracking-wider text-stone-500",
                    ),
                    rx.el.button(
                        rx.icon(
                            rx.cond(
                                DocumentsState.show_method_options,
                                "chevron-up",
                                "chevron-down",
                            ),
                            class_name="h-3.5 w-3.5",
                        ),
                        on_click=DocumentsState.toggle_method_options,
                        class_name="text-stone-400 transition-colors hover:text-stone-700",
                    ),
                    class_name="flex items-center justify-between",
                ),
                rx.el.div(
                    rx.el.select(
                        rx.foreach(
                            DocumentsState.parser_options,
                            lambda p: rx.el.option(p, value=p),
                        ),
                        value=DocumentsState.selected_parser,
                        on_change=DocumentsState.set_parser,
                        class_name="w-full appearance-none border border-stone-300 bg-white px-2.5 py-1.5 pr-8 text-[12px] font-medium text-stone-700 outline-hidden focus:border-stone-500",
                    ),
                    rx.icon(
                        "chevron-down",
                        class_name="pointer-events-none absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-stone-400",
                    ),
                    class_name="relative mt-1.5",
                ),
                rx.cond(
                    DocumentsState.show_method_options,
                    method_radio_group(),
                    rx.fragment(),
                ),
                rx.el.p(
                    "업로드 후 상태는 Uploaded → Queued → Parsing 순으로 전환됩니다.",
                    class_name="mt-3 border-l-2 border-amber-300 bg-amber-50/60 px-2.5 py-1.5 text-[11px] leading-relaxed text-stone-600",
                ),
                class_name="flex flex-col justify-center border border-stone-200 bg-white p-3.5",
            ),
            class_name="grid grid-cols-1 gap-3 p-3.5 lg:grid-cols-[1.6fr_1fr]",
        ),
        class_name="w-full border border-stone-200 bg-white",
    )


def filter_select(
    label: str, options: rx.Var[list[str]], icon: str
) -> rx.Component:
    return rx.el.div(
        rx.el.label(
            label,
            class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-500",
        ),
        rx.el.div(
            rx.icon(
                icon,
                class_name="pointer-events-none absolute left-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-stone-400",
            ),
            rx.el.select(
                rx.foreach(options, lambda o: rx.el.option(o, value=o)),
                class_name="w-full appearance-none border border-stone-300 bg-white py-1.5 pl-7 pr-7 text-[12px] font-medium text-stone-700 outline-hidden focus:border-stone-500",
            ),
            rx.icon(
                "chevron-down",
                class_name="pointer-events-none absolute right-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-stone-400",
            ),
            class_name="relative mt-1",
        ),
        class_name="min-w-[9rem]",
    )


def documents_toolbar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "문서명 검색",
                class_name="text-[10px] font-semibold uppercase tracking-wider text-stone-500",
            ),
            rx.el.div(
                rx.icon(
                    "search",
                    class_name="pointer-events-none absolute left-2 top-1/2 h-3.5 w-3.5 -translate-y-1/2 text-stone-400",
                ),
                rx.el.input(
                    placeholder="예: 예산배분안, 협약서, RFP",
                    class_name="w-full border border-stone-300 bg-white py-1.5 pl-7 pr-2.5 text-[12px] text-stone-700 outline-hidden placeholder:text-stone-400 focus:border-stone-500",
                ),
                class_name="relative mt-1",
            ),
            class_name="min-w-0 flex-1",
        ),
        filter_select("형식", DocumentsState.type_filters, "tag"),
        filter_select("상태", DocumentsState.status_filters, "activity"),
        rx.el.button(
            rx.icon("filter-x", class_name="h-3.5 w-3.5"),
            "초기화",
            class_name="mt-auto flex items-center gap-1.5 border border-stone-300 bg-white px-2.5 py-1.5 text-[12px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
        ),
        class_name="flex flex-wrap items-end gap-3 border-b border-stone-200 bg-stone-50 px-3.5 py-3",
    )


def th(icon: str, label: str) -> rx.Component:
    return rx.el.th(
        rx.el.div(
            rx.icon(icon, class_name="h-3 w-3 text-stone-400"),
            label,
            class_name="flex items-center gap-1.5",
        ),
        class_name=_TH,
    )


def row_action(icon: str, label: str, primary: bool) -> rx.Component:
    return rx.el.button(
        rx.icon(icon, class_name="h-3 w-3"),
        label,
        class_name=rx.cond(
            primary,
            "flex items-center gap-1 border border-[#151d2c] bg-[#151d2c] px-1.5 py-1 text-[11px] font-semibold text-white transition-colors hover:bg-[#1f2a3f]",
            "flex items-center gap-1 border border-stone-300 bg-white px-1.5 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
        ),
    )


def document_row(doc: DocumentRow, index: int) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.icon(
                    "file-text",
                    class_name="h-3.5 w-3.5 shrink-0 text-stone-400",
                ),
                rx.el.div(
                    rx.el.p(
                        doc["file_name"],
                        class_name="max-w-[24rem] truncate text-[12px] font-medium text-stone-900",
                    ),
                    rx.el.p(
                        doc["id"] + " · " + doc["owner"] + " · " + doc["pages"],
                        class_name="font-mono text-[10px] text-stone-400",
                    ),
                    class_name="min-w-0",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="px-3 py-2",
        ),
        rx.el.td(type_chip(doc["file_type"]), class_name=_TD),
        rx.el.td(doc["size"], class_name=f"{_TD} tabular-nums text-right"),
        rx.el.td(
            doc["uploaded_at"], class_name=f"{_TD} tabular-nums text-stone-500"
        ),
        rx.el.td(
            doc["parsed_at"], class_name=f"{_TD} tabular-nums text-stone-500"
        ),
        rx.el.td(status_badge(doc["status"]), class_name="px-3 py-2"),
        rx.el.td(
            rx.el.div(
                rx.el.select(
                    rx.foreach(
                        DocumentsState.parser_options,
                        lambda p: rx.el.option(p, value=p),
                    ),
                    default_value=doc["parser"],
                    key=doc["id"],
                    class_name="w-[8.5rem] appearance-none border border-stone-300 bg-white py-1 pl-2 pr-6 text-[11px] font-medium text-stone-700 outline-hidden focus:border-stone-500",
                ),
                rx.icon(
                    "chevron-down",
                    class_name="pointer-events-none absolute right-1.5 top-1/2 h-3 w-3 -translate-y-1/2 text-stone-400",
                ),
                class_name="relative w-fit",
            ),
            class_name="px-3 py-2",
        ),
        rx.el.td(
            rx.el.div(
                row_action("play", "파싱 실행", True),
                row_action("file-search", "결과 보기", False),
                row_action("clipboard-check", "Validation", False),
                class_name="flex items-center justify-end gap-1.5",
            ),
            class_name="px-3 py-2",
        ),
        class_name=rx.cond(
            index % 2 == 0,
            "border-b border-stone-100 bg-white transition-colors hover:bg-amber-50/40",
            "border-b border-stone-100 bg-stone-50/60 transition-colors hover:bg-amber-50/40",
        ),
    )


def documents_table() -> rx.Component:
    return rx.el.section(
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "등록 문서 목록",
                    class_name="text-[13px] font-bold tracking-tight text-stone-900",
                ),
                rx.el.p(
                    "총 ",
                    DocumentsState.documents.length(),
                    "건 표시",
                    class_name="text-[11px] text-stone-500",
                ),
            ),
            rx.el.div(
                mock_note("버튼은 화면 검토용 목업"),
                rx.el.button(
                    rx.icon("play", class_name="h-3 w-3"),
                    "선택 항목 일괄 파싱",
                    class_name="flex items-center gap-1.5 border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-700 transition-colors hover:bg-stone-100",
                ),
                rx.el.button(
                    rx.icon("download", class_name="h-3 w-3"),
                    "CSV",
                    class_name="flex items-center gap-1.5 border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-600 transition-colors hover:bg-stone-100",
                ),
                class_name="flex flex-wrap items-center gap-2",
            ),
            class_name="flex flex-wrap items-center justify-between gap-3 border-b border-stone-200 px-3.5 py-2.5",
        ),
        documents_toolbar(),
        rx.cond(
            DocumentsState.documents_loading,
            rx.el.div(
                "문서 목록을 불러오는 중...",
                class_name="p-6 text-center text-[12px] text-stone-500",
            ),
            rx.cond(
                DocumentsState.documents_error != "",
                rx.el.div(
                    DocumentsState.documents_error,
                    class_name="p-6 text-center text-[12px] font-semibold text-red-600",
                ),
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                th("file", "파일명"),
                                th("tag", "형식"),
                                th("hard-drive", "크기"),
                                th("calendar-plus", "업로드일"),
                                th("history", "마지막 파싱일"),
                                th("activity", "상태"),
                                th("cpu", "선택 Parser"),
                                rx.el.th("작업", class_name=f"{_TH} text-right"),
                            ),
                            class_name="border-b border-stone-200 bg-stone-50",
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                DocumentsState.documents,
                                lambda doc, index: document_row(doc, index),
                            )
                        ),
                        class_name="w-full table-auto border-collapse",
                    ),
                    class_name="w-full overflow-x-auto",
                ),
            ),
        ),
        rx.el.div(
            rx.el.p(
                "페이지 1 / 1,041",
                class_name="text-[11px] font-medium text-stone-500",
            ),
            rx.el.div(
                rx.el.button(
                    "이전",
                    class_name="border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-400 transition-colors hover:bg-stone-100",
                ),
                rx.el.button(
                    "다음",
                    class_name="border border-stone-300 bg-white px-2 py-1 text-[11px] font-semibold text-stone-700 transition-colors hover:bg-stone-100",
                ),
                class_name="flex items-center gap-1.5",
            ),
            class_name="flex items-center justify-between border-t border-stone-200 bg-stone-50 px-3.5 py-2",
        ),
        class_name="w-full border border-stone-200 bg-white",
    )
