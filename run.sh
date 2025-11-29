#!/bin/bash

# Run script for RAG Application

set -e

echo "🚀 Starting RAG Application..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "❌ .env file not found. Please run setup.sh first or create .env from .env.example"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d venv ]; then
    echo "❌ Virtual environment not found. Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate

# Run the application
echo "▶️  Launching Streamlit application..."
streamlit run app.py

