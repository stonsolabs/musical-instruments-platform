# Quick Deployment Reference

## 🚀 Ready to Deploy!

Your Musical Instruments Platform is now configured for separate deployment:
- **Frontend**: Vercel
- **Backend**: Render.com

## 📋 Quick Checklist

### 1. Backend on Render.com
- [ ] Create Web Service with Python runtime
- [ ] Use build command: `cd backend && pip install -r requirements.txt`
- [ ] Use start command: `cd backend && uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- [ ] Add environment variables from `env-templates/render-env-vars.txt`
- [ ] Add PostgreSQL service (copy DATABASE_URL to env vars)
- [ ] (Optional) Add Redis service (copy REDIS_URL to env vars)

### 2. Frontend on Vercel
- [ ] Connect GitHub repo
- [ ] Set root directory to `frontend`
- [ ] Add environment variables from `env-templates/vercel-env-vars.txt`
- [ ] Update `NEXT_PUBLIC_API_URL` with your Render backend URL
- [ ] Deploy

### 3. Update Environment Variables
- [ ] Replace `your-backend-app.onrender.com` with actual Render URL
- [ ] Add your actual API keys and affiliate IDs
- [ ] Update domain names

## 🔗 Important URLs

After deployment, update these:
- `NEXT_PUBLIC_API_URL` → Your Render backend URL
- `FRONTEND_URL` → Your Vercel frontend URL  
- `BACKEND_URL` → Your Render backend URL

## 🛠 Files Created/Modified

### New Files:
- `render.yaml` - Render service configuration
- `vercel.json` - Vercel deployment configuration
- `VERCEL_RENDER_DEPLOYMENT.md` - Complete deployment guide
- `deploy-separate.sh` - Deployment preparation script
- `env-templates/` - Environment variable templates

### Modified Files:
- `backend/app/config.py` - Updated CORS for separate deployment
- `frontend/next.config.js` - Optimized for Vercel
- `frontend/env.example` - Updated for new deployment model

## 🆘 Need Help?

1. Check `VERCEL_RENDER_DEPLOYMENT.md` for detailed instructions
2. Run `./deploy-separate.sh` to prepare for deployment
3. Check the troubleshooting section in the deployment guide

Happy deploying! 🎉
