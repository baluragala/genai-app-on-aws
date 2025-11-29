#!/bin/bash

# Fix dependencies script for RAG Application

set -e

echo "🔧 Fixing package dependencies for Python 3.12..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '[0-9]+\.[0-9]+')
echo "📍 Detected Python $PYTHON_VERSION"

# Check if virtual environment exists
if [ -d venv ]; then
    echo "✅ Found virtual environment"
    source venv/bin/activate
else
    echo "⚠️  No virtual environment found. Creating one..."
    python3 -m venv venv
    source venv/bin/activate
fi

echo "📦 Uninstalling conflicting packages..."
pip uninstall -y langchain langchain-openai langchain-community langchain-core langchain-text-splitters openai chromadb unstructured langsmith pydantic pydantic-settings 2>/dev/null || true

echo "🧹 Cleaning pip cache..."
pip cache purge 2>/dev/null || true

echo "📥 Installing updated packages..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo ""
echo "✅ Dependencies fixed successfully!"
echo ""
echo "📝 Note: Using Python 3.12-compatible package versions"
echo "   - unstructured 0.11.8 (DOCX support available)"
echo "   - All other packages updated to latest compatible versions"
echo ""
echo "You can now run the application:"
echo "  ./run.sh"
echo "  or"
echo "  streamlit run app.py"
echo ""

