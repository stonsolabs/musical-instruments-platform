# Protected API Documentation Setup

## 🚀 Overview

The API documentation is now fully protected using Azure App Service Authentication, ensuring only authorized admin users can access sensitive API information.

## 🔐 Security Implementation

### Frontend Protection
- **Route**: `/docs` - Protected Next.js page
- **Authentication Check**: Validates admin access via `/api/proxy/v1/admin/user-info`
- **Auto Redirect**: Automatically redirects to Azure AD login if not authenticated
- **Access Control**: Only users in `ADMIN_EMAIL` environment variable can access

### Backend Protection
- **API Route**: `/api/v1/docs/` - Protected FastAPI endpoints
- **Azure AD Integration**: Uses same Azure App Service Authentication as `/admin`
- **Admin Verification**: Requires `require_azure_admin` dependency
- **Multiple Formats**: Swagger UI, ReDoc, and OpenAPI JSON schema

## 📁 Files Created/Updated

### Frontend
```
frontend/pages/docs/index.tsx       # Protected docs page with iframe to backend
frontend/pages/admin/index.tsx      # Added API Docs link in header
```

### Backend  
```
backend/app/api/v1/docs.py         # Protected documentation endpoints
backend/app/main.py                 # Updated to include docs router
```

### Documentation
```
AZURE_APP_SERVICE_SETUP.md         # Updated with docs endpoints info
PROTECTED_DOCS_SETUP.md            # This comprehensive setup guide
```

## 🌐 Access URLs

### Production
- **Main Docs Page**: `https://seu-app.azurewebsites.net/docs`
- **Direct Swagger UI**: `https://seu-app.azurewebsites.net/api/v1/docs/`
- **ReDoc**: `https://seu-app.azurewebsites.net/api/v1/docs/redoc`
- **OpenAPI Schema**: `https://seu-app.azurewebsites.net/api/v1/docs/openapi.json`

### Development
- **Main Docs Page**: `http://localhost:3000/docs`
- **Direct Swagger UI**: `http://localhost:8000/api/v1/docs/`
- **ReDoc**: `http://localhost:8000/api/v1/docs/redoc`
- **OpenAPI Schema**: `http://localhost:8000/api/v1/docs/openapi.json`

## 🔧 API Endpoints Documentation

### Complete Endpoint Coverage

**Admin Dashboard:**
```
GET  /api/v1/admin/user-info              # User authentication info
GET  /api/v1/admin/stats                  # System statistics  
GET  /api/v1/admin/system/health          # System health check
```

**Blog Management:**
```
GET  /api/v1/admin/blog/posts             # List blog posts
POST /api/v1/admin/blog/generate          # Generate AI blog post
GET  /api/v1/admin/blog/templates         # Generation templates
GET  /api/v1/admin/blog/generation-history # AI generation history
```

**Azure Batch API:**
```
POST /api/v1/admin/blog/batch/create           # Create batch request
POST /api/v1/admin/blog/batch/{id}/upload      # Upload to Azure OpenAI
POST /api/v1/admin/blog/batch/{id}/start       # Start batch job
GET  /api/v1/admin/blog/batch/{id}/status      # Check job status
POST /api/v1/admin/blog/batch/{id}/download    # Download results
POST /api/v1/admin/blog/batch/process          # Process & create posts
GET  /api/v1/admin/blog/batches                # List all batches
```

**Public Blog API:**
```
GET  /api/v1/blog/posts                   # List published posts
GET  /api/v1/blog/posts/{slug}            # Get specific post
GET  /api/v1/blog/categories              # List categories
GET  /api/v1/blog/tags                    # List tags
```

**Product & Search API:**
```
GET  /api/v1/products                     # List products
GET  /api/v1/products/{id}                # Get product details
GET  /api/v1/search/autocomplete          # Search suggestions
POST /api/v1/compare                      # Compare products
GET  /api/v1/categories                   # List categories
GET  /api/v1/brands                       # List brands
```

## 🛡️ Security Features

### Authentication Flow
1. User accesses `/docs`
2. Frontend checks authentication via admin API
3. If not authenticated → redirect to `/.auth/login/aad`
4. If authenticated but not admin → access denied
5. If admin → access granted with full documentation

### Authorization Levels
- **Public Endpoints**: No authentication required
- **Standard API**: API key in `X-API-Key` header
- **Admin Endpoints**: Azure AD authentication + admin email verification
- **Documentation**: Admin-only access with Azure AD

### Security Headers
All documentation endpoints include security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `X-XSS-Protection: 1; mode=block`
- `Strict-Transport-Security` (production only)

## 📊 Documentation Features

### Interactive Testing
- **Swagger UI**: Full interactive API testing interface
- **Authentication Support**: Test endpoints with proper authentication
- **Request/Response Examples**: Complete examples for all endpoints
- **Schema Validation**: Real-time request validation

### Comprehensive Schema
- **Security Schemes**: API Key and Azure AD OAuth2 documented
- **Rate Limiting**: 1000 req/hour standard, 100 req/hour admin
- **Server Endpoints**: Both production and development URLs
- **Response Formats**: Detailed response schemas with examples

### User Experience
- **Admin Navigation**: Direct link from admin panel header
- **Error Handling**: Clear error messages for authentication issues
- **Responsive Design**: Works on desktop and mobile devices
- **Fast Loading**: Efficient iframe embedding with CDN resources

## 🧪 Testing & Validation

### Frontend Testing
```bash
# Test protected page access
curl -v http://localhost:3000/docs
# Should redirect to login if not authenticated

# Test with admin authentication
# Access /docs after logging in via /admin
```

### Backend Testing
```bash
# Test protected docs endpoint
curl -H "X-MS-CLIENT-PRINCIPAL-NAME: admin@domain.com" \
  http://localhost:8000/api/v1/docs/

# Test OpenAPI schema
curl -H "X-MS-CLIENT-PRINCIPAL-NAME: admin@domain.com" \
  http://localhost:8000/api/v1/docs/openapi.json
```

## 🚀 Production Deployment

### Azure App Service Configuration

The docs system automatically works with existing Azure AD setup:

1. **Authentication**: Uses same Azure AD as `/admin`
2. **Authorization**: Same `ADMIN_EMAIL` environment variable
3. **Security**: Same middleware and headers configuration
4. **Logging**: Integrated with existing audit logs

### Environment Requirements

No additional environment variables needed - uses existing setup:
- `ADMIN_EMAIL` or `ADMIN_EMAILS` - Admin access control
- `ENVIRONMENT=production` - Security configuration
- Azure AD authentication enabled on App Service

## 🔍 Monitoring & Logs

### Access Logging
```python
# Documentation access logged with admin info
logger.info(f"Generated OpenAPI schema for admin {admin['email']}")
logger.info(f"Documentation accessed by admin {admin['email']}")
```

### Security Monitoring
- Failed authentication attempts logged
- Unauthorized access attempts recorded
- Admin access patterns tracked
- API usage statistics available

## ✅ Verification Checklist

### Frontend Setup
- [ ] `/docs` page created and protected
- [ ] Authentication check implemented
- [ ] Azure AD redirect configured
- [ ] Error handling for unauthorized access
- [ ] Admin panel navigation link added

### Backend Setup
- [ ] Protected docs router created (`/api/v1/docs/`)
- [ ] Azure AD authentication middleware applied
- [ ] Swagger UI, ReDoc, and OpenAPI endpoints available
- [ ] Complete API schema with security information
- [ ] Admin access logging implemented

### Security Verification
- [ ] Unauthenticated access blocked
- [ ] Non-admin users blocked
- [ ] Admin users can access all documentation
- [ ] Security headers applied
- [ ] Production configuration disabled default docs

### Documentation Quality
- [ ] All endpoints documented with examples
- [ ] Authentication schemes properly defined
- [ ] Rate limiting information included
- [ ] Server URLs configured for both environments
- [ ] Interactive testing works correctly

## 🎯 Benefits

### Security
✅ **Zero Public Exposure**: No API docs visible to unauthorized users  
✅ **Enterprise Authentication**: Azure AD integration  
✅ **Granular Access Control**: Admin-only access  
✅ **Audit Trail**: Complete access logging  

### Developer Experience
✅ **Interactive Testing**: Full Swagger UI functionality  
✅ **Complete Coverage**: All endpoints documented  
✅ **Easy Access**: Direct link from admin panel  
✅ **Multiple Formats**: Swagger UI, ReDoc, and JSON schema  

### Operational
✅ **No Additional Config**: Uses existing authentication setup  
✅ **Automatic Updates**: Schema updates with code changes  
✅ **Performance Optimized**: CDN-hosted UI resources  
✅ **Production Ready**: Secure deployment configuration  

Your API documentation is now fully protected and ready for production use! 🚀