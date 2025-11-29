#!/bin/bash
echo "🚀 Starting RAG Application..."
echo ""
cd "$(dirname "$0")"
source venv/bin/activate
streamlit run app.py
