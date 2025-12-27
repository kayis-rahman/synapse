#!/usr/bin/env python3
"""
Test script for external LLM integration with pi-rag.

This script tests:
1. Model manager can load external models
2. RAG orchestrator works with external models
3. Chat completions work end-to-end
"""

import sys
import os
import json

# Add the project directory to Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

from rag import get_model_manager, get_orchestrator

def test_model_manager_external():
    """Test that model manager can handle external models."""
    print("Testing Model Manager with external models...")
    
    try:
        manager = get_model_manager()
        
        # Check if external model is registered
        model_info = manager.get_model_info("external_chat")
        print("External model info: " + str(model_info))
        
        if model_info and model_info.get("is_external"):
            print("[PASS] External model is properly registered")
        else:
            print("[FAIL] External model registration failed")
            return False
            
        return True
        
    except Exception as e:
        print("[FAIL] Model manager test failed: " + str(e))
        return False

def test_orchestrator_external():
    """Test that RAG orchestrator works with external models."""
    print("\nTesting RAG Orchestrator with external models...")
    
    try:
        orchestrator = get_orchestrator()
        
        # Test a simple chat completion
        messages = [
            {"role": "user", "content": "Hello! Please respond with 'Test successful'"}
        ]
        
        print("Sending test message to external model...")
        result = orchestrator.chat(
            messages=messages,
            model_name="external_chat",
            temperature=0.1,
            max_tokens=50
        )
        
        print("Response content: " + str(result.get('content', 'No content')))
        print("RAG used: " + str(result.get('rag_used', False)))
        print("Model: " + str(result.get('model', 'Unknown')))
        
        if result.get('content'):
            print("[PASS] Chat completion successful")
            return True
        else:
            print("[FAIL] Chat completion failed - no content")
            return False
            
    except Exception as e:
        print("[FAIL] Orchestrator test failed: " + str(e))
        import traceback
        traceback.print_exc()
        return False

def test_configuration():
    """Test that configuration files are properly loaded."""
    print("\nTesting configuration files...")
    
    try:
        # Test models config
        with open("configs/models_config.json", "r") as f:
            models_config = json.load(f)
        
        external_model = models_config["models"].get("external_chat")
        if external_model and external_model.get("is_external"):
            print("[PASS] External model configuration is correct")
        else:
            print("[FAIL] External model configuration is incorrect")
            return False
        
        # Test RAG config
        with open("configs/rag_config.json", "r") as f:
            rag_config = json.load(f)
        
        if "external_chat_api_url" in rag_config:
            print("[PASS] RAG configuration includes external API settings")
        else:
            print("[FAIL] RAG configuration missing external API settings")
            return False
            
        return True
        
    except Exception as e:
        print("[FAIL] Configuration test failed: " + str(e))
        return False

def main():
    """Run all tests."""
    print("=" * 60)
    print("Testing External LLM Integration with pi-rag")
    print("=" * 60)
    
    tests = [
        ("Configuration", test_configuration),
        ("Model Manager", test_model_manager_external),
        ("RAG Orchestrator", test_orchestrator_external),
    ]
    
    results = []
    for test_name, test_func in tests:
        print("\n" + test_name + " Test:")
        print("-" * 40)
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print("[FAIL] " + test_name + " test failed with exception: " + str(e))
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(test_name + ": " + status)
        if result:
            passed += 1
    
    print("\nTests passed: " + str(passed) + "/" + str(total))
    
    if passed == total:
        print("[SUCCESS] All tests passed! External LLM integration is working correctly.")
        return 0
    else:
        print("[ERROR] Some tests failed. Please check the errors above.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)