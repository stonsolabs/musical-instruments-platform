# 🔴 Redis Usage Guide - Azure Cache for Redis

## 📋 Visão Geral

O Azure Cache for Redis será usado para:
- **Cache de produtos** (melhora performance)
- **Session storage** (sessões de usuário)
- **Rate limiting** (proteção contra spam)
- **Search cache** (cache de buscas)
- **Comparison cache** (cache de comparações)

## 🏗️ Configuração do Redis

### 1. Criar Azure Cache for Redis
```bash
# Criar Redis Cache
az redis create \
  --resource-group musical-instruments-rg \
  --name musical-instruments-redis \
  --location eastus \
  --sku Basic \
  --vm-size c0
```

### 2. Obter Connection String
```bash
# Obter connection string
az redis show-connection-string \
  --resource-group musical-instruments-rg \
  --name musical-instruments-redis
```

### 3. Configurar no Azure Functions
```json
{
  "REDIS_CONNECTION_STRING": "redis://musical-instruments-redis.redis.cache.windows.net:6380?ssl=True&password=YOUR_PASSWORD"
}
```

## 🔧 Implementação no Código

### 1. Redis Client Setup
```python
import redis
import json
import os

# Configurar Redis client
redis_client = redis.Redis.from_url(
    os.getenv("REDIS_CONNECTION_STRING"),
    decode_responses=True
)

# Testar conexão
def test_redis_connection():
    try:
        redis_client.ping()
        return True
    except:
        return False
```

### 2. Cache de Produtos
```python
# Cache de produtos populares
def get_popular_products():
    cache_key = "popular_products"
    
    # Tentar buscar do cache
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    # Se não estiver no cache, buscar do banco
    products = db.get_popular_products()
    
    # Salvar no cache por 1 hora
    redis_client.setex(cache_key, 3600, json.dumps(products))
    
    return products

# Cache de produto individual
def get_product_by_id(product_id: str):
    cache_key = f"product:{product_id}"
    
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    product = db.get_product(product_id)
    if product:
        redis_client.setex(cache_key, 1800, json.dumps(product))
    
    return product
```

### 3. Cache de Busca
```python
# Cache de resultados de busca
def search_products(query: str, filters: dict = None):
    # Criar chave única para a busca
    cache_key = f"search:{hash(f'{query}_{str(filters)}')}"
    
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    results = db.search_products(query, filters)
    
    # Cache por 30 minutos
    redis_client.setex(cache_key, 1800, json.dumps(results))
    
    return results
```

### 4. Cache de Comparação
```python
# Cache de comparação de produtos
def compare_products(product_ids: list):
    # Ordenar IDs para garantir chave única
    sorted_ids = sorted(product_ids)
    cache_key = f"compare:{'_'.join(sorted_ids)}"
    
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    comparison = db.compare_products(product_ids)
    
    # Cache por 2 horas
    redis_client.setex(cache_key, 7200, json.dumps(comparison))
    
    return comparison
```

### 5. Session Storage
```python
# Gerenciar sessões de usuário
def create_user_session(user_id: str, session_data: dict):
    session_key = f"session:{user_id}"
    redis_client.setex(session_key, 86400, json.dumps(session_data))  # 24 horas

def get_user_session(user_id: str):
    session_key = f"session:{user_id}"
    cached = redis_client.get(session_key)
    return json.loads(cached) if cached else None

def delete_user_session(user_id: str):
    session_key = f"session:{user_id}"
    redis_client.delete(session_key)
```

### 6. Carrinho de Compras
```python
# Cache do carrinho
def get_user_cart(user_id: str):
    cart_key = f"cart:{user_id}"
    cached = redis_client.get(cart_key)
    return json.loads(cached) if cached else []

def update_user_cart(user_id: str, cart_data: list):
    cart_key = f"cart:{user_id}"
    redis_client.setex(cart_key, 3600, json.dumps(cart_data))  # 1 hora

def clear_user_cart(user_id: str):
    cart_key = f"cart:{user_id}"
    redis_client.delete(cart_key)
```

### 7. Rate Limiting
```python
# Rate limiting por IP
def check_rate_limit(ip: str, limit: int = 100, window: int = 60):
    key = f"rate_limit:{ip}"
    
    # Incrementar contador
    current = redis_client.incr(key)
    
    # Se for a primeira requisição, definir expiração
    if current == 1:
        redis_client.expire(key, window)
    
    return current <= limit

# Usar no endpoint
def api_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    client_ip = req.headers.get('X-Forwarded-For', 'unknown')
    
    if not check_rate_limit(client_ip):
        return func.HttpResponse(
            "Rate limit exceeded",
            status_code=429
        )
    
    # Continuar com a lógica normal
    return process_request(req)
```

### 8. Cache de Categorias
```python
# Cache de categorias (mudam raramente)
def get_categories():
    cache_key = "categories"
    
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)
    
    categories = db.get_categories()
    
    # Cache por 24 horas
    redis_client.setex(cache_key, 86400, json.dumps(categories))
    
    return categories
```

## 🧹 Limpeza e Manutenção

### 1. Limpar Cache Expirando
```python
# Redis automaticamente remove chaves expiradas
# Mas podemos limpar manualmente se necessário

def clear_expired_cache():
    # Buscar todas as chaves
    keys = redis_client.keys("*")
    
    for key in keys:
        # Verificar se a chave ainda existe (não foi expirada)
        if not redis_client.exists(key):
            continue
        
        # Verificar TTL
        ttl = redis_client.ttl(key)
        if ttl == -1:  # Sem expiração
            continue
        
        # Se TTL < 0, a chave expirou
        if ttl < 0:
            redis_client.delete(key)
```

### 2. Estatísticas do Cache
```python
def get_cache_stats():
    info = redis_client.info()
    
    return {
        "total_connections_received": info.get("total_connections_received", 0),
        "total_commands_processed": info.get("total_commands_processed", 0),
        "keyspace_hits": info.get("keyspace_hits", 0),
        "keyspace_misses": info.get("keyspace_misses", 0),
        "used_memory_human": info.get("used_memory_human", "0B"),
        "connected_clients": info.get("connected_clients", 0)
    }

def get_cache_hit_rate():
    stats = get_cache_stats()
    hits = stats["keyspace_hits"]
    misses = stats["keyspace_misses"]
    total = hits + misses
    
    if total == 0:
        return 0
    
    return (hits / total) * 100
```

## 🔍 Monitoramento

### 1. Health Check
```python
def redis_health_check():
    try:
        redis_client.ping()
        return {"status": "healthy", "message": "Redis is working"}
    except Exception as e:
        return {"status": "unhealthy", "message": str(e)}
```

### 2. Logs de Cache
```python
import logging

logger = logging.getLogger(__name__)

def log_cache_operation(operation: str, key: str, success: bool):
    logger.info(f"Cache {operation}: {key} - {'SUCCESS' if success else 'FAILED'}")
```

## ⚡ Performance Tips

1. **Use pipeline** para múltiplas operações:
```python
pipe = redis_client.pipeline()
pipe.set("key1", "value1")
pipe.set("key2", "value2")
pipe.execute()
```

2. **Serialize eficientemente**:
```python
# Use msgpack para dados complexos
import msgpack

# Serializar
data = msgpack.packb(complex_data)
redis_client.set("key", data)

# Deserializar
cached = redis_client.get("key")
if cached:
    data = msgpack.unpackb(cached)
```

3. **Use hashes** para objetos:
```python
# Em vez de JSON, use hashes para objetos
redis_client.hset("user:123", mapping={
    "name": "John",
    "email": "john@example.com",
    "preferences": json.dumps(prefs)
})
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Connection timeout**:
   - Verificar connection string
   - Verificar firewall rules
   - Verificar SSL settings

2. **Memory issues**:
   - Monitorar uso de memória
   - Ajustar TTL das chaves
   - Limpar cache antigo

3. **Performance issues**:
   - Verificar hit rate
   - Otimizar queries
   - Usar pipeline quando possível
