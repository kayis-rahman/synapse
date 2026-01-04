"""
Test utility functions for SYNAPSE tests.

Provides helper functions for creating test data, assertions, etc.
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
