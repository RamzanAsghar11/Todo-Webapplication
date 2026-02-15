"""Task model for database."""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
import uuid


class Task(SQLModel, table=True):
    """Task model representing a todo item."""

    __tablename__ = "tasks"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    user_id: str = Field(
        foreign_key="users.id",
        index=True,
        nullable=False,
    )
    title: str = Field(
        nullable=False,
        max_length=500,
    )
    completed: bool = Field(
        default=False,
        nullable=False,
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    # Relationship to user
    user: Optional["User"] = Relationship(back_populates="tasks")
