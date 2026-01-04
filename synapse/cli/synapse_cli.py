"""
SYNAPSE CLI: Unified Command-Line Interface

This module provides main CLI entry point for synapse.
Commands are organized into logical groups for better user experience.

Usage:
    synapse start          # Start Synapse server
    synapse stop           # Stop Synapse server
    synapse status         # Check system status
    synapse ingest <path>  # Ingest documents
    synapse query <text>    # Query knowledge base
    synapse setup          # First-time setup
    synapse models list    # Manage models
"""

import subprocess
from pathlib import Path
from typing import Optional
from synapse.cli.commands import start, stop, status, ingest, query, setup, models

# CLI app with rich styling
app = typer.Typer(
    name="synapse",
    help="SYNAPSE: Your Data Meets Intelligence - Local RAG System for AI Agents",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich"
)

# Start command
app.command()(start.start)

# Stop command
app.command()(stop.stop)

# Status command
app.command()(status.check_status)

# Ingest command
app.command()(ingest.ingest_files)

# Query command
app.command()(query.query_knowledge)

# Setup command
app.command()(setup.run_setup)

# Models subcommand
models_app = typer.Typer(help="Model management commands")


@models_app.command("list")
def models_list():
    """List available and installed models."""
    print("📦 Available Models:")
    print("=" * 50)
    
    print("\nembedding (BGE-M3):")
    print("  Name: bge-m3-q8_0.gguf")
    print("  Size: ~730 MB")
    print("  Status: Not installed")
    print("  Description: BGE-M3 embedding model for semantic search")
    print("  HuggingFace: BAAI/bge-m3/gguf/bge-m3-q8_0.gguf")
    
    print("\nchat (Gemma-3 1B):")
    print("  Name: gemma-3-1b-it-UD-Q4_K_XL.gguf")
    print("  Size: ~400 MB")
    print("  Status: Not installed")
    print("  Description: Gemma-3 1B chat model for local chat")
    print("  HuggingFace: google/gemma-3-1b-it/gguf/gemma-3-1b-it-UD-Q4_K_XL.gguf")


@models_app.command("download")
def models_download(
    model_name: str = typer.Argument(..., help="Model name to download"),
    force: bool = typer.Option(False, "--force", "-f", help="Force re-download")
):
    """Download model from HuggingFace."""
    print(f"📥 Downloading {model_name}...")
    print("⚠️  Model download functionality coming in Phase 2 (Model Bundling)")
    print("  For now, please download manually:")
    print(f"   1. Visit HuggingFace to get download URL")
    print("  2. Download model file")
    print("  3. Place in: ~/.synapse/models/")


@models_app.command("verify")
def models_verify():
    """Verify installed model integrity."""
    print("🔍 Verifying Models:")
    print("=" * 50)
    print("⚠️  Model verification coming in Phase 2 (Model Bundling)")
    print("  This will validate model file sizes and checksums")


@models_app.command("remove")
def models_remove(
    model_name: str = typer.Argument(..., help="Model name to remove")
):
    """Remove installed model."""
    print(f"🗑️  Removing {model_name}...")
    print("⚠️  Model removal functionality coming in Phase 2 (Model Bundling)")


# Add models subcommand to main app
app.add_typer(models_app, name="models")


def main():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    main()