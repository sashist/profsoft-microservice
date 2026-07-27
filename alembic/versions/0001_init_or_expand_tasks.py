"""init_or_expand_tasks

Revision ID: 0001_init_or_expand_tasks
Revises: 
Create Date: 2026-07-27 00:00:00.000000
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "0001_init_or_expand_tasks"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


STATUS_CHECK_NAME = "ck_tasks_status_valid"
EXTERNAL_ID_INDEX = "ix_tasks_external_id"


def _has_table(inspector: sa.Inspector, table_name: str) -> bool:
    return table_name in inspector.get_table_names()


def _has_column(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    columns = {column["name"] for column in inspector.get_columns(table_name)}
    return column_name in columns


def _has_check_constraint(inspector: sa.Inspector, table_name: str, name: str) -> bool:
    constraints = {constraint["name"] for constraint in inspector.get_check_constraints(table_name)}
    return name in constraints


def _has_index(inspector: sa.Inspector, table_name: str, name: str) -> bool:
    indexes = {index["name"] for index in inspector.get_indexes(table_name)}
    return name in indexes


def _has_unique_constraint(inspector: sa.Inspector, table_name: str, column_name: str) -> bool:
    unique_constraints = inspector.get_unique_constraints(table_name)
    for unique in unique_constraints:
        columns = unique.get("column_names") or []
        if column_name in columns:
            return True
    return False


def upgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_table(inspector, "tasks"):
        op.create_table(
            "tasks",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("external_id", sa.String(), nullable=False),
            sa.Column("input_text", sa.Text(), nullable=True),
            sa.Column("status", sa.String(), nullable=False),
            sa.Column("result", sa.Text(), nullable=True),
            sa.Column("attempts", sa.Integer(), nullable=False),
            sa.Column("error", sa.Text(), nullable=True),
            sa.Column("created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
            sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
            sa.CheckConstraint(
                "status IN ('pending', 'processing', 'done', 'sent', 'failed')",
                name=STATUS_CHECK_NAME,
            ),
            sa.PrimaryKeyConstraint("id"),
        )
        op.create_index(EXTERNAL_ID_INDEX, "tasks", ["external_id"], unique=True)
        return

    if not _has_column(inspector, "tasks", "input_text"):
        op.add_column("tasks", sa.Column("input_text", sa.Text(), nullable=True))

    if not _has_column(inspector, "tasks", "attempts"):
        op.add_column("tasks", sa.Column("attempts", sa.Integer(), server_default="0", nullable=False))
        op.alter_column("tasks", "attempts", server_default=None)

    if not _has_column(inspector, "tasks", "error"):
        op.add_column("tasks", sa.Column("error", sa.Text(), nullable=True))

    if not _has_column(inspector, "tasks", "updated_at"):
        op.add_column(
            "tasks",
            sa.Column("updated_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False),
        )

    if not _has_check_constraint(inspector, "tasks", STATUS_CHECK_NAME):
        op.create_check_constraint(
            STATUS_CHECK_NAME,
            "tasks",
            "status IN ('pending', 'processing', 'done', 'sent', 'failed')",
        )

    if not _has_index(inspector, "tasks", EXTERNAL_ID_INDEX) and not _has_unique_constraint(
        inspector,
        "tasks",
        "external_id",
    ):
        op.create_index(EXTERNAL_ID_INDEX, "tasks", ["external_id"], unique=True)


def downgrade() -> None:
    bind = op.get_bind()
    inspector = sa.inspect(bind)

    if not _has_table(inspector, "tasks"):
        return

    if _has_check_constraint(inspector, "tasks", STATUS_CHECK_NAME):
        op.drop_constraint(STATUS_CHECK_NAME, "tasks", type_="check")

    if _has_column(inspector, "tasks", "updated_at"):
        op.drop_column("tasks", "updated_at")

    if _has_column(inspector, "tasks", "error"):
        op.drop_column("tasks", "error")

    if _has_column(inspector, "tasks", "attempts"):
        op.drop_column("tasks", "attempts")

    if _has_column(inspector, "tasks", "input_text"):
        op.drop_column("tasks", "input_text")
