# data/

이 디렉터리는 런타임에 자동 생성되는 로컬 상태를 담습니다. git에는 이 README만
추적되고, 실제 데이터 파일(`*.jsonl` 등)은 `.gitignore`에 의해 제외됩니다.

## job_log.jsonl

Dashboard의 "최근 Job" / "Parser별 처리량" / "평균 파싱 시간"이 읽는 로컬
Job 로그입니다 (`app/services/job_log_service.py`). JSON Lines 형식(한 줄에
이벤트 객체 하나)이며, 파일이 없으면 빈 로그로 취급됩니다.

**지금은 아무도 이 파일에 기록하지 않습니다.** 실제 파싱 실행 기능이
만들어지면(TODO.md 4번 "Job 실행 / Worker 분리"), Job이 시작/완료되는
지점에서 `job_log_service.append_job_event(event)`를 호출하도록 배선하세요.
이벤트 스키마는 `job_log_service.JobLogEvent`를 참고하세요.

수동으로 테스트 데이터를 넣고 싶으면 이 파일에 한 줄씩 JSON 객체를
추가하면 됩니다 (예시는 [docs/superpowers/plans/2026-09-18-dashboard-real-integration.md](../docs/superpowers/plans/2026-09-18-dashboard-real-integration.md) Task 5 참고).
