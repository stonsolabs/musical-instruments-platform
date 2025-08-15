# Full-Stack Deployment Guide

## 🚀 Ready to Deploy Frontend + Backend

You're now configured to deploy the complete application with both frontend and backend using Docker.

## What Will Happen

### Build Process (~8-10 minutes)
1. **Frontend Stage** (Node.js 18 Alpine)
   - Install npm dependencies
   - Build Next.js application with simplified config
   - Generate optimized production build

2. **Backend Stage** (Python 3.11 Slim)
   - Install system dependencies (gcc, libpq-dev, curl)
   - Install Python packages from requirements.txt
   - Copy backend source code
   - Copy built frontend from stage 1

3. **Final Result**
   - Single container with both frontend and backend
   - FastAPI serving the API endpoints
   - Next.js static files served by FastAPI
   - All running on port 10000

## Configuration Details

### Current Setup
- **render.yaml**: Points to `./Dockerfile.simple-fullstack`
- **Frontend**: Uses `next.config.simple.js` (simplified config)
- **Backend**: Serves both API and static files
- **Database**: Async PostgreSQL with proper URL handling

### Environment Variables (Already Set)
- `DATABASE_URL` - PostgreSQL connection
- `SECRET_KEY` - Application security
- `ENVIRONMENT=production` - Production mode

## Deployment Steps

### 1. Commit and Push
```bash
git add .
git commit -m "Deploy fullstack with Docker"
git push
```

### 2. Monitor Build
- Go to Render.com dashboard
- Watch the build logs
- Build should take ~8-10 minutes

### 3. Test After Deployment
```bash
# Test health endpoint
curl https://your-app.onrender.com/health

# Test API endpoints
curl https://your-app.onrender.com/api/v1/products
curl https://your-app.onrender.com/api/v1/categories

# Test frontend (should serve Next.js app)
# Visit https://your-app.onrender.com in browser
```

## What You'll Get

### ✅ Backend API
- All your FastAPI endpoints working
- Proper async database connections
- Health monitoring
- CORS configured for production

### ✅ Frontend Application
- Next.js app with TailwindCSS
- Optimized production build
- Static file serving
- SPA routing support

### ✅ Production Features
- Health checks
- Custom domain support
- Automatic deployments
- Error monitoring

## If Build Fails

### Fallback Option
If the frontend build fails, you can quickly switch to backend-only:
```bash
cp render-backend-only.yaml render.yaml
git commit -m "Fallback to backend only"
git push
```

### Common Issues
- **Build timeout**: Render free tier has 15-minute limit
- **Memory issues**: Large builds may need more memory
- **Dependency conflicts**: Simplified config should prevent this

## Expected Endpoints

After successful deployment:
- **Frontend**: `https://your-app.onrender.com/`
- **Health**: `https://your-app.onrender.com/health`
- **Products API**: `https://your-app.onrender.com/api/v1/products`
- **Categories API**: `https://your-app.onrender.com/api/v1/categories`
- **Brands API**: `https://your-app.onrender.com/api/v1/brands`
- **Search API**: `https://your-app.onrender.com/api/v1/search`

## Ready to Deploy! 🚀

Your configuration is now set for fullstack deployment. Just commit and push to start the build process.
