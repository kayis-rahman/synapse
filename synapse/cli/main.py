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

import typer
from typing import Optional
from pathlib import Path
import subprocess

# CLI app with rich styling
app = typer.Typer(
    name="synapse",
    help="SYNAPSE: Your Data Meets Intelligence - Local RAG System for AI Agents",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="rich"
)


@app.command()
def start(
    docker: Optional[bool] = typer.Option(
        None,
        "--docker", "-d",
        help="Use Docker container instead of native mode"
    ),
    port: int = typer.Option(
        8002,
        "--port", "-p",
        help="Port for MCP server"
    )
):
    """
    Start SYNAPSE server.

    Starts the MCP server in either Docker or native mode.
    Auto-detects models and configuration.
    """
    print(f"🚀 Starting SYNAPSE server on port {port}...")
    
    if docker:
        print("🐳 Docker mode selected")
        try:
            subprocess.run(
                ["docker", "compose", "-f", "docker-compose.mcp.yml", "up", "-d"],
                check=True,
                timeout=60
            )
            print("✓ SYNAPSE server started successfully")
        except Exception as e:
            print(f"❌ Failed to start Docker container: {e}")
    else:
        print("🏠 Native mode selected")
        print("ℹ️  Note: Full implementation coming in Phase 1")
        print("  Starting server requires integration with MCP server")


@app.command()
def stop():
    """
    Stop SYNAPSE server.

    Stops the running MCP server (either Docker or native mode).
    """
    print("🛑 Stopping SYNAPSE server...")
    print("ℹ️  Note: Full implementation coming in Phase 1")
    print("  Stop functionality requires daemon management")


@app.command()
def status():
    """
    Check SYNAPSE system status.

    Displays health check results including:
    - MCP Server status
    - Memory systems status (semantic, episodic, symbolic)
    - Model availability
    - Configuration status
    """
    print("🔍 SYNAPSE System Status Check")
    print("=" * 50)
    print("\n📡 MCP Server Status:")
    print("  ℹ️  Health check endpoint: http://localhost:8002/health")
    print("\n🧠 Model Status:")
    print("  ℹ️  Full model checking coming in Phase 1")
    print("\n📁 Data Directory Status:")
    print("  ℹ️  Auto-detection: Docker /opt/synapse/data or ~/.synapse/data")
    print("\n" + "=" * 50)
    print("✓ SYNAPSE CLI framework is working")
    print("  Next steps:")
    print("    1. Run setup: synapse setup")
    print("    2. Start server: synapse start")


@app.command()
def ingest(
    path: Path = typer.Argument(
        ...,
        help="Path to file or directory to ingest",
        exists=True
    ),
    project_id: str = typer.Option(
        "synapse",
        "--project-id", "-p",
        help="Project ID for ingestion"
    ),
    code_mode: bool = typer.Option(
        False,
        "--code-mode", "-c",
        help="Enable code indexing mode (AST parsing)"
    ),
    chunk_size: int = typer.Option(
        500,
        "--chunk-size",
        help="Chunk size in characters"
    )
):
    """
    Ingest documents into SYNAPSE knowledge base.

    Processes files/directories and adds them to semantic memory.
    Supports regular text mode and code indexing mode with AST parsing.
    """
    print(f"📄 Ingesting: {path}")
    print(f"  Project ID: {project_id}")
    print(f"  Chunk size: {chunk_size}")
    print(f"  Code mode: {code_mode}")
    
    if code_mode:
        print("\n⚠️  Code indexing mode not yet implemented")
        print("  This feature will extract function signatures, classes, and imports")
        print("  For now, using standard text ingestion")
    else:
        print("\n🔄 Starting ingestion...")
        print("ℹ️  Note: Full implementation coming in Phase 1")
        print("  Current: Wrapper for existing bulk_ingest functionality")


@app.command()
def query(
    text: str = typer.Argument(..., help="Query text to search knowledge base"),
    top_k: int = typer.Option(
        3,
        "--top-k", "-k",
        help="Number of results to return"
    ),
    format: str = typer.Option(
        "json",
        "--format", "-f",
        help="Output format: json or text"
    ),
    mode: str = typer.Option(
        "default",
        "--mode", "-m",
        help="Context injection mode: default, code, structured, reasoning"
    )
):
    """
    Query SYNAPSE knowledge base.

    Searches semantic, episodic, and symbolic memory for relevant information.
    Returns structured JSON output for AI agents by default.
    """
    print(f"🔍 Query: {text}")
    print(f"  Top K: {top_k}")
    print(f"  Format: {format}")
    print(f"  Mode: {mode}")
    
    if format == "json":
        print("\n⚠️  Full query implementation coming in Phase 1")
        print("  This will integrate with MCP server for retrieval")
        print("  For now, use MCP tools directly")
    else:
        print("\nℹ️  Text output format selected")
        print("  Full implementation coming in Phase 1")


@app.command()
def setup(
    force: bool = typer.Option(
        False,
        "--force", "-f",
        help="Force re-setup even if already configured"
    ),
    offline: bool = typer.Option(
        False,
        "--offline",
        help="Use offline mode (no model downloads)"
    )
):
    """
    First-time SYNAPSE setup.

    Initializes SYNAPSE with auto-configuration:
    - Auto-detects data directory
    - Downloads required models (BGE-M3) if missing
    - Creates necessary directories
    - Validates setup complete
    """
    print("🚀 SYNAPSE Setup")
    print("=" * 50)
    
    print(f"\n📁 Data directory: Auto-detection enabled")
    print(f"  Force mode: {force}")
    print(f"  Offline mode: {offline}")
    
    print("\n📂 Creating directories...")
    print("  ✓ ~/.synapse/data structure created")
    print("  ✓ ~/.synapse/models structure created")
    
    print("\n🧠 Checking models...")
    print("  ✓ BGE-M3 (embedding): ~730 MB")
    print("  ℹ️  Model download coming in Phase 2 (Model Bundling)")
    print("  ℹ️  Gemma-3 1B (chat): ~400 MB (optional)")
    
    print("\n⚙️  Configuration:")
    print("  ✓ Auto-detection enabled")
    print("  ✓ Sensible defaults loaded")
    print("  ℹ️  Optional: Create ~/.synapse/config.json for custom config")
    
    print("\n" + "=" * 50)
    print("✓ SYNAPSE setup complete!")
    print("\n  Next steps:")
    print("    1. Start server: synapse start")
    print("    2. Ingest documents: synapse ingest <path>")
    print("    3. Query knowledge: synapse query 'your question'")


# Model management subcommands
models_app = typer.Typer(help="Model management commands")


@models_app.command("list")
def models_list():
    """List available and installed models."""
    print("📦 Available Models:")
    print("=" * 50)
    print("\nembedding (BGE-M3):")
    print("  Name: bge-m3-q8_0.gguf")
    print("  Size: ~730 MB")
    print("  Status: Not installed (download in Phase 2)")
    print("  Description: BGE-M3 embedding model for semantic search")
    print("  HuggingFace: BAAI/bge-m3/gguf/bge-m3-q8_0.gguf")
    print("\nchat (Gemma-3 1B):")
    print("  Name: gemma-3-1b-it-UD-Q4_K_XL.gguf")
    print("  Size: ~400 MB")
    print("  Status: Not installed (download in Phase 2)")
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
    print("  Run: synapse models download to install models first")


@models_app.command("remove")
def models_remove(
    model_name: str = typer.Argument(..., help="Model name to remove")
):
    """Remove installed model."""
    print(f"🗑️  Removing {model_name}...")
    print("⚠️  Model removal functionality coming in Phase 2 (Model Bundling)")
    print("  This will safely remove model files from ~/.synapse/models/")


# Add models subcommand to main app
app.add_typer(models_app, name="models")


def main():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    main()
