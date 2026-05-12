import pytest

from db.enums import TaskStatus

from db.models.job import Job
from db.models.task import Task
from db.models.task_execution import (
    TaskExecution,
)


@pytest.mark.asyncio
async def test_retries_create_new_execution_rows(
    db_session,
):

    job = Job(
        name="execution_history_job",
        status="RUNNING",
    )

    db_session.add(job)

    await db_session.flush()

    task = Task(
        job_id=job.id,
        name="unstable_task",
        status=TaskStatus.FAILED,
        payload={
            "type": "print",
            "message": "unstable",
        },
        retry_count=2,
    )

    db_session.add(task)

    await db_session.flush()

    execution_1 = TaskExecution(
        task_id=task.id,
        attempt_number=1,
        status=TaskStatus.FAILED,
    )

    execution_2 = TaskExecution(
        task_id=task.id,
        attempt_number=2,
        status=TaskStatus.FAILED,
    )

    db_session.add_all([
        execution_1,
        execution_2,
    ])

    await db_session.commit()

    assert (
        execution_1.id
        !=
        execution_2.id
    )

    assert (
        execution_1.attempt_number
        == 1
    )

    assert (
        execution_2.attempt_number
        == 2
    )