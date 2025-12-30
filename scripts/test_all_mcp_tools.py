#!/usr/bin/env python3
"""
Simple test script to verify all 10 MCP tools work correctly.

This tests the RAG MCP server tools without going through the MCP protocol,
directly calling the backend methods.
"""

import asyncio
import os
import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from mcp_server.rag_server import RAGMemoryBackend


class Colors:
    """Terminal colors for output."""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'


def print_header(text):
    """Print a header."""
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_success(text):
    """Print success message."""
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text):
    """Print error message."""
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text):
    """Print info message."""
    print(f"{Colors.YELLOW}ℹ {text}{Colors.RESET}")


async def test_all_tools():
    """Test all 10 MCP tools."""
    print_header("RAG MCP Server - All Tools Test")

    # Initialize backend
    print_info("Initializing RAG Memory Backend...")
    backend = RAGMemoryBackend()
    print_success("Backend initialized")

    test_results = []
    project_id = None

    # Test 1: Create project
    print_header("Test 1: Create Project")
    try:
        result = await backend.create_project("testproj", metadata={"description": "Test project"})
        print_success(f"Created project: {result['project_id']}")
        print_info(f"Project directory: {result['project_dir']}")
        project_id = result['project_id']
        test_results.append(("create_project", True, None))
    except Exception as e:
        print_error(f"Failed to create project: {e}")
        test_results.append(("create_project", False, str(e)))
        # Continue with tests even if create fails

    # Test 2: List projects
    print_header("Test 2: List Projects")
    try:
        result = await backend.list_projects()
        print_success(f"Listed {result['total']} project(s)")
        for project in result['projects']:
            print_info(f"  - {project['project_id']}: {project['name']}")
        test_results.append(("list_projects", True, None))
    except Exception as e:
        print_error(f"Failed to list projects: {e}")
        test_results.append(("list_projects", False, str(e)))

    # Test 3: Get project info
    print_header("Test 3: Get Project Info")
    if project_id is None:
        print_error("Skipping - project_id not available")
        test_results.append(("get_project_info", False, "project_id not available"))
    else:
        try:
            result = await backend.get_project_info(project_id)
            print_success(f"Got info for {result['project_id']}")
            print_info(f"  Name: {result['metadata']['name']}")
            print_info(f"  Stats: {json.dumps(result['stats'], indent=4)}")
            test_results.append(("get_project_info", True, None))
        except Exception as e:
            print_error(f"Failed to get project info: {e}")
            test_results.append(("get_project_info", False, str(e)))

    # Test 4: Add fact (symbolic memory)
    print_header("Test 4: Add Fact (Symbolic Memory)")
    if project_id is None:
        print_error("Skipping - project_id not available")
        test_results.append(("add_fact", False, "project_id not available"))
    else:
        try:
            result = await backend.add_fact(
                project_id,
                "test_fact_key",
                "test_fact_value",
                confidence=0.95,
                category="preference"
            )
            print_success(f"Added fact: {result['fact_id']}")
            print_info(f"  Key: {result.get('key', 'N/A')}")
            print_info(f"  Value: {result.get('value', 'N/A')}")
            print_info(f"  Authority: {result.get('authority', 'N/A')}")
            test_results.append(("add_fact", True, None))
        except Exception as e:
            print_error(f"Failed to add fact: {e}")
            test_results.append(("add_fact", False, str(e)))

    # Test 5: Add episode (episodic memory)
    print_header("Test 5: Add Episode (Episodic Memory)")
    if project_id is None:
        print_error("Skipping - project_id not available")
        test_results.append(("add_episode", False, "project_id not available"))
    else:
        try:
            result = await backend.add_episode(
                project_id,
                "Test Episode",
                "Situation: Testing episodic memory\nAction: Called add_episode\nOutcome: Success\nLesson: Episode was stored",
                lesson_type="success",
                quality=0.9
            )
            print_success(f"Added episode: {result['episode_id']}")
            print_info(f"  Situation: {result.get('situation', 'N/A')}")
            print_info(f"  Lesson: {result.get('lesson', 'N/A')}")
            print_info(f"  Authority: {result.get('authority', 'N/A')}")
            test_results.append(("add_episode", True, None))
        except Exception as e:
            print_error(f"Failed to add episode: {e}")
            test_results.append(("add_episode", False, str(e)))

    # Test 6: Get context
    print_header("Test 6: Get Context")
    if project_id is None:
        print_error("Skipping - project_id not available")
        test_results.append(("get_context", False, "project_id not available"))
    else:
        try:
            result = await backend.get_context(
                project_id,
                context_type="all",
                query="test",
                max_results=5
            )
            print_success(f"Retrieved context")
            print_info(f"  Symbolic facts: {len(result['symbolic'])}")
            print_info(f"  Episodic episodes: {len(result['episodic'])}")
            print_info(f"  Semantic chunks: {len(result['semantic'])}")
            print_info(f"  Message: {result['message']}")
            test_results.append(("get_context", True, None))
        except Exception as e:
            print_error(f"Failed to get context: {e}")
            test_results.append(("get_context", False, str(e)))

    # Test 7: Search
    print_header("Test 7: Search")
    if project_id is None:
        print_error("Skipping - project_id not available")
        test_results.append(("search", False, "project_id not available"))
    else:
        try:
            result = await backend.search(
                project_id,
                query="test",
                memory_type="all",
                top_k=5
            )
            print_success(f"Search completed")
            print_info(f"  Total results: {result['total']}")
            print_info(f"  Top results: {len(result['results'])}")
            for r in result['results'][:2]:
                print_info(f"    - [{r['type']}] {r.get('fact_key', r.get('title', r.get('chunk_id', 'unknown')))}")
            test_results.append(("search", True, None))
        except Exception as e:
            print_error(f"Failed to search: {e}")
            test_results.append(("search", False, str(e)))

    # Test 8: Ingest file
    print_header("Test 8: Ingest File")
    if project_id is None:
        print_error("Skipping - project_id not available")
        test_results.append(("ingest_file", False, "project_id not available"))
    else:
        try:
            # Create a test file
            test_file = "/tmp/test_rag_ingest.txt"
            with open(test_file, 'w') as f:
                f.write("This is a test document for RAG semantic memory.\n")
                f.write("It contains sample text to test the ingestion process.\n")
                f.write("The content should be chunked and stored in ChromaDB.")

            result = await backend.ingest_file(
                project_id,
                test_file,
                source_type="file",
                metadata={"test": "true"}
            )
            print_success(f"Ingested file: {result['file_path']}")
            print_info(f"  Chunks created: {result['chunk_count']}")
            print_info(f"  Document ID: {result['doc_id']}")
            print_info(f"  Authority: {result['authority']}")

            # Clean up
            os.remove(test_file)
            test_results.append(("ingest_file", True, None))
        except Exception as e:
            print_error(f"Failed to ingest file: {e}")
            test_results.append(("ingest_file", False, str(e)))

    # Test 9: List sources
    print_header("Test 9: List Sources")
    if project_id is None:
        print_error("Skipping - project_id not available")
        test_results.append(("list_sources", False, "project_id not available"))
    else:
        try:
            result = await backend.list_sources(project_id)
            print_success(f"Listed {result['total']} source(s)")
            for source in result['sources']:
                print_info(f"  - {source['path']} ({source['type']}): {source['chunk_count']} chunks")
            test_results.append(("list_sources", True, None))
        except Exception as e:
            print_error(f"Failed to list sources: {e}")
            test_results.append(("list_sources", False, str(e)))

    # Test 10: Delete project
    print_header("Test 10: Delete Project")
    if project_id is None:
        print_error("Skipping - project_id not available")
        test_results.append(("delete_project", False, "project_id not available"))
    else:
        try:
            result = await backend.delete_project(project_id)
            print_success(f"Deleted project: {result['project_id']}")
            print_info(f"  Message: {result['message']}")
            test_results.append(("delete_project", True, None))
        except Exception as e:
            print_error(f"Failed to delete project: {e}")
            test_results.append(("delete_project", False, str(e)))

    # Print summary
    print_header("Test Summary")
    passed = sum(1 for _, success, _ in test_results if success)
    total = len(test_results)

    for tool_name, success, error in test_results:
        status = f"{Colors.GREEN}PASSED{Colors.RESET}" if success else f"{Colors.RED}FAILED{Colors.RESET}"
        print(f"  {tool_name:25} {status}")
        if error:
            print(f"    {Colors.RED}Error: {error}{Colors.RESET}")

    print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.RESET}")

    if passed == total:
        print(f"{Colors.GREEN}{Colors.BOLD}All tests passed!{Colors.RESET}")
        return 0
    else:
        print(f"{Colors.RED}{Colors.BOLD}Some tests failed!{Colors.RESET}")
        return 1


if __name__ == "__main__":
    result = asyncio.run(test_all_tools())
    sys.exit(result)
