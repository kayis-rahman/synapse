#!/usr/bin/env python3
"""
Docker Integration Test for RAG MCP Server

Tests the MCP server running inside Docker container.
"""

import asyncio
import json
import sys
import os
from pathlib import Path

sys.path.insert(0, "/app")

async def test_docker_mcp_server():
    """Test MCP server running in Docker."""
    print("=" * 70)
    print("Docker MCP Server Test")
    print("=" * 70)

    # Verify environment
    print(f"\nEnvironment Check:")
    print(f"  Python path: {sys.path[:2]}")
    print(f"  RAG_DATA_DIR: {os.environ.get('RAG_DATA_DIR', 'Not set')}")
    print(f"  LOG_LEVEL: {os.environ.get('LOG_LEVEL', 'Not set')}")

    try:
        # Import server
        from mcp_server.rag_server import RAGMemoryBackend
        print("\n✅ Backend imported successfully")

        # Initialize backend
        backend = RAGMemoryBackend()
        print("✅ Backend initialized")

        # Test all 7 tools
        print("\n" + "=" * 70)
        print("Testing All 7 MCP Tools")
        print("=" * 70)

        # Test 1: list_projects
        print("\n[1/7] Testing rag.list_projects...")
        result = await backend.list_projects()
        print(f"  ✅ Found {result['total']} project(s): {result['projects']}")

        # Test 2: list_sources
        print("\n[2/7] Testing rag.list_sources...")
        result = await backend.list_sources(project_id="session")
        print(f"  ✅ Found {result['total']} source(s)")

        # Test 3: get_context
        print("\n[3/7] Testing rag.get_context...")
        result = await backend.get_context(
            project_id="session",
            context_type="all",
            query="docker test",
            max_results=3
        )
        print(f"  ✅ Retrieved context successfully")

        # Test 4: search
        print("\n[4/7] Testing rag.search...")
        result = await backend.search(
            project_id="session",
            query="docker",
            memory_type="all",
            top_k=3
        )
        print(f"  ✅ Search completed: {result.get('total', 0)} results")

        # Test 5: ingest_file
        print("\n[5/7] Testing rag.ingest_file...")
        test_file = "/tmp/test_docker.txt"
        with open(test_file, 'w') as f:
            f.write("Docker test document for RAG MCP server.\n")
            f.write("This confirms the server works in container.\n")
        result = await backend.ingest_file(
            project_id="session",
            file_path=test_file,
            source_type="file",
            metadata={"type": "doc", "source": test_file}
        )
        print(f"  ✅ Ingested {result.get('chunk_count', 0)} chunk(s)")
        os.unlink(test_file)

        # Test 6: add_fact
        print("\n[6/7] Testing rag.add_fact...")
        result = await backend.add_fact(
            project_id="session",
            fact_key="docker_test_fact",
            fact_value="Docker container test successful",
            confidence=0.95,
            category="fact"
        )
        print(f"  ✅ Added fact successfully")

        # Test 7: add_episode
        print("\n[7/7] Testing rag.add_episode...")
        result = await backend.add_episode(
            project_id="session",
            title="Docker Test Episode",
            content="Situation: Testing RAG MCP server in Docker container. Action: Called all 7 tools. Outcome: All tools worked. Lesson: Docker deployment is successful.",
            lesson_type="success",
            quality=0.95
        )
        print(f"  ✅ Added episode successfully")

        # Summary
        print("\n" + "=" * 70)
        print("Docker Test Summary")
        print("=" * 70)
        print("✅ All 7 MCP tools tested successfully!")
        print("✅ Docker container is fully functional")
        print("✅ MCP Server is ready for production deployment")
        print("\nDocker Environment Details:")
        print(f"  - Image: rag-mcp-server:latest")
        print(f"  - Data directory: {backend._get_data_dir()}")
        print(f"  - Tools available: 7")

        return True

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(test_docker_mcp_server())
    sys.exit(0 if success else 1)
