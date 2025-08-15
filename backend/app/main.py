from __future__ import annotations

import asyncio
import os
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.exceptions import HTTPException

from .config import settings
from .database import init_db
from .api import brands, categories, compare, products, redirect, search


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


# API routes
app.include_router(products.router, prefix=settings.API_V1_STR)
app.include_router(categories.router, prefix=settings.API_V1_STR)
app.include_router(brands.router, prefix=settings.API_V1_STR)
app.include_router(compare.router, prefix=settings.API_V1_STR)
app.include_router(redirect.router, prefix=settings.API_V1_STR)
app.include_router(search.router, prefix=settings.API_V1_STR)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.PROJECT_NAME}

# Static file serving for frontend (if available)
static_dir = Path(__file__).parent.parent / "static"
if static_dir.exists():
    app.mount("/_next", StaticFiles(directory=static_dir / ".next"), name="nextjs_static")
    app.mount("/static", StaticFiles(directory=static_dir / "public"), name="public_static")

# Catch-all route for frontend SPA
@app.get("/")
async def root():
    static_index = static_dir / ".next" / "server" / "app" / "page.html"
    if static_index.exists():
        return FileResponse(static_index)
    return {"status": "ok", "name": settings.PROJECT_NAME, "mode": "api_only"}

@app.get("/{path:path}")
async def catch_all(path: str):
    # Try to serve static file first
    static_file = static_dir / "public" / path
    if static_file.exists() and static_file.is_file():
        return FileResponse(static_file)
    
    # For SPA routing, return index.html
    static_index = static_dir / ".next" / "server" / "app" / "page.html"
    if static_index.exists():
        return FileResponse(static_index)
    
    # API-only mode
    raise HTTPException(status_code=404, detail="Page not found")


