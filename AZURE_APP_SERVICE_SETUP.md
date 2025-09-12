# Azure App Service Authentication Setup

## Visão Geral

Implementamos autenticação via **Azure App Service Authentication** para proteger a área administrativa (`/admin`). Apenas você, como administrador, terá acesso ao painel de gerenciamento do blog.

## 🚀 Configuração Completa

### 1. Backend Setup

#### Arquivos Criados:
- `backend/app/middleware/azure_auth.py` - Middleware de autenticação
- `backend/app/api/v1/admin.py` - Endpoints administrativos protegidos

#### Variáveis de Ambiente:
```env
# Email do administrador (seu email)
ADMIN_EMAIL=seu-email@dominio.com

# Múltiplos admins (opcional)
ADMIN_EMAILS=admin1@dominio.com,admin2@dominio.com

# Ambiente (development para testes locais)
ENVIRONMENT=production

# OpenAI para geração de blog
OPENAI_API_KEY=sua-chave-openai
```

### 2. Frontend Setup

#### Página Administrativa:
- `frontend/pages/admin/index.tsx` - Página principal do admin
- Autenticação automática via Azure AD
- Redirecionamento para login se não autenticado
- Verificação de permissões de admin

### 3. Azure App Service Configuration

#### Habilitar Authentication/Authorization no Azure:

1. **No Portal do Azure**, vá para seu App Service
2. **Authentication/Authorization** → **On**
3. **Action when request is not authenticated** → "Log in with Azure Active Directory"
4. **Authentication Providers** → **Azure Active Directory**

#### Configurar Azure AD:

```json
{
  "clientId": "sua-app-id",
  "issuer": "https://sts.windows.net/seu-tenant-id/",
  "allowedAudiences": [
    "sua-app-id",
    "https://seu-app.azurewebsites.net"
  ]
}
```

#### URLs de Login/Logout:
- **Login**: `https://seu-app.azurewebsites.net/.auth/login/aad`
- **Logout**: `https://seu-app.azurewebsites.net/.auth/logout`
- **User Info**: `https://seu-app.azurewebsites.net/.auth/me`

## 📚 Protected Documentation

### API Documentation Access

The API documentation is now protected and only accessible to authenticated admin users:

- **Frontend**: https://seu-app.azurewebsites.net/docs
- **Direct API**: https://seu-app.azurewebsites.net/api/v1/docs/
- **ReDoc**: https://seu-app.azurewebsites.net/api/v1/docs/redoc
- **OpenAPI Schema**: https://seu-app.azurewebsites.net/api/v1/docs/openapi.json

### Security Features:
✅ **Azure AD Authentication**: Same authentication as /admin  
✅ **Admin-Only Access**: Only users in ADMIN_EMAIL can access  
✅ **Interactive Testing**: Full Swagger UI with authentication  
✅ **Complete Schema**: All endpoints documented with examples  
✅ **Security Info**: Authentication schemes and rate limits documented  

## 🔐 Como Funciona

### 1. Fluxo de Autenticação
1. Usuário acessa `/admin`
2. Azure App Service verifica autenticação
3. Se não autenticado → redireciona para Azure AD
4. Após login → verifica se o email é admin
5. Se admin → acesso liberado
6. Se não admin → acesso negado

### 2. Headers Injetados pelo Azure
```javascript
// Headers automaticamente adicionados pelo Azure App Service
{
  'X-MS-CLIENT-PRINCIPAL-NAME': 'usuario@dominio.com',
  'X-MS-CLIENT-PRINCIPAL-ID': 'user-id',
  'X-MS-CLIENT-PRINCIPAL': 'base64-encoded-user-info'
}
```

### 3. Verificação de Admin
```python
# Verifica se o email é admin
user_email = request.headers.get('X-MS-CLIENT-PRINCIPAL-NAME')
is_admin = user_email.lower() in allowed_admins
```

## 📁 Estrutura da API Admin

### Endpoints Protegidos:
```
# Admin Dashboard
GET  /api/v1/admin/user-info           # Informações do usuário
GET  /api/v1/admin/stats               # Estatísticas do dashboard
GET  /api/v1/admin/blog/posts          # Posts para gerenciamento
POST /api/v1/admin/blog/generate       # Gerar post com AI
GET  /api/v1/admin/blog/templates      # Templates de geração
GET  /api/v1/admin/blog/generation-history  # Histórico de geração
GET  /api/v1/admin/system/health       # Status do sistema

# Batch API Endpoints
POST /api/v1/admin/blog/batch/create        # Criar batch
POST /api/v1/admin/blog/batch/{id}/upload   # Upload para Azure
POST /api/v1/admin/blog/batch/{id}/start    # Iniciar job
GET  /api/v1/admin/blog/batch/{id}/status   # Verificar status
POST /api/v1/admin/blog/batch/{id}/download # Download resultados
POST /api/v1/admin/blog/batch/process       # Processar resultados
GET  /api/v1/admin/blog/batches             # Listar batches

# Protected Documentation
GET  /api/v1/docs/                     # Swagger UI (protected)
GET  /api/v1/docs/redoc                # ReDoc UI (protected)  
GET  /api/v1/docs/openapi.json         # OpenAPI schema (protected)
GET  /api/v1/docs/health               # Docs health check
```

## 🌐 Configuração Passo a Passo

### 1. Azure Portal Setup

**Authentication/Authorization:**
```yaml
Plataforma: Azure App Service
Provider: Azure Active Directory
Mode: Express (recomendado)
Permissions: Sign in and read user profile
```

**Advanced Settings:**
```json
{
  "unauthenticatedClientAction": "RedirectToLoginPage",
  "defaultProvider": "AzureActiveDirectory",
  "tokenStore": {
    "enabled": true
  }
}
```

### 2. Backend Deployment

**Update your main.py:**
```python
from app.api.v1 import admin
from app.middleware.azure_auth import azure_auth

app.include_router(admin.router, prefix="/api/v1")
```

### 3. Environment Variables

**Azure App Service Configuration:**
```bash
az webapp config appsettings set \
  --name seu-app \
  --resource-group seu-grupo \
  --settings \
    ADMIN_EMAIL=seu-email@dominio.com \
    ENVIRONMENT=production \
    OPENAI_API_KEY=sua-chave
```

## 🔧 Desenvolvimento Local

### Teste sem Azure AD:
```env
# .env.local
ENVIRONMENT=development
ADMIN_EMAIL=admin@localhost
```

### Simular Azure Headers:
```javascript
// Para testes locais
const headers = {
  'X-MS-CLIENT-PRINCIPAL-NAME': 'admin@localhost'
};
```

## 🛡️ Recursos de Segurança

### 1. Proteção de Rotas
- `/admin/*` → Protegido pelo Azure AD
- Verificação automática de admin
- Logout seguro via Azure

### 2. Logging & Auditoria
```python
logger.info(f"Admin access granted to {user_info['email']} from IP: {request.client.host}")
logger.warning(f"Non-admin user {email} attempted admin access")
```

### 3. Headers de Segurança
```python
# Headers injetados automaticamente pelo Azure
X-MS-CLIENT-PRINCIPAL-NAME: email do usuário
X-MS-CLIENT-PRINCIPAL-ID: ID único
X-MS-CLIENT-PRINCIPAL: dados completos do usuário
```

## 📊 Dashboard Admin Features

### Estatísticas:
- Total de posts criados
- Posts gerados por AI
- Visualizações totais
- Taxa de sucesso da IA

### Gerenciamento:
- Criar posts manualmente
- Gerar posts com IA
- Visualizar histórico de geração
- Status do sistema

### Templates de IA:
- Buying Guides
- Product Reviews  
- Product Comparisons
- Tutorials
- Historical Articles

## 🚀 Deploy Instructions

### 1. Build & Deploy
```bash
# Frontend
npm run build
npm run export  # Se usando static export

# Backend
pip install -r requirements.txt
```

### 2. Azure App Service Settings
```bash
# Configurar autenticação
az webapp auth update \
  --name seu-app \
  --resource-group seu-grupo \
  --enabled true \
  --action LoginWithAzureActiveDirectory

# Configurar provider
az webapp auth microsoft update \
  --name seu-app \
  --resource-group seu-grupo \
  --client-id sua-app-id \
  --issuer https://sts.windows.net/seu-tenant-id/
```

## 🔍 Troubleshooting

### Problema: "Authentication Required"
**Solução:** Verificar se Azure AD está configurado corretamente

### Problema: "Admin Access Required" 
**Solução:** Verificar se seu email está em `ADMIN_EMAIL`

### Problema: Headers não aparecem
**Solução:** Verificar se Authentication está habilitado no App Service

### Teste de Headers:
```bash
curl -H "X-MS-CLIENT-PRINCIPAL-NAME: admin@dominio.com" \
  https://seu-app.azurewebsites.net/api/v1/admin/user-info
```

## 🎯 Vantagens desta Implementação

✅ **Zero Configuration** - Azure cuida da autenticação  
✅ **Enterprise Security** - Integração com Azure AD  
✅ **Single Sign-On** - Login único com Microsoft  
✅ **Automatic Headers** - Headers de usuário injetados automaticamente  
✅ **No Token Management** - Azure gerencia tokens  
✅ **Audit Logs** - Logs completos no Azure  
✅ **Cost Effective** - Incluído no App Service  

Agora você tem acesso seguro e profissional ao painel administrativo via `/admin` com autenticação Azure AD!