#!/usr/bin/env python3
"""
Comprehensive Query Expansion Test - Real-World Scenarios

Tests query expansion with realistic queries based on pi-rag project functionality.

Measures:
1. Baseline (no expansion) vs Improved (with expansion)
2. Result count improvement
3. Relevance score improvement
4. Document coverage
5. Term matching

Expected: 15-25% recall improvement
"""

import sys
import os
import json
from typing import List, Dict, Any
from datetime import datetime

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from rag.semantic_retriever import SemanticRetriever


class QueryExpansionBenchmark:
    """
    Benchmark query expansion with realistic queries.
    """

    # Realistic queries based on pi-rag project functionality
    TEST_QUERIES = [
        {
            "query": "How do I configure authentication in the RAG system?",
            "category": "Configuration",
            "expected_terms": ["auth", "config", "authentication", "system"],
            "priority": "high"
        },
        {
            "query": "Create a new memory fact for user preferences",
            "category": "Memory",
            "expected_terms": ["create", "memory", "fact", "preference"],
            "priority": "high"
        },
        {
            "query": "What API endpoints are available for the RAG system?",
            "category": "API",
            "expected_terms": ["api", "endpoint", "rag", "system"],
            "priority": "high"
        },
        {
            "query": "Debug memory storage issues in the database",
            "category": "Debugging",
            "expected_terms": ["debug", "memory", "storage", "database", "issue"],
            "priority": "medium"
        },
        {
            "query": "How to deploy the RAG system using Docker?",
            "category": "Deployment",
            "expected_terms": ["deploy", "docker", "rag", "system"],
            "priority": "medium"
        },
        {
            "query": "Handle authentication errors in the API",
            "category": "Error Handling",
            "expected_terms": ["handle", "auth", "error", "api"],
            "priority": "high"
        },
        {
            "query": "List all available models in the model manager",
            "category": "Model Management",
            "expected_terms": ["list", "model", "manager", "available"],
            "priority": "medium"
        },
        {
            "query": "Configure embedding cache for better performance",
            "category": "Performance",
            "expected_terms": ["config", "embedding", "cache", "performance"],
            "priority": "medium"
        },
        {
            "query": "How do I ingest new documents into semantic memory?",
            "category": "Ingestion",
            "expected_terms": ["ingest", "document", "semantic", "memory"],
            "priority": "high"
        },
        {
            "query": "Remove or delete a model from the registry",
            "category": "Model Management",
            "expected_terms": ["remove", "delete", "model", "registry"],
            "priority": "medium"
        }
    ]

    def __init__(self):
        """Initialize benchmark."""
        self.retriever = SemanticRetriever(
            query_expansion_enabled=False,
            num_expansions=3
        )

    def test_query(self, query: str, expected_terms: List[str]) -> Dict[str, Any]:
        """
        Test a single query with and without expansion.

        Returns:
            Dictionary with metrics
        """
        # Test without expansion (baseline)
        self.retriever.query_expansion_enabled = False
        baseline_results = self.retriever.retrieve(
            query=query,
            trigger="external_info_needed",
            top_k=10
        )

        # Test with expansion (improved)
        self.retriever.query_expansion_enabled = True
        improved_results = self.retriever.retrieve_with_expansion(
            query=query,
            trigger="external_info_needed",
            top_k=10,
            num_expansions=3
        )

        # Calculate metrics
        baseline_count = len(baseline_results)
        improved_count = len(improved_results)

        # Calculate average scores
        baseline_avg_score = sum(r.get("score", 0) for r in baseline_results) / max(baseline_count, 1)
        improved_avg_score = sum(r.get("score", 0) for r in improved_results) / max(improved_count, 1)

        # Calculate term coverage
        baseline_content = " ".join([r.get("content", "") for r in baseline_results]).lower()
        improved_content = " ".join([r.get("content", "") for r in improved_results]).lower()

        baseline_terms = sum(1 for term in expected_terms if term in baseline_content)
        improved_terms = sum(1 for term in expected_terms if term in improved_content)

        # Calculate document coverage (unique sources)
        baseline_sources = len(set(r.get("metadata", {}).get("source", "") for r in baseline_results))
        improved_sources = len(set(r.get("metadata", {}).get("source", "") for r in improved_results))

        # Calculate improvement percentages
        count_improvement = self._calc_improvement(baseline_count, improved_count)
        score_improvement = self._calc_improvement(baseline_avg_score, improved_avg_score)
        terms_improvement = self._calc_improvement(baseline_terms, improved_terms)
        sources_improvement = self._calc_improvement(baseline_sources, improved_sources)

        return {
            "query": query,
            "baseline": {
                "count": baseline_count,
                "avg_score": baseline_avg_score,
                "terms": baseline_terms,
                "sources": baseline_sources,
                "results": baseline_results
            },
            "improved": {
                "count": improved_count,
                "avg_score": improved_avg_score,
                "terms": improved_terms,
                "sources": improved_sources,
                "results": improved_results
            },
            "improvement": {
                "count_pct": count_improvement,
                "score_pct": score_improvement,
                "terms_pct": terms_improvement,
                "sources_pct": sources_improvement
            },
            "expected_terms": expected_terms,
            "better": improved_count > baseline_count or improved_terms > baseline_terms
        }

    def _calc_improvement(self, baseline: float, improved: float) -> float:
        """Calculate percentage improvement."""
        if baseline == 0:
            return 100.0 if improved > 0 else 0.0
        return ((improved - baseline) / baseline) * 100

    def run_benchmark(self) -> Dict[str, Any]:
        """
        Run full benchmark on all test queries.

        Returns:
            Dictionary with all results and summary
        """
        print("=" * 80)
        print("Query Expansion Benchmark - Real-World Scenarios")
        print("=" * 80)
        print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Test Queries: {len(self.TEST_QUERIES)}")
        print()

        results = []

        for i, test_case in enumerate(self.TEST_QUERIES, 1):
            query = test_case["query"]
            category = test_case["category"]
            expected_terms = test_case["expected_terms"]
            priority = test_case["priority"]

            print(f"[{i}/{len(self.TEST_QUERIES)}] {category} ({priority} priority)")
            print(f"Query: {query}")
            print("-" * 80)

            # Test query
            result = self.test_query(query, expected_terms)
            result["category"] = category
            result["priority"] = priority

            # Display results
            baseline = result["baseline"]
            improved = result["improved"]
            improvement = result["improvement"]

            print(f"Baseline (no expansion):")
            print(f"  Results: {baseline['count']}")
            print(f"  Avg Score: {baseline['avg_score']:.3f}")
            print(f"  Terms: {baseline['terms']}/{len(expected_terms)}")
            print(f"  Sources: {baseline['sources']}")

            print(f"Improved (with expansion):")
            print(f"  Results: {improved['count']}")
            print(f"  Avg Score: {improved['avg_score']:.3f}")
            print(f"  Terms: {improved['terms']}/{len(expected_terms)}")
            print(f"  Sources: {improved['sources']}")

            print(f"Improvement:")
            print(f"  Count: {improvement['count_pct']:+.1f}%")
            print(f"  Score: {improvement['score_pct']:+.1f}%")
            print(f"  Terms: {improvement['terms_pct']:+.1f}%")
            print(f"  Sources: {improvement['sources_pct']:+.1f}%")

            # Show top results
            print(f"Top Results (with expansion):")
            for j, r in enumerate(improved['results'][:3], 1):
                source = os.path.basename(r.get("metadata", {}).get("source", "unknown"))
                score = r.get("score", 0)
                content = r.get("content", "")[:70].replace("\n", " ")
                print(f"  {j}. [{source}] Score: {score:.3f} - {content}...")

            print()

            results.append(result)

        # Calculate summary
        summary = self._calculate_summary(results)

        # Display summary
        self._display_summary(summary)

        return {
            "results": results,
            "summary": summary,
            "timestamp": datetime.now().isoformat()
        }

    def _calculate_summary(self, results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate summary statistics."""
        better_count = sum(1 for r in results if r["better"])

        avg_count_improvement = sum(r["improvement"]["count_pct"] for r in results) / len(results)
        avg_score_improvement = sum(r["improvement"]["score_pct"] for r in results) / len(results)
        avg_terms_improvement = sum(r["improvement"]["terms_pct"] for r in results) / len(results)
        avg_sources_improvement = sum(r["improvement"]["sources_pct"] for r in results) / len(results)

        # Success criteria
        success = avg_count_improvement > 0 or avg_terms_improvement > 0

        return {
            "total_queries": len(results),
            "better_count": better_count,
            "better_percentage": (better_count / len(results)) * 100,
            "avg_count_improvement": avg_count_improvement,
            "avg_score_improvement": avg_score_improvement,
            "avg_terms_improvement": avg_terms_improvement,
            "avg_sources_improvement": avg_sources_improvement,
            "success": success,
            "meets_target": avg_count_improvement >= 15 or avg_terms_improvement >= 15
        }

    def _display_summary(self, summary: Dict[str, Any]):
        """Display summary statistics."""
        print("=" * 80)
        print("Summary")
        print("=" * 80)
        print(f"Total Queries: {summary['total_queries']}")
        print(f"Queries with Improvement: {summary['better_count']}/{summary['total_queries']} ({summary['better_percentage']:.1f}%)")
        print()
        print("Average Improvements:")
        print(f"  Result Count: {summary['avg_count_improvement']:+.1f}%")
        print(f"  Average Score: {summary['avg_score_improvement']:+.1f}%")
        print(f"  Term Coverage: {summary['avg_terms_improvement']:+.1f}%")
        print(f"  Source Coverage: {summary['avg_sources_improvement']:+.1f}%")
        print()

        if summary["success"]:
            print("✅ Query Expansion is improving retrieval quality")
            if summary["meets_target"]:
                print("✅ Meets target: ≥15% improvement achieved")
            else:
                print("⚠ Target not met: ≥15% improvement expected")
        else:
            print("⚠ No significant improvement observed")

        print()

        # Overall score
        overall_improvement = (summary['avg_count_improvement'] +
                           summary['avg_terms_improvement']) / 2

        if overall_improvement >= 15:
            print(f"🎯 Overall Improvement: {overall_improvement:.1f}% (Target: ≥15%) ✅")
        elif overall_improvement >= 0:
            print(f"📊 Overall Improvement: {overall_improvement:.1f}% (Target: ≥15%)")
        else:
            print(f"❌ Overall Improvement: {overall_improvement:.1f}% (Target: ≥15%)")

        print("=" * 80)


def main():
    """Run benchmark."""
    benchmark = QueryExpansionBenchmark()
    results = benchmark.run_benchmark()

    # Return exit code based on success
    return 0 if results["summary"]["success"] else 1


if __name__ == "__main__":
    sys.exit(main())
