# API Contract: Authentication Endpoints

**Feature**: Add Authentication to Todo Application
**Date**: 2026-02-13
**Status**: Design Complete

## Overview

This document defines the API contracts for authentication endpoints. Better Auth handles most authentication logic on the frontend, but the backend may need to support user creation and validation depending on Better Auth's architecture.

## Base URL

```
http://localhost:8001/api/auth
```

## Authentication Flow

```
┌─────────┐                    ┌──────────────┐                    ┌─────────┐
│ Browser │                    │  Better Auth │                    │ Backend │
│         │                    │  (Frontend)  │                    │  (API)  │
└────┬────┘                    └──────┬───────┘                    └────┬────┘
     │                                │                                 │
     │  1. User enters email/password │                                 │
     ├───────────────────────────────>│                                 │
     │                                │                                 │
     │                                │  2. POST /api/auth/signup       │
     │                                ├────────────────────────────────>│
     │                                │                                 │
     │                                │  3. Create user in database     │
     │                                │<────────────────────────────────┤
     │                                │                                 │
     │  4. JWT token issued           │                                 │
     │<───────────────────────────────┤                                 │
     │                                │                                 │
     │  5. Store token in session     │                                 │
     │                                │                                 │
```

## Endpoints

### POST /api/auth/signup

Create a new user account.

**Request**

```http
POST /api/auth/signup HTTP/1.1
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Schema**

```typescript
interface SignupRequest {
  email: string;      // Valid email format, max 255 characters
  password: string;   // Minimum 8 characters
}
```

**Validation Rules**

- `email`: Must match regex `^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$`
- `email`: Maximum 255 characters
- `email`: Must be unique (not already registered)
- `password`: Minimum 8 characters
- `password`: Maximum 255 characters

**Success Response (201 Created)**

```http
HTTP/1.1 201 Created
Content-Type: application/json

{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "created_at": "2026-02-13T10:30:00Z"
}
```

**Response Schema**

```typescript
interface SignupResponse {
  id: string;           // UUID
  email: string;
  created_at: string;   // ISO 8601 timestamp
}
```

**Error Responses**

| Status Code | Error Code | Description | Response Body |
|-------------|------------|-------------|---------------|
| 400 | `INVALID_EMAIL` | Email format is invalid | `{"detail": "Invalid email format"}` |
| 400 | `WEAK_PASSWORD` | Password does not meet requirements | `{"detail": "Password must be at least 8 characters"}` |
| 409 | `EMAIL_ALREADY_EXISTS` | Email is already registered | `{"detail": "Email already registered"}` |
| 422 | `VALIDATION_ERROR` | Request body validation failed | `{"detail": [{"loc": ["body", "email"], "msg": "field required"}]}` |
| 500 | `INTERNAL_ERROR` | Server error | `{"detail": "Internal server error"}` |

**Example Error Response**

```http
HTTP/1.1 409 Conflict
Content-Type: application/json

{
  "detail": "Email already registered"
}
```

---

### POST /api/auth/signin

Authenticate a user and issue a JWT token.

**Request**

```http
POST /api/auth/signin HTTP/1.1
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Schema**

```typescript
interface SigninRequest {
  email: string;
  password: string;
}
```

**Success Response (200 OK)**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 86400,
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com"
  }
}
```

**Response Schema**

```typescript
interface SigninResponse {
  access_token: string;   // JWT token
  token_type: string;     // Always "bearer"
  expires_in: number;     // Seconds until expiration (86400 = 24 hours)
  user: {
    id: string;           // UUID
    email: string;
  };
}
```

**JWT Token Payload**

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "iat": 1707820200,
  "exp": 1707906600
}
```

**Error Responses**

| Status Code | Error Code | Description | Response Body |
|-------------|------------|-------------|---------------|
| 401 | `INVALID_CREDENTIALS` | Email or password is incorrect | `{"detail": "Invalid email or password"}` |
| 422 | `VALIDATION_ERROR` | Request body validation failed | `{"detail": [{"loc": ["body", "email"], "msg": "field required"}]}` |
| 500 | `INTERNAL_ERROR` | Server error | `{"detail": "Internal server error"}` |

**Security Notes**

- Error message does not reveal whether email exists (prevents user enumeration)
- Password is never logged or exposed in error messages
- Failed login attempts should be rate-limited (future enhancement)

---

### POST /api/auth/signout

Invalidate the current user session.

**Request**

```http
POST /api/auth/signout HTTP/1.1
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Request Schema**

No request body required. JWT token must be provided in Authorization header.

**Success Response (200 OK)**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "message": "Successfully signed out"
}
```

**Response Schema**

```typescript
interface SignoutResponse {
  message: string;
}
```

**Error Responses**

| Status Code | Error Code | Description | Response Body |
|-------------|------------|-------------|---------------|
| 401 | `UNAUTHORIZED` | Missing or invalid JWT token | `{"detail": "Authentication required"}` |
| 500 | `INTERNAL_ERROR` | Server error | `{"detail": "Internal server error"}` |

**Note**: Since the backend is stateless (JWT-only), signout is primarily handled on the frontend by clearing the session. This endpoint exists for consistency but may not perform server-side actions.

---

## JWT Token Specification

### Token Format

```
Authorization: Bearer <token>
```

### Token Structure

```json
{
  "sub": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "iat": 1707820200,
  "exp": 1707906600
}
```

### Token Fields

| Field | Type | Description |
|-------|------|-------------|
| `sub` | string | Subject (user ID as UUID) |
| `email` | string | User email address |
| `iat` | number | Issued at timestamp (Unix epoch) |
| `exp` | number | Expiration timestamp (Unix epoch) |

### Token Signing

- **Algorithm**: HS256 (HMAC with SHA-256)
- **Secret**: `BETTER_AUTH_SECRET` environment variable
- **Expiration**: 24 hours (86400 seconds)

### Token Verification

Backend must verify:
1. Token signature is valid (using BETTER_AUTH_SECRET)
2. Token has not expired (`exp` > current time)
3. Token contains required fields (`sub`, `email`)

## Security Requirements

### Password Hashing

- Passwords MUST be hashed using bcrypt
- Bcrypt cost factor: 12 (recommended)
- Passwords MUST NEVER be stored in plain text
- Passwords MUST NEVER be logged

### JWT Secret

- BETTER_AUTH_SECRET MUST be at least 32 characters
- MUST be cryptographically random
- MUST be identical in frontend and backend
- MUST be stored in environment variables only

### HTTPS

- All authentication endpoints MUST use HTTPS in production
- JWT tokens MUST NOT be transmitted over HTTP in production

### Rate Limiting (Future Enhancement)

- Sign-in endpoint should be rate-limited to prevent brute force attacks
- Recommended: 5 attempts per IP per 15 minutes

## Error Response Format

All error responses follow FastAPI's standard format:

```typescript
interface ErrorResponse {
  detail: string | ValidationError[];
}

interface ValidationError {
  loc: string[];
  msg: string;
  type: string;
}
```

## Testing Checklist

- [ ] Sign up with valid email and password succeeds
- [ ] Sign up with invalid email format returns 400
- [ ] Sign up with weak password returns 400
- [ ] Sign up with duplicate email returns 409
- [ ] Sign in with valid credentials returns JWT token
- [ ] Sign in with invalid credentials returns 401
- [ ] Sign in error message does not reveal if email exists
- [ ] JWT token contains correct payload structure
- [ ] JWT token expires after 24 hours
- [ ] Sign out clears session on frontend

## Implementation Notes

**Better Auth Integration**:
- Better Auth may handle authentication entirely on the frontend
- Backend endpoints may only be needed for user creation and validation
- Verify Better Auth documentation to determine exact backend requirements

**Alternative Approach**:
- If Better Auth is fully client-side, backend may only need JWT verification
- User creation may happen through Better Auth's built-in mechanisms
- Backend endpoints may be optional depending on Better Auth architecture

## Next Steps

Proceed to create `protected-tasks.md` with updated task endpoint contracts including JWT authentication requirements.
