"""Test database connection and table creation."""
import sys
sys.path.insert(0, '/mnt/d/spec-driven-hackathon2/todo-app/backend/src')

from database import engine, create_db_and_tables
from sqlmodel import text

# Test connection
print("Testing database connection...")
try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✓ Database connection successful")
except Exception as e:
    print(f"✗ Database connection failed: {e}")
    sys.exit(1)

# Test table creation
print("\nCreating database tables...")
try:
    create_db_and_tables()
    print("✓ Tables created successfully")
except Exception as e:
    print(f"✗ Table creation failed: {e}")
    sys.exit(1)

# Verify tables exist
print("\nVerifying tables...")
try:
    with engine.connect() as conn:
        result = conn.execute(text(
            "SELECT table_name FROM information_schema.tables "
            "WHERE table_schema = 'public'"
        ))
        tables = [row[0] for row in result]
        print(f"✓ Found tables: {tables}")

        if 'tasks' in tables:
            print("✓ 'tasks' table exists")
        else:
            print("✗ 'tasks' table not found")
            sys.exit(1)
except Exception as e:
    print(f"✗ Table verification failed: {e}")
    sys.exit(1)

print("\n✓ All database tests passed!")
