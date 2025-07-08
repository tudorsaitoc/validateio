# ValidateIO Backend Operational Test

This operational test verifies that all components of the ValidateIO backend are working correctly.

## What it tests

1. **Database Connection** - Verifies PostgreSQL connectivity
2. **Table Creation** - Creates all required database tables
3. **User Creation** - Creates a test user account
4. **Validation Creation** - Creates a test validation record
5. **Agent Imports** - Verifies all AI agents can be imported
6. **Health Endpoints** - Tests API health check endpoints
7. **Validation Pipeline** - Tests the full validation workflow (if API keys are configured)

## Prerequisites

1. PostgreSQL database running and accessible
2. Python environment with dependencies installed:
   ```bash
   pip install -r requirements.txt
   ```

3. Environment variables configured in `.env` file:
   ```env
   # Database
   DATABASE_URL=postgresql+asyncpg://user:password@localhost/validateio
   
   # API Keys (at least one required for full pipeline test)
   OPENAI_API_KEY=your-openai-key
   ANTHROPIC_API_KEY=your-anthropic-key
   SERPER_API_KEY=your-serper-key  # Optional, for web search
   
   # Optional
   REDIS_URL=redis://localhost:6379/0
   ```

## Running the Test

1. **Run the operational test:**
   ```bash
   cd backend
   python test_operational.py
   ```

2. **Start the API server (in another terminal):**
   ```bash
   cd backend
   uvicorn main:app --reload
   ```

3. **Check health endpoints:**
   - Basic: http://localhost:8000/health
   - Detailed: http://localhost:8000/health/detailed

## Expected Output

The test will show colored output indicating:
- ✓ PASS (green) - Test passed
- ✗ FAIL (red) - Test failed
- ⚠ WARNING (yellow) - Non-critical issue

## Troubleshooting

### Database Connection Failed
- Ensure PostgreSQL is running
- Check DATABASE_URL in .env
- Verify database exists: `createdb validateio`

### Agent Import Failed
- Check that all dependencies are installed
- Verify Python version (3.9+ required)

### Validation Pipeline Failed
- Ensure at least one LLM API key is configured (OpenAI or Anthropic)
- Check API key validity
- Review agent-specific error messages

### Health Endpoint Failed
- Ensure the FastAPI server is running
- Check the port configuration (default: 8000)

## Next Steps

After successful operational test:
1. Set up Redis for Celery task queue
2. Configure ChromaDB for vector storage
3. Run the full test suite: `pytest`
4. Set up monitoring and logging
5. Deploy to production environment