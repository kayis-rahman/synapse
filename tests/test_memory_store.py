"""Test memory store functionality"""
import pytest
import tempfile
import os


def test_store_memory_fact():
    """Test storing a symbolic memory fact"""
    from synapse.rag import MemoryStore, MemoryFact
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        store = MemoryStore(temp_db)
        
        fact = MemoryFact(
            scope="test",
            category="test",
            key="test_key",
            value="test_value",
            confidence=1.0,
            source="test"
        )
        
        stored_fact = store.store_memory(fact)
        
        assert stored_fact.id is not None
        assert stored_fact.scope == "test"
        assert stored_fact.key == "test_key"
        assert stored_fact.value == "test_value"
        assert stored_fact.confidence == 1.0
        
        # Test retrieval
        facts = store.query_memory(scope="test", key="test_key")
        assert len(facts) == 1
        assert facts[0].value == "test_value"
        
        # Test update (replace)
        updated_fact = MemoryFact(
            scope="test",
            category="test",
            key="test_key",
            value="new_value",
            confidence=0.9,
            source="test"
        )
        store.store_memory(updated_fact)
        
        facts = store.query_memory(scope="test", key="test_key")
        assert len(facts) == 1
        assert facts[0].value == "new_value"


def test_query_memory_by_scope():
    """Test querying all facts for a scope"""
    from synapse.rag import MemoryStore
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        store = MemoryStore(temp_db)
        
        # Store multiple facts
        for i in range(3):
            fact = MemoryFact(
                scope="test",
                category="test",
                key=f"key_{i}",
                value=f"value_{i}",
                confidence=1.0,
                source="test"
            )
            store.store_memory(fact)
        
        # Query by scope
        facts = store.query_memory(scope="test")
        assert len(facts) == 3


def test_query_memory_by_min_confidence():
    """Test querying facts with minimum confidence"""
    from synapse.rag import MemoryStore
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        store = MemoryStore(temp_db)
        
        # Store facts with different confidences
        for conf in [0.5, 0.7, 1.0]:
            fact = MemoryFact(
                scope="test",
                category="test",
                key=f"conf_{conf}",
                value=f"value_{conf}",
                confidence=conf,
                source="test"
            )
            store.store_memory(fact)
        
        # Query with min_confidence
        facts = store.query_memory(scope="test", min_confidence=0.8)
        assert len(facts) == 2  # 0.7 and 1.0


def test_query_memory_by_category():
    """Test querying facts by category"""
    from synapse.rag import MemoryStore
    
    with tempfile.NamedTemporaryFile(suffix='.db') as temp_db:
        store = MemoryStore(temp_db)
        
        # Store facts with different categories
        for cat in ["preference", "constraint", "decision", "fact"]:
            fact = MemoryFact(
                scope="test",
                category=cat,
                key=f"key_{cat}",
                value=f"value_{cat}",
                confidence=1.0,
                source="test"
            )
            store.store_memory(fact)
        
        # Query by category
        facts = store.query_memory(scope="test", category="preference")
        assert len(facts) == 1
