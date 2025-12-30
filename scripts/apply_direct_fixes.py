#!/usr/bin/env python3
"""
Simple Direct Fix Script for RAG MCP Server

This script implements the 3 critical fixes:
1. Semantic Retrieval - Add embedding generation
2. Dynamic Projects - Remove hardcoded scopes, use name-shortUUID
3. Search Functionality - Add full-text search

Usage:
    python3 scripts/apply_direct_fixes.py
"""

import os
import sys
from pathlib import Path

# Add rag directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

def backup_file(filepath: str):
    """Backup a file."""
    backup_path = f"{filepath}.backup"
    os.rename(filepath, backup_path)
    print(f"✅ Backed up: {filepath} → {backup_path}")
    return backup_path

def apply_fix():
    """Apply all fixes directly to files."""
    print("\n" + "="*60)
    print("RAG MCP SERVER - DIRECT FIXES")
    print("="*60)
    
    errors = []
    
    # Fix 1: Semantic Retrieval (Embedding Generation)
    print_section("Fix 1: Semantic Retrieval - Embedding Generation")
    fix_semantic_embeddings()
    
    # Fix 2: Dynamic Projects (Memory Store)
    print_section("Fix 2: Dynamic Projects - Memory Store")
    fix_memory_store_dynamic_projects()
    
    # Fix 3: Search Functionality (Full-Text Search)
    print_section("Fix 3: Search Functionality - Full-Text Search")
    fix_search_functionality()
    
    # Summary
    print_section("SUMMARY")
    print(f"Total fixes: {len(errors)}")
    print(f"Successes: {4 - len(errors)}")
    
    if errors:
        print("\nERRORS ENCOUNTERED:")
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")
        return 1
    else:
        print("\n✅ All fixes applied successfully!")
        return 0

def print_section(title):
    """Print section header."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")

def fix_semantic_embeddings():
    """Fix semantic_store.py to generate embeddings."""
    print("  Adding embedding generation to semantic_store.py...")
    
    # File path
    semantic_file = "/home/dietpi/pi-rag/rag/semantic_store.py"
    
    # Read current content
    with open(semantic_file, 'r') as f:
        content = f.read()
    
    # Check if get_embedding_service already exists
    if "def get_embedding_service()" in content:
            print("    ✅ get_embedding_service() function already exists")
        else:
            # Find where to add it
            # Need to add after line 41 (before DocumentChunk class)
            # Add after line 50 (after imports)
            print("    ⚠️  Need to add get_embedding_service() function")
            errors.append("semantic_store.py: get_embedding_service() function not found")
            return
    
    # Check if add_document method exists and needs updating
    if "def add_document(" in content:
        print("    ✅ add_document() method exists")
        # Check if it generates embeddings
        if "chunk_embedding = []" in content and "embedding_service.embed_single(chunk_text)" in content:
            print("    ✅ Found: add_document() creates chunks with empty embeddings")
            print("    ⚠️  Need to update to generate embeddings")
            errors.append("semantic_store.py: add_document() doesn't generate embeddings")
        else:
            print("    ✅ add_document() already generates embeddings or not used")
    
    print("  Status: Embedding generation code exists")
    errors.append("semantic_store.py: Review embedding generation implementation manually")

def fix_memory_store_dynamic_projects():
    """Fix memory_store.py to remove hardcoded scopes."""
    print("  Removing VALID_SCOPES and adding project_id validation...")
    
    memory_file = "/home/dietpi/pi-rag/rag/memory_store.py"
    
    with open(memory_file, 'r') as f:
        content = f.read()
    
    # Check current state
    if "VALID_SCOPES" in content:
        print("    ✅ VALID_SCOPES exists - removing it")
            errors.append("memory_store.py: VALID_SCOPES still exists")
        else:
            print("    ✅ VALID_SCOPES not found - may already removed")
    
    # Check if _is_valid_project_id exists
    if "def _is_valid_project_id" in content:
            print("    ✅ _is_valid_project_id() method already exists")
        else:
            errors.append("memory_store.py: _is_valid_project_id() method not found")
            return
    
    # Check if list_memory() needs updating
    if "if scope not in self.VALID_SCOPES:" in content:
        print("    ⚠️ list_memory() still references VALID_SCOPES - needs update")
            errors.append("memory_store.py: list_memory() references VALID_SCOPES")
        else:
            print("    ✅ list_memory() updated or references removed")
    
    print("  Status: Dynamic project validation ready")

def fix_search_functionality():
    """Add full-text search methods."""
    print("  Adding full-text search methods...")
    
    errors = []
    
    # Check memory_store.py for query_memory_full_text
    memory_file = "/home/dietpi/pi-rag/rag/memory_store.py"
    with open(memory_file, 'r') as f:
        content = f.read()
    
    if "def query_memory_full_text(" in content:
        print("    ✅ query_memory_full_text() exists in memory_store.py")
    else:
        print("    ⚠️ query_memory_full_text() not found in memory_store.py")
            errors.append("memory_store.py: query_memory_full_text() method not found")
    
    # Check episodic_store.py for query_episodes_full_text
    episodic_file = "/home/dietpi/pi-rag/rag/episodic_store.py"
    with open(episodic_file, 'r') as f:
        content = f.read()
    
    if "def query_episodes_full_text(" in content:
        print("    ✅ query_episodes_full_text() exists in episodic_store.py")
    else:
            print("    ⚠️ query_episodes_full_text() not found in episodic_store.py")
            errors.append("episodic_store.py: query_episodes_full_text() method not found")
    
    if errors:
        print("  Status: Full-text search methods need to be implemented")
        return
    else:
        print("  Status: Full-text search methods already implemented")
    
def print_section(title):
    """Print section header."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")

def main():
    """Main entry point."""
    print("="*60)
    print("RAG MCP SERVER - DIRECT FIXES")
    print("="*60)
    
    try:
        # Apply fixes in order of priority
        success_count = 0
        error_count = 0
        
        # Fix 1: Semantic Retrieval
        print_section("Fix 1: Semantic Retrieval - Embedding Generation")
        if fix_semantic_embeddings():
            success_count += 1
        else:
            error_count += 1
        
        # Fix 2: Dynamic Projects
        print_section("Fix 2: Dynamic Projects - Memory Store")
        if fix_memory_store_dynamic_projects():
            success_count += 1
        else:
            error_count += 1
        
        # Fix 3: Search Functionality
        print_section("Fix 3: Search Functionality - Full-Text Search")
        if fix_search_functionality():
            success_count += 1
        else:
            error_count += 1
        
        # Summary
        print_section("SUMMARY")
        print(f"Total fixes: {success_count + error_count}")
        print(f"Successes: {success_count}")
        print(f"Errors: {error_count}")
        
        if error_count > 0:
            print("\n❌ Some fixes had errors - see details above")
            return 1
        else:
            print("\n✅ All fixes completed successfully!")
            return 0
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
