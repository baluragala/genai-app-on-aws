#!/bin/bash

# Docker run script for RAG Application

set -e

echo "🐳 Starting RAG Application with Docker..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found. Creating from template..."
    cp .env.example .env
    echo "❌ Please edit .env file and add your OPENAI_API_KEY, then run this script again."
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "❌ Docker is not installed. Please install Docker first."
    exit 1
fi

# Check if Docker Compose is installed
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build and run
echo "🏗️  Building Docker image..."
docker-compose build

echo "▶️  Starting containers..."
docker-compose up -d

echo ""
echo "✨ Application started successfully!"
echo ""
echo "🌐 Access the application at: http://localhost:8501"
echo ""
echo "Useful commands:"
echo "  View logs:    docker-compose logs -f"
echo "  Stop:         docker-compose down"
echo "  Restart:      docker-compose restart"
echo ""

