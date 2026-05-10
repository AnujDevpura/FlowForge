from datetime import datetime
from uuid import UUID

from pydantic import BaseModel

from db.enums import JobStatus, TaskStatus


class TaskResponse(BaseModel):

    id: UUID
    name: str
    status: TaskStatus

    retry_count: int
    max_retries: int

    created_at: datetime
    queued_at: datetime | None
    started_at: datetime | None
    completed_at: datetime | None

    last_error: str | None

    model_config = {
        "from_attributes": True
    }
    
class JobResponse(BaseModel):

    id: UUID
    name: str
    status: JobStatus

    created_at: datetime
    updated_at: datetime

    tasks: list[TaskResponse]

    model_config = {
        "from_attributes": True
    }