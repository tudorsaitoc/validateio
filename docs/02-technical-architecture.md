# Technical Architecture

## System Overview

```
[Frontend: Next.js on Vercel]
    ↓ REST API
[Backend: FastAPI on Cloud Run]
    ↓ Agents via Celery
[Agent Layer: 3 Python workers]
    ├── Market Research Agent
    ├── Experiment Generator Agent
    └── Marketing Autopilot Agent
    ↓ Store results
[Data: Supabase Postgres + GCS]
```

## Core Components

### Frontend Layer
- **Framework**: Next.js 14 with App Router
- **Styling**: Tailwind CSS + shadcn/ui components
- **State Management**: Zustand for client state
- **Deployment**: Vercel with automatic preview deployments

### Backend API
- **Framework**: FastAPI for async Python API
- **Authentication**: Supabase Auth integration
- **Task Queue**: Celery with Redis broker
- **Deployment**: Google Cloud Run (serverless)

### Agent Infrastructure
- **Orchestration**: LangChain for agent workflows
- **LLM Clients**: OpenAI and Anthropic SDKs
- **Memory**: ChromaDB for vector storage
- **Tools**: Custom tool implementations for web scraping, API calls

### Data Layer
- **Primary Database**: Supabase PostgreSQL
  - User data and authentication
  - Project and validation results
  - Agent task history
- **Object Storage**: Google Cloud Storage
  - Generated landing pages
  - Scraped competitor data
  - Agent artifacts
- **Vector Store**: ChromaDB
  - Agent memory and context
  - Semantic search capabilities

## Local Development Setup

```bash
# setup.sh
#!/bin/bash

# 1. Python environment (3.11+)
python -m venv venv
source venv/bin/activate
pip install poetry
poetry init
poetry add fastapi celery openai anthropic langchain chromadb

# 2. Node.js environment
npm init -y
npm install next react react-dom tailwindcss

# 3. Docker services
docker-compose up -d
# Includes: PostgreSQL, Redis, ChromaDB

# 4. Environment variables
cp .env.example .env.local
# Add API keys and service URLs

# 5. Database migrations
alembic upgrade head

# 6. Start development servers
# Terminal 1: FastAPI
uvicorn main:app --reload

# Terminal 2: Celery
celery -A tasks worker --loglevel=info

# Terminal 3: Next.js
npm run dev
```

## Docker Compose Configuration

```yaml
version: '3.8'
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: validateio
      POSTGRES_USER: dev
      POSTGRES_PASSWORD: devpass
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  chromadb:
    image: chromadb/chroma:latest
    ports:
      - "8000:8000"
    volumes:
      - chroma_data:/chroma/chroma

volumes:
  postgres_data:
  chroma_data:
```

## API Design

### RESTful Endpoints
```
POST   /api/auth/signup
POST   /api/auth/login
GET    /api/auth/me

GET    /api/projects
POST   /api/projects
GET    /api/projects/{id}
PUT    /api/projects/{id}
DELETE /api/projects/{id}

POST   /api/validations
GET    /api/validations/{id}
GET    /api/validations/{id}/status

POST   /api/agents/market-research
POST   /api/agents/experiment-generator
POST   /api/agents/marketing-autopilot
GET    /api/agents/tasks/{task_id}
```

### WebSocket Events
```
ws://api/ws/validations/{id}
- validation.started
- validation.progress
- validation.completed
- validation.failed
```

## Security Considerations

### API Security
- JWT tokens with refresh rotation
- Rate limiting per user/IP
- Input validation and sanitization
- CORS configuration for frontend only

### Agent Security
- Sandboxed execution environment
- Token limits per request
- Output filtering for sensitive data
- Audit logging for all agent actions

## Scalability Plan

### Phase 1 (MVP): 0-100 users
- Single Cloud Run instance
- Shared agent workers
- Basic caching

### Phase 2: 100-1,000 users
- Multiple Cloud Run instances
- Dedicated agent worker pools
- Redis caching layer
- CDN for static assets

### Phase 3: 1,000+ users
- Kubernetes deployment
- Agent microservices
- Distributed vector store
- Multi-region deployment