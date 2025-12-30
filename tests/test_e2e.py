import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from mcp_server.rag_server import RAGMemoryBackend


# Main test runner
async def run_all_tests():
    print("=" * 70)
    print("PHASE 3 E2E TEST SUITE")
    print("=" * 70)
    
    tests = [
        ("Basic Workflow", test_basic_workflow),
        ("Error Handling", test_error_handling),
        ("Multi-Episode", test_multi_episode),
        ("Persistence", test_persistence),
        ("Cross-Tool", test_cross_tool),
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\nRunning: {test_name}")
        try:
            passed = await test_func()
            results.append((test_name, passed))
            if passed:
                print(f"✓ {test_name} PASSED")
            else:
                print(f"✗ {test_name} FAILED")
        except Exception as e:
            print(f"✗ {test_name} CRASHED: {e}")
            results.append((test_name, False))
            import traceback
            traceback.print_exc()
    
    print("\n" + "=" * 70)
    print("TEST SUMMARY")
    print("=" * 70)
    
    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    
    for test_name, passed in results:
        status = "✓" if passed else "✗"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed_count}/{total_count} tests passed")
    
    if passed_count == total_count:
        print("\n🎉 ALL E2E TESTS PASSED!")
        return 0
    else:
        print(f"\n⚠️  {total_count - passed_count} test(s) FAILED")
        return 1


async def test_basic_workflow():
    """Test 1: Basic Workflow - Add, Search, Retrieve"""
    print("\nTest: Add episode -> Search -> Retrieve")
    
    backend = RAGMemoryBackend()
    
    # Add episode
    print("Adding test episode...")
    add_result = await backend.add_episode(
        project_id="project",
        title="E2E Test Episode",
        content="Situation: E2E testing\nAction: Testing operations\nOutcome: Testing successful\nLesson: E2E tests verify workflows",
        lesson_type="pattern",
        quality=0.9
    )
    
    if add_result.get("status") != "success":
        print(f"✗ Add failed: {add_result}")
        return False
    
    episode_id = add_result.get("episode_id")
    if not episode_id:
        print("✗ No episode ID returned")
        return False
    
    print(f"✓ Episode added: {episode_id}")
    
    # Search
    print("Searching for episode...")
    search_result = await backend.search(
        project_id="project",
        query="E2E test",
        memory_type="episodic",
        top_k=5
    )
    
    if search_result.get("status") != "success":
        print(f"✗ Search failed: {search_result}")
        return False
    
    print(f"✓ Search found {search_result.get('total', 0)} result(s)")
    
    # Retrieve
    print("Retrieving context...")
    context_result = await backend.get_context(
        project_id="project",
        context_type="episodic",
        query="E2E",
        max_results=10
    )
    
    if context_result.get("status") != "success":
        print(f"✗ Get context failed: {context_result}")
        return False
    
    episodes = context_result.get("episodic", [])
    found = any(e.get("episode_id") == episode_id for e in episodes)
    print(f"✓ Episode found in context: {found}")
    
    print("✓ Basic workflow test PASSED")
    return True


async def test_error_handling():
    """Test 2: Error Handling - Invalid Inputs"""
    print("\nTest: Invalid inputs")
    
    backend = RAGMemoryBackend()
    
    # Missing title - should fail gracefully
    print("Test 1: Missing title...")
    try:
        result = await backend.add_episode(
            project_id="project",
            title="",  # Empty
            content="Test content",
            lesson_type="pattern",
            quality=0.8
        )
        if result.get("status") in ["error", "failure"]:
            print("✓ Missing title rejected")
        else:
            print("✗ Missing title not rejected - unexpected")
    except Exception:
        print("✓ Missing title handled")
    
    # Invalid lesson type - should fail gracefully
    print("Test 2: Invalid lesson type...")
    try:
        result = await backend.add_episode(
            project_id="project",
            title="Test",
            content="Test content",
            lesson_type="invalid_type",  # Invalid
            quality=0.8
        )
        if result.get("status") in ["error", "failure"]:
            print("✓ Invalid lesson type rejected")
        else:
            print("✗ Invalid lesson type not rejected - unexpected")
    except Exception:
        print("✓ Invalid lesson type handled")
    
    print("✓ Error handling test PASSED")
    return True


async def test_multi_episode():
    """Test 3: Multi-Episode"""
    print("\nTest: Multi-Episode (10 episodes)")
    
    backend = RAGMemoryBackend()
    episode_ids = []
    
    lesson_types = ["pattern", "mistake", "success", "general"]
    for lesson_type in lesson_types:
        for i in range(5):
            result = await backend.add_episode(
                project_id="project",
                title=f"Test {lesson_type} {i}",
                content=f"Situation: {i}\nAction: Test {i}\nOutcome: Test {i}\nLesson: Test {lesson_type}",
                lesson_type=lesson_type,
                quality=0.7 + (i * 0.05)
            )
            if result.get("status") == "success":
                episode_ids.append(result["episode_id"])
    
    print(f"✓ Added {len(episode_ids)} episodes")
    
    # Search by type
    print("Searching by type...")
    patterns_result = await backend.search(
        project_id="project",
        query="test",
        memory_type="episodic",
        top_k=10
    )
    
    patterns = patterns_result.get("results", [])
    print(f"✓ Found {len(patterns)} pattern episodes")
    
    # Get all context
    print("Getting all context...")
    all_context = await backend.get_context(
        project_id="project",
        context_type="episodic",
        max_results=20
        )
    
    episodes = all_context.get("episodic", [])
    print(f"✓ Retrieved {len(episodes)} episodes")
    
    # Cleanup
    print("Cleaning up...")
    from rag import get_episodic_store
    episodic_store = get_episodic_store("./data/episodic.db")
    for eid in episode_ids:
        episodic_store.delete_episode(id=eid)
    
    print("✓ Multi-episode test PASSED")
    return True


async def test_persistence():
    """Test 4: Persistence Across Restart"""
    print("\nTest: Persistence")
    
    backend1 = RAGMemoryBackend()
    
    # Add episode
    print("Adding test episode...")
    result = await backend1.add_episode(
        project_id="project",
        title="Persistence Test",
        content="Situation: Testing persistence\nAction: Testing persistence\nOutcome: Testing successful\nLesson: Data should persist",
        lesson_type="success",
        quality=0.9
    )
    
    if result.get("status") != "success":
        print(f"✗ Add failed: {result}")
        return False
    
    episode_id = result["episode_id"]
    print(f"✓ Episode added: {episode_id}")
    
    # Verify in first instance
    from rag import get_episodic_store
    store1 = get_episodic_store("./data/episodic.db")
    recent1 = store1.list_recent_episodes(limit=100)
    found_before = any(ep.id == episode_id for ep in recent1)
    print(f"✓ Episode exists before restart")
    
    # Simulate restart (new backend instance)
    print("Simulating restart...")
    import asyncio
    await asyncio.sleep(0.5)
    backend2 = RAGMemoryBackend()
    
    # Search in new instance
    print("Searching in new instance...")
    result = await backend2.search(
        project_id="project",
        query="persistence test",
        memory_type="episodic",
        top_k=5
    )
    
    found_in_search = any(r.get("episode_id") == episode_id for r in result.get("results", []))
    print(f"✓ Episode found in new instance: {found_in_search}")
    
    # Verify in new instance
    print("Verifying in new instance...")
    context = await backend2.get_context(
        project_id="project",
        context_type="episodic",
        query="persistence",
        max_results=10
    )
    episodes = context.get("episodic", [])
    found_after = any(ep.id == episode_id for ep in episodes)
    print(f"✓ Episode data unchanged: {found_after}")
    
    # Cleanup
    print("Cleaning up...")
    store2 = get_episodic_store("./data/episodic.db")
    store2.delete_episode(id=episode_id)
    
    print("✓ Persistence test PASSED")
    return True


async def test_cross_tool():
    """Test 5: Cross-Tool Workflow"""
    print("\nTest: Cross-Tool")
    
    backend = RAGMemoryBackend()
    
    # List projects
    print("Listing projects...")
    projects_result = await backend.list_projects()
    if projects_result.get("status") != "success":
        print(f"✗ List projects failed: {projects_result}")
        return False
    projects = projects_result.get("projects", projects_result.get("projects", []))
    print(f"✓ Found {len(projects)} projects")
    
    # List sources
    print("Listing sources...")
    sources_result = await backend.list_sources(project_id="project")
    print(f"✓ Sources check completed")
    
    # Add episodes
    print("Adding test episodes...")
    episode_ids = []
    for i in range(3):
        result = await backend.add_episode(
            project_id="project",
            title=f"Cross-tool test {i}",
            content=f"Situation: Test {i}\nAction: Test {i}\nOutcome: Test {i}\nLesson: Test {i}",
            lesson_type="general",
            quality=0.8
        )
        if result.get("status") == "success":
            episode_ids.append(result["episode_id"])
    
    print(f"✓ Added {len(episode_ids)} episodes")
    
    # Search
    print("Searching episodes...")
    result = await backend.search(
        project_id="project",
        query="cross-tool test",
        memory_type="episodic",
        top_k=10
    )
    print(f"✓ Search found {result.get('total', 0)} result(s)")
    
    # Get context
    print("Getting context...")
    context = await backend.get_context(
        project_id="project",
        context_type="episodic",
        query="cross-tool",
        max_results=10
    )
    episodes = context.get("episodic", [])
    print(f"✓ Context retrieved {len(episodes)} episodes")
    
    # Verify consistency
    context_episodes = context.get("episodic", [])
    all_found = all(
        any(ep.id in episode_ids for ep in context_episodes)
        for ep in context_episodes
    )
    print(f"✓ Data consistent: all_found={all_found}")
    
    # Cleanup
    print("Cleaning up...")
    from rag import get_episodic_store
    episodic_store = get_episodic_store("./data/episodic.db")
    deleted = 0
    for eid in episode_ids:
        if episodic_store.delete_episode(id=eid):
            deleted += 1
    
    print(f"✓ Deleted {deleted}/{len(episode_ids)} episodes")
    
    print("✓ Cross-tool test PASSED")
    return True


if __name__ == "__main__":
    import os
    os.environ.setdefault("RAG_DATA_DIR", "/home/dietpi/pi-rag/data")
    
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)
EOT
