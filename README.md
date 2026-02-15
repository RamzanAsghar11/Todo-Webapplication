# Todo App - Authentication Setup

## Overview

This Todo application now includes full authentication using Better Auth (frontend) and JWT verification (backend).

## Features

- User registration with email and password
- User sign-in with JWT token issuance
- Protected task endpoints (users can only access their own tasks)
- Session persistence across browser restarts (24-hour expiration)
- Secure password hashing with bcrypt
- JWT-based stateless authentication

## Environment Variables

### Frontend (.env.local)

```
BETTER_AUTH_SECRET=<your-secret-here>
NEXT_PUBLIC_APP_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8001
```

### Backend (.env)

```
DATABASE_URL=<your-neon-postgresql-url>
BETTER_AUTH_SECRET=<same-secret-as-frontend>
```

**IMPORTANT**: The `BETTER_AUTH_SECRET` must be identical in both frontend and backend.

## Setup Instructions

### 1. Install Dependencies

**Frontend:**
```bash
cd frontend
npm install
```

**Backend:**
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `.env.local` in the frontend directory and `.env` in the backend directory with the required variables (see above).

### 3. Run Database Migrations

```bash
python run_migrations.py
```

This will:
- Create the `users` table
- Add `user_id` foreign key to `tasks` table
- Create a demo user account
- Assign existing tasks to the demo user

### 4. Start the Servers

**Backend:**
```bash
cd backend
source venv/bin/activate
uvicorn src.main:app --host 0.0.0.0 --port 8001 --reload
```

**Frontend:**
```bash
cd frontend
npm run dev
```

## API Endpoints

### Authentication

- `POST /api/auth/signup` - Create new user account
- `POST /api/auth/signin` - Sign in and receive JWT token
- `POST /api/auth/signout` - Sign out (client-side token removal)

### Tasks (Protected)

All task endpoints require a valid JWT token in the `Authorization: Bearer <token>` header.

- `GET /api/{user_id}/tasks` - Get all tasks for authenticated user
- `POST /api/{user_id}/tasks` - Create new task
- `GET /api/{user_id}/tasks/{id}` - Get specific task
- `PUT /api/{user_id}/tasks/{id}` - Update task
- `DELETE /api/{user_id}/tasks/{id}` - Delete task

## Security Features

- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens signed with HS256 algorithm
- Token expiration: 24 hours
- User ID verification: Backend verifies JWT user_id matches URL user_id
- Data isolation: Users can only access their own tasks
- CORS configured for localhost:3000 and localhost:3001

## Testing

### Manual Testing Checklist

1. **Registration**
   - Navigate to http://localhost:3000/signup
   - Create account with email and password (min 8 characters)
   - Verify redirect to sign-in page

2. **Sign In**
   - Navigate to http://localhost:3000/signin
   - Sign in with registered credentials
   - Verify redirect to tasks page
   - Check browser developer tools for JWT token

3. **Protected Access**
   - Create tasks while signed in
   - Sign out and verify redirect to sign-in
   - Try accessing http://localhost:3000 without authentication
   - Verify redirect to sign-in page

4. **Data Isolation**
   - Create two user accounts
   - Sign in as User A, create tasks
   - Sign out, sign in as User B
   - Verify User B cannot see User A's tasks

5. **Session Persistence**
   - Sign in successfully
   - Refresh the page - verify still authenticated
   - Close and reopen browser - verify still authenticated (within 24 hours)

## Troubleshooting

### "Invalid token" or "Authentication required" errors

- Verify `BETTER_AUTH_SECRET` is identical in both `.env.local` and `.env`
- Check that JWT token is being sent in Authorization header
- Verify token hasn't expired (24-hour limit)

### "Access denied" (403) errors

- This means the JWT user_id doesn't match the URL user_id
- Ensure you're using the correct user_id from the authenticated session

### Frontend not picking up environment variables

- Restart the Next.js dev server after changing `.env.local`
- Hard refresh browser (Ctrl+Shift+R or Cmd+Shift+R)

### Database connection errors

- Verify `DATABASE_URL` is correct in `backend/.env`
- Ensure Neon PostgreSQL database is accessible
- Check that migrations have been run successfully

## Architecture

### Frontend (Next.js 16+ App Router)
- Better Auth for authentication
- JWT tokens stored in localStorage
- Authorization header added to all API requests
- Automatic redirect to sign-in for unauthenticated users

### Backend (Python FastAPI)
- JWT verification middleware
- User-scoped data access
- SQLModel ORM with Neon PostgreSQL
- Stateless authentication (no server-side sessions)

### Database (Neon PostgreSQL)
- `users` table: id (UUID), email, hashed_password, created_at
- `tasks` table: id (UUID), user_id (FK), title, completed, created_at, updated_at

## Production Deployment

### Environment Variables

Set the following in your production environment:

**Frontend:**
- `BETTER_AUTH_SECRET` - Same as backend
- `NEXT_PUBLIC_APP_URL` - Your production domain (e.g., https://todo.example.com)
- `NEXT_PUBLIC_API_URL` - Your backend API URL

**Backend:**
- `BETTER_AUTH_SECRET` - Same as frontend
- `DATABASE_URL` - Production Neon PostgreSQL connection string

### Security Checklist

- [ ] HTTPS enabled for both frontend and backend
- [ ] `BETTER_AUTH_SECRET` is cryptographically random (32+ characters)
- [ ] Secrets not committed to version control
- [ ] CORS configured for production domain only
- [ ] Database backups configured
- [ ] Rate limiting enabled on authentication endpoints (recommended)

## License

MIT
