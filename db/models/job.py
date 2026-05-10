from datetime import datetime
from uuid import UUID as PyUUID
from uuid import uuid4

from sqlalchemy import DateTime, Enum as SAEnum, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base
from db.enums import JobStatus


class Job(Base):
    __tablename__ = "jobs"

    id: Mapped[PyUUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    status: Mapped[JobStatus] = mapped_column(
        SAEnum(JobStatus, name="job_status"),
        default=JobStatus.PENDING,
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
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

    tasks = relationship("Task", back_populates="job", cascade="all, delete-orphan")
