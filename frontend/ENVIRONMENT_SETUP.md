# Environment Setup for Production

## 🔒 Security Notice
**NEVER commit real API keys to git!** This guide shows you how to properly configure environment variables.

## 📋 Required Environment Variables

### For Production Deployment:

```bash
# API Configuration
NEXT_PUBLIC_API_BASE_URL=https://getyourmusicgear-api.azurewebsites.net
API_KEY=your_actual_api_key_here

# Domain Configuration  
NEXT_PUBLIC_DOMAIN=getyourmusicgear.com
NODE_ENV=production
```

### For Local Development:

```bash
# API Configuration (for local backend)
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
# API_KEY is optional for localhost development

# Domain Configuration
NEXT_PUBLIC_DOMAIN=localhost:3000
NODE_ENV=development
```

## 🚀 Setup Instructions

### 1. For Production (Vercel/Netlify):
1. Copy `env.azure` to `.env.local`
2. Update `API_KEY` with your real API key
3. Set environment variables in your hosting platform:
   - Vercel: Project Settings → Environment Variables
   - Netlify: Site Settings → Environment Variables

### 2. For Local Development:
1. Create `.env.local` in the frontend directory
2. Add the local development variables above
3. No API key needed for localhost

## 🔍 Environment Variable Validation

The application will:
- ✅ **Work locally** without API key (uses localhost)
- ⚠️ **Require API key** for production endpoints
- 🛑 **Fail gracefully** if API key is missing

## 🚨 Security Best Practices

1. **Never commit `.env.local`** (already in .gitignore)
2. **Use different API keys** for different environments
3. **Rotate API keys regularly**
4. **Monitor API key usage** in your backend logs

## 📁 File Structure

```
frontend/
├── env.azure          # Template with production URL
├── env.example        # Template for reference
├── .env.local         # Your actual environment (gitignored)
└── ENVIRONMENT_SETUP.md # This guide
```

## 🔧 Troubleshooting

### Error: "API_KEY environment variable is not set"
- Check that `.env.local` exists and contains `API_KEY=your_key`
- Restart your development server after adding environment variables

### Error: "API key required" 
- Verify your API key is correct
- Check that it's set in your hosting platform's environment variables

### Local development not working:
- Ensure `NEXT_PUBLIC_API_BASE_URL=http://localhost:8000`
- Make sure your backend is running on port 8000
