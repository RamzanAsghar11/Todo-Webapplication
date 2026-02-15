# Phase 1 Data Model: Authentication Schema

**Feature**: Add Authentication to Todo Application
**Date**: 2026-02-13
**Status**: Design Complete

## Overview

This document defines the database schema for authentication, including the new `users` table and modifications to the existing `tasks` table to support user-scoped data access.

## Entity Relationship Diagram

```
┌─────────────────────┐
│       users         │
├─────────────────────┤
│ id (UUID, PK)       │
│ email (VARCHAR)     │◄─────┐
│ hashed_password     │      │
│ created_at          │      │ One-to-Many
└─────────────────────┘      │
                             │
                             │
┌─────────────────────┐      │
│       tasks         │      │
├─────────────────────┤      │
│ id (INT, PK)        │      │
│ user_id (UUID, FK)  │──────┘
│ title (VARCHAR)     │
│ completed (BOOL)    │
│ created_at          │
└─────────────────────┘
```

## User Model

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from uuid import UUID, uuid4

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
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
        max_length=255
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    # Relationship
    tasks: List["Task"] = Relationship(back_populates="user")
```

### Field Specifications

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL | Unique user identifier |
| `email` | VARCHAR(255) | UNIQUE, NOT NULL, INDEXED | User email address (login identifier) |
| `hashed_password` | VARCHAR(255) | NOT NULL | Bcrypt-hashed password (handled by Better Auth) |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Account creation timestamp |

### Indexes

- **Primary Key**: `id` (automatic)
- **Unique Index**: `email` (for fast lookup during authentication)

### Validation Rules

- **Email**: Must match regex pattern `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- **Password**: Minimum 8 characters (enforced by Better Auth before hashing)
- **Hashed Password**: Bcrypt hash format (60 characters)

### Security Considerations

- Passwords are NEVER stored in plain text
- Better Auth handles password hashing using bcrypt
- Email addresses are case-insensitive (normalize to lowercase before storage)
- `hashed_password` field is never exposed in API responses

## Task Model (Modified)

### SQLModel Definition

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
from uuid import UUID

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )
    user_id: UUID = Field(
        foreign_key="users.id",
        nullable=False,
        index=True
    )
    title: str = Field(
        nullable=False,
        max_length=500
    )
    completed: bool = Field(
        default=False,
        nullable=False
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False
    )

    # Relationship
    user: Optional[User] = Relationship(back_populates="tasks")
```

### Field Specifications

| Field | Type | Constraints | Description |
|-------|------|-------------|-------------|
| `id` | INTEGER | PRIMARY KEY, AUTO INCREMENT | Unique task identifier |
| `user_id` | UUID | FOREIGN KEY (users.id), NOT NULL, INDEXED | Owner of the task |
| `title` | VARCHAR(500) | NOT NULL | Task description |
| `completed` | BOOLEAN | NOT NULL, DEFAULT FALSE | Task completion status |
| `created_at` | TIMESTAMP | NOT NULL, DEFAULT NOW() | Task creation timestamp |

### Indexes

- **Primary Key**: `id` (automatic)
- **Foreign Key Index**: `user_id` (for fast filtering by user)

### Relationships

- **Many-to-One**: Task → User (each task belongs to one user)
- **Cascade Delete**: When a user is deleted, all their tasks are deleted

### Migration Notes

**Existing Tasks Handling**:
- Current tasks table has `user_id` as STRING (not UUID)
- Migration will convert existing `user_id` values to UUID format
- Existing tasks with `user_id = "demo-user"` will be assigned to a demo user account

## Database Migration Scripts

### Migration 001: Create Users Table

```sql
-- Create users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for fast authentication lookups
CREATE INDEX idx_users_email ON users(email);

-- Create demo user for existing tasks
INSERT INTO users (id, email, hashed_password, created_at)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'demo@example.com',
    '$2b$12$dummyhashfordemouseronlyfortesting',
    CURRENT_TIMESTAMP
);
```

### Migration 002: Add user_id to Tasks Table

```sql
-- Add user_id column (nullable initially for migration)
ALTER TABLE tasks ADD COLUMN user_id_new UUID;

-- Assign all existing tasks to demo user
UPDATE tasks SET user_id_new = '00000000-0000-0000-0000-000000000001';

-- Make user_id NOT NULL
ALTER TABLE tasks ALTER COLUMN user_id_new SET NOT NULL;

-- Drop old user_id column (if it exists as string)
ALTER TABLE tasks DROP COLUMN IF EXISTS user_id;

-- Rename new column to user_id
ALTER TABLE tasks RENAME COLUMN user_id_new TO user_id;

-- Add foreign key constraint
ALTER TABLE tasks ADD CONSTRAINT fk_tasks_user_id
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- Create index on user_id for query performance
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

### Rollback Script

```sql
-- Remove foreign key constraint
ALTER TABLE tasks DROP CONSTRAINT IF EXISTS fk_tasks_user_id;

-- Drop index
DROP INDEX IF EXISTS idx_tasks_user_id;

-- Remove user_id column
ALTER TABLE tasks DROP COLUMN IF EXISTS user_id;

-- Drop users table
DROP TABLE IF EXISTS users;
```

## API Response Models

### User Response (Public)

```python
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime

    class Config:
        from_attributes = True
```

**Note**: `hashed_password` is NEVER included in API responses

### Task Response (with User Info)

```python
from pydantic import BaseModel
from typing import Optional
from uuid import UUID
from datetime import datetime

class TaskResponse(BaseModel):
    id: int
    user_id: UUID
    title: str
    completed: bool
    created_at: datetime

    class Config:
        from_attributes = True
```

## Query Patterns

### Get All Tasks for User

```python
from sqlmodel import select

def get_user_tasks(session: Session, user_id: UUID) -> List[Task]:
    statement = select(Task).where(Task.user_id == user_id)
    tasks = session.exec(statement).all()
    return tasks
```

### Create Task for User

```python
def create_task(session: Session, user_id: UUID, title: str) -> Task:
    task = Task(user_id=user_id, title=title, completed=False)
    session.add(task)
    session.commit()
    session.refresh(task)
    return task
```

### Verify Task Ownership

```python
def verify_task_ownership(session: Session, task_id: int, user_id: UUID) -> bool:
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = session.exec(statement).first()
    return task is not None
```

## Performance Considerations

### Indexes

- `users.email`: Speeds up authentication lookups (O(log n) instead of O(n))
- `tasks.user_id`: Speeds up filtering tasks by user (O(log n) instead of O(n))

### Query Optimization

- Always filter tasks by `user_id` to leverage index
- Use `select(Task).where(Task.user_id == user_id)` instead of loading all tasks
- Avoid N+1 queries by using SQLModel relationships when loading user with tasks

### Expected Performance

- User lookup by email: <10ms
- Task query by user_id: <50ms (for up to 10,000 tasks per user)
- Task creation: <20ms

## Security Constraints

1. **User ID Verification**: Backend MUST verify JWT user_id matches requested user_id
2. **Password Hashing**: Passwords MUST be hashed with bcrypt (handled by Better Auth)
3. **Email Uniqueness**: Database enforces unique constraint on email
4. **Cascade Delete**: Deleting a user deletes all their tasks (data isolation)
5. **No Cross-User Access**: Queries MUST filter by authenticated user_id

## Validation Checkpoints

- [X] User model defined with all required fields
- [X] Task model updated with user_id foreign key
- [X] Relationships defined (User ↔ Tasks)
- [X] Migration scripts created
- [X] Indexes defined for performance
- [X] Security constraints documented
- [X] API response models defined (excluding sensitive fields)

## Next Steps

Proceed to create API contracts in `contracts/` directory:
- `auth-endpoints.md`: Authentication API specifications
- `protected-tasks.md`: Updated task API with JWT requirements
