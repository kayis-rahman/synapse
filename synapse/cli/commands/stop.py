"""
SYNAPSE CLI: Stop Command

Stop SYNAPSE MCP server running in either Docker or native mode.
"""

import subprocess
from pathlib import Path
import typer


def stop_docker(container_name: str = "synapse-mcp") -> bool:
    """Stop SYNAPSE Docker container."""
    print(f"🐳 Stopping SYNAPSE Docker container...")
    
    try:
        # Check if running
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.stdout.strip() != "running":
            print("✓ SYNAPSE container is not running")
            return True
        
        # Stop container
        subprocess.run(
            ["docker", "compose", "-f", "docker-compose.mcp.yml", "stop"],
            check=True,
            timeout=30
        )
        print("✓ SYNAPSE container stopped successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to stop container: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Stop operation timed out")
        return False
    except FileNotFoundError:
        print("❌ Error: Docker not found in PATH")
        return False


def stop_native() -> bool:
    """Stop SYNAPSE native server."""
    print("🚀 Stopping SYNAPSE native server...")
    
    # Find and kill Python processes running the server
    try:
        subprocess.run(
            ["pkill", "-f", "mcp_server.http_wrapper"],
            check=False,
            timeout=10
        )
        print("✓ SYNAPSE native server stopped")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to stop native server: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Stop operation timed out")
        return False
    except FileNotFoundError:
        print("ℹ️  Note: pkill not available (not on macOS/Linux?)")
        print("   Server may still be running")
        return True


def stop_server() -> bool:
    """
    Stop SYNAPSE server.

    Auto-detects mode (Docker vs native) and stops appropriately.
    """
    # Try Docker first
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", "name=synapse-mcp", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        if result.stdout.strip() == "running":
            return stop_docker()
    except Exception:
        pass
    
    # Fall back to native
    return stop_native()
