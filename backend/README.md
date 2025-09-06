# Musical Instruments Platform - Backend

A FastAPI-based backend for comparing musical instruments with AI-generated content and affiliate store integration, deployed on **Azure App Service** with Docker containers.

## 🏗️ Architecture

- **Framework**: FastAPI with AsyncPG for PostgreSQL
- **Database**: Azure PostgreSQL Flexible Server with rich AI-generated content
- **Cache**: Azure Redis Cache for search and trending data
- **Authentication**: API key-based security with CORS protection
- **Deployment**: Azure App Service (Linux Container) with Docker
- **Content**: OpenAI-powered product descriptions in multiple languages
- **Affiliate System**: Smart store routing with brand exclusivity rules

## 🚀 **LIVE DEPLOYMENT**

**Production API**: `https://getyourmusicgear-api.azurewebsites.net`
- Health Check: ✅ https://getyourmusicgear-api.azurewebsites.net/health
- Documentation: Disabled in production for security
- Authentication: Required via `X-API-Key` header

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database (Azure PostgreSQL Flexible Server)
- Redis server (Azure Redis Cache)
- Docker (for containerized deployment)

### Local Development

1. **Install Dependencies**
```bash
pip install -r requirements.txt
```

2. **Environment Setup**
Copy `local.settings.json` and configure:
```json
{
  "IsEncrypted": false,
  "Values": {
    "DATABASE_URL": "postgresql://...",
    "API_KEY": "your-api-key",
    "OPENAI_API_KEY": "your-openai-key",
    "ENVIRONMENT": "development"
  }
}
```

3. **Database Migration**
```bash
alembic upgrade head
```

4. **Run Locally**
```bash
# FastAPI development server
python main.py
# or
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Docker development
docker build -t getyourmusicgear-backend .
docker run -p 8000:8000 --env-file .env getyourmusicgear-backend
```

## 🔐 Azure App Service Configuration

**Environment variables are securely managed via Azure App Service Application Settings:**

### Current Production Configuration
```bash
# Database & Cache
DATABASE_URL=postgresql://getyourmusicgear:***@getyourmusicgear-db.postgres.database.azure.com:5432/getyourmusicgear
REDIS_URL=rediss://:***@getyourmusicgear-redis.redis.cache.windows.net:6380

# Security
API_KEY=''
SECRET_KEY=***

# Application
ENVIRONMENT=production
DEBUG=false
PROJECT_NAME=GetYourMusicGear API
DOMAIN=getyourmusicgear.com
FRONTEND_URL=https://getyourmusicgear.com
```

### Managing Settings
```bash
# Set environment variables via Azure CLI
az webapp config appsettings set --name getyourmusicgear-api --resource-group getyourmusicgear --settings KEY=VALUE

# Or use Azure Portal → App Service → Configuration → Application Settings
```

## 🎵 Core Features

### 1. Product Management
- **Rich Content**: AI-generated descriptions, specifications, and reviews
- **Multi-language**: English (default), German, Spanish, French, Italian, Portuguese  
- **Categories**: 25+ instrument categories from guitars to DJ equipment
- **Brands**: 100+ brands with exclusivity rules

### 2. Affiliate System
Smart routing system that:
- **Brand Exclusivity**: Routes Harley Benton products exclusively to Thomann
- **Regional Priority**: Optimizes store selection by user location
- **Dynamic Scoring**: Calculates best store based on multiple factors
- **Fallback URLs**: Handles unavailable affiliate links gracefully

**Example Brand Exclusivity:**
```python
# Harley Benton products only show Thomann
harley_benton_product = await get_product(36)  # Harley Benton Delta Blues T
affiliate_stores = harley_benton_product.affiliate_stores
# Returns: [{"name": "Thomann", "priority_score": 210, "is_exclusive": true}]
```

### 3. Content Processing
OpenAI batch processing system generates:
- **Technical Analysis**: Sound characteristics, build quality, playability
- **Purchase Guidance**: Why buy, alternatives, best use cases  
- **User Reviews**: Synthetic ratings and review highlights
- **Maintenance**: Care instructions and common issues
- **Professional Assessment**: Expert ratings and competitive analysis

### 4. Search & Filtering  
- **Full-text search** across product names and descriptions
- **Category filtering** with nested relationships  
- **Brand filtering** with exclusivity awareness
- **Price range filtering** with real-time affiliate pricing
- **Sorting options**: name, price, rating, popularity

## 📊 API Endpoints

### Authentication
All endpoints require `X-API-Key` header:
```bash
curl -H "X-API-Key: your-api-key" https://getyourmusicgear-api.azurewebsites.net/api/v1/products
```

### Core Endpoints

**Products**
- `GET /api/v1/products` - List/search products with filters
- `GET /api/v1/products/{id}` - Get product details with affiliate stores
- `POST /api/v1/products/{id}/affiliate-stores` - Get affiliate store recommendations

**Categories & Brands**  
- `GET /api/v1/categories` - List all categories
- `GET /api/v1/brands` - List all brands

**Search**
- `GET /api/v1/search` - Unified search across products

### Response Structure
```json
{
  "id": 36,
  "name": "Harley Benton Delta Blues T",
  "brand": {"name": "Harley Benton"},
  "category": {"name": "Travel Guitars"},
  "content": {
    "basic_info": {
      "overview": "Vintage-style travel acoustic guitar...",
      "key_features": ["Compact travel size", "Mahogany body"],
      "target_skill_level": "Beginner to Intermediate"
    },
    "purchase_decision": {
      "why_buy": "Affordable, portable and solidly built...",
      "best_for": ["Travelers", "Beginners", "Students"]
    },
    "specifications": {"body_material": "Mahogany"},
    "store_links": {"thomann": {"product_url": "https://..."}}
  },
  "affiliate_stores": [
    {
      "name": "Thomann",
      "priority_score": 210,
      "is_exclusive": true,
      "affiliate_url": "https://thomann.de/..."
    }
  ]
}
```

## 🗄️ Database Schema

### Core Tables
- **products** - Product catalog with AI-generated JSON content
- **brands** - Brand information and exclusivity rules  
- **categories** - Hierarchical product categories
- **affiliate_stores** - Store configuration and affiliate settings
- **product_prices** - Real-time pricing from multiple stores
- **brand_exclusivities** - Brand-store exclusivity relationships

### Content Structure
Products contain rich JSON content with:
- **Global fields** (always English): specifications, store_links, warranty_info, qa
- **Localized fields**: basic_info, purchase_decision, usage_guidance, technical_analysis

## 🤖 AI Content System

### Batch Processing
Uses OpenAI batch API for cost-effective content generation:

1. **Input**: Basic product data (name, description, price, category)
2. **Processing**: GPT-4 generates comprehensive product information  
3. **Output**: Structured JSON with 7 content sections in 6+ languages
4. **Storage**: Saved to products.content JSONB column

### Content Schema Compliance
All AI content follows strict JSON schema validation:
- **Required fields**: Ensures consistent content structure
- **Type validation**: Guarantees data integrity
- **Multi-language**: Consistent format across all languages

## 🔧 Configuration

### Environment Variables (Azure Application Settings)
```bash
# Database
DATABASE_URL=postgresql://getyourmusicgear:password@host:5432/db

# Authentication  
API_KEY=your-secure-api-key-64-chars-long

# OpenAI Integration
OPENAI_API_KEY=sk-your-openai-key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4

# Application
ENVIRONMENT=production
PROJECT_NAME=Musical Instruments Platform
FRONTEND_URL=https://getyourmusicgear.com
DOMAIN=getyourmusicgear.com

# Azure Storage (for future image handling)
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;...
```

## 📈 Performance & Scaling

### Azure App Service Benefits
- **Container-based**: Docker deployment with full control
- **Always On**: Eliminates cold starts for consistent performance
- **Integrated scaling**: Manual and automatic scaling options
- **Built-in security**: HTTPS, authentication, and firewall rules

### Database Optimization
- **Indexes**: Optimized for search and filtering queries
- **JSONB content**: Efficient storage and querying of AI content
- **Connection pooling**: AsyncPG with connection management
- **Query optimization**: Selective loading with SQLAlchemy

## 🚀 Deployment

### Azure App Service Container Deployment
1. **Build Docker Image**: `docker build -t backend .`
2. **Push to Container Registry**: `docker push getyourmusicgear.azurecr.io/getyourmusicgear-backend:latest`
3. **Update App Service**: Configure to use new container image
4. **Restart App Service**: Apply changes and deploy

**Detailed deployment guide**: See `DEPLOYMENT_README.md`

### Frontend Integration
Frontend can call the API directly with authentication:
```typescript
// Direct API calls with authentication
const response = await fetch('https://getyourmusicgear-api.azurewebsites.net/api/v1/products?limit=10', {
  headers: {
    'X-API-Key': 'de798fd16f6a38539f9d590dd72c4a02f20afccd782e91bbbdc34037482632db',
    'Content-Type': 'application/json'
  }
});

// Or use a proxy in your frontend for security (recommended)
const response = await fetch('/api/proxy/products?limit=10');
```

## 🧪 Testing

### API Testing
```bash
# Health check (no auth required)
curl https://getyourmusicgear-api.azurewebsites.net/health

# Product search (requires API key)
curl -H "X-API-Key: YOUR_API_KEY" \
  "https://getyourmusicgear-api.azurewebsites.net/api/v1/products?query=guitar&limit=5"

# Specific product with affiliate stores
curl -H "X-API-Key: YOUR_API_KEY" \
  "https://getyourmusicgear-api.azurewebsites.net/api/v1/products/36"
```

### Local Testing
```bash
# Run test script
python test_product_endpoint.py

# Check affiliate exclusivity
python check_affiliate_stores.py
```

## 📊 Monitoring

### Application Insights Integration
Automatic monitoring of:
- **Request volume and latency**
- **Error rates and exceptions**  
- **Dependency calls** (database, external APIs)
- **Custom metrics** for business logic

### Logging
```python
import logging
logger = logging.getLogger(__name__)

# Logs automatically sent to Application Insights
logger.info("Product search executed", extra={"query": query, "results": count})
logger.error("Database connection failed", exc_info=True)
```

## 🔒 Security

### Authentication
- **API Key**: Required for all API endpoints
- **Header-based**: `X-API-Key` header validation
- **Environment-based**: Keys stored securely in Azure

### Data Protection
- **HTTPS only**: All communication encrypted
- **SQL injection protection**: SQLAlchemy parameterized queries
- **Input validation**: Pydantic schema validation
- **CORS configuration**: Restricted to authorized domains

## 🎯 System Status

✅ **Database**: Azure PostgreSQL with rich AI content  
✅ **Cache**: Azure Redis Cache for performance optimization  
✅ **API**: All endpoints operational at https://getyourmusicgear-api.azurewebsites.net  
✅ **Authentication**: Secure API key system with CORS protection  
✅ **Security**: Production docs disabled, HTTPS enforced  
✅ **Deployment**: Live on Azure App Service with Docker containers  

🚀 **The system is production-ready and fully operational!** 🎉

**For detailed deployment information, see: [DEPLOYMENT_README.md](./DEPLOYMENT_README.md)**
