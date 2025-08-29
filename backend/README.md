# Musical Instruments Platform - Backend

A FastAPI-based backend for comparing musical instruments with AI-generated content and affiliate store integration, deployed on Azure Functions.

## 🏗️ Architecture

- **Framework**: FastAPI with AsyncPG for PostgreSQL
- **Database**: Azure PostgreSQL with rich AI-generated product content
- **Authentication**: API key-based security
- **Deployment**: Azure Functions with direct GitHub integration
- **Content**: OpenAI-powered product descriptions in multiple languages
- **Affiliate System**: Smart store routing with brand exclusivity rules

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL database (Azure PostgreSQL)
- Azure Functions Core Tools (for local development)

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
# For Azure Functions development
func start

# Or for FastAPI development  
uvicorn app.main:app --reload
```

## 🔐 Azure Secrets Configuration

**Yes, Azure Functions supports multiple secure ways to manage secrets:**

### Option 1: Application Settings (Recommended)
Azure Portal → Function App → Configuration → Application Settings
- Encrypted at rest and in transit
- Easy to manage via Azure Portal
- Environment variables accessible via `os.getenv()`

### Option 2: Azure Key Vault Integration
```bash
# Reference Key Vault secrets in Application Settings
@Microsoft.KeyVault(SecretUri=https://your-vault.vault.azure.net/secrets/database-url/)
```

### Option 3: Managed Identity (Most Secure)
- No connection strings needed
- Azure handles authentication automatically
- Perfect for Azure PostgreSQL and Storage connections

**Configuration Example:**
```json
{
  "DATABASE_URL": "@Microsoft.KeyVault(SecretUri=https://getyourmusicgear-vault.vault.azure.net/secrets/database-url/)",
  "API_KEY": "@Microsoft.KeyVault(SecretUri=https://getyourmusicgear-vault.vault.azure.net/secrets/api-key/)",
  "OPENAI_API_KEY": "@Microsoft.KeyVault(SecretUri=https://getyourmusicgear-vault.vault.azure.net/secrets/openai-key/)"
}
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
curl -H "X-API-Key: your-api-key" https://api.getyourmusicgear.com/api/v1/products
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

### Azure Functions Benefits
- **Auto-scaling**: Handles traffic spikes automatically
- **Cost-effective**: Pay only for actual requests  
- **High availability**: Built-in redundancy across regions
- **Cold start optimization**: ~2-3 second startup time

### Database Optimization
- **Indexes**: Optimized for search and filtering queries
- **JSONB content**: Efficient storage and querying of AI content
- **Connection pooling**: AsyncPG with connection management
- **Query optimization**: Selective loading with SQLAlchemy

## 🚀 Deployment

### Azure Functions Deployment
1. **Create Function App** in Azure Portal
2. **Configure Application Settings** with environment variables
3. **Connect GitHub Repository** with direct integration
4. **Deploy automatically** on every push to main branch

Detailed guide: See `AZURE_FUNCTIONS_DEPLOYMENT.md`

### Frontend Integration
Frontend uses secure API proxy to handle authentication:
```typescript
// Frontend calls secure proxy
const response = await fetch('/api/proxy/products?limit=10');

// Proxy adds API key and forwards to Azure Functions
const backendResponse = await fetch(
  'https://getyourmusicgear-backend.azurewebsites.net/api/v1/products?limit=10',
  { headers: { 'X-API-Key': process.env.API_KEY } }
);
```

## 🧪 Testing

### API Testing
```bash
# Health check
curl https://getyourmusicgear-backend.azurewebsites.net/health

# Product search (requires API key)
curl -H "X-API-Key: your-key" \
  "https://getyourmusicgear-backend.azurewebsites.net/api/v1/products?query=guitar&limit=5"

# Specific product with affiliate stores
curl -H "X-API-Key: your-key" \
  "https://getyourmusicgear-backend.azurewebsites.net/api/v1/products/36"
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

✅ **Database**: 45 products with rich AI content  
✅ **API**: All endpoints operational with English-first content  
✅ **Authentication**: Secure API key system  
✅ **Affiliate System**: Smart routing with brand exclusivity  
✅ **Content**: OpenAI batch processing generating quality descriptions  
✅ **Deployment**: Ready for Azure Functions with GitHub integration  

The system is production-ready and fully operational! 🎉