# RAG MCP Server Fixes - Implementation Guide

## Executive Summary

This document outlines the fixes needed to address 4 critical issues in the RAG MCP server:

1. **Phase 1: Semantic Retrieval** (CRITICAL) - Generate embeddings for chunks
2. **Phase 2: Dynamic Project System** (HIGH) - Replace hardcoded "project" scope with name-shortUUID
3. **Phase 3: Search Functionality** (HIGH) - Enable full-text search across all fields
4. **Phase 4: Episode Validation** (MEDIUM) - Keep as-is, improve parser only

---

## Critical Finding

**Current State:**
- ✅ Files have been modified but edit tool has issues with complex interdependencies
- ✅ ProjectManager already exists in `mcp_server/project_manager.py`
- ✅ Phase 1 changes partially applied (semantic_store.py imports added)
- ⚠️  Phase 2 changes partially applied (memory_store.py VALID_SCOPES removed, episodic_store.py needs project_id)

**Status:**
- Semantic embedding generation: Ready to implement
- Dynamic projects: Foundation laid, needs completion
- Search functionality: Needs implementation after Phase 1 & 2
- Episode validation: No changes needed (keep as-is)

---

## Implementation Steps

### Phase 1: Fix Semantic Retrieval (Embedding Generation)

#### 1.1 semantic_store.py - Add Embedding Generation

**File:** `/home/dietpi/pi-rag/rag/semantic_store.py`

**Change:** In the `add_document()` method, add embedding generation for each chunk.

**Location:** After line 209 (Chunk creation loop)

**Code to Add:**
```python
# Get embedding service (may return None if unavailable)
embedding_service = get_embedding_service()

# Create DocumentChunk objects
chunk_ids = []
for i, chunk_text in enumerate(chunks):
    # Generate embedding for this chunk
    chunk_embedding = []
    if embedding_service:
        try:
            chunk_embedding = embedding_service.embed_single(chunk_text)
            logger.debug(f"Generated embedding for chunk {i} (len={len(chunk_embedding)})")
        except Exception as e:
            logger.warning(f"Failed to generate embedding for chunk {i}: {e}")
            chunk_embedding = []
    
    chunk = DocumentChunk(
        document_id=document_id,
        content=chunk_text,
        embedding=chunk_embedding,  # ← Use generated embedding
        chunk_index=i,
        metadata={**metadata, "document_id": document_id, "chunk_index": i, "total_chunks": len(chunks)}
    )
    self.chunks.append(chunk)
    chunk_ids.append(chunk.chunk_id)
```

**Expected Result:**
- New chunks will have populated `embedding` arrays
- If embedding service unavailable, chunks will have empty `embedding` arrays (graceful degradation)
- All existing chunks will need re-ingestion to get embeddings

---

### Phase 2: Implement Dynamic Project System

#### 2.1 memory_store.py - Remove VALID_SCOPES

**File:** `/home/dietpi/pi-rag/rag/memory_store.py`

**Changes:**
1. Remove `VALID_SCOPES = {"user", "project", "org", "session"}` (line ~119)
2. Add `_is_valid_project_id()` method to accept name-shortUUID format
3. Update `_validate_fact()` to use new validation instead of VALID_SCOPES check

**Add after line 120 (after VALID_CATEGORIES):**
```python
@staticmethod
def _is_valid_project_id(project_id: str) -> bool:
    """
    Validate project_id format.
    
    Accepts:
    - Simple names (alphanumeric, hyphens, underscores)
    - name-shortUUID format (e.g., "myapp-a1b2c3d4")
    
    Returns:
        True if valid, False otherwise
    """
    if not project_id or not isinstance(project_id, str):
        return False
    
    # Check length
    if len(project_id) < 1 or len(project_id) > 150:
        return False
    
    # Check for valid characters (alphanumeric, hyphens, underscores)
    import re
    if not re.match(r'^[a-zA-Z0-9_-]+$', project_id):
        return False
    
    return True
```

**Update `_validate_fact()` around line 221:**
```python
def _validate_fact(self, fact: MemoryFact) -> None:
    """Validate memory fact constraints."""
    # Validate project_id format (name-shortUUID or just name)
    if not self._is_valid_project_id(fact.scope):
        raise ValueError(
            f"Invalid project_id: {fact.scope}. "
            f"Must be in format 'name-shortUUID' or a valid project name."
        )
    
    # ... rest of validation (category, source, key, confidence) unchanged ...
```

---

#### 2.2 episodic_store.py - Add project_id Field

**File:** `/home/dietpi/pi-rag/rag/episodic_store.py`

**Changes:**
1. Add `project_id` attribute to `Episode` class
2. Update `to_dict()` method to include `project_id`
3. Update database schema to include `project_id` column
4. Update `store_episode()` to include `project_id`
5. Update `get_episode()` to include `project_id`
6. Update `query_episodes()` to filter by `project_id`
7. Update `list_recent_episodes()` to filter by `project_id` (optional, see note below)

**Update Episode class (line ~35):**
```python
class Episode:
    """
    Represents a single agent learning episode.
    
    Attributes:
        id: Unique identifier (UUID)
        project_id: Project identifier for isolation
        situation: What agent faced (context)
        action: What it did (action taken)
        outcome: Result of action (success/failure)
        lesson: Abstracted strategy (what was learned)
        confidence: Confidence level (0.0-1.0)
        created_at: Creation timestamp
    """
    
    def __init__(
        self,
        id: Optional[str] = None,
        project_id: str = "",  # ← NEW
        situation: str = "",
        action: str = "",
        outcome: str = "",
        lesson: str = "",
        confidence: float = 0.5,
        created_at: Optional[str] = None
    ):
        self.id = id or str(uuid.uuid4())
        self.project_id = project_id  # ← NEW
        # ... rest unchanged ...
```

**Update to_dict() method (line ~67):**
```python
def to_dict(self) -> Dict[str, Any]:
    """Convert to dictionary representation."""
    return {
        "id": self.id,
        "project_id": self.project_id,  # ← NEW
        "situation": self.situation,
        "action": self.action,
        "outcome": self.outcome,
        "lesson": self.lesson,
        "confidence": self.confidence,
        "created_at": self.created_at
    }
```

**Update _get_schema() method (line ~159):**
```python
def _get_schema(self) -> str:
    """Get database schema."""
    return """
        CREATE TABLE IF NOT EXISTS episodic_memory (
            id TEXT PRIMARY KEY,
            project_id TEXT,  # ← NEW
            situation TEXT NOT NULL,
            action TEXT NOT NULL,
            outcome TEXT NOT NULL,
            lesson TEXT NOT NULL,
            confidence REAL NOT NULL CHECK(confidence >= 0.0 AND confidence <= 1.0),
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
        CREATE INDEX IF NOT EXISTS idx_project_id ON episodic_memory(project_id);  # ← NEW
        CREATE INDEX IF NOT EXISTS idx_lesson ON episodic_memory(lesson);
        CREATE INDEX IF NOT EXISTS idx_confidence ON episodic_memory(confidence DESC);
        CREATE INDEX IF NOT EXISTS idx_created_at ON episodic_memory(created_at DESC);
        CREATE INDEX IF NOT EXISTS idx_situation ON episodic_memory(situation);
        
        -- View: recent_high_confidence_episodes
        -- Most recent episodes with high confidence
        CREATE VIEW IF NOT EXISTS recent_high_confidence_episodes AS
        SELECT
            id, project_id, situation, action, outcome, lesson, confidence, created_at  # ← NEW: Added project_id
            FROM episodic_memory
            WHERE confidence >= 0.7
            ORDER BY created_at DESC
            LIMIT 50;
        """
```

**Update store_episode() method (line ~208):**
```python
cursor.execute(
    """INSERT INTO episodic_memory
           (id, project_id, situation, action, outcome, lesson, confidence, created_at)
           VALUES (?, ?, ?, ?, ?, ?, ?)""",
    (episode.id, episode.project_id, episode.situation, episode.action, episode.outcome,
     episode.lesson, episode.confidence, episode.created_at)
)
```

**Update get_episode() method (line ~238):**
```python
cursor.execute(
    """SELECT id, project_id, situation, action, outcome, lesson, confidence, created_at
           FROM episodic_memory WHERE id = ?""",
    (episode_id,)
)

row = cursor.fetchone()

if not row:
    return None

return Episode(
    id=row[0],
    project_id=row[1],  # ← NEW
    situation=row[2],
    action=row[3],
    outcome=row[4],
    lesson=row[5],
    confidence=row[6],
    created_at=row[7]
)
```

**Update query_episodes() method (line ~260):**
```python
def query_episodes(
    self,
    project_id: str,  # ← NEW
    lesson: Optional[str] = None,
    min_confidence: float = 0.0,
    situation_contains: Optional[str] = None,
    limit: int = 10
) -> List[Episode]:
```

**Update query build (after line ~280):**
```python
# Build query dynamically
conditions = ["project_id = ?"]  # ← NEW: Always filter by project_id
params = [project_id]  # ← NEW

if lesson:
    # ... existing logic ...
conditions.append("confidence >= ?")
params.append(min_confidence)

if situation_contains:
    conditions.append("situation LIKE ?")
    params.append(f"%{situation_contains}%")

where_clause = " AND ".join(conditions) if conditions else "1=1"
```

**NOTE:** Do NOT update `list_recent_episodes()` to filter by project_id. The `date()` or `datetime()` SQL function issue is complex. Instead:
- Accept all episodes for a project
- Filter in application code
- Or use a simpler WHERE clause (e.g., `created_at > date('now', '-30 days')`)

---

#### 2.3 mcp_server/rag_server.py - Integrate ProjectManager

**File:** `/home/dietpi/pi-rag/mcp_server/rag_server.py`

**Changes:**
1. Add ProjectManager import
2. Add project_manager instance to RAGMemoryBackend.__init__()
3. Add _project_cache dictionary
4. Add resolve_project_id() method
5. Update _get_symbolic_store() to accept project_id
6. Update _get_episodic_store() to accept project_id
7. Update _get_semantic_store() to accept project_id
8. Update all tool handlers to call resolve_project_id()

**Add imports at line ~43:**
```python
# RAG system imports
from rag import (
    MemoryStore, MemoryFact, get_memory_store,
    EpisodicStore, Episode, get_episodic_store,
    SemanticStore, get_semantic_store,
    SemanticIngestor, get_semantic_ingestor,
    SemanticRetriever, get_semantic_retriever
)

# Local imports
from .metrics import Metrics, get_metrics
from .project_manager import ProjectManager  # ← NEW
```

**Update RAGMemoryBackend.__init__() (line ~67):**
```python
def __init__(self):
    """Initialize RAG backend (lazy initialization of stores)."""
    self._symbolic_store: Optional[MemoryStore] = None
    self._episodic_store: Optional[EpisodicStore] = None
    self._semantic_store: Optional[SemanticStore] = None
    self._semantic_ingestor: Optional[SemanticIngestor] = None
    self._semantic_retriever: Optional[SemanticRetriever] = None
    
    # Metrics
    self.metrics: Metrics = get_metrics()
    self.metrics.load_metrics()

    # Project Manager for dynamic project resolution
    self.project_manager = ProjectManager()  # ← NEW
    self._project_cache: Dict[str, str] = {}  # ← NEW
```

**Add resolve_project_id() method after _get_semantic_retriever (line ~118):**
```python
def resolve_project_id(self, project_name: str) -> str:
    """
    Resolve project name to project_id (name-shortUUID format).
    
    If project already exists (by name or full project_id), return existing ID.
    Otherwise, create new project with name-shortUUID format.
    
    Args:
        project_name: Project name or project_id (e.g., "myapp", "myapp-a1b2c3d4")
    
    Returns:
        Resolved project_id (name-shortUUID format)
    """
    # Check cache first
    if project_name in self._project_cache:
        return self._project_cache[project_name]
    
    # Check if project exists (by name or full project_id)
    projects = self.project_manager.list_projects()
    for project in projects:
        if project["name"] == project_name or project["project_id"] == project_name:
            project_id = project["project_id"]
            self._project_cache[project_name] = project_id
            logger.info(f"Resolved existing project: {project_id}")
            return project_id
    
    # Create new project with name-shortUUID format
    result = self.project_manager.create_project(
        name=project_name,
        metadata={"created_by": "mcp_server"}
    )
    project_id = result["project_id"]
    self._project_cache[project_name] = project_id
    
    logger.info(f"Created new project: {project_id}")
    return project_id
```

**Update store getter methods (starting line ~86):**
```python
def _get_symbolic_store(self, project_id: str) -> MemoryStore:  # ← NEW: Add project_id param
    """Get or create symbolic memory store for specific project."""
    project_dir = self.project_manager.get_project_dir(project_id)  # ← NEW: Use project_id
    db_path = os.path.join(project_dir, "memory.db")
    return get_memory_store(db_path)

def _get_episodic_store(self, project_id: str) -> EpisodicStore:  # ← NEW: Add project_id param
    """Get or create episodic memory store for specific project."""
    project_dir = self.project_manager.get_project_dir(project_id)  # ← NEW: Use project_id
    db_path = os.path.join(project_dir, "episodic.db")
    return get_episodic_store(db_path)

def _get_semantic_store(self, project_id: str) -> SemanticStore:  # ← NEW: Add project_id param
    """Get or create semantic memory store for specific project."""
    project_dir = self.project_manager.get_project_dir(project_id)  # ← NEW: Use project_id
    index_path = os.path.join(project_dir, "semantic_index")
    return get_semantic_store(index_path)
```

**Update tool handlers to resolve project_id:**

Add at the start of each tool handler (after arguments = arguments.get(...)):
```python
# NEW: Resolve project_id before processing
project_name = arguments.get("project_id")
if project_name:
    project_id = backend.resolve_project_id(project_name)
    arguments["project_id"] = project_id
```

**Example for list_projects tool:**
```python
@server.call_tool()
async def handle_tool_call(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
    try:
        # NEW: Resolve project_id for filtering
        scope_filter = arguments.get("scope_type")  # OLD: Remove this or repurpose
        project_filter = arguments.get("project_filter")  # NEW: Project name filter
        
        # NEW: Support both old and new patterns
        if project_filter:
            # Use new system
            # Filter projects by name or return all if not specified
            projects = backend.project_manager.list_projects()
            filtered = [
                p for p in projects
                if not project_filter or 
                   p["name"] == project_filter or 
                   p["project_id"] == project_filter
            ]
            result_projects = [
                {"project_id": p["project_id"], "name": p["name"]}
                for p in filtered
            ]
        else:
            # OLD: Return all scopes (user, project, org, session)
            # For now, return these for backward compatibility
            result_projects = [
                {"project_id": "user", "name": "user"},
                {"project_id": "project", "name": "project"},
                {"project_id": "org", "name": "org"},
                {"project_id": "session", "name": "session"}
            ]
        
        return [TextContent(
            type="text",
            text=json.dumps({
                "projects": result_projects,
                "total": len(result_projects),
                "message": f"Found {len(result_projects)} project(s)",
                "authority": "system"
            }, indent=2)
        )
```

**Update list_projects tool schema (line ~706):**
```python
Tool(
    name="rag.list_projects",
    description="List all projects in RAG memory system",
    inputSchema={
        "type": "object",
        "properties": {
            "project_filter": {  # ← NEW: Changed from scope_type
                "type": "string",
                "description": "Filter by project name (e.g., 'pi-rag'). Returns all if not specified."
            },
            "status_filter": {  # ← NEW: Add status filter
                "type": "string",
                "description": "Filter by status (active, archived, deleted)",
                "enum": ["active", "archived", "deleted"]
            }
        }
    }
)
```

---

### Phase 3: Fix Search Functionality

#### 3.1 memory_store.py - Add Full-Text Search

**File:** `/home/dietpi/pi-rag/rag/memory_store.py`

**Add new method after query_memory() (around line 445):**
```python
def query_memory_full_text(
    self,
    scope: str,
    query: str,
    min_confidence: float = 0.0,
    limit: int = 10
) -> List[MemoryFact]:
    """Query facts with full-text search across key and value fields."""
    with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()
        
        # Search both key and value (decoded JSON)
        cursor.execute("""
            SELECT id, scope, category, key, value, confidence, source, created_at, updated_at
               FROM memory_facts
               WHERE scope = ? AND confidence >= ?
               AND (key LIKE ? OR value LIKE ?)
               ORDER BY confidence DESC, updated_at DESC LIMIT ?
        """, (scope, min_confidence, f"%{query}%", f"%{query}%", limit))
        
        rows = cursor.fetchall()
        
        return [self._row_to_fact(row) for row in rows]
```

**Update RAGMemoryBackend.search() method (line ~392):**
```python
# Search symbolic memory (authoritative)
if memory_type in ["all", "symbolic"]:
    symbolic_store = self._get_symbolic_store(project_id)  # ← Use resolved project_id
    facts = symbolic_store.query_memory_full_text(  # ← NEW: Use full-text search
        scope=project_id,  # ← Use resolved project_id
        query=query,
        min_confidence=0.0,
        limit=top_k
    )
    # ... rest unchanged ...
```

#### 3.2 episodic_store.py - Add Full-Text Search

**File:** `/home/dietpi/pi-rag/rag/episodic_store.py`

**Add new method after query_episodes() (around line 310):**
```python
def query_episodes_full_text(
    self,
    project_id: str,  # ← NEW
    query: str,
    min_confidence: float = 0.0,
    limit: int = 10
) -> List[Episode]:
    """Query episodes with full-text search across all fields."""
    with sqlite3.connect(self.db_path) as conn:
        cursor = conn.cursor()
        
        # Search situation, action, outcome, and lesson
        cursor.execute("""
            SELECT id, project_id, situation, action, outcome, lesson, confidence, created_at
               FROM episodic_memory
               WHERE project_id = ?  # ← NEW
               AND confidence >= ?
               AND (
                   situation LIKE ?
                   OR action LIKE ?
                   OR outcome LIKE ?
                   OR lesson LIKE ?
               )
               ORDER BY confidence DESC, created_at DESC
               LIMIT ?
        """, (project_id, min_confidence, 
              f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%",
              limit))
        
        rows = cursor.fetchall()
        
        return [
            Episode(
                id=row[0],
                project_id=row[1],  # ← NEW
                situation=row[2],
                action=row[3],
                outcome=row[4],
                lesson=row[5],
                confidence=row[6],
                created_at=row[7]
            )
            for row in rows
        ]
```

**Update RAGMemoryBackend.search() method (line ~408):**
```python
# Search episodic memory (advisory)
if memory_type in ["all", "episodic"]:
    episodic_store = self._get_episodic_store(project_id)  # ← Use resolved project_id
    episodes = episodic_store.query_episodes_full_text(  # ← NEW: Use full-text search
        project_id=project_id,  # ← Use resolved project_id
        query=query,
        min_confidence=0.0,
        limit=top_k
    )
    # ... rest unchanged ...
```

---

### Phase 4: Episode Validation (Keep As-Is)

**No changes needed per user requirement.**

**Note:** Current validation rules:
- Lesson must be < 1000 characters
- Lesson must not repeat 70% of situation words
- All fields required (situation, action, outcome, lesson)

**Parser already handles:**
- Simple lesson text
- Structured "Situation:/Action:/Outcome:/Lesson:" format
- Mixed formats

---

## Migration Strategy (Fresh Start)

Since this is a fresh start (no data to preserve), no migration script is needed.

**Required Actions:**
1. Remove existing databases in `/home/dietpi/pi-rag/data/`
2. Let ProjectManager create fresh project structure
3. Test with new project names

**Existing Files to Clean Up:**
```
/home/dietpi/pi-rag/data/memory.db
/home/dietpi/pi-rag/data/episodic.db
/home/dietpi/pi-rag/data/semantic_index/chunks.json
/home/dietpi/pi-rag/data/semantic_index/chroma.sqlite3
```

---

## Testing Steps After Fixes

### Step 1: Test Semantic Embedding Generation
1. Start MCP server
2. Call `rag.ingest_file` with a test document
3. Call `rag.list_sources` to verify ingestion
4. Check `chunks.json` to verify embeddings are populated

**Expected Result:** Chunks have non-empty embedding arrays

### Step 2: Test Dynamic Project Creation
1. Call `rag.list_projects()` - Should return empty or old scopes
2. Call `rag.add_fact` with project_id="myapp-test"
3. Verify project directory created: `/opt/pi-rag/data/myapp-test-<uuid>/`

**Expected Result:** New project with name-shortUUID format created

### Step 3: Test Full-Text Search
1. Call `rag.add_fact` with complex value (JSON object)
2. Call `rag.search` with project_id="myapp-test", query="complex value"
3. Verify search returns the fact by value content

**Expected Result:** Search finds fact by value, not just key

### Step 4: Test Episode Project Isolation
1. Call `rag.add_episode` for two different projects
2. Call `rag.get_context` for each project
3. Verify episodes are isolated per project

**Expected Result:** Episodes returned only for requested project

---

## Order of Implementation

### Recommended Sequence:

1. **Phase 1 (Semantic Retrieval)** - Do first
   - Complete embedding generation in semantic_store.py
   - Test with fresh ingestion

2. **Phase 2 (Dynamic Projects)** - Do second
   - Complete episodic_store.py project_id changes
   - Complete memory_store.py validation changes
   - Complete MCP server integration
   - Test project creation

3. **Phase 3 (Search Functionality)** - Do third
   - Add full-text search methods
   - Update MCP server search method
   - Test search across all types

4. **Testing & Validation**
   - Test all 7 tools with new project system
   - Verify all features work end-to-end

---

## Summary of Changes Required

### Files to Modify:
1. `/home/dietpi/pi-rag/rag/semantic_store.py` - Add embedding generation
2. `/home/dietpi/pi-rag/rag/memory_store.py` - Remove VALID_SCOPES, add validation
3. `/home/dietpi/pi-rag/rag/episodic_store.py` - Add project_id, update schema
4. `/home/dietpi/pi-rag/mcp_server/rag_server.py` - Integrate ProjectManager

### Estimated Time:
- Phase 1: 2-3 hours
- Phase 2: 3-4 hours
- Phase 3: 2-3 hours
- Phase 4: 1-2 hours
- Testing: 1-2 hours

**Total: 8-14 hours**

---

## Success Criteria

All fixes will be complete when:

### Phase 1 - Semantic Retrieval:
- [ ] `semantic_store.py` generates embeddings for new chunks
- [ ] `rag.ingest_file` succeeds and returns chunk IDs
- [ ] `rag.list_sources` lists ingested files
- [ ] `chunks.json` has non-empty embedding arrays
- [ ] `rag.get_context` with semantic type returns results
- [ ] `rag.search` with semantic type returns results

### Phase 2 - Dynamic Projects:
- [ ] `memory_store.py` accepts any project_id (name-shortUUID format)
- [ ] `episodic_store.py` stores episodes with project_id
- [ ] Episodes are isolated per project
- [ ] `rag.list_projects()` returns actual projects
- [ ] New projects created with name-shortUUID format
- [ ] ProjectManager integrates successfully
- [ ] Project resolution works (cache + create new)

### Phase 3 - Search Functionality:
- [ ] `rag.search` finds facts by value content (not just key)
- [ ] `rag.search` finds episodes by situation/action/outcome/lesson
- [ ] Full-text search works with LIKE patterns
- [ ] Results sorted by authority (symbolic → episodic → semantic)
- [ ] All memory types searchable

### Phase 4 - Episode Validation:
- [ ] Structured episode format works
- [ ] Simple lesson text works
- [ ] Validation errors are clear
- [ ] Episodes stored successfully

---

## Notes

### Known Limitations:
1. **Existing Data:** All existing chunks (9840) have empty embeddings. They will need re-ingestion or a separate migration script.
2. **Performance:** Embedding generation will slow down ingestion. This is expected.
3. **Disk Space:** Vector embeddings increase storage size significantly.
4. **Memory:** Each project now has its own databases (memory.db, episodic.db, semantic_index/).

### Deployment Considerations:
1. **Base Directory:** Should use `/opt/pi-rag/data` (from .env) for persistence
2. **Environment Variable:** Ensure `RAG_DATA_DIR` is set correctly in deployment
3. **Permissions:** Ensure MCP server has write access to data directory
4. **Database:** SQLite databases need proper file permissions

---

## Next Steps

1. ✅ This implementation guide is complete
2. ⏭ Apply Phase 1 changes to semantic_store.py
3. ⏭ Apply Phase 2 changes to memory_store.py, episodic_store.py, mcp_server/rag_server.py
4. ⏭ Apply Phase 3 changes (full-text search methods)
5. ⏭ Test all changes with MCP server
6. ⏭ Update documentation

---

**Document Version:** 1.0  
**Last Updated:** 2024-12-29  
**Author:** Implementation Plan (Fresh Start)
