# Automatic Learning System - Tasks

**Feature ID**: 002-auto-learning
**Created**: January 4, 2026
**Status**: [In Progress]

---

## Progress Summary

- [x] Requirements.md created
- [x] Plan.md created
- [x] Tasks.md created
- [x] Implementation in progress
- [ ] Testing complete
- [ ] Documentation updated
- [ ] Completion status updated

---

## Phase 1: Foundation (1-2 hours) ✅ COMPLETE

### 1.1 Configuration Setup
- [x] Add automatic_learning configuration section to `configs/rag_config.json`
- [x] Create default config with `enabled: false, mode: moderate`
- [x] Test configuration loading
- [x] Validate configuration schema

**Linked to**: Requirement FR-6 (Configuration Support)

### 1.2 Create AutoLearningTracker Module
- [x] Create `rag/auto_learning_tracker.py` file
- [x] Implement `AutoLearningTracker` class
- [x] Implement `track_operation()` method
- [x] Implement `detect_task_completion()` method
- [x] Implement `detect_pattern()` method
- [x] Implement `should_auto_track()` method
- [x] Add operation buffer with 100-operation limit
- [x] Write docstrings and type hints

**Linked to**: Requirement FR-1 (Operation Tracking), FR-2 (Task Completion Detection), FR-5 (Pattern Detection)

### 1.3 Create LearningExtractor Module
- [x] Create `rag/learning_extractor.py` file
- [x] Implement `LearningExtractor` class
- [x] Implement `extract_episode_from_task()` method
- [x] Implement `extract_facts_from_code()` method
- [x] Implement `extract_episode_from_pattern()` method
- [x] Implement rule-based fallback extraction
- [x] Write LLM prompts for extraction
- [x] Add error handling and logging

**Linked to**: Requirement FR-3 (Episode Auto-Extraction), FR-4 (Fact Auto-Extraction)

### 1.4 Unit Tests for Foundation
- [x] Create `tests/test_auto_learning_tracker.py`
- [x] Write tests for `track_operation()`
- [x] Write tests for `detect_task_completion()`
- [x] Write tests for `detect_pattern()`
- [x] Create `tests/test_learning_extractor.py`
- [x] Write tests for `extract_episode_from_task()`
- [x] Write tests for `extract_facts_from_code()`
- [x] Run all unit tests

**Linked to**: Requirement NFR-1 (Performance), NFR-3 (Reliability)

---

## Phase 2: Integration (2-3 hours)

### 2.1 MCP Server Configuration Loading
- [ ] Add `_load_auto_learning_config()` method to `RAGMemoryBackend`
- [ ] Load config from `configs/rag_config.json`
- [ ] Add error handling with sensible defaults
- [ ] Add logging for configuration loading

**Linked to**: Requirement FR-6 (Configuration Support)

### 2.2 Initialize AutoLearningTracker
- [ ] Add `auto_learning` attribute to `RAGMemoryBackend.__init__`
- [ ] Add `_load_auto_learning_config()` method
- [ ] Initialize `AutoLearningTracker` if enabled
- [ ] Initialize `LearningExtractor` if enabled
- [ ] Add `operation_buffer` list to `__init__`
- [ ] Connect to ModelManager for LLM access
- [ ] Test initialization with enabled=false

**Linked to**: Requirement FR-1 (Operation Tracking)

### 2.3 Add Auto-Store Methods
- [ ] Implement `_auto_store_episode()` method
- [ ] Implement `_auto_store_fact()` method
- [ ] Add deduplication checks before storing
- [ ] Store immediately (no batching)
- [ ] Add logging for storage operations

**Linked to**: Requirement FR-3 (Episode Auto-Extraction), NFR-2 (Storage)

### 2.4 Wrap All 7 MCP Tools
- [ ] Wrap `list_projects()` with tracking
- [ ] Wrap `list_sources()` with tracking
- [ ] Wrap `get_context()` with tracking
- [ ] Wrap `search()` with tracking
- [ ] Wrap `ingest_file()` with tracking + fact extraction
- [ ] Wrap `add_fact()` with tracking
- [ ] Wrap `add_episode()` with tracking

**Linked to**: Requirement FR-7 (Manual Override), FR-2 (Task Completion Detection), FR-4 (Fact Auto-Extraction)

### 2.5 Add Manual Override Support
- [ ] Modify all tool wrappers to check `auto_learn` parameter
- [ ] Implement `_should_auto_track()` helper method
- [ ] Test that `auto_learn=false` disables auto-learning
- [ ] Test that manual add_fact/add_episode work regardless

**Linked to**: Requirement FR-7 (Manual Override), US-5 (Manual Override)

---

## Phase 3: Testing (1-2 hours)

### 3.1 Unit Tests Complete
- [ ] Run all unit tests from Phase 1
- [ ] Fix any failing tests
- [ ] Ensure 100% test pass rate
- [ ] Add coverage checks

**Linked to**: Requirement NFR-3 (Reliability)

### 3.2 Integration Tests
- [ ] Create `tests/test_auto_learning_integration.py`
- [ ] Test episode storage after task completion
- [ ] Test fact extraction from code ingestion
- [ ] Test pattern detection (repeated failures)
- [ ] Test manual override (auto_learn=false)
- [ ] Test configuration modes (aggressive/moderate/minimal)
- [ ] Test deduplication logic

**Linked to**: All User Stories (US-1 through US-5)

### 3.3 Performance Tests
- [ ] Measure operation tracking overhead
- [ ] Verify <50ms overhead per tool call
- [ ] Measure episode extraction latency
- [ ] Verify <2s per episode extraction
- [ ] Profile memory usage

**Linked to**: Requirement NFR-1 (Performance)

### 3.4 Error Handling Tests
- [ ] Test LLM extraction failures
- [ ] Test configuration loading errors
- [ ] Test with invalid configuration
- [ ] Test with missing ModelManager
- [ ] Verify graceful degradation

**Linked to**: Requirement NFR-3 (Reliability)

---

## Phase 4: Documentation (30 minutes)

### 4.1 Update AGENTS.md
- [ ] Add "Automatic Learning Mode" section
- [ ] Document automatic learning behavior
- [ ] Document configuration options
- [ ] Document manual override behavior
- [ ] Update memory update mandates section

**Linked to**: Requirement FR-6 (Configuration Support), US-4 (Configuration Control)

### 4.2 Update README.md
- [ ] Add configuration examples
- [ ] Add automatic learning section
- [ ] Document how to enable/disable
- [ ] Document how to use different modes

**Linked to**: Requirement FR-6 (Configuration Support), US-4 (Configuration Control)

### 4.3 Code Comments
- [ ] Add inline comments to AutoLearningTracker
- [ ] Add inline comments to LearningExtractor
- [ ] Document configuration parameters
- [ ] Document detection algorithms

**Linked to**: Requirement NFR-4 (Observability)

### 4.4 Create Troubleshooting Guide
- [ ] Create `docs/troubleshooting-auto-learning.md`
- [ ] Document common issues
- [ ] Document how to debug extraction failures
- [ ] Document how to clear bad episodes/facts

**Linked to**: Requirement NFR-4 (Observability)

---

## Phase 5: Completion & Validation

### 5.1 Validate All Requirements
- [ ] All user stories verified
- [ ] All functional requirements met
- [ ] All non-functional requirements met
- [ ] Configuration schema validated
- [ ] All risks mitigated
- [ ] All success criteria met

**Linked to**: Definition of Done

### 5.2 Update Spec Index
- [ ] Update `docs/specs/index.md` status to [Completed]
- [ ] Add completion date
- [ ] Add final commit hash
- [ ] Mark feature as complete

**Linked to**: SDD Protocol

### 5.3 Git Commit
- [ ] Stage all modified files
- [ ] Create commit with descriptive message
- [ ] Push to origin/main
- [ ] Verify git status shows clean

**Linked to**: SDD Protocol

### 5.4 User Acceptance
- [ ] User confirms "opencode is constantly learning"
- [ ] Episodes are being created automatically
- [ ] Facts are being extracted from code
- [ ] No manual intervention needed for routine work
- [ ] Success metrics met

**Linked to**: Definition of Done

---

## Notes

### Design Decisions
- Episodes stored IMMEDIATELY (no batching) - per user confirmation
- Confidence thresholds: 0.6-0.85 for auto-generated episodes
- Configuration defaults: enabled=false (backward compatible)
- Operation buffer: 100 operations (rolling window)

### Implementation Progress
- Phase 1: [x] COMPLETE - Foundation
- Phase 2: [ ] - Integration
- Phase 3: [ ] - Testing
- Phase 4: [ ] - Documentation
- Phase 5: [ ] - Completion

### Open Issues
- None

### Dependencies
- All new modules depend on existing RAG components
- No external dependencies required

---

**Last Updated**: January 4, 2026
