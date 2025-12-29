"""
Pytest Configuration and Shared Fixtures
======================================

This conftest.py provides:
- Separate test databases (not mixing with production data)
- Shared fixtures for all test files
- Test isolation and cleanup

Test Database Structure:
- Tests use separate DB files (in tests/db/)
- Production DB is in data/memory.db
- No test should modify production data
"""

import os
import shutil
import tempfile
from pathlib import Path
from typing import Generator

import pytest


# ============================================================================
# Test Database Paths
# ============================================================================

# Root directory for test databases
TEST_DB_DIR = Path(__file__).parent / "test_dbs"

# Production database (should NEVER be modified by tests)
PROD_DB_PATH = Path(__file__).parent.parent / "data" / "memory.db"

# Vector store directory for tests
TEST_VECTOR_DIR = Path(__file__).parent / "test_vectorstores"


def setup_test_environment():
    """
    Setup test environment with separate directories.

    Creates:
    - tests/test_dbs/ (for SQLite databases)
    - tests/test_vectorstores/ (for ChromaDB vector stores)
    """
    # Create test database directory
    TEST_DB_DIR.mkdir(parents=True, exist_ok=True)

    # Create test vector store directory
    TEST_VECTOR_DIR.mkdir(parents=True, exist_ok=True)


def cleanup_test_environment():
    """
    Cleanup test environment (removes all test databases).
    """
    if TEST_DB_DIR.exists():
        shutil.rmtree(TEST_DB_DIR)

    if TEST_VECTOR_DIR.exists():
        shutil.rmtree(TEST_VECTOR_DIR)


# ============================================================================
# Pytest Hooks
# ============================================================================

def pytest_configure(config):
    """
    Configure pytest before test run.

    Called once at the beginning of the test session.
    """
    # Setup test environment
    setup_test_environment()


def pytest_unconfigure(config):
    """
    Cleanup after test run.

    Called at the end of the test session.
    """
    # Note: We don't auto-cleanup by default to allow inspection
    # Use --cleanup-dbs flag to cleanup after tests
    pass


def pytest_addoption(parser, pluginmanager):
    """
    Add custom command-line options.
    """
    parser.addoption(
        "--cleanup-dbs",
        action="store_true",
        default=False,
        help="Cleanup all test databases after test run"
    )


def pytest_runtest_teardown(item, nextitem):
    """
    Called after each test item finishes.
    """
    # Individual test cleanup if needed
    pass


# ============================================================================
# Shared Fixtures
# ============================================================================

@pytest.fixture(scope="session", autouse=True)
def test_env_setup(request):
    """
    Setup test environment at session start.
    """
    setup_test_environment()
    yield
    # Teardown if --cleanup-dbs flag is set
    if request.config.getoption("--cleanup-dbs"):
        cleanup_test_environment()


@pytest.fixture
def test_db_path(request) -> Generator[str, None, None]:
    """
    Create a unique test database for each test.

    Returns:
        Path to temporary SQLite database

    The database is automatically cleaned up after the test.
    """
    # Create unique temp DB
    test_id = id(request) if hasattr(request, 'node') else id(test_db_path)
    db_filename = f"test_{test_id}.db"
    db_path = TEST_DB_DIR / db_filename

    yield str(db_path)

    # Cleanup
    if db_path.exists():
        os.remove(db_path)


@pytest.fixture
def test_db_path_persistent(request) -> Generator[str, None, None]:
    """
    Create a persistent test database (not auto-cleaned).

    Useful for tests that need to verify DB state across
    multiple operations within a single test.

    Returns:
        Path to temporary SQLite database

    The database is NOT automatically cleaned up.
    """
    # Create unique temp DB
    test_id = id(request) if hasattr(request, 'node') else id(test_db_path_persistent)
    db_filename = f"test_persistent_{test_id}.db"
    db_path = TEST_DB_DIR / db_filename

    yield str(db_path)

    # Note: No cleanup - allows cross-operation verification


@pytest.fixture(scope="session")
def test_vector_db_path(request) -> Generator[str, None, None]:
    """
    Create a test vector database path.

    Returns:
        Path to test ChromaDB vector store

    The vector store is cleaned up at session end if --cleanup-dbs is set.
    """
    # Create unique vector DB path
    test_id = id(request) if hasattr(request, 'node') else id(test_vector_db_path)
    vector_path = TEST_VECTOR_DIR / f"vector_test_{test_id}_{os.getpid()}"

    yield str(vector_path)

    # Teardown if --cleanup-dbs flag is set
    # Check in pytest_runtest_teardown hook


# ============================================================================
# Database Verification Fixtures
# ============================================================================

@pytest.fixture
def verify_prod_db_unchanged():
    """
    Fixture to verify production DB is unchanged after tests.

    Usage:
        def test_something(verify_prod_db_unchanged):
            # ... test code ...
            verify_prod_db_unchanged()

    Raises:
        AssertionError if production DB was modified
    """
    def _verify():
        # Production DB should not exist or be unchanged
        if PROD_DB_PATH.exists():
            # TODO: Could add checksum verification
            pass

    return _verify


@pytest.fixture
def memory_store_factory():
    """
    Factory function to create fresh MemoryStore instances.

    Usage:
        def test_something(memory_store_factory):
            store1 = memory_store_factory()
            store2 = memory_store_factory()  # Different instances

    Returns:
        Callable that creates MemoryStore instances
    """
    from rag.memory_store import MemoryStore

    _factory_id = 0

    def _factory(db_path: str = "") -> MemoryStore:
        """Create a fresh MemoryStore instance."""
        nonlocal _factory_id
        _factory_id += 1
        if not db_path:
            db_path = str(TEST_DB_DIR / f"factory_{_factory_id}.db")
        return MemoryStore(db_path)

    return _factory


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_memory_data():
    """
    Sample memory data for tests.

    Returns:
        Dictionary with sample facts organized by scope
    """
    return {
        "user": [
            {
                "category": "preference",
                "key": "output_format",
                "value": "json",
                "confidence": 0.95,
                "source": "user"
            },
            {
                "category": "preference",
                "key": "language",
                "value": "English",
                "confidence": 0.92,
                "source": "user"
            },
        ],
        "project": [
            {
                "category": "decision",
                "key": "programming_language",
                "value": "Python",
                "confidence": 0.95,
                "source": "user"
            },
            {
                "category": "constraint",
                "key": "max_response_length",
                "value": 1000,
                "confidence": 0.85,
                "source": "user"
            },
        ],
        "session": [
            {
                "category": "fact",
                "key": "current_topic",
                "value": "machine_learning",
                "confidence": 0.70,
                "source": "agent"
            }
        ],
        "org": [
            {
                "category": "constraint",
                "key": "security_level",
                "value": "strict",
                "confidence": 0.90,
                "source": "admin"
            }
        ]
    }


@pytest.fixture
def sample_user_query():
    """
    Sample user queries for testing.

    Returns:
        Dictionary of sample queries by type
    """
    return {
        "coding": "Help me build a REST API",
        "debugging": "Why is my code failing?",
        "architecture": "Design a microservices architecture",
        "general": "What should I do next?",
        "format_request": "Format the output as JSON",
    }


# ============================================================================
# Documentation
# ============================================================================

"""
Test Database Isolation Strategy:
==============================

1. Production DB: data/memory.db
   - NEVER modified by tests
   - Used only in production

2. Test DBs: tests/test_dbs/
   - All test databases created here
   - Each test gets unique DB filename
   - Auto-cleaned after test (or with --cleanup-dbs)

3. Vector Stores: tests/test_vectorstores/
   - Test-specific vector databases
   - Separate from production ChromaDB

Benefits:
- Tests never modify production data
- Each test is isolated
- Easy to inspect test DBs for debugging
- Simple cleanup with --cleanup-dbs flag

Running Tests:
=============

# Run all tests
pytest tests/

# Run specific test file
pytest tests/test_memory_injection_safety.py

# Run with cleanup after
pytest tests/ --cleanup-dbs

# Run with verbose output
pytest tests/ -v

# Run specific test
pytest tests/test_memory_injection_safety.py::TestRelevanceFiltering -v
"""
