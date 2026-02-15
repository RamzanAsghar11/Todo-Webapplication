# Skill: Frontend Designer
**Skill ID**: frontend-designer  
**Version**: 1.0.0  
**Last Updated**: 2026-02  
**Purpose**: Create modern, high-quality, production-ready user interfaces with excellent UI/UX using Next.js 16+ (App Router) + Tailwind CSS

## Core Competencies

This skill enables the agent to transform product requirements, wireframes, user stories, or design specifications into clean, accessible, responsive, and visually polished frontend implementations.

### Must Always Follow These Principles (Mandatory)

1. Use **Next.js 16+ App Router** exclusively (no Pages Router)
2. Use **Tailwind CSS v3.4+** with modern best practices
3. Write **TypeScript** only (no JavaScript unless explicitly requested)
4. Follow **mobile-first responsive design**
5. Prioritize **accessibility** (WCAG 2.1 AA minimum)
6. Use **semantic HTML** + proper ARIA when needed
7. Create **component-based architecture** with clear composition
8. Apply **consistent design tokens** (colors, spacing, typography, shadows, radii, etc.)
9. Write **self-documenting component code** with JSDoc-style comments
10. Optimize for **performance** & **CLS / LCP / FID** (Core Web Vitals)

## Preferred Tech Stack & Patterns (2025–2026 standards)

| Category              | Technology / Library                          | When to Use / Notes                                      |
|-----------------------|-----------------------------------------------|------------------------------------------------------------------|
| Framework             | Next.js 16+ (App Router)                      | Server Components by default, Client Components only when needed |
| Styling               | Tailwind CSS + PostCSS                        | Arbitrary values & `@apply` used sparingly                       |
| Component Library     | shadcn/ui, Radix UI primitives (via shadcn)  | Strongly preferred base — customize heavily                      |
| Icons                 | lucide-react                                  | Default icon set                                                 |
| Forms                 | react-hook-form + zod                         | For complex / validated forms                                    |
| Data Fetching         | Next.js fetch + React Server Components       | Use `async/await` Server Components whenever possible            |
| State (client)        | Zustand / Jotai / React Context              | Keep it minimal — prefer server state when possible              |
| Animations            | Framer Motion (when micro-interactions needed)| Subtle only unless spec requires otherwise                       |
| Date handling         | date-fns                                      | Lightweight & tree-shakable                                      |
| File / Image          | next/image                                    | Always use for images                                            |

## Directory & Naming Conventions
