# MCP Server - Opencode Integration Guide

## ✅ Quick Start (Recommended)

### Step 1: Copy Corrected Configuration

The corrected configuration file is at: `/home/dietpi/pi-rag/opencode_mcp_config.json`

Copy this content to your opencode configuration file:

```json
{
  "mcpServers": {
    "rag-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "RAG_DATA_DIR=/app/data",
        "-e", "LOG_LEVEL=INFO",
        "-v", "/home/dietpi/pi-rag/data:/app/data",
        "-v", "/home/dietpi/pi-rag/models:/app/models",
        "rag-mcp:latest"
      ],
      "cwd": "/home/dietpi/pi-rag"
    }
  }
}
```

**Key Changes from your config**:
- ✅ Fixed volume mount: `/home/dietpi/pi-rag/data:/app/data` (was `/host/data`)
- ✅ Added models volume mount for GGUF files
- ✅ Corrected path to actual project directory

### Step 2: Verify Docker Image Exists

```bash
docker images | grep rag-mcp
```

Should show:
```
rag-mcp:latest    847e95bcb09...    1.08GB
```

If not found, build it:

```bash
cd /home/dietpi/pi-rag
docker build -t rag-mcp:latest .
```

### Step 3: Create Data Directory (if not exists)

```bash
mkdir -p /home/dietpi/pi-rag/data/metrics
mkdir -p /home/dietpi/pi-rag/models
```

### Step 4: Test MCP Server Startup

```bash
# Test container starts correctly
docker run --rm \
  -e RAG_DATA_DIR=/app/data \
  -e LOG_LEVEL=INFO \
  -v /home/dietpi/pi-rag/data:/app/data \
  -v /home/dietpi/pi-rag/models:/app/models \
  rag-mcp:latest \
  echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | timeout 2 cat || true
```

Expected output (tool list):
```json
{
  "result": {
    "tools": [
      {
        "name": "rag.list_projects",
        "description": "List all projects in RAG memory system",
        ...
      },
      ...
    ]
  }
}
```

### Step 5: Restart Opencode

After updating your configuration, restart opencode to load the new MCP server configuration.

---

## 🛠 Available Tools (Quick Reference)

| Tool | Use Case | Example |
|------|------------|----------|
| `rag.list_projects` | List all projects | List available scopes |
| `rag.list_sources` | List document sources | See what files are indexed |
| `rag.get_context` | Get project context | Retrieve facts, lessons, docs together |
| `rag.search` | Search memory | Find specific information |
| `rag.ingest_file` | Add documents | Index code or documentation |
| `rag.add_fact` | Store facts | Remember decisions, preferences |
| `rag.add_episode` | Store lessons | Learn from experience |

---

## 📋 Example Tool Calls for Opencode

### 1. List Projects

```json
{
  "name": "rag.list_projects",
  "arguments": {}
}
```

### 2. Add a Fact (Authoritative Memory)

```json
{
  "name": "rag.add_fact",
  "arguments": {
    "project_id": "project",
    "fact_key": "framework",
    "fact_value": "Django 4.2",
    "confidence": 1.0,
    "category": "decision"
  }
}
```

### 3. Add an Episode (Lessons Learned)

```json
{
  "name": "rag.add_episode",
  "arguments": {
    "project_id": "project",
    "title": "Django async patterns",
    "content": "Situation: Need to handle database queries efficiently\nAction: Used async/await with Django ORM\nOutcome: 50% performance improvement\nLesson: Always use async for I/O operations in Django",
    "lesson_type": "pattern",
    "quality": 0.9
  }
}
```

### 4. Get Full Context (All Memory Layers)

```json
{
  "name": "rag.get_context",
  "arguments": {
    "project_id": "project",
    "context_type": "all",
    "query": "Django database",
    "max_results": 10
  }
}
```

### 5. Search Across All Memory

```json
{
  "name": "rag.search",
  "arguments": {
    "project_id": "project",
    "query": "Django views",
    "memory_type": "all",
    "top_k": 5
  }
}
```

### 6. Ingest a File

```json
{
  "name": "rag.ingest_file",
  "arguments": {
    "project_id": "project",
    "file_path": "/home/dietpi/pi-rag/docs/api.md",
    "source_type": "file",
    "metadata": {
      "tags": ["documentation", "api"]
    }
  }
}
```

---

## 🐳 Docker Management

### View Container Logs

```bash
# If opencode starts a container, find it:
docker ps | grep rag-mcp

# View logs:
docker logs -f <container_id>

# Or if container name is known:
docker logs -f rag-mcp
```

### Restart MCP Server

If you need to restart the MCP server:

1. **Stop opencode** (if running)
2. **Remove any existing containers**:
   ```bash
   docker ps -a | grep rag-mcp | awk '{print $1}' | xargs -r docker rm -f
   ```
3. **Restart opencode** (will start fresh MCP container)

### Rebuild Image

If you make changes to the code:

```bash
cd /home/dietpi/pi-rag

# Rebuild
docker build -t rag-mcp:latest .

# If container is running, remove and restart
docker ps -a | grep rag-mcp | awk '{print $1}' | xargs -r docker rm -f
```

---

## 📊 Monitoring

### Check Metrics

Metrics are stored in `/home/dietpi/pi-rag/data/metrics/`:

```bash
# List all metrics files
ls -la /home/dietpi/pi-rag/data/metrics/

# View specific project metrics
cat /home/dietpi/pi-rag/data/metrics/project_metrics.json | python3 -m json.tool
```

### Check Database Status

```bash
# Check SQLite databases
ls -la /home/dietpi/pi-rag/data/*.db

# Check vector index
ls -la /home/dietpi/pi-rag/data/semantic_index/
```

---

## 🚨 Troubleshooting

### Issue: Container won't start

**Symptom**: Opencode shows MCP server error

**Solution**:
```bash
# Test manually
docker run --rm \
  -e RAG_DATA_DIR=/app/data \
  rag-mcp:latest

# Check for errors in output
```

### Issue: Volume mount errors

**Symptom**: `no such file or directory` errors

**Solution**:
```bash
# Ensure directories exist
mkdir -p /home/dietpi/pi-rag/data
mkdir -p /home/dietpi/pi-rag/models

# Check permissions
ls -la /home/dietpi/pi-rag/
```

### Issue: Tools not found

**Symptom**: Opencode can't see MCP tools

**Solution**:
```bash
# Verify server starts and lists tools
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  docker run --rm -i \
    -e RAG_DATA_DIR=/app/data \
    -v /home/dietpi/pi-rag/data:/app/data \
    rag-mcp:latest
```

### Issue: Data persistence issues

**Symptom**: Data not saved between sessions

**Solution**:
```bash
# Check volume mounts are correct
docker inspect rag-mcp | grep -A 10 Mounts

# Should show:
# "Source": "/home/dietpi/pi-rag/data"
# "Destination": "/app/data"
```

---

## 📝 Memory Authority in Practice

### Example: Storing Framework Decision

```json
{
  "name": "rag.add_fact",
  "arguments": {
    "project_id": "project",
    "fact_key": "project.framework",
    "fact_value": "Django 4.2",
    "confidence": 1.0,
    "category": "decision"
  }
}
```

**Result**: This fact is **authoritative** - it will always be trusted over episodic/semantic memory.

### Example: Storing Lesson Learned

```json
{
  "name": "rag.add_episode",
  "arguments": {
    "project_id": "project",
    "title": "Async database queries",
    "content": "Situation: Database queries blocking request threads\nAction: Implemented async query pattern with Django ORM\nOutcome: 50% latency reduction\nLesson: Use Django's async ORM features for database operations",
    "lesson_type": "pattern",
    "quality": 0.85
  }
}
```

**Result**: This episode is **advisory** - it can suggest strategies but never overrides authoritative facts.

### Example: Context Retrieval

```json
{
  "name": "rag.get_context",
  "arguments": {
    "project_id": "project",
    "context_type": "all",
    "query": "database optimization",
    "max_results": 10
  }
}
```

**Response Structure**:
```json
{
  "symbolic": [
    {
      "key": "project.framework",
      "value": "Django 4.2",
      "authority": "authoritative"
    }
  ],
  "episodic": [
    {
      "title": "Async database queries",
      "lesson": "Use Django's async ORM features",
      "authority": "advisory"
    }
  ],
  "semantic": [
    {
      "content": "Django 4.2 includes async ORM support...",
      "citation": "[source:chunk-123]",
      "authority": "non-authoritative"
    }
  ],
  "message": "Retrieved 3 context item(s)"
}
```

**Note**: Results are **always ordered** by authority - symbolic first, then episodic, then semantic.

---

## 🎯 Best Practices

### 1. Use Facts for Decisions

- ✅ Use `rag.add_fact` for project decisions
- ✅ Set `category="decision"` for clarity
- ✅ Use `confidence=1.0` for certain facts
- ✅ Set `project_id` consistently

### 2. Use Episodes for Lessons

- ✅ Use `rag.add_episode` for learned patterns
- ✅ Write concise lessons (<500 chars)
- ✅ Include all 4 parts: Situation, Action, Outcome, Lesson
- ✅ Set `quality` based on confidence (0.7-1.0)

### 3. Use Semantic for Documentation

- ✅ Use `rag.ingest_file` for code/docs
- ✅ Tag files appropriately with metadata
- ✅ Use `rag.search` to find relevant documents
- ✅ Always include citations from semantic results

### 4. Get Context Before Writing

- ✅ Call `rag.get_context` with `context_type="all"`
- ✅ Check if information already exists in symbolic memory
- ✅ Use facts as ground truth
- ✅ Use episodes as suggestions
- ✅ Use semantic as reference

---

## 🔧 Configuration Options

### Change Log Level

Edit opencode config to add environment variable:

```json
{
  "mcpServers": {
    "rag-mcp": {
      "command": "docker",
      "args": [
        "run", "-i", "--rm",
        "-e", "RAG_DATA_DIR=/app/data",
        "-e", "LOG_LEVEL=DEBUG",  ← Change to DEBUG for detailed logs
        ...
      ]
    }
  }
}
```

### Use Different Data Directory

If you want data elsewhere:

```json
{
  "mcpServers": {
    "rag-mcp": {
      "args": [
        "-e", "RAG_DATA_DIR=/custom/path/data",
        "-v", "/custom/path/data:/app/data",
        ...
      ]
    }
  }
}
```

---

## 📞 Getting Help

### Documentation Files

- **This guide**: `MCP_OPENCODE_INTEGRATION_GUIDE.md`
- **Quick reference**: `MCP_SERVER_QUICKREF.md`
- **Implementation guide**: `MCP_SERVER_IMPLEMENTATION_GUIDE.md`
- **Deployment summary**: `MCP_DEPLOYMENT_SUMMARY.md`

### Check Logs

```bash
# Docker logs
docker logs -f rag-mcp

# Application logs
tail -f /home/dietpi/pi-rag/data/metrics/*.json
```

### Verify Server Status

```bash
# Check if Docker image exists
docker images | grep rag-mcp

# Test server responds
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | \
  docker run --rm -i rag-mcp:latest
```

---

## 🎉 Ready to Use!

Your MCP server is:

✅ **Built** - Docker image ready
✅ **Configured** - Correct opencode config provided
✅ **Tested** - All 7 tools functional
✅ **Documented** - Full integration guide
✅ **Production-ready** - Error handling, metrics, persistence

**Next Steps**:

1. Copy the corrected configuration from `opencode_mcp_config.json`
2. Paste it into `~/.opencode/opencode.jsonc`
3. Restart opencode to load the new MCP server
4. Start using the 7 RAG memory tools!

---

**End of Opencode Integration Guide**
