"""
Sample queries for testing.

Provides reusable sample queries for unit and integration tests.
"""

# Sample queries organized by type
SAMPLE_QUERIES = {
    # Fact queries - asking about facts, preferences, settings
    "fact_queries": [
        "What is the chunk size?",
        "What is the top-K value?",
        "What embedding model is used?",
        "What is the minimum retrieval score?",
        "What is the maximum token limit?",
    ],

    # Code queries - asking about code implementation
    "code_queries": [
        "How does authentication work?",
        "What functions handle user authentication?",
        "How do I implement OAuth2?",
        "What is the authentication flow?",
        "How do I refresh an access token?",
        "What error handling is available for authentication?",
    ],

    # Concept queries - asking about concepts, architecture
    "concept_queries": [
        "What is the memory hierarchy?",
        "What are the three types of memory?",
        "What is the authority level of each memory type?",
        "How does semantic memory work?",
        "What is episodic memory used for?",
        "What is symbolic memory?",
    ],

    # Multi-hop queries - complex queries requiring multiple steps
    "multi_hop_queries": [
        "How do I add a new model and use it for embedding?",
        "What happens when I query the knowledge base?",
        "How do I ingest code and query it?",
        "What are the steps to set up SYNAPSE?",
    ],

    # Triple-hop queries - very complex queries
    "triple_hop_queries": [
        "What functions handle OAuth2 authentication and how do they work together?",
        "How does memory hierarchy work and what authority levels exist?",
        "What configuration options affect retrieval and how do they interact?",
    ],

    # Ambiguous queries - queries with multiple interpretations
    "ambiguous_queries": [
        "What is auth?",
        "How do I use models?",
        "What is memory?",
        "How do I query?",
    ],

    # Negative queries - queries about what doesn't exist
    "negative_queries": [
        "Is basic authentication supported?",
        "Can I use MongoDB instead of SQLite?",
        "Does SYNAPSE support GraphQL?",
        "Is there a web UI?",
    ],

    # Procedural queries - how-to questions
    "procedural_queries": [
        "How do I install SYNAPSE?",
        "How do I configure the chunk size?",
        "How do I download models?",
        "How do I ingest my codebase?",
        "How do I start the MCP server?",
    ],

    # Comparative queries - comparing concepts
    "comparative_queries": [
        "What's the difference between semantic and episodic memory?",
        "How does symbolic memory differ from episodic memory?",
        "What is better: OAuth2 or basic authentication?",
    ],

    # Troubleshooting queries - help with issues
    "troubleshooting_queries": [
        "Why is authentication failing?",
        "How do I fix token expiration errors?",
        "Why are my queries returning empty results?",
        "How do I debug embedding generation?",
    ],
}

# Expected query categories
QUERY_CATEGORIES = {
    "fact": ["chunk_size", "top_k", "embedding_model", "min_score", "max_tokens"],
    "code": ["authentication", "oauth2", "token", "refresh", "error"],
    "concept": ["memory", "hierarchy", "authority", "semantic", "episodic", "symbolic"],
    "multi_hop": ["model", "embedding", "ingest", "query", "setup"],
    "triple_hop": ["function", "memory", "configuration", "retrieval"],
}

# Query expansion examples
QUERY_EXPANSIONS = {
    "auth": ["authentication", "login", "oauth2", "token"],
    "memory": ["knowledge_base", "storage", "retrieval", "semantic"],
    "model": ["embedding", "chat", "llm", "generation"],
    "query": ["search", "retrieve", "ask", "find"],
    "ingest": ["index", "add", "import", "load"],
}

# Expected answer types for query types
ANSWER_TYPES = {
    "fact_queries": "fact",  # Specific factual answer
    "code_queries": "code",  # Code examples and explanations
    "concept_queries": "explanation",  # Conceptual explanation
    "multi_hop_queries": "procedural",  # Step-by-step procedure
    "triple_hop_queries": "synthesis",  # Synthesized answer
}

# Sample queries with expected memory type
QUERY_MEMORY_TYPE = {
    "What is the chunk size?": "symbolic",
    "How does authentication work?": "semantic",
    "What is the memory hierarchy?": "semantic",
    "What's the best way to implement OAuth2?": "episodic",
}

# Sample queries with expected answer quality
QUERY_QUALITY = {
    "What is the chunk size?": "high",  # Definitive answer
    "How does authentication work?": "medium",  # Requires explanation
    "What functions handle OAuth2?": "high",  # Specific answer
    "What is the best authentication method?": "low",  # Subjective
}

# Queries that should use multiple memory types
MULTI_MEMORY_QUERIES = [
    "How do I configure authentication?",
    "What models should I use for my use case?",
    "How do I optimize query performance?",
]

# Queries that should return no results
NO_RESULT_QUERIES = [
    "How do I use GraphQL?",
    "What is the REST API endpoint?",
    "How do I integrate with Firebase?",
]
