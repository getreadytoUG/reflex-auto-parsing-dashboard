import reflex as rx

_BASE = "flex w-fit items-center gap-1.5 border px-2 py-0.5 text-[11px] font-semibold"


def status_badge(status: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        rx.el.span(
            class_name=rx.match(
                status,
                ("Completed", "h-1.5 w-1.5 rounded-full bg-emerald-600"),
                (
                    "Parsing",
                    "h-1.5 w-1.5 rounded-full bg-sky-600 animate-pulse",
                ),
                (
                    "Running",
                    "h-1.5 w-1.5 rounded-full bg-sky-600 animate-pulse",
                ),
                ("Uploaded", "h-1.5 w-1.5 rounded-full bg-stone-400"),
                ("Queued", "h-1.5 w-1.5 rounded-full bg-stone-400"),
                ("Warning", "h-1.5 w-1.5 rounded-full bg-amber-500"),
                ("Failed", "h-1.5 w-1.5 rounded-full bg-red-600"),
                "h-1.5 w-1.5 rounded-full bg-stone-400",
            )
        ),
        status,
        class_name=rx.match(
            status,
            (
                "Completed",
                f"{_BASE} border-emerald-200 bg-emerald-50 text-emerald-800",
            ),
            ("Parsing", f"{_BASE} border-sky-200 bg-sky-50 text-sky-800"),
            ("Running", f"{_BASE} border-sky-200 bg-sky-50 text-sky-800"),
            (
                "Uploaded",
                f"{_BASE} border-stone-300 bg-white text-stone-600",
            ),
            ("Queued", f"{_BASE} border-stone-300 bg-stone-100 text-stone-600"),
            ("Warning", f"{_BASE} border-amber-300 bg-amber-50 text-amber-800"),
            ("Failed", f"{_BASE} border-red-200 bg-red-50 text-red-700"),
            (
                "Cancelled",
                f"{_BASE} border-stone-200 bg-white text-stone-500 line-through",
            ),
            f"{_BASE} border-stone-300 bg-stone-100 text-stone-600",
        ),
    )


def type_chip(file_type: rx.Var[str]) -> rx.Component:
    return rx.el.span(
        file_type,
        class_name="flex w-fit items-center border border-stone-300 bg-white px-1.5 py-0.5 text-[10px] font-bold tracking-wide text-stone-600",
    )
