# SYNAPSE

> Your Data Meets Intelligence

A local-first RAG (Retrieval-Augmented Generation) system where your stored knowledge (neurons) fires into intelligent processing (synaptic firing) to connect with AI neural networks.

---

## Features

### 🧠 Neural Storage (Three Memory Types)

**1. Dendrites (Semantic Memory)** - Vector-based document storage
- Grounded retrieval, zero hallucinations
- BGE-M3 embeddings, local model
- Project-based organization

**2. Synapses (Episodic Memory)** - Lessons learned from experience
- Success/failure analysis
- Pattern recognition (85% confidence)
- Advisory intelligence for your system

**3. Cell Bodies (Symbolic Memory)** - Authoritative facts
- Configuration (100% accuracy)
- Technical specifications
- System-wide settings
- API endpoints, version numbers

### ⚡ Synaptic Transmission (MCP Protocol)
- **7 MCP Tools**: List projects, list sources, get context, search, ingest file, add fact, add episode
- **HTTP Upload**: Remote file ingestion with auto-cleanup

### 🔄 Neural Plasticity (Smart Ingestion & Sync)
- **Bulk Ingestion**: .gitignore-aware file ingestion with incremental updates
- **Auto-Sync**: Git hooks for continuous updates
- **Retry Mechanism**: Failed files auto-retried

---

## Quick Start

### Option 1: Docker Hub (Recommended) ⭐

```bash
# Pull and run SYNAPSE
docker pull docker.io/kayisrahman/synapse:1.0.0
docker run -d --name synapse-mcp -p 8002:8002 \
  -v synapse-data:/app/data \
  -v synapse-models:/app/models \
  docker.io/kayisrahman/synapse:1.0.0

# Or use Docker Compose
git clone https://github.com/kayis-rahman/synapse.git
cd synapse
docker compose -f docker-compose.mcp.yml up -d
```

### Option 2: pip Installation

```bash
# Install SYNAPSE
pip install synapse

# With MCP Server
pip install synapse[mcp]

# Development
pip install synapse[dev]
```

### Option 3: From Source

```bash
git clone https://github.com/kayis-rahman/synapse.git
cd synapse
pip install -e .
```

> **Note**: Linux service approach (start_http_server.sh) is deprecated. Please use Docker instead - see [DOCKER_INSTALLATION.md](DOCKER_INSTALLATION.md)

---

## MCP Tools

### Tool 1: `synapse.list_projects`
List all registered projects.

### Tool 2: `synapse.list_sources`
List all document sources in a project.

### Tool 3: `synapse.get_context`
Get comprehensive context from all memory types (dendrites, synapses, cell bodies).

### Tool 4: `synapse.search`
Search dendrites (semantic memory) for relevant documents.

### Tool 5: `synapse.ingest_file`
Ingest a file into dendrites (semantic memory).

### Tool 6: `synapse.add_fact`
Add symbolic fact to cell bodies (100% accuracy).

### Tool 7: `synapse.add_episode`
Add episodic lesson to synapses (85% confidence).

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    Your Knowledge (Neurons)                │
└────────────────────────┬────────────────────────────────────┘
                     │
┌────────────────────────┴─────────────────────────────────┐
│         Dendrites (Semantic Memory)                  │
└────────────────────────┬───────────────────────────────┘
                     │
┌────────────────────────┴─────────────────────────────────┐
│         Synapses (Episodic Memory)                   │
└────────────────────────┬───────────────────────────────┘
                     │
┌────────────────────────┴─────────────────────────────────┐
│         Cell Bodies (Symbolic Memory)                │
└────────────────────────┬───────────────────────────────┘
                     │
             SYNAPSE Server (MCP)                │
└────────────────────────┬───────────────────────────────┘
                     │
          LLMs (AI Agents)              │
└────────────────────────┬───────────────────────────────┘
```

---

## CLI Commands

### Neurobiological Commands (Docker) 🧠

These short, creative commands provide a neurobiological metaphor for SYNAPSE operations:

#### `synapse-ignite` - Ignite SYNAPSE
**Ignite synaptic transmission (start MCP server)**

```bash
./scripts/synapse-ignite
```

#### `synapse-sense` - Sense Neural State
**Check neural system status**

```bash
./scripts/synapse-sense
```

#### `synapse-feed` - Feed Neurons
**Feed data to neurons (bulk ingest)**

```bash
./scripts/synapse-feed --dry-run
```

### Standard Commands (All Methods)

**With Docker**:
```bash
# System status
docker exec synapse-mcp python -m scripts.rag_status

# Bulk ingest
docker exec synapse-mcp python -m scripts.bulk_ingest --help

# Interactive shell
docker exec -it synapse-mcp bash
```

**With pip/Source**:
```bash
# Start MCP Server
synapse-mcp-server

# Check system status
synapse-system-status

# Bulk ingest project files
synapse-bulk-ingest --dry-run
```

---

## Documentation

- 📚 [Full Documentation](https://kayis-rahman.github.io/synapse/docs)
- 🚀 [Docker Installation Guide](DOCKER_INSTALLATION.md) - Comprehensive Docker deployment guide
- 🏗️ [Architecture Overview](https://kayis-rahman.github.io/synapse/docs/architecture/overview)
- 🚀 [Installation Guide](https://kayis-rahman.github.io/synapse/docs/getting-started/installation)
- 🧠 [Memory System](https://kayis-rahman.github.io/synapse/docs/architecture/memory-system)
- 🔧 [MCP Tools Reference](https://kayis-rahman.github.io/synapse/docs/usage/mcp-tools)

---

## License

MIT License - see LICENSE file for details

---

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## Roadmap

### v1.0.0 (Current) - ✅
- ✅ Core rebranding to SYNAPSE
- ✅ Docker Hub publishing (docker.io/kayisrahman/synapse)
- ✅ Multi-platform builds (AMD64, ARM64)
- ✅ Neurobiological CLI commands (synapse-ignite, synapse-sense, synapse-feed)
- ✅ Docker-first installation guide
- ✅ Packaging files (setup.py, pyproject.toml)
- ✅ Documentation update with SYNAPSE branding
- ✅ MCP tool descriptions with neurobiological metaphor
- ✅ Linux service deprecated (use Docker instead)

### v1.1.0 (Next)
- ⏳ CLI tool enhancements
- ⏳ Performance optimization
- ⏳ Additional memory types
