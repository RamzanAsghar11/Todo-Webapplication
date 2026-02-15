<!--
Sync Impact Report:
Version: Initial → 1.0.0
Modified Principles: N/A (initial creation)
Added Sections: All sections created from template
Removed Sections: None
Templates Requiring Updates:
  ✅ constitution.md created
  ✅ plan-template.md - updated with specific constitution checks
  ✅ spec-template.md - verified, no updates needed (technology-agnostic by design)
  ✅ tasks-template.md - verified, no updates needed (flexible structure supports constitution)
Follow-up TODOs: None - all templates validated and aligned
-->

# Todo Full-Stack Web Application Constitution

## Core Principles

### I. Technology Stack Mandate

The following technology choices are MANDATORY and non-negotiable for all implementation work:

**Frontend:**
- Next.js 16+ with App Router architecture
- TypeScript for all frontend code
- Better Auth for authentication (runs on Next.js)

**Backend:**
- Python FastAPI for all API endpoints
- JWT verification for authenticated requests

**Data Layer:**
- SQLModel ONLY for database operations
- No SQLAlchemy Core or raw SQL unless absolutely necessary and explicitly justified
- Neon Serverless PostgreSQL as the database

**Rationale:** This stack ensures type safety (TypeScript), modern React patterns (App Router), high-performance async Python (FastAPI), and seamless ORM integration (SQLModel). Deviations require architectural review and amendment to this constitution.

### II. API Design & User Scoping

All API endpoints MUST follow RESTful conventions and be user-scoped:

**Required Endpoint Structure:**
```
GET     /api/{user_id}/tasks
POST    /api/{user_id}/tasks
GET     /api/{user_id}/tasks/{id}
PUT     /api/{user_id}/tasks/{id}
DELETE  /api/{user_id}/tasks/{id}
PATCH   /api/{user_id}/tasks/{id}/complete
```

**Rules:**
- Every task operation MUST be scoped to a user_id
- Endpoints MUST return only data belonging to the authenticated user
- Cross-user data access is strictly prohibited
- API responses MUST use standard HTTP status codes

**Rationale:** User-scoped routes prevent data leakage, simplify authorization logic, and make security boundaries explicit in the URL structure.

### III. Security-First Authentication

Authentication and authorization MUST be implemented with zero-trust principles:

**Non-Negotiable Rules:**
- Backend MUST NOT trust user_id from URL parameters alone
- FastAPI MUST verify JWT tokens issued by Better Auth on every protected request
- The authenticated user_id MUST be derived from the validated JWT payload
- Requests where JWT user_id does not match URL user_id MUST be rejected with 403 Forbidden
- Unauthorized requests MUST be rejected with 401 Unauthorized
- Secrets (JWT signing keys, database credentials) MUST be stored in environment variables, never hardcoded

**Rationale:** URL parameters are user-controlled and trivially spoofed. JWT verification ensures cryptographic proof of identity. Mismatched user_id indicates attempted unauthorized access.

### IV. Database Access via SQLModel Only

All database interactions MUST use SQLModel ORM:

**Rules:**
- Define all tables as SQLModel classes with proper type hints
- Use SQLModel query methods for CRUD operations
- Raw SQL is prohibited except for complex queries that cannot be expressed in SQLModel (requires justification in code comments)
- Database migrations MUST be version-controlled
- No direct SQLAlchemy Core usage unless SQLModel cannot support the use case

**Rationale:** SQLModel provides type safety, reduces boilerplate, prevents SQL injection, and integrates seamlessly with FastAPI's Pydantic validation.

### V. Spec-Driven Development (NON-NEGOTIABLE)

All features MUST follow the Spec-Driven Development workflow:

**Mandatory Workflow:**
1. Write specification (`specs/<feature>/spec.md`) defining requirements
2. Generate architectural plan (`specs/<feature>/plan.md`) with design decisions
3. Break down into testable tasks (`specs/<feature>/tasks.md`)
4. Implement via Claude Code following the plan
5. Validate against acceptance criteria in spec

**Rules:**
- No feature implementation without a spec
- Specs MUST align with this constitution
- If a spec conflicts with the constitution, the constitution wins
- All specs MUST include acceptance criteria and test scenarios

**Rationale:** Spec-first development ensures shared understanding, reduces rework, enables review before implementation, and creates documentation as a byproduct.

### VI. Separation of Concerns

Clear architectural boundaries MUST be maintained:

**Rules:**
- Backend is stateless (no session storage on server)
- No business logic in frontend components (validation, calculations, authorization)
- Frontend handles presentation, user interaction, and API calls only
- Backend handles validation, business rules, and data persistence
- Database access ONLY through backend API (frontend never connects directly)
- Environment-specific configuration via environment variables

**Rationale:** Separation of concerns improves testability, security (business logic cannot be bypassed), maintainability, and enables independent scaling of frontend and backend.

## Technology Stack Details

### Frontend Stack
- **Framework:** Next.js 16+ (App Router)
- **Language:** TypeScript 5.0+
- **Runtime:** Node.js 18+
- **Authentication:** Better Auth 0.2.0+
- **Styling:** (To be determined based on feature requirements)

### Backend Stack
- **Framework:** FastAPI 0.104+
- **Language:** Python 3.11
- **ORM:** SQLModel 0.0.8+
- **Database:** Neon Serverless PostgreSQL
- **Authentication:** JWT verification (tokens issued by Better Auth)

### Development Tools
- **Spec Management:** Spec-Kit Plus
- **AI Assistant:** Claude Code
- **Version Control:** Git

## Development Workflow

### Feature Development Process
1. **Specification Phase:** Create feature spec with requirements, acceptance criteria, and test scenarios
2. **Planning Phase:** Generate architectural plan with design decisions and ADRs for significant choices
3. **Task Breakdown:** Decompose plan into testable, dependency-ordered tasks
4. **Implementation Phase:** Execute tasks via Claude Code, validating against acceptance criteria
5. **Review Phase:** Verify implementation matches spec and adheres to constitution

### Code Quality Standards
- All code MUST be readable and maintainable
- Prefer clarity over cleverness
- No premature optimization
- Comments required only for non-obvious logic
- Type hints required for all Python functions
- TypeScript strict mode enabled

### Testing Requirements
- All API endpoints MUST have integration tests
- Database operations MUST be tested
- Authentication flows MUST be tested
- Frontend components MUST handle loading and error states

### Security Standards
- Input validation on all API endpoints
- SQL injection prevention via SQLModel (no raw SQL)
- XSS prevention via React's default escaping
- CSRF protection for state-changing operations
- Secrets management via environment variables
- JWT token expiration and refresh handling

## Governance

### Amendment Process
- Amendments to this constitution require explicit documentation of rationale
- Version number MUST be incremented according to semantic versioning:
  - **MAJOR:** Backward-incompatible changes (e.g., removing a principle, changing tech stack)
  - **MINOR:** Adding new principles or sections
  - **PATCH:** Clarifications, wording improvements, non-semantic changes
- All dependent templates (spec, plan, tasks) MUST be updated to reflect amendments
- Amendment history MUST be tracked in Sync Impact Report

### Compliance
- All pull requests MUST verify compliance with this constitution
- Specs that conflict with this constitution MUST be rejected
- Implementation that violates principles MUST be refactored
- Exceptions require explicit justification and approval

### Conflict Resolution
- Constitution supersedes all other documentation
- When in doubt, refer to Core Principles
- Ambiguities should be resolved via amendment, not interpretation

**Version**: 1.0.0 | **Ratified**: 2026-02-12 | **Last Amended**: 2026-02-12
