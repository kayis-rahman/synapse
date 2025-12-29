# MCP Server Quick Reference

## 🚀 Quick Start

### Docker Deployment (Recommended)

```bash
# Build image
docker build -t rag-mcp:latest .

# Run container
docker run -i --rm \
  -e RAG_DATA_DIR=/app/data \
  -e LOG_LEVEL=INFO \
  -v $(pwd)/data:/app/data \
  rag-mcp:latest
```

### Docker Compose

```bash
# Start server
docker-compose -f docker-compose.mcp.yml up -d

# View logs
docker-compose -f docker-compose.mcp.yml logs -f

# Stop server
docker-compose -f docker-compose.mcp.yml down
```

### Direct Execution

```bash
# Set environment
export RAG_DATA_DIR=$(pwd)/data
export LOG_LEVEL=INFO

# Start server
python3 -m mcp_server.rag_server
```

---

## 🔌 Integration with Opencode

Add to opencode's MCP configuration:

```json
{
  "mcpServers": {
    "rag-mcp": {
      "command": "python3",
      "args": ["-m", "mcp_server.rag_server"],
      "cwd": "/home/dietpi/pi-rag",
      "env": {
        "RAG_DATA_DIR": "/home/dietpi/pi-rag/data",
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

---

## 🛠 Available Tools (7 Total)

| # | Tool | Purpose | Memory Layer | Authority |
|---|-------|---------|---------------|------------|
| 1 | `rag.list_projects` | List all projects | System | N/A |
| 2 | `rag.list_sources` | List document sources | Semantic | Non-authoritative |
| 3 | `rag.get_context` | Get context (all layers) | All 3 | Respects hierarchy |
| 4 | `rag.search` | Semantic search | All 3 | Respects hierarchy |
| 5 | `rag.ingest_file` | Ingest document | Semantic | Non-authoritative |
| 6 | `rag.add_fact` | Add fact | Symbolic | **Authoritative** |
| 7 | `rag.add_episode` | Add episode | Episodic | Advisory |

---

## 📋 Tool Examples

### 1. List Projects

```json
{
  "name": "rag.list_projects",
  "arguments": {
    "scope_type": "project"
  }
}
```

### 2. List Sources

```json
{
  "name": "rag.list_sources",
  "arguments": {
    "project_id": "proj_a1b2c3d4",
    "source_type": "file"
  }
}
```

### 3. Get Context

```json
{
  "name": "rag.get_context",
  "arguments": {
    "project_id": "proj_a1b2c3d4",
    "context_type": "all",
    "query": "Django authentication",
    "max_results": 10
  }
}
```

### 4. Search

```json
{
  "name": "rag.search",
  "arguments": {
    "project_id": "proj_a1b2c3d4",
    "query": "Django views",
    "memory_type": "all",
    "top_k": 5
  }
}
```

### 5. Ingest File

```json
{
  "name": "rag.ingest_file",
  "arguments": {
    "project_id": "proj_a1b2c3d4",
    "file_path": "/path/to/document.md",
    "source_type": "file",
    "metadata": {
      "tags": ["docs", "api"]
    }
  }
}
```

### 6. Add Fact (Authoritative)

```json
{
  "name": "rag.add_fact",
  "arguments": {
    "project_id": "proj_a1b2c3d4",
    "fact_key": "project.framework",
    "fact_value": "Django 4.2",
    "confidence": 1.0,
    "category": "decision"
  }
}
```

### 7. Add Episode (Advisory)

```json
{
  "name": "rag.add_episode",
  "arguments": {
    "project_id": "proj_a1b2c3d4",
    "title": "Learned about Django patterns",
    "content": "Situation: Need to handle async operations\nAction: Used async/await\nOutcome: Improved performance\nLesson: Use async/await for I/O operations",
    "lesson_type": "pattern",
    "quality": 0.9
  }
}
```

---

## 📊 Metrics

View metrics in `/home/dietpi/pi-rag/data/metrics/`:

```bash
# List all metrics files
ls -la /home/dietpi/pi-rag/data/metrics/

# View specific project metrics
cat /home/dietpi/pi-rag/data/metrics/<project_id>_metrics.json | python3 -m json.tool
```

---

## 🎯 Memory Authority Quick Reference

```
HIGHEST PRIORITY (Always trusted):
┌─────────────────────────────────┐
│  SYMBOLIC MEMORY             │  ← rag.add_fact
│  (Authoritative)             │
└─────────────────────────────────┘
              ↓ (never overrides)
MEDIUM PRIORITY (Suggestions only):
┌─────────────────────────────────┐
│  EPISODIC MEMORY            │  ← rag.add_episode
│  (Advisory)                 │
└─────────────────────────────────┘
              ↓ (never overrides)
LOWEST PRIORITY (Context only):
┌─────────────────────────────────┐
│  SEMANTIC MEMORY             │  ← rag.ingest_file
│  (Non-authoritative)          │
└─────────────────────────────────┘
```

**Rule**: Symbolic > Episodic > Semantic
- Symbolic memory always wins conflicts
- Episodic suggests but never overrides
- Semantic provides context with citations

---

## 🔧 Environment Variables

Set these before starting:

```bash
# Required
export RAG_DATA_DIR=/home/dietpi/pi-rag/data

# Optional
export LOG_LEVEL=INFO  # DEBUG, INFO, WARN, ERROR
```

---

## 📝 Project ID Format

Recommended: **Short UUID** (8 characters)

```python
# Backend generates automatically:
project_id = backend.generate_short_uuid()
# Example: "a1b2c3d4"
```

**Valid options**:
- Short UUID: `"a1b2c3d4"` (recommended)
- Scope names: `"user"`, `"project"`, `"org"`, `"session"`
- Any string: `"my-project"` (works but not recommended)

---

## 🐛 Quick Troubleshooting

| Issue | Solution |
|--------|----------|
| Server won't start | `python3 -m py_compile mcp_server/rag_server.py` |
| Tools not found | `python3 -c "from mcp_server import server; print(len(server._tools))"` |
| Import errors | `python3 -c "from rag import *; print('OK')"` |
| DB errors | Check `/home/dietpi/pi-rag/data/` permissions |

---

## 📞 Getting Help

- **Full guide**: `MCP_SERVER_IMPLEMENTATION_GUIDE.md`
- **Integration guide**: `MCP_SERVER_INTEGRATION_GUIDE.md`
- **Logs**: `/home/dietpi/pi-rag/data/metrics/`

---

**End of Quick Reference**
