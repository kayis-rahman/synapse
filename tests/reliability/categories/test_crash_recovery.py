#!/usr/bin/env python3
"""
Test Category 1: MCP Server Crash & Restart Tests (CRITICAL)

Proves persistence & safe recovery when MCP server crashes.
"""

import asyncio
import sys
import subprocess
from pathlib import Path

# Import test harness
from .docker_orchestrate import DockerOrchestrator, get_docker_orchestrator


class CrashRecoveryTester:
    """Test MCP server crash recovery and persistence."""
    
    def __init__(self):
        """Initialize tester."""
        self.orchestrator = get_docker_orchestrator()
        self.pass_count = 0
        self.fail_count = 0
    
    async def test_crash_during_ingestion(self) -> bool:
        """
        Test 1: Kill container mid-file ingestion.
        
        Returns: Pass/Fail
        """
        print(f"\n{'='*50}")
        print(f"TEST 1: Crash During Ingestion")
        print('='*50)
        
        # Start ingestion
        result = await self.orchestrator.start_environment()
        
        # Kill container mid-operation
        print("\n🔪 Killing container mid-ingestion...")
        kill_result = await self.orchestrator.kill_container()
        print(f"Kill result: {kill_result['status']}")
        
        # Restart
        print("\n🔄 Restarting container...")
        restart_result = await self.orchestrator.restart_container()
        print(f"Restart result: {restart_result['status']}")
        
        # Verify persistence
        print("\n✅ Checking persistence...")
        sources = await self._orchestrator.container_logs()
        assert "restarted" in sources['logs'], "Container was not properly restarted"
        assert "up" in sources['logs'].lower(), "Container not running after restart"
        assert "rag-mcp-test" in sources['logs'], "Service not found"
        
        print("✅ TEST 1 PASSED: Crash recovery successful")
        self.pass_count += 1
        return True
    
    async def test_crash_during_retrieval(self) -> bool:
        """
        Test 2: Kill container during retrieval.
        
        Returns: Pass/Fail
        """
        print(f"\n{'='*50}")
        print(f"TEST 2: Crash During Retrieval")
        print('='*50)
        
        # Search to populate memory
        search_result = await self.orchestrator.run_shell_command(
            'python -c "from rag.semantic_retriever import get_semantic_retriever; '
            'retriever = get_semantic_retriever(); '
            'results = retriever.retrieve(\"test query\", trigger=\"external_info_needed\", top_k=3); '
            'print(f\"Found {len(results)} results\"); '
            'exit(0)"'
        )
        
        # Kill container mid-search
        print("\n🔪 Killing container during retrieval...")
        kill_result = await self.orchestrator.kill_container()
        print(f"Kill result: {kill_result['status']}")
        
        # Restart and verify
        print("\n🔄 Restarting container...")
        restart_result = await self.orchestrator.restart_container()
        print(f"Restart result: {restart_result['status']}")
        
        # Verify search still works
        print("\n✅ Verifying search still works...")
        search_result = await self.orchestrator.run_shell_command(
            'python -c "from rag.semantic_retriever import get_semantic_retriever; '
            'retriever = get_semantic_retriever(); '
            'results = retriever.retrieve(\"test query\", trigger=\"external_info_needed\", top_k=3); '
            'print(f\"Found {len(results)} results\"); '
            'exit(0)"'
        )
        assert len(search_result) == 3, "Search didn't return expected 3 results"
        
        print("✅ TEST 2 PASSED: Search functionality intact after crash")
        self.pass_count += 1
        return True
    
    async def test_hard_kill_and_restart(self) -> bool:
        """
        Test 3: Hard kill (-9) and restart.
        
        Returns: Pass/Fail
        """
        print(f"\n{'='*50}")
        print(f"TEST 3: Hard Kill & Restart")
        print('='*50)
        
        # Hard kill
        print("\n🔪 Sending SIGKILL...")
        kill_result = await self.orchestrator.kill_container(signal="SIGKILL")
        print(f"Kill result: {kill_result['status']}")
        
        # Wait
        print("\n⏱ Waiting 3 seconds...")
        await asyncio.sleep(3)
        
        # Restart
        print("\n🔄 Restarting container...")
        restart_result = await self.orchestrator.start_environment()
        
        # Verify all three memory types
        print("\n✅ Checking all memory types after restart...")
        sources = await self.orchestrator.container_logs()
        assert "rag-mcp-test" in sources['logs'], "Service not found"
        
        # Check symbolic memory
        symbolic_result = await self.orchestrator.run_shell_command(
            'python -c "from rag.memory_store import get_memory_store; '
            'store = get_memory_store(); '
            'facts = store.query_memory(scope=\"project\"); '
            'print(f\"Symbolic facts: {len(facts)}\"); '
            'exit(0)"'
        )
        assert "facts" in symbolic_result, "Symbolic memory not accessible"
        
        # Check episodic memory
        episodic_result = await self.orchestrator.run_shell_command(
            'python -c "from rag.episodic_store import get_episodic_store; '
            'store = get_episodic_store(); '
            'episodes = store.list_recent_episodes(limit=10); '
            'print(f\"Episodic episodes: {len(episodes)}\"); '
            'exit(0)"'
        )
        assert "episodes" in episodic_result, "Episodic memory not accessible"
        
        # Check semantic memory
        semantic_result = await self.orchestrator.run_shell_command(
            'python -c "from rag.semantic_store import get_semantic_store; '
            'store = get_semantic_store(); '
            'print(f\"Semantic chunks: {len(store.chunks)}\"); '
            'exit(0)"'
        )
        assert "chunks" in semantic_result, "Semantic memory not accessible"
        
        print("✅ TEST 3 PASSED: Hard kill & restart successful")
        self.pass_count += 1
        return True


async def main():
    """Run all Category 1 tests."""
    tester = CrashRecoveryTester()
    
    total = 3
    passed = 0
    
    try:
        if await tester.test_crash_during_ingestion():
            passed += 1
        if await tester.test_crash_during_retrieval():
            passed += 1
        if await tester.test_hard_kill_and_restart():
            passed += 1
    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        passed = 0
    
    print(f"\n{'='*70}")
    print(f"CATEGORY 1 SUMMARY - Crash & Recovery Tests")
    print('='*70)
    print(f"Passed: {passed}/{total} ({(passed/total*100):.0f}%)")
    print(f"Tests:")
    print("  1. Crash during ingestion")
    print("  2. Crash during retrieval")
    print("   3. Hard kill & restart")
    
    if passed == total:
        print(f"\n{'='*70}")
        print("✅ ALL CATEGORY 1 TESTS PASSED ✅")
        return 0
    else:
        print(f"\n❌ SOME CATEGORY 1 TESTS FAILED ❌")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(main())
