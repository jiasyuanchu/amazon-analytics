# Amazon Product Analytics Dashboard

A comprehensive full-stack application for analyzing Amazon product data with AI-powered insights. This project demonstrates modern web development practices using Python FastAPI, Next.js, PostgreSQL with TimescaleDB, and AI integration.

## 🚀 Features

### Backend Features
- **FastAPI** REST API with automatic OpenAPI documentation
- **PostgreSQL** with **TimescaleDB** for time-series data
- **Redis** for caching and session management
- **SQLAlchemy 2.0** with async support
- **Alembic** database migrations
- **Pydantic** data validation and serialization
- **AI Integration** ready for OpenAI/Anthropic APIs

### Frontend Features
- **Next.js 14** with TypeScript
- **Tailwind CSS** for responsive design
- **React Query** for efficient data fetching
- **Recharts** for data visualization
- **Responsive dashboard** with modern UI components

### DevOps & Infrastructure
- **Docker** containerization
- **Docker Compose** for multi-service orchestration
- **Nginx** reverse proxy with rate limiting
- **Health checks** and monitoring
- **Development and production** configurations

## 🛠 Tech Stack

### Backend
- Python 3.11+
- FastAPI 0.104+
- PostgreSQL 15 with TimescaleDB
- Redis 7
- SQLAlchemy 2.0
- Alembic
- Pydantic 2.0

### Frontend
- Next.js 14
- TypeScript
- Tailwind CSS
- React Query
- Recharts
- Heroicons

### DevOps
- Docker & Docker Compose
- Nginx
- GitHub Actions (ready)

## 📦 Project Structure

```
amazon-analytics/
├── backend/                 # FastAPI backend application
│   ├── app/
│   │   ├── api/v1/         # API routes and endpoints
│   │   ├── core/           # Configuration and settings
│   │   ├── db/             # Database configuration
│   │   ├── models/         # SQLAlchemy models
│   │   ├── schemas/        # Pydantic schemas
│   │   ├── services/       # Business logic and services
│   │   └── utils/          # Utility functions
│   ├── alembic/            # Database migrations
│   ├── requirements.txt    # Python dependencies
│   └── Dockerfile          # Backend container configuration
├── frontend/               # Next.js frontend application
│   ├── src/
│   │   ├── app/           # Next.js app directory
│   │   ├── components/    # React components
│   │   ├── lib/           # Utility libraries and API functions
│   │   └── types/         # TypeScript type definitions
│   ├── package.json       # Node.js dependencies
│   └── Dockerfile         # Frontend container configuration
├── docker/                # Docker configuration files
│   ├── nginx/             # Nginx configuration
│   └── postgres/          # PostgreSQL initialization
├── scripts/               # Utility scripts
└── docker-compose.yml     # Multi-service orchestration
```

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Node.js 18+ (for local development)
- Python 3.11+ (for local development)

### Option 1: Docker Development Environment

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd amazon-analytics
   ```

2. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your API keys
   ```

3. **Start development services**
   ```bash
   chmod +x scripts/start-dev.sh
   ./scripts/start-dev.sh
   ```

4. **Start backend (in separate terminal)**
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn app.main:app --reload
   ```

5. **Start frontend (in separate terminal)**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

### Option 2: Full Docker Production Environment

1. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your production configurations
   ```

2. **Start all services**
   ```bash
   chmod +x scripts/start-prod.sh
   ./scripts/start-prod.sh
   ```

## 🔧 Configuration

### Environment Variables

#### Backend (.env)
```env
# Database
POSTGRES_SERVER=localhost
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password
POSTGRES_DB=amazon_analytics
POSTGRES_PORT=5432

# Redis
REDIS_URL=redis://localhost:6379

# Security
SECRET_KEY=your-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30

# AI APIs (optional)
OPENAI_API_KEY=sk-your-openai-api-key
ANTHROPIC_API_KEY=sk-ant-your-anthropic-api-key
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 API Documentation

Once the backend is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **ReDoc documentation**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Key API Endpoints

#### Products
- `GET /api/v1/products/` - List products with pagination
- `GET /api/v1/products/{asin}` - Get product details
- `POST /api/v1/products/` - Create new product
- `GET /api/v1/products/{asin}/price-history` - Price history

#### Analytics
- `GET /api/v1/analytics/overview` - Analytics overview
- `GET /api/v1/analytics/trends` - Trend data
- `GET /api/v1/analytics/top-products` - Top performing products

#### AI Services
- `POST /api/v1/ai/analyze-product` - AI product analysis
- `POST /api/v1/ai/generate-insights` - Generate insights from data
- `GET /api/v1/ai/health` - AI service health check

## 🗄 Database Schema

### Core Tables
- **products** - Product information and metadata
- **price_history** - Historical pricing data (TimescaleDB hypertable)
- **product_analytics** - Analytics and performance metrics

### Key Features
- **TimescaleDB** for efficient time-series data handling
- **Automatic indexing** for optimal query performance
- **JSON columns** for flexible metadata storage

## 🤖 AI Integration

The application is prepared for AI integration with:

### Supported AI Providers
- **OpenAI** (GPT models)
- **Anthropic** (Claude models)

### AI Features
- Product analysis and insights
- Trend analysis and predictions
- Automated recommendations
- Market intelligence

### Usage Example
```python
# Analyze a product
analysis = await ai_service.analyze_product(
    asin="B08N5WRWNW",
    analysis_type="comprehensive"
)

# Generate insights from data
insights = await ai_service.generate_insights(
    data=analytics_data,
    insight_type="trends"
)
```

## 🧪 Testing

### Backend Testing
```bash
cd backend
pytest
```

### Frontend Testing
```bash
cd frontend
npm run test
npm run type-check
```

## 📈 Performance Optimization

### Backend Optimizations
- **Async/await** throughout the application
- **Connection pooling** for database connections
- **Redis caching** for frequently accessed data
- **Database indexing** for optimal query performance

### Frontend Optimizations
- **Next.js 14** with app directory
- **React Query** for efficient data fetching and caching
- **Code splitting** for optimal bundle sizes
- **Image optimization** with Next.js Image component

## 🔒 Security Features

- **Input validation** with Pydantic
- **SQL injection protection** with SQLAlchemy
- **Rate limiting** with Nginx
- **CORS configuration**
- **Security headers**
- **Environment-based configuration**

## 🚀 Deployment

### Production Checklist
- [ ] Set strong `SECRET_KEY`
- [ ] Configure database credentials
- [ ] Set up SSL certificates
- [ ] Configure monitoring and logging
- [ ] Set up backup strategies
- [ ] Configure domain and DNS
- [ ] Set up CI/CD pipeline

### Scaling Considerations
- **Database scaling**: Read replicas, connection pooling
- **Application scaling**: Multiple backend instances
- **Caching**: Redis cluster for high availability
- **CDN**: For static assets and API responses
- **Monitoring**: Application performance monitoring

## 📋 Development Workflow

1. **Create feature branch**
2. **Develop and test locally**
3. **Run tests and type checks**
4. **Update documentation**
5. **Create pull request**
6. **Deploy to staging**
7. **Deploy to production**

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Database Connection Issues**
```bash
# Check if PostgreSQL is running
docker-compose ps postgres

# View PostgreSQL logs
docker-compose logs postgres
```

**Frontend Build Issues**
```bash
# Clear cache and reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

**Backend Import Issues**
```bash
# Ensure PYTHONPATH is set correctly
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

## 📞 Support

For support and questions:
- Create an issue in the GitHub repository
- Check the documentation in the `/docs` directory
- Review API documentation at `/docs` endpoint

---

Built with ❤️ for Amazon product analytics and business intelligence.