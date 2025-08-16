# API Key Setup - Ready to Deploy

## Generated API Key
```
[GENERATE YOUR OWN API KEY - DO NOT USE THIS ONE]
```

## Step 1: Render Backend Configuration

### 1.1 Add Environment Variables
Go to Render dashboard → musical-instruments-platform service → Environment Variables

Add these variables:
```
API_KEY=[YOUR-GENERATED-API-KEY-HERE]
BACKEND_URL=https://musical-instruments-platform.onrender.com
VERCEL_PREVIEW_DOMAINS=getyourmusicgear.vercel.app,getyourmusicgear-felipes-projects-28a54414.vercel.app,getyourmusicgear-git-main-felipes-projects-28a54414.vercel.app,getyourmusicgear-i27l76pvy-felipes-projects-28a54414.vercel.app
```

### 1.2 Deploy Backend
- Render will automatically redeploy with the new environment variables
- Check logs to ensure no errors

## Step 2: Vercel Frontend Configuration

### 2.1 Add Environment Variables
Go to Vercel dashboard → getyourmusicgear project → Settings → Environment Variables

**Important:** We use `API_KEY` (not `NEXT_PUBLIC_API_KEY`) to keep the key server-side only!

Add these variables:
```
NEXT_PUBLIC_API_BASE_URL=https://musical-instruments-platform.onrender.com
API_KEY=[YOUR-GENERATED-API-KEY-HERE]
NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX (your actual GTM ID)
NEXT_PUBLIC_DOMAIN=getyourmusicgear.com
NEXT_TELEMETRY_DISABLED=1
```

### 2.2 Deploy Frontend
- Vercel will automatically redeploy with the new environment variables
- Check deployment logs for any errors

## Step 3: Cloudflare DNS Fix

### 3.1 Update DNS Records
Your current DNS is incorrect. Update in Cloudflare:

**Delete current A record:**
```
A    getyourmusicgear.com    216.198.79.1    DNS only
```

**Add new records:**
```
A    getyourmusicgear.com    76.76.19.76     Proxied ✅
CNAME www                    getyourmusicgear.com    Proxied ✅
```

### 3.2 Security Settings
In Cloudflare dashboard:
- SSL/TLS: Full (strict)
- Security Level: Medium
- WAF: Enable
- Rate Limiting: Enable
- Bot Management: Enable

## Step 4: Testing

### 4.1 Test Backend Security
```bash
# This should return 401 (Unauthorized)
curl https://musical-instruments-platform.onrender.com/api/v1/products

# This should return 401 (Unauthorized)
curl https://musical-instruments-platform.onrender.com/api/v1/compare
```

### 4.2 Test Frontend
- Visit: https://getyourmusicgear.com
- Should load normally
- API calls should work from frontend

### 4.3 Test API with Key
```bash
# This should work (replace with your actual API key)
curl -H "X-API-Key: [YOUR-GENERATED-API-KEY-HERE]" \
     https://musical-instruments-platform.onrender.com/api/v1/products
```

## Security Benefits Achieved

✅ **Backend Protected** - API key required for all endpoints  
✅ **No Public Access** - Backend returns 401 without key  
✅ **API Key Secure** - Server-side proxy keeps key hidden from client  
✅ **Frontend Works** - Vercel can access backend through secure proxy  
✅ **Cloudflare Protection** - DDoS, WAF, rate limiting  
✅ **SSL Everywhere** - Encrypted communication  

## Troubleshooting

### If API calls fail:
1. Check environment variables are set correctly
2. Verify API key is the same in both Render and Vercel
3. Check CORS configuration in backend

### If frontend doesn't load:
1. Fix DNS records in Cloudflare
2. Check Vercel deployment status
3. Verify domain nameservers are updated

### If backend is accessible without key:
1. Check that API_KEY environment variable is set in Render
2. Verify the auth middleware is working
3. Restart Render service after adding environment variables
