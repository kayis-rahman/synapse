# MCP Server Deployment Guide - Pi 5 + Mac M1

## Overview

Deploy RAG MCP Server on Raspberry Pi 5 and access from Mac M1 via MCP clients (Claude Desktop, Cline, Cursor).

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│  Mac M1 (Client)                                      │
│  - Claude Desktop / Cline / Cursor                      │
│  - MCP stdio connection via SSH                           │
└──────────────────────┬──────────────────────────────────────┘
                       │ SSH Tunnel / Network
                       │
┌──────────────────────▼──────────────────────────────────────┐
│  Raspberry Pi 5 (Server)                                │
│  - Docker container: rag-mcp:latest                   │
│  - MCP stdio server (7 tools)                         │
│  - RAG package: All 4 phases                         │
│  - Data: Local volume (persistant)                     │
│  - Models: /app/models (BGE-M3-Q8_0.GGUF)         │
└──────────────────────────────────────────────────────────────┘
```

## Prerequisites

### Raspberry Pi 5

- OS: Raspbian 12+ or Ubuntu 22.04+
- RAM: 8 GB (4 GB minimum, 8 GB recommended)
- Storage: 10 GB free space
- Network: WiFi configured and connected
- Software:
  - Docker 24.0+
  - Docker Compose 2.0+
  - Git (optional, for cloning repo)

### Mac M1

- macOS: Sonoma (14) or later
- Software:
  - Claude Desktop / Cline (VSCode) / Cursor
  - SSH client (terminal or SSH key configured)
  - Optional: SSH config in `~/.ssh/config`

---

## Phase 1: Setup on Raspberry Pi 5

### 1.1 Clone/Update Repository

```bash
# Navigate to project directory
cd /home/dietpi

# Update existing repo
cd pi-rag
git pull origin main

# Or clone fresh
git clone https://github.com/your-repo/pi-rag.git
cd pi-rag
```

### 1.2 Prepare Models

```bash
# Check if models exist
ls -lh ~/models/

# Expected: bge-m3-q8_0.gguf (589 MB)

# If not present, download:
mkdir -p ~/models
# Download BGE-M3 model (you have it already)
# From: https://huggingface.co/BAAI/bge-m3
```

### 1.3 Build Docker Image

```bash
# Build MCP server image (optimized for Pi 5)
docker compose -f docker-compose.mcp.yml build --no-cache

# Expected output:
# ✅ MCP SDK OK
# ✅ RAG imports OK
# ✅ Server syntax OK
# Image rag-mcp:latest built (1.1 GB)
```

### 1.4 Start MCP Server

```bash
# Start MCP server container
docker compose -f docker-compose.mcp.yml up -d

# Verify running
docker compose -f docker-compose.mcp.yml ps

# Check logs
docker compose -f docker-compose.mcp.yml logs -f

# Expected output:
# Starting RAG MCP Server...
# Data directory: /app/data
# Available tools: 7
# Server ready (stdio)
```

### 1.5 Verify Services

```bash
# Check container status
docker ps | grep rag-mcp

# Expected:
# rag-mcp   Up 5 minutes   rag-mcp:latest

# Verify all 7 tools in logs
docker compose -f docker-compose.mcp.yml logs --tail 50
```

---

## Phase 2: Configure Mac M1 Access

### 2.1 Find Pi 5 IP Address

**On Pi 5:**
```bash
# Get WiFi IP
hostname -I
# or
ip addr show wlan0 | grep "inet " | awk '{print $2}'

# Example output: 192.168.1.100
```

**On Mac M1:**
```bash
# Scan for Raspberry Pi on network
arp -a | grep -i b8:27:eb

# Example: 192.168.1.100 at b8:27:eb:xx:xx:xx
```

### 2.2 Setup SSH Access (Required for MCP stdio)

**Option A: SSH Key Authentication (Recommended)**

**Generate SSH key on Mac M1:**
```bash
# Generate new SSH key
ssh-keygen -t ed25519 -f ~/.ssh/pi_rag_ed25519 -N ""

# Copy public key to Pi 5
cat ~/.ssh/pi_rag_ed25519.pub
```

**Add key to Pi 5:**
```bash
# On Mac M1, copy key
ssh-copy-id -i ~/.ssh/pi_rag_ed25519.pub dietpi@<PI-IP>

# Or manually on Pi 5:
mkdir -p ~/.ssh
nano ~/.ssh/authorized_keys
# Paste public key content
chmod 600 ~/.ssh/authorized_keys
chmod 700 ~/.ssh
```

**Option B: Password Authentication**

```bash
# On Mac M1, test connection
ssh dietpi@<PI-IP>

# Enter password when prompted
# Should login to Pi 5 shell
```

### 2.3 Configure SSH Config (Optional but Recommended)

**On Mac M1, edit `~/.ssh/config`:**
```bash
nano ~/.ssh/config
```

**Add Pi 5 configuration:**
```
Host pi-rag
    HostName <PI-IP>
    User dietpi
    IdentityFile ~/.ssh/pi_rag_ed25519
    ServerAliveInterval 60
    ServerAliveCountMax 3
```

**Test connection:**
```bash
ssh pi-rag
# Should connect without password prompt (if using SSH key)
```

---

## Phase 3: Configure MCP Client on Mac M1

### 3.1 Claude Desktop Configuration

**Configuration file location:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Add MCP server configuration:**
```json
{
  "mcpServers": {
    "pi-rag-server": {
      "command": "ssh",
      "args": [
        "-i", "~/.ssh/pi_rag_ed25519",
        "pi-rag",
        "docker", "run", "-i", "--rm",
        "-e", "RAG_DATA_DIR=/app/data",
        "-e", "LOG_LEVEL=INFO",
        "-v", "rag-mcp-data:/app/data",
        "-v", "rag-mcp-models:/app/models:ro",
        "rag-mcp:latest"
      ],
      "env": {}
    }
  }
}
```

**Restart Claude Desktop:**
```bash
# Quit and reopen Claude Desktop
# Or use Activity Monitor to force quit
```

**Verify in Claude Desktop:**
1. Open Claude Desktop
2. Go to Settings → MCP Servers
3. Should see "pi-rag-server" listed
4. Expand to see 7 tools available

### 3.2 Cline (VSCode) Configuration

**Configuration file location:**
```bash
~/.vscode/settings.json
```

**Add MCP server configuration:**
```json
{
  "cline.mcpServers": [
    {
      "name": "pi-rag-server",
      "command": "ssh",
      "args": [
        "-i", "~/.ssh/pi_rag_ed25519",
        "pi-rag",
        "docker", "run", "-i", "--rm",
        "-e", "RAG_DATA_DIR=/app/data",
        "-e", "LOG_LEVEL=INFO",
        "-v", "rag-mcp-data:/app/data",
        "-v", "rag-mcp-models:/app/models:ro",
        "rag-mcp:latest"
      ]
    }
  ]
}
```

**Restart VSCode:**
```bash
# Reload VSCode window (Cmd+Shift+P → "Developer: Reload Window")
```

### 3.3 Cursor Configuration

**Configuration file location:**
```bash
~/Library/Application Support/Cursor/cursor_config.json
```

**Add MCP server configuration:**
```json
{
  "mcpServers": {
    "pi-rag-server": {
      "command": "ssh",
      "args": [
        "-i", "~/.ssh/pi_rag_ed25519",
        "pi-rag",
        "docker", "run", "-i", "--rm",
        "-e", "RAG_DATA_DIR=/app/data",
        "-e", "LOG_LEVEL=INFO",
        "-v", "rag-mcp-data:/app/data",
        "-v", "rag-mcp-models:/app/models:ro",
        "rag-mcp:latest"
      ],
      "env": {}
    }
  }
}
```

**Restart Cursor:**
```bash
# Quit and reopen Cursor
```

---

## Phase 4: Testing

### 4.1 Test from Mac M1

**Test 1: Verify SSH Connection**
```bash
# On Mac M1
ssh pi-rag "echo 'SSH connection successful'"

# Expected: SSH connection successful
```

**Test 2: Verify Docker Accessible**
```bash
# On Mac M1
ssh pi-rag "docker ps | grep rag-mcp"

# Expected: rag-mcp container listed
```

**Test 3: Verify MCP Tools Available**

**In Claude Desktop / Cline / Cursor:**
1. Open chat interface
2. Ask: "List available RAG projects"
3. Should trigger `rag.list_projects` tool

**Expected behavior:**
- Tool executes successfully
- Returns list of projects (org, user, session, project)
- No errors in logs

**Test 4: Add Symbolic Memory Fact**

**In Claude Desktop / Cline / Cursor:**
```
User: Add a fact to symbolic memory
Claude: [uses rag.add_fact tool]
```

**Verify on Pi 5:**
```bash
docker compose -f docker-compose.mcp.yml logs --tail 20

# Expected: "Adding fact for project session..."
```

**Test 5: Add Episodic Memory Episode**

**In Claude Desktop / Cline / Cursor:**
```
User: Record an episode about fixing a bug
Claude: [uses rag.add_episode tool]
```

**Verify on Pi 5:**
```bash
docker compose -f docker-compose.mcp.yml logs --tail 20

# Expected: "Adding episode for project session..."
```

**Test 6: Ingest File**

**In Claude Desktop / Cline / Cursor:**
```
User: Ingest a file to semantic memory
Claude: [uses rag.ingest_file tool]
```

**Verify on Pi 5:**
```bash
docker compose -f docker-compose.mcp.yml logs --tail 20

# Expected: "Ingesting file for project session..."
```

**Test 7: Query All Memory Types**

**In Claude Desktop / Cline / Cursor:**
```
User: Get context about the project
Claude: [uses rag.get_context tool]
```

**Verify on Pi 5:**
```bash
docker compose -f docker-compose.mcp.yml logs --tail 20

# Expected: "Getting context for project session..."
```

---

## Phase 5: Monitor and Troubleshooting

### 5.1 Check Logs on Pi 5

**Real-time logs:**
```bash
docker compose -f docker-compose.mcp.yml logs -f

# Last 100 lines
docker compose -f docker-compose.mcp.yml logs --tail 100

# Last 24 hours
docker compose -f docker-compose.mcp.yml logs --since 24h
```

### 5.2 Restart MCP Server

```bash
# Restart container
docker compose -f docker-compose.mcp.yml restart

# Stop and start
docker compose -f docker-compose.mcp.yml down
docker compose -f docker-compose.mcp.yml up -d
```

### 5.3 Check Resource Usage

```bash
# Container stats
docker stats rag-mcp

# Expected output:
# NAME      CPU %     MEM USAGE / LIMIT   NET I/O   BLOCK I/O   PIDS
# rag-mcp   2.5%      512Mi / 3GiB        0B / 0B    0B / 0B      15
```

### 5.4 Data Backup

```bash
# Backup data volume
docker run --rm -v rag-mcp-data:/data -v $(pwd):/backup \
  ubuntu tar czf /backup/pi-rag-data-backup-$(date +%Y%m%d).tar.gz /data

# Backup models volume
docker run --rm -v rag-mcp-models:/models -v $(pwd):/backup \
  ubuntu tar czf /backup/pi-rag-models-backup-$(date +%Y%m%d).tar.gz /models
```

---

## Troubleshooting

### Issue 1: MCP Tools Not Visible

**Symptoms:**
- Tools not listed in Claude Desktop/Cline/Cursor
- Error: "Failed to connect to MCP server"

**Solutions:**

1. **Check SSH connection:**
   ```bash
   ssh pi-rag "echo 'SSH test'"
   ```

2. **Verify Docker container running:**
   ```bash
   ssh pi-rag "docker ps | grep rag-mcp"
   ```

3. **Check MCP server logs:**
   ```bash
   ssh pi-rag "docker logs rag-mcp --tail 50"
   ```

4. **Restart MCP client:**
   - Quit and reopen Claude Desktop/Cline/Cursor

### Issue 2: High Memory Usage

**Symptoms:**
- Pi 5 becomes slow
- Docker container OOM (out of memory) killed

**Solutions:**

1. **Check current usage:**
   ```bash
   docker stats rag-mcp
   ```

2. **Adjust resource limits in docker-compose.mcp.yml:**
   ```yaml
   deploy:
     resources:
       limits:
         memory: 2G  # Reduce from 3G
   ```

3. **Restart container:**
   ```bash
   docker compose -f docker-compose.mcp.yml restart
   ```

### Issue 3: Model Not Found

**Symptoms:**
- Error: "Model file not found: ~/models/bge-m3-q8_0.gguf"
- Semantic search not working

**Solutions:**

1. **Verify model in volume:**
   ```bash
   docker run --rm -v rag-mcp-models:/models ubuntu ls -lh /models/
   ```

2. **Copy model to volume:**
   ```bash
   docker run --rm -v ~/models:/host_models -v rag-mcp-models:/models \
     ubuntu cp /host_models/bge-m3-q8_0.gguf /models/
   ```

3. **Restart container:**
   ```bash
   docker compose -f docker-compose.mcp.yml restart
   ```

### Issue 4: SSH Connection Refused

**Symptoms:**
- Error: "Connection refused"
- SSH key not working

**Solutions:**

1. **Verify SSH service on Pi 5:**
   ```bash
   # On Pi 5
   sudo systemctl status ssh
   sudo systemctl start ssh
   ```

2. **Check SSH config on Mac M1:**
   ```bash
   # On Mac M1
   cat ~/.ssh/config
   # Verify IP, user, key path correct
   ```

3. **Try password authentication:**
   ```bash
   # On Mac M1
   ssh dietpi@<PI-IP>
   # If works, SSH key issue
   ```

### Issue 5: Tools Timing Out

**Symptoms:**
- Tools take long time to respond
- Timeout errors

**Solutions:**

1. **Check network latency:**
   ```bash
   # On Mac M1
   ping -c 10 <PI-IP>
   # Expect: <50ms for local WiFi
   ```

2. **Check Pi 5 CPU/Memory:**
   ```bash
   # On Pi 5
   docker stats rag-mcp
   ```

3. **Increase timeout in client config** (if supported):
   - Claude Desktop: No timeout setting
   - Cline: Check settings for timeout
   - Cursor: Check settings for timeout

---

## MCP Tools Reference

### Available Tools (7 total)

1. **rag.list_projects**
   - List all projects (org, user, session, project)
   - No parameters

2. **rag.list_sources**
   - List document sources for a project
   - Parameters: project_id (required), source_type (optional)

3. **rag.get_context**
   - Get comprehensive context from all memory types
   - Parameters: project_id (required), context_type (optional), query (optional), max_results (optional)

4. **rag.search**
   - Semantic search across all memory types
   - Parameters: project_id (required), query (required), memory_type (optional), top_k (optional)

5. **rag.ingest_file**
   - Ingest file into semantic memory
   - Parameters: project_id (required), file_path (required), source_type (optional), metadata (optional)

6. **rag.add_fact**
   - Add fact to symbolic memory (authoritative)
   - Parameters: project_id (required), fact_key (required), fact_value (required), confidence (optional), category (optional)

7. **rag.add_episode**
   - Add episode to episodic memory (advisory)
   - Parameters: project_id (required), title (required), content (required), lesson_type (optional), quality (optional)

---

## System Information

### Raspberry Pi 5 Specifications

- CPU: Broadcom BCM2712, Cortex-A76 (ARM64)
- Cores: 4 @ 2.4 GHz
- RAM: 8 GB LPDDR4X-4267
- Storage: SD Card or NVMe SSD
- Network: WiFi 6 (802.11ax) + Ethernet

### Docker Configuration

- Container OS: Debian 12 (Python 3.11-slim)
- Resource Limits:
  - CPU: 3 cores (leave 1 for OS)
  - Memory: 3 GB (leave 5 GB for OS)
  - Reservations: 0.5 CPU, 512 MB RAM
- Volumes:
  - rag-mcp-data: Persistent data
  - rag-mcp-models: GGUF models
- Network: Bridge (172.21.0.0/16)

### MCP Server

- Image: rag-mcp:latest (1.1 GB)
- Transport: stdio (stdin/stdout)
- Tools: 7 functional tools
- Memory System: All 4 phases
  - Phase 1: Symbolic (authoritative)
  - Phase 2: Contextual (integrated)
  - Phase 3: Episodic (advisory)
  - Phase 4: Semantic (non-authoritative)
- Model: BGE-M3-Q8_0.GGUF (embeddings)

---

## Summary

### Deployment Complete Checklist

**Raspberry Pi 5:**
- [ ] Repository cloned/updated
- [ ] Docker image built successfully
- [ ] Container running (docker ps)
- [ ] All 7 tools available in logs
- [ ] Models accessible in container
- [ ] Data volume created and writable
- [ ] No errors in logs

**Mac M1:**
- [ ] SSH key generated and added to Pi 5
- [ ] SSH connection working
- [ ] Docker accessible via SSH
- [ ] Claude Desktop configured
- [ ] Cline configured (optional)
- [ ] Cursor configured (optional)
- [ ] All 7 tools visible in client
- [ ] Can add facts from Mac
- [ ] Can query episodes from Mac
- [ ] Can ingest files from Mac
- [ ] Data persists on Pi

**End-to-End:**
- [ ] SSH connection stable
- [ ] MCP tools responding within 5 seconds
- [ ] Memory operations working
- [ ] Data persists across container restarts
- [ ] System stable under load

---

## Next Steps

1. **Monitor Performance**: Track CPU/memory usage on Pi 5
2. **Test Heavy Loads**: Test with large files and many queries
3. **Optimize**: Adjust resource limits based on real usage
4. **Backup**: Set up automated backups of data volume
5. **Document**: Record any issues and solutions

---

## Support

For issues or questions:

1. Check logs: `docker compose -f docker-compose.mcp.yml logs -f`
2. Verify SSH: `ssh pi-rag "echo test"`
3. Check resources: `docker stats rag-mcp`
4. Review this documentation

---

**Deployment Guide Version:** 1.0
**Last Updated:** 2025-12-29
**Status:** Production Ready
