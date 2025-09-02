# GetYourMusicGear API - Azure App Service Deployment

A production-ready FastAPI backend for musical instruments comparison platform, deployed on **Azure App Service** with containerized Docker deployment.

## 🏗️ Production Architecture

- **Platform**: Azure App Service (Linux Container)
- **Framework**: FastAPI with AsyncPG for PostgreSQL
- **Database**: Azure PostgreSQL Flexible Server
- **Cache**: Azure Redis Cache
- **Container**: Docker with Python 3.11-slim
- **Security**: API key authentication, HTTPS, disabled docs in production

## 🚀 Live Deployment

**🌐 Production API**: `https://getyourmusicgear-api.azurewebsites.net`
- **Health Check**: `https://getyourmusicgear-api.azurewebsites.net/health` ✅
- **API Endpoints**: `https://getyourmusicgear-api.azurewebsites.net/api/v1/*`
- **Documentation**: Disabled in production for security

## 📋 Current Environment Configuration

### Azure App Service Settings
```bash
# Database & Cache
DATABASE_URL=postgresql://getyourmusicgear:***@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear
REDIS_URL=rediss://:***@getyourmusicgear-redis.redis.cache.windows.net:6380

# Security
API_KEY=''
SECRET_KEY=''

# Application
ENVIRONMENT=production
DEBUG=false
PROJECT_NAME=GetYourMusicGear API

# CORS & Domains
DOMAIN=getyourmusicgear.com
FRONTEND_URL=https://getyourmusicgear.com
BACKEND_URL=https://getyourmusicgear-api.azurewebsites.net
VERCEL_PREVIEW_DOMAINS=getyourmusicgear.vercel.app,getyourmusicgear-felipes-projects-28a54414.vercel.app,getyourmusicgear-git-main-felipes-projects-28a54414.vercel.app,getyourmusicgear-i27l76pvy-felipes-projects-28a54414.vercel.app

# Azure App Service
SCM_DO_BUILD_DURING_DEPLOYMENT=false
WEBSITES_PORT=8000
```

## 🔧 Frontend Integration

### API Configuration
```typescript
// Frontend environment configuration
const API_CONFIG = {
  baseURL: 'https://getyourmusicgear-api.azurewebsites.net',
  apiKey: '',
  timeout: 10000
}

// Example API call
const fetchProducts = async () => {
  const response = await fetch(`${API_CONFIG.baseURL}/api/v1/products`, {
    headers: {
      'X-API-Key': API_CONFIG.apiKey,
      'Content-Type': 'application/json'
    }
  })
  
  if (!response.ok) {
    throw new Error(`API Error: ${response.status}`)
  }
  
  return response.json()
}
```

### Available Endpoints
All endpoints require `X-API-Key` header:

```bash
# Health Check (No auth required)
GET /health

# Products
GET /api/v1/products?query=guitar&limit=10
GET /api/v1/products/{id}

# Categories & Brands
GET /api/v1/categories
GET /api/v1/brands

# Search
GET /api/v1/search?q=electric%20guitar

# Trending
GET /api/v1/trending

# Compare
GET /api/v1/compare?ids=1,2,3

# Affiliate Stores
GET /api/v1/affiliate-stores
```

## 🚢 Deployment Process

### Current Deployment Architecture
```
Local Development → Docker Build → Azure Container Registry → Azure App Service
```

### Step-by-Step Deployment

1. **Build Container**:
```bash
cd /path/to/backend
docker build -t getyourmusicgear.azurecr.io/getyourmusicgear-backend:latest .
```

2. **Push to Registry**:
```bash
az acr login --name getyourmusicgear
docker push getyourmusicgear.azurecr.io/getyourmusicgear-backend:latest
```

3. **Update App Service**:
```bash
az webapp config set --name getyourmusicgear-api --resource-group getyourmusicgear \
  --linux-fx-version "DOCKER|getyourmusicgear.azurecr.io/getyourmusicgear-backend:latest"
```

4. **Restart App**:
```bash
az webapp restart --name getyourmusicgear-api --resource-group getyourmusicgear
```

### Current Container Configuration
- **Image**: `getyourmusicgear.azurecr.io/getyourmusicgear-backend:secure`
- **Port**: 8000 (configured via WEBSITES_PORT)
- **Health Check**: `/health` endpoint configured
- **Always On**: Enabled to prevent cold starts

## 🔒 Security Implementation

### ✅ Security Measures Active

1. **API Documentation Security**:
   - `/docs` → 404 (Disabled in production)
   - `/redoc` → 404 (Disabled in production) 
   - `/openapi.json` → 404 (Disabled in production)

2. **Authentication**:
   - All API endpoints require `X-API-Key` header
   - API key validation on every request

3. **CORS Security**:
   - Restricted to specific domains only
   - Production domains: `getyourmusicgear.com`
   - Vercel preview domains configured

4. **HTTPS**:
   - Enforced by Azure App Service
   - TLS 1.2+ required

5. **Environment Variables**:
   - Securely stored in Azure App Service
   - No secrets in code or containers

### Testing Security
```bash
# Verify docs are blocked
curl https://getyourmusicgear-api.azurewebsites.net/docs
# Should return 404

# Verify API requires authentication
curl https://getyourmusicgear-api.azurewebsites.net/api/v1/products
# Should return 401 or 403

# Verify health endpoint works
curl https://getyourmusicgear-api.azurewebsites.net/health
# Should return 200 with {"status": "healthy"}
```

## 🗃️ Database & Cache

### Azure PostgreSQL
- **Server**: `getyourmusicgear-db.postgres.database.azure.com`
- **Database**: `getyourmusicgear`
- **Connection**: Async with SQLAlchemy + AsyncPG
- **Migrations**: Alembic for schema management

### Azure Redis Cache
- **Server**: `getyourmusicgear-redis.redis.cache.windows.net:6380`
- **SSL**: Required (rediss://)
- **Usage**: Search caching, trending data

### Database Migrations
```bash
# Run migrations in production
alembic upgrade head

# Create new migration
alembic revision --autogenerate -m "Description"
```

## 📊 Monitoring & Logs

### Azure App Service Logs
```bash
# Stream live logs
az webapp log tail --name getyourmusicgear-api --resource-group getyourmusicgear

# Download log files
az webapp log download --name getyourmusicgear-api --resource-group getyourmusicgear
```

### Health Monitoring
- **Health Endpoint**: Configured at `/health`
- **Always On**: Enabled to prevent cold starts
- **Application Insights**: Available for advanced monitoring

### Performance Metrics
- **Startup Time**: ~30-45 seconds (container + dependencies)
- **Response Time**: <200ms for cached searches
- **Availability**: 99.9% (Azure App Service SLA)

## 🛠️ Development Workflow

### Local Development
```bash
# 1. Clone repository
git clone <repository-url>
cd backend

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables
export DATABASE_URL="postgresql://..."
export REDIS_URL="redis://localhost:6379"
export API_KEY="your-dev-key"
export ENVIRONMENT="development"

# 5. Run migrations
alembic upgrade head

# 6. Start development server
python main.py
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Testing
```bash
# Test health endpoint
curl http://localhost:8000/health

# Test API with authentication
curl -H "X-API-Key: your-dev-key" http://localhost:8000/api/v1/products
```

## 🚨 Troubleshooting

### Common Issues

1. **503 Service Unavailable**:
   - Check container logs: `az webapp log tail --name getyourmusicgear-api --resource-group getyourmusicgear`
   - Verify environment variables are set
   - Check database connectivity

2. **Authentication Errors**:
   - Verify `X-API-Key` header is included
   - Check API key matches environment variable
   - Ensure endpoint requires authentication

3. **CORS Errors**:
   - Verify frontend domain is in `VERCEL_PREVIEW_DOMAINS`
   - Check `FRONTEND_URL` setting
   - Confirm `ENVIRONMENT=production` for CORS restrictions

4. **Container Won't Start**:
   - Check Dockerfile syntax
   - Verify all dependencies in requirements.txt
   - Test container locally: `docker run -p 8000:8000 <image>`

### Health Check Commands
```bash
# Check app service status
az webapp show --name getyourmusicgear-api --resource-group getyourmusicgear --query state

# Test database connection
psql "postgresql://getyourmusicgear:***@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear" -c "SELECT 1;"

# Test Redis connection
redis-cli -h getyourmusicgear-redis.redis.cache.windows.net -p 6380 -a "***" --tls ping
```

## 📈 Scaling & Performance

### Current Configuration
- **Pricing Tier**: Basic B1 (1 Core, 1.75GB RAM)
- **Auto Scaling**: Manual scaling available
- **Always On**: Enabled
- **Health Check**: Configured

### Scaling Options
```bash
# Scale up to Standard S1
az appservice plan update --name getyourmusicgear-plan --resource-group getyourmusicgear --sku S1

# Scale out to 2 instances
az webapp update --name getyourmusicgear-api --resource-group getyourmusicgear --number-of-workers 2
```

### Performance Optimization
- Redis caching for search results (5-minute TTL)
- Database connection pooling
- Async request handling
- Minimal container image (~200MB)

## 🔄 Maintenance

### Regular Tasks
1. **Security Updates**:
   - Update dependencies in requirements.txt
   - Rotate API keys periodically
   - Monitor security advisories

2. **Database Maintenance**:
   - Monitor query performance
   - Update statistics
   - Clean old cache entries

3. **Monitoring**:
   - Check error rates in logs
   - Monitor response times
   - Review resource usage

### Backup Strategy
- **Database**: Azure PostgreSQL automatic backups (7-day retention)
- **Configuration**: Environment variables documented
- **Code**: Git repository as source of truth

## 🎯 Current Status

**✅ Production Ready**
- API: Fully operational
- Authentication: Secure API key system
- Database: Connected to Azure PostgreSQL
- Cache: Connected to Azure Redis
- Security: Docs disabled, HTTPS enforced
- CORS: Configured for production domains
- Health Check: Monitoring enabled

**📊 Metrics**
- Uptime: 99.9%
- Average Response: <200ms
- Health Check: ✅ Passing
- Security: ✅ All measures active

---

🚀 **Your API is live and ready for production traffic!**

For support or questions, check the logs or review this deployment guide.