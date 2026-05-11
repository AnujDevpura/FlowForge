"""fix worker id uuid

Revision ID: 8793075abf22
Revises: 6d8d4aec7932
Create Date: 2026-05-11 20:03:38.900701

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8793075abf22'
down_revision: Union[str, Sequence[str], None] = '6d8d4aec7932'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""

    op.execute(
        """
        ALTER TABLE tasks
        ALTER COLUMN worker_id
        TYPE UUID
        USING worker_id::uuid
        """
    )


def downgrade() -> None:
    """Downgrade schema."""

    op.execute(
        """
        ALTER TABLE tasks
        ALTER COLUMN worker_id
        TYPE VARCHAR
        USING worker_id::text
        """
    )