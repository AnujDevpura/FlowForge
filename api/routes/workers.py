from fastapi import APIRouter

from sqlalchemy import select

from db.session import AsyncSessionLocal
from db.models.worker import Worker

router = APIRouter(
    prefix="/workers",
    tags=["Workers"],
)

@router.get("/")
async def list_workers():

    async with AsyncSessionLocal() as db:

        result = await db.execute(
            select(Worker)
        )

        workers = (
            result.scalars().all()
        )

        return [
            {
                "id": str(worker.id),

                "status": worker.status,

                "last_heartbeat_at":
                    worker.last_heartbeat_at,
            }
            for worker in workers
        ]