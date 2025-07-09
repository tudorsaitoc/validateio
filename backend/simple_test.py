from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "ValidateIO Simple Test"}

@app.get("/health")
async def health():
    return JSONResponse(
        content={
            "status": "healthy",
            "service": "validateio-simple-test"
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)