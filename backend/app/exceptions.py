from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging
from typing import Any, Dict
import traceback
import uuid

from .config_secure import settings

logger = logging.getLogger(__name__)

class APIException(HTTPException):
    """Base API exception with enhanced error tracking"""
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
        headers: dict = None,
        internal_message: str = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code or f"API_{status_code}"
        self.internal_message = internal_message or detail
        self.error_id = str(uuid.uuid4())[:8]

class ProductNotFoundError(APIException):
    def __init__(self, product_id: Any):
        super().__init__(
            status_code=404,
            detail="Product not found",
            error_code="PRODUCT_NOT_FOUND",
            internal_message=f"Product {product_id} not found in database"
        )

class ValidationError(APIException):
    def __init__(self, field: str, message: str):
        super().__init__(
            status_code=400,
            detail=f"Validation error: {message}",
            error_code="VALIDATION_ERROR",
            internal_message=f"Field '{field}': {message}"
        )

class DatabaseError(APIException):
    def __init__(self, operation: str, internal_error: str = None):
        super().__init__(
            status_code=500,
            detail="Database operation failed",
            error_code="DATABASE_ERROR",
            internal_message=f"Database {operation} failed: {internal_error}"
        )

class ExternalServiceError(APIException):
    def __init__(self, service: str, operation: str):
        super().__init__(
            status_code=503,
            detail=f"{service} service unavailable",
            error_code="EXTERNAL_SERVICE_ERROR",
            internal_message=f"{service} {operation} failed"
        )

async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """Enhanced API exception handler with logging and error tracking"""
    
    # Log internal details (not sent to client)
    logger.error(
        f"API Error [{exc.error_id}]: {exc.error_code} - {exc.internal_message}",
        extra={
            "error_id": exc.error_id,
            "error_code": exc.error_code,
            "status_code": exc.status_code,
            "path": request.url.path,
            "method": request.method,
            "client_ip": request.client.host if request.client else "unknown"
        }
    )
    
    # Prepare response
    response_data = {
        "error": {
            "code": exc.error_code,
            "message": exc.detail,
            "error_id": exc.error_id
        }
    }
    
    # Add debug info only in development
    if settings.DEBUG_MODE:
        response_data["error"]["internal_message"] = exc.internal_message
    
    return JSONResponse(
        status_code=exc.status_code,
        content=response_data,
        headers=exc.headers
    )

async def http_exception_handler(request: Request, exc: StarletteHTTPException) -> JSONResponse:
    """Handle standard HTTP exceptions"""
    
    error_id = str(uuid.uuid4())[:8]
    
    # Log non-client errors
    if exc.status_code >= 500:
        logger.error(
            f"HTTP Error [{error_id}]: {exc.status_code} - {exc.detail}",
            extra={
                "error_id": error_id,
                "status_code": exc.status_code,
                "path": request.url.path,
                "method": request.method
            }
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": f"HTTP_{exc.status_code}",
                "message": exc.detail,
                "error_id": error_id
            }
        }
    )

async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    """Handle Pydantic validation errors"""
    
    error_id = str(uuid.uuid4())[:8]
    
    # Extract validation error details
    errors = []
    for error in exc.errors():
        field = " -> ".join(str(loc) for loc in error["loc"])
        errors.append({
            "field": field,
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        f"Validation Error [{error_id}]: {len(errors)} validation failures",
        extra={
            "error_id": error_id,
            "path": request.url.path,
            "method": request.method,
            "errors": errors
        }
    )
    
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

async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions"""
    
    error_id = str(uuid.uuid4())[:8]
    
    # Log full traceback for debugging
    logger.error(
        f"Unhandled Exception [{error_id}]: {type(exc).__name__} - {str(exc)}",
        extra={
            "error_id": error_id,
            "exception_type": type(exc).__name__,
            "path": request.url.path,
            "method": request.method,
            "traceback": traceback.format_exc() if settings.DEBUG_MODE else None
        }
    )
    
    # Never expose internal error details in production
    response_data = {
        "error": {
            "code": "INTERNAL_SERVER_ERROR",
            "message": "An unexpected error occurred",
            "error_id": error_id
        }
    }
    
    # Add debug info only in development
    if settings.DEBUG_MODE:
        response_data["error"]["debug"] = {
            "exception_type": type(exc).__name__,
            "exception_message": str(exc),
            "traceback": traceback.format_exc().split('\n')
        }
    
    return JSONResponse(
        status_code=500,
        content=response_data
    )