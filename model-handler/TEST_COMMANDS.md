# Test Commands

Here are some curl commands you can use to test the Model Switcher API:

## 1. Test Basic Server Availability
```bash
curl http://localhost:6006/
```

## 2. List Available Models
```bash
curl http://localhost:6006/models
```

## 3. Switch to Qwen Model
```bash
curl -X POST http://localhost:6006/models/Qwen3-Coder-30B-A3B/switch
```

## 4. Switch to DeepSeek Model
```bash
curl -X POST http://localhost:6006/models/Deepseek-Coder-33b-Instruct/switch
```

## 5. Test Chat Completion with Qwen Model
```bash
curl -X POST http://localhost:6006/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3-Coder-30B-A3B",
    "messages": [{"role": "user", "content": "Hello, world!"}],
    "temperature": 0.7
  }'
```

## 6. Test Chat Completion with DeepSeek Model
```bash
curl -X POST http://localhost:6006/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Deepseek-Coder-33b-Instruct",
    "messages": [{"role": "user", "content": "Hello, world!"}],
    "temperature": 0.7
  }'
```

## 7. Check Current Status
```bash
curl http://localhost:6006/status
```

## 8. Test Invalid Model Name (Should Return 400)
```bash
curl -X POST http://localhost:6006/models/Invalid-Model/switch
```

## 9. Test Invalid Request Data (Should Return 400)
```bash
curl -X POST http://localhost:6006/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "Qwen3-Coder-30B-A3B",
    "messages": [{"role": "user", "content": "Hello, world!"}],
    "invalid_field": "should cause error"
  }'
```

## Usage Sequence Example:
1. First, check what models are available: `curl http://localhost:6006/models`
2. Switch to a model: `curl -X POST http://localhost:6006/models/Qwen3-Coder-30B-A3B/switch`
3. Test the model: `curl -X POST http://localhost:6006/chat/completions ...`
4. Check status: `curl http://localhost:6006/status`