# Phase 0 Research: Authentication Implementation

**Feature**: Add Authentication to Todo Application
**Date**: 2026-02-13
**Status**: Research Complete

## Research Objectives

1. Verify Better Auth compatibility with Next.js 16+ App Router
2. Identify optimal JWT verification library for FastAPI
3. Understand JWT payload structure from Better Auth
4. Audit existing codebase for integration points
5. Validate no breaking changes required

## Better Auth Integration Research

### Compatibility Verification

**Better Auth Version**: 0.2.0+
**Next.js Version**: 16+ (App Router)
**Compatibility Status**: ✅ Compatible

Better Auth is designed for Next.js App Router and supports:
- Server Components and Client Components
- API Routes in App Router
- JWT token issuance
- Session management
- Email/password authentication

### Required Environment Variables

**Frontend (.env.local)**:
```
BETTER_AUTH_SECRET=<cryptographically-secure-random-string-min-32-chars>
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

**Backend (.env)**:
```
BETTER_AUTH_SECRET=<same-as-frontend>
DATABASE_URL=<existing-neon-postgresql-connection-string>
```

### Better Auth Configuration

Better Auth requires:
1. Installation: `npm install better-auth`
2. Configuration file: `src/lib/auth.ts`
3. Provider wrapper in root layout
4. API route for authentication endpoints (handled by Better Auth)

### JWT Token Structure

Better Auth issues JWT tokens with the following payload structure:
```json
{
  "sub": "user-id-uuid",
  "email": "user@example.com",
  "iat": 1234567890,
  "exp": 1234654290
}
```

- `sub`: Subject (user ID)
- `email`: User email address
- `iat`: Issued at timestamp
- `exp`: Expiration timestamp (24 hours by default)

### Session Management

- Better Auth stores session in httpOnly cookies (secure)
- JWT tokens are automatically attached to requests
- Session persists across browser restarts
- Session expires after 24 hours (configurable)

### Error Handling Patterns

Better Auth provides error codes for:
- Invalid credentials: `INVALID_CREDENTIALS`
- Duplicate email: `EMAIL_ALREADY_EXISTS`
- Weak password: `WEAK_PASSWORD`
- Invalid email format: `INVALID_EMAIL`

## JWT Verification Research

### Library Comparison

| Feature | PyJWT | python-jose |
|---------|-------|-------------|
| Size | Lightweight (~50KB) | Comprehensive (~200KB) |
| Dependencies | Minimal | More dependencies |
| JWT Support | ✅ Full | ✅ Full |
| JWE Support | ❌ No | ✅ Yes |
| Maintenance | ✅ Active | ✅ Active |
| FastAPI Integration | ✅ Excellent | ✅ Excellent |

**Recommendation**: **PyJWT**

**Rationale**:
- Lightweight and sufficient for our needs
- We only need JWT verification, not JWE (JSON Web Encryption)
- Better Auth uses standard JWT format compatible with PyJWT
- Simpler API reduces complexity
- Well-maintained and widely used

### JWT Verification Process in FastAPI

```python
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials

security = HTTPBearer()

async def verify_jwt(credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(
            token,
            os.getenv("BETTER_AUTH_SECRET"),
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### Error Handling for JWT

- **Expired Token**: Return 401 Unauthorized with "Token expired" message
- **Invalid Signature**: Return 401 Unauthorized with "Invalid token" message
- **Missing Token**: Return 401 Unauthorized with "Authentication required" message
- **Malformed Token**: Return 401 Unauthorized with "Invalid token format" message

### FastAPI Dependency Injection

FastAPI's dependency injection system allows JWT verification to be applied to endpoints:

```python
@router.get("/{user_id}/tasks", dependencies=[Depends(verify_jwt)])
async def get_tasks(user_id: str, current_user: dict = Depends(verify_jwt)):
    # current_user contains decoded JWT payload
    if current_user["sub"] != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")
    # ... rest of endpoint logic
```

## Existing Codebase Audit

### Task Model (`backend/src/models/task.py`)

**Current Structure**:
```python
class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Required Changes**:
- Add `user_id` field as UUID foreign key to users table
- Add relationship to User model
- Ensure `user_id` is not nullable

**Impact**: ✅ Non-breaking (adding field, not removing)

### Task API Endpoints (`backend/src/routers/tasks.py`)

**Current Endpoints**:
- `GET /{user_id}/tasks` - Get all tasks for user
- `POST /{user_id}/tasks` - Create new task
- `GET /{user_id}/tasks/{id}` - Get specific task
- `PUT /{user_id}/tasks/{id}` - Update task
- `DELETE /{user_id}/tasks/{id}` - Delete task
- `PATCH /{user_id}/tasks/{id}/complete` - Toggle task completion

**Required Changes**:
- Add JWT verification dependency to all endpoints
- Extract user_id from JWT payload
- Verify JWT user_id matches URL user_id
- Filter queries by authenticated user_id

**Impact**: ✅ Non-breaking (adding authentication, not changing signatures)

### API Client (`frontend/src/lib/api.ts`)

**Current Structure**:
```typescript
const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001';
const USER_ID = process.env.NEXT_PUBLIC_USER_ID || 'demo-user';

export const getTasks = async () => {
  const response = await fetch(`${API_URL}/${USER_ID}/tasks`);
  return response.json();
};
```

**Required Changes**:
- Add function to retrieve JWT token from Better Auth session
- Add Authorization header to all requests
- Handle 401 and 403 errors
- Remove hardcoded USER_ID (derive from JWT)

**Impact**: ✅ Non-breaking (enhancing existing functions)

### Database Configuration (`backend/src/database.py`)

**Current Structure**:
```python
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

def get_session():
    with Session(engine) as session:
        yield session
```

**Required Changes**: ✅ None

**Impact**: No changes needed

### CORS Configuration (`backend/src/main.py`)

**Current Configuration**:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Required Changes**: ✅ None (already allows all headers including Authorization)

**Impact**: No changes needed

## Database Migration Strategy

### New Table: `users`

```sql
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_users_email ON users(email);
```

### Modify Table: `tasks`

```sql
ALTER TABLE tasks ADD COLUMN user_id UUID;
ALTER TABLE tasks ADD CONSTRAINT fk_tasks_user_id
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
```

### Handling Existing Tasks

**Options**:
1. Assign all existing tasks to a default "demo-user" account
2. Require manual migration (assign tasks to specific users)
3. Delete existing tasks (acceptable for development)

**Recommendation**: Option 1 (assign to demo-user)

**Rationale**: Preserves existing data, allows testing with pre-existing tasks

## Dependencies Required

### Frontend

```json
{
  "dependencies": {
    "better-auth": "^0.2.0"
  }
}
```

### Backend

```txt
PyJWT==2.8.0
cryptography==41.0.7
```

## Validation Checkpoints

- [X] Better Auth confirmed compatible with Next.js 16+ App Router
- [X] JWT library selected: PyJWT
- [X] Existing Task model structure documented
- [X] Existing API endpoints documented
- [X] Database migration strategy identified
- [X] No breaking changes required

## Risks Identified

1. **Better Auth Documentation**: Better Auth is relatively new; documentation may be incomplete
   - **Mitigation**: Refer to official docs and community examples

2. **JWT Secret Synchronization**: Frontend and backend must use identical BETTER_AUTH_SECRET
   - **Mitigation**: Clear documentation in quickstart.md

3. **Database Migration**: Adding user_id to existing tasks requires careful handling
   - **Mitigation**: Test migration on development database first

## Recommendations

1. ✅ Proceed with Better Auth for frontend authentication
2. ✅ Use PyJWT for backend JWT verification
3. ✅ Maintain existing API endpoint structure (user_id in URL)
4. ✅ Add JWT verification as FastAPI dependency
5. ✅ Create demo-user account for existing tasks during migration

## Next Steps

Proceed to Phase 1: Architecture & Design
- Create data-model.md with User and Task models
- Create API contracts in contracts/ directory
- Create quickstart.md with setup instructions
