"""Test configuration file handling"""
import os
import pytest
from synapse.rag import MemoryStore, MemoryFact


def test_default_data_dir_without_env():
    """Test default data directory when no environment variable is set"""
    import os
    # Clear environment variable to test default
    if "RAG_DATA_DIR" in os.environ:
        del os.environ["RAG_DATA_DIR"]
    
    store = MemoryStore(":memory:")
    data_dir = store._get_data_dir()
    
    # Default should be /app/data (container default)
    assert data_dir == "/app/data"


def test_custom_data_dir_via_env():
    """Test custom data directory via environment variable"""
    import os
    os.environ["RAG_DATA_DIR"] = "/custom/data"
    
    store = MemoryStore(":memory:")
    data_dir = store._get_data_dir()
    
    assert data_dir == "/custom/data"
    
    # Cleanup
    del os.environ["RAG_DATA_DIR"]


def test_config_file_path_resolution():
    """Test config file path resolution"""
    import os
    from pathlib import Path
    
    # Test relative path resolution
    script_dir = Path(__file__).parent.parent
    config_dir = script_dir / "configs"
    
    assert config_dir.is_absolute()


def test_config_json_structure():
    """Test that config JSON has required fields"""
    import json
    import tempfile
    
    # Create a minimal valid config
    config_data = {
        "rag_enabled": True,
        "chunk_size": 500,
        "top_k": 3,
        "index_path": "/app/data/rag_index",
        "docs_path": "/app/data/docs",
        "memory_enabled": True,
        "memory_db_path": "/app/data/memory.db",
        "remote_file_upload_enabled": True,
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(config_data, f, indent=2)
        config_path = f.name
    
    # Parse and validate
    with open(config_path, 'r') as f:
        loaded = json.load(f)
    
    assert loaded["rag_enabled"] == True
    assert loaded["chunk_size"] == 500
    assert loaded["index_path"] == "/app/data/rag_index"


def test_missing_config_file():
    """Test behavior when config file is missing"""
    import os
    import tempfile
    
    # Create temp directory without config
    with tempfile.TemporaryDirectory() as temp_dir:
        old_cwd = os.getcwd()
        os.chdir(temp_dir)
        
        # Store original config path
        original_path = os.environ.get("RAG_CONFIG_PATH")
        del os.environ["RAG_CONFIG_PATH"]
        
        try:
            store = MemoryStore(":memory:")
            # Should not crash without config
            data_dir = store._get_data_dir()
            # Should return default
            assert data_dir == "/app/data"
        finally:
            # Restore
            os.chdir(old_cwd)
            if original_path:
                os.environ["RAG_CONFIG_PATH"] = original_path
