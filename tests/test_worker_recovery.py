from datetime import datetime, UTC, timedelta

import pytest

from db.enums import WorkerStatus
from db.models.worker import Worker
from db.models.task import Task
from db.models.job import Job

from db.enums import TaskStatus

from scheduler.worker_recovery import (
    recover_dead_workers,
)


@pytest.mark.asyncio
async def test_stale_worker_becomes_dead(
    db_session,
):

    worker = Worker(
        hostname="test-worker",
        max_concurrency=4,
        status=WorkerStatus.ACTIVE,
        last_heartbeat_at=(
            datetime.utcnow()
            -
            timedelta(minutes=10)
        ),
    )

    db_session.add(worker)

    await db_session.commit()

    await recover_dead_workers(
        db_session,
    )

    await db_session.refresh(worker)

    assert (
        worker.status
        == WorkerStatus.DEAD
    )


@pytest.mark.asyncio
async def test_dead_worker_releases_running_tasks(
    db_session,
):

    worker = Worker(
        hostname="dead-worker",
        max_concurrency=4,
        status=WorkerStatus.ACTIVE,

        last_heartbeat_at=(
            datetime.utcnow()
            -
            timedelta(minutes=10)
        ),
    )

    db_session.add(worker)

    await db_session.flush()

    job = Job(
        name="recovery_job",
        status="RUNNING",
    )

    db_session.add(job)

    await db_session.flush()

    task = Task(
        job_id=job.id,

        name="orphaned_task",

        status=TaskStatus.RUNNING,

        worker_id=worker.id,

        payload={
            "type": "print",
            "message": "processing",
        },
    )

    db_session.add(task)

    await db_session.commit()

    await recover_dead_workers(
        db_session,
    )

    await db_session.refresh(worker)

    await db_session.refresh(task)

    assert (
        worker.status
        ==
        WorkerStatus.DEAD
    )

    assert (
        task.status
        ==
        TaskStatus.PENDING
    )

    assert (
        task.worker_id
        is None
    )