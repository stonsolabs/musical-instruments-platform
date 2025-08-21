from fastapi import HTTPException, Depends, Header
from typing import Optional
from .config import settings

async def verify_api_key(x_api_key: Optional[str] = Header(None)):
    """
    Verify API key from request header.
    Returns 401 if API key is missing or invalid.
    """
    # Skip API key verification in development if no API key is set
    if settings.ENVIRONMENT == "development" and not settings.API_KEY:
        return None
    
    # Check if API key is provided and valid
    if not x_api_key:
        raise HTTPException(
            status_code=401, 
            detail="API key required",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    if x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=401, 
            detail="Invalid API key",
            headers={"WWW-Authenticate": "ApiKey"}
        )
    
    return x_api_key

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
