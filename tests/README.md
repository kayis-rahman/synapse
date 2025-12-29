# Test Suite Organization

## Overview

The test suite is organized by system phase and functionality, with clear separation between test concerns and production data.

## Test Files

### Phase 1: Symbolic Memory Tests

**test_symbolic_memory.py** (formerly `test_memory.py`)
- Tests for Phase 1 Symbolic Memory subsystem
- Validates MemoryStore CRUD operations
- Tests MemoryWriter extraction logic
- Tests MemoryReader querying and formatting
- Basic integration tests

### Phase 1 Comprehensive Integration Tests

**test_memory_integration_comprehensive.py** (formerly `test_memory_integration.py`)
- Production-grade integration tests for Symbolic Memory
- Tests persistence and restart behavior
- Tests write rule enforcement
- Tests determinism
- Tests scope isolation
- Tests auditability
- Tests that memory ≠ chat history

### Phase 2: Contextual Memory Injection Tests

**test_memory_injection_safety.py** (formerly `test_phase2_memory_injection.py`)
- Production-grade integration tests for Contextual Memory Injection
- Validates all 8 core invariants:
  1. Relevance filtering
  2. Confidence threshold enforcement
  3. Scope precedence
  4. Conflict surfacing
  5. Prompt injection resistance
  6. Memory immutability
  7. Prompt structure integrity
  8. Prompt size bounds
- 29 comprehensive integration tests

### General RAG Tests

**test_rag.py**
- Tests for RAG (Retrieval Augmented Generation) functionality
- Vector store operations
- Document ingestion tests

### Simple Tests

**test_simple.py**
- Basic smoke tests
- Quick validation of core functionality

### Comprehensive Test Suite

**test_suite.py**
- Comprehensive test runner
- May contain legacy or additional test coverage

### Code Parsing Tests

**test_parse_code_file.py**
- Tests for code file parsing functionality

## Test Database Isolation

### Structure

```
tests/
├── conftest.py                 # Pytest configuration and shared fixtures
├── test_dbs/                   # Test SQLite databases (auto-created)
│   ├── test_*.db               # Each test gets unique DB
│   └── factory_*.db            # Factory-generated DBs
├── test_vectorstores/            # Test ChromaDB vector stores
│   └── vector_test_*.db        # Test-specific vector DBs
├── test_*.py                   # Test modules
└── README.md                   # This file
```

### Production Data (Separate)

```
data/
├── memory.db                    # Production memory database (NEVER modified by tests)
└── memory_db_schema.sql        # Database schema
```

### Key Features

1. **Separate Test Databases**
   - All tests use `test_db_path` fixture
   - Creates unique DB files in `tests/test_dbs/`
   - Production DB (`data/memory.db`) is NEVER modified

2. **Shared Fixtures (conftest.py)**
   - `test_db_path()`: Auto-cleaning test database per test
   - `test_db_path_persistent()`: Persistent test DB for cross-operation verification
   - `test_vector_db_path()`: Test vector database path
   - `memory_store_factory()`: Factory for fresh MemoryStore instances
   - `sample_memory_data()`: Sample memory facts
   - `sample_user_query()`: Sample user queries

3. **Cleanup Options**
   ```bash
   # Run tests with auto-cleanup
   pytest tests/ --cleanup-dbs

   # Run tests without auto-cleanup (for debugging)
   pytest tests/
   ```

4. **Test Isolation**
   - Each test gets unique database filename
   - Tests don't interfere with each other
   - Production data is never at risk

## Running Tests

### Run All Tests

```bash
# Run all tests
pytest tests/ -v

# Run with cleanup
pytest tests/ --cleanup-dbs -v

# Run with coverage
pytest tests/ --cov=rag --cov-report=html
```

### Run Specific Test Files

```bash
# Run Phase 1 tests
pytest tests/test_symbolic_memory.py -v

# Run Phase 1 integration tests
pytest tests/test_memory_integration_comprehensive.py -v

# Run Phase 2 tests (Memory Injection Safety)
pytest tests/test_memory_injection_safety.py -v

# Run RAG tests
pytest tests/test_rag.py -v
```

### Run Specific Test Classes

```bash
# Run specific test class
pytest tests/test_memory_injection_safety.py::TestRelevanceFiltering -v

# Run specific test
pytest tests/test_memory_injection_safety.py::TestRelevanceFiltering::test_relevant_memory_included_irrelevant_excluded -v

# Run with detailed output
pytest tests/test_memory_injection_safety.py -xvs
```

### Run by Phase

```bash
# Phase 1 tests
pytest tests/test_symbolic_memory.py tests/test_memory_integration_comprehensive.py -v

# Phase 2 tests
pytest tests/test_memory_injection_safety.py -v
```

## Test Categories

### Phase 1: Symbolic Memory

**Coverage:**
- MemoryStore CRUD operations
- MemoryWriter extraction and validation
- MemoryReader querying and formatting
- Data persistence and durability
- Write rule enforcement
- Auditability and traceability
- Separation from chat history

**Key Invariants:**
- Deterministic operations
- No hallucinations in memory
- Explicit write rules only
- Full audit trail
- Memory ≠ chat history

### Phase 2: Contextual Memory Injection

**Coverage:**
- Relevance filtering (3 tests)
- Confidence threshold enforcement (3 tests)
- Scope precedence (3 tests)
- Conflict surfacing (3 tests)
- Prompt injection resistance (3 tests)
- Memory immutability (3 tests)
- Prompt structure integrity (5 tests)
- Prompt size bounds (2 tests)
- Determinism (4 tests)

**Key Invariants (All 8 Protected):**
1. ✅ Only relevant memory is injected
2. ✅ Memory is read-only
3. ✅ Confidence thresholds are enforced
4. ✅ Scope precedence is respected
5. ✅ Conflicts are surfaced, not hidden
6. ✅ Prompt injection attempts fail
7. ✅ Prompt size remains bounded
8. ✅ Memory never mutates during injection

## File Naming Convention

Test files use descriptive, phase-based naming:

```
test_{feature}_{aspect}.py
```

Examples:
- `test_symbolic_memory.py` - Tests for Symbolic Memory (Phase 1)
- `test_memory_injection_safety.py` - Tests for Memory Injection Safety (Phase 2)
- `test_memory_integration_comprehensive.py` - Comprehensive integration tests

## Production Safety

### What Tests Don't Touch

1. **Production Database**: `data/memory.db`
   - Tests create their own DBs in `tests/test_dbs/`

2. **Production Vector Store**: Any production ChromaDB
   - Tests create their own vector stores in `tests/test_vectorstores/`

3. **Configuration Files**: Config files in project root
   - Tests may use example configs only

4. **Model Files**: Model weights and GGUF files
   - Tests don't modify or load actual models

### What Tests Can Touch

1. **Test Databases**: `tests/test_dbs/*.db`
2. **Test Vector Stores**: `tests/test_vectorstores/*`
3. **Temporary Files**: `tests/__pycache__`, `tests/.pytest_cache`

## Debugging

### Inspect Test Databases

```bash
# List test databases
ls -lh tests/test_dbs/

# Examine test database
sqlite3 tests/test_dbs/test_*.db "SELECT * FROM memory_facts;"

# Check database schema
sqlite3 tests/test_dbs/test_*.db ".schema"
```

### Keep Test DBs for Inspection

```bash
# Run tests without cleanup
pytest tests/  # No --cleanup-dbs flag

# Now inspect the test DBs
ls -lh tests/test_dbs/
sqlite3 tests/test_dbs/test_somedb.db
```

## Test Results

### Phase 2: Contextual Memory Injection

**Status**: ✅ ALL TESTS PASSING

- **Total Tests**: 29
- **Passed**: 29
- **Failed**: 0
- **Success Rate**: 100%

**Invariants Validated**:
1. ✅ Relevance filtering
2. ✅ Confidence threshold enforcement
3. ✅ Scope precedence
4. ✅ Conflict surfacing
5. ✅ Prompt injection resistance
6. ✅ Memory immutability
7. ✅ Prompt structure integrity
8. ✅ Prompt size bounds
9. ✅ Determinism

See `PHASE2_TEST_SUMMARY.md` for detailed results.

## Best Practices

### Writing New Tests

1. **Use Shared Fixtures**
   ```python
   def test_my_feature(test_db_path, memory_store_factory):
       # test_db_path provides isolated database
       # memory_store_factory creates fresh instances
   ```

2. **Follow Naming Convention**
   ```python
   test_{feature}_{what}.py
   ```

3. **Document Test Invariant**
   ```python
   """
   INARIANT PROTECTS: What this test protects
   --------------------------------------
   Explanation of invariant...
   """
   ```

4. **Use Descriptive Assertions**
   ```python
   assert condition, "Clear message about what failed and why"
   ```

5. **Don't Mock Critical Components**
   - Use real SQLite databases
   - Use actual MemoryStore, MemorySelector, etc.
   - Only mock external dependencies (LLMs, APIs)

6. **Test Invariants, Not Implementations**
   - Test the contract, not the implementation
   - Test edge cases and boundary conditions
   - Test error conditions

## CI/CD Integration

```yaml
# .github/workflows/tests.yml example
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.13'
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      - name: Run Phase 1 tests
        run: pytest tests/test_symbolic_memory.py -v
      - name: Run Phase 2 tests
        run: pytest tests/test_memory_injection_safety.py -v
      - name: Cleanup test databases
        run: pytest tests/ --cleanup-dbs
```

## Troubleshooting

### Common Issues

**Issue**: Tests modify production database
- **Solution**: Ensure tests use `test_db_path` fixture, not direct paths

**Issue**: Tests interfere with each other
- **Solution**: Each test should use unique DB via `test_db_path` fixture

**Issue**: Test databases accumulate
- **Solution**: Run tests with `--cleanup-dbs` flag or manually delete `tests/test_dbs/`

**Issue**: "no such table: memory_facts" error
- **Solution**: Ensure MemoryStore is initialized with test DB path from fixture

## Summary

This test organization provides:
- ✅ Clear separation between test phases
- ✅ Meaningful, descriptive file names
- ✅ Complete test database isolation
- ✅ Shared fixtures for consistency
- ✅ Production data safety
- ✅ Easy debugging and inspection
- ✅ Comprehensive coverage of all system invariants
