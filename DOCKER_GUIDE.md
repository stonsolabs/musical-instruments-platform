# Docker Setup Guide - Separated Services Architecture

This guide explains the Docker setup for the Musical Instruments Platform with separated frontend and backend services, optimized for SEO and server-side rendering.

## 🏗️ Architecture Overview

The platform now uses a **separated services architecture**:

- **Backend**: FastAPI service (deployed on Render.com)
- **Frontend**: Next.js with SSR (deployed on Vercel, but can run in Docker)
- **Database**: PostgreSQL
- **Cache**: Redis (optional)

## 📁 Docker Files Structure

```
├── backend/
│   └── Dockerfile              # Production backend image
├── frontend/
│   └── Dockerfile              # SEO-optimized frontend with SSR
├── Dockerfile.dev              # Development multi-stage build
├── docker-compose.yml          # Local development with separated services
├── docker-compose.dev.yml      # Development with hot reload
└── docker-compose.prod.yml     # Production-like environment
```

## 🚀 Quick Start

### Development Environment
```bash
# Start all services with hot reload
docker-compose -f docker-compose.dev.yml up --build

# Or use the regular compose for production-like testing
docker-compose up --build
```

### Production Testing
```bash
# Test production builds locally
docker-compose -f docker-compose.prod.yml up --build
```

## 🔧 Individual Service Commands

### Backend Only
```bash
cd backend
docker build -t musical-instruments-backend .
docker run -p 10000:10000 \
  -e DATABASE_URL=postgresql+asyncpg://postgres:postgres@host.docker.internal:5432/musical_instruments \
  musical-instruments-backend
```

### Frontend Only
```bash
cd frontend
docker build -t musical-instruments-frontend .
docker run -p 3000:3000 \
  -e NEXT_PUBLIC_API_URL=http://localhost:10000 \
  -e BUILD_STANDALONE=true \
  musical-instruments-frontend
```

## 🌟 SEO Optimizations

The frontend Docker setup includes several SEO optimizations:

### 1. Server-Side Rendering (SSR)
- Next.js runs in production mode with SSR enabled
- Products and pages are rendered on the server for better SEO
- Meta tags and structured data are generated server-side

### 2. Standalone Mode
- Uses Next.js standalone output for optimal performance
- Reduces image size and startup time
- Self-contained deployment

### 3. Health Checks
- Frontend includes `/api/health` endpoint
- Monitors backend connectivity
- Ensures services are ready before serving traffic

### 4. Performance Features
- Multi-stage builds for smaller images
- Non-root user for security
- Optimized caching layers
- Compressed assets

## 🔄 Environment Configurations

### Development (`docker-compose.dev.yml`)
- Hot reload for both frontend and backend
- Debug mode enabled
- Volume mounts for live code changes
- Detailed logging

### Testing (`docker-compose.yml`)
- Production builds but with development settings
- Good for testing deployment configurations
- Health checks enabled

### Production (`docker-compose.prod.yml`)
- Optimized production builds
- Security hardening
- Performance tuning
- Health checks and monitoring

## 📊 Service Health Monitoring

All services include health checks:

- **Backend**: `GET /health` - API health and database connectivity
- **Frontend**: `GET /api/health` - Frontend health and backend connectivity  
- **Database**: PostgreSQL readiness check
- **Redis**: Redis ping check

## 🔗 Service Communication

### Internal Communication
- Services communicate using Docker network names
- Backend: `http://backend:10000`
- Frontend: `http://frontend:3000`
- Database: `postgres:5432`
- Redis: `redis:6379`

### External Access
- Frontend: `http://localhost:3000`
- Backend API: `http://localhost:10000` (dev) or `http://localhost:8000` (prod)
- Database: `localhost:5432`
- Redis: `localhost:6379`

## 🛠️ Development Workflow

### 1. Start Development Environment
```bash
docker-compose -f docker-compose.dev.yml up
```

### 2. View Logs
```bash
# All services
docker-compose -f docker-compose.dev.yml logs -f

# Specific service
docker-compose -f docker-compose.dev.yml logs -f frontend
docker-compose -f docker-compose.dev.yml logs -f backend
```

### 3. Execute Commands in Containers
```bash
# Backend shell
docker-compose -f docker-compose.dev.yml exec backend bash

# Frontend shell  
docker-compose -f docker-compose.dev.yml exec frontend sh

# Database access
docker-compose -f docker-compose.dev.yml exec postgres psql -U postgres -d musical_instruments
```

### 4. Database Migrations
```bash
# Run migrations
docker-compose -f docker-compose.dev.yml exec backend python -m alembic upgrade head

# Create new migration
docker-compose -f docker-compose.dev.yml exec backend python -m alembic revision --autogenerate -m "Description"
```

## 🚀 Production Deployment

### Render Backend
The backend Dockerfile is optimized for Render.com:
- Uses production-grade uvicorn settings
- Includes health checks
- Security hardening with non-root user
- Optimized for single-worker deployment

### Vercel Frontend
While the frontend can run in Docker, it's optimized for Vercel:
- Set `BUILD_STANDALONE=false` for Vercel
- Set `BUILD_STANDALONE=true` for Docker deployment
- SSR works in both environments

## 🔍 Troubleshooting

### Frontend Can't Connect to Backend
```bash
# Check if backend is running
curl http://localhost:10000/health

# Check Docker network
docker network ls
docker network inspect musical-instruments-platform_default
```

### Database Connection Issues
```bash
# Check if PostgreSQL is ready
docker-compose exec postgres pg_isready -U postgres

# Check database logs
docker-compose logs postgres
```

### Build Issues
```bash
# Clean build (removes cache)
docker-compose build --no-cache

# Remove all containers and volumes
docker-compose down -v
docker system prune -a
```

### SEO Testing
```bash
# Test server-side rendering
curl -H "User-Agent: Googlebot" http://localhost:3000/products/guitar

# Check meta tags
curl -s http://localhost:3000/products/guitar | grep -i "<meta"
```

## 📈 Performance Monitoring

### Container Stats
```bash
docker stats
```

### Resource Usage
```bash
# Memory usage
docker-compose exec frontend cat /proc/meminfo
docker-compose exec backend cat /proc/meminfo

# CPU usage
docker-compose exec frontend top
```

## 🔒 Security Notes

- All containers run as non-root users
- Secrets should be passed via environment variables
- Database passwords should be changed in production
- Use Docker secrets for sensitive data in production

## 🎯 Next Steps

1. **Local Development**: Use `docker-compose.dev.yml`
2. **Production Testing**: Use `docker-compose.prod.yml`
3. **Deploy Backend**: Use `backend/Dockerfile` on Render
4. **Deploy Frontend**: Use Vercel (recommended) or Docker
5. **Monitor**: Set up logging and monitoring for production

The Docker setup ensures your SEO is optimized with server-side rendering while maintaining the flexibility of separated deployments!
