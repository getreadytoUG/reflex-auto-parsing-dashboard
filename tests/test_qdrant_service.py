import pytest

from app.services import qdrant_service


async def test_aggregate_document_stats_counts_by_status_and_file_type(monkeypatch):
    async def fake_fetch_documents(limit=10_000):
        return [
            {"status": "Completed", "file_type": "PDF"},
            {"status": "Completed", "file_type": "HWP"},
            {"status": "Failed", "file_type": "PDF"},
        ]

    monkeypatch.setattr(qdrant_service, "fetch_documents", fake_fetch_documents)

    stats = await qdrant_service.aggregate_document_stats()

    assert stats["total"] == 3
    assert stats["status_counts"] == {"Completed": 2, "Failed": 1}
    assert stats["file_type_counts"] == {"PDF": 2, "HWP": 1}


async def test_aggregate_document_stats_empty_collection(monkeypatch):
    async def fake_fetch_documents(limit=10_000):
        return []

    monkeypatch.setattr(qdrant_service, "fetch_documents", fake_fetch_documents)

    stats = await qdrant_service.aggregate_document_stats()

    assert stats == {"total": 0, "status_counts": {}, "file_type_counts": {}}
