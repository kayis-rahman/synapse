#!/usr/bin/env python3
"""
Phase 1 Test: P0-1 synapse setup

Tests setup command in multiple environments with assertions.
"""

import subprocess
import sys
from pathlib import Path
from conftest import (
    run_command, assert_success, assert_output_contains,
    assert_directory_exists, check_docker_container,
    record_test_result, print_test_summary, print_success_rate,
    TIMEOUTS, ENVIRONMENTS
)


def test_setup_1_docker() -> None:
    """Test Setup-1: Docker Auto-Detection"""
    test_name = "Setup-1: Docker Auto-Detection"

    # Skip if Docker container not running
    if not check_docker_container():
        print(f"⏭️  {test_name}: SKIPPED (Docker container not running)")
        return

    # Build command
    env = ENVIRONMENTS["docker"]
    command = env["command_prefix"] + ["synapse", "setup", "--no-model-check"]

    try:
        # Run command
        exit_code, stdout, stderr, duration = run_command(
            command,
            timeout=TIMEOUTS["setup"]
        )

        # Assert success
        assert_success(test_name, exit_code, stdout, stderr, TIMEOUTS["setup"])

        # Assert output contains expected text
        assert_output_contains(test_name, stdout, "Auto-detected Docker data directory")

        # Assert directories exist
        assert_directory_exists(test_name, env["data_dir"])
        assert_directory_exists(test_name, env["data_dir"] + "/models")
        assert_directory_exists(test_name, env["data_dir"] + "/rag_index")

        # Record result
        record_test_result(
            test_id="setup-1-docker",
            name=test_name,
            command=" ".join(command),
            environment="docker",
            exit_code=exit_code,
            stdout=stdout[:200],  # Truncate for storage
            stderr=stderr[:200],
            duration=duration,
            timeout=TIMEOUTS["setup"],
            passed=True
        )

    except AssertionError as e:
        record_test_result(
            test_id="setup-1-docker",
            name=test_name,
            command=" ".join(command),
            environment="docker",
            exit_code=-1,
            stdout="",
            stderr=str(e),
            duration=0,
            timeout=TIMEOUTS["setup"],
            passed=False
        )
        raise


def test_setup_2_native() -> None:
    """Test Setup-2: Native Auto-Detection"""
    test_name = "Setup-2: Native Auto-Detection"

    # Build command
    env = ENVIRONMENTS["native"]
    command = env["command_prefix"] + ["synapse", "setup", "--no-model-check"]

    try:
        # Run command
        exit_code, stdout, stderr, duration = run_command(
            command,
            timeout=TIMEOUTS["setup"]
        )

        # Assert success
        assert_success(test_name, exit_code, stdout, stderr, TIMEOUTS["setup"])

        # Assert output contains expected text
        assert_output_contains(test_name, stdout, "Auto-detected native data directory")

        # Assert directories exist
        assert_directory_exists(test_name, env["data_dir"])
        assert_directory_exists(test_name, env["data_dir"] + "/models")

        # Record result
        record_test_result(
            test_id="setup-2-native",
            name=test_name,
            command=" ".join(command),
            environment="native",
            exit_code=exit_code,
            stdout=stdout[:200],
            stderr=stderr[:200],
            duration=duration,
            timeout=TIMEOUTS["setup"],
            passed=True
        )

    except AssertionError as e:
        record_test_result(
            test_id="setup-2-native",
            name=test_name,
            command=" ".join(command),
            environment="native",
            exit_code=-1,
            stdout="",
            stderr=str(e),
            duration=0,
            timeout=TIMEOUTS["setup"],
            passed=False
        )
        raise


def test_setup_3_user_home() -> None:
    """Test Setup-3: User Home Auto-Detection"""
    test_name = "Setup-3: User Home Auto-Detection"

    # Build command
    env = ENVIRONMENTS["user_home"]
    command = env["command_prefix"] + ["synapse", "setup", "--no-model-check"]

    try:
        # Run command
        exit_code, stdout, stderr, duration = run_command(
            command,
            timeout=TIMEOUTS["setup"]
        )

        # Assert success
        assert_success(test_name, exit_code, stdout, stderr, TIMEOUTS["setup"])

        # Assert output contains expected text
        assert_output_contains(test_name, stdout, "Auto-detected user home data directory")

        # Assert directories exist
        assert_directory_exists(test_name, env["data_dir"])
        assert_directory_exists(test_name, env["data_dir"] + "/models")

        # Record result
        record_test_result(
            test_id="setup-3-user-home",
            name=test_name,
            command=" ".join(command),
            environment="user_home",
            exit_code=exit_code,
            stdout=stdout[:200],
            stderr=stderr[:200],
            duration=duration,
            timeout=TIMEOUTS["setup"],
            passed=True
        )

    except AssertionError as e:
        record_test_result(
            test_id="setup-3-user-home",
            name=test_name,
            command=" ".join(command),
            environment="user_home",
            exit_code=-1,
            stdout="",
            stderr=str(e),
            duration=0,
            timeout=TIMEOUTS["setup"],
            passed=False
        )
        raise


def test_setup_4_force() -> None:
    """Test Setup-4: Force Re-Setup"""
    test_name = "Setup-4: Force Re-Setup"

    # Build command
    env = ENVIRONMENTS["native"]
    command = env["command_prefix"] + ["synapse", "setup", "--force", "--no-model-check"]

    try:
        # Run command
        exit_code, stdout, stderr, duration = run_command(
            command,
            timeout=TIMEOUTS["setup"]
        )

        # Assert success
        assert_success(test_name, exit_code, stdout, stderr, TIMEOUTS["setup"])

        # Assert output contains success message
        assert_output_contains(test_name, stdout, "SYNAPSE setup complete!")

        # Record result
        record_test_result(
            test_id="setup-4-force",
            name=test_name,
            command=" ".join(command),
            environment="native",
            exit_code=exit_code,
            stdout=stdout[:200],
            stderr=stderr[:200],
            duration=duration,
            timeout=TIMEOUTS["setup"],
            passed=True
        )

    except AssertionError as e:
        record_test_result(
            test_id="setup-4-force",
            name=test_name,
            command=" ".join(command),
            environment="native",
            exit_code=-1,
            stdout="",
            stderr=str(e),
            duration=0,
            timeout=TIMEOUTS["setup"],
            passed=False
        )
        raise


def test_setup_5_offline() -> None:
    """Test Setup-5: Offline Mode"""
    test_name = "Setup-5: Offline Mode"

    # Build command
    env = ENVIRONMENTS["native"]
    command = env["command_prefix"] + ["synapse", "setup", "--offline", "--no-model-check"]

    try:
        # Run command
        exit_code, stdout, stderr, duration = run_command(
            command,
            timeout=TIMEOUTS["setup"]
        )

        # Assert success
        assert_success(test_name, exit_code, stdout, stderr, TIMEOUTS["setup"])

        # Assert output mentions offline mode
        assert_output_contains(test_name, stdout, "offline mode")

        # Record result
        record_test_result(
            test_id="setup-5-offline",
            name=test_name,
            command=" ".join(command),
            environment="native",
            exit_code=exit_code,
            stdout=stdout[:200],
            stderr=stderr[:200],
            duration=duration,
            timeout=TIMEOUTS["setup"],
            passed=True
        )

    except AssertionError as e:
        record_test_result(
            test_id="setup-5-offline",
            name=test_name,
            command=" ".join(command),
            environment="native",
            exit_code=-1,
            stdout="",
            stderr=str(e),
            duration=0,
            timeout=TIMEOUTS["setup"],
            passed=False
        )
        raise


def main():
    """Main test execution."""
    print(f"\n{'=' * 60}")
    print(f"Phase 1 Test: P0-1 synapse setup")
    print(f"{'=' * 60}\n")

    tests = [
        ("Setup-1: Docker Auto-Detection", test_setup_1_docker),
        ("Setup-2: Native Auto-Detection", test_setup_2_native),
        ("Setup-3: User Home Auto-Detection", test_setup_3_user_home),
        ("Setup-4: Force Re-Setup", test_setup_4_force),
        ("Setup-5: Offline Mode", test_setup_5_offline),
    ]

    try:
        # Run all tests
        for test_name, test_func in tests:
            print(f"\n{'-' * 60}")
            print(f"Running: {test_name}")
            print(f"{'-' * 60}")
            try:
                test_func()
                print(f"✅ {test_name}: PASSED")
            except Exception as e:
                print(f"❌ {test_name}: FAILED - {str(e)[:100]}")

    except KeyboardInterrupt:
        print("\n\n⚠️  Tests interrupted by user")
        sys.exit(2)

    # Print summary
    print_test_summary()

    # Exit with appropriate code
    exit_code = print_success_rate()
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
