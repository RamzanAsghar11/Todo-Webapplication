# Tasks: Todo Application (Core CRUD)

**Input**: Design documents from `/specs/001-todo-app-spec/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/tasks-api.yaml

**Tests**: Tests are NOT included in this phase as they were not explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`
- All paths are relative to repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create backend/ and frontend/ directories at repository root
- [ ] T002 Create backend/src/ directory structure (models/, schemas/, routers/)
- [ ] T003 Create frontend/src/ directory structure (app/, components/, lib/, types/)
- [ ] T004 [P] Initialize Python virtual environment in backend/ directory
- [ ] T005 [P] Create backend/requirements.txt with FastAPI, SQLModel, uvicorn, psycopg2-binary, python-dotenv
- [ ] T006 [P] Install Python dependencies in backend/ virtual environment
- [ ] T007 [P] Initialize Next.js project in frontend/ with TypeScript and Tailwind CSS
- [ ] T008 [P] Create backend/.env.example with DATABASE_URL placeholder
- [ ] T009 [P] Create frontend/.env.local.example with NEXT_PUBLIC_API_URL placeholder
- [ ] T010 [P] Create .gitignore at repository root (exclude venv/, node_modules/, .env, .env.local)
- [ ] T011 [P] Create backend/README.md with setup instructions
- [ ] T012 [P] Create frontend/README.md with setup instructions

**Checkpoint**: Project structure initialized, dependencies ready to install

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T013 Ask user for Neon PostgreSQL DATABASE_URL and save to backend/.env
- [ ] T014 Create backend/src/config.py to load DATABASE_URL from environment
- [ ] T015 Create backend/src/database.py with SQLModel engine, session factory, and get_session dependency
- [ ] T016 Create backend/src/models/task.py with Task SQLModel class (id, user_id, title, description, completed, created_at, updated_at)
- [ ] T017 Create backend/src/schemas/task.py with TaskCreate, TaskUpdate, TaskComplete Pydantic schemas
- [ ] T018 Create backend/src/main.py with FastAPI app initialization and CORS middleware
- [ ] T019 Add database table creation logic to backend/src/main.py startup event
- [ ] T020 Create frontend/src/types/task.ts with Task TypeScript interface
- [ ] T021 Create frontend/src/lib/api.ts with base API client configuration
- [ ] T022 Start backend server and verify database connection and table creation
- [ ] T023 Verify backend server runs on http://localhost:8000 and /docs endpoint is accessible

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - View and Create Tasks (Priority: P1) 🎯 MVP

**Goal**: Users can view their task list and create new tasks

**Independent Test**: Navigate to http://localhost:3000/test-user/tasks, create a task, verify it appears in the list

### Backend Implementation for User Story 1

- [ ] T024 [P] [US1] Create backend/src/routers/tasks.py with APIRouter initialization
- [ ] T025 [US1] Implement GET /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py
- [ ] T026 [US1] Implement POST /api/{user_id}/tasks endpoint in backend/src/routers/tasks.py
- [ ] T027 [US1] Add tasks router to backend/src/main.py with proper prefix
- [ ] T028 [US1] Test GET /api/{user_id}/tasks endpoint via Swagger UI (should return empty array)
- [ ] T029 [US1] Test POST /api/{user_id}/tasks endpoint via Swagger UI (create a task, verify response)
- [ ] T030 [US1] Test GET /api/{user_id}/tasks endpoint again (should return created task)

### Frontend Implementation for User Story 1

- [ ] T031 [P] [US1] Implement getTasks function in frontend/src/lib/api.ts
- [ ] T032 [P] [US1] Implement createTask function in frontend/src/lib/api.ts
- [ ] T033 [P] [US1] Create frontend/src/app/layout.tsx with basic HTML structure and Tailwind CSS
- [ ] T034 [P] [US1] Create frontend/src/app/page.tsx with redirect to /test-user/tasks
- [ ] T035 [US1] Create frontend/src/app/[userId]/tasks/page.tsx for task list view
- [ ] T036 [US1] Create frontend/src/components/TaskList.tsx component (displays tasks, handles empty state)
- [ ] T037 [US1] Create frontend/src/app/[userId]/tasks/new/page.tsx for create task form
- [ ] T038 [US1] Create frontend/src/components/TaskForm.tsx component (title and description inputs, validation)
- [ ] T039 [US1] Add responsive styling to TaskList component (mobile 320px+, desktop 1024px+)
- [ ] T040 [US1] Add responsive styling to TaskForm component (mobile 320px+, desktop 1024px+)
- [ ] T041 [US1] Add loading states to task list page
- [ ] T042 [US1] Add error handling to task list page (display error messages)
- [ ] T043 [US1] Add form validation to TaskForm (title required, max lengths)

### Integration Verification for User Story 1

- [ ] T044 [US1] Start both backend and frontend servers
- [ ] T045 [US1] Navigate to http://localhost:3000/test-user/tasks and verify empty state displays
- [ ] T046 [US1] Click "Create Task" button and verify form appears
- [ ] T047 [US1] Submit form without title and verify validation error displays
- [ ] T048 [US1] Create a task with title "Test Task 1" and description "Test description"
- [ ] T049 [US1] Verify task appears in list with correct title, description, and incomplete status
- [ ] T050 [US1] Refresh page and verify task persists
- [ ] T051 [US1] Create 2 more tasks and verify all 3 appear in list
- [ ] T052 [US1] Test on mobile viewport (320px width) and verify responsive layout

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently - MVP is complete!

---

## Phase 4: User Story 2 - Update and Delete Tasks (Priority: P2)

**Goal**: Users can edit existing tasks and permanently delete tasks

**Independent Test**: Create a task (using US1), edit its title/description, verify changes persist, delete the task, verify it's removed

### Backend Implementation for User Story 2

- [ ] T053 [P] [US2] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/routers/tasks.py
- [ ] T054 [P] [US2] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/routers/tasks.py
- [ ] T055 [P] [US2] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/routers/tasks.py
- [ ] T056 [US2] Add 404 error handling for task not found in all three endpoints
- [ ] T057 [US2] Test GET /api/{user_id}/tasks/{id} via Swagger UI (get existing task)
- [ ] T058 [US2] Test PUT /api/{user_id}/tasks/{id} via Swagger UI (update task, verify response)
- [ ] T059 [US2] Test DELETE /api/{user_id}/tasks/{id} via Swagger UI (delete task, verify 204 response)
- [ ] T060 [US2] Test GET /api/{user_id}/tasks/{id} with deleted task ID (verify 404 response)

### Frontend Implementation for User Story 2

- [ ] T061 [P] [US2] Implement getTask function in frontend/src/lib/api.ts
- [ ] T062 [P] [US2] Implement updateTask function in frontend/src/lib/api.ts
- [ ] T063 [P] [US2] Implement deleteTask function in frontend/src/lib/api.ts
- [ ] T064 [US2] Create frontend/src/app/[userId]/tasks/[taskId]/edit/page.tsx for edit task form
- [ ] T065 [US2] Update TaskForm component to support edit mode (pre-fill values, different submit handler)
- [ ] T066 [US2] Add "Edit" button to TaskList component (links to edit page)
- [ ] T067 [US2] Add "Delete" button to TaskList component (with confirmation dialog)
- [ ] T068 [US2] Implement delete confirmation dialog in TaskList component
- [ ] T069 [US2] Add loading state during delete operation
- [ ] T070 [US2] Add error handling for update and delete operations
- [ ] T071 [US2] Update task list after successful delete (remove from UI)
- [ ] T072 [US2] Add cancel button to edit form (navigates back to list)

### Integration Verification for User Story 2

- [ ] T073 [US2] Start both servers and navigate to task list
- [ ] T074 [US2] Create a test task using US1 functionality
- [ ] T075 [US2] Click "Edit" on the task and verify form pre-fills with current values
- [ ] T076 [US2] Update title to "Updated Task" and save
- [ ] T077 [US2] Verify updated title appears in task list
- [ ] T078 [US2] Verify updated_at timestamp changed
- [ ] T079 [US2] Try to save task with empty title and verify validation error
- [ ] T080 [US2] Click "Delete" on a task and verify confirmation dialog appears
- [ ] T081 [US2] Cancel deletion and verify task remains
- [ ] T082 [US2] Click "Delete" again and confirm deletion
- [ ] T083 [US2] Verify task is removed from list
- [ ] T084 [US2] Refresh page and verify deleted task does not reappear

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Mark Tasks Complete/Incomplete (Priority: P3)

**Goal**: Users can toggle task completion status to track progress

**Independent Test**: Create a task (US1), mark as complete, verify visual indicator, unmark as incomplete, verify status toggles

### Backend Implementation for User Story 3

- [ ] T085 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/routers/tasks.py
- [ ] T086 [US3] Add 404 error handling for task not found in complete endpoint
- [ ] T087 [US3] Test PATCH /api/{user_id}/tasks/{id}/complete via Swagger UI (toggle to true, verify response)
- [ ] T088 [US3] Test PATCH again to toggle back to false (verify bidirectional toggle)

### Frontend Implementation for User Story 3

- [ ] T089 [US3] Implement toggleTaskComplete function in frontend/src/lib/api.ts
- [ ] T090 [US3] Create frontend/src/components/TaskItem.tsx component for individual task display
- [ ] T091 [US3] Add checkbox/button to TaskItem for toggling completion
- [ ] T092 [US3] Add visual styling for completed tasks (strikethrough, different color, checkmark icon)
- [ ] T093 [US3] Update TaskList to use TaskItem component for each task
- [ ] T094 [US3] Implement toggle handler in TaskItem (calls API, updates UI optimistically)
- [ ] T095 [US3] Add loading state during toggle operation
- [ ] T096 [US3] Add error handling for toggle operation (revert UI on failure)
- [ ] T097 [US3] Ensure completed and incomplete tasks are visually distinguishable

### Integration Verification for User Story 3

- [ ] T098 [US3] Start both servers and navigate to task list
- [ ] T099 [US3] Create 2 test tasks using US1 functionality
- [ ] T100 [US3] Click checkbox/button to mark first task as complete
- [ ] T101 [US3] Verify task displays with completed styling (strikethrough, checkmark)
- [ ] T102 [US3] Click again to mark as incomplete
- [ ] T103 [US3] Verify task returns to normal styling
- [ ] T104 [US3] Mark both tasks as complete and verify both show completed styling
- [ ] T105 [US3] Refresh page and verify completion status persists
- [ ] T106 [US3] Verify updated_at timestamp changes when toggling completion

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Final improvements, cleanup, and production readiness

- [ ] T107 [P] Add proper page titles to all frontend pages (using Next.js metadata)
- [ ] T108 [P] Add navigation between pages (back to list from create/edit)
- [ ] T109 [P] Improve empty state message with helpful instructions
- [ ] T110 [P] Add success messages after create/update/delete operations
- [ ] T111 [P] Verify all error messages are user-friendly (no technical jargon)
- [ ] T112 [P] Test responsive layout on tablet viewport (768px width)
- [ ] T113 [P] Add loading spinner component for better UX
- [ ] T114 [P] Verify all forms have proper accessibility (labels, ARIA attributes)
- [ ] T115 Remove any console.log statements from frontend code
- [ ] T116 Remove any debug print statements from backend code
- [ ] T117 Verify backend/.env is in .gitignore and not committed
- [ ] T118 Verify frontend/.env.local is in .gitignore and not committed
- [ ] T119 Update repository root README.md with project overview and setup instructions
- [ ] T120 Verify quickstart.md instructions are accurate and complete
- [ ] T121 Test complete user flow from start to finish (create, view, edit, toggle, delete)
- [ ] T122 Verify no authentication logic exists in codebase (grep for "auth", "jwt", "token")
- [ ] T123 Run final constitution compliance check (verify all 6 principles)

**Checkpoint**: Application is production-ready and fully documented

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User Story 1 (P1): Can start after Foundational - No dependencies on other stories
  - User Story 2 (P2): Can start after Foundational - No dependencies on other stories (independent)
  - User Story 3 (P3): Can start after Foundational - No dependencies on other stories (independent)
- **Polish (Phase 6)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independently testable (uses US1 for test setup but doesn't depend on US1 code)
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Independently testable (uses US1 for test setup but doesn't depend on US1 code)

### Within Each User Story

- Backend tasks before frontend tasks (API must exist before UI can call it)
- Backend: Schemas → Router endpoints → Testing
- Frontend: API client functions → Pages/Components → Styling → Error handling
- Integration verification after all implementation tasks

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel (T004-T012)
- Backend and frontend foundational tasks can run in parallel after database setup (T020-T021 parallel with T016-T019)
- Within each user story:
  - Backend schema and router creation can be parallel (T024 parallel with others)
  - Frontend API functions, components, and pages can be parallel (T031-T034, T036-T038)
- Polish tasks marked [P] can run in parallel (T107-T114)

---

## Parallel Example: User Story 1

```bash
# After Foundational phase completes, launch User Story 1 backend tasks in parallel:
Task T024: Create router file
Task T025: Implement GET endpoint
Task T026: Implement POST endpoint

# Then launch User Story 1 frontend tasks in parallel:
Task T031: Implement getTasks API function
Task T032: Implement createTask API function
Task T033: Create layout
Task T034: Create home page
Task T036: Create TaskList component
Task T038: Create TaskForm component
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

**This gives you a working todo app with view and create functionality!**

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add Polish → Final production release

Each story adds value without breaking previous stories.

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (T024-T052)
   - Developer B: User Story 2 (T053-T084)
   - Developer C: User Story 3 (T085-T106)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies, can run in parallel
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Stop at any checkpoint to validate story independently
- Commit after each task or logical group
- Tests are NOT included as they were not requested in the specification
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

---

## Task Summary

**Total Tasks**: 123
**Setup Phase**: 12 tasks
**Foundational Phase**: 11 tasks
**User Story 1 (P1 - MVP)**: 29 tasks
**User Story 2 (P2)**: 32 tasks
**User Story 3 (P3)**: 22 tasks
**Polish Phase**: 17 tasks

**Parallel Opportunities**: 28 tasks marked [P] can run in parallel
**MVP Scope**: Phases 1-3 (52 tasks) delivers working todo app with view and create
**Independent Stories**: All 3 user stories can be developed in parallel after Foundational phase
