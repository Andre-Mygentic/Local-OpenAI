#!/bin/bash

# OpenAI GPT-OSS 20B Local Setup Script
# This script installs everything needed to run GPT-OSS 20B locally

set -e  # Exit on error

echo "================================================"
echo "   OpenAI GPT-OSS 20B Local Setup"
echo "   For macOS (Apple Silicon & Intel)"
echo "================================================"
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

# Check operating system
check_os() {
    if [[ "$OSTYPE" != "darwin"* ]]; then
        print_error "This script is designed for macOS. For other systems, please follow manual installation."
        exit 1
    fi
    print_status "macOS detected"
}

# Check if running on Apple Silicon
check_architecture() {
    ARCH=$(uname -m)
    if [[ "$ARCH" == "arm64" ]]; then
        print_status "Apple Silicon detected (optimized performance)"
    else
        print_status "Intel Mac detected"
    fi
}

# Check available memory
check_memory() {
    # Get total memory in GB
    if [[ "$OSTYPE" == "darwin"* ]]; then
        TOTAL_MEM=$(sysctl hw.memsize | awk '{print int($2/1024/1024/1024)}')
    fi
    
    echo "Total RAM: ${TOTAL_MEM}GB"
    
    if [[ $TOTAL_MEM -lt 16 ]]; then
        print_warning "You have ${TOTAL_MEM}GB RAM. GPT-OSS 20B requires at least 16GB for optimal performance."
        read -p "Continue anyway? (y/n) " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    else
        print_status "Sufficient RAM detected (${TOTAL_MEM}GB)"
    fi
}

# Install Homebrew if not installed
install_homebrew() {
    if ! command -v brew &> /dev/null; then
        print_warning "Homebrew not found. Installing..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
        
        # Add Homebrew to PATH for Apple Silicon
        if [[ "$ARCH" == "arm64" ]]; then
            echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
            eval "$(/opt/homebrew/bin/brew shellenv)"
        fi
        print_status "Homebrew installed"
    else
        print_status "Homebrew is already installed"
    fi
}

# Install Ollama
install_ollama() {
    if ! command -v ollama &> /dev/null; then
        print_warning "Installing Ollama..."
        brew install ollama
        print_status "Ollama installed"
    else
        print_status "Ollama is already installed"
        ollama --version
    fi
    
    # Start Ollama service
    print_status "Starting Ollama service..."
    brew services start ollama
    sleep 3
}

# Download GPT-OSS 20B model
download_model() {
    echo ""
    echo "Checking for GPT-OSS 20B model..."
    
    if ollama list | grep -q "gpt-oss:20b"; then
        print_status "GPT-OSS 20B model already installed"
    else
        print_warning "GPT-OSS 20B model not found. This will download ~13GB."
        read -p "Download now? (y/n) " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "Downloading GPT-OSS 20B (this may take 10-30 minutes)..."
            ollama pull gpt-oss:20b
            print_status "GPT-OSS 20B model downloaded"
        else
            print_warning "Skipping model download. You can download it later with: ollama pull gpt-oss:20b"
        fi
    fi
}

# Check Python installation
check_python() {
    if command -v python3 &> /dev/null; then
        PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
        print_status "Python $PYTHON_VERSION found"
    else
        print_error "Python 3 not found. Please install Python 3.9 or higher"
        exit 1
    fi
}

# Setup Python virtual environment
setup_python_env() {
    echo ""
    echo "Setting up Python environment..."
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "ollama_ui_env" ]; then
        python3 -m venv ollama_ui_env
        print_status "Virtual environment created"
    else
        print_status "Virtual environment already exists"
    fi
    
    # Activate and install requirements
    source ollama_ui_env/bin/activate
    pip install --upgrade pip > /dev/null 2>&1
    
    print_status "Installing Python dependencies..."
    pip install -r requirements.txt
    
    print_status "Python environment ready"
}

# Test the installation
test_installation() {
    echo ""
    echo "Testing installation..."
    
    # Test Ollama
    if ollama list &> /dev/null; then
        print_status "Ollama is working"
    else
        print_error "Ollama test failed"
        exit 1
    fi
    
    # Test Python imports
    source ollama_ui_env/bin/activate
    python3 -c "import streamlit; import requests; import psutil" 2> /dev/null
    if [ $? -eq 0 ]; then
        print_status "Python dependencies are installed"
    else
        print_error "Python dependency test failed"
        exit 1
    fi
}

# Main installation flow
main() {
    echo "Starting installation process..."
    echo ""
    
    check_os
    check_architecture
    check_memory
    install_homebrew
    install_ollama
    download_model
    check_python
    setup_python_env
    test_installation
    
    echo ""
    echo "================================================"
    echo -e "${GREEN}Installation Complete!${NC}"
    echo "================================================"
    echo ""
    echo "To start the Streamlit UI, run:"
    echo "  ./run_ollama_ui.sh"
    echo ""
    echo "Or use the command line:"
    echo "  ollama run gpt-oss:20b"
    echo ""
    echo "For more information, see README.md"
    echo ""
}

# Run main function
main