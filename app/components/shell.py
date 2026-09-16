import reflex as rx

from app.components.sidebar import sidebar


def topbar(title: str, breadcrumb: str, description: str) -> rx.Component:
    return rx.el.header(
        rx.el.div(
            rx.el.div(
                rx.el.p(
                    breadcrumb,
                    class_name="text-[11px] font-medium uppercase tracking-widest text-stone-400",
                ),
                rx.el.div(
                    rx.el.h1(
                        title,
                        class_name="text-[19px] font-bold tracking-tight text-stone-900",
                    ),
                    rx.el.span(
                        rx.icon("shield", class_name="h-3 w-3"),
                        "INTERNAL",
                        class_name="flex w-fit items-center gap-1 border border-amber-300 bg-amber-50 px-2 py-0.5 text-[10px] font-bold tracking-widest text-amber-700",
                    ),
                    class_name="flex flex-wrap items-center gap-2",
                ),
                rx.el.p(
                    description, class_name="mt-0.5 text-[12px] text-stone-500"
                ),
                class_name="min-w-0",
            ),
            rx.el.div(
                rx.el.div(
                    rx.icon("search", class_name="h-3.5 w-3.5 text-stone-400"),
                    rx.el.input(
                        placeholder="문서명 · Job ID 검색",
                        class_name="w-40 bg-transparent text-[12px] text-stone-700 outline-hidden placeholder:text-stone-400",
                    ),
                    class_name="hidden items-center gap-2 border border-stone-300 bg-white px-2.5 py-1.5 md:flex",
                ),
                rx.el.button(
                    rx.icon("refresh-cw", class_name="h-3.5 w-3.5"),
                    "동기화",
                    class_name="flex items-center gap-1.5 border border-stone-300 bg-white px-2.5 py-1.5 text-[12px] font-semibold text-stone-700 transition-colors hover:bg-stone-100",
                ),
                rx.el.div(
                    rx.image(
                        src="https://api.dicebear.com/9.x/initials/svg?seed=KSY",
                        class_name="size-7 rounded-full",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "김서연",
                            class_name="text-[12px] font-semibold text-stone-800",
                        ),
                        rx.el.p(
                            "문서운영팀",
                            class_name="text-[10px] text-stone-500",
                        ),
                        class_name="hidden lg:block",
                    ),
                    class_name="flex items-center gap-2 border-l border-stone-200 pl-3",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="flex w-full flex-wrap items-center justify-between gap-4 px-5 py-3",
        ),
        class_name="shrink-0 border-b border-stone-200 bg-white",
    )


def shell(
    title: str, breadcrumb: str, description: str, active: str, *children
) -> rx.Component:
    return rx.el.div(
        sidebar(active),
        rx.el.div(
            topbar(title, breadcrumb, description),
            rx.el.main(
                *children,
                class_name="min-w-0 flex-1 overflow-y-auto bg-[#f6f5f2] px-5 py-5",
            ),
            class_name="flex min-h-0 min-w-0 flex-1 flex-col",
        ),
        class_name="flex h-dvh w-full overflow-hidden font-['Noto_Sans_KR'] antialiased",
    )
