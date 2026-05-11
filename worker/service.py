import asyncio
import json
from datetime import datetime, timedelta

from sqlalchemy import select, update

from db.enums import TaskStatus
from db.models.task import Task
from db.session import AsyncSessionLocal
from queueing.redis import redis_client
from queueing.tasks import (
    enqueue_dead_letter_task,
)

from executors.dispatcher import execute_task
from services.job_status import update_job_status
from services.task_logs import create_task_log
from services.workers import (
    heartbeat_worker,
    register_worker,
)
from services.task_execution import (
    start_execution,
    complete_execution,
    fail_execution,
)
from services.task_context import (
    build_task_context,
)

QUEUE_NAME = "task_queue"

MAX_CONCURRENT_TASKS = 10

semaphore = asyncio.Semaphore(
    MAX_CONCURRENT_TASKS
)


async def renew_lease_loop(
    task_id,
):

    while True:

        async with AsyncSessionLocal() as db:

            result = await db.execute(
                select(Task).where(
                    Task.id == task_id
                )
            )

            task = result.scalar_one_or_none()

            if not task:
                return

            if task.status != TaskStatus.RUNNING:
                return

            task.lease_expires_at = (
                datetime.utcnow()
                + timedelta(seconds=30)
            )

            await db.commit()

        await asyncio.sleep(10)


async def heartbeat_loop(
    worker_id,
):

    while True:

        async with AsyncSessionLocal() as db:

            await heartbeat_worker(
                db,
                worker_id,
            )

        await asyncio.sleep(5)


async def process_task(
    task_id: str,
    worker_id,
):
    async with semaphore:
        
        print(
            f"Active worker slots: "
            f"{MAX_CONCURRENT_TASKS - semaphore._value}"
        )

        async with AsyncSessionLocal() as db:

            result = await db.execute(
                select(Task).where(
                    Task.id == task_id
                )
            )

            task = result.scalar_one_or_none()

            if not task:
                return

            execution = None
            lease_task = None

            try:

                now = datetime.utcnow()

                claim_result = await db.execute(
                    update(Task)
                    .where(
                        Task.id == task_id,
                        Task.status == "QUEUED",
                    )
                    .values(
                        status=TaskStatus.RUNNING,
                        started_at=now,
                        worker_id=worker_id,
                        lease_expires_at=(
                            now + timedelta(seconds=30)
                        ),
                    )
                    .returning(Task.id)
                )

                claimed_task = (
                    claim_result.scalar_one_or_none()
                )

                if not claimed_task:

                    print(
                        f"Task already claimed: {task_id}"
                    )

                    return

                await db.commit()

                result = await db.execute(
                    select(Task).where(
                        Task.id == task_id
                    )
                )

                task = result.scalar_one()

                lease_task = asyncio.create_task(
                    renew_lease_loop(task.id)
                )

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
                    f"[WORKER] "
                    f"Executing task: {task.name}"
                )
                
                context = await build_task_context(
                    db,
                    task,
                )
                
                execution = await start_execution(
                    db,
                    task,
                    worker_id,
                )

                result = await execute_task(
                    task.payload,
                    context,
                    execution,
                )
                
                await db.commit()

                await db.refresh(execution)

                task.status = TaskStatus.SUCCESS

                task.completed_at = (
                    datetime.utcnow()
                )

                task.next_retry_at = None

                task.lease_expires_at = None
                
                task.result = result

                await db.commit()

                await complete_execution(
                    db,
                    execution,
                )

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
                    f"[WORKER] "
                    f"Task completed: {task.name}"
                )

            except Exception as e:

                task.retry_count += 1

                task.last_error = str(e)

                task.lease_expires_at = None

                if (
                    task.retry_count
                    < task.max_retries
                ):

                    retry_delay = (
                        2 ** task.retry_count
                    )

                    task.status = TaskStatus.PENDING

                    task.next_retry_at = (
                        datetime.utcnow()
                        + timedelta(
                            seconds=retry_delay
                        )
                    )

                else:

                    task.status = TaskStatus.FAILED

                    task.next_retry_at = None

                    await enqueue_dead_letter_task(
                        task.id,
                        str(e),
                    )

                await db.commit()

                if execution:

                    await fail_execution(
                        db,
                        execution,
                        str(e),
                    )

                await create_task_log(
                    db,
                    task.id,
                    f"Task failed: {str(e)}",
                )

                await update_job_status(
                    db,
                    task.job_id,
                )

                print(
                    f"Task failed: {task.name}"
                )
            
            finally:

                if lease_task:

                    lease_task.cancel()


async def worker_loop():

    async with AsyncSessionLocal() as db:

        worker = await register_worker(
            db,
            MAX_CONCURRENT_TASKS,
        )

    worker_id = worker.id
    
    active_tasks = set()
    
    asyncio.create_task(
        heartbeat_loop(worker_id)
    )
    
    while True:

        _, raw_task = await redis_client.blpop(
            QUEUE_NAME
        )

        payload = json.loads(raw_task)

        task_id = payload["task_id"]

        task = asyncio.create_task(
            process_task(
                task_id,
                worker_id,
            )
        )

        active_tasks.add(task)

        task.add_done_callback(
            active_tasks.discard
        )