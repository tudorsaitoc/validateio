#!/bin/bash

# Development startup script for ValidateIO

set -e

echo "🚀 Starting ValidateIO Development Environment..."

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys before running the agents!"
fi

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres redis chromadb

# Wait for services to be ready
echo "⏳ Waiting for services to be healthy..."
sleep 10

# Install frontend dependencies if needed
if [ ! -d "frontend/node_modules" ]; then
    echo "📦 Installing frontend dependencies..."
    cd frontend && npm install && cd ..
fi

# Create Python virtual environment if needed
if [ ! -d "backend/.venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    cd ..
fi

# Run database migrations
echo "🔄 Running database migrations..."
if [ -d "backend/.venv" ]; then
    cd backend && source .venv/bin/activate && alembic upgrade head && cd ..
else
    echo "⚠️  Virtual environment not found, skipping migrations"
fi

# Start the services
echo "✨ Starting application services..."

# Use GNU parallel if available, otherwise use background processes
if command -v parallel &> /dev/null; then
    parallel -j 3 ::: \
        "cd frontend && npm run dev" \
        "cd backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000" \
        "cd backend && source .venv/bin/activate && celery -A app.worker worker --loglevel=info"
else
    # Start frontend
    cd frontend && npm run dev &
    FRONTEND_PID=$!
    
    # Start backend
    cd ../backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000 &
    BACKEND_PID=$!
    
    # Start Celery worker
    cd ../backend && source .venv/bin/activate && celery -A app.worker worker --loglevel=info &
    CELERY_PID=$!
    
    echo "🎯 Services started:"
    echo "   Frontend: http://localhost:3000 (PID: $FRONTEND_PID)"
    echo "   Backend API: http://localhost:8000 (PID: $BACKEND_PID)"
    echo "   API Docs: http://localhost:8000/docs"
    echo "   Celery Worker: PID $CELERY_PID"
    echo ""
    echo "Press Ctrl+C to stop all services..."
    
    # Wait for interrupt
    trap "kill $FRONTEND_PID $BACKEND_PID $CELERY_PID; docker-compose down" INT
    wait
fi