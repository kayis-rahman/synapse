#!/usr/bin/env python3
"""
Test remote file ingestion functionality.
"""

import os
import sys
import json
from pathlib import Path

# Add to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.rag_server import RAGMemoryBackend


def test_remote_ingestion():
    """Test remote file ingestion with full paths."""

    print("Testing Remote File Ingestion")
    print("=" * 60)

    backend = RAGMemoryBackend()
    upload_dir = backend._ensure_upload_directory()

    # Create test file
    test_content = """# Test Document
This is a test document for remote ingestion.

## Section 1
Test content here.

## Section 2
More test content.
"""

    test_file = os.path.join(upload_dir, "test-remote-ingest.md")

    # Write test file
    print(f"\nCreating test file: {test_file}")
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write(test_content)

    print(f"File size: {os.path.getsize(test_file)} bytes")

    # Test ingestion
    print(f"\nTesting ingestion of: {test_file}")

    try:
        import asyncio

        async def run_test():
            result = await backend.ingest_file(
                project_id="test-project",
                file_path=test_file,
                source_type="file",
                metadata={"test": True}
            )
            print(f"\nResult: {json.dumps(result, indent=2)}")

            # Verify ingestion
            if result.get("status") == "success":
                print("\n✅ Ingestion successful!")
            else:
                print(f"\n❌ Ingestion failed: {result.get('error', 'unknown')}")

        asyncio.run(run_test())

    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()

    # Cleanup
    try:
        if os.path.exists(test_file):
            os.remove(test_file)
            print(f"\nCleaned up test file: {test_file}")
    except Exception as e:
        print(f"\n⚠ Failed to clean up test file: {e}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_remote_ingestion()
