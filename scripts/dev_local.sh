#!/bin/bash

# Local development script for ValidateIO (without Docker)
# This runs everything locally on your machine

set -e

echo "🚀 Starting ValidateIO Development Environment (Local Mode)..."
echo "Note: This requires PostgreSQL and Redis to be installed locally"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys before running the agents!"
fi

# Check for local PostgreSQL
if command -v psql &> /dev/null; then
    echo "✅ PostgreSQL found"
else
    echo "❌ PostgreSQL not found. Please install it:"
    echo "   macOS: brew install postgresql"
    echo "   Ubuntu: sudo apt-get install postgresql"
    exit 1
fi

# Check for local Redis
if command -v redis-cli &> /dev/null; then
    echo "✅ Redis found"
else
    echo "❌ Redis not found. Please install it:"
    echo "   macOS: brew install redis"
    echo "   Ubuntu: sudo apt-get install redis-server"
    exit 1
fi

# Start local services
echo "🔧 Starting local services..."

# Start PostgreSQL (if not running)
if ! pg_isready -q; then
    echo "Starting PostgreSQL..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start postgresql
    else
        sudo systemctl start postgresql
    fi
fi

# Start Redis (if not running)
if ! redis-cli ping > /dev/null 2>&1; then
    echo "Starting Redis..."
    if [[ "$OSTYPE" == "darwin"* ]]; then
        brew services start redis
    else
        sudo systemctl start redis
    fi
fi

# Create database if it doesn't exist
echo "📦 Setting up database..."
createdb validateio 2>/dev/null || echo "Database 'validateio' already exists"

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
else
    echo "✅ Python environment exists"
fi

# Update .env with local database URL if needed
if ! grep -q "DATABASE_URL=postgresql" backend/.env 2>/dev/null; then
    echo "DATABASE_URL=postgresql://localhost/validateio" >> backend/.env
fi

# Run database migrations
echo "🔄 Running database migrations..."
cd backend
source .venv/bin/activate
alembic upgrade head
cd ..

# Function to kill processes on exit
cleanup() {
    echo "🛑 Stopping services..."
    kill $FRONTEND_PID $BACKEND_PID $CELERY_PID 2>/dev/null || true
    exit
}

trap cleanup INT TERM

# Start the services
echo "✨ Starting application services..."

# Start frontend
cd frontend && npm run dev &
FRONTEND_PID=$!
echo "Frontend PID: $FRONTEND_PID"

# Start backend
cd ../backend && source .venv/bin/activate && uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
echo "Backend PID: $BACKEND_PID"

# Start Celery worker
cd ../backend && source .venv/bin/activate && celery -A app.worker worker --loglevel=info &
CELERY_PID=$!
echo "Celery PID: $CELERY_PID"

echo ""
echo "🎯 Services started:"
echo "   Frontend: http://localhost:3000"
echo "   Backend API: http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "📊 To test the system:"
echo "   cd backend && python test_operational.py"
echo "   cd backend && python test_validation_pipeline.py"
echo ""
echo "Press Ctrl+C to stop all services..."

# Wait for interrupt
wait