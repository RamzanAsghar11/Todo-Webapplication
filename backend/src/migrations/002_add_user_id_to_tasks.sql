-- Migration 002: Add user_id to tasks table
-- Date: 2026-02-13
-- Description: Add user_id foreign key to tasks table for user-scoped data access

-- Add user_id column (nullable initially for migration)
ALTER TABLE tasks ADD COLUMN IF NOT EXISTS user_id_new UUID;

-- Assign all existing tasks to demo user
UPDATE tasks SET user_id_new = '00000000-0000-0000-0000-000000000001' WHERE user_id_new IS NULL;

-- Make user_id NOT NULL
ALTER TABLE tasks ALTER COLUMN user_id_new SET NOT NULL;

-- Drop old user_id column (if it exists as string)
ALTER TABLE tasks DROP COLUMN IF EXISTS user_id;

-- Rename new column to user_id
ALTER TABLE tasks RENAME COLUMN user_id_new TO user_id;

-- Add foreign key constraint
ALTER TABLE tasks ADD CONSTRAINT fk_tasks_user_id
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE;

-- Create index on user_id for query performance
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
