---
title: Quick Start
description: Get your first query in under 5 minutes
---

# Quick Start

**Goal:** From zero to your first query in under 5 minutes.

## 1️⃣ Start the Server

```bash
synapse start
```

> **Server URL:** http://localhost:8002/mcp
>
> Keep this terminal open. The server runs in the foreground.

::details{label="What does this do?"}
**Starting the server initializes:**
- MCP HTTP server on port 8002
- BGE-M3 embedding model
- Three memory systems (semantic, episodic, symbolic)
- Health check endpoint at http://localhost:8002/mcp

**Expected output:**
```
🚀 Starting SYNAPSE server...
  Port: 8002
  Environment: development
```
::

## 2️⃣ Ingest Your Data

Open a **new terminal** and run:

```bash
# Ingest the current directory
synapse ingest .

# Or ingest a specific path
synapse ingest /path/to/your/docs
```

::details{label="What does this do?"}
**Ingestion processes your files:**
- Scans for supported file types (.py, .md, .txt, etc.)
- Chunks documents (500 chars with 50 char overlap)
- Creates vector embeddings using BGE-M3
- Stores in semantic memory for retrieval

**Supported file types:**
- Code: .py, .js, .ts, .java, .cpp, etc.
- Docs: .md, .txt, .rst, .pdf, etc.
- Config: .json, .yaml, .toml, .env

**Progress indicators show:**
- Files scanned
- Documents created
- Embeddings generated
::

## 3️⃣ Query Your Knowledge

```bash
synapse query "What is SYNAPSE?"
```

::details{label="What does this do?"}
**Querying searches your knowledge:**
1. Creates query embedding using BGE-M3
2. Searches semantic memory (vectors)
3. Retrieves top-K most relevant chunks
4. Returns results with source attribution

**Query options:**
```bash
# Get more results
synapse query "question" --top-k 5

# JSON output for automation
synapse query "question" --format json
```
::

---

## 🎉 You Did It!

You now have a working SYNAPSE installation with:
- ✅ Server running at http://localhost:8002/mcp
- ✅ Your data indexed and searchable
- ✅ Query capability ready to use

## Next Steps

::cards
:::card{label="Ingest More Data"}
Add more knowledge to your system:
```bash
synapse ingest /path/to/more/docs
```
[Learn More →](../usage/ingestion)
:::
:::card{label="Explore Commands"}
Discover what else SYNAPSE can do:
```bash
synapse --help
```
[CLI Commands →](../api-reference/cli-commands)
:::
:::card{label="Understand Memory"}
Learn about the three memory types:
[SYNAPSE Architecture →](../architecture/overview)
:::
::

---

## Common Questions

::details{label="How do I stop the server?"}
Press `Ctrl+C` in the terminal where the server is running.
:::
::details{label="Can I run in background?"}
Yes, use `&` to run in background:
```bash
synapse start &
```
Or use nohup:
```bash
nohup synapse start > server.log 2>&1 &
```
:::
::details{label="Where is my data stored?"}
By default: `~/.synapse/data/`
- `semantic_index/` - Document embeddings
- `memory.db` - Symbolic memory (facts)
- `episodic.db` - Episodic memory (lessons)
:::
