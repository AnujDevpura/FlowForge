from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.enums import TaskStatus
from db.models.task import Task


async def recover_expired_leases(
    db: AsyncSession,
):
    result = await db.execute(
        select(Task).where(
            Task.status == TaskStatus.RUNNING,
            Task.lease_expires_at < datetime.utcnow(),
        )
    )

    expired_tasks = result.scalars().all()
    
    for task in expired_tasks:

        print(
            f"Recovering expired task lease: {task.id}"
        )

        task.status = TaskStatus.PENDING

        task.worker_id = None

        task.started_at = None

        task.lease_expires_at = None
        
    await db.commit()