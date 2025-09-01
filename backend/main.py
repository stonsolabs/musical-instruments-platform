"""
FastAPI app entry point for Azure App Service deployment
"""
from app.main import app

# This is the entry point for gunicorn/uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)