#!/usr/bin/env python3
"""
Semantic Search Quality Test Suite

Tests retrieval quality by running representative queries and grading results.
"""

import json
import time
from typing import List, Dict, Any
from rag.semantic_retriever import SemanticRetriever
from rag.memory_selector import MemorySelector
from rag.semantic_store import SemanticStore


class RetrievalQualityTester:
    """
    Test semantic search quality by running representative queries.
    """

    def __init__(self):
        self.retriever = SemanticRetriever()
        self.selector = MemorySelector()

    def run_test_suite(self, queries: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Run all queries and generate quality report.

        Args:
            queries: List of query dictionaries with 'query' and 'category'

        Returns:
            Dictionary with test results and metrics
        """
        results = []
        query_times = []

        for query_dict in queries:
            query = query_dict["query"]
            category = query_dict["category"]

            print(f"\n{'='*60}")
            print(f"Testing: {query}")
            print(f"Category: {category}")
            print(f"{'='*60}")

            # Measure query time
            start = time.perf_counter()

            # Retrieve top 3 results
            semantic_results = self.retriever.retrieve(query, top_k=3)

            elapsed = (time.perf_counter() - start) * 1000  # ms
            query_times.append(elapsed)

            # Grade each result
            graded = []
            for i, result in enumerate(semantic_results):
                score = self._grade_result(query, result, i)
                graded.append({
                    "rank": i + 1,
                    "file": result.get("file", "N/A"),
                    "relevance": score,
                    "contains_answer": self._check_answer_present(query, result),
                    "context_quality": self._has_complete_context(result),
                })

            results.append({
                "query": query,
                "category": category,
                "results": graded,
                "query_time_ms": elapsed,
                "metrics": self._calculate_query_metrics(graded)
            })

        # Calculate overall metrics
        baseline = {
            "total_queries": len(queries),
            "avg_relevance": sum(r["metrics"]["avg_relevance"] for r in results) / len(results),
            "answer_present_rate": sum(r["metrics"]["answer_present"] for r in results) / len(results),
            "context_quality": sum(r["metrics"]["context_quality"] for r in results) / len(results),
            "diversity": self._calculate_diversity(results),
            "avg_query_time_ms": sum(query_times) / len(query_times),
            "p50_query_time_ms": sorted(query_times)[len(query_times) // 2],
            "p95_query_time_ms": sorted(query_times)[int(len(query_times) * 0.95)],
            "min_query_time_ms": min(query_times),
            "max_query_time_ms": max(query_times),
        }

        return {
            "results": results,
            "baseline": baseline
        }

    def _grade_result(self, query: str, result: Dict[str, Any], rank: int) -> float:
        """
        Manual grading rubric for result relevance (0-10 scale).

        Scoring criteria:
        - Contains answer (up to 3 points)
        - Semantic similarity (up to 3 points)
        - Context quality (up to 2 points)
        - Source credibility (up to 2 points)
        """
        relevance = 0

        # Check if result contains answer
        if self._check_answer_present(query, result):
            relevance += 3

        # Check semantic similarity
        if self._semantically_relevant(query, result.get("content", "")):
            relevance += 3

        # Check context quality
        if self._has_complete_context(result):
            relevance += 2

        # Check source credibility
        if self._is_core_file(result.get("file", "")):
            relevance += 2
        elif self._is_config_file(result.get("file", "")):
            relevance += 1

        return min(relevance, 10)

    def _check_answer_present(self, query: str, result: Dict[str, Any]) -> bool:
        """Check if result contains answer to the query."""
        content = result.get("content", "").lower()
        query_lower = query.lower()

        # Simple keyword matching for answer presence
        query_words = set(query_lower.split())

        # If any query word appears multiple times, likely contains answer
        word_counts = {}
        for word in content.split():
            if word in query_words:
                word_counts[word] = word_counts.get(word, 0) + 1

        # Query is present if any word appears > once
        answer_present = any(count > 1 for count in word_counts.values())

        return answer_present

    def _semantically_relevant(self, query: str, content: str) -> bool:
        """Check if content is semantically relevant to query."""
        # This is a simple heuristic - in practice you might use
        # cross-encoder embeddings or more sophisticated methods
        query_lower = query.lower()
        content_lower = content.lower()

        # Extract key terms from query
        query_terms = set(query_lower.split())

        # Check if any query term appears in content
        return len(query_terms.intersection(set(content_lower.split()))) > 0

    def _has_complete_context(self, result: Dict[str, Any]) -> bool:
        """Check if result provides complete context."""
        content = result.get("content", "")

        # Good context should have enough substance
        # Minimum 50 characters or multiple sentences
        return len(content) > 50 or content.count('.') > 2

    def _is_core_file(self, file_path: str) -> bool:
        """Check if file is a core RAG module."""
        return "rag/" in file_path and file_path.endswith(".py")

    def _is_config_file(self, file_path: str) -> bool:
        """Check if file is a configuration file."""
        return "configs/" in file_path

    def _calculate_query_metrics(self, graded: List[Dict]) -> Dict[str, float]:
        """Calculate metrics for a single query."""
        total_relevance = sum(r["relevance"] for r in graded)
        avg_relevance = total_relevance / len(graded)

        answer_present = sum(1 for r in graded if r["contains_answer"])

        context_scores = [r.get("context_quality", 0) for r in graded]
        avg_context_quality = sum(context_scores) / len(context_scores)

        return {
            "avg_relevance": avg_relevance,
            "answer_present": answer_present,
            "context_quality": avg_context_quality
        }

    def _calculate_diversity(self, results: List[Dict]) -> float:
        """Calculate diversity of results (are results from different files?)."""
        files = [r["file"] for r in results]
        unique_files = len(set(files))
        total = len(files)

        return unique_files / total if total > 0 else 0


def generate_test_queries() -> List[Dict[str, str]]:
    """Generate representative test queries for pi-rag codebase."""

    return [
        # Technical Implementation (5)
        {"query": "How does the RAG orchestrator handle streaming responses?", "category": "implementation"},
        {"query": "What is the semantic memory chunking strategy?", "category": "implementation"},
        {"query": "How are embeddings generated and cached?", "category": "implementation"},
        {"query": "What is the difference between symbolic and episodic memory?", "category": "implementation"},
        {"query": "How does the MCP server tool ingestion work?", "category": "implementation"},

        # Configuration Questions (5)
        {"query": "What is the current chunk size and overlap?", "category": "configuration"},
        {"query": "How is the embedding cache configured?", "category": "configuration"},
        {"query": "What is the min_retrieval_score threshold?", "category": "configuration"},
        {"query": "What memory scope is configured?", "category": "configuration"},
        {"query": "How is the authority hierarchy enforced?", "category": "configuration"},

        # Feature-Specific Questions (5)
        {"query": "How does query caching work?", "category": "features"},
        {"query": "What file types are supported for ingestion?", "category": "features"},
        {"query": "How is the chroma vector store integrated?", "category": "features"},
        {"query": "What metrics are tracked in MCP server?", "category": "features"},
        {"query": "How does the memory selector choose between memory types?", "category": "features"},

        # Integration Questions (5)
        {"query": "How to configure RAG for production deployment?", "category": "integration"},
        {"query": "What are the Docker deployment options?", "category": "integration"},
        {"query": "How does the system handle large file ingestion?", "category": "integration"},
        {"query": "What are the backup requirements for data?", "category": "integration"},
        {"query": "How to integrate with external chat APIs?", "category": "integration"}
    ]


def main():
    """Run retrieval quality test suite."""
    print("=" * 70)
    print("Semantic Search Quality Test Suite")
    print("=" * 70)
    print()

    # Initialize tester
    tester = RetrievalQualityTester()

    # Generate test queries
    queries = generate_test_queries()
    print(f"Generated {len(queries)} test queries across {len(set(q['category'] for q in queries))} categories")
    print()

    # Run test suite
    print("Running test queries...")
    test_results = tester.run_test_suite(queries)

    # Display summary
    print()
    print("=" * 70)
    print("Test Results Summary")
    print("=" * 70)
    print()
    print(f"Total Queries Tested: {test_results['baseline']['total_queries']}")
    print(f"Average Relevance Score: {test_results['baseline']['avg_relevance']:.2f} / 10")
    print(f"Answer Present Rate: {test_results['baseline']['answer_present_rate']:.1%}")
    print(f"Average Context Quality: {test_results['baseline']['context_quality']:.2f} / 10")
    print(f"Diversity Score: {test_results['baseline']['diversity']:.2f}")
    print()
    print(f"Query Performance:")
    print(f"  Average: {test_results['baseline']['avg_query_time_ms']:.0f}ms")
    print(f"  P50: {test_results['baseline']['p50_query_time_ms']:.0f}ms")
    print(f"  P95: {test_results['baseline']['p95_query_time_ms']:.0f}ms")
    print(f"  Range: {test_results['baseline']['min_query_time_ms']:.0f}ms - {test_results['baseline']['max_query_time_ms']:.0f}ms")
    print()
    print(f"Quality Targets:")
    print(f"  Average Relevance: {'✓' if test_results['baseline']['avg_relevance'] >= 7.0 else '✗'} (target: >=7.0/10.0)")
    print(f"  Answer Present Rate: {'✓' if test_results['baseline']['answer_present_rate'] >= 0.8 else '✗'} (target: >=80%)")
    print(f"  Context Quality: {'✓' if test_results['baseline']['context_quality'] >= 0.6 else '✗'} (target: >=6.0/10.0)")
    print(f"  Diversity: {'✓' if test_results['baseline']['diversity'] >= 0.7 else '✗'} (target: >=70%)")
    print()
    print("=" * 70)

    # Save detailed results
    output_file = "/opt/pi-rag/data/retrieval_quality_test_results.json"
    with open(output_file, "w") as f:
        json.dump(test_results, f, indent=2)

    print(f"\nDetailed results saved to: {output_file}")

    # Save baseline metrics
    baseline_file = "/opt/pi-rag/data/baseline_quality_metrics.json"
    with open(baseline_file, "w") as f:
        json.dump(test_results["baseline"], f, indent=2)

    print(f"Baseline metrics saved to: {baseline_file}")

    # Print individual query results
    print()
    print("=" * 70)
    print("Individual Query Results")
    print("=" * 70)
    print()

    for i, result in enumerate(test_results["results"]):
        print(f"\nQuery {i+1}/{len(test_results['results'])}: {result['query']}")
        print(f"Category: {result['category']}")
        print(f"Query Time: {result['query_time_ms']:.0f}ms")
        print(f"Metrics:")
        print(f"  Avg Relevance: {result['metrics']['avg_relevance']:.1f}/10")
        print(f"  Answer Present: {'✓' if result['metrics']['answer_present'] else '✗'}")
        print(f"  Context Quality: {result['metrics']['context_quality']:.1f}/10")
        print()
        print(f"Top 3 Results:")
        for rank, graded in enumerate(result['results']):
            print(f"  #{rank+1} [{graded['relevance']}/10] - {graded['file']}")
            if graded['contains_answer']:
                print(f"        ✓ Contains answer")
            print(f"        Context quality: {graded['context_quality']}/10")

    print()
    print("=" * 70)
    print("Test Suite Complete")
    print("=" * 70)


if __name__ == "__main__":
    main()
