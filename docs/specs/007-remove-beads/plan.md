# Technical Plan: Remove Beads & GitHub Fork/PR Workflow

**Feature ID**: 007-remove-beads
**Created**: January 7, 2026
**Status**: In Progress

---

## Architecture Overview

This feature involves **removal and cleanup operations** rather than new feature implementation. The architecture is straightforward:

1. **Backup Phase**: Create safety snapshots before destructive operations
2. **Migration Phase**: Export and archive existing issues
3. **Removal Phase**: Delete beads artifacts from git and filesystem
4. **Update Phase**: Update documentation to remove beads references
5. **Cleanup Phase**: Remove backup files and verify completeness

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    PHASE 0: PREPARATION                 │
│  - Export beads issues to JSON                           │
│  - Create backup branch                                   │
│  - Verify git sync status                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│              PHASE 1: ISSUE MIGRATION                     │
│  - Export open issues (deferred - wait for public repo)  │
│  - Export all issues to archive                          │
│  - Document migration plan                                │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                PHASE 2: DOCUMENTATION UPDATES              │
│  - Update AGENTS.md (remove beads sections)               │
│  - Update GEMINI.md (remove beads references)            │
│  - Update all session summaries and spec files             │
│  - Create root CONTRIBUTING.md (minimal)                  │
│  - Document branch workflow (minimal prefixes)              │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                  PHASE 3: BEADS REMOVAL                  │
│  - Stop beads daemon (if running)                        │
│  - Remove .beads/ from git tracking                     │
│  - Delete .beads/ directory                             │
│  - Delete beads-sync branch                              │
│  - Commit removal                                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────┐
│                PHASE 4: CLEANUP & VERIFICATION           │
│  - Search for remaining beads references                 │
│  - Verify documentation builds                           │
│  - Verify CI/CD workflows                               │
│  - Move exports to docs/archive/                         │
│  - Remove backup files                                  │
│  - Final commit and push                                │
└─────────────────────────────────────────────────────────────┘
```

---

## Technology Stack

**Existing Tools:**
- `git` - Version control and repository management
- `jq` - JSON parsing for beads issue export
- `bash` - Shell scripting for automation
- `GitHub CLI (gh)` - Optional tool for creating GitHub Issues

**No New Dependencies Required.**

---

## Phase-by-Phase Implementation Plan

### Phase 0: Preparation & Backup

**Objective**: Create safety snapshot before any destructive operations

**Tasks:**

#### 0.1 Export Beads Issues
**Commands:**
```bash
# Export all beads issues to JSON
jq -s '.' .beads/issues.jsonl > .beads/issues-export-backup.json

# Export open issues for GitHub migration
jq -s 'map(select(.status=="open"))' .beads/issues.jsonl > .beads/open-issues-for-github.json
```

**Files Created:**
- `.beads/issues-export-backup.json` - All 86 issues (84 closed + 2 open)
- `.beads/open-issues-for-github.json` - 2 open issues for future GitHub migration

**Verification:**
```bash
# Verify exports are valid JSON
jq empty .beads/issues-export-backup.json
jq empty .beads/open-issues-for-github.json
```

#### 0.2 Create Backup Branch
**Commands:**
```bash
# Create backup branch from current state
git checkout main
git branch backup-before-beads-removal-$(date +%Y%m%d)
git push origin backup-before-beads-removal-$(date +%Y%m%d)
```

**Verification:**
```bash
# Verify backup branch exists on remote
git branch -a | grep backup-before-beads-removal
```

**Note:** This branch will be kept indefinitely as a recovery point.

#### 0.3 Verify Git Sync Status
**Commands:**
```bash
# Check for uncommitted changes
git status

# Verify local and remote are in sync
git fetch origin
git log main..origin/main --oneline
```

**Expected Output:**
- `git status` should show: "Your branch is up to date with 'origin/main'"
- No uncommitted changes
- No untracked files (except maybe backups we just created)

---

### Phase 1: Issue Migration (Deferred)

**Objective**: Prepare for GitHub Issue migration (to be executed after repository is public)

**Current Plan:**

#### 1.1 Document Open Issues
**Open Issues to Migrate:**

1. **synapse-2il**: "Update Docker Hub Repository Description"
   - Priority: 4 (low)
   - Type: task
   - Source: `.beads/open-issues-for-github.json`

2. **synapse-7bm**: "Update docs/getting-started/installation.mdx with Docker-First Content"
   - Priority: 3 (medium)
   - Type: task
   - Source: `.beads/open-issues-for-github.json`

#### 1.2 Create Migration Log
**File:** `.beads/migration-log.md`

**Content:**
```markdown
# Beads to GitHub Issue Migration Log

## Open Issues (to be created on GitHub)

| Beads ID | GitHub Issue | Title | Status |
|-----------|--------------|--------|--------|
| synapse-2il | TBD | Update Docker Hub Repository Description | Pending |
| synapse-7bm | TBD | Update docs/getting-started/installation.mdx with Docker-First Content | Pending |

## Closed Issues (archived, not migrated)

Total closed issues: 84
All archived in: `docs/archive/beads-issues-export-backup.json`

**Note:** Migration will be executed after repository is made public.
```

#### 1.3 Archive All Issues
**Commands:**
```bash
# Move export files to docs/archive/
mkdir -p docs/archive
mv .beads/issues-export-backup.json docs/archive/
mv .beads/open-issues-for-github.json docs/archive/
mv .beads/migration-log.md docs/archive/
```

**Files Moved:**
- `docs/archive/beads-issues-export-backup.json`
- `docs/archive/beads-open-issues-for-github.json`
- `docs/archive/beads-migration-log.md`

**Note:** Actual GitHub Issues creation is **deferred** until repository is made public.

---

### Phase 2: Documentation Updates

**Objective**: Remove all beads references from documentation and create minimal CONTRIBUTING.md

#### 2.1 Update AGENTS.md

**Location:** `/home/dietpi/synapse/AGENTS.md`

**Changes Required:**

a. **Remove "Issue Tracking" Section (lines 32-43):**

```markdown
# DELETE THIS SECTION:
# Issue Tracking

This project uses **bd (beads)** for issue tracking.
Run `bd prime` for workflow context, or install hooks (`bd hooks install`) for auto-injection.

**Quick reference:**
- `bd ready` - Find unblocked work
- `bd create "Title" --type task --priority=2` - Create issue
- `bd close <id>` - Complete work
- `bd sync` - Sync with git (run at session end)

For full workflow details: `bd prime`
```

b. **Update "Landing the Plane" Section (line 646):**

```markdown
# CHANGE FROM:
3. **Update issue status** - Close finished work, update in-progress items
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   bd sync
   git push
   git status  # MUST show "up to date with origin"
   ```

# CHANGE TO:
3. **Create PR if needed** - If working on fork, create pull request to main
4. **PUSH TO REMOTE** - This is MANDATORY:
   ```bash
   git pull --rebase
   git push
   git status  # MUST show "up to date with origin"
   ```
```

#### 2.2 Update GEMINI.md

**Location:** `/home/dietpi/synapse/GEMINI.md`

**Changes Required:**

a. **Remove Beads from Tech Stack (line 21):**

```markdown
# CHANGE FROM:
*   **Issue Tracking:** [Beads](https://github.com/steveyegge/beads) (Local, CLI-based).

# CHANGE TO:
*   **Issue Tracking:** [GitHub Issues](https://github.com/kayis-rahman/synapse/issues) (Standard open-source workflow).
```

b. **Remove .beads/ from Directory Structure (line 30):**

```markdown
# DELETE THIS LINE:
*   `.beads/`: Local issue tracking database.
```

#### 2.3 Create Root CONTRIBUTING.md

**Location:** `/home/dietpi/synapse/CONTRIBUTING.md`

**Content:**
```markdown
# Contributing to SYNAPSE

Contributions are welcome! Here's how to get started.

## Quick Start

1. **Fork the repository**
2. **Create a feature branch** from `develop`:
   ```bash
   git checkout develop
   git checkout -b feature/your-feature-name
   ```
3. **Make your changes** following our code style standards
4. **Test your changes** locally
5. **Commit your changes**:
   ```bash
   git commit -m "feat: Add amazing feature"
   ```
6. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```
7. **Create a Pull Request** targeting `develop` branch

## Branch Workflow

We follow GitFlow-style workflow:

- `main` - Production releases (protected)
- `develop` - Integration branch (protected)
- `feature/*` - Feature development
- `bug/*` - Bug fixes
- `hotfix/*` - Critical production fixes

## Development Setup

For detailed setup instructions, see [Development Guide](docs/app/md/development/contributing.md).

## Issue Tracking

We use [GitHub Issues](https://github.com/kayis-rahman/synapse/issues) for:
- Bug reports
- Feature requests
- Documentation improvements

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
```

**Expected Length:** ~40-45 lines (minimal)

#### 2.4 Update Session Summaries

**Files to Update:**
- `SESSION_SUMMARY.md`
- `chromadb_decision_required.md`
- `docs/specs/001-comprehensive-test-suite/SESSION_SUMMARY.md`
- `docs/specs/005-cli-priority-testing/SESSION_SUMMARY.md` (if exists)

**Search and Replace Patterns:**
- `bd create` → "Create GitHub Issue"
- `bd close` → "Close GitHub Issue"
- `bd ready` → "Check GitHub Issues"
- `bd sync` → (remove)

#### 2.5 Update Spec Files

**Files to Update:**
- `spec/problems_and_gaps.md`
- `spec/market_analysis.md`

**Changes:**
- Remove `synapse workspace add beads` references
- Remove beads workflow mentions

#### 2.6 Update docs/specs/index.md

**Changes:**
- Remove beads references from SDD protocol (if any)
- Update documentation to reference GitHub Issues instead of beads

---

### Phase 3: Beads Removal

**Objective**: Remove all beads artifacts from git and filesystem

#### 3.1 Stop Beads Daemon (if running)

**Commands:**
```bash
# Check if daemon is running
ps aux | grep bd

# If running, stop it
bd daemon stop
# OR
pkill -f "bd daemon"
```

**Verification:**
```bash
# Confirm daemon is stopped
ps aux | grep bd
# Should return no output
```

#### 3.2 Remove .beads/ Directory

**Commands:**
```bash
# Remove from git tracking
git rm -r --cached .beads/

# Move to backup location (instead of delete)
mv .beads/ .beads-backup-$(date +%Y%m%d)/
```

**Note:** Using `mv` instead of `rm -rf` for safety during verification phase.

#### 3.3 Commit Removal

**Commands:**
```bash
# Commit the removal
git commit -m "chore: Remove beads issue tracking system

- Remove .beads/ directory and all tracked files
- Transition to standard GitHub Issues and fork + PR workflow
- Archive 2 open issues for GitHub migration
- Update all documentation to remove beads references

This removes dependency on local CLI-based issue tracking in favor of
standard open-source contribution model.

Note: Git history preserved - no beads-related commits removed."
```

#### 3.4 Delete beads-sync Branch

**Commands:**
```bash
# Delete remote branch
git push origin --delete beads-sync

# Delete local tracking branch
git branch -d beads-sync

# If deletion fails (not merged), force delete
git branch -D beads-sync
```

**Verification:**
```bash
# Verify beads-sync branch is gone
git branch -a | grep beads
# Should return empty
```

#### 3.5 Verify Removal

**Commands:**
```bash
# Verify .beads/ is not in git
git ls-files | grep .beads
# Should return empty

# Verify git status is clean
git status

# Verify no beads-sync branch exists
git branch -a | grep beads
# Should return empty
```

---

### Phase 4: Cleanup & Verification

**Objective**: Verify all changes are complete and clean up temporary files

#### 4.1 Search for Remaining Beads References

**Commands:**
```bash
# Search in source code
grep -r "bd " --include="*.py" --include="*.sh" --include="*.md" \
  --exclude-dir=".git" --exclude-dir=".beads-backup-*" . > /tmp/beads-search-results.txt

# Search for "beads" in markdown
grep -r "beads" --include="*.md" \
  --exclude-dir=".git" --exclude-dir=".beads-backup-*" . >> /tmp/beads-search-results.txt
```

**Review:**
- Open `/tmp/beads-search-results.txt`
- Review each result and determine if it needs cleanup
- Clean up as needed

**Expected Findings:**
- Some references in historical context (okay to keep)
- Documentation references already updated in Phase 2

#### 4.2 Verify Documentation Builds

**Commands:**
```bash
# Test docs build
cd docs/app
npm ci
npm run docs:build
```

**Expected Output:**
- Build succeeds without errors
- No beads-related build errors
- Output in `docs/app/.vitepress/dist/`

#### 4.3 Verify CI/CD Workflows

**Commands:**
```bash
# Check if workflows reference beads
grep -r "beads" .github/workflows/

# Verify workflows exist
ls -la .github/workflows/
```

**Expected Output:**
- No beads references in workflows
- Workflows: `deploy-docs.yml`, `test.yml` (no changes needed)

#### 4.4 Test Fork + PR Workflow

**Manual Testing:**
```bash
# Create test branch from develop
git checkout develop
git checkout -b feature/test-beads-removal

# Make a minor change to CONTRIBUTING.md
echo "" >> CONTRIBUTING.md
git add CONTRIBUTING.md
git commit -m "test: Verify fork + PR workflow"

# Push to remote (if using fork)
# OR push to origin for testing
git push origin feature/test-beads-removal
```

**Verification:**
- Go to GitHub repository
- Create test PR
- Verify CI runs
- Verify no beads-related errors
- Close and delete test PR after verification

#### 4.5 Move Exports to Archive

**Commands:**
```bash
# Ensure docs/archive/ exists
mkdir -p docs/archive

# Move export files to archive
mv .beads/issues-export-backup.json docs/archive/beads-issues-export.json
mv .beads/open-issues-for-github.json docs/archive/beads-open-issues.json
mv .beads/migration-log.md docs/archive/beads-migration-log.md
```

**Note:** These files are kept for historical reference.

#### 4.6 Remove Backup Directory

**Commands:**
```bash
# Only run after all verification is successful
rm -rf .beads-backup-$(date +%Y%m%d)/
```

**Warning:** Do NOT run this until:
- All documentation builds successfully
- CI/CD workflows verified
- No remaining beads references found
- Everything is working correctly

**Alternative:** Keep backup for a few days before deleting

#### 4.7 Final Commit and Push

**Commands:**
```bash
# Add any remaining documentation updates
git add .
git commit -m "docs: Complete beads removal and transition to GitHub workflow

- Update all documentation to remove beads references
- Create root CONTRIBUTING.md with minimal content
- Document GitFlow workflow with minimal prefixes
- Archive beads issues for historical reference

Contribution workflow now uses standard GitHub Issues and fork + PR model."

# Push to remote
git pull --rebase
git push

# Verify push succeeded
git status
# Should show: "Your branch is up to date with 'origin/main'"
```

---

## Risk Assessment

### High Risk
**None identified.** All operations are reversible from backup branch.

### Medium Risk

1. **Removing .beads/ from git**
   - **Risk**: Accidental removal of important files
   - **Mitigation**: Backup branch created before removal
   - **Reversal**: Restore from backup branch

2. **Deleting beads-sync branch**
   - **Risk**: Loss of issue tracking history
   - **Mitigation**: All issues exported to JSON before deletion
   - **Reversal**: Restore from issue export files

### Low Risk

1. **Documentation updates**
   - **Risk**: Incomplete removal of beads references
   - **Mitigation**: Comprehensive search and review
   - **Reversal**: Git revert of documentation commits

2. **Deleting backup files**
   - **Risk**: Unable to recover if issues discovered later
   - **Mitigation**: Backup branch exists indefinitely
   - **Reversal**: Cannot recover deleted files (backup branch remains)

---

## Dependencies

### External Dependencies
- **None**

### Internal Dependencies
- **D-001**: Git repository must be in clean state before starting
- **D-002**: beads daemon must be stopped before removal
- **D-003**: All exports completed before directory removal
- **D-004**: Documentation updates completed before beads removal

---

## Testing Strategy

### Unit Testing
**Not applicable** - This is a removal/cleanup feature.

### Integration Testing

1. **Test Documentation Build** (Phase 4.2)
   - Run `npm run docs:build`
   - Verify no build errors
   - Verify output is generated correctly

2. **Test CI/CD Workflows** (Phase 4.3)
   - Verify workflows run correctly
   - Check for beads-related errors
   - Ensure tests pass

### Manual Testing

1. **Test Fork + PR Workflow** (Phase 4.4)
   - Create test branch and PR
   - Verify CI runs on PR
   - Verify no beads-related errors
   - Clean up test PR

### Smoke Testing

After completion:
- [ ] Clone repository to fresh location
- [ ] Verify documentation builds
- [ ] Verify no beads references in codebase
- [ ] Verify contributing workflow works

---

## Rollback Plan

If any issues arise during implementation, rollback as follows:

### Rollback from Phase 3 (Beads Removal)
```bash
# Restore from backup branch
git checkout backup-before-beads-removal-YYYYMMDD
git branch -f main
git checkout main
git push origin main --force
```

### Rollback from Phase 2 (Documentation Updates)
```bash
# Revert documentation commits
git log --oneline | grep "docs: Complete beads removal"
git revert <commit-hash>
git push
```

### Rollback from Phase 1 (Issue Migration)
**Not applicable** - Issue migration is deferred.

### Rollback from Phase 0 (Backup)
**Not applicable** - Phase 0 is backup creation.

---

## Success Metrics

The feature will be considered **successful** when:

1. **SM-001**: `.beads/` directory removed from git and filesystem
2. **SM-002**: `beads-sync` remote branch deleted
3. **SM-003**: All beads references removed from documentation (grep search returns 0 results in code)
4. **SM-004**: Root CONTRIBUTING.md created (~40-45 lines)
5. **SM-005**: Branch workflow documented with minimal prefixes (feature/, bug/, hotfix/)
6. **SM-006**: Issue export files archived in `docs/archive/`
7. **SM-007**: No beads commands in contribution workflow
8. **SM-008**: Git history preserved (no history rewrite)
9. **SM-009**: Backup files removed after verification
10. **SM-010**: All changes committed and pushed to remote (git status clean)
11. **SM-011**: Documentation builds successfully (npm run docs:build)
12. **SM-012**: CI/CD workflows run without beads errors

---

## Timeline Estimates

| Phase | Estimated Effort | Risk Level | Dependencies |
|-------|-----------------|------------|--------------|
| Phase 0: Preparation | 30 minutes | None | None |
| Phase 1: Issue Migration | 30 minutes | Low | Phase 0 complete |
| Phase 2: Documentation Updates | 1-1.5 hours | Low | None (can parallelize) |
| Phase 3: Beads Removal | 30-60 minutes | Medium | Phase 1 complete |
| Phase 4: Cleanup & Verification | 30-60 minutes | Low | Phase 3 complete |
| **Total** | **3-4.5 hours** | | |

---

## Open Questions and Decisions

### Q-001: Should we create GitHub Issues now?
**Decision**: Wait until repository is made public (deferred).
**Rationale**: GitHub Issues don't exist for private repositories, and this aligns with open-sourcing timeline.

### Q-002: Should we remove beads-related commits from git history?
**Decision**: NO (per user constraint).
**Rationale**: History preservation is more important than cleanliness. Beads commits are harmless historical context.

### Q-003: Should we keep .beads-backup/ directory?
**Decision**: Delete after verification (per user constraint).
**Rationale**: Backup branch provides recovery; local backup is redundant.

### Q-004: Minimal or comprehensive branch prefixes?
**Decision**: Minimal (feature/, bug/, hotfix/) per user constraint.
**Rationale**: Simpler workflow, less cognitive load for contributors.

---

## References

- **AGENTS.md**: Spec-Driven Development (SDD) Protocol
- **CONTRIBUTING.md**: Existing contribution guide (docs/app/md/development/contributing.md)
- **Beads Documentation**: https://github.com/steveyegge/beads
- **GitHub Flow**: https://guides.github.com/introduction/flow/
- **GitFlow**: https://nvie.com/posts/a-successful-git-branching-model/

---

## Sign-Off

**Author**: AI Assistant
**Date**: January 7, 2026
**Status**: Ready for Implementation
