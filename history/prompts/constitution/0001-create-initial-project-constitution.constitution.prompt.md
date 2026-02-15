---
id: 0001
title: Create initial project constitution
stage: constitution
date: 2026-02-12
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: user
command: /sp.constitution
labels: ["constitution", "governance", "architecture", "tech-stack", "security"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - none
---

## Prompt

```text
your task is to create a constituion.md file
This file is the single source of truth for architectural rules, technology choices, and non-negotiable constraints of the project. All future specs and implementations MUST follow this constitution.

Project Context
---------------
We are building a Todo Full-Stack Web Application.

Core Requirements
-----------------
- Implement all 5 Basic Level Todo features as a web application
- Use a Spec-Driven development approach
- Create RESTful API endpoints
- Build a responsive frontend UI
- Persist all data in Neon Serverless PostgreSQL
- Authentication must be implemented using Better Auth
- Backend must verify authenticated users securely

Technology Stack (MANDATORY)
----------------------------
Frontend:
- Next.js 16+
- App Router
- TypeScript

Backend:
- Python FastAPI

ORM Layer:
- SQLModel ONLY (no SQLAlchemy Core, no raw SQL unless absolutely necessary)

Database:
- Neon Serverless PostgreSQL

Authentication:
- Better Auth (runs on Next.js frontend)
- JWT-based authentication between frontend and FastAPI backend

API Design Rules
----------------
- RESTful APIs only
- All task routes must be user-scoped
- API endpoints must follow this structure:

GET     /api/{user_id}/tasks
POST    /api/{user_id}/tasks
GET     /api/{user_id}/tasks/{id}
PUT     /api/{user_id}/tasks/{id}
DELETE  /api/{user_id}/tasks/{id}
PATCH   /api/{user_id}/tasks/{id}/complete

Security Rules
--------------
- Backend MUST NOT trust user_id from the URL alone
- FastAPI must verify JWT tokens issued by Better Auth
- user_id must be derived from the validated JWT
- Unauthorized or mismatched users must be rejected

Architecture Principles
-----------------------
- Clear separation of frontend and backend
- Backend is stateless
- No business logic in frontend
- Database access only through SQLModel
- Environment variables for secrets (JWT secret, DB URL, etc.)
- Clean, readable, and maintainable code over shortcuts

Spec-Driven Rules
-----------------
- Specs come before implementation
- No feature should be implemented without a spec
- Specs must align with this constitution
- If a spec conflicts with the constitution, the constitution wins

What to Output
--------------
- Create a well-structured, professional `constitution.md`
- Use clear headings and bullet points
- Write it as a binding contract for the project
- Do NOT generate code
- Do NOT ask questions
- Only output the content of `constitution.md`

Begin now.
```

## Response snapshot

Created comprehensive constitution.md (v1.0.0) with six core principles:

1. **Technology Stack Mandate** - Enforces Next.js 16+/TypeScript frontend, FastAPI/Python backend, SQLModel ORM, Neon PostgreSQL
2. **API Design & User Scoping** - Mandates RESTful user-scoped endpoints with explicit structure
3. **Security-First Authentication** - Zero-trust JWT verification, no URL parameter trust
4. **Database Access via SQLModel Only** - Prohibits raw SQL except when justified
5. **Spec-Driven Development** - Non-negotiable workflow: spec → plan → tasks → implement
6. **Separation of Concerns** - Stateless backend, no business logic in frontend

Added sections for Technology Stack Details, Development Workflow (feature process, code quality, testing, security), and Governance (amendment process, compliance, conflict resolution).

Included Sync Impact Report noting templates requiring validation.

## Outcome

- ✅ Impact: Established binding architectural contract for entire project; all future work must comply
- 🧪 Tests: N/A (governance document)
- 📁 Files: Created .specify/memory/constitution.md (195 lines)
- 🔁 Next prompts: Validate dependent templates (plan-template.md, spec-template.md, tasks-template.md); create first feature spec
- 🧠 Reflection: Constitution successfully captures all mandatory requirements with clear rationale. Security principles (JWT verification, user_id validation) are explicit and testable. Spec-driven workflow is enforced as non-negotiable.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): N/A (initial constitution)
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
