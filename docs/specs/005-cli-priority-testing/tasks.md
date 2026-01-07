# Tasks: Phase 1 - Foundation & Setup Testing

**Feature ID**: 005-cli-priority-testing
**Phase**: 1 - Foundation & Setup
**Priority**: P0 (Critical Foundation)
**Status**: In Progress
**Created**: January 7, 2026

---

## Task Breakdown

This task list provides granular checklist for implementing and executing Phase 1 tests.

**ORDERING STRATEGY:**
1. Create test infrastructure first
2. Implement test scripts
3. Execute tests
4. Document results

---

## Phase 1.1: Test Infrastructure Setup (2 tasks)

### 1.1.1 Create Test Directory Structure
- [ ] Create `tests/cli/` directory
- [ ] Create `tests/cli/__init__.py` file
- [ ] Create `tests/cli/conftest.py` file (shared utilities)
- [ ] Verify directory structure is correct

### 1.1.2 Create Test Utility Functions
- [ ] Add `run_command()` utility function
- [ ] Add `assert_success()` utility function
- [ ] Add `assert_output_contains()` utility function
- [ ] Add `assert_directory_exists()` utility function
- [ ] Add `assert_timeout()` utility function
- [ ] Add `test_results` data structure
- [ ] Add `print_summary()` utility function

---

## Phase 1.2: P0-1 Setup Command Tests (10 tasks)

### 1.2.1 Create Test Script: P0-1 Setup
- [ ] Create `tests/cli/test_p0_setup.py` file
- [ ] Add imports (subprocess, sys, time, pathlib)
- [ ] Define TIMEOUTS dictionary
- [ ] Define ENVIRONMENTS dictionary
- [ ] Implement test result storage
- [ ] Add main() function
- [ ] Add error handling
- [ ] Add test summary output

### 1.2.2 Implement: Setup-1 Docker Auto-Detection
- [ ] Define test function `test_setup_1_docker()`
- [ ] Implement command: `docker exec rag-mcp synapse setup --no-model-check`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 60s
- [ ] Add assertion: output contains "Auto-detected Docker data directory"
- [ ] Add assertion: /app/data directory exists
- [ ] Add assertion: /app/data/models directory exists
- [ ] Record test result

### 1.2.3 Implement: Setup-2 Native Auto-Detection
- [ ] Define test function `test_setup_2_native()`
- [ ] Implement command: `synapse setup --no-model-check`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 60s
- [ ] Add assertion: output contains "Auto-detected native data directory"
- [ ] Add assertion: /opt/synapse/data directory exists
- [ ] Add assertion: /opt/synapse/data/models directory exists
- [ ] Record test result

### 1.2.4 Implement: Setup-3 User Home Auto-Detection
- [ ] Define test function `test_setup_3_user_home()`
- [ ] Implement command: `synapse setup --no-model-check` (from ~)
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 60s
- [ ] Add assertion: output contains "Auto-detected user home data directory"
- [ ] Add assertion: ~/.synapse/data directory exists
- [ ] Add assertion: ~/.synapse/data/models directory exists
- [ ] Record test result

### 1.2.5 Implement: Setup-4 Force Re-Setup
- [ ] Define test function `test_setup_4_force()`
- [ ] Implement command: `synapse setup --force --no-model-check`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 60s
- [ ] Add assertion: output contains "SYNAPSE setup complete!"
- [ ] Add assertion: existing directories preserved
- [ ] Record test result

### 1.2.6 Implement: Setup-5 Offline Mode
- [ ] Define test function `test_setup_5_offline()`
- [ ] Implement command: `synapse setup --offline --no-model-check`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 60s
- [ ] Add assertion: output contains "offline mode (no model downloads)"
- [ ] Add assertion: no download prompts (non-interactive)
- [ ] Record test result

### 1.2.7 Add Docker Container Check
- [ ] Add function to check if Docker container is running
- [ ] Skip Docker tests if container not running
- [ ] Log message about skipping Docker tests
- [ ] Continue with native/home mode tests

### 1.2.8 Add Permission Error Handling
- [ ] Add try-except for permission errors
- [ ] Log clear message if permission denied
- [ ] Continue with next test instead of failing entirely
- [ ] Document permission requirements

### 1.2.9 Add Network Error Handling
- [ ] Add try-except for network timeouts
- [ ] Use generous timeout (60s) for setup tests
- [ ] Log clear message if network error
- [ ] Use --offline flag to avoid network dependencies

### 1.2.10 Verify Test Script Completeness
- [ ] Verify all test functions are defined
- [ ] Verify all assertions are implemented
- [ ] Verify error handling is comprehensive
- [ ] Verify test summary is generated
- [ ] Verify exit codes are correct (0=success, 1=failure, 2=error)

---

## Phase 1.3: P0-2 Config Command Tests (8 tasks)

### 1.3.1 Create Test Script: P0-2 Config
- [ ] Create `tests/cli/test_p0_config.py` file
- [ ] Add imports and utility functions
- [ ] Define TIMEOUTs (2s for config)
- [ ] Implement main() function
- [ ] Add test summary output

### 1.3.2 Implement: Config-1 Docker Basic Display
- [ ] Define test function `test_config_1_docker()`
- [ ] Implement command: `docker exec rag-mcp synapse config`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: output contains "Data directory:"
- [ ] Add assertion: output contains "Models directory:"
- [ ] Add assertion: output contains "RAG index directory:"
- [ ] Record test result

### 1.3.3 Implement: Config-2 Docker Verbose Mode
- [ ] Define test function `test_config_2_docker_verbose()`
- [ ] Implement command: `docker exec rag-mcp synapse config --verbose`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: verbose output has more details
- [ ] Add assertion: output shows "chunk_size"
- [ ] Add assertion: output shows "top_k"
- [ ] Record test result

### 1.3.4 Implement: Config-3 Native Basic Display
- [ ] Define test function `test_config_3_native()`
- [ ] Implement command: `synapse config`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: output shows correct data directory (/opt/synapse/data)
- [ ] Add assertion: output shows correct models directory
- [ ] Record test result

### 1.3.5 Implement: Config-4 Native Verbose Mode
- [ ] Define test function `test_config_4_native_verbose()`
- [ ] Implement command: `synapse config --verbose`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: output shows all configuration values
- [ ] Record test result

### 1.3.6 Add Config Validation
- [ ] Add function to validate configuration output
- [ ] Check for required fields (data_dir, models_dir, rag_index_dir)
- [ ] Check for valid paths
- [ ] Add assertions for each field

### 1.3.7 Add Invalid Config Error Handling
- [ ] Add test for invalid config file
- [ ] Verify error message is clear
- [ ] Verify command exits with non-zero code
- [ ] Record test result

### 1.3.8 Verify Test Script Completeness
- [ ] Verify all test functions are defined
- [ ] Verify all assertions are implemented
- [ ] Verify verbose mode tests work correctly
- [ ] Verify test summary is generated

---

## Phase 1.4: P0-3 Models List Command Tests (6 tasks)

### 1.4.1 Create Test Script: P0-3 Models List
- [ ] Create `tests/cli/test_p0_models_list.py` file
- [ ] Add imports and utility functions
- [ ] Define TIMEOUTs (2s for models list)
- [ ] Implement main() function
- [ ] Add test summary output

### 1.4.2 Implement: Models-1 Docker List Installed
- [ ] Define test function `test_models_1_docker()`
- [ ] Implement command: `docker exec rag-mcp synapse models list`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: output contains "embedding"
- [ ] Add assertion: output contains "bge-m3-q8_0.gguf" (if installed)
- [ ] Add assertion: output shows model status
- [ ] Record test result

### 1.4.3 Implement: Models-2 Native List Installed
- [ ] Define test function `test_models_2_native()`
- [ ] Implement command: `synapse models list`
- [ ] Add assertion: exit_code == 0
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: output shows model file path
- [ ] Add assertion: output shows model file size (if installed)
- [ ] Add assertion: output is in readable format
- [ ] Record test result

### 1.4.4 Implement: Models-3 Handle Missing Models
- [ ] Define test function `test_models_3_missing()`
- [ ] Implement command: `synapse models list` (after removing models)
- [ ] Add assertion: exit_code == 0 (command doesn't fail)
- [ ] Add assertion: timeout < 2s
- [ ] Add assertion: output shows "not installed" for missing models
- [ ] Add assertion: clear indication of missing required model
- [ ] Record test result

### 1.4.5 Add Model Status Parsing
- [ ] Add function to parse model status from output
- [ ] Extract: model name, status, size, path
- [ ] Add assertions for each field
- [ ] Handle multiple models

### 1.4.6 Verify Test Script Completeness
- [ ] Verify all test functions are defined
- [ ] Verify all assertions are implemented
- [ ] Verify missing models test works correctly
- [ ] Verify test summary is generated

---

## Phase 1.5: Test Execution (4 tasks)

### 1.5.1 Execute P0-1 Setup Tests
- [ ] Run `python3 tests/cli/test_p0_setup.py`
- [ ] Verify all 5 tests run in Docker mode
- [ ] Verify all 5 tests run in native mode
- [ ] Verify all 5 tests run in user home mode
- [ ] Record all test results (pass/fail)
- [ ] Record performance metrics
- [ ] Document any failures

### 1.5.2 Execute P0-2 Config Tests
- [ ] Run `python3 tests/cli/test_p0_config.py`
- [ ] Verify all 4 tests run in Docker mode
- [ ] Verify all 4 tests run in native mode
- [ ] Record all test results (pass/fail)
- [ ] Record performance metrics
- [ ] Document any failures

### 1.5.3 Execute P0-3 Models List Tests
- [ ] Run `python3 tests/cli/test_p0_models_list.py`
- [ ] Verify all 3 tests run in Docker mode
- [ ] Verify all 3 tests run in native mode
- [ ] Record all test results (pass/fail)
- [ ] Record performance metrics
- [ ] Document any failures

### 1.5.4 Verify All Tests Passed
- [ ] Verify total test count: 24 tests
- [ ] Verify pass count: 24 tests
- [ ] Verify fail count: 0 tests
- [ ] Verify performance compliance: 100%
- [ ] Verify error handling: 100%
- [ ] Calculate overall success rate

---

## Phase 1.6: Documentation & Completion (3 tasks)

### 1.6.1 Create Test Results Document
- [ ] Create `docs/specs/005-cli-priority-testing/PHASE_1_RESULTS.md`
- [ ] Document all 24 test results
- [ ] Document pass/fail status for each test
- [ ] Document performance metrics
- [ ] Document any errors or issues
- [ ] Calculate overall success rate

### 1.6.2 Update Central Index
- [ ] Update `docs/specs/index.md` with feature 005 entry
- [ ] Set Phase 1 status to "[Completed]"
- [ ] Add completion date
- [ ] Add final commit hash
- [ ] Update overall progress

### 1.6.3 Mark Tasks Complete
- [ ] Mark all Phase 1.1 tasks as complete
- [ ] Mark all Phase 1.2 tasks as complete
- [ ] Mark all Phase 1.3 tasks as complete
- [ ] Mark all Phase 1.4 tasks as complete
- [ ] Mark all Phase 1.5 tasks as complete
- [ ] Mark all Phase 1.6 tasks as complete
- [ ] Update tasks.md with final commit hash

---

## Task Statistics

- **Total Tasks**: 43 tasks
- **Total Phases**: 6
- **Estimated Time**: 3-4 hours

**Task Breakdown by Phase:**
- Phase 1.1: Test Infrastructure (2 tasks)
- Phase 1.2: P0-1 Setup Tests (10 tasks)
- Phase 1.3: P0-2 Config Tests (8 tasks)
- Phase 1.4: P0-3 Models List Tests (6 tasks)
- Phase 1.5: Test Execution (4 tasks)
- Phase 1.6: Documentation (3 tasks)

---

## Test Coverage

**Total Tests**: 24 tests
- P0-1 (setup): 5 tests × 3 environments = 15 tests
- P0-2 (config): 4 tests × 2 environments = 8 tests
- P0-3 (models): 3 tests × 2 environments = 6 tests
  - **Note**: Models-3 (missing) tests in clean environment only

**Coverage Metrics**:
- Functional requirements: 100% (all FRs tested)
- Non-functional requirements: 80% (performance, error handling tested)
- Cross-platform coverage: 100% (Linux + Docker + User Home)

---

## Notes

**TESTING APPROACH (User Decisions):**
- Environments: Test all three modes (Docker, native, user home) - Option 1-A
- Test Data: Use existing project files (no fixtures) - Option 2-No
- Failure Criteria: Error, wrong output, OR performance degradation - Option 3-C
- Automation: Semi-automated scripts with assertions - Option 4-C
- Documentation: Pass/fail + metrics (not full logs) - User choice 5

**READY TO START**: Phase 1.1 - Test Infrastructure Setup

---

## Completion Checklist

Phase 1 is complete when:
- [ ] All 43 tasks marked as complete
- [ ] All 24 tests passing
- [ ] Performance compliance: 100%
- [ ] Test results documented
- [ ] Central index updated
- [ ] All changes committed to git
- [ ] Final commit hash added to tasks.md

---

**Last Updated**: January 7, 2026
