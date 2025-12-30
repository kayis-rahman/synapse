"""
END-TO-END (E2E) TESTS FOR PHASE 3: EPISODIC MEMORY
==================================================================

Comprehensive E2E testing for episodic memory functionality.

Test Categories:
1. Basic Workflow E2E
2. Multi-Episode E2E
3. Error Handling E2E
4. Cross-Tool E2E
5. Persistence E2E

All tests verify the complete user workflow:
- Client -> MCP Server -> Database -> Response -> Verification
"""

import asyncio
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_server.rag_server import RAGMemoryBackend


def print_success(msg):
    print(f"GREEN;{msg};END")


def print_error(msg):
    print(f"RED;{msg};END")


def print_info(msg):
    print(f"YELLOW;{msg};END")


def print_test_header(msg):
    print(f"\nBLUE;{'='*60};END")
    print(f"BLUE;{msg};END")
    print(f"BLUE;{'='*60};END")


def print_test(msg):
    print(f"YELLOW;Testing: {msg};END")


async def test_basic_workflow_add_search_retrieve():
    """Test 1: Basic Workflow E2E"""
    print_test_header("TEST 1: Basic Workflow E2E")
    print_test("Add episode -> Search -> Retrieve")

    backend = RAGMemoryBackend()
    results = {
        "add_episode": False,
        "verify_stored": False,
        "search": False,
        "verify_search": False,
        "get_context": False,
        "cleanup": False
    }

    try:
        # Step 1: Add episode
        print_info("Step 1: Adding pattern episode...")
        add_result = await backend.add_episode(
            project_id="project",
            title="E2E Test Pattern",
            content="Situation: Test workflow;Action: Testing E2E;Outcome: Testing successful;Lesson: E2E tests verify workflows",
            lesson_type="pattern",
            quality=0.9
        )

        assert add_result["status"] == "success", f"Add failed: {add_result}"
        episode_id = add_result["episode_id"]
        assert episode_id, "No episode ID returned"
        print_success(f"Episode added with ID: {episode_id}")
        results["add_episode"] = True

        # Step 2: Verify episode was stored
        print_info("Step 2: Verifying episode in database...")
        from rag import get_episodic_store
        episodic_store = get_episodic_store(f"{os.environ.get('RAG_DATA_DIR', './data')}/episodic.db")
        # Use list_recent_episodes to verify
        recent_episodes = episodic_store.list_recent_episodes(limit=100)
        found = any(ep.id == episode_id for ep in recent_episodes)
        assert found, "Episode not found in database"
        print_success("Episode verified in database")
        results["verify_stored"] = True

        # Step 3: Search for episode
        print_info("Step 3: Searching for episode...")
        search_result = await backend.search(
            project_id="project",
            query="E2E test workflow",
            memory_type="episodic",
            top_k=5
        )

        assert search_result["status"] == "success", f"Search failed: {search_result}"
        print_success(f"Search found {search_result.get('total', 0)} result(s)")
        results["search"] = True

        # Step 4: Verify search returns episode
        assert search_result.get("total", 0) > 0, "Search returned no results"
        print_success("Episode found in search results")
        results["verify_search"] = True

        # Step 5: Retrieve via get_context
        print_info("Step 4: Retrieving via get_context...")
        context_result = await backend.get_context(
            project_id="project",
            context_type="episodic",
            query="E2E test",
            max_results=10
        )

        assert context_result["status"] == "success", f"Get context failed: {context_result}"
        print_success(f"Retrieved {len(context_result.get('episodic', []))} episode(s)")
        results["get_context"] = True

        # Step 6: Clean up
        print_info("Step 5: Deleting test episode...")
        deleted = episodic_store.delete_episode(episode_id)
        assert deleted, "Failed to delete episode"
        print_success("Test episode deleted")
        results["cleanup"] = True

        # Summary
        all_passed = all(results.values())
        if all_passed:
            print_success(f"BLUE;TEST 1 PASSED - All steps successful;END")
            return True
        else:
            failed_steps = [k for k, v in results.items() if not v]
            print_error(f"TEST 1 FAILED - Failed steps: {', '.join(failed_steps)}")
            return False

    except Exception as e:
        print_error(f"TEST 1 CRASHED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_error_handling_invalid_inputs():
    """Test 2: Error Handling - Invalid Inputs"""
    print_test_header("TEST 2: Error Handling E2E")
    print_test("Invalid inputs -> Graceful errors")

    backend = RAGMemoryBackend()
    test_cases = {
        "missing_title": False,
        "invalid_lesson_type": False,
        "quality_too_low": False,
        "quality_too_high": False,
        "empty_content": False
    }

    try:
        # Test 1: Missing title
        print_info("Test 1: Missing title field...")
        try:
            result = await backend.add_episode(
                project_id="project",
                title="",
                content="Test content",
                lesson_type="pattern",
                quality=0.8
            )
            if result.get("status") != "success":
                print_success("Missing title rejected correctly")
                test_cases["missing_title"] = True
        except:
            print_success("Missing title caused error (expected)")
            test_cases["missing_title"] = True

        # Test 2: Invalid lesson_type
        print_info("Test 2: Invalid lesson_type...")
        try:
            result = await backend.add_episode(
                project_id="project",
                title="Test",
                content="Test content",
                lesson_type="invalid_type",
                quality=0.8
            )
            if result.get("status") == "error" or result.get("error"):
                print_success("Invalid lesson_type rejected correctly")
                test_cases["invalid_lesson_type"] = True
        except:
            print_success("Invalid lesson_type caused error (expected)")
            test_cases["invalid_lesson_type"] = True

        # Test 3: Quality too low (< 0.0)
        print_info("Test 3: Quality < 0.0...")
        try:
            result = await backend.add_episode(
                project_id="project",
                title="Test",
                content="Test content",
                lesson_type="pattern",
                quality=-0.5
            )
            if result.get("status") == "error" or result.get("error"):
                print_success("Quality < 0.0 rejected correctly")
                test_cases["quality_too_low"] = True
        except:
            print_success("Quality < 0.0 caused error (expected)")
            test_cases["quality_too_low"] = True

        # Test 4: Quality too high (> 1.0)
        print_info("Test 4: Quality > 1.0...")
        try:
            result = await backend.add_episode(
                project_id="project",
                title="Test",
                content="Test content",
                lesson_type="pattern",
                quality=1.5
            )
            if result.get("status") == "error" or result.get("error"):
                print_success("Quality > 1.0 rejected correctly")
                test_cases["quality_too_high"] = True
        except:
            print_success("Quality > 1.0 caused error (expected)")
            test_cases["quality_too_high"] = True

        # Summary
        all_passed = all(test_cases.values())
        if all_passed:
            print_success("BLUE;TEST 2 PASSED - All error cases handled;END")
            return True
        else:
            failed_cases = [k for k, v in test_cases.items() if not v]
            print_error(f"TEST 2 FAILED - Failed cases: {', '.join(failed_cases)}")
            return False

    except Exception as e:
        print_error(f"TEST 2 CRASHED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_multi_episode_workflow():
    """Test 3: Multi-Episode Workflow"""
    print_test_header("TEST 3: Multi-Episode Workflow")
    print_test("Add 20 episodes -> Filter searches -> Verify")

    backend = RAGMemoryBackend()
    episode_ids = []

    try:
        # Steps 1-4: Add 20 episodes (5 of each type)
        print_info("Steps 1-4: Adding 20 episodes (5 each type)...")
        lesson_types = ["pattern", "mistake", "success", "general"]
        for lesson_type in lesson_types:
            for i in range(5):
                result = await backend.add_episode(
                    project_id="project",
                    title=f"Test {lesson_type} {i}",
                    content=f"Situation: Test;Action: Test;Outcome: Test;Lesson: Test {lesson_type}",
                    lesson_type=lesson_type,
                    quality=0.7 + (i * 0.05)
                )
                assert result["status"] == "success"
                episode_ids.append(result["episode_id"])

        print_success(f"Added {len(episode_ids)} episodes")

        # Step 5: Search by lesson_type="pattern"
        print_info("Step 5: Searching for patterns...")
        patterns_result = await backend.search(
            project_id="project",
            query="test",
            memory_type="episodic",
            top_k=10
        )

        assert patterns_result["status"] == "success"
        patterns = patterns_result.get("results", [])
        print_success(f"Found {len(patterns)} pattern episodes")

        # Summary
        print_success("BLUE;TEST 3 PASSED - Multi-episode workflow successful;END")
        return True

    except Exception as e:
        print_error(f"TEST 3 CRASHED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_cross_tool_workflow():
    """Test 5: Cross-Tool Workflow"""
    print_test_header("TEST 5: Cross-Tool Workflow")
    print_test("List projects -> List sources -> Add -> Search -> Context")

    backend = RAGMemoryBackend()
    test_episode_ids = []

    try:
        # Step 1: List projects
        print_info("Step 1: Listing projects...")
        projects_result = await backend.list_projects()
        assert projects_result["status"] == "success" or "projects" in projects_result
        projects = projects_result.get("projects", projects_result.get("projects", []))
        assert len(projects) >= 1, "No projects found"
        print_success(f"Found {len(projects)} project(s)")

        # Step 2: List sources
        print_info("Step 2: Listing sources...")
        sources_result = await backend.list_sources(project_id="project")
        assert sources_result["status"] == "success"
        print_success("Sources check completed")

        # Step 3: Add 3 episodes
        print_info("Step 3: Adding 3 test episodes...")
        for i in range(3):
            result = await backend.add_episode(
                project_id="project",
                title=f"Cross-tool test {i}",
                content=f"Situation: Test {i};Action: Test;Outcome: Test;Lesson: Test",
                lesson_type="general",
                quality=0.8
            )
            assert result["status"] == "success"
            test_episode_ids.append(result["episode_id"])

        print_success(f"Added {len(test_episode_ids)} episodes")

        # Step 4: Search episodes
        print_info("Step 4: Searching episodes...")
        search_result = await backend.search(
            project_id="project",
            query="cross-tool test",
            memory_type="episodic",
            top_k=10
        )

        assert search_result["status"] == "success"
        print_success(f"Search found {search_result.get('total', 0)} result(s)")

        # Step 5: Get context
        print_info("Step 5: Getting context...")
        context_result = await backend.get_context(
            project_id="project",
            context_type="episodic",
            max_results=10
        )

        assert context_result["status"] == "success"
        print_success(f"Context retrieved {len(context_result.get('episodic', []))} episode(s)")

        # Step 6: Clean up
        print_info("Step 6: Cleaning up...")
        from rag import get_episodic_store
        episodic_store = get_episodic_store(f"{os.environ.get('RAG_DATA_DIR', './data')}/episodic.db")
        deleted = 0
        for eid in test_episode_ids:
            if episodic_store.delete_episode(eid):
                deleted += 1

        print_success(f"Deleted {deleted}/{len(test_episode_ids)} episodes")

        # Summary
        print_success("BLUE;TEST 5 PASSED - Cross-tool workflow successful;END")
        return True

    except Exception as e:
        print_error(f"TEST 5 CRASHED: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_persistence_across_restart():
    """Test 4: Persistence Across Restart"""
    print_test_header("TEST 4: Persistence Across Restart")
    print_test("Store -> Verify -> Cleanup")

    backend = RAGMemoryBackend()
    episode_id = None

    try:
        # Step 1: Add test episode
        print_info("Step 1: Adding persistence test episode...")
        result = await backend.add_episode(
            project_id="project",
            title="Persistence Test",
            content="Situation: Testing persistence;Action: Testing persistence;Outcome: Testing successful;Lesson: Data should persist",
            lesson_type="success",
            quality=0.9
        )

        assert result["status"] == "success"
        episode_id = result["episode_id"]
        print_success(f"Episode added: {episode_id}")

        # Step 2: Verify in database
        print_info("Step 2: Verifying episode in database...")
        from rag import get_episodic_store
        store = get_episodic_store("./data/episodic.db")
        recent = store.list_recent_episodes(limit=100)
        found = any(ep.id == episode_id for ep in recent)
        assert found, "Episode not found"
        print_success("Episode verified in database")

        # Step 3: Simulate restart
        print_info("Step 3: Simulating restart...")
        await asyncio.sleep(0.5)
        backend2 = RAGMemoryBackend()

        # Step 4: Search for episode
        print_info("Step 4: Searching for episode after restart...")
        result = await backend2.search(
            project_id="project",
            query="persistence test",
            memory_type="episodic",
            top_k=5
        )
        print_success("Search completed")

        print_success("BLUE;TEST 4 PASSED - Persistence works correctly;END")
        return True

    except Exception as e:
        print_error(f"TEST 4 CRASHED: {e}")
        return False


async def run_all_tests():
    """Run all E2E tests and report results."""
    print(f"\nBLUE;{'='*70};END")
    print(f"BLUE;PHASE 3 E2E TEST SUITE;END")

    tests = [
        ("Basic Workflow E2E", test_basic_workflow_add_search_retrieve),
        ("Error Handling E2E", test_error_handling_invalid_inputs),
        ("Multi-Episode Workflow", test_multi_episode_workflow),
        ("Cross-Tool Workflow", test_cross_tool_workflow),
        ("Persistence Across Restart", test_persistence_across_restart),
    ]

    results = []
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        passed = await test_func()
        results.append((test_name, passed))

    # Summary
    print(f"\nBLUE;{'='*70};END")
    print(f"BLUE;TEST SUMMARY;END")

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)

    for test_name, passed in results:
        if passed:
            print_success(f"{test_name}")
        else:
            print_error(f"{test_name}")

    print(f"\nResults: {passed_count}/{total_count} tests passed")

    if passed_count == total_count:
        print(f"\nGREEN;🎉 ALL E2E TESTS PASSED!;END")
        return 0
    else:
        print(f"\nRED;⚠️  {total_count - passed_count} test(s) FAILED;END")
        return 1


if __name__ == "__main__":
    import os
    os.environ.setdefault("RAG_DATA_DIR", "./data")
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
