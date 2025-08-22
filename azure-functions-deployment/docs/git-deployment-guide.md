# 🚀 Git-Based Deployment Guide - Azure Functions

## 📋 Overview

This guide shows you how to deploy Azure Functions using Git integration, which is the **recommended approach** over Docker for Azure Functions.

## 🎯 Why Git + Folder (Not Docker)?

### ✅ **Advantages of Git Deployment:**
- **Native Support** - Azure Functions designed for folder deployment
- **Better Performance** - No Docker overhead, faster cold starts
- **Easier Debugging** - Direct access to logs and monitoring
- **Cost Effective** - No container registry costs
- **Git Integration** - Perfect for your workflow
- **Automatic Scaling** - Better integration with Azure's scaling

### ❌ **Why Docker is Not Ideal:**
- Azure Functions already runs in containers (managed by Azure)
- Extra complexity without benefits
- Slower cold starts
- More expensive (container registry)
- Harder to debug

## 🏗️ Project Structure

```
azure-functions-deployment/
├── functions/
│   ├── function.json          # Function binding configuration
│   ├── host.json              # Host configuration
│   ├── requirements.txt       # Python dependencies
│   ├── api/
│   │   ├── __init__.py        # Main routing function
│   │   ├── health.py          # Health check endpoint
│   │   ├── products.py        # Products endpoints
│   │   ├── search.py          # Search endpoints
│   │   └── compare.py         # Compare endpoints
│   └── utils/
│       ├── redis_client.py    # Redis utilities
│       └── database.py        # Database utilities
├── scripts/
│   └── deploy-functions.sh    # Manual deployment script
└── .github/
    └── workflows/
        └── azure-functions-deploy.yml  # GitHub Actions
```

## 🚀 Deployment Options

### Option 1: GitHub Actions (Recommended)

1. **Get Publish Profile:**
```bash
# Get the publish profile
az functionapp deployment list-publishing-credentials \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api
```

2. **Add Secret to GitHub:**
   - Go to your GitHub repo → Settings → Secrets and variables → Actions
   - Add secret: `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`
   - Paste the publish profile content

3. **Push to Deploy:**
```bash
git add .
git commit -m "Update Azure Functions"
git push origin main
# GitHub Actions automatically deploys!
```

### Option 2: Manual Deployment

```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Deploy manually
cd azure-functions-deployment/functions
func azure functionapp publish musical-instruments-api
```

### Option 3: Using Script

```bash
# Make script executable
chmod +x azure-functions-deployment/scripts/deploy-functions.sh

# Run deployment script
./azure-functions-deployment/scripts/deploy-functions.sh
```

## 🔧 Local Development

### 1. Install Dependencies
```bash
# Install Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Install Python dependencies
cd azure-functions-deployment/functions
pip install -r requirements.txt
```

### 2. Configure Local Settings
Create `azure-functions-deployment/functions/local.settings.json`:
```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "DATABASE_URL": "postgresql+asyncpg://postgres:password@localhost:5432/musical_instruments",
    "REDIS_CONNECTION_STRING": "redis://localhost:6379",
    "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=https://devstoreaccount1.blob.core.windows.net/;QueueEndpoint=https://devstoreaccount1.queue.core.windows.net/;TableEndpoint=https://devstoreaccount1.table.core.windows.net/;",
    "AZURE_STORAGE_ACCOUNT_NAME": "devstoreaccount1",
    "AZURE_STORAGE_CONTAINER_NAME": "product-images",
    "ENVIRONMENT": "development",
    "SECRET_KEY": "dev-secret-key",
    "OPENAI_API_KEY": "your-openai-api-key",
    "AMAZON_ASSOCIATE_TAG": "your-amazon-tag",
    "THOMANN_AFFILIATE_ID": "your-thomann-id"
  }
}
```

### 3. Run Locally
```bash
# Start Functions locally
cd azure-functions-deployment/functions
func start

# Test endpoints
curl http://localhost:7071/api/health
curl http://localhost:7071/api/products
```

## 📊 Monitoring and Logs

### View Logs
```bash
# Real-time logs
az webapp log tail \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api

# Download logs
az webapp log download \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api
```

### Health Checks
```bash
# Test health endpoint
curl https://musical-instruments-api.azurewebsites.net/api/health

# Test specific endpoints
curl https://musical-instruments-api.azurewebsites.net/api/products
curl https://musical-instruments-api.azurewebsites.net/api/search?q=guitar
```

## 🔄 Git Workflow

### Daily Development:
```bash
# 1. Make changes to your code
# 2. Test locally
func start

# 3. Commit and push
git add .
git commit -m "Add new feature"
git push origin main

# 4. GitHub Actions automatically deploys!
```

### Manual Deployment:
```bash
# Deploy manually if needed
./azure-functions-deployment/scripts/deploy-functions.sh
```

## 🎯 Benefits of This Approach

1. **Simple Git Workflow** - Just push to deploy
2. **Fast Deployments** - No Docker build time
3. **Better Performance** - Native Azure Functions optimization
4. **Cost Effective** - No container registry costs
5. **Easy Debugging** - Direct access to logs
6. **Automatic Scaling** - Better integration with Azure

## 🚨 Troubleshooting

### Common Issues:

1. **Deploy Fails:**
   ```bash
   # Check logs
   az webapp log tail --resource-group musical-instruments-rg --name musical-instruments-api
   
   # Verify publish profile
   az functionapp deployment list-publishing-credentials --resource-group musical-instruments-rg --name musical-instruments-api
   ```

2. **Functions Not Starting:**
   ```bash
   # Check environment variables
   az functionapp config appsettings list --resource-group musical-instruments-rg --name musical-instruments-api
   
   # Restart Functions
   az functionapp restart --resource-group musical-instruments-rg --name musical-instruments-api
   ```

3. **Dependencies Issues:**
   ```bash
   # Verify requirements.txt
   cat azure-functions-deployment/functions/requirements.txt
   
   # Test locally first
   cd azure-functions-deployment/functions
   pip install -r requirements.txt
   func start
   ```

## ✅ Success Checklist

- [ ] Azure Functions Core Tools installed
- [ ] Local development working
- [ ] GitHub Actions configured
- [ ] Publish profile added to GitHub secrets
- [ ] First deployment successful
- [ ] Health check passing
- [ ] All endpoints working
- [ ] Monitoring configured

This Git-based approach gives you the best of both worlds: simplicity of Git deployment with the power of Azure Functions!
