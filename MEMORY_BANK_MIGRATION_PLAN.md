# Memory-Bank to RAG Migration Plan

## Executive Summary

This document outlines the migration strategy from **memory-bank-mcp** to our **Production-Grade RAG System**. The RAG system provides **significant advantages** over the file-based memory-bank approach while maintaining all core functionality.

---

## Comparison: Memory-Bank vs RAG System

### Memory-Bank-MCP Architecture

**Storage**: Filesystem (markdown files)
```
memory-bank/
├── project1/
│   ├── projectbrief.md
│   ├── productContext.md
│   ├── systemPatterns.md
│   ├── techContext.md
│   ├── activeContext.md
│   ├── progress.md
│   └── .clinerules
└── project2/
    └── ...
```

**Capabilities**:
- ✅ Multi-project support
- ✅ File read/write/update
- ✅ Project listing
- ✅ File listing per project
- ❌ No semantic search (exact filename match only)
- ❌ No conflict resolution
- ❌ No confidence levels
- ❌ No cross-project learning
- ❌ Manual organization required

**Tools** (5 tools):
1. `list_projects` - List all projects
2. `list_project_files` - List files within a project
3. `memory_bank_read` - Read a specific file
4. `memory_bank_write` - Create new file
5. `memory_bank_update` - Update existing file

---

### RAG System Architecture

**Storage**: Database-backed with multi-layer memory
```
data/
├── memory.db          (Symbolic - Authoritative)
├── episodic.db        (Episodic - Advisory)
└── semantic_index/    (Semantic - Non-authoritative)
```

**Capabilities**:
- ✅ Multi-project support (via scope field)
- ✅ Semantic search (vector-based retrieval)
- ✅ Conflict resolution (highest confidence wins)
- ✅ Confidence levels (0.0-1.0)
- ✅ Cross-project learning (with scope isolation)
- ✅ Automatic organization (database indexes)
- ✅ Citation support (provenance tracking)
- ✅ Advisory episodic memory (lessons learned)
- ✅ Authority hierarchy (symbolic > episodic > semantic)

**Phases**:
- **Phase 1**: Symbolic Memory (Authoritative)
- **Phase 2**: Contextual Injection (Deterministic)
- **Phase 3**: Episodic Memory (Advisory)
- **Phase 4**: Semantic Memory (Non-authoritative)

---

## Memory-Bank File → RAG System Mapping

| Memory-Bank File | RAG System | Phase | Storage Method | Key Features |
|------------------|------------|-------|----------------|--------------|
| **projectbrief.md** | Symbolic Memory | 1 | Explicit facts | Goals, requirements, objectives with confidence levels |
| **productContext.md** | Symbolic Memory | 1 | Explicit facts | Problem context, solutions with version control |
| **systemPatterns.md** | Symbolic + Episodic | 1+3 | Facts + episodes | Architecture patterns + lessons learned |
| **techContext.md** | Symbolic Memory | 1 | Explicit facts | Tech stack, setup instructions |
| **activeContext.md** | Session variables | N/A | Current session | Working focus, decisions (ephemeral) |
| **progress.md** | Semantic + Episodic | 4+3 | Documents + episodes | Implementation status, recent work with citations |
| **.clinerules** | Symbolic Memory | 1 | Explicit facts | Workflow preferences, patterns |
| **features/*.md** | Semantic Memory | 4 | Document chunks | Feature specs with semantic search |
| **api/*.md** | Semantic Memory | 4 | Document chunks | API documentation with citation support |
| **deployment/*.md** | Semantic Memory | 4 | Document chunks | Deployment guides with version tracking |

---

## Tool Mapping Strategy

### Existing Memory-Bank Tools → RAG Tools

| Memory-Bank Tool | RAG Tool | Description | RAG Advantage |
|-----------------|----------|-------------|----------------|
| `list_projects` | `rag.list_projects` | List all projects | Query database instead of filesystem |
| `list_project_files` | `rag.list_sources` | List sources per project | Query database with metadata filtering |
| `memory_bank_read` | `rag.get_context` | Get project context | **Semantic search** (not exact match) + authority hierarchy |
| `memory_bank_write` | `rag.ingest_file` | Add new content | Automatic validation + confidence scoring |
| `memory_bank_update` | `rag.update_fact` or `rag.ingest_file` | Update existing | Conflict resolution + audit trail |

### New RAG Tools (Beyond Memory-Bank)

| Tool | Description | Why It's Better |
|------|-------------|-----------------|
| `rag.search` | Semantic search across all memory | Vector-based retrieval (not just filename) |
| `rag.add_episode` | Record lesson learned | Advisory memory for future planning |
| `rag.get_relevant_context` | Get context with authority hierarchy | Combines all phases (symbolic > episodic > semantic) |
| `rag.get_statistics` | Memory usage statistics | Database analytics (not possible with files) |
| `rag.backup_project` | Export project to markdown | Provides memory-bank format if needed |

---

## Implementation Plan

### Phase 1: Core MCP Tools (Priority: CRITICAL)

**Goal**: Replace all memory-bank MCP tools with RAG equivalents

**Tasks**:
1. ✅ Create MCP server framework (`mcp_server/server.py`) - **DONE** (mock only)
2. ❌ Implement real tool handlers (not mocks)
3. ❌ Add Docker configuration
4. ❌ Test tools against real database

**Deliverables**:
- `mcp_server/tools/list_projects.py` - List all project scopes
- `mcp_server/tools/list_sources.py` - List semantic sources per project
- `mcp_server/tools/get_context.py` - Get project context (hierarchical)
- `mcp_server/tools/ingest_file.py` - Ingest file into semantic memory
- `mcp_server/tools/update_fact.py` - Update symbolic memory fact

**Tool Specifications**:

#### 1. `rag.list_projects`
```typescript
{
  name: "rag.list_projects",
  description: "List all projects in the RAG memory system",
  inputSchema: {
    type: "object",
    properties: {
      scope_type: {
        type: "string",
        enum: ["user", "project", "org"],
        description: "Filter by scope type (optional)"
      }
    }
  }
}
```

**Implementation**:
```python
async def list_projects(scope_type: str = None):
    """
    List all projects in RAG memory system.

    Query: SELECT DISTINCT scope_id FROM memory_facts WHERE scope = ?
    """
    if scope_type:
        results = query("SELECT DISTINCT scope_id FROM memory_facts WHERE scope = ?", scope_type)
    else:
        results = query("SELECT DISTINCT scope_id FROM memory_facts")

    return {
        "projects": [row["scope_id"] for row in results],
        "total": len(results)
    }
```

#### 2. `rag.list_sources`
```typescript
{
  name: "rag.list_sources",
  description: "List all document sources for a project in semantic memory",
  inputSchema: {
    type: "object",
    properties: {
      project_id: {
        type: "string",
        description: "The project ID"
      },
      source_type: {
        type: "string",
        enum: ["file", "code", "web"],
        description: "Filter by source type (optional)"
      }
    },
    required: ["project_id"]
  }
}
```

**Implementation**:
```python
async def list_sources(project_id: str, source_type: str = None):
    """
    List all document sources for a project.

    Query: SELECT DISTINCT source_path, source_type, doc_type
           FROM semantic_documents
           WHERE project_id = ? AND (source_type = ? OR ? IS NULL)
    """
    query = """
    SELECT DISTINCT source_path, source_type, doc_type,
           COUNT(chunk_id) as chunk_count,
           MAX(ingested_at) as last_updated
    FROM semantic_documents
    WHERE project_id = :project_id
    """

    if source_type:
        query += " AND source_type = :source_type"

    query += " GROUP BY source_path, source_type, doc_type ORDER BY last_updated DESC"

    results = execute(query, {"project_id": project_id, "source_type": source_type})

    return {
        "sources": [
            {
                "path": row["source_path"],
                "type": row["source_type"],
                "doc_type": row["doc_type"],
                "chunk_count": row["chunk_count"],
                "last_updated": row["last_updated"]
            }
            for row in results
        ],
        "total": len(results)
    }
```

#### 3. `rag.get_context`
```typescript
{
  name: "rag.get_context",
  description: "Get comprehensive project context with authority hierarchy (symbolic > episodic > semantic)",
  inputSchema: {
    type: "object",
    properties: {
      project_id: {
        type: "string",
        description: "The project ID"
      },
      context_type: {
        type: "string",
        enum: ["all", "symbolic", "episodic", "semantic"],
        description: "Type of context to retrieve (default: all)"
      },
      query: {
        type: "string",
        description: "Query for semantic retrieval (optional, for context_type='semantic' or 'all')"
      },
      max_results: {
        type: "integer",
        description: "Maximum results per memory type (default: 10)"
      }
    },
    required: ["project_id"]
  }
}
```

**Implementation**:
```python
async def get_context(project_id: str, context_type: str = "all", query: str = None, max_results: int = 10):
    """
    Get comprehensive project context with authority hierarchy.

    Returns context in order: Symbolic (authoritative) → Episodic (advisory) → Semantic (non-authoritative)
    """
    context = {}

    # 1. Symbolic Memory (Authoritative)
    if context_type in ["all", "symbolic"]:
        symbolic_facts = query("""
            SELECT fact_key, fact_value, confidence, updated_at, category
            FROM memory_facts
            WHERE scope = 'project' AND scope_id = ?
            AND status = 'active'
            ORDER BY confidence DESC, updated_at DESC
            LIMIT ?
        """, project_id, max_results)

        context["symbolic"] = [
            {
                "key": fact["fact_key"],
                "value": fact["fact_value"],
                "confidence": fact["confidence"],
                "category": fact["category"],
                "authority": "authoritative"
            }
            for fact in symbolic_facts
        ]

    # 2. Episodic Memory (Advisory)
    if context_type in ["all", "episodic"]:
        episodes = query("""
            SELECT episode_id, title, summary, lesson_type, quality, created_at
            FROM episodes
            WHERE project_id = ?
            AND status = 'validated'
            ORDER BY quality DESC, created_at DESC
            LIMIT ?
        """, project_id, max_results)

        context["episodic"] = [
            {
                "episode_id": ep["episode_id"],
                "title": ep["title"],
                "summary": ep["summary"],
                "lesson_type": ep["lesson_type"],
                "quality": ep["quality"],
                "authority": "advisory"
            }
            for ep in episodes
        ]

    # 3. Semantic Memory (Non-authoritative)
    if context_type in ["all", "semantic"] and query:
        from rag.semantic_retriever import SemanticRetriever

        retriever = SemanticRetriever()
        results = retriever.search(
            query=query,
            project_id=project_id,
            top_k=max_results,
            min_similarity=0.3
        )

        context["semantic"] = [
            {
                "chunk_id": r["chunk_id"],
                "content": r["chunk_content"],
                "source": r["source_path"],
                "similarity": r["similarity"],
                "citation": f"[source:{r['chunk_id']}]",
                "authority": "non-authoritative"
            }
            for r in results
        ]

    return context
```

#### 4. `rag.ingest_file`
```typescript
{
  name: "rag.ingest_file",
  description: "Ingest a file into semantic memory with automatic validation and chunking",
  inputSchema: {
    type: "object",
    properties: {
      project_id: {
        type: "string",
        description: "The project ID"
      },
      file_path: {
        type: "string",
        description: "Path to the file to ingest"
      },
      source_type: {
        type: "string",
        enum: ["file", "code", "web"],
        description: "Type of source (default: 'file')"
      },
      metadata: {
        type: "object",
        description: "Optional metadata to attach"
      }
    },
    required: ["project_id", "file_path"]
  }
}
```

**Implementation**:
```python
async def ingest_file(project_id: str, file_path: str, source_type: str = "file", metadata: dict = None):
    """
    Ingest a file into semantic memory.
    """
    from rag.semantic_ingest import SemanticIngestor
    from pathlib import Path

    # Validate file exists
    if not Path(file_path).exists():
        raise ValueError(f"File not found: {file_path}")

    # Ingest file
    ingestor = SemanticIngestor()
    result = ingestor.ingest_file(
        file_path=file_path,
        project_id=project_id,
        source_type=source_type,
        metadata=metadata
    )

    return {
        "status": "success",
        "file_path": file_path,
        "chunk_count": result["chunks_created"],
        "doc_id": result["doc_id"]
    }
```

#### 5. `rag.update_fact`
```typescript
{
  name: "rag.update_fact",
  description: "Update or create a symbolic memory fact (authoritative)",
  inputSchema: {
    type: "object",
    properties: {
      project_id: {
        type: "string",
        description: "The project ID"
      },
      fact_key: {
        type: "string",
        description: "The fact key"
      },
      fact_value: {
        type: "string",
        description: "The fact value"
      },
      confidence: {
        type: "number",
        description: "Confidence level (0.0-1.0, default: 0.9)"
      },
      category: {
        type: "string",
        description: "Fact category (optional)"
      }
    },
    required: ["project_id", "fact_key", "fact_value"]
  }
}
```

**Implementation**:
```python
async def update_fact(project_id: str, fact_key: str, fact_value: str, confidence: float = 0.9, category: str = None):
    """
    Update or create a symbolic memory fact.
    """
    from rag.memory_writer import MemoryWriter

    writer = MemoryWriter()
    result = writer.write_fact(
        fact_key=fact_key,
        fact_value=fact_value,
        scope="project",
        scope_id=project_id,
        confidence=confidence,
        category=category
    )

    return {
        "status": "success" if result else "failed",
        "fact_id": result.get("fact_id"),
        "action": result.get("action")  # "created" or "updated"
    }
```

### Phase 2: Migration Utility (Priority: HIGH)

**Goal**: Convert existing memory-bank markdown files to RAG database

**Tasks**:
1. Create migration script
2. Parse memory-bank file structure
3. Extract facts from markdown files
4. Import into RAG database
5. Validate migration integrity

**Deliverables**:
- `scripts/migrate_memory_bank.py` - Migration utility
- `data/memory_bank_backup/` - Backup of original files
- Migration report with statistics

**Implementation**:

```python
"""
Migrate memory-bank markdown files to RAG system.

Usage:
    python scripts/migrate_memory_bank.py --source /path/to/memory-bank --project my-project
"""

import re
from pathlib import Path
from typing import Dict, List
from rag.memory_writer import MemoryWriter
from rag.semantic_ingest import SemanticIngestor

def parse_projectbrief(content: str) -> List[Dict]:
    """Parse projectbrief.md into facts."""
    facts = []

    # Extract goals
    goals_match = re.search(r'## Goals\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if goals_match:
        goals = [line.strip() for line in goals_match.group(1).split('\n') if line.strip() and line.strip()[0] not in ['#', '*']]
        for i, goal in enumerate(goals):
            facts.append({
                "key": f"project.goal.{i+1}",
                "value": goal,
                "category": "goal",
                "confidence": 0.9
            })

    return facts

def parse_productContext(content: str) -> List[Dict]:
    """Parse productContext.md into facts."""
    facts = []

    # Extract problem statement
    problem_match = re.search(r'## Problem\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    if problem_match:
        facts.append({
            "key": "product.problem",
            "value": problem_match.group(1).strip(),
            "category": "product_context",
            "confidence": 0.9
        })

    return facts

def parse_systemPatterns(content: str) -> List[Dict]:
    """Parse systemPatterns.md into facts and episodes."""
    facts = []
    episodes = []

    # Extract patterns as facts
    pattern_matches = re.finditer(r'##\s+(.*?)\s*\n(.*?)(?=\n##|\Z)', content, re.DOTALL)
    for match in pattern_matches:
        pattern_name = match.group(1).strip()
        pattern_desc = match.group(2).strip()

        facts.append({
            "key": f"architecture.pattern.{pattern_name.lower().replace(' ', '_')}",
            "value": pattern_desc,
            "category": "architecture",
            "confidence": 0.85
        })

        # Also create episodes if patterns include lessons
        if "lesson" in pattern_desc.lower() or "learned" in pattern_desc.lower():
            episodes.append({
                "title": pattern_name,
                "content": pattern_desc,
                "lesson_type": "pattern",
                "quality": 0.8
            })

    return facts, episodes

def migrate_project(source_dir: Path, project_id: str):
    """Migrate a single project from memory-bank to RAG."""
    print(f"Migrating project: {project_id}")

    writer = MemoryWriter()
    ingestor = SemanticIngestor()

    # Migrate core files as symbolic facts
    file_mappings = {
        "projectbrief.md": parse_projectbrief,
        "productContext.md": parse_productContext,
        "systemPatterns.md": parse_systemPatterns,
        "techContext.md": lambda c: [{"key": "tech.stack", "value": c, "category": "tech", "confidence": 0.9}],
        ".clinerules": lambda c: [{"key": "workflow.rules", "value": c, "category": "workflow", "confidence": 0.95}]
    }

    for filename, parser in file_mappings.items():
        file_path = source_dir / filename
        if file_path.exists():
            print(f"  Processing {filename}...")
            content = file_path.read_text()

            if filename == "systemPatterns.md":
                facts, episodes = parser(content)

                # Write facts
                for fact in facts:
                    writer.write_fact(
                        fact_key=fact["key"],
                        fact_value=fact["value"],
                        scope="project",
                        scope_id=project_id,
                        confidence=fact["confidence"],
                        category=fact["category"]
                    )

                # Import episodes (for Phase 3)
                # Note: This would require episodic store implementation
            else:
                facts = parser(content)

                for fact in facts:
                    writer.write_fact(
                        fact_key=fact["key"],
                        fact_value=fact["value"],
                        scope="project",
                        scope_id=project_id,
                        confidence=fact["confidence"],
                        category=fact["category"]
                    )

            # Also ingest as semantic document (Phase 4)
            ingestor.ingest_file(
                file_path=str(file_path),
                project_id=project_id,
                source_type="file",
                metadata={"original_type": "memory_bank"}
            )

    # Migrate custom files (features/*.md, api/*.md, etc.)
    for category in ["features", "api", "deployment"]:
        category_dir = source_dir / category
        if category_dir.exists():
            for file_path in category_dir.glob("*.md"):
                print(f"  Processing {category}/{file_path.name}...")
                ingestor.ingest_file(
                    file_path=str(file_path),
                    project_id=project_id,
                    source_type="file",
                    metadata={"category": category}
                )

    print(f"  ✅ Migration complete for {project_id}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Migrate memory-bank to RAG")
    parser.add_argument("--source", required=True, help="Path to memory-bank directory")
    parser.add_argument("--project", required=True, help="Project ID to use in RAG")
    args = parser.parse_args()

    migrate_project(Path(args.source), args.project)
```

### Phase 3: Docker Configuration (Priority: HIGH)

**Goal**: Package RAG MCP server for easy deployment

**Tasks**:
1. Create Dockerfile
2. Test container startup
3. Configure volume mounts
4. Test MCP connection from clients

**Deliverables**:
- `Dockerfile` - Multi-stage build
- `docker-compose.yml` - Easy local setup
- `README-DOCKER.md` - Docker deployment guide

**Dockerfile**:

```dockerfile
# Multi-stage build for RAG MCP Server
FROM python:3.11-slim as builder

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libffi-dev \
    libssl-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Verify imports work
RUN python -c "from rag import MemoryStore, MemoryWriter, MemoryReader; print('✅ Phase 1 OK')" && \
    python -c "from rag.episodic_store import EpisodeStore; from rag.episodic_reader import EpisodeReader; print('✅ Phase 3 OK')" && \
    python -c "from rag.semantic_store import SemanticStore; from rag.semantic_ingest import SemanticIngestor; from rag.semantic_retriever import SemanticRetriever; from rag.semantic_injector import SemanticInjector; print('✅ Phase 4 OK')"

# Final stage
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /app /app

# Create data directories
RUN mkdir -p /app/data /app/data/semantic_index

# Set environment variables
ENV PYTHONPATH=/app
ENV RAG_DATA_DIR=/app/data

# Expose MCP server doesn't need a port (uses stdio)
# Expose for potential web interface
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "from rag import MemoryStore; store = MemoryStore(); print('healthy')" || exit 1

# Run MCP server
CMD ["python", "-m", "mcp_server.server"]
```

**docker-compose.yml**:

```yaml
version: '3.8'

services:
  rag-mcp:
    build: .
    container_name: rag-mcp-server
    restart: unless-stopped
    environment:
      - RAG_DATA_DIR=/app/data
      - LOG_LEVEL=INFO
    volumes:
      - ./data:/app/data
      - ./projects:/app/projects:ro  # Mount project files for ingestion
    # For development
    # ports:
    #   - "8080:8080"
    networks:
      - rag-network

networks:
  rag-network:
    driver: bridge
```

### Phase 4: Documentation & Configuration (Priority: MEDIUM)

**Goal**: Provide clear documentation for users and configuration guides for different clients

**Tasks**:
1. Write comprehensive migration guide
2. Update AGENTIC_RAG_COMPLETE_GUIDE.md with memory-bank comparison
3. Create configuration examples for Cline, Claude, Cursor
4. Write troubleshooting guide

**Deliverables**:
- `MIGRATION_GUIDE.md` - Step-by-step migration
- `MEMORY_BANK_VS_RAG.md` - Detailed comparison
- `CLINE_CONFIG.md` - Cline configuration
- `CLAUDE_CONFIG.md` - Claude configuration
- `CURSOR_CONFIG.md` - Cursor configuration

---

## Client Configuration Examples

### Cline Configuration

**File**: `~/Library/Application Support/Cursor/User/globalStorage/saoudrizwan.claude-dev/settings/cline_mcp_settings.json`

```json
{
  "rag-mcp": {
    "command": "python",
    "args": [
      "-m",
      "mcp_server.server"
    ],
    "cwd": "/path/to/pi-rag",
    "env": {
      "RAG_DATA_DIR": "/path/to/pi-rag/data"
    },
    "disabled": false,
    "autoApprove": [
      "rag.list_projects",
      "rag.list_sources",
      "rag.get_context",
      "rag.search",
      "rag.add_episode"
    ]
  }
}
```

### Claude Configuration

**File**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "rag-mcp": {
      "command": "python",
      "args": [
        "-m",
        "mcp_server.server"
      ],
      "cwd": "/path/to/pi-rag",
      "env": {
        "RAG_DATA_DIR": "/path/to/pi-rag/data"
      }
    }
  }
}
```

### Cursor Configuration

**Settings** → **Features** → **MCP Servers** → **Add Server**:

```bash
cd /path/to/pi-rag && RAG_DATA_DIR=/path/to/pi-rag/data python -m mcp_server.server
```

---

## Custom AI Instructions (RAG Memory System)

Copy these instructions to your AI assistant's custom instructions:

### RAG Memory System Instructions

I am an expert engineer with a sophisticated multi-layer memory system accessed via MCP tools. My memory has three distinct layers with different authority levels:

## Memory Authority Hierarchy

1. **Symbolic Memory (Phase 1)** - **AUTHORITATIVE**
   - Explicit facts with confidence levels (0.0-1.0)
   - Conflict resolution: highest confidence wins
   - Used for goals, requirements, tech stack, architecture patterns
   - **Authority**: Always trust over other memory types

2. **Episodic Memory (Phase 3)** - **ADVISORY**
   - Lessons learned from past work
   - Advisory for planning and decision-making
   - Quality-scored episodes (0.0-1.0)
   - **Authority**: Can suggest, but never override symbolic memory

3. **Semantic Memory (Phase 4)** - **NON-AUTHORITATIVE**
   - Document/code chunks with semantic search
   - Citation-based with provenance tracking
   - Vector-based retrieval with similarity scores
   - **Authority**: Context only, never asserts truth

## Key Commands

### "follow your custom instructions"
- Access RAG memory via `rag.get_context(project_id, query)`
- Follow authority hierarchy: Symbolic → Episodic → Semantic
- Execute appropriate task with full context

### "initialize project memory"
- Create project scope in symbolic memory
- Set core facts: goals, requirements, tech stack
- Initialize episodic memory for lessons
- Enable semantic ingestion for documentation

### "search project memory"
- Use `rag.search(project_id, query, memory_type)` for targeted search
- Results include authority indicators and confidence scores
- Citations included for semantic results: `[source:chunk_id]`

### "update project memory"
- Use `rag.update_fact(project_id, fact_key, fact_value, confidence)` for authoritative facts
- Use `rag.add_episode(project_id, title, content, lesson_type)` for lessons learned
- Use `rag.ingest_file(project_id, file_path)` for documentation/code

## Memory Access Pattern

### Before Any Task:
1. **Call `rag.get_context(project_id, context_type="all")`**
2. **Review results in authority order**:
   - First: Symbolic (authoritative facts)
   - Second: Episodic (advisory lessons)
   - Third: Semantic (contextual documents)

### During Task:
1. **Symbolic memory** provides absolute truth (e.g., "Python 3.11 is required")
2. **Episodic memory** provides advisory guidance (e.g., "Last time we tried X, we learned...")
3. **Semantic memory** provides contextual background (e.g., "According to the API docs...")

### After Task:
1. **Update symbolic memory** for new facts/requirements
2. **Add episodes** for lessons learned
3. **Ingest documentation** for new files created

## Memory Bank vs RAG Key Differences

| Aspect | Memory-Bank | RAG System |
|--------|-------------|------------|
| Storage | Markdown files | Database (3 layers) |
| Search | Filename only | Semantic search |
| Conflict | Manual overwrite | Automatic resolution |
| Authority | None | Hierarchy enforced |
| Learning | Manual | Automatic via episodes |
| Provenance | None | Full audit trail |

## Project Initialization Example

```python
# 1. Initialize project symbolic memory
await mcp.call_tool("rag.update_fact", {
    "project_id": "my-project",
    "fact_key": "project.goals",
    "fact_value": "Build a RAG-based memory system",
    "confidence": 0.9,
    "category": "goal"
})

# 2. Set tech stack
await mcp.call_tool("rag.update_fact", {
    "project_id": "my-project",
    "fact_key": "tech.stack.python",
    "fact_value": "3.11",
    "confidence": 1.0,
    "category": "tech"
})

# 3. Ingest existing documentation
await mcp.call_tool("rag.ingest_file", {
    "project_id": "my-project",
    "file_path": "/path/to/README.md"
})

# 4. Get context for task
context = await mcp.call_tool("rag.get_context", {
    "project_id": "my-project",
    "context_type": "all",
    "query": "API endpoints and architecture"
})
```

---

## Testing Strategy

### Unit Tests
- Each MCP tool handler
- Migration utility parsing
- Database queries
- Conflict resolution logic

### Integration Tests
- End-to-end migration from memory-bank to RAG
- MCP client connections (Cline, Claude, Cursor)
- Tool execution in real scenarios
- Authority hierarchy enforcement

### Performance Tests
- Large-scale ingestion (1000+ files)
- Semantic search performance
- Multi-project isolation
- Concurrent access

---

## Rollback Strategy

If issues occur, users can:
1. **Backup RAG database**: `cp -r data/ data_backup/`
2. **Export to memory-bank format**: Use `rag.backup_project(project_id)` tool
3. **Continue using memory-bank**: Keep original files
4. **Gradual migration**: Migrate one project at a time

---

## Success Metrics

- ✅ All 5 memory-bank tools replaced with RAG equivalents
- ✅ Migration utility successfully converts 100% of test projects
- ✅ RAG tools provide equal or better functionality
- ✅ Performance equal or better than memory-bank
- ✅ Users can migrate with minimal friction
- ✅ Authority hierarchy correctly enforced
- ✅ Cross-client compatibility (Cline, Claude, Cursor)

---

## Next Steps

1. **Fix Phase 4 import errors** (BLOCKING - Must be done first)
2. **Implement real MCP tool handlers** (currently mocks only)
3. **Create migration utility script**
4. **Add Docker configuration**
5. **Write comprehensive documentation**
6. **Test with real memory-bank projects**
7. **Deploy and gather feedback**
8. **Iterate based on user feedback**

---

## Conclusion

The RAG system provides a **significant upgrade** over memory-bank-mcp:

- ✅ **Database-backed** instead of file-based (better performance, reliability)
- ✅ **Semantic search** instead of filename matching (find relevant content easily)
- ✅ **Conflict resolution** instead of manual overwrite (automatic, confidence-based)
- ✅ **Authority hierarchy** instead of flat structure (symbolic > episodic > semantic)
- ✅ **Cross-project learning** instead of strict isolation (with scope controls)
- ✅ **Citation support** instead of no provenance (full audit trail)
- ✅ **Advisory episodic memory** instead of no learning (lessons learned)

All memory-bank functionality is preserved or enhanced, with powerful new capabilities that were impossible with file-based storage.
