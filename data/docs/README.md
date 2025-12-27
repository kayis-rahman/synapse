# pi-rag: Retrieval Augmented Generation System

## Overview

pi-rag is a local RAG system built with MLX and Qwen3 4B. It provides:

- Local inference using Qwen3 4B (4-bit quantized)
- Thinking mode for complex reasoning
- Transparent RAG augmentation
- OpenAI-compatible API
- Document ingestion and retrieval

## Key Components

### 1. Vector Store
- CPU-based vector storage
- Cosine similarity search
- Metadata filtering
- Persistent storage

### 2. Embedding Service
- MLX server integration
- LRU caching
- Batch processing
- Async operations

### 3. RAG Orchestrator
- Query augmentation with retrieved context
- Entity extraction
- Qwen3 thinking mode support
- RAG disable mechanism

## Usage

### Start Servers

```bash
./scripts/start_all.sh
```

### Ingest Documents

```bash
# Single file
python -m rag.ingest --file data/docs/README.md --tags "project:pi-rag,service:rag"

# Directory
python -m rag.bulk_ingest --directory data/docs --tags "project:pi-rag"
```

### Query System

```bash
curl -X POST http://localhost:8001/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "lmstudio-community/Qwen3-4B-Thinking-2507-MLX-4bit",
    "messages": [{"role": "user", "content": "How does the vector store work?"}]
  }'
```

## Configuration

- MLX Server: `configs/mlx_config.json`
- RAG System: `configs/rag_config.json`
- Environment: `.env` (copy from `.env.example`)

## Architecture

- MLX Server (port 8000): Model inference
- RAG API (port 8001): RAG augmentation and OpenAI-compatible endpoints

## Features

- 32,768 token context window
- Qwen3 thinking mode
- 4-bit quantization for efficiency
- Streaming responses
- Tool calling
- Metadata-based filtering
- Persistent vector store
