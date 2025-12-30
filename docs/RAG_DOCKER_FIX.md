# Docker Issue Fix - Graceful Fallback for llama-cpp-python

## Problem
Docker container fails because `llama-cpp-python` needs `libgomp.so.1` (OpenMP library) which is missing.

## Solution
Instead of failing completely, make the RAG MCP server **gracefully degrade** when semantic memory is unavailable.

## Changes to `mcp_server/rag_server.py`

### 1. Add Graceful Fallback for Semantic Components

When semantic memory tools are called but llama-cpp is unavailable:
- Return helpful error messages
- Allow other tools (symbolic, episodic) to work
- Don't crash the entire server

### 2. Modified Methods

```python
# Line ~36 - Import semantic components with try/except
try:
    from rag import (
        SemanticStore, get_semantic_store,
        SemanticIngestor, get_semantic_ingestor,
        SemanticRetriever, get_semantic_retriever
    )
except ImportError as e:
    SEMANTIC_AVAILABLE = False
    logger.warning(f"Semantic memory not available: {e}")
else:
    SEMANTIC_AVAILABLE = True

# Line ~70 - Add check in get_semantic_store()
def _get_semantic_store(self) -> Optional[SemanticStore]:
    if not SEMANTIC_AVAILABLE:
        logger.warning("Semantic store not available - skipping")
        return None
    return get_semantic_store()

# Similar for _get_semantic_ingestor() and _get_semantic_retriever()
```

### 3. Update Tool Implementations

```python
# Line ~550 - Update list_sources
async def list_sources(self, project_id: str, source_type: Optional[str] = None):
    if not SEMANTIC_AVAILABLE:
        return {
            "sources": [],
            "total": 0,
            "message": "Semantic memory not available (llama-cpp-python library issue)",
            "warning": "Use symbolic/episodic memory instead"
        }
    # ... rest of implementation

# Line ~420 - Update get_context
async def get_context(self, project_id: str, context_type: str = "all", ...):
    # ... get symbolic and episodic ...
    
    # Only attempt semantic if available
    if SEMANTIC_AVAILABLE:
        # ... semantic retrieval ...
    else:
        result["message"] = f"Retrieved {len(result['symbolic']) + len(result['episodic'])} context item(s) (semantic unavailable)"
        result["warning"] = "Semantic memory unavailable due to library dependency"

# Line ~500 - Update search
async def search(self, project_id: str, query: str, ...):
    # ... get symbolic and episodic ...
    
    # Only attempt semantic if available
    if SEMANTIC_AVAILABLE:
        # ... semantic search ...
    else:
        result["message"] = f"Found {len(results)} result(s) (semantic unavailable)"
        result["warning"] = "Semantic search unavailable - use Postgres MCP tools for document analysis"

# Line ~540 - Update ingest_file
async def ingest_file(self, project_id: str, file_path: str, ...):
    if not SEMANTIC_AVAILABLE:
        return {
            "status": "error",
            "file_path": file_path,
            "error": "Semantic memory not available - requires llama-cpp-python",
            "message": "File ingestion requires semantic memory (unavailable due to Docker library issue)",
            "suggestion": "Use rag.add_fact or rag.add_episode to store information"
        }
    # ... rest of implementation
```

## Testing

After applying these changes, test:

```bash
# Server should start without errors
export RAG_DATA_DIR=/home/dietpi/pi-rag/data
python3 -m mcp_server.rag_server

# Tools should work:
# - rag.list_projects  ✅
# - rag.list_sources   ⚠️ (returns warning)
# - rag.get_context  ✅ (symbolic + episodic only)
# - rag.search        ✅ (symbolic + episodic only)
# - rag.add_fact      ✅
# - rag.add_episode   ✅
# - rag.ingest_file   ⚠️ (returns error with suggestion)
```

## Temporary Workaround

While Docker issue exists, **use the working tools**:

- ✅ **rag.list_projects** - List all projects
- ✅ **rag.add_fact** - Store decisions (authoritative)
- ✅ **rag.add_episode** - Store lessons learned (advisory)
- ✅ **rag.get_context** - Get facts + lessons (without semantic)
- ✅ **rag.search** - Search facts + lessons (without semantic)

These 5 tools provide powerful memory capabilities without needing llama-cpp!

## Long-Term Fix

To fully fix Docker, later you can:

1. **Use different base image** with pre-installed dependencies
2. **Build llama-cpp-python** from source with OpenMP disabled
3. **Use ARM64-specific pre-built wheels** from official repository

Until then, the graceful fallback allows your RAG MCP server to work!

---

**End of Docker Issue Fix Guide**
