#!/usr/bin/env python3
"""
Test query expansion functionality.

Simple test to verify query expansion works correctly.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.query_expander import QueryExpander


def test_query_expansion():
    """Test basic query expansion."""
    expander = QueryExpander(num_expansions=3)

    test_cases = [
        {
            "query": "How do I handle authentication errors?",
            "expected_keywords": ["auth", "error", "handle"]
        },
        {
            "query": "create a new user in the database",
            "expected_keywords": ["create", "user", "database"]
        },
        {
            "query": "debug API endpoint issues",
            "expected_keywords": ["debug", "api", "endpoint", "issues"]
        }
    ]

    print("Testing Query Expansion\n" + "=" * 50)

    all_passed = True

    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: '{test_case['query']}'")
        print("-" * 50)

        # Expand query
        expanded_queries = expander.expand_query(test_case["query"])

        print(f"Original Query: {test_case['query']}")
        print(f"Expanded Queries ({len(expanded_queries)}):")
        for j, exp_query in enumerate(expanded_queries, 1):
            print(f"  {j}. {exp_query}")

        # Check if expansions contain expected keywords
        all_expanded = " ".join(expanded_queries).lower()
        missing_keywords = [
            kw for kw in test_case["expected_keywords"]
            if kw not in all_expanded
        ]

        if missing_keywords:
            print(f"⚠ Missing expected keywords: {missing_keywords}")
            all_passed = False
        else:
            print(f"✓ All expected keywords found")

    print("\n" + "=" * 50)

    # Test result merging
    print("\nTesting Result Merging\n" + "=" * 50)

    # Simulate results from multiple queries
    results_1 = [
        {"content": "Authentication error handling guide", "score": 0.9, "metadata": {"source": "doc1"}},
        {"content": "How to handle auth errors", "score": 0.85, "metadata": {"source": "doc2"}}
    ]

    results_2 = [
        {"content": "Authentication error handling guide", "score": 0.88, "metadata": {"source": "doc1"}},
        {"content": "Debugging authentication", "score": 0.75, "metadata": {"source": "doc3"}}
    ]

    results_3 = [
        {"content": "Error handling in authentication", "score": 0.82, "metadata": {"source": "doc4"}},
        {"content": "Authentication error handling guide", "score": 0.92, "metadata": {"source": "doc1"}}
    ]

    all_results = [results_1, results_2, results_3]

    merged = expander.merge_results(all_results, top_k=3)

    print("\nMerged Results (Top 3):")
    for i, result in enumerate(merged, 1):
        print(f"{i}. {result['content'][:60]}...")
        print(f"   Score: {result['score']:.2f}, Found by: {result['query_count']} queries")

    # Check if deduplication worked
    content_count = len([r for r in merged if "Authentication error handling guide" in r['content']])
    if content_count == 1:
        print("\n✓ Deduplication working correctly")
    else:
        print(f"\n⚠ Deduplication failed (found {content_count} duplicates)")
        all_passed = False

    print("\n" + "=" * 50)

    if all_passed:
        print("\n✓ All tests passed!")
        return 0
    else:
        print("\n⚠ Some tests failed")
        return 1


if __name__ == "__main__":
    sys.exit(test_query_expansion())
