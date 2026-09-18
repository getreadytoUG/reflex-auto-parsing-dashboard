"""로컬 Job 로그 — Dashboard의 '최근 Job'/'Parser 처리량'/'평균 파싱 시간'을
채우기 위한 임시 저장소.

실제 Job/Worker 시스템(TODO.md 4번)이 생기기 전까지, 파싱 이벤트를
`data/job_log.jsonl`에 한 줄씩(JSON Lines) 기록해서 그걸 읽어 집계한다.
Reflex를 import하지 않는 순수 파이썬 모듈이다 (app/services/의 다른 모듈과
같은 원칙).

실제 파싱 실행 기능이 생기면, Job이 시작/완료되는 지점에서
`append_job_event(...)`를 호출하도록 그 기능 쪽에서 배선한다 — 지금은
아무도 호출하지 않는다 (함수 시그니처와 파일 포맷만 확정해 둔다).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

_LOG_PATH = Path(__file__).resolve().parents[2] / "data" / "job_log.jsonl"

_REQUIRED_KEYS = (
    "job_id",
    "file_name",
    "file_type",
    "parser",
    "pages",
    "duration_seconds",
    "requester",
    "started_at",
    "status",
)


class JobLogEvent(TypedDict):
    job_id: str
    file_name: str
    file_type: str
    parser: str
    pages: str
    duration_seconds: float
    requester: str
    started_at: str
    status: str


def _is_valid_event(obj: object) -> bool:
    """JSON은 유효하지만 스키마가 깨진 이벤트(필수 키 누락/타입 불일치)를 걸러낸다."""
    if not isinstance(obj, dict):
        return False
    if not all(key in obj for key in _REQUIRED_KEYS):
        return False
    if isinstance(obj["duration_seconds"], bool) or not isinstance(
        obj["duration_seconds"], (int, float)
    ):
        return False
    return True


def _read_events() -> list[JobLogEvent]:
    """로그 파일을 읽어 이벤트 목록으로 반환한다.

    파일이 없으면 빈 리스트(정상 상태 — 아직 Job이 한 번도 안 돈 것뿐).
    한 줄이라도 JSON 파싱에 실패하거나, JSON은 유효하지만 필수 키가
    없거나 타입이 맞지 않으면 로그 전체를 빈 것으로 취급한다
    (부분적으로 깨진 로그를 신뢰하지 않는다).
    """
    if not _LOG_PATH.exists():
        return []
    events: list[JobLogEvent] = []
    try:
        for line in _LOG_PATH.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            parsed = json.loads(line)
            if not _is_valid_event(parsed):
                print(
                    f"[job_log_service] {_LOG_PATH}에 스키마가 유효하지 않은 "
                    f"이벤트가 있어 빈 로그로 처리: {parsed!r}"
                )
                return []
            events.append(parsed)
    except (json.JSONDecodeError, OSError) as e:
        print(f"[job_log_service] {_LOG_PATH} 읽기 실패, 빈 로그로 처리: {e}")
        return []
    return events


def append_job_event(event: JobLogEvent) -> None:
    """Job 이벤트 한 건을 로그에 append한다.

    지금은 호출하는 곳이 없다 — 실제 파싱 실행이 연결되면 Job 시작/완료
    시점에 이 함수를 호출하도록 그때 배선한다.
    """
    _LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    with _LOG_PATH.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def read_recent_jobs(limit: int = 10) -> list[JobLogEvent]:
    """가장 최근 이벤트 limit건을 최신순으로 반환한다."""
    events = _read_events()
    return list(reversed(events))[:limit]


def read_parser_throughput() -> dict[str, list]:
    """parser별 누적 처리 건수. reflex_xy 차트 데이터 형태로 반환한다."""
    events = _read_events()
    counts: dict[str, int] = {}
    for e in events:
        counts[e["parser"]] = counts.get(e["parser"], 0) + 1
    return {"parser": list(counts.keys()), "documents": list(counts.values())}


def read_average_duration_seconds() -> float | None:
    """평균 파싱 시간(초). 이벤트가 하나도 없으면 None."""
    events = _read_events()
    if not events:
        return None
    return sum(e["duration_seconds"] for e in events) / len(events)
