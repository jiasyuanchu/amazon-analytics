#!/bin/bash

# Start production environment script

echo "Starting Amazon Analytics Production Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "Error: Docker is not running. Please start Docker and try again."
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "Error: .env file not found. Please create it from .env.example"
    exit 1
fi

# Build and start all services
echo "Building and starting production services..."
docker-compose up --build -d

echo "Production services are starting..."
echo ""
echo "Services:"
echo "- Application: http://localhost (via Nginx)"
echo "- Direct Frontend: http://localhost:3000"
echo "- Direct Backend API: http://localhost:8000"
echo "- API Documentation: http://localhost:8000/docs"
echo ""
echo "Use 'docker-compose logs -f' to view logs"
echo "Use 'docker-compose down' to stop services"