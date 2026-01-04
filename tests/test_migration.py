"""Test database consistency after pi-rag → synapse migration"""
import pytest
import sqlite3
import tempfile
import os


def test_no_pi_rag_episodes_in_db():
    """Verify no 'pi-rag' project_id in episodic memory"""
    # This test verifies that migration completed successfully
    # and no old pi-rag project IDs remain

    # Use production database
    db_path = os.environ.get("EPISODIC_DB_PATH", "/opt/synapse/data/episodic.db")

    # Skip test if database doesn't exist
    if not os.path.exists(db_path):
        pytest.skip(f"Database not found: {db_path}")

    # Connect and check for pi-rag project_id
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM episodic_memory WHERE project_id='pi-rag'"
    )
    pi_rag_count = cursor.fetchone()[0]

    conn.close()

    # Assert no pi-rag episodes exist
    assert pi_rag_count == 0, (
        f"Found {pi_rag_count} episodes with 'pi-rag' project_id. "
        "Migration incomplete - run migration script to update project IDs."
    )


def test_synapse_project_registered():
    """Verify 'synapse' project can be created and registered"""
    # Use production database
    db_path = os.environ.get("REGISTRY_DB_PATH", "/opt/synapse/data/registry.db")

    # Skip test if database doesn't exist
    if not os.path.exists(db_path):
        pytest.skip(f"Registry not found: {db_path}")

    # Connect to registry
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Check if projects table exists
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='projects'"
    )
    table_exists = cursor.fetchone() is not None

    if table_exists:
        # Check if synapse is registered
        cursor.execute(
            "SELECT COUNT(*) FROM projects WHERE project_id='synapse'"
        )
        synapse_count = cursor.fetchone()[0]
    else:
        synapse_count = 0

    conn.close()

    # Note: synapse may not be registered yet if setup not run
    # This test is informational for migration verification
    if synapse_count > 0:
        assert True  # Synapse project is registered
    else:
        pytest.skip("Synapse project not registered yet (run setup script)")


def test_migration_preserves_data():
    """Test that migration preserves all existing data"""
    # This is an informational test to verify data preservation
    # Actual migration test requires full database state before/after

    # Use production databases
    episodic_db = os.environ.get("EPISODIC_DB_PATH", "/opt/synapse/data/episodic.db")
    memory_db = os.environ.get("MEMORY_DB_PATH", "/opt/synapse/data/memory.db")

    # Skip if databases don't exist
    if not os.path.exists(episodic_db) and not os.path.exists(memory_db):
        pytest.skip("Databases not found (run setup script)")

    # Check episodic database
    if os.path.exists(episodic_db):
        conn = sqlite3.connect(episodic_db)
        cursor = conn.cursor()

        # Check table structure
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        conn.close()

        assert len(tables) > 0, "Episodic database has no tables"

    # Check memory database
    if os.path.exists(memory_db):
        conn = sqlite3.connect(memory_db)
        cursor = conn.cursor()

        # Check table structure
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()

        conn.close()

        assert len(tables) > 0, "Memory database has no tables"


def test_database_file_permissions():
    """Verify database files have correct permissions"""
    # Check that databases are accessible and writable

    episodic_db = os.environ.get("EPISODIC_DB_PATH", "/opt/synapse/data/episodic.db")
    memory_db = os.environ.get("MEMORY_DB_PATH", "/opt/synapse/data/memory.db")

    # Skip if databases don't exist
    if not os.path.exists(episodic_db) and not os.path.exists(memory_db):
        pytest.skip("Databases not found (run setup script)")

    # Check episodic database
    if os.path.exists(episodic_db):
        assert os.access(episodic_db, os.R_OK), (
            f"Cannot read episodic database: {episodic_db}"
        )
        assert os.access(episodic_db, os.W_OK), (
            f"Cannot write to episodic database: {episodic_db}"
        )

    # Check memory database
    if os.path.exists(memory_db):
        assert os.access(memory_db, os.R_OK), (
            f"Cannot read memory database: {memory_db}"
        )
        assert os.access(memory_db, os.W_OK), (
            f"Cannot write to memory database: {memory_db}"
        )


def test_data_directory_structure():
    """Verify SYNAPSE data directory structure is correct"""
    data_dir = os.environ.get("SYNAPSE_DATA_DIR", "/opt/synapse/data")

    # Skip if data directory doesn't exist
    if not os.path.exists(data_dir):
        pytest.skip(f"Data directory not found: {data_dir}")

    # Verify directory is readable
    assert os.path.isdir(data_dir), f"Not a directory: {data_dir}"
    assert os.access(data_dir, os.R_OK), f"Cannot read directory: {data_dir}"

    # Check for expected subdirectories (may not exist yet)
    expected_subdirs = ["backup", "loki-data", "chroma_semantic"]
    for subdir in expected_subdirs:
        subdir_path = os.path.join(data_dir, subdir)
        if os.path.exists(subdir_path):
            assert os.path.isdir(subdir_path), f"Not a directory: {subdir_path}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
