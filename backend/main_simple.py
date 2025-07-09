"""Minimal FastAPI app for Cloud Run deployment"""
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="ValidateIO", version="0.1.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "ValidateIO API", "status": "running"}

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "validateio-api",
        "version": "0.1.0",
        "port": os.getenv("PORT", "8080")
    }

@app.get("/health/detailed")
async def health_detailed():
    return {
        "status": "healthy",
        "components": {
            "api": "healthy",
            "database": "not connected (minimal mode)",
            "supabase": "not connected (minimal mode)"
        }
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)