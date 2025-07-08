.PHONY: help dev install lint format test build clean docker-up docker-down

help:
	@echo "ValidateIO Development Commands:"
	@echo "  make dev        - Start development environment"
	@echo "  make install    - Install all dependencies"
	@echo "  make lint       - Run linters"
	@echo "  make format     - Format code"
	@echo "  make test       - Run tests"
	@echo "  make build      - Build for production"
	@echo "  make clean      - Clean build artifacts"
	@echo "  make docker-up  - Start Docker services"
	@echo "  make docker-down - Stop Docker services"

dev:
	@./scripts/dev.sh

install:
	@echo "Installing dependencies..."
	@cd frontend && npm install
	@cd backend && pip install -r requirements.txt
	@npm install

lint:
	@echo "Running linters..."
	@cd frontend && npm run lint
	@cd backend && ruff check .

format:
	@echo "Formatting code..."
	@cd frontend && npm run format
	@cd backend && black . && ruff check . --fix

test:
	@echo "Running tests..."
	@cd frontend && npm test
	@cd backend && pytest

build:
	@echo "Building for production..."
	@cd frontend && npm run build

clean:
	@echo "Cleaning build artifacts..."
	@rm -rf frontend/.next frontend/node_modules
	@rm -rf backend/__pycache__ backend/.pytest_cache backend/.venv
	@rm -rf node_modules

docker-up:
	@echo "Starting Docker services..."
	@docker-compose up -d

docker-down:
	@echo "Stopping Docker services..."
	@docker-compose down

docker-logs:
	@docker-compose logs -f