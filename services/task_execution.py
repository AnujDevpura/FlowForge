from datetime import datetime

from sqlalchemy import select

from db.enums import TaskStatus
from db.models.task_execution import (
    TaskExecution,
)


async def start_execution(
    db,
    task,
    worker_id,
):
    execution = TaskExecution(
        task_id=task.id,

        attempt_number=(
            task.retry_count + 1
        ),

        status=TaskStatus.RUNNING,

        worker_id=worker_id,

        started_at=datetime.utcnow(),
    )

    db.add(execution)

    await db.commit()

    await db.refresh(execution)

    return execution


async def complete_execution(
    db,
    execution,
):
    execution.status = TaskStatus.SUCCESS

    execution.completed_at = (
        datetime.utcnow()
    )

    await db.commit()


async def fail_execution(
    db,
    execution,
    error: str,
):
    execution.status = TaskStatus.FAILED

    execution.completed_at = (
        datetime.utcnow()
    )

    execution.error_message = error

    await db.commit()