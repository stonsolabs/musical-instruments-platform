#!/usr/bin/env python3.11
"""
Configuration loader for image management scripts.
Loads settings from both main .env and crawler/.env files.
"""

import os
from pathlib import Path
from typing import Optional

def load_env_file(file_path: str) -> dict:
    """Load environment variables from a .env file."""
    env_vars = {}
    
    if not os.path.exists(file_path):
        return env_vars
    
    try:
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    env_vars[key.strip()] = value.strip()
    except Exception as e:
        print(f"Warning: Could not load {file_path}: {e}")
    
    return env_vars

def get_config() -> dict:
    """Get configuration from environment variables and .env files."""
    
    # Get workspace root
    workspace_root = Path(__file__).parent.parent.parent.parent
    
    # Load main .env
    main_env = load_env_file(workspace_root / '.env')
    
    # Load crawler .env
    crawler_env = load_env_file(workspace_root / 'crawler' / '.env')
    
    # Merge configurations (crawler .env takes precedence)
    config = {}
    config.update(main_env)
    config.update(crawler_env)
    
    # Add environment variables (take highest precedence)
    for key, value in os.environ.items():
        config[key] = value
    
    return config

# Configuration constants
config = get_config()

# Database
DATABASE_URL = config.get('DATABASE_URL')

# Proxy settings
PROXY_URL = config.get('IPROYAL_PROXY_URL')
PROXY_USERNAME = None
PROXY_PASSWORD = None

# Parse proxy URL for username/password if present
if PROXY_URL and '@' in PROXY_URL:
    try:
        # Format: http://username:password@host:port
        auth_part = PROXY_URL.split('@')[0].replace('http://', '').replace('https://', '')
        if ':' in auth_part:
            PROXY_USERNAME, PROXY_PASSWORD = auth_part.split(':', 1)
    except:
        pass

# Azure Storage
AZURE_STORAGE_CONNECTION_STRING = config.get('AZURE_STORAGE_CONNECTION_STRING')
AZURE_STORAGE_ACCOUNT = 'getyourmusicgear'  # From connection string
AZURE_STORAGE_CONTAINER = config.get('AZURE_BLOB_CONTAINER', 'product-images')

# Redis
REDIS_URL = config.get('REDIS_URL', 'redis://localhost:6379')

# Other settings
SECRET_KEY = config.get('SECRET_KEY')
DEBUG = config.get('DEBUG', 'false').lower() == 'true'
ENVIRONMENT = config.get('ENVIRONMENT', 'production')

def print_config():
    """Print current configuration (without sensitive data)."""
    print("🔧 Current Configuration:")
    print("=========================")
    print(f"Database: {'✅ Set' if DATABASE_URL else '❌ Not set'}")
    print(f"Proxy: {'✅ Set' if PROXY_URL else '❌ Not set'}")
    print(f"Azure Storage: {'✅ Set' if AZURE_STORAGE_CONNECTION_STRING else '❌ Not set'}")
    print(f"Storage Account: {AZURE_STORAGE_ACCOUNT}")
    print(f"Storage Container: {AZURE_STORAGE_CONTAINER}")
    print(f"Redis: {'✅ Set' if REDIS_URL else '❌ Not set'}")
    print(f"Environment: {ENVIRONMENT}")
    print(f"Debug: {DEBUG}")
    
    if PROXY_URL:
        # Mask sensitive parts
        masked_proxy = PROXY_URL
        if '@' in PROXY_URL:
            parts = PROXY_URL.split('@')
            if ':' in parts[0]:
                auth_parts = parts[0].split(':')
                if len(auth_parts) >= 3:  # http://user:pass@host
                    masked_proxy = f"{auth_parts[0]}:***:***@{parts[1]}"
                else:  # http://user:pass@host
                    masked_proxy = f"{auth_parts[0]}:***@{parts[1]}"
        print(f"Proxy URL: {masked_proxy}")

if __name__ == "__main__":
    print_config()
