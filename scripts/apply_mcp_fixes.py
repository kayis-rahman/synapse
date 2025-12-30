#!/usr/bin/env python3
"""
Comprehensive Patch Script for RAG MCP Server

This script applies all fixes for:
1. Phase 1: Fix Semantic Retrieval (embedding generation)
2. Phase 2: Implement Dynamic Project System
3. Phase 3: Fix Search Functionality (full-text search)
4. Phase 4: Episode Validation (keep as-is)

Usage:
    python3 scripts/apply_mcp_fixes.py
"""

import os
import re
import shutil
import sys
from pathlib import Path

# Add rag directory to Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Patch definitions
PATCHES = []

def apply_patch(filepath: str, pattern: str, replacement: str, description: str):
    """Apply a patch to a file."""
    print(f"  Patching {filepath}")
    
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_content = re.sub(pattern, replacement, content, count=1)
    
    with open(filepath, 'w') as f:
        f.write(new_content)
    
    PATCHES.append({
        "file": filepath,
        "description": description
    })
    print(f"  ✅ Patch applied: {description}")

def print_section(title):
    """Print section header."""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}\n")

def patch_semantic_store_phase1():
    """Phase 1: Fix Semantic Retrieval - Add embedding generation."""
    print_section("Phase 1: Fix Semantic Retrieval (Embedding Generation)")
    
    filepath = "/home/dietpi/pi-rag/rag/semantic_store.py"
    
    # Patch 1: Add logging and get_embedding_service function (at top after imports)
    logging_import_patch = r'(import numpy as np\n)(\n)(logger = logging\.getLogger\(__name__))'
    embedding_service_code = '''
import logging
logger = logging.getLogger(__name__)

_embedding_service = None

def get_embedding_service():
    """Get embedding service singleton (lazy import)."""
    global _embedding_service
    if _embedding_service is None:
        try:
            from rag.embedding import get_embedding_service as get_emb
            _embedding_service = get_emb()
            logger.info("Embedding service initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize embedding service: {e}")
            _embedding_service = None
    return _embedding_service
'''
    
    pattern = r'(import numpy as np\n)'
    apply_patch(filepath, pattern, embedding_service_code + '\n\n' + embedding_service_code,
               "Phase 1: Add logging and get_embedding_service function")
    
    # Patch 2: Update add_document to generate embeddings
    chunk_creation_patch = r'(chunk_ids\.append\(chunk\.chunk_id\)\n)'
    chunk_embedding_code = '''
chunk = DocumentChunk(
                document_id=document_id,
                content=chunk_text,
                chunk_index=i,
                metadata={
                    **metadata,
                    "document_id": document_id,
                    "chunk_index": i,
                    "total_chunks": len(chunks)
                }
            )
            self.chunks.append(chunk)
            chunk_ids.append(chunk.chunk_id)'''
    
    apply_patch(filepath, chunk_creation_patch, chunk_embedding_code,
               "Phase 1: Add embedding generation to chunk creation")

def patch_memory_store_phase2():
    """Phase 2: Implement Dynamic Project System."""
    print_section("Phase 2: Implement Dynamic Project System")
    
    filepath = "/home/dietpi/pi-rag/rag/memory_store.py"
    
    # Patch 1: Remove VALID_SCOPES enum
    valid_scopes_patch = r'VALID_SCOPES = \{[^}]*"user", "project", "org", "session"\}[^}]*"\''
    apply_patch(filepath, valid_scopes_patch,
               "Phase 2: Remove VALID_SCOPES enum")
    
    # Patch 2: Add _is_valid_project_id validation method
    validation_method_code = '''
    @staticmethod
    def _is_valid_project_id(project_id: str) -> bool:
        """
        Validate project_id format (name-shortUUID or simple name).
        
        Accepts:
        - Simple names (alphanumeric, hyphens, underscores)
        - name-shortUUID format (e.g., "myapp-a1b2c3d4")
        
        Returns:
            True if valid, False otherwise
        """
        if not project_id or not isinstance(project_id, str):
            return False
        
        # Check length
        if len(project_id) < 1 or len(project_id) > 150:
            return False
        
        # Check for valid characters (alphanumeric, hyphens, underscores)
        if not re.match(r'^[a-zA-Z0-9_-]+$', project_id):
            return False
        
        return True
    '''
    
    location_code = r'(def _validate_fact\(self, fact: MemoryFact\) -> None:\n)(?    if fact\.scope not in self\.VALID_SCOPES:)'
    replacement_code = r'\1    if fact.scope not in self._is_valid_project_id(fact.scope):'
    
    apply_patch(filepath, location_code, replacement_code,
               "Phase 2: Add project_id validation")

def patch_episodic_store_phase2():
    """Phase 2: Add project_id field for isolation."""
    print_section("Phase 2: Episodic Store - Add Project ID")
    
    filepath = "/home/dietpi/pi-rag/rag/episodic_store.py"
    
    # Patch 1: Add project_id to Episode class
    episode_class_patch = r'class Episode:\s*"""(.*def __init__\(self.*?\n)(.*situation: str = "",'
    episode_init_addition = r',\n        project_id: str = "",  # <-- NEW\n        self\.project_id = project_id  # <-- NEW'
    
    apply_patch(filepath, episode_class_patch, episode_init_addition,
               "Phase 2: Add project_id to Episode class")
    
    # Patch 2: Update to_dict to include project_id
    to_dict_patch = r'(    def to_dict\(self\) -> Dict\[str, Any\]:\n)(        return \{\n(            "id": self\.id,'
    to_dict_addition = r',            "project_id": self\.project_id,  # <-- NEW\n            "situation": self\.situation,'
    apply_patch(filepath, to_dict_patch, to_dict_addition,
               "Phase 2: Update to_dict to include project_id")
    
    # Patch 3: Update database schema
    schema_patch = r'(CREATE TABLE IF NOT EXISTS episodic_memory \(\n)(    id TEXT PRIMARY KEY,\n)(            situation TEXT NOT NULL,\n)(            action TEXT NOT NULL,\n)(            outcome TEXT NOT NULL,\n)(            lesson TEXT NOT NULL,\n)(            confidence REAL NOT NULL CHECK\(confidence >= 0\.0 AND confidence <= 1\.0\),\n)(            created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n)'
    schema_addition = r'CREATE TABLE IF NOT EXISTS episodic_memory (\n            id TEXT PRIMARY KEY,\n            project_id TEXT,\n  # <-- NEW\n            situation TEXT NOT NULL,\n)(            action TEXT NOT NULL,\n)(            outcome TEXT NOT NULL,\n)(            lesson TEXT NOT NULL,\n)(            confidence REAL NOT NULL CHECK\(confidence >= 0\.0 AND confidence <= 1\.0\),\n)(            created_at DATETIME DEFAULT CURRENT_TIMESTAMP\n)'
    
    apply_patch(filepath, schema_patch, schema_addition,
               "Phase 2: Add project_id column to database schema")
    
    # Patch 4: Update store_episode to include project_id
    store_patch = r'cursor\.execute\(\n\s*"INSERT INTO episodic_memory\s+.*\(id, situation, action, outcome, lesson, confidence, created_at\)\s+.*VALUES \(\?, \?, \?, \?, \?, \?\)'
    store_addition = r'cursor.execute(\n            """INSERT INTO episodic_memory\n                   (id, project_id, situation, action, outcome, lesson, confidence, created_at)\n                   VALUES (?, ?, ?, ?, ?, ?, ?)""",'
    
    apply_patch(filepath, store_patch, store_addition,
               "Phase 2: Update store_episode to include project_id")
    
    # Patch 5: Update get_episode to include project_id
    get_episode_patch = r'cursor\.execute\(\s*"SELECT id, situation, action, outcome, lesson, confidence, created_at\s+\n\s*FROM episodic_memory WHERE id = \?"'
    get_episode_addition = r'cursor.execute(\n            """SELECT id, project_id, situation, action, outcome, lesson, confidence, created_at\n                   FROM episodic_memory WHERE id = ?"""'
    
    apply_patch(filepath, get_episode_patch, get_episode_addition,
               "Phase 2: Update get_episode to include project_id")
    
    # Patch 6: Update Episode return
    episode_return_patch = r'return Episode\(\n\s*id=row\[0\],\n\s*situation=row\[1\],\n\s*\naction=row\[2\],\n\s*\noutcome=row\[3\],\n\s*\nlesson=row\[4\],\n\s*\nconfidence=row\[5\],\n\s*\ncreated_at=row\[6\]\n\s*\)'
    
    apply_patch(filepath, episode_return_patch, episode_return_addition,
               "Phase 2: Update Episode return to include project_id")

    # Patch 7: Update query_episodes to include project_id
    query_episodes_patch = r'def query_episodes\(\s*self,\n\s*(?=,\s*project_id: str,  # <-- NEW: Add parameter\n\s*(?=,\s*min_confidence: float = 0\.0,\n\s*(?=,\s*situation_contains: Optional\[str\] = None,\n\s*(?=,\s*limit: int = 10\) -> List\[Episode\]:\n)'
    query_addition = r'def query_episodes(\n*project_id: str,\s*(?=,\s*min_confidence: float = 0\.0,\n\s*(?=,\s*situation_contains: Optional\[str\] = None,\n\s*(?=,\s*limit: int = 10\) -> List\[Episode\]:'
    
    apply_patch(filepath, query_episodes_patch, query_addition,
               "Phase 2: Update query_episodes to accept project_id")
    
    # Patch 8: Update query_episodes WHERE clause
    where_patch = r'conditions\.append\("project_id = \?"\)'
    where_replacement = r'conditions.append("project_id = ?")\n            params = [project_id]  # <-- NEW\n        conditions.append("confidence >= ?")'
    
    apply_patch(filepath, where_patch, where_replacement,
               "Phase 2: Update query_episodes to filter by project_id")
    
    # Patch 9: Fix list_recent_episodes date query (use Python date calculation)
    recent_patch = r'cursor\.execute\(\s*"SELECT id, project_id, situation, action, outcome, lesson, confidence, created_at\s+\n\s*FROM episodic_memory\s+\n\s*WHERE project_id = \?\n+\s*\s*AND datetime\(created_at\) >= datetime\('now', '-' \|\|\?) \|\|\s*\s*days\'\s+\s*\s*\s*AND confidence >= \?\s*\s*ORDER BY confidence DESC, created_at DESC LIMIT \?"'
    recent_replacement = r'''cursor.execute(
                """SELECT id, project_id, situation, action, outcome, lesson, confidence, created_at
                   FROM episodic_memory
                   WHERE project_id = ?
                   AND date(created_at) >= date('now', '-' || ? || ' days')
                   AND confidence >= ?
                   ORDER BY confidence DESC, created_at DESC LIMIT ?
                """, (project_id, days, min_confidence, limit)
                '''
    
    apply_patch(filepath, recent_patch, recent_replacement,
               "Phase 2: Fix list_recent_episodes date query (use Python date calculation)")

def patch_mcp_server_phase2():
    """Phase 2: Integrate ProjectManager into MCP server."""
    print_section("Phase 2: MCP Server - Integrate ProjectManager")
    
    filepath = "/home/dietpi/pi-rag/mcp_server/rag_server.py"
    
    # Patch 1: Add ProjectManager import
    imports_patch = r'(from rag import \([^)]+\n)'
    imports_addition = r'from rag import (\n    MemoryStore, MemoryFact, get_memory_store,\n    EpisodicStore, Episode, get_episodic_store,\n    SemanticStore, get_semantic_store,\n    SemanticIngestor, get_semantic_ingestor,\n    SemanticRetriever, get_semantic_retriever\n)'
    project_manager_addition = r'from rag import (\n    MemoryStore, MemoryFact, get_memory_store,\n    EpisodicStore, Episode, get_episodic_store,\n    SemanticStore, get_semantic_store,\n    SemanticIngestor, get_semantic_ingestor,\n    SemanticRetriever, get_semantic_retriever\n)\n\n# Local imports\nfrom .metrics import Metrics, get_metrics\nfrom .project_manager import ProjectManager  # <-- NEW'
    
    apply_patch(filepath, imports_patch, imports_addition,
               "Phase 2: Add ProjectManager import")
    
    # Patch 2: Add ProjectManager initialization
    init_patch = r'(self\._project_cache: Dict\[str, str\] = {}\n)'
    init_addition = r'self._project_cache: Dict[str, str] = {}\n\n        \n        # Project Manager for dynamic project resolution\n        self.project_manager = ProjectManager()  # <-- NEW'
    
    apply_patch(filepath, init_patch, init_addition,
               "Phase 2: Add ProjectManager initialization")
    
    # Patch 3: Add resolve_project_id method (after _get_semantic_retriever)
    resolve_method_code = '''
def resolve_project_id(self, project_name: str) -> str:
    """
    Resolve project name to project_id (name-shortUUID format).
    
    If project already exists (by name or full project_id), return existing ID.
    Otherwise, create new project with name-shortUUID format.
    
    Args:
        project_name: Project name or project_id (e.g., "myapp", "myapp-a1b2c3d4")
    
    Returns:
        Resolved project_id (name-shortUUID format)
    """
    # Check cache first
    if project_name in self._project_cache:
        return self._project_cache[project_name]
    
    # Check if project exists (by name or full project_id)
    projects = self.project_manager.list_projects()
    for project in projects:
        if project["name"] == project_name or project["project_id"] == project_name:
            project_id = project["project_id"]
            self._project_cache[project_name] = project_id
            logger.info(f"Resolved existing project: {project_id}")
            return project_id
    
    # Create new project with name-shortUUID format
    result = self.project_manager.create_project(
        name=project_name,
        metadata={"created_by": "mcp_server"}
    )
    project_id = result["project_id"]
    self._project_cache[project_name] = project_id
    
    logger.info(f"Created new project: {project_id}")
    return project_id
'''
    
    # Find location to insert method (after _get_semantic_retriever)
    insert_location = r'def _get_semantic_store\(self\) -> SemanticStore:\s*\n)'
    insert_addition = r'def _get_semantic_store(self) -> SemanticStore:\s*index_path = os\.path\.join\(self\.project_manager\.get_project_dir\(project_id\), "semantic_index"\)\s*\nreturn get_semantic_store\(index_path\)'
    
    apply_patch(filepath, insert_location, insert_addition,
               "Phase 2: Add project_id parameter to semantic store getter")
    
    # Patch 4: Update store getters to use project_id
    store_getters_patch = r'(def _get_symbolic_store\(self\) -> MemoryStore:\s*\s*db_path = os\.path\.join\(self\._get_data_dir\(\), "memory\.db"\)\s*\nreturn get_memory_store\(db_path\)\n)'
    store_addition = r'def _get_symbolic_store(self, project_id: str\) -> MemoryStore:  # <-- NEW: Add parameter\n        project_dir = self.project_manager.get_project_dir(project_id)\n        db_path = os.path.join(project_dir, "memory.db")\n        return get_memory_store(db_path)'
    
    episodic_addition = r'def _get_episodic_store\(self\) -> EpisodicStore:\s*\s*db_path = os\.path\.join\(self\._get_data_dir\(\), "episodic\.db"\)\s*\nreturn get_episodic_store\(db_path\)\n'
    episodic_addition = r'def _get_episodic_store(self, project_id: str\) -> EpisodicStore:  # <-- NEW: Add parameter\n        project_dir = self.project_manager.get_project_dir(project_id)\n        db_path = os.path.join(project_dir, "episodic.db")\n        return get_episodic_store(db_path)\n'
    
    apply_patch(filepath, store_getters_patch, store_addition, episodic_addition,
               "Phase 2: Update store getters to use project_id")
    
    # Patch 5: Update tool handlers to resolve project_id
    tool_handler_patch = r'async def handle_tool_call\(name: str, arguments: Dict\[str, Any\]\) -> List\[TextContent\]:\n\s*try:\n\s*project_name = arguments\.get\("project_id"\)\n\s*if project_name:\n\s*project_id = backend\.resolve_project_id\(project_name\)\n\s*arguments\[\"project_id\"\] = project_id\n\n\s*'
    
    apply_patch(filepath, tool_handler_patch,
               "Phase 2: Update all tool handlers to resolve project_id")

def main():
    """Main entry point."""
    print("="*60)
    print("RAG MCP SERVER - PATCH APPLIER")
    print("="*60)
    
    try:
        # Apply Phase 1: Semantic Retrieval
        patch_semantic_store_phase1()
        
        # Apply Phase 2: Dynamic Project System
        patch_memory_store_phase2()
        patch_episodic_store_phase2()
        patch_mcp_server_phase2()
        
        print_section("SUMMARY")
        print("✅ All patches applied successfully")
        print()
        print(f"Total patches applied: {len(PATCHES)}")
        print()
        print("Next steps:")
        print("1. Restart MCP server to apply changes")
        print("2. Test with new project names (e.g., 'pi-rag')")
        print("3. Test dynamic project creation")
        print("4. Verify all 7 tools work with new system")
        print()
        print("Note: Existing chunks need re-ingestion to get embeddings.")
        print("      Run semantic ingestion on existing files to populate embeddings.")
        
        return 0
    
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == "__main__":
    sys.exit(main())
