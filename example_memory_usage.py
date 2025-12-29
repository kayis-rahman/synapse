#!/usr/bin/env python3
"""
Symbolic Memory System - Example Usage

This script demonstrates the complete Symbolic Memory subsystem workflow:
1. Storing memory facts
2. Querying memory
3. LLM-assisted extraction
4. Injecting memory into prompts

Design Principles (NON-NEGOTIABLE):
- Memory ≠ conversation history
- Memory writes are explicit, not automatic
- No embeddings, no vector DB
- Every memory entry has: scope, category, confidence, source
"""

import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

from rag.memory_store import MemoryFact, get_memory_store
from rag.memory_writer import MemoryWriter, extract_and_store
from rag.memory_reader import MemoryReader, get_memory_reader, inject_memory_context


def print_section(title: str):
    """Print a section header."""
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)


def example_1_store_memory():
    """Example 1: Store memory facts explicitly."""
    print_section("Example 1: Storing Memory Facts Explicitly")

    store = get_memory_store()

    # Example: User preference
    preference_fact = MemoryFact(
        scope="user",
        category="preference",
        key="output_format",
        value="json",
        confidence=0.95,
        source="user"
    )

    stored = store.store_memory(preference_fact)
    print(f"✓ Stored preference: {stored.to_dict()}")

    # Example: Project decision
    decision_fact = MemoryFact(
        scope="project",
        category="decision",
        key="programming_language",
        value={"language": "Python", "version": "3.11"},
        confidence=0.95,
        source="user"
    )

    stored = store.store_memory(decision_fact)
    print(f"✓ Stored decision: {stored.to_dict()}")

    # Example: Constraint
    constraint_fact = MemoryFact(
        scope="project",
        category="constraint",
        key="max_response_length",
        value=1000,
        confidence=0.90,
        source="agent"
    )

    stored = store.store_memory(constraint_fact)
    print(f"✓ Stored constraint: {stored.to_dict()}")


def example_2_query_memory():
    """Example 2: Query memory with filters."""
    print_section("Example 2: Querying Memory with Filters")

    reader = get_memory_reader()

    # Query by scope
    print("\n📌 All user preferences:")
    user_facts = reader.get_preferences(scope="user")
    for fact in user_facts:
        print(f"  - {fact.key}: {fact.to_dict()['value']} (confidence: {fact.confidence})")

    # Query by category
    print("\n📌 All project decisions:")
    decisions = reader.get_decisions(scope="project")
    for fact in decisions:
        print(f"  - {fact.key}: {fact.to_dict()['value']}")

    # Query with filters
    print("\n📌 High confidence facts (confidence >= 0.9):")
    high_conf = reader.query_memory(min_confidence=0.9, limit=5)
    for fact in high_conf:
        print(f"  - [{fact.scope}/{fact.category}] {fact.key}: {fact.to_dict()['value']}")


def example_3_extract_memory():
    """Example 3: Extract memory from interaction (rule-based)."""
    print_section("Example 3: Extract Memory from User Interaction")

    writer = MemoryWriter()

    # Example interactions
    interactions = [
        {"role": "user", "content": "I prefer JSON output for all responses"},
        {"role": "user", "content": "Always use Python for this project"},
        {"role": "user", "content": "We're using FastAPI and PostgreSQL"},
        {"role": "assistant", "content": "I'll remember that."},  # Should be ignored
        {"role": "user", "content": "Just a casual mention"}  # Should be ignored
    ]

    print("\n📝 Extracting facts from interactions...")
    for interaction in interactions:
        facts = writer.extract_memory(interaction, scope="user")

        if facts:
            print(f"\n  Input: {interaction['content']}")
            for fact in facts:
                print(f"    → Extracted: {fact.category}/{fact.key}")
                print(f"       Value: {fact.to_dict()['value']}")

    # Extract and store in one step
    print("\n📝 Extract and Store (convenience function):")
    interaction = {"role": "user", "content": "I prefer markdown format with code blocks"}
    stored = extract_and_store(interaction, scope="user", db_path="./data/memory.db")

    for fact in stored:
        print(f"  ✓ Stored: {fact.key}")


def example_4_inject_memory():
    """Example 4: Inject memory into prompts."""
    print_section("Example 4: Injecting Memory into Prompts")

    reader = get_memory_reader()

    # Get all relevant facts
    facts = reader.query_memory(min_confidence=0.7, limit=10)

    # Format for prompt injection
    print("\n📋 Formatted Memory Context:")
    formatted = reader.format_facts_for_prompt(facts, group_by_category=True)
    print(formatted)

    # Inject into user query
    user_query = "Help me build a REST API"
    print(f"\n🤖 Injecting memory into query...")
    print(f"\nOriginal Query: {user_query}")

    augmented = reader.inject_into_prompt(facts, user_query)

    print(f"\nAugmented Query (with memory context):")
    print("-" * 70)
    print(augmented)
    print("-" * 70)

    # Convenience function
    print(f"\n🤖 Using inject_memory_context() convenience function:")
    augmented_simple = inject_memory_context(user_query, scope="user", max_facts=5)
    print(augmented_simple)


def example_5_conflict_resolution():
    """Example 5: Conflict detection and resolution."""
    print_section("Example 5: Conflict Detection and Resolution")

    reader = get_memory_reader()

    # Create conflicting facts
    fact1 = MemoryFact(
        scope="user",
        category="preference",
        key="output_format",
        value="json",
        confidence=0.9,
        source="user"
    )

    fact2 = MemoryFact(
        scope="user",
        category="preference",
        key="output_format",
        value="markdown",
        confidence=0.7,
        source="user"
    )

    facts = [fact1, fact2]

    # Detect conflicts
    conflicts = reader.detect_conflicts(facts)
    print(f"\n🔍 Conflicts detected: {list(conflicts.keys())}")

    # Resolve conflicts
    print("\n🔧 Resolving conflicts (highest confidence wins):")
    resolved = reader.resolve_conflicts(facts, strategy="highest_confidence")

    for fact in resolved:
        if fact.key == "output_format":
            value = fact.to_dict()["value"]
            print(f"  ✓ Kept: {value} (confidence: {fact.confidence})")


def example_6_full_workflow():
    """Example 6: Complete end-to-end workflow."""
    print_section("Example 6: Complete End-to-End Workflow")

    # 1. User interaction
    interaction = {
        "role": "user",
        "content": "I prefer JSON output and we're using Python for this project"
    }

    print(f"\n💬 User Interaction: {interaction['content']}")

    # 2. Extract and store memory
    print("\n📝 Step 1: Extract and Store Memory")
    writer = MemoryWriter()
    store = get_memory_store()

    extracted_facts = writer.extract_memory(interaction, scope="user")
    stored_facts = []

    for fact in extracted_facts:
        stored = store.store_memory(fact)
        if stored:
            stored_facts.append(stored)
            print(f"  ✓ Stored: {fact.key}")

    # 3. Query memory
    print("\n🔍 Step 2: Query Relevant Memory")
    reader = get_memory_reader()
    relevant_facts = reader.query_memory(scope="user", min_confidence=0.8)

    print(f"  Found {len(relevant_facts)} relevant facts")

    # 4. Inject into prompt
    print("\n🤖 Step 3: Inject Memory into Prompt")
    user_query = "Generate a response"

    augmented = reader.inject_into_prompt(relevant_facts, user_query)

    print("\n" + "-" * 70)
    print(augmented)
    print("-" * 70)

    print("\n✅ Workflow complete!")


def example_7_statistics():
    """Example 7: Get memory statistics."""
    print_section("Example 7: Memory Statistics")

    store = get_memory_store()
    reader = get_memory_reader()

    # Store stats
    stats = store.get_stats()
    print("\n📊 Memory Store Statistics:")
    print(f"  Total facts: {stats['total_facts']}")
    print(f"  Average confidence: {stats['average_confidence']}")
    print(f"\n  By scope:")
    for scope, count in stats['by_scope'].items():
        print(f"    - {scope}: {count} facts")

    print(f"\n  By category:")
    for category, count in stats['by_category'].items():
        print(f"    - {category}: {count} facts")

    # Reader summary
    print("\n📊 Reader Summary (user scope):")
    summary = reader.get_summary(scope="user")
    print(f"  Total: {summary['total_facts']} facts")
    for category, count in summary['by_category'].items():
        print(f"  - {category}: {count}")

    # Audit log
    print("\n📋 Recent Audit Log (last 5 entries):")
    audit_log = store.get_audit_log()[:5]
    for entry in audit_log:
        print(f"  [{entry['operation']}] {entry['fact_id'][:8]}... "
              f"by {entry['changed_by']}")


def main():
    """Run all examples."""
    print("\n" + "=" * 70)
    print("  Symbolic Memory System - Example Usage")
    print("  Phase 1: Symbolic Memory Subsystem")
    print("=" * 70)

    try:
        example_1_store_memory()
        example_2_query_memory()
        example_3_extract_memory()
        example_4_inject_memory()
        example_5_conflict_resolution()
        example_6_full_workflow()
        example_7_statistics()

        print("\n" + "=" * 70)
        print("  ✅ All examples completed successfully!")
        print("=" * 70 + "\n")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
