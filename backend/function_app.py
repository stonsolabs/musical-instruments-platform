import azure.functions as func
import logging
from app.main import app as fastapi_app
from fastapi import HTTPException

# Create the Azure Functions app
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="health", auth_level=func.AuthLevel.ANONYMOUS)
async def health(req: func.HttpRequest) -> func.HttpResponse:
    """Health check endpoint"""
    return func.HttpResponse(
        '{"status": "healthy", "service": "Musical Instruments Platform"}',
        status_code=200,
        mimetype="application/json"
    )

@app.route(route="api/{*route}", auth_level=func.AuthLevel.ANONYMOUS)
async def main(req: func.HttpRequest) -> func.HttpResponse:
    """Main function to handle all API routes"""
    
    try:
        from app.main import app as fastapi_app
        import json
        from starlette.requests import Request
        from starlette.responses import Response
        import asyncio
        
        # Convert Azure Functions request to ASGI request
        scope = {
            "type": "http",
            "method": req.method,
            "path": f"/{req.route_params.get('route', '')}",
            "query_string": req.url.encode().split(b'?', 1)[1] if b'?' in req.url.encode() else b'',
            "headers": [(k.lower().encode(), v.encode()) for k, v in req.headers.items()],
            "server": ("localhost", 80),
        }
        
        # Handle request body
        body = req.get_body()
        
        # Create ASGI application instance
        response_started = False
        status_code = 200
        headers = []
        response_body = b""
        
        async def receive():
            return {
                "type": "http.request",
                "body": body,
                "more_body": False,
            }
        
        async def send(message):
            nonlocal response_started, status_code, headers, response_body
            
            if message["type"] == "http.response.start":
                response_started = True
                status_code = message["status"]
                headers = message["headers"]
            elif message["type"] == "http.response.body":
                response_body += message.get("body", b"")
        
        # Call the FastAPI application
        await fastapi_app(scope, receive, send)
        
        # Convert headers back to dict
        response_headers = {}
        for header_name, header_value in headers:
            response_headers[header_name.decode()] = header_value.decode()
        
        return func.HttpResponse(
            response_body,
            status_code=status_code,
            headers=response_headers,
            mimetype=response_headers.get("content-type", "application/json")
        )
        
    except Exception as e:
        logging.error(f"Error handling request: {str(e)}")
        return func.HttpResponse(
            f'{{"error": "Internal server error", "details": "{str(e)}"}}',
            status_code=500,
            mimetype="application/json"
        )