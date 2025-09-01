import azure.functions as func
import logging
from fastapi_azure_functions import AzureApp
from app.main import app as fastapi_app

# Create Azure Functions app with FastAPI ASGI adapter
azure_app = AzureApp(fastapi_app, http_auth_level=func.AuthLevel.ANONYMOUS)

# Export the function app
app = azure_app.func_app