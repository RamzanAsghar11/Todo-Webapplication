# Skill: Better Auth Authentication
**Skill ID**: better-auth  
**Version**: 1.0.0  
**Last Updated**: 2026-02  
**Purpose**: Master the implementation, configuration, customization, security hardening, and best-practice usage of **Better Auth** — the modern, type-safe, batteries-included authentication & authorization library for TypeScript/JavaScript ecosystems (especially Next.js 16+ App Router, but also compatible with other frameworks).

This skill enables the agent to deliver secure, production-ready auth flows using **Better Auth** as the primary solution — covering email/password, OAuth providers, passkeys/WebAuthn, magic links, 2FA, sessions, JWT handling, organization/team support, rate limiting, CSRF protection, and advanced patterns like multi-tenant auth, role-based access control (RBAC), and session management in serverless/edge environments.

## Core Philosophy & Approach

- **Type-safe by default** — full TypeScript inference for users, sessions, accounts, etc.
- **Minimal boilerplate** — most common flows (sign-in, sign-up, OAuth, password reset) work out-of-the-box
- **Composable & extensible** — plugins architecture for 2FA, passkeys, organizations, magic links, etc.
- **Security-first mindset** — secure defaults, automatic CSRF, secure cookies, argon2 hashing, rate limiting
- **Next.js App Router native** — works beautifully with Server Components, Server Actions, Route Handlers, Middleware
- **Edge & serverless friendly** — supports JWT strategy + stateless sessions when needed

**Primary target stack in 2026**:
- Next.js 16+ App Router
- Drizzle ORM / Prisma / Kysely / any SQL DB via adapters
- Better Auth core + official plugins

## Mandatory Principles (Always Enforce)

1. Use **Better Auth v1.x+** (latest stable at time of implementation)
2. Prefer **cookie-based sessions** by default (most secure for web apps)
3. Use **JWT strategy** only when stateless/edge requirements force it (and accept trade-offs)
4. Always enable **CSRF protection** (automatic in Better Auth)
5. Implement **secure cookie settings** → HttpOnly, Secure, SameSite=Strict/Lax, partitioned when needed
6. Use **argon2id** password hashing (default in Better Auth)
7. Enable **rate limiting** on sensitive endpoints (sign-in, sign-up, OTP)
8. Support **email verification** + **password reset** flows out-of-the-box
9. Use **plugins** for advanced features instead of custom code when possible
10. Keep **user & session types** strongly typed and exported

## Recommended Plugins & Features (2026)

| Feature                  | Plugin / Config                              | When to Use / Notes                                          |
|--------------------------|----------------------------------------------|----------------------------------------------------------------|
| Core auth                | `@better-auth/core`                          | Always — foundation                                            |
| Email/Password           | Built-in                                     | Default credential provider                                    |
| OAuth / Social login     | Built-in + providers                         | Google, GitHub, Discord, Apple, etc.                           |
| Passkeys / WebAuthn      | `@better-auth/passkey`                       | Passwordless / biometric login — strongly recommended          |
| Magic links / OTP        | `@better-auth/magic-link` or OTP plugin      | Email OTP or link-based sign-in                                |
| 2FA / TOTP               | `@better-auth/2fa`                           | For high-security apps                                         |
| Organizations / Teams    | `@better-auth/organization`                  | Multi-tenant, team-based todo apps                             |
| RBAC / Permissions       | Custom via session or organization plugin    | Role + permission checks                                       |
| Database adapter         | Drizzle, Prisma, Kysely, Lucia-style         | Match your ORM choice                                          |
| Session strategy         | Cookie (default) / JWT                       | Cookie → most secure; JWT → edge/microservices                 |

## Directory & Integration Patterns (Next.js App Router)
