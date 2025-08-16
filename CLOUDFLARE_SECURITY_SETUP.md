# Cloudflare Security Setup for Frontend + Backend

## Overview
- **Frontend**: Deployed on Vercel, served through Cloudflare
- **Backend**: Deployed on Render.com, private access only
- **Security**: IP whitelisting for Vercel → Render communication

## Step 1: Backend Security (Render.com)

### 1.1 Make Backend Private
1. Go to your Render service dashboard
2. Navigate to **Settings** → **Security**
3. **Disable** "Public Networking" 
4. Your backend will now only be accessible via internal Render network

### 1.2 Get Vercel IP Ranges
Vercel uses these IP ranges (updated regularly):
```
76.76.19.76/32
76.76.2.0/24
76.76.2.2/32
76.76.2.3/32
76.76.2.4/32
76.76.2.5/32
76.76.2.6/32
76.76.2.7/32
76.76.2.8/32
76.76.2.9/32
76.76.2.10/32
76.76.2.11/32
76.76.2.12/32
76.76.2.13/32
76.76.2.14/32
76.76.2.15/32
76.76.2.16/32
76.76.2.17/32
76.76.2.18/32
76.76.2.19/32
76.76.2.20/32
76.76.2.21/32
76.76.2.22/32
76.76.2.23/32
76.76.2.24/32
76.76.2.25/32
76.76.2.26/32
76.76.2.27/32
76.76.2.28/32
76.76.2.29/32
76.76.2.30/32
76.76.2.31/32
76.76.2.32/32
76.76.2.33/32
76.76.2.34/32
76.76.2.35/32
76.76.2.36/32
76.76.2.37/32
76.76.2.38/32
76.76.2.39/32
76.76.2.40/32
76.76.2.41/32
76.76.2.42/32
76.76.2.43/32
76.76.2.44/32
76.76.2.45/32
76.76.2.46/32
76.76.2.47/32
76.76.2.48/32
76.76.2.49/32
76.76.2.50/32
76.76.2.51/32
76.76.2.52/32
76.76.2.53/32
76.76.2.54/32
76.76.2.55/32
76.76.2.56/32
76.76.2.57/32
76.76.2.58/32
76.76.2.59/32
76.76.2.60/32
76.76.2.61/32
76.76.2.62/32
76.76.2.63/32
76.76.2.64/32
76.76.2.65/32
76.76.2.66/32
76.76.2.67/32
76.76.2.68/32
76.76.2.69/32
76.76.2.70/32
76.76.2.71/32
76.76.2.72/32
76.76.2.73/32
76.76.2.74/32
76.76.2.75/32
76.76.2.76/32
76.76.2.77/32
76.76.2.78/32
76.76.2.79/32
76.76.2.80/32
76.76.2.81/32
76.76.2.82/32
76.76.2.83/32
76.76.2.84/32
76.76.2.85/32
76.76.2.86/32
76.76.2.87/32
76.76.2.88/32
76.76.2.89/32
76.76.2.90/32
76.76.2.91/32
76.76.2.92/32
76.76.2.93/32
76.76.2.94/32
76.76.2.95/32
76.76.2.96/32
76.76.2.97/32
76.76.2.98/32
76.76.2.99/32
76.76.2.100/32
76.76.2.101/32
76.76.2.102/32
76.76.2.103/32
76.76.2.104/32
76.76.2.105/32
76.76.2.106/32
76.76.2.107/32
76.76.2.108/32
76.76.2.109/32
76.76.2.110/32
76.76.2.111/32
76.76.2.112/32
76.76.2.113/32
76.76.2.114/32
76.76.2.115/32
76.76.2.116/32
76.76.2.117/32
76.76.2.118/32
76.76.2.119/32
76.76.2.120/32
76.76.2.121/32
76.76.2.122/32
76.76.2.123/32
76.76.2.124/32
76.76.2.125/32
76.76.2.126/32
76.76.2.127/32
76.76.2.128/32
76.76.2.129/32
76.76.2.130/32
76.76.2.131/32
76.76.2.132/32
76.76.2.133/32
76.76.2.134/32
76.76.2.135/32
76.76.2.136/32
76.76.2.137/32
76.76.2.138/32
76.76.2.139/32
76.76.2.140/32
76.76.2.141/32
76.76.2.142/32
76.76.2.143/32
76.76.2.144/32
76.76.2.145/32
76.76.2.146/32
76.76.2.147/32
76.76.2.148/32
76.76.2.149/32
76.76.2.150/32
76.76.2.151/32
76.76.2.152/32
76.76.2.153/32
76.76.2.154/32
76.76.2.155/32
76.76.2.156/32
76.76.2.157/32
76.76.2.158/32
76.76.2.159/32
76.76.2.160/32
76.76.2.161/32
76.76.2.162/32
76.76.2.163/32
76.76.2.164/32
76.76.2.165/32
76.76.2.166/32
76.76.2.167/32
76.76.2.168/32
76.76.2.169/32
76.76.2.170/32
76.76.2.171/32
76.76.2.172/32
76.76.2.173/32
76.76.2.174/32
76.76.2.175/32
76.76.2.176/32
76.76.2.177/32
76.76.2.178/32
76.76.2.179/32
76.76.2.180/32
76.76.2.181/32
76.76.2.182/32
76.76.2.183/32
76.76.2.184/32
76.76.2.185/32
76.76.2.186/32
76.76.2.187/32
76.76.2.188/32
76.76.2.189/32
76.76.2.190/32
76.76.2.191/32
76.76.2.192/32
76.76.2.193/32
76.76.2.194/32
76.76.2.195/32
76.76.2.196/32
76.76.2.197/32
76.76.2.198/32
76.76.2.199/32
76.76.2.200/32
76.76.2.201/32
76.76.2.202/32
76.76.2.203/32
76.76.2.204/32
76.76.2.205/32
76.76.2.206/32
76.76.2.207/32
76.76.2.208/32
76.76.2.209/32
76.76.2.210/32
76.76.2.211/32
76.76.2.212/32
76.76.2.213/32
76.76.2.214/32
76.76.2.215/32
76.76.2.216/32
76.76.2.217/32
76.76.2.218/32
76.76.2.219/32
76.76.2.220/32
76.76.2.221/32
76.76.2.222/32
76.76.2.223/32
76.76.2.224/32
76.76.2.225/32
76.76.2.226/32
76.76.2.227/32
76.76.2.228/32
76.76.2.229/32
76.76.2.230/32
76.76.2.231/32
76.76.2.232/32
76.76.2.233/32
76.76.2.234/32
76.76.2.235/32
76.76.2.236/32
76.76.2.237/32
76.76.2.238/32
76.76.2.239/32
76.76.2.240/32
76.76.2.241/32
76.76.2.242/32
76.76.2.243/32
76.76.2.244/32
76.76.2.245/32
76.76.2.246/32
76.76.2.247/32
76.76.2.248/32
76.76.2.249/32
76.76.2.250/32
76.76.2.251/32
76.76.2.252/32
76.76.2.253/32
76.76.2.254/32
76.76.2.255/32
```

### 1.3 Configure Render IP Whitelist
1. In Render dashboard, go to **Settings** → **Security**
2. Add the Vercel IP ranges above to the IP whitelist
3. Save changes

## Step 2: Frontend Configuration (Vercel)

### 2.1 Environment Variables
Set these in your Vercel project settings:

```bash
# Backend URL (your Render backend)
NEXT_PUBLIC_API_BASE_URL=https://musical-instruments-platform.onrender.com

# Google Tag Manager
NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX

# Domain
NEXT_PUBLIC_DOMAIN=getyourmusicgear.com

# Vercel Analytics (optional)
NEXT_TELEMETRY_DISABLED=1
```

### 2.2 Update API Configuration
Your `frontend/src/lib/api.ts` should already be configured correctly:

```typescript
export const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000';
```

## Step 3: Cloudflare Configuration

### 3.1 Add Domain to Cloudflare
1. Add `getyourmusicgear.com` to Cloudflare
2. Update nameservers at your domain registrar

### 3.2 DNS Configuration
Create these DNS records:

```
Type: A
Name: @
Content: 76.76.19.76 (Vercel IP)
Proxy: ✅ (Orange cloud)

Type: CNAME  
Name: www
Content: getyourmusicgear.com
Proxy: ✅ (Orange cloud)
```

### 3.3 Security Settings
In Cloudflare dashboard:

1. **SSL/TLS**: Set to "Full (strict)"
2. **Security Level**: Set to "Medium"
3. **WAF**: Enable with recommended rules
4. **Rate Limiting**: Enable for API endpoints
5. **Bot Management**: Enable

### 3.4 Page Rules (Optional)
Create page rules for additional security:

```
URL: getyourmusicgear.com/api/*
Settings:
- Security Level: High
- Rate Limiting: 100 requests per minute
- Browser Integrity Check: On
```

## Step 4: Backend CORS Configuration

Update your backend CORS settings to only allow your domain:

```python
# In your FastAPI app
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://getyourmusicgear.com",
        "https://www.getyourmusicgear.com",
        "https://getyourmusicgear.vercel.app",
        "https://getyourmusicgear-felipes-projects-28a54414.vercel.app",
        "https://getyourmusicgear-git-main-felipes-projects-28a54414.vercel.app",
        "https://getyourmusicgear-i27l76pvy-felipes-projects-28a54414.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Security Benefits

✅ **Backend is private** - Only accessible via Render internal network  
✅ **IP whitelisting** - Only Vercel can access your backend  
✅ **Cloudflare protection** - DDoS protection, WAF, rate limiting  
✅ **SSL everywhere** - Encrypted communication  
✅ **No exposed API endpoints** - Backend URL not publicly accessible  

## Testing

1. **Frontend**: Should work normally at `https://getyourmusicgear.com`
2. **Backend**: Should be inaccessible via direct URL
3. **API calls**: Should work from frontend to backend
4. **Security**: Try accessing backend directly - should be blocked

## Monitoring

- Use Cloudflare Analytics to monitor traffic
- Set up alerts for unusual activity
- Monitor Render logs for any access attempts
- Use Vercel Analytics for frontend performance
