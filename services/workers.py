import socket
from datetime import datetime, UTC

from sqlalchemy import select

from db.models.worker import Worker


async def register_worker(
    db,
    max_concurrency: int,
):

    hostname = socket.gethostname()

    worker = Worker(
        hostname=hostname,
        max_concurrency=max_concurrency,
    )

    db.add(worker)

    await db.commit()

    await db.refresh(worker)

    return worker


async def heartbeat_worker(
    db,
    worker_id,
):

    result = await db.execute(
        select(Worker).where(
            Worker.id == worker_id
        )
    )

    worker = result.scalar_one()

    worker.last_heartbeat_at = datetime.utcnow()

    await db.commit()