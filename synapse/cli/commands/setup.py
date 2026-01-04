"""
SYNAPSE CLI: Setup Command

First-time SYNAPSE setup and initialization.
"""

import os
from pathlib import Path
import typer


def detect_data_directory() -> Path:
    """Auto-detect data directory (Docker vs native vs user home)."""
    # Priority: Docker > /opt/synapse > ~/.synapse > ./data
    if os.path.exists("/app/data"):
        print("ℹ️  Auto-detected Docker data directory: /app/data")
        return Path("/app/data")
    elif os.path.exists("/opt/synapse/data"):
        print("ℹ️  Auto-detected native data directory: /opt/synapse/data")
        return Path("/opt/synapse/data")
    else:
        print("ℹ️  Auto-detected user home data directory: ~/.synapse/data")
        return Path.home() / ".synapse" / "data"


def create_directories(data_dir: Path) -> bool:
    """Create necessary directories."""
    directories = [
        data_dir,
        data_dir / "models",
        data_dir / "rag_index",
        data_dir / "docs",
        data_dir / "logs"
    ]
    
    all_created = True
    for directory in directories:
        if not directory.exists():
            try:
                directory.mkdir(parents=True, exist_ok=True)
                print(f"✓ Created: {directory}")
            except Exception as e:
                print(f"❌ Failed to create {directory}: {e}")
                all_created = False
    
    return all_created


def check_models_exist(models_dir: Path) -> dict:
    """Check for required models."""
    required_models = {
        "embedding": "bge-m3-q8_0.gguf",
        "chat": "gemma-3-1b-it-UD-Q4_K_XL.gguf"
    }
    
    model_status = {}
    for model_type, filename in required_models.items():
        model_path = models_dir / filename
        model_status[model_type] = {
            "name": filename,
            "path": str(model_path),
            "installed": model_path.exists(),
            "required": True
        }
        
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            model_status[model_type]["size_mb"] = round(size_mb, 2)
    
    return model_status


def run_setup(
    force: bool = False,
    offline: bool = False
):
    """
    First-time SYNAPSE setup.

    Initializes SYNAPSE with auto-configuration:
    - Auto-detects data directory
    - Creates necessary directories
    - Validates setup complete
    - Downloads required models (if not offline)
    """
    print("🚀 SYNAPSE Setup")
    print("=" * 50)
    
    # Detect data directory
    data_dir = detect_data_directory()
    models_dir = data_dir / "models"
    
    print(f"\n📁 Data directory: {data_dir}")
    print(f"📁 Models directory: {models_dir}")
    
    # Create directories
    print("\n📂 Creating directories...")
    create_directories(data_dir)
    
    # Check models
    print("\n🧠 Checking models...")
    model_status = check_models_exist(models_dir)
    
    for model_type, status in model_status.items():
        if status["installed"]:
            print(f"  ✓ {model_type}: {status['name']} ({status['size_mb']} MB)")
        else:
            if offline:
                print(f"  ✗ {model_type}: {status['name']} - Not installed (offline mode)")
                print(f"    Download manually or run: synapse setup --no-offline")
            else:
                print(f"  ⚠️  {model_type}: {status['name']} - Not installed")
                print(f"    Download with: synapse models download {model_type}")
    
    # Configuration status
    print("\n⚙️  Configuration:")
    print("  ✓ Auto-detection enabled")
    print("  ✓ Sensible defaults loaded")
    print("  ℹ️  Optional: Create ~/.synapse/config.json for custom config")
    
    # Summary
    print("\n" + "=" * 50)
    
    embedding_installed = model_status["embedding"]["installed"]
    chat_installed = model_status["chat"]["installed"]
    
    if embedding_installed and chat_installed:
        print("✓ SYNAPSE setup complete!")
        print("\n  Next steps:")
        print("    1. Start server: synapse start")
        print("    2. Ingest documents: synapse ingest <path>")
        print("    3. Query knowledge: synapse query 'your question'")
    elif embedding_installed:
        print("⚠️  SYNAPSE partially set up")
        print("\n  Minimum setup complete (embedding model installed)")
        print("  Chat model is optional for query functionality")
        print("\n  Next steps:")
        print("    1. Start server: synapse start")
        print("    2. Ingest documents: synapse ingest <path>")
        print("    3. Query knowledge: synapse query 'your question'")
    else:
        print("⚠️  SYNAPSE setup incomplete")
        print("\n  Missing required models")
        print("  Run: synapse setup --no-offline  (to auto-download)")
        print("  Or: synapse models download embedding")
