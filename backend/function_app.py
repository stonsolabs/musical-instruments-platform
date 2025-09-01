import azure.functions as func
import logging
from app.main import app as fastapi_app
import asyncio
from typing import Dict, Any

# Create the Azure Functions app
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

async def fastapi_to_azure_func(req: func.HttpRequest) -> func.HttpResponse:
    """Convert Azure Function request to FastAPI ASGI and back"""
    try:
        # Build ASGI scope
        method = req.method
        path = req.url.split('?')[0].split('://', 1)[1].split('/', 1)[1] if '://' in req.url else req.url
        if not path.startswith('/'):
            path = '/' + path
            
        query_string = req.url.split('?', 1)[1] if '?' in req.url else ''
        
        scope = {
            'type': 'http',
            'method': method,
            'path': path,
            'query_string': query_string.encode(),
            'headers': [(k.lower().encode(), v.encode()) for k, v in req.headers.items()],
            'server': ('localhost', 80),
        }

        # Get request body
        body = req.get_body()
        
        # Variables to capture response
        response_started = False
        status_code = 200
        headers = []
        response_body = b""

        async def receive():
            return {
                'type': 'http.request',
                'body': body,
                'more_body': False,
            }

        async def send(message):
            nonlocal response_started, status_code, headers, response_body
            
            if message['type'] == 'http.response.start':
                response_started = True
                status_code = message['status']
                headers = message['headers']
            elif message['type'] == 'http.response.body':
                response_body += message.get('body', b'')

        # Call FastAPI app
        await fastapi_app(scope, receive, send)
        
        # Convert headers to dict
        headers_dict = {}
        for header_name, header_value in headers:
            headers_dict[header_name.decode()] = header_value.decode()
        
        return func.HttpResponse(
            response_body,
            status_code=status_code,
            headers=headers_dict,
            mimetype=headers_dict.get('content-type', 'application/json')
        )
    except Exception as e:
        logging.error(f"Error in ASGI adapter: {str(e)}")
        return func.HttpResponse(
            f'{{"error": "Internal server error", "details": "{str(e)}"}}',
            status_code=500,
            mimetype="application/json"
        )

@app.route(route="{*route}", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def main(req: func.HttpRequest) -> func.HttpResponse:
    """Main function to handle all routes via FastAPI"""
    return await fastapi_to_azure_func(req)