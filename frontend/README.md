# Todo Application - Frontend

Next.js 16+ frontend with TypeScript and Tailwind CSS.

## Prerequisites

- Node.js 18+

## Setup

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables:
```bash
cp .env.local.example .env.local
# Edit .env.local and set NEXT_PUBLIC_API_URL (default: http://localhost:8000)
```

3. Run the development server:
```bash
npm run dev
```

The application will start on http://localhost:3000

## Usage

Navigate to http://localhost:3000/test-user/tasks to view and manage tasks.

## Project Structure

```
frontend/
├── src/
│   ├── app/
│   │   ├── layout.tsx                    # Root layout
│   │   ├── page.tsx                      # Home page
│   │   └── [userId]/
│   │       └── tasks/
│   │           ├── page.tsx              # Task list page
│   │           ├── new/
│   │           │   └── page.tsx          # Create task page
│   │           └── [taskId]/
│   │               └── edit/
│   │                   └── page.tsx      # Edit task page
│   ├── components/
│   │   ├── TaskList.tsx                  # Task list component
│   │   ├── TaskForm.tsx                  # Create/edit form
│   │   └── TaskItem.tsx                  # Individual task display
│   ├── lib/
│   │   └── api.ts                        # API client functions
│   └── types/
│       └── task.ts                       # TypeScript type definitions
├── package.json
└── .env.local                            # Environment variables (not in git)
```
