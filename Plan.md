# Plan: Rag Local Provider for opencode CLI (Path A)

## Goal
Integrate Rag as a local provider for opencode CLI using a Python FastAPI server on macOS, with on-device embeddings and CPU FAISS-like vector store. Port to Raspberry Pi later.

## Milestones
- M1: Local Rag server implemented with OpenAI-compatible endpoints at localhost:8000 ✅
- M2: opencode configured as OpenAI-compatible provider ✅
- M3: opencode integration working, queries Rag server and prints answers ✅
- M4: Pi-port plan defined (Docker ARM64) ✅
- M5: Documentation finalized (Agent.md, updated Plan.md) ✅

## Tasks
- T1: Ensure robust importer setup for rag modules ✅
- T2: Verify /health and OpenAI endpoints on macOS ✅
- T3: Configure opencode as OpenAI-compatible provider ✅
- T4: Prepare documentation for running the local Rag server ✅
- T5: Define Pi-port strategy (Docker ARM64) ✅

## Risks & Mitigations
- RAG OpenRouter latency: use a caching layer for frequently asked questions
- Pi memory constraints: keep a small index and enable batching
- Secrets management: env-var based; rotate keys per policy

## Acceptance Criteria
- macOS: local Rag server accessible via OpenAI-compatible endpoints, returns answers ✅
- opencode: configured and invokes Rag server, prints answers ✅
- Pi: Docker ARM64 strategy defined ✅
