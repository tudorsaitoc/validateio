# ValidateIO

AI-powered business idea validation platform that automates market research, generates experiments, and runs marketing campaigns.

## Project Structure

```
validateio/
├── frontend/          # Next.js 14 frontend application
├── backend/           # FastAPI backend with AI agents
├── shared/            # Shared types and utilities
├── infrastructure/    # IaC and deployment configurations
├── scripts/           # Development and deployment scripts
└── docs/              # Project documentation
```

## Tech Stack

### Frontend
- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS + shadcn/ui
- **State**: Zustand
- **API Client**: TanStack Query

### Backend
- **Framework**: FastAPI
- **Language**: Python 3.11+
- **AI/LLM**: LangChain + OpenAI/Anthropic
- **Task Queue**: Celery + Redis
- **Database**: PostgreSQL (Supabase)
- **Vector Store**: ChromaDB

### Infrastructure
- **Frontend Hosting**: Vercel
- **Backend Hosting**: Google Cloud Run
- **Database**: Supabase
- **File Storage**: Google Cloud Storage
- **Analytics**: PostHog
- **Email**: Resend

## Getting Started

### Prerequisites
- Node.js 18+
- Python 3.11+
- Docker & Docker Compose
- Git
- OpenAI API Key (required)

### Quick Start

1. Clone the repository:
```bash
git clone <repository-url>
cd validateio
```

2. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your API keys (minimum: OPENAI_API_KEY)
nano .env
```

3. Start everything:
```bash
./scripts/dev.sh
```

4. Verify installation:
```bash
# Check service status
./scripts/check_status.sh

# Run operational test
cd backend && python test_operational.py

# Test the full AI pipeline
cd backend && python test_validation_pipeline.py
```

### Alternative Manual Setup
```bash
# Start Docker services
docker-compose up -d postgres redis chromadb

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload

# Frontend setup (in another terminal)
cd frontend
npm install
npm run dev

# Celery worker (in another terminal)
cd backend
celery -A app.worker worker --loglevel=info
```

## Development Workflow

- Frontend runs on http://localhost:3000
- Backend API runs on http://localhost:8000
- API documentation available at http://localhost:8000/docs

## Project Timeline

- **Weeks 1-3**: Technical foundation setup ✓
- **Weeks 4-8**: MVP development (Current Phase)
- **Weeks 9-12**: Go-to-market execution

## Deployment

### Quick Deployment Guide

1. **Set up Supabase:**
   - Create a new Supabase project
   - Run migrations: `cd backend/supabase && supabase db push`
   - Copy connection strings to your environment

2. **Deploy Backend:**
   - Push to GitHub to trigger automated deployment
   - Or deploy manually to your preferred platform (Vercel, Railway, Render)

3. **Deploy Frontend:**
   - Connect your GitHub repo to Vercel
   - Set environment variables in Vercel dashboard
   - Deploy with one click

4. **Verify Deployment:**
   ```bash
   # Test Supabase connection
   python scripts/test_supabase_connection.py
   
   # Test deployed API
   python scripts/test_deployed_api.py https://your-api-url.com
   ```

See [DEPLOYMENT_VERIFICATION.md](DEPLOYMENT_VERIFICATION.md) for detailed verification steps.

## Current Status

### ✅ Completed
- Basic project structure with monorepo setup
- Frontend initialized with Next.js 14, TypeScript, Tailwind CSS, shadcn/ui
- Backend initialized with FastAPI, async support, and basic API structure
- Authentication endpoints (register, login, refresh token)
- Validation API endpoints with background task processing
- Docker Compose configuration for all services
- Development scripts and tooling
- Market Research Agent with structured output parsing
- SQLAlchemy models for User and Validation
- Database configuration with async support
- Alembic setup for database migrations
- Celery worker configuration and task definitions
- Validation service with async task processing
- Enhanced API endpoints with task tracking
- Deployment verification scripts and documentation

### 🚧 TODO
- Complete AI agents (Experiment Generator, Marketing Autopilot)
- Integrate Supabase for database and authentication
- Add comprehensive test suites
- Set up CI/CD pipelines
- Implement frontend pages (validation flow, dashboard, results)
- Add real-time updates via WebSockets
- Integrate payment processing (when needed)
- Add monitoring and analytics
- Implement rate limiting and cost controls

## License

Proprietary - All rights reserved