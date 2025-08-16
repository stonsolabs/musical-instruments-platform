# 🚨 IMMEDIATE FIX STEPS - 500 Internal Server Error

## 🔍 Root Cause
The 500 error on `/api/proxy/products` indicates that the Vercel proxy cannot communicate with your Render backend. This is likely due to:

1. **Missing or incorrect environment variables** in Vercel
2. **Invalid API key** 
3. **Backend URL configuration issue**

## 🛠️ Step-by-Step Fix

### Step 1: Set Environment Variables in Vercel

Go to your Vercel dashboard → getyourmusicgear project → Settings → Environment Variables

**Add these EXACT variables:**

```bash
# Backend API URL (must include https://)
NEXT_PUBLIC_API_BASE_URL=https://musical-instruments-platform.onrender.com

# API Key (use the one generated earlier)
API_KEY=6cf759ff7f8f3d6971ecbc614f181a5d0606f8d349d8b38f714f0f7b4b6869f9

# Other variables
NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX
NEXT_PUBLIC_DOMAIN=getyourmusicgear.com
NEXT_TELEMETRY_DISABLED=1
```

**⚠️ CRITICAL:**
- Make sure `NEXT_PUBLIC_API_BASE_URL` starts with `https://`
- Make sure `API_KEY` is exactly the same in both Vercel and Render
- **Redeploy** after adding environment variables

### Step 2: Set Environment Variables in Render

Go to your Render dashboard → musical-instruments-platform service → Environment Variables

**Add this variable:**

```bash
API_KEY=6cf759ff7f8f3d6971ecbc614f181a5d0606f8d349d8b38f714f0f7b4b6869f9
```

**⚠️ CRITICAL:**
- Must match the API_KEY in Vercel exactly
- **Redeploy** after adding environment variables

### Step 3: Test the Configuration

After setting environment variables and redeploying:

1. **Test debug endpoint:**
   ```
   https://www.getyourmusicgear.com/api/debug
   ```
   Should return environment variable status.

2. **Test backend directly:**
   ```bash
   curl -H "X-API-Key: 6cf759ff7f8f3d6971ecbc614f181a5d0606f8d349d8b38f714f0f7b4b6869f9" \
        https://musical-instruments-platform.onrender.com/api/v1/products?limit=1
   ```

3. **Test proxy endpoint:**
   ```
   https://www.getyourmusicgear.com/api/proxy/products?limit=1
   ```

### Step 4: Check Vercel Logs

1. Go to Vercel dashboard → getyourmusicgear project → Functions
2. Look for `/api/proxy/[...path]` function
3. Check the logs for detailed error messages
4. The enhanced error logging will show exactly what's failing

## 🔧 Alternative Quick Fix

If the above doesn't work, try this temporary fix to bypass the proxy:

### Option A: Use Direct API Calls (Temporary)

Update `frontend/src/lib/api.ts`:

```typescript
export const API_BASE_URL = 'https://musical-instruments-platform.onrender.com';

export const apiClient = {
  async fetch(endpoint: string, options: RequestInit = {}) {
    const response = await fetch(`${API_BASE_URL}/api/v1${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': '6cf759ff7f8f3d6971ecbc614f181a5d0606f8d349d8b38f714f0f7b4b6869f9',
        ...options.headers,
      },
    });
    
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}: ${response.statusText}`);
    }
    
    return response.json();
  },
  // ... rest of methods
};
```

**⚠️ WARNING:** This exposes the API key to the client. Only use as temporary fix.

## 🚨 Common Issues & Solutions

### Issue: "API key required" in Vercel logs
**Solution:** API_KEY environment variable not set in Vercel

### Issue: "fetch failed" in Vercel logs  
**Solution:** NEXT_PUBLIC_API_BASE_URL is incorrect or backend is down

### Issue: "Invalid API key" in Vercel logs
**Solution:** API_KEY doesn't match between Vercel and Render

### Issue: CORS errors
**Solution:** Backend CORS configuration needs to allow Vercel domain

## 📞 Next Steps

1. **Set environment variables** in both Vercel and Render
2. **Redeploy both services**
3. **Test the debug endpoint** to verify configuration
4. **Check Vercel logs** for detailed error messages
5. **Test the proxy endpoint** to confirm it's working

## 🎯 Expected Result

After fixing:
- ✅ `/api/debug` returns environment variable status
- ✅ `/api/proxy/products?limit=1` returns product data
- ✅ Frontend loads without 500 errors
- ✅ API calls work from browser

If you still get errors, check the Vercel function logs for the exact error message and share it.
