import azure.functions as func
import logging
from app.main import app as fastapi_app

# Create the Azure Functions app
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)

@app.route(route="{*route}", auth_level=func.AuthLevel.ANONYMOUS, methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"])
async def main(req: func.HttpRequest) -> func.HttpResponse:
    """Main function to handle all routes via FastAPI ASGI"""
    try:
        # Extract path from route params
        route = req.route_params.get('route', '')
        path = f"/{route}" if route else "/"
        
        # Build ASGI scope
        scope = {
            'type': 'http',
            'method': req.method,
            'path': path,
            'query_string': req.url.encode().split(b'?', 1)[1] if b'?' in req.url.encode() else b'',
            'headers': [(k.lower().encode(), v.encode()) for k, v in req.headers.items()],
            'server': ('localhost', 80),
        }

        # Get request body
        body = req.get_body()
        
        # Response capture
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
            nonlocal status_code, headers, response_body
            
            if message['type'] == 'http.response.start':
                status_code = message['status']
                headers = message['headers']
            elif message['type'] == 'http.response.body':
                response_body += message.get('body', b'')

        # Call FastAPI app
        await fastapi_app(scope, receive, send)
        
        # Convert headers
        headers_dict = {h[0].decode(): h[1].decode() for h in headers}
        
        return func.HttpResponse(
            response_body,
            status_code=status_code,
            headers=headers_dict,
            mimetype=headers_dict.get('content-type', 'application/json')
        )
        
    except Exception as e:
        logging.error(f"Error in FastAPI handler: {str(e)}")
        return func.HttpResponse(
            f'{{"error": "Internal server error", "details": "{str(e)}"}}',
            status_code=500,
            mimetype="application/json"
        )