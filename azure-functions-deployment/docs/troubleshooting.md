# 🔍 Troubleshooting Guide - Azure Functions + Vercel

## 🚨 Problemas Comuns e Soluções

### 1. Azure Functions não inicia

**Sintomas:**
- Functions retorna erro 500
- Logs mostram "Function host not running"
- Timeout ao acessar endpoints

**Soluções:**
```bash
# Verificar status do Functions App
az functionapp show \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api

# Verificar logs
az webapp log tail \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api

# Reiniciar Functions App
az functionapp restart \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api
```

**Causas comuns:**
- Environment variables incorretas
- Dependências faltando no requirements.txt
- Timeout de inicialização

### 2. Erro de Conexão com Database

**Sintomas:**
- Erro "connection refused"
- Timeout ao conectar com PostgreSQL
- Health check falha no database

**Soluções:**
```bash
# Verificar firewall rules
az postgres flexible-server firewall-rule list \
  --resource-group musical-instruments-rg \
  --name musical-instruments-db

# Adicionar IP atual se necessário
az postgres flexible-server firewall-rule create \
  --resource-group musical-instruments-rg \
  --name musical-instruments-db \
  --rule-name allow-current-ip \
  --start-ip-address $(curl -s ifconfig.me) \
  --end-ip-address $(curl -s ifconfig.me)

# Verificar connection string
az functionapp config appsettings list \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api \
  --query "[?name=='DATABASE_URL'].value"
```

**Causas comuns:**
- Firewall bloqueando conexão
- Connection string incorreta
- SSL settings incompatíveis

### 3. Erro de Conexão com Redis

**Sintomas:**
- Erro "Redis connection failed"
- Cache não funcionando
- Health check falha no Redis

**Soluções:**
```bash
# Verificar Redis status
az redis show \
  --resource-group musical-instruments-rg \
  --name musical-instruments-redis

# Obter connection string
az redis show-connection-string \
  --resource-group musical-instruments-rg \
  --name musical-instruments-redis

# Verificar SSL settings
az redis firewall-rules list \
  --resource-group musical-instruments-rg \
  --name musical-instruments-redis
```

**Causas comuns:**
- Connection string incorreta
- SSL settings incompatíveis
- Redis service indisponível

### 4. CORS Issues

**Sintomas:**
- Erro "CORS policy" no browser
- Frontend não consegue acessar API
- Preflight requests falhando

**Soluções:**
```bash
# Configurar CORS no Functions
az functionapp cors add \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api \
  --allowed-origins "https://your-vercel-domain.vercel.app"

# Verificar CORS configurado
az functionapp cors show \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api
```

**Configuração manual no código:**
```python
# Adicionar headers CORS manualmente
def add_cors_headers(response):
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
    return response
```

### 5. Timeout Issues

**Sintomas:**
- Requests demoram muito
- Timeout após 10 minutos
- Cold start muito lento

**Soluções:**
```bash
# Verificar configuração de timeout
az functionapp config show \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api \
  --query "functionTimeout"

# Aumentar timeout (se necessário)
az functionapp config set \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api \
  --function-timeout "00:10:00"
```

**Otimizações:**
- Usar cache Redis para queries pesadas
- Implementar paginação
- Otimizar queries de banco

### 6. Memory Issues

**Sintomas:**
- Erro "out of memory"
- Functions crashando
- Performance degradada

**Soluções:**
```bash
# Verificar uso de memória
az monitor metrics list \
  --resource-group musical-instruments-rg \
  --resource-type "Microsoft.Web/sites" \
  --resource-name musical-instruments-api \
  --metric "MemoryPercentage" \
  --interval PT1M
```

**Otimizações:**
- Limpar cache Redis periodicamente
- Otimizar queries de banco
- Implementar lazy loading

### 7. Rate Limiting

**Sintomas:**
- Erro 429 "Too Many Requests"
- Requests sendo rejeitados
- Performance inconsistente

**Soluções:**
```bash
# Verificar configurações de rate limiting
az functionapp config show \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api \
  --query "http"
```

**Implementação de rate limiting:**
```python
from .utils.redis_client import check_rate_limit

def api_endpoint(req: func.HttpRequest) -> func.HttpResponse:
    # Rate limiting por IP
    client_ip = req.headers.get('X-Forwarded-For', 'unknown')
    
    if not check_rate_limit(client_ip, limit=100, window=60):
        return func.HttpResponse(
            "Rate limit exceeded",
            status_code=429
        )
    
    # Continuar com a lógica normal
    return process_request(req)
```

### 8. Environment Variables

**Sintomas:**
- Variáveis não encontradas
- Configurações incorretas
- Secrets expostos

**Soluções:**
```bash
# Listar todas as variáveis
az functionapp config appsettings list \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api

# Atualizar variável específica
az functionapp config appsettings set \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api \
  --settings \
    NEW_VARIABLE="new_value"

# Remover variável
az functionapp config appsettings delete \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api \
  --setting-names "OLD_VARIABLE"
```

### 9. Deploy Issues

**Sintomas:**
- Deploy falha
- Código não atualiza
- Functions não refletem mudanças

**Soluções:**
```bash
# Verificar status do deploy
az functionapp deployment list \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api

# Forçar novo deploy
func azure functionapp publish musical-instruments-api --force

# Verificar logs de deploy
az functionapp log deployment show \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api
```

### 10. Monitoring e Logs

**Comandos úteis:**
```bash
# Logs em tempo real
az webapp log tail \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api

# Baixar logs
az webapp log download \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api

# Ver métricas
az monitor metrics list \
  --resource-group musical-instruments-rg \
  --resource-type "Microsoft.Web/sites" \
  --resource-name musical-instruments-api \
  --metric "Requests" \
  --interval PT1H
```

## 🔧 Debug Local

### 1. Executar Functions Localmente
```bash
# Instalar Azure Functions Core Tools
npm install -g azure-functions-core-tools@4

# Executar localmente
func start

# Testar endpoints
curl http://localhost:7071/api/health
```

### 2. Configurar local.settings.json
```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "DATABASE_URL": "your-local-database-url",
    "REDIS_CONNECTION_STRING": "redis://localhost:6379"
  }
}
```

### 3. Debug com VS Code
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Attach to Python Functions",
      "type": "python",
      "request": "attach",
      "port": 9091,
      "host": "localhost",
      "pathMappings": [
        {
          "localRoot": "${workspaceFolder}",
          "remoteRoot": "."
        }
      ]
    }
  ]
}
```

## 📞 Suporte

### Recursos Úteis:
- [Azure Functions Documentation](https://docs.microsoft.com/en-us/azure/azure-functions/)
- [Azure CLI Reference](https://docs.microsoft.com/en-us/cli/azure/)
- [Azure Monitor](https://docs.microsoft.com/en-us/azure/azure-monitor/)
- [Application Insights](https://docs.microsoft.com/en-us/azure/azure-monitor/app/app-insights-overview)

### Logs de Erro Comuns:
- **500 Internal Server Error**: Verificar logs do Functions
- **404 Not Found**: Verificar rotas e configuração
- **403 Forbidden**: Verificar CORS e autenticação
- **429 Too Many Requests**: Implementar rate limiting
- **502 Bad Gateway**: Verificar dependências e timeouts
