"""
Example Usage of Phase 3: Episodic Memory

This script demonstrates how to:
1. Extract episodes from agent interactions
2. Store episodes in episodic memory
3. Retrieve episodes for planning
4. Use episodes in agent prompts

Run this script to see episodic memory in action.
"""

import json
import tempfile
from typing import Dict, Any

# Import episodic memory components
from rag.episodic_store import Episode, EpisodicStore, get_episodic_store
from rag.episode_extractor import EpisodeExtractor, create_simple_llm_func
from rag.episodic_reader import EpisodicReader, get_episodic_reader


def example_1_basic_episode_storage():
    """Example 1: Basic episode storage and retrieval."""
    print("\n" + "="*70)
    print("EXAMPLE 1: Basic Episode Storage and Retrieval")
    print("="*70)

    # Create a temporary database for this example
    db_path = tempfile.mktemp(suffix="_episodic_example.db")
    store = EpisodicStore(db_path)

    # Create an episode
    episode = Episode(
        situation="Large repository with unclear entry point",
        action="Searched filenames before reading files",
        outcome="Found relevant code quickly",
        lesson="For large repos, perform keyword search before file traversal",
        confidence=0.85
    )

    print(f"\nCreated Episode:")
    print(f"  Situation: {episode.situation}")
    print(f"  Action:    {episode.action}")
    print(f"  Outcome:   {episode.outcome}")
    print(f"  Lesson:    {episode.lesson}")
    print(f"  Confidence: {episode.confidence}")

    # Validate episode
    if episode.validate():
        print("✓ Episode is valid (abstracted, not a fact)")

        # Store episode
        stored = store.store_episode(episode)
        print(f"✓ Episode stored with ID: {stored.id}")

        # Retrieve episode
        retrieved = store.get_episode(stored.id)
        print(f"✓ Episode retrieved: {retrieved.lesson}")

    else:
        print("✗ Episode is invalid (not abstracted or missing fields)")

    # Clean up
    import os
    if os.path.exists(db_path):
        os.remove(db_path)


def example_2_episode_validation():
    """Example 2: Episode validation - facts vs. lessons."""
    print("\n" + "="*70)
    print("EXAMPLE 2: Episode Validation (Facts vs. Lessons)")
    print("="*70)

    # Valid lesson
    valid_episode = Episode(
        situation="Large repository navigation",
        action="Used filename search first",
        outcome="Found code faster",
        lesson="For large repos, search filenames before reading files",
        confidence=0.9
    )

    print(f"\nValid Episode:")
    print(f"  Lesson: {valid_episode.lesson}")
    print(f"  Valid:  {valid_episode.validate()}")

    # Invalid: Fact (belongs in symbolic memory)
    fact_episode = Episode(
        situation="Project setup",
        action="Read README",
        outcome="Found language",
        lesson="Project uses Go",  # This is a FACT, not a lesson
        confidence=0.95
    )

    print(f"\nInvalid Episode (Fact):")
    print(f"  Lesson: {fact_episode.lesson}")
    # Note: Validation focuses on length and similarity, not fact detection
    # Fact detection happens in EpisodeExtractor
    print(f"  Valid (basic): {fact_episode.validate()}")
    print("  (Fact detection happens in EpisodeExtractor, not Episode.validate())")

    # Invalid: Too verbose (not abstracted)
    verbose_lesson = "When searching for authentication in a repository, " * 100
    verbose_episode = Episode(
        situation="Repository navigation",
        action="Searched for auth code",
        outcome="Found it",
        lesson=verbose_lesson,
        confidence=0.8
    )

    print(f"\nInvalid Episode (Too Verbose):")
    print(f"  Lesson length: {len(verbose_episode.lesson)} chars")
    print(f"  Valid: {verbose_episode.validate()}")
    print("  (Lessons must be < 500 chars and abstracted)")


def example_3_llm_extraction():
    """Example 3: LLM-assisted episode extraction."""
    print("\n" + "="*70)
    print("EXAMPLE 3: LLM-Assisted Episode Extraction")
    print("="*70)

    # Mock LLM function for demonstration
    def mock_llm(prompt: str) -> str:
        """Mock LLM that returns a valid episode."""
        print(f"\n[Mock LLM received prompt with {len(prompt)} chars]")
        print("[Mock LLM analyzing agent behavior...]")

        return json.dumps({
            "situation": "Large repository with unclear entry point",
            "action": "Searched filenames before reading files",
            "outcome": "Found relevant code quickly",
            "lesson": "For large repos, perform keyword search before file traversal",
            "confidence": 0.85
        })

    # Create extractor
    extractor = EpisodeExtractor(mock_llm, min_confidence=0.6)

    # Extract episode
    episode_data = extractor.extract_episode(
        situation="Large repository with unclear entry point",
        action="Searched filenames before reading files",
        outcome="Found relevant code quickly"
    )

    if episode_data:
        print("\n✓ Episode extracted successfully:")
        print(f"  Situation: {episode_data['situation']}")
        print(f"  Action:    {episode_data['action']}")
        print(f"  Outcome:   {episode_data['outcome']}")
        print(f"  Lesson:    {episode_data['lesson']}")
        print(f"  Confidence: {episode_data['confidence']}")

        # Check if lesson is abstracted
        print(f"\n  ✓ Lesson is abstract (not a fact)")
        print(f"  ✓ Lesson is concise (< 500 chars)")
        print(f"  ✓ Confidence above threshold (0.6)")
    else:
        print("\n✗ No valid episode extracted (lesson didn't qualify)")


def example_4_advisory_context():
    """Example 4: Getting advisory context for planning."""
    print("\n" + "="*70)
    print("EXAMPLE 4: Advisory Context for Planning")
    print("="*70)

    # Create temporary database
    db_path = tempfile.mktemp(suffix="_episodic_example.db")
    store = EpisodicStore(db_path)

    # Store some episodes
    episodes = [
        Episode(
            situation="Large repository navigation",
            action="Searched filenames first",
            outcome="Found code quickly",
            lesson="For large repos, search filenames before reading files",
            confidence=0.9
        ),
        Episode(
            situation="User feedback on output length",
            action="Provided concise response",
            outcome="User satisfied",
            lesson="User prefers concise output over verbose explanations",
            confidence=0.85
        ),
        Episode(
            situation="API documentation search",
            action="Searched for endpoint names",
            outcome="Found relevant endpoints",
            lesson="Search endpoint names instead of reading all docs",
            confidence=0.8
        )
    ]

    for episode in episodes:
        store.store_episode(episode)

    print(f"\nStored {len(episodes)} episodes")

    # Get advisory context for planning
    reader = EpisodicReader(db_path)

    task = "Search large repository for API endpoints"
    print(f"\nCurrent Task: {task}")

    advisory_context = reader.get_advisory_context(
        task_description=task,
        min_confidence=0.7,
        max_episodes=5
    )

    print("\nAdvisory Context:")
    print(advisory_context)

    # Get summary statistics
    summary = reader.get_summary()
    print("\nSummary Statistics:")
    print(f"  Total Episodes: {summary['total_episodes']}")
    print(f"  Avg Confidence: {summary['average_confidence']}")
    print(f"  High Confidence (>= 0.8): {summary['high_confidence_episodes']}")
    print(f"  Recent (30 days): {summary['recent_episodes_30_days']}")

    # Clean up
    import os
    if os.path.exists(db_path):
        os.remove(db_path)


def example_5_full_workflow():
    """Example 5: Full workflow - extraction, storage, planning."""
    print("\n" + "="*70)
    print("EXAMPLE 5: Full Workflow (Extract → Store → Plan)")
    print("="*70)

    # Create temporary database
    db_path = tempfile.mktemp(suffix="_episodic_example.db")
    store = EpisodicStore(db_path)

    print("\n--- STEP 1: Agent Completes Task ---")
    print("Task: Find authentication code in large repository")
    print("Agent did: Searched for 'auth' in filenames first")
    print("Result: Found auth.go file with authentication logic")

    # Mock LLM extraction
    def mock_llm(prompt: str) -> str:
        return json.dumps({
            "situation": "Large repository with unclear entry point",
            "action": "Searched filenames for 'auth' before reading files",
            "outcome": "Found authentication code quickly",
            "lesson": "For large repos, search filenames for keywords before file traversal",
            "confidence": 0.9
        })

    # Extract episode
    extractor = EpisodeExtractor(mock_llm)
    episode_data = extractor.extract_episode(
        situation="Large repository, looking for authentication",
        action="Searched for 'auth' in filenames",
        outcome="Found auth.go with authentication logic"
    )

    print("\n--- STEP 2: Extract Episode ---")
    if episode_data:
        print(f"✓ Lesson extracted: {episode_data['lesson']}")
    else:
        print("✗ No lesson qualified")
        return

    # Store episode
    episode = Episode(**episode_data)
    stored = store.store_episode(episode)
    print(f"✓ Episode stored (ID: {stored.id})")

    # Use in planning
    print("\n--- STEP 3: Use in Future Planning ---")
    print("Future Task: Search for API endpoints in another large repository")

    reader = EpisodicReader(db_path)
    advisory_context = reader.get_advisory_context(
        "Find API endpoints in large repository"
    )

    print("\nGenerated Planning Prompt:")
    print("="*70)
    print(advisory_context)
    print("="*70)

    print("\n--- STEP 4: Agent Uses Lesson ---")
    print("Agent searches for 'endpoint' in filenames first")
    print("Result: Finds api.go and endpoint.go quickly")
    print("✓ Agent applied learned lesson!")

    # Clean up
    import os
    if os.path.exists(db_path):
        os.remove(db_path)


def example_6_cleanup():
    """Example 6: Cleanup old, low-confidence episodes."""
    print("\n" + "="*70)
    print("EXAMPLE 6: Cleanup Old Episodes")
    print("="*70)

    # Create temporary database
    db_path = tempfile.mktemp(suffix="_episodic_example.db")
    store = EpisodicStore(db_path)

    # Store some episodes
    store.store_episode(Episode(
        situation="Test",
        action="Action",
        outcome="Outcome",
        lesson="High confidence lesson",
        confidence=0.9
    ))

    store.store_episode(Episode(
        situation="Test",
        action="Action",
        outcome="Outcome",
        lesson="Low confidence lesson",
        confidence=0.4
    ))

    print("\nStored 2 episodes:")
    stats = store.get_stats()
    print(f"  Total: {stats['total_episodes']}")
    print(f"  Avg Confidence: {stats['average_confidence']}")

    # Cleanup old, low-confidence episodes
    print("\nRunning cleanup:")
    print("  - Remove episodes older than 0 days")
    print("  - Remove episodes with confidence < 0.5")

    deleted = store.cleanup_old_episodes(days=0, min_confidence=0.5)
    print(f"  - Deleted {deleted} episodes")

    # Check stats after cleanup
    stats_after = store.get_stats()
    print(f"\nAfter cleanup:")
    print(f"  Total: {stats_after['total_episodes']}")
    print(f"  Avg Confidence: {stats_after['average_confidence']}")

    # Clean up
    import os
    if os.path.exists(db_path):
        os.remove(db_path)


def main():
    """Run all examples."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*10 + "PHASE 3: EPISODIC MEMORY - EXAMPLE USAGE" + " "*10 + "║")
    print("╚" + "="*68 + "╝")

    # Run examples
    example_1_basic_episode_storage()
    example_2_episode_validation()
    example_3_llm_extraction()
    example_4_advisory_context()
    example_5_full_workflow()
    example_6_cleanup()

    print("\n" + "="*70)
    print("All examples completed!")
    print("="*70)
    print("\nKey Takeaways:")
    print("  ✓ Episodes store STRATEGY, not facts")
    print("  ✓ Episodes are ADVISORY, not authoritative")
    print("  ✓ Episodes must be ABSTRACTED, not verbose")
    print("  ✓ Episodes improve planning over time")
    print("  ✓ Episodes can be cleaned up to prevent bloat")
    print("\nSee PHASE3_EPISODIC_MEMORY.md for full documentation.\n")


if __name__ == "__main__":
    main()
