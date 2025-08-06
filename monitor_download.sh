#!/bin/bash

echo "Monitoring GPT-OSS 20B download..."
echo "Started at: $(date)"
echo "================================"

while true; do
    # Check if ollama process is still running
    if ! ps -p 3250 > /dev/null 2>&1; then
        echo "Download process completed or stopped!"
        
        # Check if model is available
        if ollama list | grep -q "gpt-oss:20b"; then
            echo "✅ GPT-OSS 20B successfully downloaded!"
            echo "Run: ollama run gpt-oss:20b"
        else
            echo "⚠️ Download may have failed. Retry with: ollama pull gpt-oss:20b"
        fi
        break
    fi
    
    # Get current progress
    PROGRESS=$(grep -o "[0-9]\+%" /tmp/ollama_download.log 2>/dev/null | tail -1)
    SPEED=$(grep -o "[0-9.]\+ MB/s" /tmp/ollama_download.log 2>/dev/null | tail -1)
    TIME_LEFT=$(grep -o "[0-9]\+m[0-9]\+s" /tmp/ollama_download.log 2>/dev/null | tail -1)
    
    echo -ne "\rProgress: ${PROGRESS:-0%} | Speed: ${SPEED:-0 MB/s} | ETA: ${TIME_LEFT:-calculating...}    "
    
    sleep 5
done

echo -e "\nCompleted at: $(date)"