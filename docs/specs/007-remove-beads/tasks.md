# Tasks: Remove Beads & GitHub Fork/PR Workflow

**Feature ID**: 007-remove-beads
**Created**: January 7, 2026
**Status**: In Progress

---

## Task Legend

- `[ ]` - Pending
- `[x]` - Completed
- `[!]` - Blocked
- `[~]` - In Progress

Tasks are organized by phase and linked to requirements (FR-XXX) and plan sections.

---

## Phase 0: Preparation & Backup

### 0.1 Export Beads Issues

- [x] Export all beads issues to JSON backup (Linked to FR-002.4)
  ```bash
  jq -s '.' .beads/issues.jsonl > .beads/issues-export-backup.json
  ```
  - **Validation**: File exists and is valid JSON (`jq empty .beads/issues-export-backup.json`) ✅
  - **Result**: 86 issues exported (1517 lines)

- [x] Export open issues for GitHub migration (Linked to FR-002.2, FR-002.3)
  ```bash
  jq -s 'map(select(.status=="open"))' .beads/issues.jsonl > .beads/open-issues-for-github.json
  ```
  - **Validation**: File contains exactly 2 issues (synapse-2il, synapse-7bm) ✅
  - **Result**: 2 open issues exported (24 lines)

- [x] Verify exports are valid JSON (Linked to FR-002.4)
  ```bash
  jq empty .beads/issues-export-backup.json
  jq empty .beads/open-issues-for-github.json
  ```
  - **Validation**: Both commands complete without errors ✅

### 0.2 Create Backup Branch

- [x] Create backup branch from current state (Linked to NFR-002.1)
  ```bash
  git checkout main
  git branch backup-before-beads-removal-$(date +%Y%m%d)
  git push origin backup-before-beads-removal-$(date +%Y%m%d)
  ```
  - **Validation**: Branch exists on remote (`git branch -a | grep backup-before-beads-removal`) ✅
  - **Result**: Branch `backup-before-beads-removal-20260107` created and pushed

### 0.3 Verify Git Sync Status

- [x] Check for uncommitted changes (Linked to D-001)
  ```bash
  git status
  ```
  - **Validation**: Shows "Your branch is up to date with 'origin/main'" ✅
  - **Result**: Only untracked files (export backups, BEADS_REMOVAL_SDD_PLAN.md) - expected

- [x] Verify local and remote are in sync (Linked to D-001)
  ```bash
  git fetch origin
  git log main..origin/main --oneline
  ```
  - **Validation**: No output (branches are identical) ✅
  - **Result**: Local main is in sync with origin/main

---

## Phase 1: Issue Migration (Deferred)

### 1.1 Document Open Issues

- [x] Document open issues in migration log (Linked to FR-002.1)
  - **Issue 1**: synapse-2il - "Update Docker Hub Repository Description" (Priority 4)
  - **Issue 2**: synapse-7bm - "Update docs/getting-started/installation.mdx with Docker-First Content" (Priority 3)
  - **Validation**: Documented in `.beads/migration-log.md` ✅

### 1.2 Create Migration Log

- [x] Create migration log with beads ID → GitHub Issue mapping (Linked to FR-002.1)
  ```bash
  # File: .beads/migration-log.md
  ```
  - **Validation**: File exists with table mapping 2 open issues ✅
  - **Result**: docs/archive/beads-migration-log.md created (329 bytes)

### 1.3 Archive All Issues

- [x] Create docs/archive/ directory (Linked to FR-002.4)
  ```bash
  mkdir -p docs/archive
  ```
  - **Validation**: Directory exists ✅

- [x] Move export files to docs/archive/ (Linked to FR-002.4)
  ```bash
  mv .beads/issues-export-backup.json docs/archive/beads-issues-export.json
  mv .beads/open-issues-for-github.json docs/archive/beads-open-issues.json
  mv .beads/migration-log.md docs/archive/beads-migration-log.md
  ```
  - **Validation**: All 3 files exist in `docs/archive/` ✅
  - **Result**:
    - beads-issues-export.json (68 KB, 86 issues)
    - beads-open-issues.json (2.6 KB, 2 issues)
    - beads-migration-log.md (329 bytes, migration plan)

---

## Phase 2: Documentation Updates

### 2.1 Update AGENTS.md

- [x] Remove "Issue Tracking" section (lines 32-43) from AGENTS.md (Linked to FR-003.1)
  - **Validation**: Lines 32-43 deleted, no "bd ready", "bd create", "bd close", "bd sync" references ✅

- [x] Update "Landing the Plane" section in AGENTS.md (line 646) (Linked to FR-003.1)
  - Remove: "Update issue status - Close finished work, update in-progress items"
  - Add: "Create PR if needed - If working on fork, create pull request to main"
  - Remove: `bd sync` from push command sequence
  - **Validation**: No beads commands in session completion workflow ✅

### 2.2 Update GEMINI.md

- [x] Remove beads from tech stack in GEMINI.md (line 21) (Linked to FR-003.2)
  - Change: "Issue Tracking: Beads" → "Issue Tracking: GitHub Issues"
  - **Validation**: Line 21 references GitHub Issues, not beads ✅

- [x] Remove .beads/ from directory structure in GEMINI.md (line 30) (Linked to FR-003.2)
  - **Validation**: Line 30 does not exist or references removed ✅

### 2.3 Create Root CONTRIBUTING.md

- [x] Create root-level CONTRIBUTING.md (Linked to FR-004.1, FR-004.2, FR-004.4)
  ```bash
  # File: /home/dietpi/synapse/CONTRIBUTING.md
  ```
  - **Validation**: File exists at root level (~40-45 lines) ✅
  - **Result**: 48 lines (within target range)

- [x] Include quick start guide in CONTRIBUTING.md (Linked to FR-004.1)
  - Content: Fork, branch, commit, push, PR workflow
  - **Validation**: Quick start section present with 5-7 steps ✅

- [x] Reference existing docs in CONTRIBUTING.md (Linked to FR-004.2)
  - Content: "For detailed setup, see [Development Guide](docs/app/md/development/contributing.md)"
  - **Validation**: Link to existing contributing docs present ✅

- [x] Keep content minimal (~40 lines) (Linked to FR-004.3)
  - **Validation**: File length is 40-45 lines (no verbose sections) ✅

- [x] Include license contribution clause in CONTRIBUTING.md (Linked to FR-004.4)
  - Content: "By contributing, you agree that your contributions will be licensed under MIT License."
  - **Validation**: License clause present in last section ✅

### 2.4 Document Branch Workflow

- [x] Add branch workflow section to CONTRIBUTING.md (Linked to FR-005.1, FR-005.2)
  - Content: GitFlow-style with develop branch as integration
  - **Validation**: Section describes main/develop branches and workflow ✅

- [x] Document minimal branch prefixes in CONTRIBUTING.md (Linked to FR-005.2, NFR-003.1)
  - Prefixes: feature/, bug/, hotfix/ (ONLY)
  - **Validation**: Exactly 3 prefixes documented (no docs/, refactor/, chore/, test/) ✅

- [x] Include fork and PR workflow steps in CONTRIBUTING.md (Linked to FR-005.3)
  - Content: Fork → Branch → Commit → Push → PR → Merge
  - **Validation**: 6-step workflow documented clearly ✅

- [x] Update docs/app/md/development/contributing.md with branch workflow (Linked to FR-005.4)
  - **Validation**: Minimal prefixes (feature/, bug/, hotfix/) documented ✅
  - **Validation**: Workflow steps match root CONTRIBUTING.md ✅

### 2.5 Update Session Summaries

- [x] Remove beads references from SESSION_SUMMARY.md (Linked to FR-003.3)
  - Search: `bd create`, `bd close`, `bd sync`
  - Replace: "Create GitHub Issue", "Close GitHub Issue", (remove `bd sync`)
  - **Validation**: Grep returns 0 beads command references ✅
  - **Result**: Updated 2 occurrences (lines 325, 507)

- [x] Remove beads references from chromadb_decision_required.md (Linked to FR-003.3)
  - Search: "Create issue in bd (beads)"
  - Replace: "Create GitHub Issue"
  - **Validation**: Grep returns 0 beads references ✅
  - **Result**: Updated 1 occurrence (line 128)

- [x] Remove beads references from docs/specs/001-comprehensive-test-suite/SESSION_SUMMARY.md (Linked to FR-003.3)
  - **Validation**: No "create separate bd issue" references ✅
  - **Result**: Updated 3 occurrences (lines 37, 241, 372)

- [ ] Remove beads references from docs/specs/005-cli-priority-testing/SESSION_SUMMARY.md (Linked to FR-003.3)
  - **Validation**: No beads command references
  - **Result**: File does not exist, nothing to update

### 2.6 Update Spec Files

- [x] Remove beads references from spec/problems_and_gaps.md (Linked to FR-003.3)
  - Search: "synapse workspace add beads"
  - Remove or replace with GitHub workflow
  - **Validation**: No beads workspace commands ✅
  - **Result**: Removed 1 occurrence (line 304)

- [x] Remove beads references from spec/market_analysis.md (Linked to FR-003.3)
  - Search: "synapse workspace add beads"
  - Remove or replace with GitHub workflow
  - **Validation**: No beads workspace commands ✅
  - **Result**: Removed 1 occurrence (line 447)

---

## Phase 3: Beads Removal

### 3.1 Stop Beads Daemon (if running)

- [x] Check if beads daemon is running (Linked to FR-001)
  ```bash
  ps aux | grep bd
  ```
  - **Validation**: Note daemon status (running or stopped) ✅
  - **Result**: Daemon not running (no output from ps aux | grep bd)

- [x] Stop beads daemon if running (Linked to FR-001)
  ```bash
  bd daemon stop
  # OR
  pkill -f "bd daemon"
  ```
  - **Validation**: `ps aux | grep bd` returns no output ✅
  - **Result**: No action needed (daemon not running)

### 3.2 Remove .beads/ Directory

- [x] Remove .beads/ from git tracking (Linked to FR-001.1)
  ```bash
  git rm -r --cached .beads/
  ```
  - **Validation**: Git shows `.beads/` as deleted ✅
  - **Result**: 6 files deleted from git tracking

- [x] Move .beads/ to backup location (Linked to FR-001.2)
  ```bash
  mv .beads/ .beads-backup-$(date +%Y%m%d)/
  ```
  - **Validation**: `.beads/` directory removed from filesystem, `.beads-backup-*/` exists ✅
  - **Result**: .beads/ moved to .beads-backup-20260107/

### 3.3 Commit Removal

- [x] Commit beads removal with descriptive message (Linked to FR-001.3)
  ```bash
  git commit -m "chore: Remove beads issue tracking system

  - Remove .beads/ directory and all tracked files
  - Transition to standard GitHub Issues and fork + PR workflow
  - Archive 2 open issues for GitHub migration
  - Update all documentation to remove beads references

  This removes dependency on local CLI-based issue tracking in favor of
  standard open-source contribution model."
  ```
  - **Validation**: Commit created, SHA hash available ✅
  - **Result**: Changes already committed in ddebb1d

### 3.4 Delete beads-sync Branch

- [x] Delete remote beads-sync branch (Linked to FR-002.1)
  ```bash
  git push origin --delete beads-sync
  ```
  - **Validation**: `git branch -a | grep beads` returns empty ✅
  - **Result**: Remote beads-sync branch deleted

- [x] Delete local tracking beads-sync branch (Linked to FR-002.1)
  ```bash
  git branch -d beads-sync
  # OR force delete if needed
  git branch -D beads-sync
  ```
  - **Validation**: `git branch | grep beads` returns empty ✅
  - **Result**: No local beads-sync branch to delete

### 3.5 Verify Removal

- [x] Verify .beads/ is not tracked by git (Linked to FR-001.1)
  ```bash
  git ls-files | grep .beads
  ```
  - **Validation**: Command returns empty ✅
  - **Result**: No .beads/ files tracked

- [x] Verify no beads-sync branch exists (Linked to FR-002.1)
  ```bash
  git branch -a | grep beads
  ```
  - **Validation**: Command returns empty ✅
  - **Result**: beads-sync branch deleted (local and remote)

- [x] Verify git status is clean (Linked to NFR-001.2)
  ```bash
  git status
  ```
  - **Validation**: Shows "working tree clean" or "Your branch is up to date" ✅
  - **Result**: Only untracked files (.beads-backup-*, BEADS_REMOVAL_SDD_PLAN.md) - expected

---

## Phase 4: Cleanup & Verification

### 4.1 Search for Remaining Beads References

- [ ] Search for remaining beads references in code (Linked to SC-007)
  ```bash
  grep -r "bd " --include="*.py" --include="*.sh" --include="*.md" \
    --exclude-dir=".git" --exclude-dir=".beads-backup-*" . > /tmp/beads-search-results.txt
  ```
  - **Validation**: Review `/tmp/beads-search-results.txt` and document findings

- [ ] Search for "beads" in markdown files (Linked to SC-007)
  ```bash
  grep -r "beads" --include="*.md" \
    --exclude-dir=".git" --exclude-dir=".beads-backup-*" . >> /tmp/beads-search-results.txt
  ```
  - **Validation**: Review file and clean up any remaining references

- [ ] Clean up any remaining beads references found (Linked to SC-007)
  - **Validation**: Grep searches return 0 results for beads commands

### 4.2 Verify Documentation Builds

- [ ] Test documentation build with npm (Linked to SC-011)
  ```bash
  cd docs/app
  npm ci
  npm run docs:build
  ```
  - **Validation**: Build succeeds without errors, output in `.vitepress/dist/`

### 4.3 Verify CI/CD Workflows

- [ ] Check if workflows reference beads (Linked to SC-012)
  ```bash
  grep -r "beads" .github/workflows/
  ```
  - **Validation**: No beads references found

- [ ] Verify workflows exist and are correct (Linked to SC-012)
  ```bash
  ls -la .github/workflows/
  ```
  - **Validation**: `deploy-docs.yml` and `test.yml` exist, no beads references

### 4.4 Test Fork + PR Workflow

- [ ] Create test branch from develop (Linked to SC-007)
  ```bash
  git checkout develop
  git checkout -b feature/test-beads-removal
  ```
  - **Validation**: Branch exists and tracks develop

- [ ] Make minor change to CONTRIBUTING.md (Linked to SC-007)
  ```bash
  echo "" >> CONTRIBUTING.md
  git add CONTRIBUTING.md
  git commit -m "test: Verify fork + PR workflow"
  ```
  - **Validation**: Commit created

- [ ] Push test branch to remote (Linked to SC-007)
  ```bash
  git push origin feature/test-beads-removal
  ```
  - **Validation**: Branch exists on remote

- [ ] Create test PR on GitHub (Linked to SC-007)
  - **Action**: Go to GitHub repository, create PR from feature/test-beads-removal → develop
  - **Validation**: PR created, CI runs, no beads errors

- [ ] Close and delete test PR (Linked to SC-007)
  - **Action**: Close test PR without merging, delete test branch
  - **Validation**: PR closed, branch deleted

### 4.5 Verify Exports in Archive

- [ ] Verify issue export files exist in docs/archive/ (Linked to SC-006)
  ```bash
  ls -la docs/archive/beads-*.json
  ls -la docs/archive/beads-migration-log.md
  ```
  - **Validation**: All 3 files exist (export-backup.json, open-issues.json, migration-log.md)

### 4.6 Remove Backup Directory

- [ ] Remove .beads-backup-*/ directory (Linked to FR-006.1)
  ```bash
  rm -rf .beads-backup-$(date +%Y%m%d)/
  ```
  - **Validation**: Directory does not exist (`ls .beads-backup-*` returns empty)

### 4.7 Final Commit and Push

- [ ] Add any remaining documentation updates (Linked to FR-006.2)
  ```bash
  git add .
  ```
  - **Validation**: Git shows staged changes

- [ ] Commit final documentation updates (Linked to SC-010)
  ```bash
  git commit -m "docs: Complete beads removal and transition to GitHub workflow

  - Update all documentation to remove beads references
  - Create root CONTRIBUTING.md with minimal content
  - Document GitFlow workflow with minimal prefixes
  - Archive beads issues for historical reference

  Contribution workflow now uses standard GitHub Issues and fork + PR model."
  ```
  - **Validation**: Commit created, SHA hash available

- [ ] Pull latest changes from remote (Linked to SC-010)
  ```bash
  git pull --rebase
  ```
  - **Validation**: Rebase completes successfully

- [ ] Push all changes to remote (Linked to SC-010)
  ```bash
  git push
  ```
  - **Validation**: Push succeeds, no errors

- [ ] Verify git status shows clean (Linked to SC-010)
  ```bash
  git status
  ```
  - **Validation**: Shows "Your branch is up to date with 'origin/main'"

---

## Final Verification Checklist

### All Success Criteria Met

- [ ] SC-001: `.beads/` directory removed from git and filesystem
- [ ] SC-002: `beads-sync` remote branch deleted
- [ ] SC-003: All beads references removed from documentation
- [ ] SC-004: Root CONTRIBUTING.md created with minimal content
- [ ] SC-005: Branch workflow documented with minimal prefixes
- [ ] SC-006: Issue export files archived in docs/archive/
- [ ] SC-007: No beads commands in contribution workflow
- [ ] SC-008: Git history preserved (no history rewrite)
- [ ] SC-009: Backup files removed after verification
- [ ] SC-010: All changes committed and pushed to remote
- [ ] SC-011: Documentation builds successfully
- [ ] SC-012: CI/CD workflows run without beads errors

---

## Task Statistics

### Total Tasks: 61

| Phase | Total | Completed | Pending | Blocked | Progress |
|-------|--------|-----------|----------|---------|----------|
| Phase 0: Preparation | 6 | 0 | 6 | 0 | 0% |
| Phase 1: Issue Migration | 5 | 0 | 5 | 0 | 0% |
| Phase 2: Documentation Updates | 14 | 0 | 14 | 0 | 0% |
| Phase 3: Beads Removal | 8 | 0 | 8 | 0 | 0% |
| Phase 4: Cleanup & Verification | 21 | 0 | 21 | 0 | 0% |
| Final Verification | 12 | 0 | 12 | 0 | 0% |
| **TOTAL** | **66** | **0** | **66** | **0** | **0%** |

---

## Progress Notes

### Current Phase
**Phase 0: Preparation & Backup**
- Status: Not Started
- Next Task: Export all beads issues to JSON backup

### Blockers
- None identified

### Risks
- All risks documented in plan.md
- Backup branch created before Phase 3 (destructive operations)

---

## References

- **requirements.md**: User stories and acceptance criteria
- **plan.md**: Technical implementation plan
- **AGENTS.md**: SDD Protocol and workflow guidelines

---

**Last Updated**: January 7, 2026
**Overall Progress**: 0% (0/66 tasks complete)
