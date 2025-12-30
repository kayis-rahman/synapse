# Phase 3 Production Quick Start

**Status**: ✅ PRODUCTION READY - 100% Tested

---

## 5-Minute Quick Start

### Option A: Direct Python (Fastest)

```bash
cd /home/dietpi/pi-rag
./deploy_phase3_production.sh
```

That's it! The MCP server will start with Phase 3 (Episodic Memory) enabled.

### Option B: Docker (Production)

```bash
cd /home/dietpi/pi-rag

# Build and start
docker-compose -f docker-compose.phase3.yml up -d

# Check logs
docker-compose -f docker-compose.phase3.yml logs -f
```

---

## What You Get

### Working Features (Phase 3 Focused)

✅ **Episodic Memory** - Store lessons learned
   - Pattern discoveries
   - Mistakes and successes
   - Quality-scored episodes
   - Advisory (never authoritative)

✅ **MCP Server** - 5 tools for episodic memory
   - `rag.list_projects` - List projects
   - `rag.add_episode` - Store episode
   - `rag.get_context` - Retrieve episodes
   - `rag.search` - Search episodes
   - `rag.list_sources` - List documents

✅ **Docker Ready** - Production deployment
   - Multi-stage build
   - Health checks
   - Persistent storage

---

## First Episode Example

### Using Claude Desktop

After configuring your client (see below), try this:

```
You: Store this episode:
Situation: API calls were blocking the main thread and causing UI freezes
Action: Implemented async/await pattern using Python's asyncio library
Outcome: Response time improved by 60%, UI remains responsive
Lesson: Use async I/O for all network operations to prevent blocking

Claude: [calls rag.add_episode]
✅ Episode stored successfully!
Episode ID: abc-123-def-456
Type: pattern
Quality: 0.8
```

### Retrieving Episodes

```
You: What do you know about async patterns?

Claude: [calls rag.search]
Found 1 relevant episode:

**Async Pattern for API Calls**
Situation: API calls were blocking the main thread...
Action: Implemented async/await pattern...
Outcome: Response time improved by 60%...
Lesson: Use async I/O for all network operations...

Quality: 0.8 | Authority: advisory
```

---

## Client Configuration

### For Claude Desktop

**File**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "rag-mcp-phase3": {
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

### For Cursor/Cline

**File**: Cursor settings → MCP Servers

```json
{
  "rag-mcp-phase3": {
    "command": "python3",
    "args": ["-m", "mcp_server.rag_server"],
    "cwd": "/home/dietpi/pi-rag",
    "env": {
        "RAG_DATA_DIR": "/home/dietpi/pi-rag/data"
      }
  }
}
```

---

## Common Operations

### 1. Store a Pattern

```
Tool: rag.add_episode
Arguments:
{
  "project_id": "project",
  "title": "Async API Pattern",
  "content": "Situation: Blocked UI\nAction: Implemented async\nOutcome: 60% faster\nLesson: Always async I/O",
  "lesson_type": "pattern",
  "quality": 0.9
}
```

### 2. Store a Mistake

```
Tool: rag.add_episode
Arguments:
{
  "project_id": "project",
  "title": "Memory Leak",
  "content": "Situation: Connections not closed\nAction: Added context managers\nOutcome: Fixed\nLesson: Use 'with' for resources",
  "lesson_type": "mistake",
  "quality": 0.8
}
```

### 3. Search Episodes

```
Tool: rag.search
Arguments:
{
  "project_id": "project",
  "query": "database connection management",
  "memory_type": "episodic",
  "top_k": 5
}
```

### 4. Get All Episodes

```
Tool: rag.get_context
Arguments:
{
  "project_id": "project",
  "context_type": "episodic",
  "max_results": 20
}
```

---

## What's Different from Full System?

| Feature | Phase 3 Only | Full System |
|---------|---------------|-------------|
| **Episodic Memory** | ✅ Full | ✅ Full |
| **MCP Server** | ✅ 5 tools | ⏳ 7 tools (deferred) |
| **Symbolic Memory** | ⏳ Deferred | ⏳ Tests need updating |
| **Semantic Memory** | ⏳ Deferred | ⏳ Tests need updating |
| **Docker** | ✅ Ready | ✅ Ready |
| **Test Coverage** | 100% (Phase 3) | ~60% (mixed) |

---

## Migration Path to Full System

### When You're Ready to Add Phase 1 (Symbolic)

1. Update tests (2-3 hours estimated)
   ```bash
   # Fix test_symbolic_memory.py
   # Update to use current MemoryStore API
   ```

2. Run Phase 1 tests
   ```bash
   python3 -m pytest tests/test_symbolic_memory.py -v
   ```

3. Add to client config
   ```json
   "autoApprove": [
     "rag.add_fact",  // ADD THIS
     // ... other tools
   ]
   ```

### When You're Ready to Add Phase 4 (Semantic)

1. Update tests (1-2 hours estimated)
   ```bash
   # Fix test_semantic_memory.py
   # Use correct method names
   ```

2. Run Phase 4 tests
   ```bash
   python3 -m pytest tests/test_semantic_memory.py -v
   ```

3. Add to client config
   ```json
   "autoApprove": [
     "rag.ingest_file",  // ADD THIS
     // ... other tools
   ]
   ```

---

## Verification

### Quick Health Check

```bash
cd /home/dietpi/pi-rag

# Run Phase 3 tests
python3 -m pytest tests/test_episodic_memory.py -q

# Expected: 28 passed in ~0.3s

# Run MCP server tests
python3 test_mcp_server_comprehensive.py

# Expected: 8/8 tests passed
```

### Check Episode Storage

```bash
# View episodic database
python3 -c "
from rag import get_episodic_store
store = get_episodic_store('./data/episodic.db')
print(f'Episodes: {len(store.list_all())}')
print(f'Stats: {store.get_stats()}')
"
```

---

## Troubleshooting

### Server Won't Start

```bash
# Check data directory
ls -la /home/dietpi/pi-rag/data

# Fix permissions
chmod -R 755 /home/dietpi/pi-rag/data
```

### Tools Return Errors

```bash
# Run deployment script
./deploy_phase3_production.sh

# Check for errors in output
```

### Episodes Not Saving

```bash
# Check database exists
ls -la /home/dietpi/pi-rag/data/episodic.db

# Check permissions
chmod 644 /home/dietpi/pi-rag/data/episodic.db
```

---

## Support & Documentation

- **Full Deployment Guide**: `PHASE3_PRODUCTION_DEPLOYMENT.md`
- **Complete System Guide**: `AGENTIC_RAG_COMPLETE_GUIDE.md`
- **Test Results**: `MCP_SERVER_TEST_COMPLETE.md`

---

## Success Criteria

✅ **Phase 3 Production Ready**
- [x] Episodic memory 100% tested (28/28 tests)
- [x] MCP server fully functional
- [x] 5 tools working
- [x] Docker deployment verified
- [x] Client configurations provided
- [x] Quick start guide created
- [x] Troubleshooting documented

---

## Next Steps

**Immediate**: Deploy Phase 3 and start using episodic memory!

**Later**: When you need Phase 1 or 4, see "Migration Path to Full System" above.

---

**End of Quick Start**
