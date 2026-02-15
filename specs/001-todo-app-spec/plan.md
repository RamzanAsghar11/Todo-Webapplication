# Implementation Plan: Todo Application (Core CRUD)

**Branch**: `001-todo-app-spec` | **Date**: 2026-02-12 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-app-spec/spec.md`

**Note**: This plan defines the strict execution contract for implementing the Todo application core CRUD functionality WITHOUT authentication. Authentication will be added in a future phase.

## Summary

Build a production-ready Todo Full-Stack Web Application with complete CRUD operations for tasks. The application consists of a Next.js 16+ TypeScript frontend with App Router and a Python FastAPI backend using SQLModel ORM connected to Neon Serverless PostgreSQL. This phase focuses exclusively on task management functionality; authentication is explicitly deferred to a future specification.

**Core Capabilities:**
- Create, read, update, delete tasks
- Toggle task completion status
- User-scoped task operations (via user_id in URL path)
- Responsive UI (mobile and desktop)
- Persistent storage in PostgreSQL

**Key Constraint:** No authentication or authorization logic in this phase. User identification is handled via URL path parameters only.

## Technical Context

**Language/Version**: Python 3.11 (backend), TypeScript 5.0+ (frontend), Node.js 18+
**Primary Dependencies**: FastAPI 0.104+, SQLModel 0.0.8+, Next.js 16+, React 18+
**Storage**: Neon Serverless PostgreSQL (cloud-hosted, serverless)
**Testing**: pytest (backend), Jest/React Testing Library (frontend - optional in this phase)
**Target Platform**: Web application (Linux/macOS/Windows servers for backend, modern browsers for frontend)
**Project Type**: Web application (frontend + backend)
**Performance Goals**: <2s task creation, <3s list load (100 tasks), 50+ concurrent users
**Constraints**: <200ms API response time (p95), responsive 320px-1024px+, no offline mode
**Scale/Scope**: Individual users with up to 1000 tasks, single-region deployment

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

Verify compliance with `.specify/memory/constitution.md`:

- [x] **Technology Stack Mandate**: Using Next.js 16+/TypeScript (frontend), FastAPI/Python (backend), SQLModel (ORM), Neon PostgreSQL (database)
- [x] **API Design & User Scoping**: All API endpoints follow `/api/{user_id}/tasks` pattern with user-scoped routes
- [⚠️] **Security-First Authentication**: Backend JWT verification DEFERRED to future phase (see Complexity Tracking)
- [x] **Database Access via SQLModel Only**: All database operations use SQLModel ORM (no raw SQL)
- [x] **Spec-Driven Development**: Following spec → plan → tasks → implement workflow
- [x] **Separation of Concerns**: Clear frontend/backend separation, stateless backend, no business logic in frontend

**Violations Requiring Justification**: See Complexity Tracking section below

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-app-spec/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (in progress)
├── research.md          # Phase 0 output (to be created)
├── data-model.md        # Phase 1 output (to be created)
├── quickstart.md        # Phase 1 output (to be created)
├── contracts/           # Phase 1 output (to be created)
│   └── tasks-api.yaml   # OpenAPI specification for task endpoints
├── checklists/          # Quality validation
│   └── requirements.md  # Spec quality checklist (completed)
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── database.py          # Database connection and session management
│   ├── models/
│   │   └── task.py          # SQLModel Task model
│   ├── schemas/
│   │   └── task.py          # Pydantic request/response schemas
│   ├── routers/
│   │   └── tasks.py         # Task CRUD endpoints
│   └── config.py            # Environment configuration
├── .env.example             # Example environment variables
├── requirements.txt         # Python dependencies
└── README.md                # Backend setup instructions

frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx       # Root layout
│   │   ├── page.tsx         # Home/redirect page
│   │   └── [userId]/
│   │       └── tasks/
│   │           ├── page.tsx           # Task list page
│   │           ├── new/
│   │           │   └── page.tsx       # Create task page
│   │           └── [taskId]/
│   │               └── edit/
│   │                   └── page.tsx   # Edit task page
│   ├── components/
│   │   ├── TaskList.tsx     # Task list component
│   │   ├── TaskForm.tsx     # Create/edit task form
│   │   └── TaskItem.tsx     # Individual task display
│   ├── lib/
│   │   └── api.ts           # API client functions
│   └── types/
│       └── task.ts          # TypeScript type definitions
├── .env.local.example       # Example environment variables
├── package.json             # Node dependencies
├── tsconfig.json            # TypeScript configuration
├── next.config.js           # Next.js configuration
└── README.md                # Frontend setup instructions

.gitignore                   # Git ignore patterns
README.md                    # Project overview and setup
```

**Structure Decision**: Web application structure (Option 2) selected due to clear frontend/backend separation required by constitution. Backend uses FastAPI standard structure with routers, models, and schemas. Frontend uses Next.js 16+ App Router with file-based routing and React Server Components.

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| Security-First Authentication (JWT verification deferred) | Phased implementation approach: Core CRUD functionality must be built and tested before adding authentication layer. Spec explicitly excludes authentication to reduce complexity and enable focused testing of task management logic. | Implementing authentication simultaneously would violate single-responsibility principle, increase initial complexity, and make debugging harder. Constitution principle III will be satisfied in next phase (002-todo-app-auth). |

## Phase 0: Pre-Implementation Research

**Purpose**: Resolve all technical unknowns and establish implementation patterns before coding begins.

**Prerequisites**: Constitution and spec reviewed and understood.

### Research Tasks

1. **FastAPI + SQLModel Integration Patterns**
   - Research: Best practices for SQLModel with FastAPI
   - Research: Database session management patterns (dependency injection)
   - Research: Async vs sync database operations with SQLModel
   - Output: Recommended patterns for database.py and model definitions

2. **Next.js 16+ App Router Patterns**
   - Research: Server Components vs Client Components usage
   - Research: Data fetching patterns (Server Actions vs API routes vs client fetch)
   - Research: Form handling in App Router
   - Output: Recommended patterns for task CRUD operations

3. **Neon PostgreSQL Connection**
   - Research: Connection string format for Neon
   - Research: Connection pooling requirements
   - Research: SSL/TLS requirements
   - Output: Database configuration approach

4. **Error Handling Strategy**
   - Research: FastAPI exception handlers
   - Research: Next.js error boundaries and error.tsx
   - Research: User-friendly error message patterns
   - Output: Error handling implementation guide

5. **Responsive UI Framework Decision**
   - Research: Tailwind CSS vs CSS Modules vs styled-components
   - Research: Mobile-first responsive patterns
   - Output: Styling approach selection and justification

**Deliverable**: `research.md` documenting all findings, decisions, and rationale

## Phase 1: Design & Contracts

**Prerequisites**: Phase 0 research complete, all NEEDS CLARIFICATION resolved

### Task 1.1: Data Model Design

Create `data-model.md` with:

**Task Entity:**
```
Task
├── id: UUID (primary key, auto-generated)
├── user_id: String (indexed, required)
├── title: String (max 500 chars, required, non-empty)
├── description: String (max 2000 chars, optional, nullable)
├── completed: Boolean (default false, required)
├── created_at: DateTime (auto-set on creation, immutable)
└── updated_at: DateTime (auto-update on modification)
```

**Validation Rules:**
- title: Required, 1-500 characters, trimmed
- description: Optional, 0-2000 characters if provided
- user_id: Required, non-empty string
- completed: Boolean, defaults to false
- Timestamps: Automatically managed by database/ORM

**Indexes:**
- Primary: id (UUID)
- Secondary: (user_id, created_at) for efficient user task queries

**State Transitions:**
- completed: false ↔ true (bidirectional toggle)

### Task 1.2: API Contracts

Create `contracts/tasks-api.yaml` (OpenAPI 3.0 specification):

**Endpoints:**

1. **GET /api/{user_id}/tasks**
   - Description: Retrieve all tasks for a user
   - Path params: user_id (string)
   - Response 200: Array of Task objects
   - Response 500: Server error

2. **POST /api/{user_id}/tasks**
   - Description: Create a new task
   - Path params: user_id (string)
   - Request body: { title: string, description?: string }
   - Response 201: Created Task object
   - Response 400: Validation error
   - Response 500: Server error

3. **GET /api/{user_id}/tasks/{id}**
   - Description: Retrieve a single task
   - Path params: user_id (string), id (UUID)
   - Response 200: Task object
   - Response 404: Task not found
   - Response 500: Server error

4. **PUT /api/{user_id}/tasks/{id}**
   - Description: Update a task
   - Path params: user_id (string), id (UUID)
   - Request body: { title: string, description?: string }
   - Response 200: Updated Task object
   - Response 400: Validation error
   - Response 404: Task not found
   - Response 500: Server error

5. **DELETE /api/{user_id}/tasks/{id}**
   - Description: Delete a task
   - Path params: user_id (string), id (UUID)
   - Response 204: No content (success)
   - Response 404: Task not found
   - Response 500: Server error

6. **PATCH /api/{user_id}/tasks/{id}/complete**
   - Description: Toggle task completion status
   - Path params: user_id (string), id (UUID)
   - Request body: { completed: boolean }
   - Response 200: Updated Task object
   - Response 400: Validation error
   - Response 404: Task not found
   - Response 500: Server error

**Common Response Schemas:**
- Task: { id, user_id, title, description, completed, created_at, updated_at }
- Error: { detail: string, field?: string }

### Task 1.3: Quickstart Guide

Create `quickstart.md` with:

**Prerequisites:**
- Python 3.11+
- Node.js 18+
- Neon PostgreSQL database (user must provide DATABASE_URL)

**Backend Setup:**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
cp .env.example .env
# Edit .env and add DATABASE_URL
python src/main.py
# Server runs on http://localhost:8000
```

**Frontend Setup:**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL=http://localhost:8000
npm run dev
# App runs on http://localhost:3000
```

**Testing the Application:**
1. Navigate to http://localhost:3000/test-user/tasks
2. Create a task
3. View task list
4. Edit a task
5. Toggle completion
6. Delete a task

### Task 1.4: Update Agent Context

Run: `.specify/scripts/bash/update-agent-context.sh claude`

This updates `.claude/memory/active-technologies.md` with:
- Python 3.11 (backend)
- TypeScript 5.0+ (frontend)
- Node.js 18+ + Next.js 16+ (App Router)
- FastAPI 0.104+
- SQLModel 0.0.8+
- Neon Serverless PostgreSQL

**Deliverables**:
- `data-model.md`
- `contracts/tasks-api.yaml`
- `quickstart.md`
- Updated agent context file

## Phase 2: Constitution Re-Check

**Purpose**: Verify design compliance before implementation begins

Re-evaluate Constitution Check with completed design:

- [x] Technology Stack Mandate: Confirmed in Technical Context
- [x] API Design & User Scoping: Confirmed in contracts/tasks-api.yaml
- [⚠️] Security-First Authentication: Justified deferral documented
- [x] Database Access via SQLModel Only: Confirmed in data-model.md
- [x] Spec-Driven Development: Following workflow (spec → plan → tasks next)
- [x] Separation of Concerns: Confirmed in Project Structure

**Gate**: If any unjustified violations exist, STOP and resolve before proceeding to /sp.tasks

## Implementation Phases (Executed via /sp.tasks and /sp.implement)

The following phases will be executed after running `/sp.tasks` to generate the detailed task breakdown:

### Phase 3: Project Structure Setup

**Purpose**: Initialize project scaffolding and tooling

**Tasks** (detailed in tasks.md):
- Create backend/ and frontend/ directories
- Initialize Python virtual environment
- Initialize Next.js project with TypeScript
- Configure linting and formatting
- Create .env.example files
- Set up .gitignore

**Verification**: Both projects initialize without errors

### Phase 4: Database & ORM Layer

**Purpose**: Establish database connection and define data models

**Prerequisites**: User provides DATABASE_URL

**Tasks** (detailed in tasks.md):
- Implement database.py with SQLModel engine and session
- Define Task model in models/task.py
- Create database tables
- Test database connectivity
- Verify CRUD operations at ORM level

**Verification**: Database connection succeeds, tables created, basic queries work

### Phase 5: Backend API Implementation

**Purpose**: Implement RESTful API endpoints

**Tasks** (detailed in tasks.md):
- Implement GET /api/{user_id}/tasks
- Implement POST /api/{user_id}/tasks
- Implement GET /api/{user_id}/tasks/{id}
- Implement PUT /api/{user_id}/tasks/{id}
- Implement DELETE /api/{user_id}/tasks/{id}
- Implement PATCH /api/{user_id}/tasks/{id}/complete
- Add request validation (Pydantic schemas)
- Add error handling and logging
- Enable CORS for frontend

**Verification**: All endpoints tested manually (curl/Postman), return correct status codes and data

### Phase 6: Frontend Implementation

**Purpose**: Build responsive UI and connect to backend

**Tasks** (detailed in tasks.md):
- Implement task list page (app/[userId]/tasks/page.tsx)
- Implement create task page (app/[userId]/tasks/new/page.tsx)
- Implement edit task page (app/[userId]/tasks/[taskId]/edit/page.tsx)
- Create TaskList component
- Create TaskForm component
- Create TaskItem component
- Implement API client (lib/api.ts)
- Add loading states
- Add error handling
- Implement responsive styling

**Verification**: UI renders correctly on mobile and desktop, all CRUD operations work end-to-end

### Phase 7: Integration & Verification

**Purpose**: End-to-end testing and bug fixes

**Tasks** (detailed in tasks.md):
- Start backend server
- Start frontend dev server
- Test complete user flow:
  - Navigate to /test-user/tasks
  - Create multiple tasks
  - View task list
  - Edit tasks
  - Toggle completion
  - Delete tasks
  - Verify persistence (refresh page)
- Fix any runtime errors
- Fix any integration issues
- Verify responsive behavior on different screen sizes

**Verification**: All acceptance scenarios from spec pass without errors

### Phase 8: Production Readiness

**Purpose**: Final cleanup and documentation

**Tasks** (detailed in tasks.md):
- Verify all secrets use environment variables
- Remove debug code and console.logs
- Update README.md with setup instructions
- Verify quickstart.md accuracy
- Confirm no authentication logic exists
- Run final constitution compliance check

**Verification**: Application is ready for deployment, documentation is complete

## Error Handling Protocol

**If any error occurs during implementation:**

1. **STOP** immediately - do not proceed to next task
2. **Diagnose** root cause:
   - Read error message carefully
   - Check logs (backend and frontend)
   - Verify configuration (environment variables, dependencies)
   - Review recent changes
3. **Fix** the issue:
   - Apply targeted fix
   - Do not introduce workarounds or hacks
   - Update documentation if configuration changed
4. **Re-run** the failing step to verify fix
5. **Proceed** only after verification succeeds

**Common Error Categories:**
- **Dependency errors**: Check requirements.txt / package.json versions
- **Database errors**: Verify DATABASE_URL, check Neon dashboard
- **CORS errors**: Verify FastAPI CORS middleware configuration
- **Type errors**: Check TypeScript types, Pydantic schemas
- **Runtime errors**: Check logs, verify data flow

## Communication Protocol

**When to ask the user:**
- DATABASE_URL is required (Phase 4 start)
- Any environment variable value is needed
- Clarification on ambiguous requirement (should be rare - spec is complete)

**When NOT to ask the user:**
- Technical implementation decisions (covered in research phase)
- Styling choices (use reasonable defaults)
- Debugging steps (handle autonomously)

**Status reporting:**
- Clearly state when each phase completes
- Report what was verified and results
- Flag any deviations from plan (with justification)

## Out of Scope (Strict Enforcement)

The following MUST NOT be implemented in this phase:

- ❌ User authentication (login/signup)
- ❌ Better Auth integration
- ❌ JWT token generation or verification
- ❌ Password hashing or management
- ❌ Session management
- ❌ Authorization checks beyond user_id scoping
- ❌ User profile or account management
- ❌ Role-based access control

**Rationale**: These features are explicitly deferred to specification 002-todo-app-auth to maintain focus and reduce complexity.

## Next Steps

After this plan is complete:

1. **Run `/sp.tasks`** to generate detailed task breakdown (tasks.md)
2. **Run `/sp.implement`** to execute implementation following tasks.md
3. **Verify** all acceptance criteria from spec.md are met
4. **Document** any architectural decisions in ADRs if significant choices were made
5. **Prepare** for next phase: 002-todo-app-auth specification

## Success Criteria

This plan is successful when:

- ✅ All Phase 0-1 artifacts created (research.md, data-model.md, contracts/, quickstart.md)
- ✅ Constitution check passes (with justified authentication deferral)
- ✅ Project structure defined and documented
- ✅ Ready for /sp.tasks command to generate implementation tasks
- ✅ No unresolved technical unknowns remain
