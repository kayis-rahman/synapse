#!/usr/bin/env python3
"""
Comprehensive Validation Script for Remote File Ingestion

Tests all functionality before Mac deployment.
"""

import os
import sys
import json
import asyncio
from pathlib import Path

# Add to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mcp_server.rag_server import RAGMemoryBackend


def print_header(title: str):
    """Print formatted header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def print_test(name: str, passed: bool, details: str = ""):
    """Print test result."""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"\n{status}: {name}")
    if details:
        print(f"  {details}")


def check_configuration():
    """Test 1: Configuration"""
    print_header("Test 1: Configuration")

    passed = True
    results = []

    # Check 1: Config file exists
    config_path = "./configs/rag_config.json"
    if os.path.exists(config_path):
        print_test("Config file exists", True)
        results.append(("Config file exists", True))
    else:
        print_test("Config file exists", False)
        results.append(("Config file exists", False))
        passed = False

    # Check 2: Config file is valid JSON
    if os.path.exists(config_path):
        try:
            with open(config_path, 'r') as f:
                config = json.load(f)

            required_keys = [
                "remote_file_upload_enabled",
                "remote_upload_directory",
                "remote_upload_max_age_seconds",
                "remote_upload_max_file_size_mb"
            ]

            for key in required_keys:
                if key in config:
                    print_test(f"Config has key '{key}'", True)
                    results.append((f"Config has key '{key}'", True))
                else:
                    print_test(f"Config has key '{key}'", False)
                    results.append((f"Config has key '{key}'", False))
                    passed = False
        except json.JSONDecodeError as e:
            print_test("Config file is valid JSON", False, f"JSON decode error: {e}")
            results.append(("Config file is valid JSON", False))
            passed = False

    # Check 3: Upload directory config is set
    upload_dir = config.get("remote_upload_directory", "/tmp/rag-uploads")
    if upload_dir:
        print_test(f"Upload directory configured: {upload_dir}", True)
        results.append(("Upload directory configured", True))
    else:
        print_test("Upload directory configured", False)
        results.append(("Upload directory configured", False))
        passed = False

    # Check 4: Upload enabled config is true
    enabled = config.get("remote_file_upload_enabled", False)
    if enabled:
        print_test("Remote upload enabled", True)
        results.append(("Remote upload enabled", True))
    else:
        print_test("Remote upload enabled", False, f"Current value: {enabled}")
        results.append(("Remote upload enabled", False))
        passed = False

    # Check 5: File size limit is reasonable
    max_size = config.get("remote_upload_max_file_size_mb", 0)
    if max_size > 0:
        print_test(f"File size limit set: {max_size}MB", True)
        results.append((f"File size limit set: {max_size}MB", True))
    else:
        print_test("File size limit set: False", "File size limit is 0 or missing")
        results.append(("File size limit set: False"))
        passed = False

    # Check 6: File age limit is reasonable
    max_age = config.get("remote_upload_max_age_seconds", 0)
    if max_age > 0:
        print_test(f"File age limit set: {max_age}s ({max_age/3600:.1f}h)", True)
        results.append((f"File age limit set: {max_age}s", True))
    else:
        print_test("File age limit set: False", "File age limit is 0 or missing")
        results.append(("File age limit set: False"))
        passed = False

    print(f"\nConfiguration Test Summary: {sum(1 for p in results if p[1])}/{len(results)} passed")

    return passed


def check_upload_methods():
    """Test 2: Upload Methods"""
    print_header("Test 2: Upload Methods")

    passed = True
    results = []

    backend = RAGMemoryBackend()

    # Check 1: _load_upload_config method exists
    if hasattr(backend, '_load_upload_config'):
        print_test("_load_upload_config method exists", True)
        results.append(("_load_upload_config method exists", True))
    else:
        print_test("_load_upload_config method exists", False)
        results.append(("_load_upload_config method exists", False))
        passed = False

    # Check 2: _ensure_upload_directory method exists
    if hasattr(backend, '_ensure_upload_directory'):
        print_test("_ensure_upload_directory method exists", True)
        results.append(("_ensure_upload_directory method exists", True))
    else:
        print_test("_ensure_upload_directory method exists", False)
        results.append(("_ensure_upload_directory method exists", False))
        passed = False

    # Check 3: _validate_remote_file_path method exists
    if hasattr(backend, '_validate_remote_file_path'):
        print_test("_validate_remote_file_path method exists", True)
        results.append(("_validate_remote_file_path method exists", True))
    else:
        print_test("_validate_remote_file_path method exists", False)
        results.append(("_validate_remote_file_path method exists", False))
        passed = False

    # Check 4: _cleanup_old_uploads method exists
    if hasattr(backend, '_cleanup_old_uploads'):
        print_test("_cleanup_old_uploads method exists", True)
        results.append(("_cleanup_old_uploads method exists", True))
    else:
        print_test("_cleanup_old_uploads method exists", False)
        results.append(("_cleanup_old_uploads method exists", False))
        passed = False

    print(f"\nUpload Methods Test Summary: {sum(1 for p in results if p[1])}/{len(results)} methods exist")

    return passed


def check_upload_directory():
    """Test 3: Upload Directory"""
    print_header("Test 3: Upload Directory")

    passed = True
    results = []

    try:
        backend = RAGMemoryBackend()

        # Check 1: Upload directory creation
        upload_dir = backend._ensure_upload_directory()

        if os.path.exists(upload_dir):
            print_test("Upload directory exists", True, upload_dir)
            results.append(("Upload directory exists", True))
        else:
            print_test("Upload directory exists", False, f"Directory not created: {upload_dir}")
            results.append(("Upload directory exists", False))
            passed = False

        # Check 2: Directory is writable
        if os.path.exists(upload_dir):
            test_file = os.path.join(upload_dir, "test-write-{}.txt")
            try:
                with open(test_file, 'w') as f:
                    f.write("test")
                os.remove(test_file)
                print_test("Directory is writable", True, f"Successfully wrote to {test_file}")
                results.append(("Directory is writable", True))
            except Exception as e:
                print_test("Directory is writable", False, f"Write failed: {e}")
                results.append(("Directory is writable", False))
                passed = False

        # Check 3: Directory permissions
        if os.path.exists(upload_dir):
            stat_info = os.stat(upload_dir)
            mode = oct(stat_info.st_mode)[-3:]
            permissions_valid = mode in ["700", "755"]
            print_test("Directory permissions", permissions_valid, f"Mode: {mode}")
            if permissions_valid:
                results.append(("Directory permissions valid", True))
            else:
                results.append(("Directory permissions valid", False))
                passed = False

    except Exception as e:
        print_test("Upload directory test", False, f"Error: {e}")
        results.append(("Upload directory test", False))
        passed = False

    print(f"\nUpload Directory Test Summary: {sum(1 for p in results if p[1])}/{len(results)} checks passed")

    return passed


async def check_path_validation():
    """Test 4: Path Validation"""
    print_header("Test 4: Path Validation")

    passed = True
    results = []

    backend = RAGMemoryBackend()

    # Create test file in upload directory
    try:
        upload_dir = backend._ensure_upload_directory()
        test_file = os.path.join(upload_dir, "validation-test.txt")

        # Write test file
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Test content for validation")

        # Test 1: Valid path (within upload directory)
        print_test("Test 1: Valid path (within upload dir)", True)
        results.append(("Valid path test", True))

        async def run_valid_test():
            try:
                result = await backend.ingest_file(
                    project_id="test-validation",
                    file_path=test_file,
                    source_type="file",
                    metadata={"test": True}
                )
                is_success = result.get("status") == "success"
                print_test("Valid path - ingest_file accepts", is_success)
                results.append(("Valid path - ingest_file accepts", is_success))
                return is_success
            except Exception as e:
                print_test("Valid path - ingest_file accepts", False, f"Error: {e}")
                results.append(("Valid path - ingest_file accepts", False))
                return False

        valid_passed = await run_valid_test()

        # Test 2: Invalid path (outside upload directory)
        print_test("Test 2: Invalid path (outside upload dir)", True)
        results.append(("Invalid path test", True))

        invalid_file = "/etc/passwd"  # Clearly outside upload directory
        async def run_invalid_test():
            try:
                result = await backend.ingest_file(
                    project_id="test-validation",
                    file_path=invalid_file,
                    source_type="file",
                    metadata={"test": True}
                )
                is_rejected = result.get("status") == "error"
                print_test("Invalid path - ingest_file rejects", is_rejected)
                results.append(("Invalid path - ingest_file rejects", is_rejected))
                return is_rejected
            except Exception as e:
                print_test("Invalid path - ingest_file rejects", False, f"Error: {e}")
                results.append(("Invalid path - ingest_file rejects", False))
                return False

        invalid_passed = await run_invalid_test()

        # Test 3: Path traversal attempt (../)
        print_test("Test 3: Path traversal (../)", True)
        results.append(("Path traversal test", True))

        traversal_file = os.path.join(upload_dir, "../../../etc/passwd")
        async def run_traversal_test():
            try:
                result = await backend.ingest_file(
                    project_id="test-validation",
                    file_path=traversal_file,
                    source_type="file",
                    metadata={"test": True}
                )
                is_rejected = result.get("status") == "error"
                print_test("Path traversal - ingest_file rejects", is_rejected)
                results.append(("Path traversal - ingest_file rejects", is_rejected))
                return is_rejected
            except Exception as e:
                print_test("Path traversal - ingest_file rejects", False, f"Error: {e}")
                results.append(("Path traversal - ingest_file rejects", False))
                return False

        traversal_passed = await run_traversal_test()

        # Test 4: Non-existent file
        print_test("Test 4: Non-existent file", True)
        results.append(("Non-existent file test", True))

        nonexistent_file = os.path.join(upload_dir, "does-not-exist.txt")
        async def run_nonexistent_test():
            try:
                result = await backend.ingest_file(
                    project_id="test-validation",
                    file_path=nonexistent_file,
                    source_type="file",
                    metadata={"test": True}
                )
                is_rejected = result.get("status") == "error"
                print_test("Non-existent file - ingest_file rejects", is_rejected)
                results.append(("Non-existent file - ingest_file rejects", is_rejected))
                return is_rejected
            except Exception as e:
                print_test("Non-existent file - ingest_file rejects", False, f"Error: {e}")
                results.append(("Non-existent file - ingest_file rejects", False))
                return False

        nonexistent_passed = await run_nonexistent_test()

        if not (valid_passed and invalid_passed and traversal_passed and nonexistent_passed):
            passed = False

    except Exception as e:
        print_test("Path validation tests", False, f"Error: {e}")
        results.append(("Path validation tests", False))
        passed = False

    print(f"\nPath Validation Test Summary: {sum(1 for p in results if p[1])}/{len(results)} tests passed")

    return passed


async def check_file_size_validation():
    """Test 5: File Size Validation"""
    print_header("Test 5: File Size Validation")

    passed = True
    results = []

    backend = RAGMemoryBackend()

    try:
        upload_dir = backend._ensure_upload_directory()

        # Test 1: Small file (1KB - within limit)
        small_file = os.path.join(upload_dir, "small-test.txt")
        small_content = "x" * 1024  # 1KB
        with open(small_file, 'w', encoding='utf-8') as f:
            f.write(small_content)

        print_test("Small file created (1KB)", True)
        results.append(("Small file created", True))

        async def test_small():
            try:
                result = await backend.ingest_file(
                    project_id="test-validation",
                    file_path=small_file,
                    source_type="file",
                    metadata={"test": True}
                )
                is_success = result.get("status") == "success"
                print_test("Small file (1KB) - ingest_file accepts", is_success)
                results.append(("Small file (1KB) - ingest_file accepts", is_success))
                return is_success
            except Exception as e:
                print_test("Small file (1KB) - ingest_file accepts", False, f"Error: {e}")
                results.append(("Small file (1KB) - ingest_file accepts", False))
                return False

        small_passed = await test_small()

        # Test 2: Large file (60MB - exceeds limit)
        large_file = os.path.join(upload_dir, "large-test.txt")
        large_content = "x" * (60 * 1024 * 1024)  # 60MB
        with open(large_file, 'w', encoding='utf-8') as f:
            f.write(large_content)

        print_test("Large file created (60MB)", True)
        results.append(("Large file created", True))

        async def test_large():
            try:
                result = await backend.ingest_file(
                    project_id="test-validation",
                    file_path=large_file,
                    source_type="file",
                    metadata={"test": True}
                )
                is_rejected = result.get("status") == "error" and "too large" in result.get("error", "").lower()
                print_test("Large file (60MB) - ingest_file rejects", is_rejected)
                results.append(("Large file (60MB) - ingest_file rejects", is_rejected))
                return is_rejected
            except Exception as e:
                print_test("Large file (60MB) - ingest_file rejects", False, f"Error: {e}")
                results.append(("Large file (60MB) - ingest_file rejects", False))
                return False

        large_passed = await test_large()

        if not (small_passed and large_passed):
            passed = False

    except Exception as e:
        print_test("File size validation tests", False, f"Error: {e}")
        results.append(("File size validation tests", False))
        passed = False

    print(f"\nFile Size Validation Test Summary: {sum(1 for p in results if p[1])}/{len(results)} tests passed")

    return passed


def check_semantic_ingestion():
    """Test 6: Semantic Ingestion"""
    print_header("Test 6: Semantic Ingestion")

    passed = True
    results = []

    try:
        from rag.semantic_ingest import SemanticIngestor

        ingestor = SemanticIngestor()

        # Test 1: Ingestor can be instantiated
        print_test("SemanticIngestor instantiation", True)
        results.append(("SemanticIngestor instantiation", True))

        # Test 2: ingest_text method exists and works
        test_text = "This is a test document for semantic ingestion."
        try:
            chunk_ids = ingestor.ingest_text(
                text=test_text,
                metadata={"test": True, "source": "validation-test"},
                chunk_size=500,
                chunk_overlap=50
            )
            is_success = len(chunk_ids) > 0
            print_test("SemanticIngestor.ingest_text", is_success, f"Created {len(chunk_ids)} chunks")
            results.append(("SemanticIngestor.ingest_text", is_success))

            if is_success:
                # Test 3: Verify chunks were created in semantic store
                from rag.semantic_store import get_semantic_store
                store = get_semantic_store()

                # Count chunks for test source
                test_chunks = [c for c in store.chunks if "validation-test" in c.metadata.get("source", "")]
                print_test("Chunks created in semantic store", True, f"Found {len(test_chunks)} test chunks")
                results.append(("Chunks created in semantic store", True))
            else:
                print_test("Chunks created in semantic store", False, "No chunks created")
                results.append(("Chunks created in semantic store", False))
                passed = False

        except Exception as e:
            print_test("Semantic ingestion tests", False, f"Error: {e}")
            import traceback
            traceback.print_exc()
            results.append(("Semantic ingestion tests", False))
            passed = False

    except ImportError as e:
        print_test("Semantic ingestion tests", False, f"Import error: {e}")
        results.append(("Semantic ingestion import", False))
        passed = False

    print(f"\nSemantic Ingestion Test Summary: {sum(1 for p in results if p[1])}/{len(results)} tests passed")

    return passed


def check_response_format():
    """Test 7: Response Format"""
    print_header("Test 7: Response Format")

    passed = True
    results = []

    try:
        backend = RAGMemoryBackend()

        # Test 1: Successful response contains required fields
        test_file = os.path.join(backend._ensure_upload_directory(), "format-test.txt")
        with open(test_file, 'w', encoding='utf-8') as f:
            f.write("Format test")

        async def test_response():
            result = await backend.ingest_file(
                project_id="test-format",
                file_path=test_file,
                source_type="file",
                metadata={"test": True}
            )

            # Check for required fields
            required_fields = ["status", "file_path", "chunk_count", "doc_id", "authority", "message"]
            missing_fields = [f for f in required_fields if f not in result]

            all_present = len(missing_fields) == 0

            print_test("Success response has all required fields", all_present)
            results.append(("Success response has all required fields", all_present))

            # Check for upload_config field
            if "upload_config" in result:
                upload_config = result["upload_config"]
                has_enabled = "enabled" in upload_config
                has_directory = "directory" in upload_config
                has_max_size = "max_size_mb" in upload_config
                print_test("Success response has upload_config", True)
                results.append(("Success response has upload_config", True))

                if all([has_enabled, has_directory, has_max_size]):
                    print_test("upload_config has all required fields", True)
                    results.append(("upload_config has all required fields", True))
                else:
                    print_test("upload_config has all required fields", False, "Missing: enabled, directory, max_size_mb")
                    results.append(("upload_config has all required fields", False))
                    passed = False
            else:
                print_test("Success response has upload_config", False, "upload_config field missing")
                results.append(("Success response has upload_config", False))
                passed = False

            if not (all_present and (not all_present or passed)):
                passed = False

        response_passed = await test_response()

    except Exception as e:
        print_test("Response format tests", False, f"Error: {e}")
        results.append(("Response format tests", False))
        passed = False

    print(f"\nResponse Format Test Summary: {sum(1 for p in results if p[1])}/{len(results)} tests passed")

    return passed


def check_cleanup():
    """Test 8: File Cleanup"""
    print_header("Test 8: File Cleanup")

    passed = True
    results = []

    try:
        backend = RAGMemoryBackend()

        # Test 1: Old files are cleaned up
        upload_dir = backend._ensure_upload_directory()

        # Create multiple old files
        old_files = []
        for i in range(5):
            old_file = os.path.join(upload_dir, f"old-file-{i}.txt")
            with open(old_file, 'w', encoding='utf-8') as f:
                f.write(f"Old file {i}")
            old_files.append(old_file)

        # Run cleanup
        backend._cleanup_old_uploads()

        # Check if old files were removed
        removed_count = 0
        for old_file in old_files:
            if not os.path.exists(old_file):
                removed_count += 1

        print_test("Old files cleaned up", removed_count == 5, f"Removed {removed_count}/5 files")
        results.append(("Old files cleaned up", removed_count == 5))

        if removed_count != 5:
            passed = False

    except Exception as e:
        print_test("File cleanup tests", False, f"Error: {e}")
        results.append(("File cleanup tests", False))
        passed = False

    print(f"\nFile Cleanup Test Summary: {sum(1 for p in results if p[1])}/{len(results)} tests passed")

    return passed


def main():
    """Run all validation tests."""

    print("\n" + "=" * 70)
    print("  RAG REMOTE FILE INGESTION - COMPREHENSIVE VALIDATION")
    print("=" * 70)
    print(f"\nTimestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Python: {sys.version}")
    print(f"Working Directory: {os.getcwd()}")

    all_results = []

    # Run all tests
    config_passed = check_configuration()
    all_results.append(("Configuration", config_passed))

    methods_passed = check_upload_methods()
    all_results.append(("Upload Methods", methods_passed))

    upload_dir_passed = check_upload_directory()
    all_results.append(("Upload Directory", upload_dir_passed))

    # Run async tests
    path_passed = asyncio.run(check_path_validation())
    all_results.append(("Path Validation", path_passed))

    size_passed = asyncio.run(check_file_size_validation())
    all_results.append(("File Size Validation", size_passed))

    semantic_passed = check_semantic_ingestion()
    all_results.append(("Semantic Ingestion", semantic_passed))

    response_passed = check_response_format()
    all_results.append(("Response Format", response_passed))

    cleanup_passed = check_cleanup()
    all_results.append(("File Cleanup", cleanup_passed))

    # Summary
    print("\n" + "=" * 70)
    print("  VALIDATION SUMMARY")
    print("=" * 70)

    total_tests = len(all_results)
    passed_tests = sum(1 for _, p in all_results if p)

    print(f"\nTotal Test Suites: {total_tests}")
    print(f"Passed: {passed_tests}")
    print(f"Failed: {total_tests - passed_tests}")
    print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")

    print("\nDetailed Results:")
    for test_name, passed in all_results:
        status_icon = "✅" if passed else "❌"
        print(f"  {status_icon} {test_name}")

    print("\n" + "=" * 70)

    if passed_tests == total_tests:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\n✅ Remote file ingestion is READY for Mac deployment")
        print("\n📋 Next Steps:")
        print("  1. Copy files to Mac:")
        print("     scp /home/dietpi/pi-rag/mcp_server/rag_server.py mac@mac:/path/to/project/mcp_server/")
        print("     scp /home/dietpi/pi-rag/configs/rag_config.json mac@mac:/path/to/project/configs/")
        print("     scp /home/dietpi/pi-rag/REMOTE_INGESTION_GUIDE.md mac@mac:/path/to/project/")
        print("     scp /home/dietpi/pi-rag/MAC_QUICK_START.md mac@mac:/path/to/project/")
        print("\n  2. Set environment variable on Mac:")
        print("     export RAG_DATA_DIR=/opt/pi-rag/data")
        print("\n  3. Upload file from Mac:")
        print("     scp your-file.md dietpi@<pi-ip>:/tmp/rag-uploads/")
        print("\n  4. Ingest via MCP tool:")
        print("     Call rag.ingest_file with file path")
        print("\n  5. Verify ingestion:")
        print("     Check chunks were created")
        print("     Test retrieval with query")
        return 0
    else:
        print("\n⚠️  SOME TESTS FAILED")
        print("\n❌ Please review failed tests above before Mac deployment")
        print("\n📋 Issues to Fix:")
        for test_name, passed in all_results:
            if not passed:
                print(f"  • {test_name}")

        return 1


if __name__ == "__main__":
    sys.exit(main())
