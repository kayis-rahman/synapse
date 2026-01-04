# Changelog

All notable changes to SYNAPSE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-01-04

### Added
- Initial SYNAPSE v1.0.0 release
- MCP HTTP server implementation with 7 tools
- Three memory types (symbolic, episodic, semantic)
- Docker deployment support with docker-compose.synapse.yml
- Neurobiological CLI commands (synapse-ignite, synapse-sense, synapse-feed)
- CLI migration and project setup script (scripts/migrate_and_setup.sh)
- Comprehensive test suite (config, memory_store, episodic_store, semantic_store, migration)
- Documentation suite (README.md, CHANGELOG.md, CONTRIBUTING.md, SECURITY.md, UPGRADE.md)
- LICENSE file (MIT License)
- Makefile for common build/test/docker tasks
- Docker Hub local testing script (scripts/test_docker_build.sh)

### Changed
- Project renamed from "pi-rag" to "synapse" for better branding
- All project_id references: `pi-rag` → `synapse`
- All directory paths: `/opt/pi-rag/data` → `/opt/synapse/data`
- Environment variables and configuration for consistency
- Unified version across all files: 1.0.0
- Production logger paths updated to use `/app/` prefix (container-aware)
- ChromaDB manager default path updated to `/opt/synapse/data`
- Project manager default path updated to `/opt/synapse/data`
- HTTP wrapper config path updated to `/home/dietpi/synapse/configs/`

### Fixed
- Version conflict between pyproject.toml, VERSION file, setup.py, and rag/__init__.py
- Missing LICENSE file that was referenced in README.md
- Missing industry-standard documentation files (CHANGELOG.md, SECURITY.md, CONTRIBUTING.md)
- CLI entry points properly configured in setup.py and pyproject.toml
- Hardcoded paths in Python source files updated to use synapse naming

### MCP Tools
1. **rag.list_projects** - List all projects in RAG memory system
2. **rag.list_sources** - List document sources for a project
3. **rag.get_context** - Get comprehensive context from all memory types
4. **rag.search** - Semantic search across all memory types
5. **rag.ingest_file** - Ingest file into semantic memory (HTTP upload)
6. **rag.add_fact** - Add symbolic memory fact (authoritative)
7. **rag.add_episode** - Add episodic memory episode (advisory)

### Memory System
- **Symbolic Memory** (Cell Bodies) - Authoritative facts with 100% confidence
- **Episodic Memory** (Synapses) - Lessons learned from experience with 85% confidence
- **Semantic Memory** (Dendrites) - Document embeddings as reference suggestions

### Deployment
- **Docker**: `docker compose -f docker-compose.synapse.yml up -d`
- **Data Directory**: `/opt/synapse/data/`
- **MCP Endpoint**: `http://localhost:8002/mcp`
- **Health Check**: `http://localhost:8002/health`

### Migration
- Migration from pi-rag to synapse uses directory move (not symlink)
- Run: `./scripts/migrate_and_setup.sh check` (dry-run)
- Run: `./scripts/migrate_and_setup.sh migrate --yes` (execute)
- Automatic database backup before migration

### Documentation
- [README.md](README.md) - Quick start guide
- [CHANGELOG.md](CHANGELOG.md) - Version history (this file)
- [CONTRIBUTING.md](CONTRIBUTING.md) - Development setup
- [SECURITY.md](SECURITY.md) - Vulnerability disclosure
- [UPGRADE.md](UPGRADE.md) - Migration guide
- [DOCKER_INSTALLATION.md](DOCKER_INSTALLATION.md) - Docker deployment

### Testing
- Unit tests: `make test` or `pytest tests/ -v`
- Integration tests: MCP server tested with synapse project_id
- Docker build tests: `./scripts/test_docker_build.sh`
- Test coverage target: 70%+

---

## [Unreleased] - Future Work

- Docker Hub publishing (deferred from v1.0.0)
- Additional CLI tool enhancements
- Performance optimization
- Additional memory types
