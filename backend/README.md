# Todo Application - Backend

FastAPI backend for the Todo application with SQLModel ORM and Neon PostgreSQL.

## Prerequisites

- Python 3.11+
- Neon PostgreSQL database

## Setup

1. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# Edit .env and add your Neon PostgreSQL DATABASE_URL
```

4. Run the server:
```bash
python src/main.py
```

The server will start on http://localhost:8000

## API Documentation

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Project Structure

```
backend/
├── src/
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Environment configuration
│   ├── database.py          # Database connection and session
│   ├── models/
│   │   └── task.py          # SQLModel Task model
│   ├── schemas/
│   │   └── task.py          # Pydantic request/response schemas
│   └── routers/
│       └── tasks.py         # Task CRUD endpoints
├── requirements.txt         # Python dependencies
└── .env                     # Environment variables (not in git)
```
