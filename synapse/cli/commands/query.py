"""
SYNAPSE CLI: Query Command

Query SYNAPSE knowledge base.
"""

import typer
from typing import Optional


def query_knowledge(
    text: str,
    top_k: int = 3,
    output_format: str = "json",
    mode: str = "default"
):
    """
    Query SYNAPSE knowledge base.

    Searches semantic, episodic, and symbolic memory for relevant information.
    Returns structured JSON output for AI agents by default.
    """
    print(f"🔍 Query: {text}")
    print(f"  Top K: {top_k}")
    print(f"  Format: {output_format}")
    print(f"  Mode: {mode}")
    
    if output_format == "json":
        print("\n⚠️  Full query implementation coming in Phase 1")
        print("  This will integrate with MCP server for retrieval")
        print("  For now, use MCP tools directly")
    else:
        print("\nℹ️  Text output format selected")
        print("  Full implementation coming in Phase 1")
    
    # TODO: Integrate with MCP server
    # - Call search endpoint via HTTP
    # - Format results as JSON or text
    # - Apply context injection modes
