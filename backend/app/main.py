from __future__ import annotations

from fastapi import FastAPI, Depends, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.middleware.base import BaseHTTPMiddleware
import logging
import time
import uuid

from .config import settings
from .database import init_db
from .api import brands, categories, products, search, trending, compare, affiliate_stores, redirect, voting
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
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        
        # Add HSTS in production
        if settings.ENVIRONMENT == "production":
            response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        
        return response

# Add security headers
app.add_middleware(SecurityHeadersMiddleware)

# CORS configuration
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
    request_id = str(uuid.uuid4())[:8]
    
    logger.info(f"[{request_id}] {request.method} {request.url.path} - Start")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"[{request_id}] {response.status_code} - {process_time:.3f}s")
    
    # Add request ID to response headers for debugging
    response.headers["X-Request-ID"] = request_id
    return response

# Error handling
@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    error_id = str(uuid.uuid4())[:8]
    
    # Log server errors (5xx) but not client errors (4xx)
    if exc.status_code >= 500:
        logger.error(f"[{error_id}] HTTP {exc.status_code}: {exc.detail}")
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "error_id": error_id
            }
        },
        headers=getattr(exc, 'headers', None)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_id = str(uuid.uuid4())[:8]
    
    # Format validation errors for better readability
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(f"[{error_id}] Validation error: {len(errors)} fields failed")
    
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Request validation failed",
                "error_id": error_id,
                "details": errors
            }
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    error_id = str(uuid.uuid4())[:8]
    
    logger.error(f"[{error_id}] Unhandled exception: {type(exc).__name__} - {str(exc)}")
    
    # Never expose internal error details in production
    response_content = {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "error_id": error_id
        }
    }
    
    # Add debug info only in development
    if settings.ENVIRONMENT == "development":
        response_content["error"]["debug"] = {
            "exception_type": type(exc).__name__,
            "exception_message": str(exc)
        }
    
    return JSONResponse(
        status_code=500,
        content=response_content
    )


@app.on_event("startup")
async def on_startup() -> None:
    try:
        await init_db()
        logger.info("Database initialized successfully")
    except Exception as e:
        if settings.ENVIRONMENT == "development":
            logger.warning(f"Database initialization failed (continuing in development mode): {e}")
        else:
            logger.error(f"Database initialization failed: {e}")
            raise


# Health check endpoint (no API key required)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}


# API routes with authentication (optional in development)
if settings.ENVIRONMENT == "development":
    # In development, include routes without strict authentication
    app.include_router(products.router, prefix=settings.API_V1_STR)
    app.include_router(categories.router, prefix=settings.API_V1_STR)
    app.include_router(brands.router, prefix=settings.API_V1_STR)
    app.include_router(search.router, prefix=settings.API_V1_STR)
    app.include_router(trending.router, prefix=settings.API_V1_STR)
    app.include_router(compare.router, prefix=settings.API_V1_STR)
    app.include_router(affiliate_stores.router, prefix=settings.API_V1_STR)
    app.include_router(redirect.router, prefix=settings.API_V1_STR)
    app.include_router(voting.router, prefix=settings.API_V1_STR)
else:
    # In production, require API key authentication
    app.include_router(products.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
    app.include_router(categories.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
    app.include_router(brands.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
    app.include_router(search.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
    app.include_router(trending.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
    app.include_router(compare.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
    app.include_router(affiliate_stores.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
    app.include_router(redirect.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
    app.include_router(voting.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])


