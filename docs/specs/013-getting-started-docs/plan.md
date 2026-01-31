# Feature 013 - Getting Started Documentation Refresh: Technical Plan

**Feature ID**: 013-getting-started-docs  
**Status**: [Planning]  
**Created**: January 31, 2026  
**Objective**: Update fumadocs getting started section for speed-first experience

---

## 🎯 Technical Approach

### Overview

This feature updates 4 fumadocs files to create a speed-first getting started experience. The approach is:

1. **Trim introduction** to minimal hook + quick start link
2. **Tab-based installation** for platform-specific instructions
3. **Speed-first quick start** with one-command-per-step workflow
4. **Expandable details** for users who want to learn more
5. **Demote configuration** to reference material

### Current State Analysis

#### Current Files

| File | Current State | Issues |
|------|---------------|--------|
| `introduction.md` | Full neurobiological metaphor explanation | Too verbose, not speed-first |
| `installation.md` | Generic pip install instructions | Doesn't match reality |
| `quick-start.md` | Multi-command, assumes pre-configured env | Commands don't exist |
| `configuration.md` | Detailed config explanation | Should be reference, not prominent |

#### Current Command References (WRONG)

| Documentation Says | Actual Command |
|-------------------|----------------|
| `pip install synapse` | `pip install -e .` |
| `synapse-mcp-server` | `python -m synapse.cli.main start` |
| `synapse-bulk-ingest` | `python -m synapse.cli.main ingest` |
| `synapse query` | `python -m synapse.cli.main query` |
| `synapse list-projects` | Not implemented |

### New Design

#### 1. `introduction.md` - Minimal Hook

**Before (37 lines):**
- Full neurobiological metaphor
- Why local-first section
- Quick example (with wrong commands)

**After (10 lines):**
```markdown
# Introduction

SYNAPSE is a local-first RAG system that connects your knowledge to AI.

**Core features:**
- Three memory types (semantic, episodic, symbolic)
- MCP protocol integration
- Local embedding model (BGE-M3)

[Quick Start →](./quick-start)
```

#### 2. `installation.md` - Tab-Based OS Options

**Design:**
```markdown
# Installation

::tabs
:::tab{label="macOS"}
```bash
# Clone and install
git clone https://github.com/kayis-rahman/synapse.git
cd synapse
pip install -e .

# Verify
python -m synapse.cli.main --help
```
:::
:::tab{label="Linux"}
...same as macOS...
:::
:::tab{label="Docker"}
```bash
# Pull and run
docker pull kayisrahman/synapse:latest
docker run -p 8002:8002 kayisrahman/synapse
```
:::
:::
```

**Features:**
- Tab-based OS selection
- Same commands for macOS/Linux (Python-based)
- Docker option for container users
- Verification step

#### 3. `quick-start.md` - Speed-First Redesign

**Design:**
```markdown
# Quick Start

**Goal:** First query in 5 minutes.

## 1️⃣ Start Server

```bash
python -m synapse.cli.main start
```

> Server runs at http://localhost:8002/mcp

## 2️⃣ Ingest Your Data

```bash
# Ingest current directory
python -m synapse.cli.main ingest .

# Or ingest specific path
python -m synapse.cli.main ingest /path/to/your/docs
```

## 3️⃣ Query

```bash
python -m synapse.cli.main query "What is SYNAPSE?"
```

---

## Detailed Walkthrough

Want to understand each step?

::details{label="Step 1: Start the server"}
**What this does:**
Starts the MCP server that handles all SYNAPSE operations.

**Commands:**
```bash
python -m synapse.cli.main start
```

**Expected output:**
```
🚀 Starting SYNAPSE server...
  Port: 8002
  Environment: development
```

**Server URL:** http://localhost:8002/mcp
::

... (similar for steps 2-3)
```

**Features:**
- 3 one-line commands
- Inline server URL
- Expandable details for learning
- Expected output examples

#### 4. `configuration.md` - Demote to Reference

**Changes:**
- Keep content but reduce prominence
- Add note: "For reference after quick start"
- Link from quick start expandable details

---

## Implementation Details

### Fumadocs Syntax

#### Tabs Syntax
```markdown
::tabs
:::tab{label="macOS"}
...content...
:::
:::tab{label="Linux"}
...content...
:::
:::
```

#### Details/Collapsible Syntax
```markdown
::details{label="Section Title"}
...expandable content...
::
```

### File Locations

| File | Full Path |
|------|-----------|
| introduction.md | `/Users/kayisrahman/Documents/workspace/ideas/synapse/docs/app/md/getting-started/introduction.md` |
| installation.md | `/Users/kayisrahman/Documents/workspace/ideas/synapse/docs/app/md/getting-started/installation.md` |
| quick-start.md | `/Users/kayisrahman/Documents/workspace/ideas/synapse/docs/app/md/getting-started/quick-start.md` |
| configuration.md | `/Users/kayisrahman/Documents/workspace/ideas/synapse/docs/app/md/getting-started/configuration.md` |

### Command Examples

All commands to use:

```bash
# Installation
git clone https://github.com/kayis-rahman/synapse.git
cd synapse
pip install -e .
python -m synapse.cli.main --help

# Quick start
python -m synapse.cli.main start
python -m synapse.cli.main ingest .
python -m synapse.cli.main query "your question"

# Status check
python -m synapse.cli.main status
```

### Validation Commands

After updating, verify with:

```bash
# Test documentation builds
cd /Users/kayisrahman/Documents/workspace/ideas/synapse/docs && npm run build

# Test copy-paste workflow
cd /Users/kayisrahman/Documents/workspace/ideas/synapse
git clone test-clone .
pip install -e . -q
python -m synapse.cli.main start &
sleep 3
python -m synapse.cli.main ingest . -q
python -m synapse.cli.main query "test"
```

---

## Risk Assessment

### Low Risk
- **Risk**: Typo in documentation
- **Mitigation**: Copy-paste validation
- **Impact**: Minor, quick fix

### Low Risk
- **Risk**: Fumadocs syntax error
- **Mitigation**: Use proven syntax (tabs/details)
- **Impact**: Build failure, easy to fix

### Medium Risk
- **Risk**: CLI commands change
- **Mitigation**: Use Feature 007 as source of truth
- **Impact**: Documentation mismatch, need update

---

## Testing Strategy

### Manual Testing

| Test | Description | Expected Result |
|------|-------------|-----------------|
| Copy-paste install | Copy macOS tab, paste to terminal | Commands work |
| Copy-paste start | Copy start command | Server starts |
| Copy-paste ingest | Copy ingest command | Files ingested |
| Copy-paste query | Copy query command | Results returned |
| Tab navigation | Click each OS tab | Correct content shown |
| Detail expansion | Click each expandable section | Content expands |

### Automated Testing

| Test | Tool | Expected Result |
|------|------|-----------------|
| Docs build | `npm run build` | No errors |
| Links | Manual check | All links work |
| Code blocks | Manual check | Syntactically correct |

---

## Implementation Phases

### Phase 1: Backup and Create New Files (5 min)

1. Backup current files
2. Create new version of introduction.md
3. Verify fumadocs syntax

### Phase 2: Installation and Quick Start (30 min)

4. Update installation.md with tabs
5. Update quick-start.md with speed-first design
6. Add expandable details

### Phase 3: Configuration Demotion (10 min)

7. Demote configuration.md to reference
8. Add navigation links

### Phase 4: Validation (15 min)

9. Copy-paste workflow test
10. Documentation build test

---

## Files to Modify

### New Files Created
None (all modifications)

### Files Modified
| File | Changes |
|------|---------|
| `introduction.md` | Trim to 10 lines |
| `installation.md` | Tab-based OS options |
| `quick-start.md` | Complete redesign |
| `configuration.md` | Demote to reference |

### Files Deleted
None

---

## Dependencies

### Pre-requisites
- Python 3.8+
- git
- fumadocs (already installed)

### Post-requisites
- None

---

## Success Criteria

### Must Have
- [ ] All 4 files updated
- [ ] Tab-based installation working
- [ ] Copy-paste workflow: install → start → ingest → query
- [ ] Time to first query: < 5 minutes
- [ ] Documentation builds without errors

### Should Have
- [ ] Expandable details implemented
- [ ] All 3 OS tabs verified

### Nice to Have
- [ ] Visual enhancements
- [ ] Animated examples

---

## Timeline

| Phase | Duration | Tasks | Deliverables |
|-------|----------|-------|--------------|
| Phase 1 | 5 min | 3 | Backups, intro update |
| Phase 2 | 30 min | 3 | Install, quick start |
| Phase 3 | 10 min | 1 | Config demotion |
| Phase 4 | 15 min | 2 | Validation |
| **Total** | **~1 hr** | **9** | **4 updated files** |

---

## Notes

### Command Consistency
All commands use `python -m synapse.cli.main` pattern:
- No shell wrapper scripts
- No pip install shortcuts
- Explicit is better than implicit

### Design Principles
1. **Speed first**: One command per step
2. **Learn on demand**: Expandable details
3. **Platform aware**: Tab-based OS options
4. **Copy-paste ready**: No editing required

### Future Enhancements
After this feature:
- Add video walkthrough
- Add interactive examples
- Add troubleshooting section

---

**Plan Created**: January 31, 2026  
**Status**: Ready for Approval  
**Next**: Create tasks.md after approval
