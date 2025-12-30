# RAG Reliability Tests - Quick Start Guide

**Purpose**: End-to-end reliability and failure-mode tests for RAG MCP server on ARM/Raspberry Pi

**Status**: 🟡 In Progress
**Date**: 2025-12-29

---

## Quick Start

### Prerequisites

```bash
# Install Docker Compose (if not already installed)
sudo apt-get install docker-compose

# Make test scripts executable
chmod +x tests/reliability/*.py
chmod +x tests/reliability/categories/*.py
```

### Running All Tests

```bash
# From project root:
python tests/reliability/run_all_tests.py
```

### Running Individual Categories

```bash
# Category 1: Crash & Recovery Tests (CRITICAL)
python tests/reliability/categories/test_crash_recovery.py

# Category 2: Disk Failure Tests (CRITICAL)
python tests/reliability/categories/test_disk_failure.py

# Category 3: Corrupted Vector Store Recovery Tests
python tests/reliability/categories/test_corruption_recovery.py

# Category 4: Partial File Ingestion Tests
python tests/reliability/categories/test_partial_ingestion.py

# Category 5: Empty/Misleading RAG Tests
python tests/reliability/categories/test_empty_rag.py

# Category 6: Cross-Project Isolation Tests (CRITICAL)
python tests/reliability/categories/test_cross_project.py

# Category 7: Tool Misuse & Abuse Tests
python tests/reliability/categories/test_tool_abuse.py

# Category 8: Latency Spike & Load Tests (ARM-Realistic)
python tests/reliability/categories/test_latency_load.py

# Category 9: Observability Validation Tests
python tests/reliability/categories/test_observability.py
```

---

## Test Categories Summary

| Category | Tests | Status | Criticality |
|----------|--------|--------|------------|
| 1: Crash & Recovery | 3 | 🔴 CRITICAL |
| 2: Disk Failure | 2 | 🔴 CRITICAL |
| 3: Corruption Recovery | 5 | 🟠 HIGH |
| 4: Partial Ingestion | 4 | 🔴 CRITICAL |
| 5: Empty/Misleading RAG | 4 | 🟠 HIGH |
| 6: Cross-Project Isolation | 3 | 🔴 CRITICAL |
| 7: Tool Misuse & Abuse | 7 | 🟠 HIGH |
| 8: Latency/Load (ARM) | 4 | 🟡 MEDIUM |
| 9: Observability | 5 | 🔴 CRITICAL |
| **TOTAL** | **37** | |

---

## Success Criteria (HARD GATES)

All 9 gates must pass for system to be production-ready:

### Gate G1: Crash Recovery
- ✅ No data loss after crash+restart cycles
- ✅ No corrupted vector stores
- ✅ Subsequent searches work correctly

### Gate G2: Disk Failure
- ✅ Graceful degradation on disk errors
- ✅ All errors logged clearly
- ✅ No system panics

### Gate G3: Corruption Recovery
- ✅ Corruption doesn't spread across projects
- ✅ Affected project isolated
- ✅ Recovery mechanisms work

### Gate G4: Partial Ingestion
- ✅ No half-indexed files
- ✅ No orphaned chunks
- ✅ Re-ingestion is idempotent

### Gate G5: Empty RAG
- ✅ Empty results surfaced (not hidden)
- ✅ No hallucinations when knowledge absent
- ✅ System doesn't "make up" responses

### Gate G6: Cross-Project Isolation
- ✅ No shared chunks between projects
- ✅ Project boundaries strictly enforced
- ✅ Metrics include project_id

### Gate G7: Tool Misuse
- ✅ Invalid inputs rejected explicitly
- ✅ Rate limiting protects against abuse
- ✅ No silent failures

### Gate G8: Latency/Load
- ✅ System stays responsive under load
- ✅ No deadlocks or race conditions
- ✅ Memory usage stabilizes

### Gate G9: Observability
- ✅ All failures observable via metrics
- ✅ Root cause can be determined from logs
- ✅ No silent data loss

---

## Output Structure

After running tests, you'll find:

```
test_output/
├── category_1_results.json
├── category_2_results.json
├── category_3_results.json
├── category_4_results.json
├── category_5_results.json
├── category_6_results.json
├── category_7_results.json
├── category_8_results.json
├── category_9_results.json
└── final_test_report.json
```

---

## Environment Variables

```bash
# RAG configuration
export RAG_DATA_DIR=/app/data
export LOG_LEVEL=DEBUG
export ENABLE_METRICS=true

# Test configuration
export TEST_TIMEOUT_SECONDS=30
export TEST_RETRIES=3
export TEST_PARALLEL=false  # Run tests sequentially for reliability
```

---

## Interpreting Results

### Pass/Fail Matrix

| Status | Meaning | Action |
|--------|----------|---------|
| ✅ ALL PASSED | All tests in category passed | Ready for deployment |
| ❌ SOME FAILED | 1+ tests failed | Fix and retest |
| ⚠️ TIMEOUT | Test timed out | Increase timeout or investigate |
| 🔴 CRITICAL FAILURE | Test failed catastrophically | STOP and investigate |

### Sample Test Report

```json
{
  "category": "CATEGORY 1 - Crash & Recovery Tests",
  "timestamp": "2025-12-29T12:00:00Z",
  "total_tests": 3,
  "passed": 3,
  "failed": 0,
  "tests": [
    {
      "name": "Crash During Ingestion",
      "status": "pass",
      "duration_seconds": 15.3
    },
    {
      "name": "Crash During Retrieval",
      "status": "pass",
      "duration_seconds": 12.7
    },
    {
      "name": "Hard Kill & Restart",
      "status": "pass",
      "duration_seconds": 18.2
    }
  ],
  "gate": "G1",
  "gate_passed": true
}
```

---

## Troubleshooting

### Docker Issues

```bash
# Container won't start
docker logs rag-mcp-test

# Container not responding
docker ps | grep rag-mcp-test

# Volume permission issues
ls -la data/test_memory
chmod 755 data/test_memory
```

### Test Issues

```bash
# Tests run too slowly
export TEST_TIMEOUT_SECONDS=60

# Tests failing randomly
export TEST_RETRIES=5

# Need debug output
export LOG_LEVEL=DEBUG
docker logs rag-mcp-test | tail -100
```

---

## Next Steps

1. **Run Initial Test Suite**: Execute all 9 categories
2. **Review Results**: Check test_output/ for results
3. **Address Failures**: Fix any failing tests
4. **Re-run Until Clean**: All 9 gates must pass
5. **Generate Final Report**: Run comprehensive report generation
6. **Production Approval**: Sign off for deployment

---

## References

- Full Test Plan: `tests/reliability/RAG_RELIABILITY_TESTS.md`
- Docker Orchestration: `tests/reliability/docker_orchestrate.py`
- MCP Harness: `tests/reliability/mcp_harness.py`
- Docker Compose: `tests/reliability/docker-compose.test.yml`

---

**Last Updated**: 2025-12-29
**Version**: 1.0
