# Phase 1 Requirements: Foundation & Setup

**Feature ID**: 005-cli-priority-testing
**Phase**: 1 - Foundation & Setup
**Priority**: P0 (Critical Foundation)
**Status**: In Progress

---

## Overview

This phase validates the critical foundation commands that must work before any other functionality can operate. These commands are the prerequisites for all subsequent testing.

---

## User Stories

### US-1: First-Time Setup
**As a** new user,
**I want** to run `synapse setup` to initialize the system,
**So that** I can start using SYNAPSE without manual configuration.

**Acceptance Criteria:**
- Setup auto-detects the correct data directory
- Setup creates all required directories
- Setup downloads the BGE-M3 model if not present
- Setup works in all three modes: Docker, native, user home

### US-2: Configuration Verification
**As a** system administrator,
**I want** to run `synapse config` to view system state,
**So that** I can verify correct initialization before running operations.

**Acceptance Criteria:**
- Config command displays data directory path
- Config command displays models directory path
- Config command displays environment mode
- Config command displays all key settings

### US-3: Model Inventory
**As a** user,
**I want** to run `synapse models list` to see available models,
**So that** I can verify required models are installed and working.

**Acceptance Criteria:**
- Models list shows BGE-M3 embedding model if installed
- Models list shows model file size
- Models list shows model file path
- Models list correctly reports missing models

---

## Functional Requirements

### FR-1: Setup Command (P0-1)
The `synapse setup` command must:

**FR-1.1 Auto-Detection**
- Auto-detect data directory in order of priority:
  1. Docker: `/app/data` (if exists)
  2. Native: `/opt/synapse/data` (if exists)
  3. User Home: `~/.synapse/data` (fallback)

**FR-1.2 Directory Creation**
- Create all required directories if they don't exist:
  - `<data_dir>/`
  - `<data_dir>/models/`
  - `<data_dir>/rag_index/`
  - `<data_dir>/docs/`
  - `<data_dir>/logs/`

**FR-1.3 Model Download**
- Download BGE-M3 embedding model automatically
- Prompt user before downloading (unless `--offline` or `--no-model-check`)
- Support `--force` flag to re-download
- Support `--offline` flag to skip downloads
- Support `--no-model-check` flag to skip validation

**FR-1.4 Configuration Defaults**
- Load sensible defaults for all settings
- Create default `configs/rag_config.json` if not exists
- Allow custom config via `~/.synapse/config.json`

**FR-1.5 Cross-Platform Support**
- Work in Docker environment
- Work in native Linux environment
- Work on macOS (via user home)
- Work on Windows (via user home)

### FR-2: Config Command (P0-2)
The `synapse config` command must:

**FR-2.1 Configuration Display**
- Display all configuration settings
- Show paths (data, models, rag_index, etc.)
- Show server settings (port, host, log_level)
- Show RAG settings (chunk_size, top_k, etc.)

**FR-2.2 Verbose Mode**
- Support `--verbose` flag for detailed output
- Show all configuration values
- Show configuration source (default, file, environment)

**FR-2.3 Validation**
- Validate all paths exist
- Validate configuration is valid JSON
- Validate all required settings are present

### FR-3: Models List Command (P0-3)
The `synapse models list` command must:

**FR-3.1 Model Enumeration**
- List all known models (BGE-M3, chat models, etc.)
- Show installation status (installed/missing)
- Show model file path
- Show model file size

**FR-3.2 Model Information**
- Display model type (embedding, chat, etc.)
- Display model format (GGUF, ONNX, etc.)
- Display model quantization (q8_0, f16, etc.)

**FR-3.3 Accuracy**
- Correctly detect installed models
- Correctly detect missing models
- Show accurate file sizes
- Show accurate file paths

---

## Non-Functional Requirements

### NFR-1: Performance
- Setup completes within 60 seconds (excluding model download)
- Config command completes within 2 seconds
- Models list completes within 2 seconds

### NFR-2: Error Handling
- Handle missing dependencies gracefully
- Handle permission errors with clear messages
- Handle network errors during model download
- Handle invalid configuration files

### NFR-3: User Experience
- Provide clear, actionable error messages
- Show progress indicators for long operations (downloads)
- Support dry-run or preview modes where applicable
- Use consistent output formatting

### NFR-4: Reliability
- Setup creates directories with correct permissions
- Setup downloads complete models (not partial downloads)
- Commands handle concurrent execution safely
- Commands leave system in consistent state

---

## Test Environments

### TE-1: Docker Mode
- Target: Docker container running synapse
- Data directory: `/app/data`
- Execution: `docker exec rag-mcp synapse <command>`

### TE-2: Native Mode
- Target: Native Linux installation
- Data directory: `/opt/synapse/data`
- Execution: Direct command execution

### TE-3: User Home Mode
- Target: User's home directory
- Data directory: `~/.synapse/data`
- Execution: Direct command execution

**Note:** All three environments must be tested per user choice (Option A).

---

## Exit Criteria

Phase 1 is complete when ALL of the following are met:

1. **Setup Command (P0-1)**
   - [ ] Setup works in Docker mode
   - [ ] Setup works in native mode
   - [ ] Setup works in user home mode
   - [ ] All directories created correctly
   - [ ] BGE-M3 model downloaded or verified
   - [ ] Config file created/validated

2. **Config Command (P0-2)**
   - [ ] Config command runs in all modes
   - [ ] Config displays correct data directory
   - [ ] Config displays correct models directory
   - [ ] Config displays all key settings
   - [ ] Verbose mode works correctly

3. **Models List Command (P0-3)**
   - [ ] Models list runs in all modes
   - [ ] BGE-M3 model shows as installed (after setup)
   - [ ] Model file size displayed correctly
   - [ ] Model file path displayed correctly
   - [ ] Missing models reported correctly

4. **Error Handling (Failure Criteria Option C)**
   - [ ] Permission errors produce clear messages
   - [ ] Network errors during download are handled
   - [ ] Invalid config files are rejected with messages
   - [ ] Performance degradation is detected (>60s for setup)

5. **Test Artifacts**
   - [ ] Semi-automated test scripts created
   - [ ] Test results documented (pass/fail + metrics)
   - [ ] All tests passing
   - [ ] Central index.md updated with Phase 1 completion

---

## Risks & Mitigations

### Risk-1: Model Download Failure
**Risk**: BGE-M3 model download fails due to network or HuggingFace issues
**Mitigation**: Use `--offline` flag for testing, verify model exists manually

### Risk-2: Permission Issues
**Risk**: Cannot create directories in `/opt/synapse/data`
**Mitigation**: Run tests with appropriate permissions, test user home mode as fallback

### Risk-3: Docker Mode Limitations
**Risk**: Docker container doesn't have network access for downloads
**Mitigation**: Test `--offline` mode, pre-seed models in container image

### Risk-4: Cross-Platform Issues
**Risk**: Commands work on Linux but fail on macOS/Windows
**Mitigation**: Focus testing on Linux (primary platform), document platform limitations

---

## Dependencies

**No external dependencies** for Phase 1 testing.

All commands are part of SYNAPSE core functionality and should work independently.

---

## Success Metrics

- **Setup Success Rate**: 100% (3/3 modes)
- **Config Success Rate**: 100% (3/3 modes)
- **Models List Success Rate**: 100% (3/3 modes)
- **Performance Compliance**: 100% (all commands under time limits)
- **Error Handling**: 100% (all error scenarios produce clear messages)

---

## Related Documentation

- `AGENTS.md` - Spec-Driven Development (SDD) Protocol
- `pyproject.toml` - CLI entry points and configuration
- `synapse/cli/commands/setup.py` - Setup command implementation
- `synapse/cli/commands/models.py` - Models command implementation
- `synapse/config.py` - Configuration management

---

**Created**: January 7, 2026
**Last Updated**: January 7, 2026
