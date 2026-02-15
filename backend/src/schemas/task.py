"""Task schemas for API request/response validation."""
from pydantic import BaseModel, Field
from datetime import datetime
import uuid


class TaskCreate(BaseModel):
    """Schema for creating a new task."""

    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Task title",
    )


class TaskUpdate(BaseModel):
    """Schema for updating an existing task."""

    title: str | None = Field(
        None,
        min_length=1,
        max_length=500,
        description="Task title",
    )
    completed: bool | None = Field(
        None,
        description="Task completion status",
    )


class TaskResponse(BaseModel):
    """Schema for task response."""

    id: uuid.UUID
    user_id: str
    title: str
    completed: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
