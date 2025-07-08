#!/bin/bash

# Minimal startup script - just the API and basic testing

set -e

echo "🚀 Starting ValidateIO Minimal Mode (API only)..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "📋 Creating .env file from .env.example..."
    cp .env.example .env
fi

# Check for .env in backend
if [ ! -f backend/.env ]; then
    cp .env backend/.env
fi

# Check for OpenAI API key
if ! grep -q "OPENAI_API_KEY=sk-" backend/.env 2>/dev/null; then
    echo "⚠️  WARNING: OPENAI_API_KEY not configured!"
    echo "Please add your OpenAI API key to backend/.env"
    echo ""
fi

# Create Python virtual environment if needed
if [ ! -d "backend/.venv" ]; then
    echo "🐍 Creating Python virtual environment..."
    cd backend
    python3 -m venv .venv
    source .venv/bin/activate
    echo "📦 Installing minimal requirements (faster)..."
    pip install -r requirements-minimal.txt
    cd ..
else
    cd backend
    source .venv/bin/activate
    cd ..
fi

echo "✨ Starting API server..."
echo ""
echo "📍 API will be available at:"
echo "   - http://localhost:8000"
echo "   - http://localhost:8000/docs (Swagger UI)"
echo "   - http://localhost:8000/health"
echo ""
echo "🧪 To test the AI pipeline:"
echo "   cd backend && python test_validation_pipeline.py"
echo ""
echo "Press Ctrl+C to stop..."
echo ""

# Start the API
cd backend
source .venv/bin/activate
uvicorn main:app --reload --port 8000