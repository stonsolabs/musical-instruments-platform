# Azure Functions Deployment Guide

This guide shows how to deploy the Musical Instruments Platform backend to Azure Functions with automatic GitHub deployment.

## 🏗️ Azure Resources Setup

### 1. Create Azure Function App

**Option A: Azure Portal (Recommended)**
1. Go to Azure Portal → Create Resource → Function App
2. Configure:
   - **Resource Group**: Create new or use existing
   - **Function App Name**: `getyourmusicgear-backend` (must be globally unique)
   - **Runtime Stack**: Python 3.11
   - **Version**: 3.11
   - **Region**: Choose your preferred region
   - **Operating System**: Linux
   - **Plan Type**: Consumption (Serverless)

**Option B: Azure CLI**
```bash
# Create resource group
az group create --name getyourmusicgear-rg --location eastus

# Create function app
az functionapp create \
  --resource-group getyourmusicgear-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.11 \
  --functions-version 4 \
  --name getyourmusicgear-backend \
  --os-type linux \
  --storage-account getyourmusicgearstorage
```

### 2. Configure Secrets and Environment Variables

Azure Functions provides multiple secure ways to manage secrets:

#### Option A: Application Settings (Basic - Encrypted)
In Azure Portal → Function App → Configuration → Application Settings:

```bash
DATABASE_URL=postgresql://getyourmusicgear:arg-KDP8cjy.czu2zdv@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear
API_KEY=your-secure-api-key-here
OPENAI_API_KEY=your-openai-key
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4
ENVIRONMENT=production
PROJECT_NAME=Musical Instruments Platform
SECRET_KEY=your-secret-key-here
DEBUG=false
FRONTEND_URL=https://getyourmusicgear.com
BACKEND_URL=https://getyourmusicgear-backend.azurewebsites.net
DOMAIN=getyourmusicgear.com
AZURE_STORAGE_CONNECTION_STRING=your-azure-storage-connection-string
```

#### Option B: Azure Key Vault (Recommended - Most Secure)

1. **Create Key Vault**:
```bash
az keyvault create \
  --name getyourmusicgear-vault \
  --resource-group getyourmusicgear-rg \
  --location eastus
```

2. **Add Secrets to Key Vault**:
```bash
az keyvault secret set --vault-name getyourmusicgear-vault --name database-url --value "postgresql://..."
az keyvault secret set --vault-name getyourmusicgear-vault --name api-key --value "your-secure-key"
az keyvault secret set --vault-name getyourmusicgear-vault --name openai-key --value "your-openai-key"
```

3. **Configure Function App to Use Key Vault**:
In Application Settings, use Key Vault references:
```bash
DATABASE_URL=@Microsoft.KeyVault(SecretUri=https://getyourmusicgear-vault.vault.azure.net/secrets/database-url/)
API_KEY=@Microsoft.KeyVault(SecretUri=https://getyourmusicgear-vault.vault.azure.net/secrets/api-key/)
OPENAI_API_KEY=@Microsoft.KeyVault(SecretUri=https://getyourmusicgear-vault.vault.azure.net/secrets/openai-key/)
```

4. **Grant Function App Access**:
```bash
# Enable system managed identity for Function App
az functionapp identity assign --name getyourmusicgear-backend --resource-group getyourmusicgear-rg

# Grant Key Vault access
az keyvault set-policy \
  --name getyourmusicgear-vault \
  --object-id <function-app-principal-id> \
  --secret-permissions get
```

#### Option C: Managed Identity for Azure Services (Most Secure)

For Azure PostgreSQL and Storage, use Managed Identity (no connection strings needed):

1. **Enable Managed Identity** on Function App
2. **Grant Database Access**:
```sql
-- In PostgreSQL, create user for managed identity
CREATE ROLE "getyourmusicgear-backend" WITH LOGIN;
GRANT CONNECT ON DATABASE getyourmusicgear TO "getyourmusicgear-backend";
GRANT USAGE ON SCHEMA public TO "getyourmusicgear-backend";
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO "getyourmusicgear-backend";
```

3. **Update Connection String**:
```bash
DATABASE_URL=postgresql://getyourmusicgear-backend@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear
```

### Benefits of Each Approach

| Method | Security | Ease of Use | Cost | Best For |
|--------|----------|-------------|------|----------|
| Application Settings | Good | Easy | Free | Development, simple apps |
| Key Vault | Excellent | Medium | Low cost | Production, sensitive data |
| Managed Identity | Excellent | Medium | Free | Azure services integration |

## 🚀 GitHub Integration (Direct Deployment Connection)

### Azure Portal GitHub Integration (Recommended - No GitHub Actions)

Azure Functions supports **direct GitHub integration** without GitHub Actions:

1. **In Azure Portal**:
   - Go to your Function App
   - Navigate to **Deployment Center**
   - Choose **GitHub** as source
   - Authenticate with GitHub
   - Select:
     - **Organization**: Your GitHub username/organization
     - **Repository**: `musical-instruments-platform`
     - **Branch**: `main`
     - **Build Provider**: **App Service Build Service** (Kudu)
     - **Folder**: `/backend`

2. **Azure automatically**:
   - Connects directly to your GitHub repository
   - Monitors the `backend/` folder for changes
   - Deploys automatically on every push to main branch
   - No GitHub Actions workflow files needed

3. **Deployment triggers**:
   - Every push to the main branch that changes files in `backend/`
   - Manual sync from Azure Portal
   - Webhook-based (faster than GitHub Actions)

### Benefits of Direct GitHub Integration
✅ **No GitHub Actions needed** - Simpler setup
✅ **Faster deployments** - Direct webhook integration
✅ **No workflow files** - Less repository clutter
✅ **Azure native** - Integrated monitoring and logs
✅ **Automatic builds** - Azure handles the build process

## 📁 Project Structure for Azure Functions

```
backend/
├── function_app.py          # Main Azure Functions entry point
├── host.json               # Azure Functions configuration
├── local.settings.json     # Local development settings
├── requirements.txt        # Python dependencies (updated)
├── .funcignore            # Files to ignore during deployment
├── app/                   # Your FastAPI application
│   ├── __init__.py
│   ├── main.py           # FastAPI app
│   ├── models.py
│   ├── config.py
│   └── api/
└── alembic/              # Database migrations
```

## 🔧 Configuration Files

### `host.json` - Azure Functions Configuration
```json
{
  "version": "2.0",
  "functionTimeout": "00:05:00",
  "routePrefix": "",
  "http": {
    "routePrefix": ""
  }
}
```

### `function_app.py` - Main Entry Point
Handles the integration between Azure Functions and FastAPI.

## 🌐 Domain Configuration

### Custom Domain Setup (Optional)
1. In Azure Portal → Function App → Custom Domains
2. Add your subdomain: `api.getyourmusicgear.com`
3. Configure SSL certificate
4. Update DNS records:
   ```
   Type: CNAME
   Name: api
   Value: getyourmusicgear-backend.azurewebsites.net
   ```

### URL Structure After Deployment
- **Function App URL**: `https://getyourmusicgear-backend.azurewebsites.net`
- **API Endpoints**: `https://getyourmusicgear-backend.azurewebsites.net/api/v1/products`
- **Health Check**: `https://getyourmusicgear-backend.azurewebsites.net/health`
- **Custom Domain** (optional): `https://api.getyourmusicgear.com/api/v1/products`

## 🔐 Security Configuration

### API Key Authentication
The API requires `X-API-Key` header for all `/api/v1/*` endpoints.

### CORS Configuration
Already configured in `app/config.py` for:
- `https://getyourmusicgear.com`
- `https://www.getyourmusicgear.com`
- Vercel preview domains

## 📊 Monitoring & Logging

### Application Insights
Azure Functions automatically integrates with Application Insights for:
- Request tracking
- Performance monitoring
- Error logging
- Custom metrics

### Log Streaming
View live logs in Azure Portal → Function App → Log Stream

## 🚦 Testing Deployment

### 1. Health Check
```bash
curl https://getyourmusicgear-backend.azurewebsites.net/health
```

### 2. API Test with Authentication
```bash
curl -H "X-API-Key: your-api-key" \
     https://getyourmusicgear-backend.azurewebsites.net/api/v1/products?limit=1
```

### 3. Frontend Integration Test
Update frontend environment variable in Vercel:
```bash
NEXT_PUBLIC_API_BASE_URL=https://getyourmusicgear-backend.azurewebsites.net
```

## 🔄 Deployment Workflow

1. **Development**: Make changes in `backend/` folder
2. **Commit**: Push changes to GitHub main branch
3. **Automatic Trigger**: Azure detects changes via webhook
4. **Build**: Azure App Service Build Service installs dependencies
5. **Deploy**: Deploy to Azure Functions
6. **Verify**: Test endpoints and functionality

## 💡 Benefits of This Setup

✅ **Zero Maintenance**: No server management required
✅ **Auto-scaling**: Handles traffic spikes automatically  
✅ **Cost Effective**: Pay only for requests, not idle time
✅ **High Availability**: Built-in redundancy and failover
✅ **Direct GitHub Integration**: No GitHub Actions complexity
✅ **Fast Deployments**: Webhook-based, faster than CI/CD pipelines
✅ **SSL/TLS**: HTTPS enabled by default
✅ **Azure Storage Integration**: Ready for image storage

## 🛠️ Troubleshooting

### Common Issues

1. **Import Errors**
   - Ensure all dependencies in `requirements.txt`
   - Check Python version compatibility (3.11)

2. **Database Connection**
   - Verify `DATABASE_URL` in Application Settings
   - Check firewall rules allow Azure Services

3. **API Key Issues**
   - Verify `API_KEY` environment variable is set
   - Check header format: `X-API-Key: your-key`

4. **CORS Issues**
   - Domain already configured for getyourmusicgear.com
   - Check frontend is using correct API base URL

### Logs and Debugging
- Use Azure Portal Log Stream for real-time logs
- Check Application Insights for detailed error tracking
- Monitor deployment logs in Deployment Center

## 🎯 Deployment Steps

### 1. Setup Azure Function App
1. Create Function App in Azure Portal
2. Configure environment variables
3. Enable Application Insights

### 2. Connect GitHub Repository
1. Go to Deployment Center
2. Select GitHub as source
3. Authenticate and select repository
4. Choose `backend` folder
5. Select App Service Build Service

### 3. Update Frontend Configuration
In Vercel dashboard, update environment variable:
```
NEXT_PUBLIC_API_BASE_URL=https://getyourmusicgear-backend.azurewebsites.net
```

### 4. Test and Verify
1. Push a small change to `backend/` folder
2. Monitor deployment in Azure Portal
3. Test API endpoints
4. Verify frontend integration

## 🚀 Ready to Deploy!

The backend is now ready for Azure Functions deployment with:
- ✅ FastAPI integration via `function_app.py`
- ✅ Azure Functions configuration (`host.json`)
- ✅ Python dependencies including Azure packages
- ✅ Environment configuration
- ✅ Direct GitHub integration (no GitHub Actions needed)
- ✅ API key authentication
- ✅ CORS for getyourmusicgear.com
- ✅ Azure Storage support for future image handling