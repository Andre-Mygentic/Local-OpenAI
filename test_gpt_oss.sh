#!/bin/bash

echo "=== Testing GPT-OSS 20B Model ==="
echo "================================"

# Test 1: Code Generation
echo -e "\n📝 Test 1: Code Generation"
echo "Write a Python function to reverse a string" | ollama run gpt-oss:20b --verbose 2>/dev/null | head -20

# Test 2: Math Problem
echo -e "\n🔢 Test 2: Math Problem"
echo "Solve: If x + 2y = 10 and x - y = 1, find x and y" | ollama run gpt-oss:20b --verbose 2>/dev/null | head -15

# Test 3: Creative Writing
echo -e "\n✍️ Test 3: Creative Writing"
echo "Write a haiku about artificial intelligence" | ollama run gpt-oss:20b --verbose 2>/dev/null

# Test 4: Reasoning
echo -e "\n🧠 Test 4: Logical Reasoning"
echo "If all roses are flowers, and some flowers fade quickly, can we conclude that some roses fade quickly?" | ollama run gpt-oss:20b --verbose 2>/dev/null | head -10

# Test 5: Check Response Time
echo -e "\n⏱️ Test 5: Response Time"
time echo "Say just 'Hello'" | ollama run gpt-oss:20b 2>/dev/null

echo -e "\n=== Tests Complete ==="