# Backend Requirements Review

## 📦 Current Packages Analysis

### ✅ **Essential Packages (KEEP)**

**Core Framework & Database:**
- `fastapi==0.104.1` - ✅ Main web framework
- `sqlalchemy>=2.0.25` - ✅ Database ORM  
- `asyncpg==0.29.0` - ✅ PostgreSQL async driver
- `alembic==1.13.1` - ✅ Database migrations
- `pydantic==2.5.3` - ✅ Data validation (FastAPI dependency)
- `pydantic-settings==2.1.0` - ✅ Configuration management

**Database Drivers:**
- `psycopg2-binary==2.9.9` - ⚠️ **REVIEW** - Sync PostgreSQL driver (may not be needed with asyncpg)

**Caching & Performance:**
- `redis==5.0.1` - ✅ Essential for search caching and trending features

**HTTP & API:**
- `python-multipart==0.0.6` - ✅ Form data handling
- `httpx==0.25.2` - ✅ Async HTTP client
- `aiohttp==3.9.1` - ✅ Used in crawler system
- `requests==2.31.0` - ✅ Sync HTTP client (used in some services)

**AI/OpenAI Integration:**
- `openai==1.3.7` - ✅ OpenAI API client for content generation

**Web Scraping (Crawler System):**
- `beautifulsoup4==4.12.2` - ✅ HTML parsing for crawler
- `lxml==4.9.3` - ✅ XML/HTML parser (faster than default)

**Authentication & Security:**
- `python-jose[cryptography]==3.3.0` - ⚠️ **REVIEW** - JWT tokens (not currently used in API)
- `passlib[bcrypt]==1.7.4` - ⚠️ **REVIEW** - Password hashing (not used in current API)

**Utilities:**
- `python-dotenv==1.0.0` - ✅ Environment variable loading
- `python-slugify==8.0.1` - ✅ URL slug generation

**Azure Functions (NEW):**
- `azure-functions==1.18.0` - ✅ Required for Azure Functions
- `azure-functions-worker==1.0.0` - ✅ Required for Azure Functions
- `azure-storage-blob==12.19.0` - ✅ For future image storage
- `azure-identity==1.15.0` - ✅ Managed identity authentication

**REMOVED (Not in current requirements.txt):**
- `uvicorn[standard]==0.24.0` - ❌ Not needed for Azure Functions

## 🗑️ **Packages to Consider Removing**

### **Security Packages (Not Used)**
```python
# These are not used in current authentication system:
python-jose[cryptography]==3.3.0  # JWT token handling - API uses simple API key
passlib[bcrypt]==1.7.4             # Password hashing - no user passwords stored
```

### **Database Driver Redundancy**
```python
# May be redundant since we use asyncpg:
psycopg2-binary==2.9.9  # Sync driver - check if crawler/batch processing needs it
```

## ✅ **Optimized Requirements.txt**

### **Minimal Production Version:**
```txt
# Core Framework
fastapi==0.104.1
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6

# Database
sqlalchemy>=2.0.25
asyncpg==0.29.0
alembic==1.13.1

# Redis Caching
redis==5.0.1

# HTTP Clients
httpx==0.25.2
aiohttp==3.9.1
requests==2.31.0

# AI Integration
openai==1.3.7

# Web Scraping (for crawler)
beautifulsoup4==4.12.2
lxml==4.9.3

# Utilities
python-dotenv==1.0.0
python-slugify==8.0.1

# Azure Functions
azure-functions==1.18.0
azure-functions-worker==1.0.0
azure-storage-blob==12.19.0
azure-identity==1.15.0
```

### **Full Version (Keep Current Packages):**
```txt
# Keep all current packages for safety
fastapi==0.104.1
sqlalchemy>=2.0.25
asyncpg==0.29.0
psycopg2-binary==2.9.9
alembic==1.13.1
redis==5.0.1
pydantic==2.5.3
pydantic-settings==2.1.0
python-multipart==0.0.6
openai==1.3.7
httpx==0.25.2
aiohttp==3.9.1
beautifulsoup4==4.12.2
lxml==4.9.3
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
python-slugify==8.0.1
requests==2.31.0
azure-functions==1.18.0
azure-functions-worker==1.0.0
azure-storage-blob==12.19.0
azure-identity==1.15.0
```

## 🔍 **Package Usage Analysis**

### **Used in Core API:**
- FastAPI, SQLAlchemy, AsyncPG, Pydantic - Core API functionality ✅
- Redis - Search caching and trending features ✅  
- OpenAI - AI content generation ✅

### **Used in Crawler System:**
- aiohttp, BeautifulSoup, lxml, requests - Web scraping ✅

### **Used in Batch Processing:**  
- OpenAI, httpx - Batch content generation ✅

### **Not Currently Used:**
- python-jose, passlib - Authentication packages (API uses simple API key)
- psycopg2-binary - May be used by some scripts, but asyncpg handles main DB

## 💡 **Recommendation**

**For Production Deployment: Keep All Packages**
- Safer to keep current packages to avoid breaking crawler/batch systems
- Total package size is reasonable for Azure Functions
- Unused packages have minimal impact on cold start time

**For Future Optimization:**
- Test removing `python-jose` and `passlib` in staging
- Verify if `psycopg2-binary` is needed by any scripts
- Consider adding these back only if needed

## 🚀 **New Redis Features Added**

With the trending service, Redis now provides:

1. **Search Caching** (existing)
   - Search results cached for 5 minutes
   - Autocomplete suggestions cached

2. **Trending Instruments** (new)
   - Real-time view tracking per product
   - Hourly view analytics with decay weights  
   - Trending scores based on recent activity

3. **Popular Comparisons** (new)
   - Track when products are compared
   - Rank comparison pairs by frequency
   - Cache popular comparison results

4. **Analytics Dashboard** (new)
   - View counts per hour/day
   - Comparison statistics  
   - Cache health monitoring

**New API Endpoints:**
- `GET /api/v1/trending/instruments` - Get trending products
- `GET /api/v1/trending/comparisons` - Get popular comparisons  
- `POST /api/v1/trending/track/view/{id}` - Track product views
- `POST /api/v1/trending/track/comparison` - Track comparisons

**Redis Benefits for Your Site:**
✅ **Homepage** - Show trending instruments automatically
✅ **Performance** - Cached trending calculations  
✅ **User Engagement** - Popular comparison suggestions
✅ **Analytics** - Real-time usage insights
✅ **SEO** - Dynamic content based on user behavior

The trending system will make your homepage dynamic and engaging by showing what instruments people are actually viewing and comparing! 🎵