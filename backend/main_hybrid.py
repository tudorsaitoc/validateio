"""Hybrid main file that gracefully handles missing dependencies"""
import os
import sys
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# Create app
app = FastAPI(
    title="ValidateIO",
    version="0.1.0",
    description="AI-powered startup validation platform"
)

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track what features are available
FEATURES = {
    "database": False,
    "ai_agents": False,
    "supabase": False,
    "full_api": False
}

# Try to import full API
try:
    # First check if we can import config
    from app.core.config import settings
    print(f"✅ Config loaded - Environment: {settings.ENVIRONMENT}")
    FEATURES["config"] = True
    
    # Check database
    try:
        from app.db.session import AsyncSessionLocal, engine
        FEATURES["database"] = True
        print("✅ Database modules loaded")
    except Exception as e:
        print(f"⚠️  Database import failed: {e}")
    
    # Check Supabase
    if settings.SUPABASE_URL:
        FEATURES["supabase"] = True
        print("✅ Supabase configured")
    
    # Try full API import
    from app.api.v1.api import api_router
    app.include_router(api_router, prefix="/api/v1")
    FEATURES["full_api"] = True
    print("✅ Full API loaded")
    
except Exception as e:
    print(f"⚠️  Could not load full API: {e}")
    print(f"Error type: {type(e).__name__}")
    import traceback
    traceback.print_exc()
    print("Running in limited mode")

# Basic endpoints that always work
@app.get("/")
async def root():
    return {
        "message": "ValidateIO API",
        "version": "0.1.0",
        "features": FEATURES,
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "validateio-api",
        "version": "0.1.0",
        "mode": "full" if FEATURES["full_api"] else "limited"
    }

@app.get("/health/detailed")
async def health_detailed():
    components = {
        "api": "healthy",
        "features": FEATURES
    }
    
    # Check database if available
    if FEATURES["database"]:
        try:
            from app.db.session import AsyncSessionLocal
            components["database"] = "connected"
        except:
            components["database"] = "not available"
    else:
        components["database"] = "not configured"
    
    # Check Supabase
    if FEATURES["supabase"]:
        try:
            from app.core.config import settings
            if settings.SUPABASE_URL:
                components["supabase"] = "configured"
            else:
                components["supabase"] = "not configured"
        except:
            components["supabase"] = "error"
    else:
        components["supabase"] = "not available"
    
    return {
        "status": "healthy",
        "components": components,
        "mode": "full" if FEATURES["full_api"] else "limited"
    }

# Limited mode endpoints (when full API not available)
if not FEATURES["full_api"]:
    @app.post("/api/v1/validations")
    async def create_validation_limited(data: dict):
        return {
            "error": "API running in limited mode",
            "message": "Full validation features not available",
            "received_data": data
        }
    
    @app.get("/api/v1/validations")
    async def list_validations_limited():
        return {
            "error": "API running in limited mode",
            "validations": [],
            "message": "Database not connected"
        }

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={
            "detail": str(exc),
            "type": type(exc).__name__,
            "mode": "full" if FEATURES["full_api"] else "limited"
        }
    )

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)