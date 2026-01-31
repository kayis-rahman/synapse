---
title: CLI Commands Complete Reference
description: All SYNAPSE CLI commands
---

# All SYNAPSE CLI Commands

Complete reference for all SYNAPSE command-line interface commands.

## Available Commands

| Command | Description |
|---------|-------------|
| `synapse start` | Start SYNAPSE server |
| `synapse stop` | Stop SYNAPSE server |
| `synapse status` | Check SYNAPSE system status |
| `synapse ingest` | Ingest documents into knowledge base |
| `synapse query` | Query knowledge base |
| `synapse config` | Show SYNAPSE configuration |
| `synapse setup` | First-time SYNAPSE setup |
| `synapse onboard` | SYNAPSE Onboarding Wizard |
| `synapse models` | Model management commands |

## Quick Reference

```bash
# Start server
synapse start

# Stop server
synapse stop

# Check status
synapse status

# Ingest files
synapse ingest .

# Query knowledge base
synapse query "your question"

# Show configuration
synapse config

# Run onboarding wizard
synapse onboard
```

## Command Summary

### synapse start

Start SYNAPSE server (MCP HTTP server on port 8002).

```bash
# Start in native mode
synapse start

# Start with custom port
synapse start --port 9000

# Start in Docker mode
synapse start --docker
```

### synapse stop

Stop SYNAPSE server.

```bash
synapse stop
```

### synapse status

Check SYNAPSE system status.

```bash
# Brief status
synapse status

# Verbose status
synapse status --verbose
```

### synapse ingest

Ingest documents into SYNAPSE knowledge base.

```bash
# Ingest current directory
synapse ingest .

# Ingest specific path
synapse ingest /path/to/your/docs

# Ingest with file type filter
synapse ingest . --file-type code --file-type doc

# Ingest with exclusions
synapse ingest . --exclude "*.log" --exclude "*.tmp"
```

### synapse query

Query SYNAPSE knowledge base.

```bash
# Simple query
synapse query "How does SYNAPSE work?"

# Get more results
synapse query "your question" --top-k 5

# JSON output for automation
synapse query "your question" --format json
```

### synapse config

Show SYNAPSE configuration.

```bash
# Brief config
synapse config

# Verbose config
synapse config --verbose
```

### synapse setup

First-time SYNAPSE setup.

```bash
# Fresh setup
synapse setup

# Force re-setup
synapse setup --force

# Offline mode (no model download)
synapse setup --offline
```

### synapse onboard

SYNAPSE Onboarding Wizard.

```bash
# Interactive mode
synapse onboard

# Quick mode
synapse onboard --quick

# Skip test
synapse onboard --skip-test

# Skip ingestion
synapse onboard --skip-ingest
```

### synapse models

Model management commands.

```bash
# List installed models
synapse models list

# Download a model
synapse models download bge-m3

# Verify model
synapse models verify

# Remove a model
synapse models remove bge-m3
```

---

## See Also

- [Getting Started](/getting-started/introduction) - Get started with SYNAPSE
- [MCP Protocol](/usage/mcp-tools.md) - MCP tools documentation
- [API Reference - Server API](/api-reference/server-api.md) - HTTP API endpoints
- [API Reference - Memory Tools](/api-reference/memory-tools.md) - Python memory APIs
- [Development](/development/contributing.md) - Contributing, testing, and deployment
