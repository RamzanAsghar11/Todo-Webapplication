# Skill: Neon Serverless PostgreSQL Database
**Skill ID**: neon-serverless-postgres  
**Version**: 1.0.0  
**Last Updated**: 2026-02  
**Purpose**: Master the architecture, configuration, best practices, integration patterns, performance optimization, and developer workflows for **Neon** — the leading serverless PostgreSQL platform with separated compute/storage, instant branching, autoscaling, scale-to-zero, and strong Next.js + TypeScript ecosystem compatibility.

This skill enables the agent to design, implement, troubleshoot, and optimize Neon-powered database setups, especially in serverless/edge environments (Vercel, Cloudflare, etc.) for modern full-stack applications like todo apps built with Next.js App Router.

## Core Philosophy & Approach

- **Serverless-first PostgreSQL** — true separation of storage & compute
- **Branching as a first-class citizen** — treat databases like code (git-style workflows)
- **Pay-per-use + scale-to-zero** — but intelligently manage cold starts & always-on needs
- **Edge & serverless friendly** — HTTP/WebSocket drivers over TCP when appropriate
- **Production reliability** — balance developer velocity with stability

**Primary integration targets in 2026**:
- Drizzle ORM (preferred for SQL-like control)
- Prisma ORM (when heavy abstraction + type-safety is prioritized)
- Next.js 16+ App Router + Server Components / Server Actions

## Mandatory Principles (Always Enforce)

1. Use **pooled connection strings** (`-pooler` hostname) for most applications (>10–20 concurrent connections expected)
2. Prefer **Neon serverless driver** (`@neondatabase/serverless`) + HTTP/WebSocket mode in edge/serverless runtimes
3. **Disable scale-to-zero** on production primary branch (or set very high min compute) to avoid cold-start latency
4. Leverage **database branching** for preview environments, feature branches, CI/CD, experiments
5. Implement **connection management** carefully — singleton/cached pools, per-request in pure serverless
6. Always define **connection strings** via environment variables with pooling vs direct variants
7. Use **autoscaling ranges** (min–max CU) on production branches
8. Monitor **compute usage**, **active time**, **written data** for cost & perf tuning
9. Enable **point-in-time recovery** (PITR) in production (adjust retention based on risk)
10. Apply **connection pooling best practices** — limit max connections per function/environment

## Recommended Tech Stack & Patterns (2026)

| Category                  | Primary Recommendation                          | Alternatives / Notes                                                                 |
|---------------------------|--------------------------------------------------|---------------------------------------------------------------------------------------|
| Connection Driver         | @neondatabase/serverless (WebSocket or HTTP)    | postgres.js (direct), libsql (if Turso-like needed)                                  |
| ORM                       | Drizzle ORM + neon-serverless / neon-http       | Prisma + @prisma/adapter-neon / PrismaNeon adapter                                   |
| Pooling                   | Neon's built-in PgBouncer pooler endpoint       | Custom pool only if very specific needs                                               |
| Branching Use-case        | Preview deployments (Vercel), feature dev       | Schema diffing + migration application per branch                                     |
| Autoscaling               | Enabled with sensible min/max CU range          | Disable on tiny/hobby projects; always-on for latency-critical                       |
| Cold-start Mitigation     | Keep primary always-on + prepared statements    | Use connection init in global scope where safe                                        |
| Local Dev                 | Docker Compose or local Postgres mirror         | neonctl + local proxy if needed                                                       |

## Connection String Patterns

- **Direct (non-pooled)**: `postgresql://user:pass@ep-project-123456.us-east-2.aws.neon.tech/dbname?sslmode=require`
- **Pooled** (recommended): `postgresql://user:pass@ep-project-123456-pooler.us-east-2.aws.neon.tech/dbname?sslmode=require&pgbouncer=true`
- **Non-pooling variant** (direct for long transactions): append `-non-pooling` or use separate endpoint

## Best Practices Checklist

- [ ] Use **pooled endpoint** by default for Next.js apps
- [ ] Set **production branch compute** → always active (scale-to-zero = off) or min CU ≥ 1–2
- [ ] Configure **autoscaling range** (e.g. 0.25–8 CU) on production
- [ ] Create **read replicas** (lightweight branches) for analytics / read-heavy jobs
- [ ] Use **instant branching** for preview environments (one branch per Vercel preview)
- [ ] Implement **retry logic** + **exponential backoff** for transient errors (cold starts, network)
- [ ] Keep **written data volume** in mind — heavy writes increase storage cost
- [ ] Use **Neon console / API / neonctl** for branch automation in CI/CD
- [ ] Monitor **connection usage** — avoid exhausting pool limits
- [ ] Prefer **Drizzle HTTP driver** in edge functions when transactions are simple

## Common Patterns to Produce

1. **Singleton Neon client** in Next.js Server Components/Actions
2. **Branch-aware connection strings** for preview/prod separation
3. **Migration workflow** with Drizzle Kit across branches
4. **Read replica routing** for reporting / heavy SELECTs
5. **Cost-optimized configuration** for dev/staging (scale-to-zero + short idle timeout)
6. **Branch creation / promotion script** (feature → staging → prod)
7. **Cold-start friendly** query patterns (prepared statements, minimal roundtrips)

## Example Invocation Prompts That Activate This Skill

- "Set up Neon project + branching strategy for Next.js todo app with preview environments"
- "Configure Drizzle ORM with Neon pooled + non-pooled connections for Vercel deployment"
- "Create production-ready Neon compute settings: autoscaling, scale-to-zero policy, replicas"
- "Implement branch-per-preview-deployment pattern with Vercel + Neon API"
- "Optimize Neon costs for a low-traffic todo app while keeping good UX"
- "Add read replica for todo analytics dashboard using Drizzle"

## Anti-Patterns to Avoid

- Using direct (non-pooled) connection in high-concurrency serverless apps
- Leaving scale-to-zero enabled on production primary branch
- Creating hundreds of branches without cleanup policy
- Ignoring cold-start latency in user-facing paths
- Over-relying on HTTP driver for long-running / interactive transactions
- Not distinguishing pooled vs direct endpoints in code
- Missing retry handling for transient Neon errors

---

**This skill is mastered by**: database-architect subagent  
**Related skills**: orm-sql-model, drizzle-orm-specialist, prisma-orm-specialist, nextjs-data-layer-architect, postgres-expert, serverless-patterns

Use this skill to deliver reliable, cost-efficient, developer-friendly Neon PostgreSQL integrations — especially leveraging branching and serverless characteristics to accelerate development velocity while maintaining production-grade stability.