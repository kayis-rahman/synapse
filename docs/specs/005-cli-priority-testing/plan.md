# Phase 1 Plan: Foundation & Setup Testing

**Feature ID**: 005-cli-priority-testing
**Phase**: 1 - Foundation & Setup
**Priority**: P0 (Critical Foundation)
**Status**: Planning

---

## Overview

This plan details the testing strategy for P0 (Critical Foundation) commands: `synapse setup`, `synapse config`, and `synapse models list`. These commands must work correctly before any other functionality can be validated.

---

## Testing Strategy

### Approach: Semi-Automated Scripts with Assertions

Based on user choice (Option 4-C), we'll create:
- **Test Scripts**: Python scripts with built-in assertions
- **Manual Execution**: Run scripts and observe results
- **Assertions**: Check exit codes, output format, and performance
- **Documentation**: Record pass/fail + metrics

**Why Semi-Automated?**
- Full automation (pytest) is overkill for CLI commands
- Manual procedures alone are error-prone
- Scripts with assertions provide repeatability without test framework overhead

### Test Environments: All Three Modes (Option 1-A)

Per user choice (Option 1-A), we'll test all three environments:
1. **Docker Mode**: Running inside `rag-mcp` container
2. **Native Mode**: Direct execution on host system
3. **User Home Mode**: Execution using `~/.synapse/data`

**Order of Testing**:
1. Docker mode (production environment)
2. Native mode (primary deployment)
3. User home mode (fallback/cross-platform)

### Test Data: Existing Project Files (Option 2-No)

Per user choice (Option 2-No), we'll use existing project files:
- README.md for ingestion tests (Phase 3)
- configs/rag_config.json for config validation
- Existing models in /opt/synapse/data/models

**Why Not Create Fixtures?**
- Existing files are more realistic
- Avoids fixture maintenance overhead
- Tests actual system as deployed

### Failure Criteria: Comprehensive (Option 3-C)

Per user choice (Option 3-C), a test fails if:
- **Error**: Command exits with non-zero code
- **Wrong Output Format**: Output doesn't match expected format
- **Performance Degradation**: Command exceeds time limits

---

## Architecture & Design

### Test Script Structure

```
tests/cli/
├── __init__.py
├── conftest.py              # Common test fixtures and utilities
├── test_p0_setup.py         # P0-1: synapse setup tests
├── test_p0_config.py        # P0-2: synapse config tests
└── test_p0_models_list.py    # P0-3: synapse models list tests
```

### Test Script Template

Each test script follows this pattern:

```python
#!/usr/bin/env python3
"""
Phase 1 Test: P0-X <Command Name>

Tests <command> in multiple environments with assertions.
"""

import subprocess
import sys
import time
from pathlib import Path
from typing import Dict, Tuple, List

# Test results storage
test_results: List[Dict[str, any]] = []

# Configuration
TIMEOUTS = {
    "setup": 60,      # seconds
    "config": 2,       # seconds
    "models_list": 2    # seconds
}

# Environments to test
ENVIRONMENTS = {
    "docker": {
        "command_prefix": ["docker", "exec", "rag-mcp"],
        "data_dir": "/app/data",
        "expected": True
    },
    "native": {
        "command_prefix": [],
        "data_dir": "/opt/synapse/data",
        "expected": True
    },
    "user_home": {
        "command_prefix": [],
        "data_dir": str(Path.home() / ".synapse" / "data"),
        "expected": False  # May not exist initially
    }
}

def run_command(
    command: List[str],
    timeout: int,
    check_exit_code: bool = True
) -> Tuple[int, str, str, float]:
    """
    Run command and return (exit_code, stdout, stderr, duration).
    
    Raises AssertionError if check_exit_code=True and exit_code != 0.
    """
    start_time = time.time()
    try:
        result = subprocess.run(
            command,
            timeout=timeout,
            capture_output=True,
            text=True,
            check=not check_exit_code
        )
        duration = time.time() - start_time
        return (result.returncode, result.stdout, result.stderr, duration)
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        return (-1, "", f"Command timed out after {timeout}s", duration)
    except Exception as e:
        duration = time.time() - start_time
        return (-1, "", str(e), duration)

def assert_success(
    test_name: str,
    exit_code: int,
    stdout: str,
    stderr: str,
    duration: float,
    timeout: int
) -> None:
    """Assert command succeeded (exit code 0, within timeout)."""
    # Assert exit code
    if exit_code != 0:
        raise AssertionError(
            f"{test_name}: FAILED - Exit code {exit_code}\n"
            f"STDOUT:\n{stdout}\n\n"
            f"STDERR:\n{stderr}"
        )
    
    # Assert timeout
    if duration > timeout:
        raise AssertionError(
            f"{test_name}: FAILED - Performance degradation\n"
            f"Duration: {duration:.2f}s (timeout: {timeout}s)"
        )
    
    print(f"✅ {test_name}: PASSED (duration: {duration:.2f}s)")

def main():
    """Main test execution."""
    global test_results
    
    print(f"\n{'='*60}")
    print(f"Phase 1 Test: P0-X <Command Name>")
    print(f"{'='*60}\n")
    
    try:
        # Run tests
        pass  # Test implementation goes here
        
    except AssertionError as e:
        print(f"\n❌ TEST FAILED:\n{e}\n")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR:\n{e}\n")
        sys.exit(2)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"Test Summary: {len(test_results)} tests, {sum(1 for r in test_results if r['passed'])} passed")
    print(f"{'='*60}\n")
    
    for result in test_results:
        status = "✅ PASS" if result['passed'] else "❌ FAIL"
        print(f"{status}: {result['name']} ({result['duration']:.2f}s)")
    
    # Exit with appropriate code
    failed_count = sum(1 for r in test_results if not r['passed'])
    if failed_count > 0:
        print(f"\n❌ {failed_count} test(s) failed")
        sys.exit(1)
    else:
        print(f"\n✅ All tests passed!")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Test Design: P0-1 (synapse setup)

### Test Setup-1: Auto-Detection (Docker)
**Description**: Verify setup auto-detects Docker data directory
**Environment**: Docker container
**Command**: `docker exec rag-mcp synapse setup --no-model-check`
**Assertions**:
- Exit code: 0
- Timeout: <60s
- Output contains: "Auto-detected Docker data directory: /app/data"
- Directory exists: `/app/data`
- Directory exists: `/app/data/models`
- Directory exists: `/app/data/rag_index`

### Test Setup-2: Auto-Detection (Native)
**Description**: Verify setup auto-detects native data directory
**Environment**: Native Linux
**Command**: `synapse setup --no-model-check` (from /opt/synapse)
**Assertions**:
- Exit code: 0
- Timeout: <60s
- Output contains: "Auto-detected native data directory: /opt/synapse/data"
- Directory exists: `/opt/synapse/data`
- Directory exists: `/opt/synapse/data/models`

### Test Setup-3: Auto-Detection (User Home)
**Description**: Verify setup auto-detects user home directory
**Environment**: User home
**Command**: `synapse setup --no-model-check` (from ~)
**Assertions**:
- Exit code: 0
- Timeout: <60s
- Output contains: "Auto-detected user home data directory"
- Directory exists: `~/.synapse/data`
- Directory exists: `~/.synapse/data/models`

### Test Setup-4: Force Re-Setup
**Description**: Verify `--force` flag works correctly
**Environment**: Native
**Command**: `synapse setup --force --no-model-check`
**Assertions**:
- Exit code: 0
- Timeout: <60s
- Output contains: "SYNAPSE setup complete!"
- Existing directories preserved (not deleted)

### Test Setup-5: Offline Mode
**Description**: Verify `--offline` flag skips model downloads
**Environment**: Native
**Command**: `synapse setup --offline --no-model-check`
**Assertions**:
- Exit code: 0
- Timeout: <60s
- Output contains: "offline mode (no model downloads)"
- No download prompts (non-interactive)

---

## Test Design: P0-2 (synapse config)

### Test Config-1: Basic Config Display (Docker)
**Description**: Verify config command displays configuration in Docker
**Environment**: Docker container
**Command**: `docker exec rag-mcp synapse config`
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Output contains: "Data directory:"
- Output contains: "Models directory:"
- Output contains: "RAG index directory:"

### Test Config-2: Verbose Mode (Docker)
**Description**: Verify `--verbose` flag displays detailed config
**Environment**: Docker container
**Command**: `docker exec rag-mcp synapse config --verbose`
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Output contains more details than non-verbose
- Output shows: "chunk_size"
- Output shows: "top_k"

### Test Config-3: Basic Config Display (Native)
**Description**: Verify config command works natively
**Environment**: Native Linux
**Command**: `synapse config`
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Output displays correct data directory: `/opt/synapse/data`
- Output displays correct models directory: `/opt/synapse/data/models`

### Test Config-4: Verbose Mode (Native)
**Description**: Verify verbose mode works natively
**Environment**: Native Linux
**Command**: `synapse config --verbose`
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Output shows all configuration values

---

## Test Design: P0-3 (synapse models list)

### Test Models-1: List Installed Models (Docker)
**Description**: Verify models list shows installed models in Docker
**Environment**: Docker container
**Command**: `docker exec rag-mcp synapse models list`
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Output contains: "embedding"
- Output contains: "bge-m3-q8_0.gguf" (if installed)
- Output shows model status: "installed" or "not installed"

### Test Models-2: List Installed Models (Native)
**Description**: Verify models list works natively
**Environment**: Native Linux
**Command**: `synapse models list`
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Output shows model file path
- Output shows model file size (if installed)
- Output is in readable format

### Test Models-3: Handle Missing Models
**Description**: Verify correct handling when models are missing
**Environment**: Clean environment (no models)
**Command**: `synapse models list` (after removing models)
**Assertions**:
- Exit code: 0 (command doesn't fail)
- Timeout: <2s
- Output shows: "not installed" for missing models
- Clear indication of missing required model

---

## Data Schemas

### Test Result Schema

Each test stores results in this format:

```python
{
    "test_id": "setup-1-docker",
    "name": "Setup-1: Auto-Detection (Docker)",
    "command": "synapse setup --no-model-check",
    "environment": "docker",
    "exit_code": 0,
    "stdout": "...",
    "stderr": "",
    "duration": 1.23,
    "timeout": 60,
    "passed": True,
    "timestamp": "2026-01-07T12:00:00Z",
    "assertions": [
        {"name": "exit_code", "expected": 0, "actual": 0, "passed": True},
        {"name": "timeout", "expected": "<60s", "actual": "1.23s", "passed": True},
        {"name": "output_contains", "expected": "Auto-detected Docker", "actual": True, "passed": True}
    ]
}
```

---

## Dependencies

### Python Dependencies
- `subprocess` - Command execution (built-in)
- `pathlib` - Path operations (built-in)
- `time` - Performance measurement (built-in)
- `json` - Result serialization (built-in)

### System Dependencies
- Docker (for Docker mode tests)
- Python 3.8+ (for test scripts)
- SYNAPSE CLI (must be installed or in PYTHONPATH)

### Test Data Dependencies
- Existing README.md (for context)
- Existing configs/rag_config.json (for validation)
- BGE-M3 model (optional, can test without)

---

## Risk Assessment

### Risk-1: Docker Container Not Running
**Likelihood**: Medium
**Impact**: Docker mode tests fail
**Mitigation**:
- Check container status before tests
- Skip Docker tests if container not running
- Document requirement clearly

### Risk-2: Permission Issues
**Likelihood**: Low
**Impact**: Directory creation fails
**Mitigation**:
- Run tests with appropriate permissions
- Test user home mode if native mode fails
- Clear error messages guide user

### Risk-3: Network Issues
**Likelihood**: Low (using --no-model-check)
**Impact**: Model download tests timeout
**Mitigation**:
- Use `--offline` flag for most tests
- Use `--no-model-check` to skip validation
- Set generous timeout (60s)

### Risk-4: Cross-Platform Differences
**Likelihood**: Medium
**Impact**: Tests pass on Linux, fail on macOS/Windows
**Mitigation**:
- Focus on Linux (primary platform)
- Document platform-specific behavior
- Test user home mode for cross-platform

---

## Success Criteria

Phase 1 is complete when:

1. **All P0-1 Tests Pass** (setup command)
   - 5/5 tests passing in Docker mode
   - 5/5 tests passing in native mode
   - 5/5 tests passing in user home mode

2. **All P0-2 Tests Pass** (config command)
   - 4/4 tests passing in Docker mode
   - 4/4 tests passing in native mode

3. **All P0-3 Tests Pass** (models list command)
   - 3/3 tests passing in Docker mode
   - 3/3 tests passing in native mode

4. **Total Test Success Rate**: 100% (24/24 tests)

5. **Performance Compliance**: 100% (all tests within timeouts)

6. **Test Documentation Created**: All test scripts and results documented

7. **Central Index Updated**: `docs/specs/index.md` shows Phase 1 as [Completed]

---

## Timeline

### Estimated Duration: 3-4 hours

**Breakdown:**
- Requirements.md: ✅ Complete (0.5 hrs)
- Plan.md: ✅ Complete (0.5 hrs) ← You are here
- Tasks.md: 0.5 hrs
- Test Scripts: 1.5 hrs
- Test Execution: 1.0 hrs
- Documentation: 0.5 hrs

**Total**: 4.5 hours

---

## Next Steps

After this plan is approved:

1. **Create Tasks.md** - Detailed checklist for Phase 1
2. **Implement Test Scripts** - Create `tests/cli/test_p0_*.py` files
3. **Execute Tests** - Run all 24 tests across 3 environments
4. **Document Results** - Record pass/fail + metrics
5. **Update Central Index** - Mark Phase 1 as [Completed]

---

**Created**: January 7, 2026
**Last Updated**: January 7, 2026
**Status**: Ready for Approval
