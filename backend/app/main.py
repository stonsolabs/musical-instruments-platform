from __future__ import annotations

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from .config import settings
from .database import init_db
from .api import brands, categories, products, search, trending, compare, affiliate_stores, redirect
from .auth import verify_api_key, optional_api_key


app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)


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


