# Beads to GitHub Issue Migration Log

**Created**: January 7, 2026
**Status**: Deferred (pending public repository)

---

## Open Issues (to be created on GitHub)

| Beads ID | GitHub Issue | Title | Status |
|-----------|--------------|--------|--------|
| synapse-2il | TBD | Update Docker Hub Repository Description | Pending |
| synapse-7bm | TBD | Update docs/getting-started/installation.mdx with Docker-First Content | Pending |

### Issue 1: synapse-2il
- **Title**: Update Docker Hub Repository Description
- **Priority**: 4 (low)
- **Type**: task
- **Description**: Add description, logo, and links to Docker Hub repository page. Steps: 1) Go to https://hub.docker.com/repository/docker/kayisrahman/synapse/general, 2) Set visibility to Public, 3) Add description: 'SYNAPSE - Your Data Meets Intelligence', 4) Add repository link: https://github.com/kayis-rahman/synapse, 5) Upload logo (optional), 6) Add tags: rag, mcp, local-ai, neural-network.
- **Estimated**: 10 min

### Issue 2: synapse-7bm
- **Title**: Update docs/getting-started/installation.mdx with Docker-First Content
- **Priority**: 3 (medium)
- **Type**: task
- **Description**: Update the Fumadocs installation documentation page with Docker-first approach, CLI commands, and all installation options. Current Status: DOCKER_INSTALLATION.md created (comprehensive) but docs/getting-started/installation.mdx still shows pip-only installation. Implementation Plan: 1) Read current docs/content/docs/getting-started/installation.mdx, 2) Add Docker Hub installation as primary option (copy from DOCKER_INSTALLATION.md), 3) Add Docker Compose as secondary option, 4) Keep pip and source as alternatives, 5) Add CLI Commands section with neurobiological commands (synapse-ignite, synapse-sense, synapse-feed), 6) Add 'Choosing an Installation Method' comparison table, 7) Update Quick Start code examples, 8) Add links to DOCKERHUB_SETUP.md and DOCKER_INSTALLATION.md.
- **Estimated**: 30 min

---

## Closed Issues (archived, not migrated)

**Total closed issues**: 84
**All archived in**: `docs/archive/beads-issues-export-backup.json`

**Note**: These 84 closed issues are historical and will not be migrated to GitHub. The export file preserves the complete history for reference.

---

## Migration Status

- [x] Export all beads issues to JSON (86 total)
- [x] Export open issues to separate file (2 open)
- [x] Document open issues in migration log
- [ ] Create GitHub Issue #1 (synapse-2il) - **DEFERRED**
- [ ] Create GitHub Issue #2 (synapse-7bm) - **DEFERRED**
- [ ] Update migration log with GitHub Issue numbers - **DEFERRED**

---

## Notes

**Migration Strategy:**
1. This file documents the 2 open issues that need to be migrated to GitHub
2. GitHub Issues will be created AFTER the repository is made public
3. When creating GitHub Issues, update the "GitHub Issue" column above with the actual issue numbers
4. All 84 closed issues are preserved in the export file but will not be migrated

**Deferral Reason:**
- GitHub Issues feature is not available for private repositories
- Repository needs to be made public before GitHub Issues can be created
- This aligns with the overall open-sourcing timeline

---

**Last Updated**: January 7, 2026
**Migration Status**: Ready (waiting for public repository)
