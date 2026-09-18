from app.states.dashboard_state import _build_kpis, _job_event_to_row


def test_build_kpis_maps_qdrant_stats_and_average_duration():
    stats = {
        "total": 10,
        "status_counts": {"Completed": 6, "Warning": 2, "Failed": 1},
        "file_type_counts": {"PDF": 10},
    }

    kpis = _build_kpis(stats, avg_duration=42.6)

    by_label = {kpi["label"]: kpi for kpi in kpis}
    assert by_label["전체 문서"]["value"] == "10"
    assert by_label["파싱 성공"]["value"] == "6"
    assert by_label["Warning"]["value"] == "2"
    assert by_label["Failed"]["value"] == "1"
    assert by_label["검수 필요"]["value"] == "2"
    assert by_label["평균 파싱 시간"]["value"] == "42.6"
    assert by_label["평균 파싱 시간"]["unit"] == "초/문서"


def test_build_kpis_shows_dash_when_no_average_duration():
    stats = {"total": 0, "status_counts": {}, "file_type_counts": {}}

    kpis = _build_kpis(stats, avg_duration=None)

    by_label = {kpi["label"]: kpi for kpi in kpis}
    assert by_label["평균 파싱 시간"]["value"] == "—"


def test_job_event_to_row_formats_duration_under_a_minute():
    event = {
        "job_id": "JOB-1",
        "file_name": "a.pdf",
        "file_type": "PDF",
        "parser": "PyMuPDF",
        "pages": "10 p",
        "duration_seconds": 38.0,
        "requester": "이준호",
        "started_at": "10:39",
        "status": "Completed",
    }

    row = _job_event_to_row(event)

    assert row["duration"] == "38초"
    assert row["id"] == "JOB-1"
    assert row["file_type"] == "PDF"


def test_job_event_to_row_formats_duration_over_a_minute():
    event = {
        "job_id": "JOB-2",
        "file_name": "b.pdf",
        "file_type": "PDF",
        "parser": "PyMuPDF",
        "pages": "128 p",
        "duration_seconds": 72.0,
        "requester": "김서연",
        "started_at": "10:42",
        "status": "Completed",
    }

    row = _job_event_to_row(event)

    assert row["duration"] == "1분 12초"
