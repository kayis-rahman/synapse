---
title: Configuration Reference
description: SYNAPSE configuration options (reference)
---

> **Note:** This is a reference page. For getting started, see [Quick Start](./quick-start).

# Configuration Reference

This page documents all SYNAPSE configuration options for advanced customization.

## Environment Variables

Set these in your `.env` file:

```bash
# Server configuration
HOST=0.0.0.0
PORT=8002

# RAG configuration
PROJECT_ROOT=~/.synapse/data
CHUNK_SIZE=500
CHUNK_OVERLAP=50
```

## Configuration Files

### `configs/rag_config.json`

Main RAG configuration file:

```json
{
  "chunk_size": 500,
  "chunk_overlap": 50,
  "top_k": 3,
  "model_path": "models/bge-m3-q8_0.gguf",
  "mcp_port": 8002,
  "automatic_learning": {
    "enabled": true,
    "mode": "aggressive"
  }
}
```

### `configs/models_config.json`

Model registry:

```json
{
  "bge-m3": {
    "path": "models/bge-m3-q8_0.gguf",
    "size": "605MB",
    "type": "embedding"
  }
}
```

## Data Directory Structure

```
~/.synapse/data/
├── semantic_index/          # Document embeddings (vector store)
├── memory.db               # Symbolic memory (facts)
├── episodic.db             # Episodic memory (lessons)
└── registry.db              # Project registry
```

## Advanced Options

::details{label="Chunk Size Tuning"}
**Default:** 500 characters

Larger chunks = more context per result but less precise retrieval. Smaller chunks = more precise but less context.

```json
{
  "chunk_size": 1000,  // More context
  "chunk_size": 250    // More precise
}
```
:::
::details{label="Top-K Retrieval"}
**Default:** 3 results

Controls how many results are returned per query.

```json
{
  "top_k": 5  // More results
}
```
:::
::details{label="Automatic Learning"}
Enable intelligent learning from operations:

```json
{
  "automatic_learning": {
    "enabled": true,
    "mode": "aggressive",  // or "moderate", "minimal"
    "track_tasks": true,
    "track_code_changes": true,
    "track_operations": true
  }
}
```
:::

## Related Pages

- [Quick Start](./quick-start) - Get started in 5 minutes
- [CLI Commands](../api-reference/cli-commands) - All available commands
- [Architecture Overview](../architecture/overview) - How SYNAPSE works
