.PHONY: help setup install run test docker-build docker-up docker-down docker-logs clean

help:
	@echo "RAG Application - Makefile Commands"
	@echo ""
	@echo "Setup & Installation:"
	@echo "  make setup          - Set up virtual environment and install dependencies"
	@echo "  make install        - Install dependencies only"
	@echo ""
	@echo "Running:"
	@echo "  make run            - Run the application locally"
	@echo "  make test           - Run tests"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-build   - Build Docker image"
	@echo "  make docker-up      - Start Docker containers"
	@echo "  make docker-down    - Stop Docker containers"
	@echo "  make docker-logs    - View Docker logs"
	@echo ""
	@echo "Cleanup:"
	@echo "  make clean          - Remove generated files and caches"

setup:
	@echo "Setting up virtual environment..."
	python3 -m venv venv
	@echo "Installing dependencies..."
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "Creating .env file..."
	@if [ ! -f .env ]; then cp .env.example .env; echo "Please edit .env and add your OPENAI_API_KEY"; fi
	@mkdir -p logs data
	@echo "Setup complete!"

install:
	@echo "Installing dependencies..."
	pip install --upgrade pip
	pip install -r requirements.txt

run:
	@echo "Starting application..."
	streamlit run app.py

test:
	@echo "Running tests..."
	python test_rag.py

docker-build:
	@echo "Building Docker image..."
	docker-compose build

docker-up:
	@echo "Starting Docker containers..."
	docker-compose up -d
	@echo "Application available at http://localhost:8501"

docker-down:
	@echo "Stopping Docker containers..."
	docker-compose down

docker-logs:
	@echo "Showing Docker logs..."
	docker-compose logs -f

clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf build dist .pytest_cache .coverage htmlcov
	@echo "Cleanup complete!"

