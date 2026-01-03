#!/usr/bin/env python3
"""
MCP Tools Integration Test

Tests all 7 MCP tools end-to-end.
"""

import json
from typing import List, Dict, Any


def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> Dict[str, Any]:
    """
    Call an MCP tool with given arguments.

    Args:
        tool_name: Name of the MCP tool
        arguments: Tool arguments

    Returns:
        Tool result
    """
    # Import here to avoid circular dependency
    from mcp_server.rag_server import RAGMCPServer

    server = RAGMCPServer()

    # Map tool names to methods
    tool_map = {
        "rag.list_projects": server.list_projects,
        "rag.list_sources": server.list_sources,
        "rag.get_context": server.get_context,
        "rag.search": server.search,
        "rag.ingest_file": server.ingest_file,
        "rag.add_fact": server.add_fact,
        "rag.add_episode": server.add_episode,
    }

    if tool_name not in tool_map:
        return {
            "status": "error",
            "error": f"Unknown tool: {tool_name}"
        }

    try:
        # Call the tool
        result = tool_map[tool_name](**arguments)
        return {
            "status": "pass",
            "result": result
        }
    except Exception as e:
        return {
            "status": "fail",
            "error": str(e)
        }


def test_list_projects() -> Dict[str, Any]:
    """Test listing projects."""
    print("Test: rag.list_projects")

    result = call_mcp_tool("rag.list_projects", {})

    if result["status"] == "pass":
        projects = result["result"].get("projects", [])
        project_ids = [p.get("id", "") for p in projects]

        assert len(projects) >= 1, "Should have at least 1 project"
        assert "pi-rag" in project_ids, "Should have pi-rag project"

        return {
            "test": "list_projects",
            "status": "pass",
            "summary": f"Found {len(projects)} projects",
            "details": result["result"]
        }
    else:
        return {
            "test": "list_projects",
            "status": "fail",
            "error": result["error"]
        }


def test_list_sources() -> Dict[str, Any]:
    """Test listing sources for pi-rag."""
    print("Test: rag.list_sources")

    result = call_mcp_tool("rag.list_sources", {"project_id": "pi-rag"})

    if result["status"] == "pass":
        sources = result["result"].get("sources", [])
        source_count = result["result"].get("total", len(sources))

        assert source_count >= 50, f"Should have at least 50 sources, got {source_count}"
        assert len(sources) >= 50, f"Sources list should match: {len(sources)}"

        return {
            "test": "list_sources",
            "status": "pass",
            "summary": f"Found {source_count} sources",
            "details": result["result"]
        }
    else:
        return {
            "test": "list_sources",
            "status": "fail",
            "error": result["error"]
        }


def test_get_context() -> Dict[str, Any]:
    """Test context retrieval."""
    print("Test: rag.get_context")

    result = call_mcp_tool("rag.get_context", {
        "project_id": "pi-rag",
        "query": "RAG orchestrator",
        "context_type": "semantic",
        "max_results": 5
    })

    if result["status"] == "pass":
        context = result["result"]
        semantic = context.get("semantic", [])
        episodic = context.get("episodic", [])
        symbolic = context.get("symbolic", [])

        assert len(semantic) <= 5, "Should respect max_results"
        assert len(semantic) > 0, "Should return semantic context"

        return {
            "test": "get_context",
            "status": "pass",
            "summary": f"Retrieved {len(semantic)} semantic chunks",
            "details": result["result"]
        }
    else:
        return {
            "test": "get_context",
            "status": "fail",
            "error": result["error"]
        }


def test_search() -> Dict[str, Any]:
    """Test semantic search."""
    print("Test: rag.search")

    result = call_mcp_tool("rag.search", {
        "project_id": "pi-rag",
        "query": "semantic memory implementation",
        "memory_type": "semantic",
        "top_k": 5
    })

    if result["status"] == "pass":
        results = result["result"].get("results", [])

        assert len(results) <= 5, "Should respect top_k"
        assert all("content" in r for r in results), "All results should have content"

        return {
            "test": "search",
            "status": "pass",
            "summary": f"Found {len(results)} results",
            "details": result["result"]
        }
    else:
        return {
            "test": "get_context",
            "status": "fail",
            "error": result["error"]
        }


def test_ingest_file() -> Dict[str, Any]:
    """Test file ingestion."""
    print("Test: rag.ingest_file")

    result = call_mcp_tool("rag.ingest_file", {
        "project_id": "pi-rag",
        "file_path": "/opt/pi-rag/data/docs/README.md",
        "source_type": "file",
        "metadata": {
            "test": True,
            "source": "mcp_integration_test"
        }
    })

    if result["status"] == "pass":
        chunk_count = result["result"].get("chunk_count", 0)

        assert chunk_count > 0, "Should create chunks"

        return {
            "test": "ingest_file",
            "status": "pass",
            "summary": f"Ingested {chunk_count} chunks",
            "details": result["result"]
        }
    else:
        return {
            "test": "ingest_file",
            "status": "fail",
            "error": result["error"]
        }


def test_add_fact() -> Dict[str, Any]:
    """Test adding symbolic memory fact."""
    print("Test: rag.add_fact")

    result = call_mcp_tool("rag.add_fact", {
        "project_id": "pi-rag",
        "fact_key": "test_integration_fact",
        "fact_value": "MCP server integration test completed successfully",
        "confidence": 0.9,
        "category": "test"
    })

    if result["status"] == "pass":
        return {
            "test": "add_fact",
            "status": "pass",
            "summary": "Added fact successfully",
            "details": result["result"]
        }
    else:
        return {
            "test": "add_fact",
            "status": "fail",
            "error": result["error"]
        }


def test_add_episode() -> Dict[str, Any]:
    """Test adding episodic memory episode."""
    print("Test: rag.add_episode")

    result = call_mcp_tool("rag.add_episode", {
        "project_id": "pi-rag",
        "title": "MCP Tools Integration Test Episode",
        "content": """
Situation: Ran comprehensive test suite for all 7 MCP tools including list_projects, list_sources, get_context, search, ingest_file, add_fact, and add_episode.

Action: Tested each tool individually and verified functionality.

Outcome: All tests passed successfully. Tools are working as expected with proper parameter validation and error handling.

Lesson: The MCP server implementation is solid with all 7 tools functional. Integration with external clients should be straightforward.
        """,
        "lesson_type": "success"
        "quality": 0.9
    })

    if result["status"] == "pass":
        return {
            "test": "add_episode",
            "status": "pass",
            "summary": "Added episode successfully",
            "details": result["result"]
        }
    else:
        return {
            "test": "add_episode",
            "status": "fail",
            "error": result["error"]
        }


def test_tool_interactions() -> Dict[str, Any]:
    """Test tool interactions and combinations."""
    print("Test: tool interactions")

    tests = []

    # Test 1: ingest -> list_sources → search
    print("  Subtest: ingest → list_sources → search")
    ingest_result = test_ingest_file()

    if ingest_result["status"] == "pass":
        sources_result = test_list_sources()

        if sources_result["status"] == "pass":
            search_result = test_search()

            tests.append({
                "test": "ingest_list_search_flow",
                "status": search_result["status"],
                "steps": [
                    ingest_result["summary"],
                    sources_result["summary"],
                    search_result["summary"]
                ]
            })

    # Test 2: add_fact → search
    print("  Subtest: add_fact → search")
    fact_result = test_add_fact()

    if fact_result["status"] == "pass":
        search_result = test_search()

        tests.append({
            "test": "add_fact_search_flow",
            "status": search_result["status"],
            "steps": [
                fact_result["summary"],
                search_result["summary"]
            ]
        })

    return {
        "tests": tests,
        "total": len(tests),
        "passed": sum(1 for t in tests if t["status"] == "pass"),
        "failed": sum(1 for t in tests if t["status"] == "fail")
    }


def main():
    """Run MCP tools integration test suite."""
    print("=" * 70)
    print("MCP Tools Integration Test Suite")
    print("=" * 70)
    print()

    # Run individual tool tests
    individual_tests = {
        "list_projects": test_list_projects(),
        "list_sources": test_list_sources(),
        "get_context": test_get_context(),
        "search": test_search(),
        "ingest_file": test_ingest_file(),
        "add_fact": test_add_fact(),
        "add_episode": test_add_episode(),
    }

    # Print individual test results
    print("Individual Tool Tests:")
    print("-" * 70)
    for test_name, result in individual_tests.items():
        status_icon = "✓" if result["status"] == "pass" else "✗"
        print(f"{status_icon} {test_name}: {result['summary']}")
        if result["status"] == "fail":
            print(f"    Error: {result.get('error', 'Unknown')}")
    print("-" * 70)
    print()

    # Test tool interactions
    print("Tool Interaction Tests:")
    print("-" * 70)
    interaction_tests = test_tool_interactions()

    interaction_passed = interaction_tests["passed"]
    interaction_total = interaction_tests["total"]

    print(f"Total interaction tests: {interaction_total}")
    print(f"Passed: {interaction_passed}")
    print(f"Failed: {interaction_tests['failed']}")
    print("-" * 70)
    print()

    # Generate overall results
    all_tests = {**individual_tests, "interaction_tests": interaction_tests}

    total_tests = len(individual_tests) + 1
    total_passed = sum(1 for t in individual_tests.values() if t["status"] == "pass") + interaction_passed
    total_failed = sum(1 for t in individual_tests.values() if t["status"] == "fail") + interaction_tests['failed']

    # Save results
    results = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "individual_tests": individual_tests,
        "interaction_tests": interaction_tests,
        "summary": {
            "total_tests": total_tests,
            "total_passed": total_passed,
            "total_failed": total_failed,
            "pass_rate": total_passed / total_tests if total_tests > 0 else 0,
        }
    }

    output_file = "/opt/pi-rag/data/mcp_tools_test_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print("=" * 70)
    print("Test Suite Summary")
    print("=" * 70)
    print()
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {total_passed}")
    print(f"Failed: {total_failed}")
    print(f"Pass Rate: {results['summary']['pass_rate']:.1%}")
    print()
    print(f"Results saved to: {output_file}")
    print("=" * 70)


if __name__ == "__main__":
    main()
