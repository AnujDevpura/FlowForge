import pytest

from scheduler.runnable import (
    get_runnable_tasks,
)

from db.enums import TaskStatus
from db.models.job import Job
from db.models.task import Task
from db.models.dependency import (
    TaskDependency,
)


@pytest.mark.asyncio
async def test_only_unblocked_tasks_are_runnable(
    db_session,
):

    job = Job(
        name="test_job",
        status="RUNNING",
    )

    db_session.add(job)

    await db_session.flush()

    task_a = Task(
        job_id=job.id,
        name="task_a",
        status=TaskStatus.SUCCESS,
        payload={
            "type": "print",
            "message": "a",
        },
    )

    task_b = Task(
        job_id=job.id,
        name="task_b",
        status=TaskStatus.PENDING,
        payload={
            "type": "print",
            "message": "b",
        },
    )

    task_c = Task(
        job_id=job.id,
        name="task_c",
        status=TaskStatus.PENDING,
        payload={
            "type": "print",
            "message": "c",
        },
    )

    db_session.add_all([
        task_a,
        task_b,
        task_c,
    ])

    await db_session.flush()

    dependency = TaskDependency(
        task_id=task_b.id,
        depends_on_task_id=task_a.id,
    )

    dependency_2 = TaskDependency(
        task_id=task_c.id,
        depends_on_task_id=task_b.id,
    )

    db_session.add_all([
        dependency,
        dependency_2,
    ])

    await db_session.commit()

    runnable_tasks = await get_runnable_tasks(
        db_session,
    )

    runnable_names = {
        task.name
        for task in runnable_tasks
    }

    assert "task_b" in runnable_names

    assert "task_c" not in runnable_names