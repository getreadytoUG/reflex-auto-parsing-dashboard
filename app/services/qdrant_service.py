"""Qdrant에서 문서 목록을 조회하는 서비스.

State/컴포넌트에서 import는 하되, rx.State를 import하지 않는 순수 파이썬 모듈로 유지한다
(app/parsers/contracts.py가 지키는 원칙과 동일).
"""

from __future__ import annotations

from qdrant_client import AsyncQdrantClient, models

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


async def aggregate_document_stats() -> dict:
    """PARENT_COLLECTION 전체를 스캔해 문서 수 통계를 집계한다.

    fetch_documents()의 payload 매핑(_PAYLOAD_FIELD_MAP)을 그대로 재사용하므로,
    실제 payload 스키마가 확인되어 그 매핑을 고치면 여기 집계도 같이 맞는다.
    문서 수가 10,000건을 넘으면 이 limit을 늘리거나 커서 페이지네이션으로
    바꿔야 한다 (미해결 사항).
    """
    rows = await fetch_documents(limit=10_000)
    status_counts: dict[str, int] = {}
    file_type_counts: dict[str, int] = {}
    for row in rows:
        status_counts[row["status"]] = status_counts.get(row["status"], 0) + 1
        file_type_counts[row["file_type"]] = (
            file_type_counts.get(row["file_type"], 0) + 1
        )
    return {
        "total": len(rows),
        "status_counts": status_counts,
        "file_type_counts": file_type_counts,
    }


_CHUNK_PAYLOAD_FIELD_MAP: dict[str, str] = {
    "document_id": "document_id",  # CHILD_COLLECTION에서 부모 문서를 가리키는 필드명 — 실제 스키마 확인 전 플레이스홀더
    "block_id": "block_id",
    "kind": "kind",          # heading/paragraph/list/table/caption/footnote 중 하나로 가정
    "text": "text",
    "page": "page",
    "order": "order",         # 문서 내 순서 — 정렬 기준
    "level": "level",         # heading일 때만 의미 있음 (1/2/3...)
    "confidence": "confidence",
}

_CHUNK_DEFAULTS: dict[str, object] = {
    "block_id": "-",
    "kind": "paragraph",
    "text": "",
    "page": "-",
    "order": 0,
    "level": 1,
    "confidence": "-",
}


async def fetch_document_chunks(document_id: str) -> list[dict]:
    """CHILD_COLLECTION에서 특정 문서의 청크를 조회해 order 기준으로 정렬한 뒤 반환한다.

    실패(네트워크 에러, 컬렉션 없음 등) 시 예외를 그대로 올린다 — 호출부(State)가
    잡아서 에러 상태를 표시한다 (fetch_documents()와 동일 원칙).
    """
    if not config.CHILD_COLLECTION:
        raise RuntimeError("CHILD_COLLECTION 환경변수가 설정되어 있지 않습니다.")

    client = get_client()
    points, _next_offset = await client.scroll(
        collection_name=config.CHILD_COLLECTION,
        scroll_filter=models.Filter(
            must=[
                models.FieldCondition(
                    key=_CHUNK_PAYLOAD_FIELD_MAP["document_id"],
                    match=models.MatchValue(value=document_id),
                )
            ]
        ),
        limit=1000,
        with_payload=True,
        with_vectors=False,
    )

    chunks: list[dict] = []
    for point in points:
        payload = point.payload or {}
        chunk = {
            row_key: payload.get(payload_key, _CHUNK_DEFAULTS[row_key])
            for payload_key, row_key in _CHUNK_PAYLOAD_FIELD_MAP.items()
            if row_key != "document_id"
        }
        chunk["block_id"] = chunk["block_id"] if chunk["block_id"] != "-" else str(point.id)
        chunks.append(chunk)

    chunks.sort(key=lambda c: (c["order"] if isinstance(c["order"], (int, float)) else 0))
    return chunks
