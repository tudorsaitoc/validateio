# ValidateIO Quick Start Guide

Get ValidateIO operational in 5 minutes!

## Prerequisites

- Python 3.11+ installed
- Node.js 18+ installed (for frontend)
- API Keys: OpenAI (required), Anthropic (optional), Serper (optional)
- Docker & Docker Compose (optional, but recommended)

## 🚨 No Docker? No Problem!

If you don't have Docker installed, you have several options:

### Option 1: Minimal Mode (Fastest)
```bash
# Just run the API server - no database needed for testing
./scripts/start_minimal.sh
```

### Option 2: Local Development Mode
```bash
# Requires local PostgreSQL and Redis
brew install postgresql redis  # macOS
sudo apt-get install postgresql redis-server  # Ubuntu

./scripts/dev_local.sh
```

### Option 3: Install Docker
```bash
./scripts/install_docker.sh  # Shows installation instructions
```

## Step 1: Environment Setup

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit .env and add your API keys (minimum: OPENAI_API_KEY)
nano .env
```

## Step 2: Start Services

```bash
# Option A: Use the dev script (recommended)
./scripts/dev.sh

# Option B: Start services manually
docker-compose up -d postgres redis chromadb
cd backend && python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
```

## Step 3: Verify Installation

```bash
# Run operational test
cd backend
python test_operational.py

# Check API health
curl http://localhost:8000/health/detailed
```

## Step 4: Test the Validation Flow

```bash
# 1. Start the API server (if not using dev.sh)
cd backend && uvicorn main:app --reload

# 2. Start Celery worker (in another terminal)
cd backend && celery -A app.worker worker --loglevel=info

# 3. Create a test validation via API
curl -X POST http://localhost:8000/api/v1/validations/ \
  -H "Content-Type: application/json" \
  -d '{
    "business_idea": "AI-powered personal finance app for millennials",
    "target_market": "Tech-savvy millennials aged 25-35",
    "industry": "FinTech"
  }'
```

## Service URLs

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **Database**: localhost:5432 (PostgreSQL)
- **Redis**: localhost:6379
- **ChromaDB**: localhost:8001

## Common Issues & Solutions

### PostgreSQL Connection Error
```bash
# Ensure PostgreSQL is running
docker-compose ps
docker-compose up -d postgres
```

### Missing API Keys
```bash
# Check which keys are configured
grep -E "OPENAI_API_KEY|ANTHROPIC_API_KEY|SERPER_API_KEY" .env
```

### Python Dependencies Error
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install -r requirements.txt
```

### Migration Error
```bash
# Reset and recreate database
docker-compose down -v
docker-compose up -d postgres
cd backend && alembic upgrade head
```

## What's Working Now

✅ **Backend API**
- User registration/authentication endpoints
- Validation creation and tracking
- Health check endpoints
- Async task processing with Celery

✅ **AI Agents**
- Market Research Agent (competitor analysis, market sizing, trends)
- Experiment Generator Agent (landing pages, A/B tests, copy variations)
- Marketing Autopilot Agent (ad campaigns, content strategy, budget allocation)

✅ **Infrastructure**
- PostgreSQL database with migrations
- Redis for task queue
- ChromaDB for vector storage
- Docker Compose setup

## Next Steps

1. **Frontend Development**
   - Build validation input form
   - Create results dashboard
   - Add real-time status updates

2. **Production Setup**
   - Configure Supabase for managed PostgreSQL
   - Deploy backend to Google Cloud Run
   - Deploy frontend to Vercel
   - Set up monitoring with PostHog

3. **Enhancements**
   - Add WebSocket support for real-time updates
   - Implement rate limiting
   - Add payment integration (Stripe)
   - Enhanced error handling and logging

## Development Commands

```bash
# Run tests
make test

# Format code
make format

# Lint code
make lint

# Build for production
make build

# View logs
docker-compose logs -f
```

## Support

- GitHub Issues: [Report bugs or request features]
- Documentation: See `/docs` directory
- API Reference: http://localhost:8000/docs

---

🚀 **ValidateIO** - Turn your business ideas into validated opportunities!