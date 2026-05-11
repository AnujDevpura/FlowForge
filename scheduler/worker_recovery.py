from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.enums import TaskStatus
from db.models.task import Task
from db.models.worker import Worker


HEARTBEAT_TIMEOUT_SECONDS = 15

async def recover_dead_workers(
    db: AsyncSession,
):

    cutoff = (
        datetime.utcnow()
        - timedelta(
            seconds=HEARTBEAT_TIMEOUT_SECONDS
        )
    )

    result = await db.execute(
        select(Worker).where(
            Worker.last_heartbeat_at < cutoff,
            Worker.status == "ACTIVE",
        )
    )

    dead_workers = result.scalars().all()

    for worker in dead_workers:

        print(
            f"[RECOVERY] "
            f"Recovering dead worker: {worker.id}"
        )

        task_result = await db.execute(
            select(Task).where(
                Task.worker_id == worker.id,
                Task.status == TaskStatus.RUNNING,
            )
        )

        orphaned_tasks = (
            task_result.scalars().all()
        )

        for task in orphaned_tasks:

            task.status = TaskStatus.PENDING

            task.worker_id = None

            task.started_at = None

            print(
                f"[RECOVERY] "
                f"Recovered task: {task.id}"
            )

        worker.status = "DEAD"

    await db.commit()