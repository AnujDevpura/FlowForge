import asyncio
import json
from datetime import datetime

from sqlalchemy import select

from db.enums import TaskStatus
from db.models.task import Task
from db.session import AsyncSessionLocal
from queueing.redis import redis_client

from executors.dispatcher import execute_task
from services.job_status import update_job_status
from services.task_logs import create_task_log


QUEUE_NAME = "task_queue"

async def worker_loop():

    while True:

        _, raw_task = await redis_client.blpop(
            QUEUE_NAME
        )

        payload = json.loads(raw_task)

        task_id = payload["task_id"]

        async with AsyncSessionLocal() as db:

            result = await db.execute(
                select(Task).where(
                    Task.id == task_id
                )
            )

            task = result.scalar_one_or_none()

            if not task:
                continue

            try:

                task.status = TaskStatus.RUNNING
                task.started_at = datetime.utcnow()

                await db.commit()
                
                await create_task_log(
                    db,
                    task.id,
                    f"Task started: {task.name}",
                )
                
                await update_job_status(
                    db,
                    task.job_id,
                )

                print(
                    f"Executing task: {task.name}"
                )

                await execute_task(
                    task.payload
                )

                task.status = TaskStatus.SUCCESS
                task.completed_at = datetime.utcnow()

                await db.commit()
                
                await create_task_log(
                    db,
                    task.id,
                    f"Task completed successfully",
                )
                
                await update_job_status(
                    db,
                    task.job_id,
                )

                print(
                    f"Task completed: {task.name}"
                )

            except Exception as e:

                task.retry_count += 1

                task.last_error = str(e)

                if (
                    task.retry_count
                    < task.max_retries
                ):

                    task.status = TaskStatus.PENDING

                else:
                    task.status = TaskStatus.FAILED

                await db.commit()
                
                await create_task_log(
                    db,
                    task.id,
                    f"Task failed: {str(e)}",
                )

                await update_job_status(
                    db,
                    task.job_id,
                )