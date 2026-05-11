from fastapi import APIRouter

from sqlalchemy import func
from sqlalchemy import select

from db.models.task import Task
from db.models.worker import Worker
from db.enums import TaskStatus

from db.session import AsyncSessionLocal

router = APIRouter(
    prefix="/metrics",
    tags=["metrics"],
)

@router.get("/")
async def get_metrics():

    async with AsyncSessionLocal() as db:

        queued = await db.scalar(
            select(func.count())
            .select_from(Task)
            .where(
                Task.status
                ==
                TaskStatus.QUEUED
            )
        )

        running = await db.scalar(
            select(func.count())
            .select_from(Task)
            .where(
                Task.status
                ==
                TaskStatus.RUNNING
            )
        )

        failed = await db.scalar(
            select(func.count())
            .select_from(Task)
            .where(
                Task.status
                ==
                TaskStatus.FAILED
            )
        )

        active_workers = await db.scalar(
            select(func.count())
            .select_from(Worker)
            .where(
                Worker.status == "ACTIVE"
            )
        )

        return {
            "queued_tasks": queued,
            "running_tasks": running,
            "failed_tasks": failed,
            "active_workers": active_workers,
        }