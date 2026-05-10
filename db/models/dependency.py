from uuid import UUID as PyUUID

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.base import Base


class Dependency(Base):
    __tablename__ = "dependencies"
    __table_args__ = (
        UniqueConstraint("task_id", "depends_on_task_id", name="uq_task_dependency"),
    )

    task_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    )
    depends_on_task_id: Mapped[PyUUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tasks.id", ondelete="CASCADE"),
        primary_key=True,
    )

    task = relationship("Task", foreign_keys=[task_id], back_populates="upstream_dependencies")
    depends_on_task = relationship(
        "Task",
        foreign_keys=[depends_on_task_id],
        back_populates="downstream_dependents",
    )
