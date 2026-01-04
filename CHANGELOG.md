# Changelog

All notable changes to SYNAPSE will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2025-01-04

### Added
- Renamed project from "pi-rag" to "synapse" for better branding
- Created backward compatibility symlink `/opt/synapse` → `/opt/pi-rag`
- Added parallel deployment support with container versioning (v1/v2)
- Created LICENSE file (MIT License)
- Added CHANGELOG.md following Keep a Changelog standard
- Added SECURITY.md vulnerability disclosure policy
- Added 'sy' CLI shortname command (2-character Unix standard)
- Created Makefile for common build/test/docker tasks
- Created UPGRADE.md migration guide (v1 → v2)

### Changed
- All project_id references: `pi-rag` → `synapse`
- All directory paths: `/opt/pi-rag/data` → `/opt/synapse/data`
- Environment variables and configuration for consistency
- Docker image versioning: synapse:v1.0.0 (old) and synapse:v2.0.0 (new)
- Database project IDs: episodic episodes updated to use 'synapse'
- Setup.py version fallback fixed to match VERSION file
- pyproject.toml version updated to 2.0.0
- Production logger paths updated to use `/app/` prefix (container-aware)

### Fixed
- Version conflict between pyproject.toml, VERSION file, and setup.py fallback
- Missing LICENSE file that was referenced in README.md
- Missing industry-standard documentation files (CHANGELOG.md, SECURITY.md)
- CLI entry points missing "sy" shortname command
- Hardcoded paths in configuration files updated to use environment variables

### Removed
- All "pi-rag" references removed from codebase
- Old deployment references removed
- Legacy directory references removed

## [1.0.0] - 2024-12-29

### Added
- Initial SYNAPSE release (renamed from pi-rag)
- MCP HTTP server implementation
- Three memory types (symbolic, episodic, semantic)
- Docker containerization
- Complete documentation suite
