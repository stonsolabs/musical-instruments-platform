# 🎵 European Musical Instruments Comparison Platform

A modern, scalable platform for comparing musical instrument prices across Europe, built with FastAPI and Next.js.

## 🚀 Quick Start

1. **Setup development environment:**
```bash
./scripts/setup_dev_environment.sh
```

2. **Configure environment variables:**
```bash
cp .env.example .env
# Edit .env with your API keys
```

3. **Start development servers:**
```bash
# Backend (Terminal 1)
cd backend && source venv/bin/activate && uvicorn app.main:app --reload

# Frontend (Terminal 2)  
cd frontend && npm run dev
```

4. **Access the application:**
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🎯 Features

- **Product Comparison**: Compare 2-10 musical instruments side by side
- **Price Tracking**: Real-time prices from major European stores
- **AI Content**: Automated product descriptions and reviews
- **Smart Search**: Advanced filtering and search capabilities
- **Mobile Responsive**: Optimized for all devices
- **SEO Optimized**: Built for search engine visibility

## 🛠️ Tech Stack

- **Backend**: FastAPI + PostgreSQL + Redis + OpenAI API
- **Frontend**: Next.js 14 + TypeScript + Tailwind CSS
- **Deployment**: Vercel (Frontend) + Railway/Render (Backend)

## 💰 Revenue Model

- Affiliate commissions from Amazon, Thomann, Gear4Music, Kytary
- Target: €25K-€75K monthly revenue within 12 months

## 📊 Project Status

- ✅ Complete backend API implementation
- ✅ Full frontend React components
- ✅ AI content generation system
- ✅ Multi-store price comparison
- ✅ Production deployment scripts
- 🔄 Ready for customization and launch

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - see LICENSE file for details.
