# Phase 2 Plan: Server Operations Testing

**Feature ID**: 005-cli-priority-testing
**Phase**: 2 - Server Operations
**Priority**: P1 (Core Server)
**Status**: Planning

---

## Overview

This plan details the testing strategy for P1 (Core Server) commands: `synapse start`, `synapse stop`, and `synapse status`. These commands manage the MCP server lifecycle and are critical for SYNAPSE operation.

---

## Testing Strategy

### Approach: Interactive Testing with Docker Compose

Based on user requirements, we'll use:
- **Test Scripts**: Python scripts with built-in assertions
- **Docker Compose**: Use docker compose for start/stop operations
- **Interactive Execution**: Run tests step-by-step with user verification
- **Full Error Coverage**: Test all error scenarios
- **Destructive Testing**: Full destructive tests (actually start/stop servers)

**Why Interactive Testing?**
- User wants to verify each phase before moving to next
- Allows catching issues early
- Provides confidence in each test phase

**Why Docker Compose?**
- Production deployment method
- Easier to test start/stop cycles
- Clean environment isolation

**Why Full Error & Destructive Testing?**
- User explicitly requested full error scenario testing
- User explicitly requested full destructive testing
- Validates robustness completely

### Test Environments: Docker Compose & Native (Option 3-A)

Per user choice (Option 3-A), we'll test both environments:
1. **Docker Compose Mode**: Using `docker compose` up/down
2. **Native Mode**: Direct Python process execution

**Order of Testing**:
1. Docker Compose mode (production environment)
2. Native mode (alternative deployment)

---

## Architecture & Design

### Test Script Structure

```
tests/cli/
├── conftest.py              # Common test fixtures and utilities
├── test_p1_start.py         # P1-1: synapse start tests
├── test_p1_stop.py          # P1-2: synapse stop tests
└── test_p1_status.py        # P1-3: synapse status tests
```

### Test Script Template

Each test script follows this pattern:

```python
#!/usr/bin/env python3
"""
Phase 2 Test: P1-X <Command Name>

Tests <command> using Docker Compose and native modes.
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
    "start": 10,      # seconds (server startup)
    "stop": 5,        # seconds (graceful shutdown)
    "status": 2,       # seconds (status check)
    "health_check": 1   # seconds (health endpoint response)
}

# Environments to test
ENVIRONMENTS = {
    "docker_compose": {
        "name": "Docker Compose",
        "start_command": ["docker", "compose", "up", "-d", "rag-mcp"],
        "stop_command": ["docker", "compose", "down"],
        "health_url": "http://localhost:8002/health",
        "expected": True
    },
    "native": {
        "name": "Native",
        "start_command": ["python3", "-m", "mcp_server.rag_server"],
        "stop_command": ["pkill", "-f", "rag_server.py"],
        "health_url": "http://localhost:8002/health",
        "expected": True
    }
}


def run_command(
    command: List[str],
    timeout: int,
    check_exit_code: bool = True
) -> Tuple[int, str, str, float]:
    """
    Run command and return (exit_code, stdout, stderr, duration).
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


def check_health_check(url: str, timeout: int = 1) -> Tuple[int, str, str, float]:
    """
    Check health endpoint and return (exit_code, stdout, stderr, duration).
    """
    cmd = ["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", url]
    return run_command(cmd, timeout, check_exit_code=False)


def assert_success(
    test_name: str,
    exit_code: int,
    stdout: str,
    stderr: str,
    duration: float,
    timeout: int
) -> None:
    """Assert command succeeded."""
    if exit_code != 0:
        raise AssertionError(
            f"{test_name}: FAILED - Exit code {exit_code}\n"
            f"STDOUT:\n{stdout}\n\n"
            f"STDERR:\n{stderr}"
        )
    if duration > timeout:
        raise AssertionError(
            f"{test_name}: FAILED - Performance degradation\n"
            f"Duration: {duration:.2f}s (timeout: {timeout}s)"
        )
    print(f"✅ {test_name}: PASSED (duration: {duration:.2f}s)")


def record_test_result(
    test_id: str,
    name: str,
    command: str,
    environment: str,
    exit_code: int,
    stdout: str,
    stderr: str,
    duration: float,
    timeout: int,
    passed: bool,
    assertions: List[Dict[str, any]] = None
) -> None:
    """Record test result for later summary."""
    global test_results

    from datetime import datetime

    test_result = {
        "test_id": test_id,
        "name": name,
        "command": command,
        "environment": environment,
        "exit_code": exit_code,
        "stdout": stdout,
        "stderr": stderr,
        "duration": duration,
        "timeout": timeout,
        "passed": passed,
        "timestamp": datetime.now().isoformat(),
        "assertions": assertions or []
    }
    test_results.append(test_result)


def print_test_summary() -> None:
    """Print summary of all test results."""
    global test_results

    print(f"\n{'=' * 60}")
    print(f"Phase 2 Test Summary")
    print(f"{'=' * 60}")
    print(f"\nTotal tests: {len(test_results)}")
    print(f"Passed: {sum(1 for r in test_results if r['passed'])}")
    print(f"Failed: {sum(1 for r in test_results if not r['passed'])}")
    print(f"Success rate: {sum(1 for r in test_results if r['passed']) / len(test_results) * 100:.1f}%")

    for result in test_results:
        status = "✅ PASS" if result['passed'] else "❌ FAIL"
        print(f"{status}: {result['name']} ({result['duration']:.2f}s, env: {result['environment']})")

    print(f"{'-' * 60}\n")


def main():
    """Main test execution."""
    global test_results

    print(f"\n{'=' * 60}")
    print(f"Phase 2 Test: P1-X <Command Name>")
    print(f"{'=' * 60}\n")

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
    print_test_summary()

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

## Test Design: P1-1 (synapse start)

### Test Start-1: Docker Compose Start
**Description**: Verify start command starts Docker container via docker compose
**Environment**: Docker Compose
**Command**: `docker compose up -d rag-mcp`
**Assertions**:
- Exit code: 0
- Timeout: <10s
- Container starts successfully
- Health check returns 200 OK
- Server runs in background

### Test Start-2: Native Start
**Description**: Verify start command starts native Python process
**Environment**: Native
**Command**: `python3 -m mcp_server.rag_server`
**Assertions**:
- Exit code: 0 (background process)
- Timeout: <10s
- Process starts successfully
- Health check returns 200 OK
- Server runs in background

### Test Start-3: Port Configuration
**Description**: Verify --port flag works correctly
**Environment**: Native
**Command**: `synapse start --port 9000`
**Assertions**:
- Exit code: 0
- Server starts on port 9000
- Health check on port 9000 succeeds
- Configuration shows correct port

### Test Start-4: Port Already in Use
**Description**: Verify error handling when port is occupied
**Environment**: Native
**Setup**: Start server on port 8002, then attempt another start
**Assertions**:
- Exit code: non-zero
- Error message mentions port conflict
- Error message is clear and actionable
- Server not corrupted

### Test Start-5: Missing Dependencies
**Description**: Verify error handling when dependencies missing
**Environment**: Native
**Setup**: Mock missing dependency (e.g., delete required module)
**Assertions**:
- Exit code: non-zero
- Error message mentions missing dependency
- Error message suggests installation
- No partial startup

### Test Start-6: Configuration Error
**Description**: Verify error handling with invalid config
**Environment**: Native
**Setup**: Provide invalid configuration
**Assertions**:
- Exit code: non-zero
- Error message mentions configuration issue
- Error message shows file/line of error
- Suggests fix

### Test Start-7: Docker Mode Flag
**Description**: Verify --docker flag uses Docker Compose
**Environment**: Native (with --docker flag)
**Command**: `synapse start --docker`
**Assertions**:
- Exit code: 0
- Docker Compose is invoked
- Container starts via Docker Compose
- Not starting native process

---

## Test Design: P1-2 (synapse stop)

### Test Stop-1: Docker Compose Stop
**Description**: Verify stop command stops Docker container via docker compose
**Environment**: Docker Compose
**Command**: `docker compose down`
**Setup**: Server must be running first
**Assertions**:
- Exit code: 0
- Timeout: <5s
- Container stops gracefully
- No zombie processes
- All connections closed

### Test Stop-2: Native Stop
**Description**: Verify stop command stops native Python process
**Environment**: Native
**Command**: `synapse stop`
**Setup**: Server must be running first
**Assertions**:
- Exit code: 0
- Timeout: <5s
- Process stops gracefully
- No zombie processes
- Health check fails (server down)

### Test Stop-3: Server Not Running
**Description**: Verify graceful handling when server not running
**Environment**: Native
**Setup**: Server not running
**Assertions**:
- Exit code: non-zero
- Error message mentions server not running
- Error message is clear
- No system corruption

### Test Stop-4: Forced Stop
**Description**: Verify forced stop behavior
**Environment**: Native
**Command**: Force stop signal
**Assertions**:
- Exit code: 0 or non-zero (per implementation)
- Server stops immediately
- Resources cleaned up
- No partial shutdown

### Test Stop-5: Docker Volume Persistence
**Description**: Verify Docker volumes persist after stop
**Environment**: Docker Compose
**Setup**: Create data before stop, verify after start
**Assertions**:
- Exit code: 0
- Volumes are not deleted
- Data persists across stop/start cycle
- Models directory intact

### Test Stop-6: Connection Cleanup
**Description**: Verify all connections are closed properly
**Environment**: Native
**Setup**: Simulate active connection, then stop
**Assertions**:
- Exit code: 0
- Connections closed gracefully
- No connection errors in logs
- Clean shutdown

---

## Test Design: P1-3 (synapse status)

### Test Status-1: Docker Compose Status (Running)
**Description**: Verify status shows Docker container as running
**Environment**: Docker Compose
**Command**: `synapse status`
**Setup**: Server running
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Status shows "running"
- Status shows mode: "Docker"
- Status shows correct port

### Test Status-2: Docker Compose Status (Stopped)
**Description**: Verify status shows Docker container as stopped
**Environment**: Docker Compose
**Command**: `synapse status`
**Setup**: Server not running
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Status shows "stopped"
- Status shows mode: "Docker"
- Clear indication of stopped state

### Test Status-3: Native Status (Running)
**Description**: Verify status shows native process as running
**Environment**: Native
**Command**: `synapse status`
**Setup**: Server running
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Status shows "running"
- Status shows mode: "Native"
- Status shows correct port

### Test Status-4: Native Status (Stopped)
**Description**: Verify status shows native process as stopped
**Environment**: Native
**Command**: `synapse status`
**Setup**: Server not running
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Status shows "stopped"
- Status shows mode: "Native"
- Clear indication of stopped state

### Test Status-5: Verbose Mode (Docker)
**Description**: Verify --verbose shows detailed Docker status
**Environment**: Docker Compose
**Command**: `synapse status --verbose`
**Setup**: Server running
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Output shows memory system health
- Output shows connection statistics
- Output shows performance metrics
- More details than non-verbose

### Test Status-6: Verbose Mode (Native)
**Description**: Verify --verbose shows detailed native status
**Environment**: Native
**Command**: `synapse status --verbose`
**Setup**: Server running
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Output shows memory system health
- Output shows connection statistics
- Output shows performance metrics
- More details than non-verbose

### Test Status-7: Health Check Integration
**Description**: Verify status command queries health endpoint
**Environment**: Native
**Command**: `synapse status`
**Assertions**:
- Exit code: 0
- Health endpoint is queried
- Health status is displayed
- Mismatch is reported if health fails
- Health endpoint URL is shown

---

## Test Design: P1-4 (Docker Integration)

### Test Docker-1: Docker Compose Up
**Description**: Verify docker compose up starts service correctly
**Environment**: Docker Compose
**Command**: `docker compose up -d rag-mcp`
**Assertions**:
- Exit code: 0
- Timeout: <10s
- Container starts successfully
- Health checks configured
- Environment variables loaded

### Test Docker-2: Docker Compose Stop
**Description**: Verify docker compose down stops service correctly
**Environment**: Docker Compose
**Command**: `docker compose down`
**Assertions**:
- Exit code: 0
- Timeout: <5s
- Container stops gracefully
- Volumes preserved
- Network cleaned up

### Test Docker-3: Docker Compose Ps
**Description**: Verify docker compose ps shows service status
**Environment**: Docker Compose
**Command**: `docker compose ps`
**Assertions**:
- Exit code: 0
- Timeout: <2s
- Service status shown
- Container status accurate
- Port mappings shown

### Test Docker-4: Docker Compose Logs
**Description**: Verify docker compose logs show service logs
**Environment**: Docker Compose
**Command**: `docker compose logs rag-mcp`
**Assertions**:
- Exit code: 0
- Logs are accessible
- Logs show startup messages
- Logs show errors (if any)
- Logs are in readable format

---

## Data Schemas

### Test Result Schema

Each test stores results in this format:

```python
{
    "test_id": "start-1-docker",
    "name": "Start-1: Docker Compose Start",
    "command": "docker compose up -d rag-mcp",
    "environment": "docker_compose",
    "exit_code": 0,
    "stdout": "...",
    "stderr": "",
    "duration": 5.23,
    "timeout": 10,
    "passed": True,
    "timestamp": "2026-01-07T15:00:00Z",
    "assertions": [
        {"name": "exit_code", "expected": 0, "actual": 0, "passed": True},
        {"name": "timeout", "expected": "<10s", "actual": "5.23s", "passed": True},
        {"name": "health_check", "expected": 200, "actual": 200, "passed": True}
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
- Docker and Docker Compose (v2+)
- curl or httpx (for health check)
- Python 3.8+ (for native mode)

### Test Data Dependencies
- docker-compose.mcp.yml (Docker compose configuration)
- MCP server implementation
- Server configuration files

---

## Risk Assessment

### Risk-1: Port Conflicts During Testing
**Likelihood**: High
**Impact**: Start tests fail if port 8002 already in use
**Mitigation**:
- Always stop existing server before start tests
- Use alternative port for port conflict test
- Document port usage in test

### Risk-2: Docker Compose Version Issues
**Likelihood**: Medium
**Impact**: Docker compose v1 vs v2 syntax causes failures
**Mitigation**:
- Check docker compose version before tests
- Use v2 syntax (current standard)
- Test with both v1 and v2 if needed

### Risk-3: Zombie Processes
**Likelihood**: Medium
**Impact**: Processes not cleaned up properly
**Mitigation**:
- Test process cleanup after each stop
- Verify no zombie processes with ps/pkill
- Force cleanup if needed

### Risk-4: Destructive Testing Side Effects
**Likelihood**: High
**Impact**: Stopping server affects other operations/tests
**Mitigation**:
- Isolate each test (start fresh server)
- Always restart server after stop tests
- Clean up state between tests

### Risk-5: Health Check Timing Issues
**Likelihood**: Medium
**Impact**: Race conditions during startup
**Mitigation**:
- Add delays before health checks
- Retry health checks with backoff
- Use generous timeout (30s for startup)

---

## Success Criteria

Phase 2 is complete when:

1. **All P1-1 Tests Pass** (start command)
   - 7/7 tests passing in Docker Compose mode
   - 7/7 tests passing in native mode

2. **All P1-2 Tests Pass** (stop command)
   - 6/6 tests passing in Docker Compose mode
   - 6/6 tests passing in native mode

3. **All P1-3 Tests Pass** (status command)
   - 7/7 tests passing in Docker Compose mode
   - 7/7 tests passing in native mode

4. **All P1-4 Tests Pass** (docker integration)
   - 4/4 tests passing in Docker Compose mode

5. **Total Test Success Rate**: 100% (31/31 tests)

6. **Performance Compliance**: 100% (all tests within timeouts)

7. **Test Documentation Created**: All test scripts and results documented

8. **Central Index Updated**: `docs/specs/index.md` shows Phase 2 as [Completed]

---

## Timeline

### Estimated Duration: 2-3 hours

**Breakdown**:
- PHASE_2_REQUIREMENTS.md: ✅ Complete (0.5 hrs)
- PHASE_2_PLAN.md: ✅ Complete (0.5 hrs) ← You are here
- PHASE_2_TASKS.md: 0.5 hrs
- Test Scripts: 1.0 hrs
- Test Execution: 0.5 hrs
- Documentation: 0.5 hrs

**Total**: 3.0 hours

---

## Next Steps

After this plan is approved:

1. **Create Tasks.md** - Detailed checklist for Phase 2
2. **Implement Test Scripts** - Create `tests/cli/test_p1_*.py` files
3. **Execute Tests** - Run all 31 tests interactively
4. **Document Results** - Record pass/fail + metrics
5. **Update Central Index** - Mark Phase 2 as [Completed]

---

**Created**: January 7, 2026
**Last Updated**: January 7, 2026
**Status**: Ready for Approval
