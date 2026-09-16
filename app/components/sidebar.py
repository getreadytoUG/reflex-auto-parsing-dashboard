import reflex as rx

NAV_ITEMS: list[tuple[str, str, str, str]] = [
    ("Dashboard", "운영 현황", "layout-dashboard", "/"),
    ("Documents", "문서 등록", "files", "/documents"),
    ("Parsing Jobs", "작업 큐", "list-checks", "/jobs"),
    ("Validation", "구조 검수", "clipboard-check", "/validation"),
    ("Settings", "환경 설정", "settings", "/settings"),
]


def nav_item(
    label: str, sub: str, icon: str, href: str, active: bool
) -> rx.Component:
    return rx.el.a(
        rx.icon(
            icon,
            class_name=rx.cond(
                active,
                "h-4 w-4 text-amber-300 shrink-0",
                "h-4 w-4 text-slate-400 shrink-0",
            ),
        ),
        rx.el.div(
            rx.el.span(
                label,
                class_name="block text-[13px] font-semibold leading-tight",
            ),
            rx.el.span(
                sub,
                class_name=rx.cond(
                    active,
                    "block text-[11px] leading-tight text-slate-300",
                    "block text-[11px] leading-tight text-slate-500",
                ),
            ),
            class_name="min-w-0",
        ),
        href=href,
        class_name=rx.cond(
            active,
            "flex items-center gap-3 border-l-2 border-amber-400 bg-white/10 px-3 py-2 text-white transition-colors",
            "flex items-center gap-3 border-l-2 border-transparent px-3 py-2 text-slate-300 transition-colors hover:bg-white/5 hover:text-white",
        ),
    )


def sidebar(active: str = "Dashboard") -> rx.Component:
    return rx.el.aside(
        rx.el.div(
            rx.el.div(
                rx.icon("file-stack", class_name="h-5 w-5 text-amber-300"),
                class_name="flex h-9 w-9 items-center justify-center border border-white/15 bg-white/5",
            ),
            rx.el.div(
                rx.el.p(
                    "DocParse Console",
                    class_name="text-[13px] font-bold tracking-tight text-white",
                ),
                rx.el.p(
                    "문서 파싱 운영 시스템",
                    class_name="text-[11px] text-slate-400",
                ),
            ),
            class_name="flex h-16 shrink-0 items-center gap-3 border-b border-white/10 px-4",
        ),
        rx.el.nav(
            rx.el.p(
                "운영",
                class_name="px-3 pb-1 pt-1 text-[10px] font-semibold uppercase tracking-widest text-slate-500",
            ),
            *[
                nav_item(label, sub, icon, href, label == active)
                for label, sub, icon, href in NAV_ITEMS
            ],
            class_name="flex min-h-0 w-full flex-1 flex-col gap-0.5 overflow-y-auto py-3",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.span(
                    "Worker",
                    class_name="text-[11px] font-medium uppercase tracking-wider text-slate-500",
                ),
                rx.el.span(
                    "4 / 6 active",
                    class_name="text-[11px] font-semibold text-emerald-300",
                ),
                class_name="flex items-center justify-between",
            ),
            rx.el.div(
                rx.el.div(class_name="h-full w-2/3 bg-emerald-400/80"),
                class_name="mt-2 h-1 w-full bg-white/10",
            ),
            rx.el.p(
                "내부망 전용 · 외부 전송 차단",
                class_name="mt-3 text-[11px] leading-relaxed text-slate-500",
            ),
            class_name="shrink-0 border-t border-white/10 px-4 py-4",
        ),
        class_name="flex h-full w-60 shrink-0 flex-col bg-[#151d2c]",
    )
