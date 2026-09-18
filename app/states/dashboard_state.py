from datetime import datetime
from typing import TypedDict

import reflex as rx
import reflex_xy

from app.services.job_log_service import JobLogEvent
from app.services import job_log_service, qdrant_service


class KpiItem(TypedDict):
    label: str
    value: str
    unit: str
    delta: str
    trend: str
    icon: str


class JobRow(TypedDict):
    id: str
    file_name: str
    file_type: str
    parser: str
    pages: str
    duration: str
    requester: str
    started_at: str
    status: str


class DashboardState(rx.State):
    kpis: list[KpiItem] = []
    file_types: list[str] = []
    file_type_counts: list[int] = []
    parsers: list[str] = []
    parser_throughput: list[int] = []
    recent_jobs: list[JobRow] = []
    queue_stages: list[tuple[str, str, int]] = []

    dashboard_loading: bool = True
    dashboard_error: str = ""

    @rx.event
    async def load_dashboard(self):
        self.dashboard_loading = True
        self.dashboard_error = ""

        # 로컬 job 로그는 Qdrant와 별개 데이터 소스지만, "평균 파싱 시간"이
        # kpis 리스트 안에 함께 들어가야 하므로(kpi_grid()가 리스트 하나만
        # 순회) Qdrant 집계보다 먼저 읽어서 _build_kpis에 같이 넘긴다.
        avg_duration = job_log_service.read_average_duration_seconds()

        try:
            stats = await qdrant_service.aggregate_document_stats()
            self.kpis = _build_kpis(stats, avg_duration)
            self.file_types = list(stats["file_type_counts"].keys())
            self.file_type_counts = list(stats["file_type_counts"].values())
        except Exception as e:
            self.dashboard_error = f"대시보드 통계를 불러오지 못했습니다: {e}"
        finally:
            self.dashboard_loading = False

        recent = job_log_service.read_recent_jobs()
        self.recent_jobs = [_job_event_to_row(e) for e in recent]
        throughput = job_log_service.read_parser_throughput()
        self.parsers = throughput["parser"]
        self.parser_throughput = throughput["documents"]

        # 파이프라인 단계별 카운트: 실시간 큐 시스템이 없어 항상 빈 리스트.
        # UI(Task 5)가 이 경우 "실시간 큐 연동 대기" 안내로 대체한다.
        self.queue_stages = []

    @reflex_xy.data
    def file_type_data(self) -> dict[str, list[str] | list[int]]:
        return {"file_type": self.file_types, "count": self.file_type_counts}

    @reflex_xy.data
    def parser_data(self) -> dict[str, list[str] | list[int]]:
        return {"parser": self.parsers, "documents": self.parser_throughput}


def _build_kpis(stats: dict, avg_duration: float | None) -> list[KpiItem]:
    status_counts = stats["status_counts"]
    completed = status_counts.get("Completed", 0)
    warning = status_counts.get("Warning", 0)
    failed = status_counts.get("Failed", 0)
    # "검수 필요"에 대응하는 실제 status 값이 아직 확인되지 않았다 —
    # Documents 페이지의 상태 값 중 "Warning"을 임시로 재사용한다.
    # 실제 payload 스키마가 확인되면 이 줄만 고치면 된다.
    needs_review = status_counts.get("Warning", 0)

    avg_duration_value = "—" if avg_duration is None else f"{avg_duration:.1f}"

    return [
        {
            "label": "전체 문서",
            "value": str(stats["total"]),
            "unit": "건",
            "delta": "—",
            "trend": "down",
            "icon": "files",
        },
        {
            "label": "파싱 성공",
            "value": str(completed),
            "unit": "건",
            "delta": "—",
            "trend": "down",
            "icon": "circle-check",
        },
        {
            "label": "Warning",
            "value": str(warning),
            "unit": "건",
            "delta": "—",
            "trend": "down",
            "icon": "triangle-alert",
        },
        {
            "label": "Failed",
            "value": str(failed),
            "unit": "건",
            "delta": "—",
            "trend": "down",
            "icon": "circle-x",
        },
        {
            "label": "검수 필요",
            "value": str(needs_review),
            "unit": "건",
            "delta": "—",
            "trend": "down",
            "icon": "clipboard-check",
        },
        {
            "label": "평균 파싱 시간",
            "value": avg_duration_value,
            "unit": "초/문서",
            "delta": "—",
            "trend": "down",
            "icon": "timer",
        },
    ]


def _format_started_at(started_at: str) -> str:
    """ISO 8601 문자열을 "시작" 컬럼에 맞는 HH:MM으로 포맷한다.

    파싱에 실패하면(예: 수작업으로 편집된 로그) 원본 문자열을 그대로
    반환한다 — 크래시보다 부정확한 표시가 낫다.
    """
    try:
        return datetime.fromisoformat(started_at).strftime("%H:%M")
    except ValueError:
        return started_at


def _job_event_to_row(event: JobLogEvent) -> JobRow:
    minutes, seconds = divmod(int(event["duration_seconds"]), 60)
    duration = f"{minutes}분 {seconds}초" if minutes else f"{seconds}초"
    return {
        "id": event["job_id"],
        "file_name": event["file_name"],
        "file_type": event["file_type"],
        "parser": event["parser"],
        "pages": event["pages"],
        "duration": duration,
        "requester": event["requester"],
        "started_at": _format_started_at(event["started_at"]),
        "status": event["status"],
    }
