from typing import TypedDict

import reflex as rx


class JobSummary(TypedDict):
    label: str
    count: str
    icon: str


class ParsingJob(TypedDict):
    id: str
    file_name: str
    file_type: str
    parser: str
    status: str
    progress: int
    current_page: int
    total_pages: int
    stage: str
    started_at: str
    finished_at: str
    requester: str
    error: str
    output_path: str


from app.services import jobs_service


class JobsState(rx.State):
    """작업 큐 상태. 실제 API_BASE_URL 연동 전까지는 호출은 하되 항상 미구현 에러를 받는다."""

    auto_refresh_label: str = "자동 갱신 대기 (Job API 연동 전)"
    last_refreshed_at: str = "—"
    next_refresh_at: str = "—"

    summary: list[JobSummary] = []
    status_filters: list[str] = [
        "전체",
        "Queued",
        "Running",
        "Completed",
        "Warning",
        "Failed",
        "Cancelled",
    ]
    selected_status_filter: str = "전체"

    jobs: list[ParsingJob] = []

    jobs_loading: bool = True
    summary_error: str = ""
    jobs_error: str = ""

    @rx.event
    async def load_jobs(self):
        self.jobs_loading = True
        self.summary_error = ""
        self.jobs_error = ""

        status_arg = (
            None
            if self.selected_status_filter == "전체"
            else self.selected_status_filter
        )

        try:
            self.summary = await jobs_service.fetch_job_summary()
        except NotImplementedError as e:
            self.summary_error = str(e)

        try:
            self.jobs = await jobs_service.fetch_jobs(status_filter=status_arg)
        except NotImplementedError as e:
            self.jobs_error = str(e)

        self.jobs_loading = False

    @rx.event
    async def set_status_filter(self, value: str):
        self.selected_status_filter = value
        await self.load_jobs()
