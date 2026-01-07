"""
SYNAPSE Configuration Defaults

Single source of truth for all SYNAPSE configuration settings.
Implements auto-detection, configuration layering, and validation.

Configuration Priority (lowest to highest):
1. Defaults (this file) - Sensible out-of-box defaults
2. User config - ~/.synapse/config.json (user-wide settings)
3. Project config - .synapse/config.json (project-specific settings)
4. Environment variables - SYNDROME_* (overrides everything)
5. CLI arguments - Highest priority (command-line flags)
"""

import os
import json
from pathlib import Path
from typing import Dict, Any, Optional, List


def detect_data_directory() -> str:
    """
    Auto-detect data directory with priority order.
    
    Priority:
    1. Docker container: /app/data
    2. Native install: /opt/synapse/data
    3. User home: ~/.synapse/data
    4. Fallback: ./data
    """
    # Docker container
    if os.path.exists("/app/data"):
        return "/app/data"
    
    # Native install
    if os.path.exists("/opt/synapse/data"):
        return "/opt/synapse/data"
    
    # User home
    user_data = Path.home() / ".synapse" / "data"
    if user_data.exists():
        return str(user_data)
    
    # Fallback (will create on first run)
    return str(Path.home() / ".synapse" / "data")


def detect_models_directory() -> str:
    """
    Auto-detect models directory.
    
    Priority:
    1. Docker container: /app/models
    2. Native install: /opt/synapse/models
    3. User home: ~/.synapse/models
    4. Fallback: ./models
    """
    # Docker container
    if os.path.exists("/app/models"):
        return "/app/models"
    
    # Native install
    if os.path.exists("/opt/synapse/models"):
        return "/opt/synapse/models"
    
    # User home
    user_models = Path.home() / ".synapse" / "models"
    if user_models.exists():
        return str(user_models)
    
    # Fallback (will create on first run)
    return str(Path.home() / ".synapse" / "models")


def detect_environment() -> str:
    """
    Detect current environment (Docker vs native).
    
    Returns: 'docker' or 'native'
    """
    if os.path.exists("/.dockerenv"):
        return "docker"
    
    # Check if running in container
    if os.path.exists("/app/data"):
        return "docker"
    
    return "native"


# Sensible defaults (authoritative source)
DEFAULT_CONFIG: Dict[str, Any] = {
    # RAG Settings
    "chunk_size": 500,
    "chunk_overlap": 50,
    "top_k": 3,
    "min_retrieval_score": 0.3,
    
    # Query Expansion
    "query_expansion_enabled": True,
    "num_expansions": 3,
    "query_expansion_method": "semantic",
    
    # Paths (auto-detected)
    "data_dir": detect_data_directory(),
    "models_dir": detect_models_directory(),
    "rag_index_dir": None,  # Will be set to {data_dir}/rag_index
    "docs_dir": None,  # Will be set to {data_dir}/docs
    "logs_dir": None,  # Will be set to {data_dir}/logs
    
    # Models
    "embedding_model": "bge-m3-q8_0.gguf",
    "chat_model": "gemma-3-1b-it-UD-Q4_K_XL.gguf",
    
    # Memory Systems
    "semantic_memory_enabled": True,
    "episodic_memory_enabled": True,
    "symbolic_memory_enabled": True,
    
    # Server Settings
    "mcp_port": 8002,
    "mcp_host": "0.0.0.0",
    
    # Environment
    "environment": detect_environment(),
    
    # Ingestion
    "gitignore_enabled": True,
    "max_file_size_mb": 50,
    "supported_extensions": [".md", ".txt", ".py", ".js", ".ts", ".json", ".yaml", ".yml", ".toml"],
}


def load_config_file(config_path: Optional[Path] = None) -> Dict[str, Any]:
    """
    Load configuration from JSON file.
    
    Returns empty dict if file doesn't exist or is invalid.
    """
    if config_path is None:
        # Try user-wide config
        user_config = Path.home() / ".synapse" / "config.json"
        if user_config.exists():
            config_path = user_config
        else:
            # Try project-specific config
            project_config = Path(".synapse") / "config.json"
            if project_config.exists():
                config_path = project_config
            else:
                return {}
    
    if not config_path.exists():
        return {}
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"⚠️  Warning: Failed to load config from {config_path}: {e}")
        return {}


def apply_environment_variables(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply environment variable overrides.
    
    Environment variables:
    - SYNDROME_DATA_DIR
    - SYNDROME_MODELS_DIR
    - SYNDROME_MCP_PORT
    - SYNDROME_MCP_HOST
    - SYNDROME_CHUNK_SIZE
    - SYNDROME_TOP_K
    """
    env_overrides = {
        "data_dir": os.getenv("SYNDROME_DATA_DIR"),
        "models_dir": os.getenv("SYNDROME_MODELS_DIR"),
        "mcp_port": os.getenv("SYNDROME_MCP_PORT"),
        "mcp_host": os.getenv("SYNDROME_MCP_HOST"),
        "chunk_size": os.getenv("SYNDROME_CHUNK_SIZE"),
        "top_k": os.getenv("SYNDROME_TOP_K"),
    }
    
    for key, env_value in env_overrides.items():
        if env_value is not None:
            # Type conversion
            if key in ["mcp_port", "chunk_size", "top_k"]:
                config[key] = int(env_value)
            else:
                config[key] = env_value
    
    return config


def get_config(
    user_config_path: Optional[Path] = None,
    project_config_path: Optional[Path] = None,
    env_overrides: bool = True
) -> Dict[str, Any]:
    """
    Get final configuration with all layers applied.
    
    Configuration layering (lowest to highest priority):
    1. Defaults (DEFAULT_CONFIG)
    2. User config (~/.synapse/config.json)
    3. Project config (.synapse/config.json)
    4. Environment variables (SYNDROME_*)
    5. CLI arguments (not included here, applied separately)
    
    Args:
        user_config_path: Path to user-wide config file
        project_config_path: Path to project-specific config file
        env_overrides: Apply environment variable overrides
    
    Returns:
        Final configuration dictionary
    """
    # Start with defaults
    config = DEFAULT_CONFIG.copy()
    
    # Apply user config
    user_config = load_config_file(user_config_path)
    config.update(user_config)
    
    # Apply project config
    project_config = load_config_file(project_config_path)
    config.update(project_config)
    
    # Apply environment overrides
    if env_overrides:
        config = apply_environment_variables(config)
    
    # Validate configuration
    config = validate_config(config)
    
    return config


def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validate configuration and fix common issues.
    
    - Ensure directories exist (create if missing)
    - Validate numeric ranges
    - Fix invalid paths
    """
    # Validate numeric ranges
    if config.get("chunk_size", 0) < 100:
        config["chunk_size"] = 100
        print("⚠️  Warning: chunk_size too small, set to minimum 100")
    
    if config.get("chunk_size", 0) > 2000:
        config["chunk_size"] = 2000
        print("⚠️  Warning: chunk_size too large, set to maximum 2000")
    
    if config.get("top_k", 0) < 1:
        config["top_k"] = 1
        print("⚠️  Warning: top_k too small, set to minimum 1")
    
    if config.get("top_k", 0) > 20:
        config["top_k"] = 20
        print("⚠️  Warning: top_k too large, set to maximum 20")
    
    # Validate and create directories
    directories = [
        ("data_dir", config.get("data_dir")),
        ("models_dir", config.get("models_dir")),
    ]
    
    for key, dir_path in directories:
        if dir_path is None:
            print(f"❌ Error: {key} is not configured")
            continue
        
        path = Path(dir_path)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
                print(f"✓ Created directory: {path}")
            except Exception as e:
                print(f"❌ Error: Failed to create directory {path}: {e}")
    
    # Set derived paths
    data_dir = Path(config.get("data_dir", ""))
    config["rag_index_dir"] = str(data_dir / "rag_index")
    config["docs_dir"] = str(data_dir / "docs")
    config["logs_dir"] = str(data_dir / "logs")
    
    return config


def print_config_summary(config: Dict[str, Any]):
    """
    Print configuration summary for debugging.
    """
    print("🔧 SYNAPSE Configuration Summary")
    print("=" * 50)
    
    print(f"\nEnvironment: {config.get('environment', 'unknown')}")
    print(f"Data Directory: {config.get('data_dir')}")
    print(f"Models Directory: {config.get('models_dir')}")
    
    print(f"\nRAG Settings:")
    print(f"  Chunk Size: {config.get('chunk_size')}")
    print(f"  Chunk Overlap: {config.get('chunk_overlap')}")
    print(f"  Top K: {config.get('top_k')}")
    print(f"  Min Retrieval Score: {config.get('min_retrieval_score')}")
    
    print(f"\nModels:")
    print(f"  Embedding: {config.get('embedding_model')}")
    print(f"  Chat: {config.get('chat_model')}")
    
    print(f"\nServer:")
    print(f"  Host: {config.get('mcp_host')}")
    print(f"  Port: {config.get('mcp_port')}")
    
    print("\n" + "=" * 50)
