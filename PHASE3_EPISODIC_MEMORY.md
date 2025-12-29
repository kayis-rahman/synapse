# Phase 3: Episodic Memory - Implementation Summary

## Overview

Phase 3 implements **Episodic Memory** - a system for capturing and storing agent experience and learned lessons, distinct from symbolic memory (facts) and semantic memory (knowledge).

**Key Principle**: Episodic memory captures **what the agent learned from acting**, not facts about the world.

---

## Design Philosophy (NON-NEGOTIABLE)

### Memory Type Boundaries

| Memory Type       | Role                    | Example                              |
|-------------------|-------------------------|--------------------------------------|
| **Symbolic**      | Truth / Authority       | "Project uses Go (confidence 0.92)"   |
| **Episodic**      | Strategy / Experience   | "Search filenames first in large repos"|
| **Semantic**      | Knowledge / Content     | "Authentication in Go projects"      |

### Episodic Memory CANNOT:
- ✗ Assert facts
- ✗ Override decisions
- ✗ Change preferences
- ✗ Be treated as authoritative

### Episodic Memory CAN:
- ✓ Provide strategy advice
- ✓ Improve planning
- ✓ Guide behavior
- ✓ Be optional and ignored

---

## What Qualifies as an "Episode"

### Valid Episodes (✔)

```json
{
  "situation": "Large repository with unclear entry point",
  "action": "Searched filenames before reading files",
  "outcome": "Found relevant code quickly",
  "lesson": "For large repos, perform keyword search before file traversal",
  "confidence": 0.85
}
```

Examples:
- ✔ "Searching filenames first helps in large repos"
- ✔ "User prefers concise output over verbose explanations"
- ✔ "Running retrieval before planning caused confusion"

### Invalid Episodes (❌)

```json
{
  "situation": "Project setup",
  "action": "Read README",
  "outcome": "Found project uses Go",
  "lesson": "Project uses Go",  // WRONG: This is a FACT, not a lesson
  "confidence": 0.9
}
```

Examples:
- ❌ "Project uses Go" (symbolic)
- ❌ "User likes JSON" (symbolic)
- ❌ Raw chat logs
- ❌ "User said X, then I did Y" (lesson not abstracted)

---

## Data Model

### Schema (SQLite, Postgres-compatible)

```sql
CREATE TABLE episodic_memory (
    id TEXT PRIMARY KEY,
    situation TEXT NOT NULL,
    action TEXT NOT NULL,
    outcome TEXT NOT NULL,
    lesson TEXT NOT NULL,
    confidence REAL NOT NULL CHECK(confidence >= 0.0 AND confidence <= 1.0),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_lesson ON episodic_memory(lesson);
CREATE INDEX idx_confidence ON episodic_memory(confidence DESC);
CREATE INDEX idx_created_at ON episodic_memory(created_at DESC);
```

### Fields

- `id`: UUID for unique identification
- `situation`: What the agent faced (context)
- `action`: What the agent did
- `outcome`: Result (success/failure)
- `lesson`: Abstracted strategy (what was learned)
- `confidence`: Confidence level (0.0-1.0)
- `created_at`: Timestamp

---

## Episode Write Rules (CRITICAL)

### Episodes MAY be written if:

1. **Non-obvious success**: Task completes successfully in a non-obvious way
2. **Mistake corrected**: A mistake is detected and corrected
3. **Strategy repeats**: Strategy repeats across sessions
4. **Feedback alters behavior**: User feedback alters agent behavior

### Episodes MUST NOT be written for:

1. ✗ Normal success (expected behavior)
2. ✗ Single attempts (no pattern)
3. ✗ Raw failures without insight
4. ✗ Facts (belongs in symbolic memory)
5. ✗ Raw logs (not abstracted)

---

## Implementation Components

### 1. `episodic_store.py` - Storage Layer

**Purpose**: SQLite storage for episodic memory.

**Key Features**:
- Postgres-compatible schema
- Episode validation before storage
- Conflict resolution (highest confidence)
- Cleanup for old, low-confidence episodes
- Full CRUD operations

**Key Classes**:

```python
from rag.episodic_store import Episode, EpisodicStore

# Create episode
episode = Episode(
    situation="Large repository with unclear entry point",
    action="Searched filenames before reading files",
    outcome="Found relevant code quickly",
    lesson="For large repos, perform keyword search before file traversal",
    confidence=0.85
)

# Validate episode
assert episode.validate()  # Returns False if not abstracted

# Store episode
store = EpisodicStore("./data/episodic.db")
stored = store.store_episode(episode)

# Query episodes
recent_episodes = store.list_recent_episodes(days=30, min_confidence=0.7)
```

### 2. `episode_extractor.py` - LLM-Assisted Extraction

**Purpose**: Extract lessons from agent interactions using LLM.

**Key Features**:
- Strict JSON output validation
- Fact vs. lesson detection
- Lesson abstraction validation
- Empty response if no lesson qualifies
- Confidence threshold filtering

**Key Classes**:

```python
from rag.episode_extractor import EpisodeExtractor
from rag.model_manager import get_model_manager

# Create LLM function
model_manager = get_model_manager()
llm_func = create_simple_llm_func(model_manager, "chat")

# Create extractor
extractor = EpisodeExtractor(llm_func, min_confidence=0.6)

# Extract episode
episode_data = extractor.extract_episode(
    situation="Large repository with unclear entry point",
    action="Searched filenames before reading files",
    outcome="Found relevant code quickly"
)

if episode_data:
    # Store episode
    episode = Episode(**episode_data)
    store.store_episode(episode)
```

**Extraction Prompt Structure**:

```
You are an episode extractor for an AI agent. Your task is to analyze agent behavior and extract learned lessons.

Input:
- Situation: {situation}
- Action: {action}
- Outcome: {outcome}

Instructions:
1. Determine if this represents a LEARNABLE LESSON (not just a fact, not a log)
2. If NO lesson is learned, return empty JSON: {}
3. If a lesson exists, extract the ABSTRACTED STRATEGY
4. The lesson should be generalizable, not specific to this exact situation
5. Output MUST be valid JSON only (no extra text)

Output format:
{
  "situation": "Brief description of the situation",
  "action": "Brief description of the action taken",
  "outcome": "Brief description of the outcome",
  "lesson": "Abstracted strategy (generalizable)",
  "confidence": 0.85
}
```

### 3. `episodic_reader.py` - Reading for Planning

**Purpose**: Read episodic memory for planning and strategy advice.

**Key Features**:
- Advisory context (not authoritative)
- Relevance-based filtering
- Limited results (prevents bloat)
- Clear disclaimer markers
- Delete and explainable

**Key Classes**:

```python
from rag.episodic_reader import EpisodicReader

# Create reader
reader = EpisodicReader("./data/episodic.db")

# Get advisory context for planning
advisory_context = reader.get_advisory_context(
    task_description="Find relevant code in large repository",
    min_confidence=0.7,
    max_episodes=5
)

print(advisory_context)
# Output:
# PAST AGENT LESSONS (ADVISORY, NON-AUTHORITATIVE):
# • For large repos, perform keyword search before file traversal (confidence: 0.85, learned 5 days ago)
#
# Note: These are lessons from experience, not guaranteed facts. Use your judgment.
```

---

## Using Episodic Memory in Planning

### Planner Prompt Example

```
SYSTEM:
You are a helpful coding assistant.

PAST AGENT LESSONS (ADVISORY, NON-AUTHORITATIVE):
• For large repos, search filenames first.
• User prefers concise output over verbose explanations.

Note: These are lessons from experience, not guaranteed facts. Use your judgment.

PERSISTENT MEMORY (READ-ONLY):
• Project language: Go (confidence 0.92)
• User prefers JSON output (confidence 0.85)

USER REQUEST:
Help me find the authentication code in this large Go project.
```

### Integration with RAG Orchestrator

```python
from rag.orchestrator import RAGOrchestrator
from rag.episodic_reader import EpisodicReader

# Create orchestrator
orchestrator = RAGOrchestrator()

# Create episodic reader
episodic_reader = EpisodicReader("./data/episodic.db")

# Get episodic context
episodic_context = episodic_reader.get_advisory_context("Find authentication code")

# Inject into messages (advisory)
if episodic_context:
    messages[0]["content"] += "\n\n" + episodic_context

# Generate response
response = orchestrator.chat(messages)
```

---

## Safety & Governance Rules

### Episodic Memory MUST NEVER:

1. ✗ Modify symbolic memory
2. ✗ Be injected as fact
3. ✗ Be blindly followed
4. ✗ Override user preferences
5. ✗ Assert factual claims

### Episodic Memory MUST:

1. ✓ Be deletable
2. ✓ Be explainable ("Why do we believe this?")
3. ✓ Be marked as advisory
4. ✓ Have clear disclaimer
5. ✓ Be optional in planning

---

## Testing

### Test Coverage

1. **Episode Validation Tests** (5 tests)
   - Required fields validation
   - Lesson abstraction validation
   - Confidence clamping

2. **Episode Extraction Tests** (4 tests)
   - Valid lesson extraction
   - Fact rejection
   - Insufficient confidence rejection
   - Invalid JSON handling

3. **Episodic Storage Tests** (5 tests)
   - Valid episode storage
   - Invalid episode rejection
   - Episode retrieval
   - Confidence-based queries
   - Cleanup operations

4. **Episodic Reader Tests** (5 tests)
   - Advisory context formatting
   - Disclaimer inclusion
   - Empty context handling
   - Episode limiting
   - Statistics

5. **Safety Tests** (5 tests)
   - No fact storage
   - No chat log storage
   - Advisory marking
   - Deletability
   - Controlled growth

6. **Integration Tests** (3 tests)
   - Full workflow (extraction → storage → planning)
   - Multiple episodes retrieval
   - Stats integration

### Running Tests

```bash
# Run all episodic memory tests
pytest tests/test_episodic_memory.py -v

# Run specific test class
pytest tests/test_episodic_memory.py::TestEpisodeValidation -v

# Run specific test
pytest tests/test_episodic_memory.py::TestEpisodeValidation::test_episode_with_all_required_fields_is_valid -v
```

---

## Configuration

### RAG Config (`configs/rag_config.json`)

```json
{
  "episodic_memory": {
    "enabled": true,
    "db_path": "./data/episodic.db",
    "min_confidence": 0.7,
    "max_episodes_in_context": 5,
    "cleanup_days": 90,
    "cleanup_min_confidence": 0.5
  }
}
```

---

## Example Workflow

### Step 1: Agent Completes Task (Non-obvious success)

```python
# Agent faced: Large repository
# Agent did: Searched filenames first
# Outcome: Found code quickly
```

### Step 2: Extract Episode

```python
from rag.episode_extractor import EpisodeExtractor, create_simple_llm_func
from rag.model_manager import get_model_manager

# Create LLM function
model_manager = get_model_manager()
llm_func = create_simple_llm_func(model_manager, "chat")

# Extract episode
extractor = EpisodeExtractor(llm_func)
episode_data = extractor.extract_episode(
    situation="Large repository with unclear entry point",
    action="Searched filenames before reading files",
    outcome="Found relevant code quickly"
)

# Result:
# {
#   "situation": "Large repository with unclear entry point",
#   "action": "Searched filenames before reading files",
#   "outcome": "Found relevant code quickly",
#   "lesson": "For large repos, perform keyword search before file traversal",
#   "confidence": 0.85
# }
```

### Step 3: Store Episode

```python
from rag.episodic_store import Episode, EpisodicStore

# Create episode object
episode = Episode(**episode_data)

# Store
store = EpisodicStore("./data/episodic.db")
stored = store.store_episode(episode)
```

### Step 4: Use in Future Planning

```python
from rag.episodic_reader import EpisodicReader

# Create reader
reader = EpisodicReader("./data/episodic.db")

# Get advisory context
advisory_context = reader.get_advisory_context(
    "Need to search another large repository"
)

# Inject into planning prompt
planner_prompt = f"""
{advisory_context}

PERSISTENT MEMORY (READ-ONLY):
• Project language: Go (confidence 0.92)

USER REQUEST:
Help me find the API endpoints in this large codebase.
"""
```

---

## Cleanup and Maintenance

### Automatic Cleanup

```python
from rag.episodic_store import EpisodicStore

store = EpisodicStore("./data/episodic.db")

# Remove old, low-confidence episodes
deleted = store.cleanup_old_episodes(
    days=90,              # Older than 90 days
    min_confidence=0.5     # Confidence below 0.5
)

print(f"Deleted {deleted} old episodes")
```

### Manual Episode Deletion

```python
# Delete specific episode
episode_id = "550e8400-e29b-41d4-a716-446655440000"
deleted = store.delete_episode(episode_id)

# Retrieve episode details
episode = store.get_episode(episode_id)
```

---

## Performance Considerations

### Memory Bloat Prevention

1. **Validation**: Episodes must be abstracted (not verbose)
2. **Confidence Threshold**: Low-confidence episodes filtered out
3. **Context Limiting**: Max 5 episodes in planning
4. **Automatic Cleanup**: Old, low-confidence episodes removed
5. **No Auto-Persistence**: Explicit write API only

### Query Optimization

1. **Indexes**: On `lesson`, `confidence`, `created_at`
2. **Keyword Matching**: Fast text-based relevance
3. **Pagination**: `LIMIT` on all queries
4. **Views**: `recent_high_confidence_episodes` for common queries

---

## Key Differences from Symbolic Memory

| Aspect                | Symbolic Memory               | Episodic Memory                  |
|-----------------------|-------------------------------|----------------------------------|
| **Purpose**           | Facts, preferences             | Strategies, experience            |
| **Authority**          | Authoritative                  | Advisory                         |
| **Storage**           | Automatic (Phase 2)           | Explicit write only               |
| **Validation**        | Scope, category, source        | Abstraction, lesson validation    |
| **Conflict Res.**     | Highest confidence wins        | No conflict (separate system)    |
| **Planning Usage**    | Read-only, mandatory          | Advisory, optional               |
| **Example**           | "Project uses Go"             | "Search filenames first in repos"|
| **Can Override**      | Yes (higher confidence)       | No                               |

---

## Troubleshooting

### Issue: Episodes Not Being Stored

**Cause**: Episode validation failing (not abstracted)

**Solution**:
```python
# Check validation
episode = Episode(**episode_data)
print(f"Valid: {episode.validate()}")

# Check lesson length
print(f"Lesson length: {len(episode.lesson)}")  # Should be < 500

# Check lesson vs. situation overlap
if episode.situation.lower() in episode.lesson.lower():
    print("Lesson too similar to situation")
```

### Issue: Too Many Episodes in Context

**Cause**: `max_episodes_in_context` too high

**Solution**:
```python
# Reduce limit
reader = EpisodicReader("./data/episodic.db")
context = reader.get_advisory_context(
    task="...",
    max_episodes=3  # Reduce from 5 to 3
)
```

### Issue: Memory Database Growing Too Large

**Cause**: Old episodes accumulating

**Solution**:
```python
# Run cleanup
store = EpisodicStore("./data/episodic.db")
deleted = store.cleanup_old_episodes(days=60, min_confidence=0.6)

# Or schedule periodic cleanup
import schedule
import time

def cleanup_job():
    deleted = store.cleanup_old_episodes(days=90, min_confidence=0.5)
    print(f"Cleaned up {deleted} episodes")

schedule.every().week.do(cleanup_job)

while True:
    schedule.run_pending()
    time.sleep(3600)  # Check every hour
```

---

## Future Enhancements

1. **Semantic Search**: Use embeddings for better episode relevance
2. **Episode Clustering**: Group similar episodes automatically
3. **Confidence Decay**: Reduce confidence over time
4. **Episode Feedback**: Allow user to upvote/downvote episodes
5. **Episode Expiration**: Auto-expire outdated strategies
6. **Cross-Session Learning**: Share episodes across sessions

---

## Summary

Phase 3: Episodic Memory provides:

✅ **Agent Experience Capture**: Stores lessons learned from acting
✅ **Non-Factual**: Separates strategy from facts
✅ **Advisory Usage**: Clearly marked as non-authoritative
✅ **Controlled Growth**: Validation, limits, and cleanup
✅ **Safety First**: No fact storage, no chat logs, deletable
✅ **Production-Ready**: Comprehensive tests, SQLite schema, documentation

**Key Achievement**: Improves agent planning over time while maintaining clear boundaries between facts (symbolic) and strategies (episodic).

---

## Files Created

1. `rag/episodic_store.py` - Episodic memory storage
2. `rag/episode_extractor.py` - LLM-assisted episode extraction
3. `rag/episodic_reader.py` - Reading episodes for planning
4. `tests/test_episodic_memory.py` - Comprehensive tests
5. `PHASE3_EPISODIC_MEMORY.md` - This documentation

---

## Dependencies

- `sqlite3` (Python stdlib)
- `json` (Python stdlib)
- `uuid` (Python stdlib)
- `datetime` (Python stdlib)
- `typing` (Python stdlib)

No external dependencies required for episodic memory itself.

---

## Version

Phase 3: Episodic Memory - Version 1.0.0

Compatible with Phase 1 (Symbolic Memory) and Phase 2 (Contextual Memory Injection).

---

**End of Phase 3 Implementation**
