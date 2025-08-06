#!/usr/bin/env python3
"""
Ollama API Example for Mac M4 Max
This script demonstrates how to use Ollama's API to interact with local LLMs
"""

import requests
import json
from typing import Dict, Any, Optional

class OllamaClient:
    """Simple client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        
    def list_models(self) -> Dict[str, Any]:
        """List all available models"""
        response = requests.get(f"{self.base_url}/api/tags")
        return response.json()
    
    def generate(self, model: str, prompt: str, stream: bool = False) -> Dict[str, Any]:
        """Generate a response from the model"""
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": stream
        }
        
        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload
        )
        
        if stream:
            # Handle streaming response
            for line in response.iter_lines():
                if line:
                    yield json.loads(line)
        else:
            return response.json()
    
    def chat(self, model: str, messages: list, stream: bool = False) -> Dict[str, Any]:
        """Chat with the model using conversation history"""
        payload = {
            "model": model,
            "messages": messages,
            "stream": stream
        }
        
        response = requests.post(
            f"{self.base_url}/api/chat",
            json=payload
        )
        
        if stream:
            # Handle streaming response
            for line in response.iter_lines():
                if line:
                    yield json.loads(line)
        else:
            return response.json()


# Alternative: Using OpenAI-compatible API
def use_openai_sdk():
    """Example using OpenAI SDK with Ollama"""
    try:
        from openai import OpenAI
        
        # Configure OpenAI client to use Ollama
        client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"  # Ollama doesn't require an API key
        )
        
        # Make a chat completion request
        response = client.chat.completions.create(
            model="tinyllama",  # Use any model you've pulled
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say hello from Dubai!"}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return response.choices[0].message.content
    except ImportError:
        return "OpenAI SDK not installed. Run: pip install openai"


def main():
    """Main function demonstrating various Ollama API features"""
    
    # Initialize Ollama client
    client = OllamaClient()
    
    print("=" * 50)
    print("Ollama API Example on Mac M4 Max")
    print("=" * 50)
    
    # 1. List available models
    print("\n1. Available Models:")
    print("-" * 30)
    try:
        models = client.list_models()
        for model in models.get("models", []):
            size_gb = model.get("size", 0) / (1024**3)
            print(f"  - {model['name']}: {size_gb:.2f} GB")
    except Exception as e:
        print(f"  Error listing models: {e}")
    
    # 2. Generate a simple response
    print("\n2. Simple Generation:")
    print("-" * 30)
    try:
        response = client.generate(
            model="tinyllama",
            prompt="Write a haiku about Dubai"
        )
        print(f"  {response.get('response', 'No response')}")
    except Exception as e:
        print(f"  Error generating response: {e}")
    
    # 3. Chat conversation
    print("\n3. Chat Conversation:")
    print("-" * 30)
    try:
        messages = [
            {"role": "user", "content": "What's the weather like in Dubai?"},
            {"role": "assistant", "content": "Dubai typically has a desert climate with hot summers and warm winters. Summer temperatures can exceed 40°C (104°F), while winters are mild around 20-25°C (68-77°F)."},
            {"role": "user", "content": "What's the best time to visit?"}
        ]
        
        response = client.chat(
            model="tinyllama",
            messages=messages
        )
        print(f"  User: {messages[-1]['content']}")
        print(f"  Assistant: {response.get('message', {}).get('content', 'No response')}")
    except Exception as e:
        print(f"  Error in chat: {e}")
    
    # 4. Streaming response
    print("\n4. Streaming Response:")
    print("-" * 30)
    print("  Prompt: Tell me a short fact about the M4 Max chip")
    print("  Response: ", end="", flush=True)
    try:
        for chunk in client.generate(
            model="tinyllama",
            prompt="Tell me a short fact about the M4 Max chip",
            stream=True
        ):
            if not chunk.get("done"):
                print(chunk.get("response", ""), end="", flush=True)
            else:
                print()  # New line at the end
    except Exception as e:
        print(f"\n  Error in streaming: {e}")
    
    # 5. Using OpenAI SDK (if available)
    print("\n5. OpenAI SDK Example:")
    print("-" * 30)
    result = use_openai_sdk()
    print(f"  {result}")
    
    print("\n" + "=" * 50)
    print("Performance Notes for M4 Max:")
    print("- Apple Silicon optimizations provide excellent inference speed")
    print("- 36GB RAM allows running models up to ~20B parameters comfortably")
    print("- Metal Performance Shaders acceleration is automatic")
    print("=" * 50)


if __name__ == "__main__":
    main()