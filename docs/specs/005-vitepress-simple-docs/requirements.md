# VitePress Simple Documentation - Requirements

**Feature ID**: 005-vitepress-simple-docs
**Status**: [In Progress]
**Created**: January 7, 2026
**Last Updated**: January 7, 2026

---

## Executive Summary

Create a clean, simple VitePress-based documentation system for SYNAPSE by consolidating existing documentation content from two mixed systems (Fumadocs and VitePress) into a single, streamlined VitePress setup.

### Problem Statement

The `docs/` directory currently contains:
- **Fumadocs** (Next.js-based): 16 MDX files in `/docs/content/docs/`
- **Partial VitePress**: 4 markdown files in `/docs/docs/docs/api/cli-commands/`
- **Mixed config files**: Fumadocs and Next.js configurations
- **Cluttered structure**: Empty directories, archives, debris files

This creates confusion, maintenance overhead, and prevents clean deployment.

### Solution

Restructure to a clean three-directory system:
```
docs/
├── app/        # VitePress engine only
├── specs/      # SDD specifications
└── md/         # All documentation content
```

### Success Metrics

- [ ] Clean `/docs/` directory with only 3 subdirectories
- [ ] All documentation accessible via VitePress (16+ pages)
- [ ] Build time < 2 minutes
- [ ] Pages load < 2 seconds
- [ ] 100% cross-link coverage (no broken links)
- [ ] Documentation deployment to GitHub Pages

---

## User Stories

### US-1: Developer Wants Clean Documentation Structure

**As a** developer working on SYNAPSE
**I want** a clean documentation directory with only `app/`, `specs/`, and `md/`
**So that** I can easily understand and maintain the documentation system

**Acceptance Criteria:**
- [ ] `/docs/` directory contains ONLY: `app/`, `specs/`, `md/`
- [ ] No configuration files at `/docs/` root level
- [ ] No empty directories
- [ ] No archive directories
- [ ] No legacy documentation systems

**Priority:** High

---

### US-2: Developer Wants Single Documentation System

**As a** developer contributing to SYNAPSE
**I want** to use VitePress as the sole documentation system
**So that** I don't need to maintain two separate documentation engines

**Acceptance Criteria:**
- [ ] Fumadocs system completely removed
- [ ] Next.js configuration files removed
- [ ] Only VitePress remains
- [ ] All documentation content in VitePress-compatible markdown
- [ ] Single build command: `npm run docs:build`

**Priority:** High

---

### US-3: Developer Wants Comprehensive Documentation Coverage

**As a** SYNAPSE user
**I want** complete documentation covering all SYNAPSE features
**So that** I can effectively use the system without guessing

**Acceptance Criteria:**
- [ ] Getting Started documentation (4 pages)
  - Introduction
  - Installation
  - Quick Start
  - Configuration
- [ ] Architecture documentation (3 pages)
  - Overview
  - Memory System
  - MCP Protocol
- [ ] Usage documentation (3 pages)
  - MCP Tools
  - Ingestion
  - Querying
- [ ] API Reference (3 pages)
  - Memory Tools
  - Server API
  - CLI Commands
- [ ] Development documentation (3 pages)
  - Contributing
  - Testing
  - Deployment
- [ ] Home page with SYNAPSE branding

**Priority:** High

---

### US-4: Developer Wants Easy Navigation

**As a** SYNAPSE user
**I want** clear navigation structure with sidebar
**So that** I can quickly find the documentation I need

**Acceptance Criteria:**
- [ ] Sidebar navigation with all sections
- [ ] Collapsible sections for API Reference
- [ ] Home page link in nav bar
- [ ] Getting Started link in nav bar
- [ ] API Reference link in nav bar
- [ ] Internal cross-references between pages

**Priority:** Medium

---

### US-5: Developer Wants Search Functionality

**As a** SYNAPSE user
**I want** to search documentation for specific terms
**So that** I can quickly find relevant information

**Acceptance Criteria:**
- [ ] Search bar visible on all pages
- [ ] Keyboard shortcut ⌘K works
- [ ] Search results highlight matching terms
- [ ] Search covers all documentation pages

**Priority:** Medium

---

### US-6: Developer Wants Dark/Light Theme Support

**As a** SYNAPSE user
**I want** to toggle between dark and light themes
**So that** I can read documentation comfortably in any lighting

**Acceptance Criteria:**
- [ ] Theme toggle button visible
- [ ] Theme preference persists across sessions
- [ ] Dark theme is legible
- [ ] Light theme is legible
- [ ] Default theme respects system preference

**Priority:** Low

---

## Functional Requirements

### FR-1: Clean Directory Structure
- The `/docs/` directory must contain ONLY three subdirectories: `app/`, `specs/`, `md/`
- All other files and directories at `/docs/` root must be removed
- Empty directories must not exist

### FR-2: VitePress Configuration
- VitePress config must point to `/docs/md/` as source directory
- Navigation must be configured with three main sections
- Sidebar must be configured with hierarchical structure
- GitHub social links must be configured

### FR-3: Content Conversion
- All 16 Fumadocs MDX files must be converted to VitePress markdown
- MDX-specific syntax must be removed (imports, components)
- Content structure must be preserved
- Internal links must be updated for new paths

### FR-4: Home Page
- Home page must feature SYNAPSE branding ("Your Data Meets Intelligence")
- Home page must have action buttons (Get Started, Quick Start)
- Home page must link to main documentation sections

### FR-5: Code Syntax Highlighting
- Code blocks must use syntax highlighting
- Supported languages: Python, bash, JSON, markdown, TypeScript

### FR-6: Cross-References
- All internal links must work correctly
- No broken links in documentation
- See Also sections must link to related pages

---

## Non-Functional Requirements

### NFR-1: Performance
- Build time: < 2 minutes
- Page load time: < 2 seconds (on localhost)
- Static generation: All pages must be statically generated

### NFR-2: Accessibility
- WCAG AA compliance for color contrast
- Keyboard navigation support
- Screen reader support
- Proper heading hierarchy (h1, h2, h3)

### NFR-3: Responsiveness
- Mobile-friendly layout (< 768px)
- Tablet-friendly layout (768px - 1024px)
- Desktop layout optimized (> 1024px)

### NFR-4: Maintainability
- Documentation files use standard markdown syntax
- No custom components that require JavaScript knowledge
- Content can be edited without build system knowledge
- Configuration is minimal and well-documented

### NFR-5: Deployment
- Must be deployable to GitHub Pages
- Build artifacts in `.vitepress/dist/`
- Base path configurable for GitHub Pages

---

## Out of Scope

The following are explicitly OUT OF SCOPE for this feature:

- Custom VitePress theme development (using default theme)
- Interactive code examples or sandboxes
- Auto-generated API documentation from code
- Multi-language support (i18n)
- Custom components beyond VitePress built-ins
- Real-time documentation preview (using standard dev server)
- Analytics integration
- User authentication or comments
- Advanced customization (custom CSS, JavaScript)

---

## Constraints

### Technical Constraints
- Must use VitePress 1.6.4 (current version)
- Must use markdown (no MDX)
- Must use default VitePress theme
- Must be deployable to GitHub Pages

### Time Constraints
- Target completion: 6 hours
- Maximum phases: 4

### Resource Constraints
- No additional dependencies beyond VitePress
- No build-time external APIs
- No custom development of VitePress plugins

---

## Dependencies

### Internal Dependencies
- Existing Fumadocs MDX content (16 files in `/docs/content/docs/`)
- Existing partial VitePress config (`/docs/app/.vitepress/config.mts`)
- Existing CLI documentation (4 files in `/docs/docs/docs/`)

### External Dependencies
- VitePress 1.6.4
- Vue 3.4.0
- TypeScript 5.3.0

---

## Risks

### Risk 1: MDX to Markdown Conversion Issues
**Description**: MDX-specific syntax may not convert cleanly to markdown

**Probability**: Medium
**Impact**: Medium
**Mitigation**:
- Manually review each converted file
- Test build after each file conversion
- Keep original MDX files until conversion verified

### Risk 2: Broken Internal Links
**Description**: Internal links may break after restructuring

**Probability**: High
**Impact**: Medium
**Mitigation**:
- Use search-and-replace for known patterns
- Manually verify all internal links
- Test navigation before deployment

### Risk 3: Build Configuration Issues
**Description**: VitePress config may need adjustment for new structure

**Probability**: Medium
**Impact**: High
**Mitigation**:
- Test build incrementally
- Verify config with small subset first
- Document configuration changes

### Risk 4: Data Loss During Cleanup
**Description**: Accidentally deleting important documentation

**Probability**: Low
**Impact**: High
**Mitigation**:
- Create backup of `/docs/` before cleanup
- Migrate content BEFORE deletion
- Verify content exists in new location

---

## Acceptance Criteria Summary

### Must Have (High Priority)
- [ ] Clean directory structure (only `app/`, `specs/`, `md/`)
- [ ] Single VitePress system (Fumadocs removed)
- [ ] All 16 documentation pages converted and accessible
- [ ] Build succeeds with `npm run docs:build`
- [ ] No broken links in navigation
- [ ] Dev server runs on `localhost:5173`

### Should Have (Medium Priority)
- [ ] Search functionality works
- [ ] Dark/light theme toggle works
- [ ] Responsive design on mobile/tablet
- [ ] Home page with SYNAPSE branding

### Could Have (Low Priority)
- [ ] GitHub social links configured
- [ ] Custom styling for authority levels (optional)
- [ ] Edit on GitHub links (optional)

---

## Definition of Done

A task is considered complete when:
1. All acceptance criteria for the task are met
2. Code has been reviewed (or self-reviewed)
3. Changes are committed to git
4. Documentation is updated if needed
5. Tests (if applicable) pass

The feature is complete when:
1. All user stories have their acceptance criteria met
2. Build succeeds without errors
3. Documentation can be viewed locally
4. All internal links work
5. Feature is tracked in `docs/specs/index.md`

---

## Success Metrics Dashboard

| Metric | Target | Current | Status |
|--------|--------|---------|--------|
| Directories in /docs/ | 3 (app, specs, md) | 10+ | 🔴 Not Started |
| Documentation pages | 16+ | 0 | 🔴 Not Started |
| Build time | < 2 min | N/A | 🔴 Not Started |
| Broken links | 0 | Unknown | 🔴 Not Started |
| Fumadocs removed | 100% | 0% | 🔴 Not Started |
| VitePress configured | Yes | Partial | 🟡 In Progress |

---

## Related Features

- **002-auto-learning**: Automatic learning system (referenced in docs)
- **004-universal-hook-auto-learning**: Multi-agent hooks (referenced in docs)
- **001-comprehensive-test-suite**: Testing (referenced in development docs)

---

## Notes

### Key Decisions
1. **Default Theme**: Using VitePress default theme to minimize complexity
2. **Markdown over MDX**: Simpler, no build-time dependencies
3. **Single Source of Truth**: VitePress only (no mixed systems)
4. **Minimal Configuration**: Keep VitePress config simple and maintainable

### Content Preservation
- All 16 Fumadocs MDX files will be converted to markdown
- Content structure preserved (sections, subsections)
- Cross-references maintained
- Code examples preserved

### Migration Strategy
- Phase 1: Clean up (delete unnecessary files)
- Phase 2: Create new structure (app, specs, md)
- Phase 3: Migrate and convert content (MDX → markdown)
- Phase 4: Configure and test (VitePress config, build, links)

---

**Document Status**: Ready for Technical Planning Phase

**Next Step**: Create `plan.md` with technical architecture and implementation details
