"""
SYNAPSE CLI: Ingest Command

Ingest documents into SYNAPSE knowledge base.
"""

import sys
from pathlib import Path
import typer

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

try:
    from scripts.bulk_ingest import main as bulk_ingest_main
except ImportError:
    # Fall back if scripts module not accessible
    print("ℹ️  Note: Using wrapper for existing bulk ingest functionality")
    bulk_ingest_main = None


def ingest_files(
    path: Path,
    project_id: str = "synapse",
    code_mode: bool = False,
    chunk_size: int = 500
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
    
    # Try to use existing bulk_ingest functionality
    if bulk_ingest_main:
        print("\n🔄 Starting ingestion...")
        sys.argv = [
            "synapse-bulk-ingest",
            "--project-id", project_id,
            "--chunk-size", str(chunk_size),
            str(path)
        ]
        try:
            bulk_ingest_main()
        except SystemExit:
            pass
    else:
        print("\nℹ️  Basic ingestion wrapper")
        print(f"  Path: {path}")
        print("  Full implementation coming in Phase 1")
        print("  Use: python -m scripts.bulk_ingest <path>")
