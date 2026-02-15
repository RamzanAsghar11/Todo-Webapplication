---
description: "Task list for authentication implementation"
---

# Tasks: Add Authentication to Todo Application

**Input**: Design documents from `/specs/002-add-authentication/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Tests are NOT explicitly requested in the specification, so test tasks are excluded. Manual testing will be performed during Phase 6 validation.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- All paths are relative to repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization, environment variables, and dependency installation

- [ ] T001 Generate BETTER_AUTH_SECRET using `openssl rand -hex 32` and document in quickstart.md
- [ ] T002 Create frontend/.env.local with BETTER_AUTH_SECRET, NEXT_PUBLIC_APP_URL, NEXT_PUBLIC_API_URL
- [ ] T003 Update backend/.env with BETTER_AUTH_SECRET (same value as frontend)
- [ ] T004 [P] Install better-auth in frontend: `cd frontend && npm install better-auth`
- [ ] T005 [P] Install PyJWT in backend: `cd backend && pip install PyJWT==2.8.0 cryptography==41.0.7`
- [ ] T006 [P] Update backend/requirements.txt with PyJWT and cryptography
- [ ] T007 Verify environment variables are identical in both frontend/.env.local and backend/.env

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core database schema and models that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create backend/src/models/user.py with User SQLModel (id, email, hashed_password, created_at)
- [ ] T009 Update backend/src/models/task.py to add user_id UUID foreign key field
- [ ] T010 Create database migration script in backend/src/migrations/001_create_users_table.sql
- [ ] T011 Create database migration script in backend/src/migrations/002_add_user_id_to_tasks.sql
- [ ] T012 Run database migrations against Neon PostgreSQL (verify users table and tasks.user_id column exist)
- [ ] T013 Create demo user account with id='00000000-0000-0000-0000-000000000001' and email='demo@example.com'
- [ ] T014 Assign all existing tasks to demo user (UPDATE tasks SET user_id = '00000000-0000-0000-0000-000000000001')

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - User Registration and Sign In (Priority: P1) 🎯 MVP

**Goal**: Users can register with email/password, sign in, and sign out. JWT tokens are issued upon authentication.

**Independent Test**:
1. Navigate to sign-up page, create account with email and password
2. Sign out
3. Sign in with same credentials
4. Verify redirect to tasks page
5. Verify JWT token in browser developer tools (Application → Cookies or Local Storage)

### Frontend Authentication Setup (User Story 1)

- [ ] T015 [P] [US1] Create frontend/src/lib/auth.ts with Better Auth configuration (BETTER_AUTH_SECRET, NEXT_PUBLIC_APP_URL, JWT settings)
- [ ] T016 [P] [US1] Create frontend/src/app/(auth)/signup/page.tsx with sign-up form (email, password inputs, validation)
- [ ] T017 [P] [US1] Create frontend/src/app/(auth)/signin/page.tsx with sign-in form (email, password inputs, error handling)
- [ ] T018 [P] [US1] Create frontend/src/components/SignOutButton.tsx with sign-out functionality
- [ ] T019 [US1] Update frontend/src/app/layout.tsx to wrap app with Better Auth provider
- [ ] T020 [US1] Update frontend/src/app/page.tsx to check authentication status and redirect to /signin if not authenticated
- [ ] T021 [US1] Update frontend/src/lib/api.ts to retrieve JWT token from Better Auth session and add to Authorization header

### Backend Authentication Endpoints (User Story 1)

- [ ] T022 [P] [US1] Create backend/src/routers/auth.py with POST /api/auth/signup endpoint (create user, hash password, return user data)
- [ ] T023 [P] [US1] Add POST /api/auth/signin endpoint to backend/src/routers/auth.py (validate credentials, issue JWT token)
- [ ] T024 [P] [US1] Add POST /api/auth/signout endpoint to backend/src/routers/auth.py (invalidate session)
- [ ] T025 [US1] Register auth router in backend/src/main.py with app.include_router()
- [ ] T026 [US1] Verify CORS configuration in backend/src/main.py allows Authorization header

**Checkpoint**: At this point, User Story 1 should be fully functional - users can register, sign in, sign out, and JWT tokens are issued

---

## Phase 4: User Story 2 - Protected Task Access (Priority: P2)

**Goal**: Authenticated users can only view and manage their own tasks. Unauthenticated users are redirected to sign-in. Users cannot access other users' tasks.

**Independent Test**:
1. Create two user accounts (User A and User B)
2. Sign in as User A, create tasks
3. Sign out, sign in as User B
4. Verify User B cannot see User A's tasks
5. Try accessing task URLs without authentication - verify redirect to sign-in
6. Try accessing another user's task by guessing task ID - verify 403 or 404

### Backend JWT Verification (User Story 2)

- [ ] T027 [US2] Create backend/src/middleware/jwt_auth.py with verify_jwt dependency function (extract token, verify signature, decode payload)
- [ ] T028 [US2] Add error handling to jwt_auth.py for expired tokens (return 401 with "Token expired")
- [ ] T029 [US2] Add error handling to jwt_auth.py for invalid tokens (return 401 with "Invalid token")
- [ ] T030 [US2] Add error handling to jwt_auth.py for missing tokens (return 401 with "Authentication required")

### Protected Task Endpoints (User Story 2)

- [ ] T031 [US2] Update GET /{user_id}/tasks in backend/src/routers/tasks.py to add JWT verification dependency
- [ ] T032 [US2] Update POST /{user_id}/tasks in backend/src/routers/tasks.py to add JWT verification and verify user_id match
- [ ] T033 [US2] Update GET /{user_id}/tasks/{id} in backend/src/routers/tasks.py to add JWT verification and verify task ownership
- [ ] T034 [US2] Update PUT /{user_id}/tasks/{id} in backend/src/routers/tasks.py to add JWT verification and verify task ownership
- [ ] T035 [US2] Update DELETE /{user_id}/tasks/{id} in backend/src/routers/tasks.py to add JWT verification and verify task ownership
- [ ] T036 [US2] Update PATCH /{user_id}/tasks/{id}/complete in backend/src/routers/tasks.py to add JWT verification and verify task ownership
- [ ] T037 [US2] Add user_id mismatch check to all task endpoints (return 403 Forbidden if JWT user_id != URL user_id)
- [ ] T038 [US2] Update all task queries to filter by authenticated user_id from JWT payload (not URL parameter)

### Frontend Authorization Handling (User Story 2)

- [ ] T039 [US2] Update frontend/src/lib/api.ts to handle 401 Unauthorized responses (redirect to /signin)
- [ ] T040 [US2] Update frontend/src/lib/api.ts to handle 403 Forbidden responses (show error message)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - users can authenticate AND their tasks are protected/isolated

---

## Phase 5: User Story 3 - Seamless Session Management (Priority: P3)

**Goal**: Users remain signed in across browser sessions and page refreshes until they explicitly sign out or their session expires.

**Independent Test**:
1. Sign in successfully
2. Refresh the page - verify user remains authenticated
3. Close browser, reopen, navigate to app - verify user remains authenticated (within 24-hour window)
4. Wait for session timeout (or manually expire token) - verify redirect to sign-in

### Session Persistence (User Story 3)

- [ ] T041 [US3] Configure Better Auth session expiration to 24 hours in frontend/src/lib/auth.ts
- [ ] T042 [US3] Verify Better Auth stores session in httpOnly cookies for security
- [ ] T043 [US3] Update frontend/src/app/page.tsx to check session on mount and restore authentication state
- [ ] T044 [US3] Add session refresh logic to frontend/src/lib/api.ts to handle near-expiration tokens
- [ ] T045 [US3] Test session persistence across page refreshes (manual test)
- [ ] T046 [US3] Test session persistence across browser restarts (manual test)

**Checkpoint**: All user stories should now be independently functional - complete authentication with session management

---

## Phase 6: Integration Testing & Validation

**Purpose**: End-to-end testing and acceptance criteria validation

### End-to-End Authentication Flow

- [ ] T047 Manual test: Register new user via frontend sign-up page
- [ ] T048 Manual test: Verify user created in database (query users table)
- [ ] T049 Manual test: Sign in with registered user credentials
- [ ] T050 Manual test: Verify JWT token issued (check browser developer tools)
- [ ] T051 Manual test: Access tasks page and verify tasks API call includes Authorization header
- [ ] T052 Manual test: Create new task and verify it's associated with authenticated user
- [ ] T053 Manual test: Sign out and verify redirect to sign-in page

### Security Testing

- [ ] T054 Manual test: Attempt to access tasks without authentication (should redirect to sign-in)
- [ ] T055 Manual test: Create two users, verify User A cannot see User B's tasks
- [ ] T056 Manual test: Attempt to use expired JWT token (should return 401)
- [ ] T057 Manual test: Attempt to use invalid JWT token (should return 401)
- [ ] T058 Manual test: Verify user_id mismatch returns 403 Forbidden

### Error Handling Testing

- [ ] T059 Manual test: Sign up with invalid email format (should show error)
- [ ] T060 Manual test: Sign up with weak password (< 8 characters, should show error)
- [ ] T061 Manual test: Sign up with duplicate email (should show error)
- [ ] T062 Manual test: Sign in with incorrect password (should show error)
- [ ] T063 Manual test: Sign in with non-existent email (should show error)

### Acceptance Criteria Validation (from spec.md)

- [ ] T064 Validate FR-001: Users can register with email and password
- [ ] T065 Validate FR-002: Email format validation during registration
- [ ] T066 Validate FR-003: Password minimum 8 characters enforced
- [ ] T067 Validate FR-004: Users can sign in with email and password
- [ ] T068 Validate FR-005: JWT tokens issued upon successful authentication
- [ ] T069 Validate FR-006: JWT tokens attached to all API requests
- [ ] T070 Validate FR-007: Backend verifies JWT tokens on all protected endpoints
- [ ] T071 Validate FR-008: Invalid/expired tokens rejected
- [ ] T072 Validate FR-009: Tasks associated with authenticated user
- [ ] T073 Validate FR-010: Task queries filtered by authenticated user
- [ ] T074 Validate FR-011: Users cannot access other users' tasks
- [ ] T075 Validate FR-012: Unauthenticated users redirected to sign-in
- [ ] T076 Validate FR-013: Sign-out function works
- [ ] T077 Validate FR-014: Secrets loaded from environment variables
- [ ] T078 Validate FR-015: Clear error messages displayed
- [ ] T079 Validate FR-016: Sessions persist across page refreshes
- [ ] T080 Validate FR-017: Errors handled gracefully
- [ ] T081 Validate FR-018: Duplicate email registrations prevented

**Checkpoint**: All acceptance criteria validated - authentication is production-ready

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Security hardening, performance validation, and documentation

### Security Review

- [ ] T082 [P] Verify no hardcoded secrets in codebase (grep for BETTER_AUTH_SECRET in source files)
- [ ] T083 [P] Verify password hashing is secure (Better Auth uses bcrypt)
- [ ] T084 [P] Verify JWT signature verification is correct in backend/src/middleware/jwt_auth.py
- [ ] T085 [P] Verify CORS configuration is secure in backend/src/main.py
- [ ] T086 [P] Verify error messages don't leak sensitive information (check all auth endpoints)

### Performance Validation

- [ ] T087 Measure JWT verification latency (must be <100ms) using backend logs or profiling
- [ ] T088 Measure authentication response time (must be <2s) for sign-up and sign-in
- [ ] T089 Verify database queries use indexes (check tasks.user_id index exists)

### Documentation Updates

- [ ] T090 [P] Update README.md with authentication setup instructions
- [ ] T091 [P] Document environment variables in README.md (BETTER_AUTH_SECRET, NEXT_PUBLIC_APP_URL, DATABASE_URL)
- [ ] T092 [P] Document authentication flow for developers in README.md or docs/
- [ ] T093 [P] Update API documentation with authentication requirements (Authorization header format)

### Deployment Readiness

- [ ] T094 Verify frontend runs without errors (check browser console)
- [ ] T095 Verify backend runs without errors (check server logs)
- [ ] T096 Verify no TypeScript compilation errors in frontend
- [ ] T097 Verify no Python runtime errors in backend
- [ ] T098 Run quickstart.md validation checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - Depends on US1 for authentication context
  - User Story 3 (P3): Can start after Foundational - Depends on US1 for session management
- **Integration Testing (Phase 6)**: Depends on all user stories being complete
- **Polish (Phase 7)**: Depends on Integration Testing completion

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Depends on User Story 1 (needs authentication to protect tasks)
- **User Story 3 (P3)**: Depends on User Story 1 (needs authentication to manage sessions)

**Recommended Execution Order**: Phase 1 → Phase 2 → Phase 3 (US1) → Phase 4 (US2) → Phase 5 (US3) → Phase 6 → Phase 7

### Within Each User Story

- Frontend and backend tasks can be worked on in parallel within a story
- Tasks marked [P] can run in parallel (different files, no dependencies)
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- **Phase 1 (Setup)**: T004, T005, T006 can run in parallel (different package managers)
- **Phase 2 (Foundational)**: T008, T009, T010, T011 can run in parallel (different files)
- **Phase 3 (US1)**: T015-T018 (frontend) and T022-T024 (backend) can run in parallel
- **Phase 4 (US2)**: T031-T036 (task endpoints) can be updated in parallel if careful with file conflicts
- **Phase 7 (Polish)**: T082-T086 (security review) and T090-T093 (documentation) can run in parallel

---

## Parallel Example: User Story 1

```bash
# Launch frontend auth setup tasks together:
Task: "Create frontend/src/lib/auth.ts with Better Auth configuration"
Task: "Create frontend/src/app/(auth)/signup/page.tsx with sign-up form"
Task: "Create frontend/src/app/(auth)/signin/page.tsx with sign-in form"
Task: "Create frontend/src/components/SignOutButton.tsx with sign-out functionality"

# Launch backend auth endpoints together:
Task: "Create backend/src/routers/auth.py with POST /api/auth/signup endpoint"
Task: "Add POST /api/auth/signin endpoint to backend/src/routers/auth.py"
Task: "Add POST /api/auth/signout endpoint to backend/src/routers/auth.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T007)
2. Complete Phase 2: Foundational (T008-T014) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T015-T026)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Can users register and sign in?
   - Are JWT tokens issued?
   - Does sign-out work?
5. Deploy/demo if ready

**MVP Scope**: After Phase 3, you have a working authentication system. Users can register, sign in, and sign out. This is the minimum viable product.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP! 🎯)
3. Add User Story 2 → Test independently → Deploy/Demo (Protected tasks)
4. Add User Story 3 → Test independently → Deploy/Demo (Session persistence)
5. Complete Integration Testing → Validate all acceptance criteria
6. Complete Polish → Production-ready
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together (T001-T014)
2. Once Foundational is done:
   - Developer A: User Story 1 (T015-T026) - Authentication
   - Developer B: Can start User Story 2 prep (read contracts, plan implementation)
3. After US1 complete:
   - Developer A: User Story 3 (T041-T046) - Session management
   - Developer B: User Story 2 (T027-T040) - Protected tasks
4. Both developers: Integration Testing (T047-T081)
5. Both developers: Polish (T082-T098)

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Manual testing is used instead of automated tests (not requested in spec)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **CRITICAL**: Verify BETTER_AUTH_SECRET is identical in frontend and backend
- **SECURITY**: Never commit .env or .env.local files to version control
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Count Summary

- **Phase 1 (Setup)**: 7 tasks
- **Phase 2 (Foundational)**: 7 tasks
- **Phase 3 (User Story 1)**: 12 tasks
- **Phase 4 (User Story 2)**: 14 tasks
- **Phase 5 (User Story 3)**: 6 tasks
- **Phase 6 (Integration Testing)**: 35 tasks
- **Phase 7 (Polish)**: 17 tasks

**Total**: 98 tasks

**Parallel Opportunities**: 23 tasks marked [P] can run in parallel

**MVP Scope**: 26 tasks (Phase 1 + Phase 2 + Phase 3)
