#!/usr/bin/env python3
"""
Test MCP Server - Verify all 7 tools work correctly.

This script tests the MCP server by:
1. Listing available tools
2. Testing each tool with sample data
3. Verifying the authority hierarchy
4. Checking error handling
"""

import asyncio
import json
import os
import sys
import tempfile
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.rag_server import RAGMemoryBackend, tools


class Colors:
    """Terminal colors for output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'


def print_success(msg: str):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {msg}{Colors.END}")


def print_error(msg: str):
    """Print error message."""
    print(f"{Colors.RED}✗ {msg}{Colors.END}")


def print_info(msg: str):
    """Print info message."""
    print(f"{Colors.BLUE}ℹ {msg}{Colors.END}")


def print_header(msg: str):
    """Print header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{msg}{Colors.END}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.END}\n")


def print_test(msg: str):
    """Print test message."""
    print(f"{Colors.YELLOW}Testing: {msg}{Colors.END}")


async def test_list_tools():
    """Test that all 7 tools are registered."""
    print_header("TEST 1: List Available Tools")

    print_test("Checking number of tools...")
    print_info(f"Found {len(tools)} tools")

    expected_tools = [
        "rag.list_projects",
        "rag.list_sources",
        "rag.get_context",
        "rag.search",
        "rag.ingest_file",
        "rag.add_fact",
        "rag.add_episode"
    ]

    print_test("Verifying tool names...")
    tool_names = [t.name for t in tools]
    for expected_tool in expected_tools:
        if expected_tool in tool_names:
            print_success(f"Tool '{expected_tool}' found")
        else:
            print_error(f"Tool '{expected_tool}' MISSING")
            return False

    print_success("All 7 tools present!")
    return True


async def test_list_projects():
    """Test listing projects."""
    print_header("TEST 2: List Projects")

    backend = RAGMemoryBackend()

    print_test("Calling list_projects()...")
    try:
        result = await backend.list_projects()

        print_info(f"Result: {json.dumps(result, indent=2)}")

        if result and "projects" in result:
            print_success(f"Found {result['total']} projects")
            return True
        else:
            print_error("Invalid result format")
            return False

    except Exception as e:
        print_error(f"Failed: {e}")
        return False


async def test_add_fact():
    """Test adding a symbolic memory fact (authoritative)."""
    print_header("TEST 3: Add Symbolic Fact")

    backend = RAGMemoryBackend()

    print_test("Adding symbolic fact...")
    try:
        result = await backend.add_fact(
            project_id="project",  # Valid scope: session, project, user, org
            fact_key="test_framework",
            fact_value="pytest",
            confidence=0.9,
            category="preference"
        )

        print_info(f"Result: {json.dumps(result, indent=2)}")

        if result and "status" in result and result["status"] == "success":
            print_success("Symbolic fact added successfully")
            return True
        else:
            print_error("Invalid result format")
            return False

    except Exception as e:
        print_error(f"Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_add_episode():
    """Test adding an episodic memory episode (advisory)."""
    print_header("TEST 4: Add Episodic Episode")

    backend = RAGMemoryBackend()

    print_test("Adding episodic episode...")
    try:
        result = await backend.add_episode(
            project_id="test-project",
            title="Test Episode",
            content="Situation: Testing MCP server\nAction: Called add_episode\nOutcome: Success!\nLesson: Episodes work correctly",
            lesson_type="success",
            quality=0.8
        )

        print_info(f"Result: {json.dumps(result, indent=2)}")

        if result and "status" in result and result["status"] == "success":
            print_success("Episodic episode added successfully")
            return True
        else:
            print_error("Invalid result format")
            return False

    except Exception as e:
        print_error(f"Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_ingest_file():
    """Test ingesting a file into semantic memory."""
    print_header("TEST 5: Ingest File")

    backend = RAGMemoryBackend()

    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
        f.write("# Test Document\n\n")
        f.write("This is a test document for the MCP server.\n")
        f.write("It contains multiple paragraphs.\n\n")
        f.write("## Section 1\n\n")
        f.write("First section content.\n")
        temp_file_path = f.name

    try:
        print_test(f"Ingesting file: {temp_file_path}...")
        result = await backend.ingest_file(
            project_id="test-project",
            file_path=temp_file_path,
            source_type="file",
            metadata={"test": "true"}
        )

        print_info(f"Result: {json.dumps(result, indent=2)}")

        if result and "status" in result and result["status"] == "success":
            print_success("File ingested successfully")
            return True
        else:
            print_error("Invalid result format")
            return False

    except Exception as e:
        print_error(f"Failed: {e}")
        import traceback
        traceback.print_exc()
        return False

    finally:
        # Clean up
        if os.path.exists(temp_file_path):
            os.unlink(temp_file_path)


async def test_list_sources():
    """Test listing sources."""
    print_header("TEST 6: List Sources")

    backend = RAGMemoryBackend()

    print_test("Listing sources for test-project...")
    try:
        result = await backend.list_sources(
            project_id="test-project",
            source_type="file"
        )

        print_info(f"Result: {json.dumps(result, indent=2)}")

        if result and "sources" in result:
            print_success(f"Found {result['total']} source(s)")
            return True
        else:
            print_error("Invalid result format")
            return False

    except Exception as e:
        print_error(f"Failed: {e}")
        return False


async def test_get_context():
    """Test getting context with authority hierarchy."""
    print_header("TEST 7: Get Context")

    backend = RAGMemoryBackend()

    print_test("Getting context for project...")
    try:
        result = await backend.get_context(
            project_id="project",  # Valid scope
            context_type="all",
            query="test",
            max_results=10
        )

        print_info(f"Result: {json.dumps(result, indent=2)}")

        # Check result structure
        if result and "symbolic" in result and "episodic" in result and "semantic" in result:
            print_success(f"Retrieved context with 3 memory types")

            # Check authority hierarchy is present
            if len(result.get("symbolic", [])) > 0:
                print_success("Symbolic memory included (authoritative)")
            if len(result.get("episodic", [])) > 0:
                print_success("Episodic memory included (advisory)")
            if len(result.get("semantic", [])) > 0:
                print_success("Semantic memory included (non-authoritative)")

            return True
        else:
            print_error("Invalid result format - expected symbolic, episodic, semantic keys")
            return False

    except Exception as e:
        print_error(f"Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_search():
    """Test semantic search across all memory types."""
    print_header("TEST 8: Semantic Search")

    backend = RAGMemoryBackend()

    print_test("Searching across all memory types...")
    try:
        result = await backend.search(
            project_id="project",  # Valid scope
            query="test framework",
            memory_type="all",
            top_k=5
        )

        print_info(f"Result: {json.dumps(result, indent=2)}")

        if result and "results" in result:
            print_success(f"Found {result['total']} result(s)")
            return True
        else:
            print_error("Invalid result format")
            return False

    except Exception as e:
        print_error(f"Failed: {e}")
        import traceback
        traceback.print_exc()
        return False


async def run_all_tests():
    """Run all tests and report results."""
    print(f"\n{Colors.BOLD}{Colors.GREEN}╔═══════════════════════════════════════════════════════════╗{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}║       MCP SERVER COMPREHENSIVE TEST SUITE                  ║{Colors.END}")
    print(f"{Colors.BOLD}{Colors.GREEN}╚═══════════════════════════════════════════════════════════╝{Colors.END}")

    # Set environment
    os.environ["RAG_DATA_DIR"] = "/home/dietpi/pi-rag/data"

    # Run tests
    tests = [
        ("List Tools", test_list_tools),
        ("List Projects", test_list_projects),
        ("Add Symbolic Fact", test_add_fact),
        ("Add Episodic Episode", test_add_episode),
        ("Ingest File", test_ingest_file),
        ("List Sources", test_list_sources),
        ("Get Context", test_get_context),
        ("Semantic Search", test_search),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            passed = await test_func()
            results.append((test_name, passed))
        except Exception as e:
            print_error(f"Test crashed: {e}")
            import traceback
            traceback.print_exc()
            results.append((test_name, False))

    # Summary
    print_header("TEST SUMMARY")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        if passed:
            print_success(test_name)
        else:
            print_error(test_name)

    print(f"\n{Colors.BOLD}Results: {passed_count}/{total_count} tests passed{Colors.END}")

    if passed_count == total_count:
        print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL TESTS PASSED! MCP Server is working correctly!{Colors.END}")
        return 0
    else:
        print(f"\n{Colors.RED}{Colors.BOLD}⚠️  {total_count - passed_count} test(s) failed{Colors.END}")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
