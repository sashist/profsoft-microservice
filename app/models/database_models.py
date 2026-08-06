from sqlalchemy import CheckConstraint, Column, DateTime, Integer, String, Text, func

from app.db.database import Base


class Task(Base):
    """ORM model for the tasks table."""

    __tablename__ = "tasks"
    __table_args__ = (
        CheckConstraint(
            "status IN ('pending', 'processing', 'done', 'sent', 'failed')",
            name="ck_tasks_status_valid",
        ),
    )

    id = Column(Integer, primary_key=True)
    external_id = Column(String, unique=True, index=True, nullable=False)
    input_text = Column(Text, nullable=True)
    status = Column(String, default="pending", nullable=False)
    result = Column(Text, nullable=True)
    attempts = Column(Integer, default=0, nullable=False)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)


class Document(Base):
    """ORM model for tracking document indexing status."""

    __tablename__ = "documents"
    __table_args__ = (
        CheckConstraint(
            "status IN ('idle', 'syncing', 'indexed', 'failed')",
            name="ck_documents_status_valid",
        ),
    )

    id = Column(Integer, primary_key=True)
    source = Column(String, unique=True, index=True, nullable=False)
    text = Column(Text, nullable=True)
    status = Column(String, default="idle", nullable=False)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
