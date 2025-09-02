from __future__ import annotations

from fastapi import FastAPI, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
import logging
import time

from .config import settings
from .database import init_db
from .api import brands, categories, products, search, trending, compare, affiliate_stores, redirect
from .auth import verify_api_key, optional_api_key


# Disable docs in production for security
docs_url = "/docs" if settings.ENVIRONMENT != "production" else None
redoc_url = "/redoc" if settings.ENVIRONMENT != "production" else None
openapi_url = "/openapi.json" if settings.ENVIRONMENT != "production" else None

app = FastAPI(
    title=settings.PROJECT_NAME,
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    logger.info(f"Request: {request.method} {request.url}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"Response: {response.status_code} - {process_time:.3f}s")
    return response


@app.on_event("startup")
async def on_startup() -> None:
    await init_db()


# Health check endpoint (no API key required)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}


# API routes with authentication
app.include_router(products.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(categories.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(brands.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(search.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(trending.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(compare.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(affiliate_stores.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(redirect.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])


