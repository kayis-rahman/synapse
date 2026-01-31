---
title: Ingestion
description: Bulk and single file ingestion
---

# Ingestion

SYNAPSE provides multiple ways to ingest your data into memory.

## CLI Ingestion

Use the `synapse ingest` command to ingest files and directories:

```bash
# Ingest current directory
synapse ingest .

# Ingest specific directory
synapse ingest /path/to/your/docs

# Ingest specific file
synapse ingest /path/to/file.py

# Filter by file type
synapse ingest . --file-type code --file-type doc

# Custom exclusions
synapse ingest . --exclude "*.log" --exclude "*.tmp"
```

## Bulk Ingestion Script

For advanced ingestion with .gitignore awareness and incremental updates:

```bash
# Preview what will be ingested
python3 -m scripts.bulk_ingest --root-dir . --dry-run

# Ingest all files
python3 -m scripts.bulk_ingest --root-dir .

# Ingest specific directory
python3 -m scripts.bulk_ingest --root-dir /path/to/project

# Filter by file type
python3 -m scripts.bulk_ingest --root-dir . --file-type code --file-type doc

# Custom exclusions
python3 -m scripts.bulk_ingest --root-dir . --no-gitignore --exclude "*.log"
```

## File Type Filters

- **code** - Programming language files (.py, .js, .ts, .java, .cpp, etc.)
- **config** - Configuration files (.json, .yaml, .toml, .env, etc.)
- **doc** - Documentation files (.md, .txt, .rst, .pdf, etc.)
- **web** - Web files (.html, .css, .scss, .vue, etc.)
- **data** - Data files (.csv, .sql, .tsv, etc.)
- **devops** - DevOps files (Dockerfile, Makefile, Jenkinsfile, etc.)

## Features

- ✅ **.gitignore Pattern Parsing** - Automatically reads and applies `.gitignore`
- ✅ **Incremental Ingestion** - Skip files that haven't changed (checksum-based)
- ✅ **Retry Mechanism** - Failed files are saved and retried on subsequent runs
- ✅ **Progress Tracking** - Visual progress bar with detailed statistics
- ✅ **Project-Based** - Reusable for any project with configurable project ID

## Via MCP Tool

```json
{
  "method": "tools/call",
  "params": {
    "name": "synapse.ingest_file",
    "arguments": {
      "file_path": "/path/to/file.py",
      "metadata": {
        "project_id": "synapse",
        "type": "code"
      }
    }
  }
}
```

Next: [Querying](./querying)
