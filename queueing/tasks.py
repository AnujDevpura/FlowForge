import json
from uuid import UUID

from queueing.redis import redis_client


QUEUE_NAME = "task_queue"

async def enqueue_task(task_id: UUID):
    payload = {
        "task_id": str(task_id),
    }

    await redis_client.rpush(
        QUEUE_NAME,
        json.dumps(payload),
    )


DEAD_LETTER_QUEUE = "dead_letter_queue"

async def enqueue_dead_letter_task(
    task_id: UUID,
    error: str,
):

    payload = {
        "task_id": str(task_id),
        "error": error,
    }

    await redis_client.rpush(
        DEAD_LETTER_QUEUE,
        json.dumps(payload),
    )