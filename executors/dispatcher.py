from executors.http import HTTPExecutor
from executors.print import PrintExecutor


EXECUTOR_MAP = {
    "print": PrintExecutor(),
    "http": HTTPExecutor(),
}


async def execute_task(
    payload: dict,
):

    task_type = payload.get("type")

    executor = EXECUTOR_MAP.get(
        task_type
    )

    if not executor:
        raise ValueError(
            f"Unknown task type: {task_type}"
        )

    await executor.execute(payload)