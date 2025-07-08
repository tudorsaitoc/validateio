#!/bin/bash

# Quick start with minimal requirements - get ValidateIO running FAST!

set -e

echo "🚀 ValidateIO Quick Start (Docker + Minimal Deps)"
echo "================================================"
echo ""

# Check Docker services
echo "🐳 Docker services status:"
docker-compose ps
echo ""

# Quick backend setup
echo "🐍 Setting up backend with minimal dependencies..."
cd backend

# Create fresh virtual environment
if [ -d ".venv_quick" ]; then
    rm -rf .venv_quick
fi

python3 -m venv .venv_quick
source .venv_quick/bin/activate

# Install only what we need to run
echo "📦 Installing core dependencies only..."
pip install fastapi uvicorn python-dotenv pydantic pydantic-settings
pip install openai langchain langchain-openai httpx
pip install sqlalchemy asyncpg alembic
pip install celery redis

# Copy environment if needed
if [ ! -f .env ]; then
    cp ../.env.example .env
fi

# Check for API key
if grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
    echo "✅ OpenAI API key found!"
else
    echo "⚠️  Please add your OpenAI API key to backend/.env"
fi

# Set database URL for localhost
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/validateio"

# Run migrations
echo "🔄 Running database migrations..."
alembic upgrade head || echo "⚠️  Migrations skipped (may need to create database first)"

echo ""
echo "✨ Starting API server..."
echo ""
echo "📍 Services:"
echo "  API:     http://localhost:8000"
echo "  Docs:    http://localhost:8000/docs"
echo "  Health:  http://localhost:8000/health"
echo ""
echo "🧪 Test the AI pipeline:"
echo "  python test_validation_pipeline.py"
echo ""
echo "Press Ctrl+C to stop..."
echo ""

# Start the API
uvicorn main:app --reload --port 8000