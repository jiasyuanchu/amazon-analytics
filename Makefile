.PHONY: help install-backend install-frontend install dev-up dev-down prod-up prod-down test-backend test-frontend test clean

# Default target
help:
	@echo "Amazon Analytics Dashboard - Available Commands:"
	@echo ""
	@echo "Installation:"
	@echo "  install-backend    Install Python dependencies"
	@echo "  install-frontend   Install Node.js dependencies" 
	@echo "  install            Install all dependencies"
	@echo ""
	@echo "Development:"
	@echo "  dev-up             Start development environment"
	@echo "  dev-down           Stop development environment"
	@echo "  dev-backend        Start backend development server"
	@echo "  dev-frontend       Start frontend development server"
	@echo ""
	@echo "Production:"
	@echo "  prod-up            Start production environment"
	@echo "  prod-down          Stop production environment"
	@echo ""
	@echo "Testing:"
	@echo "  test-backend       Run backend tests"
	@echo "  test-frontend      Run frontend tests"
	@echo "  test               Run all tests"
	@echo ""
	@echo "Maintenance:"
	@echo "  clean              Clean up containers and volumes"
	@echo "  logs               Show container logs"

# Installation
install-backend:
	cd backend && pip install -r requirements.txt

install-frontend:
	cd frontend && npm install

install: install-backend install-frontend
	@echo "All dependencies installed!"

# Development
dev-up:
	docker-compose -f docker-compose.dev.yml up -d
	@echo "Development database and Redis are running!"
	@echo "Start backend: make dev-backend"
	@echo "Start frontend: make dev-frontend"

dev-down:
	docker-compose -f docker-compose.dev.yml down

dev-backend:
	cd backend && uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

dev-frontend:
	cd frontend && npm run dev

# Production
prod-up:
	docker-compose up --build -d
	@echo "Production environment is starting..."
	@echo "Visit: http://localhost"

prod-down:
	docker-compose down

# Testing
test-backend:
	cd backend && pytest

test-frontend:
	cd frontend && npm run test && npm run type-check

test: test-backend test-frontend

# Database
db-upgrade:
	cd backend && alembic upgrade head

db-downgrade:
	cd backend && alembic downgrade -1

db-migration:
	cd backend && alembic revision --autogenerate -m "$(MESSAGE)"

# Maintenance
clean:
	docker-compose down -v
	docker-compose -f docker-compose.dev.yml down -v
	docker system prune -f

logs:
	docker-compose logs -f

logs-backend:
	docker-compose logs -f backend

logs-frontend:
	docker-compose logs -f frontend

logs-db:
	docker-compose logs -f postgres