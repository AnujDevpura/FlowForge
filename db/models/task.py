from datetime import datetime
from uuid import UUID as PyUUID
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SAEnum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.enums import TaskStatus


class Task(Base):
    __tablename__ = "tasks"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    job_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("jobs.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[TaskStatus] = mapped_column(
        SAEnum(TaskStatus, name="task_status"),
        default=TaskStatus.QUEUED,
        nullable=False,
        index=True,
    )
    payload: Mapped[dict] = mapped_column(JSONB, default=dict, nullable=False)
    retry_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)
    max_retries: Mapped[int] = mapped_column(Integer, default=3, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    job = relationship("Job", back_populates="tasks")
    upstream_dependencies = relationship(
        "Dependency",
        foreign_keys="Dependency.task_id",
        back_populates="task",
        cascade="all, delete-orphan",
    )
    downstream_dependents = relationship(
        "Dependency",
        foreign_keys="Dependency.depends_on_task_id",
        back_populates="depends_on_task",
        cascade="all, delete-orphan",
    )
