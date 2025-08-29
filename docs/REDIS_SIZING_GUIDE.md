# Azure Cache for Redis - Sizing Guide

## 📊 Usage Analysis for getyourmusicgear.com

### **Current Redis Usage Patterns:**

#### **1. Search Caching**
- **Key Pattern**: `search:{hash}:{limit}`
- **Data Size**: ~2-5KB per search result (JSON product data)
- **TTL**: 5 minutes
- **Estimated Keys**: 500-1000 unique searches per day
- **Storage**: ~2-5MB for search cache

#### **2. Trending System (NEW)**
- **View Tracking**: `views:product:hour:{timestamp}` 
- **Comparison Tracking**: `comparisons:pair`, `comparisons:individual`
- **Cache Results**: `trending:instruments:{category}:{limit}`
- **Data Size**: ~1KB per hourly view set, ~10KB per trending result
- **TTL**: 1-24 hours
- **Storage**: ~5-10MB for trending data

#### **3. Autocomplete/Suggestions**
- **Key Pattern**: `suggestions:{hash}`
- **Data Size**: ~500B per suggestion set
- **TTL**: 5 minutes  
- **Storage**: ~1-2MB for suggestions

### **Total Estimated Storage Need**: 8-17MB active data

## 🏷️ **Azure Cache for Redis SKU Recommendations**

### **🥉 Basic Tier (Development/Testing)**
```
SKU: Basic C0
Memory: 250MB
Price: ~$16/month
Pros: Cheapest option
Cons: No SLA, no persistence, single node
```
**Verdict**: ✅ Good for development, not for production

### **🥈 Standard C0 (Recommended - Small Production)** 
```
SKU: Standard C0  
Memory: 250MB
Price: ~$30/month
Features:
- 99.9% SLA
- Master/Replica setup
- Backup/Restore capability
- SSL/TLS encryption
```
**Verdict**: ✅ **RECOMMENDED** - Perfect for your usage (17MB << 250MB)

### **🥇 Standard C1 (Future Growth)**
```
SKU: Standard C1
Memory: 1GB  
Price: ~$55/month
Features: Same as C0 but 4x memory
```
**Verdict**: ⚠️ Overkill initially, good for scaling

### **💎 Premium Options**
```
SKU: Premium P1
Memory: 6GB
Price: ~$250/month
Features: Clustering, persistence, advanced security
```
**Verdict**: ❌ Way overkill for your needs

## 🎯 **Specific Recommendation for Your Project**

### **Start with Standard C0 (250MB)**

**Why this is perfect:**
✅ **Memory**: 250MB >> 17MB needed (15x headroom)
✅ **SLA**: 99.9% uptime for production 
✅ **Redundancy**: Master/replica setup
✅ **Cost**: Only ~$30/month
✅ **Features**: SSL, backup, monitoring included
✅ **Scalability**: Easy to upgrade if needed

## 📈 **Growth Projections**

### **Current State** (45 products, starting traffic)
- **Storage Needed**: 8-17MB
- **Keys**: ~1,500 active keys
- **Recommendation**: Standard C0 (250MB)

### **6 Months** (More products, growing traffic)
- **Storage Needed**: 25-50MB  
- **Keys**: ~5,000 active keys
- **Recommendation**: Still Standard C0 (plenty of headroom)

### **1 Year** (Established traffic, full product catalog)
- **Storage Needed**: 50-100MB
- **Keys**: ~10,000 active keys  
- **Recommendation**: Consider Standard C1 (1GB) for comfort

## 🛠️ **Azure Setup Commands**

### **Create Redis Cache**
```bash
# Create Standard C0 Redis Cache
az redis create \
  --name getyourmusicgear-redis \
  --resource-group getyourmusicgear-rg \
  --location eastus \
  --sku Standard \
  --vm-size C0 \
  --enable-non-ssl-port false
```

### **Get Connection Details**
```bash
# Get Redis connection string
az redis list-keys \
  --name getyourmusicgear-redis \
  --resource-group getyourmusicgear-rg
```

### **Connection String Format**
```bash
REDIS_URL=rediss://getyourmusicgear-redis.redis.cache.windows.net:6380?ssl_cert_reqs=required&password=your-redis-key
```

## 💰 **Cost Analysis**

### **Monthly Costs (US East)**
| SKU | Memory | Price/Month | Annual Cost |
|-----|---------|-------------|-------------|
| Basic C0 | 250MB | $16 | $192 |
| **Standard C0** | **250MB** | **$30** | **$360** |
| Standard C1 | 1GB | $55 | $660 |
| Premium P1 | 6GB | $250 | $3,000 |

**Recommendation: Standard C0 at $30/month = $360/year**

## 🔧 **Configuration Settings**

### **Redis Configuration for Your Use Case**
```bash
# In Azure Portal Redis Configuration:
maxmemory-policy: allkeys-lru  # Evict least recently used keys
timeout: 0                     # No idle timeout
tcp-keepalive: 300            # Keep connections alive
```

### **Application Settings (Azure Functions)**
```bash
REDIS_URL=rediss://getyourmusicgear-redis.redis.cache.windows.net:6380?ssl_cert_reqs=required&password=your-key
REDIS_SSL=true
REDIS_MAX_CONNECTIONS=20
```

## 📊 **Monitoring Metrics to Watch**

### **Key Metrics in Azure Portal:**
1. **Memory Usage** - Should stay well under 250MB
2. **Connected Clients** - Monitor connection count
3. **Cache Hit Rate** - Should be >80% for good performance
4. **Operations/Second** - Track request volume
5. **Network In/Out** - Monitor bandwidth usage

### **Alerts to Set:**
- Memory usage > 80% (200MB)
- Connected clients > 50
- Cache hit rate < 70%
- High error rate

## 🚀 **Implementation Priority**

### **Phase 1: Basic Setup**
1. Create Standard C0 Redis cache
2. Configure connection in Azure Functions
3. Deploy existing search caching
4. Monitor basic metrics

### **Phase 2: Trending Features**
1. Deploy trending service
2. Add view tracking to frontend
3. Monitor cache performance
4. Optimize TTL values based on usage

### **Phase 3: Optimization**  
1. Analyze cache hit rates
2. Fine-tune TTL values
3. Add more sophisticated caching
4. Consider upgrade if needed

## 🎯 **Final Recommendation**

**Start with Azure Cache for Redis Standard C0:**
- **Memory**: 250MB (15x your current needs)
- **Cost**: $30/month ($360/year)
- **Features**: Production SLA, redundancy, SSL, backups
- **Scalability**: Easy upgrade path to C1 (1GB) when needed

This gives you excellent performance for trending features and search caching while staying cost-effective. You can always scale up later as traffic grows!

**The cost is minimal compared to the performance benefits Redis provides for your search and trending features.** 🎵⚡