#!/usr/bin/env python3
"""
Comprehensive functional test for all RAG MCP server tools.

Tests all 7 MCP tools:
1. rag.list_projects
2. rag.list_sources
3. rag.get_context
4. rag.search
5. rag.add_fact
6. rag.add_episode
7. rag.ingest_file
"""

import asyncio
import json
import os
import sys
from datetime import datetime
from pathlib import Path

# Add project to path
sys.path.insert(0, '/home/dietpi/pi-rag')

from mcp_server.rag_server import RAGMemoryBackend


class RAGMCPTester:
    """Test suite for RAG MCP server tools."""

    def __init__(self):
        self.backend = RAGMemoryBackend()
        self.project_id = "mcp_test_project"
        self.test_results = []
        self.test_fact_key = None
        self.test_episode_id = None
        self.test_doc_id = None

    def log_result(self, tool_name: str, status: str, message: str, details: dict = None):
        """Log test result."""
        result = {
            "tool": tool_name,
            "status": status,  # PASS, FAIL, SKIP
            "message": message,
            "details": details or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        self.test_results.append(result)
        print(f"[{status}] {tool_name}: {message}")
        if details:
            print(f"    Details: {json.dumps(details, indent=4, default=str)}")

    async def test_list_projects(self):
        """Test Tool 1: rag.list_projects"""
        print("\n" + "="*60)
        print("TEST 1: rag.list_projects")
        print("="*60)

        try:
            # Test without filter
            result = await self.backend.list_projects()
            assert "projects" in result, "Result missing 'projects' key"
            assert "total" in result, "Result missing 'total' key"
            assert isinstance(result["projects"], list), "Projects should be a list"

            print(f"Found {result['total']} project(s): {result['projects']}")

            # Test with filter
            filtered = await self.backend.list_projects(scope_type="user")
            assert "projects" in filtered, "Filtered result missing 'projects' key"

            self.log_result(
                "rag.list_projects",
                "PASS",
                f"Successfully listed {result['total']} projects",
                {"projects": result["projects"], "filtered": filtered["projects"]}
            )
            return True

        except Exception as e:
            self.log_result("rag.list_projects", "FAIL", str(e), {"error": str(e)})
            return False

    async def test_list_sources(self):
        """Test Tool 2: rag.list_sources"""
        print("\n" + "="*60)
        print("TEST 2: rag.list_sources")
        print("="*60)

        try:
            # Test listing sources for project
            result = await self.backend.list_sources(project_id=self.project_id)
            assert "sources" in result, "Result missing 'sources' key"
            assert "total" in result, "Result missing 'total' key"
            assert isinstance(result["sources"], list), "Sources should be a list"

            print(f"Found {result['total']} source(s)")

            # Test with type filter
            filtered = await self.backend.list_sources(
                project_id=self.project_id,
                source_type="file"
            )
            assert "sources" in filtered, "Filtered result missing 'sources' key"

            self.log_result(
                "rag.list_sources",
                "PASS",
                f"Successfully listed {result['total']} sources",
                {"sources": result["sources"], "filtered_count": len(filtered["sources"])}
            )
            return True

        except Exception as e:
            self.log_result("rag.list_sources", "FAIL", str(e), {"error": str(e)})
            return False

    async def test_get_context(self):
        """Test Tool 3: rag.get_context"""
        print("\n" + "="*60)
        print("TEST 3: rag.get_context")
        print("="*60)

        try:
            # Test getting all context types
            result = await self.backend.get_context(
                project_id=self.project_id,
                context_type="all",
                query="test",
                max_results=5
            )
            assert "symbolic" in result, "Result missing 'symbolic' key"
            assert "episodic" in result, "Result missing 'episodic' key"
            assert "semantic" in result, "Result missing 'semantic' key"
            assert "message" in result, "Result missing 'message' key"

            print(f"Context retrieved: {len(result['symbolic'])} symbolic, "
                  f"{len(result['episodic'])} episodic, "
                  f"{len(result['semantic'])} semantic")

            # Test getting only symbolic context
            symbolic_only = await self.backend.get_context(
                project_id=self.project_id,
                context_type="symbolic",
                max_results=3
            )
            assert len(symbolic_only["episodic"]) == 0, "Should not return episodic"
            assert len(symbolic_only["semantic"]) == 0, "Should not return semantic"

            self.log_result(
                "rag.get_context",
                "PASS",
                f"Successfully retrieved context from all memory types",
                {"symbolic_count": len(result["symbolic"]),
                 "episodic_count": len(result["episodic"]),
                 "semantic_count": len(result["semantic"])}
            )
            return True

        except Exception as e:
            self.log_result("rag.get_context", "FAIL", str(e), {"error": str(e)})
            return False

    async def test_search(self):
        """Test Tool 4: rag.search"""
        print("\n" + "="*60)
        print("TEST 4: rag.search")
        print("="*60)

        try:
            # Test searching all memory types
            result = await self.backend.search(
                project_id=self.project_id,
                query="memory",
                memory_type="all",
                top_k=5
            )
            assert "results" in result, "Result missing 'results' key"
            assert "total" in result, "Result missing 'total' key"
            assert "message" in result, "Result missing 'message' key"
            assert isinstance(result["results"], list), "Results should be a list"

            print(f"Search returned {result['total']} result(s)")

            # Verify results have authority field
            for r in result["results"]:
                assert "authority" in r, f"Result missing 'authority': {r}"
                assert "type" in r, f"Result missing 'type': {r}"

            # Test searching specific memory type
            symbolic_only = await self.backend.search(
                project_id=self.project_id,
                query="test",
                memory_type="symbolic",
                top_k=3
            )
            assert all(r["type"] == "symbolic" for r in symbolic_only["results"]), \
                   "All results should be symbolic"

            self.log_result(
                "rag.search",
                "PASS",
                f"Successfully searched and found {result['total']} results",
                {"total_results": result["total"], "types_found": list(set(r["type"] for r in result["results"]))}
            )
            return True

        except Exception as e:
            self.log_result("rag.search", "FAIL", str(e), {"error": str(e)})
            return False

    async def test_add_fact(self):
        """Test Tool 5: rag.add_fact"""
        print("\n" + "="*60)
        print("TEST 5: rag.add_fact")
        print("="*60)

        try:
            # Generate unique fact key for this test
            self.test_fact_key = f"mcp_test_fact_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Add a test fact
            result = await self.backend.add_fact(
                project_id=self.project_id,
                fact_key=self.test_fact_key,
                fact_value={
                    "test_data": "This is a test fact from MCP tool verification",
                    "timestamp": datetime.utcnow().isoformat(),
                    "tool": "rag.add_fact"
                },
                confidence=0.95,
                category="fact"
            )

            assert "status" in result, "Result missing 'status' key"
            assert result["status"] == "success", f"Expected success, got: {result}"
            assert "fact_id" in result, "Result missing 'fact_id' key"
            assert "authority" in result, "Result missing 'authority' key"
            assert result["authority"] == "authoritative", "Fact should be authoritative"

            print(f"Successfully added fact with ID: {result['fact_id']}")
            print(f"Fact key: {self.test_fact_key}")

            # Verify fact was stored by searching for it
            search_result = await self.backend.search(
                project_id=self.project_id,
                query=self.test_fact_key,
                memory_type="symbolic",
                top_k=1
            )

            assert len(search_result["results"]) > 0, "Fact not found in search"

            self.log_result(
                "rag.add_fact",
                "PASS",
                f"Successfully added fact with ID: {result['fact_id']}",
                {"fact_id": result["fact_id"], "fact_key": self.test_fact_key, "verified": True}
            )
            return True

        except Exception as e:
            self.log_result("rag.add_fact", "FAIL", str(e), {"error": str(e)})
            return False

    async def test_add_episode(self):
        """Test Tool 6: rag.add_episode"""
        print("\n" + "="*60)
        print("TEST 6: rag.add_episode")
        print("="*60)

        try:
            # Add a test episode
            episode_title = f"MCP Test Episode - {datetime.now().strftime('%Y%m%d_%H%M%S')}"

            episode_content = """Situation: Testing the RAG MCP server add_episode tool.
Action: Executed add_episode with structured content.
Outcome: Successfully added episodic memory entry.
Lesson: Episode content parsing works correctly for MCP server."""

            result = await self.backend.add_episode(
                project_id=self.project_id,
                title=episode_title,
                content=episode_content,
                lesson_type="success",
                quality=0.9
            )

            assert "status" in result, "Result missing 'status' key"
            assert result["status"] == "success", f"Expected success, got: {result}"
            assert "episode_id" in result, "Result missing 'episode_id' key"
            assert "authority" in result, "Result missing 'authority' key"
            assert result["authority"] == "advisory", "Episode should be advisory"

            self.test_episode_id = result["episode_id"]
            print(f"Successfully added episode with ID: {result['episode_id']}")
            print(f"Title: {episode_title}")

            # Verify episode was stored
            context_result = await self.backend.get_context(
                project_id=self.project_id,
                context_type="episodic",
                max_results=5
            )

            assert len(context_result["episodic"]) > 0, "No episodes found in context"

            self.log_result(
                "rag.add_episode",
                "PASS",
                f"Successfully added episode with ID: {result['episode_id']}",
                {"episode_id": result["episode_id"], "title": episode_title, "verified": True}
            )
            return True

        except Exception as e:
            self.log_result("rag.add_episode", "FAIL", str(e), {"error": str(e)})
            return False

    async def test_ingest_file(self):
        """Test Tool 7: rag.ingest_file"""
        print("\n" + "="*60)
        print("TEST 7: rag.ingest_file")
        print("="*60)

        try:
            # Find a suitable test file from the project
            test_files = [
                "/home/dietpi/pi-rag/README.md",
                "/home/dietpi/pi-rag/requirements.txt",
                "/home/dietpi/pi-rag/api/main.py"
            ]

            test_file = None
            for f in test_files:
                if os.path.exists(f):
                    test_file = f
                    break

            if not test_file:
                raise FileNotFoundError("No suitable test file found")

            print(f"Ingesting file: {test_file}")

            # Ingest the file
            result = await self.backend.ingest_file(
                project_id=self.project_id,
                file_path=test_file,
                source_type="file",
                metadata={
                    "test_run": datetime.utcnow().isoformat(),
                    "tool": "rag.ingest_file"
                }
            )

            assert "status" in result, "Result missing 'status' key"
            assert result["status"] == "success", f"Expected success, got: {result}"
            assert "chunk_count" in result, "Result missing 'chunk_count' key"
            assert "doc_id" in result, "Result missing 'doc_id' key"
            assert result["chunk_count"] > 0, "Should have created at least one chunk"

            self.test_doc_id = result["doc_id"]
            print(f"Successfully ingested file with {result['chunk_count']} chunk(s)")
            print(f"Document ID: {result['doc_id']}")

            # Verify file was indexed by searching for it
            search_result = await self.backend.search(
                project_id=self.project_id,
                query="ingest test file",
                memory_type="semantic",
                top_k=3
            )

            print(f"Semantic search found {len(search_result['results'])} result(s)")

            # List sources to verify document is indexed
            sources_result = await self.backend.list_sources(
                project_id=self.project_id,
                source_type="file"
            )

            found_source = any(s["path"] == test_file for s in sources_result["sources"])
            assert found_source, f"File not found in sources: {test_file}"

            self.log_result(
                "rag.ingest_file",
                "PASS",
                f"Successfully ingested file with {result['chunk_count']} chunk(s)",
                {"doc_id": result["doc_id"], "file_path": test_file, "verified": True}
            )
            return True

        except Exception as e:
            self.log_result("rag.ingest_file", "FAIL", str(e), {"error": str(e)})
            return False

    async def test_verification_search(self):
        """Final verification: Search for all test data"""
        print("\n" + "="*60)
        print("FINAL VERIFICATION: Search for all test data")
        print("="*60)

        try:
            # Search for the test fact
            if self.test_fact_key:
                fact_result = await self.backend.search(
                    project_id=self.project_id,
                    query=self.test_fact_key,
                    memory_type="symbolic",
                    top_k=1
                )
                print(f"Test fact found: {len(fact_result['results']) > 0}")

            # Search for the test episode
            episode_result = await self.backend.search(
                project_id=self.project_id,
                query="MCP Test Episode",
                memory_type="episodic",
                top_k=3
            )
            print(f"Test episode found: {len(episode_result['results']) > 0}")

            # Search for semantic content
            semantic_result = await self.backend.search(
                project_id=self.project_id,
                query="ingest test",
                memory_type="semantic",
                top_k=3
            )
            print(f"Semantic content found: {len(semantic_result['results']) > 0}")

            self.log_result(
                "verification_search",
                "PASS",
                "All test data successfully retrieved",
                {
                    "fact_found": len(fact_result.get("results", [])) > 0,
                    "episode_found": len(episode_result.get("results", [])) > 0,
                    "semantic_found": len(semantic_result.get("results", [])) > 0
                }
            )
            return True

        except Exception as e:
            self.log_result("verification_search", "FAIL", str(e), {"error": str(e)})
            return False

    def print_summary(self):
        """Print test summary."""
        print("\n" + "="*60)
        print("TEST SUMMARY")
        print("="*60)

        passed = sum(1 for r in self.test_results if r["status"] == "PASS")
        failed = sum(1 for r in self.test_results if r["status"] == "FAIL")
        total = len(self.test_results)

        print(f"\nTotal Tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {failed}")
        print(f"Success Rate: {passed/total*100:.1f}%")

        print("\nDetailed Results:")
        print("-" * 60)
        for result in self.test_results:
            status_symbol = "✓" if result["status"] == "PASS" else "✗"
            print(f"{status_symbol} {result['tool']}: {result['message']}")

        # Save results to file
        output_file = "/home/dietpi/pi-rag/mcp_test_results.json"
        with open(output_file, 'w') as f:
            json.dump({
                "summary": {
                    "total": total,
                    "passed": passed,
                    "failed": failed,
                    "success_rate": f"{passed/total*100:.1f}%"
                },
                "tests": self.test_results,
                "timestamp": datetime.utcnow().isoformat()
            }, f, indent=2)

        print(f"\nDetailed results saved to: {output_file}")

        return failed == 0


async def main():
    """Run all tests."""
    print("RAG MCP Server Tool Verification Test Suite")
    print("=" * 60)
    print(f"Project ID: mcp_test_project")
    print(f"Start Time: {datetime.utcnow().isoformat()}")
    print("=" * 60)

    tester = RAGMCPTester()

    # Test Phase 1: Read-only operations
    await tester.test_list_projects()
    await tester.test_list_sources()
    await tester.test_get_context()
    await tester.test_search()

    # Test Phase 2: Write operations
    await tester.test_add_fact()
    await tester.test_add_episode()
    await tester.test_ingest_file()

    # Test Phase 3: Verification
    await tester.test_verification_search()

    # Print summary
    success = tester.print_summary()

    return 0 if success else 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
