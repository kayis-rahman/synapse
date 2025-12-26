#!/usr/bin/env python3
"""
Model Switcher for LLaMA Server
Manages switching between Qwen3-Coder and DeepSeek-Coder models
"""

import subprocess
import signal
import sys
import time
import os
from typing import Optional, Dict, Any
import argparse
import json

class ModelSwitcher:
    def __init__(self):
        self.active_model: Optional[str] = None
        self.process: Optional[subprocess.Popen] = None
        self.llama_server = "/root/autodl-tmp/llama.cpp/build/bin/llama-server"
        self.model_configs = {
            "qwen": {
                "model_path": "/root/autodl-tmp/llama.cpp/models/Qwen3-Coder-30B-A3B-Instruct-Q5_K_M.gguf",
                "port": 6007,  # Internal port - different from API port
                "host": "127.0.0.1",  # Local interface
                "context": 131072,
                "ngl": 24,
                "flash_attn": "on",
                "ctk": "q8_0",
                "ctv": "q8_0",
                "batch_size": 512,
                "ub": 512,
                "mlock": True
            },
            "deepseek": {
                "model_path": "/root/autodl-tmp/llama.cpp/models/deepseek-coder-33b-instruct.Q5_K_M.gguf",
                "port": 6008,  # Internal port - different from API port
                "host": "127.0.0.1",  # Local interface
                "context": 32768,
                "ngl": 49,
                "flash_attn": "on",
                "ctk": "q4_0",
                "ctv": "q4_0",
                "batch_size": 512,
                "ub": 512,
                "mlock": True,
                "np": 1
            }
        }

    def start_model(self, model_name: str) -> bool:
        """Start a specific model with its configuration"""
        if model_name not in self.model_configs:
            print(f"Unknown model: {model_name}")
            return False
            
        config = self.model_configs[model_name]
        
        # Check if model file exists
        if not os.path.exists(config["model_path"]):
            print(f"Model file not found: {config['model_path']}")
            return False
            
        # Check if the same model is already running
        if self.active_model == model_name and self.process and self.process.poll() is None:
            print(f"Model {model_name} is already running")
            return True
            
        # Stop current model if running
        if self.process and self.process.poll() is None:
            print("A model is already running. Stopping it first...")
            self.stop_model()
            
        # Give a brief moment for the previous process to fully terminate
        time.sleep(0.5)
            
        # Build the command
        cmd = [
            self.llama_server,
            "-m", config["model_path"],
            "--port", str(config["port"]),
            "--host", config["host"],
            "-c", str(config["context"]),
            "-ngl", str(config["ngl"]),
            "-fa", config["flash_attn"],
            "-ctk", config["ctk"],
            "-ctv", config["ctv"],
            "-b", str(config["batch_size"]),
            "-ub", str(config["ub"])
        ]
        
        if "np" in config:
            cmd.extend(["-np", str(config["np"])])
            
        if config["mlock"]:
            cmd.append("--mlock")
            
        print(f"Starting {model_name} model with command: {' '.join(cmd)}")
        
        try:
            # Start the process
            self.process = subprocess.Popen(cmd)
            self.active_model = model_name
            print(f"Model {model_name} started successfully on port {config['port']}")
            return True
        except Exception as e:
            print(f"Failed to start model {model_name}: {e}")
            return False

    def stop_model(self) -> bool:
        """Stop the currently running model"""
        if not self.process:
            print("No model is currently running")
            return False
            
        try:
            print("Stopping the current model...")
            # Send terminate signal
            self.process.terminate()
            
            # Wait for graceful shutdown
            try:
                self.process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                print("Model did not stop gracefully, forcing termination...")
                # Force kill if it doesn't stop gracefully
                if self.process and hasattr(self.process, 'pid') and self.process.pid:
                    self.process.kill()
                self.process.wait()
                
            self.active_model = None
            self.process = None
            print("Model stopped successfully")
            return True
        except Exception as e:
            print(f"Failed to stop model: {e}")
            # Even if there's an error, clear the state
            self.active_model = None
            self.process = None
            return False

    def get_status(self) -> Dict[str, Any]:
        """Get the current status of the model switcher"""
        return {
            "active_model": self.active_model,
            "is_running": self.process is not None and self.process.poll() is None
        }

    def switch_model(self, model_name: str) -> bool:
        """Switch to a different model"""
        if self.active_model == model_name:
            print(f"Model {model_name} is already active")
            return True
            
        print(f"Switching from {self.active_model} to {model_name}")
        return self.start_model(model_name)

def main():
    switcher = ModelSwitcher()
    
    parser = argparse.ArgumentParser(description="Model Switcher for LLaMA Server")
    parser.add_argument("action", choices=["start", "stop", "switch", "status"], 
                       help="Action to perform")
    parser.add_argument("--model", choices=["qwen", "deepseek"], 
                       help="Model to switch to (required for switch action)")
    
    args = parser.parse_args()
    
    if args.action == "start":
        if args.model:
            success = switcher.start_model(args.model)
            sys.exit(0 if success else 1)
        else:
            print("Model name required for start action")
            sys.exit(1)
            
    elif args.action == "stop":
        success = switcher.stop_model()
        sys.exit(0 if success else 1)
        
    elif args.action == "switch":
        if args.model:
            success = switcher.switch_model(args.model)
            sys.exit(0 if success else 1)
        else:
            print("Model name required for switch action")
            sys.exit(1)
            
    elif args.action == "status":
        status = switcher.get_status()
        print(json.dumps(status, indent=2))
        sys.exit(0)

if __name__ == "__main__":
    main()