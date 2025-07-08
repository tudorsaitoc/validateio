#!/bin/bash

# Optimal Docker development script for ValidateIO
# Uses Docker for databases but runs apps locally for better development experience

set -e

echo "🚀 Starting ValidateIO (Docker Optimal Mode)..."
echo "================================================"
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update .env with your API keys!"
fi

# Copy .env to backend if needed
if [ ! -f backend/.env ]; then
    cp .env backend/.env
fi

# Check for OpenAI API key
if ! grep -q "OPENAI_API_KEY=sk-" backend/.env 2>/dev/null; then
    echo "⚠️  WARNING: OPENAI_API_KEY not configured in backend/.env"
    echo "   The AI agents won't work without it!"
    echo ""
fi

# Start Docker services (databases only)
echo "🐳 Starting Docker services (PostgreSQL, Redis, ChromaDB)..."
docker-compose up -d postgres redis chromadb

# Wait for services
echo "⏳ Waiting for Docker services to be ready..."
sleep 5

# Check service health
echo "🔍 Checking service health..."
docker-compose ps

# Setup backend environment
echo ""
echo "🐍 Setting up backend environment..."
cd backend

# Create virtual environment if needed
if [ ! -d ".venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "📦 Installing backend dependencies..."
pip install -r requirements.txt

# Update database URL to use localhost
export DATABASE_URL="postgresql://postgres:postgres@localhost:5432/validateio"
export REDIS_URL="redis://localhost:6379/0"
export CELERY_BROKER_URL="redis://localhost:6379/0"
export CELERY_RESULT_BACKEND="redis://localhost:6379/0"
export CHROMA_HOST="localhost"
export CHROMA_PORT="8001"

# Run database migrations
echo "🔄 Running database migrations..."
alembic upgrade head

# Return to root
cd ..

# Setup frontend
echo ""
echo "💻 Setting up frontend..."
if [ ! -d "frontend/node_modules" ]; then
    cd frontend
    echo "📦 Installing frontend dependencies..."
    npm install
    cd ..
fi

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "🛑 Stopping services..."
    kill $BACKEND_PID $CELERY_PID $FRONTEND_PID 2>/dev/null || true
    echo "Docker services will continue running. To stop them:"
    echo "  docker-compose down"
    exit
}

trap cleanup INT TERM

# Start services
echo ""
echo "✨ Starting application services..."
echo ""

# Start backend
echo "Starting backend API..."
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Start Celery worker
echo "Starting Celery worker..."
cd backend
source .venv/bin/activate
celery -A app.worker worker --loglevel=info &
CELERY_PID=$!
cd ..

# Start frontend
echo "Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

# Display status
echo ""
echo "====================================================="
echo "🎉 ValidateIO is running!"
echo "====================================================="
echo ""
echo "📍 Services:"
echo "  Frontend:    http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs:    http://localhost:8000/docs"
echo "  Health:      http://localhost:8000/health/detailed"
echo ""
echo "🐳 Docker Services:"
echo "  PostgreSQL:  localhost:5432"
echo "  Redis:       localhost:6379"
echo "  ChromaDB:    localhost:8001"
echo ""
echo "🧪 Test the system:"
echo "  cd backend && python test_operational.py"
echo "  cd backend && python test_validation_pipeline.py"
echo ""
echo "📝 Create a validation:"
echo '  curl -X POST http://localhost:8000/api/v1/validations/ \'
echo '    -H "Content-Type: application/json" \'
echo '    -d "{"business_idea": "AI personal finance app", "industry": "FinTech"}"'
echo ""
echo "Press Ctrl+C to stop all services..."
echo ""

# Keep script running
wait