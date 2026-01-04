"""
SYNAPSE CLI: Unified Command-Line Interface

This module provides the main CLI entry point for synapse.
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
    docker: bool = typer.Option(
        False,
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
    from synapse.cli.commands.start import start_server
    start_server(docker=docker, port=port)


@app.command()
def stop():
    """
    Stop SYNAPSE server.

    Stops the running MCP server (either Docker or native mode).
    """
    from synapse.cli.commands.stop import stop_server
    stop_server()


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
    from synapse.cli.commands.status import check_status
    check_status()


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
    from synapse.cli.commands.ingest import ingest_files
    ingest_files(
        path=path,
        project_id=project_id,
        code_mode=code_mode,
        chunk_size=chunk_size
    )


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
    from synapse.cli.commands.query import query_knowledge
    query_knowledge(
        text=text,
        top_k=top_k,
        output_format=format,
        mode=mode
    )


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
    from synapse.cli.commands.setup import run_setup
    run_setup(force=force, offline=offline)


# Model management subcommands
models_app = typer.Typer(help="Model management commands")


@models_app.command("list")
def models_list():
    """List available and installed models."""
    from synapse.cli.commands.models import list_models
    list_models()


@models_app.command("download")
def models_download(
    model_name: str = typer.Argument(..., help="Model name to download"),
    force: bool = typer.Option(False, "--force", "-f", help="Force re-download")
):
    """Download model from HuggingFace."""
    from synapse.cli.commands.models import download_model
    download_model(model_name=model_name, force=force)


@models_app.command("verify")
def models_verify():
    """Verify installed model integrity."""
    from synapse.cli.commands.models import verify_models
    verify_models()


@models_app.command("remove")
def models_remove(
    model_name: str = typer.Argument(..., help="Model name to remove")
):
    """Remove installed model."""
    from synapse.cli.commands.models import remove_model
    remove_model(model_name=model_name)


# Add models subcommand to main app
app.add_typer(models_app, name="models")


def main():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    main()
