# 🤖 OpenAI GPT-OSS 20B - Run Locally on Mac

Run OpenAI's powerful GPT-OSS 20B model locally on your Mac with a beautiful Streamlit UI. One-click installation, no cloud required, 100% private.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Platform](https://img.shields.io/badge/platform-macOS-lightgrey.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)

## ✨ Features

- 🚀 **One-Command Installation** - Get up and running in minutes
- 💻 **Beautiful Web UI** - Clean Streamlit interface for chatting with GPT-OSS
- 🔒 **100% Local & Private** - Your data never leaves your machine
- ⚡ **Optimized for Apple Silicon** - Leverages Metal Performance Shaders
- 📊 **Real-time Stats** - Monitor performance, response times, and memory usage
- 💾 **Chat History** - Export and save your conversations

## 📋 Requirements

- **macOS** (Apple Silicon M1/M2/M3/M4 or Intel)
- **16GB+ RAM** (36GB recommended for best performance)
- **14GB free disk space** for the model
- **Python 3.9+** (usually pre-installed on Mac)

## 🚀 Quick Start

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/ollama-gpt-oss.git
cd ollama-gpt-oss
```

### Step 2: Run the Setup Script (One-Time)
```bash
chmod +x setup.sh
./setup.sh
```

This script will automatically:
- ✅ Install Homebrew (if needed)
- ✅ Install Ollama
- ✅ Download the GPT-OSS 20B model (13GB)
- ✅ Create Python virtual environment
- ✅ Install all dependencies
- ✅ Verify everything is working

**Note:** The model download may take 10-30 minutes depending on your internet speed.

### Step 3: Start the UI
```bash
./run_ollama_ui.sh
```

Then open your browser to: **http://localhost:8501**

That's it! You're now running GPT-OSS 20B locally! 🎉

## 💬 Usage

### Web UI (Recommended)
After running `./run_ollama_ui.sh`, you can:
- Chat with the model in real-time
- Adjust temperature and max tokens
- Export chat history
- Monitor performance metrics

### Command Line
```bash
ollama run gpt-oss:20b
```

### Python API
```python
import requests

response = requests.post('http://localhost:11434/api/generate', 
    json={
        "model": "gpt-oss:20b",
        "prompt": "Hello, how are you?"
    })
print(response.json()['response'])
```

## 📁 Project Structure
```
ollama-gpt-oss/
├── setup.sh                   # One-time setup script
├── run_ollama_ui.sh          # Start the Streamlit UI
├── ollama_streamlit_app.py   # Streamlit application
├── requirements.txt          # Python dependencies
├── ollama_api_example.py     # API usage examples
└── README.md                 # This file
```

## 🛠️ Troubleshooting

### Model Download Issues
If the download is interrupted, simply run:
```bash
ollama pull gpt-oss:20b
```
Ollama will resume from where it left off.

### Port Already in Use
If port 8501 is busy, you can specify a different port:
```bash
streamlit run ollama_streamlit_app.py --server.port 8502
```

### Memory Issues
GPT-OSS 20B requires significant RAM. If you experience issues:
- Close other applications
- Consider using a smaller model: `ollama pull llama3.1:8b`

## 🔧 Manual Installation

If you prefer to install components manually:

1. **Install Ollama:**
```bash
brew install ollama
brew services start ollama
```

2. **Download the model:**
```bash
ollama pull gpt-oss:20b
```

3. **Setup Python environment:**
```bash
python3 -m venv ollama_ui_env
source ollama_ui_env/bin/activate
pip install -r requirements.txt
```

4. **Run the UI:**
```bash
streamlit run ollama_streamlit_app.py
```

## 🎯 Performance

On Apple M4 Max (36GB RAM):
- **Model Load Time:** ~5 seconds
- **Average Response Time:** 2-3 seconds
- **Memory Usage:** 8-10GB when active
- **Token Generation:** ~30-50 tokens/second

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for releasing GPT-OSS as open-source
- Ollama team for the excellent local LLM runtime
- Streamlit for the amazing web framework

## ⭐ Star History

If you find this useful, please consider giving it a star!

## 📮 Contact

For issues, questions, or suggestions, please open an issue on GitHub.

---

**Made with ❤️ for the open-source community**