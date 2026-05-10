from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from db.deps import get_db
from db.models.dependency import TaskDependency
from db.models.job import Job
from db.models.task import Task
from schemas.job import JobCreate
from schemas.responses import JobResponse

from utils.dag_validation import validate_dag

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)


@router.post("/")
async def create_job(
    job_data: JobCreate,
    db: AsyncSession = Depends(get_db),
):
    
    try:
        validate_dag(job_data)

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    
    job = Job(
        name=job_data.name,
    )

    db.add(job)

    await db.flush()

    task_name_to_id = {}

    tasks = []

    for task_data in job_data.tasks:
        task = Task(
            job_id=job.id,
            name=task_data.name,
            payload=task_data.payload,
            max_retries=task_data.max_retries,
        )

        db.add(task)

        await db.flush()

        task_name_to_id[task.name] = task.id

        tasks.append((task, task_data))

    for task, task_data in tasks:
        for dependency_name in task_data.dependencies:

            dependency = TaskDependency(
                task_id=task.id,
                depends_on_task_id=task_name_to_id[
                    dependency_name
                ],
            )

            db.add(dependency)

    return {
        "job_id": str(job.id),
        "message": "Job created successfully",
    }


@router.get(
    "/{job_id}",
    response_model=JobResponse,
)
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Job)
        .options(
            selectinload(Job.tasks)
        )
        .where(Job.id == job_id)
    )

    job = result.scalar_one_or_none()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job