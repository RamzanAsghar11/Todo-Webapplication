# Implementation Plan: Add Authentication to Todo Application

**Branch**: `002-add-authentication` | **Date**: 2026-02-13 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-add-authentication/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

Integrate Better Auth authentication into the existing Todo Full-Stack Web Application to enable secure multi-user access. Users will register and sign in via Better Auth on the Next.js frontend, which issues JWT tokens. The FastAPI backend will verify these tokens and enforce user-scoped data access, ensuring each user can only view and manage their own tasks. This implementation adds authentication without modifying existing task CRUD logic or API endpoint paths.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.0+ (frontend), Node.js 18+
**Primary Dependencies**: Better Auth 0.2.0+, FastAPI 0.104+, SQLModel 0.0.8+, Next.js 16+ (App Router), PyJWT (for JWT verification)
**Storage**: Neon Serverless PostgreSQL (existing database extended with users table)
**Testing**: pytest (backend), Jest/React Testing Library (frontend)
**Target Platform**: Web application (Linux server backend, browser frontend)
**Project Type**: Web (frontend + backend)
**Performance Goals**: JWT verification <100ms, authentication <2s, support 100+ concurrent users
**Constraints**: No breaking changes to existing task API, all secrets via environment variables, backward compatible database schema
**Scale/Scope**: Multi-user application, ~5 new API endpoints, 1 new database table, 3-5 frontend pages

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with `.specify/memory/constitution.md`:

- [X] **Technology Stack Mandate**: Using Next.js 16+/TypeScript (frontend), FastAPI/Python (backend), SQLModel (ORM), Neon PostgreSQL (database), Better Auth (authentication)?
- [X] **API Design & User Scoping**: All API endpoints follow `/api/{user_id}/tasks` pattern with user-scoped routes?
- [X] **Security-First Authentication**: Backend verifies JWT tokens, derives user_id from JWT payload, rejects mismatched requests?
- [X] **Database Access via SQLModel Only**: All database operations use SQLModel ORM (no raw SQL unless justified)?
- [X] **Spec-Driven Development**: Following spec → plan → tasks → implement workflow?
- [X] **Separation of Concerns**: Clear frontend/backend separation, stateless backend, no business logic in frontend?

**Violations Requiring Justification**: None. This plan fully adheres to all constitutional principles.

## Project Structure

### Documentation (this feature)

```text
specs/002-add-authentication/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output: Better Auth + JWT verification research
├── data-model.md        # Phase 1 output: User table schema and relationships
├── quickstart.md        # Phase 1 output: Setup instructions for developers
├── contracts/           # Phase 1 output: API contracts
│   ├── auth-endpoints.md       # POST /auth/signup, POST /auth/signin, POST /auth/signout
│   └── protected-tasks.md      # Updated task endpoints with JWT requirements
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── models/
│   │   ├── task.py              # Existing (add user_id foreign key)
│   │   └── user.py              # NEW: User model with SQLModel
│   ├── routers/
│   │   ├── tasks.py             # Existing (add JWT verification)
│   │   └── auth.py              # NEW: Authentication endpoints
│   ├── middleware/
│   │   └── jwt_auth.py          # NEW: JWT verification middleware
│   ├── database.py              # Existing (no changes)
│   └── main.py                  # Existing (register auth router)
├── tests/
│   ├── test_auth.py             # NEW: Authentication flow tests
│   └── test_tasks_auth.py       # NEW: Protected task endpoint tests
├── .env                         # Add BETTER_AUTH_SECRET, DATABASE_URL
└── requirements.txt             # Add PyJWT, python-jose

frontend/
├── src/
│   ├── app/
│   │   ├── (auth)/              # NEW: Auth route group
│   │   │   ├── signin/
│   │   │   │   └── page.tsx     # NEW: Sign-in page
│   │   │   └── signup/
│   │   │       └── page.tsx     # NEW: Sign-up page
│   │   ├── page.tsx             # Existing (add auth check, redirect)
│   │   └── layout.tsx           # Existing (add Better Auth provider)
│   ├── lib/
│   │   ├── auth.ts              # NEW: Better Auth configuration
│   │   └── api.ts               # Existing (add JWT token to headers)
│   └── components/
│       ├── AuthProvider.tsx     # NEW: Better Auth context provider
│       └── SignOutButton.tsx    # NEW: Sign-out button component
├── .env.local                   # Add BETTER_AUTH_SECRET, NEXT_PUBLIC_APP_URL
└── package.json                 # Add better-auth dependency
```

**Structure Decision**: Web application structure (Option 2) with separate backend/ and frontend/ directories. This matches the existing project layout and maintains clear separation between Python FastAPI backend and Next.js frontend.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

No violations. This plan adheres to all constitutional principles.

## Phase 0: Pre-flight Research & Validation

**Objective**: Verify Better Auth compatibility, understand JWT flow, and validate existing codebase readiness.

**Agent**: Use `better-auth-security` agent for Better Auth research, `fastapi-backend-dev` agent for JWT verification research.

### Research Tasks

1. **Better Auth Integration Research** (`research.md`)
   - Verify Better Auth 0.2.0+ compatibility with Next.js 16+ App Router
   - Document Better Auth JWT configuration options
   - Identify required environment variables (BETTER_AUTH_SECRET, NEXT_PUBLIC_APP_URL)
   - Document Better Auth session management and token issuance
   - Research Better Auth error handling patterns

2. **JWT Verification Research** (`research.md`)
   - Identify Python JWT libraries (PyJWT vs python-jose)
   - Document JWT verification process in FastAPI
   - Research JWT payload structure from Better Auth
   - Document error handling for expired/invalid tokens
   - Research FastAPI dependency injection for JWT verification

3. **Existing Codebase Audit**
   - Read `backend/src/models/task.py` to understand current Task model
   - Read `backend/src/routers/tasks.py` to understand current API endpoints
   - Read `frontend/src/lib/api.ts` to understand current API client
   - Verify database connection configuration in `backend/src/database.py`
   - Confirm CORS configuration in `backend/src/main.py` allows authentication headers

### Validation Checkpoints

- [ ] Better Auth confirmed compatible with Next.js 16+ App Router
- [ ] JWT library selected for FastAPI (PyJWT or python-jose)
- [ ] Existing Task model structure documented
- [ ] Existing API endpoints documented
- [ ] Database migration strategy identified (add user_id column to tasks table)

### Deliverables

- `specs/002-add-authentication/research.md` with findings and recommendations
- List of required dependencies (better-auth, PyJWT/python-jose)
- Confirmation that no breaking changes are required

## Phase 1: Architecture & Design

**Objective**: Define data models, API contracts, and integration points.

**Agent**: Use `database-architect` for schema design, `sqlmodel-expert` for SQLModel implementation, `better-auth-security` for auth flow design.

### Design Tasks

1. **Data Model Design** (`data-model.md`)
   - Define User model with SQLModel (id, email, hashed_password, created_at)
   - Define relationship between User and Task (one-to-many)
   - Design migration to add user_id foreign key to tasks table
   - Document password hashing strategy (bcrypt via Better Auth)
   - Define indexes for performance (user_id on tasks table)

2. **API Contract Definition** (`contracts/`)
   - **Authentication Endpoints** (`contracts/auth-endpoints.md`):
     - POST /auth/signup: Request/response schemas, validation rules, error codes
     - POST /auth/signin: Request/response schemas, JWT token format, error codes
     - POST /auth/signout: Request/response schemas, session invalidation
   - **Protected Task Endpoints** (`contracts/protected-tasks.md`):
     - Document JWT requirement in Authorization header
     - Define 401 Unauthorized and 403 Forbidden error responses
     - Specify user_id extraction from JWT payload
     - Document user_id validation (JWT user_id must match URL user_id)

3. **Integration Points** (`quickstart.md`)
   - Document environment variable setup for both frontend and backend
   - Define Better Auth configuration in Next.js
   - Define JWT verification middleware in FastAPI
   - Document CORS updates (if needed) for authentication headers
   - Create developer setup instructions

### Design Decisions

**Decision 1: JWT Library Selection**
- **Options**: PyJWT (lightweight) vs python-jose (comprehensive)
- **Choice**: PyJWT (recommended for simplicity and Better Auth compatibility)
- **Rationale**: PyJWT is lightweight, well-maintained, and sufficient for JWT verification. python-jose adds unnecessary complexity for our use case.

**Decision 2: Password Hashing**
- **Options**: Implement in backend vs rely on Better Auth
- **Choice**: Rely on Better Auth for password hashing
- **Rationale**: Better Auth handles password hashing securely. Duplicating this logic in the backend violates DRY and increases attack surface.

**Decision 3: Session Storage**
- **Options**: Server-side sessions vs JWT-only
- **Choice**: JWT-only (stateless backend)
- **Rationale**: Aligns with constitutional principle of stateless backend. Better Auth issues JWT tokens that contain all necessary session information.

**Decision 4: User ID in URL**
- **Options**: Keep user_id in URL vs remove it
- **Choice**: Keep user_id in URL, verify against JWT
- **Rationale**: Maintains backward compatibility with existing API structure. Backend verifies JWT user_id matches URL user_id for security.

### Validation Checkpoints

- [ ] User model defined with all required fields
- [ ] Task model updated with user_id foreign key
- [ ] All API contracts documented with request/response schemas
- [ ] JWT verification flow documented
- [ ] Environment variable requirements documented
- [ ] Database migration strategy defined

### Deliverables

- `specs/002-add-authentication/data-model.md`
- `specs/002-add-authentication/contracts/auth-endpoints.md`
- `specs/002-add-authentication/contracts/protected-tasks.md`
- `specs/002-add-authentication/quickstart.md`

## Phase 2: Frontend Authentication Setup

**Objective**: Install Better Auth, create sign-up/sign-in pages, configure JWT token handling.

**Agent**: Use `better-auth-security` agent for Better Auth implementation, `frontend-ui-designer` agent for UI components.

### Implementation Tasks

1. **Install Better Auth**
   - Add better-auth to frontend/package.json
   - Run npm install
   - Verify installation

2. **Configure Better Auth** (`frontend/src/lib/auth.ts`)
   - Create Better Auth client configuration
   - Set BETTER_AUTH_SECRET from environment variable
   - Set NEXT_PUBLIC_APP_URL from environment variable
   - Configure JWT token issuance
   - Configure session management (24-hour expiration)

3. **Create Authentication Pages**
   - **Sign-up Page** (`frontend/src/app/(auth)/signup/page.tsx`):
     - Email and password input fields
     - Form validation (email format, password minimum 8 characters)
     - Better Auth signup integration
     - Error handling and display
     - Redirect to tasks page on success
   - **Sign-in Page** (`frontend/src/app/(auth)/signin/page.tsx`):
     - Email and password input fields
     - Better Auth signin integration
     - Error handling and display
     - Redirect to tasks page on success

4. **Update API Client** (`frontend/src/lib/api.ts`)
   - Add function to retrieve JWT token from Better Auth session
   - Update all API calls to include Authorization: Bearer <token> header
   - Add error handling for 401 Unauthorized (redirect to sign-in)
   - Add error handling for 403 Forbidden (show error message)

5. **Add Authentication Provider** (`frontend/src/app/layout.tsx`)
   - Wrap application with Better Auth provider
   - Ensure session is available to all components

6. **Protect Task Page** (`frontend/src/app/page.tsx`)
   - Check authentication status on page load
   - Redirect to sign-in page if not authenticated
   - Show loading state during authentication check

7. **Add Sign-out Functionality** (`frontend/src/components/SignOutButton.tsx`)
   - Create sign-out button component
   - Call Better Auth signout function
   - Redirect to sign-in page after sign-out

### Validation Checkpoints

- [ ] Better Auth installed and configured
- [ ] Sign-up page functional with validation
- [ ] Sign-in page functional with error handling
- [ ] JWT token attached to all API requests
- [ ] Unauthenticated users redirected to sign-in
- [ ] Sign-out functionality working

### Testing

- Manual test: Register new user
- Manual test: Sign in with registered user
- Manual test: Sign out and verify redirect
- Manual test: Try accessing tasks page without authentication
- Manual test: Verify JWT token in browser developer tools

## Phase 3: Backend User Model & Database Migration

**Objective**: Create User model, add user_id to Task model, run database migration.

**Agent**: Use `sqlmodel-expert` agent for SQLModel implementation, `database-architect` agent for migration.

### Implementation Tasks

1. **Create User Model** (`backend/src/models/user.py`)
   - Define User class with SQLModel
   - Fields: id (UUID, primary key), email (String, unique, indexed), hashed_password (String), created_at (DateTime)
   - Add table=True to create database table
   - Add validation for email format

2. **Update Task Model** (`backend/src/models/task.py`)
   - Add user_id field (UUID, foreign key to users.id)
   - Add relationship to User model
   - Ensure user_id is required (not nullable)

3. **Create Database Migration**
   - Create migration script to add users table
   - Create migration script to add user_id column to tasks table
   - Add index on tasks.user_id for query performance
   - Handle existing tasks (assign to default user or require manual migration)

4. **Run Migration**
   - **STOP HERE**: Ask user for database credentials if not in .env
   - Execute migration against Neon PostgreSQL database
   - Verify users table created
   - Verify tasks.user_id column added
   - Verify indexes created

### Validation Checkpoints

- [ ] User model defined with all fields
- [ ] Task model updated with user_id foreign key
- [ ] Migration scripts created
- [ ] Migration executed successfully
- [ ] Database schema verified

### Testing

- Query database to verify users table exists
- Query database to verify tasks.user_id column exists
- Verify indexes created on tasks.user_id

## Phase 4: Backend JWT Verification Middleware

**Objective**: Implement JWT verification middleware to authenticate requests.

**Agent**: Use `fastapi-backend-dev` agent for FastAPI middleware, `better-auth-security` agent for JWT verification.

### Implementation Tasks

1. **Install JWT Library**
   - Add PyJWT to backend/requirements.txt
   - Run pip install -r requirements.txt
   - Verify installation

2. **Create JWT Verification Middleware** (`backend/src/middleware/jwt_auth.py`)
   - Create dependency function for FastAPI
   - Extract JWT token from Authorization header
   - Verify token signature using BETTER_AUTH_SECRET
   - Decode token payload to extract user_id and email
   - Handle expired tokens (return 401 Unauthorized)
   - Handle invalid tokens (return 401 Unauthorized)
   - Handle missing tokens (return 401 Unauthorized)
   - Return authenticated user information

3. **Update Task Endpoints** (`backend/src/routers/tasks.py`)
   - Add JWT verification dependency to all task endpoints
   - Extract user_id from JWT payload
   - Verify JWT user_id matches URL user_id parameter
   - Return 403 Forbidden if user_id mismatch
   - Filter task queries by authenticated user_id
   - Ensure task creation associates task with authenticated user

4. **Update CORS Configuration** (`backend/src/main.py`)
   - Verify Authorization header is allowed in CORS
   - Add "Authorization" to allow_headers if not present

### Validation Checkpoints

- [ ] PyJWT installed
- [ ] JWT verification middleware implemented
- [ ] All task endpoints protected with JWT verification
- [ ] User ID mismatch returns 403 Forbidden
- [ ] Missing/invalid token returns 401 Unauthorized
- [ ] CORS allows Authorization header

### Testing

- Test with valid JWT token: should succeed
- Test with expired JWT token: should return 401
- Test with invalid JWT token: should return 401
- Test with missing JWT token: should return 401
- Test with mismatched user_id: should return 403

## Phase 5: Backend Authentication Endpoints

**Objective**: Create sign-up and sign-in endpoints (if needed for backend validation).

**Agent**: Use `fastapi-backend-dev` agent for endpoint implementation.

### Implementation Tasks

**Note**: Better Auth handles authentication on the frontend. Backend endpoints are only needed if Better Auth requires backend validation or if we need server-side user management.

1. **Evaluate Need for Backend Auth Endpoints**
   - Review Better Auth documentation
   - Determine if Better Auth handles all authentication server-side
   - If Better Auth is fully client-side, backend auth endpoints may not be needed

2. **Create Authentication Router** (`backend/src/routers/auth.py`) - ONLY IF NEEDED
   - POST /auth/signup: Create new user (if Better Auth requires backend)
   - POST /auth/signin: Validate credentials (if Better Auth requires backend)
   - Use SQLModel to query User table
   - Return appropriate error codes

3. **Register Auth Router** (`backend/src/main.py`) - ONLY IF NEEDED
   - Import auth router
   - Register with app.include_router()

### Validation Checkpoints

- [ ] Determined if backend auth endpoints are needed
- [ ] If needed: endpoints implemented and tested
- [ ] If not needed: documented why they're not required

### Testing

- If endpoints created: test sign-up and sign-in flows
- If endpoints not created: verify Better Auth handles all authentication

## Phase 6: Integration Testing & Validation

**Objective**: Test end-to-end authentication flow and verify all acceptance criteria.

**Agent**: Use `better-auth-security` agent for authentication testing.

### Testing Tasks

1. **End-to-End Authentication Flow**
   - Register new user via frontend
   - Verify user created in database
   - Sign in with registered user
   - Verify JWT token issued
   - Access tasks page
   - Verify tasks API call includes JWT token
   - Create new task
   - Verify task associated with authenticated user
   - Sign out
   - Verify redirect to sign-in page

2. **Security Testing**
   - Attempt to access tasks without authentication (should fail)
   - Attempt to access another user's tasks (should fail)
   - Attempt to use expired JWT token (should fail)
   - Attempt to use invalid JWT token (should fail)
   - Verify user_id mismatch returns 403

3. **Error Handling Testing**
   - Test sign-up with invalid email format
   - Test sign-up with weak password
   - Test sign-up with duplicate email
   - Test sign-in with incorrect password
   - Test sign-in with non-existent email

4. **Acceptance Criteria Validation** (from spec.md)
   - [ ] Users can register with email and password (FR-001, FR-002, FR-003)
   - [ ] Users can sign in with email and password (FR-004)
   - [ ] JWT tokens issued upon successful authentication (FR-005)
   - [ ] JWT tokens attached to all API requests (FR-006)
   - [ ] Backend verifies JWT tokens on all protected endpoints (FR-007)
   - [ ] Invalid/expired tokens rejected (FR-008)
   - [ ] Tasks associated with authenticated user (FR-009)
   - [ ] Task queries filtered by user (FR-010)
   - [ ] Users cannot access other users' tasks (FR-011)
   - [ ] Unauthenticated users redirected to sign-in (FR-012)
   - [ ] Sign-out function works (FR-013)
   - [ ] Secrets loaded from environment variables (FR-014)
   - [ ] Clear error messages displayed (FR-015)
   - [ ] Sessions persist across page refreshes (FR-016)
   - [ ] Errors handled gracefully (FR-017)
   - [ ] Duplicate email registrations prevented (FR-018)

### Validation Checkpoints

- [ ] All end-to-end tests passing
- [ ] All security tests passing
- [ ] All error handling tests passing
- [ ] All 18 functional requirements validated
- [ ] All 8 success criteria met

### Deliverables

- Test results documented
- Any bugs identified and fixed
- Acceptance criteria validation report

## Phase 7: Hardening & Documentation

**Objective**: Finalize implementation, update documentation, prepare for production.

**Agent**: Use `better-auth-security` agent for security review.

### Hardening Tasks

1. **Security Review**
   - Verify all secrets in environment variables (no hardcoded secrets)
   - Verify password hashing is secure
   - Verify JWT signature verification is correct
   - Verify CORS configuration is secure
   - Verify error messages don't leak sensitive information

2. **Performance Validation**
   - Measure JWT verification latency (must be <100ms)
   - Measure authentication response time (must be <2s)
   - Verify database queries are indexed and performant

3. **Documentation Updates**
   - Update README with authentication setup instructions
   - Document environment variables required
   - Document authentication flow for developers
   - Update API documentation with authentication requirements

4. **Environment Variable Checklist**
   - **Frontend (.env.local)**:
     - BETTER_AUTH_SECRET (shared secret for JWT signing)
     - NEXT_PUBLIC_APP_URL (application URL)
   - **Backend (.env)**:
     - BETTER_AUTH_SECRET (same as frontend, for JWT verification)
     - DATABASE_URL (existing, verify it's set)

5. **Deployment Readiness**
   - Verify application runs without errors
   - Verify all tests pass
   - Verify no console errors in browser
   - Verify no runtime errors in backend logs

### Validation Checkpoints

- [ ] Security review completed
- [ ] Performance requirements met
- [ ] Documentation updated
- [ ] Environment variables documented
- [ ] Application production-ready

### Deliverables

- Updated README.md
- Environment variable documentation
- Security review report
- Performance validation report

## Risk Analysis & Mitigation

### Risk 1: Better Auth Compatibility Issues
**Probability**: Medium | **Impact**: High | **Blast Radius**: Entire authentication system

**Mitigation**:
- Phase 0 research validates Better Auth compatibility before implementation
- If incompatible, fallback to NextAuth.js or custom JWT implementation
- Kill switch: Can revert to unauthenticated mode if critical issues arise

### Risk 2: Database Migration Failure
**Probability**: Low | **Impact**: High | **Blast Radius**: Existing tasks data

**Mitigation**:
- Test migration on development database first
- Backup production database before migration
- Create rollback script to remove user_id column if needed
- Existing tasks can be assigned to a default user if migration fails

### Risk 3: JWT Secret Mismatch Between Frontend and Backend
**Probability**: Medium | **Impact**: High | **Blast Radius**: All authentication

**Mitigation**:
- Document clearly that BETTER_AUTH_SECRET must be identical in both .env files
- Add validation step in Phase 6 to verify JWT tokens work end-to-end
- Provide clear error messages if JWT verification fails

### Risk 4: Breaking Changes to Existing Task API
**Probability**: Low | **Impact**: High | **Blast Radius**: Existing functionality

**Mitigation**:
- Constitution mandates no breaking changes
- Phase 0 audit validates existing API structure
- Integration tests verify existing task CRUD still works
- Rollback plan: Remove JWT verification middleware if issues arise

## Definition of Done

### Implementation Complete When:
- [ ] All 7 phases completed
- [ ] All validation checkpoints passed
- [ ] All 18 functional requirements implemented
- [ ] All 8 success criteria met
- [ ] All tests passing (manual and automated)
- [ ] No runtime or build errors
- [ ] Documentation updated
- [ ] Security review completed
- [ ] Performance requirements met

### Acceptance Criteria (from spec.md):
- [ ] Users can register with email and password
- [ ] Users can sign in with email and password
- [ ] Users can sign out
- [ ] JWT tokens issued upon successful authentication
- [ ] JWT tokens attached to all API requests
- [ ] Backend verifies JWT tokens on all task endpoints
- [ ] Users can only access their own tasks
- [ ] Unauthenticated users redirected to sign-in page
- [ ] All authentication secrets loaded from environment variables
- [ ] Application runs without errors

## Next Steps

1. **Immediate**: Run `/sp.tasks` to generate task breakdown from this plan
2. **After Tasks**: Run `/sp.implement` to execute tasks via Claude Code
3. **After Implementation**: Validate against acceptance criteria
4. **Final**: Create pull request and merge to main branch

## Architectural Decision Records

📋 **Architectural decision detected**: JWT-based authentication with Better Auth frontend and FastAPI backend verification

This plan includes several architecturally significant decisions:
1. **JWT Library Selection** (PyJWT vs python-jose)
2. **Password Hashing Strategy** (Better Auth vs backend implementation)
3. **Session Storage** (JWT-only vs server-side sessions)
4. **User ID Verification** (Keep user_id in URL vs remove it)

**Recommendation**: Document these decisions with `/sp.adr better-auth-jwt-architecture` after plan approval.
