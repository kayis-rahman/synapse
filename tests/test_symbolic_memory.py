"""
Comprehensive tests for the Symbolic Memory subsystem.

Tests cover:
- MemoryStore CRUD operations
- MemoryWriter extraction and validation
- MemoryReader querying and injection
- Integration tests
- Edge cases and error handling
"""

import os
import json
import tempfile
from pathlib import Path

import pytest

from rag.memory_store import MemoryStore, MemoryFact, get_memory_store
from rag.memory_writer import MemoryWriter, extract_and_store
from rag.memory_reader import MemoryReader, get_memory_reader, inject_memory_context


# ============================================================================
# Fixtures
# ============================================================================

@pytest.fixture
def temp_db():
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = f.name
    yield db_path
    # Cleanup
    if os.path.exists(db_path):
        os.remove(db_path)


@pytest.fixture
def memory_store(temp_db):
    """Create a MemoryStore instance with temp database."""
    store = MemoryStore(temp_db)
    yield store
    store.close()


@pytest.fixture
def memory_reader(temp_db):
    """Create a MemoryReader instance with temp database."""
    return MemoryReader(temp_db)


@pytest.fixture
def memory_writer():
    """Create a MemoryWriter instance."""
    return MemoryWriter()


@pytest.fixture
def sample_facts():
    """Sample memory facts for testing."""
    return [
        MemoryFact(
            scope="user",
            category="preference",
            key="output_format",
            value="json",
            confidence=0.9,
            source="user"
        ),
        MemoryFact(
            scope="user",
            category="preference",
            key="language",
            value="English",
            confidence=0.95,
            source="user"
        ),
        MemoryFact(
            scope="project",
            category="decision",
            key="programming_language",
            value="Python",
            confidence=0.95,
            source="user"
        ),
        MemoryFact(
            scope="project",
            category="constraint",
            key="max_response_length",
            value=1000,
            confidence=0.8,
            source="user"
        ),
        MemoryFact(
            scope="session",
            category="fact",
            key="topic",
            value="machine_learning",
            confidence=0.7,
            source="agent"
        )
    ]


# ============================================================================
# MemoryStore Tests
# ============================================================================

class TestMemoryStore:
    """Test MemoryStore CRUD operations."""

    def test_init_database(self, temp_db):
        """Test database initialization."""
        store = MemoryStore(temp_db)
        assert os.path.exists(temp_db)

        # Check tables exist
        with store._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='memory_facts'"
            )
            assert cursor.fetchone() is not None

    def test_store_memory(self, memory_store):
        """Test storing a memory fact."""
        fact = MemoryFact(
            scope="user",
            category="preference",
            key="test_key",
            value="test_value",
            confidence=0.9,
            source="user"
        )

        stored = memory_store.store_memory(fact)
        assert stored is not None
        assert stored.key == "test_key"
        assert stored.scope == "user"
        assert stored.confidence == 0.9

    def test_store_memory_with_existing_key_higher_confidence(self, memory_store):
        """Test updating fact when new confidence is higher."""
        # Store initial fact
        fact1 = MemoryFact(
            scope="user",
            category="preference",
            key="output_format",
            value="json",
            confidence=0.7,
            source="user"
        )
        memory_store.store_memory(fact1)

        # Store updated fact with higher confidence
        fact2 = MemoryFact(
            scope="user",
            category="preference",
            key="output_format",
            value="markdown",
            confidence=0.9,
            source="user"
        )
        stored = memory_store.store_memory(fact2)

        # Should be updated
        assert stored.value == json.dumps("markdown")
        assert stored.confidence == 0.9

    def test_store_memory_with_existing_key_lower_confidence(self, memory_store):
        """Test not updating fact when new confidence is lower."""
        # Store initial fact with high confidence
        fact1 = MemoryFact(
            scope="user",
            category="preference",
            key="output_format",
            value="json",
            confidence=0.9,
            source="user"
        )
        stored1 = memory_store.store_memory(fact1)

        # Try to update with lower confidence
        fact2 = MemoryFact(
            scope="user",
            category="preference",
            key="output_format",
            value="markdown",
            confidence=0.5,
            source="user"
        )
        stored2 = memory_store.store_memory(fact2)

        # Should not be updated
        assert stored2.value == json.dumps("json")
        assert stored2.confidence == 0.9

    def test_update_memory(self, memory_store):
        """Test updating an existing memory fact."""
        # Store initial fact
        fact1 = MemoryFact(
            scope="user",
            category="preference",
            key="test_key",
            value="initial_value",
            confidence=0.8,
            source="user"
        )
        stored1 = memory_store.store_memory(fact1)

        # Update the fact
        fact2 = MemoryFact(
            id=stored1.id,
            scope="user",
            category="preference",
            key="test_key",
            value="updated_value",
            confidence=0.9,
            source="user"
        )
        stored2 = memory_store.update_memory(fact2)

        assert stored2.id == stored1.id
        assert stored2.value == json.dumps("updated_value")
        assert stored2.confidence == 0.9

    def test_query_memory_by_scope(self, memory_store, sample_facts):
        """Test querying memory by scope."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        # Query user scope
        user_facts = memory_store.query_memory(scope="user")
        assert len(user_facts) == 2
        assert all(f.scope == "user" for f in user_facts)

        # Query project scope
        project_facts = memory_store.query_memory(scope="project")
        assert len(project_facts) == 2
        assert all(f.scope == "project" for f in project_facts)

    def test_query_memory_by_category(self, memory_store, sample_facts):
        """Test querying memory by category."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        # Query preferences
        preferences = memory_store.query_memory(category="preference")
        assert len(preferences) == 2
        assert all(f.category == "preference" for f in preferences)

    def test_query_memory_by_key(self, memory_store):
        """Test querying memory by key."""
        fact = MemoryFact(
            scope="user",
            category="preference",
            key="output_format",
            value="json",
            confidence=0.9,
            source="user"
        )
        memory_store.store_memory(fact)

        # Query by exact key
        results = memory_store.query_memory(key="output_format")
        assert len(results) == 1
        assert results[0].key == "output_format"

    def test_query_memory_with_min_confidence(self, memory_store, sample_facts):
        """Test querying memory with minimum confidence."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        # Query with min_confidence
        high_conf = memory_store.query_memory(min_confidence=0.85)
        assert len(high_conf) == 3  # Only facts with confidence >= 0.85

    def test_list_memory(self, memory_store, sample_facts):
        """Test listing all facts for a scope."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        # List user scope
        user_facts = memory_store.list_memory("user")
        assert len(user_facts) == 2

    def test_delete_memory(self, memory_store):
        """Test deleting a memory fact."""
        fact = MemoryFact(
            scope="user",
            category="preference",
            key="test_key",
            value="test_value",
            confidence=0.9,
            source="user"
        )
        stored = memory_store.store_memory(fact)

        # Delete
        deleted = memory_store.delete_memory(stored.id)
        assert deleted is True

        # Verify deletion
        retrieved = memory_store.get_memory(stored.id)
        assert retrieved is None

    def test_get_memory(self, memory_store):
        """Test retrieving a memory fact by ID."""
        fact = MemoryFact(
            scope="user",
            category="preference",
            key="test_key",
            value="test_value",
            confidence=0.9,
            source="user"
        )
        stored = memory_store.store_memory(fact)

        # Retrieve
        retrieved = memory_store.get_memory(stored.id)
        assert retrieved is not None
        assert retrieved.id == stored.id
        assert retrieved.key == "test_key"

    def test_get_stats(self, memory_store, sample_facts):
        """Test getting memory store statistics."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        stats = memory_store.get_stats()
        assert stats["total_facts"] == 5
        assert stats["by_scope"]["user"] == 2
        assert stats["by_scope"]["project"] == 2
        assert stats["by_scope"]["session"] == 1
        assert "average_confidence" in stats

    def test_validation_invalid_scope(self, memory_store):
        """Test validation with invalid scope."""
        with pytest.raises(ValueError, match="Invalid scope"):
            MemoryFact(
                scope="invalid",
                category="preference",
                key="test_key",
                value="test_value",
                confidence=0.9,
                source="user"
            )

    def test_validation_invalid_category(self, memory_store):
        """Test validation with invalid category."""
        with pytest.raises(ValueError, match="Invalid category"):
            MemoryFact(
                scope="user",
                category="invalid",
                key="test_key",
                value="test_value",
                confidence=0.9,
                source="user"
            )

    def test_validation_invalid_confidence(self, memory_store):
        """Test validation with invalid confidence."""
        with pytest.raises(ValueError, match="Confidence must be between"):
            MemoryFact(
                scope="user",
                category="preference",
                key="test_key",
                value="test_value",
                confidence=1.5,
                source="user"
            )


# ============================================================================
# MemoryWriter Tests
# ============================================================================

class TestMemoryWriter:
    """Test MemoryWriter extraction logic."""

    def test_extract_memory_empty_response(self, memory_writer):
        """Test extraction with empty interaction."""
        interaction = {"role": "user", "content": ""}
        facts = memory_writer.extract_memory(interaction)
        assert facts == []

    def test_extract_memory_explicit_prefer(self, memory_writer):
        """Test extraction of explicit preference."""
        interaction = {"role": "user", "content": "I prefer JSON output"}
        facts = memory_writer.extract_memory(interaction)

        assert len(facts) == 1
        assert facts[0].category == "preference"
        assert facts[0].key == "user_preference"

    def test_extract_memory_always_use(self, memory_writer):
        """Test extraction of 'always use' pattern."""
        interaction = {"role": "user", "content": "Always use Python for this project"}
        facts = memory_writer.extract_memory(interaction)

        assert len(facts) == 1
        assert facts[0].category == "preference"
        assert facts[0].key == "always_use"

    def test_extract_memory_we_are_using(self, memory_writer):
        """Test extraction of 'we're using' pattern."""
        interaction = {"role": "user", "content": "We're using Python and FastAPI"}
        facts = memory_writer.extract_memory(interaction)

        assert len(facts) >= 1
        assert any(f.key == "programming_language" for f in facts)

    def test_extract_memory_non_user_role(self, memory_writer):
        """Test that non-user messages are not extracted."""
        interaction = {"role": "assistant", "content": "Remember: I prefer JSON"}
        facts = memory_writer.extract_memory(interaction)
        assert facts == []

    def test_parse_valid_json_response(self, memory_writer):
        """Test parsing valid JSON response."""
        response = '{"facts": [{"scope": "user", "category": "preference", "key": "test", "value": "value", "confidence": 0.9, "source": "user"}]}'
        facts = memory_writer._parse_and_validate_response(response, "user")

        assert len(facts) == 1
        assert facts[0].category == "preference"

    def test_parse_empty_facts_response(self, memory_writer):
        """Test parsing response with empty facts array."""
        response = '{"facts": []}'
        facts = memory_writer._parse_and_validate_response(response, "user")
        assert facts == []

    def test_parse_invalid_json(self, memory_writer):
        """Test parsing invalid JSON."""
        response = "invalid json"
        facts = memory_writer._parse_and_validate_response(response, "user")
        assert facts == []

    def test_dict_to_memory_fact(self, memory_writer):
        """Test converting dict to MemoryFact."""
        data = {
            "scope": "user",
            "category": "preference",
            "key": "test_key",
            "value": "test_value",
            "confidence": 0.9,
            "source": "user"
        }

        fact = memory_writer._dict_to_memory_fact(data, "user")
        assert fact.scope == "user"
        assert fact.category == "preference"
        assert fact.key == "test_key"


# ============================================================================
# MemoryReader Tests
# ============================================================================

class TestMemoryReader:
    """Test MemoryReader querying and injection."""

    def test_query_memory(self, memory_reader, memory_store, sample_facts):
        """Test querying memory facts."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        # Query
        facts = memory_reader.query_memory(scope="user")
        assert len(facts) == 2

    def test_get_all_for_scope(self, memory_reader, memory_store, sample_facts):
        """Test getting all facts for a scope."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        user_facts = memory_reader.get_all_for_scope("user")
        assert len(user_facts) == 2

    def test_get_preferences(self, memory_reader, memory_store, sample_facts):
        """Test getting all preferences."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        preferences = memory_reader.get_preferences()
        assert len(preferences) == 2
        assert all(f.category == "preference" for f in preferences)

    def test_format_facts_for_prompt(self, memory_reader, sample_facts):
        """Test formatting facts for prompt injection."""
        formatted = memory_reader.format_facts_for_prompt(sample_facts)

        assert formatted != ""
        assert "Preferences:" in formatted
        assert "output_format" in formatted

    def test_format_facts_single(self, memory_reader):
        """Test formatting a single fact."""
        fact = MemoryFact(
            scope="user",
            category="preference",
            key="test_key",
            value="test_value",
            confidence=0.9,
            source="user"
        )

        formatted = memory_reader._format_single_fact(fact, include_confidence=True)
        assert "test_key" in formatted
        assert "test_value" in formatted
        assert "0.90" in formatted

    def test_inject_into_prompt(self, memory_reader, sample_facts):
        """Test injecting facts into prompt."""
        user_query = "Help me build an API"

        augmented = memory_reader.inject_into_prompt(sample_facts, user_query)

        assert user_query in augmented
        assert "persistent facts" in augmented.lower() or "known facts" in augmented.lower()

    def test_build_memory_context(self, memory_reader, memory_store, sample_facts):
        """Test building memory context."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        context = memory_reader.build_memory_context(max_facts=5)

        assert "output_format" in context
        assert "programming_language" in context

    def test_detect_conflicts(self, memory_reader):
        """Test conflict detection."""
        facts = [
            MemoryFact(
                scope="user",
                category="preference",
                key="output_format",
                value="json",
                confidence=0.9,
                source="user"
            ),
            MemoryFact(
                scope="user",
                category="preference",
                key="output_format",
                value="markdown",
                confidence=0.8,
                source="user"
            )
        ]

        conflicts = memory_reader.detect_conflicts(facts)
        assert "output_format" in conflicts
        assert len(conflicts["output_format"]) == 2

    def test_resolve_conflicts_highest_confidence(self, memory_reader):
        """Test resolving conflicts with highest confidence strategy."""
        facts = [
            MemoryFact(
                scope="user",
                category="preference",
                key="output_format",
                value="json",
                confidence=0.9,
                source="user"
            ),
            MemoryFact(
                scope="user",
                category="preference",
                key="output_format",
                value="markdown",
                confidence=0.8,
                source="user"
            )
        ]

        resolved = memory_reader.resolve_conflicts(facts, strategy="highest_confidence")

        # Should only have one fact (highest confidence)
        output_facts = [f for f in resolved if f.key == "output_format"]
        assert len(output_facts) == 1
        assert output_facts[0].value == json.dumps("json")
        assert output_facts[0].confidence == 0.9

    def test_get_summary(self, memory_reader, memory_store, sample_facts):
        """Test getting memory summary."""
        # Store facts
        for fact in sample_facts:
            memory_store.store_memory(fact)

        summary = memory_reader.get_summary(scope="user")
        assert summary["scope"] == "user"
        assert summary["total_facts"] == 2
        assert "preference" in summary["by_category"]


# ============================================================================
# Integration Tests
# ============================================================================

class TestIntegration:
    """Integration tests for the memory subsystem."""

    def test_full_workflow(self, temp_db):
        """Test complete workflow: extract, store, query, inject."""
        # Initialize components
        writer = MemoryWriter()
        reader = MemoryReader(temp_db)
        store = get_memory_store(temp_db)

        # Extract and store facts
        interaction = {"role": "user", "content": "I prefer JSON output for all responses"}
        facts = writer.extract_memory(interaction, scope="user")

        for fact in facts:
            store.store_memory(fact)

        # Query facts
        stored_facts = reader.query_memory(scope="user", category="preference")

        # Inject into prompt
        user_query = "Generate a response"
        augmented = reader.inject_into_prompt(stored_facts, user_query)

        # Verify
        assert len(stored_facts) > 0
        assert user_query in augmented

    def test_extract_and_store_convenience(self, temp_db):
        """Test convenience function extract_and_store."""
        interaction = {"role": "user", "content": "Always use Python for this project"}

        stored = extract_and_store(interaction, scope="user", db_path=temp_db)

        assert len(stored) > 0

    def test_inject_memory_context_convenience(self, temp_db):
        """Test convenience function inject_memory_context."""
        # Store a fact
        store = get_memory_store(temp_db)
        fact = MemoryFact(
            scope="session",
            category="preference",
            key="language",
            value="Python",
            confidence=0.9,
            source="user"
        )
        store.store_memory(fact)

        # Inject context
        user_query = "Help me write code"
        augmented = inject_memory_context(user_query, scope="session", db_path=temp_db)

        assert user_query in augmented

    def test_audit_log(self, temp_db):
        """Test audit log functionality."""
        store = get_memory_store(temp_db)

        # Store fact
        fact = MemoryFact(
            scope="user",
            category="preference",
            key="test",
            value="value1",
            confidence=0.9,
            source="user"
        )
        stored = store.store_memory(fact)

        # Update fact
        updated = MemoryFact(
            id=stored.id,
            scope="user",
            category="preference",
            key="test",
            value="value2",
            confidence=0.95,
            source="user"
        )
        store.update_memory(updated)

        # Check audit log
        audit_log = store.get_audit_log(stored.id)

        # Should have INSERT and UPDATE entries
        operations = [entry["operation"] for entry in audit_log]
        assert "INSERT" in operations
        assert "UPDATE" in operations


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
