# Skill: Backend with Python and FastAPI
**Skill ID**: fastapi-backend  
**Version**: 1.0.0  
**Last Updated**: 2026-02  
**Purpose**: Master building modern, high-performance, production-ready RESTful (and WebSocket) backends using **Python 3.11+** and **FastAPI** — with strong emphasis on type safety, async patterns, clean architecture, automatic documentation, security, testing, and deployment readiness. Ideal for API-first applications like todo web apps in a spec-driven development workflow.

This skill enables the agent to transform specifications, user stories, or domain requirements into clean, scalable, well-tested FastAPI backends — often paired with PostgreSQL (via SQLModel / SQLAlchemy / asyncpg) and modern tooling.

## Core Philosophy & Approach

- **Async-first** when I/O-bound (database, external APIs, file ops) — synchronous for CPU-bound only when justified
- **Type hints + Pydantic v2** everywhere for safety, autocompletion & auto-docs
- **Dependency injection** for clean, testable code (databases, auth, config, services)
- **Modular / domain-driven structure** — separate concerns (routers, schemas, services, repositories, models)
- **Production mindset from day one** — logging, error handling, validation, security headers, rate limiting, monitoring hooks
- **Automatic OpenAPI/Swagger + ReDoc** — treat docs as first-class citizen

**Primary ORM/Database choice in 2026** → **SQLModel** (preferred for FastAPI ecosystem harmony)  
Alternatives: SQLAlchemy 2.0+ (more mature/complex needs), asyncpg raw (max perf), Tortoise-ORM (if Django-like feel wanted)

## Mandatory Principles (Always Enforce)

1. Use **Python 3.11+** (ideally 3.12) — leverage new syntax & performance
2. FastAPI **0.110+** + **Pydantic v2** (Annotated, TypeAlias, etc.)
3. **ASGI server**: Uvicorn (with uvloop + httptools when possible)
4. **Dependency injection** via `Depends()` for sessions, current_user, settings, etc.
5. Separate **request schemas** (Create/Update) from **response schemas** & **DB models**
6. Use **lifespan events** for startup/shutdown (db pool init, etc.)
7. Implement **proper exception handlers** (HTTPException, custom handlers)
8. Add **CORS**, **security headers**, **rate limiting** in production config
9. Write **unit + integration tests** with `TestClient` + pytest + anyio
10. Structure code for **scalability** — routers per domain, services/repositories pattern

## Recommended Tech Stack (2026)

| Category              | Primary Choice                          | Alternatives                          | When / Notes                                           |
|-----------------------|-----------------------------------------|---------------------------------------|--------------------------------------------------------|
| Framework             | FastAPI                                 | —                                     | —                                                      |
| Data Validation       | Pydantic v2                             | —                                     | Annotated types, strict mode, custom validators        |
| ORM / DB Layer        | SQLModel (sync + async)                 | SQLAlchemy 2.0+, asyncpg raw          | SQLModel → best FastAPI integration + type safety      |
| Migrations            | Alembic (with SQLAlchemy/SQLModel)      | —                                     | Auto-generate + manual review                          |
| Async Driver          | asyncpg (PostgreSQL)                    | —                                     | Neon/Supabase friendly                                 |
| Auth                  | OAuth2 + JWT (fastapi-users / PyJWT)    | HTTP Basic, API Keys                  | Use dependencies for current_user                      |
| Config                | Pydantic Settings (BaseSettings)       | python-dotenv                         | .env + .env.example                                    |
| Testing               | pytest + pytest-asyncio + anyio         | unittest                              | Use TestClient                                         |
| Logging               | structlog / python-json-logger          | logging                               | Structured + correlation IDs                           |
| Deployment            | Docker + Uvicorn/Gunicorn               | Railway/Fly.io/Render                 | Multi-stage builds                                     |

## Directory & File Structure (Recommended – Domain/Feature Modular)
