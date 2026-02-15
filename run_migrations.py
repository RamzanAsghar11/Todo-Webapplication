"""Database migration using SQLModel."""
import os
import sys
from sqlmodel import SQLModel, create_engine, Session, select
from dotenv import load_dotenv
import uuid

# Add backend/src to path
sys.path.insert(0, 'backend/src')

# Load environment variables
load_dotenv('backend/.env')

DATABASE_URL = os.getenv('DATABASE_URL')

# Import models
from models.user import User
from models.task import Task

def run_migrations():
    """Create all tables and setup demo user."""
    print("Creating database engine...")
    engine = create_engine(DATABASE_URL, echo=True)

    print("\nCreating all tables...")
    SQLModel.metadata.create_all(engine)
    print("✓ Tables created successfully")

    print("\nCreating demo user...")
    with Session(engine) as session:
        # Check if demo user exists
        demo_user_id = uuid.UUID('00000000-0000-0000-0000-000000000001')
        existing_user = session.get(User, demo_user_id)

        if not existing_user:
            demo_user = User(
                id=demo_user_id,
                email='demo@example.com',
                hashed_password='$2b$12$dummyhashfordemouseronlyfortesting'
            )
            session.add(demo_user)
            session.commit()
            print("✓ Demo user created")
        else:
            print("✓ Demo user already exists")

        # Update existing tasks to belong to demo user
        print("\nUpdating existing tasks to belong to demo user...")
        tasks = session.exec(select(Task)).all()
        updated_count = 0
        for task in tasks:
            if task.user_id != demo_user_id:
                task.user_id = demo_user_id
                updated_count += 1

        if updated_count > 0:
            session.commit()
            print(f"✓ Updated {updated_count} tasks to belong to demo user")
        else:
            print("✓ All tasks already belong to demo user")

    print("\n✓ All migrations completed successfully")

if __name__ == "__main__":
    run_migrations()
