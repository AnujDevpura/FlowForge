import asyncio
from datetime import datetime

from sqlalchemy import update

from db.enums import TaskStatus
from db.session import AsyncSessionLocal
from queueing.tasks import enqueue_task
from scheduler.runnable import get_runnable_tasks
from scheduler.worker_recovery import (
    recover_dead_workers,
)
from db.models.task import Task
from scheduler.lease_recovery import (
    recover_expired_leases,
)


async def scheduler_loop():

    while True:

        async with AsyncSessionLocal() as db:
            
            await recover_dead_workers(db)
            
            await recover_expired_leases(db)

            runnable_tasks = await get_runnable_tasks(db)

            for task in runnable_tasks:

                claim_result = await db.execute(
                    update(Task)
                    .where(
                        Task.id == task.id,
                        Task.status == TaskStatus.PENDING,
                    )
                    .values(
                        status=TaskStatus.QUEUED,
                        queued_at=datetime.utcnow(),
                    )
                    .returning(Task.id)
                )

                claimed_task = (
                    claim_result.scalar_one_or_none()
                )

                if not claimed_task:
                    continue

                await db.commit()

                await enqueue_task(task.id)

                print(
                    f"[SCHEDULER] "
                    f"Queued task: {task.name}"
                )

            await db.commit()

        await asyncio.sleep(5)