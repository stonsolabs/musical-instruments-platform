# Azure Functions Deployment Guide

This guide explains how to deploy the backend from the `/backend` subdirectory to Azure Functions.

## Prerequisites

1. **Azure CLI installed**: [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
2. **Azure subscription and Function App created**
3. **Logged in to Azure CLI**: `az login`
4. **Python 3.11** installed locally

## Deployment Options

### Option 1: GitHub Actions (Recommended)

1. **Move workflow file to repository root**:
   ```bash
   # From the repository root
   mkdir -p .github/workflows
   cp backend/azure-functions-deploy.yml .github/workflows/
   ```

2. **Set up Azure credentials**:
   - Go to your GitHub repository → Settings → Secrets and variables → Actions
   - Add these secrets:
     - `AZURE_FUNCTIONAPP_PUBLISH_PROFILE`: Download from Azure portal
     - OR `AZURE_CREDENTIALS`: JSON with service principal credentials

3. **Update the workflow file**:
   - Replace `AZURE_FUNCTIONAPP_NAME` with your Function App name
   - Replace `RESOURCE_GROUP` with your resource group name

4. **Push to main branch**:
   ```bash
   git add .github/workflows/azure-functions-deploy.yml
   git commit -m "Add Azure Functions deployment workflow"
   git push origin main
   ```

### Option 2: Manual Deployment Script

1. **Update configuration**:
   ```bash
   export FUNCTION_APP_NAME="your-function-app-name"
   export RESOURCE_GROUP="your-resource-group"
   ```

2. **Run deployment script**:
   ```bash
   cd backend
   ./deploy-to-azure.sh
   ```

### Option 3: Azure CLI Direct

```bash
cd backend

# Install dependencies
pip install -r requirements.txt --target=".python_packages/lib/site-packages"

# Create deployment ZIP
zip -r ../backend-deploy.zip . -x "venv/*" "__pycache__/*" "*.pyc" ".env*" "local.settings.json"

# Deploy
az functionapp deployment source config-zip \
    --resource-group "your-resource-group" \
    --name "your-function-app-name" \
    --src ../backend-deploy.zip
```

## Configuration

### Required Environment Variables in Azure

Set these in the Azure portal under Configuration → Application settings:

```bash
DATABASE_URL="postgresql://user:password@host:port/database"
REDIS_URL="redis://host:port"
SECRET_KEY="your-secret-key"
API_KEY="your-api-key"
ENVIRONMENT="production"
FRONTEND_URL="https://your-frontend-domain.com"
DOMAIN="your-domain.com"
```

### Optional Environment Variables

```bash
AMAZON_ASSOCIATE_TAG="your-amazon-tag"
THOMANN_AFFILIATE_ID="your-thomann-id"
```

## Troubleshooting

### Common Issues

1. **"From directory doesn't exist" error**:
   - This happens when Azure tries to deploy from root instead of `/backend`
   - Use the provided GitHub Actions workflow or deployment script

2. **Import errors**:
   - Make sure all dependencies are in `requirements.txt`
   - Check that Python version matches (3.11)

3. **Function not starting**:
   - Check Azure portal logs
   - Verify environment variables are set
   - Ensure `host.json` and `function_app.py` are in the package

### Verification Steps

1. **Check deployment logs** in Azure portal
2. **Test health endpoint**: `https://your-app.azurewebsites.net/health`
3. **Test API endpoint**: `https://your-app.azurewebsites.net/api/v1/products`

## File Structure

The deployment package includes:
```
backend/
├── function_app.py          # Azure Functions entry point
├── host.json               # Azure Functions configuration
├── requirements.txt        # Python dependencies
├── app/                    # FastAPI application
│   ├── main.py            # FastAPI app instance
│   ├── models.py          # Database models
│   ├── config.py          # Configuration
│   └── api/               # API routes
└── .python_packages/       # Installed dependencies (auto-generated)
```

## GitHub Actions Workflow Features

- ✅ Triggers on changes to `backend/` directory
- ✅ Installs Python dependencies
- ✅ Cleans up development files
- ✅ Creates optimized deployment package
- ✅ Deploys to Azure Functions
- ✅ Verifies deployment

## Next Steps

After successful deployment:

1. Update frontend `NEXT_PUBLIC_API_BASE_URL` to point to your Azure Function App
2. Test the full stack integration
3. Set up monitoring and logging in Azure
4. Configure custom domains if needed

## Support

If you encounter issues:
1. Check Azure portal logs
2. Verify environment variables
3. Test locally with `func start`
4. Review the deployment guide above