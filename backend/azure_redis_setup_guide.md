# Azure Cache for Redis Setup Guide

## Current Issue
Your Azure App Service `getyourmusicgear-api` cannot connect to Redis, causing autocomplete to fail.

## Required Environment Variables

You need to set these environment variables in your Azure App Service:

### Option 1: Using Redis Connection String (Recommended)
```bash
REDIS_URL=rediss://:YOUR_REDIS_ACCESS_KEY@getyourmusicgear-redis.redis.cache.windows.net:6380
```

### Option 2: Using Redis Password Separately
```bash
REDIS_PASSWORD=YOUR_REDIS_ACCESS_KEY
```

## How to Get Your Redis Access Key

1. Go to Azure Portal
2. Navigate to your Redis instance: `getyourmusicgear-redis`
3. Go to "Access keys" section
4. Copy the "Primary" access key

## How to Set Environment Variables in Azure App Service

1. Go to Azure Portal
2. Navigate to your App Service: `getyourmusicgear-api`
3. Go to "Configuration" > "Application settings"
4. Add new application setting:
   - Name: `REDIS_URL`
   - Value: `rediss://:YOUR_ACCESS_KEY@getyourmusicgear-redis.redis.cache.windows.net:6380`

## Important Notes

- Use `rediss://` (with 's') for SSL connection
- Port 6380 is the SSL port for Azure Cache for Redis
- Replace `YOUR_ACCESS_KEY` with the actual access key from Redis
- The format is: `rediss://:password@hostname:port`
- Note the `:` before the password (no username)

## Alternative: Azure AD Authentication

If you prefer managed identity, set:
```bash
REDIS_USE_AAD=true
```

But this requires configuring managed identity for your App Service.

## Test After Configuration

After setting the environment variable, restart your App Service and test:
- Health check: `https://getyourmusicgear-api.azurewebsites.net/health`
- Redis test: `https://getyourmusicgear-api.azurewebsites.net/test-redis`
- Autocomplete: `https://getyourmusicgear-api.azurewebsites.net/api/v1/search/autocomplete?q=guitar`
