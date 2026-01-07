"""
Test utility functions for SYNAPSE tests.

Provides helper functions for creating test data, assertions, mocks, etc.
"""

import json
import uuid
from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime


def create_test_fact(
    scope: str = "session",
    category: str = "fact",
    key: str = "test_key",
    value: Any = "test_value",
    confidence: float = 1.0,
    source: str = "agent"
) -> Dict[str, Any]:
    """
    Create a test fact dictionary.

    Args:
        scope: Memory scope (user|project|org|session)
        category: Fact category (preference|constraint|decision|fact)
        key: Unique key within scope
        value: Fact value
        confidence: Confidence level (0.0-1.0)
        source: Source of fact (user|agent|tool)

    Returns:
        Fact dictionary
    """
    return {
        "id": str(uuid.uuid4()),
        "scope": scope,
        "category": category,
        "key": key,
        "value": value,
        "confidence": confidence,
        "source": source,
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }


def create_test_episode(
    situation: str = "Test situation",
    action: str = "Test action",
    outcome: str = "success",
    lesson: str = "Test lesson",
    confidence: float = 0.9,
    lesson_type: str = "pattern",
    quality: float = 0.9
) -> Dict[str, Any]:
    """
    Create a test episode dictionary.

    Args:
        situation: What the agent faced
        action: What the agent did
        outcome: Result of action (success/failure)
        lesson: Abstracted strategy
        confidence: Confidence level (0.0-1.0)
        lesson_type: Type of lesson (success|pattern|mistake|failure)
        quality: Quality score (0.0-1.0)

    Returns:
        Episode dictionary
    """
    return {
        "id": str(uuid.uuid4()),
        "situation": situation,
        "action": action,
        "outcome": outcome,
        "lesson": lesson,
        "confidence": confidence,
        "created_at": datetime.utcnow().isoformat(),
        "lesson_type": lesson_type,
        "quality": quality,
    }


def create_test_document(
    content: str = "Test document content.",
    metadata: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Create a test document dictionary.

    Args:
        content: Document content
        metadata: Optional document metadata

    Returns:
        Document dictionary
    """
    return {
        "id": str(uuid.uuid4()),
        "content": content,
        "metadata": metadata or {},
        "created_at": datetime.utcnow().isoformat(),
    }


def create_test_chunk(
    content: str = "Test chunk content.",
    document_id: Optional[str] = None,
    chunk_index: int = 0
) -> Dict[str, Any]:
    """
    Create a test chunk dictionary.

    Args:
        content: Chunk content
        document_id: Parent document ID
        chunk_index: Index of chunk in document

    Returns:
        Chunk dictionary
    """
    return {
        "id": str(uuid.uuid4()),
        "content": content,
        "document_id": document_id or str(uuid.uuid4()),
        "chunk_index": chunk_index,
        "metadata": {},
    }


def assert_dict_subset(subset: Dict[str, Any], superset: Dict[str, Any], msg: str = ""):
    """
    Assert that all key-value pairs in subset exist in superset.

    Args:
        subset: Dictionary of expected key-value pairs
        superset: Dictionary to check
        msg: Optional error message

    Raises:
        AssertionError if subset not contained in superset
    """
    for key, value in subset.items():
        if key not in superset:
            raise AssertionError(f"Key '{key}' not in superset. {msg}")
        if superset[key] != value:
            raise AssertionError(
                f"Value mismatch for key '{key}': "
                f"expected {value}, got {superset[key]}. {msg}"
            )


def assert_lists_equal_unordered(list1: List[Any], list2: List[Any], msg: str = ""):
    """
    Assert that two lists contain the same elements, regardless of order.

    Args:
        list1: First list
        list2: Second list
        msg: Optional error message

    Raises:
        AssertionError if lists differ
    """
    if len(list1) != len(list2):
        raise AssertionError(
            f"Lists have different lengths: {len(list1)} vs {len(list2)}. {msg}"
        )

    for item in list1:
        if item not in list2:
            raise AssertionError(f"Item {item} not in second list. {msg}")


def assert_between(
    value: float,
    min_val: float,
    max_val: float,
    msg: str = ""
):
    """
    Assert that a value is between min and max (inclusive).

    Args:
        value: Value to check
        min_val: Minimum value
        max_val: Maximum value
        msg: Optional error message

    Raises:
        AssertionError if value not in range
    """
    if not (min_val <= value <= max_val):
        raise AssertionError(
            f"Value {value} not in range [{min_val}, {max_val}]. {msg}"
        )


def normalize_string(s: str) -> str:
    """
    Normalize a string for comparison.

    Removes extra whitespace and normalizes line endings.

    Args:
        s: String to normalize

    Returns:
        Normalized string
    """
    return " ".join(s.split()).strip()


def save_test_config(path: str, config: Dict[str, Any]):
    """
    Save a test configuration to a JSON file.

    Args:
        path: Path to save config file
        config: Configuration dictionary
    """
    with open(path, 'w') as f:
        json.dump(config, f, indent=2)


def load_test_config(path: str) -> Dict[str, Any]:
    """
    Load a test configuration from a JSON file.

    Args:
        path: Path to config file

    Returns:
        Configuration dictionary
    """
    with open(path, 'r') as f:
        return json.load(f)


# ============================================================================
# Assertion Helpers
# ============================================================================

def assert_valid_uuid(uuid_str: str, msg: str = ""):
    """
    Assert that a string is a valid UUID.

    Args:
        uuid_str: UUID string to validate
        msg: Optional error message

    Raises:
        AssertionError if invalid UUID
    """
    try:
        uuid.UUID(uuid_str)
    except ValueError:
        raise AssertionError(f"Invalid UUID: {uuid_str}. {msg}")


def assert_valid_embedding(embedding: List[float], msg: str = ""):
    """
    Assert that a vector is a valid embedding.

    Args:
        embedding: Embedding vector to validate
        msg: Optional error message

    Raises:
        AssertionError if invalid embedding
    """
    assert isinstance(embedding, list), f"Embedding must be a list. {msg}"
    assert len(embedding) > 0, f"Embedding must not be empty. {msg}"
    assert all(isinstance(x, (int, float)) for x in embedding), \
        f"Embedding must contain numbers. {msg}"
    assert all(0.0 <= x <= 1.0 for x in embedding), \
        f"Embedding values must be normalized [0, 1]. {msg}"


def assert_valid_fact(fact: Dict[str, Any], msg: str = ""):
    """
    Assert that a dictionary is a valid fact structure.

    Args:
        fact: Fact dictionary to validate
        msg: Optional error message

    Raises:
        AssertionError if invalid fact
    """
    required_keys = ["id", "scope", "category", "key", "value", "confidence", "source"]
    for key in required_keys:
        assert key in fact, f"Missing required key '{key}' in fact. {msg}"
    assert_valid_uuid(fact["id"], msg)


def assert_valid_episode(episode: Dict[str, Any], msg: str = ""):
    """
    Assert that a dictionary is a valid episode structure.

    Args:
        episode: Episode dictionary to validate
        msg: Optional error message

    Raises:
        AssertionError if invalid episode
    """
    required_keys = ["id", "situation", "action", "outcome", "lesson", "confidence", "lesson_type", "quality"]
    for key in required_keys:
        assert key in episode, f"Missing required key '{key}' in episode. {msg}"
    assert_valid_uuid(episode["id"], msg)


def assert_valid_chunk(chunk: Dict[str, Any], msg: str = ""):
    """
    Assert that a dictionary is a valid chunk structure.

    Args:
        chunk: Chunk dictionary to validate
        msg: Optional error message

    Raises:
        AssertionError if invalid chunk
    """
    required_keys = ["id", "content"]
    for key in required_keys:
        assert key in chunk, f"Missing required key '{key}' in chunk. {msg}"
    assert "content" in chunk and len(chunk["content"]) > 0, \
        f"Chunk content must not be empty. {msg}"


# ============================================================================
# Mock Factories
# ============================================================================

class MockEmbeddingService:
    """Mock embedding service for fast tests."""

    def __init__(self, embedding_dim: int = 768):
        """
        Initialize mock embedding service.

        Args:
            embedding_dim: Dimension of embeddings (default: 768)
        """
        self.embedding_dim = embedding_dim
        self.embed_count = 0

    def embed(self, texts: List[str]) -> List[List[float]]:
        """
        Generate mock embeddings.

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        self.embed_count += len(texts)
        return [[0.1] * self.embedding_dim for _ in texts]

    def embed_single(self, text: str) -> List[float]:
        """
        Generate mock embedding for single text.

        Args:
            text: Text string

        Returns:
            Embedding vector
        """
        self.embed_count += 1
        return [0.1] * self.embedding_dim


class MockLLMService:
    """Mock LLM service for fast tests."""

    def __init__(self):
        """Initialize mock LLM service."""
        self.generate_count = 0

    def generate(self, prompt: str) -> str:
        """
        Generate mock response.

        Args:
            prompt: Input prompt

        Returns:
            Mock response string
        """
        self.generate_count += 1
        return f"Mock response to: {prompt[:50]}..."


class MockHTTPClient:
    """Mock HTTP client for MCP server tests."""

    def __init__(self, mock_responses: Optional[Dict[str, Any]] = None):
        """
        Initialize mock HTTP client.

        Args:
            mock_responses: Optional dictionary of mock responses
        """
        self.mock_responses = mock_responses or {}

    def get(self, url: str, **kwargs):
        """Mock GET request."""
        return MockResponse(status_code=200, json_data=self.mock_responses.get(url, {}))

    def post(self, url: str, **kwargs):
        """Mock POST request."""
        return MockResponse(status_code=200, json_data=self.mock_responses.get(url, {}))


class MockResponse:
    """Mock HTTP response."""

    def __init__(self, status_code: int = 200, json_data: Any = None):
        """
        Initialize mock response.

        Args:
            status_code: HTTP status code (default: 200)
            json_data: JSON response data
        """
        self.status_code = status_code
        self.json_data = json_data

    def json(self):
        """Return JSON data."""
        return self.json_data


class MockDatabase:
    """Mock database for fast tests."""

    def __init__(self):
        """Initialize mock database."""
        self.data = {}

    def execute(self, query: str, params: Optional[Dict] = None):
        """Mock SQL execute."""
        return []

    def cursor(self):
        """Return mock cursor."""
        return MockCursor()


class MockCursor:
    """Mock database cursor."""

    def __init__(self):
        """Initialize mock cursor."""
        self.results = []

    def execute(self, query: str, params: Optional[Dict] = None):
        """Mock execute."""
        pass

    def fetchall(self):
        """Mock fetchall."""
        return []

    def fetchone(self):
        """Mock fetchone."""
        return None

    def close(self):
        """Mock close."""
        pass
