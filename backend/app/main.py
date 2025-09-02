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

# Redis connection test endpoint
@app.get("/test-redis")
async def test_redis():
    """Test Redis connection for debugging"""
    import redis.asyncio as redis
    from azure.identity.aio import DefaultAzureCredential
    import json
    
    results = []
    redis_url = settings.REDIS_URL
    
    # Test 1: Current Redis URL
    results.append(f"🔍 Testing current REDIS_URL: {redis_url}")
    try:
        client = redis.from_url(redis_url, decode_responses=True)
        await client.ping()
        await client.set("test_key", "test_value", ex=30)
        value = await client.get("test_key")
        await client.delete("test_key")
        await client.close()
        results.append("✅ Current Redis URL works!")
        return {"status": "success", "method": "current_url", "results": results}
    except Exception as e:
        results.append(f"❌ Current URL failed: {type(e).__name__}: {e}")
        try:
            await client.close()
        except:
            pass
    
    # Test 2: Try with access key from environment
    results.append("\n🧪 Testing with access key from environment...")
    redis_password = os.getenv("REDIS_PASSWORD")
    if not redis_password:
        results.append("❌ REDIS_PASSWORD environment variable not set")
        return jsonify({"error": "Redis password not configured", "details": results})
    
    try:
        client = redis.Redis(
            host="getyourmusicgear-redis.redis.cache.windows.net",
            port=6380,
            password=redis_password,
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True
        )
        await client.ping()
        results.append("✅ Access key authentication works!")
        await client.close()
        return {"status": "success", "method": "access_key", "results": results}
    except Exception as e:
        results.append(f"❌ Access key failed: {type(e).__name__}: {e}")
        try:
            await client.close()
        except:
            pass
    
    # Test 3: Try Azure AD authentication
    results.append("\n🔐 Testing Azure AD authentication...")
    try:
        # This requires the app to have managed identity access to Redis
        credential = DefaultAzureCredential()
        token = await credential.get_token("https://redis.azure.com/.default")
        
        client = redis.Redis(
            host="getyourmusicgear-redis.redis.cache.windows.net",
            port=6380,
            password=token.token,
            ssl=True,
            ssl_cert_reqs=None,
            decode_responses=True
        )
        await client.ping()
        results.append("✅ Azure AD authentication works!")
        await client.close()
        return {"status": "success", "method": "azure_ad", "results": results}
    except Exception as e:
        results.append(f"❌ Azure AD failed: {type(e).__name__}: {e}")
        try:
            await client.close()
        except:
            pass
    
    return {"status": "all_failed", "results": results}

# API routes with authentication
app.include_router(products.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(categories.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(brands.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(search.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(trending.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(compare.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(affiliate_stores.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])
app.include_router(redirect.router, prefix=settings.API_V1_STR, dependencies=[Depends(verify_api_key)])


