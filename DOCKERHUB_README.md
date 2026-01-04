# SYNAPSE

> Your Data Meets Intelligence

**Version**: 1.0.0  
**License**: MIT  
**Repository**: [kayis-rahman/synapse](https://github.com/kayis-rahman/synapse)

---

## What is SYNAPSE?

SYNAPSE is a local-first RAG (Retrieval-Augmented Generation) system where your stored knowledge (neurons) fires into intelligent processing through synaptic transmission.

### Key Features

- 🧠 **Neural Storage** - Three-tier memory system (Semantic, Episodic, Symbolic)
- ⚡ **Synaptic Transmission** - MCP Protocol for seamless integration
- 🔄 **Neural Plasticity** - Smart ingestion with incremental updates
- 🔒 **Local-First** - Your data stays on your machine
- 🐳 **Docker-Ready** - Easy deployment with multi-platform support

---

## Quick Start

### Pull and Run

```bash
docker pull docker.io/kayisrahman/synapse:1.0.0

docker run -d --name synapse-mcp \
  -p 8002:8002 \
  -v synapse-data:/app/data \
  -v synapse-models:/app/models \
  docker.io/kayisrahman/synapse:1.0.0
```

### Or with Docker Compose

```bash
git clone https://github.com/kayis-rahman/synapse.git
cd synapse
docker compose -f docker-compose.mcp.yml up -d
```

### Verify Installation

```bash
# Health check
curl http://localhost:8002/health

# Expected response
{"status": "ok", "service": "synapse"}
```

---

## CLI Commands

### Neurobiological Commands (Short & Creative)

```bash
# Ignite SYNAPSE (start server)
./scripts/synapse-ignite

# Feed data to neurons (bulk ingest)
./scripts/synapse-feed --dry-run

# Sense neural state (check status)
./scripts/synapse-sense
```

### Standard Docker Commands

```bash
# System status
docker exec synapse-mcp python -m scripts.rag_status

# Bulk ingest
docker exec synapse-mcp python -m scripts.bulk_ingest --help

# Interactive shell
docker exec -it synapse-mcp bash
```

---

## Architecture

SYNAPSE uses a neurobiological metaphor for its three-tier memory system:

```
┌─────────────────────────────────────────┐
│      Your Knowledge (Neurons)       │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│    Dendrites (Semantic Memory)    │
│    Vector-based document storage    │
│    60% confidence              │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│    Synapses (Episodic Memory)     │
│    Lessons learned from experience │
│    85% confidence              │
└─────────────────┬───────────────────────┘
                  │
┌─────────────────┴───────────────────────┐
│  Cell Bodies (Symbolic Memory)     │
│  Authoritative facts (100% truth)   │
└─────────────────┬───────────────────────┘
                  │
          SYNAPSE Server (MCP)
                  │
              LLMs (AI Agents)
```

---

## Memory Types

### 1. Dendrites (Semantic Memory)
- **Purpose**: Vector-based document storage
- **Confidence**: 60% (suggestions)
- **Use Case**: Grounded retrieval, zero hallucinations
- **Model**: BGE-M3 embeddings (local)

### 2. Synapses (Episodic Memory)
- **Purpose**: Lessons learned from experience
- **Confidence**: 85% (high-priority guidance)
- **Use Case**: Success/failure analysis, pattern recognition
- **Storage**: SQLite database

### 3. Cell Bodies (Symbolic Memory)
- **Purpose**: Authoritative facts
- **Confidence**: 100% (absolute truth)
- **Use Case**: Configuration, technical specs, API endpoints
- **Storage**: SQLite database

---

## MCP Tools

SYNAPSE provides 7 MCP tools for seamless integration:

1. **`synapse.list_projects`** - List all registered projects
2. **`synapse.list_sources`** - List document sources in a project
3. **`synapse.get_context`** - Get comprehensive context from all memory types
4. **`synapse.search`** - Search semantic memory for relevant documents
5. **`synapse.ingest_file`** - Ingest a file into semantic memory
6. **`synapse.add_fact`** - Add symbolic fact (100% accuracy)
7. **`synapse.add_episode`** - Add episodic lesson (85% confidence)

---

## Tags

- `1.0.0` - Latest stable release
- `latest` - Most recent version (updates with main branch)
- `main` - Development branch builds

---

## Platforms

- `linux/amd64` - Intel/AMD x86_64
- `linux/arm64` - ARM 64-bit (Raspberry Pi, Apple Silicon)

---

## Environment Variables

Key configuration options:

```bash
# Server
HOST=0.0.0.0
PORT=8002

# RAG Configuration
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K=3

# Logging
LOG_LEVEL=INFO
```

See [DOCKER_INSTALLATION.md](https://github.com/kayis-rahman/synapse/blob/main/DOCKER_INSTALLATION.md) for full configuration options.

---

## Volume Mounts

Recommended volumes for persistence:

```bash
-v synapse-data:/app/data      # Vector store & databases
-v synapse-models:/app/models    # GGUF embedding models
-v $(pwd)/configs:/app/configs:ro  # Configuration files
```

---

## Documentation

- 📚 [Full Documentation](https://kayis-rahman.github.io/synapse/docs)
- 🚀 [Docker Installation Guide](https://github.com/kayis-rahman/synapse/blob/main/DOCKER_INSTALLATION.md)
- 🏗️ [Architecture Overview](https://github.com/kayis-rahman/synapse/blob/main/docs/architecture/overview.mdx)
- 🔧 [MCP Tools Reference](https://github.com/kayis-rahman/synapse/blob/main/docs/usage/mcp-tools.mdx)

---

## Support

- **Issues**: [GitHub Issues](https://github.com/kayis-rahman/synapse/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kayis-rahman/synapse/discussions)
- **Documentation**: [Full Docs](https://kayis-rahman.github.io/synapse/docs)

---

## License

MIT License - see [LICENSE](https://github.com/kayis-rahman/synapse/blob/main/LICENSE) file for details.

---

## Contributing

Contributions welcome! Please read [CONTRIBUTING.md](https://github.com/kayis-rahman/synapse/blob/main/CONTRIBUTING.md) for guidelines.

---

## Roadmap

### v1.0.0 (Current) - ✅
- ✅ Docker Hub publishing
- ✅ Multi-platform builds (AMD64, ARM64)
- ✅ Neurobiological CLI commands
- ✅ Docker-first deployment

### v1.1.0 (Next)
- ⏳ CLI tool enhancements
- ⏳ Performance optimization
- ⏳ Additional memory types

---

**Made with ❤️ by [Kayis Rahman](https://github.com/kayis-rahman)**

Your Data Meets Intelligence 🧠⚡
