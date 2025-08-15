# Cloudflare Domain Setup - Vercel Frontend + Render Backend

## 🌐 Domain Architecture

With your separated deployment, you'll set up:
- **Main domain** (`getyourmusicgear.com`) → **Vercel** (Frontend)
- **API subdomain** (`api.getyourmusicgear.com`) → **Render** (Backend)
- **www subdomain** (`www.getyourmusicgear.com`) → **Vercel** (Frontend)

## 🔧 Step 1: Cloudflare DNS Configuration

### **Frontend (Vercel) - Main Domain**

In your Cloudflare dashboard:

1. **A Record for Root Domain**:
   ```
   Type: A
   Name: @
   Content: 76.76.19.61
   Proxy: ✅ Proxied
   TTL: Auto
   ```

2. **CNAME for www**:
   ```
   Type: CNAME
   Name: www
   Content: cname.vercel-dns.com
   Proxy: ✅ Proxied
   TTL: Auto
   ```

### **Backend (Render) - API Subdomain**

3. **CNAME for API**:
   ```
   Type: CNAME
   Name: api
   Content: your-backend-app.onrender.com
   Proxy: ✅ Proxied (recommended for security)
   TTL: Auto
   ```

## 🚀 Step 2: Vercel Domain Configuration

### **Add Domain to Vercel**

1. Go to your Vercel project dashboard
2. Navigate to **Settings** → **Domains**
3. Add these domains:
   - `getyourmusicgear.com`
   - `www.getyourmusicgear.com`

### **Vercel DNS Configuration**

Vercel will show you the required DNS records. Since you're using Cloudflare, you'll need:

```bash
# Vercel will provide these values
A Record: @ → 76.76.19.61
CNAME: www → cname.vercel-dns.com
```

## 🔧 Step 3: Render Domain Configuration (Optional)

If you want a custom domain for your API:

1. Go to your Render service dashboard
2. Navigate to **Settings** → **Custom Domains**
3. Add: `api.getyourmusicgear.com`
4. Render will provide a CNAME target

## 🔑 Step 4: Update Environment Variables

### **Vercel Environment Variables**

Update your Vercel environment variables:

```bash
# Use your custom API domain
NEXT_PUBLIC_API_URL=https://api.getyourmusicgear.com

# Main domain
NEXT_PUBLIC_DOMAIN=getyourmusicgear.com
```

### **Render Environment Variables**

Update your Render backend environment variables:

```bash
# Frontend URLs
FRONTEND_URL=https://getyourmusicgear.com
DOMAIN=getyourmusicgear.com

# Backend URL (if using custom domain)
BACKEND_URL=https://api.getyourmusicgear.com

# CORS - Add your domains
VERCEL_PREVIEW_DOMAINS=getyourmusicgear.com,www.getyourmusicgear.com
```

## 🛡️ Step 5: Cloudflare Security Settings

### **SSL/TLS Configuration**

1. Go to **SSL/TLS** → **Overview**
2. Set encryption mode to: **Full (strict)**
3. Enable **Always Use HTTPS**

### **Security Rules**

1. Go to **Security** → **WAF**
2. Consider enabling:
   - Bot Fight Mode
   - Browser Integrity Check
   - Challenge for suspicious traffic

### **Page Rules (Optional)**

Create page rules for better performance:

```bash
# Cache everything for static assets
Pattern: getyourmusicgear.com/_next/static/*
Settings: Cache Level = Cache Everything

# API subdomain rules
Pattern: api.getyourmusicgear.com/*
Settings: SSL = Full (strict)
```

## 📊 Step 6: Verification

### **Test Your Domains**

```bash
# Test main domain
curl -I https://getyourmusicgear.com

# Test www redirect
curl -I https://www.getyourmusicgear.com

# Test API subdomain
curl -I https://api.getyourmusicgear.com/health

# Test SSL
openssl s_client -connect getyourmusicgear.com:443 -servername getyourmusicgear.com
```

### **DNS Propagation Check**

Use tools like:
- `dig getyourmusicgear.com`
- `nslookup api.getyourmusicgear.com`
- Online tools: whatsmydns.net

## 🔄 Step 7: Update CORS Configuration

Your backend is already configured to handle custom domains! The CORS settings in `backend/app/config.py` will automatically include:

```python
vercel_origins = [
    f"https://{self.DOMAIN}",           # https://getyourmusicgear.com
    f"https://www.{self.DOMAIN}",       # https://www.getyourmusicgear.com
    "https://getyourmusicgear.vercel.app",  # Vercel default domain
]
```

Just make sure your Render environment variables are set correctly:

```bash
DOMAIN=getyourmusicgear.com
FRONTEND_URL=https://getyourmusicgear.com
```

## ⚡ Step 8: Performance Optimization

### **Cloudflare Caching**

1. Go to **Caching** → **Configuration**
2. Set **Caching Level**: Standard
3. Enable **Auto Minify** for HTML, CSS, JS
4. Set **Browser Cache TTL**: 4 hours (or higher)

### **Speed Optimizations**

1. **Enable Brotli compression**
2. **Enable HTTP/2**
3. **Enable 0-RTT Connection Resumption**
4. **Optimize images** with Polish (Pro feature)

## 🚨 Troubleshooting

### **Common Issues**

1. **DNS not propagating**:
   ```bash
   # Clear DNS cache
   sudo dscacheutil -flushcache
   
   # Check propagation
   dig getyourmusicgear.com @8.8.8.8
   ```

2. **SSL certificate issues**:
   - Wait 10-15 minutes for Cloudflare SSL to provision
   - Check SSL/TLS settings are on "Full (strict)"

3. **CORS errors**:
   - Verify domain matches exactly in environment variables
   - Check browser developer tools for specific error messages

4. **Vercel domain not working**:
   - Ensure DNS records point to correct Vercel IPs
   - Check Vercel dashboard for domain verification status

### **Testing Commands**

```bash
# Test main site
curl -H "Host: getyourmusicgear.com" https://getyourmusicgear.com

# Test API
curl https://api.getyourmusicgear.com/health

# Test CORS
curl -H "Origin: https://getyourmusicgear.com" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     https://api.getyourmusicgear.com/api/v1/products
```

## ✅ Final Checklist

- [ ] Cloudflare DNS records configured
- [ ] Vercel domain added and verified
- [ ] Render custom domain configured (optional)
- [ ] Environment variables updated
- [ ] SSL certificates working
- [ ] CORS configuration tested
- [ ] Performance optimizations enabled
- [ ] All domains resolve correctly

## 🎉 You're All Set!

Your domain architecture:
- 🌐 **getyourmusicgear.com** → Vercel (Frontend with SSR)
- 🌐 **www.getyourmusicgear.com** → Vercel (Frontend)
- 🔧 **api.getyourmusicgear.com** → Render (Backend API)

Benefits:
- ✅ **Fast global CDN** via Cloudflare
- ✅ **SSL termination** at Cloudflare edge
- ✅ **DDoS protection** and security
- ✅ **SEO-friendly** URLs
- ✅ **Separate scaling** for frontend/backend

<function_calls>
<invoke name="read_file">
<parameter name="target_file">/Users/felipe/pprojects/musical-instruments-platform/backend/app/config.py
