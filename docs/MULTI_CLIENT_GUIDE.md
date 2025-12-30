# Multi-Client Architecture Guide

## Overview

The pi-rag MCP server supports multi-client isolation with per-project ChromaDB instances.

## Architecture

### Directory Structure

```
/opt/pi-rag/
└── data/
    ├── registry.db              # Global project registry
    ├── docs/                   # External documents TO BE ingested
    │   └── ...                # User documents here
    └── {project-name}-{uuid}/   # Project-specific data
        ├── memory.db            # Symbolic memory
        ├── episodic.db          # Episodic memory
        ├── chroma_semantic/     # ChromaDB (semantic memory)
        └── project.json        # Project metadata
```

### Project Isolation

Each project gets:
- **Isolated SQLite databases**: `memory.db`, `episodic.db`
- **Isolated ChromaDB instance**: `chroma_semantic/`
- **Unique project ID**: `{name}-{8-char-UUID}`
- **Complete data separation**: No cross-project data leakage

## Getting Started

### Prerequisites

Ensure `/opt/pi-rag/data/` exists with proper ownership:

```bash
sudo mkdir -p /opt/pi-rag/data
sudo chown -R dietpi:dietpi /opt/pi-rag
ls -ld /opt/pi-rag
# Should show: drwxr-xr-x dietpi dietpi /opt/pi-rag
```

### Create Project

**Via MCP Tool**:
```
rag.create_project(name="myproject")
```

**Via Python API**:
```python
from mcp_server.rag_server import RAGMemoryBackend

backend = RAGMemoryBackend()
project = await backend.create_project("myproject")
print(f"Created: {project['project']['project_id']}")
# Output: Created: myproject-abc12345
```

### List Projects

**Via MCP Tool**:
```
rag.list_projects()
```

**Via Python API**:
```python
from mcp_server.project_manager import ProjectManager

pm = ProjectManager("/opt/pi-rag/data")
projects = pm.list_projects()
for p in projects:
    print(f"{p['project_id']}: {p['name']}")
```

### Delete Project

**Via MCP Tool**:
```
rag.delete_project(project_id="myproject-abc12345")
```

## Data Ingestion

### Add Documents

Place documents in `/opt/pi-rag/data/docs/`:

```bash
cp my_document.md /opt/pi-rag/data/docs/
cp my_code.py /opt/pi-rag/data/docs/
```

Then ingest via MCP:
```
rag.ingest_file(
    project_id="myproject-abc12345",
    file_path="/opt/pi-rag/data/docs/my_document.md"
)
```

## Configuration

### Environment Variables

```bash
export RAG_DATA_DIR=/opt/pi-rag/data
export MULTI_CLIENT=true
export CHROMA_ISOLATION=project
```

### Config File

`configs/rag_config.json`:
```json
{
  "data_dir": "/opt/pi-rag/data",
  "docs_path": "/opt/pi-rag/data/docs",
  "multi_client": true,
  "chroma_isolation": "project"
}
```

## Troubleshooting

### Permission Denied

```bash
sudo chown -R dietpi:dietpi /opt/pi-rag
```

### Project Not Found

```bash
# Check if project directory exists
ls -la /opt/pi-rag/data/myproject-abc12345/
```

### ChromaDB Errors

```bash
# Check ChromaDB directory
ls -la /opt/pi-rag/data/myproject-abc12345/chroma_semantic/
```

## Cleanup

### Delete Specific Project

```bash
# Via MCP
rag.delete_project(project_id="myproject-abc12345")

# Or manually
rm -rf /opt/pi-rag/data/myproject-abc12345
```

### Delete All Data

⚠️ **WARNING**: This deletes ALL projects and data!

```bash
rm -rf /opt/pi-rag/data/*
# Reinitialize
systemctl restart rag-mcp
```
