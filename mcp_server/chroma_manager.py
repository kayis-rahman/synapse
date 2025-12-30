"""
ChromaDB Manager - Per-project ChromaDB isolation (Option A).

Each project gets its own ChromaDB instance for complete isolation.
"""
import os
from typing import Dict
import chromadb
import logging

logger = logging.getLogger(__name__)


class ProjectChromaManager:
    """
    Manages ChromaDB instances for multi-client isolation.

    Features:
    - One ChromaDB client per project
    - Client caching to avoid repeated initialization
    - Complete isolation between projects
    """

    def __init__(self, base_data_dir: str = "/opt/pi-rag/data"):
        """
        Initialize ChromaDB manager.

        Args:
            base_data_dir: Base data directory
        """
        self.base_data_dir = base_data_dir
        self._clients: Dict[str, chromadb.PersistentClient] = {}
        logger.info("ProjectChromaManager initialized")

    def get_chroma_client(
        self,
        project_id: str,
        create_if_missing: bool = True
    ) -> chromadb.PersistentClient:
        """
        Get or create ChromaDB client for specific project.

        Args:
            project_id: Project identifier
            create_if_missing: Create ChromaDB directory if doesn't exist

        Returns:
            ChromaDB client instance
        """
        if project_id in self._clients:
            return self._clients[project_id]

        # Build ChromaDB path for project
        chroma_path = os.path.join(
            self.base_data_dir,
            project_id,
            "chroma_semantic"
        )

        # Create directory if needed
        if create_if_missing:
            os.makedirs(chroma_path, exist_ok=True)

        # Create ChromaDB client
        client = chromadb.PersistentClient(path=chroma_path)

        # Cache client
        self._clients[project_id] = client

        logger.debug(f"Created ChromaDB client for project {project_id}: {chroma_path}")

        return client

    def get_collection(
        self,
        project_id: str,
        collection_name: str = "semantic_chunks"
    ):
        """
        Get or create collection for project.

        Args:
            project_id: Project identifier
            collection_name: Name of collection

        Returns:
            ChromaDB collection
        """
        client = self.get_chroma_client(project_id)

        return client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def remove_client(self, project_id: str) -> None:
        """
        Remove client from cache (for cleanup).

        Args:
            project_id: Project identifier
        """
        if project_id in self._clients:
            del self._clients[project_id]
            logger.debug(f"Removed ChromaDB client for project {project_id}")
