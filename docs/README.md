# pi-rag: Local RAG System with llama.cpp

**pi-rag** is a local Retrieval Augmented Generation (RAG) system built with **llama-cpp-python**, designed for efficient multi-model management. It uses GGUF models for both chat and embeddings, with dynamic model loading/unloading to optimize memory usage.

## Features

- **Multi-Model Support**: Load/unload GGUF models dynamically to manage memory
- **Local Inference**: Run chat and embedding models locally with llama.cpp
- **RAG Pipeline**: Transparent retrieval augmentation with configurable chunking
- **OpenAI-Compatible API**: Drop-in replacement for OpenAI endpoints
- **Memory Efficient**: LRU model eviction to stay within memory limits
- **Batch Ingestion**: CLI tools for single and bulk document ingestion
- **Caching**: Embedding cache to reduce redundant computations
- **Persistence**: Vector store persistence to disk

## Quick Start

### Prerequisites

- Python 3.11+
- llama.cpp built (with `llama-cpp-python` or standalone)
- GGUF model files (chat model + embedding model)
- 8-16GB RAM recommended

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/pi-rag.git
cd pi-rag

# Install dependencies
pip install -r requirements.txt

# For Metal (Apple Silicon) acceleration:
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python --force-reinstall --no-cache-dir
```

### Download Models

You'll need GGUF model files. Recommended models:

**Chat Model** (e.g., Qwen3 4B):
```bash
# From Hugging Face
huggingface-cli download Qwen/Qwen3-4B-GGUF qwen3-4b-q4_k_m.gguf --local-dir ./models
```

**Embedding Model** (e.g., nomic-embed-text):
```bash
huggingface-cli download nomic-ai/nomic-embed-text-v1.5-GGUF nomic-embed-text-v1.5.Q4_K_M.gguf --local-dir ./models
```

### Configure Models

Edit `configs/rag_config.json`:

```json
{
  "chat_model_path": "./models/qwen3-4b-q4_k_m.gguf",
  "embedding_model_path": "./models/nomic-embed-text-v1.5.Q4_K_M.gguf"
}
```

### Start RAG API

```bash
./scripts/start_rag_api.sh
```

### Verify Installation

```bash
# Check health
curl http://localhost:8001/health

# List models
curl http://localhost:8001/v1/models
```

## Usage

### Ingest Documents

#### Single File

```bash
python -m rag.ingest ./data/docs/readme.md
```

#### Bulk Directory

```bash
python -m rag.bulk_ingest ./data/docs --tags "project:pi-rag"
```

### Query the System

#### Using curl

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [
      {"role": "user", "content": "How does the vector store work?"}
    ]
  }'
```

#### Using Python

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8001/v1",
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="chat",
    messages=[
        {"role": "user", "content": "Explain the RAG pipeline"}
    ]
)

print(response.choices[0].message.content)
```

#### Search Documents Directly

```bash
curl -X POST http://localhost:8001/v1/search \
  -H "Content-Type: application/json" \
  -d '{"query": "vector store", "top_k": 5}'
```

#### Disable RAG for a Query

```python
response = client.chat.completions.create(
    model="chat",
    messages=[
        {"role": "system", "content": "disable-rag"},
        {"role": "user", "content": "What is Python?"}
    ]
)
```

### Model Management

#### Load/Unload Models via API

```bash
# Load chat model
curl -X POST http://localhost:8001/v1/models/chat/load

# Unload to free memory
curl -X POST http://localhost:8001/v1/models/chat/unload

# Check loaded models
curl http://localhost:8001/v1/models
```

#### Programmatic Model Management

```python
from rag import get_model_manager, ModelConfig

manager = get_model_manager()

# Register a new model
manager.register_model("qwen3", ModelConfig(
    path="./models/qwen3-4b-q4_k_m.gguf",
    model_type="chat",
    n_ctx=32768,
    n_gpu_layers=-1  # All layers on GPU
))

# Load model
model = manager.get_model("qwen3")

# Use model
response = model.create_chat_completion(
    messages=[{"role": "user", "content": "Hello!"}]
)

# Unload to free memory
manager.unload_model("qwen3")
```

## Configuration

### RAG Configuration (`configs/rag_config.json`)

```json
{
  "rag_enabled": true,
  "chunk_size": 500,
  "chunk_overlap": 50,
  "top_k": 3,
  "min_retrieval_score": 0.3,
  
  "index_path": "./data/rag_index",
  "docs_path": "./data/docs",
  
  "rag_disable_keyword": "disable-rag",
  
  "embedding_model_path": "./models/nomic-embed-text-v1.5.Q4_K_M.gguf",
  "embedding_model_name": "embedding",
  "embedding_n_ctx": 2048,
  "embedding_n_gpu_layers": -1,
  "embedding_cache_enabled": true,
  "embedding_cache_size": 1000,
  
  "chat_model_path": "./models/qwen3-4b-q4_k_m.gguf",
  "chat_model_name": "chat",
  "chat_n_ctx": 32768,
  "chat_n_gpu_layers": -1,
  
  "temperature": 0.7,
  "max_tokens": 2048,
  
  "rag_api_port": 8001,
  "rag_api_host": "0.0.0.0"
}
```

### Models Configuration (`configs/models_config.json`)

```json
{
  "max_loaded_models": 2,
  "models": {
    "chat": {
      "path": "./models/qwen3-4b-q4_k_m.gguf",
      "type": "chat",
      "n_ctx": 32768,
      "n_gpu_layers": -1
    },
    "embedding": {
      "path": "./models/nomic-embed-text-v1.5.Q4_K_M.gguf",
      "type": "embedding",
      "n_ctx": 2048,
      "n_gpu_layers": -1
    }
  }
}
```

## API Endpoints

### Health & Status

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Basic health check |
| `/health` | GET | Detailed health with model status |
| `/v1/stats` | GET | System statistics |

### Chat & Search

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/chat/completions` | POST | Chat with RAG augmentation |
| `/v1/search` | POST | Direct document search |
| `/v1/ingest` | POST | Ingest text via API |

### Model Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/models` | GET | List all models |
| `/v1/models/{name}/load` | POST | Load model into memory |
| `/v1/models/{name}/unload` | POST | Unload model from memory |

### Index Management

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/v1/index` | DELETE | Clear the RAG index |

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   User/API Requests                      │
└────────────────────────┬────────────────────────────────┘
                         │
               ┌─────────▼─────────┐
               │    FastAPI App     │
               │    Port: 8001      │
               └─────────┬─────────┘
                         │
               ┌─────────▼─────────┐
               │  RAGOrchestrator   │
               │  - Query Analysis  │
               │  - Context Inject  │
               └─────────┬─────────┘
                         │
         ┌───────────────┼───────────────┐
         │               │               │
┌────────▼────────┐ ┌────▼────┐ ┌───────▼───────┐
│  ModelManager    │ │Retriever│ │  VectorStore  │
│  - Load/Unload   │ │         │ │  - Cosine Sim │
│  - LRU Eviction  │ │         │ │  - Persist    │
└────────┬────────┘ └────┬────┘ └───────────────┘
         │               │
┌────────▼────────┐ ┌────▼────────────┐
│  llama.cpp       │ │EmbeddingService │
│  GGUF Models     │ │  - Cache        │
│  - Chat          │ │  - GGUF Model   │
│  - Embedding     │ └─────────────────┘
└─────────────────┘
```

## Project Structure

```
pi-rag/
├── configs/                   # Configuration files
│   ├── rag_config.json       # RAG settings
│   └── models_config.json    # Model registry
├── scripts/                   # Startup scripts
│   └── start_rag_api.sh      # Start API server
├── rag/                       # Core RAG implementation
│   ├── __init__.py           # Package exports
│   ├── model_manager.py      # Multi-model management
│   ├── vectorstore.py        # Vector storage
│   ├── embedding.py          # Embedding service
│   ├── retriever.py          # Document retrieval
│   ├── orchestrator.py       # RAG orchestration
│   ├── ingest.py             # Single file ingestion
│   └── bulk_ingest.py        # Bulk ingestion
├── api/                       # API layer
│   └── main.py               # FastAPI server
├── data/                      # Data storage
│   ├── rag_index/            # Vector store files
│   └── docs/                 # Source documents
├── models/                    # GGUF model files
├── tests/                     # Test suite
├── requirements.txt
└── README.md
```

## Troubleshooting

### Model Loading Fails

```bash
# Check if model file exists
ls -la ./models/*.gguf

# Verify llama-cpp-python installation
python -c "from llama_cpp import Llama; print('OK')"
```

### Out of Memory

- Reduce `n_ctx` in config
- Set `max_loaded_models: 1` to only load one model at a time
- Use smaller quantization (Q4_K_M instead of Q8)

### Slow Performance

- Enable Metal: `CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python`
- Increase `n_gpu_layers` to offload more to GPU
- Enable embedding cache in config

### RAG Not Finding Documents

- Ensure documents are ingested: `python -m rag.bulk_ingest ./data/docs`
- Check index exists: `ls ./data/rag_index/`
- Lower `min_retrieval_score` threshold
- Increase `top_k` for more results

## License

Apache 2.0

## Contributing

Contributions welcome! Please feel free to submit a Pull Request.
