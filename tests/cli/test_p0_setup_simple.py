#!/usr/bin/env python3
"""
Phase 1 Test: P0-1 synapse setup (Simple Version)

Simplified test using direct function calls without complex imports.
"""

import sys
import subprocess

# Simple timeout configuration
TIMEOUTS = {
    "setup": 60,
    "config": 2,
    "models_list": 2
}


def run_setup_command(args):
    """Run synapse setup command with given arguments"""
    cmd = ["python3", "-c", "from synapse.cli.commands.setup import run_setup; run_setup(" + args + ")"]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=TIMEOUTS["setup"]
        )
        return result.returncode, result.stdout, result.stderr
    except subprocess.TimeoutExpired:
        return -1, "", f"Command timed out after {TIMEOUTS['setup']}s", ""
    except Exception as e:
        return -1, "", str(e), ""


def test_setup_2_native():
    """Test Setup-2: Native Auto-Detection"""
    print("\n" + "="*60)
    print("Testing: Setup-2: Native Auto-Detection")
    print("="*60)

    # Run setup with --no-model-check
    exit_code, stdout, stderr = run_setup_command("--no-model-check")

    if exit_code != 0:
        print(f"❌ FAILED - Exit code {exit_code}")
        print(f"STDERR:\n{stderr}")
        return False

    # Check for expected output
    if "Auto-detected native data directory" not in stdout:
        print(f"❌ FAILED - Output doesn't contain 'Auto-detected native data directory'")
        print(f"STDOUT:\n{stdout[:500]}")
        return False

    if "/opt/synapse/data" not in stdout:
        print(f"❌ FAILED - Output doesn't contain '/opt/synapse/data'")
        print(f"STDOUT:\n{stdout[:500]}")
        return False

    # Check for data directory
    if not stdout.startswith("ℹ️  Auto-detected native data directory: /opt/synapse/data"):
        print(f"❌ FAILED - Wrong data directory detected")
        return False

    # Check for models directory
    if "/opt/synapse/data/models" not in stdout:
        print(f"❌ FAILED - Models directory not mentioned")
        return False

    print("✅ PASSED - Native auto-detection works")
    print("  Data directory: /opt/synapse/data")
    print("  Models directory: /opt/synapse/data/models")
    return True


def test_setup_5_offline():
    """Test Setup-5: Offline Mode"""
    print("\n" + "="*60)
    print("Testing: Setup-5: Offline Mode")
    print("="*60)

    # Run setup with --offline --no-model-check
    exit_code, stdout, stderr = run_setup_command("--offline --no-model-check")

    if exit_code != 0:
        print(f"❌ FAILED - Exit code {exit_code}")
        print(f"STDERR:\n{stderr}")
        return False

    # Check for offline mode mention
    if "offline mode" not in stdout:
        print(f"❌ FAILED - Output doesn't mention 'offline mode'")
        print(f"STDOUT:\n{stdout[:500]}")
        return False

    print("✅ PASSED - Offline mode works")
    return True


def main():
    """Main test execution"""
    print("\n" + "="*60)
    print("Phase 1 Test: P0-1 synapse setup (Simple)")
    print("="*60)

    tests = [
        ("Setup-2: Native Auto-Detection", test_setup_2_native),
        ("Setup-5: Offline Mode", test_setup_5_offline),
    ]

    results = []
    for test_name, test_func in tests:
        try:
            passed = test_func()
            results.append((test_name, passed))
        except Exception as e:
            print(f"❌ {test_name}: EXCEPTION - {str(e)[:100]}")
            results.append((test_name, False))

    # Print summary
    print("\n" + "="*60)
    print("Test Summary")
    print("="*60)

    passed_count = sum(1 for _, passed in results if passed)
    total_count = len(results)
    success_rate = (passed_count / total_count * 100) if total_count > 0 else 0

    print(f"Total tests: {total_count}")
    print(f"Passed: {passed_count}")
    print(f"Failed: {total_count - passed_count}")
    print(f"Success rate: {success_rate:.1f}%")

    print("\n" + "="*60)

    # Exit with appropriate code
    sys.exit(0 if passed_count == total_count else 1)


if __name__ == "__main__":
    main()
