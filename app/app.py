import reflex as rx

from app.pages.dashboard import dashboard_page
from app.pages.documents import documents_page
from app.pages.jobs import jobs_page
from app.pages.settings import settings_page
from app.pages.validation import validation_page
from app.states.dashboard_state import DashboardState
from app.states.documents_state import DocumentsState
from app.states.jobs_state import JobsState
from app.states.validation_state import ValidationState


def index() -> rx.Component:
    return dashboard_page()


app = rx.App(
    theme=rx.theme(appearance="light"),
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(
            rel="preconnect",
            href="https://fonts.gstatic.com",
            cross_origin="",
        ),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Noto+Sans+KR:wght@400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
app.add_page(index, route="/", on_load=DashboardState.load_dashboard)
app.add_page(
    documents_page, route="/documents", on_load=DocumentsState.load_documents
)
app.add_page(jobs_page, route="/jobs", on_load=JobsState.load_jobs)
app.add_page(
    validation_page, route="/validation", on_load=ValidationState.on_page_load
)
app.add_page(settings_page, route="/settings")
