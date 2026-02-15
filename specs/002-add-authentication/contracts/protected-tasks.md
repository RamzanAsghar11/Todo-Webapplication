# API Contract: Protected Task Endpoints

**Feature**: Add Authentication to Todo Application
**Date**: 2026-02-13
**Status**: Design Complete

## Overview

This document defines the updated API contracts for task endpoints with JWT authentication. All task endpoints now require a valid JWT token and enforce user-scoped data access.

## Base URL

```
http://localhost:8001/api
```

## Authentication Requirements

### JWT Token Required

All task endpoints require a valid JWT token in the Authorization header:

```http
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### User ID Verification

The backend MUST:
1. Extract `user_id` from the JWT token payload (`sub` field)
2. Compare JWT `user_id` with the `user_id` in the URL path
3. Return 403 Forbidden if they do not match

### Error Responses for Authentication

| Status Code | Error Code | Description | Response Body |
|-------------|------------|-------------|---------------|
| 401 | `UNAUTHORIZED` | Missing or invalid JWT token | `{"detail": "Authentication required"}` |
| 401 | `TOKEN_EXPIRED` | JWT token has expired | `{"detail": "Token expired"}` |
| 401 | `INVALID_TOKEN` | JWT token signature is invalid | `{"detail": "Invalid token"}` |
| 403 | `FORBIDDEN` | JWT user_id does not match URL user_id | `{"detail": "Access denied"}` |

## Endpoints

### GET /{user_id}/tasks

Get all tasks for the authenticated user.

**Request**

```http
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Authentication Flow**

1. Extract JWT token from Authorization header
2. Verify JWT signature using BETTER_AUTH_SECRET
3. Extract `user_id` from JWT payload (`sub` field)
4. Verify JWT `user_id` matches URL `user_id`
5. If mismatch: return 403 Forbidden
6. If match: proceed with query

**Success Response (200 OK)**

```http
HTTP/1.1 200 OK
Content-Type: application/json

[
  {
    "id": 1,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Buy groceries",
    "completed": false,
    "created_at": "2026-02-13T10:00:00Z"
  },
  {
    "id": 2,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Write documentation",
    "completed": true,
    "created_at": "2026-02-13T11:00:00Z"
  }
]
```

**Response Schema**

```typescript
interface Task {
  id: number;
  user_id: string;      // UUID
  title: string;
  completed: boolean;
  created_at: string;   // ISO 8601 timestamp
}

type GetTasksResponse = Task[];
```

**Error Responses**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 401 | Missing or invalid JWT token | `{"detail": "Authentication required"}` |
| 403 | JWT user_id does not match URL user_id | `{"detail": "Access denied"}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

**Security Notes**

- Query MUST filter by authenticated user_id from JWT
- Users can ONLY see their own tasks
- Empty array returned if user has no tasks

---

### POST /{user_id}/tasks

Create a new task for the authenticated user.

**Request**

```http
POST /api/550e8400-e29b-41d4-a716-446655440000/tasks HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries"
}
```

**Request Schema**

```typescript
interface CreateTaskRequest {
  title: string;  // Required, max 500 characters
}
```

**Validation Rules**

- `title`: Required, cannot be empty
- `title`: Maximum 500 characters
- `title`: Whitespace-only strings are invalid

**Authentication Flow**

1. Verify JWT token
2. Extract `user_id` from JWT payload
3. Verify JWT `user_id` matches URL `user_id`
4. Associate new task with authenticated `user_id` (from JWT, not URL)

**Success Response (201 Created)**

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": 3,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "completed": false,
  "created_at": "2026-02-13T12:00:00Z"
}
```

**Response Schema**

```typescript
interface CreateTaskResponse {
  id: number;
  user_id: string;      // UUID from JWT payload
  title: string;
  completed: boolean;   // Always false for new tasks
  created_at: string;   // ISO 8601 timestamp
}
```

**Error Responses**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 400 | Title is empty or invalid | `{"detail": "Title cannot be empty"}` |
| 401 | Missing or invalid JWT token | `{"detail": "Authentication required"}` |
| 403 | JWT user_id does not match URL user_id | `{"detail": "Access denied"}` |
| 422 | Validation error | `{"detail": [{"loc": ["body", "title"], "msg": "field required"}]}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

**Security Notes**

- Task MUST be associated with `user_id` from JWT payload (not URL)
- This prevents users from creating tasks for other users

---

### GET /{user_id}/tasks/{id}

Get a specific task by ID.

**Request**

```http
GET /api/550e8400-e29b-41d4-a716-446655440000/tasks/1 HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Authentication Flow**

1. Verify JWT token
2. Extract `user_id` from JWT payload
3. Verify JWT `user_id` matches URL `user_id`
4. Query task by ID AND user_id (double verification)

**Success Response (200 OK)**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "completed": false,
  "created_at": "2026-02-13T10:00:00Z"
}
```

**Error Responses**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 401 | Missing or invalid JWT token | `{"detail": "Authentication required"}` |
| 403 | JWT user_id does not match URL user_id | `{"detail": "Access denied"}` |
| 404 | Task not found or does not belong to user | `{"detail": "Task not found"}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

**Security Notes**

- Query MUST filter by both task ID and authenticated user_id
- 404 returned if task exists but belongs to another user (prevents information leakage)

---

### PUT /{user_id}/tasks/{id}

Update a task's title and/or completion status.

**Request**

```http
PUT /api/550e8400-e29b-41d4-a716-446655440000/tasks/1 HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner",
  "completed": true
}
```

**Request Schema**

```typescript
interface UpdateTaskRequest {
  title?: string;       // Optional, max 500 characters
  completed?: boolean;  // Optional
}
```

**Validation Rules**

- At least one field (`title` or `completed`) must be provided
- `title`: If provided, cannot be empty, max 500 characters
- `completed`: If provided, must be boolean

**Authentication Flow**

1. Verify JWT token
2. Extract `user_id` from JWT payload
3. Verify JWT `user_id` matches URL `user_id`
4. Verify task belongs to authenticated user before updating

**Success Response (200 OK)**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries and cook dinner",
  "completed": true,
  "created_at": "2026-02-13T10:00:00Z"
}
```

**Error Responses**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 400 | Invalid request body | `{"detail": "At least one field must be provided"}` |
| 401 | Missing or invalid JWT token | `{"detail": "Authentication required"}` |
| 403 | JWT user_id does not match URL user_id | `{"detail": "Access denied"}` |
| 404 | Task not found or does not belong to user | `{"detail": "Task not found"}` |
| 422 | Validation error | `{"detail": [{"loc": ["body", "title"], "msg": "field required"}]}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

**Security Notes**

- Update MUST verify task belongs to authenticated user
- Users cannot update other users' tasks

---

### DELETE /{user_id}/tasks/{id}

Delete a task.

**Request**

```http
DELETE /api/550e8400-e29b-41d4-a716-446655440000/tasks/1 HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Authentication Flow**

1. Verify JWT token
2. Extract `user_id` from JWT payload
3. Verify JWT `user_id` matches URL `user_id`
4. Verify task belongs to authenticated user before deleting

**Success Response (204 No Content)**

```http
HTTP/1.1 204 No Content
```

**Error Responses**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 401 | Missing or invalid JWT token | `{"detail": "Authentication required"}` |
| 403 | JWT user_id does not match URL user_id | `{"detail": "Access denied"}` |
| 404 | Task not found or does not belong to user | `{"detail": "Task not found"}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

**Security Notes**

- Delete MUST verify task belongs to authenticated user
- Users cannot delete other users' tasks

---

### PATCH /{user_id}/tasks/{id}/complete

Toggle a task's completion status.

**Request**

```http
PATCH /api/550e8400-e29b-41d4-a716-446655440000/tasks/1/complete HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Authentication Flow**

1. Verify JWT token
2. Extract `user_id` from JWT payload
3. Verify JWT `user_id` matches URL `user_id`
4. Verify task belongs to authenticated user before toggling

**Success Response (200 OK)**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "id": 1,
  "user_id": "550e8400-e29b-41d4-a716-446655440000",
  "title": "Buy groceries",
  "completed": true,
  "created_at": "2026-02-13T10:00:00Z"
}
```

**Error Responses**

| Status Code | Description | Response Body |
|-------------|-------------|---------------|
| 401 | Missing or invalid JWT token | `{"detail": "Authentication required"}` |
| 403 | JWT user_id does not match URL user_id | `{"detail": "Access denied"}` |
| 404 | Task not found or does not belong to user | `{"detail": "Task not found"}` |
| 500 | Server error | `{"detail": "Internal server error"}` |

**Security Notes**

- Toggle MUST verify task belongs to authenticated user
- Users cannot toggle other users' tasks

---

## Security Implementation Checklist

### JWT Verification (All Endpoints)

- [ ] Extract JWT token from Authorization header
- [ ] Verify token signature using BETTER_AUTH_SECRET
- [ ] Check token expiration (`exp` field)
- [ ] Extract `user_id` from token payload (`sub` field)
- [ ] Return 401 if token is missing, invalid, or expired

### User ID Verification (All Endpoints)

- [ ] Compare JWT `user_id` with URL `user_id`
- [ ] Return 403 Forbidden if they do not match
- [ ] Use JWT `user_id` (not URL `user_id`) for database queries

### Data Isolation (All Endpoints)

- [ ] All queries MUST filter by authenticated `user_id`
- [ ] Users can ONLY access their own tasks
- [ ] Return 404 (not 403) if task exists but belongs to another user

### CORS Configuration

- [ ] Allow Authorization header in CORS configuration
- [ ] Allow credentials in CORS configuration

## Testing Checklist

### Authentication Tests

- [ ] Request without JWT token returns 401
- [ ] Request with invalid JWT token returns 401
- [ ] Request with expired JWT token returns 401
- [ ] Request with valid JWT token succeeds

### Authorization Tests

- [ ] User A cannot access User B's tasks (returns 403)
- [ ] User A cannot create tasks for User B (returns 403)
- [ ] User A cannot update User B's tasks (returns 404)
- [ ] User A cannot delete User B's tasks (returns 404)

### Data Isolation Tests

- [ ] GET /tasks returns only authenticated user's tasks
- [ ] POST /tasks associates task with authenticated user
- [ ] PUT /tasks only updates authenticated user's tasks
- [ ] DELETE /tasks only deletes authenticated user's tasks

## Implementation Notes

### FastAPI Dependency Injection

```python
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_jwt_and_user_id(
    user_id: str,
    credentials: HTTPAuthCredentials = Depends(security)
):
    # Verify JWT token
    payload = verify_jwt(credentials.credentials)

    # Extract user_id from JWT
    jwt_user_id = payload.get("sub")

    # Verify match
    if jwt_user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    return jwt_user_id
```

### Usage in Endpoints

```python
@router.get("/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    authenticated_user_id: str = Depends(verify_jwt_and_user_id),
    session: Session = Depends(get_session)
):
    # authenticated_user_id is guaranteed to match user_id
    statement = select(Task).where(Task.user_id == authenticated_user_id)
    tasks = session.exec(statement).all()
    return tasks
```

## Next Steps

Proceed to create `quickstart.md` with developer setup instructions for authentication.
