-- Migration 001: Create users table
-- Date: 2026-02-13
-- Description: Add users table for authentication

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    hashed_password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

-- Create index on email for fast authentication lookups
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);

-- Create demo user for existing tasks
INSERT INTO users (id, email, hashed_password, created_at)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'demo@example.com',
    '$2b$12$dummyhashfordemouseronlyfortesting',
    CURRENT_TIMESTAMP
)
ON CONFLICT (id) DO NOTHING;
