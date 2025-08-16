# API Connection Debugging Guide

## 🔍 Issue Summary
Your frontend (Vercel) and backend (Render) are both working independently, but the frontend is not receiving calls from the backend.

## 🛠️ Fixes Applied

### 1. Fixed Server-Side API Calls
**Problem**: Server-side components were making direct API calls without API key authentication.

**Files Fixed**:
- `frontend/src/app/products/page.tsx` - Added API key to server-side fetch calls
- `frontend/src/app/compare/page.tsx` - Already had API key (good!)

### 2. Fixed Client-Side API Calls
**Problem**: Client-side components were making direct API calls instead of using the proxy route.

**Files Fixed**:
- `frontend/src/app/page.tsx` - Changed to use `/api/proxy/products`
- `frontend/src/app/products/ProductsClient.tsx` - Changed to use `/api/proxy/products`
- `frontend/src/app/products/[slug]/page.tsx` - Changed to use `/api/proxy/products`
- `frontend/src/components/SearchAutocomplete.tsx` - Changed to use `/api/proxy/search/autocomplete`

### 3. Fixed Environment Variable Inconsistency
**Problem**: `env.example` had `NEXT_PUBLIC_API_URL` but code uses `NEXT_PUBLIC_API_BASE_URL`

**Fixed**: Updated `frontend/env.example` to use correct variable name.

## 🔧 Environment Variables Checklist

### Vercel Frontend Environment Variables
Make sure these are set in your Vercel project settings:

```bash
# Backend API URL (your Render backend)
NEXT_PUBLIC_API_BASE_URL=https://musical-instruments-platform.onrender.com

# API Key for backend authentication (server-side only)
API_KEY=your-actual-api-key-here

# Other variables...
NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX
NEXT_PUBLIC_DOMAIN=getyourmusicgear.com
```

### Render Backend Environment Variables
Make sure these are set in your Render service:

```bash
# API Key (must match the one in Vercel)
API_KEY=your-actual-api-key-here

# Database
DATABASE_URL=postgresql+asyncpg://...

# Other backend variables...
ENVIRONMENT=production
DEBUG=false
```

## 🧪 Testing Steps

### 1. Test Backend Directly
```bash
# Test health endpoint (no API key needed)
curl https://musical-instruments-platform.onrender.com/health

# Test API endpoint (API key required)
curl -H "X-API-Key: your-api-key" \
     https://musical-instruments-platform.onrender.com/api/v1/products?limit=1
```

### 2. Test Frontend Proxy
```bash
# Test frontend proxy endpoint
curl https://your-frontend-domain.vercel.app/api/proxy/products?limit=1
```

### 3. Run the Test Script
```bash
# Set your environment variables
export BACKEND_URL=https://musical-instruments-platform.onrender.com
export API_KEY=your-actual-api-key

# Run the test script
node test-api-connection.js
```

## 🔍 Debugging Checklist

### Frontend Issues
- [ ] Check Vercel environment variables are set correctly
- [ ] Verify `NEXT_PUBLIC_API_BASE_URL` points to your Render backend
- [ ] Ensure `API_KEY` matches between frontend and backend
- [ ] Check Vercel function logs for proxy errors

### Backend Issues
- [ ] Verify Render service is running
- [ ] Check Render logs for API errors
- [ ] Ensure CORS is configured correctly
- [ ] Verify API key authentication is working

### Network Issues
- [ ] Test if Render backend is accessible from external sources
- [ ] Check if Vercel can reach Render (no firewall issues)
- [ ] Verify DNS resolution for both domains

## 🚨 Common Issues & Solutions

### Issue: "API key required" errors
**Solution**: Ensure `API_KEY` environment variable is set in both Vercel and Render.

### Issue: CORS errors in browser console
**Solution**: Check that your frontend domain is in the `ALLOWED_ORIGINS` list in backend config.

### Issue: 404 errors on API endpoints
**Solution**: Verify the API routes are correctly configured in `backend/app/main.py`.

### Issue: Timeout errors
**Solution**: Render free tier has cold starts. Consider upgrading or implementing health checks.

## 📊 Monitoring

### Vercel Monitoring
- Check Vercel function logs for proxy errors
- Monitor API route performance
- Check for environment variable issues

### Render Monitoring
- Check Render service logs
- Monitor API response times
- Verify database connectivity

## 🎯 Next Steps

1. **Deploy the fixes** to both frontend and backend
2. **Test the API connection** using the provided test script
3. **Check browser console** for any remaining errors
4. **Monitor logs** in both Vercel and Render
5. **Test user flows** to ensure everything works end-to-end

## 📞 Support

If issues persist after applying these fixes:
1. Check the logs in both Vercel and Render
2. Run the test script and share the output
3. Verify all environment variables are set correctly
4. Test with a simple curl command to isolate the issue
