# Rag Local Provider (Path A) for opencode CLI

## Overview
This document describes a local Rag provider integration that exposes Rag’s API via a Python FastAPI server and wires it into the opencode CLI in a local, llama.cpp/Ollama-like UX. The server runs on macOS, uses on-device embeddings and a CPU FAISS-like vector store, and delegates LLM generation to OpenRouter via a cloud API key stored in environment variables.

## Architecture Summary
- Local Rag server: Python FastAPI with OpenAI-compatible endpoints:
  - GET /health: readiness check
  - GET /v1/models: list available models
  - POST /v1/chat/completions: processes a query and returns OpenAI-style chat completion
    - Response: { "id": "...", "object": "chat.completion", "created": int, "model": "...", "choices": [{"index": 0, "message": {"role": "assistant", "content": "answer"}, "finish_reason": "stop"}] }
  - POST /v1/completions: text completion
- Rag core: EmbeddingService, VectorStore, Retriever, LLMController, RagOrchestrator
- Rag provider for opencode: Configured as OpenAI-compatible provider
  - Base URL: http://localhost:8000
  - Model: mistralai/devstral-2512:free
  - API Key: OpenRouter key for LLM generation

## Local Server Contract (Path A)
- Base URL: http://localhost:8000
- Endpoints:
  - GET /health -> {"status": "ok"}
  - GET /v1/models -> {"object": "list", "data": [{"id": "mistralai/devstral-2512:free", ...}]}
  - POST /v1/chat/completions
    - Body: {"model": "mistralai/devstral-2512:free", "messages": [{"role": "user", "content": "query"}]}
    - Response: OpenAI chat completion format with Rag-generated answer
- Auth: API key sent in request (not checked by server)

## Env & Configuration
- Rag server:
  - RAG_INDEX_PATH: path to index/docs on disk (default: ./rag_index)
  - RAG_TOP_K: number of top docs to retrieve (default: 5)
  - OPENROUTER_API_KEY: API key for LLM generation via OpenRouter
- opencode config (~/.config/opencode/opencode.jsonc):
  - Provider: pi-rag
  - baseURL: "http://localhost:8000"
  - apiKey: OpenRouter key
  - Models: {"mistralai/devstral-2512:free": {"name": "Mistral Devstral 2512 Free"}}

## opencode Integration (Provider Surface)
- Configured as OpenAI-compatible provider in opencode config
- Provider name: pi-rag
- Uses @ai-sdk/openai-compatible npm package
- Command: opencode run -m pi-rag/mistralai/devstral-2512:free "query"

## How to Run (Mac)
- Start server:
  - python3 -m uvicorn rag_server.main:app --reload --host 127.0.0.1 --port 8000
- Health check:
  - curl http://127.0.0.1:8000/health
- Query via opencode:
  - opencode run -m pi-rag/mistralai/devstral-2512:free "What is Rag?"
- Manual query:
  - curl -X POST http://127.0.0.1:8000/v1/chat/completions -H "Content-Type: application/json" -d '{"model": "mistralai/devstral-2512:free", "messages": [{"role": "user", "content": "What is Rag?"}]}'

## Security Considerations
- Do not commit OPENROUTER_API_KEY. Use env vars.
- Bind to localhost; consider additional token if you expose externally

## Extensibility
- Swap embedding models or vector stores if needed
- Add caching, batching, or a simple UI wrapper later

## Pi Porting Plan (Phase 2)
- Containerize with Docker ARM64 for Raspberry Pi
- Ensure Python 3 and dependencies available
- Reuse opencode config pointing to Pi-hosted server

## Patch Summary
- This document describes Path A local Rag server + opencode provider integration for a seamless, local-LM UX.