# Render.com Deployment Guide

## Quick Fix for Current Issues

The main issue is with `npm ci` failing. Here are the solutions:

### Option 1: Use the Optimized Dockerfile (Recommended)
The main `Dockerfile` has been optimized with:
- Replaced `npm ci` with `npm install` with fallback options
- Simplified build process
- Removed unnecessary complexity

### Option 2: Use the Simple Dockerfile
If the main Dockerfile still fails, use `Dockerfile.simple`:
```bash
# In render.yaml, change:
dockerfilePath: ./Dockerfile.simple
```

## Deployment Steps

1. **Push the updated files to your repository**
2. **In Render.com dashboard:**
   - Go to your service
   - Under "Settings" → "Build & Deploy"
   - Set "Dockerfile Path" to `./Dockerfile` (or `./Dockerfile.simple` if needed)
   - Set "Docker Context" to `.`

3. **Environment Variables:**
   Make sure these are set in your Render environment:
   ```
   DATABASE_URL=your_postgres_url
   REDIS_URL=your_redis_url
   SECRET_KEY=your_secret_key
   ```

4. **Manual Deploy:**
   - Click "Manual Deploy" → "Deploy latest commit"

## Troubleshooting

### If npm install still fails:
1. Check the build logs in Render
2. Try using `Dockerfile.simple` instead
3. Ensure your `package.json` is valid

### If the app starts but doesn't work:
1. Check the health endpoint: `https://your-app.onrender.com/health`
2. Verify environment variables are set correctly
3. Check the application logs in Render dashboard

### Common Issues:
- **Build timeout**: Render free tier has 15-minute build limit
- **Memory issues**: The optimized Dockerfile uses less memory
- **Port issues**: Make sure the app listens on `$PORT` environment variable

## Alternative: Separate Frontend/Backend Deployment

If the single-container approach continues to fail, consider:

1. **Deploy backend only** on Render
2. **Deploy frontend** on Vercel/Netlify
3. **Connect them** via environment variables

## Monitoring

After deployment:
1. Check the health endpoint
2. Monitor logs in Render dashboard
3. Test your main functionality
4. Set up alerts if needed

## Rollback Plan

If deployment fails:
1. Use the previous working commit
2. Switch to `Dockerfile.simple`
3. Consider the separate deployment approach
