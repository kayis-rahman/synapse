#!/usr/bin/env python3
"""
MCP Server Connection Test - Robust Version

Tests MCP server connectivity and handles initialization properly.
"""

import subprocess
import json


def test_server_startup() -> bool:
    """Test if MCP server can start and respond."""
    print("Testing MCP Server Startup...")
    print("-" * 60)

    # Try to ping server
    print("\n1. Sending ping to server...")
    try:
        # Send empty params (just to test connection)
        ping_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "ping",
            "params": {}
        }

        # Send request
        process = subprocess.Popen(
            [sys.executable, "-m", "mcp_server.rag_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=5
        )

        # Get output
        stdout, stderr = process.communicate()

        # Parse output (skip empty lines)
        output_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        output = '\n'.join(output_lines)

        # Check for response
        if output:
            print(f"✓ Server responded")
            return True
        else:
            print(f"✗ Server not responding")
            print(f"  Stderr: {stderr}")
            return False

    except subprocess.TimeoutExpired:
        print(f"✗ Server timeout (5s exceeded)")
        return False
    except Exception as e:
        print(f"✗ Server error: {str(e)}")
        print(f"  Stderr: {process.stderr}")
        return False


def test_tools_list() -> bool:
    """Test that tools/list endpoint works."""
    print("\n2. Testing tools/list endpoint...")
    try:
        # Send tools/list request
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }

        process = subprocess.Popen(
            [sys.executable, "-m", "mcp_server.rag_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        # Get output
        stdout, stderr = process.communicate()

        # Parse output
        output_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        output = '\n'.join(output_lines)

        # Check for tools list
        if output:
            try:
                response = json.loads(output)

                if "result" in response and "tools" in response["result"]:
                    tools = response["result"]["tools"]
                    print(f"✓ Server responded with {len(tools)} tools")
                    for i, tool in enumerate(tools[:3]):
                        print(f"  {i+1}. {tool.get('name', 'Unknown tool')}")

                    # Verify expected tools
                    expected_tools = ["rag.list_projects", "rag.list_sources", "rag.get_context", "rag.search", "rag.ingest_file", "rag.add_fact", "rag.add_episode"]
                    actual_tool_names = [t.get("name", "") for t in tools]

                    print(f"  Expected tools: {', '.join(expected_tools)}")

                    # Check if all expected are present
                    for expected_tool in expected_tools:
                        if expected_tool not in actual_tool_names:
                            print(f"  ⚠ Missing expected tool: {expected_tool}")
                    else:
                            print(f"  ✓ All expected tools present")

                    return len(actual_tool_names) >= 7
                else:
                    print(f"✗ Invalid response format: 'result' not found")
                    return False

            except json.JSONDecodeError as e:
                print(f"✗ Failed to parse JSON: {str(e)}")
                print(f"  Output: {output}")
                return False

    except Exception as e:
        print(f"✗ Server error: {str(e)}")
        return False

    except subprocess.TimeoutExpired:
        print(f"✗ Request timeout (10s exceeded)")
        return False


def test_project_list() -> bool:
    """Test rag.list_projects endpoint."""
    print("\n3. Testing rag.list_projects endpoint...")
    try:
        # Send list projects request
        list_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "rag.list_projects",
                "arguments": {}
            }
        }

        process = subprocess.Popen(
            [sys.executable, "-m", "mcp_server.rag_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        # Get output
        stdout, stderr = process.communicate()

        # Parse output
        output_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        output = '\n'.join(output_lines)

        if not output:
            print(f"✗ No output from server")
            return False

        try:
            response = json.loads(output)

            if "result" in response:
                content = response["result"]
                projects = content.get("projects", [])
                project_ids = [p.get("id", "") for p in projects]
                print(f"✓ Found {len(projects)} project(s)")

                return len(projects) >= 1

            else:
                print(f"✗ Invalid response format: 'result' not found")
                return False

        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse JSON: {str(e)}")
                print(f"  Output: {output}")
                return False

    except Exception as e:
        print(f"✗ Server error: {str(e)}")
        return False

    except subprocess.TimeoutExpired:
        print(f"✗ Request timeout (10s exceeded)")
        return False


def test_source_list() -> bool:
    """Test rag.list_sources endpoint."""
    print("\n4. Testing rag.list_sources endpoint...")
    try:
        # Send list sources request
        sources_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "rag.list_sources",
                "arguments": {
                    "project_id": "pi-rag"
                }
            }
        }

        process = subprocess.Popen(
            [sys.executable, "-m", "mcp_server.rag_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=10
        )

        # Get output
        stdout, stderr = process.communicate()

        # Parse output
        output_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        output = '\n'.join(output_lines)

        if not output:
            print(f"✗ No output from server")
            return False

        try:
            response = json.loads(output)

            if "result" in response:
                content = response["result"]
                sources = content.get("sources", [])
                total = content.get("total", 0)

                print(f"✓ Found {total} sources")

                if total >= 50:
                    print(f"  ✓ Expected 50+ sources (from ingestion)")
                    return True
                else:
                    print(f"  ⚠ Found {total} sources (expected 50+)")

                return False

            else:
                print(f"✗ Invalid response format: 'result' not found")
                return False

        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse JSON: {str(e)}")
            print(f"  Output: {output}")
            return False

    except Exception as e:
        print(f"✗ Server error: {str(e)}")
        return False

    except subprocess.TimeoutExpired:
        print(f"✗ Request timeout (10s exceeded)")
        return False


def test_context_retrieval() -> bool:
    """Test rag.get_context endpoint."""
    print("\n5. Testing rag.get_context endpoint...")
    try:
        # Send get context request
        context_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "tools/call",
            "params": {
                "name": "rag.get_context",
                "arguments": {
                    "project_id": "pi-rag",
                    "query": "RAG system architecture",
                    "context_type": "semantic",
                    "max_results": 5
                }
            }
        }

        process = subprocess.Popen(
            [sys.executable, "-m", "mcp_server.rag_server"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=15  # Longer timeout for context retrieval
        )

        # Get output
        stdout, stderr = process.communicate()

        # Parse output
        output_lines = [line.strip() for line in stdout.split('\n') if line.strip()]
        output = '\n'.join(output_lines)

        if not output:
            print(f"✗ No output from server")
            return False

        try:
            response = json.loads(output)

            if "result" in response:
                content = response["result"]

                # Check for context types
                context_types = list(content.keys())

                print(f"✓ Context types: {', '.join(context_types)}")

                if len(context_types) >= 1:
                    print(f"  ✓ Got context data")
                    return True
                else:
                    print(f"✗ No context types in response")
                    return False

            else:
                print(f"✗ Invalid response format: 'result' not found")
                return False

        except json.JSONDecodeError as e:
            print(f"✗ Failed to parse JSON: {str(e)}")
            print(f"  Output: {output}")
            return False

    except Exception as e:
        print(f"✗ Server error: {str(e)}")
        return False

    except subprocess.TimeoutExpired:
        print(f"✗ Request timeout (15s exceeded)")
        return False


def main():
    """Run all connection tests."""
    print("=" * 70)
    print("MCP Server Connection Test")
    print("=" * 70)
    print()

    # Track test results
    tests = {
        "server_startup": test_server_startup(),
        "tools_list": test_tools_list(),
        "project_list": test_project_list(),
        "source_list": test_source_list(),
        "context_retrieval": test_context_retrieval()
    }

    passed = sum(1 for t in tests.values() if t)
    total = len(tests)

    # Print summary
    print()
    print("Test Results Summary:")
    print("=" * 70)
    print(f"Total Tests: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print()
    print("=" * 70)

    if passed == total:
        print("✓ ALL TESTS PASSED - MCP Server is working correctly!")
        print()
        print("Next: Ready for Phase 2 improvements")
    else:
        print(f"✗ {passed}/{total} tests passed")
        print()
        print("Note: Some tests may have timed out - re-run to verify")
        print()
        print("=" * 70)

    # Exit with appropriate code
    sys.exit(0 if passed == total else 1)
