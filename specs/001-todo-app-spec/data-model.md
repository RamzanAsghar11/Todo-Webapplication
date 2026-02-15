# Data Model: Todo Application (Core CRUD)

**Feature**: 001-todo-app-spec
**Date**: 2026-02-12
**Purpose**: Define database schema and entity specifications

## Entity: Task

### Overview

The Task entity represents a single todo item belonging to a user. Tasks support basic CRUD operations and completion status tracking.

### Schema Definition

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| `id` | UUID | PRIMARY KEY, NOT NULL, AUTO-GENERATED | uuid4() | Unique identifier for the task |
| `user_id` | String | NOT NULL, INDEXED | - | Identifier of the user who owns this task |
| `title` | String | NOT NULL, MAX 500 chars, MIN 1 char | - | Task title (required) |
| `description` | String | NULLABLE, MAX 2000 chars | NULL | Optional detailed description |
| `completed` | Boolean | NOT NULL | false | Completion status flag |
| `created_at` | DateTime (UTC) | NOT NULL, IMMUTABLE | now() | Timestamp when task was created |
| `updated_at` | DateTime (UTC) | NOT NULL, AUTO-UPDATE | now() | Timestamp when task was last modified |

### SQLModel Implementation

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional

class Task(SQLModel, table=True):
    """
    Task entity representing a todo item.

    Attributes:
        id: Unique identifier (UUID)
        user_id: Owner identifier (string)
        title: Task title (required, 1-500 chars)
        description: Optional detailed description (max 2000 chars)
        completed: Completion status (default: false)
        created_at: Creation timestamp (auto-set, immutable)
        updated_at: Last modification timestamp (auto-update)
    """
    __tablename__ = "tasks"

    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False
    )

    user_id: str = Field(
        index=True,
        nullable=False,
        description="User identifier for task ownership"
    )

    title: str = Field(
        min_length=1,
        max_length=500,
        nullable=False,
        description="Task title (required)"
    )

    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        nullable=True,
        description="Optional task description"
    )

    completed: bool = Field(
        default=False,
        nullable=False,
        description="Task completion status"
    )

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Creation timestamp (UTC)"
    )

    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp (UTC)"
    )
```

### Validation Rules

**Title:**
- Required (cannot be null or empty)
- Minimum length: 1 character (after trimming whitespace)
- Maximum length: 500 characters
- Trimmed before storage (leading/trailing whitespace removed)

**Description:**
- Optional (can be null)
- Maximum length: 2000 characters if provided
- Empty string treated as null

**User ID:**
- Required (cannot be null or empty)
- No format validation in this phase (authentication phase will define format)
- Used for scoping all task queries

**Completed:**
- Boolean value only (true/false)
- Defaults to false on creation
- Can be toggled bidirectionally

**Timestamps:**
- Automatically set on creation (created_at)
- Automatically updated on modification (updated_at)
- Stored in UTC timezone
- Immutable after creation (created_at)

### Indexes

**Primary Index:**
- `id` (UUID) - Clustered index for fast lookups by task ID

**Secondary Index:**
- `(user_id, created_at)` - Composite index for efficient user task queries
- Supports: "Get all tasks for user X ordered by creation date"
- Improves performance for list operations

**Index Rationale:**
- Primary index on `id` enables fast single-task lookups (GET, PUT, DELETE, PATCH by ID)
- Composite index on `(user_id, created_at)` optimizes the most common query pattern: fetching all tasks for a user
- `created_at` in index supports default ordering (newest first or oldest first)

### State Transitions

**Completion Status:**
```
┌─────────────┐
│  completed  │
│   = false   │
│ (incomplete)│
└──────┬──────┘
       │
       │ PATCH /api/{user_id}/tasks/{id}/complete
       │ { completed: true }
       ↓
┌─────────────┐
│  completed  │
│   = true    │
│  (complete) │
└──────┬──────┘
       │
       │ PATCH /api/{user_id}/tasks/{id}/complete
       │ { completed: false }
       ↓
┌─────────────┐
│  completed  │
│   = false   │
│ (incomplete)│
└─────────────┘
```

**Lifecycle:**
```
     POST /api/{user_id}/tasks
              ↓
         [CREATED]
         completed=false
         created_at=now
         updated_at=now
              ↓
    ┌─────────────────┐
    │                 │
    ↓                 ↓
[UPDATE]         [TOGGLE]
PUT /tasks/{id}  PATCH /tasks/{id}/complete
updated_at=now   updated_at=now
    │                 │
    └────────┬────────┘
             ↓
        [DELETED]
    DELETE /tasks/{id}
    (permanent removal)
```

### Relationships

**Current Phase (No Authentication):**
- No foreign key relationship to User table (User table doesn't exist yet)
- `user_id` is a plain string field
- No referential integrity constraints

**Future Phase (With Authentication):**
- `user_id` will become a foreign key to `users.id`
- Add `ON DELETE CASCADE` to remove tasks when user is deleted
- Add foreign key constraint for referential integrity

### Database Table Creation

**SQL (Generated by SQLModel):**
```sql
CREATE TABLE tasks (
    id UUID PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    title VARCHAR(500) NOT NULL,
    description VARCHAR(2000),
    completed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tasks_user_id_created_at ON tasks(user_id, created_at);
```

**Table Creation Method:**
```python
from sqlmodel import SQLModel, create_engine

# Create all tables
SQLModel.metadata.create_all(engine)
```

### Data Integrity

**Constraints Enforced:**
- NOT NULL constraints on required fields
- Length constraints on title and description
- Default values for completed and timestamps
- Primary key uniqueness on id

**Constraints NOT Enforced (Deferred):**
- No foreign key constraint on user_id (no User table yet)
- No unique constraint on (user_id, title) - users can have duplicate task titles
- No check constraint on title non-empty (handled by application validation)

### Performance Considerations

**Expected Data Volume:**
- Target: Up to 1000 tasks per user
- Estimated total: 10,000-100,000 tasks (100 users)
- Table size: ~10-50 MB (with indexes)

**Query Patterns:**
- Most common: List all tasks for user (uses composite index)
- Second most: Get single task by ID (uses primary key)
- Less common: Update, delete, toggle (all use primary key)

**Optimization Strategy:**
- Composite index covers most common query
- UUID primary key provides fast lookups
- No pagination needed for <1000 tasks per user
- Future: Add pagination if users exceed 1000 tasks

### Migration Strategy

**Initial Setup:**
- Use `SQLModel.metadata.create_all(engine)` for table creation
- No migration framework needed for initial phase
- Tables created on first application startup

**Future Migrations:**
- Add Alembic for schema migrations when authentication is added
- Migration will add User table and foreign key constraint
- Existing tasks will need user_id validation before constraint addition

### Example Data

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "test-user",
  "title": "Complete project documentation",
  "description": "Write comprehensive docs for the Todo API including setup instructions and examples",
  "completed": false,
  "created_at": "2026-02-12T10:30:00Z",
  "updated_at": "2026-02-12T10:30:00Z"
}
```

```json
{
  "id": "6ba7b810-9dad-11d1-80b4-00c04fd430c8",
  "user_id": "test-user",
  "title": "Buy groceries",
  "description": null,
  "completed": true,
  "created_at": "2026-02-11T15:20:00Z",
  "updated_at": "2026-02-12T09:15:00Z"
}
```

## Summary

The Task entity provides a simple, efficient data model for todo items with:
- UUID-based identification for scalability
- User scoping via user_id field
- Flexible title and optional description
- Boolean completion tracking
- Automatic timestamp management
- Optimized indexes for common query patterns

This model satisfies all functional requirements from the specification while maintaining simplicity and performance for the target scale (up to 1000 tasks per user).
