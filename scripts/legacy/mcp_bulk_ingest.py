#!/usr/bin/env python3
"""
Bulk Ingest Script - Ingest all pi-rag files via MCP protocol.

This script:
1. Connects to RAG MCP server
2. Reads file list
3. Ingests each file sequentially via rag.ingest_file
4. Tracks progress and errors
5. Generates summary report
"""

import json
import subprocess
import sys
import os
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
from tqdm import tqdm

# Configuration
PROJECT_ID = "pi-rag"
FILES_LIST = os.environ.get("FILES_LIST", "/tmp/files_to_ingest.txt")
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
MAX_RETRIES = 3

# Source type mapping by extension
SOURCE_TYPE_MAP = {
    # Code files
    '.py': 'code',
    '.js': 'code',
    '.ts': 'code',
    '.jsx': 'code',
    '.tsx': 'code',
    '.java': 'code',
    '.cpp': 'code',
    '.c': 'code',
    '.h': 'code',
    '.sh': 'code',
    '.bash': 'code',

    # Documentation and config files
    '.md': 'file',
    '.txt': 'file',
    '.json': 'file',
    '.yaml': 'file',
    '.yml': 'file',
    '.toml': 'file',
    '.ini': 'file',
}


def get_source_type(file_path: str) -> str:
    """Determine source type based on file extension."""
    ext = Path(file_path).suffix.lower()
    return SOURCE_TYPE_MAP.get(ext, 'file')


def get_file_metadata(file_path: str) -> Dict[str, Any]:
    """Generate metadata for a file."""
    path = Path(file_path)

    # Relative path from project root
    project_root = Path('/home/dietpi/pi-rag')
    relative_path = str(path.relative_to(project_root)) if path.is_relative_to(project_root) else file_path

    # Determine directory category
    if relative_path.startswith('rag/'):
        category = 'core_rag'
    elif relative_path.startswith('api/'):
        category = 'api'
    elif relative_path.startswith('mcp_server/'):
        category = 'mcp_server'
    elif relative_path.startswith('scripts/'):
        category = 'scripts'
    elif relative_path.startswith('configs/'):
        category = 'config'
    elif relative_path.startswith('data/'):
        category = 'data'
    else:
        category = 'root'

    return {
        "project": PROJECT_ID,
        "ingested_at": datetime.utcnow().isoformat(),
        "scope": "full_project",
        "source_type": get_source_type(file_path),
        "category": category,
        "relative_path": relative_path,
        "file_name": path.name,
        "extension": path.suffix.lower(),
    }


class MCPClient:
    """Simple MCP client for RAG server."""

    def __init__(self):
        self.proc = None

    def connect(self) -> bool:
        """Connect to MCP server."""
        self.proc = subprocess.Popen(
            [sys.executable, '-m', 'mcp_server.rag_server'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1
        )

        # Initialize
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "bulk-ingest-client",
                    "version": "1.0.0"
                }
            }
        }

        self._send(init_request)
        response = self._read_response()

        if 'error' in response:
            print(f"✗ Failed to initialize: {response['error']}")
            return False

        # Send initialized notification
        initialized = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        self._send(initialized)
        return True

    def _send(self, message: Dict[str, Any]):
        """Send message to server."""
        if self.proc and self.proc.stdin:
            self.proc.stdin.write(json.dumps(message) + "\n")
            self.proc.stdin.flush()

    def _read_response(self) -> Dict[str, Any]:
        """Read response from server."""
        if self.proc and self.proc.stdout:
            line = self.proc.stdout.readline()
            if line:
                return json.loads(line.strip())
        return {}

    def ingest_file(self, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Ingest a file via MCP."""
        request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {
                "name": "rag.ingest_file",
                "arguments": {
                    "project_id": PROJECT_ID,
                    "file_path": file_path,
                    "source_type": metadata.get("source_type", "file"),
                    "metadata": metadata
                }
            }
        }

        self._send(request)
        response = self._read_response()

        if 'result' in response:
            content = response['result'].get('content', [])
            if content and len(content) > 0:
                data = json.loads(content[0].get('text', '{}'))
                return {
                    "success": True,
                    "data": data
                }
            else:
                return {
                    "success": False,
                    "error": "No content in response"
                }
        else:
            return {
                "success": False,
                "error": response.get('error', {}).get('message', 'Unknown error')
            }

    def list_sources(self) -> Dict[str, Any]:
        """List all sources."""
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "rag.list_sources",
                "arguments": {
                    "project_id": PROJECT_ID
                }
            }
        }

        self._send(request)
        response = self._read_response()

        if 'result' in response:
            content = response['result'].get('content', [])
            if content and len(content) > 0:
                data = json.loads(content[0].get('text', '{}'))
                return data
        return {}

    def close(self):
        """Close connection."""
        if self.proc:
            try:
                self.proc.stdin.close()
                self.proc.terminate()
                self.proc.wait(timeout=5)
            except:
                self.proc.kill()


def ingest_file_with_retry(client: MCPClient, file_path: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
    """Ingest file with retry logic."""
    for attempt in range(MAX_RETRIES):
        result = client.ingest_file(file_path, metadata)

        if result['success']:
            return result

        # Retry on failure
        if attempt < MAX_RETRIES - 1:
            print(f"  ⚠ Retry {attempt + 2}/{MAX_RETRIES}...")
            import time
            time.sleep(1 * (attempt + 1))  # Exponential backoff

    return result


def main():
    """Main ingestion process."""
    print("=" * 70)
    print("BULK INGESTION: pi-rag Project Files")
    print("=" * 70)
    print()

    # Read file list
    if not os.path.exists(FILES_LIST):
        print(f"✗ File list not found: {FILES_LIST}")
        print("Run: find /home/dietpi/pi-rag -type f ... > /tmp/files_to_ingest.txt")
        return 1

    with open(FILES_LIST, 'r') as f:
        files = [line.strip() for line in f if line.strip()]

    print(f"📋 Found {len(files)} files to ingest")
    print(f"🎯 Project ID: {PROJECT_ID}")
    print(f"📊 Chunk size: {CHUNK_SIZE} chars, overlap: {CHUNK_OVERLAP} chars")
    print()

    # Connect to MCP server
    print("🔌 Connecting to MCP server...")
    client = MCPClient()
    if not client.connect():
        print("✗ Failed to connect to MCP server")
        return 1
    print("✓ Connected")
    print()

    # Ingest files
    stats = {
        "total": len(files),
        "success": 0,
        "failed": 0,
        "skipped": 0,
        "total_chunks": 0,
        "errors": []
    }

    print("🚀 Starting ingestion...")
    print()

    # Progress bar
    with tqdm(files, desc="Ingesting", unit="file") as pbar:
        for file_path in pbar:
            # Skip files that don't exist
            if not os.path.exists(file_path):
                stats["skipped"] += 1
                pbar.set_postfix(status="skipped")
                continue

            # Generate metadata
            metadata = get_file_metadata(file_path)
            source_type = metadata.get("source_type", "file")

            # Update progress bar with file type
            pbar.set_postfix(status=source_type[0].upper())

            # Ingest file
            result = ingest_file_with_retry(client, file_path, metadata)

            if result['success']:
                stats["success"] += 1
                stats["total_chunks"] += result['data'].get('chunk_count', 0)
                pbar.set_postfix(status="✓")
            else:
                stats["failed"] += 1
                stats["errors"].append({
                    "file": file_path,
                    "error": result.get('error')
                })
                pbar.set_postfix(status="✗")

    print()

    # Get final sources count
    print("📊 Checking ingested sources...")
    sources_data = client.list_sources()
    sources_count = sources_data.get('total', 0)

    # Close connection
    client.close()

    # Summary report
    print()
    print("=" * 70)
    print("INGESTION SUMMARY")
    print("=" * 70)
    print()
    print(f"Total files: {stats['total']}")
    print(f"✅ Successfully ingested: {stats['success']}")
    print(f"❌ Failed: {stats['failed']}")
    print(f"⏭️  Skipped: {stats['skipped']}")
    print(f"📦 Total chunks created: {stats['total_chunks']}")
    print(f"📋 Total sources in database: {sources_count}")
    print()

    if stats['errors']:
        print("=" * 70)
        print("ERRORS:")
        print("=" * 70)
        for i, error in enumerate(stats['errors'][:10], 1):
            print(f"{i}. {error['file']}")
            print(f"   Error: {error['error']}")
        if len(stats['errors']) > 10:
            print(f"... and {len(stats['errors']) - 10} more errors")
        print()

    print("=" * 70)
    if stats['failed'] == 0:
        print("✅ ALL FILES INGESTED SUCCESSFULLY!")
    else:
        print(f"⚠️  INGESTION COMPLETE WITH {stats['failed']} ERRORS")
    print("=" * 70)

    return 0 if stats['failed'] == 0 else 1


if __name__ == "__main__":
    success = main()
    sys.exit(success)
