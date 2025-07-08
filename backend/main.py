import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import setup_logging

# Set up logging
setup_logging()
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up ValidateIO API...")
    # Initialize ChromaDB, Redis connections, etc.
    yield
    # Shutdown
    logger.info("Shutting down ValidateIO API...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Health check endpoint
@app.get("/health")
async def health_check():
    """Basic health check endpoint."""
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "validateio-api",
            "version": settings.VERSION,
        }
    )


# Detailed health check endpoint
@app.get("/health/detailed")
async def detailed_health_check():
    """Detailed health check with component status."""
    from app.db.session import AsyncSessionLocal
    from sqlalchemy import text
    
    health_status = {
        "status": "healthy",
        "service": "validateio-api",
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat(),
        "components": {}
    }
    
    # Check database
    try:
        async with AsyncSessionLocal() as session:
            await session.execute(text("SELECT 1"))
        health_status["components"]["database"] = {"status": "healthy"}
    except Exception as e:
        health_status["components"]["database"] = {"status": "unhealthy", "error": str(e)}
        health_status["status"] = "degraded"
    
    # Check Redis (if configured)
    if settings.REDIS_URL:
        try:
            import redis.asyncio as redis
            r = redis.from_url(settings.REDIS_URL)
            await r.ping()
            await r.close()
            health_status["components"]["redis"] = {"status": "healthy"}
        except Exception as e:
            health_status["components"]["redis"] = {"status": "unhealthy", "error": str(e)}
            health_status["status"] = "degraded"
    
    # Check API keys
    health_status["components"]["api_keys"] = {
        "openai": "configured" if settings.OPENAI_API_KEY else "missing",
        "anthropic": "configured" if settings.ANTHROPIC_API_KEY else "missing",
        "serper": "configured" if settings.SERPER_API_KEY else "missing",
    }
    
    # Feature flags
    health_status["features"] = {
        "market_research": settings.ENABLE_RESEARCH_AGENT,
        "experiments": settings.ENABLE_EXPERIMENT_AGENT,
        "marketing": settings.ENABLE_MARKETING_AGENT,
    }
    
    return JSONResponse(content=health_status)


# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.PORT,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )