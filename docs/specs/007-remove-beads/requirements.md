# Requirements: Remove Beads & GitHub Fork/PR Workflow

**Feature ID**: 007-remove-beads
**Created**: January 7, 2026
**Status**: In Progress

---

## Overview

Remove all beads (bd) integration from the synapse repository and transition to standard open-source fork + pull request workflow for contributions.

## Problem Statement

Currently, synapse uses beads (bd) as a local CLI-based issue tracking system. While useful for local development, this is non-standard for open-source projects and creates barriers for contributors who expect GitHub Issues and PRs. The project needs to transition to a standard open-source contribution model.

### Current State

- **Beads Integration Points:**
  - `.beads/` directory with 7 tracked files
  - `beads-sync` remote branch for issue tracking
  - 86 issues in beads database (84 closed, 2 open)
  - Documentation references beads throughout codebase
  - AGENTS.md includes beads workflow commands
  - Git history has 2 beads-related commits

- **Beads Usage Patterns:**
  - Issue tracking: `bd create`, `bd close`, `bd ready`
  - Workflow integration: `bd sync` in session completion
  - Configuration: sync-branch set to "beads-sync"

### Barriers to Open Sourcing

1. **Non-standard workflow**: Contributors expect GitHub Issues, not local CLI
2. **Documentation overhead**: Need to explain beads installation and usage
3. **Git complexity**: beads-sync branch adds confusion to git workflow
4. **Issue migration**: Existing issues need to move to GitHub Issues
5. **Maintenance overhead**: Project maintain beads integration alongside GitHub

---

## User Stories

### US-001: Contributor Uses GitHub Issues
**As a** new contributor,
**I want to** use GitHub Issues to report bugs and request features,
**So that** I can contribute using standard open-source workflows.

**Acceptance Criteria:**
- GitHub Issues page exists and is accessible
- Issue templates are available (bug report, feature request)
- No beads installation required for contributors
- Documentation references GitHub Issues only

### US-002: Contributor Uses Fork and PR Workflow
**As a** contributor,
**I want to** fork the repository and submit pull requests,
**So that** my contributions can be reviewed and merged using standard GitHub workflows.

**Acceptance Criteria:**
- Fork and PR workflow is documented in CONTRIBUTING.md
- Branch workflow (feature/, bug/, hotfix/) is documented
- No beads commands in contribution documentation
- CI/CD runs on PRs from forks

### US-003: Maintainer Uses GitHub for Issue Management
**As a** project maintainer,
**I want to** manage issues and PRs on GitHub,
**So that** I can use standard GitHub features (labels, milestones, assignees).

**Acceptance Criteria:**
- All open issues migrated to GitHub Issues
- Closed issues archived in docs/ for historical reference
- No beads operations in maintainer workflow
- GitHub labels and templates configured

---

## Functional Requirements

### FR-001: Remove Beads Directory
The system shall remove the `.beads/` directory and all tracked files from git.

- **FR-001.1**: Remove `.beads/` from git tracking using `git rm -r --cached`
- **FR-001.2**: Delete `.beads/` directory from filesystem
- **FR-001.3**: Commit removal with descriptive message

### FR-002: Remove Beads-Sync Branch
The system shall delete the `beads-sync` remote branch.

- **FR-002.1**: Delete remote branch: `git push origin --delete beads-sync`
- **FR-002.2**: Delete local tracking branch

### FR-002: Migrate Open Issues to GitHub
The system shall migrate 2 open beads issues to GitHub Issues.

- **FR-002.1**: Export open issues from beads database
- **FR-002.2**: Create GitHub Issue #1: "Update Docker Hub Repository Description"
- **FR-002.3**: Create GitHub Issue #2: "Update docs/getting-started/installation.mdx with Docker-First Content"
- **FR-002.4**: Archive 84 closed issues in `docs/archive/` for historical reference

**Note:** GitHub Issues creation will be deferred until repository is made public.

### FR-003: Update Documentation
The system shall remove all beads references from documentation.

- **FR-003.1**: Update AGENTS.md
  - Remove "Issue Tracking" section (lines 32-43)
  - Remove `bd sync` from "Landing the Plane" section
- **FR-003.2**: Update GEMINI.md
  - Remove beads from tech stack
  - Remove `.beads/` from directory structure
- **FR-003.3**: Remove beads references from:
  - SESSION_SUMMARY.md
  - chromadb_decision_required.md
  - docs/specs/*/SESSION_SUMMARY.md
  - spec/problems_and_gaps.md
  - spec/market_analysis.md

### FR-004: Create Minimal CONTRIBUTING.md
The system shall create a root-level `CONTRIBUTING.md` file with minimal content.

- **FR-004.1**: Include quick start guide (fork, branch, PR)
- **FR-004.2**: Reference existing docs for detailed guide
- **FR-004.3**: Keep content minimal (~30-40 lines)
- **FR-004.4**: Include license contribution clause

### FR-005: Document Branch Workflow
The system shall document GitFlow-style branch workflow with minimal prefixes.

- **FR-005.1**: Document `develop` branch as integration branch
- **FR-005.2**: Document branch prefixes: `feature/`, `bug/`, `hotfix/`
- **FR-005.3**: Include fork and PR workflow steps
- **FR-005.4**: Update contributing docs with workflow

### FR-006: Cleanup After Verification
The system shall remove backup files after successful verification.

- **FR-006.1**: Remove `.beads-backup-*/` directory
- **FR-006.2**: Keep issue export files in `docs/archive/` for historical reference
- **FR-006.3**: Verify no beads references remain in codebase

---

## Non-Functional Requirements

### NFR-001: Backwards Compatibility
The removal of beads shall NOT break existing git history or code functionality.

- **NFR-001.1**: Git history preservation: Do NOT remove beads-related commits
- **NFR-001.2**: No code changes to core functionality
- **NFR-001.3**: Documentation updates only (no code logic changes)

### NFR-002: Safety and Reversibility
The removal process shall include safety measures to allow recovery if needed.

- **NFR-002.1**: Create backup branch before any destructive operations
- **NFR-002.2**: Export all beads issues to JSON before removal
- **NFR-002.3**: Keep issue export in `docs/archive/` for historical reference

### NFR-003: Minimal Branch Prefixes
The branch workflow shall use minimal prefixes only.

- **NFR-003.1**: Allowed prefixes: `feature/`, `bug/`, `hotfix/`
- **NFR-003.2**: No additional prefixes (docs/, refactor/, chore/, test/)

---

## Constraints and Assumptions

### Constraints

- **C-001**: Must NOT rewrite git history (keep beads-related commits)
- **C-002**: Must use minimal branch prefixes (feature/, bug/, hotfix/ only)
- **C-003**: Must create root CONTRIBUTING.md with minimal content
- **C-004**: Must delete backup files after verification (no redundant backups)

### Assumptions

- **A-001**: Repository will be made public after beads removal
- **A-002**: GitHub Issues will be created manually after repository is public
- **A-003**: No contributors are currently using beads for this project
- **A-004**: beads daemon is not currently running

---

## Out of Scope

The following items are explicitly **out of scope** for this feature:

- **OS-001**: Removing beads-related commits from git history (C-001 constraint)
- **OS-002**: Creating GitHub Issues now (deferred until repository is public)
- **OS-003**: Configuring branch protection rules (future enhancement)
- **OS-004**: Setting up GitHub automation (issue templates, PR templates - future)
- **OS-005**: Implementing pre-commit hooks (future enhancement)

---

## Success Criteria

The feature will be considered **successful** when:

1. **SC-001**: `.beads/` directory is removed from git and filesystem
2. **SC-002**: `beads-sync` remote branch is deleted
3. **SC-003**: All beads references are removed from documentation (AGENTS.md, GEMINI.md, etc.)
4. **SC-004**: Root CONTRIBUTING.md is created with minimal content
5. **SC-005**: Branch workflow documented with minimal prefixes (feature/, bug/, hotfix/)
6. **SC-006**: Issue export files archived in `docs/archive/`
7. **SC-007**: No beads commands in contribution workflow
8. **SC-008**: Git history preserved (no history rewrite)
9. **SC-009**: Backup files removed after verification
10. **SC-010**: All changes committed and pushed to remote

---

## Open Questions

**Q-001**: Should we create GitHub Issues now or wait for public repository?
- **Decision**: Wait until repository is made public (deferred)

**Q-002**: Should we create issue templates on GitHub?
- **Decision**: Out of scope for this feature (future enhancement)

**Q-003**: Should we configure branch protection on main/develop?
- **Decision**: Out of scope for this feature (future enhancement)

---

## References

- AGENTS.md: Spec-Driven Development (SDD) Protocol
- docs/app/md/development/contributing.md: Existing contribution guide (fork + PR workflow)
- Beads documentation: https://github.com/steveyegge/beads

---

## Stakeholders

- **Primary**: Project maintainer (current beads user)
- **Secondary**: Future contributors (who will use GitHub Issues/PRs)
- **Tertiary**: Open-source community (GitHub users)
