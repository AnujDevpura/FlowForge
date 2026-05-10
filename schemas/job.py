from typing import Any

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    name: str

    payload: dict[str, Any]

    dependencies: list[str] = Field(
        default_factory=list
    )

    max_retries: int = 3


class JobCreate(BaseModel):
    name: str

    tasks: list[TaskCreate]