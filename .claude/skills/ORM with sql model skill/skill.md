# Skill: ORM using SQL Model
**Skill ID**: orm-sql-model  
**Version**: 1.0.0  
**Last Updated**: 2026-02  
**Purpose**: Expert-level mastery of defining, querying, migrating and optimizing relational data models using modern TypeScript-first SQL-oriented ORMs, with strong emphasis on clean SQL expression, type safety, performance and serverless/edge compatibility in Next.js 16+ App Router applications.

## Core Philosophy & Approach

This skill focuses on **"SQL Model"** style ORMs — tools that keep you close to real SQL while providing excellent TypeScript inference, autocompletion and safety.

**Primary ORM of choice in 2026 for this skill** → **Drizzle ORM**  
(Prisma remains acceptable when the spec explicitly asks for it or when maximum abstraction + Studio GUI is desired, but default preference leans toward Drizzle for control + performance.)

### Mandatory Principles (Always Enforce)

1. Write **type-safe queries** — never use `any` or `unknown` for result shapes
2. Prefer **SQL-like / composable syntax** over magic object notation when possible
3. Use **server components + Server Actions** as primary data access pattern in Next.js App Router
4. Implement **connection management best-practices** for serverless environments (Vercel, Edge, etc.)
5. Always define **indexes**, **constraints** and **relations** explicitly
6. Write **migrations** that are **reviewable** and **repeatable**
7. Support **both PostgreSQL** (primary) and **MySQL / SQLite** (secondary)
8. Keep business logic **separate** from persistence logic (repository / service layer pattern recommended)
9. Handle **optimistic concurrency**, **soft deletes**, **timestamps** consistently
10. Produce **clean, readable SQL under the hood** — avoid N+1 problems by default

## Recommended Tech Stack (2026)

| Category               | Primary Choice                  | Alternatives                          | Rationale / When to use                                 |
|------------------------|----------------------------------|----------------------------------------|----------------------------------------------------------|
| ORM                    | Drizzle ORM                     | Prisma ORM (schema-first), Kysely     | Drizzle → best perf + SQL control + edge compatibility   |
| Database (dev/prod)    | PostgreSQL                      | MySQL, SQLite (dev/testing)           | Postgres → modern features, JSONB, full-text search      |
| Driver                 | postgres.js / @neondatabase/serverless | libsql (Turso), mysql2              | Neon / Supabase / Turso friendly                         |
| Schema location        | `db/schema.ts`                  | —                                      | Central, importable, type-exportable                     |
| Migrations             | Drizzle Kit                     | Prisma Migrate                        | Drizzle Kit → lightweight, SQL-first                     |
| Query building         | Drizzle core + relational query API | raw SQL via `sql` template          | relational → safest joins & relations                    |
| Transactions           | Drizzle transaction API         | —                                      | nested transactions support                              |
| Zod integration        | zod → parse incoming & outgoing | —                                      | End-to-end type + validation safety                      |

## Directory & File Structure (Recommended)
