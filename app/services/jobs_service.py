"""Job 큐 조회/제어 — API_BASE_URL 호출 계약.

실제 내부망 API 스펙(엔드포인트 경로, 응답 필드명)이 아직 없어 함수
시그니처만 고정하고 본문은 스텁으로 둔다. State 쪽 이벤트 핸들러는 이
함수들을 실제로 호출하고 NotImplementedError를 잡아 "아직 연동 안 됨"을
사용자에게 보여준다 (app/services/upload_service.py와 동일 패턴).
"""

from __future__ import annotations


async def fetch_job_summary() -> list[dict]:
    """API_BASE_URL에서 상태별 Job 건수 요약을 가져온다.

    TODO: 실제 API 스펙 확정되면 구현. 반환 형태는 JobSummary
    (label/count/icon) 리스트와 맞춰야 한다.
    """
    raise NotImplementedError("API_BASE_URL Job 요약 연동 대기 — API 스펙 확정 후 구현")


async def fetch_jobs(status_filter: str | None = None) -> list[dict]:
    """API_BASE_URL에서 Job 목록을 가져온다.

    status_filter가 None이 아니면 해당 상태로 필터링된 결과를 요청한다
    (전체 조회 후 클라이언트에서 거를지, 서버 쿼리 파라미터로 넘길지는
    실제 API 스펙 확정 시 정한다 — 지금은 인자만 받아둔다).
    TODO: 실제 API 스펙 확정되면 구현. 반환 형태는 ParsingJob 리스트와
    맞춰야 한다.
    """
    raise NotImplementedError("API_BASE_URL Job 목록 연동 대기 — API 스펙 확정 후 구현")
