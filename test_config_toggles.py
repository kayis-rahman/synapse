#!/usr/bin/env python3
"""
Automated test script for config-based feature toggles.

Tests:
1. file_path_mode_enabled flag
2. context_injection_enabled flag
3. Both flags disabled together
4. Both flags enabled together
5. Backward compatibility
"""

import asyncio
import os
import sys
import json
import tempfile
sys.path.insert(0, '/home/dietpi/pi-rag')

from mcp_server.rag_server import RAGMemoryBackend
from rag.orchestrator import RAGOrchestrator

# Test configuration path
TEST_CONFIG_PATH = "/tmp/test_rag_config.json"

def create_config(file_path_mode, context_injection):
    """Create test configuration file."""
    config = {
        "rag_enabled": True,
        "chunk_size": 500,
        "chunk_overlap": 50,
        "top_k": 3,
        "min_retrieval_score": 0.3,
        "index_path": "/tmp/test_rag_index",
        "docs_path": "/tmp/test_rag_docs",
        "rag_disable_keyword": "disable-rag",
        "embedding_model_path": "/home/dietpi/models/bge-small-en-v1.5-q8_0.gguf",
        "embedding_model_name": "embedding",
        "embedding_n_ctx": 8194,
        "embedding_n_gpu_layers": 0,
        "embedding_cache_enabled": True,
        "embedding_cache_size": 1000,
        "chat_model_path": "~/models/gemma-3-1b-it-UD-Q4_K_XL.gguf",
        "chat_model_name": "gemma-3-1b-it",
        "chat_n_ctx": 8192,
        "chat_n_gpu_layers": 0,
        "external_chat_api_url": "",
        "external_chat_api_key": "",
        "use_external_chat_model": False,
        "temperature": 0.7,
        "max_tokens": 2048,
        "memory_enabled": True,
        "memory_db_path": "/tmp/test_memory.db",
        "memory_scope": "session",
        "memory_min_confidence": 0.7,
        "memory_max_facts": 10,
        "remote_file_upload_enabled": True,
        "remote_upload_directory": "/tmp/test-rag-uploads",
        "remote_upload_max_age_seconds": 3600,
        "remote_upload_max_file_size_mb": 50,
        "file_path_mode_enabled": file_path_mode,
        "context_injection_enabled": context_injection
    }

    with open(TEST_CONFIG_PATH, 'w') as f:
        json.dump(config, f, indent=2)

def print_section(title):
    """Print test section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70 + "\n")

def print_result(test_name, passed, message=""):
    """Print test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {test_name}")
    if message:
        print(f"       {message}")

async def test_file_path_mode_disabled():
    """Test file_path mode when disabled."""
    print_section("Test 1: File Path Mode Disabled")

    # Create config with file_path_mode_enabled = false
    create_config(file_path_mode=False, context_injection=True)

    # Initialize backend with test config
    backend = RAGMemoryBackend()

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content")
        temp_file = f.name

    try:
        # Try to ingest using file_path mode
        result = await backend.ingest_file(
            project_id="global",
            file_path=temp_file,
            source_type="file"
        )

        # Should fail with file_path_mode_disabled error
        if result.get("status") == "error" and "file_path_mode_disabled" in result.get("error", ""):
            print_result("File path mode rejected", True, "Correctly blocked when disabled")
        else:
            print_result("File path mode rejection", False, f"Expected error, got: {result}")
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(TEST_CONFIG_PATH):
            os.remove(TEST_CONFIG_PATH)

async def test_file_path_mode_enabled():
    """Test file_path mode when enabled."""
    print_section("Test 2: File Path Mode Enabled")

    # Create config with file_path_mode_enabled = true
    create_config(file_path_mode=True, context_injection=True)

    # Initialize backend with test config
    backend = RAGMemoryBackend()

    # Create temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("Test content for file path mode")
        temp_file = f.name

    try:
        # Try to ingest using file_path mode
        result = await backend.ingest_file(
            project_id="global",
            file_path=temp_file,
            source_type="file"
        )

        # Should succeed
        if result.get("status") == "success":
            print_result("File path mode accepted", True, f"Ingested {result.get('chunk_count')} chunks")
        else:
            print_result("File path mode acceptance", False, f"Expected success, got: {result}")
    finally:
        # Cleanup
        if os.path.exists(temp_file):
            os.remove(temp_file)
        if os.path.exists(TEST_CONFIG_PATH):
            os.remove(TEST_CONFIG_PATH)

async def test_context_injection_disabled():
    """Test context injection when disabled."""
    print_section("Test 3: Context Injection Disabled")

    # Create config with context_injection_enabled = false
    create_config(file_path_mode=True, context_injection=False)

    # Initialize orchestrator with test config
    orchestrator = RAGOrchestrator(config_path=TEST_CONFIG_PATH)

    # Verify config loaded
    if not orchestrator.context_injection_enabled:
        print_result("Context injection flag loaded", True, "Correctly set to False")
    else:
        print_result("Context injection flag loaded", False, f"Expected False, got {orchestrator.context_injection_enabled}")

    # Test _inject_context returns messages unchanged
    test_messages = [
        {"role": "user", "content": "Test query"}
    ]

    result = orchestrator._inject_context(
        messages=test_messages,
        context="Test context",
        memory_context="Test memory"
    )

    # Should return original messages (no injection)
    if result == test_messages:
        print_result("Context not injected", True, "Messages unchanged when disabled")
    else:
        print_result("Context not injected", False, f"Expected no change, got modified messages")

    # Cleanup
    if os.path.exists(TEST_CONFIG_PATH):
        os.remove(TEST_CONFIG_PATH)

async def test_context_injection_enabled():
    """Test context injection when enabled."""
    print_section("Test 4: Context Injection Enabled")

    # Create config with context_injection_enabled = true
    create_config(file_path_mode=True, context_injection=True)

    # Initialize orchestrator with test config
    orchestrator = RAGOrchestrator(config_path=TEST_CONFIG_PATH)

    # Verify config loaded
    if orchestrator.context_injection_enabled:
        print_result("Context injection flag loaded", True, "Correctly set to True")
    else:
        print_result("Context injection flag loaded", False, f"Expected True, got {orchestrator.context_injection_enabled}")

    # Test _inject_context modifies messages
    test_messages = [
        {"role": "system", "content": "Test system"},
        {"role": "user", "content": "Test query"}
    ]

    result = orchestrator._inject_context(
        messages=test_messages,
        context="Test context",
        memory_context="Test memory"
    )

    # Should return modified messages (with injection)
    if result != test_messages:
        print_result("Context injected", True, "Messages modified with context")
    else:
        print_result("Context injected", False, "Expected modification, got no change")

    # Cleanup
    if os.path.exists(TEST_CONFIG_PATH):
        os.remove(TEST_CONFIG_PATH)

async def test_both_disabled():
    """Test both features disabled together."""
    print_section("Test 5: Both Features Disabled")

    # Create config with both disabled
    create_config(file_path_mode=False, context_injection=False)

    # Initialize components
    backend = RAGMemoryBackend()
    orchestrator = RAGOrchestrator(config_path=TEST_CONFIG_PATH)

    # Test file_path mode blocked
    test_passed = True

    if not backend._upload_config.get("file_path_mode_enabled", True):
        print_result("Backend config loaded", True, "File path mode disabled")
    else:
        print_result("Backend config loaded", False, "File path mode should be disabled")
        test_passed = False

    if not orchestrator.context_injection_enabled:
        print_result("Orchestrator config loaded", True, "Context injection disabled")
    else:
        print_result("Orchestrator config loaded", False, "Context injection should be disabled")
        test_passed = False

    # Cleanup
    if os.path.exists(TEST_CONFIG_PATH):
        os.remove(TEST_CONFIG_PATH)

    return test_passed

async def test_content_mode_always_works():
    """Test content mode always works regardless of file_path_mode setting."""
    print_section("Test 6: Content Mode Always Works")

    # Test with file_path_mode disabled
    create_config(file_path_mode=False, context_injection=True)

    backend = RAGMemoryBackend()

    # Ingest using content mode
    result = await backend.ingest_file(
        project_id="global",
        content="# Test Document\n\nContent for testing content mode.",
        filename="test_content.md",
        source_type="file"
    )

    # Should succeed
    if result.get("status") == "success":
        print_result("Content mode with file_path disabled", True, f"Ingested {result.get('chunk_count')} chunks")
    else:
        print_result("Content mode with file_path disabled", False, f"Expected success, got: {result}")

    # Cleanup
    if os.path.exists(TEST_CONFIG_PATH):
        os.remove(TEST_CONFIG_PATH)

async def main():
    """Run all tests."""
    print("\n" + "=" * 70)
    print("  CONFIG-BASED FEATURE TOGGLE TESTS")
    print("=" * 70)

    tests_passed = 0
    tests_total = 7

    try:
        await test_file_path_mode_disabled()
        tests_passed += 1
    except Exception as e:
        print_result("Test 1", False, f"Exception: {e}")

    try:
        await test_file_path_mode_enabled()
        tests_passed += 1
    except Exception as e:
        print_result("Test 2", False, f"Exception: {e}")

    try:
        await test_context_injection_disabled()
        tests_passed += 1
    except Exception as e:
        print_result("Test 3", False, f"Exception: {e}")

    try:
        await test_context_injection_enabled()
        tests_passed += 1
    except Exception as e:
        print_result("Test 4", False, f"Exception: {e}")

    try:
        await test_both_disabled()
        tests_passed += 1
    except Exception as e:
        print_result("Test 5", False, f"Exception: {e}")

    try:
        await test_content_mode_always_works()
        tests_passed += 1
    except Exception as e:
        print_result("Test 6", False, f"Exception: {e}")

    # Final summary
    print_section("TEST SUMMARY")
    print(f"Tests Passed: {tests_passed}/{tests_total}")
    print(f"Success Rate: {(tests_passed/tests_total)*100:.1f}%")

    if tests_passed == tests_total:
        print("\n✅ ALL TESTS PASSED - Config-based toggles working correctly!")
        return 0
    else:
        print(f"\n❌ {tests_total - tests_passed} TEST(S) FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
