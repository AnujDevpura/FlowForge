import asyncio
from datetime import datetime

from sqlalchemy import update

from db.enums import TaskStatus
from db.session import AsyncSessionLocal
from queueing.tasks import enqueue_task
from scheduler.runnable import get_runnable_tasks
from db.models.task import Task


async def scheduler_loop():

    while True:

        async with AsyncSessionLocal() as db:

            runnable_tasks = await get_runnable_tasks(db)

            for task in runnable_tasks:

                await enqueue_task(task.id)

                await db.execute(
                    update(Task)
                    .where(Task.id == task.id)
                    .values(
                        status=TaskStatus.QUEUED,
                        queued_at=datetime.utcnow(),
                    )
                )

            await db.commit()

        await asyncio.sleep(5)