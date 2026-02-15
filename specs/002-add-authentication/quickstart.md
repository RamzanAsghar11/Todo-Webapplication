# Quick Start Guide: Authentication Setup

**Feature**: Add Authentication to Todo Application
**Date**: 2026-02-13
**Audience**: Developers implementing authentication

## Overview

This guide provides step-by-step instructions for setting up authentication in the Todo Full-Stack Web Application using Better Auth (frontend) and JWT verification (backend).

## Prerequisites

- Node.js 18+ installed
- Python 3.11 installed
- Neon PostgreSQL database accessible
- Existing Todo application running (frontend on port 3000, backend on port 8001)

## Environment Variables Setup

### Step 1: Generate BETTER_AUTH_SECRET

Generate a cryptographically secure random string (minimum 32 characters):

```bash
# Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"

# Using Python
python3 -c "import secrets; print(secrets.token_hex(32))"

# Using OpenSSL
openssl rand -hex 32
```

**Example output**: `a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2`

**IMPORTANT**: Use the SAME secret for both frontend and backend!

### Step 2: Configure Frontend Environment Variables

Create or update `frontend/.env.local`:

```bash
# Navigate to frontend directory
cd frontend

# Create .env.local file
cat > .env.local << 'EOF'
# Better Auth Configuration
BETTER_AUTH_SECRET=<paste-your-generated-secret-here>
NEXT_PUBLIC_APP_URL=http://localhost:3000

# API Configuration (existing)
NEXT_PUBLIC_API_URL=http://localhost:8001
EOF
```

**Example**:
```
BETTER_AUTH_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Step 3: Configure Backend Environment Variables

Update `backend/.env`:

```bash
# Navigate to backend directory
cd backend

# Add to existing .env file
cat >> .env << 'EOF'

# Better Auth Configuration
BETTER_AUTH_SECRET=<paste-the-same-secret-here>
EOF
```

**Example**:
```
# Database (existing)
DATABASE_URL=postgresql://neondb_owner:npg_ioM0xgsEN2IV@ep-twilight-waterfall-ai82nl7n-pooler.c-4.us-east-1.aws.neon.tech/neondb?sslmode=require

# Better Auth Configuration (new)
BETTER_AUTH_SECRET=a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8s9t0u1v2w3x4y5z6a7b8c9d0e1f2
```

**CRITICAL**: Verify that `BETTER_AUTH_SECRET` is IDENTICAL in both files!

## Frontend Setup

### Step 1: Install Better Auth

```bash
cd frontend
npm install better-auth
```

### Step 2: Verify Installation

```bash
npm list better-auth
```

Expected output:
```
todo-frontend@0.1.0 /path/to/frontend
└── better-auth@0.2.0
```

### Step 3: Restart Frontend Development Server

```bash
# Kill existing Next.js process
pkill -f "next dev"

# Start fresh
npm run dev
```

Expected output:
```
▲ Next.js 16.1.6 (Turbopack)
- Local:         http://localhost:3000
- Environments: .env.local

✓ Starting...
✓ Ready in 2s
```

## Backend Setup

### Step 1: Install JWT Library

```bash
cd backend
pip install PyJWT==2.8.0 cryptography==41.0.7
```

### Step 2: Update requirements.txt

```bash
pip freeze | grep -E "(PyJWT|cryptography)" >> requirements.txt
```

### Step 3: Verify Installation

```bash
python3 -c "import jwt; print(f'PyJWT version: {jwt.__version__}')"
```

Expected output:
```
PyJWT version: 2.8.0
```

### Step 4: Restart Backend Server

```bash
# Kill existing uvicorn process
pkill -f "uvicorn"

# Start fresh
cd backend
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

Expected output:
```
INFO:     Uvicorn running on http://0.0.0.0:8001 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

## Database Migration

### Step 1: Backup Database (Recommended)

```bash
# Using Neon CLI or pg_dump
pg_dump $DATABASE_URL > backup_before_auth_migration.sql
```

### Step 2: Run Migration Scripts

**Option A: Using SQLModel (Recommended)**

```python
# backend/src/migrate.py
from sqlmodel import SQLModel, create_engine
from src.models.user import User
from src.models.task import Task
import os

DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Create all tables
SQLModel.metadata.create_all(engine)
print("✓ Migration complete: users table created")
```

Run migration:
```bash
cd backend
python3 -m src.migrate
```

**Option B: Using Raw SQL**

```bash
# Connect to Neon PostgreSQL
psql $DATABASE_URL

-- Run migration SQL from data-model.md
-- (Copy migration scripts from data-model.md)
```

### Step 3: Verify Migration

```bash
# Check users table exists
psql $DATABASE_URL -c "\d users"

# Check tasks table has user_id column
psql $DATABASE_URL -c "\d tasks"

# Verify demo user created
psql $DATABASE_URL -c "SELECT id, email FROM users;"
```

Expected output:
```
                  id                  |      email
--------------------------------------+------------------
 00000000-0000-0000-0000-000000000001 | demo@example.com
```

## Verification Checklist

### Environment Variables

- [ ] `BETTER_AUTH_SECRET` is set in `frontend/.env.local`
- [ ] `BETTER_AUTH_SECRET` is set in `backend/.env`
- [ ] Both secrets are IDENTICAL (compare character by character)
- [ ] `NEXT_PUBLIC_APP_URL` is set to `http://localhost:3000`
- [ ] `DATABASE_URL` is set in `backend/.env`

### Dependencies

- [ ] `better-auth` installed in frontend (`npm list better-auth`)
- [ ] `PyJWT` installed in backend (`pip show PyJWT`)
- [ ] `cryptography` installed in backend (`pip show cryptography`)

### Servers Running

- [ ] Frontend running on http://localhost:3000
- [ ] Backend running on http://localhost:8001
- [ ] No port conflicts (check with `lsof -i :3000` and `lsof -i :8001`)

### Database

- [ ] `users` table exists
- [ ] `tasks` table has `user_id` column
- [ ] Demo user exists in `users` table
- [ ] Existing tasks assigned to demo user

## Testing Authentication Setup

### Test 1: Frontend Environment Variables

```bash
cd frontend
npm run dev
```

Open browser console at http://localhost:3000 and check:
```javascript
console.log(process.env.NEXT_PUBLIC_APP_URL)
// Should output: http://localhost:3000
```

### Test 2: Backend Environment Variables

```bash
cd backend
python3 -c "import os; print('BETTER_AUTH_SECRET:', os.getenv('BETTER_AUTH_SECRET')[:10] + '...')"
```

Expected output:
```
BETTER_AUTH_SECRET: a1b2c3d4e5...
```

### Test 3: Database Connection

```bash
cd backend
python3 -c "from src.database import engine; print('✓ Database connected')"
```

Expected output:
```
✓ Database connected
```

### Test 4: JWT Token Generation (Manual Test)

```python
# backend/test_jwt.py
import jwt
import os
from datetime import datetime, timedelta

SECRET = os.getenv("BETTER_AUTH_SECRET")
payload = {
    "sub": "550e8400-e29b-41d4-a716-446655440000",
    "email": "test@example.com",
    "iat": datetime.utcnow(),
    "exp": datetime.utcnow() + timedelta(hours=24)
}

token = jwt.encode(payload, SECRET, algorithm="HS256")
print(f"Generated token: {token[:50]}...")

# Verify token
decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
print(f"✓ Token verified: {decoded['email']}")
```

Run test:
```bash
cd backend
python3 test_jwt.py
```

Expected output:
```
Generated token: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOi...
✓ Token verified: test@example.com
```

## Common Issues & Troubleshooting

### Issue 1: "Invalid token" error

**Cause**: BETTER_AUTH_SECRET mismatch between frontend and backend

**Solution**:
```bash
# Compare secrets
echo "Frontend secret:"
grep BETTER_AUTH_SECRET frontend/.env.local

echo "Backend secret:"
grep BETTER_AUTH_SECRET backend/.env

# If different, update both to use the same secret
```

### Issue 2: "Authentication required" on all requests

**Cause**: JWT token not being sent in Authorization header

**Solution**:
- Check browser developer tools → Network tab
- Verify Authorization header is present: `Authorization: Bearer <token>`
- Verify Better Auth is configured correctly in frontend

### Issue 3: Frontend not picking up environment variables

**Cause**: Next.js needs rebuild to embed NEXT_PUBLIC_* variables

**Solution**:
```bash
cd frontend
rm -rf .next
npm run dev
```

Hard refresh browser: `Ctrl+Shift+R` (Windows/Linux) or `Cmd+Shift+R` (Mac)

### Issue 4: Database migration fails

**Cause**: Existing tasks table has incompatible schema

**Solution**:
```bash
# Check current schema
psql $DATABASE_URL -c "\d tasks"

# If user_id column already exists as string, drop and recreate
psql $DATABASE_URL -c "ALTER TABLE tasks DROP COLUMN IF EXISTS user_id;"

# Re-run migration
python3 -m src.migrate
```

### Issue 5: CORS error when making authenticated requests

**Cause**: Authorization header not allowed in CORS

**Solution**:
Verify `backend/src/main.py` CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],  # This allows Authorization header
)
```

## Security Checklist

- [ ] BETTER_AUTH_SECRET is at least 32 characters
- [ ] BETTER_AUTH_SECRET is cryptographically random (not a dictionary word)
- [ ] BETTER_AUTH_SECRET is not committed to version control
- [ ] `.env` and `.env.local` are in `.gitignore`
- [ ] Passwords are never logged or exposed in error messages
- [ ] JWT tokens are transmitted over HTTPS in production

## Production Deployment Notes

### Environment Variables

**Frontend (Vercel/Netlify)**:
- Set `BETTER_AUTH_SECRET` in deployment environment variables
- Set `NEXT_PUBLIC_APP_URL` to production domain (e.g., `https://todo.example.com`)

**Backend (Railway/Render/AWS)**:
- Set `BETTER_AUTH_SECRET` (same as frontend)
- Set `DATABASE_URL` to production Neon PostgreSQL connection string

### HTTPS Requirement

- JWT tokens MUST be transmitted over HTTPS in production
- Configure SSL/TLS certificates for both frontend and backend
- Update CORS to allow production domain

### Database Migration

- Run migration on production database during deployment
- Backup database before migration
- Test migration on staging environment first

## Next Steps

After completing this setup:

1. **Verify Setup**: Run all tests in "Testing Authentication Setup" section
2. **Implement Authentication**: Proceed with Phase 2 (Frontend Authentication Setup) from plan.md
3. **Test End-to-End**: Follow acceptance criteria in spec.md

## Support

If you encounter issues not covered in this guide:

1. Check `specs/002-add-authentication/plan.md` for detailed implementation phases
2. Review `specs/002-add-authentication/contracts/` for API specifications
3. Consult Better Auth documentation: https://better-auth.com
4. Check PyJWT documentation: https://pyjwt.readthedocs.io

## Quick Reference

### File Locations

```
frontend/
├── .env.local                    # Frontend environment variables
├── src/lib/auth.ts              # Better Auth configuration (to be created)
└── src/app/layout.tsx           # Auth provider wrapper (to be modified)

backend/
├── .env                         # Backend environment variables
├── src/models/user.py           # User model (to be created)
├── src/middleware/jwt_auth.py   # JWT verification (to be created)
└── src/routers/tasks.py         # Task endpoints (to be modified)
```

### Key Commands

```bash
# Generate secret
openssl rand -hex 32

# Install frontend dependencies
cd frontend && npm install better-auth

# Install backend dependencies
cd backend && pip install PyJWT cryptography

# Run migration
cd backend && python3 -m src.migrate

# Start servers
cd frontend && npm run dev
cd backend && uvicorn src.main:app --port 8001 --reload
```

### Environment Variable Template

**frontend/.env.local**:
```
BETTER_AUTH_SECRET=<your-secret-here>
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8001
```

**backend/.env**:
```
DATABASE_URL=<your-neon-postgresql-url>
BETTER_AUTH_SECRET=<same-secret-as-frontend>
```
