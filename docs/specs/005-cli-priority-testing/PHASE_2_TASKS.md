# Tasks: Phase 2 - Server Operations

**Feature ID**: 005-cli-priority-testing
**Phase**: 2 - Server Operations
**Priority**: P1 (Core Server)
**Created**: January 7, 2026

---

## Task Breakdown

This task list provides granular checklist for implementing and executing Phase 2 tests.

**ORDERING STRATEGY:**
1. Create test scripts for start, stop, status
2. Implement tests for each command
3. Execute tests interactively with user
4. Document results

---

## Phase 2.1: P1-1 Start Command Tests (14 tasks)

### 2.1.1 Create Test Script: P1-1 Start
- [x] Create `tests/cli/test_p1_start.py` file
- [x] Add imports (subprocess, sys, time, pathlib)
- [x] Define TIMEOUTS dictionary (start: 10s, health_check: 1s)
- [x] Define ENVIRONMENTS dictionary (docker_compose, native)
- [x] Implement test result storage
- [x] Add main() function
- [x] Add error handling
- [x] Add test summary output

### 2.1.2 Implement: Start-1 Docker Compose Start
- [x] Define test function `test_start_1_docker_compose()`
- [x] Implement command: `docker compose up -d rag-mcp`
- [x] Add assertion: exit_code == 0
- [x] Add assertion: timeout < 10s
- [x] Add assertion: container starts successfully
- [x] Add assertion: health check returns 200 OK
- [x] Add assertion: server runs in background
- [x] Record test result

### 2.1.3 Implement: Start-2 Native Start
- [x] Define test function `test_start_2_native()`
- [x] Implement command: `python3 -m synapse.cli.main start`
- [x] Add assertion: exit_code == 0 (background process)
- [x] Add assertion: timeout < 10s
- [x] Add assertion: process starts successfully
- [x] Add assertion: health check returns 200 OK
- [x] Add assertion: server runs in background
- [x] Record test result

### 2.1.4 Implement: Start-3 Port Configuration
- [x] Define test function `test_start_3_port_config()`
- [x] Implement command: `synapse start --port 9000`
- [x] Add assertion: exit_code == 0
- [x] Add assertion: server starts on port 9000
- [x] Add assertion: health check on port 9000 succeeds
- [x] Add assertion: configuration shows correct port
- [x] Record test result

### 2.1.5 Implement: Start-4 Port Already in Use
- [x] Define test function `test_start_4_port_in_use()`
- [x] Setup: Start server on port 8002, then attempt another start
- [x] Add assertion: exit_code == non-zero
- [x] Add assertion: error message mentions port conflict
- [x] Add assertion: error message is clear and actionable
- [x] Add assertion: server not corrupted
- [x] Record test result

### 2.1.6 Implement: Start-5 Missing Dependencies
- [x] Define test function `test_start_5_missing_deps()`
- [x] Setup: Mock missing dependency (e.g., delete required module temporarily)
- [x] Add assertion: exit_code == non-zero
- [x] Add assertion: error message mentions missing dependency
- [x] Add assertion: error message suggests installation
- [x] Add assertion: no partial startup
- [x] Restore dependency
- [x] Record test result

### 2.1.7 Implement: Start-6 Configuration Error
- [x] Define test function `test_start_6_config_error()`
- [x] Setup: Provide invalid configuration
- [x] Add assertion: exit_code == non-zero
- [x] Add assertion: error message mentions configuration issue
- [x] Add assertion: error message shows file/line of error
- [x] Add assertion: suggests fix
- [x] Restore valid configuration
- [x] Record test result

### 2.1.8 Implement: Start-7 Docker Mode Flag
- [x] Define test function `test_start_7_docker_mode()`
- [x] Implement command: `synapse start --docker`
- [x] Add assertion: exit_code == 0
- [x] Add assertion: Docker Compose is invoked
- [x] Add assertion: container starts via Docker Compose
- [x] Add assertion: not starting native process
- [x] Record test result

### 2.1.9 Add Health Check Utility
- [x] Add function to check health endpoint
- [x] Implement curl-based health check
- [x] Implement retry logic with backoff
- [x] Handle health check failures gracefully
- [x] Return health status and duration

### 2.1.10 Add Docker Compose Check
- [x] Add function to check Docker Compose version
- [x] Verify docker compose is available
- [x] Test v1 vs v2 syntax
- [x] Document version requirements

### 2.1.11 Add Background Process Management
- [x] Add function to verify process is background
- [x] Check for process detachment
- [x] Verify no blocking I/O
- [x] Test process cleanup

### 2.1.12 Add Startup Timeout Handling
- [x] Add try-except for startup timeouts
- [x] Use generous timeout (30s) for health checks
- [x] Log clear message if timeout
- [x] Cleanup on timeout

### 2.1.13 Verify Start Server Functionality
- [x] Verify server actually responds to requests
- [x] Verify MCP endpoints are available
- [x] Verify logging is working
- [x] Verify no errors in startup logs

### 2.1.14 Verify Test Script Completeness
- [x] Verify all test functions are defined
- [x] Verify all assertions are implemented
- [x] Verify error handling is comprehensive
- [x] Verify test summary is generated
- [x] Verify exit codes are correct

---

## Phase 2.2: P1-2 Stop Command Tests (12 tasks)

### 2.2.1 Create Test Script: P1-2 Stop
- [ ] Create `tests/cli/test_p1_stop.py` file
- [ ] Add imports and utility functions
- [ ] Define TIMEOUTs (stop: 5s)
- [ ] Implement main() function
- [ ] Add test summary output

### 2.2.2 Implement: Stop-1 Docker Compose Stop
- [ ] Define test function `test_stop_1_docker_compose()`
- [ ] Implement command: `docker compose down`
- [ ] Setup: Server must be running first
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 5s
- [ ] Add assertion: container stops gracefully
- [ ] Add assertion: no zombie processes
- [ ] Add assertion: all connections closed
- [ ] Record test result

### 2.2.3 Implement: Stop-2 Native Stop
- [ ] Define test function `test_stop_2_native()`
- [ ] Implement command: `synapse stop`
- [ ] Setup: Server must be running first
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 5s
- [ ] Add assertion: process stops gracefully
- [ ] Add assertion: no zombie processes
- [ ] Add assertion: health check fails (server down)
- [ ] Record test result

### 2.2.4 Implement: Stop-3 Server Not Running
- [ ] Define test function `test_stop_3_not_running()`
- [ ] Setup: Server not running
- [ ] Add assertion: exit_code == non-zero
- [ ] Add assertion: error message mentions server not running
- [ ] Add assertion: error message is clear
- [ ] Add assertion: no system corruption
- [ ] Record test result

### 2.2.5 Implement: Stop-4 Forced Stop
- [ ] Define test function `test_stop_4_forced()`
- [ ] Implement command: Force stop signal
- [ ] Setup: Server running with active connections
- [ ] Add assertion: exit_code == 0 or non-zero (per implementation)
- [ ] Add assertion: server stops immediately
- [ ] Add assertion: resources cleaned up
- [ ] Add assertion: no partial shutdown
- [ ] Record test result

### 2.2.6 Implement: Stop-5 Docker Volume Persistence
- [ ] Define test function `test_stop_5_volume_persistence()`
- [ ] Setup: Create data before stop, verify after start
- [ ] Implement start, write test data, stop, start
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: volumes are not deleted
- [ ] Add assertion: data persists across stop/start cycle
- [ ] Add assertion: models directory intact
- [ ] Record test result

### 2.2.7 Implement: Stop-6 Connection Cleanup
- [ ] Define test function `test_stop_6_connection_cleanup()`
- [ ] Setup: Simulate active connection, then stop
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: connections closed gracefully
- [ ] Add assertion: no connection errors in logs
- [ ] Add assertion: clean shutdown
- [ ] Record test result

### 2.2.8 Add Graceful Shutdown Verification
- [ ] Add function to verify graceful shutdown
- [ ] Check for SIGTERM handling
- [ ] Verify in-flight requests complete
- [ ] Verify resources released

### 2.2.9 Add Zombie Process Detection
- [ ] Add function to detect zombie processes
- [ ] Check with ps/pgrep after stop
- [ ] Verify no orphaned processes
- [ ] Force cleanup if needed

### 2.2.10 Add Server State Verification
- [ ] Add function to check server state
- [ ] Verify server is actually stopped
- [ ] Verify no process listening on port
- [ ] Verify no zombie processes

### 2.2.11 Add Cleanup on Failure
- [ ] Add cleanup for failed stop attempts
- [ ] Handle forced kill scenarios
- [ ] Log partial shutdown states
- [ ] Document cleanup steps

### 2.2.12 Verify Test Script Completeness
- [ ] Verify all test functions are defined
- [ ] Verify all assertions are implemented
- [ ] Verify cleanup functions work correctly
- [ ] Verify test summary is generated

---

## Phase 2.3: P1-3 Status Command Tests (14 tasks)

### 2.3.1 Create Test Script: P1-3 Status
- [ ] Create `tests/cli/test_p1_status.py` file
- [ ] Add imports and utility functions
- [ ] Define TIMEOUTs (status: 2s, health_check: 1s)
- [ ] Implement main() function
- [ ] Add test summary output

### 2.3.2 Implement: Status-1 Docker Compose Status (Running)
- [ ] Define test function `test_status_1_docker_running()`
- [ ] Implement command: `synapse status`
- [ ] Setup: Server running
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: status shows "running"
- [ ] Add assertion: status shows mode: "Docker"
- [ ] Add assertion: status shows correct port
- [ ] Record test result

### 2.3.3 Implement: Status-2 Docker Compose Status (Stopped)
- [ ] Define test function `test_status_2_docker_stopped()`
- [ ] Implement command: `synapse status`
- [ ] Setup: Server not running
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: status shows "stopped"
- [ ] Add assertion: status shows mode: "Docker"
- [ ] Add assertion: clear indication of stopped state
- [ ] Record test result

### 2.3.4 Implement: Status-3 Native Status (Running)
- [ ] Define test function `test_status_3_native_running()`
- [ ] Implement command: `synapse status`
- [ ] Setup: Server running
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: status shows "running"
- [ ] Add assertion: status shows mode: "Native"
- [ ] Add assertion: status shows correct port
- [ ] Record test result

### 2.3.5 Implement: Status-4 Native Status (Stopped)
- [ ] Define test function `test_status_4_native_stopped()`
- [ ] Implement command: `synapse status`
- [ ] Setup: Server not running
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: status shows "stopped"
- [ ] Add assertion: status shows mode: "Native"
- [ ] Add assertion: clear indication of stopped state
- [ ] Record test result

### 2.3.6 Implement: Status-5 Verbose Mode (Docker)
- [ ] Define test function `test_status_5_docker_verbose()`
- [ ] Implement command: `synapse status --verbose`
- [ ] Setup: Server running
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: output shows memory system health
- [ ] Add assertion: output shows connection statistics
- [ ] Add assertion: output shows performance metrics
- [ ] Add assertion: more details than non-verbose
- [ ] Record test result

### 2.3.7 Implement: Status-6 Verbose Mode (Native)
- [ ] Define test function `test_status_6_native_verbose()`
- [ ] Implement command: `synapse status --verbose`
- [ ] Setup: Server running
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: output shows memory system health
- [ ] Add assertion: output shows connection statistics
- [ ] Add assertion: output shows performance metrics
- [ ] Add assertion: more details than non-verbose
- [ ] Record test result

### 2.3.8 Implement: Status-7 Health Check Integration
- [ ] Define test function `test_status_7_health_check()`
- [ ] Implement command: `synapse status`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: health endpoint is queried
- [ ] Add assertion: health status is displayed
- [ ] Add assertion: mismatch is reported if health fails
- [ ] Add assertion: health endpoint URL is shown
- [ ] Record test result

### 2.3.9 Add Server State Detection
- [ ] Add function to detect server state
- [ ] Check for running process/container
- [ ] Verify server mode (Docker/Native)
- [ ] Verify server port

### 2.3.10 Add Memory System Health Check
- [ ] Add function to check memory system health
- [ ] Query MCP endpoint for status
- [ ] Check symbolic, episodic, semantic memory
- [ ] Display health status

### 2.3.11 Add Connection Statistics
- [ ] Add function to get connection statistics
- [ ] Query active connections
- [ ] Query request metrics
- [ ] Display statistics in verbose mode

### 2.3.12 Add Performance Metrics
- [ ] Add function to get performance metrics
- [ ] Query CPU/memory usage
- [ ] Query request/response times
- [ ] Display metrics in verbose mode

### 2.3.13 Add Status Accuracy Verification
- [ ] Add function to verify status accuracy
- [ ] Compare reported state with actual state
- [ ] Report mismatches
- [ ] Ensure status is truthful

### 2.3.14 Verify Test Script Completeness
- [ ] Verify all test functions are defined
- [ ] Verify all assertions are implemented
- [ ] Verify verbose mode works correctly
- [ ] Verify test summary is generated

---

## Phase 2.4: P1-4 Docker Integration Tests (8 tasks)

### 2.4.1 Create Test Script: P1-4 Docker Integration
- [ ] Create `tests/cli/test_p1_docker.py` file
- [ ] Add imports and utility functions
- [ ] Define TIMEOUTs (compose: 10s, stop: 5s, ps: 2s)
- [ ] Implement main() function
- [ ] Add test summary output

### 2.4.2 Implement: Docker-1 Docker Compose Up
- [ ] Define test function `test_docker_1_compose_up()`
- [ ] Implement command: `docker compose up -d rag-mcp`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 10s
- [ ] Add assertion: container starts successfully
- [ ] Add assertion: health checks configured
- [ ] Add assertion: environment variables loaded
- [ ] Record test result

### 2.4.3 Implement: Docker-2 Docker Compose Stop
- [ ] Define test function `test_docker_2_compose_stop()`
- [ ] Implement command: `docker compose down`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 5s
- [ ] Add assertion: container stops gracefully
- [ ] Add assertion: volumes preserved
- [ ] Add assertion: network cleaned up
- [ ] Record test result

### 2.4.4 Implement: Docker-3 Docker Compose Ps
- [ ] Define test function `test_docker_3_compose_ps()`
- [ ] Implement command: `docker compose ps`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: service status shown
- [ ] Add assertion: container status accurate
- [ ] Add assertion: port mappings shown
- [ ] Record test result

### 2.4.5 Implement: Docker-4 Docker Compose Logs
- [ ] Define test function `test_docker_4_compose_logs()`
- [ ] Implement command: `docker compose logs rag-mcp`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: logs are accessible
- [ ] Add assertion: logs show startup messages
- [ ] Add assertion: logs show errors (if any)
- [ ] Add assertion: logs are in readable format
- [ ] Record test result

### 2.4.6 Add Docker Compose Version Check
- [ ] Add function to check docker compose version
- [ ] Verify v2 syntax compatibility
- [ ] Document version requirements
- [ ] Test with available version

### 2.4.7 Add Volume Mount Verification
- [ ] Add function to verify volume mounts
- [ ] Check data directory is mounted
- [ ] Check models directory is mounted
- [ ] Check RAG index directory is mounted
- [ ] Verify persistence

### 2.4.8 Verify Test Script Completeness
- [ ] Verify all test functions are defined
- [ ] Verify all assertions are implemented
- [ ] Verify Docker Compose operations work
- [ ] Verify test summary is generated

---

## Phase 2.5: Test Execution (4 tasks)

### 2.5.1 Execute P1-1 Start Tests
- [ ] Run `python3 tests/cli/test_p1_start.py`
- [ ] Verify all 8 tests run in Docker Compose mode
- [ ] Verify all 8 tests run in native mode
- [ ] Record all test results (pass/fail)
- [ ] Record performance metrics
- [ ] Document any failures
- [ ] Interactive review with user

### 2.5.2 Execute P1-2 Stop Tests
- [ ] Run `python3 tests/cli/test_p1_stop.py`
- [ ] Verify all 7 tests run in Docker Compose mode
- [ ] Verify all 7 tests run in native mode
- [ ] Record all test results (pass/fail)
- [ ] Record performance metrics
- [ ] Document any failures
- [ ] Interative review with user

### 2.5.3 Execute P1-3 Status Tests
- [ ] Run `python3 tests/cli/test_p1_status.py`
- [ ] Verify all 8 tests run in Docker Compose mode
- [ ] Verify all 8 tests run in native mode
- [ ] Record all test results (pass/fail)
- [ ] Record performance metrics
- [ ] Document any failures
- [ ] Interative review with user

### 2.5.4 Execute P1-4 Docker Integration Tests
- [ ] Run `python3 tests/cli/test_p1_docker.py`
- [ ] Verify all 5 tests run in Docker Compose mode
- [ ] Record all test results (pass/fail)
- [ ] Record performance metrics
- [ ] Document any failures
- [ ] Interative review with user

### 2.5.5 Verify All Tests Passed
- [ ] Verify total test count: 31 tests
- [ ] Verify pass count: 31 tests
- [ ] Verify fail count: 0 tests
- [ ] Verify performance compliance: 100%
- [ ] Verify error handling: 100%
- [ ] Calculate overall success rate

---

## Phase 2.6: Documentation & Completion (3 tasks)

### 2.6.1 Create Test Results Document
- [ ] Create `docs/specs/005-cli-priority-testing/PHASE_2_RESULTS.md`
- [ ] Document all 31 test results
- [ ] Document pass/fail status for each test
- [ ] Document performance metrics
- [ ] Document any errors or issues
- [ ] Calculate overall success rate

### 2.6.2 Update Central Index
- [ ] Update `docs/specs/index.md` with feature 005 entry
- [ ] Set Phase 2 status to "[Completed]"
- [ ] Add completion date
- [ ] Add final commit hash
- [ ] Update overall progress

### 2.6.3 Mark Tasks Complete
- [ ] Mark all Phase 2.1 tasks as complete
- [ ] Mark all Phase 2.2 tasks as complete
- [ ] Mark all Phase 2.3 tasks as complete
- [ ] Mark all Phase 2.4 tasks as complete
- [ ] Mark all Phase 2.5 tasks as complete
- [ ] Mark all Phase 2.6 tasks as complete
- [ ] Update tasks.md with final commit hash

---

## Task Statistics

- **Total Tasks**: 58 tasks
- **Total Phases**: 6
- **Estimated Time**: 2-3 hours

**Task Breakdown by Phase:**
- Phase 2.1: P1-1 Start Tests (14 tasks)
- Phase 2.2: P1-2 Stop Tests (12 tasks)
- Phase 2.3: P1-3 Status Tests (14 tasks)
- Phase 2.4: P1-4 Docker Integration (8 tasks)
- Phase 2.5: Test Execution (5 tasks)
- Phase 2.6: Documentation (3 tasks)

---

## Test Coverage

**Total Tests**: 31 tests
- P1-1 (start): 8 tests × 2 environments = 16 tests
- P1-2 (stop): 7 tests × 2 environments = 14 tests
- P1-3 (status): 8 tests × 2 environments = 16 tests
- P1-4 (docker): 5 tests × 1 environment = 5 tests
  - **Note**: Some tests may overlap, actual total may vary

**Coverage Metrics**:
- Functional requirements: 100% (all FRs tested)
- Non-functional requirements: 100% (performance, error handling, UX tested)
- Error scenarios: 100% (all error paths tested)
- Docker integration: 100% (docker compose operations tested)

---

## Notes

**TESTING APPROACH (User Decisions):**
- Environments: Test Docker Compose and Native modes
- Error Testing: Test ALL error scenarios
- Destructive Testing: Full destructive tests (actually start/stop servers)
- Docker Integration: Use Docker Compose for server management
- Planning: Full SDD protocol (requirements, plan, tasks)

**READY TO START**: Phase 2.1 - P1-1 Start Command Tests

---

## Completion Checklist

Phase 2 is complete when:
- [ ] All 58 tasks marked as complete
- [ ] All 31 tests passing
- [ ] Performance compliance: 100%
- [ ] Test results documented
- [ ] Central index updated
- [ ] All changes committed to git
- [ ] Final commit hash added to tasks.md

---

**Last Updated**: January 7, 2026
**Phase 2.1 Status**: ✅ COMPLETE (14/14 tasks, test_p1_start.py created, commit: b77c029)
**Next Phase**: Phase 2.2 - Stop Command Tests
