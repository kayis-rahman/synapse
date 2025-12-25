# FastAPI Model Switcher Server

This FastAPI server provides an OpenAI-compatible API interface for switching between Qwen3-Coder and DeepSeek-Coder models.

## Features

- OpenAI-compatible `/chat/completions` endpoint
- `/models` endpoint to list available models
- `/status` endpoint to check current model status
- `/models/{model_name}/switch` endpoint to switch models
- Automatic model switching based on requests
- Unified API that works with either model

## Usage

### Start the server
```bash
python main.py
```

### Available endpoints:
- `GET /` - Server information
- `GET /models` - List available models
- `POST /chat/completions` - Chat completions (routes to active model)
- `POST /models/{model_name}/switch` - Switch to a specific model
- `GET /status` - Current model status

### Example API usage:
```bash
# Switch to Qwen model
curl -X POST "http://localhost:8000/models/qwen/switch"

# Get current status
curl -X GET "http://localhost:8000/status"

# Make a chat completion request
curl -X POST "http://localhost:8000/chat/completions" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen",
    "messages": [{"role": "user", "content": "Hello, world!"}],
    "temperature": 0.7
  }'
```

## Requirements

- Python 3.7+
- FastAPI
- Uvicorn
- The model_switcher.py script (included)

## Implementation Notes

This server provides a unified API interface that:
1. Automatically starts/stops models as needed
2. Routes requests to the currently active model
3. Provides a clean OpenAI-compatible interface
4. Maintains the correct port 6006 usage for models

Note: In a production environment, you would need to implement actual API calls to the running models rather than returning mock responses.