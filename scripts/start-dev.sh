#!/bin/bash

# Start development environment script

echo "Starting Amazon Analytics Development Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from example..."
    cp .env.example .env
    echo "Please edit .env file with your API keys and configurations"
fi

# Start development services
echo "Starting development services..."
docker-compose -f docker-compose.dev.yml up -d postgres redis

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 10

# Run database migrations (optional - uncomment if needed)
# echo "Running database migrations..."
# docker-compose -f docker-compose.dev.yml exec backend-dev alembic upgrade head

echo "Development services are ready!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Start backend: cd backend && uvicorn app.main:app --reload"
echo "3. Start frontend: cd frontend && npm run dev"
echo ""
echo "Services:"
echo "- Frontend: http://localhost:3000"
echo "- Backend API: http://localhost:8000"
echo "- API Documentation: http://localhost:8000/docs"
echo "- PostgreSQL: localhost:5432"
echo "- Redis: localhost:6379"