import pytest

from db.enums import TaskStatus

from db.models.job import Job
from db.models.task import Task
from db.models.dependency import (
    TaskDependency,
)

from services.task_context import (
    build_task_context,
)


@pytest.mark.asyncio
async def test_dependency_outputs_are_passed_downstream(
    db_session,
):

    job = Job(
        name="context_job",
        status="RUNNING",
    )

    db_session.add(job)

    await db_session.flush()

    upstream = Task(
        job_id=job.id,
        name="fetch_data",
        status=TaskStatus.SUCCESS,
        payload={
            "type": "http",
            "url": "https://example.com",
        },
        result={
            "records": 100,
        },
    )

    downstream = Task(
        job_id=job.id,
        name="process_data",
        status=TaskStatus.PENDING,
        payload={
            "type": "print",
            "message": "processing",
        },
    )

    db_session.add_all([
        upstream,
        downstream,
    ])

    await db_session.flush()

    dependency = TaskDependency(
        task_id=downstream.id,
        depends_on_task_id=upstream.id,
    )

    db_session.add(dependency)

    await db_session.commit()

    context = await build_task_context(
        db_session,
        downstream,
    )

    assert (
        context["dependencies"]
        ["fetch_data"]
        ["records"]
        == 100
    )