---
title: Introduction
description: What is SYNAPSE and how it works
---

# Introduction

**SYNAPSE** is a local-first RAG (Retrieval-Augmented Generation) system that connects your knowledge to AI.

## Core Features

- **Three Memory Types**: Semantic (vectors), Episodic (lessons), Symbolic (facts)
- **MCP Protocol Integration**: Connect to AI agents via Model Context Protocol
- **Local Embedding Model**: BGE-M3 runs entirely on your machine
- **Privacy-First**: Your data never leaves your system

## Quick Example

```bash
# Start server
python -m synapse.cli.main start

# Query your knowledge
python -m synapse.cli.main query "What did I learn?"
```

[Quick Start →](./quick-start)
