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