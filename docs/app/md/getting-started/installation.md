---
title: Installation
description: Install SYNAPSE on your platform
---

# Installation

Install SYNAPSE from source and verify your installation.

::tabs
:::tab{label="macOS"}
## macOS Installation

```bash
# Clone the repository
git clone https://github.com/kayis-rahman/synapse.git
cd synapse

# Install dependencies
pip install -e .

# Verify installation
synapse --help
```

**Expected output:**
```
 Usage: synapse [OPTIONS] COMMAND [ARGS]...

 SYNAPSE: Your Data Meets Intelligence - Local RAG System for AI Agents

╭─ Options ───────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                │
╰────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────╮
│ start     Start SYNAPSE server.                                            │
│ stop      Stop SYNAPSE server.                                             │
│ status    Check SYNAPSE system status.                                     │
│ ingest    Ingest documents into SYNAPSE knowledge base.                    │
│ query     Query SYNAPSE knowledge base.                                    │
│ config    Show SYNAPSE configuration.                                      │
│ setup     First-time SYNAPSE setup.                                        │
│ onboard   SYNAPSE Onboarding Wizard.                                       │
│ models    Model management commands                                        │
╰────────────────────────────────────────────────────────────────────────────╯
```

**Next**: [Quick Start →](./quick-start)
:::
:::tab{label="Linux"}
## Linux Installation

```bash
# Clone the repository
git clone https://github.com/kayis-rahman/synapse.git
cd synapse

# Install dependencies
pip install -e .

# Verify installation
synapse --help
```

**Expected output:**
```
 Usage: synapse [OPTIONS] COMMAND [ARGS]...

 SYNAPSE: Your Data Meets Intelligence - Local RAG System for AI Agents

╭─ Options ───────────────────────────────────────────────────────────────────╮
│ --help          Show this message and exit.                                │
╰────────────────────────────────────────────────────────────────────────────╯
╭─ Commands ─────────────────────────────────────────────────────────────────╮
│ start     Start SYNAPSE server.                                            │
│ stop      Stop SYNAPSE server.                                             │
│ status    Check SYNAPSE system status.                                     │
│ ingest    Ingest documents into SYNAPSE knowledge base.                    │
│ query     Query SYNAPSE knowledge base.                                    │
│ config    Show SYNAPSE configuration.                                      │
│ setup     First-time SYNAPSE setup.                                        │
│ onboard   SYNAPSE Onboarding Wizard.                                       │
│ models    Model management commands                                        │
╰────────────────────────────────────────────────────────────────────────────╯
```

**Next**: [Quick Start →](./quick-start)
:::
:::tab{label="Docker"}
## Docker Installation

```bash
# Pull the latest image
docker pull kayisrahman/synapse:latest

# Run the container
docker run -p 8002:8002 -v synapse-data:/opt/synapse/data kayisrahman/synapse
```

**What this does:**
- Starts SYNAPSE MCP server on port 8002
- Persists data in Docker volume `synapse-data`
- Exposes HTTP endpoint at http://localhost:8002/mcp

**Next**: [Quick Start →](./quick-start)
:::
::

## Prerequisites

Before installing, ensure you have:

- **Python 3.8+** - Run `python3 --version` to verify
- **git** - Run `git --version` to verify
- **pip** - Run `pip --version` to verify

## Troubleshooting

::details{label="Python version error"}
If you see a Python version error, make sure you have Python 3.8 or higher:

```bash
# Check Python version
python3 --version

# If needed, install Python 3.11 on macOS
brew install python@3.11

# On Linux (Ubuntu/Debian)
sudo apt update
sudo apt install python3.11
```
::

::details{label="pip install error"}
If pip install fails, try:

```bash
# Upgrade pip first
pip install --upgrade pip

# Try again
pip install -e .
```

Still having issues? Check that you're using the correct Python installation.
::
