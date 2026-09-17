"""업로드/삭제/DRM 호출 계약.

실제 내부망 API 스펙이 아직 없어 함수 시그니처만 고정하고 본문은 스텁으로 둔다.
호출부(State)는 이 함수들을 실제로 호출하고 NotImplementedError를 잡아
"아직 연동 안 됨"을 사용자에게 보여준다.
"""

from __future__ import annotations


class UploadError(RuntimeError):
    pass


async def upload_document(file_name: str, content: bytes) -> str:
    """UPLOAD_BASE_URL로 원본 업로드. 반환값은 서버가 부여한 document_id.

    TODO: 실제 API 스펙 확정되면 구현.
    """
    raise NotImplementedError("UPLOAD_BASE_URL 연동 대기 — API 스펙 확정 후 구현")


async def delete_document(document_id: str) -> None:
    """DELETE_BASE_URL로 삭제.

    TODO: 실제 API 스펙 확정되면 구현.
    """
    raise NotImplementedError("DELETE_BASE_URL 연동 대기 — API 스펙 확정 후 구현")


async def check_drm(document_id: str) -> bool:
    """DRM_BASE_URL로 DRM 통과 여부 확인.

    TODO: 실제 API 스펙 확정되면 구현. 업로드 흐름에서 언제 호출할지는
    아직 정해지지 않았다 (미해결 사항 참고).
    """
    raise NotImplementedError("DRM_BASE_URL 연동 대기 — API 스펙 확정 후 구현")
