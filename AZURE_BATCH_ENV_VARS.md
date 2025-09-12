# Azure Batch Blog Generation - Environment Variables

## 🚀 Required Environment Variables for Azure App Service

Configure estas variáveis de ambiente no seu Azure App Service para habilitar a geração de blog posts em lote usando Azure OpenAI Batch API.

### 1. Azure OpenAI Configuration

```bash
# Azure OpenAI API Key
AZURE_OPENAI_API_KEY=your_azure_openai_api_key

# Azure OpenAI Endpoint
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# API Version (recomendado usar a mais recente)
AZURE_OPENAI_API_VERSION=2024-07-01-preview

# Deployment Name (o nome do seu modelo GPT-4.1)
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1
```

### 2. Azure Storage Configuration

**Opção A: Connection String (Recomendado)**
```bash
# Azure Storage Connection String
AZURE_STORAGE_CONNECTION_STRING=DefaultEndpointsProtocol=https;AccountName=yourstorageaccount;AccountKey=yourkey;EndpointSuffix=core.windows.net
```

**Opção B: Account Name + Key**
```bash
# Azure Storage Account Name
AZURE_STORAGE_ACCOUNT_NAME=yourstorageaccount

# Azure Storage Account Key
AZURE_STORAGE_ACCOUNT_KEY=your_storage_account_key
```

**Container Configuration**
```bash
# Container name for batch files (será criado automaticamente se não existir)
AZURE_STORAGE_CONTAINER=blog-batch-files
```

### 3. Admin Authentication

```bash
# Email do administrador (obrigatório)
ADMIN_EMAIL=seu-email@dominio.com

# Múltiplos admins (opcional)
ADMIN_EMAILS=admin1@dominio.com,admin2@dominio.com

# Environment
ENVIRONMENT=production
```

### 4. Database Configuration

```bash
# PostgreSQL Database URL
DATABASE_URL=postgresql://user:password@host:port/database
```

## 🔧 Como Configurar no Azure App Service

### Via Azure CLI:

```bash
# Configurar todas as variáveis de uma vez
az webapp config appsettings set \
  --name your-app-name \
  --resource-group your-resource-group \
  --settings \
    AZURE_OPENAI_API_KEY="your_azure_openai_api_key" \
    AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com" \
    AZURE_OPENAI_API_VERSION="2024-07-01-preview" \
    AZURE_OPENAI_DEPLOYMENT_NAME="gpt-4.1" \
    AZURE_STORAGE_CONNECTION_STRING="your_connection_string" \
    AZURE_STORAGE_CONTAINER="blog-batch-files" \
    ADMIN_EMAIL="seu-email@dominio.com" \
    ENVIRONMENT="production"
```

### Via Portal do Azure:

1. Vá para seu **App Service** no Portal do Azure
2. **Configuration** → **Application settings**
3. **+ New application setting** para cada variável
4. **Save** para aplicar as configurações

## 📁 Estrutura dos Arquivos no Azure Storage

```
blog-batch-files/
├── batch_files/
│   ├── blog_batch_20241201_143022.jsonl
│   ├── blog_batch_20241201_143022_metadata.json
│   └── ...
└── batch_results/
    ├── results_batch_abc123def456.jsonl
    ├── results_batch_xyz789abc123.jsonl
    └── ...
```

## 🔄 Workflow do Batch API

### 1. Criar Batch
```http
POST /api/v1/admin/blog/batch/create
```

### 2. Upload para Azure OpenAI
```http
POST /api/v1/admin/blog/batch/{batch_id}/upload
```

### 3. Iniciar Job
```http
POST /api/v1/admin/blog/batch/{file_id}/start
```

### 4. Monitorar Status
```http
GET /api/v1/admin/blog/batch/{azure_batch_id}/status
```

### 5. Download Resultados
```http
POST /api/v1/admin/blog/batch/{azure_batch_id}/download
```

### 6. Processar e Criar Posts
```http
POST /api/v1/admin/blog/batch/process
```

## 🛡️ Segurança e Permissões

### Azure Storage Permissions:
- **Blob Contributor** role para o App Service
- Ou usar **Storage Account Key** nas variáveis de ambiente

### Azure OpenAI Permissions:
- **Cognitive Services OpenAI Contributor** role
- Ou usar **API Key** diretamente

### Managed Identity (Opcional):
```bash
# Habilitar Managed Identity no App Service
az webapp identity assign \
  --name your-app-name \
  --resource-group your-resource-group

# Atribuir roles necessários
az role assignment create \
  --assignee <managed-identity-principal-id> \
  --role "Storage Blob Data Contributor" \
  --scope /subscriptions/<subscription-id>/resourceGroups/<rg>/providers/Microsoft.Storage/storageAccounts/<storage-account>
```

## 🧪 Desenvolvimento Local

### .env.local:
```bash
# Para testes locais
ENVIRONMENT=development
ADMIN_EMAIL=admin@localhost

# Azure services (usar as mesmas credenciais)
AZURE_OPENAI_API_KEY=your_key
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_API_VERSION=2024-07-01-preview
AZURE_OPENAI_DEPLOYMENT_NAME=gpt-4.1

# Storage local fallback será usado se não configurar Azure Storage
# AZURE_STORAGE_CONNECTION_STRING=...
```

## 📊 Monitoramento

### Logs Importantes:
```python
# Criação do batch
logger.info(f"Batch criado: {batch_name} com {len(batch_requests)} requests")

# Upload para Azure
logger.info(f"Arquivo uploadado: {file_upload_response.id}")

# Job iniciado
logger.info(f"Batch job criado: {batch_response.id}")

# Resultados processados
logger.info(f"Batch processado: {len(successful_posts)} sucessos, {len(failed_posts)} falhas")
```

### Azure Application Insights:
O App Service automaticamente enviará logs para Application Insights se configurado.

## 🚨 Troubleshooting

### Erro: "Azure Storage credentials not found"
**Solução**: Verificar se `AZURE_STORAGE_CONNECTION_STRING` ou (`AZURE_STORAGE_ACCOUNT_NAME` + `AZURE_STORAGE_ACCOUNT_KEY`) estão configurados.

### Erro: "OpenAI API key not configured"
**Solução**: Verificar se `AZURE_OPENAI_API_KEY` está configurado corretamente.

### Erro: "Batch not found"
**Solução**: Verificar se o `batch_id` existe na tabela `blog_batch_jobs`.

### Erro: "Admin access required"
**Solução**: Verificar se o email do usuário está em `ADMIN_EMAIL` ou `ADMIN_EMAILS`.

## 💰 Estimativa de Custos

### Azure OpenAI Batch API:
- **50% de desconto** comparado às chamadas individuais
- GPT-4: ~$15/1M tokens input, ~$30/1M tokens output
- Batch: ~$7.50/1M tokens input, ~$15/1M tokens output

### Azure Storage:
- **Hot tier**: ~$0.0184/GB/mês
- **Transações**: ~$0.0004/10,000 operações

### Exemplo de Uso:
- **100 blog posts/mês**
- **~2,000 tokens/post** = 200K tokens total
- **Custo estimado**: ~$3-5/mês (OpenAI) + ~$1/mês (Storage)

## ✅ Checklist de Configuração

- [ ] Azure OpenAI resource criado
- [ ] Deployment GPT-4.1 configurado
- [ ] Azure Storage Account criado
- [ ] Container `blog-batch-files` disponível (ou será criado automaticamente)
- [ ] Variáveis de ambiente configuradas no App Service
- [ ] Azure AD Authentication habilitado
- [ ] Admin email configurado
- [ ] Migrations do banco executadas
- [ ] Testes do endpoint `/api/v1/admin/user-info` funcionando

Agora você está pronto para usar o sistema de geração de blog posts em lote com Azure OpenAI Batch API! 🚀