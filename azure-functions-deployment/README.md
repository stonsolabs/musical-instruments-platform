# 🚀 Azure Functions + Vercel Deployment

## 📊 Arquitetura Híbrida

**Frontend**: Next.js no Vercel (mantém a simplicidade atual)  
**Backend**: FastAPI em Azure Functions (serverless)  
**Database**: Azure Database for PostgreSQL  
**Cache**: Azure Cache for Redis  
**Storage**: Azure Blob Storage (para imagens)

## 💰 Estimativa de Custos

| Serviço | Custo Mensal | Detalhes |
|---------|-------------|----------|
| Vercel | FREE | Frontend (mantém atual) |
| Azure Functions | FREE | 1M execuções/mês |
| PostgreSQL | $12/mês | Burstable B1ms |
| Redis Cache | $13/mês | Basic tier |
| Blob Storage | $2/mês | Standard LRS |
| **Total** | **~$27/mês** | **25 meses de créditos** |

## 🎯 Vantagens desta Abordagem

✅ **Mantém Vercel** - Simplicidade do frontend atual  
✅ **Serverless Backend** - Paga apenas pelo que usar  
✅ **Escalabilidade** - Azure Functions escala automaticamente  
✅ **Custo otimizado** - Aproveita melhor os créditos Azure  
✅ **Performance** - Redis dedicado para cache  
✅ **Flexibilidade** - Pode migrar frontend depois se quiser  

## 🔄 Como Funciona o Redis

### Cache de Produtos
```python
# Cache de produtos populares
redis_client.setex("popular_products", 3600, json.dumps(products))

# Cache de busca
redis_client.setex(f"search:{query}", 1800, json.dumps(results))

# Cache de comparação
redis_client.setex(f"compare:{product_ids}", 7200, json.dumps(comparison))
```

### Session Storage
```python
# Sessões de usuário
redis_client.setex(f"session:{user_id}", 86400, session_data)

# Carrinho de compras
redis_client.setex(f"cart:{user_id}", 3600, cart_data)
```

### Rate Limiting
```python
# Rate limiting por IP
redis_client.incr(f"rate_limit:{ip}")
redis_client.expire(f"rate_limit:{ip}", 60)
```

## 🏗️ Estrutura do Projeto

```
azure-functions-deployment/
├── README.md
├── functions/
│   ├── host.json
│   ├── local.settings.json
│   ├── requirements.txt
│   └── api/
│       ├── __init__.py
│       ├── products.py
│       ├── search.py
│       ├── compare.py
│       └── health.py
├── scripts/
│   ├── deploy-functions.sh
│   ├── setup-azure.sh
│   └── migrate-data.sh
└── docs/
    ├── setup-guide.md
    ├── redis-usage.md
    └── troubleshooting.md
```

## 🚀 Próximos Passos

1. **Configurar Azure Functions** para o backend
2. **Migrar FastAPI** para Azure Functions
3. **Configurar Redis** para cache
4. **Atualizar frontend** para usar Azure Functions
5. **Migrar dados** para Azure PostgreSQL

## 📋 Checklist de Migração

- [ ] Criar Azure Functions App
- [ ] Configurar PostgreSQL no Azure
- [ ] Configurar Redis Cache
- [ ] Migrar código FastAPI para Functions
- [ ] Configurar variáveis de ambiente
- [ ] Testar endpoints
- [ ] Atualizar frontend (Vercel)
- [ ] Migrar dados
- [ ] Configurar monitoramento
