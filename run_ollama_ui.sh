#!/bin/bash

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "🚀 Starting GPT-OSS 20B Streamlit UI"
echo "===================================="

# Check if Ollama is running
if ! pgrep -x "ollama" > /dev/null; then
    echo "⚠️  Ollama is not running. Starting Ollama service..."
    brew services start ollama
    sleep 3
fi

# Check if model exists
if ! ollama list | grep -q "gpt-oss:20b"; then
    echo "❌ GPT-OSS 20B model not found!"
    echo "Run: ollama pull gpt-oss:20b"
    exit 1
fi

echo "✅ Ollama is running"
echo "✅ GPT-OSS 20B model is available"

# Change to script directory
cd "$SCRIPT_DIR"

# Activate virtual environment
echo "🔧 Activating Python virtual environment..."
source ollama_ui_env/bin/activate

# Launch Streamlit
echo "🌐 Launching Streamlit app..."
echo "===================================="
echo "📍 Opening in browser: http://localhost:8501"
echo "📍 Press Ctrl+C to stop"
echo "===================================="

streamlit run ollama_streamlit_app.py