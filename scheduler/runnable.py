from sqlalchemy import Select, func, select, or_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from db.enums import TaskStatus
from db.models.dependency import TaskDependency
from db.models.task import Task

async def get_runnable_tasks(
    db: AsyncSession,
):
    dependency_subquery = (
        select(
            TaskDependency.task_id,
            func.count().label("total_dependencies"),
        )
        .group_by(TaskDependency.task_id)
        .subquery()
    )

    successful_dependency_subquery = (
        select(
            TaskDependency.task_id,
            func.count().label("successful_dependencies"),
        )
        .join(
            Task,
            Task.id == TaskDependency.depends_on_task_id,
        )
        .where(
            Task.status == TaskStatus.SUCCESS
        )
        .group_by(TaskDependency.task_id)
        .subquery()
    )

    query: Select = (
        select(Task)
        .outerjoin(
            dependency_subquery,
            Task.id == dependency_subquery.c.task_id,
        )
        .outerjoin(
            successful_dependency_subquery,
            Task.id == successful_dependency_subquery.c.task_id,
        )
        .where(
            Task.status == TaskStatus.PENDING
        )
        .where(
            func.coalesce(
                dependency_subquery.c.total_dependencies,
                0,
            )
            ==
            func.coalesce(
                successful_dependency_subquery.c.successful_dependencies,
                0,
            )
        )
        
        .where(
            or_(
                Task.next_retry_at.is_(None),
                Task.next_retry_at <= datetime.utcnow(),
            )
        )
    )

    result = await db.execute(query)

    return result.scalars().all()