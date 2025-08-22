# 🚀 Setup Guide - Azure Functions + Vercel

## 📋 Pré-requisitos

1. **Azure Account** com créditos
2. **Azure CLI** instalado
3. **Node.js** (para desenvolvimento local)
4. **Python** 3.8+ (para Azure Functions)
5. **Git** (para versionamento)

## 🏗️ Passo a Passo

### 1. Configurar Azure CLI
```bash
# Login no Azure
az login

# Verificar subscription
az account show

# Definir subscription (se necessário)
az account set --subscription "Your Subscription Name"
```

### 2. Criar Resource Group
```bash
# Criar resource group
az group create \
  --name musical-instruments-rg \
  --location eastus
```

### 3. Criar Azure Database for PostgreSQL
```bash
# Criar PostgreSQL server
az postgres flexible-server create \
  --resource-group musical-instruments-rg \
  --name musical-instruments-db \
  --location eastus \
  --admin-user postgres \
  --admin-password "YourSecurePassword123!" \
  --sku-name Standard_B1ms \
  --version 15 \
  --storage-size 32

# Criar database
az postgres flexible-server db create \
  --resource-group musical-instruments-rg \
  --server-name musical-instruments-db \
  --database-name musical_instruments

# Configurar firewall
az postgres flexible-server firewall-rule create \
  --resource-group musical-instruments-rg \
  --name musical-instruments-db \
  --rule-name allow-azure-services \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 0.0.0.0
```

### 4. Criar Azure Cache for Redis
```bash
# Criar Redis cache
az redis create \
  --resource-group musical-instruments-rg \
  --name musical-instruments-redis \
  --location eastus \
  --sku Basic \
  --vm-size c0

# Obter connection string
az redis show-connection-string \
  --resource-group musical-instruments-rg \
  --name musical-instruments-redis
```

### 5. Criar Azure Storage Account
```bash
# Criar storage account
az storage account create \
  --resource-group musical-instruments-rg \
  --name musicalinstrumentsstorage \
  --location eastus \
  --sku Standard_LRS \
  --kind StorageV2

# Criar container para imagens
az storage container create \
  --account-name musicalinstrumentsstorage \
  --name product-images \
  --public-access blob
```

### 6. Criar Azure Functions App
```bash
# Criar storage account para Functions
az storage account create \
  --resource-group musical-instruments-rg \
  --name musicalfunctionsstorage \
  --location eastus \
  --sku Standard_LRS

# Criar Functions App
az functionapp create \
  --resource-group musical-instruments-rg \
  --consumption-plan-location eastus \
  --runtime python \
  --runtime-version 3.9 \
  --functions-version 4 \
  --name musical-instruments-api \
  --storage-account musicalfunctionsstorage \
  --os-type linux
```

### 7. Configurar Environment Variables
```bash
# Configurar variáveis do Functions
az functionapp config appsettings set \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api \
  --settings \
    DATABASE_URL="postgresql+asyncpg://postgres:YourSecurePassword123!@musical-instruments-db.postgres.database.azure.com:5432/musical_instruments" \
    REDIS_CONNECTION_STRING="redis://musical-instruments-redis.redis.cache.windows.net:6380?ssl=True&password=YOUR_REDIS_PASSWORD" \
    AZURE_STORAGE_CONNECTION_STRING="DefaultEndpointsProtocol=https;AccountName=musicalinstrumentsstorage;AccountKey=YOUR_STORAGE_KEY;EndpointSuffix=core.windows.net" \
    AZURE_STORAGE_ACCOUNT_NAME="musicalinstrumentsstorage" \
    AZURE_STORAGE_CONTAINER_NAME="product-images" \
    ENVIRONMENT="production" \
    SECRET_KEY="your-secret-key-here" \
    OPENAI_API_KEY="your-openai-api-key" \
    AMAZON_ASSOCIATE_TAG="your-amazon-tag" \
    THOMANN_AFFILIATE_ID="your-thomann-id"
```

## 🔧 Desenvolvimento Local

### 1. Instalar Azure Functions Core Tools
```bash
# macOS
brew tap azure/functions
brew install azure-functions-core-tools@4

# Windows
npm install -g azure-functions-core-tools@4

# Linux
curl https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor > microsoft.gpg
sudo mv microsoft.gpg /etc/apt/trusted.gpg.d/microsoft.gpg
sudo sh -c 'echo "deb [arch=amd64] https://packages.microsoft.com/repos/microsoft-ubuntu-$(lsb_release -cs)-prod $(lsb_release -cs) main" > /etc/apt/sources.list.d/dotnetdev.list'
sudo apt-get update
sudo apt-get install azure-functions-core-tools-4
```

### 2. Configurar Projeto Local
```bash
# Criar projeto Functions
func init musical-instruments-api --python

# Instalar dependências
cd musical-instruments-api
pip install -r requirements.txt
```

### 3. Configurar local.settings.json
```json
{
  "IsEncrypted": false,
  "Values": {
    "FUNCTIONS_WORKER_RUNTIME": "python",
    "AzureWebJobsStorage": "UseDevelopmentStorage=true",
    "DATABASE_URL": "postgresql+asyncpg://postgres:password@localhost:5432/musical_instruments",
    "REDIS_CONNECTION_STRING": "redis://localhost:6379",
    "AZURE_STORAGE_CONNECTION_STRING": "DefaultEndpointsProtocol=https;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;BlobEndpoint=https://devstoreaccount1.blob.core.windows.net/;QueueEndpoint=https://devstoreaccount1.queue.core.windows.net/;TableEndpoint=https://devstoreaccount1.table.core.windows.net/;",
    "AZURE_STORAGE_ACCOUNT_NAME": "devstoreaccount1",
    "AZURE_STORAGE_CONTAINER_NAME": "product-images",
    "ENVIRONMENT": "development",
    "SECRET_KEY": "dev-secret-key",
    "OPENAI_API_KEY": "your-openai-api-key",
    "AMAZON_ASSOCIATE_TAG": "your-amazon-tag",
    "THOMANN_AFFILIATE_ID": "your-thomann-id"
  }
}
```

### 4. Executar Localmente
```bash
# Iniciar Functions localmente
func start

# Testar endpoints
curl http://localhost:7071/api/health
curl http://localhost:7071/api/products
```

## 🚀 Deploy

### 1. Deploy para Azure Functions
```bash
# Fazer login no Azure
az login

# Deploy
func azure functionapp publish musical-instruments-api
```

### 2. Verificar Deploy
```bash
# Verificar status
az functionapp show \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api

# Testar endpoint
curl https://musical-instruments-api.azurewebsites.net/api/health
```

## 🔄 Atualizar Frontend (Vercel)

### 1. Atualizar API URL
```bash
# No Vercel, atualizar environment variable
NEXT_PUBLIC_API_URL=https://musical-instruments-api.azurewebsites.net/api
```

### 2. Deploy Frontend
```bash
# Push para GitHub (se usando GitHub integration)
git add .
git commit -m "Update API URL to Azure Functions"
git push origin main

# Ou deploy manual
vercel --prod
```

## 📊 Monitoramento

### 1. Azure Application Insights
```bash
# Criar Application Insights
az monitor app-insights component create \
  --resource-group musical-instruments-rg \
  --app musical-instruments-insights \
  --location eastus \
  --kind web

# Conectar ao Functions
az functionapp config appsettings set \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api \
  --settings \
    APPINSIGHTS_INSTRUMENTATIONKEY="YOUR_INSTRUMENTATION_KEY"
```

### 2. Logs
```bash
# Ver logs em tempo real
az webapp log tail \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api

# Baixar logs
az webapp log download \
  --resource-group musical-instruments-rg \
  --name musical-instruments-api
```

## 🔍 Troubleshooting

### Problemas Comuns

1. **Functions não inicia**:
   - Verificar Python version
   - Verificar requirements.txt
   - Verificar local.settings.json

2. **Database connection**:
   - Verificar DATABASE_URL
   - Verificar firewall rules
   - Verificar SSL settings

3. **Redis connection**:
   - Verificar REDIS_CONNECTION_STRING
   - Verificar SSL settings
   - Verificar firewall rules

4. **CORS issues**:
   - Configurar CORS no Functions
   - Verificar origins permitidos

## ✅ Checklist Final

- [ ] Azure CLI configurado
- [ ] Resource group criado
- [ ] PostgreSQL configurado
- [ ] Redis configurado
- [ ] Storage account criado
- [ ] Functions App criado
- [ ] Environment variables configuradas
- [ ] Desenvolvimento local funcionando
- [ ] Deploy realizado
- [ ] Frontend atualizado
- [ ] Monitoramento configurado
- [ ] Testes realizados
