#!/bin/bash
# Launcher script for RAG Chatbot
# This ensures the virtual environment is activated

cd "$(dirname "$0")"

# Check command line arguments
MODE="web"
if [ "$1" = "--cli" ]; then
    MODE="cli"
fi

# Activate virtual environment if it exists
if [ -d "venv" ]; then
    source venv/bin/activate
    echo "✓ Virtual environment activated"
else
    echo "⚠️  Warning: No virtual environment found. Using system Python."
fi

# Run the main script
if [ "$MODE" = "cli" ]; then
    echo "💻 Starting RAG Chatbot CLI Interface..."
    python3 main.py --cli
else
    echo "🌐 Starting RAG Chatbot Web Interface..."
    python3 main.py
fi

