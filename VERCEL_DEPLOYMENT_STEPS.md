# Vercel Deployment Guide - Step by Step

## 🚀 Deploy Your Frontend to Vercel

Follow these exact steps to deploy your Musical Instruments Platform frontend to Vercel.

## 📋 Prerequisites

1. ✅ Your code is pushed to GitHub
2. ✅ Backend is deployed on Render.com (get your backend URL)
3. ✅ You have a Vercel account

## 🔗 Step 1: Connect to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in
2. Click **"New Project"**
3. Import your GitHub repository: `musical-instruments-platform`
4. Click **"Import"**

## ⚙️ Step 2: Configure Project Settings

### **Framework Preset**
- Select: **Next.js** ✅

### **Root Directory**
- **IMPORTANT**: Set to `frontend` ✅
- Click "Edit" next to Root Directory
- Type: `frontend`

### **Build and Output Settings**
- **Build Command**: `npm run build` (default is fine)
- **Output Directory**: `.next` (default is fine)
- **Install Command**: `npm install` (default is fine)

### **Node.js Version**
- Use: **18.x** (recommended)

## 🔑 Step 3: Environment Variables

Click **"Environment Variables"** and add these:

### **Required Variables:**
```bash
# Backend API URL - MUST include https:// protocol
# Replace with your actual Render URL
# WRONG: your-backend-app.onrender.com  
# CORRECT: https://your-backend-app.onrender.com
NEXT_PUBLIC_API_URL=https://your-backend-app.onrender.com

# Domain (for production)
NEXT_PUBLIC_DOMAIN=getyourmusicgear.com
```

### **Optional Analytics Variables:**
```bash
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX
```

### **Environment Settings:**
- Set these for: **Production**, **Preview**, and **Development**
- Make sure `NEXT_PUBLIC_API_URL` points to your Render backend

## 🚀 Step 4: Deploy

1. Click **"Deploy"**
2. Wait for the build to complete (usually 2-3 minutes)
3. You'll get a URL like: `https://musical-instruments-platform-xxx.vercel.app`

## ✅ Step 5: Verify Deployment

### Test these URLs:
```bash
# Homepage
https://your-app.vercel.app

# Products page (should load server-side)
https://your-app.vercel.app/products

# Health check
https://your-app.vercel.app/api/health

# Compare page
https://your-app.vercel.app/compare
```

### Check SEO:
```bash
# Test with curl to see server-side rendering
curl -H "User-Agent: Googlebot" https://your-app.vercel.app/products
```

## 🌐 Step 6: Custom Domain (Optional)

1. In Vercel dashboard, go to **Settings** → **Domains**
2. Add your domain: `getyourmusicgear.com`
3. Add www subdomain: `www.getyourmusicgear.com`
4. Configure DNS as instructed by Vercel

## 🔄 Step 7: Update Backend CORS

Once deployed, update your Render backend environment variables:

```bash
# Add your Vercel URLs to backend CORS
VERCEL_PREVIEW_DOMAINS=your-app.vercel.app,your-app-git-main.vercel.app

# Update frontend URL
FRONTEND_URL=https://your-app.vercel.app
```

## 🔧 Common Issues & Solutions

### **Build Fails**
```bash
# Check if Next.js config is correct
# Ensure all dependencies are in package.json
# Check for TypeScript errors
```

### **API Calls Fail**
```bash
# Verify NEXT_PUBLIC_API_URL is set correctly
# Check backend CORS settings
# Ensure backend is deployed and healthy
```

### **Environment Variables Not Working**
```bash
# Make sure they start with NEXT_PUBLIC_ for client-side
# Redeploy after adding environment variables
# Check they're set for the right environment (Production/Preview)
```

### **SSR Not Working**
```bash
# Check if pages are using server components
# Verify API calls work from server-side
# Check browser network tab for hydration
```

## 📊 Monitoring & Analytics

### **Vercel Analytics**
- Enable in Vercel dashboard → Analytics
- Monitor Core Web Vitals
- Track page performance

### **Custom Analytics**
- Google Analytics will work with your `NEXT_PUBLIC_GA_ID`
- GTM will work with your `NEXT_PUBLIC_GTM_ID`

## 🔄 Automatic Deployments

Vercel automatically deploys when you:
- Push to `main` branch → Production deployment
- Push to other branches → Preview deployment
- Open pull requests → Preview deployment

## 🎯 Final Checklist

- [ ] Frontend deploys successfully
- [ ] Environment variables are set
- [ ] API calls work (check `/api/health`)
- [ ] Products page loads with server-side rendering
- [ ] Backend CORS allows Vercel domains
- [ ] Custom domain configured (if needed)
- [ ] Analytics tracking works

## 🚀 You're Live!

Your Musical Instruments Platform is now deployed with:
- ✅ **Frontend**: Vercel (with SSR for SEO)
- ✅ **Backend**: Render.com
- ✅ **SEO Optimized**: Server-side rendering
- ✅ **Performance**: Optimized builds
- ✅ **Monitoring**: Health checks and analytics

## 📞 Need Help?

Check the logs:
- **Vercel**: Dashboard → Functions → View Function Logs
- **Render**: Dashboard → Logs
- **Local Testing**: Use `./scripts/docker-seo-test.sh`
