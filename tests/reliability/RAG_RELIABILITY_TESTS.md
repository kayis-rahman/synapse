# RAG Reliability & Failure-Mode Tests - Implementation Plan

**Status**: 🟡 IN PROGRESS
**Date**: 2025-12-29
**Project**: pi-rag (MCP-based Agentic RAG)
**Environment**: ARM/Raspberry Pi, Docker, GLM-4.7B, opencode CLI

---

## Executive Summary

This document defines comprehensive end-to-end reliability and failure-mode tests for the production MCP-based Agentic RAG system. Tests validate that the system behaves predictably, safely, and correctly when faced with real-world failures.

## Test Philosophy

**CRITICAL PRINCIPLES**:
1. **No Mocking Storage**: Use real Docker containers, real volumes, real MCP invocations
2. **Production-Realistic**: Test on actual ARM/Raspberry Pi with real model loading
3. **Containment First**: Prove failures don't cross project boundaries
4. **Observability-Driven**: All tests validate via metrics + logs, not assertions
5. **Hard Gates**: System is not production-ready if any test fails

---

## Test Architecture

### Component Diagram

```
┌─────────────────────────────────────────────────────┐
│              Test Orchestration Scripts             │
│  (Python, shell, docker SDK)                │
└──────────────────────┬──────────────────────────┘
                       │
        ┌──────────────▼──────────────┐
        │      Docker Compose         │
        │  (test environment)        │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   RAG MCP Container          │
        │  + Memory Volumes             │
        │  + Metrics Collection          │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   Test Harness (Python)       │
        │   - MCP Client               │
        │   - Metrics Parser            │
        │   - Assertions               │
        └──────────────┬──────────────┘
                       │
        ┌──────────────▼──────────────┐
        │   Observability Layer         │
        │   - Metrics API              │
        │   - Log Collection           │
        │   - Failure Detection          │
        └───────────────────────────────────┘
```

---

## Test Environment Setup

### Directory Structure

```
tests/
├── reliability/
│   ├── __init__.py
│   ├── test_plan.py           # Test orchestrator
│   ├── docker_orchestrate.py   # Docker management
│   ├── mcp_harness.py        # MCP client wrapper
│   ├── observability.py       # Metrics + logs
│   └── categories/
│       ├── test_crash.py         # Category 1
│       ├── test_disk.py           # Category 2
│       ├── test_corruption.py     # Category 3
│       ├── test_ingestion.py      # Category 4
│       ├── test_empty_rag.py      # Category 5
│       ├── test_cross_project.py   # Category 6
│             ├── test_tool_abuse.py    # Category 7
│       ├── test_latency.py        # Category 8 (ARM-realistic)
│       └── test_observability.py  # Category 9
├── docker-compose.test.yml       # Test environment
├── metrics_parser.py             # Parse MCP metrics
└── test_report.md               # This document
```

### Docker Compose Test Environment

```yaml
# docker-compose.test.yml
version: '3.8'

services:
  rag-mcp:
    build:
      context: .
      dockerfile: Dockerfile.pi
    container_name: rag-mcp-test
    volumes:
      # Production memory volumes
      - ./data/test_memory:/app/data
      - ./data/test_semantic_index:/app/data/semantic_index
      - ./data/test_episodic.db:/app/data/episodic.db
      # Metrics/log collection
      - ./test_output:/app/test_output
    environment:
      - RAG_DATA_DIR=/app/data
      - LOG_LEVEL=DEBUG
      - ENABLE_METRICS=true
      - ENABLE_DEBUG_LOGS=true
    ports:
      - "8001:8001"
    cap_add:
      - SYS_ADMIN  # For failure simulation

  # Test metrics collection service
  test-collector:
    image: python:3.11-slim
    volumes:
      - ./test_output:/test_output
    command: python -m http.server 8080 --directory /test_output
```

---

## Test Categories (9 Total)

### ✅ CATEGORY 1: MCP Server Crash & Restart Tests (CRITICAL)

**Goal**: Prove persistence & safe recovery

**Scenarios**:
1. **Crash During Ingestion**
   - Kill container mid-file ingestion
   - Restart container
   - Assert: No partial chunks, no orphaned metadata, complete files re-ingestable

2. **Crash During Retrieval**
   - Kill container during rag.search
   - Restart container
   - Assert: Previous searches still work, no corrupted indexes

3. **Hard Kill & Restart**
   - Force kill (-9) container
   - Restart
   - Assert: All three memory types intact, no data loss

4. **Clean Restart (No Data Loss)**
   - Normal restart (docker-compose restart)
   - Assert: Same content before/after, no corruption

**Success Criteria**:
- ✅ No corrupted vector stores after any crash scenario
- ✅ No partial chunks in semantic index
- ✅ Symbolic/episodic memory consistent across restarts
- ✅ Metrics emitted on every startup/shutdown

---

### ✅ CATEGORY 2: Disk Failure & Read-Only Mode Tests

**Goal**: Prove graceful degradation

**Scenarios**:
1. **Simulate Full Disk**
   - Mount a tiny 1MB volume for /app/data
   - Attempt large file ingestion
   - Assert: Clear error, safe fallback, no crash

2. **Simulate Disk Full During Retrieval**
   - Fill volume, then run searches
   - Assert: Searches fail gracefully with clear error

3. **Simulate Permission Denied**
   - Make /app/data read-only (chmod 444)
   - Attempt all write operations
   - Assert: All fail with "permission denied" or "read-only mode"

4. **Read-Only Mode Behavior**
   - Run queries in read-only mode
   - Assert: Retrieval still works, writes fail cleanly

**Success Criteria**:
- ✅ System never crashes on disk errors
- ✅ All errors logged with clear messages
- ✅ Read-only mode allows reads, blocks writes
- ✅ No silent data corruption

---

### ✅ CATEGORY 3: Corrupted Vector Store Recovery Tests

**Goal**: Prove containment of corruption

**Scenarios**:
1. **Manual Index Corruption**
   - Manually corrupt chunks.json (add duplicate chunk_id, break JSON)
   - Run retrieval
   - Assert: Error detected, other projects unaffected

2. **Metadata/Index Mismatch**
   - Delete document from metadata but not chunks.json
   - Run retrieval
   - Assert: Orphaned chunks detected or cleaned automatically

3. **Empty/Zero-Length Chunks**
   - Inject chunks with empty content
   - Run search
   - Assert: Empty chunks handled gracefully or filtered

4. **Broken Embeddings**
   - Modify chunks.json to have invalid embedding vectors
   - Run search
   - Assert: Error caught, graceful degradation

5. **Full Index Recovery**
   - Delete entire semantic_index directory
   - Call `rag.verify_embeddings` → all missing
   - Run `rag.reindex_semantic(force=true)` → all fixed
   - Assert: Full recovery successful

**Success Criteria**:
- ✅ Corruption detected early and logged
- ✅ Affected project isolated from others
- ✅ Recovery mechanisms work end-to-end
- ✅ No silent data loss

---

### ✅ CATEGORY 4: Partial File Ingestion Tests

**Goal**: Prove ingestion atomicity

**Scenarios**:
1. **Kill During Large File**
   - Ingest 100KB file, kill at 50%
   - Restart
   - Assert: File either fully present or fully absent, no partial state

2. **Kill Mid-Batch (10 files)**
   - Start batch ingest of 10 files
   - Kill after 5 files
   - Restart
   - Assert: Either 0 or 10 files present, no inconsistent state

3. **Interrupted Directory Ingestion**
   - Ingest directory with 20 files
   - Kill mid-way through
   - Restart
   - Assert: No orphaned chunks, clean recovery path

4. **Re-Ingestion After Failure**
   - Fail ingestion, then retry same file
   - Assert: No duplicate chunks, idempotent behavior

**Success Criteria**:
- ✅ No half-indexed files in any scenario
- ✅ No orphaned chunks after partial failures
- ✅ Re-ingestion is idempotent
- ✅ Batch operations can be resumed cleanly

---

### ✅ CATEGORY 5: Empty/Misleading RAG Tests

**Goal**: Prove safe fallback behavior

**Scenarios**:
1. **Empty Vector Store**
   - Delete all chunks from semantic index
   - Run retrieval queries
   - Assert: Returns empty results, no hallucinations, no crashes

2. **All Low-Score Results**
   - Add chunks with low similarity scores (<0.3)
   - Run retrieval
   - Assert: Results returned but flagged as low-quality, no misleading content

3. **Query With No Context**
   - Query for non-existent topic
   - Run retrieval
   - Assert: Returns empty or minimal results, doesn't fabricate content

4. **Ambiguous Queries**
   - Query with multiple interpretations
   - Run retrieval multiple times
   - Assert: Consistent results, no random hallucinations

**Success Criteria**:
- ✅ Empty results surfaced to caller (not hidden)
- ✅ Low-quality results are flagged for attention
- ✅ No hallucinations when knowledge is absent
- ✅ System doesn't "make up" responses

---

### ✅ RATEGORY 6: Cross-Project Isolation Failure Tests (CRITICAL)

**Goal**: Prove strict project boundaries

**Scenarios**:
1. **Same Query Across Projects**
   - Query "system architecture" in project "pi-rag"
   - Query "system architecture" in project "other-project"
   - Assert: Different results, no shared chunks, no data leakage

2. **Project Deletion Doesn't Affect Others**
   - Delete all chunks from "pi-rag"
   - Run search on both projects
   - Assert: "other-project" still works, no cross-project data loss

3. **Corrupted Project Doesn't Corrupt Others**
   - Manually corrupt "pi-rag" chunks.json
   - Run search on both projects
   - Assert: "other-project" unaffected, error logged for "pi-rag"

4. **Cleanup One Project**
   - Run `rag.cleanup_memory` on "pi-rag"
   - Verify "other-project" untouched
   - Assert: Isolation maintained

**Success Criteria**:
- ✅ No shared chunks between projects
- ✅ Project deletion affects only that project
- ✅ Corruption is isolated (doesn't spread)
- ✅ Metrics and logs include project_id for all operations

---

### ✅ RATEGORY 7: Tool Misuse & Abuse Tests

**Goal**: Prove robustness against misuse

**Scenarios**:
1. **Missing project_id**
   - Call rag.ingest_file without project_id
   - Assert: Error message "project_id is required", no silent default

2. **Invalid project_id Format**
   - Use non-existent project: "malicious-inject"
   - Assert: Project created but isolated, no side effects

3. **Excessive Top_K Values**
   - Call rag.search with top_k=10000
   - Assert: Limited to configured max (top_k=10), rate-limited

4. **Spam Ingestion Attacks**
   - Attempt rapid batch ingestion (100 files in <1 second)
   - Assert: Rate-limited, queue or delayed

5. **Flood Search Requests**
   - Make 100 search requests rapidly
   - Assert: Rate-limited or rejected after threshold

6. **Special Characters in Inputs**
   - Try injecting shell commands in query
   - Assert: Input sanitized, no RCE

7. **Large Metadata Payloads**
   - Try 10MB metadata object
   - Assert: Validation error or size limit enforced

**Success Criteria**:
- ✅ All invalid inputs rejected with clear error messages
- ✅ No silent failures or default behaviors
- ✅ Rate limiting protects against abuse
- ✅ No code execution from sanitized inputs

---

### ✅ CATEGORY 8: Latency Spike & Load Tests (ARM-REALISTIC)

**Goal**: Prove stability under load

**Scenarios**:
1. **Burst of Searches**
   - Make 50 concurrent search requests
   - Assert: System stays responsive (<5s p95 latency), no deadlocks

2. **Concurrent Ingestion**
   - Ingest 10 files concurrently
   - Assert: All files ingested correctly, no lost chunks, embeddings generated

3. **Memory Pressure Simulation**
   - Ingest 100MB of data
   - Monitor memory usage
   - Assert: No memory leaks, graceful degradation

4. **Long-Running Operations**
   - 24-hour continuous retrieval test (1 query/minute)
   - Assert: No memory growth, no slowdown over time

**Success Criteria (ARM-specific)**:
- ✅ System handles burst load without crashing
- ✅ Latency increases predictably under load
- ✅ No deadlocks or race conditions
- ✅ Memory usage stabilizes (no leaks)

---

### ✅ CATEGORY 9: Observability Validation Tests

**Goal**: Prove visibility during failures

**Assertions**:
1. **Metrics Emitted During Failures**
   - Corrupt vector store
   - Kill container during operation
   - Assert: Metrics show tool call count, error count, latency

2. **Logs Include project_id**
   - Check all log lines
   - Assert: Every log entry includes project_id, no cross-project data in logs

3. **Mutation Audit Trail**
   - Delete a chunk
   - Verify operation is in audit log
   - Assert: All mutations tracked with timestamp, operation, value

4. **Clear Error Messages**
   - Trigger read-only mode
   - Verify error message is human-readable
   - Assert: No cryptic errors, includes actionable recovery steps

5. **Metrics API Accessibility**
   - Call rag.get_memory_stats
   - Verify metrics endpoint returns data
   - Assert: Comprehensive stats across all memory types

**Success Criteria**:
- ✅ Every failure is observable via metrics
- ✅ Root cause can be determined from logs
- ✅ No silent failures or data loss
- ✅ Audit trail supports recovery investigation

---

## Test Harness Design

### MCP Client Wrapper (`mcp_harness.py`)

```python
class MCPTestHarness:
    """
    Real MCP client wrapper for production testing.
    
    Features:
    - Connects to running RAG MCP server
    - Wraps all 15 MCP tools
    - Collects metrics and responses
    - Supports failure injection
    """
    
    def __init__(self, base_url="http://localhost:8001"):
        self.base_url = base_url
        self.session_id = str(uuid.uuid4())
        self.metrics = []
    
    async def call_tool(self, name: str, params: dict) -> dict:
        """Call MCP tool and capture result."""
        result = await self._mcp_call(name, params)
        self.metrics.append({
            "tool": name,
            "params": params,
            "result": result,
            "timestamp": datetime.now().isoformat()
        })
        return result
    
    async def _mcp_call(self, name: str, params: dict) -> dict:
        """Make actual MCP HTTP call."""
        # Use real MCP SDK
        from mcp.client import Client
        async with Client(self.base_url) as client:
            result = await client.call_tool(name, params)
            return result
```

### Metrics Parser (`metrics_parser.py`)

```python
def parse_mcp_metrics(metrics_output: str) -> dict:
    """
    Parse MCP server metrics output.
    
    Returns structured metrics:
    - Total calls per tool
    - Success/error rates
    - Latency metrics (p50, p95, p99)
    - Recent errors
    """
```

---

## Docker Orchestration (`docker_orchestrate.py`)

### Key Functions

```python
async def start_test_environment():
    """Start Docker test environment."""
    await run_docker_compose("up -f docker-compose.test.yml")

async def restart_container(service_name="rag-mcp"):
    """Gracefully restart RAG container."""
    await run_docker_compose(f"restart {service_name}")

async def kill_container(service_name="rag-mcp", signal=9):
    """Kill container with signal (-9 = SIGKILL)."""
    await run_docker_compose(f"kill -s SIGKILL {service_name}")

async def simulate_disk_full():
    """Mount tiny volume to simulate disk full."""
    # Modify docker-compose.test.yml to use 1MB volume
    await run_docker_compose("up -f docker-compose.test.yml")

async def make_read_only(path="/app/data"):
    """Make path read-only."""
    await run_shell(f"chmod 444 {path}")

async def restore_permissions(path="/app/data"):
    """Restore normal permissions."""
    await run_shell(f"chmod 755 {path}")

async def collect_metrics():
    """Collect and save metrics from all containers."""
    # Query rag.get_memory_stats endpoint
    # Save to test_output/metrics.json
```

---

## Success Criteria (HARD GATES)

The system is **NOT PRODUCTION-READY** until all gates pass:

### Hard Gates

| Gate | Criteria | Test Category |
|------|----------|----------------|
| **G1** | No data loss after crash+restart cycles | Cat 1 |
| **G2** | Graceful degradation on disk errors | Cat 2 |
| **G3** | Corruption doesn't spread across projects | Cat 3 |
| **G4** | No partial or orphaned chunks | Cat 4 |
| **G5** | Empty RAG doesn't hallucinate | Cat 5 |
| **G6** | Project boundaries are strictly enforced | Cat 6 |
| **G7** | Invalid inputs rejected | Cat 7 |
| **G8** | System stays responsive under load | Cat 8 |
| **G9** | All failures are observable | Cat 9 |

### Failure Mode Conditions

If ANY test fails with UNDEFINED BEHAVIOR:
- ❌ STOP: Do not deploy
- 🔧 FIX: Address root cause
- 🧪 RETEST: All gates must pass again

If tests pass but system panics in production:
- 🔴 EMERGENCY: Rollback immediately
- 🔍 INVESTIGATE: Use metrics/logs to trace
- 📋 DOCUMENT: Record for post-mortem

---

## Implementation Order

### Phase 1: Infrastructure (Day 1)
1. Create test directory structure
2. Write docker-compose.test.yml
3. Implement docker_orchestrate.py
4. Implement mcp_harness.py
5. Implement metrics_parser.py
6. Create observability.py skeleton

### Phase 2: Test Harness (Day 1)
1. Complete MCP client wrapper
2. Add metrics collection
3. Add failure injection capabilities
4. Test basic connectivity

### Phase 3: Category Tests (Days 2-4)
1. Implement and run Category 1 tests (Crash/Restart)
2. Implement and run Category 2 tests (Disk Failure)
3. Implement and run Category 3 tests (Corruption)
4. Implement and run Category 4 tests (Partial Ingestion)
5. Implement and run Category 5 tests (Empty RAG)
6. Implement and run Category 6 tests (Cross-Project)
7. Implement and run Category 7 tests (Tool Misuse)
8. Implement and run Category 8 tests (Latency/Load)
9. Implement and run Category 9 tests (Observability)

### Phase 4: Integration (Day 5)
1. Run all 9 categories end-to-end
2. Generate comprehensive test report
3. Verify all 9 hard gates pass
4. Document any failures and remediation steps

---

## Exit Criteria

### SUCCESS State
- All 9 hard gates pass
- No undefined behaviors observed in 100+ runs per test
- System remains stable under stress testing
- Full test report shows 100% pass rate
- Production deployment approved

### FAILURE STATE
- Any hard gate fails
- Root cause documented
- Fix implemented
- All 9 gates pass in retest
- Deployment blocked until approval

---

## Next Steps

1. Review and approve this test plan
2. Authorize creation of test infrastructure
3. Begin implementation starting with Phase 1
4. Report progress at end of each phase
5. Generate final certification report

---

**Document Version**: 1.0
**Last Updated**: 2025-12-29
**Status**: 🟡 Waiting for approval
