# Tasks: Universal Multi-Agent Hook-Based Auto-Learning System

**Feature ID**: 004-universal-hook-auto-learning
**Version**: 1.0
**Status**: [In Progress] - Foundation Phase
**Created**: January 4, 2026

---

## Task Breakdown

This task list provides granular checklist for implementing universal hook-based auto-learning system. Tasks are grouped into logical phases following the implementation order:

**ORDERING STRATEGY (User Decision)**:
- **Phase 3.1**: OpenCode Adapter ONLY (Priority 1) - Implement and test
- **WAIT FOR USER FEEDBACK** after Phase 3.1 completes
- **Phase 3.2**: Claude Code Adapter (Priority 2) - After approval
- **Phase 3.3**: Gemini/Aider/Other Adapters (Priority 3) - After approval

**DECISIONS INCORPORATED**:
- **Q1**: Implement ONLY OpenCode first, then wait for feedback, then Claude Code and Gemini
- **Q2**: A - Implement full async (ConversationAnalyzer async, RAG tool async, adapters async)
- **Q3**: A - Implement and test OpenCode adapter fully before other adapters
- **Q4**: A - Use existing chat model (from `rag_config.json`)
- **Q5**: B - Document each adapter as we implement it

---

## Phase 1: Foundation (2-3 hours, 10 tasks)

### 1.1 Create Directory Structure
- [ ] Create `rag/universal_hook.py` for Python interface
- [ ] Create `interfaces/hook-interface.ts` for TypeScript interface
- [ ] Create `rag/adapters/` directory for adapter implementations
- [ ] Create `rag/conversation_analyzer.py` for analyzer
- [ ] Create `interfaces/` directory if not exists

### 1.2 Define Standard Hook Interface (Python)
- [ ] Define `UniversalHookInterface` abstract base class
- [ ] Add `pre_tool_use()` method signature with docstring
- [ ] Add `post_tool_use()` method signature with docstring
- [ ] Add `session_start()` method signature with docstring
- [ ] Add `session_end()` method signature with docstring
- [ ] Add `user_prompt_submit()` method signature with docstring
- [ ] Add type hints for all methods
- [ ] Add detailed docstrings with parameter descriptions

### 1.3 Define Standard Hook Interface (TypeScript)
- [ ] Define `UniversalHookInterface` TypeScript interface
- [ ] Add `preToolUse?` method signature
- [ ] Add `postToolUse?` method signature
- [ ] Add `sessionStart?` method signature
- [ ] Add `sessionEnd?` method signature
- [ ] Add `userPromptSubmit?` method signature
- [ ] Add JSDoc comments for all methods
- [ ] Export interface for use by adapters

### 1.4 Update RAG Configuration Schema
- [ ] Add `universal_hooks` section to `configs/rag_config.json`
- [ ] Add `enabled`, `default_project_id` fields
- [ ] Add `adapters` sub-section with per-adapter configs
- [ ] Add `conversation_analyzer` sub-section
- [ ] Add `performance` section for tuning
- [ ] Add default values for all configuration options
- [ ] Add comments explaining each configuration option

### 1.5 Create Adapter Directory Structure
- [ ] Create `rag/adapters/__init__.py` for Python package
- [ ] Add docstrings to `__init__.py` describing adapters
- [ ] Create placeholder files for future adapters

### 1.6 Create Interface Documentation
- [ ] Add "Standard Hook Interface" section to plan.md (referenced, not create new)
- [ ] Document method contracts and return types
- [ ] Document error handling expectations
- [ ] Provide example implementation template

### 1.7 Create Configuration Guide
- [ ] Document all `universal_hooks` config options
- [ ] Explain per-adapter configuration
- [ ] Provide example configurations for each adapter
- [ ] Explain performance tuning options

### 1.8 Verify Foundation Components
- [ ] Run `python -m py_compile rag/universal_hook.py` to check syntax
- [ ] Run `tsc` on TypeScript interface (if TypeScript available)
- [ ] Verify `rag_config.json` is valid JSON
- [ ] Verify all directories are created correctly

---

## Phase 2: Core Components (3-4 hours, 15 tasks)

### 2.1 Create Conversation Analyzer Class
- [ ] Define `ConversationAnalyzer` class in `rag/conversation_analyzer.py`
- [ ] Add `__init__()` method with model_manager and config parameters
- [ ] Add class-level docstring explaining extraction strategies
- [ ] Add logging configuration
- [ ] Configure async processing flag from config
- [ ] Configure token budget management from config
- [ ] Configure per-day deduplication from config

### 2.2 Implement Heuristic Fact Extraction
- [ ] Create `_extract_facts_heuristic()` method
- [ ] Add regex pattern for API endpoints
- [ ] Add regex pattern for version numbers
- [ ] Add regex pattern for preferences
- [ ] Add regex pattern for decisions
- [ ] Add regex pattern for constraints
- [ ] Return list of fact dictionaries with confidence scores

### 2.3 Implement Heuristic Episode Extraction
- [ ] Create `_extract_episodes_heuristic()` method
- [ ] Add regex pattern for workarounds
- [ ] Add regex pattern for mistakes
- [ ] Add regex pattern for lessons
- [ ] Add regex pattern for recommendations
- [ ] Add regex pattern for successes
- [ ] Return list of episode dictionaries with lesson types

### 2.4 Implement Async LLM Fact Extraction (Q2-A: Full Async)
- [ ] Create `_extract_facts_llm_async()` method with async/await
- [ ] Define extraction prompt template
- [ ] Add async LLM call logic with `await` keyword
- [ ] Parse JSON response from LLM
- [ ] Handle JSON parsing errors gracefully
- [ ] Add error handling for LLM failures with try-except
- [ ] Return list of fact dictionaries or empty list on failure

### 2.5 Implement Async LLM Episode Extraction (Q2-A: Full Async)
- [ ] Create `_extract_episodes_llm_async()` method with async/await
- [ ] Define extraction prompt template
- [ ] Add async LLM call logic with `await` keyword
- [ ] Parse JSON response from LLM
- [ ] Handle JSON parsing errors gracefully
- [ ] Add error handling for LLM failures with try-except
- [ ] Return list of episode dictionaries or empty list on failure

### 2.6 Implement Main Async Conversation Analysis Method (Q2-A: Full Async)
- [ ] Create `analyze_conversation_async()` method with `async def`
- [ ] Call `analyze_user_message()` helper (can be sync wrapper)
- [ ] Call `analyze_agent_response()` helper (can be sync wrapper)
- [ ] Merge results from both analyses
- [ ] Return combined list of learnings
- [ ] Use `asyncio.gather()` for parallel LLM extractions
- [ ] Handle LLM extraction errors with `return_exceptions=True`

### 2.7 Implement User Message Analysis
- [ ] Create `analyze_user_message()` method
- [ ] Call heuristic fact extraction
- [ ] Call heuristic episode extraction
- [ ] Call LLM extraction if enabled (via async)
- [ ] Return list of learnings
- [ ] Add context parameter handling

### 2.8 Implement Agent Response Analysis
- [ ] Create `analyze_agent_response()` method
- [ ] Extract learnings specific to agent responses
- [ ] Detect patterns in agent's explanations
- [ ] Return list of learnings
- [ ] Add context parameter handling

### 2.9 Implement Confidence Scoring
- [ ] Create `score_confidence()` method
- [ ] Score heuristic extractions (0.7-0.9 range)
- [ ] Score LLM extractions (use LLM confidence if provided)
- [ ] Apply context relevance boost
- [ ] Return confidence score (0.0-1.0)

### 2.10 Implement Per-Day Deduplication (Q5-B: Per-Day Strategy)
- [ ] Create `deduplicate()` method with per-day logic
- [ ] Track recent facts in `self.recent_facts` dict (key -> list of timestamps)
- [ ] Track recent episodes in `self.recent_episodes` dict (key -> list of timestamps)
- [ ] Allow 1 fact per day within deduplication window (7 days default)
- [ ] Reinforce learning if added on different days
- [ ] Return deduplicated list of learnings

### 2.11 Implement Fact Extraction Public Method
- [ ] Create `extract_facts()` public method
- [ ] Delegate to heuristic or LLM based on config
- [ ] Add confidence scoring
- [ ] Return filtered list of facts

### 2.12 Implement Episode Extraction Public Method
- [ ] Create `extract_episodes()` public method
- [ ] Delegate to heuristic or LLM based on config
- [ ] Add confidence scoring
- [ ] Return filtered list of episodes

### 2.13 Add Configuration Integration
- [ ] Load `extraction_mode` from config (heuristic/llm/hybrid)
- [ ] Load `use_llm` flag from config
- [ ] Load `min_fact_confidence` from config
- [ ] Load `min_episode_confidence` from config
- [ ] Load deduplication settings from config (mode, window_days)
- [ ] Load token budget settings from config (enabled, limits)

### 2.14 Implement Token Budget Management (Q4: Configurable)
- [ ] Create `_should_skip_llm_due_to_budget()` method
- [ ] Check per-message token limit
- [ ] Check per-session token limit
- [ ] Implement token tracking (`tokens_used_this_session`, `tokens_used_today`)
- [ ] Implement token estimation (`_estimate_tokens()`)
- [ ] Add budget reset mode logic (per_session/per_day/never)

### 2.15 Unit Test Conversation Analyzer
- [ ] Create `tests/test_conversation_analyzer.py`
- [ ] Test heuristic fact extraction with known inputs
- [ ] Test heuristic episode extraction with known inputs
- [ ] Test confidence scoring logic
- [ ] Test per-day deduplication logic
- [ ] Test async LLM extraction with mock model_manager
- [ ] Test error handling (invalid inputs, LLM failures)
- [ ] Verify all tests pass

---

## Phase 3.1: OpenCode Adapter ONLY (Priority 1) - WAIT FOR FEEDBACK (6-8 hours, 20 tasks)

### 3.1.1 Create OpenCode Plugin Structure (Q3-A: Test OpenCode First)
- [ ] Create `.opencode/plugins/` directory if not exists
- [ ] Create `synapse-auto-learning.ts` file
- [ ] Define plugin default object with name, version, description
- [ ] Set priority to 1 (first adapter to implement)
- [ ] Define SynapseConfig interface
- [ ] Define hooks property

### 3.1.2 Define OpenCode Plugin Configuration
- [ ] Define config properties: enabled, priority, analyze_after_tools
- [ ] Define config properties: min_message_length, skip_patterns
- [ ] Define config property: rag_project_id
- [ ] Define config property: async_processing (set to true)
- [ ] Define config property: extraction_mode (set to "hybrid")
- [ ] Add TypeScript types for all config properties

### 3.1.3 Implement tool.execute.before Hook
- [ ] Implement `tool.execute.before` async hook
- [ ] Check config.enabled before processing
- [ ] Check if tool_name is in analyze_after_tools list
- [ ] Validate user_message and lastAgentResponse exist
- [ ] Apply min_message_length filter
- [ ] Apply skip_patterns regex filters
- [ ] Return immediately (non-blocking per Q2-A)

### 3.1.4 Implement RAG Tool Call Helper
- [ ] Implement `callRAGTool()` async helper method
- [ ] Find RAG tool by name in `this.tools`
- [ ] Execute tool with provided arguments
- [ ] Handle tool-not-found error
- [ ] Return result or throw exception
- [ ] Use existing chat model from config (Q4-A)

### 3.1.5 Implement tool.execute.after Hook
- [ ] Implement `tool.execute.after` async hook
- [ ] Track tool execution for session-end analysis
- [ ] Log tool execution for debugging
- [ ] Return immediately (non-blocking)

### 3.1.6 Add TypeScript Types and Interfaces
- [ ] Add JSDoc comments for all methods
- [ ] Define TypeScript interfaces for config, hooks, tool params
- [ ] Export all interfaces for reuse
- [ ] Add proper type annotations throughout

### 3.1.7 Implement Error Handling (Graceful Degradation)
- [ ] Add try-except blocks to all hook methods
- [ ] Log errors without throwing exceptions
- [ ] Never block agent execution (always allow tool to proceed)
- [ ] Return graceful error messages in logs
- [ ] Test with RAG server offline scenario

### 3.1.8 Add Logging Integration
- [ ] Add console.log for analysis results (facts_stored, episodes_stored)
- [ ] Add console.error for errors (don't throw)
- [ ] Add console.debug for detailed hook execution
- [ ] Use `[Synapse]` prefix for all log messages

### 3.1.9 Create OpenCode Integration Documentation (Q5-B: Document As We Go)
- [ ] Create `.opencode/plugins/README.md`
- [ ] Document installation steps
- [ ] Document configuration options
- [ ] Provide usage examples
- [ ] Document troubleshooting steps

### 3.1.10 Test OpenCode Plugin Locally
- [ ] Compile TypeScript plugin (`tsc` if available)
- [ ] Verify plugin structure is valid
- [ ] Test configuration loading
- [ ] Test skip pattern matching
- [ ] Test hook execution flow

### 3.1.11 Integration Test: OpenCode Plugin + RAG MCP Tool
- [ ] Test OpenCode plugin calls `rag.analyze_conversation` tool
- [ ] Test with sample user message and agent response
- [ ] Verify tool returns correct JSON structure
- [ ] Verify facts and episodes are stored correctly
- [ ] Test error handling (invalid parameters)

### 3.1.12 Performance Test: Async Processing (Q2-A)
- [ ] Benchmark hook execution time (target: <50ms)
- [ ] Benchmark heuristic extraction (target: <10ms)
- [ ] Verify non-blocking behavior (doesn't delay agent)
- [ ] Test with 100+ consecutive tool calls
- [ ] Verify no memory leaks

### 3.1.13 Accuracy Test: Extraction Quality
- [ ] Test fact extraction with known fact patterns
- [ ] Test episode extraction with known episode patterns
- [ ] Calculate fact precision (target: >75%)
- [ ] Calculate episode precision (target: >70%)
- [ ] Test confidence filtering effectiveness

### 3.1.14 Test Per-Day Deduplication (Q5-B)
- [ ] Test same fact added twice in same day (should skip second)
- [ ] Test same fact added on different days (should allow both)
- [ ] Test deduplication window boundary (7 days default)
- [ ] Verify fact reinforcement works correctly
- [ ] Test episode deduplication similarly

### 3.1.15 Test Token Budget (Q4)
- [ ] Test token budget enforcement when enabled
- [ ] Test token tracking across session
- [ ] Test per-message limit enforcement
- [ ] Test per-session limit enforcement
- [ ] Verify LLM calls are skipped when budget exceeded

### 3.1.16 Integration Test: End-to-End Flow
- [ ] Test full flow: OpenCode plugin → RAG tool → analyzer → storage
- [ ] Test with actual OpenCode instance (if available)
- [ ] Test error propagation through all layers
- [ ] Test graceful degradation when RAG server unavailable
- [ ] Verify system works end-to-end without blocking

### 3.1.17 Test Configuration Options
- [ ] Test with `extraction_mode: "heuristic"` (LLM disabled)
- [ ] Test with `extraction_mode: "llm"` (heuristics disabled)
- [ ] Test with `extraction_mode: "hybrid"` (default, both enabled)
- [ ] Test token budget enabled/disabled
- [ ] Test async_processing enabled/disabled

### 3.1.18 User Acceptance Testing
- [ ] Test with real user workflow (simulate actual usage)
- [ ] Verify extraction quality meets user expectations
- [ ] Verify no false positives (incorrect facts/episodes)
- [ ] Verify no false negatives (missed learnings)
- [ ] Gather feedback for improvements

### 3.1.19 Performance Benchmarking
- [ ] Measure average hook execution time
- [ ] Measure LLM call latency (when used)
- [ ] Measure memory usage over time
- [ ] Create performance baseline report
- [ ] Verify targets met (<50ms hooks, <100ms LLM)

### 3.1.20 Update Documentation (Q5-B: Final Docs)
- [ ] Update README.md with final configuration values
- [ ] Add known issues and solutions
- [ ] Add performance tuning guide
- [ ] Add screenshots or examples if applicable
- [ ] Document all test results and findings

---

### **STOP POINT - WAIT FOR USER FEEDBACK**

**After completing Phase 3.1, STOP and await user feedback before continuing.**

- [ ] Prepare Phase 3.1 completion report
- [ ] Document all test results
- [ ] List any issues or concerns
- [ ] Gather user feedback on OpenCode adapter
- [ ] **WAIT for approval to proceed to Phase 3.2**

---

## Phase 3.2: Claude Code Adapter (Priority 2) - AFTER APPROVAL (6-8 hours, 20 tasks)

### 3.2.1 Create Claude Code Hook Adapter Class
- [ ] Create `ClaudeCodeHookAdapter` class in `rag/adapters/claude_code_hook.py`
- [ ] Implement `__init__()` with project_id parameter
- [ ] Add conversation buffer (list for storing turns)
- [ ] Add type hints and docstrings

### 3.2.2 Implement Claude Code Pre-Tool Hook
- [ ] Implement `pre_tool_use()` method
- [ ] Append conversation to buffer (user_message, agent_response, tool_name, args)
- [ ] Check if tool_name is in `analyze_after_tools` list
- [ ] Return `{"analyze_now": True}` if analysis should trigger
- [ ] Return `None` otherwise
- [ ] Add logging for hook execution

### 3.2.3 Implement Claude Code Post-Tool Hook
- [ ] Implement `post_tool_use()` method
- [ ] Update buffered conversation with tool result
- [ ] Return `{"analyze": False}` to defer analysis
- [ ] Add logging for hook execution

### 3.2.4 Implement Claude Code Session Hooks
- [ ] Implement `session_start()` method
- [ ] Initialize empty conversation buffer
- [ ] Initialize ConversationAnalyzer instance
- [ ] Implement `session_end()` method
- [ ] Analyze all buffered conversations at session end
- [ ] Clear buffer after analysis
- [ ] Return analysis statistics

### 3.2.5 Add Claude Code CLI Entry Point
- [ ] Add `main()` function with argparse
- [ ] Add command subparser (pre_tool_use, post_tool_use, session_start, session_end)
- [ ] Add project_id argument
- [ ] Add user_message argument
- [ ] Add tool_name argument
- [ ] Add arguments argument (JSON)
- [ ] Add result argument (JSON)
- [ ] Add agent_response argument
- [ ] Add analyze_all flag

### 3.2.6 Add Claude Code Command Routing
- [ ] Route pre_tool_use command to adapter method
- [ ] Route post_tool_use command to adapter method
- [ ] Route session_start command to adapter method
- [ ] Route session_end command to adapter method
- [ ] Print results as JSON to stdout
- [ ] Add error handling for invalid commands

### 3.2.7 Test Claude Code Adapter Unit Tests
- [ ] Test pre_tool_use with valid input
- [ ] Test post_tool_use with valid input
- [ ] Test session_start and session_end
- [ ] Test conversation buffering
- [ ] Test CLI entry point with all commands
- [ ] Verify JSON output format

### 3.2.8 Create Claude Code Integration Documentation (Q5-B)
- [ ] Create docs/CLAUDE_CODE_INTEGRATION.md
- [ ] Document `.claude/settings.json` configuration
- [ ] Document available hooks (PreToolUse, PostToolUse, SessionEnd)
- [ ] Provide configuration examples
- [ ] Add troubleshooting section

### 3.2.9 Test Claude Code Integration
- [ ] Test with sample `.claude/settings.json`
- [ ] Verify hooks are triggered correctly
- [ ] Test conversation analysis at session end
- [ ] Test error handling
- [ ] Verify no crashes occur

### 3.2.10 Performance Test: Claude Code Adapter
- [ ] Benchmark hook execution time
- [ ] Test with 100+ consecutive tool calls
- [ ] Verify no memory leaks
- [ ] Measure CLI overhead
- [ ] Verify targets met

### 3.2.11 Create Claude Code Setup Script
- [ ] Create setup script for easy configuration
- [ ] Add installation instructions
- [ ] Add validation script
- [ ] Test setup script
- [ ] Document setup process

### 3.2.12 Integration Test: Claude Code + RAG
- [ ] Test full flow: Claude Code hooks → adapter → RAG tool → storage
- [ ] Test with actual Claude Code (if available)
- [ ] Verify end-to-end functionality
- [ ] Test error handling
- [ ] Verify graceful degradation

### 3.2.13 Test Multi-Session Scenario
- [ ] Test with multiple Claude Code sessions
- [ ] Verify deduplication works across sessions
- [ ] Verify token budget resets correctly
- [ ] Test session start/end hooks
- [ ] Verify buffer management

### 3.2.14 Test Edge Cases
- [ ] Test with empty user messages
- [ ] Test with very long messages
- [ ] Test with special characters
- [ ] Test with malformed tool results
- [ ] Verify robust handling

### 3.2.15 Documentation: Advanced Usage
- [ ] Document advanced configuration options
- [ ] Document performance tuning
- [ ] Document common issues and solutions
- [ ] Add FAQ section
- [ ] Provide examples for various use cases

### 3.2.16 Create Test Suite for Claude Code
- [ ] Create comprehensive test suite
- [ ] Add unit tests for all methods
- [ ] Add integration tests
- [ ] Add performance tests
- [ ] Verify all tests pass

### 3.2.17 Verify Compliance with AGENTS.md
- [ ] Verify adapter follows SDD protocol
- [ ] Verify RAG STRICT MANDATE compliance
- [ ] Verify memory feeding is automatic
- [ ] Verify configuration options documented
- [ ] Verify error handling is graceful

### 3.2.18 Create Migration Guide
- [ ] Document upgrade path from manual to automatic learning
- [ ] Provide migration checklist
- [ ] Document backward compatibility
- [ ] Add rollback instructions if needed
- [ ] Test migration process

### 3.2.19 Final Validation
- [ ] Run all unit tests
- [ ] Run all integration tests
- [ ] Verify all adapters work correctly
- [ ] Verify RAG MCP server integration
- [ ] Verify documentation is complete

### 3.2.20 Prepare for Feedback
- [ ] Prepare Phase 3.2 completion report
- [ ] Document all test results
- [ ] List any issues or concerns
- [ ] Gather user feedback
- [ ] **WAIT for approval to proceed to Phase 3.3**

---

### **STOP POINT - WAIT FOR USER FEEDBACK**

**After completing Phase 3.2, STOP and await user feedback before continuing.**

- [ ] Prepare Phase 3.2 completion report
- [ ] Document all test results
- [ ] List any issues or concerns
- [ ] Gather user feedback on Claude Code adapter
- [ ] **WAIT for approval to proceed to Phase 3.3**

---

## Phase 3.3: Other Adapters - Gemini, Aider, etc. (Priority 3) - AFTER APPROVAL (8-10 hours, 20 tasks)

### 3.3.1 Assess Adapter Requirements
- [ ] Research Gemini CLI hook system
- [ ] Research Aider hook system
- [ ] Research other agents (Goose, GPT-engineer, Amazon Q, Grok, Cline, Plandex)
- [ ] Document hook system differences
- [ ] Identify common patterns

### 3.3.2 Create Generic Bash Adapter
- [ ] Extend generic bash adapter for multiple agents
- [ ] Add agent-specific configuration options
- [ ] Add tool filtering per agent
- [ ] Test with Aider
- [ ] Test with Goose
- [ ] Test with other bash-based agents

### 3.3.3 Create Gemini CLI Adapter
- [ ] Create Gemini-specific adapter if needed
- [ ] Implement Gemini hook integration
- [ ] Test with Gemini CLI
- [ ] Document Gemini-specific configuration
- [ ] Add troubleshooting steps

### 3.3.4 Create REST API Adapter Enhancement
- [ ] Enhance REST adapter for multiple remote agents
- [ ] Add authentication support
- [ ] Add rate limiting
- [ ] Test with various clients
- [ ] Document REST API usage

### 3.3.5 Cross-Adapter Testing
- [ ] Test all adapters with same test suite
- [ ] Verify consistent behavior across adapters
- [ ] Verify configuration handling
- [ ] Verify error handling
- [ ] Document adapter-specific issues

### 3.3.6 Performance Comparison
- [ ] Benchmark all adapters
- [ ] Compare performance metrics
- [ ] Identify bottlenecks
- [ ] Optimize slow adapters
- [ ] Document performance characteristics

### 3.3.7 Documentation: All Adapters
- [ ] Create comprehensive adapter guide
- [ ] Document each adapter's specific features
- [ ] Provide comparison matrix
- [ ] Add adapter selection guide
- [ ] Add migration guide between adapters

### 3.3.8 Create Adapter Template
- [ ] Create template for new adapters
- [ ] Document adapter creation process
- [ ] Provide step-by-step guide
- [ ] Include testing checklist
- [ ] Include documentation checklist

### 3.3.9 Test Multi-Agent Scenario
- [ ] Test with multiple agents running simultaneously
- [ ] Verify RAG server handles concurrent requests
- [ ] Verify deduplication works across agents
- [ ] Test resource contention
- [ ] Document scalability limits

### 3.3.10 Security Audit
- [ ] Review code for security issues
- [ ] Check for injection vulnerabilities
- [ ] Verify proper validation
- [ ] Review logging for sensitive data
- [ ] Address any security concerns

### 3.3.11 Documentation: Troubleshooting
- [ ] Create troubleshooting guide for all adapters
- [ ] Document common issues
- [ ] Provide solutions
- [ ] Add debugging guide
- [ ] Add log interpretation guide

### 3.3.12 Test Real-World Scenarios
- [ ] Test with actual user workflows
- [ ] Test with complex conversations
- [ ] Test with edge cases
- [ ] Test with error scenarios
- [ ] Gather real-world feedback

### 3.3.13 Performance Optimization
- [ ] Optimize slow adapters based on benchmarks
- [ ] Reduce token usage where possible
- [ ] Improve caching strategies
- [ ] Optimize regex patterns
- [ ] Verify optimization results

### 3.3.14 Final Integration Testing
- [ ] Test all adapters with RAG MCP server
- [ ] Test with actual agents (OpenCode, Claude Code, etc.)
- [ ] Verify end-to-end functionality
- [ ] Test error handling
- [ ] Verify graceful degradation

### 3.3.15 Documentation: Completion
- [ ] Finalize all adapter documentation
- [ ] Create getting started guide
- [ ] Create reference manual
- [ ] Create API documentation
- [ ] Add examples and tutorials

### 3.3.16 User Acceptance Testing
- [ ] Conduct user acceptance testing
- [ ] Gather feedback from all adapter users
- [ ] Address critical issues
- [ ] Make final adjustments
- [ ] Prepare for release

### 3.3.17 Performance Validation
- [ ] Validate performance meets targets
- [ ] Verify no blocking operations
- [ ] Verify minimal overhead
- [ ] Verify scalability
- [ ] Document performance metrics

### 3.3.18 Code Review
- [ ] Conduct peer code review
- [ ] Address review comments
- [ ] Refactor if needed
- [ ] Ensure code quality
- [ ] Finalize code

### 3.3.19 Release Preparation
- [ ] Tag release version
- [ ] Create release notes
- [ ] Prepare changelog
- [ ] Update version numbers
- [ ] Verify all components ready

### 3.3.20 Final Documentation
- [ ] Complete all documentation
- [ ] Update index files
- [ ] Create final summary
- [ ] Prepare announcement
- [ ] Archive development artifacts

---

## Phase 4: RAG MCP Server Integration (1-2 hours, 5 tasks)

### 4.1 Add RAG MCP Tool: rag.analyze_conversation
- [ ] Create `handle_analyze_conversation()` async function
- [ ] Add @server.call_tool() decorator
- [ ] Define function parameters with type hints
- [ ] Add comprehensive docstring with examples
- [ ] Import ConversationAnalyzer

### 4.2 Implement Tool Logic: Async Processing (Q2-A)
- [ ] Initialize ConversationAnalyzer with config
- [ ] Call analyze_conversation_async (not sync)
- [ ] Filter learnings by confidence thresholds
- [ ] Store facts via handle_add_fact (async)
- [ ] Store episodes via handle_add_episode (async)
- [ ] Use asyncio.gather() for parallel storage

### 4.3 Add Tool Configuration Support
- [ ] Extract conversation_analyzer config from auto_learning_config
- [ ] Apply min_fact_confidence and min_episode_confidence
- [ ] Respect auto_store and return_only flags
- [ ] Handle context parameter
- [ ] Support extraction_mode parameter

### 4.4 Register Tool with Server
- [ ] Add Tool object to tools list in rag_server.py
- [ ] Set tool name to "rag.analyze_conversation"
- [ ] Set tool description with agent compatibility info
- [ ] Define inputSchema (project_id, user_message, agent_response, context, auto_store, return_only)
- [ ] Mark required parameters

### 4.5 Test Tool Integration
- [ ] Test tool with auto_store=True
- [ ] Test tool with auto_store=False
- [ ] Test tool with return_only=True
- [ ] Test with confidence filtering
- [ ] Verify tool returns correct JSON structure
- [ ] Test error handling (invalid parameters)

---

## Phase 5: Documentation (2-3 hours, 8 tasks)

### 5.1 Create Universal Hook Integration Guide
- [ ] Create `docs/UNIVERSAL_HOOK_INTEGRATION.md`
- [ ] Add overview section explaining architecture
- [ ] Add supported agents list with checkmarks
- [ ] Add quick start section
- [ ] Add architecture diagram

### 5.2 Document OpenCode Integration (Q5-B: Completed)
- [ ] Add OpenCode setup instructions (already created in Phase 3.1.9)
- [ ] Provide `.opencode/plugins/synapse-auto-learning.ts` configuration example
- [ ] Document available hooks (tool.execute.before, tool.execute.after)
- [ ] Add troubleshooting section for OpenCode
- [ ] Link to OpenCode README.md

### 5.3 Document Claude Code Integration (Q5-B)
- [ ] Add Claude Code setup instructions
- [ ] Provide `.claude/settings.json` configuration example
- [ ] Document available hooks (PreToolUse, PostToolUse, SessionEnd)
- [ ] Add troubleshooting section for Claude Code
- [ ] Link to CLAUDE_CODE_INTEGRATION.md

### 5.4 Document Other Agents (Bash/REST)
- [ ] Add setup instructions for Aider
- [ ] Add setup instructions for Gemini CLI
- [ ] Add setup instructions for Goose
- [ ] Add setup instructions for GPT-engineer
- [ ] Add setup instructions for Amazon Q CLI
- [ ] Add setup instructions for Grok CLI
- [ ] Add setup instructions for Cline
- [ ] Add setup instructions for Plandex
- [ ] Provide generic bash hook config examples

### 5.5 Document REST API Integration
- [ ] Add REST API setup instructions
- [ ] Document all available endpoints
- [ ] Provide curl examples for each endpoint
- [ ] Add authentication/security notes
- [ ] Document data formats

### 5.6 Document Configuration Options
- [ ] Document all `universal_hooks` config options
- [ ] Document extraction modes (heuristic/llm/hybrid)
- [ ] Document confidence thresholds
- [ ] Document deduplication settings
- [ ] Document performance tuning options
- [ ] Document token budget settings

### 5.7 Create Troubleshooting Guide
- [ ] Add common issues and solutions
- [ ] Add hook not firing troubleshooting
- [ ] Add extraction accuracy troubleshooting
- [ ] Add performance troubleshooting
- [ ] Add adapter-specific troubleshooting
- [ ] Add RAG server connectivity troubleshooting

### 5.8 Create Adapter Development Guide
- [ ] Add "Creating a Custom Adapter" section
- [ ] Document UniversalHookInterface contract
- [ ] Provide step-by-step adapter creation guide
- [ ] Provide example custom adapter template
- [ ] Document testing requirements for new adapters
- [ ] Document submission process

---

## Phase 6: Testing (2-3 hours, 10 tasks)

### 6.1 Create Unit Test Suite
- [ ] Create `tests/integration/test_universal_hooks.py`
- [ ] Add imports for all adapters and components
- [ ] Create test fixtures for mock RAG calls
- [ ] Create test fixtures for mock conversations

### 6.2 Test Conversation Analyzer
- [ ] Test heuristic fact extraction accuracy (test with known facts)
- [ ] Test heuristic episode extraction accuracy (test with known episodes)
- [ ] Test confidence scoring logic
- [ ] Test per-day deduplication logic (exact duplicates, per-day reinforcement)
- [ ] Test LLM extraction with mock model_manager (Q4-A)
- [ ] Test hybrid extraction mode (heuristics + LLM)
- [ ] Test error handling (invalid inputs, LLM failures)

### 6.3 Test OpenCode Adapter (Q3-A: Tested First)
- [ ] Test TypeScript plugin structure (already tested in Phase 3.1)
- [ ] Test tool.execute.before hook execution
- [ ] Test configuration loading
- [ ] Test RAG tool integration
- [ ] Test skip patterns and filters
- [ ] Verify TypeScript compiles

### 6.4 Test Claude Code Adapter
- [ ] Test pre_tool_use hook execution
- [ ] Test post_tool_use hook execution
- [ ] Test session_start and session_end
- [ ] Test conversation buffering
- [ ] Test CLI entry point with all commands
- [ ] Verify JSON output format

### 6.5 Test Other Adapters (Bash/REST/Gemini)
- [ ] Test CLI entry point for bash adapter
- [ ] Test conversation file buffering
- [ ] Test session_end analysis
- [ ] Test error handling with invalid inputs
- [ ] Test file permissions and cleanup
- [ ] Test REST API endpoints

### 6.6 Test Integration End-to-End
- [ ] Test full flow: hook → adapter → RAG tool → analyzer → storage
- [ ] Test with actual RAG MCP server (if available)
- [ ] Test error propagation through all layers
- [ ] Test graceful degradation when RAG server unavailable
- [ ] Test with multiple concurrent requests
- [ ] Verify no blocking operations

### 6.7 Performance Testing (Q2-A: Async)
- [ ] Benchmark heuristic extraction time (target: <10ms)
- [ ] Benchmark LLM extraction time (target: <100ms)
- [ ] Benchmark hook execution time (target: <50ms)
- [ ] Test with 100+ consecutive conversations
- [ ] Verify no memory leaks
- [ ] Verify async processing is non-blocking

### 6.8 Accuracy Testing
- [ ] Test fact extraction precision with known dataset (target: >75%)
- [ ] Test episode extraction precision with known dataset (target: >70%)
- [ ] Calculate fact precision
- [ ] Calculate episode precision
- [ ] Test confidence filtering effectiveness
- [ ] Document accuracy results

### 6.9 Compatibility Testing
- [ ] Test with Python 3.8+
- [ ] Test with TypeScript (if available)
- [ ] Test with no LLM model manager (fallback to heuristics)
- [ ] Test with minimal configuration (sensible defaults)
- [ ] Test with RAG server offline (graceful degradation)
- [ ] Test across different operating systems

### 6.10 Test Coverage Validation
- [ ] Run pytest with coverage report
- [ ] Verify unit test coverage >80% for all adapters
- [ ] Verify integration tests cover all scenarios
- [ ] Check for uncovered code paths
- [ ] Add tests for uncovered paths
- [ ] Document coverage metrics

---

## Phase 7: Completion & Validation (1 hour, 4 tasks)

### 7.1 Update Central Index
- [ ] Update `docs/specs/index.md` with feature 004 entry
- [ ] Set status to "[In Progress]"
- [ ] Add completion date placeholder (TBD)
- [ ] Verify index format matches existing entries

### 7.2 Final Code Review
- [ ] Review all adapter implementations
- [ ] Review conversation analyzer code
- [ ] Review RAG MCP tool implementation
- [ ] Check for consistency across all components
- [ ] Verify error handling is comprehensive

### 7.3 Update AGENTS.md (if needed)
- [ ] Update AGENTS.md if workflow changes are needed
- [ ] Document new RAG tool usage
- [ ] Add reference to universal hook integration
- [ ] Update RAG STRICT MANDATE if needed
- [ ] Verify all documentation is consistent

### 7.4 Final Validation
- [ ] Run all unit tests (`pytest tests/`)
- [ ] Run integration tests (`pytest tests/integration/`)
- [ ] Verify all adapters load without errors
- [ ] Verify RAG server starts without errors
- [ ] Test with at least one real agent (OpenCode or Claude Code)
- [ ] Document final commit hash
- [ ] Prepare release notes

---

## Task Statistics

- **Total Tasks**: 173
- **Total Phases**: 7
- **Estimated Time**: 21-28 hours
- **Current Progress**: 0/173 (0%)

---

## Notes

**IMPLEMENTATION ORDER (User Decision Q1)**:
- **Phase 3.1 ONLY**: Implement OpenCode adapter, test thoroughly, document
- **STOP & WAIT**: Gather user feedback on OpenCode implementation
- **Phase 3.2**: After approval, implement Claude Code adapter
- **Phase 3.3**: After approval, implement other adapters (Gemini, Aider, etc.)

**DECISIONS INCORPORATED**:
- **Q1**: OpenCode ONLY first, wait for feedback, then Claude Code and Gemini
- **Q2-A**: Implement full async (ConversationAnalyzer async, RAG tool async, adapters async)
- **Q3-A**: Implement and test OpenCode adapter fully first
- **Q4-A**: Use existing chat model (from `rag_config.json`)
- **Q5-B**: Document each adapter as we implement it

**READY TO START**: Phase 3.1 (OpenCode Adapter ONLY) after final approval
