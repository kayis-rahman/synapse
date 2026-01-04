# Docker Installation Guide for SYNAPSE v1.0.0

> Your Data Meets Intelligence

This guide walks you through installing SYNAPSE using Docker, the recommended deployment method.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation Methods](#installation-methods)
- [CLI Commands](#cli-commands)
- [Configuration](#configuration)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required

- **Docker** (v20.10+): [Install Docker](https://docs.docker.com/get-docker/)
- **Docker Compose** (v2.0+): Included with Docker Desktop
- **Memory**: At least 2GB RAM (4GB+ recommended)
- **Disk**: 10GB+ free space
- **Network**: Internet access for initial image pull

### Optional

- **Docker Hub Account**: For pulling images (not required, public images available)
- **GPU**: Not required (CPU-only embeddings)

### Verify Docker Installation

```bash
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Test Docker is running
docker run hello-world
```

---

## Installation Methods

### Method 1: Docker Hub (Recommended) ⭐

**Best for**: Production, quick start, consistent updates

```bash
# Pull latest image
docker pull docker.io/kayisrahman/synapse:1.0.0

# Run container
docker run -d --name synapse-mcp \
  -p 8002:8002 \
  -v synapse-data:/app/data \
  -v synapse-models:/app/models \
  -v $(pwd)/configs:/app/configs:ro \
  docker.io/kayisrahman/synapse:1.0.0
```

**Verify deployment**:
```bash
# Check container is running
docker ps | grep synapse-mcp

# Health check
curl http://localhost:8002/health

# View logs
docker logs -f synapse-mcp
```

---

### Method 2: Docker Compose (Best for Customization) ⭐

**Best for**: Production, customization, development

```bash
# Clone repository
git clone https://github.com/kayis-rahman/synapse.git
cd synapse

# Start with Docker Compose
docker compose -f docker-compose.mcp.yml up -d
```

**Or use CLI wrapper**:
```bash
# Ignite SYNAPSE (start server)
./scripts/synapse-ignite
```

---

### Method 3: Building from Source (Development)

**Best for**: Development, testing, customization

```bash
# Clone repository
git clone https://github.com/kayis-rahman/synapse.git
cd synapse

# Build Docker image locally
docker build -t synapse:1.0.0 .

# Run container
docker run -d --name synapse-mcp \
  -p 8002:8002 \
  -v synapse-data:/app/data \
  -v synapse-models:/app/models \
  synapse:1.0.0
```

---

## CLI Commands

### Neurobiological Commands (Short & Creative) 🧠

These commands provide a neurobiological metaphor for SYNAPSE operations:

#### `synapse-ignite` - Start Server

**Ignite synaptic transmission (start MCP server)**

```bash
# Fire up SYNAPSE
./scripts/synapse-ignite
```

**Equivalent to**:
```bash
docker compose -f docker-compose.mcp.yml up -d
```

**What it does**:
- Starts the SYNAPSE container
- Initializes neural storage (data, models)
- Exposes MCP endpoint on http://localhost:8002/mcp
- Checks health status

---

#### `synapse-sense` - Check Status

**Sense neural system state (check status)**

```bash
# Check neural pulse
./scripts/synapse-sense

# With specific options
./scripts/synapse-sense --verbose
```

**Equivalent to**:
```bash
docker exec synapse-mcp python -m scripts.rag_status
```

**What it shows**:
- Container status
- Memory usage (semantic, episodic, symbolic)
- Project statistics
- API endpoints

---

#### `synapse-feed` - Feed Data

**Feed data to neurons (bulk ingest)**

```bash
# Feed documents (dry run first)
./scripts/synapse-feed --dry-run

# Feed documents (actual ingestion)
./scripts/synapse-feed

# Feed specific directory
./scripts/synapse-feed --source /path/to/docs
```

**Equivalent to**:
```bash
docker exec synapse-mcp python -m scripts.bulk_ingest
```

**What it does**:
- Scans document directories
- Respects .gitignore rules
- Chunks documents for semantic memory
- Generates embeddings (BGE-M3)
- Stores in vector database

---

### Standard Docker Commands

You can also use Docker directly:

```bash
# Start container
docker compose -f docker-compose.mcp.yml up -d

# Stop container
docker compose -f docker-compose.mcp.yml down

# Restart container
docker restart synapse-mcp

# View logs
docker logs -f synapse-mcp

# Execute command in container
docker exec synapse-mcp python -m scripts.rag_status
docker exec synapse-mcp python -m scripts.bulk_ingest --help

# Interactive shell
docker exec -it synapse-mcp bash
```

---

## Configuration

### Environment Variables

Configure SYNAPSE using environment variables:

**In `.env.docker`**:
```bash
# Server
HOST=0.0.0.0
PORT=8002

# RAG Configuration
PROJECT_ROOT=/app/data
CHUNK_SIZE=500
CHUNK_OVERLAP=50
TOP_K=3

# Logging
LOG_LEVEL=INFO
PYTHONUNBUFFERED=1

# Performance
EMBEDDING_CACHE_ENABLED=true
EMBEDDING_CACHE_SIZE=1000
```

**Pass with docker run**:
```bash
docker run -d --name synapse-mcp \
  -e LOG_LEVEL=DEBUG \
  -e CHUNK_SIZE=1000 \
  -p 8002:8002 \
  docker.io/kayisrahman/synapse:1.0.0
```

**With Docker Compose**:
```yaml
services:
  synapse-mcp:
    environment:
      - LOG_LEVEL=DEBUG
      - CHUNK_SIZE=1000
```

---

### Volume Mounting

SYNAPSE uses Docker volumes for persistence:

#### Named Volumes (Recommended)

```bash
# Data volume (databases, vector index)
docker volume create synapse-data

# Models volume (GGUF embedding models)
docker volume create synapse-models

# Run container with volumes
docker run -d --name synapse-mcp \
  -v synapse-data:/app/data \
  -v synapse-models:/app/models \
  -p 8002:8002 \
  docker.io/kayisrahman/synapse:1.0.0
```

#### Bind Mounts (Development)

```bash
# Mount host directory
docker run -d --name synapse-mcp \
  -v $(pwd)/data:/app/data \
  -v $(pwd)/models:/app/models \
  -v $(pwd)/configs:/app/configs:ro \
  -p 8002:8002 \
  docker.io/kayisrahman/synapse:1.0.0
```

---

### Port Mapping

Default port: **8002** (MCP HTTP endpoint)

**Custom port**:
```bash
docker run -d --name synapse-mcp \
  -p 9000:8002 \
  docker.io/kayisrahman/synapse:1.0.0
```

**Then access**: http://localhost:9002/mcp

---

### Configuration Files

Mount your configuration files:

```bash
docker run -d --name synapse-mcp \
  -v $(pwd)/configs:/app/configs:ro \
  -p 8002:8002 \
  docker.io/kayisrahman/synapse:1.0.0
```

**Read-only mount** (`:ro`) prevents accidental modifications.

---

## Troubleshooting

### Container Won't Start

**Check logs**:
```bash
docker logs synapse-mcp
```

**Common issues**:
1. **Port already in use**:
   ```bash
   # Check what's using port 8002
   netstat -tlnp | grep 8002
   # Or
   lsof -i :8002

   # Stop conflicting service or use different port
   docker run -p 9000:8002 ...
   ```

2. **Volume permission issues**:
   ```bash
   # Check volume permissions
   docker exec synapse-mcp ls -la /app/data

   # Fix permissions on host
   sudo chown -R $USER:$USER ./data
   ```

3. **Docker not running**:
   ```bash
   # Check Docker status
   docker info

   # Start Docker
   sudo systemctl start docker  # Linux
   # Or restart Docker Desktop (Windows/Mac)
   ```

---

### Health Check Fails

**Test health endpoint**:
```bash
curl http://localhost:8002/health
```

**Expected response**:
```json
{"status": "ok", "service": "synapse"}
```

**Debug mode**:
```bash
# Run with debug logging
docker run -d --name synapse-mcp \
  -e LOG_LEVEL=DEBUG \
  -p 8002:8002 \
  docker.io/kayisrahman/synapse:1.0.0

# View detailed logs
docker logs -f synapse-mcp
```

---

### Out of Memory

**Check resource usage**:
```bash
docker stats synapse-mcp
```

**Increase memory limit** (Docker Compose):
```yaml
services:
  synapse-mcp:
    deploy:
      resources:
        limits:
          memory: 4G  # Increase from default
```

**Or reduce cache size**:
```bash
docker run -d --name synapse-mcp \
  -e EMBEDDING_CACHE_SIZE=500 \
  -p 8002:8002 \
  docker.io/kayisrahman/synapse:1.0.0
```

---

### CLI Commands Not Working

**Check container is running**:
```bash
docker ps | grep synapse-mcp
```

**Check script permissions**:
```bash
ls -la scripts/synapse-*

# Make executable if needed
chmod +x scripts/synapse-ignite
chmod +x scripts/synapse-sense
chmod +x scripts/synapse-feed
```

**Check script path**:
```bash
# Ensure you're in SYNAPSE directory
pwd  # Should be /path/to/synapse
ls scripts/synapse-*
```

---

### Volume Issues

**Inspect volume**:
```bash
docker volume inspect synapse-data
```

**Volume contents**:
```bash
docker run --rm -v synapse-data:/data alpine ls -la /data
```

**Backup volume**:
```bash
docker run --rm \
  -v synapse-data:/data \
  -v $(pwd):/backup \
  alpine tar czf /backup/synapse-data-backup.tar.gz /data
```

**Restore volume**:
```bash
docker run --rm \
  -v synapse-data:/data \
  -v $(pwd):/backup \
  alpine sh -c "cd /data && tar xzf /backup/synapse-data-backup.tar.gz --strip 1"
```

---

### Network Issues

**Test connectivity**:
```bash
# Test MCP endpoint
curl http://localhost:8002/mcp

# Test from inside container
docker exec synapse-mcp curl http://localhost:8002/health

# Check container IP
docker inspect synapse-mcp | grep IPAddress
```

**Firewall issues**:
```bash
# Allow port 8002 (Linux)
sudo ufw allow 8002

# Check firewall rules
sudo ufw status
```

---

## Advanced Usage

### Multi-Container Setup

Run multiple SYNAPSE instances:

```bash
# Instance 1 (port 8002)
docker run -d --name synapse-mcp-1 \
  -p 8002:8002 \
  -v synapse-data-1:/app/data \
  docker.io/kayisrahman/synapse:1.0.0

# Instance 2 (port 8003)
docker run -d --name synapse-mcp-2 \
  -p 8003:8002 \
  -v synapse-data-2:/app/data \
  docker.io/kayisrahman/synapse:1.0.0
```

---

### Custom Entrypoint

```bash
docker run -d --name synapse-mcp \
  --entrypoint python \
  docker.io/kayisrahman/synapse:1.0.0 \
  -c "print('Custom entrypoint')"
```

---

### Debugging Shell

```bash
# Interactive shell in running container
docker exec -it synapse-mcp bash

# Run container in interactive mode
docker run -it --rm \
  -p 8002:8002 \
  docker.io/kayisrahman/synapse:1.0.0 \
  bash
```

---

## Updating SYNAPSE

### Update Docker Image

```bash
# Pull latest version
docker pull docker.io/kayisrahman/synapse:latest

# Stop and remove old container
docker stop synapse-mcp
docker rm synapse-mcp

# Run new container
docker run -d --name synapse-mcp \
  -p 8002:8002 \
  -v synapse-data:/app/data \
  -v synapse-models:/app/models \
  docker.io/kayisrahman/synapse:latest
```

### Update with Docker Compose

```bash
# Pull latest image
docker compose -f docker-compose.mcp.yml pull

# Recreate container
docker compose -f docker-compose.mcp.yml up -d --force-recreate
```

---

## Uninstalling

### Stop and Remove Container

```bash
# Stop container
docker stop synapse-mcp

# Remove container
docker rm synapse-mcp

# Remove image
docker rmi docker.io/kayisrahman/synapse:1.0.0
```

### Remove Volumes (⚠️ Warning: Deletes data)

```bash
# Remove volumes
docker volume rm synapse-data synapse-models

# List all volumes
docker volume ls

# Remove all unused volumes
docker volume prune
```

### Complete Cleanup

```bash
# Stop all SYNAPSE containers
docker stop $(docker ps -q --filter name=synapse-mcp)

# Remove all SYNAPSE containers
docker rm $(docker ps -aq --filter name=synapse-mcp)

# Remove all SYNAPSE images
docker rmi $(docker images -q kayisrahman/synapse)

# Remove all SYNAPSE volumes
docker volume rm $(docker volume ls -q --filter name=synapse)

# Prune Docker
docker system prune -a --volumes
```

---

## Next Steps

- [Quick Start Guide](https://github.com/kayis-rahman/synapse#readme)
- [Configuration Guide](https://github.com/kayis-rahman/synapse/blob/main/docs/getting-started/configuration.md)
- [MCP Tools Reference](https://github.com/kayis-rahman/synapse/blob/main/docs/usage/mcp-tools.mdx)
- [Architecture Overview](https://github.com/kayis-rahman/synapse/blob/main/docs/architecture/overview.mdx)

---

## Support

- **Issues**: [GitHub Issues](https://github.com/kayis-rahman/synapse/issues)
- **Discussions**: [GitHub Discussions](https://github.com/kayis-rahman/synapse/discussions)
- **Documentation**: [Full Docs](https://kayis-rahman.github.io/synapse)

---

## License

MIT License - see LICENSE file for details.
