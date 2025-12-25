# Model Switcher API Server

This directory contains the complete implementation for switching between Qwen3-Coder and DeepSeek-Coder models with an OpenAI-compatible API interface.

## Files

- **main.py** - FastAPI server with OpenAI-compatible endpoints
- **model_switcher.py** - Model management and switching logic  
- **start_server.sh** - Startup script to run the server directly
- **install_service.sh** - Script to install as a systemd service
- **model-switcher.service** - Systemd service configuration
- **README.md** - Basic usage instructions
- **SERVER_README.md** - Server usage documentation
- **ARCHITECTURE.md** - Solution architecture explanation

## Quick Start

### Option 1: Run directly with start script
```bash
./start_server.sh
```

### Option 2: Install as systemd service
```bash
sudo ./install_service.sh
sudo systemctl start model-switcher
sudo systemctl enable model-switcher
```

## API Endpoints

- `GET /` - Server information
- `GET /models` - List available models
- `POST /chat/completions` - Chat completions
- `POST /models/{model_name}/switch` - Switch models
- `GET /status` - Current model status

## Model Names

The API accepts these exact model names:
- `Qwen3-Coder-30B-A3B`
- `Deepseek-Coder-33b-Instruct`

## Usage Example

```bash
# Switch to Qwen model
curl -X POST "http://localhost:6006/models/Qwen3-Coder-30B-A3B/switch"

# Make a chat completion request
curl -X POST "http://localhost:6006/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3-Coder-30B-A3B",
    "messages": [{"role": "user", "content": "Hello, world!"}],
    "temperature": 0.7
  }'
```

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- llama.cpp server binaries
- Model files in models/ directory:
  - `Qwen3-Coder-30B-A3B-Instruct-Q5_K_M.gguf`
  - `deepseek-coder-33b-instruct.Q5_K_M.gguf`