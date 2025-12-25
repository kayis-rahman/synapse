#!/usr/bin/env python3
"""
Test script for the model switcher functionality
"""

import subprocess
import time
import sys
import os

def test_model_switcher():
    """Test that the model switcher works correctly"""
    
    # Check if the switcher script exists
    switcher_path = "./model_switcher.py"
    if not os.path.exists(switcher_path):
        print("Error: model_switcher.py not found")
        return False
        
    # Test status
    print("Testing status command...")
    try:
        result = subprocess.run([sys.executable, switcher_path, "status"], 
                              capture_output=True, text=True, timeout=10)
        print(f"Status output: {result.stdout}")
        if result.stderr:
            print(f"Status errors: {result.stderr}")
    except Exception as e:
        print(f"Error running status: {e}")
        return False
        
    # Test starting qwen model
    print("\nTesting start qwen model...")
    try:
        result = subprocess.run([sys.executable, switcher_path, "start", "--model", "qwen"], 
                              capture_output=True, text=True, timeout=30)
        print(f"Start Qwen output: {result.stdout}")
        if result.stderr:
            print(f"Start Qwen errors: {result.stderr}")
    except Exception as e:
        print(f"Error starting Qwen model: {e}")
        return False
        
    # Wait a bit for the model to start
    time.sleep(3)
    
    # Test status again
    print("\nTesting status after starting Qwen...")
    try:
        result = subprocess.run([sys.executable, switcher_path, "status"], 
                              capture_output=True, text=True, timeout=10)
        print(f"Status output: {result.stdout}")
    except Exception as e:
        print(f"Error running status: {e}")
        return False
        
    # Test stopping model
    print("\nTesting stop command...")
    try:
        result = subprocess.run([sys.executable, switcher_path, "stop"], 
                              capture_output=True, text=True, timeout=10)
        print(f"Stop output: {result.stdout}")
        if result.stderr:
            print(f"Stop errors: {result.stderr}")
    except Exception as e:
        print(f"Error stopping model: {e}")
        return False
        
    # Test switching to deepseek
    print("\nTesting switch to deepseek model...")
    try:
        result = subprocess.run([sys.executable, switcher_path, "switch", "--model", "deepseek"], 
                              capture_output=True, text=True, timeout=30)
        print(f"Switch to DeepSeek output: {result.stdout}")
        if result.stderr:
            print(f"Switch to DeepSeek errors: {result.stderr}")
    except Exception as e:
        print(f"Error switching to DeepSeek model: {e}")
        return False
    
    print("\nAll tests completed successfully!")
    return True

if __name__ == "__main__":
    test_model_switcher()