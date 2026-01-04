"""
SYNAPSE CLI: Status Command

Check SYNAPSE system health and status.
"""

import subprocess
import httpx
import typer
from pathlib import Path


def check_mcp_server(port: int = 8002) -> dict:
    """Check if MCP server is running and healthy."""
    try:
        response = httpx.get(
            f"http://localhost:{port}/health",
            timeout=5.0
        )
        return {
            "running": True,
            "status": response.status_code,
            "healthy": response.status_code == 200
        }
    except Exception:
        return {
            "running": False,
            "status": None,
            "healthy": False
        }


def check_docker_container(container_name: str = "synapse-mcp") -> dict:
    """Check Docker container status."""
    try:
        result = subprocess.run(
            ["docker", "ps", "--filter", f"name={container_name}", "--format", "{{.Status}}"],
            capture_output=True,
            text=True,
            timeout=5
        )
        status = result.stdout.strip()
        return {
            "exists": status != "",
            "status": status
        }
    except Exception:
        return {
            "exists": False,
            "status": "unknown"
        }


def check_models(models_dir: str = "~/.synapse/models") -> dict:
    """Check for required models."""
    from pathlib import Path
    models_path = Path(models_dir).expanduser()
    
    required_models = {
        "embedding": "bge-m3-q8_0.gguf",
        "chat": "gemma-3-1b-it-UD-Q4_K_XL.gguf"
    }
    
    model_status = {}
    for model_type, filename in required_models.items():
        model_path = models_path / filename
        if model_path.exists():
            size_mb = model_path.stat().st_size / (1024 * 1024)
            model_status[model_type] = {
                "installed": True,
                "path": str(model_path),
                "size_mb": round(size_mb, 2)
            }
        else:
            model_status[model_type] = {
                "installed": False,
                "path": str(model_path),
                "size_mb": 0
            }
    
    return model_status


def check_data_directory() -> dict:
    """Check data directory status."""
    from pathlib import Path
    
    # Try common locations
    possible_dirs = [
        Path("/opt/synapse/data"),
        Path("/app/data"),
        Path.home() / ".synapse" / "data",
        Path("./data")
    ]
    
    for data_dir in possible_dirs:
        if data_dir.exists():
            return {
                "exists": True,
                "path": str(data_dir),
                "writable": os.access(data_dir, os.W_OK)
            }
    
    return {
        "exists": False,
        "path": None,
        "writable": False
    }


def check_status():
    """
    Check SYNAPSE system status.

    Displays comprehensive health check for:
    - MCP Server status
    - Docker container status (if applicable)
    - Model availability
    - Data directory status
    - Configuration status
    """
    print("🔍 SYNAPSE System Status Check")
    print("=" * 50)
    
    # Check MCP Server
    print("\n📡 MCP Server Status:")
    mcp_status = check_mcp_server()
    if mcp_status["running"] and mcp_status["healthy"]:
        print(f"  ✓ Running and healthy")
        print(f"    Port: 8002")
        print(f"    Health endpoint: /health")
    elif mcp_status["running"]:
        print(f"  ⚠️  Running but unhealthy (status code: {mcp_status['status']})")
    else:
        print(f"  ✗ Not running")
        print(f"    Start with: synapse start")
    
    # Check Docker Container
    print("\n🐳 Docker Container Status:")
    docker_status = check_docker_container()
    if docker_status["exists"]:
        status_symbol = "✓" if docker_status["status"] == "running" else "✗"
        print(f"  {status_symbol} Container: {docker_status['status']}")
    else:
        print(f"  ℹ️  Not running in Docker mode")
    
    # Check Models
    print("\n🧠 Model Status:")
    model_status = check_models()
    for model_type, status in model_status.items():
        if status["installed"]:
            print(f"  ✓ {model_type}: {status['path']} ({status['size_mb']} MB)")
        else:
            print(f"  ✗ {model_type}: Not installed")
            print(f"    Download with: synapse models download {model_type}")
    
    # Check Data Directory
    print("\n📁 Data Directory Status:")
    data_dir_status = check_data_directory()
    if data_dir_status["exists"]:
        print(f"  ✓ Path: {data_dir_status['path']}")
        writable = "✓ Writable" if data_dir_status["writable"] else "✗ Not writable"
        print(f"    {writable}")
    else:
        print(f"  ✗ Not found")
        print(f"    Run setup with: synapse setup")
    
    # Overall Status
    print("\n" + "=" * 50)
    all_healthy = (
        mcp_status["healthy"] and
        (model_status["embedding"]["installed"] or model_status["chat"]["installed"]) and
        data_dir_status["exists"] and
        data_dir_status["writable"]
    )
    
    if all_healthy:
        print("✓ SYNAPSE system is healthy and ready to use")
        print("  Query with: synapse query 'your question'")
    else:
        print("⚠️  SYNAPSE system needs attention")
        print("  See issues above and run: synapse setup")
