# Feature 013 - Getting Started Documentation Refresh

**Feature ID**: 013-getting-started-docs  
**Status**: [Planning]  
**Created**: January 31, 2026  
**Objective**: Update fumadocs getting started section for speed-first experience

---

## 📋 Overview

This feature refreshes the fumadocs getting started section to match actual CLI commands, enabling a "copy-paste → 5 minutes to first query" experience.

**Current State**: Documentation references non-existent CLI commands  
**Target State**: Copy-paste workflow using actual commands (`python -m synapse.cli.main`)

**Estimated Timeline**: ~1.5 hours (10 tasks across 3 phases)

---

## 🎯 User Stories

### US-001: Speed-First Quick Start
**As a** new user  
**I want** to go from zero to my first query in under 5 minutes  
**So that** I can quickly verify SYNAPSE works before diving deeper

**Acceptance Criteria:**
- [ ] One-command install
- [ ] One-command start
- [ ] One-command ingest
- [ ] One-command query
- [ ] Total time: < 5 minutes from git clone to query result

### US-002: OS-Specific Installation
**As a** user on any platform (macOS, Linux, Docker)  
**I want** platform-specific installation instructions  
**So that** I don't encounter OS-specific issues

**Acceptance Criteria:**
- [ ] Tab-based OS selection (macOS, Linux, Docker)
- [ ] Platform-specific prerequisites listed
- [ ] Verified working on each platform

### US-003: Learning on Demand
**As a** user who wants to understand the system  
**I want** expandable details available  
**So that** I can learn while still having fast start option

**Acceptance Criteria:**
- [ ] Quick start section available first
- [ ] Expandable "Learn More" sections
- [ ] Each command explained in expandable detail
- [ ] Links to deeper documentation

---

## 📊 Requirements Summary

### Functional Requirements

| ID | Requirement | Priority | Status |
|----|-------------|----------|--------|
| FR-1 | Tab-based installation (macOS, Linux, Docker) | MUST | Pending |
| FR-2 | Speed-first quick start (< 5 min to query) | MUST | Pending |
| FR-3 | All code blocks use actual CLI commands | MUST | Pending |
| FR-4 | Expandable details for learning | SHOULD | Pending |
| FR-5 | Copy-paste workflow validation | MUST | Pending |

### Non-Functional Requirements

| ID | Requirement | Target | Status |
|----|-------------|--------|--------|
| NFR-1 | Time to first query | < 5 min | Pending |
| NFR-2 | Code block success rate | 100% | Pending |
| NFR-3 | Documentation build | Pass | Pending |

---

## 🔗 Dependencies

### External Dependencies
- **fumadocs**: Documentation framework (already installed)
- **Python 3.8+**: Required for CLI

### Internal Dependencies
- **Feature 007**: CLI commands implemented
- **Current docs**: Files to update

### Feature Dependencies
- None (standalone documentation update)

---

## 📦 Scope

### In Scope
- Update `docs/app/md/getting-started/introduction.md`
- Update `docs/app/md/getting-started/installation.md`
- Update `docs/app/md/getting-started/quick-start.md`
- Demote `docs/app/md/getting-started/configuration.md` to reference
- Tab-based OS selection
- Copy-paste validation

### Out of Scope
- Changes to CLI commands
- Changes to architecture documentation
- Changes to API reference
- Changes to usage documentation
- Deployment to GitHub Pages

---

## ✅ Acceptance Criteria Checklist

### Must Have (Go Live)
- [ ] FR-1: Tab-based installation working
- [ ] FR-2: Time to first query < 5 minutes
- [ ] FR-3: All code blocks use actual commands
- [ ] FR-5: Copy-paste workflow validated
- [ ] NFR-2: 100% code block success

### Should Have (Quality)
- [ ] FR-4: Expandable details implemented
- [ ] NFR-1: Timing verified

### Nice to Have (Polish)
- [ ] Animated progress indicators
- [ ] Visual command highlighting
- [ ] Interactive examples

---

## 📈 Success Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Files updated | 4/4 | 100% |
| Code block success | 100% | Manual copy-paste test |
| Time to first query | < 5 min | Timer test |
| Tab navigation | 3/3 tabs | Verify each OS |

---

## 📅 Timeline

| Phase | Duration | Tasks | Focus |
|-------|----------|-------|-------|
| Planning | - | 2 | This document |
| Implementation | 1 hr | 6 | Update 4 files |
| Validation | 15 min | 2 | Copy-paste test |
| **Total** | **~1.5 hrs** | **10** | |

---

## 📝 Notes

**Constraint**: Follow SDD protocol (AGENTS.md)  
**Testing**: Manual copy-paste validation  
**Documentation**: Update completion in index.md  
**Branch**: `feature/013-getting-started-docs`

---

**Created**: January 31, 2026  
**Status**: Ready for Planning Approval  
**Next**: Create plan.md
