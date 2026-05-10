from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.enums import JobStatus, TaskStatus
from db.models.job import Job
from db.models.task import Task


async def update_job_status(
    db: AsyncSession,
    job_id,
):

    result = await db.execute(
        select(Task).where(
            Task.job_id == job_id
        )
    )

    tasks = result.scalars().all()

    statuses = {
        task.status
        for task in tasks
    }

    job_result = await db.execute(
        select(Job).where(
            Job.id == job_id
        )
    )

    job = job_result.scalar_one()

    if all(
        status == TaskStatus.SUCCESS
        for status in statuses
    ):

        job.status = JobStatus.SUCCESS

    elif any(
        status == TaskStatus.FAILED
        for status in statuses
    ):

        job.status = JobStatus.FAILED

    elif any(
        status in {
            TaskStatus.RUNNING,
            TaskStatus.QUEUED,
            TaskStatus.SUCCESS,
        }
        for status in statuses
    ):

        job.status = JobStatus.RUNNING

    else:

        job.status = JobStatus.PENDING

    await db.commit()