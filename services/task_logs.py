from db.models.task_log import TaskLog


async def create_task_log(
    db,
    task_id,
    message: str,
):

    log = TaskLog(
        task_id=task_id,
        message=message,
    )

    db.add(log)

    await db.commit()