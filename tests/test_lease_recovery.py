from datetime import datetime, UTC, timedelta

import pytest

from db.enums import TaskStatus
from db.models.job import Job
from db.models.task import Task

from scheduler.lease_recovery import (
    recover_expired_leases,
)


@pytest.mark.asyncio
async def test_expired_running_task_gets_requeued(
    db_session,
):

    job = Job(
        name="lease_test",
        status="RUNNING",
    )

    db_session.add(job)

    await db_session.flush()

    task = Task(
        job_id=job.id,
        name="processing_task",
        status=TaskStatus.RUNNING,
        payload={
            "type": "print",
            "message": "processing",
        },
        lease_expires_at=(
            datetime.utcnow()
            -
            timedelta(seconds=30)
        ),
    )

    db_session.add(task)

    await db_session.commit()

    await recover_expired_leases(
        db_session,
    )

    await db_session.refresh(task)

    assert (
        task.status
        == TaskStatus.PENDING
    )