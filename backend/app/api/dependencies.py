"""
API dependencies for authentication and authorization
"""

from fastapi import HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
import os
import logging

logger = logging.getLogger(__name__)

security = HTTPBearer(auto_error=False)

# Admin configuration
ADMIN_API_KEY = os.getenv('ADMIN_API_KEY', 'your-super-secret-admin-key')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@getyourmusicgear.com')

async def get_api_key(request: Request) -> str:
    """
    Get API key from headers for general API access
    """
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    # In production, validate against database or secure store
    expected_api_key = os.getenv('API_KEY')
    if not expected_api_key:
        raise HTTPException(status_code=500, detail="API key not configured")
    
    if api_key != expected_api_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    
    return api_key

async def get_admin_key(request: Request) -> str:
    """
    Get admin API key for admin-only operations
    """
    # Check for admin API key in headers
    admin_key = request.headers.get('X-Admin-Key')
    if not admin_key:
        raise HTTPException(
            status_code=401, 
            detail="Admin access required. Please provide X-Admin-Key header."
        )
    
    if admin_key != ADMIN_API_KEY:
        raise HTTPException(status_code=403, detail="Invalid admin credentials")
    
    logger.info(f"Admin access granted from IP: {request.client.host}")
    return admin_key

async def get_optional_admin_key(request: Request) -> Optional[str]:
    """
    Optional admin key check - returns None if not admin
    """
    admin_key = request.headers.get('X-Admin-Key')
    if admin_key and admin_key == ADMIN_API_KEY:
        return admin_key
    return None

class AdminRequired:
    """
    Dependency class for admin-only endpoints
    """
    def __init__(self, require_admin: bool = True):
        self.require_admin = require_admin
    
    async def __call__(self, request: Request) -> dict:
        if self.require_admin:
            admin_key = await get_admin_key(request)
            return {
                "is_admin": True,
                "admin_key": admin_key,
                "ip_address": request.client.host
            }
        else:
            admin_key = await get_optional_admin_key(request)
            return {
                "is_admin": bool(admin_key),
                "admin_key": admin_key,
                "ip_address": request.client.host
            }

# Common dependency instances
require_admin = AdminRequired(require_admin=True)
optional_admin = AdminRequired(require_admin=False)