#!/bin/bash

# Status check script for ValidateIO

set -e

echo "🔍 ValidateIO Status Check"
echo "========================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Docker services
echo "📦 Docker Services:"
if command -v docker-compose &> /dev/null; then
    echo "  PostgreSQL: $(docker-compose ps postgres 2>/dev/null | grep -q "Up" && echo -e "${GREEN}✓ Running${NC}" || echo -e "${RED}✗ Not running${NC}")"
    echo "  Redis:      $(docker-compose ps redis 2>/dev/null | grep -q "Up" && echo -e "${GREEN}✓ Running${NC}" || echo -e "${RED}✗ Not running${NC}")"
    echo "  ChromaDB:   $(docker-compose ps chromadb 2>/dev/null | grep -q "Up" && echo -e "${GREEN}✓ Running${NC}" || echo -e "${RED}✗ Not running${NC}")"
else
    echo -e "  ${RED}Docker Compose not found${NC}"
fi
echo ""

# Check API server
echo "🌐 API Server:"
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ Running at http://localhost:8000${NC}"
    echo "  API Docs: http://localhost:8000/docs"
else
    echo -e "  ${RED}✗ Not running${NC}"
    echo "  Start with: cd backend && uvicorn main:app --reload"
fi
echo ""

# Check frontend
echo "💻 Frontend:"
if curl -s http://localhost:3000 > /dev/null 2>&1; then
    echo -e "  ${GREEN}✓ Running at http://localhost:3000${NC}"
else
    echo -e "  ${RED}✗ Not running${NC}"
    echo "  Start with: cd frontend && npm run dev"
fi
echo ""

# Check Celery worker
echo "⚡ Celery Worker:"
if pgrep -f "celery.*worker" > /dev/null; then
    echo -e "  ${GREEN}✓ Running${NC}"
else
    echo -e "  ${RED}✗ Not running${NC}"
    echo "  Start with: cd backend && celery -A app.worker worker --loglevel=info"
fi
echo ""

# Check environment
echo "🔑 Environment:"
if [ -f .env ]; then
    echo -e "  .env file: ${GREEN}✓ Found${NC}"
    
    # Check API keys (without showing values)
    if grep -q "OPENAI_API_KEY=sk-" .env 2>/dev/null; then
        echo -e "  OpenAI API Key: ${GREEN}✓ Configured${NC}"
    else
        echo -e "  OpenAI API Key: ${YELLOW}⚠ Not configured${NC}"
    fi
    
    if grep -q "DATABASE_URL=" .env 2>/dev/null; then
        echo -e "  Database URL: ${GREEN}✓ Configured${NC}"
    else
        echo -e "  Database URL: ${YELLOW}⚠ Not configured${NC}"
    fi
else
    echo -e "  .env file: ${RED}✗ Not found${NC}"
    echo "  Create with: cp .env.example .env"
fi
echo ""

# Quick start command
echo "🚀 Quick Start:"
echo "  To start all services: ./scripts/dev.sh"
echo ""
echo "📊 Test Pipeline:"
echo "  To test AI agents: cd backend && python test_validation_pipeline.py"
echo ""