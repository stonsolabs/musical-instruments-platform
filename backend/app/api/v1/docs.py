"""
Protected API documentation endpoints
"""

from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi
import logging

from app.middleware.azure_auth import require_azure_admin

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/docs", tags=["docs"])

@router.get("/", response_class=HTMLResponse)
async def get_swagger_documentation(
    request: Request,
    admin: dict = Depends(require_azure_admin)
):
    """
    Protected Swagger UI documentation - admin access only
    """
    try:
        # Get the full app instance to generate OpenAPI spec
        app = request.app
        
        # Generate OpenAPI schema
        openapi_schema = get_openapi(
            title=app.title,
            version=getattr(app, 'version', '1.0.0'),
            description="GetYourMusicGear API - Protected Documentation",
            routes=app.routes,
        )
        
        # Return Swagger UI with the schema
        return get_swagger_ui_html(
            openapi_url="/api/v1/docs/openapi.json",
            title=f"{app.title} - Documentation",
            swagger_js_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui-bundle.js",
            swagger_css_url="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/swagger-ui.css",
            swagger_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        )
        
    except Exception as e:
        logger.error(f"Error generating Swagger documentation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate documentation")

@router.get("/redoc", response_class=HTMLResponse)
async def get_redoc_documentation(
    request: Request,
    admin: dict = Depends(require_azure_admin)
):
    """
    Protected ReDoc documentation - admin access only
    """
    try:
        # Get the full app instance
        app = request.app
        
        # Return ReDoc with the schema
        return get_redoc_html(
            openapi_url="/api/v1/docs/openapi.json",
            title=f"{app.title} - ReDoc",
            redoc_js_url="https://cdn.jsdelivr.net/npm/redoc@2.1.3/bundles/redoc.standalone.js",
            redoc_favicon_url="https://fastapi.tiangolo.com/img/favicon.png",
        )
        
    except Exception as e:
        logger.error(f"Error generating ReDoc documentation: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate documentation")

@router.get("/openapi.json")
async def get_protected_openapi(
    request: Request,
    admin: dict = Depends(require_azure_admin)
):
    """
    Protected OpenAPI schema - admin access only
    """
    try:
        app = request.app
        
        # Generate complete OpenAPI schema
        openapi_schema = get_openapi(
            title=app.title,
            version=getattr(app, 'version', '1.0.0'),
            description="""
## GetYourMusicGear API Documentation

This is the protected API documentation for the GetYourMusicGear platform.

### Authentication
- **API Key**: Required in the `X-API-Key` header for most endpoints
- **Azure AD**: Admin endpoints require Azure App Service Authentication

### Base URL
- **Production**: `https://getyourmusicgear-api.azurewebsites.net/api/v1`
- **Development**: `http://localhost:8000/api/v1`

### Key Features
- **Product Catalog**: Browse and search musical instruments
- **AI Blog Generation**: Automated content creation with product integration
- **Batch Processing**: Efficient bulk operations using Azure OpenAI Batch API
- **Admin Dashboard**: Complete administrative interface
- **Affiliate Integration**: Smart store selection with regional preferences

### Rate Limiting
- Standard endpoints: 1000 requests/hour
- Admin endpoints: 100 requests/hour
- Search endpoints: 500 requests/hour

### Response Format
All responses follow a consistent JSON structure with proper error handling and status codes.
            """.strip(),
            routes=app.routes,
            servers=[
                {
                    "url": "https://getyourmusicgear-api.azurewebsites.net/api/v1",
                    "description": "Production server"
                },
                {
                    "url": "http://localhost:8000/api/v1", 
                    "description": "Development server"
                }
            ]
        )
        
        # Add security schemes
        openapi_schema["components"]["securitySchemes"] = {
            "ApiKeyAuth": {
                "type": "apiKey",
                "in": "header",
                "name": "X-API-Key",
                "description": "API key for authentication"
            },
            "AzureAD": {
                "type": "oauth2",
                "description": "Azure App Service Authentication",
                "flows": {
                    "implicit": {
                        "authorizationUrl": "/.auth/login/aad",
                        "scopes": {}
                    }
                }
            }
        }
        
        # Add global security requirement
        openapi_schema["security"] = [{"ApiKeyAuth": []}]
        
        logger.info(f"Generated OpenAPI schema for admin {admin['email']}")
        return openapi_schema
        
    except Exception as e:
        logger.error(f"Error generating OpenAPI schema: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate OpenAPI schema")

@router.get("/health")
async def docs_health_check(admin: dict = Depends(require_azure_admin)):
    """
    Health check for docs service
    """
    return {
        "status": "healthy",
        "service": "Protected API Documentation",
        "admin_user": admin.get('email', 'unknown'),
        "features": [
            "Swagger UI",
            "ReDoc",
            "OpenAPI Schema",
            "Azure AD Protected"
        ]
    }