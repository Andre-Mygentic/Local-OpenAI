#!/bin/bash

# Ollama API Examples using curl
# For Mac M4 Max with 36GB RAM

echo "========================================"
echo "Ollama API Examples (using curl)"
echo "========================================"

# 1. List available models
echo -e "\n1. Available Models:"
echo "------------------------"
curl -s http://localhost:11434/api/tags | python3 -m json.tool | grep '"name"' | head -5

# 2. Generate a simple response
echo -e "\n2. Simple Generation:"
echo "------------------------"
echo "Prompt: Write a haiku about Dubai"
curl -s http://localhost:11434/api/generate -d '{
  "model": "tinyllama",
  "prompt": "Write a haiku about Dubai",
  "stream": false
}' | python3 -c "import sys, json; print(json.load(sys.stdin).get('response', ''))"

# 3. Chat conversation
echo -e "\n3. Chat Conversation:"
echo "------------------------"
echo "User: What's special about the Apple M4 Max chip?"
curl -s http://localhost:11434/api/chat -d '{
  "model": "tinyllama",
  "messages": [
    {"role": "user", "content": "What'\''s special about the Apple M4 Max chip?"}
  ],
  "stream": false
}' | python3 -c "import sys, json; print('Assistant:', json.load(sys.stdin)['message']['content'])"

# 4. Model information
echo -e "\n4. Model Information:"
echo "------------------------"
curl -s http://localhost:11434/api/show -d '{
  "name": "tinyllama"
}' | python3 -c "import sys, json; data = json.load(sys.stdin); print(f\"Model: {data.get('modelfile', 'N/A')[:100]}...\")"

echo -e "\n========================================"
echo "Performance Notes for M4 Max:"
echo "- Ollama uses Metal for GPU acceleration"
echo "- 36GB RAM supports models up to ~20B parameters"
echo "- Quantized models (Q4, Q5) offer best speed/quality balance"
echo "========================================"