#!/bin/bash

# Quick Start Script for Free AI Agent App

echo "🤖 Free AI Agent Model App - Quick Start"
echo "========================================"
echo ""

# Check Python version
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION found"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip > /dev/null 2>&1
pip install -r requirements.txt

echo "✓ Dependencies installed"
echo ""

# Copy .env.example to .env if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "✓ .env file created. Edit it with your API keys if needed."
    echo ""
fi

echo "🎉 Setup complete!"
echo ""
echo "Next steps:"
echo ""
echo "Option 1 - Use Ollama (recommended for local/free):"
echo "  1. Install Ollama from https://ollama.ai"
echo "  2. Run: ollama pull llama3"
echo "  3. Run: python main.py"
echo ""
echo "Option 2 - Use Hugging Face:"
echo "  1. Get free API key from https://huggingface.co/settings/tokens"
echo "  2. Add to .env file: HUGGINGFACE_API_KEY=your_key"
echo "  3. Run: python main.py --provider huggingface"
echo ""
echo "Option 3 - Web Interface:"
echo "  1. Run: python app.py"
echo "  2. Open http://localhost:5000 in your browser"
echo ""
