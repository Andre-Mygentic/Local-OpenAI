"""
Streamlit UI for GPT-OSS 20B Model
Run with: streamlit run ollama_streamlit_app.py
"""

import streamlit as st
import requests
import json
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="GPT-OSS 20B Chat",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        color: #1f2937;
        margin-bottom: 1.5rem;
    }
    .chat-message {
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
    .user-message {
        background-color: #e3f2fd;
        margin-left: 20%;
    }
    .assistant-message {
        background-color: #f5f5f5;
        margin-right: 20%;
    }
    .stats-box {
        background-color: rgba(255, 255, 255, 0.1);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "model" not in st.session_state:
    st.session_state.model = "gpt-oss:20b"
if "temperature" not in st.session_state:
    st.session_state.temperature = 0.7
if "max_tokens" not in st.session_state:
    st.session_state.max_tokens = 3000
if "streaming" not in st.session_state:
    st.session_state.streaming = True

# Ollama API configuration
OLLAMA_API_BASE = "http://localhost:11434"

def check_ollama_status():
    """Check if Ollama is running and model is available"""
    try:
        response = requests.get(f"{OLLAMA_API_BASE}/api/tags", timeout=2)
        if response.status_code == 200:
            models = response.json().get("models", [])
            return True, [model["name"] for model in models]
        return False, []
    except:
        return False, []

def generate_response(prompt, model, temperature, max_tokens, streaming=True):
    """Generate response from Ollama API"""
    url = f"{OLLAMA_API_BASE}/api/generate"
    payload = {
        "model": model,
        "prompt": prompt,
        "temperature": temperature,
        "options": {
            "num_predict": max_tokens,
            "num_ctx": 4096  # Add context window
        },
        "stream": streaming,
        "keep_alive": "5m"  # Keep model loaded for 5 minutes
    }
    
    try:
        # Increase timeout for larger responses
        timeout = (10, 300) if streaming else 300  # (connect timeout, read timeout)
        response = requests.post(url, json=payload, stream=streaming, timeout=timeout)
        
        if streaming:
            full_response = ""
            try:
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            chunk = json.loads(line)
                            if "response" in chunk:
                                full_response += chunk["response"]
                                yield chunk["response"]
                            # Check if response is done
                            if chunk.get("done", False):
                                break
                        except json.JSONDecodeError:
                            continue
            except requests.exceptions.Timeout:
                yield "\n\n[Response truncated due to timeout. Try reducing max tokens or disabling streaming.]"
            except Exception as stream_error:
                yield f"\n\n[Streaming error: {str(stream_error)}]"
            return full_response
        else:
            return response.json().get("response", "Error: No response")
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The model may be processing a long response. Try reducing max tokens or enabling streaming."
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Please ensure Ollama is running (brew services start ollama)"
    except Exception as e:
        return f"Error: {str(e)}"

def chat_completion(messages, model, temperature, max_tokens, streaming=True):
    """Chat completion with conversation history"""
    url = f"{OLLAMA_API_BASE}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "options": {
            "num_predict": max_tokens,
            "num_ctx": 4096  # Add context window
        },
        "stream": streaming,
        "keep_alive": "5m"  # Keep model loaded for 5 minutes
    }
    
    try:
        # Increase timeout for larger responses
        timeout = (10, 300) if streaming else 300  # (connect timeout, read timeout)
        response = requests.post(url, json=payload, stream=streaming, timeout=timeout)
        
        if streaming:
            full_response = ""
            chunk_count = 0
            is_thinking = True
            thinking_marker_sent = False
            try:
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        try:
                            chunk = json.loads(line)
                            if "message" in chunk:
                                message = chunk["message"]
                                # Check if this is a thinking message (has thinking field)
                                if "thinking" in message:
                                    # Model is thinking, don't display this
                                    is_thinking = True
                                    # Send thinking marker only once
                                    if not thinking_marker_sent:
                                        yield "[THINKING]"
                                        thinking_marker_sent = True
                                elif "content" in message:
                                    # We have actual content to display (no thinking field)
                                    content = message["content"]
                                    if content is not None:
                                        is_thinking = False
                                        full_response += content
                                        chunk_count += 1
                                        yield content
                            # Check if response is done
                            if chunk.get("done", False):
                                # Log for debugging
                                print(f"Stream complete. Chunks: {chunk_count}, Total length: {len(full_response)}, Was thinking: {is_thinking}")
                                # If we got no content but finished, it might be all in thinking
                                if not full_response and "message" in chunk:
                                    # Check if there's a final message with content
                                    final_content = chunk.get("message", {}).get("content", "")
                                    if final_content:
                                        full_response = final_content
                                        yield final_content
                                break
                        except json.JSONDecodeError as e:
                            print(f"JSON decode error: {e}, Line: {line}")
                            continue
            except requests.exceptions.Timeout:
                yield "\n\n[Response truncated due to timeout. Try reducing max tokens or disabling streaming.]"
            except Exception as stream_error:
                print(f"Streaming error: {stream_error}")
                yield f"\n\n[Streaming error: {str(stream_error)}]"
            return full_response
        else:
            return response.json().get("message", {}).get("content", "Error: No response")
    except requests.exceptions.Timeout:
        return "Error: Request timed out. The model may be processing a long response. Try reducing max tokens or enabling streaming."
    except requests.exceptions.ConnectionError:
        return "Error: Cannot connect to Ollama. Please ensure Ollama is running (brew services start ollama)"
    except Exception as e:
        return f"Error: {str(e)}"

# Main app layout
st.markdown('<h1 class="main-header">🤖 OpenAI\'s GPT-OSS 20B Opensource Running Locally</h1>', unsafe_allow_html=True)

# Check Ollama status
ollama_running, available_models = check_ollama_status()

# Sidebar
with st.sidebar:
    st.header("⚙️ Settings")
    
    # Status indicator
    if ollama_running:
        st.success("✅ Ollama is running")
        
        # Model selection
        if available_models:
            selected_model = st.selectbox(
                "Select Model",
                available_models,
                index=available_models.index(st.session_state.model) if st.session_state.model in available_models else 0
            )
            st.session_state.model = selected_model
        else:
            st.warning("No models found. Pull a model first.")
    else:
        st.error("❌ Ollama is not running")
        st.code("brew services start ollama", language="bash")
    
    # Model parameters
    st.subheader("Model Parameters")
    
    st.session_state.temperature = st.slider(
        "Temperature",
        min_value=0.0,
        max_value=2.0,
        value=st.session_state.temperature,
        step=0.1,
        help="Higher values make output more random"
    )
    
    st.session_state.max_tokens = st.number_input(
        "Max Tokens",
        min_value=100,
        max_value=8000,
        value=st.session_state.max_tokens,
        step=100,
        help="Maximum number of tokens to generate"
    )
    
    st.session_state.streaming = st.checkbox(
        "Enable Streaming",
        value=st.session_state.streaming,
        help="Stream responses as they're generated"
    )
    
    # Chat controls
    st.subheader("Chat Controls")
    
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
    
    if st.button("💾 Export Chat", use_container_width=True):
        chat_export = json.dumps(st.session_state.messages, indent=2)
        st.download_button(
            label="Download JSON",
            data=chat_export,
            file_name=f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )
    
    # Model info
    st.subheader("Model Info")
    st.info(f"""
    **Current Model:** {st.session_state.model}
    **Size:** 13GB (quantized)
    **Parameters:** 20B
    **Architecture:** Transformer
    """)
    
    # Performance stats
    st.subheader("Performance")
    
    # Real message count
    message_count = len(st.session_state.messages)
    st.metric("Messages", message_count)
    
    # Calculate average response time from session
    if "response_times" not in st.session_state:
        st.session_state.response_times = []
    
    if st.session_state.response_times:
        avg_time = sum(st.session_state.response_times) / len(st.session_state.response_times)
        st.metric("Avg Response Time", f"{avg_time:.2f}s")
    else:
        st.metric("Avg Response Time", "No data yet")
    
    # Get actual memory usage
    try:
        import psutil
        # Get Ollama process memory
        for proc in psutil.process_iter(['pid', 'name', 'memory_info']):
            if 'ollama' in proc.info['name'].lower():
                mem_gb = proc.info['memory_info'].rss / (1024**3)
                st.metric("Memory Usage", f"{mem_gb:.1f} GB")
                break
        else:
            st.metric("Memory Usage", "N/A")
    except:
        st.metric("Memory Usage", "N/A")

# Main chat interface
if not ollama_running:
    st.error("⚠️ Please start Ollama to use the chat interface")
    st.code("brew services start ollama", language="bash")
else:
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Type your message here..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Generate and display assistant response
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            full_response = ""
            
            # Measure response time
            start_time = time.time()
            
            # Generate response
            if st.session_state.streaming:
                # Streaming response
                response_generator = chat_completion(
                    st.session_state.messages,
                    st.session_state.model,
                    st.session_state.temperature,
                    st.session_state.max_tokens,
                    streaming=True
                )
                
                # Show thinking indicator initially
                thinking_shown = False
                for chunk in response_generator:
                    if isinstance(chunk, str):
                        if chunk == "[THINKING]":
                            # Show thinking message
                            if not thinking_shown:
                                message_placeholder.markdown("*🤔 Thinking...*")
                                thinking_shown = True
                        elif chunk:  # Actual content
                            full_response += chunk
                            message_placeholder.markdown(full_response + "▌")
                
                # Final display without cursor
                if full_response:
                    message_placeholder.markdown(full_response)
                else:
                    message_placeholder.markdown("*[No response generated - the model may still be thinking. Try asking again or reducing max tokens.]*")
            else:
                # Non-streaming response
                with st.spinner("Thinking..."):
                    full_response = chat_completion(
                        st.session_state.messages,
                        st.session_state.model,
                        st.session_state.temperature,
                        st.session_state.max_tokens,
                        streaming=False
                    )
                message_placeholder.markdown(full_response)
            
            # Calculate response time
            response_time = time.time() - start_time
            
            # Track response time for metrics
            if "response_times" not in st.session_state:
                st.session_state.response_times = []
            st.session_state.response_times.append(response_time)
            # Keep only last 20 response times
            if len(st.session_state.response_times) > 20:
                st.session_state.response_times.pop(0)
            
            # Add assistant message to history
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
            # Show response time
            st.caption(f"Response generated in {response_time:.2f} seconds")

