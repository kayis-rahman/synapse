# Phase 2 Requirements: Server Operations

**Feature ID**: 005-cli-priority-testing
**Phase**: 2 - Server Operations
**Priority**: P1 (Core Server)
**Status**: In Progress

---

## Overview

This phase validates server operations that manage the SYNAPSE MCP server lifecycle. These commands are critical for running and managing the SYNAPSE service.

---

## User Stories

### US-1: Server Startup
**As a** system administrator,
**I want** to run `synapse start` to launch the MCP server,
**So that** SYNAPSE is available for queries and operations.

**Acceptance Criteria:**
- Start command launches server in Docker or native mode
- Server starts within reasonable time (<10s)
- Server runs in background (non-blocking)
- Server responds to health check endpoint
- Command returns to shell after server starts

### US-2: Server Shutdown
**As a** system administrator,
**I want** to run `synapse stop` to gracefully stop the MCP server,
**So that** I can safely shut down SYNAPSE without data loss.

**Acceptance Criteria:**
- Stop command stops running server
- Server shuts down gracefully (no errors)
- All connections closed properly
- Command confirms server stopped
- Server processes cleaned up

### US-3: Server Status
**As a** system administrator,
**I want** to run `synapse status` to check server health,
**So that** I can verify SYNAPSE is running correctly.

**Acceptance Criteria:**
- Status command shows current server state (running/stopped)
- Status shows server mode (Docker/Native)
- Status shows server port and endpoint
- Status shows memory systems health
- Status is accurate (matches actual server state)

### US-4: Docker Integration
**As a** DevOps engineer,
**I want** to use docker compose for server management,
**So that** SYNAPSE integrates cleanly with Docker infrastructure.

**Acceptance Criteria:**
- Docker compose starts rag-mcp container
- Docker compose stops rag-mcp container cleanly
- Container persists data volumes
- Health checks work in Docker
- Environment variables are properly configured

---

## Functional Requirements

### FR-1: Start Command (P1-1)
The `synapse start` command must:

**FR-1.1 Mode Selection**
- Support `--docker` flag for Docker mode
- Support `--native` flag for native mode (default)
- Auto-detect mode if not specified
- Validate mode is available

**FR-1.2 Background Execution**
- Start server in background process
- Return control to shell after startup
- Show startup progress messages
- Indicate successful start

**FR-1.3 Health Check**
- Start health check endpoint (default: http://localhost:8002/health)
- Health endpoint returns 200 OK when server ready
- Wait for health check before returning success
- Timeout after 30s if health check fails

**FR-1.4 Port Configuration**
- Use port from config (default: 8002)
- Support `--port` flag to override port
- Validate port is available
- Show port in startup messages

**FR-1.5 Error Handling**
- Handle port already in use gracefully
- Handle missing dependencies with clear message
- Handle configuration errors gracefully
- Show actionable error messages

**FR-1.6 Docker Compose Integration**
- Use docker compose for Docker mode
- Respect docker-compose.mcp.yml configuration
- Mount data volumes correctly
- Use environment variables from compose file

### FR-2: Stop Command (P1-2)
The `synapse stop` command must:

**FR-2.1 Server Detection**
- Auto-detect running server (Docker or native)
- Check if server is running before attempting stop
- Handle no-server-running case gracefully

**FR-2.2 Graceful Shutdown**
- Send graceful shutdown signal
- Wait for in-flight requests to complete
- Close all connections properly
- Clean up resources

**FR-2.3 Confirmation**
- Confirm server stopped successfully
- Show shutdown completion message
- Return exit code 0 on success
- Return non-zero on failure

**FR-2.4 Docker Compose Integration**
- Use docker compose stop for Docker mode
- Gracefully stop container (not kill)
- Preserve container state
- Keep volumes intact

**FR-2.5 Error Handling**
- Handle server not running gracefully
- Handle forced kill scenarios
- Handle permission errors
- Show clear error messages

### FR-3: Status Command (P1-3)
The `synapse status` command must:

**FR-3.1 Server State Detection**
- Detect if server is running
- Detect server mode (Docker/Native)
- Detect server port and host
- Detect server uptime (if running)

**FR-3.2 Health Check**
- Query health check endpoint
- Verify server is responsive
- Check memory systems (symbolic, episodic, semantic)
- Show health status

**FR-3.3 Configuration Display**
- Show current configuration
- Show data directory paths
- Show model availability
- Show server endpoints

**FR-3.4 Verbose Mode**
- Support `--verbose` flag for detailed status
- Show all memory system details
- Show connection statistics
- Show performance metrics

**FR-3.5 Error Handling**
- Handle server not running gracefully
- Handle health check failures gracefully
- Handle connection errors
- Show informative status

### FR-4: Docker Mode (P1-4)
The Docker mode integration must:

**FR-4.1 Docker Compose Support**
- Use docker compose up for start
- Use docker compose stop for stop
- Use docker compose ps for status
- Use docker compose logs for logs

**FR-4.2 Container Management**
- Start rag-mcp container correctly
- Stop rag-mcp container gracefully
- Restart container if needed
- Show container logs on errors

**FR-4.3 Volume Persistence**
- Mount data volumes from host
- Persist data across container restarts
- Preserve models directory
- Preserve RAG index directory

**FR-4.4 Environment Configuration**
- Use environment variables from compose file
- Pass MCP endpoint configuration
- Configure logging levels
- Set resource limits

**FR-4.5 Health Checks**
- Implement health check in docker-compose.yml
- Configure healthcheck interval and timeout
- Configure restart policy
- Show health status in docker ps

---

## Non-Functional Requirements

### NFR-1: Performance
- Start command completes within 10s (background process)
- Stop command completes within 5s (graceful shutdown)
- Status command completes within 2s
- Health check responds within 1s

### NFR-2: Reliability
- Server starts successfully 100% of time (with valid config)
- Server stops gracefully 100% of time
- Status command is accurate 100% of time
- No zombie processes after stop

### NFR-3: Error Handling
- All error scenarios produce clear messages
- No silent failures
- All commands return appropriate exit codes
- Errors suggest remediation steps

### NFR-4: User Experience
- Show progress indicators for long operations (startup)
- Use consistent output formatting
- Support `--quiet` mode for automated scripts
- Provide helpful tips in error messages

### NFR-5: Cross-Platform
- Work with docker compose v2
- Work with Docker desktop (Linux, macOS, Windows)
- Work with docker compose standalone (Linux)
- Work with systemd integration (native mode)

---

## Test Environments

### TE-1: Docker Compose Mode
- Target: Docker compose service (rag-mcp)
- Method: docker compose up/down/stop
- Data directory: /opt/synapse/data (mounted volume)
- Health check: http://localhost:8002/health

### TE-2: Native Mode
- Target: Native Linux process
- Method: Direct Python process execution
- Data directory: /opt/synapse/data
- Health check: http://localhost:8002/health

---

## Exit Criteria

Phase 2 is complete when ALL of the following are met:

1. **Start Command (P1-1)**
   - [ ] Start works in Docker compose mode
   - [ ] Start works in native mode
   - [ ] Server starts in background
   - [ ] Health check returns 200 OK
   - [ ] Port configuration works
   - [ ] Error handling tested (port in use, missing config)

2. **Stop Command (P1-2)**
   - [ ] Stop works in Docker compose mode
   - [ ] Stop works in native mode
   - [ ] Graceful shutdown verified
   - [ ] No zombie processes
   - [ ] Error handling tested (server not running)

3. **Status Command (P1-3)**
   - [ ] Status works in Docker compose mode
   - [ ] Status works in native mode
   - [ ] Accurate server state detection
   - [ ] Health check integration works
   - [ ] Verbose mode works
   - [ ] Error handling tested (server not running)

4. **Docker Integration (P1-4)**
   - [ ] Docker compose start works
   - [ ] Docker compose stop works
   - [ ] Volume persistence verified
   - [ ] Health checks configured
   - [ ] Environment variables work

5. **Error Handling (All Error Scenarios)**
   - [ ] Port already in use handled
   - [ ] Missing dependencies handled
   - [ ] Configuration errors handled
   - [ ] Server not running handled
   - [ ] Permission errors handled
   - [ ] Network errors handled

6. **Test Artifacts**
   - [ ] Semi-automated test scripts created
   - [ ] Test results documented (pass/fail + metrics)
   - [ ] All tests passing
   - [ ] Central index.md updated with Phase 2 completion

---

## Risks & Mitigations

### Risk-1: Port Conflicts
**Risk**: Port 8002 already in use by another process
**Mitigation**:
- Test port detection logic
- Test error message clarity
- Test alternative port flag

### Risk-2: Docker Compose Version
**Risk**: Docker compose v1 vs v2 syntax differences
**Mitigation**:
- Test with docker compose v2 (current standard)
- Check docker compose version in tests
- Document version requirements

### Risk-3: Background Process Management
**Risk**: Server doesn't detach properly or becomes zombie
**Mitigation**:
- Test proper daemonization
- Test process cleanup
- Verify no zombie processes after stop

### Risk-4: Health Check Timing
**Risk**: Health check timeout or race condition during startup
**Mitigation**:
- Test with different startup delays
- Test health check retry logic
- Test timeout handling

### Risk-5: Destructive Testing
**Risk**: Stopping server affects other operations or tests
**Mitigation**:
- Use isolated test environment
- Always restart server after stop tests
- Clean up state before each test

---

## Dependencies

**External Dependencies**:
- Docker and Docker Compose (for Docker mode tests)
- curl or httpx (for health check queries)
- Python 3.8+ (for native mode)

**Internal Dependencies**:
- Phase 1 tests complete (setup, config, models validated)
- MCP server implementation working
- Configuration management functional

---

## Success Metrics

- **Start Success Rate**: 100% (2/2 modes)
- **Stop Success Rate**: 100% (2/2 modes)
- **Status Success Rate**: 100% (2/2 modes)
- **Performance Compliance**: 100% (all commands under time limits)
- **Error Handling**: 100% (all error scenarios tested)
- **Docker Integration**: 100% (docker compose operations work)

---

## Related Documentation

- `AGENTS.md` - Spec-Driven Development (SDD) Protocol
- `docker-compose.mcp.yml` - Docker compose configuration
- `mcp_server/rag_server.py` - MCP server implementation
- `synapse/cli/commands/start.py` - Start command implementation
- `synapse/cli/commands/stop.py` - Stop command implementation
- `synapse/cli/commands/status.py` - Status command implementation

---

**Created**: January 7, 2026
**Last Updated**: January 7, 2026
