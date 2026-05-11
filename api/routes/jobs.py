from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select

from db.deps import get_db
from db.models.dependency import TaskDependency
from db.models.task_execution import (
    TaskExecution,
)
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

    dependency_result = await db.execute(
        select(TaskDependency)
        .join(
            Task,
            Task.id
            ==
            TaskDependency.task_id,
        )
        .where(
            Task.job_id == job.id
        )
    )

    dependencies = (
        dependency_result.scalars().all()
    )

    execution_result = await db.execute(
        select(TaskExecution)
        .join(
            Task,
            Task.id
            ==
            TaskExecution.task_id,
        )
        .where(
            Task.job_id == job.id
        )
    )

    executions = (
        execution_result.scalars().all()
    )

    return {
        "id": str(job.id),

        "name": job.name,

        "status": job.status,

        "created_at": job.created_at,

        "updated_at": job.updated_at,

        "tasks": [
            {
                "id": str(task.id),

                "name": task.name,

                "status": task.status,
                
                "worker_id": (
                    str(task.worker_id)
                    if task.worker_id
                    else None
                ),

                "lease_expires_at":
                    task.lease_expires_at,

                "retry_count":
                    task.retry_count,

                "max_retries":
                    task.max_retries,

                "created_at":
                    task.created_at,

                "queued_at":
                    task.queued_at,

                "started_at":
                    task.started_at,

                "completed_at":
                    task.completed_at,

                "last_error":
                    task.last_error,

                "executions": [
                    {
                        "id":
                            str(execution.id),

                        "attempt_number":
                            execution.attempt_number,

                        "status":
                            execution.status,
                            
                        "logs":
                            execution.logs,

                        "worker_id":
                            str(execution.worker_id)
                            if execution.worker_id
                            else None,

                        "started_at":
                            execution.started_at,

                        "completed_at":
                            execution.completed_at,

                        "error_message":
                            execution.error_message,
                    }
                    for execution in executions
                    if execution.task_id
                    == task.id
                ],
            }
            for task in job.tasks
        ],

        "dependencies": [
            {
                "task_id":
                    str(dep.task_id),

                "depends_on_task_id":
                    str(
                        dep.depends_on_task_id
                    ),
            }
            for dep in dependencies
        ],
    }


@router.get("/")
async def list_jobs(
    db: AsyncSession = Depends(get_db),
):

    result = await db.execute(
        select(Job)
    )

    jobs = result.scalars().all()

    return jobs