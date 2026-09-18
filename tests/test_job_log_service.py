import pytest

from app.services import job_log_service


@pytest.fixture(autouse=True)
def isolate_log_path(tmp_path, monkeypatch):
    monkeypatch.setattr(job_log_service, "_LOG_PATH", tmp_path / "job_log.jsonl")


def make_event(**overrides):
    event = {
        "job_id": "JOB-1",
        "file_name": "a.pdf",
        "file_type": "PDF",
        "parser": "PyMuPDF",
        "pages": "10 p",
        "duration_seconds": 10.0,
        "requester": "tester",
        "started_at": "2026-09-18T00:00:00",
        "status": "Completed",
    }
    event.update(overrides)
    return event


def test_read_recent_jobs_returns_empty_list_when_no_log_file():
    assert job_log_service.read_recent_jobs() == []


def test_read_average_duration_seconds_returns_none_when_no_events():
    assert job_log_service.read_average_duration_seconds() is None


def test_append_and_read_recent_jobs_round_trip():
    job_log_service.append_job_event(make_event(job_id="JOB-1"))
    job_log_service.append_job_event(make_event(job_id="JOB-2"))

    recent = job_log_service.read_recent_jobs()

    assert [e["job_id"] for e in recent] == ["JOB-2", "JOB-1"]


def test_read_recent_jobs_respects_limit():
    for i in range(5):
        job_log_service.append_job_event(make_event(job_id=f"JOB-{i}"))

    recent = job_log_service.read_recent_jobs(limit=2)

    assert [e["job_id"] for e in recent] == ["JOB-4", "JOB-3"]


def test_read_parser_throughput_counts_by_parser():
    job_log_service.append_job_event(make_event(parser="PyMuPDF"))
    job_log_service.append_job_event(make_event(parser="PyMuPDF"))
    job_log_service.append_job_event(make_event(parser="HwpAdapter"))

    throughput = job_log_service.read_parser_throughput()

    assert dict(zip(throughput["parser"], throughput["documents"])) == {
        "PyMuPDF": 2,
        "HwpAdapter": 1,
    }


def test_read_average_duration_seconds_computes_mean():
    job_log_service.append_job_event(make_event(duration_seconds=10.0))
    job_log_service.append_job_event(make_event(duration_seconds=20.0))

    assert job_log_service.read_average_duration_seconds() == 15.0


def test_corrupted_log_line_is_treated_as_empty_log():
    job_log_service._LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    job_log_service._LOG_PATH.write_text("not json\n", encoding="utf-8")

    assert job_log_service.read_recent_jobs() == []
    assert job_log_service.read_average_duration_seconds() is None


def test_schema_invalid_log_line_is_treated_as_empty_log():
    # JSON이 유효해도 필수 키(duration_seconds 등)가 없으면 스키마 위반이다 —
    # 손상된 로그와 동일하게 전체를 빈 것으로 취급해서 KeyError를 막아야 한다.
    job_log_service._LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    job_log_service._LOG_PATH.write_text(
        '{"job_id": "JOB-1"}\n', encoding="utf-8"
    )

    assert job_log_service.read_recent_jobs() == []
    assert job_log_service.read_average_duration_seconds() is None
