#!/usr/bin/env python3
"""
Docker Orchestration Script - Test Environment Management

This script orchestrates Docker containers for RAG MCP reliability testing.
Provides functions to start/stop/restart containers, collect metrics, and manage volumes.

Usage:
    python docker_orchestrate.py start
    python docker_orchestrate.py stop
    python docker_orchestrate.py restart
    python docker_orchestrate.py simulate_disk_full
    python docker_orchestrate.py collect_metrics
"""

import asyncio
import subprocess
import json
import os
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime


class DockerOrchestrator:
    """Manage Docker containers for RAG MCP testing."""
    
    def __init__(self, compose_file: str = "docker-compose.test.yml"):
        """Initialize Docker orchestrator."""
        self.compose_file = compose_file
        self.base_dir = Path(__file__).parent.parent
        self.test_output_dir = self.base_dir / "test_output"
        self.test_output_dir.mkdir(exist_ok=True)
    
    async def start_environment(self, service_name: str = "rag-mcp-test") -> Dict[str, Any]:
        """Start Docker test environment."""
        print(f"[Orchestrator] Starting test environment: {service_name}")
        
        try:
            # Start test compose environment
            result = subprocess.run(
                ["docker-compose", "-f", self.compose_file, "up", "-d", service_name],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            
            # Wait for service to be ready
            await asyncio.sleep(5)
            
            # Check if container is running
            status_result = subprocess.run(
                ["docker-compose", "-f", self.compose_file, "ps", service_name],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            
            is_running = service_name in status_result.stdout
            
            return {
                "status": "success" if is_running else "error",
                "service": service_name,
                "logs": result.stdout,
                "message": f"Environment started (running={is_running})"
            }
        except Exception as e:
            return {
                "status": "error",
                "service": service_name,
                "error": str(e),
                "message": f"Failed to start environment: {e}"
            }
    
    async def stop_container(self, service_name: str = "rag-mcp-test", signal: str = "SIGTERM") -> Dict[str, Any]:
        """Stop Docker container."""
        print(f"[Orchestrator] Stopping container: {service_name} (signal: {signal})")
        
        try:
            result = subprocess.run(
                ["docker-compose", "-f", self.compose_file, "kill", signal, service_name],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            
            return {
                "status": "success",
                "service": service_name,
                "logs": result.stdout,
                "message": f"Container stopped"
            }
        except Exception as e:
            return {
                "status": "error",
                "service": service_name,
                "error": str(e),
                "message": f"Failed to stop container: {e}"
            }
    
    async def kill_container(self, service_name: str = "rag-mcp-test") -> Dict[str, Any]:
        """Force kill container (SIGKILL)."""
        print(f"[Orchestrator] Force killing container: {service_name}")
        
        try:
            result = subprocess.run(
                ["docker-compose", "-f", self.compose_file, "kill", "-s", "SIGKILL", service_name],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            
            return {
                "status": "success",
                "service": service_name,
                "logs": result.stdout,
                "message": f"Container force killed"
            }
        except Exception as e:
            return {
                "status": "error",
                "service": service_name,
                "error": str(e),
                "message": f"Failed to kill container: {e}"
            }
    
    async def restart_container(self, service_name: str = "rag-mcp-test") -> Dict[str, Any]:
        """Gracefully restart container."""
        print(f"[Orchestrator] Restarting container: {service_name}")
        
        try:
            # Stop
            stop_result = await self.stop_container(service_name)
            
            # Wait
            await asyncio.sleep(3)
            
            # Start
            start_result = await self.start_environment(service_name)
            
            # Wait for restart
            await asyncio.sleep(5)
            
            return {
                "status": "success",
                "service": service_name,
                "stop_result": stop_result,
                "start_result": start_result,
                "message": "Container restarted"
            }
        except Exception as e:
            return {
                "status": "error",
                "service": service_name,
                "error": str(e),
                "message": f"Failed to restart container: {e}"
            }
    
    async def container_logs(self, service_name: str = "rag-mcp-test", lines: int = 100) -> str:
        """Get container logs."""
        print(f"[Orchestrator] Getting logs from {service_name}")
        
        try:
            result = subprocess.run(
                ["docker-compose", "-f", self.compose_file, "logs", "--tail", str(lines), service_name],
                cwd=self.base_dir,
                capture_output=True,
                text=True
            )
            
            return {
                "status": "success",
                "logs": result.stdout,
                "lines_returned": lines,
                "message": f"Retrieved last {lines} log lines"
            }
        except Exception as e:
            return {
                "status": "error",
                "logs": "",
                "error": str(e),
                "message": f"Failed to get logs: {e}"
            }
    
    async def get_container_stats(self, service_name: str = "rag-mcp-test") -> Dict[str, Any]:
        """Get container stats (CPU, memory)."""
        print(f"[Orchestrator] Getting stats for {service_name}")
        
        try:
            result = subprocess.run(
                ["docker", "stats", "--format", "json", service_name],
                capture_output=True,
                text=True
            )
            
            stats = json.loads(result.stdout) if result.stdout else {}
            
            return {
                "status": "success",
                "stats": stats,
                "message": f"Stats retrieved"
            }
        except Exception as e:
            return {
                "status": "error",
                "stats": {},
                "error": str(e),
                "message": f"Failed to get stats: {e}"
            }
    
    async def create_test_volume_snapshot(self) -> str:
        """Create snapshot of test volumes."""
        print(f"[Orchestrator] Creating snapshot of test volumes")
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        snapshot_path = self.base_dir / f"test_snapshots/snapshot_{timestamp}.tar.gz"
        snapshot_path.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            subprocess.run([
                "tar", "-czf", str(snapshot_path),
                "data/test_memory",
                "data/test_semantic_index",
                "data/test_episodic.db"
                "data/test_output"
            ], cwd=self.base_dir)
            
            return str(snapshot_path)
        except Exception as e:
            return f"Failed to create snapshot: {e}"
    
    async def restore_test_volume(self, snapshot_path: str) -> Dict[str, Any]:
        """Restore test volumes from snapshot."""
        print(f"[Orchestrator] Restoring test volumes from: {snapshot_path}")
        
        try:
            subprocess.run([
                "tar", "-xzf", snapshot_path, "-C", str(self.base_dir.parent)
            ], cwd=self.base_dir.parent)
            
            return {
                "status": "success",
                "message": f"Volumes restored from {snapshot_path}"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "message": f"Failed to restore volumes: {e}"
            }
    
    async def collect_metrics(self, service_name: str = "rag-mcp-test") -> Dict[str, Any]:
        """Collect metrics from test-collector service."""
        print(f"[Orchestrator] Collecting metrics from {service_name}")
        
        try:
            result = subprocess.run([
                "curl", "-s", "http://localhost:8080/metrics", 
                "|", "grep", "\"total_calls\""
            ], capture_output=True, text=True)
            
            lines = result.stdout.strip().split('\n') if result.stdout else []
            
            # Parse metrics
            metrics_data = {}
            for line in lines:
                if 'total_calls' in line and ':' in line:
                    key, value = line.split(':', 1)
                    metrics_data[key.strip()] = value.strip()
            
            return {
                "status": "success",
                "metrics": metrics_data,
                "lines": len(lines),
                "message": f"Collected {len(lines)} metrics lines"
            }
        except Exception as e:
            return {
                "status": "error",
                "metrics": {},
                "error": str(e),
                "message": f"Failed to collect metrics: {e}"
            }
    
    async def clean_test_volumes(self) -> str:
        """Clean up test volumes (remove snapshots, clear logs)."""
        print(f"[Orchestrator] Cleaning test volumes")
        
        try:
            # Stop container if running
            await self.stop_container()
            
            # Remove test output
            import shutil
            if self.test_output_dir.exists():
                shutil.rmtree(self.test_output_dir)
                self.test_output_dir.mkdir(exist_ok=True)
            
            # Clean snapshots
            snapshots_dir = self.base_dir / "test_snapshots"
            if snapshots_dir.exists():
                shutil.rmtree(snapshots_dir)
                snapshots_dir.mkdir(exist_ok=True)
            
            # Recreate directories
            for dir_name in ["test_memory", "test_semantic_index", "test_episodic.db"]:
                dir_path = self.base_dir / "data" / dir_name
                if dir_path.exists():
                    shutil.rmtree(dir_path)
                dir_path.mkdir(exist_ok=True)
            
            return "Test volumes cleaned"
        except Exception as e:
            return f"Failed to clean volumes: {e}"


# Singleton instance
_orchestrator: Optional[DockerOrchestrator] = None

def get_orchestrator(compose_file: str = "docker-compose.test.yml") -> DockerOrchestrator:
    """
    Get or create Docker orchestrator singleton.
    
    Args:
        compose_file: Path to docker-compose test file
    
    Returns:
        DockerOrchestrator instance
    """
    global _orchestrator
    if _orchestrator is None:
        _orchestrator = DockerOrchestrator(compose_file)
    return _orchestrator


async def run_docker_compose(command: str) -> subprocess.CompletedProcess:
    """
    Run docker-compose command and return result.
    """
    result = subprocess.run(
        ["docker-compose", "-f", command],
        cwd=Path(__file__).parent,
        capture_output=True,
        text=True
    )
    return result


async def start_environment():
    """Start test environment."""
    orchestrator = get_orchestrator()
    result = await orchestrator.start_environment()
    print(json.dumps(result, indent=2))


async def stop_environment():
    """Stop test environment."""
    orchestrator = get_orchestrator()
    result = await orchestrator.stop_container()
    print(json.dumps(result, indent=2))


async def restart_environment():
    """Restart test environment."""
    orchestrator = get_orchestrator()
    result = await orchestrator.restart_container()
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        command = sys.argv[1]
        if command == "start":
            asyncio.run(start_environment())
        elif command == "stop":
            asyncio.run(stop_environment())
        elif command == "restart":
            asyncio.run(restart_environment())
        else:
            print(f"Unknown command: {command}")
    else:
        asyncio.run(start_environment())
