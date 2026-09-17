"""Qdrant에서 문서 목록을 조회하는 서비스.

State/컴포넌트에서 import는 하되, rx.State를 import하지 않는 순수 파이썬 모듈로 유지한다
(app/parsers/contracts.py가 지키는 원칙과 동일).
"""

from __future__ import annotations

from qdrant_client import AsyncQdrantClient

from app import config

_client: AsyncQdrantClient | None = None

# Qdrant payload 키 -> DocumentRow 필드 매핑. 실제 payload 스키마를 확인하면
# 이 딕셔너리만 고치면 된다 (지금은 동일한 이름으로 가정한 플레이스홀더).
_PAYLOAD_FIELD_MAP: dict[str, str] = {
    "file_name": "file_name",
    "file_type": "file_type",
    "size": "size",
    "uploaded_at": "uploaded_at",
    "parsed_at": "parsed_at",
    "status": "status",
    "parser": "parser",
    "owner": "owner",
    "pages": "pages",
}

_ROW_DEFAULTS: dict[str, str] = {
    "file_name": "(파일명 없음)",
    "file_type": "-",
    "size": "-",
    "uploaded_at": "-",
    "parsed_at": "-",
    "status": "Uploaded",
    "parser": "-",
    "owner": "-",
    "pages": "-",
}


def get_client() -> AsyncQdrantClient:
    global _client
    if _client is None:
        if not config.QDRANT_BASE_URL:
            raise RuntimeError("QDRANT_BASE_URL 환경변수가 설정되어 있지 않습니다.")
        _client = AsyncQdrantClient(url=config.QDRANT_BASE_URL, api_key=None)
    return _client


async def fetch_documents(limit: int = 50) -> list[dict]:
    """PARENT_COLLECTION에서 문서 단위 포인트를 읽어 DocumentRow 모양의 dict 목록으로 변환한다.

    실패(네트워크 에러, 컬렉션 없음 등) 시 예외를 삼키지 않고 그대로 올린다 —
    호출부(State)가 try/except로 잡아 에러 상태를 표시한다.
    """
    if not config.PARENT_COLLECTION:
        raise RuntimeError("PARENT_COLLECTION 환경변수가 설정되어 있지 않습니다.")

    client = get_client()
    points, _next_offset = await client.scroll(
        collection_name=config.PARENT_COLLECTION,
        limit=limit,
        with_payload=True,
        with_vectors=False,
    )

    rows: list[dict] = []
    for point in points:
        payload = point.payload or {}
        row = {
            row_key: payload.get(payload_key, _ROW_DEFAULTS[row_key])
            for payload_key, row_key in _PAYLOAD_FIELD_MAP.items()
        }
        row["id"] = str(point.id)
        rows.append(row)
    return rows
