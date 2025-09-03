from fastapi import HTTPException, Depends, Header, Request
from typing import Optional
import logging
import time
from collections import defaultdict
from .config import settings

logger = logging.getLogger(__name__)

# Simple rate limiting (use Redis in production for scaling)
rate_limit_store = defaultdict(list)

def get_client_ip(request: Request) -> str:
    """Extract client IP with proper proxy header handling"""
    # Check forwarded headers first (App Service / proxy)
    forwarded_for = request.headers.get("X-Forwarded-For")
    if forwarded_for:
        return forwarded_for.split(",")[0].strip()
    
    real_ip = request.headers.get("X-Real-IP")
    if real_ip:
        return real_ip
    
    # Fallback to direct connection
    if hasattr(request.client, 'host') and request.client.host:
        return request.client.host
    
    return "unknown"

def is_rate_limited(client_ip: str, limit: int = 100, period: int = 60) -> bool:
    """Simple rate limiting - 100 requests per minute per IP"""
    current_time = time.time()
    requests = rate_limit_store[client_ip]
    
    # Remove old requests outside the time window
    rate_limit_store[client_ip] = [
        req_time for req_time in requests 
        if current_time - req_time < period
    ]
    
    # Check if limit exceeded
    if len(rate_limit_store[client_ip]) >= limit:
        return True
    
    # Add current request
    rate_limit_store[client_ip].append(current_time)
    return False

async def verify_api_key(
    request: Request,
    x_api_key: Optional[str] = Header(None, alias="X-API-Key")
):
    """
    Secure API key verification with rate limiting and logging.
    Compatible with App Service deployment.
    """
    client_ip = get_client_ip(request)
    
    # Rate limiting protection
    if is_rate_limited(client_ip):
        logger.warning(f"Rate limit exceeded for IP: {client_ip}")
        raise HTTPException(
            status_code=429,
            detail="Too many requests. Please try again later.",
            headers={"Retry-After": "60"}
        )
    
    # Development mode - require API key but allow easier setup
    if settings.ENVIRONMENT == "development":
        if not settings.API_KEY:
            logger.warning("Development mode with no API key - this is insecure for production!")
            return "dev-bypass"  # Allow for local development setup
    
    # Production mode - strict validation required
    if not x_api_key:
        logger.warning(f"Missing API key from {client_ip} on {request.url.path}")
        raise HTTPException(
            status_code=401, 
            detail="API key required in X-API-Key header",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    if not settings.API_KEY:
        logger.error("API_KEY not configured - check environment variables")
        raise HTTPException(
            status_code=500, 
            detail="Server configuration error"
        )
    
    # Secure comparison (prevent timing attacks)
    if not secure_compare(x_api_key, settings.API_KEY):
        logger.warning(f"Invalid API key attempt from {client_ip} on {request.url.path}")
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    # Log successful authentication (but not the key)
    logger.info(f"Authenticated request from {client_ip} to {request.url.path}")
    return x_api_key

def secure_compare(a: str, b: str) -> bool:
    """Constant-time string comparison to prevent timing attacks"""
    if len(a) != len(b):
        return False
    
    result = 0
    for x, y in zip(a, b):
        result |= ord(x) ^ ord(y)
    
    return result == 0

# Optional dependency for routes that don't require API key
async def optional_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Optional API key verification - doesn't fail if key is missing.
    Useful for health checks and public endpoints.
    """
    if not x_api_key or not settings.API_KEY:
        return None
    
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    return x_api_key
