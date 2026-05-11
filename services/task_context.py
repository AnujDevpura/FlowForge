from sqlalchemy import select

from db.models.task import Task
from db.models.dependency import (
    TaskDependency,
)

async def build_task_context(
    db,
    task,
):
    context = {
        "task_id": str(task.id),
        "job_id": str(task.job_id),
        "dependencies": {},
    }
    
    result = await db.execute(
        select(TaskDependency).where(
            TaskDependency.task_id == task.id
        )
    )

    dependencies = result.scalars().all()
    
    for dependency in dependencies:

        dependency_result = await db.execute(
            select(Task).where(
                Task.id
                == dependency.depends_on_task_id
            )
        )

        dependency_task = (
            dependency_result.scalar_one()
        )

        context["dependencies"][
            dependency_task.name
        ] = dependency_task.result
    
    return context