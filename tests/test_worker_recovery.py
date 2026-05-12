from datetime import datetime, UTC, timedelta

import pytest

from db.enums import WorkerStatus
from db.models.worker import Worker

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