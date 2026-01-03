#!/usr/bin/env python3
"""
Test MCP server to verify it works correctly.
"""

import json
import subprocess
import sys
import os

# Set environment
os.environ['RAG_DATA_DIR'] = '/home/dietpi/pi-rag/data'

def test_mcp_server():
    """Test MCP server by sending JSON-RPC requests."""

    print("=" * 60)
    print("Testing RAG MCP Server")
    print("=" * 60)
    print()

    # Start MCP server process
    proc = subprocess.Popen(
        [sys.executable, '-m', 'mcp_server.rag_server'],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )

    try:
        # Step 1: Initialize
        print("Step 1: Initializing MCP server...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        proc.stdin.write(json.dumps(init_request) + "\n")
        proc.stdin.flush()

        # Read response
        response = proc.stdout.readline()
        init_response = json.loads(response)
        print(f"✓ Initialized: {init_response.get('result', {}).get('serverInfo', {}).get('name', 'Unknown')}")
        print()

        # Step 2: Send initialized notification
        print("Step 2: Sending initialized notification...")
        initialized = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        proc.stdin.write(json.dumps(initialized) + "\n")
        proc.stdin.flush()
        print("✓ Initialized notification sent")
        print()

        # Step 3: List tools
        print("Step 3: Listing available tools...")
        list_tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        proc.stdin.write(json.dumps(list_tools_request) + "\n")
        proc.stdin.flush()

        # Read response
        response = proc.stdout.readline()
        tools_response = json.loads(response)

        if 'result' in tools_response:
            tools = tools_response['result'].get('tools', [])
            print(f"✓ Found {len(tools)} tools:")
            for tool in tools:
                print(f"  - {tool.get('name')}: {tool.get('description', 'No description')}")
        else:
            print(f"✗ Error: {tools_response.get('error')}")
            return False
        print()

        # Step 4: Test list_projects
        print("Step 4: Testing rag.list_projects...")
        list_projects_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "rag.list_projects",
                "arguments": {}
            }
        }
        proc.stdin.write(json.dumps(list_projects_request) + "\n")
        proc.stdin.flush()

        # Read response
        response = proc.stdout.readline()
        projects_response = json.loads(response)

        if 'result' in projects_response:
            content = projects_response['result'].get('content', [])
            if content and len(content) > 0:
                data = json.loads(content[0].get('text', '{}'))
                print(f"✓ Projects: {data.get('message', 'No message')}")
            else:
                print("✓ No content in response")
        else:
            print(f"✗ Error: {projects_response.get('error')}")
        print()

        # Step 5: Test with a real file
        print("Step 5: Testing rag.ingest_file with README.md...")
        test_file = "/home/dietpi/pi-rag/README.md"
        if os.path.exists(test_file):
            ingest_request = {
                "jsonrpc": "2.0",
                "id": 4,
                "method": "tools/call",
                "params": {
                    "name": "rag.ingest_file",
                    "arguments": {
                        "project_id": "pi-rag",
                        "file_path": test_file,
                        "source_type": "file",
                        "metadata": {
                            "test": "true",
                            "scope": "full_project"
                        }
                    }
                }
            }
            proc.stdin.write(json.dumps(ingest_request) + "\n")
            proc.stdin.flush()

            # Read response (might take a while due to ingestion)
            response = proc.stdout.readline()
            ingest_response = json.loads(response)

            if 'result' in ingest_response:
                content = ingest_response['result'].get('content', [])
                if content and len(content) > 0:
                    data = json.loads(content[0].get('text', '{}'))
                    if data.get('status') == 'success':
                        print(f"✓ Ingested {data.get('file_path')}")
                        print(f"  Chunks: {data.get('chunk_count')}")
                        print(f"  Doc ID: {data.get('doc_id')}")
                    else:
                        print(f"✗ Ingestion failed: {data.get('message')}")
                else:
                    print("✗ No content in response")
            else:
                print(f"✗ Error: {ingest_response.get('error')}")
        else:
            print(f"⚠ Test file not found: {test_file}")
        print()

        # Step 6: List sources
        print("Step 6: Testing rag.list_sources...")
        list_sources_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "rag.list_sources",
                "arguments": {
                    "project_id": "pi-rag"
                }
            }
        }
        proc.stdin.write(json.dumps(list_sources_request) + "\n")
        proc.stdin.flush()

        # Read response
        response = proc.stdout.readline()
        sources_response = json.loads(response)

        if 'result' in sources_response:
            content = sources_response['result'].get('content', [])
            if content and len(content) > 0:
                data = json.loads(content[0].get('text', '{}'))
                print(f"✓ Sources: {data.get('message', 'No message')}")
                print(f"  Total: {data.get('total', 0)} sources")
            else:
                print("✓ No content in response")
        else:
            print(f"✗ Error: {sources_response.get('error')}")
        print()

        print("=" * 60)
        print("✓ MCP Server Test Completed Successfully!")
        print("=" * 60)

        return True

    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Cleanup
        try:
            proc.stdin.close()
            proc.terminate()
            proc.wait(timeout=5)
        except:
            proc.kill()


if __name__ == "__main__":
    success = test_mcp_server()
    sys.exit(0 if success else 1)
