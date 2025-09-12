# Admin Authentication Setup Guide

## Overview

The blog management system is now secured with admin-only access control. Only users with the correct admin key can access the BlogManager, AI Generator, and other admin features.

## Backend Setup

### 1. Environment Variables

Add these environment variables to your backend configuration:

**Production (.env):**
```env
# Regular API key for general access
API_KEY=your-regular-api-key

# Admin-only access key (keep this secure!)
ADMIN_API_KEY=your-super-secret-admin-key-change-this-immediately

# Admin email (optional, for logging)
ADMIN_EMAIL=admin@getyourmusicgear.com

# OpenAI API key for AI blog generation
OPENAI_API_KEY=your-openai-api-key
```

**Development (.env.local):**
```env
API_KEY=dev-api-key
ADMIN_API_KEY=dev-admin-key-123456789
ADMIN_EMAIL=admin@localhost
OPENAI_API_KEY=your-openai-api-key
```

### 2. Admin Key Security

**Important Security Notes:**
- Use a strong, randomly generated admin key (at least 32 characters)
- Keep the admin key secret and don't commit it to version control
- Consider using different admin keys for different environments
- The admin key is stored in sessionStorage (cleared when browser closes)

**Generate a secure admin key:**
```bash
# Linux/macOS
openssl rand -base64 32

# Or use Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### 3. Protected Endpoints

The following endpoints now require admin authentication:

- `POST /blog/posts` - Create blog post manually
- `POST /blog/templates` - Create generation templates  
- `POST /blog/generate` - Generate AI blog posts
- `GET /blog/generation-history` - View generation history
- `GET /blog/ai-posts/{id}` - Get AI post details

**Authentication Method:**
Send the admin key in the `X-Admin-Key` header:

```javascript
fetch('/api/proxy/v1/blog/generate', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Admin-Key': 'your-admin-key-here'
  },
  body: JSON.stringify(requestData)
});
```

## Frontend Setup

### 1. Admin Login Flow

1. User visits BlogManager component
2. If not authenticated, shows AdminLogin form
3. User enters admin key
4. System validates key by testing protected endpoint
5. If valid, key is stored in sessionStorage
6. User gains access to admin features

### 2. Session Management

- **Storage**: Admin key stored in `sessionStorage` (cleared on browser close)
- **Validation**: Automatic validation on page load
- **Logout**: Manual logout button clears session
- **Auto-logout**: Session expires when browser closes

### 3. Component Protection

Protected components automatically redirect to login:

```typescript
// BlogManager checks authentication
const { isAdmin, isLoading } = useAuth();

if (!isAdmin) {
  return <AdminLogin onSuccess={() => {}} />;
}
```

## Usage Instructions

### For the Site Owner (Admin)

1. **Set up your admin key** in the backend environment variables
2. **Access the blog manager** at `/admin/blog` (or wherever you mount BlogManager)
3. **Enter your admin key** in the login form
4. **Start managing blogs** - create posts, generate with AI, view history

### For Developers

1. **Use the `useAuth` hook** to check admin status in components
2. **Add admin protection** to new admin-only features:

```typescript
import { useAuth } from '../hooks/useAuth';

function MyAdminComponent() {
  const { isAdmin, getAuthHeaders } = useAuth();
  
  if (!isAdmin) {
    return <AdminLogin onSuccess={() => {}} />;
  }
  
  // Use getAuthHeaders() for API calls
  const response = await fetch('/api/admin-endpoint', {
    headers: getAuthHeaders()
  });
}
```

## API Authentication Examples

### Frontend API Calls

```typescript
import { useAuth } from '../hooks/useAuth';

function BlogAdminPanel() {
  const { getAuthHeaders } = useAuth();
  
  const createPost = async (postData) => {
    const response = await fetch('/api/proxy/v1/blog/posts', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        ...getAuthHeaders() // Automatically adds X-Admin-Key if authenticated
      },
      body: JSON.stringify(postData)
    });
  };
}
```

### Direct API Calls (External Tools)

```bash
# Create a blog post via API
curl -X POST https://your-api.com/api/v1/blog/posts \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: your-admin-key" \
  -d '{"title": "Test Post", "content": "Content here"}'

# Generate AI blog post
curl -X POST https://your-api.com/api/v1/blog/generate \
  -H "Content-Type: application/json" \
  -H "X-Admin-Key: your-admin-key" \
  -d '{"template_id": 1, "target_word_count": 800}'
```

## Security Features

### 1. Access Control
- Admin key required for all blog management operations
- Automatic session validation on component mount
- Graceful handling of expired/invalid sessions

### 2. Logging & Monitoring
- Admin access attempts logged with IP addresses
- Failed authentication attempts tracked
- Generation history includes admin context

### 3. Error Handling
- Clear error messages for invalid credentials
- Automatic retry on network failures
- Secure error responses (no sensitive data leaked)

## Troubleshooting

### Common Issues

**"Admin access required" error:**
- Check that `ADMIN_API_KEY` is set in backend environment
- Verify the key matches what you're entering in login form
- Check browser network tab for 401/403 responses

**"Invalid admin credentials":**
- Admin key doesn't match backend `ADMIN_API_KEY`
- Key might contain extra spaces or characters
- Environment variable not loaded properly

**Session keeps expiring:**
- SessionStorage is cleared when browser closes (by design)
- Use "Remember me" functionality if you implement persistent storage
- Check for JavaScript errors in browser console

### Development Testing

```bash
# Test admin authentication
curl -H "X-Admin-Key: dev-admin-key-123456789" \
  http://localhost:8000/api/v1/blog/generation-history?limit=1

# Should return 200 OK if authentication works
# Should return 401/403 if authentication fails
```

## Extending Admin Features

To add new admin-only features:

1. **Backend**: Use `require_admin` dependency
```python
@router.post("/admin/new-feature")
async def new_admin_feature(
    admin: dict = Depends(require_admin)
):
    # Admin-only logic here
    return {"success": True}
```

2. **Frontend**: Use `useAuth` hook
```typescript
function NewAdminFeature() {
  const { isAdmin, getAuthHeaders } = useAuth();
  
  if (!isAdmin) {
    return <AdminLogin onSuccess={() => {}} />;
  }
  
  // Admin feature implementation
}
```

This setup ensures that only you (the admin) can access the blog management features while keeping the system secure and user-friendly.