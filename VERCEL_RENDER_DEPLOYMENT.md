# Deployment Guide: Vercel Frontend + Render Backend

This guide explains how to deploy the Musical Instruments Platform with the frontend on Vercel and the backend on Render.com.

## Architecture Overview

- **Frontend**: Next.js app deployed on Vercel
- **Backend**: FastAPI app deployed on Render.com
- **Database**: PostgreSQL on Render.com
- **Cache**: Redis on Render.com (optional)

## 1. Backend Deployment on Render.com

### Step 1: Create Backend Service

1. Go to [Render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Use these settings:
   - **Name**: `musical-instruments-backend`
   - **Region**: `Frankfurt` (or your preferred region)
   - **Branch**: `main`
   - **Runtime**: `Python 3`
   - **Build Command**: `cd backend && pip install -r requirements.txt`
   - **Start Command**: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

### Step 2: Configure Environment Variables

Create an environment variable group called `backend_vars` with:

```bash
# Database
DATABASE_URL=postgresql+asyncpg://user:password@host:port/database

# Redis (optional)
REDIS_URL=redis://host:port

# Environment
ENVIRONMENT=production
DEBUG=false

# Domain Configuration
DOMAIN=getyourmusicgear.com
FRONTEND_URL=https://getyourmusicgear.com
BACKEND_URL=https://your-backend-app.onrender.com

# Security
SECRET_KEY=your-super-secret-key-here

# OpenAI (for AI features)
OPENAI_API_KEY=sk-your-openai-key

# Affiliate Programs
AMAZON_ASSOCIATE_TAG=your-amazon-tag
THOMANN_AFFILIATE_ID=your-thomann-id

# CORS - Add your Vercel domains
VERCEL_PREVIEW_DOMAINS=your-project.vercel.app,your-project-git-main.vercel.app
```

### Step 3: Add Database Services

1. Create a PostgreSQL service:
   - Go to "New +" → "PostgreSQL"
   - Choose your plan and region
   - Copy the database URL to your environment variables

2. (Optional) Create a Redis service:
   - Go to "New +" → "Redis"
   - Choose your plan and region
   - Copy the Redis URL to your environment variables

## 2. Frontend Deployment on Vercel

### Step 1: Connect Repository

1. Go to [Vercel.com](https://vercel.com) and sign in
2. Click "New Project"
3. Import your GitHub repository
4. Configure the project:
   - **Framework Preset**: Next.js
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `.next`

### Step 2: Configure Environment Variables

In your Vercel project settings, add these environment variables:

```bash
# Backend API URL (replace with your Render backend URL)
NEXT_PUBLIC_API_URL=https://your-backend-app.onrender.com

# Analytics (optional)
NEXT_PUBLIC_GA_ID=G-XXXXXXXXXX
NEXT_PUBLIC_GTM_ID=GTM-XXXXXXX

# Domain
NEXT_PUBLIC_DOMAIN=getyourmusicgear.com
```

### Step 3: Deploy

1. Click "Deploy" to trigger the first deployment
2. Once deployed, your frontend will be available at your Vercel URL

## 3. Domain Configuration

### Custom Domain for Frontend (Vercel)

1. In your Vercel project, go to "Settings" → "Domains"
2. Add your custom domain (e.g., `getyourmusicgear.com`)
3. Configure DNS records as instructed by Vercel

### Custom Domain for Backend (Optional)

1. In your Render service, go to "Settings" → "Custom Domains"
2. Add a subdomain (e.g., `api.getyourmusicgear.com`)
3. Update your `NEXT_PUBLIC_API_URL` to use the custom domain

## 4. Environment-Specific Configuration

### Development

```bash
# frontend/.env.local
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### Production

The environment variables are managed through:
- **Vercel**: Project settings → Environment Variables
- **Render**: Service settings → Environment Variables

## 5. Deployment Commands

### Backend (Render)

Render automatically deploys when you push to your main branch. You can also:
- Manually deploy from the Render dashboard
- Use the Render API for automated deployments

### Frontend (Vercel)

Vercel automatically deploys when you push to your main branch. You can also:
- Use `vercel --prod` for manual production deployments
- Use `vercel` for preview deployments

## 6. Monitoring and Logs

### Backend Logs (Render)
- View logs in the Render dashboard under your service
- Use `render logs` CLI command

### Frontend Logs (Vercel)
- View function logs in the Vercel dashboard
- Use `vercel logs` CLI command

## 7. Scaling

### Backend (Render)
- Upgrade your plan for more resources
- Consider using Render's autoscaling features

### Frontend (Vercel)
- Vercel automatically scales based on traffic
- Monitor usage in the Vercel dashboard

## 8. Database Migrations

Run database migrations on Render:

```bash
# In your Render service shell
cd backend
alembic upgrade head
```

Or set up automatic migrations in your start command:

```bash
cd backend && alembic upgrade head && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

## 9. Troubleshooting

### CORS Issues
- Ensure your Vercel domains are added to the backend CORS configuration
- Check the `ALLOWED_ORIGINS` in `backend/app/config.py`

### API Connection Issues
- Verify `NEXT_PUBLIC_API_URL` points to your Render backend
- Check backend health endpoint: `https://your-backend-app.onrender.com/health`

### Build Issues
- Check build logs in respective platforms
- Ensure all environment variables are set correctly

## 10. Cost Optimization

### Render (Backend)
- Use the free tier for development
- Upgrade to paid plans for production with custom domains

### Vercel (Frontend)
- Free tier includes generous limits for most projects
- Pro plan needed for team collaboration and advanced features

## Files Created/Modified

- `render.yaml`: Render service configuration
- `vercel.json`: Vercel deployment configuration  
- `frontend/next.config.js`: Updated for Vercel deployment
- `backend/app/config.py`: Updated CORS for separate deployments
- `frontend/env.example`: Updated environment variable examples
