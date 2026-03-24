"""create photos table

Revision ID: a94ee3e0e2cd
Revises:
Create Date: 2026-03-24
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "a94ee3e0e2cd"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "photos",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("file_id", sa.String(length=255), nullable=False),
        sa.Column("file_path", sa.String(length=1024), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_photos_user_id"), "photos", ["user_id"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_photos_user_id"), table_name="photos")
    op.drop_table("photos")
