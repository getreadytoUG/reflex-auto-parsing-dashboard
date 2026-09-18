import pytest

from app.services import jobs_service


async def test_fetch_job_summary_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        await jobs_service.fetch_job_summary()


async def test_fetch_jobs_raises_not_implemented_with_no_filter():
    with pytest.raises(NotImplementedError):
        await jobs_service.fetch_jobs()


async def test_fetch_jobs_raises_not_implemented_with_status_filter():
    with pytest.raises(NotImplementedError):
        await jobs_service.fetch_jobs(status_filter="Running")


async def test_submit_reparse_job_raises_not_implemented():
    with pytest.raises(NotImplementedError):
        await jobs_service.submit_reparse_job("DOC-100482", "PyMuPDF 1.24.9")
