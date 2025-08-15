# Deployment Guide - Musical Instruments Platform

## Render.com Deployment

### Prerequisites

1. **GitHub Repository**: Your code should be in a GitHub repository
2. **Render.com Account**: Sign up at [render.com](https://render.com)
3. **Environment Variables**: Configure your environment variables in Render.com

### Environment Variables Setup

In your Render.com dashboard, create an environment group called `production_vars` with the following variables:

#### Required Variables
- `DATABASE_URL`: Your PostgreSQL connection string
- `SECRET_KEY`: A secure random string for JWT tokens
- `DEBUG`: Set to `false` for production
- `ENVIRONMENT`: Set to `production`

#### Optional Variables
- `OPENAI_API_KEY`: For AI features
- `AMAZON_ASSOCIATE_TAG`: For Amazon affiliate links
- `THOMANN_AFFILIATE_ID`: For Thomann affiliate links
- `REDIS_URL`: For caching (optional)

### Database Setup

1. **Create PostgreSQL Database**:
   - In Render.com, create a new PostgreSQL service
   - Note the connection string
   - Add it to your environment variables as `DATABASE_URL`

2. **Database Migration**:
   - The application will automatically run migrations on startup
   - If you need to run migrations manually:
   ```bash
   cd backend
   python -m alembic upgrade head
   ```

### Deployment Steps

1. **Connect Repository**:
   - In Render.com, create a new Web Service
   - Connect your GitHub repository
   - Set the repository to: `https://github.com/stonsolabs/musical-instruments-platform`

2. **Configure Service**:
   - **Name**: `musical-instruments-platform`
   - **Runtime**: `Docker`
   - **Region**: `Frankfurt` (or your preferred region)
   - **Branch**: `main`
   - **Root Directory**: Leave empty (uses root)
   - **Dockerfile Path**: `./Dockerfile`

3. **Environment Variables**:
   - Add environment variables from your `production_vars` group
   - Or configure them individually in the service

4. **Health Check**:
   - **Health Check Path**: `/health`
   - The application includes a health endpoint that returns `{"status": "healthy"}`

5. **Custom Domains** (Optional):
   - Add your custom domains in the service settings
   - Configure DNS to point to your Render.com service

### Build Process

The Dockerfile uses a multi-stage build:

1. **Frontend Build Stage**:
   - Uses Node.js 18 Alpine
   - Installs dependencies
   - Builds the Next.js application

2. **Production Stage**:
   - Uses Python 3.11 Slim
   - Installs Python dependencies
   - Copies built frontend
   - Runs database migrations
   - Starts the FastAPI application

### Monitoring

- **Health Checks**: Render.com will monitor `/health` endpoint
- **Logs**: View application logs in the Render.com dashboard
- **Metrics**: Monitor performance and errors

### Troubleshooting

#### Common Issues

1. **Build Failures**:
   - Check the build logs in Render.com
   - Ensure all dependencies are in `requirements.txt`
   - Verify the Dockerfile syntax

2. **Database Connection Issues**:
   - Verify `DATABASE_URL` is correct
   - Check if the database is accessible
   - Ensure migrations can run

3. **Environment Variables**:
   - Verify all required variables are set
   - Check variable names match the application config

4. **Port Issues**:
   - The application uses the `PORT` environment variable
   - Render.com automatically sets this

#### Debug Commands

```bash
# Check application logs
# View in Render.com dashboard

# Test database connection
python -c "
import asyncio
from app.database import engine
asyncio.run(engine.connect().close())
print('Database connection successful')
"

# Run migrations manually
python -m alembic upgrade head

# Check environment variables
python -c "
import os
print('DATABASE_URL:', os.getenv('DATABASE_URL'))
print('DEBUG:', os.getenv('DEBUG'))
"
```

### Performance Optimization

1. **Database Connection Pooling**: Already configured in the application
2. **Static File Serving**: Frontend files are served by FastAPI
3. **Caching**: Consider adding Redis for caching
4. **CDN**: Use a CDN for static assets in production

### Security

1. **Environment Variables**: Never commit secrets to the repository
2. **HTTPS**: Render.com provides automatic HTTPS
3. **CORS**: Configured for production domains
4. **Database**: Use connection pooling and prepared statements

### Updates

To update the application:

1. Push changes to the `main` branch
2. Render.com will automatically redeploy
3. Monitor the deployment logs
4. Verify the health check passes

### Rollback

If you need to rollback:

1. Go to the service in Render.com
2. Navigate to the "Deploys" tab
3. Select a previous successful deployment
4. Click "Rollback"

---

For more information, see the [Render.com documentation](https://render.com/docs).
