# Security Setup Checklist

## Your Current Setup
- **Frontend**: Vercel (getyourmusicgear.vercel.app)
- **Backend**: Render (musical-instruments-platform.onrender.com)
- **Domain**: getyourmusicgear.com

## Step 1: Render Backend Security ✅

### 1.1 Make Backend Private
- [ ] Go to Render dashboard → musical-instruments-platform service
- [ ] Settings → Security → Disable "Public Networking"
- [ ] This makes your backend private (not publicly accessible)

### 1.2 IP Whitelist Vercel
- [ ] In Render dashboard → Settings → Security
- [ ] Add Vercel IP ranges (see CLOUDFLARE_SECURITY_SETUP.md)
- [ ] This allows only Vercel to access your backend

### 1.3 Update Environment Variables
- [ ] Copy from `env-templates/render-env-vars.txt`
- [ ] Update in Render dashboard → Environment Variables
- [ ] Key variables to set:
  ```
  BACKEND_URL=https://musical-instruments-platform.onrender.com
  VERCEL_PREVIEW_DOMAINS=getyourmusicgear.vercel.app,getyourmusicgear-felipes-projects-28a54414.vercel.app,getyourmusicgear-git-main-felipes-projects-28a54414.vercel.app,getyourmusicgear-i27l76pvy-felipes-projects-28a54414.vercel.app
  ```

## Step 2: Vercel Frontend Configuration ✅

### 2.1 Environment Variables
- [ ] Go to Vercel dashboard → getyourmusicgear project
- [ ] Settings → Environment Variables
- [ ] Add these variables:
  ```
  NEXT_PUBLIC_API_BASE_URL=https://musical-instruments-platform.onrender.com
  NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX (your actual GTM ID)
  NEXT_PUBLIC_DOMAIN=getyourmusicgear.com
  NEXT_TELEMETRY_DISABLED=1
  ```

### 2.2 Test Frontend
- [ ] Deploy should work now
- [ ] Check that API calls work from frontend to backend

## Step 3: Cloudflare Setup ✅

### 3.1 Add Domain to Cloudflare
- [ ] Add `getyourmusicgear.com` to Cloudflare
- [ ] Update nameservers at your domain registrar

### 3.2 DNS Configuration
- [ ] Create A record: `@` → `76.76.19.76` (Vercel IP)
- [ ] Create CNAME: `www` → `getyourmusicgear.com`
- [ ] Enable proxy (orange cloud) for both

### 3.3 Security Settings
- [ ] SSL/TLS: Full (strict)
- [ ] Security Level: Medium
- [ ] WAF: Enable
- [ ] Rate Limiting: Enable
- [ ] Bot Management: Enable

## Step 4: Backend CORS Update ✅

### 4.1 Update CORS Configuration
- [ ] In your backend code, update CORS origins:
  ```python
  allow_origins=[
      "https://getyourmusicgear.com",
      "https://www.getyourmusicgear.com", 
      "https://getyourmusicgear.vercel.app",
      "https://getyourmusicgear-felipes-projects-28a54414.vercel.app",
      "https://getyourmusicgear-git-main-felipes-projects-28a54414.vercel.app",
      "https://getyourmusicgear-i27l76pvy-felipes-projects-28a54414.vercel.app",
  ]
  ```

## Step 5: Testing ✅

### 5.1 Security Tests
- [ ] Frontend works: https://getyourmusicgear.com
- [ ] Backend blocked: https://musical-instruments-platform.onrender.com (should be inaccessible)
- [ ] API calls work: Frontend can call backend APIs
- [ ] CORS works: No CORS errors in browser

### 5.2 Monitoring
- [ ] Check Cloudflare Analytics
- [ ] Monitor Render logs for access attempts
- [ ] Set up alerts for unusual activity

## Security Benefits Achieved ✅

- ✅ **Backend is private** - No public access to API
- ✅ **IP whitelisting** - Only Vercel can access backend  
- ✅ **Cloudflare protection** - DDoS, WAF, rate limiting
- ✅ **SSL everywhere** - Encrypted communication
- ✅ **Domain protection** - Frontend served through Cloudflare

## Troubleshooting

### If API calls fail:
1. Check Vercel environment variables
2. Verify CORS configuration in backend
3. Check Render IP whitelist includes Vercel IPs

### If frontend doesn't load:
1. Check Cloudflare DNS configuration
2. Verify domain nameservers are updated
3. Check Vercel deployment status

### If backend is still accessible:
1. Verify "Public Networking" is disabled in Render
2. Check IP whitelist configuration
3. Restart Render service after changes
