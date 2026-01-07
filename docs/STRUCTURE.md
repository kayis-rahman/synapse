# SYNAPSE Documentation Structure

## Overview

This document explains the current VitePress documentation structure used by SYNAPSE, known as **Option B**.

## Current Implementation (Option B)

### Directory Layout

```
docs/
├── app/                              # VitePress engine
│   ├── .vitepress/
│   │   ├── config.mts                # VitePress configuration
│   │   ├── cache/                    # Build cache
│   │   └── dist/                     # Build output (generated)
│   ├── package.json                  # VitePress dependencies
│   └── node_modules/                 # Installed packages
│
├── md/                               # All markdown content
│   ├── index.md                       # Home page
│   ├── getting-started/                # 4 files
│   ├── architecture/                   # 3 files
│   ├── usage/                         # 3 files
│   ├── api-reference/                  # 3 files
│   └── development/                   # 3 files
│
├── specs/                            # SDD specifications
│   ├── index.md
│   ├── 001-comprehensive-test-suite/
│   ├── 002-auto-learning/
│   ├── 003-rag-quality-metrics/
│   ├── 004-universal-hook-auto-learning/
│   └── 005-vitepress-simple-docs/
│
└── backup-20260107-144833/          # Historical backup (old structure)
    ├── app/                          # Next.js + Fumadocs
    ├── content/                      # MDX files
    └── archive/                      # Historical docs
```

### Key Configuration

The `srcDir: "../md"` setting in `docs/app/.vitepress/config.mts` is what makes this structure work:

```typescript
// docs/app/.vitepress/config.mts
export default defineConfig({
  srcDir: "../md",  // Points VitePress to /docs/md/ directory

  title: "SYNAPSE",
  description: "Your Data Meets Intelligence - Local-first RAG system",

  themeConfig: {
    // Navigation and sidebar configuration...
  }
})
```

### How `srcDir` Works

1. **Config Location**: `/docs/app/.vitepress/config.mts`
2. **Content Location**: `/docs/md/`
3. **Build Output**: `/docs/app/.vitepress/dist/`
4. **Dev Server**: Reads content from `../md` relative to config

This means:
- VitePress config is isolated in `app/`
- Content is separate in `md/`
- Build artifacts stay in `app/.vitepress/`

---

## Why This Structure?

### 1. Separation of Concerns
- **Engine**: `app/` contains VitePress configuration and build artifacts
- **Content**: `md/` contains only documentation pages
- **Specifications**: `specs/` contains SDD development specifications

### 2. Maintainability
- Developers edit markdown files without touching configuration
- Config changes don't clutter content git history
- Easier to review content changes separately from engine changes

### 3. Git History
- Content edits show small, focused diffs
- Configuration changes tracked separately
- Clear blame attribution for both content and config

### 4. Size Efficiency
- Current structure: 72K (just content)
- Old structure: 992K (with Next.js/Fumadocs)
- **92% reduction in documentation footprint**

---

## Comparison: Before vs After

| Aspect | Old (Fumadocs/Next.js) | New (VitePress Option B) |
|--------|------------------------|--------------------------|
| Framework | Next.js 15.5.9 | VitePress 1.6.4 |
| Content Format | MDX | Markdown |
| Config Files | 5 files (next.config.mjs, source.config.ts, etc.) | 1 file (config.mts) |
| Structure | Mixed app/content | Separated app/md |
| Total Size | 992K | 72K |
| Build Complexity | High | Low |
| Dependencies | 50+ packages | 3 packages |
| Build Time | ~2 minutes | ~30 seconds |

---

## Directory Responsibilities

### `/docs/app/` - VitePress Engine

**Purpose**: Contains all VitePress-specific files

**Files**:
- `.vitepress/config.mts` - Main VitePress configuration
- `.vitepress/cache/` - Build cache (gitignored)
- `.vitepress/dist/` - Build output (gitignored)
- `package.json` - VitePress dependencies
- `node_modules/` - Installed packages (gitignored)

**What goes here**:
- VitePress configuration
- Theme customization
- Build scripts
- Node.js dependencies

**What does NOT go here**:
- Documentation content (belongs in `/docs/md/`)

### `/docs/md/` - Documentation Content

**Purpose**: Contains all documentation pages

**Files**:
- `index.md` - Home page
- `getting-started/` - 4 files (introduction, installation, quick-start, configuration)
- `architecture/` - 3 files (overview, memory-system, mcp-protocol)
- `usage/` - 3 files (mcp-tools, ingestion, querying)
- `api-reference/` - 3 files (memory-tools, server-api, cli-commands)
- `development/` - 3 files (contributing, testing, deployment)

**What goes here**:
- Documentation pages
- Images and assets (optional)
- Static content files

**What does NOT go here**:
- Configuration files
- Build artifacts
- Node.js dependencies

### `/docs/specs/` - SDD Specifications

**Purpose**: Spec-Driven Development (SDD) specifications

**Contains**:
- Feature specifications (requirements, plans, tasks)
- Implementation progress tracking
- Completion reports

### `/docs/backup-20260107-144833/` - Historical Backup

**Purpose**: Reference to previous Fumadocs/Next.js structure

**Contains**:
- Next.js application code
- Fumadocs configuration
- MDX content files
- Historical documentation

**Status**: Keep for reference, can be deleted after documentation is finalized

---

## File Location Reference

| What | Where | Purpose |
|------|-------|---------|
| VitePress Config | `/docs/app/.vitepress/config.mts` | Main configuration |
| Home Page | `/docs/md/index.md` | Landing page |
| Getting Started | `/docs/md/getting-started/` | User onboarding |
| Architecture | `/docs/md/architecture/` | System design |
| Usage | `/docs/md/usage/` | How to use SYNAPSE |
| API Reference | `/docs/md/api-reference/` | API documentation |
| Development | `/docs/md/development/` | Contributing guide |
| SDD Specs | `/docs/specs/` | Feature specifications |
| Old Backup | `/docs/backup-20260107-144833/` | Historical reference |

---

## Navigation Configuration

Navigation is configured in `/docs/app/.vitepress/config.mts`:

### Top Navigation Bar
```typescript
nav: [
  { text: 'Home', link: '/' },
  { text: 'Getting Started', link: '/getting-started/introduction' },
  { text: 'Architecture', link: '/architecture/overview' },
  { text: 'Usage', link: '/usage/mcp-tools' },
  { text: 'API Reference', link: '/api-reference/memory-tools' },
  { text: 'Development', link: '/development/contributing' }
]
```

### Sidebar Navigation
```typescript
sidebar: [
  {
    text: 'Getting Started',
    items: [
      { text: 'Introduction', link: '/getting-started/introduction' },
      { text: 'Installation', link: '/getting-started/installation' },
      { text: 'Quick Start', link: '/getting-started/quick-start' },
      { text: 'Configuration', link: '/getting-started/configuration' }
    ]
  },
  // ... more sections
]
```

---

## Quick Reference

### Working with Documentation

**Start Dev Server:**
```bash
cd docs/app
npm run docs:dev
# Runs on http://localhost:5173
```

**Build for Production:**
```bash
cd docs/app
npm run docs:build
# Output: docs/app/.vitepress/dist/
```

**Preview Production Build:**
```bash
cd docs/app
npm run docs:preview
# Runs on http://localhost:4173
```

### Adding New Pages

1. Create `.md` file in `/docs/md/` or subdirectory
2. Add frontmatter (title, description)
3. Update navigation in `/docs/app/.vitepress/config.mts`
4. Restart dev server to see changes

### Editing Existing Pages

1. Edit `.md` file in `/docs/md/`
2. Changes hot-reload automatically
3. Test by viewing in browser
4. Commit changes when satisfied

---

## Alternative Structures

### Option A (Not Used)
```
docs/
└── app/
    ├── .vitepress/
    └── index.md        # Content mixed with config
```
- **Pros**: Simpler for small projects
- **Cons**: Config and content mixed, harder to maintain

### Option B (Current)
```
docs/
├── app/
│   └── .vitepress/
└── md/
    └── index.md
```
- **Pros**: Clear separation, better organization
- **Cons**: Requires `srcDir` configuration

### Option C (Not Used)
```
docs/
└── docs/
    ├── .vitepress/
    └── index.md
```
- **Pros**: Standard VitePress structure
- **Cons**: Confusing naming (docs/docs/)

---

## Conclusion

The **Option B** structure provides a clean, maintainable documentation system with:

- Clear separation between engine and content
- Efficient git history
- Smaller footprint (92% reduction)
- Better developer experience
- Easy to understand and maintain

For more details, see:
- [Migration Summary](./MIGRATION.md) - How we got here
- [Contributing Guide](./CONTRIBUTING-DOCS.md) - How to edit docs
- [README](./README.md) - Quick start guide
