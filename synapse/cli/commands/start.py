"""
SYNAPSE CLI: Start Command

Start SYNAPSE MCP server in either Docker or native mode.
"""

import subprocess
import sys
import os
from pathlib import Path
import typer
from typing import Optional


def check_docker_running(container_name: str = "synapse-mcp") -> bool:
    """Check if Docker container is running."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        return result.stdout.strip() == "running"
    except Exception:
        return False


def start_docker(docker_compose_file: str = "docker-compose.mcp.yml", port: int = 8002) -> bool:
    """Start SYNAPSE server in Docker mode."""
    print(f"🐳 Starting SYNAPSE server in Docker mode on port {port}...")
    
    # Check if already running
    if check_docker_running():
        print("✓ SYNAPSE container is already running")
        print("  Use 'synapse status' to check health")
        return True
    
    # Check for docker-compose file
    compose_file = Path(docker_compose_file)
    if not compose_file.exists():
        # Try common locations
        possible_locations = [
            Path(docker_compose_file),
            Path("docker-compose.synapse.yml"),
            Path("docker-compose.yml"),
            Path("docker-compose.mcp.yml")
        ]
        
        compose_file = None
        for loc in possible_locations:
            if loc.exists():
                compose_file = loc
                break
        
        if compose_file is None:
            print(f"❌ Error: Docker compose file not found")
            print(f"   Searched for: {docker_compose_file}")
            print(f"   Please ensure you're in the synapse directory")
            return False
    
    # Start container
    try:
        subprocess.run(
            ["docker", "compose", "-f", str(compose_file), "up", "-d"],
            check=True,
            timeout=60
        )
        print(f"✓ SYNAPSE server started successfully")
        print(f"  Docker container: synapse-mcp")
        print(f"  Port: {port}")
        print(f"  Health check: http://localhost:{port}/health")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start Docker container: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Docker start timed out")
        return False
    except FileNotFoundError:
        print("❌ Error: Docker not found in PATH")
        print("   Please install Docker: https://docs.docker.com/get-docker/")
        return False


def start_native(port: int = 8002) -> bool:
    """Start SYNAPSE server in native (Python) mode."""
    print(f"🚀 Starting SYNAPSE server in native mode on port {port}...")
    
    # Start HTTP server
    try:
        subprocess.run(
            ["python", "-m", "mcp_server.http_wrapper"],
            check=True,
            timeout=30
        )
        print(f"✓ SYNAPSE server started successfully")
        print(f"  Port: {port}")
        print(f"  Health check: http://localhost:{port}/health")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start native server: {e}")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Server start timed out")
        return False
    except FileNotFoundError:
        print("❌ Error: Python not found in PATH")
        return False


def start_server(docker: bool = False, port: int = 8002) -> bool:
    """
    Start SYNAPSE server.

    Automatically detects best mode (Docker vs native) if not specified.
    """
    # Auto-detect mode
    if docker is None:
        # Check if Docker is available
        try:
            subprocess.run(["docker", "--version"], capture_output=True, timeout=5)
            # Check if docker-compose file exists
            compose_files = [
                "docker-compose.mcp.yml",
                "docker-compose.synapse.yml",
                "docker-compose.yml"
            ]
            has_compose = any(Path(f).exists() for f in compose_files)
            
            if has_compose:
                docker = True
                print("ℹ️  Auto-detected Docker mode")
            else:
                docker = False
                print("ℹ️  Auto-detected native mode (no docker-compose file found)")
        except Exception:
            docker = False
            print("ℹ️  Auto-detected native mode (Docker not available)")
    
    if docker:
        return start_docker(port=port)
    else:
        return start_native(port=port)
