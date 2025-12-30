# Opencode MCP Configuration for RAG Memory System

## Quick Setup

### 1. MCP Server Configuration (JSON)

Add this to your Opencode MCP configuration:

```json
{
  "mcpServers": {
    "rag-memory": {
      "command": "python3",
      "args": [
        "-m",
        "mcp_server.rag_server"
      ],
      "env": {
        "RAG_DATA_DIR": "/opt/pi-rag/data",
        "LOG_LEVEL": "INFO",
        "EMBEDDING_MODEL_PATH": "/home/dietpi/models/bge-m3-q8_0.gguf"
      }
    }
  }
}
```

### 2. Alternative: Start Script

For easier management, use the provided launch script:

```bash
#!/bin/bash
# /home/dietpi/start_rag_mcp.sh

# Environment variables
export RAG_DATA_DIR="/opt/pi-rag/data"
export LOG_LEVEL="INFO"
export EMBEDDING_MODEL_PATH="/home/dietpi/models/bge-m3-q8_0.gguf"

# Start MCP server
cd /home/dietpi/pi-rag
python3 -m mcp_server.rag_server
```

Then configure Opencode to use:

```json
{
  "mcpServers": {
    "rag-memory": {
      "command": "/home/dietpi/start_rag_mcp.sh"
    }
  }
}
```

### 3. Verify Connection

In Opencode, check that all 10 tools are available:

```
Available MCP Tools:
- rag.list_projects
- rag.list_sources
- rag.get_context
- rag.search
- rag.ingest_file
- rag.add_fact
- rag.add_episode
- rag.create_project
- rag.delete_project
- rag.get_project_info
```

## Tool Usage Examples

### 1. Create a New Project

```python
result = await call_tool("rag.create_project", {
    "name": "myproject",
    "metadata": {"description": "Project for development"}
})
# Returns: project_id, name, project_dir
```

### 2. Add a Fact (Symbolic Memory)

```python
result = await call_tool("rag.add_fact", {
    "project_id": "myproject-abc12345",
    "fact_key": "user_preference",
    "fact_value": "prefers_dark_mode",
    "confidence": 0.95,
    "category": "preference"
})
# Returns: fact_id, status (authoritative)
```

### 3. Add an Episode (Episodic Memory)

```python
result = await call_tool("rag.add_episode", {
    "project_id": "myproject-abc12345",
    "title": "Code Refactoring Lesson",
    "content": """
        Situation: Large file with duplicated code
        Action: Extracted common functions into module
        Outcome: Reduced code by 40%, easier to maintain
        Lesson: Always look for code duplication before optimization
    """,
    "lesson_type": "pattern",
    "quality": 0.85
})
# Returns: episode_id, status (advisory)
```

### 4. Get Context (All Memory Types)

```python
result = await call_tool("rag.get_context", {
    "project_id": "myproject-abc12345",
    "context_type": "all",
    "query": "code optimization",
    "max_results": 10
})
# Returns:
# {
#   "symbolic": [...],      # Authoritative facts
#   "episodic": [...],      # Advisory lessons
#   "semantic": [...]       # Non-authoritative docs
# }
```

### 5. Search Across Memory

```python
result = await call_tool("rag.search", {
    "project_id": "myproject-abc12345",
    "query": "database optimization",
    "memory_type": "all",
    "top_k": 5
})
# Returns results sorted by authority (symbolic > episodic > semantic)
```

### 6. Ingest a File

```python
result = await call_tool("rag.ingest_file", {
    "project_id": "myproject-abc12345",
    "file_path": "/path/to/documentation.md",
    "source_type": "file",
    "metadata": {
        "category": "technical_docs",
        "version": "1.0"
    }
})
# Returns: doc_id, chunk_count, status (non-authoritative)
```

## Environment Variables

| Variable | Default | Description |
|----------|----------|-------------|
| `RAG_DATA_DIR` | `/opt/pi-rag/data` | Base directory for all project data |
| `LOG_LEVEL` | `INFO` | Logging level (DEBUG, INFO, WARNING, ERROR) |
| `EMBEDDING_MODEL_PATH` | Auto-detected | Path to embedding model (BGE-M3) |

## Memory Authority Hierarchy

When using `rag.get_context` or `rag.search`, results are prioritized:

1. **Symbolic Memory** (Authoritative)
   - Facts, preferences, constraints
   - Always returned, highest trust
   - Added via `rag.add_fact`

2. **Episodic Memory** (Advisory)
   - Experience, lessons learned
   - Returned when relevant, medium trust
   - Added via `rag.add_episode`

3. **Semantic Memory** (Non-Authoritative)
   - Document content, files
   - Only returned when explicitly requested
   - Lowest trust, must be verified

## Logs & Metrics

### View Logs
Logs are written to: `/opt/pi-rag/logs/rag-mcp.log`

Format: Pipe-delimited for human readability + analytics
```
2025-12-29T17:00:00 | INFO | mcp_server.rag_server | Starting RAG MCP Server | data_dir=/opt/pi-rag/data | node=pi5-01
```

### View Metrics
Metrics are written to: `/opt/pi-rag/loki-data/metrics.json`

Format: JSON for Prometheus/Grafana
```json
{
  "timestamps": [...],
  "data": {
    "tool_calls": {
      "rag.add_fact": {"total": 100, "errors": 2, "avg_latency_ms": 45.3}
    }
  }
}
```

## Troubleshooting

### Issue: "Project not found"
**Cause**: Project ID incorrect or project was deleted
**Fix**: Use `rag.list_projects` to get correct project ID

### Issue: "Invalid scope" error
**Cause**: Internal error - should not occur
**Fix**: Check logs at `/opt/pi-rag/logs/rag-mcp.log`

### Issue: Slow file ingestion
**Cause**: First-time embedding generation takes 30+ seconds
**Fix**: Embeddings are cached after first run. Use `LOG_LEVEL=INFO` to track progress.

### Issue: Tools not visible in Opencode
**Cause**: MCP server not running or configuration incorrect
**Fix**:
1. Start server in terminal: `python3 -m mcp_server.rag_server`
2. Check for "Logger initialized" message
3. Verify Opencode MCP configuration JSON syntax
4. Restart Opencode

## Performance Notes

- **Concurrent Projects**: Each project is isolated, no cross-project interference
- **Embedding Speed**: First run ~30s/file, cached runs ~2s/file
- **Search Speed**: <100ms for queries with existing embeddings
- **Memory Usage**: ~500MB base + ~100MB per active project
- **CPU Usage**: Embedding uses 100% CPU (single core), others are fast

## Next Steps

1. ✅ Connect Opencode to MCP server
2. ✅ Test all 10 tools through Opencode
3. ⏳ Set up observability stack (Prometheus + Grafana)
4. ⏳ Run stress tests
