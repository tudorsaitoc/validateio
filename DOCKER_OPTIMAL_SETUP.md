# ValidateIO - Docker Optimal Setup 🐳

## Current Status

Your Docker services are running perfectly:
- ✅ PostgreSQL (localhost:5432)
- ✅ Redis (localhost:6379)  
- ✅ ChromaDB (localhost:8001)

The setup script is currently installing Python dependencies. This takes a few minutes due to packages like numpy and other AI libraries.

## While Dependencies Install...

### 1. Add Your OpenAI API Key

```bash
# Edit the backend .env file
nano backend/.env

# Add this line:
OPENAI_API_KEY=sk-your-actual-key-here
```

### 2. Check Installation Progress

In a new terminal:
```bash
# Watch the processes
ps aux | grep -E "pip|python"

# Check Docker services
docker-compose ps
```

### 3. Manual Quick Test (Skip the installation)

If you want to test immediately while dependencies install:

```bash
# New terminal
cd backend
python3 -m venv .venv_test
source .venv_test/bin/activate
pip install -r requirements-minimal.txt

# Add your API key to .env
echo "OPENAI_API_KEY=sk-your-key" >> .env

# Test the pipeline
python test_validation_pipeline.py
```

## Once Installation Completes

The script will automatically:
1. ✅ Run database migrations
2. ✅ Start the backend API (http://localhost:8000)
3. ✅ Start the Celery worker
4. ✅ Start the frontend (http://localhost:3000)

## Quick Commands

### Test the API
```bash
curl http://localhost:8000/health/detailed
```

### Test AI Pipeline
```bash
cd backend
source .venv/bin/activate
python test_validation_pipeline.py
```

### Create a Validation
```bash
curl -X POST http://localhost:8000/api/v1/validations/ \
  -H "Content-Type: application/json" \
  -d '{
    "business_idea": "AI-powered personal finance app for millennials",
    "target_market": "Tech-savvy millennials aged 25-35",
    "industry": "FinTech"
  }'
```

## Architecture

```
Your Machine                 Docker Containers
├── Backend (Port 8000)  ←→  ├── PostgreSQL (5432)
├── Frontend (Port 3000)     ├── Redis (6379)
└── Celery Worker       ←→   └── ChromaDB (8001)
```

## Troubleshooting

### If installation is taking too long:
1. Cancel with Ctrl+C
2. Use the minimal requirements:
   ```bash
   cd backend
   pip install -r requirements-minimal.txt
   ```

### If ports are already in use:
```bash
# Find and kill processes
lsof -ti:8000 | xargs kill -9
lsof -ti:3000 | xargs kill -9
```

### To restart everything:
```bash
docker-compose down
docker-compose up -d postgres redis chromadb
./scripts/dev_docker_optimal.sh
```

## What's Next?

1. **Wait for installation** - Should complete in 2-5 minutes
2. **Add your API key** - Required for AI agents
3. **Test the pipeline** - Verify everything works
4. **Start building!** - The system is ready for development

---

The optimal Docker setup gives you:
- 🚀 Fast local development (no Docker overhead for apps)
- 🐳 Reliable databases (PostgreSQL, Redis in Docker)
- 🔧 Easy debugging (apps run natively)
- 📦 Consistent environment (same for all developers)