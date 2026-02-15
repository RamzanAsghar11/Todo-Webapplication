"""User model for authentication."""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List
import uuid


class User(SQLModel, table=True):
    """User model representing an authenticated user."""

    __tablename__ = "users"

    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        nullable=False,
    )
    email: str = Field(
        unique=True,
        index=True,
        nullable=False,
        max_length=255,
        sa_column_kwargs={"unique": True}
    )
    hashed_password: str = Field(
        nullable=False,
        max_length=255,
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
    )

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="user")
