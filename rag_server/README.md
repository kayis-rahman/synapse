Rag Local Server (Python FastAPI)

This local server exposes a Rag query API to be consumed by the opencode CLI as a local provider. It uses on-device embeddings and a FAISS-like vector store, and delegates LLM generation to Rag OpenRouter API via the OPENROUTER_API_KEY env var.

Usage:
- Ensure prerequisites: Python 3.x, uvicorn, fastapi
- Install server requirements:
  - pip install fastapi uvicorn
- Start server:
  - RAG_INDEX_PATH=./rag_index RAG_TOP_K=5 OPENROUTER_API_KEY=<your-key> uvicorn rag_server.main:app --reload --port 8000
- Health check:
  - curl http://localhost:8000/health
- Query:
  - curl -sS -X POST http://localhost:8000/query -H 'Content-Type: application/json' -d '{"query": "What is Rag?", "top_k": 5}' | jq

Note: Do not commit OpenRouter API keys. Use environment variable OPENROUTER_API_KEY.
