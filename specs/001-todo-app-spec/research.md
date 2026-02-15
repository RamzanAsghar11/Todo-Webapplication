# Research: Todo Application (Core CRUD)

**Feature**: 001-todo-app-spec
**Date**: 2026-02-12
**Purpose**: Resolve technical unknowns and establish implementation patterns

## 1. FastAPI + SQLModel Integration Patterns

### Research Question
What are the best practices for integrating SQLModel with FastAPI, particularly around database session management and async operations?

### Findings

**SQLModel with FastAPI Best Practices:**
- SQLModel is built on top of SQLAlchemy and Pydantic, designed specifically for FastAPI integration
- Use dependency injection for database sessions to ensure proper lifecycle management
- SQLModel supports both sync and async operations; async is preferred for FastAPI to avoid blocking

**Database Session Management Pattern:**
```python
# Recommended pattern using dependency injection
from sqlmodel import Session, create_engine

engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session

# Usage in route
@app.get("/items")
def get_items(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()
```

**Async vs Sync Decision:**
- **Decision**: Use **sync** SQLModel operations for this phase
- **Rationale**:
  - Simpler implementation for CRUD operations
  - Neon PostgreSQL supports both sync and async
  - Performance difference negligible for <1000 tasks per user
  - Async adds complexity without significant benefit at this scale
  - Can migrate to async later if needed

**Model Definition Pattern:**
- Use SQLModel class with `table=True` for database tables
- Separate read/write schemas using Pydantic models if needed
- Use `Field()` for constraints and defaults

### Decision

**Adopt sync SQLModel with dependency injection pattern:**
- database.py: Create engine and session factory
- Use `Depends(get_session)` in all route handlers
- Define models with SQLModel table classes
- Use context manager for session lifecycle

---

## 2. Next.js 16+ App Router Patterns

### Research Question
What are the recommended patterns for data fetching, Server Components vs Client Components, and form handling in Next.js 16+ App Router?

### Findings

**Server Components vs Client Components:**
- Server Components: Default in App Router, render on server, no JavaScript sent to client
- Client Components: Marked with `'use client'`, needed for interactivity (onClick, useState, etc.)
- Recommendation: Use Server Components by default, Client Components only when needed

**Data Fetching Patterns:**
- **Server Components**: Can fetch data directly in component (async/await)
- **Client Components**: Use fetch in useEffect or React Query/SWR
- **Server Actions**: New pattern for mutations, but still experimental

**For This Project:**
- **Decision**: Use **Client Components with client-side fetch**
- **Rationale**:
  - Task list needs real-time interactivity (create, update, delete, toggle)
  - Client-side state management simpler for CRUD operations
  - Avoids Server Actions complexity (still experimental)
  - Better user experience with optimistic updates
  - Clearer separation: backend API handles all logic, frontend just displays

**Form Handling:**
- Use controlled components with React state
- Handle form submission with async fetch to backend API
- Display loading states during submission
- Show validation errors from backend

### Decision

**Adopt Client Component pattern with API client:**
- Mark interactive components with `'use client'`
- Create centralized API client in `lib/api.ts`
- Use React state for form handling
- Fetch data on component mount and after mutations

---

## 3. Neon PostgreSQL Connection

### Research Question
What is the correct connection string format for Neon PostgreSQL, and what are the connection pooling and SSL requirements?

### Findings

**Neon Connection String Format:**
```
postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require
```

**Key Requirements:**
- SSL/TLS is **required** for Neon connections (`sslmode=require`)
- Connection pooling is handled by Neon's proxy layer
- No additional pooling configuration needed for small-scale apps
- Connection string provided by Neon dashboard

**SQLModel/SQLAlchemy Configuration:**
```python
from sqlmodel import create_engine

# Neon requires SSL
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries (disable in production)
    connect_args={"sslmode": "require"}  # Required for Neon
)
```

**Environment Variable:**
- Store as `DATABASE_URL` in `.env`
- Never commit to version control
- Format: Full PostgreSQL connection string from Neon

### Decision

**Use Neon-provided connection string with SSL:**
- Require `DATABASE_URL` environment variable
- Add `sslmode=require` to connection string or connect_args
- Use SQLModel's create_engine with minimal configuration
- Log queries in development (echo=True), disable in production

---

## 4. Error Handling Strategy

### Research Question
What are the best practices for error handling in FastAPI and Next.js, particularly for user-friendly error messages?

### Findings

**FastAPI Error Handling:**
- Use HTTPException for expected errors (404, 400, etc.)
- Use exception handlers for unexpected errors (500)
- Return consistent error response format

**Recommended Pattern:**
```python
from fastapi import HTTPException

# For expected errors
raise HTTPException(status_code=404, detail="Task not found")

# For validation errors (automatic with Pydantic)
# FastAPI returns 422 with detailed field errors

# For unexpected errors, use exception handler
@app.exception_handler(Exception)
async def generic_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"}
    )
```

**Next.js Error Handling:**
- Use try-catch in API client functions
- Display user-friendly messages in UI
- Use error boundaries for component errors (error.tsx)
- Show loading states during async operations

**Error Response Format:**
```json
{
  "detail": "User-friendly error message",
  "field": "title"  // Optional, for validation errors
}
```

### Decision

**Adopt consistent error handling pattern:**
- Backend: Use HTTPException with descriptive detail messages
- Backend: Return 400 for validation, 404 for not found, 500 for server errors
- Frontend: Wrap API calls in try-catch
- Frontend: Display error.detail to user in alert/toast
- Frontend: Show field-specific errors for validation failures

---

## 5. Responsive UI Framework Decision

### Research Question
Which styling approach should be used for responsive UI: Tailwind CSS, CSS Modules, or styled-components?

### Findings

**Options Comparison:**

**Tailwind CSS:**
- Pros: Utility-first, fast development, built-in responsive classes, small bundle
- Cons: Verbose className strings, learning curve
- Mobile-first by default (sm:, md:, lg: breakpoints)

**CSS Modules:**
- Pros: Scoped styles, familiar CSS syntax, no runtime overhead
- Cons: More boilerplate, manual responsive breakpoints

**styled-components:**
- Pros: CSS-in-JS, dynamic styling, component-scoped
- Cons: Runtime overhead, larger bundle, requires Client Components

**For This Project:**
- **Decision**: **Tailwind CSS**
- **Rationale**:
  - Mobile-first responsive design built-in
  - Fast development with utility classes
  - No runtime overhead (build-time)
  - Works with both Server and Client Components
  - Industry standard for Next.js projects
  - Easy to implement responsive breakpoints (320px-1024px+ requirement)

**Responsive Breakpoints:**
- Default (mobile): 320px+
- sm: 640px (small tablets)
- md: 768px (tablets)
- lg: 1024px (desktops)

### Decision

**Use Tailwind CSS for styling:**
- Install Tailwind CSS in Next.js project
- Use utility classes for responsive design
- Follow mobile-first approach (base styles for mobile, add sm:/md:/lg: for larger screens)
- Use Tailwind's form plugin for consistent form styling

---

## Summary of Decisions

| Area | Decision | Rationale |
|------|----------|-----------|
| **Database Operations** | Sync SQLModel with dependency injection | Simpler, sufficient performance for scale, easier debugging |
| **Frontend Architecture** | Client Components with API client | Better interactivity, clearer separation, simpler state management |
| **Database Connection** | Neon connection string with SSL required | Neon requirement, secure by default |
| **Error Handling** | HTTPException (backend) + try-catch (frontend) | Consistent format, user-friendly messages |
| **Styling** | Tailwind CSS | Mobile-first, fast development, no runtime overhead |

## Implementation Patterns

### Backend Pattern (FastAPI + SQLModel)
```python
# database.py
from sqlmodel import create_engine, Session

engine = create_engine(DATABASE_URL, connect_args={"sslmode": "require"})

def get_session():
    with Session(engine) as session:
        yield session

# models/task.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from uuid import UUID, uuid4

class Task(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: str = Field(index=True)
    title: str = Field(max_length=500)
    description: str | None = Field(default=None, max_length=2000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

# routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

router = APIRouter()

@router.get("/api/{user_id}/tasks")
def get_tasks(user_id: str, session: Session = Depends(get_session)):
    tasks = session.exec(select(Task).where(Task.user_id == user_id)).all()
    return tasks
```

### Frontend Pattern (Next.js + Tailwind)
```typescript
// lib/api.ts
export async function getTasks(userId: string) {
  const response = await fetch(`${API_URL}/api/${userId}/tasks`);
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'Failed to fetch tasks');
  }
  return response.json();
}

// components/TaskList.tsx
'use client';

import { useEffect, useState } from 'react';
import { getTasks } from '@/lib/api';

export default function TaskList({ userId }: { userId: string }) {
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    getTasks(userId)
      .then(setTasks)
      .catch(err => setError(err.message))
      .finally(() => setLoading(false));
  }, [userId]);

  if (loading) return <div className="text-center py-8">Loading...</div>;
  if (error) return <div className="text-red-600 py-4">{error}</div>;

  return (
    <div className="space-y-4">
      {tasks.map(task => (
        <div key={task.id} className="p-4 border rounded-lg hover:shadow-md transition-shadow">
          <h3 className="text-lg font-semibold">{task.title}</h3>
          {task.description && <p className="text-gray-600 mt-2">{task.description}</p>}
        </div>
      ))}
    </div>
  );
}
```

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Neon connection issues | High - app unusable | Validate DATABASE_URL early, provide clear error messages |
| CORS errors between frontend/backend | High - API calls fail | Configure CORS middleware in FastAPI from start |
| TypeScript type mismatches | Medium - runtime errors | Define shared types, validate API responses |
| Responsive design issues | Medium - poor UX | Test on multiple screen sizes, use Tailwind breakpoints |
| Missing error handling | Medium - poor UX | Implement error handling in every API call |

## Next Steps

With research complete, proceed to Phase 1: Design & Contracts
- Create data-model.md (detailed Task entity specification)
- Create contracts/tasks-api.yaml (OpenAPI specification)
- Create quickstart.md (setup instructions)
- Update agent context with selected technologies
