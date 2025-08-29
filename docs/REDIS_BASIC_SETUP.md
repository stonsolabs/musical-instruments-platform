# Azure Cache for Redis - Basic C0 Setup

## ✅ **Your Choice: Basic C0**

### **Configuration:**
- **SKU**: Basic C0  
- **Memory**: 250MB
- **Cost**: ~$16/month ($192/year)
- **Single Node**: No replica (acceptable for development/startup)

## 🛠️ **Setup Instructions**

### **1. Create Basic C0 Redis Cache**
```bash
# Create Basic C0 Redis Cache
az redis create \
  --name getyourmusicgear-redis \
  --resource-group getyourmusicgear-rg \
  --location eastus \
  --sku Basic \
  --vm-size C0 \
  --enable-non-ssl-port false
```

### **2. Get Connection Information**
```bash
# Get Redis keys
az redis list-keys \
  --name getyourmusicgear-redis \
  --resource-group getyourmusicgear-rg

# Get Redis hostname
az redis show \
  --name getyourmusicgear-redis \
  --resource-group getyourmusicgear-rg \
  --query hostName
```

### **3. Connection String for Basic C0**
```bash
# Non-SSL connection (Basic tier doesn't require SSL)
REDIS_URL=redis://getyourmusicgear-redis.redis.cache.windows.net:6379?password=your-redis-primary-key

# Or SSL connection (recommended even for Basic)
REDIS_URL=rediss://getyourmusicgear-redis.redis.cache.windows.net:6380?ssl_cert_reqs=required&password=your-redis-primary-key
```

## ⚖️ **Basic C0 Considerations**

### **Pros:**
✅ **Cost**: Only $16/month - great for startup budget
✅ **Memory**: 250MB is still 15x your current needs (8-17MB)
✅ **Performance**: Same Redis performance as Standard tier
✅ **Features**: All caching functionality works perfectly

### **Limitations:**
⚠️ **No SLA**: No guaranteed uptime (but typically very reliable)
⚠️ **Single Node**: No automatic failover if instance fails
⚠️ **No Persistence**: Data is lost if Redis restarts (but caches rebuild automatically)

### **Impact on Your Application:**
✅ **Search Caching**: Works perfectly - if cache is down, falls back to database
✅ **Trending Data**: Works perfectly - analytics rebuild automatically
✅ **User Experience**: Minimal impact during rare Redis outages (just slower, not broken)

## 🔧 **Azure Functions Configuration**

### **Environment Variables:**
```bash
# Add to Azure Functions Application Settings:
REDIS_URL=redis://getyourmusicgear-redis.redis.cache.windows.net:6379?password=your-primary-key
REDIS_TIMEOUT=5
REDIS_MAX_CONNECTIONS=10
```

### **Connection Pool Settings (for Basic):**
```python
# In your trending_service.py and search_service.py
redis_client = redis.from_url(
    settings.REDIS_URL, 
    decode_responses=True,
    max_connections=10,  # Lower for Basic tier
    retry_on_timeout=True,
    socket_timeout=5
)
```

## 📊 **Monitoring Basic C0**

### **Key Metrics to Watch:**
- **Memory Usage**: Should stay well under 250MB
- **Connected Clients**: Keep under 20 for Basic tier
- **Operations/Second**: Monitor for performance
- **Cache Hit Rate**: Target >80%

### **Set Alerts For:**
- Memory usage > 200MB (80% of capacity)
- Connected clients > 15
- Cache miss rate > 30%

## 🚀 **Deployment Steps**

### **1. Create Redis Cache**
```bash
az redis create \
  --name getyourmusicgear-redis \
  --resource-group getyourmusicgear-rg \
  --sku Basic \
  --vm-size C0
```

### **2. Update Azure Functions Settings**
In Azure Portal → Function App → Configuration → Application Settings:
```
Name: REDIS_URL
Value: redis://getyourmusicgear-redis.redis.cache.windows.net:6379?password=your-key
```

### **3. Test Connection**
```bash
# Test Redis connection
curl -H "X-API-Key: your-api-key" \
  "https://getyourmusicgear-backend.azurewebsites.net/api/v1/search/autocomplete?q=guitar"
```

### **4. Monitor Performance**
Check Azure Portal → Redis Cache → Metrics for:
- Memory usage
- Cache hit/miss rates
- Connection counts

## 📈 **Upgrade Path**

### **When to Upgrade to Standard C0:**
- If you experience any Redis downtime affecting users
- When you need guaranteed 99.9% SLA
- If you want automatic failover protection
- For production stability (only +$14/month)

### **Easy Upgrade Command:**
```bash
# Upgrade to Standard C0 (can do anytime)
az redis update \
  --name getyourmusicgear-redis \
  --resource-group getyourmusicgear-rg \
  --sku Standard
```

## 💡 **Optimization Tips for Basic C0**

### **1. Aggressive TTL Management**
```python
# Shorter TTLs to save memory
self.trending_cache_ttl = 1800    # 30 min instead of 1 hour
self.search_cache_ttl = 180       # 3 min instead of 5 min
```

### **2. Memory-Efficient Keys**
```python
# Use shorter key names to save memory
cache_key = f"t:{category_id}:{limit}"     # Instead of "trending:instruments:..."
search_key = f"s:{hash[:8]}:{limit}"       # Shorter hash
```

### **3. Graceful Degradation**
```python
# Always handle Redis failures gracefully
try:
    cached_result = await self.redis_client.get(cache_key)
    if cached_result:
        return json.loads(cached_result)
except Exception:
    # Continue without cache - get from database
    pass
```

## 🎯 **Summary**

**Basic C0 is a great choice for your startup phase:**
- **Cost-effective**: $16/month saves you $14 vs Standard
- **Sufficient**: 250MB >> 17MB your current needs  
- **Performance**: Full Redis speed for caching and trending
- **Risk**: Minimal - your app works fine without Redis, just slower

**Your trending features and search caching will work perfectly with Basic C0!** The only difference is no SLA guarantee, but for a startup, the cost savings make sense.

You can always upgrade to Standard C0 later ($30/month) when you want production SLA and automatic failover. 🚀