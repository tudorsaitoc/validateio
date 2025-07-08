#!/bin/bash

# Script to run database migrations

set -e

echo "🔄 Running database migrations..."

cd backend

# Activate virtual environment if it exists
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

# Run migrations
alembic upgrade head

echo "✅ Migrations applied successfully!"