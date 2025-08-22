import azure.functions as func
import json
import os
from datetime import datetime
from ..utils.redis_client import redis_client
from ..utils.database import test_database_connection

def main(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    
    try:
        # Check database connection
        db_status = "healthy"
        db_message = "Database connection successful"
        try:
            test_database_connection()
        except Exception as e:
            db_status = "unhealthy"
            db_message = f"Database connection failed: {str(e)}"
        
        # Check Redis connection
        redis_status = "healthy"
        redis_message = "Redis connection successful"
        try:
            redis_client.ping()
        except Exception as e:
            redis_status = "unhealthy"
            redis_message = f"Redis connection failed: {str(e)}"
        
        # Overall health status
        overall_status = "healthy" if db_status == "healthy" and redis_status == "healthy" else "unhealthy"
        
        # Build response
        health_data = {
            "status": overall_status,
            "timestamp": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "environment": os.getenv("ENVIRONMENT", "production"),
            "services": {
                "database": {
                    "status": db_status,
                    "message": db_message
                },
                "redis": {
                    "status": redis_status,
                    "message": redis_message
                }
            }
        }
        
        # Return appropriate status code
        status_code = 200 if overall_status == "healthy" else 503
        
        return func.HttpResponse(
            json.dumps(health_data, indent=2),
            status_code=status_code,
            mimetype="application/json"
        )
        
    except Exception as e:
        error_response = {
            "status": "error",
            "timestamp": datetime.utcnow().isoformat(),
            "message": f"Health check failed: {str(e)}"
        }
        
        return func.HttpResponse(
            json.dumps(error_response, indent=2),
            status_code=500,
            mimetype="application/json"
        )
