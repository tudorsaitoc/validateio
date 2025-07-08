#!/bin/bash
echo "Starting ValidateIO Full Stack Development..."

# Start backend
echo "Starting backend..."
cd backend
source .venv/bin/activate 2>/dev/null || python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000 &
BACKEND_PID=$!

# Start frontend
echo "Starting frontend..."
cd ../frontend
npm install
npm run dev &
FRONTEND_PID=$!

echo ""
echo "🚀 Development servers running:"
echo "- Backend: http://localhost:8000"
echo "- Frontend: http://localhost:3000"
echo "- API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait and handle shutdown
trap "kill $BACKEND_PID $FRONTEND_PID" INT
wait
