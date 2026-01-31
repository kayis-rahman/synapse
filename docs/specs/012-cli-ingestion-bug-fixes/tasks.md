# Feature 012 - CLI & Ingestion Bug Fixes: Task Breakdown

**Feature ID**: 012-cli-ingestion-bug-fixes  
**Status**: [In Progress]  
**Created**: January 31, 2026  
**Last Updated**: January 31, 2026

---

## Task Statistics

| Phase | Tasks | Duration | Focus |
|-------|-------|----------|-------|
| Phase 1: CLI Config Fixes | 8 | 2-3 hours | JSON output, formatting |
| Phase 2: CLI Models Fixes | 6 | 2 hours | Model detection |
| Phase 3: CLI Ingest Implementation | 10 | 3-4 hours | Full ingest command |
| Phase 4: CLI Query Implementation | 10 | 3-4 hours | Full query command |
| Phase 5: BUG-INGEST-01 Fix | 12 | 4-5 hours | Persistence fix |
| Phase 6: Testing & Validation | 8 | 2-3 hours | Pytest + manual |
| **Total** | **54** | **16-19 hours** | |

---

## Phase 1: CLI Config Fixes (8 tasks)

### 1.1: Analyze Current Config Command
- [ ] 1.1.1 Read `synapse/cli/commands/config.py` (Linked to BUG-004)
- [ ] 1.1.2 Read `synapse/config/__init__.py` (Linked to BUG-005)
- [ ] 1.1.3 Document current --json implementation (or lack thereof) (Linked to BUG-004)
- [ ] 1.1.4 Document current output formatting issues (Linked to BUG-005)

### 1.2: Implement JSON Output
- [ ] 1.2.1 Add `--json` flag to config command (Linked to FR-1)
- [ ] 1.2.2 Implement JSON formatting with json.dumps (Linked to FR-1)
- [ ] 1.2.3 Test JSON output is valid (Linked to FR-1)
- [ ] 1.2.4 Test all config sections included (Linked to FR-1)

### 1.3: Fix Output Formatting
- [ ] 1.3.1 Improve print_config_summary function (Linked to FR-1)
- [ ] 1.3.2 Add consistent spacing and headers (Linked to FR-1)
- [ ] 1.3.3 Add typer styling for readability (Linked to FR-1)
- [ ] 1.3.4 Add color coding for status (Linked to FR-1)

**Phase 1 Exit Criteria:** `synapse config --json` outputs valid JSON

---

## Phase 2: CLI Models Fixes (6 tasks)

### 2.1: Analyze Current Models Command
- [ ] 2.1.1 Read `synapse/cli/commands/models.py` (Linked to BUG-006)
- [ ] 2.1.2 Test current models list output (Linked to BUG-006)
- [ ] 2.1.3 Document missing or incorrect model info (Linked to BUG-006)

### 2.2: Fix Model Detection
- [ ] 2.2.1 Update model file detection logic (Linked to FR-2)
- [ ] 2.2.2 Fix BGE-M3 detection (Linked to FR-2)
- [ ] 2.2.3 Fix Gemma model detection (Linked to FR-2)
- [ ] 2.2.4 Add missing model types (Linked to FR-2)

**Phase 2 Exit Criteria:** `synapse models list` shows all installed models

---

## Phase 3: CLI Ingest Implementation (10 tasks)

### 3.1: Analyze Current Ingest Command
- [ ] 3.1.1 Read `synapse/cli/commands/ingest.py` (Linked to BUG-007)
- [ ] 3.1.2 Document current stub implementation (Linked to BUG-007)
- [ ] 3.1.3 Review MCP ingest_file tool documentation (Linked to BUG-007)

### 3.2: Implement File Discovery
- [ ] 3.2.1 Add single file detection (Linked to FR-3)
- [ ] 3.2.2 Add directory traversal (Linked to FR-3)
- [ ] 3.2.3 Add file type filtering (.py, .md, .txt, .json) (Linked to FR-3)
- [ ] 3.2.4 Add progress reporting (Linked to FR-3)

### 3.3: Implement MCP Integration
- [ ] 3.3.1 Add httpx import and MCP endpoint call (Linked to FR-3)
- [ ] 3.3.2 Implement file upload via MCP ingest_file (Linked to FR-3)
- [ ] 3.3.3 Add error handling for MCP calls (Linked to FR-3)
- [ ] 3.3.4 Add success/failure reporting (Linked to FR-3)
- [ ] 3.3.5 Add --project-id option (Linked to FR-3)
- [ ] 3.3.6 Add --chunk-size option (Linked to FR-3)

**Phase 3 Exit Criteria:** `synapse ingest <path>` successfully ingests files

---

## Phase 4: CLI Query Implementation (10 tasks)

### 4.1: Analyze Current Query Command
- [ ] 4.1.1 Read `synapse/cli/commands/query.py` (Linked to BUG-008)
- [ ] 4.1.2 Document current stub implementation (Linked to BUG-008)
- [ ] 4.1.3 Review MCP search tool documentation (Linked to BUG-008)

### 4.2: Implement Query Logic
- [ ] 4.2.1 Add query text argument (Linked to FR-4)
- [ ] 4.2.2 Add --top-k option (Linked to FR-4)
- [ ] 4.2.3 Add --format option (json/text) (Linked to FR-4)
- [ ] 4.2.4 Add --mode option (Linked to FR-4)

### 4.3: Implement MCP Integration
- [ ] 4.3.1 Add httpx import and MCP endpoint call (Linked to FR-4)
- [ ] 4.3.2 Implement query via MCP search (Linked to FR-4)
- [ ] 4.3.3 Add SSE response parsing (Linked to FR-4)
- [ ] 4.3.4 Add output formatting (Linked to FR-4)
- [ ] 4.3.5 Add error handling (Linked to FR-4)

**Phase 4 Exit Criteria:** `synapse query "text"` returns relevant results

---

## Phase 5: BUG-INGEST-01 Fix (12 tasks)

### 5.1: Investigate Persistence Issue
- [ ] 5.1.1 Read `scripts/bulk_ingest.py` (Linked to BUG-INGEST-01)
- [ ] 5.1.2 Identify storage backend (ChromaDB/FAISS/custom) (Linked to BUG-INGEST-01)
- [ ] 5.1.3 Find persist/commit calls (Linked to BUG-INGEST-01)
- [ ] 5.1.4 Document current persistence flow (Linked to BUG-INGEST-01)

### 5.2: Fix Persistence
- [ ] 5.2.1 Add explicit persist/commit call (Linked to FR-5)
- [ ] 5.2.2 Verify collection.persist() or equivalent (Linked to FR-5)
- [ ] 5.2.3 Add error handling for persist failure (Linked to FR-5)
- [ ] 5.2.4 Add verification step (Linked to FR-5)
- [ ] 5.2.5 Test data persists after bulk_ingest (Linked to FR-5)
- [ ] 5.2.6 Test data survives server restart (Linked to FR-5)
- [ ] 5.2.7 Verify list_sources returns > 50 (Linked to FR-5)

### 5.3: Performance Optimization
- [ ] 5.3.1 Benchmark current ingestion time (Linked to NFR-2)
- [ ] 5.3.2 Identify bottlenecks (Linked to NFR-2)
- [ ] 5.3.3 Optimize if > 5 minutes (Linked to NFR-2)

**Phase 5 Exit Criteria:** Ingestion persists (> 50 sources in list_sources)

---

## Phase 6: Testing & Validation (8 tasks)

### 6.1: Write Pytest Tests
- [ ] 6.1.1 Create `tests/unit/test_cli_config.py` (Linked to NFR-1)
- [ ] 6.1.2 Create `tests/unit/test_cli_models.py` (Linked to NFR-1)
- [ ] 6.1.3 Create `tests/unit/test_cli_ingest.py` (Linked to NFR-1)
- [ ] 6.1.4 Create `tests/unit/test_cli_query.py` (Linked to NFR-1)
- [ ] 6.1.5 Create `tests/unit/test_bulk_ingest_persistence.py` (Linked to NFR-1)

### 6.2: Run Tests
- [ ] 6.2.1 Run pytest with coverage (Linked to NFR-1)
- [ ] 6.2.2 Fix any failing tests (Linked to NFR-1)
- [ ] 6.2.3 Verify 80%+ coverage (Linked to NFR-1)

### 6.3: Manual Validation
- [ ] 6.3.1 Test all CLI commands manually (Linked to US-001 to US-006)
- [ ] 6.3.2 Verify bug fixes (BUG-004 to BUG-009, BUG-INGEST-01)

**Phase 6 Exit Criteria:** All tests pass, 80%+ coverage, all bugs fixed

---

## Success Criteria Checklist

### Must Have (Go Live)
- [ ] FR-1: `synapse config --json` works
- [ ] FR-2: `synapse models list` complete
- [ ] FR-3: `synapse ingest` functional
- [ ] FR-4: `synapse query` functional
- [ ] FR-5: Ingestion persists (> 50 sources)
- [ ] BUG-004 fixed: JSON output
- [ ] BUG-005 fixed: Config formatting
- [ ] BUG-006 fixed: Models list
- [ ] BUG-007 fixed: Ingest command
- [ ] BUG-008 fixed: Query command
- [ ] BUG-009 fixed: Config flags
- [ ] BUG-INGEST-01 fixed: Persistence
- [ ] NFR-1: 80%+ pytest coverage

### Should Have (Quality)
- [ ] FR-6: Help text complete
- [ ] FR-7: Error messages helpful
- [ ] NFR-2: Ingestion < 5 minutes
- [ ] NFR-3: CLI response < 2 seconds

---

## Testing Commands Reference

### Pytest Commands
```bash
# Run all new tests
pytest tests/unit/test_cli_config.py tests/unit/test_cli_models.py \
       tests/unit/test_cli_ingest.py tests/unit/test_cli_query.py \
       tests/unit/test_bulk_ingest_persistence.py -v

# Run with coverage
pytest tests/unit/test_cli_*.py tests/unit/test_bulk_ingest_persistence.py \
       --cov=synapse.cli.commands --cov=scripts.bulk_ingest --cov-report=term-missing

# Run specific test file
pytest tests/unit/test_cli_config.py -v
```

### Manual Testing Commands
```bash
# Test config JSON
synapse config --json | jq .

# Test models list
synapse models list

# Test ingest
synapse ingest /path/to/file.py
synapse ingest /path/to/directory --project-id test

# Test query
synapse query "What is Synapse?"
synapse query "embedding model" --json

# Test persistence
bulk_ingest (via script)
curl -X POST http://localhost:8002/mcp -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"list_sources","arguments":{"project_id":"synapse"}}}'
```

---

## Notes

**Constraint Reminder:**
- NO source files modified except those listed
- NO temporary files in project root
- Test with mocks where possible
- Follow SDD protocol (AGENTS.md)

**Execution Order:**
1. Phase 1: CLI Config Fixes (quick wins)
2. Phase 2: CLI Models Fixes (quick wins)
3. Phase 3: CLI Ingest Implementation (core feature)
4. Phase 4: CLI Query Implementation (core feature)
5. Phase 5: BUG-INGEST-01 Fix (critical)
6. Phase 6: Testing & Validation (wrap up)

**Expected Issues:**
- MCP server must be running for ingest/query tests
- Mock embeddings may slow ingestion tests
- Persistence testing requires clean state

**Workarounds:**
- Use mocks for unit tests
- Skip integration tests if server unavailable
- Clear data directory before persistence tests

---

**Last Updated**: January 31, 2026  
**Status**: Ready for Implementation  
**Next Phase**: Phase 1 - CLI Config Fixes
