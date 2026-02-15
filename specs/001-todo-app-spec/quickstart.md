# Quickstart Guide: Todo Application

**Feature**: 001-todo-app-spec
**Last Updated**: 2026-02-12

## Overview

This guide provides step-by-step instructions to set up and run the Todo Full-Stack Web Application locally. The application consists of a FastAPI backend and a Next.js frontend.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.11 or higher** - [Download Python](https://www.python.org/downloads/)
- **Node.js 18 or higher** - [Download Node.js](https://nodejs.org/)
- **Neon PostgreSQL Database** - [Sign up for Neon](https://neon.tech/)

### Verify Prerequisites

```bash
# Check Python version
python --version  # Should be 3.11+

# Check Node.js version
node --version  # Should be 18+

# Check npm version
npm --version
```

## Database Setup

### 1. Create Neon PostgreSQL Database

1. Sign up for a free account at [neon.tech](https://neon.tech/)
2. Create a new project
3. Copy the connection string from the Neon dashboard
4. The connection string format:
   ```
   postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require
   ```

**Important**: Keep this connection string secure. You'll need it for the backend setup.

## Backend Setup

### 1. Navigate to Backend Directory

```bash
cd backend
```

### 2. Create Python Virtual Environment

**On macOS/Linux:**
```bash
python -m venv venv
source venv/bin/activate
```

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

You should see `(venv)` in your terminal prompt indicating the virtual environment is active.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**Expected dependencies:**
- fastapi>=0.104.0
- sqlmodel>=0.0.8
- uvicorn[standard]>=0.24.0
- psycopg2-binary>=2.9.9
- python-dotenv>=1.0.0

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your Neon database URL
# Use your preferred text editor (nano, vim, code, etc.)
nano .env
```

**Add the following to `.env`:**
```env
DATABASE_URL=postgresql://[user]:[password]@[endpoint]/[database]?sslmode=require
```

Replace the placeholder with your actual Neon connection string.

### 5. Start the Backend Server

```bash
python src/main.py
```

**Expected output:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

**Verify backend is running:**
- Open browser to http://localhost:8000/docs
- You should see the FastAPI interactive API documentation (Swagger UI)

**Keep this terminal open** - the backend server needs to stay running.

## Frontend Setup

### 1. Open New Terminal

Open a new terminal window/tab (keep the backend terminal running).

### 2. Navigate to Frontend Directory

```bash
cd frontend
```

### 3. Install Dependencies

```bash
npm install
```

**Expected dependencies:**
- next>=16.0.0
- react>=18.0.0
- react-dom>=18.0.0
- typescript>=5.0.0
- tailwindcss>=3.4.0

### 4. Configure Environment Variables

```bash
# Copy the example environment file
cp .env.local.example .env.local

# Edit .env.local
nano .env.local
```

**Add the following to `.env.local`:**
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 5. Start the Frontend Development Server

```bash
npm run dev
```

**Expected output:**
```
  ▲ Next.js 16.x.x
  - Local:        http://localhost:3000
  - Ready in 2.3s
```

**Verify frontend is running:**
- Open browser to http://localhost:3000
- You should see the Todo application home page

## Testing the Application

### 1. Navigate to Task List

Open your browser to:
```
http://localhost:3000/test-user/tasks
```

Replace `test-user` with any user identifier you want to use for testing.

### 2. Create Your First Task

1. Click the "Create Task" or "Add Task" button
2. Enter a title (required): e.g., "Buy groceries"
3. Optionally enter a description: e.g., "Milk, eggs, bread"
4. Click "Save" or "Create"
5. You should see your new task appear in the list

### 3. Test CRUD Operations

**View Tasks:**
- Navigate to the task list page
- All your tasks should be displayed

**Update a Task:**
1. Click "Edit" on a task
2. Modify the title or description
3. Click "Save"
4. Verify the changes appear in the list

**Toggle Completion:**
1. Click the checkbox or "Mark Complete" button on a task
2. The task should show as completed (e.g., strikethrough text)
3. Click again to mark as incomplete

**Delete a Task:**
1. Click "Delete" on a task
2. Confirm the deletion if prompted
3. The task should disappear from the list

### 4. Verify Persistence

1. Refresh the browser page
2. All your tasks should still be there
3. Stop both servers (Ctrl+C in both terminals)
4. Restart both servers
5. Navigate back to the task list
6. Your tasks should still be persisted

## API Endpoints

The backend exposes the following REST API endpoints:

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/{user_id}/tasks` | Get all tasks for a user |
| POST | `/api/{user_id}/tasks` | Create a new task |
| GET | `/api/{user_id}/tasks/{id}` | Get a single task |
| PUT | `/api/{user_id}/tasks/{id}` | Update a task |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete a task |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle task completion |

**Interactive API Documentation:**
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Troubleshooting

### Backend Issues

**Problem: "ModuleNotFoundError: No module named 'fastapi'"**
- Solution: Ensure virtual environment is activated and dependencies are installed
  ```bash
  source venv/bin/activate  # or venv\Scripts\activate on Windows
  pip install -r requirements.txt
  ```

**Problem: "Could not connect to database"**
- Solution: Verify DATABASE_URL in `.env` is correct
- Check Neon dashboard to ensure database is active
- Ensure connection string includes `?sslmode=require`

**Problem: "Port 8000 already in use"**
- Solution: Kill the process using port 8000 or change the port in `main.py`
  ```bash
  # Find process on port 8000
  lsof -i :8000  # macOS/Linux
  netstat -ano | findstr :8000  # Windows
  ```

### Frontend Issues

**Problem: "Cannot connect to backend API"**
- Solution: Verify backend is running on http://localhost:8000
- Check NEXT_PUBLIC_API_URL in `.env.local` is correct
- Check browser console for CORS errors

**Problem: "CORS error when calling API"**
- Solution: Ensure FastAPI CORS middleware is configured in backend
- Verify `allow_origins` includes `http://localhost:3000`

**Problem: "Port 3000 already in use"**
- Solution: Kill the process or use a different port
  ```bash
  # Use different port
  npm run dev -- -p 3001
  ```

### Database Issues

**Problem: "SSL connection required"**
- Solution: Add `?sslmode=require` to your DATABASE_URL

**Problem: "Table does not exist"**
- Solution: Ensure backend has started at least once to create tables
- Check backend logs for table creation messages

## Development Workflow

### Making Changes

**Backend Changes:**
1. Edit Python files in `backend/src/`
2. Server auto-reloads on file changes (if using `--reload` flag)
3. Test changes via Swagger UI or frontend

**Frontend Changes:**
1. Edit TypeScript/React files in `frontend/src/`
2. Next.js auto-reloads on file changes (Fast Refresh)
3. Changes appear immediately in browser

### Stopping the Servers

**Backend:**
- Press `Ctrl+C` in the backend terminal
- Deactivate virtual environment: `deactivate`

**Frontend:**
- Press `Ctrl+C` in the frontend terminal

### Restarting the Servers

Follow the "Start the Backend Server" and "Start the Frontend Development Server" steps above.

## Next Steps

- **Add more tasks** and test all CRUD operations
- **Test on mobile** by accessing http://localhost:3000 from your phone (use your computer's IP address)
- **Explore the API** using the Swagger UI at http://localhost:8000/docs
- **Review the code** to understand the implementation

## Additional Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **SQLModel Documentation**: https://sqlmodel.tiangolo.com/
- **Next.js Documentation**: https://nextjs.org/docs
- **Neon Documentation**: https://neon.tech/docs

## Support

If you encounter issues not covered in this guide:
1. Check the backend logs in the terminal
2. Check the browser console for frontend errors
3. Review the API documentation at http://localhost:8000/docs
4. Verify all prerequisites are correctly installed
