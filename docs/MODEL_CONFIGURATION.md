# RAG Model Configuration - Implementation Summary

## Date
December 28, 2025

## Overview
Successfully configured the pi-rag system to use local GGUF models for both embedding and chat, with CPU-only execution (no GPU layers).

## Models Configured

### 1. Embedding Model: bge-m3-q8_0.gguf
- **Path**: `~/models/bge-m3-q8_0.gguf` (589M)
- **Type**: Embedding model
- **Dimensions**: 1024
- **Context Size**: 8194
- **GPU Layers**: 0 (CPU-only)
- **Status**: ✅ Tested and working

### 2. Chat Model: gemma-3-1b-it-UD-Q4_K_XL.gguf
- **Path**: `~/models/gemma-3-1b-it-UD-Q4_K_XL.gguf` (770M)
- **Type**: Chat/completion model
- **Context Size**: 8192
- **GPU Layers**: 0 (CPU-only)
- **Status**: ✅ Tested and working

### 3. External API (Fallback)
- **API URL**: https://u425-afb3-687d7019.singapore-a.gpuhub.com:8443/v1/chat/completions
- **Model**: Qwen3-Coder-30B-A3B-Instruct
- **Status**: Available as fallback, not default

## Configuration Changes Made

### 1. `configs/models_config.json`
```json
{
  "models": {
    "embedding": {
      "path": "~/models/bge-m3-q8_0.gguf",
      "type": "embedding",
      "n_ctx": 8194,
      "n_gpu_layers": 0,
      "n_batch": 512,
      "verbose": false
    },
    "chat": {
      "path": "~/models/gemma-3-1b-it-UD-Q4_K_XL.gguf",
      "type": "chat",
      "n_ctx": 8192,
      "n_gpu_layers": 0,
      "n_batch": 512,
      "verbose": false
    },
    "external_chat": {
      "is_external": true,
      "api_url": "https://u425-afb3-687d7019.singapore-a.gpuhub.com:8443/v1/chat/completions",
      "api_key": "",
      "model_name": "Qwen3-Coder-30B-A3B-Instruct",
      "type": "chat"
    }
  },
  "max_loaded_models": 2
}
```

### 2. `configs/rag_config.json`
```json
{
  "rag_enabled": true,
  "chunk_size": 500,
  "chunk_overlap": 50,
  "top_k": 3,
  "min_retrieval_score": 0.3,

  "embedding_model_path": "~/models/bge-m3-q8_0.gguf",
  "embedding_model_name": "embedding",
  "embedding_n_ctx": 8194,
  "embedding_n_gpu_layers": 0,
  "embedding_cache_enabled": true,
  "embedding_cache_size": 1000,

  "chat_model_path": "~/models/gemma-3-1b-it-UD-Q4_K_XL.gguf",
  "chat_model_name": "chat",
  "chat_n_ctx": 8192,
  "chat_n_gpu_layers": 0,

  "external_chat_api_url": "https://u425-afb3-687d7019.singapore-a.gpuhub.com:8443/v1/chat/completions",
  "external_chat_api_key": "",
  "use_external_chat_model": false,

  "temperature": 0.7,
  "max_tokens": 2048,

  "rag_api_port": 8001,
  "rag_api_host": "0.0.0.0"
}
```

## Code Fixes Applied

### 1. `rag/model_manager.py`
**Fixed**: Path expansion for `~` in model paths
- Added `os.path.expanduser()` to handle tilde in paths
- Line 171: `expanded_path = os.path.expanduser(config.path)`
- Line 182: `model_path=expanded_path` (instead of `config.path`)

**Fixed**: Embedding generation type detection
- Line 417-421: Changed from checking `hasattr(model, 'create_chat_completion')` to checking `config.is_external`
- This correctly identifies local vs external models

**Fixed**: Embedding return type handling
- Line 427-432: Simplified embedding handling since `model.embed()` returns a plain Python list

### 2. `rag/embedding.py`
**Fixed**: Removed debug print statement
- Line 165: Removed `print("Debug", uncached_texts)`

### 3. `api/main.py`
**Fixed**: Removed debug print statements
- Line 150: Removed `print(request.stream)`
- Line 193: Removed `print(result)`

## Important Notes

### Model Selection Issue
The original request was to use `embeddinggemma-300M-BF16.gguf`, but this model uses the 'gemma-embedding' architecture which is **not yet supported** by llama-cpp-python v0.3.16.

**Solution**: Used `bge-m3-q8_0.gguf` instead, which is:
- A proven, well-supported embedding model
- Generates 1024-dimensional embeddings
- Excellent for RAG applications
- Fully compatible with llama-cpp-python

## Testing Results

### ✅ All Tests Passed

1. **Model Manager**: Successfully registered 3 models (embedding, chat, external_chat)
2. **Embedding Service**: Successfully generated embeddings (1024 dimensions)
3. **Chat Model**: Successfully generated responses
4. **API Configuration**: All settings verified

### Performance Metrics
- **Embedding Model Load Time**: ~0.77 seconds
- **Chat Model Load Time**: ~1.16 seconds
- **Embedding Generation**: ~19.37 tokens/second
- **Chat Generation**: ~9.99 tokens/second

## Usage

### Starting the API Server
```bash
cd /home/dietpi/pi-rag
python -m uvicorn api.main:app --host 0.0.0.0 --port 8001
```

### Using the API

#### Default (Local Chat Model)
```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "chat",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

#### Using External Chat Model (Fallback)
```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "external_chat",
    "messages": [{"role": "user", "content": "Hello!"}],
    "stream": false
  }'
```

#### RAG Search
```bash
curl -X POST http://localhost:8001/v1/search \
  -H "Content-Type: application/json" \
  -d '{
    "query": "How does authentication work?",
    "top_k": 3
  }'
```

#### List Available Models
```bash
curl http://localhost:8001/v1/models
```

#### System Statistics
```bash
curl http://localhost:8001/v1/stats
```

## Memory Management

- **max_loaded_models**: 2 (both models can stay loaded)
- **Total Memory Required**: ~1.36GB (embedding: 589M + chat: 770M)
- **LRU Eviction**: Automatically unloads least recently used model when loading third model

## Future Enhancements

1. **Update llama-cpp-python**: When gemma-embedding architecture is supported, can use `embeddinggemma-300M-BF16.gguf`
2. **GPU Acceleration**: Set `n_gpu_layers` > 0 if GPU becomes available
3. **Model Scaling**: Increase `max_loaded_models` if more RAM available
4. **Batch Processing**: Optimize embedding generation for batch processing

## Verification Commands

```bash
# Check model files exist
ls -lh ~/models/bge-m3-q8_0.gguf ~/models/gemma-3-1b-it-UD-Q4_K_XL.gguf

# Test model manager
python3 -c "
from rag.model_manager import get_model_manager
manager = get_model_manager()
print(manager.get_stats())
"

# Test embeddings
python3 -c "
from rag.embedding import get_embedding_service
service = get_embedding_service()
embeddings = service.embed(['test'])
print(f'Generated {len(embeddings)} embeddings with {len(embeddings[0])} dimensions')
"

# Test chat
python3 -c "
from rag.orchestrator import get_orchestrator
orch = get_orchestrator()
result = orch.chat([{'role': 'user', 'content': 'Hello'}])
print(f'Response: {result[\"content\"]}')
"
```

## Troubleshooting

### Issue: Model file not found
**Solution**: Ensure models are in `~/models/` directory with correct filenames

### Issue: Out of memory
**Solution**:
- Reduce `max_loaded_models` in `models_config.json`
- Use smaller quantized models
- Close other applications

### Issue: Slow responses
**Solution**:
- This is expected for CPU-only inference
- Consider using GPU if available
- Use smaller models (Q2/Q3 quantization)

## Summary

✅ **Successfully configured local GGUF models for RAG**
✅ **Both embedding and chat models tested and working**
✅ **CPU-only configuration (no GPU layers)**
✅ **External API fallback available**
✅ **All configuration files updated**
✅ **Code fixes applied for path expansion and embedding generation**

The system is now ready for production use with the configured local models!
