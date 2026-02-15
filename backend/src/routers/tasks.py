"""Task router endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List
import uuid

from ..database import get_session
from ..models.task import Task
from ..schemas.task import TaskCreate, TaskUpdate, TaskResponse
from ..middleware.jwt_auth import verify_user_access

router = APIRouter()


@router.get("/{user_id}/tasks", response_model=List[TaskResponse])
def get_tasks(
    user_id: str,
    authenticated_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Get all tasks for a user."""
    # Use authenticated_user_id from JWT, not URL parameter
    statement = select(Task).where(Task.user_id == authenticated_user_id)
    tasks = session.exec(statement).all()
    return tasks


@router.post("/{user_id}/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    user_id: str,
    task_data: TaskCreate,
    authenticated_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Create a new task for a user."""
    # Use authenticated_user_id from JWT, not URL parameter
    task = Task(
        user_id=authenticated_user_id,
        title=task_data.title,
    )
    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.get("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    user_id: str,
    task_id: uuid.UUID,
    authenticated_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Get a specific task by ID."""
    # Use authenticated_user_id from JWT, not URL parameter
    statement = select(Task).where(Task.id == task_id, Task.user_id == authenticated_user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    return task


@router.put("/{user_id}/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    user_id: str,
    task_id: uuid.UUID,
    task_data: TaskUpdate,
    authenticated_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Update a task."""
    # Use authenticated_user_id from JWT, not URL parameter
    statement = select(Task).where(Task.id == task_id, Task.user_id == authenticated_user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    # Update only provided fields
    if task_data.title is not None:
        task.title = task_data.title
    if task_data.completed is not None:
        task.completed = task_data.completed

    from datetime import datetime
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task


@router.delete("/{user_id}/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    user_id: str,
    task_id: uuid.UUID,
    authenticated_user_id: str = Depends(verify_user_access),
    session: Session = Depends(get_session),
):
    """Delete a task."""
    # Use authenticated_user_id from JWT, not URL parameter
    statement = select(Task).where(Task.id == task_id, Task.user_id == authenticated_user_id)
    task = session.exec(statement).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found",
        )

    session.delete(task)
    session.commit()
    return None
