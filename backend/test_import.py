#!/usr/bin/env python3
"""Test script to verify app imports work"""

try:
    print("Testing imports...")
    from app.main import app as fastapi_app
    print("✅ Successfully imported FastAPI app")
    
    import azure.functions as func
    print("✅ Azure Functions imported successfully")
    
    print("FastAPI app type:", type(fastapi_app))
    print("App attributes:", dir(fastapi_app))
    
except ImportError as e:
    print(f"❌ Import error: {e}")
except Exception as e:
    print(f"❌ Error: {e}")