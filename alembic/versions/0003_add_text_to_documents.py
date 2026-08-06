"""add_text_to_documents

Revision ID: 0003_add_text_to_documents
Revises: 0002_add_documents_table
Create Date: 2026-08-06 00:30:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0003_add_text_to_documents"
down_revision: Union[str, Sequence[str], None] = "0002_add_documents_table"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("text", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "text")
