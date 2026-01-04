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
app.add_typer(models.app, name="models")

# Main function
def main():
    """Main CLI entry point."""
    app()


if __name__ == "__main__":
    main()
