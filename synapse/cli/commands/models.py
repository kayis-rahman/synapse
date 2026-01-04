"""
SYNAPSE CLI: Models Management

Model download and management commands.
"""

import typer
from pathlib import Path
from typing import Optional


# Model registry (will be in synapse/config/models.json in Phase 3)
AVAILABLE_MODELS = {
    "embedding": {
        "name": "bge-m3",
        "file": "bge-m3-q8_0.gguf",
        "size_mb": 730,
        "description": "BGE-M3 embedding model for semantic search",
        "huggingface": "BAAI/bge-m3/gguf/bge-m3-q8_0.gguf"
    },
    "chat": {
        "name": "gemma-3-1b",
        "file": "gemma-3-1b-it-UD-Q4_K_XL.gguf",
        "size_mb": 400,
        "description": "Gemma 3 1B chat model for local chat",
        "huggingface": "google/gemma-3-1b-it/gguf/gemma-3-1b-it-UD-Q4_K_XL.gguf"
    }
}


def get_models_directory() -> Path:
    """Get models directory path."""
    import os
    # Try common locations
    locations = [
        Path("/app/models"),  # Docker
        Path("/opt/synapse/models"),  # Native install
        Path.home() / ".synapse" / "models",  # User home
        Path("~/.synapse/models").expanduser()
    ]
    
    for loc in locations:
        if loc.exists():
            return loc
    
    # Create in user home as fallback
    user_models = Path.home() / ".synapse" / "models"
    user_models.mkdir(parents=True, exist_ok=True)
    return user_models


def list_models():
    """List available and installed models."""
    print("📦 Available Models:")
    print("=" * 50)
    
    models_dir = get_models_directory()
    
    for model_type, model_info in AVAILABLE_MODELS.items():
        model_path = models_dir / model_info["file"]
        installed = model_path.exists()
        
        status = "✓ Installed" if installed else "✗ Not installed"
        size_info = f"{model_info['size_mb']} MB"
        
        print(f"\n{model_type.upper()}:")
        print(f"  Name: {model_info['name']}")
        print(f"  File: {model_info['file']}")
        print(f"  Size: {size_info}")
        print(f"  Description: {model_info['description']}")
        print(f"  Status: {status}")
        
        if installed:
            actual_size_mb = model_path.stat().st_size / (1024 * 1024)
            print(f"  Actual size: {round(actual_size_mb, 2)} MB")


def download_model(
    model_name: str,
    force: bool = False
):
    """
    Download model from HuggingFace.

    Args:
        model_name: Model type to download (embedding or chat)
        force: Force re-download even if already exists
    """
    if model_name not in AVAILABLE_MODELS:
        print(f"❌ Unknown model: {model_name}")
        print(f"   Available models: {', '.join(AVAILABLE_MODELS.keys())}")
        return False
    
    model_info = AVAILABLE_MODELS[model_name]
    models_dir = get_models_directory()
    model_path = models_dir / model_info["file"]
    
    print(f"📥 Downloading {model_info['name']} ({model_info['size_mb']} MB)...")
    print(f"  From: {model_info['huggingface']}")
    
    if model_path.exists() and not force:
        print(f"  ✓ Model already installed")
        print(f"  Use --force to re-download")
        return True
    
    # TODO: Implement actual download using huggingface_hub in Phase 3
    print("\n⚠️  Download functionality coming in Phase 3")
    print("  For now, please download manually:")
    print(f"  1. Visit: https://huggingface.co/{model_info['huggingface'].split('/')[0]}")
    print(f"  2. Download: {model_info['file']}")
    print(f"  3. Place in: {models_dir}")
    
    return False


def verify_models():
    """Verify installed model integrity."""
    print("🔍 Verifying Models:")
    print("=" * 50)
    
    models_dir = get_models_directory()
    all_valid = True
    
    for model_type, model_info in AVAILABLE_MODELS.items():
        model_path = models_dir / model_info["file"]
        
        if not model_path.exists():
            print(f"\n✗ {model_type}: Not installed")
            all_valid = False
            continue
        
        # Check file size
        size_mb = model_path.stat().st_size / (1024 * 1024)
        expected_size = model_info["size_mb"]
        
        # Allow 10% variance
        size_valid = abs(size_mb - expected_size) < (expected_size * 0.1)
        
        status = "✓ Valid" if size_valid else "⚠️  Size mismatch"
        print(f"\n{model_type.upper()}:")
        print(f"  Path: {model_path}")
        print(f"  Expected size: {expected_size} MB")
        print(f"  Actual size: {round(size_mb, 2)} MB")
        print(f"  Status: {status}")
        
        if not size_valid:
            all_valid = False
    
    print("\n" + "=" * 50)
    if all_valid:
        print("✓ All models verified successfully")
    else:
        print("⚠️  Some models need attention")
        print("  Re-download with: synapse models download <model-name> --force")


def remove_model(model_name: str):
    """
    Remove installed model.

    Args:
        model_name: Model type to remove (embedding or chat)
    """
    if model_name not in AVAILABLE_MODELS:
        print(f"❌ Unknown model: {model_name}")
        print(f"   Available models: {', '.join(AVAILABLE_MODELS.keys())}")
        return False
    
    model_info = AVAILABLE_MODELS[model_name]
    models_dir = get_models_directory()
    model_path = models_dir / model_info["file"]
    
    print(f"🗑️  Removing {model_info['name']}...")
    
    if not model_path.exists():
        print(f"  ✗ Model not installed")
        return False
    
    try:
        model_path.unlink()
        print(f"  ✓ Model removed successfully")
        return True
    except Exception as e:
        print(f"  ❌ Failed to remove model: {e}")
        return False
