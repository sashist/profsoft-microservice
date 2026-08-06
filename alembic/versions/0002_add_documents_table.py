"""add_documents_table

Revision ID: 0002_add_documents_table
Revises: 0001_init_or_expand_tasks
Create Date: 2026-08-06 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0002_add_documents_table"
down_revision: Union[str, Sequence[str], None] = "0001_init_or_expand_tasks"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "documents",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        sa.CheckConstraint(
            "status IN ('idle', 'syncing', 'indexed', 'failed')",
            name="ck_documents_status_valid",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_documents_source", "documents", ["source"], unique=True)


def downgrade() -> None:
    op.drop_index("ix_documents_source", table_name="documents")
    op.drop_table("documents")
