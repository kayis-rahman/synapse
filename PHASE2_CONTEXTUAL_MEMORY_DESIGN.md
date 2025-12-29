# Phase 2: Contextual Memory Injection

## Overview

This document describes the design and implementation of Phase 2: Contextual Memory Injection
for the pi-rag Agentic RAG system.

## Current State Analysis

### Existing Memory Infrastructure (Phase 1)

1. **memory_store.py** (1,449 lines)
   - SQLite-based symbolic memory storage
   - Fully functional CRUD operations
   - Full audit trail via triggers
   - Deterministic operations

2. **memory_reader.py** (592 lines)
   - Query memory facts with filters
   - Basic `inject_into_prompt()` method
   - `build_memory_context()` method

3. **memory_writer.py** (473 lines)
   - LLM-assisted memory extraction
   - Rule-based fallback extraction

4. **orchestrator.py** (357 lines)
   - `_get_memory_context()` method (calls build_memory_context)
   - `_inject_context()` method (injects both RAG and memory)
   - Basic memory integration

### Problems with Current Implementation

1. **No Scope Priority**: Memory is queried without scope hierarchy
   - Doesn't respect session → project → user → org order
   - All scopes treated equally

2. **No Conflict Detection**: Conflicting facts not surfaced
   - Multiple facts with same key aren't detected
   - No transparent resolution

3. **No Category Relevance**: No filtering by category relevance to request
   - All relevant categories injected regardless of context

4. **Mixed Context Injection**: Memory and RAG combined in same context block
   - No clear separation between memory (authoritative) and RAG (advisory)

5. **No "READ-ONLY" Marker**: Injected memory doesn't explicitly state read-only
   - LLM could think it's mutable

## Phase 2 Design

### Architectural Principle

**Memory is authoritative, LLM is advisory.**

The LLM can USE memory but CANNOT:
- Modify memory
- Question memory
- Forget memory
- Override memory

Memory can be INJECTED into LLM prompts but is:

- Read-only during use
- Immutable without explicit user command
- Stored in separate, authoritative database

### Memory Selection Rules

**Only inject memory that meets ALL criteria:**

1. **Relevance**: Category must be relevant to request
   - Coding question → Use decisions, constraints, technical facts
   - Output format question → Use preferences
   - General question → Use high-confidence facts only

2. **Scope Priority**: Apply in priority order until sufficient
   - Session scope first (most specific to current interaction)
   - Project scope (if session insufficient)
   - User scope (if project insufficient)
   - Org scope (if user insufficient)

3. **Confidence Threshold**: Must meet minimum threshold
   - Default: ≥ 0.7 (adjustable)
   - Prevents weak/unreliable facts from influencing decisions

4. **Conflict Resolution**: Detect and handle duplicates
   - Prefer higher confidence
   - Prefer newer timestamp if same confidence
   - Inject both if ambiguous with conflict flag

5. **Non-Conflicting**: Exclude facts that contradict each other
   - Mark low-confidence versions as superseded by high-confidence

### Never Inject

- Irrelevant preferences (don't match request category)
- Low-confidence facts (below threshold)
- Duplicate/stale entries (keep only highest confidence)
- Conflicts where resolution unclear

### Prompt Injection Contract

**Injected Memory Section Must Be:**

```text
PERSISTENT MEMORY (READ-ONLY)
════════════════════════════════

[Formatted memory facts]

Use these facts unless the user explicitly contradicts them.
These facts are authoritative and cannot be modified by AI.

════════════════════════════════
```

### Safety Requirements

1. **No Memory Mutation**: LLM cannot modify memory via prompts
2. **No Forget Commands**: "Forget previous" commands must not clear memory
3. **No Questioning Memory**: LLM cannot ask "what do you remember about X"
4. **No Hallucination Checks**: LLM shouldn't reference facts not injected
5. **No Prompt Override**: User commands to "ignore previous" must not override memory

## Implementation Plan

### New Module: `memory_selector.py`

**Purpose**: Intelligent memory fact selection based on context

**Key Functions**:

1. `select_relevant_facts(user_request, confidence_threshold)`
   - Analyzes user request to determine relevant categories
   - Applies scope priority hierarchy
   - Filters by confidence threshold
   - Returns sorted list of facts

2. `detect_conflicts(facts)`
   - Identifies duplicate keys
   - Returns conflict groups
   - Recommends resolution strategy

3. `filter_by_relevance(facts, request_type)`
   - Maps request types to relevant memory categories
   - Returns only appropriate facts

### Enhanced Module: `memory_formatter.py`

**Purpose**: Format memory facts as immutable, read-only context

**Key Functions**:

1. `format_as_read_only_context(facts)`
   - Creates "PERSISTENT MEMORY (READ-ONLY)" header
   - Formats facts clearly
   - Adds immutability warnings
   - Separates from user query

2. `annotate_conflicts(facts)`
   - Adds conflict flags to ambiguous facts
   - Explains resolution strategy

3. `estimate_context_size(facts)`
   - Calculates character count
   - Warns if exceeding limits (prevents bloat)

### Updated Module: `prompt_builder.py`

**Purpose**: Assemble final prompt with separated sections

**Structure**:
```
[System Instructions]

[PERSISTENT MEMORY (READ-ONLY)]
[Formatted memory facts]

[RELEVANT CONTEXT - RAG]
[Retrieved documents if RAG enabled]

[USER REQUEST]
[Original user query]
```

### Integration with Existing Code

**MemoryReader Enhancements**:
- Add `build_contextual_context()` method for Phase 2
- Keep existing `build_memory_context()` for backward compatibility

**RAGOrchestrator Enhancements**:
- Replace `_get_memory_context()` with Phase 2 aware version
- Update `_inject_context()` to separate memory and RAG
- Add conflict detection and flagging

**Configuration Updates**:
- Add Phase 2 config options to `rag_config.json`:
  - `memory_scope_priority`: ["session", "project", "user", "org"]
  - `memory_confidence_threshold`: 0.7
  - `memory_context_max_chars`: 5000
  - `memory_detect_conflicts`: true
  - `memory_read_only_marker`: true

## Testing Strategy

### Unit Tests

1. Memory Selection Tests
   - Scope priority ordering
   - Confidence threshold enforcement
   - Category relevance filtering
   - Conflict detection

2. Conflict Resolution Tests
   - Higher confidence wins
   - Newer timestamp wins
   - Ambiguous cases get both with flags

3. Context Formatting Tests
   - Read-only marker present
   - Memory separated from user input
   - No mutation instructions in context

4. Safety Tests
   - Prompt override attempts rejected
   - Forget commands don't clear memory
   - Memory cannot be modified via prompts

### Integration Tests

1. End-to-End Workflow
   - User request → Memory selection → Formatting → LLM generation
   - Verify only relevant facts injected
   - Verify read-only contract honored

2. Multi-Scope Scenarios
   - Session + project facts present
   - User requests across different scopes
   - Verify correct priority order

3. Conflict Scenarios
   - Duplicate facts with different values
   - Verify resolution strategy applied
   - Verify user notified of conflicts

## File Structure

```
rag/
├── memory_store.py           (existing, Phase 1)
├── memory_reader.py           (existing, Phase 1)
├── memory_writer.py           (existing, Phase 1)
├── memory_selector.py       (NEW, Phase 2)
├── memory_formatter.py      (NEW, Phase 2)
└── prompt_builder.py          (NEW, Phase 2)

tests/
└── test_phase2_contextual_memory.py  (NEW, Phase 2)
```

## API Changes

### New Endpoints

1. `GET /v1/memory/context`
   - Get memory context for a specific user request
   - Query params: `user_request`, `confidence_threshold`
   - Returns formatted memory context

2. `GET /v1/memory/conflicts`
   - List all detected conflicts
   - Returns: conflicts, facts involved, recommended resolution

3. `POST /v1/memory/select`
   - Manual memory selection interface
   - Body: `{user_request, scope_filter, category_filter}`
   - Returns: selected facts, reason for selection

## Rollout Plan

### Phase 1: Design Document (Current)
✅ Complete

### Phase 2: Implementation (Next)

1. Create `memory_selector.py`
   - Implement scope priority logic
   - Implement category relevance mapping
   - Implement conflict detection
   - Add confidence filtering

2. Create `memory_formatter.py`
   - Implement read-only context formatting
   - Implement conflict annotation
   - Implement context size estimation

3. Create `prompt_builder.py`
   - Implement sectioned prompt assembly
   - Integrate with MemoryReader
   - Test backward compatibility

4. Update `memory_reader.py`
   - Add `build_contextual_context()`
   - Maintain existing methods

5. Update `orchestrator.py`
   - Integrate Phase 2 components
   - Update configuration loading
   - Add conflict detection

6. Update Configuration
   - Add Phase 2 settings to `rag_config.json`
   - Document new configuration options

### Phase 3: Testing (After Implementation)

1. Unit tests for all new modules
2. Integration tests for end-to-end workflow
3. Safety tests for prompt injection resistance
4. Performance tests (context size, selection speed)

### Phase 4: Deployment

1. Update API with new endpoints
2. Migrate configuration files
3. Update documentation
4. Monitor memory injection in production

## Success Criteria

Phase 2 is complete when:

- [ ] Only relevant memory facts are injected
- [ ] Scope priority hierarchy is enforced
- [ ] Confidence thresholds are respected
- [ ] Conflicts are detected and handled
- [ ] Memory is clearly marked as read-only
- [ ] Memory is separated from RAG context
- [ ] Prompt override attempts are prevented
- [ ] All tests pass
- [ ] Documentation is updated

## Risks and Mitigations

### Risk: Breaking Changes
- Mitigation: Maintain backward compatibility with Phase 1
- Keep existing methods, add new ones
- Make Phase 2 opt-in via configuration

### Risk: Performance Impact
- Mitigation: Efficient selection algorithms
- Context size limits to prevent bloat
- Indexing strategy for fast lookups

### Risk: Complex Configuration
- Mitigation: Sensible defaults
- Clear documentation
- Migration guide

## Notes

- This design builds upon Phase 1 (Symbolic Memory)
- Phase 1 memory infrastructure remains unchanged
- Phase 2 adds intelligent selection and safe injection
- No changes to Phase 1's storage or query mechanisms
- Fully backward compatible with existing RAG pipeline
