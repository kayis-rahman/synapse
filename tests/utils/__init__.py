"""
Test utilities package.

Contains helper functions, assertions, mocks, and generators for test writing.
"""

# Data generators and helpers
from .helpers import (
    create_test_fact,
    create_test_episode,
    create_test_document,
    create_test_chunk,
    assert_dict_subset,
    assert_lists_equal_unordered,
    assert_between,
    normalize_string,
    save_test_config,
    load_test_config,
    # Assertion helpers
    assert_valid_uuid,
    assert_valid_embedding,
    assert_valid_fact,
    assert_valid_episode,
    assert_valid_chunk,
    # Mock factories
    MockEmbeddingService,
    MockLLMService,
    MockHTTPClient,
    MockDatabase,
    MockResponse,
    MockCursor,
)

__all__ = [
    # Data generators and helpers
    "create_test_fact",
    "create_test_episode",
    "create_test_document",
    "create_test_chunk",
    "assert_dict_subset",
    "assert_lists_equal_unordered",
    "assert_between",
    "normalize_string",
    "save_test_config",
    "load_test_config",
    # Assertion helpers
    "assert_valid_uuid",
    "assert_valid_embedding",
    "assert_valid_fact",
    "assert_valid_episode",
    "assert_valid_chunk",
    # Mock factories
    "MockEmbeddingService",
    "MockLLMService",
    "MockHTTPClient",
    "MockDatabase",
    "MockResponse",
    "MockCursor",
]
