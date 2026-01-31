# Feature 012 - CLI & Ingestion Bug Fixes: Requirements

**Feature ID**: 012-cli-ingestion-bug-fixes  
**Status**: [In Progress]  
**Created**: January 31, 2026  
**Objective**: Fix 7 bugs identified during Feature 010 validation

---

## 📋 Overview

This feature addresses bugs discovered during the Fresh Installation Validation (Feature 010) to make the SYNAPSE CLI fully functional and fix the critical ingestion persistence issue.

**Total Bugs to Fix**: 7  
**Estimated Timeline**: 16-19 hours (54 tasks across 6 phases)

---

## 🎯 User Stories

### US-001: Config JSON Output
**As a** DevOps engineer  
**I want** to get configuration as JSON  
**So that** I can parse it in automation scripts

**Acceptance Criteria:**
- [ ] `synapse config --json` outputs valid JSON
- [ ] Output includes all configuration sections
- [ ] Exit code 0 on success
- [ ] Exit code 1 on error

### US-002: Models List Completeness  
**As a** System Administrator  
**I want** to see all installed models  
**So that** I can verify the setup is complete

**Acceptance Criteria:**
- [ ] `synapse models list` shows all models
- [ ] Includes BGE-M3 and other embedding models
- [ ] Shows model file paths and sizes
- [ ] Correctly identifies missing models

### US-003: Functional Ingest Command
**As a** Knowledge Engineer  
**I want** to ingest files into the knowledge base  
**So that** I can build a searchable knowledge base

**Acceptance Criteria:**
- [ ] `synapse ingest <path>` ingests files
- [ ] Supports single files and directories
- [ ] Shows progress during ingestion
- [ ] Reports number of documents/chunks created
- [ ] Exit code 0 on success

### US-004: Functional Query Command
**As a** AI Agent  
**I want** to query the knowledge base  
**So that** I can retrieve relevant information

**Acceptance Criteria:**
- [ ] `synapse query "search text"` returns results
- [ ] Returns relevant documents from knowledge base
- [ ] Shows source attribution
- [ ] Exit code 0 on success

### US-005: Ingestion Data Persistence
**As a** Data Engineer  
**I want** ingested data to persist across restarts  
**So that** the knowledge base is reliable and permanent

**Acceptance Criteria:**
- [ ] `bulk_ingest` saves data to storage
- [ ] `list_sources` returns ingested documents (> 50)
- [ ] Data survives MCP server restart
- [ ] No "0 sources" after successful ingestion

### US-006: CLI Help Completeness
**As a** New User  
**I want** complete help for all CLI commands  
**So that** I can understand how to use SYNAPSE

**Acceptance Criteria:**
- [ ] All commands have `--help` text
- [ ] Help includes examples
- [ ] Help shows all available options
- [ ] Error messages are helpful

---

## 🐛 Bugs to Fix

### Critical Bugs (Must Fix)

#### BUG-INGEST-01: Ingestion Persistence Failure
**Severity**: HIGH  
**Impact**: Knowledge base doesn't work  
**Issue**: bulk_ingest completes but data not persisted  
**Root Cause**: Storage backend not committing data  
**Fix**: Add explicit persist/commit operation

#### BUG-007: Ingest Command Not Implemented
**Severity**: MEDIUM  
**Impact**: Cannot ingest files via CLI  
**Issue**: Returns stub message "not yet implemented"  
**Fix**: Implement full ingest command

#### BUG-008: Query Command Not Implemented  
**Severity**: MEDIUM  
**Impact**: Cannot query knowledge base via CLI  
**Issue**: Returns stub message "not yet implemented"  
**Fix**: Implement full query command

### Medium Bugs (Should Fix)

#### BUG-006: Models List Incomplete
**Severity**: MEDIUM  
**Impact**: Cannot verify model installation  
**Issue**: Shows incomplete or incorrect model list  
**Fix**: Fix model detection logic

#### BUG-004: Config JSON Output Missing
**Severity**: LOW  
**Impact**: Cannot parse config programmatically  
**Issue**: `--json` flag not implemented  
**Fix**: Add JSON output formatting

#### BUG-005: Config Output Format Issues
**Severity**: LOW  
**Impact**: Poor readability  
**Issue**: Output formatting problems  
**Fix**: Improve formatting

### Low Bugs (Nice to Fix)

#### BUG-009: Config Flags Missing
**Severity**: LOW  
**Impact**: Incomplete CLI functionality  
**Issue**: Various flags not implemented  
**Fix**: Add missing options

---

## 📊 Requirements Summary

### Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-1 | Config JSON output | MUST | Pending |
| FR-2 | Models list completeness | MUST | Pending |
| FR-3 | Ingest command implementation | MUST | Pending |
| FR-4 | Query command implementation | MUST | Pending |
| FR-5 | Ingestion persistence fix | MUST | Pending |
| FR-6 | Help text completeness | SHOULD | Pending |
| FR-7 | Error message quality | SHOULD | Pending |

### Non-Functional Requirements

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR-1 | Pytest coverage | 80%+ | Pending |
| NFR-2 | Ingestion performance | < 5 min | Pending |
| NFR-3 | CLI response time | < 2 sec | Pending |
| NFR-4 | Error handling | Graceful | Pending |

---

## 🔗 Dependencies

### External Dependencies
- **Python 3.13+**: Required for CLI
- **httpx**: For HTTP client in CLI
- **typer**: For CLI framework

### Internal Dependencies
- **MCP Server**: Must be running for ingest/query
- **bulk_ingest.py**: Script to fix
- **RAG Config**: Configuration structure

### Feature Dependencies
- **Feature 010**: Provides bug reports and test cases
- **Feature 011**: Provides CLI command framework

---

## 📦 Scope

### In Scope
- Fix CLI config JSON output (BUG-004)
- Fix CLI config formatting (BUG-005)
- Fix CLI models list (BUG-006)
- Implement CLI ingest command (BUG-007)
- Implement CLI query command (BUG-008)
- Add missing CLI flags (BUG-009)
- Fix bulk_ingest persistence (BUG-INGEST-01)
- Write pytest tests for all fixes
- Update documentation

### Out of Scope
- MCP server modifications (except bulk_ingest)
- RAG algorithm changes
- New feature development
- Performance optimization (beyond requirements)
- Platform-specific fixes (Mac/Linux separate)

---

## ✅ Acceptance Criteria Checklist

### Must Have (Go Live)
- [ ] FR-1: `synapse config --json` works
- [ ] FR-2: `synapse models list` complete
- [ ] FR-3: `synapse ingest` functional
- [ ] FR-4: `synapse query` functional  
- [ ] FR-5: Ingestion persists (> 50 sources)
- [ ] NFR-1: 80%+ pytest coverage
- [ ] All BUG-0XX bugs fixed or documented

### Should Have (Quality)
- [ ] FR-6: Help text complete
- [ ] FR-7: Error messages helpful
- [ ] NFR-2: Ingestion < 5 minutes
- [ ] NFR-3: CLI response < 2 seconds

### Nice to Have (Polish)
- [ ] Colored output
- [ ] Progress bars
- [ ] Batch processing options
- [ ] Configuration validation

---

## 📈 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Bugs fixed | 7/7 | 100% |
| CLI commands working | 12/12 | Manual testing |
| Ingestion persistence | 100% | list_sources > 50 |
| Pytest coverage | 80%+ | pytest --cov |
| Test pass rate | 100% | pytest |

---

## 📅 Timeline

| Phase | Duration | Tasks | Focus |
|-------|----------|-------|-------|
| Phase 1 | 2-3 hrs | 8 | CLI Config Fixes |
| Phase 2 | 2 hrs | 6 | CLI Models Fixes |
| Phase 3 | 3-4 hrs | 10 | CLI Ingest Implementation |
| Phase 4 | 3-4 hrs | 10 | CLI Query Implementation |
| Phase 5 | 4-5 hrs | 12 | BUG-INGEST-01 Fix |
| Phase 6 | 2-3 hrs | 8 | Testing & Validation |
| **Total** | **16-19 hrs** | **54** | |

---

## 📝 Notes

**Constraint**: Follow SDD protocol (AGENTS.md)  
**Testing**: Dual strategy (pytest + manual)  
**Documentation**: Create completion report  
**Branch**: `feature/012-cli-ingestion-bug-fixes`

---

**Created**: January 31, 2026  
**Status**: Ready for Planning  
**Next**: Create plan.md
